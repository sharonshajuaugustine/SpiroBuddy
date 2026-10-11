# 14 – One home page per role (founder, Mon 12 Oct 2026, 03:35 IST)

**Founder's words, summarised:** every login landing on the same nurse dashboard is wrong. The hospital needs a page with all its patients, doctors, departments, staff and who is on duty – no calling features there. The doctor needs a main page for dealing with patients: enter details and records, and a **Record** button to record the consultation for the next visit. The spirometer is an **option** a doctor or nurse switches on for a patient, not something every patient does. Big, simple, easy-to-read screens – no small text. Plan the nurse and department pages so they connect.

## Who lands where after login
| Role | Lands on | Device |
|---|---|---|
| Hospital admin | `/hospital/` – Hospital overview | Laptop |
| Doctor | `/doctor.html` – My patients and the patient record | Laptop |
| Nurse | `/dashboard.html` – the ward list (needs a call / watch / on track), alerts | Phone or laptop |
| Department (Planned) | Department desk: register patients, rooms and beds, duty roster | Laptop |
| Patient | `/app.html` – their own app | Phone |

`/dashboard.html` stays reachable for every staff member (the demo video uses it).

## Hospital overview (build now)
Big number tiles: patients under care · in hospital (no discharge date) · at home (discharged) · staff on duty today. Then plain lists: **Departments** (doctors, nurses, patients in each), **Doctors** and **Nurses** (department, on duty today, patients), **Patients** (registration number, ward and bed, department, doctor, in hospital or at home). The admin ticks who is on duty today (kept in the hospital's settings, audited). Rooms and beds as a board = Planned (department module). No calls, messages or alerts on this page.

## Doctor workspace (build now)
- Left: **My patients** (big rows, search) and **Add a patient** (name, age, sex, phone, department, ward/bed, condition as written by the doctor; registration number made automatically).
- Right: the **patient record** – details (editable), allergies "as recorded by the doctor", **visit notes** (newest first, add a note), **Prescribe** (opens the existing prescription page), and a big **Record conversation** button.
- **Recording rules:** a tick "The patient agreed to this recording" is required first; a red "Recording…" bar with a timer while it runs; the audio is saved privately with the visit and can be played back next time; never shared with the patient or family automatically. A written transcript only when a speech service key is set (otherwise the badge says In development). The app never summarises or diagnoses from it.
- **Breathing exercise (spirometer) switch** per patient: off by default for new patients; a doctor or nurse switches it on with a target. When it is off, the patient app hides the breathing coach and the ward list shows no missed sessions for that patient.

## Nurse (phone) – plan, connects to the department
Today's duty and rooms (from the department's roster), the patients in those rooms with plain status words, tasks (breathing sessions due if switched on, medicines to give, calls to make), alerts, and **More → Devices** for spirometer pairing. Built later on the existing ward list.

## Department desk – plan
A new `department` login under the hospital. Registers patients when they arrive (registration number, details, doctor), keeps the **room and bed board**, books appointments, and makes the **nurse duty roster** (who handles which rooms, meetings). Everything it saves shows up at once on the hospital overview and on the doctor's and nurses' pages.

## Design rules for all staff pages
Body text 18 px or more, headings 24 px or more, buttons and rows at least 48 px tall, one main action per screen area, plain words, the shared colour palette, light and dark. Status badges from `features.py` only.
