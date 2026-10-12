/* SpiroBuddy public story site: shared header, footer, theme button, status legend and small helpers.
 * Needs /js/icons.js, /js/api.js and /js/ui.js loaded before it. Every status badge comes from the
 * registry (GET /api/features) through SB.ui: this file never writes a status word by hand. */
(function () {
  const SB = (window.SB = window.SB || {});
  const ui = SB.ui;
  const esc = ui.esc;

  const NAV = [
    ['Home', '/'],
    ['Impact', '/impact.html'],
    ['Trust', '/trust.html'],
    ['Vision', '/vision.html'],
    ['Architecture', '/architecture.html'],
    ['3D showroom', '/showcase/'],
  ];
  const LOGIN = '/login.html?next=/dashboard.html';
  const APP = '/patient-login.html';

  function here() {
    const p = location.pathname.replace(/index\.html$/, '');
    return p === '' ? '/' : p;
  }

  function headerHTML() {
    const cur = here();
    const links = NAV.map(([label, href]) =>
      `<li><a class="nav-link" href="${href}"${href === cur ? ' aria-current="page"' : ''}>${esc(label)}</a></li>`).join('');
    return `
      <a class="skip-link" href="#main">Skip to content</a>
      <div class="pub-bar"><div class="pub-wrap">
        <a class="logo" href="/" aria-label="SpiroBuddy home page">${ui.LOGO}<span class="logo-name">SpiroBuddy</span></a>
        <nav class="pub-nav" id="pub-nav" aria-label="Main">
          <ul>${links}
            <li class="nav-cta"><a class="btn" href="${LOGIN}">Hospital login</a><a class="btn primary" href="${APP}">Patient login</a></li>
          </ul>
        </nav>
        <div class="pub-actions">
          <a class="btn sm" href="${LOGIN}">Hospital login</a>
          <a class="btn sm primary" href="${APP}">Patient login</a>
          <button class="icon-btn" id="pub-theme" type="button" aria-label="Switch light or dark theme" title="Light / dark theme"></button>
          <button class="icon-btn pub-menu-btn" id="pub-menu" type="button" aria-expanded="false" aria-controls="pub-nav" aria-label="Open the menu">
            <svg class="i" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
          </button>
        </div>
      </div></div>`;
  }

  function footerHTML() {
    return `
      <div class="pub-wrap">
        <p class="foot-notice">Sample patients · not a medical device · not for clinical use</p>
        <p class="small">The hospital on this site is fictional (Dawnlight General Hospital). No real hospital, doctor or patient appears here.</p>
        <ul>
          <li><a href="/">Home</a></li><li><a href="/impact.html">Impact</a></li><li><a href="/trust.html">Trust</a></li>
          <li><a href="/vision.html">Vision</a></li><li><a href="/architecture.html">Architecture</a></li>
          <li><a href="/showcase/">3D showroom</a></li><li><a href="${LOGIN}">Hospital login</a></li><li><a href="${APP}">Patient app</a></li>
        </ul>
      </div>`;
  }

  function paintTheme() {
    const b = document.getElementById('pub-theme');
    if (b) b.innerHTML = ui.ic(ui.currentTheme() === 'dark' ? 'sun' : 'moon');
  }

  function mount() {
    document.body.classList.add('pub');
    const h = document.getElementById('pub-header');
    if (h) h.innerHTML = headerHTML();
    const f = document.getElementById('pub-footer');
    if (f) { f.className = 'pub-foot'; f.innerHTML = footerHTML(); }

    const theme = document.getElementById('pub-theme');
    if (theme) {
      theme.addEventListener('click', () => {
        const next = ui.currentTheme() === 'dark' ? 'light' : 'dark';
        ui.applyTheme(next);
        try { localStorage.setItem('sb_theme', next); } catch (_) { /* private mode */ }
        paintTheme();
      });
      paintTheme();
    }
    const menu = document.getElementById('pub-menu');
    const nav = document.getElementById('pub-nav');
    if (menu && nav) {
      const set = (open) => { nav.classList.toggle('open', open); menu.setAttribute('aria-expanded', String(open)); menu.setAttribute('aria-label', open ? 'Close the menu' : 'Open the menu'); };
      menu.addEventListener('click', () => set(!nav.classList.contains('open')));
      document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('open')) { set(false); menu.focus(); } });
      nav.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    }
    const main = document.getElementById('main');
    if (main && !main.hasAttribute('tabindex')) main.setAttribute('tabindex', '-1');
    ui.hydrateIcons(document);
    ui.loadFeatures();        // fills every <span data-feature="key"></span> once the registry answers
  }

  /* Status legend: the four words and one line each, drawn from the shared kit (SB.ui.FSTATUS). */
  const LEGEND_TEXT = {
    live: 'Works on this site today, with sample patients.',
    simulated: 'Works from start to finish, but its input or its sending is a built-in simulator.',
    in_development: 'Partly built. Not switched on, or not working from start to finish yet.',
    planned: 'Not built. Shown only so you can see where we are heading.',
  };
  function legend(el) {
    if (!el) return;
    el.innerHTML = Object.keys(LEGEND_TEXT).map((k) => {
      const s = ui.FSTATUS[k];
      return `<div class="legend-row"><span class="fbadge ${k}">${ui.ic(s.icon, { size: 14 })}${esc(s.word)}</span><span class="ld">${esc(LEGEND_TEXT[k])}</span></div>`;
    }).join('');
  }

  /* Tiny render helpers shared by the page scripts. */
  const LBL = { estimate: 'Estimate', assumption: 'Assumption', target: 'Target', counted: 'Counted', demo: 'Sample data' };
  const lbl = (kind) => `<span class="lbl ${esc(kind)}">${esc(LBL[kind] || kind)}</span>`;
  const src = (text) => `<span class="src">${esc(text)}</span>`;
  const badge = (key) => `<span data-feature="${esc(key)}"></span>`;
  const nf = (n, d) => Number(n).toLocaleString('en-IN', { maximumFractionDigits: d == null ? 0 : d, minimumFractionDigits: d == null ? 0 : d });

  async function getJSON(path) {
    const r = await fetch(path, { headers: { Accept: 'application/json' } });
    if (!r.ok) throw new Error(path + ' ' + r.status);
    return r.json();
  }

  window.SBPub = { esc, lbl, src, badge, nf, getJSON, legend, hydrate: (root) => ui.hydrateBadges(root || document), paintTheme };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
  document.querySelectorAll('[data-legend]').forEach(legend);
  document.addEventListener('DOMContentLoaded', () => document.querySelectorAll('[data-legend]').forEach(legend));
})();
