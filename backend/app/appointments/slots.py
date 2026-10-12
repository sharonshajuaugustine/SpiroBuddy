"""A doctor's weekly hours, leave days and extra sessions, and the time slots they make.

Tables: availability (weekday 0 = Monday, start_time, end_time, slot_minutes, location) and
availability_exceptions (date, kind leave | extra, start_time, end_time).
A doctor with no weekly rows gets the built-in hours: Monday to Saturday, 09:30-13:00, 15-minute
slots, "OPD". All times are India time.
"""
from __future__ import annotations

import re
import threading
from datetime import date, datetime, time, timedelta

from .. import service as core
from ..config import TZ, iso, now_local

MAX_DAYS_AHEAD = 180               # nobody can book further ahead than this
DEFAULT_SLOT_MINUTES = 15
DEFAULT_LOCATION = "OPD"
DEFAULT_WEEKLY = tuple({"weekday": d, "start_time": "09:30", "end_time": "13:00",
                        "slot_minutes": DEFAULT_SLOT_MINUTES, "location": DEFAULT_LOCATION}
                       for d in range(6))
EXCEPTION_KINDS = ("leave", "extra")
MAX_WEEKLY_ROWS = 40
MAX_EXCEPTIONS = 300
MAX_EXCEPTION_DAYS_AHEAD = 400

_HHMM = re.compile(r"^(\d{1,2}):(\d{2})(?::\d{2})?$")
_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_save_lock = threading.Lock()


# ----------------------------------------------------------------------------- small parsers

def parse_hhmm(value) -> str | None:
    """"9:30" or "09:30" -> "09:30"; anything else -> None."""
    if not isinstance(value, str):
        return None
    m = _HHMM.match(value.strip())
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    return f"{h:02d}:{mi:02d}" if h <= 23 and mi <= 59 else None


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def parse_day(value) -> date:
    """"2026-10-15" -> a date. Raises ValueError for anything else."""
    if not isinstance(value, str) or not _DAY.match(value.strip()):
        raise ValueError("Please give the date like 2026-10-15.")
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        raise ValueError("That is not a real date. Please give it like 2026-10-15.")


def now_day() -> date:
    """Today's date in India."""
    return now_local().date()


def at(d: date, minutes: int) -> datetime:
    return datetime.combine(d, time(minutes // 60, minutes % 60), tzinfo=TZ)


# ----------------------------------------------------------------------------- read

def _weekly_view(r: dict) -> dict | None:
    start, end = parse_hhmm(r.get("start_time")), parse_hhmm(r.get("end_time"))
    try:
        weekday, step = int(r.get("weekday")), int(r.get("slot_minutes") or DEFAULT_SLOT_MINUTES)
    except (TypeError, ValueError):
        return None
    if start is None or end is None or not 0 <= weekday <= 6 or step < 1 or end <= start:
        return None
    return {"weekday": weekday, "start_time": start, "end_time": end, "slot_minutes": step,
            "location": r.get("location") or DEFAULT_LOCATION}


def _exception_view(r: dict) -> dict | None:
    day = str(r.get("date") or "")[:10]
    kind = r.get("kind")
    if not _DAY.match(day) or kind not in EXCEPTION_KINDS:
        return None
    out = {"date": day, "kind": kind}
    start, end = parse_hhmm(r.get("start_time")), parse_hhmm(r.get("end_time"))
    if start and end and end > start:
        out["start_time"], out["end_time"] = start, end
    elif kind == "extra":
        return None                 # an extra session without hours is nothing
    return out


def load(doctor_id: int) -> dict:
    """{weekly, exceptions, default}. Exceptions in the past are left out."""
    st = core.store()
    weekly = [v for v in (_weekly_view(r) for r in
                          st.select("availability", [("doctor_id", "eq", doctor_id)])) if v]
    weekly.sort(key=lambda w: (w["weekday"], w["start_time"]))
    default = not weekly
    if default:
        weekly = [dict(w) for w in DEFAULT_WEEKLY]
    today = now_local().date().isoformat()
    exceptions = [v for v in (_exception_view(r) for r in st.select(
        "availability_exceptions", [("doctor_id", "eq", doctor_id)], order="date"))
        if v and v["date"] >= today]
    exceptions.sort(key=lambda e: (e["date"], e.get("start_time", ""), e["kind"]))
    return {"weekly": weekly, "exceptions": exceptions, "default": default}


# ----------------------------------------------------------------------------- write

def clean(body) -> tuple[list[dict], list[dict]]:
    """Check a PUT body. Returns (weekly rows, exception rows) ready to save, or raises
    ValueError with a plain message."""
    if not isinstance(body, dict):
        raise ValueError("Send the hours as {weekly: [...], exceptions: [...]}.")
    weekly_in = body.get("weekly", [])
    exceptions_in = body.get("exceptions", [])
    if weekly_in is None:
        weekly_in = []
    if exceptions_in is None:
        exceptions_in = []
    if not isinstance(weekly_in, list) or not isinstance(exceptions_in, list):
        raise ValueError("weekly and exceptions must be lists.")
    if len(weekly_in) > MAX_WEEKLY_ROWS or len(exceptions_in) > MAX_EXCEPTIONS:
        raise ValueError("That is too many entries.")
    weekly, seen = [], set()
    for w in weekly_in:
        if not isinstance(w, dict):
            raise ValueError("Each weekly entry must have a weekday and hours.")
        wd = w.get("weekday")
        if isinstance(wd, bool) or not isinstance(wd, int) or not 0 <= wd <= 6:
            raise ValueError("The weekday must be a number from 0 (Monday) to 6 (Sunday).")
        start, end = parse_hhmm(w.get("start_time")), parse_hhmm(w.get("end_time"))
        if start is None or end is None:
            raise ValueError("Times must look like 09:30.")
        if end <= start:
            raise ValueError("The finishing time must be after the starting time.")
        step = w.get("slot_minutes", DEFAULT_SLOT_MINUTES)
        if step is None:
            step = DEFAULT_SLOT_MINUTES
        if isinstance(step, bool) or not isinstance(step, int) or not 5 <= step <= 120:
            raise ValueError("A visit slot must be between 5 and 120 minutes.")
        if step > to_minutes(end) - to_minutes(start):
            raise ValueError("A visit slot is longer than the working hours.")
        loc = w.get("location")
        if loc is not None and not isinstance(loc, str):
            raise ValueError("The place must be text.")
        loc = " ".join((loc or "").split())[:60] or DEFAULT_LOCATION
        key = (wd, start, end)
        if key in seen:
            continue
        seen.add(key)
        weekly.append({"weekday": wd, "start_time": start, "end_time": end,
                       "slot_minutes": step, "location": loc})
    today = now_local().date()
    last = today + timedelta(days=MAX_EXCEPTION_DAYS_AHEAD)
    exceptions, seen = [], set()
    for e in exceptions_in:
        if not isinstance(e, dict):
            raise ValueError("Each leave or extra entry must have a date and a kind.")
        day = parse_day(e.get("date"))
        kind = e.get("kind")
        if kind not in EXCEPTION_KINDS:
            raise ValueError("The kind must be leave or extra.")
        start_raw, end_raw = e.get("start_time"), e.get("end_time")
        start = end = None
        if start_raw not in (None, "") or end_raw not in (None, ""):
            start, end = parse_hhmm(start_raw), parse_hhmm(end_raw)
            if start is None or end is None:
                raise ValueError("Times must look like 09:30, and both are needed.")
            if end <= start:
                raise ValueError("The finishing time must be after the starting time.")
        elif kind == "extra":
            raise ValueError("An extra session needs a start and finish time.")
        if day > last:
            raise ValueError("Leave and extra days can be set up to 400 days ahead.")
        if day < today:
            continue                       # the past is not kept
        key = (day, kind, start, end)
        if key in seen:
            continue
        seen.add(key)
        exceptions.append({"date": day.isoformat(), "kind": kind, "start_time": start,
                           "end_time": end})
    return weekly, exceptions


def save(doctor_id: int, hospital_id: int, body) -> None:
    """Replace the doctor's hours. The new rows go in first, then the old ones go, so a reader
    never sees an empty week in between."""
    weekly, exceptions = clean(body)
    st = core.store()
    now = iso(now_local())
    with _save_lock:
        old_w = [r["id"] for r in st.select("availability", [("doctor_id", "eq", doctor_id)],
                                            columns="id")]
        old_e = [r["id"] for r in st.select("availability_exceptions",
                                            [("doctor_id", "eq", doctor_id)], columns="id")]
        if weekly:
            st.insert("availability", [{"hospital_id": hospital_id, "doctor_id": doctor_id,
                                        "created_at": now, **w} for w in weekly])
        if exceptions:
            st.insert("availability_exceptions", [{"hospital_id": hospital_id,
                                                   "doctor_id": doctor_id, "created_at": now, **e}
                                                  for e in exceptions])
        if old_w:
            st.delete("availability", [("id", "in", old_w)])
        if old_e:
            st.delete("availability_exceptions", [("id", "in", old_e)])


# ----------------------------------------------------------------------------- slots

def _windows(av: dict, d: date) -> tuple[list[tuple], list[tuple | None]]:
    """(working windows, leave windows) for one day, in minutes. A leave of None = all day."""
    ds, wd = d.isoformat(), d.weekday()
    windows = [(to_minutes(w["start_time"]), to_minutes(w["end_time"]), w["slot_minutes"],
                w["location"]) for w in av["weekly"] if w["weekday"] == wd]
    step = av["weekly"][0]["slot_minutes"] if av["weekly"] else DEFAULT_SLOT_MINUTES
    loc = av["weekly"][0]["location"] if av["weekly"] else DEFAULT_LOCATION
    leaves: list[tuple | None] = []
    for e in av["exceptions"]:
        if e["date"] != ds:
            continue
        has_hours = "start_time" in e
        if e["kind"] == "extra" and has_hours:
            windows.append((to_minutes(e["start_time"]), to_minutes(e["end_time"]), step, loc))
        elif e["kind"] == "leave":
            leaves.append((to_minutes(e["start_time"]), to_minutes(e["end_time"]))
                          if has_hours else None)
    return windows, leaves


def offered(av: dict, d: date, now: datetime | None = None) -> list[dict]:
    """The doctor's slots on that day that are still in the future and within 180 days, before
    any booking is taken off: [{start, end, location}] with datetimes, soonest first."""
    now = now or now_local()
    windows, leaves = _windows(av, d)
    if None in leaves:
        return []
    out: dict[datetime, dict] = {}
    horizon = now + timedelta(days=MAX_DAYS_AHEAD)
    for start_m, end_m, step, loc in windows:
        t = start_m
        while t + step <= end_m:
            if not any(t < le and t + step > ls for ls, le in leaves):
                start = at(d, t)
                if now < start <= horizon and start not in out:
                    out[start] = {"start": start, "end": start + timedelta(minutes=step),
                                  "location": loc}
            t += step
    return [out[k] for k in sorted(out)]


def length_and_place(av: dict, start: datetime) -> tuple[int, str]:
    """How long a visit starting at this time is, and where: from the working window it falls
    in; 15 minutes at the OPD when it is outside every window (staff booked a special time)."""
    start = start.astimezone(TZ)
    minute = start.hour * 60 + start.minute
    windows, _ = _windows(av, start.date())
    for s, e, step, loc in windows:
        if s <= minute < e:
            return step, loc
    return DEFAULT_SLOT_MINUTES, DEFAULT_LOCATION
