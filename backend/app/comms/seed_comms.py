"""Demo comms data for the fake patients: care circles (Indian joint-family guardians), care
settings, a few alerts and escalation history, so every screen has something real to show.

Phone numbers end in XXXX on purpose: they are placeholders and are never dialled. Real sends
in demo mode go to DEMO_PATIENT_PHONE / DEMO_GUARDIAN_PHONE / DEMO_NURSE_PHONE instead.
Called from backend/app/seed.py (wipe + seed hooks) and lazily by routes_comms (ensure()).
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from ..config import iso
from .common import now

log = logging.getLogger("spirobuddy.comms.seed")

COMMS_TABLES = ["escalation_events", "calls", "cheers", "inbound_messages", "alerts",
                "escalations", "guardians", "care_settings"]

# patient id -> patient phone + guardians (name, relation, city, language, channel, phone, extras)
CIRCLES = {
    1: {"phone": "+91 94150 2XXXX", "guardians": [
        dict(name="Amit Kumar", relation="son", city="Bengaluru", language="hi", channel="both",
             phone="+91 98450 1XXXX", is_primary=True, token="ravi-amit-demo"),
        dict(name="Pooja Kumar", relation="daughter-in-law", city="Lucknow (at home)", language="hi",
             channel="call", phone="+91 94150 3XXXX"),
        dict(name="Neha Verma", relation="daughter", city="Pune", language="en", channel="whatsapp",
             phone="+91 98220 4XXXX", quiet_start="22:30", quiet_end="07:00"),
    ]},
    2: {"phone": "+91 98100 5XXXX", "guardians": [
        dict(name="Rohit Sharma", relation="husband", city="Delhi (at home)", language="en",
             channel="both", phone="+91 98110 6XXXX", is_primary=True),
        dict(name="Ananya Sharma", relation="daughter", city="Delhi", language="en", channel="whatsapp",
             phone="+91 99990 7XXXX"),
    ]},
    3: {"phone": "+91 98490 8XXXX", "guardians": [
        dict(name="Imran Rahman", relation="son", city="Hyderabad", language="hi", channel="both",
             phone="+91 98480 9XXXX", is_primary=True),
        dict(name="Ayesha Rahman", relation="daughter-in-law", city="Hyderabad (at home)",
             language="hi", channel="call", phone="+91 90000 1XXXX"),
    ]},
    4: {"phone": "+91 94440 2XXXX", "guardians": [
        dict(name="Venkat Iyer", relation="son", city="Chennai", language="ta", channel="both",
             phone="+91 98400 3XXXX", is_primary=True),
        dict(name="Meena Iyer", relation="daughter-in-law", city="Chennai (at home)", language="ta",
             channel="call", phone="+91 94450 4XXXX"),
    ]},
    5: {"phone": "+91 98300 5XXXX", "guardians": [
        dict(name="Rakesh Das", relation="son", city="Kolkata", language="hi", channel="both",
             phone="+91 98310 6XXXX", is_primary=True),
        dict(name="Rina Das", relation="daughter", city="Delhi", language="en", channel="whatsapp",
             phone="+91 98990 7XXXX"),
    ]},
    6: {"phone": "+91 98250 8XXXX", "guardians": [
        dict(name="Kiran Patel", relation="husband", city="Ahmedabad (at home)", language="hi",
             channel="both", phone="+91 98240 9XXXX", is_primary=True),
    ]},
    7: {"phone": "+91 98490 1XXXX", "guardians": [
        dict(name="Divya Reddy", relation="wife", city="Hyderabad (at home)", language="en",
             channel="both", phone="+91 99490 2XXXX", is_primary=True),
    ]},
}


def wipe(st) -> None:
    for t in COMMS_TABLES:
        try:
            st.delete(t, [("patient_id", "gte", 0)])
        except Exception as e:     # table missing in an old Supabase schema
            log.warning("comms wipe %s failed: %s", t, e)
    try:
        st.delete("inbound_messages", [("id", "gte", 0)])   # unknown senders have no patient_id
    except Exception:
        pass
    try:
        from . import escalation
        escalation.reset_memory()
    except Exception:
        pass


def _anchor(d: dict, t: datetime) -> tuple[datetime, int]:
    """A time for seeded history: the latest missed hour today, else yesterday evening."""
    missed = [s["hour"] for s in d.get("today", []) if s["status"] == "missed"]
    if missed:
        h = missed[-1]
        return t.replace(hour=h, minute=12, second=0, microsecond=0), h
    y = (t - timedelta(days=1)).replace(hour=19, minute=12, second=0, microsecond=0)
    return y, 19


def seed(st, t: datetime | None = None) -> None:
    from .. import service
    from .guardians import default_config
    t = t or now()
    present = {p["id"]: p for p in st.select("patients")}
    g_rows = []
    for pid, c in CIRCLES.items():
        if pid not in present:
            continue
        cfg = default_config()
        cfg["patient_phone"] = c["phone"]
        cfg["consent"] = True                       # recorded at discharge (demo)
        cfg["consent_at"] = iso(t - timedelta(days=2))
        if pid == 4:
            cfg["quiet_start"], cfg["quiet_end"] = "21:00", "08:00"   # Lakshmi sleeps early
        st.upsert("care_settings", [{"patient_id": pid, "config": cfg, "updated_at": iso(t)}])
        for g in c["guardians"]:
            from .guardians import new_token
            g_rows.append({"patient_id": pid, "name": g["name"], "relation": g["relation"],
                           "phone": g["phone"], "language": g["language"], "channel": g["channel"],
                           "city": g.get("city"), "quiet_start": g.get("quiet_start"),
                           "quiet_end": g.get("quiet_end"), "is_primary": bool(g.get("is_primary")),
                           "consent": True, "consent_at": iso(t - timedelta(days=2)), "token": g.get("token") or new_token(),
                           "created_at": iso(t - timedelta(days=5))})
    if g_rows:
        st.insert("guardians", g_rows)

    ev, alerts_rows, runs = [], [], []

    def E(pid, at, kind, title, detail="", channel="system", actor="system", to_name=None,
          status="info", run_key=None):
        ev.append(({"patient_id": pid, "run_id": None, "kind": kind, "channel": channel,
                    "actor": actor, "to_name": to_name, "title": title, "detail": detail,
                    "status": status, "ref_id": None, "created_at": iso(at)}, run_key))

    # Mohan Das (5): nobody answered -> nurse alert, still open
    if 5 in present:
        d = service.patient_detail(5) or {}
        at, h = _anchor(d, t)
        runs.append(("mohan", {"patient_id": 5, "reason": "missed", "status": "completed",
                               "speed": "real", "step_index": 5, "next_at": None,
                               "slot_date": at.date().isoformat(), "slot_hour": h, "snoozes": 0,
                               "outcome": "nurse alerted", "meta": {"missed": 2, "done_steps": [
                                   "device", "patient_whatsapp", "patient_call", "guardian", "nurse"]},
                               "created_at": iso(at), "updated_at": iso(at + timedelta(minutes=50))}))
        E(5, at, "start", "Escalation ladder started – 2 missed sessions in a row", run_key="mohan")
        E(5, at, "device_beep", "Device beep + blinking teal light on Mohan's SpiroBuddy",
          channel="device", actor="patient", to_name="Mohan", status="ok", run_key="mohan")
        E(5, at + timedelta(minutes=10), "whatsapp", "WhatsApp to Mohan: reminder (would send – dry run)",
          "🔔 नमस्ते Mohan जी, साँस के व्यायाम का समय हो गया है – SpiroBuddy के साथ 10 धीमी, गहरी साँसें। क्या आपने कर लिया?",
          "whatsapp", "patient", "Mohan", "dry_run", "mohan")
        E(5, at + timedelta(minutes=20), "call", "Automated call to Mohan Das – ringing in the phone simulator (dry run)",
          channel="call", actor="patient", to_name="Mohan Das", status="dry_run", run_key="mohan")
        E(5, at + timedelta(minutes=21), "no_answer", "Mohan Das did not answer", channel="call",
          actor="patient", to_name="Mohan Das", status="warn", run_key="mohan")
        E(5, at + timedelta(minutes=35), "guardian_whatsapp", "WhatsApp to Rakesh (son): guardian alert (would send – dry run)",
          channel="whatsapp", actor="guardian", to_name="Rakesh (son)", status="dry_run", run_key="mohan")
        E(5, at + timedelta(minutes=35), "guardian_call", "Automated call to Rakesh (son) – ringing in the phone simulator (dry run)",
          channel="call", actor="guardian", to_name="Rakesh (son)", status="dry_run", run_key="mohan")
        E(5, at + timedelta(minutes=36), "no_answer", "Rakesh (son) did not answer", channel="call",
          actor="guardian", to_name="Rakesh (son)", status="warn", run_key="mohan")
        E(5, at + timedelta(minutes=50), "nurse_alert", "Nurse alerted – red on the dashboard",
          "Mohan Das: 2 missed sessions – no answer from Mohan Das, Rakesh (son)", "dashboard",
          "nurse", status="ok", run_key="mohan")
        alerts_rows.append(("mohan", {"patient_id": 5, "kind": "no_answer", "severity": "red",
                                      "title": "Mohan Das: 2 missed sessions – no answer from Mohan Das, Rakesh (son)",
                                      "detail": "Device beep → WhatsApp → call (no answer) → son Rakesh WhatsApp + call (no answer).",
                                      "status": "open", "assigned_to": None, "snooze_until": None,
                                      "created_at": iso(at + timedelta(minutes=50)),
                                      "updated_at": iso(at + timedelta(minutes=50)), "acted_by": None}))

    # Abdul Rahman (3): answered the call and pressed 3 (talk to the nurse)
    if 3 in present:
        d = service.patient_detail(3) or {}
        at, h = _anchor(d, t)
        at = at - timedelta(hours=1) if at.hour > 9 else at
        runs.append(("abdul", {"patient_id": 3, "reason": "missed", "status": "resolved",
                               "speed": "real", "step_index": 3, "next_at": None,
                               "slot_date": at.date().isoformat(), "slot_hour": at.hour, "snoozes": 0,
                               "outcome": "nurse_callback", "meta": {"missed": 2, "patient_answered": True,
                                                                     "done_steps": ["device", "patient_whatsapp", "patient_call"]},
                               "created_at": iso(at), "updated_at": iso(at + timedelta(minutes=22))}))
        E(3, at, "start", "Escalation ladder started – 2 missed sessions in a row", run_key="abdul")
        E(3, at, "device_beep", "Device beep + blinking teal light on Abdul's SpiroBuddy",
          channel="device", actor="patient", to_name="Abdul", status="ok", run_key="abdul")
        E(3, at + timedelta(minutes=10), "whatsapp", "WhatsApp to Abdul: reminder (would send – dry run)",
          channel="whatsapp", actor="patient", to_name="Abdul", status="dry_run", run_key="abdul")
        E(3, at + timedelta(minutes=20), "call", "Automated call to Abdul Rahman – ringing in the phone simulator (dry run)",
          channel="call", actor="patient", to_name="Abdul Rahman", status="dry_run", run_key="abdul")
        E(3, at + timedelta(minutes=21), "call_answered", "Abdul Rahman answered the call",
          channel="call", actor="patient", to_name="Abdul Rahman", status="ok", run_key="abdul")
        E(3, at + timedelta(minutes=22), "keypress", "Abdul Rahman pressed 3", "Talk to the nurse",
          "call", "patient", "Abdul Rahman", "ok", "abdul")
        E(3, at + timedelta(minutes=22), "nurse_alert", "Call-back request from Abdul sent to the nurse",
          channel="dashboard", actor="nurse", status="ok", run_key="abdul")
        E(3, at + timedelta(minutes=22), "resolved", "Handed to the nurse (call-back requested)",
          actor="patient", status="ok", run_key="abdul")
        alerts_rows.append(("abdul", {"patient_id": 3, "kind": "callback", "severity": "amber",
                                      "title": "Abdul Rahman asked to talk to a nurse",
                                      "detail": "Pressed 3 on the reminder call. Please call back.",
                                      "status": "acknowledged", "assigned_to": "Sister Anjali",
                                      "snooze_until": None, "created_at": iso(at + timedelta(minutes=22)),
                                      "updated_at": iso(at + timedelta(minutes=30)),
                                      "acted_by": "Sister Anjali"}))
        alerts_rows.append((None, {"patient_id": 3, "kind": "missed", "severity": "red",
                                   "title": "Abdul Rahman: " + ((d.get("status_reasons") or ["very few sessions done"])[0])
                                            + (" (yesterday)" if d.get("status_basis") == "yesterday" else ""),
                                   "detail": "Status rule (red): 2+ missed in a row or fewer than 40% of due sessions done.",
                                   "status": "open", "assigned_to": None, "snooze_until": None,
                                   "created_at": iso(t - timedelta(minutes=25)),
                                   "updated_at": iso(t - timedelta(minutes=25)), "acted_by": None}))

    # Ravi Kumar (1): yesterday he pressed 1 (done); son Amit asked STATUS; daughter-in-law cheered
    if 1 in present:
        y = (t - timedelta(days=1)).replace(hour=13, minute=10, second=0, microsecond=0)
        runs.append(("ravi", {"patient_id": 1, "reason": "missed", "status": "resolved",
                              "speed": "real", "step_index": 3, "next_at": None,
                              "slot_date": y.date().isoformat(), "slot_hour": 13, "snoozes": 0,
                              "outcome": "patient_done", "meta": {"missed": 2, "patient_answered": True,
                                                                  "done_steps": ["device", "patient_whatsapp", "patient_call"]},
                              "created_at": iso(y), "updated_at": iso(y + timedelta(minutes=21))}))
        E(1, y, "start", "Escalation ladder started – 2 missed sessions in a row", run_key="ravi")
        E(1, y, "device_beep", "Device beep + blinking teal light on Ravi's SpiroBuddy",
          channel="device", actor="patient", to_name="Ravi", status="ok", run_key="ravi")
        E(1, y + timedelta(minutes=10), "whatsapp", "WhatsApp to Ravi: reminder (would send – dry run)",
          channel="whatsapp", actor="patient", to_name="Ravi", status="dry_run", run_key="ravi")
        E(1, y + timedelta(minutes=20), "call", "Automated call to Ravi Kumar – ringing in the phone simulator (dry run)",
          channel="call", actor="patient", to_name="Ravi Kumar", status="dry_run", run_key="ravi")
        E(1, y + timedelta(minutes=20, seconds=40), "keypress", "Ravi Kumar pressed 1", "Session done",
          "call", "patient", "Ravi Kumar", "ok", "ravi")
        E(1, y + timedelta(minutes=21), "resolved", "Ravi says the session is done ✅ – ladder stopped",
          actor="patient", status="ok", run_key="ravi")
        E(1, y.replace(hour=19, minute=40), "inbound", "Amit replied “status”",
          "Understood as: status", "whatsapp", "guardian", "Amit")
        E(1, y.replace(hour=20, minute=5), "cheer", "Cheer from Pooja played to the patient after the 20:00 session",
          "आप कर सकते हैं! दस धीमी साँसें – हमें आप पर गर्व है। 💪", "device", "patient", status="ok")

    # Arjun Reddy (7): lower than usual (observation)
    if 7 in present:
        from .trend import evaluate
        d = service.patient_detail(7) or {}
        ev7 = evaluate(d)
        text = ev7.get("text") or ("Today's best breath is well below his own 3-day average. This is an "
                                   "observation, not a diagnosis – a check-in call may help.")
        alerts_rows.append((None, {"patient_id": 7, "kind": "low_trend", "severity": "amber",
                                   "title": f"Arjun Reddy: lower than usual today"
                                            + (f" ({ev7['pct_below']}% below own average)" if ev7.get("pct_below") else ""),
                                   "detail": text, "status": "open", "assigned_to": None,
                                   "snooze_until": None, "created_at": iso(t - timedelta(minutes=40)),
                                   "updated_at": iso(t - timedelta(minutes=40)), "acted_by": None}))
        E(7, t - timedelta(minutes=40), "trend", "Lower-than-usual flag for Arjun", text,
          "dashboard", "nurse", status="warn")

    run_ids = {}
    for key, r in runs:
        run_ids[key] = st.insert("escalations", [r])[0]["id"]
    rows = []
    for e, key in ev:
        if key:
            e["run_id"] = run_ids.get(key)
        rows.append(e)
    if rows:
        st.insert("escalation_events", rows)
    arows = []
    for key, a in alerts_rows:
        a["run_id"] = run_ids.get(key) if key else None
        arows.append(a)
    if arows:
        st.insert("alerts", arows)

    # inbound + cheers + outbound messages for the WhatsApp simulator history
    if 1 in present:
        y = t - timedelta(days=1)
        st.insert("inbound_messages", [{
            "patient_id": 1, "guardian_id": None, "from_number": "+91 98450 1XXXX",
            "from_role": "guardian", "from_name": "Amit Kumar", "channel": "whatsapp",
            "body": "status", "intent": "status",
            "reply": "📊 पापा (Ravi) – आज 11 में से 10 सत्र पूरे। सबसे अच्छी साँस 1950 mL (लक्ष्य 2000 mL)।",
            "created_at": iso(y.replace(hour=19, minute=40))}])
        st.insert("cheers", [{"patient_id": 1, "guardian_id": None, "from_name": "Pooja Kumar",
                              "text": "आप कर सकते हैं! दस धीमी साँसें – हमें आप पर गर्व है। 💪",
                              "language": "hi", "status": "played",
                              "created_at": iso(y.replace(hour=18, minute=55)),
                              "played_at": iso(y.replace(hour=20, minute=5))}])
        st.insert("messages", [
            {"patient_id": 1, "kind": "reminder", "to_role": "patient", "to_number": "+91 94150 2XXXX",
             "text": "🔔 नमस्ते Ravi जी, साँस के व्यायाम का समय हो गया है – SpiroBuddy के साथ 10 धीमी, गहरी साँसें। क्या आपने कर लिया?\n\n— SpiroBuddy (स्वचालित संदेश)। नर्स से बात करने के लिए 3 भेजें।",
             "sent": False, "dry_run": True, "created_at": iso(y.replace(hour=13, minute=20))},
            {"patient_id": 1, "kind": "reply", "to_role": "family", "to_number": "+91 98450 1XXXX",
             "text": "📊 पापा (Ravi) – आज 11 में से 10 सत्र पूरे। सबसे अच्छी साँस 1950 mL (लक्ष्य 2000 mL)।",
             "sent": False, "dry_run": True, "created_at": iso(y.replace(hour=19, minute=40, second=5))},
        ])
    log.info("Seeded comms demo data (%d guardians, %d alerts, %d events)", len(g_rows),
             len(arows), len(rows))


def ensure(st) -> bool:
    """Seed comms data once for a store that already had patients (e.g. an older demo DB)."""
    try:
        if st.select("guardians", limit=1, columns="id"):
            return False
        if not st.select("patients", limit=1, columns="id"):
            return False
        seed(st)
        return True
    except Exception as e:
        log.warning("comms ensure failed: %s", e)
        return False
