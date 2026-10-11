/* SpiroBuddy - the patient's medicines screen (meds.html).
 * Reads /api/me/medicines and /api/me/prescription-card with the patient session cookie (the same one the
 * patient app opens). Big text, big buttons, icons plus words, four languages. A tap on "I took it" is sent
 * as a REPORT (the screen says Reported) - SpiroBuddy never knows that a medicine was really swallowed.
 * The pharmacy screen is a full-screen white card with a QR that opens the hospital's copy for the chemist.
 */
(function () {
  'use strict';
  const M = SB.meds, esc = M.esc;
  const ic = (n, o) => SB.icon(n, o);
  const $ = (s, r) => (r || document).querySelector(s);
  const q = new URLSearchParams(location.search);
  const LS = 'sb_meds_lang';

  let lang = pickLang(), langChosen = !!(q.get('lang') && M.T[q.get('lang')]) || !!stored();
  let data = null, failed = null, view = location.hash === '#all' ? 'all' : 'home';
  let cards = null, cardIdx = 0, reading = false, busy = false;
  let sessionTried = false;

  function stored() { try { const v = localStorage.getItem(LS); return M.T[v] ? v : null; } catch (_) { return null; } }
  function pickLang() { const l = q.get('lang'); return (M.T[l] && l) || stored() || 'hi'; }
  const tr = (k, v) => M.tr(lang, k, v);

  /* ---------------------------------------------------------------- loading */
  async function openSession() {
    const t = q.get('t'), id = Number(q.get('id'));
    if (!t && !id) return false;
    try {
      const r = await SB.api.post('/api/me/session', t ? { token: t } : { patient_id: id });
      if (t) { q.delete('t'); try { history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : '') + location.hash); } catch (_) { /* keep the address */ } }
      return !!r;
    } catch (_) { return false; }
  }
  async function load() {
    failed = null;
    try {
      /* a link with ?id= or ?t= opens its own session before the read, so a new visitor does not trigger a 401 in the console */
      let opened = false;
      if (!sessionTried && (q.get('t') || Number(q.get('id')))) { sessionTried = true; opened = await openSession(); }
      try { data = await SB.api.get('/api/me/medicines'); }
      catch (e) {
        if (e && e.status === 401 && !opened && await openSession()) data = await SB.api.get('/api/me/medicines');
        else throw e;
      }
      if (!langChosen && data.patient && M.T[data.patient.language]) lang = data.patient.language;
    } catch (e) { failed = (e && e.status === 401) ? 'open' : 'load'; }
    paint();
  }

  /* ---------------------------------------------------------------- drawing */
  function paintStatic() {
    document.documentElement.lang = lang;
    document.title = tr('title') + ' · SpiroBuddy';
    $('#m-title').textContent = tr('title');
    $('#m-foot').textContent = tr('foot');
    $('#m-status-h').textContent = tr('status');
    document.querySelectorAll('#m-status [data-i]').forEach((el) => { el.textContent = tr(el.dataset.i); });
    $('#m-lang').innerHTML = M.LANGS.map((c) => `<button type="button" data-l="${c}" lang="${c}" aria-pressed="${c === lang}">${esc(M.NATIVE[c])}</button>`).join('');
    const rib = $('.ribbon-fake span', $('#m-ribbon')); if (rib) rib.textContent = tr('fake');
  }

  function groupsOf(doses) {
    const by = {};
    doses.forEach((d) => { (by[d.due_at] = by[d.due_at] || []).push(d); });
    return Object.keys(by).sort().map((k) => by[k]);
  }
  const isDone = (g) => g.every((d) => /^reported/.test(d.status));

  function doseCard(g, isNext) {
    const done = isDone(g), head = g[0];
    const slotIcon = head.slot === 'night' ? 'moon' : 'sun';
    const late = !done && g.some((d) => d.status === 'missed');
    const when = M.clock(head.due_at);
    const items = g.map((d) => {
      const food = M.foodText(d, lang);
      return `<li>${ic('pill', { size: 28 })}<div><div class="m-dose-name">${esc(d.drug_name)}${d.strength ? ` <span class="m-med-str">${esc(d.strength)}</span>` : ''}</div>
        <div class="m-dose-how">${esc(M.doseText(d, lang))}${food ? ' · ' + esc(food) : ''}</div></div></li>`;
    }).join('');
    const rep = g.map((d) => d.reported_at).filter(Boolean).sort().pop();
    const btn = done
      ? `<button type="button" class="m-btn done" disabled>${ic('check-circle', { size: 30 })}<span>${esc(rep ? tr('reportedAt', { t: M.clock(rep) }) : tr('reported'))}</span></button>`
      : `<button type="button" class="m-btn${isNext ? '' : ' outline'}" data-ids="${g.map((d) => d.id).join(',')}">${ic('check', { size: 30 })}<span>${esc(tr('took'))}</span></button>`;
    return `<section class="m-card m-dose${done ? ' done' : ''}" aria-label="${esc(tr(head.slot) + ' ' + when)}">
      <div class="m-dose-head"><span class="m-dose-ic">${ic(slotIcon, { size: 36 })}</span>
        <div><div class="m-dose-time">${esc(when)}</div><div class="m-dose-slot">${esc(tr(head.slot))}${late ? ' · ' + esc(tr('notYet')) : ''}</div></div></div>
      <ul class="m-dose-meds">${items}</ul>${btn}</section>`;
  }

  function renderHome() {
    const p = data.patient;
    let h = `<h1 class="m-hello">${esc(tr('hello', { n: p.given_name || '' }))}</h1>`;
    if (!data.has_prescription) {
      return h + `<div class="m-card m-empty">${ic('pill', { size: 56 })}<p>${esc(tr('none'))}</p>${backBtn()}</div>`;
    }
    h += `<p class="m-sub">${esc(tr('issued', { d: data.doctor || '', date: M.dateText(data.issued_on, lang) }))}</p>`;
    h += `<h2 class="m-sec-h">${ic('calendar', { size: 30 })}<span>${esc(tr('today'))}</span></h2>`;
    const groups = groupsOf(data.today || []);
    if (!groups.length) h += `<div class="m-card"><p style="margin:0">${esc(tr('noneToday'))}</p></div>`;
    else {
      const next = groups.findIndex((g) => !isDone(g));
      h += groups.map((g, i) => doseCard(g, i === next)).join('');
      if (next < 0) h += `<div class="m-msg" style="background:var(--green-soft);border:1px solid var(--green-line);color:var(--green)">${ic('check-circle', { size: 28 })}<span>${esc(tr('allDone'))}</span></div>`;
    }
    h += `<div style="margin-top:var(--sp-6)">
      <button type="button" class="m-btn plain" data-act="all">${ic('pill', { size: 30 })}<span>${esc(tr('all'))}</span></button>
      <button type="button" class="m-btn" data-act="pharmacy">${ic('file', { size: 30 })}<span>${esc(tr('pharmacy'))}</span></button></div>`;
    return h;
  }

  function readBtn() {
    if (!('speechSynthesis' in window)) return '';
    return `<button type="button" class="m-btn outline small" data-act="read">${ic('volume', { size: 28 })}<span>${esc(tr(reading ? 'stopRead' : 'readAloud'))}</span></button>`;
  }
  const backBtn = () => `<a class="m-btn plain" href="app.html?id=${esc((data && data.patient && data.patient.id) || q.get('id') || '')}&lang=${esc(lang)}">${ic('arrow-left', { size: 28 })}<span>${esc(tr('back'))}</span></a>`;

  function renderAll() {
    const lines = (data.active || []).concat(data.as_needed || []);
    let h = `<button type="button" class="m-btn plain small" data-act="home">${ic('arrow-left', { size: 28 })}<span>${esc(tr('back'))}</span></button>
      <h1 class="m-hello">${esc(tr('all'))}</h1>`;
    h += readBtn();
    h += lines.length ? lines.map((l) => M.medCard(l, lang)).join('') : `<div class="m-card m-empty">${ic('pill', { size: 56 })}<p>${esc(tr('none'))}</p></div>`;
    h += `<button type="button" class="m-btn" data-act="pharmacy">${ic('file', { size: 30 })}<span>${esc(tr('pharmacy'))}</span></button>`;
    return h;
  }

  function paint() {
    paintStatic();
    const main = $('#m-main');
    if (failed === 'open') {
      main.innerHTML = `<div class="m-card m-empty">${ic('info', { size: 56 })}<p>${esc(tr('errOpen'))}</p><a class="m-btn" href="app.html">${esc(tr('openApp'))}</a></div>`;
    } else if (failed) {
      main.innerHTML = `<div class="m-msg bad" role="alert">${ic('alert-triangle', { size: 28 })}<span>${esc(tr('errLoad'))}</span></div>
        <button type="button" class="m-btn" data-act="retry">${ic('refresh', { size: 28 })}<span>${esc(tr('retry'))}</span></button>`;
    } else if (!data) {
      return;
    } else {
      main.innerHTML = view === 'all' ? renderAll() : renderHome();
    }
    if (!$('#m-pharmacy').classList.contains('hidden')) paintCard();
  }

  /* ---------------------------------------------------------------- reading aloud */
  function toggleRead() {
    if (!('speechSynthesis' in window)) return;
    const was = reading;
    speechSynthesis.cancel();
    reading = false;
    if (!was) {
      const lines = (data.active || []).concat(data.as_needed || []);
      if (lines.length) {
        reading = true;
        lines.forEach((l, i) => {
          const u = new SpeechSynthesisUtterance(M.speakText(l, lang));
          u.lang = M.SPEECH[lang]; u.rate = 0.9;
          if (i === lines.length - 1) u.onend = u.onerror = () => { reading = false; if (view === 'all') paint(); };
          speechSynthesis.speak(u);
        });
      }
    }
    paint();
  }

  /* ---------------------------------------------------------------- reporting */
  async function report(btn) {
    if (busy) return;
    busy = true;
    const ids = btn.dataset.ids.split(',');
    btn.disabled = true; btn.querySelector('span').textContent = tr('saving');
    try {
      const done = await Promise.all(ids.map((id) => SB.api.post('/api/me/doses/' + id + '/report', {})));
      done.forEach((d) => { const i = data.today.findIndex((x) => x.id === d.id); if (i >= 0) data.today[i] = d; });
      paint();
    } catch (_) {
      paint();
      $('#m-main').insertAdjacentHTML('afterbegin', `<div class="m-msg bad" role="alert">${ic('alert-triangle', { size: 28 })}<span>${esc(tr('errReport'))}</span></div>`);
    }
    busy = false;
  }

  /* ---------------------------------------------------------------- the pharmacy screen */
  const SEX = { M: 'Male', F: 'Female', O: 'Other' };
  const dmy = (iso) => (iso ? M.dateText(iso, 'en') : '');   // 12 October 2026, not 12/10/2026 (day/month is ambiguous)

  function drawQR(box, url) {
    box.innerHTML = '';
    if (window.QRCode) {
      try { new window.QRCode(box, { text: url, width: 168, height: 168, correctLevel: window.QRCode.CorrectLevel.M, colorDark: '#000000', colorLight: '#ffffff' }); return; } catch (_) { /* fall through */ }
    }
    box.innerHTML = '<span style="font-weight:700;text-align:center;padding:8px">QR not available offline</span>';
  }

  function paintCard() {
    const ov = $('#m-pharmacy');
    const bar = `<div class="rxc-bar"><p id="rxc-bar-t">${esc(tr('showTitle'))}</p><button type="button" class="rxc-close" data-act="close">${ic('x', { size: 28 })}<span>${esc(tr('close'))}</span></button></div>`;
    if (!cards) { ov.innerHTML = bar + '<div class="rxc-paper"><p>…</p></div>'; return; }
    if (!cards.length) { ov.innerHTML = bar + `<div class="rxc-paper"><p class="rxc-n">No current prescription.</p><p class="rxc-how">${esc(tr('none'))}</p></div>`; return; }
    const c = cards[Math.min(cardIdx, cards.length - 1)];
    const reg = c.doctor && c.doctor.reg_no_display ? esc(c.doctor.reg_no_display) : 'Not recorded';
    const url = location.origin + c.verify_path;
    const meds = c.lines.map((l, i) => `<li><div class="rxc-n">${i + 1}. ${esc(l.drug_name)}${l.strength ? ` <small>${esc(l.strength)}</small>` : ''}${l.as_needed ? '<span class="rxc-tag">ONLY WHEN NEEDED</span>' : ''}</div>
        <div class="rxc-how">${esc(M.summary(l))}</div>${l.instructions ? `<div class="rxc-note">Note: ${esc(l.instructions)}</div>` : ''}</li>`).join('');
    const pager = cards.length > 1 ? `<div class="rxc-pager"><button type="button" data-act="prev">Previous</button><span style="align-self:center;font-weight:800">${cardIdx + 1} / ${cards.length}</span><button type="button" data-act="next">Next</button></div>` : '';
    ov.innerHTML = bar + `<div class="rxc-paper">
      <p class="rxc-hosp">${esc(c.hospital.name || '')}${c.hospital.city ? `<small>${esc(c.hospital.city)}</small>` : ''}</p>
      <h2 class="rxc-title">Prescription</h2>
      <dl class="rxc-grid">
        <div><dt>Patient</dt><dd>${esc(c.patient.name)}<br><small>${esc(c.patient.age != null ? c.patient.age + ' years' : '')}${c.patient.sex ? ' · ' + esc(SEX[c.patient.sex] || c.patient.sex) : ''}</small></dd></div>
        <div><dt>Issued on</dt><dd>${esc(dmy(c.issued_on))}</dd></div>
        <div><dt>Doctor</dt><dd>${esc((c.doctor && c.doctor.name) || '')}</dd></div>
        <div><dt>Registration number <small>(display only)</small></dt><dd>${reg}</dd></div>
      </dl>
      <ol class="rxc-meds" style="list-style:none">${meds}</ol>
      <div class="rxc-qr"><div class="rxc-qr-box" id="rxc-qr-box"></div>
        <p>Pharmacist: scan this code to check the prescription at the hospital.<small>${esc(url)}</small></p></div>
      <p class="rxc-demo">${esc(c.notice || 'Demo - fictional patient. Pharmacy acceptance is not yet tested.')}</p>${pager}</div>`;
    drawQR($('#rxc-qr-box', ov), url);
  }

  async function openCard() {
    const ov = $('#m-pharmacy');
    ov.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    cards = null; cardIdx = 0; paintCard();
    ov.scrollTop = 0;
    const closeBtn = $('.rxc-close', ov); if (closeBtn) closeBtn.focus();
    try { const r = await SB.api.get('/api/me/prescription-card'); cards = r.cards || []; }
    catch (_) { cards = []; }
    paintCard();
    const c2 = $('.rxc-close', ov); if (c2) c2.focus();
  }
  function closeCard() {
    $('#m-pharmacy').classList.add('hidden');
    document.body.style.overflow = '';
    const b = $('[data-act="pharmacy"]'); if (b) b.focus();
  }

  /* ---------------------------------------------------------------- events */
  document.addEventListener('click', (e) => {
    const lb = e.target.closest('#m-lang [data-l]');
    if (lb) {
      lang = lb.dataset.l; langChosen = true;
      try { localStorage.setItem(LS, lang); } catch (_) { /* private mode */ }
      if (reading) { speechSynthesis.cancel(); reading = false; }
      paint(); return;
    }
    const took = e.target.closest('[data-ids]');
    if (took) { report(took); return; }
    const act = e.target.closest('[data-act]');
    if (!act) return;
    const a = act.dataset.act;
    if (a === 'all') { view = 'all'; history.replaceState(null, '', '#all'); paint(); window.scrollTo(0, 0); }
    else if (a === 'home') { view = 'home'; history.replaceState(null, '', location.pathname + location.search); paint(); window.scrollTo(0, 0); }
    else if (a === 'pharmacy') openCard();
    else if (a === 'close') closeCard();
    else if (a === 'read') toggleRead();
    else if (a === 'retry') { $('#m-main').innerHTML = '<div class="m-card"><span class="skeleton" style="height:72px"></span></div>'; load(); }
    else if (a === 'prev' && cards) { cardIdx = (cardIdx + cards.length - 1) % cards.length; paintCard(); $('#m-pharmacy').scrollTop = 0; }
    else if (a === 'next' && cards) { cardIdx = (cardIdx + 1) % cards.length; paintCard(); $('#m-pharmacy').scrollTop = 0; }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !$('#m-pharmacy').classList.contains('hidden')) closeCard(); });
  window.addEventListener('pagehide', () => { try { speechSynthesis.cancel(); } catch (_) { /* no speech */ } });

  /* ---------------------------------------------------------------- start */
  (async function start() {
    paintStatic();
    try { await SB.api.init(); } catch (_) { /* a failed load shows the retry message */ }
    try { SB.ui.loadFeatures(); } catch (_) { /* badges are optional */ }
    try { SB.ui.fakeRibbon({ into: '#m-ribbon', large: true, text: tr('fake') }); } catch (_) { /* optional */ }
    await load();
  })();
})();
