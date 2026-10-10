"""Voice & language API (/api/voice/*). Auto-included by main.py. Contract: docs/VOICE.md §3.

Every endpoint answers cleanly with no Sarvam key: audio endpoints return 503/404 JSON with
`fallback: "browser"` plus the text, so web/js/voice.js speaks it with the browser's voice.
"""
from __future__ import annotations

import json
import logging
import re
import threading

from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from . import llm, service, voice
from .config import DATA_DIR, WEB_DIR
from .voice_cues import CUES, all_cues, cue_text

log = logging.getLogger("spirobuddy.voice")
router = APIRouter(prefix="/api/voice", tags=["voice"])

AUDIO_DIR = WEB_DIR / "audio"
PREFS_FILE = DATA_DIR / "voice_prefs.json"
_prefs_lock = threading.Lock()
MAX_TTS_CHARS = 5000            # longer text is split into 2500-char requests by voice.tts
MAX_STT_BYTES = 5 * 1024 * 1024  # ~30 s of compressed speech is far below this
_SAFE_NAME = re.compile(r"^[0-9a-f]{8,64}\.(mp3|wav)$")
_SAFE_CUE = re.compile(r"^[a-z0-9_]{1,40}$")
MEDIA = {"mp3": "audio/mpeg", "wav": "audio/wav"}


def _browser_fallback(text: str, lang: str, status: int, reason: str) -> JSONResponse:
    return JSONResponse({"error": reason, "status": status, "fallback": "browser",
                         "text": text, "lang": lang, "bcp47": voice.bcp47(lang)},
                        status_code=status)


def _lang_or_400(value, default: str = "en") -> str:
    if value in (None, ""):
        return default
    lg = voice.norm_lang(value)
    if not lg:
        raise HTTPException(400, f"unknown language {value!r}; use one of {list(voice.LANGS)}")
    return lg


def _audio_response(path: str) -> FileResponse:
    ext = path.rsplit(".", 1)[-1]
    return FileResponse(path, media_type=MEDIA.get(ext, "application/octet-stream"),
                        headers={"Cache-Control": "public, max-age=86400",
                                 "X-Audio-Url": voice.tts_url(path) or ""})


# ----------------------------------------------------------------------------- prefs

def _load_prefs() -> dict:
    try:
        return json.loads(PREFS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_prefs(pid: int, patient: dict | None = None) -> dict:
    """Voice settings of a patient: {language, speaker, pace}. Language defaults to the
    patient's own language (en/hi/ta in the patients table; voice supports all 11)."""
    p = _load_prefs().get(str(pid)) or {}
    if patient is None:
        patient = service.get_patient_row(pid) or {}
    return {"patient_id": pid,
            "language": voice.norm_lang(p.get("language")) or voice.norm_lang(patient.get("language")) or "en",
            "speaker": p.get("speaker") or None, "pace": p.get("pace") or None,
            "saved": bool(p)}


@router.get("/prefs/{pid}")
def prefs(pid: int):
    p = service.get_patient_row(pid)
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    return get_prefs(pid, p)


@router.put("/prefs/{pid}")
def set_prefs(pid: int, body: dict = Body(...)):
    p = service.get_patient_row(pid)
    if not p:
        raise HTTPException(404, f"patient {pid} not found")
    with _prefs_lock:
        allp = _load_prefs()
        cur = allp.get(str(pid)) or {}
        if "language" in body:
            cur["language"] = _lang_or_400(body["language"])
        if "speaker" in body:
            spk = (body["speaker"] if isinstance(body["speaker"], str) else "").strip().lower() or None
            if spk and spk not in voice.V3_SPEAKERS and "_" not in spk:
                raise HTTPException(400, "unknown speaker")
            cur["speaker"] = spk
        if "pace" in body:
            try:
                if isinstance(body["pace"], (bool, list, dict)):
                    raise ValueError("pace")
                cur["pace"] = None if body["pace"] in (None, "") else min(2.0, max(0.5, float(body["pace"])))
            except ValueError:
                raise HTTPException(400, "pace must be a number between 0.5 and 2")
        allp[str(pid)] = cur
        PREFS_FILE.write_text(json.dumps(allp, ensure_ascii=False, indent=1), encoding="utf-8")
    return get_prefs(pid, p)


# ----------------------------------------------------------------------------- info

@router.get("/status")
def status():
    s = voice.status()
    s["clips"] = {lg: len(list((AUDIO_DIR / lg).glob("*.mp3")) + list((AUDIO_DIR / lg).glob("*.wav")))
                  if (AUDIO_DIR / lg).is_dir() else 0 for lg in voice.LANGS}
    s["cue_count"] = len(CUES)
    s["fallback"] = "clips, then browser speech" if not s["enabled"] else "browser speech if Sarvam fails"
    return s


@router.get("/cues")
def cues(lang: str | None = None):
    data = all_cues()
    if lang:
        lg = _lang_or_400(lang)
        data = {"lang": lg, "order": data["order"],
                "cues": {k: cue_text(k, lg) for k in data["order"]}}
    return data


# ----------------------------------------------------------------------------- audio

@router.post("/tts")
def tts(body: dict = Body(...)):
    text = str(body.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "text is required")
    if len(text) > MAX_TTS_CHARS:
        raise HTTPException(400, f"text is longer than {MAX_TTS_CHARS} characters")
    lang = _lang_or_400(body.get("language") or body.get("lang"))
    path = voice.tts(text, lang, speaker=body.get("speaker"), pace=body.get("pace"),
                     fmt=body.get("format"))
    if not path:
        why = "no SARVAM_API_KEY" if not voice.enabled() else "Sarvam TTS failed"
        return _browser_fallback(text, lang, 503, why)
    return _audio_response(path)


@router.get("/audio/{name}")
def audio(name: str):
    if not _SAFE_NAME.match(name):
        raise HTTPException(404, "no such audio")
    path = voice.TTS_CACHE_DIR / name
    if not path.is_file():
        raise HTTPException(404, "no such audio (cache cleared?)")
    return _audio_response(str(path))


@router.get("/clip/{lang}/{cue}")
def clip(lang: str, cue: str):
    lg = _lang_or_400(lang)
    cue = cue.rsplit(".", 1)[0]
    if not _SAFE_CUE.match(cue) or cue not in CUES:
        raise HTTPException(404, f"unknown cue {cue!r}")
    for ext in ("mp3", "wav"):
        f = AUDIO_DIR / lg / f"{cue}.{ext}"
        if f.is_file():
            return FileResponse(str(f), media_type=MEDIA[ext],
                                headers={"Cache-Control": "public, max-age=86400"})
    text = cue_text(cue, lg)
    path = voice.tts(text, lg) if voice.enabled() else None
    if path:
        return _audio_response(path)
    return _browser_fallback(text, lg, 404, "no pre-made clip and no SARVAM_API_KEY")


# ----------------------------------------------------------------------------- text

@router.post("/translate")
def translate(body: dict = Body(...)):
    text = str(body.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "text is required")
    if len(text) > 5000:
        raise HTTPException(400, "text is longer than 5000 characters")
    tgt = _lang_or_400(body.get("target") or body.get("tgt"))
    src_raw = body.get("source") or body.get("src")
    src = None if src_raw in (None, "", "auto") else _lang_or_400(src_raw)
    out = voice.translate(text, src, tgt)
    return {"text": out, "source": src or voice.detect_language(text), "target": tgt,
            "translated": out != text, "provider": "sarvam" if voice.enabled() else "none"}


@router.post("/detect")
def detect(body: dict = Body(...)):
    text = str(body.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "text is required")
    return {"lang": voice.detect_language(text), "script_guess": voice.script_language(text),
            "provider": "sarvam" if voice.enabled() else "script"}


# ----------------------------------------------------------------------------- push-to-talk

_FAQ_HOW_OFTEN = re.compile(
    r"how (many|often|much)|kitn[ie]|कितन|कब कब|how long|কতবার|எத்தனை|ఎన్ని|ಎಷ್ಟು|എത്ര|किती|કેટલ|ਕਿੰਨ|କେତେ",
    re.I)


def _notify_nurse(patient: dict | None, kind: str, text: str):
    """Log for the nurse (message log) and, if the comms module offers it, raise an alert."""
    if not patient:
        return
    try:
        service.log_message(patient, kind, "nurse", None, text, False, True)
    except Exception as e:
        log.warning("could not log voice question: %s", e)
    try:  # optional hook for the comms agent's alert inbox / escalation ladder
        from . import comms  # type: ignore
        fn = getattr(comms, "raise_alert", None)
        if callable(fn):
            fn(patient["id"], kind=kind, text=text,
               severity="red" if kind == "red_flag" else "info")
    except Exception as e:
        log.debug("comms alert hook not used: %s", e)


@router.post("/stt")
async def stt(file: UploadFile | None = File(None), language: str | None = Form(None),
              patient_id: int | None = Form(None), text: str | None = Form(None)):
    """Patient's spoken question -> {text, lang, red_flag, reply, reply_audio_url, ...}.
    `text` may be sent instead of audio (typed question, or a demo without a Sarvam key)."""
    patient = service.get_patient_row(patient_id) if patient_id else None
    if patient_id and not patient:
        raise HTTPException(404, f"patient {patient_id} not found")
    hint = voice.norm_lang(language) or (get_prefs(patient_id, patient)["language"] if patient else None)
    res = {"text": "", "lang": hint, "ok": False, "source": "none"}
    if text and text.strip():
        t = text.strip()[:1000]
        res = {"text": t, "lang": voice.detect_language(t) or hint, "ok": True, "source": "typed"}
    elif file is not None:
        audio_bytes = await file.read()
        if len(audio_bytes) > MAX_STT_BYTES:
            raise HTTPException(413, "audio too long – keep questions under 30 seconds")
        res = voice.stt(audio_bytes, hint, file.filename or "audio.webm")
    else:
        raise HTTPException(400, "send an audio file (field 'file') or 'text'")

    heard = res.get("text") or ""
    lang = res.get("lang") or hint or "en"
    # Romanised Indian text ("mujhe bukhar hai") looks English: answer in the chosen language.
    if lang == "en" and hint and hint != "en" and voice.script_language(heard) in ("en", None):
        lang = hint
    if not res.get("ok"):
        return JSONResponse({"text": "", "lang": lang, "red_flag": False, "reply": None,
                             "reply_audio_url": None, "ok": False, "fallback": "browser",
                             "error": res.get("error") or "speech-to-text unavailable",
                             "source": res.get("source")}, status_code=503)

    english = heard if lang == "en" else voice.translate(heard, lang, "en")
    flagged = voice.red_flag(heard) or voice.red_flag(english)
    if flagged:
        cue = "red_flag"
    elif _FAQ_HOW_OFTEN.search(heard) or _FAQ_HOW_OFTEN.search(english):
        cue = "faq_how_often"
    else:
        cue = "question_noted"
    reply = cue_text(cue, lang)
    reply_path = voice.tts(reply, lang) if heard else None
    if heard:
        who = patient["name"] if patient else "Patient"
        tag = "RED FLAG – " if flagged else ""
        note = f"{tag}Voice question from {who}: \"{heard}\""
        if english and english != heard:
            note += f" (English: \"{english}\")"
        _notify_nurse(patient, "red_flag" if flagged else "voice_question", note)
    return {"text": heard, "lang": lang, "english": english, "red_flag": flagged,
            "reply": reply, "reply_cue": cue, "reply_audio_url": voice.tts_url(reply_path),
            "ok": True, "source": res.get("source"), "nurse_notified": bool(patient and heard)}


# ----------------------------------------------------------------------------- voice-note summary

@router.post("/summary-audio/{pid}")
def summary_audio(pid: int, body: dict | None = Body(None)):
    """Evening summary as a voice note in the patient's language (for WhatsApp voice notes and
    automated calls). -> {text, lang, source, translated, audio_url, public_url, fallback?}"""
    d = service.patient_detail(pid)
    if d is None:
        raise HTTPException(404, f"patient {pid} not found")
    body = body or {}
    prefs_ = get_prefs(pid, d)
    lang = _lang_or_400(body.get("language"), prefs_["language"])
    stats = service.summary_stats(d)
    base_lang = lang if lang in llm.LANG_NAMES else "en"
    s = llm.summarize(stats, base_lang)
    text, translated = s["text"], False
    # llm.summarize falls back to an en/hi template; translate if the text isn't in `lang` yet
    actual = voice.script_language(text) or "en"
    if actual != lang and not (lang == "mr" and actual == "hi"):
        out = voice.translate(text, actual, lang)
        translated = out != text
        text = out
    path = voice.tts(text, lang, speaker=body.get("speaker") or prefs_["speaker"],
                     pace=body.get("pace") or prefs_["pace"])
    res = {"patient_id": pid, "text": text, "lang": lang, "bcp47": voice.bcp47(lang),
           "source": s.get("source"), "translated": translated,
           "text_lang": lang if (translated or actual == lang) else actual,
           "audio_url": voice.tts_url(path), "public_url": voice.public_url(path)}
    if not path:
        # English text for browsers that have no voice in `lang` (see web/js/voice.js)
        res["text_en"] = text if res["text_lang"] == "en" else llm.template_summary(stats, "en")
        res["fallback"] = "browser"
        res["note"] = ("no SARVAM_API_KEY – the browser reads the text aloud instead"
                       if not voice.enabled() else "Sarvam TTS failed – browser voice used")
    return res
