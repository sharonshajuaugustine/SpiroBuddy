# Digital prescription (P2-RX) - integration notes for the lead

Written by builder B. The founder's idea: the doctor types the prescription, the patient sees every medicine on their own phone, and at the medicine counter they show the phone instead of paper. There is no photo upload and no AI in this feature.

## What is done

- **Doctor page** `web/prescribe.html?id=<patient id>`: patient header, current medicines (Change, Stop), a "Write a prescription" form (add and remove rows, Morning / Afternoon / Night chips or a 1-0-1 style code, food, days or "until stopped", "only when needed"), a big "Send to the patient's phone" button with a confirm step, then a preview of what the patient sees in four languages.
- **Patient page** `web/meds.html` (English, Hindi, Tamil, Malayalam): Today with a big "I took it" per time of day (shows "Reported"), All my medicines, "Show at the pharmacy" (full-screen white card with a QR), optional Read aloud.
- **Pharmacist page** `web/rx.html?t=<token>`: "Prescription check", public, no login.
- **Backend** `backend/app/routes_meds.py` and `backend/app/meds/` (normaliser, service, seed). Routes: Contract H (`POST /api/patients/{pid}/prescriptions`, `GET /api/prescriptions/{rx}`, `POST /api/prescriptions/{rx}/stop`, `GET /api/patients/{pid}/medicines`, `GET /api/patients/{pid}/doses`, `POST /api/patients/{pid}/doses/{dose}/report`), patient routes (`GET /api/me/medicines`, `GET /api/me/today`, `GET /api/me/prescription-card`, `POST /api/me/doses/{dose}/report` plus the contract's second name for the same tap), public `GET /api/rx-check/{token}`.
- **Demo data**: Ravi (patient 1) gets one issued prescription from Dr. Meera Nair (paracetamol 500 mg 1-0-1 after food 5 days, pantoprazole 40 mg 1-0-0 before food 14 days, ondansetron 4 mg only when needed). A demo reset recreates it. The demo doctor gets the clearly fictional registration number "DEMO-REG-0001 (fictional)" if she has none.
- **Not built, on purpose**: photo upload, AI reading, the review queue, nurse confirmation, patient upload (the upload and review routes of Contract H are left out).

## Two small hooks outside my files (already applied, please keep)

1. `backend/app/main.py`: `"/api/rx-check/"` added to `PUBLIC_PREFIXES`.
2. `backend/app/seed.py`: a guarded `seed_meds.wipe(st)` call in `wipe()` (before the patients are deleted, because prescriptions point at patients and patient ids are reused) and a guarded `seed_meds.seed(st, now)` call at the end of `seed()`. If `seed_v2.wipe` later clears prescriptions as well, both can stay.

## Edits the lead must make in files I don't own

### (a) `web/patient.html` (Ravi's staff page, used in the demo video)

In the template string that builds `.ph-actions` (around line 156), add one link after the Print button:

```html
<a class="btn" href="prescribe.html?id=${esc(id)}" title="Write a prescription and send it to the patient's phone">${ic('pill')}Medicines</a>
```

`id` is the page's existing `const id = new URLSearchParams(location.search).get('id') || '1';`. Nothing else on that page changes.

### (b) `web/app.html` (patient app, used in the video)

1. After the `#today` section (and before the alert section) add one big button, using the app's own button class:

```html
<a class="pa-btn primary" id="meds-link" href="meds.html"></a>
```

2. In the `T` object add one key per language:
   - `en`: `meds: 'My medicines'`
   - `hi`: `meds: 'मेरी दवाइयाँ'`
   - `ta`: `meds: 'என் மருந்துகள்'`
   - `ml`: `meds: 'എന്റെ മരുന്നുകൾ'`
3. At the end of `paintStatic()` add:

```js
$('#meds-link').innerHTML = ic('pill', { size: 24 }) + esc(tr('meds'));
$('#meds-link').href = 'meds.html?id=' + pid + '&lang=' + lang;
```

`meds.html` opens the same patient session as the app (cookie `sb_patient`). If the cookie is missing and the link carries `id` (demo) or `t` (personal link), it opens the session itself. The language comes from `?lang=`, then from the language the patient chose on `meds.html`, then from the patient's saved language.

## Feature keys to flip to live (only these are really finished)

| Key | Flip to | Why |
|---|---|---|
| `rx.manual` | `live` | The doctor types it; tested end to end. |
| `rx.patient_phone` | `live` | The patient sees it on their phone; tested. |
| `rx.pharmacy_screen` | `live` | The full-screen card works. Its footer says pharmacy acceptance is not yet tested; keep the registry note saying the same. |
| `rx.verify_qr` | `live` | The QR opens the public check page; tested. |
| `doses.tracking` | `live` | A tap is stored and shown as reported, nothing more; tested. Keep the note "nobody measures it". |

Leave `doses.reminders` (no chime or full-screen reminder yet), `doses.missed_alert` (no alert is raised), `rx.normaliser` (the table is built and tested, but there is no review screen; flip it if you are happy with "in the typed path only"), `rx.ai_read`, `rx.review` and `rx.patient_upload` as they are.

## Things the lead should know

- **Same path as Contract K.** `GET /api/me/today` is defined in `routes_meds.py` (it is in the brief) in the Contract K shape (`now_card`, `today`, `medicines`, `next_visit` always null for now, `offline_ok`) plus the full `doses`. If the patient-app builder also writes `/api/me/today` in `routes_me.py`, the one included earlier wins (`routes_meds` is before `routes_me` in `main.py`). Either drop one, or let `routes_me` import `meds.service.today_doses` and `counts_today`.
- **Service functions for other builders** (REBUILD_PLAN 3.12), in `backend/app/meds/service.py`: `medicines_for(pid)`, `doses_for(pid, from, to)`, `today_doses(pid)`, `report_dose(dose_id, role, actor_id, channel)`, `counts_today(pid)` (`{"reported", "due", "missed"}`). Not built: `snooze_dose`, `make_due_now`, `mark_missed`, `tick`.
- **Dose statuses.** The table stores `upcoming`, the contract's reported status (the one a patient tap sets) and `cancelled`. `due` and `missed` are worked out when read, from the clock and the hospital's `grace_minutes` (default 60). No alert or family notice is raised for a missed dose.
- **Dose events** are made for today and tomorrow, from the time of issue onward, and topped up whenever a patient or staff list is read (at most every 20 seconds per patient). The demo prescription is issued "at the start of today", so every dose of today is on the screen at any hour.
- **No schema change.** Stop reasons go to the audit log only (the table has no column for them). "Issued on" is `reviewed_at`; the table keeps the contract's internal status word for an issued prescription, but no page shows it, they show "Issued".
- **Pharmacist token** = `<prescription id>.<32 hex>`, an HMAC of (id, version, patient id). The secret is `RX_TOKEN_SECRET` if set; otherwise a random secret made once and kept in `app_settings` (survives a restart). Replacing a prescription makes a new id and version, so the old QR then answers "No longer current". Add `RX_TOKEN_SECRET` to `.env.example` if you want a fixed secret across hosts.
- **Rate limits** on `/api/rx-check/`: 60 requests a minute per address, and 10 bad tokens per 10 minutes per address, then 429.
- **Audit rows written:** `rx.create`, `rx.replace`, `rx.stop`, `dose.report` (only when a dose is newly reported), and `rx.verify` (public check, anonymous actor, with `hospital_id` in the detail). Drug names and tokens are never put in the audit detail.
- **Tamil and Malayalam** wording on `meds.html` needs a check by a native speaker (same note as the voice cues). English and Hindi are the main languages.
- **Offline.** The patient page needs a connection for each load and each tap; there is no saved copy. A QR that cannot be drawn offline falls back to the written address under it.
- **Tests:** `tests/test_meds.py` (55 tests). Run it with `tests/test_auth.py`, `tests/test_platform.py` and `tests/test_isolation.py`.
