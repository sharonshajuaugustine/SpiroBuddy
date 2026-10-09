"""Bridge to backend/app/voice.py (natural Indian-language voices via Sarvam, voice agent's module).

`voice.tts(text, lang)` returns a cached audio path or None; `voice.tts_url(path)` turns it into
"/api/voice/audio/<file>" (served by routes_voice). For Twilio/WhatsApp we need an absolute URL
(PUBLIC_BASE_URL + that path). If voice.py is missing or has no key, callers fall back to
Twilio <Say> / the browser's own speech.
"""
from __future__ import annotations

import logging

from .common import public_base

log = logging.getLogger("spirobuddy.comms.audio")


def _voice():
    try:
        from .. import voice   # optional module (voice agent)
        return voice if hasattr(voice, "tts") else None
    except Exception:
        return None


def available() -> bool:
    v = _voice()
    try:
        return bool(v and v.enabled())
    except Exception:
        return False


def tts_url(text: str, lang: str = "en", absolute: bool = False, phone: bool = False) -> str | None:
    """URL of natural-voice audio for `text`, or None (caller then uses <Say> / browser speech).
    phone=True asks for 8 kHz audio, which is what a phone line carries."""
    v = _voice()
    if not v or not text:
        return None
    try:
        path = v.tts(text, lang, sample_rate=8000) if phone else v.tts(text, lang)
    except TypeError:
        path = v.tts(text, lang)
    except Exception as e:
        log.info("voice.tts failed (%s); falling back to built-in speech", e)
        return None
    if not path:
        return None
    try:
        url = v.tts_url(path)
    except Exception:
        return None
    if absolute:
        base = public_base()
        return (base + url) if (base and url) else None
    return url


def red_flag(text: str) -> bool:
    """voice.red_flag covers red-flag words in 11 Indian languages."""
    v = _voice()
    try:
        return bool(v and hasattr(v, "red_flag") and v.red_flag(text))
    except Exception:
        return False
