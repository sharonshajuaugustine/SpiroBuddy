"""Load the trained model once and classify breath features.

    from ml import predict
    predict.load()                      # -> True if ml/model.joblib loaded
    predict.predict(features)           # -> {"label": "good", "proba": {...}}
    predict.is_loaded()

If no model is loaded, predict() falls back to the rule label (proba 1.0).
"""
from __future__ import annotations

from pathlib import Path

from ml.features import FEATURE_KEYS, LABELS, rule_label

DEFAULT_PATH = Path(__file__).resolve().parent / "model.joblib"
_bundle = None


def load(path=None) -> bool:
    global _bundle
    p = Path(path) if path else DEFAULT_PATH
    try:
        import joblib
        b = joblib.load(p)
        if isinstance(b, dict) and "model" in b:
            _bundle = b
        else:  # bare estimator
            _bundle = {"model": b, "feature_keys": FEATURE_KEYS}
        try:  # single-threaded prediction is much faster for one row
            _bundle["model"].set_params(n_jobs=1)
        except Exception:
            pass
        return True
    except Exception:
        _bundle = None
        return False


def is_loaded() -> bool:
    return _bundle is not None


def predict(features) -> dict:
    if _bundle is None:
        lab = rule_label(features)
        return {"label": lab, "proba": {l: (1.0 if l == lab else 0.0) for l in LABELS}}
    import numpy as np
    keys = _bundle.get("feature_keys", FEATURE_KEYS)
    x = np.array([[float(features.get(k, 0) or 0) for k in keys]])
    model = _bundle["model"]
    probs = model.predict_proba(x)[0]
    proba = {l: 0.0 for l in LABELS}
    for cls, p in zip(model.classes_, probs):
        proba[str(cls)] = round(float(p), 3)
    label = max(proba, key=proba.get)
    return {"label": label, "proba": proba}
