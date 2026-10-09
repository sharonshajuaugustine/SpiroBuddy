# SpiroBuddy – Complete Build Plan (Version 2)

*Updated 9 October 2026. This replaces version 1. Fact checks and sources are in **SpiroBuddy_Final_Research.md** on the Desktop.*

**Track:** Healthcare & Wellbeing

**One-line pitch:** The US proved that a clip-on spirometer tracker works. SpiroBuddy brings it to India: it fits the spirometers Indian hospitals already hand out, works at home, coaches in Indian languages and keeps families updated on WhatsApp.

> **Do these two things today**
> 1. Confirm your hackathon's exact name, deadline and judging rules. A third-party site lists the deadline for *Hack for a Social Cause 2026* as **15 October**.
> 2. Order the parts in section 3. Delivery usually takes a few days.

---

## Contents
1. Pitch and positioning
2. How the whole system fits together
3. Shopping list
4. Hardware build
5. Device software (firmware)
6. AI and machine learning
7. Patient app
8. Nurse dashboard
9. Server (backend)
10. Reminders and WhatsApp
11. Privacy, safety and regulation
12. All tools and accounts
13. Team roles
14. Build timeline
15. Testing plan
16. Demo script
17. Pitch deck
18. Answers to judge questions
19. Costs and business model
20. Risks and backups
21. Future roadmap
22. Checklists
23. Words used in this plan
24. Sources

---

## 1. Pitch and positioning

### The story judges will hear
1. **Problem.** After surgery, patients get a ₹300 breathing-exercise device (an incentive spirometer). At home they stop using it or use it wrong, and nobody can tell.
2. **Why it matters in India.** Indian studies find lung complications in roughly 3–30% of surgery patients. At Apollo Hospital, Chennai, the rate was 9.4% overall and over 55% after chest surgery. In a Udaipur study, patients with these complications stayed in hospital 21.7 days instead of 12.5.
3. **Proof that tracking helps.** An hourly reminder doubled how many patients did their exercises: 58% vs 28% (*JAMA Surgery*, Eltorai et al., 2019).
4. **What already exists.** In the US, Penn's Airalux digital spirometer was tested after surgery (patients did about 15 sessions a day), and **InSee**, a clip-on tracker, was cleared by the FDA in August 2025.
5. **The gap.** Those fit American devices, work in hospitals and speak English.
6. **SpiroBuddy.** A clip-on unit, our own breath-technique AI, a voice coach in Indian languages and WhatsApp updates, for use **at home** after discharge.
7. **Honest limits.** It's an exercise coach and tracker. It doesn't diagnose anything.

### How we compare
| | InSee (US) | Airalux (US) | **SpiroBuddy** |
|---|---|---|---|
| What it is | Clip-on box for one US spirometer | A whole new digital spirometer | Clip-on unit for Indian spirometers |
| Where it's used | Hospital | Research trial after surgery | Home, after discharge |
| Coaching | Counts attempts, sends reminders | Reminders, game features | Live voice coach + our own breath-technique AI |
| Language | English | iPhone-only app | Hindi, Tamil, Bengali and more |
| Updates | Hospital system | App | WhatsApp to family and nurse |
| Status | FDA-cleared (2025) | Research trial | Hackathon prototype |

### Words to avoid
| Don't say | Say instead |
|---|---|
| "First in the world" / "nobody has done this" | "Built for India: Indian spirometers, Indian languages, home use" |
| "Diagnoses" / "detects pneumonia" | "Flags patients for a nurse to review" |
| "Prevents pneumonia" | "Helps patients do the exercise doctors prescribe" |
| "Measures lung function" | "Tracks breathing exercises" |
| "Costs ₹1,000" (unless you've proven it) | "About ₹X as a hand-built prototype; we aim for under ₹1,000 in mass production" |

---

## 2. How the whole system fits together

```
 [Romsons spirometer]   the disc rises when the patient breathes in
          |
 [SpiroBuddy clip-on unit]   laser sensor -> tiny computer (ESP32) -> beeper + light
          |   Bluetooth   (backups: USB cable or Wi-Fi)
 [Patient app on an Android phone]   live gauge, voice coach, today's checklist
          |   internet
 [Server]   database, reminders, AI reports, WhatsApp sending
          |                         |
 [Nurse dashboard]          [WhatsApp to family and nurse]
```

### What happens during one session
1. The patient presses the button on the unit and taps **Start** in the app.
2. The laser measures how high the disc is, 30 times a second. The unit turns that height into mL.
3. A small program on the unit follows each breath through four stages: waiting → breathing in → holding → falling. This is called a **state machine**.
4. If the disc rises too fast, the phone instantly says "Slower…" in the patient's language (a pre-recorded clip), and the light turns amber.
5. When the breath ends, **our own AI model, running on the unit**, labels it: *good*, *too fast*, *too shallow* or *no hold*. The app shows a score out of 10.
6. When the patient reaches the target volume, the unit beeps.
7. After 10 breaths, that hour's reminder ticks itself off and the results upload to the server.
8. In the evening, the server writes a 3-sentence summary and sends it on WhatsApp to the family and nurse.

---

## 3. Shopping list

Prices are rough online prices in India (October 2026). Check before buying.

**Where to buy:**
- **Electronics:** Robu.in, Robocraze, Amazon.in, or a local electronics market such as Lamington Road (Mumbai), SP Road (Bengaluru), Lajpat Rai Market (Delhi) or Ritchie Street (Chennai).
- **Spirometer:** a local chemist or medical store, Medikabazaar or Amazon.in.

### A. Core parts: buy today
| # | Item | Qty | Price each (approx.) | Notes |
|---|---|---|---|---|
| 1 | **Romsons Breazer 2500** volumetric spirometer | 2 | ₹220–500 | One to build on, one spare. It must be the **volumetric (piston)** type, not the 3-ball type. Buy one from a local chemist today so the 3D design can start. |
| 2 | **Seeed Studio XIAO ESP32-C3** board | 2 | ₹500–900 | The unit's tiny computer. It has Bluetooth and Wi-Fi, and charges a battery by itself. One spare. Attach the small antenna that comes in the box. |
| 3 | **VL53L1X** laser distance sensor module | 2 | ₹500–1,000 | The main sensor. One spare. |
| 4 | VL53L0X laser distance sensor module | 1 | ₹250–400 | Backup sensor to compare against. |
| 5 | LiPo battery 3.7 V, 400–600 mAh, **with protection circuit** | 2 | ₹200–400 | Powers the unit. One spare. |
| 6 | Passive piezo buzzer | 2 | ₹20–40 | Can play different tones. |
| 7 | WS2812B single-LED module ("NeoPixel") | 2 | ₹20–50 | Status light that can show any colour from one pin. |
| 8 | Tactile push buttons (pack) + mini slide switch | 1 each | ₹30–50 | Start button and power switch. |
| 9 | Resistor kit (must include 220 kΩ) | 1 | ₹80–150 | For reading the battery level. |
| 10 | Breadboard (830 points) + jumper wire set | 1 | ₹150–250 | For testing before soldering. |
| 11 | Small perfboard + header pins | 1 | ₹50–100 | For the final soldered version. |
| 12 | Thin silicone wire (26–30 AWG) | 1 | ₹50–100 | Wiring inside the unit. |
| 13 | USB-C cables **that carry data** | 2 | ₹100–200 | Charge-only cables can't upload code. |

### B. Materials for the clip-on unit
| # | Item | Qty | Price (approx.) | Notes |
|---|---|---|---|---|
| 14 | 3D printing: 3–5 test prints | — | ₹300–800 total | Use a college makerspace or a printing service. PETG handles alcohol wipes better than PLA. |
| 15 | Black EVA foam sheet, 2–3 mm | 1 | ₹50–100 | Ring around the sensor to block stray light. |
| 16 | Velcro strap or elastic band | 1 | ₹50–100 | Holds the unit on the spirometer. |
| 17 | Small screws and nuts (M2 / M2.5) | 1 kit | ₹100–150 | Closes the case. |
| 18 | Double-sided foam tape + hot-glue sticks | 1 each | ₹80–150 | |
| 19 | Heat-shrink tubing set | 1 | ₹80–150 | Covers soldered joints. |
| 20 | 70% isopropyl alcohol wipes | 1 pack | ₹80–150 | Cleaning between users. |

### C. Optional extras
| # | Item | Price (approx.) | Why |
|---|---|---|---|
| 21 | 0.96" OLED display (SSD1306, I²C) | ₹200–300 | Shows breath count and score on the unit itself, for patients without a phone. |
| 22 | USB power meter | ₹300–500 | Measures battery use, so your battery-life claim is real. |
| 23 | Small USB power bank | (you may have one) | Backup power on the demo table. |

### D. Tools: borrow from your college lab if you can
| # | Tool | Price if buying |
|---|---|---|
| 24 | Soldering iron kit (iron, stand, solder, flux) | ₹500–900 |
| 25 | Digital multimeter | ₹300–700 |
| 26 | Digital vernier caliper, 150 mm (to measure the spirometer for the 3D design) | ₹500–1,000 |
| 27 | Wire stripper, cutter, small screwdrivers | ₹200–400 |
| 28 | Hot-glue gun | ₹200–400 |

### E. Things you need that aren't bought in a shop
- An **Android phone with Chrome**. The app uses Bluetooth through the browser, which doesn't work on iPhones. A laptop with Chrome also works.
- A laptop for coding.
- Online accounts (section 12). Claude API credit costs about ₹500–1,000 for the whole project (estimate). The rest are free tiers.

### Budget summary
| Part | Approx. total |
|---|---|
| A. Core parts, minimum (no spares) | ₹1,950–3,800 |
| A. Core parts, recommended (with spares) | ₹3,750–7,300 |
| B. Materials | ₹750–1,600 |
| C. Optional extras | ₹500–800 |
| D. Tools (only if you can't borrow them) | ₹1,700–3,400 |
| Online services | ₹500–1,000 |

**Parts inside one finished unit:** about ₹1,400–2,600 at retail prices (board, sensor, battery, beeper, light, button and printed case).

---

## 4. Hardware build

### 4.1 The spirometer
- Use the **Romsons Breazer 2500** first. Design for one model only, and add others later.
- With a vernier caliper, measure: chamber diameter, height, the disc's lowest and highest positions, and where the air openings are.
- Look for printed mL marks on the side. You'll use them for calibration.
- **Never change the air path of a spirometer a patient will use.** Experiment only on your spare.

### 4.2 The sensor
- **VL53L1X**, a laser distance sensor that measures by timing how long light takes to bounce back. Its laser is Class 1, meaning it's eye-safe.
- **Settings:** short-distance mode (best below 1.3 m and in bright rooms) and about 33 ms per reading, which gives roughly 30 readings a second.
- **Narrow the view:** the VL53L1X can shrink its field of view from about 27° down to about 15°, so it sees the disc and not the chamber walls. Aim the centre of the view at the middle of the disc.
- **Calibrate it:** run the library's offset calibration (a white card at a known distance, e.g. 100 mm). If there's plastic in front of the sensor, also run crosstalk calibration.
- **Keep at least 5 cm between sensor and disc at all times.** The sensor can't measure reliably closer than about 4 cm.
- **Backup:** the VL53L0X (fixed view of about 25°).

### 4.3 Where to mount the sensor (test both on day 2)
| Option | How | Good | Watch out |
|---|---|---|---|
| **A. Base mount** (tried first) | The spirometer sits on a short stand. The sensor looks **up** at the underside of the disc. | In most volumetric spirometers, outside air enters under the disc through the base, so there's often a gap with **no plastic in the way**. InSee also mounts at the base. | Don't block the air openings: leave channels in the stand. Keep the 5 cm minimum distance. |
| **B. Top mount** | The sensor sits on a bracket on top and looks **down** through the chamber top. | Easy to clip on. | The laser goes through plastic, which can cause false readings (crosstalk). Press the sensor flat against the plastic with no air gap, put a foam ring around it and run crosstalk calibration. |

Check your Breazer unit first: designs differ, so confirm where the air enters and whether the base is open.

### 4.4 Wiring (XIAO ESP32-C3)
| Part | Part pin | XIAO pin |
|---|---|---|
| VL53L1X sensor | VIN | 3V3 |
| | GND | GND |
| | SDA (data) | D4 |
| | SCL (clock) | D5 |
| | XSHUT (on/off) | D10 |
| Piezo buzzer | + | D2 |
| | − | GND |
| WS2812B light | DIN | D3 |
| | VCC / GND | 3V3 / GND |
| Push button | one leg / other leg | D1 / GND (uses the chip's built-in pull-up) |
| Battery level | middle of two 220 kΩ resistors | A0 (D0); follow Seeed's wiki for the battery divider |
| LiPo battery | + / − | BAT+ / BAT− pads under the XIAO, through the slide switch |
| OLED (optional) | SDA / SCL / VCC / GND | D4 / D5 / 3V3 / GND (shares the sensor's I²C wires) |

Notes:
- D1 is wired to the button on purpose. On the ESP32-C3, only pins GPIO 0–5 can wake the chip from deep sleep, and D1 is GPIO 3.
- Build everything on the breadboard first. Solder onto perfboard only after it all works (day 7).

### 4.5 The clip-on unit (3D design)
1. Design it in **Fusion 360** (free for personal use), **Onshape** or **Tinkercad** (easiest).
2. **Print a thin "fit-test ring" first.** It takes about 10 minutes and checks that the unit fits the spirometer. Adjust, then print the full unit.
3. Design rules:
   - The sensor stays at least 5 cm from the disc in every position.
   - Air openings stay open.
   - A black foam ring goes around the sensor.
   - The USB-C port stays reachable for charging.
   - The battery has its own small compartment.
   - Walls are about 2 mm thick, with no sharp edges.
   - The unit comes off in 5 seconds for cleaning.
4. Print in PETG (better with alcohol wipes) or PLA (fine for prototypes).
5. Hold the unit on with a snug collar lined with foam, or a Velcro strap.

### 4.6 Calibration: turning disc height into mL
1. **Sensor check (once per unit):** offset calibration with a white card; crosstalk calibration if there's plastic in front.
2. **Volume table (once per spirometer model):**
   - One person breathes in and holds the disc steady at a printed mark (500, 1,000, 1,500, 2,000 mL).
   - A teammate presses a key to record the reading.
   - Do each mark 3 times and average the readings.
   - Save the table on the unit. Readings between marks are worked out with a straight line between the two nearest points (called **interpolation**).
3. **Accuracy check:** do 20 breaths and compare the unit's reading with the mark you see by eye.
   - Our target: within ±100 mL.
   - Put the real number on a slide.

### 4.7 What the light and beeper mean
| Signal | Meaning |
|---|---|
| Blue blinking | Waiting to connect |
| Blue steady | Connected to the phone |
| Green | Good breath / target reached |
| Amber | Slow down |
| Red blinking | Battery low |
| One short beep | Target reached |
| Two low beeps | Too fast |
| Three rising tones | Session complete |

### 4.8 Power and battery
- The unit runs on a 400–600 mAh LiPo battery and charges over USB-C through the XIAO.
- Between sessions, it switches the sensor off (XSHUT) and puts the chip to sleep. A button press wakes it.
- **Rough estimate:** several days per charge with sleep. **Measure it** with a USB power meter before you claim a number.

---

## 5. Device software (firmware)

### 5.1 Setup
- **Arduino IDE 2**, with the "esp32 by Espressif Systems" board package. Choose the board **XIAO_ESP32C3**.
- Turn on **Tools → USB CDC On Boot → Enabled**, or the Serial Monitor shows nothing on this board.
- **Libraries:**
  - SparkFun VL53L1X (sensor)
  - NimBLE-Arduino (Bluetooth)
  - Adafruit NeoPixel (light)
  - emlearn (our AI model)
  - The built-in Preferences (saves calibration) and LittleFS (stores breaths while offline)

### 5.2 Code files
| File | Job |
|---|---|
| `spirobuddy.ino` | Starts everything; runs the 30-times-a-second loop |
| `sensor.cpp` | Reads distance, smooths it (median of the last 5 readings), converts to mL |
| `breath_fsm.cpp` | The breath state machine |
| `features.cpp` | Works out the numbers that describe each breath |
| `spirobuddy_model.h` | Our trained AI model, generated by emlearn |
| `feedback.cpp` | Beeps and light colours |
| `ble.cpp` | Bluetooth connection to the app |
| `storage.cpp` | Saves breaths while offline; uploads them later |

### 5.3 The breath state machine (starting values; tune them with your data)
| Stage | Starts when | Ends when |
|---|---|---|
| WAITING | Session starts, or the last breath finished | Volume goes above 150 mL and rising → BREATHING IN |
| BREATHING IN | The disc is rising | The rise stops for 0.3 s → HOLDING; or it drops → FALLING |
| HOLDING | The disc stays near its peak | It drops more than 10% below the peak → FALLING |
| FALLING | The disc is going down | Volume goes below 100 mL → **breath finished** → WAITING |

Safety rules:
- Ignore "breaths" shorter than 0.5 s or with a peak under 250 mL. These are bumps, not breaths. InSee also counts only attempts above 250 mL.
- Reset after 20 s if something gets stuck.

### 5.4 What gets saved for each breath
Time, peak mL, % of target, time to peak, average and fastest rise speed, hold seconds, smoothness, AI label and score.

### 5.5 Bluetooth design
One custom service, with five "characteristics" (data channels):

| Channel | Direction | What it carries |
|---|---|---|
| `live` | Unit → phone | Current mL and stage, about 20 times a second (for the gauge) |
| `breath` | Unit → phone | One record per finished breath |
| `command` | Phone → unit | Start/stop session, set target, set clock, ask for stored breaths |
| `status` | Unit → phone | Battery %, software version, calibrated yes/no |
| `sync` | Unit → phone | Breaths stored while offline, sent in small chunks |

- The unit has no clock of its own, so the phone sends the current time each time it connects.
- Make your own unique IDs (UUIDs) for the service and channels with any online UUID generator.

### 5.6 Backup connections
1. **USB cable to a laptop:** the same web app reads the data through Chrome's Web Serial feature. This is the best fallback if Bluetooth fails at the venue.
2. **Wi-Fi:** the unit sends data to the laptop server over a live connection (WebSocket).

### 5.7 Offline behaviour
Without the phone, the unit still counts, beeps and stores up to about 2,000 breaths. It uploads them at the next connection.

---

## 6. AI and machine learning

### 6.1 The AI parts at a glance
| Part | Type | Runs on | Job |
|---|---|---|---|
| **Breath-technique checker** ⭐ | **Our own trained model** (random forest) | The unit's chip (backup: server) | Labels each breath |
| Instant speed warning | Simple rule | Unit + phone | Says "Slower…" with no delay |
| Voice coach | Pre-recorded clips made with Sarvam's Bulbul voice | Phone (works offline) | Speaks cues in the patient's language |
| After-session feedback | LLM (Claude), spoken by Sarvam | Server | One personal sentence |
| Nurse and family report | LLM (Claude) | Server | 3 sentences in any supported language |
| Patient Q&A *(stretch goal)* | LLM restricted to a nurse-approved guide | Server | Answers simple questions |
| Recovery flags | Rules (on purpose) | Server | "Review suggested" alerts |

### 6.2 Our own model, step by step

**1. Set up data collection**
- The unit streams readings over USB to a laptop.
- A Python script, `collect.py` (using pyserial), shows a live graph.
- Before each breath, press a key for the kind of breath: **g** = good, **f** = too fast, **s** = too shallow, **n** = no hold.
- The script cuts out each breath and saves it with its label and the person's ID.

**2. Write down how to do each kind of breath**, so everyone does them the same way:
| Label | How to breathe |
|---|---|
| good | Slow, steady breath in over 3–5 seconds to your usual depth, then hold for 3 seconds |
| too fast | Breathe in sharply, like a gasp |
| too shallow | Stop at about a third of your usual breath |
| no hold | Breathe in fully, then let go straight away |

**3. Collect the data**
- 4–6 healthy adults (the team plus friends, with their permission). Each does 60–80 breaths, in sets of 10.
- Aim for **300+ breaths** in total, with about the same number of each kind.
- Sit upright, and rest 30–60 seconds between sets.
- **Stop if anyone feels dizzy.** Deep-breathing exercises can make people light-headed.

**4. Turn each breath into 8 numbers** (called **features**): peak mL, % of target, time to peak, average rise speed, fastest rise speed, hold time, smoothness (how jerky the rise was) and total duration.

**5. Train the model** in a Jupyter notebook, `train.ipynb`:
- Use scikit-learn's **RandomForestClassifier** with 10–20 trees and depth of 8 or less, so it fits on the chip.
- Also write a simple rule-based checker. This is the **baseline** the AI has to beat.

**6. Test it fairly: "leave one person out".**
- Train on everyone except one person, test on that person, and repeat for each person.
- This shows the model works on **people it has never seen**.
- Report accuracy, results per breath type, and a **confusion matrix** (a table of what it got right and what it mixed up).
- Make a chart of which features mattered most. It makes a good slide.

**7. Targets**
- At least 85% correct on unseen people, and better than the rule baseline.
- If you fall short: collect more data, merge two breath types, or add features.

**8. Put it on the chip**
- Use **emlearn** to convert the model into C code (`spirobuddy_model.h`) and add it to the firmware. Follow emlearn's Arduino example.
- Check that the chip and the laptop give **the same labels** for 20 test breaths.

**9. Fallback:** if the chip version fails, run the same model on the server. You can still truthfully say "our own model".

**Pitch line:** "We recorded X breaths from Y people and trained our own model. It runs on a ₹600 chip with no internet, and labels breathing technique correctly Z% of the time on people it has never seen."

### 6.3 Breath score out of 10 (simple, explainable maths)
- **Depth:** 0–4 points = 4 × (peak ÷ target), maximum 4.
- **Speed:** 3 points if the rise speed is in the "good" range, 1 if a bit fast, 0 if too fast. The ranges come from the *good* breaths in your data.
- **Hold:** 0–3 points = 3 × (hold seconds ÷ hold target), maximum 3. The default hold target is 3 seconds; the nurse can change it.
- **Score** = depth + speed + hold.

The score is plain maths, so anyone can check it. The AI label explains *what* went wrong.

### 6.4 Voice coach
- **12 phrases, recorded once per language:**
  1. Sit up straight and breathe out normally.
  2. Now breathe in slowly and deeply.
  3. Slower…
  4. A little deeper…
  5. Hold it… 3, 2, 1.
  6. Great breath!
  7. You reached your target!
  8. Rest and breathe normally.
  9. Breath number 1 … 10 (one clip per number).
  10. Session complete. Well done!
  11. Time for your breathing exercise.
  12. Please charge your SpiroBuddy.
- **Hindi examples:** "धीरे-धीरे गहरी साँस लें" (breathe in slowly and deeply) · "थोड़ा धीरे…" (a little slower) · "साँस रोकें… 3, 2, 1" (hold your breath) · "बहुत बढ़िया!" (excellent!)
- **How to make the clips:**
  - A script, `generate_audio.py`, calls **Sarvam's Bulbul v3** text-to-speech (model `bulbul:v3`) and saves MP3 files into the app.
  - The clips are pre-made, so they play instantly and work without internet.
- **Demo languages:** Hindi, English and one regional language that fits your judges' region (e.g. Tamil, Kannada or Bengali).
- **Have a native speaker check every clip.**

### 6.5 LLM setup (Claude)
- **Connection:** the Anthropic Python package `anthropic`. Keep the key in a `.env` file as `ANTHROPIC_API_KEY`. **Never put it on GitHub.**
- **Model:**
  - Default: **Claude Opus 5.5** (`claude-opus-5-5`).
  - **Your choice:** Claude Haiku 5.5 (`claude-haiku-5-5`) is much faster and about 40× cheaper. Test both in your 3 languages and pick.
- **Settings:**
  - Set effort to **"low"** for these short replies. It's faster, and Opus 5.5's default is "medium".
  - Opus 5.5's thinking can't be turned off. That's fine for this use.
- **Fixed format for the nurse report:** use the structured-output feature so the reply always comes back in the same shape (3 sentences + a family message). The server then checks it automatically.
- **Error handling:** check the reply's `stop_reason`. If it isn't a normal finish (for example a refusal, or cut off for length), use the template text instead.
- **Template fallback for every AI feature.** Example: "Ravi completed {done} of {due} sessions today. Best breath {best} mL." The demo then never depends on the internet or the AI.
- **The AI never decides alerts or colours.** Rules do that (section 6.7). The AI only puts results into words.
- **Optional, for the Q&A:** Claude's *citations* feature can show which line of the nurse's guide an answer came from. Nurses like that. It can't be combined with the fixed-format feature, so use it only for the Q&A.
- **Cost estimate** (October 2026 list prices: Opus 5.5 $4 / $20, Haiku 5.5 $0.10 / $0.50 per million input / output tokens):
  - One short call costs about ₹0.9 on Opus or ₹0.02 on Haiku.
  - Development plus demo: roughly ₹500–1,000 on Opus.

**Prompt outlines** (finalise them in code):
- **After-session coach:** "You are SpiroBuddy, a kind breathing-exercise coach. Write ONE short sentence (max 15 words) in {language} for an elderly patient, based on these results: {json}. Praise one thing and suggest one improvement if needed. Never give medical advice or mention illnesses."
- **Nurse report:** "Write exactly 3 short sentences in {language} summarising today's breathing exercises for a nurse. Use only the numbers given. Don't diagnose or suggest treatment. If status is 'review', end with 'A check-in call is suggested.'"
- **Q&A (stretch):** "Answer only from the guide below. If the answer isn't there, say you don't know and suggest asking the nurse."

**Safety check before the AI:** the server looks for warning words in each language (pain, chest pain, fever, breathless, blood, dizzy). If it finds one, **it skips the AI** and shows a fixed message: "Please contact your nurse or doctor now. In an emergency, call 112 (or 108 for an ambulance)." Safety then doesn't depend on the AI.

### 6.6 Speech input for the Q&A (stretch goal)
Use Sarvam's speech-to-text or Chrome's built-in speech recognition. Keep typed input as the default.

### 6.7 Recovery flags (rules, not AI, on purpose)
| Flag | Rule (starting values; agree them with a nurse) | Shows as |
|---|---|---|
| Low practice today | Less than 50% of due sessions done by 6 pm | 🟡 |
| Missed in a row | 2 sessions missed in a row | 🔴 + WhatsApp alert |
| Dropping trend | Best breath of the day down 3 days running, or more than 20% below the patient's best for 2 days | 🟡 "Review suggested" |
| Not syncing | No data for 6+ waking hours | ⚪ "Device offline" |

**Target suggestion:** if a patient beats their target on 80% of breaths for 2 days, the dashboard *suggests* a new target (90% of their recent best). **Only the nurse can approve it.**

---

## 7. Patient app

### 7.1 Why a web app (PWA)
- It installs from Chrome with "Add to Home screen". There's no Play Store approval to wait for.
- Bluetooth from a web page (**Web Bluetooth**) works in Chrome on Android, Windows, Mac and ChromeOS, but **not on iPhones**. iPhone families can still get WhatsApp updates.
- **Rule:** Bluetooth needs a secure (HTTPS) link and a tap from the user, so the patient taps **Connect** once each time they open the app.

### 7.2 Tools
- React + Vite (app framework and build tool)
- vite-plugin-pwa (makes it installable and offline)
- Chart.js (graphs)
- idb (stores data on the phone)
- Web Bluetooth, plus Web Serial for the laptop backup

### 7.3 Screens
1. **Welcome:** pick a language first, then a consent screen in that language and the family's WhatsApp number.
2. **Connect:** one big button.
3. **Home:**
   - Today's checklist (8 am–9 pm): ✅ done, ⏳ upcoming, ❌ missed
   - Next reminder time and streak
   - A big **Start** button
4. **Session:**
   - A big gauge rising to a target line
   - A slow / OK / fast speed meter
   - A breath counter (x of 10) and a hold countdown
   - Voice cues
5. **Results:** score for each breath, labels in plain words, best breath, and one spoken AI sentence.
6. **Progress:** daily best breath (line chart), sessions per day (bars), streak badges.
7. **Ask** *(stretch)*: Q&A with a microphone button.
8. **Settings:** language, reminder hours, large text, family contacts, sound on/off.

### 7.4 Design rules for elderly patients
- Text at least 18 px, with strong contrast.
- Icons and words together.
- One main action per screen.
- Everything is also spoken aloud.
- It works offline after the first load.

### 7.5 Offline and demo modes
- **Offline:** a service worker (a background helper in the browser) keeps the app and voice clips on the phone. Breaths wait in phone storage and upload when the internet returns.
- **Replay mode** (hidden switch): plays recorded breaths as if they came from the unit.
  - The app team can build everything **before the hardware is ready**.
  - It's also a last-resort demo backup.

---

## 8. Nurse dashboard
It's part of the same React project, at `/nurse`.

- **Login:** a PIN for the demo. A real product needs proper accounts.
- **Patient list**, red patients first. Each row shows:
  - name and surgery
  - days since discharge
  - sessions today (e.g. 9/14)
  - best breath vs target
  - trend arrow and colour
- **Patient page:**
  - 7-day charts (best breath and sessions per day) and today's breaths
  - the AI's 3-sentence summary and any flags
  - **Set target**, **Set reminder hours**, **Send summary now**, **Download PDF** (the browser's print-to-PDF)
- **Live updates:** new sessions appear within seconds (WebSocket), so judges see the demo breath arrive.
- **Demo data:** a script, `seed_demo_data.py`, creates 6 fake patients with a week of history (2 green, 2 yellow, 1 red, plus your live demo patient).

---

## 9. Server (backend)

### 9.1 Tools
| Tool | Job |
|---|---|
| Python 3.12 + FastAPI + Uvicorn | The web server |
| SQLModel + SQLite | The database. SQLite is a single file, fine for the demo; switch to PostgreSQL later. |
| APScheduler | Timed jobs (reminders, evening reports) |
| pywebpush | Phone notifications. Needs "VAPID" keys, a key pair that lets your server send notifications. |
| twilio | WhatsApp messages |
| httpx | Calls Sarvam's API |
| anthropic | Calls Claude |
| scikit-learn + joblib | Server copy of our model (backup) |
| python-dotenv | Loads secret keys from `.env` |

### 9.2 Database tables
| Table | Main fields |
|---|---|
| patients | id, first name, language, surgery type, target mL, hold target, reminder start/end, family phone, nurse id |
| devices | id, patient id, Bluetooth id, calibration table |
| sessions | id, patient id, start, end, breaths, good breaths |
| breaths | id, session id, time, peak mL, time to peak, rise speeds, hold, smoothness, label, score |
| slots | id, patient id, hour, status (done / missed / snoozed) |
| messages | id, patient id, channel, recipient, text, sent time, status |
| nurses | id, name, PIN (stored scrambled) |
| push_subscriptions | patient id, browser subscription details |

### 9.3 Main web addresses (API endpoints)
| Endpoint | Does |
|---|---|
| `POST /api/breaths` | Uploads a batch of breaths |
| `POST /api/sessions` | Starts or ends a session |
| `GET /api/patients/{id}/today` | Today's checklist and stats |
| `GET /api/patients/{id}/history?days=7` | Chart data |
| `PUT /api/patients/{id}/target` | Nurse sets the target |
| `GET /api/nurse/patients` | Dashboard list with colours |
| `POST /api/coach/feedback` | AI sentence after a session |
| `POST /api/reports/{id}/send` | Sends the WhatsApp summary now |
| `POST /api/push/subscribe` | Registers the phone for notifications |
| `POST /api/qa` | Q&A *(stretch)* |
| `WS /ws/live` | Live updates for the dashboard |

### 9.4 Timed jobs
| Job | When | What it does |
|---|---|---|
| Hourly reminder | On the hour, within each patient's hours | Phone notification (and WhatsApp if chosen) |
| Missed check | 10 minutes before the next slot | Marks the slot missed; 2 in a row triggers an alert |
| Evening report | 9:30 pm | AI summary → WhatsApp to family and nurse |
| Trend check | 10 pm | Updates the flags |

**Fast-clock mode:** a test setting where 1 minute equals 1 hour. You can check a whole day of reminders in 15 minutes, or show "a day in one minute" in the demo.

### 9.5 Hosting
- **Demo:**
  - Run the server on a laptop and share it through **Cloudflare Tunnel** (free). It gives an HTTPS web address, which phones and Twilio need.
  - Put the app on **Vercel** or **Netlify** (free).
- **Later:** a cloud server in an Indian region, so data stays in India.

### 9.6 Project folder layout (one GitHub repository)
```
spirobuddy/
  firmware/      Arduino code + spirobuddy_model.h
  ml/            collect.py, features.py, train.ipynb, export_model.py, data/
  backend/       FastAPI app, database, AI, voice, WhatsApp, scheduler, .env.example
  app/           React app (patient app + nurse dashboard), public/audio/<language>/
  cad/           3D design files, STL files, fit-test ring
  scripts/       generate_audio.py, seed_demo_data.py
  docs/          pitch deck, demo script, photos, test results
```

---

## 10. Reminders and WhatsApp

### 10.1 Reminder channels
1. **Phone notification** from the server (web push).
   - Works in Chrome on Android.
   - On iPhone, it works only if the app was added to the home screen (iOS 16.4 or later).
2. **WhatsApp message.** Optional; the patient or family chooses.
3. **Beep on the unit**, if it's switched on.

Quiet hours: no messages between 10 pm and 8 am.

### 10.2 WhatsApp
- **Demo: Twilio WhatsApp Sandbox** (free trial).
  - Each phone must first send the "join <code>" message to the sandbox number.
  - **Send it again on demo morning** so the link is fresh.
- **Real product: Meta's WhatsApp Business Platform.**
  - It needs business verification and pre-approved message templates to message people who haven't written in the last 24 hours.
  - Meta charges per message, so check current India prices.
- **Example messages:**
  - *Family, evening:* "SpiroBuddy update for Ravi: 9 of 14 breathing sessions done today. Best breath 1,500 mL, up 15% since Monday. Please encourage the afternoon sessions."
  - *Missed alert:* "Ravi has missed 2 breathing sessions in a row. A gentle reminder may help."
  - *Nurse:* the AI's 3-sentence summary plus a dashboard link.

---

## 11. Privacy, safety and regulation

### 11.1 Privacy
- Collect the minimum: first name, language, phone numbers and breath numbers.
- Show a consent screen in the patient's language, saying who sees what. Share data only with people the patient chooses.
- Add a "Delete my data" button. Use HTTPS everywhere.
- Keep API keys in `.env`, and add `.env` to `.gitignore`.
- Follow the principles of India's **Digital Personal Data Protection Act, 2023**: clear consent, used only for the stated purpose.
- **In the hackathon, use fake patients only. No real health data.**

### 11.2 Safety rules
1. The AI coaches and summarises. It never diagnoses or gives treatment advice.
2. Warning words skip the AI and show a fixed "contact your nurse / call 112" message.
3. Alerts and colours come from rules a nurse agreed to, not from the AI.
4. The nurse approves any change to a patient's target.
5. **Hardware:**
   - The laser sits outside the breathing path, and the unit doesn't block air openings.
   - Use a LiPo with a protection circuit, and no sharp edges.
   - Wipe with alcohol between users.

### 11.3 Regulation (what to tell judges)
- India's regulator, **CDSCO**, classes medical devices from A (lowest risk) to D (highest). We couldn't confirm the class for incentive spirometers.
- CDSCO finalised guidance for medical device software in **July 2026**. General **wellness** apps are excluded, and what the maker says the product is *for* decides how software is treated.
- **Answer:** "Today it's an exercise coach and tracker, not a diagnostic. Before launch we'd get an official ruling through CDSCO's online classification portal."

---

## 12. All tools and accounts

### Hardware and design
| Tool | Used for | Cost |
|---|---|---|
| Fusion 360 / Onshape / Tinkercad | 3D design of the unit | Free (personal or education) |
| UltiMaker Cura / PrusaSlicer / Bambu Studio | Preparing 3D prints | Free |
| Soldering kit, multimeter, vernier caliper | Building and measuring | See section 3 |

### Device software
| Tool | Used for | Cost |
|---|---|---|
| Arduino IDE 2 + esp32 board package | Writing and uploading firmware | Free |
| SparkFun VL53L1X, NimBLE-Arduino, Adafruit NeoPixel, emlearn | Libraries | Free |
| nRF Connect (Android app) | Testing the unit's Bluetooth channels | Free |

### AI and data
| Tool | Used for | Cost |
|---|---|---|
| Python 3.12, Jupyter | Data collection and training | Free |
| pandas, numpy, scikit-learn, matplotlib, joblib, pyserial | Data, model, charts | Free |
| emlearn (Python) | Converting the model for the chip | Free |
| Claude API (Anthropic) | Feedback sentences, reports, Q&A | Pay per use: about ₹500–1,000 for the project |
| Sarvam AI (Bulbul v3 voice; speech-to-text optional) | Indian-language voice | Free tier |

### App and server
| Tool | Used for | Cost |
|---|---|---|
| VS Code, Git, GitHub | Code and teamwork | Free |
| Node.js (LTS), React, Vite, vite-plugin-pwa, Chart.js, idb | Patient app and dashboard | Free |
| FastAPI, SQLModel, APScheduler, pywebpush, twilio, httpx, anthropic, python-dotenv | Server | Free |
| Twilio | WhatsApp sandbox | Free trial |
| Cloudflare Tunnel | HTTPS link to the laptop server | Free |
| Vercel or Netlify | Hosting the app | Free tier |
| Chrome DevTools, Lighthouse, FastAPI's built-in `/docs` page | Testing | Free |

### Pitch
| Tool | Used for | Cost |
|---|---|---|
| Google Slides or Canva | Pitch deck | Free |
| OBS Studio | Recording the backup demo video; combining camera and screen in an online demo | Free |
| Figma (optional) | Screen designs | Free tier |

### Accounts to create on day 0
Anthropic (API key + credits), Sarvam AI, Twilio, GitHub, Vercel or Netlify, Cloudflare.

---

## 13. Team roles (3 people; adjust to your team)
| Person | Owns | Also helps with |
|---|---|---|
| **A: Hardware** | Spirometer measurements, 3D design, wiring, sensor, calibration, firmware, Bluetooth, model on the chip | Data collection |
| **B: AI & server** | Data-collection script, training, emlearn export, server, database, Claude, Sarvam voice, reminders, WhatsApp | The nurse call |
| **C: App & pitch** | Patient app, nurse dashboard, replay mode, charts, design, pitch deck, demo video | Testing with an older person |

**Everyone:** data-collection day (day 4), integration day (day 8) and rehearsals.

---

## 14. Build timeline

**Day 0 (today):**
- Confirm the event and its rules, and register.
- Order the parts, and buy a spirometer from a local chemist.
- Create accounts and the GitHub repository.
- **Book a 10-minute call with a nurse or physiotherapist** for days 1–3.

| Day | A: Hardware | B: AI & server | C: App & pitch | Done when… |
|---|---|---|---|---|
| 1 | Measure the spirometer; start the 3D design; print a fit-test ring | Server skeleton, database, fake-patient script | App skeleton, replay mode, screen sketches | The app shows replayed breaths |
| 2 | Wire the sensor on a breadboard; test base vs top mount | Voice-clip script; generate clips; report template + Claude | Session screen with gauge and voice | Real distances appear on screen |
| 3 | Fit the sensor; calibrate; build the mL table; stream over USB | Data-collection script with live graph and label keys | Home checklist and progress charts | A breath shows as mL on the laptop |
| 4 | **Morning, everyone:** collect and label 300+ breaths. **Afternoon:** state machine on the chip | Features, training, leave-one-person-out test | Nurse dashboard list page | Accuracy number known |
| 5 | Bluetooth service | emlearn export; check chip vs laptop labels match | Web Bluetooth connection; live gauge from the real unit | Gauge moves with a real breath |
| 6 | Model on the chip, beeps and lights, offline storage | Reminders (push + scheduler), missed-slot logic | Patient page, set target, live updates | Reminder ticks itself after 10 breaths |
| 7 | Solder onto perfboard, add the battery, print the final case | WhatsApp summary and missed alert | Results screen with spoken AI sentence | WhatsApp arrives on a phone |
| 8 | **Integration day, everyone:** run the full loop 5 times, fix bugs, add trend flags, measure battery and accuracy | | | Whole demo works end to end |
| 9 | Build and flash the spare unit | Q&A *(stretch)*; prepare pre-made reports as backup | Pitch deck; record the backup video | Video saved offline |
| 10 | **Everyone:** rehearse 3+ times with a timer; pack the demo kit; rest | | | Under time, no crashes |

### Crash plan (if you only have 3–4 days)
- **Keep:** live breath → mL → AI label (model on the laptop) → pre-recorded voice → nurse dashboard with fake data → WhatsApp summary (template text is fine).
- **Use the USB cable** instead of Bluetooth (Web Serial on a laptop).
- **Skip:** model on the chip, push reminders (show a mock-up), Q&A, battery.

---

## 15. Testing plan
| Test | How | Pass mark |
|---|---|---|
| Sensor steadiness | Disc still for 30 s | Readings wobble less than ±5 mm |
| Volume accuracy | 20 breaths held at printed marks | Within ±100 mL |
| Breath detection | 50 real breaths + bumping the table | 48+ detected; bumps ignored |
| AI model | Leave-one-person-out | 85%+ on unseen people; beats rule baseline |
| Chip vs laptop | Same 20 breaths both ways | Identical labels |
| Bluetooth | 10 connect/disconnect cycles; walk 5 m away | Reconnects every time |
| Offline | Phone internet off during a session, then on | Data uploads by itself |
| Reminders | Fast-clock day | Correct ticks and misses; alert after 2 misses |
| WhatsApp | Send to 2 phones | Arrives within 30 seconds |
| AI text | 30 sample days × 3 languages | Native speaker approves; no medical advice; template used when AI fails |
| Battery | Full charge, one session per hour | Lasts as long as you claim |
| Ease of use | An older relative tries it with no help | Finishes a session after 2 minutes of instructions |
| Full demo | 3-minute run, 3 times | Under time, no crashes |

---

## 16. Demo script (3 minutes)
| Time | What you do and say |
|---|---|
| 0:00–0:20 | "After surgery, patients forget their breathing exercises. A simple reminder doubles how many do them, from 28% to 58%." |
| 0:20–0:35 | Hold up the ₹300 Romsons spirometer and clip on SpiroBuddy. "It never touches the patient's breath." |
| 0:35–1:05 | Take a **fast** breath. The light turns amber, the phone says "थोड़ा धीरे…" ("slower") and the label reads *too fast*. |
| 1:05–1:40 | Take a **good** breath. The gauge reaches the target, "Hold… 3, 2, 1", beep, "बहुत बढ़िया!", score 9/10. "That label came from our own AI model, running on this ₹600 chip." |
| 1:40–2:00 | Show the phone checklist: this hour ticks itself ✅. |
| 2:00–2:30 | Show the nurse dashboard: the row updates live, a red patient stands out, then the AI summary. Press **Send**, and WhatsApp arrives on a phone the judges can see. |
| 2:30–2:50 | "The US proved this works: InSee was FDA-cleared in 2025. We built it for India: Indian spirometers, home use, your language, your family on WhatsApp." |
| 2:50–3:00 | "SpiroBuddy. Any Indian spirometer. Your language. Your family in the loop." |

**For an online (video-call) demo:**
- Use a second phone or webcam pointed at the unit.
- Combine it with your screen in OBS.
- Keep the WhatsApp phone in view.

**Backup:** a recorded video of a perfect run, saved offline on the laptop and on a USB drive.

---

## 17. Pitch deck (11 slides)
1. Title + one-line pitch
2. The problem, through one patient's story
3. India's numbers (3–30%; 9.4% / 55%; 21.7 vs 12.5 days)
4. The evidence (58% vs 28%)
5. What exists (InSee, Airalux) and the gap
6. SpiroBuddy: how it works (the diagram from section 2)
7. **Our own AI:** data, model, accuracy on unseen people, runs on the chip
8. Live demo
9. Cost and impact (unit cost and cost per patient, with the maths shown)
10. Safety, privacy and honest limits
11. Roadmap and what you'd do next (hospital pilot)

---

## 18. Answers to judge questions
| Question | Answer |
|---|---|
| "Isn't this just InSee?" | "InSee proves the idea works. It fits one US spirometer, is for hospital use and is in English. Ours fits Indian spirometers, works at home, coaches in Indian languages, checks technique with our own AI and updates families on WhatsApp." |
| "How accurate is it?" | "We calibrate against the spirometer's own printed marks. In our tests it was within ±X mL. It's an exercise coach, not a diagnostic test." |
| "Why AI and not simple rules?" | "We tested both. On people it had never seen, our model scored X% and the rules scored Y%. It learns combinations, like a jerky rise with a short hold." |
| "Does it need internet?" | "No. The unit counts, beeps and stores breaths, and the voice clips are on the phone. Everything uploads later." |
| "What about iPhones, or no smartphone?" | "The unit works alone with beeps and lights, and the family gets WhatsApp. Native apps and voice-call reminders for basic phones are next." |
| "Is the AI safe?" | "It only coaches and summarises. Warning words go straight to a fixed 'call your nurse' message. Alerts come from rules a nurse agreed to." |
| "Privacy?" | "Minimum data, consent in the patient's language, shared only with people they choose. We follow the DPDP Act principles, and the demo uses fake patients." |
| "Regulation?" | "Today it's an exercise coach. Before launch we'd get an official ruling through CDSCO's classification portal." |
| "Hygiene?" | "The laser is outside the breathing path. The spirometer stays with one patient; the unit is wiped and reused." |
| "Who pays?" | "Hospitals lend units at discharge and reuse them. See the cost per patient on slide 9." |
| "Battery life?" | "We measured X days per charge." |
| "Did you talk to a nurse?" | Use your real quote. |

---

## 19. Costs and business model

### Unit cost
- **Hand-built prototype:** about ₹1,400–2,600 in parts at retail prices.
- **Mass production:** we *aim* for under ₹1,000 with a custom circuit board and bulk parts. **This is an estimate, not a quote.**

### Cost per patient: example maths (replace with your real numbers)
| Item | Assumption | Per patient (2-week recovery) |
|---|---|---|
| Unit | ₹2,000, reused for 20 patients | ₹100 |
| AI feedback + reports | ~14 sessions a day + 2 reports a day | ~₹200 on Opus 5.5, or ~₹5 on Haiku 5.5 |
| WhatsApp | 2 messages a day | Check Meta's current India prices |
| **Total** | | **about ₹105–300 + messaging** |

To cut costs, use template text for the after-session sentences and keep the AI for evening reports only.

### Who could pay
1. **Hospitals:** lend units at discharge, take them back, clean and reuse them. This could be part of the surgery package.
2. **Insurers or government schemes:** later, once a hospital pilot shows fewer complications.
3. **Families of patients with long-term lung disease (COPD):** monthly rental.

---

## 20. Risks and backups
| Risk | Backup plan |
|---|---|
| Laser readings jump through plastic | Base mount with a clear path, foam ring, crosstalk calibration, or the VL53L0X |
| Disc gets closer than 4 cm to the sensor | Raise the sensor on a spacer |
| 3D print doesn't fit | Fit-test rings first; Velcro strap |
| Bluetooth fails at the venue | USB cable to the laptop (Web Serial), or Wi-Fi |
| Internet fails | Voice clips work offline; template text; backup video |
| AI service slow or down | Template text; reports generated before the demo |
| WhatsApp sandbox expired | Re-join that morning; keep a screenshot as backup |
| Model accuracy too low | More data, fewer breath types, rule backup; still show your honest number |
| Board damaged | A spare unit with the final code already loaded |
| Battery flat | Charge the night before; USB power bank |
| Volunteer feels dizzy | Sit down, rest between sets, stop |
| Judges raise InSee | The comparison slide is ready |

---

## 21. Future roadmap
1. **Hospital pilot:** 30–50 patients, with ethics approval, comparing adherence with normal care.
2. **More spirometer models**, using adapter rings.
3. **Native Android and iPhone apps**, so Bluetooth and reminders work in the background.
4. **Voice-call reminders (IVR)** for basic phones, to reach patients without smartphones.
5. **Link with India's digital health records** (Ayushman Bharat Digital Mission).
6. **CDSCO classification** and a quality system.
7. **A custom circuit board** to bring the unit under ₹1,000.

---

## 22. Checklists

### Today
- [ ] Confirm the hackathon's name, deadline and judging rules; register
- [ ] Order the parts in section 3; buy one spirometer locally
- [ ] Create accounts: Anthropic, Sarvam, Twilio, GitHub, Vercel or Netlify, Cloudflare
- [ ] Create the GitHub repository with the folder layout in 9.6
- [ ] Book a 10-minute call with a nurse or physiotherapist

### Before the event
- [ ] Every test in section 15 passed (write down the real numbers)
- [ ] Pitch deck uses only sourced numbers
- [ ] Backup video recorded and saved offline
- [ ] Spare unit loaded with the final code
- [ ] Demo data loaded; WhatsApp sandbox re-joined; API keys tested
- [ ] Batteries and phones charged

### Demo-day kit
- [ ] 2 spirometers, 2 SpiroBuddy units
- [ ] USB-C data cables, power bank
- [ ] Laptop + charger; Android phone (charged) + stand
- [ ] Alcohol wipes
- [ ] Backup video on the laptop and a USB drive
- [ ] One-page printed summary for the judges

---

## 23. Words used in this plan
| Word | Meaning |
|---|---|
| Incentive spirometer | Breathing-exercise device where a disc or ball rises as you breathe in |
| Volumetric (piston) spirometer | A type whose disc height shows the volume breathed in, in mL |
| Adherence | How often patients actually do the prescribed exercise |
| ESP32 / XIAO ESP32-C3 | A tiny, cheap computer chip with Bluetooth and Wi-Fi / a thumb-sized board using it |
| Laser distance sensor (time-of-flight) | Measures distance by timing how long light takes to bounce back |
| Field of view | How wide a cone the sensor "sees" |
| Crosstalk | False readings caused by light bouncing off plastic in front of the sensor |
| Calibration | Matching sensor readings to known true values |
| Interpolation | Estimating values between two known points with a straight line |
| Firmware | The program running on the unit's chip |
| I²C | A simple two-wire connection between the chip and the sensor |
| State machine | A program that moves through fixed stages (waiting → breathing in → holding → falling) |
| BLE / Web Bluetooth | Low-power Bluetooth / using Bluetooth directly from a web page in Chrome |
| Web Serial | Talking to a device over a USB cable from a web page in Chrome |
| PWA | A website that installs and works like an app, even offline |
| Service worker | A background helper that lets a web app work offline and receive notifications |
| Backend / server | The computer program that stores data and sends messages |
| API / endpoint | A defined way for programs to talk to each other / one specific address for that |
| LLM | A large language model, an AI that reads and writes text (e.g. Claude) |
| Text-to-speech | Turning written text into spoken audio |
| Random forest | A machine-learning model made of many small decision trees that vote |
| Features | The numbers that describe each breath, used by the model |
| Leave-one-person-out | Testing the model on a person it never trained on |
| Confusion matrix | A table showing what the model got right and what it mixed up |
| emlearn | A tool that turns a Python model into C code for small chips |
| Web push | Notifications sent from a server to a phone's browser |
| Sandbox | A free test version of a service (here, Twilio's WhatsApp) |
| Cloudflare Tunnel | A free way to give a laptop server a secure public web address |
| DPDP Act | India's Digital Personal Data Protection Act, 2023 |
| CDSCO | India's medical device regulator |

---

## 24. Sources

**Research** (full details in SpiroBuddy_Final_Research.md):
- Eltorai et al., *JAMA Surgery* 2019 (58% vs 28%): https://jamanetwork.com/journals/jamasurgery/article-abstract/2730077
- InSee FDA clearance letter, Aug 2025: https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241152.pdf
- Penn Airalux trial: https://clinicaltrials.gov/study/NCT06629454
- Indian studies of lung complications after surgery: https://www.ijsurgery.com/index.php/isj/article/view/3176 (Udaipur numbers, Int Surg J 2018;5:3057–65; corrected link) · https://doaj.org/article/8ce7474ddd114cdbb332bb5c0d16b782
- Romsons Breazer listing: https://www.medikabazaar.com/products/romsons-breazer-2500-volumetric-lung-exerciser-mbpgmrsmmssrre15739
- ST VL53L1X manual (field of view): https://st.com/resource/en/user_manual/um2555-vl53l1x-ultra-lite-driver-multiple-zone-implementation-stmicroelectronics.pdf
- ST cover-window guide (crosstalk): https://www.st.com/resource/en/application_note/an5231-cover-glass-guidelines-for-the-singlezone-timeofflight-sensor-stmicroelectronics.pdf
- CDSCO software guidance (2026): https://www.emergobyul.com/news/india-cdsco-finalizes-guidance-medical-device-software
- Hack for a Social Cause 2026: https://mybharat.gov.in/pages/hack_social

**Tool documentation:**
- Seeed XIAO ESP32-C3: https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/
- SparkFun VL53L1X library: https://github.com/sparkfun/SparkFun_VL53L1X_Arduino_Library
- NimBLE-Arduino: https://github.com/h2zero/NimBLE-Arduino
- emlearn: https://github.com/emlearn/emlearn
- Web Bluetooth (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API
- vite-plugin-pwa: https://vite-pwa-org.netlify.app/
- Sarvam text-to-speech: https://docs.sarvam.ai/api-reference-docs/text-to-speech/api/overview
- Twilio WhatsApp sandbox: https://www.twilio.com/docs/whatsapp/sandbox
- Claude API: https://docs.anthropic.com

*All prices and costs are estimates as of October 2026. Check them before buying or quoting them to judges.*
