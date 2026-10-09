"""Plain-language progress numbers used by WhatsApp replies, the guardian page and the card."""
from __future__ import annotations

from datetime import timedelta

from .. import service
from ..config import iso
from .common import now, to_dt

GOOD_DAY_SESSIONS = 8      # a day counts towards the streak with 8+ of the 14 hourly sessions


def streak_days(history: list[dict], done_today: int, due_today: int) -> int:
    """Days in a row with 8+ sessions. Today counts if it is already a good day; an unfinished
    today never breaks the streak."""
    days = list(history)                      # oldest .. today
    n = 0
    today = days[-1] if days else None
    if today and today.get("sessions_done", 0) >= GOOD_DAY_SESSIONS:
        n += 1
    for h in reversed(days[:-1]):
        if h.get("sessions_done", 0) >= GOOD_DAY_SESSIONS:
            n += 1
        else:
            break
    return n


def progress(pid: int) -> dict | None:
    d = service.patient_detail(int(pid))
    if d is None:
        return None
    last = None
    sess = service.list_sessions(int(pid), limit=1)
    if sess:
        s = sess[0]
        last = {"at": s["started_at"], "best_ml": s["best_ml"], "avg_score": s["avg_score"],
                "slot_hour": s["slot_hour"]}
    week = d.get("history") or []
    week_sessions = sum(h.get("sessions_done", 0) for h in week)
    week_best = max([h.get("best_ml") or 0 for h in week], default=0)
    return {
        "patient": d, "done": d["done_today"], "due": d["due_today"], "best_today": d["best_today"],
        "target_ml": d["target_ml"], "status": d["status"], "trend": d["trend"],
        "streak": streak_days(week, d["done_today"], d["due_today"]), "last": last,
        "today": d["today"], "week": week, "week_sessions": week_sessions,
        "week_possible": 14 * len(week), "week_best": week_best,
        "trailing_missed": d.get("trailing_missed", 0),
    }


def minutes_ago(at) -> int | None:
    t = to_dt(at)
    return None if t is None else max(0, int((now() - t).total_seconds() // 60))


def iso_or_none(v):
    t = to_dt(v)
    return iso(t) if t else None


def day_label(i_from_today: int) -> str:
    return (now().date() - timedelta(days=i_from_today)).isoformat()
