"""Turn what a doctor types into a clear schedule. Pure functions, no database, no AI.

The rule: a line is scheduled only when its frequency is understood (and it is not "only when
needed"). Anything else is marked unclear and gets NO reminder - the patient still sees the line
exactly as the doctor wrote it. Nothing is ever guessed.

Times come from the patient's routine (breakfast / lunch / dinner / bed) or these defaults:
morning 08:00, afternoon 14:00, night 21:00 (India time).
"""
from __future__ import annotations

import re

DEFAULT_TIMES = {"morning": "08:00", "afternoon": "14:00", "night": "21:00"}
BEDTIME_DEFAULT = "22:00"
FOUR_TIMES = ["08:00", "12:00", "16:00", "20:00"]
SLOTS = ("morning", "afternoon", "night")
_ROUTINE_KEY = {"morning": "breakfast", "afternoon": "lunch", "night": "dinner"}

_HHMM = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")


def clean_hhmm(value) -> str | None:
    """'8:05' -> '08:05'; anything that is not a clock time -> None."""
    m = _HHMM.match(str(value or "").strip())
    return f"{int(m.group(1)):02d}:{m.group(2)}" if m else None


def slot_times(routine) -> dict:
    """{'morning': 'HH:MM', 'afternoon': ..., 'night': ..., 'bedtime': ...} from the patient's
    routine where it has a valid value, else the defaults."""
    routine = routine if isinstance(routine, dict) else {}
    out = {s: clean_hhmm(routine.get(_ROUTINE_KEY[s])) or DEFAULT_TIMES[s] for s in SLOTS}
    out["bedtime"] = clean_hhmm(routine.get("bed")) or BEDTIME_DEFAULT
    return out


def _clean(text) -> str:
    s = str(text or "").lower().replace("–", "-").replace("—", "-")
    s = s.replace(".", "")                    # "T.D.S." -> "tds"
    s = re.sub(r"[,;:()]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


_AS_NEEDED = {"sos", "prn", "if needed", "as needed", "when needed", "only when needed",
              "if required", "as required", "when required", "only if needed", "only if required",
              "as and when needed", "if necessary"}
_STAT = {"stat", "immediately", "at once"}
_WORDS = {   # words -> the 3-digit morning-afternoon-night code (or 'HS' / 'QID')
    "od": "1-0-0", "qd": "1-0-0", "once daily": "1-0-0", "once a day": "1-0-0", "daily": "1-0-0",
    "morning": "1-0-0", "in the morning": "1-0-0", "every morning": "1-0-0",
    "bd": "1-0-1", "bid": "1-0-1", "twice daily": "1-0-1", "twice a day": "1-0-1",
    "tds": "1-1-1", "tid": "1-1-1", "thrice daily": "1-1-1", "three times daily": "1-1-1",
    "three times a day": "1-1-1",
    "qid": "QID", "qds": "QID", "four times daily": "QID", "four times a day": "QID",
    "hs": "HS", "bedtime": "HS", "at bedtime": "HS", "nocte": "HS",
    "night": "0-0-1", "at night": "0-0-1", "every night": "0-0-1",
    "afternoon": "0-1-0", "in the afternoon": "0-1-0",
}
_DIGITS = re.compile(r"^([01]) ?- ?([01]) ?- ?([01])(?: ?- ?([01]))?$")


def _result(code, times, slots, kind, reason=None) -> dict:
    return {"code": code, "times": times, "slots": slots, "kind": kind,
            "as_needed": kind == "as_needed", "unclear": kind in ("unclear", "stat"),
            "reason": reason}


def from_slots(slots, routine=None) -> dict:
    """Explicit Morning / Afternoon / Night choices (the doctor's chips)."""
    chosen = [s for s in SLOTS if s in set(slots or [])]
    bad = [s for s in (slots or []) if s not in SLOTS]
    if bad or not chosen:
        return _result(None, [], [], "unclear", "choose morning, afternoon and/or night")
    t = slot_times(routine)
    times = sorted({t[s] for s in chosen})
    return _result("-".join("1" if s in chosen else "0" for s in SLOTS), times, chosen, "scheduled")


def from_times(times) -> dict:
    """Exact clock times typed by the doctor, e.g. ['08:00', '20:30']."""
    if not isinstance(times, (list, tuple)) or not times or len(times) > 6:
        return _result(None, [], [], "unclear", "give between 1 and 6 clock times")
    clean = [clean_hhmm(x) for x in times]
    if None in clean:
        return _result(None, [], [], "unclear", "a clock time is not valid (use HH:MM)")
    return _result("custom", sorted(set(clean)), [], "scheduled")


def normalise_frequency(text, routine=None) -> dict:
    """Dose notation -> {code, times, slots, kind, as_needed, unclear, reason}.
    kind: 'scheduled' | 'as_needed' | 'stat' | 'unclear'."""
    s = _clean(text)
    if not s:
        return _result(None, [], [], "unclear", "no frequency given")
    if s in _AS_NEEDED:
        return _result("SOS", [], [], "as_needed")
    if s in _STAT:
        return _result("STAT", [], [], "stat", "STAT: ask the clinician - no reminder is set")
    t = slot_times(routine)
    m = _DIGITS.match(s)
    if m:
        code = "-".join(g for g in m.groups() if g is not None)
    else:
        code = _WORDS.get(s)
    if code is None:
        return _result(None, [], [], "unclear", "frequency not recognised")
    if code == "HS":
        return _result("HS", [t["bedtime"]], ["bedtime"], "scheduled")
    if code in ("QID", "1-1-1-1"):
        return _result("QID", list(FOUR_TIMES), [], "scheduled")
    parts = code.split("-")
    if len(parts) == 4:                       # 4-part codes other than 1-1-1-1 are not a known notation
        return _result(None, [], [], "unclear", "frequency not recognised")
    chosen = [s_ for s_, d in zip(SLOTS, parts) if d == "1"]
    if not chosen:                            # 0-0-0
        return _result(None, [], [], "unclear", "frequency not recognised")
    return _result(code, sorted({t[x] for x in chosen}), chosen, "scheduled")


# ---------------------------------------------------------------------------- food and duration

_FOOD = {
    "before_food": {"before food", "before meals", "before meal", "before eating", "ac",
                    "before_food", "before"},
    "after_food": {"after food", "after meals", "after meal", "after eating", "pc", "after_food",
                   "after"},
    "with_food": {"with food", "with meals", "with meal", "with_food", "with"},
    "any": {"", "any", "any time", "anytime", "no food rule", "any_food"},
}


def normalise_food(text) -> tuple[str, bool]:
    """-> (value, understood). value is before_food | after_food | with_food | any."""
    s = _clean(text).replace("_", " ")
    for key, words in _FOOD.items():
        if s in {w.replace("_", " ") for w in words}:
            return key, True
    return "any", False


def normalise_duration(days, until_stopped) -> tuple[int | None, bool, bool]:
    """-> (duration_days, until_stopped, understood). Days 1..365, or 'until stopped'."""
    if until_stopped:
        return None, True, True
    if days in (None, ""):
        return None, False, False
    try:
        if isinstance(days, bool):
            raise ValueError
        n = int(float(str(days).strip()))
        if float(str(days).strip()) != n:
            raise ValueError
    except (TypeError, ValueError):
        return None, False, False
    if not 1 <= n <= 365:
        return None, False, False
    return n, False, True


_FRACTIONS = {"½": 0.5, "¼": 0.25, "¾": 0.75}


def parse_qty(value) -> float | None:
    """'1', 1.5, '1/2', '1 1/2', '½' -> a number between 0 (exclusive) and 100."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        q = float(value)
    else:
        s = str(value).strip()
        try:
            q = None
            for ch, v in _FRACTIONS.items():
                if s.endswith(ch):
                    head = s[:-1].strip()
                    q = (float(head) if head else 0.0) + v
                    break
            if q is None:
                m = re.match(r"^(?:(\d+)\s+)?(\d+)\s*/\s*(\d+)$", s)
                if m:
                    q = float(m.group(1) or 0) + int(m.group(2)) / int(m.group(3))
                else:
                    q = float(s)
        except (ValueError, ZeroDivisionError):
            return None
    return round(q, 3) if 0 < q <= 100 else None


def qty_text(q) -> str:
    """0.5 -> '½', 1.5 -> '1½', 2 -> '2'."""
    try:
        q = float(q)
    except (TypeError, ValueError):
        return ""
    whole, frac = int(q), round(q - int(q), 3)
    sym = {0.5: "½", 0.25: "¼", 0.75: "¾"}.get(frac)
    if frac == 0:
        return str(whole)
    if sym:
        return (str(whole) if whole else "") + sym
    return f"{q:g}"
