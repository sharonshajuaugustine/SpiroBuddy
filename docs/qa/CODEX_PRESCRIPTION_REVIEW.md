# Doctor notepad and prescription review audit

**Implementation update:** publication now rejects missing reviewed form/unit/timing/food fields when an AI notepad reference is supplied, and rejects previously reviewed references. A negative-publication regression and duplicate-reference assertion passed in the final core regression set. AI governance now includes notepad reviews (three focused tests passed). The transaction/concurrent publication limitations below still apply; these guards do not provide distributed idempotency.

Reviewed 12 October 2026. Static source review only; no provider calls, patient database mutations or additional test run. Graph discovery found `meds.service.create_prescription`; newly added notepad routes were absent from the graph, so their known source files were read directly.

## Verified strengths

- `routes_meds.notepad_draft` requires doctor `rx.create` permission for the target patient. Drafting does not insert prescriptions or dose events.
- Draft prompts ask the provider to copy explicit values, leave missing values null and avoid recommendations. When provider/consent gates fail, pipe-separated manual parsing is available; ambiguous free text remains a name without an inferred dose.
- Issuing requires patient-scoped doctor permission. An supplied AI event must match patient, hospital, purpose `rx_notepad` and successful status. Cross-patient references return 404.
- Frontend populates missing fields as “Needs review”, checks the fields and opens an explicit publication confirmation. Successful publication records the actual signed-in doctor.
- Backend rejects an absent/invalid positive dose quantity and empty medication name. Unrecognized frequency/duration is retained with warnings and no scheduled dose reminders. SOS does not generate reminders.
- New prescription/items are initially drafted, then approved. Failures within item insertion/approval attempt cleanup. Superseded prescriptions remain in history.

## Findings needing attention

### P1: API can publish missing-unit and unspecified-food drafts

`meds.service.clean_lines` requires a dose number but permits absent form and dose unit. `normalise_food(None)` treats missing food instruction as `any`, understood. Thus a direct doctor POST of a notepad line with drug name, quantity 1, BD and three days, but null unit/form/food, can become an approved scheduled medicine. This bypasses the frontend’s explicit review checks. Missing food is not an explicit “no food restriction” choice.

Recommended fix: enforce required reviewed fields at publication on the server. At minimum reject missing dose unit and an unspecified food decision on the notepad workflow; distinguish an explicit `any` from null. Consider preserving compatibility for old structured prescriptions deliberately rather than changing legacy semantics accidentally. Add an API test with a successful scoped notepad event and missing fields.

### P2: publication is not atomic across replacement and dose generation

`create_prescription` approves the new prescription before updating the replaced prescription, cancelling its future doses and calling `refresh_doses`. Those operations occur outside the cleanup try block. A later store error can therefore return an error after the new prescription is already visible; a retry can create another current prescription. Concurrent replacement requests can both observe the same current old prescription. There is no idempotency key or compare-and-swap around publication.

Recommended fix: transaction where the backend supports it, otherwise a patient-scoped lock with explicit recovery and idempotent publication reference for the single-process prototype. Failure injection tests should assert that retries cannot duplicate visible prescriptions and that replacement does not leave conflicting reminders. Do not advertise multi-instance atomicity.

### P2: new notepad reviews are omitted from governance review totals

`ai_register.stats` counts drafts/reviews only when purpose equals `rx_extract`. New notepad events use `rx_notepad`, so they appear in `by_purpose` calls but do not contribute to headline draft/review/edit totals. The trust/governance totals can show zero reviewed drafts after a successful notepad review. Include both prescription draft purposes in these totals, with tests.

### P2: review reference can be reused and history overwritten

Issuance checks event scope and success but not prior decision, and no prescription-to-event relation is persisted. Reusing one event for another issue updates its single reviewed-by/decision row. This is not a cross-patient authorization bug, but it loses review history and allows reuse of a stale draft reference. Recommended: bind the event to a specific issued prescription and preserve immutable review records, or disallow reuse if one event represents one publication.

### P3: structured dose frequencies use fixed clock defaults

BD resolves to routine morning/night; QID resolves to 08:00, 12:00, 16:00, 20:00. These are configurable/default schedule conventions, not clock times extracted from an unspecified note. Exact explicit times are supported by the existing structured API, but the notepad schema has no `times` field. A note containing exact times may return unsupported frequency text and receive no reminder rather than preserve those times structurally. Keep that limitation visible; expand schema only with clinician review.

### P3: manual draft truncation is silent

Manual parsing returns the first 20 non-empty lines without warning when additional lines are supplied. AI response length is validated. Warn or reject more than 20 manual medicine lines so omitted lines are visible to the doctor.

## Existing test evidence read

`tests/test_submission_flow.py` contains tests for manual draft non-publication and mocked AI draft publication/review/cross-patient scope. `tests/test_meds.py` covers normalization, unclear schedules, replacing/stopping, audit and pharmacy verification. These test definitions were inspected; their execution result belongs to the parent’s running suite. Real provider quality, clinician acceptance, failure-injection atomicity, replay behavior and API missing-unit review were not verified by this audit.

## Integration ownership

This worker changed only this report. No backend/frontend/test changes were made. P1 and persistence findings were reported to the coordinating agent for implementation ownership.
