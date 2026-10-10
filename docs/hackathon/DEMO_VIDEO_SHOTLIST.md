# Demo video – shot list (you record the screen, you add the voice-over)

**Deadline:** upload with the submission by **Mon 12 Oct 2026, 11:00 AM IST** (organisers' email; replaces Sun 11 Oct, 3 pm). **Format:** one MP4 file, under 100 MB, English or Hindi.
**Target length:** 2 minutes 30 seconds to 3 minutes. The form says the video must "show the Prototype/MVP in action", so most of it should be the live app, not the 3D animation.

## Before you record
1. Open **https://spirobuddy.onrender.com/demo.html** and click **Reset demo data**. Wait for the page to refresh.
2. Use Chrome. Press **F11** for full screen. Close other tabs and turn off notifications.
3. Record with **Win + Alt + R** (Xbox Game Bar) or OBS. Record the tab's sound too, so the Hindi voice coach is heard.
4. Open these tabs in this order, so you only press **Ctrl + Tab** while recording:
   1. `https://spirobuddy.onrender.com/showcase/videos.html`
   2. `https://spirobuddy.onrender.com/app.html?id=1` (press **F12**, then the phone icon, pick a phone size; or just make the window narrow)
   3. `https://spirobuddy.onrender.com/` (nurse dashboard)
   4. `https://spirobuddy.onrender.com/demo.html`
5. The site should already be awake (it is kept awake automatically). Open it once a minute before, to be sure.

**Honesty rule for the voice-over:** say "simulated" for the device, the WhatsApp messages and the phone calls. Say "mobile web app", not "Android app". Never say "prevents pneumonia", "first", "clinically proven" or "diagnoses".

## The shots

| # | Time | What is on screen | What to click | What to say (short) |
|---|---|---|---|---|
| 1 | 0:00–0:20 | **Tour video**, opening (patient outline with the spirometer) | Play `tour.mp4` from the start, let it run 20 s | The problem: after surgery patients go home with this breathing exerciser. About 1 in 10 surgical patients gets a lung complication. Most forget the exercise or do it wrong, and nobody can see that. |
| 2 | 0:20–0:40 | **Tour video**, "Meet SpiroBuddy" and "How it measures" (skip to 0:10 and 0:34) | Drag the video bar | Our idea: a base the ordinary exerciser stands on. A laser sensor reads how high the disc rises. This is a 3D concept model with sourced dimensions. We have not built the hardware yet. |
| 3 | 0:40–1:25 | **Patient phone app** | Click **व्यायाम शुरू करें** (Start). Open **Demo controls** at the bottom and click **Good breath**, wait for it to finish, then **Too fast**, then **Good breath** | This is the patient's phone. It coaches by voice in Hindi: breathe in slowly, hold, well done. When the breath is too fast it says "slower" at once and the frame turns amber. The breath comes from a simulator today. Each breath is scored by our model. |
| 4 | 1:25–1:40 | Same app | Click **Play a full demo session** earlier in a second take and cut to its end, or click **अभी समाप्त करें** (Finish now). Scroll to **Today** | The session saves itself. Today's hourly ticks update. Nothing to type. Tap English, Tamil or Malayalam to show the languages. |
| 5 | 1:40–1:50 | Same app | Click **I do not feel well** | One safety button. It always shows the same fixed message, contact your nurse or call 112, and alerts the nurse. This part does not use AI. |
| 6 | 1:50–2:20 | **Nurse dashboard** | Show the list, then click **Ravi Kumar** | The nurse sees every patient, most urgent first. Ravi's new session and his red flag are already here. Status is always an icon and a word, never colour alone. |
| 7 | 2:20–2:40 | **Demo panel** | On Ravi's card click **Simulate 2 missed slots**, then **Send summary to family (WhatsApp)** | If sessions are missed, a ladder starts: reminder, family message, nurse alert, nurse calls. The family gets one short update a day, with consent and a one-word STOP. These sends are previews, not real messages yet. |
| 8 | 2:40–2:55 | **Family page** (open from the patient page, "Care circle" link) or the dashboard again | – | Impact: we measure the share of hourly sessions completed, automatically. A US trial showed reminders alone doubled use. We will not claim medical outcomes until a proper study. |
| 9 | 2:55–3:00 | Tour video's last frame (logo) | – | SpiroBuddy. Coaching every breath at home. Team, track: Healthcare and Wellbeing. |

## Extra shot: one unit, many patients (about 25 seconds, between shots 6 and 7)
Open **Units** in the left menu of the nurse site (`/units.html`). First click **Reset mock units**.
1. Point at the list: every unit, who has it, battery, and where it is in its cycle.
2. On **SB-0011** (with Ravi) click **Take back**, then **Clean and check** (tick the three boxes, **Sign as cleaned**), then **Wipe unit**. It returns to "In stock".
3. On the same unit click **Hand over**: **Simulate scan**, pick **Priya Sharma**, **Run test breath**, **Hand over**.
4. Click **Patient app** on that row. The app opens greeting Priya, with her goal, and shows "Unit SB-0011".

**What to say:** "Units are lent and reused. The unit stores nothing about a person. Language, goal and family contacts live on the patient's record, so moving a unit to the next patient is one scan. A unit that is not on loan records nothing." **Say plainly:** "This screen is a mock-up; no real units exist yet." The page also says so.

## Shortcuts that help while recording
- **Patient app keys:** `G` good breath · `F` too fast · `S` too shallow · `N` no hold · `A` full 10-breath session.
- **Demo panel keys (for Ravi):** `G` good session · `M` mixed · `P` poor · `X` 2 missed slots · `S` send summary · `L` play the reminder ladder.
- If something looks wrong, click **Reset demo data** and start that shot again. Record each shot separately and join them; it is easier than one perfect take.

## If the internet fails
Run it on the laptop instead: start the server (`scripts\run.ps1`) and use `http://localhost:8000` in place of `https://spirobuddy.onrender.com`. Everything in this list works the same.

## Getting under 100 MB
A 3-minute screen recording at 1080p is usually 30–80 MB. If yours is bigger, tell Claude the file name and it will shrink it.
