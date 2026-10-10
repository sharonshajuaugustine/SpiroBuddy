"""WhatsApp for the ladder: texts in English / Hindi / Tamil / Malayalam, quick-reply buttons (Twilio Content
API when a template SID is set, otherwise "Reply 1/2/3" text), media (weekly card, voice note),
and inbound replies ("1", "done", "status", "स्थिति", "help" -> red-flag flow).

Rules (FEATURE_PLAN Part D): one question per message, at most 3 options, the patient's own
language, every automated message says it is automatic and how to reach a human, never a
diagnosis. Red-flag words always get the fixed "contact your nurse / call 112" message.

Malayalam ("ml", Q-28): every Malayalam string in this file was written without a native speaker
and NEEDS A NATIVE-SPEAKER CHECK before real use. Calls/IVR stay en/hi/ta (common.lang_of).
Reminder wording is strictly *utility* (no promotion) so Meta bills it at the utility rate.
"""
from __future__ import annotations

import json
import logging
import re

from .. import service, whatsapp
from ..config import env, iso
from .common import (call_name, disclosed, e164, first_name, honorific, log_event, now,
                     resolve_number, st, text_lang)

log = logging.getLogger("spirobuddy.comms.messages")

# ----------------------------------------------------------------------------- fixed texts

RED_FLAG_TEXT = {
    "en": "Please contact your nurse now. If it's an emergency, call 112.",
    "hi": "कृपया अभी अपनी नर्स से संपर्क करें। आपातकाल हो तो 112 पर कॉल करें।",
    "ta": "தயவுசெய்து உடனே உங்கள் செவிலியரைத் தொடர்பு கொள்ளுங்கள். அவசரம் என்றால் 112 ஐ அழைக்கவும்.",
    "ml": "ദയവായി ഉടൻ തന്നെ നിങ്ങളുടെ നഴ്സിനെ ബന്ധപ്പെടുക. അടിയന്തര സാഹചര്യമാണെങ്കിൽ 112-ൽ വിളിക്കുക.",
}
try:   # one fixed red-flag phrase everywhere: reuse the voice agent's cue (voice_cues.py)
    from ..voice_cues import cue_text as _cue
    RED_FLAG_TEXT = {k: (_cue("red_flag", k) or v) for k, v in RED_FLAG_TEXT.items()}
except Exception:
    pass
NURSE_TOLD = {"en": "We have told your nurse.", "hi": "हमने आपकी नर्स को बता दिया है।",
              "ta": "உங்கள் செவிலியருக்குத் தெரிவித்துள்ளோம்.",
              "ml": "ഞങ്ങൾ നിങ്ങളുടെ നഴ്സിനെ അറിയിച്ചിട്ടുണ്ട്."}
FOOTER = {
    "en": "— SpiroBuddy (automatic message). Reply 3 to talk to your nurse.",
    "hi": "— SpiroBuddy (स्वचालित संदेश)। नर्स से बात करने के लिए 3 भेजें।",
    "ta": "— SpiroBuddy (தானியங்கி செய்தி). செவிலியருடன் பேச 3 அனுப்பவும்.",
    "ml": "— SpiroBuddy (ഓട്ടോമാറ്റിക് സന്ദേശം). നഴ്സുമായി സംസാരിക്കാൻ 3 അയയ്ക്കുക.",
}

PATIENT_BUTTONS = {
    "en": [("done", "✅ Done"), ("snooze", "⏰ 15 min"), ("call_me", "📞 Call me")],
    "hi": [("done", "✅ हो गया"), ("snooze", "⏰ 15 मिनट बाद"), ("call_me", "📞 मुझे कॉल करें")],
    "ta": [("done", "✅ முடிந்தது"), ("snooze", "⏰ 15 நிமிடம்"), ("call_me", "📞 அழைக்கவும்")],
    "ml": [("done", "✅ ചെയ്തു"), ("snooze", "⏰ 15 മിനിറ്റ്"), ("call_me", "📞 എന്നെ വിളിക്കൂ")],
}
GUARDIAN_BUTTONS = {
    "en": [("guardian_ack", "👍 I'll check"), ("status", "📊 Status"), ("nurse", "📞 Nurse")],
    "hi": [("guardian_ack", "👍 मैं देखता हूँ"), ("status", "📊 स्थिति"), ("nurse", "📞 नर्स")],
    "ta": [("guardian_ack", "👍 பார்க்கிறேன்"), ("status", "📊 நிலை"), ("nurse", "📞 செவிலியர்")],
    "ml": [("guardian_ack", "👍 ഞാൻ നോക്കാം"), ("status", "📊 സ്ഥിതി"), ("nurse", "📞 നഴ്സ്")],
}
from .consent import RENEW_BUTTONS  # noqa: E402  (weekly "keep calling? yes / STOP")

BUTTONS_BY_KIND = {"reminder": ("patient", PATIENT_BUTTONS),
                   "guardian_alert": ("guardian", GUARDIAN_BUTTONS),
                   "consent_renewal": ("any", RENEW_BUTTONS)}


def numbered(buttons: list[tuple[str, str]], lang: str) -> str:
    word = {"en": "Reply", "hi": "जवाब दें", "ta": "பதில்", "ml": "മറുപടി"}.get(lang, "Reply")
    return f"{word}: " + " · ".join(f"{i + 1} = {label}" for i, (_, label) in enumerate(buttons))


def addr(patient: dict, lang: str) -> str:
    fn = first_name(patient.get("name"))
    if lang == "hi":
        return f"{fn} जी"
    if lang == "ta":
        return f"{fn} {'அம்மா' if (patient.get('sex') or '').upper() == 'F' else 'ஐயா'}"
    if lang == "ml":           # 'Sreedevi ചേച്ചി' / 'Gopan ചേട്ടൻ' (native-speaker check: ചേച്ചി or അമ്മ?)
        return f"{fn} {'ചേച്ചി' if (patient.get('sex') or '').upper() == 'F' else 'ചേട്ടൻ'}"
    return honorific(patient, "en")


def reminder_text(patient: dict, lang: str, missed: int) -> str:
    a = addr(patient, lang)
    if lang == "hi":
        return (f"🔔 नमस्ते {a}, यह SpiroBuddy की स्वचालित देखभाल सहायक है। साँस के व्यायाम का समय "
                f"हो गया है – 10 धीमी, गहरी साँसें। क्या आपने कर लिया?")
    if lang == "ta":
        return (f"🔔 வணக்கம் {a}, இது SpiroBuddy-இன் தானியங்கி பராமரிப்பு உதவியாளர். மூச்சுப் பயிற்சி "
                f"நேரம் – 10 மெதுவான, ஆழ்ந்த மூச்சுகள். முடித்துவிட்டீர்களா?")
    if lang == "ml":
        return (f"🔔 നമസ്കാരം {a}, ഇത് SpiroBuddy-യുടെ ഓട്ടോമാറ്റിക് പരിചരണ സഹായിയാണ്. ശ്വസന "
                f"വ്യായാമത്തിനുള്ള സമയമായി – 10 പതുക്കെയുള്ള, ആഴത്തിലുള്ള ശ്വാസങ്ങൾ. നിങ്ങൾ ചെയ്തോ?")
    return (f"🔔 Namaste {a}, this is SpiroBuddy's automated care assistant. It's time for your "
            f"breathing exercise – 10 slow, deep breaths. Have you done it?")


def guardian_alert_text(patient: dict, guardian: dict, missed: int, patient_answered: bool,
                        red_flag: bool = False) -> str:
    lang = text_lang(guardian.get("language"), "en")
    who = call_name(guardian.get("relation"), patient, lang)
    fn = first_name(patient.get("name"))
    gname = first_name(guardian.get("name"))
    me = {"hi": "यह SpiroBuddy की स्वचालित देखभाल सहायक है।",
          "ta": "இது SpiroBuddy-இன் தானியங்கி பராமரிப்பு உதவியாளர்.",
          "ml": "ഇത് SpiroBuddy-യുടെ ഓട്ടോമാറ്റിക് പരിചരണ സഹായിയാണ്.",
          "en": "this is SpiroBuddy's automated care assistant."}[lang]
    if red_flag:
        if lang == "hi":
            return (f"🚨 {gname} जी, {me} {who} ({fn}) ने SpiroBuddy पर मदद माँगी है। नर्स को बता दिया गया है। "
                    f"कृपया तुरंत उनसे बात करें। आपातकाल हो तो 112 पर कॉल करें।")
        if lang == "ta":
            return (f"🚨 {gname}, {me} {who} ({fn}) SpiroBuddy-இல் உதவி கேட்டுள்ளார். செவிலியருக்குத் "
                    f"தெரிவிக்கப்பட்டது. உடனே பேசுங்கள். அவசரம் என்றால் 112 ஐ அழைக்கவும்.")
        if lang == "ml":
            return (f"🚨 {gname}, {me} {who} ({fn}) SpiroBuddy-യിൽ സഹായം ചോദിച്ചിട്ടുണ്ട്. നഴ്സിനെ "
                    f"അറിയിച്ചിട്ടുണ്ട്. ദയവായി ഉടൻ സംസാരിക്കുക. അടിയന്തര സാഹചര്യത്തിൽ 112-ൽ വിളിക്കുക.")
        return (f"🚨 {gname}, {me} {who} ({fn}) asked for help on SpiroBuddy. The nurse has been told. "
                f"Please speak to them now. In an emergency, call 112.")
    if lang == "hi":
        tail = "और हमारी रिमाइंडर कॉल का जवाब नहीं दिया" if not patient_answered else ""
        return (f"नमस्ते {gname} जी, {me} {who} ({fn}) ने लगातार {missed} साँस-व्यायाम छोड़ दिए हैं {tail}। "
                f"क्या आप एक बार उनका हाल पूछ लेंगे?").replace("  ", " ").replace(" ।", "।")
    if lang == "ta":
        return (f"வணக்கம் {gname}, {me} {who} ({fn}) தொடர்ந்து {missed} மூச்சுப் பயிற்சிகளைத் "
                f"தவறவிட்டுள்ளார். ஒருமுறை அவரை விசாரிப்பீர்களா?")
    if lang == "ml":
        tail = ", ഞങ്ങളുടെ ഓർമ്മപ്പെടുത്തൽ കോളിന് മറുപടിയും നൽകിയില്ല" if not patient_answered else ""
        return (f"നമസ്കാരം {gname}, {me} {who} ({fn}) തുടർച്ചയായി {missed} ശ്വസന വ്യായാമങ്ങൾ "
                f"ചെയ്തില്ല{tail}. ഒന്ന് വിവരം അന്വേഷിക്കാമോ?")
    tail = " and didn't answer our reminder call" if not patient_answered else ""
    return (f"Namaste {gname}, {me} {who} ({fn}) has missed {missed} breathing sessions in a row{tail}. "
            f"Could you check on them?")


def status_text(pid: int, lang: str, for_guardian: dict | None = None) -> str:
    from .progress import progress
    pr = progress(pid)
    if not pr:
        return "—"
    p = pr["patient"]
    fn = first_name(p["name"])
    who = call_name(for_guardian.get("relation"), p, lang) if for_guardian else fn
    best = int(pr["best_today"] or 0)
    label = f"{who} ({fn})" if for_guardian and who != fn else fn
    last_hr = pr["last"]["slot_hour"] if pr["last"] else None
    if lang == "hi":
        s = f"📊 {label} – " + (f"आज {pr['due']} में से {pr['done']} सेशन पूरे।" if pr["due"]
                               else "आज के सेशन सुबह 8 बजे शुरू होंगे।")
        s += f" सबसे अच्छी साँस {best} mL (लक्ष्य {pr['target_ml']} mL)।" if best else ""
        if pr["streak"]:
            s += f" लगातार {pr['streak']} दिन अच्छे रहे। 🔥"
        if last_hr is not None:
            s += f" आख़िरी सत्र {last_hr}:00 बजे।"
        return s
    if lang == "ta":
        s = f"📊 {label} – " + (f"இன்று {pr['due']} இல் {pr['done']} பயிற்சிகள் முடிந்தன." if pr["due"]
                               else "இன்றைய பயிற்சிகள் காலை 8 மணிக்குத் தொடங்கும்.")
        s += f" சிறந்த மூச்சு {best} mL (இலக்கு {pr['target_ml']} mL)." if best else ""
        if pr["streak"]:
            s += f" தொடர்ந்து {pr['streak']} நல்ல நாட்கள் 🔥"
        return s
    if lang == "ml":
        s = f"📊 {label} – " + (f"ഇന്ന് {pr['due']}-ൽ {pr['done']} സെഷനുകൾ പൂർത്തിയായി." if pr["due"]
                               else "ഇന്നത്തെ സെഷനുകൾ രാവിലെ 8 മണിക്ക് തുടങ്ങും.")
        s += f" ഏറ്റവും നല്ല ശ്വാസം {best} mL (ലക്ഷ്യം {pr['target_ml']} mL)." if best else ""
        if pr["streak"]:
            s += f" തുടർച്ചയായി {pr['streak']} നല്ല ദിവസങ്ങൾ 🔥"
        if last_hr is not None:
            s += f" അവസാന സെഷൻ {last_hr}:00-ന്."
        return s
    s = f"📊 {label} – " + (f"{pr['done']} of {pr['due']} sessions done today." if pr["due"]
                           else "Today's sessions start at 8:00.")
    s += f" Best breath {best:,} mL (target {pr['target_ml']:,} mL)." if best else ""
    if pr["streak"]:
        s += f" {pr['streak']} good days in a row. 🔥"
    if last_hr is not None:
        s += f" Last session at {last_hr}:00."
    return s


REPLIES = {
    "done": {"en": "Shabash! ✅ Thank you, {a}. Your SpiroBuddy counts the breaths and ticks it for you.",
             "hi": "शाबाश! ✅ धन्यवाद {a}। आपका SpiroBuddy साँसें गिनकर इसे टिक कर देगा।",
             "ta": "சபாஷ்! ✅ நன்றி {a}. உங்கள் SpiroBuddy மூச்சுகளை எண்ணி டிக் செய்யும்.",
             "ml": "മിടുക്ക്! ✅ നന്ദി {a}. നിങ്ങളുടെ SpiroBuddy ശ്വാസങ്ങൾ എണ്ണി ഇത് രേഖപ്പെടുത്തും."},
    "snooze": {"en": "⏰ Okay {a}, I'll remind you again in 15 minutes.",
               "hi": "⏰ ठीक है {a}, 15 मिनट बाद फिर याद दिलाऊँगा।",
               "ta": "⏰ சரி {a}, 15 நிமிடத்தில் மீண்டும் நினைவூட்டுகிறேன்.",
             "ml": "⏰ ശരി {a}, 15 മിനിറ്റ് കഴിഞ്ഞ് വീണ്ടും ഓർമ്മിപ്പിക്കാം."},
    "call_me": {"en": "📞 Okay {a}, your nurse will call you soon.",
                "hi": "📞 ठीक है {a}, आपकी नर्स जल्द ही आपको कॉल करेंगी।",
                "ta": "📞 சரி {a}, உங்கள் செவிலியர் விரைவில் அழைப்பார்.",
             "ml": "📞 ശരി {a}, നിങ്ങളുടെ നഴ്സ് ഉടൻ വിളിക്കും."},
    "guardian_ack": {"en": "🙏 Thank you, {g}. We've noted that you'll check on {who}.",
                     "hi": "🙏 धन्यवाद {g} जी। हमने नोट कर लिया कि आप {who} का हाल पूछेंगे।",
                     "ta": "🙏 நன்றி {g}. நீங்கள் {who}-ஐ விசாரிப்பீர்கள் என்று குறித்துக்கொண்டோம்.",
             "ml": "🙏 നന്ദി {g}. നിങ്ങൾ {who}-യുടെ വിവരം അന്വേഷിക്കുമെന്ന് ഞങ്ങൾ രേഖപ്പെടുത്തി."},
    "nurse": {"en": "📞 Okay {g}, the nurse will call you back soon.",
              "hi": "📞 ठीक है {g} जी, नर्स जल्द ही आपको कॉल करेंगी।",
              "ta": "📞 சரி {g}, செவிலியர் விரைவில் அழைப்பார்.",
             "ml": "📞 ശരി {g}, നഴ്സ് ഉടൻ തിരികെ വിളിക്കും."},
    "cheer": {"en": "💛 Your cheer is saved. {who} will hear it after the next breathing session.",
              "hi": "💛 आपका संदेश सेव हो गया। अगले व्यायाम के बाद {who} इसे सुनेंगे।",
              "ta": "💛 உங்கள் வாழ்த்து சேமிக்கப்பட்டது. அடுத்த பயிற்சிக்குப் பின் {who} கேட்பார்.",
             "ml": "💛 നിങ്ങളുടെ സന്ദേശം സേവ് ചെയ്തു. അടുത്ത ശ്വസന വ്യായാമത്തിന് ശേഷം {who} ഇത് കേൾക്കും."},
    "unknown_patient": {"en": "Sorry, I didn't understand. Reply 1 = ✅ Done, 2 = ⏰ remind in 15 min, 3 = 📞 talk to the nurse.",
                        "hi": "माफ़ कीजिए, समझ नहीं पाया। 1 = ✅ हो गया, 2 = ⏰ 15 मिनट बाद, 3 = 📞 नर्स से बात।",
                        "ta": "மன்னிக்கவும், புரியவில்லை. 1 = ✅ முடிந்தது, 2 = ⏰ 15 நிமிடம், 3 = 📞 செவிலியர்.",
             "ml": "ക്ഷമിക്കണം, മനസ്സിലായില്ല. 1 = ✅ ചെയ്തു, 2 = ⏰ 15 മിനിറ്റ് കഴിഞ്ഞ്, 3 = 📞 നഴ്സുമായി സംസാരിക്കാൻ."},
    "unknown_guardian": {"en": "Sorry, I didn't understand. Reply 1 = 👍 I'll check, 2 = 📊 today's status, 3 = 📞 talk to the nurse.",
                         "hi": "माफ़ कीजिए, समझ नहीं पाया। 1 = 👍 मैं देखता हूँ, 2 = 📊 आज की स्थिति, 3 = 📞 नर्स से बात।",
                         "ta": "மன்னிக்கவும், புரியவில்லை. 1 = 👍 பார்க்கிறேன், 2 = 📊 இன்றைய நிலை, 3 = 📞 செவிலியர்.",
             "ml": "ക്ഷമിക്കണം, മനസ്സിലായില്ല. 1 = 👍 ഞാൻ നോക്കാം, 2 = 📊 ഇന്നത്തെ സ്ഥിതി, 3 = 📞 നഴ്സുമായി സംസാരിക്കാൻ."},
    "unknown_sender": {"en": "Namaste! This is SpiroBuddy, an automatic breathing-exercise helper. We couldn't match your number to a patient. Please ask the hospital to add you to the care circle. In an emergency, call 112.",
                       "hi": "नमस्ते! यह SpiroBuddy है, एक स्वचालित साँस-व्यायाम सहायक। आपका नंबर किसी मरीज़ से नहीं जुड़ा है। कृपया अस्पताल से आपको जोड़ने को कहें। आपातकाल में 112 पर कॉल करें।"},
}


def reply_text(key: str, lang: str, **kw) -> str:
    d = REPLIES[key]
    return (d.get(lang) or d["en"]).format(**kw)


CHEER_PRESETS = {
    "en": ["You can do it! Ten slow breaths – we're proud of you. 💪",
           "Every breath makes your lungs stronger. Keep going! 🌱",
           "We love you. Get well soon! 💛"],
    "hi": ["आप कर सकते हैं! दस धीमी साँसें – हमें आप पर गर्व है। 💪",
           "हर साँस आपके फेफड़ों को मज़बूत बनाती है। ऐसे ही करते रहिए! 🌱",
           "हम आपसे बहुत प्यार करते हैं। जल्दी ठीक हो जाइए! 💛"],
    "ta": ["உங்களால் முடியும்! பத்து மெதுவான மூச்சுகள் – உங்களைப் பற்றி பெருமை. 💪",
           "ஒவ்வொரு மூச்சும் நுரையீரலை வலுப்படுத்தும். தொடருங்கள்! 🌱",
           "உங்களை நேசிக்கிறோம். விரைவில் குணமடையுங்கள்! 💛"],
    "ml": ["നിങ്ങൾക്ക് കഴിയും! പത്ത് പതുക്കെയുള്ള ശ്വാസങ്ങൾ – ഞങ്ങൾക്ക് നിങ്ങളെക്കുറിച്ച് അഭിമാനമുണ്ട്. 💪",
           "ഓരോ ശ്വാസവും നിങ്ങളെ കൂടുതൽ ശക്തരാക്കുന്നു. തുടരൂ! 🌱",
           "ഞങ്ങൾ നിങ്ങളെ സ്നേഹിക്കുന്നു. വേഗം സുഖമാകട്ടെ! 💛"],
}

# ----------------------------------------------------------------------------- intents

RED_FLAG_RE = re.compile(
    r"chest\s*pain|can'?t\s*breathe|cannot\s*breathe|not\s*able\s*to\s*breathe|short(ness)?\s*of\s*breath|"
    r"breathless|fever|blood|bleed|faint|dizzy|unconscious|emergency|\bsos\b|\bhelp\b|"
    r"सीने में दर्द|छाती में दर्द|साँस नहीं|सांस नहीं|साँस फूल|सांस फूल|बुखार|खून|चक्कर|बेहोश|मदद|बचाओ|"
    r"\bmadad\b|bachao|saans\s*nahi|seene\s*mein\s*dard|bukhar|"
    r"நெஞ்சு வலி|மூச்சு திணறல்|காய்ச்சல்|ரத்தம்|மயக்கம்|உதவி|"
    r"സഹായ|രക്ഷിക്ക", re.I)       # Malayalam "help" / "save me" (needs a native-speaker check, Q-28)

_PATIENT_WORDS = {
    "done": r"^(1|✅.*|done|did it|ho gaya|ho gya|haan|ha|yes|हो गया|हाँ|हां|कर लिया|முடிந்தது|ஆம்|ചെയ്തു|അതെ)$",
    "snooze": r"^(2|⏰.*|later|remind.*|15.*|baad mein|बाद में|15 मिनट.*|பிறகு|15 நிமிடம்|പിന്നീട്|15 മിനിറ്റ്.*)$",
    "call_me": r"^(3|📞.*|call( me)?|call me please|nurse|कॉल.*|मुझे कॉल करें|नर्स|அழைக்கவும்|செவிலியர்|എന്നെ വിളിക്കൂ|വിളിക്കൂ|നഴ്സ്)$",
    "status": r"^(status|sthiti|स्थिति|halat|हाल|progress|நிலை|സ്ഥിതി|📊.*)$",
}
_GUARDIAN_WORDS = {
    "guardian_ack": r"^(1|👍.*|ok|okay|i'?ll check|will check|haan|हाँ|हां|मैं देखता हूँ|मैं देखती हूँ|பார்க்கிறேன்|ഞാൻ നോക്കാം)$",
    "status": r"^(2|status|sthiti|स्थिति|हाल|progress|நிலை|സ്ഥിതി|📊.*)$",
    "nurse": r"^(3|📞.*|nurse|call|नर्स|कॉल.*|செவிலியர்|നഴ്സ്)$",
    "cheer": r"^(cheer|💛|शाबाश|shabash|வாழ்த்து).*$",
}


def detect_intent(body: str, role: str, payload: str | None = None) -> str:
    if payload:
        p = payload.strip().lower()
        valid = ("done", "snooze", "call_me", "status") if role == "patient" else \
            ("guardian_ack", "status", "nurse", "cheer")
        if p in valid or p in ("consent_yes", "stop"):
            return p
    text = (body or "").strip()
    from .consent import STOP_RE
    if STOP_RE.match(text):                 # DPDP: one word withdraws consent
        return "stop"
    from .audio import red_flag as voice_red_flag
    if RED_FLAG_RE.search(text) or voice_red_flag(text):
        return "red_flag"
    low = text.lower().strip(" .!?।")
    for intent, rx in (_PATIENT_WORDS if role == "patient" else _GUARDIAN_WORDS).items():
        if re.match(rx, low, re.I):
            return intent
    return "unknown"


# ----------------------------------------------------------------------------- sending

def content_sid_for(kind: str) -> str | None:
    return {"reminder": env("TWILIO_CONTENT_SID_REMINDER"),
            "guardian_alert": env("TWILIO_CONTENT_SID_GUARDIAN")}.get(kind) or None


def send(patient: dict, role: str, stored_number: str | None, text: str, kind: str,
         lang: str = "en", buttons: list | None = None, media_url: str | None = None,
         to_name: str | None = None, run_id: int | None = None, footer: bool = True,
         content_vars: dict | None = None) -> dict:
    """Send (or dry-run) one WhatsApp message, log it in `messages` and the timeline.

    role: 'patient' | 'family' (guardian) | 'nurse'. Real sends go to the stored number if it is
    real, otherwise to the DEMO_* number for that role (never to a placeholder).
    """
    lang = text_lang(lang, "en")
    # AI disclosure first (reminders/alerts carry it in their own wording; replies get a short tag)
    text = disclosed(text, lang, short=(kind == "reply"))
    body = text + (f"\n\n{FOOTER[lang]}" if footer else "")
    number = resolve_number(stored_number, "guardian" if role == "family" else role)
    to = f"whatsapp:{number}" if number else None
    sid = content_sid_for(kind) if buttons else None
    res = {"sent": False, "dry_run": True}
    mode = "dry_run"
    if whatsapp.whatsapp_enabled() and to:
        if sid:
            whatsapp.throttle()
            res = _send_content(to, sid, content_vars or {"1": first_name(patient.get("name"))})
            mode = "buttons"
        else:
            real_body = body + (f"\n{numbered(buttons, lang)}" if buttons else "")
            if media_url and media_url.startswith("http"):
                whatsapp.throttle()
                res = _send_media(to, real_body, media_url)
                mode = "media"
            else:
                res = whatsapp.send(to, real_body)      # throttles itself (≥3 s between sends)
                mode = "text"
        _remember_result(res)
    logged = service.log_message(patient, kind, role, stored_number or number, body,
                                 res.get("sent", False), res.get("dry_run", True))
    status = "sent" if res.get("sent") else ("dry_run" if res.get("dry_run") else "failed")
    who = {"patient": "patient", "family": "guardian", "nurse": "nurse"}[role]
    log_event(patient["id"], "guardian_whatsapp" if role == "family" else "whatsapp",
              f"WhatsApp to {to_name or who}: {kind.replace('_', ' ')}"
              + (" (would send – dry run)" if status == "dry_run" else " – failed" if status == "failed" else ""),
              detail=text, channel="whatsapp", actor=who, to_name=to_name, status=status,
              run_id=run_id, ref_id=logged.get("id"))
    out = {"sent": bool(res.get("sent")), "dry_run": bool(res.get("dry_run")), "text": body,
           "message_id": logged.get("id"), "mode": mode,
           "buttons": [label for _, label in buttons] if buttons else []}
    if res.get("error"):
        out["error"] = res["error"]
        out["hint"] = error_hint(res["error"])
    return out


MIN_GAP_S = whatsapp.MIN_GAP_S      # Twilio WhatsApp sandbox: at most 1 message every 3 seconds
SANDBOX_FROM = "+14155238886"
last_result: dict = {}             # last real WhatsApp attempt (for /api/comms/status)


def _remember_result(res: dict) -> None:
    last_result.clear()
    last_result.update({"at": iso(now()), "sent": bool(res.get("sent")),
                        "error": res.get("error"),
                        "hint": error_hint(res["error"]) if res.get("error") else None})


def is_sandbox() -> bool:
    return SANDBOX_FROM in env("TWILIO_WHATSAPP_FROM").replace(" ", "")


def sandbox_hint() -> str | None:
    if not is_sandbox():
        return None
    return ("Twilio WhatsApp sandbox: every phone must send 'join <your code>' to +1 415 523 8886. "
            "The sandbox session ends after 3 days – rejoin on demo morning (it also opens the "
            "24-hour window for free-form messages).")


def error_hint(err: str) -> str:
    e = (err or "").lower()
    if "63016" in e or "outside the allowed window" in e or "24" in e and "window" in e:
        return ("Outside WhatsApp's 24-hour window: the person must message first (sandbox: send "
                "'join <code>' again – the sandbox session lasts 3 days) or use an approved template.")
    if "63007" in e or "channel" in e and "not" in e:
        return "TWILIO_WHATSAPP_FROM isn't a WhatsApp-enabled sender (sandbox: whatsapp:+14155238886)."
    if "63015" in e or "sandbox" in e or "join" in e:
        return "Sandbox: rejoin needed – the phone must send 'join <code>' to the sandbox number."
    if "21608" in e or "unverified" in e:
        return "Twilio trial: the number must be verified first."
    return "WhatsApp send failed – see docs/COMMS.md (troubleshooting)."


def _client():
    from twilio.rest import Client
    return Client(env("TWILIO_ACCOUNT_SID"), env("TWILIO_AUTH_TOKEN"))


def _from():
    f = env("TWILIO_WHATSAPP_FROM")
    return f if f.startswith("whatsapp:") else f"whatsapp:{f}"


def _send_content(to: str, content_sid: str, variables: dict) -> dict:
    """Quick-reply buttons via a Twilio Content Template (twilio/quick-reply)."""
    try:
        kw = {"from_": _from(), "to": to, "content_sid": content_sid,
              "content_variables": json.dumps({str(k): str(v) for k, v in variables.items()})}
        ms = env("TWILIO_MESSAGING_SERVICE_SID")
        if ms:
            kw.pop("from_")
            kw["messaging_service_sid"] = ms
        m = _client().messages.create(**kw)
        return {"sent": True, "dry_run": False, "sid": m.sid}
    except Exception as e:
        log.warning("Twilio content send failed: %s", e)
        return {"sent": False, "dry_run": False, "error": str(e)[:300]}


def _send_media(to: str, body: str, media_url: str) -> dict:
    try:
        m = _client().messages.create(from_=_from(), to=to, body=body[:1500], media_url=[media_url])
        return {"sent": True, "dry_run": False, "sid": m.sid}
    except Exception as e:
        log.warning("Twilio media send failed: %s", e)
        return {"sent": False, "dry_run": False, "error": str(e)[:300]}


def send_reminder(patient: dict, cfg: dict, missed: int, run_id: int | None = None) -> dict:
    lang = text_lang(patient.get("language"), "en")
    btns = PATIENT_BUTTONS[lang]
    return send(patient, "patient", cfg.get("patient_phone"), reminder_text(patient, lang, missed),
                "reminder", lang, buttons=btns, to_name=first_name(patient["name"]), run_id=run_id)


def send_guardian_alert(patient: dict, guardian: dict, missed: int, patient_answered: bool,
                        run_id: int | None = None, red_flag: bool = False) -> dict:
    lang = text_lang(guardian.get("language"), "en")
    return send(patient, "family", guardian.get("phone"),
                guardian_alert_text(patient, guardian, missed, patient_answered, red_flag),
                "guardian_alert", lang, buttons=GUARDIAN_BUTTONS[lang],
                to_name=f"{first_name(guardian['name'])} ({guardian.get('relation') or 'family'})",
                run_id=run_id, content_vars={"1": first_name(guardian["name"]),
                                             "2": first_name(patient["name"])})


def care_update_recipient(patient: dict, to_role: str) -> tuple[dict | None, str, str | None, str | None]:
    """For /api/whatsapp/{pid}: -> (guardian, lang, stored number, blocked_reason).

    'family' goes to the primary guardian in the care circle, in the guardian's language, and
    only with their recorded consent (a guardian who replied STOP is blocked). 'nurse' is
    hospital staff (not an automated message to a patient/family), so no consent is needed.
    """
    from .common import has_consent
    from .guardians import guardian_label, primary_guardian
    if to_role == "nurse":
        return None, "en", patient.get("nurse_phone"), None
    g = primary_guardian(int(patient["id"]))
    if not g:
        return None, "en", patient.get("family_phone"), "no guardian with recorded consent in the care circle"
    lang = text_lang(g.get("language"), "en")
    if not has_consent(g):
        return g, lang, g.get("phone"), (f"{guardian_label(g)} has not given consent or replied STOP – "
                                         "no automated WhatsApp sent")
    return g, lang, g.get("phone") or patient.get("family_phone"), None


def send_care_update(patient: dict, kind: str, to_role: str, text: str, lang: str,
                     guardian: dict | None = None, stored_number: str | None = None,
                     blocked_reason: str | None = None) -> dict:
    """The nurse dashboard's 'send summary / missed alert' (CONTRACT D: {sent, dry_run, text, to_role}).

    Goes through `send` (AI disclosure in the recipient's language, footer, shared ≥3 s throttle,
    logging). When consent blocks it nothing is sent: sent=false, dry_run=false + error.
    """
    if blocked_reason:
        from .guardians import guardian_label
        name = guardian_label(guardian) if guardian else "family"
        log_event(patient["id"], "guardian_whatsapp", f"WhatsApp to {name}: {kind} blocked – no consent",
                  detail=blocked_reason, channel="whatsapp", actor="guardian", to_name=name,
                  status="skipped")
        return {"sent": False, "dry_run": False, "text": text, "to_role": to_role,
                "blocked": True, "blocked_reason": blocked_reason, "error": blocked_reason}
    to_name = None
    if guardian:
        to_name = f"{first_name(guardian['name'])} ({guardian.get('relation') or 'family'})"
    out = send(patient, to_role, stored_number, text, kind, lang, to_name=to_name)
    out["to_role"] = to_role
    return out


# ----------------------------------------------------------------------------- inbound

def identify(from_number: str | None) -> tuple[dict | None, str | None, dict | None]:
    """-> (patient, role 'patient'|'guardian', guardian) from a phone number."""
    n = e164(from_number)
    if not n:
        return None, None, None
    from .guardians import get_settings
    for p in st().select("patients"):
        if e164(get_settings(p["id"]).get("patient_phone")) == n:
            return p, "patient", None
    for g in st().select("guardians"):
        if e164(g.get("phone")) == n:
            return service.get_patient_row(g["patient_id"]), "guardian", g
    if n == e164(env("DEMO_PATIENT_PHONE")):
        return service.get_patient_row(1), "patient", None
    if n in (e164(env("DEMO_GUARDIAN_PHONE")), e164(env("DEMO_FAMILY_WHATSAPP"))):
        from .guardians import primary_guardian
        return service.get_patient_row(1), "guardian", primary_guardian(1)
    return None, None, None


def handle_inbound(body: str, from_number: str | None = None, payload: str | None = None,
                   patient_id: int | None = None, role: str | None = None,
                   guardian_id: int | None = None, channel: str = "whatsapp",
                   send_reply: bool = True) -> dict:
    """One inbound reply (real webhook or the browser WhatsApp simulator) -> action + reply."""
    from . import escalation
    from .guardians import get_guardian, primary_guardian
    guardian = None
    if patient_id is not None:
        patient = service.get_patient_row(int(patient_id))
        role = role if role in ("patient", "guardian") else "patient"
        if role == "guardian":
            guardian = get_guardian(guardian_id) if guardian_id else primary_guardian(int(patient_id))
    else:
        patient, role, guardian = identify(from_number)
    full_body = (body or "").strip()        # intent (STOP / red flag) is read from the WHOLE message
    body = full_body[:1000]
    if not patient:
        reply = reply_text("unknown_sender", "en")
        st().insert("inbound_messages", [{"patient_id": None, "guardian_id": None,
                                          "from_number": from_number, "from_role": "unknown",
                                          "from_name": None, "channel": channel, "body": body,
                                          "intent": "unknown", "reply": reply, "created_at": iso(now())}])
        return {"intent": "unknown", "reply": reply, "patient_id": None, "role": None}

    lang = text_lang((guardian or {}).get("language") if role == "guardian" else patient.get("language"), "en")
    intent = detect_intent(full_body or payload or "", role, payload)
    if intent not in ("stop", "consent_yes", "red_flag") and _last_out_kind(patient["id"], role, guardian) == "consent_renewal":
        # the last question was "keep the reminders?": 1/yes = keep, 2 = stop
        low = (body or "").strip().lower().strip(" .!।")
        if low in ("1", "yes", "haan", "हाँ", "हां", "ஆம்", "അതെ", "ok", "okay") or intent in ("done", "guardian_ack"):
            intent = "consent_yes"
        elif low in ("2", "no", "nahi", "नहीं", "இல்லை", "വേണ്ട", "ഇല്ല"):
            intent = "stop"
    a = addr(patient, lang)
    g_first = first_name((guardian or {}).get("name")) or "ji"
    who = call_name((guardian or {}).get("relation"), patient, lang)
    from_name = guardian["name"] if guardian else patient["name"]
    actor = "guardian" if role == "guardian" else "patient"
    log_event(patient["id"], "inbound", f"{first_name(from_name)} replied “{body or payload}”",
              detail=f"Understood as: {intent.replace('_', ' ')}", channel=channel, actor=actor,
              to_name=first_name(from_name), status="info")

    if intent == "red_flag":
        escalation.red_flag(patient["id"], body, source=f"{actor} message ({channel})",
                            from_guardian=guardian)
        reply = RED_FLAG_TEXT[lang] + " " + NURSE_TOLD[lang]
    elif intent in ("stop", "consent_yes"):
        from . import consent
        consent.apply(patient["id"], role, guardian, intent == "consent_yes",
                      f"Reply “{body or payload}” via {channel}")
        reply = consent.REPLY[intent][lang]
        if intent == "stop":
            run = escalation.active_run(patient["id"])
            if run and role == "patient":
                escalation.resolve(run, "stopped_by_patient", "Patient said STOP – automated steps stopped "
                                   "(nurse alert still possible)", "patient")
    elif role == "patient" and intent in ("done", "snooze", "call_me"):
        escalation.patient_response(patient["id"], intent, source=f"WhatsApp ({channel})")
        reply = reply_text(intent, lang, a=a)
    elif role == "guardian" and intent in ("guardian_ack", "nurse"):
        escalation.guardian_response(patient["id"], guardian, intent, source=f"WhatsApp ({channel})")
        reply = reply_text(intent, lang, g=g_first, who=who)
    elif intent == "status":
        reply = status_text(patient["id"], lang, guardian if role == "guardian" else None)
    elif intent == "cheer" and role == "guardian":
        text = body if len(body) > 8 else CHEER_PRESETS[lang][0]
        queue_cheer(patient["id"], guardian, text, lang)
        reply = reply_text("cheer", lang, who=who)
    else:
        reply = reply_text("unknown_guardian" if role == "guardian" else "unknown_patient", lang)

    st().insert("inbound_messages", [{
        "patient_id": patient["id"], "guardian_id": (guardian or {}).get("id"),
        "from_number": from_number, "from_role": role, "from_name": from_name, "channel": channel,
        "body": body or payload, "intent": intent, "reply": reply, "created_at": iso(now())}])
    out = {"intent": intent, "reply": reply, "patient_id": patient["id"], "role": role}
    if send_reply:
        r = send(patient, "family" if role == "guardian" else "patient",
                 (guardian or {}).get("phone") if role == "guardian" else None, reply, "reply",
                 lang, to_name=first_name(from_name), footer=False)
        out["reply_sent"] = r["sent"]
        out["reply_dry_run"] = r["dry_run"]
    return out


def _last_out_kind(pid: int, role: str, guardian: dict | None) -> str | None:
    """Kind of the newest automated message (not a reply) sent to this person."""
    to_role = "family" if role == "guardian" else "patient"
    rows = st().select("messages", [("patient_id", "eq", int(pid)), ("to_role", "eq", to_role)],
                       order="id", desc=True, limit=6)
    for m in rows:
        if m.get("kind") == "reply":
            continue
        if role == "guardian" and guardian and m.get("to_number") not in (guardian.get("phone"), None):
            continue
        return m.get("kind")
    return None


# ----------------------------------------------------------------------------- cheers

def queue_cheer(pid: int, guardian: dict | None, text: str, lang: str) -> dict:
    row = {"patient_id": int(pid), "guardian_id": (guardian or {}).get("id"),
           "from_name": (guardian or {}).get("name") or "Family", "text": text[:300],
           "language": lang, "status": "queued", "created_at": iso(now()), "played_at": None}
    r = st().insert("cheers", [row])[0]
    log_event(pid, "cheer", f"Cheer queued from {first_name(row['from_name'])}",
              detail=text, channel="web", actor="guardian", to_name=first_name(row["from_name"]),
              status="info", ref_id=r.get("id"))
    return r


def mark_cheers_played(pid: int, after_session_hour: int | None = None) -> list[dict]:
    rows = st().select("cheers", [("patient_id", "eq", int(pid)), ("status", "eq", "queued")])
    t = iso(now())
    for c in rows:
        st().update("cheers", [("id", "eq", c["id"])], {"status": "played", "played_at": t})
        when = f" after the {after_session_hour}:00 session" if after_session_hour is not None else ""
        log_event(pid, "cheer", f"Cheer from {first_name(c.get('from_name'))} played to the patient{when}",
                  detail=c.get("text") or "", channel="device", actor="patient",
                  status="ok", ref_id=c["id"])
    return rows
