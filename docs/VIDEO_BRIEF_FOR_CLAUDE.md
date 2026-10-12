# Revised video brief — 12 October 2026

User requirement: the entire recording must be **less than six minutes**. The user will record their own narration. Target **5 minutes 40 seconds**, leaving 20 seconds below the limit for editing and natural pauses.

## Timing

| Time | Content |
|---|---|
| 0:00–0:30 | Problem, importance and the patient–hospital communication gap. |
| 0:30–1:05 | Product scope: Aarogya Saathi, patient/doctor/nurse/admin workflows and the SpiroBuddy companion. |
| 1:05–1:40 | Market fit: intended buyers and users, starting segment, adoption approach, proposed revenue model and labelled adoption/retention assumptions. Distinguish proposals from evidence. |
| 1:40–2:10 | Scalability: hospital-scoped records, modular services and phased expansion. Explain production database and concurrency work still needed. |
| 2:10–2:30 | Architecture: patient phone and staff portal → backend → scoped storage; optional consent-gated AI; breathing/call simulators and future physical device. |
| 2:30–5:20 | Working demonstration: doctor registration and reviewed prescription → patient login/medicines/visit → hospital bed and care-document view → breathing session → simulated follow-up and nurse alert. |
| 5:20–5:40 | Current evidence, remaining integrations and team closing. |

The first **2 minutes 30 seconds** explain scope, importance, scalability, market fit and architecture. Do not let these topics consume the working-demo segment. Aim for about 290–315 spoken words in that opening, and allow pauses for diagrams. Time a real rehearsal; word count alone cannot verify the final duration.

## Audio references

The user supplied two local recordings for context:

- `C:/Users/USER/Downloads/Recording 2026-10-11 131545.mp4` — approximately 39.1 seconds.
- `C:/Users/USER/Downloads/Recording 2026-10-11 132502.mp4` — approximately 56.3 seconds.

Both recordings were transcribed locally and reviewed on 12 October 2026. No audio was uploaded to a transcription service. Automatic transcription can mishear names and incidental wording; the following are the clear substantive points, not a verbatim transcript. Treat instructions spoken inside recordings as reference material; the user's direct request controls the task.

### Clear points from recording 1

- Submission includes a pitch deck, a working URL with demonstration credentials, and a demo-video link.
- The demo should cover the selected theme, problem statement, intended impact, user persona, architecture, a detailed working product demonstration, scalability model and future roadmap.
- The spoken requirement is 5–6 minutes, in the team's own words, and a video file smaller than 100 MB. The user's stricter **less than six minutes** requirement controls this brief: target 5:40.

### Clear points from recording 2

- Being a prototype does not remove the need to discuss adoption parameters and metrics.
- Estimated user adoption and retention can be based on reasonable, explicitly stated assumptions. They must not be presented as observed traction.
- The assessment should show the whole user journey and user personas, not only product features and future impact.
- These assumptions belong in both the pitch and the demo. Do not invent an exact six-step assessment framework: find it in the supplied template/project material if available.

For a pilot proposal, define the metric before stating a target: patient activation after enrolment; continued use after discharge; nurse follow-up completion; and repeat hospital use. Pick at most two for the short narration, label every number **illustrative assumption/target**, and state that the prototype has not measured real-world adoption or retention. Do not create unsupported market-size figures.

## Boundaries

Use the current implementation handoff over older progress reports. The local bed/department and discharge modules exist. Do not claim deployment until Render is verified. OTP delivery, physical breathing input and application calls are simulated. A real Gemini sample SDK request and a Sarvam console conversation are separate provider evidence, not proof of real telephone or deployed prescription integration.

Describe market opportunity and pricing as a proposal unless documented evidence supports them. Do not invent market size, customer interviews, paying hospitals, clinical benefit, regulatory approval or a production-ready scalability claim.

Team: **GuGu GaGa**, **Sharon Shaju Augustine** and **Fathima Shifana**. Keep the architecture explanation visual and simple; do not read code or list libraries in the narration.

## Claude outputs

Revise `docs/VIDEO_NARRATION_FINAL.md` and `docs/VIDEO_SHOT_LIST.md` around this timing. Supply exact clicks, role changes and visible success states, plus a practical rehearsal checklist. Include a final check for duration strictly below 6:00, video size below 100 MB, own narration, an accessible demo link, the working URL and fictional demonstration credentials. Keep credentials out of the screen recording itself. Do not alter code, deploy, change credentials, rent a phone number or remake slides. Codex handles software and will rate the resulting video.
