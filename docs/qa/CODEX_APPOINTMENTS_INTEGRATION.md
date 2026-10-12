# Appointments integration review

Date: 2026-10-12. Read-only snapshot while Claude owns this module. No application edits, commits or test runs were performed.

## Present implementation

The root pages `web/appointments.html`, `web/doctor-day.html`, and `web/patient-visits.html`, their JavaScript and `backend/app/routes_appointments.py` exist. Graph discovery returned no indexed appointments nodes, so direct file reads were used.

`main.py` already attempts to include `routes_appointments` before the API catch-all (around line 605). No router patch is required. This review verifies the inclusion mechanism statically, not successful import into a restarted server: check `SKIPPED_MODULES` and actual endpoint responses after Claude completes its module.

Eleven declared endpoints cover doctor availability, staff slots/list/booking/transitions/day and patient slots/list/request/transitions. Staff handlers require `appt.manage`; nurse access depends on `manage_appointments`. Patient endpoints use the patient actor and `appt.request`. Main middleware selects only the patient cookie for `/api/me/*`, requires `X-SB` for writes, and applies resource visibility before handler validation. `authz.py` recognizes the `appt` resource parameter. Query/body patient and doctor IDs receive additional handler checks. These observations do not replace executed authorization tests.

## Minimal shared-file integration for Codex

1. In legacy `PAGES` in `web/js/ui.js`, add `appointments.html` (Appointments, calendar) and `doctor-day.html` (My day, calendar) entries. On identity refresh, show Appointments for admin/doctor or nurses with `hasPerm(me, 'manage_appointments')`; show My day only for doctors. Avoid briefly exposing links before identity resolves by initially hiding these entries.
2. The hospital shell currently points Appointments at `/hospital/appointments.html`; no matching hospital page was found. Point that entry to `/appointments.html` when this module is ready. Existing `/hospital/availability.html` should be reviewed separately rather than assuming the new root module supplies that page.
3. Preserve explicit safe `?next` login destinations. For the fallback in `web/login.html`, route doctors to `/doctor-day.html` after successful authentication; keep other roles at `/dashboard.html`. Read the actual authenticated identity, not the clicked demo role. Keep the existing same-origin redirect validation.
4. In `web/js/meds-patient.js`, add a translated `My visits` link to `patient-visits.html?lang=<encoded language>` beside the existing breathing/print links. The patient session cookie supplies identity: do not include a patient token or MRN in the URL. Provide English/Hindi/Tamil/Malayalam labels or an explicitly identified English fallback.
5. Patient visits currently links back through its `appLink()` helper to the breathing app; review changing its return target to `meds.html?lang=<encoded language>` so patients without breathing assignment return to their medicines home. Ask Claude to implement this inside its owned file or wait for the handoff before editing it.

These are integration instructions, not already-applied changes. Root can add nav/login/medicine links after receiving a completed handoff.

## Feature registry

`appt.booking`, `appt.availability`, and `appt.reminders` remain `in_development`; `appt.teleconsult` remains `planned`. Do not change these merely because files exist. Booking/availability can be reassessed after tests and browser validation. The new routes alone do not establish implemented day-before/two-hour reminders or video visits.

## Tests and completion gate

`tests/test_appointments.py` contains 25 test functions covering request/confirm, alternative-time acceptance/decline, cancellation, attendance/no-show, invalid transitions, double booking and racing requests, database uniqueness, pending-request limits, cross-hospital/patient scope, anonymous access, nurse permissions, bad dates/availability, absent doctor, filters, doctor-day rules and audit writes. This agent did not execute them and makes no pass claim. Parameterization may increase the actual collected case count.

`docs/CLAUDE_APPOINTMENTS_HANDOFF.md` was absent at inspection time. Before integrating: obtain Claude's final handoff, run its tests in isolated data, confirm route import has not been skipped, restart the local server, and verify doctor and patient paths including narrow-screen layouts. Test root nav links rather than the existing hospital placeholder paths. Concurrent file changes may supersede this snapshot.
