# Claude task: independent submission QA and demo rehearsal

You are working on Aarogya Saathi / SpiroBuddy in `C:\Users\USER\Desktop\SpiroBuddy`. Submission is approaching. Independently verify the patient, doctor and nurse demo, find reproducible problems, and prepare an honest demonstration script. Complete the work rather than returning only a plan.

## Read first

Read AGENTS.md, CLAUDE.md, docs/AAROGYA_SAATHI_PROJECT_AUDIT.md and the current feature registry. Prefer the codebase-memory MCP graph tools for code discovery, falling back to file search when necessary. Treat current code as the source of implementation truth; older documents may be stale.

## Coordinate safely

Codex owns registration, OTP, consultation notes, prescriptions, notepad review, reminders, staff identity, breathing validation and the DTI deck. Another Claude task may own department/bed operations or appointments. Do not edit their application files, tests or presentation files. Do not reset, stash, commit, push or deploy. Do not edit .env, inspect secrets, send real messages or write to the deployed database.

Your owned outputs are ONLY:

- docs/qa/CLAUDE_SUBMISSION_QA.md
- docs/qa/CLAUDE_DEMO_SCRIPT.md
- docs/qa/CLAUDE_FIX_HANDOFF.md
- docs/qa/evidence/ (sample-data screenshots; no patient identifiers from real records)
- tests/test_claude_submission_regressions.py, if genuinely useful independent regression tests are needed

Do not overwrite an existing file without first checking whether another session owns it. If these paths are taken, create a clearly named new QA output and report its location.

## Use an isolated local demo

Inspect existing test fixtures and startup configuration. Create a separate local test data directory and use a free localhost port. Do not reuse or stop Codex's server on port 8010. Use DEMO_MODE with sample data and blank external provider credentials; disable demo autopilot if supported. Keep runtime data outside tracked application files. Document the exact launch command without secrets.

Use the deployed site https://spirobuddy.onrender.com/ only for read-only comparison of public pages and implementation status. Never assume a local feature is deployed. Do not create accounts, issue prescriptions or exercise OTP mutations on the deployed site.

## Verify these end-to-end flows

1. Doctor signs in: displayed identity and hospital match the authenticated account. Register a sample patient with MRN and phone. Save consultation notes. Prepare a notepad prescription draft, review missing fields, explicitly approve it, and confirm the patient's medication schedule uses the approved prescription. Draft preparation must not publish a prescription.
2. Patient signs in using hospital + MRN + simulated OTP. Verify clear demo labeling, generic responses for unknown records, expiry, single use, wrong-code limits and hospital isolation. Check reusable PIN fallback labeling. Confirm changing the registered phone invalidates outstanding OTPs if that feature is present.
3. Patient on a narrow phone viewport: medicine name, strength, quantity, timing and instructions are readable; mark a scheduled dose taken; reload and confirm persistence. Check print view. Check opt-in reminder behavior and document that closed-app notifications are not implemented if applicable.
4. Breathing exercise is available only when assigned. Empty, malformed and partial sessions must not count as completed. A completed valid sample session should reach the staff view for the correct patient. Browser-generated data must not be presented as verified physical hardware measurements.
5. Nurse signs in: correct actor appears in the header and alert actions. Verify a missed medication dose creates a scoped nurse alert, repeated checks do not duplicate it, and a patient dose update clears it appropriately. Do not claim family messaging exists unless verified.
6. Authorization: another patient cannot read these records; another hospital cannot access them; patients cannot issue prescriptions or change clinician settings; nurses cannot perform doctor-only actions. Use test fixtures and sample records only.
7. Mobile and navigation: check patient login, medicines, doctor registration/prescribing and nurse dashboard at about 375 px and desktop width. Record horizontal scrolling, blocked controls, broken links, placeholder claims, unclear labels and language-switch issues.

For time-dependent features, use isolated test fixtures or supported clock control. Do not change the computer clock or live records. If browser tooling or a provider is unavailable, document exactly what could not be verified; do not fabricate a pass or screenshot.

## Deliverables

In CLAUDE_SUBMISSION_QA.md, give a compact matrix of each flow: Pass / Fail / Not verified, local versus deployed, evidence and limitations. For each failure include a concrete reproduction, expected and actual behavior, severity and probable source location. Keep sample IDs explicit and artificial. Record the commands and actual test results.

In CLAUDE_FIX_HANDOFF.md, list the smallest recommended fixes in priority order: submission blockers first, then important demo problems, then polish. Include exact file/function references and suggested changes, but do not modify application files. Separate verified defects from hypotheses. Do not propose broad refactors under the deadline.

In CLAUDE_DEMO_SCRIPT.md, write a practical 3-minute presentation and a 5-minute backup walkthrough, with account roles, sample actions and recovery steps if a provider or Render is unavailable. State what is built, simulated and planned. Describe Aarogya Saathi as the hospital platform and SpiroBuddy as its breathing companion. Team name: GuGu GaGa. Members: Sharon Shaju Augustine and Fathima Shifana; coworkers and former B.Sc Computer Science classmates. Do not invent an employer, contact, college spelling, clinical outcomes or user validation.

If adding regression tests, make them isolated, meaningful and compatible with existing fixtures. Do not weaken assertions or alter existing tests just to obtain a green result. Run your tests and report failures honestly. If an operating-system sandbox blocks test execution, report the limitation separately from an application failure.

Finish with paths to your outputs, actual verification results, the top five fixes Codex should integrate, and all remaining unverified behavior. Leave the repository and other sessions' work intact.
