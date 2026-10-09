"""Shared helpers for the comms package: time & quiet hours (IST), names, numbers, events."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from .. import service
from ..config import demo_mode, env, iso, now_local, parse_dt

log = logging.getLogger("spirobuddy.comms")

LANGS = ("en", "hi", "ta")          # languages with FULL comms text (calls, IVR, consent statement)
# WhatsApp text (messages, disclosure, footer, replies, summaries) also exists in Malayalam (Q-28).
# Calls/IVR/consent statement have no Malayalam yet, so they keep using lang_of() (ml -> en).
TEXT_LANGS = LANGS + ("ml",)


def st():
    return service.store()


def now() -> datetime:
    return now_local()


def to_dt(v) -> datetime | None:
    if v in (None, ""):
        return None
    try:
        return parse_dt(v)
    except (TypeError, ValueError):
        return None


def lang_of(value, default: str = "en") -> str:
    v = str(value or "").lower()[:2]
    if v in LANGS:
        return v
    # A real language we have no comms text for yet (e.g. Malayalam "ml") -> English, never
    # another Indian language: a Malayali should not get Hindi. Empty/unknown -> `default`.
    if v.isalpha() and len(v) == 2:
        return "en"
    return default


def text_lang(value, default: str = "en") -> str:
    """Language for WhatsApp TEXT: like lang_of, but Malayalam ("ml") is kept (Q-28).
    Any other language we have no text for -> English."""
    v = str(value or "").lower()[:2]
    return v if v in TEXT_LANGS else lang_of(value, default)


def first_name(name: str | None) -> str:
    return (name or "").split()[0] if name else ""


# ----------------------------------------------------------------------------- quiet hours (IST)

def default_quiet() -> tuple[str, str]:
    """QUIET_HOURS env like '21:00-07:00' (IST). Default 21:00–07:00 (research F-COMMS round 3)."""
    raw = env("QUIET_HOURS", "21:00-07:00")
    try:
        a, b = [x.strip() for x in raw.split("-")]
        parse_hm(a), parse_hm(b)
        return a, b
    except Exception:
        return "21:00", "07:00"


def parse_hm(s: str) -> tuple[int, int]:
    h, m = str(s).strip().split(":")
    h, m = int(h), int(m)
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError(f"bad time {s}")
    return h, m


def valid_hm(s) -> bool:
    try:
        parse_hm(s)
        return True
    except Exception:
        return False


def in_quiet(dt: datetime, start: str, end: str) -> bool:
    """True if dt (local) falls inside [start, end), which may wrap past midnight."""
    try:
        sh, sm = parse_hm(start)
        eh, em = parse_hm(end)
    except Exception:
        return False
    t = dt.hour * 60 + dt.minute
    s, e = sh * 60 + sm, eh * 60 + em
    if s == e:
        return False
    return (s <= t < e) if s < e else (t >= s or t < e)


def quiet_end_after(dt: datetime, end: str) -> datetime:
    """The next time the quiet window ends after dt."""
    eh, em = parse_hm(end)
    cand = dt.replace(hour=eh, minute=em, second=0, microsecond=0)
    if cand <= dt:
        cand += timedelta(days=1)
    return cand


# ----------------------------------------------------------------------------- names

def honorific(patient: dict, lang: str = "en") -> str:
    """'Ravi ji' (Hindi/English, respectful Indian usage); Tamil: 'Lakshmi amma' / 'Mohan ayya';
    Malayalam: 'Sreedevi chechi' / '<name> chettan' (needs a native speaker's check)."""
    fn = first_name(patient.get("name"))
    female = (patient.get("sex") or "").upper() == "F"
    if lang == "ta":
        return f"{fn} {'amma' if female else 'ayya'}"
    if lang == "ml":                       # Malayalam: 'Sreedevi chechi' / 'Gopan chettan'
        return f"{fn} {'chechi' if female else 'chettan'}"
    return f"{fn} ji"


_CALL_NAMES = {
    # relation -> (male patient, female patient) per language
    "son": {"en": ("Papa", "Maa"), "hi": ("पापा", "माँ"), "ta": ("Appa", "Amma"), "ml": ("Achan", "Amma")},
    "daughter": {"en": ("Papa", "Maa"), "hi": ("पापा", "माँ"), "ta": ("Appa", "Amma"), "ml": ("Achan", "Amma")},
    "daughter-in-law": {"en": ("Papa ji", "Mummy ji"), "hi": ("पापा जी", "मम्मी जी"),
                        "ta": ("Mama", "Athai"), "ml": ("Achan", "Amma")},
    "son-in-law": {"en": ("Papa ji", "Mummy ji"), "hi": ("पापा जी", "मम्मी जी"),
                   "ta": ("Mama", "Athai"), "ml": ("Achan", "Amma")},
    "grandson": {"en": ("Dadaji", "Dadi"), "hi": ("दादाजी", "दादी"), "ta": ("Thatha", "Paati"), "ml": ("Appooppan", "Ammoomma")},
    "granddaughter": {"en": ("Dadaji", "Dadi"), "hi": ("दादाजी", "दादी"),
                      "ta": ("Thatha", "Paati"), "ml": ("Appooppan", "Ammoomma")},
    "brother": {"en": ("Bhaiya", "Didi"), "hi": ("भैया", "दीदी"), "ta": ("Anna", "Akka"), "ml": ("Chettan", "Chechi")},
    "sister": {"en": ("Bhaiya", "Didi"), "hi": ("भैया", "दीदी"), "ta": ("Anna", "Akka"), "ml": ("Chettan", "Chechi")},
}


def call_name(relation: str | None, patient: dict, lang: str = "en") -> str:
    """What this guardian calls the patient: 'Papa', 'Maa', 'Mummy ji', or the first name."""
    rel = (relation or "").strip().lower()
    names = _CALL_NAMES.get(rel)
    if not names:
        return first_name(patient.get("name"))
    pair = names.get(lang) or names["en"]
    return pair[1] if (patient.get("sex") or "").upper() == "F" else pair[0]


RELATIONS_HI = {"son": "बेटा", "daughter": "बेटी", "daughter-in-law": "बहू",
                "son-in-law": "दामाद", "wife": "पत्नी", "husband": "पति",
                "grandson": "पोता", "granddaughter": "पोती", "brother": "भाई",
                "sister": "बहन", "neighbour": "पड़ोसी", "friend": "दोस्त"}


# ----------------------------------------------------------------------------- numbers

def e164(number: str | None) -> str | None:
    """'+91 98450 12345' -> '+919845012345'. Placeholders with X (seeded fake numbers) -> None."""
    if not number:
        return None
    n = str(number).strip().replace(" ", "").replace("-", "")
    if n.lower().startswith("whatsapp:"):
        n = n[9:]
    if not n or "X" in n.upper():
        return None
    if n.startswith("0") and len(n) == 11:          # 09845012345 -> +919845012345
        n = "+91" + n[1:]
    if n.isdigit() and len(n) == 10:                 # Indian mobile without code
        n = "+91" + n
    return n if n.startswith("+") and n[1:].isdigit() and 8 <= len(n) <= 16 else None


def demo_route(role: str) -> str | None:
    """Where a real message/call goes when the stored number is a demo placeholder."""
    if role == "patient":
        return e164(env("DEMO_PATIENT_PHONE"))
    if role == "nurse":
        return e164(env("DEMO_NURSE_PHONE")) or e164(env("DEMO_NURSE_WHATSAPP"))
    return e164(env("DEMO_GUARDIAN_PHONE")) or e164(env("DEMO_FAMILY_WHATSAPP"))


def resolve_number(stored: str | None, role: str) -> str | None:
    """Real number to use: the stored one if it is real, else the DEMO_* route for this role."""
    return e164(stored) or demo_route(role)


def public_base() -> str:
    return env("PUBLIC_BASE_URL").rstrip("/")


# ----------------------------------------------------------------------------- patients

def patient(pid: int) -> dict | None:
    return service.get_patient_row(int(pid))


def patient_names() -> dict[int, str]:
    return {p["id"]: p["name"] for p in st().select("patients", columns="id,name")}


# ----------------------------------------------------------------------------- events (timeline)

EVENT_ICONS = {
    "device_beep": "🔔", "whatsapp": "💬", "call": "📞", "call_answered": "📞", "keypress": "🔢",
    "no_answer": "📵", "guardian_whatsapp": "💬", "guardian_call": "📞", "nurse_alert": "🚨",
    "quiet_hold": "🌙", "resolved": "✅", "inbound": "↩", "cheer": "💛", "click_to_call": "☎",
    "red_flag": "🚨", "snooze": "⏰", "trend": "📉", "start": "▶", "stopped": "■",
    "voice_note": "🎧", "weekly_card": "🖼", "sms": "✉", "call_result": "🗒", "consent": "✍",
}


def log_event(patient_id: int | None, kind: str, title: str, detail: str = "",
              channel: str = "system", actor: str = "system", to_name: str | None = None,
              status: str = "info", run_id: int | None = None, ref_id: int | None = None,
              at: datetime | None = None) -> dict:
    row = {"patient_id": patient_id, "run_id": run_id, "kind": kind, "channel": channel,
           "actor": actor, "to_name": to_name, "title": title[:300], "detail": (detail or "")[:1500],
           "status": status, "ref_id": ref_id, "created_at": iso(at or now())}
    try:
        return st().insert("escalation_events", [row])[0]
    except Exception as e:      # the timeline must never break a send
        log.warning("event log failed: %s", e)
        return row


def public_event(e: dict) -> dict:
    return {"id": e.get("id"), "patient_id": e.get("patient_id"), "run_id": e.get("run_id"),
            "kind": e.get("kind"), "icon": EVENT_ICONS.get(e.get("kind") or "", "•"),
            "channel": e.get("channel"), "actor": e.get("actor"), "to_name": e.get("to_name"),
            "title": e.get("title"), "detail": e.get("detail"), "status": e.get("status"),
            "ref_id": e.get("ref_id"),
            "created_at": iso(to_dt(e.get("created_at")) or now())}


def is_demo() -> bool:
    return demo_mode()


# ----------------------------------------------------------------------------- consent & disclosure

CONSENT_RENEW_DAYS = 7     # TRAI 2026: "ongoing use" A2P-call consent lasts 7 days (renewable)


def has_consent(obj: dict | None) -> bool:
    """A real automated call/message needs BOTH the consent flag and the date it was recorded
    (care settings for the patient, the guardian row for family). TRAI / Twilio India / DPDP."""
    return bool(obj and obj.get("consent") and to_dt(obj.get("consent_at")))


def consent_current(obj: dict | None) -> bool:
    """Consent recorded AND younger than 7 days. A REAL automated call needs this; once it has
    lapsed, calls only ring in the simulator until the person says "yes, keep calling" again."""
    age = consent_age_days(obj)
    return has_consent(obj) and age is not None and age < CONSENT_RENEW_DAYS


def consent_age_days(obj: dict | None) -> int | None:
    t = to_dt((obj or {}).get("consent_at"))
    return None if t is None else max(0, (now() - t).days)


# Every automated call and message starts by saying it is an automated (AI) assistant, in the
# person's language (Sarvam terms of service + FEATURE_PLAN idea 70).
DISCLOSURE = {
    "en": "Namaste, this is SpiroBuddy's automated care assistant.",
    "hi": "नमस्ते, यह SpiroBuddy की स्वचालित देखभाल सहायक है।",
    "ta": "வணக்கம், இது SpiroBuddy-இன் தானியங்கி பராமரிப்பு உதவியாளர்.",
    # ml: NEEDS A NATIVE-SPEAKER CHECK (Q-28)
    "ml": "നമസ്കാരം, ഇത് SpiroBuddy-യുടെ ഓട്ടോമാറ്റിക് പരിചരണ സഹായിയാണ്.",
}
DISCLOSURE_TAG = {      # short form for replies inside a conversation the person already started
    "en": "🤖 SpiroBuddy automated assistant:",
    "hi": "🤖 SpiroBuddy स्वचालित सहायक:",
    "ta": "🤖 SpiroBuddy தானியங்கி உதவியாளர்:",
    "ml": "🤖 SpiroBuddy ഓട്ടോമാറ്റിക് സഹായി:",         # needs a native-speaker check
}
_AUTO_MARKERS = ("automated", "स्वचालित", "தானியங்கி", "ഓട്ടോമാറ്റിക്")


def disclosed(text: str, lang: str = "en", short: bool = False) -> str:
    """Prefix the AI disclosure unless the text already carries it."""
    lang = text_lang(lang, "en")
    low = (text or "").lower()
    if any(m in low for m in _AUTO_MARKERS):
        return text
    tag = (DISCLOSURE_TAG if short else DISCLOSURE)[lang]
    return f"{tag} {text}" if short else f"{tag}\n{text}"
