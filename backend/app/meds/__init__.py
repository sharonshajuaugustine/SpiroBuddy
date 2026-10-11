"""Digital prescription: the doctor types it, the patient sees it on the phone (Contract H).

normalise.py  pure functions: dose notation (1-0-1, BD, TDS, SOS...) -> times; no AI, no guessing.
service.py    the database logic: issue, stop, replace, doses, the pharmacist check token.
seed_meds.py  one fictional prescription for the demo patient (and its wipe).
Routes live in backend/app/routes_meds.py.
"""
