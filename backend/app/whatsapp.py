"""WhatsApp via Twilio (sandbox), or a dry run when credentials/numbers are missing.

Every attempt (sent, dry run or failed) is stored in the `messages` table by the caller.
For safety in DEMO mode, messages only ever go to the patient's own family/nurse number if
one was set in the app, otherwise to DEMO_FAMILY_WHATSAPP / DEMO_NURSE_WHATSAPP.
"""
from __future__ import annotations

import logging
import threading
import time

from .config import env

log = logging.getLogger("spirobuddy.whatsapp")

MIN_GAP_S = 3.0          # Twilio WhatsApp sandbox: at most one message every 3 seconds
_last_send = 0.0
_send_lock = threading.Lock()


def throttle() -> None:
    """Wait so real WhatsApp sends are at least MIN_GAP_S apart (shared by every sender)."""
    global _last_send
    with _send_lock:
        wait = MIN_GAP_S - (time.time() - _last_send)
        if wait > 0:
            time.sleep(wait)
        _last_send = time.time()


def whatsapp_enabled() -> bool:
    return bool(env("TWILIO_ACCOUNT_SID") and env("TWILIO_AUTH_TOKEN") and env("TWILIO_WHATSAPP_FROM"))


def _norm(number: str | None) -> str | None:
    if not number:
        return None
    n = number.strip().replace(" ", "")
    if not n or "X" in n.upper().replace("WHATSAPP:", ""):   # placeholder like +91XXXXXXXXXX
        return None
    return n if n.startswith("whatsapp:") else f"whatsapp:{n}"


def resolve_number(patient: dict, to_role: str) -> str | None:
    if to_role == "nurse":
        return _norm(patient.get("nurse_phone")) or _norm(env("DEMO_NURSE_WHATSAPP"))
    return _norm(patient.get("family_phone")) or _norm(env("DEMO_FAMILY_WHATSAPP"))


def send(to_number: str | None, text: str) -> dict:
    """-> {sent, dry_run, error?}"""
    if not whatsapp_enabled() or not to_number:
        return {"sent": False, "dry_run": True}
    throttle()
    try:
        from twilio.rest import Client
        client = Client(env("TWILIO_ACCOUNT_SID"), env("TWILIO_AUTH_TOKEN"))
        msg = client.messages.create(from_=_norm(env("TWILIO_WHATSAPP_FROM")), to=to_number,
                                     body=text[:1500])
        return {"sent": True, "dry_run": False, "sid": msg.sid}
    except Exception as e:
        log.warning("Twilio send failed: %s", e)
        return {"sent": False, "dry_run": False, "error": str(e)[:300]}


def missed_text(patient: dict, hours: list[int], language: str) -> str:
    first = patient["name"].split()[0]
    times = ", ".join(f"{h}:00" for h in hours) if hours else ""
    if language == "hi":
        return (f"SpiroBuddy सूचना: {first} ने लगातार {max(2, len(hours))} साँस-व्यायाम सत्र छोड़ दिए हैं"
                f"{' (' + times + ')' if times else ''}। कृपया उनसे बात करें। "
                f"साँस लेने में तकलीफ़ हो तो नर्स से संपर्क करें या 112 पर कॉल करें।")
    # ta / ml: written without a native speaker – NEEDS A NATIVE-SPEAKER CHECK (Q-28).
    if language == "ta":
        return (f"SpiroBuddy அறிவிப்பு: {first} தொடர்ந்து {max(2, len(hours))} மூச்சுப் பயிற்சி அமர்வுகளைத் "
                f"தவறவிட்டுள்ளார்{' (' + times + ')' if times else ''}. தயவுசெய்து அவரிடம் பேசுங்கள். "
                f"மூச்சு விடுவதில் சிரமம் இருந்தால் செவிலியரைத் தொடர்பு கொள்ளுங்கள் அல்லது 112 ஐ அழைக்கவும்.")
    if language == "ml":
        return (f"SpiroBuddy അറിയിപ്പ്: {first} തുടർച്ചയായി {max(2, len(hours))} ശ്വസന വ്യായാമ സെഷനുകൾ "
                f"ചെയ്തില്ല{' (' + times + ')' if times else ''}. ദയവായി അവരുമായി സംസാരിക്കുക. "
                f"ശ്വാസമെടുക്കാൻ ബുദ്ധിമുട്ടുണ്ടെങ്കിൽ നഴ്സിനെ ബന്ധപ്പെടുക അല്ലെങ്കിൽ 112-ൽ വിളിക്കുക.")
    return (f"SpiroBuddy alert: {first} has missed {max(2, len(hours))} breathing sessions in a row"
            f"{' (' + times + ')' if times else ''}. Please check in with them. "
            f"If they have trouble breathing, contact the nurse or call 112.")
