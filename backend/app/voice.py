"""Voice & language via Sarvam AI (TTS, STT, translate, language ID) with offline fallbacks.

Stable interface (used by routes_voice.py and the comms agent – keep these signatures):
    enabled() -> bool
    tts(text, lang, speaker=None, pace=None, fmt=None) -> str | None   path to a cached audio file
    tts_url(path) -> str                                                 "/api/voice/audio/<file>"
    stt(audio_bytes, lang=None, filename="audio.webm") -> dict           {text, lang, ok, source, error?}
    translate(text, src, tgt) -> str                                     original text on any failure
    detect_language(text) -> str | None                                  short code, e.g. "hi"
    norm_lang(lang) -> str | None                                        "hi-IN"/"Hindi"/"hi" -> "hi"
    red_flag(text) -> bool                                               red-flag words, 11 languages
    red_flag_message(lang) -> str                                        fixed nurse/112 message

Nothing here ever raises to callers. With no SARVAM_API_KEY: tts -> None (the browser speaks
instead), stt -> {ok: False, text: ""}, translate -> the original text, detect_language -> a
Unicode-script guess. API facts (verified 9 Oct 2026) are in docs/VOICE.md.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import logging
import re
import threading
import unicodedata
import wave
from pathlib import Path

from .config import DATA_DIR, env
from .voice_cues import LANG_ORDER, RED_FLAG_EN, cue_text

log = logging.getLogger("spirobuddy.voice")

API_BASE = "https://api.sarvam.ai"
TTS_CACHE_DIR = DATA_DIR / "tts_cache"
_TRANSLATE_CACHE_FILE = DATA_DIR / "translate_cache.json"
TTS_MAX_CHARS = 2500          # bulbul:v3 / v4-flash per request
TRANSLATE_MAX_CHARS = 900     # mayura:v1 allows 1000; keep a margin
LID_MAX_CHARS = 1000

# short code -> Sarvam BCP-47 code, names, and the calm per-language voices recommended for
# bulbul:v3 in Sarvam's "Bulbul v3 best practices" (female first: warm, calm for elderly users).
LANGS: dict[str, dict] = {
    "en": {"code": "en-IN", "name": "English", "native": "English", "female": "ishita", "male": "ratan"},
    "hi": {"code": "hi-IN", "name": "Hindi", "native": "हिन्दी", "female": "priya", "male": "shubh"},
    "bn": {"code": "bn-IN", "name": "Bengali", "native": "বাংলা", "female": "roopa", "male": "rehan"},
    "ta": {"code": "ta-IN", "name": "Tamil", "native": "தமிழ்", "female": "ishita", "male": "ratan"},
    "te": {"code": "te-IN", "name": "Telugu", "native": "తెలుగు", "female": "neha", "male": "shubh"},
    "kn": {"code": "kn-IN", "name": "Kannada", "native": "ಕನ್ನಡ", "female": "neha", "male": "shubh"},
    "ml": {"code": "ml-IN", "name": "Malayalam", "native": "മലയാളം", "female": "pooja", "male": "shubh"},
    "mr": {"code": "mr-IN", "name": "Marathi", "native": "मराठी", "female": "priya", "male": "ratan"},
    "gu": {"code": "gu-IN", "name": "Gujarati", "native": "ગુજરાતી", "female": "priya", "male": "ratan"},
    "pa": {"code": "pa-IN", "name": "Punjabi", "native": "ਪੰਜਾਬੀ", "female": "roopa", "male": "mani"},
    "or": {"code": "od-IN", "name": "Odia", "native": "ଓଡ଼ିଆ", "female": "ritu", "male": "shubh"},
}
assert list(LANGS) == LANG_ORDER

# Every bulbul:v3 speaker (docs.sarvam.ai/api-reference/text-to-speech/convert). "varun" is left
# out on purpose: Sarvam marks it as a dramatic/suspense voice.
V3_SPEAKERS = ["shubh", "aditya", "ritu", "priya", "neha", "rahul", "pooja", "rohan", "simran",
               "kavya", "amit", "dev", "ishita", "shreya", "ratan", "manan", "sumit", "roopa",
               "kabir", "aayan", "ashutosh", "advait", "anand", "tanya", "tarun", "sunny", "mani",
               "gokul", "vijay", "shruti", "suhani", "mohit", "kavitha", "rehan", "soham", "rupali"]

_ALIASES = {"od": "or", "odia": "or", "oriya": "or", "english": "en", "hindi": "hi",
            "bengali": "bn", "bangla": "bn", "tamil": "ta", "telugu": "te", "kannada": "kn",
            "malayalam": "ml", "marathi": "mr", "gujarati": "gu", "punjabi": "pa"}


# ----------------------------------------------------------------------------- settings

def enabled() -> bool:
    return bool(env("SARVAM_API_KEY"))


def tts_model() -> str:
    return env("SARVAM_TTS_MODEL", "bulbul:v3")


def stt_model() -> str:
    return env("SARVAM_STT_MODEL", "saaras:v4")


def translate_model() -> str:
    return env("SARVAM_TRANSLATE_MODEL", "mayura:v1")


def default_pace() -> float:
    """0.85 = Sarvam's "relaxed" range (0.8-0.9) for elderly listeners (KNOWLEDGE_BASE F-VOICE-11)."""
    try:
        return min(2.0, max(0.5, float(env("SARVAM_TTS_PACE", "0.85"))))
    except ValueError:
        return 0.85


def default_temperature() -> float | None:
    """Bulbul v3 / v4-flash `temperature` (0.01-1.0, API default 0.6; docs/VOICE.md 1.1).
    0.7 = Sarvam's "warm" range for wellness content. None for models without it (v2)."""
    if not tts_model().startswith(("bulbul:v3", "bulbul:v4")):
        return None
    try:
        return min(1.0, max(0.01, float(env("SARVAM_TTS_TEMPERATURE", "0.7"))))
    except ValueError:
        return 0.7


def default_codec() -> str:
    c = env("SARVAM_TTS_CODEC", "mp3").lower()
    return c if c in ("mp3", "wav") else "mp3"


def _timeout() -> float:
    try:
        return float(env("SARVAM_TIMEOUT_S", "25"))
    except ValueError:
        return 25.0


def norm_lang(lang) -> str | None:
    """'hi', 'hi-IN', 'HI_in', 'Hindi', 'od-IN' -> our short code; None if unknown."""
    if not lang:
        return None
    s = str(lang).strip().lower().replace("_", "-")
    s = _ALIASES.get(s, s)
    s = s.split("-")[0]
    s = _ALIASES.get(s, s)
    return s if s in LANGS else None


def bcp47(lang) -> str:
    return LANGS[norm_lang(lang) or "en"]["code"]


def speaker_for(lang, speaker: str | None = None) -> str:
    """A valid bulbul voice: the requested one, else SARVAM_TTS_SPEAKER, else the per-language
    recommended voice of VOICE_GENDER (female by default)."""
    model = tts_model()
    for cand in (speaker, env("SARVAM_TTS_SPEAKER")):
        if cand:
            c = cand.strip().lower()
            if model == "bulbul:v4-flash" and "_" in c:
                return c
            if c in V3_SPEAKERS and model != "bulbul:v4-flash":
                return c
    gender = "male" if env("VOICE_GENDER", "female").lower().startswith("m") else "female"
    return LANGS[norm_lang(lang) or "en"][gender]


def status() -> dict:
    return {
        "enabled": enabled(),
        "provider": "sarvam" if enabled() else "browser",
        "tts_model": tts_model(), "stt_model": stt_model(), "translate_model": translate_model(),
        "pace": default_pace(), "temperature": default_temperature(), "codec": default_codec(),
        "languages": [{"lang": k, "code": v["code"], "name": v["name"], "native": v["native"],
                       "speaker": speaker_for(k)} for k, v in LANGS.items()],
        "voices": {k: {"female": v["female"], "male": v["male"]} for k, v in LANGS.items()},
        "all_speakers": V3_SPEAKERS,
    }


# ----------------------------------------------------------------------------- HTTP

def _post(path: str, *, json_body: dict | None = None, files=None, data=None) -> dict:
    import httpx
    headers = {"api-subscription-key": env("SARVAM_API_KEY")}
    with httpx.Client(base_url=API_BASE, timeout=_timeout()) as c:
        r = c.post(path, json=json_body, files=files, data=data, headers=headers)
    if r.status_code >= 400:
        try:
            err = r.json().get("error") or {}
            msg = f"{err.get('code', '')}: {err.get('message', '')}".strip(": ")
        except Exception:
            msg = r.text[:200]
        hint = {402: " (Sarvam credits used up – add credits in the dashboard)",
                403: " (key rejected – check SARVAM_API_KEY)",
                429: " (rate limit – wait a minute)"}.get(r.status_code, "")
        raise RuntimeError(f"Sarvam {path} HTTP {r.status_code}: {msg}{hint}")
    return r.json()


# ----------------------------------------------------------------------------- TTS

def _split_text(text: str, limit: int) -> list[str]:
    """Split at sentence ends (., !, ?, ।, danda) so each part fits the per-request limit."""
    text = text.strip()
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for sent in re.split(r"(?<=[.!?।॥])\s+", text):
        while len(sent) > limit:                      # one giant sentence: hard cut at a space
            cut = sent.rfind(" ", 0, limit)
            cut = cut if cut > limit // 2 else limit
            parts.append(sent[:cut].strip())
            sent = sent[cut:].strip()
        if len(cur) + len(sent) + 1 > limit:
            parts.append(cur.strip())
            cur = sent
        else:
            cur = f"{cur} {sent}" if cur else sent
    if cur.strip():
        parts.append(cur.strip())
    return [p for p in parts if p]


def _join_wavs(blobs: list[bytes]) -> bytes:
    out = io.BytesIO()
    params, frames = None, []
    for b in blobs:
        with wave.open(io.BytesIO(b)) as w:
            params = params or w.getparams()
            frames.append(w.readframes(w.getnframes()))
    with wave.open(out, "wb") as w:
        w.setparams(params)
        for f in frames:
            w.writeframes(f)
    return out.getvalue()


def cache_key(text: str, lang: str, speaker: str, pace: float, codec: str,
              sample_rate: int | None = None) -> str:
    temp = default_temperature()
    raw = "|".join([tts_model(), bcp47(lang), speaker, f"{pace:.2f}", codec,
                    str(sample_rate or ""), "" if temp is None else f"t{temp:.2f}", text.strip()])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:24]


def tts(text: str, lang: str, speaker: str | None = None, pace: float | None = None,
        fmt: str | None = None, sample_rate: int | None = None) -> str | None:
    """Speak `text` in `lang` -> path of a cached audio file (mp3 by default), or None when
    there is no key / the call failed (callers then use pre-made clips or browser speech).
    Same text + language + voice + pace = same file, so repeats are free and instant.
    `sample_rate` (8000–48000) is optional, e.g. 8000 for phone calls."""
    try:
        text = (text or "").strip()
        if not text:
            return None
        lang = norm_lang(lang) or "en"
        spk = speaker_for(lang, speaker)
        p = default_pace() if pace is None else min(2.0, max(0.5, float(pace)))
        codec = fmt if fmt in ("mp3", "wav") else default_codec()
        chunks = _split_text(text, TTS_MAX_CHARS)
        if len(chunks) > 1:
            codec = "wav"                              # wav joins cleanly; mp3 frames might not
        key = cache_key(text, lang, spk, p, codec, sample_rate)
        path = TTS_CACHE_DIR / f"{key}.{codec}"
        if path.exists() and path.stat().st_size > 0:
            return str(path)
        if not enabled():
            return None
        blobs = []
        for chunk in chunks:
            body = {"text": chunk, "language_code": bcp47(lang), "speaker": spk, "pace": p,
                    "model": tts_model(), "output_audio_codec": codec}
            if sample_rate:
                body["speech_sample_rate"] = int(sample_rate)
            temp = default_temperature()
            if temp is not None:
                body["temperature"] = temp
            res = _post("/text-to-speech", json_body=body)
            audios = res.get("audios") or []
            if not audios:
                raise RuntimeError("Sarvam TTS returned no audio")
            blobs.append(b"".join(base64.b64decode(a) for a in audios))
        data = blobs[0] if len(blobs) == 1 else _join_wavs(blobs)
        TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        tmp.write_bytes(data)
        tmp.replace(path)
        log.info("TTS %s %s %d chars -> %s", lang, spk, len(text), path.name)
        return str(path)
    except Exception as e:
        log.warning("TTS failed (%s): %s", lang, e)
        return None


def tts_url(path: str | None) -> str | None:
    """Server URL for a file returned by tts(). Add PUBLIC_BASE_URL for WhatsApp/Twilio."""
    if not path:
        return None
    return f"/api/voice/audio/{Path(path).name}"


def public_url(path: str | None) -> str | None:
    rel = tts_url(path)
    base = env("PUBLIC_BASE_URL").rstrip("/")
    return f"{base}{rel}" if rel and base else None


def tts_cue(cue: str, lang: str, **kw) -> str | None:
    """TTS of a cue from voice_cues.py (handy for the comms agent's calls)."""
    t = cue_text(cue, norm_lang(lang) or "en")
    return tts(t, lang, **kw) if t else None


# ----------------------------------------------------------------------------- STT

STT_KEYTERMS = ["SpiroBuddy", "spirometer", "incentive spirometer", "nurse", "112"]


def stt(audio_bytes: bytes, lang: str | None = None, filename: str = "audio.webm") -> dict:
    """Speech -> text. -> {text, lang (short code or None), ok, source, error?}.
    Sarvam REST accepts up to 30 seconds of audio (WAV/MP3/OGG/WebM/M4A…)."""
    out = {"text": "", "lang": norm_lang(lang), "ok": False, "source": "none"}
    if not audio_bytes:
        out["error"] = "no audio received"
        return out
    if not enabled():
        out["error"] = "speech-to-text needs SARVAM_API_KEY"
        return out
    try:
        model = stt_model()
        data = {"model": model, "language_code": bcp47(lang) if norm_lang(lang) else "unknown"}
        if model.startswith("saaras:v4"):
            data["keyterms"] = json.dumps(STT_KEYTERMS)
        ctype = _audio_mime(filename)
        res = _post("/speech-to-text", files={"file": (filename or "audio.webm", audio_bytes, ctype)},
                    data=data)
        out.update(text=(res.get("transcript") or "").strip(), ok=True, source="sarvam",
                   lang=norm_lang(res.get("language_code")) or out["lang"])
        if out["text"] and not out["lang"]:
            out["lang"] = detect_language(out["text"])
        return out
    except Exception as e:
        log.warning("STT failed: %s", e)
        out["error"] = str(e)[:300]
        return out


def _audio_mime(filename: str) -> str:
    ext = (filename or "").rsplit(".", 1)[-1].lower()
    return {"wav": "audio/wav", "mp3": "audio/mpeg", "ogg": "audio/ogg", "oga": "audio/ogg",
            "opus": "audio/ogg", "webm": "audio/webm", "m4a": "audio/mp4", "mp4": "audio/mp4",
            "aac": "audio/aac", "flac": "audio/flac", "amr": "audio/amr"}.get(ext, "audio/webm")


# ----------------------------------------------------------------------------- translate

_tcache: dict[str, str] | None = None
_tlock = threading.Lock()


def _tcache_load() -> dict:
    global _tcache
    if _tcache is None:
        try:
            _tcache = json.loads(_TRANSLATE_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            _tcache = {}
    return _tcache


def _tcache_put(k: str, v: str):
    with _tlock:
        c = _tcache_load()
        c[k] = v
        try:
            _TRANSLATE_CACHE_FILE.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            log.debug("translate cache write failed: %s", e)


def translate(text: str, src: str | None, tgt: str) -> str:
    """Translate between our 11 languages. src may be None/'auto'. Returns the original text
    when there is no key, the languages match, or anything fails."""
    try:
        text = (text or "").strip()
        t = norm_lang(tgt)
        s = norm_lang(src) if src and str(src).lower() != "auto" else None
        if not text or not t or s == t:
            return text
        key = hashlib.sha1(f"{translate_model()}|{s or 'auto'}|{t}|{text}".encode()).hexdigest()
        cached = _tcache_load().get(key)
        if cached:
            return cached
        if not enabled():
            return text
        if s is None:
            s = detect_language(text)
            if s == t:
                return text
        model = translate_model()
        out = []
        for chunk in _split_text(text, TRANSLATE_MAX_CHARS):
            body = {"input": chunk, "source_language_code": bcp47(s) if s else "auto",
                    "target_language_code": bcp47(t), "model": model, "mode": "formal",
                    "numerals_format": "international"}
            if model == "sarvam-translate:v1" and body["source_language_code"] == "auto":
                body["source_language_code"] = "en-IN"
            res = _post("/translate", json_body=body)
            out.append((res.get("translated_text") or "").strip())
        result = " ".join(x for x in out if x) or text
        _tcache_put(key, result)
        return result
    except Exception as e:
        log.warning("translate failed (%s->%s): %s", src, tgt, e)
        return text


# ----------------------------------------------------------------------------- language ID

_SCRIPT_RANGES = [  # (first, last, lang) – Unicode blocks
    (0x0980, 0x09FF, "bn"), (0x0A00, 0x0A7F, "pa"), (0x0A80, 0x0AFF, "gu"),
    (0x0B00, 0x0B7F, "or"), (0x0B80, 0x0BFF, "ta"), (0x0C00, 0x0C7F, "te"),
    (0x0C80, 0x0CFF, "kn"), (0x0D00, 0x0D7F, "ml"), (0x0900, 0x097F, "hi"),
]
_MARATHI_HINTS = re.compile(r"आहे|आहात|नाही|आणि|मला|तुम्ही|काय|झाल|श्वास")


def script_language(text: str) -> str | None:
    """Offline guess from the writing system. Devanagari -> Hindi unless Marathi words show."""
    counts: dict[str, int] = {}
    latin = 0
    for ch in text or "":
        o = ord(ch)
        if ch.isascii() and ch.isalpha():
            latin += 1
            continue
        for a, b, lg in _SCRIPT_RANGES:
            if a <= o <= b:
                counts[lg] = counts.get(lg, 0) + 1
                break
    if counts:
        best = max(counts, key=counts.get)
        if best == "hi" and _MARATHI_HINTS.search(text):
            return "mr"
        return best
    return "en" if latin else None


def detect_language(text: str) -> str | None:
    """Sarvam language ID when a key exists, else (or on failure) the script guess."""
    text = (text or "").strip()
    if not text:
        return None
    if enabled():
        try:
            res = _post("/text-lid", json_body={"input": text[:LID_MAX_CHARS]})
            lg = norm_lang(res.get("language_code"))
            if lg:
                return lg
        except Exception as e:
            log.warning("language ID failed, using script guess: %s", e)
    return script_language(text)


# ----------------------------------------------------------------------------- red flags

# Words that must always reach a person. Deliberately broad: a false alarm is far safer than a
# missed one. Romanised Hindi ("Hinglish") is included because many people type that way.
RED_FLAG_WORDS: dict[str, list[str]] = {
    # Exact romanized phrases from the existing critical regressions. This is limited
    # deterministic coverage, not a complete vocabulary or native-speaker validation.
    "ta_latn": ["nenju vali", "moochu thinaral", "kaichal"],
    "ml_latn": ["nenchu vedana", "swasam muttunnu", "sahayam"],
    "en": ["chest pain", "pain in my chest", "pain in chest", "can't breathe", "cant breathe",
           "cannot breathe", "can not breathe", "unable to breathe", "not able to breathe",
           "difficulty breathing", "trouble breathing", "hard to breathe", "short of breath",
           "shortness of breath", "breathless", "out of breath", "choking", "suffocat",
           "blood", "bleeding", "fever", "high temperature", "faint", "fainted", "dizzy",
           "unconscious", "passed out", "collapse", "blue lips", "lips are blue", "heart attack",
           "emergency", "help me", "ambulance", "severe pain", "very bad pain", "confused",
           "palpitation", "racing heart",
           # 2.0 (spec §2): phrasings the review found missing – typos and everyday wording
           "cant breath", "can't breath", "cannot breath", "can not breath", "difficulty in breathing",
           "difficult to breathe", "difficulty to breathe", "breathing difficulty", "breathing problem",
           "problem breathing", "chest hurt", "chest is hurting", "chest really hurt", "hurts in my chest",
           "took too many", "taken too many", "take too many", "too many tablets", "too many pills",
           "too many medicines", "overdose", "rash"],
    "hi_latn": ["seene mein dard", "sine me dard", "seene me dard", "chhati mein dard",
                "chati me dard", "saans nahi", "sans nahi", "saans lene mein takleef",
                "saans phool", "sans phool", "dam ghut", "khoon", "bukhar", "bukhaar",
                "chakkar", "behosh", "madad karo", "bachao",
                # 2.0: can't breathe / difficulty breathing / chest hurts / too many tablets /
                # rash / bleeding / fainted, as people type them in Roman letters
                "saans nahin", "sans nahin", "saans nhi", "sans nhi", "saans ruk",
                "saans lene me", "sans lene me", "saans lene mein", "sans lene mein",
                "saans lene mai", "saans me takleef", "saans mein takleef", "saans me dikkat",
                "saans mein dikkat", "sans me dikkat", "seena dukh", "sina dukh", "chhati dukh",
                "chati dukh", "seene me dukh", "seene mein dukh", "chest me dard", "chest mein dard",
                "chhati me dard", "chati mein dard",
                "zyada goli", "jyada goli", "zyada tablet", "jyada tablet", "zyada dawa",
                "jyada dawa", "bahut saari goli", "bahut sari goli", "chakatte", "chakte",
                "lal daane", "laal daane", "lal dane", "laal dane", "daane nikal", "dane nikal",
                "sharir par daane", "sharir par dane", "khun beh", "khun nikal", "khun aa raha",
                "behos ho", "hosh kho"],
    "hi": ["सीने में दर्द", "सीने मे दर्द", "छाती में दर्द", "छाती मे दर्द", "साँस नहीं",
           "सांस नहीं", "साँस लेने में", "सांस लेने में", "साँस फूल", "सांस फूल", "दम घुट",
           "खून", "बुखार", "चक्कर", "बेहोश", "मदद करो", "बचाओ", "घबराहट", "एम्बुलेंस",
           # 2.0: the same seven meanings in Devanagari (with common spelling variants)
           "साँस नही", "सांस नही", "साँस लेने मे", "सांस लेने मे", "साँस में तकलीफ",
           "सांस में तकलीफ", "साँस में दिक्कत", "सांस में दिक्कत", "सीना दुख", "छाती दुख",
           "सीने में दुख", "छाती में दुख", "सीने में तकलीफ", "ज्यादा गोली", "ज़्यादा गोली",
           "ज्यादा गोलि", "ज़्यादा गोलि", "ज्यादा दवा", "ज़्यादा दवा", "बहुत सारी गोलि",
           "बहुत ज्यादा गोलि", "ओवरडोज", "चकत्ते", "चकत्ता", "लाल दाने", "दाने निकल",
           "शरीर पर दाने", "रैश", "ख़ून", "रक्तस्राव", "ब्लीडिंग", "होश खो", "गश खा", "मूर्छित"],
    "bn": ["বুকে ব্যথা", "বুকে ব্যাথা", "শ্বাসকষ্ট", "শ্বাস নিতে পারছি না", "দম বন্ধ", "রক্ত",
           "জ্বর", "মাথা ঘোরা", "মাথা ঘুরছে", "অজ্ঞান", "বাঁচাও"],
    "ta": ["நெஞ்சு வலி", "நெஞ்சுவலி", "மார்பு வலி", "மூச்சுத் திணறல்", "மூச்சு திணறல்",
           "மூச்சு விட முடியவில்லை", "இரத்தம்", "ரத்தம்", "காய்ச்சல்", "மயக்கம்", "தலைசுற்றல்",
           "தலை சுற்றுகிறது",
           # 2.0: can't breathe / difficulty breathing / chest hurts / too many tablets / rash /
           # bleeding / fainted. Written without a native speaker: NEEDS A NATIVE-SPEAKER CHECK.
           "மூச்சு விட முடியல", "மூச்சுவிட முடியவில்லை", "மூச்சுவிட முடியல", "மூச்சு வரவில்லை",
           "மூச்சு வரல", "மூச்சு அடைக்கு", "சுவாசிக்க முடியவில்லை", "சுவாசிக்க முடியல",
           "மூச்சு விடுவதில் சிரம", "மூச்சு விட சிரம", "மூச்சுவிட சிரம", "மூச்சு விட கஷ்ட",
           "சுவாசிப்பதில் சிரம", "மூச்சு திணறு", "மூச்சுத் திணறு", "மூச்சு வாங்கு",
           "நெஞ்சில் வலி", "நெஞ்சுல வலி", "மார்பில் வலி", "அதிக மாத்திரை", "அதிகமாக மாத்திரை",
           "நிறைய மாத்திரை", "மாத்திரை அதிகமா", "அதிக மருந்து", "அதிகமாக மருந்து", "மருந்து அதிகமா",
           "தடிப்பு", "சொறி", "இரத்தப்போக்கு", "ரத்தப்போக்கு", "இரத்தக்கசிவு", "ரத்தக்கசிவு",
           "மயங்கி", "மயக்கமா", "நினைவிழ"],
    "te": ["ఛాతీ నొప్పి", "ఛాతి నొప్పి", "గుండె నొప్పి", "శ్వాస ఆడటం లేదు", "ఊపిరి ఆడటం లేదు",
           "ఆయాసం", "రక్తం", "జ్వరం", "కళ్ళు తిరుగు", "తల తిరుగు", "స్పృహ"],
    "kn": ["ಎದೆ ನೋವು", "ಎದೆನೋವು", "ಉಸಿರಾಟದ ತೊಂದರೆ", "ಉಸಿರು ಕಟ್ಟು", "ಉಸಿರಾಡಲು ಆಗುತ್ತಿಲ್ಲ",
           "ರಕ್ತ", "ಜ್ವರ", "ತಲೆ ಸುತ್ತು", "ಪ್ರಜ್ಞೆ"],
    "ml": ["നെഞ്ചുവേദന", "നെഞ്ച് വേദന", "ശ്വാസം മുട്ട", "ശ്വാസതടസ്സം", "ശ്വസിക്കാൻ പറ്റുന്നില്ല",
           "രക്തം", "ചോര", "പനി", "തലകറക്ക", "ബോധം",
           # 2.0: can't breathe / difficulty breathing / chest hurts / too many tablets / rash /
           # bleeding / fainted. Written without a native speaker: NEEDS A NATIVE-SPEAKER CHECK.
           "ശ്വാസം കിട്ടുന്നില്ല", "ശ്വാസം കിട്ടണില്ല", "ശ്വാസം എടുക്കാൻ പറ്റുന്നില്ല",
           "ശ്വാസമെടുക്കാൻ പറ്റുന്നില്ല", "ശ്വാസം എടുക്കാൻ കഴിയുന്നില്ല",
           "ശ്വാസമെടുക്കാൻ കഴിയുന്നില്ല", "ശ്വസിക്കാൻ കഴിയുന്നില്ല", "ശ്വാസ തടസ്സം", "ശ്വാസംമുട്ട",
           "ശ്വസിക്കാൻ ബുദ്ധിമുട്ട", "ശ്വാസമെടുക്കാൻ ബുദ്ധിമുട്ട", "ശ്വാസം എടുക്കാൻ ബുദ്ധിമുട്ട",
           "നെഞ്ചിൽ വേദന", "നെഞ്ചു വേദന", "നെഞ്ചിന് വേദന", "കൂടുതൽ ഗുളിക", "അധികം ഗുളിക",
           "ഗുളിക കൂടുതൽ", "ഗുളിക അധികം", "ഒരുപാട് ഗുളിക", "കൂടുതൽ മരുന്ന", "മരുന്ന് കൂടുതൽ",
           "അമിതമായി മരുന്ന", "തിണർപ്പ", "തടിപ്പ", "ചുവന്ന പാട", "രക്തസ്രാവം", "ബ്ലീഡിംഗ്",
           "ബോധക്ഷയ", "ബോധരഹിത", "ബോധമില്ല", "തലകറങ്ങി", "കുഴഞ്ഞുവീണ", "കുഴഞ്ഞു വീണ"],
    "mr": ["छातीत दुख", "छातीत वेदना", "श्वास घेता येत नाही", "धाप", "दम लाग", "रक्त", "ताप",
           "चक्कर", "बेशुद्ध"],
    "gu": ["છાતીમાં દુખ", "છાતીમાં દુઃખ", "શ્વાસ લેવામાં તકલીફ", "શ્વાસ નથી", "હાંફ", "લોહી",
           "તાવ", "ચક્કર", "બેભાન"],
    "pa": ["ਛਾਤੀ ਵਿੱਚ ਦਰਦ", "ਛਾਤੀ ਵਿਚ ਦਰਦ", "ਸਾਹ ਨਹੀਂ", "ਸਾਹ ਚੜ੍ਹ", "ਸਾਹ ਲੈਣ ਵਿੱਚ", "ਖੂਨ",
           "ਖ਼ੂਨ", "ਬੁਖਾਰ", "ਬੁਖ਼ਾਰ", "ਚੱਕਰ", "ਬੇਹੋਸ਼"],
    "or": ["ଛାତି ଯନ୍ତ୍ରଣା", "ଛାତି ବିନ୍ଧା", "ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ", "ନିଶ୍ୱାସ ନେଇ ପାରୁନି", "ରକ୍ତ",
           "ଜ୍ୱର", "ମୁଣ୍ଡ ବୁଲା", "ବେହୋସ"],
}
_RF_NORMAL = [unicodedata.normalize("NFC", w).lower()
              for words in RED_FLAG_WORDS.values() for w in words]


_RF_PUNCT = re.compile(r"[\s\-_/.,;:!?।…\"()\[\]*]+")


def red_flag(text: str) -> bool:
    """True if the text contains any red-flag word in any of our languages. Extra spaces and
    punctuation between words ("chest-pain", double spaces) do not hide a red flag."""
    t = unicodedata.normalize("NFC", text or "").lower()
    t = t.replace("’", "'").replace("‘", "'")
    t = _RF_PUNCT.sub(" ", t)
    return any(w in t for w in _RF_NORMAL)


def red_flag_message(lang: str | None) -> str:
    return cue_text("red_flag", norm_lang(lang) or "en") or RED_FLAG_EN
