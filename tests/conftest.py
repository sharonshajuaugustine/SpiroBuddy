"""Shared test setup: a FastAPI TestClient on a throw-away data folder, demo mode, no keys."""
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Must be set before backend.app is imported: config reads them at import time,
# and load_dotenv() never overrides a variable that already exists (even if empty).
_TMP = tempfile.mkdtemp(prefix="spirobuddy-test-")
os.environ.update({
    "SPIROBUDDY_DATA_DIR": _TMP,
    "DEMO_MODE": "1",
    "DATA_BACKEND": "demo",
    "DEMO_AUTOPILOT": "0",
})
for key in ("ANTHROPIC_API_KEY", "SARVAM_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN",
            "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "EXOTEL_API_KEY", "EXOTEL_API_TOKEN",
            "SARVAM_AGENT_ID"):
    os.environ[key] = ""


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from backend.app.main import app
    with TestClient(app) as c:
        yield c
    shutil.rmtree(_TMP, ignore_errors=True)


@pytest.fixture()
def fresh(client):
    """Reset the demo data before a test that changes it."""
    assert client.post("/api/demo/reset").status_code == 200
    return client
