"""SpiroBuddy communications: escalation ladder, automated calls, WhatsApp, alerts, guardians.

Everything works with no keys (dry run + browser simulators). See docs/COMMS.md and
ARCHITECTURE.md CONTRACT D2. Modules:
  common      shared helpers (time, quiet hours, names, events, settings)
  guardians   care circle (guardians, patient phone, ladder settings, magic links)
  alerts      nurse alerts inbox
  messages    WhatsApp texts in en/hi/ta, sending, inbound replies (1/2/3, status, help)
  calls       automated calls: Twilio Voice / Exotel / dry run, TwiML, keypresses
  escalation  the ladder engine + background tick + auto triggers
  trend       lower-than-usual trend flag (observation, never a diagnosis)
  cards       weekly progress card PNG (Pillow)
  script      AI nurse call script (Claude + template fallback)
  audio       bridge to backend/app/voice.py (natural Indian-language voices)
  seed_comms  demo guardians, alerts and escalation history
"""


def raise_alert(patient_id: int, kind: str = "help", text: str = "", severity: str = "amber") -> dict:
    """Public hook for other modules (e.g. routes_voice /api/voice/stt): put an alert in the
    nurse's inbox. kind='red_flag' runs the full red-flag flow (red alert, family told, quiet
    hours ignored). Never raises."""
    import logging
    try:
        if kind == "red_flag":
            from .escalation import red_flag
            red_flag(int(patient_id), text or "red-flag words", source="voice question")
            return {"ok": True, "kind": kind}
        from . import alerts
        from .common import log_event, patient
        p = patient(int(patient_id)) or {"name": f"Patient {patient_id}"}
        sev = severity if severity in ("red", "amber", "info") else "amber"
        titles = {"question": f"{p['name']} asked a question", "help": f"{p['name']} asked for help"}
        a = alerts.raise_alert(int(patient_id), kind if kind in alerts.KINDS else "help", sev,
                               titles.get(kind, f"{p['name']}: {kind.replace('_', ' ')}"),
                               detail=(text or "")[:1000], dedupe_hours=1)
        log_event(int(patient_id), "inbound", f"Voice message from {p['name'].split()[0]}",
                  detail=text or "", channel="voice", actor="patient", status="info",
                  ref_id=a.get("id"))
        return {"ok": True, "alert_id": a.get("id")}
    except Exception as e:
        logging.getLogger("spirobuddy.comms").warning("raise_alert failed: %s", e)
        return {"ok": False, "error": str(e)}
