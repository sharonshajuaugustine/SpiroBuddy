# SpiroBuddy – Hackathon Plan (starts tomorrow morning)

*Written 9 October 2026. The full long-term plan stays in SpiroBuddy_Complete_Plan.md. This page is just for the hackathon.*

## The goal: ONE demo that works from start to finish

The judges should see these 6 steps:
1. A patient breathes into the spirometer, and a big gauge on screen rises in mL.
2. Too fast: the voice says "Slower…". Good breath: "Great breath!" plus a score out of 10.
3. The label (*good / too fast / too shallow / no hold*) comes from **our own AI model**, trained at the hackathon on our own breaths.
4. After 10 breaths, this hour's reminder ticks itself off ✅.
5. The nurse dashboard updates live, and a "red" patient stands out.
6. Press **Send**, and an AI-written WhatsApp summary arrives on a phone.

**Cut for now** (put these under "Next steps" in the pitch): Bluetooth, battery, AI model on the chip, 3D-printed case (unless you already have a printer), phone notifications, Q&A chat, more than 2–3 languages.

---

## Tonight, in this order

1. **Read the rules (10 minutes).** Check:
   - Is code written before the event allowed?
   - Are AI coding tools allowed?
   - Is it online or in person?
   - How long is the demo?
   - What do you submit (video, GitHub link, slides)?
   - How are teams judged?
2. **Buy a spirometer from a chemist tonight.** Get the volumetric (piston) type if they have it. If they only have the 3-ball type, buy it anyway.
3. **Find electronics tonight.** Online orders won't arrive in time.
   - Any **ESP32 or Arduino** (Uno or Nano is fine) + its USB cable
   - A **VL53L0X or VL53L1X** laser distance sensor + jumper wires
   - Ask teammates, friends, seniors or the college lab, or try a local electronics shop if one is still open.
   - **No sensor?** Use Plan B (camera version) below.
4. **Install software tonight**, because downloads can be slow:
   - Chrome, VS Code, Git
   - Arduino IDE 2 + your board package + the sensor library (Pololu VL53L0X, or SparkFun VL53L1X)
   - Python 3.12, then run: `pip install fastapi uvicorn scikit-learn pandas joblib anthropic twilio python-dotenv`
5. **Create accounts and test each one on its website:**
   - **Twilio** → WhatsApp Sandbox → from **every phone** you'll use in the demo, send the "join <code>" message
   - **Anthropic Console** → create an API key and add a small credit
   - *(Optional)* **Sarvam AI** → API key for Indian-language voices
6. **Draft the slides (8).** Take the content from SpiroBuddy_Complete_Plan.md, sections 1, 16 and 17. Use only the sourced numbers.
7. **Charge** laptops and phones. **Sleep at least 5–6 hours.**

---

## The simplest setup for tomorrow

```
Sensor -> Arduino/ESP32 -> USB cable -> laptop (Chrome)
   Web page: live gauge, breath detection, score, voice, checklist
   Python server on the SAME laptop: AI model, Claude summary, WhatsApp, saved data
   Nurse dashboard: a second page from the same server
```

Why this setup:
- Everything runs on one laptop: no hosting, no Bluetooth, no app store.
- Only WhatsApp and the Claude summary need internet, and both have backups.
- The board just prints distance numbers over USB, which takes about 30 lines of Arduino code.
- Chrome reads the USB cable directly using **Web Serial**.

---

## Who does what (3 people)

| A: Hardware | B: Server & AI | C: App & pitch |
|---|---|---|
| Sensor → board → numbers over USB. Mount it on the spirometer neatly (clip, cardboard, tape). Calibrate to mL using the printed marks. | Python server, fake patients, training the AI model, Claude summary with a template backup, WhatsApp sending. | Web page: connect, gauge, breath detection, score, voice, checklist, nurse dashboard. Slides and backup video. |

---

## Hour by hour (for a 24-hour event starting at 9 am; squeeze it if yours is shorter)

| Time | Person A | Person B | Person C |
|---|---|---|---|
| 9:00–9:30 | **Everyone:** set up, agree on the 6-step demo, test the Wi-Fi | | |
| 9:30–12:30 | Readings over USB about 30 times a second; mount it; calibration table | Server; fake patients; "Send summary" (template first, then Claude); WhatsApp test | Connect over USB; live gauge; breath detection; score; voice |
| 12:30–13:30 | **Everyone:** connect it all. A real breath shows on the gauge with a score. | | |
| 13:30–15:00 | **Everyone:** record and label 120–200 breaths (good / too fast / too shallow / no hold) | | |
| 15:00–17:00 | Make the mount tidier and the readings more accurate | Train the model; test it on a person it hasn't seen; plug it into the app | Checklist ticks after 10 breaths; nurse dashboard |
| 17:00–19:00 | Help connect things | Missed-session alert; summary in Hindi + English | Live dashboard updates; results screen |
| 19:00–20:00 | **Everyone:** run the full demo 3 times; write down every bug | | |
| 20:00–24:00 | Fix bugs | Fix bugs | Finish slides; **record the backup video as soon as the demo works** |
| Night | Sleep in shifts | | |
| Morning | **Stop adding features 3 hours before judging.** Only fix bugs. Rehearse 3 times with a timer. Test the judging setup. | | |

**For a shorter event (8–12 hours):**
- Record 80–100 breaths and use just two labels: *good* vs *needs work*.
- Use template text instead of Claude if time is tight.
- Keep the dashboard simple.

---

## Plan B

| Problem | Do this |
|---|---|
| **No laser sensor** | **Camera version:** point a phone or laptop camera at the spirometer, with white paper behind it and good light. The web page tracks how high the disc is, and you click the 0 and top marks once to calibrate. No electronics needed. |
| Readings jump around | Press the sensor flat on top, put black tape or foam around it, aim at the centre of the disc, and average 5 readings. |
| Web Serial won't connect | A small Python script reads the USB data and sends it to the server. |
| No internet at the venue | Pre-recorded voice clips; template summary; a screenshot of a WhatsApp message as backup. |
| AI model accuracy is low | Use two labels (*good* vs *needs work*) and show your honest number. |
| Demo crashes | Play the backup video. |

---

## If judging is on a video call

- Share the laptop screen to show the gauge and dashboard.
- Use a second camera (a phone as webcam) for a close-up of the spirometer.
- Keep the WhatsApp phone ready to hold up to the camera.
- Test all of this before your slot.

---

## Pitch changes for a 24-hour prototype

- Say "prototype built in 24 hours".
- Show the real numbers you measured: breaths collected, model accuracy, mL accuracy.
- Put Bluetooth, battery, on-chip AI and the 3D case under "Next steps".
- Use the InSee comparison: "The US proved this works. We built it for India."
