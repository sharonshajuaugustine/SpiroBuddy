/* SpiroBuddy - the doctor's "My day" (doctor-day.html).
 * One call, GET /api/doctor/day?date=&doctor=, gives: requests that need an answer, visits waiting for the patient,
 * and that day's visits in time order. The buttons come from each visit's `can` flags; the server checks every action again.
 * A doctor sees their own day. An admin or a nurse with the "manage appointments" permission picks a doctor first.
 * Uses SB.appt from js/appointments.js. India time (IST) everywhere. No payments, no diagnosis.
 */
(function () {
  'use strict';
  const A = SB.appt, esc = A.esc, ic = A.ic;
  const $ = (s, r) => (r || document).querySelector(s);
  const q = new URLSearchParams(location.search);
  const LS = 'sb_day_doctor';

  let me = null, doctors = [], data = null, seq = 0, loading = false;
  let date = A.validYmd(q.get('date')) ? q.get('date') : A.todayYmd();
  let doctorId = q.get('doctor') || '';
  const mine = () => !!(me && me.role === 'doctor');

  function stored() { try { return localStorage.getItem(LS) || ''; } catch (_) { return ''; } }
  function remember(v) { try { localStorage.setItem(LS, v); } catch (_) { /* private mode */ } }
  function syncUrl() {
    const p = new URLSearchParams();
    if (date !== A.todayYmd()) p.set('date', date);
    if (!mine() && doctorId) p.set('doctor', doctorId);
    try { history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : '')); } catch (_) { /* keep the address */ }
  }

  /* ------------------------------------------------ the date bar and (for admin / nurse) the doctor picker */
  function paintPick() {
    const host = $('#dd-pick');
    if (mine()) { host.innerHTML = ''; return; }
    host.innerHTML = `<section class="ap-panel" aria-label="Doctor"><div class="ap-field" style="max-width:420px"><label for="dd-doc">Whose day do you want to see?</label>
      <select id="dd-doc">${A.doctorOptions(doctors, doctorId, 'Choose a doctor')}</select></div></section>`;
  }
  function paintBar() {
    const t = A.todayYmd(), y = A.addDays(t, -1), n = A.addDays(t, 1);
    const b = (v, label, icon) => `<button type="button" class="ap-btn" data-day="${v}" aria-pressed="${date === v}"${date === v ? ' style="background:var(--brand);border-color:var(--brand);color:var(--brand-ink)"' : ''}>${icon ? ic(icon) : ''}<span>${label}</span></button>`;
    $('#dd-bar').innerHTML = `<div class="ap-bar" role="group" aria-label="Choose a day">
      ${b(y, 'Yesterday', 'arrow-left')}${b(t, 'Today')}${b(n, 'Tomorrow', 'arrow-right')}
      <label class="sr-only" for="dd-date">Pick a date</label><input class="ap-date" type="date" id="dd-date" value="${esc(date)}"></div>`;
  }

  /* ------------------------------------------------ the sections */
  const list = (arr, o) => `<ul class="ap-list">${arr.map((a) => A.rowHTML(a, o)).join('')}</ul>`;
  const section = (cls, icon, title, count, sub, inner) =>
    `<section class="ap-sec ${cls || ''}" aria-label="${esc(title)}"><h2>${ic(icon, { size: 28 })}<span>${esc(title)}</span>${count == null ? '' : `<span class="ap-count">${count}</span>`}</h2>${sub ? `<p class="ap-sec-sub">${esc(sub)}</p>` : ''}${inner}</section>`;

  function paintBody() {
    const body = $('#dd-body');
    if (!data) return;
    const need = data.needs_answer || [], wait = data.waiting_for_patient || [], visits = data.visits || [];
    const words = data.date_words || A.dateWords(date);
    const who = data.doctor && data.doctor.name ? data.doctor.name : '';
    $('#dd-sub').textContent = (who ? who + ' · ' : '') + words;
    const counts = data.counts || {};
    const nv = counts.visits != null ? counts.visits : visits.length, nn = counts.needs_answer != null ? counts.needs_answer : need.length;
    let h = `<h2 class="ap-day-title">${esc(words)}${date === A.todayYmd() ? ' (today)' : ''}</h2>
      <div class="ap-chips"><span class="ap-chip"><b>${nv}</b> ${nv === 1 ? 'visit' : 'visits'} this day</span>
      <span class="ap-chip${nn ? ' warn' : ''}"><b>${nn}</b> ${nn === 1 ? 'request needs' : 'requests need'} your answer</span></div>`;
    h += section('ask', 'hourglass', 'Needs your answer', need.length, need.length ? 'Patients asked for these times. Confirm, suggest another time, or decline.' : '',
      need.length ? list(need, { showDate: true }) : `<div class="ap-empty">${ic('check-circle', { size: 32 })}<b>Nothing is waiting for your answer</b>New requests from patients will appear here.</div>`);
    if (wait.length) {
      h += section('', 'refresh', 'Waiting for the patient', wait.length, 'You suggested another time. The patient has not answered yet.', list(wait, { showDate: true }));
    }
    h += section('', 'calendar', 'Visits on ' + words, visits.length, '',
      visits.length ? list(visits, {}) : `<div class="ap-empty">${ic('calendar', { size: 32 })}<b>No visits on this day</b>Pick another day above.</div>`);
    body.innerHTML = h;
  }

  function find(id) {
    if (!data) return null;
    return [].concat(data.needs_answer || [], data.waiting_for_patient || [], data.visits || []).find((a) => String(a.id) === String(id)) || null;
  }

  /* ------------------------------------------------ loading */
  async function load(quiet) {
    const my = ++seq; loading = true;
    const body = $('#dd-body');
    paintBar();
    if (!mine() && !doctorId) {
      data = null; $('#dd-sub').textContent = 'Choose a doctor to see their day.';
      body.innerHTML = `<div class="ap-empty">${ic('users', { size: 40 })}<b>Choose a doctor</b>${doctors.length ? 'Pick a name above to see their requests and visits.' : 'No doctors were found for your account.'}</div>`;
      loading = false; return;
    }
    if (!quiet) body.innerHTML = '<span class="skeleton ap-skel"></span>';
    try {
      const r = await SB.api.get('/api/doctor/day?date=' + encodeURIComponent(date) + (!mine() && doctorId ? '&doctor=' + encodeURIComponent(doctorId) : ''));
      if (my !== seq) return;
      data = r;
      paintBody();
    } catch (e) {
      if (my !== seq) return;
      data = null;
      A.problem(body, e, () => load(), 'doctor day');
      if (e && (e.status === 403 || e.status === 404) && !mine()) $('#dd-sub').textContent = 'Visit requests, and who is coming.';
    }
    loading = false;
  }

  function go(v) {
    if (!A.validYmd(v)) return;
    date = v; syncUrl(); load();
  }

  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-day]');
    if (b) go(b.dataset.day);
  });
  document.addEventListener('change', (e) => {
    if (e.target.id === 'dd-date') go(e.target.value);
    else if (e.target.id === 'dd-doc') { doctorId = e.target.value; if (doctorId) remember(doctorId); syncUrl(); load(); }
  });

  A.wire($('#dd-body'), { find, reload: () => load(true), doctorId: () => (data && data.doctor && data.doctor.id) || doctorId });

  (async function start() {
    try { await SB.ui.boot('doctor-day'); } catch (_) { /* the shell is optional */ }
    me = SB.ui.me;
    if (!me) { $('#dd-bar').innerHTML = ''; A.needLogin($('#dd-body')); return; }
    if (!mine()) {
      doctors = await A.loadDoctors(me);
      if (doctors.denied) { $('#dd-bar').innerHTML = ''; A.problem($('#dd-body'), { status: 403 }); return; }
      if (!doctorId) { const s = stored(); if (s && doctors.some((d) => String(d.id) === s)) doctorId = s; }
      if (!doctorId && doctors.length === 1) doctorId = String(doctors[0].id);
      paintPick();
    }
    paintBar();
    await load();
    setInterval(() => { if (!document.hidden && !document.querySelector('dialog[open]') && !loading) load(true); }, 60000);
  })();
})();
