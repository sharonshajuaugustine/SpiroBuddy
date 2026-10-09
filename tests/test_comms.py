"""Comms tests (escalation ladder, IVR, quiet hours, consent, Sarvam webhook, WhatsApp inbound,
guardian page, demo replay). No keys, temporary data folder (tests/conftest.py)."""
import os
from datetime import timedelta

import pytest

# No background ticker or clock-driven auto-ladders during tests: every step is driven explicitly.
os.environ["COMMS_TICKER"] = "0"
os.environ["COMMS_AUTO_ESCALATE"] = "0"

C = "/api/comms"


# ----------------------------------------------------------------------------- helpers

def _events(client, pid=1, limit=200):
    return client.get(f"{C}/timeline/{pid}?limit={limit}").json()


def _run_events(client, rid, pid=1):
    return [e for e in _events(client, pid) if e["run_id"] == rid]


def _start_fast(client, pid=1):
    r = client.post(f"{C}/demo/ladder/{pid}", json={"override_quiet": True})
    assert r.status_code == 200, r.text
    run = r.json()
    assert run["status"] == "active" and run["speed"] == "fast"
    assert run["steps"][0]["key"] == "device" and run["steps"][0]["state"] == "done"
    return run


def _advance(client, rid):
    r = client.post(f"{C}/escalations/{rid}/advance")
    assert r.status_code == 200, r.text
    return r.json()


def _ringing_call(client, pid=1, role="patient"):
    calls = client.get(f"{C}/calls?patient_id={pid}&active=1").json()
    mine = [c for c in calls if c["to_role"] == role and c["status"] == "ringing"]
    assert mine, calls
    return mine[0]


def _sarvam_env(monkeypatch, secret="s3cret"):
    for k, v in {"SARVAM_AGENT_API_KEY": "test-key", "SARVAM_ORG_ID": "org1",
                 "SARVAM_WORKSPACE_ID": "ws1", "SARVAM_AGENT_ID": "app1",
                 "SARVAM_CONNECTION_ID": "conn1", "SARVAM_AGENT_NUMBER": "+918045550000",
                 "PUBLIC_BASE_URL": "https://spirobuddy.example.com",
                 "SARVAM_WEBHOOK_SECRET": secret, "DEMO_PATIENT_PHONE": "+919800000002",
                 "CALL_PROVIDER": "auto"}.items():
        monkeypatch.setenv(k, v)


# ----------------------------------------------------------------------------- ladder

def test_ladder_fast_forward_reaches_nurse(fresh):
    run = _start_fast(fresh)
    rid = run["id"]
    for _ in range(4):                       # whatsapp -> call -> guardian -> nurse
        run = _advance(fresh, rid)
    assert run["status"] == "completed"
    assert [s["state"] for s in run["steps"]] == ["done"] * 5
    kinds = {e["kind"] for e in _run_events(fresh, rid)}
    assert {"start", "device_beep", "whatsapp", "call", "guardian_whatsapp", "guardian_call",
            "nurse_alert"} <= kinds
    alerts = fresh.get(f"{C}/alerts?patient_id=1").json()
    assert any(a["run_id"] == rid and a["severity"] == "red" for a in alerts)


def test_every_automated_message_and_call_discloses_ai(fresh):
    run = _start_fast(fresh)
    _advance(fresh, run["id"])               # WhatsApp reminder
    _advance(fresh, run["id"])               # automated call
    thread = fresh.get(f"{C}/wa/thread/1?role=patient").json()
    reminder = [m for m in thread["items"] if m["kind"] == "reminder"][-1]
    assert "स्वचालित देखभाल सहायक" in reminder["text"]          # Ravi speaks Hindi
    call = _ringing_call(fresh)
    assert "स्वचालित देखभाल सहायक" in call["script"]
    # replies get the short tag
    r = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": "status"}).json()
    thread = fresh.get(f"{C}/wa/thread/1?role=patient").json()
    assert any(m["kind"] == "reply" and m["text"].startswith("🤖 SpiroBuddy") for m in thread["items"])
    assert r["intent"] == "status"


# ----------------------------------------------------------------------------- IVR keypresses

@pytest.mark.parametrize("digit,expect", [("1", "resolved"), ("3", "resolved"), ("2", "active")])
def test_ivr_press(fresh, digit, expect):
    run = _start_fast(fresh)
    _advance(fresh, run["id"])
    _advance(fresh, run["id"])               # patient call rings in the simulator
    call = _ringing_call(fresh)
    assert call["simulated"] and call["style"] == "ivr"
    assert fresh.post(f"{C}/calls/{call['id']}/answer").json()["status"] == "in-progress"
    res = fresh.post(f"{C}/calls/{call['id']}/press", json={"digit": digit}).json()
    assert res["end"] is True and res["say"]
    run = fresh.get(f"{C}/escalations?patient_id=1").json()[0]
    assert run["status"] == expect
    if digit == "1":
        assert run["outcome"] == "patient_done"
    if digit == "2":
        assert run["snoozes"] == 1 and run["steps"][2]["state"] == "next"
    if digit == "3":
        alerts = fresh.get(f"{C}/alerts?patient_id=1").json()
        assert any(a["kind"] == "callback" for a in alerts)


def test_press_rejects_bad_digit(client):
    assert client.post(f"{C}/calls/1/press", json={"digit": "9"}).status_code == 400


# ----------------------------------------------------------------------------- quiet hours

def test_quiet_hours_hold_but_red_flag_goes_through(fresh):
    from backend.app.config import now_local
    t = now_local()
    qs, qe = (t - timedelta(hours=1)).strftime("%H:%M"), (t + timedelta(hours=1)).strftime("%H:%M")
    assert fresh.put(f"{C}/care/1", json={"quiet_start": qs, "quiet_end": qe}).status_code == 200
    run = fresh.post(f"{C}/escalations/start/1", json={"speed": "real", "reason": "manual"}).json()
    assert run["status"] == "active" and run["held_until"]
    assert run["steps"][0]["state"] == "held"
    assert any(e["kind"] == "quiet_hold" for e in _run_events(fresh, run["id"]))
    # red-flag words ignore quiet hours: family is told straight away
    r = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient",
                                          "text": "I have chest pain"}).json()
    assert r["intent"] == "red_flag"
    red = fresh.get(f"{C}/escalations?patient_id=1").json()[0]
    assert red["red_flag"] and red["steps"][0]["key"] == "guardian" and red["steps"][0]["state"] == "done"


def test_quiet_hours_validation(client):
    assert client.put(f"{C}/care/1", json={"quiet_start": "25:00"}).status_code == 400


# ----------------------------------------------------------------------------- consent

def test_consent_needs_flag_and_date():
    from backend.app.comms.common import has_consent
    assert not has_consent({"consent": True, "consent_at": None})
    assert not has_consent({"consent": False, "consent_at": "2026-10-09T10:00:00+05:30"})
    assert has_consent({"consent": True, "consent_at": "2026-10-09T10:00:00+05:30"})


def test_no_consent_blocks_automated_calls_and_messages(fresh):
    s = fresh.put(f"{C}/care/1", json={"consent": False}).json()["settings"]
    assert s["consent"] is False and s["consent_at"] is None and s["consent_ok"] is False
    assert fresh.post(f"{C}/checkin-call/1").status_code == 409
    run = _start_fast(fresh)
    _advance(fresh, run["id"])
    _advance(fresh, run["id"])
    evs = _run_events(fresh, run["id"])
    assert any(e["kind"] == "whatsapp" and e["status"] == "skipped" for e in evs)
    assert any(e["kind"] == "call" and e["status"] == "skipped" for e in evs)
    assert not [c for c in fresh.get(f"{C}/calls?patient_id=1&active=1").json() if c["to_role"] == "patient"]
    # recording consent stores today's date
    s = fresh.put(f"{C}/care/1", json={"consent": True}).json()["settings"]
    assert s["consent_ok"] and s["consent_at"] and s["consent_renew_due"] is False


def test_guardian_without_consent_is_skipped(fresh):
    g = fresh.get(f"{C}/care/1").json()["guardians"]
    for x in g:
        fresh.put(f"{C}/guardians/{x['id']}", json={"consent": False})
    run = _start_fast(fresh)
    for _ in range(3):
        _advance(fresh, run["id"])
    evs = _run_events(fresh, run["id"])
    assert any(e["kind"] == "guardian_whatsapp" and e["status"] == "skipped" for e in evs)
    assert not any(e["kind"] == "guardian_call" for e in evs)


# ----------------------------------------------------------------------------- Sarvam webhook

def _sample(name):
    from backend.app.comms import sarvam
    import json
    return json.loads(json.dumps(sarvam.load_samples()[name]["payload"]))


def test_normalise_pain_needs_review():
    from backend.app.comms import sarvam
    n = sarvam.normalise(_sample("pain"))
    assert n["provider"] == "sarvam" and n["status"] == "completed"
    assert n["outcome"] == "needs_nurse_review" and n["reason_category"] == "pain"
    assert n["red_flag"] is False and n["callback_requested"] is True
    assert n["patient_words"].startswith("I had mild pain near the incision")
    assert n["neutral_note"].startswith("Patient reported") and n["neutral_note"].endswith("Nurse review requested.")
    assert n["transcript_reference"] == "20261009/demo-ravi-pain"
    assert set(n) >= {"provider", "status", "outcome", "reason_category", "patient_words",
                      "neutral_note", "red_flag", "callback_requested", "transcript_reference"}


def test_red_flag_is_our_rule_not_the_providers():
    from backend.app.comms import sarvam
    p = _sample("fine")
    p["final_agent_variables"].update({"red_flag": "true", "outcome": "red_flag",
                                       "reason_category": "breathing"})
    n = sarvam.normalise(p)                       # provider claims a red flag; the words don't
    assert n["red_flag"] is False and n["outcome"] == "ok"
    p = _sample("fine")
    p["final_agent_variables"]["patient_words"] = "I can't breathe properly"
    n = sarvam.normalise(p)                       # provider says 'forgot'; the words are red
    assert n["red_flag"] is True and n["outcome"] == "red_flag"
    assert n["red_flag_rule"] == "voice.red_flag word list"
    n = sarvam.normalise(_sample("red_flag"))
    assert n["red_flag"] and n["possible_distress"]           # sentiment only a soft hint
    n = sarvam.normalise(_sample("no_answer"))
    assert n["outcome"] == "no_answer" and n["status"] == "no-answer"


def test_sarvam_call_request_and_webhook(fresh, monkeypatch):
    from backend.app.comms import sarvam
    _sarvam_env(monkeypatch)
    sent = {}

    def fake_post(url, body):
        sent["url"], sent["body"] = url, body
        return {"attempt_id": "att-123"}
    monkeypatch.setattr(sarvam, "_post", fake_post)
    assert fresh.get(f"{C}/status").json()["checkin_provider"] == "sarvam_agent"
    call = fresh.post(f"{C}/checkin-call/1").json()
    assert call["provider"] == "sarvam_agent" and call["style"] == "agent"
    assert call["result"]["pending"] is True
    assert sent["url"] == ("https://apps.sarvam.ai/api/outbounds/v1/orgs/org1/workspaces/ws1/outbounds")
    app = sent["body"]["app_config"]
    assert app["app_id"] == "app1" and app["connection_config"] == {
        "connection_id": "conn1", "agent_phone_number": "+918045550000"}
    assert set(app["agent_variables"]) == {"patient_id", "patient_name", "language",
                                           "missed_slots", "callback_number"}
    assert app["agent_variables"]["patient_name"] == "Ravi"
    assert app["app_overrides"]["initial_language_name"] == "Hindi"
    assert sent["body"]["user_config"] == {"user_phone_number": "+919800000002"}
    wh = sent["body"]["webhook_config"]
    assert wh["url"] == "https://spirobuddy.example.com/api/comms/webhooks/sarvam?token=s3cret"
    assert wh["metadata"]["call_id"] == call["id"]

    payload = _sample("pain")
    payload["attempt_id"] = "att-123"
    assert fresh.post(f"{C}/webhooks/sarvam?token=wrong", json=payload).status_code == 403
    assert fresh.post(f"{C}/webhooks/sarvam", json=payload).status_code == 403
    r = fresh.post(f"{C}/webhooks/sarvam?token=s3cret", json=payload).json()
    assert r["ok"] and r["duplicate"] is False and r["result"]["outcome"] == "needs_nurse_review"
    again = fresh.post(f"{C}/webhooks/sarvam?token=s3cret", json=payload).json()
    assert again["duplicate"] is True                       # idempotent
    alerts = [a for a in fresh.get(f"{C}/alerts?patient_id=1").json() if a["kind"] == "call_review"]
    assert len(alerts) == 1 and "Nurse review requested" in alerts[0]["detail"]
    c = fresh.get(f"{C}/calls/{call['id']}").json()
    assert c["status"] == "completed" and c["result"]["pending"] is False
    unknown = dict(payload, attempt_id="not-ours", webhook_config=None)
    assert fresh.post(f"{C}/webhooks/sarvam?token=s3cret", json=unknown).status_code == 404


def test_sarvam_failure_falls_back_to_simulator(fresh, monkeypatch):
    from backend.app.comms import sarvam
    _sarvam_env(monkeypatch)

    def boom(url, body):
        raise RuntimeError("Sarvam 402: no credits")
    monkeypatch.setattr(sarvam, "_post", boom)
    call = fresh.post(f"{C}/checkin-call/1").json()
    assert call["provider"] == "dry_run" and call["status"] == "ringing" and call["style"] == "agent"


def test_simulated_conversation_same_outcome(fresh):
    call = fresh.post(f"{C}/checkin-call/1").json()
    assert call["provider"] == "dry_run" and call["answers"]
    fresh.post(f"{C}/calls/{call['id']}/answer")
    assert fresh.post(f"{C}/calls/{call['id']}/press", json={"digit": "1"}).status_code == 400
    t1 = fresh.post(f"{C}/calls/{call['id']}/agent-turn",
                    json={"text": "आज सुबह टांकों के पास हल्का दर्द था।", "source": "voice"}).json()
    assert t1["end"] is False and t1["answers"]
    t2 = fresh.post(f"{C}/calls/{call['id']}/agent-turn", json={"text": "हाँ, कॉल कीजिए।"}).json()
    assert t2["end"] is True
    assert t2["result"]["outcome"] == "needs_nurse_review" and t2["result"]["callback_requested"]
    # red flag on the first answer ends the call with the fixed message
    call = fresh.post(f"{C}/checkin-call/2").json()
    fresh.post(f"{C}/calls/{call['id']}/answer")
    t = fresh.post(f"{C}/calls/{call['id']}/agent-turn", json={"text": "I can't breathe properly"}).json()
    assert t["end"] and t["result"]["outcome"] == "red_flag" and "112" in t["say"]


# ----------------------------------------------------------------------------- demo replay

@pytest.mark.parametrize("sample,outcome", [("pain", "needs_nurse_review"), ("red_flag", "red_flag"),
                                            ("fine", "ok"), ("no_answer", "no_answer")])
def test_replay(fresh, sample, outcome):
    r = fresh.post(f"{C}/demo/sarvam-replay/1", json={"sample": sample})
    assert r.status_code == 200, r.text
    assert r.json()["result"]["outcome"] == outcome
    if outcome == "red_flag":
        assert any(a["kind"] == "red_flag" for a in fresh.get(f"{C}/alerts?patient_id=1").json())


def test_replay_bad_sample(client):
    assert client.post(f"{C}/demo/sarvam-replay/1", json={"sample": "nope"}).status_code == 400
    assert {s["key"] for s in client.get(f"{C}/demo/sarvam-samples").json()} >= {"pain", "red_flag"}


# ----------------------------------------------------------------------------- WhatsApp inbound

@pytest.mark.parametrize("text,intent", [("1", "done"), ("done", "done"), ("status", "status"),
                                         ("स्थिति", "status"), ("help", "red_flag"), ("2", "snooze")])
def test_whatsapp_patient_keywords(fresh, text, intent):
    r = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": text}).json()
    assert r["intent"] == intent and r["reply"]


def test_whatsapp_webhook_identifies_guardian(fresh, monkeypatch):
    monkeypatch.setenv("DEMO_GUARDIAN_PHONE", "+919800000001")
    r = fresh.post(f"{C}/webhooks/whatsapp", data={"From": "whatsapp:+919800000001", "Body": "स्थिति"})
    assert r.status_code == 200 and "<Response" in r.text
    th = fresh.get(f"{C}/wa/thread/1?role=guardian").json()
    assert any(m["dir"] == "in" and m["intent"] == "status" for m in th["items"])


def test_whatsapp_rate_limit(monkeypatch):
    from backend.app import whatsapp
    assert whatsapp.MIN_GAP_S >= 3
    slept = []
    monkeypatch.setattr(whatsapp.time, "sleep", lambda s: slept.append(s))
    whatsapp.throttle()
    whatsapp.throttle()
    assert slept and slept[-1] > 2.5


def test_sandbox_hint():
    from backend.app.comms import messages
    assert "rejoin" in messages.error_hint("Error 63015: sandbox participant").lower()


# ----------------------------------------------------------------------------- guardian page

def test_guardian_token_page(fresh):
    g = fresh.get(f"{C}/care/1").json()["guardians"][0]
    v = fresh.get(f"{C}/guardian/{g['token']}").json()
    assert v["patient"]["first_name"] == "Ravi" and v["status"] in ("good", "nudge", "call")
    assert len(v["cheer_presets"]) == 3 and "today" in v and "call" in v
    c = fresh.post(f"{C}/guardian/{g['token']}/cheer", json={"preset": 1}).json()
    assert c["ok"] and c["cheer_id"]
    assert fresh.post(f"{C}/guardian/{g['token']}/call-log").json()["ok"]
    assert fresh.get(f"{C}/guardian/not-a-real-token").status_code == 404
    new = fresh.put(f"{C}/guardians/{g['id']}", json={"new_link": True}).json()
    assert new["token"] != g["token"]
    assert fresh.get(f"{C}/guardian/{g['token']}").status_code == 404


# ----------------------------------------------------------------------------- misc endpoints

def test_status_script_trend_card(fresh):
    st = fresh.get(f"{C}/status").json()
    assert st["calls_provider"] == "dry_run" and st["checkin_provider"] == "dry_run"
    s = fresh.post(f"{C}/call-script/1").json()
    assert s["source"] == "template" and "•" in s["text"]
    assert "flag" in fresh.get(f"{C}/trend/1").json()
    png = fresh.get(f"{C}/card/1.png?lang=hi")
    assert png.status_code == 200 and png.content[:4] == b"\x89PNG"
    cp = fresh.post(f"{C}/call-patient/1", json={"nurse_name": "Sister Anjali"}).json()
    assert cp["dry_run"] is True
    a = fresh.get(f"{C}/alerts").json()[0]
    for act in ("ack", "snooze", "assign", "resolve", "reopen"):
        assert fresh.post(f"{C}/alerts/{a['id']}/{act}", json={"by": "Sister Anjali"}).status_code == 200


# ----------------------------------------------------------------------------- round 3: TRAI / DPDP

def _age_patient_consent(days, pid=1):
    from backend.app.comms import guardians
    from backend.app.comms.common import st
    from backend.app.config import iso, now_local
    cfg = guardians.get_settings(pid)
    cfg["consent_at"] = iso(now_local() - timedelta(days=days))
    st().upsert("care_settings", [{"patient_id": pid, "config": cfg, "updated_at": iso(now_local())}])


def test_default_quiet_hours_are_21_to_07(client, monkeypatch):
    from backend.app.comms.common import default_quiet
    monkeypatch.delenv("QUIET_HOURS", raising=False)
    assert default_quiet() == ("21:00", "07:00")


def test_lapsed_consent_blocks_real_calls(fresh, monkeypatch):
    from backend.app.comms import sarvam
    _sarvam_env(monkeypatch)
    monkeypatch.setattr(sarvam, "_post", lambda url, body: pytest.fail("real call placed with lapsed consent"))
    _age_patient_consent(8)
    s = fresh.get(f"{C}/care/1").json()["settings"]
    assert s["consent_ok"] and s["consent_renew_due"]
    call = fresh.post(f"{C}/checkin-call/1").json()
    assert call["provider"] == "dry_run" and "7 days" in call["note"]


def test_weekly_renewal_yes_and_stop(fresh):
    _age_patient_consent(6)
    from backend.app.comms import consent
    consent.weekly_check()            # sends nothing during quiet hours, so also ask directly
    r = fresh.post(f"{C}/consent/ask/1", json={"to": "patient"}).json()
    assert r["buttons"] and "SpiroBuddy" in r["text"]
    th = fresh.get(f"{C}/wa/thread/1?role=patient").json()
    ask = [m for m in th["items"] if m["kind"] == "consent_renewal"][-1]
    assert [b["payload"] for b in ask["buttons"]] == ["consent_yes", "stop"]
    yes = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": "1"}).json()
    assert yes["intent"] == "consent_yes"
    s = fresh.get(f"{C}/care/1").json()["settings"]
    assert s["consent_ok"] and s["consent_age_days"] == 0
    stop = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "patient", "text": "STOP"}).json()
    assert stop["intent"] == "stop"
    assert fresh.get(f"{C}/care/1").json()["settings"]["consent_ok"] is False
    assert fresh.post(f"{C}/checkin-call/1").status_code == 409


@pytest.mark.parametrize("word", ["stop", "रोको", "நிறுத்து"])
def test_stop_word_any_language(fresh, word):
    r = fresh.post(f"{C}/wa/reply", json={"patient_id": 1, "role": "guardian", "text": word}).json()
    assert r["intent"] == "stop"
    g = fresh.get(f"{C}/care/1").json()["guardians"][0]
    assert g["consent_ok"] is False


def test_consent_text_itemised_in_language(client):
    r = client.get(f"{C}/consent-text/1?lang=hi").json()
    assert r["language"] == "hi" and len(r["items"]) == 5 and "STOP" in r["text"]
    assert all(item in r["text"] for item in r["items"]) and r["valid_days"] == 7
    assert client.get(f"{C}/consent-text/1?lang=en").json()["text"].startswith("I agree")


def test_guardian_sets_own_quiet_hours(fresh):
    g = fresh.get(f"{C}/care/1").json()["guardians"][0]
    v = fresh.get(f"{C}/guardian/{g['token']}").json()
    assert v["quiet"]["presets"][0] == ["21:00", "07:00"]
    assert fresh.put(f"{C}/guardian/{g['token']}/quiet",
                     json={"quiet_start": "22:00", "quiet_end": "07:00"}).json()["ok"]
    v = fresh.get(f"{C}/guardian/{g['token']}").json()
    assert v["quiet"] == {**v["quiet"], "start": "22:00", "end": "07:00", "own": True}
    assert fresh.put(f"{C}/guardian/{g['token']}/quiet", json={"quiet_start": "9pm"}).status_code == 400


def test_guardian_abroad_number(fresh):
    from backend.app.comms.common import e164
    assert e164("+44 7700 900123") == "+447700900123" and e164("+971 50 123 4567") == "+971501234567"
    g = fresh.post(f"{C}/guardians", json={"patient_id": 1, "name": "Ravi Jr", "relation": "son",
                                           "phone": "+44 7700 900123", "language": "en",
                                           "consent": True}).json()
    assert g["phone"] == "+44 7700 900123" and g["consent_ok"]
    assert len(fresh.get(f"{C}/care/1").json()["guardians"]) >= 3
