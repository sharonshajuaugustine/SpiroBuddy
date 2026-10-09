"""The escalation ladder: device beep -> patient WhatsApp (quick replies) -> automated call to the
patient (press 1/2/3) -> guardian WhatsApp + call -> nurse alert (red on the dashboard).

- Per-patient steps and delays (care settings). "fast" speed = the demo fast-forward (~60 s).
- Quiet hours (default 21:00–07:00 IST, per patient and per guardian) hold every step that
  would disturb someone, except red-flag. The nurse alert is never held (it's a dashboard).
- Every step is an event in the patient's timeline (escalation_events).
- A real session (device/app/demo), a "1 / Done" reply, a guardian "I'll check" or a nurse
  call-back request stops the ladder. "2 / 15 min" snoozes once, then calls again.
- Runs on a background tick (started by routes_comms) plus a lazy tick on comms requests.
"""
from __future__ import annotations

import logging
import threading
import time
from datetime import timedelta

from .. import service
from ..config import FIRST_SLOT, LAST_SLOT, env_flag, iso
from . import alerts, calls, messages
from .common import (consent_current, first_name, has_consent, in_quiet, log_event, now, patient,
                     patient_names, quiet_end_after, st, to_dt)
from .guardians import (STEP_KEYS, STEP_LABELS, get_settings, guardian_label, guardian_quiet,
                        list_guardians)

log = logging.getLogger("spirobuddy.comms.escalation")

FAST_DELAY_S = {"device": 0, "patient_whatsapp": 6, "patient_call": 7, "guardian": 20, "nurse": 18}
FAST_RING_S = 12
FAST_SNOOZE_S = 12
MAX_SNOOZES = 1

_lock = threading.RLock()
_last_scan = 0.0
_last_trend = 0.0
_last_consent = 0.0
_seen_sessions: dict[int, int] | None = None


# ----------------------------------------------------------------------------- runs

def get_run(rid: int) -> dict | None:
    rows = st().select("escalations", [("id", "eq", int(rid))])
    return rows[0] if rows else None


def active_run(pid: int) -> dict | None:
    rows = st().select("escalations", [("patient_id", "eq", int(pid)), ("status", "eq", "active")],
                       order="id", desc=True, limit=1)
    return rows[0] if rows else None


def _meta(run: dict) -> dict:
    m = run.get("meta")
    return dict(m) if isinstance(m, dict) else {}


def _save(run: dict, **vals) -> dict:
    vals["updated_at"] = iso(now())
    st().update("escalations", [("id", "eq", run["id"])], vals)
    run.update(vals)
    return run


def _enabled_keys(cfg: dict, run: dict | None = None) -> list[str]:
    keys = [s["key"] for s in cfg["steps"] if s.get("enabled")]
    if run and _meta(run).get("red_flag"):
        keys = [k for k in ("guardian", "nurse")]
    return keys


def _delay(key: str, run: dict, cfg: dict) -> timedelta:
    if _meta(run).get("red_flag"):
        return timedelta(seconds=0 if key == "guardian" else (5 if run.get("speed") == "fast" else 60))
    if run.get("speed") == "fast":
        return timedelta(seconds=FAST_DELAY_S.get(key, 8))
    d = next((s.get("delay_min", 0) for s in cfg["steps"] if s["key"] == key), 0)
    return timedelta(minutes=int(d or 0))


def public_run(run: dict, names: dict | None = None) -> dict:
    cfg = get_settings(run["patient_id"])
    keys = _enabled_keys(cfg, run)
    idx = int(run.get("step_index") or 0)
    meta = _meta(run)
    done_keys = meta.get("done_steps", [])
    steps = []
    for i, k in enumerate(keys):
        if k in done_keys:
            state = "done"
        elif run.get("status") == "active" and i == idx:
            state = "held" if meta.get("held_until") else "next"
        elif run.get("status") == "active" and i > idx:
            state = "waiting"
        else:
            state = "skipped"
        steps.append({"key": k, "label": STEP_LABELS[k], "state": state})
    nxt = to_dt(run.get("next_at"))
    names = names if names is not None else patient_names()
    created = to_dt(run.get("created_at"))
    return {"id": run["id"], "patient_id": run["patient_id"],
            "patient_name": names.get(run["patient_id"]), "reason": run.get("reason"),
            "status": run.get("status"), "speed": run.get("speed"), "step_index": idx,
            "steps": steps, "outcome": run.get("outcome"), "snoozes": run.get("snoozes") or 0,
            "next_at": iso(nxt) if nxt and run.get("status") == "active" else None,
            "seconds_to_next": max(0, int((nxt - now()).total_seconds()))
            if nxt and run.get("status") == "active" else None,
            "held_until": meta.get("held_until"), "red_flag": bool(meta.get("red_flag")),
            "override_quiet": bool(meta.get("override_quiet")),
            "slot_hour": run.get("slot_hour"), "created_at": iso(created) if created else None}


def list_runs(patient_id: int | None = None, active_only: bool = False, limit: int = 20) -> list[dict]:
    f = []
    if patient_id is not None:
        f.append(("patient_id", "eq", int(patient_id)))
    if active_only:
        f.append(("status", "eq", "active"))
    names = patient_names()
    return [public_run(r, names) for r in st().select("escalations", f, order="id", desc=True,
                                                      limit=limit)]


def start(pid: int, reason: str = "manual", speed: str = "real", slot_hour: int | None = None,
          override_quiet: bool = False, missed: int | None = None, red_flag: bool = False,
          run_now: bool = True) -> dict:
    with _lock:
        p = patient(pid)
        if not p:
            raise KeyError(pid)
        old = active_run(pid)
        if old:
            _save(old, status="stopped", outcome="replaced by a new ladder")
        t = now()
        d = service.patient_detail(int(pid)) or {}
        if missed is None:
            missed = max(2, int(d.get("trailing_missed") or 0))
        if slot_hour is None:
            missed_hours = [s["hour"] for s in d.get("today", []) if s["status"] == "missed"]
            slot_hour = missed_hours[-1] if missed_hours else t.hour
        cfg = get_settings(pid)
        meta = {"override_quiet": bool(override_quiet), "missed": int(missed),
                "red_flag": bool(red_flag), "done_steps": [], "patient_answered": False}
        run = {"patient_id": int(pid), "reason": reason, "status": "active",
               "speed": "fast" if speed == "fast" else "real", "step_index": 0,
               "next_at": iso(t), "slot_date": t.date().isoformat(), "slot_hour": slot_hour,
               "snoozes": 0, "outcome": None, "meta": meta, "created_at": iso(t),
               "updated_at": iso(t)}
        run = st().insert("escalations", [run])[0]
        if not isinstance(run.get("meta"), dict):
            run["meta"] = meta
        keys = _enabled_keys(cfg, run)
        why = {"missed": f"{missed} missed sessions in a row", "manual": "started by the nurse",
               "demo": "demo fast-forward", "red_flag": "red flag"}.get(reason, reason)
        log_event(pid, "start",
                  f"Escalation ladder started – {why}" + (" (fast-forward ×60)" if speed == "fast" else ""),
                  detail=" → ".join(STEP_LABELS[k].split(" (")[0] for k in keys)
                  + (" · quiet hours ignored for the demo" if override_quiet else ""),
                  channel="system", actor="system", status="info", run_id=run["id"])
        if run_now:
            _tick_run(run)
        return public_run(get_run(run["id"]) or run)


def stop(rid: int, by: str = "nurse") -> dict | None:
    with _lock:
        run = get_run(rid)
        if not run:
            return None
        if run.get("status") == "active":
            _save(run, status="stopped", outcome=f"stopped by {by}")
            log_event(run["patient_id"], "stopped", f"Ladder stopped by {by}", channel="dashboard",
                      actor="nurse", status="info", run_id=rid)
        return public_run(run)


def advance(rid: int) -> dict | None:
    """Run the next step now (presenter/nurse 'next step' button)."""
    with _lock:
        run = get_run(rid)
        if not run or run.get("status") != "active":
            return public_run(run) if run else None
        meta = _meta(run)
        was_held = meta.pop("held_until", None)
        meta["override_quiet"] = bool(meta.get("override_quiet") or was_held)
        _save(run, next_at=iso(now()), meta=meta)
        _tick_run(run)
        return public_run(get_run(rid) or run)


def resolve(run: dict, outcome: str, title: str, actor: str = "patient") -> None:
    if run.get("status") != "active":
        return
    _save(run, status="resolved", outcome=outcome)
    log_event(run["patient_id"], "resolved", title, channel="system", actor=actor, status="ok",
              run_id=run["id"])


# ----------------------------------------------------------------------------- steps

def _tick_run(run: dict) -> None:
    t = now()
    nxt = to_dt(run.get("next_at"))
    if run.get("status") != "active" or (nxt and nxt > t):
        return
    p = patient(run["patient_id"])
    if not p:
        _save(run, status="stopped", outcome="patient removed")
        return
    cfg = get_settings(p["id"])
    keys = _enabled_keys(cfg, run)
    idx = int(run.get("step_index") or 0)
    if idx >= len(keys):
        _save(run, status="completed", outcome=run.get("outcome") or "nurse alerted")
        return
    key = keys[idx]
    meta = _meta(run)
    overriding = meta.get("override_quiet") or meta.get("red_flag")
    disturbs = key in ("device", "patient_whatsapp", "patient_call")
    if disturbs and not overriding and in_quiet(t, cfg["quiet_start"], cfg["quiet_end"]):
        until = quiet_end_after(t, cfg["quiet_end"])
        if not meta.get("held_until"):
            log_event(p["id"], "quiet_hold",
                      f"Quiet hours ({cfg['quiet_start']}–{cfg['quiet_end']} IST) – "
                      f"{STEP_LABELS[key].split(' (')[0].lower()} held until {cfg['quiet_end']}",
                      channel="system", status="held", run_id=run["id"])
        meta["held_until"] = iso(until)
        _save(run, next_at=iso(until), meta=meta)
        return
    meta.pop("held_until", None)
    _execute(run, key, p, cfg, meta)
    meta.setdefault("done_steps", []).append(key)
    idx += 1
    if idx >= len(keys):
        _save(run, step_index=idx, status="completed",
              outcome=run.get("outcome") or "nurse alerted", meta=meta)
        return
    _save(run, step_index=idx, next_at=iso(t + _delay(keys[idx], run, cfg)), meta=meta)


def _execute(run: dict, key: str, p: dict, cfg: dict, meta: dict) -> None:
    rid = run["id"]
    fast = run.get("speed") == "fast"
    missed = int(meta.get("missed") or 2)
    fn = first_name(p["name"])
    if key == "device":
        log_event(p["id"], "device_beep", f"Device beep + blinking teal light on {fn}'s SpiroBuddy",
                  detail="A soft chime; a press on the device snoozes it for 15 min.",
                  channel="device", actor="patient", to_name=fn, status="ok", run_id=rid)
    elif key == "patient_whatsapp":
        if not has_consent(cfg):
            log_event(p["id"], "whatsapp", f"WhatsApp to {fn} skipped – no recorded consent (flag + date)",
                      channel="whatsapp", actor="patient", status="skipped", run_id=rid)
        else:
            messages.send_reminder(p, cfg, missed, run_id=rid)
    elif key == "patient_call":
        calls.place_call(p, "reminder", "patient", p["name"], cfg.get("patient_phone"),
                         p.get("language") or "en", run_id=rid,
                         ring_s=FAST_RING_S if fast else int(cfg.get("ring_s") or 30),
                         consent=has_consent(cfg), missed=missed,
                         style=cfg.get("call_style") or "ivr", consent_fresh=consent_current(cfg))
    elif key == "guardian":
        _guardian_step(run, p, cfg, meta, fast, missed)
    elif key == "nurse":
        _nurse_step(run, p, meta, missed)


def _guardian_step(run, p, cfg, meta, fast, missed) -> None:
    rid = run["id"]
    gs = list_guardians(p["id"])
    red = bool(meta.get("red_flag"))
    if not gs:
        log_event(p["id"], "guardian_whatsapp", "No guardian in the care circle – skipped",
                  channel="system", status="skipped", run_id=rid)
        return
    t = now()
    called = False
    for g in gs:
        label = guardian_label(g)
        qs, qe = guardian_quiet(g, cfg)
        if not red and not meta.get("override_quiet") and in_quiet(t, qs, qe):
            log_event(p["id"], "quiet_hold", f"{label}: quiet hours ({qs}–{qe}) – not contacted",
                      channel="system", actor="guardian", to_name=label, status="held", run_id=rid)
            continue
        if not has_consent(g):
            log_event(p["id"], "guardian_whatsapp", f"{label}: skipped – no recorded consent (flag + date)",
                      channel="system", actor="guardian", to_name=label, status="skipped", run_id=rid)
            continue
        ch = g.get("channel") or "both"
        if ch in ("whatsapp", "both"):
            messages.send_guardian_alert(p, g, missed, bool(meta.get("patient_answered")),
                                         run_id=rid, red_flag=red)
        elif ch == "sms":
            log_event(p["id"], "sms", f"SMS to {label} (dry run – SMS in India needs DLT registration)",
                      detail=messages.guardian_alert_text(p, g, missed, False, red),
                      channel="sms", actor="guardian", to_name=label, status="dry_run", run_id=rid)
        if ch in ("call", "both") and not called:
            called = True
            calls.place_call(p, "guardian_red_flag" if red else "guardian", "guardian", label,
                             g.get("phone"), g.get("language") or "hi", run_id=rid, guardian=g,
                             ring_s=FAST_RING_S if fast else int(cfg.get("ring_s") or 30),
                             consent=has_consent(g), missed=missed,
                             consent_fresh=consent_current(g))


def _nurse_step(run, p, meta, missed) -> None:
    rid = run["id"]
    evs = st().select("escalation_events", [("run_id", "eq", rid)], order="id")
    unanswered = [e.get("to_name") for e in evs if e.get("kind") == "no_answer"]
    red = bool(meta.get("red_flag"))
    if red:
        title = f"{p['name']}: asked for help (red flag) – call now"
        kind, sev = "red_flag", "red"
    elif unanswered:
        who = ", ".join(dict.fromkeys(u for u in unanswered if u))
        title = f"{p['name']}: {missed} missed sessions – no answer from {who}"
        kind, sev = "no_answer", "red"
    else:
        title = f"{p['name']}: {missed} missed sessions in a row – please call"
        kind, sev = "missed", "red"
    steps = "; ".join(e.get("title") or "" for e in evs if e.get("kind") not in ("start",))[:1200]
    a = alerts.raise_alert(p["id"], kind, sev, title, detail=steps, run_id=rid)
    log_event(p["id"], "nurse_alert", "Nurse alerted – red on the dashboard", detail=title,
              channel="dashboard", actor="nurse", status="ok", run_id=rid, ref_id=a.get("id"))


# ----------------------------------------------------------------------------- responses

def patient_response(pid: int, intent: str, source: str = "") -> None:
    with _lock:
        run = active_run(pid)
        p = patient(pid) or {"name": "Patient"}
        fn = first_name(p["name"])
        if run:
            meta = _meta(run)
            meta["patient_answered"] = True
            _save(run, meta=meta)
        if intent == "done":
            if run:
                resolve(run, "patient_done", f"{fn} says the session is done ✅ – ladder stopped "
                                             f"(the device count confirms it)", "patient")
        elif intent == "snooze":
            if run and (run.get("snoozes") or 0) < MAX_SNOOZES:
                cfg = get_settings(pid)
                keys = _enabled_keys(cfg, run)
                fast = run.get("speed") == "fast"
                delta = timedelta(seconds=FAST_SNOOZE_S) if fast else \
                    timedelta(minutes=int(cfg.get("snooze_min") or 15))
                at = now() + delta
                idx = keys.index("patient_call") if "patient_call" in keys else run.get("step_index")
                meta = _meta(run)
                meta["done_steps"] = [k for k in meta.get("done_steps", [])
                                      if k in keys and keys.index(k) < idx]
                _save(run, step_index=idx, next_at=iso(at), snoozes=(run.get("snoozes") or 0) + 1,
                      meta=meta)
                log_event(pid, "snooze", f"{fn} asked to be reminded in "
                                         f"{'15 min' if not fast else '15 min (12 s in fast-forward)'}",
                          detail=f"Next reminder call at {at.strftime('%H:%M:%S')}",
                          channel="system", actor="patient", status="info", run_id=run["id"])
            elif run:
                log_event(pid, "snooze", f"{fn} asked for another delay – the ladder continues",
                          channel="system", actor="patient", status="info", run_id=run["id"])
        elif intent == "call_me":
            a = alerts.raise_alert(pid, "callback", "amber", f"{p['name']} asked to talk to a nurse",
                                   detail=f"Request via {source}. Please call back.",
                                   run_id=run["id"] if run else None)
            log_event(pid, "nurse_alert", f"Call-back request from {fn} sent to the nurse",
                      channel="dashboard", actor="nurse", status="ok",
                      run_id=run["id"] if run else None, ref_id=a.get("id"))
            if run:
                resolve(run, "nurse_callback", "Handed to the nurse (call-back requested)", "patient")


def guardian_response(pid: int, guardian: dict | None, intent: str, source: str = "") -> None:
    with _lock:
        run = active_run(pid)
        p = patient(pid) or {"name": "Patient"}
        label = guardian_label(guardian) if guardian else "Family"
        if intent == "guardian_ack":
            if run:
                resolve(run, "guardian_ack", f"{label} will check on {first_name(p['name'])} – ladder stopped",
                        "guardian")
            else:
                log_event(pid, "inbound", f"{label} will check on {first_name(p['name'])}",
                          channel="system", actor="guardian", status="info")
        elif intent == "nurse":
            a = alerts.raise_alert(pid, "callback", "amber", f"{label} asked the nurse to call back",
                                   detail=f"About {p['name']}. Request via {source}.",
                                   run_id=run["id"] if run else None)
            log_event(pid, "nurse_alert", f"Call-back request from {label} sent to the nurse",
                      channel="dashboard", actor="nurse", status="ok",
                      run_id=run["id"] if run else None, ref_id=a.get("id"))
            if run:
                resolve(run, "nurse_callback", "Handed to the nurse (family asked for a call-back)",
                        "guardian")


def red_flag(pid: int, text: str, source: str = "", from_guardian: dict | None = None,
             speed: str | None = None) -> dict:
    """Red-flag words / HELP: fixed message (sent by the caller), red alert now, family told,
    quiet hours ignored."""
    p = patient(pid) or {"name": "Patient"}
    who = guardian_label(from_guardian) if from_guardian else first_name(p["name"])
    a = alerts.raise_alert(pid, "red_flag", "red", f"{p['name']}: red-flag message – call now",
                           detail=f"{who} wrote: “{text[:300]}” (via {source}). "
                                  f"The fixed 'contact your nurse / call 112' message was sent.",
                           dedupe_hours=1)
    log_event(pid, "red_flag", f"Red flag from {who}: “{text[:120]}”",
              detail="Fixed message sent: contact your nurse now / call 112. Nurse alerted.",
              channel="system", actor="guardian" if from_guardian else "patient", status="warn",
              ref_id=a.get("id"))
    cur = active_run(pid)
    sp = speed or (cur.get("speed") if cur else "real")
    run = start(pid, reason="red_flag", speed=sp, red_flag=True, override_quiet=True)
    return run


def on_call_unanswered(call: dict) -> None:
    """In fast-forward, an unanswered call brings the next step forward a little."""
    rid = call.get("run_id")
    if not rid:
        return
    run = get_run(rid)
    if not run or run.get("status") != "active" or run.get("speed") != "fast":
        return
    nxt = to_dt(run.get("next_at"))
    soon = now() + timedelta(seconds=3)
    if nxt and nxt > soon:
        _save(run, next_at=iso(soon))


# ----------------------------------------------------------------------------- tick

def _auto_resolve() -> None:
    for run in st().select("escalations", [("status", "eq", "active")]):
        if _meta(run).get("red_flag"):
            continue
        created = to_dt(run.get("created_at"))
        rows = st().select("sessions", [("patient_id", "eq", run["patient_id"])],
                           order="started_at", desc=True, limit=1)
        if rows and created:
            s_at = to_dt(rows[0].get("started_at"))
            if s_at and s_at > created:
                resolve(run, "session_done",
                        f"Session done at {s_at.strftime('%H:%M')} ✅ – ladder stopped", "patient")


def _cheers() -> None:
    """Queued family cheers are 'played' after the patient's next session."""
    global _seen_sessions
    rows = st().select("sessions", order="id", desc=True, limit=40,
                       columns="id,patient_id,slot_hour")
    latest: dict[int, dict] = {}
    for r in rows:
        latest.setdefault(r["patient_id"], r)
    if _seen_sessions is None:
        _seen_sessions = {pid: r["id"] for pid, r in latest.items()}
        return
    for pid, r in latest.items():
        if r["id"] > _seen_sessions.get(pid, 0):
            _seen_sessions[pid] = r["id"]
            messages.mark_cheers_played(pid, r.get("slot_hour"))


def reset_memory() -> None:
    global _seen_sessions, _last_scan, _last_trend
    _seen_sessions = None
    _last_scan = _last_trend = 0.0


def auto_trigger() -> int:
    """Start a ladder when a patient has just missed N sessions in a row (N per patient)."""
    if not env_flag("COMMS_AUTO_ESCALATE", "1"):
        return 0
    t = now()
    last_hour = t.hour - 1
    if not FIRST_SLOT <= last_hour <= LAST_SLOT:
        return 0
    started = 0
    today = t.date().isoformat()
    existing = {(r["patient_id"], r.get("slot_hour")) for r in
                st().select("escalations", [("slot_date", "eq", today)],
                            columns="patient_id,slot_hour")}
    for p in st().select("patients", columns="id"):
        cfg = get_settings(p["id"])
        if not cfg.get("auto") or in_quiet(t, cfg["quiet_start"], cfg["quiet_end"]):
            continue
        if (p["id"], last_hour) in existing or active_run(p["id"]):
            continue
        d = service.patient_detail(p["id"])
        if not d:
            continue
        trailing = 0
        for s in reversed([s for s in d["today"] if s["status"] in ("done", "missed")]):
            if s["status"] != "missed":
                break
            trailing += 1
        last = next((s for s in d["today"] if s["hour"] == last_hour), None)
        cur = next((s for s in d["today"] if s["hour"] == t.hour), None)
        if trailing >= int(cfg.get("trigger_missed") or 2) and last and last["status"] == "missed" \
                and not (cur and cur["status"] == "done"):
            start(p["id"], reason="missed", speed="real", slot_hour=last_hour, missed=trailing)
            started += 1
    return started


def tick() -> dict:
    """One pass: expire simulator calls, run due steps, auto-resolve, cheers, auto triggers."""
    global _last_scan, _last_trend
    if not _lock.acquire(blocking=False):
        return {"skipped": True}
    try:
        calls.expire_simulated()
        ran = 0
        t = now()
        for run in st().select("escalations", [("status", "eq", "active")]):
            nxt = to_dt(run.get("next_at"))
            if nxt is None or nxt <= t:
                _tick_run(run)
                ran += 1
        _auto_resolve()
        _cheers()
        started = 0
        if time.time() - _last_scan > 60:
            _last_scan = time.time()
            try:
                started = auto_trigger()
            except Exception as e:
                log.warning("auto trigger failed: %s", e)
        global _last_consent
        if time.time() - _last_consent > 3600 and env_flag("COMMS_CONSENT_RENEWAL", "1"):
            _last_consent = time.time()
            try:
                from . import consent
                consent.weekly_check()
            except Exception as e:
                log.warning("consent renewal check failed: %s", e)
        if time.time() - _last_trend > 600:
            _last_trend = time.time()
            try:
                from . import trend
                trend.check_all()
            except Exception as e:
                log.warning("trend check failed: %s", e)
        return {"ran": ran, "started": started}
    finally:
        _lock.release()


def busy() -> bool:
    """True when something needs second-by-second ticking (fast runs, ringing calls)."""
    if st().select("escalations", [("status", "eq", "active"), ("speed", "eq", "fast")],
                   limit=1, columns="id"):
        return True
    return bool(st().select("calls", [("status", "in", ["ringing", "in-progress"])], limit=1,
                            columns="id"))


__all__ = ["start", "stop", "advance", "tick", "patient_response", "guardian_response",
           "red_flag", "list_runs", "public_run", "active_run", "STEP_KEYS"]
