# Submission video tools (version 4)

These scripts make the hackathon video from the live site. They are helpers for the team, not part of the app.

**What the video is:** a silent 1920 × 1080 film (cards for the explanation, then a recording of the live site), plus a teleprompter copy for reading the script. The team records its own voice over it.

## The steps, in order

| Step | Script | What it does |
|---|---|---|
| 1. Record | `live_run_v4.py <site address> <folder> "<fictional patient name>"` | Drives the site in a browser (Edge) and records the 17 demo shots in care order with one new fictional patient. Writes `run.json`: when each shot starts and ends, where every click landed, and where the "it worked" messages are. |
| 1b. Retake one shot | `rerecord_s8c.py <site address> <folder>` | Re-records only the patient's "visit confirmed" screen (read-only), if that page was still loading in the main run. |
| 2. Fit the script | `assemble.py <narration.md> <spec.json> <recording folder> <out folder>` | Puts the recorded patient's name into the script and the on-screen text, and sets the call subtitles to the app's own English wording of its scripted lines. |
| 3. Check the script | `check_narration.py <narration.md> <spec.json>` | Checks times, reading pace, and that every card's cue phrase really is in the script. |
| 4. Build | `build_v4.py <work folder> <recording folder> <narration.md> <spec.json> <assets folder> <out folder>` | Renders `Aarogya_Saathi_video_SILENT.mp4` and `Aarogya_Saathi_video_TELEPROMPTER.mp4`. |
| 5. Add the voice | `mux_voice.py <silent.mp4> <voice file> <out.mp4>` | Joins the team's voice recording to the silent video and checks the limits (under 6:00, under 100 MB). |

Small helpers: `runinfo.py` (lines the log's times up with each video), `gfx_v4.py` (draws the Part 1 cards), `sheet.py` (contact sheet of frames, for checking), `changes.py` (finds the moments a recording changes).

## Rules these scripts follow

- **Fictional patients only.** The recorder registers one new made-up patient and refuses a name that already exists on the site.
- **Nothing is faked.** Every product shot is a real recording of the site. The edit only adds rings on clicks, boxes, zooms, captions and subtitles.
- **Local first.** Run the recorder on a local copy (`.claude/launch.json`, "recording-8021") before the live site.
- **The log is saved after every shot**, so a failed run still leaves usable marks.

## Where things are

- Script and on-screen text: `docs/VIDEO_NARRATION_FINAL.md` and `docs/video/spec_v4.json`.
- Wording rules (what may and may not be said, with evidence): `docs/video/claims_v4.md`.
- Recordings and work files are large and are **not** in git: `.build/video_v4/`.
- Finished videos: `output/video/` (also not in git). Version 3 is kept in `output/video/v3/`.

Needs: the project's Python environment (`.venv`, with Playwright and Pillow), Microsoft Edge, and `ffmpeg` on the PATH.
