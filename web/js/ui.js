/* SpiroBuddy – shared UI: header, nav, health chips, banners, theme, toasts, helpers. */
(function () {
  const SB = (window.SB = window.SB || {});

  const LOGO = `<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0b6e8a"/>
    <rect x="9" y="6" width="6" height="20" rx="3" fill="#fff" opacity=".35"/><rect x="9" y="13" width="6" height="13" rx="3" fill="#fff"/>
    <path d="M19 12c3 0 3 4 6 4M19 18c3 0 3 4 6 4" stroke="#7fe0c8" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>`;

  const PAGES = [
    { href: 'index.html', label: 'Dashboard', key: 'dashboard' },
    { href: 'demo.html', label: 'Demo panel', key: 'demo' },
    { href: 'collect.html', label: 'Record breaths', key: 'collect' },
    { href: 'showcase/', label: '3D showroom', key: 'showcase' },
  ];

  /* ---------- helpers ---------- */
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  function link(href) {
    // keep ?mock=1 when it was forced, so navigation stays in mock mode
    if (SB.api && SB.api.state.forcedMock && !/^https?:/.test(href)) return href + (href.includes('?') ? '&' : '?') + 'mock=1';
    return href;
  }
  function hourLabel(h) { return String(h).padStart(2, '0') + ':00'; }
  function parseDate(v) { if (!v) return null; const d = new Date(v); return isNaN(d) ? null : d; }
  function timeLabel(v) { const d = parseDate(v); return d ? d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '—'; }
  function dateTimeLabel(v) {
    const d = parseDate(v); if (!d) return '—';
    const today = new Date().toDateString() === d.toDateString();
    return today ? 'Today ' + timeLabel(d) : d.toLocaleDateString([], { day: 'numeric', month: 'short' }) + ' ' + timeLabel(d);
  }
  function ago(v) {
    const d = parseDate(v); if (!d) return 'no sessions yet';
    const s = Math.round((Date.now() - d.getTime()) / 1000);
    if (s < 45) return 'just now';
    if (s < 3600) return Math.round(s / 60) + ' min ago';
    if (s < 86400) return Math.round(s / 3600) + ' h ago';
    return Math.round(s / 86400) + ' d ago';
  }
  function initials(name) { return String(name || '?').split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join(''); }
  const STATUS_TEXT = { red: 'Needs a call', yellow: 'Watch', green: 'On track' };
  const STATUS_RANK = { red: 0, yellow: 1, green: 2 };
  function statusPill(status) { const s = STATUS_TEXT[status] ? status : 'green'; return `<span class="status-pill status-${s}">${STATUS_TEXT[s]}</span>`; }
  function normTrend(t) {
    if (typeof t === 'number') return t > 0.02 ? 'up' : t < -0.02 ? 'down' : 'flat';
    const s = String(t || '').toLowerCase();
    if (['up', 'improving', 'rising', '+', 'better'].includes(s)) return 'up';
    if (['down', 'worse', 'falling', 'declining', '-'].includes(s)) return 'down';
    return 'flat';
  }
  function trendHTML(t) {
    const n = normTrend(t);
    return n === 'up' ? '<span class="trend-up" title="Improving">▲ Improving</span>' : n === 'down' ? '<span class="trend-down" title="Getting worse">▼ Falling</span>' : '<span class="trend-flat" title="Steady">→ Steady</span>';
  }
  const LANG = { en: 'English', hi: 'Hindi', ta: 'Tamil' };
  const LABEL_TEXT = { good: 'Good', too_fast: 'Too fast', too_shallow: 'Too shallow', no_hold: 'No hold' };
  function labelChips(counts) {
    if (!counts) return '—';
    return Object.keys(LABEL_TEXT).filter((k) => counts[k]).map((k) => `<span class="lbl-chip lbl-${k}">${LABEL_TEXT[k]} ${counts[k]}</span>`).join('') || '—';
  }
  function fmtMl(v) { return v == null || v === '' || Number(v) === 0 ? '—' : Math.round(Number(v)).toLocaleString() + ' mL'; }

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

  /* ---------- header ---------- */
  function renderHeader(pageKey) {
    const host = $('#app-header');
    if (!host) return;
    host.className = 'app-header';
    host.innerHTML = `<div class="bar">
      <a class="logo" href="${link('index.html')}">${LOGO}<span>SpiroBuddy<span class="sub">Nurse &amp; doctor</span></span></a>
      <span class="badge-demo" title="Fake patients only – no real health data">DEMO</span>
      <nav class="nav" aria-label="Main">${PAGES.map((p) => `<a href="${p.key === 'showcase' ? p.href : link(p.href)}" ${p.key === pageKey ? 'aria-current="page"' : ''}>${p.label}</a>`).join('')}</nav>
      <div class="header-right">
        <div class="health" id="health-chips" aria-label="System status"><span class="chip"><span class="dot"></span>Connecting…</span></div>
        <button class="icon-btn" id="theme-btn" type="button" aria-label="Switch light/dark theme" title="Light / dark theme">◐</button>
      </div></div>`;
    $('#theme-btn').addEventListener('click', () => {
      const next = currentTheme() === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('sb_theme', next); } catch (_) { /* ignore */ }
    });
    const bw = document.createElement('div');
    bw.className = 'banner-wrap';
    bw.id = 'banner-wrap';
    host.after(bw);
  }

  function renderHealth(state) {
    const box = $('#health-chips');
    if (!box) return;
    const h = state.health || {};
    const chips = [];
    if (state.mock) chips.push(['warn', 'Data: MOCK', 'Built-in demo data in this browser – the server is not used']);
    else if (state.online === false) chips.push(['bad', 'Server offline', 'Cannot reach the API']);
    else chips.push(['ok', 'Data: ' + (h.data_backend === 'supabase' ? 'Supabase' : 'Demo DB'), h.data_backend === 'supabase' ? 'Postgres on Supabase' : 'Local SQLite demo store']);
    chips.push([h.model_loaded ? 'ok' : 'warn', 'ML: ' + (h.model_loaded ? 'model' : 'rules'), h.model_loaded ? 'Trained ML model is loaded' : 'No model file – using rule fallback']);
    chips.push([h.llm_enabled ? 'ok' : 'warn', 'AI: ' + (h.llm_enabled ? 'Claude' : 'template'), h.llm_enabled ? 'AI summaries by Claude' : 'No API key – template summaries']);
    chips.push([h.whatsapp_enabled ? 'ok' : 'warn', 'WhatsApp: ' + (h.whatsapp_enabled ? 'live' : 'dry run'), h.whatsapp_enabled ? 'Messages are really sent (Twilio)' : 'Messages are logged as "would send"']);
    box.innerHTML = chips.map(([k, t, title]) => `<span class="chip ${k}" title="${esc(title)}"><span class="dot"></span>${esc(t)}</span>`).join('');
  }

  function renderBanner(state) {
    const bw = $('#banner-wrap');
    if (!bw) return;
    let html = '';
    if (state.forcedMock) {
      html = `<div class="banner mock" role="status">MOCK MODE – showing built-in demo data (the server is not used). <a class="btn sm" href="${location.pathname}">Use live server</a></div>`;
    } else if (state.mock) {
      html = `<div class="banner offline" role="alert">⚠ Server offline – showing built-in demo data (mock mode). Start it with <span class="mono">scripts\\run.ps1</span>.
        ${state.serverBack ? '<button class="btn sm primary" id="go-live">Server is back – switch to live</button>' : '<button class="btn sm" id="go-live">Retry now</button>'}</div>`;
    } else if (state.online === false) {
      html = `<div class="banner offline" role="alert">⚠ Server offline – lost connection to the API. Retrying every 2 s… (data shown may be out of date)</div>`;
    }
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

  SB.ui = { esc, $, $$, link, hourLabel, timeLabel, dateTimeLabel, ago, initials, statusPill, trendHTML, normTrend, STATUS_RANK, STATUS_TEXT, LANG, LABEL_TEXT, labelChips, fmtMl, toast, busy, boot, poll, LOGO };
})();
