"""Patient login with the hospital registration number + a 6-digit PIN (docs/rebuild/REGNO_PIN_BRIEF.md).

The logic lives here; the HTTP routes are in routes_me.py. In plain words:
- every patient has a registration number (patients.mrn), made by the server as
  <hospital prefix>-<6 digits>, e.g. DGH-000001, or typed by staff (the hospital's own number);
- the PIN is 6 digits made by the server, kept only as an argon2 hash, shown once to staff;
- 5 wrong PINs lock that patient for 15 minutes.

The three PIN columns exist on Supabase only after supabase/schema_v2.sql is pasted again. Until
then columns_ready() is False and callers answer "not set up yet" instead of failing.
"""
from __future__ import annotations

import logging
import re
import secrets
import time
from datetime import timedelta

from . import authz
from .config import demo_mode, iso, now_local, parse_dt
from .seed_auth import hasher

log = logging.getLogger("spirobuddy.patient_login")

PIN_LEN = 6
MAX_FAILS = 5                       # wrong PINs in a row -> locked
LOCK_MINUTES = 15
IP_TRIES = 20                       # failed tries per IP per 15 minutes
IP_WINDOW_SECONDS = 15 * 60
DEMO_PIN = "246810"                 # Ravi (patient 1), DEMO_MODE only
DEMO_PATIENT_ID = 1
PIN_COLS = "pin_hash,pin_failed,pin_locked_until"

MSG_NOT_SET_UP = "This login is not set up yet - please ask the hospital."
MSG_WRONG = "That number and PIN don't match. Please check the slip or ask the hospital."
MSG_LOCKED = ("Too many wrong tries. Please wait 15 minutes and try again, "
              "or ask the hospital for a new PIN.")
MSG_BAD_FORMAT = "Please type your hospital number and the 6 numbers of your PIN."
MSG_IP_LIMIT = "Too many tries from this phone. Please wait 15 minutes and try again."

_WEAK_PINS = {"000000", "111111", "222222", "333333", "444444", "555555", "666666", "777777",
              "888888", "999999", "123456", "654321", "012345", "123123"}


def now():
    """Wrapped so tests can move the clock."""
    return now_local()


# ----------------------------------------------------------------------------- are the columns there

_PROBE_SECONDS = 30                 # how long a "no" is remembered, so a fresh paste works soon


def columns_ready(st) -> bool:
    """True if patients has the PIN columns. Always true for the local SQLite file (it adds them
    itself); on Supabase it is true after schema_v2.sql is pasted again. Never raises."""
    if getattr(st, "name", "") != "supabase":
        return True
    cached = vars(st).get("_sb_login_cols")
    if cached is not None and (cached[0] or time.monotonic() - cached[1] < _PROBE_SECONDS):
        return cached[0]
    try:
        st.select("patients", limit=1, columns="id," + PIN_COLS)
        ok = True
    except Exception as e:          # a missing column or an outage: either way, not ready now
        log.info("patient login columns not usable yet: %s", str(e)[:160])
        ok = False
    try:
        st._sb_login_cols = (ok, time.monotonic())
    except Exception:
        pass
    return ok


# ----------------------------------------------------------------------------- registration numbers

_CANON_BAD = re.compile(r"\s+")
_GENERATED = re.compile(r"^([A-Z]{2,6})-?(\d{6})$")
REGNO_OK = re.compile(r"^[A-Z0-9][A-Z0-9/_.\-]{1,38}[A-Z0-9]$")


def canonical_regno(text) -> str:
    """How a registration number is stored: no spaces, capital letters."""
    return _CANON_BAD.sub("", str(text or "")).upper()


def regno_candidates(text) -> list[str]:
    """The forms of what a person typed that may be stored: capitals, no spaces, and the
    PREFIX-000000 form for a number typed without the dash."""
    c = canonical_regno(text)
    if not c or len(c) > 40:
        return []
    out = [c]
    m = _GENERATED.match(c)
    if m:
        out.append(f"{m.group(1)}-{m.group(2)}")
    return list(dict.fromkeys(out))


def hospital_prefix(hospital_id) -> str:
    """Hospital settings reg_prefix, else the initials of the hospital name ("Demo General
    Hospital (fictional)" -> DGH). Falls back to SB."""
    hid = hospital_id or authz.LEGACY_HOSPITAL_ID
    try:
        rows = authz.ident().select("hospitals", [("id", "eq", hid)], columns="name,settings", limit=1)
    except Exception:
        rows = []
    row = rows[0] if rows else {}
    settings = row.get("settings") if isinstance(row.get("settings"), dict) else {}
    custom = canonical_regno(settings.get("reg_prefix"))
    if re.fullmatch(r"[A-Z]{2,6}", custom or ""):
        return custom
    name = re.sub(r"\(.*?\)", " ", str(row.get("name") or ""))
    initials = "".join(w[0] for w in re.findall(r"[A-Za-z]+", name))[:5].upper()
    return initials if len(initials) >= 2 else "SB"


def _hospital_rows(st, hospital_id) -> list[dict]:
    """id + mrn of every patient in this hospital (old rows without a hospital belong to hospital 1)."""
    hid = int(hospital_id or authz.LEGACY_HOSPITAL_ID)
    if hid == authz.LEGACY_HOSPITAL_ID:
        rows = st.select("patients", columns="id,hospital_id,mrn")
        return [r for r in rows if int(r.get("hospital_id") or authz.LEGACY_HOSPITAL_ID) == hid]
    return st.select("patients", [("hospital_id", "eq", hid)], columns="id,hospital_id,mrn")


def next_regno(st, hospital_id) -> str:
    """The next free <prefix>-<6 digits> in this hospital."""
    prefix = hospital_prefix(hospital_id)
    rows = _hospital_rows(st, hospital_id)
    top = 0
    for r in rows:
        m = re.fullmatch(re.escape(prefix) + r"-(\d{6})", canonical_regno(r.get("mrn")))
        if m:
            top = max(top, int(m.group(1)))
    return f"{prefix}-{top + 1:06d}"


def ensure_regno(st, patient: dict) -> str:
    """The patient's registration number; makes and saves one if there is none."""
    have = canonical_regno(patient.get("mrn"))
    if have:
        return have
    last: Exception | None = None
    for _ in range(3):              # two patients made at once may pick the same number: try again
        number = next_regno(st, patient.get("hospital_id"))
        try:
            st.update("patients", [("id", "eq", patient["id"])], {"mrn": number})
            patient["mrn"] = number
            return number
        except Exception as e:
            last = e
    raise RuntimeError(f"could not save a registration number: {last}")


def regno_taken(st, hospital_id, number: str, except_pid=None) -> bool:
    rows = _hospital_rows(st, hospital_id)
    return any(canonical_regno(r.get("mrn")) == number and r["id"] != except_pid for r in rows)


# ----------------------------------------------------------------------------- PINs

def new_pin() -> str:
    while True:
        pin = f"{secrets.randbelow(10 ** PIN_LEN):0{PIN_LEN}d}"
        if pin not in _WEAK_PINS:
            return pin


def clean_pin(text) -> str | None:
    """The 6 digits a person typed (spaces ignored), or None if it is not 6 digits."""
    s = _CANON_BAD.sub("", str(text or ""))
    return s if re.fullmatch(r"\d{%d}" % PIN_LEN, s) else None


def hash_pin(pin: str) -> str:
    return hasher().hash(pin)


def pin_matches(stored: str | None, pin: str) -> bool:
    """Checks the PIN. With nothing stored it still does the slow check on a dummy, so the time
    time spent does not tell whether the number exists."""
    from .routes_auth import _verify
    return _verify(stored, pin)


def is_locked(row: dict) -> bool:
    until = row.get("pin_locked_until")
    try:
        return bool(until) and parse_dt(until) > now()
    except Exception:
        return False


def set_pin(st, pid: int, pin: str) -> None:
    st.update("patients", [("id", "eq", pid)],
              {"pin_hash": hash_pin(pin), "pin_failed": 0, "pin_locked_until": None})


def note_failure(st, row: dict) -> bool:
    """Count one wrong PIN. True if this one locked the patient."""
    fails = int(row.get("pin_failed") or 0) + 1
    if fails >= MAX_FAILS:
        st.update("patients", [("id", "eq", row["id"])],
                  {"pin_failed": 0, "pin_locked_until": iso(now() + timedelta(minutes=LOCK_MINUTES))})
        return True
    st.update("patients", [("id", "eq", row["id"])], {"pin_failed": fails})
    return False


def note_success(st, row: dict) -> None:
    if int(row.get("pin_failed") or 0) or row.get("pin_locked_until"):
        st.update("patients", [("id", "eq", row["id"])], {"pin_failed": 0, "pin_locked_until": None})


# ----------------------------------------------------------------------------- the demo patient

def demo_credentials(st) -> dict:
    """What the demo box on the login page shows: Ravi's number and the fixed PIN, only in
    DEMO_MODE, and only while that PIN still works (staff may have made a new one)."""
    if not demo_mode():
        return {"demo": False}
    try:
        from . import seed_patient_login
        rows = st.select("patients", [("id", "eq", DEMO_PATIENT_ID)], limit=1)
        if not rows:
            return {"demo": False}
        row = rows[0]
        if not canonical_regno(row.get("mrn")) or (columns_ready(st) and not row.get("pin_hash")):
            seed_patient_login.ensure(st)           # an older database: make them now
            rows = st.select("patients", [("id", "eq", DEMO_PATIENT_ID)], limit=1)
            row = rows[0] if rows else row
        number = canonical_regno(row.get("mrn"))
        if not number or not columns_ready(st):
            return {"demo": False}
        out = {"demo": True, "registration_no": number, "name": row.get("name"), "pin": None}
        if row.get("pin_hash") and pin_matches(row["pin_hash"], DEMO_PIN):
            out["pin"] = DEMO_PIN
        return out
    except Exception as e:
        log.warning("demo login hint skipped: %s", e)
        return {"demo": False}
