# Department operations handoff — implemented by Codex

12 October 2026. This module was completed by a Codex subagent after the delegated Claude session stopped. No live data, environment, schema or credentials were changed.

## Completed workflow

- Admin-operated department workspace and hospital overview, with server-derived hospital scope. Doctor, nurse and patient access is rejected; dedicated department provisioning/login remains Planned.
- Explicit bed inventory: department and ward must match the hospital configuration; unique bed identity is independent of its human label. Initial inventory is empty. Existing patient chart labels are shown separately and are never counted as admissions.
- Admit, transfer, discharge, cleaning and ready transitions. A transfer releases the old bed into cleaning and occupies the new bed, without counting another admission. Discharge releases the bed into cleaning; it neither changes medication nor publishes a clinical discharge summary.
- Duplicate patient/bed allocation, invalid transitions and stale edits return conflicts. Operational history records action, bed, department, patient reference where applicable, staff identity and India local timestamp.
- Patient ward/bed fields follow confirmed allocation. Failed operational-state saving compensates those display-field writes.
- Hospital counts derive only from recorded bed operations. Available, occupied and cleaning counts are separate. Admission and discharge counts today come from history; transfers do not inflate admissions.
- Patient chart, existing registration and doctor prescription workspace links; no duplicate registration flow.

## Files

`backend/app/routes_departments.py`, `backend/app/department_ops/`, `web/department.html`, `web/hospital-overview.html`, `web/js/department.js`, `web/js/hospital-overview.js`, `web/css/department.css`, `tests/test_department_ops.py`, this document.

## Route contracts

All routes require the existing hospital admin staff session. POST requests also require the existing `X-SB: 1` CSRF header. Body hospital identifiers are ignored; the authenticated actor determines the tenant.

| Method and route | Body | Result |
| --- | --- | --- |
| GET `/api/department-ops` | none | version, hospital, configured departments/wards, beds, hospital-scoped patient/doctor summaries, history and counts |
| POST `/api/department-ops/beds` | `version`, `department`, `ward`, `label` | refreshed board |
| POST `/api/department-ops/beds/{bed_id}/admit` | `version`, integer `patient_id` | refreshed board |
| POST `/api/department-ops/beds/{bed_id}/transfer` | `version`, integer `patient_id`; target bed is the path resource | refreshed board |
| POST `/api/department-ops/beds/{bed_id}/discharge` | `version` | refreshed board |
| POST `/api/department-ops/beds/{bed_id}/clean` | `version` | refreshed board |
| POST `/api/department-ops/beds/{bed_id}/ready` | `version` | refreshed board |

Bed IDs are opaque generated hex strings. Missing and foreign-hospital beds return 404. Missing and foreign-hospital patients return 404. Invalid identifiers/input return 400. Version mismatch or invalid occupancy transition returns 409. Logged-out requests return 401; staff of other roles return 403. Patient-only sessions are rejected by the existing staff API middleware with 401.

## Shared integration

The root Codex agent has already added `"routes_departments"` to the optional feature-router list in `backend/app/main.py`, before the API catch-all, and added `/department.html` and `/hospital-overview.html` to the staff-page allowlist in `web/js/api.js`.

Navigation now includes admin-only links to `/department.html` and `/hospital-overview.html` in `web/js/ui.js`. Do not add them to doctor/nurse navigation or introduce a department role without migration and provisioning. Feature registry entries may describe admin-operated bed operations and hospital counts as Live after integration and checks; a dedicated department login remains Planned.

Integration update: admin-only links have now been added to both navigation shells, with initially hidden legacy links. The authorized `seed.py` reset hook now deletes only `department_ops:` and `discharge:v1:` state keys before removing/reusing patients, preserving unrelated application settings. The department creation form preserves selected department/ward across refreshes and filters. Patient visits return to the medicines home using the existing patient cookie and selected language, rather than the breathing page.

## Verification

Node syntax checks passed for both new scripts, and Python compilation passed for the route and service modules. `.venv\Scripts\python.exe -m pytest tests/test_department_ops.py -q --tb=short` completed with **5 passed in 39.53 seconds** on isolated disposable demo data. Tests cover complete operation/history/count changes, malformed identifiers, transition conflicts, stale edits, role and tenant isolation, two concurrent allocation attempts and compensation after storage failure. The first run exposed a test expectation mismatch: patient-only sessions return 401 from existing staff middleware rather than 403; the test now reflects the enforced middleware contract.

Browser/phone layout checks have not been performed by this subagent; the root agent owns browser verification. Responsive CSS uses flexible columns and a horizontally scrollable patient table. Do not report those layout checks as passed until inspected.

Parent browser evidence: created beds QA-1 and QA-2, admitted sample patient 101 into QA-1 and transferred them into QA-2. The old bed showed cleaning and the new bed occupied. The browser connection stalled at the discharge click, so discharge/ready and phone layout are not browser-verified. See `docs/qa/CODEX_FINAL_BROWSER_QA.md` for the broader partial browser evidence and its limits.

Additional reset regression: `tests/test_department_ops.py::test_demo_reset_removes_operational_assignments_only` passed in **21.74 seconds**, confirming reset removes active allocations/history and preserves an unrelated settings record. Both changed JavaScript files passed Node syntax checking; `seed.py` compiled successfully.

## Prototype limitations

Operational data persists in `app_settings` under `department_ops:<hospital_id>`. No database migration is applied. One process-wide reentrant lock and version check serialize mutations within a single application process. They do not prevent races across multiple workers/servers. Patient display fields and JSON state are separate storage writes with compensation; process termination between writes is still a consistency risk. Migrate to normalized beds/admissions/events tables with transactional occupancy uniqueness and row locking before production or multiple workers.

No automatic bed import, full patient encounter/admission lifecycle, nurse roster, hospital billing, discharge-summary publishing or department staff login. History is append-only within this operational state but is not a regulated immutable audit store. Hospital date calculations currently use the existing application's India local clock; additional tenant timezones need integration.
