"""Consent for automated calls and messages (TRAI 2026 A2P rules + DPDP Act / Rules).

- The consent text is FROM the patient's point of view, in their language, read aloud to them
  (browser voice / Sarvam), with an itemised list of the data kept, and a one-word STOP.
- Consent = flag + date (common.has_consent). "Ongoing use" consent lasts 7 days: after that REAL
  automated calls are blocked (simulator only) until the person says yes again (consent_current).
- Every week SpiroBuddy asks one question on WhatsApp: "Keep the reminder calls? ✅ Yes / ⛔ STOP".
  One tap renews; "STOP" (any of our languages) withdraws consent immediately.
"""
from __future__ import annotations

import re
from datetime import timedelta

from ..config import iso
from .common import (CONSENT_RENEW_DAYS, consent_age_days, first_name, has_consent, in_quiet,
                     lang_of, log_event, now, st, text_lang, to_dt)

DATA_ITEMS = {
    "en": ["your name, age and operation", "your phone number and language",
           "your family members' names and phone numbers",
           "your breathing-exercise counts and readings from the SpiroBuddy device",
           "your answers on SpiroBuddy calls and WhatsApp messages"],
    "hi": ["आपका नाम, उम्र और ऑपरेशन", "आपका फ़ोन नंबर और भाषा",
           "आपके परिवार के लोगों के नाम और फ़ोन नंबर",
           "SpiroBuddy उपकरण से आपके साँस-व्यायाम की गिनती और रीडिंग",
           "SpiroBuddy कॉल और WhatsApp संदेशों पर आपके जवाब"],
    "ta": ["உங்கள் பெயர், வயது மற்றும் அறுவை சிகிச்சை", "உங்கள் தொலைபேசி எண் மற்றும் மொழி",
           "உங்கள் குடும்பத்தினரின் பெயர்கள் மற்றும் தொலைபேசி எண்கள்",
           "SpiroBuddy கருவியிலிருந்து உங்கள் மூச்சுப் பயிற்சி எண்ணிக்கை மற்றும் அளவீடுகள்",
           "SpiroBuddy அழைப்புகள் மற்றும் WhatsApp செய்திகளில் உங்கள் பதில்கள்"],
}
CONSENT_TEXT = {
    "en": ("I agree that SpiroBuddy, an automated (AI) care assistant from my hospital, may send me "
           "breathing-exercise reminders on WhatsApp, call me with an automated voice, and tell my "
           "family and my nurse if I miss sessions or ask for help. It keeps only: {items}. It never "
           "diagnoses. I can stop at any time by saying or sending one word: STOP. This permission "
           "lasts 7 days, and SpiroBuddy will ask me again every week."),
    "hi": ("मैं सहमत हूँ कि SpiroBuddy, मेरे अस्पताल की स्वचालित (AI) देखभाल सहायक, मुझे WhatsApp पर "
           "साँस-व्यायाम की याद दिला सकती है, स्वचालित आवाज़ में कॉल कर सकती है, और अगर मैं व्यायाम छोड़ूँ या "
           "मदद माँगूँ तो मेरे परिवार और नर्स को बता सकती है। यह केवल यह जानकारी रखती है: {items}। यह कभी "
           "बीमारी नहीं बताती। मैं कभी भी एक शब्द बोलकर या भेजकर रोक सकता/सकती हूँ: STOP या \"रोको\"। यह "
           "अनुमति 7 दिन चलती है, और SpiroBuddy हर हफ़्ते फिर पूछेगी।"),
    "ta": ("எனது மருத்துவமனையின் தானியங்கி (AI) பராமரிப்பு உதவியாளரான SpiroBuddy, எனக்கு WhatsApp-இல் "
           "மூச்சுப் பயிற்சி நினைவூட்டல்களை அனுப்பவும், தானியங்கி குரலில் அழைக்கவும், நான் பயிற்சியைத் தவறவிட்டால் "
           "அல்லது உதவி கேட்டால் என் குடும்பத்தினருக்கும் செவிலியருக்கும் தெரிவிக்கவும் நான் ஒப்புக்கொள்கிறேன். "
           "இது வைத்திருப்பது இவை மட்டுமே: {items}. இது நோயைக் கண்டறியாது. ஒரே ஒரு சொல் சொல்லி அல்லது அனுப்பி "
           "எப்போது வேண்டுமானாலும் நிறுத்தலாம்: STOP அல்லது \"நிறுத்து\". இந்த அனுமதி 7 நாட்கள் செல்லும்; "
           "SpiroBuddy ஒவ்வொரு வாரமும் மீண்டும் கேட்கும்."),
}
RENEW_TEXT = {
    "en": "Namaste {n}, this is SpiroBuddy's automated care assistant. One question: shall we keep "
          "sending your breathing reminders and automated calls for another week?",
    "hi": "नमस्ते {n}, यह SpiroBuddy की स्वचालित देखभाल सहायक है। एक सवाल: क्या हम अगले एक हफ़्ते भी "
          "साँस-व्यायाम की याद और स्वचालित कॉल भेजते रहें?",
    "ta": "வணக்கம் {n}, இது SpiroBuddy-இன் தானியங்கி பராமரிப்பு உதவியாளர். ஒரு கேள்வி: இன்னும் ஒரு வாரம் "
          "மூச்சுப் பயிற்சி நினைவூட்டல்களும் தானியங்கி அழைப்புகளும் தொடரலாமா?",
    # ml strings in this file: NEEDS A NATIVE-SPEAKER CHECK (Q-28). The full consent statement
    # (CONSENT_TEXT) has no Malayalam yet and stays English for ml.
    "ml": "നമസ്കാരം {n}, ഇത് SpiroBuddy-യുടെ ഓട്ടോമാറ്റിക് പരിചരണ സഹായിയാണ്. ഒരു ചോദ്യം: ശ്വസന വ്യായാമ "
          "ഓർമ്മപ്പെടുത്തലുകളും ഓട്ടോമാറ്റിക് കോളുകളും ഒരു ആഴ്ച കൂടി തുടരട്ടെയോ?",
}
RENEW_BUTTONS = {
    "en": [("consent_yes", "✅ Yes, keep them"), ("stop", "⛔ STOP")],
    "hi": [("consent_yes", "✅ हाँ, जारी रखें"), ("stop", "⛔ रोको (STOP)")],
    "ta": [("consent_yes", "✅ ஆம், தொடரவும்"), ("stop", "⛔ நிறுத்து (STOP)")],
    "ml": [("consent_yes", "✅ അതെ, തുടരുക"), ("stop", "⛔ നിർത്തുക (STOP)")],
}
REPLY = {
    "consent_yes": {"en": "✅ Thank you. Reminders continue for another 7 days. Send STOP at any time to stop.",
                    "hi": "✅ धन्यवाद। अगले 7 दिन याद दिलाना जारी रहेगा। रोकने के लिए कभी भी STOP भेजें।",
                    "ta": "✅ நன்றி. இன்னும் 7 நாட்கள் நினைவூட்டல்கள் தொடரும். நிறுத்த எப்போது வேண்டுமானாலும் STOP அனுப்பவும்.",
                    "ml": "✅ നന്ദി. ഓർമ്മപ്പെടുത്തലുകൾ 7 ദിവസം കൂടി തുടരും. നിർത്താൻ എപ്പോൾ വേണമെങ്കിലും STOP അയയ്ക്കുക."},
    "stop": {"en": "⛔ Done – SpiroBuddy will not send automated calls or messages any more. Your nurse can still call you. In an emergency, call 112.",
             "hi": "⛔ ठीक है – SpiroBuddy अब स्वचालित कॉल या संदेश नहीं भेजेगी। आपकी नर्स फिर भी कॉल कर सकती हैं। आपातकाल में 112 पर कॉल करें।",
             "ta": "⛔ சரி – SpiroBuddy இனி தானியங்கி அழைப்புகள் அல்லது செய்திகளை அனுப்பாது. உங்கள் செவிலியர் இன்னும் அழைக்கலாம். அவசரத்தில் 112 ஐ அழைக்கவும்.",
             "ml": "⛔ ശരി – SpiroBuddy ഇനി ഓട്ടോമാറ്റിക് കോളുകളോ സന്ദേശങ്ങളോ അയയ്ക്കില്ല. നിങ്ങളുടെ നഴ്സിന് ഇപ്പോഴും വിളിക്കാം. അടിയന്തര സാഹചര്യത്തിൽ 112-ൽ വിളിക്കുക."},
}
STOP_RE = re.compile(r"^\s*(stop|unsubscribe|रोको|रोकें|बंद करो|बंद|நிறுத்து|நிறுத்தவும்|നിർത്തുക|നിർത്തൂ|നിർത്ത്|⛔.*)\s*[.!।]?\s*$", re.I)


def consent_text(lang: str) -> dict:
    lang = lang_of(lang, "en")
    items = DATA_ITEMS[lang]
    sep = {"en": "; ", "hi": "; ", "ta": "; "}[lang]
    return {"language": lang, "text": CONSENT_TEXT[lang].format(items=sep.join(items)),
            "items": items, "valid_days": CONSENT_RENEW_DAYS, "stop_word": "STOP"}


def info(obj: dict) -> dict:
    age = consent_age_days(obj)
    return {"consent_ok": has_consent(obj), "consent_age_days": age,
            "consent_renew_due": bool(has_consent(obj) and age is not None and age >= CONSENT_RENEW_DAYS)}


# ----------------------------------------------------------------------------- set / withdraw

def _set_patient(pid: int, value: bool, how: str) -> None:
    from .guardians import put_settings
    put_settings(pid, {"consent": value, "renew_consent": value})
    p = st().select("patients", [("id", "eq", int(pid))]) or [{"name": "Patient"}]
    fn = first_name(p[0].get("name"))
    log_event(pid, "consent", f"{fn} {'renewed consent for 7 days' if value else 'said STOP – consent withdrawn'}",
              detail=how, channel="whatsapp", actor="patient", to_name=fn,
              status="ok" if value else "warn")


def _set_guardian(g: dict, value: bool, how: str) -> None:
    from .guardians import guardian_label, update_guardian
    update_guardian(g["id"], {"consent": value})
    log_event(g["patient_id"], "consent",
              f"{guardian_label(g)} {'renewed consent for 7 days' if value else 'said STOP – consent withdrawn'}",
              detail=how, channel="whatsapp", actor="guardian", to_name=first_name(g.get("name")),
              status="ok" if value else "warn")


def apply(pid: int, role: str, guardian: dict | None, value: bool, how: str) -> None:
    if role == "guardian" and guardian:
        _set_guardian(guardian, value, how)
    else:
        _set_patient(pid, value, how)


def last_ask(pid: int, to_role: str, number: str | None = None) -> dict | None:
    f = [("patient_id", "eq", int(pid)), ("kind", "eq", "consent_renewal"), ("to_role", "eq", to_role)]
    if number:
        f.append(("to_number", "eq", number))
    rows = st().select("messages", f, order="id", desc=True, limit=1)
    return rows[0] if rows else None


def asked_recently(pid: int, to_role: str, hours: float = 48, number: str | None = None) -> bool:
    m = last_ask(pid, to_role, number)
    t = to_dt((m or {}).get("created_at"))
    return bool(t and now() - t < timedelta(hours=hours))


# ----------------------------------------------------------------------------- weekly question

def ask(pid: int, to: str = "patient", guardian: dict | None = None) -> dict:
    """Send the one-question renewal on WhatsApp (one tap: ✅ yes / ⛔ STOP)."""
    from . import messages
    from .guardians import get_settings, guardian_label, primary_guardian
    p = st().select("patients", [("id", "eq", int(pid))])[0]
    if to == "family":
        g = guardian or primary_guardian(pid)
        if not g:
            raise ValueError("no guardian in the care circle")
        lang = text_lang(g.get("language"), "en")
        return messages.send(p, "family", g.get("phone"), RENEW_TEXT[lang].format(n=first_name(g["name"])),
                             "consent_renewal", lang, buttons=RENEW_BUTTONS[lang],
                             to_name=guardian_label(g))
    lang = text_lang(p.get("language"), "en")
    return messages.send(p, "patient", get_settings(pid).get("patient_phone"),
                         RENEW_TEXT[lang].format(n=messages.addr(p, lang)), "consent_renewal", lang,
                         buttons=RENEW_BUTTONS[lang], to_name=first_name(p["name"]))


def weekly_check() -> int:
    """Ask once (outside quiet hours) when consent is 6+ days old and not asked in 48 h."""
    from .guardians import get_settings, guardian_quiet, list_guardians
    n = 0
    t = now()
    for p in st().select("patients", columns="id"):
        cfg = get_settings(p["id"])
        if in_quiet(t, cfg["quiet_start"], cfg["quiet_end"]):
            continue
        age = consent_age_days(cfg)
        if has_consent(cfg) and age is not None and age >= CONSENT_RENEW_DAYS - 1 \
                and not asked_recently(p["id"], "patient"):
            ask(p["id"], "patient")
            n += 1
        for g in list_guardians(p["id"]):
            qs, qe = guardian_quiet(g, cfg)
            age = consent_age_days(g)
            if has_consent(g) and age is not None and age >= CONSENT_RENEW_DAYS - 1 \
                    and not in_quiet(t, qs, qe)                     and not asked_recently(p["id"], "family", number=g.get("phone")):
                ask(p["id"], "family", g)
                n += 1
    return n


def stamp() -> str:
    return iso(now())
