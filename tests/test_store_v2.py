"""SpiroBuddy 2.0 data layer: the new tables in SQLite and supabase/schema_v2.sql, per-table
json/bool handling, the double-booking guard, the "v2 tables missing" fallback and the new
settings. No Supabase account and no internet: Supabase is faked with httpx.MockTransport.
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

import httpx
import pytest

from backend.app import config, service
from backend.app import store as store_mod
from backend.app.store import (SQLITE_DDL, TABLES, TABLES_V2, SqliteStore, SupabaseStore,
                               V2TablesMissing)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_V2_SQL = (ROOT / "supabase" / "schema_v2.sql").read_text(encoding="utf-8")

# Spec §9 columns (plus hospital_id and created_at on every new table).
SPEC_COLUMNS = {
    "hospitals": "name city address phone timezone languages join_code_hash join_requires_approval settings",
    "staff": "hospital_id role name email password_hash phone department specialty reg_no_display "
             "status failed_logins locked_until last_login_at",
    "auth_sessions": "staff_id token_hash expires_at ip user_agent revoked_at kind patient_id last_seen_at",
    "access_keys": "created_by label key_hash key_hint scope patient_ids permissions expires_at max_uses "
                   "uses revoked_at",
    "key_grants": "key_id staff_id granted_at",
    "care_team": "patient_id staff_id role",
    "consents": "patient_id version items method taken_by language read_aloud teach_back_ok created_at "
                "withdrawn_at",
    "prescriptions": "patient_id source document_id status version supersedes_id prescriber_on_paper "
                     "prescribed_on ai_event_id reviewed_by reviewed_at created_by",
    "prescription_items": "prescription_id patient_id line_no drug_name form strength dose_qty dose_unit "
                          "frequency_raw frequency_code times food_timing duration_raw duration_days "
                          "start_date end_date as_needed instructions_raw confidence unclear_fields box_2d "
                          "status confirmed_by confirmed_at",
    "dose_events": "patient_id item_id due_at status reported_at reported_by_role reported_by_id channel note",
    "appointments": "patient_id doctor_id department kind start_at end_at status requested_by_role "
                    "reason_text location notes",
    "availability": "doctor_id weekday start_time end_time slot_minutes location valid_from valid_to",
    "availability_exceptions": "doctor_id date kind start_time end_time",
    "documents": "patient_id kind title doc_date storage_path mime size sha256 thumb_path uploaded_by_role "
                 "uploaded_by_id visible_to_patient visible_to_family ai_suggested deleted_at",
    "notes": "patient_id author_id kind text edited_at",
    "audit_events": "at actor_type actor_id actor_role action resource_type resource_id patient_id detail "
                    "ip request_id prev_hash hash",
    "ai_events": "purpose provider model prompt_version input_ref output latency_ms ok error patient_id "
                 "reviewed_by decision lines_total lines_edited lines_removed",
    "devices": "serial model spirometer_model firmware battery_pct state assigned_patient_id last_seen_at "
               "calibration health",
    "device_events": "device_id kind by_staff_id detail",
    "session_curves": "session_id patient_id samples",
    "pilot_checklist": "step_no title status owner due evidence_url note",
    "app_settings": "key value",
}
PATIENT_COLUMNS = ("hospital_id primary_doctor_id ward bed mrn phone city emergency_contact allergies_text "
                   "discharge_date programme_status routine app_token_hash app_token_hint "
                   "pin_hash pin_failed pin_locked_until").split()

# The least each table needs for an insert (NOT NULL columns without a default).
MINIMAL = {
    "hospitals": {"name": "Demo General Hospital (fictional)"},
    "staff": {"role": "doctor", "name": "Dr. Test", "email": "test.doctor@demo-general.example"},
    "auth_sessions": {"token_hash": "h1", "expires_at": "2026-10-12T10:00:00+05:30"},
    "access_keys": {"key_hash": "k1"},
    "key_grants": {"key_id": 1, "staff_id": 4},
    "care_team": {"patient_id": 1, "staff_id": 2},
    "consents": {"patient_id": 1},
    "documents": {"patient_id": 1, "storage_path": "docs/202610/abc.png"},
    "prescriptions": {"patient_id": 1},
    "prescription_items": {"prescription_id": 1},
    "dose_events": {"patient_id": 1, "due_at": "2026-10-11T08:00:00+05:30"},
    "appointments": {"patient_id": 1, "start_at": "2026-10-15T10:30:00+05:30"},
    "availability": {"doctor_id": 2, "weekday": 0, "start_time": "09:00", "end_time": "13:00"},
    "availability_exceptions": {"doctor_id": 2, "date": "2026-10-20", "kind": "leave"},
    "notes": {"patient_id": 1, "text": "Called, all well."},
    "audit_events": {"action": "patient.view"},
    "ai_events": {"purpose": "rx_extract"},
    "devices": {"serial": "SB-TEST-0001"},
    "device_events": {"device_id": 1, "kind": "assign"},
    "session_curves": {"patient_id": 1},
    "pilot_checklist": {"step_no": 1, "title": "Ethics committee approval"},
    "app_settings": {"key": "test_setting"},
    "patients": {"name": "Test Patient (fake)"},
}
JSON_SAMPLES = {"languages": ["en", "hi"], "departments": ["Surgery"], "wards": ["W1"],
                "settings": {"grace_minutes": 60, "ai_enabled": True},
                "patient_ids": [1, 2], "permissions": ["view", "acknowledge_alerts"],
                "emergency_contact": {"name": "Fake Contact", "relation": "son"},
                "routine": {"wake": "07:00", "bed": "22:00"},
                "items": {"care_reminders": True, "ai_training": False},
                "ai_suggested": {"kind": "lab_report", "title": "CBC", "doc_date": "2026-10-01"},
                "times": ["08:00", "20:00"], "unclear_fields": ["strength"],
                "box_2d": [10, 20, 30, 40], "detail": {"n": 123, "why": "test"},
                "output": {"lines": [{"line_no": 1}]}, "calibration": {"offset_ml": 0},
                "health": {"battery": "ok"}, "samples": [0, 120.5, 300], "value": {"public": "x"}}


@pytest.fixture()
def st(tmp_path):
    return SqliteStore(tmp_path / "v2.db")


# ----------------------------------------------------------------------------- schema_v2.sql

def parse_v2(sql: str) -> dict[str, dict[str, dict]]:
    tables: dict[str, dict[str, dict]] = {}
    for m in re.finditer(r"create table if not exists public\.(\w+)\s*\((.*?)\n\);", sql, re.S):
        cols = {}
        for line in m.group(2).splitlines():
            line = line.split("--")[0].strip().rstrip(",")
            mm = re.match(r"(\w+)\s+(bigint|int|text|real|date|timestamptz|jsonb|boolean)\b(.*)", line)
            if mm:
                chk = re.search(r"check \(\w+ in \(([^)]*)\)\)", mm.group(3))
                cols[mm.group(1)] = {"type": mm.group(2), "rest": mm.group(3),
                                     "allowed": [v.strip().strip("'") for v in chk.group(1).split(",")]
                                     if chk else None}
        tables[m.group(1)] = cols
    tables["patients"] = {
        m.group(1): {"type": m.group(2), "rest": "", "allowed": None}
        for m in re.finditer(r"alter table public\.patients add column if not exists (\w+)\s+(\w+)", sql)}
    return tables


V2 = parse_v2(SCHEMA_V2_SQL)
SQLITE_TYPE = {"bigint": "INTEGER", "int": "INTEGER", "boolean": "INTEGER", "real": "REAL",
               "text": "TEXT", "date": "TEXT", "timestamptz": "TEXT", "jsonb": "TEXT"}


def sqlite_cols(st: SqliteStore, table: str) -> dict[str, str]:
    return {r[1]: r[2].upper() for r in st.conn.execute(f"PRAGMA table_info({table})")}


def test_every_v2_table_has_the_spec_columns_in_sqlite_and_schema_v2(st):
    assert set(SPEC_COLUMNS) == set(TABLES_V2) and not set(TABLES) & set(TABLES_V2)
    for t in TABLES_V2:
        have = sqlite_cols(st, t)
        want = set(SPEC_COLUMNS[t].split()) | {"created_at"} | ({"hospital_id"} if t != "hospitals" else set())
        assert not want - set(have), f"SQLite {t}: missing {want - set(have)}"
        assert t in V2, f"schema_v2.sql has no table {t}"
        assert set(V2[t]) == set(have), f"{t}: SQLite and schema_v2.sql columns differ: " \
                                        f"{set(V2[t]) ^ set(have)}"
        for col, c in V2[t].items():
            assert have[col] == SQLITE_TYPE[c["type"]], f"{t}.{col}: {have[col]} vs {c['type']}"
    pat = sqlite_cols(st, "patients")
    assert set(PATIENT_COLUMNS) <= set(pat) and set(V2["patients"]) == set(PATIENT_COLUMNS)


def test_store_json_bool_and_time_sets_match_schema_v2():
    for t, cols in V2.items():
        jsonb = {c for c, v in cols.items() if v["type"] == "jsonb"}
        boolean = {c for c, v in cols.items() if v["type"] == "boolean"}
        ts = {c for c, v in cols.items() if v["type"] == "timestamptz"}
        assert jsonb == store_mod.json_cols(t) & set(cols), f"{t}: jsonb {jsonb}"
        assert boolean == store_mod.bool_cols(t) & set(cols), f"{t}: boolean {boolean}"
        assert ts == store_mod.ts_cols(t) & set(cols), f"{t}: timestamptz {ts}"
    # the old tables are untouched: their plain-text "detail" is never json
    assert "detail" not in store_mod.json_cols("alerts") | store_mod.json_cols("escalation_events")


def test_schema_v2_is_additive_safe_and_locked_down():
    low = SCHEMA_V2_SQL.lower()
    code = "\n".join(line.split("--")[0] for line in low.splitlines())
    assert not re.search(r"\bdrop\s+(table|column|index|constraint)\b|\brename\b|\btruncate\b|\bdelete\s+from\b", code)
    assert "create policy" not in code
    assert not re.search(r"grant [^;]* to (anon|authenticated)", code)
    assert len(re.findall(r"create table (?!if not exists)", code)) == 0
    assert len(re.findall(r"create (unique )?index (?!if not exists)", code)) == 0
    for t in TABLES_V2:
        assert re.search(rf"alter table public\.{t}\s+enable row level security", code), t
        if t != "app_settings":
            assert re.search(rf"create table if not exists public\.{t} \(\s*id\s+bigint generated by "
                             r"default as identity \(start with 1000\) primary key", code), t
    assert re.search(r"key\s+text primary key", code)
    assert re.search(r"create unique index if not exists \w+\s+on public\.appointments \(doctor_id, "
                     r"start_at\) where status in \('requested','confirmed'\)", code)
    assert "on public.staff (lower(email))" in code and "key_hash    text not null unique" in code
    assert "token_hash   text not null unique" in code
    assert "pg_get_serial_sequence('public.patients','id')" in code and "greatest(1000" in code
    assert code.rstrip().endswith("notify pgrst, 'reload schema';")
    assert "grant select, insert, update, delete on all tables in schema public to service_role" in code


# ----------------------------------------------------------------------------- SQLite behaviour

def test_old_local_database_upgrades_on_start(tmp_path):
    path = tmp_path / "old.db"
    con = sqlite3.connect(path)
    con.executescript(SQLITE_DDL)   # a database made before 2.0
    con.execute("INSERT INTO patients (id, name) VALUES (1, 'Old Patient (fake)')")
    con.commit()
    con.close()
    st = SqliteStore(path)
    p = st.select("patients")[0]
    assert p["programme_status"] == "active" and p["hospital_id"] is None
    assert set(PATIENT_COLUMNS) <= set(p)
    for t in TABLES_V2:
        assert st.count(t) == 0
    SqliteStore(path)   # and starting again is fine


@pytest.mark.parametrize("table", sorted(set(store_mod.JSON_COLS_BY_TABLE) | set(store_mod.BOOL_COLS_BY_TABLE)))
def test_json_and_bool_round_trip_per_table(st, table):
    row = dict(MINIMAL[table])
    for col in store_mod.JSON_COLS_BY_TABLE.get(table, ()):
        row[col] = JSON_SAMPLES[col]
    bools = store_mod.BOOL_COLS_BY_TABLE.get(table, ())
    for col in bools:
        row[col] = True
    st.insert(table, [row])
    got = st.select(table)[0]
    for col in store_mod.JSON_COLS_BY_TABLE.get(table, ()):
        assert got[col] == JSON_SAMPLES[col], f"{table}.{col}"
    for col in bools:
        assert got[col] is True, f"{table}.{col}"
    # stored as text / 0-1 underneath
    key, val = store_mod.pk(table)[0], got[store_mod.pk(table)[0]]
    raw = dict(st.conn.execute(f"SELECT * FROM {table} WHERE {key} = ?", [val]).fetchone())
    for col in bools:
        assert raw[col] == 1
    # update keeps the same encoding; False stays False (not None)
    st.update(table, [(key, "eq", val)], {c: False for c in bools} or
              {c: {"changed": 1} for c in store_mod.JSON_COLS_BY_TABLE[table]})
    got = st.select(table, [(key, "eq", val)])[0]
    assert all(got[c] is False for c in bools)
    if not bools:
        assert all(got[c] == {"changed": 1} for c in store_mod.JSON_COLS_BY_TABLE[table])


def test_defaults_decode_like_postgres(st):
    st.insert("hospitals", [MINIMAL["hospitals"]])
    h = st.select("hospitals")[0]
    assert h["languages"] == [] and h["settings"] == {} and h["join_requires_approval"] is True
    assert h["timezone"] == "Asia/Kolkata" and h["created_at"]
    st.insert("access_keys", [MINIMAL["access_keys"]])
    k = st.select("access_keys")[0]
    assert k["patient_ids"] == [] and k["permissions"] == [] and k["scope"] == "patients"
    assert k["uses"] == 0 and k["max_uses"] == 1
    st.insert("prescription_items", [MINIMAL["prescription_items"]])
    i = st.select("prescription_items")[0]
    assert i["as_needed"] is False and i["unclear_fields"] == [] and i["status"] == "pending"
    st.insert("ai_events", [MINIMAL["ai_events"]])
    assert st.select("ai_events")[0]["ok"] is False
    st.insert("consents", [MINIMAL["consents"]])
    c = st.select("consents")[0]
    assert c["read_aloud"] is False and c["teach_back_ok"] is None and c["items"] == {}
    st.insert("auth_sessions", [MINIMAL["auth_sessions"]])
    assert st.select("auth_sessions")[0]["kind"] == "staff"
    # created_at missing -> filled (Postgres: default now()); explicit None fails like Postgres
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("notes", [{**MINIMAL["notes"], "created_at": None}])


def test_old_text_detail_columns_stay_text(st):
    st.insert("alerts", [{"patient_id": 1, "kind": "missed", "detail": "123",
                          "created_at": "2026-10-11T10:00:00+05:30"}])
    st.insert("escalation_events", [{"patient_id": 1, "kind": "x", "detail": "[1, 2]"}])
    st.insert("audit_events", [{"action": "patient.view", "detail": {"n": 123}}])
    assert st.select("alerts")[0]["detail"] == "123"
    assert st.select("escalation_events")[0]["detail"] == "[1, 2]"
    assert st.select("audit_events")[0]["detail"] == {"n": 123}
    # also on the Supabase decode path
    assert SupabaseStore._decode({"detail": "123"}, "alerts") == {"detail": "123"}
    assert SupabaseStore._decode({"detail": '{"n": 1}'}, "audit_events") == {"detail": {"n": 1}}
    assert SupabaseStore._decode({"detail": "123"}) == {"detail": "123"}


def test_appointments_double_booking_guard(st):
    a = {"patient_id": 1, "doctor_id": 2, "start_at": "2026-10-15T10:30:00+05:30",
         "status": "confirmed"}
    first = st.insert("appointments", [a])[0]
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("appointments", [{**a, "patient_id": 3}])
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("appointments", [{**a, "patient_id": 3, "status": "requested"}])
    st.insert("appointments", [{**a, "doctor_id": 3}])                       # another doctor: fine
    st.insert("appointments", [{**a, "patient_id": 4, "status": "declined"}])  # not live: fine
    st.update("appointments", [("id", "eq", first["id"])], {"status": "cancelled"})
    st.insert("appointments", [{**a, "patient_id": 3}])                       # slot free again
    live = st.select("appointments", [("doctor_id", "eq", 2), ("status", "in", ["requested", "confirmed"])])
    assert [r["patient_id"] for r in live] == [3]


def test_unique_keys_and_checks(st):
    st.insert("staff", [MINIMAL["staff"]])
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("staff", [{**MINIMAL["staff"], "name": "Copy"}])
    st.insert("access_keys", [MINIMAL["access_keys"]])
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("access_keys", [MINIMAL["access_keys"]])
    st.insert("auth_sessions", [MINIMAL["auth_sessions"]])
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("auth_sessions", [MINIMAL["auth_sessions"]])
    st.insert("patients", [{"name": "A (fake)", "app_token_hash": "t1"}, {"name": "B (fake)"},
                           {"name": "C (fake)"}])   # many NULL tokens are fine
    with pytest.raises(sqlite3.IntegrityError):
        st.insert("patients", [{"name": "D (fake)", "app_token_hash": "t1"}])


def test_sqlite_check_constraints_match_schema_v2(st):
    """Every check (col in (...)) list in schema_v2.sql is enforced the same way in SQLite."""
    checked = 0
    for t, cols in V2.items():
        for col, c in cols.items():
            if not c["allowed"]:
                continue
            key = store_mod.pk(t)[0]
            for i, v in enumerate(c["allowed"]):
                row = {**MINIMAL[t], col: v}
                if t == "staff":
                    row["email"] = f"ok{i}@demo-general.example"
                for u in ("token_hash", "key_hash"):
                    if u in row:
                        row[u] = f"{u}-{col}-{i}"
                if t == "appointments":
                    row["start_at"] = f"2026-10-15T1{i}:00:00+05:30"
                st.insert(t, [row])
            with pytest.raises(sqlite3.IntegrityError):
                st.insert(t, [{**MINIMAL[t], col: "not-a-valid-value"}])
            st.delete(t, [(key, "gte", 0)])
            checked += 1
    assert checked >= 8


def test_app_settings_upsert_by_key(st):
    st.upsert("app_settings", [{"key": "vapid_keys", "value": {"public": "a"}}])
    st.upsert("app_settings", [{"key": "vapid_keys", "value": {"public": "b"}}])
    rows = st.select("app_settings")
    assert len(rows) == 1 and rows[0]["value"] == {"public": "b"} and "id" not in rows[0]
    assert st.count("app_settings") == 1 and rows[0]["updated_at"]


# ----------------------------------------------------------------------------- Supabase fallback

class FakeSupabase:
    """Answers PostgREST probes: 200 for known tables, 404 for the ones in `missing`."""

    def __init__(self, missing=(), status_for=None, no_patient_v2_cols=False, rows=None):
        self.missing, self.status_for = set(missing), status_for or {}
        self.no_patient_v2_cols, self.rows = no_patient_v2_cols, rows or {}
        self.log: list[httpx.Request] = []

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.log.append(request)
        table = request.url.path.rsplit("/", 1)[-1]
        if table in self.status_for:
            return httpx.Response(self.status_for[table], json={"message": "nope"})
        if table in self.missing or table not in set(TABLES) | set(TABLES_V2):
            return httpx.Response(404, json={"code": "PGRST205",
                                             "message": f"Could not find the table 'public.{table}' in the schema cache"})
        if table == "patients" and self.no_patient_v2_cols and "hospital_id" in request.url.params.get("select", ""):
            return httpx.Response(400, json={"code": "42703", "message": "column patients.hospital_id does not exist"})
        if request.method == "GET":
            return httpx.Response(200, json=self.rows.get(table, []),
                                  headers={"content-range": f"*/{len(self.rows.get(table, []))}"})
        return httpx.Response(201)

    def client(self) -> httpx.Client:
        return httpx.Client(base_url="https://demo.supabase.co/rest/v1",
                            headers={"apikey": "sb_secret_test"},
                            transport=httpx.MockTransport(self.handle))


@pytest.fixture()
def supabase_env(monkeypatch):
    """make_store() talks to a FakeSupabase; the module flag is restored afterwards."""
    monkeypatch.setattr(store_mod, "_v2_missing", False)
    monkeypatch.setenv("DATA_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "https://demo.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "sb_secret_test")
    real_client = httpx.Client

    def use(fake: FakeSupabase):
        monkeypatch.setattr(httpx, "Client",
                            lambda **kw: real_client(transport=httpx.MockTransport(fake.handle), **kw))
        return fake
    return use


def test_store_without_check_v2_probes_only_the_old_tables():
    fake = FakeSupabase(missing={"dose_events"})
    SupabaseStore("https://demo.supabase.co", "k", client=fake.client())
    assert {r.url.path.rsplit("/", 1)[-1] for r in fake.log} == set(TABLES)


def test_v2_check_raises_a_distinct_error():
    fake = FakeSupabase(missing={"dose_events", "staff"})
    with pytest.raises(V2TablesMissing) as e:
        SupabaseStore("https://demo.supabase.co", "k", client=fake.client(), check_v2=True)
    assert e.value.tables == ["staff", "dose_events"] and "schema_v2.sql" in str(e.value)
    probed = {r.url.path.rsplit("/", 1)[-1] for r in fake.log}
    assert probed == set(TABLES) | set(TABLES_V2)
    # the old v1 message and behaviour are unchanged (v1 is checked first)
    fake = FakeSupabase(missing={"guardians", "staff"})
    with pytest.raises(RuntimeError, match="guardians.*schema.sql") as e:
        SupabaseStore("https://demo.supabase.co", "k", client=fake.client(), check_v2=True)
    assert not isinstance(e.value, V2TablesMissing)


def test_make_store_falls_back_when_v2_tables_are_missing(supabase_env, client):
    supabase_env(FakeSupabase(missing={"prescription_items"}))
    st, note = store_mod.make_store()
    assert isinstance(st, SqliteStore)
    assert note == "v2 tables missing on Supabase – run supabase/schema_v2.sql; using demo SQLite"
    assert store_mod.v2_missing() is True and service.v2_missing() is True
    assert client.get("/api/health").json()["v2_missing"] is True


def test_make_store_flags_missing_patient_columns(supabase_env):
    supabase_env(FakeSupabase(no_patient_v2_cols=True))
    st, note = store_mod.make_store()
    assert isinstance(st, SqliteStore) and note == store_mod.V2_MISSING_NOTE and store_mod.v2_missing()


def test_make_store_connects_when_everything_is_there(supabase_env):
    supabase_env(FakeSupabase())
    store_mod._v2_missing = True     # a stale flag from an earlier start is cleared
    st, note = store_mod.make_store()
    assert isinstance(st, SupabaseStore) and note == "supabase connected"
    assert store_mod.v2_missing() is False


def test_make_store_keeps_the_old_notes(supabase_env):
    supabase_env(FakeSupabase(missing={"alerts"}))
    st, note = store_mod.make_store()
    assert isinstance(st, SqliteStore) and note.startswith("Supabase unreachable (table alerts")
    assert "schema.sql" in note and not store_mod.v2_missing()
    supabase_env(FakeSupabase(status_for={"hospitals": 401}))    # a v2 probe fails for another reason
    st, note = store_mod.make_store()
    assert isinstance(st, SqliteStore) and note.startswith("Supabase unreachable (table hospitals")
    assert not store_mod.v2_missing()


def test_health_reports_v2_missing_false_by_default(client):
    h = client.get("/api/health").json()
    assert h["v2_missing"] is False and h["data_backend"] == "demo"


def test_supabase_reads_v2_rows_like_sqlite():
    fake = FakeSupabase(rows={
        "audit_events": [{"id": 1, "at": "2026-10-11T04:30:00+00:00", "detail": {"a": 1},
                          "created_at": "2026-10-11T04:30:00.123+00:00"}],
        "alerts": [{"id": 1, "detail": "123", "created_at": "2026-10-11T04:30:00+00:00"}],
        "dose_events": [{"id": 5, "due_at": "2026-10-11T02:30:00+00:00", "patient_id": 1}],
        "app_settings": [{"key": "vapid_keys", "value": {"public": "x"}}],
    })
    sb = SupabaseStore("https://demo.supabase.co", "k", client=fake.client())
    a = sb.select("audit_events")[0]
    assert a["at"] == "2026-10-11T10:00:00+05:30" and a["detail"] == {"a": 1}
    assert sb.select("alerts")[0]["detail"] == "123"
    assert sb.select("dose_events")[0]["due_at"] == "2026-10-11T08:00:00+05:30"
    fake.log.clear()
    sb.select("app_settings")
    assert fake.log[-1].url.params["order"] == "key.asc"
    sb.upsert("app_settings", [{"key": "vapid_keys", "value": {"public": "y"}}])
    assert fake.log[-1].url.params["on_conflict"] == "key"
    assert json.loads(fake.log[-1].content) == [{"key": "vapid_keys", "value": {"public": "y"}}]


# ----------------------------------------------------------------------------- settings files

def test_config_names_and_defaults(monkeypatch):
    for name in ("ALLOW_TRAINING", "SHOW_API_DOCS", "GEMINI_MODEL", "GEMINI_TIMEOUT_S", "AI_DAILY_LIMIT",
                 "AI_PER_IP_HOUR", "UPLOAD_PER_IP_HOUR", "SUPABASE_BUCKET"):
        monkeypatch.delenv(name, raising=False)
    assert config.allow_training() is False and config.show_api_docs() is False
    assert config.gemini_model() == "gemini-3.1-flash-lite" == config.GEMINI_MODEL_DEFAULT
    assert (config.gemini_timeout_s(), config.ai_daily_limit(), config.ai_per_ip_hour(),
            config.upload_per_ip_hour()) == (30, 300, 20, 30)
    assert config.supabase_bucket() == "documents"
    monkeypatch.setenv("ALLOW_TRAINING", "1")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.8-flash")
    monkeypatch.setenv("AI_DAILY_LIMIT", "not a number")
    assert config.allow_training() is True and config.gemini_model() == "gemini-3.8-flash"
    assert config.ai_daily_limit() == 300
    assert config.UPLOAD_DIR == config.DATA_DIR / "uploads" and config.UPLOAD_DIR.is_dir()
    for name in ("ALLOW_TRAINING", "SHOW_API_DOCS", "GEMINI_API_KEY", "GEMINI_MODEL", "GEMINI_TIMEOUT_S",
                 "AI_DAILY_LIMIT", "AI_PER_IP_HOUR", "UPLOAD_PER_IP_HOUR", "SUPABASE_BUCKET"):
        assert hasattr(config, name), name


def test_env_example_render_and_requirements_list_the_new_settings():
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for line in ("GEMINI_API_KEY=", "GEMINI_MODEL=gemini-3.1-flash-lite", "AI_DAILY_LIMIT=300",
                 "AI_PER_IP_HOUR=20", "UPLOAD_PER_IP_HOUR=30", "ALLOW_TRAINING=0", "SHOW_API_DOCS=0"):
        assert re.search(rf"^{re.escape(line)}\s*$", env_example, re.M), line
    render = (ROOT / "render.yaml").read_text(encoding="utf-8")
    assert re.search(r"key: GEMINI_API_KEY[^\n]*\n\s+sync: false", render)
    for key, value in (("GEMINI_MODEL", "gemini-3.1-flash-lite"), ("AI_DAILY_LIMIT", '"300"'),
                       ("AI_PER_IP_HOUR", '"20"'), ("ALLOW_TRAINING", '"0"'), ("SHOW_API_DOCS", '"0"'),
                       ("UPLOAD_PER_IP_HOUR", '"30"')):
        assert re.search(rf"key: {key}[^\n]*\n\s+value: {re.escape(value)}", render), key
    req = (ROOT / "backend" / "requirements.txt").read_text(encoding="utf-8")
    assert "google-genai==2.29.0" in req and "argon2-cffi==25.1.0" in req
