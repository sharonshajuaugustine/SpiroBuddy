"""Care circle: guardians (joint-family friendly), the patient's own phone, quiet hours and the
escalation-ladder settings, plus guardian magic links (no login)."""
from __future__ import annotations

import copy
import secrets

from ..config import iso
from .common import (CONSENT_RENEW_DAYS, TEXT_LANGS, call_name, consent_age_days, default_quiet,
                     first_name, has_consent, now, st, to_dt, valid_hm)

STEP_KEYS = ["device", "patient_whatsapp", "patient_call", "guardian", "nurse"]
STEP_LABELS = {
    "device": "Device beep + teal light",
    "patient_whatsapp": "WhatsApp reminder to the patient (✅ Done / ⏰ 15 min / 📞 Call me)",
    "patient_call": "Automated call to the patient (press 1 / 2 / 3)",
    "guardian": "Guardian WhatsApp + call",
    "nurse": "Nurse alert (red on the dashboard)",
}
DEFAULT_DELAYS = {"device": 0, "patient_whatsapp": 10, "patient_call": 10, "guardian": 15,
                  "nurse": 15}
CHANNELS = ("whatsapp", "call", "sms", "both")
CALL_STYLES = ("ivr", "agent")


def default_config() -> dict:
    qs, qe = default_quiet()
    return {
        "patient_phone": None,
        # Recorded consent for automated calls/WhatsApp (TRAI / Twilio India rules; DPDP Act).
        # No consent -> the ladder skips calls/messages to the patient and logs why.
        "consent": False,
        "consent_at": None,
        "quiet_start": qs, "quiet_end": qe,
        "trigger_missed": 2,          # missed hourly sessions in a row that start the ladder
        "auto": True,                 # start the ladder automatically
        "snooze_min": 15,
        "ring_s": 30,                 # how long a real call rings before "no answer"
        # Patient reminder call: "ivr" = press 1/2/3 menu; "agent" = conversational AI check-in
        # ("Are you okay? Why did you miss it?" – Sarvam Voice Agent, or the browser simulator).
        "call_style": "ivr",
        "steps": [{"key": k, "enabled": True, "delay_min": DEFAULT_DELAYS[k]} for k in STEP_KEYS],
    }


def get_settings(pid: int) -> dict:
    cfg = default_config()
    rows = st().select("care_settings", [("patient_id", "eq", int(pid))])
    stored = (rows[0].get("config") if rows else None) or {}
    if isinstance(stored, dict):
        for k, v in stored.items():
            if k == "steps" and isinstance(v, list):
                by_key = {s.get("key"): s for s in v if isinstance(s, dict)}
                cfg["steps"] = [{**d, **{kk: vv for kk, vv in by_key.get(d["key"], {}).items()
                                         if kk in ("enabled", "delay_min")}}
                                for d in cfg["steps"]]
            elif k in cfg:
                cfg[k] = v
    return cfg


def put_settings(pid: int, patch: dict) -> dict:
    cfg = get_settings(pid)
    if "patient_phone" in patch:
        v = patch["patient_phone"]
        cfg["patient_phone"] = (str(v).strip() or None) if v is not None else None
    for k in ("quiet_start", "quiet_end"):
        if patch.get(k) is not None:
            if not valid_hm(patch[k]):
                raise ValueError(f"{k} must be HH:MM (24 h, IST)")
            cfg[k] = patch[k]
    if patch.get("trigger_missed") is not None:
        n = int(patch["trigger_missed"])
        if not 1 <= n <= 6:
            raise ValueError("trigger_missed must be 1..6")
        cfg["trigger_missed"] = n
    for k, lo, hi in (("snooze_min", 5, 60), ("ring_s", 10, 60)):
        if patch.get(k) is not None:
            n = int(patch[k])
            if not lo <= n <= hi:
                raise ValueError(f"{k} must be {lo}..{hi}")
            cfg[k] = n
    if patch.get("auto") is not None:
        cfg["auto"] = bool(patch["auto"])
    if patch.get("call_style") is not None:
        if patch["call_style"] not in CALL_STYLES:
            raise ValueError("call_style must be ivr or agent")
        cfg["call_style"] = patch["call_style"]
    if patch.get("consent") is not None:
        if bool(patch["consent"]) and not cfg.get("consent"):
            cfg["consent_at"] = iso(now())
        cfg["consent"] = bool(patch["consent"])
        if not cfg["consent"]:
            cfg["consent_at"] = None
    if patch.get("renew_consent") and cfg.get("consent"):
        cfg["consent_at"] = iso(now())          # consent re-confirmed today
    if isinstance(patch.get("steps"), list):
        by_key = {s.get("key"): s for s in patch["steps"] if isinstance(s, dict)}
        new = []
        for s in cfg["steps"]:
            p = by_key.get(s["key"], {})
            s = dict(s)
            if "enabled" in p:
                s["enabled"] = bool(p["enabled"])
            if p.get("delay_min") is not None:
                d = int(p["delay_min"])
                if not 0 <= d <= 180:
                    raise ValueError("delay_min must be 0..180")
                s["delay_min"] = d
            new.append(s)
        cfg["steps"] = new
    st().upsert("care_settings", [{"patient_id": int(pid), "config": cfg,
                                   "updated_at": iso(now())}])
    return cfg


def settings_public(pid: int) -> dict:
    cfg = copy.deepcopy(get_settings(pid))
    for s in cfg["steps"]:
        s["label"] = STEP_LABELS[s["key"]]
    _consent_info(cfg, cfg)
    return cfg


def _consent_info(out: dict, src: dict) -> None:
    """consent_ok = flag + date recorded; renew_due = older than 7 days (TRAI 'ongoing use')."""
    age = consent_age_days(src)
    out["consent_ok"] = has_consent(src)
    out["consent_age_days"] = age
    out["consent_renew_due"] = bool(out["consent_ok"] and age is not None and age >= CONSENT_RENEW_DAYS)


# ----------------------------------------------------------------------------- guardians

def new_token() -> str:
    return secrets.token_urlsafe(9)


def list_guardians(pid: int) -> list[dict]:
    rows = st().select("guardians", [("patient_id", "eq", int(pid))], order="id")
    rows.sort(key=lambda g: (not g.get("is_primary"), g.get("id") or 0))
    return rows


def get_guardian(gid: int) -> dict | None:
    rows = st().select("guardians", [("id", "eq", int(gid))])
    return rows[0] if rows else None


def by_token(token: str) -> dict | None:
    if not token or len(token) > 64:
        return None
    rows = st().select("guardians", [("token", "eq", token)])
    return rows[0] if rows else None


def primary_guardian(pid: int) -> dict | None:
    g = list_guardians(pid)
    return g[0] if g else None


def _clean(body: dict, partial: bool) -> dict:
    out = {}
    if not partial or "name" in body:
        name = str(body.get("name") or "").strip()
        if not name:
            raise ValueError("name is required")
        out["name"] = name[:80]
    if "relation" in body or not partial:
        out["relation"] = (str(body.get("relation") or "").strip().lower() or None)
    if "phone" in body or not partial:
        out["phone"] = (str(body.get("phone") or "").strip() or None)
    if "city" in body:
        out["city"] = (str(body.get("city") or "").strip() or None)
    if "language" in body or not partial:
        lang = str(body.get("language") or "hi")
        if lang not in TEXT_LANGS:
            raise ValueError("language must be en, hi, ta or ml")
        out["language"] = lang
    if "channel" in body or not partial:
        ch = str(body.get("channel") or "both")
        if ch not in CHANNELS:
            raise ValueError("channel must be whatsapp, call, sms or both")
        out["channel"] = ch
    for k in ("quiet_start", "quiet_end"):
        if k in body:
            v = body.get(k)
            if v in (None, ""):
                out[k] = None
            elif not valid_hm(v):
                raise ValueError(f"{k} must be HH:MM")
            else:
                out[k] = v
    if "is_primary" in body:
        out["is_primary"] = bool(body["is_primary"])
    if "consent" in body:
        out["consent"] = bool(body["consent"])
        out["consent_at"] = iso(now()) if out["consent"] else None
    return out


def create_guardian(pid: int, body: dict) -> dict:
    row = _clean(body, partial=False)
    row.update({"patient_id": int(pid), "token": new_token(), "created_at": iso(now())})
    row.setdefault("is_primary", not list_guardians(pid))
    if row["is_primary"]:
        st().update("guardians", [("patient_id", "eq", int(pid))], {"is_primary": False})
    return st().insert("guardians", [row])[0]


def update_guardian(gid: int, body: dict) -> dict | None:
    g = get_guardian(gid)
    if not g:
        return None
    vals = _clean(body, partial=True)
    if vals.get("is_primary"):
        st().update("guardians", [("patient_id", "eq", g["patient_id"])], {"is_primary": False})
    if body.get("new_link"):
        vals["token"] = new_token()
    if vals:
        st().update("guardians", [("id", "eq", int(gid))], vals)
    return get_guardian(gid)


def delete_guardian(gid: int) -> bool:
    g = get_guardian(gid)
    if not g:
        return False
    st().delete("guardians", [("id", "eq", int(gid))])
    return True


def public_guardian(g: dict, patient: dict | None = None) -> dict:
    out = {k: g.get(k) for k in ("id", "patient_id", "name", "relation", "phone", "language",
                                 "channel", "city", "quiet_start", "quiet_end", "token")}
    out["is_primary"] = bool(g.get("is_primary"))
    out["consent"] = bool(g.get("consent"))
    ca = to_dt(g.get("consent_at"))
    out["consent_at"] = iso(ca) if ca else None
    _consent_info(out, g)
    out["link"] = f"guardian.html?t={g.get('token')}"
    if patient:
        out["calls_patient"] = call_name(g.get("relation"), patient, g.get("language") or "en")
    created = to_dt(g.get("created_at"))
    out["created_at"] = iso(created) if created else None
    return out


def guardian_quiet(g: dict, cfg: dict) -> tuple[str, str]:
    return (g.get("quiet_start") or cfg["quiet_start"], g.get("quiet_end") or cfg["quiet_end"])


def guardian_label(g: dict) -> str:
    rel = f" ({g['relation']})" if g.get("relation") else ""
    return f"{first_name(g.get('name'))}{rel}"
