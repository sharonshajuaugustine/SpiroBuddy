"""Critical tests: attempts to break SpiroBuddy (security, safety, failures, load).

Plain-English results: docs/CRITICAL_TEST_REPORT.md. Same rules as the other tests: no network,
no keys, no hardware, fake patients only, throw-away data folder (tests/conftest.py).

- Tests marked `xfail` are KNOWN OPEN problems that were too big for a small safe fix. They are
  `strict`: the day somebody fixes one, the test turns red and says "remove the mark".
- A demo reset takes about 4 seconds, so only tests that need the seeded data untouched ask for
  `fresh`; the others work on whatever state they find (`raw`).
- Every test runs with real network connections blocked (see `_hermetic`).
"""
import json
import os
import re
import socket
import statistics
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

# No background ticker or clock-driven auto-ladders during tests: every step is driven explicitly.
os.environ["COMMS_TICKER"] = "0"
os.environ["COMMS_AUTO_ESCALATE"] = "0"

C = "/api/comms"
ROOT = Path(__file__).resolve().parents[1]
DEMO_TOKEN = "ravi-amit-demo"                      # seeded demo guardian link (patient 1)
PUBLIC = "https://spirobuddy.example.com"
PATIENT_PHONE = "+919800000002"                    # made-up number used as "the demo patient's phone"
LOCAL = (None, "", "localhost", "127.0.0.1", "::1", "0.0.0.0")
# Settings a developer's own .env may fill in (conftest.py only blanks the secret keys). A test
# that needs one sets it itself.
BLANK_ENV = ["TWILIO_WHATSAPP_FROM", "TWILIO_VOICE_FROM", "TWILIO_MESSAGING_SERVICE_SID", "TWILIO_CONTENT_SID_REMINDER",
             "TWILIO_CONTENT_SID_GUARDIAN", "DEMO_FAMILY_WHATSAPP", "DEMO_NURSE_WHATSAPP", "DEMO_PATIENT_PHONE",
             "DEMO_GUARDIAN_PHONE", "DEMO_NURSE_PHONE", "NURSE_DESK_PHONE", "PUBLIC_BASE_URL", "SARVAM_WEBHOOK_SECRET",
             "SARVAM_AGENT_API_KEY", "SARVAM_ORG_ID", "SARVAM_WORKSPACE_ID", "SARVAM_CONNECTION_ID", "SARVAM_AGENT_NUMBER",
             "CALL_PROVIDER", "EXOTEL_SID", "EXOTEL_CALLER_ID", "EXOTEL_APP_ID", "QUIET_HOURS", "TWILIO_VALIDATE"]


# ----------------------------------------------------------------------------- fixtures & helpers

@pytest.fixture(autouse=True)
def _hermetic(monkeypatch):
    """No test in this file may touch the internet: outside connections are refused and counted,
    and the test fails if the app even tried (the app would otherwise hide it behind a fallback)."""
    for k in BLANK_ENV:
        monkeypatch.setenv(k, "")
    attempts = []
    real_connect, real_lookup = socket.socket.connect, socket.getaddrinfo

    def connect(self, address, *a, **k):
        host = address[0] if isinstance(address, tuple) else address
        if isinstance(host, bytes):
            host = host.decode("ascii", "replace")
        if host not in LOCAL:
            attempts.append(f"connect {address}")
            raise OSError(f"blocked by tests/test_critical.py: real network call to {address}")
        return real_connect(self, address, *a, **k)

    def lookup(host, *a, **k):
        name = host.decode("ascii", "replace") if isinstance(host, bytes) else host
        if name not in LOCAL:
            attempts.append(f"lookup {name}")
            raise socket.gaierror(f"blocked by tests/test_critical.py: real network lookup of {name}")
        return real_lookup(host, *a, **k)

    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket, "getaddrinfo", lookup)
    yield
    assert not attempts, f"the app tried to reach the internet during this test: {attempts[:5]}"


@pytest.fixture(scope="module", autouse=True)
def _leave_the_demo_data_clean(client):
    yield
    assert client.post("/api/demo/reset").status_code == 200


@pytest.fixture()
def raw(client):
    """Same app as `client`, but a server crash comes back as HTTP 500 instead of raising inside
    the test, so "never a 500" can be asserted. Does NOT reset the demo data."""
    from fastapi.testclient import TestClient
    from backend.app.main import app
    return TestClient(app, raise_server_exceptions=False)


def _st():
    from backend.app.comms.common import st
    return st()


def _out(pid, to_role, number=None):
    """Automated messages logged for this person (the short reply to a message they just sent
    themselves is not counted)."""
    rows = _st().select("messages", [("patient_id", "eq", pid), ("to_role", "eq", to_role)], order="id")
    rows = [m for m in rows if m.get("kind") != "reply"]
    if number is not None:
        rows = [m for m in rows if m.get("to_number") == number]
    return rows


def _calls_to(pid, role, guardian_id=None):
    rows = _st().select("calls", [("patient_id", "eq", pid), ("to_role", "eq", role)])
    if guardian_id is not None:
        rows = [c for c in rows if c.get("guardian_id") == guardian_id]
    return rows


def _snapshot(pid=1, counts=True):
    """Everything a forged webhook could change for one patient."""
    s = _st()
    snap = {"care": s.select("care_settings", [("patient_id", "eq", pid)]),
            "guardians": s.select("guardians", [("patient_id", "eq", pid)], order="id"),
            "alerts": s.select("alerts", [("patient_id", "eq", pid)], order="id"),
            "calls": s.select("calls", [("patient_id", "eq", pid)], order="id"),
            "runs": [(r["id"], r["status"]) for r in s.select("escalations", [("patient_id", "eq", pid)], order="id")]}
    if counts:
        snap.update(inbound=s.count("inbound_messages"), messages=s.count("messages"))
    return snap


def _age_consent(days, pid=1, guardian_id=None):
    from backend.app.comms import guardians
    from backend.app.config import iso, now_local
    when = iso(now_local() - timedelta(days=days))
    if guardian_id is not None:
        _st().update("guardians", [("id", "eq", guardian_id)], {"consent": True, "consent_at": when})
        return
    cfg = guardians.get_settings(pid)
    cfg["consent"], cfg["consent_at"] = True, when
    _st().upsert("care_settings", [{"patient_id": pid, "config": cfg, "updated_at": iso(now_local())}])


def _run_whole_ladder(client, pid=1):
    """Fast-forward ladder with quiet hours ignored, every step run now."""
    r = client.post(f"{C}/demo/ladder/{pid}", json={"override_quiet": True})
    assert r.status_code == 200, r.text
    rid = r.json()["id"]
    for _ in range(6):
        assert client.post(f"{C}/escalations/{rid}/advance").status_code == 200
    return rid


def _ringing_patient_call(client, pid=1):
    rid = client.post(f"{C}/demo/ladder/{pid}", json={"override_quiet": True}).json()["id"]
    for _ in range(2):
        client.post(f"{C}/escalations/{rid}/advance")
    calls = [c for c in client.get(f"{C}/calls?patient_id={pid}&active=1").json() if c["to_role"] == "patient"]
    assert calls, "no reminder call is ringing (does this patient still have consent?)"
    return calls[0]


def _sample(name):
    data = json.loads((ROOT / "backend/app/comms/samples/sarvam_webhooks.json").read_text(encoding="utf-8"))
    return json.loads(json.dumps(data["samples"][name]["payload"]))


def _sarvam_env(monkeypatch, secret="s3cret"):
    for k, v in {"SARVAM_AGENT_API_KEY": "test-key", "SARVAM_ORG_ID": "org1", "SARVAM_WORKSPACE_ID": "ws1",
                 "SARVAM_AGENT_ID": "app1", "SARVAM_CONNECTION_ID": "conn1",
                 "SARVAM_AGENT_NUMBER": "+918045550000", "PUBLIC_BASE_URL": PUBLIC,
                 "SARVAM_WEBHOOK_SECRET": secret, "DEMO_PATIENT_PHONE": PATIENT_PHONE,
                 "CALL_PROVIDER": "auto"}.items():
        monkeypatch.setenv(k, v)


def _twilio_env(monkeypatch, token="twilio-test-token", base=PUBLIC):
    """Twilio webhook checking on (auth token + public address). WhatsApp sending stays off."""
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", token)
    monkeypatch.setenv("PUBLIC_BASE_URL", base)
    monkeypatch.setenv("DEMO_PATIENT_PHONE", PATIENT_PHONE)


def _twilio_voice_env(monkeypatch):
    """Real Twilio phone calls 'possible' (the dial itself is always faked by the test).
    TWILIO_WHATSAPP_FROM stays empty, so no WhatsApp is attempted."""
    for k, v in {"TWILIO_ACCOUNT_SID": "ACtest", "TWILIO_AUTH_TOKEN": "tok", "TWILIO_VOICE_FROM": "+15005550006",
                 "PUBLIC_BASE_URL": PUBLIC, "CALL_PROVIDER": "twilio", "DEMO_PATIENT_PHONE": PATIENT_PHONE,
                 "DEMO_GUARDIAN_PHONE": "+919800000003", "TWILIO_WHATSAPP_FROM": ""}.items():
        monkeypatch.setenv(k, v)


def _twilio_sig(token, path, form):
    from twilio.request_validator import RequestValidator
    return RequestValidator(token).compute_signature(PUBLIC + path, form)


class _FakeClaude:
    """Stands in for anthropic.Anthropic: counts calls and plays a scripted behaviour."""
    calls = []
    behaviour = None

    def __init__(self, **kw):
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kw):
        type(self).calls.append(kw)
        return type(self).behaviour(kw)


def _claude(monkeypatch, behaviour):
    import anthropic
    _FakeClaude.calls, _FakeClaude.behaviour = [], staticmethod(behaviour)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake-key-for-tests")
    monkeypatch.setattr(anthropic, "Anthropic", _FakeClaude)
    return _FakeClaude


def _says(text, stop="end_turn"):
    return lambda kw: SimpleNamespace(stop_reason=stop, content=[SimpleNamespace(type="text", text=text)])


def _boom(exc):
    def f(*a, **kw):
        raise exc
    return f


# ============================================================================= 1. SECURITY

# ----- guardian (family) links

def test_new_guardian_tokens_are_long_random_and_unique(raw):
    made = [raw.post(f"{C}/guardians", json={"patient_id": 2, "name": f"Test Guardian {i}",
                                             "language": "en"}).json() for i in range(40)]
    try:
        tokens = [g["token"] for g in made]
        assert len(set(tokens)) == 40
        for g in made:
            t = g["token"]
            assert len(t) >= 20, f"token too short to be unguessable: {t!r}"    # was 12 characters before the fix
            assert re.fullmatch(r"[A-Za-z0-9_-]+", t)
            assert str(g["id"]) != t and not t.isdigit()                        # not an id, not a counter
        assert len({t[:4] for t in tokens}) > 30 and len({t[-4:] for t in tokens}) > 30   # no fixed start/end
    finally:
        for g in made:
            raw.delete(f"{C}/guardians/{g['id']}")


@pytest.mark.parametrize("token", [
    "x", "1", "0", "-1", "999999", "null", "None", "undefined", "ravi-amit-dem", "ravi-amit-demo2",
    "RAVI-AMIT-DEMO", "ravi_amit_demo", "%", "*", "_", "' OR '1'='1", "ravi-amit-demo'--", "a" * 64,
    "a" * 5000, "%00", "../ravi-amit-demo", "ravi-amit-demo%00"])
def test_wrong_guardian_token_gets_404_and_no_data(raw, token):
    for method, path in (("GET", ""), ("POST", "/cheer"), ("POST", "/call-log"), ("PUT", "/quiet")):
        body = {"quiet_start": "20:00", "quiet_end": "08:00"} if method == "PUT" else {} if method == "POST" else None
        r = raw.request(method, f"{C}/guardian/{token}{path}", json=body)
        assert r.status_code in (404, 405), f"{method} {path}: {r.status_code} {r.text[:200]}"
        assert "Ravi" not in r.text and "Kumar" not in r.text and "+91" not in r.text


def test_guardian_link_opens_only_its_own_patient_and_a_new_link_kills_the_old_one(fresh):
    r = fresh.get(f"{C}/guardian/{DEMO_TOKEN}")
    assert r.status_code == 200
    body = r.text
    others = [p["name"] for p in fresh.get("/api/patients").json() if p["id"] != 1]
    assert others and not any(n in body or n.split()[0] in body for n in others)
    assert r.json()["patient"]["first_name"] == "Ravi"
    assert "token" not in body and "surgery" not in body      # nothing more than the family needs
    # a link for patient 2's guardian opens patient 2, never patient 1
    g2 = fresh.get(f"{C}/care/2").json()["guardians"][0]
    d2 = fresh.get(f"{C}/guardian/{g2['token']}").json()
    assert d2["patient"]["first_name"] != "Ravi" and d2["guardian"]["id"] == g2["id"]
    # a cheer sent with patient 2's link lands with patient 2 only
    before = len(fresh.get(f"{C}/cheers/1").json())
    assert fresh.post(f"{C}/guardian/{g2['token']}/cheer", json={"preset": 0}).status_code == 200
    assert len(fresh.get(f"{C}/cheers/1").json()) == before
    assert fresh.get(f"{C}/cheers/2").json()[0]["guardian_id"] == g2["id"]
    # "new link" makes the old one useless; removing the guardian kills the new one too
    g = fresh.get(f"{C}/care/1").json()["guardians"][0]
    assert g["token"] == DEMO_TOKEN
    new = fresh.put(f"{C}/guardians/{g['id']}", json={"new_link": True}).json()
    assert new["token"] != DEMO_TOKEN and len(new["token"]) >= 20
    assert fresh.get(f"{C}/guardian/{DEMO_TOKEN}").status_code == 404
    assert fresh.get(f"{C}/guardian/{new['token']}").status_code == 200
    assert fresh.delete(f"{C}/guardians/{g['id']}").status_code == 200
    assert fresh.get(f"{C}/guardian/{new['token']}").status_code == 404


def test_guardian_tokens_are_not_listed_where_they_are_not_needed(fresh):
    tokens = [g["token"] for pid in (1, 2, 3) for g in fresh.get(f"{C}/care/{pid}").json()["guardians"]]
    assert len(tokens) >= 6
    _run_whole_ladder(fresh, 1)
    for url in ("/api/patients", "/api/patients/1", "/api/patients/1/sessions", "/api/messages?limit=500",
                "/api/health", f"{C}/status", f"{C}/alerts?status=all", f"{C}/alerts/counts", f"{C}/events?limit=300",
                f"{C}/timeline/1?limit=500", f"{C}/calls?limit=200", f"{C}/escalations", f"{C}/cheers/1",
                f"{C}/trend/1", f"{C}/wa/thread/1?role=guardian", f"{C}/guardian/{DEMO_TOKEN}"):
        r = fresh.get(url)
        assert r.status_code == 200, url
        leaked = [t for t in tokens if t in r.text]
        assert not leaked, f"{url} lists guardian link tokens: {leaked}"


@pytest.mark.xfail(strict=True, reason="OPEN (fix before real patients): the nurse API has no login, so "
                   "GET /api/comms/care/{pid} and /api/comms/patient/{pid} hand every family link token, "
                   "phone number and health detail to anyone who can reach the server "
                   "(backend/app/routes_comms.py care() and patient_comms()). Fine for a fake-patient demo.")
def test_open_nurse_api_needs_a_login_before_real_patients(raw):
    assert raw.get(f"{C}/care/1").status_code in (401, 403)


# ----- webhooks: Sarvam voice agent

SARVAM_JUNK = [
    {}, {"attempt_id": "not-ours"}, {"attempt_id": None}, {"attempt_id": 5}, {"attempt_id": ["x"]},
    {"attempt_id": {"a": 1}}, {"attempt_id": "x" * 100000}, {"webhook_config": "x"}, {"webhook_config": []},
    {"webhook_config": {"metadata": "x"}}, {"webhook_config": {"metadata": {"call_id": "abc"}}},
    {"webhook_config": {"metadata": {"call_id": [1]}}}, {"webhook_config": {"metadata": {"call_id": {"a": 1}}}},
    {"webhook_config": {"metadata": {"call_id": 999999}}}, {"webhook_config": {"metadata": {"call_id": -1}}},
    {"webhook_config": {"metadata": {"call_id": True}}}, {"webhook_config": {"metadata": {"call_id": 1e30}}},
    {"attempt_id": "nope", "status": {"a": 1}, "final_agent_variables": "x", "interaction_transcript": "y"},
]
SARVAM_ODD_BODIES = {
    "form": dict(data={"a": "b"}), "xml": dict(content=b"<a/>", headers={"Content-Type": "application/xml"}),
    "list": dict(json=[1, 2]), "text": dict(content=b"hello", headers={"Content-Type": "text/plain"}),
    "empty": dict(content=b""), "bad_utf8": dict(content=b"\xff\xfe{", headers={"Content-Type": "application/json"}),
    "deep": dict(content=b"[" * 50000 + b"]" * 50000, headers={"Content-Type": "application/json"}),
    "huge": dict(content=json.dumps({"attempt_id": "A" * (3 * 1024 * 1024)}).encode(),
                 headers={"Content-Type": "application/json"}),
}


def test_sarvam_webhook_forged_is_refused_junk_is_4xx_real_one_is_accepted(fresh, raw, monkeypatch):
    from backend.app.comms import sarvam
    _sarvam_env(monkeypatch)
    monkeypatch.setattr(sarvam, "_post", lambda url, body: {"attempt_id": "att-critical-1"})
    call = fresh.post(f"{C}/checkin-call/1").json()
    assert call["provider"] == "sarvam_agent", call
    forged = _sample("red_flag")                           # the most damaging thing to forge
    forged["attempt_id"] = "att-critical-1"
    forged["webhook_config"] = {"metadata": {"call_id": call["id"], "patient_id": 1}}
    before = _snapshot(1)
    # 1) no secret / wrong secret -> 403, nothing changes
    for name, url, headers, body in (
            ("none", "", {}, forged), ("wrong_query", "?token=guess", {}, forged),
            ("wrong_header", "", {"X-Webhook-Token": "guess"}, forged), ("empty", "?token=", {}, forged),
            ("prefix", "?token=s3cre", {}, forged), ("longer", "?token=s3cret1", {}, forged),
            ("case", "?token=S3CRET", {}, forged), ("secret_in_body", "", {}, {**forged, "token": "s3cret"}),
            ("bearer", "", {"Authorization": "Bearer s3cret"}, forged)):
        r = raw.post(f"{C}/webhooks/sarvam{url}", json=body, headers=headers)
        assert r.status_code == 403, f"{name}: {r.status_code} {r.text[:200]}"
        assert _snapshot(1) == before, name
    # 2) right secret but junk -> 4xx, never a crash, nothing changes
    bad = []
    for body in SARVAM_JUNK:
        r = raw.post(f"{C}/webhooks/sarvam?token=s3cret", json=body)
        if not 400 <= r.status_code < 500:
            bad.append((json.dumps(body)[:80], r.status_code, r.text[:120]))
    for name, kw in SARVAM_ODD_BODIES.items():
        r = raw.post(f"{C}/webhooks/sarvam?token=s3cret", **kw)
        if not 400 <= r.status_code < 500:
            bad.append((name, r.status_code, r.text[:120]))
    assert not bad, bad
    assert _snapshot(1) == before
    assert fresh.get(f"{C}/calls/{call['id']}").json()["result"]["pending"] is True
    assert raw.get(f"{C}/webhooks/sarvam").status_code in (404, 405)
    # 3) the real thing (secret in the header or the URL) is accepted once
    payload = _sample("pain")
    payload["attempt_id"] = "att-critical-1"
    r = raw.post(f"{C}/webhooks/sarvam", json=payload, headers={"X-Webhook-Token": "s3cret"})
    assert r.status_code == 200 and r.json()["result"]["outcome"] == "needs_nurse_review"
    again = raw.post(f"{C}/webhooks/sarvam?token=s3cret", json=payload)
    assert again.status_code == 200 and again.json()["duplicate"] is True
    assert fresh.get(f"{C}/calls/{call['id']}").json()["status"] == "completed"
    # 4) outside demo mode, with no secret configured, the webhook is closed
    monkeypatch.setenv("DEMO_MODE", "0")
    monkeypatch.setenv("SARVAM_WEBHOOK_SECRET", "")
    assert raw.post(f"{C}/webhooks/sarvam", json=payload).status_code == 403


# ----- webhooks: Twilio (WhatsApp inbound + voice)

def test_twilio_webhooks_forged_are_refused_and_signed_ones_accepted(fresh, raw, monkeypatch):
    _twilio_env(monkeypatch)
    call = _ringing_patient_call(fresh, 1)
    before = _snapshot(1)
    path = f"{C}/webhooks/whatsapp"
    # 1) WhatsApp: STOP (withdraw consent), red flag, "1" (stop a ladder) without a valid signature
    for text in ("STOP", "chest pain", "1"):
        form = {"From": f"whatsapp:{PATIENT_PHONE}", "Body": text}
        for name, headers in (("no signature", {}), ("empty", {"X-Twilio-Signature": ""}),
                              ("random", {"X-Twilio-Signature": "AAAAAAAAAAAAAAAAAAAAAAAAAAA="}),
                              ("signed with another token", {"X-Twilio-Signature": _twilio_sig("some-other-token", path, form)}),
                              ("signed for another body", {"X-Twilio-Signature": _twilio_sig("twilio-test-token", path, {**form, "Body": "hello"})})):
            r = raw.post(path, data=form, headers=headers)
            assert r.status_code == 403, f"{text} / {name}: {r.status_code} {r.text[:200]}"
    # 2) call webhooks (key press, call status, call start, message status)
    assert raw.post(f"{C}/twilio/gather/{call['id']}", data={"Digits": "1"}).status_code == 403
    assert raw.post(f"{C}/twilio/status/{call['id']}", data={"CallStatus": "completed"}).status_code == 403
    assert raw.post(f"{C}/twilio/voice/{call['id']}", data={}).status_code == 403
    assert raw.post(f"{C}/webhooks/whatsapp/status", data={"MessageStatus": "failed"}).status_code == 403
    assert _snapshot(1) == before
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is True
    # 3) a correctly signed STOP is accepted
    form = {"From": f"whatsapp:{PATIENT_PHONE}", "Body": "STOP"}
    sig = _twilio_sig("twilio-test-token", path, form)
    r = raw.post(path, data=form, headers={"X-Twilio-Signature": sig})
    assert r.status_code == 200 and r.text == "<Response/>"
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is False


@pytest.mark.xfail(strict=True, reason="OPEN (should fix): with TWILIO_AUTH_TOKEN set but PUBLIC_BASE_URL empty "
                   "the Twilio signature is not checked at all (backend/app/routes_comms.py _twilio_form, the "
                   "`if token and public_base()` line). On Render PUBLIC_BASE_URL is filled in automatically, so "
                   "this only bites a local run behind a tunnel. Not fixed: failing closed could break the live "
                   "WhatsApp demo on a laptop.")
def test_twilio_signature_is_checked_even_without_public_base_url(raw, monkeypatch):
    _twilio_env(monkeypatch, base="")
    try:
        r = raw.post(f"{C}/webhooks/whatsapp", data={"From": f"whatsapp:{PATIENT_PHONE}", "Body": "STOP"})
        assert r.status_code == 403
    finally:
        raw.put(f"{C}/care/1", json={"consent": True})         # undo what the forged STOP did


@pytest.mark.xfail(strict=True, reason="OPEN (fix before real patients): GET /api/comms/twilio/voice/{id} skips the "
                   "signature check that the POST form has (backend/app/routes_comms.py twilio_voice, "
                   "`if request.method == 'POST'`), so anyone can mark a ringing call as answered.")
def test_twilio_voice_get_is_also_signature_checked(raw, monkeypatch):
    _twilio_env(monkeypatch)
    call = _ringing_patient_call(raw, 5)
    assert raw.get(f"{C}/twilio/voice/{call['id']}").status_code == 403


@pytest.mark.xfail(strict=True, reason="OPEN (fix before real patients): the Exotel call webhooks have no secret or "
                   "signature at all (backend/app/routes_comms.py exotel_greeting / exotel_gather / exotel_passthru / "
                   "exotel_status). Call ids are small counting numbers, so a stranger can 'press 1' for a "
                   "patient and stop a ladder. Exotel is not used in the demo.")
def test_exotel_webhooks_need_a_secret(raw, monkeypatch):
    monkeypatch.setenv("EXOTEL_API_KEY", "k")
    monkeypatch.setenv("EXOTEL_API_TOKEN", "t")
    call = _ringing_patient_call(raw, 5)
    r = raw.get(f"{C}/exotel/passthru?CustomField={call['id']}&digits=1")
    assert r.status_code == 403
    assert raw.get(f"{C}/escalations?patient_id=5").json()[0]["status"] == "active"


WA_ODD = {
    "json_content_type": dict(content=b'{"From":"whatsapp:+919800000002","Body":"STOP"}', headers={"Content-Type": "application/json"}),
    "plain_text": dict(content=b"STOP", headers={"Content-Type": "text/plain"}),
    "no_body": dict(content=b""),
    "bad_multipart": dict(content=b"garbage", headers={"Content-Type": "multipart/form-data; boundary=x"}),
    "multipart_no_boundary": dict(content=b"garbage", headers={"Content-Type": "multipart/form-data"}),
    "binary": dict(content=b"\xff\xfe\x00\x01", headers={"Content-Type": "application/x-www-form-urlencoded"}),
    "huge_field": dict(data={"From": "whatsapp:+919999999999", "Body": "A" * (3 * 1024 * 1024)}),
    "two_thousand_fields": dict(data={f"k{i}": "v" for i in range(2000)}),
    "unknown_sender": dict(data={"From": "whatsapp:+10000000000", "Body": "STOP"}),
    "unknown_sender_red_flag": dict(data={"From": "whatsapp:+10000000000", "Body": "chest pain"}),
    "no_sender": dict(data={"Body": "chest pain"}),
    "sender_is_script": dict(data={"From": "<script>alert(1)</script>", "Body": "1"}),
    "sender_is_sql": dict(data={"From": "' OR 1=1 --", "Body": "STOP"}),
}


def test_whatsapp_webhook_odd_requests_never_crash_or_touch_a_patient(raw):
    before = {pid: _snapshot(pid, counts=False) for pid in (1, 2, 3)}
    for name, kw in WA_ODD.items():
        for path in ("/webhooks/whatsapp", "/webhooks/whatsapp/status"):
            r = raw.post(f"{C}{path}", **kw)
            assert r.status_code < 500, f"{name} {path}: {r.status_code} {r.text[:200]}"
    assert {pid: _snapshot(pid, counts=False) for pid in (1, 2, 3)} == before     # e.g. nobody lost consent to a stranger's STOP
    stranger = _st().select("inbound_messages", [("from_role", "eq", "unknown")], order="id", desc=True, limit=1)[0]
    assert stranger["patient_id"] is None and "112" in stranger["reply"]            # a stranger is still told about 112


@pytest.mark.parametrize("method,url", [
    ("POST", f"{C}/twilio/status/999999"), ("POST", f"{C}/twilio/gather/999999"), ("GET", f"{C}/twilio/voice/999999"),
    ("POST", f"{C}/twilio/voice/999999"), ("POST", f"{C}/exotel/status/999999"), ("GET", f"{C}/exotel/greeting"),
    ("GET", f"{C}/exotel/greeting?CustomField=abc"), ("GET", f"{C}/exotel/gather?CustomField=999999"),
    ("GET", f"{C}/exotel/passthru?CustomField=%22abc%22&digits=%221%22"), ("GET", f"{C}/exotel/passthru"),
    ("GET", f"{C}/exotel/passthru?CustomField=-1&digits=<script>"), ("POST", f"{C}/twilio/voice/abc"),
    ("GET", f"{C}/twilio/voice/1?retry=abc"), ("POST", f"{C}/twilio/gather/99999999999999999999999"),
    ("GET", f"{C}/exotel/passthru?CustomField=99999999999999999999999&digits=1")])
def test_call_webhooks_with_unknown_call_ids_do_not_crash(raw, method, url):
    r = raw.request(method, url, data={"CallStatus": "completed", "Digits": "1", "Status": "busy"} if method == "POST" else None)
    assert r.status_code < 500, r.text[:200]


# ----- harmful text

HARMFUL = {
    "script_tag": "<script>alert(1)</script>",
    "img_onerror": "<img src=x onerror=alert(1)>",
    "html_attr_break": "\"><svg/onload=alert(1)>",
    "sql_drop": "Robert'); DROP TABLE patients;--",
    "sql_or": "' OR '1'='1",
    "very_long": "A" * 20000,
    "emoji": "😀👨‍👩‍👧‍👦🔥 Dadi 💛",
    "right_to_left": "\u202eevil\u202c אבא مرحبا",
    "malayalam": "രവി കുമാർ",
    "tamil": "ரவி குமார்",
    "hindi": "रवि कुमार",
    "null_bytes": "A\x00B\x00",
    "format_string": "{name} {0} %s %d {a.__class__}",
    "header_injection": "Line1\r\nSet-Cookie: x=1",
    "backslashes": "C:\\Windows\\..\\..\\x",
}


def test_harmful_text_is_stored_and_returned_exactly_and_breaks_nothing(fresh, raw):
    problems = []
    for name, evil in HARMFUL.items():
        r = raw.post(f"{C}/guardians", json={"patient_id": 1, "name": evil, "relation": evil, "phone": evil,
                                             "city": evil, "language": "en", "consent": True})
        assert r.status_code == 200, f"{name}: {r.status_code} {r.text[:200]}"
        assert r.headers["content-type"].startswith("application/json")
        g = r.json()
        if g["name"] != evil.strip()[:80] or len(g["name"]) > 80:
            problems.append((name, "guardian name changed", g["name"][:60]))
        if g["city"] != evil.strip():
            problems.append((name, "city changed"))
        calls = {
            "family page": raw.get(f"{C}/guardian/{g['token']}"),
            "family reply": raw.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "guardian", "guardian_id": g["id"], "text": evil}),
            "family 1": raw.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "guardian", "guardian_id": g["id"], "text": "1"}),
            "family status": raw.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "guardian", "guardian_id": g["id"], "text": "status"}),
            "cheer": raw.post(f"{C}/guardian/{g['token']}/cheer", json={"preset": 0}),
            "consent ask": raw.post(f"{C}/consent/ask/1", json={"to": "family", "guardian_id": g["id"]}),
            "patient reply": raw.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": evil}),
            "family phone": raw.put("/api/patients/1", json={"family_phone": evil}),
            "patient phone": raw.put(f"{C}/care/1", json={"patient_phone": evil}),
            "nurse name": raw.post(f"{C}/call-patient/1", json={"nurse_name": evil, "nurse_phone": evil}),
            "collect person": raw.post("/api/collect", json={"person": evil, "label": "good", "features": {}}),
            "alert by": raw.post(f"{C}/alerts/1/assign", json={"by": evil, "to": evil}),
            "ladder reason": raw.post(f"{C}/escalations/start/1", json={"reason": evil, "speed": "fast", "override_quiet": True}),
            "voice question": raw.post("/api/voice/stt", data={"text": evil.replace("\x00", " "), "patient_id": "1"}),
        }
        rid = calls["ladder reason"].json().get("id") if calls["ladder reason"].status_code == 200 else None
        for i in range(5):
            if rid:
                calls[f"advance {i}"] = raw.post(f"{C}/escalations/{rid}/advance")
        for url in (f"{C}/patient/1", f"{C}/care/1", f"{C}/timeline/1?limit=200", f"{C}/alerts?status=all",
                    f"{C}/calls", f"{C}/events", "/api/messages?limit=200", "/api/patients", "/api/patients/1",
                    f"{C}/wa/thread/1?role=guardian&guardian_id={g['id']}", f"{C}/wa/thread/1?role=patient"):
            calls[url] = raw.get(url)
        for what, resp in calls.items():
            if resp.status_code >= 500:
                problems.append((name, what, resp.status_code, resp.text[:160]))
        # the text comes back unchanged (as JSON data): escaping is the web page's job
        thread = raw.get(f"{C}/wa/thread/1?role=guardian&guardian_id={g['id']}").json()
        if evil.strip() and evil.strip()[:1000] not in [m.get("text") for m in thread["items"] if m["dir"] == "in"]:
            problems.append((name, "inbound text not stored verbatim"))
        care = raw.get(f"{C}/care/1").json()
        if not any(x["name"] == evil.strip()[:80] for x in care["guardians"]):
            problems.append((name, "guardian name not returned verbatim"))
        assert raw.delete(f"{C}/guardians/{g['id']}").status_code == 200
    assert not problems, problems
    assert raw.get(f"{C}/card/1.png").headers["content-type"] == "image/png"
    # SQL-looking names did no damage
    assert len(raw.get("/api/patients").json()) == 7
    assert _st().count("patients") == 7 and _st().count("sessions") > 0


def test_harmful_text_in_urls_and_queries_comes_back_as_json_not_html(raw):
    for url in ("/api/<script>alert(1)</script>", "/api/patients/<script>alert(1)</script>",
                f"{C}/guardian/<script>alert(1)</script>", f"{C}/alerts?status=<script>alert(1)</script>",
                f"{C}/wa/thread/1?role=<img src=x onerror=alert(1)>", f"{C}/consent-text/1?lang=<b>x</b>",
                "/api/voice/cues?lang=<script>", f"{C}/card/1.png?lang=<script>"):
        r = raw.get(url)
        assert r.status_code < 500, url
        ctype = r.headers.get("content-type", "")
        assert "html" not in ctype, f"{url} answered as {ctype}"      # reflected text is never a web page


# ----- path traversal, odd ids, odd methods

TRAVERSAL = [
    "/%2e%2e/.env", "/..%2f.env", "/..%5c.env", "/.env", "/../.env", "/../../.env", "/%2e%2e%2f%2e%2e%2fCLAUDE.md",
    "/js/..%2f..%2f.env", "/js/../../.env", "/audio/../../.env", "/js/..%5c..%5cCLAUDE.md", "/js%5c..%5c..%5cCLAUDE.md",
    "/../backend/app/main.py", "/..%5cbackend%5capp%5cmain.py", "/%5c%5c..%5c..%5cbackend%5capp%5cmain.py",
    "/C:/Windows/win.ini", "/C:%5cWindows%5cwin.ini", "/js/api.js%00.png", "/....//....//.env",
    "/api/voice/audio/..%2F..%2F.env", "/api/voice/audio/....//....//.env", "/api/voice/audio/%2e%2e%5c%2e%2e%5c.env",
    "/api/voice/audio/..", "/api/voice/audio/abcdef12.mp3%00.env", "/api/voice/audio/ABCDEF12.exe",
    "/api/voice/clip/en/..%2F..%2Fx", "/api/voice/clip/..%2Fen/ready", "/api/voice/clip/en/%2e%2e%5cready",
    "/api/comms/card/..%2F..%2F.env.png", "/api/comms/card/1%2F..%2F..%2F.env.png", "/api/comms/card/%2e%2e.png",
    "/showcase/..%2f..%2f.env", "/showcase/../../backend/requirements.txt",
]


@pytest.mark.parametrize("url", TRAVERSAL)
def test_path_traversal_never_serves_a_file_outside_web(raw, url):
    r = raw.get(url)
    assert r.status_code in (400, 404, 405, 422), f"{url}: {r.status_code}"
    for secret in ("ANTHROPIC_API_KEY", "TWILIO_AUTH_TOKEN", "SARVAM_API_KEY", "from fastapi import", "[fonts]",
                   "instructions for every Claude session", "fastapi=="):
        assert secret not in r.text


ODD = [
    ("GET", "/api/patients/-1", (404,)), ("GET", "/api/patients/0", (404,)), ("GET", "/api/patients/999999", (404,)),
    ("GET", "/api/patients/abc", (422,)), ("GET", "/api/patients/1e3", (422,)), ("GET", "/api/patients/1.5", (422,)),
    ("GET", "/api/patients/99999999999999999999999", (400, 404, 422)),          # was a 500 (OverflowError)
    ("PUT", "/api/patients/99999999999999999999999", (400, 404, 422)),
    ("GET", "/api/patients/1/sessions?limit=0", (422,)), ("GET", "/api/patients/1/sessions?limit=abc", (422,)),
    ("GET", "/api/patients/1/sessions?limit=999999", (422,)), ("GET", "/api/patients/999999/sessions", (404,)),
    ("DELETE", "/api/patients/1", (405,)), ("PATCH", "/api/patients/1", (405,)), ("POST", "/api/patients", (405,)),
    ("DELETE", "/api/health", (405,)), ("PUT", "/api/demo/reset", (405,)), ("DELETE", "/api/messages", (405,)),
    ("GET", "/api/messages?limit=-1", (422,)), ("GET", "/api/nope", (404,)), ("POST", "/api/nope", (404, 405)),
    ("POST", "/api/summary/999999", (404,)), ("POST", "/api/summary/abc", (422,)), ("POST", "/api/whatsapp/-1", (404,)),
    ("POST", "/api/demo/simulate/999999", (404,)), ("POST", "/api/demo/miss/0", (404,)),
    ("GET", f"{C}/card/999999.png", (404,)), ("GET", f"{C}/card/abc.png", (422,)), ("GET", f"{C}/card/-1.png", (404,)),
    ("GET", f"{C}/card/99999999999999999999999.png", (400, 404, 422)),
    ("GET", f"{C}/calls/0", (404,)), ("GET", f"{C}/calls/-1", (404,)), ("GET", f"{C}/calls/abc", (422,)),
    ("POST", f"{C}/calls/999999/answer", (404,)), ("POST", f"{C}/calls/999999/hangup", (404,)),
    ("POST", f"{C}/calls/999999/press", (404, 422)), ("POST", f"{C}/calls/999999/agent-turn", (404, 422)),
    ("GET", f"{C}/alerts?limit=99999", (422,)), ("GET", f"{C}/alerts?patient_id=abc", (422,)),
    ("GET", f"{C}/alerts?status=%27;DROP%20TABLE%20alerts", (200,)), ("POST", f"{C}/alerts/999999/ack", (404,)),
    ("POST", f"{C}/alerts/999999/explode", (400, 404)), ("POST", f"{C}/alerts/abc/ack", (422,)),
    ("GET", f"{C}/timeline/999999", (404,)), ("GET", f"{C}/timeline/1?limit=0", (422,)), ("GET", f"{C}/events?since_id=-5", (200,)),
    ("GET", f"{C}/events?since_id=abc", (422,)), ("GET", f"{C}/wa/thread/999999", (404,)),
    ("GET", f"{C}/wa/thread/1?role=guardian&guardian_id=999999", (200,)), ("GET", f"{C}/wa/thread/1?guardian_id=abc", (422,)),
    ("GET", f"{C}/cheers/999999", (404,)), ("POST", f"{C}/cheers/999999/played", (404,)),
    ("GET", f"{C}/trend/999999", (404,)), ("GET", f"{C}/patient/999999", (404,)), ("GET", f"{C}/care/0", (404,)),
    ("PUT", f"{C}/care/999999", (404, 422)), ("GET", f"{C}/consent-text/999999", (404,)),
    ("POST", f"{C}/consent/ask/999999", (404,)), ("POST", f"{C}/escalations/start/999999", (404,)),
    ("POST", f"{C}/escalations/999999/stop", (404,)), ("POST", f"{C}/escalations/999999/advance", (404,)),
    ("POST", f"{C}/demo/ladder/999999", (404,)), ("POST", f"{C}/demo/red-flag/999999", (404,)),
    ("POST", f"{C}/checkin-call/999999", (404,)), ("POST", f"{C}/call-patient/999999", (404,)),
    ("POST", f"{C}/call-script/999999", (404,)), ("POST", f"{C}/weekly-card/999999", (404,)),
    ("POST", f"{C}/voice-note/999999", (404,)), ("DELETE", f"{C}/guardians/999999", (404,)),
    ("DELETE", f"{C}/guardians/abc", (422,)), ("PUT", f"{C}/guardians/999999", (404, 422)),
    ("GET", f"{C}/guardians", (404, 405)), ("GET", f"{C}/webhooks/whatsapp", (404, 405)),
    ("GET", "/api/voice/prefs/abc", (422,)), ("GET", "/api/voice/prefs/999999", (404,)),
    ("GET", "/api/voice/cues?lang=zz", (400,)), ("GET", "/api/voice/clip/zz/ready", (400,)),
    ("GET", "/api/voice/clip/en/not_a_cue", (404,)), ("POST", "/api/voice/stt", (400,)),
    ("POST", "/api/voice/summary-audio/999999", (404,)),
]


@pytest.mark.parametrize("method,url,expected", ODD, ids=[f"{m} {u}"[:70] for m, u, _ in ODD])
def test_odd_ids_and_methods_get_a_clean_answer(raw, method, url, expected):
    r = raw.request(method, url)
    assert r.status_code in expected, f"{r.status_code} {r.text[:200]}"
    if r.status_code >= 400:
        assert "error" in r.json()                           # always the JSON error shape, never a stack trace
        assert "Traceback" not in r.text


def test_voice_upload_limits_and_bad_patient(raw):
    assert raw.post("/api/voice/stt", data={"text": "hello", "patient_id": "abc"}).status_code == 422
    assert raw.post("/api/voice/stt", data={"text": "hello", "patient_id": "999999"}).status_code == 404
    big = raw.post("/api/voice/stt", files={"file": ("a.webm", b"\x00" * (5 * 1024 * 1024 + 1))})
    assert big.status_code == 413
    tiny = raw.post("/api/voice/stt", files={"file": ("../../x.webm", b"abc")})
    assert tiny.status_code == 503 and tiny.json()["fallback"] == "browser"      # no key: clean fallback
    assert raw.post("/api/voice/tts", json={"text": "x" * 5001}).status_code == 400


# ============================================================================= 2. SAFETY

RED_FLAGS = {
    "en": ["chest pain", "CHEST PAIN", "Chest  Pain!!!", "chest-pain", "I have chest pain since morning, what should I do?",
           "i cant breathe", "I can’t breathe", "I CAN'T BREATHE", "can not breathe", "shortness   of breath",
           "HELP", "help me please", "fever", "FEVER 102", "there is blood in my cough", "I feel dizzy",
           "feeling faint", "is this an emergency?", "ok done but chest pain now", "breathless"],
    "hi": ["सीने में दर्द", "सीने  में  दर्द है", "मुझे साँस नहीं आ रही", "मुझे सांस नहीं आ रही है।", "बुखार है",
           "मदद", "बचाओ!", "छाती में दर्द हो रहा है", "खून आ रहा है", "चक्कर आ रहा है", "मैं बेहोश हो रहा हूँ",
           "नमस्ते, कल से बुखार है और साँस फूल रही है"],
    "hi_typed_in_english": ["seene mein dard hai", "SEENE MEIN DARD", "Seene  mein  dard", "saans nahi aa rahi",
                            "mujhe bukhar hai", "bachao", "madad", "Madad karo", "sans nahi aa rahi",
                            "chakkar aa raha hai", "khoon aa raha hai"],
    "ta": ["நெஞ்சு வலி", "எனக்கு நெஞ்சு வலி இருக்கு", "நெஞ்சு  வலி!", "மூச்சு திணறல்", "மூச்சுத் திணறல் இருக்கிறது",
           "காய்ச்சல்", "உதவி", "ரத்தம் வருகிறது", "மயக்கம்", "மூச்சு விட முடியவில்லை"],
    "ml": ["നെഞ്ചുവേദന", "എനിക്ക് നെഞ്ചുവേദന ഉണ്ട്", "നെഞ്ച് വേദന", "ശ്വാസം മുട്ടുന്നു", "പനി ഉണ്ട്", "രക്തം",
           "തലകറക്കം", "ശ്വസിക്കാൻ പറ്റുന്നില്ല", "സഹായം", "സഹായിക്കൂ!", "എന്നെ രക്ഷിക്കൂ"],
}
RED_FLAG_CASES = [(lang, t) for lang, ts in RED_FLAGS.items() for t in ts]


@pytest.mark.parametrize("lang,text", RED_FLAG_CASES, ids=[f"{lg}-{i}" for i, (lg, _) in enumerate(RED_FLAG_CASES)])
def test_every_red_flag_wording_is_caught_for_patient_and_family(lang, text):
    from backend.app.comms import messages, sarvam
    assert messages.detect_intent(text, "patient") == "red_flag", text
    assert messages.detect_intent(text, "guardian") == "red_flag", text
    if text.strip(" !?.").lower() != "help":                  # on a phone call a bare "help" is deliberately ignored
        assert sarvam.red_flag_words(text), text


@pytest.mark.parametrize("text", ["done", "1", "2", "3", "status", "I did my breathing", "thank you", "ok",
                                  "हो गया", "நிலை", "ചെയ്തു", "what time is my next session?"])
def test_ordinary_replies_are_not_red_flags(text):
    from backend.app.comms import messages
    assert messages.detect_intent(text, "patient") != "red_flag"


@pytest.mark.xfail(strict=True, reason="OPEN (fix before real patients): Tamil and Malayalam typed in English letters "
                   "('nenju vali', 'swasam muttunnu') are not in the red-flag lists; only typed Hindi is "
                   "(backend/app/voice.py RED_FLAG_WORDS 'hi_latn', backend/app/comms/messages.py RED_FLAG_RE). "
                   "Needs word lists from native speakers.")
@pytest.mark.parametrize("text", ["nenju vali", "moochu thinaral", "kaichal", "nenchu vedana", "swasam muttunnu", "sahayam"])
def test_typed_tamil_and_malayalam_red_flags(text):
    from backend.app.comms import messages
    assert messages.detect_intent(text, "patient") == "red_flag"


def test_red_flag_gets_the_fixed_message_and_an_alert_in_all_four_languages(fresh):
    from backend.app.comms.messages import NURSE_TOLD, RED_FLAG_TEXT
    by_lang = {p["language"]: p["id"] for p in reversed(fresh.get("/api/patients").json())}
    phrase = {"en": "Sister, I have CHEST   pain since morning", "hi": "मुझे सीने  में दर्द है!!",
              "ta": "எனக்கு நெஞ்சு வலி இருக்கு", "ml": "എനിക്ക് നെഞ്ചുവേദന ഉണ്ട്"}
    assert set(phrase) <= set(by_lang)
    for lang, text in phrase.items():
        pid = by_lang[lang]
        r = fresh.post(f"{C}/wa/reply", json={"patient_id": pid, "role": "patient", "text": text})
        assert r.status_code == 200, r.text
        out = r.json()
        assert out["intent"] == "red_flag"
        assert out["reply"] == f"{RED_FLAG_TEXT[lang]} {NURSE_TOLD[lang]}"       # FIXED text, word for word
        assert "112" in out["reply"]
        alerts = [a for a in fresh.get(f"{C}/alerts?patient_id={pid}").json() if a["kind"] == "red_flag"]
        assert len(alerts) == 1 and alerts[0]["severity"] == "red" and alerts[0]["status"] == "open"
        row = next(p for p in fresh.get("/api/patients").json() if p["id"] == pid)
        assert row["red_flag_open"] is True and row["status"] == "red"
        sent = _st().select("messages", [("patient_id", "eq", pid), ("kind", "eq", "reply")])
        assert any(RED_FLAG_TEXT[lang] in m["text"] for m in sent)               # and it was actually sent back
        assert fresh.get(f"{C}/escalations?patient_id={pid}").json()[0]["red_flag"] is True   # family + nurse ladder
    # a family member's red flag counts too
    g = fresh.get(f"{C}/care/3").json()["guardians"][0]
    fam = fresh.post(f"{C}/wa/reply", json={"patient_id": 3, "role": "guardian", "guardian_id": g["id"],
                                            "text": "he can't breathe"}).json()
    assert fam["intent"] == "red_flag" and "112" in fam["reply"]
    assert [a for a in fresh.get(f"{C}/alerts?patient_id=3").json() if a["kind"] == "red_flag" and a["status"] == "open"]


def test_red_flag_at_the_end_of_a_long_message_and_in_the_ai_phone_call(raw):
    from backend.app.voice import red_flag_message
    text = ("I did my exercise today and I feel okay. " * 40) + "but now I have chest pain"
    assert len(text) > 1000                                    # only the first 1000 characters are stored
    r = raw.post(f"{C}/wa/reply", json={"patient_id": 5, "role": "patient", "text": text}).json()
    assert r["intent"] == "red_flag" and "112" in r["reply"]   # missed before the fix
    assert [a for a in raw.get(f"{C}/alerts?patient_id=5").json() if a["kind"] == "red_flag"]
    # the simulated AI conversation call
    call = raw.post(f"{C}/checkin-call/7").json()
    assert call["simulated"] and call["style"] == "agent", call
    assert raw.post(f"{C}/calls/{call['id']}/answer").status_code == 200
    turn = raw.post(f"{C}/calls/{call['id']}/agent-turn", json={"text": "I can't breathe properly.", "source": "voice"}).json()
    assert red_flag_message(call["language"]) in turn["say"]
    done = raw.get(f"{C}/calls/{call['id']}").json()
    assert done["result"]["outcome"] == "red_flag" and done["result"]["red_flag"] is True
    assert [a for a in raw.get(f"{C}/alerts?patient_id=7").json() if a["kind"] == "red_flag"]


def test_red_flags_never_go_to_the_ai_for_a_free_answer(raw, monkeypatch):
    from backend.app.comms.messages import RED_FLAG_TEXT
    from backend.app.voice_cues import cue_text
    fake = _claude(monkeypatch, _says("It is probably nothing, just rest."))       # what a free answer would look like
    monkeypatch.setenv("DEMO_PATIENT_PHONE", PATIENT_PHONE)
    replies = []
    for text in ("chest pain", "मुझे साँस नहीं आ रही", "help", "I have a fever and blood in my cough"):
        replies.append(raw.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": text}).json()["reply"])
    assert raw.post(f"{C}/webhooks/whatsapp", data={"From": f"whatsapp:{PATIENT_PHONE}", "Body": "chest pain"}).status_code == 200
    replies.append(raw.post(f"{C}/demo/red-flag/1", json={"text": "seene mein dard"}).json()["reply"])
    for r in replies:
        assert r.startswith(RED_FLAG_TEXT["hi"]) and "probably nothing" not in r
    v = raw.post("/api/voice/stt", data={"text": "I can't breathe", "patient_id": "1"}).json()
    assert v["red_flag"] is True and v["reply_cue"] == "red_flag" and v["reply"] == cue_text("red_flag", v["lang"])
    assert fake.calls == [], "a red-flag message was passed to the LLM"
    logged = _st().select("messages", [("patient_id", "eq", 1)])
    assert not any("probably nothing" in (m.get("text") or "") for m in logged)


def test_spoken_red_flag_gets_the_fixed_message_in_all_four_languages(raw):
    from backend.app.voice_cues import cue_text
    by_lang = {p["language"]: p["id"] for p in reversed(raw.get("/api/patients").json())}
    for lang, text in (("en", "I have chest pain"), ("hi", "मुझे सीने में दर्द है"), ("ta", "எனக்கு நெஞ்சு வலி"),
                       ("ml", "എനിക്ക് നെഞ്ചുവേദന")):
        pid = by_lang[lang]
        r = raw.post("/api/voice/stt", data={"text": text, "patient_id": str(pid)})
        assert r.status_code == 200, r.text
        v = r.json()
        assert v["red_flag"] is True and v["reply_cue"] == "red_flag" and v["nurse_notified"] is True, lang
        assert v["reply"] == cue_text("red_flag", v["lang"]) and "112" in v["reply"]
        assert [a for a in raw.get(f"{C}/alerts?patient_id={pid}").json() if a["kind"] == "red_flag"], lang
    calm = raw.post("/api/voice/stt", data={"text": "How many times a day should I do this?", "patient_id": "1"}).json()
    assert calm["red_flag"] is False and calm["reply_cue"] == "faq_how_often"


# ----- STOP / opt-out

STOP_WORDS = ["stop", "STOP", " Stop. ", "stop!", "Stop!!", "STOP please", "please stop", "Please STOP.", "stop it",
              "stop messages", "stop calls", "stop sending messages", "unsubscribe", "रोको", "रोको।", "रोकें", "बंद करो",
              "बंद", "நிறுத்து", "நிறுத்தவும்", "നിർത്തുക", "നിർത്തൂ", "roko", "Ruko", "band karo", "⛔ STOP", "⛔ रोको (STOP)"]


@pytest.mark.parametrize("word", STOP_WORDS)
def test_stop_word_is_understood_in_every_language(word):
    from backend.app.comms import messages
    assert messages.detect_intent(word, "patient") == "stop", word
    assert messages.detect_intent(word, "guardian") == "stop", word


@pytest.mark.parametrize("text,expect", [
    ("I can't stop coughing", "unknown"), ("don't stop the reminders", "unknown"), ("non stop", "unknown"),
    ("stop the bleeding", "red_flag"), ("please stop, I have chest pain", "red_flag"), ("बंद करो, बुखार है", "red_flag")])
def test_stop_is_not_triggered_by_accident_and_never_hides_a_red_flag(text, expect):
    from backend.app.comms import messages
    assert messages.detect_intent(text, "patient") == expect


@pytest.mark.xfail(strict=True, reason="OPEN (fix before real patients): STOP typed in English letters for Tamil / "
                   "Malayalam ('niruthu', 'nirthu') is not understood (backend/app/comms/consent.py STOP_RE). "
                   "Needs spellings from native speakers. The word STOP itself works for everyone.")
@pytest.mark.parametrize("word", ["niruthu", "nirthu", "niruththu"])
def test_typed_tamil_and_malayalam_stop_words(word):
    from backend.app.comms import messages
    assert messages.detect_intent(word, "patient") == "stop"


def test_after_patient_stop_nothing_automated_reaches_the_patient(fresh):
    from backend.app.comms import consent
    rid = fresh.post(f"{C}/demo/ladder/1", json={"override_quiet": True}).json()["id"]
    r = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": "STOP"}).json()
    assert r["intent"] == "stop"
    run = [x for x in fresh.get(f"{C}/escalations?patient_id=1").json() if x["id"] == rid][0]
    assert run["status"] == "resolved" and run["outcome"] == "stopped_by_patient"     # the running ladder stops too
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is False
    msgs, calls = len(_out(1, "patient")), len(_calls_to(1, "patient"))
    card = fresh.post(f"{C}/weekly-card/1", json={"to": "patient"})
    note = fresh.post(f"{C}/voice-note/1", json={"to": "patient"})
    ask = fresh.post(f"{C}/consent/ask/1", json={"to": "patient"})
    for resp in (card, note, ask):                         # each of these sent a message before the fix
        assert resp.status_code == 200, resp.text
        assert resp.json()["blocked"] is True and resp.json()["sent"] is False and resp.json()["dry_run"] is False
    assert fresh.post(f"{C}/checkin-call/1").status_code == 409
    _run_whole_ladder(fresh, 1)                            # reminder WhatsApp + reminder call steps
    consent.weekly_check()
    assert len(_out(1, "patient")) == msgs, [m["kind"] for m in _out(1, "patient")][-5:]
    assert len(_calls_to(1, "patient")) == calls
    titles = [e["title"] for e in fresh.get(f"{C}/timeline/1?limit=200").json()]
    assert any("skipped – no recorded consent" in t for t in titles)             # and the nurse can see why
    assert [a for a in fresh.get(f"{C}/alerts?patient_id=1").json() if a["severity"] == "red"]   # nurse still told
    # a red flag after STOP still gets the fixed reply and reaches the nurse
    red = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": "chest pain"}).json()
    assert "112" in red["reply"]
    assert [a for a in fresh.get(f"{C}/alerts?patient_id=1").json() if a["kind"] == "red_flag" and a["status"] == "open"]
    # consent given again (recorded by the nurse) -> reminders flow again
    fresh.put(f"{C}/care/1", json={"consent": True})
    _run_whole_ladder(fresh, 1)
    assert len(_out(1, "patient")) == msgs + 1 and _out(1, "patient")[-1]["kind"] == "reminder"
    assert len(_calls_to(1, "patient")) == calls + 1
    # the same through the API for the other languages and a polite form
    for word in ("please stop", "रोको", "நிறுத்து", "നിർത്തുക", "band karo"):
        assert fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": word}).json()["intent"] == "stop", word
        assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is False
        assert fresh.post(f"{C}/weekly-card/1", json={"to": "patient"}).json()["blocked"] is True
        fresh.put(f"{C}/care/1", json={"consent": True})


def test_after_guardian_stop_nothing_automated_reaches_that_guardian(fresh):
    from backend.app.comms import consent
    g = fresh.get(f"{C}/care/1").json()["guardians"][0]
    assert g["is_primary"] and g["consent_ok"]
    r = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "guardian", "guardian_id": g["id"], "text": "रोको"}).json()
    assert r["intent"] == "stop"
    assert fresh.get(f"{C}/care/1").json()["guardians"][0]["consent_ok"] is False
    family_before = len(_out(1, "family"))
    mine = len(_out(1, "family", g["phone"]))
    calls = len(_calls_to(1, "guardian", g["id"]))
    summary = fresh.post("/api/whatsapp/1", json={"kind": "summary", "to": "family"}).json()
    missed = fresh.post("/api/whatsapp/1", json={"kind": "missed", "to": "family"}).json()
    card = fresh.post(f"{C}/weekly-card/1", json={"to": "family"}).json()          # sent before the fix
    note = fresh.post(f"{C}/voice-note/1", json={"to": "family"}).json()           # sent before the fix
    ask = fresh.post(f"{C}/consent/ask/1", json={"to": "family"}).json()           # sent before the fix
    for out in (summary, missed, card, note, ask):
        assert out["blocked"] is True and out["sent"] is False and out["dry_run"] is False, out
    miss = fresh.post("/api/demo/miss/1").json()
    assert miss["alerts"][1]["blocked"] is True               # the family half of the missed alert (sent before the fix)
    assert miss["alerts"][0]["to_role"] == "nurse" and miss["alerts"][0].get("blocked") is not True
    assert len(_out(1, "family")) == family_before             # none of the six went anywhere
    _run_whole_ladder(fresh, 1)                               # guardian WhatsApp + guardian call step
    fresh.post(f"{C}/demo/red-flag/1", json={"text": "chest pain"})
    rid = fresh.get(f"{C}/escalations?patient_id=1&active=1").json()[0]["id"]
    for _ in range(3):
        fresh.post(f"{C}/escalations/{rid}/advance")
    consent.weekly_check()
    assert len(_out(1, "family", g["phone"])) == mine
    assert len(_calls_to(1, "guardian", g["id"])) == calls
    # the other family members, who did not say STOP, are still told
    others = [m for m in _out(1, "family") if m.get("to_number") != g["phone"]]
    assert any(m["kind"] == "guardian_alert" for m in others)
    # consent again -> updates flow again
    fresh.put(f"{C}/guardians/{g['id']}", json={"consent": True})
    again = fresh.post("/api/whatsapp/1", json={"kind": "summary", "to": "family"}).json()
    assert again.get("blocked") is not True and again["dry_run"] is True
    # the same through the API for the other languages
    for word in ("stop", "நிறுத்து", "നിർത്തൂ", "STOP please"):
        out = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "guardian", "guardian_id": g["id"], "text": word}).json()
        assert out["intent"] == "stop", word
        assert fresh.post("/api/whatsapp/1", json={"kind": "summary", "to": "family"}).json()["blocked"] is True
        fresh.put(f"{C}/guardians/{g['id']}", json={"consent": True})


# ----- the AI never diagnoses

BANNED_CLAIMS = re.compile(
    r"prevents?\s+pneumonia|prevents?\s+(lung\s+)?(infection|complication)|clinically\s+proven|fda|"
    r"world'?s\s+first|first\s+of\s+its\s+kind|first[- ]ever|\bcures?\b|guarantee|"
    r"you\s+(may\s+|might\s+|probably\s+)?have\s+(a\s+|an\s+)?(pneumonia|infection|atelectasis|embolism|covid|tb\b)", re.I)
DISEASE_WORDS = re.compile(r"pneumonia|atelectasis|embolism|tuberculosis|antibiotic|\bcopd\b|asthma|cancer|"
                           r"निमोनिया|நிமோனியா|ന്യുമോണിയ", re.I)


def _all_fixed_texts():
    """Every fixed sentence SpiroBuddy can say or send by itself (templates and fallbacks)."""
    from backend.app import llm, voice_cues, whatsapp
    from backend.app.comms import calls, common, consent, messages, sarvam
    p = {"id": 1, "name": "Ravi Kumar", "sex": "M", "language": "hi"}
    g = {"id": 1, "name": "Amit Kumar", "relation": "son", "language": "en"}
    out = []
    shapes = [dict(first_name="Ravi", done=d, due=u, best_ml=b, target_ml=2000, personal_best_ml=2100)
              for d, u, b in ((0, 0, 0), (0, 5, 0), (2, 6, 900), (6, 6, 2100))]
    shapes.append({**shapes[0], "recent": {"days": 1, "sessions": 7, "best_ml": 1800}})
    shapes.append({**shapes[0], "recent": {"days": 3, "sessions": 12, "best_ml": 1900}})
    for lang in ("en", "hi", "ta", "ml"):
        out += [("summary template", llm.template_summary(s, lang)) for s in shapes]
        out += [("missed alert", whatsapp.missed_text(p, [9, 10], lang)), ("reminder", messages.reminder_text(p, lang, 2)),
                ("red flag", messages.RED_FLAG_TEXT[lang]), ("nurse told", messages.NURSE_TOLD[lang]),
                ("footer", messages.FOOTER[lang]), ("disclosure", common.DISCLOSURE[lang]),
                ("renew", consent.RENEW_TEXT[lang]), ("stop reply", consent.REPLY["stop"][lang]),
                ("yes reply", consent.REPLY["consent_yes"][lang])]
        out += [("cheer", c) for c in messages.CHEER_PRESETS[lang]]
        out += [("reply " + k, v.get(lang) or v["en"]) for k, v in messages.REPLIES.items()]
        for red in (False, True):
            out.append(("guardian alert", messages.guardian_alert_text(p, {**g, "language": lang}, 2, False, red)))
    for lang in ("en", "hi", "ta"):
        out += [("consent text", consent.consent_text(lang)["text"]), ("ivr patient", calls.menu_text("reminder", p, lang, None, 2)),
                ("ivr guardian", calls.menu_text("guardian", p, lang, g, 2)),
                ("ivr guardian red", calls.menu_text("guardian_red_flag", p, lang, g, 2))]
        out += [("agent line " + k, v[lang]) for k, v in sarvam.AGENT_LINES.items()]
        out += [("after key", v[lang]) for v in calls.AFTER.values()]
    for key in voice_cues.all_cues()["order"]:
        for lang in ("en", "hi", "ta", "ml"):
            out.append((f"voice cue {key}", voice_cues.cue_text(key, lang) or ""))
    return [(k, t) for k, t in out if t]


def test_no_fixed_text_makes_a_banned_claim_or_names_a_disease():
    texts = _all_fixed_texts()
    assert len(texts) > 250
    bad = []
    for where, t in texts:
        if BANNED_CLAIMS.search(t) or DISEASE_WORDS.search(t):
            bad.append((where, t[:140]))
        for m in re.finditer(r"diagnos\w*", t, re.I):         # the only allowed use: "it never diagnoses"
            if not re.search(r"never|not|no", t[max(0, m.start() - 25):m.start()], re.I):
                bad.append((where, t[:140]))
    assert not bad, bad


def test_ai_instructions_forbid_diagnosis_and_the_operation_is_not_sent_for_family_text(raw, monkeypatch):
    from backend.app import llm
    from backend.app.comms import script
    for name, prompt in (("llm.SYSTEM", llm.SYSTEM), ("script.SYSTEM", script.SYSTEM)):
        assert re.search(r"never diagnose", prompt, re.I), name
        assert re.search(r"never name diseases", prompt, re.I), name
        assert not BANNED_CLAIMS.search(prompt), name
    fake = _claude(monkeypatch, _says("Ravi did two sessions today. The best breath was 1500 mL. Keep breathing slowly."))
    r = raw.post("/api/summary/1", json={}).json()
    assert r["source"] == "llm" and len(fake.calls) == 1        # proves the fake AI is really in the path
    sent = fake.calls[0]
    assert sent["model"] == "claude-opus-5-5" and sent["max_tokens"] <= 400
    assert sent["output_config"] == {"effort": "low"}
    family_prompt = sent["messages"][0]["content"]
    assert "hernia" not in family_prompt.lower() and "surgery" not in family_prompt.lower()   # Q-23


def test_ai_text_that_sounds_like_a_diagnosis_is_thrown_away(raw, monkeypatch):
    for ai_text in ("Ravi may have pneumonia, please see a doctor.", "This looks like a chest infection.",
                    "He should take his medication and an antibiotic.", "I diagnose a mild fever.",
                    "Signs of atelectasis today.", "Increase the dose of the medicine."):
        fake = _claude(monkeypatch, _says(ai_text))
        r = raw.post("/api/summary/1", json={"language": "en"})
        assert r.status_code == 200
        assert r.json()["source"] == "template" and ai_text not in r.json()["text"], ai_text
        assert len(fake.calls) == 1
        s = raw.post(f"{C}/call-script/1").json()
        assert s["source"] == "template" and ai_text not in s["text"]
        w = raw.post("/api/whatsapp/1", json={"kind": "summary", "to": "nurse"}).json()
        assert ai_text not in w["text"] and len(fake.calls) == 3


# ----- consent: date, expiry, weekly renewal

def test_consent_older_than_7_days_blocks_real_calls_until_renewed(fresh, monkeypatch):
    from backend.app.comms import calls, guardians
    from backend.app.config import iso, now_local
    placed = []
    monkeypatch.setattr(calls, "_twilio_call", lambda cid, number, ring_s: placed.append((cid, number)) or None)
    _twilio_voice_env(monkeypatch)
    fresh.put(f"{C}/care/1", json={"call_style": "ivr"})
    gs = fresh.get(f"{C}/care/1").json()["guardians"]

    def ladder_calls():
        placed.clear()
        _run_whole_ladder(fresh, 1)
        rows = _st().select("calls", [("patient_id", "eq", 1)], order="id", desc=True, limit=2)
        return {c["to_role"]: c for c in rows}

    # day 2 (seeded): real calls go out to the patient and one guardian
    first = ladder_calls()
    assert {c["provider"] for c in first.values()} == {"twilio"} and len(placed) == 2
    # day 8: consent is still "on record" but too old -> simulator only, nothing real is dialled
    _age_consent(8, pid=1)
    for g in gs:
        _age_consent(8, guardian_id=g["id"])
    s = fresh.get(f"{C}/care/1").json()
    assert s["settings"]["consent_ok"] and s["settings"]["consent_renew_due"] and s["settings"]["consent_age_days"] == 8
    assert all(g["consent_renew_due"] for g in s["guardians"])
    old = ladder_calls()
    assert placed == [], "a real call was placed with consent older than 7 days"
    assert {c["provider"] for c in old.values()} == {"dry_run"}
    assert all("7 days" in c["meta"]["note"] for c in old.values())
    # exactly 7 days is already too old; 6 days is still fine
    _age_consent(7, pid=1)
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_renew_due"] is True
    _age_consent(6, pid=1)
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_renew_due"] is False
    # the patient says "yes" to the weekly question -> real calls again (the family's is still too old)
    _age_consent(8, pid=1)
    fresh.post(f"{C}/consent/ask/1", json={"to": "patient"})
    yes = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": "1"}).json()
    assert yes["intent"] == "consent_yes"
    renewed = ladder_calls()
    assert renewed["patient"]["provider"] == "twilio" and renewed["guardian"]["provider"] == "dry_run"
    assert [n for _, n in placed] == [PATIENT_PHONE]
    # a consent tick with no date (or a broken date) is not consent at all
    for when in (None, "not-a-date"):
        cfg = guardians.get_settings(1)
        cfg["consent"], cfg["consent_at"] = True, when
        _st().upsert("care_settings", [{"patient_id": 1, "config": cfg, "updated_at": iso(now_local())}])
        assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is False
        assert fresh.post(f"{C}/checkin-call/1").status_code == 409
        assert fresh.post(f"{C}/weekly-card/1", json={"to": "patient"}).json()["blocked"] is True


def test_weekly_renewal_question_goes_out_once_and_only_to_people_with_consent(fresh, monkeypatch):
    from backend.app.comms import common, consent
    monkeypatch.setattr(consent, "in_quiet", lambda *a, **k: False)             # run as if it were daytime
    _age_consent(6, pid=1)                                                      # runs out tomorrow -> ask today
    fresh.post(f"{C}/wa/reply", json={"patient_id": 2, "role": "patient", "text": "STOP"})
    before2 = len(_out(2, "patient"))
    n = consent.weekly_check()
    asked = [m for m in _out(1, "patient") if m["kind"] == "consent_renewal"]
    assert n >= 1 and len(asked) == 1
    assert consent.weekly_check() == 0                                           # not asked twice within 48 hours
    assert len([m for m in _out(1, "patient") if m["kind"] == "consent_renewal"]) == 1
    assert len(_out(2, "patient")) == before2                                    # never to someone who said STOP
    assert common.CONSENT_RENEW_DAYS == 7


# ============================================================================= 3. FAILURES

def test_llm_failure_falls_back_to_the_template_with_http_200(raw, monkeypatch):
    failures = {
        "timeout": _boom(TimeoutError("timed out")),
        "api_error": _boom(RuntimeError("529 overloaded")),
        "connection": _boom(ConnectionError("no network")),
        "refusal": _says("I can't help with that.", stop="refusal"),
        "max_tokens": _says("Ravi did", stop="max_tokens"),
        "empty": _says("   "),
        "bad_shape": lambda kw: SimpleNamespace(stop_reason="end_turn", content=None),
    }
    for name, behaviour in failures.items():
        fake = _claude(monkeypatch, behaviour)
        for lang in ("en", "hi", "ta", "ml"):
            r = raw.post("/api/summary/2", json={"language": lang})
            assert r.status_code == 200, f"{name}/{lang}: {r.text}"
            assert r.json()["source"] == "template" and len(r.json()["text"]) > 40
        assert len(fake.calls) == 4, name
        assert raw.post(f"{C}/call-script/2").json()["source"] == "template"
        assert raw.post("/api/whatsapp/2", json={"kind": "summary", "to": "nurse"}).status_code == 200
        assert raw.post(f"{C}/voice-note/2", json={"to": "family"}).status_code == 200
        assert raw.post("/api/voice/summary-audio/2", json={}).status_code == 200
        assert len(fake.calls) >= 7, name                      # the AI really was asked each time, and failed


def test_no_llm_key_uses_the_template(raw, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    assert raw.get("/api/health").json()["llm_enabled"] is False
    for pid in (1, 2, 4, 6):
        r = raw.post(f"/api/summary/{pid}", json={})
        assert r.status_code == 200 and r.json()["source"] == "template"
    assert raw.post("/api/summary/1", json={"language": "xx"}).json()["source"] == "template"   # unknown language -> English
    assert raw.post(f"{C}/call-script/1").json()["source"] == "template"


def test_sarvam_voice_down_falls_back_to_the_browser_voice(raw, monkeypatch):
    from backend.app import voice
    monkeypatch.setenv("SARVAM_API_KEY", "fake-sarvam-key")
    hits = []

    def down(path, **kw):
        hits.append(path)
        raise ConnectionError("Sarvam is down")
    monkeypatch.setattr(voice, "_post", down)
    assert voice.enabled()
    t = raw.post("/api/voice/tts", json={"text": "यह पहले कभी नहीं बोला गया वाक्य है", "language": "hi"})
    assert t.status_code == 503 and t.json()["fallback"] == "browser" and t.json()["text"]
    tr = raw.post("/api/voice/translate", json={"text": "Never translated before sentence", "target": "ta"})
    assert tr.status_code == 200 and tr.json()["translated"] is False            # original text, no crash
    assert raw.post("/api/voice/detect", json={"text": "नमस्ते"}).json()["lang"] == "hi"
    s = raw.post("/api/voice/stt", files={"file": ("q.webm", b"not really audio")})
    assert s.status_code == 503 and s.json()["fallback"] == "browser"
    q = raw.post("/api/voice/stt", data={"text": "मुझे सीने में दर्द है", "patient_id": "1"})
    assert q.status_code == 200 and q.json()["red_flag"] is True                 # red flag still caught offline
    sa = raw.post("/api/voice/summary-audio/2", json={})
    assert sa.status_code == 200 and sa.json()["fallback"] == "browser" and sa.json()["text"]
    vn = raw.post(f"{C}/voice-note/2", json={"to": "family"})
    assert vn.status_code == 200 and vn.json()["audio_url"] is None
    assert raw.get(f"{C}/consent-text/1").status_code == 200
    assert hits, "the fake Sarvam was never reached, so this test proved nothing"


def test_sarvam_agent_and_twilio_calls_down_ring_the_simulator_instead(raw, monkeypatch):
    from backend.app.comms import calls, sarvam
    _sarvam_env(monkeypatch)
    monkeypatch.setattr(sarvam, "_post", _boom(ConnectionError("Sarvam agent is down")))
    c = raw.post(f"{C}/checkin-call/7")
    assert c.status_code == 200 and c.json()["provider"] == "dry_run" and c.json()["status"] == "ringing"
    assert "Sarvam call failed" in c.json()["note"]
    _twilio_voice_env(monkeypatch)
    monkeypatch.setattr(calls, "_twilio_client", _boom(ConnectionError("Twilio is down")))
    raw.put(f"{C}/care/7", json={"call_style": "ivr"})
    _run_whole_ladder(raw, 7)
    last = raw.get(f"{C}/calls?patient_id=7&limit=2").json()
    assert {x["provider"] for x in last} == {"dry_run"} and all("real call failed" in x["note"] for x in last)
    titles = " | ".join(e["title"] for e in raw.get(f"{C}/timeline/7?limit=100").json())
    assert "would call" in titles                              # the nurse sees that it only rang in the simulator


def test_whatsapp_provider_down_reports_failed_not_sent_and_never_500(raw, monkeypatch):
    import twilio.rest
    from backend.app import whatsapp
    for k, v in {"TWILIO_ACCOUNT_SID": "ACtest", "TWILIO_AUTH_TOKEN": "tok", "TWILIO_WHATSAPP_FROM": "whatsapp:+14155238886",
                 "DEMO_GUARDIAN_PHONE": "+919800000003", "DEMO_PATIENT_PHONE": PATIENT_PHONE,
                 "DEMO_NURSE_WHATSAPP": "+919800000004", "DEMO_FAMILY_WHATSAPP": "+919800000003"}.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(whatsapp, "throttle", lambda: None)                      # no 3-second waits in tests
    tried = []

    class Down:
        def __init__(self, *a, **k):
            tried.append(a)
            raise ConnectionError("Twilio is down")
    monkeypatch.setattr(twilio.rest, "Client", Down)
    assert raw.get("/api/health").json()["whatsapp_enabled"] is True
    for body in ({"kind": "summary", "to": "family"}, {"kind": "missed", "to": "nurse"}):
        r = raw.post("/api/whatsapp/3", json=body)
        assert r.status_code == 200, r.text
        out = r.json()
        assert out["sent"] is False and out["dry_run"] is False and "Twilio is down" in out["error"], out
    for url, body in ((f"{C}/weekly-card/3", {"to": "family"}), (f"{C}/voice-note/3", {"to": "patient"}),
                      (f"{C}/consent/ask/3", {"to": "patient"}), ("/api/demo/miss/3", None),
                      (f"{C}/wa/reply", {"patient_id": 3, "role": "patient", "text": "status"})):
        r = raw.post(url, json=body)
        assert r.status_code == 200, f"{url}: {r.text[:200]}"
    _run_whole_ladder(raw, 3)
    assert len(tried) >= 6
    log = raw.get("/api/messages?limit=12").json()
    assert log and not any(m["sent"] for m in log)             # nothing is recorded as sent
    assert raw.get(f"{C}/status").json()["whatsapp_last"]["sent"] is False


def test_no_provider_keys_means_a_clear_would_send_dry_run(raw):
    assert raw.get("/api/health").json()["whatsapp_enabled"] is False
    st = raw.get(f"{C}/status").json()
    assert st["calls_provider"] == "dry_run" and st["checkin_provider"] == "dry_run"
    for body in ({"kind": "summary", "to": "family"}, {"kind": "missed", "to": "nurse"}):
        out = raw.post("/api/whatsapp/4", json=body).json()
        assert out["sent"] is False and out["dry_run"] is True and out["text"], out
    _run_whole_ladder(raw, 4)
    events = raw.get(f"{C}/timeline/4?limit=100").json()
    assert any("would send – dry run" in e["title"] for e in events)
    assert any("phone simulator" in e["title"] and "dry run" in e["title"] for e in events)
    assert all(c["simulated"] for c in raw.get(f"{C}/calls?patient_id=4").json())


# ----- data store

def test_supabase_without_keys_falls_back_to_the_demo_store(monkeypatch):
    from backend.app import store
    monkeypatch.setenv("DATA_BACKEND", "supabase")
    for url, key in (("", ""), ("https://demo.supabase.co", ""), ("", "sb_secret_test")):
        monkeypatch.setenv("SUPABASE_URL", url)
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", key)
        st, note = store.make_store()
        try:
            assert st.name == "demo" and "missing" in note and "demo SQLite" in note
        finally:
            st.conn.close()


@pytest.mark.parametrize("error", [ConnectionError("no route to host"), TimeoutError("timed out"),
                                   RuntimeError("401 Invalid API key"), RuntimeError("relation \"patients\" does not exist"),
                                   ValueError("not JSON")], ids=["unreachable", "timeout", "wrong_key", "tables_missing", "not_json"])
def test_supabase_that_raises_at_startup_falls_back_to_the_demo_store(monkeypatch, error):
    from backend.app import store
    monkeypatch.setenv("DATA_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "https://demo.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "sb_secret_test")
    monkeypatch.setattr(store.SupabaseStore, "__init__", _boom(error))
    st, note = store.make_store()
    try:
        assert st.name == "demo" and note.startswith("Supabase unreachable") and "using demo SQLite" in note
    finally:
        st.conn.close()


def test_app_starts_on_the_demo_store_when_supabase_is_unreachable(tmp_path):
    """A whole fresh server process with DATA_BACKEND=supabase pointing at a closed port on this
    computer: it must start, say why in /api/health, and serve the 7 demo patients."""
    code = (
        "import json, logging\n"
        "logging.disable(logging.CRITICAL)\n"
        "from fastapi.testclient import TestClient\n"
        "from backend.app.main import app\n"
        "with TestClient(app) as c:\n"
        "    h = c.get('/api/health').json()\n"
        "    n = len(c.get('/api/patients').json())\n"
        "    s = c.post('/api/demo/simulate/1', json={}).status_code\n"
        "print('RESULT ' + json.dumps({'backend': h['data_backend'], 'note': h['data_note'], 'patients': n, 'sim': s}))\n")
    env = {**os.environ, "DATA_BACKEND": "supabase", "SUPABASE_URL": "http://127.0.0.1:9",
           "SUPABASE_SERVICE_ROLE_KEY": "sb_secret_test", "SPIROBUDDY_DATA_DIR": str(tmp_path),
           "DEMO_MODE": "1", "DEMO_AUTOPILOT": "0", "COMMS_TICKER": "0", "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=180)
    assert p.returncode == 0, p.stderr[-1500:]
    line = [x for x in p.stdout.splitlines() if x.startswith("RESULT ")][-1]
    res = json.loads(line[7:])
    assert res["backend"] == "demo" and res["patients"] == 7 and res["sim"] == 200
    assert "Supabase unreachable" in res["note"] and "using demo SQLite" in res["note"]


class _BrokenStore:
    """A data store that dies on every call (database gone in the middle of the demo)."""
    name = "supabase"

    def __getattr__(self, item):
        def fail(*a, **k):
            raise ConnectionError("database connection lost")
        return fail


def test_store_dying_mid_run_gives_a_json_error_and_recovers(raw, monkeypatch):
    from backend.app import service
    good = service._store
    n = len(raw.get("/api/patients").json())
    monkeypatch.setattr(service, "_store", _BrokenStore())
    for method, url, body in (("GET", "/api/patients", None), ("GET", "/api/patients/1", None),
                              ("POST", "/api/sessions", {"patient_id": 1, "breaths": []}),
                              ("POST", "/api/summary/1", {}), ("GET", f"{C}/alerts", None),
                              ("GET", f"{C}/guardian/{DEMO_TOKEN}", None),
                              ("POST", f"{C}/wa/reply", {"patient_id": 1, "text": "chest pain"})):
        r = raw.request(method, url, json=body)
        assert r.status_code in (500, 503), f"{url}: {r.status_code}"
        err = r.json()                                       # still our JSON error shape, not a dead connection
        assert err["status"] == r.status_code and "database connection lost" in err["error"]
    assert raw.get("/api/health").status_code == 200           # the health check never needs the database
    assert raw.get("/index.html").status_code == 200           # and the pages still load
    monkeypatch.setattr(service, "_store", good)
    assert len(raw.get("/api/patients").json()) == n            # back as soon as the store is back


@pytest.mark.xfail(strict=True, reason="OPEN (fix before real patients): if the database drops while the server is "
                   "running, requests answer HTTP 500 with the raw Python error text "
                   "(backend/app/main.py server_error returns f'{type(exc).__name__}: {exc}'). It should be a 503 "
                   "with a plain message, must not show internal details to the browser, and a red-flag message "
                   "that arrives during the outage gets no '112' reply.")
def test_store_outage_is_a_503_with_a_plain_message(raw, monkeypatch):
    from backend.app import service
    monkeypatch.setattr(service, "_store", _BrokenStore())
    r = raw.get("/api/patients")
    assert r.status_code == 503 and "ConnectionError" not in r.text


# ----- malformed bodies on every write route

BAD_BODIES = [
    None, [], "x", 5, True, {}, {"patient_id": "abc"}, {"patient_id": None}, {"patient_id": 999999}, {"patient_id": -1},
    {"patient_id": [1]}, {"patient_id": {"a": 1}}, {"patient_id": 1.5}, {"patient_id": True},
    {"patient_id": 99999999999999999999999}, {"patient_id": 1, "breaths": "x"}, {"patient_id": 1, "breaths": [1, "a", None]},
    {"patient_id": 1, "breaths": [{"features": "x"}]}, {"patient_id": 1, "breaths": [{"features": {"peak_ml": "abc"}}]},
    {"patient_id": 1, "breaths": [{"features": {"peak_ml": [1]}}]}, {"patient_id": 1, "breaths": [{"t": "x", "score": "y", "label": 5}]},
    {"patient_id": 1, "started_at": "garbage"}, {"patient_id": 1, "started_at": {"a": 1}}, {"patient_id": 1, "started_at": 1e30},
    {"patient_id": 1, "started_at": -1e30}, {"patient_id": 1, "started_at": "99999999999999999999"},
    {"patient_id": 1, "source": ["x"]},
    {"target_ml": "abc"}, {"target_ml": [1]}, {"target_ml": True}, {"target_ml": "1e400"}, {"target_ml": "nan"},
    {"hold_target_s": "x"}, {"hold_target_s": {"a": 1}}, {"language": 5}, {"language": ["en"]}, {"language": {"a": 1}},
    {"family_phone": {"a": 1}}, {"kind": 5}, {"kind": ["summary"]}, {"to": {"a": 1}}, {"to": 5}, {"quality": ["good"]},
    {"breaths": "abc"}, {"breaths": 1e9}, {"breaths": [1]}, {"label": ["good"]}, {"label": "good", "samples": "x", "features": "y"},
    {"label": "good", "features": {"peak_ml": "x"}}, {"label": "good", "features": [1]}, {"text": 5}, {"text": ["a"]},
    {"text": {"a": 1}}, {"digit": [1]}, {"digit": {"a": 1}}, {"digit": "9"}, {"speed": ["fast"]}, {"speed": "warp"},
    {"missed": "abc"}, {"missed": [1]}, {"by": 5}, {"by": ["x"]}, {"minutes": "abc"}, {"minutes": [5]}, {"minutes": 1e12},
    {"sample": ["pain"]}, {"sample": 5}, {"nurse_name": 5}, {"nurse_name": ["x"]}, {"nurse_phone": {"a": 1}},
    {"patient_id": 1, "role": 5, "text": 5, "payload": 5, "guardian_id": "abc"},
    {"patient_id": 1, "role": "guardian", "text": "hi", "guardian_id": 999999},
    {"patient_id": 1, "role": "guardian", "text": "1", "guardian_id": [1]},
    {"patient_id": 1, "text": "hi", "payload": {"a": 1}}, {"patient_id": 1, "payload": ["done"]},
    {"patient_id": 1, "name": 5}, {"patient_id": 1, "name": ["x"]}, {"patient_id": 1, "name": "x", "phone": {"a": 1}, "language": 5},
    {"patient_id": 1, "name": "x", "language": "hi", "quiet_start": 5}, {"patient_id": 1, "name": "x", "language": "hi", "channel": ["a"]},
    {"name": ""}, {"quiet_start": 5}, {"quiet_start": "25:00"}, {"quiet_start": [1], "quiet_end": {"a": 1}}, {"is_primary": "x"},
    {"to": "family", "guardian_id": "abc"}, {"to": "family", "guardian_id": 999999},
    {"to": "family", "guardian_id": [1]}, {"preset": "abc"}, {"preset": 99}, {"preset": [1]}, {"language": 5, "preset": 0},
    {"patient_phone": {"a": 1}}, {"trigger_missed": "abc"}, {"snooze_min": [1]}, {"ring_s": {"a": 1}}, {"steps": "x"},
    {"steps": [1, {"key": ["x"]}]}, {"steps": [{"key": "device", "delay_min": "abc"}]}, {"steps": [{"key": "device", "delay_min": [1]}]},
    {"call_style": 5}, {"auto": "no"}, {"speaker": 5}, {"speaker": ["x"]}, {"pace": "abc"}, {"pace": [1]},
    {"text": "hi", "language": 5}, {"text": "hi", "pace": "abc", "language": "en"}, {"text": "hi", "target": 5},
    {"text": "x" * 6000}, {"override_quiet": "x"}, {"reason": ["x"]}, {"reason": 5}, {"reason": {"a": 1}},
]
RAW_BODIES = [b"{bad json", b"", b"\xff\xfe\x00", b"null", b"[", b'{"a":', b"NaN", b'{"patient_id": NaN}', b'{"target_ml": Infinity}',
              b'{"target_ml": NaN}', b'{"breaths": Infinity}', b'{"missed": NaN}', b'{"pace": NaN}']
WRITE_ROUTES = [
    ("PUT", "/api/patients/1"), ("POST", "/api/classify"), ("POST", "/api/sessions"), ("POST", "/api/collect"),
    ("POST", "/api/summary/1"), ("POST", "/api/whatsapp/1"), ("POST", "/api/demo/simulate/1"), ("POST", "/api/demo/miss/1"),
    ("POST", f"{C}/alerts/ALERT/ack"), ("POST", f"{C}/alerts/ALERT/snooze"), ("POST", f"{C}/alerts/ALERT/assign"),
    ("POST", f"{C}/alerts/ALERT/resolve"), ("POST", f"{C}/alerts/ALERT/bogus"), ("POST", f"{C}/escalations/start/1"),
    ("POST", f"{C}/escalations/1/stop"), ("POST", f"{C}/escalations/1/advance"), ("POST", f"{C}/demo/ladder/1"),
    ("POST", f"{C}/demo/red-flag/1"), ("POST", f"{C}/demo/trend/1"), ("POST", f"{C}/calls/CALL/answer"),
    ("POST", f"{C}/calls/CALL/press"), ("POST", f"{C}/calls/CALL/agent-turn"), ("POST", f"{C}/calls/CALL/hangup"),
    ("POST", f"{C}/call-patient/1"), ("POST", f"{C}/checkin-call/1"), ("POST", f"{C}/webhooks/sarvam"),
    ("POST", f"{C}/demo/sarvam-replay/1"), ("POST", f"{C}/call-script/1"), ("POST", f"{C}/wa/reply"),
    ("POST", f"{C}/weekly-card/1"), ("POST", f"{C}/voice-note/1"), ("PUT", f"{C}/care/1"), ("POST", f"{C}/guardians"),
    ("PUT", f"{C}/guardians/GUARDIAN"), ("POST", f"{C}/consent/ask/1"), ("POST", f"{C}/guardian/TOKEN/cheer"),
    ("PUT", f"{C}/guardian/TOKEN/quiet"), ("POST", f"{C}/guardian/TOKEN/call-log"),
    ("POST", f"{C}/cheers/1/played"), ("POST", f"{C}/tick"), ("PUT", "/api/voice/prefs/1"), ("POST", "/api/voice/tts"),
    ("POST", "/api/voice/translate"), ("POST", "/api/voice/detect"), ("POST", "/api/voice/summary-audio/1"),
]


@pytest.mark.parametrize("method,route", WRITE_ROUTES, ids=[f"{m} {r}" for m, r in WRITE_ROUTES])
def test_malformed_bodies_are_4xx_never_500(raw, method, route):
    """Every write route x about 150 broken bodies (wrong types, missing fields, broken JSON)."""
    if "CALL" in route:
        calls = raw.get(f"{C}/calls?limit=1").json()
        if not calls:
            raw.post(f"{C}/demo/ladder/1", json={"override_quiet": True})
            calls = raw.get(f"{C}/calls?limit=1").json()
        route = route.replace("CALL", str(calls[0]["id"] if calls else 1))
    guardians = raw.get(f"{C}/care/1").json()["guardians"]
    alerts = raw.get(f"{C}/alerts?status=all&limit=1").json()
    route = (route.replace("GUARDIAN", str(guardians[0]["id"])).replace("TOKEN", guardians[0]["token"])
             .replace("ALERT", str(alerts[0]["id"] if alerts else 1)))
    crashed = []

    def is_crash(r):
        # 503 + fallback:"browser" is the designed "no voice key, the browser speaks" answer, not a crash
        return r.status_code >= 500 and not (r.status_code == 503 and '"fallback":"browser"' in r.text)
    for body in BAD_BODIES:
        r = raw.request(method, route, content=json.dumps(body), headers={"Content-Type": "application/json"})
        if is_crash(r):
            crashed.append((json.dumps(body)[:90], r.status_code, r.text[:140]))
    for blob in RAW_BODIES:
        r = raw.request(method, route, content=blob, headers={"Content-Type": "application/json"})
        if is_crash(r):
            crashed.append((repr(blob), r.status_code, r.text[:140]))
    for ctype in ("text/plain", "application/xml", "application/x-www-form-urlencoded", "multipart/form-data; boundary=x"):
        r = raw.request(method, route, content=b"a=b&c=d", headers={"Content-Type": ctype})
        if is_crash(r):
            crashed.append((ctype, r.status_code, r.text[:140]))
    assert not crashed, f"{len(crashed)} server errors, first ones: {crashed[:6]}"


def test_demo_data_resets_cleanly_after_the_malformed_body_storm(fresh):
    pts = fresh.get("/api/patients").json()
    assert len(pts) == 7 and {"red", "yellow", "green"} <= {p["status"] for p in pts}
    assert fresh.get("/api/patients/1").json()["name"] == "Ravi Kumar"
    assert fresh.get(f"{C}/guardian/{DEMO_TOKEN}").status_code == 200
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is True


def test_bad_numbers_in_a_session_never_store_half_a_session(raw):
    before = _st().count("sessions"), _st().count("breaths")
    good = {"features": {"peak_ml": 1500, "hold_s": 3, "max_rise_ml_s": 600, "pct_target": 0.75}}
    for body in ({"patient_id": 1, "breaths": [good, {"features": {"peak_ml": "abc"}}]},
                 {"patient_id": 1, "breaths": [good, "junk"]},
                 {"patient_id": 1, "breaths": [good, {"features": [1, 2]}]},
                 {"patient_id": 1, "started_at": "yesterday-ish", "breaths": [good]},
                 {"patient_id": 1, "started_at": 1e30, "breaths": [good]},
                 {"patient_id": "one", "breaths": [good]}):
        r = raw.post("/api/sessions", json=body)
        assert r.status_code == 400, f"{body}: {r.status_code} {r.text[:150]}"
    assert (_st().count("sessions"), _st().count("breaths")) == before


# ============================================================================= 4. LOAD

N_PATIENTS, SESSIONS_EACH, BREATHS_EACH = 50, 4, 6
LOAD_NUMBERS = {}


def _add_fake_patients(total):
    from backend.app.config import iso, now_local
    have = [p["id"] for p in _st().select("patients", order="id", columns="id")]
    rows = [{"name": f"Load Test Patient {i:02d}", "age": 40 + i % 30, "sex": "MF"[i % 2], "surgery": "Demo surgery (fake)",
             "surgery_date": "2026-10-01", "language": ("en", "hi", "ta", "ml")[i % 4], "target_ml": 1500 + 50 * (i % 10),
             "hold_target_s": 3, "family_phone": None, "nurse_phone": None, "personal_best_ml": 0,
             "created_at": iso(now_local())} for i in range(total - len(have))]
    _st().insert("patients", rows)
    ids = [p["id"] for p in _st().select("patients", order="id", columns="id")]
    return ids, [i for i in ids if i not in have]


def test_fifty_patients_posting_sessions_at_the_same_time(raw):
    ids, new_ids = _add_fake_patients(N_PATIENTS)
    assert len(ids) == N_PATIENTS and len(new_ids) >= 40
    before_s = {pid: len(_st().select("sessions", [("patient_id", "eq", pid)], columns="id")) for pid in ids}
    before_b = _st().count("breaths")
    results, read_times, errors = [], [], []
    lock = threading.Lock()
    start_gate = threading.Barrier(N_PATIENTS + 5)
    stop_readers = threading.Event()

    def writer(pid):
        start_gate.wait(timeout=60)
        for n in range(SESSIONS_EACH):
            peak = 1000 + pid * 10 + n * 100
            body = {"patient_id": pid, "source": "device",
                    "breaths": [{"features": {"peak_ml": peak - i, "pct_target": 0.8, "time_to_peak_s": 3.0,
                                              "mean_rise_ml_s": 500, "max_rise_ml_s": 700, "hold_s": 3.1,
                                              "smoothness": 0.4, "duration_s": 8.0}} for i in range(BREATHS_EACH)]}
            t0 = time.perf_counter()
            try:
                r = raw.post("/api/sessions", json=body)
                with lock:
                    results.append((pid, r.status_code, r.text if r.status_code != 200 else r.json()["session_id"],
                                    time.perf_counter() - t0))
            except Exception as e:                           # a dropped connection counts as a failure too
                with lock:
                    errors.append(f"writer {pid}: {type(e).__name__}: {e}")

    def reader(i):
        start_gate.wait(timeout=60)
        urls = ("/api/patients", f"/api/patients/{ids[i]}", f"{C}/alerts", f"{C}/alerts/counts", f"/api/patients/{ids[-1 - i]}/sessions")
        while not stop_readers.is_set():
            for u in urls:
                t0 = time.perf_counter()
                try:
                    r = raw.get(u)
                    with lock:
                        if u == "/api/patients":
                            read_times.append(time.perf_counter() - t0)
                        if r.status_code != 200:
                            errors.append(f"reader {u}: {r.status_code} {r.text[:120]}")
                except Exception as e:
                    with lock:
                        errors.append(f"reader {u}: {type(e).__name__}: {e}")

    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=N_PATIENTS + 5) as pool:
        readers = [pool.submit(reader, i) for i in range(5)]
        writers = [pool.submit(writer, pid) for pid in ids]
        for w in writers:
            w.result(timeout=300)
        stop_readers.set()
        for rd in readers:
            rd.result(timeout=60)
    wall = time.perf_counter() - t_start

    expected = N_PATIENTS * SESSIONS_EACH
    assert not errors, errors[:5]
    bad = [(pid, code, str(body)[:200]) for pid, code, body, _ in results if code != 200]
    assert not bad, f"{len(bad)} failed writes, e.g. {bad[:3]}"
    assert len(results) == expected
    assert not any("locked" in str(body).lower() for _, _, body, _ in results)
    session_ids = [body for _, _, body, _ in results]
    assert len(set(session_ids)) == expected, "two writes got the same session id"
    # no lost writes: every patient has exactly 4 more sessions, every session has its 6 breaths
    for pid in ids:
        rows = _st().select("sessions", [("patient_id", "eq", pid)], columns="id")
        assert len(rows) == before_s[pid] + SESSIONS_EACH, f"patient {pid}: {len(rows) - before_s[pid]} of {SESSIONS_EACH} sessions stored"
    assert _st().count("breaths") == before_b + expected * BREATHS_EACH
    per_session = {}
    for b in _st().select("breaths", [("session_id", "in", session_ids)], columns="session_id"):
        per_session[b["session_id"]] = per_session.get(b["session_id"], 0) + 1
    assert set(per_session) == set(session_ids) and set(per_session.values()) == {BREATHS_EACH}
    # the personal best is the highest breath ever posted
    for p in _st().select("patients", [("id", "in", new_ids)]):
        assert p["personal_best_ml"] == 1000 + p["id"] * 10 + (SESSIONS_EACH - 1) * 100, p
    # the dashboard still answers, with all 50 patients
    after = []
    for _ in range(7):
        t0 = time.perf_counter()
        r = raw.get("/api/patients")
        after.append(time.perf_counter() - t0)
        assert r.status_code == 200 and len(r.json()) == N_PATIENTS
    write_times = sorted(t for *_, t in results)
    LOAD_NUMBERS.update({
        "patients": N_PATIENTS, "writes": expected, "breaths_written": expected * BREATHS_EACH, "wall_s": round(wall, 2),
        "writes_per_s": round(expected / wall, 1), "write_median_ms": round(statistics.median(write_times) * 1000),
        "write_p95_ms": round(write_times[int(len(write_times) * 0.95) - 1] * 1000), "write_max_ms": round(write_times[-1] * 1000),
        "list_during_load_n": len(read_times),
        "list_during_load_median_ms": round(statistics.median(read_times) * 1000) if read_times else None,
        "list_during_load_max_ms": round(max(read_times) * 1000) if read_times else None,
        "list_after_median_ms": round(statistics.median(after) * 1000), "list_after_max_ms": round(max(after) * 1000)})
    print("\nLOAD NUMBERS " + json.dumps(LOAD_NUMBERS))
    # deliberately loose (a laptop demo; shared test machines are slow): only catch a real hang
    assert statistics.median(after) < 10, f"GET /api/patients took {statistics.median(after):.1f}s with 50 patients"
    assert wall < 240
    # the demo reset puts everything back
    assert raw.post("/api/demo/reset").json()["patients"] == 7
    assert len(raw.get("/api/patients").json()) == 7


def test_two_sessions_arriving_together_never_lower_the_personal_best(raw):
    """Lost update: both requests read the patient before either saved (same stale copy)."""
    from backend.app import service

    def breath(peak):
        return {"features": {"peak_ml": peak, "hold_s": 3, "max_rise_ml_s": 600, "pct_target": 0.9}}
    stale = service.get_patient_row(2)
    top = float(stale["personal_best_ml"]) + 900
    service.record_session(dict(stale), None, [breath(top)], source="device")
    service.record_session(dict(stale), None, [breath(top - 400)], source="device")      # was: best dropped to top-400
    assert float(service.get_patient_row(2)["personal_best_ml"]) == top


def test_same_patient_hammered_from_twenty_threads_keeps_every_write(raw):
    before = len(_st().select("sessions", [("patient_id", "eq", 3)], columns="id"))
    base = float(_st().select("patients", [("id", "eq", 3)])[0]["personal_best_ml"]) + 1000
    codes = []

    def post(i):
        r = raw.post("/api/sessions", json={"patient_id": 3, "breaths": [{"features": {"peak_ml": base + i}}]})
        codes.append(r.status_code)
        return raw.post(f"{C}/wa/reply", json={"patient_id": 3, "role": "patient", "text": "status"}).status_code
    with ThreadPoolExecutor(max_workers=20) as pool:
        replies = list(pool.map(post, range(60)))
    assert codes == [200] * 60 and replies == [200] * 60
    assert len(_st().select("sessions", [("patient_id", "eq", 3)], columns="id")) == before + 60
    assert float(_st().select("patients", [("id", "eq", 3)])[0]["personal_best_ml"]) == base + 59   # highest one wins
    today = [s for s in raw.get("/api/patients/3").json()["today"] if s["status"] == "done"]
    assert len({s["hour"] for s in today}) == len(today)      # one tick per hour slot, no duplicates
