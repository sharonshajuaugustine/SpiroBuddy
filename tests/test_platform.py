"""Platform pieces of SpiroBuddy 2.0: the feature status registry, the Gemini wrapper with its
limits and consent gate, the AI register, file storage and the summary provider order.

Nothing here talks to a real service: ai_gemini._call_model, the google-genai client and the
Supabase Storage request function are always replaced by fakes.
"""
import io
import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]

# Test-only ids, far away from the seeded ones.
HID, PID_YES, PID_NO, PID_NONE, PID_GONE = 9100, 9101, 9102, 9103, 9104
FAKE_KEY = "test-gemini-key-not-real"
PNG_MARK = b"SECRET-BYTES-MARKER"
FAKE_FILE = b"\x89PNG\r\n\x1a\n" + PNG_MARK


# ============================================================================= 1. FEATURES

REQUIRED_KEYS = [
    "coach.breath", "coach.voice", "rx.ai_read", "rx.manual", "rx.review", "doses.reminders",
    "doses.web_push", "appt.booking", "appt.teleconsult", "docs.vault", "docs.abdm_link",
    "twin.live", "twin.public", "twin.fleet", "device.usb", "device.ble",
    "device.three_ball_reader", "device.speaking_base", "vitals.bluetooth", "auth.staff_login",
    "auth.sso_otp", "db.rls_per_hospital", "consent.itemised", "ai.register", "audit.log",
    "audit.hash_chain", "pilot.checklist", "fhir.export", "discharge.print", "comms.whatsapp",
    "comms.calls", "comms.whatsapp_real_send", "comms.ivr_reminders", "family.page",
    "impact.metrics", "rx.interaction_checks", "abha.field", "data_rights.requests",
    "hospital.self_registration", "demo.nightly_reset",
]


def test_feature_registry_is_well_formed():
    from backend.app import features
    keys = [f["key"] for f in features.FEATURES]
    assert len(keys) == len(set(keys)), "duplicate feature keys"
    assert len(keys) >= 60
    for f in features.FEATURES:
        assert set(f) == {"key", "name", "status", "where", "note"}, f
        assert re.fullmatch(r"[a-z0-9_]+(\.[a-z0-9_]+)+", f["key"]), f["key"]
        assert f["status"] in ("live", "simulated", "in_development", "planned"), f
        assert f["name"].strip() and f["where"].strip() and f["note"].strip(), f
        assert "\n" not in f["note"] and len(f["note"]) <= 140, f["key"]      # one plain line
    assert set(features.STATUS_LABEL) == set(features.STATUSES)


def test_feature_registry_has_every_planned_and_built_item_from_the_spec():
    from backend.app import features
    missing = [k for k in REQUIRED_KEYS if features.get(k) is None]
    assert not missing, missing
    status = {f["key"]: f["status"] for f in features.FEATURES}
    assert status["coach.breath"] == "simulated"                 # breaths are simulated
    assert status["twin.live"] == status["twin.public"] == status["twin.fleet"] == "simulated"
    assert status["device.usb"] == "in_development"
    assert status["comms.whatsapp_real_send"] == "in_development"
    assert status["comms.whatsapp"] == status["comms.calls"] == "simulated"
    assert status["fhir.export"] == "live"
    for planned in ("device.ble", "doses.web_push", "auth.sso_otp", "db.rls_per_hospital",
                    "appt.teleconsult", "docs.abdm_link", "abha.field", "device.three_ball_reader",
                    "device.speaking_base", "vitals.bluetooth", "rx.interaction_checks",
                    "data_rights.requests", "hospital.self_registration"):
        assert status[planned] == "planned", planned
    assert "clinical decision support" in features.get("rx.interaction_checks")["note"]


def test_feature_notes_never_use_a_never_say_phrase():
    from backend.app import features
    never = re.compile(r"approved|compliant|certified|validated|real[- ]time monitoring|"
                       r"prevents?\s+pneumonia|reduces?\s+readmission|abdm[- ]integrated|"
                       r"works with any spirometer|accurately|\bfirst\b", re.I)
    bad = [f["key"] for f in features.FEATURES if never.search(f["name"] + " " + f["note"])]
    assert not bad, bad
    assert not [f["key"] for f in features.FEATURES
                if features.NEVER_SAY.search(f["name"] + " " + f["note"])]


def test_feature_get_and_public_list_return_copies():
    from backend.app import features
    assert features.get("no.such.key") is None
    one = features.get("coach.breath")
    one["status"] = "live"
    assert features.get("coach.breath")["status"] == "simulated"
    listed = features.public_list()
    assert [f["key"] for f in listed] == [f["key"] for f in features.FEATURES]
    listed[0]["note"] = "changed"
    assert features.FEATURES[0]["note"] != "changed"


def test_features_endpoint_is_public(anon):
    from backend.app import features
    r = anon.get("/api/features")
    if r.status_code == 404:
        pytest.skip("the features router is not registered in main.py yet")
    assert r.status_code == 200, r.text
    body = r.json()
    assert isinstance(body, list) and body == features.public_list()


def test_every_badge_key_used_in_a_page_exists_in_the_registry():
    """Plan §3.6: a page may only show a badge for a key that is in features.py."""
    from backend.app import features
    used = set()
    for path in (ROOT / "web").rglob("*"):
        if path.suffix in (".html", ".js") and path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            used |= set(re.findall(r"data-feature=[\"']([a-z0-9_]+(?:\.[a-z0-9_]+)+)[\"']", text))
    unknown = sorted(k for k in used if features.get(k) is None)
    assert not unknown, unknown


# ============================================================================= 2. AI (Gemini)

class _FakeModel:
    """Stands in for ai_gemini._call_model: records every call, then answers or raises."""

    def __init__(self, *answers):
        self.answers, self.calls = list(answers), []

    def __call__(self, data, mime, prompt, schema=None):
        self.calls.append({"data": data, "mime": mime, "prompt": prompt, "schema": schema})
        a = self.answers[min(len(self.calls), len(self.answers)) - 1]
        if isinstance(a, BaseException):
            raise a
        return a


def _wipe(st, first_event_id):
    st.delete("ai_events", [("id", "gt", first_event_id)])
    for pid in (PID_YES, PID_NO, PID_NONE, PID_GONE):
        st.delete("consents", [("patient_id", "eq", pid)])
    st.delete("hospitals", [("id", "eq", HID)])


@pytest.fixture()
def ai(client, monkeypatch):
    """A test hospital with AI on, three consent records, a fake key and clean counters."""
    from backend.app import ai_gemini, service
    from backend.app.config import iso, now_local
    st = service.store()
    last = st.select("ai_events", order="id", desc=True, limit=1)
    first_event_id = last[0]["id"] if last else 0
    _wipe(st, first_event_id)
    st.insert("hospitals", [{"id": HID, "name": "Test Hospital (fictional)", "settings": {}}])
    st.insert("consents", [
        {"hospital_id": HID, "patient_id": PID_YES, "items": {"ai_use": True, "family_sharing": False}},
        {"hospital_id": HID, "patient_id": PID_NO, "items": {"ai_use": False, "care_reminders": True}},
        {"hospital_id": HID, "patient_id": PID_GONE, "items": {"ai_use": True}, "withdrawn_at": iso(now_local())},
    ])
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    monkeypatch.setenv("AI_DAILY_LIMIT", "300")
    monkeypatch.setenv("AI_PER_IP_HOUR", "20")
    monkeypatch.delenv("GEMINI_THINKING", raising=False)
    ai_gemini.reset_limits()
    yield SimpleNamespace(st=st, first_event_id=first_event_id,
                          events=lambda: st.select("ai_events", [("id", "gt", first_event_id)], order="id"))
    _wipe(st, first_event_id)
    ai_gemini.reset_limits()


def _fake(monkeypatch, *answers):
    from backend.app import ai_gemini
    fake = _FakeModel(*answers)
    monkeypatch.setattr(ai_gemini, "_call_model", fake)
    return fake


RX_ANSWER = {
    "doctor_name": "Dr. Meera Nair", "hospital_name": "Demo General Hospital (fictional)",
    "date": "08/10/2026", "patient_name_on_paper": "Ravi K", "handwritten": False, "legibility": "good",
    "advice": "Patient should also take vitamin D",                      # not asked for -> dropped
    "lines": [
        {"line_no": 1, "drug_name": "Pantoprazole", "form": "Tab", "strength": "40 mg", "dose_qty": "1",
         "dose_unit": "tablet", "frequency_raw": "OD", "food_timing_raw": "before breakfast",
         "duration_raw": "x 14 days", "as_needed": False, "instructions_raw": None, "confidence": 0.96,
         "unclear_fields": [], "box_2d": [100, 50, 140, 900], "warning": "may interact"},
        {"line_no": 2, "drug_name": "Paracetamol", "form": "Tab", "strength": None, "dose_qty": None,
         "dose_unit": None, "frequency_raw": "TDS", "food_timing_raw": None, "duration_raw": None,
         "as_needed": None, "instructions_raw": None, "confidence": 0.41,
         "unclear_fields": ["strength", "duration_raw", "not_a_field"], "box_2d": None},
    ],
}


def _rx(pid=PID_YES, ip="10.0.0.1", ref="document:12", data=FAKE_FILE, mime="image/png"):
    from backend.app import ai_gemini
    return ai_gemini.extract_prescription(data, mime, patient_id=pid, hospital_id=HID, ip=ip, input_ref=ref)


def test_rx_prompt_is_the_spec_text_and_carries_no_patient_data():
    from backend.app import ai_gemini as g
    assert g.RX_PROMPT_VERSION == "rx-v1" and g.DOC_PROMPT_VERSION == "doc-v1"
    assert g.RX_PROMPT_V1.startswith(
        "You transcribe medicine prescriptions. Copy exactly what is written. Do not correct "
        "spelling, do not add or remove medicines, do not infer missing values: use null and list "
        "the field in unclear_fields. Do not give advice, warnings or interpretations.")
    for field in ("doctor_name", "hospital_name", "date", "patient_name_on_paper", "handwritten",
                  "legibility", "line_no", "drug_name", "form", "strength", "dose_qty", "dose_unit",
                  "frequency_raw", "food_timing_raw", "duration_raw", "as_needed", "instructions_raw",
                  "confidence", "unclear_fields", "box_2d"):
        assert field in g.RX_PROMPT_V1, field
    assert set(g.RX_FIELDS) == {"doctor_name", "hospital_name", "date", "patient_name_on_paper",
                                "handwritten", "legibility", "lines"}
    assert "{" not in g.RX_PROMPT_V1 and "{" not in g.DOC_PROMPT_V1     # fixed text: nothing is filled in


def test_ok_draft_logs_an_ai_event_with_references_and_no_content(ai, monkeypatch):
    from backend.app import ai_gemini as g
    fake = _fake(monkeypatch, RX_ANSWER)
    out = _rx()
    assert out["ok"] is True and out["reason"] is None and out["ai_event_id"]
    draft = out["draft"]
    assert set(draft) == set(g.RX_FIELDS) and "advice" not in draft
    assert draft["handwritten"] is False                      # returned as is; the caller decides
    assert [ln["drug_name"] for ln in draft["lines"]] == ["Pantoprazole", "Paracetamol"]
    assert all(set(ln) == set(g.RX_LINE_FIELDS) for ln in draft["lines"])
    assert draft["lines"][1]["strength"] is None              # unclear stays blank, never guessed
    assert draft["lines"][1]["unclear_fields"] == ["strength", "duration_raw"]
    # exactly one model call: the file + the fixed prompt, nothing about the patient
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call["prompt"] == g.RX_PROMPT_V1 and call["schema"] is g.RxDraft
    assert call["data"] == FAKE_FILE and call["mime"] == "image/png"
    assert str(PID_YES) not in call["prompt"] and str(HID) not in call["prompt"]
    # the register row: references and the structured output only
    rows = ai.events()
    assert len(rows) == 1 and rows[0]["id"] == out["ai_event_id"]
    row = rows[0]
    assert row["purpose"] == "rx_extract" and row["provider"] == "gemini"
    assert row["model"] == "gemini-3.1-flash-lite"
    assert row["prompt_version"] == "rx-v1" and row["input_ref"] == "document:12"
    assert row["ok"] is True and row["error"] is None and row["patient_id"] == PID_YES
    assert row["hospital_id"] == HID and row["latency_ms"] >= 0
    assert row["output"] == draft
    blob = json.dumps(row, default=str)
    assert PNG_MARK.decode() not in blob and "You transcribe" not in blob and FAKE_KEY not in blob


def test_no_key_means_the_manual_path(ai, monkeypatch):
    from backend.app import ai_gemini as g
    monkeypatch.setenv("GEMINI_API_KEY", "")
    fake = _fake(monkeypatch, RX_ANSWER)
    assert g.gemini_enabled() is False
    out = _rx()
    assert out == {"ok": False, "reason": "No Gemini key – type the lines", "ai_event_id": None, "draft": None}
    assert g.ai_allowed(HID, PID_YES, "10.0.0.1") == (False, "No Gemini key – type the lines")
    assert fake.calls == [] and ai.events() == []


def test_daily_limit_stops_ai_calls(ai, monkeypatch):
    from backend.app import ai_gemini as g
    monkeypatch.setenv("AI_DAILY_LIMIT", "2")
    fake = _fake(monkeypatch, RX_ANSWER)
    assert _rx(ip="10.0.0.1")["ok"] and _rx(ip="10.0.0.2")["ok"]
    out = _rx(ip="10.0.0.3")
    assert out["ok"] is False and out["reason"] == "Daily AI limit reached" and out["draft"] is None
    assert len(fake.calls) == 2
    assert g.usage()["today"] == 2
    assert g.summarize_text("hello") is None and len(fake.calls) == 2      # summaries share the daily limit
    g.reset_limits()
    assert _rx(ip="10.0.0.3")["ok"]


def test_per_ip_limit_stops_one_network_only(ai, monkeypatch):
    monkeypatch.setenv("AI_PER_IP_HOUR", "1")
    fake = _fake(monkeypatch, RX_ANSWER)
    assert _rx(ip="10.0.0.1")["ok"]
    out = _rx(ip="10.0.0.1")
    assert out["ok"] is False and "Too many AI requests" in out["reason"]
    assert _rx(ip="10.0.0.2")["ok"]
    assert len(fake.calls) == 2


def test_patient_who_chose_no_ai_never_reaches_the_model(ai, monkeypatch):
    from backend.app import ai_gemini as g
    fake = _fake(monkeypatch, RX_ANSWER)
    out = _rx(pid=PID_NO)
    assert out["ok"] is False and out["reason"] == "Patient chose no AI" and out["draft"] is None
    doc = g.suggest_document(FAKE_FILE, "image/png", patient_id=PID_NO, hospital_id=HID,
                             ip="10.0.0.1", input_ref="document:13")
    assert doc["ok"] is False and doc["reason"] == "Patient chose no AI" and doc["suggestion"] is None
    assert fake.calls == [] and ai.events() == []                  # no AI call, so nothing to log


def test_no_consent_record_or_a_withdrawn_one_also_blocks_ai(ai, monkeypatch):
    from backend.app import ai_gemini as g
    fake = _fake(monkeypatch, RX_ANSWER)
    none = _rx(pid=PID_NONE)
    assert none["ok"] is False and none["reason"] == "No AI consent recorded for this patient"
    gone = _rx(pid=PID_GONE)
    assert gone["ok"] is False and gone["reason"] == "Patient chose no AI"
    assert g.consent_ai(PID_YES) is True and g.consent_ai(PID_NO) is False
    assert g.consent_ai(PID_NONE) is None and g.consent_ai(PID_GONE) is False
    assert fake.calls == []


def test_the_latest_consent_record_wins(ai, monkeypatch):
    from backend.app import ai_gemini as g
    fake = _fake(monkeypatch, RX_ANSWER)
    ai.st.insert("consents", [{"hospital_id": HID, "patient_id": PID_YES, "version": 2,
                               "items": {"ai_use": False}}])
    assert g.consent_ai(PID_YES) is False
    assert _rx()["reason"] == "Patient chose no AI" and fake.calls == []


def test_hospital_ai_switch_off_blocks_ai(ai, monkeypatch):
    fake = _fake(monkeypatch, RX_ANSWER)
    ai.st.update("hospitals", [("id", "eq", HID)], {"settings": {"ai_enabled": False}})
    out = _rx()
    assert out["ok"] is False and out["reason"] == "AI is switched off for this hospital"
    assert fake.calls == []
    ai.st.update("hospitals", [("id", "eq", HID)], {"settings": {"ai_handwriting": False}})
    assert _rx()["ok"] is True                                     # the default is "AI on"


def test_timeout_or_error_gives_ok_false_after_one_retry_and_is_logged(ai, monkeypatch):
    for exc in (TimeoutError("timed out"), RuntimeError("503 overloaded"), ValueError("bad json")):
        fake = _fake(monkeypatch, exc)
        out = _rx()
        assert out["ok"] is False and out["draft"] is None
        assert out["reason"] == "AI could not read this file – type the lines"
        assert len(fake.calls) == 2, "one retry"
        row = ai.events()[-1]
        assert out["ai_event_id"] == row["id"]
        assert row["ok"] is False and row["output"] is None and type(exc).__name__ in row["error"]
        assert row["prompt_version"] == "rx-v1" and row["input_ref"] == "document:12"


def test_a_failed_first_try_is_retried_once(ai, monkeypatch):
    fake = _fake(monkeypatch, TimeoutError("timed out"), RX_ANSWER)
    out = _rx()
    assert out["ok"] is True and len(fake.calls) == 2
    assert [r["ok"] for r in ai.events()] == [True]


def test_error_text_in_the_register_never_holds_the_key(ai, monkeypatch):
    _fake(monkeypatch, RuntimeError(f"401 invalid api key {FAKE_KEY} " + "x" * 600))
    out = _rx()
    row = ai.events()[-1]
    assert out["ok"] is False and FAKE_KEY not in row["error"] and len(row["error"]) <= 300


def test_an_answer_in_the_wrong_shape_is_a_failure_not_a_crash(ai, monkeypatch):
    for answer in ("not json at all", None, ["a", "list"], 42):
        _fake(monkeypatch, answer)
        out = _rx()
        assert out["ok"] is False and out["draft"] is None, answer
        assert out["reason"] == "AI could not read this file – type the lines"
        assert ai.events()[-1]["ok"] is False and "bad answer shape" in ai.events()[-1]["error"]
    for answer in ({"lines": "nope"}, {"lines": ["x", 3, None]}, {}):       # an object with no usable lines
        _fake(monkeypatch, answer)
        out = _rx()
        assert out["ok"] is True and out["draft"]["lines"] == [], answer


def test_file_types_the_ai_cannot_read_never_reach_the_model(ai, monkeypatch):
    fake = _fake(monkeypatch, RX_ANSWER)
    for mime in ("image/svg+xml", "text/html", "image/gif", "", None):
        out = _rx(mime=mime)
        assert out["ok"] is False and "type the lines" in out["reason"], mime
    assert _rx(data=b"")["ok"] is False
    assert fake.calls == []


def test_input_ref_can_only_be_a_short_reference(ai, monkeypatch):
    _fake(monkeypatch, RX_ANSWER)
    _rx(ref="Ravi Kumar's prescription, 3 lines: Pantoprazole 40 mg ...")
    assert ai.events()[-1]["input_ref"] == "invalid-ref"


def test_suggest_document_keeps_only_kind_title_and_date(ai, monkeypatch):
    from backend.app import ai_gemini as g
    assert set(g.DocSuggestion.model_fields) == {"kind", "title", "doc_date"}
    assert g.DOC_FIELDS == ("kind", "title", "doc_date")
    fake = _fake(monkeypatch, {"kind": "lab_report", "title": "Lab report", "doc_date": "2026-10-05",
                               "findings": "Hb 9.1 g/dL (low)", "patient_name": "Ravi Kumar",
                               "values": [{"test": "Hb", "value": 9.1}], "summary": "Anaemia"})
    out = g.suggest_document(FAKE_FILE, "application/pdf", patient_id=PID_YES, hospital_id=HID,
                             ip="10.0.0.1", input_ref="document:14")
    assert out["ok"] is True
    assert out["suggestion"] == {"kind": "lab_report", "title": "Lab report", "doc_date": "2026-10-05"}
    assert fake.calls[0]["prompt"] == g.DOC_PROMPT_V1 and fake.calls[0]["schema"] is g.DocSuggestion
    row = ai.events()[-1]
    assert row["purpose"] == "doc_suggest" and row["prompt_version"] == "doc-v1"
    assert row["input_ref"] == "document:14"
    assert row["output"] == out["suggestion"]                       # nothing else is stored
    blob = json.dumps(row, default=str)
    for leaked in ("9.1", "Anaemia", "Ravi Kumar", "findings", "values"):
        assert leaked not in blob, leaked


def test_suggest_document_never_passes_on_a_result_or_a_made_up_kind(ai, monkeypatch):
    from backend.app import ai_gemini as g
    cases = [
        ({"kind": "Lab Report", "title": "Blood sugar 240 – high", "doc_date": "05/10/2026"},
         {"kind": "lab_report", "title": None, "doc_date": None}),
        ({"kind": "x-ray", "title": "Chest X-ray: abnormal shadow", "doc_date": "2026-10-05"},
         {"kind": "other", "title": None, "doc_date": "2026-10-05"}),
        ({"kind": "discharge_summary", "title": "  Discharge summary  ", "doc_date": None},
         {"kind": "discharge_summary", "title": "Discharge summary", "doc_date": None}),
        ({}, {"kind": "other", "title": None, "doc_date": None}),
    ]
    for answer, want in cases:
        _fake(monkeypatch, answer)
        out = g.suggest_document(FAKE_FILE, "image/jpeg", patient_id=PID_YES, hospital_id=HID,
                                 ip=None, input_ref="document:15")
        assert out["ok"] is True and out["suggestion"] == want, answer
    low = g.DOC_PROMPT_V1.lower()
    assert "kind" in low and "title" in low and "doc_date" in low
    assert "do not read out, summarise or interpret" in low


def test_summarize_text_logs_only_the_length(ai, monkeypatch):
    from backend.app import ai_gemini as g
    fake = _fake(monkeypatch, "  Ravi did two sessions today.  ")
    assert g.summarize_text("PROMPT WITH NUMBERS") == "Ravi did two sessions today."
    assert fake.calls[0] == {"data": None, "mime": None, "prompt": "PROMPT WITH NUMBERS", "schema": None}
    row = ai.events()[-1]
    assert row["purpose"] == "summary" and row["ok"] is True
    assert row["output"] == {"chars": len("Ravi did two sessions today.")}
    assert "Ravi" not in json.dumps(row, default=str) and "PROMPT WITH" not in json.dumps(row, default=str)
    _fake(monkeypatch, RuntimeError("finish_reason=SAFETY"))
    assert g.summarize_text("x") is None and ai.events()[-1]["ok"] is False
    monkeypatch.setenv("GEMINI_API_KEY", "")
    assert g.summarize_text("x") is None


def test_ai_register_review_and_stats(ai, monkeypatch):
    from backend.app import ai_register
    _fake(monkeypatch, RX_ANSWER)
    a, b, c = _rx()["ai_event_id"], _rx()["ai_event_id"], _rx()["ai_event_id"]
    _fake(monkeypatch, TimeoutError("timed out"))
    _rx()
    empty = ai_register.stats(HID)
    assert empty["drafts"] == 3 and empty["reviewed"] == 0 and empty["lines_total"] == 0
    assert empty["lines_edited_pct"] == 0.0 and empty["rejected_pct"] == 0.0
    ai_register.record_review(a, 2, "approved", 3, 0, 0)
    ai_register.record_review(b, 2, "edited", 5, 2, 1)
    ai_register.record_review(c, 4, "rejected", 2, 0, 0)
    ai_register.record_review(0, 2, "approved", 1, 0, 0)            # no AI event: quietly nothing
    with pytest.raises(ValueError):
        ai_register.record_review(a, 2, "looks fine", 1, 0, 0)
    s = ai_register.stats(HID)
    assert s["drafts"] == 3 and s["reviewed"] == 3 and s["lines_total"] == 10
    assert s["lines_edited_pct"] == 20.0 and s["lines_removed_pct"] == 10.0
    assert s["rejected_pct"] == 33.3
    assert s["by_purpose"]["rx_extract"] == {"calls": 4, "ok": 3, "failed": 1}
    row = [r for r in ai.events() if r["id"] == b][0]
    assert row["reviewed_by"] == 2 and row["decision"] == "edited" and row["reviewed_at"]
    assert ai_register.stats(HID + 1)["drafts"] == 0                 # another hospital sees none of it
    assert ai_register.stats()["drafts"] >= 3
    assert len(ai_register.events_for(HID, purpose="rx_extract", limit=2)) == 2


# ----- the one SDK call, with a fake google-genai client (no network)

class _FakeGenaiClient:
    made = []
    answer = None

    def __init__(self, api_key=None, **kw):
        self.api_key = api_key
        self.models = SimpleNamespace(generate_content=self._generate)

    def _generate(self, **kw):
        _FakeGenaiClient.made.append({"api_key": self.api_key, **kw})
        return _FakeGenaiClient.answer


def _sdk(monkeypatch, finish="STOP", parsed=None, text=""):
    from google import genai
    from google.genai import types
    _FakeGenaiClient.made = []
    _FakeGenaiClient.answer = SimpleNamespace(
        candidates=[SimpleNamespace(finish_reason=getattr(types.FinishReason, finish))],
        parsed=parsed, text=text)
    monkeypatch.setattr(genai, "Client", _FakeGenaiClient)
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    return _FakeGenaiClient


def test_call_model_sends_the_file_the_prompt_and_a_json_schema(monkeypatch):
    from backend.app import ai_gemini as g
    monkeypatch.delenv("GEMINI_THINKING", raising=False)
    monkeypatch.setenv("GEMINI_TIMEOUT_S", "30")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    sdk = _sdk(monkeypatch, parsed=g.DocSuggestion(kind="other", title="Paper", doc_date=None))
    out = g._call_model(FAKE_FILE, "image/png", g.DOC_PROMPT_V1, g.DocSuggestion)
    assert out == {"kind": "other", "title": "Paper", "doc_date": None}
    sent = sdk.made[0]
    assert sent["api_key"] == FAKE_KEY and sent["model"] == "gemini-3.1-flash-lite"
    part, prompt = sent["contents"]
    assert part.inline_data.data == FAKE_FILE and part.inline_data.mime_type == "image/png"
    assert prompt == g.DOC_PROMPT_V1
    cfg = sent["config"]
    assert cfg.response_mime_type == "application/json" and cfg.response_schema is g.DocSuggestion
    assert cfg.http_options.timeout == 30000
    assert cfg.temperature is None and cfg.thinking_config is None      # model defaults
    # a dict or plain JSON text also works
    _sdk(monkeypatch, parsed={"kind": "other"})
    assert g._call_model(FAKE_FILE, "image/png", "p", g.DocSuggestion) == {"kind": "other"}
    _sdk(monkeypatch, parsed=None, text='{"kind": "lab_report"}')
    assert g._call_model(FAKE_FILE, "image/png", "p", g.DocSuggestion) == {"kind": "lab_report"}


def test_call_model_plain_text_thinking_level_and_stop_reasons(monkeypatch):
    from backend.app import ai_gemini as g
    sdk = _sdk(monkeypatch, text="  Three plain sentences.  ")
    monkeypatch.setenv("GEMINI_THINKING", "low")
    assert g._call_model(None, None, "write it", None) == "Three plain sentences."
    sent = sdk.made[0]
    assert sent["contents"] == "write it" and sent["config"].response_schema is None
    assert sent["config"].thinking_config.thinking_level.name == "LOW"
    monkeypatch.setenv("GEMINI_THINKING", "banana")                     # a bad value is ignored
    sdk = _sdk(monkeypatch, text="ok")
    assert g._call_model(None, None, "write it", None) == "ok"
    assert sdk.made[0]["config"].thinking_config is None
    for finish in ("MAX_TOKENS", "SAFETY", "RECITATION", "OTHER"):
        _sdk(monkeypatch, finish=finish, text="half an ans")
        with pytest.raises(RuntimeError, match="finish_reason"):
            g._call_model(None, None, "write it", None)
    _FakeGenaiClient.answer = SimpleNamespace(candidates=[], parsed=None, text="")
    with pytest.raises(RuntimeError, match="finish_reason"):
        g._call_model(None, None, "write it", None)


def test_the_response_schemas_are_accepted_by_the_installed_sdk():
    """Offline: the SDK turns our Pydantic models into its own schema without a network call."""
    from backend.app import ai_gemini as g
    try:
        from google import genai
        from google.genai import _transformers as t
    except Exception:
        pytest.skip("google-genai internals moved")
    c = genai.Client(api_key="x")
    rx = t.t_schema(c._api_client, g.RxDraft)
    doc = t.t_schema(c._api_client, g.DocSuggestion)
    assert set(rx.properties) == set(g.RX_FIELDS)
    assert set(doc.properties) == {"kind", "title", "doc_date"}


# ============================================================================= 3. STORAGE

def _img(fmt="PNG", size=(40, 20), mode="RGB", exif=True, text=True):
    from PIL import Image, PngImagePlugin
    img = Image.new(mode, size, (200, 30, 30) if mode == "RGB" else (200, 30, 30, 128))
    for x in range(size[0] // 2):                       # left half blue, so rotation is visible
        for y in range(size[1]):
            img.putpixel((x, y), (30, 30, 200) if mode == "RGB" else (30, 30, 200, 255))
    kw = {}
    if exif:
        ex = Image.Exif()
        ex[0x010F] = "SecretPhoneMaker"                 # Make
        ex[0x0112] = 6                                  # Orientation: rotate 90° to show upright
        kw["exif"] = ex
    if text and fmt == "PNG":
        info = PngImagePlugin.PngInfo()
        info.add_text("Comment", "hidden-note-123")
        kw["pnginfo"] = info
    buf = io.BytesIO()
    img.save(buf, fmt, **kw)
    return buf.getvalue()


def _open(data):
    from PIL import Image
    return Image.open(io.BytesIO(data))


def test_png_with_exif_comes_back_clean(client):
    from backend.app import storage
    dirty = _img("PNG")
    assert b"SecretPhoneMaker" in dirty and b"hidden-note-123" in dirty
    mime, cleaned, thumb = storage.validate_upload(dirty, "IMG_0001.png", "image/png")
    assert mime == "image/png"
    assert b"SecretPhoneMaker" not in cleaned and b"hidden-note-123" not in cleaned
    out = _open(cleaned)
    assert out.format == "PNG" and len(out.getexif()) == 0 and "Comment" not in out.info
    assert out.size == (20, 40)                         # the camera's rotation was applied
    t = _open(thumb)
    assert t.format == "PNG" and max(t.size) <= 320 and len(t.getexif()) == 0


def test_jpeg_and_webp_are_re_encoded_without_exif(client):
    from backend.app import storage
    for fmt, mime, name in (("JPEG", "image/jpeg", "photo.jpg"), ("WEBP", "image/webp", "photo.webp")):
        dirty = _img(fmt)
        assert b"SecretPhoneMaker" in dirty
        got, cleaned, thumb = storage.validate_upload(dirty, name, None)
        assert got == mime and b"SecretPhoneMaker" not in cleaned and b"Exif" not in cleaned
        out = _open(cleaned)
        assert out.format == fmt and len(out.getexif()) == 0 and out.size == (20, 40)
        assert _open(thumb).format == "PNG"


def test_the_type_comes_from_the_bytes_not_the_name_or_the_declared_type(client):
    from backend.app import storage
    jpeg = _img("JPEG", exif=False)
    assert storage.validate_upload(jpeg, "scan.png", "image/png")[0] == "image/jpeg"
    assert storage.validate_upload(jpeg, "../../etc/passwd", "application/octet-stream")[0] == "image/jpeg"
    assert storage.validate_upload(_img("PNG", mode="RGBA", exif=False), "a.png", None)[0] == "image/png"


def test_anything_hidden_after_the_picture_is_dropped(client):
    from backend.app import storage
    sneaky = _img("PNG", exif=False, text=False) + b"<script>alert('x')</script><?php evil(); ?>"
    mime, cleaned, _ = storage.validate_upload(sneaky, "x.png", "image/png")
    assert mime == "image/png" and b"<script" not in cleaned and b"<?php" not in cleaned


BAD_FILES = [
    ("svg renamed .png", b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>', "photo.png", "image/png"),
    ("svg with xml header", b'<?xml version="1.0"?>\n<svg xmlns="http://www.w3.org/2000/svg"/>', "photo.jpg", "image/jpeg"),
    ("svg after a BOM and spaces", b"\xef\xbb\xbf  \n<svg onload='x()'></svg>", "photo.webp", None),
    ("html renamed .pdf", b"<!DOCTYPE html><html><body><script>alert(1)</script></body></html>", "report.pdf", "application/pdf"),
    ("html fragment", b"hello <script>alert(1)</script>", "note.pdf", "application/pdf"),
    ("pdf header + web page", b"%PDF-1.4\n<html><script>alert(1)</script></html>\n%%EOF", "report.pdf", "application/pdf"),
    ("pdf with JavaScript", b"%PDF-1.4\n1 0 obj << /S /JavaScript /JS (app.alert(1)) >> endobj\n%%EOF", "report.pdf", "application/pdf"),
    ("pdf that launches a program", b"%PDF-1.4\n1 0 obj << /S /Launch /F (cmd.exe) >> endobj\n%%EOF", "report.pdf", "application/pdf"),
    ("cut-off pdf", b"%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\n", "report.pdf", "application/pdf"),
    ("xml", b'<?xml version="1.0"?><note>hi</note>', "data.png", None),
    ("shell script", b"#!/bin/sh\nrm -rf /\n", "run.jpg", "image/jpeg"),
    ("php", b"<?php system($_GET['c']); ?>", "x.png", "image/png"),
    ("gif (wrong magic)", b"GIF89a" + b"\x00" * 64, "anim.jpg", "image/jpeg"),
    ("windows program", b"MZ\x90\x00" + b"\x00" * 64, "setup.png", "image/png"),
    ("zip / docx", b"PK\x03\x04" + b"\x00" * 64, "letter.pdf", "application/pdf"),
    ("plain text", b"just some words, not a picture", "note.png", "image/png"),
    ("empty", b"", "empty.png", "image/png"),
    ("jpeg header only", b"\xff\xd8\xff\xe0" + b"\x00" * 32, "broken.jpg", "image/jpeg"),
    ("png header only", b"\x89PNG\r\n\x1a\n" + b"\x00" * 32, "broken.png", "image/png"),
]


@pytest.mark.parametrize("name,data,filename,declared", BAD_FILES, ids=[b[0] for b in BAD_FILES])
def test_bad_uploads_are_refused(client, name, data, filename, declared):
    from backend.app import storage
    with pytest.raises(ValueError) as e:
        storage.validate_upload(data, filename, declared)
    assert str(e.value) and "Traceback" not in str(e.value)          # a plain reason for the user


def test_a_real_picture_declared_as_svg_or_html_is_refused(client):
    from backend.app import storage
    png = _img("PNG", exif=False)
    for declared in ("image/svg+xml", "text/html", "application/xml", "text/javascript"):
        with pytest.raises(ValueError):
            storage.validate_upload(png, "photo.png", declared)


def test_more_than_10_mb_is_refused(client):
    from backend.app import storage
    assert storage.MAX_BYTES == 10 * 1024 * 1024
    big = b"\xff\xd8\xff" + b"0" * storage.MAX_BYTES
    with pytest.raises(ValueError, match="10 MB"):
        storage.validate_upload(big, "huge.jpg", "image/jpeg")
    big_pdf = b"%PDF-1.4\n" + b"0" * storage.MAX_BYTES + b"\n%%EOF"
    with pytest.raises(ValueError, match="10 MB"):
        storage.validate_upload(big_pdf, "huge.pdf", "application/pdf")


def test_cut_off_and_absurdly_large_pictures_are_refused(client, monkeypatch):
    from backend.app import storage
    whole = _img("JPEG", size=(300, 200), exif=False)
    with pytest.raises(ValueError):
        storage.validate_upload(whole[: len(whole) // 2], "cut.jpg", "image/jpeg")
    monkeypatch.setattr(storage, "MAX_PIXELS", 100)
    with pytest.raises(ValueError, match="too large"):
        storage.validate_upload(_img("PNG", exif=False), "big.png", "image/png")


def test_long_photos_are_scaled_down(client, monkeypatch):
    from backend.app import storage
    monkeypatch.setattr(storage, "MAX_SIDE", 64)
    for fmt in ("JPEG", "PNG"):
        _, cleaned, thumb = storage.validate_upload(_img(fmt, size=(400, 200), exif=False), "p", None)
        assert max(_open(cleaned).size) <= 64 and max(_open(thumb).size) <= 64


def test_a_pdf_is_kept_as_is_with_no_thumbnail(client):
    from backend.app import storage
    pdf = b"%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\ntrailer << /Root 1 0 R >>\n%%EOF\n"
    assert storage.validate_upload(pdf, "summary.pdf", "application/pdf") == ("application/pdf", pdf, None)
    assert storage.validate_upload(pdf, "summary.png", "image/png")[0] == "application/pdf"


def test_the_demo_sample_files_pass_validation(client):
    from backend.app import storage
    samples = [p for p in (ROOT / "web" / "samples").glob("*") if p.suffix in (".png", ".pdf")]
    if not samples:
        pytest.skip("no sample files in web/samples")
    for p in samples:
        mime, cleaned, thumb = storage.validate_upload(p.read_bytes(), p.name, None)
        assert mime == ("application/pdf" if p.suffix == ".pdf" else "image/png"), p.name
        assert (thumb is None) == (p.suffix == ".pdf") and cleaned


def test_save_load_delete_round_trip_locally(client):
    from backend.app import storage
    from backend.app.config import UPLOAD_DIR
    assert storage.backend_name() == "local"
    storage.ensure_bucket()
    mime, cleaned, thumb = storage.validate_upload(_img("PNG"), "My Prescription (final).PNG", "image/png")
    key = storage.save(cleaned, mime, prefix="docs")
    assert re.fullmatch(r"docs/\d{6}/[0-9a-f]{32}\.png", key)
    assert "prescription" not in key.lower()                        # the file name is never used
    assert (UPLOAD_DIR / key).is_file()
    tkey = storage.save(thumb, "image/png", prefix="thumbs", like=key)
    assert tkey == key.replace("docs/", "thumbs/", 1)
    assert storage.load(key) == cleaned and storage.load(tkey) == thumb
    other = storage.save(b"%PDF-1.4\n%%EOF", "application/pdf", prefix="docs")
    assert other != key and other.endswith(".pdf")
    for k in (key, tkey, other):
        storage.delete(k)
        storage.delete(k)                                           # already gone: not an error
        with pytest.raises(FileNotFoundError):
            storage.load(k)


def test_storage_keys_cannot_escape_the_upload_folder(client):
    from backend.app import storage
    for bad in ("../secrets.txt", "docs/../../.env", "/etc/passwd", "docs/202610/abc.png",
                "docs/202610/" + "g" * 32 + ".png", "docs/202610/" + "a" * 32 + ".svg", "", None):
        with pytest.raises(ValueError):
            storage.load(bad)
        with pytest.raises(ValueError):
            storage.delete(bad)
    for prefix in ("../x", "docs/evil", "", "UPPER"):
        with pytest.raises(ValueError):
            storage.save(b"x", "image/png", prefix=prefix)
    with pytest.raises(ValueError):
        storage.save(b"x", "image/svg+xml", prefix="docs")


def test_supabase_storage_calls_use_the_private_bucket(client, monkeypatch):
    from backend.app import storage
    calls, box = [], {}

    def fake_request(method, path, **kw):
        calls.append((method, path, kw))
        if method == "POST" and path.startswith("/object/"):
            box[path.split("/", 3)[3]] = kw["content"]
            return SimpleNamespace(status_code=200, content=b"", text="{}")
        if method == "GET":
            key = path.split("/", 4)[4]
            return (SimpleNamespace(status_code=200, content=box[key], text="") if key in box
                    else SimpleNamespace(status_code=400, content=b"", text='{"error":"not_found"}'))
        if method == "DELETE":
            box.pop(path.split("/", 3)[3], None)
            return SimpleNamespace(status_code=200, content=b"", text="{}")
        return SimpleNamespace(status_code=400, content=b"", text='{"message":"The resource already exists"}')

    monkeypatch.setattr(storage, "_supabase", lambda: ("https://example.invalid", "service-key"))
    monkeypatch.setattr(storage, "_request", fake_request)
    assert storage.backend_name() == "supabase"
    key = storage.save(b"%PDF-1.4\n%%EOF", "application/pdf", prefix="docs")
    method, path, kw = calls[-1]
    assert (method, path) == ("POST", f"/object/documents/{key}")
    assert kw["headers"]["Content-Type"] == "application/pdf"
    assert storage.load(key) == b"%PDF-1.4\n%%EOF"
    assert calls[-1][:2] == ("GET", f"/object/authenticated/documents/{key}")
    storage.delete(key)
    assert calls[-1][:2] == ("DELETE", f"/object/documents/{key}")
    with pytest.raises(FileNotFoundError):
        storage.load(key)
    storage.ensure_bucket()                                         # "already exists" is fine
    method, path, kw = calls[-1]
    assert (method, path) == ("POST", "/bucket")
    assert kw["json"]["id"] == "documents" and kw["json"]["public"] is False


def test_supabase_storage_problems_are_clear_errors_and_ensure_bucket_never_raises(client, monkeypatch):
    from backend.app import storage

    def down(method, path, **kw):
        raise ConnectionError("no network")

    monkeypatch.setattr(storage, "_supabase", lambda: ("https://example.invalid", "service-key"))
    monkeypatch.setattr(storage, "_request", down)
    storage.ensure_bucket()
    key = "docs/202610/" + "a" * 32 + ".png"
    for call in (lambda: storage.save(b"x", "image/png", prefix="docs"), lambda: storage.load(key),
                 lambda: storage.delete(key)):
        with pytest.raises(storage.StorageError):
            call()
    monkeypatch.setattr(storage, "_request", lambda m, p, **kw: SimpleNamespace(status_code=500, content=b"", text="boom"))
    storage.ensure_bucket()
    with pytest.raises(storage.StorageError):
        storage.save(b"x", "image/png", prefix="docs")


# ============================================================================= 4. SUMMARY PROVIDERS

STATS = {"first_name": "Ravi", "done": 2, "due": 3, "best_ml": 1500, "target_ml": 1500,
         "personal_best_ml": 1600, "avg_score": 8, "label_counts": {"good": 6}, "trend": "up",
         "trailing_missed": 0}
GOOD_TEXT = "Ravi did two of three sessions today. The best breath reached the target. Keep going slowly."


def _providers(monkeypatch, anthropic=None, gemini=None):
    """Give a key to the named providers and replace their network calls. A value is the text to
    answer or an exception to raise. Returns the list that records which provider was asked."""
    from backend.app import ai_gemini, llm
    asked = []
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake" if anthropic is not None else "")
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY if gemini is not None else "")

    def answer(name, value):
        def f(*a, **kw):
            asked.append(name)
            if isinstance(value, BaseException):
                raise value
            return value
        return f

    monkeypatch.setattr(llm, "_anthropic_text", answer("anthropic", anthropic))
    monkeypatch.setattr(ai_gemini, "_call_model", answer("gemini", gemini))
    return asked


def test_no_keys_means_the_template(ai, monkeypatch):
    from backend.app import llm
    asked = _providers(monkeypatch)
    assert llm.llm_enabled() is False and llm.providers() == []
    out = llm.summarize(STATS, "en")
    assert out == {"text": llm.template_summary(STATS, "en"), "source": "template"} and asked == []


def test_anthropic_is_asked_before_gemini(ai, monkeypatch):
    from backend.app import llm
    asked = _providers(monkeypatch, anthropic=GOOD_TEXT, gemini="Gemini text that is never used.")
    assert llm.providers() == ["anthropic", "gemini"]
    assert llm.summarize(STATS, "en") == {"text": GOOD_TEXT, "source": "llm"}
    assert asked == ["anthropic"]


def test_gemini_is_used_when_anthropic_fails_or_has_no_key(ai, monkeypatch):
    from backend.app import llm
    gem = "Ravi kept up the practice today. The breaths were deep. Keep the slow pace."
    for failure in (TimeoutError("timed out"), RuntimeError("stop_reason=refusal"), ""):
        asked = _providers(monkeypatch, anthropic=failure, gemini=gem)
        assert llm.summarize(STATS, "hi") == {"text": gem, "source": "llm"}
        assert asked == ["anthropic", "gemini"]
    asked = _providers(monkeypatch, gemini=gem)
    assert llm.llm_enabled() is True and llm.providers() == ["gemini"]
    assert llm.summarize(STATS, "en") == {"text": gem, "source": "llm"}
    assert asked == ["gemini"]


def test_gemini_gets_the_same_instructions_and_only_text(ai, monkeypatch):
    from backend.app import ai_gemini, llm
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("GEMINI_API_KEY", FAKE_KEY)
    fake = _fake(monkeypatch, GOOD_TEXT)
    assert llm.summarize(STATS, "ta")["source"] == "llm"
    call = fake.calls[0]
    assert call["data"] is None and call["mime"] is None and call["schema"] is None
    assert call["prompt"].startswith(llm.SYSTEM) and "Never diagnose" in call["prompt"]
    assert "Tamil" in call["prompt"] and "Sessions done today: 2 of 3" in call["prompt"]
    assert ai_gemini.usage()["today"] == 1


def test_both_providers_failing_gives_the_template(ai, monkeypatch):
    from backend.app import llm
    for gem_failure in (TimeoutError("timed out"), RuntimeError("finish_reason=SAFETY"),
                        RuntimeError("finish_reason=MAX_TOKENS"), "", "   "):
        asked = _providers(monkeypatch, anthropic=ConnectionError("no network"), gemini=gem_failure)
        for lang in ("en", "hi", "ta", "ml"):
            out = llm.summarize(STATS, lang)
            assert out["source"] == "template" and len(out["text"]) > 40
        retried = isinstance(gem_failure, BaseException)                   # an error is retried once
        assert asked.count("anthropic") == 4 and asked.count("gemini") == (8 if retried else 4)


def test_the_never_diagnose_filter_applies_to_gemini_text_too(ai, monkeypatch):
    from backend.app import llm
    for bad in ("Ravi may have pneumonia, please see a doctor.", "This looks like a chest infection.",
                "He should take his medication.", "I diagnose a mild fever.", "Increase the dose."):
        asked = _providers(monkeypatch, gemini=bad)
        out = llm.summarize(STATS, "en")
        assert out["source"] == "template" and bad not in out["text"], bad
        assert asked == ["gemini"]
        asked = _providers(monkeypatch, anthropic=bad, gemini=bad)
        assert llm.summarize(STATS, "en")["source"] == "template"
        assert asked == ["anthropic", "gemini"]


def test_summary_respects_the_patients_ai_choice_when_a_patient_id_is_given(ai, monkeypatch):
    from backend.app import llm
    asked = _providers(monkeypatch, anthropic=GOOD_TEXT, gemini=GOOD_TEXT)
    for pid in (PID_NO, PID_NONE, PID_GONE):
        assert llm.summarize(STATS, "en", patient_id=pid)["source"] == "template"
    assert asked == []                                               # no AI call at all
    assert llm.summarize(STATS, "en", patient_id=PID_YES) == {"text": GOOD_TEXT, "source": "llm"}
    assert llm.summarize(STATS, "en")["source"] == "llm"             # old callers: unchanged
