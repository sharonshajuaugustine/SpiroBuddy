# Writes spec.json (the on-screen text for version 4). Run: python make_spec_v4.py
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
N = None


def card(kicker, title, lines, tag=N, accent="teal", style="solid", big=N, cue=N):
    return {"kicker": kicker, "title": title, "lines": lines, "tag": tag, "accent": accent,
            "style": style, "big": big, "cue": cue}


part1 = [
    {"start": "0:00", "end": "0:31", "chip": "PROBLEM SIGNIFICANCE", "graphics": [
        {"type": "title", "cue": N, "name": "Aarogya Saathi",
         "line1": "Connecting hospital care to", "line2": "the patient's phone.",
         "pill1": "Health & Well-being  ·  SDG 3", "pill2": "Team GuGu GaGa",
         "team": "Sharon Shaju Augustine  ·  Fathima Shifana",
         "foot": "Dolphin Tank India  ·  Social Impact Hackathon 2026"},
        {"type": "stats", "cue": "India's public records", "head": "After surgery: the numbers we rely on",
         "cards": [
             {"big": "49 lakh", "text": "major operations a year\nin India's public records",
              "source": "Int J Surg 2024 · 2019 data\nan undercount", "cue": "forty-nine lakh"},
             {"big": "1 in 10", "text": "adults having surgery\nhad a lung complication",
              "source": "LAS VEGAS study, Eur J Anaesthesiol 2017\n9,864 patients, 29 countries, mostly Europe",
              "cue": "one in ten"},
             {"big": "6% → 72%", "text": "used their spirometer properly on day 1;\n72% by day 3 with teaching (in hospital)",
              "source": "Small Chennai study, 60 inpatients, 2024\nNo Indian home-use data found",
              "cue": "six percent"},
         ],
         "footer": "In hospital, not at home. After discharge: patients need a clear plan, nurses need to see who needs help.",
         "footer_cue": "That was in hospital"},
    ]},
    {"start": "0:31", "end": "1:00", "chip": "UNDERSTANDING OF USERS", "graphics": [
        {"type": "cards", "cue": N, "head": "Who we design for",
         "sub": "Illustrative personas, not real people. Fictional sample data only.",
         "cards": [
             card("Patient persona", "Kamala, 68",
                  ["Home after lung surgery", "Reads Hindi", "Needs one clear screen, one action at a time",
                   "Illustrative persona, not a real patient"],
                  tag="Illustrative persona", accent="teal"),
             card("Nurse persona", "Sister Anjali, ward nurse",
                  ["Must know whom to call first, and why", "Has limited time for repeated coaching",
                   "Illustrative persona, not a real nurse"],
                  tag="Illustrative persona", accent="violet", cue="Sister Anjali"),
         ], "footer": N, "footer_cue": N},
        {"type": "cards", "cue": "Informal feedback", "head": "Informal nurse feedback",
         "sub": "Second-hand and informal. Not an interview, not a study.",
         "cards": [
             card("Concerns raised", "What she reported",
                  ["Painful breathing exercises may be skipped", "Medicine instructions can be forgotten",
                   "Discharge paperwork can be confusing", "Repeated coaching takes staff time"],
                  accent="amber"),
             card("Source label", "How to read this",
                  ["One nurse's informal feedback, relayed by a", "team member; additional themes confirmed by",
                   "phone according to the team member,", "12 October 2026."],
                  tag="Not a study", accent="grey", style="dashed"),
         ],
         "footer": "Our response: a readable care plan, and check-ins that ask why, then bring concerns to the nurse.",
         "footer_cue": N},
        {"type": "strip", "cue": "five steps", "head": "One journey, five steps",
         "steps": [
             {"title": "In hospital", "text": "Doctor registers; admin admits to a bed", "cue": "hospital, discharge"},
             {"title": "Discharge", "text": "Doctor sends medicines and care instructions", "cue": "discharge, home"},
             {"title": "At home", "text": "Kamala reads her plan; breathing coach", "cue": "home, follow-up"},
             {"title": "Follow-up", "text": "She asks for a visit; the doctor confirms", "cue": "follow-up, and"},
             {"title": "Concern", "text": "Check-in asks why; rules alert the nurse", "cue": "a concern reaching"},
         ],
         "footer": "Next: this journey on our public site, with a fictional sample patient."},
    ]},
    {"start": "1:00", "end": "1:20", "chip": "INNOVATION", "graphics": [
        {"type": "cards", "cue": N, "head": "What we add: the combination",
         "sub": "Record apps and breath trackers already exist. We do not claim to be the only one.",
         "cards": [
             card("Health-record apps", "e.g. Aarogya Setu 2.0, Eka Care",
                  ["Hold health records and reminders"], accent="grey"),
             card("Hospital breath trackers", "e.g. InSee (US)",
                  ["Base-mounted tracker, one spirometer model", "FDA-cleared (510(k) K241152)",
                   "Cleared for hospital use only"], accent="grey", cue="InSee"),
             card("Aarogya Saathi", "Joined on one hospital record",
                  ["Doctor-approved plan + dose reports", "Breathing coach (optional module)",
                   "Check-in that asks why (Simulated)", "Each hospital's own name, logo, colour"],
                  tag="Clip-on unit: In development", accent="teal", cue="We join"),
         ],
         "footer": "Sources: FDA 510(k) K241152 (InSee, Tidal Medical); record apps named as examples only.",
         "footer_cue": N},
    ]},
    {"start": "1:20", "end": "1:45", "chip": "SOLUTION QUALITY", "graphics": [
        {"type": "image", "cue": N, "img": "slide7", "tag": "3D concept render, not built", "zoom": N},
        {"type": "image", "cue": "Firmware is written", "img": "arch_device", "tag": "USB link: In development",
         "zoom": [0.325, 0.765, 2.3]},
        {"type": "image", "cue": "A laser sensor", "img": "slide8", "tag": "3D concept render, not built", "zoom": N},
    ]},
    {"start": "1:45", "end": "2:19", "chip": "SOCIAL IMPACT", "graphics": [
        {"type": "cards", "cue": N, "head": "Who gains · SDG 3",
         "sub": "Intended impact. Nothing here is measured yet.",
         "cards": [
             card("Older patients", "The doctor's plan, on one screen",
                  ["Large text, one action at a time", "Screen labels in 4 languages (Hindi shown)",
                   "Voice coach: 10 Indian languages + English", "Doctor's text is shown as typed"],
                  tag="Intended, not measured", accent="teal", cue="older patients"),
             card("Families", "Kept informed, with consent",
                  ["A private family page for one member", "Shown only with the patient's consent"],
                  tag="Intended, not measured", accent="green", cue="families follow"),
             card("Ward nurses", "Whom to call first",
                  ["Fixed rules sort who needs a call", "Alerts carry what the patient reported",
                   "Nurse minutes per day: to be measured"],
                  tag="Intended, not measured", accent="violet", cue="nurses see"),
         ],
         "footer": "Tamil and Malayalam text still needs a native-speaker check.", "footer_cue": N},
        {"type": "cards", "cue": "A one-ward pilot", "head": "What a pilot would measure",
         "sub": "Proposed: 1 ward, 20 patients, 14 days. Illustrative targets, not results.",
         "cards": [
             card("Activation", "Plan viewed within 48 hours", ["of enrolled patients"],
                  tag="Illustrative target", accent="amber", style="dashed", big="80%", cue="plan views"),
             card("Day-7 return", "Activated patients who return", ["of activated patients"],
                  tag="Illustrative target", accent="amber", style="dashed", big="60%", cue="day-seven return"),
             card("Nurse workload", "Nurse minutes per day", ["Unmeasured today", "Counted in the pilot"],
                  tag="Not measured yet", accent="grey", style="dashed", cue="nurse minutes"),
             card("Health benefit", "Not claimed",
                  ["Evidence for the exercise alone is mixed", "A study is required first"],
                  tag="Study required", accent="grey", style="dashed", cue="Evidence that"),
         ],
         "footer": "Mixed evidence: Cochrane review 2014; 2024 cardiac-surgery review. We measure follow-through first.",
         "footer_cue": "Evidence that"},
    ]},
    {"start": "2:19", "end": "2:36", "chip": "SUSTAINABILITY / BUSINESS MODEL  ·  SCALABILITY", "graphics": [
        {"type": "cards", "cue": N, "head": "Who pays: the hospital",
         "sub": "Proposed pricing, unvalidated. No paying customers.",
         "cards": [
             card("In a follow-up episode", "What the hospital gets",
                  ["Approved plan on the patient's phone", "Check-ins and the nurse's alert list",
                   "Hospital-scoped records and audit log"], accent="teal"),
             card("Proposed price", "Per care follow-up episode",
                  ["Paid by the hospital", "Unvalidated; no paying customers"],
                  tag="Proposed, unvalidated", accent="amber", style="dashed", big="Rs 1,000",
                  cue="thousand rupees"),
             card("Patients", "We do not charge patients",
                  ["No payments inside the patient,", "nurse or hospital apps"],
                  accent="green", cue="We do not charge"),
         ], "footer": N, "footer_cue": N},
        {"type": "cards", "cue": "Every record carries", "head": "Each hospital keeps its own records",
         "sub": "Two fictional sample hospitals on the same service.",
         "cards": [
             card("Sample hospital", "Dawnlight General Hospital",
                  ["Its own patients, staff and records", "Its own app name and accent colour"],
                  tag="Fictional", accent="teal"),
             card("Sample hospital", "Dawnlight Riverside Clinic",
                  ["Its own patients, staff and records", "Its own app name and accent colour"],
                  tag="Fictional", accent="violet"),
             card("Modules", "Breathing: switched on per patient",
                  ["The spirometer coach is module one", "More modules and devices: Planned",
                   "Production scaling: not yet proven"],
                  tag="Expansion plan", accent="grey", style="dashed"),
         ],
         "footer": "Next targets, not commitments: usability checks + device bench tests in 90 days; reviewed pilot by 6 months.",
         "footer_cue": "Our plan"},
    ]},
    {"start": "2:36", "end": "2:57", "chip": "RESPONSIBLE TECHNOLOGY", "graphics": [
        # assets/trust_icmr.png = make_trust_icmr.py: live Trust page excerpts (ICMR 2017 Privacy + Ethics
        # committee review rows, the ICMR AI 2023 table, "Not reviewed or approved by ICMR ..."). On screen 11.5 s.
        {"type": "image", "cue": N, "img": "trust_icmr", "tag": "Live site: Trust page, excerpts", "zoom": N},
        # 9.5 s on screen, 184 characters (about 19 a second); each card appears when it is spoken.
        {"type": "cards", "cue": "Before real use", "head": "Before real use",
         "sub": N,
         "cards": [
             card(N, "Ethics committee review", ["Full ICMR assessment pending"],
                  tag="Planned", accent="violet", style="dashed", cue="ethics committee review"),
             card(N, "Database transactions", ["Plus real SMS (Planned)"],
                  tag="Not done yet", accent="amber", style="dashed", cue="database transactions"),
             card(N, "Ask CDSCO for a ruling", ["No approval claimed"],
                  tag="No ruling yet", accent="grey", style="dashed", cue="a ruling from"),
         ], "footer": N, "footer_cue": N},
    ]},
]


def staff(key, tracker, caption, tag=N):
    return {"key": key, "tracker": tracker, "caption": caption, "tag": tag}


def phone(key, title, desc, tag=N):
    return {"key": key, "tracker": "Patient", "phone_title": title, "phone_desc": desc, "tag": tag}


scenes = [
    {"start": "2:57", "end": "3:08", "sub": "Doctor registers Kamala Devi", "journey_step": 0, "shots": [
        staff("s1_register", "Doctor", "Our site runs under the module name SpiroBuddy · age 68, Hindi",
              "FICTIONAL SAMPLE PATIENT")]},
    {"start": "3:08", "end": "3:17", "sub": "Admin admits her to a bed", "journey_step": 0, "shots": [
        staff("s2a_admit", "Admin", "Chest Ward bed: 'Admit / transfer here'; the bed shows occupied"),
        staff("s2b_overview", "Admin", "Overview (prototype): counts come from recorded bed operations")]},
    {"start": "3:17", "end": "3:36", "sub": "Prescription: draft, review, send", "journey_step": 1, "shots": [
        staff("s3_prescribe", "Doctor", "Manual-format draft · no AI · 'Needs review' until the doctor chooses",
              "MANUAL DRAFT · NO AI")]},
    {"start": "3:36", "end": "3:42", "sub": "Doctor publishes care instructions", "journey_step": 1, "shots": [
        staff("s4_publish", "Doctor", "Instructions the doctor wrote herself, published as version 1")]},
    {"start": "3:42", "end": "4:11", "sub": "Kamala's phone: login, medicines, pharmacy", "journey_step": 2, "shots": [
        phone("s5a_login", "Hospital number + code",
              "Real code · simulated delivery (no SMS). Single use, expires in 10 minutes. Her medicines open with Hindi labels.",
              "SIMULATED DELIVERY"),
        phone("s5b_meds", "Her medicines",
              "One tap changes the screen labels to English. Medicine names stay as the doctor typed them."),
        phone("s5c_pharmacy", "Show at the pharmacy",
              "A chemist can scan the QR to check the hospital's copy. Not for dispensing. Doctor's registration no. is a sample.")]},
    {"start": "4:11", "end": "4:18", "sub": "Kamala reads the care instructions", "journey_step": 2, "shots": [
        phone("s6_ack", "Care instructions",
              "She taps 'I have read this version'. This records reading, not consent. This page is in English only.")]},
    {"start": "4:18", "end": "4:38", "sub": "Breathing coach · simulated breaths", "journey_step": 2, "shots": [
        phone("s7a_device", "Connect device (USB)",
              "Where the clip-on unit would connect. No unit exists yet, so a simulator stands in.",
              "DEVICE NOT BUILT YET"),
        phone("s7b_breathing", "Breathing coach",
              "Simulated breaths · saved as partial (complete = 10 valid breaths). It coaches practice; it is not a lung test.",
              "SIMULATED BREATHS")]},
    {"start": "4:38", "end": "4:55", "sub": "Follow-up visit: asked and confirmed", "journey_step": 3, "shots": [
        phone("s8a_request", "Ask for a visit",
              "Tomorrow, a time, 'Check-up', then Send request. In the app only: no SMS or WhatsApp is sent."),
        staff("s8b_confirm", "Doctor", "My day: the request waits under 'Needs your answer'; she confirms it"),
        phone("s8c_confirmed", "Visit confirmed", "Kamala's visits page now shows Confirmed.")]},
    {"start": "4:55", "end": "5:29", "sub": "Simulated check-in call · nurse alert", "journey_step": 4, "shots": [
        staff("s9a_call", "Doctor", "Call simulator · scripted Hindi lines · preset answers · no real call",
              "SIMULATED CALL"),
        staff("s9b_nurse", "Nurse", "Raised by fixed rules, not AI · she assigns it and acknowledges it")]},
    {"start": "5:29", "end": "5:38", "sub": "Each hospital's own name, logo, colour", "journey_step": 0, "shots": [
        staff("s10_branding", "Admin", "Preview only · not saved · safety text and status labels stay fixed",
              "PREVIEW ONLY")]},
]

A = "Automated assistant (simulator, scripted): "
K = "Kamala (sample answer): "
call_subs = [
    A + "SpiroBuddy's automated care\nassistant, from the hospital. You missed {missed} sessions. Are you okay? Why?",
    K + "I had mild pain near the stitches this morning.\n" + A + "I will tell your care team.",
    A + "If pain is severe, get urgent help.\nShall the nurse call you back?  " + K + "Yes, please call.",
]

outro = {"start": "5:38", "end": "5:54", "chip": "", "graphics": [
    {"type": "cards", "cue": N, "head": "Live · Simulated · In development · Planned",
     "sub": "Every feature on our status list carries one of these labels.",
     "cards": [
         card("Works today, sample data", "Live",
              ["Register, beds, overview (prototype)", "Prescription on the phone; pharmacy QR",
               "Visit requests, My day, nurse alerts", "Hospital branding; 4 screen languages"],
              accent="green"),
         card("Built-in simulator", "Simulated",
              ["Login-code delivery (no SMS sent)", "Breaths and breath labels",
               "Check-in call (scripted, no real call)", "All patients and hospitals: fictional"],
              accent="amber", cue="Simulated"),
         card("Partly built", "In development",
              ["Clip-on unit over USB: no unit built", "Prescription notepad draft; AI drafting",
               "A person confirms every line (review)"],
              accent="violet", cue="The device is not built"),
         card("Not built", "Planned",
              ["Login code by real SMS", "Bluetooth pairing", "Database-level rules per hospital",
               "Dedicated department login"],
              accent="grey", style="dashed", cue="Our ask"),
     ],
     "footer": "Fictional patients only · Device not built · Our ask: one surgical ward to test this before any patient pilot",
     "footer_cue": "one surgical ward"}],
    "link": "spirobuddy.onrender.com",
    "team": "Team GuGu GaGa · Sharon Shaju Augustine · Fathima Shifana"}

spec = {"version": 4, "part1": part1,
        "demo": {"chip": "MVP / PROTOTYPE",
                 "journey": ["In hospital", "Discharge", "At home", "Follow-up", "Concern"],
                 "scenes": scenes, "call_subs": call_subs,
                 "nurse_sub": "Raised by fixed rules, not AI. Reported: \"mild pain near the stitches\"."},
        "outro": outro}

with open(os.path.join(HERE, "spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote spec.json")
