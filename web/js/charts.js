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

  /* 7-day chart: bars = best mL per day, dashed line = target, green line = sessions done (right axis, 0–14). */
  function weekChart(el, history, target) {
    const W = 640, H = 290, L = 56, R = 44, T = 30, B = 40;
    const iw = W - L - R, ih = H - T - B;
    const data = (history || []).slice(-7);
    const rawMax = Math.max(target || 0, ...data.map((d) => d.best_ml || 0), 500) * 1.08;
    const step = rawMax <= 3200 ? 500 : 1000;
    const ticks = Math.ceil(rawMax / step);
    const maxMl = ticks * step;
    const maxS = 14;
    const n = Math.max(data.length, 1);
    const bw = (iw / n) * 0.55;
    const x = (i) => L + (iw / n) * (i + 0.5);
    const y = (v) => T + ih - (v / maxMl) * ih;
    const y2 = (v) => T + ih - (v / maxS) * ih;
    let s = `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Best breath per day for the last 7 days, compared with the target, and sessions done per day">`;
    s += '<g class="grid">';
    for (let i = 0; i <= ticks; i++) {
      const v = step * i;
      s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L - 8}" y="${y(v) + 4}" text-anchor="end">${Math.round(v)}</text>`;
    }
    for (let i = 0; i <= 7; i++) s += `<text x="${W - R + 8}" y="${y2(i * 2) + 4}">${i * 2}</text>`;
    s += '</g>';
    s += `<text x="${L - 8}" y="${T - 14}" text-anchor="end" style="font-weight:600">mL</text><text x="${W - R + 8}" y="${T - 14}" style="font-weight:600">sess.</text>`;
    data.forEach((d, i) => {
      const v = d.best_ml || 0;
      const under = target && v < 0.8 * target;
      const dt = new Date(d.date + 'T00:00:00');
      const lbl = isNaN(dt) ? d.date : dt.toLocaleDateString([], { weekday: 'short', day: 'numeric' });
      s += `<rect class="bar${under ? ' under' : ''}" x="${x(i) - bw / 2}" y="${y(v)}" width="${bw}" height="${Math.max(0, T + ih - y(v))}" rx="4"><title>${esc(lbl)}: best ${Math.round(v)} mL, ${d.sessions_done || 0} sessions${d.avg_score != null ? ', avg score ' + d.avg_score : ''}</title></rect>`;
      s += `<text x="${x(i)}" y="${H - B + 18}" text-anchor="middle">${esc(lbl)}</text>`;
    });
    if (target) s += `<line class="target" x1="${L}" x2="${W - R}" y1="${y(target)}" y2="${y(target)}"><title>Target ${target} mL</title></line>`;
    if (data.length) {
      s += `<polyline class="line" points="${data.map((d, i) => `${x(i)},${y2(d.sessions_done || 0)}`).join(' ')}"/>`;
      data.forEach((d, i) => { s += `<circle class="pt" cx="${x(i)}" cy="${y2(d.sessions_done || 0)}" r="4.5"><title>${d.sessions_done || 0} sessions done</title></circle>`; });
    }
    s += '</svg>';
    el.innerHTML = s;
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
      g.setLineDash([6, 4]); g.strokeStyle = col('--red'); g.lineWidth = 2; g.beginPath(); g.moveTo(L, y(this.target)); g.lineTo(w - R, y(this.target)); g.stroke(); g.setLineDash([]);
      g.fillStyle = col('--red'); g.fillText('target ' + this.target, w - R - 90, y(this.target) - 5);
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

  SB.charts = { weekChart, LiveChart, niceMax };
})();
