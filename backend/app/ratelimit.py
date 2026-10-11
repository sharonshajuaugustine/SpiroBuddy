"""Simple in-memory rate limits (docs/REBUILD_PLAN.md §3.9).

One process, no extra service: each (bucket, key) keeps the times of its recent hits. Buckets
in use: "login" (10 per 15 min per IP + email), "signup", "redeem", "patient_session", "ai",
"upload" (30 per hour per IP) and "live" (twin frames). A restart clears every counter.
"""
from __future__ import annotations

import threading
import time

_lock = threading.Lock()
_hits: dict[tuple[str, str], list[float]] = {}


def _recent(bucket: str, key: str, per_seconds: float, now: float) -> list[float]:
    k = (bucket, str(key))
    hits = [t for t in _hits.get(k, ()) if now - t < per_seconds]
    if hits:
        _hits[k] = hits
    else:
        _hits.pop(k, None)
    return hits


def allow(bucket: str, key: str, limit: int, per_seconds: int) -> bool:
    """Count one hit. True while there were fewer than `limit` hits in the last `per_seconds`."""
    now = time.monotonic()
    with _lock:
        hits = _recent(bucket, key, per_seconds, now)
        if len(hits) >= limit:
            return False
        _hits.setdefault((bucket, str(key)), hits).append(now)
        return True


def peek(bucket: str, key: str, limit: int, per_seconds: int) -> bool:
    """Like allow(), but counts nothing: would one more hit still be allowed?"""
    with _lock:
        return len(_recent(bucket, key, per_seconds, time.monotonic())) < limit


def reset(bucket: str | None = None, key: str | None = None) -> None:
    """Forget the counters: everything, one bucket, or one key in a bucket (tests, a good login)."""
    with _lock:
        if bucket is None:
            _hits.clear()
        elif key is None:
            for k in [k for k in _hits if k[0] == bucket]:
                _hits.pop(k, None)
        else:
            _hits.pop((bucket, str(key)), None)
