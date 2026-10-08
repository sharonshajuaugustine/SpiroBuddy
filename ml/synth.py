"""Synthetic incentive-spirometer breaths (about 30 samples per second).

Each breath = short rest -> inhale (rise) -> hold near the top -> piston falls
-> rest. Shape, speed, depth, hold and sensor noise vary per "person" and per
breath. About 15% of breaths are deliberately borderline (near the rule
thresholds), so the rules and the model do not agree 100% of the time.

make_breath(label, target_ml=2000, rng=None) -> (samples, features)
    samples = [{"t": seconds, "ml": volume}, ...]
make_dataset(n_per_label, seed) -> pandas DataFrame (person, label, 8 features)
"""
from __future__ import annotations

import numpy as np

from ml.features import FEATURE_KEYS, LABELS, extract_features

FS = 30.0  # samples per second
BORDERLINE_P = 0.15


def _person(rng):
    return {
        "speed": rng.uniform(0.85, 1.15),     # tends to breathe faster/slower
        "capacity": rng.uniform(0.9, 1.08),   # lung capacity vs target
        "hold": rng.uniform(0.8, 1.2),        # tends to hold longer/shorter
        "noise": rng.uniform(3.0, 14.0),      # sensor noise, mL
        "tremor": rng.uniform(0.0, 25.0),     # wobble while inhaling, mL
        "shape": rng.uniform(0.0, 0.7),       # 0 = smooth S-curve, 1 = fast start
    }


def _params(label, rng, person):
    """Return (pct_of_target, max_rise_rate, wanted_hold_s, borderline).

    wanted_hold_s is the time we want at >= 90% of peak (what hold_s measures);
    make_curve subtracts the part already spent near the top of the rise/fall.
    """
    border = rng.random() < BORDERLINE_P
    sp, cap, ho = person["speed"], person["capacity"], person["hold"]
    if label == "good":
        if border:
            kind = rng.integers(3)
            pct = rng.uniform(0.48, 0.62) if kind == 0 else rng.uniform(0.65, 1.1)
            rate = rng.uniform(1150, 1500) if kind == 1 else rng.uniform(400, 1100)
            hold = rng.uniform(0.7, 1.3) if kind == 2 else rng.uniform(1.6, 4.5)
            return pct, rate, hold, True
        return (rng.uniform(0.62, 1.15) * cap, rng.uniform(320, 1150) * sp,
                rng.uniform(1.5, 5.0) * ho, False)
    if label == "too_fast":
        rate = rng.uniform(1250, 1600) if border else rng.uniform(1550, 3600) * sp
        return rng.uniform(0.45, 1.15) * cap, rate, rng.uniform(0.0, 4.0), border
    if label == "too_shallow":
        pct = rng.uniform(0.44, 0.56) if border else rng.uniform(0.12, 0.47) * cap
        return pct, rng.uniform(200, 1150) * sp, rng.uniform(0.0, 4.0), border
    if label == "no_hold":
        hold = rng.uniform(0.75, 1.25) if border else rng.uniform(0.05, 0.75) / ho
        return rng.uniform(0.52, 1.1) * cap, rng.uniform(320, 1250) * sp, hold, border
    raise ValueError(f"unknown label {label!r}")


def _unit_rise(x, w):
    """Unit rise 0..1: mix of a smooth S-curve and a fast-start curve."""
    s = 0.5 - 0.5 * np.cos(np.pi * x)
    f = 1 - (1 - x) ** 2
    return (1 - w) * s + w * f


def _median5(v):
    pad = np.pad(v, 2, mode="edge")
    win = np.lib.stride_tricks.sliding_window_view(pad, 5)
    return np.median(win, axis=1)


def make_curve(pct, rate, hold_s, target_ml, rng, person, fall=None, stop=1.0):
    """stop < 1 = the inhale is cut off abruptly before it levels out."""
    peak = max(pct * target_ml, 60.0)
    w = float(np.clip(person["shape"] + rng.normal(0, 0.1), 0, 1))

    def rise(x):
        return _unit_rise(x * stop, w) / _unit_rise(stop, w)

    xs = np.linspace(0, 1, 201)
    unit_slope = np.max(np.diff(rise(xs)) / np.diff(xs))
    ttp = float(np.clip(peak * unit_slope / rate, 0.25, 8.0))

    pre = rng.uniform(0.3, 0.8)
    if fall is None:
        fall = rng.uniform(0.5, 1.4)
    # time already >= 90% of peak during the top of the rise and start of the fall
    top_rise = ttp * (1 - xs[np.argmax(rise(xs) >= 0.9)])
    plateau_s = max(0.0, hold_s - top_rise - 0.2 * fall)
    post = rng.uniform(0.3, 0.8)
    total = pre + ttp + plateau_s + fall + post
    t = np.arange(0, total, 1 / FS)
    v = np.zeros_like(t)

    r = (t >= pre) & (t < pre + ttp)
    x = (t[r] - pre) / ttp
    v[r] = peak * rise(x)
    # tremor while inhaling (bigger for fast, jerky breaths)
    jerk = person["tremor"] * (1.5 if rate > 1400 else 1.0)
    v[r] += jerk * np.sin(2 * np.pi * rng.uniform(2, 6) * t[r] + rng.uniform(0, 6)) * np.sin(np.pi * x)

    h0 = pre + ttp
    h = (t >= h0) & (t < h0 + plateau_s)
    sag = rng.uniform(0.0, 0.07)
    if plateau_s > 0:
        v[h] = peak * (1 - sag * (t[h] - h0) / plateau_s)
    top = peak * (1 - sag) if plateau_s > 0 else peak

    f0 = h0 + plateau_s
    f = (t >= f0) & (t < f0 + fall)
    v[f] = top * (0.5 + 0.5 * np.cos(np.pi * (t[f] - f0) / fall))

    v = v + rng.normal(0, person["noise"], size=len(v))
    v = np.clip(_median5(v), 0, None)
    return t, v


def make_breath(label, target_ml=2000, rng=None, person=None):
    """Return (samples, features) for one synthetic breath of the given label."""
    if rng is None:
        rng = np.random.default_rng()
    elif isinstance(rng, (int, np.integer)):
        rng = np.random.default_rng(rng)
    if person is None:
        person = _person(rng)
    pct, rate, hold, _ = _params(label, rng, person)
    if label == "no_hold":  # stops inhaling abruptly and lets go quickly
        fall, stop = rng.uniform(0.3, 0.7), rng.uniform(0.6, 0.85)
    else:
        fall, stop = None, rng.uniform(0.85, 1.0)
    t, v = make_curve(pct, rate, hold, target_ml, rng, person, fall, stop)
    samples = [{"t": round(float(a), 3), "ml": round(float(b), 1)} for a, b in zip(t, v)]
    return samples, extract_features(samples, target_ml)


def make_dataset(n_per_label=500, seed=0, breaths_per_person=20):
    """DataFrame with columns: person, label, <8 features>."""
    import pandas as pd

    rng = np.random.default_rng(seed)
    rows = []
    n_people = max(1, (n_per_label * len(LABELS)) // breaths_per_person)
    people = [_person(rng) for _ in range(n_people)]
    for label in LABELS:
        for i in range(n_per_label):
            pid = int(rng.integers(n_people))
            target = float(rng.choice([1500, 1750, 2000, 2250, 2500]))
            _, feats = make_breath(label, target, rng, people[pid])
            rows.append({"person": f"synth_{pid}", "label": label, **feats})
    return pd.DataFrame(rows, columns=["person", "label", *FEATURE_KEYS])
