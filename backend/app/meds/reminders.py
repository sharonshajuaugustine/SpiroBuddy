"""Missed-dose follow-up for the single-process prototype. No outbound messages.

One alert per patient and scheduled time. A late self-report resolves that alert. Family
delivery is deliberately absent until its consent and channel workflow is implemented.
"""
from __future__ import annotations

import threading
import time

from .. import authz
from .. import service as core
from ..comms import alerts
from ..config import iso, now_local, parse_dt
from . import service as meds

_lock = threading.Lock()
_last = 0.0


def _matches_due(alert, due):
    """Stable titles for new alerts; recognize legacy titles without depending on names."""
    title = alert.get("title") or ""
    return title == f"Medicine follow-up at {due}" or title.endswith(
        ": medicine follow-up at " + parse_dt(due).strftime('%d %b %I:%M %p')) or title.endswith(
        ": medicine follow-up at " + parse_dt(due).strftime('%d %b %Y, %I:%M %p'))


def tick(force=False):
    global _last
    if not _lock.acquire(blocking=False):
        return
    try:
        if not force and time.monotonic() - _last < 30:
            return
        _last = time.monotonic()
        for p in core.store().select("patients"):
            if not authz.alerts_allowed(p):
                continue
            existing = core.store().select("alerts", [("patient_id", "eq", p["id"]), ("kind", "eq", "missed_dose")])
            # Past dose events remain reportable. Include them when reconciling an existing
            # follow-up, but create new alerts only for today's missed doses.
            today = meds.now_local().date().isoformat()
            raw = core.store().select("dose_events", [("patient_id", "eq", p["id"])])
            first = min([parse_dt(d["due_at"]).date().isoformat() for d in raw], default=today)
            groups = {}
            for d in meds.doses_for(p["id"], first, today, True):
                groups.setdefault(d["due_at"], []).append(d)
            for due, doses in groups.items():
                title = f"{p['name']}: medicine follow-up at " + parse_dt(due).strftime('%d %b %Y, %I:%M %p')
                found = next((a for a in existing if _matches_due(a, due)), None)
                late = [d for d in doses if d["status"] == "missed"]
                if not late:
                    if found and found.get("status") != "resolved" and all(
                            d["status"] in (meds.REPORTED, "cancelled") for d in doses):
                        alerts.act(found["id"], "resolve", "Patient dose report")
                    continue
                # Resolving an alert is an explicit staff decision, not a reason to spam it again.
                if found:
                    continue
                if parse_dt(due).date().isoformat() != today:
                    continue
                # Generic raise_alert deduplicates by kind/time, which can collapse two
                # different dose times created in the same tick. Deduplicate above by due.
                stamp = iso(now_local())
                core.store().insert("alerts", [{"patient_id": p["id"], "kind": "missed_dose",
                    "severity": "amber", "title": title,
                    "detail": "Not yet reported: " + ", ".join(d["drug_name"] for d in late) +
                    ". Contact the patient if needed. No advice to double or skip a dose.",
                    "status": "open", "assigned_to": None, "snooze_until": None,
                    "run_id": None, "created_at": stamp, "updated_at": stamp, "acted_by": None}])
    finally:
        _lock.release()
