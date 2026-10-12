# SpiroBuddy

## ICMR ethical guidance

Aarogya Saathi's design is informed by ICMR's [healthcare AI ethical guidance (2023)](https://www.icmr.gov.in/ethical-guidelines-for-application-of-artificial-intelligence-in-biomedical-research-and-healthcare) and [human-participant research guidelines (2017)](https://ethics.ncdirindia.org/icmr_ethical_guidelines.aspx/Default.aspx). The prototype includes optional AI consent, clinician approval of prescriptions, scoped access and transparent simulation. **Full guideline assessment, independent validation and applicable institutional ethics review remain pending. No ICMR approval, certification or full compliance is claimed.** See [the safeguards and remaining-work mapping](docs/ICMR_ETHICS_CONTEXT.md).

**After big surgery, the hospital stays connected to the patient at home.**
SpiroBuddy combines a proposed clip-on incentive-spirometer unit, a voice breathing coach, a patient app, a nurse dashboard and family updates. The physical attachment remains unbuilt and untested; demo breaths are simulated and reported sessions do not prove exercise completion. The app puts the doctor's approved prescription on the patient's phone for reference.

Healthcare & Wellbeing track. **Fake patients only. Not a medical device. Not for clinical use.**

<!-- FOUNDER: add your disclosure sentence here (verdict A1) -->

## Try it (live demo)

| What | Link |
|---|---|
| Start here (the story, impact, trust, vision, architecture) | https://spirobuddy.onrender.com/ |
| Patient app – Ravi, Hindi voice coach, no login | https://spirobuddy.onrender.com/app.html?id=1 |
| Hospital login (one-click demo buttons) | https://spirobuddy.onrender.com/login.html |
| Nurse dashboard (after login) | https://spirobuddy.onrender.com/dashboard.html |

The free server may take up to a minute to wake up if nobody has used it for a while.

### A two-minute tour
1. **Patient app:** open Ravi's app, press **Start**, and tap a demo breath. The coach speaks in Hindi, and the session is saved.
2. **Medicines:** in the app, tap **मेरी दवाइयाँ** (My medicines). You see today's medicines from Dr. Meera Nair. Tap **Show at the medicine shop** for a full-screen prescription with a QR code. Scanning the QR opens the hospital's copy, marked "Current".
3. **Hospital:** log in with **Try as Doctor**. The triage list puts the most urgent patient at the top. Open Ravi → **Medicines** to write or change a prescription and send it to his phone.
4. **Safety:** in the app, **I do not feel well** tells the nurse at once. Red-flag words always get the fixed message "Please contact your nurse now. In an emergency call 112."
5. **Family:** Amit's page shows Ravi's progress, limited to what Ravi agreed to share.

### Demo accounts (fictional, demo mode only)

| Who | Email | Password |
|---|---|---|
| Hospital admin | `admin@demo-general.example` | `demo-admin-2026` |
| Dr. Meera Nair | `meera.nair@demo-general.example` | `demo-doctor-2026` |
| Sister Anjali (nurse) | `anjali@demo-general.example` | `demo-nurse-2026` |
| Second hospital admin (to see that hospitals are kept apart) | `admin@demo-riverside.example` | `demo-riverside-2026` |

## Honest status

Every feature carries exactly one label, from one registry (`backend/app/features.py`, served at `/api/features`):

- **Live:** works in this demo today, with fake patients.
- **Simulated:** works, but its input or its sending is a built-in simulator (for example, the breaths and the WhatsApp phone).
- **In development:** partly built and not switched on, for example appointments, the document vault and missed-dose alerts.
- **Planned:** not built; shown only as a disabled card with the reason.

The AI never diagnoses and never changes a medicine. It writes short coaching summaries, with fixed template text whenever no AI key is set or a call fails.

## How it is built

- **Server:** Python + FastAPI. **Front end:** plain HTML, CSS and JavaScript (no build step).
- **Data:** Supabase (Postgres) when configured, otherwise a local SQLite file. One rulebook (`backend/app/authz.py`) decides who may see which patient. Every write is logged.
- **Logins:** staff use email and password. Patients and family use a personal link (no password). The pharmacist uses the QR code.
- **Works with no hardware and no API keys:** simulator mode, recorded voice clips and template text.

More: [architecture and contracts](docs/ARCHITECTURE.md) · [scale and cost](docs/SCALING_AND_COST.md) · [working beside a hospital's own software](docs/INTEROPERABILITY.md) · [company structure](docs/COMPANY_STRUCTURE.md)

## Run it on your computer (Windows)

```
powershell -ExecutionPolicy Bypass -File scripts\run.ps1
```

Then open http://localhost:8000. The script sets up the Python environment by itself if it is missing. Copy `.env.example` to `.env` to add optional keys; everything works without them.
