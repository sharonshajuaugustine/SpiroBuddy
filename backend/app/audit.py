"""The audit log: who did what, to which patient, when (docs/REBUILD_PLAN.md §3.5).

write() never raises – a broken log must not break the request. Never put a token, password,
key or document content in `detail` (anything that looks like one is blanked here as a second
line of defence). The hash chain (prev_hash, hash) is a later step.
"""
from __future__ import annotations

import logging
import uuid

from . import authz
from .config import iso, now_local, parse_dt

log = logging.getLogger("spirobuddy.audit")

_SECRET_WORDS = ("password", "token", "secret", "cookie", "join_code", "key_hash")
_SECRET_KEYS = {"key", "code"}


def client_ip(request) -> str | None:
    """Authoritative socket address, after any server-configured trusted proxy handling.

    Client-supplied forwarding headers must not create a new rate-limit identity.
    Deployment proxy trust belongs in the ASGI server, not in application header parsing.
    """
    if request is None:
        return None
    try:
        return request.client.host if request.client else None
    except Exception:
        return None


def _clean(value, depth: int = 0):
    """Copy of `detail` that is safe to store: secrets blanked, long text cut."""
    if depth > 4:
        return None
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            name = str(k).lower()
            if name in _SECRET_KEYS or any(w in name for w in _SECRET_WORDS):
                out[str(k)] = "[hidden]"
            else:
                out[str(k)] = _clean(v, depth + 1)
        return out
    if isinstance(value, (list, tuple, set)):
        return [_clean(v, depth + 1) for v in list(value)[:100]]
    if isinstance(value, str):
        return value[:500]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return str(value)[:200]


def write(action: str, resource_type: str, resource_id=None, patient_id=None,
          detail: dict | None = None, actor: authz.Actor | None = None, request=None) -> None:
    """Add one audit row. The actor defaults to the current one. Never raises."""
    try:
        actor = actor if actor is not None else authz.current_actor()
        detail = _clean(dict(detail or {}))
        hospital_id = actor.hospital_id if actor is not None else detail.get("hospital_id")
        if actor is not None and patient_id is None:
            detail.setdefault("hospital_id", actor.hospital_id)
        request_id = getattr(getattr(request, "state", None), "request_id", None) or uuid.uuid4().hex
        now = iso(now_local())
        authz.ident().insert("audit_events", [{
            "hospital_id": hospital_id, "at": now,
            "actor_type": actor.kind if actor is not None else "anonymous",
            "actor_id": actor.id if actor is not None else None,
            "actor_role": actor.role if actor is not None else None,
            "action": str(action), "resource_type": str(resource_type),
            "resource_id": None if resource_id is None else str(resource_id)[:80],
            "patient_id": patient_id if isinstance(patient_id, int) else None,
            "detail": detail, "ip": client_ip(request), "request_id": request_id,
            "created_at": now}])
    except Exception as e:          # the log must never take the request down with it
        log.warning("audit write failed (%s %s): %s", action, resource_type, e)


def list_events(hospital_id, filters: dict | None = None, limit: int = 200) -> list[dict]:
    """Newest first. filters: patient_id, actor_id, action, from, to (ISO times),
    patient_ids (a set: only these patients – for doctors and nurses)."""
    filters = filters or {}
    f = [("hospital_id", "eq", hospital_id)]
    for col in ("patient_id", "actor_id", "action"):
        if filters.get(col) not in (None, ""):
            f.append((col, "eq", filters[col]))
    rows = authz.ident().select("audit_events", f, order="id", desc=True,
                                limit=max(1, min(int(limit or 200), 5000)) * 3)
    lo = parse_dt(filters["from"]) if filters.get("from") else None
    hi = parse_dt(filters["to"]) if filters.get("to") else None
    only = filters.get("patient_ids")
    out = []
    for r in rows:
        if only is not None and r.get("patient_id") not in only:
            continue
        if lo or hi:
            try:
                at = parse_dt(r.get("at") or r.get("created_at"))
            except (TypeError, ValueError):
                continue
            if (lo and at < lo) or (hi and at > hi):
                continue
        out.append(r)
        if len(out) >= limit:
            break
    return out
