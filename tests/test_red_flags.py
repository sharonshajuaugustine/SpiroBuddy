"""Red-flag words (spec §2): the phrasings the review found missing must always reach a person.

Seven meanings – can't breathe, difficulty breathing, chest hurts, took too many, rash, bleeding,
fainted – in English, Hindi (Devanagari and Roman letters), Tamil and Malayalam. Each phrase must
trigger BOTH fixed checks: voice.red_flag (the word list) and comms.messages.RED_FLAG_RE.
No AI is involved anywhere. ta/ml phrases were written without a native speaker.
"""
import pytest

NEW_PHRASES = {
    "en": [
        # exactly as listed in the spec / review
        "I cant breath", "I can't breathe", "cant breathe", "difficulty in breathing",
        "my chest hurts", "took too many", "rash", "bleeding", "fainted",
        # everyday sentences with the same meaning
        "I can’t breathe properly", "i cannot breath", "having difficulty in breathing since morning",
        "My chest is hurting a lot", "I think I took too many tablets", "took too many pills by mistake",
        "I have a rash on my arm", "red rashes all over", "there is bleeding from the stitches",
        "I fainted this morning",
    ],
    "hi": [
        "मैं साँस नहीं ले पा रहा हूँ", "सांस नही आ रही", "साँस लेने में तकलीफ हो रही है",
        "सांस लेने मे दिक्कत है", "मेरा सीना दुख रहा है", "छाती में दुख रहा है",
        "मैंने ज़्यादा गोलियाँ खा लीं",        # ज़्यादा with a separate nukta
        "मैंने ज़्यादा गोलियाँ खा लीं",              # ज़्यादा as one letter
        "ज्यादा दवा खा ली", "शरीर पर दाने निकल आए हैं", "चकत्ते हो गए हैं", "खून बह रहा है",
        "ख़ून आ रहा है",                                      # ख़ून with a nukta
        "मैं बेहोश हो गया था",
    ],
    "hi_latn": [
        "saans nahi le pa raha hoon", "sans nhi aa rahi", "saans lene me takleef ho rahi hai",
        "saans lene mein dikkat hai", "mera seena dukh raha hai", "chhati me dard hai",
        "maine zyada goli kha li", "jyada dawa le li", "sharir par daane nikal aaye",
        "lal dane ho gaye", "khoon beh raha hai", "khun nikal raha hai", "main behosh ho gaya tha",
    ],
    "ta": [
        "என்னால் மூச்சு விட முடியவில்லை", "மூச்சு விட முடியல", "மூச்சு விடுவதில் சிரமம்",
        "மூச்சு விட கஷ்டமாக இருக்கு", "என் நெஞ்சு வலிக்கிறது", "நெஞ்சில் வலி இருக்கிறது",
        "நான் அதிக மாத்திரை சாப்பிட்டுவிட்டேன்", "மாத்திரை அதிகமாக சாப்பிட்டேன்",
        "உடம்பில் தடிப்பு வந்திருக்கிறது", "இரத்தப்போக்கு இருக்கிறது", "ரத்தம் வருகிறது",
        "நான் மயங்கி விழுந்தேன்",
    ],
    "ml": [
        "എനിക്ക് ശ്വാസം കിട്ടുന്നില്ല", "ശ്വാസമെടുക്കാൻ പറ്റുന്നില്ല", "ശ്വസിക്കാൻ കഴിയുന്നില്ല",
        "ശ്വസിക്കാൻ ബുദ്ധിമുട്ടുണ്ട്", "ശ്വാസമെടുക്കാൻ ബുദ്ധിമുട്ട്", "എന്റെ നെഞ്ച് വേദനിക്കുന്നു",
        "നെഞ്ചിൽ വേദനയുണ്ട്", "ഞാൻ കൂടുതൽ ഗുളിക കഴിച്ചു", "ഗുളിക കൂടുതൽ കഴിച്ചുപോയി",
        "ശരീരത്തിൽ തിണർപ്പ് ഉണ്ട്", "ചുവന്ന പാടുകൾ വന്നു", "രക്തസ്രാവം ഉണ്ട്", "ചോര വരുന്നു",
        "ഞാൻ ബോധംകെട്ടു വീണു", "തലകറങ്ങി വീണു",
    ],
}

ORDINARY = [
    "I took my medicine", "breathing exercise done", "done", "ok", "I did ten slow breaths",
    "see you tomorrow", "what time is my next session", "I took my tablet after breakfast",
    "मैंने दवा ले ली", "साँस का व्यायाम हो गया", "हो गया", "नमस्ते",
    "maine dawa le li", "saans ki exercise ho gayi", "theek hai",
    "நான் மருந்து சாப்பிட்டேன்", "மூச்சுப் பயிற்சி முடிந்தது", "நன்றி",
    "ഞാൻ മരുന്ന് കഴിച്ചു", "ശ്വസന വ്യായാമം കഴിഞ്ഞു", "നന്ദി",
]

_ALL_NEW = [(lang, p) for lang, phrases in NEW_PHRASES.items() for p in phrases]


@pytest.mark.parametrize("lang,phrase", _ALL_NEW)
def test_new_red_flag_phrase_triggers_both_checks(lang, phrase):
    from backend.app import voice
    from backend.app.comms import messages
    assert voice.red_flag(phrase), f"voice.red_flag missed ({lang}): {phrase}"
    assert messages.RED_FLAG_RE.search(phrase), f"RED_FLAG_RE missed ({lang}): {phrase}"
    assert messages.detect_intent(phrase, "patient") == "red_flag"
    assert messages.detect_intent(phrase, "guardian") == "red_flag"


@pytest.mark.parametrize("phrase", ORDINARY)
def test_ordinary_sentences_are_not_red_flags(phrase):
    from backend.app import voice
    from backend.app.comms import messages
    assert not voice.red_flag(phrase), phrase
    assert not messages.RED_FLAG_RE.search(phrase), phrase
    assert messages.detect_intent(phrase, "patient") != "red_flag"


def test_every_language_covers_all_seven_meanings():
    """A guard for whoever edits the lists next: at least seven phrases per language."""
    for lang in ("en", "hi", "hi_latn", "ta", "ml"):
        assert len(NEW_PHRASES[lang]) >= 7, lang


def test_the_older_red_flag_words_still_work():
    from backend.app import voice
    from backend.app.comms import messages
    for phrase in ("chest pain", "can't breathe", "short of breath", "blood", "fever", "dizzy",
                   "सीने में दर्द", "बुखार", "saans nahi", "seene mein dard", "நெஞ்சு வலி",
                   "காய்ச்சல்", "மயக்கம்"):
        assert voice.red_flag(phrase), phrase
        assert messages.RED_FLAG_RE.search(phrase), phrase
    for phrase in ("നെഞ്ചുവേദന", "പനി", "choking", "ambulance"):       # only ever in the voice list
        assert voice.red_flag(phrase), phrase


def test_spacing_punctuation_and_case_do_not_hide_a_red_flag():
    from backend.app import voice
    for phrase in ("I CANT BREATH", "i  cant   breath!!", "My chest... hurts", "Took-too-many tablets",
                   "RASH."):
        assert voice.red_flag(phrase), phrase


def test_red_flag_reply_is_the_fixed_message_never_ai_text():
    from backend.app import voice
    from backend.app.voice_cues import RED_FLAG_EN
    assert "112" in RED_FLAG_EN and "nurse" in RED_FLAG_EN.lower()
    for lang in ("en", "hi", "ta", "ml"):
        msg = voice.red_flag_message(lang)
        assert msg and "112" in msg, lang
