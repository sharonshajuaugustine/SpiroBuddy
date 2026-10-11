# Brief – patient login with hospital registration number + OTP (founder, Mon 12 Oct 2026, 01:53 IST)

**Founder's words:** "Why do patients need a registration number as well as another six-digit number from the hospital slip? Just keep it the registration number and then an OTP to the phone number the patient used when registering. If the patient came in from a sudden accident, keep that aside as a special case: they can't check their phone until they are conscious again."

**This replaces `REGNO_PIN_BRIEF.md` as the patient-facing design.** The PIN work built on 12 Oct is not thrown away: it becomes the staff-issued **desk code** used in the special cases below.

## 1. The honest limit (say it the same way everywhere)
A real OTP by SMS cannot be sent yet. In India it needs a paid SMS service and DLT registration of the sender name and the message text with the telecom operators, which takes days. So:
- **The login flow is real; the delivery is Simulated.** The code appears in an on-screen "phone" box (and in the phone simulator), labelled Simulated, instead of arriving by SMS.
- Registry keys: `auth.patient_otp` ("Patient logs in with hospital number + a code sent to their phone") = **simulated**; `auth.otp_sms` ("Code sent by SMS") = **planned**; `auth.patient_regno` (the desk code) = whatever it has earned. Never call any of it "secure" or "safe"; say what it does.

## 2. Normal case
1. **At registration** the staff type the patient's phone number (`patients.phone`, exists in both stores) next to the registration number (`patients.mrn`), and read it back to the patient.
2. The patient opens `/patient-login.html`, types the **registration number**, and taps **Send my code**.
3. The server finds the patient by hospital registration number (ignoring case and spaces). If a phone number is on file it makes a 6-digit code, keeps **only a hash** of it with an expiry and a try counter, and hands the code to the delivery adapter:
   - `simulated` (default, and the only one today): the code goes to the phone simulator; in DEMO_MODE the answer also carries it so the page can show it in the sample phone box.
   - `sms`: a stub that says "not set up" (Planned).
4. The page always answers the same way, whether or not the number exists or has a phone: "If the hospital has a phone number for you, a code is on its way. No code after two minutes? Please ask the ward desk." (So nobody can use the page to find out which numbers exist.)
5. The patient types the code → the same patient session as today → the patient app.

**Limits:** a code works once and for 10 minutes (kind to slow, elderly users); 5 wrong tries lock that patient's login for 15 minutes; a new code at most once a minute and 5 an hour per patient, plus a per-IP limit; every request and every try is audited, never with the code.

**Storage (no schema change, no new Supabase paste):** keep the code's hash, expiry and counters in the existing `app_settings` table under the key `otp:<patient id>` (the table exists in SQLite and in `schema_v2.sql`). Delete the row on success.

## 3. Special cases
| Case | What happens |
|---|---|
| **No phone on file** – admitted unconscious after an accident, no phone with them, or no phone at all | Staff register the patient with the phone box empty. The record shows **"Phone number pending"**. There is no app login for that patient yet, and nothing in the hospital's own work depends on it: doctors and nurses see and do everything on their side. When the patient is awake and agrees, staff add the number, and the normal case applies from then on. |
| **The code does not arrive, the phone is lost, or the number changed** | Staff check who the person is at the desk, correct the phone number if needed, or give a **one-time desk code** (the 12 Oct PIN work: made by the server, shown once, stored only as a hash, printed on a slip). Target: the desk code works once and for 24 hours. |
| **A family member's phone instead of the patient's** | Only with the patient's recorded consent. For a patient who cannot consent, it depends on the hospital's own policy for next of kin: **Planned**, not built, needs a real hospital's input. |
| **Patient has no smartphone** | No app login is needed. The hospital side works as usual; reminders by call or WhatsApp to a basic phone are the existing (simulated) channels. |

## 4. Build notes
- **New:** `backend/app/patient_otp.py` (make, hash, expire, verify, limits, delivery adapters). Routes in `backend/app/routes_me.py`: `POST /api/me/otp/request {registration_no}` and `POST /api/me/otp/verify {registration_no, code}`; both public paths (`PUBLIC_PATHS` in `main.py`). Reuse the session helper, the lockout idea, the generic wrong-login message and the rate limiter from the PIN work.
- **Page** `web/patient-login.html` + `web/js/patient-login.js`: two steps (number → code), English, Hindi, Tamil, Malayalam, elderly-first; the sample phone box (DEMO_MODE only, labelled Simulated) shows the code; a small link "I have a desk code from the hospital" opens the old number + desk-code form.
- **Staff card** on `web/patient.html` (`web/js/patient-login-card.js`): shows the phone on file with only the last two digits visible, or "Phone number pending"; staff with `patient.edit` can add or correct it; "Make a new PIN" is renamed "Give a one-time desk code".
- **Seed:** every sample patient gets a clearly non-dialable sample number (Indian mobile numbers never start with 0, so use `+91 00000 001xx`). One sample patient has no phone, to show "Phone number pending".
- **Tests** (`tests/test_patient_otp.py`): request → verify → own data only; same answer for an unknown number and for a patient without a phone; the code is never stored in plain text and never in the audit detail or the logs; a code works once; expiry (freeze time); 5 wrong tries lock; resend and hourly limits; the code is returned to the page only in DEMO_MODE; desk code still works; staff of another hospital cannot see or change the phone number (404); a nurse without `patient.edit` cannot change it (403).
- **Wording:** follow the tone rule in `STATE.md` ("Sample patient", one calm line, status word "Simulated").

## 5. Later (after the hackathon)
1. A paid SMS service and DLT registration, or WhatsApp's own login-code messages; then `auth.otp_sms` can go Live.
2. Check the phone number at registration by sending a code to it at the desk.
3. Family-phone access with consent, and the next-of-kin policy, designed with a real hospital.
