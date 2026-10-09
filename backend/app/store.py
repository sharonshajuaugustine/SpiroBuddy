"""Data store: one small table-level interface, two implementations.

- SqliteStore   : demo / local / fallback. File backend/data/spirobuddy.db.
- SupabaseStore : Supabase Postgres via its REST API (PostgREST) using httpx.
                  Chosen with DATA_BACKEND=supabase + SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY.

Filters are lists of (column, op, value) with op in: eq, neq, gte, lte, gt, lt, in.
Tables and columns follow docs/ARCHITECTURE.md section 10.
"""
from __future__ import annotations

import json
import logging
import sqlite3
import threading
from typing import Any, Iterable

from .config import DB_PATH, env

log = logging.getLogger("spirobuddy.store")

TABLES = ["patients", "sessions", "breaths", "slots", "messages", "breaths_labelled",
          # comms tables (backend/app/comms/, docs/COMMS.md)
          "guardians", "care_settings", "alerts", "escalations", "escalation_events", "calls",
          "cheers", "inbound_messages"]
JSON_COLS = {"features", "samples", "config", "meta"}
BOOL_COLS = {"sent", "dry_run", "is_primary", "consent"}
PKS = {"slots": ["patient_id", "slot_date", "slot_hour"], "care_settings": ["patient_id"]}

Filter = tuple[str, str, Any]


class Store:
    name = "base"   # "demo" or "supabase"

    def select(self, table: str, filters: Iterable[Filter] = (), order: str | None = None,
               desc: bool = False, limit: int | None = None, columns: str = "*") -> list[dict]:
        raise NotImplementedError

    def insert(self, table: str, rows: list[dict]) -> list[dict]:
        """Insert rows, return them with their generated ids (same order is NOT guaranteed)."""
        raise NotImplementedError

    def update(self, table: str, filters: Iterable[Filter], values: dict) -> None:
        raise NotImplementedError

    def upsert(self, table: str, rows: list[dict]) -> None:
        """Insert or replace on the table's primary key (used for slots)."""
        raise NotImplementedError

    def delete(self, table: str, filters: Iterable[Filter]) -> None:
        raise NotImplementedError

    def count(self, table: str) -> int:
        return len(self.select(table, columns="id" if table != "slots" else "patient_id"))


# ----------------------------------------------------------------------------- SQLite

SQLITE_DDL = """
CREATE TABLE IF NOT EXISTS patients (
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER, sex TEXT,
  surgery TEXT, surgery_date TEXT, language TEXT DEFAULT 'en', target_ml INTEGER DEFAULT 2000,
  hold_target_s REAL DEFAULT 3, family_phone TEXT, nurse_phone TEXT,
  personal_best_ml REAL DEFAULT 0, created_at TEXT);
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER REFERENCES patients(id),
  started_at TEXT, slot_date TEXT, slot_hour INTEGER, breaths_count INTEGER,
  best_ml REAL, avg_score REAL, source TEXT DEFAULT 'demo');
CREATE TABLE IF NOT EXISTS breaths (
  id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER REFERENCES sessions(id),
  patient_id INTEGER, t INTEGER, features TEXT, label TEXT, score REAL);
CREATE TABLE IF NOT EXISTS slots (
  patient_id INTEGER, slot_date TEXT, slot_hour INTEGER, status TEXT, session_id INTEGER,
  PRIMARY KEY (patient_id, slot_date, slot_hour));
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, kind TEXT, to_role TEXT,
  to_number TEXT, text TEXT, sent INTEGER, dry_run INTEGER, created_at TEXT);
CREATE TABLE IF NOT EXISTS breaths_labelled (
  id INTEGER PRIMARY KEY AUTOINCREMENT, person TEXT, label TEXT, samples TEXT,
  features TEXT, created_at TEXT);
-- comms tables (backend/app/comms/, docs/COMMS.md)
CREATE TABLE IF NOT EXISTS guardians (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, name TEXT, relation TEXT,
  phone TEXT, language TEXT DEFAULT 'hi', channel TEXT DEFAULT 'both', city TEXT,
  quiet_start TEXT, quiet_end TEXT, is_primary INTEGER DEFAULT 0, consent INTEGER DEFAULT 0,
  consent_at TEXT, token TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS care_settings (
  patient_id INTEGER PRIMARY KEY, config TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, kind TEXT, severity TEXT,
  title TEXT, detail TEXT, status TEXT DEFAULT 'open', assigned_to TEXT, snooze_until TEXT,
  run_id INTEGER, created_at TEXT, updated_at TEXT, acted_by TEXT);
CREATE TABLE IF NOT EXISTS escalations (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, reason TEXT, status TEXT,
  speed TEXT, step_index INTEGER, next_at TEXT, slot_date TEXT, slot_hour INTEGER,
  snoozes INTEGER DEFAULT 0, outcome TEXT, meta TEXT, created_at TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS escalation_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, run_id INTEGER, kind TEXT,
  channel TEXT, actor TEXT, to_name TEXT, title TEXT, detail TEXT, status TEXT, ref_id INTEGER,
  created_at TEXT);
CREATE TABLE IF NOT EXISTS calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, run_id INTEGER, guardian_id INTEGER,
  to_role TEXT, to_name TEXT, to_number TEXT, purpose TEXT, provider TEXT, provider_sid TEXT,
  status TEXT, digits TEXT, outcome TEXT, language TEXT, script TEXT, meta TEXT,
  ring_until TEXT, created_at TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS cheers (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, guardian_id INTEGER, from_name TEXT,
  text TEXT, language TEXT, status TEXT DEFAULT 'queued', created_at TEXT, played_at TEXT);
CREATE TABLE IF NOT EXISTS inbound_messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, guardian_id INTEGER,
  from_number TEXT, from_role TEXT, from_name TEXT, channel TEXT, body TEXT, intent TEXT,
  reply TEXT, created_at TEXT);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status, patient_id);
CREATE INDEX IF NOT EXISTS idx_events_patient ON escalation_events(patient_id, created_at);
CREATE INDEX IF NOT EXISTS idx_calls_status ON calls(status);
CREATE INDEX IF NOT EXISTS idx_sessions_patient ON sessions(patient_id, slot_date);
CREATE INDEX IF NOT EXISTS idx_breaths_session ON breaths(session_id);
CREATE INDEX IF NOT EXISTS idx_slots_date ON slots(slot_date);
"""

# (table, column, type) added to existing local databases on start-up
SQLITE_ADD_COLUMNS = [("guardians", "consent", "INTEGER DEFAULT 0"),
                      ("guardians", "consent_at", "TEXT")]

_SQL_OPS = {"eq": "=", "neq": "!=", "gte": ">=", "lte": "<=", "gt": ">", "lt": "<"}


def _encode(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        if k in JSON_COLS and v is not None and not isinstance(v, str):
            v = json.dumps(v)
        elif k in BOOL_COLS and v is not None:
            v = 1 if v else 0
        out[k] = v
    return out


def _decode(row: dict) -> dict:
    for k in JSON_COLS & row.keys():
        if isinstance(row[k], str):
            try:
                row[k] = json.loads(row[k])
            except ValueError:
                pass
    for k in BOOL_COLS & row.keys():
        if row[k] is not None:
            row[k] = bool(row[k])
    return row


class SqliteStore(Store):
    name = "demo"

    def __init__(self, path=DB_PATH):
        self.path = str(path)
        self.lock = threading.RLock()
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SQLITE_DDL)
        for table, col, typ in SQLITE_ADD_COLUMNS:     # columns added after a table existed
            have = {r[1] for r in self.conn.execute(f"PRAGMA table_info({table})")}
            if col not in have:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
        self.conn.commit()

    @staticmethod
    def _where(filters: Iterable[Filter]) -> tuple[str, list]:
        parts, args = [], []
        for col, op, val in filters:
            if op == "in":
                vals = list(val)
                if not vals:
                    parts.append("0")
                    continue
                parts.append(f"{col} IN ({','.join('?' * len(vals))})")
                args.extend(vals)
            else:
                parts.append(f"{col} {_SQL_OPS[op]} ?")
                args.append(val)
        return (" WHERE " + " AND ".join(parts)) if parts else "", args

    def select(self, table, filters=(), order=None, desc=False, limit=None, columns="*"):
        where, args = self._where(filters)
        sql = f"SELECT {columns} FROM {table}{where}"
        if order:
            sql += f" ORDER BY {order} {'DESC' if desc else 'ASC'}"
        if limit:
            sql += f" LIMIT {int(limit)}"
        with self.lock:
            rows = self.conn.execute(sql, args).fetchall()
        return [_decode(dict(r)) for r in rows]

    def insert(self, table, rows):
        out = []
        with self.lock:
            for row in rows:
                r = _encode(row)
                cols = list(r.keys())
                cur = self.conn.execute(
                    f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                    [r[c] for c in cols])
                new = dict(row)
                if table != "slots":
                    new["id"] = cur.lastrowid
                out.append(new)
            self.conn.commit()
        return out

    def update(self, table, filters, values):
        where, args = self._where(filters)
        v = _encode(values)
        sets = ",".join(f"{k}=?" for k in v)
        with self.lock:
            self.conn.execute(f"UPDATE {table} SET {sets}{where}", list(v.values()) + args)
            self.conn.commit()

    def upsert(self, table, rows):
        with self.lock:
            for row in rows:
                r = _encode(row)
                cols = list(r.keys())
                self.conn.execute(
                    f"INSERT OR REPLACE INTO {table} ({','.join(cols)}) "
                    f"VALUES ({','.join('?' * len(cols))})", [r[c] for c in cols])
            self.conn.commit()

    def delete(self, table, filters):
        where, args = self._where(filters)
        with self.lock:
            self.conn.execute(f"DELETE FROM {table}{where}", args)
            self.conn.commit()

    def count(self, table):
        with self.lock:
            return self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


# ----------------------------------------------------------------------------- Supabase

class SupabaseStore(Store):
    """Supabase Postgres through PostgREST (https://<ref>.supabase.co/rest/v1/<table>).

    Auth: the key always goes in the `apikey` header. Legacy JWT keys (service_role, start
    with "eyJ") also go in `Authorization: Bearer`; new `sb_secret_...` keys must NOT
    (Supabase docs: "Send publishable and secret keys on the apikey header").
    """
    name = "supabase"
    PAGE = 1000   # Supabase caps rows per response (default max-rows 1000), so page through

    def __init__(self, url: str, key: str):
        import httpx
        headers = {"apikey": key, "Content-Type": "application/json"}
        if key.startswith("eyJ"):
            headers["Authorization"] = f"Bearer {key}"
        self.client = httpx.Client(base_url=url.rstrip("/") + "/rest/v1", headers=headers,
                                   timeout=15.0)
        self.client.get("/patients", params={"select": "id", "limit": "1"}).raise_for_status()

    @staticmethod
    def _params(filters: Iterable[Filter]) -> list[tuple[str, str]]:
        params = []
        for col, op, val in filters:
            if op == "in":
                vals = ",".join(str(v) for v in val)
                params.append((col, f"in.({vals})"))
            elif isinstance(val, bool):
                params.append((col, f"{op}.{'true' if val else 'false'}"))
            else:
                params.append((col, f"{op}.{val}"))
        return params

    def _check(self, r):
        if r.status_code >= 400:
            raise RuntimeError(f"Supabase {r.request.method} {r.request.url.path}: "
                               f"{r.status_code} {r.text[:300]}")
        return r

    def select(self, table, filters=(), order=None, desc=False, limit=None, columns="*"):
        base = [("select", columns)] + self._params(filters)
        if order:
            base.append(("order", f"{order}.{'desc' if desc else 'asc'}"))
        out: list[dict] = []
        offset = 0
        while True:
            want = self.PAGE if limit is None else min(self.PAGE, limit - len(out))
            params = base + [("limit", str(want)), ("offset", str(offset))]
            rows = self._check(self.client.get(f"/{table}", params=params)).json()
            out.extend(rows)
            offset += len(rows)
            if len(rows) < want or (limit is not None and len(out) >= limit):
                break
        return out

    def insert(self, table, rows):
        out = []
        for i in range(0, len(rows), 500):
            chunk = rows[i:i + 500]
            r = self._check(self.client.post(f"/{table}", json=chunk,
                                             headers={"Prefer": "return=representation"}))
            out.extend(r.json())
        return out

    def update(self, table, filters, values):
        self._check(self.client.patch(f"/{table}", params=self._params(filters), json=values))

    def upsert(self, table, rows):
        pk = PKS.get(table, ["id"])
        self._check(self.client.post(
            f"/{table}", params={"on_conflict": ",".join(pk)}, json=rows,
            headers={"Prefer": "resolution=merge-duplicates,return=minimal"}))

    def delete(self, table, filters):
        self._check(self.client.delete(f"/{table}", params=self._params(filters)))

    def count(self, table):
        col = "patient_id" if table == "slots" else "id"
        r = self._check(self.client.get(f"/{table}", params={"select": col, "limit": "1"},
                                        headers={"Prefer": "count=exact"}))
        rng = r.headers.get("content-range", "*/0")   # e.g. "0-0/42"
        try:
            return int(rng.split("/")[-1])
        except ValueError:
            return len(self.select(table, columns=col))


# ----------------------------------------------------------------------------- factory

def make_store() -> tuple[Store, str]:
    """Return (store, note). Falls back to SQLite with a warning if Supabase isn't usable."""
    want = env("DATA_BACKEND", "demo").lower()
    if want == "supabase":
        url, key = env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            note = "DATA_BACKEND=supabase but SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY missing; using demo SQLite"
            log.warning(note)
            return SqliteStore(), note
        try:
            return SupabaseStore(url, key), "supabase connected"
        except Exception as e:  # unreachable, wrong key, tables missing...
            note = f"Supabase unreachable ({str(e)[:200]}); using demo SQLite"
            log.warning(note)
            return SqliteStore(), note
    return SqliteStore(), "demo SQLite"
