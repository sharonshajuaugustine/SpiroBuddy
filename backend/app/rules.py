"""Rules from ARCHITECTURE.md: score (contract C), rule-based label, slot list, status colour."""
from __future__ import annotations

from datetime import datetime, timedelta

from .config import FEATURE_KEYS, FIRST_SLOT, LAST_SLOT, LABELS

FAST_MAX_RISE = 1400   # mL/s


def clean_features(f: dict) -> dict:
    """Coerce the 8 feature keys to floats (missing -> 0.0). Raises ValueError on junk."""
    out = {}
    for k in FEATURE_KEYS:
        v = f.get(k, 0.0)
        out[k] = float(v if v is not None else 0.0)
    return out


def score(features: dict, target_ml: float, hold_target_s: float) -> float:
    peak = float(features.get("peak_ml", 0) or 0)
    max_rise = float(features.get("max_rise_ml_s", 0) or 0)
    hold = float(features.get("hold_s", 0) or 0)
    depth = 4 * min(peak / target_ml, 1.0) if target_ml else 0.0
    speed = 3 if max_rise <= 900 else (1 if max_rise <= FAST_MAX_RISE else 0)
    hold_pts = 3 * min(hold / hold_target_s, 1.0) if hold_target_s else 0.0
    return round(max(0.0, depth + speed + hold_pts), 1)


def rule_label(features: dict) -> str:
    if float(features.get("max_rise_ml_s", 0) or 0) > FAST_MAX_RISE:
        return "too_fast"
    if float(features.get("pct_target", 0) or 0) < 0.5:
        return "too_shallow"
    if float(features.get("hold_s", 0) or 0) < 1.0:
        return "no_hold"
    return "good"


def rule_classify(features: dict) -> dict:
    label = rule_label(features)
    return {"label": label, "proba": {l: (1.0 if l == label else 0.0) for l in LABELS},
            "source": "rules"}


def clamp_slot_hour(hour: int) -> int:
    return max(FIRST_SLOT, min(LAST_SLOT, hour))


# ----------------------------------------------------------------------------- slots & status

def day_slots(stored: dict[int, dict], day: str, now: datetime) -> list[dict]:
    """Build the 14 slot entries for `day` (YYYY-MM-DD).

    stored: {hour: slot row} for that day. A past hour with no 'done' row counts as missed.
    """
    today = now.date().isoformat()
    out = []
    for hour in range(FIRST_SLOT, LAST_SLOT + 1):
        row = stored.get(hour)
        if row and row.get("status") == "done":
            entry = {"hour": hour, "status": "done", "session_id": row.get("session_id")}
        elif row and row.get("status") == "missed":
            entry = {"hour": hour, "status": "missed"}
        elif day < today or (day == today and hour < now.hour):
            entry = {"hour": hour, "status": "missed"}
        elif day == today and hour == now.hour:
            entry = {"hour": hour, "status": "pending"}
        else:
            entry = {"hour": hour, "status": "upcoming"}
        out.append(entry)
    return out


def due_count(slots: list[dict]) -> int:
    """Contract: slots from 8:00 up to the current hour (max 14) = everything not 'upcoming'."""
    return sum(1 for s in slots if s["status"] != "upcoming")


def evaluate(slots: list[dict], best_ml: float, personal_best_ml: float) -> dict:
    """Status colour for one day's slots. The current hour (still 'pending') is not held
    against the patient, so the ratio uses elapsed slots + the current one if already done."""
    done = sum(1 for s in slots if s["status"] == "done")
    due_eff = sum(1 for s in slots if s["status"] in ("done", "missed"))
    trailing = 0
    for s in reversed([s for s in slots if s["status"] in ("done", "missed")]):
        if s["status"] != "missed":
            break
        trailing += 1
    ratio = done / due_eff if due_eff else None
    reasons, status = [], "green"
    if trailing >= 2:
        reasons.append(f"{trailing} missed sessions in a row")
    if ratio is not None and ratio < 0.4:
        reasons.append(f"only {done} of {due_eff} sessions done")
    if reasons:
        status = "red"
    else:
        if ratio is not None and ratio < 0.7:
            reasons.append(f"{done} of {due_eff} sessions done")
        if done and personal_best_ml and best_ml < 0.8 * personal_best_ml:
            reasons.append(f"best breath {int(best_ml)} mL is below 80% of personal best "
                           f"{int(personal_best_ml)} mL")
        status = "yellow" if reasons else "green"
    if not reasons:
        reasons.append("on track")
    return {"status": status, "reasons": reasons, "done": done, "due_eff": due_eff,
            "trailing_missed": trailing}


def status_day(now: datetime, today_slots: list[dict]) -> str:
    """Which day the colour is judged on: today, or yesterday if nothing is due yet
    (before ~9:00, or before 8:00), so the board still means something early in the morning."""
    if any(s["status"] in ("done", "missed") for s in today_slots):
        return now.date().isoformat()
    return (now.date() - timedelta(days=1)).isoformat()
