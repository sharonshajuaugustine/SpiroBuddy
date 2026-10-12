"""The booking rules for appointments (Contract I).

The database has no "proposed" status and its check list cannot change, so:
  Requested            = status 'requested' and the patient asked (requested_by_role 'patient')
  Alternative proposed = status 'requested' and staff (doctor / nurse / admin) suggested a time
  Confirmed / Declined / Cancelled / Attended / No-show = the status of the same name

One live visit (requested or confirmed) per doctor per time is the rule. It is enforced three
ways: a check before every write (which also catches overlaps), a module-level lock so two
requests in this process cannot both pass the check, and the unique index in the database as the
last line of defence (its error is turned into the same 409).
"""
from __future__ import annotations

import sqlite3
import threading
from datetime import date, datetime, timedelta

from fastapi import HTTPException

from .. import authz
from .. import service as core
from ..config import TZ, iso, now_local, parse_dt
from . import slots, words

LOCK = threading.Lock()
LIVE = ("requested", "confirmed")
STAFF_ROLES = ("doctor", "nurse", "admin")
KINDS = ("follow_up", "review", "other")
TAKEN = "That time was just taken. Please choose another."
FALLBACK_MINUTES = 15
MAX_WAITING = 3                      # requests a patient may have waiting for an answer
MAX_TEXT = 300
FLAGS = ("confirm", "propose", "decline", "cancel", "attended", "no_show", "accept")


# ----------------------------------------------------------------------------- small helpers

def state_of(row: dict) -> str:
    s = row.get("status")
    if s == "requested":
        return "proposed" if row.get("requested_by_role") in STAFF_ROLES else "requested"
    return s


def times(row: dict) -> tuple[datetime, datetime]:
    start = parse_dt(row["start_at"]).astimezone(TZ)
    end = parse_dt(row["end_at"]).astimezone(TZ) if row.get("end_at") \
        else start + timedelta(minutes=FALLBACK_MINUTES)
    return start, end


def clean_text(value, what: str) -> str | None:
    """Optional short text from a body: None when empty, 400 when not text or too long."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise HTTPException(400, f"{what} must be text")
    value = " ".join(value.split())
    if len(value) > MAX_TEXT:
        raise HTTPException(400, f"{what} must be {MAX_TEXT} characters or fewer")
    return value or None


def whole_number(value, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise HTTPException(400, f"{what} must be a whole number")
    try:
        return int(value)
    except ValueError:
        raise HTTPException(400, f"{what} must be a whole number")


def parse_start(value, now: datetime | None = None) -> datetime:
    """A date and time from a body, in India time to the minute: 400 unless it is a real time
    in the future and within 180 days."""
    now = now or now_local()
    if not isinstance(value, str) or not value.strip() or value.strip().isdigit():
        raise HTTPException(400, "start_at must be a date and time like 2026-10-15T10:30:00+05:30")
    try:
        dt = parse_dt(value)
    except (ValueError, OverflowError):
        raise HTTPException(400, "start_at must be a date and time like 2026-10-15T10:30:00+05:30")
    dt = dt.astimezone(TZ).replace(second=0, microsecond=0)
    if dt <= now:
        raise HTTPException(400, "That time has already passed. Please choose a later time.")
    if dt > now + timedelta(days=slots.MAX_DAYS_AHEAD):
        raise HTTPException(400, f"Visits can be booked up to {slots.MAX_DAYS_AHEAD} days ahead.")
    return dt


def parse_day(value) -> date:
    try:
        return slots.parse_day(value)
    except ValueError as e:
        raise HTTPException(400, str(e))


def unique_violation(e: Exception) -> bool:
    """The database refused a second live visit for the same doctor and time."""
    if isinstance(e, sqlite3.IntegrityError):
        return "UNIQUE" in str(e).upper()
    text = str(e).lower()
    return isinstance(e, RuntimeError) and ("duplicate key" in text or "23505" in text)


# ----------------------------------------------------------------------------- people

def doctor_row(doctor_id, hospital_id) -> dict:
    """An active doctor of this hospital, or 404 (another hospital's doctor looks like none)."""
    rows = authz.ident().select("staff", [("id", "eq", doctor_id)], limit=1) \
        if doctor_id is not None else []
    r = rows[0] if rows else None
    if not r or r.get("role") != "doctor" or r.get("status") != "active" \
            or int(r.get("hospital_id") or 0) != int(hospital_id):
        raise HTTPException(404, f"doctor {doctor_id} not found")
    return r


def patient_hospital(patient: dict) -> int:
    return int(patient.get("hospital_id") or authz.LEGACY_HOSPITAL_ID)


def primary_doctor(patient: dict) -> dict | None:
    try:
        return doctor_row(patient.get("primary_doctor_id"), patient_hospital(patient))
    except HTTPException:
        return None


def managed_ids(actor: authz.Actor) -> set[int]:
    """Patients this staff member may manage appointments for."""
    visible = authz.visible_patient_ids(actor)
    if actor.role in ("admin", "doctor"):          # the same answer for every patient they can see
        return set(visible) if authz.can(actor, "appt.manage") else set()
    return {p for p in visible if authz.can(actor, "appt.manage", p)}      # nurses: key by key


class Names:
    """Patient and doctor names for a page of appointments, looked up in two queries."""

    def __init__(self):
        self.patients: dict[int, str] = {}
        self.doctors: dict[int, str] = {}

    def load(self, rows: list[dict]) -> "Names":
        need_p = {int(r["patient_id"]) for r in rows if r.get("patient_id") is not None} \
            - self.patients.keys()
        need_d = {int(r["doctor_id"]) for r in rows if r.get("doctor_id") is not None} \
            - self.doctors.keys()
        if need_p:
            for p in core.store().select("patients", [("id", "in", sorted(need_p))],
                                         columns="id,name"):
                self.patients[int(p["id"])] = p.get("name") or ""
        if need_d:
            for s in authz.ident().select("staff", [("id", "in", sorted(need_d))],
                                          columns="id,name"):
                self.doctors[int(s["id"])] = s.get("name") or ""
        return self


# ----------------------------------------------------------------------------- how a row looks

def can_flags(state: str, start: datetime, viewer: str, manage_ok: bool = True,
              now: datetime | None = None) -> dict:
    """What THIS viewer ('staff' or 'patient') may do to a visit in this state right now."""
    now = now or now_local()
    future = start > now
    open_ = state in ("requested", "proposed", "confirmed")
    f = dict.fromkeys(FLAGS, False)
    if viewer == "patient":
        f["accept"] = state == "proposed" and future
        f["decline"] = state == "proposed"
        f["cancel"] = open_ and future
    elif manage_ok:
        f["confirm"] = state == "requested" and future
        f["propose"] = state in ("requested", "proposed")
        f["decline"] = state in ("requested", "proposed")
        f["cancel"] = open_ and future
        f["attended"] = f["no_show"] = \
            state == "confirmed" and start.date() <= now.astimezone(TZ).date()
    return f


def view(row: dict, names: Names, viewer: str, manage_ok: bool = True,
         now: datetime | None = None) -> dict:
    now = now or now_local()
    start, end = times(row)
    state = state_of(row)
    pid, did = row.get("patient_id"), row.get("doctor_id")
    return {
        "id": row["id"], "patient_id": pid, "patient_name": names.patients.get(pid) or "",
        "doctor_id": did, "doctor_name": names.doctors.get(did) or "",
        "start_at": iso(start), "end_at": iso(end), "state": state,
        "status_words": words.STATUS_WORDS.get(state, state), "when_words": words.when_words(start),
        "kind": row.get("kind") or "follow_up", "reason_text": row.get("reason_text"),
        "location": row.get("location"),
        "decline_reason": row.get("notes") if state in ("declined", "cancelled") else None,
        "upcoming": state in ("requested", "proposed", "confirmed") and end > now,
        "can": can_flags(state, start, viewer, manage_ok, now)}


def views(rows: list[dict], viewer: str, allowed: set[int] | None = None) -> list[dict]:
    """Views of many rows. `allowed` = patients the staff viewer may manage (None = all)."""
    names = Names().load(rows)
    now = now_local()
    return [view(r, names, viewer, allowed is None or int(r["patient_id"]) in allowed, now)
            for r in rows]


def get_row(appt_id: int) -> dict:
    rows = core.store().select("appointments", [("id", "eq", appt_id)], limit=1)
    if not rows:
        raise HTTPException(404, f"appointment {appt_id} not found")
    return rows[0]


# ----------------------------------------------------------------------------- free time

def _live_between(doctor_id: int, lo: datetime, hi: datetime, exclude_id=None) -> list[tuple]:
    """(start, end) of live visits of this doctor that start in [lo, hi)."""
    rows = core.store().select("appointments", [
        ("doctor_id", "eq", doctor_id), ("status", "in", list(LIVE)),
        ("start_at", "gte", iso(lo)), ("start_at", "lt", iso(hi))])
    return [times(r) for r in rows if exclude_id is None or r["id"] != exclude_id]


def overlaps_live(doctor_id, start: datetime, end: datetime, exclude_id=None) -> bool:
    if doctor_id is None:
        return False
    return any(s < end and e > start for s, e in
               _live_between(doctor_id, start - timedelta(days=1), end, exclude_id))


def free_slots(doctor_id: int, day) -> list[dict]:
    """[{start_at, end_at, location}] still free on that day (future only)."""
    offered = slots.offered(slots.load(doctor_id), day)
    if not offered:
        return []
    live = _live_between(doctor_id, slots.at(day, 0) - timedelta(days=1),
                         slots.at(day, 0) + timedelta(days=2))
    return [{"start_at": iso(o["start"]), "end_at": iso(o["end"]), "location": o["location"]}
            for o in offered if not any(s < o["end"] and e > o["start"] for s, e in live)]


# ----------------------------------------------------------------------------- writes

def waiting_count(patient_id: int) -> int:
    return len(core.store().select("appointments", [
        ("patient_id", "eq", patient_id), ("status", "eq", "requested"),
        ("start_at", "gt", iso(now_local()))], columns="id"))


def create(*, patient: dict, doctor: dict, start: datetime, minutes: int, location: str | None,
           kind: str, status: str, role: str, reason: str | None) -> dict:
    """Insert one visit, or 409 if the doctor already has one then."""
    end = start + timedelta(minutes=minutes)
    row = {"hospital_id": patient_hospital(patient), "patient_id": int(patient["id"]),
           "doctor_id": int(doctor["id"]), "department": doctor.get("department"), "kind": kind,
           "start_at": iso(start), "end_at": iso(end), "status": status,
           "requested_by_role": role, "reason_text": reason, "location": location,
           "notes": None, "created_at": iso(now_local())}
    with LOCK:
        if role == "patient" and waiting_count(row["patient_id"]) >= MAX_WAITING:
            raise HTTPException(409, f"You already have {MAX_WAITING} requests waiting. "
                                     "Please wait for the hospital to answer, or cancel one.")
        if overlaps_live(row["doctor_id"], start, end):
            raise HTTPException(409, TAKEN)
        try:
            return core.store().insert("appointments", [row])[0]
        except Exception as e:                       # the database's own guard
            if unique_violation(e):
                raise HTTPException(409, TAKEN)
            raise


def transition(appt_id: int, plan) -> dict:
    """Read the visit, let plan(row, now) check the rules and return the new values, then save
    them: all under the lock, so two people answering at once cannot both win."""
    with LOCK:
        row = get_row(appt_id)
        values = plan(row, now_local())
        try:
            core.store().update("appointments", [("id", "eq", appt_id)], values)
        except Exception as e:
            if unique_violation(e):
                raise HTTPException(409, TAKEN)
            raise
        return {**row, **values}


def _wrong_state(state: str, verb: str) -> HTTPException:
    return HTTPException(409, f"This visit is {words.STATUS_WORDS.get(state, state).lower()}, "
                              f"so it cannot be {verb}.")


STAFF_ACTIONS = ("confirm", "propose", "decline", "cancel", "attended", "no-show")
PATIENT_ACTIONS = ("accept", "decline", "cancel")


def staff_plan(action: str, role: str, body: dict, new_start: datetime | None):
    """The rules for what staff may do. Returns plan(row, now) for transition()."""
    reason = clean_text(body.get("reason"), "reason")

    def plan(row: dict, now: datetime) -> dict:
        state = state_of(row)
        start, end = times(row)
        if action == "confirm":
            if state == "proposed":
                raise HTTPException(409, "This time is waiting for the patient's answer.")
            if state != "requested":
                raise _wrong_state(state, "confirmed")
            if start <= now:
                raise HTTPException(409, "That time has passed. Propose another time or decline.")
            return {"status": "confirmed"}
        if action == "propose":
            if state not in ("requested", "proposed"):
                raise _wrong_state(state, "given a new time")
            if new_start == start:
                raise HTTPException(400, "That is the same time. Please choose a different time.")
            new_end = new_start + (end - start)
            if overlaps_live(row.get("doctor_id"), new_start, new_end, exclude_id=row["id"]):
                raise HTTPException(409, TAKEN)
            return {"start_at": iso(new_start), "end_at": iso(new_end), "status": "requested",
                    "requested_by_role": role}
        if action == "decline":
            if state not in ("requested", "proposed"):
                raise _wrong_state(state, "declined")
            return {"status": "declined", "notes": reason}
        if action == "cancel":
            if state not in ("requested", "proposed", "confirmed"):
                raise _wrong_state(state, "cancelled")
            if start <= now:
                raise HTTPException(409, "This visit time has passed, so it cannot be cancelled.")
            return {"status": "cancelled", "notes": reason}
        # attended / no-show
        verb = "marked as attended" if action == "attended" else "marked as no-show"
        if state != "confirmed":
            raise _wrong_state(state, verb)
        if start.date() > now.astimezone(TZ).date():
            raise HTTPException(409, "This can only be marked on the day of the visit or after.")
        return {"status": "attended" if action == "attended" else "no_show"}

    return plan


def patient_plan(action: str):
    """The rules for what the patient may do to their own visit."""
    def plan(row: dict, now: datetime) -> dict:
        state = state_of(row)
        start, _ = times(row)
        if action == "accept":
            if state != "proposed":
                raise HTTPException(409, "There is no new time to accept.")
            if start <= now:
                raise HTTPException(409, "That time has passed. Please ask for a new visit.")
            return {"status": "confirmed"}
        if action == "decline":
            if state != "proposed":
                raise HTTPException(409, "There is no new time to say no to.")
            return {"status": "cancelled", "notes": "patient declined the proposed time"}
        if state not in ("requested", "proposed", "confirmed"):
            raise _wrong_state(state, "cancelled")
        if start <= now:
            raise HTTPException(409, "This visit time has passed, so it cannot be cancelled.")
        return {"status": "cancelled", "notes": "cancelled by the patient"}
    return plan


# ----------------------------------------------------------------------------- lists

DB_STATUS = {"requested": "requested", "proposed": "requested", "confirmed": "confirmed",
             "declined": "declined", "cancelled": "cancelled", "attended": "attended",
             "no_show": "no_show"}


def normalise_status(value) -> str | None:
    """A status filter from the query string: 'no-show' and 'no_show' both work."""
    if value in (None, ""):
        return None
    s = str(value).strip().lower().replace("-", "_")
    if s not in DB_STATUS:
        raise HTTPException(400, "status must be one of: " + ", ".join(words.STATES))
    return s


def list_rows(actor: authz.Actor, *, doctor_id=None, patient_id=None, date_from=None,
              date_to=None, status: str | None = None, limit: int = 300) -> list[dict]:
    """Visits this staff member may manage, newest start first."""
    allowed = managed_ids(actor)
    if not allowed or (patient_id is not None and patient_id not in allowed):
        return []
    f: list = []
    if doctor_id is not None:
        f.append(("doctor_id", "eq", doctor_id))
    if patient_id is not None:
        f.append(("patient_id", "eq", patient_id))
    elif len(allowed) <= 400:
        f.append(("patient_id", "in", sorted(allowed)))
    else:
        f.append(("hospital_id", "eq", actor.hospital_id))
    if date_from is not None:
        f.append(("start_at", "gte", iso(slots.at(date_from, 0))))
    if date_to is not None:
        f.append(("start_at", "lt", iso(slots.at(date_to + timedelta(days=1), 0))))
    if status:
        f.append(("status", "eq", DB_STATUS[status]))
    rows = core.store().select("appointments", f, order="start_at", desc=True)
    rows = [r for r in rows if int(r["patient_id"]) in allowed
            and (not status or state_of(r) == status)]
    return rows[:max(1, min(int(limit), 1000))]


def day_view(actor: authz.Actor, doctor: dict, day) -> dict:
    """The doctor's day: requests to answer, proposals waiting for the patient, that day's visits."""
    allowed = managed_ids(actor)
    did = int(doctor["id"])
    st = core.store()
    waiting_rows = st.select("appointments", [("doctor_id", "eq", did),
                                              ("status", "eq", "requested")])
    visit_rows = st.select("appointments", [
        ("doctor_id", "eq", did), ("status", "in", ["confirmed", "attended", "no_show"]),
        ("start_at", "gte", iso(slots.at(day, 0))),
        ("start_at", "lt", iso(slots.at(day + timedelta(days=1), 0)))])
    waiting_rows = [r for r in waiting_rows if int(r["patient_id"]) in allowed]
    visit_rows = sorted((r for r in visit_rows if int(r["patient_id"]) in allowed),
                        key=lambda r: times(r)[0])
    asked = sorted((r for r in waiting_rows if state_of(r) == "requested"),
                   key=lambda r: (r.get("created_at") or "", times(r)[0]))
    proposed = sorted((r for r in waiting_rows if state_of(r) == "proposed"),
                      key=lambda r: times(r)[0])
    names = Names().load(waiting_rows + visit_rows)
    now = now_local()

    def many(rows):
        return [view(r, names, "staff", True, now) for r in rows]

    return {"date": day.isoformat(), "date_words": words.date_words(day),
            "doctor": {"id": did, "name": doctor.get("name") or ""},
            "needs_answer": many(asked), "waiting_for_patient": many(proposed),
            "visits": many(visit_rows),
            "counts": {"visits": len(visit_rows), "needs_answer": len(asked),
                       "waiting_for_patient": len(proposed)}}


def patient_items(patient_id: int) -> list[dict]:
    """The patient's own visits, upcoming first (soonest first), then the past (newest first)."""
    rows = core.store().select("appointments", [("patient_id", "eq", patient_id)],
                               order="start_at", desc=True)
    names = Names().load(rows)
    now = now_local()
    items = [view(r, names, "patient", True, now) for r in rows]
    upcoming = sorted((i for i in items if i["upcoming"]), key=lambda i: i["start_at"])
    past = [i for i in items if not i["upcoming"]]
    return (upcoming + past)[:100]
