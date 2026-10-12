# Prompt for Claude: department operations and hospital overview

You are working on Aarogya Saathi / SpiroBuddy in `C:\Users\USER\Desktop\SpiroBuddy`.

Submission is approaching. Build one complete department and bed-management prototype, with a hospital overview derived from the same data. Use sample patients only.

## Read first

Read AGENTS.md, CLAUDE.md, docs/AAROGYA_SAATHI_PROJECT_AUDIT.md, docs/ARCHITECTURE.md and docs/plan/13_AROGYA_SATHI_PLATFORM.md. Prefer codebase-memory MCP tools for code discovery. Inspect actual schema columns and permission helpers before coding.

## Coordination: another agent is editing this checkout

Codex is working on patient registration, OTP, consultation notes, prescriptions/notepad review, medication reminders, staff identity, breathing validation and the DTI deck. Leave those files alone. If another Claude session owns appointments, leave its files alone too.

Do not reset, stash, overwrite or commit another agent's changes. Do not push, deploy, reset the live demo or change the live database. Do not edit .env or print credentials.

## Your task

Build:

1. A department workspace showing its patients, doctor, ward/bed and current admission state.
2. A bed board showing available, occupied and cleaning beds. Staff can admit a patient, transfer them and discharge them.
3. A hospital overview showing current admissions, admissions/discharges today, occupied/free beds and department totals.
4. A patient row linking to the existing patient chart and prescribing page. Reuse the existing registration page rather than building a second registration flow.

Use the existing hospital admin account for the operational coordinator prototype. Clearly describe this as an admin-operated department view. A dedicated department login remains Planned until its role, provisioning and migration are properly integrated. Do not silently broaden doctor or nurse access.

## File ownership

Create only these new files/directories:

- backend/app/routes_departments.py
- backend/app/department_ops/ (new helpers)
- web/department.html
- web/hospital-overview.html
- web/js/department.js
- web/js/hospital-overview.js
- web/css/department.css
- tests/test_department_ops.py
- docs/CLAUDE_DEPARTMENT_HANDOFF.md

Do not modify existing shared files, including main.py, authz.py, store.py, features.py, ui.js, api.js, patient.html, register.html, app.html or medicine/OTP code. Put the exact required router/navigation/registry integration patches in the handoff document for Codex to apply.

## Storage and correctness

- Reuse existing hospitals, staff and patients.
- For this single-process prototype, use hospital-scoped app_settings records for bed inventory and operational state if that avoids an immediate schema migration. Store patient references, not copies of patient records or credentials. Document this prototype limitation and the eventual normalized-table migration.
- Treat hospital_id as a server-derived property from the authenticated actor, never a trusted request-body field.
- Validate department names against the hospital's departments.
- Separate bed identity from its displayed label.
- Keep admission, transfer and discharge history with staff actor and timestamps.
- Prevent a patient having two active bed assignments and a bed having two active patients.
- Serialize allocation mutations in this single-process prototype. Include a version/conflict check for stale edits. Do not claim this proves distributed concurrency safety.
- Keep the existing patient's ward/bed fields consistent with confirmed operational assignments. Check patient scope before any update.
- Derive dashboard counts from the stored operational records. Never use hardcoded occupancy numbers or infer admissions from breathing sessions.
- Requests without the proper session/permission must fail. Cross-hospital resources return 404.
- Use the middleware's documented resource parameter names where applicable. Every non-GET browser request carries X-SB: 1.
- No payments, diagnosis, AI-generated conditions or real notifications.
- Plain HTML/CSS/JS, no frontend build step. Match the existing design and make the pages usable at phone and laptop widths.

## Verification

Test admission, transfer, discharge, cleaning/ready transitions, occupied-bed rejection, a second active allocation for the same patient, stale updates, simultaneous allocation attempts, cross-hospital requests and unauthorized roles. Verify the hospital totals change correctly after each operation. Test malformed identifiers and missing patients. Record browser checks and errors honestly.

Use .venv\Scripts\python.exe. FastAPI's test client needs local loopback sockets, which may require normal test execution permissions outside the sandbox. Do not change application security to bypass a test-environment problem.

## Handoff

Write docs/CLAUDE_DEPARTMENT_HANDOFF.md with completed files, route contracts, exact test results, browser checks, limitations and precise shared-file integration patches. List any database change separately; do not apply it live. Leave the original registration and prescription workflow intact.

Finish the smallest complete workflow before adding roster, meetings or unrelated features. Report what works and what remains Planned.
