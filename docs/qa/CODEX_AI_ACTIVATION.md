# Gemini activation: verified code prerequisites

**Implementation update:** patient GET/POST `/api/me/ai-consent` and the optional English/Hindi medicine-page control are now implemented and router/script integrated. Three isolated consent tests passed. The user's `AQ.` authorization key also passed one actual sample-only structured request through the application SDK using `gemini-3.1-flash-lite`. Earlier missing-UI findings below describe the pre-fix state. Deployment and the live consent-to-draft browser journey remain to be verified. Correct doctor editor URL: `/prescribe.html?id=<sample-id>`.

Checked 12 October 2026. Read-only inspection; no secrets, live records or consent choices were read or changed.

## User setup

1. Create a Gemini API key in Google AI Studio and put `GEMINI_API_KEY` in the Render service's environment settings. Do not paste it in chat, source code, browser JavaScript or the repository.
2. Set `GEMINI_MODEL` to an available model for that account, or retain the code default `gemini-3.1-flash-lite`. Actual account/model availability must be verified with a real request; this report does not certify that model entitlement.
3. Save environment changes and allow Render to restart/redeploy. An isolated local server started with blank provider keys will continue to use the manual fallback even if the deployed service now has a key.
4. Optional usage caps: `AI_DAILY_LIMIT` defaults to 300 across the service; `AI_PER_IP_HOUR` defaults to 20. Limits are in-memory, single-process counters.

## Required application gates

`backend/app/ai_gemini.py::ai_allowed` checks these in order:

- `gemini_enabled()` sees a nonempty server-side key.
- The patient's hospital has `hospitals.settings.ai_enabled` other than false. The default is true. This is **not** an `app_settings` key.
- The patient's latest `consents` row (highest `id`) has `items.ai_use` exactly boolean true and no `withdrawn_at`.
- Daily and IP caps permit the request.

Missing consent blocks provider requests. A withdrawn or false choice blocks them too. Clinical consent and the separate WhatsApp/phone reminder consent are different records: comms consent cannot activate Gemini.

## Missing activation UI/API

The current source has no writer for the clinical `consents` table and no patient AI-consent UI. `docs/ARCHITECTURE.md` describes GET/POST `/api/patients/{id}/consent` and GET/PUT `/api/admin/settings`, but these routes are not implemented in the inspected source. They must not be presented as working setup instructions.

The hospital branding API only accepts branding fields. PUT `/api/admin/branding` cannot enable AI. No existing hospital settings API was found either. Hospital AI defaults on; an existing explicitly disabled hospital requires a proper scoped settings implementation, not a branding workaround.

No application seed inserts clinical AI consent. `tests/test_platform.py` inserts synthetic consent rows only inside its isolated fixture. Those tests do not enable real or demo patients on Render. Newly registered patients therefore remain on manual-format notepad fallback until consent recording is implemented.

## Minimal safe implementation proposal

Add a narrowly scoped, versioned consent module and UI before claiming Gemini activation:

- Patient GET/POST `/api/me/ai-consent`: derive patient/hospital from the authenticated patient session; never accept either identity from the request body. Display a separate optional AI-processing choice, explain external-provider processing and manual fallback, default unchecked, and permit withdrawal.
- Store a new consent version with `items.ai_use` boolean, `created_at`, authenticated recorder, method and language. Preserve other consent item choices from the latest record; do not fabricate agreement to unrelated purposes. Record withdrawal explicitly. Serialize version creation or use a transaction.
- For staff-assisted recording, require patient access and a specifically authorized role. Record the actual recorder and stated consent method; staff login alone is not patient agreement. Do not automatically insert consent on registration or seed actual patients as consenting.
- If hospital control is needed now, add GET/PUT `/api/admin/ai-settings`, requiring `admin.manage`, deriving the hospital from the actor, accepting only a strict boolean and merging `hospitals.settings` without replacing other settings. Audit the setting change.
- Wire new routers before the static/catch-all route and provide clear navigation. Test own-patient consent, cross-hospital denial, missing/false/withdrawn/latest-choice behavior, settings preservation, audit identity and manual fallback.

This is a proposal, not a completed implementation. Coordinate with the root agent before assigning shared route/frontend ownership.

## End-to-end verification after implementation

1. Log in as a synthetic patient and explicitly choose AI processing for that patient.
2. Log in as the treating doctor, open `/meds-prescribe.html?pid=<synthetic-id>` and use a short sample notepad text containing explicit medicine fields only. Never send real identifiers or clinical records for setup testing.
3. Prepare the draft. Confirm the API response has `source: "gemini"`; inspect the corresponding `ai_events` entry for purpose `rx_notepad`, successful status, model and latency. Do not publish until the doctor has reviewed every field.
4. Confirm preparation created no prescription/dose events. Approve only the reviewed test draft through the existing publish action.
5. Withdraw consent and repeat preparation: expect `source: "manual_format"` and zero new provider calls.
6. Real provider access is **unverified** until step 3 succeeds. The mocked provider unit test proves application handling, not Google authentication, billing, quota, model access or network connectivity.

The existing route is POST `/api/patients/{pid}/prescriptions/draft-text`, doctor-only and patient-scoped. The notepad fallback remains usable without Gemini; missing values require human completion. No hardware measurement depends on the Gemini key.
