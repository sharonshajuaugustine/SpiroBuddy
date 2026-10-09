/* SpiroBuddy – small dependency-free charts (SVG + canvas), so they work offline. */
(function () {
  const SB = (window.SB = window.SB || {});
  const NS = 'http://www.w3.org/2000/svg';
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function niceMax(v) {
    if (v <= 0) return 1;
    const p = Math.pow(10, Math.floor(Math.log10(v)));
    const n = v / p;
    return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * p;
  }

  const fmt = (v) => Math.round(v).toLocaleString('en-IN');

  /* 7-day chart (honest by design): one measure only – best breath per day in mL, y-axis from 0,
   * labelled axis, dashed goal line with its value, each bar labelled with its number, sessions done
   * written under each day (no second axis). Bars under 80% of the goal are amber. Also writes a
   * screen-reader table with the same numbers. */
  function weekChart(el, history, target) {
    const W = 680, H = 300, L = 60, R = 64, T = 26, B = 52;
    const iw = W - L - R, ih = H - T - B;
    const data = (history || []).slice(-7);
    if (!data.length) { el.innerHTML = '<div class="empty"><b>No history yet</b>The chart fills in after the first day of sessions.</div>'; return; }
    const rawMax = Math.max(target || 0, ...data.map((d) => d.best_ml || 0), 500) * 1.1;
    const step = rawMax <= 1600 ? 250 : rawMax <= 3200 ? 500 : 1000;
    const ticks = Math.ceil(rawMax / step);
    const maxMl = ticks * step;
    const n = data.length;
    const bw = Math.min(56, (iw / n) * 0.56);
    const x = (i) => L + (iw / n) * (i + 0.5);
    const y = (v) => T + ih - (v / maxMl) * ih;
    const today = new Date().toDateString();
    let s = `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Bar chart: best breath per day for the last ${n} days in millilitres, with the goal of ${target ? fmt(target) : '—'} mL. The same numbers are in the table below.">`;
    s += '<g class="grid">';
    for (let i = 0; i <= ticks; i++) {
      const v = step * i;
      s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}"${i === 0 ? ' class="baseline"' : ''}/><text x="${L - 8}" y="${y(v) + 4}" text-anchor="end">${fmt(v)}</text>`;
    }
    s += '</g>';
    s += `<text class="axis-title" transform="translate(14 ${T + ih / 2}) rotate(-90)" text-anchor="middle">Best breath (mL)</text>`;
    data.forEach((d, i) => {
      const v = d.best_ml || 0;
      const under = target && v > 0 && v < 0.8 * target;
      const dt = new Date(d.date + 'T00:00:00');
      const isToday = !isNaN(dt) && dt.toDateString() === today;
      const lbl = isNaN(dt) ? d.date : isToday ? 'Today' : dt.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric' });
      const tip = `${lbl}: best ${v ? fmt(v) + ' mL' : 'no breath'}, ${d.sessions_done || 0} sessions${d.avg_score != null ? ', average score ' + d.avg_score + ' / 10' : ''}`;
      if (v > 0) {
        s += `<rect class="bar${under ? ' under' : ''}" x="${x(i) - bw / 2}" y="${y(v)}" width="${bw}" height="${Math.max(0, T + ih - y(v))}" rx="3"><title>${esc(tip)}</title></rect>`;
        s += `<text class="val" x="${x(i)}" y="${y(v) - 6}" text-anchor="middle">${fmt(v)}</text>`;
      } else {
        s += `<rect class="bar none" x="${x(i) - bw / 2}" y="${T + ih - 4}" width="${bw}" height="4" rx="2"><title>${esc(tip)}</title></rect>`;
        s += `<text class="sess" x="${x(i)}" y="${T + ih - 10}" text-anchor="middle">none</text>`;
      }
      s += `<text x="${x(i)}" y="${T + ih + 18}" text-anchor="middle"${isToday ? ' style="font-weight:700"' : ''}>${esc(lbl)}</text>`;
      s += `<text class="sess" x="${x(i)}" y="${T + ih + 34}" text-anchor="middle">${d.sessions_done || 0} sess.</text>`;
    });
    if (target) {
      s += `<line class="target" x1="${L}" x2="${W - R}" y1="${y(target)}" y2="${y(target)}"><title>Goal ${fmt(target)} mL</title></line>`;
      s += `<text class="target-lbl" x="${W - R + 6}" y="${y(target) - 3}">Goal</text><text class="target-lbl" x="${W - R + 6}" y="${y(target) + 11}">${fmt(target)}</text>`;
    }
    s += '</svg>';
    s += `<div class="sr-only"><table><caption>Best breath per day</caption><thead><tr><th>Day</th><th>Best breath (mL)</th><th>Sessions done</th><th>Average score</th></tr></thead><tbody>${data.map((d) => `<tr><td>${esc(d.date)}</td><td>${d.best_ml ? fmt(d.best_ml) : 'none'}</td><td>${d.sessions_done || 0}</td><td>${d.avg_score != null ? esc(d.avg_score) : '—'}</td></tr>`).join('')}</tbody></table></div>`;
    el.innerHTML = s;
  }

  /* Breath quality: one stacked bar + a list with counts and percentages (colour is never the only cue). */
  const Q = [['good', 'Good'], ['too_fast', 'Too fast'], ['too_shallow', 'Too shallow'], ['no_hold', 'No hold']];
  function qualityBar(el, counts) {
    const total = Q.reduce((a, [k]) => a + (Number(counts && counts[k]) || 0), 0);
    if (!total) { el.innerHTML = '<div class="empty"><b>No breaths recorded yet</b>Quality appears after the first session.</div>'; return; }
    const pct = (k) => ((Number(counts[k]) || 0) / total) * 100;
    el.innerHTML = `<div class="qbar" role="img" aria-label="${Q.map(([k, l]) => `${l} ${Math.round(pct(k))}%`).join(', ')}">${Q.filter(([k]) => counts[k]).map(([k, l]) => `<span class="q-${k}" style="width:${pct(k).toFixed(1)}%" title="${l}: ${counts[k]}"></span>`).join('')}</div>
      <ul class="qlist">${Q.map(([k, l]) => `<li><span class="sw q-${k}" aria-hidden="true"></span>${l}<b>${Number(counts[k]) || 0}</b><span class="pct">${Math.round(pct(k))}%</span></li>`).join('')}</ul>`;
  }

  /* Live volume graph on a canvas. push(t_ms, ml) then it redraws on animation frames. */
  class LiveChart {
    constructor(canvas, opts) {
      this.c = canvas; this.ctx = canvas.getContext('2d');
      this.windowMs = (opts && opts.windowMs) || 15000;
      this.maxMl = (opts && opts.maxMl) || 3000;
      this.target = (opts && opts.target) || 2000;
      this.points = []; this.marks = [];
      this.dirty = true;
      const loop = () => { if (this.dirty) this.draw(); requestAnimationFrame(loop); };
      requestAnimationFrame(loop);
      window.addEventListener('resize', () => (this.dirty = true));
    }
    push(t, ml, st) { this.points.push({ t, ml, st }); const cut = t - this.windowMs - 1000; while (this.points.length && this.points[0].t < cut) this.points.shift(); this.dirty = true; }
    mark(t, text, color) { this.marks.push({ t, text, color }); if (this.marks.length > 30) this.marks.shift(); this.dirty = true; }
    clear() { this.points = []; this.marks = []; this.dirty = true; }
    draw() {
      this.dirty = false;
      const c = this.c, dpr = window.devicePixelRatio || 1;
      const w = c.clientWidth, h = c.clientHeight;
      if (!w || !h) return;
      if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
      const g = this.ctx; g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
      const css = getComputedStyle(document.documentElement);
      const col = (n) => css.getPropertyValue(n).trim() || '#888';
      const L = 48, B = 22, T = 10, R = 10;
      const iw = w - L - R, ih = h - T - B;
      const now = this.points.length ? this.points[this.points.length - 1].t : 0;
      const x = (t) => L + iw - ((now - t) / this.windowMs) * iw;
      const y = (v) => T + ih - (Math.max(0, Math.min(v, this.maxMl)) / this.maxMl) * ih;
      g.font = '12px Segoe UI, system-ui, sans-serif'; g.fillStyle = col('--text-3'); g.strokeStyle = col('--border'); g.lineWidth = 1;
      for (let v = 0; v <= this.maxMl; v += 500) { g.beginPath(); g.moveTo(L, y(v)); g.lineTo(w - R, y(v)); g.stroke(); g.fillText(String(v), 6, y(v) + 4); }
      // state shading
      const stateCol = { INHALING: '--brand-soft', HOLDING: '--green-soft', FALLING: '--yellow-soft' };
      for (let i = 1; i < this.points.length; i++) {
        const p = this.points[i]; const k = stateCol[p.st];
        if (!k) continue; g.fillStyle = col(k); g.globalAlpha = .7;
        g.fillRect(x(this.points[i - 1].t), T, Math.max(1, x(p.t) - x(this.points[i - 1].t) + 0.5), ih); g.globalAlpha = 1;
      }
      // target line
      // goal line is neutral (red is reserved for "a person is needed now")
      g.setLineDash([6, 4]); g.strokeStyle = col('--text-2'); g.lineWidth = 1.5; g.beginPath(); g.moveTo(L, y(this.target)); g.lineTo(w - R, y(this.target)); g.stroke(); g.setLineDash([]);
      g.fillStyle = col('--text'); g.fillText('goal ' + this.target + ' mL', w - R - 100, y(this.target) - 5);
      // curve
      g.strokeStyle = col('--brand'); g.lineWidth = 2.5; g.beginPath();
      this.points.forEach((p, i) => (i ? g.lineTo(x(p.t), y(p.ml)) : g.moveTo(x(p.t), y(p.ml)))); g.stroke();
      // marks
      this.marks.forEach((m) => { const mx = x(m.t); if (mx < L) return; g.strokeStyle = m.color || col('--text-2'); g.beginPath(); g.moveTo(mx, T); g.lineTo(mx, T + ih); g.stroke(); g.fillStyle = m.color || col('--text-2'); g.fillText(m.text, Math.min(mx + 4, w - 120), T + 14); });
      // time axis
      g.fillStyle = col('--text-3');
      for (let s = 0; s <= this.windowMs / 1000; s += 5) g.fillText(s ? `-${s}s` : 'now', x(now - s * 1000) - 12, h - 6);
    }
  }

  SB.charts = { weekChart, qualityBar, LiveChart, niceMax };
})();
