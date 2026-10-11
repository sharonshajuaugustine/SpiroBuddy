# 13 – Arogya Sathi: the whole-hospital platform (founder's plan, Mon 12 Oct 2026, ~01:00 IST)

**Name:** **Arogya Sathi** ("health companion") – the app in the Play Store and the App Store. SpiroBuddy's breathing coach and clip-on device become one part of it (see open question 1).

## 1. Who uses it, on what

| Account | Device | Created by | What they do |
|---|---|---|---|
| **Hospital** | Laptop | Us (the company sets it up on site: name, theme, logo – plan 12) | Whole-hospital view: patients checked in and out, beds in use, departments, staff; hospital settings |
| **Department** | Laptop | The hospital | Registers new patients when they come for an appointment; rooms and beds (who is where, their condition, under which doctor); appointments; nurse duty roster, room assignments, meetings |
| **Doctor** | Laptop | The hospital | Today's list (who is next, e.g. an echo appointment), patient details (age, condition, notes), writes prescriptions; saving updates the department and hospital views at once |
| **Nurse** | Phone (Arogya Sathi app) | The department | Her duty schedule, her rooms and patients, tasks, meetings, alerts |
| **Patient** | Phone (Arogya Sathi app) | The department (registration number) + doctor (prescriptions) | Sees every prescribed medicine; a printable PDF of the prescription; medicine times with "I took it"; a **spoken reminder** when a dose is missed; pharmacy screen with QR; breathing coach if given a spirometer |

Accounts hang from the hospital: Hospital → Departments → Doctors and Nurses; each Patient belongs to a department and a doctor. Login with credentials made by the level above (patients: registration number + PIN, OTP later).

## 2. What already exists in the code (reuse)
- Hospitals kept apart, staff logins (admin, doctor, nurse), departments as a staff field, nurse access keys, audit log (`authz.py`, `routes_auth.py`).
- Doctor writes a prescription → patient's phone → pharmacy screen + QR (`routes_meds.py`, `meds.html`, `prescribe.html`).
- Dose tracking ("I took it" = reported), voice coach and recorded/browser voice (`voice.js`), call and WhatsApp simulators with the reminder ladder (`comms/`).
- Plans: registration number + PIN (`docs/rebuild/REGNO_PIN_BRIEF.md`), per-hospital branding and store apps (plan 12), importing a hospital's data (Contract L).

## 3. New pieces to build (in order of value)
1. **Department account + department page:** a new role `department` (between hospital admin and staff). Pages: register a patient (registration number, name, age, contact, doctor), **bed board** (rooms × beds: patient, condition in plain words chosen by staff, doctor, admitted on), check-in / check-out.
2. **Hospital overview:** counts from the department data – checked in today, checked out, beds occupied / free, by department.
3. **Doctor's day:** next patients and appointments, the patient record (age, condition, notes), prescribe (exists) – saving shows up in the department and hospital views.
4. **Patient app:** prescriptions + **printable PDF** (print-ready page first; a server PDF later), medicine times with "I took it", **spoken missed-dose reminder** (in the app: voice clip in their language; when the app is closed: a phone notification in the store app, or the existing automated call – Simulated in the demo), pharmacy screen.
5. **Nurse app (phone):** duty roster, assigned rooms, tasks, meetings (department makes the roster).
6. **Store apps "Arogya Sathi":** one app per store wrapping the web app (Android Trusted Web Activity; iOS Capacitor with real native parts – notifications), rebranded inside after login (plan 12).

## 3b. Connected devices (founder, ~01:10 IST)
- **Device modules:** the SpiroBuddy spirometer clip-on is **device module v1**. Later modules connect the same way over **Bluetooth**: e.g. pulse oximeter, blood-pressure cuff, peak-flow meter, other breathing or exercise devices the hospital lends out (each one Planned until built).
- **Pairing from either phone:** the patient's phone (main path) or the nurse's phone (set-up and checks on the ward).
- **Placement:** **patient app** – a big, always-visible card on the home screen ("My device: Spirometer – Start") and the **Breathing** tab, only when the hospital assigned that patient a device. **Nurse app** – tucked under **More → Devices** (pair, check battery, hand over / take back), out of the way of daily work.
- **Technical fact:** Bluetooth from a web page works in Chrome on Android, not in Safari on iPhone → iPhones need the store app (Capacitor Bluetooth plugin). Each device type gets one small "driver" that turns its readings into the same format, so new devices plug into the same screens.
- **Regulation:** a device that measures a patient may fall under India's Medical Devices Rules 2017 (CDSCO); claim only "practice and recording" until we have the regulator's written view (already on the roadmap).

## 4. Safety and honesty rules for the new parts
- **Patients never switch medicines off by themselves.** "Choose which medicines to continue" becomes: the patient can tell the doctor "I stopped this / I have side effects" (sent to the doctor as a report); the schedule changes only when the doctor changes it. Reminder **times** can be shifted by the patient within the doctor's plan.
- Patient condition is written by staff in plain words; the app never diagnoses or suggests a dose.
- Nothing to do with money (no bills, prices, insurance).
- Health data law: India's DPDP Act 2023 applies (consent, purpose, deletion on request) – design for it; claim nothing until checked.

## 5. Open questions for the founder
1. **Names:** is "Arogya Sathi" the product and "SpiroBuddy" its breathing module, or the company? The hackathon entry and live site are named SpiroBuddy – renaming everything before the video is risky; suggested for tonight: "Arogya Sathi, with the SpiroBuddy breathing coach" in the deck, site unchanged.
2. **Check the name before using it publicly:** search the Play Store, App Store and the trademark registry for "Arogya Sathi" / "Aarogya Saathi" (similar names may exist, and it is close to the government's "Aarogya Setu").
3. Which departments first (e.g. surgery, cardiology)? What fields does a bed board need in your hospitals? (needs research with a real nurse)

## 6. What to do tonight vs after the hackathon
- **Tonight (before the 03:00 freeze):** the deck tells this whole plan as the roadmap (Planned badges), the demo shows what is live; build only the registration number + PIN login (brief exists). Add the new pieces as Planned keys in `features.py`.
- **After:** department + bed board → hospital overview → doctor's day → patient PDF + spoken reminders → nurse app → store apps. Roughly: a working web version of the first three in 3–4 weeks with a small team; store apps after a pilot hospital agrees (estimate).
