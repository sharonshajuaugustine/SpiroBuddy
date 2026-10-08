# ml/ – the breath classifier

This folder teaches a small model to sort each breath into one of four labels:
**good**, **too_fast**, **too_shallow**, **no_hold**.

## Files
| File | What it does |
|---|---|
| `features.py` | Turns a breath (a list of `{t, ml}` points, `t` in **seconds**) into the 8 numbers from CONTRACT C. Also `score()` (0–10) and `rule_label()` (the simple fallback rules). |
| `synth.py` | Makes realistic fake breaths (30 points per second) with person-to-person differences, sensor noise and ~15% borderline cases. `make_breath(label)` → `(samples, features)`; `make_dataset(n_per_label, seed)` → table. |
| `train.py` | Trains a RandomForest on fake breaths + real ones (if any), saves `model.joblib` and `metrics.json`. |
| `predict.py` | `load()`, `predict(features)` → `{label, proba}`, `is_loaded()`. Falls back to the rules if no model is loaded. |

## Train
From the repo root:
```
.venv\Scripts\python.exe ml/train.py
```
Takes about 10 seconds. Options: `--n-per-label 600 --seed 42`.

## Real data
If `backend/data/breaths_labelled.csv` exists, it is added to training and each real row counts **3×**.
Columns (with a header row):
```
person,label,peak_ml,pct_target,time_to_peak_s,mean_rise_ml_s,max_rise_ml_s,hold_s,smoothness,duration_s
```
With 3 or more different people, `metrics.json` also has a "leave one person out" score:
the model is tested on each person after training without them (how well it works on a new patient).

## Feature notes
- `max_rise_ml_s` = fastest rise over any 0.3-second stretch of the inhale.
- `hold_s` = total time at 90% of the peak or higher (includes the very top of the rise and fall).
- `smoothness` = how jumpy the inhale is (lower = smoother).
- Timestamps in milliseconds are detected and converted automatically.

## Use
```python
from ml import predict, synth
predict.load()
samples, feats = synth.make_breath("good")
predict.predict(feats)   # {'label': 'good', 'proba': {...}}
```
