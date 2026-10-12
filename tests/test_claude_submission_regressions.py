"""Independent QA regressions for the submission demo (written by the Claude QA session, 12 Oct 2026).

Plain meaning: these tests check the doctor -> patient -> nurse journey from the outside, using only
the shared fixtures in conftest.py (throw-away data folder, demo mode, no provider keys).

Tests marked xfail(strict=True) describe a CONFIRMED defect from docs/qa/CLAUDE_SUBMISSION_QA.md.
They assert the correct behaviour and fail today. When the defect is fixed the test starts to pass,
strict xfail then reports it, and the marker should be deleted. Nothing here weakens an assertion.
"""
import time
from datetime import timedelta

import pytest

from backend.app import ratelimit, service
from backend.app.config import iso, now_local
from backend.app.meds import reminders

MEERA = "meera.nair@demo-general.example"
KABIR = "kabir.rao@demo-general.example"
ANJALI = "anjali@demo-general.example"
THOMAS = "thomas@demo-general.example"
RIVERSIDE_ADMIN = "admin@demo-riverside.example"


@pytest.fixture(autouse=True)
def clean_limits():
    for bucket in ("otp_request", "otp_verify", "login", "patient_session"):
        ratelimit.reset(bucket)
    yield
    for bucket in ("otp_request", "otp_verify", "login", "patient_session"):
        ratelimit.reset(bucket)


_TOKENS = {}      # patient id -> the doctor-given personal link token (shown once at registration)


def register(doctor, number, name="QA Sample", phone="+919000000077", breathing=True):
    r = doctor.post("/api/patients", json={
        "registration_no": number, "name": name, "age": 50, "sex": "F", "language": "en",
        "phone": phone, "condition": "Sample follow-up (artificial)", "breathing_enabled": breathing})
    assert r.status_code == 200, r.text
    pid = r.json()["patient"]["id"]
    _TOKENS[pid] = r.json()["app_link"].split("t=")[1]
    return pid


def pclient(anon, pid):
    """A patient-app session for a doctor-registered patient, opened with the personal link token
    (not the DEMO_MODE id shortcut, which defect F-2 is about and which may be restricted later)."""
    c = type(anon)(anon.app, headers={"X-SB": "1"})
    c.cookies.clear()                        # conftest gives new clients the demo admin cookie: drop it
    r = c.post("/api/me/session", json={"token": _TOKENS[pid]})
    assert r.status_code == 200, r.text
    return c


def breath(i=0):
    return {"t": 1760000000000 + i * 15000, "features": {
        "peak_ml": 1800.0, "pct_target": 90.0, "time_to_peak_s": 2.6, "mean_rise_ml_s": 700.0,
        "max_rise_ml_s": 900.0, "hold_s": 3.2, "smoothness": 0.8, "duration_s": 6.5}}


def otp(anon, number, hospital=1):
    return anon.post("/api/me/otp/request", json={"hospital_id": hospital, "registration_no": number}).json()


def verify(c, number, challenge, code, hospital=1):
    return c.post("/api/me/otp/verify", json={"hospital_id": hospital, "registration_no": number,
                                              "challenge_id": challenge, "code": code})


LINES = [{"drug_name": "Paracetamol", "strength": "500 mg", "form": "tablet", "dose_qty": 1,
          "dose_unit": "tablet", "slots": ["morning", "night"], "food_timing": "after_food",
          "duration_days": 3}]


# ----------------------------------------------------------------------------- draft vs approval

def test_notepad_draft_publishes_nothing_and_only_approval_creates_doses(fresh, login_as):
    doctor = login_as(MEERA)
    pid = register(doctor, "QA-REG-1")
    d = doctor.post(f"/api/patients/{pid}/prescriptions/draft-text", json={
        "text": "Amoxicillin | 500 mg | capsule | 1 | capsule | 1-1-1 | | with water"})
    assert d.status_code == 200 and d.json()["lines"][0]["duration_days"] is None
    st = service.store()
    assert not st.select("prescriptions", [("patient_id", "eq", pid)])
    assert not st.select("dose_events", [("patient_id", "eq", pid)])
    assert doctor.get(f"/api/patients/{pid}/medicines").json()["current"] == []
    ok = doctor.post(f"/api/patients/{pid}/prescriptions", json={"lines": LINES})
    assert ok.status_code == 200 and ok.json()["prescription"]["state"] == "current"
    names = {x["drug_name"] for x in doctor.get(f"/api/patients/{pid}/doses").json()}
    assert names == {"Paracetamol"}          # the unapproved Amoxicillin draft never reached the schedule


def test_draft_and_issue_are_doctor_only_and_scoped(fresh, login_as, anon):
    doctor = login_as(MEERA)
    pid = register(doctor, "QA-REG-2")
    body = {"text": "X | 1 mg | tablet | 1 | tablet | OD | 2 | x"}
    for who, want in ((login_as(ANJALI), 403), (login_as(KABIR), 404), (login_as(RIVERSIDE_ADMIN), 404),
                      (login_as(THOMAS), 404), (anon, 401), (pclient(anon, pid), (401, 403))):
        r = who.post(f"/api/patients/{pid}/prescriptions/draft-text", json=body)
        assert r.status_code in (want if isinstance(want, tuple) else (want,)), (who, r.status_code)
        r = who.post(f"/api/patients/{pid}/prescriptions", json={"lines": []})
        assert r.status_code in (want if isinstance(want, tuple) else (want,)), (who, r.status_code)
    assert login_as(ANJALI).post(f"/api/patients/{pid}/notes", json={"kind": "consultation", "text": "x"}).status_code == 403


# ----------------------------------------------------------------------------- registration

def test_registration_rejects_bad_input_and_duplicates(fresh, login_as):
    doctor = login_as(MEERA)
    register(doctor, "QA-REG-3")
    base = {"name": "QA Bad", "age": 40, "sex": "M", "language": "en"}
    assert doctor.post("/api/patients", json={**base, "registration_no": " qa-reg-3 "}).status_code == 409
    for bad in ({"phone": "98ab"}, {"age": 121}, {"sex": "X"}, {"language": "fr"}, {"primary_doctor_id": 3},
                {"breathing_enabled": "maybe"}, {"name": " "}):
        r = doctor.post("/api/patients", json={**base, "registration_no": "QA-REG-4", **bad})
        assert r.status_code == 400, (bad, r.status_code)
    assert not service.store().select("patients", [("mrn", "eq", "QA-REG-4")])


# ----------------------------------------------------------------------------- OTP

def test_changing_the_phone_invalidates_an_outstanding_code(fresh, login_as, anon):
    doctor = login_as(MEERA)
    pid = register(doctor, "QA-REG-5")
    d = otp(anon, "QA-REG-5")
    assert doctor.put(f"/api/patients/{pid}/phone", json={"phone": "+919000000078"}).status_code == 200
    assert verify(anon, "QA-REG-5", d["challenge_id"], d["demo_code"]).status_code == 401
    assert "demo_code" in otp(anon, "QA-REG-5")      # a fresh code is available straight away


def test_otp_is_single_use_hospital_scoped_and_locks_after_five_wrong_codes(fresh, login_as, anon):
    doctor = login_as(MEERA)
    register(doctor, "QA-REG-6")
    d = otp(anon, "QA-REG-6")
    assert "demo_code" not in otp(anon, "QA-REG-6", hospital=2)       # other hospital: no code
    assert verify(anon, "QA-REG-6", d["challenge_id"], d["demo_code"]).status_code == 200
    assert verify(anon, "QA-REG-6", d["challenge_id"], d["demo_code"]).status_code == 401
    ratelimit.reset("otp_request")
    service.store().delete("app_settings", [("key", "eq", "otp:1:QA-REG-6")])
    d = otp(anon, "QA-REG-6")
    wrong = "000000" if d["demo_code"] != "000000" else "111111"
    codes = [verify(anon, "QA-REG-6", d["challenge_id"], wrong).status_code for _ in range(5)]
    assert codes == [401, 401, 401, 401, 429]
    assert verify(anon, "QA-REG-6", d["challenge_id"], d["demo_code"]).status_code == 429


def test_second_code_request_inside_cooldown_leaves_the_patient_able_to_log_in(fresh, login_as, anon):
    register(login_as(MEERA), "QA-REG-7")
    first = otp(anon, "QA-REG-7")
    second = otp(anon, "QA-REG-7")                 # patient taps "send again" straight away
    code = second.get("demo_code") or first["demo_code"]
    # whatever challenge the page now holds must work with a code the patient can actually see
    assert verify(anon, "QA-REG-7", second["challenge_id"], code).status_code == 200


def test_patient_id_shortcut_does_not_open_a_doctor_registered_patient(fresh, login_as, anon):
    pid = register(login_as(MEERA), "QA-REG-8")
    r = anon.post("/api/me/session", json={"patient_id": pid})
    assert r.status_code in (403, 404)


def test_per_ip_limit_cannot_be_reset_with_a_forged_forwarded_for_header(fresh, anon):
    statuses = [anon.post("/api/me/otp/request", json={"hospital_id": 1, "registration_no": f"ZZ-{i:03d}"},
                          headers={"X-Forwarded-For": f"203.0.113.{i % 250 + 1}"}).status_code for i in range(30)]
    assert 429 in statuses


# ----------------------------------------------------------------------------- breathing

def test_breathing_empty_malformed_partial_and_unassigned_sessions_do_not_count(fresh, login_as, anon):
    doctor = login_as(MEERA)
    pid = register(doctor, "QA-REG-9")
    pc = pclient(anon, pid)
    start = iso(now_local())
    for body in ({"patient_id": pid, "breaths": []}, {"patient_id": pid}, {"patient_id": pid, "breaths": "abc"},
                 {"patient_id": pid, "breaths": [1, 2]}, {"patient_id": pid, "breaths": [{"features": {}}] * 10},
                 {"patient_id": pid, "breaths": [breath(i) for i in range(101)]}):
        assert pc.post("/api/sessions", json=body).status_code == 400
    assert not service.store().select("sessions", [("patient_id", "eq", pid)])
    r = pc.post("/api/sessions", json={"patient_id": pid, "started_at": start, "breaths": [breath(i) for i in range(5)]})
    assert r.status_code == 200 and r.json()["slot_status"] == "partial"
    assert not service.store().select("slots", [("patient_id", "eq", pid)])
    row = [p for p in doctor.get("/api/patients").json() if p["id"] == pid][0]
    assert row["done_today"] == 0
    r = pc.post("/api/sessions", json={"patient_id": pid, "started_at": start, "breaths": [breath(i) for i in range(12)]})
    assert r.status_code == 200 and r.json()["slot_status"] == "done"
    assert service.store().select("slots", [("patient_id", "eq", pid)])


def test_breathing_is_refused_when_not_assigned_and_browser_cannot_claim_hardware(fresh, login_as, anon):
    doctor = login_as(MEERA)
    off = register(doctor, "QA-REG-10", breathing=False)
    on = register(doctor, "QA-REG-11")
    assert pclient(anon, off).post("/api/sessions", json={"patient_id": off, "breaths": [breath(i) for i in range(12)]}).status_code == 403
    assert doctor.post("/api/sessions", json={"patient_id": off, "breaths": [breath(i) for i in range(12)]}).status_code == 403
    pc = pclient(anon, on)
    r = pc.post("/api/sessions", json={"patient_id": on, "device": "HW-1", "verified": True, "source": "device",
                                       "breaths": [breath(i) for i in range(12)]})
    assert r.status_code == 200
    assert service.store().select("sessions", [("id", "eq", r.json()["session_id"])])[0]["source"] == "app"
    assert pc.post("/api/sessions", json={"patient_id": off, "breaths": [breath(i) for i in range(12)]}).status_code in (403, 404)


# ----------------------------------------------------------------------------- missed-dose alert

def _tick():
    for _ in range(3):
        reminders.tick(force=True)
        time.sleep(0.2)


def _missed_dose(login_as, number, name):
    """A doctor-registered patient with one dose that is 90 minutes overdue today."""
    now = now_local()
    if now.hour < 2:
        pytest.skip("needs a dose time earlier today (run after 02:00 IST)")
    doctor = login_as(MEERA)
    pid = register(doctor, number, name=name)
    assert doctor.post(f"/api/patients/{pid}/prescriptions", json={"lines": LINES}).status_code == 200
    dose = next(d for d in doctor.get(f"/api/patients/{pid}/doses").json() if d["due_at"][:10] == now.date().isoformat())
    service.store().update("dose_events", [("id", "eq", dose["id"])], {"due_at": iso(now - timedelta(hours=1, minutes=30))})
    _tick()
    return doctor, pid, dose


def _mine(c, pid):
    return [a for a in c.get("/api/comms/alerts?status=all&limit=500").json()
            if a["kind"] == "missed_dose" and a["patient_id"] == pid]


def test_missed_dose_alert_is_scoped_single_and_cleared_by_the_patient_report(fresh, login_as, anon):
    doctor, pid, dose = _missed_dose(login_as, "QA-REG-12", "QA Alert Sample")
    nurse = login_as(ANJALI)
    found = _mine(nurse, pid)
    assert len(found) == 1 and found[0]["severity"] == "amber" and found[0]["patient_name"] == "QA Alert Sample"
    _tick(); _tick()
    assert len(_mine(nurse, pid)) == 1                        # repeated checks never duplicate it
    assert _mine(doctor, pid) and not _mine(login_as(THOMAS), pid) and not _mine(login_as(KABIR), pid)         and not _mine(login_as(RIVERSIDE_ADMIN), pid)
    assert login_as(THOMAS).post(f"/api/comms/alerts/{found[0]['id']}/ack", json={}).status_code == 404
    acted = nurse.post(f"/api/comms/alerts/{found[0]['id']}/ack", json={"by": "Impostor Name"}).json()
    assert acted["acted_by"] == "Sister Anjali"               # the signed-in nurse, not the name in the request
    assert pclient(anon, pid).post(f"/api/me/doses/{dose['id']}/taken").status_code == 200
    _tick()
    assert _mine(nurse, pid)[0]["status"] == "resolved"
    _tick()
    assert len(_mine(nurse, pid)) == 1                        # not re-raised


def test_missed_dose_alert_title_names_the_patient_and_uses_a_readable_time(fresh, login_as):
    import re
    _, pid, _ = _missed_dose(login_as, "QA-REG-13", "QA Readable Sample")
    title = _mine(login_as(ANJALI), pid)[0]["title"]
    assert "QA Readable Sample" in title
    assert not re.search(r"\d{4}-\d{2}-\d{2}T", title)
