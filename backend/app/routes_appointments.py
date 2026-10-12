"""Appointments (Contract I, docs/ARCHITECTURE.md section 18). Logic: backend/app/appointments/.

Staff: a doctor's weekly hours and free slots, the list of visits, booking, and answering a
patient's request (confirm / propose another time / decline), cancelling, attended, no-show,
and a doctor's day. Patient (/api/me/*): their own visits, the free slots of their own doctor,
asking for a visit, and answering a new time the hospital proposed.

Who may do what (REBUILD_PLAN 3.3): staff need appt.manage (hospital admin, doctor, or a nurse
whose key has "manage_appointments"); a patient uses appt.request on their own id. The middleware
already answers 404 for an appointment or doctor (path parameter) that the caller cannot see;
query and body ids are checked here, with the same 404.
"""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException, Query, Request

from . import audit, authz
from . import service as core
from .appointments import service as svc
from .appointments import slots

router = APIRouter()


# ----------------------------------------------------------------------------- helpers

def _manager() -> authz.Actor:
    """The logged-in staff member, if they may manage appointments at all (else 401 / 403)."""
    actor = authz.require_staff()
    if not authz.can(actor, "appt.manage"):
        raise HTTPException(403, "you don't have permission to do this")
    return actor


def _me() -> authz.Actor:
    a = authz.current_actor()
    if a is None or a.kind != "patient" or a.patient_id is None:
        raise HTTPException(401, "login needed")
    return a


def _patient(pid: int) -> dict:
    p = core.get_patient_row(pid)
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    return p


def _day_or_400(value):
    if value in (None, ""):
        raise HTTPException(400, "date is required, like 2026-10-15")
    return svc.parse_day(value)


def _body(body) -> dict:
    return body if isinstance(body, dict) else {}


# ----------------------------------------------------------------------------- doctor hours and slots

@router.get("/api/doctors/{doctor_id}/availability")
def get_availability(doctor_id: int):
    actor = _manager()
    svc.doctor_row(doctor_id, actor.hospital_id)
    return slots.load(doctor_id)


@router.put("/api/doctors/{doctor_id}/availability")
def put_availability(doctor_id: int, request: Request, body: dict = Body(...)):
    """The doctor themself or a hospital admin replaces the weekly hours and the leave / extra days."""
    actor = authz.require_staff()
    if not (actor.role == "admin" or (actor.role == "doctor" and actor.id == doctor_id)):
        raise HTTPException(403, "only the doctor or the hospital admin can change these hours")
    svc.doctor_row(doctor_id, actor.hospital_id)
    try:
        slots.save(doctor_id, actor.hospital_id, body)
    except ValueError as e:
        raise HTTPException(400, str(e))
    saved = slots.load(doctor_id)
    audit.write("availability.update", "availability", doctor_id, actor=actor, request=request,
                detail={"doctor_id": doctor_id,
                        "weekly_rows": 0 if saved["default"] else len(saved["weekly"]),
                        "exceptions": len(saved["exceptions"])})
    return saved


@router.get("/api/slots")
def get_slots(doctor: int | None = Query(None), day: str | None = Query(None, alias="date")):
    """Free future slots of one doctor on one day."""
    actor = _manager()
    if doctor is None:
        raise HTTPException(400, "doctor is required")
    d = _day_or_400(day)
    svc.doctor_row(doctor, actor.hospital_id)
    return svc.free_slots(doctor, d)


# ----------------------------------------------------------------------------- staff: visits

@router.get("/api/appointments")
def list_appointments(doctor: int | None = Query(None), patient: int | None = Query(None),
                      date_from: str | None = Query(None, alias="from"),
                      date_to: str | None = Query(None, alias="to"),
                      status: str | None = Query(None), limit: int = Query(300)):
    actor = _manager()
    if doctor is not None:
        svc.doctor_row(doctor, actor.hospital_id)
    if patient is not None:
        authz.require("appt.manage", patient)
    lo = svc.parse_day(date_from) if date_from not in (None, "") else None
    hi = svc.parse_day(date_to) if date_to not in (None, "") else None
    rows = svc.list_rows(actor, doctor_id=doctor, patient_id=patient, date_from=lo, date_to=hi,
                         status=svc.normalise_status(status), limit=limit)
    return svc.views(rows, "staff", svc.managed_ids(actor))


@router.post("/api/appointments")
def book(request: Request, body: dict = Body(...)):
    """Staff book a visit: it is confirmed at once. A taken time is 409."""
    pid = svc.whole_number(body.get("patient_id"), "patient_id")
    actor = authz.require("appt.manage", pid)
    patient = _patient(pid)
    doctor = svc.doctor_row(svc.whole_number(body.get("doctor_id"), "doctor_id"),
                            actor.hospital_id)
    start = svc.parse_start(body.get("start_at"))
    kind = body.get("kind") or "follow_up"
    if kind not in svc.KINDS:
        raise HTTPException(400, "kind must be follow_up, review or other")
    reason = svc.clean_text(body.get("reason_text"), "reason_text")
    minutes, place = slots.length_and_place(slots.load(int(doctor["id"])), start)
    row = svc.create(patient=patient, doctor=doctor, start=start, minutes=minutes, location=place,
                     kind=kind, status="confirmed", role=actor.role, reason=reason)
    audit.write("appt.book", "appointment", row["id"], patient_id=pid, actor=actor,
                request=request, detail={"doctor_id": doctor["id"], "start_at": row["start_at"],
                                         "kind": kind})
    return svc.views([row], "staff")[0]


@router.post("/api/appointments/{appt}/{action}")
def answer(appt: int, action: str, request: Request, body: dict | None = Body(default=None)):
    """confirm | propose {start_at} | decline {reason} | cancel {reason?} | attended | no-show"""
    action = action.lower().replace("_", "-")
    if action not in svc.STAFF_ACTIONS:
        raise HTTPException(404, f"no such action: {action}")
    row = svc.get_row(appt)
    pid = int(row["patient_id"])
    actor = authz.require("appt.manage", pid)
    body = _body(body)
    new_start = svc.parse_start(body.get("start_at")) if action == "propose" else None
    updated = svc.transition(appt, svc.staff_plan(action, actor.role, body, new_start))
    detail = {"doctor_id": updated.get("doctor_id"), "start_at": updated.get("start_at"),
              "from_start_at": row.get("start_at"), "reason_given": bool(body.get("reason"))}
    audit.write("appt." + action.replace("-", "_"), "appointment", appt, patient_id=pid,
                actor=actor, request=request, detail=detail)
    return svc.views([updated], "staff")[0]


@router.get("/api/doctor/day")
def doctor_day(day: str | None = Query(None, alias="date"), doctor: int | None = Query(None)):
    """A doctor's day: requests to answer, times waiting for the patient, and that day's visits.
    A doctor sees their own day; an admin or a nurse with the permission passes ?doctor=."""
    actor = _manager()
    d = svc.parse_day(day) if day not in (None, "") else slots.now_day()
    if doctor is None:
        if actor.role != "doctor":
            raise HTTPException(400, "doctor is required")
        doctor = actor.id
    elif actor.role == "doctor" and doctor != actor.id:
        raise HTTPException(403, "you can only open your own day")
    return svc.day_view(actor, svc.doctor_row(doctor, actor.hospital_id), d)


# ----------------------------------------------------------------------------- the patient (/api/me/*)

def _my_doctor(patient: dict) -> dict:
    doctor = svc.primary_doctor(patient)
    if doctor is None:
        raise HTTPException(409, "No doctor is assigned to you yet. Please ask the hospital.")
    return doctor


@router.get("/api/me/appointments")
def me_appointments():
    a = _me()
    pid = int(a.patient_id)
    authz.require("appt.request", pid)
    doctor = svc.primary_doctor(_patient(pid))
    return {"doctor": {"id": doctor["id"], "name": doctor.get("name") or ""} if doctor else None,
            "items": svc.patient_items(pid)}


@router.get("/api/me/slots")
def me_slots(day: str | None = Query(None, alias="date")):
    """Free slots of the patient's own doctor on one day."""
    a = _me()
    pid = int(a.patient_id)
    authz.require("appt.request", pid)
    doctor = _my_doctor(_patient(pid))
    return svc.free_slots(int(doctor["id"]), _day_or_400(day))


@router.post("/api/me/appointments")
def me_request(request: Request, body: dict = Body(...)):
    """The patient asks for one of the free slots of their doctor. Status: Requested."""
    a = _me()
    pid = int(a.patient_id)
    actor = authz.require("appt.request", pid)
    patient = _patient(pid)
    doctor = _my_doctor(patient)
    start = svc.parse_start(body.get("start_at"))
    reason = svc.clean_text(body.get("reason_text"), "reason_text")
    did = int(doctor["id"])
    av = slots.load(did)
    offered = {o["start"]: o for o in slots.offered(av, start.date())}
    if start not in offered:
        raise HTTPException(400, "That time is not available. Please choose one of the times shown.")
    o = offered[start]
    minutes = int((o["end"] - o["start"]).total_seconds() // 60)
    row = svc.create(patient=patient, doctor=doctor, start=start, minutes=minutes,
                     location=o["location"], kind="follow_up", status="requested",
                     role="patient", reason=reason)
    audit.write("appt.request", "appointment", row["id"], patient_id=pid, actor=actor,
                request=request, detail={"doctor_id": did, "start_at": row["start_at"]})
    return svc.views([row], "patient")[0]


@router.post("/api/me/appointments/{appt}/{action}")
def me_answer(appt: int, action: str, request: Request):
    """accept (the time the hospital proposed) | decline (that time) | cancel (own visit)"""
    action = action.lower()
    if action not in svc.PATIENT_ACTIONS:
        raise HTTPException(404, f"no such action: {action}")
    a = _me()
    pid = int(a.patient_id)
    actor = authz.require("appt.request", pid)
    row = svc.get_row(appt)
    if int(row["patient_id"]) != pid:
        raise HTTPException(404, f"appointment {appt} not found")
    updated = svc.transition(appt, svc.patient_plan(action))
    audit.write("appt.patient_" + action, "appointment", appt, patient_id=pid, actor=actor,
                request=request, detail={"doctor_id": updated.get("doctor_id"),
                                         "start_at": updated.get("start_at")})
    return svc.views([updated], "patient")[0]
