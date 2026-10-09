"""Settings, paths and time helpers shared by the backend modules."""
from __future__ import annotations

import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]          # repo root
BACKEND_DIR = ROOT / "backend"
DATA_DIR = Path(os.getenv("SPIROBUDDY_DATA_DIR") or BACKEND_DIR / "data")   # tests point this at a temp folder
WEB_DIR = ROOT / "web"
ML_DIR = ROOT / "ml"
DB_PATH = DATA_DIR / "spirobuddy.db"
LABELLED_CSV = DATA_DIR / "breaths_labelled.csv"

load_dotenv(ROOT / ".env")
# On Render the public address is known automatically (RENDER_EXTERNAL_URL); use it when
# PUBLIC_BASE_URL wasn't set by hand, so Twilio/Sarvam webhooks and voice-note links work.
if not (os.getenv("PUBLIC_BASE_URL") or "").strip() and (os.getenv("RENDER_EXTERNAL_URL") or "").strip():
    os.environ["PUBLIC_BASE_URL"] = os.environ["RENDER_EXTERNAL_URL"].strip()
if str(ROOT) not in sys.path:                        # so `import ml` works
    sys.path.insert(0, str(ROOT))

DATA_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_KEYS = ["peak_ml", "pct_target", "time_to_peak_s", "mean_rise_ml_s",
                "max_rise_ml_s", "hold_s", "smoothness", "duration_s"]
LABELS = ["good", "too_fast", "too_shallow", "no_hold"]
FIRST_SLOT, LAST_SLOT = 8, 21                        # 14 hourly slots 8:00..21:00


def env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def env_flag(name: str, default: str = "0") -> bool:
    return env(name, default).lower() in ("1", "true", "yes", "on")


def demo_mode() -> bool:
    return env_flag("DEMO_MODE", "1")


def _tz():
    name = env("TZ_NAME", "Asia/Kolkata")
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:  # no tz database: India has no DST, so a fixed offset is fine
        return timezone(timedelta(hours=5, minutes=30), "IST")


TZ = _tz()


def now_local() -> datetime:
    return datetime.now(TZ)


def today_str() -> str:
    return now_local().date().isoformat()


def date_str(d: date) -> str:
    return d.isoformat()


def parse_dt(value) -> datetime:
    """Accept ISO strings (with or without offset) or epoch milliseconds; return aware local time."""
    if value is None or value == "":
        return now_local()
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value) / 1000.0, TZ)
    s = str(value).strip()
    if s.isdigit():
        return datetime.fromtimestamp(int(s) / 1000.0, TZ)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return dt.astimezone(TZ)


def iso(dt: datetime) -> str:
    return dt.astimezone(TZ).isoformat(timespec="seconds")
