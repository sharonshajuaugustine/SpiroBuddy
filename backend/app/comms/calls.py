"""Automated calls (IVR: press 1 / 2 / 3) and nurse click-to-call.

Providers (CALL_PROVIDER = auto | twilio | exotel | sarvam_agent | dry_run, default auto):
  - sarvam_agent : conversational AI check-in call ("Are you okay? Why did you miss it?") through a
             Sarvam Voice Agent on an Indian number (comms/sarvam.py). Used for the patient's call
             when the care setting call_style = "agent". Spoken answers (Sarvam DTMF is planned).
  - exotel : Indian caller ID (ExoPhone) – the production choice for India. Needs EXOTEL_* and a
             call flow built in the Exotel dashboard that points at our webhooks (docs/COMMS.md).
  - twilio : demo provider. Twilio calls to Indian numbers show an *international* caller ID
             (+1…), consent is required (Twilio India voice guidelines) – fine for a demo.
  - dry_run: no keys, or no PUBLIC_BASE_URL for webhooks. The call "rings" in the browser phone
             simulator on the demo panel, and pressing 1/2/3 there runs the same logic.
Automated calls are only placed when consent is recorded for that person (care circle).
Audio: natural Indian voices from backend/app/voice.py via <Play>, else Twilio <Say>.
"""
from __future__ import annotations

import logging
from datetime import timedelta
from urllib.parse import urlencode

from ..config import demo_mode, env, iso
from . import audio
from .common import (call_name, first_name, lang_of, log_event, now, public_base,
                     masked_number, resolve_number, st, to_dt)

log = logging.getLogger("spirobuddy.comms.calls")

ACTIVE = ("queued", "initiated", "ringing", "in-progress")
FINAL = ("completed", "no-answer", "busy", "failed", "canceled")

# Twilio <Say> voices (fallback when voice.py has no audio). Polly.Aditi speaks hi-IN and en-IN.
SAY_VOICE = {"hi": ("hi-IN", "Polly.Aditi"), "en": ("en-IN", "Polly.Aditi"),
             "ta": ("ta-IN", "Google.ta-IN-Standard-A")}
BROWSER_LANG = {"hi": "hi-IN", "en": "en-IN", "ta": "ta-IN"}


# ----------------------------------------------------------------------------- provider choice

def twilio_ready() -> bool:
    return bool(env("TWILIO_ACCOUNT_SID") and env("TWILIO_AUTH_TOKEN") and env("TWILIO_VOICE_FROM"))


def exotel_ready() -> bool:
    return bool(env("EXOTEL_SID") and env("EXOTEL_API_KEY") and env("EXOTEL_API_TOKEN")
                and env("EXOTEL_CALLER_ID") and env("EXOTEL_WEBHOOK_SECRET"))


def sarvam_ready() -> bool:
    from . import sarvam
    return sarvam.ready()


def provider(purpose: str | None = None) -> tuple[str, str]:
    """-> (provider, note). purpose="checkin" = the conversational AI call (Sarvam or simulator);
    anything else = the keypad (IVR) call through Exotel / Twilio / simulator."""
    pref = env("CALL_PROVIDER", "auto").lower()
    if pref == "dry_run":
        return "dry_run", "CALL_PROVIDER=dry_run"
    base = public_base()
    if purpose == "checkin":
        if pref in ("auto", "sarvam_agent") and sarvam_ready():
            if not base:
                return "dry_run", "Sarvam agent settings found but PUBLIC_BASE_URL missing (Sarvam can't reach our webhook)"
            return "sarvam_agent", "Sarvam Voice Agent (AI check-in call, Indian number)"
        return "dry_run", "no Sarvam Voice Agent settings – the AI check-in call runs in the browser phone simulator"
    want = []
    if pref in ("auto", "exotel"):
        want.append("exotel")
    if pref in ("auto", "twilio"):
        want.append("twilio")
    for p in want:
        if p == "exotel" and exotel_ready():
            if not base or not env("EXOTEL_APP_ID"):
                return "dry_run", "Exotel keys set but PUBLIC_BASE_URL / EXOTEL_APP_ID missing"
            return "exotel", "Exotel (Indian caller ID)"
        if p == "twilio" and twilio_ready():
            if not base:
                return "dry_run", "Twilio keys set but PUBLIC_BASE_URL missing (Twilio can't reach our webhooks)"
            return "twilio", "Twilio (international caller ID – demo)"
    return "dry_run", "no call provider keys – calls ring in the browser phone simulator"


def calls_enabled() -> bool:
    return provider()[0] != "dry_run"


# ----------------------------------------------------------------------------- scripts

def menu_text(purpose: str, patient: dict, lang: str, guardian: dict | None = None,
              missed: int = 2) -> str:
    fn = first_name(patient.get("name"))
    male = (patient.get("sex") or "").upper() != "F"
    if purpose in ("guardian", "guardian_red_flag"):
        g = first_name((guardian or {}).get("name"))
        who = call_name((guardian or {}).get("relation"), patient, lang)
        red = purpose == "guardian_red_flag"
        if lang == "hi":
            head = (f"नमस्ते {g} जी, यह स्पाइरो-बडी की स्वचालित देखभाल सहायक है, अस्पताल की ओर से, {who} के लिए। "
                    + (f"{who} ने मदद माँगी है, और नर्स को बता दिया गया है। " if red else
                       f"{who} ने लगातार {missed} साँस-व्यायाम छोड़ दिए हैं और हमारी कॉल का जवाब नहीं दिया। "))
            return head + ("अगर आप अभी उनका हाल पूछेंगे तो 1 दबाइए। आज की प्रगति सुनने के लिए 2 दबाइए। "
                           "नर्स से बात करने के लिए 3 दबाइए।")
        if lang == "ta":
            head = (f"வணக்கம் {g}, இது ஸ்பைரோபடியின் தானியங்கி பராமரிப்பு உதவியாளர், {who}-க்காக மருத்துவமனையிலிருந்து. "
                    + (f"{who} உதவி கேட்டுள்ளார்; செவிலியருக்குத் தெரிவிக்கப்பட்டது. " if red else
                       f"{who} தொடர்ந்து {missed} மூச்சுப் பயிற்சிகளைத் தவறவிட்டுள்ளார். "))
            return head + ("இப்போது விசாரிப்பீர்கள் என்றால் 1 அழுத்தவும். இன்றைய நிலையை கேட்க 2. "
                           "செவிலியருடன் பேச 3 அழுத்தவும்.")
        pron = "He" if male else "She"
        head = (f"Namaste {g}, this is SpiroBuddy's automated care assistant, calling from the hospital "
                f"about {who}, {fn}. "
                + (f"{who} has asked for help, and the nurse has been told. " if red else
                   f"{pron} has missed {missed} breathing sessions in a row and did not answer our reminder. "))
        return head + ("Press 1 if you will check on them now. Press 2 to hear today's progress. "
                       "Press 3 to talk to the nurse.")
    # patient reminder
    if lang == "hi":
        return (f"नमस्ते {fn} जी, यह स्पाइरो-बडी की स्वचालित देखभाल सहायक है, अस्पताल की ओर से। "
                f"आपके साँस के व्यायाम का समय हो गया है: दस धीमी, गहरी साँसें। "
                f"अगर आपने कर लिया है तो 1 दबाइए। 15 मिनट बाद याद दिलाने के लिए 2 दबाइए। "
                f"नर्स से बात करने के लिए 3 दबाइए।")
    if lang == "ta":
        t = "அம்மா" if not male else "ஐயா"
        return (f"வணக்கம் {fn} {t}, இது ஸ்பைரோபடியின் தானியங்கி பராமரிப்பு உதவியாளர், மருத்துவமனையிலிருந்து. "
                f"உங்கள் மூச்சுப் பயிற்சி நேரம்: பத்து மெதுவான, ஆழ்ந்த மூச்சுகள். "
                f"முடித்திருந்தால் 1 அழுத்தவும். 15 நிமிடத்தில் நினைவூட்ட 2 அழுத்தவும். "
                f"செவிலியருடன் பேச 3 அழுத்தவும்.")
    return (f"Namaste {fn} ji, this is SpiroBuddy's automated care assistant, calling from the hospital. "
            f"It is time for your breathing exercise: ten slow, deep breaths. "
            f"Press 1 if you have done it. Press 2 to be reminded in 15 minutes. "
            f"Press 3 to talk to your nurse.")


AFTER = {
    ("patient", "1"): {"en": "Shabash! Thank you. Your SpiroBuddy will count the breaths. Goodbye.",
                       "hi": "शाबाश! धन्यवाद। आपका स्पाइरो-बडी साँसें गिन लेगा। नमस्ते।",
                       "ta": "சபாஷ்! நன்றி. உங்கள் ஸ்பைரோபடி மூச்சுகளை எண்ணும். வணக்கம்."},
    ("patient", "2"): {"en": "Okay. I will remind you again in 15 minutes. Goodbye.",
                       "hi": "ठीक है। 15 मिनट बाद मैं फिर याद दिलाऊँगा। नमस्ते।",
                       "ta": "சரி. 15 நிமிடத்தில் மீண்டும் நினைவூட்டுகிறேன். வணக்கம்."},
    ("patient", "3"): {"en": "Okay. Your nurse will call you back very soon. If it is an emergency, call 112.",
                       "hi": "ठीक है। आपकी नर्स जल्द ही आपको कॉल करेंगी। आपातकाल हो तो 112 पर कॉल करें।",
                       "ta": "சரி. உங்கள் செவிலியர் விரைவில் அழைப்பார். அவசரம் என்றால் 112 ஐ அழைக்கவும்."},
    ("guardian", "1"): {"en": "Thank you. We have noted that you will check on them. Goodbye.",
                        "hi": "धन्यवाद। हमने नोट कर लिया कि आप उनका हाल पूछेंगे। नमस्ते।",
                        "ta": "நன்றி. நீங்கள் விசாரிப்பீர்கள் என்று குறித்துக்கொண்டோம். வணக்கம்."},
    ("guardian", "3"): {"en": "Okay. The nurse will call you back very soon. Goodbye.",
                        "hi": "ठीक है। नर्स जल्द ही आपको कॉल करेंगी। नमस्ते।",
                        "ta": "சரி. செவிலியர் விரைவில் அழைப்பார். வணக்கம்."},
}
NO_INPUT = {"en": "We did not hear a key press. We will try again later. Goodbye.",
            "hi": "हमें कोई बटन दबाने की आवाज़ नहीं मिली। हम बाद में फिर कोशिश करेंगे। नमस्ते।",
            "ta": "எந்த பொத்தானும் அழுத்தப்படவில்லை. பிறகு மீண்டும் முயற்சிப்போம். வணக்கம்."}
CONNECTING = {"en": "Connecting you to your nurse now.", "hi": "आपको अभी नर्स से जोड़ रहे हैं।",
              "ta": "உங்களை இப்போது செவிலியருடன் இணைக்கிறோம்."}


def explain_error(err: str) -> str:
    """Plain-English reason for common provider errors."""
    e = (err or "").lower()
    if "21219" in e or "unverified" in e:
        return "Twilio trial accounts can only call verified numbers (max 5) – verify it or upgrade"
    if "21215" in e or "geo" in e or "permission" in e:
        return "calling India isn't enabled – Twilio Console > Voice > Settings > Geo permissions"
    if "21210" in e or "21212" in e or "caller id" in e or "from" in e and "invalid" in e:
        return "the caller ID (TWILIO_VOICE_FROM) isn't a valid Twilio voice number"
    if "401" in e or "authenticate" in e:
        return "wrong account SID / auth token"
    if "exotel" in e:
        return "Exotel rejected the call – check the ExoPhone, KYC and the app (flow) ID"
    return "the provider rejected the call"


def role_of(call: dict) -> str:
    return "guardian" if call.get("to_role") == "guardian" else "patient"


def nurse_desk_number() -> str | None:
    """Nurse number a call can be put through to (press 3), if configured."""
    from .common import e164
    return e164(env("NURSE_DESK_PHONE")) or e164(env("DEMO_NURSE_PHONE"))


# ----------------------------------------------------------------------------- rows

def public_call(c: dict) -> dict:
    from . import sarvam
    lang = lang_of(c.get("language"), "en")
    created, ring = to_dt(c.get("created_at")), to_dt(c.get("ring_until"))
    meta = c.get("meta") if isinstance(c.get("meta"), dict) else {}
    style = meta.get("style") or "ivr"
    return {"style": style, "result": sarvam.public_result(c), "note": meta.get("note"),
            "answers": (sarvam.ANSWERS[min(int(meta.get("stage") or 0), 1)][lang]
                        if style == "agent" and not meta.get("result") else []),
            "id": c.get("id"), "patient_id": c.get("patient_id"), "run_id": c.get("run_id"),
            "guardian_id": c.get("guardian_id"), "to_role": c.get("to_role"),
            "to_name": c.get("to_name"), "to_number": masked_number(c.get("to_number")),
            "purpose": c.get("purpose"), "provider": c.get("provider"),
            "status": c.get("status"), "digits": c.get("digits"), "outcome": c.get("outcome"),
            "language": lang, "browser_lang": BROWSER_LANG[lang], "script": c.get("script"),
            "audio_url": meta.get("audio_url"),
            "simulated": c.get("provider") == "dry_run",
            "ring_until": iso(ring) if ring else None,
            "created_at": iso(created) if created else None}


def get_call(cid: int) -> dict | None:
    rows = st().select("calls", [("id", "eq", int(cid))])
    return rows[0] if rows else None


def _update(cid: int, **vals) -> None:
    vals["updated_at"] = iso(now())
    st().update("calls", [("id", "eq", int(cid))], vals)


def list_calls(active_only: bool = False, patient_id: int | None = None, limit: int = 30) -> list[dict]:
    f = []
    if patient_id is not None:
        f.append(("patient_id", "eq", int(patient_id)))
    if active_only:
        f.append(("status", "in", list(ACTIVE)))
    rows = st().select("calls", f, order="id", desc=True, limit=limit)
    return [public_call(c) for c in rows]


# ----------------------------------------------------------------------------- placing calls

def place_call(patient: dict, purpose: str, to_role: str, to_name: str, stored_number: str | None,
               lang: str, run_id: int | None = None, guardian: dict | None = None,
               ring_s: int = 30, consent: bool = False, missed: int = 2,
               style: str = "ivr", consent_fresh: bool = True) -> dict | None:
    """Create a call row and ring it (real provider or the browser simulator).
    `consent` must be True (flag + date recorded, common.has_consent) or the call is skipped.
    style="agent" turns the patient's reminder into the conversational AI check-in call.
    Returns the public call, or None when skipped (no consent)."""
    lang = lang_of(lang, "en")
    actor = "guardian" if to_role == "guardian" else "patient"
    kind = "guardian_call" if to_role == "guardian" else "call"
    if not consent:
        log_event(patient["id"], kind, f"Call to {to_name} skipped – no recorded consent for automated calls",
                  detail="Record consent (yes + date) in Care circle settings before any automated call "
                         "(TRAI 2026 A2P rules, Twilio India guidelines, DPDP Act).",
                  channel="call", actor=actor, to_name=to_name, status="skipped", run_id=run_id)
        return None
    if to_role == "patient" and purpose == "reminder" and style == "agent":
        return _place_checkin(patient, to_name, stored_number, lang, run_id, ring_s, missed,
                              consent_fresh)
    script = menu_text(purpose, patient, lang, guardian, missed)
    prov, note = provider()
    if prov != "dry_run" and not consent_fresh:
        prov, note = "dry_run", "consent is older than 7 days (TRAI 'ongoing use' rule) – real call blocked until the person says yes again; simulator only"
    number = resolve_number(stored_number, "guardian" if to_role == "guardian" else "patient")
    if prov != "dry_run" and not number:
        prov, note = "dry_run", "no real number for this person (demo placeholder) – simulator only"
    t = now()
    audio_url = audio.tts_url(script, lang)
    row = {"patient_id": patient["id"], "run_id": run_id,
           "guardian_id": (guardian or {}).get("id"), "to_role": to_role, "to_name": to_name,
           "to_number": number, "purpose": purpose, "provider": prov,
           "provider_sid": None, "status": "ringing" if prov == "dry_run" else "queued",
           "digits": None, "outcome": None, "language": lang, "script": script,
           "meta": {"audio_url": audio_url, "note": note, "missed": missed,
                    "stored_number": stored_number},
           "ring_until": iso(t + timedelta(seconds=ring_s)), "created_at": iso(t),
           "updated_at": iso(t)}
    call = st().insert("calls", [row])[0]
    cid = call["id"]
    err = None
    if prov == "twilio":
        err = _twilio_call(cid, number, ring_s)
    elif prov == "exotel":
        err = _exotel_call(cid, number, ring_s)
    if err:
        # Real call failed (trial limits, foreign caller ID, wrong number…): never lose the step –
        # ring the browser phone simulator instead and say why ("would call").
        reason = explain_error(err)
        _update(cid, provider="dry_run", status="ringing",
                ring_until=iso(now() + timedelta(seconds=ring_s)),
                meta={**row["meta"], "error": err, "note": f"real call failed: {reason}"})
        log_event(patient["id"], kind,
                  f"Real call to {to_name} failed ({prov}) – would call; ringing in the phone simulator instead",
                  detail=f"{reason} – {err}", channel="call", actor=actor, to_name=to_name,
                  status="failed", run_id=run_id, ref_id=cid)
        return public_call(get_call(cid) or call)
    label = {"dry_run": "ringing in the phone simulator (dry run)", "twilio": "via Twilio",
             "exotel": "via Exotel"}[prov]
    if prov == "twilio" and number and number.startswith("+91"):
        label += " (international caller ID – Twilio India rule)"
    log_event(patient["id"], kind, f"Automated call to {to_name} – {label}",
              detail=script, channel="call", actor=actor, to_name=to_name,
              status="dry_run" if prov == "dry_run" else "sent", run_id=run_id, ref_id=cid)
    return public_call(get_call(cid) or call)


def _place_checkin(patient: dict, to_name: str, stored_number: str | None, lang: str,
                   run_id: int | None, ring_s: int, missed: int,
                   consent_fresh: bool = True) -> dict:
    """Conversational AI check-in call: Sarvam Voice Agent, or the browser simulator."""
    from . import sarvam
    script = sarvam.greeting(patient, lang, missed)
    prov, note = provider("checkin")
    if prov != "dry_run" and not consent_fresh:
        prov, note = "dry_run", "consent is older than 7 days (TRAI 'ongoing use' rule) – real call blocked until the person says yes again; simulator only"
    number = resolve_number(stored_number, "patient")
    if prov != "dry_run" and not number:
        prov, note = "dry_run", "no real number for this person (demo placeholder) – simulator only"
    t = now()
    row = {"patient_id": patient["id"], "run_id": run_id, "guardian_id": None, "to_role": "patient",
           "to_name": to_name, "to_number": number, "purpose": "checkin",
           "provider": prov, "provider_sid": None,
           "status": "ringing" if prov == "dry_run" else "queued", "digits": None, "outcome": None,
           "language": lang, "script": script,
           "meta": {"style": "agent", "note": note, "missed": missed, "stage": 0,
                    "stored_number": stored_number,
                    "result_pending": True, "audio_url": audio.tts_url(script, lang)},
           "ring_until": iso(t + timedelta(seconds=ring_s if prov == "dry_run" else 90)),
           "created_at": iso(t), "updated_at": iso(t)}
    call = st().insert("calls", [row])[0]
    if prov == "sarvam_agent":
        err = sarvam.place(call, patient, number, lang, missed)
        if err:
            _update(call["id"], provider="dry_run", status="ringing",
                    ring_until=iso(now() + timedelta(seconds=ring_s)),
                    meta={**row["meta"], "error": err, "note": f"Sarvam call failed: {err[:120]}"})
            log_event(patient["id"], "call",
                      f"Sarvam AI call to {to_name} failed – would call; ringing in the phone simulator instead",
                      detail=err, channel="call", actor="patient", to_name=to_name, status="failed",
                      run_id=run_id, ref_id=call["id"])
            return public_call(get_call(call["id"]) or call)
    label = ("via Sarvam Voice Agent – result pending until Sarvam's webhook arrives"
             if prov == "sarvam_agent" else "ringing in the phone simulator (AI conversation, dry run)")
    log_event(patient["id"], "call", f"AI check-in call to {to_name} – {label}", detail=script,
              channel="call", actor="patient", to_name=to_name,
              status="sent" if prov == "sarvam_agent" else "dry_run", run_id=run_id, ref_id=call["id"])
    return public_call(get_call(call["id"]) or call)


def _twilio_client():
    from twilio.rest import Client
    return Client(env("TWILIO_ACCOUNT_SID"), env("TWILIO_AUTH_TOKEN"))


def _twilio_call(cid: int, number: str, ring_s: int) -> str | None:
    base = public_base()
    try:
        c = _twilio_client().calls.create(
            to=number, from_=env("TWILIO_VOICE_FROM"),
            url=f"{base}/api/comms/twilio/voice/{cid}", method="POST",
            status_callback=f"{base}/api/comms/twilio/status/{cid}",
            status_callback_event=["initiated", "ringing", "answered", "completed"],
            status_callback_method="POST", timeout=ring_s)
        _update(cid, provider_sid=c.sid)
        return None
    except Exception as e:
        log.warning("Twilio call failed: %s", e)
        return str(e)[:300]


def _exotel_base() -> str:
    sub = env("EXOTEL_SUBDOMAIN", "api.exotel.com")
    return f"https://{sub}/v1/Accounts/{env('EXOTEL_SID')}"


def _exotel_status_url(cid: int) -> str:
    return f"{public_base()}/api/comms/exotel/status/{cid}?" + urlencode(
        {"token": env("EXOTEL_WEBHOOK_SECRET")})


def _exotel_call(cid: int, number: str, ring_s: int) -> str | None:
    """Exotel 'connect a number to a call flow': the flow's Greeting/Gather/Passthru applets
    call our /api/comms/exotel/* endpoints with CustomField=<call id>."""
    import httpx
    if not env("EXOTEL_WEBHOOK_SECRET"):
        return "Exotel callback authentication is not configured"
    base = public_base()
    data = {"From": number, "CallerId": env("EXOTEL_CALLER_ID"),
            "Url": f"http://my.exotel.com/{env('EXOTEL_SID')}/exoml/start_voice/{env('EXOTEL_APP_ID')}",
            "CallType": "trans", "TimeLimit": "300", "TimeOut": str(ring_s),
            "CustomField": str(cid),
            "StatusCallback": _exotel_status_url(cid)}
    try:
        r = httpx.post(f"{_exotel_base()}/Calls/connect.json", data=data,
                       auth=(env("EXOTEL_API_KEY"), env("EXOTEL_API_TOKEN")), timeout=15)
        if r.status_code >= 400:
            return f"Exotel {r.status_code}: {r.text[:200]}"
        sid = ((r.json() or {}).get("Call") or {}).get("Sid")
        _update(cid, provider_sid=sid)
        return None
    except Exception as e:
        log.warning("Exotel call failed: %s", e)
        return str(e)[:300]


# ----------------------------------------------------------------------------- call progress

def answer(cid: int, source: str = "simulator") -> dict | None:
    c = get_call(cid)
    if not c:
        return None
    if c.get("status") in FINAL:
        return public_call(c)
    _update(cid, status="in-progress")
    log_event(c["patient_id"], "call_answered", f"{c.get('to_name')} answered the call",
              detail=f"via {source}", channel="call", actor=role_of(c), to_name=c.get("to_name"),
              status="ok", run_id=c.get("run_id"), ref_id=cid)
    return public_call({**c, "status": "in-progress"})


def press(cid: int, digit: str, source: str = "simulator") -> dict:
    """A keypress (real Gather webhook or the simulator). Drives the same ladder logic.
    -> {say, language, audio_url, end, dial, call}"""
    from . import escalation, messages
    c = get_call(cid)
    if not c:
        raise KeyError(cid)
    digit = str(digit or "").strip()[:1]
    lang = lang_of(c.get("language"), "en")
    role = role_of(c)
    patient_id = c["patient_id"]
    from .common import patient as get_patient
    patient = get_patient(patient_id) or {"id": patient_id, "name": c.get("to_name") or ""}
    guardian = None
    if c.get("guardian_id"):
        from .guardians import get_guardian
        guardian = get_guardian(c["guardian_id"])
    log_event(patient_id, "keypress", f"{c.get('to_name')} pressed {digit or 'nothing'}",
              detail=f"via {source}", channel="call", actor=role, to_name=c.get("to_name"),
              status="ok", run_id=c.get("run_id"), ref_id=cid)
    dial = None
    end = True
    if role == "patient" and digit in ("1", "2", "3"):
        intent = {"1": "done", "2": "snooze", "3": "call_me"}[digit]
        escalation.patient_response(patient_id, intent, source=f"call keypress ({source})")
        say = AFTER[("patient", digit)][lang]
        if digit == "3" and c.get("provider") != "dry_run" and nurse_desk_number():
            dial, say = nurse_desk_number(), CONNECTING[lang]
        outcome = intent
    elif role == "guardian" and digit in ("1", "3"):
        intent = "guardian_ack" if digit == "1" else "nurse"
        escalation.guardian_response(patient_id, guardian, intent, source=f"call keypress ({source})")
        say = AFTER[("guardian", digit)][lang]
        if digit == "3" and c.get("provider") != "dry_run" and nurse_desk_number():
            dial, say = nurse_desk_number(), CONNECTING[lang]
        outcome = intent
    elif role == "guardian" and digit == "2":
        say = messages.status_text(patient_id, lang, guardian).replace("📊 ", "").replace(" 🔥", "") \
            + " " + menu_tail(lang)
        end = False
        outcome = "status"
    else:
        say = NO_INPUT[lang]
        outcome = "no_input"
    vals = {"digits": ((c.get("digits") or "") + digit)[-10:], "outcome": outcome}
    if end:
        vals["status"] = "completed"
    _update(cid, **vals)
    return {"say": say, "language": lang, "browser_lang": BROWSER_LANG[lang],
            "audio_url": audio.tts_url(say, lang), "end": end, "dial": dial,
            "call": public_call({**c, **vals})}


def menu_tail(lang: str) -> str:
    return {"en": "Press 1 if you will check on them now. Press 3 to talk to the nurse.",
            "hi": "अगर आप अभी उनका हाल पूछेंगे तो 1 दबाइए। नर्स से बात करने के लिए 3 दबाइए।",
            "ta": "இப்போது விசாரிப்பீர்கள் என்றால் 1. செவிலியருடன் பேச 3 அழுத்தவும்."}[lang]


def finish(cid: int, status: str, source: str = "provider") -> dict | None:
    """Final status from a provider callback or the simulator (declined / timed out)."""
    from . import escalation
    c = get_call(cid)
    if not c:
        return None
    if c.get("status") in FINAL and c.get("status") != "completed":
        return public_call(c)
    status = status if status in FINAL else "completed"
    vals = {"status": status}
    if status in ("no-answer", "busy", "failed", "canceled"):
        vals["outcome"] = "no_answer"
    elif not c.get("outcome"):
        vals["outcome"] = "no_input"
    already_final = c.get("status") == "completed"
    _update(cid, **vals)
    if not already_final and vals.get("outcome") in ("no_answer", "no_input"):
        what = "did not answer" if vals["outcome"] == "no_answer" else "answered but pressed no key"
        log_event(c["patient_id"], "no_answer", f"{c.get('to_name')} {what}",
                  detail=f"{status} via {source}", channel="call", actor=role_of(c),
                  to_name=c.get("to_name"), status="warn", run_id=c.get("run_id"), ref_id=cid)
        escalation.on_call_unanswered(c)
    return public_call({**c, **vals})


def expire_simulated() -> int:
    """Simulator calls nobody picked up -> no-answer; answered ones idle > 90 s -> completed."""
    t = now()
    n = 0
    for c in st().select("calls", [("provider", "eq", "dry_run"), ("status", "in", ["ringing", "in-progress"])]):
        ring = to_dt(c.get("ring_until"))
        if c["status"] == "ringing" and ring and ring <= t:
            finish(c["id"], "no-answer", "simulator (nobody picked up)")
            n += 1
        elif c["status"] == "in-progress":
            upd = to_dt(c.get("updated_at"))
            if upd and (t - upd).total_seconds() > 90:
                if isinstance(c.get("meta"), dict) and c["meta"].get("style") == "agent":
                    from . import sarvam
                    sarvam.sim_finish(c["id"], "simulator (no reply for 90 s)")
                else:
                    finish(c["id"], "completed", "simulator (hung up)")
                n += 1
    return n


# ----------------------------------------------------------------------------- TwiML

def twiml_menu(c: dict, retry: bool = False) -> str:
    from twilio.twiml.voice_response import Gather, VoiceResponse
    base = public_base()
    lang = lang_of(c.get("language"), "en")
    language, voice = SAY_VOICE[lang]
    audio_abs = audio.tts_url(c.get("script") or "", lang, absolute=True, phone=True)
    r = VoiceResponse()
    g = Gather(input="dtmf", num_digits=1, timeout=7, method="POST",
               action=f"{base}/api/comms/twilio/gather/{c['id']}")
    if audio_abs:
        g.play(audio_abs)
    else:
        g.say(c.get("script") or "", language=language, voice=voice)
    r.append(g)
    if not retry:
        r.redirect(f"{base}/api/comms/twilio/voice/{c['id']}?retry=1", method="POST")
    else:
        r.say(NO_INPUT[lang], language=language, voice=voice)
        r.hangup()
    return str(r)


def twiml_after(result: dict) -> str:
    from twilio.twiml.voice_response import Gather, VoiceResponse
    lang = result["language"]
    language, voice = SAY_VOICE[lang]
    r = VoiceResponse()
    audio_abs = audio.tts_url(result.get("say") or "", lang, absolute=True, phone=True)
    if not result.get("end"):
        g = Gather(input="dtmf", num_digits=1, timeout=7, method="POST",
                   action=f"{public_base()}/api/comms/twilio/gather/{result['call']['id']}")
        g.play(audio_abs) if audio_abs else g.say(result["say"], language=language, voice=voice)
        r.append(g)
        r.say(NO_INPUT[lang], language=language, voice=voice)
        return str(r)
    if audio_abs:
        r.play(audio_abs)
    else:
        r.say(result["say"], language=language, voice=voice)
    if result.get("dial"):
        r.dial(result["dial"], caller_id=env("TWILIO_VOICE_FROM") or None)
    r.hangup()
    return str(r)


TWILIO_STATUS = {"queued": "queued", "initiated": "initiated", "ringing": "ringing",
                 "in-progress": "in-progress", "answered": "in-progress", "completed": "completed",
                 "busy": "busy", "failed": "failed", "no-answer": "no-answer",
                 "canceled": "canceled"}


def provider_status(cid: int, raw: str, source: str) -> dict | None:
    s = TWILIO_STATUS.get((raw or "").lower().replace("_", "-"), None)
    if s is None:
        return None
    c = get_call(cid)
    if not c:
        return None
    if s in FINAL:
        return finish(cid, s, source)
    if s == "in-progress" and c.get("status") != "in-progress":
        return answer(cid, source)
    if s != c.get("status"):
        _update(cid, status=s)
    return public_call({**c, "status": s})


# ----------------------------------------------------------------------------- click-to-call

def click_to_call(patient: dict, nurse_name: str, nurse_phone: str | None, cfg: dict) -> dict:
    """Nurse <-> patient bridge. Real: the provider rings the nurse first, then connects the
    patient (nobody sees the other's personal number). Dry run: logged for the demo."""
    from .common import e164
    t = now()
    nurse_num = (resolve_number(nurse_phone, "nurse") if demo_mode()
                 else e164(nurse_phone) or nurse_desk_number())
    pat_num = resolve_number(cfg.get("patient_phone"), "patient")
    prov, note = provider()
    if prov == "exotel" and (not nurse_num or not pat_num):
        prov = "dry_run"
    if prov == "dry_run" and twilio_ready() and nurse_num and pat_num:
        prov = "twilio"            # inline TwiML needs no public webhook
    elif prov == "twilio" and (not nurse_num or not pat_num):
        prov = "dry_run"
    if prov == "dry_run":
        note = ("no call keys" if not (twilio_ready() or exotel_ready())
                else "missing a real nurse or patient number – set NURSE_DESK_PHONE / the patient's phone")
    lang = lang_of(patient.get("language"), "en")
    row = {"patient_id": patient["id"], "run_id": None, "guardian_id": None,
           "to_role": "patient", "to_name": patient["name"],
           "to_number": pat_num, "purpose": "nurse_bridge",
           "provider": prov, "provider_sid": None,
           "status": "completed" if prov == "dry_run" else "queued", "digits": None,
           "outcome": "dry_run" if prov == "dry_run" else None, "language": lang,
           "script": f"{nurse_name} → {patient['name']}", "meta": {"nurse": nurse_name,
                "note": note, "stored_number": cfg.get("patient_phone"),
                "stored_nurse_number": nurse_phone, "nurse_destination": nurse_num},
           "ring_until": None, "created_at": iso(t), "updated_at": iso(t)}
    call = st().insert("calls", [row])[0]
    err = None
    if prov == "twilio":
        try:
            from twilio.twiml.voice_response import VoiceResponse
            vr = VoiceResponse()
            vr.say(f"SpiroBuddy. Connecting you to {patient['name']}.", language="en-IN",
                   voice="Polly.Aditi")
            vr.dial(pat_num, caller_id=env("TWILIO_VOICE_FROM"))
            kw = {"to": nurse_num, "from_": env("TWILIO_VOICE_FROM"), "twiml": str(vr)}
            if public_base():
                kw.update(status_callback=f"{public_base()}/api/comms/twilio/status/{call['id']}",
                          status_callback_event=["answered", "completed"])
            c = _twilio_client().calls.create(**kw)
            _update(call["id"], provider_sid=c.sid)
        except Exception as e:
            err = str(e)[:300]
    elif prov == "exotel":
        import httpx
        try:
            data = {"From": nurse_num, "To": pat_num, "CallerId": env("EXOTEL_CALLER_ID"),
                    "CallType": "trans", "CustomField": str(call["id"])}
            if public_base():
                data["StatusCallback"] = _exotel_status_url(call['id'])
            r = httpx.post(f"{_exotel_base()}/Calls/connect.json", data=data,
                           auth=(env("EXOTEL_API_KEY"), env("EXOTEL_API_TOKEN")), timeout=15)
            if r.status_code >= 400:
                err = f"Exotel {r.status_code}: {r.text[:200]}"
        except Exception as e:
            err = str(e)[:300]
    if err:
        _update(call["id"], status="failed", outcome="provider_error")
    status = "failed" if err else ("dry_run" if prov == "dry_run" else "sent")
    title = {"dry_run": f"{nurse_name} pressed Call patient – dry run (would ring the nurse, then connect {first_name(patient['name'])})",
             "twilio": f"{nurse_name} is calling {first_name(patient['name'])} via Twilio (nurse's phone rings first)",
             "exotel": f"{nurse_name} is calling {first_name(patient['name'])} via Exotel (nurse's phone rings first)"}[prov]
    log_event(patient["id"], "click_to_call", title if not err else f"Click-to-call failed ({prov})",
              detail=err or note, channel="call", actor="nurse", to_name=nurse_name,
              status=status, ref_id=call["id"])
    out = public_call(get_call(call["id"]) or call)
    out.update({"dry_run": prov == "dry_run", "note": note, "error": err})
    return out
