# Remaining submission and prototype limits

Updated 12 October 2026 from current source, existing test assertions and implementation handoffs. This review did not run providers, inspect credentials or verify Render. The final combined test run and deployment evidence belong to the root handoff.

## Submission blockers and honest demo boundaries

1. **Publish and smoke-test the combined build.** Local pages and passing isolated tests do not establish that Render has registration, OTP, appointments, bed operations, discharge documents or the updated registry. Verify the deployed URLs and the sample doctor → patient → nurse journey after publication. Do not reset the live database for a demonstration.
2. **Telephone calling is not verified.** Sarvam's provider-dashboard Chat conversation was tested, but no telephone connection, KYC completion, actual phone call, output extraction or matching application webhook has been verified. Use the labelled simulator/replay for the submission unless the complete acceptance sequence succeeds. See [SARVAM_CALL_DEMO_SETUP.md](../SARVAM_CALL_DEMO_SETUP.md).
3. **Real SMS and hardware are unavailable evidence.** OTP delivery is simulated; the PIN fallback is reusable. Browser breathing sessions are app/simulator reports, not attested device measurements. Do not describe the prototype as physical monitoring or real SMS authentication. Real Gemini SDK success is separate from a deployed, consent-gated prescription-draft browser demonstration.

These boundaries need accurate labelling rather than hurried replacement of the working demo. The editable deck and current local implementation should be presented as a tested hackathon prototype, without clinical outcome, compliance or production-readiness claims.

## Former expected failures: actual assertions and current fixes

The historical markers were in [test_critical.py](../../tests/test_critical.py). Current source has no `xfail` decorators: the stale nurse-login test was corrected and the callback, language-intent and outage cases were addressed. The earlier combined run recorded **904 passed, 14 expected failures** against the previous source. Focused checks and a new combined run must establish the final source; do not relabel that historical run as having zero expected failures.

| Assertion / test | Current implementation and remaining scope |
|---|---|
| `test_twilio_signature_is_checked_even_without_public_base_url`: forged WhatsApp request must return `403` | Configured Twilio credentials now require a canonical public base and a valid signature. Missing base fails closed. Real callback delivery with the deployed canonical URL remains unverified. |
| `test_twilio_voice_get_is_also_signature_checked`: unsigned GET voice request must return `403` | GET and POST use the same validator, including the signed query string. Unsigned no-key callbacks remain available only in demo mode for historical simulator behavior. |
| `test_exotel_webhooks_need_a_secret`: forged passthrough must return `403` and leave the escalation active | All Exotel callback handlers require `EXOTEL_WEBHOOK_SECRET`; outbound readiness requires it and generated status URLs carry its encoded token. Manual flow applet URLs must be configured with that token. This is an application shared secret, not a verified provider signature format; real Exotel operation remains untested. |
| `test_typed_tamil_and_malayalam_red_flags` (six phrases): intent must be `red_flag` | Source now covers the recorded Latin-script cases. Native-speaker review and clinical escalation validation are still required; a short fixed word list does not establish complete multilingual emergency recognition. |
| `test_typed_tamil_and_malayalam_stop_words` (three spellings): intent must be `stop` | Source now handles the recorded transliterations. English `STOP` remains the documented fallback; broader dialect/spelling coverage still needs review. |
| `test_store_outage_is_a_503_with_a_plain_message`: outage response must be `503` and omit `ConnectionError` | Known connection/transport errors now return neutral `503`; unexpected errors return neutral `500`, keeping exception details in server logs. An outage can still prevent normal alert persistence and care-team handoff; emergency help must remain available independently. |

**Corrected nurse-login test:** `test_open_nurse_api_needs_a_login_before_real_patients` now uses `anon` and requires `401`, with its stale expected-failure marker removed. Previously it used `raw`, which inherits a logged-in demo-admin cookie from `tests/conftest.py`; that failure did not prove anonymous access. The ordinary authentication test `test_anonymous_gets_401_json_on_the_nurse_api_and_public_routes_stay_open` also explicitly requires `401` for `/api/comms/care/1`, alerts and patient APIs. Do not report “the nurse API has no login” as a current defect.

Focused verification of the corrected nurse-login test: **1 passed in 16.95 seconds**, recorded in `.build/pytest-nurse-access-final.log`. This is separate from the already-running combined suite, which loaded the historical marker before this edit.

Focused webhook hardening verification: **33 passed, 334 deselected in 71.53 seconds**, recorded in `.build/pytest-webhook-hardening.log`. This includes the three corrected callback assertions, valid/invalid callback contracts and nine new local security tests; it does not establish a real provider call or deployed callback delivery.

## Other prototype limits

- Dedicated department accounts remain Planned. Bed operations and hospital overview use the existing hospital-admin login; this is not the complete five-role provisioning system.
- Bed/OTP/reminder/discharge concurrency protection is for one application process. A production multi-worker setup needs transactional/shared coordination and persistence verification against its actual database.
- Appointment requests and scheduling exist. Delivered appointment notifications, teleconsultation and the availability-editing screen remain unfinished. Medicine voice reminders work only while the visible page is open; closed-app push and family missed-dose delivery remain Planned.
- Discharge print renders saved doctor-authored text. Publishing does not discharge a bed or change medicines, and no clinical instructions are generated by this module.
- Tamil/Malayalam wording needs native-speaker review. The OTP page currently supports English/Hindi rather than the entire four-language patient interface.
- Final browser/mobile and actual print-dialog verification must be recorded separately from module tests. Automated tests use sample data and isolated storage, not production credentials or real patients.

## Historical documentation to avoid treating as current

- [FEATURE_STATUS.md](../FEATURE_STATUS.md) now explicitly identifies its remaining content as the 10 October snapshot. Its old counts, “no slides” and provider statements should not be reused as current facts.
- [CLAUDE_SUBMISSION_QA.md](CLAUDE_SUBMISSION_QA.md) and [CLAUDE_FIX_HANDOFF.md](CLAUDE_FIX_HANDOFF.md) record an earlier QA run. The three OTP-resend, registered-patient ID-shortcut and forged-forwarding-header cases are now ordinary passing tests, with their markers removed. Their former “open/xfail” labels and old fixture description need a dated addendum if those reports are circulated.
- `CLAUDE.md` has a current-handoff notice, but historical lines still call the PIN a “one-time desk code.” The implementation and current registry correctly describe a reusable PIN fallback.
- The local registry now describes authenticated patient access, admin bed/overview prototypes, patient AI choice and doctor-authored discharge print honestly. Its **Live** status means working with sample data in this local prototype; it is not a deployed-provider or clinical certification claim.

Use [CODEX_IMPLEMENTATION_HANDOFF.md](../CODEX_IMPLEMENTATION_HANDOFF.md) as the current implementation record, with the final test and deployment result added when actually completed.
