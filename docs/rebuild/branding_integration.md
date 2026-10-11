# Branding lite - integration note (builder BR, STATE row P2-BRAND)

Each hospital's own name and logo at the top of the patient pages, set by the hospital admin. Design: `docs/plan/12_HOSPITAL_ONBOARDING_AND_BRANDING.md` sections 2 and 6 (step 2 only). The per-hospital install address `/h/<slug>/` and the store apps are not part of this.

## What was built (all committed, tests green)

- **Data, no schema change.** `hospitals.settings["branding"] = {display_name, short_name, accent, logo_path}`. No branding saved means: display name = the hospital's own name, no logo, the SpiroBuddy teal.
- `backend/app/branding.py` - defaults, validation (name 2-40 characters, short name 2-14, no `< > " \` { } \`), accent `#rrggbb` with a contrast check (see below), reading, saving, logo processing (PNG / JPEG / WebP only, 512 KB, re-encoded with Pillow so metadata is gone, scaled to at most 512 px; a picture of more than 9 million pixels is refused from its header before it is decoded, and the refusal words talk about logos), logo read.
- `backend/app/routes_admin.py` (new; the module name was already in the router loop, `main.py` untouched):
  - `GET /api/admin/branding`, `PUT /api/admin/branding` (name, short name, accent only), `POST /api/admin/branding/logo`, `DELETE /api/admin/branding/logo` - action `admin.manage` (hospital admin only; doctor and nurse get 403, a patient or nobody gets 401), own hospital only, every write audited (`branding.update`, `branding.logo_upload`, `branding.logo_remove`).
  - Reads for the apps (never error, no branding gives the defaults): `GET /api/me/branding` + `GET /api/me/branding/logo` for a **patient** session, and `GET /api/branding/mine` + `GET /api/branding/mine/logo` for a **staff** session (any role).
  - **Why two pairs of read paths (a deviation from the brief):** the middleware in `main.py` lets only a patient session through under `/api/me/*` and only a staff session through everywhere else. A staff session on `/api/me/branding` therefore gets 401, and fixing that needs a `main.py` change. Both pairs return the same JSON; only the `logo_url` inside differs. There is no public logo address.
  - What the JSON holds: `{display_name, short_name, accent, accent_ink, logo_url | null, powered_by: "with SpiroBuddy"}`. The line `powered_by` is a constant in code: the API refuses any attempt to send it (or `logo_path`, or any other key) and the page also writes the line itself instead of trusting the server's text.
- **Contrast rule.** The accent is the background of the name strip. The strip's text is white or the dark ink, whichever reads better, and needs 4.5 to 1. The strip also needs 1.5 to 1 against the page background of the light screen and of the dark screen, so it never fades away (near-white and near-black colours are refused; so are mid-greys where neither text colour is clear). The refusal message says in plain words what is wrong. The same rule runs in the browser while the admin types.
- `web/branding.html` + `web/js/branding-admin.js`: the admin page (app name, short name, accent colour with the refusal message, logo upload and remove, a phone-shaped live preview of the unsaved changes, Save, Undo) and a list of what a hospital can NOT change (safety messages, status labels, the "with SpiroBuddy" line). Badge `data-feature="hospital.branding"`. Only the admin can use it: others see a plain "only the hospital admin" message.
- `web/js/branding.js` (the one script tag a patient page loads; it adds `css/branding.css` itself): waits until a login exists (the patient pages open their session a moment after loading: it looks at `/api/auth/me`, which never answers 401, at 0 / 0.7 / 1.8 / 4 / 8 s), reads `/api/me/branding` (patient) or `/api/branding/mine` (staff), fills `<div id="brand-slot" hidden>`. Any problem leaves the slot hidden and the page exactly as it was. The accent colour paints this strip only. Text goes in as text, the logo only from an address starting with `/api/`. The logo sits on a white tile so a logo in the same colour as the strip still shows.
- Added to `web/app.html` and `web/meds.html`: one `<div id="brand-slot" hidden></div>` and one `<script src="js/branding.js" defer>` each, nothing else. Checked in Chrome at 375 and 1440 px, light and dark: no console errors, no sideways scroll, and on `app.html` a simulated breathing session still runs (reached 1920 mL) with no console errors. With no login at all the slot stays hidden.
- `backend/app/seed_branding.py` + ONE guarded hook in `backend/app/seed.py` (right after `seed_auth.ensure`): both demo hospitals get a branding block ("Demo General Care" blue, "Riverside Care" plum) and a generated initials-on-colour PNG logo. Recreated on every demo reset.
- `web/dashboard.html`: one link "App branding", hidden until a one-line script sees an admin login (`/api/auth/me` role = admin). Nobody else sees it, the page is otherwise unchanged. If the lead wants the video dashboard to stay untouched, delete the two added lines after `id="demo-link"`.
- `web/js/api.js`: `'/branding.html'` added to `STAFF_PAGES` (a 401 on that page sends the user to the login page).
- `tests/test_branding.py` (49 tests): defaults; admin saves and the patient of that hospital sees it; nobody of the other hospital sees it (patient, admin, logo bytes); doctor, nurse, patient, nobody cannot save; bad and low-contrast colours, bad names refused; the fixed line and other keys cannot be set; other hospital settings survive a save; PNG / JPEG / WebP accepted, SVG, PDF, markup, empty, oversized refused; metadata removed; logo address changes with a new logo; one audit row per write; pages free of the banned words and of anything about money; both patient pages carry exactly one script tag.

## Tests run

`tests/test_branding.py` (49 passed). Required neighbours: `tests/test_auth.py`, `tests/test_platform.py`, `tests/test_isolation.py` - result in the builder's final report. The whole suite was not run (the lead does that).

## Edits needed in files I do not own

1. **`backend/app/features.py`** - flip `hospital.branding` from `planned` to `live` once the lead is satisfied (it works end to end for the two patient pages named below). Keep `hospital.pwa_install` `planned`. Suggested note text: "Name and logo show at the top of the patient app and My medicines; set by the hospital admin. Safety messages and status labels stay fixed."
2. **New patient pages** (`web/patient.html`, `web/patient-login.html` or the new patient app page by the PIN-login builder): to get the strip, add `<div id="brand-slot" hidden></div>` where the header goes and `<script src="js/branding.js" defer></script>`. Nothing else is needed. After a PIN login the patient session exists, so the strip fills in on its own.
3. **Whoever builds the hospital Settings save** (`PUT` of `hospitals.settings`): merge, never replace. The `branding` block lives inside `settings`. `authz.hospital_settings()` already returns it next to the defaults.
4. **`web/js/ui.js` `HOSP_NAV`** (optional): add `{ group: 'Hospital', key: 'branding', href: '/branding.html', label: 'App branding', icon: 'edit', roles: ['admin'] }` so the admin finds the page in the side menu of the new hospital shell. The dashboard link already works without it.

## Notes and limits (said plainly)

- Staff on a patient page see their own hospital's strip. With a patient session in the same browser the strip follows the staff login, not the patient: cosmetic, and only in a browser that holds both logins.
- The "with SpiroBuddy" line is English only (it is a fixed brand line). The hospital's name is shown as the hospital typed it.
- The accent is used on the strip only. Buttons, alerts and status colours are the shared ones.
- Logo files go through `backend/app/storage.py` (local folder or Supabase storage); an old logo file is removed when a new one is uploaded. On a demo reset the old demo logo file is left behind (harmless).
- Nothing in these pages touches money (a test guards that). All names are fictional.

## Founder, by hand

Nothing is needed for the demo. To try it: log in as `admin@demo-general.example` (password is in `backend/app/seed_auth.py`), open the dashboard, press "App branding", change the colour, press Save, then open the patient app (`/app.html?id=1`).
