"""AI register: one ai_events row for every AI call, plus the human decision on it (spec §8.15).

What a row holds: purpose, provider, model, prompt version, a REFERENCE to the input
(like "document:12"), the structured output, how long it took and whether it worked.
What a row never holds: the prompt text, the photo or PDF bytes, a key or a token.

The governance page and /trust.html show stats(): drafts, % of lines people edited, % rejected.
"""
from __future__ import annotations

import logging
import re

from . import service
from .config import iso, now_local

log = logging.getLogger("spirobuddy.ai_register")

PURPOSE_RX = "rx_extract"        # prescription photo/PDF -> draft lines
PURPOSE_DOC = "doc_suggest"      # document -> kind/title/date suggestion
PURPOSE_SUMMARY = "summary"      # daily summary text
DECISIONS = ("approved", "edited", "rejected")

_REF_OK = re.compile(r"^[A-Za-z0-9_.:\-/]{1,80}$")     # "document:12", "sample:rx_ravi_printed"


def _safe_ref(input_ref) -> str | None:
    """Only a short reference is ever stored. Anything that looks like content is dropped."""
    if input_ref is None:
        return None
    ref = str(input_ref).strip()
    return ref if _REF_OK.match(ref) else "invalid-ref"


def _hospital_of(patient_id) -> int | None:
    if patient_id is None:
        return None
    try:
        rows = service.store().select("patients", [("id", "eq", int(patient_id))], limit=1)
        return rows[0].get("hospital_id") if rows else None
    except Exception:
        return None


def log_event(purpose, provider, model, prompt_version, input_ref, output, latency_ms, ok,
              error=None, patient_id=None, hospital_id=None) -> int:
    """Write one ai_events row and return its id (0 if the write failed – it never raises,
    so a register problem can't break the manual path)."""
    try:
        row = {
            "hospital_id": hospital_id if hospital_id is not None else _hospital_of(patient_id),
            "purpose": str(purpose), "provider": provider, "model": model,
            "prompt_version": prompt_version, "input_ref": _safe_ref(input_ref),
            "output": output if isinstance(output, (dict, list)) else None,
            "latency_ms": int(latency_ms or 0), "ok": bool(ok),
            "error": (str(error)[:300] if error else None),
            "patient_id": int(patient_id) if patient_id is not None else None,
        }
        saved = service.store().insert("ai_events", [row])
        return int(saved[0]["id"]) if saved else 0
    except Exception as e:
        log.warning("could not write the AI register row: %s", e)
        return 0


def record_review(ai_event_id, reviewer_id, decision, lines_total, lines_edited, lines_removed) -> None:
    """Store the human decision on an AI draft: approved | edited | rejected, and how many of
    the lines the reviewer changed or removed. A wrong decision word raises ValueError (a
    coding mistake); a store problem is only logged."""
    if not ai_event_id:
        return
    if decision not in DECISIONS:
        raise ValueError(f"decision must be one of {DECISIONS}")
    try:
        service.store().update("ai_events", [("id", "eq", int(ai_event_id))], {
            "reviewed_by": int(reviewer_id) if reviewer_id is not None else None,
            "reviewed_at": iso(now_local()), "decision": decision,
            "lines_total": max(0, int(lines_total or 0)),
            "lines_edited": max(0, int(lines_edited or 0)),
            "lines_removed": max(0, int(lines_removed or 0)),
        })
    except Exception as e:
        log.warning("could not store the review of AI event %s: %s", ai_event_id, e)


def _pct(part: int, whole: int) -> float:
    return round(100.0 * part / whole, 1) if whole else 0.0


def events_for(hospital_id=None, purpose: str | None = None, limit: int = 200) -> list[dict]:
    """AI register rows for one hospital (its own rows + rows of its patients), newest first.
    hospital_id None = every row (used for the public demo totals)."""
    st = service.store()
    filters = [("purpose", "eq", purpose)] if purpose else []
    rows = st.select("ai_events", filters, order="id", desc=True)
    if hospital_id is not None:
        pids = {p["id"] for p in st.select("patients", [("hospital_id", "eq", hospital_id)],
                                           columns="id")}
        rows = [r for r in rows if r.get("hospital_id") == hospital_id
                or (r.get("hospital_id") is None and r.get("patient_id") in pids)]
    return rows[:limit] if limit else rows


def stats(hospital_id=None) -> dict:
    """{drafts, reviewed, lines_total, lines_edited_pct, rejected_pct, by_purpose} (+ a few
    plain counts). drafts = prescription drafts the AI produced; the percentages are over the
    drafts a person has reviewed. Everything is 0 when there is nothing yet."""
    try:
        rows = events_for(hospital_id, limit=0)
    except Exception as e:
        log.warning("AI register stats failed: %s", e)
        rows = []
    drafts = [r for r in rows if r.get("purpose") == PURPOSE_RX and r.get("ok")]
    reviewed = [r for r in drafts if r.get("decision")]
    lines_total = sum(int(r.get("lines_total") or 0) for r in reviewed)
    lines_edited = sum(int(r.get("lines_edited") or 0) for r in reviewed)
    lines_removed = sum(int(r.get("lines_removed") or 0) for r in reviewed)
    rejected = sum(1 for r in reviewed if r.get("decision") == "rejected")
    by_purpose: dict[str, dict] = {}
    for r in rows:
        b = by_purpose.setdefault(r.get("purpose") or "other", {"calls": 0, "ok": 0, "failed": 0})
        b["calls"] += 1
        b["ok" if r.get("ok") else "failed"] += 1
    return {
        "drafts": len(drafts), "reviewed": len(reviewed), "lines_total": lines_total,
        "lines_edited": lines_edited, "lines_removed": lines_removed,
        "lines_edited_pct": _pct(lines_edited, lines_total),
        "lines_removed_pct": _pct(lines_removed, lines_total),
        "rejected_pct": _pct(rejected, len(reviewed)),
        "calls": len(rows), "failed": sum(1 for r in rows if not r.get("ok")),
        "by_purpose": by_purpose,
    }
