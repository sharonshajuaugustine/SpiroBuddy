"""Sarvam Voice Agent check-in call ("Are you okay? Why did you miss it?") – provider `sarvam_agent`.

Verified against docs.sarvam.ai on 9 Oct 2026 (docs/COMMS.md §5 lists the URLs):
  - Create:  POST https://apps.sarvam.ai/api/outbounds/v1/orgs/{org_id}/workspaces/{workspace_id}/outbounds
             header `X-API-Key`; body {app_config:{app_id, app_version, connection_config:
             {connection_id, agent_phone_number}, agent_variables, app_overrides:
             {initial_language_name}}, user_config:{user_phone_number}, webhook_config:{url, metadata}}
             -> {attempt_id}
  - Webhook: POST to webhook_config.url after the attempt: {attempt_id, status: connected|no_answer|
             busy|failed, channel_info, duration, interaction_id, failure_reason,
             final_agent_variables, webhook_config (echoed, with our metadata),
             interaction_transcript:[{role: agent|user, en_text}]}
  - No webhook signature is documented, so we put our own secret in the URL (?token=...) and only
    accept attempts we placed ourselves. Sarvam DTMF (keypad) input is still "planned" -> spoken answers.

Safety: the provider's text is never trusted for medical meaning. The red flag is decided by OUR
fixed word list (voice.red_flag on the patient's own words); the note to the nurse is a neutral
template ("Patient reported … Nurse review requested."). Sentiment, if the agent sends it, is shown
only as "possible distress – nurse to review" (low confidence). Nothing here diagnoses.

The browser phone simulator runs the same conversation (sim_turn) and its result goes through the
same normalise() + apply_result() as a real webhook.
"""
from __future__ import annotations

import hmac
import json
import logging
import re
import threading
import uuid
from datetime import timedelta
from pathlib import Path

from ..config import demo_mode, env, iso
from .common import (DISCLOSURE, first_name, lang_of, log_event, now, patient, public_base, st,
                     to_dt)

log = logging.getLogger("spirobuddy.comms.sarvam")

SAMPLES_FILE = Path(__file__).resolve().parent / "samples" / "sarvam_webhooks.json"
API_BASE_DEFAULT = "https://apps.sarvam.ai/api/outbounds"
_lock = threading.RLock()

# Sarvam `initial_language_name` values (from the Create outbound call reference)
SARVAM_LANG = {"en": "English", "hi": "Hindi", "bn": "Bengali", "ta": "Tamil", "te": "Telugu",
               "kn": "Kannada", "ml": "Malayalam", "mr": "Marathi", "gu": "Gujarati",
               "pa": "Punjabi", "or": "Odia"}
REASONS = ("pain", "breathing", "cough", "tired_unwell", "forgot", "busy_away", "device_problem",
           "feeling_fine", "other")
REASON_LABEL = {"pain": "pain", "breathing": "breathing difficulty", "cough": "cough",
                "tired_unwell": "feeling tired or unwell", "forgot": "forgot",
                "busy_away": "busy or away", "device_problem": "a problem with the device",
                "feeling_fine": "feeling fine", "other": "other reason"}
OUTCOME_LABEL = {"ok": "Patient answered – no concern raised", "needs_nurse_review": "Nurse review requested",
                 "red_flag": "RED FLAG – fixed 112 message given", "no_answer": "No answer",
                 "failed": "Call failed", "unclear": "Answer unclear – nurse review requested"}
NUM_WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


# ----------------------------------------------------------------------------- settings

def api_key() -> str:
    return env("SARVAM_AGENT_API_KEY") or env("SARVAM_API_KEY")


def ready() -> bool:
    """All the settings a real Sarvam outbound call needs (docs/COMMS.md §5)."""
    return bool(api_key() and env("SARVAM_ORG_ID") and env("SARVAM_WORKSPACE_ID")
                and env("SARVAM_AGENT_ID") and env("SARVAM_CONNECTION_ID")
                and env("SARVAM_AGENT_NUMBER"))


def missing() -> list[str]:
    need = {"SARVAM_AGENT_API_KEY (or SARVAM_API_KEY)": api_key(), "SARVAM_ORG_ID": env("SARVAM_ORG_ID"),
            "SARVAM_WORKSPACE_ID": env("SARVAM_WORKSPACE_ID"), "SARVAM_AGENT_ID": env("SARVAM_AGENT_ID"),
            "SARVAM_CONNECTION_ID": env("SARVAM_CONNECTION_ID"),
            "SARVAM_AGENT_NUMBER": env("SARVAM_AGENT_NUMBER")}
    out = [k for k, v in need.items() if not v]
    if not public_base():
        out.append("PUBLIC_BASE_URL")
    return out


def webhook_url() -> str | None:
    base = public_base()
    if not base:
        return None
    secret = env("SARVAM_WEBHOOK_SECRET")
    return f"{base}/api/comms/webhooks/sarvam" + (f"?token={secret}" if secret else "")


def check_token(token: str | None) -> bool:
    """Our own shared secret (Sarvam documents no signature). Without a secret configured we
    only accept webhooks in DEMO mode (and only for attempts we placed – checked later)."""
    secret = env("SARVAM_WEBHOOK_SECRET")
    if not secret:
        return demo_mode()
    return bool(token) and hmac.compare_digest(str(token), secret)


def voice_lang(pid: int, fallback: str) -> str:
    """The patient's voice language (11 languages, docs/VOICE.md) – falls back to the profile."""
    try:
        from ..routes_voice import get_prefs
        return get_prefs(int(pid)).get("language") or fallback
    except Exception:
        return fallback


# ----------------------------------------------------------------------------- the conversation

AGENT_LINES = {
    "greeting": {
        "en": "{d} Calling from the hospital. {n} ji, we noticed you missed your breathing exercise {m} times. Are you okay, and would you like to tell me why?",
        "hi": "{d} अस्पताल की ओर से। {n} जी, हमने देखा कि आपका साँस का व्यायाम {m} बार छूट गया है। क्या आप ठीक हैं? क्या आप बताना चाहेंगे कि क्यों छूटा?",
        "ta": "{d} மருத்துவமனையிலிருந்து அழைக்கிறோம். {n}, உங்கள் மூச்சுப் பயிற்சி {m} முறை தவறியது. நீங்கள் நலமா? ஏன் தவறியது என்று சொல்ல விரும்புகிறீர்களா?",
    },
    "ack_concern": {
        "en": "Thank you for telling me. I will pass that to your care team. If the pain is severe, new, or you feel breathless, please seek urgent help. Would you like your nurse to call you back? Please say yes or no.",
        "hi": "बताने के लिए धन्यवाद। मैं यह आपकी देखभाल टीम तक पहुँचा दूँगी। अगर दर्द तेज़ या नया हो, या साँस फूले, तो तुरंत मदद लें। क्या आप चाहेंगे कि नर्स आपको वापस कॉल करें? हाँ या ना कहिए।",
        "ta": "சொன்னதற்கு நன்றி. இதை உங்கள் பராமரிப்புக் குழுவிடம் தெரிவிக்கிறேன். வலி கடுமையாக அல்லது புதிதாக இருந்தால், அல்லது மூச்சுத் திணறினால், உடனே உதவி பெறுங்கள். செவிலியர் உங்களை மீண்டும் அழைக்க வேண்டுமா? ஆம் அல்லது இல்லை என்று சொல்லுங்கள்.",
    },
    "ack_ok": {
        "en": "Thank you, that's good to hear. Would you like your nurse to call you back? Please say yes or no.",
        "hi": "धन्यवाद, यह सुनकर अच्छा लगा। क्या आप चाहेंगे कि नर्स आपको वापस कॉल करें? हाँ या ना कहिए।",
        "ta": "நன்றி, கேட்க மகிழ்ச்சி. செவிலியர் உங்களை மீண்டும் அழைக்க வேண்டுமா? ஆம் அல்லது இல்லை என்று சொல்லுங்கள்.",
    },
    "bye_callback": {
        "en": "Your callback request has been sent to your care team for review. If you need urgent help, contact your care team directly or call 112 in an emergency. Goodbye.",
        "hi": "आपकी वापस कॉल करने की विनती देखभाल टीम को समीक्षा के लिए भेज दी गई है। तुरंत मदद चाहिए तो अपनी देखभाल टीम से सीधे संपर्क करें, या आपातकाल में 112 पर कॉल करें। नमस्ते।",
        "ta": "உங்களை மீண்டும் அழைக்குமாறு கேட்ட கோரிக்கை பராமரிப்புக் குழுவின் ஆய்வுக்கு அனுப்பப்பட்டுள்ளது. உடனடி உதவி தேவைப்பட்டால் பராமரிப்புக் குழுவை நேரடியாகத் தொடர்புகொள்ளுங்கள் அல்லது அவசரத்தில் 112 ஐ அழையுங்கள். வணக்கம்.",
    },
    "bye_ok": {
        "en": "Thank you. Your response has been recorded. If you need help, contact your care team directly or call 112 in an emergency. Goodbye.",
        "hi": "धन्यवाद। आपका जवाब दर्ज कर लिया गया है। मदद चाहिए तो अपनी देखभाल टीम से सीधे संपर्क करें, या आपातकाल में 112 पर कॉल करें। नमस्ते।",
        "ta": "நன்றி. உங்கள் பதில் பதிவு செய்யப்பட்டுள்ளது. உதவி தேவைப்பட்டால் பராமரிப்புக் குழுவை நேரடியாகத் தொடர்புகொள்ளுங்கள் அல்லது அவசரத்தில் 112 ஐ அழையுங்கள். வணக்கம்.",
    },
    "red_tail": {
        "en": "I am telling your nurse right away.",
        "hi": "मैं अभी आपकी नर्स को बता रही हूँ।",
        "ta": "உடனே உங்கள் செவிலியருக்குத் தெரிவிக்கிறேன்.",
    },
    "repeat": {
        "en": "Sorry, I did not hear you. Are you okay, and why was the exercise missed?",
        "hi": "माफ़ कीजिए, मैं सुन नहीं पाई। क्या आप ठीक हैं, और व्यायाम क्यों छूटा?",
        "ta": "மன்னிக்கவும், கேட்கவில்லை. நீங்கள் நலமா, பயிற்சி ஏன் தவறியது?",
    },
}
# Pre-written answers the presenter can tap in the browser phone simulator (one question at a time).
ANSWERS = {
    0: {"en": ["I had mild pain near the incision this morning.", "I forgot. I will do it now.",
               "I can't breathe properly."],
        "hi": ["आज सुबह टांकों के पास हल्का दर्द था।", "मैं भूल गया था, अभी करता हूँ।",
               "मुझे ठीक से साँस नहीं आ रही।"],
        "ta": ["இன்று காலை தையல் அருகே லேசான வலி இருந்தது.", "மறந்துவிட்டேன், இப்போது செய்கிறேன்.",
               "எனக்கு மூச்சு விட முடியவில்லை."]},
    1: {"en": ["Yes, please call me.", "No, I am fine."],
        "hi": ["हाँ, कॉल कीजिए।", "नहीं, मैं ठीक हूँ।"],
        "ta": ["ஆம், அழையுங்கள்.", "இல்லை, நான் நலம்."]},
}


def line(key: str, lang: str, **kw) -> str:
    lang = lang_of(lang, "en")
    return AGENT_LINES[key][lang].format(**kw)


def greeting(p: dict, lang: str, missed: int) -> str:
    lang = lang_of(lang, "en")
    return line("greeting", lang, d=DISCLOSURE[lang], n=first_name(p.get("name")), m=missed)


# ----------------------------------------------------------------------------- deterministic rules

_REASON_RX = [
    ("pain", r"pain|hurt|ache|sore|incision|stitch|wound|dard|दर्द|टांक|टाँक|घाव|வலி|தையல்|காயம்"),
    ("breathing", r"breathless|hard to breathe|short of breath|out of breath|saans ph|sans ph|"
                  r"साँस फूल|सांस फूल|साँस लेने में|सांस लेने में|மூச்சுத் திணற|மூச்சு திணற"),
    ("cough", r"cough|khansi|खांसी|खाँसी|இருமல்"),
    ("tired_unwell", r"tired|weak|unwell|sick|not well|sleep|thak|कमज़ोर|कमजोर|थक|नींद|சோர்வ|தூக்க|உடம்பு சரியில்லை"),
    ("device_problem", r"device|machine|broken|not working|battery|spirometer|मशीन|खराब|கருவி|வேலை செய்யவில்லை"),
    ("forgot", r"forgot|forget|bhool|भूल|மறந்"),
    ("busy_away", r"busy|out|away|travel|visitor|guest|market|bahar|बाहर|व्यस्त|மும்முரம்|வெளியே"),
    ("feeling_fine", r"fine|ok|okay|good|theek|ठीक|நலம|சரி|பரவாயில்லை"),
]
YES_WORDS = {"yes", "yeah", "yep", "please", "sure", "ok", "okay", "haan", "han", "ha", "ji",
             "हाँ", "हां", "जी", "ஆம்", "ஆமாம்"}
NO_WORDS = {"no", "nope", "nahi", "nahin", "नहीं", "ना", "இல்லை", "வேண்டாம்"}
YES_PHRASES = ("call me", "please call", "कॉल कीजिए", "कॉल करें", "அழையுங்கள்", "அழைக்கவும்")
NO_PHRASES = ("i am fine", "i'm fine", "not needed", "no need", "ज़रूरत नहीं", "जरूरत नहीं", "தேவையில்லை")
CONCERN = ("pain", "breathing", "cough", "tired_unwell", "device_problem")


def classify_reason(words: str) -> str:
    t = (words or "").lower()
    for reason, rx in _REASON_RX:
        if re.search(rx, t, re.I):
            return reason
    return "other"


def yes_no(text: str) -> bool | None:
    """Spoken yes/no in en/hi/ta (first word, then common phrases). None = unclear."""
    t = (text or "").strip().lower()
    first = re.split(r"[\s,.!?।]+", t)[0] if t else ""
    if first in NO_WORDS or any(ph in t for ph in NO_PHRASES):
        return False
    if first in YES_WORDS or any(ph in t for ph in YES_PHRASES):
        return True
    return None


def red_flag_words(text: str) -> bool:
    """Our fixed red-flag list (voice.red_flag, 11 languages) + the WhatsApp list. Never the AI."""
    from .audio import red_flag as voice_red_flag
    from .messages import RED_FLAG_RE
    t = text or ""
    if voice_red_flag(t):
        return True
    # the WhatsApp list includes bare "help"; on a call "help" alone is too broad, so drop it here
    m = RED_FLAG_RE.search(t)
    return bool(m and m.group(0).lower() != "help")


def _truthy(v) -> bool | None:
    if isinstance(v, bool):
        return v
    s = str(v or "").strip().lower()
    if s in ("yes", "y", "true", "1", "requested", "haan", "हाँ"):
        return True
    if s in ("no", "n", "false", "0", "not_requested", "nahi", "नहीं"):
        return False
    return None


def neutral_note(outcome: str, words: str, missed: int, reason: str, callback: bool) -> str:
    w = (words or "").strip().rstrip(".!?। ")
    q = f"“{w}”" if w else "no clear reason"
    n = NUM_WORD.get(int(missed or 0), str(missed))
    if outcome == "red_flag":
        return (f"Patient reported {q} and missed {n} sessions. Red-flag words matched SpiroBuddy's "
                f"fixed list; the fixed 'contact your nurse / call 112' message was given. "
                f"Urgent nurse review requested.")
    if outcome == "needs_nurse_review":
        why = "" if reason in CONCERN else " The patient asked for a call-back."
        return f"Patient reported {q} and missed {n} sessions.{why} Nurse review requested."
    if outcome == "unclear":
        return f"The check-in call connected but the answer was unclear ({q}). Missed {n} sessions. Nurse review requested."
    if outcome == "ok":
        return f"Patient reported {q} and missed {n} sessions. No concern raised and no call-back requested."
    return f"Check-in call: {OUTCOME_LABEL.get(outcome, outcome)}. Missed {n} sessions."


def normalise(payload: dict, call: dict | None = None, provider: str = "sarvam") -> dict:
    """Sarvam webhook (or the simulator's equivalent) -> SpiroBuddy's fixed outcome schema:
    {provider, status, outcome, reason_category, patient_words, neutral_note, red_flag,
     callback_requested, transcript_reference, possible_distress, red_flag_rule, attempt_id}"""
    payload = payload or {}
    raw = str(payload.get("status") or "").lower()
    status = {"connected": "completed", "completed": "completed", "no_answer": "no-answer",
              "no-answer": "no-answer", "busy": "busy", "failed": "failed"}.get(raw, "failed")
    fav = payload.get("final_agent_variables") or {}
    if not isinstance(fav, dict):
        fav = {}
    turns = payload.get("interaction_transcript") or []
    user_turns = [str(t.get("en_text") or t.get("text") or "") for t in turns
                  if isinstance(t, dict) and t.get("role") == "user"]
    words = str(fav.get("patient_words") or "").strip() or (user_turns[0] if user_turns else "")
    meta = (call or {}).get("meta") if isinstance((call or {}).get("meta"), dict) else {}
    missed = fav.get("missed_slots") or meta.get("missed") or 2
    try:
        missed = int(missed)
    except (TypeError, ValueError):
        missed = 2
    out = {"provider": provider, "status": status, "attempt_id": payload.get("attempt_id"),
           "transcript_reference": payload.get("interaction_id"),
           "duration_s": payload.get("duration"), "failure_reason": payload.get("failure_reason"),
           "patient_words": words[:500], "missed": missed, "red_flag": False, "red_flag_rule": None,
           "callback_requested": False, "possible_distress": False,
           "reason_category": None, "outcome": None, "neutral_note": ""}
    if status != "completed":
        out["outcome"] = "no_answer" if status in ("no-answer", "busy") else "failed"
        out["neutral_note"] = neutral_note(out["outcome"], "", missed, "other", False)
        return out
    # 1) red flag: OUR deterministic rule on the patient's own words (all user turns), never the AI
    patient_text = " ".join([words] + user_turns)
    out["red_flag"] = red_flag_words(patient_text)
    out["red_flag_rule"] = "voice.red_flag word list" if out["red_flag"] else None
    # 2) reason: the agent's enum if it is one we know and our keywords found nothing specific
    ours = classify_reason(words)
    theirs = str(fav.get("reason_category") or "").strip().lower()
    out["reason_category"] = ours if ours != "other" or theirs not in REASONS else theirs
    cb = _truthy(fav.get("callback_requested"))
    if cb is None and len(user_turns) > 1:
        cb = yes_no(user_turns[-1])
    out["callback_requested"] = bool(cb)
    # 3) optional sentiment -> only a soft, low-confidence hint for the nurse
    out["possible_distress"] = str(fav.get("sentiment") or "").strip().lower() in ("negative", "distressed")
    if out["red_flag"]:
        out["outcome"] = "red_flag"
        out["callback_requested"] = True
    elif not words:
        out["outcome"] = "unclear"
    elif out["reason_category"] in CONCERN or out["callback_requested"] or out["possible_distress"]:
        out["outcome"] = "needs_nurse_review"
    else:
        out["outcome"] = "ok"
    out["neutral_note"] = neutral_note(out["outcome"], words, missed, out["reason_category"],
                                       out["callback_requested"])
    return out


# ----------------------------------------------------------------------------- applying a result

def apply_result(call: dict, norm: dict, source: str) -> dict:
    """Write a normalised outcome into SpiroBuddy: call row, timeline note, alerts, ladder."""
    from . import alerts, calls, escalation
    cid = call["id"]
    pid = call["patient_id"]
    p = patient(pid) or {"name": call.get("to_name") or "Patient"}
    fn = first_name(p["name"])
    meta = call.get("meta") if isinstance(call.get("meta"), dict) else {}
    meta = {**meta, "result": norm, "result_pending": False, "result_at": iso(now()),
            "result_source": source}
    if norm.get("attempt_id"):
        meta["webhook_attempt"] = norm["attempt_id"]
    outcome = norm["outcome"]
    if outcome in ("no_answer", "failed"):
        st().update("calls", [("id", "eq", cid)], {"meta": meta, "updated_at": iso(now())})
        calls.finish(cid, norm["status"] if norm["status"] in calls.FINAL else "failed", source)
        if norm.get("failure_reason"):
            log_event(pid, "call", f"Check-in call to {fn} failed", detail=norm["failure_reason"],
                      channel="call", actor="patient", status="failed", run_id=call.get("run_id"),
                      ref_id=cid)
        return calls.public_call(calls.get_call(cid) or call)
    st().update("calls", [("id", "eq", cid)], {"status": "completed", "outcome": outcome,
                                               "meta": meta, "updated_at": iso(now())})
    distress = " · possible distress – nurse to review (low confidence)" if norm.get("possible_distress") else ""
    log_event(pid, "call_result", f"Check-in call result: {OUTCOME_LABEL[outcome]}{distress}",
              detail=norm["neutral_note"], channel="call", actor="patient", to_name=fn,
              status="warn" if outcome in ("red_flag", "needs_nurse_review", "unclear") else "ok",
              run_id=call.get("run_id"), ref_id=cid)
    if outcome == "red_flag":
        escalation.red_flag(pid, norm.get("patient_words") or "red-flag words",
                            source=f"AI check-in call ({source})")
    elif outcome in ("needs_nurse_review", "unclear"):
        detail = norm["neutral_note"]
        if norm.get("patient_words"):
            detail += f"\nPatient's own words: “{norm['patient_words']}”"
        if norm.get("possible_distress"):
            detail += "\nPossible distress – nurse to review (low confidence, from call sentiment)."
        if norm.get("transcript_reference"):
            detail += f"\nTranscript reference: {norm['transcript_reference']}"
        a = alerts.raise_alert(pid, "call_review", "amber",
                               f"{p['name']}: check-in call – nurse review requested", detail=detail,
                               run_id=call.get("run_id"), dedupe_hours=2)
        run = escalation.active_run(pid)
        if run:
            escalation.resolve(run, "nurse_review", "Handed to the nurse – check-in call note", "patient")
        log_event(pid, "nurse_alert", f"Check-in call note for {fn} sent to the nurse",
                  channel="dashboard", actor="nurse", status="ok", run_id=call.get("run_id"),
                  ref_id=a.get("id"))
    else:   # ok
        run = escalation.active_run(pid)
        if run:
            escalation.resolve(run, "checkin_ok", f"{fn} answered the check-in call – no concern raised "
                                                  f"(the device count confirms the session)", "patient")
    return calls.public_call(calls.get_call(cid) or call)


def find_call(payload: dict) -> dict | None:
    from . import calls
    attempt = str(payload.get("attempt_id") or "")
    if attempt:
        rows = st().select("calls", [("provider_sid", "eq", attempt)])
        if rows:
            return rows[0]
    wc = payload.get("webhook_config")
    md = (wc.get("metadata") if isinstance(wc, dict) else None) or {}
    cid = md.get("call_id") if isinstance(md, dict) else None
    try:        # a forged / malformed webhook must never crash the handler (it is just "unknown")
        cid = int(cid) if cid and not isinstance(cid, (bool, list, dict)) else None
    except (TypeError, ValueError):
        cid = None
    if cid:
        c = calls.get_call(cid)
        if c and str(c.get("provider_sid") or "") in ("", attempt) and c.get("provider") == "sarvam_agent":
            return c
    return None


def handle_webhook(payload: dict, source: str = "Sarvam webhook") -> dict:
    """Idempotent: a repeated delivery of the same attempt returns the stored result."""
    with _lock:
        call = find_call(payload or {})
        if not call:
            return {"ok": False, "error": "unknown attempt_id – not a call SpiroBuddy placed"}
        meta = call.get("meta") if isinstance(call.get("meta"), dict) else {}
        if meta.get("result") and meta.get("webhook_attempt") == payload.get("attempt_id"):
            return {"ok": True, "duplicate": True, "call_id": call["id"], "result": meta["result"]}
        norm = normalise(payload, call)
        pc = apply_result(call, norm, source)
        return {"ok": True, "duplicate": False, "call_id": call["id"], "result": norm, "call": pc}


# ----------------------------------------------------------------------------- placing the call

def _post(url: str, body: dict) -> dict:
    import httpx
    r = httpx.post(url, json=body, headers={"X-API-Key": api_key(), "Content-Type": "application/json"},
                   timeout=float(env("SARVAM_TIMEOUT_S", "25") or 25))
    if r.status_code >= 400:
        raise RuntimeError(f"Sarvam {r.status_code}: {r.text[:200]}")
    return r.json()


def build_request(call: dict, p: dict, number: str, lang: str, missed: int) -> dict:
    from .calls import nurse_desk_number
    vlang = SARVAM_LANG.get(voice_lang(p["id"], lang), SARVAM_LANG.get(lang, "English"))
    app = {"app_id": env("SARVAM_AGENT_ID"), "app_version": int(env("SARVAM_AGENT_VERSION", "1") or 1),
           "connection_config": {"connection_id": env("SARVAM_CONNECTION_ID"),
                                 "agent_phone_number": env("SARVAM_AGENT_NUMBER")},
           # input variables defined in the agent (docs/COMMS.md §5): all strings
           "agent_variables": {"patient_id": str(p["id"]), "patient_name": first_name(p.get("name")),
                               "language": vlang, "missed_slots": str(missed),
                               "callback_number": env("SARVAM_CALLBACK_NUMBER") or nurse_desk_number() or ""},
           "app_overrides": {"initial_language_name": vlang}}
    return {"app_config": app, "user_config": {"user_phone_number": number},
            "webhook_config": {"url": webhook_url(),
                               "metadata": {"call_id": call["id"], "patient_id": p["id"]}}}


def place(call: dict, p: dict, number: str, lang: str, missed: int) -> str | None:
    """Ask Sarvam to dial. -> error text or None (attempt_id stored as provider_sid)."""
    url = (f"{env('SARVAM_AGENT_API_BASE', API_BASE_DEFAULT).rstrip('/')}/v1/orgs/"
           f"{env('SARVAM_ORG_ID')}/workspaces/{env('SARVAM_WORKSPACE_ID')}/outbounds")
    try:
        res = _post(url, build_request(call, p, number, lang, missed))
        attempt = str((res or {}).get("attempt_id") or "")
        if not attempt:
            return "Sarvam returned no attempt_id"
        meta = call.get("meta") if isinstance(call.get("meta"), dict) else {}
        st().update("calls", [("id", "eq", call["id"])],
                    {"provider_sid": attempt, "status": "initiated",
                     "meta": {**meta, "result_pending": True}, "updated_at": iso(now())})
        return None
    except Exception as e:
        log.warning("Sarvam outbound call failed: %s", e)
        return str(e)[:300]


# ----------------------------------------------------------------------------- browser simulator

def sim_turn(cid: int, text: str, source: str = "phone simulator") -> dict:
    """One spoken (or tapped) patient answer in the simulated conversational call.
    -> {say, language, end, stage, answers, result?, call}"""
    from . import calls
    with _lock:
        c = calls.get_call(cid)
        if not c:
            raise KeyError(cid)
        meta = c.get("meta") if isinstance(c.get("meta"), dict) else {}
        lang = lang_of(c.get("language"), "en")
        if meta.get("result"):
            return {"say": "", "language": lang, "end": True, "stage": 2, "answers": [],
                    "result": meta["result"], "call": calls.public_call(c)}
        stage = int(meta.get("stage") or 0)
        text = (text or "").strip()[:500]
        turns = list(meta.get("turns") or [{"role": "agent", "en_text": c.get("script") or ""}])
        p = patient(c["patient_id"]) or {"name": c.get("to_name")}
        if text:
            turns.append({"role": "user", "en_text": text})
            log_event(c["patient_id"], "inbound", f"{first_name(p['name'])} said: “{text[:120]}”",
                      detail=f"Spoken answer on the check-in call (via {source})", channel="call",
                      actor="patient", to_name=first_name(p["name"]), status="info",
                      run_id=c.get("run_id"), ref_id=cid)
        end = False
        if not text:
            say = line("repeat", lang)
        elif red_flag_words(text):
            from ..voice import red_flag_message
            say = f"{red_flag_message(lang)} {line('red_tail', lang)}"
            end = True
        elif stage == 0:
            meta["patient_words"] = text
            reason = classify_reason(text)
            meta["reason"] = reason
            say = line("ack_concern" if reason in CONCERN else "ack_ok", lang)
            stage = 1
        else:
            yn = yes_no(text)
            meta["callback"] = "yes" if yn else "no"
            say = line("bye_callback" if yn else "bye_ok", lang)
            end = True
        turns.append({"role": "agent", "en_text": say})
        meta.update({"stage": stage, "turns": turns})
        st().update("calls", [("id", "eq", cid)], {"meta": meta, "status": "in-progress",
                                                   "updated_at": iso(now())})
        out = {"say": say, "language": lang, "end": end, "stage": stage,
               "answers": [] if end else ANSWERS[min(stage, 1)][lang]}
        if end:
            payload = {"attempt_id": f"sim-{cid}", "status": "connected",
                       "interaction_id": f"simulator/call-{cid}", "duration": None,
                       "final_agent_variables": {"patient_words": meta.get("patient_words") or text,
                                                 "reason_category": meta.get("reason"),
                                                 "callback_requested": meta.get("callback"),
                                                 "missed_slots": str(meta.get("missed") or 2)},
                       "interaction_transcript": turns}
            c = calls.get_call(cid) or c
            norm = normalise(payload, c, provider="simulator")
            out["call"] = apply_result(c, norm, source)
            out["result"] = norm
        else:
            out["call"] = calls.public_call(calls.get_call(cid) or c)
        try:
            from .audio import tts_url
            out["audio_url"] = tts_url(say, lang) if say else None
        except Exception:
            out["audio_url"] = None
        return out


def sim_finish(cid: int, source: str = "phone simulator (hung up)") -> dict | None:
    """The simulated AI call ended early (hang-up / idle): turn what was said into a result.
    Nothing said -> 'unclear' (nurse review), never silently dropped."""
    from . import calls
    with _lock:
        c = calls.get_call(cid)
        if not c:
            return None
        meta = c.get("meta") if isinstance(c.get("meta"), dict) else {}
        if meta.get("result"):
            return calls.public_call(c)
        turns = list(meta.get("turns") or [{"role": "agent", "en_text": c.get("script") or ""}])
        payload = {"attempt_id": f"sim-{cid}", "status": "connected",
                   "interaction_id": f"simulator/call-{cid}",
                   "final_agent_variables": {"patient_words": meta.get("patient_words") or "",
                                             "reason_category": meta.get("reason"),
                                             "callback_requested": meta.get("callback"),
                                             "missed_slots": str(meta.get("missed") or 2)},
                   "interaction_transcript": turns}
        return apply_result(c, normalise(payload, c, provider="simulator"), source)


# ----------------------------------------------------------------------------- demo replay

def load_samples() -> dict:
    try:
        return json.loads(SAMPLES_FILE.read_text(encoding="utf-8")).get("samples", {})
    except Exception as e:
        log.warning("cannot read %s: %s", SAMPLES_FILE, e)
        return {}


def replay(pid: int, sample: str) -> dict:
    """Demo: create a Sarvam-style call row and feed a saved webhook payload through the SAME
    handler a live webhook uses, so the nurse note appears even if a live call fails."""
    from . import calls
    samples = load_samples()
    if sample not in samples:
        raise ValueError(f"sample must be one of {', '.join(samples)}")
    p = patient(pid)
    if not p:
        raise KeyError(pid)
    s = json.loads(json.dumps(samples[sample]["payload"]))
    t = now()
    attempt = f"demo-{uuid.uuid4()}"
    fav = s.get("final_agent_variables")
    if isinstance(fav, dict):
        fav["patient_id"] = str(pid)
        fav["patient_name"] = first_name(p["name"])
    missed = int((fav or {}).get("missed_slots") or 2)
    lang = lang_of(p.get("language"), "en")
    row = {"patient_id": int(pid), "run_id": (escalation_run_id(pid)), "guardian_id": None,
           "to_role": "patient", "to_name": p["name"], "to_number": None, "purpose": "checkin",
           "provider": "sarvam_agent", "provider_sid": attempt, "status": "initiated",
           "digits": None, "outcome": None, "language": lang, "script": greeting(p, lang, missed),
           "meta": {"style": "agent", "missed": missed, "result_pending": True, "replay": sample,
                    "note": "demo replay of a saved Sarvam webhook payload"},
           "ring_until": iso(t + timedelta(seconds=30)), "created_at": iso(t), "updated_at": iso(t)}
    call = st().insert("calls", [row])[0]
    log_event(pid, "call", f"Replay: AI check-in call to {first_name(p['name'])} (saved Sarvam result)",
              detail=samples[sample].get("label") or sample, channel="call", actor="patient",
              to_name=first_name(p["name"]), status="dry_run", run_id=row["run_id"], ref_id=call["id"])
    s["attempt_id"] = attempt
    s["webhook_config"] = {"url": "/api/comms/webhooks/sarvam",
                           "metadata": {"call_id": call["id"], "patient_id": pid}}
    return handle_webhook(s, source="demo replay")


def escalation_run_id(pid: int) -> int | None:
    from .escalation import active_run
    r = active_run(pid)
    return r["id"] if r else None


def public_result(c: dict) -> dict | None:
    """What the dashboard shows for a check-in call (pending vs result)."""
    meta = c.get("meta") if isinstance(c.get("meta"), dict) else {}
    if (meta.get("style") != "agent") and c.get("provider") != "sarvam_agent":
        return None
    res = meta.get("result")
    if res:
        return {"pending": False, "label": OUTCOME_LABEL.get(res.get("outcome"), res.get("outcome")),
                **{k: res.get(k) for k in ("outcome", "reason_category", "patient_words",
                                            "neutral_note", "red_flag", "callback_requested",
                                            "possible_distress", "transcript_reference", "provider")}}
    if c.get("status") in ("no-answer", "busy", "failed", "canceled"):
        o = "no_answer" if c.get("status") in ("no-answer", "busy", "canceled") else "failed"
        return {"pending": False, "label": OUTCOME_LABEL[o], "outcome": o, "reason_category": None,
                "patient_words": "", "neutral_note": f"Check-in call: {OUTCOME_LABEL[o].lower()}.",
                "red_flag": False, "callback_requested": False, "possible_distress": False,
                "transcript_reference": None, "provider": c.get("provider")}
    ring = to_dt(c.get("ring_until"))
    calling = c.get("status") in ("queued", "initiated", "ringing") and ring and ring > now()
    return {"pending": True,
            "label": "calling…" if calling else "call completed; result pending"}
