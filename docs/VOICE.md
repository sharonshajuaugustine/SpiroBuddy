# Voice & language (Sarvam AI) – SpiroBuddy

**In one line:** SpiroBuddy speaks and listens in 11 Indian languages using Sarvam AI (an Indian speech company). Without a Sarvam key it still talks, using pre-made clips or the browser's own voice.

Status of this file: research verified 9 Oct 2026 from the official docs (URLs below). Build notes are added at the end.

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
