"""Train the breath classifier. Run from the repo root:  python ml/train.py

Data:
- synthetic breaths from ml/synth.py (always)
- real breaths from backend/data/breaths_labelled.csv if it exists, weighted x3.
  CSV columns (header row required):
    person,label,peak_ml,pct_target,time_to_peak_s,mean_rise_ml_s,max_rise_ml_s,hold_s,smoothness,duration_s
  label is one of good / too_fast / too_shallow / no_hold.

Output: ml/model.joblib  (dict: model, feature_keys, labels, created_at)
        ml/metrics.json  (accuracy, per-class report, confusion matrix, counts,
                          rule agreement, leave-one-person-out if 3+ real people)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402

from ml.features import FEATURE_KEYS, LABELS, rule_label  # noqa: E402
from ml.synth import make_dataset  # noqa: E402

ML_DIR = ROOT / "ml"
REAL_CSV = ROOT / "backend" / "data" / "breaths_labelled.csv"
REAL_WEIGHT = 3.0


def _model(seed):
    return RandomForestClassifier(
        n_estimators=200, min_samples_leaf=2, class_weight="balanced",
        random_state=seed, n_jobs=-1,
    )


def load_real(path=REAL_CSV):
    if not Path(path).exists():
        return None
    df = pd.read_csv(path)
    missing = [c for c in ["person", "label", *FEATURE_KEYS] if c not in df.columns]
    if missing:
        print(f"[train] ignoring {path}: missing columns {missing}")
        return None
    df = df[df["label"].isin(LABELS)].dropna(subset=FEATURE_KEYS)
    df["person"] = df["person"].astype(str)
    return df if len(df) else None


def train(n_per_label=600, seed=42, out_dir=ML_DIR):
    synth = make_dataset(n_per_label, seed)
    synth["source"] = "synthetic"
    real = load_real()
    parts = [synth]
    if real is not None:
        real = real.assign(source="real")
        parts.append(real[["person", "label", *FEATURE_KEYS, "source"]])
    df = pd.concat(parts, ignore_index=True)
    X = df[FEATURE_KEYS].to_numpy(float)
    y = df["label"].to_numpy()
    w = np.where(df["source"] == "real", REAL_WEIGHT, 1.0)

    Xtr, Xte, ytr, yte, wtr, _, _, src_te = train_test_split(
        X, y, w, df["source"].to_numpy(), test_size=0.2, stratify=y, random_state=seed)
    clf = _model(seed).fit(Xtr, ytr, sample_weight=wtr)
    pred = clf.predict(Xte)
    syn_mask = src_te == "synthetic"

    rules_te = np.array([rule_label(dict(zip(FEATURE_KEYS, row))) for row in Xte])
    metrics = {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": "RandomForestClassifier(n_estimators=200, min_samples_leaf=2)",
        "feature_keys": FEATURE_KEYS,
        "labels": LABELS,
        "n_samples": int(len(df)),
        "n_synthetic": int((df["source"] == "synthetic").sum()),
        "n_real": int((df["source"] == "real").sum()),
        "n_real_people": int(real["person"].nunique()) if real is not None else 0,
        "n_test": int(len(yte)),
        "accuracy": round(float(accuracy_score(yte, pred)), 4),
        "accuracy_synthetic_test": round(float(accuracy_score(yte[syn_mask], pred[syn_mask])), 4)
        if syn_mask.any() else None,
        "rules_accuracy_on_test": round(float(accuracy_score(yte, rules_te)), 4),
        "per_class": {
            k: {m: round(float(v), 4) for m, v in d.items()}
            for k, d in classification_report(yte, pred, labels=LABELS, output_dict=True,
                                              zero_division=0).items()
            if k in LABELS
        },
        "confusion_matrix": {"labels": LABELS,
                             "matrix": confusion_matrix(yte, pred, labels=LABELS).tolist()},
        "feature_importance": {k: round(float(v), 4)
                               for k, v in zip(FEATURE_KEYS, clf.feature_importances_)},
        "leave_one_person_out": None,
    }

    # Leave-one-person-out on real data (train on everything except that person)
    if real is not None and real["person"].nunique() >= 3:
        per = {}
        for p in sorted(real["person"].unique()):
            held = (df["source"] == "real") & (df["person"] == p)
            m = _model(seed).fit(X[~held], y[~held], sample_weight=w[~held])
            per[p] = {"n": int(held.sum()),
                      "accuracy": round(float(accuracy_score(y[held], m.predict(X[held]))), 4)}
        accs = [v["accuracy"] for v in per.values()]
        metrics["leave_one_person_out"] = {"mean_accuracy": round(float(np.mean(accs)), 4),
                                           "per_person": per}

    # Final model on all data
    final = _model(seed).fit(X, y, sample_weight=w)
    out_dir = Path(out_dir)
    joblib.dump({"model": final, "feature_keys": FEATURE_KEYS, "labels": LABELS,
                 "created_at": metrics["created_at"]}, out_dir / "model.joblib", compress=3)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main():
    ap = argparse.ArgumentParser(description="Train the SpiroBuddy breath classifier")
    ap.add_argument("--n-per-label", type=int, default=600)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    m = train(a.n_per_label, a.seed)
    print(f"[train] samples={m['n_samples']} (real={m['n_real']}) test={m['n_test']}")
    print(f"[train] model accuracy={m['accuracy']}  rules accuracy={m['rules_accuracy_on_test']}")
    for lab in LABELS:
        pc = m["per_class"].get(lab, {})
        print(f"  {lab:12s} precision={pc.get('precision')} recall={pc.get('recall')} f1={pc.get('f1-score')}")
    print("[train] confusion (rows=true):", LABELS)
    for lab, row in zip(LABELS, m["confusion_matrix"]["matrix"]):
        print(f"  {lab:12s} {row}")
    if m["leave_one_person_out"]:
        print(f"[train] leave-one-person-out mean accuracy={m['leave_one_person_out']['mean_accuracy']}")
    print(f"[train] saved {ML_DIR / 'model.joblib'} and {ML_DIR / 'metrics.json'}")


if __name__ == "__main__":
    main()
