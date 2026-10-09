/* SpiroBuddy – shared voice player (used by every page and the comms phone simulator).
 *
 *   Voice.say('breathe_in')                 speak a cue (see backend/app/voice_cues.py) in Voice.lang
 *   Voice.say('hold', 'ta')                 …in Tamil
 *   Voice.say('Namaste Ravi ji', 'hi')      free text
 *   Voice.say(x, lang, {interrupt:true})    cut off whatever is playing (urgent cues like "Slower…")
 *   Voice.say(text, 'hi', {fallbackText})   English text to read if this browser has no Hindi voice
 *   Voice.playUrl('/api/voice/audio/…mp3')  queue an audio file
 *   Voice.tone('good' | 'slower')           chime / low double-tone (DESIGN_SYSTEM.md §5)
 *   Voice.setLang('bn'), Voice.setMuted(true), Voice.toggleMute(), Voice.stop()
 *   const rec = Voice.record({lang, patientId}); …; rec.stop(); const r = await rec.done
 *        -> {text, lang, red_flag, reply, …} from POST /api/voice/stt (reply is spoken aloud)
 *   Voice.ask('typed question', {lang, patientId})   same, without a microphone
 *   Voice.onChange(fn)                      fn(state) when speaking / mute / language changes
 *
 * Every say() returns a Promise that resolves when that item has finished (never rejects).
 * Order of sources for a cue: pre-made clip web/audio/<lang>/<cue>.mp3 → server TTS (Sarvam)
 * → the browser's speechSynthesis with the best Indian voice → English cue if the browser has
 * no voice for that language. Items play one at a time, never overlapping.
 */
(function () {
  'use strict';
  const LS_LANG = 'sb_voice_lang', LS_MUTE = 'sb_voice_muted';
  const LANGS = {
    en: { bcp47: 'en-IN', name: 'English', native: 'English' },
    hi: { bcp47: 'hi-IN', name: 'Hindi', native: 'हिन्दी' },
    bn: { bcp47: 'bn-IN', name: 'Bengali', native: 'বাংলা' },
    ta: { bcp47: 'ta-IN', name: 'Tamil', native: 'தமிழ்' },
    te: { bcp47: 'te-IN', name: 'Telugu', native: 'తెలుగు' },
    kn: { bcp47: 'kn-IN', name: 'Kannada', native: 'ಕನ್ನಡ' },
    ml: { bcp47: 'ml-IN', name: 'Malayalam', native: 'മലയാളം' },
    mr: { bcp47: 'mr-IN', name: 'Marathi', native: 'मराठी' },
    gu: { bcp47: 'gu-IN', name: 'Gujarati', native: 'ગુજરાતી' },
    pa: { bcp47: 'pa-IN', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
    or: { bcp47: 'or-IN', name: 'Odia', native: 'ଓଡ଼ିଆ' }, // browsers use or-IN; Sarvam uses od-IN
  };
  const ALIAS = { od: 'or', odia: 'or', oriya: 'or' };

  function normLang(l) {
    if (!l) return null;
    let s = String(l).trim().toLowerCase().replace('_', '-');
    s = ALIAS[s] || s; s = s.split('-')[0]; s = ALIAS[s] || s;
    return LANGS[s] ? s : null;
  }
  function lsGet(k) { try { return localStorage.getItem(k); } catch (_) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (_) { /* private mode */ } }

  const state = {
    lang: normLang(lsGet(LS_LANG)) || 'en',
    muted: lsGet(LS_MUTE) === '1',
    speaking: false,
    current: null,          // {kind, label, via}
    lastVia: null,          // 'clip' | 'server' | 'browser' | 'browser-en' | 'none'
    server: null,           // /api/voice/status result or null (offline)
  };
  const listeners = new Set();
  function emit() { listeners.forEach((fn) => { try { fn(state); } catch (e) { console.error(e); } }); }

  /* ---------------- server status + cue texts ---------------- */
  let statusP = null, cuesP = null, cueTexts = null;
  function fetchJSON(url, ms) {
    const ctrl = new AbortController(); const t = setTimeout(() => ctrl.abort(), ms || 4000);
    return fetch(url, { signal: ctrl.signal, cache: 'no-store' }).then((r) => (r.ok ? r.json() : null)).catch(() => null).finally(() => clearTimeout(t));
  }
  function status(refresh) {
    if (!statusP || refresh) statusP = fetchJSON('/api/voice/status').then((s) => { state.server = s; emit(); return s; });
    return statusP;
  }
  function loadCues() {
    if (!cuesP) cuesP = fetchJSON('/api/voice/cues').then((d) => d || fetchJSON('/audio/cues.json')).then((d) => { cueTexts = (d && d.cues) || {}; return cueTexts; });
    return cuesP;
  }
  function cueText(cue, lang) { const row = cueTexts && cueTexts[cue]; return row ? (row[lang] || row.en || null) : null; }

  /* ---------------- browser voices ---------------- */
  let voicesP = null;
  function voices() {
    if (!('speechSynthesis' in window)) return Promise.resolve([]);
    if (!voicesP) voicesP = new Promise((res) => {
      const now = speechSynthesis.getVoices();
      if (now.length) return res(now);
      const done = () => res(speechSynthesis.getVoices());
      speechSynthesis.addEventListener('voiceschanged', done, { once: true });
      setTimeout(done, 1500);
    });
    return voicesP;
  }
  function scoreVoice(v, bcp) {
    const vl = (v.lang || '').toLowerCase().replace('_', '-'), want = bcp.toLowerCase(), base = want.split('-')[0];
    let s = 0;
    if (vl === want) s += 100; else if (vl.split('-')[0] === base) s += 60; else return -1;
    if (base === 'en' && vl === 'en-in') s += 20;
    if (/natural|neural|online/i.test(v.name)) s += 15;   // Edge "Online (Natural)" voices sound best
    if (/google/i.test(v.name)) s += 10;
    if (/female|swara|neerja|heera|kalpana|pallavi|shruti|sapna|vani|gagan|aarohi|kavya/i.test(v.name)) s += 3;
    if (v.localService) s += 1;
    return s;
  }
  async function bestVoice(lang) {
    const list = await voices(); const bcp = LANGS[lang].bcp47;
    let best = null, bs = -1;
    list.forEach((v) => { const s = scoreVoice(v, bcp); if (s > bs) { bs = s; best = v; } });
    return bs >= 0 ? best : null;
  }
  async function hasBrowserVoice(lang) { return !!(await bestVoice(normLang(lang) || 'en')); }

  function speakBrowser(text, lang, opts) {
    return new Promise(async (resolve) => {
      if (!('speechSynthesis' in window)) return resolve(false);
      const v = await bestVoice(lang);
      const u = new SpeechSynthesisUtterance(text);
      u.lang = (v && v.lang) || LANGS[lang].bcp47;
      if (v) u.voice = v;
      u.rate = (opts && opts.rate) || 0.9;               // a little slower for elderly listeners
      u.pitch = 1;
      let finished = false;
      const end = (ok) => { if (!finished) { finished = true; clearTimeout(guard); resolve(ok); } };
      u.onend = () => end(true); u.onerror = () => end(false);
      // Chrome sometimes never fires onend: guard by length
      const guard = setTimeout(() => end(true), 2500 + text.length * 140);
      cancelCurrent = () => { try { speechSynthesis.cancel(); } catch (_) { /* ignore */ } end(false); };
      speechSynthesis.speak(u);
    });
  }

  /* ---------------- audio element playback ---------------- */
  const audio = new Audio(); audio.preload = 'auto';
  let cancelCurrent = null;
  function playAudio(url) {
    return new Promise((resolve) => {
      let finished = false;
      const end = (ok) => { if (finished) return; finished = true; audio.onended = audio.onerror = null; resolve(ok); };
      audio.onended = () => end(true);
      audio.onerror = () => end(false);
      cancelCurrent = () => { try { audio.pause(); } catch (_) { /* ignore */ } end(false); };
      audio.src = url;
      const p = audio.play();
      if (p && p.catch) p.catch((e) => { if (e && e.name === 'NotAllowedError') console.warn('[Voice] autoplay blocked – tap the page once'); end(false); });
    });
  }

  const blobCache = new Map(); // `${lang}|${text}` -> objectURL
  async function serverTTS(text, lang) {
    const key = lang + '|' + text;
    if (blobCache.has(key)) return blobCache.get(key);
    try {
      const ctrl = new AbortController(); const t = setTimeout(() => ctrl.abort(), 25000);
      const r = await fetch('/api/voice/tts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text, language: lang }), signal: ctrl.signal });
      clearTimeout(t);
      if (!r.ok) return null;
      const url = URL.createObjectURL(await r.blob());
      blobCache.set(key, url);
      return url;
    } catch (_) { return null; }
  }

  /* ---------------- the queue ---------------- */
  const queue = [];
  let running = false;
  function enqueue(task, interrupt) {
    return new Promise((resolve) => {
      if (interrupt) stop();
      queue.push({ task, resolve });
      run();
    });
  }
  async function run() {
    if (running) return;
    running = true;
    while (queue.length) {
      const { task, resolve } = queue.shift();
      if (state.muted) { resolve({ ok: false, via: 'muted' }); continue; }
      state.speaking = true; state.current = { label: task.label }; emit();
      let res = { ok: false, via: 'none' };
      try { res = await task.run(); } catch (e) { console.warn('[Voice]', e); }
      cancelCurrent = null;
      state.lastVia = res.via; state.speaking = false; state.current = null; emit();
      resolve(res);
    }
    running = false;
  }
  function stop() {
    queue.splice(0).forEach((q) => q.resolve({ ok: false, via: 'stopped' }));
    if (cancelCurrent) cancelCurrent();
    try { if ('speechSynthesis' in window) speechSynthesis.cancel(); } catch (_) { /* ignore */ }
  }

  async function playCue(cue, lang, opts) {
    await Promise.all([status(), loadCues()]);
    const s = state.server;
    // 1. pre-made clip (static file, fastest; only tried when the server reports clips)
    if (s && s.clips && s.clips[lang] > 0 && await playAudio(`/audio/${lang}/${cue}.mp3`)) return { ok: true, via: 'clip' };
    // 2. server TTS (makes and caches the clip with Sarvam)
    if (s && s.enabled && await playAudio(`/api/voice/clip/${lang}/${cue}`)) return { ok: true, via: 'server' };
    // 3. browser voice in the language, 4. English cue if the browser has no such voice
    const text = cueText(cue, lang);
    if (!text) return { ok: false, via: 'none' };
    if (lang === 'en' || await hasBrowserVoice(lang)) return { ok: await speakBrowser(text, lang, opts), via: 'browser' };
    const en = cueText(cue, 'en');
    return { ok: await speakBrowser(en, 'en', opts), via: 'browser-en' };
  }
  async function playText(text, lang, opts) {
    await status();
    const s = state.server;
    if (s && s.enabled) { const url = await serverTTS(text, lang); if (url && await playAudio(url)) return { ok: true, via: 'server' }; }
    if (lang === 'en' || await hasBrowserVoice(lang)) return { ok: await speakBrowser(text, lang, opts), via: 'browser' };
    // No voice for this language in this browser: use the English version if the caller gave one
    if (opts && opts.fallbackText) return { ok: await speakBrowser(opts.fallbackText, 'en', opts), via: 'browser-en' };
    return { ok: await speakBrowser(text, lang, opts), via: 'browser' };   // engine may still manage
  }

  function isCue(x) { return /^[a-z0-9_]{2,40}$/.test(x) && (!cueTexts || cueTexts[x]); }

  function say(cueOrText, lang, opts) {
    opts = opts || {};
    const l = normLang(lang) || state.lang;
    const x = String(cueOrText == null ? '' : cueOrText).trim();
    if (!x) return Promise.resolve({ ok: false, via: 'none' });
    return enqueue({ label: x.slice(0, 60), run: async () => { await loadCues(); return isCue(x) && cueTexts[x] ? playCue(x, l, opts) : playText(x, l, opts); } }, opts.interrupt);
  }
  function playUrl(url, opts) { return enqueue({ label: url, run: async () => ({ ok: await playAudio(url), via: 'url' }) }, opts && opts.interrupt); }

  /* ---------------- sounds (WebAudio, no files) ---------------- */
  let ctx = null;
  function actx() {
    if (!ctx) { const C = window.AudioContext || window.webkitAudioContext; if (!C) return null; ctx = new C(); }
    if (ctx.state === 'suspended') ctx.resume().catch(() => {});
    return ctx;
  }
  function note(c, freq, start, dur, type, peak) {
    const o = c.createOscillator(), g = c.createGain();
    o.type = type; o.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, start);
    g.gain.exponentialRampToValueAtTime(peak, start + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, start + dur);
    o.connect(g).connect(c.destination); o.start(start); o.stop(start + dur + 0.05);
  }
  /** 'good' = one short friendly chime; 'slower' = one low, soft double-tone. No harsh alarms. */
  function tone(kind) {
    if (state.muted) return;
    const c = actx(); if (!c) return;
    const t = c.currentTime + 0.01;
    if (kind === 'slower') { note(c, 330, t, 0.16, 'triangle', 0.18); note(c, 294, t + 0.24, 0.2, 'triangle', 0.18); }
    else { note(c, 1047, t, 0.7, 'sine', 0.22); note(c, 1568, t, 0.45, 'sine', 0.07); note(c, 1319, t + 0.09, 0.6, 'sine', 0.12); }
  }
  // browsers only allow sound after a tap/key: unlock on the first gesture
  ['pointerdown', 'keydown', 'touchstart'].forEach((ev) => window.addEventListener(ev, function unlock() { actx(); window.removeEventListener(ev, unlock, true); }, true));

  /* ---------------- push-to-talk ---------------- */
  async function postQuestion(form) {
    try {
      const r = await fetch('/api/voice/stt', { method: 'POST', body: form });
      const d = await r.json().catch(() => ({}));
      return Object.assign({ httpStatus: r.status }, d);
    } catch (e) { return { ok: false, error: 'Server offline – could not send the question', fallback: 'browser' }; }
  }
  async function answer(res, lang, speak) {
    if (speak !== false && res && res.reply) {
      if (res.reply_audio_url) await playUrl(res.reply_audio_url);
      else await say(res.reply_cue || res.reply, res.lang || lang);   // a cue gets clip + English fallback
    }
    return res;
  }
  /** Typed (or browser-recognised) question → same red-flag check and reply as a voice note. */
  async function ask(text, opts) {
    opts = opts || {};
    const lang = normLang(opts.lang) || state.lang;
    const f = new FormData(); f.append('text', text); f.append('language', lang);
    if (opts.patientId) f.append('patient_id', String(opts.patientId));
    return answer(await postQuestion(f), lang, opts.speak);
  }
  /**
   * Start recording. Returns {stop(), cancel(), done: Promise<result>, mode}.
   * mode 'sarvam'  – records audio (max opts.maxMs, default 25 s) and sends it to /api/voice/stt.
   * mode 'browser' – no Sarvam key: the browser's own speech recognition (Chrome/Edge) turns
   *                  speech into text, which is then checked by the server the same way.
   */
  function record(opts) {
    opts = opts || {};
    const lang = normLang(opts.lang) || state.lang;
    const maxMs = opts.maxMs || 25000;
    let stopFn = () => {}, cancelled = false, mode = 'pending';
    const ctl = { stop: () => stopFn(), cancel: () => { cancelled = true; stopFn(); }, get mode() { return mode; } };
    ctl.done = (async () => {
      const s = await status();
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!(s && s.enabled) && SR) {
        mode = 'browser';
        const text = await new Promise((resolve) => {
          const rec = new SR(); rec.lang = LANGS[lang].bcp47; rec.interimResults = false; rec.maxAlternatives = 1;
          let got = '';
          rec.onresult = (e) => { got = Array.from(e.results).map((r) => r[0].transcript).join(' '); };
          rec.onerror = (e) => { if (e.error !== 'no-speech' && e.error !== 'aborted') console.warn('[Voice] recognition', e.error); };
          rec.onend = () => resolve(got);
          stopFn = () => { try { rec.stop(); } catch (_) { /* ignore */ } };
          setTimeout(stopFn, maxMs);
          try { rec.start(); } catch (e) { resolve(''); }
        });
        if (cancelled) return { ok: false, cancelled: true };
        if (!text) return { ok: false, error: 'Nothing was heard – please try again', mode };
        return Object.assign(await ask(text, Object.assign({}, opts, { lang })), { mode });
      }
      if (!navigator.mediaDevices || !window.MediaRecorder) return { ok: false, error: 'This browser cannot record – please type the question', mode: 'none' };
      if (!(s && s.enabled)) return { ok: false, error: 'Speech-to-text needs the Sarvam key or Chrome/Edge – please type the question', mode: 'none' };
      mode = 'sarvam';
      let stream;
      try { stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true } }); }
      catch (e) { return { ok: false, error: 'Microphone not allowed – please allow it, or type the question', mode }; }
      const mime = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/mp4'].find((m) => MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) || '';
      const mr = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
      const chunks = [];
      mr.ondataavailable = (e) => { if (e.data && e.data.size) chunks.push(e.data); };
      const stopped = new Promise((r) => (mr.onstop = r));
      stopFn = () => { if (mr.state !== 'inactive') mr.stop(); };
      const timer = setTimeout(stopFn, maxMs);
      mr.start();
      await stopped; clearTimeout(timer);
      stream.getTracks().forEach((t) => t.stop());
      if (cancelled) return { ok: false, cancelled: true, mode };
      const type = mr.mimeType || mime || 'audio/webm';
      const ext = /mp4/.test(type) ? 'm4a' : /ogg/.test(type) ? 'ogg' : 'webm';
      const f = new FormData();
      f.append('file', new Blob(chunks, { type }), 'question.' + ext);
      f.append('language', lang);
      if (opts.patientId) f.append('patient_id', String(opts.patientId));
      return Object.assign(await answer(await postQuestion(f), lang, opts.speak), { mode });
    })();
    return ctl;
  }

  /* ---------------- settings ---------------- */
  function setLang(l) { const n = normLang(l); if (n && n !== state.lang) { state.lang = n; lsSet(LS_LANG, n); emit(); } return state.lang; }
  function setMuted(m) { state.muted = !!m; lsSet(LS_MUTE, state.muted ? '1' : '0'); if (state.muted) stop(); emit(); return state.muted; }

  /** Fill a <select> with all 11 languages (native name first, for patients). */
  function fillLangSelect(sel, value) {
    sel.innerHTML = Object.entries(LANGS).map(([k, v]) => `<option value="${k}">${v.native}${v.native !== v.name ? ' – ' + v.name : ''}</option>`).join('');
    sel.value = normLang(value) || state.lang;
    return sel;
  }
  /** Make a button a mute switch (🔊 Voice on / 🔇 Voice off). */
  function bindMute(btn) {
    const paint = () => { btn.textContent = state.muted ? '🔇 Voice off' : '🔊 Voice on'; btn.setAttribute('aria-pressed', String(!state.muted)); btn.title = state.muted ? 'Turn the voice coach on' : 'Mute the voice coach'; };
    btn.addEventListener('click', () => setMuted(!state.muted));
    listeners.add(paint); paint();
    return btn;
  }

  window.Voice = {
    LANGS, state, normLang, say, playUrl, stop, tone, record, ask, status, loadCues, cueText,
    setLang, setMuted, toggleMute: () => setMuted(!state.muted), fillLangSelect, bindMute, hasBrowserVoice,
    onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
    get lang() { return state.lang; }, get muted() { return state.muted; },
  };
  loadCues(); status();
})();
