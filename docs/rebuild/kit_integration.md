# kit – integration notes (front-end kit, P1-1.3 + REBUILD_PLAN §3.10/§3.11)

Changes the kit builder needs in files it does not own. Written Sun 11 Oct 2026.

## 1. `web/sw.js` – keep the patient token out of the offline cache (owner: lead or the patient-app builder)
The service worker caches every page it fetches under the full address. A patient link `app.html?t=<token>` therefore stores the token as a cache key on the phone. `app.html` already removes `t` from the address bar, but the cache entry stays.

Exact change, in the `fetch` handler:
```js
// before
const put = (res) => { if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return res; };
// after
const put = (res) => { if (res && res.ok && !url.searchParams.has('t')) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return res; };
```

## 2. `web/app.html` – for the builder who rewrites it later
- The shim (`openSession()`, just above `boot()`) opens a session only when the link has `t=` or `id=`. A plain `/app.html`, or a `?unit=` link with no `id`, opens **no** session. Once the auth middleware is on, those fall back to the placeholder patient. Fix when rewriting: after the unit lookup, call `SB.auth.me()`; a patient cookie gives `patient_id`. If there is none and `/api/health` says `demo_mode`, post `{patient_id: pid}` to `/api/me/session`.
- The "who" demo button calls `SB.api.patients()`, which is staff-only from now on. It fails quietly for a patient session.
- `app.html` does not load `ui.js`. To show the demo ribbon, load `/js/ui.js` and call `SB.ui.fakeRibbon({ large: true })` (it checks `/api/health` itself). Same for `guardian.html`.

## 3. Backend auth (Contract E owner) – what the kit expects
- `POST /api/auth/login` → `{ok, me}`. `me` has the same shape as `GET /api/auth/me` (`role`, `name`, `hospital: {id, name}`, `department`, `permissions_summary`, `demo_mode`).
- `permissions_summary` for a nurse: the kit accepts a list of permission names, `{permissions: [...]}` or `{perm: true}`. Any of these drives the nav (`confirm_prescriptions` → Prescription review, `manage_appointments` → Appointments).
- 403 reasons: `login.html` shows its own sentence when the reason contains "pending" or "approv" (waiting for the admin) or "disabled". Any other 403 reason is shown as written, so keep it plain English.
- 429 → "locked for 15 minutes". 401 → "Wrong email or password".

## 4. Feature-key test (`features.py` owner)
`web/js/ui.js` no longer has a literal `data-feature="…"` example in its comments, so a grep of `web/` for that attribute only finds real keys.
