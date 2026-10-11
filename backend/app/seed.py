"""Fake demo patients with 7 days of history, timed relative to *now* (TZ_NAME).

The mix is chosen so the dashboard always shows green, yellow AND red patients:
  1 Ravi Kumar    – live demo patient, green, current hour left pending for the live demo
  2 Priya Sharma  – green          3 Abdul Rahman – red (very few sessions)
  4 Lakshmi Iyer  – yellow         5 Mohan Das    – red (last 2 slots missed, breathes too fast)
  6 Sreedevi Nair – green (Malayalam)  7 Arjun Reddy – yellow (best breath well below personal best)
Ages/operations follow the India-fit list (docs/HANDOFF.md): CABG man in his 60s, knee replacement
woman in her 60s, gallbladder (cholecystectomy) woman in her 40s, man ~50 in post-TB lung rehab.
All people and hospitals are fictional.
Before ~9:00 the colour is judged on yesterday, which follows the same patterns.

The demo "autopilot" keeps the green/yellow patients (and Ravi's past hours) ticking as the
day goes on, so the board still looks right hours after seeding.

CLI:  python -m backend.app.seed [--target demo|supabase] [--force]
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import time
from datetime import datetime, timedelta

import numpy as np

from . import rules, service
from .config import FIRST_SLOT, LAST_SLOT, LABELS, TZ, iso, now_local
from .store import Store

log = logging.getLogger("spirobuddy.seed")

ALL_HOURS = list(range(FIRST_SLOT, LAST_SLOT + 1))

# ability = typical peak as a fraction of target; ramp goes from day -6 to day -2.
PROFILES = {
    1: dict(name="Ravi Kumar", age=58, sex="M", surgery="Abdominal surgery (open hernia repair)",
            surgery_days_ago=8, language="hi", target_ml=2000, ramp=(0.62, 0.88), today=0.90,
            err=0.25, errs=["no_hold", "too_fast", "too_shallow"], miss={13}, auto=True),
    2: dict(name="Priya Sharma", age=44, sex="F", surgery="Laparoscopic cholecystectomy (gallbladder)",
            surgery_days_ago=5, language="en", target_ml=2500, ramp=(0.75, 0.95), today=0.97,
            err=0.10, errs=["no_hold", "too_fast"], miss=set(), auto=True),
    3: dict(name="Abdul Rahman", age=63, sex="M", surgery="Heart bypass surgery (CABG)",
            surgery_days_ago=9, language="en", target_ml=1500, ramp=(0.50, 0.65), today=0.62,
            err=0.40, errs=["too_shallow", "no_hold"], only={10, 14}, auto=False),
    4: dict(name="Lakshmi Iyer", age=66, sex="F", surgery="Total knee replacement",
            surgery_days_ago=6, language="ta", target_ml=1500, ramp=(0.60, 0.85), today=0.62,
            err=0.30, errs=["too_shallow", "no_hold"], miss={10, 13, 15, 18, 20}, auto=True),
    5: dict(name="Mohan Das", age=50, sex="M", surgery="Lung rehab after TB treatment (post-TB)",
            surgery_days_ago=7, language="hi", target_ml=1750, ramp=(0.55, 0.80), today=0.75,
            err=0.45, errs=["too_fast", "too_fast", "no_hold"],
            only={8, 9, 11, 13, 15, 17, 19, 21}, lag=2, auto=False),
    6: dict(name="Sreedevi Nair", age=54, sex="F", surgery="Hysterectomy",
            surgery_days_ago=4, language="ml", target_ml=2250, ramp=(0.70, 0.92), today=0.93,
            err=0.15, errs=["no_hold", "too_fast"], miss={14}, auto=True),
    7: dict(name="Arjun Reddy", age=41, sex="M", surgery="Appendix removal (appendectomy)",
            surgery_days_ago=3, language="en", target_ml=3000, ramp=(0.70, 0.95), today=0.60,
            err=0.20, errs=["no_hold", "too_shallow"], miss=set(), auto=True),
}
HOLD_TARGET = 3.0
BREATHS_PER_SESSION = 10


def _rng(*parts) -> np.random.Generator:
    h = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def planned_done(pid: int, hour: int) -> bool:
    """Does this patient's daily pattern include a session at `hour`?"""
    p = PROFILES[pid]
    if "only" in p:
        return hour in p["only"]
    return hour not in p["miss"]


def ability(pid: int, days_ago: int) -> float:
    p = PROFILES[pid]
    if days_ago <= 1:            # today and yesterday share the "today" picture
        return p["today"]
    lo, hi = p["ramp"]           # days_ago 6..2 -> lo..hi
    return lo + (hi - lo) * (6 - days_ago) / 4


def make_session(pid: int, day: datetime, hour: int, days_ago: int, rng) -> tuple[dict, list]:
    from . import models_ml
    p = PROFILES[pid]
    target = p["target_ml"]
    eff_target = target * ability(pid, days_ago)
    minute = int(rng.integers(3, 50))
    started = day.replace(hour=hour, minute=minute, second=int(rng.integers(0, 60)))
    t0 = int(started.timestamp() * 1000)
    breaths = []
    for i in range(BREATHS_PER_SESSION):
        label = p["errs"][int(rng.integers(len(p["errs"])))] if rng.random() < p["err"] else "good"
        _, feats = models_ml.make_breath(label, eff_target, rng)
        feats = dict(feats)
        feats["pct_target"] = round(feats["peak_ml"] / target, 3)
        breaths.append({"patient_id": pid, "t": t0 + i * 15000 + int(rng.integers(0, 4000)),
                        "features": feats, "label": label,
                        "score": rules.score(feats, target, HOLD_TARGET)})
    best = max(b["features"]["peak_ml"] for b in breaths)
    sess = {"patient_id": pid, "started_at": iso(started), "slot_date": day.date().isoformat(),
            "slot_hour": hour, "breaths_count": len(breaths), "best_ml": round(best, 1),
            "avg_score": round(sum(b["score"] for b in breaths) / len(breaths), 1),
            "source": "demo"}
    return sess, breaths


def bulk_insert(st: Store, items: list[tuple[dict, list]]) -> None:
    """Insert sessions, then their breaths and 'done' slots (maps ids by patient/date/hour)."""
    if not items:
        return
    rows = st.insert("sessions", [s for s, _ in items])
    ids = {(int(r["patient_id"]), str(r["slot_date"])[:10], int(r["slot_hour"])): r["id"]
           for r in rows}
    breaths, slots = [], []
    for s, bs in items:
        sid = ids[(s["patient_id"], s["slot_date"], s["slot_hour"])]
        breaths += [{"session_id": sid, **b} for b in bs]
        slots.append({"patient_id": s["patient_id"], "slot_date": s["slot_date"],
                      "slot_hour": s["slot_hour"], "status": "done", "session_id": sid})
    st.insert("breaths", breaths)
    st.upsert("slots", slots)


def _v2_ok(st: Store) -> bool:
    """False for a Supabase project without the 2.0 tables (then only the old tables are seeded)."""
    from . import authz
    return authz.v2_ok(st)


def wipe(st: Store) -> None:
    # Filters are always given: Supabase may block DELETE without a WHERE clause.
    # --- 2.0 hooks: clinical 2.0 tables first (they point at patients), then demo-made logins ---
    if _v2_ok(st):
        try:
            from . import seed_v2
            seed_v2.wipe(st)
        except ImportError:
            pass                                   # backend/app/seed_v2.py comes later
        except Exception as e:
            log.error("2.0 wipe failed: %s", e)
    if _v2_ok(st):              # digital prescriptions point at patients: clear them first (meds/seed_meds.py)
        try:
            from .meds import seed_meds
            seed_meds.wipe(st)
        except Exception as e:
            log.error("prescription wipe failed: %s", e)
    try:
        from . import seed_auth
        seed_auth.wipe(st)
    except Exception as e:
        log.error("login wipe failed: %s", e)
    # --- comms hook: wipe comms tables first (backend/app/comms/seed_comms.py) ---
    try:
        from .comms import seed_comms
        seed_comms.wipe(st)
    except Exception as e:
        log.warning("comms wipe skipped: %s", e)
    st.delete("breaths", [("id", "gte", 0)])
    st.delete("slots", [("patient_id", "gte", 0)])
    st.delete("sessions", [("id", "gte", 0)])
    st.delete("messages", [("id", "gte", 0)])
    st.delete("patients", [("id", "gte", 0)])
    # breaths_labelled is real training data -> never wiped by a demo reset


def seed(st: Store, now: datetime | None = None) -> int:
    t_start = time.time()
    now = now or now_local()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    patients = []
    from . import seed_auth
    v2 = _v2_ok(st)             # 2.0: every demo patient belongs to hospital 1 and has a doctor
    # --- 2.0 hook: hospitals, staff logins, nurse keys, the second hospital (seed_auth.py).
    # --- Before the patients: on Supabase a patient row points at its hospital and doctor.
    try:
        seed_auth.ensure(st, reset=True)
    except Exception as e:
        log.error("login seed failed: %s", e)
    for pid, p in PROFILES.items():
        patients.append({
            **({"hospital_id": seed_auth.DEMO_HOSPITAL_ID,
                "primary_doctor_id": seed_auth.PRIMARY_DOCTOR.get(pid)} if v2 else {}),
            "id": pid, "name": p["name"], "age": p["age"], "sex": p["sex"],
            "surgery": p["surgery"],
            "surgery_date": (today - timedelta(days=p["surgery_days_ago"])).date().isoformat(),
            "language": p["language"], "target_ml": p["target_ml"], "hold_target_s": HOLD_TARGET,
            "family_phone": None, "nurse_phone": None, "personal_best_ml": 0,
            "created_at": iso(now - timedelta(days=p["surgery_days_ago"]))})
    st.insert("patients", patients)
    try:                        # registration numbers + Ravi's demo PIN (seed_patient_login.py)
        from . import seed_patient_login
        seed_patient_login.ensure(st)
    except Exception as e:
        log.warning("patient login seed skipped: %s", e)

    items: list[tuple[dict, list]] = []
    for pid, p in PROFILES.items():
        first_day = min(6, p["surgery_days_ago"] - 1)
        for days_ago in range(first_day, -1, -1):
            day = today - timedelta(days=days_ago)
            rng = _rng("seed", pid, day.date().isoformat())
            if days_ago == 0:
                last = min(now.hour, LAST_SLOT + 1) - 1 - p.get("lag", 0)   # past hours only
            else:
                last = LAST_SLOT - (p.get("lag", 0) + 2 if p.get("lag") else 0)
            for hour in ALL_HOURS:
                if hour > last:
                    break
                if days_ago >= 2:      # older days: the pattern plus a little noise
                    if "only" in p:
                        done = rng.random() < 0.55
                    else:
                        done = planned_done(pid, hour) and rng.random() > 0.08
                else:
                    done = planned_done(pid, hour)
                if done:
                    items.append(make_session(pid, day, hour, days_ago, rng))
    bulk_insert(st, items)

    pb: dict[int, float] = {}
    for s, _ in items:
        pb[s["patient_id"]] = max(pb.get(s["patient_id"], 0), s["best_ml"])
    for pid, best in pb.items():
        st.update("patients", [("id", "eq", pid)], {"personal_best_ml": best})

    _seed_messages(st, now)
    # --- comms hook: guardians, care settings, alerts, ladder history (comms/seed_comms.py) ---
    try:
        from .comms import seed_comms
        seed_comms.seed(st, now)
    except Exception as e:
        log.warning("comms seed skipped: %s", e)
    # --- 2.0 hook: prescriptions, doses, appointments, documents... (seed_v2.py) ---
    if v2:
        try:
            from . import seed_v2
            seed_v2.seed(st, now)
        except ImportError:
            pass                                   # backend/app/seed_v2.py comes later
        except Exception as e:
            log.error("2.0 seed failed: %s", e)
        try:                    # the demo patient's digital prescription (meds/seed_meds.py)
            from .meds import seed_meds
            seed_meds.seed(st, now)
        except Exception as e:
            log.error("prescription seed failed: %s", e)
    log.info("Seeded %d patients, %d sessions in %.1fs", len(patients), len(items),
             time.time() - t_start)
    return len(patients)


def _seed_messages(st: Store, now: datetime) -> None:
    from . import llm, whatsapp
    rows = []
    for pid in (3, 5):
        p = {"id": pid, "name": PROFILES[pid]["name"]}
        hours = [h for h in ALL_HOURS if h < now.hour][-2:] or [20, 21]
        rows.append({"patient_id": pid, "kind": "missed", "to_role": "nurse", "to_number": None,
                     "text": whatsapp.missed_text(p, hours, "en"), "sent": False, "dry_run": True,
                     "created_at": iso(now - timedelta(minutes=10 + pid))})
    stats = {"first_name": "Priya", "done": 14, "due": 14, "best_ml": 2390, "target_ml": 2500}
    rows.append({"patient_id": 2, "kind": "summary", "to_role": "family", "to_number": None,
                 "text": llm.template_summary(stats, "en"), "sent": False, "dry_run": True,
                 "created_at": iso((now - timedelta(days=1)).replace(hour=20, minute=30))})
    st.insert("messages", rows)


def needs_seed(st: Store, now: datetime | None = None) -> bool:
    """Empty, or demo data too old to look right (no slots today or yesterday)."""
    now = now or now_local()
    if st.count("patients") == 0:
        return True
    since = (now.date() - timedelta(days=1)).isoformat()
    return not st.select("slots", [("slot_date", "gte", since)], limit=1,
                         columns="patient_id")


def reset(st: Store) -> int:
    wipe(st)
    return seed(st)


# ----------------------------------------------------------------------------- autopilot

_last_autopilot = 0.0


def autopilot(st: Store, now: datetime | None = None, min_interval_s: float = 60) -> int:
    """Fill elapsed hours today for 'auto' patients per their pattern (never the current hour).
    Lets the demo board stay meaningful all day. Returns the number of sessions added."""
    global _last_autopilot
    if time.time() - _last_autopilot < min_interval_s:
        return 0
    _last_autopilot = time.time()
    now = now or now_local()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    d = today.date().isoformat()
    existing = {(s["patient_id"], int(s["slot_hour"]))
                for s in st.select("slots", [("slot_date", "eq", d)],
                                   columns="patient_id,slot_hour")}
    present = {p["id"] for p in st.select("patients", columns="id")}
    items = []
    for pid, p in PROFILES.items():
        if not p["auto"] or pid not in present:
            continue
        for hour in ALL_HOURS:
            if hour >= now.hour:
                break
            if (pid, hour) in existing or not planned_done(pid, hour):
                continue
            items.append(make_session(pid, today, hour, 0, _rng("auto", pid, d, hour)))
    if items:
        bulk_insert(st, items)
        for pid in {s["patient_id"] for s, _ in items}:
            best = max(s["best_ml"] for s, _ in items if s["patient_id"] == pid)
            row = st.select("patients", [("id", "eq", pid)], columns="personal_best_ml")
            if row and best > float(row[0]["personal_best_ml"] or 0):
                st.update("patients", [("id", "eq", pid)], {"personal_best_ml": best})
        log.info("autopilot added %d sessions", len(items))
    return len(items)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Seed SpiroBuddy demo data")
    ap.add_argument("--target", choices=["demo", "supabase"], default=None,
                    help="demo = local SQLite, supabase = needs SUPABASE_URL + key in .env")
    ap.add_argument("--force", action="store_true", help="wipe and re-seed even if data exists")
    args = ap.parse_args()
    import os
    if args.target:
        os.environ["DATA_BACKEND"] = args.target
    st = service.init_store()
    print(f"Backend: {st.name} ({service.store_note()})")
    if args.target == "supabase" and st.name != "supabase":
        raise SystemExit("Supabase not reachable - check SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY "
                         "and that supabase/schema.sql was run.")
    if args.force or needs_seed(st):
        n = reset(st)
        print(f"Seeded {n} demo patients.")
    else:
        print("Data already present and fresh. Use --force to wipe and re-seed.")


if __name__ == "__main__":
    main()
