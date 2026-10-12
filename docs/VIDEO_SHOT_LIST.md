# Video shot list — exact screens, clicks and success states

Goes with [VIDEO_NARRATION_FINAL.md](VIDEO_NARRATION_FINAL.md) and [VIDEO_RECORDING_CHECKLIST.md](VIDEO_RECORDING_CHECKLIST.md).

**How this was checked:** every click below was done on 12 Oct 2026, first on an isolated local copy (08:31–08:40 IST), then by an automated browser on the **live site** (09:20–09:25 IST, fictional patient `REC-2026-12`). Both passed. The words in **bold** are copied from the screen. That live run is already recorded as `output/video/Aarogya_Saathi_video_SILENT.mp4`; see the checklist's "Fastest path". Use this shot list only if you want to record the screen yourself, and then use a new number (`REC-2026-13` or higher).

`<site>` below means `https://spirobuddy.onrender.com` (or `http://127.0.0.1:8021` if you fall back to the local copy).

---

## 0. Set up three browser windows (off camera)

Each window must be a separate browser or profile, because each one keeps its own login. A new private window shares a login with other private windows, so use three truly separate ones:

| Window | Suggested browser | Who | Size |
|---|---|---|---|
| **A · Doctor** | Edge, normal window | Dr. Meera Nair | Full screen. Zoom 125% (press Ctrl and +) if text looks small. |
| **B · Patient phone** | Edge InPrivate window (Ctrl+Shift+N) | the sample patient | Drag the window narrow, about phone width (about 400 px wide). |
| **C · Admin, then Nurse** | Chrome (or a second Edge profile) | admin desk, later Sister Anjali | Full screen, zoom 125%. |

Log in **before** recording. The login page prints the sample passwords, so it must never be on camera.

1. Window A: open `<site>/login.html` → click **Try as Doctor**. You land on **My day** with "Dr. Meera Nair".
2. Window C: open `<site>/login.html` → click **Try as Admin**.
3. Window B: open `<site>/patient-login.html` and leave it there.

### Values for the take

| Field | Value |
|---|---|
| Hospital registration number | `REC-2026-11` (if the site says it already exists, use `REC-2026-12`, and so on) |
| Full name | `Sample Recording Patient` |
| Age | `45` |
| Registered phone number | `+910000000321` (fictional) |
| Notepad line (copy it to the clipboard) | `Sample medicine \| sample strength \| tablet \| 1 \| tablet \| BD \| 3 \| Sample instruction only` |
| Bed labels | `REC-11A` and `REC-11B` |

The notepad line is made-up demonstration text, not a medical instruction.

---

## 1. Recording plan: six clips, joined in order

Recording in clips lets you do set-up steps between them, off camera. Join the clips in the editor with plain cuts. Never cut in a way that suggests something happened that did not.

| Clip | Narration time | Contents | Off-camera prep **before** this clip |
|---|---|---|---|
| 1 | 0:00–2:30 | Slides + architecture page | Open the readable deck in slideshow mode, and `<site>/architecture.html` in a tab |
| 2 | 2:30–3:20 | Scenes 2–3 (register, prescribe) | Section 0 above |
| 3 | 3:20–4:03 | Scenes 4–5 (patient login, visit) | **Prep P1** below |
| 4 | 4:03–4:33 | Scenes 6–7 (bed, care document) | **Prep P2** below |
| 5 | 4:33–5:20 | Scenes 8–9 (breathing, Hindi call, nurse) | **Prep P3** below |
| 6 | 5:20–5:40 | Close on slide 17 | — |

**Prep P1 (after clip 2), in window A (doctor):**
1. Note the patient id from the address bar of the prescription page (`prescribe.html?id=` **number**).
2. Open `<site>/discharge-editor.html?id=<that number>` → click **Create replacement / new draft**.
3. Type in **Condition summary**: `Artificial follow-up condition`
4. Type in **Home-care instructions**: `Sample clinician-authored home-care text for this software demonstration only.`
5. Type in **Follow-up instructions**: `Sample follow-up instruction recorded by the doctor.`
6. Click **Save draft**. Wait for **"Draft saved. The patient cannot see this draft."** Do not publish yet.
7. Go back to `<site>/doctor-day.html` (My day).

**Prep P2 (after clip 3), in window C (admin):**
1. Open `<site>/department.html`.
2. Under **Configure a bed**: Department **General Surgery**, Ward **Surgical Ward A**, Bed label `REC-11A` → **Add bed**. Wait for **"Operation recorded."**
3. Bed label `REC-11B` → **Add bed**.
4. Open `<site>/hospital-overview.html` in a second tab and note the **Occupied beds** number.
5. Go back to the `department.html` tab and scroll so bed **REC-11A** is visible.
6. In window A, open `<site>/discharge-editor.html?id=<number>` (the saved draft shows in the form).

**Prep P3 (after clip 4):**
1. Window C: log out (top right) → `<site>/login.html` → **Try as Nurse**. You land on the dashboard as **Sister Anjali · Nurse**. Keep this window ready for the end of clip 5.
2. Window A (still the doctor): open `<site>/demo.html` (the Demo panel; also in the left menu as **Demo panel**). Scroll to **Calls & WhatsApp – live simulators**. Do not touch **Reset demo data**.
3. Window B: go back to **My medicines**, so the link **My breathing exercise (Simulated)** is visible.

---

## 2. Scenes

Hold every success state on screen for about 2 seconds before moving on.

### Scene 1 · Explain (0:00–2:30) · clip 1
Slides from `output/Aarogya_Saathi_DTI_With_SpiroBuddy.pptx`, as in the narration file: 1 → 2 → 5 → 4 → 7 → 8 → 13 → 14 → 12 → 16 → 9, then `<site>/architecture.html`, section **1. The system** (the diagram with Live / Simulated / In development / Planned badges). Do not scroll into the long text sections.

### Scene 2 · Doctor registers a patient (2:30–2:47) · window A
1. In the left menu, click **Register patient**. Page title: **Register a patient**.
2. Type **Hospital registration number**, **Full name**, **Age**, **Registered phone number** from the values table.
3. Leave **Responsible doctor** as **Dr. Meera Nair**. Skip Ward and Bed.
4. Tick **Assign the breathing exercise module (simulated input)**.
5. Click **Register patient**.

**Success state:** a card **"Sample Recording Patient registered"**, **Hospital number: REC-2026-11**, **Registered phone saved.**, buttons **Open patient record** and **Write prescription**.

Do not hover over the **Open patient app** link (its address contains a personal login token). Do not read out the hint "Bed occupancy management is planned" on this form; the bed module is shown later.

### Scene 3 · Reviewed prescription (2:47–3:13) · window A
1. Click **Write prescription**. Page: **Medicines for Sample Recording Patient**, with **No current prescription**.
2. Click inside the **Prescription notepad** box and paste the notepad line (Ctrl+V).
3. Click **Prepare draft for review**.
   **Success state:** a line starting **"Manual-format draft."** appears, and the **Write a prescription** form below fills in: Medicine name, Strength, Form **Tablet**, Dose **1 tablet**, code **BD**, **Reminder: morning and night.**, **3** days, the note.
4. The food box shows **Needs review**. Open it and choose **After food**. (This is the "doctor decides" moment.)
5. Scroll down and click **Send to the patient's phone**.
6. A box asks **"Send to the patient's phone?"** with **"1 medicine will appear on Sample Recording Patient's phone at once."** Click **Send now**.

**Success state:** a green message **"Sent to Sample Recording Patient's phone"**; **Current medicines** shows **Prescription of 12 October 2026 · Issued · Dr. Meera Nair**; a **What the patient sees** panel shows the medicine card.

On the live site the "Manual-format draft." line may give a different reason (for example, no AI consent recorded for this patient). Either way, call it a draft and do not say AI wrote it.

### Scene 4 · Patient login and medicines (3:13–3:36) · window B
1. **Hospital**: leave **Dawnlight General Hospital**. **Hospital registration number**: type `REC-2026-11`. Click **Send my code**.
2. **Success state:** a dashed box **"Sample phone Simulated"** with a 6-digit code and **"This code appears here instead of an SMS."**
3. Type that code into **6-digit code** → click **Open my medicines**.
4. **Success state:** page **My medicines** with the hospital banner **"Dawnlight Care with SpiroBuddy"**, the **Sample patient** strip, **"Hello, Sample"**, **"Prescribed by Dr. Meera Nair on 12 October 2026"**, and the dose card **9:00 PM · Night · Sample medicine · 1 tablet · after food** with **I took it**.
5. Tap the **English** language button once (see "Screen quirks", item 1).
6. Tap **I took it**.

**Success state:** the card turns green, **"Reported at <time>"** and **"Everything for today is reported."**

Do not resend the code: a second code is blocked for about a minute (**"Another code available in 59s"**).

### Scene 5 · Visit request and confirmation (3:36–3:58) · windows B and A
1. Window B: scroll to **My visits** and tap it. Tap **Ask for a visit**.
2. Under **Choose a day**, tap **Tue 13 · Tomorrow**. Under **Choose a time**, tap **10:00 AM**. Under **What is it about?**, tap **Check-up**. Tap **Send request**.
   **Success state:** **"Your request was sent. The hospital will answer here."** and a card **Requested · Tuesday, 13 October 2026, 10:00 AM · Dr. Meera Nair · OPD**.
3. Window A: open **My day** (left menu). Under **Needs your answer** the request shows **10:00 AM · Tue 13 Oct · Sample Recording Patient · Requested · Reason: Check-up**. Click **Confirm**.
   **Success state:** message **"Visit confirmed."** Click **Tomorrow** to show it listed as **Confirmed**.
4. Window B: refresh (F5). **Success state:** the card now says **Confirmed**.

If you record on a later day, pick any day that is not marked **No times** (Sundays show **No times**).

### Scene 6 · Bed management (3:58–4:11) · window C (admin)
1. On **Department operations**, find the bed card **Surgical Ward A · REC-11A** (**General Surgery · available**).
2. In its **Patient** box choose **Sample Recording Patient · REC-2026-11** → click **Admit / transfer here**.
   **Success state:** **"Operation recorded."**; the card now reads **General Surgery · occupied** and **Sample Recording Patient · Dr. Meera Nair**, with a **Discharge from bed** button.
3. Switch to the **Hospital overview** tab → click **Refresh overview**.
   **Success state:** **Occupied beds** is one higher than you noted; **Current admissions** and **Admissions today** are also one higher.

Keep the yellow line **"Admin-operated department prototype. Dedicated department login is Planned."** visible; it is the honest label.

### Scene 7 · Care document (4:11–4:25) · windows A and B
1. Window A, discharge editor (draft already in the form): click **Publish saved draft to patient**.
2. A browser pop-up asks **"Publish the SAVED draft? The patient will be able to view this version…"** Click **OK**.
   **Success state:** **"Published version 1 · Dr. Meera Nair · <time>"** and **"Patient has not acknowledged this version."**
3. Window B: go back to **My medicines** and tap **My care instructions**.
   **Success state:** **"Version 1 · Dr. Meera Nair · Published …"** with the condition, home care and follow-up text.
4. Tap **I have read this version**.
   **Success state:** **"Read acknowledgement saved: <time>"**, plus the line **"Acknowledgement records reading this version. It does not confirm consent, treatment adherence or recovery."**

If you want to show the preview: **Preview saved draft** opens a page marked **"DRAFT — staff preview only"**. Come back with the browser's **Back** button, because its only link goes to the patient page.

### Scene 8 · Breathing session (4:25–4:45) · window B
1. On **My medicines**, tap **My breathing exercise (Simulated)**. Do not use the link on the care page (see Screen quirks, item 5).
2. Tap **Start my exercise**. The card shows **Breath 1 of 10**, **Finish now**, and buttons under **"No device connected: tap to make a simulated breath"**.
3. Tap **Good breath**. Wait about 4 seconds.
   **Success state:** **"Great breath!"**, **Breath 2 of 10**, and a line like **"1,860 mL · Score 7.7 out of 10"**.
4. Tap **Too fast**. **Success state:** **"That was too fast. Try slower."**
5. Tap **Finish now**.
   **Success state:** **"Session saved · 1 of 2 good breaths"** and **"Partial exercise saved. Complete 10 breaths to finish the hourly task."**

The bottom of the page says **"Simulator (no device connected)"**. Let it show for a moment. Numbers (mL and score) are simulated and change each time; do not read them as real measurements.

### Scene 9 · Simulated call in Hindi, then nurse alert (4:45–5:20) · windows A and C
1. Window A, **Demo panel**, section **Calls & WhatsApp – live simulators**. Show the status line **"AI check-in calls: simulated here · WhatsApp: dry run"**.
2. **Patient**: choose **Ravi Kumar ★**. Click **AI check-in call – optional, where consent allows**.
   **Success state:** message **"AI check-in call ringing on the patient phone"**; the phone simulator shows an incoming call.
3. On the phone simulator, press the green answer button **✆**.
4. The assistant's first Hindi line appears. Tap the answer **"आज सुबह टांकों के पास हल्का दर्द था।"**
5. The assistant asks about a callback. Tap **"हाँ, कॉल कीजिए।"**
   **Success state:** **"⚠ Nurse review requested"**, **"Sent to the nurse dashboard · decided by fixed rules, not the AI"**, and the message **"Check-in call note for Ravi sent to the nurse"**.
6. Window C (Sister Anjali): scroll to the **Alerts inbox**. A new item **CHECK-IN CALL NOTE · just now · Ravi Kumar: check-in call – nurse review requested** is at the top, and **Open alerts** has gone up by one. (On the local copy it was exactly **1 amber**; the live site may already hold other sample alerts.) If it is not there, press F5 once.
7. Click **Details**. **Success state:** **"Patient's own words: "आज सुबह टांकों के पास हल्का दर्द था।""**
8. Click **Acknowledge**. **Success state:** message **"Acknowledged"**; one amber alert moves to **mine** (locally: from **1 amber** to **1 mine**), under the signed-in name **Sister Anjali**.

**Why Ravi and not the new patient:** the new patient has no recorded consent for automated calls, so the button refuses with **"No recorded consent (yes + date) for automated calls to this patient"**. That refusal is a safety feature. Do not record consent for the new patient just to make the call work.

#### The Hindi call, line by line (for your narration or an optional caption)

| Who | Hindi on screen | Meaning in English |
|---|---|---|
| Assistant | नमस्ते, यह SpiroBuddy की स्वचालित देखभाल सहायक है। अस्पताल की ओर से। Ravi जी, हमने देखा कि आपका साँस का व्यायाम 2 बार छूट गया है। क्या आप ठीक हैं? क्या आप बताना चाहेंगे कि क्यों छूटा? | Hello, this is SpiroBuddy's automated care assistant, calling for the hospital. Ravi-ji, we noticed your breathing exercise was missed twice. Are you okay? Would you like to tell us why? |
| Ravi (tap) | आज सुबह टांकों के पास हल्का दर्द था। | I had mild pain near my stitches this morning. |
| Assistant | बताने के लिए धन्यवाद। मैं यह आपकी देखभाल टीम तक पहुँचा दूँगी। अगर दर्द तेज़ या नया हो, या साँस फूले, तो तुरंत मदद लें। क्या आप चाहेंगे कि नर्स आपको वापस कॉल करें? हाँ या ना कहिए। | Thank you for telling me. I will pass this to your care team. If the pain becomes strong or new, or you feel breathless, get help at once. Would you like a nurse to call you back? Please say yes or no. |
| Ravi (tap) | हाँ, कॉल कीजिए। | Yes, please call. |
| Assistant | आपकी वापस कॉल करने की विनती देखभाल टीम को समीक्षा के लिए भेज दी गई है। तुरंत मदद चाहिए तो अपनी देखभाल टीम से सीधे संपर्क करें, या आपातकाल में 112 पर कॉल करें। नमस्ते। | Your callback request has been sent to the care team for review. If you need help right away, contact your care team directly, or call 112 in an emergency. Namaste. |

The other two answer buttons are **"मैं भूल गया था, अभी करता हूँ।"** (I forgot, I'll do it now: no concern) and **"मुझे ठीक से साँस नहीं आ रही।"** (I can't breathe properly: the red-flag path). Use the mild-pain answer for the video; it is the path that was checked end to end.

**Speaking Hindi yourself (optional):** the phone simulator also has **🎤 दबाएँ और बोलें** (press and speak), which uses the browser's speech recognition. It may mishear. Tapping the answer buttons is the reliable path, and the on-screen log labels the answer as "tapped answer" either way. If the browser reads the assistant's lines aloud in Hindi, let the first line play, then talk over the rest quietly to stay on time.

### Scene 10 · Close (5:20–5:40) · clip 6
Deck slide 17 (**Team Structure**: Sharon Shaju Augustine, Fathima Shifana). Slide 19 shows `spirobuddy.onrender.com` if you prefer to end on the URL.

---

## 3. Screen quirks found during the run-through (work around them; no code was changed)

1. **AI choice box shows Hindi on an English page.** On first load of **My medicines**, the **Optional AI processing** box at the bottom appeared in Hindi even though English was selected. Tapping **English** once fixed it ("Optional AI processing … Save my choice"). Do this before scrolling down. This is for Codex to fix later.
2. **Login page shows sample passwords.** Log in before recording; never show `/login.html`.
3. **Reported at a morning time for the 9 PM dose.** The app lets the patient report the night dose early. Say "records the patient's own report"; do not say "on time".
4. **Draft preview page** links only to the patient's "My care" page. Use the browser's **Back** button.
5. **"My breathing exercise" on the care page** has no patient number. In a fresh browser it opened the default sample patient ("Hello, Ravi"). Always use the link on **My medicines**.
6. **Registration form hint** says bed occupancy is planned, but the separate admin bed board works. Don't read the hint out.
7. **Red "Reset demo data" button** at the top of the Demo panel. Never press it: it wipes the sample patients, bed operations and care documents (on the live site too).

## 4. If something goes wrong while recording

| Problem | What to do |
|---|---|
| "Already exists" on registration | Use the next number (`REC-2026-12`). |
| Code box says to wait | Wait for the countdown, press **Send my code** once. Or use **I have a hospital PIN**, and say "PIN" on camera. |
| No free visit times | Pick another day that is not **No times**. Never claim a visit you did not see confirmed. |
| Bed board empty | You skipped Prep P2. Add the beds off camera, then re-record clip 4. |
| Publish says conflict | Reload the editor, check the saved draft, publish again. |
| No nurse alert after the call | Press F5 in window C. If it is still missing, say "the alert did not arrive in this take" and re-record clip 5. Never fake it. |
| Live site slow or a page missing | Switch the whole recording to the local copy (see checklist) and say so in the close. Do not mix live and local clips. |
