# 12 – Hospital onboarding, per-hospital branding, store apps, doctor reminders, spirometer placement

Founder's asks, Mon 12 Oct 2026, ~00:35 IST. Written from known platform rules (no web research this time – check the starred ★ facts against the official pages before quoting them to judges).

## 1. Verdicts in one line each

| Ask | Verdict |
|---|---|
| Hospital data moved in "in minutes" | **Yes for doctors, departments and patients** (CSV/Excel or FHIR file, with a dry run). Medicines history comes in as "to confirm", never as active. Already specified as Contract L / `docs/INTEROPERABILITY.md` (build item P2-X3). |
| Each hospital's own name, logo and colours **inside** the app after login | **Yes, cheap.** Store branding per hospital; the app reads it after the patient logs in. |
| The **home-screen** name and icon change to "MIMS – …" after login | **Not for store apps.** ★ iOS can switch only to icons bundled in the app at build time (and shows a system message); the home-screen name can't change. ★ Android can switch only between pre-built launcher aliases. **Yes for the web app (PWA):** each hospital gets its own address and manifest, so "Add to home screen" from the hospital's QR shows the hospital's name and logo. |
| One app in Play Store and App Store | **Yes, as one generic "SpiroBuddy" app** that wraps the web app (Android: Trusted Web Activity; iOS: a Capacitor wrapper with real native parts such as notifications, because Apple rejects thin website wrappers). |
| A separate store app per hospital ("MIMS Care") | **Only if the hospital publishes it under its own developer account.** ★ Apple's App Store Review Guideline 4.2.6 rejects apps made from a commercial template unless the content owner submits them. So: later, for big hospitals that want it. |
| Login with registration number + OTP | **PIN now, OTP later.** ★ In India, SMS OTP needs a paid SMS provider and TRAI DLT registration of the sender and message template (takes days). WhatsApp authentication messages are another paid option. Demo: PIN (Live) + OTP (Simulated). |
| Reminders for doctors (surgeries etc.) | **"My day" for doctors is possible now** (patients needing a call, prescriptions to renew, visit requests). **Surgery (OT) reminders = Planned:** they need the hospital's operation-theatre schedule from its own system. |
| Where the spirometer lives in the patient app | A **"Breathing" tab** that appears only when the hospital gave this patient a spirometer. Simple 2D piston on the phone; the 3D model stays on the hospital and public pages. |

## 2. Per-hospital branding – design

**Data (no schema change needed):** `hospitals.settings` (JSON, exists) gets a `branding` block:
`{display_name: "MIMS Care", short_name: "MIMS", logo_path: "<storage key>", accent: "#0b6e8a", slug: "mims"}`.
Logo uploads go through `backend/app/storage.py` (type, size, re-encode, strip metadata).

**Hospital admin page "App branding"** (admin only, audited): upload logo, pick an accent colour (the page refuses colours that fail text contrast in light or dark), set the app name, see a live phone preview, publish.

**Patient app after login:** `GET /api/me` returns the hospital's branding → the app shows "MIMS Care" + logo in the header and on the splash, and uses the accent colour for highlights only. Fixed and not editable by hospitals: the safety texts (red-flag message, "does not diagnose"), the status labels, and a small "with SpiroBuddy" line.

**Per-hospital home-screen install (PWA):** each hospital gets `/h/<slug>/` and `/h/<slug>/manifest.webmanifest` (name, short_name, icons from its logo, theme colour). The discharge slip's QR opens `/h/<slug>/patient-login.html`; "Add to home screen" then shows the hospital's own name and icon. Works on Android Chrome and iOS Safari, no store needed.

**Store apps (later):** one generic SpiroBuddy listing on each store. After login the inside rebrands; the home-screen icon stays SpiroBuddy. Big hospitals can later publish their own listing from their own developer account (same code, their name).

## 3. Moving a hospital in "in minutes" (Contract L, P2-X3)

1. Admin downloads our template (or uploads their own export: CSV / Excel / FHIR R4 Bundle).
2. A mapping screen guesses columns ("UHID", "MRN", "Reg No" → registration number; "Dr", "Consultant" → doctor).
3. **Dry run:** rows OK, rows with errors, duplicates, all shown before anything is saved.
4. Import: doctors and departments (accounts created as "invited", each sets a password), patients (registration numbers kept, PINs made on first visit or printed in a batch).
5. Old prescriptions arrive as **"to confirm"**: a doctor must confirm before anything reaches a patient's phone (safety rule, Contract L).
6. Whole-hospital export at any time (no lock-in).
Honest claim: "a hospital's doctors, departments and patients can be moved in within minutes from a spreadsheet; medicines need a doctor's confirm".

## 4. Doctor reminders
- **Now-ish (build):** doctor home "My day": patients who need a call, prescriptions ending in the next 2 days (renew or stop), visit requests, missed doses.
- **Planned (pitch only):** operation-theatre reminders and pre-op checklists, from the hospital's OT schedule (needs a connection to its own system, Contract L levels 2–3).

## 5. Patient app layout (elderly-first, every hospital)
Bottom bar with at most 4 big tabs, icons + words, in the patient's language:
**Today** (what to do now: medicine due, breathing session due, a visit) · **Medicines** (list + "Show at the pharmacy") · **Breathing** (only if the care plan includes a spirometer: the current coach with the 2D piston, voice and "connect device" = In development) · **Help** (I do not feel well / call).
The 3D twin stays out of the patient app (too heavy for old phones; three.js only on twin pages); staff see it in the patient chart, judges on `/twin.html`.

## 6. Order of work
1. Registration number + PIN login (`docs/rebuild/REGNO_PIN_BRIEF.md`) – first.
2. **Branding lite** (one builder, ~45 min): `hospitals.settings.branding` for both demo hospitals, the patient app/medicines page/patient-login page show the hospital's name + logo after login, an admin "App branding" card (upload logo, name, accent, preview). Feature key `hospital.branding`.
3. Per-hospital PWA manifest `/h/<slug>/` (small) – nice demo: scan the slip → home-screen icon is the hospital's.
4. Patient app tabs (Today · Medicines · Breathing · Help) – medium; touches `app.html`, which the video uses – only with the founder's OK.
5. Everything else (store wrappers, OTP, OT reminders, CSV import screen) = Planned cards with honest labels; CSV import is specified already (Contract L) if time allows after the freeze-free window.
