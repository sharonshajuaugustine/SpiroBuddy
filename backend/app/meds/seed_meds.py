"""Demo data for the digital prescription: one issued prescription for Ravi (patient 1).

Called from backend/app/seed.py (guarded). Fictional patient, ordinary post-surgery medicines,
issued by the demo doctor. seed() is safe to call twice; wipe() clears the three tables so a demo
reset starts clean (patient ids are reused after a reset).
"""
from __future__ import annotations

import logging

from .. import authz
from .. import service as core
from ..config import now_local
from . import service as meds

log = logging.getLogger("spirobuddy.meds.seed")

RAVI = 1
DOCTOR_ID = 2                        # Dr. Meera Nair (seed_auth.PRIMARY_DOCTOR[1])
DEMO_REG_NO = "DEMO-REG-0001 (fictional)"

LINES = [
    {"drug_name": "Paracetamol", "form": "tablet", "strength": "500 mg", "dose_qty": 1,
     "dose_unit": "tablet", "frequency_raw": "1-0-1", "food_timing": "after_food",
     "duration_days": 5, "instructions": "For pain after the operation."},
    {"drug_name": "Pantoprazole", "form": "tablet", "strength": "40 mg", "dose_qty": 1,
     "dose_unit": "tablet", "frequency_raw": "1-0-0", "food_timing": "before_food",
     "duration_days": 14, "instructions": "Take on an empty stomach in the morning."},
    {"drug_name": "Ondansetron", "form": "tablet", "strength": "4 mg", "dose_qty": 1,
     "dose_unit": "tablet", "frequency_raw": "SOS", "as_needed": True, "food_timing": "any",
     "instructions": "Only when needed for nausea."},
]


def wipe(st) -> None:
    """Remove every prescription, line and dose (they point at patients, which a reset deletes)."""
    for table in ("dose_events", "prescription_items", "prescriptions"):
        st.delete(table, [("id", "gte", 0)])
    meds._last_refresh.clear()


def seed(st, now=None) -> None:
    patient = core.get_patient_row(RAVI)
    if not patient or not authz.v2_ok(st):
        return
    if st.select("prescriptions", [("patient_id", "eq", RAVI)], columns="id", limit=1):
        return
    ident = authz.ident(st)
    doctor = ident.select("staff", [("id", "eq", DOCTOR_ID)], limit=1)
    if not doctor:
        return
    if not doctor[0].get("reg_no_display"):          # a clearly fictional number, shown on the card
        ident.update("staff", [("id", "eq", DOCTOR_ID)], {"reg_no_display": DEMO_REG_NO})
    now = now or now_local()
    # issued at the start of today, so every dose of today is on the screen (also late in the day)
    issued = now.replace(hour=0, minute=0, second=0, microsecond=0)
    meds.create_prescription(patient, DOCTOR_ID, [dict(x) for x in LINES], issued_at=issued)
    log.info("Seeded the demo prescription for patient %s", RAVI)
