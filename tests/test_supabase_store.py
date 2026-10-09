"""SupabaseStore against a fake Supabase (no account, no internet).

FakePostgrest answers the same HTTP calls PostgREST would (GET/POST/PATCH/DELETE on
/rest/v1/<table>) from an in-memory SQLite database, and checks every write against
supabase/schema.sql: column names, NOT NULL columns, CHECK (... in (...)) lists and value
types. Like real Postgres it returns timestamps in UTC and booleans/jsonb as JSON values.
So these tests catch: a column the code writes that schema.sql lacks, a demo value the
schema rejects, bulk inserts with mixed keys (PostgREST PGRST102), DELETE without a filter
(Supabase's safeupdate), and wrong query syntax.
"""
from __future__ import annotations

import json
import re
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest

from backend.app import store as store_mod
from backend.app.store import SQLITE_DDL, TABLES, SupabaseStore

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_SQL = (ROOT / "supabase" / "schema.sql").read_text(encoding="utf-8")
SEED_SQL = (ROOT / "supabase" / "seed.sql").read_text(encoding="utf-8")


# ----------------------------------------------------------------------------- schema.sql

def parse_schema(sql: str) -> dict[str, dict[str, dict]]:
    tables: dict[str, dict[str, dict]] = {}
    for m in re.finditer(r"create table if not exists public\.(\w+)\s*\((.*?)\n\);", sql, re.S):
        cols = {}
        for line in m.group(2).splitlines():
            line = line.split("--")[0].strip().rstrip(",")
            mm = re.match(r"(\w+)\s+(bigint|int|text|real|date|timestamptz|jsonb|boolean)\b(.*)", line)
            if not mm:
                continue
            name, typ, rest = mm.groups()
            chk = re.search(r"check \(\w+ in \(([^)]*)\)\)", rest)
            cols[name] = {
                "type": typ,
                "required": "not null" in rest and "default" not in rest
                            and "identity" not in rest,
                "allowed": [v.strip().strip("'") for v in chk.group(1).split(",")] if chk else None,
            }
        tables[m.group(1)] = cols
    for m in re.finditer(r"alter table public\.(\w+)\s+add column if not exists (\w+)\s+(\w+)", sql):
        tables[m.group(1)].setdefault(m.group(2), {"type": m.group(3), "required": False,
                                                   "allowed": None})
    for m in re.finditer(r"drop constraint if exists (\w+?)_(\w+)_check", sql):
        if m.group(1) in tables and m.group(2) in tables[m.group(1)]:
            tables[m.group(1)][m.group(2)]["allowed"] = None
    return tables


SCHEMA = parse_schema(SCHEMA_SQL)


def _type_ok(typ: str, v) -> bool:
    if v is None:
        return True
    if typ in ("int", "bigint"):
        return isinstance(v, int) and not isinstance(v, bool)
    if typ == "real":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if typ == "boolean":
        return isinstance(v, bool)
    if typ == "text":
        return isinstance(v, str)
    if typ == "date":
        return isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) is not None
    if typ == "timestamptz":
        try:
            datetime.fromisoformat(str(v).replace("Z", "+00:00"))
            return True
        except ValueError:
            return False
    return True  # jsonb: anything JSON


# ----------------------------------------------------------------------------- fake PostgREST

class FakePostgrest:
    RESERVED = {"select", "order", "limit", "offset", "on_conflict", "columns"}

    def __init__(self):
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SQLITE_DDL)
        self.lock = threading.RLock()
        self.log: list[httpx.Request] = []
        self.missing_tables: set[str] = set()

    def client(self, headers=None) -> httpx.Client:
        return httpx.Client(base_url="https://demo.supabase.co/rest/v1",
                            headers=headers or {"apikey": "sb_secret_test"},
                            transport=httpx.MockTransport(self.handle))

    # -- helpers
    @staticmethod
    def _err(code: int, msg: str) -> httpx.Response:
        return httpx.Response(code, json={"code": "FAKE", "message": msg})

    def _validate(self, table: str, row: dict, insert: bool) -> str | None:
        cols = SCHEMA[table]
        for k, v in row.items():
            if k not in cols:
                return f'column "{k}" of relation "{table}" does not exist (not in schema.sql)'
            c = cols[k]
            if not _type_ok(c["type"], v):
                return f"{table}.{k}: {v!r} is not a valid {c['type']}"
            if c["allowed"] and v is not None and v not in c["allowed"]:
                return f'{table}.{k}: {v!r} violates check constraint ({c["allowed"]})'
            if v is None and c["required"]:
                return f'null value in column "{k}" of "{table}" violates not-null constraint'
        if insert:
            for k, c in cols.items():
                if c["required"] and k not in row:
                    return f'null value in column "{k}" of "{table}" violates not-null constraint'
        return None

    @staticmethod
    def _to_db(row: dict) -> dict:
        return {k: json.dumps(v) if isinstance(v, (dict, list)) else
                (int(v) if isinstance(v, bool) else v) for k, v in row.items()}

    def _out(self, table: str, row: dict) -> dict:
        cols = SCHEMA[table]
        out = {}
        for k, v in row.items():
            typ = cols.get(k, {}).get("type")
            if typ == "boolean" and v is not None:
                v = bool(v)
            elif typ == "jsonb" and isinstance(v, str):
                v = json.loads(v)
            elif typ == "timestamptz" and v:   # Postgres answers in UTC
                v = datetime.fromisoformat(v).astimezone(timezone.utc).isoformat()
            out[k] = v
        return out

    @staticmethod
    def _split_in(s: str) -> list[str]:
        vals, cur, quoted, i = [], "", False, 0
        while i < len(s):
            ch = s[i]
            if quoted and ch == "\\":
                cur += s[i + 1]
                i += 2
                continue
            if ch == '"':
                quoted = not quoted
            elif ch == "," and not quoted:
                vals.append(cur)
                cur = ""
            else:
                cur += ch
            i += 1
        vals.append(cur)
        return vals

    def _where(self, params) -> tuple[str, list]:
        ops = {"eq": "=", "neq": "!=", "gte": ">=", "lte": "<=", "gt": ">", "lt": "<"}
        parts, args = [], []
        for k, v in params.multi_items():
            if k in self.RESERVED:
                continue
            if v == "is.null":
                parts.append(f"{k} IS NULL")
                continue
            if v == "not.is.null":
                parts.append(f"{k} IS NOT NULL")
                continue
            op, _, val = v.partition(".")
            if op == "in":
                assert val.startswith("(") and val.endswith(")"), v
                vals = self._split_in(val[1:-1])
                parts.append(f"{k} IN ({','.join('?' * len(vals))})" if vals else "0")
                args += vals
            else:
                assert op in ops, f"unknown operator in {k}={v}"
                parts.append(f"{k} {ops[op]} ?")
                args.append({"true": 1, "false": 0}.get(val, val))
        return (" WHERE " + " AND ".join(parts)) if parts else "", args

    # -- the HTTP handler
    def handle(self, request: httpx.Request) -> httpx.Response:
        with self.lock:
            self.log.append(request)
            table = request.url.path.split("/rest/v1/")[-1]
            if table not in SCHEMA or table in self.missing_tables:
                return self._err(404, f'relation "public.{table}" does not exist')
            p = request.url.params
            prefer = request.headers.get("prefer", "")
            where, args = self._where(p)
            m = request.method
            if m == "GET":
                sql = f"SELECT {p.get('select', '*')} FROM {table}{where}"
                if p.get("order"):
                    sql += " ORDER BY " + ", ".join(
                        f"{c.rsplit('.', 1)[0]} {c.rsplit('.', 1)[1].upper()}"
                        for c in p["order"].split(","))
                if p.get("limit") is not None:
                    sql += f" LIMIT {int(p['limit'])} OFFSET {int(p.get('offset', 0))}"
                rows = [self._out(table, dict(r)) for r in self.db.execute(sql, args)]
                headers = {}
                if "count=exact" in prefer:
                    n = self.db.execute(f"SELECT COUNT(*) FROM {table}{where}", args).fetchone()[0]
                    headers["content-range"] = f"0-{max(len(rows) - 1, 0)}/{n}" if n else "*/0"
                return httpx.Response(200, json=rows, headers=headers)
            if m == "POST":
                body = json.loads(request.content)
                rows = body if isinstance(body, list) else [body]
                if len({tuple(sorted(r)) for r in rows}) > 1:
                    return self._err(400, "All object keys must match")   # PGRST102
                for r in rows:
                    err = self._validate(table, r, insert=True)
                    if err:
                        return self._err(400, err)
                conflict = p.get("on_conflict")
                if conflict:
                    assert "resolution=merge-duplicates" in prefer
                    pk = store_mod.PKS.get(table, ["id"])
                    assert conflict.split(",") == pk, f"on_conflict {conflict} is not the PK {pk}"
                out = []
                for r in rows:
                    d = self._to_db(r)
                    verb = "INSERT OR REPLACE" if conflict else "INSERT"
                    cur = self.db.execute(
                        f"{verb} INTO {table} ({','.join(d)}) VALUES ({','.join('?' * len(d))})",
                        list(d.values()))
                    if "id" in SCHEMA[table]:
                        full = self.db.execute(f"SELECT * FROM {table} WHERE id = ?",
                                               [cur.lastrowid]).fetchone()
                        out.append(self._out(table, dict(full)))
                    else:
                        out.append(r)
                if "return=representation" in prefer:
                    return httpx.Response(201, json=out)
                return httpx.Response(201)
            if m == "PATCH":
                vals = json.loads(request.content)
                err = self._validate(table, vals, insert=False)
                if err:
                    return self._err(400, err)
                if not where:
                    return self._err(400, "UPDATE requires a WHERE clause")
                d = self._to_db(vals)
                self.db.execute(f"UPDATE {table} SET {','.join(f'{k}=?' for k in d)}{where}",
                                list(d.values()) + args)
                return httpx.Response(204)
            if m == "DELETE":
                if not where:
                    return self._err(400, "DELETE requires a WHERE clause")
                self.db.execute(f"DELETE FROM {table}{where}", args)
                return httpx.Response(204)
            return self._err(405, m)


@pytest.fixture()
def fake():
    return FakePostgrest()


@pytest.fixture()
def sb(fake):
    return SupabaseStore("https://demo.supabase.co", "sb_secret_test", client=fake.client())


# ----------------------------------------------------------------------------- schema checks

def test_schema_sql_has_every_store_table_and_sqlite_column():
    """Every table and column of the local SQLite demo store also exists in schema.sql."""
    con = sqlite3.connect(":memory:")
    con.executescript(SQLITE_DDL)
    for t in TABLES:
        assert t in SCHEMA, f"table {t} missing from supabase/schema.sql"
        sqlite_cols = {r[1] for r in con.execute(f"PRAGMA table_info({t})")}
        missing = sqlite_cols - set(SCHEMA[t])
        assert not missing, f"{t}: columns {missing} missing from supabase/schema.sql"
    for t, cols in store_mod.PKS.items():
        assert re.search(rf"primary key \({', '.join(cols)}\)", SCHEMA_SQL) or \
            re.search(rf"{cols[0]}\s+bigint primary key", SCHEMA_SQL), f"{t}: PK {cols} for upsert"


def test_schema_keeps_rls_on_and_never_opens_anon():
    for t in TABLES:
        assert re.search(rf"alter table public\.{t}\s+enable row level security", SCHEMA_SQL), t
    assert "create policy" not in SCHEMA_SQL.lower()
    assert not re.search(r"grant [^;]* to (anon|authenticated)", SCHEMA_SQL, re.I)


def test_seed_sql_matches_demo_seed():
    from backend.app.seed import PROFILES
    for pid, p in PROFILES.items():
        m = re.search(rf"\({pid}, '([^']+)',\s+(\d+), '(\w)', '([^']+)',\s+current_date - (\d+), "
                      rf"'(\w+)', (\d+),", SEED_SQL)
        assert m, f"patient {pid} missing in supabase/seed.sql"
        name, age, sex, surgery, days, lang, target = m.groups()
        assert (name, int(age), sex, surgery, int(days), lang, int(target)) == (
            p["name"], p["age"], p["sex"], p["surgery"], p["surgery_days_ago"], p["language"],
            p["target_ml"]), f"seed.sql patient {pid} differs from backend/app/seed.py"
        allowed = SCHEMA["patients"]["language"]["allowed"]
        assert allowed is None or lang in allowed, f"schema.sql rejects language {lang!r}"


# ----------------------------------------------------------------------------- request shapes

def test_connect_probes_every_table_and_reports_missing(fake):
    SupabaseStore("https://demo.supabase.co", "k", client=fake.client())
    probed = {r.url.path.rsplit("/", 1)[-1] for r in fake.log}
    assert probed == set(TABLES)
    fake.missing_tables.add("guardians")
    with pytest.raises(RuntimeError, match="guardians.*schema.sql"):
        SupabaseStore("https://demo.supabase.co", "k", client=fake.client())


def test_auth_headers_for_new_and_legacy_keys(monkeypatch):
    seen = {}

    class Client:
        def __init__(self, base_url, headers, timeout):
            seen.update(base_url=base_url, headers=headers)

        def get(self, *a, **k):
            return httpx.Response(200, json=[], request=httpx.Request("GET", "https://x"))

    monkeypatch.setattr(httpx, "Client", Client)
    SupabaseStore("https://abc.supabase.co/", "sb_secret_xyz")
    assert seen["base_url"] == "https://abc.supabase.co/rest/v1"
    assert seen["headers"]["apikey"] == "sb_secret_xyz" and "Authorization" not in seen["headers"]
    SupabaseStore("https://abc.supabase.co", "eyJhbGciOi.legacy")
    assert seen["headers"]["Authorization"] == "Bearer eyJhbGciOi.legacy"


def test_select_query_string(sb, fake):
    fake.log.clear()
    sb.select("alerts", [("status", "neq", "resolved"), ("patient_id", "in", [3, 5]),
                         ("created_at", "gte", "2026-10-10T09:00:00+05:30")],
              order="created_at", desc=True, limit=5, columns="id,title")
    q = fake.log[-1].url.params
    assert fake.log[-1].method == "GET" and fake.log[-1].url.path == "/rest/v1/alerts"
    assert q["select"] == "id,title"
    assert q["status"] == "neq.resolved" and q["patient_id"] == "in.(3,5)"
    assert q["created_at"] == "gte.2026-10-10T09:00:00+05:30"
    assert b"%2B05%3A30" in fake.log[-1].url.query or b"%2B05:30" in fake.log[-1].url.query  # '+' not a space
    assert q["order"] == "created_at.desc,id.desc" and q["limit"] == "5" and q["offset"] == "0"


def test_in_filter_quotes_strings_and_bools_are_lowercase(sb, fake):
    fake.log.clear()
    sb.select("calls", [("status", "in", ["ringing", "in-progress", "a,b"])])
    assert fake.log[-1].url.params["status"] == 'in.(ringing,in-progress,"a,b")'
    sb.select("guardians", [("is_primary", "eq", True)])
    assert fake.log[-1].url.params["is_primary"] == "eq.true"


def test_select_pages_past_1000_rows(sb, fake):
    sb.insert("breaths_labelled", [{"person": "p", "label": "good", "samples": [], "features": {},
                                    "created_at": "2026-10-10T10:00:00+05:30"}] * 1203)
    fake.log.clear()
    rows = sb.select("breaths_labelled", columns="id")
    assert len(rows) == 1203 and len({r["id"] for r in rows}) == 1203
    offsets = [r.url.params["offset"] for r in fake.log]
    assert offsets == ["0", "1000"]


def test_insert_upsert_update_delete_payloads(sb, fake):
    fake.log.clear()
    rows = sb.insert("patients", [{"id": 1, "name": "Test", "language": "ml",
                                   "created_at": "2026-10-10T10:00:00+05:30"}])
    req = fake.log[-1]
    assert req.method == "POST" and req.headers["prefer"] == "return=representation"
    assert json.loads(req.content) == [{"id": 1, "name": "Test", "language": "ml",
                                        "created_at": "2026-10-10T10:00:00+05:30"}]
    # comes back like SqliteStore: local time, defaults filled in
    assert rows[0]["created_at"] == "2026-10-10T10:00:00+05:30" and rows[0]["target_ml"] == 2000

    sb.upsert("slots", [{"patient_id": 1, "slot_date": "2026-10-10", "slot_hour": 9,
                         "status": "done", "session_id": None}])
    req = fake.log[-1]
    assert req.url.params["on_conflict"] == "patient_id,slot_date,slot_hour"
    assert "resolution=merge-duplicates" in req.headers["prefer"]
    sb.upsert("slots", [{"patient_id": 1, "slot_date": "2026-10-10", "slot_hour": 9,
                         "status": "missed", "session_id": None}])
    assert [s["status"] for s in sb.select("slots")] == ["missed"]
    sb.upsert("care_settings", [{"patient_id": 1, "config": {"a": 1},
                                 "updated_at": "2026-10-10T10:00:00+05:30"}])
    assert fake.log[-1].url.params["on_conflict"] == "patient_id"
    assert sb.select("care_settings")[0]["config"] == {"a": 1}

    sb.update("patients", [("id", "eq", 1)], {"personal_best_ml": 1234.5})
    req = fake.log[-1]
    assert req.method == "PATCH" and req.url.params["id"] == "eq.1"
    assert json.loads(req.content) == {"personal_best_ml": 1234.5}

    sb.delete("slots", [("patient_id", "gte", 0)])
    assert fake.log[-1].method == "DELETE" and fake.log[-1].url.params["patient_id"] == "gte.0"
    assert sb.count("slots") == 0 and sb.count("patients") == 1
    assert fake.log[-1].headers["prefer"] == "count=exact"


def test_mixed_key_rows_are_split_into_matching_batches(sb, fake):
    out = sb.insert("inbound_messages", [{"patient_id": None, "body": "a"},
                                         {"patient_id": None, "body": "b", "intent": "x"}])
    assert len(out) == 2 and {r["body"] for r in out} == {"a", "b"}


def test_timestamps_and_booleans_come_back_like_sqlite(sb):
    sb.insert("patients", [{"id": 1, "name": "T"}])
    sb.insert("messages", [{"patient_id": 1, "kind": "x", "text": "hi", "sent": False,
                            "dry_run": True, "created_at": "2026-10-10T20:30:00+05:30"}])
    m = sb.select("messages")[0]
    assert m["created_at"] == "2026-10-10T20:30:00+05:30"
    assert m["sent"] is False and m["dry_run"] is True


# ----------------------------------------------------------------------------- whole demo

def test_demo_seed_and_api_run_on_supabase_store(client, fake):
    """Seed + the main screens through SupabaseStore: every write must fit schema.sql."""
    from backend.app import service
    sb = SupabaseStore("https://demo.supabase.co", "sb_secret_test", client=fake.client())
    old = service._store, service._store_note
    service._store, service._store_note = sb, "supabase connected"
    try:
        r = client.post("/api/demo/reset")
        assert r.status_code == 200, r.text
        assert sb.count("patients") == 7
        assert sb.count("guardians") >= 10 and sb.count("care_settings") == 7
        assert sb.count("alerts") >= 3 and sb.count("escalation_events") >= 10
        assert sb.select("guardians", [("token", "eq", "ravi-amit-demo")])
        assert {p["language"] for p in sb.select("patients")} >= {"hi", "ta", "ml", "en"}
        h = client.get("/api/health").json()
        assert h["data_backend"] == "supabase"
        pts = client.get("/api/patients").json()
        assert len(pts) == 7 and {"red", "yellow", "green"} <= {p["status"] for p in pts}
        for url in ("/api/patients/1", "/api/patients/1/sessions", "/api/messages",
                    "/api/comms/alerts", "/api/comms/events", "/api/comms/calls",
                    "/api/comms/guardian/ravi-amit-demo"):
            r = client.get(url)
            assert r.status_code == 200, f"{url}: {r.text[:300]}"
        r = client.post("/api/demo/simulate/1", json={"quality": "mixed"})
        assert r.status_code == 200, r.text
        r = client.post("/api/demo/miss/5")
        assert r.status_code == 200, r.text
        r = client.post("/api/whatsapp/2", json={})
        assert r.status_code == 200, r.text
        r = client.post("/api/collect", json={"person": "t", "label": "good", "samples": [],
                                              "features": {"peak_ml": 1800}})
        assert r.status_code == 200, r.text
        assert service.export_labelled_csv() == 1
    finally:
        service._store, service._store_note = old
        client.post("/api/demo/reset")
