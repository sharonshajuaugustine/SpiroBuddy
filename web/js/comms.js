/* SpiroBuddy – comms (CONTRACT D2): API wrapper, header alert bell, shared renderers, speech.
 * Needs js/api.js + js/ui.js. Optional: js/voice.js (natural voices) – falls back to speechSynthesis.
 *   SB.comms.api.*            calls /api/comms/*
 *   SB.comms.speak(text, lang, {audioUrl, interrupt})   -> Promise
 *   SB.comms.mountBell()      bell with open-alert counts in the header (all nurse pages)
 *   SB.comms.me()             the nurse using this browser ("assign to me"), stored per browser
 */
(function () {
  const SB = (window.SB = window.SB || {});
  const A = () => SB.api;
  const enc = encodeURIComponent;

  const api = {
    status: () => A().get('/api/comms/status'),
    alerts: (status = 'active', pid) => A().get(`/api/comms/alerts?status=${enc(status)}${pid != null ? '&patient_id=' + enc(pid) : ''}`),
    counts: (me) => A().get('/api/comms/alerts/counts' + (me ? '?me=' + enc(me) : '')),
    alertAct: (id, action, body) => A().post(`/api/comms/alerts/${id}/${action}`, body || {}),
    runs: (pid, active) => A().get(`/api/comms/escalations?limit=10${pid != null ? '&patient_id=' + enc(pid) : ''}${active ? '&active=1' : ''}`),
    startRun: (pid, body) => A().post(`/api/comms/escalations/start/${pid}`, body || {}),
    stopRun: (id, by) => A().post(`/api/comms/escalations/${id}/stop`, { by }),
    advanceRun: (id) => A().post(`/api/comms/escalations/${id}/advance`, {}),
    demoLadder: (pid, overrideQuiet) => A().post(`/api/comms/demo/ladder/${pid}`, { override_quiet: !!overrideQuiet }),
    demoRedFlag: (pid, text) => A().post(`/api/comms/demo/red-flag/${pid}`, text ? { text } : {}),
    timeline: (pid, limit = 60) => A().get(`/api/comms/timeline/${pid}?limit=${limit}`),
    events: (sinceId = 0, limit = 50) => A().get(`/api/comms/events?since_id=${sinceId}&limit=${limit}`),
    calls: (pid, active) => A().get(`/api/comms/calls?limit=10${pid != null ? '&patient_id=' + enc(pid) : ''}${active ? '&active=1' : ''}`),
    answer: (id) => A().post(`/api/comms/calls/${id}/answer`, {}),
    press: (id, digit) => A().post(`/api/comms/calls/${id}/press`, { digit: String(digit) }),
    hangup: (id, reason) => A().post(`/api/comms/calls/${id}/hangup`, { reason }),
    callPatient: (pid, nurseName) => A().post(`/api/comms/call-patient/${pid}`, { nurse_name: nurseName }),
    callScript: (pid) => A().post(`/api/comms/call-script/${pid}`, {}, { timeout: 45000 }),
    thread: (pid, role, gid) => A().get(`/api/comms/wa/thread/${pid}?role=${role}${gid ? '&guardian_id=' + gid : ''}`),
    reply: (body) => A().post('/api/comms/wa/reply', body),
    weeklyCard: (pid, to) => A().post(`/api/comms/weekly-card/${pid}`, { to: to || 'family' }),
    voiceNote: (pid, to) => A().post(`/api/comms/voice-note/${pid}`, { to: to || 'family' }, { timeout: 45000 }),
    care: (pid) => A().get(`/api/comms/care/${pid}`),
    putCare: (pid, body) => A().put(`/api/comms/care/${pid}`, body),
    addGuardian: (body) => A().post('/api/comms/guardians', body),
    editGuardian: (id, body) => A().put(`/api/comms/guardians/${id}`, body),
    delGuardian: async (id) => {
      const r = await fetch(`/api/comms/guardians/${id}`, { method: 'DELETE', cache: 'no-store' });
      const d = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(d.error || `HTTP ${r.status}`);
      return d;
    },
    patient: (pid) => A().get(`/api/comms/patient/${pid}`),
  };

  /* ---------- who am I (no login in the demo) ---------- */
  const NURSES = ['Sister Anjali', 'Dr. Mehta', 'Nurse Rakesh', 'Physio Kavya'];
  function me() { try { return localStorage.getItem('sb_me') || NURSES[0]; } catch (_) { return NURSES[0]; } }
  function setMe(n) { try { localStorage.setItem('sb_me', n); } catch (_) { /* ignore */ } }

  /* ---------- speech ---------- */
  const BCP = { en: 'en-IN', hi: 'hi-IN', ta: 'ta-IN' };
  function browserSpeak(text, lang) {
    return new Promise((resolve) => {
      if (!('speechSynthesis' in window)) return resolve(false);
      try {
        const u = new SpeechSynthesisUtterance(text);
        u.lang = BCP[lang] || lang || 'en-IN';
        const v = speechSynthesis.getVoices().find((x) => x.lang && x.lang.toLowerCase().startsWith((BCP[lang] || 'en').slice(0, 2)));
        if (v) u.voice = v;
        u.rate = 0.95;
        u.onend = () => resolve(true); u.onerror = () => resolve(false);
        speechSynthesis.speak(u);
        setTimeout(() => resolve(true), Math.min(30000, 1500 + text.length * 90));
      } catch (_) { resolve(false); }
    });
  }
  function speak(text, lang, opts) {
    opts = opts || {};
    if (!text) return Promise.resolve();
    const V = window.Voice;
    if (V && opts.audioUrl && V.playUrl) return V.playUrl(opts.audioUrl, { interrupt: !!opts.interrupt });
    if (V && V.say) return V.say(text, lang || 'en', { interrupt: !!opts.interrupt, fallbackText: opts.fallbackText });
    if (opts.audioUrl) return new Audio(opts.audioUrl).play().catch(() => browserSpeak(text, lang));
    if (opts.interrupt) { try { speechSynthesis.cancel(); } catch (_) { /* ignore */ } }
    return browserSpeak(text, lang);
  }
  function stopSpeaking() {
    try { if (window.Voice && Voice.stop) Voice.stop(); } catch (_) { /* ignore */ }
    try { speechSynthesis.cancel(); } catch (_) { /* ignore */ }
  }

  /* ---------- sounds (Web Audio, no files) ---------- */
  let ctx = null;
  function ac() { if (!ctx) { const C = window.AudioContext || window.webkitAudioContext; if (C) ctx = new C(); } if (ctx && ctx.state === 'suspended') ctx.resume(); return ctx; }
  function beep(freq, start, dur, vol) {
    const c = ac(); if (!c) return;
    const o = c.createOscillator(), g = c.createGain();
    o.type = 'sine'; o.frequency.value = freq;
    g.gain.setValueAtTime(0, c.currentTime + start);
    g.gain.linearRampToValueAtTime(vol || 0.15, c.currentTime + start + 0.02);
    g.gain.linearRampToValueAtTime(0, c.currentTime + start + dur);
    o.connect(g).connect(c.destination); o.start(c.currentTime + start); o.stop(c.currentTime + start + dur + 0.05);
  }
  function chime() { if (window.Voice && Voice.tone) { try { Voice.tone('good'); return; } catch (_) { /* fall through */ } } beep(880, 0, 0.18); beep(1320, 0.16, 0.3); }
  function ring() { /* Indian-style double ring */ [0, 0.45].forEach((t) => { beep(400, t, 0.35, 0.12); beep(450, t, 0.35, 0.08); }); }
  function unlockAudio() { ac(); }
  document.addEventListener('pointerdown', unlockAudio, { once: true });

  /* ---------- small renderers ---------- */
  const { esc } = SB.ui;
  const SEV_TEXT = { red: '● Needs a person now', amber: '⚠ Watch', info: 'ℹ Info' };
  function timeOnly(v) { const d = new Date(v); return isNaN(d) ? '' : d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }); }
  const STATUS_TAG = { ok: ['sent', 'done'], sent: ['sent', 'sent'], dry_run: ['dry', 'would send'], failed: ['missed', 'failed'], warn: ['missed', 'no answer'], held: ['dry', 'held'], skipped: ['', 'skipped'], info: ['', ''] };
  function eventRow(e, opts) {
    opts = opts || {};
    const [cls, label] = STATUS_TAG[e.status] || ['', e.status || ''];
    return `<li class="tl-item tl-${esc(e.status || 'info')}" data-id="${esc(e.id)}">
      <span class="tl-icon" aria-hidden="true">${esc(e.icon || '•')}</span>
      <div class="tl-body">
        <div class="tl-title">${opts.showPatient && e.patient_name ? `<b>${esc(e.patient_name)}</b> · ` : ''}${esc(e.title || '')}</div>
        ${e.detail ? `<div class="tl-detail">${esc(e.detail)}</div>` : ''}
        <div class="tl-meta"><span>${esc(SB.ui.dateTimeLabel(e.created_at))}</span>${e.channel ? `<span>· ${esc(e.channel)}</span>` : ''}${label ? `<span class="tag ${cls}">${esc(label)}</span>` : ''}</div>
      </div></li>`;
  }
  function stepper(run) {
    if (!run) return '';
    const ST = { done: '✓', next: '▶', held: '🌙', waiting: '…', skipped: '–' };
    return `<ol class="ladder" aria-label="Escalation ladder">${run.steps.map((s, i) => `<li class="ladder-step ${esc(s.state)}"><span class="n">${ST[s.state] || i + 1}</span><span class="l">${esc(s.label.split(' (')[0])}</span></li>`).join('')}</ol>`;
  }
  function runSummary(run) {
    if (!run) return '';
    const OUT = { patient_done: '✅ Patient says done', session_done: '✅ Session done', guardian_ack: '👍 Family will check', nurse_callback: '📞 Handed to nurse', 'nurse alerted': '🚨 Nurse alerted' };
    if (run.status === 'active') {
      const t = run.held_until ? `held for quiet hours until ${timeOnly(run.held_until)}` : run.seconds_to_next != null ? `next step in ${run.seconds_to_next < 90 ? run.seconds_to_next + ' s' : Math.round(run.seconds_to_next / 60) + ' min'}` : '';
      return `<span class="tag ${run.red_flag ? 'missed' : 'summary'}">${run.red_flag ? 'RED FLAG' : run.speed === 'fast' ? 'FAST-FORWARD' : 'ACTIVE'}</span> ${esc(t)}`;
    }
    return `<span class="tag ${run.status === 'resolved' ? 'sent' : run.status === 'completed' ? 'missed' : ''}">${esc(run.status)}</span> ${esc(OUT[run.outcome] || run.outcome || '')}`;
  }

  /* ---------- header bell ---------- */
  function mountBell() {
    const right = document.querySelector('.header-right');
    if (!right || document.getElementById('alert-bell')) return;
    const a = document.createElement('a');
    a.id = 'alert-bell'; a.className = 'bell'; a.href = SB.ui.link('index.html') + '#alerts';
    a.setAttribute('aria-label', 'Alerts'); a.title = 'Alerts inbox';
    a.innerHTML = '<span aria-hidden="true">🔔</span><span class="bell-n" id="bell-n">–</span>';
    right.insertBefore(a, right.firstChild);
    let lastRed = null;
    SB.ui.poll(async () => {
      if (SB.api.state.mock) { a.classList.add('hidden'); return; }
      const c = await api.counts(me());
      a.classList.remove('hidden');
      const n = c.open || 0;
      document.getElementById('bell-n').textContent = n;
      a.classList.toggle('has-red', (c.red || 0) > 0);
      a.title = `${n} open alert${n === 1 ? '' : 's'} (${c.red || 0} red, ${c.amber || 0} amber) · ${c.mine || 0} assigned to ${me()}`;
      if (lastRed != null && (c.red || 0) > lastRed) SB.ui.toast('🚨 New red alert – see the Alerts inbox', 'bad', 6000);
      lastRed = c.red || 0;
      SB.comms.lastCounts = c;
      document.dispatchEvent(new CustomEvent('sb:alert-counts', { detail: c }));
    }, 3000);
  }

  SB.comms = { api, me, setMe, NURSES, speak, stopSpeaking, chime, ring, beep, unlockAudio, eventRow, stepper, runSummary, timeOnly, SEV_TEXT, BCP, mountBell };
})();
