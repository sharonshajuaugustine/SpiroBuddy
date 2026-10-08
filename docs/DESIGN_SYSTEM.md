# SpiroBuddy design system – one look for everything

Every SpiroBuddy surface uses this: the nurse/doctor website, the demo panel, the 3D showroom and videos, WhatsApp cards, the device light, slides, and later the patient app. **Source of truth for the values:** the CSS variables at the top of `web/css/styles.css`. If a value changes, change it there and here together.

## 1. Colour
| Token | Light | Dark | Used for |
|---|---|---|---|
| `--brand` | `#0b6e8a` (deep teal) | `#3fb4d4` | Logo, primary buttons, links, the device accent, "breathing in" |
| `--brand-soft` | `#e3f2f6` | `#143241` | Selected tabs, highlights, info boxes |
| `--bg` / `--surface` | `#f4f6f9` / `#ffffff` | `#0f151c` / `#17202a` | Page / cards |
| `--text` / `--text-2` / `--text-3` | `#13202e` / `#4a5868` / `#6b7888` | `#e8eef4` / `#b4c0cc` / `#8d9aa8` | Body / secondary / hints |
| `--green` / `--green-dot` | `#1d7a3a` / `#2e9d4e` | `#5fd17f` / `#4cc06d` | On track, good breath, done ✓ |
| `--yellow` / `--yellow-dot` | `#a15c00` / `#f0a020` | `#f3b443` | Watch, "Slower…", needs attention |
| `--red` | `#c62828` | `#ff6b6b` | Needs a call, missed, red-flag alerts |
| `--focus` | `#1a73e8` | | Keyboard focus ring |

**Meaning is fixed everywhere:** teal = SpiroBuddy / breathing in · green = good / done · amber = slow down / watch · red = needs a person now. The device LED, the app, WhatsApp cards and the dashboard use the same meaning.
**Never use colour alone:** always add a word and an icon (✓ Done, ⚠ Watch, ● Needs a call), for colour-blind users and for patients who can't see well.

## 2. Type
- Font: `"Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif`; Devanagari and Tamil fall back to Nirmala UI / Noto Sans.
- Nurse website: 15–16 px body, 13 px minimum.
- **Patient and guardian surfaces: 20 px body minimum, 32–48 px for the main number, one action per screen.**
- Numbers use tabular figures (`font-variant-numeric: tabular-nums`) so live values don't jump around.

## 3. Shape and space
- Corners: 12 px for cards, 8 px for small items, fully round for pills and status chips.
- Spacing scale: 4, 8, 12, 16, 24, 32, 48.
- Shadows: soft, `0 1px 2px` plus `0 2px 8px`, low opacity.
- Touch targets: 44 px on the nurse site; **64 px on patient and guardian screens**.

## 4. Voice and tone (all text, voice prompts, WhatsApp, calls)
- Warm, short, respectful. Use "Ravi ji" style address in Hindi. No medical jargon.
- Praise first, then one simple next step.
- **Never diagnose.** Red-flag words get the fixed message: "Please contact your nurse now. If it's an emergency, call 112."
- The same phrase means the same thing everywhere (e.g. always "Slower…" / "धीरे…", never a synonym).

## 5. Sound
- One short, friendly chime for a good breath; one low double-tone for "slower"; no harsh alarms for patients.
- The voice is a calm, warm voice in the patient's language, from pre-recorded clips, with browser speech or TTS as fallback.

## 6. Icons and illustration
- Line icons with 2 px strokes, rounded ends, in the current text or brand colour.
- The 3D model and videos use brand teal for the SpiroBuddy unit's accent and the same status colours for the LED and phone screens.
