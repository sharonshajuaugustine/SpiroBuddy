"""Digital prescription (Contract H, founder idea of 11 Oct 2026): the doctor types it, the patient
sees it on the phone, shows it at the pharmacy counter, and the pharmacist can check the QR.

Fictional patients and accounts only (backend/app/seed_auth.py). No network, no AI.
"""
import re
from datetime import timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MEERA = "meera.nair@demo-general.example"      # doctor of patients 1, 2, 4, 6
KABIR = "kabir.rao@demo-general.example"       # doctor of patients 3, 5, 7
ANJALI = "anjali@demo-general.example"         # nurse, every permission, Dr. Meera's patients
ADMIN = "admin@demo-general.example"
PID = 2                                        # Priya Sharma (Dr. Meera's patient) - the test patient

BD = {"drug_name": "Paracetamol", "form": "tablet", "strength": "500 mg", "dose_qty": 1,
      "dose_unit": "tablet", "frequency_raw": "1-0-1", "food_timing": "after_food",
      "duration_days": 5}
SOS = {"drug_name": "Ondansetron", "form": "tablet", "strength": "4 mg", "dose_qty": 1,
       "dose_unit": "tablet", "frequency_raw": "SOS", "as_needed": True}


def line(**kw):
    return {**BD, **kw}


@pytest.fixture(autouse=True)
def rxdb(client):
    """A clean prescription world for each test; Ravi's demo prescription is put back afterwards."""
    from backend.app import ratelimit, service
    from backend.app.meds import seed_meds
    seed_meds.wipe(service.store())
    ratelimit.reset()
    yield service.store()
    seed_meds.wipe(service.store())
    seed_meds.seed(service.store())
    ratelimit.reset()


@pytest.fixture()
def doctor(login_as):
    return login_as(MEERA)


def _issue(c, lines, pid=PID, **extra):
    r = c.post(f"/api/patients/{pid}/prescriptions", json={"lines": lines, **extra})
    return r


def _issue_from_midnight(pid=PID, lines=None):
    """Issue through the service with today's start as the issue time, so today's doses exist at
    any hour of the day (the HTTP route issues 'now', which can be after today's last dose time)."""
    from backend.app import service
    from backend.app.config import now_local
    from backend.app.meds import service as meds
    now = now_local().replace(hour=0, minute=0, second=0, microsecond=0)
    rx, _ = meds.create_prescription(service.get_patient_row(pid), 2, lines or [line()], issued_at=now)
    return rx


def _dose_rows(st, pid=PID):
    return st.select("dose_events", [("patient_id", "eq", pid)])


# ------------------------------------------------------------------------------ the normaliser

@pytest.mark.parametrize("text,code,times,kind", [
    ("1-0-0", "1-0-0", ["08:00"], "scheduled"),
    ("OD", "1-0-0", ["08:00"], "scheduled"),
    ("0-0-1", "0-0-1", ["21:00"], "scheduled"),
    ("1-0-1", "1-0-1", ["08:00", "21:00"], "scheduled"),
    ("BD", "1-0-1", ["08:00", "21:00"], "scheduled"),
    ("1 - 1 - 1", "1-1-1", ["08:00", "14:00", "21:00"], "scheduled"),
    ("TDS", "1-1-1", ["08:00", "14:00", "21:00"], "scheduled"),
    ("T.D.S.", "1-1-1", ["08:00", "14:00", "21:00"], "scheduled"),
    ("QID", "QID", ["08:00", "12:00", "16:00", "20:00"], "scheduled"),
    ("1-1-1-1", "QID", ["08:00", "12:00", "16:00", "20:00"], "scheduled"),
    ("HS", "HS", ["22:00"], "scheduled"),
    ("twice daily", "1-0-1", ["08:00", "21:00"], "scheduled"),
    ("SOS", "SOS", [], "as_needed"),
    ("only when needed", "SOS", [], "as_needed"),
    ("PRN", "SOS", [], "as_needed"),
    ("STAT", "STAT", [], "stat"),
    ("whenever", None, [], "unclear"),
    ("2-0-2", None, [], "unclear"),
    ("0-0-0", None, [], "unclear"),
    ("1-0-1-0", None, [], "unclear"),
    ("", None, [], "unclear"),
])
def test_normaliser_table(text, code, times, kind):
    from backend.app.meds import normalise as nz
    r = nz.normalise_frequency(text)
    assert (r["code"], r["times"], r["kind"]) == (code, times, kind)
    assert r["as_needed"] == (kind == "as_needed")
    assert r["unclear"] == (kind in ("unclear", "stat"))


def test_normaliser_uses_the_patients_routine_and_explicit_choices():
    from backend.app.meds import normalise as nz
    routine = {"breakfast": "07:30", "lunch": "13:00", "dinner": "20:30", "bed": "22:30"}
    assert nz.normalise_frequency("1-1-1", routine)["times"] == ["07:30", "13:00", "20:30"]
    assert nz.normalise_frequency("HS", routine)["times"] == ["22:30"]
    assert nz.normalise_frequency("1-0-1", {"breakfast": "nonsense"})["times"] == ["08:00", "21:00"]
    r = nz.from_slots(["morning", "night"])
    assert (r["code"], r["times"], r["slots"]) == ("1-0-1", ["08:00", "21:00"], ["morning", "night"])
    assert nz.from_slots(["lunchtime"])["unclear"] and nz.from_slots([])["unclear"]
    assert nz.from_times(["20:30", "8:00"])["times"] == ["08:00", "20:30"]
    assert nz.from_times(["25:00"])["unclear"]


def test_normaliser_food_duration_and_amounts():
    from backend.app.meds import normalise as nz
    assert nz.normalise_food("After food") == ("after_food", True)
    assert nz.normalise_food("before_food") == ("before_food", True)
    assert nz.normalise_food("") == ("any", True)
    assert nz.normalise_food("with a banana")[1] is False
    assert nz.normalise_duration(5, False) == (5, False, True)
    assert nz.normalise_duration(None, True) == (None, True, True)
    assert nz.normalise_duration(None, False)[2] is False
    assert nz.normalise_duration(0, False)[2] is False and nz.normalise_duration(400, False)[2] is False
    assert nz.normalise_duration(2.5, False)[2] is False
    assert nz.parse_qty("1/2") == 0.5 and nz.parse_qty("1½") == 1.5 and nz.parse_qty(2) == 2.0
    assert nz.parse_qty(0) is None and nz.parse_qty("abc") is None and nz.parse_qty(500) is None
    assert nz.qty_text(0.5) == "½" and nz.qty_text(1.5) == "1½" and nz.qty_text(2) == "2"


# ------------------------------------------------------------------------------ issuing

def test_issue_then_the_patient_sees_it(doctor, patient_client, rxdb):
    r = _issue(doctor, [line(), SOS], prescriber_on_paper=None)
    assert r.status_code == 200, r.text
    rx = r.json()["prescription"]
    assert rx["state"] == "current" and rx["state_text"] == "Issued" and rx["version"] == 1
    assert rx["doctor"]["name"] == "Dr. Meera Nair"
    assert [ln["drug_name"] for ln in rx["lines"]] == ["Paracetamol", "Ondansetron"]
    bd = rx["lines"][0]
    assert (bd["frequency_code"], bd["times"], bd["slots"], bd["food_timing"], bd["duration_days"]) == \
        ("1-0-1", ["08:00", "21:00"], ["morning", "night"], "after_food", 5)
    assert bd["dose_text"] == "1 tablet" and bd["scheduled"] and not bd["unclear_fields"]
    # the patient's phone
    me = patient_client(PID).get("/api/me/medicines")
    assert me.status_code == 200
    m = me.json()
    assert m["has_prescription"] and m["patient"]["language"] == "en" and m["doctor"] == "Dr. Meera Nair"
    assert [x["drug_name"] for x in m["active"]] == ["Paracetamol"]
    assert [x["drug_name"] for x in m["as_needed"]] == ["Ondansetron"]
    # staff list
    staff = doctor.get(f"/api/patients/{PID}/medicines").json()
    assert len(staff["active"]) == 1 and len(staff["as_needed"]) == 1 and len(staff["history"]) == 1
    assert doctor.get(f"/api/prescriptions/{rx['id']}").json()["items"][0]["drug_name"] == "Paracetamol"


def test_nothing_is_scheduled_before_a_prescription_is_issued(patient_client, rxdb):
    from backend.app import service
    from backend.app.config import iso, now_local
    from backend.app.meds import service as meds
    now = iso(now_local())
    for status in ("draft", "needs_review", "rejected"):
        rx = rxdb.insert("prescriptions", [{"hospital_id": 1, "patient_id": PID, "status": status,
                                            "version": 1, "created_at": now}])[0]
        rxdb.insert("prescription_items", [{
            "hospital_id": 1, "prescription_id": rx["id"], "patient_id": PID, "line_no": 1,
            "drug_name": "Draft medicine (fake)", "dose_qty": 1, "dose_unit": "tablet",
            "frequency_code": "1-0-1", "times": ["08:00", "21:00"], "food_timing": "any",
            "duration_days": 5, "start_date": now[:10], "end_date": now[:10], "as_needed": False,
            "unclear_fields": [], "status": "confirmed", "created_at": now}])
    assert meds.refresh_doses(PID, force=True) == 0
    assert _dose_rows(rxdb) == []
    c = patient_client(PID)
    m = c.get("/api/me/medicines").json()
    assert m["has_prescription"] is False and m["active"] == [] and m["today"] == []
    assert c.get("/api/me/prescription-card").json()["card"] is None
    assert service.get_patient_row(PID)           # (the patient is fine, there is just nothing issued)


def test_sos_lines_are_never_scheduled(doctor, rxdb):
    r = _issue(doctor, [SOS, line(drug_name="Cough syrup", frequency_raw="1-1-1", as_needed=True)])
    assert r.status_code == 200
    assert all(ln["as_needed"] and ln["times"] == [] and not ln["scheduled"] for ln in r.json()["items"])
    assert _dose_rows(rxdb) == []
    # a scheduled line next to an SOS line: doses only for the scheduled one
    _issue_from_midnight(lines=[SOS, line()])
    sos_ids = {i["id"] for i in rxdb.select("prescription_items") if i["as_needed"]}
    doses = _dose_rows(rxdb)
    assert sos_ids and doses and not any(d["item_id"] in sos_ids for d in doses)


def test_unclear_lines_are_kept_but_not_scheduled(doctor, patient_client, rxdb):
    r = _issue(doctor, [line(drug_name="Vitamin X", frequency_raw="whenever"),
                        line(drug_name="Vitamin Y", frequency_raw="BD", duration_days=None),
                        line(drug_name="Vitamin Z", frequency_raw="BD", until_stopped=True,
                             food_timing="with a banana")])
    assert r.status_code == 200
    items = {ln["drug_name"]: ln for ln in r.json()["items"]}
    assert items["Vitamin X"]["unclear_fields"] == ["frequency"] and not items["Vitamin X"]["scheduled"]
    assert items["Vitamin Y"]["unclear_fields"] == ["duration"] and not items["Vitamin Y"]["scheduled"]
    assert items["Vitamin Z"]["scheduled"] and items["Vitamin Z"]["until_stopped"]
    assert items["Vitamin Z"]["unclear_fields"] == ["food_timing"]
    codes = {w["code"] for w in r.json()["warnings"]}
    assert {"unclear_frequency", "unclear_duration", "unclear_food"} <= codes
    scheduled_ids = {items["Vitamin Z"]["id"]}
    assert {d["item_id"] for d in _dose_rows(rxdb)} <= scheduled_ids
    # the patient still sees the unclear lines, exactly as written
    m = patient_client(PID).get("/api/me/medicines").json()
    seen = {x["drug_name"]: x for x in m["active"]}
    assert seen["Vitamin X"]["frequency_raw"] == "whenever" and not seen["Vitamin X"]["scheduled"]


def test_doses_follow_the_schedule_and_only_from_the_issue_time(doctor, rxdb):
    from backend.app.config import now_local, parse_dt
    r = _issue(doctor, [line(frequency_raw="1-1-1", duration_days=2)])
    assert r.status_code == 200
    now = now_local()
    rows = _dose_rows(rxdb)
    assert rows, "tomorrow's doses always exist"
    for d in rows:
        due = parse_dt(d["due_at"])
        assert due >= now.replace(second=0, microsecond=0) - timedelta(seconds=1)
        assert due.date() in (now.date(), now.date() + timedelta(days=1))
        assert d["status"] == "upcoming"
    # three times a day, today (only the ones still to come) + tomorrow (all three)
    tomorrow = [d for d in rows if parse_dt(d["due_at"]).date() == now.date() + timedelta(days=1)]
    assert sorted(parse_dt(d["due_at"]).strftime("%H:%M") for d in tomorrow) == ["08:00", "14:00", "21:00"]
    # calling it again changes nothing
    from backend.app.meds import service as meds
    assert meds.refresh_doses(PID, force=True) == 0


def test_validation_messages(doctor):
    assert _issue(doctor, []).status_code == 400
    assert _issue(doctor, "nothing").status_code == 400
    assert _issue(doctor, [line(drug_name="  ")]).status_code == 400
    assert _issue(doctor, [line(dose_qty=0)]).status_code == 400
    assert _issue(doctor, [line(dose_qty="lots")]).status_code == 400
    assert _issue(doctor, ["Paracetamol"]).status_code == 400
    assert _issue(doctor, [line()] * 21).status_code == 400
    assert _issue(doctor, [line()], prescribed_on="not a date").status_code == 400
    assert _issue(doctor, [line()], prescribed_on="2999-01-01").status_code == 400
    assert _issue(doctor, [line()], replaces=999999).status_code == 404
    assert doctor.post(f"/api/patients/{PID}/prescriptions", json={}).status_code == 400
    assert doctor.post("/api/patients/abc/prescriptions", json={"lines": [line()]}).status_code == 422


# ------------------------------------------------------------------------------ doses

def test_the_patient_reports_a_dose(patient_client, rxdb):
    _issue_from_midnight()
    c = patient_client(PID)
    today = c.get("/api/me/today").json()
    assert today["offline_ok"] is True and today["medicines"]["reported"] == 0
    doses = today["doses"]
    assert len(doses) == 2 and today["now_card"]["kind"] == "medicine"
    d = doses[0]
    r = c.post(f"/api/me/doses/{d['id']}/report")
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "reported_taken" and r.json()["reported_at"]
    again = c.post(f"/api/me/doses/{d['id']}/report")                     # reporting twice changes nothing
    assert again.status_code == 200 and again.json()["reported_at"] == r.json()["reported_at"]
    assert c.get("/api/me/today").json()["medicines"]["reported"] == 1
    # the contract's second name for the same tap
    d2 = doses[1]
    assert c.post(f"/api/me/doses/{d2['id']}/taken").status_code == 200
    row = rxdb.select("dose_events", [("id", "eq", d["id"])])[0]
    assert row["reported_by_role"] == "patient" and row["channel"] == "app"


def test_a_patient_only_sees_and_reports_their_own(patient_client, rxdb):
    _issue_from_midnight(PID)
    _issue_from_midnight(4, [line(drug_name="Other patient's medicine (fake)")])
    mine = patient_client(PID)
    other_dose = [d for d in rxdb.select("dose_events", [("patient_id", "eq", 4)])][0]
    assert mine.post(f"/api/me/doses/{other_dose['id']}/report").status_code == 404
    names = {x["drug_name"] for x in mine.get("/api/me/medicines").json()["active"]}
    assert names == {"Paracetamol"}
    assert "Other patient's medicine (fake)" not in mine.get("/api/me/prescription-card").text
    # nobody logged in is not a patient
    from tests.conftest import _new_client
    assert _new_client().get("/api/me/medicines").status_code == 401


def test_staff_can_report_for_the_patient_and_it_is_logged(login_as, rxdb):
    _issue_from_midnight()
    nurse = login_as(ANJALI)
    d = _dose_rows(rxdb)[0]
    r = nurse.post(f"/api/patients/{PID}/doses/{d['id']}/report")
    assert r.status_code == 200 and r.json()["reported_by_role"] == "nurse"
    wrong = nurse.post(f"/api/patients/{PID}/doses/{_dose_rows(rxdb, PID)[0]['id'] + 9999}/report")
    assert wrong.status_code == 404
    listing = nurse.get(f"/api/patients/{PID}/doses").json()
    assert listing and {"id", "item_id", "drug_name", "due_at", "status", "reported_at",
                        "reported_by_role"} <= set(listing[0])
    assert nurse.get(f"/api/patients/{PID}/doses?from=nonsense").status_code == 400


def test_dose_statuses_follow_the_clock(patient_client, rxdb):
    from backend.app.config import iso, now_local
    from backend.app.meds import service as meds
    _issue_from_midnight()
    item = rxdb.select("prescription_items", [("patient_id", "eq", PID)])[0]
    now = now_local()
    base = {"hospital_id": 1, "patient_id": PID, "item_id": item["id"], "status": "upcoming"}
    rxdb.delete("dose_events", [("patient_id", "eq", PID)])
    ids = {}
    for name, delta in (("upcoming", 120), ("due", 5), ("late", -30), ("missed", -300)):
        ids[name] = rxdb.insert("dose_events", [{**base, "due_at": iso(now + timedelta(minutes=delta))}])[0]["id"]
    got = {d["id"]: d["status"] for d in meds.doses_for(PID, now.date().isoformat(),
                                                         (now + timedelta(days=1)).date().isoformat())}
    assert got[ids["upcoming"]] == "upcoming" and got[ids["due"]] == "due"
    assert got[ids["late"]] == "due" and got[ids["missed"]] == "missed"


# ------------------------------------------------------------------------------ stop and replace

def test_stopping_hides_it_from_the_patient_and_the_pharmacist_check_says_so(doctor, patient_client, anon, rxdb):
    rx = _issue(doctor, [line()]).json()["prescription"]
    c = patient_client(PID)
    token = c.get("/api/me/prescription-card").json()["card"]["token"]
    assert anon.get(f"/api/rx-check/{token}").json()["state"] == "current"
    item_ids = {i["id"] for i in rxdb.select("prescription_items", [("prescription_id", "eq", rx["id"])])}
    assert any(d["item_id"] in item_ids for d in _dose_rows(rxdb))
    r = doctor.post(f"/api/prescriptions/{rx['id']}/stop", json={"reason": "Allergy rash"})
    assert r.status_code == 200 and r.json()["prescription"]["state"] == "stopped"
    m = c.get("/api/me/medicines").json()
    assert m["has_prescription"] is False and m["active"] == [] and m["as_needed"] == []
    assert c.get("/api/me/prescription-card").json()["card"] is None
    j = anon.get(f"/api/rx-check/{token}").json()                 # the old QR still answers, honestly
    assert j["state"] == "no_longer_current" and j["current"] is False and j["lines"] == []
    # its future doses are cancelled, nothing is deleted
    mine = [d for d in _dose_rows(rxdb) if d["item_id"] in item_ids]
    assert mine and all(d["status"] == "cancelled" for d in mine)
    assert c.get("/api/me/today").json()["doses"] == []
    assert doctor.get(f"/api/patients/{PID}/medicines").json()["history"][-1]["state"] == "stopped"
    assert doctor.post(f"/api/prescriptions/{rx['id']}/stop", json={}).status_code == 409


def test_replacing_keeps_the_history_and_changes_the_token(doctor, patient_client, anon, rxdb):
    a = _issue(doctor, [line()]).json()["prescription"]
    c = patient_client(PID)
    token_a = c.get("/api/me/prescription-card").json()["card"]["token"]
    r = _issue(doctor, [line(drug_name="Ibuprofen", frequency_raw="TDS")], replaces=a["id"])
    assert r.status_code == 200, r.text
    b = r.json()["prescription"]
    assert b["version"] == 2 and b["supersedes_id"] == a["id"] and b["state"] == "current"
    hist = doctor.get(f"/api/patients/{PID}/medicines").json()
    assert [h["state"] for h in hist["history"]] == ["current", "replaced"]
    assert [x["drug_name"] for x in hist["active"]] == ["Ibuprofen"]
    assert [x["drug_name"] for x in c.get("/api/me/medicines").json()["active"]] == ["Ibuprofen"]
    token_b = c.get("/api/me/prescription-card").json()["card"]["token"]
    assert token_a != token_b
    assert anon.get(f"/api/rx-check/{token_a}").json()["state"] == "no_longer_current"
    assert anon.get(f"/api/rx-check/{token_b}").json()["state"] == "current"
    assert rxdb.select("prescriptions", [("id", "eq", a["id"])])[0]["status"] == "superseded"
    # a replaced (or stopped) prescription cannot be replaced again
    assert _issue(doctor, [line()], replaces=a["id"]).status_code == 404


# ------------------------------------------------------------------------------ who may do what

def test_only_a_doctor_of_the_patient_can_issue(login_as, anon, patient_client, rxdb):
    body = {"lines": [line()]}
    assert login_as(KABIR).post(f"/api/patients/{PID}/prescriptions", json=body).status_code == 404   # not his patient
    assert login_as(ANJALI).post(f"/api/patients/{PID}/prescriptions", json=body).status_code == 403  # a nurse never prescribes
    assert login_as(ADMIN).post(f"/api/patients/{PID}/prescriptions", json=body).status_code == 403   # nor the admin
    assert patient_client(PID).post(f"/api/patients/{PID}/prescriptions", json=body).status_code in (401, 403)
    assert anon.post(f"/api/patients/{PID}/prescriptions", json=body).status_code == 401
    assert rxdb.select("prescriptions") == []


@pytest.fixture()
def other_hospital_doctor(login_as):
    from backend.app import authz, seed_auth
    from backend.app.config import iso, now_local
    ist = authz.ident()
    ist.insert("staff", [{"id": 91, "hospital_id": 2, "role": "doctor", "name": "Dr. Riverside (fictional)",
                          "email": "doc@demo-riverside.example",
                          "password_hash": seed_auth.hasher().hash("riverside-doc-2026"),
                          "status": "active", "failed_logins": 0, "created_at": iso(now_local())}])
    yield login_as("doc@demo-riverside.example", "riverside-doc-2026")
    ist.delete("auth_sessions", [("staff_id", "eq", 91)])
    ist.delete("staff", [("id", "eq", 91)])


def test_a_doctor_of_the_other_hospital_gets_404(doctor, other_hospital_doctor, rxdb):
    rx = _issue(doctor, [line()]).json()["prescription"]
    _issue_from_midnight()
    d = _dose_rows(rxdb)[0]
    o = other_hospital_doctor
    assert _issue(o, [line()]).status_code == 404
    assert o.get(f"/api/patients/{PID}/medicines").status_code == 404
    assert o.get(f"/api/patients/{PID}/doses").status_code == 404
    assert o.get(f"/api/prescriptions/{rx['id']}").status_code == 404
    assert o.post(f"/api/prescriptions/{rx['id']}/stop", json={}).status_code == 404
    assert o.post(f"/api/patients/{PID}/doses/{d['id']}/report").status_code == 404


# ------------------------------------------------------------------------------ the pharmacist check

def test_rx_check_is_public_minimal_and_strict(doctor, patient_client, anon, rxdb):
    _issue(doctor, [line(), SOS])
    card = patient_client(PID).get("/api/me/prescription-card").json()["card"]
    token = card["token"]
    assert card["verify_path"] == f"/rx.html?t={token}"
    assert card["hospital"]["name"].startswith("Demo General Hospital")
    assert card["patient"]["name"] == "Priya Sharma" and card["patient"]["age"] == 44
    assert card["doctor"]["name"] == "Dr. Meera Nair" and card["notice"].startswith("Demo - fictional patient.")
    assert card["lines"][0]["summary"] == "1 tablet · morning and night · after food · 5 days"
    assert card["lines"][1]["summary"].startswith("1 tablet · only when needed")
    r = anon.get(f"/api/rx-check/{token}")                       # no login at all
    assert r.status_code == 200
    j = r.json()
    assert r.headers["cache-control"] == "no-store"
    assert j["current"] is True and j["state"] == "current"
    assert j["patient"] == {"name": "Priya S.", "age": 44, "sex": "F"}
    assert j["hospital"]["name"].startswith("Demo General Hospital")
    assert [ln["drug_name"] for ln in j["lines"]] == ["Paracetamol", "Ondansetron"]
    text = r.text.lower()
    for word in ("phone", "address", "email", "family", "app_token", "patient_id", '"id"', "token"):
        assert word not in text, word
    assert "priya sharma" not in text                            # first name and initial only
    assert j["notice"] == "Compare with the patient's screen. Demo data only."
    # bad tokens
    for bad in ("nonsense", "1.", "0.deadbeef", f"{token}0", token[:-1] + ("0" if token[-1] != "0" else "1"),
                "99999." + token.split(".")[1], "1." + "0" * 32):
        assert anon.get(f"/api/rx-check/{bad}").status_code == 404, bad


def test_rx_check_is_rate_limited(anon, doctor, patient_client):
    _issue(doctor, [line()])
    token = patient_client(PID).get("/api/me/prescription-card").json()["card"]["token"]
    codes = [anon.get(f"/api/rx-check/nope{i}.{'0' * 32}").status_code for i in range(12)]
    assert codes[:10] == [404] * 10 and codes[10:] == [429, 429]
    assert anon.get(f"/api/rx-check/{token}").status_code == 429       # this address waits a few minutes


def test_the_token_survives_a_restart_and_cannot_be_forged(doctor, patient_client, anon, monkeypatch):
    from backend.app.meds import service as meds
    _issue(doctor, [line()])
    token = patient_client(PID).get("/api/me/prescription-card").json()["card"]["token"]
    meds._secret_cache = None                                     # a new process reads the same secret again
    assert patient_client(PID).get("/api/me/prescription-card").json()["card"]["token"] == token
    meds._secret_cache = b"another server secret"                 # ...but another secret does not match
    assert anon.get(f"/api/rx-check/{token}").status_code == 404
    meds._secret_cache = None


# ------------------------------------------------------------------------------ audit

def test_every_write_is_audited(doctor, patient_client, rxdb):
    from backend.app import authz

    def events(action):
        rows = [e for e in authz.ident().select("audit_events", [("action", "eq", action)])
                if e.get("patient_id") == PID]
        return sorted(rows, key=lambda e: e["id"])
    seen = {x: len(events(x)) for x in ("rx.create", "rx.replace", "rx.stop", "dose.report")}

    def added(action):
        return events(action)[seen[action]:]
    a = _issue(doctor, [line()]).json()["prescription"]
    assert len(added("rx.create")) == 1
    e = added("rx.create")[0]
    assert e["resource_type"] == "prescription" and e["resource_id"] == str(a["id"]) and e["actor_role"] == "doctor"
    assert e["detail"]["lines"] == 1 and "Paracetamol" not in str(e["detail"])
    b = _issue(doctor, [line()], replaces=a["id"]).json()["prescription"]
    assert len(added("rx.create")) == 2 and len(added("rx.replace")) == 1
    doctor.post(f"/api/prescriptions/{b['id']}/stop", json={"reason": "Changed plan"})
    assert len(added("rx.stop")) == 1 and added("rx.stop")[0]["detail"]["reason"] == "Changed plan"
    _issue_from_midnight()
    c = patient_client(PID)
    dose = c.get("/api/me/today").json()["doses"][0]["id"]
    c.post(f"/api/me/doses/{dose}/report")
    c.post(f"/api/me/doses/{dose}/report")                        # the second tap is not logged again
    ev = added("dose.report")
    assert len(ev) == 1 and ev[0]["actor_type"] == "patient" and ev[0]["resource_id"] == str(dose)


def test_the_pharmacist_check_is_logged_without_a_login(doctor, patient_client, anon):
    from backend.app import authz
    _issue(doctor, [line()])
    token = patient_client(PID).get("/api/me/prescription-card").json()["card"]["token"]
    before = len([e for e in authz.ident().select("audit_events", [("action", "eq", "rx.verify")])])
    anon.get(f"/api/rx-check/{token}")
    rows = authz.ident().select("audit_events", [("action", "eq", "rx.verify")])
    assert len(rows) == before + 1
    assert rows[-1]["actor_type"] == "anonymous" and rows[-1]["patient_id"] == PID
    assert token not in str(rows[-1]["detail"]) and rows[-1]["detail"]["hospital_id"] == 1


# ------------------------------------------------------------------------------ demo data

def test_the_demo_prescription_for_ravi(patient_client, anon, rxdb):
    from backend.app.meds import seed_meds
    seed_meds.seed(rxdb)
    seed_meds.seed(rxdb)                                          # twice makes no second prescription
    assert len(rxdb.select("prescriptions", [("patient_id", "eq", 1)])) == 1
    c = patient_client(1)
    m = c.get("/api/me/medicines").json()
    assert m["patient"]["given_name"] == "Ravi" and m["patient"]["language"] == "hi"
    by = {x["drug_name"]: x for x in m["active"] + m["as_needed"]}
    assert (by["Paracetamol"]["strength"], by["Paracetamol"]["frequency_code"], by["Paracetamol"]["food_timing"],
            by["Paracetamol"]["duration_days"]) == ("500 mg", "1-0-1", "after_food", 5)
    assert (by["Pantoprazole"]["strength"], by["Pantoprazole"]["frequency_code"], by["Pantoprazole"]["food_timing"],
            by["Pantoprazole"]["duration_days"]) == ("40 mg", "1-0-0", "before_food", 14)
    assert by["Ondansetron"]["as_needed"] and by["Ondansetron"]["times"] == []
    assert len(m["today"]) == 3                                    # 2 paracetamol + 1 pantoprazole, all of today
    card = c.get("/api/me/prescription-card").json()["card"]
    assert card["doctor"]["name"] == "Dr. Meera Nair" and "fictional" in card["doctor"]["reg_no_display"]
    assert anon.get(card["verify_path"].replace("/rx.html?t=", "/api/rx-check/")).json()["current"] is True


def test_a_demo_reset_brings_the_demo_prescription_back(client, patient_client, doctor):
    _issue(doctor, [line()])                                       # made during the demo: gone after a reset
    assert client.post("/api/demo/reset").status_code == 200
    c = patient_client(1)
    m = c.get("/api/me/medicines").json()
    assert m["has_prescription"] and {x["drug_name"] for x in m["active"]} == {"Paracetamol", "Pantoprazole"}
    assert patient_client(PID).get("/api/me/medicines").json()["has_prescription"] is False


# ------------------------------------------------------------------------------ the pages

PAGES = ["web/prescribe.html", "web/meds.html", "web/rx.html", "web/css/meds.css",
         "docs/rebuild/meds_integration.md"] + [f"web/js/{p.name}" for p in (ROOT / "web/js").glob("meds-*.js")]
NEVER = ["approved", "compliant", "certified", "validated", "real-time monitoring", "prevents pneumonia",
         "reduces readmission", "abdm-integrated", "works with any spirometer", "accurately",
         "clinically proven", "guarantee", "first", "cure", "taken"]
MONEY = re.compile(r"₹|\brs\.?\s?\d|\bprice|\bcost\b|\bbill|insurance|\bpayments?\b|\bpay\b|\binr\b")


@pytest.mark.parametrize("path", PAGES)
def test_pages_obey_the_never_say_list(path):
    f = ROOT / path
    assert f.exists(), path
    text = f.read_text(encoding="utf-8").lower()
    assert [w for w in NEVER if w in text] == []
    assert MONEY.findall(text) == []


def test_pages_only_use_badge_keys_from_the_registry():
    from backend.app import features
    keys = set()
    for path in PAGES:
        keys |= set(re.findall(r'data-feature="([\w.]+)"', (ROOT / path).read_text(encoding="utf-8")))
        keys |= set(re.findall(r"SB\.ui\.badge\('([\w.]+)'\)", (ROOT / path).read_text(encoding="utf-8")))
    assert {"rx.manual", "rx.patient_phone", "rx.pharmacy_screen", "rx.verify_qr"} <= keys
    assert all(features.get(k) for k in keys), keys


def test_the_pages_are_served_and_staff_page_needs_a_login(client, anon):
    for p in ("/prescribe.html", "/meds.html", "/rx.html"):
        assert client.get(p).status_code == 200, p
    assert "qrcodejs/1.0.0/qrcode.min.js" in client.get("/meds.html").text
    from backend.app import main
    assert "/api/rx-check/" in main.PUBLIC_PREFIXES
