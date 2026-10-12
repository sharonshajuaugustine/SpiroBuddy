# Recording and export checklist

Goes with [VIDEO_NARRATION_FINAL.md](VIDEO_NARRATION_FINAL.md) (what to say) and [VIDEO_SHOT_LIST.md](VIDEO_SHOT_LIST.md) (what to click).

Rules: under 6:00 (aim for 5:40), under 100 MB, your own voice, sample data only, no passwords or keys on screen.

---

## A. Which site to record (checked 12 Oct 2026, 08:22–08:25 IST)

| Check | Result |
|---|---|
| GitHub `main` has the latest commit (`6755f77`) | Yes |
| Live pages (`register`, `prescribe`, `patient-login`, `meds`, `patient-visits`, `doctor-day`, `department`, `hospital-overview`, `discharge-editor`, `my-care`, `demo`, `dashboard`, `login`) and their scripts | **Byte-for-byte the same** as the local files |
| Live `/api/health` | OK; sample-data mode; Supabase database |
| Live public login API (`/api/me/otp/hospitals`) | Returns the two Dawnlight sample hospitals |
| Full click-through (register → prescribe → OTP → visit → bed → care document → breathing → call → nurse) | **Done on the isolated local copy only.** Not yet done on the live site. |

**Recommendation:** record on the live site (`https://spirobuddy.onrender.com`), because that is the URL the judges will open. First do the 5-minute live check below. If any step fails, record everything on the local copy instead (section F) and say so in the close.

### 5-minute live check (do this silently; it does not need to be recorded)
1. Open `https://spirobuddy.onrender.com/api/health`. Wait until it shows `"ok":true`. The first load after a quiet period can take a minute.
2. Run scenes 2, 3 and 4 of the shot list quickly, using the number `REC-2026-10` (not your take number).
3. As admin, open `/department.html` and `/hospital-overview.html`: both should load and show **Configure a bed** and **Refresh overview**.
4. As doctor, open `/demo.html` → Ravi → **AI check-in call – optional, where consent allows**: the phone should ring. Answer and finish the call, or end it.
5. If all four work, record on the live site with `REC-2026-11`. If any fails, use section F.

Everything you create on the live site is fictional sample data. Never press **Reset demo data** on the live site.

---

## B. Before you press record

- [ ] Quiet room. Phone on silent. Do a 10-second microphone test and listen back.
- [ ] Windows notifications off: **Settings → System → Notifications → Do not disturb: On**.
- [ ] Close email, chat and any tab with personal or account information.
- [ ] Hide the browser's bookmarks bar (Ctrl+Shift+B) if it shows personal sites.
- [ ] Screen resolution 1920 × 1080 if possible; browser zoom 125% on staff pages.
- [ ] Three windows set up and logged in as in shot list section 0. The login page is **never** on camera.
- [ ] Notepad line copied to the clipboard.
- [ ] Deck open in slideshow mode: `output/Aarogya_Saathi_DTI_GuGu_GaGa_Readable.pptx`.
- [ ] No terminal, `.env` file, Render dashboard, Sarvam/Google consoles or API keys anywhere on screen.

## C. Rehearse once with a stopwatch

- [ ] Read Part 1 aloud against a phone stopwatch. It should end between 2:25 and 2:35.
- [ ] Do one full silent click-through of clips 2–5 with the stopwatch. Each clip should fit its time in the shot list (section 1).
- [ ] Write the real times in the table at the end of the narration file. Cut as that file says if you are over.

## D. Record

- [ ] Record the six clips in order (shot list section 1), doing the off-camera prep between them.
- [ ] Pause 2 seconds on every success message before moving on.
- [ ] Check every clip straight after recording: is the success message visible and is your voice clear? Re-record a clip if not. Never edit a clip to suggest a step worked when it did not.

Recording tools already in Windows 11:
- **Snipping Tool:** press Windows + Shift + R, drag over the screen area, turn the microphone on, press **Start**. Clips save as MP4 in your Videos folder (Screen Recordings).
- **Clipchamp** (the built-in video editor) can join the clips and export. If your version also offers screen recording, you can record there instead.

## E. Join, export and check the file

1. Open **Clipchamp** → create a new video → drag the six clips onto the timeline in order.
2. Trim the dead time at the start and end of each clip. Keep the success messages.
3. Check the total length on the timeline: **under 6:00, ideally about 5:40.**
4. **Export** → choose **1080p**.
5. In File Explorer, right-click the exported file → **Properties** → check **Size**. It must be **under 100 MB**. If it is not, export again at **720p**.
6. Play the exported file from start to end once. Check sound, length and that no password or key appears.

## F. Fallback: record on the local copy

Use this only if the live check fails. It runs a separate copy on your laptop with its own sample database; it never touches the live database.

1. Open PowerShell in the project folder (`C:\Users\USER\Desktop\SpiroBuddy`).
2. Paste and run:

```powershell
.\.venv\Scripts\python.exe .build\start_recording.py
```

3. Open `http://127.0.0.1:8021/api/health` in the browser. It must say `"data_backend":"demo"`. If it says `supabase`, stop (press Ctrl+C) and do not record.
4. Use `http://127.0.0.1:8021` wherever the shot list says `<site>`. Keep the PowerShell window open but off camera.
5. In the close, say "This is our local working prototype, with sample data." Do not say it is live. Do not mix local and live clips.
6. The local copy already holds the run-through records (`REC-2026-01`, beds `REC-A` and `REC-B`). The take values (`REC-2026-11`, `REC-11A`, `REC-11B`) are still free.
7. After recording, press Ctrl+C in PowerShell to stop it.

## G. Upload and make the link work for anyone

Pick one:
- **YouTube:** upload → Visibility **Unlisted** (not Private).
- **Google Drive:** upload → **Share** → General access **Anyone with the link** → **Viewer**.

Then:
- [ ] Copy the link and open it in an InPrivate window **while signed out**. It must play.
- [ ] Wait until the video has finished processing (YouTube shows HD only after processing).

## H. Submission form

| Field | What to enter |
|---|---|
| Working URL | `https://spirobuddy.onrender.com` |
| Staff sample logins | `https://spirobuddy.onrender.com/login.html` → the **Sample logins** box: **Try as Admin**, **Try as Doctor** (Dr. Meera Nair), **Try as Nurse** (Sister Anjali). One click each. The fictional email and password for each person are printed in that box; copy them from there if the form asks for them. |
| Patient sample login | `https://spirobuddy.onrender.com/patient-login.html` → **Use Ravi's hospital number** → **Send my code** → type the code shown in the **Sample phone · Simulated** box → **Open my medicines**. |
| Demo video | The link from section G |
| Note for judges (optional) | "All people and records are fictional. The SMS code, breathing input and calls are simulated. If the site is slow to open, wait a minute and refresh." |

## I. Final check before you submit

- [ ] Video length is **under 6:00** (aim 5:40).
- [ ] File is **under 100 MB**.
- [ ] Narration is in your own words and your own voice; team **GuGu GaGa**, **Sharon Shaju Augustine** and **Fathima Shifana** are named.
- [ ] Part 1 covers theme, problem, scope, personas, market fit, the two metrics with **illustrative** targets, scalability, roadmap and architecture.
- [ ] The demo shows a success message after each click.
- [ ] "Simulated" is said for the code, the breathing input and the call; the device is "in development".
- [ ] Gemini and Sarvam are described only as **separate tests**, not as working phone calls or AI-written prescriptions.
- [ ] No real patient data, phone numbers, passwords, keys or personal tabs appear.
- [ ] The video link opens signed out.
- [ ] The working URL opens and the sample logins work.

## Issues to pass to Codex later (not changed now; you asked for no code changes)

1. On **My medicines**, the **Optional AI processing** box loads in Hindi when the page is in English, until the **English** button is pressed.
2. The draft preview page (`discharge-print.html`) offers only a patient "My care" link to staff.
3. The registration form's bed hint ("Bed occupancy management is planned") contradicts the working admin bed board.
4. The night dose can be reported in the morning ("Reported at 8:34 AM" for a 9:00 PM dose).
