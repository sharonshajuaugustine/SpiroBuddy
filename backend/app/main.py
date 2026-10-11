"""SpiroBuddy API (contract D in docs/ARCHITECTURE.md) + static hosting of web/.

Run from the repo root:  uvicorn backend.app.main:app --port 8000
"""
from __future__ import annotations

import logging
import math
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import llm, models_ml, rules, seed, service, whatsapp
from .config import (FIRST_SLOT, LABELS, LAST_SLOT, WEB_DIR, demo_mode, env, env_flag, iso,
                     now_local)

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
    models_ml.load()
    yield


app = FastAPI(title="SpiroBuddy API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])


@app.middleware("http")
async def _revalidate_static(request, call_next):
    """Browsers must re-check web/ files (cheap 304 via ETag), so a fix is never hidden by cache."""
    resp = await call_next(request)
    if not request.url.path.startswith("/api"):
        resp.headers.setdefault("Cache-Control", "no-cache")
    return resp


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
def update_patient(pid: int, body: dict = Body(...)):
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
    p = _patient_or_404(_int_or_400(pid, "patient_id"))
    breaths = body.get("breaths") or []
    if not isinstance(breaths, list) or not all(
            isinstance(b, dict) and isinstance(b.get("features") or {}, dict) for b in breaths):
        raise HTTPException(400, "breaths must be a list of {t, features, label, score} objects")
    try:
        res = service.record_session(p, body.get("started_at"), breaths,
                                     source=body.get("source") or "app")
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
def demo_reset():
    _require_demo()
    n = seed.reset(service.store())
    seed._last_autopilot = 0.0
    return {"ok": True, "patients": n}


# Feature modules plug in here (each owns its own file). Must stay above the /api 404 catch-all.
for _mod in ("routes_voice", "routes_comms"):
    try:
        app.include_router(__import__(f"{__package__}.{_mod}", fromlist=["router"]).router)
    except ModuleNotFoundError as e:
        if e.name != f"{__package__}.{_mod}":
            raise
        log.info("optional module %s not present yet", _mod)


@app.get("/api/{rest:path}", include_in_schema=False)
def api_404(rest: str):
    raise HTTPException(404, f"no such API endpoint: /api/{rest}")


# Static website LAST so /api/* wins. html=True serves index.html for folders (/showcase/).
if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
