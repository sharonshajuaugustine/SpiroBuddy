# Demo script: GuGu GaGa, Aarogya Saathi + SpiroBuddy

**Team:** GuGu GaGa. Sharon Shaju Augustine and Fathima Shifana, coworkers and former B.Sc Computer Science classmates.
**One line:** Aarogya Saathi is the hospital platform. SpiroBuddy is its breathing companion, the first module.
Everything below was rehearsed against the local copy on 12 Oct 2026 (see `CLAUDE_SUBMISSION_QA.md`). Where the live site is behind, this script says so.

## What is built, simulated and planned (say it exactly like this)

Status words are the ones in `backend/app/features.py`. Never say "live" for something marked otherwise.

| Status | What it covers |
|---|---|
| **Built (Live)** | A doctor registers a patient with the hospital number and phone. Doctor's consultation notes. The doctor types a prescription and approves it. The prescription shows on the patient's phone, with a pharmacy screen, a QR the chemist can check, and a print/PDF page. The patient taps "I took it", which is stored as **reported**, never as proof. Spoken reminders **while the page is open**. A missed dose raises an amber nurse alert after a one-hour grace time (no dosing advice). Nurse alerts inbox. Nurses see only their own patients. Each hospital's own name and logo in the patient app. |
| **Simulated** | Patient login by hospital number + OTP: the code appears in an on-screen "Sample phone", no SMS is sent. The breathing coach: breaths come from a built-in simulator. WhatsApp updates and phone calls: they play in a built-in phone simulator. |
| **In development** | The clip-on unit for an ordinary incentive spirometer (firmware and 3D design exist; **no unit is built or bench-tested**). AI notepad draft (the manual format works; AI needs a provider and recorded consent). Visit booking. Real calls and WhatsApp to the team's own numbers only. |
| **Planned** | SMS codes (needs a paid SMS service and DLT registration). Bluetooth. Reminders when the app is closed (web push). Family seeing medicines. Tele-consult. Hospital self sign-up. |
| **Not in this demo** | Department, bed and whole-hospital views (another session is building them and QA did not test them). Payments (never part of the product). |

**Do not say:** anything about real patients, pilots, hospitals using it, clinical outcomes, accuracy of measurements, or "AI reads prescriptions" (the AI draft needs a provider that is off in this setup). The patient app is a web app, not a store app. Do not claim family messaging works for missed doses (it does not exist).

## Accounts and sample data

| Role | How to sign in | Notes |
|---|---|---|
| Doctor, Dr. Meera Nair | `/login.html` then **Try as Doctor** | Only doctors write prescriptions. Sees her own patients. |
| Nurse, Sister Anjali | `/login.html` then **Try as Nurse** | Sees Dr. Meera's patients, can acknowledge alerts, cannot prescribe. |
| Admin desk | `/login.html` then **Try as Admin** | Can register patients; cannot prescribe. |
| Patient (new) | `/patient-login.html`: hospital, hospital number, **Send my code**, type the code shown in the Sample phone box | Use the number you register in step 2. |
| Patient (sample) | same page, tap **Use Ravi's hospital number** | Ravi Kumar, `DGH-000001`. |
| Other hospital (backup, isolation) | `admin@demo-riverside.example` / `demo-riverside-2026` | Dawnlight Riverside Clinic. Sees none of Dawnlight General's patients. |

All names, numbers and passwords are fictional sample data. Use fake phone numbers like `+910000000098`.

## Before you go on (10 minutes)

1. Decide where you present. **Plan A is the live site only if Codex has redeployed and `/patient-login.html` and `/register.html` open (they returned 404 at 04:10 today).** Otherwise present Plan B, the local copy (below). Open `/api/health` first; the live site sleeps and the first load can take about a minute.
2. Open three windows: **A** doctor (desktop width), **B** patient phone view (Chrome DevTools device toolbar at 375 px, or a real phone), **C** nurse (desktop width).
3. Stage the missed-dose alert **at least 2 hours before** (it cannot be made live: a dose becomes "missed" one hour after its time). Register a second sample patient, e.g. number `AS-9001`, phone `+910000000097`, tick the breathing module. Issue a prescription whose time falls shortly after you issue it (Afternoon is 14:00, Night is 21:00; the dose time must come after the issue time). One hour after that dose time the nurse inbox shows "<name>: medicine follow-up at ...". Check it on the day.
4. Do **not** click **Reset demo data** on the Demo panel (it wipes the staged patient). Do not reload the patient login page and ask for a code twice within one minute (known defect F-3: no code appears for up to 60 s).
5. Staff screens scroll sideways on a phone today (known defect F-5). Show staff screens on the desktop window and use the phone view only for the patient.
6. Skip these on screen until fixed: the note author ("Staff #2"), the header ward label "Post-op Ward 3B".

## The 3-minute presentation

| Time | Window | Do | Say |
|---|---|---|---|
| 0:00 | Landing `/` | Show "Every breath, coached and counted." and the line "Sample patients at a fictional hospital. The clip-on unit is in development; breaths here are simulated." | "We are GuGu GaGa, Sharon and Fathima, coworkers and former B.Sc Computer Science classmates. Aarogya Saathi is a hospital platform. SpiroBuddy is its breathing companion. Everything you see uses sample patients at a fictional hospital." |
| 0:20 | A: doctor | **Try as Doctor**, then **Register patient** (`/register.html`). Number `AS-1001`, name `Sample Patient One`, age 58, phone `+910000000096`, condition "lung surgery recovery (sample)", tick the breathing module, **Register patient**. | "The doctor registers the patient with the hospital's own number and the phone the hospital already has. The patient's login depends on these two." |
| 0:45 | A: doctor | **Write prescription**. Paste into the notepad: `Paracetamol \| 500 mg \| tablet \| 1 \| tablet \| 1-0-1 \| 5 \| with water` and a second line `Cetirizine \| 10 mg \| tablet \| 1 \| tablet \| 0-0-1 \| 3 \|`. Press **Prepare draft for review**. Show the "Needs review" food field; choose **After food** on both lines. Press **Send to the patient's phone**, read the confirm list, confirm. | "The notepad only prepares a draft; nothing reaches the patient yet. The doctor checks every field and approves. The AI part needs a provider, so today this is the manual format." |
| 1:20 | B: phone | `/patient-login.html`, choose the hospital, enter `AS-1001`, **Send my code**. Read the 6 digits from the **Sample phone, Simulated** box, type them, **Open my medicines**. Show the big-text medicine cards. Tap **I took it**; it turns to "Reported at ...". Tap the pharmacy button to show the full-screen card and QR. | "The code would be an SMS. In this demo it is simulated on a sample phone. The patient sees every medicine in large text. 'I took it' is recorded as reported, never as proof. The pharmacy screen replaces paper." |
| 2:00 | B then A | In B open **My breathing exercise** and **Start my exercise**, then tap **Good breath** once (simulated; the piston rises and the screen says "Breath 1 of 10"). Do not wait for the full 10 breaths on stage: a full simulated session takes about 100 seconds. Press **Finish now** if you leave early (a partial session is saved but does not count as completed). In A open the Demo panel (`/demo.html`) and press **Simulate good** for Sample Patient One; open the patient chart and show "Recent sessions". | "The clip-on device is in development and not built. Here the breaths are simulated, so the coach and the chart are real software with simulated input. We never present these as measurements." |
| 2:30 | C: nurse | **Try as Nurse**. Open the Alerts inbox (staged patient). Point at the "medicine follow-up" alert. Press **Acknowledge**; the "I am" box shows Sister Anjali. | "If a dose is not reported an hour after its time, the nurse gets an amber alert. It names the patient and gives no dosing advice. The nurse's own name is recorded." |
| 2:50 | any | Show this slide or say it: Built / Simulated / In development / Planned. | "Built: registration, prescriptions on the phone, reported doses, nurse alerts. Simulated: the SMS code and the breath input. In development: the clip-on unit, which does not exist yet. Planned: SMS, Bluetooth, reminders when the app is closed." |

## The 5-minute backup walkthrough

Use this when you have time or a judge asks for depth. Same accounts.

1. **0:00 Registration safety (doctor).** Try to register `AS-1001` again: "This hospital number is already registered". Then show that a nurse cannot: sign in as the nurse and open `/prescribe.html?id=<patient>`: "Only doctors write prescriptions", and the chart has no consultation form.
2. **0:45 Consultation.** On the patient's chart (doctor) write a short note ("Sample: comfortable, continue exercises"), **Save consultation note**.
3. **1:15 Patient in Hindi.** On the medicines screen switch to Hindi; the reminder button and print link translate. Open **Print / Save prescription as PDF**: plain words, no codes, the "sample, not for dispensing" line.
4. **2:00 Opt-in reminders.** Tap **Enable spoken medicine reminders while this page is open**. Say: "Reminders speak only while the page is open. When the app is closed, nothing reminds the patient yet. That is Planned."
5. **2:30 Wrong code and PIN fallback.** On the login page type a wrong code: "That code could not be checked". Mention five wrong codes lock it for 15 minutes. Then, as the doctor on the patient's chart, show the **Patient login** card: it says the PIN is a reusable fallback, "not a one-time code", and "Phone number pending" if no phone is on file.
6. **3:15 Not assigned means no breathing.** Register a patient without the breathing box. Their medicines screen has no breathing link; their breathing page says "Breathing exercise is not assigned".
7. **3:45 Hospital isolation.** Sign in as `admin@demo-riverside.example`: no Dawnlight patients, and a Dawnlight number typed at the Riverside hospital gets no code.
8. **4:15 Pharmacist check.** Open the QR link (`/rx.html?t=...`) in a new tab: "Current, issued by the hospital", short name only. Replace the prescription as the doctor and reload: "No longer current".
9. **4:45 Close** with the Built / Simulated / In development / Planned table above.

## If something fails

| Problem | Do this |
|---|---|
| Live site slow or asleep | Open `/api/health` five minutes early. If a page takes more than a minute, switch to Plan B. |
| Live site lacks the new pages (404) or is down | **Plan B, local copy:** save the launcher below as `C:\Temp\sb_launch.py`, then from the project folder run `.venv\Scripts\python.exe C:\Temp\sb_launch.py` and open `http://127.0.0.1:8021`. Do not use `scripts\run.ps1` for a rehearsal: it reads `.env`, which holds the live database and keys. |
| A provider is down (AI, voice, WhatsApp, calls, SMS) | Nothing in the 3-minute script needs one. The notepad falls back to the manual format, voice falls back to the browser voice, WhatsApp and calls play in the built-in simulator. Say "simulated" and carry on. |
| No code appears on the login page | You asked twice inside a minute. Wait 60 s and ask once. Or use the PIN: on the patient's chart press **Make a new PIN** and use `/patient-pin.html` (the PIN is shown once). |
| Registration says the number exists | Use another number (`AS-1002`) or use Ravi's button. |
| The staged alert is missing (someone reset the data) | Show the seeded alerts already in the inbox (for example "Abdul Rahman: 7 missed sessions in a row") and say the medicine alert is built but takes an hour after a dose time to appear; the screenshot is `docs/qa/evidence/m375_nurse_alert_row_after_fix.png`. |
| Nothing speaks | Skip the voice step; browsers need the page to be open and visible. |
| Phone and staff sessions mix up | Use a second browser profile or a private window for the patient. |

### Local launcher (variable names only; no secrets)

```python
import os, sys, uvicorn
sys.path.insert(0, r"C:\Users\USER\Desktop\SpiroBuddy")
for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "SARVAM_API_KEY",
          "SARVAM_AGENT_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "EXOTEL_API_KEY", "EXOTEL_API_TOKEN",
          "PUBLIC_BASE_URL"):
    os.environ[k] = ""            # blank beats the same name in .env
os.environ.update(SPIROBUDDY_DATA_DIR=r"C:\Temp\sb_demo_data", DEMO_MODE="1", DATA_BACKEND="demo",
                  DEMO_AUTOPILOT="0", COMMS_AUTO_ESCALATE="0")
uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8021)
```

After it starts, `http://127.0.0.1:8021/api/health` must say `"data_backend":"demo"` and `"data_note":"demo SQLite"`. If it says `supabase`, stop it at once. Delete `C:\Temp\sb_demo_data` for a clean start.
