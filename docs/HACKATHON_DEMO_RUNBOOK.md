# Six-minute hackathon recording: Aarogya Saathi + SpiroBuddy

**Team GuGu GaGa:** Sharon Shaju Augustine and Fathima Shifana. Coworkers and former B.Sc. Computer Science classmates. This guide prepares a recording; it does not claim a video file has already been made.

Use fictional sample records only. Say: **“Aarogya Saathi connects the hospital care team to the patient's phone. SpiroBuddy is its breathing companion. This demonstration uses sample data.”**

## Choose the build before recording

**Updated local build:** use the coordinator's existing isolated local server if it is running. Open `/api/health`, then `/register.html`, `/patient-login.html`, `/department.html` and `/my-care.html`. A page existing does not establish authentication or workflow success: rehearse the sequence below once. The newest department and discharge modules have isolated tests; their full integrated browser check may still be pending.

**Deployed site:** open `https://spirobuddy.onrender.com/api/health` early to wake the service. Use the deployed site for the full sequence only after the tested build has been published and the same pages/workflows verified. If new pages return 404 or lack the new controls, use local for the complete demonstration. Label the recording **“Local working prototype — sample data.”** Do not switch silently between local screens and an older deployment, or claim local changes are deployed.

If no isolated local server is available, the following PowerShell starts a separate sample-data instance. Run from the project directory. It overrides providers before application import; it does not reset a shared/live database.

```powershell
New-Item -ItemType Directory -Path .build -Force | Out-Null
@'
import os, sys
sys.path.insert(0, os.getcwd())
for name in ('SUPABASE_URL','SUPABASE_SERVICE_ROLE_KEY','GEMINI_API_KEY',
             'ANTHROPIC_API_KEY','SARVAM_API_KEY','SARVAM_AGENT_API_KEY',
             'TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','EXOTEL_API_KEY',
             'EXOTEL_API_TOKEN','SARVAM_WEBHOOK_SECRET','PUBLIC_BASE_URL'):
    os.environ[name] = ''
os.environ.update(SPIROBUDDY_DATA_DIR=os.path.join(os.getcwd(),'.build','recording-data'),
                  DEMO_MODE='1', DATA_BACKEND='demo', DEMO_AUTOPILOT='0',
                  COMMS_AUTO_ESCALATE='0', CALL_PROVIDER='dry_run')
import uvicorn
uvicorn.run('backend.app.main:app', host='127.0.0.1', port=8021)
'@ | Set-Content -LiteralPath .build/start_recording.py -Encoding utf8
.\.venv\Scripts\python.exe .build/start_recording.py
```

Open `http://127.0.0.1:8021/api/health`; confirm demo SQLite rather than Supabase before entering data. If it is not isolated demo data, stop the rehearsal. Keep this terminal open. Stop with Ctrl+C after recording. Do not show terminals/environment panels in the video.

## Stage the recording in 10–15 minutes

1. Create **three browser profiles/private windows**: doctor, patient at about 375px width, and staff. Separate profiles prevent changing the other window's staff cookie. Use `/login.html` → **Try as Doctor**, **Try as Nurse**, or **Try as Admin** as needed. The actual signed-in identity should appear in staff headers.
2. Choose a fresh hospital number, for example `REC-2026-01`, with sample name `Sample Recording Patient`, age 45 and phone `+910000000321`. Tick the breathing module only for this fictional record. Note the resulting numeric patient ID for editor/chart URLs. Do not display a real phone number.
3. Prepare this manual notepad text in a clipboard. It is artificial demonstration data, not a recommendation or dispensing instruction:

   ```text
   Sample medicine | sample strength | tablet | 1 | tablet | BD | 3 | Sample instruction only
   ```

   In review, explicitly choose the food instruction and check every field. The manual fallback intentionally leaves uncertain fields for a clinician's decision.
4. Stage a **saved discharge draft** for the same sample patient using `/discharge-editor.html?id=<ID>`. Use condition `Artificial follow-up condition`, home care `Sample clinician-authored home-care text for this software demonstration only.` and follow-up `Sample follow-up instruction recorded by the doctor.` Leave unsupported clinical details blank. Save but do not publish until the recording.
5. As admin, open `/department.html`. Add two beds using departments/wards actually offered by the form, labels `REC-A` and `REC-B`. Inventory starts empty; old chart ward labels are not admissions. Leave the patient unallocated for the recorded admission.
6. As patient, inspect **My visits** and available slots; use an offered future slot. As doctor, keep `/doctor-day.html` ready. Do not type a guessed time or promise a reminder.
7. Rehearse the simulated call on `/demo.html` with a seeded fictional patient whose automation consent is valid. Confirm dry-run/simulator mode. Choose a reason plus **callback requested** so the workflow generates a nurse-review alert. Use the same patient throughout that call sequence. Do not change a real person's consent to prepare the demonstration.
8. Keep `/dashboard.html` open as the nurse. A medicine-missed alert takes the configured grace time after a due dose; it cannot be honestly created by immediately issuing a prescription. For the short recording, use the actual call-generated alert or a clearly identified seeded demonstration alert instead.
9. Do not press **Reset demo data** after staging: it clears patient records, bed operations and discharge documents. If an MRN exists, choose a new number; do not delete or reset shared data to bypass it. Never show keys, webhook URLs or environment settings.

## Main recording: 5 minutes 50 seconds

Use screen capture with microphone narration. Pause briefly after saves so the real result appears. These times are a target; if a provider or page stalls, use the fallback below rather than editing separate scenes to imply an unverified integration.

| Time | Exact action | Short narration |
|---|---|---|
| 0:00–0:20 | Show landing page or deck cover with team names. | “We are GuGu GaGa: Sharon Shaju Augustine and Fathima Shifana. Aarogya Saathi connects hospital care with the patient's phone. SpiroBuddy is its breathing companion. All records here are fictional.” |
| 0:20–0:55 | Doctor: `/register.html`. Register the fresh sample MRN/phone and breathing assignment. Show the resulting chart link and MRN. If you staged this patient already, show the existing chart and registration form instead of creating a duplicate. | “The hospital number connects the doctor's record, medicines and patient login. The hospital controls which patient has the breathing module.” |
| 0:55–1:40 | Doctor: `/prescribe.html?id=<ID>`. Paste sample notepad, **Prepare draft for review**, complete missing review choices, **Send to the patient's phone**, then explicit confirmation. Show issued prescription. | “Preparation creates a draft only. The doctor checks each field and confirms publication. This isolated recording uses the manual-format fallback. Gemini has separately passed a sample structured request, but is optional and consent-gated.” |
| 1:40–2:20 | Patient: `/patient-login.html`, hospital and same MRN, **Send my code**, use the displayed **Sample phone / Simulated** code, open medicines. Show medicine details; if a due report button exists, tap **I took it** and show **Reported**. Show the optional AI-processing choice without implying unrelated consent. | “OTP delivery is simulated here; no SMS is sent. The patient sees the approved prescription. A tap records a report, not proof that medicine was swallowed. AI processing is a separate optional choice.” |
| 2:20–2:55 | Patient: **My visits**, request an offered future slot. Doctor: **My day**, confirm that request. Patient: refresh and show **Confirmed**. | “Patients ask for a visit, the doctor responds, and the patient sees the decision in the app. Appointment reminders and teleconsultation remain future work.” |
| 2:55–3:30 | Admin: `/department.html`, choose the sample patient on `REC-A`, **Admit / transfer here**. Open `/hospital-overview.html` and show changed occupied/available counts. | “This admin-operated department prototype records bed allocation and derives hospital counts from actual operations. A separate department login is still planned.” |
| 3:30–4:10 | Doctor: saved draft at `/discharge-editor.html?id=<ID>`, show **Preview saved draft** labelled Draft, return and **Publish saved draft to patient**. Patient: **My care instructions**, acknowledge this version, open print page. | “Drafts remain hidden from patients. The doctor publishes the saved instructions; replacements retain history. This button acknowledges reading one version. The printable document stays separate from current medicines and bed discharge.” |
| 4:10–4:35 | Patient: **My breathing exercise**, show explicit simulation label and one simulated breath. If leaving early, show partial status rather than claiming ten breaths completed. | “The software guides the exercise. Today's input is simulated: the physical laser attachment is still in development. A partial session does not count as a completed ten-breath session.” |
| 4:35–5:25 | `/demo.html`, same staged sample patient, **AI check-in call – optional, where consent allows**. Answer the browser phone; choose “forgot” and callback requested. Show resulting neutral note. Nurse: `/dashboard.html`, open corresponding actual generated alert and acknowledge under the real signed-in nurse name. | “This is a simulated call. The assistant captures the stated reason and callback preference. The nurse reviews the resulting alert; the assistant does not diagnose or alter treatment.” |
| 5:25–5:50 | End on nurse inbox and final status slide. | “Built locally: registration, reviewed prescriptions, visits, beds and care documents. Simulated: OTP delivery, breathing input and this call. The next work is real hardware validation, SMS delivery and reminders when the app is closed.” |

If spoken medicine reminders are shown, say **“Only while this page is open and visible, after opt-in.”** Do not call it closed-app push. Patient care text is preserved in the clinician's document language; translated navigation does not establish clinically validated translation.

## Optional 40-second real Sarvam console chat clip

This is separate evidence of a provider conversation, **not a telephone call or application webhook demonstration**. Put a visible caption **“Real Sarvam console chat — fictional sample conversation”** on the clip. Do not show account/credential panels or secret callback URLs.

| Time | Action |
|---|---|
| 0–8s | Open the already configured **SpiroBuddy check-in** agent's Chat test. Say: “This separately tests the provider's conversation. Telephony is not connected.” |
| 8–25s | In the fictional chat, enter “I forgot the exercise this morning.” Then request “Yes, please ask the demo care team to call me back.” Show the assistant's actual response; do not fabricate a transcript. |
| 25–35s | Show the neutral ending and callback preference in the console. If output-variable extraction is not verified, say so rather than claiming it has reached the hospital record. |
| 35–40s | End on caption: “Console chat verified. Phone rental/KYC and application callback integration pending.” |

Keep this clip separate from a simulator/replayed inbox scene. Do not splice them into a claimed end-to-end live call. The real chat has been tested; the application telephony credential, phone connection, outbound call and matching callback have not been verified. Setup and outstanding acceptance checks: [SARVAM_CALL_DEMO_SETUP.md](SARVAM_CALL_DEMO_SETUP.md). Gemini/provider preparation: [HACKATHON_SETUP_CHECKLIST.md](HACKATHON_SETUP_CHECKLIST.md).

## Fast recovery

| Problem | Recovery |
|---|---|
| Render is old, asleep or missing a new page | Use the isolated local build and label it. Keep the public URL on the final slide, without claiming new features are deployed. |
| Registration number already exists | Open that sample chart or use a fresh MRN. |
| OTP resend is cooling down | Wait for the displayed cooldown and request once. Alternatively use the existing reusable PIN fallback at `/patient-pin.html`, clearly labelled as a PIN. |
| AI preparation is manual-format | Continue review/publication and name it correctly. Real Gemini request verification is separate evidence, not an automatic claim about this screen. |
| No suitable visit slot | Show the actual empty state or select another offered future day. Do not invent a confirmed visit. |
| Bed inventory is empty | Add beds from the configured selectors. Chart labels alone are not occupancy. |
| Discharge says conflict | Reload; another edit or acknowledgement changed the revision. Review the saved draft before publication. |
| No nurse alert appears | Request callback in the controlled simulator and refresh. If still absent, show the note and state that the alert step did not complete. Do not claim a screenshot proves the current call succeeded. |
| Speech/microphone unavailable | Tap the prepared simulator answers and label the interaction simulated. |
| Call provider not ready | Keep dry-run mode. KYC/rental pending is a valid stated limitation; do not attempt calls to fictional sample numbers. |

Record only the behavior actually shown. No real patient outcomes, calibrated sensor accuracy, partner hospitals, validated clinical translation, real OTP SMS, live phone call or closed-app push is established by this walkthrough.
