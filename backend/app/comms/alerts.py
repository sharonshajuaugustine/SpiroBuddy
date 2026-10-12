"""Nurse alerts inbox: every alert (missed sessions, red flag, no answer, lower-than-usual trend,
call-back request) with acknowledge / snooze / assign / resolve. Alerts come from fixed rules,
never from the AI."""
from __future__ import annotations

from datetime import timedelta

from ..config import iso
from .common import log_event, now, patient_names, st, to_dt

KINDS = ("missed", "missed_dose", "red_flag", "no_answer", "low_trend", "callback", "help", "question",
         "call_review")
SEVERITY_RANK = {"red": 0, "amber": 1, "info": 2}
KIND_LABEL = {"missed": "Missed sessions", "red_flag": "Red flag", "no_answer": "No answer",
              "missed_dose": "Medicine follow-up",
              "low_trend": "Lower than usual", "callback": "Call-back request",
              "help": "Asked for help", "question": "Question",
              "call_review": "Check-in call note"}


def _effective_status(a: dict, t=None) -> str:
    """Snoozed alerts come back as 'open' once the snooze has run out."""
    t = t or now()
    if a.get("status") == "snoozed":
        until = to_dt(a.get("snooze_until"))
        if until is None or until <= t:
            return "open"
    return a.get("status") or "open"


def public_alert(a: dict, names: dict | None = None, t=None) -> dict:
    t = t or now()
    names = names if names is not None else patient_names()
    created, updated = to_dt(a.get("created_at")), to_dt(a.get("updated_at"))
    snooze = to_dt(a.get("snooze_until"))
    return {"id": a.get("id"), "patient_id": a.get("patient_id"),
            "patient_name": names.get(a.get("patient_id")), "kind": a.get("kind"),
            "kind_label": KIND_LABEL.get(a.get("kind"), a.get("kind")),
            "severity": a.get("severity") or "amber", "title": a.get("title"),
            "detail": a.get("detail"), "status": _effective_status(a, t),
            "assigned_to": a.get("assigned_to"), "acted_by": a.get("acted_by"),
            "snooze_until": iso(snooze) if snooze else None, "run_id": a.get("run_id"),
            "created_at": iso(created) if created else None,
            "updated_at": iso(updated) if updated else None}


def list_alerts(status: str = "open", patient_id: int | None = None, limit: int = 100) -> list[dict]:
    f = []
    if patient_id is not None:
        f.append(("patient_id", "eq", int(patient_id)))
    rows = st().select("alerts", f, order="created_at", desc=True, limit=500)
    t = now()
    names = patient_names()
    out = [public_alert(a, names, t) for a in rows]
    if status == "open":
        out = [a for a in out if a["status"] == "open"]
    elif status == "active":          # open + acknowledged (not yet resolved)
        out = [a for a in out if a["status"] in ("open", "acknowledged")]
    elif status in ("acknowledged", "snoozed", "resolved"):
        out = [a for a in out if a["status"] == status]
    out.sort(key=lambda a: (a["status"] != "open", SEVERITY_RANK.get(a["severity"], 3),
                            -(to_dt(a["created_at"]).timestamp() if a["created_at"] else 0)))
    return out[:limit]


def counts(me: str | None = None, only: set | None = None) -> dict:
    """Open / acknowledged / snoozed counts. `only`: the patient ids the viewer may see (None =
    everyone); alerts outside it, and alerts with no patient, are then left out."""
    rows = st().select("alerts", [("status", "neq", "resolved")])
    if only is not None:
        rows = [a for a in rows if a.get("patient_id") in only]
    t = now()
    c = {"open": 0, "red": 0, "amber": 0, "acknowledged": 0, "snoozed": 0, "mine": 0}
    by_patient: dict[int, dict] = {}
    for a in rows:
        s = _effective_status(a, t)
        if s == "open":
            c["open"] += 1
            sev = a.get("severity") or "amber"
            if sev in ("red", "amber"):
                c[sev] += 1
            bp = by_patient.setdefault(a.get("patient_id"), {"open": 0, "red": 0})
            bp["open"] += 1
            bp["red"] += 1 if sev == "red" else 0
        elif s in c:
            c[s] += 1
        if me and a.get("assigned_to") == me and s != "resolved":
            c["mine"] += 1
    c["by_patient"] = {str(k): v for k, v in by_patient.items() if k is not None}
    return c


def get(aid: int) -> dict | None:
    rows = st().select("alerts", [("id", "eq", int(aid))])
    return rows[0] if rows else None


def raise_alert(patient_id: int, kind: str, severity: str, title: str, detail: str = "",
                run_id: int | None = None, dedupe_hours: float = 12) -> dict:
    """Create an alert, or refresh the open one of the same kind for this patient (no spam)."""
    t = now()
    since = t - timedelta(hours=dedupe_hours)
    for a in st().select("alerts", [("patient_id", "eq", int(patient_id)), ("kind", "eq", kind)],
                         order="created_at", desc=True, limit=5):
        created = to_dt(a.get("created_at"))
        if a.get("status") != "resolved" and created and created >= since:
            vals = {"title": title, "detail": detail, "updated_at": iso(t)}
            if SEVERITY_RANK.get(severity, 3) < SEVERITY_RANK.get(a.get("severity"), 3):
                vals["severity"] = severity
            if _effective_status(a, t) != "open" and severity == "red":
                vals["status"] = "open"           # something new and serious: re-open it
            if run_id:
                vals["run_id"] = run_id
            st().update("alerts", [("id", "eq", a["id"])], vals)
            return {**a, **vals}
    row = {"patient_id": int(patient_id), "kind": kind, "severity": severity, "title": title,
           "detail": detail, "status": "open", "assigned_to": None, "snooze_until": None,
           "run_id": run_id, "created_at": iso(t), "updated_at": iso(t), "acted_by": None}
    return st().insert("alerts", [row])[0]


def act(aid: int, action: str, by: str | None = None, minutes: int | None = None,
        to: str | None = None) -> dict | None:
    a = get(aid)
    if not a:
        return None
    t = now()
    by = (by or "Nurse").strip()[:60]
    vals = {"updated_at": iso(t), "acted_by": by}
    if action == "ack":
        vals.update(status="acknowledged", snooze_until=None)
        if not a.get("assigned_to"):
            vals["assigned_to"] = by
        note = f"Acknowledged by {by}"
    elif action == "snooze":
        m = int(minutes or 30)
        if not 5 <= m <= 24 * 60:
            raise ValueError("minutes must be 5..1440")
        vals.update(status="snoozed", snooze_until=iso(t + timedelta(minutes=m)))
        note = f"Snoozed {m} min by {by}"
    elif action == "assign":
        who = (to or by).strip()[:60]
        vals["assigned_to"] = who
        if _effective_status(a, t) == "snoozed":
            vals["status"] = "open"
        note = f"Assigned to {who}"
    elif action == "resolve":
        vals.update(status="resolved", snooze_until=None)
        note = f"Resolved by {by}"
    elif action == "reopen":
        vals.update(status="open", snooze_until=None)
        note = f"Re-opened by {by}"
    else:
        raise ValueError("action must be ack, snooze, assign, resolve or reopen")
    st().update("alerts", [("id", "eq", int(aid))], vals)
    log_event(a.get("patient_id"), "nurse_alert", f"Alert “{a.get('title')}”: {note}",
              channel="dashboard", actor="nurse", status="info", ref_id=a.get("id"))
    return public_alert({**a, **vals})
