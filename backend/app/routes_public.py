"""Public story-site API (B7): GET /api/impact – live demo metrics for /impact.html and /trust.html.

Contract K (docs/ARCHITECTURE.md §20). Public on purpose (REBUILD_PLAN §3.4 item 2: `/api/impact*`):
it returns only hospital-wide counts for the demo hospital, never a name, id or any row.

Rules for this endpoint:
- It never errors. A missing table, a missing column or a store outage gives zeros, not a 500.
- Numbers come only from the store (fake patients). The label says so: "demo data, fake patients".
- Patient taps are counted as "reported", never "taken".
- A 15-second cache keeps a busy public page from hammering Supabase.
"""
from __future__ import annotations

import logging
import threading
import time

from fastapi import APIRouter

from . import service
from .config import iso, now_local

log = logging.getLogger("spirobuddy.public")

router = APIRouter()

DEMO_HOSPITAL_ID = 1
LABEL = "demo data, fake patients"
HOSPITAL_LABEL = "Demo General Hospital (fictional)"
CACHE_SECONDS = 15.0

_cache: dict = {"at": 0.0, "data": None}
_cache_lock = threading.Lock()


def _rows(table: str, filters=(), columns: str = "*") -> list[dict]:
    """Rows from the store, or [] if the table (or the store) isn't there yet."""
    try:
        return service.store().select(table, list(filters), columns=columns) or []
    except Exception as e:  # missing table / column / network: zeros, never a 500
        log.debug("impact: %s unavailable (%s)", table, e)
        return []


def _int(v) -> int:
    try:
        return int(v or 0)
    except (TypeError, ValueError):
        return 0


def _pct(part: float, whole: float) -> float:
    return round(100.0 * part / whole, 1) if whole else 0.0


def _in_demo_hospital(row: dict) -> bool:
    # v1 rows have no hospital_id; the seeded demo hospital is id 1. Riverside (id 2) never counts.
    hid = row.get("hospital_id")
    return hid in (None, "", DEMO_HOSPITAL_ID, str(DEMO_HOSPITAL_ID))


def _patient_ids() -> list[int]:
    return [int(p["id"]) for p in _rows("patients") if p.get("id") is not None and _in_demo_hospital(p)]


def _ai_stats() -> dict:
    """AI register totals for the demo hospital. Uses the platform's ai_register.stats() when it
    exists (same numbers as the governance page); otherwise counts ai_events directly."""
    try:
        from . import ai_register  # type: ignore[attr-defined]
        s = ai_register.stats(DEMO_HOSPITAL_ID) or {}
        return {"drafts": _int(s.get("drafts")), "reviewed": _int(s.get("reviewed")),
                "lines_total": _int(s.get("lines_total")),
                "lines_edited_pct": round(float(s.get("lines_edited_pct") or 0), 1),
                "rejected_pct": round(float(s.get("rejected_pct") or 0), 1)}
    except Exception as e:  # module not there yet, or it failed: count ourselves
        log.debug("impact: ai_register.stats unavailable (%s)", e)
    events = [e for e in _rows("ai_events") if _in_demo_hospital(e)]
    drafts = sum(1 for e in events if e.get("ok") in (True, 1, "1", "true", "t"))
    reviewed = [e for e in events if e.get("decision")]
    lines_total = sum(_int(e.get("lines_total")) for e in reviewed)
    lines_edited = sum(_int(e.get("lines_edited")) for e in reviewed)
    rejected = sum(1 for e in reviewed if str(e.get("decision")).lower() == "rejected")
    return {"drafts": drafts, "reviewed": len(reviewed), "lines_total": lines_total,
            "lines_edited_pct": _pct(lines_edited, lines_total),
            "rejected_pct": _pct(rejected, len(reviewed))}


def _sessions_today(pids: set[int]) -> tuple[int, int]:
    """(done, due so far) today across the demo hospital – the pitch's one impact metric."""
    try:
        done = due = 0
        for p in service.list_patients():
            if int(p.get("id") or 0) in pids:
                done += _int(p.get("done_today"))
                due += _int(p.get("due_today"))
        return done, due
    except Exception as e:
        log.debug("impact: today's sessions unavailable (%s)", e)
        return 0, 0


def compute_impact() -> dict:
    """Hospital-wide demo metrics. Every field is a number (or the label strings)."""
    pids = _patient_ids()
    pid_set = set(pids)
    in_pids = [("patient_id", "in", pids)] if pids else None

    sessions = _rows("sessions", in_pids, columns="patient_id") if in_pids else []
    sessions = [s for s in sessions if _int(s.get("patient_id")) in pid_set]
    coached = len({_int(s.get("patient_id")) for s in sessions})

    doses = [d for d in (_rows("dose_events", in_pids, columns="patient_id,status") if in_pids else [])
             if _int(d.get("patient_id")) in pid_set]
    reported = sum(1 for d in doses if d.get("status") == "reported_taken")
    missed = sum(1 for d in doses if d.get("status") == "missed")

    appts = [a for a in (_rows("appointments", in_pids, columns="patient_id,status") if in_pids else [])
             if _int(a.get("patient_id")) in pid_set]
    attended = sum(1 for a in appts if a.get("status") == "attended")
    no_show = sum(1 for a in appts if a.get("status") == "no_show")

    guardians = [g for g in (_rows("guardians", in_pids, columns="patient_id,consent") if in_pids else [])
                 if _int(g.get("patient_id")) in pid_set]
    families = len({_int(g.get("patient_id")) for g in guardians
                    if g.get("consent") in (True, 1, "1", "true", "t")})

    ai = _ai_stats()
    done_today, due_today = _sessions_today(pid_set)

    return {
        # Contract K fields
        "patients_coached": coached,
        "sessions_completed": len(sessions),
        "doses_reported_pct": _pct(reported, reported + missed),
        "follow_ups_kept_pct": _pct(attended, attended + no_show),
        "families_informed": families,
        "ai_lines_edited_pct": ai["lines_edited_pct"],
        "label": LABEL,
        # extras for /trust.html (no login needed) and honest "no data yet" states
        "ai_drafts": ai["drafts"],
        "ai_reviewed": ai["reviewed"],
        "ai_lines_total": ai["lines_total"],
        "ai_rejected_pct": ai["rejected_pct"],
        "patients_in_programme": len(pids),
        "doses_reported": reported,
        "doses_missed": missed,
        "follow_ups_attended": attended,
        "follow_ups_missed": no_show,
        "sessions_done_today": done_today,
        "sessions_due_today": due_today,
        "sessions_done_of_due_pct": _pct(done_today, due_today),
        "hospital": HOSPITAL_LABEL,
        "as_of": iso(now_local()),
    }


def _empty() -> dict:
    zeros = {k: 0 for k in ("patients_coached", "sessions_completed", "families_informed", "ai_drafts",
                            "ai_reviewed", "ai_lines_total", "patients_in_programme", "doses_reported",
                            "doses_missed", "follow_ups_attended", "follow_ups_missed",
                            "sessions_done_today", "sessions_due_today")}
    zeros.update({k: 0.0 for k in ("doses_reported_pct", "follow_ups_kept_pct", "ai_lines_edited_pct",
                                   "ai_rejected_pct", "sessions_done_of_due_pct")})
    zeros.update({"label": LABEL, "hospital": HOSPITAL_LABEL, "as_of": iso(now_local())})
    return zeros


def clear_cache() -> None:
    with _cache_lock:
        _cache["at"], _cache["data"] = 0.0, None


@router.get("/api/impact")
def impact():
    """Live demo metrics (public). Never errors: anything missing counts as zero."""
    now = time.monotonic()
    with _cache_lock:
        if _cache["data"] is not None and now - _cache["at"] < CACHE_SECONDS:
            return _cache["data"]
    try:
        data = compute_impact()
    except Exception:  # belt and braces: the public page must never see a 500
        log.exception("impact: compute failed – returning zeros")
        data = _empty()
    with _cache_lock:
        _cache["at"], _cache["data"] = time.monotonic(), data
    return data
