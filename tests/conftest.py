"""Shared test setup: a FastAPI TestClient on a throw-away data folder, demo mode, no keys.

SpiroBuddy 2.0 puts every API call behind a login and the X-SB header, so:
- `client` (session-wide) is logged in as the demo admin, admin@demo-general.example;
- every other TestClient a test builds (the `raw` fixture in test_critical.py, and the fresh
  server process one test starts) also starts as the demo admin with the X-SB header;
- `anon` is a client with no login, `login_as(email)` gives a new client logged in as that
  demo account, `patient_client(pid)` one with a patient-app session;
- the second hospital's patient (id 100) is left out of the old suite, which counts exactly
  7 demo patients; the `riverside_patient` fixture adds it for a test and removes it again.
"""
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ADMIN_EMAIL, ADMIN_PASSWORD = "admin@demo-general.example", "demo-admin-2026"

# Must be set before backend.app is imported: config reads them at import time,
# and load_dotenv() never overrides a variable that already exists (even if empty).
_TMP = tempfile.mkdtemp(prefix="spirobuddy-test-")
os.environ.update({
    "SPIROBUDDY_DATA_DIR": _TMP,
    "DEMO_MODE": "1",
    "DATA_BACKEND": "demo",
    "DEMO_AUTOPILOT": "0",
    "ALLOW_TRAINING": "1",          # the old tests use /api/collect and /api/train (as the admin)
    "SHOW_API_DOCS": "0",
})
for key in ("ANTHROPIC_API_KEY", "SARVAM_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN",
            "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "EXOTEL_API_KEY", "EXOTEL_API_TOKEN",
            "SARVAM_AGENT_ID", "GEMINI_API_KEY"):
    os.environ[key] = ""

# A test that starts a whole new server process (test_critical.py) can't use the fixtures
# below. This file is put on PYTHONPATH for child processes only: there, a TestClient logs in
# as the demo admin as soon as the app has started.
_SITE = Path(_TMP) / "child-site"
_SITE.mkdir()
(_SITE / "sitecustomize.py").write_text(
    "import os\n"
    "if os.environ.get('SB_TEST_AUTOLOGIN'):\n"
    "    try:\n"
    "        from starlette.testclient import TestClient as _TC\n"
    "        _enter = _TC.__enter__\n"
    "        def _login(self):\n"
    "            out = _enter(self)\n"
    "            try:\n"
    "                self.headers['X-SB'] = '1'\n"
    "                email, _, password = os.environ['SB_TEST_AUTOLOGIN'].partition('|')\n"
    "                self.post('/api/auth/login', json={'email': email, 'password': password})\n"
    "            except Exception:\n"
    "                pass\n"
    "            return out\n"
    "        _TC.__enter__ = _login\n"
    "    except Exception:\n"
    "        pass\n", encoding="utf-8")
os.environ["SB_TEST_AUTOLOGIN"] = f"{ADMIN_EMAIL}|{ADMIN_PASSWORD}"
os.environ["PYTHONPATH"] = os.pathsep.join(
    [str(_SITE)] + [p for p in os.environ.get("PYTHONPATH", "").split(os.pathsep) if p])

_admin = {"token": None}        # the demo admin's session cookie, once `client` has logged in


def _patch_testclient() -> None:
    """Every TestClient made after `client` starts with the X-SB header and the admin session."""
    from starlette.testclient import TestClient
    if getattr(TestClient, "_sb_patched", False):
        return
    plain_init = TestClient.__init__

    def init(self, *args, **kwargs):
        plain_init(self, *args, **kwargs)
        self.headers.setdefault("X-SB", "1")
        if _admin["token"]:
            self.cookies.set("sb_staff", _admin["token"])

    TestClient.__init__ = init
    TestClient._sb_patched = True


def _new_client(**kwargs):
    """A separate client with its own (empty) cookie jar."""
    from fastapi.testclient import TestClient
    from backend.app.main import app
    c = TestClient(app, headers={"X-SB": "1"}, **kwargs)
    c.cookies.clear()
    return c


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from backend.app import seed_auth
    from backend.app.main import app
    seed_auth.SEED_RIVERSIDE_PATIENT = False     # the old suite counts exactly 7 demo patients
    _patch_testclient()
    with TestClient(app, headers={"X-SB": "1"}) as c:
        r = c.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert r.status_code == 200, r.text
        _admin["token"] = c.cookies.get("sb_staff")
        assert _admin["token"]
        yield c
    shutil.rmtree(_TMP, ignore_errors=True)


@pytest.fixture()
def fresh(client):
    """Reset the demo data before a test that changes it (the admin stays logged in)."""
    assert client.post("/api/demo/reset").status_code == 200
    return client


@pytest.fixture()
def anon(client):
    """A client that is not logged in (it still sends the X-SB header)."""
    return _new_client()


@pytest.fixture()
def login_as(client):
    """login_as(email) -> a NEW client, logged in as that demo account (own cookies)."""
    from backend.app import ratelimit, seed_auth

    def make(email: str, password: str | None = None):
        ratelimit.reset("login")
        c = _new_client()
        r = c.post("/api/auth/login", json={"email": email,
                                            "password": password or seed_auth.DEMO_PASSWORDS[email]})
        assert r.status_code == 200, r.text
        return c
    return make


@pytest.fixture()
def patient_client(client):
    """patient_client(pid) -> a NEW client with a patient-app session (DEMO_MODE id shortcut)."""
    def make(pid: int):
        c = _new_client()
        r = c.post("/api/me/session", json={"patient_id": pid})
        assert r.status_code == 200, r.text
        return c
    return make


@pytest.fixture()
def riverside_patient(client):
    """Patient 100 at the second hospital exists during this test (also across demo resets)."""
    from backend.app import seed_auth, service
    seed_auth.SEED_RIVERSIDE_PATIENT = True
    seed_auth.ensure_riverside_patient(service.store())
    yield seed_auth.RIVERSIDE_PATIENT_ID
    seed_auth.SEED_RIVERSIDE_PATIENT = False
    seed_auth.remove_riverside_patient(service.store())
