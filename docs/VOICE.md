# Voice & language (Sarvam AI) – SpiroBuddy

**In one line:** SpiroBuddy speaks and listens in 11 Indian languages using Sarvam AI (an Indian speech company). Without a Sarvam key it still talks, using pre-made clips or the browser's own voice.

Status: research verified 9 Oct 2026 from the official docs (URLs in §1). Built and tested without a key on 9 Oct 2026 (§7). **Waiting on the user: the Sarvam key (§6).**

## 0. For the user – get the Sarvam key (about 5 minutes, free to start)
1. Open https://dashboard.sarvam.ai and click **Sign up** (Google sign-in is fine). New accounts get **₹100 free credit** that never expires. That is enough for the whole demo.
2. In the dashboard, open **API Keys** and click **Create new key**. Give it a name like `spirobuddy`.
3. **Copy the key straight away.** Sarvam shows it only once.
4. Open the file `.env` in the SpiroBuddy folder (Notepad is fine). Find the line `SARVAM_API_KEY=` and paste the key right after the `=`, with no spaces. Save the file.
5. Restart the server (close the window running `scripts\run.ps1`, then run it again).
6. Optional, for the best demo: make the pre-recorded clips (about 12 minutes, about ₹45 of credit):
   `.venv\Scripts\python.exe tools\voice\make_clips.py`
7. Which plan: **Starter (pay as you go)**. There is no monthly fee; you only spend credits. If you want a safety margin, go to **Settings → Billing → Add Credits** and add ₹200–₹500. You don't need the Enterprise plan.

When the key is in, the demo panel's "Voice check" card shows **"Sarvam AI voice"** instead of "Browser voice".

---

## 1. Verified API facts (from docs.sarvam.ai, read 9 Oct 2026)

All APIs live on `https://api.sarvam.ai`. Auth header on every call: `api-subscription-key: <SARVAM_API_KEY>` (the docs say `Authorization: Bearer <key>` is also accepted).
Source: https://docs.sarvam.ai/api-reference/authentication.md

### 1.1 Text-to-speech (TTS = computer voice) – Bulbul
- `POST /text-to-speech`, JSON body. Source: https://docs.sarvam.ai/api-reference/text-to-speech/convert.md
- Fields: `text` (required, max **2500 characters** for bulbul:v3 and v4-flash; 1500 for v2), `language_code` (required), `speaker`, `pace` (0.5–2.0 on v3/v4-flash, default 1.0), `speech_sample_rate` (8000/16000/22050/24000/32000/44100/48000, default 22050), `model` (`bulbul:v3` = API default, `bulbul:v4-flash` = newest, `bulbul:v2` = legacy), `output_audio_codec` (`wav` default, also `mp3`, `aac`, `flac`, `linear16`, `mulaw`, `alaw`; `opus` currently errors on v3/v4-flash), `temperature` (0.01–1.0, default 0.6, v3/v4-flash only), `dict_id` (pronunciation dictionary).
- `pitch`, `loudness`, `enable_preprocessing` are **not** supported on v3/v4-flash.
- Numbers bigger than 4 digits should be written with commas ("10,000").
- Response: `{request_id, audios: [base64 string]}` – audio is base64 and must be decoded.
- Errors: 400 / 403 / 422 / 429 / 500 with `{error: {message, code, request_id}}`. 402 when credits run out (https://docs.sarvam.ai/api/platform/billing.md).
- **Language codes (exactly these 11):** `bn-IN`, `en-IN`, `gu-IN`, `hi-IN`, `kn-IN`, `ml-IN`, `mr-IN`, **`od-IN`** (Odia – note: *od*, not *or*), `pa-IN`, `ta-IN`, `te-IN`.
- **Voices:** bulbul:v3 short names (lowercase): shubh (default), aditya, ritu, priya, neha, rahul, pooja, rohan, simran, kavya, amit, dev, ishita, shreya, ratan, varun, manan, sumit, roopa, kabir, aayan, ashutosh, advait, anand, tanya, tarun, sunny, mani, gokul, vijay, shruti, suhani, mohit, kavitha, rehan, soham, rupali. bulbul:v4-flash uses 222 persona IDs like `ritu_hi_medical`, but its catalog has **no Malayalam or Odia voices**; v3 covers all 11 languages. Source: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices.md and https://docs.sarvam.ai/api/getting-started/models/bulbul.md
- **Recommended speakers per language for bulbul:v3** (https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices.md):

| Language | Code | Male | Female |
|---|---|---|---|
| English | en-IN | ratan | ishita |
| Hindi | hi-IN | shubh, ashutosh | priya, suhani |
| Telugu | te-IN | shubh, ratan | neha, priya |
| Kannada | kn-IN | shubh, ratan | neha, ishita |
| Bengali | bn-IN | rehan | roopa, suhani |
| Tamil | ta-IN | ratan, rohan | ishita, ritu |
| Odia | od-IN | shubh | ritu, pooja |
| Malayalam | ml-IN | shubh | pooja |
| Marathi | mr-IN | ratan | priya, ritu |
| Punjabi | pa-IN | mani | roopa, suhani |
| Gujarati | gu-IN | ratan | priya, ritu |

  Same page: "varun" is a dramatic voice – do not use. Preset for IVR/telephony: pace 1.1, temperature 0.4, 8 kHz.
- Streaming TTS (HTTP and WebSocket) also exists; not needed for SpiroBuddy. https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview.md

### 1.2 Speech-to-text (STT) – Saaras
- `POST /speech-to-text`, `multipart/form-data`. Source: https://docs.sarvam.ai/api-reference/speech-to-text/transcribe.md
- Fields: `file` (required; WAV, MP3, AAC, OGG, OPUS, FLAC, M4A, AMR, WebM… auto-detected; best at 16 kHz), `model` (`saaras:v4` = default and recommended; `saaras:v3`), `mode` (transcribe/translate/verbatim/translit/codemix – documented as for saaras:v3), `language_code` (`unknown` = auto-detect, or one of the 11 codes plus 12 more Indian languages), `with_timestamps`, `keyterms` (up to 50 terms to bias recognition, saaras:v4 only, sent as a JSON array string).
- Response: `{request_id, transcript, language_code, language_probability?}`.
- **Limit: 30 seconds of audio per REST request** (longer = Batch API). https://docs.sarvam.ai/api/getting-started/models/saaras.md

### 1.3 Translate – Mayura / Sarvam-Translate
- `POST /translate`, JSON. Source: https://docs.sarvam.ai/api-reference/text/translate-text.md
- Fields: `input` (max 1000 chars for `mayura:v1`, 2000 for `sarvam-translate:v1`), `source_language_code` (`auto` allowed with mayura:v1), `target_language_code`, `speaker_gender` (`Male`/`Female`), `mode` (`formal` default, `modern-colloquial`, `classic-colloquial`, `code-mixed`; sarvam-translate:v1 = formal only), `model`, `output_script`, `numerals_format` (`international` default / `native`).
- Response: `{request_id, translated_text, source_language_code}`.

### 1.4 Language identification
- `POST /text-lid`, JSON `{input}` (max 1000 chars). Response `{request_id, language_code, script_code}`. Source: https://docs.sarvam.ai/api-reference/text/identify-language.md

### 1.5 Transliterate and chat (not used by SpiroBuddy)
- Transliterate: `POST /transliterate` https://docs.sarvam.ai/api-reference/text/transliterate-text.md
- Chat: `POST /v1/chat/completions`, models `sarvam-105b`, `sarvam-105b-conversations`. https://docs.sarvam.ai/api-reference/chat/chat-completions-v1.md – SpiroBuddy keeps Claude for writing text (project rule) and only uses Sarvam for voice and translation.

### 1.6 Price, free credits, limits
Source: https://docs.sarvam.ai/api/getting-started/pricing.md , https://docs.sarvam.ai/api/getting-started/ratelimits.md , https://docs.sarvam.ai/api/platform/billing.md
- **Free credits: ₹100 for every new account. Credits never expire.**
- TTS Bulbul v3: ₹30 per 10,000 characters. STT: ₹30 per hour (billed per second). Translate: ₹20 per 10,000 characters. Language ID: ₹3.5 per 10,000 characters.
- Plans: **Starter = pay as you go from credits** (no monthly fee); Enterprise = custom.
- Starter rate limits: TTS 60 requests/min (**30/min for bulbul:v3**), STT 60/min, translate 60/min.

**What the demo costs (estimate):** the whole clip library is about 11 languages × ~35 cues × ~40 characters ≈ 15,000 characters ≈ **₹45**. A day of testing summaries and questions is a few rupees. The free ₹100 covers the demo; adding ₹200–500 of credit gives a safe margin.

### 1.7 Python SDK
`sarvamai` on PyPI, latest 0.1.36 (checked 9 Oct 2026, https://pypi.org/pypi/sarvamai/json). SpiroBuddy calls the REST API directly with `httpx` (already installed) – fewer moving parts, same endpoints.

**Cross-check with the research agent (docs/research/KNOWLEDGE_BASE.md):** agrees on ₹100 free credit, v4-flash lacking Malayalam/Odia, 2,500 chars, pace 0.5–2.0, 30 req/min for bulbul:v3 on Starter, opus failing, and Saaras replacing the deprecated Saarika STT. One difference: it lists translation at ₹0.005/character; the pricing page I read says ₹20 per 10,000 characters (₹0.002/character). Either way it is a few paise per message.

---

## 2. How SpiroBuddy uses it

**Main idea:** the patient always hears a warm voice in their own language. The server picks the best source that works right now.

Think of it like a radio with three stations. The first is a recording made in advance (pre-made clips). The second is a live announcer (Sarvam, made on demand and then kept). The third is a backup speaker built into the computer (the browser voice). If one station is silent, the next one plays.

How it really works, in order, for each spoken cue:
1. **Pre-made clip** `web/audio/<lang>/<cue>.mp3` (made once by `tools/voice/make_clips.py`). Fastest. Works with no internet once the page is loaded.
2. **Sarvam TTS on the server** (`/api/voice/clip/...` or `/api/voice/tts`). The result is saved under `backend/data/tts_cache/`, so the same sentence is never paid for twice.
3. **The browser's own voice** (speechSynthesis), picking the best voice for the language (for example "Microsoft Swara Online (Natural)" for Hindi in Edge).
4. If the browser has **no voice for that language**, it speaks the **English** version of the cue, so the patient still hears something useful.

Where the comparison breaks: the browser voice depends on the computer. Many Windows PCs only have English voices. Edge has more Indian voices than Chrome, and you can add voices in Windows (Settings → Time & language → Speech → Add voices). With the Sarvam key, all 11 languages sound the same on every device.

**Sounds** (`Voice.tone`): one short friendly chime for a good breath, one low soft double-tone for "Slower". They are made in the browser (WebAudio), so there are no files and no harsh alarms.

**Patient questions (push to talk):** the patient holds the 🎤 button and speaks (max 25 seconds; Sarvam allows 30). Sarvam turns it into text. Without a key, Chrome/Edge's own speech recognition is used instead, or the question can be typed. The server then checks it for **danger words in English, romanised Hindi and all 10 Indian scripts** (also on the English translation when a key exists). A danger word gets the fixed message "Please contact your nurse now. If it's an emergency, call 112." in the patient's language, and the question goes into the nurse's message log as `red_flag`. Other questions get "Thank you. I have sent your question to your nurse." (or the "10 slow breaths every hour" answer for "how many/how often"). The AI never answers medical questions.

**Voice-note summary:** `POST /api/voice/summary-audio/{id}` reuses `llm.summarize` (Claude, or the template). Claude writes en/hi/ta directly; for the other 8 languages the English text is translated by Sarvam. Then Sarvam reads it aloud and the server returns an audio URL (and a public URL when `PUBLIC_BASE_URL` is set, for WhatsApp voice notes and automated calls).

**Voice language per patient:** the patients table only allows en/hi/ta, so the voice language (all 11) is stored separately in `backend/data/voice_prefs.json` via `/api/voice/prefs/{id}`. It defaults to the patient's profile language.

## 3. API (prefix /api/voice) – contract
| Method & path | Body | Returns |
|---|---|---|
| GET /status | – | `{enabled, provider:"sarvam"\|"browser", tts_model, stt_model, translate_model, pace, codec, languages:[{lang, code, name, native, speaker}], voices, all_speakers, clips:{lang:count}, cue_count}` |
| GET /cues | `?lang=hi` optional | `{order, languages, cues:{cue:{lang:text}}}` or `{lang, order, cues:{cue:text}}` |
| POST /tts | `{text, language, speaker?, pace?, format?:"mp3"\|"wav"}` | audio file (`X-Audio-Url` header = cached URL), or **503** `{fallback:"browser", text, lang, bcp47}` |
| GET /audio/{file} | – | a cached TTS file |
| GET /clip/{lang}/{cue} | – | pre-made clip → Sarvam TTS → **404** `{fallback:"browser", text, lang}` |
| POST /stt | multipart: `file` (audio ≤30 s) **or** `text`; `language?`, `patient_id?` | `{text, lang, english, red_flag, reply, reply_cue, reply_audio_url, nurse_notified, source}`; **503** `{ok:false, fallback:"browser", error}` without a key |
| POST /translate | `{text, source?:"auto", target}` | `{text, source, target, translated, provider}` (original text without a key) |
| POST /detect | `{text}` | `{lang, script_guess, provider}` |
| GET/PUT /prefs/{patient_id} | `{language?, speaker?, pace?}` | `{patient_id, language, speaker, pace, saved}` |
| POST /summary-audio/{patient_id} | `{language?, speaker?, pace?}` | `{text, lang, text_lang, source, translated, audio_url, public_url, text_en?, fallback?}` |

Languages are our short codes: `en hi bn ta te kn ml mr gu pa or` (Odia = `or` here, `od-IN` at Sarvam; `od`, `hi-IN`, "Hindi" are also accepted).

## 4. For other agents (comms: calls, WhatsApp, guardian page)
**Python** (`from backend.app import voice`), signatures are stable:
- `voice.tts(text, lang, speaker=None, pace=None, fmt=None, sample_rate=None) -> path | None` (use `sample_rate=8000` for phone audio)
- `voice.tts_url(path)` → `/api/voice/audio/<file>`; `voice.public_url(path)` → full URL when `PUBLIC_BASE_URL` is set (Twilio needs it)
- `voice.tts_cue(cue, lang)`; `voice.translate(text, src, tgt) -> str`; `voice.detect_language(text)`; `voice.norm_lang(x)`; `voice.bcp47(x)`
- `voice.red_flag(text) -> bool`; `voice.red_flag_message(lang)`
- `voice_cues.cue_text(cue, lang)`; all cue ids in `voice_cues.CUE_ORDER`
- Optional hook: if `backend/app/comms` exposes `raise_alert(patient_id, kind=, text=, severity=)`, `/api/voice/stt` calls it for red flags (`kind="red_flag"`, severity red) and questions (`kind="voice_question"`, info).

**Browser** (`<script src="js/voice.js">`): `Voice.say(cueOrText, lang, {interrupt, fallbackText})`, `Voice.playUrl(url)`, `Voice.tone('good'|'slower')`, `Voice.record({lang, patientId})` → `{stop(), done}`, `Voice.ask(text, {lang, patientId})`, `Voice.setLang`, `Voice.setMuted`, `Voice.bindMute(button)`, `Voice.fillLangSelect(select)`, `Voice.onChange(fn)`. Each `say` returns a Promise that resolves when that item finishes; items never overlap.
Widgets (`js/voice-ui.js`) mount on `#voice-patient-card`, `#voice-check-card`, `#voice-coach-bar`; `SB.voiceCoach.onState/onEvent/onBreath` speaks coaching during breaths.

## 5. The cue library (all spoken text)
Source of truth: `backend/app/voice_cues.py` (31 cues × 11 languages): ready, breathe_in, slower, hold, count_3/2/1, breathe_out, great_breath, too_fast, breathe_deeper, hold_longer, breath_1 … breath_10 ("Breath N of 10"), session_complete, reminder, missed_reminder, red_flag, encourage_1/2/3, question_noted, faq_how_often. `tools/voice/make_clips.py` also writes `web/audio/cues.json` for the browser.

> **⚠ Needs native-speaker check:** every non-English line (Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia) was written by hand, not by Sarvam, because there was no key yet. They use polite forms (आप / ನೀವು / நீங்கள் style). Please have one native speaker per language read the "Voice check" card before the demo. Most likely to need polish: the "Breath N of 10" phrasing and the Malayalam imperatives (-ഊ forms are friendly; a nurse may prefer more formal ones). Fix wording only in `voice_cues.py`, then re-run `make_clips.py --force --lang <code>`.

## 6. Settings (.env)
| Variable | Default | Meaning |
|---|---|---|
| `SARVAM_API_KEY` | (empty) | The only one you must set. Empty = browser voice + pre-made clips. |
| `SARVAM_TTS_MODEL` | `bulbul:v3` | v3 covers all 11 languages. `bulbul:v4-flash` has no Malayalam/Odia voices. |
| `SARVAM_TTS_SPEAKER` | (empty) | Empty = the calm voice Sarvam recommends for each language (table in §1.1). |
| `VOICE_GENDER` | `female` | `male` switches to the recommended male voices. |
| `SARVAM_TTS_PACE` | `0.9` | A little slower than normal for elderly listeners (0.5–2.0). |
| `SARVAM_TTS_CODEC` | `mp3` | `mp3` or `wav`. |
| `SARVAM_STT_MODEL` | `saaras:v4` | Speech-to-text model. |
| `SARVAM_TRANSLATE_MODEL` | `mayura:v1` | `sarvam-translate:v1` also works (formal only). |
| `SARVAM_TIMEOUT_S` | `25` | Seconds before a Sarvam call gives up and the fallback is used. |
| `PUBLIC_BASE_URL` | (empty) | e.g. `https://spirobuddy.onrender.com`, so WhatsApp/Twilio can fetch voice notes. |

On Render, add `SARVAM_API_KEY` in the service's Environment tab. Render's disk is temporary, so the TTS cache refills after each restart (cheap). The pre-made clips in `web/audio/` should be committed so they ship with the site.

## 7. Test results (9 Oct 2026, no Sarvam key, server on port 8002)
- `/api/voice/status`: enabled false, 11 languages, 31 cues. `/tts` → 503 with `fallback:"browser"`. `/clip/ta/hold` → 404 with the Tamil text. Bad language → 400.
- `/stt` with typed "मुझे सीने में दर्द हो रहा है" → red_flag true, Hindi 112 message, logged for the nurse. "mujhe bukhar hai" (romanised) → red flag, Hindi reply. "how many times…" → the 10-breaths answer. Audio without a key → 503 `{fallback:"browser"}`.
- `/summary-audio/1` in Bengali without a key → English template text + `text_en`, `fallback:"browser"`.
- Browser: patient page card, demo "Voice check" card (31 cues) and the collect page coach all load with no console errors. Collect page simulated breaths spoke: breathe_in → hold → 3, 2, 1 → chime + great_breath → breath 1; a too-fast breath gave the slower tone + "Slower…" → too_fast → breath 2.
- This test browser had only English voices, so Hindi/Tamil cues fell back to the English cue (as designed).
- **Not yet tested: real Sarvam TTS/STT/translate** – no key yet. Run `make_clips.py` and press the cues on the demo panel after adding it.
