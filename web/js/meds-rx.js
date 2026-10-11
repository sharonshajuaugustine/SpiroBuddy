/* SpiroBuddy - the pharmacist's check page (rx.html?t=<token>). No login.
 * Shows the hospital's copy of the prescription and whether it is still current. Minimal data: given name
 * and initial, age, hospital, doctor, date, medicines. A stopped or replaced prescription shows no medicines.
 */
(function () {
  'use strict';
  const esc = SB.meds.esc, ic = (n, o) => SB.icon(n, o);
  const main = document.getElementById('rxp-main');
  const token = new URLSearchParams(location.search).get('t') || '';
  const SEX = { M: 'Male', F: 'Female', O: 'Other' };
  const dmy = (v) => (v && SB.ui.dmy ? SB.ui.dmy(v) : '-');

  function show(d) {
    const good = d.current;
    const p = d.patient || {};
    main.innerHTML = `<div class="rxp-state ${good ? 'good' : 'bad'}">${ic(good ? 'check-circle' : 'x-circle', { size: 34 })}<span>${esc(good ? 'Current' : 'No longer current')}<br><small style="font-weight:600;font-size:1.05rem">${esc(d.state_text)}</small></span></div>
      <dl class="rxp-grid">
        <div><dt>Hospital</dt><dd>${esc((d.hospital || {}).name || '')}${(d.hospital || {}).city ? `<br><small>${esc(d.hospital.city)}</small>` : ''}</dd></div>
        <div><dt>Issued on</dt><dd>${esc(dmy(d.issued_on))}</dd></div>
        <div><dt>Doctor</dt><dd>${esc((d.doctor || {}).name || '')}</dd></div>
        <div><dt>Registration number <small>(display only)</small></dt><dd>${esc((d.doctor || {}).reg_no_display || 'Not recorded')}</dd></div>
        <div><dt>Patient</dt><dd>${esc(p.name || '')}${p.age != null ? ', ' + esc(p.age) + ' years' : ''}${p.sex ? ', ' + esc(SEX[p.sex] || p.sex) : ''}</dd></div>
      </dl>
      ${good ? `<ol class="rxp-meds" style="list-style:none">${(d.lines || []).map((l, i) => `<li><div class="rxp-n">${i + 1}. ${esc(l.drug_name)}${l.strength ? ' ' + esc(l.strength) : ''}${l.as_needed ? ' <span class="chip">Only when needed</span>' : ''}</div>
        <div class="rxp-how">${esc(l.summary || '')}</div>${l.instructions ? `<div class="rxp-how">Note: ${esc(l.instructions)}</div>` : ''}</li>`).join('')}</ol>` : ''}
      <p class="rxp-note">${ic('info', { size: 18 })} ${esc(d.notice || "Compare with the patient's screen.")}</p>
      <p style="color:var(--text-3);font-size:var(--fs-sm)">Checked ${esc(SB.ui.dateTimeLabel ? SB.ui.dateTimeLabel(d.checked_at) : d.checked_at)}.</p>`;
  }

  function fail(status) {
    const msg = status === 429 ? 'Too many tries from this device. Please wait a few minutes and try again.'
      : status === 404 ? 'This code is not valid. It may be mistyped, or from another system. Please ask the patient to show the screen again.'
        : 'Could not reach the hospital copy. Please check the internet and try again.';
    main.innerHTML = `<div class="rxp-state bad" role="alert">${ic('x-circle', { size: 34 })}<span>${esc(msg)}</span></div>`;
  }

  (async function start() {
    try { await SB.api.init(); } catch (_) { /* a failed read shows the message below */ }
    try { SB.ui.loadFeatures(); SB.ui.fakeRibbon({ into: '#rxp-ribbon' }); } catch (_) { /* optional */ }
    if (!token) { fail(404); return; }
    try { show(await SB.api.get('/api/rx-check/' + encodeURIComponent(token))); }
    catch (e) { fail(e && e.status); }
  })();
})();
