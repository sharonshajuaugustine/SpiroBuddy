"""Plain words for dates, times and statuses. Times are always India time (config.TZ)."""
from __future__ import annotations

from datetime import date, datetime

from ..config import TZ, parse_dt

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December")

# The states a person sees. The database has no "proposed": see service.state_of().
STATUS_WORDS = {
    "requested": "Requested",
    "proposed": "Alternative proposed",
    "confirmed": "Confirmed",
    "declined": "Declined",
    "cancelled": "Cancelled",
    "attended": "Attended",
    "no_show": "No-show",
}
STATES = tuple(STATUS_WORDS)


def date_words(d: date | datetime) -> str:
    """Thursday, 15 October 2026"""
    return f"{WEEKDAYS[d.weekday()]}, {d.day} {MONTHS[d.month - 1]} {d.year}"


def time_words(dt: datetime) -> str:
    """10:30 AM"""
    dt = dt.astimezone(TZ)
    hour = dt.hour % 12 or 12
    return f"{hour}:{dt.minute:02d} {'AM' if dt.hour < 12 else 'PM'}"


def when_words(value) -> str:
    """Thursday, 15 October 2026, 10:30 AM (an ISO string or a datetime)."""
    dt = value if isinstance(value, datetime) else parse_dt(value)
    dt = dt.astimezone(TZ)
    return f"{date_words(dt)}, {time_words(dt)}"
