/* SpiroBuddy – browser phone + WhatsApp simulator for the demo panel.
 * Shows the patient's and the guardian's phones. Automated calls "ring" here (dry run), play the
 * call script aloud in Hindi/English/Tamil and let the presenter press 1/2/3 – which runs the same
 * server logic as a real call. WhatsApp messages appear with tappable quick-reply buttons, the
 * weekly progress card and the voice note. Also: SB.commsDemo.mount() – the ladder controls,
 * device light/beep and the live comms feed. Needs api.js, ui.js, comms.js (voice.js optional). */
(function () {
  const SB = window.SB;
  const { esc, $, $$, toast, busy } = SB.ui;
  const C = SB.comms;

  const KEYS = {
    patient: {
      en: ['Done ✅', 'Remind me in 15 min ⏰', 'Talk to my nurse 📞'],
      hi: ['हो गया ✅', '15 मिनट बाद याद दिलाएँ ⏰', 'नर्स से बात 📞'],
      ta: ['முடிந்தது ✅', '15 நிமிடத்தில் நினைவூட்டு ⏰', 'செவிலியருடன் பேச 📞'],
    },
    guardian: {
      en: ["I'll check on them 👍", "Hear today's progress 📊", 'Talk to the nurse 📞'],
      hi: ['मैं हाल पूछता हूँ 👍', 'आज की प्रगति सुनें 📊', 'नर्स से बात 📞'],
      ta: ['நான் விசாரிக்கிறேன் 👍', 'இன்றைய நிலை 📊', 'செவிலியருடன் பேச 📞'],
    },
  };
  const T = {
    incoming: { en: 'Incoming call…', hi: 'इनकमिंग कॉल…', ta: 'அழைப்பு வருகிறது…' },
    auto: { en: 'SpiroBuddy Care · automated call', hi: 'SpiroBuddy केयर · स्वचालित कॉल', ta: 'SpiroBuddy · தானியங்கி அழைப்பு' },
    agent: { en: 'AI care assistant · check-in call', hi: 'AI देखभाल सहायक · हाल-चाल कॉल', ta: 'AI பராமரிப்பு உதவியாளர் · நலம் விசாரிப்பு' },
    speak: { en: '🎤 Tap and speak', hi: '🎤 दबाएँ और बोलें', ta: '🎤 அழுத்திப் பேசுங்கள்' },
    stop: { en: '■ Tap when done', hi: '■ बोल लिया? दबाएँ', ta: '■ முடிந்ததும் அழுத்தவும்' },
    listening: { en: 'Listening…', hi: 'सुन रहे हैं…', ta: 'கேட்கிறது…' },
    orTap: { en: 'Presenter: or tap an answer', hi: 'प्रस्तुतकर्ता: या कोई जवाब चुनें', ta: 'அல்லது ஒரு பதிலைத் தட்டவும்' },
  };
  const OUT_TXT = { red_flag: '🚨 Red flag – nurse alerted now', needs_nurse_review: '⚠ Nurse review requested', unclear: '⚠ Unclear – nurse review requested', ok: '✓ No concern raised' };

  function create(el, opts) {
    const role = opts.role; // 'patient' | 'guardian'
    let pid = opts.patientId || 1;
    let call = null, phase = null, ringTimer = null, lastSig = '', lastCount = 0, endTimer = null;
    el.innerHTML = `<div class="phone-cap" data-cap>${esc(opts.caption || '')}</div>
      <div class="phone"><div class="phone-screen">
        <div class="wa-head"><div class="av">SB</div><div><div class="nm">SpiroBuddy Care</div><div class="sub">automated · hospital care assistant</div></div></div>
        <div class="wa-body" aria-live="polite"><div class="muted small" style="align-self:center">Loading chat…</div></div>
        <form class="wa-input" autocomplete="off"><input aria-label="Presenter: type a WhatsApp reply" placeholder="Presenter: type e.g. status, help…"><button type="submit" aria-label="Send">➤</button></form>
        <div class="call-screen hidden" aria-live="assertive"></div>
      </div></div>`;
    const body = $('.wa-body', el), callEl = $('.call-screen', el), cap = $('[data-cap]', el);

    /* ---- WhatsApp chat ---- */
    function renderThread(th) {
      const items = th.items || [];
      const sig = JSON.stringify(items.map((x) => [x.id, x.answered]));
      if (sig === lastSig) return;
      const grew = items.length > lastCount;
      if (lastSig && grew && items[items.length - 1].dir === 'out') C.beep(1200, 0, 0.08, 0.08);
      lastSig = sig; lastCount = items.length;
      body.innerHTML = items.length ? items.map((m) => {
        const time = new Date(m.at);
        const t = isNaN(time) ? '' : time.toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
        const btns = m.buttons && m.buttons.length ? `<div class="wa-btns">${m.buttons.map((b) => `<button type="button" data-payload="${esc(b.payload)}" ${m.answered ? 'disabled' : ''}>${esc(b.label)}</button>`).join('')}</div>` : '';
        const img = m.image ? `<img src="${esc(m.image)}" alt="Weekly progress card" loading="lazy" data-zoom>` : '';
        const audio = m.audio ? `<button class="wa-play" type="button" data-speak="${esc(m.id)}">▶ 0:20 voice note</button>` : '';
        return `<div class="wa-msg ${m.dir === 'in' ? 'in' : ''}" data-mid="${esc(m.id)}">${img}${audio}${esc(m.text || '')}${btns}<div class="t">${m.dir === 'out' && m.dry_run ? '<span class="wa-dry">dry run · </span>' : ''}${esc(t)}${m.dir === 'in' ? ' ✓✓' : ''}</div></div>`;
      }).join('') : '<div class="muted small" style="align-self:center;padding:1rem;text-align:center">No messages yet.<br>Press “Play escalation ladder”.</div>';
      body.scrollTop = body.scrollHeight;
      body._items = items;
      body._lang = th.language;
    }
    body.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-payload]');
      if (b) {
        b.disabled = true;
        C.api.reply({ patient_id: pid, role, payload: b.dataset.payload, text: b.textContent })
          .then((r) => { toast(`${role === 'patient' ? 'Patient' : 'Family'} tapped “${b.textContent}”`, 'good'); refreshThread(); })
          .catch((err) => toast(err.message, 'bad'));
        return;
      }
      const sp = e.target.closest('[data-speak]');
      if (sp) {
        const m = (body._items || []).find((x) => x.id === sp.dataset.speak);
        if (m) C.speak((m.text || '').replace(/^🎧\s*/, '').split('\n\n—')[0], body._lang || 'hi', { interrupt: true });
        return;
      }
      const z = e.target.closest('img[data-zoom]');
      if (z) window.open(z.src, '_blank', 'noopener');
    });
    $('.wa-input', el).addEventListener('submit', (e) => {
      e.preventDefault();
      const inp = $('input', e.currentTarget); const text = inp.value.trim();
      if (!text) return;
      inp.value = '';
      C.api.reply({ patient_id: pid, role, text }).then((r) => { if (r.intent === 'red_flag') toast('🚨 Red flag – nurse alerted, fixed 112 message sent', 'bad', 6000); refreshThread(); }).catch((err) => toast(err.message, 'bad'));
    });
    async function refreshThread() {
      if (SB.api.state.mock) { body.innerHTML = '<div class="muted small" style="align-self:center;padding:1rem">Needs the live server.</div>'; return; }
      try { renderThread(await C.api.thread(pid, role)); } catch (_) { /* offline – banner shows it */ }
    }

    /* ---- calls ---- */
    function lang() { return (call && call.language) || 'hi'; }
    function stopRing() { clearInterval(ringTimer); ringTimer = null; }
    function closeCall(delay) {
      clearTimeout(endTimer);
      endTimer = setTimeout(() => { callEl.classList.add('hidden'); callEl.innerHTML = ''; call = null; phase = null; }, delay || 0);
    }
    function showRinging(c) {
      call = c; phase = 'ringing';
      callEl.className = 'call-screen ringing';
      const sub = c.style === 'agent' ? T.agent : T.auto;
      callEl.innerHTML = `<div class="cstate">${esc(T.incoming[lang()] || T.incoming.en)}</div><div class="cav">${c.style === 'agent' ? '🗣' : '📞'}</div>
        <div class="cname">SpiroBuddy Care</div><div class="cstate">${esc(sub[lang()] || sub.en)}</div>
        <div class="cstate small">to ${esc(c.to_name)} · ${esc(c.to_number || '')}</div>
        <div class="call-actions"><button class="dec" type="button" aria-label="Decline call">✕</button><button class="acc" type="button" aria-label="Answer call">✆</button></div>`;
      C.ring(); stopRing(); ringTimer = setInterval(() => phase === 'ringing' && C.ring(), 2600);
      $('.acc', callEl).addEventListener('click', answer);
      $('.dec', callEl).addEventListener('click', () => { stopRing(); C.api.hangup(c.id, 'declined').catch(() => {}); closeCall(); });
      if (opts.onRing) opts.onRing(c);
    }
    async function answer() {
      stopRing();
      phase = 'talking';
      const c = await C.api.answer(call.id).catch(() => call);
      call = Object.assign({}, call, c);
      if (call.style === 'agent') return agentCall();
      const keys = KEYS[role][lang()] || KEYS[role].en;
      callEl.className = 'call-screen';
      callEl.innerHTML = `<div class="cname">SpiroBuddy Care</div><div class="cstate" data-timer>00:00 · ${esc(T.auto[lang()] || T.auto.en)}</div>
        <div class="ctext" data-text>${esc(call.script || '')}</div>
        <div class="keypad">${keys.map((k, i) => `<button type="button" data-d="${i + 1}"><span class="k">${i + 1}</span>${esc(k)}</button>`).join('')}
          <button type="button" class="end" data-end aria-label="End call">✕ End call</button></div>`;
      const started = Date.now();
      const tm = setInterval(() => { const n = $('[data-timer]', callEl); if (!n || phase !== 'talking') return clearInterval(tm); const s = Math.round((Date.now() - started) / 1000); n.textContent = `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')} · ${T.auto[lang()] || T.auto.en}`; }, 1000);
      $$('.keypad [data-d]', callEl).forEach((b) => b.addEventListener('click', () => press(b.dataset.d)));
      $('[data-end]', callEl).addEventListener('click', () => { C.stopSpeaking(); C.api.hangup(call.id, 'hangup').catch(() => {}); phase = 'ended'; closeCall(); });
      C.speak(call.script, lang(), { audioUrl: call.audio_url, interrupt: true });
    }
    async function press(d) {
      C.beep(697 + Number(d) * 40, 0, 0.12, 0.1);
      C.stopSpeaking();
      try {
        const r = await C.api.press(call.id, d);
        $('[data-text]', callEl).textContent = r.say;
        await C.speak(r.say, r.language || lang(), { audioUrl: r.audio_url, interrupt: true });
        if (r.end) {
          phase = 'ended';
          $('.keypad', callEl).innerHTML = `<div class="cstate" style="text-align:center">Call ended · pressed ${esc(d)}</div>`;
          closeCall(2500);
          refreshThread();
        }
      } catch (e) { toast(e.message, 'bad'); }
    }
    /* ---- conversational (Sarvam-style) call: the agent speaks, the presenter answers by voice
       (Voice.record -> /api/voice/stt, or the browser's own recognition) or taps an answer ---- */
    let rec = null;
    function agentCall() {
      const L = lang();
      callEl.className = 'call-screen';
      callEl.innerHTML = `<div class="cname">SpiroBuddy Care</div><div class="cstate">${esc(T.agent[L] || T.agent.en)}</div>
        <div class="ctext" data-text aria-live="polite">${esc(call.script || '')}</div>
        <div class="agent-talk" data-talk></div>`;
      renderAnswers(call.answers || []);
      C.speak(call.script, L, { audioUrl: call.audio_url, interrupt: true });
    }
    function renderAnswers(answers) {
      const L = lang();
      const box = $('[data-talk]', callEl); if (!box) return;
      const canRec = !!(window.Voice && Voice.record);
      box.innerHTML = `${canRec ? `<button type="button" class="mic" data-mic>${esc(T.speak[L] || T.speak.en)}</button>` : ''}
        ${answers.length ? `<div class="hint">${esc(T.orTap[L] || T.orTap.en)}</div>` : ''}
        ${answers.map((a) => `<button type="button" class="ans" data-ans>${esc(a)}</button>`).join('')}
        <div class="keypad" style="margin-top:.2rem;padding-top:0"><button type="button" class="end" data-end aria-label="End call">✕ End call</button></div>`;
      $$('[data-ans]', box).forEach((b) => b.addEventListener('click', () => sendAnswer(b.textContent, 'tap')));
      const mic = $('[data-mic]', box);
      if (mic) mic.addEventListener('click', toggleMic);
      $('[data-end]', box).addEventListener('click', () => {
        C.stopSpeaking(); if (rec) { rec.cancel(); rec = null; }
        C.api.hangup(call.id, 'hangup').then(showResult).catch(() => {});
        phase = 'ended'; closeCall(3500);
      });
    }
    function toggleMic(e) {
      const L = lang();
      const btn = e.currentTarget;
      if (rec) { rec.stop(); btn.textContent = T.listening[L] || T.listening.en; btn.disabled = true; return; }
      C.stopSpeaking();
      rec = Voice.record({ lang: L, speak: false });
      btn.classList.add('rec'); btn.textContent = T.stop[L] || T.stop.en;
      rec.done.then((r) => {
        rec = null;
        if (r && r.text) return sendAnswer(r.text, 'voice');
        btn.classList.remove('rec'); btn.disabled = false; btn.textContent = T.speak[L] || T.speak.en;
        if (r && !r.cancelled) toast((r && r.error) || 'Nothing was heard – tap an answer instead', '', 5000);
      }).catch(() => { rec = null; });
    }
    async function sendAnswer(text, source) {
      if (!call || phase !== 'talking') return;
      C.stopSpeaking();
      $$('[data-talk] button', callEl).forEach((b) => { b.disabled = true; });
      const t = $('[data-text]', callEl);
      t.innerHTML = `<div style="opacity:.8">🧓 “${esc(text)}”</div>`;
      try {
        const r = await C.api.agentTurn(call.id, text, source);
        t.insertAdjacentHTML('beforeend', `<div style="margin-top:.35rem">🤖 ${esc(r.say || '')}</div>`);
        t.scrollTop = t.scrollHeight;
        const spoken = C.speak(r.say, r.language || lang(), { audioUrl: r.audio_url, interrupt: true });
        if (r.end) {
          phase = 'ended';
          showResult(r.call || { result: r.result });
          await spoken;
          closeCall(6000);
          refreshThread();
        } else renderAnswers(r.answers || []);
      } catch (e) { toast(e.message, 'bad'); renderAnswers(call.answers || []); }
    }
    function showResult(c) {
      const res = c && c.result; const box = $('[data-talk]', callEl);
      if (!res || !box) return;
      box.innerHTML = `<div class="agent-res"><b>${esc(OUT_TXT[res.outcome] || res.label || '')}</b>${esc(res.neutral_note || '')}<div class="small" style="opacity:.75;margin-top:.25rem">Sent to the nurse dashboard · decided by fixed rules, not the AI</div></div>`;
      if (res.outcome === 'red_flag') toast('🚨 Red flag on the check-in call – nurse + family alerted', 'bad', 7000);
      else if (res.outcome) toast('🗒 Check-in call note sent to the nurse', 'good', 5000);
    }

    async function pollCalls() {
      if (SB.api.state.mock) return;
      const list = await C.api.calls(pid, true);
      const mine = list.filter((c) => c.simulated && (role === 'guardian' ? c.to_role === 'guardian' : c.to_role === 'patient' && c.purpose !== 'nurse_bridge'));
      if (!call && mine.length && mine[0].status === 'ringing') { showRinging(mine[0]); return; }
      if (call && phase === 'ringing' && !mine.some((c) => c.id === call.id)) {
        stopRing(); phase = 'missed';
        callEl.className = 'call-screen';
        callEl.innerHTML = `<div class="cav">📵</div><div class="cname">Missed call</div><div class="cstate">SpiroBuddy Care – nobody picked up</div>`;
        closeCall(2200);
      }
    }

    SB.ui.poll(refreshThread, 2000);
    SB.ui.poll(() => pollCalls().catch(() => {}), 1000);
    return {
      setPatient(id, caption) { pid = id; lastSig = ''; lastCount = 0; if (call) { stopRing(); closeCall(); } cap.textContent = caption || ''; refreshThread(); },
      setCaption(t) { cap.textContent = t; },
    };
  }

  /* ---------------------------------------------------------------------------- demo panel */
  function mountDemo(el) {
    let pid = 1, sinceId = 0, patients = [], care = null;
    el.innerHTML = `
      <div class="card-head"><h2 style="margin:0">📞 Calls &amp; WhatsApp – live simulators</h2><span class="muted small">no phone signal needed · the same logic as real calls</span></div>
      <div class="sim-grid">
        <div class="sim-controls">
          <div class="mini-form">
            <div class="field"><label for="cd-p">Patient</label><select id="cd-p"></select></div>
            <div class="field"><label class="row" style="gap:.4rem"><input type="checkbox" id="cd-quiet"> Respect quiet hours</label></div>
          </div>
          <div class="row" style="margin:.6rem 0">
            <button class="btn primary lg" id="cd-play" type="button" title="Shortcut: L">▶ Play escalation ladder (≈60 s)</button>
            <button class="btn danger" id="cd-stop" type="button" hidden>■ Stop</button>
            <button class="btn" id="cd-next" type="button" hidden>⏭ Next step</button>
          </div>
          <div class="row" style="margin-bottom:.6rem">
            <button class="btn poor" id="cd-red" type="button" title="Patient writes red-flag words">🚨 Red-flag message</button>
            <button class="btn" id="cd-card" type="button">🖼 Weekly card</button>
            <button class="btn" id="cd-voice" type="button">🎧 Voice note</button>
            <a class="btn" id="cd-guardian" target="_blank" rel="noopener">👪 Family page ↗</a>
          </div>
          <div class="row" style="margin-bottom:.6rem">
            <label class="small" for="cd-style">Patient's call</label>
            <select id="cd-style" class="sm-select" title="How the ladder's automated call to the patient works">
              <option value="ivr">⌨ Keypad menu (press 1 / 2 / 3)</option>
              <option value="agent">🗣 AI conversation (Sarvam-style)</option></select>
          </div>
          <div class="row" style="margin-bottom:.6rem">
            <button class="btn primary" id="cd-nurse" type="button" title="A person calls: the nurse's phone rings first, then the patient (click-to-call)">☎ Nurse calls patient</button>
            <button class="btn sm" id="cd-checkin" type="button" title="Backup: ring the patient now with the automated AI check-in call (needs consent; some reminder calls need consent renewed weekly)">🗣 Automated check-in call (backup)</button>
          </div>
          <div class="row" style="margin-bottom:.6rem">
            <select id="cd-sample" class="sm-select" aria-label="Saved Sarvam call result"><option value="pain">Loading samples…</option></select>
            <button class="btn" id="cd-replay" type="button" title="Backup if a live call fails: feeds a saved Sarvam webhook through the real handler">⏯ Replay saved Sarvam result</button>
          </div>
          <ul class="call-res" id="cd-results" aria-live="polite"></ul>
          <div class="muted small" id="cd-hint"></div>
          <div id="cd-run" style="margin:.5rem 0"></div>
          <div class="device" id="cd-device" title="The SpiroBuddy unit on the spirometer"><div class="unit"><div class="led"></div></div><div><b>SpiroBuddy unit</b><div class="small muted" id="cd-device-t">Idle · light off</div></div></div>
          <h3 style="margin:.9rem 0 .3rem">Live comms feed</h3>
          <ul class="timeline feed" id="cd-feed"><li class="muted">Waiting for events…</li></ul>
        </div>
        <div id="cd-phone-p"></div>
        <div id="cd-phone-g"></div>
      </div>`;
    const phoneP = create($('#cd-phone-p', el), { role: 'patient', caption: '' });
    const phoneG = create($('#cd-phone-g', el), { role: 'guardian', caption: '' });

    function captions() {
      const p = patients.find((x) => String(x.id) === String(pid));
      const g = care && care.guardians && care.guardians[0];
      phoneP.setPatient(pid, p ? `${p.name.split(' ')[0]}'s phone (patient)` : 'Patient phone');
      phoneG.setPatient(pid, g ? `${g.name.split(' ')[0]}'s phone (${g.relation || 'family'}${g.city ? ', ' + g.city.replace(/ \(.*\)/, '') : ''})` : 'Guardian phone (none in care circle)');
      $('#cd-guardian', el).href = g ? SB.ui.link(g.link) : '#';
      if (care && care.settings) $('#cd-style', el).value = care.settings.call_style || 'ivr';
    }
    $('#cd-style', el).addEventListener('change', (e) => {
      C.api.putCare(pid, { call_style: e.target.value })
        .then((r) => { care = Object.assign({}, care, r); toast(e.target.value === 'agent' ? '🗣 The ladder now calls with the AI conversation' : '⌨ The ladder now calls with the keypad menu', 'good'); })
        .catch((err) => toast(err.message, 'bad'));
    });
    C.api.sarvamSamples().then((list) => {
      $('#cd-sample', el).innerHTML = list.map((s) => `<option value="${esc(s.key)}">${esc(s.label)}</option>`).join('');
    }).catch(() => {});
    async function refreshResults() {
      if (SB.api.state.mock) return;
      const list = (await C.api.calls(pid, false)).filter((c) => c.result).slice(0, 3);
      const html = list.map(C.callResult).join('');
      if (html !== refreshResults.last) { refreshResults.last = html; $('#cd-results', el).innerHTML = html; }
    }
    async function loadPatients() {
      patients = await SB.api.patients();
      $('#cd-p', el).innerHTML = patients.map((p) => `<option value="${p.id}" ${String(p.id) === String(pid) ? 'selected' : ''}>${esc(p.name)}${String(p.id) === '1' ? ' ★' : ''}</option>`).join('');
      care = await C.api.care(pid).catch(() => null);
      captions();
    }
    $('#cd-p', el).addEventListener('change', async (e) => { pid = Number(e.target.value); care = await C.api.care(pid).catch(() => null); captions(); refreshRun(); });

    const run = (fn) => (e) => { C.unlockAudio(); busy(e.currentTarget, fn).then(refreshRun).catch(() => {}); };
    $('#cd-play', el).addEventListener('click', run(async () => {
      const r = await C.api.demoLadder(pid, !$('#cd-quiet', el).checked);
      toast('▶ Ladder playing – watch the phones', 'good');
      return r;
    }));
    $('#cd-nurse', el).addEventListener('click', run(async () => {
      const r = await C.api.callPatient(pid, C.me());
      toast(r.dry_run ? `Dry run – would ring ${C.me()}'s phone first, then connect the patient` : r.error ? '✖ Call failed: ' + r.error : '📞 Calling – the nurse’s phone rings first', r.error ? 'bad' : 'good', 6000);
      return r;
    }));
    $('#cd-stop', el).addEventListener('click', run(async () => { if (curRun) await C.api.stopRun(curRun.id, 'presenter'); }));
    $('#cd-next', el).addEventListener('click', run(async () => { if (curRun) await C.api.advanceRun(curRun.id); }));
    $('#cd-red', el).addEventListener('click', run(async () => {
      const r = await C.api.demoRedFlag(pid);
      toast('🚨 Red flag: fixed 112 message sent, nurse + family alerted', 'bad', 6000);
      C.speak(r.reply, (patients.find((x) => x.id === pid) || {}).language || 'hi', { interrupt: true });
    }));
    $('#cd-checkin', el).addEventListener('click', run(async () => {
      const c = await C.api.checkinCall(pid);
      toast(c.provider === 'sarvam_agent' ? '🗣 Sarvam is dialling the real phone – result appears when its webhook arrives' : '🗣 AI check-in call ringing on the patient phone', 'good', 6000);
    }));
    $('#cd-replay', el).addEventListener('click', run(async () => {
      const r = await C.api.sarvamReplay(pid, $('#cd-sample', el).value);
      const res = r.result || {};
      toast(res.outcome === 'red_flag' ? '🚨 Replayed: red flag – nurse + family alerted' : `🗒 Replayed: ${res.neutral_note || res.outcome}`, res.outcome === 'red_flag' ? 'bad' : 'good', 7000);
      refreshResults.last = null; await refreshResults();
    }));
    $('#cd-card', el).addEventListener('click', run(async () => { const r = await C.api.weeklyCard(pid, 'family'); toast(r.sent ? 'Weekly card sent' : 'Weekly card – dry run (see the family phone)', r.sent ? 'good' : ''); }));
    $('#cd-voice', el).addEventListener('click', run(async () => { const r = await C.api.voiceNote(pid, 'family'); C.speak(r.speak_text, r.language, { audioUrl: r.audio_url, interrupt: true }); }));
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || /INPUT|SELECT|TEXTAREA/.test(e.target.tagName)) return;
      if (e.key.toLowerCase() === 'l') { e.preventDefault(); $('#cd-play', el).click(); }
    });

    let curRun = null;
    async function refreshRun() {
      if (SB.api.state.mock) { $('#cd-run', el).innerHTML = '<div class="banner mock" style="margin:0">Needs the live server – simulators are off in mock mode.</div>'; return; }
      const [runs, st] = await Promise.all([C.api.runs(pid), refreshRun.st && Date.now() - refreshRun.stAt < 15000 ? Promise.resolve(refreshRun.st) : C.api.status()]);
      if (st !== refreshRun.st) { refreshRun.st = st; refreshRun.stAt = Date.now(); }
      const r = runs[0];
      curRun = r && r.status === 'active' ? r : null;
      $('#cd-run', el).innerHTML = r ? `<div class="row">${C.runSummary(r)}</div>${C.stepper(r)}` : '<div class="muted small">No ladder yet for this patient.</div>';
      $('#cd-stop', el).hidden = !curRun; $('#cd-next', el).hidden = !curRun;
      const q = st.quiet_hours || {};
      const wl = st.whatsapp_last;
      $('#cd-hint', el).textContent = `Keypad calls: ${st.calls_provider === 'dry_run' ? 'simulated here (no call keys)' : st.calls_provider} · AI check-in calls: ${st.checkin_provider === 'sarvam_agent' ? 'Sarvam Voice Agent (live)' : 'simulated here'} · WhatsApp: ${st.whatsapp_enabled ? 'live (Twilio)' : 'dry run'} · voices: ${st.voice_tts ? 'Sarvam' : 'browser'} · quiet hours ${q.start}–${q.end} IST${q.now_quiet ? ' – it is quiet hours now: untick “Respect quiet hours” to play calls' : ''}.${wl && wl.hint ? ' ⚠ WhatsApp: ' + wl.hint : st.whatsapp_hint ? ' ' + st.whatsapp_hint : ''}`;
      if (refreshRun.first == null) { refreshRun.first = true; $('#cd-quiet', el).checked = !q.now_quiet; }
    }

    function deviceBeep(name) {
      const d = $('#cd-device', el);
      d.classList.remove('beep'); void d.offsetWidth; d.classList.add('beep');
      $('#cd-device-t', el).textContent = `Beep! Blinking teal light – ${name}, time for 10 breaths`;
      C.chime();
      setTimeout(() => { d.classList.remove('beep'); $('#cd-device-t', el).textContent = 'Idle · light off'; }, 6000);
    }
    async function pollFeed() {
      if (SB.api.state.mock) return;
      const evs = await C.api.events(sinceId, 30);
      if (!evs.length) { if (!sinceId) $('#cd-feed', el).innerHTML = '<li class="muted">No events yet.</li>'; return; }
      const first = sinceId === 0;
      sinceId = Math.max(sinceId, ...evs.map((e) => e.id));
      const feed = $('#cd-feed', el);
      if (first) feed.innerHTML = '';
      evs.slice().reverse().forEach((e) => {
        feed.insertAdjacentHTML('afterbegin', C.eventRow(e, { showPatient: true }));
        if (!first) feed.firstElementChild.classList.add('new');
        if (first) return;
        if (e.kind === 'device_beep' && e.patient_id === pid) deviceBeep((e.to_name || '').split(' ')[0]);
        if (e.kind === 'nurse_alert' && e.status === 'ok') toast('🚨 ' + (e.detail || e.title), 'bad', 7000);
        if (e.kind === 'cheer' && /played/.test(e.title || '') && e.patient_id === pid) {
          toast('💛 ' + e.title, 'good', 6000);
          C.speak(e.detail, /[ऀ-ॿ]/.test(e.detail || '') ? 'hi' : 'en');
        }
      });
      while (feed.children.length > 60) feed.lastElementChild.remove();
    }

    loadPatients().catch(() => {});
    SB.ui.poll(() => refreshRun().catch(() => {}), 1000);
    SB.ui.poll(() => refreshResults().catch(() => {}), 2500);
    SB.ui.poll(() => pollFeed().catch(() => {}), 1500);
  }

  SB.phoneSim = { create };
  SB.commsDemo = { mount: mountDemo };
})();
