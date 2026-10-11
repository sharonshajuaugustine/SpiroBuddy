"""SpiroBuddy API (contract D in docs/ARCHITECTURE.md) + static hosting of web/.

Run from the repo root:  uvicorn backend.app.main:app --port 8000
"""
from __future__ import annotations

import logging
import math
import re
import uuid
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import audit, authz, llm, models_ml, rules, seed, seed_auth, service, whatsapp
from .config import (FIRST_SLOT, LABELS, LAST_SLOT, WEB_DIR, allow_training, demo_mode, env,
                     env_flag, iso, now_local, show_api_docs)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("spirobuddy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    st = service.init_store()
    log.info("Data store: %s (%s)", st.name, service.store_note())
    try:
        if demo_mode() and seed.needs_seed(st):
            log.info("Seeding demo data...")
            seed.reset(st)
        elif st.count("patients") == 0:
            seed.seed(st)
    except Exception as e:
        log.error("Seeding failed: %s", e)
    try:        # 2.0 logins: the demo hospitals, staff and keys (only what is missing)
        if demo_mode() or not authz.ident(st).select("staff", limit=1, columns="id"):
            seed_auth.ensure(st)
    except Exception as e:
        log.error("Login seeding failed: %s", e)
    if demo_mode():
        try:
            from . import seed_patient_login
            from .meds import seed_meds
            seed_patient_login.ensure(st, reset_pin=False)
            seed_meds.seed(st)
        except Exception as e:
            log.warning("Sample patient setup skipped: %s", e)
    try:        # the private "documents" bucket (backend/app/storage.py, comes with Phase 1)
        from . import storage
        storage.ensure_bucket()
    except ImportError:
        pass
    except Exception as e:
        log.warning("storage bucket check failed: %s", e)
    models_ml.load()
    yield


# The API docs stay hidden unless SHOW_API_DOCS=1 (spec §12).
_DOCS = show_api_docs()
app = FastAPI(title="SpiroBuddy API", version="0.2.0", lifespan=lifespan,
              docs_url="/docs" if _DOCS else None, redoc_url="/redoc" if _DOCS else None,
              openapi_url="/openapi.json" if _DOCS else None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])


@app.middleware("http")
async def _revalidate_static(request, call_next):
    """Browsers must re-check web/ files (cheap 304 via ETag), so a fix is never hidden by cache."""
    resp = await call_next(request)
    if not request.url.path.startswith("/api"):
        resp.headers.setdefault("Cache-Control", "no-cache")
    return resp


# ----------------------------------------------------------------------------- who may call what
# One place for the access policy (docs/REBUILD_PLAN.md §3.4). Permissions live in authz.py.

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
WEBHOOK_PREFIXES = ("/api/comms/webhooks/", "/api/comms/twilio/", "/api/comms/exotel/")
PUBLIC_PATHS = {"/api/health", "/api/features", "/api/auth/login", "/api/auth/signup",
                "/api/auth/redeem", "/api/auth/me", "/api/auth/logout", "/api/me/session",
                "/api/me/login", "/api/me/login-demo",          # patient login: number + PIN
                "/api/me/otp/hospitals", "/api/me/otp/request", "/api/me/otp/verify",
                "/api/voice/status", "/api/voice/cues"}
PUBLIC_PREFIXES = ("/api/impact", "/api/twin/sim", "/api/voice/clip/", "/api/voice/audio/",
                   "/api/comms/card/", "/api/comms/guardian/",
                   "/api/rx-check/") + WEBHOOK_PREFIXES      # rx-check: the pharmacist's QR page
# A patient session (or staff) is enough for these; everything else needs staff.
PATIENT_PATHS = {"/api/sessions", "/api/classify", "/api/voice/tts", "/api/voice/stt",
                 "/api/voice/translate", "/api/voice/detect"}
PATIENT_PREFIXES = ("/api/voice/prefs/", "/api/voice/summary-audio/", "/api/comms/cheers/",
                    "/api/comms/demo/red-flag/")
_PATIENT_CHART = re.compile(r"^/api/patients/[^/]+$")
DEMO_PREFIXES = ("/api/demo/", "/api/comms/demo/")
DEMO_HOSPITAL_ONLY = {"/api/demo/reset", "/api/demo/prepare-recording"}   # these wipe demo data
TRAINING_PATHS = {"/api/collect", "/api/train"}
# Pages of this site that this site itself shows inside a frame (the 3D twin and showroom).
FRAMEABLE_PREFIXES = ("/twin.html", "/showcase/")


def _deny(status: int, message: str) -> JSONResponse:
    return JSONResponse({"error": message, "status": status}, status_code=status)


def _is_public(path: str) -> bool:
    return path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES)


def _patient_allowed(path: str, method: str) -> bool:
    return (path in PATIENT_PATHS or path.startswith(PATIENT_PREFIXES)
            or (method == "POST" and path.startswith("/api/live/"))
            or (method in ("GET", "HEAD") and _PATIENT_CHART.match(path) is not None))


_route_table: tuple[int, list] = (-1, [])


def _flatten_routes(routes, out: list) -> list:
    """Every route as (path regex, methods), in order. FastAPI keeps an included router as one
    nested entry (routes are no longer copied into app.routes), so those are opened up here."""
    for r in routes:
        nested = getattr(r, "effective_candidates", None)
        if callable(nested):
            _flatten_routes(nested(), out)
        elif getattr(r, "path_regex", None) is not None:
            out.append((r.path_regex, getattr(r, "methods", None)))
    return out


def api_route_table() -> list:
    global _route_table
    n = len(app.router.routes)
    if _route_table[0] != n:
        _route_table = (n, _flatten_routes(app.router.routes, []))
    return _route_table[1]


def _path_params(path: str, method: str) -> dict:
    """Path parameters of the route this request will reach: the first route that matches the
    path and method and names a checked parameter ({} if there is none)."""
    for regex, methods in api_route_table():
        if methods is not None and method not in methods:
            continue
        m = regex.match(path)
        if m:
            params = m.groupdict()
            if any(k in authz.RESOURCE_PARAMS for k in params):
                return params
    return {}


def _resource_error(params: dict, actor: authz.Actor, path: str) -> JSONResponse | None:
    """404 if a path parameter points at something this actor can't see (other hospital, out of
    scope, or not there at all). Runs before the handler and before body validation."""
    for name, value in params.items():
        if name not in authz.RESOURCE_PARAMS:
            continue
        try:
            owner = authz.resolve_param_owner(name, value, path)
        except ValueError:
            continue                    # not a whole number: the route itself answers 422
        if not authz.owner_visible(actor, owner):
            return _deny(404, f"{authz.resource_label(name, path)} {value} not found")
    return None


def _decide(request: Request):
    """-> (actor, second actor, error response or None). Blocking (reads the store)."""
    path, method = request.url.path, request.method
    public = _is_public(path)
    try:
        staff, patient = authz.resolve_actors(request)
    except Exception:
        if not public:
            raise
        staff = patient = None          # a public page must not fail because the store is down
    if path.startswith("/api/me/"):     # the patient app: only the patient session counts
        actor, alt = patient, None
    else:
        actor, alt = (staff or patient), (patient if staff else None)
    # CSRF: a browser on another site can't add this header to a cross-site form post
    if method not in SAFE_METHODS and not path.startswith(WEBHOOK_PREFIXES) \
            and request.headers.get("x-sb") != "1":
        return actor, alt, _deny(403, "missing X-SB header")
    if public:
        return actor, alt, None
    if actor is None:
        return None, None, _deny(401, "login needed")
    patient_ok = path.startswith("/api/me/") or _patient_allowed(path, method)
    if not patient_ok:                  # staff only
        if staff is None:
            return None, None, _deny(401, "login needed")
        actor, alt = staff, None
    if path.startswith(DEMO_PREFIXES):
        if not demo_mode():
            return actor, alt, _deny(403, "demo endpoints are disabled (set DEMO_MODE=1)")
        if actor.kind == "staff" and actor.role not in ("admin", "doctor"):
            return actor, alt, _deny(403, "demo controls are for the hospital admin and doctors")
        if path in DEMO_HOSPITAL_ONLY and actor.hospital_id != seed_auth.DEMO_HOSPITAL_ID:
            return actor, alt, _deny(403, "only the demo hospital can reset the demo data")
    if path in TRAINING_PATHS and not (actor.role == "admin" and allow_training()):
        return actor, alt, _deny(403, "training is switched off (needs an admin and ALLOW_TRAINING=1)")
    params = _path_params(path, method)
    err = _resource_error(params, actor, path)
    if err is not None and alt is not None and _resource_error(params, alt, path) is None:
        actor, alt, err = alt, None, None      # the patient cookie owns it, the staff one doesn't
    return actor, alt, err


def _harden(resp, path: str):
    """Security headers on every response (spec §12)."""
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("X-Frame-Options",
                            "SAMEORIGIN" if path.startswith(FRAMEABLE_PREFIXES) else "DENY")
    return resp


@app.middleware("http")
async def _gate(request: Request, call_next):
    """Every /api/ request: find out who is asking, apply the policy, then run the handler."""
    path = request.url.path
    if not path.startswith("/api/") or request.method == "OPTIONS":
        return _harden(await call_next(request), path)
    request.state.request_id = uuid.uuid4().hex
    try:
        actor, alt, err = await run_in_threadpool(_decide, request)
    except OverflowError:
        return _harden(_deny(400, "number out of range"), path)
    except Exception as exc:            # same JSON shape as server_error below
        log.exception("Unhandled error on %s", path)
        return _harden(_deny(500, f"{type(exc).__name__}: {exc}"), path)
    if err is not None:
        return _harden(err, path)
    tokens = authz.set_actor(actor, alt)
    try:
        resp = await call_next(request)
    finally:
        authz.reset_actor(tokens)
    # the chart view is audited here, once per request (staff only; a patient reads their own)
    if request.method == "GET" and resp.status_code == 200 and actor is not None \
            and actor.kind == "staff" and _PATIENT_CHART.match(path):
        pid = path.rsplit("/", 1)[-1]
        if pid.isdigit():
            await run_in_threadpool(audit.write, "patient.view", "patient", int(pid), int(pid),
                                    None, actor, request)
    return _harden(resp, path)


# ----------------------------------------------------------------------------- errors as JSON

@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    return JSONResponse({"error": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
                         "status": exc.status_code}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse({"error": "invalid request", "status": 422,
                         "details": jsonable_errors(exc)}, status_code=422)


@app.exception_handler(OverflowError)
async def number_out_of_range(request: Request, exc: OverflowError):
    """An absurdly large number in the URL or body (id, timestamp...) is a bad request, not a crash."""
    return JSONResponse({"error": "number out of range", "status": 400}, status_code=400)


@app.exception_handler(Exception)
async def server_error(request: Request, exc: Exception):
    log.exception("Unhandled error on %s", request.url.path)
    return JSONResponse({"error": f"{type(exc).__name__}: {exc}", "status": 500},
                        status_code=500)


def jsonable_errors(exc: RequestValidationError) -> list:
    return [{"loc": list(e.get("loc", [])), "msg": e.get("msg")} for e in exc.errors()]


def _patient_or_404(pid: int) -> dict:
    p = service.get_patient_row(pid)
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    return p


def _require_demo():
    if not demo_mode():
        raise HTTPException(403, "demo endpoints are disabled (set DEMO_MODE=1)")


def _int_or_400(value, what: str) -> int:
    """Whole number from a JSON body, or a clean 400 (never a 500) for text, lists, objects."""
    try:
        if isinstance(value, (bool, list, dict)):
            raise TypeError(what)
        return int(value)
    except (TypeError, ValueError):
        raise HTTPException(400, f"{what} must be a whole number")


def _maybe_autopilot():
    if demo_mode() and env_flag("DEMO_AUTOPILOT", "1"):
        try:
            seed.autopilot(service.store())
        except Exception as e:
            log.warning("autopilot failed: %s", e)


# ----------------------------------------------------------------------------- core API

@app.get("/api/health")
def health():
    return {"ok": True, "model_loaded": models_ml.model_loaded(),
            "llm_enabled": llm.llm_enabled(), "whatsapp_enabled": whatsapp.whatsapp_enabled(),
            "data_backend": service.store().name, "demo_mode": demo_mode(),
            "data_note": service.store_note(), "v2_missing": service.v2_missing(),
            "tz": env("TZ_NAME", "Asia/Kolkata"), "now": iso(now_local())}


@app.get("/api/patients")
def patients():
    _maybe_autopilot()
    return service.list_patients()


@app.get("/api/patients/{pid}")
def patient(pid: int):
    _maybe_autopilot()
    d = service.patient_detail(pid)
    if d is None:
        raise HTTPException(404, f"patient {pid} not found")
    return d


@app.put("/api/patients/{pid}")
def update_patient(pid: int, request: Request, body: dict = Body(...)):
    # targets = the care plan; language and family phone = patient details (spec §6)
    plan = any(k in body for k in ("target_ml", "hold_target_s"))
    actor = authz.require("careplan.edit" if plan else "patient.edit", pid)
    _patient_or_404(pid)
    values = {}
    for k in ("target_ml", "hold_target_s"):          # text, lists, NaN -> 400, not a crash
        v = body.get(k)
        try:
            if v is not None and (isinstance(v, (bool, list, dict)) or not math.isfinite(float(v))):
                raise ValueError(k)
        except ValueError:
            raise HTTPException(400, f"{k} must be a number")
    if body.get("target_ml") is not None:
        t = int(float(body["target_ml"]))
        if not 250 <= t <= 5000:
            raise HTTPException(400, "target_ml must be between 250 and 5000")
        values["target_ml"] = t
    if body.get("hold_target_s") is not None:
        h = float(body["hold_target_s"])
        if not 0.5 <= h <= 10:
            raise HTTPException(400, "hold_target_s must be between 0.5 and 10")
        values["hold_target_s"] = h
    if body.get("language") is not None:
        if body["language"] not in ("en", "hi", "ta"):
            raise HTTPException(400, "language must be en, hi or ta")
        values["language"] = body["language"]
    if "family_phone" in body:
        values["family_phone"] = (str(body["family_phone"]).strip() or None) \
            if body["family_phone"] is not None else None
    if values:
        service.store().update("patients", [("id", "eq", pid)], values)
        audit.write("patient.update", "patient", pid, pid, {"fields": sorted(values)},
                    actor=actor, request=request)
    return service.patient_detail(pid)


@app.get("/api/patients/{pid}/sessions")
def sessions(pid: int, limit: int = Query(20, ge=1, le=200)):
    _patient_or_404(pid)
    return service.list_sessions(pid, limit)


@app.post("/api/classify")
def classify(features: dict = Body(...)):
    try:
        return models_ml.classify(features)
    except (TypeError, ValueError) as e:
        raise HTTPException(400, f"bad features: {e}")


@app.post("/api/sessions")
def post_session(body: dict = Body(...)):
    pid = body.get("patient_id")
    if pid is None:
        raise HTTPException(400, "patient_id is required")
    pid = _int_or_400(pid, "patient_id")
    authz.require("patient.view", pid)      # a patient posts their own sessions; staff: visible only
    p = _patient_or_404(pid)
    if not (p.get("routine") or {}).get("breathing_enabled", True):
        raise HTTPException(403, "Breathing exercise has not been assigned to this patient")
    breaths = body.get("breaths") or []
    if not isinstance(breaths, list) or not all(
            isinstance(b, dict) and isinstance(b.get("features") or {}, dict) for b in breaths):
        raise HTTPException(400, "breaths must be a list of {t, features, label, score} objects")
    try:
        source = "demo" if body.get("source") == "demo" and demo_mode() else "app"
        # A browser-supplied 'device' string is not authenticated sensor evidence.
        res = service.record_session(p, body.get("started_at"), breaths,
                                     source=source)
    except (TypeError, ValueError) as e:
        raise HTTPException(400, f"bad session data: {e}")
    res.pop("breaths", None)
    return res


@app.post("/api/collect")
def collect(body: dict = Body(...)):
    label = body.get("label")
    if label not in LABELS:
        raise HTTPException(400, f"label must be one of {LABELS}")
    if not isinstance(body.get("features") or {}, dict) or not isinstance(body.get("samples") or [], list):
        raise HTTPException(400, "features must be an object and samples a list")
    try:
        counts = service.save_labelled(str(body.get("person") or "anon"), label,
                                       body.get("samples") or [], body.get("features") or {})
    except (TypeError, ValueError) as e:
        raise HTTPException(400, f"bad features: {e}")
    return {"ok": True, "count_by_label": counts}


@app.post("/api/train")
def train():
    if service.store().name == "supabase":     # local disk may have been wiped (Render restart)
        try:
            service.export_labelled_csv()
        except Exception as e:
            log.warning("could not export labelled breaths from Supabase: %s", e)
    res = models_ml.train()
    if not res.get("ok") and res.get("error"):
        raise HTTPException(503, res["error"])
    return res


@app.get("/api/model")
def model():
    m = models_ml.metrics()
    out = dict(m) if m else {"note": "no model trained yet (run python ml/train.py)"}
    out["model_loaded"] = models_ml.model_loaded()
    out["source"] = "model" if models_ml.model_loaded() else "rules"
    if not models_ml.model_loaded() and models_ml.load_error():
        out["load_error"] = models_ml.load_error()
    return out


@app.post("/api/summary/{pid}")
def summary(pid: int, body: dict | None = Body(None)):
    authz.require("patient.view", pid)
    d = service.patient_detail(pid)
    if d is None:
        raise HTTPException(404, f"patient {pid} not found")
    lang = (body or {}).get("language") or d.get("language") or "en"
    if not isinstance(lang, str):
        raise HTTPException(400, "language must be text, e.g. en, hi, ta or ml")
    return llm.summarize(service.summary_stats(d), lang)


def _send(p: dict, kind: str, to_role: str, text: str) -> dict:
    number = whatsapp.resolve_number(p, to_role)
    res = whatsapp.send(number, text)
    service.log_message(p, kind, to_role, number, text, res["sent"], res["dry_run"])
    out = {"sent": res["sent"], "dry_run": res["dry_run"], "text": text, "to_role": to_role}
    if res.get("error"):
        out["error"] = res["error"]
    return out


@app.post("/api/whatsapp/{pid}")
def send_whatsapp(pid: int, body: dict | None = Body(None)):
    authz.require("comms.use", pid)
    body = body or {}
    kind = body.get("kind") or "summary"
    to_role = body.get("to") or ("nurse" if kind == "missed" else "family")
    if kind not in ("summary", "missed") or to_role not in ("family", "nurse"):
        raise HTTPException(400, "kind must be summary|missed and to must be family|nurse")
    d = service.patient_detail(pid)
    if d is None:
        raise HTTPException(404, f"patient {pid} not found")
    # Through the comms sender: consent/STOP check, AI disclosure in the recipient's language,
    # footer, shared ≥3 s throttle (QA Review 1, Q-01). whatsapp.send stays the transport.
    from .comms import messages as comms_messages
    guardian, lang, number, blocked = comms_messages.care_update_recipient(d, to_role)
    if kind == "summary":
        # before 8 am nothing is due yet: add yesterday's numbers instead of "0 of 0" (Q-29)
        s = llm.summarize(llm.add_recent(service.summary_stats(d), d), lang)
        # The disclosure line already names SpiroBuddy (Q-29): no "SpiroBuddy - Name:" prefix.
        # The nurse gets the full name so she knows which patient it is.
        text = s["text"] if to_role == "family" else f"{d['name']}: {s['text']}"
    else:
        missed = [s["hour"] for s in d["today"] if s["status"] == "missed"][-2:]
        text = whatsapp.missed_text(d, missed, lang)        # en/hi/ta/ml; anything else -> English
    return comms_messages.send_care_update(d, kind, to_role, text, lang, guardian=guardian,
                                           stored_number=number, blocked_reason=blocked)


@app.get("/api/messages")
def messages(limit: int = Query(50, ge=1, le=500)):
    return service.list_messages(limit)


# ----------------------------------------------------------------------------- demo

QUALITY_MIX = {"good": 0.1, "mixed": 0.4, "poor": 0.7}   # share of faulty breaths


@app.post("/api/demo/simulate/{pid}")
def demo_simulate(pid: int, body: dict | None = Body(None)):
    _require_demo()
    authz.require("demo.control", pid)
    import numpy as np
    p = _patient_or_404(pid)
    body = body or {}
    quality = body.get("quality") or "good"
    if not isinstance(quality, str) or quality not in QUALITY_MIX:
        raise HTTPException(400, "quality must be good, mixed or poor")
    n = _int_or_400(body.get("breaths") or 10, "breaths")
    if not 1 <= n <= 30:
        raise HTTPException(400, "breaths must be 1..30")
    rng = np.random.default_rng()
    target = float(p.get("target_ml") or 2000)
    now = now_local()
    t0 = int(now.timestamp() * 1000) - n * 15000
    n_bad = int(round(n * QUALITY_MIX[quality]))
    intended = ["good"] * (n - n_bad) + [["too_fast", "too_shallow", "no_hold"][i % 3]
                                         for i in range(n_bad)]
    rng.shuffle(intended)
    breaths, extra = [], []
    for i, lab in enumerate(intended):
        _, feats = models_ml.make_breath(lab, target, rng)
        c = models_ml.classify(feats)
        sc = rules.score(feats, target, float(p.get("hold_target_s") or 3))
        breaths.append({"t": t0 + i * 15000, "features": feats, "label": c["label"], "score": sc})
        extra.append({"proba": c["proba"], "source": c["source"], "intended": lab})
    res = service.record_session(p, now, breaths, source="demo")
    res["breaths"] = [{**b, **e} for b, e in zip(res["breaths"], extra)]
    res["quality"] = quality
    return res


@app.post("/api/demo/miss/{pid}")
def demo_miss(pid: int):
    _require_demo()
    authz.require("demo.control", pid)
    p = _patient_or_404(pid)
    now = now_local()
    targets = []                       # (date, hour) of the last 2 elapsed slots
    day, hour = now.date(), now.hour - 1
    while len(targets) < 2:
        if hour < FIRST_SLOT:
            day, hour = day - timedelta(days=1), LAST_SLOT
            continue
        targets.append((day.isoformat(), min(hour, LAST_SLOT)))
        hour = min(hour, LAST_SLOT) - 1
    service.store().upsert("slots", [{"patient_id": pid, "slot_date": d, "slot_hour": h,
                                      "status": "missed", "session_id": None}
                                     for d, h in targets])
    hours = sorted(h for _, h in targets)
    lang = p.get("language") if p.get("language") in ("en", "hi") else "en"
    text = whatsapp.missed_text(p, hours, lang)
    alerts = [_send(p, "missed", "nurse", text)]
    # Family: only with recorded consent – a guardian who replied STOP gets nothing (same rule
    # as POST /api/whatsapp/{pid}); the blocked attempt is shown in the timeline instead.
    from .comms import messages as comms_messages
    guardian, _, number, blocked = comms_messages.care_update_recipient(p, "family")
    alerts.append(comms_messages.send_care_update(p, "missed", "family", text, lang, guardian=guardian,
                                                  stored_number=number, blocked_reason=blocked)
                  if guardian and blocked else _send(p, "missed", "family", text))
    d = service.patient_detail(pid)
    return {"ok": True, "patient_id": pid,
            "missed": [{"slot_date": d_, "slot_hour": h} for d_, h in targets],
            "status": d["status"], "alert": alerts[0], "alerts": alerts}


@app.post("/api/demo/reset")
def demo_reset(request: Request):
    _require_demo()
    actor = authz.require("demo.control")
    n = seed.reset(service.store())
    seed._last_autopilot = 0.0
    audit.write("demo.reset", "demo", actor=actor, request=request)
    return {"ok": True, "patients": n}


# Feature modules plug in here (each owns its own file). Must stay above the /api 404 catch-all.
# A module that isn't written yet is skipped. One that fails to load is skipped too, with an
# error in the log (and in SKIPPED_MODULES), so one broken feature can't take the site down.
SKIPPED_MODULES: dict[str, str] = {}
for _mod in ("routes_voice", "routes_comms", "routes_auth", "features", "routes_admin",
             "routes_patients", "routes_meds", "routes_appointments", "routes_documents",
             "routes_me", "routes_public", "routes_twin", "routes_devices", "routes_consent",
             "routes_hospital", "routes_doctor"):
    try:
        app.include_router(__import__(f"{__package__}.{_mod}", fromlist=["router"]).router)
    except ModuleNotFoundError as e:
        if e.name != f"{__package__}.{_mod}":
            SKIPPED_MODULES[_mod] = f"{type(e).__name__}: {e}"
            log.error("module %s failed to load: %s", _mod, e)
        else:
            log.info("optional module %s not present yet", _mod)
    except Exception as e:
        SKIPPED_MODULES[_mod] = f"{type(e).__name__}: {e}"
        log.error("module %s failed to load: %s", _mod, e)


@app.get("/api/{rest:path}", include_in_schema=False)
def api_404(rest: str):
    raise HTTPException(404, f"no such API endpoint: /api/{rest}")


# Static website LAST so /api/* wins. html=True serves index.html for folders (/showcase/).
if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
