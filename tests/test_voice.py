"""CONTRACT E (voice) with no Sarvam key: clean fallbacks and the red-flag filter."""
import pytest


def test_status_disabled_without_key(client):
    s = client.get("/api/voice/status").json()
    assert s["enabled"] is False
    assert len(s["languages"]) >= 11


def test_tts_falls_back_to_browser(client):
    r = client.post("/api/voice/tts", json={"text": "Breathe in slowly", "language": "hi"})
    assert r.status_code == 503 and r.json()["fallback"] == "browser"


@pytest.mark.parametrize("text,lang", [
    ("I can't breathe", "en"),
    ("mujhe saans nahi aa rahi", "hi"),
    ("mujhe bukhar hai", "hi"),
    ("मुझे सीने में दर्द है", "hi"),
])
def test_red_flags_get_fixed_message(client, text, lang):
    r = client.post("/api/voice/stt", data={"text": text, "language": lang, "patient_id": "1"}).json()
    assert r["red_flag"] is True, text
    assert r["reply"], "a fixed contact-your-nurse / 112 reply must be returned"


def test_normal_question_is_not_red_flag(client):
    r = client.post("/api/voice/stt", data={"text": "How many breaths should I do?", "language": "en",
                                            "patient_id": "1"}).json()
    assert r["red_flag"] is False and r["reply"]
