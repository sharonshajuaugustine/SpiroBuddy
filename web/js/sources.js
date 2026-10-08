/* SpiroBuddy – input sources (CONTRACT A + B). Each source calls onSample({t: ms, raw}).
 *  - SimulatorSource: realistic breaths of each label at ~30 Hz, raw is already mL (identity calibration)
 *  - SerialSource: Web Serial (Chrome/Edge), parses lines "D,<millis>,<distance_mm>"
 */
(function () {
  const SB = (window.SB = window.SB || {});

  function gauss(r) { let u = 0, v = 0; while (!u) u = r(); while (!v) v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  const smoothstep = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
  const rand = (a, b) => a + (b - a) * Math.random();

  /* Build a breath curve: function of seconds since start → mL, plus total length */
  function makeCurve(label, targetMl) {
    const T = targetMl || 2000;
    let peak, ttp, hold, fall;
    switch (label) {
      case 'too_fast': peak = T * rand(0.7, 0.95); ttp = rand(0.6, 0.95); hold = rand(1.8, 2.8); fall = rand(1.2, 2); break;
      case 'too_shallow': peak = T * rand(0.28, 0.42); ttp = rand(2.2, 3); hold = rand(2.2, 3.2); fall = rand(1.2, 1.8); break;
      case 'no_hold': peak = T * rand(0.75, 0.95); ttp = Math.max(2.2, (1.45 * peak) / 1200); hold = rand(0, 0.15); fall = rand(0.7, 1.0); break;
      default: // good
        peak = T * rand(0.85, 1.02); ttp = Math.max(rand(3, 3.8), (1.5 * peak) / 820); hold = rand(3, 4); fall = rand(1.8, 2.6);
    }
    const wobble = label === 'too_fast' ? 0.04 : 0.015;
    const fn = (s) => {
      let v;
      if (s < ttp) v = peak * smoothstep(s / ttp);
      else if (s < ttp + hold) v = peak * (1 - 0.04 * ((s - ttp) / Math.max(hold, 0.01)));
      else v = peak * 0.96 * (1 - smoothstep((s - ttp - hold) / fall));
      return v * (1 + wobble * Math.sin(s * 7.3));
    };
    return { fn, length: ttp + hold + fall + 0.4, label, peak };
  }

  class SimulatorSource {
    constructor(opts) {
      this.kind = 'simulator';
      this.hz = (opts && opts.hz) || 30;
      this.targetMl = (opts && opts.targetMl) || 2000;
      this.noise = (opts && opts.noise) != null ? opts.noise : 12;
      this.onSample = null; this.onStatus = null;
      this.queue = []; this.current = null; this.timer = null;
    }
    get connected() { return !!this.timer; }
    async start() {
      if (this.timer) return;
      this.timer = setInterval(() => this._tick(), 1000 / this.hz);
      this.onStatus && this.onStatus('Simulator running');
    }
    async stop() { clearInterval(this.timer); this.timer = null; this.onStatus && this.onStatus('Simulator stopped'); }
    /* queue a breath of the given label: good | too_fast | too_shallow | no_hold */
    breathe(label) { this.queue.push(label); return this.queue.length + (this.current ? 1 : 0); }
    get busy() { return !!this.current || this.queue.length > 0; }
    _tick() {
      const now = performance.now();
      if (!this.current && this.queue.length) this.current = { curve: makeCurve(this.queue.shift(), this.targetMl), t0: now + 300 };
      let ml = 0;
      if (this.current) {
        const s = (now - this.current.t0) / 1000;
        if (s >= 0) ml = this.current.curve.fn(s);
        if (s > this.current.curve.length) this.current = null;
      }
      ml = Math.max(0, ml + gauss(Math.random) * this.noise);
      this.onSample && this.onSample({ t: now, raw: ml });
    }
  }

  class SerialSource {
    constructor() {
      this.kind = 'serial'; this.onSample = null; this.onStatus = null; this.onError = null;
      this.port = null; this.reader = null; this.closed = null; this.keepReading = false; this.lastRaw = null;
    }
    static get supported() { return 'serial' in navigator; }
    get connected() { return !!this.port; }
    async start() {
      if (!SerialSource.supported) throw new Error('Web Serial is not available. Use Chrome or Edge on a laptop (http://localhost counts as secure).');
      this.port = await navigator.serial.requestPort();
      await this.port.open({ baudRate: 115200 });
      this.onStatus && this.onStatus('Serial port open (115200 baud)');
      this.keepReading = true;
      this._readLoop();
    }
    async _readLoop() {
      let buf = '';
      while (this.port && this.port.readable && this.keepReading) {
        const decoder = new TextDecoderStream();
        this.closed = this.port.readable.pipeTo(decoder.writable).catch(() => {});
        this.reader = decoder.readable.getReader();
        try {
          for (;;) {
            const { value, done } = await this.reader.read();
            if (done) break;
            buf += value;
            let i;
            while ((i = buf.indexOf('\n')) >= 0) { this._line(buf.slice(0, i).trim()); buf = buf.slice(i + 1); }
            if (buf.length > 4096) buf = '';
          }
        } catch (e) {
          this.onError && this.onError(e);
        } finally {
          try { this.reader.releaseLock(); } catch (_) { /* ignore */ }
        }
        if (!this.keepReading) break;
      }
    }
    _line(line) {
      if (!line) return;
      const parts = line.split(',');
      if (parts[0] === 'D' && parts.length >= 3) {
        const t = Number(parts[1]), raw = Number(parts[2]);
        if (isFinite(t) && isFinite(raw)) { this.lastRaw = raw; this.onSample && this.onSample({ t, raw }); }
      } else if (parts[0] === 'S') this.onStatus && this.onStatus('Device: ' + parts.slice(1).join(','));
      else if (parts[0] === 'E') this.onError && this.onError(new Error('Device error: ' + parts.slice(1).join(',')));
      // anything else is ignored (CONTRACT A)
    }
    async beep() {
      if (!this.port || !this.port.writable) return;
      const w = this.port.writable.getWriter();
      try { await w.write(new TextEncoder().encode('B\n')); } finally { w.releaseLock(); }
    }
    async stop() {
      this.keepReading = false;
      try { if (this.reader) await this.reader.cancel(); } catch (_) { /* ignore */ }
      try { if (this.closed) await this.closed; } catch (_) { /* ignore */ }
      try { if (this.port) await this.port.close(); } catch (_) { /* ignore */ }
      this.port = null; this.reader = null;
      this.onStatus && this.onStatus('Serial port closed');
    }
  }

  SB.sources = { SimulatorSource, SerialSource, makeCurve };
})();
