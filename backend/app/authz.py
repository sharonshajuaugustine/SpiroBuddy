"""Who is asking, and what may they do (docs/REBUILD_PLAN.md §3.3, spec §6).

The one place for permissions. The middleware in main.py reads the session cookie once per
request, turns it into an Actor and keeps it in a contextvar. Handlers call
require(action, pid). Answers: not logged in -> 401, a patient you can't see -> 404 (so nobody
learns the patient exists), visible but not allowed -> 403.

Only sha256 hashes of session tokens, nurse keys and join codes are stored (hash_token).
"""
from __future__ import annotations

import contextvars
import copy
import hashlib
import threading
from dataclasses import dataclass, field

from fastapi import HTTPException

from . import service
from .config import demo_mode, now_local, parse_dt

STAFF_COOKIE = "sb_staff"            # staff session, 12 hours
PATIENT_COOKIE = "sb_patient"        # patient app session, 30 days
STAFF_SESSION_HOURS = 12
PATIENT_SESSION_DAYS = 30
# Patients created before 2.0 have no hospital_id: they belong to the first (demo) hospital.
LEGACY_HOSPITAL_ID = 1


@dataclass
class Actor:
    kind: str              # "staff" | "patient"
    id: int                # staff id, or patient id for a patient
    role: str              # "admin" | "doctor" | "nurse" | "patient"
    hospital_id: int
    name: str
    email: str | None = None
    patient_id: int | None = None          # patients only
    # nurses: [{key_id, doctor_id, scope, patient_ids, permissions, expires_at}] (live keys only)
    grants: list[dict] = field(default_factory=list)


PERMS = ("view", "update_care_plan", "confirm_prescriptions", "manage_appointments",
         "upload_documents", "acknowledge_alerts")          # nurse key permissions

ACTIONS = ("patient.view", "patient.edit", "careplan.edit", "programme.change", "rx.create",
           "rx.approve", "rx.upload", "dose.report", "appt.manage", "appt.request", "doc.upload",
           "doc.view", "doc.view_family", "alerts.ack", "comms.use", "keys.create", "keys.revoke",
           "admin.manage", "governance.read", "demo.control", "device.manage")

# The permission matrix (spec §6). Admins don't prescribe or report doses; only doctors make keys.
_ADMIN = {"patient.view", "patient.edit", "careplan.edit", "programme.change", "appt.manage",
          "appt.request", "doc.upload", "doc.view", "doc.view_family", "alerts.ack", "comms.use",
          "keys.revoke", "admin.manage", "governance.read", "demo.control", "device.manage"}
_DOCTOR = {"patient.view", "patient.edit", "careplan.edit", "programme.change", "rx.create",
           "rx.approve", "rx.upload", "dose.report", "appt.manage", "appt.request", "doc.upload",
           "doc.view", "doc.view_family", "alerts.ack", "comms.use", "keys.create", "keys.revoke",
           "governance.read", "demo.control", "device.manage"}
_PATIENT = {"patient.view", "dose.report", "appt.request", "doc.upload", "doc.view", "rx.upload"}
# nurse key permission -> actions it opens (rx.approve also needs the hospital setting)
_NURSE = {
    "view": {"patient.view", "dose.report", "doc.view", "doc.view_family", "governance.read"},
    "update_care_plan": {"careplan.edit", "patient.edit", "comms.use"},
    "confirm_prescriptions": {"rx.approve"},
    "manage_appointments": {"appt.manage", "appt.request"},
    "upload_documents": {"doc.upload", "doc.view", "doc.view_family"},
    "acknowledge_alerts": {"alerts.ack", "comms.use"},
}

# Hospital settings and their defaults (spec §8.3). Stored in hospitals.settings (json).
SETTINGS_DEFAULTS = {
    "grace_minutes": 60,
    "quiet_hours": "21:00-07:00",
    "routine": {"wake": "07:00", "breakfast": "08:00", "lunch": "13:00", "dinner": "20:00",
                "bed": "22:00"},
    "rx_confirm_by": "doctor_or_permitted_nurse",     # or "doctor_only"
    "ai_enabled": True,
    "ai_handwriting": False,
    "reminder_channels": ["app"],
    "alert_thresholds": {},
}

_current: contextvars.ContextVar[Actor | None] = contextvars.ContextVar("sb_actor", default=None)
# A browser can hold a staff cookie and a patient cookie at once (the demo: doctor in one tab,
# patient app in another). The second one is kept here; require() falls back to it.
_alt: contextvars.ContextVar[Actor | None] = contextvars.ContextVar("sb_actor_alt", default=None)


# ----------------------------------------------------------------------------- stores

_local_store = None
_local_lock = threading.Lock()


def v2_ok(st=None) -> bool:
    """False only when the store is a Supabase project that lacks the 2.0 tables (schema_v2.sql
    not run). make_store() normally falls back to SQLite in that case, so this is a safety net."""
    st = st if st is not None else service.store()
    if getattr(st, "name", "") != "supabase":
        return True
    ok = vars(st).get("_sb_v2_ok")
    if ok is None:
        try:
            st.select("auth_sessions", limit=1, columns="id")
            ok = True
        except RuntimeError as e:          # "missing table" is an answer; an outage is not
            if not any(s in str(e) for s in ("does not exist", "schema cache", " 404 ")):
                raise
            ok = False
        st._sb_v2_ok = ok
    return ok


def ident(st=None):
    """The store that holds logins: hospitals, staff, auth_sessions, access_keys, key_grants,
    care_team and audit_events. This is the active store; if that one has no 2.0 tables, the
    local SQLite file is used so login still works."""
    global _local_store
    st = st if st is not None else service.store()
    if v2_ok(st):
        return st
    with _local_lock:
        if _local_store is None:
            from .store import SqliteStore
            _local_store = SqliteStore()
    return _local_store


def hash_token(token: str) -> str:
    """sha256 of a session token, patient link token or nurse key. Only this is stored."""
    return hashlib.sha256(str(token).strip().encode("utf-8")).hexdigest()


def hash_join_code(code: str) -> str:
    """Join codes ignore case, spaces and dashes: "demo 2026" == "DEMO-2026"."""
    return hash_token("".join(ch for ch in str(code).upper() if ch.isalnum()))


def _as_int(v) -> int | None:
    try:
        if isinstance(v, bool):
            return None
        return int(v)
    except (TypeError, ValueError):
        return None


def _past(value) -> bool:
    """True when an ISO time is now or earlier. A broken value counts as past (fail closed)."""
    try:
        return parse_dt(value) <= now_local()
    except (TypeError, ValueError):
        return True


# ----------------------------------------------------------------------------- who is asking

def current_actor() -> Actor | None:
    return _current.get()


def set_actor(actor: Actor | None, alt: Actor | None = None):
    """Used by the middleware. Returns the tokens for reset_actor()."""
    return _current.set(actor), _alt.set(alt)


def reset_actor(tokens) -> None:
    _current.reset(tokens[0])
    _alt.reset(tokens[1])


def session_row(token: str | None, kind: str) -> dict | None:
    """The live auth_sessions row for a cookie value, or None (unknown, revoked, expired)."""
    if not token or len(token) > 200:
        return None
    rows = ident().select("auth_sessions", [("token_hash", "eq", hash_token(token))], limit=1)
    if not rows:
        return None
    s = rows[0]
    if (s.get("kind") or "staff") != kind or s.get("revoked_at") or _past(s.get("expires_at")):
        return None
    return s


def live_grants(staff_id: int, hospital_id: int | None = None) -> list[dict]:
    """A nurse's key grants, read fresh at every request: revoked and expired keys drop out."""
    st = ident()
    grants = st.select("key_grants", [("staff_id", "eq", int(staff_id))])
    if not grants:
        return []
    keys = {k["id"]: k for k in st.select("access_keys",
                                          [("id", "in", [g["key_id"] for g in grants])])}
    out, seen = [], set()
    for g in grants:
        k = keys.get(g["key_id"])
        if not k or k["id"] in seen or k.get("revoked_at"):
            continue
        if k.get("expires_at") and _past(k["expires_at"]):
            continue
        if hospital_id is not None and k.get("hospital_id") not in (None, hospital_id):
            continue
        seen.add(k["id"])
        ids = k.get("patient_ids") if isinstance(k.get("patient_ids"), list) else []
        perms = k.get("permissions") if isinstance(k.get("permissions"), list) else []
        out.append({"key_id": k["id"], "doctor_id": k.get("created_by"),
                    "scope": k.get("scope") or "patients",
                    "patient_ids": [i for i in (_as_int(x) for x in ids) if i is not None],
                    "permissions": [p for p in perms if p in PERMS],
                    "expires_at": k.get("expires_at")})
    return out


def staff_actor(member: dict) -> Actor | None:
    """Actor for a staff row; None unless the account is active."""
    if not member or member.get("status") != "active":
        return None
    actor = Actor("staff", int(member["id"]), member["role"], int(member.get("hospital_id") or 0),
                  member.get("name") or "", member.get("email"))
    if actor.role == "nurse":
        actor.grants = live_grants(actor.id, actor.hospital_id)
    return actor


def patient_actor(p: dict) -> Actor | None:
    if not p:
        return None
    pid = int(p["id"])
    return Actor("patient", pid, "patient", int(p.get("hospital_id") or LEGACY_HOSPITAL_ID),
                 p.get("name") or "", None, pid)


def resolve_actors(request) -> tuple[Actor | None, Actor | None]:
    """(staff, patient) from the two cookies. Each is None when its cookie is missing, expired
    or revoked, the staff account is pending or disabled, or the patient is gone."""
    staff = patient = None
    s = session_row(request.cookies.get(STAFF_COOKIE), "staff")
    if s and s.get("staff_id") is not None:
        rows = ident().select("staff", [("id", "eq", s["staff_id"])], limit=1)
        staff = staff_actor(rows[0]) if rows else None
    s = session_row(request.cookies.get(PATIENT_COOKIE), "patient")
    if s and s.get("patient_id") is not None:
        patient = patient_actor(service.get_patient_row(int(s["patient_id"])))
    return staff, patient


def resolve_actor(request) -> Actor | None:
    """Cookie -> Actor. The staff session wins when both cookies are there, except under
    /api/me/ (the patient app), where only the patient session counts."""
    staff, patient = resolve_actors(request)
    if request.url.path.startswith("/api/me/"):
        return patient
    return staff or patient


# ----------------------------------------------------------------------------- what they may see

def _patient_index(actor: Actor) -> list[dict]:
    """[{id, hospital_id, primary_doctor_id}] for every patient; read once per request."""
    rows = vars(actor).get("_patients")
    if rows is None:
        st = service.store()
        cols = "id,hospital_id,primary_doctor_id" if v2_ok(st) else "id"
        rows = st.select("patients", columns=cols)
        actor._patients = rows
    return rows


def _doctor_patient_ids(actor: Actor, doctor_id) -> set[int]:
    """A doctor's patients inside the actor's hospital: primary doctor, or in the care team."""
    if doctor_id is None:
        return set()
    cache = vars(actor).setdefault("_by_doctor", {})
    if doctor_id not in cache:
        in_hospital = {int(p["id"]): p for p in _patient_index(actor)
                       if int(p.get("hospital_id") or LEGACY_HOSPITAL_ID) == actor.hospital_id}
        ids = {pid for pid, p in in_hospital.items() if p.get("primary_doctor_id") == doctor_id}
        ids |= {int(r["patient_id"]) for r in ident().select(
            "care_team", [("staff_id", "eq", doctor_id)], columns="patient_id")} & set(in_hospital)
        cache[doctor_id] = ids
    return cache[doctor_id]


def _grant_ids(actor: Actor, grant: dict) -> set[int]:
    mine = _doctor_patient_ids(actor, grant.get("doctor_id"))
    return set(mine) if grant.get("scope") == "all" else mine & set(grant.get("patient_ids") or [])


def visible_patient_ids(actor: Actor | None) -> set[int]:
    """admin: every patient in the hospital; doctor: own patients (primary doctor or care
    team); nurse: union of the live key scopes; patient: only themselves."""
    if actor is None:
        return set()
    ids = vars(actor).get("_visible")
    if ids is None:
        if actor.kind == "patient":
            ids = {int(actor.patient_id)} if actor.patient_id is not None else set()
        elif actor.role == "admin":
            ids = {int(p["id"]) for p in _patient_index(actor)
                   if int(p.get("hospital_id") or LEGACY_HOSPITAL_ID) == actor.hospital_id}
        elif actor.role == "doctor":
            ids = set(_doctor_patient_ids(actor, actor.id))
        elif actor.role == "nurse":
            ids = set()
            for g in actor.grants:
                ids |= _grant_ids(actor, g)
        else:
            ids = set()
        actor._visible = ids
    return ids


def _nurse_actions(actor: Actor, perms: set[str]) -> set[str]:
    acts: set[str] = set()
    for p in perms:
        acts |= _NURSE.get(p, set())
    if "rx.approve" in acts and \
            hospital_settings(actor.hospital_id).get("rx_confirm_by") != "doctor_or_permitted_nurse":
        acts.discard("rx.approve")
    return acts


def _role_actions(actor: Actor) -> set[str]:
    """Actions this actor has at all (no particular patient)."""
    if actor.kind == "patient":
        return set(_PATIENT)
    if actor.role == "admin":
        return set(_ADMIN)
    if actor.role == "doctor":
        return set(_DOCTOR)
    if actor.role == "nurse":
        return _nurse_actions(actor, {p for g in actor.grants for p in g.get("permissions") or []})
    return set()


def patient_permissions(actor: Actor | None, pid) -> set[str]:
    """Actions this actor may do on this patient (empty when they can't see the patient)."""
    pid = _as_int(pid)
    if actor is None or pid is None or pid not in visible_patient_ids(actor):
        return set()
    if actor.kind == "staff" and actor.role == "nurse":
        perms = {p for g in actor.grants if pid in _grant_ids(actor, g)
                 for p in g.get("permissions") or []}
        return _nurse_actions(actor, perms)
    return _role_actions(actor)


def nurse_permissions(actor: Actor | None, pid=None) -> set[str]:
    """Nurse key permission names (PERMS): for one patient, or the union over all live keys."""
    if actor is None or actor.role != "nurse":
        return set()
    pid = _as_int(pid)
    return {p for g in actor.grants if pid is None or pid in _grant_ids(actor, g)
            for p in g.get("permissions") or []}


def can(actor: Actor | None, action: str, pid: int | None = None) -> bool:
    if actor is None:
        return False
    if action == "demo.control" and not demo_mode():
        return False
    if pid is not None:
        return action in patient_permissions(actor, pid)
    return action in _role_actions(actor)


def require(action: str, pid: int | None = None) -> Actor:
    """The current actor, if they may do `action` (on patient `pid`). Otherwise raises:
    no login -> 401; patient not visible (other hospital, out of scope, missing) -> 404;
    visible but not allowed -> 403."""
    actor, alt = _current.get(), _alt.get()
    for a in (actor, alt):
        if a is not None and can(a, action, pid):
            return a
    a = actor or alt
    if a is None:
        raise HTTPException(401, "login needed")
    if pid is not None and (_as_int(pid) is None or _as_int(pid) not in visible_patient_ids(a)):
        raise HTTPException(404, f"patient {pid} not found")
    raise HTTPException(403, "you don't have permission to do this")


def require_staff(*roles: str) -> Actor:
    """The logged-in staff member (optionally one of `roles`). 401 without a staff session,
    403 for a patient session or the wrong role."""
    actor = _current.get()
    if actor is None:
        raise HTTPException(401, "login needed")
    if actor.kind != "staff" or (roles and actor.role not in roles):
        raise HTTPException(403, "you don't have permission to do this")
    return actor


def hospital_settings(hospital_id) -> dict:
    """The hospital's settings, with the defaults (spec §8.3) filled in."""
    out = copy.deepcopy(SETTINGS_DEFAULTS)
    rows = ident().select("hospitals", [("id", "eq", hospital_id)], columns="settings", limit=1) \
        if _as_int(hospital_id) is not None else []
    stored = rows[0].get("settings") if rows else None
    if isinstance(stored, dict):
        for k, v in stored.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k] = {**out[k], **v}
            elif v is not None:
                out[k] = v
    return out


def reminders_allowed(patient_row: dict | None) -> bool:
    """No reminders for a patient whose programme is paused, stopped or who has died."""
    status = (patient_row or {}).get("programme_status") or "active"
    return status not in ("paused", "stopped", "deceased")


def alerts_allowed(patient_row: dict | None) -> bool:
    """A paused programme also stops alerts (so do stopped and deceased)."""
    return reminders_allowed(patient_row)


# ----------------------------------------------------------------------------- path parameters

# Path parameter name -> (what it is, table, column that names the owner). The middleware looks
# every one of these up before the handler runs (docs/REBUILD_PLAN.md §3.4 item 11), so every
# route must name its path parameters from this list.
RESOURCE_PARAMS: dict[str, tuple[str, str, str]] = {
    "pid": ("patient", "patients", "id"),
    "rx": ("prescription", "prescriptions", "patient_id"),
    "item": ("prescription line", "prescription_items", "prescription_id"),   # -> prescriptions
    "dose": ("dose", "dose_events", "patient_id"),
    "appt": ("appointment", "appointments", "patient_id"),
    "doc": ("document", "documents", "patient_id"),
    "note_id": ("note", "notes", "patient_id"),
    "aid": ("alert", "alerts", "patient_id"),
    "rid": ("escalation", "escalations", "patient_id"),
    "cid": ("call", "calls", "patient_id"),            # under /api/comms/cheers/ it is a cheer
    "gid": ("guardian", "guardians", "patient_id"),
    "staff_id": ("staff member", "staff", "hospital_id"),
    "doctor_id": ("staff member", "staff", "hospital_id"),
    "key_id": ("access key", "access_keys", "hospital_id"),
    "device_id": ("device", "devices", "hospital_id"),
}
_IDENT_TABLES = {"staff", "access_keys"}
_MAX_ID = 2 ** 62          # larger numbers can't be a row id (and would overflow SQLite)


def resource_label(name: str, path: str = "") -> str:
    if name == "cid" and "/cheers/" in path:
        return "cheer"
    return RESOURCE_PARAMS[name][0]


def resolve_param_owner(name: str, value, path: str = "") -> tuple[str, int | None] | None:
    """Who owns the thing a path parameter points at: ("patient", patient_id) or
    ("hospital", hospital_id). None when there is no such row. Raises ValueError when the value
    isn't a whole number (the route's own validation then answers 422).
    For `pid` no row is read: visible_patient_ids() already says whether it exists."""
    _, table, col = RESOURCE_PARAMS[name]
    rid = int(str(value))                       # ValueError for "abc", "1.5", "1e3"
    if abs(rid) > _MAX_ID:
        return None
    if name == "pid":
        return "patient", rid
    if name == "cid" and "/cheers/" in path:
        table = "cheers"
    st = ident() if table in _IDENT_TABLES else service.store()
    rows = st.select(table, [("id", "eq", rid)], columns=col, limit=1)
    if not rows:
        return None
    owner = _as_int(rows[0].get(col))
    if name == "item":                          # prescription line -> its prescription's patient
        rows = st.select("prescriptions", [("id", "eq", owner)], columns="patient_id", limit=1) \
            if owner is not None else []
        if not rows:
            return None
        owner = _as_int(rows[0].get("patient_id"))
    return ("hospital" if col == "hospital_id" else "patient"), owner


def owner_visible(actor: Actor | None, owner: tuple[str, int | None] | None) -> bool:
    """May this actor know that the resource exists?"""
    if actor is None or owner is None:
        return False
    kind, oid = owner
    if kind == "hospital":
        return oid is not None and oid == actor.hospital_id
    if oid is None:        # an old row with no patient (e.g. a message from an unknown number)
        return actor.kind == "staff" and actor.hospital_id == LEGACY_HOSPITAL_ID
    return oid in visible_patient_ids(actor)
