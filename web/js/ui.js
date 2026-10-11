/* SpiroBuddy – shared UI: app shell (top bar, side nav, system status, IST clock), banners, theme, toasts, helpers.
 * Optional: js/icons.js (loaded first) for line icons. If a page doesn't load it, ui.js loads it itself
 * and fills every <span data-icon="…"> when it arrives.
 * 2.0: pages under /hospital/ get a role-aware shell (REBUILD_PLAN §3.11): nav by role and permission, the
 * user's name/role/hospital with Logout, the "Fake patients only" ribbon in DEMO_MODE and the red
 * "Database update needed" banner. Feature status badges (SB.ui.badge / plannedCard) come from /api/features. */
(function () {
  const SB = (window.SB = window.SB || {});

  const LOGO = `<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0b6e8a"/>
    <rect x="9" y="6" width="6" height="20" rx="3" fill="#fff" opacity=".35"/><rect x="9" y="13" width="6" height="13" rx="3" fill="#fff"/>
    <path d="M19 12c3 0 3 4 6 4M19 18c3 0 3 4 6 4" stroke="#7fe0c8" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>`;

  /* Demo site identity shown in the top bar (fake hospital – demo only). */
  const SITE = { hospital: 'Demo City Hospital', ward: 'Post-op Ward 3B' };

  const PAGES = [
    { group: 'Ward', href: 'dashboard.html', label: 'Dashboard', key: 'dashboard', icon: 'dashboard' },
    { group: 'Ward', href: 'dashboard.html#alerts', label: 'Alerts', key: 'alerts', icon: 'bell', count: true },
    { group: 'Ward', href: 'dashboard.html#patients-card', label: 'Patients', key: 'patient', icon: 'users' },
    { group: 'Ward', href: 'units.html', label: 'Units', key: 'units', icon: 'database' },
    { group: 'Tools', href: 'demo.html', label: 'Demo panel', key: 'demo', icon: 'sliders' },
    { group: 'Tools', href: 'collect.html', label: 'Record breaths', key: 'collect', icon: 'activity' },
    { group: 'Tools', href: 'showcase/', label: '3D showroom', key: 'showcase', icon: 'cube', ext: true },
  ];

  /* 2.0 hospital nav (REBUILD_PLAN §3.11). roles = who sees it among admin/doctor (none = both).
   * nurse: true = every nurse, a permission name = only nurses holding it, missing = no nurse. demo = DEMO_MODE only. */
  const HOSP_NAV = [
    { group: 'Care', key: 'home', href: '/hospital/index.html', label: 'Home', icon: 'dashboard', nurse: true },
    { group: 'Care', key: 'patients', href: '/hospital/patients.html', label: 'Patients', icon: 'users', nurse: true },
    { group: 'Care', key: 'review', href: '/hospital/review.html', label: 'Prescription review', icon: 'pill', nurse: 'confirm_prescriptions' },
    { group: 'Care', key: 'appointments', href: '/hospital/appointments.html', label: 'Appointments', icon: 'calendar', nurse: 'manage_appointments' },
    { group: 'Care', key: 'availability', href: '/hospital/availability.html', label: 'Availability', icon: 'clock' },
    { group: 'Hospital', key: 'keys', href: '/hospital/keys.html', label: 'Nurse keys', icon: 'key' },
    { group: 'Hospital', key: 'staff', href: '/hospital/staff.html', label: 'Staff', icon: 'user-check', roles: ['admin'] },
    { group: 'Hospital', key: 'devices', href: '/hospital/devices.html', label: 'Devices', icon: 'cpu', nurse: true },
    { group: 'Hospital', key: 'settings', href: '/hospital/settings.html', label: 'Settings', icon: 'settings', roles: ['admin'] },
    { group: 'Hospital', key: 'governance', href: '/hospital/governance.html', label: 'Governance', icon: 'shield' },
    { group: 'Demo', key: 'demo', href: '/hospital/demo.html', label: 'Demo controls', icon: 'sliders', demo: true },
  ];
  const ROLE_TEXT = { admin: 'Admin', doctor: 'Doctor', nurse: 'Nurse' };

  /* Icons the 2.0 screens need that icons.js doesn't have yet (same 24 px grid, 2 px stroke). */
  const EXTRA_ICONS = {
    key: '<path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.78 7.78 5.5 5.5 0 0 1 7.78-7.78zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>',
    lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'log-out': '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
    'log-in': '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>',
    copy: '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>',
    file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
    pill: '<path d="M10.5 20.5l10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7z"/><path d="M8.5 8.5l7 7"/>',
    upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
    cpu: '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
    mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22 6 12 13 2 6"/>',
    'eye-off': '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>',
  };
  function addIcons() { if (SB.icons) Object.keys(EXTRA_ICONS).forEach((k) => { if (!SB.icons[k]) SB.icons[k] = EXTRA_ICONS[k]; }); }
  addIcons();

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
    s.onload = () => { addIcons(); hydrateIcons(document); };
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
  /* DD/MM/YYYY in India time, and the "Edited by … at …" line under an inline edit (.ie-meta). */
  function dmy(v) { const d = parseDate(v); return d ? d.toLocaleDateString('en-GB', { timeZone: 'Asia/Kolkata', day: '2-digit', month: '2-digit', year: 'numeric' }) : '—'; }
  function editedMeta(by, at) {
    const d = parseDate(at);
    const when = d ? dmy(d) + ', ' + d.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: 'numeric', minute: '2-digit', hour12: true }) : '';
    return `<p class="ie-meta">${ic('edit', { size: 14 })}<span>Edited${by ? ' by ' + esc(by) : ''}${when ? ' at ' + esc(when) : ''}</span></p>`;
  }

  /* ---------- roles and permissions (display only – the server decides; authz.py is the real check) ---------- */
  // me.permissions_summary may be a list of nurse permission names, an object {permissions:[…]} or {perm: true}.
  function hasPerm(me, perm) {
    if (!me) return false;
    if (me.role === 'admin' || me.role === 'doctor') return true;
    const s = me.permissions_summary, lists = [];
    if (Array.isArray(s)) lists.push(s);
    else if (s && typeof s === 'object') {
      if (Array.isArray(s.permissions)) lists.push(s.permissions);
      if (s[perm] === true || Number(s[perm]) > 0) return true;
    }
    (me.grants || []).forEach((g) => { if (g && Array.isArray(g.permissions)) lists.push(g.permissions); });
    return lists.some((l) => l.indexOf(perm) >= 0);
  }
  function navAllowed(item, me, demo) {
    if (item.demo && !demo) return false;
    const role = me && me.role;
    if (!role) return item.key === 'home' || item.key === 'patients';      // login unknown (server error): the basics only
    if (role === 'nurse') return item.nurse === true || (typeof item.nurse === 'string' && hasPerm(me, item.nurse));
    return !item.roles || item.roles.indexOf(role) >= 0;
  }

  /* ---------- feature status badges (/api/features, fetched once per page) ----------
   * SB.ui.badge(key) -> '<span class="fbadge live">✓ Live</span>' (icon + word, never colour alone).
   * SB.ui.plannedCard(key) -> a disabled card (not clickable) with the badge, the feature name and its note.
   * Called before the list arrives, both return a placeholder that fills itself in. In HTML you can also write
   * a span with the attribute data-feature (value = the feature key), or a div with data-feature plus
   * data-fkind="card" for a Planned card; boot() fills them. (No literal example here on purpose: the feature
   * test greps web/ for that attribute and checks every key against the registry – see DESIGN_SYSTEM.md §10.) */
  const FSTATUS = {
    live: { word: 'Live', icon: 'check-circle' },
    simulated: { word: 'Simulated', icon: 'flask' },
    in_development: { word: 'In development', icon: 'hourglass' },
    planned: { word: 'Planned', icon: 'calendar' },
  };
  const FEAT = {};
  const FKEY = 'data-fkey';                     // placeholder attribute (pages use data-feature; see above)
  let featP = null, featReady = false;
  function featureCache() { try { return JSON.parse(localStorage.getItem('sb_features_cache') || 'null'); } catch (_) { return null; } }
  function loadFeatures() {
    if (featP) return featP;
    featP = SB.api.get('/api/features')
      .then((r) => {
        const list = Array.isArray(r) ? r : (r && Array.isArray(r.features) ? r.features : []);
        if (list.length && !SB.api.state.mock) { try { localStorage.setItem('sb_features_cache', JSON.stringify(list)); } catch (_) { /* private mode */ } }
        return list.length ? list : (featureCache() || []);
      })
      .catch((e) => { console.warn('[SpiroBuddy] /api/features failed – using the last saved list', e && e.message); return featureCache() || []; })
      .then((list) => {
        list.forEach((f) => { if (f && f.key) FEAT[f.key] = f; });
        featReady = true;
        hydrateBadges(document);
        return list;
      });
    return featP;
  }
  function humanize(key) { const s = String(key || '').replace(/[_-]+/g, ' ').trim(); return s ? s[0].toUpperCase() + s.slice(1) : 'Feature'; }
  function featureOf(key) {
    const f = FEAT[key];
    if (!f || !FSTATUS[f.status]) console.warn(`[SpiroBuddy] feature "${key}" is not in /api/features – showing "Planned"`);
    return f || null;
  }
  function badgeHTML(key, f) {
    const st = f && FSTATUS[f.status] ? f.status : 'planned';
    const s = FSTATUS[st];
    const tip = `${(f && f.name) || humanize(key)}: ${s.word}${f && f.note ? ' – ' + f.note : ''}`;
    return `<span class="fbadge ${st}" title="${esc(tip)}">${ic(s.icon, { size: 14 })}${s.word}</span>`;
  }
  function plannedCardHTML(key, f) {
    const name = (f && f.name) || humanize(key);
    const st = f && FSTATUS[f.status] ? f.status : 'planned';
    return `<div class="planned-card" role="group" aria-disabled="true" aria-label="${esc(name)} – ${FSTATUS[st].word}">
      <div class="pc-head"><span class="pc-name">${esc(name)}</span>${badgeHTML(key, f)}</div>
      ${f && f.note ? `<p class="pc-note">${esc(f.note)}</p>` : '<p class="pc-note">Not available yet.</p>'}</div>`;
  }
  function badge(key) {
    if (featReady) return badgeHTML(key, featureOf(key));
    loadFeatures();
    return `<span class="fbadge pending" ${FKEY}="${esc(key)}" data-fkind="badge"><span class="sr-only">Checking status…</span></span>`;
  }
  function plannedCard(key) {
    if (featReady) return plannedCardHTML(key, featureOf(key));
    loadFeatures();
    return `<div class="planned-card pending" ${FKEY}="${esc(key)}" data-fkind="card" aria-busy="true"><span class="skeleton" style="width:60%"></span><span class="skeleton" style="width:90%"></span></div>`;
  }
  /* fill placeholders and elements that carry data-feature (call again after you render new HTML) */
  function hydrateBadges(root) {
    const els = $$('[' + FKEY + '], [data-feature]', root);
    if (!els.length) return;
    if (!featReady) { loadFeatures(); return; }
    els.forEach((el) => {
      const key = el.getAttribute(FKEY) || el.getAttribute('data-feature');
      const card = el.getAttribute('data-fkind') === 'card';
      const f = featureOf(key);
      try { el.outerHTML = card ? plannedCardHTML(key, f) : badgeHTML(key, f); } catch (_) { /* detached element */ }
    });
  }

  /* ---------- "Fake patients only" ribbon ----------
   * Hospital pages get it from boot(). The patient app and the family page call SB.ui.fakeRibbon() – optional
   * {text, into, large} (e.g. a Hindi text, a container, large: true for the patient-size ribbon) – which checks
   * /api/health and only shows it in DEMO_MODE. */
  function fakeRibbonHTML(text, large) {
    return `<div class="ribbon-fake${large ? ' lg' : ''}" role="note">${ic('flask', { size: large ? 20 : 14 })}<span>${esc(text || 'Fake patients only · demo')}</span></div>`;
  }
  async function fakeRibbon(opts) {
    opts = opts || {};
    let h = SB.api && SB.api.state.health;
    if (!h && SB.api) { try { h = await SB.api.health(); } catch (_) { h = null; } }
    if (!h || !h.demo_mode) return null;
    const host = typeof opts.into === 'string' ? $(opts.into) : (opts.into || document.body);
    if (!host) return null;
    const old = $('.ribbon-fake', host);
    if (old) return old;
    host.insertAdjacentHTML('afterbegin', fakeRibbonHTML(opts.text, opts.large));
    const el = $('.ribbon-fake', host);
    hydrateIcons(el);
    return el;
  }

  /* ---------- shown-once secret (nurse key, join code, temp password) ----------
   * SB.ui.keyReveal(secret, {label, note}) -> HTML; the Copy button works by itself (one listener below). */
  function keyReveal(secret, opts) {
    opts = opts || {};
    return `<div class="key-reveal" role="group" aria-label="${esc(opts.label || 'New key')}">
      <div class="kr-label">${ic('key', { size: 16 })}${esc(opts.label || 'New key')}</div>
      <div class="kr-row"><code class="kr-code">${esc(secret)}</code>
        <button class="btn sm kr-copy" type="button">${ic('copy', { size: 16 })}<span>Copy</span></button></div>
      <p class="kr-note">${ic('alert-triangle', { size: 14 })}<span>${esc(opts.note || 'Shown only once. Copy it now – it cannot be shown again.')}</span></p></div>`;
  }
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest && e.target.closest('.kr-copy');
    if (!btn) return;
    const code = btn.closest('.key-reveal') && btn.closest('.key-reveal').querySelector('.kr-code');
    if (!code) return;
    let ok = false;
    try { await navigator.clipboard.writeText(code.textContent); ok = true; } catch (_) {
      try { const r = document.createRange(); r.selectNodeContents(code); const s = getSelection(); s.removeAllRanges(); s.addRange(r); ok = document.execCommand('copy'); } catch (__) { ok = false; }
    }
    const span = btn.querySelector('span');
    if (span) span.textContent = ok ? 'Copied' : 'Select and copy';
    btn.classList.toggle('done', ok);
    setTimeout(() => { if (span) span.textContent = 'Copy'; btn.classList.remove('done'); }, 2500);
  });

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
  const isHospitalPage = () => location.pathname === '/hospital' || location.pathname.indexOf('/hospital/') === 0;
  let unauthorized = false;   // a 401 on a page that doesn't redirect (old dashboard at /): show a "Log in" banner

  function navHTML(pageKey) {
    let html = '', group = '';
    PAGES.forEach((p) => {
      if (p.group !== group) { html += `${group ? '</ul>' : ''}<div class="nav-group">${esc(p.group)}</div><ul>`; group = p.group; }
      const href = p.key === 'showcase' ? p.href : link(p.href);
      html += `<li><a href="${href}" ${p.key === pageKey ? 'aria-current="page"' : ''}>${ic(p.icon)}<span>${p.label}</span>${p.count ? '<span class="nav-count" data-nav-count hidden></span>' : ''}${p.ext ? '<span class="sr-only"> (opens the 3D page)</span>' : ''}</a></li>`;
    });
    return html + '</ul>';
  }
  function hospNavHTML(pageKey, me, demo) {
    let html = '', group = '';
    HOSP_NAV.filter((p) => navAllowed(p, me, demo)).forEach((p) => {
      if (p.group !== group) { html += `${group ? '</ul>' : ''}<div class="nav-group">${esc(p.group)}</div><ul>`; group = p.group; }
      html += `<li><a href="${link(p.href)}" ${p.key === pageKey ? 'aria-current="page"' : ''}>${ic(p.icon)}<span>${esc(p.label)}</span></a></li>`;
    });
    return html + (group ? '</ul>' : '');
  }
  const NAV_FOOT = `<div class="nav-foot">${ic('info', { size: 14 })}<span>Fake patients only. SpiroBuddy coaches and summarises – it never diagnoses.</span></div>`;
  function themeIcon() { return ic(currentTheme() === 'dark' ? 'sun' : 'moon'); }
  function closeOnOutside(id) {
    document.addEventListener('click', (e) => { const d = $('#' + id); if (d && d.open && !d.contains(e.target)) d.open = false; });
    document.addEventListener('keydown', (e) => { const d = $('#' + id); if (e.key === 'Escape' && d && d.open) { d.open = false; d.querySelector('summary').focus(); } });
  }

  function renderHeader(pageKey, hosp) {
    const host = $('#app-header');
    if (!host) return;
    document.body.classList.add('shell');
    if (hosp) document.body.classList.add('hosp');
    host.className = 'app-header';
    const site = hosp
      ? `<span class="site" title="Your hospital – fake patients only">${ic('hospital', { size: 16 })}<span class="site-h" id="site-h">…</span></span>`
      : `<span class="site" title="Demo hospital – fake patients only">${ic('hospital', { size: 16 })}<span class="site-h">${esc(SITE.hospital)}</span><span class="site-w">${esc(SITE.ward)}</span></span>
      <span class="chip chip-demo" title="Demo mode – fake patients only, no real health data">${ic('flask', { size: 14 })}Demo mode</span>`;
    host.innerHTML = `<div class="bar">
      <a class="skip-link" href="#main">Skip to content</a>
      <a class="logo" href="${link(hosp ? '/hospital/index.html' : 'dashboard.html')}" aria-label="SpiroBuddy – ${hosp ? 'hospital home' : 'dashboard'}">${LOGO}<span class="logo-name">SpiroBuddy</span></a>
      ${site}
      <div class="header-right">
        <details class="sys" id="sys">
          <summary title="System status"><span class="sys-dot" id="sys-dot"></span><span class="sys-txt" id="sys-txt">Connecting…</span>${ic('chevron-down', { size: 14 })}</summary>
          <div class="sys-pop" role="group" aria-label="System status"><div class="health" id="health-chips"></div>
            <p class="sys-note">Every AI and messaging feature has an offline fallback. Fallbacks are labelled.</p></div>
        </details>
        <span class="clock" id="ist-clock" title="India Standard Time">${ic('clock', { size: 16 })}<span id="ist-time">${istClock()}</span></span>
        <button class="icon-btn" id="theme-btn" type="button" aria-label="Switch light or dark theme" title="Light / dark theme">${themeIcon()}</button>
        ${hosp ? '<div class="user-slot" id="user-slot"><span class="skeleton um-skel"></span></div>' : ''}
      </div></div>${hosp ? '<div id="ribbon-slot"></div>' : ''}`;
    $('#theme-btn').addEventListener('click', () => {
      const next = currentTheme() === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('sb_theme', next); } catch (_) { /* ignore */ }
      $('#theme-btn').innerHTML = themeIcon();
    });
    closeOnOutside('sys');
    if (hosp) closeOnOutside('user-menu');
    setInterval(() => { const t = $('#ist-time'); if (t) t.textContent = istClock(); }, 15000);

    const nav = document.createElement('nav');
    nav.className = 'side-nav';
    nav.id = 'side-nav';
    nav.setAttribute('aria-label', 'Main');
    // hospital pages: the nav depends on who is logged in, so it fills in after /api/auth/me
    nav.innerHTML = (hosp ? '<ul class="nav-skel" aria-hidden="true"><li><span class="skeleton"></span></li><li><span class="skeleton"></span></li><li><span class="skeleton"></span></li></ul>' : navHTML(pageKey)) + NAV_FOOT;
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
    // api.js fires this on a 401 when the page is not on the login allow-list (e.g. the old dashboard at /)
    document.addEventListener('sb:unauthorized', () => { if (!unauthorized) { unauthorized = true; renderBanner(SB.api.state); } });
    hydrateIcons(document);
  }

  /* hospital pages, after /api/auth/me: nav by role, user menu with Logout, hospital name, ribbon */
  function renderHospitalShell(pageKey, me, demo, loginError) {
    const nav = $('#side-nav');
    if (nav) nav.innerHTML = hospNavHTML(pageKey, me, demo) + NAV_FOOT;
    const siteH = $('#site-h');
    if (siteH) siteH.textContent = (me && me.hospital && me.hospital.name) || 'Hospital';
    const slot = $('#user-slot');
    if (slot) {
      if (me) {
        const role = ROLE_TEXT[me.role] || humanize(me.role);
        const hospName = (me.hospital && me.hospital.name) || '';
        slot.innerHTML = `<details class="user-menu" id="user-menu">
          <summary title="Your account"><span class="um-avatar" aria-hidden="true">${esc(initials(me.name))}</span>
            <span class="um-text"><span class="um-name">${esc(me.name)}</span><span class="um-role">${esc(role)}</span></span>${ic('chevron-down', { size: 14 })}</summary>
          <div class="um-pop" role="group" aria-label="Your account">
            <div class="um-who"><b>${esc(me.name)}</b><span>${esc(role)}${hospName ? ' · ' + esc(hospName) : ''}</span>${me.department ? `<span class="subtle">${esc(me.department)}</span>` : ''}${me.email ? `<span class="subtle">${esc(me.email)}</span>` : ''}</div>
            <button class="btn sm um-logout" id="logout-btn" type="button">${ic('log-out', { size: 16 })}Log out</button>
          </div></details>`;
        $('#logout-btn').addEventListener('click', (e) => busy(e.currentTarget, () => SB.auth.logout()));
      } else {
        const next = encodeURIComponent(location.pathname + location.search);
        slot.innerHTML = `<a class="btn sm" href="/login.html?next=${next}">${ic('log-in', { size: 16 })}Log in</a>`;
      }
    }
    const rib = $('#ribbon-slot');
    if (rib) rib.innerHTML = demo ? fakeRibbonHTML() : '';
    document.body.classList.toggle('has-ribbon', !!(rib && demo));   // styles.css: the sticky nav starts below the ribbon
    if (loginError) toast('Could not check your login: ' + loginError, 'bad', 6000);
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
    if (h.v2_missing) chips.push(['warn', 'Database: update needed', 'The 2.0 tables are missing on Supabase – using the demo SQLite store. See SETUP_STEPS.md']);
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
    // 2.0: Supabase is missing the new tables -> the server runs on the demo SQLite store until schema_v2.sql is run
    if (state.health && state.health.v2_missing && !state.mock) {
      html += `<div class="banner db" role="alert">${ic('database')}<span><b>Database update needed</b> – see SETUP_STEPS.md. Until then the demo database is used.</span></div>`;
    }
    if (unauthorized && !state.mock) {
      const next = encodeURIComponent(location.pathname + location.search);
      html += `<div class="banner info" role="status">${ic('lock')}<span><b>Hospital login needed</b> – patient data is shown only to logged-in staff.</span><a class="btn sm primary" href="/login.html?next=${next}">${ic('log-in', { size: 16 })}Log in</a></div>`;
    }
    if (bw.dataset.html === html) return;
    bw.dataset.html = html;
    bw.innerHTML = html;
    const b = $('#go-live');
    if (b) b.addEventListener('click', () => location.reload());
  }

  /* boot(pageKey): builds the shell and starts the API. Old pages (index, patient, demo, units, collect) keep
   * their old shell. Pages under /hospital/ also wait for /api/auth/me: not logged in -> /login.html?next=…
   * (the promise then never resolves, so the page doesn't fire calls while it leaves). SB.ui.me = the user. */
  async function boot(pageKey) {
    const hosp = isHospitalPage();
    renderHeader(pageKey, hosp);
    SB.api.onChange((s) => { renderHealth(s); renderBanner(s); });
    await SB.api.init();
    if (document.querySelector('[data-feature]')) loadFeatures();
    if (!hosp) return SB.api.state;
    const me = await SB.auth.me();
    const staff = !!(me && me.authenticated && me.kind !== 'patient');
    if (!staff && !me.error && SB.auth.loginRedirect('/api/auth/me')) return new Promise(() => {});
    SB.ui.me = staff ? me : null;
    const demo = !!((SB.api.state.health && SB.api.state.health.demo_mode) || (staff && me.demo_mode));
    renderHospitalShell(pageKey, SB.ui.me, demo, me.error);
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

  SB.ui = { esc, $, $$, link, ic, hydrateIcons, hourLabel, hourRange, TREND_LABEL, timeLabel, dateTimeLabel, ago, istClock, istDate, initials, statusPill, redFlagPill, STATUS_ICON, trendHTML, normTrend, STATUS_RANK, STATUS_TEXT, LANG, LABEL_TEXT, labelChips, fmtMl, meter, toast, busy, boot, poll, LOGO, SITE,
    // 2.0 kit
    me: null, ROLE_TEXT, HOSP_NAV, hasPerm, navAllowed, dmy, editedMeta, loadFeatures, badge, plannedCard, hydrateBadges, FSTATUS,
    fakeRibbon, fakeRibbonHTML, keyReveal, applyTheme, currentTheme };
})();
