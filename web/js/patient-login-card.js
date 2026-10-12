/* SpiroBuddy - the staff "Patient login" card on patient.html.
 * Shows the patient's hospital registration number, makes a new 6-digit PIN (shown once), and prints a slip
 * with the number, the PIN and a QR that opens /patient-login.html. The PIN lives in this page's memory only
 * until staff press "Hide the PIN"; it is never put in an address, storage or the console.
 * Needs <section class="card" id="patient-login-card"></section> on the page; fills it and does nothing else.
 * The QR library (qrcodejs 1.0.0, cdnjs) is loaded only when a slip is shown; without it the slip shows the address. */
(function () {
  'use strict';
  const host = document.getElementById('patient-login-card');
  if (!host) return;
  const pid = new URLSearchParams(location.search).get('id') || '1';
  const QR_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js';
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ic = (n, o) => (window.SB && SB.icon ? SB.icon(n, o) : '');
  const loginUrl = () => location.origin + '/patient-pin.html';

  let info = null, fresh = null, busy = false, msg = null, ownOpen = false;

  if (!document.getElementById('pl-css')) {
    const l = document.createElement('link');
    l.id = 'pl-css'; l.rel = 'stylesheet'; l.href = 'css/patient-login.css';
    document.head.appendChild(l);
  }

  async function call(method, path, body) {
    const opts = { method, credentials: 'same-origin', cache: 'no-store', headers: { Accept: 'application/json' } };
    if (method !== 'GET') { opts.headers['X-SB'] = '1'; opts.headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(body || {}); }
    let r;
    try { r = await fetch(path, opts); } catch (_) { throw new Error('Cannot reach the server. Please try again.'); }
    let data = null;
    try { data = await r.json(); } catch (_) { /* not JSON */ }
    if (!r.ok) {
      const m = (data && (data.error || data.detail)) || ('HTTP ' + r.status);
      throw Object.assign(new Error(typeof m === 'string' ? m : 'Something went wrong.'), { status: r.status });
    }
    return data;
  }

  /* ---------- the slip (always black on white) ---------- */
  function slipHTML(d) {
    return `<div class="pl-slip">
      <h3>${esc(d.hospital_name)}</h3>
      <p class="s-sub">Your login for SpiroBuddy · आपका लॉगिन</p>
      <dl>
        <dt>Patient · मरीज़</dt><dd>${esc(d.patient_name)}</dd>
        <dt>Hospital number · अस्पताल नंबर</dt><dd>${esc(d.registration_no)}</dd>
        <dt>PIN</dt><dd class="pin">${esc(d.pin)}</dd>
      </dl>
      <div class="s-go"><div class="s-qr" aria-hidden="true"></div>
        <div><div class="s-url">${esc(loginUrl())}</div><div>Scan the QR or type this address. · QR स्कैन कीजिए या यह पता खोलिए।</div></div></div>
      <p class="s-fine">Keep this slip with you. Anyone who has the number and the PIN can open this patient's medicines. If you lose it, ask the hospital for a new PIN.<br>
      यह पर्ची अपने पास रखिए। नंबर और PIN जिसके पास हो, वह इस मरीज़ की दवाइयाँ खोल सकता है। खो जाए तो अस्पताल से नया PIN माँगिए।</p>
    </div>`;
  }
  function loadQrLib() {
    if (window.QRCode) return Promise.resolve(true);
    return new Promise((resolve) => {
      const s = document.createElement('script');
      s.src = QR_SRC; s.onload = () => resolve(!!window.QRCode); s.onerror = () => resolve(false);
      document.head.appendChild(s);
    });
  }
  async function drawQr(box) {
    if (!box) return;
    box.textContent = '';
    if (!(await loadQrLib())) return;                       // offline: the written address is still on the slip
    try { new window.QRCode(box, { text: loginUrl(), width: 112, height: 112, correctLevel: window.QRCode.CorrectLevel.M }); } catch (_) { /* no QR */ }
  }

  function printSlip() {
    if (!fresh) return;
    let root = document.getElementById('pl-print-root');
    if (root) root.remove();
    root = document.createElement('div');
    root.id = 'pl-print-root';
    root.innerHTML = slipHTML(fresh);
    document.body.appendChild(root);
    document.body.classList.add('pl-printing');
    const done = () => { document.body.classList.remove('pl-printing'); const r = document.getElementById('pl-print-root'); if (r) r.remove(); window.removeEventListener('afterprint', done); };
    window.addEventListener('afterprint', done);
    drawQr(root.querySelector('.s-qr')).then(() => { setTimeout(() => { window.print(); setTimeout(done, 1500); }, 150); });
  }

  /* ---------- the card ---------- */
  function render() {
    if (!info) {
      host.innerHTML = `<div class="card-head"><h2>${ic('lock')} Patient login</h2></div>` +
        (msg ? `<div class="form-msg bad" role="alert">${esc(msg)}</div>` : '<span class="skeleton" style="height:96px"></span>');
      return;
    }
    const no = info.registration_no;
    const status = !info.set_up ? 'Not set up yet' : info.locked ? 'Locked for 15 minutes after wrong tries' : info.has_pin ? 'PIN is set' : 'No PIN yet';
    const canMake = info.set_up && info.can_edit && !busy;
    host.innerHTML = `
      <div class="card-head"><h2 id="plc-h">${ic('lock')} Patient login</h2><div class="spacer"></div><span class="muted" id="plc-status">${esc(status)}</span></div>
      <p class="plc-note" style="margin-top:0">The patient uses their hospital number and a phone code. Delivery is <b>Simulated</b>. <a href="patient-login.html?hospital=${info.hospital_id || 1}">Open patient login</a></p>
      <p>${esc(info.phone_hint || 'Phone number pending')}</p>
      ${info.can_edit ? '<label>Registered phone number<input id="plc-phone" type="tel" placeholder="Enter a new number, or leave blank" maxlength="16"></label><button class="btn sm" id="plc-save-phone" type="button">Save registered phone</button>' : ''}
      <p class="small">The reusable hospital PIN below is a fallback. It is not a one-time code.</p>
      ${info.can_plan_edit ? `<label><input type="checkbox" id="plc-breathing"${info.breathing_enabled ? ' checked' : ''}> Breathing exercise assigned (Simulated input)</label><button class="btn sm" id="plc-save-breathing" type="button">Save breathing assignment</button>` : ''}
      <div class="plc-no"><span class="muted">Hospital registration number</span><b id="plc-no">${no ? esc(no) : 'not made yet'}</b></div>
      ${!info.set_up ? `<div class="form-msg bad plc-msg" role="alert">${esc(info.message || 'This login is not set up yet.')} The database update (supabase/schema_v2.sql) has not been run.</div>` : ''}
      <div class="plc-row">
        <button class="btn primary" id="plc-make" type="button" ${canMake ? '' : 'disabled'}>${ic('refresh')} ${busy ? 'Making…' : 'Make a new PIN'}</button>
        <button class="btn ghost sm" id="plc-own-btn" type="button" aria-expanded="${ownOpen}" ${info.can_edit ? '' : 'disabled'}>Use the hospital's own number</button>
      </div>
      <p class="plc-note">${info.can_edit ? 'A new PIN is shown once, and the old PIN stops working.' : 'Only a doctor, the admin, or a nurse allowed to edit patients can make a PIN.'}</p>
      ${ownOpen ? `<form class="plc-own" id="plc-own" autocomplete="off"><label class="sr-only" for="plc-own-in">Hospital's own registration number</label>
        <input id="plc-own-in" type="text" maxlength="40" placeholder="e.g. MH-2026-0412" autocapitalize="characters" spellcheck="false"><button class="btn" type="submit">Save number</button></form>` : ''}
      <div aria-live="polite" id="plc-live">${msg ? `<div class="form-msg ${msg.startsWith('OK:') ? 'good' : 'bad'} plc-msg" role="status">${esc(msg.replace(/^OK:/, ''))}</div>` : ''}</div>
      ${fresh ? `<div class="plc-pin" id="plc-pin-box">
          <p class="plc-warn">Write this PIN on the slip now. It is shown once and cannot be looked up later.</p>
          <div class="muted">${esc(fresh.registration_no)} · ${esc(fresh.patient_name)}</div>
          <div class="plc-big" id="plc-pin">${esc(fresh.pin)}</div>
          ${slipHTML(fresh)}
          <div class="plc-row"><button class="btn primary" id="plc-print" type="button">${ic('printer')} Print the slip</button>
            <button class="btn" id="plc-hide" type="button">Hide the PIN</button></div>
        </div>` : ''}`;
    const make = host.querySelector('#plc-make');
    const phone = host.querySelector('#plc-save-phone');
    const breathing = host.querySelector('#plc-save-breathing');
    if (breathing) breathing.addEventListener('click', async () => {
      if (busy) return;
      const enabled = host.querySelector('#plc-breathing').checked;
      busy = true; breathing.disabled = true;
      try {await call('PUT', '/api/patients/' + encodeURIComponent(pid) + '/breathing', {enabled});await load();}
      catch(e){msg=e.message;render();}
      finally{busy=false;render();}
    });
    if (phone) phone.addEventListener('click', async () => {
      if (busy) return;
      const value = host.querySelector('#plc-phone').value.trim();
      busy = true; phone.disabled = true;
      try { await call('PUT', '/api/patients/' + encodeURIComponent(pid) + '/phone', {phone: value}); await load(); }
      catch (e) { msg = e.message; render(); }
      finally {busy = false; render();}
    });
    if (make) make.addEventListener('click', makePin);
    const own = host.querySelector('#plc-own-btn');
    if (own) own.addEventListener('click', () => { ownOpen = !ownOpen; msg = null; render(); const i = host.querySelector('#plc-own-in'); if (i) i.focus(); });
    const form = host.querySelector('#plc-own');
    if (form) form.addEventListener('submit', saveOwn);
    const pr = host.querySelector('#plc-print');
    if (pr) pr.addEventListener('click', printSlip);
    const hide = host.querySelector('#plc-hide');
    if (hide) hide.addEventListener('click', () => { fresh = null; msg = null; load(); });
    if (fresh) drawQr(host.querySelector('#plc-pin-box .s-qr'));
  }

  async function load() {
    try { info = await call('GET', '/api/patients/' + encodeURIComponent(pid) + '/login'); msg = fresh ? msg : null; }
    catch (e) { info = null; msg = e.status === 401 ? 'Please log in as hospital staff to see this card.' : e.message; }
    render();
  }
  async function makePin() {
    if (busy) return;
    busy = true; msg = null; render();
    try {
      fresh = await call('POST', '/api/patients/' + encodeURIComponent(pid) + '/pin');
      busy = false;
      info = Object.assign({}, info, { registration_no: fresh.registration_no, has_pin: true, locked: false });
      msg = null; render();
      const box = host.querySelector('#plc-pin-box');
      if (box && box.scrollIntoView) box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    } catch (e) {
      busy = false; fresh = null; msg = e.message; render();
    }
  }
  async function saveOwn(ev) {
    ev.preventDefault();
    const v = (host.querySelector('#plc-own-in').value || '').trim();
    if (!v) return;
    try {
      const r = await call('PUT', '/api/patients/' + encodeURIComponent(pid) + '/regno', { registration_no: v });
      ownOpen = false; fresh = null; msg = 'OK:Saved. The hospital number is now ' + r.registration_no + '. Make a new PIN for the slip.';
      await load(); msg = 'OK:Saved. The hospital number is now ' + r.registration_no + '. Make a new PIN for the slip.'; render();
    } catch (e) { msg = e.message; render(); }
  }

  render();
  load();
})();
