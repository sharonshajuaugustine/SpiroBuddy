"""Feature status registry: the ONE source of truth for every status badge (spec §8.16, plan §3.6).

Each feature has: key, name, status, where (the place it appears) and note (one plain line).
Status is exactly one of:
    live            works in this demo today (always with fake patients)
    simulated       works, but its input or its sending is a built-in simulator
    in_development  partly built; not switched on
    planned         not built; shown as a disabled card with the reason

Pages read this through GET /api/features (public). docs/FEATURE_STATUS.md is generated from it.
Rules for a note: one short line, plain words, and never a claim we can't back (see NEVER_SAY).
"""
from __future__ import annotations

import re

from fastapi import APIRouter

STATUSES = ("live", "simulated", "in_development", "planned")
STATUS_LABEL = {"live": "Live", "simulated": "Simulated", "in_development": "In development",
                "planned": "Planned"}

# Words a note must never use (the project's never-say lists). tests/test_platform.py checks this.
NEVER_SAY = re.compile(
    r"approved|compliant|certified|validated|real[- ]time monitoring|prevents?\s+pneumonia|"
    r"reduces?\s+readmissions?|abdm[- ]integrated|works with any spirometer|accurately|"
    r"clinically proven|guarantee|\bfirst\b|\bcures?\b", re.I)


def _f(key: str, name: str, status: str, where: str, note: str) -> dict:
    return {"key": key, "name": name, "status": status, "where": where, "note": note}


FEATURES: list[dict] = [
    # ---- 8.1 public story site
    _f("public.landing", "Public story site", "live", "/",
       "Short pages that explain the problem, the product and its limits."),
    _f("public.impact", "Impact page", "live", "/impact.html",
       "Every number cites its source or is labelled estimate, assumption or target."),
    _f("impact.calculator", "Impact calculator", "live", "/impact.html",
       "Sliders give rough estimates only; no health-outcome claims."),
    _f("impact.metrics", "Live demo metrics", "simulated", "/impact.html",
       "Counts come from this site's sample patients, not from real use."),
    _f("public.trust", "Trust and safety page", "live", "/trust.html",
       "Shows which rules we designed for; no outside body has reviewed the product."),
    _f("public.vision", "Vision and roadmap page", "live", "/vision.html",
       "Business model in words, with labelled estimate ranges only."),
    _f("public.architecture", "Architecture page", "live", "/architecture.html",
       "System diagram with every box coloured by its status."),
    _f("segment.post_surgery", "Recovery after heart, chest and upper-tummy surgery", "simulated",
       "/impact.html", "The current focus; this site runs with sample patients."),
    _f("segment.prehab", "Breathing practice before surgery (prehabilitation)", "planned",
       "/impact.html", "Needs its own care plan and a clinical adviser."),
    _f("segment.post_tb", "Rehabilitation after TB treatment", "planned", "/impact.html",
       "Later segment; needs a programme partner."),
    _f("segment.copd", "Long-term lung conditions (COPD)", "planned", "/impact.html",
       "Later segment; needs clinical guidance."),

    # ---- 8.2 login and access
    _f("auth.staff_login", "Staff login (email and password)", "live", "/login.html",
       "Demo-grade login with hashed passwords, 12-hour sessions and attempt limits."),
    _f("auth.doctor_signup", "Doctor sign-up with a hospital join code", "in_development", "/signup.html",
       "The hospital admin can require a check before a new doctor gets in."),
    _f("auth.nurse_keys", "Nurse access keys", "in_development", "Hospital · Access keys",
       "A doctor shares chosen patients and chosen permissions; a key can be revoked."),
    _f("auth.patient_link", "Patient link or QR, no password", "live", "Patient app",
       "A personal link opens the app; the link can be replaced at any time."),
    _f("auth.sso_otp", "Hospital SSO / OTP login", "planned", "Hospital · Settings",
       "Needs the hospital's own identity system; the demo uses a simple login."),
    _f("security.limits", "Attempt limits and upload checks", "live", "Whole site",
       "Limits on login tries and AI calls; an uploaded hospital logo is checked and re-encoded."),

    # ---- 8.3 hospital admin
    _f("admin.hospital_profile", "Hospital profile", "in_development", "Hospital · Settings",
       "Name, city, languages, departments and wards (fictional hospital)."),
    _f("admin.staff", "Staff management", "in_development", "Hospital · Staff",
       "Check, disable, re-enable and reset staff accounts."),
    _f("admin.join_code", "Join code", "in_development", "Hospital · Staff",
       "Show, copy or replace the code doctors use to sign up."),
    _f("admin.settings", "Hospital settings", "in_development", "Hospital · Settings",
       "Grace minutes, quiet hours, daily routine, who may confirm prescriptions, AI on or off."),
    _f("admin.reports", "Reports and CSV exports", "planned", "Hospital · Governance",
       "Exports of patients, doses and visits come after the demo."),
    _f("tenancy.hospitals", "Separate hospitals in one system", "live", "Whole site",
       "Every record carries its hospital; the app checks it on each request, with tests."),
    _f("db.rls_per_hospital", "Postgres per-hospital row security", "planned", "Hospital · Settings",
       "Today the app layer does the check; database-level rules are the next step."),
    _f("hospital.self_registration", "Hospitals register themselves", "planned", "/vision.html",
       "Today a hospital is set up by us; self sign-up needs identity checks."),

    # ---- 8.4 doctor workspace · 8.5 nurse workspace
    _f("doctor.my_patients", "My patients (triage list)", "live", "Hospital · Patients",
       "Sorted so the people who need a call come at the top."),
    _f("doctor.enrol", "Register a patient", "live", "/register.html",
       "Hospital number, phone, doctor and care details; itemised consent remains In development."),
    _f("doctor.handout", "Printed patient handout", "in_development", "Hospital · Patient chart",
       "QR code, daily plan and nurse phone in large text."),
    _f("nurse.triage", "Nurse triage and tasks", "live", "Hospital · Home",
       "Fixed rules pick who needs a call; no AI decides."),
    _f("nurse.scope", "Nurses see only their patients", "live", "Hospital · Patients",
       "The server limits which patients and actions a nurse can open (covered by tests); the screen for making keys is In development."),
    _f("hospital.bed_operations", "Hospital beds and admissions (prototype)", "live", "/department.html",
       "The hospital admin records beds, admission, transfer, discharge, cleaning and ready states; dedicated department accounts are Planned."),
    _f("hospital.overview", "Hospital operations overview (prototype)", "live", "/hospital-overview.html",
       "Admin-only counts come from recorded bed operations, not breathing activity; no external hospital-system integration."),
    _f("auth.department", "Dedicated department login", "planned", "/vision.html",
       "Department operations use the hospital admin account; separate department provisioning and permissions are not implemented."),

    # ---- 8.6 patient chart
    _f("chart.tabs", "Patient chart", "in_development", "Hospital · Patient chart",
       "Breathing, medicines, visits, papers, care team, notes and device in one place."),
    _f("chart.timeline", "Chart timeline", "in_development", "Hospital · Patient chart",
       "Every save shows who did it and when."),
    _f("chart.notes", "Consultation and staff notes", "live", "/patient.html",
       "Doctors save consultation notes with author and time; visible only to the care team."),
    _f("programme.status", "Pause, complete or stop a programme", "in_development", "Hospital · Patient chart",
       "Paused, stopped or deceased turns reminders and calls off at once."),

    # ---- 8.7 prescriptions
    _f("auth.patient_regno", "Hospital number + reusable PIN fallback", "live",
       "/patient-pin.html", "Staff-issued PIN with attempt limits; not a one-time desk code."),
    _f("auth.patient_otp", "Hospital number + phone-code login", "simulated",
       "/patient-login.html", "Single-use expiring code displayed on a sample phone; SMS is Planned."),
    _f("auth.otp_sms", "Login code sent by SMS", "planned",
       "Patient app", "Needs a paid SMS service and telecom (DLT) registration."),
    _f("hospital.branding", "Each hospital's own name and logo inside the patient app", "live",
       "Patient app", "Shown at the top of the patient app and the medicines page; set by the hospital admin. "
       "Safety messages and status labels stay fixed."),
    _f("hospital.pwa_install", "Home-screen icon with the hospital's own name and logo", "planned",
       "/vision.html", "Each hospital gets its own web address; installing from its QR shows its logo."),
    _f("hospital.import", "Move a hospital's doctors, departments and patients in from a spreadsheet", "planned",
       "/vision.html", "A practice run before anything is saved; old prescriptions wait for a doctor to confirm them."),
    _f("store.apps", "SpiroBuddy in the Play Store and the App Store", "planned", "/vision.html",
       "One app for all hospitals; it shows the hospital's name inside after login."),
    _f("doctor.my_day", "Doctor's 'My day' page", "live", "/doctor-day.html",
       "Visit requests, proposed times and scheduled visits. Prescriptions ending and patients to call remain planned."),
    _f("doctor.ot_reminders", "Operation-theatre reminders for doctors", "planned", "Hospital · Home",
       "Needs the hospital's own theatre schedule from its system."),
    _f("rx.patient_phone", "The doctor's prescription on the patient's phone", "live",
       "Patient app · Medicines",
       "The doctor writes it in the hospital software; the patient sees every medicine at once."),
    _f("rx.pharmacy_screen", "Show the prescription at the pharmacy counter", "live",
       "Patient app · Medicines",
       "A clear screen to show the chemist instead of paper; sample data, not tried with a real pharmacy."),
    _f("rx.verify_qr", "Pharmacist scans a QR to check the prescription", "live",
       "Patient app · Medicines",
       "Opens the issuing hospital's copy so the chemist can compare; no login, sample patients only."),
    _f("rx.manual", "Doctor types the prescription", "live", "Hospital · Medicines tab",
       "No AI involved; this path always works."),
    _f("rx.notepad", "Prescription notepad draft", "in_development", "/prescribe.html",
       "AI needs a configured provider and recorded consent; a manual-format draft is available."),
    _f("rx.print", "Printable prescription", "live", "/prescription-print.html",
       "Patient prints the hospital's current prescription or saves it as PDF using the browser."),
    _f("rx.ai_read", "AI drafts a prescription from a photo", "in_development", "Hospital · Review",
       "Gemini copies what is written on sample prescriptions; a person checks every line."),
    _f("rx.patient_upload", "Patient or family sends a prescription photo", "planned", "Patient app · Medicines",
       "It waits for a doctor or permitted nurse; no reminder starts before that."),
    _f("rx.review", "A person confirms every prescription line", "in_development", "Hospital · Review",
       "Unclear fields stay blank and amber; nothing is guessed."),
    _f("rx.normaliser", "Indian dose notation to times (1-0-1, BD, TDS)", "in_development", "Hospital · Review",
       "Fixed rules turn the written frequency into times; no AI sets a time or dose."),
    _f("rx.handwriting", "AI reads handwritten prescriptions", "in_development", "Hospital · Settings",
       "Experimental and off by default; staff type handwritten papers."),
    _f("rx.line_crops", "Photo crop beside each line", "planned", "Hospital · Review",
       "Would show the exact part of the photo for each line."),
    _f("rx.interaction_checks", "Drug-interaction and dose-range checks", "planned", "/vision.html",
       "Deliberately not built: would be clinical decision support."),

    # ---- 8.8 medicine reminders and dose tracking
    _f("doses.reminders", "Spoken medicine reminders in the open app", "live", "/meds.html",
       "Patient enables voice on Medicines; reminders work while the page is open and visible."),
    _f("doses.tracking", "Dose tracking (reported by the patient)", "live", "Patient app · Medicines",
       "A tap is shown as reported, never as taken; nobody measures it."),
    _f("doses.missed_alert", "Missed-dose alert to the nurse", "live", "/dashboard.html",
       "Amber follow-up after the grace time; no dosing advice. Family delivery is Planned."),
    _f("doses.web_push", "Reminders when the app is closed (Web Push)", "planned", "Patient app",
       "Today reminders show only while the app is open."),
    _f("doses.offline_queue", "Save taps while offline", "planned", "Patient app",
       "Today a tap needs a connection."),
    _f("comms.ivr_reminders", "Medicine reminder by phone call or WhatsApp", "planned", "Hospital · Demo",
       "Today medicine reminders are in the app only."),

    # ---- 8.9 appointments
    _f("appt.booking", "Ask for and book a visit", "live", "/patient-visits.html",
       "The patient asks; the hospital confirms, proposes another time or declines. In-app only; no SMS or WhatsApp."),
    _f("appt.availability", "Doctor availability and slots", "in_development", "Hospital · Availability",
       "Weekly times plus leave days; a slot can't be booked twice."),
    _f("appt.reminders", "Visit reminders in the app", "planned", "/patient-visits.html",
       "No appointment notification is delivered today; planned reminders are separate from the current visit list."),
    _f("appt.teleconsult", "Tele-consult", "planned", "Patient app · Visits",
       "Video visits need their own rules and consent; visits are in person for now."),

    # ---- 8.10 document vault
    _f("docs.vault", "Document vault", "in_development", "Patient app · Papers",
       "Photos and PDFs are checked, re-encoded and served only after a permission check."),
    _f("docs.ai_suggest", "AI suggests a paper's type, title and date", "in_development", "Hospital · Papers tab",
       "It never reads out or interprets a result; a person can change the suggestion."),
    _f("docs.abdm_link", "ABDM link (view in your health locker)", "planned", "Patient app · Papers",
       "Needs ABDM sandbox onboarding and the patient's consent."),
    _f("abha.field", "ABHA number field", "planned", "Hospital · Patient chart",
       "We collect no government ID today."),

    # ---- 8.11 spirometer and coach
    _f("coach.breath", "Breathing coach", "simulated", "Patient app · Today",
       "Breaths come from the built-in simulator until the clip-on unit is connected."),
    _f("coach.voice", "Voice coach in 10 Indian languages and English", "live", "Patient app",
       "Recorded clips, with the browser voice as the fallback."),
    _f("coach.classifier", "Breath labels and scores", "simulated", "Patient app · Today",
       "The model was trained on simulated breaths, not on patient data."),
    _f("coach.triage", "Triage rules (on track, watch, needs a call)", "live", "Hospital · Patients",
       "Plain rules on sessions and volumes; they never name a condition."),
    _f("device.usb", "Clip-on unit over USB", "in_development", "Hospital · Devices",
       "The firmware and the 3D design exist; no unit is built or bench-tested."),
    _f("device.ble", "Bluetooth pairing", "planned", "Hospital · Devices",
       "The unit sends by USB for now."),
    _f("device.three_ball_reader", "Three-ball reader (light gate / phone camera)", "planned",
       "Hospital · Devices", "For three-ball spirometers; the current unit fits the piston type."),
    _f("device.speaking_base", "Speaking base with SIM for homes without a smartphone", "planned",
       "Patient app", "A stand-alone unit that talks and sends data by itself."),
    _f("vitals.bluetooth", "Pulse oximeter and BP cuff by Bluetooth", "planned", "Patient app · Medicines",
       "We record no vital signs today."),

    # ---- 8.12 patient app · 8.13 family page
    _f("app.patient", "Authenticated patient phone app", "live", "/app.html",
       "Hospital number with simulated OTP, reusable PIN fallback or a hospital-issued personal link; large text and one action at a time."),
    _f("app.languages", "Screen languages: English, Hindi, Tamil, Malayalam", "live", "Patient app",
       "Tamil and Malayalam text still needs a native-speaker check."),
    _f("app.help", "Help button", "live", "Patient app",
       "Shows a fixed message and call buttons; no AI answers a health question."),
    _f("app.offline", "Last data when offline", "live", "Patient app",
       "Shows the last saved day with a clear offline notice."),
    _f("family.page", "Family page", "live", "/guardian.html",
       "A private link for one family member; shown only with the patient's consent."),
    _f("family.medicines_visits", "Family sees medicines, visits and shared papers", "planned",
       "/guardian.html", "Only what the patient agreed to share will appear."),

    # ---- 8.14 digital twin
    _f("twin.live", "Live twin of the spirometer", "in_development", "Hospital · Breathing tab",
       "Simulated input; a live view while a session is running."),
    _f("twin.replay", "Replay of the last session", "in_development", "Hospital · Breathing tab",
       "Replays the stored curve of a simulated session."),
    _f("twin.public", "Public 3D twin", "in_development", "/twin.html",
       "Runs on its own in-browser simulator."),
    _f("twin.fleet", "Device fleet twin", "simulated", "Hospital · Devices",
       "Units, battery and hand-over history are sample data."),

    # ---- 8.15 trust layer
    _f("consent.itemised", "Itemised consent", "in_development", "Hospital · Care team and consent",
       "Separate choices for reminders, family sharing, records and AI; withdraw at any time."),
    _f("consent.ai_optout", "Patient AI opt-in and withdrawal", "live", "/meds.html",
       "Authenticated choice defaults off, records consent versions and gates patient AI drafting; withdrawal preserves unrelated choices."),
    _f("consent.ai_training", "Use of data to train AI", "planned", "Hospital · Care team and consent",
       "Always off in the demo; needs an ethics committee review before any use."),
    _f("consent.teach_back", "Teach-back question at consent", "planned", "Hospital · Care team and consent",
       "A short question to confirm the patient understood."),
    _f("ai.register", "AI register", "in_development", "Hospital · Governance",
       "Every AI call is logged by reference, never by content, with the human decision."),
    _f("ai.summary", "Daily summary text", "live", "Hospital · Patient chart",
       "Three plain sentences from the day's numbers, written from a fixed template unless an AI key is set; the tag on the summary says which."),
    _f("safety.red_flags", "Red-flag words reach a person", "live", "Patient app",
       "A fixed word list triggers a fixed message and a nurse alert; no AI is involved."),
    _f("audit.log", "Audit log", "live", "Hospital · Governance",
       "Every write and every chart view is recorded with who and when."),
    _f("audit.viewer", "Audit log viewer with filters and CSV", "planned", "Hospital · Governance",
       "The log is written today; the full viewer comes next."),
    _f("audit.hash_chain", "Tamper-evident audit log (hash chain)", "planned", "Hospital · Governance",
       "Each entry would carry the hash of the one before it."),
    _f("pilot.checklist", "Pilot readiness checklist", "planned", "Hospital · Governance",
       "The 14 steps before any real pilot; none are done for a real hospital."),
    _f("data_rights.requests", "Data export and deletion requests", "planned", "Hospital · Governance",
       "A patient's request would become an admin task."),

    # ---- 8.16 future features and exports
    _f("fhir.export", "FHIR R4 export", "in_development", "Hospital · Patient chart",
       "Basic bundle for one patient; not checked against ABDM rules."),
    _f("discharge.print", "Printable discharge plan", "live", "/discharge-print.html",
       "Prints saved doctor-authored instructions with version/state notices; generates no clinical advice or medication changes."),

    # ---- 8.17 demo controls, and the existing comms
    _f("demo.controls", "Demo controls", "live", "Hospital · Demo",
       "Reset the demo data and trigger demo events; fake patients only."),
    _f("demo.seed", "Seeded demo story", "simulated", "Whole site",
       "All patients, staff and hospitals are fictional."),
    _f("demo.nightly_reset", "Nightly demo reset", "planned", "Hospital · Demo",
       "Today an admin or doctor resets the demo by hand."),
    _f("comms.alerts", "Nurse alerts inbox", "live", "Hospital · Home",
       "Alerts raised by fixed rules; a nurse acknowledges each one."),
    _f("comms.escalation", "Escalation ladder (patient, family, nurse)", "simulated", "Hospital · Demo",
       "The steps run for real; calls and messages go to the built-in simulators."),
    _f("comms.whatsapp", "WhatsApp updates", "simulated", "Hospital · Demo",
       "Messages appear in the built-in phone simulator (dry run)."),
    _f("comms.calls", "Phone calls and IVR", "simulated", "Hospital · Demo",
       "Calls play in the built-in phone simulator (dry run)."),
    _f("comms.whatsapp_real_send", "Real WhatsApp sending", "in_development", "Hospital · Settings",
       "Works only to the team's own test numbers; off for patients."),
    _f("comms.calls_real", "Real phone calls", "in_development", "Hospital · Settings",
       "Works only to the team's own test numbers; off for patients."),
]

_BY_KEY = {f["key"]: f for f in FEATURES}


def get(key: str) -> dict | None:
    """One feature by key, or None. (A page shows "Planned" for a key it can't find.)"""
    f = _BY_KEY.get(key)
    return dict(f) if f else None


def public_list() -> list[dict]:
    """Every feature, in registry order (copies, so a caller can't change the registry)."""
    return [dict(f) for f in FEATURES]


router = APIRouter()


@router.get("/api/features")
def list_features():
    """Public: the status registry [{key, name, status, where, note}] (Contract K)."""
    return public_list()
