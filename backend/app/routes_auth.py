"""CONTRACT E – auth (docs/ARCHITECTURE.md §14): staff login, doctor signup with the hospital's
join code, nurse keys (create, redeem, revoke), password change and the patient-app session.

Demo-grade login: argon2 password hashes, server-side sessions in auth_sessions (only the
sha256 of the cookie token is stored), HttpOnly cookies. Every login, failure, logout, signup,
redeem, key change and password change goes to the audit log – never with a secret in it.
"""
from __future__ import annotations

import logging
import re
import secrets
from datetime import timedelta

from fastapi import APIRouter, Body, HTTPException, Request, Response

from . import audit, authz, ratelimit, service
from .config import demo_mode, iso, now_local, parse_dt
from .seed_auth import hasher

log = logging.getLogger("spirobuddy.auth")
router = APIRouter(tags=["auth"])

LOGIN_TRIES = 10                    # per 15 minutes per IP + email, then a 15-minute lockout
LOCK_SECONDS = 15 * 60
MIN_PASSWORD = 10
EMAIL_RE = re.compile(r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$")
_DUMMY_HASH = None                  # verified when the email is unknown, so timing tells nothing


def _st():
    return authz.ident()


def _text(body: dict, key: str, max_len: int = 200) -> str:
    v = body.get(key)
    if v is None:
        return ""
    if not isinstance(v, str):
        raise HTTPException(400, f"{key} must be text")
    return v.strip()[:max_len]


def _password(body: dict, key: str) -> str:
    v = body.get(key)
    if not isinstance(v, str) or not v:
        raise HTTPException(400, f"{key} is required")
    if len(v) > 200:
        raise HTTPException(400, f"{key} is too long")
    return v


def _email(body: dict) -> str:
    e = _text(body, "email").lower()
    if not EMAIL_RE.match(e):
        raise HTTPException(400, "please enter a valid email address")
    return e


def _verify(stored: str | None, password: str) -> bool:
    global _DUMMY_HASH
    if not stored:
        if _DUMMY_HASH is None:
            _DUMMY_HASH = hasher().hash(secrets.token_urlsafe(16))
        stored, ok_possible = _DUMMY_HASH, False
    else:
        ok_possible = True
    try:
        return bool(hasher().verify(stored, password)) and ok_possible
    except Exception:
        return False


def _is_https(request: Request) -> bool:
    proto = (request.headers.get("x-forwarded-proto") or "").split(",")[0].strip().lower()
    return request.url.scheme == "https" or proto == "https"


def _start_session(request: Request, response: Response, kind: str, hospital_id,
                   staff_id=None, patient_id=None) -> None:
    """New session row + cookie. Only the sha256 of the token is stored."""
    token = secrets.token_urlsafe(32)
    life = timedelta(hours=authz.STAFF_SESSION_HOURS) if kind == "staff" \
        else timedelta(days=authz.PATIENT_SESSION_DAYS)
    now = now_local()
    _st().insert("auth_sessions", [{
        "hospital_id": hospital_id, "kind": kind, "staff_id": staff_id, "patient_id": patient_id,
        "token_hash": authz.hash_token(token), "expires_at": iso(now + life),
        "ip": audit.client_ip(request), "user_agent": (request.headers.get("user-agent") or "")[:200],
        "revoked_at": None, "last_seen_at": iso(now), "created_at": iso(now)}])
    response.set_cookie(authz.STAFF_COOKIE if kind == "staff" else authz.PATIENT_COOKIE, token,
                        max_age=int(life.total_seconds()), httponly=True, samesite="lax",
                        secure=_is_https(request), path="/")


def _end_session(request: Request, cookie: str, kind: str) -> dict | None:
    s = authz.session_row(request.cookies.get(cookie), kind)
    if s:
        _st().update("auth_sessions", [("id", "eq", s["id"])], {"revoked_at": iso(now_local())})
    return s


def _hospital(hospital_id) -> dict:
    rows = _st().select("hospitals", [("id", "eq", hospital_id)], columns="id,name", limit=1)
    return {"id": rows[0]["id"], "name": rows[0]["name"]} if rows else {"id": hospital_id, "name": ""}


def _me(actor: authz.Actor | None) -> dict:
    if actor is None:
        return {"authenticated": False}
    if actor.kind == "patient":
        p = service.get_patient_row(actor.id) or {}
        return {"authenticated": True, "kind": "patient", "patient_id": actor.id,
                "name": p.get("name") or actor.name, "language": p.get("language") or "en"}
    rows = _st().select("staff", [("id", "eq", actor.id)], columns="department,specialty", limit=1)
    perms = [p for p in authz.PERMS if actor.role != "nurse" or p in authz.nurse_permissions(actor)]
    out = {"authenticated": True, "kind": "staff", "id": actor.id, "name": actor.name,
           "email": actor.email, "role": actor.role, "hospital": _hospital(actor.hospital_id),
           "department": rows[0].get("department") if rows else None,
           "specialty": rows[0].get("specialty") if rows else None,
           "permissions_summary": perms, "demo_mode": demo_mode()}
    if actor.role == "nurse":
        out["grants"] = actor.grants
        out["patients_count"] = len(authz.visible_patient_ids(actor))
    return out


# ----------------------------------------------------------------------------- staff login

@router.post("/api/auth/login")
def login(request: Request, response: Response, body: dict = Body(...)):
    email = _text(body, "email").lower()
    password = body.get("password")
    if not email or not isinstance(password, str) or not password:
        raise HTTPException(400, "email and password are required")
    ip = audit.client_ip(request) or "?"
    bucket_key = f"{ip}|{email}"
    st = _st()
    rows = st.select("staff", [("email", "eq", email)], limit=1) if EMAIL_RE.match(email) else []
    member = rows[0] if rows else None
    now = now_local()
    locked = bool(member and member.get("locked_until") and parse_dt(member["locked_until"]) > now)
    if locked or not ratelimit.peek("login", bucket_key, LOGIN_TRIES, LOCK_SECONDS):
        if member and not locked:
            st.update("staff", [("id", "eq", member["id"])],
                      {"locked_until": iso(now + timedelta(seconds=LOCK_SECONDS))})
        audit.write("auth.login_failed", "staff", member["id"] if member else None,
                    detail={"email": email, "reason": "locked",
                            "hospital_id": member.get("hospital_id") if member else None},
                    request=request)
        raise HTTPException(429, "too many tries – please wait 15 minutes and try again")
    if not _verify(member.get("password_hash") if member else None, password[:200]):
        ratelimit.allow("login", bucket_key, LOGIN_TRIES, LOCK_SECONDS)
        if member:
            fails = int(member.get("failed_logins") or 0) + 1
            values = {"failed_logins": fails}
            if fails >= LOGIN_TRIES:
                values["locked_until"] = iso(now + timedelta(seconds=LOCK_SECONDS))
            st.update("staff", [("id", "eq", member["id"])], values)
        audit.write("auth.login_failed", "staff", member["id"] if member else None,
                    detail={"email": email, "reason": "wrong email or password",
                            "hospital_id": member.get("hospital_id") if member else None},
                    request=request)
        raise HTTPException(401, "wrong email or password")
    if member.get("status") != "active":
        reason = ("your account is waiting for the hospital admin's approval"
                  if member.get("status") == "pending"
                  else "this account is switched off – please ask your hospital admin")
        audit.write("auth.login_failed", "staff", member["id"],
                    detail={"email": email, "reason": member.get("status"),
                            "hospital_id": member.get("hospital_id")}, request=request)
        raise HTTPException(403, reason)
    ratelimit.reset("login", bucket_key)
    st.update("staff", [("id", "eq", member["id"])],
              {"failed_logins": 0, "locked_until": None, "last_login_at": iso(now)})
    _start_session(request, response, "staff", member.get("hospital_id"), staff_id=member["id"])
    actor = authz.staff_actor(member)
    audit.write("auth.login", "staff", member["id"], actor=actor, request=request)
    return {"ok": True, "me": _me(actor)}


@router.post("/api/auth/logout")
def logout(request: Request, response: Response):
    s = _end_session(request, authz.STAFF_COOKIE, "staff")
    p = _end_session(request, authz.PATIENT_COOKIE, "patient")
    if s or p:
        audit.write("auth.logout", "staff" if s else "patient",
                    (s or {}).get("staff_id") or (p or {}).get("patient_id"),
                    detail={"hospital_id": (s or p).get("hospital_id")}, request=request)
    response.delete_cookie(authz.STAFF_COOKIE, path="/")
    response.delete_cookie(authz.PATIENT_COOKIE, path="/")
    return {"ok": True}


@router.get("/api/auth/me")
def me():
    return _me(authz.current_actor())


@router.post("/api/auth/password")
def change_password(request: Request, body: dict = Body(...)):
    actor = authz.require_staff()
    old, new = _password(body, "old_password"), _password(body, "new_password")
    if len(new) < MIN_PASSWORD:
        raise HTTPException(400, f"the new password needs at least {MIN_PASSWORD} characters")
    st = _st()
    rows = st.select("staff", [("id", "eq", actor.id)], limit=1)
    if not rows or not _verify(rows[0].get("password_hash"), old):
        audit.write("auth.password_change_failed", "staff", actor.id, request=request)
        raise HTTPException(403, "the old password is not right")
    st.update("staff", [("id", "eq", actor.id)], {"password_hash": hasher().hash(new)})
    # other devices are logged out; this one stays
    mine = authz.hash_token(request.cookies.get(authz.STAFF_COOKIE) or "")
    st.update("auth_sessions", [("staff_id", "eq", actor.id), ("token_hash", "neq", mine)],
              {"revoked_at": iso(now_local())})
    audit.write("auth.password_change", "staff", actor.id, request=request)
    return {"ok": True}


# ----------------------------------------------------------------------------- doctor signup

@router.post("/api/auth/signup")
def signup(request: Request, body: dict = Body(...)):
    ip = audit.client_ip(request) or "?"
    if not ratelimit.allow("signup", ip, 20, LOCK_SECONDS):
        raise HTTPException(429, "too many tries – please wait 15 minutes and try again")
    code = _text(body, "join_code", 64)
    name = _text(body, "name", 80)
    if not code or not name:
        raise HTTPException(400, "join_code and name are required")
    email = _email(body)
    password = _password(body, "password")
    if len(password) < MIN_PASSWORD:
        raise HTTPException(400, f"the password needs at least {MIN_PASSWORD} characters")
    st = _st()
    hospitals = st.select("hospitals", [("join_code_hash", "eq", authz.hash_join_code(code))], limit=1)
    if not hospitals:
        audit.write("auth.signup_failed", "staff", detail={"email": email, "reason": "join code"},
                    request=request)
        raise HTTPException(400, "that join code is not right – please ask your hospital admin")
    hospital = hospitals[0]
    if st.select("staff", [("email", "eq", email)], columns="id", limit=1):
        raise HTTPException(400, "this email already has an account – please log in")
    status = "active" if demo_mode() or not hospital.get("join_requires_approval") else "pending"
    now = iso(now_local())
    row = st.insert("staff", [{
        "hospital_id": hospital["id"], "role": "doctor", "name": name, "email": email,
        "password_hash": hasher().hash(password), "phone": None,
        "department": _text(body, "department", 80) or None,
        "specialty": _text(body, "specialty", 80) or None,
        "reg_no_display": _text(body, "reg_no_display", 40) or None, "status": status,
        "failed_logins": 0, "locked_until": None, "last_login_at": None, "created_at": now}])[0]
    audit.write("auth.signup", "staff", row["id"],
                detail={"email": email, "status": status, "hospital_id": hospital["id"]},
                request=request)
    return {"ok": True, "status": status}


# ----------------------------------------------------------------------------- nurse keys

def _key_status(k: dict) -> str:
    if k.get("revoked_at"):
        return "revoked"
    if k.get("expires_at") and parse_dt(k["expires_at"]) <= now_local():
        return "expired"
    if k.get("max_uses") is not None and int(k.get("uses") or 0) >= int(k["max_uses"]):
        return "used_up"
    return "active"


def _key_out(k: dict, names: dict[int, str], grants: list[dict]) -> dict:
    return {"id": k["id"], "label": k.get("label"),
            "doctor": {"id": k.get("created_by"), "name": names.get(k.get("created_by"))},
            "scope": k.get("scope"), "patient_ids": k.get("patient_ids") or [],
            "permissions": k.get("permissions") or [], "expires_at": k.get("expires_at"),
            "max_uses": k.get("max_uses"), "uses": int(k.get("uses") or 0),
            "revoked_at": k.get("revoked_at"), "status": _key_status(k),
            "key_hint": k.get("key_hint"), "created_at": k.get("created_at"),
            "grants": [{"staff_id": g["staff_id"], "name": names.get(g["staff_id"])}
                       for g in grants if g["key_id"] == k["id"]]}


def _keys_out(keys: list[dict]) -> list[dict]:
    if not keys:
        return []
    st = _st()
    grants = st.select("key_grants", [("key_id", "in", [k["id"] for k in keys])])
    ids = {k.get("created_by") for k in keys} | {g["staff_id"] for g in grants}
    names = {s["id"]: s["name"] for s in st.select(
        "staff", [("id", "in", [i for i in ids if i is not None])], columns="id,name")}
    return [_key_out(k, names, grants) for k in keys]


@router.get("/api/keys")
def list_keys():
    actor = authz.require_staff("admin", "doctor")
    f = [("hospital_id", "eq", actor.hospital_id)]
    if actor.role == "doctor":
        f.append(("created_by", "eq", actor.id))
    return _keys_out(_st().select("access_keys", f, order="id", desc=True))


@router.post("/api/keys")
def create_key(request: Request, body: dict = Body(...)):
    actor = authz.require_staff("doctor")              # the admin can revoke, not create
    label = _text(body, "label", 80) or "Nurse key"
    scope = body.get("scope") or "patients"
    if scope not in ("all", "patients"):
        raise HTTPException(400, "scope must be all or patients")
    perms = body.get("permissions")
    if not isinstance(perms, list) or not perms or any(p not in authz.PERMS for p in perms):
        raise HTTPException(400, "permissions must be a list from: " + ", ".join(authz.PERMS))
    perms = [p for p in authz.PERMS if p in perms or p == "view"]     # a key always lets you view
    patient_ids: list[int] = []
    if scope == "patients":
        raw = body.get("patient_ids")
        if not isinstance(raw, list) or not raw or len(raw) > 500:
            raise HTTPException(400, "choose at least one patient for this key")
        mine = authz.visible_patient_ids(actor)
        for v in raw:
            if isinstance(v, bool) or not isinstance(v, int) or v not in mine:
                raise HTTPException(400, "a key can only cover your own patients")
            if v not in patient_ids:
                patient_ids.append(v)
    days = body.get("expires_days", 30)
    uses = body.get("max_uses", 1)
    for what, v, hi in (("expires_days", days, 365), ("max_uses", uses, 50)):
        if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= hi:
            raise HTTPException(400, f"{what} must be a whole number from 1 to {hi}")
    plain = secrets.token_urlsafe(18)
    now = now_local()
    row = _st().insert("access_keys", [{
        "hospital_id": actor.hospital_id, "created_by": actor.id, "label": label,
        "key_hash": authz.hash_token(plain), "key_hint": plain[-4:], "scope": scope,
        "patient_ids": patient_ids, "permissions": perms,
        "expires_at": iso(now + timedelta(days=days)), "max_uses": uses, "uses": 0,
        "revoked_at": None, "created_at": iso(now)}])[0]
    audit.write("key.create", "access_key", row["id"],
                detail={"label": label, "scope": scope, "patient_ids": patient_ids,
                        "permissions": perms, "expires_days": days, "max_uses": uses},
                request=request)
    return {**_keys_out([row])[0], "key": plain}       # the plain key is shown once, never again


@router.post("/api/keys/{key_id}/revoke")
def revoke_key(key_id: int, request: Request):
    actor = authz.require_staff("admin", "doctor")
    st = _st()
    rows = st.select("access_keys", [("id", "eq", key_id), ("hospital_id", "eq", actor.hospital_id)],
                     limit=1)
    if not rows or (actor.role == "doctor" and rows[0].get("created_by") != actor.id):
        raise HTTPException(404, f"access key {key_id} not found")
    k = rows[0]
    if not k.get("revoked_at"):
        k["revoked_at"] = iso(now_local())
        st.update("access_keys", [("id", "eq", key_id)], {"revoked_at": k["revoked_at"]})
        audit.write("key.revoke", "access_key", key_id, detail={"label": k.get("label")},
                    request=request)
    return _keys_out([k])[0]


@router.post("/api/auth/redeem")
def redeem(request: Request, response: Response, body: dict = Body(...)):
    ip = audit.client_ip(request) or "?"
    if not ratelimit.allow("redeem", ip, 20, LOCK_SECONDS):
        raise HTTPException(429, "too many tries – please wait 15 minutes and try again")
    plain = _text(body, "key", 100)
    if not plain:
        raise HTTPException(400, "key is required")
    st = _st()
    rows = st.select("access_keys", [("key_hash", "eq", authz.hash_token(plain))], limit=1)
    status = _key_status(rows[0]) if rows else "unknown"
    if status != "active":
        reason = {"unknown": "this key is not right – please check it with the doctor",
                  "revoked": "this key was switched off – please ask the doctor for a new one",
                  "expired": "this key has expired – please ask the doctor for a new one",
                  "used_up": "this key has already been used – please ask the doctor for a new one"}
        audit.write("key.redeem_failed", "access_key", rows[0]["id"] if rows else None,
                    detail={"reason": status,
                            "hospital_id": rows[0].get("hospital_id") if rows else None},
                    request=request)
        raise HTTPException(400, reason[status])
    key = rows[0]
    actor = authz.current_actor()
    new_login = False
    if actor is not None and actor.kind == "staff" and actor.role == "nurse" \
            and actor.hospital_id == key.get("hospital_id"):
        member = st.select("staff", [("id", "eq", actor.id)], limit=1)[0]   # add to this nurse
    else:
        name = _text(body, "name", 80)
        email = _email(body)
        password = _password(body, "password")
        existing = st.select("staff", [("email", "eq", email)], limit=1)
        if existing:
            member = existing[0]
            if member.get("role") != "nurse" or member.get("hospital_id") != key.get("hospital_id") \
                    or member.get("status") != "active" \
                    or not _verify(member.get("password_hash"), password):
                raise HTTPException(400, "this email already has an account – log in first, "
                                         "then use the key")
        else:
            if not name:
                raise HTTPException(400, "name is required")
            if len(password) < MIN_PASSWORD:
                raise HTTPException(400, f"the password needs at least {MIN_PASSWORD} characters")
            now = iso(now_local())
            member = st.insert("staff", [{
                "hospital_id": key.get("hospital_id"), "role": "nurse", "name": name,
                "email": email, "password_hash": hasher().hash(password), "phone": None,
                "department": "Nursing", "specialty": None, "reg_no_display": None,
                "status": "active", "failed_logins": 0, "locked_until": None,
                "last_login_at": now, "created_at": now}])[0]
        new_login = True
    if not st.select("key_grants", [("key_id", "eq", key["id"]), ("staff_id", "eq", member["id"])],
                     columns="id", limit=1):
        now = iso(now_local())
        st.insert("key_grants", [{"hospital_id": key.get("hospital_id"), "key_id": key["id"],
                                  "staff_id": member["id"], "granted_at": now, "created_at": now}])
        st.update("access_keys", [("id", "eq", key["id"])], {"uses": int(key.get("uses") or 0) + 1})
    if new_login:
        _start_session(request, response, "staff", member.get("hospital_id"), staff_id=member["id"])
    actor = authz.staff_actor(member)
    audit.write("key.redeem", "access_key", key["id"], actor=actor,
                detail={"label": key.get("label"), "staff_id": member["id"]}, request=request)
    return {"ok": True, "me": _me(actor)}


# ----------------------------------------------------------------------------- patient app

@router.post("/api/me/session")
def patient_session(request: Request, response: Response, body: dict = Body(...)):
    """A personal link token (or, in DEMO_MODE only, a patient id) -> the sb_patient cookie."""
    ip = audit.client_ip(request) or "?"
    token = body.get("token")
    if token is not None:
        if not isinstance(token, str) or not token.strip() or len(token) > 200:
            raise HTTPException(400, "this link is not right – please ask the hospital for a new one")
        if not ratelimit.allow("patient_session", ip, 30, LOCK_SECONDS):
            raise HTTPException(429, "too many tries – please wait 15 minutes and try again")
        data = service.store()
        rows = data.select("patients", [("app_token_hash", "eq", authz.hash_token(token))],
                           limit=1) if authz.v2_ok(data) else []
        if not rows:
            raise HTTPException(400, "this link is not right – please ask the hospital for a new one")
        p = rows[0]
    else:
        pid = body.get("patient_id")
        if pid is None:
            raise HTTPException(400, "token is required")
        if not demo_mode():
            raise HTTPException(403, "a personal link is needed to open the patient app")
        if isinstance(pid, (bool, list, dict, float)) or not str(pid).strip().lstrip("-").isdigit():
            raise HTTPException(400, "patient_id must be a whole number")
        p = service.get_patient_row(int(pid)) if abs(int(pid)) < 2 ** 62 else None
        if not p:
            raise HTTPException(404, f"patient {pid} not found")
    cur = authz.session_row(request.cookies.get(authz.PATIENT_COOKIE), "patient")
    if not cur or cur.get("patient_id") != p["id"]:          # reuse a live session for this patient
        _start_session(request, response, "patient", p.get("hospital_id") or authz.LEGACY_HOSPITAL_ID,
                       patient_id=p["id"])
        audit.write("auth.patient_session", "patient", p["id"], patient_id=p["id"],
                    actor=authz.patient_actor(p), detail={"by": "token" if token else "demo id"},
                    request=request)
    return {"ok": True, "patient_id": p["id"], "name": p.get("name"),
            "language": p.get("language") or "en"}
