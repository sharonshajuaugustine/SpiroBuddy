"""Digital prescription routes (Contract H, docs/ARCHITECTURE.md section 17) and the patient's
medicines (Contract K /api/me/*). Logic lives in backend/app/meds/.

The doctor types a prescription; saving it issues it. The patient sees it on their phone, shows a
pharmacy screen at the counter, and the pharmacist can scan a QR to check the hospital's copy.
There is no photo upload and no AI here.

Who may do what (REBUILD_PLAN 3.3): rx.create = doctors only (admins, nurses and patients get 403);
reading = patient.view; a patient reports a dose with dose.report on their own id. The middleware
already answers 404 for any pid / rx / item / dose the caller cannot see.
"""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException, Query, Request, Response

from . import audit, authz, ratelimit
from . import service as core
from .config import demo_mode, iso, now_local, parse_dt
from .meds import service as meds

router = APIRouter()


def _patient(pid: int) -> dict:
    p = core.get_patient_row(pid)
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    return p


def _rx_row(rx: int) -> dict:
    rows = meds.st().select("prescriptions", [("id", "eq", rx)], limit=1)
    if not rows:
        raise HTTPException(404, f"prescription {rx} not found")
    return rows[0]


def _rx_body(rx_id: int) -> dict:
    v = meds.get_prescription(rx_id)
    return {"prescription": v, "items": v["lines"], "warnings": meds.warnings_of(v), "document": None}


# ---------------------------------------------------------------------------- staff

@router.post("/api/patients/{pid}/prescriptions")
def issue_prescription(pid: int, request: Request, body: dict = Body(...)):
    """The doctor types the lines; saving issues it at once. -> {prescription, items, warnings}.
    `replaces` (a current prescription id) makes the old one history ("replaced")."""
    actor = authz.require("rx.create", pid)
    patient = _patient(pid)
    try:
        rx, warnings = meds.create_prescription(
            patient, actor.id, body.get("lines"), prescribed_on=body.get("prescribed_on"),
            prescriber_on_paper=body.get("prescriber_on_paper"), replaces=body.get("replaces"))
    except ValueError as e:
        raise HTTPException(400, str(e))
    except LookupError as e:
        raise HTTPException(404, str(e))
    audit.write("rx.create", "prescription", rx["id"], patient_id=pid, actor=actor, request=request,
                detail={"version": rx["version"], "lines": len(rx["lines"]),
                        "unclear_lines": sum(1 for ln in rx["lines"] if ln["unclear_fields"]),
                        "replaces": rx["supersedes_id"]})
    if rx["supersedes_id"]:
        audit.write("rx.replace", "prescription", rx["supersedes_id"], patient_id=pid, actor=actor,
                    request=request, detail={"replaced_by": rx["id"]})
    return {"prescription": rx, "items": rx["lines"], "warnings": warnings, "document": None}


@router.get("/api/prescriptions/{rx}")
def get_prescription(rx: int):
    row = _rx_row(rx)
    authz.require("patient.view", int(row["patient_id"]))
    return _rx_body(rx)


@router.post("/api/prescriptions/{rx}/stop")
def stop_prescription(rx: int, request: Request, body: dict | None = Body(default=None)):
    row = _rx_row(rx)
    pid = int(row["patient_id"])
    actor = authz.require("rx.create", pid)
    reason = " ".join(str((body or {}).get("reason") or "").split())[:200]
    try:
        meds.stop_prescription(rx)
    except ValueError as e:
        raise HTTPException(409, str(e))
    audit.write("rx.stop", "prescription", rx, patient_id=pid, actor=actor, request=request,
                detail={"reason": reason or None})
    return _rx_body(rx)


@router.get("/api/patients/{pid}/medicines")
def patient_medicines(pid: int):
    authz.require("patient.view", pid)
    _patient(pid)
    return meds.medicines_for(pid)


@router.get("/api/patients/{pid}/doses")
def patient_doses(pid: int, date_from: str | None = Query(None, alias="from"),
                  date_to: str | None = Query(None, alias="to")):
    authz.require("patient.view", pid)
    _patient(pid)
    try:
        return meds.doses_for(pid, date_from, date_to)
    except ValueError:
        raise HTTPException(400, "from and to must be dates like 2026-10-11")


@router.post("/api/patients/{pid}/doses/{dose}/report")
def staff_report_dose(pid: int, dose: int, request: Request):
    """Staff report a dose on the patient's behalf (logged with their role)."""
    actor = authz.require("dose.report", pid)
    if meds.owner_of_dose(dose) != pid:
        raise HTTPException(404, f"dose {dose} not found")
    return _report(dose, pid, actor, "staff", request)


def _report(dose: int, pid: int, actor: authz.Actor, channel: str, request: Request) -> dict:
    try:
        view, new = meds.report_dose(dose, actor.role, actor.id, channel)
    except LookupError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(409, str(e))
    if new:
        audit.write("dose.report", "dose_event", dose, patient_id=pid, actor=actor, request=request,
                    detail={"by": actor.role, "channel": channel})
    return view


# ---------------------------------------------------------------------------- the patient (/api/me/*)

def _me() -> authz.Actor:
    a = authz.current_actor()
    if a is None or a.kind != "patient" or a.patient_id is None:
        raise HTTPException(401, "login needed")
    return a


@router.get("/api/me/medicines")
def me_medicines():
    """Everything the medicines screen needs: today's doses, every current medicine, the ones
    'only when needed'. Only issued, current prescriptions - never a draft."""
    a = _me()
    pid = int(a.patient_id)
    authz.require("patient.view", pid)
    p = _patient(pid)
    meds.refresh_doses(pid)
    m = meds.medicines_for(pid)
    newest = m["current"][0] if m["current"] else None
    hosp = meds._hospital(p.get("hospital_id") or authz.LEGACY_HOSPITAL_ID)
    return {
        "patient": {"id": pid, "name": p.get("name"), "given_name": (p.get("name") or "").split(" ")[0],
                    "age": p.get("age"), "sex": p.get("sex"), "language": p.get("language") or "en"},
        "hospital": {"name": hosp.get("name")},
        "doctor": newest["doctor"]["name"] if newest else None,
        "has_prescription": bool(newest), "issued_on": newest["issued_on"] if newest else None,
        "today": meds.today_doses(pid), "active": m["active"], "as_needed": m["as_needed"],
        "now": iso(now_local()), "demo": demo_mode()}


@router.get("/api/me/today")
def me_today():
    """Contract K shape (now_card, today, medicines, next_visit, offline_ok) plus the full doses."""
    a = _me()
    pid = int(a.patient_id)
    authz.require("patient.view", pid)
    _patient(pid)
    meds.refresh_doses(pid)
    doses = meds.today_doses(pid)
    open_ = [d for d in doses if d["status"] in ("due", "missed", "upcoming")]
    due = [d for d in open_ if d["status"] in ("due", "missed")]
    pick = (due or open_)[:1]
    if pick:
        same = [d for d in open_ if d["due_at"] == pick[0]["due_at"]]
        now_card = {"kind": "medicine", "due_at": pick[0]["due_at"], "status": pick[0]["status"],
                    "title": ", ".join(d["drug_name"] for d in same), "dose_ids": [d["id"] for d in same]}
    else:
        now_card = {"kind": "done"}
    return {"now_card": now_card,
            "today": [{"kind": "medicine", "title": d["drug_name"], "time": parse_dt(d["due_at"]).strftime("%H:%M"),
                       "status": d["status"], "icon": "pill", "dose_id": d["id"]} for d in doses],
            "medicines": meds.counts_today(pid), "next_visit": None, "offline_ok": True, "doses": doses}


@router.get("/api/me/prescription-card")
def me_prescription_card():
    """Data for the full-screen pharmacy card: hospital, doctor, registration number (display
    only), issue date, patient, each medicine, and the check token for the QR."""
    a = _me()
    pid = int(a.patient_id)
    authz.require("patient.view", pid)
    cards = meds.cards_for(pid)
    return {"cards": cards, "card": cards[0] if cards else None, "demo": demo_mode()}


@router.post("/api/me/doses/{dose}/report")
@router.post("/api/me/doses/{dose}/taken")
def me_report_dose(dose: int, request: Request):
    """The patient taps "I took it" -> the dose is REPORTED (the screen says Reported)."""
    a = _me()
    pid = int(a.patient_id)
    actor = authz.require("dose.report", pid)
    if meds.owner_of_dose(dose) != pid:
        raise HTTPException(404, f"dose {dose} not found")
    return _report(dose, pid, actor, "app", request)


# ---------------------------------------------------------------------------- the pharmacist (public)

@router.get("/api/rx-check/{token}")
def rx_check(token: str, request: Request, response: Response):
    """Public, rate limited, minimal: the hospital's copy of a prescription for a valid QR token.
    A bad token is 404 (and too many bad ones from one address are 429)."""
    ip = audit.client_ip(request) or "?"
    if not ratelimit.allow("rx_check", ip, 60, 60) or not ratelimit.peek("rx_check_bad", ip, 10, 600):
        raise HTTPException(429, "too many tries - please wait a few minutes")
    data = meds.public_check(token)
    if data is None:
        ratelimit.allow("rx_check_bad", ip, 10, 600)
        raise HTTPException(404, "this code is not valid")
    rx_id, pid, hid = data.pop("_rx_id"), data.pop("_patient_id"), data.pop("_hospital_id")
    audit.write("rx.verify", "prescription", rx_id, patient_id=pid, request=request,
                detail={"hospital_id": hid, "result": data["state"]})
    response.headers["Cache-Control"] = "no-store"
    return data
