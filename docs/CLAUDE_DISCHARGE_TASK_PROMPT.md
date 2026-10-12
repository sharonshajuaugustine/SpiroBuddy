# Claude task: discharge summaries and patient care instructions

You are working on Aarogya Saathi / SpiroBuddy in `C:\Users\USER\Desktop\SpiroBuddy`. Build a complete, reviewable discharge-document and patient care-instructions module for this hackathon. Use your available reasoning capacity to implement and test the module, not merely plan it. Prioritize a working end-to-end prototype over decorative features.

## Understand the project first

Read AGENTS.md, CLAUDE.md, docs/AAROGYA_SAATHI_PROJECT_AUDIT.md and current architecture/feature documentation. Prefer codebase-memory MCP tools for code discovery. Inspect the actual authentication, hospital scoping, patient access, persistence, prescription and audit helpers before designing your module. Do not assume documentation describes the latest implementation.

Aarogya Saathi is the hospital platform. SpiroBuddy is its breathing companion. The priority is connecting doctors and nurses to patients on their phones. Discharge instructions should remain accessible to the authenticated patient after leaving the ward.

## Parallel work and file ownership

Codex owns registration, OTP/PIN, consultation notes, prescriptions/notepad review, medicine reminders, staff identity, breathing validation and the presentation deck. Other Claude tasks may own department/bed operations, appointments and independent QA. Do not edit those files or their tests.

Create only these new module files, checking for existing ownership before writing:

- backend/app/routes_discharge.py
- backend/app/discharge_docs/ (your new persistence, validation and document helpers)
- web/discharge-editor.html
- web/my-care.html
- web/discharge-print.html
- web/js/discharge-editor.js
- web/js/my-care.js
- web/js/discharge-print.js
- web/css/discharge-docs.css
- tests/test_discharge_docs.py
- docs/CLAUDE_DISCHARGE_HANDOFF.md

If any path already exists, inspect it and stop writing to that path until ownership is clear. Do not overwrite another session's work. Do not reset, stash, commit, push, deploy, edit .env, print secrets or modify the live database. Use isolated sample data. Do not send real SMS, WhatsApp or email.

Do not edit shared main.py, auth, schema, feature registry, patient pages, navigation or prescriptions. Describe the exact minimal integration patches in your handoff. If the main application already has a supported router discovery mechanism, use it without editing shared files; otherwise exercise your router using an isolated test application and clearly mark integration as pending.

## Required behavior

### 1. Doctor workspace

Create a responsive editor for one scoped patient. Show patient name, hospital MRN and hospital context retrieved through existing authorized APIs. Permit the doctor to enter:

- diagnosis/condition summary;
- treatment/course summary;
- clinician-authored home-care instructions;
- clinician-authored warning signs and what action to take;
- follow-up instructions and optional date;
- optional discharge date;
- clinician-authored SpiroBuddy exercise instructions, only as documented guidance, without generating a new exercise prescription.

The system must not invent diagnosis, medicine doses, warning signs or exercise targets. No AI provider is required. Do not translate clinical text automatically or claim a validated translation. Label the document language and preserve exactly what the clinician writes.

Support saving a draft, reloading it, previewing it and explicit publication by an authorized doctor. Drafts must never appear in the patient workspace. The publish step should state clearly that the patient will be able to view the document.

### 2. Document state and history

Implement draft -> published -> superseded or withdrawn states. Published content is immutable. To revise it, create a new draft version, preserve the previous version and supersede it only when the replacement is published. Withdrawing a document must retain its history and a reason while removing it from the patient's current-care view. Show publication time, author and version.

Use optimistic concurrency/version checks so stale edits return a clear conflict rather than silently overwriting another doctor's changes. Publication and supersession must be one consistent operation within the supported persistence model. If atomicity is limited to a single process, state that explicitly and test it. Do not claim distributed safety.

### 3. Patient workspace

Create a phone-friendly My care page using the existing authenticated patient session. Resolve patient identity server-side; never trust a patient_id query parameter as authorization. Show only the current published document for that patient, with author, hospital, publication time, document language and version.

Display instructions as readable sections, with a print link and a button to acknowledge reading this specific document version. Acknowledgement is not consent, proof of adherence or a clinical outcome. Repeated acknowledgement should be idempotent. Show a friendly empty state if nothing has been published. Make long text wrap without horizontal scrolling at approximately 375 px.

Include navigation links to existing patient medicines and breathing pages only where appropriate and already supported. Do not expose clinician editor links to patients.

### 4. Staff visibility

Authorized nurses may read the published document and its acknowledgement state for patients they can already access. They may not author, publish, revise or withdraw doctor documents. Doctors may edit only within existing patient/doctor access rules. Do not broaden permissions for convenience. Admin access should follow existing policy; document any unresolved policy decision instead of inventing one.

### 5. Medication references

If existing prescription APIs support it safely, display the current approved medicines alongside the document using those APIs. Clearly distinguish a current medication list from the discharge document's publication snapshot. A historically reproducible snapshot may be stored as a read-only reference if its source, prescription IDs and capture time are explicit. Do not create a second prescribing system, modify prescriptions, recalculate doses, invent missing instructions or issue medicine automatically.

The discharge document is separate from bed/admission status. Publishing a document must not discharge a bed or change patient admission state. Leave that workflow to the department module.

### 6. Print page

Provide a clean browser-printable document with patient/MRN, hospital, author, publication date, version and clinician content. Use existing authorization for every read. Patients can print their own current document; authorized staff can print scoped documents according to policy. Escape all text and avoid raw HTML insertion. An isolated preview of a draft must clearly say Draft and remain staff-only.

## Backend and data requirements

Follow existing API patterns and cookie/session conventions. Propose explicit route contracts for draft creation/update, preview, publish, version list, withdraw, staff read, patient read and patient acknowledgement. Validate lengths, dates, empty required content and all state transitions. Treat content as plain text. Use server-derived hospital/actor/patient scope for reads and writes; block cross-hospital and cross-patient access.

Prefer existing persistence abstractions. If there is no supported extension without shared schema edits, use carefully namespaced hospital-scoped app_settings state for the prototype, with bounded document sizes, explicit locking/version checks and a documented migration plan. Never store passwords, tokens or OTPs in document state. Avoid large unbounded scans where scoped lookup is possible.

Audit creation, publication, replacement, withdrawal and acknowledgement using existing audit conventions. Log identifiers, actor, time and transition metadata; do not put full clinical text in application logs or general audit messages. Do not duplicate patient profiles.

## Verification

Use an isolated demo/test data directory and a free localhost port, not Codex's port 8010. Blank external-provider credentials. Use artificial patient records only. Verify the module independently if shared-router integration is pending.

Test meaningful behavior:

- draft invisible to patient;
- correct publication and authenticated patient read;
- cross-hospital and cross-patient denial;
- nurse mutation denial and allowed scoped read;
- stale edit conflict;
- immutable published version and replacement history;
- failed publication does not supersede the current document;
- withdrawal behavior;
- acknowledgement attached to one version and idempotent;
- replacement requires a new acknowledgement;
- malicious HTML rendered as plain text;
- invalid dates, excessive content and invalid state transitions;
- persistence after reconstructing the service;
- simultaneous publication consistency within the claimed concurrency model.

Run your tests. If tooling allows, exercise doctor draft/publish -> patient read/acknowledge -> doctor replacement -> patient sees updated version in a browser. Verify phone layout and print layout. Report actual results; do not fabricate screenshots or passes. Distinguish environmental execution failures from product defects.

## Handoff

In docs/CLAUDE_DISCHARGE_HANDOFF.md include:

1. What works, with new file paths and entry URLs.
2. Exact route contracts and authentication requirements.
3. Exact minimal integration patches for shared router/auth middleware, navigation and feature registry; check middleware allowlists, not just router mounting. Do not make patient routes publicly readable.
4. Storage design, atomicity/concurrency limitations and migration path.
5. Test commands and actual results, plus browser checks and unverified behavior.
6. A short sample-data demonstration and remaining work in priority order.

Finish with a concise summary of implemented behavior, integration work left to Codex and any blockers. Leave all other sessions' work intact. Do not claim the module is deployed or clinically validated.
