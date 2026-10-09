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
  };

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
        const t = isNaN(time) ? '' : time.toLocaleString([], { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
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
      callEl.innerHTML = `<div class="cstate">${esc(T.incoming[lang()] || T.incoming.en)}</div><div class="cav">📞</div>
        <div class="cname">SpiroBuddy Care</div><div class="cstate">${esc(T.auto[lang()] || T.auto.en)}</div>
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
    $('#cd-stop', el).addEventListener('click', run(async () => { if (curRun) await C.api.stopRun(curRun.id, 'presenter'); }));
    $('#cd-next', el).addEventListener('click', run(async () => { if (curRun) await C.api.advanceRun(curRun.id); }));
    $('#cd-red', el).addEventListener('click', run(async () => {
      const r = await C.api.demoRedFlag(pid);
      toast('🚨 Red flag: fixed 112 message sent, nurse + family alerted', 'bad', 6000);
      C.speak(r.reply, (patients.find((x) => x.id === pid) || {}).language || 'hi', { interrupt: true });
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
      const [runs, st] = await Promise.all([C.api.runs(pid), refreshRun.st ? Promise.resolve(refreshRun.st) : C.api.status()]);
      refreshRun.st = st;
      const r = runs[0];
      curRun = r && r.status === 'active' ? r : null;
      $('#cd-run', el).innerHTML = r ? `<div class="row">${C.runSummary(r)}</div>${C.stepper(r)}` : '<div class="muted small">No ladder yet for this patient.</div>';
      $('#cd-stop', el).hidden = !curRun; $('#cd-next', el).hidden = !curRun;
      const q = st.quiet_hours || {};
      $('#cd-hint', el).textContent = `Calls: ${st.calls_provider === 'dry_run' ? 'simulated here (no call keys)' : st.calls_provider} · WhatsApp: ${st.whatsapp_enabled ? 'live (Twilio)' : 'dry run'} · voices: ${st.voice_tts ? 'Sarvam' : 'browser'} · quiet hours ${q.start}–${q.end} IST${q.now_quiet ? ' – it is quiet hours now: untick “Respect quiet hours” to play calls' : ''}.`;
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
    SB.ui.poll(() => pollFeed().catch(() => {}), 1500);
  }

  SB.phoneSim = { create };
  SB.commsDemo = { mount: mountDemo };
})();
