/* SpiroBuddy – breath processing, exactly CONTRACT B + C (docs/ARCHITECTURE.md).
 *  - Calibration: raw → mL by linear interpolation over sorted points [{raw, ml}], clamped 0..max
 *  - Smoothing: median of the last 5 values
 *  - State machine IDLE → INHALING → HOLDING → FALLING → IDLE, emits breaths with the features object
 *  - Score 0–10 and the rule fallback for labels
 */
(function () {
  const SB = (window.SB = window.SB || {});

  const LABELS = ['good', 'too_fast', 'too_shallow', 'no_hold'];
  const FEATURE_KEYS = ['peak_ml', 'pct_target', 'time_to_peak_s', 'mean_rise_ml_s', 'max_rise_ml_s', 'hold_s', 'smoothness', 'duration_s'];
  const CFG = {
    START_ML: 150,        // IDLE → INHALING
    HOLD_SLOPE: 150,      // mL/s, |slope| below this for HOLD_MIN_S → HOLDING
    HOLD_MIN_S: 0.3,
    FALL_RATIO: 0.9,      // vol < 0.9 × peak → FALLING
    END_ML: 100,          // FALLING → IDLE (emit)
    MIN_DURATION_S: 0.5,
    MIN_PEAK_ML: 250,
    STATE_TIMEOUT_S: 20,
    FAST_RATE: 1200,      // mL/s, live "too fast" warning
    SLOPE_WINDOW_S: 0.3,
  };

  const r2 = (x) => Math.round(x * 100) / 100;
  const r1 = (x) => Math.round(x * 10) / 10;

  /* ---------- CONTRACT B: calibration ---------- */
  class Calibration {
    constructor(points) { this.setPoints(points || []); }
    setPoints(points) {
      this.points = (points || []).filter((p) => isFinite(p.raw) && isFinite(p.ml)).map((p) => ({ raw: Number(p.raw), ml: Number(p.ml) })).sort((a, b) => a.raw - b.raw);
      this.maxMl = this.points.length ? Math.max(...this.points.map((p) => p.ml)) : Infinity;
    }
    get isIdentity() { return this.points.length < 2; }
    toMl(raw) {
      const P = this.points;
      if (P.length < 2) return Math.max(0, raw); // identity (simulator)
      let i = 0;
      if (raw <= P[0].raw) i = 0;
      else if (raw >= P[P.length - 1].raw) i = P.length - 2;
      else while (i < P.length - 2 && raw > P[i + 1].raw) i++;
      const a = P[i], b = P[i + 1];
      const ml = b.raw === a.raw ? a.ml : a.ml + ((raw - a.raw) * (b.ml - a.ml)) / (b.raw - a.raw);
      return Math.max(0, Math.min(this.maxMl, ml));
    }
    static load(key) { try { const v = JSON.parse(localStorage.getItem(key) || '[]'); return new Calibration(Array.isArray(v) ? v : []); } catch (_) { return new Calibration([]); } }
    save(key) { try { localStorage.setItem(key, JSON.stringify(this.points)); } catch (_) { /* ignore */ } }
  }

  class MedianFilter {
    constructor(n) { this.n = n || 5; this.buf = []; }
    push(v) { this.buf.push(v); if (this.buf.length > this.n) this.buf.shift(); const s = this.buf.slice().sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; }
    reset() { this.buf = []; }
  }

  /* rate of change over the last `win` seconds ending at index i (mL/s) */
  function rateAt(samples, i, win) {
    const t1 = samples[i].t;
    let j = i;
    while (j > 0 && t1 - samples[j - 1].t <= win * 1000) j--;
    if (j === i) return 0;
    const dt = (t1 - samples[j].t) / 1000;
    return dt > 0 ? (samples[i].ml - samples[j].ml) / dt : 0;
  }

  /* ---------- CONTRACT C: features (mirrors ml/features.py exactly) ----------
   * samples: [{t, ml}], t in ms (browser) – converted to seconds here.
   * onset = first sample >= 10% of peak; rising segment = onset..peak;
   * duration = onset → last sample >= 10% of peak; max_rise = fastest 0.3 s window
   * (j = first sample with t >= t_i + 0.3 s), never below mean_rise; if the rise
   * lasts <= 0.3 s → mean_rise; hold = sum of gaps to the next sample for samples >= 0.9 × peak. */
  const r3 = (x) => Math.round(x * 1000) / 1000;
  function computeFeatures(samples, targetMl) {
    const target = targetMl || 2000;
    if (!samples || samples.length < 2) return null;
    const S = samples.slice().sort((a, b) => a.t - b.t);
    const steps = []; for (let i = 1; i < S.length; i++) steps.push(S[i].t - S[i - 1].t);
    steps.sort((a, b) => a - b);
    const med = steps.length % 2 ? steps[(steps.length - 1) / 2] : (steps[steps.length / 2 - 1] + steps[steps.length / 2]) / 2;
    const k = med > 1.0 ? 1000 : 1; // ms → s (same heuristic as Python)
    const t = S.map((s) => s.t / k), v = S.map((s) => Number(s.ml));
    let pi = 0; for (let i = 1; i < v.length; i++) if (v[i] > v[pi]) pi = i;
    const peak = v[pi];
    if (peak <= 0) return null;
    let onset = 0; while (v[onset] < 0.1 * peak) onset++;
    let end = v.length - 1; while (v[end] < 0.1 * peak) end--;
    const ttp = t[pi] - t[onset];
    const rt = t.slice(onset, pi + 1), rv = v.slice(onset, pi + 1);
    const meanRise = ttp > 0 ? (peak - v[onset]) / ttp : 0;
    let maxRise = meanRise;
    if (ttp > CFG.SLOPE_WINDOW_S && rt.length >= 2) {
      let best = -Infinity, j = 0;
      for (let i = 0; i < rt.length; i++) {
        if (j < i) j = i;
        while (j < rt.length && rt[j] < rt[i] + CFG.SLOPE_WINDOW_S) j++;
        if (j >= rt.length) break;
        const dt = rt[j] - rt[i];
        const rate = dt > 0 ? (rv[j] - rv[i]) / dt : 0;
        if (rate > best) best = rate;
      }
      if (best > -Infinity) maxRise = Math.max(best, meanRise);
    }
    let hold = 0;
    for (let i = 0; i < v.length - 1; i++) if (v[i] >= 0.9 * peak) hold += t[i + 1] - t[i];
    let smooth = 0;
    if (rv.length >= 3) {
      const d = []; for (let i = 1; i < rv.length; i++) d.push(rv[i] - rv[i - 1]);
      const mean = d.reduce((a, b) => a + b, 0) / d.length;
      const sd = Math.sqrt(d.reduce((a, b) => a + (b - mean) * (b - mean), 0) / d.length);
      smooth = mean > 0 ? sd / mean : 0;
    }
    return {
      peak_ml: r1(peak),
      pct_target: r3(peak / target),
      time_to_peak_s: r3(ttp),
      mean_rise_ml_s: r1(meanRise),
      max_rise_ml_s: r1(maxRise),
      hold_s: r3(hold),
      smoothness: r3(smooth),
      duration_s: r3(t[end] - t[onset]),
    };
  }

  function score(f, targetMl, holdTargetS) {
    const depth = 4 * Math.min(f.peak_ml / (targetMl || 2000), 1);
    const speed = f.max_rise_ml_s <= 900 ? 3 : f.max_rise_ml_s <= 1400 ? 1 : 0;
    const hold = 3 * Math.min(f.hold_s / (holdTargetS || 3), 1);
    return r1(depth + speed + hold);
  }

  function ruleLabel(f) {
    if (f.max_rise_ml_s > 1400) return 'too_fast';
    if (f.pct_target < 0.5) return 'too_shallow';
    if (f.hold_s < 1.0) return 'no_hold';
    return 'good';
  }

  /* server model first, client rules if the server can't be reached */
  async function classify(features) {
    try {
      if (SB.api && !SB.api.state.mock) return await SB.api.classify(features);
    } catch (_) { /* fall through */ }
    const label = ruleLabel(features);
    const proba = {}; LABELS.forEach((l) => (proba[l] = l === label ? 1 : 0));
    return { label, proba, source: 'rules' };
  }

  /* ---------- CONTRACT C: state machine ---------- */
  class BreathDetector {
    constructor(opts) {
      this.opts = Object.assign({ targetMl: 2000, holdTargetS: 3, fastRate: CFG.FAST_RATE }, opts || {});
      this.reset();
    }
    reset() {
      this.state = 'IDLE'; this.stateSince = null; this.hist = []; this.breath = null; this.peak = 0; this.lowSince = null; this.fastWarned = false;
    }
    _set(s, t) { if (s === this.state) return; const prev = this.state; this.state = s; this.stateSince = t; this.lowSince = null; this.opts.onState && this.opts.onState(s, prev, t); }
    /* push one smoothed sample {t: ms, ml} */
    push(sample) {
      const t = sample.t, v = sample.ml;
      this.hist.push({ t, ml: v });
      while (this.hist.length > 2 && t - this.hist[0].t > 2000) this.hist.shift();
      const slope = rateAt(this.hist, this.hist.length - 1, CFG.SLOPE_WINDOW_S);
      if (this.stateSince == null) this.stateSince = t;
      if (this.breath) this.breath.samples.push({ t, ml: v });

      // timeout: a non-idle state lasting > 20 s → reset
      if (this.state !== 'IDLE' && (t - this.stateSince) / 1000 > CFG.STATE_TIMEOUT_S) {
        this.opts.onEvent && this.opts.onEvent({ type: 'reset', reason: 'timeout', t });
        this.breath = null; this.peak = 0; this._set('IDLE', t); return slope;
      }

      switch (this.state) {
        case 'IDLE':
          if (v > CFG.START_ML && slope > 0) {
            // start the breath where the rise began (last sample at or below 50 mL in the recent history)
            let k = this.hist.length - 1;
            while (k > 0 && this.hist[k - 1].ml > 50) k--;
            this.breath = { samples: this.hist.slice(Math.max(0, k - 1)).map((s) => ({ t: s.t, ml: s.ml })) };
            this.peak = v; this.fastWarned = false;
            this._set('INHALING', t);
          }
          break;
        case 'INHALING':
          this.peak = Math.max(this.peak, v);
          if (!this.fastWarned && slope > this.opts.fastRate) {
            this.fastWarned = true;
            this.opts.onEvent && this.opts.onEvent({ type: 'too_fast_live', rate: Math.round(slope), t });
          }
          if (v < CFG.FALL_RATIO * this.peak) { this._set('FALLING', t); break; }
          if (Math.abs(slope) < CFG.HOLD_SLOPE) {
            if (this.lowSince == null) this.lowSince = t;
            if ((t - this.lowSince) / 1000 >= CFG.HOLD_MIN_S) this._set('HOLDING', t);
          } else this.lowSince = null;
          break;
        case 'HOLDING':
          this.peak = Math.max(this.peak, v);
          if (v < CFG.FALL_RATIO * this.peak) this._set('FALLING', t);
          break;
        case 'FALLING':
          if (v < CFG.END_ML) {
            const b = this.breath; this.breath = null;
            const peak = this.peak; this.peak = 0;
            this._set('IDLE', t);
            const f = b && computeFeatures(b.samples, this.opts.targetMl);
            if (!f || f.duration_s < CFG.MIN_DURATION_S || peak < CFG.MIN_PEAK_ML) {
              this.opts.onEvent && this.opts.onEvent({ type: 'ignored', t, peak: Math.round(peak) });
              break;
            }
            const breath = { t: b.samples[0].t, samples: b.samples, features: f, score: score(f, this.opts.targetMl, this.opts.holdTargetS), rule_label: ruleLabel(f) };
            this.opts.onBreath && this.opts.onBreath(breath);
          }
          break;
      }
      return slope;
    }
  }

  SB.breath = { CFG, LABELS, FEATURE_KEYS, Calibration, MedianFilter, BreathDetector, computeFeatures, score, ruleLabel, classify, rateAt };
})();
