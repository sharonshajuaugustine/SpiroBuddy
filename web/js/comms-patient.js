/* SpiroBuddy – patient page comms panels: click-to-call + AI call script + trend observation +
 * this patient's alerts, the escalation ladder with its timeline, and the care circle settings
 * (patient phone, consent, quiet hours, ladder delays, guardians, magic links, weekly card).
 * Needs api.js, ui.js, comms.js. */
(function () {
  const SB = window.SB;
  const { esc, $, $$, toast, busy, ago, ic } = SB.ui;
  const C = SB.comms;
  const LANGS = { hi: 'Hindi', en: 'English', ta: 'Tamil', ml: 'Malayalam', te: 'Telugu', kn: 'Kannada', bn: 'Bengali', mr: 'Marathi', gu: 'Gujarati' };
  const CH = { both: 'WhatsApp + call', whatsapp: 'WhatsApp only', call: 'Call only', sms: 'SMS (dry run)' };
  const RELS = ['son', 'daughter', 'daughter-in-law', 'son-in-law', 'wife', 'husband', 'grandson', 'granddaughter', 'brother', 'sister', 'neighbour', 'friend'];

  function mount(pid, els) {
    let data = null, lastEventIds = null, careFilled = false;

    /* ---------- actions card ---------- */
    els.actions.innerHTML = `
      <div class="card-head"><h2>${ic('phone')}Care team actions</h2><div class="spacer"></div><span id="cp-provider" class="muted small"></span></div>
      <div class="row" style="margin-bottom:.6rem">
        <button class="btn primary" id="cp-call" type="button" title="A nurse calls: your phone rings first, then the patient – nobody sees the other's number">${ic('phone')}Nurse: call patient now</button>
        <button class="btn" id="cp-script" type="button" title="Opening lines for your call – it does not diagnose">${ic('sparkles')}Call script</button>
        <span class="muted small">Calling as <b id="cp-me"></b></span>
      </div>
      <div class="row" style="margin-bottom:.6rem">
        <button class="btn sm" id="cp-checkin" type="button" title="Automated AI check-in call: asks if they are okay and why the exercise was missed (needs recorded consent)">AI check-in call – optional, where consent allows</button>
        <span class="muted small">A nurse calls first; the AI call is only a backup. Some reminder calls need consent renewed weekly.</span>
      </div>
      <div id="cp-call-res" aria-live="polite"></div>
      <div class="script-box" id="cp-script-box" hidden></div>
      <div id="cp-trend" style="margin-top:.6rem"></div>
      <h3 class="section-title">Check-in call notes</h3>
      <ul class="call-res" id="cp-calls"><li class="muted" style="border:0;background:none;padding:0">No AI check-in calls yet.</li></ul>
      <h3 class="section-title">Open alerts for this patient</h3>
      <ul class="alerts" id="cp-alerts" style="max-height:300px"><li class="muted">–</li></ul>`;
    $('#cp-me', els.actions).textContent = C.me();
    $('#cp-call', els.actions).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const r = await C.api.callPatient(pid, C.me());
      $('#cp-call-res', els.actions).innerHTML = `<div class="drybox${r.dry_run ? '' : ' sent'}"><div class="t">${r.dry_run ? 'DRY RUN – would ring your phone first, then connect the patient' : r.error ? '✖ Call failed' : '📞 Calling – your phone rings first'}</div><div class="small">${esc(r.error || r.note || '')}</div></div>`;
      await refresh();
    }).catch(() => {}));
    $('#cp-script', els.actions).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const box = $('#cp-script-box', els.actions);
      box.hidden = false; box.textContent = 'Writing a call script…';
      const r = await C.api.callScript(pid);
      box.innerHTML = `<div class="row" style="margin-bottom:.35rem"><b>Call script</b>${r.source === 'llm' ? '<span class="source-tag llm">AI (Claude)</span>' : '<span class="source-tag" title="No AI key or the AI call failed – fixed template">Template</span>'}<span class="muted small">Helps you open the call – it does not diagnose.</span></div>${esc(r.text)}`;
    }).catch(() => {}));
    $('#cp-checkin', els.actions).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const c = await C.api.checkinCall(pid);
      toast(c.provider === 'sarvam_agent' ? 'Sarvam is calling – the note appears when the result arrives' : 'Dry run – the AI check-in call rings in the phone simulator (Demo page)', c.provider === 'sarvam_agent' ? 'good' : '', 6000);
      await refresh();
    }).catch(() => {}));
    $('#cp-alerts', els.actions).addEventListener('click', (e) => {
      const b = e.target.closest('button[data-act]'); if (!b) return;
      const id = b.closest('[data-id]').dataset.id;
      busy(b, async () => { await C.api.alertAct(id, b.dataset.act, { by: C.me(), minutes: 30, to: C.me() }); toast('Done', 'good'); await refresh(); }).catch(() => {});
    });

    /* ---------- ladder card ---------- */
    els.ladder.innerHTML = `
      <div class="card-head"><h2>Escalation ladder</h2><span class="muted small">beep → WhatsApp → call → family → nurse</span><div class="spacer"></div>
        <button class="btn sm" id="lad-start" type="button" title="Start the ladder now at real speed">${ic('play', { size: 14 })}Start now</button>
        <button class="btn sm" id="lad-fast" type="button" title="Demo: the whole ladder in about 60 seconds">⏩ Fast-forward</button>
        <button class="btn sm" id="lad-next" type="button" hidden>⏭ Next step now</button>
        <button class="btn sm danger" id="lad-stop" type="button" hidden>■ Stop</button></div>
      <div id="lad-run"><div class="muted">No ladder running. It starts by itself after missed sessions (see Care circle).</div></div>
      <h3 class="section-title">Communications timeline</h3>
      <ul class="timeline" id="lad-tl"><li class="muted">Loading…</li></ul>`;
    const act = (fn) => (e) => busy(e.currentTarget, async () => { await fn(); await refresh(); }).catch(() => {});
    $('#lad-start', els.ladder).addEventListener('click', act(() => C.api.startRun(pid, { speed: 'real', reason: 'manual' })));
    $('#lad-fast', els.ladder).addEventListener('click', act(() => C.api.demoLadder(pid, true)));
    $('#lad-next', els.ladder).addEventListener('click', act(() => data.active_run && C.api.advanceRun(data.active_run.id)));
    $('#lad-stop', els.ladder).addEventListener('click', act(() => data.active_run && C.api.stopRun(data.active_run.id, C.me())));

    /* ---------- care circle card ---------- */
    els.care.innerHTML = `
      <div class="card-head"><h2>${ic('users')}Care circle &amp; reminders</h2><span class="muted small">who is told, how and when (IST)</span></div>
      <form id="cc-form" class="mini-form" autocomplete="off">
        <div class="field"><label for="cc-phone">Patient's phone</label><input id="cc-phone" type="tel" placeholder="+91 98xxx xxxxx"></div>
        <div class="field"><label for="cc-qs">Quiet from</label><input id="cc-qs" type="time"></div>
        <div class="field"><label for="cc-qe">Quiet until</label><input id="cc-qe" type="time"></div>
        <div class="field"><label for="cc-style">Patient's call</label><select id="cc-style"><option value="ivr">Keypad menu (press 1/2/3)</option><option value="agent">AI conversation (spoken answers)</option></select></div>
        <div class="field"><label for="cc-trig">Start after missed</label><select id="cc-trig">${[1, 2, 3, 4].map((n) => `<option value="${n}">${n} in a row</option>`).join('')}</select></div>
        <div class="field"><label class="row" style="gap:.4rem"><input type="checkbox" id="cc-auto"> Start automatically</label>
          <label class="row" style="gap:.4rem"><input type="checkbox" id="cc-consent"> Consent recorded</label></div>
      </form>
      <div class="muted small" id="cc-consent-note" style="margin:.35rem 0"></div>
      <div class="row" style="margin:.25rem 0 .5rem">
        <button class="btn sm" id="cc-read" type="button" title="Play the consent statement to the patient in their language (itemised data list, one-word STOP)">🔊 Read consent aloud</button>
        <button class="btn sm" id="cc-renew" type="button" hidden title="Some reminder calls need consent renewed weekly (TRAI)">↻ Consent re-confirmed today</button>
        <button class="btn sm" id="cc-ask" type="button" title="Send the weekly one-tap question on WhatsApp: keep the reminders? ✅ yes / ⛔ STOP">📨 Ask “keep reminders?”</button>
      </div>
      <div class="script-box" id="cc-consent-text" hidden></div>
      <details style="margin:.5rem 0"><summary><b>Ladder steps and delays</b></summary><div class="steps-edit" id="cc-steps" style="margin-top:.5rem"></div></details>
      <div class="row" style="margin:.5rem 0 1rem"><button class="btn primary" id="cc-save" type="button">Save settings</button><span class="muted small">Quiet hours hold calls and messages, except red-flag.</span></div>
      <h3 class="section-title">Family (guardians)</h3>
      <div class="guardians" id="cc-guardians"></div>
      <details style="margin-top:.75rem"><summary><b>＋ Add a family member</b></summary>
        <form id="cc-add" class="mini-form" style="margin-top:.5rem" autocomplete="off">
          <div class="field"><label for="ga-name">Name</label><input id="ga-name" required placeholder="e.g. Amit Kumar"></div>
          <div class="field"><label for="ga-rel">Relation</label><select id="ga-rel">${RELS.map((r) => `<option>${r}</option>`).join('')}</select></div>
          <div class="field"><label for="ga-phone">Phone (with country code)</label><input id="ga-phone" type="tel" placeholder="+91 98xxx xxxxx · +971 / +44 … abroad"></div>
          <div class="field"><label for="ga-lang">Language</label><select id="ga-lang">${Object.entries(LANGS).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select></div>
          <div class="field"><label for="ga-ch">How to reach</label><select id="ga-ch">${Object.entries(CH).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select></div>
          <div class="field"><label class="row" style="gap:.4rem"><input type="checkbox" id="ga-consent" checked> Consent recorded</label></div>
          <div class="field"><button class="btn primary" type="submit">Add</button></div>
        </form></details>
      <div class="row" style="margin-top:1rem">
        <button class="btn" id="cc-card" type="button">🖼 Send weekly progress card</button>
        <button class="btn" id="cc-voice" type="button">🎧 Send voice-note summary</button>
        <a class="btn" id="cc-card-view" target="_blank" rel="noopener">View card ↗</a>
      </div>
      <div id="cc-send-res" aria-live="polite"></div>`;

    function fillCare(s) {
      $('#cc-phone', els.care).value = s.patient_phone || '';
      $('#cc-qs', els.care).value = s.quiet_start || '21:00';
      $('#cc-qe', els.care).value = s.quiet_end || '07:00';
      $('#cc-trig', els.care).value = String(s.trigger_missed || 2);
      $('#cc-style', els.care).value = s.call_style || 'ivr';
      $('#cc-auto', els.care).checked = !!s.auto;
      $('#cc-consent', els.care).checked = !!s.consent;
      $('#cc-steps', els.care).innerHTML = s.steps.map((st) => `<label data-key="${esc(st.key)}"><input type="checkbox" ${st.enabled ? 'checked' : ''}> ${esc(st.label)} <span class="muted small">after</span> <input type="number" min="0" max="180" value="${esc(st.delay_min)}" aria-label="minutes before ${esc(st.label)}"> <span class="muted small">min</span></label>`).join('');
      careFilled = true;
    }
    function consentNote(s) {
      const when = s.consent_at ? new Date(s.consent_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '';
      $('#cc-consent-note', els.care).textContent = s.consent_ok
        ? `Consent for automated calls/WhatsApp recorded on ${when} (TRAI rules).${s.consent_renew_due ? ` ⚠ It is ${s.consent_age_days} days old – some reminder calls need consent renewed weekly (TRAI): please re-confirm with the patient.` : ''} Automated calls in production go through an Indian provider (Exotel or a Sarvam-rented number); in this demo they ring in the phone simulator.`
        : '⚠ No consent recorded (yes + date) – the ladder will skip automated calls and WhatsApp to the patient (device beep and nurse alert still work).';
      $('#cc-renew', els.care).hidden = !s.consent_ok;
    }
    $('#cc-read', els.care).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const r = await C.api.consentText(pid);
      const box = $('#cc-consent-text', els.care);
      box.hidden = false;
      box.innerHTML = `<b>Consent statement (${esc(LANGS[r.language] || r.language)}) – read aloud, then tick “Consent recorded” if the patient says yes:</b><div style="margin:.35rem 0">${esc(r.text)}</div><div class="small muted">Data kept: ${r.items.map(esc).join(' · ')} · valid ${esc(r.valid_days)} days · stop word: ${esc(r.stop_word)}</div>`;
      C.speak(r.text, r.language, { audioUrl: r.audio_url, interrupt: true });
    }).catch(() => {}));
    $('#cc-ask', els.care).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const r = await C.api.consentAsk(pid, 'patient');
      toast(r.sent ? 'Renewal question sent on WhatsApp' : 'Dry run – the renewal question is in the patient\'s WhatsApp (Demo page)', r.sent ? 'good' : '', 6000);
    }).catch(() => {}));
    $('#cc-renew', els.care).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const s = await C.api.putCare(pid, { renew_consent: true });
      consentNote(s.settings); toast('Consent date updated to today', 'good');
    }).catch(() => {}));
    function renderGuardians(gs) {
      $('#cc-guardians', els.care).innerHTML = gs.length ? gs.map((g) => `<div class="guardian-row" data-id="${g.id}">
        <div class="who"><b>${esc(g.name)}</b> <span class="muted">· ${esc(g.relation || 'family')}${g.city ? ' · ' + esc(g.city) : ''}</span>${g.is_primary ? ' <span class="chip ok">primary</span>' : ''}
          <div class="small muted">${esc(g.phone || 'no phone')} · ${esc(LANGS[g.language] || g.language)} · ${esc(CH[g.channel] || g.channel)}${g.quiet_start ? ` · quiet ${esc(g.quiet_start)}–${esc(g.quiet_end)}` : ''} · calls the patient “${esc(g.calls_patient || '')}” · ${g.consent_ok ? `✓ consent ${esc(new Date(g.consent_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }))}${g.consent_renew_due ? ' (re-confirm: over 7 days)' : ''}` : '⚠ no consent'}</div></div>
        <a class="btn sm" href="${esc(SB.ui.link(g.link))}" target="_blank" rel="noopener" title="Magic link – no login">Family page ↗</a>
        <button class="btn sm" data-g="copy" type="button">Copy link</button>
        <select class="sm-select" data-g="channel" aria-label="How to reach ${esc(g.name)}">${Object.entries(CH).map(([k, v]) => `<option value="${k}" ${k === g.channel ? 'selected' : ''}>${v}</option>`).join('')}</select>
        ${g.is_primary ? '' : '<button class="btn sm" data-g="primary" type="button">Make primary</button>'}
        ${g.consent_ok && g.consent_renew_due ? '<button class="btn sm" data-g="renew" type="button">↻ Re-confirm consent</button>' : ''}<button class="btn sm" data-g="consent" type="button">${g.consent_ok ? 'Withdraw consent' : 'Record consent'}</button>
        <button class="btn sm danger" data-g="del" type="button" aria-label="Remove ${esc(g.name)}">✕</button></div>`).join('') : '<div class="muted">No family members yet.</div>';
    }
    $('#cc-guardians', els.care).addEventListener('click', (e) => {
      const b = e.target.closest('button[data-g]'); if (!b) return;
      const row = b.closest('[data-id]'); const id = row.dataset.id;
      const g = data.guardians.find((x) => String(x.id) === id);
      if (b.dataset.g === 'copy') {
        const url = new URL(g.link, location.href).href;
        (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(() => toast('Link copied – send it to ' + g.name, 'good')).catch(() => prompt('Copy this link', url));
        return;
      }
      if (b.dataset.g === 'del' && !confirm(`Remove ${g.name} from the care circle?`)) return;
      busy(b, async () => {
        if (b.dataset.g === 'del') await C.api.delGuardian(id);
        if (b.dataset.g === 'primary') await C.api.editGuardian(id, { is_primary: true });
        if (b.dataset.g === 'consent') await C.api.editGuardian(id, { consent: !g.consent_ok });
        if (b.dataset.g === 'renew') await C.api.editGuardian(id, { consent: true });
        toast('Saved', 'good'); await refresh(true);
      }).catch(() => {});
    });
    $('#cc-guardians', els.care).addEventListener('change', (e) => {
      const s = e.target.closest('select[data-g="channel"]'); if (!s) return;
      C.api.editGuardian(s.closest('[data-id]').dataset.id, { channel: s.value }).then(() => { toast('Saved', 'good'); refresh(true); }).catch((err) => toast(err.message, 'bad'));
    });
    $('#cc-save', els.care).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const steps = $$('#cc-steps label', els.care).map((l) => ({ key: l.dataset.key, enabled: l.querySelector('input[type=checkbox]').checked, delay_min: Number(l.querySelector('input[type=number]').value) || 0 }));
      const s = await C.api.putCare(pid, { patient_phone: $('#cc-phone', els.care).value.trim() || null, quiet_start: $('#cc-qs', els.care).value, quiet_end: $('#cc-qe', els.care).value, trigger_missed: Number($('#cc-trig', els.care).value), auto: $('#cc-auto', els.care).checked, call_style: $('#cc-style', els.care).value, consent: $('#cc-consent', els.care).checked, steps });
      fillCare(s.settings); consentNote(s.settings); toast('Settings saved', 'good');
    }).catch(() => {}));
    $('#cc-add', els.care).addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = e.currentTarget.querySelector('button[type=submit]');
      busy(btn, async () => {
        await C.api.addGuardian({ patient_id: pid, name: $('#ga-name', els.care).value.trim(), relation: $('#ga-rel', els.care).value, phone: $('#ga-phone', els.care).value.trim(), language: $('#ga-lang', els.care).value, channel: $('#ga-ch', els.care).value, consent: $('#ga-consent', els.care).checked });
        e.target.reset(); toast('Family member added', 'good'); await refresh(true);
      }).catch(() => {});
    });
    function sendRes(r, what) {
      $('#cc-send-res', els.care).innerHTML = `<div class="drybox${r.sent ? ' sent' : ''}"><div class="t">${r.sent ? '✅ Sent on WhatsApp' : r.dry_run ? `DRY RUN – would send the ${what}` : '✖ Not sent'}${r.hint ? ' – ' + esc(r.hint) : ''}</div>${r.image_url ? `<img src="${esc(r.image_url)}" alt="Weekly progress card" style="max-width:260px;width:100%;border-radius:8px;display:block;margin:.4rem 0">` : ''}<div style="white-space:pre-wrap">${esc(r.text || '')}</div>${r.note ? `<div class="small muted">${esc(r.note)}</div>` : ''}</div>`;
    }
    $('#cc-card', els.care).addEventListener('click', (e) => busy(e.currentTarget, async () => sendRes(await C.api.weeklyCard(pid, 'family'), 'weekly card')).catch(() => {}));
    $('#cc-voice', els.care).addEventListener('click', (e) => busy(e.currentTarget, async () => {
      const r = await C.api.voiceNote(pid, 'family');
      sendRes(r, 'voice note');
      C.speak(r.speak_text, r.language, { audioUrl: r.audio_url, interrupt: true });
    }).catch(() => {}));

    /* ---------- refresh ---------- */
    function renderAlerts(list) {
      $('#cp-alerts', els.actions).innerHTML = list.length ? list.map((a) => `<li class="alert-item sev-${esc(a.severity)} st-${esc(a.status)}" data-id="${a.id}">
        <div class="alert-main"><div class="alert-top"><span class="sev sev-${esc(a.severity)}">${esc(C.SEV_TEXT[a.severity] || a.severity)}</span><span class="tag">${esc(a.kind_label)}</span>${a.status !== 'open' ? `<span class="tag dry">${esc(a.status)}</span>` : ''}${a.assigned_to ? `<span class="chip">👤 ${esc(a.assigned_to)}</span>` : ''}<span class="muted small" style="margin-left:auto">${esc(ago(a.created_at))}</span></div>
        <div class="alert-title">${esc(a.title)}</div>${a.detail ? `<div class="small muted" style="white-space:pre-wrap">${esc(a.detail)}</div>` : ''}</div>
        <div class="alert-actions">${a.status === 'open' ? `<button class="btn sm primary" data-act="ack" type="button">${ic('check', { size: 14 })}Acknowledge</button>` : ''}<button class="btn sm" data-act="assign" type="button">${ic('user-check', { size: 14 })}Assign to me</button><button class="btn sm good" data-act="resolve" type="button">${ic('check-circle', { size: 14 })}Resolve</button></div></li>`).join('')
        : `<li class="empty">${ic('check-circle', { size: 24 })}<b>No open alerts</b>Nothing needs action for this patient.</li>`;
    }
    async function refresh(forceCare) {
      if (SB.api.state.mock) { [els.actions, els.ladder, els.care].forEach((el) => { if (!el.dataset.mockNote) { el.dataset.mockNote = 1; el.insertAdjacentHTML('afterbegin', '<div class="banner mock" style="margin:0 0 .5rem">Needs the live server – not available in mock mode.</div>'); } }); return; }
      const [d, tl, st] = await Promise.all([C.api.patient(pid), C.api.timeline(pid, 60), refresh.status ? Promise.resolve(refresh.status) : C.api.status().catch(() => null)]);
      refresh.status = st;
      data = d;
      if (st) $('#cp-provider', els.actions).textContent = `Calls: ${st.calls_provider === 'dry_run' ? 'dry run (simulator)' : st.calls_provider} · AI check-in: ${st.checkin_provider === 'sarvam_agent' ? 'Sarvam' : 'simulator'}`;
      const cr = (d.calls || []).filter((c) => c.result).map(C.callResult).join('');
      if (cr !== refresh.csig) { refresh.csig = cr; $('#cp-calls', els.actions).innerHTML = cr || '<li class="muted" style="border:0;background:none;padding:0">No AI check-in calls yet.</li>'; }
      const tr = d.trend;
      $('#cp-trend', els.actions).innerHTML = tr && tr.flag ? `<div class="observation"><b>📉 Lower than usual (observation)</b><br>${esc(tr.text)}</div>`
        : tr && tr.avg3 ? `<div class="muted small">Today's best vs own 3-day average (${Number(tr.avg3).toLocaleString('en-IN')} mL): ${tr.pct_below ? tr.pct_below + '% lower' : 'not lower'} – no flag.</div>` : '';
      const sig = JSON.stringify(d.alerts);
      if (sig !== refresh.asig && !els.actions.querySelector('.busy')) { refresh.asig = sig; renderAlerts(d.alerts); }
      const run = d.active_run || (d.runs && d.runs[0]);
      $('#lad-run', els.ladder).innerHTML = run ? `<div class="row">${C.runSummary(run)}<span class="muted small">${esc(run.reason === 'demo' ? 'demo fast-forward' : run.reason)} · started ${esc(SB.ui.dateTimeLabel(run.created_at))}</span></div>${C.stepper(run)}` : '<div class="muted">No ladder yet. It starts by itself after missed sessions.</div>';
      $('#lad-next', els.ladder).hidden = !d.active_run;
      $('#lad-stop', els.ladder).hidden = !d.active_run;
      const ids = new Set(tl.map((e) => e.id));
      const tsig = tl.map((e) => e.id).join(',');
      if (tsig !== refresh.tsig) {
        refresh.tsig = tsig;
        $('#lad-tl', els.ladder).innerHTML = tl.length ? tl.map((e) => C.eventRow(e)).join('') : '<li class="muted">No events yet.</li>';
        if (lastEventIds) $$('#lad-tl .tl-item', els.ladder).forEach((li) => { if (!lastEventIds.has(Number(li.dataset.id))) li.classList.add('new'); });
        lastEventIds = ids;
      }
      if (!careFilled || forceCare) { fillCare(d.settings); }
      consentNote(d.settings);
      const gsig = JSON.stringify(d.guardians);
      if (gsig !== refresh.gsig) { refresh.gsig = gsig; renderGuardians(d.guardians); document.dispatchEvent(new CustomEvent('sb:care-data', { detail: { guardians: d.guardians } })); }
      const lang = (d.guardians[0] && d.guardians[0].language) === 'hi' ? 'hi' : 'en';
      $('#cc-card-view', els.care).href = `/api/comms/card/${pid}.png?lang=${lang}`;
    }
    SB.ui.poll(() => refresh(false), 3000);
  }

  SB.commsPatient = { mount };
})();
