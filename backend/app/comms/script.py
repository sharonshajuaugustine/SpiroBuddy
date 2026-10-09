"""AI nurse call script: "Ravi ji missed 3 hours; ask about pain; suggest a session now."

Claude (same settings as llm.py: claude-opus-5-5, effort low, short output) with a template
fallback when there's no key, on any error, or if the text strays into diagnosis/medication.
The script only helps the nurse open the call – it never diagnoses.
"""
from __future__ import annotations

import logging
import re

from .. import llm, service
from ..config import env
from .common import first_name, lang_of, st
from .trend import evaluate

log = logging.getLogger("spirobuddy.comms.script")

SYSTEM = (
    "You draft a short phone-call script for a nurse who is about to call a patient at home after "
    "surgery about their incentive-spirometer breathing exercise (SpiroBuddy). Output 5 short "
    "lines, each starting with '• ': 1) a warm opening line to say in the patient's language "
    "(use 'ji' after the first name for Hindi/English), 2) what the data shows in plain words, "
    "3) two gentle questions to ask (how they feel, whether deep breaths are uncomfortable), "
    "4) a suggestion to do a 10-breath session now while on the call, 5) a reminder to follow "
    "the hospital's red-flag protocol if they report breathlessness at rest, chest pain or "
    "fever. Use only the facts given. Never diagnose, never name diseases or complications, "
    "never suggest medicines or doses. No markdown other than the bullets, no emojis."
)
_BAD = re.compile(r"diagnos|pneumonia|atelectasis|embolism|infection|antibiotic|medication|"
                  r"medicine|dose|mg\b|tablet", re.I)


def facts(pid: int) -> dict | None:
    d = service.patient_detail(int(pid))
    if not d:
        return None
    missed_hours = [s["hour"] for s in d["today"] if s["status"] == "missed"]
    trailing = d.get("trailing_missed", 0)
    ev = evaluate(d)
    evs = st().select("escalation_events", [("patient_id", "eq", int(pid))], order="id",
                      desc=True, limit=8)
    lc = service.summary_stats(d).get("label_counts", {})
    return {"name": d["name"], "first": first_name(d["name"]), "age": d.get("age"),
            "sex": d.get("sex"), "surgery": d.get("surgery"), "language": d.get("language"),
            "done": d["done_today"], "due": d["due_today"], "trailing": trailing,
            "missed_hours": missed_hours[-4:], "best": int(d["best_today"] or 0),
            "target": d["target_ml"], "trend": ev, "too_fast": lc.get("too_fast", 0),
            "no_hold": lc.get("no_hold", 0), "too_shallow": lc.get("too_shallow", 0),
            "recent_events": [e.get("title") for e in evs][:5]}


LANG_OPEN = {
    "hi": "नमस्ते {f} जी, मैं SpiroBuddy क्लिनिक से नर्स बोल रही हूँ। आप कैसे हैं?",
    "ta": "வணக்கம் {f}, நான் SpiroBuddy மருத்துவமனையிலிருந்து செவிலியர் பேசுகிறேன். எப்படி இருக்கிறீர்கள்?",
    "en": "Namaste {f} ji, this is your nurse calling from the SpiroBuddy clinic. How are you feeling today?",
}


def template(f: dict) -> str:
    lang = lang_of(f.get("language"), "en")
    lines = [f"• Open ({ {'hi': 'Hindi', 'ta': 'Tamil', 'en': 'English'}[lang] }): "
             f"“{LANG_OPEN[lang].format(f=f['first'])}”"]
    data = f"{f['first']} has done {f['done']} of {f['due']} sessions today"
    if f["trailing"] >= 2:
        hrs = ", ".join(f"{h}:00" for h in f["missed_hours"][-f['trailing']:])
        data += f" and missed the last {f['trailing']} in a row ({hrs})"
    if f["best"]:
        data += f"; best breath {f['best']:,} mL of a {f['target']:,} mL target"
    if f["trend"].get("flag"):
        data += f" – about {f['trend']['pct_below']}% lower than {('her' if (f.get('sex') or '').upper() == 'F' else 'his')} own 3-day average"
    lines.append(f"• What the data shows: {data}.")
    q = "Ask: “How are you feeling today?” and “Is it uncomfortable or painful to take a deep breath?”"
    if f["too_fast"] >= 3:
        q += " Many breaths were too fast – remind them to breathe in slowly."
    lines.append(f"• {q}")
    lines.append("• Suggest a 10-breath session now while you stay on the line: slow, deep breath in, "
                 "hold for 3 seconds, then rest.")
    lines.append("• If they report breathlessness at rest, chest pain or fever, follow the hospital's "
                 "red-flag protocol (tell them to call 112 in an emergency).")
    return "\n".join(lines)


def generate(pid: int) -> dict | None:
    f = facts(pid)
    if not f:
        return None
    if not llm.llm_enabled():
        return {"text": template(f), "source": "template", "facts": _public_facts(f)}
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"), timeout=30.0, max_retries=1)
        prompt = (f"Patient: {f['first']} ({f['age']} y, {f['sex']}), {f['surgery']}. Speaks "
                  f"{ {'hi': 'Hindi', 'ta': 'Tamil', 'en': 'English'}.get(f['language'], 'English') }.\n"
                  f"Sessions today: {f['done']} of {f['due']} due; missed in a row now: {f['trailing']} "
                  f"(hours {', '.join(str(h) + ':00' for h in f['missed_hours'])}).\n"
                  f"Best breath today: {f['best']} mL, target {f['target']} mL.\n"
                  f"Trend: {f['trend'].get('text') or 'no lower-than-usual flag'}\n"
                  f"Breath quality today: too fast {f['too_fast']}, no hold {f['no_hold']}, "
                  f"too shallow {f['too_shallow']}.\n"
                  f"Recent reminders: {'; '.join(t for t in f['recent_events'] if t) or 'none'}")
        resp = client.beta.messages.create(
            model=llm.MODEL, max_tokens=400, output_config={"effort": "low"}, system=SYSTEM,
            messages=[{"role": "user", "content": prompt}],
            betas=["server-side-fallback-2026-07-01"], fallbacks="default")
        if resp.stop_reason != "end_turn":
            raise RuntimeError(f"stop_reason={resp.stop_reason}")
        text = " ".join(b.text for b in resp.content if b.type == "text").strip()
        if not text or _BAD.search(text):
            raise RuntimeError("empty or medical wording")
        return {"text": text, "source": "llm", "facts": _public_facts(f)}
    except Exception as e:
        log.warning("AI call script failed, using template: %s", e)
        return {"text": template(f), "source": "template", "facts": _public_facts(f)}


def _public_facts(f: dict) -> dict:
    return {k: f[k] for k in ("done", "due", "trailing", "missed_hours", "best", "target")} | {
        "trend_flag": bool(f["trend"].get("flag")), "trend_text": f["trend"].get("text")}
