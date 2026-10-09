"""Comms API (ARCHITECTURE.md CONTRACT D2): escalation ladder, automated calls, WhatsApp
quick replies + inbound webhook, alerts inbox, care circle, guardian magic-link page, weekly
card, voice note, AI nurse call script, trend flag. Everything works with no keys (dry run +
browser simulators). main.py includes `router` automatically. Docs: docs/COMMS.md.
"""
from __future__ import annotations

import logging
import threading
import time

from fastapi import APIRouter, Body, HTTPException, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from . import llm, service, whatsapp
from .comms import (alerts, audio, calls, cards, consent, escalation, guardians, messages,
                    progress, sarvam, script, seed_comms, trend)
from .comms.common import (DISCLOSURE, call_name, consent_current, e164, first_name, has_consent, in_quiet,
                           lang_of, now, public_base, public_event, st, to_dt)
from .config import demo_mode, env, env_flag, iso

log = logging.getLogger("spirobuddy.comms.api")
router = APIRouter(prefix="/api/comms", tags=["comms"])

# ----------------------------------------------------------------------------- background ticker

_ticker: threading.Thread | None = None
_ticker_last = 0.0
_ensured = False


def _ticker_loop():
    global _ticker_last
    # wait for main.py's lifespan to create (and maybe seed) the store
    for _ in range(120):
        if service._store is not None:
            break
        time.sleep(0.5)
    time.sleep(3)
    _ensure_seeded()
    while True:
        try:
            escalation.tick()
            _ticker_last = time.time()
            pause = 1.0 if escalation.busy() else 4.0
        except Exception as e:      # never die: log and keep going
            log.warning("comms tick failed: %s", e)
            pause = 5.0
        time.sleep(pause)


def _start_ticker():
    global _ticker
    if not env_flag("COMMS_TICKER", "1"):
        return
    if _ticker is None or not _ticker.is_alive():
        _ticker = threading.Thread(target=_ticker_loop, name="comms-ticker", daemon=True)
        _ticker.start()


def _ensure_seeded():
    global _ensured
    if _ensured:
        return
    _ensured = True
    if seed_comms.ensure(st()):
        log.info("comms demo data added to the existing store")


def _lazy():
    """Called by every endpoint: make sure the ticker runs and tick if it seems stalled."""
    _start_ticker()
    _ensure_seeded()
    if time.time() - _ticker_last > 6:
        try:
            escalation.tick()
        except Exception as e:
            log.warning("lazy tick failed: %s", e)


_start_ticker()


def _patient_or_404(pid: int) -> dict:
    p = service.get_patient_row(int(pid))
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    return p


def _require_demo():
    if not demo_mode():
        raise HTTPException(403, "demo endpoints are disabled (set DEMO_MODE=1)")


def _bad(e: Exception):
    raise HTTPException(400, str(e))


# ----------------------------------------------------------------------------- status

@router.get("/status")
def status():
    _lazy()
    prov, note = calls.provider()
    qs, qe = guardians.default_config()["quiet_start"], guardians.default_config()["quiet_end"]
    t = now()
    cprov, cnote = calls.provider("checkin")
    return {"ok": True, "calls_provider": prov, "calls_note": note,
            "checkin_provider": cprov, "checkin_note": cnote,
            "sarvam_agent_ready": sarvam.ready(), "sarvam_agent_missing": sarvam.missing(),
            "sarvam_webhook_secret": bool(env("SARVAM_WEBHOOK_SECRET")),
            "twilio_voice_ready": calls.twilio_ready(), "exotel_ready": calls.exotel_ready(),
            "whatsapp_enabled": whatsapp.whatsapp_enabled(),
            "whatsapp_sandbox": messages.is_sandbox(),
            "whatsapp_hint": messages.sandbox_hint() if whatsapp.whatsapp_enabled() else None,
            "whatsapp_last": dict(messages.last_result) or None,
            "whatsapp_min_gap_s": messages.MIN_GAP_S,
            "whatsapp_buttons": bool(messages.content_sid_for("reminder")),
            "public_base_url": public_base() or None, "voice_tts": audio.available(),
            "llm_enabled": llm.llm_enabled(), "hindi_card": cards.hindi_ok(),
            "quiet_hours": {"start": qs, "end": qe, "now_quiet": in_quiet(t, qs, qe)},
            "auto_escalate": env_flag("COMMS_AUTO_ESCALATE", "1"),
            "ticker_alive": bool(_ticker and _ticker.is_alive()),
            "demo_mode": demo_mode(), "now": iso(t)}


@router.post("/tick")
def manual_tick():
    return escalation.tick()


# ----------------------------------------------------------------------------- alerts

@router.get("/alerts")
def get_alerts(status: str = Query("active"), patient_id: int | None = None,
               limit: int = Query(100, ge=1, le=500)):
    _lazy()
    return alerts.list_alerts(status, patient_id, limit)


@router.get("/alerts/counts")
def alert_counts(me: str | None = None):
    _lazy()
    return alerts.counts(me)


@router.post("/alerts/{aid}/{action}")
def alert_action(aid: int, action: str, body: dict | None = Body(None)):
    body = body or {}
    try:
        a = alerts.act(aid, action, body.get("by"), body.get("minutes"), body.get("to"))
    except ValueError as e:
        _bad(e)
    if a is None:
        raise HTTPException(404, f"alert {aid} not found")
    return a


# ----------------------------------------------------------------------------- escalation

@router.get("/escalations")
def get_escalations(patient_id: int | None = None, active: bool = False,
                    limit: int = Query(20, ge=1, le=200)):
    _lazy()
    return escalation.list_runs(patient_id, active, limit)


@router.post("/escalations/start/{pid}")
def start_escalation(pid: int, body: dict | None = Body(None)):
    _patient_or_404(pid)
    body = body or {}
    speed = body.get("speed") or "real"
    if speed not in ("real", "fast"):
        raise HTTPException(400, "speed must be real or fast")
    return escalation.start(pid, reason=body.get("reason") or "manual", speed=speed,
                            override_quiet=bool(body.get("override_quiet")))


@router.post("/escalations/{rid}/stop")
def stop_escalation(rid: int, body: dict | None = Body(None)):
    r = escalation.stop(rid, (body or {}).get("by") or "nurse")
    if r is None:
        raise HTTPException(404, f"escalation {rid} not found")
    return r


@router.post("/escalations/{rid}/advance")
def advance_escalation(rid: int):
    r = escalation.advance(rid)
    if r is None:
        raise HTTPException(404, f"escalation {rid} not found")
    return r


@router.post("/demo/ladder/{pid}")
def demo_ladder(pid: int, body: dict | None = Body(None)):
    """Demo fast-forward: the whole ladder plays out in about 60 seconds."""
    _require_demo()
    _patient_or_404(pid)
    body = body or {}
    return escalation.start(pid, reason="demo", speed="fast",
                            override_quiet=bool(body.get("override_quiet", False)))


@router.post("/demo/red-flag/{pid}")
def demo_red_flag(pid: int, body: dict | None = Body(None)):
    _require_demo()
    _patient_or_404(pid)
    text = (body or {}).get("text") or "सीने में दर्द है, साँस नहीं आ रही"
    return messages.handle_inbound(text, patient_id=pid, role="patient", channel="simulator")


@router.post("/demo/trend/{pid}")
def demo_trend(pid: int):
    _require_demo()
    _patient_or_404(pid)
    return trend.check_patient(pid)


# ----------------------------------------------------------------------------- timeline

@router.get("/timeline/{pid}")
def timeline(pid: int, limit: int = Query(60, ge=1, le=500)):
    _lazy()
    _patient_or_404(pid)
    rows = st().select("escalation_events", [("patient_id", "eq", pid)], order="created_at", desc=True,
                       limit=limit)
    return [public_event(e) for e in rows]


@router.get("/events")
def events(since_id: int = 0, limit: int = Query(50, ge=1, le=300), patient_id: int | None = None):
    """All patients' comms events (newest first) – the demo panel's live feed."""
    _lazy()
    f = [("id", "gt", since_id)]
    if patient_id is not None:
        f.append(("patient_id", "eq", patient_id))
    names = {p["id"]: p["name"] for p in st().select("patients", columns="id,name")}
    out = []
    for e in st().select("escalation_events", f, order="id", desc=True, limit=limit):
        pe = public_event(e)
        pe["patient_name"] = names.get(e.get("patient_id"))
        out.append(pe)
    return out


# ----------------------------------------------------------------------------- calls

@router.get("/calls")
def get_calls(active: bool = False, patient_id: int | None = None,
              limit: int = Query(30, ge=1, le=200)):
    _lazy()
    return calls.list_calls(active, patient_id, limit)


@router.get("/calls/{cid}")
def get_call(cid: int):
    c = calls.get_call(cid)
    if not c:
        raise HTTPException(404, f"call {cid} not found")
    return calls.public_call(c)


@router.post("/calls/{cid}/answer")
def answer_call(cid: int):
    c = calls.answer(cid, "phone simulator")
    if c is None:
        raise HTTPException(404, f"call {cid} not found")
    return c


@router.post("/calls/{cid}/press")
def press_key(cid: int, body: dict = Body(...)):
    digit = str(body.get("digit") or "")
    if digit not in ("1", "2", "3", ""):
        raise HTTPException(400, "digit must be 1, 2 or 3")
    c = calls.get_call(cid)
    if c and isinstance(c.get("meta"), dict) and c["meta"].get("style") == "agent":
        raise HTTPException(400, "this is a conversational AI call – answer by voice (POST /agent-turn)")
    try:
        return calls.press(cid, digit, "phone simulator")
    except KeyError:
        raise HTTPException(404, f"call {cid} not found")


@router.post("/calls/{cid}/agent-turn")
def agent_turn(cid: int, body: dict = Body(...)):
    """Conversational (Sarvam-style) call in the browser phone simulator: the patient's spoken
    answer (Voice.record -> /api/voice/stt) or a tapped pre-written answer. The final result goes
    through the same normalise + apply as the real Sarvam webhook."""
    c = calls.get_call(cid)
    if not c:
        raise HTTPException(404, f"call {cid} not found")
    if not (isinstance(c.get("meta"), dict) and c["meta"].get("style") == "agent"):
        raise HTTPException(400, "this is a keypad (IVR) call – use /press")
    if c.get("provider") != "dry_run":
        raise HTTPException(400, "only simulated calls take answers here – the real call talks to Sarvam")
    src = "voice" if (body or {}).get("source") == "voice" else "tap"
    return sarvam.sim_turn(cid, str((body or {}).get("text") or ""),
                           f"phone simulator ({'spoken' if src == 'voice' else 'tapped answer'})")


@router.post("/calls/{cid}/hangup")
def hangup(cid: int, body: dict | None = Body(None)):
    reason = (body or {}).get("reason") or "hangup"
    cur = calls.get_call(cid)
    if cur and reason != "declined" and cur.get("status") == "in-progress" \
            and isinstance(cur.get("meta"), dict) and cur["meta"].get("style") == "agent":
        return sarvam.sim_finish(cid, f"phone simulator ({reason})")
    c = calls.finish(cid, "no-answer" if reason == "declined" else "completed",
                     f"phone simulator ({reason})")
    if c is None:
        raise HTTPException(404, f"call {cid} not found")
    return c


@router.post("/call-patient/{pid}")
def call_patient(pid: int, body: dict | None = Body(None)):
    p = _patient_or_404(pid)
    body = body or {}
    nurse = (body.get("nurse_name") or "Nurse").strip()[:60]
    return calls.click_to_call(p, nurse, body.get("nurse_phone"), guardians.get_settings(pid))


@router.post("/checkin-call/{pid}")
def checkin_call(pid: int, body: dict | None = Body(None)):
    """AI check-in call now ("Are you okay? Why did you miss it?"): Sarvam Voice Agent when it is
    set up, otherwise the browser phone simulator. Needs recorded consent (flag + date)."""
    p = _patient_or_404(pid)
    cfg = guardians.get_settings(pid)
    d = service.patient_detail(pid) or {}
    missed = int((body or {}).get("missed") or max(2, int(d.get("trailing_missed") or 0)))
    run = escalation.active_run(pid)
    c = calls.place_call(p, "reminder", "patient", p["name"], cfg.get("patient_phone"),
                         p.get("language") or "en", run_id=run["id"] if run else None,
                         ring_s=int(cfg.get("ring_s") or 30), consent=has_consent(cfg),
                         missed=missed, style="agent", consent_fresh=consent_current(cfg))
    if c is None:
        raise HTTPException(409, "No recorded consent (yes + date) for automated calls to this patient – "
                                 "record it in Care circle settings first.")
    return c


# ----- Sarvam Voice Agent webhook + demo replay (comms/sarvam.py, docs/COMMS.md §5)

@router.post("/webhooks/sarvam")
async def sarvam_webhook(request: Request, token: str | None = None):
    """Sarvam 'Instant Outbound' webhook (sent once per call attempt). Our shared secret is in
    the URL (?token=) because Sarvam documents no signature; only attempts we placed count."""
    if not sarvam.check_token(token or request.headers.get("X-Webhook-Token")):
        raise HTTPException(403, "bad or missing webhook token")
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(400, "body must be JSON")
    if not isinstance(payload, dict):
        raise HTTPException(400, "body must be a JSON object")
    res = sarvam.handle_webhook(payload)
    if not res.get("ok"):
        raise HTTPException(404, res.get("error") or "unknown call")
    return res


@router.get("/demo/sarvam-samples")
def sarvam_samples():
    return [{"key": k, "label": v.get("label") or k, "status": (v.get("payload") or {}).get("status")}
            for k, v in sarvam.load_samples().items()]


@router.post("/demo/sarvam-replay/{pid}")
def sarvam_replay(pid: int, body: dict | None = Body(None)):
    """Demo: feed a saved Sarvam webhook payload through the real webhook handler, so the
    nurse note appears even if the live call fails."""
    _require_demo()
    _patient_or_404(pid)
    try:
        return sarvam.replay(pid, (body or {}).get("sample") or "pain")
    except ValueError as e:
        _bad(e)


@router.post("/call-script/{pid}")
def call_script(pid: int):
    _patient_or_404(pid)
    return script.generate(pid)


# ----- Twilio webhooks (TwiML)

async def _twilio_form(request: Request) -> dict:
    form = {k: v for k, v in (await request.form()).items()}
    token = env("TWILIO_AUTH_TOKEN")
    if token and public_base() and env_flag("TWILIO_VALIDATE", "1"):
        from twilio.request_validator import RequestValidator
        url = public_base() + request.url.path + (f"?{request.url.query}" if request.url.query else "")
        if not RequestValidator(token).validate(url, form, request.headers.get("X-Twilio-Signature", "")):
            raise HTTPException(403, "bad Twilio signature")
    return form


def _xml(s: str) -> Response:
    return Response(content=s, media_type="application/xml")


@router.api_route("/twilio/voice/{cid}", methods=["GET", "POST"])
async def twilio_voice(cid: int, request: Request, retry: int = 0):
    if request.method == "POST":
        await _twilio_form(request)
    c = calls.get_call(cid)
    if not c:
        return _xml("<Response><Hangup/></Response>")
    if c.get("status") != "in-progress":
        calls.answer(cid, "Twilio")
    return _xml(calls.twiml_menu(c, retry=bool(retry)))


@router.post("/twilio/gather/{cid}")
async def twilio_gather(cid: int, request: Request):
    form = await _twilio_form(request)
    try:
        res = calls.press(cid, form.get("Digits", ""), "Twilio keypress")
    except KeyError:
        return _xml("<Response><Hangup/></Response>")
    return _xml(calls.twiml_after(res))


@router.post("/twilio/status/{cid}")
async def twilio_status(cid: int, request: Request):
    form = await _twilio_form(request)
    calls.provider_status(cid, form.get("CallStatus", ""), "Twilio status callback")
    return _xml("<Response/>")


# ----- Exotel webhooks (call flow applets point here with CustomField=<call id>)

def _exo_call(request: Request) -> dict | None:
    cid = request.query_params.get("CustomField") or request.query_params.get("customfield")
    try:
        return calls.get_call(int(str(cid).strip('"')))
    except (TypeError, ValueError):
        return None


@router.get("/exotel/greeting")
def exotel_greeting(request: Request):
    """Greeting applet (dynamic text). Returns the menu as plain text."""
    c = _exo_call(request)
    if c and c.get("status") != "in-progress":
        calls.answer(c["id"], "Exotel")
    return PlainTextResponse((c or {}).get("script") or "Namaste. This is SpiroBuddy.")


@router.get("/exotel/gather")
def exotel_gather(request: Request):
    """Gather applet (dynamic URL): menu prompt, 1 digit."""
    c = _exo_call(request)
    lang = lang_of((c or {}).get("language"), "en")
    prompt = {"text": (c or {}).get("script") or ""}
    url = audio.tts_url(prompt["text"], lang, absolute=True, phone=True)
    if url:
        prompt = {"audio_url": url}
    return JSONResponse({"gather_prompt": prompt, "max_input_digits": 1, "finish_on_key": "#",
                         "input_timeout": 7, "repeat_menu": 2,
                         "repeat_gather_prompt": prompt})


@router.get("/exotel/passthru")
def exotel_passthru(request: Request):
    """Passthru applet after Gather: digits arrive as ?digits="1"."""
    c = _exo_call(request)
    if not c:
        return PlainTextResponse("ok")
    digit = (request.query_params.get("digits") or "").strip('"')[:1]
    try:
        res = calls.press(c["id"], digit, "Exotel keypress")
        return PlainTextResponse(res["say"])
    except KeyError:
        return PlainTextResponse("ok")


@router.post("/exotel/status/{cid}")
async def exotel_status(cid: int, request: Request):
    form = {k: v for k, v in (await request.form()).items()}
    raw = (form.get("Status") or form.get("status") or "").lower()
    calls.provider_status(cid, {"completed": "completed", "busy": "busy", "failed": "failed",
                                "no-answer": "no-answer"}.get(raw, raw), "Exotel status callback")
    return PlainTextResponse("ok")


# ----------------------------------------------------------------------------- WhatsApp

@router.post("/webhooks/whatsapp")
async def whatsapp_inbound(request: Request):
    """Twilio WhatsApp inbound webhook: From, Body, ButtonPayload/ButtonText."""
    form = await _twilio_form(request)
    messages.handle_inbound(form.get("Body") or form.get("ButtonText") or "",
                            from_number=form.get("From"),
                            payload=form.get("ButtonPayload"), channel="whatsapp")
    return _xml("<Response/>")


@router.post("/webhooks/whatsapp/status")
async def whatsapp_status(request: Request):
    await _twilio_form(request)
    return _xml("<Response/>")


@router.get("/wa/thread/{pid}")
def wa_thread(pid: int, role: str = "patient", guardian_id: int | None = None,
              limit: int = Query(40, ge=1, le=200)):
    """Chat history for the WhatsApp simulator: outbound messages + replies, oldest first."""
    _lazy()
    p = _patient_or_404(pid)
    g = None
    if role == "guardian":
        g = guardians.get_guardian(guardian_id) if guardian_id else guardians.primary_guardian(pid)
    to_role = "family" if role == "guardian" else "patient"
    outs = st().select("messages", [("patient_id", "eq", pid), ("to_role", "eq", to_role)],
                       order="id", desc=True, limit=limit)
    if role == "guardian" and g:
        is_primary = bool(g.get("is_primary"))
        others = {x.get("phone") for x in guardians.list_guardians(pid) if x["id"] != g["id"]}
        outs = [m for m in outs if m.get("to_number") == g.get("phone")
                or (is_primary and m.get("to_number") not in others)]
    ins = st().select("inbound_messages", [("patient_id", "eq", pid),
                                           ("from_role", "eq", "guardian" if role == "guardian" else "patient")],
                      order="id", desc=True, limit=limit)
    if role == "guardian" and g:
        ins = [m for m in ins if m.get("guardian_id") in (None, g.get("id"))]
    lang = lang_of((g or {}).get("language") if role == "guardian" else p.get("language"), "en")
    items = []
    for m in outs:
        kind = m.get("kind")
        btns = []
        if kind in messages.BUTTONS_BY_KIND:
            r, table = messages.BUTTONS_BY_KIND[kind]
            btns = [{"payload": k, "label": lbl} for k, lbl in table[lang]]
        item = {"dir": "out", "id": f"m{m['id']}", "kind": kind, "text": m.get("text"),
                "buttons": btns, "sent": bool(m.get("sent")), "dry_run": bool(m.get("dry_run")),
                "at": iso(to_dt(m.get("created_at")) or now())}
        if kind == "weekly_card":
            item["image"] = f"/api/comms/card/{pid}.png?lang={lang}&v={m['id']}"
        if kind == "voice_note":
            item["audio"] = True
        items.append(item)
    for m in ins:
        items.append({"dir": "in", "id": f"i{m['id']}", "text": m.get("body"),
                      "intent": m.get("intent"), "at": iso(to_dt(m.get("created_at")) or now())})
    items.sort(key=lambda x: x["at"])
    # a reminder's buttons are spent once the person answered after it
    last_in = max([x["at"] for x in items if x["dir"] == "in"], default="")
    for x in items:
        if x.get("buttons") and last_in and x["at"] < last_in:
            x["answered"] = True
    return {"patient_id": pid, "role": role, "language": lang,
            "contact": {"name": (g or p).get("name"),
                        "relation": (g or {}).get("relation"),
                        "number": (g or {}).get("phone") if role == "guardian"
                        else guardians.get_settings(pid).get("patient_phone")},
            "guardian_id": (g or {}).get("id"), "items": items[-limit:]}


@router.post("/wa/reply")
def wa_reply(body: dict = Body(...)):
    """A reply typed/tapped in the WhatsApp simulator – same logic as the real webhook."""
    pid = body.get("patient_id")
    if pid is None:
        raise HTTPException(400, "patient_id is required")
    _patient_or_404(int(pid))
    role = body.get("role") if body.get("role") in ("patient", "guardian") else "patient"
    text = str(body.get("text") or "").strip()
    payload = body.get("payload")
    if not text and not payload:
        raise HTTPException(400, "text or payload is required")
    return messages.handle_inbound(text or "", payload=payload, patient_id=int(pid), role=role,
                                   guardian_id=body.get("guardian_id"), channel="simulator")


@router.get("/card/{pid}.png")
def card_png(pid: int, lang: str = "hi"):
    _patient_or_404(pid)
    png = cards.render_card(pid, lang)
    if not png:
        raise HTTPException(404, "no data")
    return Response(content=png, media_type="image/png",
                    headers={"Cache-Control": "no-store"})


@router.post("/weekly-card/{pid}")
def send_weekly_card(pid: int, body: dict | None = Body(None)):
    p = _patient_or_404(pid)
    body = body or {}
    to = body.get("to") or "family"
    if to not in ("family", "patient"):
        raise HTTPException(400, "to must be family or patient")
    g = guardians.primary_guardian(pid) if to == "family" else None
    lang = lang_of(body.get("language") or ((g or {}).get("language") if g else p.get("language")), "hi")
    card_lang = "hi" if lang == "hi" else "en"
    base = public_base()
    media = f"{base}/api/comms/card/{pid}.png?lang={card_lang}" if base else None
    res = messages.send(p, to, (g or {}).get("phone") if g else guardians.get_settings(pid).get("patient_phone"),
                        cards.caption(pid, card_lang), "weekly_card", lang, media_url=media,
                        to_name=guardians.guardian_label(g) if g else first_name(p["name"]))
    res["image_url"] = f"/api/comms/card/{pid}.png?lang={card_lang}"
    if not media:
        res["note"] = "Set PUBLIC_BASE_URL so WhatsApp can fetch the image; text caption only."
    return res


@router.post("/voice-note/{pid}")
def send_voice_note(pid: int, body: dict | None = Body(None)):
    """Evening summary as a 20-second voice note in the guardian's/patient's language."""
    p = _patient_or_404(pid)
    body = body or {}
    to = body.get("to") or "family"
    g = guardians.primary_guardian(pid) if to == "family" else None
    lang = lang_of((g or {}).get("language") if g else p.get("language"), "hi")
    d = service.patient_detail(pid)
    s = llm.summarize(llm.add_recent(service.summary_stats(d), d), "hi" if lang == "hi" else "en")
    text = s["text"]
    if lang == "ta":
        try:
            from . import voice
            text = voice.translate(text, "en", "ta")
        except Exception:
            pass
    spoken = f"{DISCLOSURE[lang]} {text}"           # the voice note starts with the AI disclosure
    rel = audio.tts_url(spoken, lang)
    absolute = audio.tts_url(spoken, lang, absolute=True)
    res = messages.send(p, "family" if g else "patient",
                        (g or {}).get("phone") if g else guardians.get_settings(pid).get("patient_phone"),
                        "🎧 " + text, "voice_note", lang, media_url=absolute,
                        to_name=guardians.guardian_label(g) if g else first_name(p["name"]))
    res.update({"audio_url": rel, "summary_source": s["source"], "language": lang,
                "browser_lang": calls.BROWSER_LANG[lang], "speak_text": spoken})
    if not rel:
        res["note"] = "No SARVAM_API_KEY – the browser reads the note aloud instead."
    return res


# ----------------------------------------------------------------------------- care circle

@router.get("/care/{pid}")
def care(pid: int):
    _lazy()
    p = _patient_or_404(pid)
    return {"patient_id": pid, "settings": guardians.settings_public(pid),
            "guardians": [guardians.public_guardian(g, p) for g in guardians.list_guardians(pid)]}


@router.put("/care/{pid}")
def put_care(pid: int, body: dict = Body(...)):
    p = _patient_or_404(pid)
    try:
        guardians.put_settings(pid, body)
    except (ValueError, TypeError) as e:
        _bad(e)
    return {"patient_id": pid, "settings": guardians.settings_public(pid),
            "guardians": [guardians.public_guardian(g, p) for g in guardians.list_guardians(pid)]}


@router.post("/guardians")
def add_guardian(body: dict = Body(...)):
    pid = body.get("patient_id")
    if pid is None:
        raise HTTPException(400, "patient_id is required")
    p = _patient_or_404(int(pid))
    try:
        g = guardians.create_guardian(int(pid), body)
    except ValueError as e:
        _bad(e)
    return guardians.public_guardian(g, p)


@router.put("/guardians/{gid}")
def edit_guardian(gid: int, body: dict = Body(...)):
    try:
        g = guardians.update_guardian(gid, body)
    except ValueError as e:
        _bad(e)
    if not g:
        raise HTTPException(404, f"guardian {gid} not found")
    return guardians.public_guardian(g, service.get_patient_row(g["patient_id"]))


@router.delete("/guardians/{gid}")
def remove_guardian(gid: int):
    if not guardians.delete_guardian(gid):
        raise HTTPException(404, f"guardian {gid} not found")
    return {"ok": True}


# ----------------------------------------------------------------------------- consent

@router.get("/consent-text/{pid}")
def consent_text(pid: int, lang: str | None = None):
    """The consent statement in the patient's language (read aloud to them), with the itemised
    list of data kept and the one-word STOP. Valid 7 days, renewed weekly."""
    p = _patient_or_404(pid)
    out = consent.consent_text(lang or p.get("language") or "en")
    out["audio_url"] = audio.tts_url(out["text"], out["language"])
    out["browser_lang"] = calls.BROWSER_LANG[out["language"]]
    return out


@router.post("/consent/ask/{pid}")
def consent_ask(pid: int, body: dict | None = Body(None)):
    """Send the weekly one-question renewal now ("keep the reminders? ✅ yes / ⛔ STOP")."""
    _patient_or_404(pid)
    body = body or {}
    to = body.get("to") or "patient"
    if to not in ("patient", "family"):
        raise HTTPException(400, "to must be patient or family")
    g = guardians.get_guardian(int(body["guardian_id"])) if body.get("guardian_id") else None
    try:
        return consent.ask(pid, to, g)
    except ValueError as e:
        _bad(e)


# ----------------------------------------------------------------------------- guardian page

STATUS_PLAIN = {"green": "good", "yellow": "nudge", "red": "call"}


def _guardian_or_404(token: str) -> dict:
    g = guardians.by_token(token)
    if not g:
        raise HTTPException(404, "This link is not valid any more. Please ask the hospital for a new one.")
    return g


@router.get("/guardian/{token}")
def guardian_view(token: str):
    _lazy()
    g = _guardian_or_404(token)
    pr = progress.progress(g["patient_id"])
    if not pr:
        raise HTTPException(404, "patient not found")
    p = pr["patient"]
    lang = lang_of(g.get("language"), "hi")
    cfg = guardians.get_settings(g["patient_id"])
    tel = e164(cfg.get("patient_phone")) or e164(env("DEMO_PATIENT_PHONE"))
    queued = st().select("cheers", [("patient_id", "eq", g["patient_id"]), ("status", "eq", "queued")])
    last = pr["last"]
    return {
        "guardian": {"id": g["id"], "name": g["name"], "first_name": first_name(g["name"]),
                     "relation": g.get("relation"), "language": lang},
        "patient": {"first_name": first_name(p["name"]), "name": p["name"], "sex": p.get("sex"),
                    "calls_patient": call_name(g.get("relation"), p, lang),
                    "calls_patient_en": call_name(g.get("relation"), p, "en"),
                    "calls_patient_hi": call_name(g.get("relation"), p, "hi"),
                    "calls_patient_ta": call_name(g.get("relation"), p, "ta")},
        "status": STATUS_PLAIN.get(pr["status"], "good"),
        "today": [{"hour": s["hour"], "status": s["status"]} for s in pr["today"]],
        "done": pr["done"], "due": pr["due"], "streak": pr["streak"],
        "best_today": pr["best_today"], "target_ml": pr["target_ml"],
        "last": ({"at": last["at"], "minutes_ago": progress.minutes_ago(last["at"]),
                  "best_ml": last["best_ml"], "slot_hour": last["slot_hour"]} if last else None),
        "call": {"tel": tel, "display": cfg.get("patient_phone"), "demo": tel is None},
        "cheers_queued": len(queued),
        "quiet": {"start": guardians.guardian_quiet(g, cfg)[0], "end": guardians.guardian_quiet(g, cfg)[1],
                  "own": bool(g.get("quiet_start")), "presets": QUIET_PRESETS},
        "cheer_presets": messages.CHEER_PRESETS[lang],
        "updated_at": iso(now()),
    }


@router.post("/guardian/{token}/cheer")
def guardian_cheer(token: str, body: dict | None = Body(None)):
    g = _guardian_or_404(token)
    body = body or {}
    lang = lang_of(body.get("language") or g.get("language"), "hi")
    presets = messages.CHEER_PRESETS[lang]
    try:
        i = int(body.get("preset", 0))
    except (TypeError, ValueError):
        i = 0
    if not 0 <= i < len(presets):
        raise HTTPException(400, f"preset must be 0..{len(presets) - 1}")
    c = messages.queue_cheer(g["patient_id"], g, presets[i], lang)
    p = service.get_patient_row(g["patient_id"]) or {}
    return {"ok": True, "cheer_id": c.get("id"), "text": presets[i],
            "message": messages.reply_text("cheer", lang, who=call_name(g.get("relation"), p, lang))}


QUIET_PRESETS = [["21:00", "07:00"], ["22:00", "07:00"], ["20:00", "08:00"]]


@router.put("/guardian/{token}/quiet")
def guardian_quiet_hours(token: str, body: dict = Body(...)):
    """The family member sets their own quiet hours (no calls/messages to them then, except a
    red flag). One tap on the family page – no typing."""
    g = _guardian_or_404(token)
    try:
        guardians.update_guardian(g["id"], {"quiet_start": body.get("quiet_start"),
                                            "quiet_end": body.get("quiet_end")})
    except ValueError as e:
        _bad(e)
    from .comms.common import log_event
    log_event(g["patient_id"], "quiet_hold", f"{guardians.guardian_label(g)} set quiet hours "
              f"{body.get('quiet_start')}–{body.get('quiet_end')} on the family page",
              channel="web", actor="guardian", to_name=first_name(g["name"]), status="info")
    return {"ok": True, "quiet_start": body.get("quiet_start"), "quiet_end": body.get("quiet_end")}


@router.post("/guardian/{token}/call-log")
def guardian_call_log(token: str):
    """The guardian tapped 'Call Papa' (we log it; the phone dials via tel:)."""
    g = _guardian_or_404(token)
    from .comms.common import log_event
    log_event(g["patient_id"], "click_to_call", f"{guardians.guardian_label(g)} tapped “Call” on the family page",
              channel="web", actor="guardian", to_name=first_name(g["name"]), status="info")
    return {"ok": True}


# ----------------------------------------------------------------------------- cheers & trend

@router.get("/cheers/{pid}")
def get_cheers(pid: int, status: str = "queued"):
    _patient_or_404(pid)
    f = [("patient_id", "eq", pid)]
    if status in ("queued", "played"):
        f.append(("status", "eq", status))
    return st().select("cheers", f, order="id", desc=True, limit=50)


@router.post("/cheers/{cid}/played")
def cheer_played(cid: int):
    rows = st().select("cheers", [("id", "eq", cid)])
    if not rows:
        raise HTTPException(404, f"cheer {cid} not found")
    st().update("cheers", [("id", "eq", cid)], {"status": "played", "played_at": iso(now())})
    return {"ok": True}


@router.get("/trend/{pid}")
def get_trend(pid: int):
    d = service.patient_detail(pid)
    if d is None:
        raise HTTPException(404, f"patient {pid} not found")
    return trend.evaluate(d)


@router.get("/patient/{pid}")
def patient_comms(pid: int):
    """Everything the patient page needs in one poll."""
    _lazy()
    p = _patient_or_404(pid)
    d = service.patient_detail(pid)
    runs = escalation.list_runs(pid, limit=5)
    return {"patient_id": pid, "active_run": next((r for r in runs if r["status"] == "active"), None),
            "runs": runs, "alerts": alerts.list_alerts("active", pid, 20),
            "trend": trend.evaluate(d) if d else None,
            "calls": calls.list_calls(False, pid, 5),
            "guardians": [guardians.public_guardian(g, p) for g in guardians.list_guardians(pid)],
            "settings": guardians.settings_public(pid)}
