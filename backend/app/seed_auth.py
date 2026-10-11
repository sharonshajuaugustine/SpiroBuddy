"""Demo hospitals, staff logins and nurse keys (docs/REBUILD_PLAN.md §2). All fictional.

ensure(st) is safe to call at every start: it only adds what is missing. seed.reset() calls
wipe(st) and then ensure(st, reset=True), which also puts the hospitals, passwords and keys back
to the values shown on the demo login page. The seeded staff keep their fixed ids and their
sessions, so a logged-in demo admin or doctor stays logged in across a demo reset.
"""
from __future__ import annotations

import logging
import secrets
from datetime import timedelta

from . import authz
from .config import iso, now_local

log = logging.getLogger("spirobuddy.seed_auth")

DEMO_HOSPITAL_ID = 1
RIVERSIDE_HOSPITAL_ID = 2
RIVERSIDE_PATIENT_ID = 100
DEMO_JOIN_CODE = "DEMO-2026"
DEMO_NURSE_KEY = "DEMO-NURSE-KEY-0001"       # key id 5: shown on the demo page for the redeem step
# The second hospital's one patient (isolation checks). Tests switch this off for the old suite.
SEED_RIVERSIDE_PATIENT = True

HOSPITALS = [
    {"id": DEMO_HOSPITAL_ID, "name": "Demo General Hospital (fictional)",
     "city": "Kochi (fictional demo)", "address": "1 Example Road (fictional)", "phone": None,
     "timezone": "Asia/Kolkata", "languages": ["en", "hi", "ta", "ml"],
     "departments": ["General Surgery", "Chest Medicine", "Nursing"],
     "wards": ["Surgical Ward A", "Surgical Ward B", "Chest Ward"],
     "join_code": DEMO_JOIN_CODE, "join_requires_approval": True},
    {"id": RIVERSIDE_HOSPITAL_ID, "name": "Demo Riverside Clinic (fictional)",
     "city": "Kochi (fictional demo)", "address": "2 Example Road (fictional)", "phone": None,
     "timezone": "Asia/Kolkata", "languages": ["en", "ml"], "departments": ["General Surgery"],
     "wards": ["Ward 1"], "join_code": "RIVERSIDE-2026", "join_requires_approval": True},
]

# Fixed ids. The passwords are public demo passwords (shown on /login.html in DEMO_MODE).
STAFF = [
    {"id": 1, "hospital_id": 1, "role": "admin", "name": "Admin desk",
     "email": "admin@demo-general.example", "password": "demo-admin-2026",
     "department": "Administration", "specialty": None},
    {"id": 2, "hospital_id": 1, "role": "doctor", "name": "Dr. Meera Nair",
     "email": "meera.nair@demo-general.example", "password": "demo-doctor-2026",
     "department": "General Surgery", "specialty": "Surgeon"},
    {"id": 3, "hospital_id": 1, "role": "doctor", "name": "Dr. Kabir Rao",
     "email": "kabir.rao@demo-general.example", "password": "demo-doctor-2026",
     "department": "Chest Medicine", "specialty": "Chest physician"},
    {"id": 4, "hospital_id": 1, "role": "nurse", "name": "Sister Anjali",
     "email": "anjali@demo-general.example", "password": "demo-nurse-2026",
     "department": "Nursing", "specialty": "Ward nurse"},
    {"id": 5, "hospital_id": 1, "role": "nurse", "name": "Nurse Thomas Mathew",
     "email": "thomas@demo-general.example", "password": "demo-nurse-2026",
     "department": "Nursing", "specialty": "Ward nurse"},
    {"id": 50, "hospital_id": 2, "role": "admin", "name": "Riverside admin desk",
     "email": "admin@demo-riverside.example", "password": "demo-riverside-2026",
     "department": "Administration", "specialty": None},
]
SEED_STAFF_IDS = [s["id"] for s in STAFF]
DEMO_PASSWORDS = {s["email"]: s["password"] for s in STAFF}

PRIMARY_DOCTOR = {1: 2, 2: 2, 4: 2, 6: 2, 3: 3, 5: 3, 7: 3}     # patient id -> staff id

# (id, doctor, label, scope, patients, permissions, plain key or None, uses, max uses, state)
KEYS = [
    (1, 2, "Ward nurse – Sister Anjali", "all", [], list(authz.PERMS), None, 1, 2, "active"),
    (2, 3, "Chest ward – Nurse Thomas", "patients", [3, 5], ["view", "acknowledge_alerts"],
     None, 1, 2, "active"),
    (3, 2, "Night shift (revoked)", "patients", [1], ["view"], None, 0, 1, "revoked"),
    (4, 3, "Locum cover (expired)", "patients", [7], ["view"], None, 0, 1, "expired"),
    (5, 2, "Demo key – try the redeem step", "patients", [1, 2],
     ["view", "confirm_prescriptions", "manage_appointments"], DEMO_NURSE_KEY, 0, 5, "active"),
]
GRANTS = [(1, 1, 4), (2, 2, 5)]            # (grant id, key id, nurse staff id)

_hasher = None
_hashes: dict[str, str] = {}               # email -> hash of the demo password, made once


def hasher():
    global _hasher
    if _hasher is None:
        from argon2 import PasswordHasher
        _hasher = PasswordHasher()
    return _hasher


def _demo_hash(member: dict, stored: str | None = None) -> str:
    """A hash of this demo account's password. Hashing is slow, so one hash is kept per
    process and a stored hash that already matches the demo password is reused."""
    email = member["email"]
    if stored and _hashes.get(email) == stored:
        return stored
    if stored:
        try:
            hasher().verify(stored, member["password"])
            _hashes[email] = stored
            return stored
        except Exception:
            pass
    if email not in _hashes:
        _hashes[email] = hasher().hash(member["password"])
    return _hashes[email]


def _hospital_row(h: dict) -> dict:
    code = h["join_code"]
    return {"id": h["id"], "name": h["name"], "city": h["city"], "address": h["address"],
            "phone": h["phone"], "timezone": h["timezone"], "languages": h["languages"],
            "departments": h["departments"], "wards": h["wards"],
            "join_code_hash": authz.hash_join_code(code), "join_code_hint": code[-4:],
            "join_requires_approval": h["join_requires_approval"],
            "settings": dict(authz.SETTINGS_DEFAULTS)}


def _ensure_hospitals(ist, reset: bool) -> None:
    have = {h["id"] for h in ist.select("hospitals", [("id", "in", [h["id"] for h in HOSPITALS])],
                                        columns="id")}
    now = iso(now_local())
    for h in HOSPITALS:
        row = _hospital_row(h)
        if h["id"] not in have:
            ist.insert("hospitals", [{**row, "created_at": now}])
        elif reset:
            row.pop("id")
            ist.update("hospitals", [("id", "eq", h["id"])], row)


def _ensure_staff(ist, reset: bool) -> None:
    have = {s["id"]: s for s in ist.select("staff", [("id", "in", SEED_STAFF_IDS)])}
    now = iso(now_local())
    for m in STAFF:
        cur = have.get(m["id"])
        if cur is None:
            ist.insert("staff", [{
                "id": m["id"], "hospital_id": m["hospital_id"], "role": m["role"],
                "name": m["name"], "email": m["email"], "password_hash": _demo_hash(m),
                "phone": None, "department": m["department"], "specialty": m["specialty"],
                "reg_no_display": None, "status": "active", "failed_logins": 0,
                "locked_until": None, "last_login_at": None, "created_at": now}])
            continue
        values = {}
        if cur.get("status") != "active":
            values["status"] = "active"
        if cur.get("failed_logins"):
            values["failed_logins"] = 0
        if cur.get("locked_until"):
            values["locked_until"] = None
        if reset:                              # back to what the demo login page shows
            for k in ("hospital_id", "role", "name", "email", "department", "specialty"):
                if cur.get(k) != m[k]:
                    values[k] = m[k]
            h = _demo_hash(m, cur.get("password_hash"))
            if h != cur.get("password_hash"):
                values["password_hash"] = h
        if values:
            ist.update("staff", [("id", "eq", m["id"])], values)


def _key_row(spec, now) -> dict:
    kid, doctor, label, scope, pids, perms, plain, uses, max_uses, state = spec
    plain = plain or secrets.token_urlsafe(18)          # nobody ever sees these ones
    return {"id": kid, "hospital_id": DEMO_HOSPITAL_ID, "created_by": doctor, "label": label,
            "key_hash": authz.hash_token(plain), "key_hint": plain[-4:], "scope": scope,
            "patient_ids": pids, "permissions": perms,
            "expires_at": iso(now - timedelta(days=1) if state == "expired"
                              else now + timedelta(days=30)),
            "max_uses": max_uses, "uses": uses,
            "revoked_at": iso(now - timedelta(days=2)) if state == "revoked" else None,
            "created_at": iso(now - timedelta(days=5))}


def _ensure_keys(ist) -> None:
    now = now_local()
    have = {k["id"] for k in ist.select("access_keys", [("id", "in", [k[0] for k in KEYS])],
                                        columns="id")}
    rows = [_key_row(k, now) for k in KEYS if k[0] not in have]
    if rows:
        ist.insert("access_keys", rows)
    have = {g["id"] for g in ist.select("key_grants", [("id", "in", [g[0] for g in GRANTS])],
                                        columns="id")}
    rows = [{"id": gid, "hospital_id": DEMO_HOSPITAL_ID, "key_id": kid, "staff_id": sid,
             "granted_at": iso(now - timedelta(days=5)), "created_at": iso(now - timedelta(days=5))}
            for gid, kid, sid in GRANTS if gid not in have]
    if rows:
        ist.insert("key_grants", rows)


def _ensure_patients(st) -> None:
    """Demo patients 1-7 belong to hospital 1 with their primary doctor; Riverside gets one."""
    for p in st.select("patients", [("id", "in", list(PRIMARY_DOCTOR))],
                       columns="id,hospital_id,primary_doctor_id"):
        values = {}
        if p.get("hospital_id") is None:
            values["hospital_id"] = DEMO_HOSPITAL_ID
        if p.get("primary_doctor_id") is None:
            values["primary_doctor_id"] = PRIMARY_DOCTOR[p["id"]]
        if values:
            st.update("patients", [("id", "eq", p["id"])], values)
    if SEED_RIVERSIDE_PATIENT:
        ensure_riverside_patient(st)


def ensure_riverside_patient(st) -> None:
    """Patient 100 "Kiran Joseph" at the Riverside clinic, with two sessions (fictional)."""
    pid = RIVERSIDE_PATIENT_ID
    if st.select("patients", [("id", "eq", pid)], columns="id", limit=1):
        return
    now = now_local()
    st.insert("patients", [{
        "id": pid, "name": "Kiran Joseph", "age": 46, "sex": "M",
        "surgery": "Laparoscopic hernia repair",
        "surgery_date": (now - timedelta(days=3)).date().isoformat(), "language": "en",
        "target_ml": 2000, "hold_target_s": 3.0, "family_phone": None, "nurse_phone": None,
        "personal_best_ml": 1720, "created_at": iso(now - timedelta(days=3)),
        "hospital_id": RIVERSIDE_HOSPITAL_ID, "primary_doctor_id": None}])
    sessions, slots = [], []
    for days_ago, hour, best in ((1, 10, 1640.0), (1, 16, 1720.0)):
        day = (now - timedelta(days=days_ago)).replace(hour=hour, minute=5, second=0, microsecond=0)
        sessions.append({"patient_id": pid, "started_at": iso(day),
                         "slot_date": day.date().isoformat(), "slot_hour": hour,
                         "breaths_count": 10, "best_ml": best, "avg_score": 78.0, "source": "demo"})
    for s in st.insert("sessions", sessions):
        slots.append({"patient_id": pid, "slot_date": s["slot_date"], "slot_hour": s["slot_hour"],
                      "status": "done", "session_id": s["id"]})
    st.upsert("slots", slots)
    # no automatic call ladder for this patient: it only exists to prove hospitals are separate
    st.upsert("care_settings", [{"patient_id": pid, "config": {"auto": False},
                                 "updated_at": iso(now)}])


def remove_riverside_patient(st) -> None:
    pid = RIVERSIDE_PATIENT_ID
    for table, col in (("breaths", "patient_id"), ("slots", "patient_id"),
                       ("sessions", "patient_id"), ("care_settings", "patient_id"),
                       ("patients", "id")):
        st.delete(table, [(col, "eq", pid)])


def ensure(st, reset: bool = False) -> None:
    """Add the demo hospitals, staff, keys and patient links that are missing. With reset=True
    also put names, passwords, join codes and settings back to the demo values."""
    ist = authz.ident(st)
    _ensure_hospitals(ist, reset)
    _ensure_staff(ist, reset)
    _ensure_keys(ist)
    if authz.v2_ok(st):
        _ensure_patients(st)


def wipe(st) -> None:
    """Part of a demo reset: remove staff made during the demo (signups, redeemed nurses) with
    their sessions and grants, and every key (ensure() seeds the demo keys again). Hospitals,
    the seeded staff and their sessions stay, so demo users stay logged in."""
    ist = authz.ident(st)
    extra = [s["id"] for s in ist.select("staff", columns="id") if s["id"] not in SEED_STAFF_IDS]
    if extra:
        ist.delete("auth_sessions", [("staff_id", "in", extra)])
        ist.delete("care_team", [("staff_id", "in", extra)])
        ist.delete("staff", [("id", "in", extra)])
    ist.delete("key_grants", [("id", "gte", 0)])
    ist.delete("access_keys", [("id", "gte", 0)])
    # patient-app sessions of patients that a reset removes (ids outside the seeded ones)
    keep = list(PRIMARY_DOCTOR) + [RIVERSIDE_PATIENT_ID]
    gone = [s["id"] for s in ist.select("auth_sessions", [("kind", "eq", "patient")],
                                        columns="id,patient_id") if s.get("patient_id") not in keep]
    if gone:
        ist.delete("auth_sessions", [("id", "in", gone)])
