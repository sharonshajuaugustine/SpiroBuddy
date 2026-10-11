"""Business logic shared by the API, the seed script and the demo autopilot."""
from __future__ import annotations

import csv
import logging
import threading
from collections import defaultdict
from datetime import datetime, timedelta

from . import rules
from .config import (FEATURE_KEYS, LABELLED_CSV, LABELS, iso, now_local, parse_dt)
from .store import Store, make_store

log = logging.getLogger("spirobuddy.service")

_store: Store | None = None
_store_note = ""
_best_lock = threading.Lock()       # personal-best read + write must not interleave (record_session)


def init_store() -> Store:
    global _store, _store_note
    _store, _store_note = make_store()
    return _store


def store() -> Store:
    return _store if _store is not None else init_store()


def store_note() -> str:
    return _store_note


def v2_missing() -> bool:
    """True when Supabase lacks the 2.0 tables (schema_v2.sql not run) and we use demo SQLite."""
    from . import store as store_module
    return store_module.v2_missing()


# ----------------------------------------------------------------------------- helpers

def _num(v, default=0.0) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def norm_session(s: dict) -> dict:
    s = dict(s)
    s["started_at"] = iso(parse_dt(s.get("started_at")))
    s["slot_date"] = str(s.get("slot_date"))[:10]
    s["best_ml"] = round(_num(s.get("best_ml")), 1)
    s["avg_score"] = round(_num(s.get("avg_score")), 1)
    return s


def public_patient(p: dict) -> dict:
    keys = ["id", "name", "age", "sex", "surgery", "surgery_date", "language", "target_ml",
            "hold_target_s", "family_phone", "nurse_phone", "personal_best_ml"]
    out = {k: p.get(k) for k in keys}
    out["surgery_date"] = str(out["surgery_date"])[:10] if out["surgery_date"] else None
    out["personal_best_ml"] = round(_num(out["personal_best_ml"]), 1)
    out["target_ml"] = int(_num(out["target_ml"], 2000))
    out["hold_target_s"] = _num(out["hold_target_s"], 3.0)
    return out


def get_patient_row(pid: int) -> dict | None:
    rows = store().select("patients", [("id", "eq", pid)])
    return rows[0] if rows else None


def load_window(now: datetime, patient_id: int | None = None, days: int = 7):
    """Sessions + slots from (today - days + 1) on, optionally for one patient."""
    since = (now.date() - timedelta(days=days)).isoformat()   # one extra day for 'yesterday'
    f = [("slot_date", "gte", since)]
    if patient_id is not None:
        f.append(("patient_id", "eq", patient_id))
    sessions = [norm_session(s) for s in store().select("sessions", f)]
    slots = store().select("slots", f)
    for s in slots:
        s["slot_date"] = str(s["slot_date"])[:10]
    return sessions, slots


def red_flag_patient_ids() -> set[int]:
    """Patients with an unresolved red-flag alert (open, acknowledged or snoozed). Such a patient is
    always shown red ("Needs a call") on the nurse side, never "On track"."""
    try:
        rows = store().select("alerts", [("kind", "eq", "red_flag"), ("status", "neq", "resolved")],
                              columns="patient_id")
    except Exception:          # comms tables not created yet → no red flags
        return set()
    return {int(r["patient_id"]) for r in rows if r.get("patient_id") is not None}


def compute_patient(p: dict, sessions: list[dict], slots: list[dict], now: datetime,
                    red_flags: set[int] | None = None) -> dict:
    """Patient object as in contract D (list fields) plus `today`, `history`, status details."""
    pid = p["id"]
    today = now.date().isoformat()
    my_sessions = [s for s in sessions if s["patient_id"] == pid]
    my_slots = [s for s in slots if s["patient_id"] == pid]
    by_day_slots: dict[str, dict[int, dict]] = defaultdict(dict)
    for s in my_slots:
        by_day_slots[s["slot_date"]][int(s["slot_hour"])] = s
    by_day_sessions: dict[str, list[dict]] = defaultdict(list)
    for s in my_sessions:
        by_day_sessions[s["slot_date"]].append(s)

    today_slots = rules.day_slots(by_day_slots.get(today, {}), today, now)
    basis = rules.status_day(now, today_slots)
    basis_slots = today_slots if basis == today else rules.day_slots(
        by_day_slots.get(basis, {}), basis, now)

    pb = _num(p.get("personal_best_ml"))
    if my_sessions:
        pb = max(pb, max(s["best_ml"] for s in my_sessions))
    best_basis = max([s["best_ml"] for s in by_day_sessions.get(basis, [])], default=0.0)
    ev = rules.evaluate(basis_slots, best_basis, pb)

    history = []
    for i in range(6, -1, -1):
        d = (now.date() - timedelta(days=i)).isoformat()
        ds = by_day_sessions.get(d, [])
        history.append({
            "date": d,
            "best_ml": round(max([s["best_ml"] for s in ds], default=0.0), 1),
            "sessions_done": len(ds),
            "avg_score": round(sum(s["avg_score"] for s in ds) / len(ds), 1) if ds else None,
        })
    recent = [h["best_ml"] for h in history[4:] if h["best_ml"]]
    older = [h["best_ml"] for h in history[1:4] if h["best_ml"]]
    trend = "flat"
    if recent and older:
        r, o = sum(recent) / len(recent), sum(older) / len(older)
        trend = "up" if r > o * 1.05 else ("down" if r < o * 0.95 else "flat")

    today_sessions = by_day_sessions.get(today, [])
    red_flag_open = pid in (red_flags if red_flags is not None else red_flag_patient_ids())
    status, reasons = ev["status"], list(ev["reasons"])
    if red_flag_open:
        status = "red"
        reasons = ["Open red-flag alert"] + [r for r in reasons if r != "on track"]
    out = public_patient(p)
    out["personal_best_ml"] = round(pb, 1)
    out.update({
        "status": status,
        "status_reasons": reasons,
        "red_flag_open": red_flag_open,
        "status_basis": "today" if basis == today else "yesterday",
        "done_today": sum(1 for s in today_slots if s["status"] == "done"),
        "due_today": rules.due_count(today_slots),
        "best_today": round(max([s["best_ml"] for s in today_sessions], default=0.0), 1),
        "trend": trend,
        "trailing_missed": ev["trailing_missed"],
        "last_session_at": max([s["started_at"] for s in my_sessions], default=None),
        "today": today_slots,
        "history": history,
    })
    return out


LIST_KEYS = ["id", "name", "age", "sex", "surgery", "surgery_date", "language", "target_ml",
             "status", "done_today", "due_today", "best_today", "personal_best_ml", "trend",
             "last_session_at", "status_reasons", "status_basis", "hold_target_s", "red_flag_open"]


def list_patients(now: datetime | None = None) -> list[dict]:
    now = now or now_local()
    patients = store().select("patients", order="id")
    sessions, slots = load_window(now)
    flags = red_flag_patient_ids()
    out = []
    for p in patients:
        full = compute_patient(p, sessions, slots, now, flags)
        out.append({k: full[k] for k in LIST_KEYS})
    return out


def patient_detail(pid: int, now: datetime | None = None) -> dict | None:
    now = now or now_local()
    p = get_patient_row(pid)
    if not p:
        return None
    sessions, slots = load_window(now, pid)
    return compute_patient(p, sessions, slots, now)


def label_counts_for(session_ids: list[int]) -> dict[int, dict]:
    counts: dict[int, dict] = {sid: {l: 0 for l in LABELS} for sid in session_ids}
    if not session_ids:
        return counts
    for b in store().select("breaths", [("session_id", "in", session_ids)],
                            columns="session_id,label"):
        if b["label"] in LABELS and b["session_id"] in counts:
            counts[b["session_id"]][b["label"]] += 1
    return counts


def list_sessions(pid: int, limit: int = 20) -> list[dict]:
    rows = [norm_session(s) for s in store().select(
        "sessions", [("patient_id", "eq", pid)], order="started_at", desc=True, limit=limit)]
    counts = label_counts_for([s["id"] for s in rows])
    return [{"id": s["id"], "started_at": s["started_at"], "slot_date": s["slot_date"],
             "slot_hour": s["slot_hour"], "breaths_count": s.get("breaths_count") or 0,
             "best_ml": s["best_ml"], "avg_score": s["avg_score"], "source": s.get("source"),
             "label_counts": counts.get(s["id"], {l: 0 for l in LABELS})} for s in rows]


# ----------------------------------------------------------------------------- writes

def record_session(patient: dict, started_at, breaths: list[dict], source: str = "app") -> dict:
    """Store a session + its breaths, tick the slot. Breaths without label/score get them here."""
    from . import models_ml
    st = store()
    started = parse_dt(started_at)
    target = _num(patient.get("target_ml"), 2000) or 2000
    hold_t = _num(patient.get("hold_target_s"), 3) or 3
    clean = []
    for i, b in enumerate(breaths):
        feats = rules.clean_features(b.get("features") or {})
        label = b.get("label") if b.get("label") in LABELS else models_ml.classify(feats)["label"]
        sc = b.get("score")
        sc = round(float(sc), 1) if isinstance(sc, (int, float)) else rules.score(feats, target, hold_t)
        t = b.get("t")
        t = int(t) if isinstance(t, (int, float)) else int(started.timestamp() * 1000) + i * 15000
        clean.append({"t": t, "features": feats, "label": label, "score": sc})
    best = max([b["features"]["peak_ml"] for b in clean], default=0.0)
    avg = round(sum(b["score"] for b in clean) / len(clean), 1) if clean else 0.0
    slot_hour = rules.clamp_slot_hour(started.hour)
    slot_date = started.date().isoformat()
    sess = st.insert("sessions", [{
        "patient_id": patient["id"], "started_at": iso(started), "slot_date": slot_date,
        "slot_hour": slot_hour, "breaths_count": len(clean), "best_ml": round(best, 1),
        "avg_score": avg, "source": source if source in ("demo", "device", "app") else "app"}])[0]
    sid = sess["id"]
    if clean:
        st.insert("breaths", [{"session_id": sid, "patient_id": patient["id"], **b} for b in clean])
    st.upsert("slots", [{"patient_id": patient["id"], "slot_date": slot_date,
                         "slot_hour": slot_hour, "status": "done", "session_id": sid}])
    # Compare with the value in the store NOW (under a lock), not the copy read when the request
    # started: two sessions arriving together must never lower the personal best (lost update).
    with _best_lock:
        cur = st.select("patients", [("id", "eq", patient["id"])], columns="personal_best_ml")
        if best > _num((cur[0] if cur else patient).get("personal_best_ml")):
            st.update("patients", [("id", "eq", patient["id"])], {"personal_best_ml": round(best, 1)})
    counts = {l: 0 for l in LABELS}
    for b in clean:
        counts[b["label"]] += 1
    return {"session_id": sid, "slot_hour": slot_hour, "slot_date": slot_date,
            "slot_status": "done", "best_ml": round(best, 1), "avg_score": avg,
            "label_counts": counts, "breaths": clean}


def log_message(patient: dict | None, kind: str, to_role: str, to_number: str | None,
                text: str, sent: bool, dry_run: bool, created_at: datetime | None = None) -> dict:
    return store().insert("messages", [{
        "patient_id": patient["id"] if patient else None, "kind": kind, "to_role": to_role,
        "to_number": to_number, "text": text, "sent": bool(sent), "dry_run": bool(dry_run),
        "created_at": iso(created_at or now_local())}])[0]


def list_messages(limit: int = 50) -> list[dict]:
    rows = store().select("messages", order="created_at", desc=True, limit=limit)
    names = {p["id"]: p["name"] for p in store().select("patients", columns="id,name")}
    return [{"id": m["id"], "patient_id": m.get("patient_id"),
             "patient_name": names.get(m.get("patient_id")), "kind": m.get("kind"),
             "to_role": m.get("to_role"), "text": m.get("text"), "sent": bool(m.get("sent")),
             "dry_run": bool(m.get("dry_run")),
             "created_at": iso(parse_dt(m.get("created_at")))} for m in rows]


def save_labelled(person: str, label: str, samples: list, features: dict) -> dict:
    """Store a labelled breath for ML training (DB + backend/data/breaths_labelled.csv)."""
    feats = rules.clean_features(features or {})
    created = iso(now_local())
    store().insert("breaths_labelled", [{"person": person, "label": label, "samples": samples,
                                         "features": feats, "created_at": created}])
    import json
    new_file = not LABELLED_CSV.exists()
    with open(LABELLED_CSV, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new_file:
            w.writerow(["created_at", "person", "label", *FEATURE_KEYS, "samples"])
        w.writerow([created, person, label, *[feats[k] for k in FEATURE_KEYS],
                    json.dumps(samples, separators=(",", ":"))])
    counts = {l: 0 for l in LABELS}
    for r in store().select("breaths_labelled", columns="label"):
        if r["label"] in counts:
            counts[r["label"]] += 1
    return counts


def export_labelled_csv() -> int:
    """Rewrite backend/data/breaths_labelled.csv from the store before training.

    On Render the disk is wiped on every restart, but the labelled breaths are safe in Supabase,
    so ml/train.py (which reads the CSV) still sees every collected breath. Returns the row count.
    """
    import json
    rows = store().select("breaths_labelled", order="id")
    if not rows:
        return 0
    with open(LABELLED_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["created_at", "person", "label", *FEATURE_KEYS, "samples"])
        for r in rows:
            feats = r.get("features") or {}
            if not isinstance(feats, dict) or not all(k in feats for k in FEATURE_KEYS):
                continue
            w.writerow([r.get("created_at"), r.get("person"), r.get("label"),
                        *[feats[k] for k in FEATURE_KEYS],
                        json.dumps(r.get("samples") or [], separators=(",", ":"))])
    return len(rows)


def summary_stats(detail: dict) -> dict:
    """Numbers for the AI/template summary from a patient_detail() result."""
    today = now_local().date().isoformat()
    sessions = [s for s in list_sessions(detail["id"], limit=20) if s["slot_date"] == today]
    lc = {l: 0 for l in LABELS}
    for s in sessions:
        for l in LABELS:
            lc[l] += s["label_counts"].get(l, 0)
    scores = [s["avg_score"] for s in sessions]
    done = detail["done_today"]
    due = max(detail["due_today"], done)
    return {"first_name": detail["name"].split()[0], "surgery": detail.get("surgery"),
            "done": done, "due": due, "best_ml": detail["best_today"],
            "target_ml": detail["target_ml"], "personal_best_ml": detail["personal_best_ml"],
            "avg_score": round(sum(scores) / len(scores), 1) if scores else None,
            "label_counts": lc, "trend": detail["trend"],
            "trailing_missed": detail.get("trailing_missed", 0)}
