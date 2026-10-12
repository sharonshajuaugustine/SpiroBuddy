"""Patient login with the hospital registration number + a 6-digit PIN.

Public:  POST /api/me/login          {registration_no, pin} -> the patient-app session cookie
         GET  /api/me/login-demo     Ravi's number + PIN, only in DEMO_MODE (the demo box)
Staff:   GET  /api/patients/{pid}/login   the number and whether a PIN exists (never the PIN)
         POST /api/patients/{pid}/pin     a new PIN, shown once (patient.edit)
         PUT  /api/patients/{pid}/regno   type the hospital's own number (patient.edit)

Logic: patient_login.py. A PIN is never logged, never put in the audit detail and never stored
except as an argon2 hash. Until supabase/schema_v2.sql is pasted again the PIN columns do not exist
on Supabase: every route then answers "not set up yet" (503), nothing else is affected.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, Body, HTTPException, Request, Response

from . import audit, authz, ratelimit, service
from . import patient_login as pl
from .config import demo_mode
from .routes_auth import _end_session, _hospital, _start_session

log = logging.getLogger("spirobuddy.me")
router = APIRouter(tags=["patient-login"])

@router.get("/api/me/otp/hospitals")
def otp_hospitals(response: Response):
    _no_store(response)
    return service.store().select("hospitals", columns="id,name", order="name")


@router.post("/api/me/otp/request")
def otp_request(request: Request, response: Response, body: dict = Body(...)):
    from . import patient_otp as otp
    _no_store(response)
    if not ratelimit.allow("otp_request", audit.client_ip(request) or "?", 20, 900):
        raise HTTPException(429, "Please wait before requesting another code")
    hid, number = otp.identity(body)
    result = otp.request_code(hid, number)
    audit.write("auth.otp_request", "hospital", hid, actor=None,
                detail={"delivery": "simulated"}, request=request)
    return result


@router.post("/api/me/otp/verify")
def otp_verify(request: Request, response: Response, body: dict = Body(...)):
    from . import patient_otp as otp
    _no_store(response)
    if not ratelimit.allow("otp_verify", audit.client_ip(request) or "?", 40, 900):
        raise HTTPException(429, "Please wait before trying again")
    hid, number = otp.identity(body)
    try:
        p = otp.verify_code(hid, number, body.get("challenge_id"), body.get("code"))
    except HTTPException:
        audit.write("auth.otp_verify", "hospital", hid, actor=None,
                    detail={"ok": False}, request=request)
        raise
    _end_session(request, authz.PATIENT_COOKIE, "patient")
    _start_session(request, response, "patient", hid, patient_id=p["id"])
    audit.write("auth.otp_verify", "patient", p["id"], patient_id=p["id"],
                actor=authz.patient_actor(p), detail={"ok": True}, request=request)
    return {"ok": True, "patient_id": p["id"], "name": p["name"], "language": p.get("language") or "en"}

LOGIN_COLS = "id,name,language,hospital_id,mrn,pin_hash,pin_failed,pin_locked_until,programme_status"


def _no_store(response: Response) -> None:
    response.headers["Cache-Control"] = "no-store"


def _fail(request: Request, status: int, message: str, reason: str, row: dict | None = None,
          count_ip: bool = True) -> None:
    """Audit one failed login (no PIN anywhere) and answer."""
    if count_ip:
        ratelimit.allow("patient_login", audit.client_ip(request) or "?", pl.IP_TRIES,
                        pl.IP_WINDOW_SECONDS)
    audit.write("auth.patient_login", "patient", row["id"] if row else None,
                patient_id=row["id"] if row else None, actor=None,
                detail={"ok": False, "reason": reason,
                        "hospital_id": (row.get("hospital_id") or authz.LEGACY_HOSPITAL_ID)
                        if row else None},
                request=request)
    raise HTTPException(status, message)


# ----------------------------------------------------------------------------- the patient logs in

@router.post("/api/me/login")
def patient_login(request: Request, response: Response, body: dict = Body(...)):
    """Registration number + PIN -> the same patient session as /api/me/session."""
    _no_store(response)
    ip = audit.client_ip(request) or "?"
    if not ratelimit.peek("patient_login", ip, pl.IP_TRIES, pl.IP_WINDOW_SECONDS):
        audit.write("auth.patient_login", "patient", None, actor=None,
                    detail={"ok": False, "reason": "too many tries from this address"},
                    request=request)
        raise HTTPException(429, pl.MSG_IP_LIMIT)
    number, pin = body.get("registration_no"), pl.clean_pin(body.get("pin"))
    candidates = pl.regno_candidates(number) if isinstance(number, str) else []
    if not candidates or pin is None:
        raise HTTPException(400, pl.MSG_BAD_FORMAT)
    st = service.store()
    if not pl.columns_ready(st):
        raise HTTPException(503, pl.MSG_NOT_SET_UP)
    try:
        rows = st.select("patients", [("mrn", "in", candidates)], columns=LOGIN_COLS, limit=10)
    except Exception as e:
        log.warning("patient login lookup failed: %s", str(e)[:200])
        raise HTTPException(503, pl.MSG_NOT_SET_UP)
    rows = [r for r in rows if (r.get("programme_status") or "active") != "deceased"]
    if not rows:
        pl.pin_matches(None, pin)                       # same time spent as for a real number
        _fail(request, 401, pl.MSG_WRONG, "unknown number")
    live = [r for r in rows if not pl.is_locked(r)]
    if not live:
        _fail(request, 429, pl.MSG_LOCKED, "locked", rows[0], count_ip=False)
    matched = None
    for r in live:
        if r.get("pin_hash") and pl.pin_matches(r["pin_hash"], pin):
            matched = r
            break
    if matched is None:
        locked_now = False
        for r in live:
            if r.get("pin_hash"):
                locked_now = pl.note_failure(st, r) or locked_now
        if not any(r.get("pin_hash") for r in live):
            pl.pin_matches(None, pin)
        _fail(request, 429 if locked_now else 401, pl.MSG_LOCKED if locked_now else pl.MSG_WRONG,
              "locked now" if locked_now else "wrong pin", live[0])
    pl.note_success(st, matched)
    _end_session(request, authz.PATIENT_COOKIE, "patient")        # no old session of this browser stays
    hid = matched.get("hospital_id") or authz.LEGACY_HOSPITAL_ID
    _start_session(request, response, "patient", hid, patient_id=matched["id"])
    audit.write("auth.patient_login", "patient", matched["id"], patient_id=matched["id"],
                actor=authz.patient_actor(matched),
                detail={"ok": True, "hospital_id": hid}, request=request)
    return {"ok": True, "patient_id": matched["id"], "name": matched.get("name"),
            "language": matched.get("language") or "en"}


@router.get("/api/me/login-demo")
def login_demo(response: Response):
    """The demo box on the login page: only in DEMO_MODE, never anything real."""
    _no_store(response)
    if not demo_mode():
        return {"demo": False}
    return pl.demo_credentials(service.store())


# ----------------------------------------------------------------------------- staff side

def _patient_row(pid: int) -> dict:
    p = service.get_patient_row(pid)
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    return p


@router.get("/api/patients/{pid}/login")
def login_info(pid: int, response: Response):
    """For the "Patient login" card: the registration number and whether a PIN is set."""
    _no_store(response)
    actor = authz.require("patient.view", pid)
    p = _patient_row(pid)
    st = service.store()
    ready = pl.columns_ready(st)
    return {"patient_id": pid, "patient_name": p.get("name"),
            "hospital_id": p.get("hospital_id") or authz.LEGACY_HOSPITAL_ID,
            "phone_hint": "Ending " + str(p["phone"])[-2:] if p.get("phone") else "Phone number pending",
            "breathing_enabled": (p.get("routine") or {}).get("breathing_enabled", True),
            "can_plan_edit": authz.can(actor, "careplan.edit", pid),
            "hospital_name": _hospital(p.get("hospital_id") or authz.LEGACY_HOSPITAL_ID)["name"],
            "registration_no": pl.canonical_regno(p.get("mrn")) or None,
            "set_up": ready, "message": None if ready else pl.MSG_NOT_SET_UP,
            "has_pin": bool(ready and p.get("pin_hash")),
            "locked": bool(ready and pl.is_locked(p)),
            "can_edit": authz.can(actor, "patient.edit", pid),
            "login_path": "/patient-login.html"}


@router.put("/api/patients/{pid}/phone")
def set_phone(pid: int, request: Request, body: dict = Body(...)):
    import re
    actor = authz.require("patient.edit", pid)
    _patient_row(pid)
    phone = body.get("phone")
    if not isinstance(phone, str) or (phone and not re.fullmatch(r"\+?[0-9]{10,15}", phone)):
        raise HTTPException(400, "Enter 10 to 15 digits, optionally starting with +, or leave empty")
    from . import patient_otp as otp
    with otp.LOCK:
        service.store().update("patients", [("id", "eq", pid)], {"phone": phone or None})
        p = _patient_row(pid)
        service.store().delete("app_settings", [("key", "eq", otp._key(p.get("hospital_id") or 1, pl.canonical_regno(p.get("mrn"))))])
    audit.write("patient.phone_update", "patient", pid, patient_id=pid, actor=actor,
                detail={"phone_on_file": bool(phone)}, request=request)
    return {"ok": True}


@router.put("/api/patients/{pid}/breathing")
def set_breathing(pid: int, request: Request, body: dict = Body(...)):
    actor = authz.require("careplan.edit", pid)
    p = _patient_row(pid)
    enabled = body.get("enabled")
    if not isinstance(enabled, bool):
        raise HTTPException(400, "Choose whether breathing exercise is assigned")
    routine = {**(p.get("routine") or {}), "breathing_enabled": enabled}
    service.store().update("patients", [("id", "eq", pid)], {"routine": routine})
    audit.write("patient.breathing_assignment", "patient", pid, patient_id=pid, actor=actor,
                detail={"enabled": enabled}, request=request)
    return {"ok": True, "breathing_enabled": enabled}


@router.post("/api/patients/{pid}/pin")
def make_pin(pid: int, request: Request, response: Response):
    """A new 6-digit PIN for this patient. The PIN is in this answer only, once."""
    _no_store(response)
    actor = authz.require("patient.edit", pid)
    p = _patient_row(pid)
    st = service.store()
    if not pl.columns_ready(st):
        raise HTTPException(503, pl.MSG_NOT_SET_UP)
    number = pl.ensure_regno(st, p)
    pin = pl.new_pin()
    pl.set_pin(st, pid, pin)
    audit.write("patient.pin_create", "patient", pid, patient_id=pid, actor=actor, request=request,
                detail={"registration_no": number, "replaced_old_pin": bool(p.get("pin_hash"))})
    hid = p.get("hospital_id") or authz.LEGACY_HOSPITAL_ID
    return {"ok": True, "patient_id": pid, "patient_name": p.get("name"),
            "hospital_name": _hospital(hid)["name"], "registration_no": number, "pin": pin,
            "login_path": "/patient-login.html"}


@router.put("/api/patients/{pid}/regno")
def set_regno(pid: int, request: Request, body: dict = Body(...)):
    """Use the hospital's own registration number instead of the generated one."""
    actor = authz.require("patient.edit", pid)
    p = _patient_row(pid)
    raw = body.get("registration_no")
    number = pl.canonical_regno(raw) if isinstance(raw, str) else ""
    if not pl.REGNO_OK.match(number):
        raise HTTPException(400, "A hospital number uses 3 to 40 letters, numbers, - or /")
    st = service.store()
    if pl.regno_taken(st, p.get("hospital_id"), number, except_pid=pid):
        raise HTTPException(400, "Another patient in this hospital already has that number")
    old = pl.canonical_regno(p.get("mrn")) or None
    from . import patient_otp as otp
    try:
        with otp.LOCK:
            st.update("patients", [("id", "eq", pid)], {"mrn": number})
            hid = p.get("hospital_id") or authz.LEGACY_HOSPITAL_ID
            for changed_number in {old, number} - {None}:
                st.delete("app_settings", [("key", "eq", otp._key(hid, changed_number))])
    except Exception as e:
        log.warning("registration number not saved: %s", str(e)[:200])
        raise HTTPException(400, "That number could not be saved - is it used by another patient?")
    audit.write("patient.regno_set", "patient", pid, patient_id=pid, actor=actor, request=request,
                detail={"old": old, "new": number})
    return {"ok": True, "patient_id": pid, "registration_no": number}
