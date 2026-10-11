"""Hospital admin: the "App branding" page's API, and the branding the apps read.

    GET    /api/admin/branding          admin of the hospital: current branding + limits
    PUT    /api/admin/branding          admin: app name, short name, accent colour
    POST   /api/admin/branding/logo     admin: upload a logo (PNG, JPEG or WebP, about 512 KB)
    DELETE /api/admin/branding/logo     admin: remove the logo
    GET    /api/me/branding             patient session: the patient's own hospital's branding
    GET    /api/me/branding/logo        patient session: that hospital's logo
    GET    /api/branding/mine           staff session (any role): their own hospital's branding
    GET    /api/branding/mine/logo      staff session: their own hospital's logo

Why two pairs of read routes: the middleware (main.py) lets only a patient session through under
/api/me/, and only a staff session through everywhere else. Both return the same JSON; only the
logo address inside it differs. There is no public logo address.
Every write is permission-checked (admin.manage, own hospital only) and audited.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, Body, File, HTTPException, Request, Response, UploadFile

from . import audit, authz, branding

log = logging.getLogger("spirobuddy.routes_admin")
router = APIRouter(tags=["branding"])

LOGO_ROUTE = {"staff": "/api/branding/mine/logo", "patient": "/api/me/branding/logo"}
LOGO_ADMIN_ROUTE = "/api/branding/mine/logo"       # the admin is a staff member


def _actor() -> authz.Actor:
    actor = authz.current_actor()
    if actor is None:
        raise HTTPException(401, "login needed")
    return actor


def _session_view(actor: authz.Actor) -> dict:
    """The branding for this session's hospital. Never errors: no branding -> the defaults."""
    try:
        return branding.view(actor.hospital_id, LOGO_ROUTE.get(actor.kind, LOGO_ROUTE["staff"]))
    except Exception as e:                       # a broken read must not break the patient app
        log.warning("branding read failed: %s", e)
        return {"display_name": "SpiroBuddy", "short_name": "SpiroBuddy",
                "accent": branding.DEFAULT_ACCENT, "accent_ink": branding.STRIP_INK_LIGHT,
                "logo_url": None, "powered_by": branding.POWERED_BY}


def _logo_response(actor: authz.Actor) -> Response:
    found = branding.logo_bytes(actor.hospital_id)
    if not found:
        raise HTTPException(404, "no logo")
    data, mime = found
    return Response(content=data, media_type=mime,
                    headers={"Cache-Control": "private, max-age=300",
                             "Content-Disposition": "inline"})


# ----------------------------------------------------------------------------- admin

@router.get("/api/admin/branding")
def admin_get():
    actor = authz.require("admin.manage")
    return branding.admin_view(actor.hospital_id, LOGO_ADMIN_ROUTE)


@router.put("/api/admin/branding")
def admin_put(request: Request, body: dict = Body(...)):
    actor = authz.require("admin.manage")
    unknown = sorted(str(k) for k in body if k not in branding.EDITABLE)
    if unknown:
        raise HTTPException(400, "These settings cannot be changed here: " + ", ".join(unknown)
                            + ". You can change the app name, the short name and the accent colour.")
    try:
        clean = branding.save(actor.hospital_id, body)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except LookupError:
        raise HTTPException(404, "hospital not found")
    audit.write("branding.update", "hospital", actor.hospital_id,
                detail={"fields": sorted(clean), **clean}, actor=actor, request=request)
    return branding.admin_view(actor.hospital_id, LOGO_ADMIN_ROUTE)


@router.post("/api/admin/branding/logo")
async def admin_logo_upload(request: Request, file: UploadFile = File(...)):
    actor = authz.require("admin.manage")
    data = await file.read(branding.MAX_LOGO_BYTES + 1)
    try:
        clean, mime = branding.process_logo(data, file.filename or "logo", file.content_type)
        branding.set_logo(actor.hospital_id, clean, mime)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except LookupError:
        raise HTTPException(404, "hospital not found")
    except Exception as e:                       # file storage down, disk full ...
        log.warning("logo upload failed: %s", type(e).__name__)
        raise HTTPException(503, "The logo could not be saved right now. Please try again.")
    audit.write("branding.logo_upload", "hospital", actor.hospital_id,
                detail={"type": mime, "bytes": len(clean)}, actor=actor, request=request)
    return branding.admin_view(actor.hospital_id, LOGO_ADMIN_ROUTE)


@router.delete("/api/admin/branding/logo")
def admin_logo_remove(request: Request):
    actor = authz.require("admin.manage")
    removed = branding.clear_logo(actor.hospital_id)
    audit.write("branding.logo_remove", "hospital", actor.hospital_id,
                detail={"removed": removed}, actor=actor, request=request)
    return branding.admin_view(actor.hospital_id, LOGO_ADMIN_ROUTE)


# ----------------------------------------------------------------------------- what the apps read

@router.get("/api/me/branding")
def patient_branding():
    return _session_view(_actor())


@router.get("/api/me/branding/logo")
def patient_logo():
    return _logo_response(_actor())


@router.get("/api/branding/mine")
def staff_branding():
    return _session_view(_actor())


@router.get("/api/branding/mine/logo")
def staff_logo():
    return _logo_response(_actor())
