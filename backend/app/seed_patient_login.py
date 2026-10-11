"""Seed for patient login: a registration number for every patient who has none, and (only in
DEMO_MODE) the fixed demo PIN for Ravi (patient 1), so the demo box on /patient-login.html works.

Called from seed.py after the demo patients are inserted, so a demo reset makes them again.
Works on a Supabase project that still lacks the PIN columns: the numbers are saved (mrn is an
older column) and the PIN is skipped with a log line.
"""
from __future__ import annotations

import logging

from . import patient_login as pl
from .config import demo_mode

log = logging.getLogger("spirobuddy.seed_patient_login")


def ensure(st) -> dict:
    """-> {"numbers": how many patients got a number, "demo_pin": True if Ravi's PIN was set}."""
    from . import authz
    out = {"numbers": 0, "demo_pin": False}
    if not authz.v2_ok(st):
        return out
    rows = sorted(st.select("patients", columns="id,hospital_id,mrn"), key=lambda r: r["id"])
    for r in rows:
        if pl.canonical_regno(r.get("mrn")):
            continue
        try:
            pl.ensure_regno(st, r)
            out["numbers"] += 1
        except Exception as e:                       # one bad row must not stop the others
            log.warning("no registration number for patient %s: %s", r.get("id"), e)
    if demo_mode():
        if not pl.columns_ready(st):
            log.info("demo PIN skipped: run supabase/schema_v2.sql again to add the PIN columns")
        else:
            try:
                ravi = [r for r in rows if r["id"] == pl.DEMO_PATIENT_ID]
                if ravi:
                    pl.set_pin(st, pl.DEMO_PATIENT_ID, pl.DEMO_PIN)
                    out["demo_pin"] = True
            except Exception as e:
                log.warning("demo PIN not set: %s", e)
    log.info("patient login seed: %s", out)
    return out
