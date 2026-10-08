"""Breath features, score and rule label (CONTRACT C in docs/ARCHITECTURE.md).

Input samples: list of {"t": seconds, "ml": volume}. Time is in SECONDS.
(If the timestamps look like milliseconds - median step > 1.0 - they are
converted to seconds automatically, because the browser sources emit ms.)

Definitions used (keep in sync with web/ JS):
- onset          = first sample with vol >= 10% of peak
- rising segment = onset .. peak sample
- peak_ml        = max volume
- pct_target     = peak_ml / target_ml
- time_to_peak_s = t[peak] - t[onset]
- mean_rise_ml_s = (peak - vol[onset]) / time_to_peak_s
- max_rise_ml_s  = largest rise rate over any 0.3 s window inside the rising
                   segment: (vol[j] - vol[i]) / (t[j] - t[i]) where j is the
                   first sample >= t[i] + 0.3 s. Segment shorter than 0.3 s ->
                   uses the whole segment.
- hold_s         = total time with vol >= 0.9 x peak (each sample counts for
                   the gap to the next sample)
- smoothness     = std(diff(vol over rising segment)) / mean(diff(...)),
                   lower = smoother; 0 if fewer than 3 points or mean <= 0
- duration_s     = t[last sample with vol >= 10% of peak] - t[onset]
"""
from __future__ import annotations

import numpy as np

FEATURE_KEYS = [
    "peak_ml", "pct_target", "time_to_peak_s", "mean_rise_ml_s",
    "max_rise_ml_s", "hold_s", "smoothness", "duration_s",
]
LABELS = ["good", "too_fast", "too_shallow", "no_hold"]

RISE_WINDOW_S = 0.3


def _arrays(samples):
    t = np.asarray([float(s["t"]) for s in samples], dtype=float)
    v = np.asarray([float(s["ml"]) for s in samples], dtype=float)
    order = np.argsort(t, kind="stable")
    t, v = t[order], v[order]
    if len(t) > 1 and np.median(np.diff(t)) > 1.0:  # looks like milliseconds
        t = t / 1000.0
    return t, v


def extract_features(samples, target_ml=2000):
    """samples: list of {t (seconds), ml}. Returns dict with FEATURE_KEYS order."""
    zero = {k: 0.0 for k in FEATURE_KEYS}
    if not samples:
        return zero
    t, v = _arrays(samples)
    peak_i = int(np.argmax(v))
    peak = float(v[peak_i])
    if peak <= 0:
        return zero

    above = np.nonzero(v >= 0.1 * peak)[0]
    onset = int(above[0])
    end = int(above[-1])

    ttp = float(t[peak_i] - t[onset])
    rise_t, rise_v = t[onset:peak_i + 1], v[onset:peak_i + 1]
    mean_rise = (peak - float(v[onset])) / ttp if ttp > 0 else 0.0

    # max rise over 0.3 s windows
    if ttp <= RISE_WINDOW_S or len(rise_t) < 2:
        max_rise = mean_rise
    else:
        js = np.searchsorted(rise_t, rise_t + RISE_WINDOW_S, side="left")
        ok = js < len(rise_t)
        i_idx = np.nonzero(ok)[0]
        j_idx = js[ok]
        dt = rise_t[j_idx] - rise_t[i_idx]
        rates = (rise_v[j_idx] - rise_v[i_idx]) / np.where(dt > 0, dt, np.inf)
        max_rise = float(rates.max()) if len(rates) else mean_rise
        max_rise = max(max_rise, mean_rise)

    # hold: time at >= 90% of peak
    dts = np.diff(t, append=t[-1])
    hold = float(dts[v >= 0.9 * peak].sum())

    d = np.diff(rise_v)
    if len(d) >= 2 and d.mean() > 0:
        smooth = float(d.std() / d.mean())
    else:
        smooth = 0.0

    feats = {
        "peak_ml": round(peak, 1),
        "pct_target": round(peak / float(target_ml), 3) if target_ml else 0.0,
        "time_to_peak_s": round(ttp, 3),
        "mean_rise_ml_s": round(mean_rise, 1),
        "max_rise_ml_s": round(max_rise, 1),
        "hold_s": round(hold, 3),
        "smoothness": round(smooth, 3),
        "duration_s": round(float(t[end] - t[onset]), 3),
    }
    return {k: feats[k] for k in FEATURE_KEYS}


def score(features, target_ml, hold_target_s=3):
    """0-10 score, one decimal (CONTRACT C)."""
    peak = float(features.get("peak_ml", 0))
    depth = 4 * min(peak / target_ml, 1) if target_ml else 0
    mr = float(features.get("max_rise_ml_s", 0))
    speed = 3 if mr <= 900 else (1 if mr <= 1400 else 0)
    hold = 3 * min(float(features.get("hold_s", 0)) / hold_target_s, 1) if hold_target_s else 0
    return round(max(depth, 0) + speed + max(hold, 0), 1)


def rule_label(features):
    """Rule fallback label (CONTRACT C)."""
    if float(features.get("max_rise_ml_s", 0)) > 1400:
        return "too_fast"
    if float(features.get("pct_target", 0)) < 0.5:
        return "too_shallow"
    if float(features.get("hold_s", 0)) < 1.0:
        return "no_hold"
    return "good"
