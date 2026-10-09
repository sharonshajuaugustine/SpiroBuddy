"""AI daily summary (3 sentences, English or Hindi) with a template fallback.

Claude via the Anthropic Python SDK, model claude-opus-5-5, effort "low", max_tokens 400.
Falls back to template text when there is no ANTHROPIC_API_KEY, on any error, on a
non-"end_turn" stop_reason (refusal, max_tokens...), or if the text sounds like a diagnosis.
The AI never diagnoses: it only coaches and summarises the numbers it is given.
"""
from __future__ import annotations

import logging
import re

from .config import env

log = logging.getLogger("spirobuddy.llm")

MODEL = "claude-opus-5-5"
LANG_NAMES = {"en": "English", "hi": "Hindi (Devanagari script)", "ta": "Tamil (Tamil script)"}

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


def llm_enabled() -> bool:
    return bool(env("ANTHROPIC_API_KEY"))


def template_summary(stats: dict, language: str) -> str:
    name = stats["first_name"]
    done, due = stats["done"], stats["due"]
    best, target = int(stats["best_ml"]), int(stats["target_ml"])
    if language == "hi":
        s1 = f"{name} ने आज {due} में से {done} साँस-व्यायाम सत्र पूरे किए।"
        if best:
            s2 = f"आज की सबसे अच्छी साँस {best} mL रही, लक्ष्य {target} mL है।"
        else:
            s2 = f"आज अभी तक कोई साँस दर्ज नहीं हुई, लक्ष्य {target} mL है।"
        s3 = ("कृपया हर घंटे धीरे-धीरे गहरी साँस लेने और 3 सेकंड रोकने के लिए प्रोत्साहित करें।"
               if done < due or best < target else "बहुत बढ़िया, ऐसे ही हर घंटे अभ्यास जारी रखें।")
        return " ".join([s1, s2, s3])
    s1 = f"{name} completed {done} of {due} breathing sessions today."
    if best:
        s2 = f"The best breath today was {best} mL against a target of {target} mL."
    else:
        s2 = f"No breaths have been recorded yet today; the target is {target} mL."
    s3 = ("Please encourage a slow, deep breath with a 3-second hold every hour."
           if done < due or best < target else "Great work - keep practising every hour like this.")
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
    )


def summarize(stats: dict, language: str = "en") -> dict:
    """-> {text, source: "llm"|"template"}"""
    language = language if language in LANG_NAMES else "en"
    fallback_lang = "hi" if language == "hi" else "en"
    if not llm_enabled():
        return {"text": template_summary(stats, fallback_lang), "source": "template"}
    try:
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
        text = " ".join(b.text for b in resp.content if b.type == "text").strip()
        if not text:
            raise RuntimeError("empty response")
        if _DIAGNOSIS_WORDS.search(text):
            raise RuntimeError("summary contained medical/diagnostic wording")
        return {"text": text, "source": "llm"}
    except Exception as e:
        log.warning("LLM summary failed, using template: %s", e)
        return {"text": template_summary(stats, fallback_lang), "source": "template"}
