"""Lower-than-usual trend flag: today's best breath compared with the patient's OWN average of
the previous 3 days. Worded as an observation for the nurse – never as a diagnosis."""
from __future__ import annotations

from .. import service
from ..config import iso
from . import alerts
from .common import first_name, log_event, now, st, to_dt

LOW_TREND_RATIO = 0.80          # flag when today's best is 20 %+ below the own 3-day average
MIN_SESSIONS_TODAY = 1


def evaluate(detail: dict) -> dict:
    hist = detail.get("history") or []
    today = hist[-1] if hist else {}
    prev = [h["best_ml"] for h in hist[-4:-1] if h.get("best_ml")]
    out = {"flag": False, "today_best": today.get("best_ml") or 0, "avg3": None,
           "pct_below": None, "text": None}
    if not prev or (today.get("sessions_done") or 0) < MIN_SESSIONS_TODAY:
        return out
    avg3 = sum(prev) / len(prev)
    best = float(today.get("best_ml") or 0)
    out["avg3"] = round(avg3)
    if avg3 <= 0:
        return out
    ratio = best / avg3
    out["pct_below"] = max(0, round((1 - ratio) * 100))
    if ratio < LOW_TREND_RATIO:
        pron = "her" if (detail.get("sex") or "").upper() == "F" else "his"
        out["flag"] = True
        out["text"] = (f"Today's best breath ({int(best):,} mL) is {out['pct_below']}% lower than "
                       f"{pron} own 3-day average ({int(avg3):,} mL). This is an observation, not a "
                       f"diagnosis – a check-in call may help.")
    return out


def check_patient(pid: int) -> dict:
    d = service.patient_detail(int(pid))
    if not d:
        return {"flag": False}
    ev = evaluate(d)
    if ev["flag"]:
        today = now().date().isoformat()
        existing = [a for a in st().select("alerts", [("patient_id", "eq", int(pid)),
                                                      ("kind", "eq", "low_trend")])
                    if (to_dt(a.get("created_at")) or now()).date().isoformat() == today]
        a = alerts.raise_alert(int(pid), "low_trend", "amber",
                               f"{d['name']}: lower than usual today ({ev['pct_below']}% below own average)",
                               detail=ev["text"], dedupe_hours=20)
        if not existing:
            log_event(int(pid), "trend", f"Lower-than-usual flag for {first_name(d['name'])}",
                      detail=ev["text"], channel="dashboard", actor="nurse", status="warn",
                      ref_id=a.get("id"))
    return ev


def check_all() -> int:
    n = 0
    for p in st().select("patients", columns="id"):
        if check_patient(p["id"]).get("flag"):
            n += 1
    return n


def stamp() -> str:
    return iso(now())
