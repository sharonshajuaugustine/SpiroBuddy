/* SpiroBuddy – voice widgets for the website (needs js/voice.js; uses SB.ui if present).
 * Each widget mounts itself if its placeholder exists on the page:
 *   <section id="voice-patient-card" data-patient-id="1">  patient.html – language, voice-note summary, ask a question
 *   <section id="voice-check-card">                        demo.html    – play every cue in any language
 *   <div id="voice-coach-bar">                             collect.html – language + mute; SB.voiceCoach speaks cues
 */
(function () {
  'use strict';
  const V = window.Voice;
  if (!V) { console.warn('[voice-ui] js/voice.js missing'); return; }
  const SB = (window.SB = window.SB || {});
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const toast = (m, k) => (SB.ui && SB.ui.toast ? SB.ui.toast(m, k) : console.log(m));
  const VIA = { clip: 'pre-made clip', server: 'Sarvam voice', browser: 'browser voice', 'browser-en': 'browser voice (English – no voice for this language on this computer)', muted: 'muted', none: 'no voice available', url: 'audio file' };

  function providerChip(s) {
    if (!s) return '<span class="source-tag" title="Voice server not reachable">Browser voice (offline)</span>';
    return s.enabled ? `<span class="source-tag llm" title="${esc(s.tts_model)} · ${esc(s.stt_model)}">Sarvam AI voice</span>`
      : '<span class="source-tag" title="No SARVAM_API_KEY – pre-made clips or the browser\'s own voice are used">Browser voice (no Sarvam key)</span>';
  }

  /* ======================================================= patient page */
  async function mountPatient(card) {
    const pid = card.dataset.patientId || new URLSearchParams(location.search).get('id') || '1';
    card.innerHTML = `
      <div class="card-head"><h2>Voice &amp; language</h2><div class="spacer"></div><span class="vprov"></span><button class="btn sm vmute" type="button"></button></div>
      <div class="row" style="margin-bottom:.6rem">
        <label for="v-lang">Voice language</label><select id="v-lang"></select>
        <span class="muted small" id="v-lang-note"></span>
      </div>
      <div class="row" style="margin-bottom:.6rem">
        <button class="btn primary" id="v-sum" type="button">▶ Play summary as voice note</button>
        <button class="btn" id="v-stop" type="button">■ Stop</button>
      </div>
      <div class="summary-box" id="v-sum-text" aria-live="polite"><span class="muted">The evening summary, read aloud in the patient's language – the same audio is sent as a WhatsApp voice note.</span></div>
      <div class="card-head" style="margin-top:1rem"><h3 style="margin:0">Patient question (push to talk)</h3></div>
      <div class="row">
        <button class="btn" id="v-rec" type="button" aria-pressed="false">🎤 Hold to ask</button>
        <input id="v-q" placeholder="…or type a question" maxlength="300" style="flex:1;min-width:160px">
        <button class="btn" id="v-ask" type="button">Ask</button>
      </div>
      <div id="v-q-out" aria-live="polite" style="margin-top:.5rem"></div>
      <p class="muted small" style="margin-bottom:0">Questions are checked for danger words in every language. Those get the fixed message "contact your nurse / call 112" and go to the nurse. SpiroBuddy never diagnoses.</p>`;
    const $ = (s) => card.querySelector(s);
    V.bindMute($('.vmute'));
    const sel = V.fillLangSelect($('#v-lang'), V.lang);
    V.status().then((s) => { $('.vprov').innerHTML = providerChip(s); });

    // load the saved voice language of this patient
    try {
      const r = await fetch(`/api/voice/prefs/${encodeURIComponent(pid)}`);
      if (r.ok) { const p = await r.json(); sel.value = p.language; V.setLang(p.language); $('#v-lang-note').textContent = p.saved ? 'saved for this patient' : 'from the patient profile'; }
    } catch (_) { /* offline: keep browser setting */ }
    sel.addEventListener('change', async () => {
      V.setLang(sel.value);
      try {
        const r = await fetch(`/api/voice/prefs/${encodeURIComponent(pid)}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ language: sel.value }) });
        $('#v-lang-note').textContent = r.ok ? 'saved for this patient' : 'could not save';
      } catch (_) { $('#v-lang-note').textContent = 'offline – used on this computer only'; }
      V.say('ready', sel.value, { interrupt: true });
      langHint();
    });
    async function langHint() {
      const s = await V.status();
      if (s && s.enabled) return;
      if (!(await V.hasBrowserVoice(sel.value))) $('#v-lang-note').textContent += ` · this browser has no ${V.LANGS[sel.value].name} voice: cues fall back to English until the Sarvam key is added`;
    }
    langHint();

    $('#v-stop').addEventListener('click', () => V.stop());
    $('#v-sum').addEventListener('click', async (e) => {
      const btn = e.currentTarget; btn.disabled = true; btn.classList.add('busy');
      $('#v-sum-text').innerHTML = '<span class="muted">Writing and recording the summary…</span>';
      try {
        const r = await fetch(`/api/voice/summary-audio/${encodeURIComponent(pid)}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ language: sel.value }) });
        const d = await r.json();
        if (!r.ok) throw new Error(d.error || 'HTTP ' + r.status);
        const langName = (V.LANGS[d.text_lang] || {}).name || d.text_lang;
        $('#v-sum-text').innerHTML = `<div>${esc(d.text)}</div><div class="muted small" style="margin-top:.4rem">${d.audio_url ? `🔊 Voice note ready (Sarvam) · <a href="${esc(d.audio_url)}" target="_blank" rel="noopener">open audio</a>` : '🔊 Read by the browser voice (' + esc(d.note || 'no audio file') + ')'} · text: ${esc(d.source === 'llm' ? 'AI (Claude)' : 'template')}${d.translated ? ' + Sarvam translation' : ''} · language: ${esc(langName)}</div>`;
        const res = d.audio_url ? await V.playUrl(d.audio_url, { interrupt: true }) : await V.say(d.text, d.text_lang || sel.value, { interrupt: true, fallbackText: d.text_en });
        if (res.via === 'browser-en') toast(`This computer has no ${langName} voice, so the English version was read. Add the Sarvam key for every language.`);
        if (!res.ok && res.via !== 'stopped') toast(res.via === 'muted' ? 'Voice is muted' : 'Could not play the voice note', 'bad');
      } catch (err) {
        $('#v-sum-text').innerHTML = `<span class="muted">Could not make the voice note: ${esc(err.message)}</span>`;
      } finally { btn.disabled = false; btn.classList.remove('busy'); }
    });

    function showAnswer(r) {
      if (!r || r.cancelled) return;
      if (!r.ok && !r.text) { $('#v-q-out').innerHTML = `<div class="drybox"><div class="t">${esc(r.error || 'Could not understand the question')}</div></div>`; return; }
      $('#v-q-out').innerHTML = `<div class="drybox${r.red_flag ? '' : ' sent'}" style="${r.red_flag ? 'border-color:var(--red)' : ''}">
        <div class="t">${r.red_flag ? '● Red flag – nurse alerted' : '✓ Question received'}${r.mode === 'browser' ? ' <span class="muted small">(heard by the browser)</span>' : ''}</div>
        <div><b>Heard:</b> ${esc(r.text)}${r.english && r.english !== r.text ? ` <span class="muted">(${esc(r.english)})</span>` : ''}</div>
        <div><b>Reply:</b> ${esc(r.reply || '')}</div></div>`;
    }
    let rec = null;
    const recBtn = $('#v-rec');
    const startRec = () => {
      if (rec) return;
      recBtn.classList.add('busy'); recBtn.setAttribute('aria-pressed', 'true'); recBtn.textContent = '🎤 Listening… release to send';
      rec = V.record({ lang: sel.value, patientId: pid });
      rec.done.then(showAnswer).finally(() => { rec = null; recBtn.classList.remove('busy'); recBtn.setAttribute('aria-pressed', 'false'); recBtn.textContent = '🎤 Hold to ask'; });
    };
    const stopRec = () => { if (rec) rec.stop(); };
    recBtn.addEventListener('pointerdown', (e) => { e.preventDefault(); startRec(); });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach((ev) => recBtn.addEventListener(ev, stopRec));
    recBtn.addEventListener('keydown', (e) => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); startRec(); } });
    recBtn.addEventListener('keyup', (e) => { if (e.key === ' ' || e.key === 'Enter') stopRec(); });
    const ask = async () => {
      const q = $('#v-q').value.trim(); if (!q) return;
      $('#v-ask').disabled = true;
      try { showAnswer(await V.ask(q, { lang: sel.value, patientId: pid })); $('#v-q').value = ''; }
      finally { $('#v-ask').disabled = false; }
    };
    $('#v-ask').addEventListener('click', ask);
    $('#v-q').addEventListener('keydown', (e) => { if (e.key === 'Enter') ask(); });
  }

  /* ======================================================= demo panel: voice check */
  async function mountCheck(card) {
    card.innerHTML = `
      <div class="card-head"><h2>Voice check</h2><span class="muted small">every coaching cue, in any language</span><div class="spacer"></div><span class="vprov"></span><button class="btn sm vmute" type="button"></button></div>
      <div class="row" style="margin-bottom:.6rem">
        <label for="vc-lang">Language</label><select id="vc-lang"></select>
        <button class="btn primary" id="vc-all" type="button">▶ Play the coaching sequence</button>
        <button class="btn" id="vc-stop" type="button">■ Stop</button>
        <button class="btn sm" id="vc-good" type="button">♪ Chime</button>
        <button class="btn sm" id="vc-slow" type="button">♪ Slower tone</button>
      </div>
      <div class="muted small" id="vc-now" aria-live="polite" style="margin-bottom:.4rem">Pick a language and press a cue.</div>
      <div class="vc-grid" id="vc-list" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.4rem"></div>`;
    const $ = (s) => card.querySelector(s);
    V.bindMute($('.vmute'));
    const sel = V.fillLangSelect($('#vc-lang'), V.lang);
    V.status().then((s) => {
      $('.vprov').innerHTML = providerChip(s);
      if (s) { const n = Object.values(s.clips || {}).reduce((a, b) => a + b, 0); $('#vc-now').textContent = `${n} pre-made clips on the server · ${s.enabled ? 'missing clips are made by Sarvam on first play' : 'no Sarvam key: the browser voice speaks'}`; }
    });
    const cues = await V.loadCues();
    const order = Object.keys(cues);
    function render() {
      const lang = sel.value;
      $('#vc-list').innerHTML = order.map((k) => `<button class="btn sm" type="button" data-cue="${esc(k)}" style="justify-content:flex-start;text-align:left;white-space:normal;height:auto;min-height:44px">
        <span><b class="mono small">${esc(k)}</b><br>${esc(V.cueText(k, lang) || '')}</span></button>`).join('');
    }
    render();
    sel.addEventListener('change', () => { V.setLang(sel.value); render(); });
    const show = (cue, r) => { $('#vc-now').textContent = `${cue}: ${r.ok ? 'played via ' + (VIA[r.via] || r.via) : VIA[r.via] || 'not played'}`; };
    $('#vc-list').addEventListener('click', async (e) => {
      const b = e.target.closest('[data-cue]'); if (!b) return;
      const cue = b.dataset.cue; $('#vc-now').textContent = `${cue}: playing…`;
      show(cue, await V.say(cue, sel.value, { interrupt: true }));
    });
    $('#vc-stop').addEventListener('click', () => V.stop());
    $('#vc-good').addEventListener('click', () => V.tone('good'));
    $('#vc-slow').addEventListener('click', () => V.tone('slower'));
    $('#vc-all').addEventListener('click', async () => {
      V.stop();
      const lang = sel.value;
      const seq = ['reminder', 'ready', 'breathe_in', 'slower', 'hold', 'count_3', 'count_2', 'count_1', 'breathe_out', 'great_breath', 'breath_1', 'encourage_1', 'session_complete'];
      for (const cue of seq) {
        if (cue === 'slower') V.tone('slower');
        if (cue === 'great_breath') V.tone('good');
        $('#vc-now').textContent = `${cue}: playing…`;
        const r = await V.say(cue, lang);
        if (r.via === 'stopped' || r.via === 'muted') { show(cue, r); return; }
        show(cue, r);
      }
    });
  }

  /* ======================================================= breath coach (collect page) */
  function makeCoach() {
    let n = 0, lastSlower = 0, lastIn = 0;
    const on = () => !V.muted;
    return {
      get count() { return n; },
      reset() { n = 0; },
      onState(s) {
        if (!on()) return;
        const now = Date.now();
        if (s === 'INHALING' && now - lastIn > 2500) { lastIn = now; V.say('breathe_in', null, { interrupt: true }); }
        if (s === 'HOLDING') { V.say('hold', null, { interrupt: true }); ['count_3', 'count_2', 'count_1'].forEach((c) => V.say(c)); }
      },
      onEvent(ev) {
        if (!on() || ev.type !== 'too_fast_live') return;
        const now = Date.now();
        if (now - lastSlower < 3000) return;
        lastSlower = now; V.tone('slower'); V.say('slower', null, { interrupt: true });
      },
      onBreath(b) {
        if (!on()) return;
        n = Math.min(n + 1, 10);
        const label = (b && (b.label || b.rule_label)) || 'good';
        V.stop();
        if (label === 'good') { V.tone('good'); V.say('great_breath'); }
        else V.say({ too_fast: 'too_fast', too_shallow: 'breathe_deeper', no_hold: 'hold_longer' }[label] || 'encourage_3');
        V.say('breath_' + n);
        if (n >= 10) { V.say('session_complete'); n = 0; }
      },
    };
  }
  SB.voiceCoach = makeCoach();

  function mountCoachBar(bar) {
    bar.innerHTML = `<label for="vcb-lang" class="small">Voice coach</label> <select id="vcb-lang" class="sm"></select> <button class="btn sm vmute" type="button"></button> <span class="muted small vcount"></span>`;
    V.fillLangSelect(bar.querySelector('#vcb-lang'), V.lang).addEventListener('change', (e) => { V.setLang(e.target.value); V.say('ready', e.target.value, { interrupt: true }); });
    V.bindMute(bar.querySelector('.vmute'));
  }

  function boot() {
    const p = document.getElementById('voice-patient-card'); if (p) mountPatient(p);
    const c = document.getElementById('voice-check-card'); if (c) mountCheck(c);
    const b = document.getElementById('voice-coach-bar'); if (b) mountCoachBar(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
