/* SpiroBuddy – shared UI: app shell (top bar, side nav, system status, IST clock), banners, theme, toasts, helpers.
 * Optional: js/icons.js (loaded first) for line icons. If a page doesn't load it, ui.js loads it itself
 * and fills every <span data-icon="…"> when it arrives. */
(function () {
  const SB = (window.SB = window.SB || {});

  const LOGO = `<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0b6e8a"/>
    <rect x="9" y="6" width="6" height="20" rx="3" fill="#fff" opacity=".35"/><rect x="9" y="13" width="6" height="13" rx="3" fill="#fff"/>
    <path d="M19 12c3 0 3 4 6 4M19 18c3 0 3 4 6 4" stroke="#7fe0c8" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>`;

  /* Demo site identity shown in the top bar (fake hospital – demo only). */
  const SITE = { hospital: 'Demo City Hospital', ward: 'Post-op Ward 3B' };

  const PAGES = [
    { group: 'Ward', href: 'index.html', label: 'Dashboard', key: 'dashboard', icon: 'dashboard' },
    { group: 'Ward', href: 'index.html#alerts', label: 'Alerts', key: 'alerts', icon: 'bell', count: true },
    { group: 'Ward', href: 'index.html#patients-card', label: 'Patients', key: 'patient', icon: 'users' },
    { group: 'Tools', href: 'demo.html', label: 'Demo panel', key: 'demo', icon: 'sliders' },
    { group: 'Tools', href: 'collect.html', label: 'Record breaths', key: 'collect', icon: 'activity' },
    { group: 'Tools', href: 'showcase/', label: '3D showroom', key: 'showcase', icon: 'cube', ext: true },
  ];

  /* ---------- helpers ---------- */
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  function link(href) {
    // keep ?mock=1 when it was forced, so navigation stays in mock mode
    if (SB.api && SB.api.state.forcedMock && !/^https?:/.test(href)) {
      const [path, hash] = href.split('#');
      return path + (path.includes('?') ? '&' : '?') + 'mock=1' + (hash ? '#' + hash : '');
    }
    return href;
  }
  /* icon html (empty placeholder that fills itself if icons.js is not loaded yet) */
  function ic(name, opts) {
    if (SB.icon) return SB.icon(name, opts);
    return `<span class="i-ph" data-icon="${esc(name)}" data-size="${(opts && opts.size) || 18}" aria-hidden="true"></span>`;
  }
  function hydrateIcons(root) {
    if (!SB.icon) return;
    $$('[data-icon]', root).forEach((el) => {
      if (el.dataset.done) return;
      el.dataset.done = '1';
      el.innerHTML = SB.icon(el.dataset.icon, { size: Number(el.dataset.size) || 18 });
    });
  }
  if (!SB.icon && document.currentScript) {
    const s = document.createElement('script');
    s.src = document.currentScript.src.replace(/ui\.js(\?.*)?$/, 'icons.js');
    s.onload = () => hydrateIcons(document);
    document.head.appendChild(s);
  }

  // 12-hour clock as used in India: 8 → "8 am", 13 → "1 pm", 12 → "12 pm" (API keeps 24-hour numbers).
  function hourLabel(h) { const n = ((Number(h) % 24) + 24) % 24; return (n % 12 || 12) + (n < 12 ? ' am' : ' pm'); }
  function hourRange(a, b) { return hourLabel(a) + '–' + hourLabel(b); }
  function parseDate(v) { if (!v) return null; const d = new Date(v); return isNaN(d) ? null : d; }
  function timeLabel(v) { const d = parseDate(v); return d ? d.toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true }) : '—'; }
  function dateTimeLabel(v) {
    const d = parseDate(v); if (!d) return '—';
    const today = new Date().toDateString() === d.toDateString();
    return today ? 'Today ' + timeLabel(d) : d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) + ' ' + timeLabel(d);
  }
  function ago(v) {
    const d = parseDate(v); if (!d) return 'no sessions yet';
    const s = Math.round((Date.now() - d.getTime()) / 1000);
    if (s < 45) return 'just now';
    if (s < 3600) return Math.round(s / 60) + ' min ago';
    if (s < 86400) return Math.round(s / 3600) + ' h ago';
    return Math.round(s / 86400) + ' d ago';
  }
  /* "3:04 pm IST" – the ward clock is always India time */
  function istClock(d) { return (d || new Date()).toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: 'numeric', minute: '2-digit', hour12: true }) + ' IST'; }
  function istDate(d) { return (d || new Date()).toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); }
  function initials(name) { return String(name || '?').split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join(''); }

  /* Status: colour + icon + word, always together. */
  const STATUS_TEXT = { red: 'Needs a call', yellow: 'Watch', green: 'On track' };
  const STATUS_ICON = { red: 'alert-octagon', yellow: 'alert-triangle', green: 'check-circle' };
  const STATUS_RANK = { red: 0, yellow: 1, green: 2 };
  function statusPill(status) { const s = STATUS_TEXT[status] ? status : 'green'; return `<span class="status-pill status-${s}">${ic(STATUS_ICON[s], { size: 14 })}${STATUS_TEXT[s]}</span>`; }
  function redFlagPill() { return `<span class="status-pill status-flag redflag-badge" title="Open red-flag alert – see the alerts inbox">${ic('flag', { size: 14 })}Red flag</span>`; }
  function normTrend(t) {
    if (typeof t === 'number') return t > 0.02 ? 'up' : t < -0.02 ? 'down' : 'flat';
    const s = String(t || '').toLowerCase();
    if (['up', 'improving', 'rising', '+', 'better'].includes(s)) return 'up';
    if (['down', 'worse', 'falling', 'declining', '-'].includes(s)) return 'down';
    return 'flat';
  }
  // Breath volume over the last 3 days vs the 3 days before (not an overall "getting better" verdict).
  // Pass the patient object: when today is due but nothing is done, no arrow is shown, so the card
  // never says "▲ Higher" next to "Needs a call".
  function trendHTML(t, p) {
    if (p && typeof p === 'object' && (p.due_today || 0) > 0 && !(p.done_today > 0)) return `<span class="trend-flat" title="No sessions done yet today">${ic('minus', { size: 14 })}None today</span>`;
    const n = normTrend(t);
    const tip = 'Best-breath volume, last 3 days vs the 3 days before';
    return n === 'up' ? `<span class="trend-up" title="${tip}">${ic('arrow-up', { size: 14 })}Higher</span>` : n === 'down' ? `<span class="trend-down" title="${tip}">${ic('arrow-down', { size: 14 })}Lower</span>` : `<span class="trend-flat" title="${tip}">${ic('arrow-right', { size: 14 })}Steady</span>`;
  }
  const TREND_LABEL = 'Volume (3 days)';
  const LANG = { en: 'English', hi: 'Hindi', ta: 'Tamil', ml: 'Malayalam', te: 'Telugu', kn: 'Kannada', bn: 'Bengali', mr: 'Marathi', gu: 'Gujarati', pa: 'Punjabi', or: 'Odia' };
  const LABEL_TEXT = { good: 'Good', too_fast: 'Too fast', too_shallow: 'Too shallow', no_hold: 'No hold' };
  function labelChips(counts) {
    if (!counts) return '—';
    return Object.keys(LABEL_TEXT).filter((k) => counts[k]).map((k) => `<span class="lbl-chip lbl-${k}">${LABEL_TEXT[k]} ${counts[k]}</span>`).join('') || '—';
  }
  function fmtMl(v) { return v == null || v === '' || Number(v) === 0 ? '—' : Math.round(Number(v)).toLocaleString('en-IN') + ' mL'; }
  /* small horizontal meter: value 0..1, tone = good | warn | bad | brand */
  function meter(frac, tone, label) {
    const pct = Math.max(0, Math.min(1, Number(frac) || 0)) * 100;
    return `<span class="meter ${tone || 'brand'}" role="img" aria-label="${esc(label || Math.round(pct) + '%')}"><span style="width:${pct.toFixed(1)}%"></span></span>`;
  }

  /* ---------- toasts ---------- */
  function toast(msg, kind, ms) {
    let box = $('.toasts');
    if (!box) { box = document.createElement('div'); box.className = 'toasts'; box.setAttribute('role', 'status'); box.setAttribute('aria-live', 'polite'); document.body.appendChild(box); }
    const t = document.createElement('div');
    t.className = 'toast' + (kind ? ' ' + kind : '');
    t.textContent = msg;
    box.appendChild(t);
    setTimeout(() => t.remove(), ms || 4000);
  }

  /* run an async action with a busy button + error toast */
  async function busy(btn, fn) {
    const old = btn ? btn.innerHTML : '';
    if (btn) { btn.classList.add('busy'); btn.disabled = true; btn.setAttribute('aria-busy', 'true'); }
    try { return await fn(); }
    catch (e) { console.error(e); toast((e && e.message) || 'Something went wrong', 'bad', 6000); throw e; }
    finally { if (btn) { btn.classList.remove('busy'); btn.disabled = false; btn.removeAttribute('aria-busy'); btn.innerHTML = old; } }
  }

  /* ---------- theme ---------- */
  function applyTheme(t) {
    if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
    else document.documentElement.removeAttribute('data-theme');
  }
  function currentTheme() {
    const t = document.documentElement.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  try { applyTheme(localStorage.getItem('sb_theme')); } catch (_) { /* ignore */ }

  /* ---------- app shell: top bar + side nav ---------- */
  function navHTML(pageKey) {
    let html = '', group = '';
    PAGES.forEach((p) => {
      if (p.group !== group) { html += `${group ? '</ul>' : ''}<div class="nav-group">${esc(p.group)}</div><ul>`; group = p.group; }
      const href = p.key === 'showcase' ? p.href : link(p.href);
      html += `<li><a href="${href}" ${p.key === pageKey ? 'aria-current="page"' : ''}>${ic(p.icon)}<span>${p.label}</span>${p.count ? '<span class="nav-count" data-nav-count hidden></span>' : ''}${p.ext ? '<span class="sr-only"> (opens the 3D page)</span>' : ''}</a></li>`;
    });
    return html + '</ul>';
  }
  function themeIcon() { return ic(currentTheme() === 'dark' ? 'sun' : 'moon'); }

  function renderHeader(pageKey) {
    const host = $('#app-header');
    if (!host) return;
    document.body.classList.add('shell');
    host.className = 'app-header';
    host.innerHTML = `<div class="bar">
      <a class="skip-link" href="#main">Skip to content</a>
      <a class="logo" href="${link('index.html')}" aria-label="SpiroBuddy – dashboard">${LOGO}<span class="logo-name">SpiroBuddy</span></a>
      <span class="site" title="Demo hospital – fake patients only">${ic('hospital', { size: 16 })}<span class="site-h">${esc(SITE.hospital)}</span><span class="site-w">${esc(SITE.ward)}</span></span>
      <span class="chip chip-demo" title="Demo mode – fake patients only, no real health data">${ic('flask', { size: 14 })}Demo mode</span>
      <div class="header-right">
        <details class="sys" id="sys">
          <summary title="System status"><span class="sys-dot" id="sys-dot"></span><span class="sys-txt" id="sys-txt">Connecting…</span>${ic('chevron-down', { size: 14 })}</summary>
          <div class="sys-pop" role="group" aria-label="System status"><div class="health" id="health-chips"></div>
            <p class="sys-note">Every AI and messaging feature has an offline fallback. Fallbacks are labelled.</p></div>
        </details>
        <span class="clock" id="ist-clock" title="India Standard Time">${ic('clock', { size: 16 })}<span id="ist-time">${istClock()}</span></span>
        <button class="icon-btn" id="theme-btn" type="button" aria-label="Switch light or dark theme" title="Light / dark theme">${themeIcon()}</button>
      </div></div>`;
    $('#theme-btn').addEventListener('click', () => {
      const next = currentTheme() === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('sb_theme', next); } catch (_) { /* ignore */ }
      $('#theme-btn').innerHTML = themeIcon();
    });
    document.addEventListener('click', (e) => { const d = $('#sys'); if (d && d.open && !d.contains(e.target)) d.open = false; });
    document.addEventListener('keydown', (e) => { const d = $('#sys'); if (e.key === 'Escape' && d && d.open) { d.open = false; d.querySelector('summary').focus(); } });
    setInterval(() => { const t = $('#ist-time'); if (t) t.textContent = istClock(); }, 15000);

    const nav = document.createElement('nav');
    nav.className = 'side-nav';
    nav.id = 'side-nav';
    nav.setAttribute('aria-label', 'Main');
    nav.innerHTML = navHTML(pageKey) + `<div class="nav-foot">${ic('info', { size: 14 })}<span>Fake patients only. SpiroBuddy coaches and summarises – it never diagnoses.</span></div>`;
    host.after(nav);
    const bw = document.createElement('div');
    bw.className = 'banner-wrap';
    bw.id = 'banner-wrap';
    nav.after(bw);
    const main = $('main');
    if (main && !main.id) main.id = 'main';
    if (main) main.setAttribute('tabindex', '-1');
    // open-alert count next to "Alerts" in the nav (counts come from comms.js)
    document.addEventListener('sb:alert-counts', (e) => {
      const n = (e.detail && e.detail.open) || 0;
      $$('[data-nav-count]').forEach((el) => { el.hidden = !n; el.textContent = n; el.classList.toggle('red', ((e.detail && e.detail.red) || 0) > 0); });
    });
    hydrateIcons(document);
  }

  function renderHealth(state) {
    const box = $('#health-chips');
    if (!box) return;
    const h = state.health || {};
    const chips = [];
    if (state.mock) chips.push(['warn', 'Data: built-in demo', 'Built-in demo data in this browser – the server is not used']);
    else if (state.online === false) chips.push(['bad', 'Server offline', 'Cannot reach the API']);
    else chips.push(['ok', 'Data: ' + (h.data_backend === 'supabase' ? 'Supabase' : 'Demo DB'), h.data_backend === 'supabase' ? 'Postgres on Supabase' : 'Local SQLite demo store']);
    chips.push([h.model_loaded ? 'ok' : 'warn', 'ML: ' + (h.model_loaded ? 'trained model' : 'rules'), h.model_loaded ? 'Trained ML model is loaded' : 'No model file – using rule fallback']);
    chips.push([h.llm_enabled ? 'ok' : 'warn', 'AI: ' + (h.llm_enabled ? 'Claude' : 'template'), h.llm_enabled ? 'AI summaries by Claude' : 'No API key – template summaries']);
    chips.push([h.whatsapp_enabled ? 'ok' : 'warn', 'WhatsApp: ' + (h.whatsapp_enabled ? 'live' : 'dry run'), h.whatsapp_enabled ? 'Messages are really sent (Twilio)' : 'Messages are logged as "would send"']);
    const WORD = { ok: 'OK', warn: 'Fallback', bad: 'Down' };
    box.innerHTML = chips.map(([k, t, title]) => `<div class="sys-row ${k}"><span class="dot"></span><span class="sys-name">${esc(t)}</span><span class="sys-state">${WORD[k]}</span><span class="sys-why">${esc(title)}</span></div>`).join('');
    const bad = chips.filter((c) => c[0] === 'bad').length, warn = chips.filter((c) => c[0] === 'warn').length;
    const dot = $('#sys-dot'), txt = $('#sys-txt');
    if (dot) dot.className = 'sys-dot ' + (bad ? 'bad' : warn ? 'warn' : 'ok');
    if (txt) txt.textContent = bad ? 'Server offline' : warn ? `${warn} fallback${warn === 1 ? '' : 's'} on` : 'All systems live';
  }

  function renderBanner(state) {
    const bw = $('#banner-wrap');
    if (!bw) return;
    let html = '';
    if (state.forcedMock) {
      html = `<div class="banner mock" role="status">${ic('flask')}<span><b>Mock mode</b> – showing built-in demo data; the server is not used.</span><a class="btn sm" href="${location.pathname}">Use live server</a></div>`;
    } else if (state.mock) {
      html = `<div class="banner offline" role="alert">${ic('wifi-off')}<span><b>Server offline</b> – showing built-in demo data. Start it with <span class="mono">scripts\\run.ps1</span>.</span>
        ${state.serverBack ? '<button class="btn sm primary" id="go-live" type="button">Server is back – switch to live</button>' : '<button class="btn sm" id="go-live" type="button">Retry now</button>'}</div>`;
    } else if (state.online === false) {
      html = `<div class="banner offline" role="alert">${ic('wifi-off')}<span><b>Server offline</b> – showing last data. Retrying every 2 s…</span></div>`;
    }
    if (bw.dataset.html === html) return;
    bw.dataset.html = html;
    bw.innerHTML = html;
    const b = $('#go-live');
    if (b) b.addEventListener('click', () => location.reload());
  }

  async function boot(pageKey) {
    renderHeader(pageKey);
    SB.api.onChange((s) => { renderHealth(s); renderBanner(s); });
    await SB.api.init();
    return SB.api.state;
  }

  /* simple poller that never overlaps; slows down (x5) while the tab is hidden */
  function poll(fn, ms) {
    let stopped = false, running = false, timer = null;
    async function tick() {
      if (stopped) return;
      clearTimeout(timer);
      if (!running) {
        running = true;
        try { await fn(); } catch (e) { /* banner shows offline state */ if (!(e instanceof SB.api.ApiError)) console.error(e); }
        running = false;
      }
      timer = setTimeout(tick, document.hidden ? ms * 5 : ms);
    }
    document.addEventListener('visibilitychange', () => { if (!document.hidden && !running) tick(); });
    tick();
    return () => { stopped = true; clearTimeout(timer); };
  }

  SB.ui = { esc, $, $$, link, ic, hydrateIcons, hourLabel, hourRange, TREND_LABEL, timeLabel, dateTimeLabel, ago, istClock, istDate, initials, statusPill, redFlagPill, STATUS_ICON, trendHTML, normTrend, STATUS_RANK, STATUS_TEXT, LANG, LABEL_TEXT, labelChips, fmtMl, meter, toast, busy, boot, poll, LOGO, SITE };
})();
