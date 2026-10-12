"""Patient registration and consultation notes, using the existing v2 schema."""
from __future__ import annotations

import re
import secrets
import threading
from datetime import date

from fastapi import APIRouter, Body, HTTPException, Request

from . import audit, authz, patient_login as pl, service
from .config import iso, now_local

router = APIRouter(tags=["registration"])
_register_lock = threading.Lock()


@router.get("/api/registration/options")
def options():
    a = authz.require_staff("admin", "doctor")
    st = service.store()
    h = st.select("hospitals", [("id", "eq", a.hospital_id)], limit=1)[0]
    doctors = st.select("staff", [("hospital_id", "eq", a.hospital_id),
        ("role", "eq", "doctor"), ("status", "eq", "active")], columns="id,name,department")
    if a.role == "doctor":
        doctors = [d for d in doctors if d["id"] == a.id]
    return {"hospital": {"id": h["id"], "name": h["name"]}, "doctors": doctors,
            "departments": h.get("departments") or [], "wards": h.get("wards") or []}


def _text(body, name, limit, required=False):
    value = body.get(name, "")
    if value is None:
        value = ""
    if not isinstance(value, str) or len(value) > limit or (required and not value.strip()):
        raise HTTPException(400, f"Please enter a valid {name.replace('_', ' ')}")
    return value.strip()


@router.post("/api/patients")
def register(request: Request, body: dict = Body(...)):
    a = authz.require_staff("admin", "doctor")
    st = service.store()
    name = _text(body, "name", 120, True)
    number = pl.canonical_regno(_text(body, "registration_no", 40, True))
    if not pl.REGNO_OK.fullmatch(number):
        raise HTTPException(400, "Hospital number must contain 3 to 40 letters or numbers")
    try:
        age = int(body.get("age"))
        if isinstance(body.get("age"), bool) or str(body.get("age")) != str(age) or not 0 <= age <= 120:
            raise ValueError()
        doctor_id = int(body.get("primary_doctor_id") or a.id)
    except (TypeError, ValueError):
        raise HTTPException(400, "Enter an age from 0 to 120 and choose a doctor")
    doctors = st.select("staff", [("id", "eq", doctor_id), ("hospital_id", "eq", a.hospital_id),
        ("role", "eq", "doctor"), ("status", "eq", "active")], limit=1)
    if not doctors or (a.role == "doctor" and doctor_id != a.id):
        raise HTTPException(400, "Choose an active doctor from your hospital")
    sex, language = body.get("sex"), body.get("language", "en")
    if sex not in ("M", "F", "O") or language not in ("en", "hi", "ta", "ml"):
        raise HTTPException(400, "Choose a sex and supported language")
    phone = _text(body, "phone", 24)
    if phone and not re.fullmatch(r"\+?[0-9]{10,15}", phone):
        raise HTTPException(400, "Enter 10 to 15 phone digits, with an optional + country code")
    token = secrets.token_urlsafe(32)
    breathing = body.get("breathing_enabled", False)
    if breathing == "on":
        breathing = True  # native HTML checkbox value
    if not isinstance(breathing, bool):
        raise HTTPException(400, "Breathing assignment must be true or false")
    row = {"hospital_id": a.hospital_id, "primary_doctor_id": doctor_id, "mrn": number,
        "name": name, "age": age, "sex": sex, "language": language, "phone": phone or None,
        "surgery": _text(body, "condition", 300), "ward": _text(body, "ward", 80) or None,
        "bed": _text(body, "bed", 40) or None, "allergies_text": _text(body, "allergies_text", 500),
        "target_ml": 2000, "hold_target_s": 3, "personal_best_ml": 0,
        "programme_status": "active", "created_at": iso(now_local()),
        "routine": {"breathing_enabled": breathing},
        "app_token_hash": authz.hash_token(token), "app_token_hint": token[-4:]}
    with _register_lock:
        if pl.regno_taken(st, a.hospital_id, number):
            raise HTTPException(409, "This hospital number is already registered. Open the existing patient.")
        try:
            p = st.insert("patients", [row])[0]
        except Exception:
            raise HTTPException(409, "The patient could not be registered. Check the hospital number and try again.")
    audit.write("patient.register", "patient", p["id"], patient_id=p["id"], actor=a,
                detail={"doctor_id": doctor_id}, request=request)
    return {"patient": service.public_patient(p), "registration_no": number,
            "app_link": f"/app.html?t={token}", "login_path": f"/patient-login.html?hospital={a.hospital_id}"}


@router.get("/api/patients/{pid}/notes")
def notes(pid: int):
    authz.require("patient.view", pid)
    return service.store().select("notes", [("patient_id", "eq", pid)], order="created_at", desc=True, limit=100)


@router.post("/api/patients/{pid}/notes")
def add_note(pid: int, request: Request, body: dict = Body(...)):
    a = authz.require("patient.edit", pid)
    kind = body.get("kind", "consultation")
    if kind not in ("consultation", "note", "handover") or (kind == "consultation" and a.role != "doctor"):
        raise HTTPException(403, "Only a doctor records a consultation")
    text = _text(body, "text", 6000, True)
    p = service.get_patient_row(pid)
    row = service.store().insert("notes", [{"hospital_id": p.get("hospital_id") or a.hospital_id,
        "patient_id": pid, "kind": kind, "text": text, "author_id": a.id,
        "created_at": iso(now_local())}])[0]
    audit.write("patient.note_create", "note", row["id"], patient_id=pid, actor=a,
                detail={"kind": kind}, request=request)
    return row
