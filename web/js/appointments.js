/* SpiroBuddy - visits (appointments) for staff. This file does two jobs:
 *   1. SB.appt = the shared pieces of the two staff pages (status words, dates in India time, one visit row, the
 *      action buttons, the "another time" and reason dialogs, the free-time picker). doctor-day.js uses them too.
 *   2. The appointments.html page itself (list, filters, "Book a visit"). It starts only when the page body has
 *      data-ap-page="appointments".
 * What the server says is final: the buttons shown come from each visit's `can` flags, and every action is checked
 * again on the server. Times are India time (IST). No payments, no diagnosis, no real messages are sent from here.
 */
(function () {
  'use strict';
  const SB = (window.SB = window.SB || {});
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ic = (n, o) => (SB.icon ? SB.icon(n, Object.assign({ size: 22 }, o || {})) : '');
  const $ = (s, r) => (r || document).querySelector(s);
  const pad = (n) => String(n).padStart(2, '0');

  /* ---------------------------------------------------------------- status words (exactly these) */
  const STATE = {
    requested: { word: 'Requested', icon: 'hourglass', tone: 'warn' },
    proposed: { word: 'Alternative proposed', icon: 'refresh', tone: 'info' },
    confirmed: { word: 'Confirmed', icon: 'check-circle', tone: 'good' },
    declined: { word: 'Declined', icon: 'x-circle', tone: 'bad' },
    cancelled: { word: 'Cancelled', icon: 'x-circle', tone: 'muted' },
    attended: { word: 'Attended', icon: 'check', tone: 'good' },
    no_show: { word: 'No-show', icon: 'alert-triangle', tone: 'warn' },
  };
  const KIND = { follow_up: 'Follow-up', review: 'Review', other: 'Other' };
  const stateOf = (a) => STATE[a && a.state] || STATE.requested;
  const wordOf = (a) => (a && a.status_words) || stateOf(a).word;
  function stateBadge(a) {
    const s = stateOf(a);
    return `<span class="ap-state ap-t-${s.tone}">${ic(s.icon, { size: 20 })}<span>${esc(wordOf(a))}</span></span>`;
  }

  /* ---------------------------------------------------------------- dates and times (India time, no locale surprises) */
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  function ist(iso) {                       // -> {ymd, h, m} in India time, whatever zone the browser is in
    const t = new Date(iso).getTime();
    if (isNaN(t)) return null;
    const d = new Date(t + 330 * 60000);
    return { ymd: d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate()), h: d.getUTCHours(), m: d.getUTCMinutes() };
  }
  const todayYmd = () => ist(new Date().toISOString()).ymd;
  function addDays(ymd, n) { const d = new Date(ymd + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  const validYmd = (s) => /^\d{4}-\d{2}-\d{2}$/.test(String(s || '')) && !isNaN(new Date(s + 'T12:00:00Z'));
  function dateWords(ymd) {
    if (!validYmd(ymd)) return '';
    const d = new Date(ymd + 'T12:00:00Z');
    return DAYS[d.getUTCDay()] + ', ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()] + ' ' + d.getUTCFullYear();
  }
  function shortDate(ymd) {
    if (!validYmd(ymd)) return '';
    const d = new Date(ymd + 'T12:00:00Z');
    return DAYS[d.getUTCDay()].slice(0, 3) + ' ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()].slice(0, 3);
  }
  function timeWords(iso) {
    const p = ist(iso);
    return p ? (p.h % 12 || 12) + ':' + pad(p.m) + ' ' + (p.h < 12 ? 'AM' : 'PM') : '';
  }
  const whenWords = (a) => (a && a.when_words) || (a && a.start_at && ist(a.start_at) ? dateWords(ist(a.start_at).ymd) + ', ' + timeWords(a.start_at) : '');
  const isPast = (iso) => { const t = new Date(iso).getTime(); return !isNaN(t) && t < Date.now(); };

  /* ---------------------------------------------------------------- errors, in plain words */
  function msgOf(e, fallback) {
    if (e && e.status === 0) return 'Cannot reach the server. Please check the connection and try again.';
    const m = e && e.message ? String(e.message) : '';
    if (!m || /^HTTP \d+/.test(m) || /^[[{]/.test(m) || m === 'Not Found' || m === 'Internal Server Error') return fallback || 'Something went wrong. Please try again.';
    return m;
  }
  /* Shows a calm card in `host` for a failed page load. status: 401 login, 403 not allowed, 404/501 not there, else retry. */
  function problem(host, e, retry, what) {
    const st = e && e.status;
    let icon = 'alert-triangle', title, text, extra = '';
    if (st === 401) {
      icon = 'lock'; title = 'Please log in';
      text = 'Visits are shown only to logged-in hospital staff.';
      extra = `<a class="ap-btn primary" href="/login.html?next=${encodeURIComponent(location.pathname + location.search)}">${ic('log-in')}Log in</a>`;
    } else if (st === 403) {
      icon = 'lock'; title = 'You do not have access to this page yet';
      text = 'Your account is not set up to manage appointments. Please ask your hospital admin or the doctor who gave you your key to add the permission "Manage appointments".';
      extra = '<a class="ap-btn" href="/dashboard.html">Back to the patient list</a>';
    } else if (st === 404 || st === 501) {
      icon = 'info'; title = 'Visits are not available yet';
      text = 'This server does not have the ' + (what || 'visits') + ' service switched on yet. Nothing is broken on your side.';
      extra = retry ? `<button type="button" class="ap-btn" data-ap-retry>${ic('refresh')}Check again</button>` : '';
    } else {
      title = 'We could not load this page';
      text = msgOf(e, 'Please check the internet connection and try again.');
      extra = retry ? `<button type="button" class="ap-btn primary" data-ap-retry>${ic('refresh')}Try again</button>` : '';
    }
    host.innerHTML = `<div class="ap-empty" role="alert">${ic(icon, { size: 40 })}<b>${esc(title)}</b><p>${esc(text)}</p>${extra}</div>`;
    const b = $('[data-ap-retry]', host);
    if (b && retry) b.addEventListener('click', retry);
  }
  /* page has no staff login (the shell sets SB.ui.me to null) */
  function needLogin(host) { problem(host, { status: 401 }); }

  /* ---------------------------------------------------------------- dialogs (native <dialog>) */
  function modal(o) {
    return new Promise((resolve) => {
      const d = document.createElement('dialog');
      d.className = 'ap-dlg';
      d.setAttribute('aria-labelledby', 'ap-dlg-t');
      d.innerHTML = `<div class="dh"><h2 id="ap-dlg-t">${esc(o.title)}</h2></div><div class="db">${o.body || ''}</div><div class="df"></div>`;
      const foot = $('.df', d);
      let result = null;
      (o.buttons || []).forEach((b) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ap-btn' + (b.cls ? ' ' + b.cls : '');
        btn.innerHTML = (b.icon ? ic(b.icon) : '') + '<span>' + esc(b.label) + '</span>';
        if (b.id) btn.id = b.id;
        btn.addEventListener('click', async () => {
          if (btn.disabled) return;
          if (!b.run) { d.close(); return; }
          btn.classList.add('busy');
          try {
            const r = await b.run(d, btn);
            if (r && r.close) { result = r.value === undefined ? true : r.value; d.close(); }
          } finally { btn.classList.remove('busy'); }
        });
        foot.appendChild(btn);
      });
      d.addEventListener('close', () => { d.remove(); resolve(result); });
      document.body.appendChild(d);
      d.showModal();
      if (o.onOpen) o.onOpen(d);
    });
  }
  const askConfirm = (title, text, yes, cls) => modal({
    title, body: `<p style="margin:0">${esc(text)}</p>`,
    buttons: [{ label: 'No, keep it', value: false }, { label: yes, cls: cls || 'danger', run: () => ({ close: true, value: true }) }],
  }).then((v) => v === true);
  function askReason(a) {
    return modal({
      title: 'Decline this request?',
      body: `<p style="margin:0">${esc(a.patient_name || 'The patient')} asked for ${esc(whenWords(a))}. Please give a short reason. The patient will see it.</p>
        <div class="ap-field"><label for="ap-reason">Reason</label><textarea id="ap-reason" maxlength="300" placeholder="For example: I am on leave that day. Please ask for another day."></textarea></div>
        <p id="ap-reason-err" role="alert" class="ap-muted" style="margin:0;color:var(--red)" hidden>Please write a short reason.</p>`,
      buttons: [{ label: 'Go back', value: null },
        { label: 'Decline request', cls: 'danger', icon: 'x-circle', run: (d) => {
          const v = $('#ap-reason', d).value.trim();
          if (!v) { $('#ap-reason-err', d).hidden = false; $('#ap-reason', d).focus(); return null; }
          return { close: true, value: v };
        } }],
      onOpen: (d) => $('#ap-reason', d).focus(),
    });
  }

  /* ---------------------------------------------------------------- doctors (best effort, scoped by the server) */
  let docsP = null;
  function loadDoctors(me) {
    if (docsP) return docsP;
    docsP = (async () => {
      const m = new Map();
      const put = (id, name, dept) => {
        id = Number(id); if (!id) return;
        const cur = m.get(id);
        if (!cur) m.set(id, { id, name: name || ('Doctor ' + id), department: dept || '' });
        else if (name && /^Doctor \d+$/.test(cur.name)) cur.name = name;
      };
      let denied = false;
      if (me && me.role === 'doctor') put(me.id, me.name);
      // an admin gets every active doctor of the hospital; a doctor's own entry is above
      if (me && me.role === 'admin') {
        try { const r = await SB.api.get('/api/registration/options'); ((r && r.doctors) || []).forEach((d) => put(d.id, d.name, d.department)); } catch (_) { /* optional */ }
      }
      // everyone: the doctors who have visits (each visit carries the doctor's name). There is no "list of doctors"
      // route that a nurse may call, so for a nurse this is the best source (see the handoff note).
      try {
        const rows = await SB.api.get('/api/appointments');
        (Array.isArray(rows) ? rows : []).forEach((a) => put(a.doctor_id, a.doctor_name));
      } catch (e) { if (e && e.status === 403) denied = true; }
      const out = Array.from(m.values()).sort((a, b) => a.name.localeCompare(b.name));
      out.denied = denied;
      return out;
    })();
    return docsP;
  }
  const doctorOptions = (docs, sel, blank) => (blank ? `<option value="">${esc(blank)}</option>` : '') +
    docs.map((d) => `<option value="${d.id}"${String(sel) === String(d.id) ? ' selected' : ''}>${esc(d.name)}${d.department ? ' (' + esc(d.department) + ')' : ''}</option>`).join('');

  /* ---------------------------------------------------------------- free-time picker (a day, then big time buttons) */
  function slotPicker(host, o) {
    const id = 'sp' + Math.random().toString(36).slice(2, 7);
    const min = todayYmd(), max = addDays(min, 180);
    let date = o.date && validYmd(o.date) ? o.date : min, doctor = o.doctor || '', picked = null, seq = 0;
    host.innerHTML = `<div class="ap-field"><label for="${id}-d">Day</label><input type="date" id="${id}-d" min="${min}" max="${max}" value="${date}"></div>
      <div><p class="ap-sec-sub" id="${id}-w" style="margin:0 0 var(--sp-2)">${esc(dateWords(date))}</p>
      <div id="${id}-s" aria-live="polite"></div></div>`;
    const box = $('#' + id + '-s', host), words = $('#' + id + '-w', host), inp = $('#' + id + '-d', host);
    function say(html) { box.innerHTML = html; }
    async function load() {
      const my = ++seq;
      picked = null; o.onPick && o.onPick(null);
      words.textContent = dateWords(date);
      if (!doctor) { say('<p class="ap-muted" style="margin:0">Choose a doctor first.</p>'); return; }
      if (!validYmd(date) || date < min || date > max) { say('<p class="ap-muted" style="margin:0">Choose a day from today up to 180 days ahead.</p>'); return; }
      say('<span class="skeleton ap-skel"></span>');
      let slots;
      try { slots = await SB.api.get('/api/slots?doctor=' + encodeURIComponent(doctor) + '&date=' + encodeURIComponent(date)); }
      catch (e) { if (my === seq) say(`<div class="ap-note bad" role="alert">${ic('alert-triangle')}<span>${esc(msgOf(e, 'Could not load the free times.'))}</span></div>`); return; }
      if (my !== seq) return;
      slots = Array.isArray(slots) ? slots : [];
      if (!slots.length) { say(`<div class="ap-empty">${ic('calendar', { size: 32 })}<b>No free times on this day</b>Try another day.</div>`); return; }
      const loc = slots[0].location;
      say((loc ? `<p class="ap-muted" style="margin:0 0 var(--sp-2)">Place: ${esc(loc)}</p>` : '') +
        `<div class="ap-slots" role="group" aria-label="Free times">${slots.map((s) => `<button type="button" class="ap-slot" data-start="${esc(s.start_at)}" aria-pressed="false">${esc(timeWords(s.start_at))}</button>`).join('')}</div>`);
    }
    box.addEventListener('click', (e) => {
      const b = e.target.closest('.ap-slot'); if (!b) return;
      box.querySelectorAll('.ap-slot').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      picked = b.dataset.start;
      o.onPick && o.onPick(picked);
    });
    inp.addEventListener('change', () => { date = inp.value; load(); });
    load();
    return { setDoctor(v) { doctor = v || ''; load(); }, reload: load, value: () => picked, date: () => date };
  }

  function askAnotherTime(a, doctorId) {
    let picker = null, chosen = null;
    return modal({
      title: 'Suggest another time',
      body: `<p style="margin:0">${esc(a.patient_name || 'The patient')} asked for <b>${esc(whenWords(a))}</b>. Choose a free time to suggest. The patient will be asked to accept it.</p>
        <div id="ap-sp"></div><p class="ap-pickedtime" id="ap-picked" aria-live="polite" style="margin:0"></p>`,
      buttons: [{ label: 'Go back', value: null },
        { label: 'Suggest this time', cls: 'primary', icon: 'send', id: 'ap-dlg-ok', run: () => (chosen ? { close: true, value: chosen } : null) }],
      onOpen: (d) => {
        const ok = $('#ap-dlg-ok', d); ok.disabled = true;
        const start = ist(a.start_at);
        picker = slotPicker($('#ap-sp', d), {
          doctor: doctorId || a.doctor_id,
          date: start && start.ymd >= todayYmd() ? start.ymd : todayYmd(),
          onPick: (v) => { chosen = v; ok.disabled = !v; $('#ap-picked', d).textContent = v ? 'Suggested: ' + dateWords(ist(v).ymd) + ', ' + timeWords(v) : ''; },
        });
      },
    });
  }

  /* ---------------------------------------------------------------- one visit row + its buttons */
  function actionsHTML(a) {
    const c = a.can || {}, id = esc(a.id), b = [];
    const add = (flag, act, cls, icon, label) => { if (flag) b.push(`<button type="button" class="ap-btn ${cls}" data-ap-act="${act}" data-ap-id="${id}">${ic(icon)}<span>${label}</span></button>`); };
    add(c.confirm, 'confirm', 'good', 'check-circle', 'Confirm');
    add(c.propose, 'propose', '', 'clock', 'Another time');
    add(c.attended, 'attended', 'good', 'check', 'Attended');
    add(c.no_show, 'no-show', 'warn', 'alert-triangle', 'No-show');
    add(c.decline, 'decline', 'danger', 'x-circle', 'Decline');
    add(c.cancel && !c.decline, 'cancel', 'danger', 'x', 'Cancel visit');   // Decline already covers a request waiting for an answer
    return b.length ? `<div class="ap-acts">${b.join('')}</div>` : '';
  }
  /* o: {showDoctor, showDate, link} */
  function rowHTML(a, o) {
    o = o || {};
    const s = stateOf(a), p = ist(a.start_at);
    const name = esc(a.patient_name || ('Patient ' + a.patient_id));
    const who = o.noLink ? name : `<a href="/patient.html?id=${encodeURIComponent(a.patient_id)}">${name}</a>`;
    const meta = [];
    if (o.showDoctor && a.doctor_name) meta.push(esc(a.doctor_name));
    if (a.kind && KIND[a.kind]) meta.push(esc(KIND[a.kind]));
    if (a.location) meta.push(esc(a.location));
    const reason = a.reason_text ? `<div class="reason"><b>Reason:</b> ${esc(a.reason_text)}</div>` : '';
    const dec = a.state === 'declined' && a.decline_reason ? `<div class="reason"><b>Declined because:</b> ${esc(a.decline_reason)}</div>` : '';
    const waiting = a.state === 'proposed' ? '<div class="reason">Waiting for the patient to answer.</div>' : '';
    return `<li class="ap-row t-${s.tone}${isPast(a.start_at) ? ' is-past' : ''}" data-ap-row="${esc(a.id)}">
      <div class="ap-time">${esc(timeWords(a.start_at))}${o.showDate && p ? `<small>${esc(shortDate(p.ymd))}</small>` : ''}</div>
      <div class="ap-who"><div class="ap-head"><span class="name">${who}</span>${stateBadge(a)}</div>
        ${meta.length ? `<div class="meta">${meta.join(' · ')}</div>` : ''}${reason}${dec}${waiting}</div>
      ${actionsHTML(a)}</li>`;
  }

  /* One click handler per list. ctx = {find(id) -> visit, reload(), doctorId?} */
  function wire(root, ctx) {
    root.addEventListener('click', async (e) => {
      const btn = e.target.closest('[data-ap-act]'); if (!btn || !root.contains(btn) || btn.disabled) return;
      const act = btn.dataset.apAct, a = ctx.find(btn.dataset.apId);
      if (!a) return;
      let body = {};
      if (act === 'decline') { const r = await askReason(a); if (!r) return; body = { reason: r }; }
      else if (act === 'propose') { const st = await askAnotherTime(a, ctx.doctorId && ctx.doctorId()); if (!st) return; body = { start_at: st }; }
      else if (act === 'cancel') { if (!(await askConfirm('Cancel this visit?', `${a.patient_name || 'The patient'} on ${whenWords(a)}. The patient will see that it is cancelled.`, 'Yes, cancel the visit'))) return; }
      else if (act === 'no-show') { if (!(await askConfirm('Mark as no-show?', `${a.patient_name || 'The patient'} did not come on ${whenWords(a)}. This cannot be undone.`, 'Yes, mark no-show', 'warn'))) return; }
      btn.classList.add('busy'); btn.disabled = true;
      try {
        await SB.api.post('/api/appointments/' + encodeURIComponent(a.id) + '/' + act, body);
        const done = { confirm: 'Visit confirmed.', propose: 'New time suggested. Waiting for the patient.', decline: 'Request declined.', cancel: 'Visit cancelled.', attended: 'Marked as attended.', 'no-show': 'Marked as no-show.' }[act];
        SB.ui.toast(done, 'good');
      } catch (err) {
        SB.ui.toast(msgOf(err, 'That did not work. Please try again.'), 'bad', 6000);
      }
      await ctx.reload();
    });
  }

  SB.appt = { STATE, KIND, stateBadge, wordOf, ist, todayYmd, addDays, validYmd, dateWords, shortDate, timeWords, whenWords, isPast,
    msgOf, problem, needLogin, modal, askConfirm, loadDoctors, doctorOptions, slotPicker, rowHTML, actionsHTML, wire, esc, ic };

  /* ================================================================ appointments.html */
  if (document.body && document.body.dataset.apPage === 'appointments') page();

  function page() {
    const main = $('#ap-body');
    const F = { doctor: '', status: '', from: todayYmd(), to: '', range: 'upcoming' };
    let items = [], doctors = [], seq = 0, me = null;

    const STATUS_OPTS = [['', 'Any status'], ['requested', 'Requested'], ['proposed', 'Alternative proposed'], ['confirmed', 'Confirmed'], ['attended', 'Attended'], ['no_show', 'No-show'], ['declined', 'Declined'], ['cancelled', 'Cancelled']];

    function shell() {
      main.innerHTML = `<section class="ap-panel" aria-label="Filters">
        <div class="ap-quick" role="group" aria-label="Quick ranges">
          <button type="button" class="ap-btn" data-range="upcoming" aria-pressed="${F.range === 'upcoming'}">Upcoming</button>
          <button type="button" class="ap-btn" data-range="past" aria-pressed="${F.range === 'past'}">Last 30 days</button>
          <button type="button" class="ap-btn" data-range="all" aria-pressed="${F.range === 'all'}">All dates</button>
        </div>
        <div class="ap-filters">
          <div class="ap-field"><label for="f-doc">Doctor</label><select id="f-doc"></select></div>
          <div class="ap-field"><label for="f-status">Status</label><select id="f-status">${STATUS_OPTS.map(([v, t]) => `<option value="${v}"${F.status === v ? ' selected' : ''}>${t}</option>`).join('')}</select></div>
          <div class="ap-field"><label for="f-from">From</label><input type="date" id="f-from" value="${esc(F.from)}"></div>
          <div class="ap-field"><label for="f-to">To</label><input type="date" id="f-to" value="${esc(F.to)}"></div>
        </div></section>
        <p class="ap-sec-sub" id="ap-count" aria-live="polite"></p>
        <div id="ap-list" aria-live="polite"><span class="skeleton ap-skel"></span></div>`;
      fillDoctors();
    }
    function fillDoctors() {
      const sel = $('#f-doc'); if (!sel) return;
      sel.innerHTML = doctorOptions(doctors, F.doctor, 'All doctors');
    }

    const setRange = (r) => {
      F.range = r;
      const t = todayYmd();
      if (r === 'upcoming') { F.from = t; F.to = ''; }
      else if (r === 'past') { F.from = addDays(t, -30); F.to = addDays(t, -1); }
      else { F.from = ''; F.to = ''; }
    };

    async function load(quiet) {
      const my = ++seq;
      const list = $('#ap-list');
      if (!quiet && list) list.innerHTML = '<span class="skeleton ap-skel"></span>';
      const qs = [];
      if (F.doctor) qs.push('doctor=' + encodeURIComponent(F.doctor));
      if (F.status) qs.push('status=' + encodeURIComponent(F.status === 'proposed' ? 'requested' : F.status));
      if (F.from && validYmd(F.from)) qs.push('from=' + F.from);
      if (F.to && validYmd(F.to)) qs.push('to=' + F.to);
      try {
        const r = await SB.api.get('/api/appointments' + (qs.length ? '?' + qs.join('&') : ''));
        if (my !== seq) return;
        items = Array.isArray(r) ? r : ((r && r.items) || []);
        // doctors we learn from the visits themselves
        items.forEach((a) => { if (a.doctor_id && !doctors.some((d) => d.id === a.doctor_id)) doctors.push({ id: a.doctor_id, name: a.doctor_name || ('Doctor ' + a.doctor_id), department: '' }); });
        doctors.sort((a, b) => a.name.localeCompare(b.name));
        fillDoctors();
        paintList();
      } catch (e) {
        if (my === seq && list) problem(list, e, () => load(), 'visits');
      }
    }

    function paintList() {
      const list = $('#ap-list'); if (!list) return;
      let rows = items.slice();
      if (F.status === 'requested' || F.status === 'proposed') rows = rows.filter((a) => a.state === F.status);
      rows.sort((a, b) => (F.range === 'upcoming' ? 1 : -1) * (new Date(a.start_at) - new Date(b.start_at)));
      $('#ap-count').textContent = rows.length === 1 ? '1 visit' : rows.length + ' visits';
      if (!rows.length) {
        list.innerHTML = `<div class="ap-empty">${ic('calendar', { size: 40 })}<b>No visits found</b>Change the filters, or use "Book a visit" to add one.</div>`;
        return;
      }
      let html = '', day = '';
      rows.forEach((a) => {
        const p = ist(a.start_at), k = p ? p.ymd : '';
        if (k !== day) {
          html += (day ? '</ul>' : '') + `<h2 class="ap-daygroup">${esc(dateWords(k))}${k === todayYmd() ? ' (today)' : ''}</h2><ul class="ap-list">`;
          day = k;
        }
        html += rowHTML(a, { showDoctor: true });
      });
      list.innerHTML = html + '</ul>';
    }

    wire(main, { find: (id) => items.find((a) => String(a.id) === String(id)), reload: () => load(true), doctorId: () => F.doctor });

    main.addEventListener('click', (e) => {
      const r = e.target.closest('[data-range]');
      if (r) { setRange(r.dataset.range); shell(); load(); }
    });
    main.addEventListener('change', (e) => {
      const t = e.target;
      if (t.id === 'f-doc') F.doctor = t.value;
      else if (t.id === 'f-status') F.status = t.value;
      else if (t.id === 'f-from') { F.from = t.value; F.range = ''; }
      else if (t.id === 'f-to') { F.to = t.value; F.range = ''; }
      else return;
      if (t.id === 'f-from' || t.id === 'f-to') main.querySelectorAll('[data-range]').forEach((b) => b.setAttribute('aria-pressed', 'false'));
      load();
    });

    /* ------------------------------------------------ Book a visit */
    async function book() {
      let patients = [];
      try { const r = await SB.api.get('/api/patients'); patients = Array.isArray(r) ? r : []; } catch (e) { SB.ui.toast(msgOf(e, 'Could not load your patients.'), 'bad', 6000); return; }
      if (!patients.length) { SB.ui.toast('There are no patients to book for yet.', 'bad'); return; }
      patients.sort((a, b) => String(a.name).localeCompare(String(b.name)));
      const pdoc = {};                                             // patient id -> primary doctor id (from the patient's detail, once)
      async function primaryOf(pid) {
        if (pdoc[pid] !== undefined) return pdoc[pid];
        let v = null;
        try { const d = await SB.api.get('/api/patients/' + encodeURIComponent(pid)); v = (d && (d.primary_doctor_id || (d.primary_doctor && d.primary_doctor.id))) || null; } catch (_) { /* no default then */ }
        return (pdoc[pid] = v);
      }
      const firstDoc = (me && me.role === 'doctor' ? me.id : '') || (doctors[0] && doctors[0].id) || '';
      let picker = null, chosen = null;
      await modal({
        title: 'Book a visit',
        body: `<div class="ap-field"><label for="bk-pat">Patient</label><select id="bk-pat">${patients.map((p) => `<option value="${esc(p.id)}">${esc(p.name)}${p.mrn ? ' · ' + esc(p.mrn) : ''}</option>`).join('')}</select></div>
          <div class="ap-field"><label for="bk-doc">Doctor</label><select id="bk-doc">${doctorOptions(doctors, firstDoc, doctors.length ? '' : 'No doctors found')}</select></div>
          <div class="ap-field"><label for="bk-kind">Kind of visit</label><select id="bk-kind"><option value="follow_up">Follow-up</option><option value="review">Review</option><option value="other">Other</option></select></div>
          <div id="bk-slots" style="display:grid;gap:var(--sp-3)"></div>
          <p class="ap-pickedtime" id="bk-picked" aria-live="polite" style="margin:0"></p>
          <div class="ap-field"><label for="bk-reason">Reason (optional)</label><input id="bk-reason" maxlength="200" autocomplete="off" placeholder="For example: wound check"></div>
          <div id="bk-err" role="alert"></div>`,
        buttons: [{ label: 'Close', value: null },
          { label: 'Book visit', cls: 'primary', icon: 'check-circle', id: 'bk-ok', run: async (d) => {
            const err = $('#bk-err', d); err.innerHTML = '';
            if (!chosen) return null;
            const body = { patient_id: Number($('#bk-pat', d).value), doctor_id: Number($('#bk-doc', d).value), start_at: chosen, kind: $('#bk-kind', d).value };
            const why = $('#bk-reason', d).value.trim(); if (why) body.reason_text = why;
            try {
              const a = await SB.api.post('/api/appointments', body);
              SB.ui.toast('Booked: ' + (whenWords(a) || dateWords(ist(chosen).ymd) + ', ' + timeWords(chosen)), 'good', 6000);
              return { close: true, value: true };
            } catch (e) {
              err.innerHTML = `<div class="ap-note bad">${ic('alert-triangle')}<span>${esc(msgOf(e, 'Could not book this visit. Please try again.'))}</span></div>`;
              if (e && e.status === 409 && picker) picker.reload();
              return null;
            }
          } }],
        onOpen: (d) => {
          const ok = $('#bk-ok', d); ok.disabled = true;
          picker = slotPicker($('#bk-slots', d), { doctor: firstDoc, onPick: (v) => { chosen = v; ok.disabled = !v; $('#bk-picked', d).textContent = v ? 'Chosen: ' + dateWords(ist(v).ymd) + ', ' + timeWords(v) : ''; } });
          $('#bk-doc', d).addEventListener('change', (e) => picker.setDoctor(e.target.value));
          async function useDefaultDoctor(pid) {
            const did = await primaryOf(pid);
            const sel = $('#bk-doc', d);
            if (!did || !sel) return;
            if (!Array.from(sel.options).some((o) => o.value === String(did))) {
              if (me && me.role === 'doctor') return;               // a doctor books only for themself
              sel.insertAdjacentHTML('beforeend', `<option value="${esc(did)}">Doctor ${esc(did)}</option>`);
            }
            if (sel.value !== String(did)) { sel.value = String(did); picker.setDoctor(did); }
          }
          $('#bk-pat', d).addEventListener('change', (e) => useDefaultDoctor(e.target.value));
          useDefaultDoctor($('#bk-pat', d).value);
        },
      }).then((done) => { if (done) load(true); });
    }
    $('#ap-book').addEventListener('click', book);

    /* ------------------------------------------------ start */
    (async function start() {
      try { await SB.ui.boot('appointments'); } catch (_) { /* the shell is optional */ }
      me = SB.ui.me;
      if (!me) { needLogin(main); $('#ap-book').hidden = true; return; }
      doctors = await loadDoctors(me);
      if (doctors.denied) { problem(main, { status: 403 }); $('#ap-book').hidden = true; return; }
      shell();
      fillDoctors();
      await load();
      setInterval(() => { if (!document.hidden && !document.querySelector('dialog[open]')) load(true); }, 60000);
    })();
  }
})();
