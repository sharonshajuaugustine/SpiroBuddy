/* SpiroBuddy - the hospital's own name and logo at the top of the patient pages.
 * Add ONE script tag to a page that has <div id="brand-slot" hidden></div>. This file:
 *   1. waits until a login exists (the patient pages open their session a moment after loading),
 *   2. asks GET /api/me/branding (patient session) or GET /api/branding/mine (staff session),
 *   3. fills the slot with the logo, the hospital's app name and the fixed line "with SpiroBuddy".
 * Any problem (no login, offline, error, old browser) leaves the page exactly as it was: the slot stays hidden.
 * The accent colour paints this strip only. Everything it writes goes in as text or as an image address
 * that starts with /api/ - never as markup. */
(function () {
  'use strict';
  var slot = document.getElementById('brand-slot');

  var DELAYS = [0, 700, 1800, 4000, 8000];     // ms: when to look for a login (it opens a moment after the page)
  var HEX = /^#[0-9a-fA-F]{6}$/;

  function getJson(url) {
    return fetch(url, { credentials: 'same-origin', cache: 'no-store', headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); });
  }

  function addCss() {
    if (document.getElementById('brand-css')) return;
    var l = document.createElement('link');
    l.id = 'brand-css'; l.rel = 'stylesheet'; l.href = 'css/branding.css';
    document.head.appendChild(l);
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  /* b = {display_name, accent, accent_ink, logo_url, powered_by}; also used by the admin page preview */
  function render(b, into) {
    var host = into || slot;
    if (!host || !b || typeof b.display_name !== 'string' || !b.display_name) return false;
    var strip = el('div', 'brand-strip');
    strip.setAttribute('role', 'group');
    strip.setAttribute('aria-label', b.display_name + ' ' + (b.powered_by || 'with SpiroBuddy'));
    if (HEX.test(b.accent || '')) strip.style.setProperty('--brand-accent', b.accent);
    if (HEX.test(b.accent_ink || '')) strip.style.setProperty('--brand-ink', b.accent_ink);
    if (typeof b.logo_url === 'string' && b.logo_url.indexOf('/api/') === 0) {
      var img = el('img', 'brand-logo');
      img.alt = ''; img.width = 48; img.height = 48; img.decoding = 'async';
      img.onerror = function () { if (img.parentNode) img.parentNode.removeChild(img); };   // no picture: the name still shows
      img.src = b.logo_url;
      strip.appendChild(img);
    }
    var text = el('div', 'brand-text');
    text.appendChild(el('span', 'brand-name', b.display_name));
    text.appendChild(el('span', 'brand-by', 'with SpiroBuddy'));    // fixed line: not read from the server
    strip.appendChild(text);
    host.textContent = '';
    host.appendChild(strip);
    host.hidden = false;
    return true;
  }

  function load() {
    return getJson('/api/auth/me').then(function (me) {
      if (!me || !me.authenticated) throw new Error('no login yet');
      return getJson(me.kind === 'patient' ? '/api/me/branding' : '/api/branding/mine');
    });
  }

  function attempt(i) {
    if (i >= DELAYS.length) return;
    setTimeout(function () {
      load().then(function (b) { render(b); }).catch(function () { attempt(i + 1); });
    }, DELAYS[i] - (i ? DELAYS[i - 1] : 0));
  }

  window.SBBrand = { render: render, addCss: addCss };      // the admin page draws its preview with these
  if (!slot || !window.fetch) return;                          // a page without the slot is left alone
  addCss();
  attempt(0);
})();
