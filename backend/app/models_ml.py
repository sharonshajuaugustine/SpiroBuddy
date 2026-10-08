"""Breath classifier: uses ml/predict.py (load / predict) when present, else the rule fallback.

Also wraps ml/synth.make_breath with a small internal generator as fallback.
"""
from __future__ import annotations

import importlib
import json
import logging
import subprocess
import sys

import numpy as np

from . import rules
from .config import FEATURE_KEYS, LABELS, ML_DIR, ROOT

log = logging.getLogger("spirobuddy.ml")

_predict_mod = None
_model_loaded = False
_load_error = ""

_PROBE = {"peak_ml": 1800, "pct_target": 0.9, "time_to_peak_s": 3.1, "mean_rise_ml_s": 580,
          "max_rise_ml_s": 900, "hold_s": 3.2, "smoothness": 0.12, "duration_s": 8.4}


def load() -> bool:
    """(Re)load ml/predict.py and its model. Safe if ml/ doesn't exist yet."""
    global _predict_mod, _model_loaded, _load_error
    _predict_mod, _model_loaded, _load_error = None, False, ""
    try:
        mod = importlib.import_module("ml.predict")
        mod = importlib.reload(mod)
        mod.load()
        out = mod.predict(dict(_PROBE))          # probe: the model must actually answer
        if not isinstance(out, dict) or out.get("label") not in LABELS:
            raise ValueError(f"unexpected predict() output: {out!r}")
        _predict_mod, _model_loaded = mod, True
        log.info("ML model loaded from ml/predict.py")
    except Exception as e:  # ImportError, missing model.joblib, anything
        _load_error = f"{type(e).__name__}: {e}"
        log.warning("ML model not available, using rules (%s)", _load_error)
    return _model_loaded


def model_loaded() -> bool:
    return _model_loaded


def load_error() -> str:
    return _load_error


def classify(features: dict) -> dict:
    """-> {label, proba:{good,too_fast,too_shallow,no_hold}, source:"model"|"rules"}"""
    feats = rules.clean_features(features)
    if _model_loaded and _predict_mod is not None:
        try:
            out = _predict_mod.predict(feats)
            label = out.get("label")
            if label in LABELS:
                proba = {l: round(float((out.get("proba") or {}).get(l, 0.0)), 4) for l in LABELS}
                return {"label": label, "proba": proba, "source": "model"}
        except Exception as e:
            log.warning("model predict failed, using rules: %s", e)
    return rules.rule_classify(feats)


# ----------------------------------------------------------------------------- training

def train(timeout_s: int = 600) -> dict:
    script = ML_DIR / "train.py"
    if not script.exists():
        return {"ok": False, "error": "ml/train.py not found yet"}
    proc = subprocess.run([sys.executable, str(script)], cwd=str(ROOT), capture_output=True,
                          text=True, timeout=timeout_s)
    ok = proc.returncode == 0
    load()
    out = {"ok": ok, "model_loaded": _model_loaded,
           "log_tail": (proc.stdout + proc.stderr)[-1500:]}
    out.update(metrics() or {})
    return out


def metrics() -> dict | None:
    path = ML_DIR / "metrics.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": f"metrics.json unreadable: {e}"}


# ----------------------------------------------------------------------------- breath generator

def _internal_breath(label: str, target_ml: float, rng: np.random.Generator) -> tuple[list, dict]:
    """Small fallback generator: plausible features (and a coarse curve) per label."""
    u = rng.uniform
    if label == "too_fast":
        peak = target_ml * u(0.6, 1.0); ttp = u(0.6, 1.3); hold = u(0.8, 3.0)
    elif label == "too_shallow":
        peak = target_ml * u(0.2, 0.45); ttp = u(2.0, 4.0); hold = u(1.2, 3.5)
    elif label == "no_hold":
        peak = target_ml * u(0.6, 1.0); ttp = u(2.5, 4.5); hold = u(0.0, 0.8)
    else:
        peak = target_ml * u(0.75, 1.05); ttp = u(2.5, 4.5); hold = u(2.5, 5.0)
    mean_rise = peak / ttp
    max_rise = mean_rise * u(1.25, 1.6)
    if label == "too_fast":
        max_rise = max(max_rise, u(1500, 2600))
    elif max_rise > 880:
        max_rise = u(700, 880)
    fall = u(1.5, 3.5)
    feats = {"peak_ml": round(peak, 1), "pct_target": round(peak / target_ml, 3),
             "time_to_peak_s": round(ttp, 2), "mean_rise_ml_s": round(mean_rise, 1),
             "max_rise_ml_s": round(max_rise, 1), "hold_s": round(hold, 2),
             "smoothness": round(u(0.25, 0.6) if label == "too_fast" else u(0.05, 0.22), 3),
             "duration_s": round(ttp + hold + fall, 2)}
    samples, t, dt = [], 0.0, 1 / 30
    while t <= feats["duration_s"]:
        if t < ttp:
            v = peak * (t / ttp) ** 0.8
        elif t < ttp + hold:
            v = peak * u(0.93, 1.0)
        else:
            v = peak * max(0.0, 1 - (t - ttp - hold) / fall)
        samples.append({"t": int(t * 1000), "ml": round(v, 1)})
        t += dt
    return samples, feats


def make_breath(label: str, target_ml: float, rng: np.random.Generator) -> tuple[list, dict]:
    """ml.synth.make_breath if importable and sane, else the internal generator."""
    try:
        synth = importlib.import_module("ml.synth")
        samples, feats = synth.make_breath(label, target_ml, rng)
        feats = {k: float(feats[k]) for k in FEATURE_KEYS}
        return list(samples) if samples is not None else [], feats
    except Exception:
        return _internal_breath(label, target_ml, rng)
