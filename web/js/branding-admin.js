/* SpiroBuddy - "App branding" page for the hospital admin (web/branding.html).
 * Talks to GET/PUT /api/admin/branding and POST/DELETE /api/admin/branding/logo. The server is the judge of
 * every value; the colour check below only gives an answer while typing (same rules as backend/app/branding.py).
 * The preview is drawn with the same code the patient app uses (js/branding.js). */
(function () {
  'use strict';
  const { $, esc, ic } = SB.ui;
  const HEX = /^#[0-9a-fA-F]{6}$/;
  const PAGE_BG = { light: '#f4f6f8', dark: '#0d1319' };
  const INK = { light: '#ffffff', dark: '#101c27' };
  const MAX_TEXT = 4.5, MIN_EDGE = 1.5, MAX_LOGO = 512 * 1024;

  let saved = null;            // what the server holds: the admin view
  let busy = false;

  /* ---------- colour check (mirrors branding.check_accent) ---------- */
  function lin(v) { const c = v / 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  function lum(h) { const n = parseInt(h.slice(1), 16); return 0.2126 * lin(n >> 16 & 255) + 0.7152 * lin(n >> 8 & 255) + 0.0722 * lin(n & 255); }
  function ratio(a, b) { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function inkFor(a) { return ratio(INK.light, a) >= ratio(INK.dark, a) ? INK.light : INK.dark; }
  function colourProblem(v) {
    if (!HEX.test(v)) return 'The colour must look like #0b6e8a (a # and six letters or digits).';
    v = v.toLowerCase();
    if (ratio(inkFor(v), v) < MAX_TEXT) return 'This colour is too hard to read text on. Please pick a darker or a lighter shade.';
    if (ratio(v, PAGE_BG.light) < MIN_EDGE) return 'This colour is too close to white. On the light screen the name strip would fade into the page. Please pick a stronger colour.';
    if (ratio(v, PAGE_BG.dark) < MIN_EDGE) return 'This colour is too close to black. On the dark screen the name strip would fade into the page. Please pick a lighter colour.';
    return '';
  }

  /* ---------- small helpers ---------- */
  function say(id, text, tone) {
    const n = $('#' + id);
    n.className = 'form-msg bd-msg ' + (tone || 'info');
    n.setAttribute('role', tone === 'bad' ? 'alert' : 'status');
    n.innerHTML = text ? `${ic(tone === 'bad' ? 'alert-triangle' : tone === 'good' ? 'check' : 'info', { size: 18 })}<span>${esc(text)}</span>` : '';
  }
  function draft() {
    return { display_name: $('#f-name').value.trim(), short_name: $('#f-short').value.trim(), accent: $('#f-hex').value.trim() };
  }
  function problems(d) {
    const out = [];
    if (d.display_name.length < 2 || d.display_name.length > 40) out.push('The app name needs 2 to 40 characters.');
    if (d.short_name.length < 2 || d.short_name.length > 14) out.push('The short name needs 2 to 14 characters.');
    const c = colourProblem(d.accent);
    if (c) out.push(c);
    return out;
  }

  /* ---------- preview ---------- */
  function paintPreview() {
    const d = draft();
    const okColour = !colourProblem(d.accent);
    const view = {
      display_name: d.display_name || (saved && saved.display_name) || 'Your hospital',
      accent: okColour ? d.accent.toLowerCase() : (saved && saved.accent) || '#0b6e8a',
      accent_ink: okColour ? inkFor(d.accent.toLowerCase()) : (saved && saved.accent_ink) || '#ffffff',
      logo_url: saved && saved.logo_url,
    };
    const host = $('#bd-preview');
    if (window.SBBrand) { SBBrand.addCss(); SBBrand.render(view, host); }
    const msg = d.accent && colourProblem(d.accent);
    say('f-col-msg', msg || '', 'bad');
  }

  function fill(view) {
    saved = view;
    $('#f-name').value = view.display_name;
    $('#f-short').value = view.short_name;
    setColour(view.accent);
    paintLogo();
    paintPreview();
    if (Array.isArray(view.fixed) && view.fixed.length) {
      $('#bd-fixed').innerHTML = view.fixed.map((t) => `<li>${esc(t)}</li>`).join('');
    }
  }
  function setColour(v) { $('#f-hex').value = v; if (HEX.test(v)) $('#f-colour').value = v.toLowerCase(); }
  function paintLogo() {
    const box = $('#logo-now');
    if (saved && saved.logo_url) { box.innerHTML = `<img alt="Current logo" src="${esc(saved.logo_url)}">`; }
    else { box.textContent = 'No logo'; }
    $('#logo-rm').disabled = !(saved && saved.logo_url);
  }

  /* ---------- actions ---------- */
  async function save(e) {
    e.preventDefault();
    if (busy) return;
    const d = draft();
    const p = problems(d);
    if (p.length) { say('bd-msg', p[0], 'bad'); return; }
    busy = true;
    try {
      const r = await SB.ui.busy($('#bd-save'), () => SB.api.put('/api/admin/branding', d));
      fill(r);
      say('bd-msg', 'Saved. Patients see the new name the next time they open the app.', 'good');
    } catch (err) {
      say('bd-msg', (err && err.message) || 'Could not save. Please try again.', 'bad');
    } finally { busy = false; }
  }
  async function upload() {
    const f = $('#f-file').files[0];
    if (!f) { say('logo-msg', 'Choose a PNG, JPEG or WebP picture to upload.', 'bad'); return; }
    if (f.size > MAX_LOGO) { say('logo-msg', 'This picture is larger than 512 KB. Please use a smaller one.', 'bad'); return; }
    if (!/^image\/(png|jpeg|webp)$/.test(f.type)) { say('logo-msg', 'The logo must be a PNG, JPEG or WebP picture.', 'bad'); return; }
    const fd = new FormData();
    fd.append('file', f, f.name);
    try {
      const r = await SB.ui.busy($('#logo-up'), () => SB.api.upload('/api/admin/branding/logo', fd));
      saved = Object.assign({}, saved, { logo_url: r.logo_url });
      $('#f-file').value = '';
      paintLogo(); paintPreview();
      say('logo-msg', 'Logo saved.', 'good');
    } catch (err) {
      say('logo-msg', (err && err.message) || 'The logo could not be saved.', 'bad');
    }
  }
  async function removeLogo() {
    try {
      const r = await SB.ui.busy($('#logo-rm'), () => SB.api.del('/api/admin/branding/logo'));
      saved = Object.assign({}, saved, { logo_url: r.logo_url });
      paintLogo(); paintPreview();
      say('logo-msg', 'Logo removed.', 'good');
    } catch (err) {
      say('logo-msg', (err && err.message) || 'The logo could not be removed.', 'bad');
    }
  }

  function wire() {
    $('#bd-form').addEventListener('submit', save);
    ['f-name', 'f-short'].forEach((id) => $('#' + id).addEventListener('input', paintPreview));
    $('#f-hex').addEventListener('input', () => { const v = $('#f-hex').value.trim(); if (HEX.test(v)) $('#f-colour').value = v.toLowerCase(); paintPreview(); });
    $('#f-colour').addEventListener('input', () => { $('#f-hex').value = $('#f-colour').value; paintPreview(); });
    $('#f-colour-reset').addEventListener('click', () => { setColour((saved && saved.defaults && saved.defaults.accent) || '#0b6e8a'); paintPreview(); });
    $('#bd-undo').addEventListener('click', () => { if (saved) { fill(saved); say('bd-msg', '', 'info'); } });
    $('#logo-up').addEventListener('click', upload);
    $('#logo-rm').addEventListener('click', removeLogo);
  }

  function lock(message) {
    $('#bd-grid').classList.add('hidden');
    $('#bd-note').innerHTML = `<div class="empty">${ic('lock', { size: 28 })}<b>${esc(message)}</b></div>`;
  }

  (async function start() {
    await SB.ui.boot('branding');
    SB.ui.hydrateIcons(document);
    wire();
    if (SB.api.state.mock) { lock('This page needs the live server. It is not available in the offline demo.'); return; }
    const me = await SB.auth.me();
    if (!me || !me.authenticated || me.kind === 'patient') {
      if (SB.auth.loginRedirect('/api/auth/me')) return;
      lock('Please log in as the hospital admin.'); return;
    }
    if (me.role !== 'admin') { lock('Only the hospital admin can change the app branding.'); return; }
    try {
      fill(await SB.api.get('/api/admin/branding'));
    } catch (err) {
      lock((err && err.status === 403) ? 'Only the hospital admin can change the app branding.' : ((err && err.message) || 'Could not load the branding.'));
    }
  })();
})();
