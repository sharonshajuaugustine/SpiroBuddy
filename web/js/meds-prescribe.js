/* SpiroBuddy - the doctor's prescription page (prescribe.html?id=<patient id>).
 * The doctor types the medicines; "Send to the patient's phone" issues the prescription (saving is the
 * doctor's sign-off). Nothing here reads a photo or asks an AI. The server decides what gets a reminder:
 * a line with a clear schedule does, "only when needed" and unclear lines do not.
 */
(function () {
  'use strict';
  const M = SB.meds, esc = SB.ui.esc;
  if (SB.icons && !SB.icons.plus) SB.icons.plus = '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>';
  const ic = (n, o) => SB.icon(n, o);
  const $ = (s, r) => (r || document).querySelector(s);
  const pid = Number(new URLSearchParams(location.search).get('id')) || 0;

  let patient = null, meds = null, role = null, rowSeq = 0, replacing = null, preLang = 'en', lastRx = null;

  const FORMS = [['tablet', 'Tablet'], ['capsule', 'Capsule'], ['syrup', 'Syrup'], ['drops', 'Drops'], ['injection', 'Injection'], ['inhaler', 'Inhaler'], ['cream', 'Cream or ointment'], ['other', 'Other']];
  const UNITS = [['tablet', 'tablet'], ['capsule', 'capsule'], ['ml', 'ml'], ['drop', 'drop'], ['puff', 'puff'], ['unit', 'unit'], ['sachet', 'sachet']];
  const FORM_UNIT = { tablet: 'tablet', capsule: 'capsule', syrup: 'ml', drops: 'drop', inhaler: 'puff', injection: 'ml' };
  const FOODS = [['after_food', 'After food'], ['before_food', 'Before food'], ['with_food', 'With food'], ['any', 'Any time']];
  const SLOTS = [['morning', 'Morning', 'sun'], ['afternoon', 'Afternoon', 'sun'], ['night', 'Night', 'moon']];

  /* a small copy of the server's reading of "1-0-1", "BD" ... only to show a hint; the server decides */
  const WORDS = { od: '1-0-0', qd: '1-0-0', 'once daily': '1-0-0', daily: '1-0-0', bd: '1-0-1', bid: '1-0-1', 'twice daily': '1-0-1', tds: '1-1-1', tid: '1-1-1', 'three times daily': '1-1-1', qid: 'QID', qds: 'QID', hs: 'HS', bedtime: 'HS', night: '0-0-1', 'at night': '0-0-1', morning: '1-0-0', afternoon: '0-1-0' };
  const ASNEED = ['sos', 'prn', 'if needed', 'as needed', 'when needed', 'only when needed', 'if required', 'as required'];
  function hintFor(text) {
    const s = String(text || '').toLowerCase().replace(/\./g, '').replace(/\s+/g, ' ').trim();
    if (!s) return null;
    if (ASNEED.indexOf(s) >= 0) return { ok: true, text: 'Only when needed - never scheduled, no reminder.' };
    if (s === 'stat') return { ok: false, text: 'STAT - ask the clinician. No reminder is set.' };
    let code = WORDS[s];
    const m = /^([01]) ?- ?([01]) ?- ?([01])(?: ?- ?([01]))?$/.exec(s);
    if (m) code = m[4] === '1' && m[1] + m[2] + m[3] === '111' ? 'QID' : (m[4] != null ? null : m[1] + '-' + m[2] + '-' + m[3]);
    if (!code || code === '0-0-0') return { ok: false, text: 'Not recognised - the patient will see it as typed, with no reminder.' };
    if (code === 'QID') return { ok: true, text: 'Four times a day: 8:00 AM, 12:00 PM, 4:00 PM, 8:00 PM.' };
    if (code === 'HS') return { ok: true, text: 'At bedtime (10:00 PM unless the patient set another time).' };
    const names = code.split('-').map((d, i) => (d === '1' ? ['morning', 'afternoon', 'night'][i] : null)).filter(Boolean);
    return { ok: true, text: 'Reminder: ' + names.join(' and ') + '.' };
  }

  /* ---------------------------------------------------------------- the form */
  function opts(list, sel) { return list.map(([v, t]) => `<option value="${esc(v)}"${v === sel ? ' selected' : ''}>${esc(t)}</option>`).join(''); }

  function rowHTML(n, v) {
    v = v || {};
    const id = ++rowSeq;
    const unit = v.dose_unit || FORM_UNIT[v.form || 'tablet'] || 'tablet';
    const unitOpts = UNITS.some(([u]) => u === unit) ? UNITS : UNITS.concat([[unit, unit]]);
    return `<fieldset class="rx-row" data-row="${id}">
      <div class="rx-row-head"><b>Medicine <span data-n>${n}</span></b><button type="button" class="btn sm ghost" data-remove aria-label="Remove this medicine">${ic('x', { size: 16 })}Remove</button></div>
      <div class="form-grid">
        <label class="field"><span class="lbl">Medicine name</span><input data-f="drug_name" maxlength="120" autocomplete="off" required value="${esc(v.drug_name || '')}"></label>
        <label class="field"><span class="lbl">Strength</span><input data-f="strength" maxlength="40" autocomplete="off" placeholder="for example 500 mg" value="${esc(v.strength || '')}"></label>
        <label class="field"><span class="lbl">Form</span><select data-f="form">${opts(FORMS, v.form || 'tablet')}</select></label>
        <div class="field"><span class="lbl">Dose each time</span><div class="rx-dose"><input data-f="dose_qty" inputmode="decimal" aria-label="Amount" value="${esc(v.dose_qty != null ? M.qtyText(v.dose_qty) : '1')}"><select data-f="dose_unit" aria-label="Unit">${opts(unitOpts, unit)}</select></div></div>
      </div>
      <div class="field rx-when" style="margin-top:var(--sp-3)"><span class="lbl">When to take it</span>
        <div class="rx-chips" role="group" aria-label="Times of day">${SLOTS.map(([s, t, i]) => `<button type="button" class="rx-chip" data-slot="${s}" aria-pressed="${(v.chips || []).indexOf(s) >= 0}">${ic(i, { size: 18 })}${t}</button>`).join('')}</div>
        <label class="field"><span class="hint">or type a code: 1-0-1, 1-1-1, 0-0-1, OD, BD, TDS, QID, HS, SOS</span><input data-f="frequency" maxlength="60" autocomplete="off" value="${esc(v.code || '')}"></label>
        <p class="rx-hint" data-hint aria-live="polite"></p></div>
      <div class="form-grid" style="margin-top:var(--sp-3)">
        <label class="field"><span class="lbl">With food</span><select data-f="food_timing">${opts(FOODS, v.food_timing || 'after_food')}</select></label>
        <div class="field"><span class="lbl">For how long</span><div class="rx-dose" style="grid-template-columns:110px auto"><input data-f="duration_days" type="number" min="1" max="365" inputmode="numeric" aria-label="Number of days" placeholder="days" value="${v.duration_days || ''}"><label style="display:inline-flex;align-items:center;gap:var(--sp-2);min-height:var(--target);font-weight:600"><input type="checkbox" data-f="until_stopped"${v.until_stopped ? ' checked' : ''}>Until stopped</label></div></div>
      </div>
      <div class="rx-checks"><label><input type="checkbox" data-f="as_needed"${v.as_needed ? ' checked' : ''}>Only when needed (SOS) - no reminder</label></div>
      <label class="field" style="margin-top:var(--sp-3)"><span class="lbl">Note for the patient (optional)</span><input data-f="instructions" maxlength="300" autocomplete="off" value="${esc(v.instructions || '')}"></label>
    </fieldset>`;
  }

  function renumber() {
    const rows = document.querySelectorAll('#rows .rx-row');
    rows.forEach((r, i) => { r.querySelector('[data-n]').textContent = i + 1; r.querySelector('[data-remove]').hidden = rows.length === 1; });
  }
  function addRow(v) {
    const n = document.querySelectorAll('#rows .rx-row').length + 1;
    $('#rows').insertAdjacentHTML('beforeend', rowHTML(n, v));
    const row = $('#rows').lastElementChild;
    syncRow(row); renumber();
    return row;
  }
  const val = (row, f) => { const el = row.querySelector(`[data-f="${f}"]`); return el ? (el.type === 'checkbox' ? el.checked : el.value.trim()) : ''; };

  /* keep the row consistent: chips beat the code box; "only when needed" and "until stopped" switch things off */
  function syncRow(row) {
    const chips = [...row.querySelectorAll('[data-slot][aria-pressed="true"]')].map((b) => b.dataset.slot);
    const sos = val(row, 'as_needed'), until = val(row, 'until_stopped');
    row.querySelectorAll('[data-slot]').forEach((b) => { b.disabled = sos; });
    row.querySelector('[data-f="frequency"]').disabled = sos || chips.length > 0;
    row.querySelector('[data-f="duration_days"]').disabled = sos || until;
    row.querySelector('[data-f="until_stopped"]').disabled = sos;
    const hint = row.querySelector('[data-hint]');
    let h = null;
    if (sos) h = { ok: true, text: 'Only when needed - the patient sees it, but no reminder is ever set.' };
    else if (chips.length) h = { ok: true, text: 'Reminder: ' + chips.join(' and ') + '.' };
    else h = hintFor(val(row, 'frequency'));
    hint.className = 'rx-hint' + (h && !h.ok ? ' warn' : '');
    hint.innerHTML = h ? ic(h.ok ? 'info' : 'alert-triangle', { size: 16 }) + '<span>' + esc(h.text) + '</span>' : '';
  }

  function collect() {
    const rows = [...document.querySelectorAll('#rows .rx-row')], lines = [], errs = [];
    rows.forEach((row, i) => {
      const n = i + 1, sos = val(row, 'as_needed');
      const chips = [...row.querySelectorAll('[data-slot][aria-pressed="true"]')].map((b) => b.dataset.slot);
      const l = { drug_name: val(row, 'drug_name'), strength: val(row, 'strength'), form: val(row, 'form'), dose_qty: val(row, 'dose_qty'), dose_unit: val(row, 'dose_unit'), food_timing: val(row, 'food_timing'), instructions: val(row, 'instructions'), as_needed: sos };
      if (!l.drug_name) errs.push(`Medicine ${n}: type the name.`);
      if (!(parseFloat(String(l.dose_qty).replace('½', '.5')) > 0) && !/^\d+\s*\/\s*\d+$/.test(l.dose_qty)) errs.push(`Medicine ${n}: the dose each time must be a number above 0.`);
      if (sos) { l.frequency_raw = 'SOS'; }
      else {
        if (chips.length) l.slots = chips; else if (val(row, 'frequency')) l.frequency_raw = val(row, 'frequency');
        else errs.push(`Medicine ${n}: choose when to take it, or tick "Only when needed".`);
        if (val(row, 'until_stopped')) l.until_stopped = true;
        else if (val(row, 'duration_days')) l.duration_days = Number(val(row, 'duration_days'));
        else errs.push(`Medicine ${n}: give the number of days, or tick "Until stopped".`);
      }
      lines.push(l);
    });
    return { lines, errs };
  }

  /* ---------------------------------------------------------------- showing what exists */
  function lineLi(l) {
    const flag = (l.unclear_fields || []).length ? `<div class="rx-unclear">${ic('alert-triangle', { size: 14 })} Check: ${esc((l.unclear_fields || []).join(', ').replace('food_timing', 'food instruction'))} - no reminder where this is unclear</div>` : '';
    return `<li>${ic('pill', { size: 18 })}<div><b>${esc(l.drug_name)}</b>${l.strength ? ' ' + esc(l.strength) : ''}<div class="rx-sum">${esc(M.summary(l))}</div>${l.instructions ? `<div class="rx-sum">Note: ${esc(l.instructions)}</div>` : ''}${flag}</div></li>`;
  }
  const dmy = (v) => (v ? SB.ui.dmy(v) : '-');

  function paintPatient() {
    const p = patient;
    $('#h-title').textContent = 'Medicines for ' + (p.name || 'patient');
    $('#back-patient').href = 'patient.html?id=' + pid;
    $('#back-patient').textContent = p.name || 'Patient';
    document.title = 'Medicines · ' + (p.name || 'patient') + ' · SpiroBuddy';
    $('#p-card').innerHTML = `<div class="rx-who"><span class="avatar" aria-hidden="true" style="width:44px;height:44px;border-radius:50%;background:var(--brand-soft);color:var(--brand);display:grid;place-items:center;font-weight:700">${esc(SB.ui.initials(p.name))}</span>
      <div><b>${esc(p.name)}</b><div class="subtle" style="color:var(--text-2)">${esc(p.age)} years · ${esc(p.sex || '')} · ${esc(p.surgery || '')}</div></div>
      <a class="btn sm" href="patient.html?id=${pid}" style="margin-left:auto">${ic('user', { size: 16 })}Open chart</a></div>`;
  }

  function paintCurrent() {
    const cur = meds.current || [];
    const can = role === 'doctor';
    $('#cur').innerHTML = cur.length ? cur.map((rx) => `<div class="rx-cur">
        <div class="rx-cur-head"><b>Prescription of ${esc(dmy(rx.issued_on))}</b><span class="chip ok"><span class="dot"></span>${esc(rx.state_text)}</span><span class="subtle" style="color:var(--text-2)">${esc(rx.doctor.name || '')}${rx.version > 1 ? ' · version ' + rx.version : ''}</span><span class="spacer"></span>
          ${can ? `<button class="btn sm" type="button" data-change="${rx.id}">${ic('edit', { size: 16 })}Change</button><button class="btn sm danger" type="button" data-stop="${rx.id}">${ic('stop', { size: 16 })}Stop</button>` : ''}</div>
        <ul class="rx-lines">${rx.lines.map(lineLi).join('')}</ul></div>`).join('')
      : `<div class="empty">${ic('pill', { size: 28 })}<b>No current prescription</b>${can ? 'Write one on this page and send it to the phone.' : 'A doctor has not sent one yet.'}</div>`;
    const hist = (meds.history || []).filter((h) => h.state !== 'current');
    $('#hist').innerHTML = hist.length ? hist.map((rx) => `<div class="rx-cur"><div class="rx-cur-head"><b>Prescription of ${esc(dmy(rx.issued_on))}</b><span class="chip"><span class="dot"></span>${esc(rx.state_text)}</span><span class="subtle" style="color:var(--text-2)">${esc(rx.doctor.name || '')}</span></div>
        <ul class="rx-lines">${rx.lines.map(lineLi).join('')}</ul></div>`).join('') : '<p class="subtle" style="color:var(--text-2)">Nothing stopped or replaced yet.</p>';
    // the "this prescription" choice
    const sel = $('#replaces');
    sel.innerHTML = '<option value="">A new prescription (keep the current ones)</option>' +
      cur.map((rx) => `<option value="${rx.id}">Replace the prescription of ${esc(dmy(rx.issued_on))}</option>`).join('');
    sel.value = replacing && cur.some((r) => r.id === replacing) ? String(replacing) : '';
    $('#replace-wrap').hidden = !cur.length;
  }

  function paintBanner() {
    const rx = replacing && (meds.current || []).find((r) => r.id === replacing);
    $('#rx-banner').innerHTML = rx ? `<div class="form-msg info">${ic('info', { size: 18 })}<span>You are changing the prescription of ${esc(dmy(rx.issued_on))}. Sending replaces it; the old one stays in the history.
      <button class="btn sm ghost" type="button" id="cancel-change" style="margin-left:8px">Cancel the change</button></span></div>` : '';
  }

  async function reload() {
    meds = await SB.api.get(`/api/patients/${pid}/medicines`);
    paintCurrent(); paintBanner();
  }

  /* ---------------------------------------------------------------- preview of what the patient sees */
  function paintPreview() {
    if (!lastRx) return;
    $('#pre-lang').innerHTML = M.LANGS.map((c) => `<button type="button" class="btn sm${c === preLang ? ' primary' : ''}" data-pl="${c}" lang="${c}" aria-pressed="${c === preLang}">${esc(M.NATIVE[c])}</button>`).join('');
    $('#pre').innerHTML = `<p style="margin:0 0 var(--sp-3);font-weight:700">${esc(M.tr(preLang, 'issued', { d: lastRx.doctor.name || '', date: M.dateText(lastRx.issued_on, preLang) }))}</p>` +
      lastRx.lines.map((l) => M.medCard(l, preLang)).join('');
  }

  /* ---------------------------------------------------------------- sending */
  function confirmText(lines) {
    const rx = replacing && (meds.current || []).find((r) => r.id === replacing);
    const noRem = lines.filter((l) => !l.as_needed && !l.slots && !hintOk(l.frequency_raw)).length;
    return `<p style="margin-top:0">${lines.length === 1 ? '1 medicine' : lines.length + ' medicines'} will appear on <b>${esc(patient.name)}</b>'s phone at once.</p>
      <ul class="rx-lines" style="margin-bottom:var(--sp-3)">${lines.map((l) => `<li>${ic('pill', { size: 16 })}<span><b>${esc(l.drug_name)}</b> ${esc(l.strength || '')}</span></li>`).join('')}</ul>
      ${rx ? `<p>It replaces the prescription of ${esc(dmy(rx.issued_on))}, which stays in the history.</p>` : ''}
      ${noRem ? `<div class="form-msg info">${ic('alert-triangle', { size: 18 })}<span>${noRem} line${noRem > 1 ? 's' : ''} will be shown without a reminder because the schedule was not recognised.</span></div>` : ''}`;
  }
  const hintOk = (t) => { const h = hintFor(t); return !h || h.ok; };

  let pending = null;
  function ask() {
    $('#form-err').innerHTML = '';
    const { lines, errs } = collect();
    if (errs.length) {
      $('#form-err').innerHTML = `<div class="form-msg bad">${ic('alert-triangle', { size: 18 })}<span>${errs.map(esc).join('<br>')}</span></div>`;
      return;
    }
    pending = lines;
    $('#send-body').innerHTML = confirmText(lines);
    $('#send-dlg').showModal();
  }

  async function send() {
    const body = { lines: pending };
    const rep = $('#replaces').value;
    if (rep) body.replaces = Number(rep);
    const btn = $('#send-ok');
    try {
      const r = await SB.ui.busy(btn, () => SB.api.post(`/api/patients/${pid}/prescriptions`, body));
      $('#send-dlg').close();
      lastRx = r.prescription;
      $('#pre-card').classList.remove('hidden');
      $('#pre-warn').innerHTML = (r.warnings || []).length ? `<div class="form-msg info" style="margin-bottom:var(--sp-3)">${ic('alert-triangle', { size: 18 })}<span>${r.warnings.map((w) => esc(w.text)).join('<br>')}</span></div>` : '';
      preLang = M.T[patient.language] ? patient.language : 'en';
      paintPreview();
      SB.ui.toast('Sent to ' + (patient.name || 'the patient') + "'s phone", 'good');
      replacing = null; $('#rows').innerHTML = ''; addRow();
      await reload();
      $('#pre-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {
      $('#send-dlg').close();
      $('#form-err').innerHTML = `<div class="form-msg bad">${ic('alert-triangle', { size: 18 })}<span>${esc((e && e.message) || 'Could not send. Please try again.')}</span></div>`;
    }
  }

  /* ---------------------------------------------------------------- change / stop */
  function startChange(id) {
    const rx = (meds.current || []).find((r) => r.id === id);
    if (!rx) return;
    replacing = id;
    $('#rows').innerHTML = '';
    rx.lines.forEach((l) => {
      const code = /^[01]-[01]-[01]$/.test(l.frequency_code || '') ? null : (l.as_needed ? '' : l.frequency_raw || l.frequency_code || '');
      addRow({ drug_name: l.drug_name, strength: l.strength, form: l.form || 'tablet', dose_qty: l.dose_qty, dose_unit: l.dose_unit, food_timing: l.food_timing, duration_days: l.duration_days, until_stopped: l.until_stopped, as_needed: l.as_needed, instructions: l.instructions, chips: l.slots && ['morning', 'afternoon', 'night'].some((s) => l.slots.indexOf(s) >= 0) ? l.slots.filter((s) => s !== 'bedtime') : [], code: code === null ? '' : code });
    });
    paintCurrent(); paintBanner();
    $('#write-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  let stopId = null;
  function askStop(id) {
    const rx = (meds.current || []).find((r) => r.id === id);
    if (!rx) return;
    stopId = id;
    $('#stop-body').textContent = `The prescription of ${dmy(rx.issued_on)} (${rx.lines.length} ${rx.lines.length === 1 ? 'medicine' : 'medicines'}) will no longer show as current on the patient's phone, and its reminders end. It stays in the history.`;
    $('#stop-reason').value = '';
    $('#stop-dlg').showModal();
  }
  async function doStop() {
    const btn = $('#stop-ok');
    try {
      await SB.ui.busy(btn, () => SB.api.post(`/api/prescriptions/${stopId}/stop`, { reason: $('#stop-reason').value.trim() }));
      $('#stop-dlg').close();
      if (replacing === stopId) replacing = null;
      SB.ui.toast('Prescription stopped', 'good');
      await reload();
    } catch (_) { $('#stop-dlg').close(); }
  }

  /* ---------------------------------------------------------------- events */
  document.addEventListener('click', (e) => {
    const chip = e.target.closest('.rx-chip');
    if (chip) { chip.setAttribute('aria-pressed', chip.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); syncRow(chip.closest('.rx-row')); return; }
    if (e.target.closest('#add-row')) { const r = addRow(); r.querySelector('[data-f="drug_name"]').focus(); return; }
    const rm = e.target.closest('[data-remove]');
    if (rm) { rm.closest('.rx-row').remove(); renumber(); return; }
    const ch = e.target.closest('[data-change]'); if (ch) { startChange(Number(ch.dataset.change)); return; }
    const st = e.target.closest('[data-stop]'); if (st) { askStop(Number(st.dataset.stop)); return; }
    if (e.target.closest('#cancel-change')) { replacing = null; paintCurrent(); paintBanner(); return; }
    const pl = e.target.closest('[data-pl]'); if (pl) { preLang = pl.dataset.pl; paintPreview(); return; }
    if (e.target.closest('#send-cancel')) $('#send-dlg').close();
    if (e.target.closest('#send-ok')) send();
    if (e.target.closest('#stop-cancel')) $('#stop-dlg').close();
    if (e.target.closest('#stop-ok')) doStop();
  });
  document.addEventListener('input', (e) => { const row = e.target.closest && e.target.closest('.rx-row'); if (row) syncRow(row); });
  document.addEventListener('change', (e) => {
    const row = e.target.closest && e.target.closest('.rx-row');
    if (!row) return;
    if (e.target.matches('[data-f="form"]') && FORM_UNIT[e.target.value]) row.querySelector('[data-f="dose_unit"]').value = FORM_UNIT[e.target.value];
    syncRow(row);
  });
  $('#rx-form').addEventListener('submit', (e) => { e.preventDefault(); ask(); });
  $('#replaces').addEventListener('change', (e) => { replacing = e.target.value ? Number(e.target.value) : null; paintBanner(); });

  /* ---------------------------------------------------------------- start */
  (async function start() {
    await SB.ui.boot('patient');
    SB.ui.hydrateIcons(document);
    if (!pid) {
      $('#rx-top').innerHTML = '<div class="empty"><b>Open a patient from the list</b>Go to <a href="dashboard.html">Patients</a>, open a patient, then choose Medicines.</div>';
      return;
    }
    try {
      const me = await SB.auth.me();
      role = me && me.role;
      patient = await SB.api.patient(pid);
      paintPatient();
      if (role !== 'doctor') {
        $('#write-card').innerHTML = `<div class="empty">${ic('lock', { size: 28 })}<b>Only doctors write prescriptions</b>You can see the medicines and the history. Ask the patient's doctor to write or change a prescription.</div>`;
      } else addRow();
      await reload();
    } catch (e) {
      $('#p-msg').innerHTML = `<div class="form-msg bad" role="alert">${ic('alert-triangle', { size: 18 })}<span>${esc((e && e.status === 404) ? 'This patient was not found, or is not one of your patients.' : ((e && e.message) || 'Could not load this page.'))}</span></div>`;
      $('#rx-top').classList.add('hidden');
    }
  })();
})();
