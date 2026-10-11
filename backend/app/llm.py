"""AI daily summary (3 sentences; English, Hindi, Tamil or Malayalam) with a template fallback.

Provider order: Anthropic -> Gemini -> template (spec §5 "AI").
  1. Claude via the Anthropic Python SDK, model claude-opus-5-5, effort "low", max_tokens 400
     (only when ANTHROPIC_API_KEY is set).
  2. Gemini via ai_gemini.summarize_text (only when GEMINI_API_KEY is set).
  3. Template text: no key, any error, a stop reason other than a normal finish (refusal,
     max_tokens, safety block...), an empty answer, or text that sounds like a diagnosis.
The same checks apply to both providers. The AI never diagnoses: it only coaches and
summarises the numbers it is given.
"""
from __future__ import annotations

import logging
import re

from .config import env

log = logging.getLogger("spirobuddy.llm")

MODEL = "claude-opus-5-5"
LANG_NAMES = {"en": "English", "hi": "Hindi (Devanagari script)", "ta": "Tamil (Tamil script)",
              "ml": "Malayalam (Malayalam script)"}

SYSTEM = (
    "You write short daily progress updates for SpiroBuddy, a breathing-exercise coach used at "
    "home after surgery with an incentive spirometer. The reader is the patient's family or "
    "nurse. Write exactly 3 short, warm, plain sentences: what was done today, how the "
    "breathing went compared with the target, and one encouraging, practical tip about the "
    "exercise (slow deep breath, hold, regular hourly practice). Use only the numbers given. "
    "Never diagnose, never name diseases or complications, never give medical or medication "
    "advice. If the numbers look worrying, only say the care team will check in. No greeting, "
    "no sign-off, no markdown, no emojis."
)

# Words that must never appear in an AI summary -> use the template instead.
_DIAGNOSIS_WORDS = re.compile(
    r"diagnos|pneumonia|atelectasis|infection|embolism|copd|asthma|fever|antibiotic|"
    r"tuberculosis|\btb\b|cancer|medicine|medication|dose|disease", re.I)


def anthropic_enabled() -> bool:
    return bool(env("ANTHROPIC_API_KEY"))


def gemini_enabled() -> bool:
    return bool(env("GEMINI_API_KEY"))


def providers() -> list[str]:
    """The AI providers that have a key, in the order they are tried."""
    return [name for name, on in (("anthropic", anthropic_enabled()), ("gemini", gemini_enabled()))
            if on]


def llm_enabled() -> bool:
    """True when at least one AI provider has a key (otherwise every summary is the template)."""
    return bool(providers())


def add_recent(stats: dict, detail: dict) -> dict:
    """Before the first slot (8 am) nothing is due yet today: attach yesterday's numbers (or, if
    yesterday is empty, the last few days) from patient_detail()['history'] so the summary can say
    something useful instead of "0 of 0" (Q-29). Returns `stats` (changed in place)."""
    if stats.get("due"):
        return stats
    hist = list(detail.get("history") or [])[:-1]          # last item is today
    if not hist:
        return stats
    y = hist[-1]
    if y.get("sessions_done"):
        stats["recent"] = {"days": 1, "sessions": int(y["sessions_done"]),
                           "best_ml": int(y.get("best_ml") or 0)}
        return stats
    days = [h for h in hist if h.get("sessions_done")]
    if days:
        stats["recent"] = {"days": len(hist), "sessions": sum(int(h["sessions_done"]) for h in days),
                           "best_ml": int(max(h.get("best_ml") or 0 for h in days))}
    return stats


# Template text. ta/ml strings were written without a native speaker: NEEDS A NATIVE-SPEAKER CHECK.
# Family-facing text: never names a disease or the operation.
_T = {
    "en": {
        "today": "{name} completed {done} of {due} breathing sessions today.",
        "best": "The best breath today was {best} mL against a target of {target} mL.",
        "nobest": "No breaths have been recorded yet today; the target is {target} mL.",
        "tip": "Please encourage a slow, deep breath with a 3-second hold every hour.",
        "great": "Great work - keep practising every hour like this.",
        "early": "{name}'s breathing sessions for today start at 8 am, so none are due yet.",
        "yday": "Yesterday {name} did {n} breathing sessions, with a best breath of {best} mL "
                "against a target of {target} mL.",
        "recent": "Over the last {days} days {name} did {n} breathing sessions, with a best breath of "
                  "{best} mL against a target of {target} mL.",
        "early_tip": "Once the day starts, please encourage a slow, deep breath with a 3-second hold "
                     "every hour.",
    },
    "hi": {
        "today": "{name} ने आज {due} में से {done} साँस-व्यायाम सत्र पूरे किए।",
        "best": "आज की सबसे अच्छी साँस {best} mL रही, लक्ष्य {target} mL है।",
        "nobest": "आज अभी तक कोई साँस दर्ज नहीं हुई, लक्ष्य {target} mL है।",
        "tip": "कृपया हर घंटे धीरे-धीरे गहरी साँस लेने और 3 सेकंड रोकने के लिए प्रोत्साहित करें।",
        "great": "बहुत बढ़िया, ऐसे ही हर घंटे अभ्यास जारी रखें।",
        "early": "{name} के आज के साँस-व्यायाम सुबह 8 बजे शुरू होंगे, अभी कोई सत्र बाकी नहीं है।",
        "yday": "कल {name} ने {n} सत्र पूरे किए, सबसे अच्छी साँस {best} mL रही (लक्ष्य {target} mL)।",
        "recent": "पिछले {days} दिनों में {name} ने {n} सत्र पूरे किए, सबसे अच्छी साँस {best} mL रही "
                  "(लक्ष्य {target} mL)।",
        "early_tip": "दिन शुरू होने पर कृपया हर घंटे धीरे-धीरे गहरी साँस लेने और 3 सेकंड रोकने के लिए "
                     "प्रोत्साहित करें।",
    },
    "ta": {
        "today": "{name} இன்று {due} இல் {done} மூச்சுப் பயிற்சி அமர்வுகளை முடித்தார்.",
        "best": "இன்றைய சிறந்த மூச்சு {best} mL, இலக்கு {target} mL.",
        "nobest": "இன்று இதுவரை மூச்சு எதுவும் பதிவாகவில்லை; இலக்கு {target} mL.",
        "tip": "ஒவ்வொரு மணி நேரமும் மெதுவாக ஆழ்ந்த மூச்சு எடுத்து 3 வினாடி நிறுத்த ஊக்குவியுங்கள்.",
        "great": "மிக நன்று, ஒவ்வொரு மணி நேரமும் இப்படியே பயிற்சியைத் தொடருங்கள்.",
        "early": "{name}-இன் இன்றைய மூச்சுப் பயிற்சிகள் காலை 8 மணிக்குத் தொடங்கும்; இப்போது எதுவும் "
                 "நிலுவையில் இல்லை.",
        "yday": "நேற்று {name} {n} அமர்வுகளை முடித்தார்; சிறந்த மூச்சு {best} mL (இலக்கு {target} mL).",
        "recent": "கடந்த {days} நாட்களில் {name} {n} அமர்வுகளை முடித்தார்; சிறந்த மூச்சு {best} mL "
                  "(இலக்கு {target} mL).",
        "early_tip": "நாள் தொடங்கியதும், ஒவ்வொரு மணி நேரமும் மெதுவாக ஆழ்ந்த மூச்சு எடுத்து 3 வினாடி "
                     "நிறுத்த ஊக்குவியுங்கள்.",
    },
    "ml": {
        "today": "{name} ഇന്ന് {due}-ൽ {done} ശ്വസന വ്യായാമ സെഷനുകൾ പൂർത്തിയാക്കി.",
        "best": "ഇന്നത്തെ ഏറ്റവും നല്ല ശ്വാസം {best} mL ആയിരുന്നു, ലക്ഷ്യം {target} mL ആണ്.",
        "nobest": "ഇന്ന് ഇതുവരെ ശ്വാസമൊന്നും രേഖപ്പെടുത്തിയിട്ടില്ല, ലക്ഷ്യം {target} mL ആണ്.",
        "tip": "ദയവായി ഓരോ മണിക്കൂറിലും പതുക്കെ ആഴത്തിൽ ശ്വാസമെടുത്ത് 3 സെക്കൻഡ് പിടിച്ചുനിർത്താൻ "
               "പ്രോത്സാഹിപ്പിക്കുക.",
        "great": "വളരെ നന്നായി, ഓരോ മണിക്കൂറിലും ഇതുപോലെ പരിശീലനം തുടരൂ.",
        "early": "{name}-ന്റെ ഇന്നത്തെ ശ്വസന വ്യായാമങ്ങൾ രാവിലെ 8 മണിക്ക് തുടങ്ങും; ഇപ്പോൾ ഒന്നും "
                 "ചെയ്യേണ്ടതില്ല.",
        "yday": "ഇന്നലെ {name} {n} സെഷനുകൾ ചെയ്തു; ഏറ്റവും നല്ല ശ്വാസം {best} mL (ലക്ഷ്യം {target} mL).",
        "recent": "കഴിഞ്ഞ {days} ദിവസങ്ങളിൽ {name} {n} സെഷനുകൾ ചെയ്തു; ഏറ്റവും നല്ല ശ്വാസം {best} mL "
                  "(ലക്ഷ്യം {target} mL).",
        "early_tip": "ദിവസം തുടങ്ങുമ്പോൾ, ഓരോ മണിക്കൂറിലും പതുക്കെ ആഴത്തിൽ ശ്വാസമെടുത്ത് 3 സെക്കൻഡ് "
                     "പിടിച്ചുനിർത്താൻ പ്രോത്സാഹിപ്പിക്കുക.",
    },
}


def template_summary(stats: dict, language: str) -> str:
    t = _T.get(language) or _T["en"]
    name = stats["first_name"]
    done, due = stats["done"], stats["due"]
    best, target = int(stats["best_ml"]), int(stats["target_ml"])
    if not due:                     # before 8 am: nothing due yet -> no "0 of 0" (Q-29)
        parts = [t["early"].format(name=name)]
        r = stats.get("recent")
        if r and r.get("sessions"):
            key = "yday" if r["days"] == 1 else "recent"
            parts.append(t[key].format(name=name, n=r["sessions"], days=r["days"],
                                       best=r["best_ml"], target=target))
        parts.append(t["early_tip"])
        return " ".join(parts)
    s1 = t["today"].format(name=name, done=done, due=due)
    s2 = (t["best"] if best else t["nobest"]).format(best=best, target=target)
    s3 = t["tip"] if done < due or best < target else t["great"]
    return " ".join([s1, s2, s3])


def _prompt(stats: dict, language: str) -> str:
    lc = stats.get("label_counts", {})
    return (
        f"Write the update in {LANG_NAMES.get(language, 'English')}.\n"
        f"Patient first name: {stats['first_name']}\n"
        # The operation/condition is deliberately NOT sent: family-facing text never names it (Q-23).
        "Context: recovering at home, doing a daily breathing exercise\n"
        f"Sessions done today: {stats['done']} of {stats['due']} due so far\n"
        f"Best breath today: {int(stats['best_ml'])} mL (target {int(stats['target_ml'])} mL, "
        f"personal best {int(stats['personal_best_ml'])} mL)\n"
        f"Average score today: {stats.get('avg_score') if stats.get('avg_score') is not None else 'n/a'} / 10\n"
        f"Breaths today - good: {lc.get('good', 0)}, too fast: {lc.get('too_fast', 0)}, "
        f"too shallow: {lc.get('too_shallow', 0)}, no hold: {lc.get('no_hold', 0)}\n"
        f"7-day trend of best breath: {stats.get('trend', 'flat')}\n"
        f"Missed sessions in a row right now: {stats.get('trailing_missed', 0)}"
        + _early_note(stats)
    )


def _early_note(stats: dict) -> str:
    """Before the first slot: tell the model nothing is due yet and give recent days (Q-29)."""
    if stats.get("due"):
        return ""
    note = ("\nIt is before today's first session (8 am), so no sessions are due yet today. "
            "Do not say '0 of 0'; say today's sessions start at 8 am")
    r = stats.get("recent")
    if r and r.get("sessions"):
        when = "Yesterday" if r["days"] == 1 else f"Last {r['days']} days"
        note += (f", and summarise the recent days instead.\n{when}: {r['sessions']} sessions done, "
                 f"best breath {r['best_ml']} mL")
    return note + "."


def _anthropic_text(stats: dict, language: str, patient_id=None) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"), timeout=30.0,
                                 max_retries=1)
    # Server-side refusal fallback (beta) so a safety-classifier refusal is retried on a
    # substitute model instead of failing; our own template is the final fallback.
    resp = client.beta.messages.create(
        model=MODEL,
        max_tokens=400,
        output_config={"effort": "low"},
        system=SYSTEM,
        messages=[{"role": "user", "content": _prompt(stats, language)}],
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if resp.stop_reason != "end_turn":
        raise RuntimeError(f"stop_reason={resp.stop_reason}")
    return " ".join(b.text for b in resp.content if b.type == "text").strip()


def _gemini_text(stats: dict, language: str, patient_id=None) -> str:
    """Same instructions and numbers as the Anthropic call. ai_gemini refuses any finish reason
    other than a normal stop, applies the daily AI limit and writes the AI register row."""
    from . import ai_gemini
    text = ai_gemini.summarize_text(SYSTEM + "\n\n" + _prompt(stats, language), patient_id=patient_id)
    if text is None:
        raise RuntimeError("no answer from Gemini")
    return text.strip()


def _ai_consent_blocks(patient_id) -> bool:
    """True when this patient's consent record says "no AI" (or has no AI consent at all)."""
    try:
        from . import ai_gemini
        return ai_gemini.consent_ai(patient_id) is not True
    except Exception as e:
        log.warning("could not read the AI consent, using template: %s", e)
        return True


def summarize(stats: dict, language: str = "en", *, patient_id: int | None = None) -> dict:
    """-> {text, source: "llm"|"template"}

    Tries each provider that has a key (Anthropic, then Gemini); the first clean answer wins,
    otherwise the template. Pass patient_id to enforce the patient's AI consent (consent v2):
    with "no AI" the template is used and no AI call is made."""
    language = language if language in LANG_NAMES else "en"
    fallback_lang = language if language in _T else "en"
    names = providers()
    if names and patient_id is not None and _ai_consent_blocks(patient_id):
        names = []
    for name in names:
        try:
            call = _anthropic_text if name == "anthropic" else _gemini_text
            text = call(stats, language, patient_id)
            if not text:
                raise RuntimeError("empty response")
            if _DIAGNOSIS_WORDS.search(text):
                raise RuntimeError("summary contained medical/diagnostic wording")
            return {"text": text, "source": "llm"}
        except Exception as e:
            log.warning("LLM summary failed (%s), trying the next option: %s", name, e)
    return {"text": template_summary(stats, fallback_lang), "source": "template"}
