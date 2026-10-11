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

from .config import DB_PATH, env, iso, now_local, parse_dt

log = logging.getLogger("spirobuddy.store")

TABLES = ["patients", "sessions", "breaths", "slots", "messages", "breaths_labelled",
          # comms tables (backend/app/comms/, docs/COMMS.md)
          "guardians", "care_settings", "alerts", "escalations", "escalation_events", "calls",
          "cheers", "inbound_messages"]
JSON_COLS = {"features", "samples", "config", "meta"}
BOOL_COLS = {"sent", "dry_run", "is_primary", "consent"}
# timestamptz columns in supabase/schema.sql (returned in UTC by Postgres -> made local again)
TS_COLS = {"created_at", "started_at", "updated_at", "consent_at", "snooze_until", "next_at",
           "ring_until", "played_at"}
PKS = {"slots": ["patient_id", "slot_date", "slot_hour"], "care_settings": ["patient_id"]}

# ---- SpiroBuddy 2.0 tables (supabase/schema_v2.sql, spec §9), parents before children.
TABLES_V2 = ["hospitals", "staff", "auth_sessions", "access_keys", "key_grants", "care_team",
             "consents", "documents", "prescriptions", "prescription_items", "dose_events",
             "appointments", "availability", "availability_exceptions", "notes", "audit_events",
             "ai_events", "devices", "device_events", "session_curves", "pilot_checklist",
             "app_settings"]
# json / boolean / timestamptz columns of the 2.0 tables (and the new patients columns), per
# table: old tables already have plain-text columns with the same names (alerts.detail,
# escalation_events.detail) that must never be json-decoded. The global sets above still apply.
JSON_COLS_BY_TABLE = {
    "hospitals": {"languages", "departments", "wards", "settings"},
    "access_keys": {"patient_ids", "permissions"},
    "patients": {"emergency_contact", "routine"},
    "consents": {"items"},
    "documents": {"ai_suggested"},
    "prescription_items": {"times", "unclear_fields", "box_2d"},
    "audit_events": {"detail"},
    "ai_events": {"output"},
    "devices": {"calibration", "health"},
    "device_events": {"detail"},
    "session_curves": {"samples"},
    "app_settings": {"value"},
}
BOOL_COLS_BY_TABLE = {
    "hospitals": {"join_requires_approval"},
    "consents": {"read_aloud", "teach_back_ok"},
    "documents": {"visible_to_patient", "visible_to_family"},
    "prescription_items": {"as_needed"},
    "ai_events": {"ok"},
}
TS_COLS_BY_TABLE = {
    "staff": {"locked_until", "last_login_at"},
    "auth_sessions": {"expires_at", "revoked_at", "last_seen_at"},
    "access_keys": {"expires_at", "revoked_at"},
    "key_grants": {"granted_at"},
    "consents": {"withdrawn_at"},
    "documents": {"deleted_at"},
    "prescriptions": {"reviewed_at"},
    "prescription_items": {"confirmed_at"},
    "dose_events": {"due_at", "reported_at"},
    "appointments": {"start_at", "end_at"},
    "notes": {"edited_at"},
    "audit_events": {"at"},
    "ai_events": {"reviewed_at"},
    "devices": {"last_seen_at"},
    "patients": {"pin_locked_until"},
}
# Kept apart from PKS (tests/test_supabase_store.py checks every PKS entry against schema.sql).
PKS_V2 = {"app_settings": ["key"]}

V2_MISSING_NOTE = "v2 tables missing on Supabase – run supabase/schema_v2.sql; using demo SQLite"
_v2_missing = False   # set by make_store(); read with v2_missing() / service.v2_missing()

Filter = tuple[str, str, Any]


def pk(table: str) -> list[str]:
    """Primary-key columns of a table (most tables: ["id"])."""
    return PKS.get(table) or PKS_V2.get(table) or ["id"]


def json_cols(table: str | None) -> set[str]:
    return JSON_COLS | JSON_COLS_BY_TABLE.get(table, set()) if table else JSON_COLS


def bool_cols(table: str | None) -> set[str]:
    return BOOL_COLS | BOOL_COLS_BY_TABLE.get(table, set()) if table else BOOL_COLS


def ts_cols(table: str | None) -> set[str]:
    return TS_COLS | TS_COLS_BY_TABLE.get(table, set()) if table else TS_COLS


def v2_missing() -> bool:
    """True when Supabase had the old tables but not the 2.0 ones, so we fell back to SQLite."""
    return _v2_missing


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
        return len(self.select(table, columns=pk(table)[0]))


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
CREATE INDEX IF NOT EXISTS idx_calls_sid ON calls(provider_sid);
CREATE INDEX IF NOT EXISTS idx_sessions_patient ON sessions(patient_id, slot_date);
CREATE INDEX IF NOT EXISTS idx_breaths_session ON breaths(session_id);
CREATE INDEX IF NOT EXISTS idx_slots_date ON slots(slot_date);
"""

# SpiroBuddy 2.0 tables: same columns, defaults, NOT NULLs and CHECKs as supabase/schema_v2.sql
# (json -> TEXT, boolean -> INTEGER 0/1, timestamptz/date -> TEXT ISO strings).
SQLITE_DDL_V2 = """
CREATE TABLE IF NOT EXISTS hospitals (
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, city TEXT, address TEXT, phone TEXT,
  timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata', languages TEXT NOT NULL DEFAULT '[]',
  departments TEXT NOT NULL DEFAULT '[]', wards TEXT NOT NULL DEFAULT '[]', join_code_hash TEXT,
  join_code_hint TEXT, join_requires_approval INTEGER NOT NULL DEFAULT 1,
  settings TEXT NOT NULL DEFAULT '{}', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS staff (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER,
  role TEXT NOT NULL CHECK (role IN ('admin','doctor','nurse')), name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE, password_hash TEXT, phone TEXT, department TEXT, specialty TEXT,
  reg_no_display TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('pending','active','disabled')),
  failed_logins INTEGER NOT NULL DEFAULT 0, locked_until TEXT, last_login_at TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS auth_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER,
  kind TEXT NOT NULL DEFAULT 'staff' CHECK (kind IN ('staff','patient')), staff_id INTEGER,
  patient_id INTEGER, token_hash TEXT NOT NULL UNIQUE, expires_at TEXT NOT NULL, ip TEXT,
  user_agent TEXT, revoked_at TEXT, last_seen_at TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS access_keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, created_by INTEGER, label TEXT,
  key_hash TEXT NOT NULL UNIQUE, key_hint TEXT,
  scope TEXT NOT NULL DEFAULT 'patients' CHECK (scope IN ('all','patients')),
  patient_ids TEXT NOT NULL DEFAULT '[]', permissions TEXT NOT NULL DEFAULT '[]', expires_at TEXT,
  max_uses INTEGER DEFAULT 1, uses INTEGER NOT NULL DEFAULT 0, revoked_at TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS key_grants (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, key_id INTEGER NOT NULL,
  staff_id INTEGER NOT NULL, granted_at TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS care_team (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  staff_id INTEGER NOT NULL, role TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS consents (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1, items TEXT NOT NULL DEFAULT '{}', method TEXT,
  taken_by INTEGER, language TEXT, read_aloud INTEGER NOT NULL DEFAULT 0, teach_back_ok INTEGER,
  created_at TEXT NOT NULL, withdrawn_at TEXT);
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  kind TEXT NOT NULL DEFAULT 'other', title TEXT, doc_date TEXT, source TEXT,
  storage_path TEXT NOT NULL, mime TEXT, size INTEGER, sha256 TEXT, thumb_path TEXT,
  uploaded_by_role TEXT, uploaded_by_id INTEGER, visible_to_patient INTEGER NOT NULL DEFAULT 0,
  visible_to_family INTEGER NOT NULL DEFAULT 0, ai_suggested TEXT, deleted_at TEXT,
  created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS prescriptions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  source TEXT, document_id INTEGER,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','needs_review','approved',
    'rejected','stopped','superseded')),
  version INTEGER NOT NULL DEFAULT 1, supersedes_id INTEGER, prescriber_on_paper TEXT,
  prescribed_on TEXT, ai_event_id INTEGER, reviewed_by INTEGER, reviewed_at TEXT,
  created_by INTEGER, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS prescription_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, prescription_id INTEGER NOT NULL,
  patient_id INTEGER, line_no INTEGER, drug_name TEXT, form TEXT, strength TEXT, dose_qty REAL,
  dose_unit TEXT, frequency_raw TEXT, frequency_code TEXT, times TEXT, food_timing TEXT,
  duration_raw TEXT, duration_days INTEGER, start_date TEXT, end_date TEXT,
  as_needed INTEGER NOT NULL DEFAULT 0, instructions_raw TEXT, confidence REAL,
  unclear_fields TEXT NOT NULL DEFAULT '[]', box_2d TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','confirmed','edited',
    'removed')),
  confirmed_by INTEGER, confirmed_at TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS dose_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  item_id INTEGER, due_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'upcoming',
  reported_at TEXT, reported_by_role TEXT, reported_by_id INTEGER, channel TEXT, note TEXT,
  snooze_until TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS appointments (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  doctor_id INTEGER, department TEXT, kind TEXT NOT NULL DEFAULT 'follow_up',
  start_at TEXT NOT NULL, end_at TEXT,
  status TEXT NOT NULL DEFAULT 'requested' CHECK (status IN ('requested','confirmed','cancelled',
    'attended','no_show','declined')),
  requested_by_role TEXT, reason_text TEXT, location TEXT, notes TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS availability (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, doctor_id INTEGER NOT NULL,
  weekday INTEGER NOT NULL, start_time TEXT NOT NULL, end_time TEXT NOT NULL,
  slot_minutes INTEGER NOT NULL DEFAULT 15, location TEXT, valid_from TEXT, valid_to TEXT,
  created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS availability_exceptions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, doctor_id INTEGER NOT NULL,
  date TEXT NOT NULL, kind TEXT NOT NULL CHECK (kind IN ('leave','extra')), start_time TEXT,
  end_time TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, patient_id INTEGER NOT NULL,
  author_id INTEGER, kind TEXT NOT NULL DEFAULT 'note', text TEXT NOT NULL, edited_at TEXT,
  created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, at TEXT, actor_type TEXT,
  actor_id INTEGER, actor_role TEXT, action TEXT NOT NULL, resource_type TEXT, resource_id TEXT,
  patient_id INTEGER, detail TEXT, ip TEXT, request_id TEXT, prev_hash TEXT, hash TEXT,
  created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS ai_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, purpose TEXT NOT NULL,
  provider TEXT, model TEXT, prompt_version TEXT, input_ref TEXT, output TEXT,
  latency_ms INTEGER, ok INTEGER NOT NULL DEFAULT 0, error TEXT, patient_id INTEGER,
  reviewed_by INTEGER, reviewed_at TEXT, decision TEXT, lines_total INTEGER,
  lines_edited INTEGER, lines_removed INTEGER, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, serial TEXT NOT NULL, model TEXT,
  spirometer_model TEXT, firmware TEXT, battery_pct INTEGER, state TEXT NOT NULL DEFAULT 'ready',
  assigned_patient_id INTEGER, last_seen_at TEXT, calibration TEXT, health TEXT,
  created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS device_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, device_id INTEGER NOT NULL,
  kind TEXT NOT NULL, by_staff_id INTEGER, detail TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS session_curves (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, session_id INTEGER,
  patient_id INTEGER NOT NULL, samples TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS pilot_checklist (
  id INTEGER PRIMARY KEY AUTOINCREMENT, hospital_id INTEGER, step_no INTEGER NOT NULL,
  title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'todo', owner TEXT, due TEXT,
  evidence_url TEXT, note TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS app_settings (
  key TEXT PRIMARY KEY, hospital_id INTEGER, value TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
-- one live (requested or confirmed) visit per doctor per start time: no double booking
CREATE UNIQUE INDEX IF NOT EXISTS idx_appt_no_double_booking ON appointments(doctor_id, start_at)
  WHERE status IN ('requested','confirmed');
CREATE INDEX IF NOT EXISTS idx_staff_hospital ON staff(hospital_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_staff ON auth_sessions(staff_id);
CREATE INDEX IF NOT EXISTS idx_key_grants_staff ON key_grants(staff_id);
CREATE INDEX IF NOT EXISTS idx_care_team_patient ON care_team(patient_id);
CREATE INDEX IF NOT EXISTS idx_care_team_staff ON care_team(staff_id);
CREATE INDEX IF NOT EXISTS idx_consents_patient ON consents(patient_id);
CREATE INDEX IF NOT EXISTS idx_documents_patient ON documents(patient_id);
CREATE INDEX IF NOT EXISTS idx_rx_patient ON prescriptions(patient_id, status);
CREATE INDEX IF NOT EXISTS idx_rx_status ON prescriptions(status);
CREATE INDEX IF NOT EXISTS idx_rx_items_rx ON prescription_items(prescription_id);
CREATE INDEX IF NOT EXISTS idx_dose_patient_due ON dose_events(patient_id, due_at);
CREATE INDEX IF NOT EXISTS idx_dose_status_due ON dose_events(status, due_at);
CREATE INDEX IF NOT EXISTS idx_appt_patient ON appointments(patient_id, start_at);
CREATE INDEX IF NOT EXISTS idx_appt_doctor ON appointments(doctor_id, start_at);
CREATE INDEX IF NOT EXISTS idx_appt_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_availability_doctor ON availability(doctor_id);
CREATE INDEX IF NOT EXISTS idx_avail_exc_doctor ON availability_exceptions(doctor_id, date);
CREATE INDEX IF NOT EXISTS idx_notes_patient ON notes(patient_id, created_at);
CREATE INDEX IF NOT EXISTS idx_audit_hospital_at ON audit_events(hospital_id, at);
CREATE INDEX IF NOT EXISTS idx_audit_patient ON audit_events(patient_id, at);
CREATE INDEX IF NOT EXISTS idx_ai_events_created ON ai_events(created_at);
CREATE INDEX IF NOT EXISTS idx_devices_hospital ON devices(hospital_id);
CREATE INDEX IF NOT EXISTS idx_device_events_device ON device_events(device_id, created_at);
CREATE INDEX IF NOT EXISTS idx_curves_session ON session_curves(session_id);
CREATE INDEX IF NOT EXISTS idx_curves_patient ON session_curves(patient_id);
"""

# (table, column, type) added to existing local databases on start-up
SQLITE_ADD_COLUMNS = [("guardians", "consent", "INTEGER DEFAULT 0"),
                      ("guardians", "consent_at", "TEXT"),
                      # 2.0 patients columns (schema_v2.sql: alter table public.patients ...)
                      ("patients", "hospital_id", "INTEGER"),
                      ("patients", "primary_doctor_id", "INTEGER"),
                      ("patients", "ward", "TEXT"),
                      ("patients", "bed", "TEXT"),
                      ("patients", "mrn", "TEXT"),
                      ("patients", "phone", "TEXT"),
                      ("patients", "city", "TEXT"),
                      ("patients", "emergency_contact", "TEXT"),
                      ("patients", "allergies_text", "TEXT"),
                      ("patients", "discharge_date", "TEXT"),
                      ("patients", "programme_status", "TEXT NOT NULL DEFAULT 'active'"),
                      ("patients", "routine", "TEXT"),
                      ("patients", "app_token_hash", "TEXT"),
                      ("patients", "app_token_hint", "TEXT"),
                      # patient login with the registration number + PIN (schema_v2.sql, same names)
                      ("patients", "pin_hash", "TEXT"),
                      ("patients", "pin_failed", "INTEGER NOT NULL DEFAULT 0"),
                      ("patients", "pin_locked_until", "TEXT")]
# These three exist on Supabase only after schema_v2.sql is pasted again. Until then the site must
# keep running, so they are NOT probed by check_v2_tables() and patient login says "not set up yet".
PATIENT_LOGIN_COLS = ("pin_hash", "pin_failed", "pin_locked_until")

# run after SQLITE_ADD_COLUMNS (these index columns that older databases only get then)
SQLITE_DDL_V2_AFTER = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_patients_app_token ON patients(app_token_hash);
CREATE INDEX IF NOT EXISTS idx_patients_hospital ON patients(hospital_id);
CREATE INDEX IF NOT EXISTS idx_patients_doctor ON patients(primary_doctor_id);
"""
SQLITE_PATIENT_MRN_INDEX = ("CREATE UNIQUE INDEX IF NOT EXISTS idx_patients_hospital_mrn "
                            "ON patients(coalesce(hospital_id, 0), lower(mrn)) WHERE mrn IS NOT NULL")
_V2 = set(TABLES_V2)

_SQL_OPS = {"eq": "=", "neq": "!=", "gte": ">=", "lte": "<=", "gt": ">", "lt": "<"}


def _encode(row: dict, table: str | None = None) -> dict:
    """Python values -> SQLite values. A str in a json column is taken as already-encoded JSON."""
    jcols, bcols = json_cols(table), bool_cols(table)
    out = {}
    for k, v in row.items():
        if k in jcols and v is not None and not isinstance(v, str):
            v = json.dumps(v)
        elif k in bcols and v is not None:
            v = 1 if v else 0
        out[k] = v
    return out


def _decode(row: dict, table: str | None = None) -> dict:
    for k in json_cols(table) & row.keys():
        if isinstance(row[k], str):
            try:
                row[k] = json.loads(row[k])
            except ValueError:
                pass
    for k in bool_cols(table) & row.keys():
        if row[k] is not None:
            row[k] = bool(row[k])
    return row


def _with_defaults(table: str, row: dict) -> dict:
    """2.0 tables: fill created_at (and app_settings.updated_at) when the caller left it out,
    like Postgres' "not null default now()" on Supabase. An explicit None fails on both."""
    if table in _V2:
        for col in ("created_at", "updated_at") if table == "app_settings" else ("created_at",):
            if col not in row:
                row = {**row, col: iso(now_local())}
    return row


class SqliteStore(Store):
    name = "demo"

    def __init__(self, path=DB_PATH):
        self.path = str(path)
        self.lock = threading.RLock()
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SQLITE_DDL)
        self.conn.executescript(SQLITE_DDL_V2)
        for table, col, typ in SQLITE_ADD_COLUMNS:     # columns added after a table existed
            have = {r[1] for r in self.conn.execute(f"PRAGMA table_info({table})")}
            if col not in have:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
        self.conn.executescript(SQLITE_DDL_V2_AFTER)
        try:        # one registration number per hospital, ignoring case; a duplicate must not stop start-up
            self.conn.execute(SQLITE_PATIENT_MRN_INDEX)
        except sqlite3.Error as e:
            log.warning("registration-number index not created (duplicate numbers?): %s", e)
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
        return [_decode(dict(r), table) for r in rows]

    def insert(self, table, rows):
        out = []
        with self.lock:
            for row in rows:
                row = _with_defaults(table, row)
                r = _encode(row, table)
                cols = list(r.keys())
                cur = self.conn.execute(
                    f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                    [r[c] for c in cols])
                new = dict(row)
                if table not in ("slots", "app_settings"):
                    new["id"] = cur.lastrowid
                out.append(new)
            self.conn.commit()
        return out

    def update(self, table, filters, values):
        where, args = self._where(filters)
        v = _encode(values, table)
        sets = ",".join(f"{k}=?" for k in v)
        with self.lock:
            self.conn.execute(f"UPDATE {table} SET {sets}{where}", list(v.values()) + args)
            self.conn.commit()

    def upsert(self, table, rows):
        with self.lock:
            for row in rows:
                r = _encode(_with_defaults(table, row), table)
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

def _same_keys(rows: list[dict]) -> list[list[dict]]:
    """PostgREST bulk inserts need every object to have the same keys: group rows by key set."""
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        groups.setdefault(tuple(sorted(r.keys())), []).append(r)
    return list(groups.values())


def _pg_value(v) -> str:
    """A value inside a PostgREST in.(...) list: quote it if it has reserved characters."""
    s = str(v)
    if any(c in s for c in ',()" \\'):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


PATIENTS_V2_COLS = [c for t, c, _ in SQLITE_ADD_COLUMNS
                    if t == "patients" and c not in PATIENT_LOGIN_COLS]


class V2TablesMissing(RuntimeError):
    """Supabase has the old tables but not the 2.0 ones: supabase/schema_v2.sql wasn't run."""

    def __init__(self, tables: list[str]):
        self.tables = list(tables)
        super().__init__("2.0 tables missing on Supabase: " + ", ".join(self.tables)
                         + " - run supabase/schema_v2.sql in the Supabase SQL Editor")


class SupabaseStore(Store):
    """Supabase Postgres through PostgREST (https://<ref>.supabase.co/rest/v1/<table>).

    Auth: the key always goes in the `apikey` header. Legacy JWT keys (service_role, start
    with "eyJ") also go in `Authorization: Bearer`; new `sb_secret_...` keys must NOT
    (Supabase docs: "Send publishable and secret keys on the apikey header").

    Rows come back looking like SqliteStore rows: timestamps as local ISO strings
    (Postgres would return UTC, e.g. "...T04:35:00.123+00:00"), jsonb as dict/list.
    """
    name = "supabase"
    PAGE = 1000   # Supabase caps rows per response (default max-rows 1000), so page through

    def __init__(self, url: str, key: str, client=None, check_v2: bool = False):
        if client is None:
            import httpx
            headers = {"apikey": key, "Content-Type": "application/json"}
            if key.startswith("eyJ"):
                headers["Authorization"] = f"Bearer {key}"
            client = httpx.Client(base_url=url.rstrip("/") + "/rest/v1", headers=headers,
                                  timeout=15.0)
        self.client = client
        # Fail fast (-> demo fallback with a clear note) if the key is wrong or a table is missing.
        for t in TABLES:
            r = self.client.get(f"/{t}", params={"select": "*", "limit": "0"})
            if r.status_code >= 400:
                hint = (" - run supabase/schema.sql in the Supabase SQL Editor"
                        if self._is_missing(r) else "")
                raise RuntimeError(f"table {t}: HTTP {r.status_code} {r.text[:160]}{hint}")
        if check_v2:       # make_store() asks for this; the old tests build the store without it
            self.check_v2_tables()

    @staticmethod
    def _is_missing(r) -> bool:
        return r.status_code in (404, 400) or "does not exist" in r.text or "schema cache" in r.text

    def check_v2_tables(self) -> None:
        """Raise V2TablesMissing if schema_v2.sql hasn't been run (a 2.0 table or a new
        patients column is missing). Any other error (wrong key, outage) is a RuntimeError."""
        probes = [(t, "*") for t in TABLES_V2] + [("patients", ",".join(PATIENTS_V2_COLS))]
        missing = []
        for t, cols in probes:
            r = self.client.get(f"/{t}", params={"select": cols, "limit": "0"})
            if r.status_code < 400:
                continue
            if not self._is_missing(r):
                raise RuntimeError(f"table {t}: HTTP {r.status_code} {r.text[:160]}")
            missing.append(t if cols == "*" else f"{t} (2.0 columns)")
        if missing:
            raise V2TablesMissing(missing)

    @staticmethod
    def _params(filters: Iterable[Filter]) -> list[tuple[str, str]]:
        params = []
        for col, op, val in filters:
            if op == "in":
                vals = ",".join(_pg_value(v) for v in val)
                params.append((col, f"in.({vals})"))
            elif isinstance(val, bool):
                params.append((col, f"{op}.{'true' if val else 'false'}"))
            elif val is None:
                params.append((col, "is.null" if op == "eq" else "not.is.null"))
            else:
                params.append((col, f"{op}.{val}"))
        return params

    @staticmethod
    def _decode(row: dict, table: str | None = None) -> dict:
        tcols, jcols = ts_cols(table), json_cols(table)
        for k, v in row.items():
            if k in tcols and isinstance(v, str) and v:
                try:
                    row[k] = iso(parse_dt(v))
                except ValueError:
                    pass
            elif k in jcols and isinstance(v, str):
                try:
                    row[k] = json.loads(v)
                except ValueError:
                    pass
        return row

    def _check(self, r):
        if r.status_code >= 400:
            raise RuntimeError(f"Supabase {r.request.method} {r.request.url.path}: "
                               f"{r.status_code} {r.text[:300]}")
        return r

    def select(self, table, filters=(), order=None, desc=False, limit=None, columns="*"):
        base = [("select", columns)] + self._params(filters)
        # Always order (tie-break on the primary key) so paging with offset is stable.
        direction = "desc" if desc else "asc"
        keys = ([f"{order}.{direction}"] if order else []) + \
               [f"{k}.{direction}" for k in pk(table) if k != order]
        base.append(("order", ",".join(keys)))
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
        return [self._decode(r, table) for r in out]

    def insert(self, table, rows):
        out = []
        for group in _same_keys(rows):
            for i in range(0, len(group), 500):
                chunk = group[i:i + 500]
                r = self._check(self.client.post(f"/{table}", json=chunk,
                                                 headers={"Prefer": "return=representation"}))
                out.extend(self._decode(x, table) for x in r.json())
        return out

    def update(self, table, filters, values):
        self._check(self.client.patch(f"/{table}", params=self._params(filters), json=values,
                                      headers={"Prefer": "return=minimal"}))

    def upsert(self, table, rows):
        keys = pk(table)
        for group in _same_keys(rows):
            self._check(self.client.post(
                f"/{table}", params={"on_conflict": ",".join(keys)}, json=group,
                headers={"Prefer": "resolution=merge-duplicates,return=minimal"}))

    def delete(self, table, filters):
        self._check(self.client.delete(f"/{table}", params=self._params(filters)))

    def count(self, table):
        col = pk(table)[0]
        r = self._check(self.client.get(f"/{table}", params={"select": col, "limit": "1"},
                                        headers={"Prefer": "count=exact"}))
        rng = r.headers.get("content-range", "*/0")   # e.g. "0-0/42"
        try:
            return int(rng.split("/")[-1])
        except ValueError:
            return len(self.select(table, columns=col))


# ----------------------------------------------------------------------------- factory

def make_store() -> tuple[Store, str]:
    """Return (store, note). Falls back to SQLite with a warning if Supabase isn't usable.

    If Supabase has the old tables but not the 2.0 ones, the note is V2_MISSING_NOTE and
    v2_missing() turns True (the hospital pages show "Database update needed")."""
    global _v2_missing
    _v2_missing = False
    want = env("DATA_BACKEND", "demo").lower()
    if want == "supabase":
        url, key = env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            note = "DATA_BACKEND=supabase but SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY missing; using demo SQLite"
            log.warning(note)
            return SqliteStore(), note
        try:
            return SupabaseStore(url, key, check_v2=True), "supabase connected"
        except V2TablesMissing as e:
            _v2_missing = True
            log.warning("%s (missing: %s)", V2_MISSING_NOTE, ", ".join(e.tables))
            return SqliteStore(), V2_MISSING_NOTE
        except Exception as e:  # unreachable, wrong key, tables missing...
            note = f"Supabase unreachable ({str(e)[:200]}); using demo SQLite"
            log.warning(note)
            return SqliteStore(), note
    return SqliteStore(), "demo SQLite"
