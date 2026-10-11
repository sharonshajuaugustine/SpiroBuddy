"""Patient login with the hospital registration number + a 6-digit PIN (docs/rebuild/REGNO_PIN_BRIEF.md).

Ravi (patient 1) is DGH-000001 with the fixed demo PIN 246810 in DEMO_MODE. Staff make a new PIN
at POST /api/patients/{pid}/pin (shown once). 5 wrong PINs lock the patient for 15 minutes.
"""
from __future__ import annotations

import json
from datetime import timedelta

import pytest

RAVI_NO, RAVI_PIN = "DGH-000001", "246810"
THOMAS = "thomas@demo-general.example"            # nurse, may only view patients 3 and 5
RIVERSIDE_ADMIN = "admin@demo-riverside.example"


@pytest.fixture(autouse=True)
def _clean(client):
    """A clean demo (Ravi has his number + demo PIN) and no leftover rate-limit counters."""
    from backend.app import ratelimit
    ratelimit.reset()
    assert client.post("/api/demo/reset").status_code == 200
    ratelimit.reset()
    yield
    ratelimit.reset()


def _login(c, number=RAVI_NO, pin=RAVI_PIN):
    return c.post("/api/me/login", json={"registration_no": number, "pin": pin})


def _row(pid=1):
    from backend.app import service
    return service.get_patient_row(pid)


# ----------------------------------------------------------------------------- numbers + demo

def test_demo_patients_get_registration_numbers(client):
    from backend.app import service
    rows = service.store().select("patients", columns="id,mrn")
    nums = {r["id"]: r["mrn"] for r in rows}
    assert nums[1] == RAVI_NO and nums[2] == "DGH-000002" and nums[7] == "DGH-000007"
    assert len(set(nums.values())) == len(nums)


def test_demo_box_shows_ravi_only_in_demo_mode(anon, monkeypatch):
    d = anon.get("/api/me/login-demo").json()
    assert d["demo"] is True and d["registration_no"] == RAVI_NO and d["pin"] == RAVI_PIN
    monkeypatch.setenv("DEMO_MODE", "0")
    assert anon.get("/api/me/login-demo").json() == {"demo": False}


def test_demo_pin_is_not_set_outside_demo_mode(client, monkeypatch):
    from backend.app import seed_patient_login, service
    st = service.store()
    st.update("patients", [("id", "eq", 1)], {"pin_hash": None})
    monkeypatch.setenv("DEMO_MODE", "0")
    out = seed_patient_login.ensure(st)
    assert out["demo_pin"] is False and _row(1)["pin_hash"] is None


def test_demo_box_does_not_show_a_pin_that_staff_replaced(client, anon):
    assert client.post("/api/patients/1/pin").status_code == 200
    d = anon.get("/api/me/login-demo").json()
    assert d["demo"] is True and d["registration_no"] == RAVI_NO and d["pin"] is None


# ----------------------------------------------------------------------------- logging in

def test_login_ok_gives_own_data_only(anon):
    r = _login(anon)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] and body["patient_id"] == 1 and body["name"]
    assert "sb_patient" in anon.cookies
    assert anon.get("/api/patients/1").status_code == 200
    assert anon.get("/api/patients/2").status_code == 404           # someone else's chart
    text = anon.get("/api/patients/1").text
    assert "pin_hash" not in text and "argon2" not in text


def test_number_match_ignores_case_and_spaces(anon):
    for typed in ("dgh-000001", " DGH-000001 ", "dgh 000001", "DGH000001", "d g h - 0 0 0 0 0 1"):
        c = type(anon)(anon.app, headers={"X-SB": "1"})
        r = _login(c, typed, " 246 810 ")
        assert r.status_code == 200, (typed, r.text)
        assert r.json()["patient_id"] == 1


def test_wrong_pin_and_unknown_number_get_the_same_plain_message(anon):
    from backend.app import patient_login as pl
    a = _login(anon, RAVI_NO, "111222")
    b = _login(anon, "DGH-999999", "111222")
    assert a.status_code == b.status_code == 401
    assert a.json()["error"] == b.json()["error"] == pl.MSG_WRONG
    assert "sb_patient" not in anon.cookies


def test_bad_format_is_a_400_not_a_failure_count(anon):
    assert _login(anon, RAVI_NO, "12").status_code == 400
    assert _login(anon, RAVI_NO, "abcdef").status_code == 400
    assert _login(anon, "", RAVI_PIN).status_code == 400
    assert anon.post("/api/me/login", json={"registration_no": ["x"], "pin": 5}).status_code == 400
    assert _row(1)["pin_failed"] == 0


def test_five_wrong_pins_lock_for_15_minutes_then_unlock(anon, monkeypatch):
    from backend.app import patient_login as pl
    for i in range(4):
        assert _login(anon, RAVI_NO, "000001").status_code == 401
    r = _login(anon, RAVI_NO, "000001")                      # the 5th one locks
    assert r.status_code == 429 and r.json()["error"] == pl.MSG_LOCKED
    assert _login(anon).status_code == 429                   # even the right PIN waits
    t0 = pl.now()
    monkeypatch.setattr(pl, "now", lambda: t0 + timedelta(minutes=14))
    assert _login(anon).status_code == 429
    monkeypatch.setattr(pl, "now", lambda: t0 + timedelta(minutes=16))
    assert _login(anon).status_code == 200
    assert _row(1)["pin_failed"] == 0 and not _row(1)["pin_locked_until"]


def test_a_right_pin_resets_the_wrong_count(anon):
    for _ in range(3):
        assert _login(anon, RAVI_NO, "000001").status_code == 401
    assert _login(anon).status_code == 200
    assert _row(1)["pin_failed"] == 0
    for _ in range(4):
        assert _login(anon, RAVI_NO, "000001").status_code == 401   # a fresh count of 4: not locked
    assert _login(anon).status_code == 200


def test_one_address_is_limited_to_20_failed_tries(anon):
    for i in range(20):
        assert _login(anon, f"NOPE-{i:06d}", "123123").status_code == 401
    assert _login(anon, "NOPE-000099", "123123").status_code == 429


# ----------------------------------------------------------------------------- making a PIN

def test_staff_make_a_pin_shown_once_and_it_works(client, anon):
    r = client.post("/api/patients/1/pin")
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["registration_no"] == RAVI_NO and len(d["pin"]) == 6 and d["pin"].isdigit()
    assert d["hospital_name"] and d["patient_name"] and d["login_path"] == "/patient-login.html"
    assert r.headers["cache-control"] == "no-store"
    assert _login(anon, RAVI_NO, d["pin"]).status_code == 200
    # the staff card never gets the PIN back
    info = client.get("/api/patients/1/login").json()
    assert info["registration_no"] == RAVI_NO and info["has_pin"] is True
    assert "pin" not in info and d["pin"] not in json.dumps(info)


def test_a_new_pin_stops_the_old_one(client, anon):
    old = client.post("/api/patients/1/pin").json()["pin"]
    new = client.post("/api/patients/1/pin").json()["pin"]
    assert old != new or True                                  # (1 in a million to match)
    if old != new:
        assert _login(anon, RAVI_NO, old).status_code == 401
    assert _login(anon, RAVI_NO, new).status_code == 200


def test_new_pin_clears_a_lock(client, anon):
    for _ in range(5):
        _login(anon, RAVI_NO, "000001")
    assert _login(anon).status_code == 429
    pin = client.post("/api/patients/1/pin").json()["pin"]
    assert client.get("/api/patients/1/login").json()["locked"] is False
    assert _login(anon, RAVI_NO, pin).status_code == 200


def test_pin_is_never_stored_or_logged_in_plain_text(client, anon):
    from backend.app import authz
    pin = client.post("/api/patients/1/pin").json()["pin"]
    _login(anon, RAVI_NO, pin)
    _login(anon, RAVI_NO, "135790")                            # a failed one too
    row = _row(1)
    assert row["pin_hash"].startswith("$argon2")
    assert pin not in json.dumps(row, default=str)
    events = authz.ident().select("audit_events", columns="action,detail")
    actions = {e["action"] for e in events}
    assert {"patient.pin_create", "auth.patient_login"} <= actions
    dump = json.dumps(events, default=str)
    assert pin not in dump and RAVI_PIN not in dump and "135790" not in dump
    ok = [e for e in events if e["action"] == "auth.patient_login"]
    assert any(e["detail"].get("ok") is True for e in ok) and any(e["detail"].get("ok") is False for e in ok)


def test_other_hospital_gets_404_and_a_nurse_without_patient_edit_gets_403(client, login_as,
                                                                          riverside_patient):
    other = login_as(RIVERSIDE_ADMIN)
    assert other.post("/api/patients/1/pin").status_code == 404           # not their patient
    assert other.get("/api/patients/1/login").status_code == 404
    assert other.put("/api/patients/1/regno", json={"registration_no": "ZZ-1"}).status_code == 404
    assert client.post(f"/api/patients/{riverside_patient}/pin").status_code == 404   # and back
    nurse = login_as(THOMAS)
    assert nurse.post("/api/patients/3/pin").status_code == 403           # may view, not edit
    assert nurse.post("/api/patients/1/pin").status_code == 404           # not on his list at all
    assert nurse.get("/api/patients/3/login").json()["can_edit"] is False
    assert _row(1)["pin_hash"] != ""                                      # nothing changed


def test_patients_and_strangers_cannot_make_pins(anon, patient_client):
    assert anon.post("/api/patients/1/pin").status_code == 401
    p = patient_client(1)
    assert p.post("/api/patients/1/pin").status_code == 401               # a patient session is not staff


def test_riverside_gets_its_own_prefix(login_as, riverside_patient):
    from backend.app import patient_login as pl, service
    st = service.store()
    row = service.get_patient_row(riverside_patient)
    assert pl.ensure_regno(st, row) == "DRC-000001"
    other = login_as(RIVERSIDE_ADMIN)
    d = other.post(f"/api/patients/{riverside_patient}/pin").json()
    assert d["registration_no"] == "DRC-000001"


# ----------------------------------------------------------------------------- own number

def test_staff_can_type_the_hospitals_own_number(client, anon):
    r = client.put("/api/patients/2/regno", json={"registration_no": " ab 12/2026 "})
    assert r.status_code == 200 and r.json()["registration_no"] == "AB12/2026"
    pin = client.post("/api/patients/2/pin").json()
    assert pin["registration_no"] == "AB12/2026"
    assert _login(anon, "ab12/2026", pin["pin"]).json()["patient_id"] == 2
    # a number is used once per hospital, and the format is checked
    assert client.put("/api/patients/3/regno", json={"registration_no": "AB12/2026"}).status_code == 400
    assert client.put("/api/patients/3/regno", json={"registration_no": "x"}).status_code == 400
    assert client.put("/api/patients/3/regno", json={"registration_no": "a;b<c>"}).status_code == 400


def test_a_patient_without_a_number_gets_one_with_the_first_pin(client):
    from backend.app import service
    service.store().update("patients", [("id", "eq", 7)], {"mrn": None})
    assert client.get("/api/patients/7/login").json()["registration_no"] is None
    d = client.post("/api/patients/7/pin").json()
    assert d["registration_no"] == "DGH-000008" or d["registration_no"].startswith("DGH-")
    assert _row(7)["mrn"] == d["registration_no"]


# ----------------------------------------------------------------------------- columns missing

class _NoPinColumns:
    """A Supabase-like store whose patients table lacks the three PIN columns (schema_v2.sql not
    pasted again): anything that mentions them fails the way PostgREST fails."""
    name = "supabase"
    _COLS = ("pin_hash", "pin_failed", "pin_locked_until")

    def __init__(self, real):
        self._real = real
        self.writes = []

    def _check(self, table, text):
        if table == "patients" and any(c in text for c in self._COLS):
            raise RuntimeError("Supabase GET /patients: 400 {\"message\":\"column patients.pin_hash does not exist\"}")

    def select(self, table, filters=(), order=None, desc=False, limit=None, columns="*"):
        self._check(table, columns + repr(list(filters)))
        rows = self._real.select(table, filters, order, desc, limit, columns)
        if table == "patients" and columns == "*":
            rows = [{k: v for k, v in r.items() if k not in self._COLS} for r in rows]
        return rows

    def insert(self, table, rows):
        self._check(table, repr(rows))
        return self._real.insert(table, rows)

    def update(self, table, filters, values):
        self._check(table, repr(values))
        self.writes.append((table, dict(values)))
        return self._real.update(table, filters, values)

    def __getattr__(self, item):
        return getattr(self._real, item)


@pytest.fixture()
def no_pin_columns(client, monkeypatch):
    from backend.app import service
    proxy = _NoPinColumns(service.store())
    monkeypatch.setattr(service, "_store", proxy)
    yield proxy


def test_missing_columns_say_not_set_up_and_never_crash(client, anon, no_pin_columns):
    from backend.app import patient_login as pl
    r = _login(anon)
    assert r.status_code == 503 and r.json()["error"] == pl.MSG_NOT_SET_UP
    assert "Traceback" not in r.text and "pin_hash" not in r.text
    r = client.post("/api/patients/1/pin")
    assert r.status_code == 503 and r.json()["error"] == pl.MSG_NOT_SET_UP
    info = client.get("/api/patients/1/login")
    assert info.status_code == 200 and info.json()["set_up"] is False and info.json()["has_pin"] is False
    assert info.json()["message"] == pl.MSG_NOT_SET_UP
    assert anon.get("/api/me/login-demo").json() == {"demo": False}
    # everything else keeps working
    assert client.get("/api/patients/1").status_code == 200
    assert client.get("/api/patients").status_code == 200


def test_seed_without_the_columns_saves_numbers_and_skips_the_pin(client, no_pin_columns):
    from backend.app import seed_patient_login
    no_pin_columns._real.update("patients", [("id", "gte", 0)], {"mrn": None})
    out = seed_patient_login.ensure(no_pin_columns)
    assert out["numbers"] == 7 and out["demo_pin"] is False
    assert no_pin_columns.writes and all("pin_hash" not in w[1] for w in no_pin_columns.writes)
    assert no_pin_columns._real.select("patients", [("id", "eq", 1)], columns="mrn")[0]["mrn"] == RAVI_NO


def test_columns_ready_remembers_no_only_briefly(monkeypatch):
    from backend.app import patient_login as pl

    class S:
        name = "supabase"
        calls = 0
        broken = True

        def select(self, *a, **k):
            S.calls += 1
            if S.broken:
                raise RuntimeError("400 column does not exist")
            return []

    s = S()
    assert pl.columns_ready(s) is False and pl.columns_ready(s) is False
    assert S.calls == 1                                         # the "no" is cached for a moment
    S.broken = False
    s._sb_login_cols = (False, s._sb_login_cols[1] - 60)        # a minute later: ask again
    assert pl.columns_ready(s) is True and pl.columns_ready(s) is True
    assert S.calls == 2


def test_schema_v2_sql_is_safe_to_run_again():
    from pathlib import Path
    sql = (Path(__file__).resolve().parents[1] / "supabase" / "schema_v2.sql").read_text(encoding="utf-8")
    for col in ("pin_hash", "pin_failed", "pin_locked_until"):
        assert f"add column if not exists {col}" in sql
    # the unique index skips rows without a number and cannot abort the script on duplicates
    block = sql[sql.index("idx_patients_hospital_mrn") - 200:]
    assert "where mrn is not null" in block and "exception when others" in block
