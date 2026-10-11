"""Gemini wrapper: AI reads, code schedules, a human approves (spec §11, plan §3.7).

Two reading jobs and one writing job:
    extract_prescription()  photo/PDF -> a DRAFT of what is written (never advice, never guesses)
    suggest_document()      photo/PDF -> only {kind, title, doc_date} (never a result or value)
    summarize_text()        the daily summary text when there is no Anthropic key (llm.py)

Safety and privacy rules that live here, in code:
  * Only the file goes to Gemini. The prompts are fixed text: no patient name, id or other data.
  * ai_allowed() must say yes first: a key, the hospital's AI switch, the patient's AI consent,
    and the daily / per-IP limits. Anything else -> {"ok": False, "reason": ...} and the caller
    uses the manual path (staff type the lines). That path must always work.
  * Only the fields we asked for are kept; anything extra the model adds is dropped.
  * Every call writes one ai_events row (ok or failed) with references, never content.
  * _call_model() is the ONE place that touches the SDK. Tests replace it; no test calls Google.
"""
from __future__ import annotations

import logging
import re
import threading
import time

from pydantic import BaseModel

from . import ai_register, service
from .config import (ai_daily_limit, ai_per_ip_hour, env, gemini_api_key, gemini_model,
                     gemini_timeout_s, today_str)

log = logging.getLogger("spirobuddy.ai_gemini")

PROVIDER = "gemini"
AI_MIMES = ("image/jpeg", "image/png", "image/webp", "application/pdf")
DOC_KINDS = ("prescription", "discharge_summary", "lab_report", "scan_report", "consent_form", "other")

# ----------------------------------------------------------------------------- prompts

RX_PROMPT_VERSION = "rx-v1"
RX_PROMPT_V1 = (
    "You transcribe medicine prescriptions. Copy exactly what is written. Do not correct "
    "spelling, do not add or remove medicines, do not infer missing values: use null and list "
    "the field in unclear_fields. Do not give advice, warnings or interpretations.\n"
    "\n"
    "Return JSON with these fields:\n"
    "- doctor_name, hospital_name, date, patient_name_on_paper: text exactly as written, or null.\n"
    "- handwritten: true if the medicine lines are written by hand, false if printed.\n"
    "- legibility: \"good\", \"fair\" or \"poor\".\n"
    "- lines: one entry per medicine line, in the order written, each with:\n"
    "  line_no (1, 2, 3...), drug_name, form (tablet, capsule, syrup... as written), strength, "
    "dose_qty, dose_unit, frequency_raw (for example \"1-0-1\", \"BD\", \"TDS\"), "
    "food_timing_raw, duration_raw, as_needed (true only if the paper says SOS, PRN or "
    "\"if needed\"), instructions_raw, confidence (0 to 1: how sure you are that you read this "
    "line correctly), unclear_fields (the names of the fields you could not read or that are "
    "missing), box_2d (the line's box as [ymin, xmin, ymax, xmax] on a 0-1000 scale, or null).\n"
    "Every text field is copied as written. If a value is not on the paper or cannot be read, "
    "use null and add the field name to unclear_fields. Never fill a gap from what is usual."
)

DOC_PROMPT_VERSION = "doc-v1"
DOC_PROMPT_V1 = (
    "You help file hospital papers. Look at this paper and return JSON with exactly three fields:\n"
    "- kind: one of prescription, discharge_summary, lab_report, scan_report, consent_form, other.\n"
    "- title: a short neutral name for the paper, at most 8 words, with no person's name.\n"
    "- doc_date: the date printed on the paper as YYYY-MM-DD, or null if there is none.\n"
    "Return nothing else. Do not read out, summarise or interpret anything written in the paper."
)


class RxLine(BaseModel):
    line_no: int | None
    drug_name: str | None
    form: str | None
    strength: str | None
    dose_qty: str | None            # as written ("1", "½", "1½"); the normaliser turns it into a number
    dose_unit: str | None
    frequency_raw: str | None
    food_timing_raw: str | None
    duration_raw: str | None
    as_needed: bool | None
    instructions_raw: str | None
    confidence: float | None
    unclear_fields: list[str]
    box_2d: list[int] | None


class RxDraft(BaseModel):
    doctor_name: str | None
    hospital_name: str | None
    date: str | None
    patient_name_on_paper: str | None
    handwritten: bool | None
    legibility: str | None
    lines: list[RxLine]


class DocSuggestion(BaseModel):
    kind: str | None
    title: str | None
    doc_date: str | None


RX_FIELDS = tuple(RxDraft.model_fields)
RX_LINE_FIELDS = tuple(RxLine.model_fields)
DOC_FIELDS = tuple(DocSuggestion.model_fields)          # ("kind", "title", "doc_date") – nothing else

# ----------------------------------------------------------------------------- switches and limits

REASON_NO_KEY = "No Gemini key – type the lines"
REASON_HOSPITAL_OFF = "AI is switched off for this hospital"
REASON_NO_CONSENT = "Patient chose no AI"
REASON_NO_CONSENT_ROW = "No AI consent recorded for this patient"
REASON_DAILY = "Daily AI limit reached"
REASON_IP = "Too many AI requests from this network – try again in an hour"
REASON_FILE = "AI can't read this kind of file – type the lines"
REASON_FAILED = "AI could not read this file – type the lines"

_lock = threading.Lock()
_day = {"date": "", "n": 0}                 # AI calls today, across the whole site
_ip_hits: dict[str, list[float]] = {}       # ip -> times of the calls in the last hour


def gemini_enabled() -> bool:
    return bool(gemini_api_key())


def reset_limits() -> None:
    """Forget the in-memory counters (tests, and the demo reset)."""
    with _lock:
        _day.update(date="", n=0)
        _ip_hits.clear()


def _limit_reason(ip: str | None) -> str | None:
    """None if another AI call is allowed now, else the plain reason. Does not count a call."""
    now = time.time()
    with _lock:
        if _day["date"] != today_str():
            _day.update(date=today_str(), n=0)
        if _day["n"] >= ai_daily_limit():
            return REASON_DAILY
        if ip:
            hits = [t for t in _ip_hits.get(ip, []) if now - t < 3600]
            _ip_hits[ip] = hits
            if len(hits) >= ai_per_ip_hour():
                return REASON_IP
    return None


def _count_call(ip: str | None) -> None:
    with _lock:
        if _day["date"] != today_str():
            _day.update(date=today_str(), n=0)
        _day["n"] += 1
        if ip:
            _ip_hits.setdefault(ip, []).append(time.time())
            if len(_ip_hits) > 5000:                        # keep the table small
                for k in [k for k, v in _ip_hits.items() if not v or time.time() - v[-1] > 3600]:
                    _ip_hits.pop(k, None)


def usage() -> dict:
    """Today's count and limit, for an admin page."""
    with _lock:
        n = _day["n"] if _day["date"] == today_str() else 0
    return {"today": n, "daily_limit": ai_daily_limit(), "per_ip_hour": ai_per_ip_hour()}


def _hospital_ai_on(hospital_id, patient_id) -> bool:
    """The hospital's "AI on or off" setting (default on). Read straight from the hospitals row."""
    st = service.store()
    if hospital_id is None and patient_id is not None:
        rows = st.select("patients", [("id", "eq", int(patient_id))], limit=1)
        hospital_id = rows[0].get("hospital_id") if rows else None
    if hospital_id is None:
        return True
    rows = st.select("hospitals", [("id", "eq", int(hospital_id))], limit=1)
    settings = (rows[0].get("settings") if rows else None) or {}
    return settings.get("ai_enabled", True) is not False


def consent_ai(patient_id) -> bool | None:
    """The patient's AI choice from their latest consent record: True, False, or None when
    there is no consent record at all. A withdrawn consent counts as "no"."""
    if patient_id is None:
        return None
    rows = service.store().select("consents", [("patient_id", "eq", int(patient_id))],
                                  order="id", desc=True, limit=1)
    if not rows:
        return None
    if rows[0].get("withdrawn_at"):
        return False
    return (rows[0].get("items") or {}).get("ai_use") is True


def ai_allowed(hospital_id, patient_id, ip) -> tuple[bool, str]:
    """(True, "") when an AI call may be made for this patient now, else (False, plain reason).
    Checks, in order: the key, the hospital's AI switch, the patient's AI consent, the limits.
    Any problem reading the settings counts as "not allowed" (the manual path is always safe)."""
    if not gemini_enabled():
        return False, REASON_NO_KEY
    try:
        if not _hospital_ai_on(hospital_id, patient_id):
            return False, REASON_HOSPITAL_OFF
        choice = consent_ai(patient_id)
    except Exception as e:
        log.warning("could not read the AI settings: %s", e)
        return False, REASON_NO_CONSENT_ROW
    if choice is None:
        return False, REASON_NO_CONSENT_ROW
    if choice is False:
        return False, REASON_NO_CONSENT
    limit = _limit_reason(ip)
    if limit:
        return False, limit
    return True, ""


# ----------------------------------------------------------------------------- the SDK call

_THINKING_LEVELS = ("MINIMAL", "LOW", "MEDIUM", "HIGH")


def _call_model(data: bytes | None, mime: str | None, prompt: str, schema=None):
    """The ONE place that touches the google-genai SDK.

    With a schema: sends the file + prompt and returns the parsed JSON as a dict.
    Without a schema (data may be None): returns the plain text.
    Raises on a timeout, an API error, or a finish reason other than STOP (blocked, cut off...).
    Temperature is left at the model default (Google's advice for Gemini 3); no thinking config
    unless the GEMINI_THINKING env var names a level."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=gemini_api_key())
    cfg: dict = {"http_options": types.HttpOptions(timeout=gemini_timeout_s() * 1000)}
    if schema is not None:
        cfg.update(response_mime_type="application/json", response_schema=schema)
    level = env("GEMINI_THINKING").upper()
    if level in _THINKING_LEVELS:
        cfg["thinking_config"] = types.ThinkingConfig(thinking_level=level)
    contents = [types.Part.from_bytes(data=data, mime_type=mime), prompt] if data is not None else prompt
    resp = client.models.generate_content(model=gemini_model(), contents=contents,
                                          config=types.GenerateContentConfig(**cfg))
    cands = resp.candidates or []
    finish = getattr(cands[0].finish_reason, "name", str(cands[0].finish_reason)) if cands else "NO_ANSWER"
    if finish != "STOP":
        raise RuntimeError(f"finish_reason={finish}")
    if schema is None:
        return (resp.text or "").strip()
    parsed = resp.parsed
    if isinstance(parsed, BaseModel):
        return parsed.model_dump()
    if isinstance(parsed, dict):
        return parsed
    import json
    return json.loads(resp.text or "")


def _safe_error(e: Exception) -> str:
    """A short error for the register: the kind of failure, never a key or any content."""
    msg = f"{type(e).__name__}: {e}"
    key = gemini_api_key()
    if key:
        msg = msg.replace(key, "***")
    return msg[:200]


def _run(data, mime, prompt, schema, ip):
    """Call the model with 1 retry. -> (result, error_text, latency_ms). Each try counts
    against the limits (it uses the free tier whether it works or not)."""
    t0 = time.monotonic()
    err = "no attempt"
    for attempt in (1, 2):
        _count_call(ip)
        try:
            out = _call_model(data, mime, prompt, schema)
            return out, None, int((time.monotonic() - t0) * 1000)
        except Exception as e:
            err = _safe_error(e)
            log.warning("Gemini call failed (try %d of 2): %s", attempt, err)
    return None, err, int((time.monotonic() - t0) * 1000)


# ----------------------------------------------------------------------------- cleaning the output

def _text(v, limit: int = 300) -> str | None:
    """A text field as written: trimmed, or None when empty."""
    if v is None:
        return None
    s = str(v).strip()
    return s[:limit] if s and s.lower() not in ("null", "none", "n/a") else None


def _clean_draft(raw) -> dict:
    """Keep only the fields of RX_PROMPT_V1 (anything else the model added is dropped), make
    the types safe, and number the lines. An empty value becomes None – it is never filled in –
    and a line with no readable medicine name always lists drug_name in unclear_fields."""
    if not isinstance(raw, dict):
        raise ValueError("the answer is not a JSON object")
    out = {k: _text(raw.get(k)) for k in ("doctor_name", "hospital_name", "date", "patient_name_on_paper")}
    out["handwritten"] = raw.get("handwritten") if isinstance(raw.get("handwritten"), bool) else None
    leg = (_text(raw.get("legibility")) or "").lower()
    out["legibility"] = leg if leg in ("good", "fair", "poor") else None
    lines = []
    for ln in (raw.get("lines") if isinstance(raw.get("lines"), list) else []):
        if not isinstance(ln, dict):
            continue
        i = len(lines) + 1
        row = {k: _text(ln.get(k)) for k in ("drug_name", "form", "strength", "dose_qty", "dose_unit",
                                             "frequency_raw", "food_timing_raw", "duration_raw",
                                             "instructions_raw")}
        row["line_no"] = i
        row["as_needed"] = ln.get("as_needed") if isinstance(ln.get("as_needed"), bool) else None
        try:
            conf = float(ln.get("confidence"))
            row["confidence"] = round(min(1.0, max(0.0, conf)), 2)
        except (TypeError, ValueError):
            row["confidence"] = None
        unclear = [str(x) for x in (ln.get("unclear_fields") or []) if str(x) in RX_LINE_FIELDS]
        if not row["drug_name"] and "drug_name" not in unclear:
            unclear.append("drug_name")
        row["unclear_fields"] = unclear
        box = ln.get("box_2d")
        try:
            row["box_2d"] = [int(x) for x in box] if isinstance(box, (list, tuple)) and len(box) == 4 else None
        except (TypeError, ValueError):
            row["box_2d"] = None
        lines.append(row)
    out["lines"] = lines
    return RxDraft.model_validate(out).model_dump()


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A title is only a filing label. If it carries a number or a result word, drop it.
_RESULT_WORDS = re.compile(
    r"\d|normal|abnormal|positive|negative|\bhigh\b|\blow\b|elevated|raised|deficien|diagnos|"
    r"detected|infection|severe|critical", re.I)


def _clean_suggestion(raw) -> dict:
    """Keep ONLY kind, title and doc_date – every other key is dropped, whatever the model sent."""
    if not isinstance(raw, dict):
        raise ValueError("the answer is not a JSON object")
    kind = (_text(raw.get("kind")) or "").lower().replace(" ", "_").replace("-", "_")
    title = _text(raw.get("title"), 80)
    if title and _RESULT_WORDS.search(title):
        title = None
    date = _text(raw.get("doc_date"), 10)
    return {"kind": kind if kind in DOC_KINDS else "other",
            "title": title,
            "doc_date": date if date and _DATE_RE.match(date) else None}


# ----------------------------------------------------------------------------- public functions

def _read(purpose, prompt, version, schema, cleaner, result_key, data, mime, patient_id,
          hospital_id, ip, input_ref) -> dict:
    out = {"ok": False, "reason": None, "ai_event_id": None, result_key: None}
    ok, reason = ai_allowed(hospital_id, patient_id, ip)
    if not ok:                                  # no AI call is made, so there is nothing to log
        out["reason"] = reason
        return out
    if mime not in AI_MIMES or not data:
        out["reason"] = REASON_FILE
        return out
    raw, err, ms = _run(data, mime, prompt, schema, ip)
    cleaned = None
    if err is None:
        try:
            cleaned = cleaner(raw)
        except Exception as e:                  # an answer in the wrong shape = a failed call
            err = f"bad answer shape: {type(e).__name__}"
    event_id = ai_register.log_event(purpose, PROVIDER, gemini_model(), version, input_ref, cleaned,
                                     ms, ok=err is None, error=err, patient_id=patient_id,
                                     hospital_id=hospital_id)
    out["ai_event_id"] = event_id or None
    if err is not None:
        out["reason"] = REASON_FAILED
        return out
    out.update(ok=True, **{result_key: cleaned})
    return out


def extract_prescription(data: bytes, mime: str, *, patient_id, hospital_id, ip, input_ref) -> dict:
    """Draft what is written on a prescription photo or PDF.
    -> {"ok", "reason", "ai_event_id", "draft"}; draft has the RX_PROMPT_V1 fields, including
    "handwritten" (the CALLER decides what to do with a handwritten paper, from the hospital's
    ai_handwriting setting). ok False = use the manual path and show `reason`."""
    return _read(ai_register.PURPOSE_RX, RX_PROMPT_V1, RX_PROMPT_VERSION, RxDraft, _clean_draft,
                 "draft", data, mime, patient_id, hospital_id, ip, input_ref)


def suggest_document(data: bytes, mime: str, *, patient_id, hospital_id, ip, input_ref) -> dict:
    """Suggest a paper's kind, title and date – nothing else is asked for or kept.
    -> {"ok", "reason", "ai_event_id", "suggestion": {"kind", "title", "doc_date"} | None}"""
    return _read(ai_register.PURPOSE_DOC, DOC_PROMPT_V1, DOC_PROMPT_VERSION, DocSuggestion,
                 _clean_suggestion, "suggestion", data, mime, patient_id, hospital_id, ip, input_ref)


def summarize_text(prompt: str, *, patient_id=None) -> str | None:
    """Plain text for the daily summary (llm.py's second provider). None when there is no key,
    the daily limit is reached, or the call fails – llm.py then uses its template. The register
    stores only the length of the text."""
    if not gemini_enabled() or _limit_reason(None):
        return None
    text, err, ms = _run(None, None, prompt, None, None)
    text = text.strip() if isinstance(text, str) else None
    if err is None and not text:
        err = "empty answer"
    ai_register.log_event(ai_register.PURPOSE_SUMMARY, PROVIDER, gemini_model(), "summary-v1",
                          "summary", {"chars": len(text)} if text else None, ms, ok=err is None,
                          error=err, patient_id=patient_id)
    return text if err is None else None
