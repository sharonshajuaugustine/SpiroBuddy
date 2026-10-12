# Final browser verification — 12 October 2026

This record distinguishes observed browser behavior from automated tests. Browser observations below were reported by the parent Codex agent from the isolated local sample-data application; they do not establish that the Render deployment contains the same build.

## Department operations observed in the browser

- Hospital admin created bed **QA-1** successfully.
- Hospital admin admitted sample patient **101** to QA-1 successfully.
- Hospital admin created bed **QA-2** successfully.
- Hospital admin transferred sample patient 101 to QA-2 successfully. The old bed displayed **cleaning**, and the new bed displayed **occupied**.
- Browser CDP stalled at the subsequent discharge click. **Discharge completion has not been observed in the browser.** Do not count this as a successful discharge, cleaning/ready or complete end-to-end browser verification.

## Patient consent and language observed in the browser

- Patient AI consent was off by default. The patient explicitly enabled it, saved it and reloaded; the saved state remained true.
- The patient then withdrew consent and saved; the saved state was false. This verifies the consent controls and persistence, not a real provider call or clinical validation.
- Switching between English and Hindi worked. Tamil and Malayalam browser behavior was not checked in this sequence.

## Appointments observed in the browser

- Sample patient 101 requested **12 October 2026, 9:30 am**, with **Check-up** as the reason.
- The request appeared in the actual **Dr. Meera** doctor's My day workspace.
- The doctor confirmed the request, and the patient visits screen displayed **Confirmed**.

## Discharge document browser observations

- A fresh browser tab loaded the discharge editor for the administrator in read-only mode, showing the authorized sample patient 101 data.
- After restoring browser interaction, the doctor created a replacement draft, saved it and published **version 2**.
- The authenticated patient read their own version 2 and acknowledged that exact version; the acknowledgement was confirmed in the browser.
- The print view rendered **version 1** content. This verifies print-page content rendering, not exported PDF output or a physical print.
- At a 375 px viewport, the patient care page's document width was **375 px**, with no horizontal page overflow.
- Saved screenshot evidence exists at `.build/qa-evidence/patient-care-mobile.png` and `.build/qa-evidence/patient-care-published.png`. These are private local build artifacts, not committed release assets.

## Staff phone layout and session-source observation

- At 375 px, the dashboard and charts for patients **101** and **1** had a reported document width of **360 px**, within the viewport.
- The Recent sessions table's **Source** heading was present. Patient 1's session labels had not loaded in that browser observation, so no claim is made that a specific simulator/app label was observed there. The label mapping has separate mocked-render coverage.

## Integrated local HTTP smoke checks

The parent agent verified bed release and marking the released bed ready through authenticated local HTTP requests. A doctor saved and published discharge version 1; the patient opened their own document after OTP authentication and acknowledged it successfully. These are integration/API checks, distinct from browser clicks and the browser version 2 replacement flow above.

## Browser simulator call-to-nurse journey

The complete local simulator sequence was observed: Ravi's simulated AI check-in → answer → mild pain selection → explicit yes to a callback → neutral conversation ending → **Nurse review requested**. Try Nurse then logged in as actual **Sister Anjali**, and the nurse inbox showed Ravi's check-in call with the nurse-review request. Screenshot evidence: `.build/qa-evidence/simulated-ai-callback.png` and `.build/qa-evidence/nurse-callback-alert.png`. This verifies the local browser simulator journey; it is not Sarvam API, telephone or webhook integration evidence.

## Automated verification, separate from browser results

- **Combined suite: 930 passed, zero failures, zero expected failures in 1151.77 seconds**, as reported by the parent agent, before the final startup/phone-preservation guards. Earlier expected-failure counts are historical; none remained in that full run.
- Final startup guards: **5 focused checks passed** (approximately 30 seconds), `.build/pytest-startup-preservation.log`; populated storage is never automatically reset at lifespan startup, and empty storage receives non-destructive initial seeding.
- Latest phone-preservation/PIN checks: **28 passed**, `.build/pytest-seed-phone-preservation.log`. These targeted post-guard results are separate from the earlier 930-test total.
- Department workflow tests: **5 passed in 39.53 seconds**, including admission, transfer, discharge, cleaning/ready counts and history; role/hospital isolation; stale and duplicate allocations; malformed input; a simultaneous allocation race; and rollback of patient display labels after operational storage failure.
- Additional department demo-reset regression: **1 passed in 21.74 seconds**, confirming reset removes bed allocations/history and preserves unrelated settings.
- Latest discharge focused test run: **6 passed**, as reported by the responsible discharge worker/root agent.
- Final bundled Node syntax sweep, repeated after the source-column and layout fixes: **55 scripts checked, zero syntax failures** — 38 external scripts under `web/js` and 17 executable inline scripts across `web` HTML. External-script tags, empty scripts and non-JavaScript data scripts were excluded from the inline count. Module inline scripts used module parsing. This verifies syntax, not browser execution, layout or functionality.

## Remaining browser checks

Complete the bed discharge/ready browser-click sequence and inspect department/overview and prescribing layouts at phone width. Observe loaded session-source row labels and exercise print/save-PDF if an exported PDF is needed. Direct access by unauthorized roles and another hospital should also be checked in the browser; the corresponding API boundaries already have automated coverage. These observations cover several complete journeys but do not constitute exhaustive browser acceptance or live-deployment verification.

## Provider configuration and submission artifact boundary

The parent agent confirmed Sarvam's corrected greeting was committed as version 2. The approved API key and organisation/workspace/agent metadata, including version 2, were saved in Render with **Save only**. The user selected browser-only demonstration and **`CALL_PROVIDER=dry_run`** was saved. No redeploy, outbound telephone call, phone connection or application webhook delivery is implied by those saved settings.

The canonical readable deck is `output/Aarogya_Saathi_DTI_GuGu_GaGa_Readable.pptx`: 17 slides, seven native editable tables and larger fonts, with all slides visually checked and zero issues. Its cover is receiving a final refinement. Claude owns the video with the team's own narration; target a complete video under six minutes and 100 MB, with approximately 2.5 minutes explaining the product. No completed video is claimed by this QA report.
