"""Digital prescription logic: issue, replace, stop, doses, and the pharmacist check token.

Rules in code (docs/ARCHITECTURE.md Contract H, REBUILD_PLAN 3.12):
- A doctor types the prescription. Saving it is the doctor's sign-off, so it is issued at once
  (the table keeps the contract word "approved"; the screens say "Issued").
- Dose events exist ONLY for issued prescriptions, only for lines with a clear schedule, and never
  for "only when needed" (SOS) lines. Unclear lines are shown to the patient but get no reminder.
- A patient tap is "reported" (stored as reported_taken), never proof that the medicine was taken.
- Replacing a prescription keeps the old one in history ("superseded"); stopping cancels its
  future doses. Nothing is deleted.
- The pharmacist check token is an HMAC of (prescription id, version, patient id) with a server
  secret, so it cannot be guessed, survives a restart and changes when a prescription is replaced.
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import secrets
import threading
import time
from datetime import date, datetime, timedelta

from .. import authz
from .. import service as core
from ..config import TZ, demo_mode, env, iso, now_local, parse_dt
from . import normalise as nz

log = logging.getLogger("spirobuddy.meds")

CURRENT, STOPPED, REPLACED = "approved", "stopped", "superseded"     # prescriptions.status
ISSUED_STATES = (CURRENT, STOPPED, REPLACED)                         # never draft / needs_review / rejected
STATE = {CURRENT: ("current", "Issued"), STOPPED: ("stopped", "Stopped by the doctor"),
         REPLACED: ("replaced", "Replaced by a newer prescription")}
MAX_LINES = 20
REPORTED = "reported_taken"                                           # dose_events.status (Contract H)
DEMO_NOTICE = "Demo - fictional patient. Pharmacy acceptance is not yet tested."
EARLY_MINUTES = 15            # a dose counts as "due" this long before its time


def st():
    return core.store()


def _hospital_of(patient: dict) -> int:
    return int(patient.get("hospital_id") or authz.LEGACY_HOSPITAL_ID)


def _text(v, n: int) -> str:
    s = " ".join(str(v).split()) if v is not None else ""
    return "".join(ch for ch in s if ch.isprintable())[:n]


def _today() -> date:
    return now_local().date()


# ---------------------------------------------------------------------------- lines

def clean_lines(raw, routine=None, today: date | None = None) -> tuple[list[dict], list[dict]]:
    """Validate the typed lines -> (item rows without ids, warnings). Raises ValueError (a message
    for the doctor). A line whose frequency or duration is not understood is KEPT but marked
    unclear and gets no times (so no reminder)."""
    today = today or _today()
    if not isinstance(raw, list) or not raw:
        raise ValueError("add at least one medicine")
    if len(raw) > MAX_LINES:
        raise ValueError(f"at most {MAX_LINES} medicines in one prescription")
    items, warnings = [], []
    for n, line in enumerate(raw, 1):
        if not isinstance(line, dict):
            raise ValueError(f"line {n} is not valid")
        name = _text(line.get("drug_name"), 120)
        if not name:
            raise ValueError(f"line {n}: the medicine name is needed")
        qty = nz.parse_qty(line.get("dose_qty"))
        if qty is None:
            raise ValueError(f"line {n} ({name}): the dose amount is needed (a number above 0)")
        freq_raw = _text(line.get("frequency_raw") or line.get("frequency_code")
                         or line.get("frequency"), 60)
        as_needed = bool(line.get("as_needed"))
        if line.get("times"):
            f = nz.from_times(line.get("times"))
            freq_raw = freq_raw or ", ".join(str(t) for t in (line["times"] if isinstance(line["times"], list) else []))
        elif line.get("slots"):
            f = nz.from_slots(line.get("slots"), routine)
            freq_raw = freq_raw or ", ".join(str(s) for s in (line["slots"] if isinstance(line["slots"], list) else []))
        elif freq_raw:
            f = nz.normalise_frequency(freq_raw, routine)
        elif as_needed:
            f = nz.normalise_frequency("SOS")
        else:
            f = nz.normalise_frequency("")
        as_needed = as_needed or f["kind"] == "as_needed"
        days, until, dur_ok = nz.normalise_duration(line.get("duration_days"), line.get("until_stopped"))
        food, food_ok = nz.normalise_food(line.get("food_timing"))
        unclear: list[str] = []
        if not as_needed and f["unclear"]:
            unclear.append("frequency")
            warnings.append({"code": "unclear_frequency", "line": n, "text":
                             f"Line {n} ({name}): " + (f["reason"] or "frequency not recognised")
                             + " - the patient sees it, but no reminder is set."})
        if not as_needed and not dur_ok:
            unclear.append("duration")
            warnings.append({"code": "unclear_duration", "line": n, "text":
                             f"Line {n} ({name}): give the number of days or 'until stopped' - "
                             "no reminder is set."})
        if not food_ok:
            unclear.append("food_timing")
            warnings.append({"code": "unclear_food", "line": n, "text":
                             f"Line {n} ({name}): the food instruction was not understood."})
        scheduled = (not as_needed) and f["kind"] == "scheduled" and dur_ok and bool(f["times"])
        end = (today + timedelta(days=days - 1)).isoformat() if days else None
        items.append({
            "line_no": n, "drug_name": name, "form": _text(line.get("form"), 30) or None,
            "strength": _text(line.get("strength"), 40) or None, "dose_qty": qty,
            "dose_unit": _text(line.get("dose_unit"), 20).lower() or None,
            "frequency_raw": freq_raw or None,
            "frequency_code": "SOS" if as_needed else f["code"],
            "times": list(f["times"]) if scheduled else [], "food_timing": food,
            "duration_raw": "until stopped" if until else (f"{days} days" if days else None),
            "duration_days": days, "start_date": today.isoformat() if scheduled else None,
            "end_date": end if scheduled else None, "as_needed": as_needed,
            "instructions_raw": _text(line.get("instructions_raw") or line.get("instructions"), 300) or None,
            "confidence": None, "unclear_fields": unclear, "status": "confirmed"})
    return items, warnings


# ---------------------------------------------------------------------------- views

def _slots_of(code: str | None) -> list[str]:
    code = code or ""
    if code == "HS":
        return ["bedtime"]
    parts = code.split("-")
    if len(parts) == 3 and all(p in ("0", "1") for p in parts):
        return [s for s, d in zip(nz.SLOTS, parts) if d == "1"]
    return []


def line_view(it: dict) -> dict:
    qty = it.get("dose_qty")
    unit = it.get("dose_unit") or ""
    times = it.get("times") if isinstance(it.get("times"), list) else []
    return {
        "id": it.get("id"), "line_no": it.get("line_no"), "drug_name": it.get("drug_name"),
        "form": it.get("form"), "strength": it.get("strength"), "dose_qty": qty,
        "dose_unit": unit, "dose_text": (nz.qty_text(qty) + " " + unit).strip(),
        "frequency_raw": it.get("frequency_raw"), "frequency_code": it.get("frequency_code"),
        "slots": _slots_of(it.get("frequency_code")) if times else [], "times": times,
        "food_timing": it.get("food_timing") or "any", "duration_days": it.get("duration_days"),
        "until_stopped": it.get("duration_raw") == "until stopped",
        "start_date": it.get("start_date"), "end_date": it.get("end_date"),
        "as_needed": bool(it.get("as_needed")), "instructions": it.get("instructions_raw"),
        "unclear_fields": it.get("unclear_fields") or [], "scheduled": bool(times)}


_SLOT_WORD = {"morning": "morning", "afternoon": "afternoon", "night": "night", "bedtime": "at bedtime"}
_FOOD_WORD = {"before_food": "before food", "after_food": "after food", "with_food": "with food"}


def english_summary(v: dict) -> str:
    """'1 tablet - morning and night - after food - 5 days' (the pharmacist's page and the card)."""
    parts = [v.get("dose_text") or ""]
    if v.get("as_needed"):
        parts.append("only when needed")
    elif v.get("slots"):
        parts.append(" and ".join(_SLOT_WORD[s] for s in v["slots"]))
    elif v.get("times"):
        parts.append("at " + ", ".join(v["times"]))
    elif v.get("frequency_raw"):
        parts.append(f"as written: {v['frequency_raw']}")
    if v.get("food_timing") in _FOOD_WORD:
        parts.append(_FOOD_WORD[v["food_timing"]])
    if v.get("until_stopped"):
        parts.append("until the doctor says stop")
    elif v.get("duration_days"):
        parts.append(f"{v['duration_days']} days")
    return " · ".join(p for p in parts if p)


def _staff_map(ids) -> dict:
    ids = sorted({int(i) for i in ids if i is not None})
    if not ids:
        return {}
    rows = authz.ident().select("staff", [("id", "in", ids)], columns="id,name,reg_no_display")
    return {r["id"]: r for r in rows}


def _issued_on(rx: dict) -> str | None:
    at = rx.get("reviewed_at")
    if at:
        try:
            return parse_dt(at).date().isoformat()
        except (TypeError, ValueError):
            pass
    return (str(rx["prescribed_on"])[:10] if rx.get("prescribed_on") else None)


def rx_view(rx: dict, items: list[dict], staff: dict | None = None) -> dict:
    state, text = STATE.get(rx.get("status"), (rx.get("status"), rx.get("status")))
    doc = (staff or {}).get(rx.get("reviewed_by") or rx.get("created_by")) or {}
    return {
        "id": rx["id"], "patient_id": rx["patient_id"], "version": rx.get("version") or 1,
        "status": rx.get("status"), "state": state, "state_text": text,
        "issued_on": _issued_on(rx), "prescribed_on": str(rx["prescribed_on"])[:10] if rx.get("prescribed_on") else None,
        "issued_at": rx.get("reviewed_at"), "supersedes_id": rx.get("supersedes_id"),
        "doctor": {"id": rx.get("reviewed_by") or rx.get("created_by"), "name": doc.get("name"),
                   "reg_no_display": doc.get("reg_no_display")},
        "prescriber_on_paper": rx.get("prescriber_on_paper"),
        "lines": [line_view(i) for i in sorted(items, key=lambda x: x.get("line_no") or 0)
                  if i.get("status") != "removed"]}


def _load(pid: int, statuses=ISSUED_STATES) -> list[tuple[dict, list[dict]]]:
    """[(prescription, items)] newest first, only prescriptions that were issued."""
    rxs = st().select("prescriptions", [("patient_id", "eq", pid), ("status", "in", list(statuses))],
                      order="id", desc=True)
    if not rxs:
        return []
    items = st().select("prescription_items", [("prescription_id", "in", [r["id"] for r in rxs])])
    by: dict[int, list] = {}
    for i in items:
        by.setdefault(i["prescription_id"], []).append(i)
    return [(r, by.get(r["id"], [])) for r in rxs]


def medicines_for(pid: int) -> dict:
    """{active, as_needed, history, current}: lines of the current prescriptions split into
    scheduled and only-when-needed, every issued version, and the current prescriptions."""
    pairs = _load(pid)
    staff = _staff_map([x for r, _ in pairs for x in (r.get("reviewed_by"), r.get("created_by"))])
    views = [rx_view(r, i, staff) for r, i in pairs]
    current = [v for v in views if v["state"] == "current"]
    active, as_needed = [], []
    for v in current:
        for ln in v["lines"]:
            row = {**ln, "rx_id": v["id"], "issued_on": v["issued_on"], "doctor": v["doctor"]["name"]}
            (as_needed if ln["as_needed"] else active).append(row)
    return {"active": active, "as_needed": as_needed, "history": views, "current": current}


# ---------------------------------------------------------------------------- issue / replace / stop

def _routine_of(patient: dict):
    r = patient.get("routine")
    return r if isinstance(r, dict) else None


def create_prescription(patient: dict, doctor_id: int | None, raw_lines, *, prescribed_on=None,
                        prescriber_on_paper=None, replaces: int | None = None,
                        issued_at: datetime | None = None, source: str = "doctor_typed"
                        ) -> tuple[dict, list[dict]]:
    """Issue a prescription for `patient`. -> (rx_view, warnings). Raises ValueError (bad input),
    LookupError (the prescription to replace is not this patient's current one)."""
    pid = int(patient["id"])
    now = issued_at or now_local()
    today = now.date()
    items, warnings = clean_lines(raw_lines, _routine_of(patient), today)
    if prescribed_on in (None, ""):
        written = today
    else:
        try:
            written = date.fromisoformat(str(prescribed_on)[:10])
        except ValueError:
            raise ValueError("prescribed_on must be a date like 2026-10-11")
        if written > today or written < today - timedelta(days=365):
            raise ValueError("prescribed_on must be today or an earlier date within a year")
    old = None
    if replaces not in (None, ""):
        try:
            rid = int(replaces)
        except (TypeError, ValueError):
            raise ValueError("replaces must be a prescription number")
        rows = st().select("prescriptions", [("id", "eq", rid), ("patient_id", "eq", pid)], limit=1)
        if not rows or rows[0].get("status") != CURRENT:
            raise LookupError("the prescription to replace is not a current prescription of this patient")
        old = rows[0]
    hospital_id = _hospital_of(patient)
    rx = st().insert("prescriptions", [{
        "hospital_id": hospital_id, "patient_id": pid, "source": source, "document_id": None,
        "status": "draft", "version": (old.get("version") or 1) + 1 if old else 1,
        "supersedes_id": old["id"] if old else None,
        "prescriber_on_paper": _text(prescriber_on_paper, 120) or None,
        "prescribed_on": written.isoformat(), "created_by": doctor_id,
        "created_at": iso(now)}])[0]
    try:
        stamp = iso(now)
        st().insert("prescription_items", [{
            **it, "hospital_id": hospital_id, "prescription_id": rx["id"], "patient_id": pid,
            "confirmed_by": doctor_id, "confirmed_at": stamp, "created_at": stamp} for it in items])
        # the doctor's save is the sign-off: only now does the patient see it
        st().update("prescriptions", [("id", "eq", rx["id"])],
                    {"status": CURRENT, "reviewed_by": doctor_id, "reviewed_at": stamp})
    except Exception:
        st().delete("prescription_items", [("prescription_id", "eq", rx["id"])])
        st().delete("prescriptions", [("id", "eq", rx["id"])])
        raise
    if old:
        st().update("prescriptions", [("id", "eq", old["id"])], {"status": REPLACED})
        _cancel_future(old["id"], now)
    refresh_doses(pid, force=True, now=now)
    return get_prescription(rx["id"]), warnings


def get_prescription(rx_id: int) -> dict | None:
    rows = st().select("prescriptions", [("id", "eq", rx_id)], limit=1)
    if not rows:
        return None
    items = st().select("prescription_items", [("prescription_id", "eq", rx_id)])
    return rx_view(rows[0], items, _staff_map([rows[0].get("reviewed_by"), rows[0].get("created_by")]))


def warnings_of(view: dict) -> list[dict]:
    """The "check this line" notes for a prescription view (from each line's unclear fields)."""
    text = {"frequency": "frequency not recognised - the patient sees it, but no reminder is set",
            "duration": "days or 'until stopped' missing - no reminder is set",
            "food_timing": "the food instruction was not understood"}
    return [{"code": "unclear_" + f, "line": ln["line_no"],
             "text": f"Line {ln['line_no']} ({ln['drug_name']}): {text[f]}."}
            for ln in view["lines"] for f in ln["unclear_fields"] if f in text]


def stop_prescription(rx_id: int, now: datetime | None = None) -> dict:
    """A current prescription -> stopped; its future unreported doses are cancelled."""
    rows = st().select("prescriptions", [("id", "eq", rx_id)], limit=1)
    if not rows:
        raise LookupError("prescription not found")
    if rows[0].get("status") != CURRENT:
        raise ValueError("only a current prescription can be stopped")
    now = now or now_local()
    st().update("prescriptions", [("id", "eq", rx_id)], {"status": STOPPED})
    _cancel_future(rx_id, now)
    return get_prescription(rx_id)


def _cancel_future(rx_id: int, now: datetime) -> int:
    ids = [i["id"] for i in st().select("prescription_items", [("prescription_id", "eq", rx_id)],
                                        columns="id")]
    if not ids:
        return 0
    n = 0
    for d in st().select("dose_events", [("item_id", "in", ids)]):
        if d.get("status") in (REPORTED, "cancelled"):
            continue
        if parse_dt(d["due_at"]) >= now:
            st().update("dose_events", [("id", "eq", d["id"])], {"status": "cancelled"})
            n += 1
    return n


# ---------------------------------------------------------------------------- doses

_last_refresh: dict[int, float] = {}
_refresh_lock = threading.Lock()
REFRESH_EVERY_S = 20.0


def _minute_key(item_id, when) -> tuple:
    return (item_id, parse_dt(when).strftime("%Y-%m-%dT%H:%M"))


def refresh_doses(pid: int, force: bool = False, now: datetime | None = None) -> int:
    """Make the dose events for today and tomorrow of every CURRENT prescription (idempotent).
    Only scheduled lines get any; "only when needed" lines never do. Returns how many were added."""
    with _refresh_lock:
        if not force and time.monotonic() - _last_refresh.get(pid, -1e9) < REFRESH_EVERY_S:
            return 0
        _last_refresh[pid] = time.monotonic()
    patient = core.get_patient_row(pid)
    if not patient or not authz.reminders_allowed(patient):
        return 0
    now = now or now_local()
    pairs = [(r, i) for r, i in _load(pid, (CURRENT,))]
    if not pairs:
        return 0
    item_ids = [i["id"] for _, its in pairs for i in its]
    have = {_minute_key(d["item_id"], d["due_at"]) for d in
            st().select("dose_events", [("item_id", "in", item_ids)], columns="item_id,due_at")}
    new, today = [], now.date()
    for rx, its in pairs:
        try:
            issued = parse_dt(rx.get("reviewed_at")) if rx.get("reviewed_at") else now
        except (TypeError, ValueError):
            issued = now
        for it in its:
            times = it.get("times") if isinstance(it.get("times"), list) else []
            if it.get("as_needed") or not times or it.get("status") == "removed":
                continue
            start = date.fromisoformat(str(it["start_date"])[:10]) if it.get("start_date") else today
            end = date.fromisoformat(str(it["end_date"])[:10]) if it.get("end_date") else None
            for offset in (0, 1):
                day = today + timedelta(days=offset)
                if day < start or (end and day > end):
                    continue
                for hhmm in times:
                    h, m = int(hhmm[:2]), int(hhmm[3:5])
                    due = datetime(day.year, day.month, day.day, h, m, tzinfo=TZ)
                    if due < issued.replace(second=0, microsecond=0) or \
                            _minute_key(it["id"], due.isoformat()) in have:
                        continue
                    have.add(_minute_key(it["id"], due.isoformat()))
                    new.append({"hospital_id": _hospital_of(patient), "patient_id": pid,
                                "item_id": it["id"], "due_at": iso(due), "status": "upcoming",
                                "created_at": iso(now)})
    if new:
        st().insert("dose_events", new)
    return len(new)


def _effective(d: dict, now: datetime, grace: int, paused: bool) -> str:
    s = d.get("status") or "upcoming"
    if s in (REPORTED, "cancelled"):
        return s
    if paused:
        return "paused"
    due = parse_dt(d["due_at"])
    if now < due - timedelta(minutes=EARLY_MINUTES):
        return "upcoming"
    return "due" if now <= due + timedelta(minutes=grace) else "missed"


def _slot_of(due: datetime) -> str:
    return "morning" if due.hour < 12 else ("afternoon" if due.hour < 17 else "night")


def _dose_views(rows: list[dict], patient: dict | None, now: datetime) -> list[dict]:
    if not rows:
        return []
    items = {i["id"]: i for i in st().select("prescription_items",
                                             [("id", "in", sorted({r["item_id"] for r in rows if r.get("item_id")}))])}
    grace = int(authz.hospital_settings(_hospital_of(patient or {})).get("grace_minutes") or 60)
    paused = bool(patient) and not authz.reminders_allowed(patient)
    out = []
    for d in rows:
        it = items.get(d.get("item_id")) or {}
        due = parse_dt(d["due_at"])
        v = line_view(it) if it else {}
        out.append({
            "id": d["id"], "item_id": d.get("item_id"), "rx_id": it.get("prescription_id"),
            "drug_name": it.get("drug_name"), "form": it.get("form"), "strength": it.get("strength"),
            "dose_qty": it.get("dose_qty"), "dose_unit": it.get("dose_unit"),
            "dose_text": v.get("dose_text"), "food_timing": v.get("food_timing"),
            "instructions": it.get("instructions_raw"),
            "due_at": iso(due), "slot": _slot_of(due), "status": _effective(d, now, grace, paused),
            "reported_at": d.get("reported_at"), "reported_by_role": d.get("reported_by_role")})
    return sorted(out, key=lambda x: (x["due_at"], x["id"]))


def doses_for(pid: int, date_from=None, date_to=None, include_cancelled: bool = True) -> list[dict]:
    """The patient's dose events between two dates (inclusive, India time). Default: today and tomorrow."""
    refresh_doses(pid)
    now = now_local()
    lo = parse_dt(date_from).date() if date_from else now.date()
    hi = parse_dt(date_to).date() if date_to else now.date() + timedelta(days=1)
    rows = [d for d in st().select("dose_events", [("patient_id", "eq", pid)])
            if lo <= parse_dt(d["due_at"]).date() <= hi]
    views = _dose_views(rows, core.get_patient_row(pid), now)
    return views if include_cancelled else [v for v in views if v["status"] != "cancelled"]


def today_doses(pid: int) -> list[dict]:
    now = now_local()
    return [d for d in doses_for(pid, now.date().isoformat(), now.date().isoformat(), False)]


def owner_of_dose(dose_id: int) -> int | None:
    rows = st().select("dose_events", [("id", "eq", dose_id)], columns="patient_id", limit=1)
    return int(rows[0]["patient_id"]) if rows else None


def report_dose(dose_id: int, role: str, actor_id: int | None, channel: str = "app") -> tuple[dict, bool]:
    """The patient (or staff on their behalf) reports a dose -> (dose view, newly reported).
    Stored as reported_taken; the screens say "Reported". Reporting twice changes nothing.
    Raises LookupError / ValueError."""
    rows = st().select("dose_events", [("id", "eq", dose_id)], limit=1)
    if not rows:
        raise LookupError("dose not found")
    d, now, new = rows[0], now_local(), False
    if d.get("status") == "cancelled":
        raise ValueError("this medicine was stopped by the doctor")
    if d.get("status") != REPORTED:
        if parse_dt(d["due_at"]).date() > now.date():
            raise ValueError("this dose is for another day - it can be reported on that day")
        st().update("dose_events", [("id", "eq", dose_id)], {
            "status": REPORTED, "reported_at": iso(now), "reported_by_role": role,
            "reported_by_id": actor_id, "channel": channel})
        d, new = st().select("dose_events", [("id", "eq", dose_id)], limit=1)[0], True
    return _dose_views([d], core.get_patient_row(int(d["patient_id"])), now)[0], new


def counts_today(pid: int) -> dict:
    c = {"reported": 0, "due": 0, "missed": 0}
    for d in today_doses(pid):
        if d["status"] == REPORTED:
            c["reported"] += 1
        elif d["status"] in ("due", "missed"):
            c[d["status"]] += 1
    return c


# ---------------------------------------------------------------------------- pharmacist token

_secret_cache: bytes | None = None
_secret_lock = threading.Lock()


def _secret() -> bytes:
    """RX_TOKEN_SECRET if set; else a random secret made once and kept in app_settings (so it
    survives a restart); else (store down) a per-process random one."""
    global _secret_cache
    if _secret_cache:
        return _secret_cache
    with _secret_lock:
        if _secret_cache:
            return _secret_cache
        val = env("RX_TOKEN_SECRET")
        if not val:
            try:
                rows = st().select("app_settings", [("key", "eq", "rx_token_secret")], limit=1)
                if rows and isinstance(rows[0].get("value"), dict) and rows[0]["value"].get("secret"):
                    val = rows[0]["value"]["secret"]
                else:
                    val = secrets.token_hex(32)
                    st().insert("app_settings", [{"key": "rx_token_secret", "hospital_id": None,
                                                  "value": {"secret": val}}])
            except Exception as e:
                log.warning("could not keep the prescription token secret in the store: %s", e)
                val = secrets.token_hex(32)
        _secret_cache = val.encode("utf-8")
        return _secret_cache


def _mac(rx: dict) -> str:
    msg = f"rx:{rx['id']}:v{rx.get('version') or 1}:p{rx['patient_id']}".encode()
    return hmac.new(_secret(), msg, hashlib.sha256).hexdigest()[:32]


def token_for(rx: dict) -> str:
    return f"{rx['id']}.{_mac(rx)}"


def rx_from_token(token) -> dict | None:
    """The prescription row for a valid token (any status), else None."""
    if not isinstance(token, str) or not 3 <= len(token) <= 80 or token.count(".") != 1:
        return None
    left, mac = token.split(".")
    if not left.isdigit() or len(left) > 18 or len(mac) != 32:
        return None
    rows = st().select("prescriptions", [("id", "eq", int(left))], limit=1)
    if not rows or rows[0].get("status") not in ISSUED_STATES:
        return None
    return rows[0] if hmac.compare_digest(_mac(rows[0]), mac) else None


def _short_name(name: str) -> str:
    parts = str(name or "").split()
    return (parts[0] + (f" {parts[-1][0].upper()}." if len(parts) > 1 else "")) if parts else ""


def _hospital(hid) -> dict:
    rows = authz.ident().select("hospitals", [("id", "eq", hid)], columns="id,name,city", limit=1)
    return rows[0] if rows else {}


def card_for(rx: dict, patient: dict) -> dict:
    """Everything the patient's pharmacy screen shows."""
    v = get_prescription(rx["id"])
    hosp = _hospital(rx.get("hospital_id"))
    token = token_for(rx)
    return {"token": token, "verify_path": f"/rx.html?t={token}", "state": v["state"],
            "hospital": {"name": hosp.get("name"), "city": hosp.get("city")},
            "doctor": v["doctor"], "issued_on": v["issued_on"],
            "patient": {"name": patient.get("name"), "age": patient.get("age"), "sex": patient.get("sex")},
            "lines": [{**ln, "summary": english_summary(ln)} for ln in v["lines"]],
            "demo": demo_mode(), "notice": DEMO_NOTICE if demo_mode() else None}


def cards_for(pid: int) -> list[dict]:
    patient = core.get_patient_row(pid)
    if not patient:
        return []
    return [card_for(r, patient) for r, _ in _load(pid, (CURRENT,))]


_PUBLIC_LINE_KEYS = ("line_no", "drug_name", "form", "strength", "dose_text", "frequency_code", "slots",
                     "food_timing", "duration_days", "until_stopped", "as_needed", "instructions")


def _public_line(ln: dict) -> dict:
    """A medicine line as the pharmacist sees it: what to dispense and how it is to be used, no ids."""
    return {**{k: ln.get(k) for k in _PUBLIC_LINE_KEYS}, "summary": english_summary(ln)}


def public_check(token) -> dict | None:
    """What a pharmacist may see for a valid token: minimal, no phone, address or ids. A prescription
    that is stopped or replaced says so and shows no medicines."""
    rx = rx_from_token(token)
    if not rx:
        return None
    patient = core.get_patient_row(int(rx["patient_id"])) or {}
    v = get_prescription(rx["id"])
    hosp = _hospital(rx.get("hospital_id"))
    current = v["state"] == "current"
    return {
        "ok": True, "current": current, "state": "current" if current else "no_longer_current",
        "state_text": "Current - issued by the hospital" if current else
        "No longer current - this prescription was stopped or replaced. Ask the patient for the latest one, or contact the hospital.",
        "checked_at": iso(now_local()), "issued_on": v["issued_on"],
        "hospital": {"name": hosp.get("name"), "city": hosp.get("city")},
        "doctor": {"name": v["doctor"]["name"], "reg_no_display": v["doctor"]["reg_no_display"]},
        "patient": {"name": _short_name(patient.get("name")), "age": patient.get("age"),
                    "sex": patient.get("sex")},
        "lines": [_public_line(ln) for ln in v["lines"]] if current else [],
        "demo": demo_mode(),
        "notice": "Compare with the patient's screen. Demo data only." if demo_mode()
        else "Compare with the patient's screen.",
        "_rx_id": rx["id"], "_patient_id": rx["patient_id"], "_hospital_id": rx.get("hospital_id")}
