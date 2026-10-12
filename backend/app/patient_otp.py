"""Simulated patient OTP delivery. Challenges persist in app_settings, never as plaintext.

This adapter deliberately sends no SMS. A sample code is returned only in DEMO_MODE.
Hospital + MRN identifies the patient. Locks serialize requests in this single-process demo;
distributed SMS deployment needs transactional challenge consumption and shared rate limits.
"""
from __future__ import annotations

import secrets
import threading
from datetime import timedelta

from fastapi import HTTPException

from . import authz, patient_login as pl, service
from .config import demo_mode, iso, now_local, parse_dt
from .seed_auth import hasher

LOCK = threading.RLock()
GENERIC = "If the hospital has your phone number, a code is on its way. No code? Please ask the hospital desk."
WRONG = "That code could not be checked. Request a new code or ask the hospital desk."


def now():
    return now_local()


def identity(body):
    try:
        hid = int(body.get("hospital_id") or (1 if demo_mode() else 0))
    except (TypeError, ValueError):
        raise HTTPException(400, "Choose your hospital")
    raw = body.get("registration_no")
    number = pl.canonical_regno(raw) if isinstance(raw, str) else ""
    if hid <= 0 or not pl.REGNO_OK.fullmatch(number):
        raise HTTPException(400, "Choose your hospital and enter its registration number")
    return hid, number


def _key(hid, number):
    canonical = pl.regno_candidates(number)[-1]
    return f"otp:{hid}:{canonical}"


def _read(key):
    rows = service.store().select("app_settings", [("key", "eq", key)], limit=1)
    return (rows[0].get("value") or {}) if rows else {}


def _save(key, hid, value):
    stamp = iso(now())
    service.store().upsert("app_settings", [{"key": key, "hospital_id": hid,
        "value": value, "created_at": stamp, "updated_at": stamp}])


def request_code(hid, number):
    challenge = secrets.token_urlsafe(24)
    answer = {"ok": True, "message": GENERIC, "challenge_id": challenge,
              "delivery": "simulated", "expires_in": 600}
    with LOCK:
        key, stamp = _key(hid, number), now()
        state = _read(key)
        if state.get("locked_until") and parse_dt(state["locked_until"]) > stamp:
            return answer
        if state.get("issued_at") and parse_dt(state["issued_at"]) + timedelta(seconds=60) > stamp:
            if not state.get("consumed") and state.get("challenge_id") and state.get("expires_at") \
                    and parse_dt(state["expires_at"]) > stamp:
                # A rapid resend must not replace the browser's still-usable challenge.
                # Only the hash is stored: never recover or return the earlier code.
                answer["challenge_id"] = state["challenge_id"]
                answer["expires_in"] = max(1, int((parse_dt(state["expires_at"]) - stamp).total_seconds()))
            return answer
        window = parse_dt(state["window_at"]) if state.get("window_at") else stamp
        count = int(state.get("requests") or 0) if window + timedelta(hours=1) > stamp else 0
        if count >= 5:
            return answer
        rows = service.store().select("patients", [("hospital_id", "eq", hid),
            ("mrn", "in", pl.regno_candidates(number))], limit=2)
        patient = rows[0] if len(rows) == 1 else None
        if not patient or not patient.get("phone") or patient.get("programme_status") == "deceased":
            return answer
        code = f"{secrets.randbelow(1000000):06d}"
        value = {"patient_id": patient["id"], "challenge_id": challenge,
            "code_hash": hasher().hash(code), "expires_at": iso(stamp + timedelta(minutes=10)),
            "issued_at": iso(stamp), "attempts": 0, "consumed": False,
            "window_at": iso(window if count else stamp), "requests": count + 1}
        _save(key, hid, value)
        if demo_mode():
            answer["demo_code"] = code
        return answer


def verify_code(hid, number, challenge, code):
    if not isinstance(code, str) or not code.isascii() or len(code) != 6 or not code.isdigit():
        raise HTTPException(400, "Enter the six digits of your code")
    with LOCK:
        key, stamp = _key(hid, number), now()
        state = _read(key)
        if state.get("locked_until") and parse_dt(state["locked_until"]) > stamp:
            raise HTTPException(429, "Too many wrong codes. Please wait 15 minutes.")
        if not state or state.get("consumed") or state.get("challenge_id") != challenge \
                or parse_dt(state["expires_at"]) <= stamp:
            raise HTTPException(401, WRONG)
        try:
            matched = hasher().verify(state["code_hash"], code)
        except Exception:
            matched = False
        if not matched:
            state["attempts"] = int(state.get("attempts") or 0) + 1
            if state["attempts"] >= 5:
                state["locked_until"] = iso(stamp + timedelta(minutes=15))
            _save(key, hid, state)
            raise HTTPException(429 if state["attempts"] >= 5 else 401, WRONG)
        p = service.get_patient_row(int(state["patient_id"]))
        if not p or p.get("hospital_id") != hid or p.get("programme_status") == "deceased" \
                or pl.canonical_regno(p.get("mrn")) not in pl.regno_candidates(number):
            raise HTTPException(401, WRONG)
        state["consumed"] = True
        state.pop("code_hash", None)
        _save(key, hid, state)
        return p
