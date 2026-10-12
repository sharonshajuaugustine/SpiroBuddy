"""Appointments (Contract I, docs/ARCHITECTURE.md section 18): hours and slots, a patient asking for
a visit, staff booking, confirm / propose / decline / cancel / attended / no-show, double booking,
hospital separation, nurse permissions and the audit log.

Fictional demo accounts only (backend/app/seed_auth.py): Dr. Meera Nair (id 2) has patients 1, 2,
4, 6; Dr. Kabir Rao (id 3) has patients 3, 5, 7; Sister Anjali has every nurse permission for
Dr. Meera's patients; Nurse Thomas has only view + acknowledge_alerts (patients 3 and 5).
"""
from __future__ import annotations

import re
import threading
from datetime import timedelta

import pytest

from backend.app.config import iso, now_local, parse_dt

MEERA, KABIR = "meera.nair@demo-general.example", "kabir.rao@demo-general.example"
ANJALI, THOMAS = "anjali@demo-general.example", "thomas@demo-general.example"
RIVERSIDE_ADMIN = "admin@demo-riverside.example"
MEERA_ID, KABIR_ID = 2, 3
PID, PID2 = 1, 2             # Dr. Meera's patients
KABIR_PATIENT = 3            # Dr. Kabir's patient (Nurse Thomas can see him)
WORDS = re.compile(r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \d{1,2} "
                   r"(January|February|March|April|May|June|July|August|September|October|"
                   r"November|December) \d{4}, \d{1,2}:\d{2} (AM|PM)$")


# ----------------------------------------------------------------------------- helpers

def _store():
    from backend.app import service
    return service.store()


def _wipe():
    st = _store()
    for table in ("appointments", "availability", "availability_exceptions"):
        st.delete(table, [("id", "gte", 0)])


@pytest.fixture(autouse=True)
def clean_world(client):
    """No visits and no saved hours before and after each test: every doctor has the built-in hours."""
    _wipe()
    yield
    _wipe()


def expected_words(iso_text: str) -> str:
    dt = parse_dt(iso_text)
    return (f"{dt:%A}, {dt.day} {dt:%B} {dt.year}, "
            f"{dt.hour % 12 or 12}:{dt:%M} {'AM' if dt.hour < 12 else 'PM'}")


def open_days(c, n: int = 1, doctor: int = MEERA_ID, first: int = 1):
    """[(date, slots)] for the next n days on which the doctor has free slots."""
    found = []
    for i in range(first, first + 21):
        day = (now_local().date() + timedelta(days=i)).isoformat()
        r = c.get(f"/api/slots?doctor={doctor}&date={day}")
        assert r.status_code == 200, r.text
        if len(r.json()) >= 4:
            found.append((day, r.json()))
        if len(found) == n:
            return found
    raise AssertionError("no open days found")


def book(c, pid, doctor, start_at, **extra):
    return c.post("/api/appointments", json={"patient_id": pid, "doctor_id": doctor,
                                             "start_at": start_at, **extra})


def ask(pc, start_at, **extra):
    return pc.post("/api/me/appointments", json={"start_at": start_at, **extra})


def move(appt_id, **values):
    _store().update("appointments", [("id", "eq", appt_id)], values)


def audit_rows(action, appt_id=None):
    from backend.app import authz
    rows = authz.ident().select("audit_events", [("action", "eq", action)])
    if appt_id is not None:
        rows = [r for r in rows if r["resource_id"] == str(appt_id)]
    return rows


def free_starts(c, day, doctor=MEERA_ID):
    return [s["start_at"] for s in c.get(f"/api/slots?doctor={doctor}&date={day}").json()]


@pytest.fixture()
def meera(login_as):
    return login_as(MEERA)


@pytest.fixture()
def patient(patient_client):
    return patient_client(PID)


# ----------------------------------------------------------------------------- 1. request -> confirm

def test_patient_request_then_doctor_confirms(client, meera, patient):
    (day, slots), = open_days(client)
    s = slots[0]
    r = ask(patient, s["start_at"], reason_text="Check my wound")
    assert r.status_code == 200, r.text
    a = r.json()
    assert a["state"] == "requested" and a["status_words"] == "Requested"
    assert a["patient_id"] == PID and a["doctor_id"] == MEERA_ID
    assert a["doctor_name"] == "Dr. Meera Nair" and a["patient_name"]
    assert a["start_at"] == s["start_at"] and a["end_at"] == s["end_at"]
    assert a["location"] == "OPD" and a["reason_text"] == "Check my wound"
    assert WORDS.match(a["when_words"]) and a["when_words"] == expected_words(s["start_at"])
    assert a["start_at"].endswith("+05:30")
    assert a["can"]["cancel"] and not a["can"]["confirm"] and not a["can"]["accept"]
    # the slot is taken now
    assert s["start_at"] not in free_starts(client, day)
    # Dr. Meera sees it among the requests she must answer
    d = meera.get(f"/api/doctor/day?date={day}").json()
    assert d["doctor"] == {"id": MEERA_ID, "name": "Dr. Meera Nair"}
    assert [x["id"] for x in d["needs_answer"]] == [a["id"]]
    assert d["counts"]["needs_answer"] == 1 and d["counts"]["visits"] == 0
    assert d["needs_answer"][0]["can"]["confirm"] and d["needs_answer"][0]["can"]["propose"]
    # she confirms; the patient sees Confirmed with the date in words
    r = meera.post(f"/api/appointments/{a['id']}/confirm")
    assert r.status_code == 200, r.text
    assert r.json()["state"] == "confirmed" and r.json()["status_words"] == "Confirmed"
    mine = patient.get("/api/me/appointments").json()
    assert mine["doctor"] == {"id": MEERA_ID, "name": "Dr. Meera Nair"}
    item = mine["items"][0]
    assert item["id"] == a["id"] and item["status_words"] == "Confirmed"
    assert item["when_words"] == expected_words(s["start_at"])
    assert item["upcoming"] is True
    d = meera.get(f"/api/doctor/day?date={day}").json()
    assert d["needs_answer"] == [] and [v["id"] for v in d["visits"]] == [a["id"]]
    assert d["date_words"] == expected_words(s["start_at"]).rsplit(",", 1)[0]
    # confirming twice is a clear 409
    assert meera.post(f"/api/appointments/{a['id']}/confirm").status_code == 409


# ----------------------------------------------------------------------------- 2. propose / decline

def test_propose_then_patient_accepts(client, meera, patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    r = meera.post(f"/api/appointments/{a['id']}/propose", json={"start_at": slots[1]["start_at"]})
    assert r.status_code == 200, r.text
    p = r.json()
    assert p["state"] == "proposed" and p["status_words"] == "Alternative proposed"
    assert p["start_at"] == slots[1]["start_at"]
    assert not p["can"]["confirm"]            # waiting for the patient, not for the doctor
    # the old slot is free again, the new one is held
    free = free_starts(client, day)
    assert slots[0]["start_at"] in free and slots[1]["start_at"] not in free
    # the doctor sees it as "waiting for the patient"
    d = meera.get(f"/api/doctor/day?date={day}").json()
    assert d["needs_answer"] == [] and [x["id"] for x in d["waiting_for_patient"]] == [a["id"]]
    # the patient sees the new time and can accept it
    item = patient.get("/api/me/appointments").json()["items"][0]
    assert item["status_words"] == "Alternative proposed"
    assert item["when_words"] == expected_words(slots[1]["start_at"])
    assert item["can"]["accept"] and item["can"]["decline"] and item["can"]["cancel"]
    r = patient.post(f"/api/me/appointments/{a['id']}/accept")
    assert r.status_code == 200, r.text
    assert r.json()["state"] == "confirmed" and r.json()["status_words"] == "Confirmed"
    assert r.json()["start_at"] == slots[1]["start_at"]
    # nothing left to accept
    assert patient.post(f"/api/me/appointments/{a['id']}/accept").status_code == 409


def test_propose_then_patient_declines(client, meera, patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    meera.post(f"/api/appointments/{a['id']}/propose", json={"start_at": slots[2]["start_at"]})
    r = patient.post(f"/api/me/appointments/{a['id']}/decline")
    assert r.status_code == 200, r.text
    assert r.json()["state"] == "cancelled" and r.json()["status_words"] == "Cancelled"
    assert r.json()["decline_reason"] == "patient declined the proposed time"
    assert slots[2]["start_at"] in free_starts(client, day)          # the held time is free again
    # a patient cannot accept or decline a plain request of their own
    b = ask(patient, slots[0]["start_at"]).json()
    assert patient.post(f"/api/me/appointments/{b['id']}/accept").status_code == 409
    assert patient.post(f"/api/me/appointments/{b['id']}/decline").status_code == 409


def test_doctor_declines_with_a_reason(client, meera, patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    r = meera.post(f"/api/appointments/{a['id']}/decline",
                   json={"reason": "Please see the ward nurse first"})
    assert r.status_code == 200, r.text
    assert r.json()["state"] == "declined" and r.json()["status_words"] == "Declined"
    assert r.json()["decline_reason"] == "Please see the ward nurse first"
    item = patient.get("/api/me/appointments").json()["items"][0]
    assert item["status_words"] == "Declined"
    assert item["decline_reason"] == "Please see the ward nurse first"
    assert not item["upcoming"] and not any(item["can"].values())
    assert slots[0]["start_at"] in free_starts(client, day)
    assert meera.post(f"/api/appointments/{a['id']}/decline", json={}).status_code == 409


# ----------------------------------------------------------------------------- 3. cancel / attended

def test_cancel_by_patient_and_by_staff(client, meera, patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    r = patient.post(f"/api/me/appointments/{a['id']}/cancel")
    assert r.status_code == 200 and r.json()["status_words"] == "Cancelled"
    assert patient.post(f"/api/me/appointments/{a['id']}/cancel").status_code == 409
    assert slots[0]["start_at"] in free_starts(client, day)
    # staff book a visit, then cancel it with a reason
    b = book(client, PID, MEERA_ID, slots[1]["start_at"], kind="review").json()
    assert b["state"] == "confirmed" and b["kind"] == "review"
    r = meera.post(f"/api/appointments/{b['id']}/cancel", json={"reason": "Doctor is in surgery"})
    assert r.status_code == 200 and r.json()["state"] == "cancelled"
    assert r.json()["decline_reason"] == "Doctor is in surgery"
    assert meera.post(f"/api/appointments/{b['id']}/cancel").status_code == 409
    # and a confirmed visit can be cancelled by the patient too
    c = book(client, PID, MEERA_ID, slots[2]["start_at"]).json()
    assert patient.post(f"/api/me/appointments/{c['id']}/cancel").json()["state"] == "cancelled"


def test_attended_and_no_show_only_when_allowed(client, meera, patient):
    (day, slots), = open_days(client)
    a = book(client, PID, MEERA_ID, slots[0]["start_at"]).json()
    # the visit is tomorrow or later: too early
    assert not a["can"]["attended"] and not a["can"]["no_show"]
    assert meera.post(f"/api/appointments/{a['id']}/attended").status_code == 409
    assert meera.post(f"/api/appointments/{a['id']}/no-show").status_code == 409
    # today (a bit later) or in the past: allowed, but only on a confirmed visit
    today_late = now_local().replace(hour=23, minute=50, second=0, microsecond=0)
    move(a["id"], start_at=iso(today_late), end_at=iso(today_late + timedelta(minutes=15)))
    listed = meera.get(f"/api/appointments?patient={PID}").json()
    assert listed[0]["can"]["attended"] and listed[0]["can"]["no_show"]
    r = meera.post(f"/api/appointments/{a['id']}/attended")
    assert r.status_code == 200 and r.json()["state"] == "attended"
    assert r.json()["status_words"] == "Attended"
    assert meera.post(f"/api/appointments/{a['id']}/no-show").status_code == 409   # already attended
    assert meera.post(f"/api/appointments/{a['id']}/cancel").status_code == 409
    # a visit that was missed in the past
    b = book(client, PID, MEERA_ID, slots[1]["start_at"]).json()
    past = now_local() - timedelta(hours=3)
    move(b["id"], start_at=iso(past), end_at=iso(past + timedelta(minutes=15)))
    r = meera.post(f"/api/appointments/{b['id']}/no-show")
    assert r.status_code == 200 and r.json()["state"] == "no_show"
    assert r.json()["status_words"] == "No-show"
    # a plain request (not confirmed) cannot be marked, and neither can a past visit be cancelled
    c = ask(patient, slots[2]["start_at"]).json()
    move(c["id"], start_at=iso(past - timedelta(hours=1)))
    assert meera.post(f"/api/appointments/{c['id']}/attended").status_code == 409
    assert meera.post(f"/api/appointments/{c['id']}/confirm").status_code == 409   # time has passed
    assert patient.post(f"/api/me/appointments/{c['id']}/cancel").status_code == 409
    # the patient's own list: past things come after the upcoming ones
    items = patient.get("/api/me/appointments").json()["items"]
    assert [i["upcoming"] for i in items] == sorted((i["upcoming"] for i in items), reverse=True)


def test_wrong_state_and_bad_action(client, meera, patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    assert meera.post(f"/api/appointments/{a['id']}/explode").status_code == 404
    assert patient.post(f"/api/me/appointments/{a['id']}/confirm").status_code == 404
    assert patient.post(f"/api/me/appointments/{a['id']}/attended").status_code == 404
    assert meera.post("/api/appointments/999999/confirm").status_code == 404
    # propose needs a real new time
    assert meera.post(f"/api/appointments/{a['id']}/propose").status_code == 400
    assert meera.post(f"/api/appointments/{a['id']}/propose",
                      json={"start_at": "not a time"}).status_code == 400
    past = iso(now_local() - timedelta(days=1))
    assert meera.post(f"/api/appointments/{a['id']}/propose", json={"start_at": past}).status_code == 400
    assert meera.post(f"/api/appointments/{a['id']}/propose",
                      json={"start_at": slots[0]["start_at"]}).status_code == 400   # same time
    # a proposed time that is taken by someone else is a 409
    b = book(client, PID2, MEERA_ID, slots[3]["start_at"]).json()
    assert b["state"] == "confirmed"
    assert meera.post(f"/api/appointments/{a['id']}/propose",
                      json={"start_at": slots[3]["start_at"]}).status_code == 409
    # confirming a proposal is the patient's job
    meera.post(f"/api/appointments/{a['id']}/propose", json={"start_at": slots[1]["start_at"]})
    r = meera.post(f"/api/appointments/{a['id']}/confirm")
    assert r.status_code == 409 and "patient" in r.json()["error"]


# ----------------------------------------------------------------------------- 4. double booking

def test_double_booking_is_refused(client, meera, patient, patient_client):
    (day, slots), = open_days(client)
    s = slots[0]["start_at"]
    assert book(client, PID, MEERA_ID, s).status_code == 200
    r = book(client, PID2, MEERA_ID, s)
    assert r.status_code == 409 and "just taken" in r.json()["error"]
    r = ask(patient, s)
    assert r.status_code == 409 and "just taken" in r.json()["error"]
    assert s not in free_starts(client, day)
    # a cancelled visit gives the time back
    first = meera.get(f"/api/appointments?patient={PID}").json()[0]
    meera.post(f"/api/appointments/{first['id']}/cancel")
    assert s in free_starts(client, day)
    assert ask(patient, s).status_code == 200
    # an overlapping time (a slot is 15 minutes) is refused as well
    odd = iso(parse_dt(s) + timedelta(minutes=5))
    assert book(client, PID2, MEERA_ID, odd).status_code == 409


def test_two_requests_for_the_same_slot_exactly_one_wins(client, patient_client):
    (day, slots), = open_days(client)
    s = slots[0]["start_at"]
    pids = [1, 2, 4, 6]                         # all Dr. Meera's patients
    clients = [patient_client(p) for p in pids]
    barrier = threading.Barrier(len(clients))
    results = []

    def go(pc):
        barrier.wait()
        results.append(ask(pc, s).status_code)

    threads = [threading.Thread(target=go, args=(pc,)) for pc in clients]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    assert sorted(results) == [200, 409, 409, 409], results
    live = [r for r in _store().select("appointments", [("doctor_id", "eq", MEERA_ID)])
            if r["status"] in ("requested", "confirmed")]
    assert len(live) == 1


def test_database_guard_turns_a_unique_violation_into_409(client, monkeypatch):
    """Even if the check before the write were skipped, the unique index answers 409."""
    from backend.app.appointments import service as svc
    (day, slots), = open_days(client)
    s = slots[0]["start_at"]
    assert book(client, PID, MEERA_ID, s).status_code == 200
    monkeypatch.setattr(svc, "overlaps_live", lambda *a, **k: False)
    r = book(client, PID2, MEERA_ID, s)
    assert r.status_code == 409 and "just taken" in r.json()["error"]
    assert len(_store().select("appointments")) == 1
    assert svc.unique_violation(RuntimeError(
        'Supabase POST /rest/v1/appointments: 409 {"code":"23505","message":"duplicate key value"}'))
    assert not svc.unique_violation(RuntimeError("Supabase POST /rest/v1/appointments: 500 boom"))


def test_a_patient_can_only_have_three_requests_waiting(client, patient):
    (day, slots), = open_days(client)
    for s in slots[:3]:
        assert ask(patient, s["start_at"]).status_code == 200
    r = ask(patient, slots[3]["start_at"])
    assert r.status_code == 409 and "3 requests" in r.json()["error"]


# ----------------------------------------------------------------------------- 5. hospitals and patients stay apart

def test_another_hospital_gets_404_everywhere(client, login_as, patient, riverside_patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    b = book(client, PID, MEERA_ID, slots[1]["start_at"]).json()
    other = login_as(RIVERSIDE_ADMIN)
    for appt_id in (a["id"], b["id"]):
        for action in ("confirm", "cancel", "decline", "attended", "no-show"):
            assert other.post(f"/api/appointments/{appt_id}/{action}").status_code == 404
        assert other.post(f"/api/appointments/{appt_id}/propose",
                          json={"start_at": slots[2]["start_at"]}).status_code == 404
    # the doctor and the patient of the other hospital do not exist for them
    assert other.get(f"/api/doctors/{MEERA_ID}/availability").status_code == 404
    assert other.put(f"/api/doctors/{MEERA_ID}/availability", json={"weekly": []}).status_code == 404
    assert other.get(f"/api/slots?doctor={MEERA_ID}&date={day}").status_code == 404
    assert other.get(f"/api/appointments?patient={PID}").status_code == 404
    assert other.get(f"/api/appointments?doctor={MEERA_ID}").status_code == 404
    assert other.get(f"/api/doctor/day?doctor={MEERA_ID}&date={day}").status_code == 404
    assert book(other, PID, MEERA_ID, slots[2]["start_at"]).status_code == 404
    assert other.get("/api/appointments").json() == []
    # the other hospital's own patient cannot be booked with this hospital's doctor either
    assert book(other, riverside_patient, MEERA_ID, slots[2]["start_at"]).status_code == 404
    # nothing changed for the home hospital
    assert client.get(f"/api/appointments?patient={PID}").json()[0]["state"] in ("requested", "confirmed")
    assert len(client.get("/api/appointments").json()) == 2


def test_a_patient_only_sees_and_acts_on_their_own_visits(client, patient, patient_client):
    (day, slots), = open_days(client)
    mine = ask(patient, slots[0]["start_at"]).json()
    other = patient_client(PID2)
    theirs = ask(other, slots[1]["start_at"]).json()
    assert [i["id"] for i in patient.get("/api/me/appointments").json()["items"]] == [mine["id"]]
    assert [i["id"] for i in other.get("/api/me/appointments").json()["items"]] == [theirs["id"]]
    for action in ("accept", "decline", "cancel"):
        assert patient.post(f"/api/me/appointments/{theirs['id']}/{action}").status_code == 404
    # still intact
    assert client.get(f"/api/appointments?patient={PID2}").json()[0]["state"] == "requested"
    # patients have no way into the staff routes
    assert patient.get("/api/appointments").status_code in (401, 403)
    assert patient.post(f"/api/appointments/{mine['id']}/confirm").status_code in (401, 403)
    assert patient.get(f"/api/doctors/{MEERA_ID}/availability").status_code in (401, 403)
    assert patient.get(f"/api/slots?doctor={MEERA_ID}&date={day}").status_code in (401, 403)


def test_not_logged_in_is_401(anon):
    assert anon.get("/api/appointments").status_code == 401
    assert anon.get("/api/me/appointments").status_code == 401
    assert anon.get("/api/slots?doctor=2&date=2030-01-01").status_code == 401
    assert anon.post("/api/appointments/1/confirm").status_code == 401


# ----------------------------------------------------------------------------- 6. nurse permission

def test_nurse_without_manage_appointments_gets_403(client, login_as):
    (day, slots), = open_days(client, doctor=KABIR_ID)
    kabir = login_as(KABIR)
    visit = book(kabir, KABIR_PATIENT, KABIR_ID, slots[0]["start_at"]).json()
    assert visit["state"] == "confirmed"
    thomas = login_as(THOMAS)           # sees patient 3 (view + acknowledge_alerts only)
    assert thomas.get("/api/appointments").status_code == 403
    assert thomas.get(f"/api/appointments?patient={KABIR_PATIENT}").status_code == 403
    assert thomas.get(f"/api/slots?doctor={KABIR_ID}&date={day}").status_code == 403
    assert thomas.get(f"/api/doctors/{KABIR_ID}/availability").status_code == 403
    assert thomas.get(f"/api/doctor/day?doctor={KABIR_ID}").status_code == 403
    assert thomas.post(f"/api/appointments/{visit['id']}/cancel").status_code == 403
    assert thomas.post(f"/api/appointments/{visit['id']}/propose",
                       json={"start_at": slots[1]["start_at"]}).status_code == 403
    assert book(thomas, KABIR_PATIENT, KABIR_ID, slots[1]["start_at"]).status_code == 403
    assert thomas.put(f"/api/doctors/{KABIR_ID}/availability", json={"weekly": []}).status_code == 403
    # a patient outside the key is not even visible
    (d2, s2), = open_days(client)
    other = book(client, PID, MEERA_ID, s2[0]["start_at"]).json()
    assert thomas.post(f"/api/appointments/{other['id']}/cancel").status_code == 404
    # nothing was changed
    assert client.get(f"/api/appointments?patient={KABIR_PATIENT}").json()[0]["state"] == "confirmed"


def test_nurse_with_manage_appointments_works_in_her_scope(client, login_as, patient):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    anjali = login_as(ANJALI)           # every permission, Dr. Meera's patients
    assert anjali.get("/api/doctor/day").status_code == 400            # a nurse must pick the doctor
    d = anjali.get(f"/api/doctor/day?doctor={MEERA_ID}&date={day}").json()
    assert [x["id"] for x in d["needs_answer"]] == [a["id"]]
    r = anjali.post(f"/api/appointments/{a['id']}/confirm")
    assert r.status_code == 200 and r.json()["state"] == "confirmed"
    b = book(anjali, PID2, MEERA_ID, slots[1]["start_at"], reason_text="Stitches out")
    assert b.status_code == 200 and b.json()["state"] == "confirmed"
    assert {x["id"] for x in anjali.get("/api/appointments").json()} == {a["id"], b.json()["id"]}
    # but not Dr. Kabir's patients
    assert book(anjali, KABIR_PATIENT, KABIR_ID, slots[2]["start_at"]).status_code == 404
    # nurses cannot change a doctor's working hours
    assert anjali.put(f"/api/doctors/{MEERA_ID}/availability", json={"weekly": []}).status_code == 403
    assert audit_rows("appt.confirm", a["id"])[0]["actor_role"] == "nurse"


# ----------------------------------------------------------------------------- 7. bad input

def test_bad_dates_and_times(client, meera, patient):
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date=banana").status_code == 400
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date=2026-13-45").status_code == 400
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date=2026-W41-1").status_code == 400
    assert client.get(f"/api/slots?doctor={MEERA_ID}").status_code == 400
    assert client.get("/api/slots?date=2030-01-01").status_code == 400
    assert client.get(f"/api/slots?doctor=999999&date=2030-01-01").status_code == 404
    assert client.get(f"/api/slots?doctor=1&date=2030-01-01").status_code == 404     # the admin is no doctor
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date=2020-01-01").json() == []  # only future times
    far = (now_local().date() + timedelta(days=400)).isoformat()
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date={far}").json() == []
    assert patient.get("/api/me/slots").status_code == 400
    assert patient.get("/api/me/slots?date=nope").status_code == 400
    assert client.get("/api/appointments?from=nope").status_code == 400
    assert client.get("/api/appointments?status=nonsense").status_code == 400
    (day, slots), = open_days(client)
    ok = slots[0]["start_at"]
    past = iso(now_local() - timedelta(hours=1))
    toofar = iso(now_local() + timedelta(days=181))
    for bad in (None, "", "banana", "12345", 12345, past, toofar, "2026-02-30T10:00:00+05:30"):
        body = {"patient_id": PID, "doctor_id": MEERA_ID, "start_at": bad}
        assert client.post("/api/appointments", json=body).status_code == 400, bad
        assert patient.post("/api/me/appointments", json={"start_at": bad}).status_code == 400, bad
    assert book(client, PID, MEERA_ID, ok, kind="surgery").status_code == 400
    assert book(client, PID, MEERA_ID, ok, reason_text="x" * 400).status_code == 400
    assert book(client, PID, MEERA_ID, ok, reason_text=5).status_code == 400
    assert client.post("/api/appointments", json={"doctor_id": MEERA_ID, "start_at": ok}).status_code == 400
    assert client.post("/api/appointments",
                       json={"patient_id": "abc", "doctor_id": MEERA_ID, "start_at": ok}).status_code == 400
    assert client.post("/api/appointments",
                       json={"patient_id": PID, "doctor_id": True, "start_at": ok}).status_code == 400
    assert book(client, 999999, MEERA_ID, ok).status_code == 404
    assert _store().select("appointments") == []          # none of the bad ones saved anything


def test_a_time_that_is_not_a_free_slot(client, patient):
    (day, slots), = open_days(client)
    start = parse_dt(slots[0]["start_at"])
    at_3am = iso(start.replace(hour=3, minute=0))
    half_way = iso(start + timedelta(minutes=7))              # between two slots
    assert patient.post("/api/me/appointments", json={"start_at": at_3am}).status_code == 400
    assert patient.post("/api/me/appointments", json={"start_at": half_way}).status_code == 400
    # a Sunday has no hours (Monday to Saturday by default)
    sunday = next(now_local().date() + timedelta(days=i) for i in range(1, 8)
                  if (now_local().date() + timedelta(days=i)).weekday() == 6)
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date={sunday}").json() == []
    sun_time = iso(parse_dt(f"{sunday}T10:00:00+05:30"))
    assert patient.post("/api/me/appointments", json={"start_at": sun_time}).status_code == 400
    # staff may book outside the usual hours (a special visit)
    assert book(client, PID, MEERA_ID, sun_time).status_code == 200
    assert _store().select("appointments", [("patient_id", "eq", PID)])[0]["status"] == "confirmed"


def test_a_doctor_of_another_hospital_or_not_a_doctor(client, login_as):
    from backend.app import authz
    ist = authz.ident()
    row = ist.insert("staff", [{"hospital_id": 2, "role": "doctor", "name": "Dr. Riverside Test",
                                "email": "dr.riverside.apptest@demo.example", "status": "active"}])[0]
    try:
        (day, slots), = open_days(client)
        s = slots[0]["start_at"]
        assert book(client, PID, row["id"], s).status_code == 404            # the doctor of hospital 2
        assert book(client, PID, 1, s).status_code == 404                    # an admin, not a doctor
        assert book(client, PID, 4, s).status_code == 404                    # a nurse
        assert client.get(f"/api/doctors/{row['id']}/availability").status_code == 404
        assert client.get(f"/api/slots?doctor={row['id']}&date={day}").status_code == 404
        assert client.get(f"/api/appointments?doctor={row['id']}").status_code == 404
        # a doctor who has been switched off cannot be booked
        ist.update("staff", [("id", "eq", MEERA_ID)], {"status": "disabled"})
        try:
            assert book(client, PID, MEERA_ID, s).status_code == 404
        finally:
            ist.update("staff", [("id", "eq", MEERA_ID)], {"status": "active"})
        assert _store().select("appointments") == []
    finally:
        ist.delete("staff", [("id", "eq", row["id"])])


def test_patient_without_a_doctor(client, patient_client, riverside_patient):
    pc = patient_client(riverside_patient)
    r = pc.get("/api/me/slots?date=2030-01-01")
    assert r.status_code == 409 and r.json()["error"] == \
        "No doctor is assigned to you yet. Please ask the hospital."
    assert pc.post("/api/me/appointments", json={"start_at": "2030-01-01T10:00:00+05:30"}).status_code in (400, 409)
    (day, slots), = open_days(client)
    assert pc.post("/api/me/appointments", json={"start_at": slots[0]["start_at"]}).status_code == 409
    mine = pc.get("/api/me/appointments").json()
    assert mine == {"doctor": None, "items": []}


# ----------------------------------------------------------------------------- hours, leave, extra days

def test_default_hours_then_the_doctor_sets_their_own(client, meera, login_as):
    av = client.get(f"/api/doctors/{MEERA_ID}/availability").json()
    assert av["default"] is True and av["exceptions"] == []
    assert [w["weekday"] for w in av["weekly"]] == [0, 1, 2, 3, 4, 5]
    assert av["weekly"][0] == {"weekday": 0, "start_time": "09:30", "end_time": "13:00",
                               "slot_minutes": 15, "location": "OPD"}
    week = [{"weekday": d, "start_time": "10:00", "end_time": "11:00", "slot_minutes": 30,
             "location": "Room 4"} for d in range(7)]
    day1 = (now_local().date() + timedelta(days=2)).isoformat()
    day2 = (now_local().date() + timedelta(days=3)).isoformat()
    day3 = (now_local().date() + timedelta(days=4)).isoformat()
    body = {"weekly": week, "exceptions": [
        {"date": day1, "kind": "leave"},
        {"date": day2, "kind": "leave", "start_time": "10:00", "end_time": "10:30"},
        {"date": day3, "kind": "extra", "start_time": "16:00", "end_time": "17:00"}]}
    r = meera.put(f"/api/doctors/{MEERA_ID}/availability", json=body)      # the doctor, for themself
    assert r.status_code == 200, r.text
    saved = r.json()
    assert saved["default"] is False and len(saved["weekly"]) == 7
    assert saved["exceptions"] == [
        {"date": day1, "kind": "leave"},
        {"date": day2, "kind": "leave", "start_time": "10:00", "end_time": "10:30"},
        {"date": day3, "kind": "extra", "start_time": "16:00", "end_time": "17:00"}]
    assert client.get(f"/api/doctors/{MEERA_ID}/availability").json() == saved
    day0 = (now_local().date() + timedelta(days=1)).isoformat()
    s0 = client.get(f"/api/slots?doctor={MEERA_ID}&date={day0}").json()
    assert [parse_dt(s["start_at"]).strftime("%H:%M") for s in s0] == ["10:00", "10:30"]
    assert s0[0]["location"] == "Room 4"
    assert parse_dt(s0[0]["end_at"]) - parse_dt(s0[0]["start_at"]) == timedelta(minutes=30)
    assert client.get(f"/api/slots?doctor={MEERA_ID}&date={day1}").json() == []        # on leave
    s2 = client.get(f"/api/slots?doctor={MEERA_ID}&date={day2}").json()
    assert [parse_dt(s["start_at"]).strftime("%H:%M") for s in s2] == ["10:30"]        # part-day leave
    s3 = client.get(f"/api/slots?doctor={MEERA_ID}&date={day3}").json()
    assert [parse_dt(s["start_at"]).strftime("%H:%M") for s in s3] == \
        ["10:00", "10:30", "16:00", "16:30"]                                           # extra session
    # a booked slot drops out of the list, and the patient sees the doctor's own slots
    assert book(client, PID, MEERA_ID, s0[0]["start_at"]).status_code == 200
    assert [s["start_at"] for s in client.get(f"/api/slots?doctor={MEERA_ID}&date={day0}").json()] == \
        [s0[1]["start_at"]]
    assert book(client, PID, MEERA_ID, s0[0]["start_at"]).status_code == 409
    # a hospital admin can change it too; another doctor cannot
    kabir = login_as(KABIR)
    assert kabir.put(f"/api/doctors/{MEERA_ID}/availability", json=body).status_code == 403
    r = client.put(f"/api/doctors/{MEERA_ID}/availability", json={"weekly": week[:1]})
    assert r.status_code == 200 and len(r.json()["weekly"]) == 1 and r.json()["exceptions"] == []
    # saving an empty week goes back to the built-in hours
    r = client.put(f"/api/doctors/{MEERA_ID}/availability", json={"weekly": [], "exceptions": []})
    assert r.status_code == 200 and r.json()["default"] is True
    assert _store().select("availability", [("doctor_id", "eq", MEERA_ID)]) == []
    # Dr. Kabir's hours were never touched
    assert client.get(f"/api/doctors/{KABIR_ID}/availability").json()["default"] is True


def test_bad_hours_are_refused(client, meera):
    url = f"/api/doctors/{MEERA_ID}/availability"
    good = {"weekday": 1, "start_time": "09:00", "end_time": "12:00", "slot_minutes": 20}
    day = (now_local().date() + timedelta(days=3)).isoformat()
    for bad in ({"weekly": [{**good, "weekday": 7}]}, {"weekly": [{**good, "weekday": -1}]},
                {"weekly": [{**good, "weekday": "1"}]}, {"weekly": [{**good, "start_time": "9am"}]},
                {"weekly": [{**good, "end_time": "08:00"}]}, {"weekly": [{**good, "slot_minutes": 2}]},
                {"weekly": [{**good, "slot_minutes": 500}]}, {"weekly": "Monday"},
                {"weekly": [good], "exceptions": [{"date": "soon", "kind": "leave"}]},
                {"weekly": [good], "exceptions": [{"date": day, "kind": "holiday"}]},
                {"weekly": [good], "exceptions": [{"date": day, "kind": "extra"}]},
                {"weekly": [good], "exceptions": [{"date": day, "kind": "leave", "start_time": "10:00"}]},
                {"weekly": [good], "exceptions": [{"date": "2099-01-01", "kind": "leave"}]}):
        assert meera.put(url, json=bad).status_code == 400, bad
    assert client.get(url).json()["default"] is True           # nothing was saved
    assert meera.put(url, json=["not", "an", "object"]).status_code == 422


# ----------------------------------------------------------------------------- lists and filters

def test_list_filters_and_order(client, meera, patient):
    days = open_days(client, 2)
    (d1, s1), (d2, s2) = days
    a = book(client, PID, MEERA_ID, s1[0]["start_at"]).json()
    b = book(client, PID2, MEERA_ID, s2[0]["start_at"]).json()
    c = ask(patient, s2[1]["start_at"]).json()
    all_ = client.get("/api/appointments").json()
    assert [x["id"] for x in all_] == [c["id"], b["id"], a["id"]]            # newest start first
    assert [x["id"] for x in client.get(f"/api/appointments?patient={PID2}").json()] == [b["id"]]
    assert {x["id"] for x in client.get(f"/api/appointments?doctor={MEERA_ID}").json()} == \
        {a["id"], b["id"], c["id"]}
    assert client.get(f"/api/appointments?doctor={KABIR_ID}").json() == []
    assert [x["id"] for x in client.get("/api/appointments?status=requested").json()] == [c["id"]]
    assert {x["id"] for x in client.get("/api/appointments?status=confirmed").json()} == {a["id"], b["id"]}
    assert client.get("/api/appointments?status=proposed").json() == []
    meera.post(f"/api/appointments/{c['id']}/propose", json={"start_at": s2[2]["start_at"]})
    assert [x["id"] for x in client.get("/api/appointments?status=proposed").json()] == [c["id"]]
    assert client.get("/api/appointments?status=requested").json() == []
    assert [x["id"] for x in client.get(f"/api/appointments?from={d1}&to={d1}").json()] == [a["id"]]
    assert {x["id"] for x in client.get(f"/api/appointments?from={d2}").json()} == {b["id"], c["id"]}
    assert client.get(f"/api/appointments?to={d1}").json()[0]["id"] == a["id"]
    assert client.get("/api/appointments?status=no-show").json() == []
    # every row carries all the contract fields
    keys = {"id", "patient_id", "patient_name", "doctor_id", "doctor_name", "start_at", "end_at",
            "state", "status_words", "when_words", "kind", "reason_text", "location",
            "decline_reason", "can"}
    assert keys <= set(all_[0]) and set(all_[0]["can"]) == {
        "confirm", "propose", "decline", "cancel", "attended", "no_show", "accept"}
    # Dr. Kabir sees none of Dr. Meera's patients
    assert login_kabir(client).get("/api/appointments").json() == []


def login_kabir(client):
    from tests.conftest import _new_client
    c = _new_client()
    assert c.post("/api/auth/login", json={"email": KABIR, "password": "demo-doctor-2026"}).status_code == 200
    return c


def test_doctor_day_rules(client, meera, patient, login_as):
    (d1, s1), (d2, s2) = open_days(client, 2)
    ask(patient, s2[0]["start_at"])                                          # a request for a later day
    v2 = book(client, PID2, MEERA_ID, s1[1]["start_at"]).json()
    v1 = book(client, PID, MEERA_ID, s1[0]["start_at"]).json()
    d = meera.get(f"/api/doctor/day?date={d1}").json()
    assert [v["id"] for v in d["visits"]] == [v1["id"], v2["id"]]            # by time
    assert d["counts"] == {"visits": 2, "needs_answer": 1, "waiting_for_patient": 0}
    assert len(d["needs_answer"]) == 1                                       # any date
    assert d["date"] == d1
    # today is the default day
    assert meera.get("/api/doctor/day").json()["date"] == now_local().date().isoformat()
    # an admin has to say which doctor; a doctor only opens their own day
    assert client.get("/api/doctor/day").status_code == 400
    assert client.get(f"/api/doctor/day?doctor={MEERA_ID}&date={d1}").json()["counts"]["visits"] == 2
    assert meera.get(f"/api/doctor/day?doctor={KABIR_ID}").status_code == 403
    assert meera.get("/api/doctor/day?date=nope").status_code == 400
    kabir = login_as(KABIR)
    k = kabir.get(f"/api/doctor/day?date={d1}").json()
    assert k["visits"] == [] and k["needs_answer"] == [] and k["counts"]["visits"] == 0
    assert kabir.get(f"/api/doctor/day?doctor={MEERA_ID}").status_code == 403


# ----------------------------------------------------------------------------- 8. audit

def test_every_write_leaves_an_audit_row(client, meera, patient, login_as):
    (day, slots), = open_days(client)
    a = ask(patient, slots[0]["start_at"]).json()
    rows = audit_rows("appt.request", a["id"])
    assert len(rows) == 1 and rows[0]["patient_id"] == PID
    assert rows[0]["actor_type"] == "patient" and rows[0]["actor_id"] == PID
    assert rows[0]["resource_type"] == "appointment"
    # propose -> patient accepts
    meera.post(f"/api/appointments/{a['id']}/propose", json={"start_at": slots[1]["start_at"]})
    patient.post(f"/api/me/appointments/{a['id']}/accept")
    for action in ("appt.propose", "appt.patient_accept"):
        assert len(audit_rows(action, a["id"])) == 1, action
    # book -> cancel
    b = book(client, PID2, MEERA_ID, slots[2]["start_at"]).json()
    booked = audit_rows("appt.book", b["id"])
    assert len(booked) == 1 and booked[0]["actor_role"] == "admin" and booked[0]["patient_id"] == PID2
    client.post(f"/api/appointments/{b['id']}/cancel")
    assert len(audit_rows("appt.cancel", b["id"])) == 1
    # decline, patient decline of a proposal, patient cancel
    c = ask(patient, slots[3]["start_at"]).json()
    meera.post(f"/api/appointments/{c['id']}/decline", json={"reason": "No"})
    assert len(audit_rows("appt.decline", c["id"])) == 1
    d = ask(patient, slots[4]["start_at"]).json()
    meera.post(f"/api/appointments/{d['id']}/propose", json={"start_at": slots[5]["start_at"]})
    patient.post(f"/api/me/appointments/{d['id']}/decline")
    assert len(audit_rows("appt.patient_decline", d["id"])) == 1
    e = ask(patient, slots[6]["start_at"]).json()
    patient.post(f"/api/me/appointments/{e['id']}/cancel")
    assert len(audit_rows("appt.patient_cancel", e["id"])) == 1
    # confirm, attended, no-show
    f = ask(patient, slots[7]["start_at"]).json()
    meera.post(f"/api/appointments/{f['id']}/confirm")
    assert len(audit_rows("appt.confirm", f["id"])) == 1
    past = now_local() - timedelta(hours=2)
    move(f["id"], start_at=iso(past), end_at=iso(past + timedelta(minutes=15)))
    meera.post(f"/api/appointments/{f['id']}/attended")
    assert len(audit_rows("appt.attended", f["id"])) == 1
    g = book(client, PID2, MEERA_ID, slots[8]["start_at"]).json()
    move(g["id"], start_at=iso(past), end_at=iso(past + timedelta(minutes=15)))
    meera.post(f"/api/appointments/{g['id']}/no-show")
    assert len(audit_rows("appt.no_show", g["id"])) == 1
    # a refused action writes nothing
    before = len(audit_rows("appt.cancel"))
    assert meera.post(f"/api/appointments/{b['id']}/cancel").status_code == 409
    assert len(audit_rows("appt.cancel")) == before
    # hours
    before = len(audit_rows("availability.update", MEERA_ID))
    meera.put(f"/api/doctors/{MEERA_ID}/availability",
              json={"weekly": [{"weekday": 0, "start_time": "10:00", "end_time": "12:00"}]})
    hours = audit_rows("availability.update", MEERA_ID)
    assert len(hours) == before + 1
    assert hours[-1]["actor_role"] == "doctor" and hours[-1]["patient_id"] is None
    # the audit detail holds no free text (a reason may mention health)
    detail = audit_rows("appt.decline", c["id"])[0]["detail"]
    assert detail["reason_given"] is True and "reason" not in detail
