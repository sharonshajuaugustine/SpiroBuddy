/* SpiroBuddy – API client (CONTRACT D, plus Contract E auth for 2.0) with a built-in MOCK mode.
 * Usage: await SB.api.init(); const list = await SB.api.get('/api/patients');
 * Mock mode turns on with ?mock=1, or automatically when /api/health fails at start-up.
 * 2.0: every non-GET call carries the CSRF header X-SB: 1 (raw fetch() calls in other files too),
 * SB.api.upload() sends multipart forms, SB.auth.* wraps login/logout/me, and a 401 on a staff page
 * sends the user to /login.html once.
 */
(function () {
  const SB = (window.SB = window.SB || {});
  const params = new URLSearchParams(location.search);
  const listeners = new Set();
  const SAFE_METHOD = /^(GET|HEAD|OPTIONS)$/i;

  const state = {
    mock: params.get('mock') === '1',
    forcedMock: params.get('mock') === '1',
    online: null,          // true / false / null (unknown)
    health: null,
    lastError: null,
  };

  function emit() { listeners.forEach((fn) => { try { fn(state); } catch (e) { console.error(e); } }); }

  class ApiError extends Error {
    constructor(status, message, detail) { super(message); this.status = status; this.detail = detail; }
  }

  /* CSRF rule (Contract E): every non-GET request under /api/ needs X-SB: 1. rawFetch adds it; this
   * small wrapper adds it to raw fetch() calls in other scripts (voice.js, comms.js, app.html …) so
   * nobody has to remember. Same-origin /api/ only; a header that is already there is left alone. */
  if (window.fetch && !window.fetch.__sbCsrf) {
    const nativeFetch = window.fetch.bind(window);
    const csrfFetch = function (input, init) {
      try {
        const isReq = typeof Request !== 'undefined' && input instanceof Request;
        const method = String((init && init.method) || (isReq ? input.method : 'GET'));
        if (!SAFE_METHOD.test(method)) {
          const url = new URL(isReq ? input.url : String(input), location.href);
          if (url.origin === location.origin && url.pathname.indexOf('/api/') === 0) {
            const h = new Headers((init && init.headers) || (isReq ? input.headers : undefined));
            if (!h.has('X-SB')) { h.set('X-SB', '1'); init = Object.assign({}, init, { headers: h }); }
          }
        }
      } catch (_) { /* never block a request because of the helper */ }
      return nativeFetch(input, init);
    };
    csrfFetch.__sbCsrf = true;
    window.fetch = csrfFetch;
  }

  /* ---------- login redirect: ONE allow-list ----------
   * Staff-only pages: anything under /hospital/, plus the old staff pages that still exist.
   * Everything else never redirects: / and /index.html (the public landing page from B7 on),
   * app.html, guardian.html, login/signup/redeem, impact/trust/vision/architecture/twin, /showcase/. */
  const STAFF_PAGES = ['/dashboard.html', '/prescribe.html', '/patient.html', '/demo.html', '/units.html', '/collect.html'];
  function needsLogin(pathname) {
    const p = pathname == null ? location.pathname : String(pathname);
    return p === '/hospital' || p.indexOf('/hospital/') === 0 || STAFF_PAGES.indexOf(p) >= 0;
  }
  const NO_REDIRECT_API = /^\/api\/auth\/(login|signup|redeem|password)\b/;   // a 401 here is a form error, not "logged out"
  let redirecting = false;
  function loginRedirect(apiPath) {
    if (redirecting || state.mock || !needsLogin()) return false;
    if (apiPath && NO_REDIRECT_API.test(String(apiPath).split('?')[0])) return false;
    redirecting = true;
    location.assign('/login.html?next=' + encodeURIComponent(location.pathname + location.search + location.hash));
    return true;
  }
  function onUnauthorized(apiPath) {
    if (loginRedirect(apiPath)) return;
    // pages that don't redirect (e.g. the old dashboard at /) can show a "please log in" banner
    try { document.dispatchEvent(new CustomEvent('sb:unauthorized', { detail: { path: apiPath } })); } catch (_) { /* old browser */ }
  }

  async function rawFetch(method, path, body, timeoutMs) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeoutMs || 10000);
    try {
      const opts = { method, signal: ctrl.signal, headers: { Accept: 'application/json' }, cache: 'no-store', credentials: 'same-origin' };
      if (!SAFE_METHOD.test(method)) opts.headers['X-SB'] = '1';
      if (typeof FormData !== 'undefined' && body instanceof FormData) opts.body = body;   // the browser sets the multipart boundary
      else if (body !== undefined) { opts.headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(body); }
      const res = await fetch(path, opts);
      const text = await res.text();
      let data = null;
      try { data = text ? JSON.parse(text) : null; } catch (_) { data = text; }
      if (!res.ok) {
        const msg = (data && (data.detail || data.error || data.message)) || `HTTP ${res.status}`;
        if (res.status === 401) onUnauthorized(path);
        throw new ApiError(res.status, typeof msg === 'string' ? msg : JSON.stringify(msg), data);
      }
      return data;
    } finally { clearTimeout(timer); }
  }

  async function request(method, path, body, opts) {
    if (state.mock) return SB.mock.handle(method, path, body);
    try {
      const data = await rawFetch(method, path, body, opts && opts.timeout);
      if (state.online !== true) { state.online = true; emit(); }
      return data;
    } catch (e) {
      // Network failure / timeout → server offline. HTTP errors (ApiError) mean the server is up.
      if (!(e instanceof ApiError)) {
        state.lastError = e;
        if (state.online !== false) { state.online = false; emit(); }
        throw new ApiError(0, 'Server offline – could not reach ' + path);
      }
      throw e;
    }
  }

  let retryTimer = null;
  function startRetry() {
    if (retryTimer || state.forcedMock) return;
    retryTimer = setInterval(async () => {
      try {
        const h = await rawFetch('GET', '/api/health', undefined, 4000);
        if (h && h.ok !== false) {
          clearInterval(retryTimer); retryTimer = null;
          state.serverBack = true; emit();
        }
      } catch (_) { /* still offline */ }
    }, 8000);
  }

  async function init() {
    if (state.forcedMock) {
      state.health = await SB.mock.handle('GET', '/api/health');
      emit();
      return state;
    }
    try {
      state.health = await rawFetch('GET', '/api/health', undefined, 5000);
      state.online = true;
      state.mock = false;
    } catch (e) {
      console.warn('[SpiroBuddy] /api/health failed – switching to MOCK mode.', e);
      state.online = false;
      state.mock = true;
      state.health = await SB.mock.handle('GET', '/api/health');
      startRetry();
    }
    emit();
    return state;
  }

  async function refreshHealth() {
    try { state.health = await request('GET', '/api/health'); emit(); } catch (_) { /* banner handles it */ }
    return state.health;
  }

  SB.api = {
    state, init, refreshHealth, ApiError,
    onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
    get: (p, o) => request('GET', p, undefined, o),
    post: (p, b, o) => request('POST', p, b === undefined ? {} : b, o),
    put: (p, b, o) => request('PUT', p, b, o),
    del: (p, o) => request('DELETE', p, undefined, o),
    // multipart upload (photos, PDFs): pass a FormData; no Content-Type here, the browser sets the boundary.
    upload: (p, formData, o) => request((o && o.method) || 'POST', p, formData, Object.assign({ timeout: 60000 }, o)),
    needsLogin, loginRedirect,
    // convenience wrappers for CONTRACT D
    health: () => request('GET', '/api/health'),
    patients: () => request('GET', '/api/patients'),
    patient: (id) => request('GET', `/api/patients/${id}`),
    updatePatient: (id, body) => request('PUT', `/api/patients/${id}`, body),
    sessions: (id, limit = 20) => request('GET', `/api/patients/${id}/sessions?limit=${limit}`),
    classify: (features) => request('POST', '/api/classify', features),
    collect: (body) => request('POST', '/api/collect', body),
    train: () => request('POST', '/api/train', {}, { timeout: 180000 }),
    model: () => request('GET', '/api/model'),
    summary: (id, language) => request('POST', `/api/summary/${id}`, language ? { language } : {}, { timeout: 45000 }),
    whatsapp: (id, kind, to) => request('POST', `/api/whatsapp/${id}`, { kind, to }, { timeout: 45000 }),
    messages: (limit = 50) => request('GET', `/api/messages?limit=${limit}`),
    simulate: (id, quality, breaths = 10) => request('POST', `/api/demo/simulate/${id}`, { quality, breaths }, { timeout: 30000 }),
    miss: (id) => request('POST', `/api/demo/miss/${id}`, {}, { timeout: 30000 }),
    reset: () => request('POST', '/api/demo/reset', {}, { timeout: 30000 }),
  };

  /* ---------- SB.auth – Contract E (staff login) ----------
   * me()            -> {authenticated:false} or {authenticated:true, kind, name, role, hospital, …}; one call per
   *                    page (cached promise), me({refresh:true}) asks again. Never throws: a failed call returns
   *                    {authenticated:false, error, status} and is not cached.
   * login(e, p)     -> {ok, me}; throws ApiError (401 wrong password, 403 pending/disabled, 429 locked out).
   * logout()        -> ends the session, then goes to /login.html. */
  let meP = null;
  function setMe(me) {
    const m = me && typeof me === 'object' ? Object.assign({ authenticated: true }, me) : { authenticated: false };
    meP = Promise.resolve(m);
    return m;
  }
  SB.auth = {
    me(opts) {
      if (!meP || (opts && opts.refresh)) {
        const p = request('GET', '/api/auth/me').then(
          (m) => (m && typeof m === 'object' ? m : { authenticated: false }),
          (e) => { if (meP === p) meP = null; return { authenticated: false, error: (e && e.message) || 'error', status: e && e.status }; });
        meP = p;
      }
      return meP;
    },
    async login(email, password) {
      const res = await request('POST', '/api/auth/login', { email: String(email || '').trim(), password: String(password || '') });
      setMe(res && res.me);
      return res;
    },
    async logout() {
      try { await request('POST', '/api/auth/logout', {}); } catch (_) { /* go to the login page anyway */ }
      meP = null;
      location.assign('/login.html' + (state.forcedMock ? '?mock=1' : ''));
    },
    setMe, needsLogin, loginRedirect,
  };
})();

/* ---------------------------------------------------------------------------
 * MOCK server – in-browser fake of CONTRACT D, so every page renders without
 * the backend (screenshots, offline demo backup). State is kept in localStorage
 * so the demo panel and the dashboard in another tab stay in sync.
 * ------------------------------------------------------------------------- */
(function () {
  const SB = (window.SB = window.SB || {});
  const KEY = 'sb_mock_state_v1';
  const FIRST = 8, LAST = 21;
  const LABELS = ['good', 'too_fast', 'too_shallow', 'no_hold'];

  function rng(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
  function todayStr(d = new Date()) { return d.toISOString().slice(0, 10); }
  function localDateStr(d) { const z = (n) => String(n).padStart(2, '0'); return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}`; }
  // Mock clock: before 08:00 there is nothing due, so the mock pretends it is 15:00 to keep screenshots useful.
  function nowHour() { const h = new Date().getHours(); return h < FIRST ? 15 : h; }
  function iso(dateStr, hour, minute) { const d = new Date(`${dateStr}T00:00:00`); d.setHours(hour, minute || 0, 0, 0); return d.toISOString(); }
  function round1(x) { return Math.round(x * 10) / 10; }

  // Same fictional people as backend/app/seed.py (ids 1–7; Ravi is the live demo patient).
  const PEOPLE = [
    { id: 1, name: 'Ravi Kumar', age: 58, sex: 'M', surgery: 'Abdominal surgery (open hernia repair)', days: 8, language: 'hi', target_ml: 2000, adherence: 0.85, quality: 0.8, pb: 1950 },
    { id: 2, name: 'Priya Sharma', age: 44, sex: 'F', surgery: 'Laparoscopic cholecystectomy (gallbladder)', days: 5, language: 'en', target_ml: 2500, adherence: 0.95, quality: 0.9, pb: 2400 },
    { id: 3, name: 'Abdul Rahman', age: 63, sex: 'M', surgery: 'Heart bypass surgery (CABG)', days: 9, language: 'en', target_ml: 1500, adherence: 0.3, quality: 0.5, pb: 1000, missLast: true },
    { id: 4, name: 'Lakshmi Iyer', age: 66, sex: 'F', surgery: 'Total knee replacement', days: 6, language: 'ta', target_ml: 1500, adherence: 0.6, quality: 0.7, pb: 1300 },
    { id: 5, name: 'Mohan Das', age: 50, sex: 'M', surgery: 'Lung rehab after TB treatment (post-TB)', days: 7, language: 'hi', target_ml: 1750, adherence: 0.5, quality: 0.6, pb: 1450, missLast: true },
    { id: 6, name: 'Sreedevi Nair', age: 54, sex: 'F', surgery: 'Hysterectomy', days: 4, language: 'ml', target_ml: 2250, adherence: 0.9, quality: 0.85, pb: 2150 },
    { id: 7, name: 'Arjun Reddy', age: 41, sex: 'M', surgery: 'Appendix removal (appendectomy)', days: 3, language: 'en', target_ml: 3000, adherence: 0.9, quality: 0.55, pb: 2900 },
  ];

  function scoreOf(f, target, holdTarget) {
    const depth = 4 * Math.min(f.peak_ml / target, 1);
    const speed = f.max_rise_ml_s <= 900 ? 3 : f.max_rise_ml_s <= 1400 ? 1 : 0;
    const hold = 3 * Math.min(f.hold_s / (holdTarget || 3), 1);
    return round1(depth + speed + hold);
  }
  function ruleLabel(f) {
    if (f.max_rise_ml_s > 1400) return 'too_fast';
    if (f.pct_target < 0.5) return 'too_shallow';
    if (f.hold_s < 1.0) return 'no_hold';
    return 'good';
  }
  function makeFeatures(label, target, r) {
    const j = (a, b) => a + (b - a) * r();
    let peak, ttp, hold;
    if (label === 'good') { peak = target * j(0.8, 1.05); ttp = j(2.6, 4); hold = j(2.6, 4); }
    else if (label === 'too_fast') { peak = target * j(0.7, 1.0); ttp = j(0.6, 1.0); hold = j(1.2, 3); }
    else if (label === 'too_shallow') { peak = target * j(0.25, 0.45); ttp = j(1.8, 3); hold = j(1.5, 3); }
    else { peak = target * j(0.7, 0.95); ttp = j(2.2, 3.5); hold = j(0.2, 0.8); }
    const mean = peak / ttp;
    const max = label === 'too_fast' ? Math.max(1500, mean * j(1.3, 1.6)) : Math.min(mean * j(1.2, 1.5), 880);
    const f = {
      peak_ml: Math.round(peak), pct_target: round1(peak / target * 10) / 10, time_to_peak_s: round1(ttp),
      mean_rise_ml_s: Math.round(mean), max_rise_ml_s: Math.round(max), hold_s: round1(hold),
      smoothness: Math.round(j(0.08, label === 'too_fast' ? 0.5 : 0.25) * 100) / 100, duration_s: round1(ttp + hold + j(2, 3.5)),
    };
    f.pct_target = Math.round((f.peak_ml / target) * 100) / 100;
    return f;
  }
  function pickLabel(quality, r) {
    const x = r();
    if (quality === 'good') return x < 0.85 ? 'good' : LABELS[1 + Math.floor(r() * 3)];
    if (quality === 'poor') return x < 0.15 ? 'good' : LABELS[1 + Math.floor(r() * 3)];
    return x < 0.5 ? 'good' : LABELS[1 + Math.floor(r() * 3)];
  }
  function qualityOf(q) { return q >= 0.8 ? 'good' : q >= 0.6 ? 'mixed' : 'poor'; }

  function makeSession(st, p, dateStr, hour, quality, r, nBreaths) {
    const breaths = [];
    const startedAt = iso(dateStr, hour, 5 + Math.floor(r() * 40));
    for (let i = 0; i < (nBreaths || 10); i++) {
      const label = pickLabel(quality, r);
      const features = makeFeatures(label, p.target_ml, r);
      breaths.push({ t: new Date(startedAt).getTime() + i * 15000, features, label, score: scoreOf(features, p.target_ml, p.hold_target_s) });
    }
    const counts = { good: 0, too_fast: 0, too_shallow: 0, no_hold: 0 };
    breaths.forEach((b) => counts[b.label]++);
    const s = {
      id: st.nextSession++, patient_id: p.id, started_at: startedAt, slot_date: dateStr, slot_hour: hour,
      breaths_count: breaths.length, best_ml: Math.max(...breaths.map((b) => b.features.peak_ml)),
      avg_score: round1(breaths.reduce((a, b) => a + b.score, 0) / breaths.length), label_counts: counts, source: 'demo',
    };
    st.sessions.push(s);
    return { session: s, breaths };
  }

  function seed() {
    const st = { date: localDateStr(new Date()), patients: [], sessions: [], slots: {}, messages: [], nextSession: 1, nextMsg: 1, collect: { good: 0, too_fast: 0, too_shallow: 0, no_hold: 0 }, model: null };
    const h = nowHour();
    PEOPLE.forEach((pp) => {
      const r = rng(pp.id * 977);
      const surg = new Date(); surg.setDate(surg.getDate() - pp.days);
      const p = {
        id: pp.id, name: pp.name, age: pp.age, sex: pp.sex, surgery: pp.surgery, surgery_date: localDateStr(surg), language: pp.language,
        target_ml: pp.target_ml, hold_target_s: 3, family_phone: '+91 98xxxxxx' + String(10 + pp.id), nurse_phone: '+91 97xxxxxx01', personal_best_ml: pp.pb,
      };
      st.patients.push(p);
      // 6 past days of history
      for (let d = 6; d >= 1; d--) {
        const day = new Date(); day.setDate(day.getDate() - d);
        const ds = localDateStr(day);
        for (let hr = FIRST; hr <= LAST; hr++) {
          if (r() < pp.adherence * (0.75 + 0.05 * (6 - d))) {
            const { session } = makeSession(st, p, ds, hr, qualityOf(pp.quality - 0.03 * d), r, 10);
            st.slots[`${p.id}|${ds}|${hr}`] = { status: 'done', session_id: session.id };
          } else st.slots[`${p.id}|${ds}|${hr}`] = { status: 'missed' };
        }
      }
      // today, up to the previous hour
      const ds = st.date;
      for (let hr = FIRST; hr < Math.min(h, LAST + 1); hr++) {
        const isLast2 = hr >= h - 2;
        if (pp.missLast && isLast2) { st.slots[`${p.id}|${ds}|${hr}`] = { status: 'missed' }; continue; }
        if (r() < pp.adherence) {
          const { session } = makeSession(st, p, ds, hr, qualityOf(pp.quality), r, 10);
          st.slots[`${p.id}|${ds}|${hr}`] = { status: 'done', session_id: session.id };
        } else st.slots[`${p.id}|${ds}|${hr}`] = { status: 'missed' };
      }
    });
    st.messages.push({ id: st.nextMsg++, patient_id: 3, patient_name: 'Mohammed Arif', kind: 'missed', to_role: 'nurse', text: 'SpiroBuddy alert: Mohammed Arif has missed 2 breathing sessions in a row. Please give him a call.', sent: false, dry_run: true, created_at: new Date(Date.now() - 40 * 60000).toISOString() });
    return st;
  }

  let st = null;
  function load() {
    if (st) return st;
    try { const raw = localStorage.getItem(KEY); if (raw) st = JSON.parse(raw); } catch (_) { st = null; }
    if (!st || st.date !== localDateStr(new Date())) { st = seed(); save(); }
    return st;
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (_) { /* private mode */ } }
  function reloadFromStorage() { st = null; return load(); }

  function slotsToday(p) {
    const h = nowHour();
    const out = [];
    for (let hr = FIRST; hr <= LAST; hr++) {
      const s = st.slots[`${p.id}|${st.date}|${hr}`];
      let status;
      if (s && s.status === 'done') status = 'done';
      else if (s && s.status === 'missed') status = 'missed';
      else if (hr < h) status = 'missed';
      else if (hr === h) status = 'pending';
      else status = 'upcoming';
      const o = { hour: hr, status };
      if (s && s.session_id) o.session_id = s.session_id;
      out.push(o);
    }
    return out;
  }
  function summaryOf(p) {
    const today = slotsToday(p);
    const h = nowHour();
    const due = Math.max(0, Math.min(14, h - FIRST + 1));
    const done = today.filter((s) => s.status === 'done').length;
    const todaySessions = st.sessions.filter((s) => s.patient_id === p.id && s.slot_date === st.date);
    const best = todaySessions.length ? Math.max(...todaySessions.map((s) => s.best_ml)) : null;
    // consecutive missed up to now
    let run = 0, maxRun = 0;
    today.forEach((s) => { if (s.hour > h) return; if (s.status === 'missed') { run++; maxRun = Math.max(maxRun, run); } else if (s.status === 'done') run = 0; });
    const ratio = due ? done / due : 1;
    let status = 'green';
    if (run >= 2 || (due && ratio < 0.4)) status = 'red';
    else if ((due && ratio < 0.7) || (best != null && best < 0.8 * p.personal_best_ml)) status = 'yellow';
    // trend: today's best vs. yesterday's best
    const y = new Date(); y.setDate(y.getDate() - 1); const ys = localDateStr(y);
    const ySess = st.sessions.filter((s) => s.patient_id === p.id && s.slot_date === ys);
    const yBest = ySess.length ? Math.max(...ySess.map((s) => s.best_ml)) : null;
    let trend = 'flat';
    if (best != null && yBest != null) trend = best > yBest * 1.03 ? 'up' : best < yBest * 0.97 ? 'down' : 'flat';
    const all = st.sessions.filter((s) => s.patient_id === p.id).sort((a, b) => a.started_at < b.started_at ? 1 : -1);
    return Object.assign({}, p, { status, done_today: done, due_today: due, best_today: best, trend, last_session_at: all.length ? all[0].started_at : null });
  }
  function history(p) {
    const out = [];
    for (let d = 6; d >= 0; d--) {
      const day = new Date(); day.setDate(day.getDate() - d);
      const ds = localDateStr(day);
      const ss = st.sessions.filter((s) => s.patient_id === p.id && s.slot_date === ds);
      out.push({
        date: ds, best_ml: ss.length ? Math.max(...ss.map((s) => s.best_ml)) : 0, sessions_done: ss.length,
        avg_score: ss.length ? round1(ss.reduce((a, s) => a + s.avg_score, 0) / ss.length) : null,
      });
    }
    return out;
  }
  function findP(id) {
    const p = st.patients.find((x) => x.id === Number(id));
    if (!p) { const e = new SB.api.ApiError(404, 'Patient not found'); throw e; }
    return p;
  }
  function addMsg(p, kind, to, text) {
    const m = { id: st.nextMsg++, patient_id: p.id, patient_name: p.name, kind, to_role: to, text, sent: false, dry_run: true, created_at: new Date().toISOString() };
    st.messages.push(m);
    return m;
  }
  function summaryText(p, lang) {
    const s = summaryOf(p);
    const best = s.best_today != null ? `${s.best_today} mL` : 'no reading yet';
    if (lang === 'hi') return `${p.name} ने आज ${s.done_today} में से ${s.due_today} सत्र पूरे किए। आज की सबसे अच्छी साँस ${best} रही (लक्ष्य ${p.target_ml} mL)। धीरे-धीरे और गहरी साँस लेते रहें – आप अच्छा कर रहे हैं!`;
    return `${p.name} completed ${s.done_today} of ${s.due_today} breathing sessions so far today. Best breath today: ${best} (target ${p.target_ml} mL). Keep breathing slowly and deeply, and hold for 3 seconds – steady progress!`;
  }

  /* Mock logins: the fictional demo accounts (docs/REBUILD_PLAN.md §2). Never real people. */
  const ME_KEY = 'sb_mock_me';
  const HOSP = { id: 1, name: 'Demo General Hospital' };
  const ALL_PERMS = ['view', 'update_care_plan', 'confirm_prescriptions', 'manage_appointments', 'upload_documents', 'acknowledge_alerts'];
  const ACCOUNTS = [
    { id: 1, email: 'admin@demo-general.example', password: 'demo-admin-2026', name: 'Admin desk', role: 'admin', department: 'Administration', perms: ALL_PERMS },
    { id: 2, email: 'meera.nair@demo-general.example', password: 'demo-doctor-2026', name: 'Dr. Meera Nair', role: 'doctor', department: 'Surgery', perms: ALL_PERMS },
    { id: 3, email: 'kabir.rao@demo-general.example', password: 'demo-doctor-2026', name: 'Dr. Kabir Rao', role: 'doctor', department: 'Chest medicine', perms: ALL_PERMS },
    { id: 4, email: 'anjali@demo-general.example', password: 'demo-nurse-2026', name: 'Sister Anjali', role: 'nurse', department: 'Post-op ward', perms: ALL_PERMS },
    { id: 5, email: 'thomas@demo-general.example', password: 'demo-nurse-2026', name: 'Nurse Thomas Mathew', role: 'nurse', department: 'Chest ward', perms: ['view', 'acknowledge_alerts'] },
  ];
  function mockMe() {
    let email = null;
    try { email = localStorage.getItem(ME_KEY); } catch (_) { /* private mode */ }
    const a = ACCOUNTS.find((x) => x.email === email) || ACCOUNTS[0];
    return { authenticated: true, kind: 'staff', id: a.id, name: a.name, email: a.email, role: a.role, hospital: HOSP, department: a.department, permissions_summary: a.perms.slice(), demo_mode: true, mock: true };
  }
  // /api/features in mock mode: the last list this browser got from the real server (saved by SB.ui.loadFeatures).
  function featureCache() { try { return JSON.parse(localStorage.getItem('sb_features_cache') || 'null'); } catch (_) { return null; } }

  async function handle(method, path, body) {
    await new Promise((r) => setTimeout(r, 120)); // feel like a network call
    reloadFromStorage();
    const url = new URL(path, location.origin);
    const p = url.pathname;
    const q = url.searchParams;
    let m;
    const out = (() => {
      if (method === 'GET' && p === '/api/health') return { ok: true, model_loaded: true, llm_enabled: false, whatsapp_enabled: false, data_backend: 'demo', demo_mode: true, v2_missing: false, mock: true };
      // Contract E in mock mode: the demo accounts only (fictional, REBUILD_PLAN §2); default = the demo admin.
      if (method === 'GET' && p === '/api/auth/me') return mockMe();
      if (method === 'POST' && p === '/api/auth/login') {
        const a = ACCOUNTS.find((x) => x.email === String((body && body.email) || '').trim().toLowerCase());
        if (!a || a.password !== (body && body.password)) throw new SB.api.ApiError(401, 'wrong email or password');
        try { localStorage.setItem(ME_KEY, a.email); } catch (_) { /* private mode */ }
        return { ok: true, me: mockMe() };
      }
      if (method === 'POST' && p === '/api/auth/logout') { try { localStorage.removeItem(ME_KEY); } catch (_) { /* ignore */ } return { ok: true }; }
      if (method === 'POST' && p === '/api/me/session') {
        const pt = st.patients.find((x) => x.id === Number(body && body.patient_id)) || st.patients[0];
        return { ok: true, patient_id: pt.id, name: pt.name, language: pt.language };
      }
      if (method === 'GET' && p === '/api/features') return featureCache() || [];
      if (method === 'GET' && p === '/api/patients') return st.patients.map(summaryOf);
      if ((m = p.match(/^\/api\/patients\/(\d+)$/))) {
        const pt = findP(m[1]);
        if (method === 'PUT') {
          ['target_ml', 'hold_target_s', 'language', 'family_phone'].forEach((k) => { if (body && body[k] !== undefined && body[k] !== null && body[k] !== '') pt[k] = body[k]; });
          return summaryOf(pt);
        }
        return Object.assign(summaryOf(pt), { today: slotsToday(pt), history: history(pt) });
      }
      if ((m = p.match(/^\/api\/patients\/(\d+)\/sessions$/))) {
        const pt = findP(m[1]);
        const lim = Number(q.get('limit') || 20);
        return st.sessions.filter((s) => s.patient_id === pt.id).sort((a, b) => a.started_at < b.started_at ? 1 : -1).slice(0, lim)
          .map((s) => ({ id: s.id, started_at: s.started_at, slot_hour: s.slot_hour, breaths_count: s.breaths_count, best_ml: s.best_ml, avg_score: s.avg_score, label_counts: s.label_counts }));
      }
      if (method === 'POST' && p === '/api/classify') { const label = ruleLabel(body || {}); const proba = {}; LABELS.forEach((l) => (proba[l] = l === label ? 1 : 0)); return { label, proba, source: 'rules' }; }
      if (method === 'POST' && p === '/api/collect') { const l = body && body.label; if (st.collect[l] !== undefined) st.collect[l]++; return { ok: true, count_by_label: st.collect }; }
      if (method === 'POST' && p === '/api/train') { st.model = { accuracy: 0.94, n_train: 3200 + Object.values(st.collect).reduce((a, b) => a + b, 0), n_real: Object.values(st.collect).reduce((a, b) => a + b, 0), labels: LABELS, trained_at: new Date().toISOString(), note: 'MOCK metrics – start the server for real training' }; return st.model; }
      if (method === 'GET' && p === '/api/model') return st.model || { accuracy: 0.93, note: 'MOCK metrics' };
      if ((m = p.match(/^\/api\/summary\/(\d+)$/))) { const pt = findP(m[1]); return { text: summaryText(pt, (body && body.language) || pt.language), source: 'template' }; }
      if ((m = p.match(/^\/api\/whatsapp\/(\d+)$/))) {
        const pt = findP(m[1]);
        const kind = (body && body.kind) || 'summary'; const to = (body && body.to) || 'family';
        const text = kind === 'missed' ? `SpiroBuddy alert: ${pt.name} has missed 2 breathing sessions in a row. Please give them a call.` : summaryText(pt, pt.language);
        addMsg(pt, kind, to, text);
        return { sent: false, dry_run: true, text };
      }
      if (method === 'GET' && p === '/api/messages') { const lim = Number(q.get('limit') || 50); return st.messages.slice().reverse().slice(0, lim); }
      if ((m = p.match(/^\/api\/demo\/simulate\/(\d+)$/))) {
        const pt = findP(m[1]);
        const h = Math.min(Math.max(nowHour(), FIRST), LAST);
        const r = rng(Date.now() % 100000 + pt.id);
        const { session, breaths } = makeSession(st, pt, st.date, h, (body && body.quality) || 'good', r, (body && body.breaths) || 10);
        session.started_at = new Date().toISOString();
        breaths.forEach((b, i) => (b.t = Date.now() - (breaths.length - i) * 15000));
        st.slots[`${pt.id}|${st.date}|${h}`] = { status: 'done', session_id: session.id };
        if (session.best_ml > pt.personal_best_ml) pt.personal_best_ml = session.best_ml;
        return { session_id: session.id, slot_hour: h, slot_status: 'done', breaths };
      }
      if ((m = p.match(/^\/api\/demo\/miss\/(\d+)$/))) {
        const pt = findP(m[1]);
        const h = nowHour();
        const hours = [];
        for (let hr = Math.min(h, LAST); hr >= FIRST && hours.length < 2; hr--) hours.push(hr);
        hours.forEach((hr) => { st.slots[`${pt.id}|${st.date}|${hr}`] = { status: 'missed' }; });
        st.sessions = st.sessions.filter((s) => !(s.patient_id === pt.id && s.slot_date === st.date && hours.includes(s.slot_hour)));
        const msg = addMsg(pt, 'missed', 'nurse', `SpiroBuddy alert: ${pt.name} has missed 2 breathing sessions in a row. Please give them a call.`);
        return { ok: true, missed_hours: hours.sort(), message: msg };
      }
      if (method === 'POST' && p === '/api/demo/reset') { st = seed(); return { ok: true, patients: st.patients.length }; }
      throw new SB.api.ApiError(404, `Mock: no route for ${method} ${p}`);
    })();
    save();
    return JSON.parse(JSON.stringify(out));
  }

  SB.mock = { handle, reset() { st = seed(); save(); } };
})();
