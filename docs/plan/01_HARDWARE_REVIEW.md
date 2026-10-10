# 01 – Hardware review: is this the best, smallest, toughest unit we can build now?

**Written:** 10 Oct 2026 · **Sources opened this round:** 23 read + 3 that failed (table at the end) · **Confidence overall:** medium on parts and prices, **low on anything that depends on the real spirometer's size** (nobody has measured one yet)
**Answers founder notes 3, 9, 10, 11, 12** (`docs/plan/00_FOUNDER_NOTES.md`).
**How to read the labels:** CONFIRMED = a primary source (datasheet, standard, study) or two independent sources · SINGLE SOURCE · NOT CONFIRMED · **(est.)** = our own arithmetic or reasoning, shown so you can check it · **(snippet)** = seen in a search result only, page not opened · `[#n]` = row in `docs/research/SOURCES_LEDGER.md`, reused without re-opening · `[H n]` = source opened this round.
**Prices** are single-unit listings on Evelta (Mumbai) on 10 Oct 2026, **before 18% GST**, unless stated. They are shop prices, not quotes.

---

## Answer in 12 lines

1. **The sensing method is right. Keep it.** A laser distance sensor under the spirometer, looking up at the piston, needs no change to the spirometer, never touches the air the patient breathes, and is the layout the FDA-cleared InSee uses [#102, #103]. Every alternative we checked is worse on at least one of: accuracy, hygiene, or "works without modifying the spirometer".
2. **The exact sensor chip is not settled. Test two.** The current VL53L1X cannot read closer than 40 mm, and that single fact is why our base is 46 mm tall. Its sister chip **VL53L4CD reads from 1 mm**, is more accurate out of the box (±7–8 mm against ±20–25 mm) and has a built-in 55 µA "watch and wake" mode [H1]. It could make the base roughly half as tall. But its beam is slightly wider (18° fixed) and **we found no Indian shop selling it today**.
3. **The biggest risk is still unmeasured plastic, not electronics.** Nobody knows whether the floor under the Breazer's piston is open (`3D_SOURCES.md:28`, B26). The beam is about 43 mm wide at the top of travel against a tube bore of about 44 mm, both derived from a drawing (`RESEARCH_REPORT.md:260`). **Buy two spirometers and a caliper before any more electronics decisions.**
4. **Change the main board for the battery unit.** The ESP32-C3 cannot stay "listening" on Bluetooth while asleep; a third-party test shows about 9.7 mA with Bluetooth alive (snippet), which empties a 500 mAh cell in about two days (est.). The **nRF52840** idles at about 1.5 µA and advertises for about 16 µA (snippets of the Nordic specification and forum). Same tiny board size (XIAO, 21 × 17.8 mm), ₹1,030 against ₹620 [H10].
5. **"How do we detect the device is on?" The unit tells the phone, about once a second, for almost no power.** It never truly switches off. It sleeps and sends a tiny radio "I'm here" message that also carries battery level and whether the spirometer is on the base. The app shows "ready" when it hears the message and "can't find your unit" when it has not heard one for a few seconds. Full answer in H-3.
6. **No on/off switch for the patient.** One big button, a light and a beep. The unit wakes when picked up or when the button is pressed, and sleeps by itself. A hidden "shipping mode" turns it fully off for storage.
7. **Battery: keep a rechargeable lithium pouch cell, but make it about 1,000–1,200 mAh, not 500.** Our arithmetic gives about 18 days on 500 mAh with the nRF52840 design, with thin margin once the cell ages. InSee uses 1,200 mAh [#101 group].
8. **Feedback: light + beeper for the pilot (the phone speaks). Add a speaker and stored voice only for the no-phone version.** All 11 languages fit in a 16 MB memory chip if the clips are compressed (est.).
9. **PLA plastic is for the demo only.** Print the pilot units in PETG, wipe-test them with 70% alcohol, and design to survive a 1 m drop and dripping water (the IEC 60601 figures for hand-held and home-use devices) [H4, H8].
10. **The ₹1,000–1,700 parts estimate holds only for a no-battery cable prototype (₹1,365 before GST, sourced). A real pilot unit is about ₹2,300–2,500 before GST.** A 1,000-unit price cannot be honestly totalled without four quotes (sensor chip, battery, circuit board, moulded case).
11. **The technology most likely to make the base unit unnecessary is a phone camera reading the scale.** A 2025 paper did it with a tablet and a stand, but tested it only on simulated patients [H3]. It is an opportunity as much as a threat: our value is the coaching, the dashboard and the family link, so the app must accept breaths from **any** source.
12. **Design rules that protect the team:** sensor on its own small plug-in board; nothing personal stored in the unit; one stable message format between unit and app (distance + status), versioned; per-model calibration tables kept on the server; firmware updatable over Bluetooth from day one.

---

## Verdict per part (one table)

| Part / choice | Today (file:line) | Verdict | What to do |
|---|---|---|---|
| Sensing method: laser distance sensor under the piston | `HARDWARE.md:185`, `3D_SOURCES.md:145` | **KEEP** | Prove it on a real Breazer first (H-11) |
| Sensor chip: VL53L1X | `HARDWARE.md:17`, `spirobuddy_serial.ino:22` | **TEST BOTH** | VL53L1X (in stock in India) against VL53L4CD / L4CX family |
| Narrowest view setting (ROI 4×4) | `spirobuddy_serial.ino:29`, `HARDWARE.md:194` | **KEEP** | Also try 8×8 if signal is weak |
| Main board: XIAO ESP32-C3 | `HARDWARE.md:16`, `showcase.js:51` | **CHANGE for battery units; keep for the USB demo** | XIAO nRF52840 for the pilot |
| On/off | nothing exists (`00_FOUNDER_NOTES.md:15-16`) | **ADD** | Always-asleep design, button + motion wake, status in the Bluetooth "I'm here" message |
| Motion sensor (accelerometer) | not in design | **ADD** | LIS3DH, ₹59 chip / ₹225 board |
| Battery: 500 mAh LiPo | `showcase.js:57`, `3D_SOURCES.md:122` | **CHANGE size** | 1,000–1,200 mAh pouch with protection circuit and BIS mark |
| Charging: via the XIAO board | `3D_SOURCES.md:116` | **KEEP for pilot** | Own charger + protection chips on the 1,000-unit board |
| Battery gauge | none | **ADD (cheap way)** | Measure battery voltage with the chip; a gauge chip (₹507) is not worth it |
| Light: WS2812B colour LED | `showcase.js:59` | **TEST** | It draws power even when dark; compare with 2–3 plain LEDs behind icons |
| Sound: piezo beeper | `HARDWARE.md:20` (optional today) | **KEEP, make it standard** | Speaker only for the no-phone version |
| Display | none | **KEEP OUT** | Adds cost, a window to seal and scratch; the phone is the screen |
| Start button | `showcase.js:60` | **KEEP, make it large and sealed** | One button only |
| Case: 46 mm tall tray, 3D print | `3D_SOURCES.md:136`, `showcase.js:66-67` | **CHANGE** | Thinner (target about 25–35 mm, est.), PETG now, moulded PC blend at scale |
| Sensor window | open hole + foam ring (`3D_SOURCES.md:140-141`) | **CHANGE** | Sealed, recessed infrared window; run the sensor's own cross-talk calibration |
| USB-C | open cut-out (`3D_SOURCES.md:142`) | **KEEP, protect it** | Recess it, add a tethered rubber plug |
| Fit: Breazer 2500 only | `HARDWARE.md:15` | **KEEP for the pilot** | Removable per-model insert later |
| Calibration: table from printed marks | `HARDWARE.md:198-209` | **KEEP** | Add a per-unit offset step and store tables on the server |

---

## Step 1 – What exists today, stated exactly

| Fact | Where |
|---|---|
| The parts list is: a volumetric spirometer (Breazer 2500), one board (XIAO ESP32-C3 first choice, or ESP32 DevKit, or Arduino Uno/Nano), one sensor (VL53L1X first choice, VL53L0X backup), a data USB cable, jumper wires, an **optional** piezo buzzer, black foam, tape or a clip | `docs/HARDWARE.md:15-22` |
| The XIAO C3 has no status light; the antenna is "not needed for USB" | `docs/HARDWARE.md:56` |
| Rules: keep at least 5 cm from sensor to disc; the sensor must not move ("even 2 mm of wobble shows up as volume"); never change the air path | `docs/HARDWARE.md:181-183` |
| Base mount (sensor looks up) is "try first"; top mount risks cross-talk through the lid | `docs/HARDWARE.md:185-190` |
| The sketch narrows the view to the smallest window, 4×4, about 15° | `docs/HARDWARE.md:194`; `firmware/spirobuddy_serial/spirobuddy_serial.ino:29-30, 136-137` |
| Short-distance mode, 33 ms per reading, about 30 readings a second | `spirobuddy_serial.ino:87, 134-138` |
| Output is text over USB only: `D,<ms>,<mm>`; commands `B` (beep) and `I` (status) | `spirobuddy_serial.ino:5-12, 171-176, 210-218` |
| **There is no Bluetooth, no sleep, no battery reading, no button and no identity in the firmware.** One beep at power-on is the only "I am on" signal | `spirobuddy_serial.ino:262` and the whole sketch |
| The sketch has never been compiled or run on a board | `docs/HARDWARE.md:235` |
| "Target: within ±100 mL" is a target, not a result | `docs/HARDWARE.md:207` |
| The modelled base unit: XIAO ESP32-C3 (21 × 17.8 × about 5 mm), VL53L1X on a Pololu board (13 × 18 × 2 mm), 500 mAh LiPo (36 × 29 × 4.75 mm), piezo (Ø 11.9 × 6.5 mm), WS2812B light, 6 mm button | `web/showcase/showcase.js:50-61` |
| The modelled case: 181.5 × 89 mm footprint, tray 34 + lid 12 = **46 mm tall**, 2 mm walls, 8 mm pocket, 20 mm light tunnel, 4 air slots a side, USB cut-out | `web/showcase/showcase.js:63-76`; `docs/3D_SOURCES.md:134-144` |
| Sensor to piston: **51.5 mm at rest, 162.9 mm at 2,500 mL**. Beam spot 13.6 mm at rest, **42.9 mm at the top**; bore about 44.2 mm; piston 40.5 mm | `docs/3D_SOURCES.md:138-139` |
| "That margin is thin and rests on derived sizes" | `docs/research/RESEARCH_REPORT.md:260`; also `:669` ("Measure it") |
| No published test of this sensor inside an incentive spirometer exists | `docs/research/RESEARCH_REPORT.md:246, 626` |
| Parts cost estimates: ₹1,000–1,700 (knowledge base) and ₹1,400–2,600 (plan); both the team's own | `docs/research/RESEARCH_REPORT.md:266-270` |
| Connection plan: Bluetooth to a phone for the pilot; built-in 4G and a speaker at scale; battery life "not measured; no hardware yet" | `docs/DEVICE_LIFECYCLE.md:17-18, 88-89, 334` |

### Every dimension flagged "measure with caliper"
All from `docs/3D_SOURCES.md`. **Bold = the hardware design depends on it.**

| ID | What | Model value | Flag |
|---|---|---|---|
| **B26** | **Is the floor under the piston open? Hole size?** | unknown | NOT PUBLISHED – "the single most important check" (line 28) |
| **B02** | **Total height incl. cap** | 200 mm | DERIVED, LOW – every other B size scales with it (line 20) |
| **B04 / B05 / B06** | **Base width / height / depth** | 172.5 / 28.0 / 80 mm | DERIVED – sets our pocket |
| B06b | Air arches in the base | 30 × 8 mm | DERIVED, LOW – our air slots must not block them |
| **B09** | **Volume tube outer diameter and position** | 47.2 mm at 106.8 mm | DERIVED – where the sensor sits |
| **B10** | **Wall thickness of the clear tubes** | 1.5 / 2 mm | NOT PUBLISHED – placeholder. Sets the real bore |
| **B11 / B12** | **Chamber bottom, seat, piston size and resting height** | 14.7 / 21.3 mm; piston 40.5 × 30.7 mm | DERIVED – sets sensor distance and beam margin |
| **B14** | **Height of the 250 mL and 2,500 mL marks** | 61.9 and 162.2 mm (11.14 mm per 250 mL) | DERIVED – the calibration scale |
| B03, B07, B08 | Overall width, cap thickness, cap lobes | 177.1; 17.3; 65.3 / 61.3 mm | DERIVED |
| B15–B19, B19b, B21, B22 | Flow tube, float, emoji boxes, connector, handle, hose, mouthpiece | see file | DERIVED or NOT PUBLISHED (cosmetic for hardware) |
| E02 / E03 | XIAO thickness and USB-C shell | about 5 mm; 8.9 × 3.2 × 7.3 mm | NOT PUBLISHED – placeholders |
| E08 | Sensor board, if not the Pololu one | 13 × 18 mm | measure if a different board is bought (the 7Semi and probots boards are different sizes) |

---

## Findings

### H-1: The sensing method. Laser time-of-flight from below is still the best choice; the chip inside it should be re-chosen on the bench

**What it is for:** knowing where the piston is, about 30 times a second, so software can work out volume, speed and hold.

**The geometry that decides everything (est., from `3D_SOURCES.md` rows B11–B14):**
- The piston's underside rests about 50.8 − 30.7 = **20.1 mm** above the spirometer's own floor.
- It travels 10 × 11.14 = **111.4 mm** from 0 to 2,500 mL. So **1 mm of travel ≈ 22.4 mL**.
- A beam with a full angle of A spreads to a spot of 2 × distance × tan(A/2).
- All of this rests on a drawing scaled from one retailer figure. Treat it as a guide until a caliper says otherwise.

**Datasheet comparison of distance sensors**

| Sensor | Range (datasheet) | Out-of-box accuracy | View angle | Spot at top of travel (est.) | Low-power "watch and wake" | Price / where in India | Status |
|---|---|---|---|---|---|---|---|
| **VL53L1X** (current) | 40 mm to about 1.3 m in short mode [#118] | ±20 mm dark, ±25 mm room light [#118] | 27°, software-narrowed to about 15° [#118, #149 snippet] | 42.9 mm with the sensor 51.5 mm below the piston (as modelled); **39.9 mm** if moved up to the 40 mm minimum | Yes: separate ST driver, 65 µA at one reading a second (snippet of ST page) | 7Semi board ₹745, 144 in stock [H11]; probots ₹677 + GST, out of stock [H5] | CONFIRMED (range, accuracy); SINGLE SOURCE (15°) |
| **VL53L4CD** (candidate) | **1 mm** to 1,200 mm; white target indoors 1,200 mm, grey 17% target 450 mm [H1] | **±7 mm at 1–100 mm, ±8 mm at 101–200 mm** indoors; ±8–9 mm outdoors overcast [H1] | **18° diagonal, fixed** [H1] | about **43 mm** with the sensor 25 mm below the piston (est.) | **Yes, built in: down to 55 µA**, raises an interrupt when a target crosses a threshold [H1] | **Not found** at Evelta or ThinkRobotics [H7, H22]. Import needed | CONFIRMED (datasheet DS13812 Rev 8, July 2024) |
| VL53L4CX | Same family, longer range, can report more than one target (not opened this round) | not opened | not opened | – | not opened | Adafruit board ₹1,759 [H7, H11] | NOT CONFIRMED – read its datasheet before buying |
| VL53L0X (backup today) | older part | not opened this round | about 25° fixed (`HARDWARE.md:194`) | about 66 mm at 150 mm: **wider than the tube** (est.) | – | Grove board ₹693 [H12] | Too wide. **Drop it as a backup** |
| VL6180X | about 0–100 mm class part (not opened) | – | – | – | – | SparkFun board ₹1,339 [H16] | Too short: we need about 20–135 mm at least |
| VL53L5CX / L8CX (8 × 8 zones) | 20 mm to 4 m (snippet) | not opened | 45° square split into 64 zones, so each zone is about 5.6° (est.) | middle four zones ≈ 11°: about **26 mm** (est.), the narrowest of all | autonomous mode exists; one user could not get below 25 mA (forum, snippet) | none found in India this round | Interesting, but 216–313 mW when running (ST staff on forum, snippet) and only 15 readings a second in 8 × 8 mode. **Watch, do not buy first** |
| TMF8806 (ams OSRAM) | 10 mm to 5 m or 10 m depending on datasheet version (snippet) | not found | not found | – | "ultra low power mode" (snippet) | not found in India | NOT CONFIRMED. No reason to prefer it yet |

**What this means**
- The **40 mm minimum of the VL53L1X plus the team's 50 mm rule is what makes the base 46 mm tall** (`3D_SOURCES.md:136-138`). The VL53L4CD removes that limit.
- Moving the sensor **closer** to the piston makes the spot at the top of travel **smaller**, because the top is then nearer too. That helps the thin beam margin whichever chip is used.
- On paper the two chips end up with a similar spot (about 40–43 mm) against a piston of about 40.5 mm and a bore of about 44 mm. **Paper cannot settle this. The bench must.**
- The VL53L4CD's better starting accuracy matters: ±7 mm is about ±157 mL before calibration; ±20 mm is about ±450 mL (est., using 22.4 mL per mm). Calibration removes most of this in both cases, but a smaller starting error means less unit-to-unit work.

**Other ways to sense the piston, compared honestly**

| Method | Evidence found | Works without modifying the spirometer? | Touches the breathing air? | Verdict |
|---|---|---|---|---|
| **Row of infrared reflective sensors beside the tube** | A US team used 10 along the volume tube (one per 500 mL) and 3 on the flow tube, an ESP32, a 2,400 mAh cell; 99% of piston readings at the correct sensor; volume within 7.5%; about US$150 in parts; sensors did not line up on a second spirometer model [H2] – CONFIRMED (peer-reviewed) | Yes | No | **Reject as the main sensor.** Only as fine as the sensor spacing (500 mL steps there), so it cannot measure speed well, and it is tied to one model's scale |
| **Phone or tablet camera reading the scale** | Tablet camera + image processing tracked the indicator in more than 95% of frames, 28 ms a frame, **250 simulated scenarios, no real patients**; needs a stand; authors list low light, glare, blur and model differences as limits [H3] – SINGLE SOURCE | Yes | No | **Not for the pilot; build the door for it.** See H-10 |
| ESP32 camera inside the unit | no study found | Yes | No | Reject: more power, a lens to keep clean, lighting needed, no accuracy evidence |
| **Ultrasound** | InSee's patent lists a sound-based option [#86]; no accuracy study found | Only if the path under the piston is open air | No | Reject for now: cheap ultrasonic parts have wide beams and echo off tube walls (reasoning, not sourced) |
| **Hall-effect sensor + magnet on the piston** | none found | **No** – a magnet must be fixed to the piston | No, but it adds weight to the moving part | **Reject.** It changes the device the patient was given and breaks our "never modify" rule (`HARDWARE.md:183`) |
| Capacitive strip along the tube | none found | Yes | No | Reject: no evidence; hands near the tube would disturb it (reasoning) |
| Row of light gates across the tube | same idea as the reflective row [H2] | Yes | No | Same limit: steps, not a smooth reading |
| **Pressure or flow sensor in the hose** | none opened this round | **No** – it sits in the air path | **Yes** | **Reject, firmly.** Anything in the air path must be cleaned or replaced between patients, can change breathing resistance, and makes us a measuring device in the patient's airway. Our reading: this would move us towards a higher device class and far more testing. Confirm with a regulatory consultant |
| Microphone listening to airflow | none found | Yes | No | Reject: no evidence it gives volume; room noise |
| 60 GHz radar | Chip makers claim "sub-millimetre movement" detection, but the range step is about 3 cm; no published accuracy through plastic for our kind of use (snippets) | Yes | No | Watch only (H-10) |

**Behaviour near clear plastic and light (what we know)**
- Light passing through clear plastic causes false short readings, called cross-talk [#14]. Inside a tube, wall echoes make the sensor under-read; the fixes are the narrowest view, dull dark walls and a clear target [#136, forum incl. ST staff].
- The VL53L4CD datasheet says a cover window is allowed but then "crosstalk calibration is also needed" [H1].
- Bright daylight shortens range: the VL53L4CD's reach on a grey target drops from 450 mm to 400 mm outdoors overcast [H1]. We need about 135–165 mm, so there is headroom. **Direct sun through a window onto a clear tube is untested.**
- The laser is invisible 940 nm light, Class 1 (eye-safe) [H1, #118].

**Must be bench-tested before anything is ordered in quantity:** (1) is the floor open (B26); (2) does either chip read the piston smoothly over the full travel; (3) how much the reading wanders with the piston held still; (4) sunlight; (5) the blue seat's effect.

- **Status:** method CONFIRMED as workable on another spirometer (InSee, [#102, #103]); **NOT CONFIRMED on the Breazer**.
- **Verdict:** KEEP the method. TEST VL53L1X against the VL53L4CD family. DROP the VL53L0X as a backup.

---

### H-2: Microcontroller and radio. ESP32-C3 for the cable demo; nRF52840 for anything on a battery

**What it is for:** the small computer that reads the sensor, runs the Bluetooth link and controls sleep.

**Why this matters now:** the founder wants the app to connect "automatically, every time Bluetooth is on". That needs the unit to be reachable all day. So the question is: **how much power does the chip use while doing nothing but staying reachable?**

| Chip / board | Sleep and radio figures found | Price in India (ex GST) | Tools and community | Verdict |
|---|---|---|---|---|
| **ESP32-C3** (XIAO ESP32-C3, current) | Chip deep sleep 5 µA, light sleep about 130 µA (Espressif datasheet and guide, **snippet**). On the XIAO board a third-party test measured **44 µA deep sleep, 9.7 mA light sleep with Bluetooth on, 26.8 mA modem-sleep with Bluetooth on** (snippet). In deep sleep the radio is off, so it cannot be found | XIAO ESP32-C3 ₹620; bare module ESP32-C3-WROOM-02 ₹265 [H10, H17] | Excellent; our sketch already targets it. Secure boot and encrypted storage documented [#201] | **Keep for USB prototype. Not for an always-reachable battery unit** |
| ESP32-C6 | not opened this round | module ESP32-C6-MINI-1 ₹285, 271 in stock [H17] | Newer; adds Wi-Fi 6 and Thread/Zigbee, which we do not need | No reason to switch to it |
| ESP32-H2 | not found in India this round | – | Bluetooth-only Espressif chip | NOT CONFIRMED; skip |
| ESP32-S3 | not opened | XIAO ESP32-S3 ₹900 [H10] | Most audio libraries target it | Only relevant for the speaker version (H-5) |
| **nRF52840** (XIAO nRF52840) | **System OFF 0.4 µA; sleeping with a wake-up clock 1.5 µA; radio peaks 4.8 mA sending, 4.6 mA receiving** (Nordic specification v1.8, **snippet**). Board standby "less than 5 µA" [H15]. Advertising once a second measured at about 14–16 µA average on Nordic's forum (snippet) | **XIAO nRF52840 ₹1,030**, 4 in stock; IndieSemiC nRF52840 module ₹539; bare chip ₹357 [H10, H18] | Good. Arduino, MicroPython, CircuitPython on the XIAO [H15]; Nordic's own toolkit is harder to learn. Built-in battery charger chip (BQ25101, 50 or 100 mA) and 2 MB extra memory on the board [H15] | **Use for the first 10 and for the pilot** |
| nRF52832 | not opened | not found | Older, smaller sibling | Skip |
| nRF54L15 | Nordic's newest; development kits exist; supports Bluetooth 6 distance-measuring (snippets) | not found in India | Young; forum reports of teething bugs (snippet) | Watch (H-10) |
| BL702 / BL616, STM32WB | ST publishes India radio approval for one STM32WB module (snippet) | not found | Smaller communities | Skip |
| RP2040 W / RP2350 | not a low-power radio chip | XIAO RP2040 ₹495; RP2350 ₹570 [H10] (these XIAO boards have no radio) | – | Skip |

**Radio approval in India (WPC "ETA")**
- Bluetooth uses a licence-free band, but equipment still needs an Equipment Type Approval from the telecom ministry's WPC wing. Module makers obtain one per module model; Espressif publishes theirs [#295].
- Law-firm and consultancy notes say a module's approval **does not automatically cover the finished product** built around it, though it is useful evidence; one quotes ₹10,000 per model for the self-declaration route (snippets, grade C).
- **Our reading:** choosing a module that already has an Indian ETA saves radio lab testing, not the paperwork. Confirm with a WPC consultant before selling. For a 10–50 unit research pilot the practical risk is low, but ask.
- **Status:** NOT CONFIRMED (no official text opened; `dot.gov.in` was blocked last round [#304]).

**Firmware updates and security**
- ESP32-C3: signed firmware and encrypted storage are documented [#201].
- nRF52840: signed over-the-air updates are standard in Nordic's toolkit (not opened this round – NOT CONFIRMED here). The Arduino route on the XIAO is quicker to start but weaker on this point. **Plan to move to Nordic's toolkit before the pilot ships.**

**Which for 10 units, which for 1,000**
- **First 10:** XIAO nRF52840 (drop-in for the XIAO C3's footprint). Buy one XIAO ESP32-C3 too, because today's sketch runs on it unchanged.
- **1,000:** our own circuit board with a pre-approved nRF52840-class module, **or**, if the no-phone 4G unit goes ahead, a cellular module becomes the main part and this choice is reopened. Do not design the 1,000-unit board until the pilot shows which link patients actually use.
- **Verdict:** CHANGE for battery units; KEEP ESP32-C3 for the cable demo.

---

### H-3: Power, and "is the unit on?" (the founder's direct question)

#### The main point
**The unit never fully switches off. It dozes, and about once a second it sends a tiny radio message saying "I'm here, battery 80%, spirometer on base". The phone listens for that message. Hearing it means "on and nearby". Silence means "off, flat, or too far".**

#### An everyday comparison
A lighthouse. It does not know whether any ship is watching. It just flashes on a schedule, and the pattern of flashes says which lighthouse it is. A ship that sees the flash knows the lighthouse is working and roughly where it is. A ship that sees nothing cannot tell whether the lamp is broken or simply over the horizon.

| Lighthouse | SpiroBuddy |
|---|---|
| The flash | An "advertising" packet (**advertising** = a short radio broadcast a Bluetooth gadget repeats so phones can find it) |
| The flash pattern | The unit's serial number plus a few status bytes |
| A ship seeing the flash | The app marks the unit "ready" |
| A ship sailing in to dock | The app connects and starts receiving live readings |
| No flash seen | "Can't find your unit" |

#### How it really works
1. **Asleep (nearly all day).** The chip sleeps at a few millionths of an amp and wakes for about 1–5 thousandths of a second each second to broadcast. Cost: about 16 µA on an nRF52-class chip (forum measurement, snippet).
2. **The broadcast carries status.** Unit ID, battery percent, charging yes/no, "spirometer seated" yes/no, firmware version, a fault flag. About 10 bytes. The app reads this **without connecting**.
3. **Waking up fully.** Any of: the patient presses the button; the unit is picked up or nudged (a motion chip raises a signal); the phone connects; or the laser sensor, in its low-power watch mode, sees the piston leave its rest position.
4. **Awake.** The laser sensor runs, the light glows, readings stream to the phone 30 times a second.
5. **Back to sleep.** 60 seconds after the last breath, or when the phone disconnects.
6. **The server's view.** The phone passes on "last heard from unit SB-0007 at 10:42, battery 64%". The nurse dashboard shows "seen 2 h ago", as `DEVICE_LIFECYCLE.md:203-204` already plans.

#### Where the comparison breaks
- A lighthouse cannot be asked a question. Our unit can: once the phone connects, it can ask for stored breaths and send commands.
- Silence is ambiguous for the app, exactly as for the ship. **So the unit itself must show its state** with a light, because the phone cannot tell "flat battery" from "in another room".
- A web page cannot listen in the background. Today's patient app is a web page; `DEVICE_LIFECYCLE.md:108` already notes this. Automatic connection with the screen off needs the Android app the founder asked for (founder note 1). That is the app team's file, not this one, but the hardware supports it either way.

#### Ways to turn on and off, compared

| Option | Standing power cost | Good | Bad | Verdict |
|---|---|---|---|---|
| **Slide switch (hard on/off)** | Zero when off | Simple; true zero drain | Elderly patients forget it both ways; the app can never tell "switched off" from "broken"; a slot to seal against wipes; a part that breaks | **Reject for patients.** Keep a hidden version as "shipping mode" |
| **Push button with a latch circuit** | About zero when off | One button | Same "is it off or broken?" problem; extra parts | Reject |
| **Always asleep, wake on button** | 0.4–5 µA chip sleep (nRF52840 spec snippet; XIAO board [H15]) | Nothing to forget | Needs a press every session | Part of the answer |
| **Wake on motion** (LIS3DH / LIS2DH12 motion chip) | "down to 2 µA" headline for LIS2DH12 (ST product page, **snippet**; exact wake-mode current not opened) | Picks up, nudges and taps wake it; also tells us "being carried" or "dropped" | A nearby door slam could wake it briefly (harmless) | **Add.** LIS3DH chip ₹59, 7Semi board ₹225 [H20] |
| **Wake when the spirometer is seated** (reed switch + magnet, micro-switch, pressure pad) | Zero for a reed switch | Tells us "on its base" directly | A reed needs a magnet glued to the spirometer: that modifies it. A micro-switch is a moving part and a gap to clean | **Reject the magnet. Use the laser itself**: a seated spirometer returns a piston distance inside a known window; an empty base returns "nothing" or the ceiling |
| **Wake when the piston moves** (laser sensor's low-power watch mode) | **55 µA** on VL53L4CD [H1]; 65 µA at 1 reading a second on VL53L1X (snippet) | The patient just breathes; no button at all | It checks about once a second, so the first second of the first breath may be missed; ST's own forum says the threshold "window" behaviour needs checking on hardware (snippet) | **Test.** If it works, it is the best experience for an elderly patient |
| **Wake on a Bluetooth connection** (advertise all the time) | about 16 µA at a 1-second interval; halve the interval and the cost roughly doubles (est. from the same model) | The phone can find and wake the unit; the app always knows it is alive | Only practical on a low-power radio chip (H-2) | **Yes. This is the core of the answer** |

#### Battery-life estimate (arithmetic shown; every input labelled)

**Use assumed:** 14 sessions a day (the figure in `DEVICE_LIFECYCLE.md:334`) × 3 minutes awake each = **0.7 h awake a day**. Usable battery = 80% of the label (assumption, to allow for ageing and cut-off).

| Input | Value | Source |
|---|---|---|
| Laser sensor, ranging | 22 mA typical | VL53L4CD datasheet Table 14 [H1] (VL53L1X assumed similar) |
| Laser sensor, hardware standby | 5 µA | [H1] |
| Laser sensor, low-power watch mode | 55 µA | [H1] |
| XIAO ESP32-C3 with Bluetooth active | 26.8 mA | third-party board test (**snippet**) |
| XIAO ESP32-C3 light sleep, Bluetooth alive | 9.7 mA | same (**snippet**) |
| XIAO ESP32-C3 deep sleep (radio off) | 44 µA | same (**snippet**); also on the Seeed page [#23] |
| nRF52840 awake and streaming | 3 mA | **assumption** (radio peaks are 4.6–4.8 mA for brief moments; measure it) |
| nRF52840 advertising once a second, incl. sleep | 16 µA | Nordic forum measurement (**snippet**) |
| XIAO nRF52840 board leakage | 5 µA | "less than 5 µA" [H15] |
| Motion chip | 2 µA | ST headline figure (**snippet**) |
| Light, averaged while awake | 5 mA | **assumption** |

| Design | Asleep (23.3 h) | Awake (0.7 h) | Per day | 500 mAh cell (400 usable) | 1,200 mAh cell (960 usable) |
|---|---|---|---|---|---|
| **A. ESP32-C3, always reachable** (light sleep with Bluetooth) | 9.7 mA × 23.3 h = 226 mAh | (26.8 + 22 + 5) mA × 0.7 h = 37.7 mAh | **264 mAh** | **1.5 days** | 3.6 days |
| **B. ESP32-C3, deep sleep, button to wake** (not reachable while asleep) | 0.044 mA × 23.3 h = 1.0 mAh | 37.7 mAh | **38.7 mAh** | **10 days** | 25 days |
| **C. nRF52840, always reachable, button + motion wake** | (16 + 5 + 5 + 2) µA = 0.028 mA × 23.3 h = 0.65 mAh | (3 + 22 + 5) mA × 0.7 h = 21 mAh | **21.7 mAh** | **18 days** | 44 days |
| **D. As C, plus the laser watching for the piston** | (16 + 5 + 55 + 2) µA = 0.078 mA × 23.3 h = 1.8 mAh | 21 mAh | **22.8 mAh** | **17.5 days** | 42 days |

**What the table says**
- **Time awake dominates.** In designs C and D, sleeping costs under 10% of the day's energy. The laser sensor's 22 mA is the biggest single draw. So: sleep quickly after the last breath.
- **The piston-watch mode costs almost nothing** (C to D loses half a day in 18). If it works on the bench, use it.
- **Design A is not viable. Design B meets the battery target but fails the founder's "connects automatically" wish**, because a deep-sleeping ESP32 cannot be found.
- **These are estimates. None is measured.** Experiment 3 in H-11 replaces them with real numbers.

#### How the app learns each state

| State | How the unit signals it | What the app shows |
|---|---|---|
| On and nearby | Broadcast heard in the last 5 seconds | "Unit ready" (green) |
| Off, flat or out of range | No broadcast for 10 seconds | "Can't find your unit. Is its light on? Press the big button." |
| Low battery | Battery byte in the broadcast below 20% | "Please charge the unit tonight" + the nurse sees it as a unit problem, not a missed session |
| Charging / charged | Charging flag | "Charging" / "Charged" |
| Spirometer not on the base | Laser sees no piston in the expected window | "Stand the spirometer on the unit" with a picture |
| Fault (sensor not answering) | Fault flag | "Unit needs attention. Your nurse has been told." |
| Out of range mid-session | Connection drops; the unit keeps counting breaths in memory | "Keep going, I'm still counting" then syncs later |

#### What the patient sees and hears on the unit, with no phone

| Moment | Light | Sound |
|---|---|---|
| Asleep | off | – |
| Woken (button, pick-up, or first breath) | slow white pulse | one short beep |
| Phone connected | steady blue for 2 s | two rising beeps |
| Breath in progress | fills green as the piston rises | – |
| Good breath | green flash | happy beep |
| Too fast | amber flash | low beep |
| Battery low | red blink every 10 s while awake only | one long beep at wake |
| Charging / full | amber breathing / steady green | – |
| Spirometer not seated | white blink | – |
| Fault | red steady | three beeps |

Colour must never be the only cue (some older patients cannot tell red from green): pair each colour with a position or a blink pattern.

- **Status:** design proposal; inputs are datasheet (CONFIRMED) and snippets (NOT CONFIRMED) as labelled.
- **Verdict:** ADD. Always-asleep design on an nRF52840, button + motion wake, piston-watch wake to be tested, status in the broadcast, a hidden shipping-off mode.

---

### H-4: Battery and charging

**What it is for:** 14 days at home between charges (the task's target), safely, in a device elderly people keep by the bed.

**Capacity needed (from the H-3 table):** design C or D uses about 22–23 mAh a day, so 14 days needs about **320 mAh usable**. A 500 mAh cell just covers it when new. With cold, age and a patient who does more sessions, it will not. **Choose about 1,000–1,200 mAh** (about 40 days, est.). InSee carries 1,200 mAh [#101 group]. The US research add-on used 2,400 mAh [H2].

| Option | Good | Bad | Price found | Verdict |
|---|---|---|---|---|
| **LiPo pouch cell with its own protection circuit** (current idea) | Thin (4–6 mm), light, the XIAO boards charge it directly [H15, #23] | Lithium: needs protection against over-charge, over-discharge and short circuit; must not be user-reachable; swells if abused | **No single-cell price found this round** (Evelta's first pages show only chargers and chips [H13, H19]; Robocraze page did not load [H23]). The plan's own estimate is ₹200–400 | **Keep; get a quote** |
| Cylindrical Li-ion (18650 size) | Cheap per mAh, robust can | 18 mm thick: would add back the height we are trying to remove | not sourced | Reject on thickness |
| LiFePO4 (a safer lithium chemistry) | More tolerant of abuse, longer life | Lower voltage (about 3.2 V) is marginal for the laser's 2.8 V rail without care; larger for the same energy; rarely sold as thin pouches | not sourced | Consider only if a hospital demands it |
| **2 × AA or AAA, alkaline or rechargeable NiMH** | No charger, no lithium transport rules, the family can swap them, sold everywhere | Thick (AA 14.5 mm, AAA 10.5 mm); a battery door is a weak point, a hygiene trap and something to lose; needs a small step-up circuit | not sourced | **Serious runner-up for a sold home unit.** Not for a lent unit: nurses would be changing batteries |
| USB power only (no battery) | Cheapest, nothing to charge or age | A cable to the bedside is a trip hazard and a chore (`DEVICE_LIFECYCLE.md:116`) | ₹0 | Prototype only |

**Charging and protection parts (for our own board at scale)**
- Charger chip: TP4056 family, ₹6.20–31.19 each; TP4054 ₹2.74 [H13].
- Protection chip: DW01A ₹11.50; DW06D ₹7.50; TI BQ29700 ₹43.10 (7Semi module ₹195) [H13, H19].
- Battery gauge chip: MAX17048 ₹507.45 [H13]. **Not worth it.** Read the battery voltage with the main chip through two resistors; accuracy of "full / half / low" is all we need.
- Set the charge current low (the XIAO nRF52840 offers 50 or 100 mA [H15]). A 1,000 mAh cell then charges overnight and stays cool.

**Rules and safety**
- **BIS registration.** Lithium cells and battery packs for portable use are under India's Compulsory Registration Scheme (standard IS 16046) [#300; consultancy snippets]. Buy cells that already carry a BIS registration mark and keep the certificate. Whether a device containing such a cell needs anything further was **not found** this round – NOT CONFIRMED.
- A 2026 ministry order will require rated-capacity checks on lithium cells for new registrations from about May 2027 (snippets; sources disagree on the exact date). Ask the cell supplier.
- **Battery waste rules** apply to whoever places batteries on the Indian market [#294].
- **Shipping.** Lithium cells travel under dangerous-goods rules (the UN 38.3 test summary). Not opened this round – NOT CONFIRMED. Ask the cell supplier for the UN 38.3 summary with the quote.
- **In the home:** no user-openable battery; a cell with its own protection board plus a second protection chip on our board; a temperature cut-off on charging if the charger chip supports it; never charge under a pillow (say so on the label and in the voice prompt).

- **Verdict:** KEEP LiPo, CHANGE to about 1,000–1,200 mAh, BIS-marked, with protection. Get three quotes.

---

### H-5: Feedback on the unit

| Choice | Good | Bad | Price found | Verdict |
|---|---|---|---|---|
| One colour-changing LED (WS2812B, current) behind a light bar | Any colour, one part, one wire | The chip inside draws power even when dark (not sourced this round: measure it); must be switched off by a transistor during sleep | not sourced | **Test** |
| 2–3 plain LEDs behind printed icons (battery, Bluetooth, tick) | Works for colour-blind users; zero drain when off; cheaper | Less "alive" | not sourced | **Preferred for the pilot** if the light bar is not needed for breath feedback |
| Piezo beeper (current, optional) | Tiny, cheap, robust, no opening needed (it sounds through the wall) | Beeps only; shrill for some hearing aids | not sourced | **Keep, make standard** |
| **Small speaker + I2S amplifier (MAX98357A)** with stored voice | Real spoken coaching with no phone | Needs a grille (a hole to seal), more battery, more memory | Amplifier boards ₹567–730 [H14] (the ₹150–300 in `DEVICE_LIFECYCLE.md:123` was a snippet; Evelta's branded boards cost more) | **Only for the no-phone version** |
| Small display | Shows numbers | Cost, a window that scratches and must be sealed, small text is useless to the elderly | not sourced | **No** |
| Vibration motor | Felt by people with poor hearing | The unit sits on a table, not in the hand; a motor would shake the sensor during a reading | not sourced | **No** |

**Sizing the voice memory (est.)**
- The repo counts 31 clips per language and about 3 MB a language as raw sound (`DEVICE_LIFECYCLE.md:123`). That matches about 93 seconds at 16,000 samples a second, 16 bits (93 × 32 kB ≈ 3 MB).
- 11 languages raw ≈ **33 MB**.
- With simple 4-to-1 compression (ADPCM, a light method any small chip can decode) ≈ **8 MB**. At phone-call quality (8,000 samples a second) ≈ **4 MB**.
- So a **16 MB memory chip holds all 11 languages** compressed. The XIAO nRF52840's built-in 2 MB extra memory [H15] holds one language at phone quality. This removes the "download a language pack at each handover" step in `DEVICE_LIFECYCLE.md:126`.
- **Status:** our arithmetic; the 3-second average clip length is inferred, not measured.

---

### H-6: Enclosure, compactness and durability ("we don't want it to break the second time")

#### What sets the 46 mm height, and how low it can go

| Layer (from `3D_SOURCES.md:136-138`) | Now | Why |
|---|---|---|
| Floor + standoff + sensor board + chip | 8.6 mm | electronics stack |
| Empty light tunnel up to the spirometer's floor | **31.4 mm** | **only there to keep the sensor 51.5 mm from the piston** |
| Foam pads, pocket rim | 2 + 8 mm (rim overlaps) | holds the spirometer |
| **Total** | **46 mm** | |

- The empty tunnel is the waste. The VL53L1X needs 40 mm; the piston already rests about 20 mm above the spirometer's floor, so about 20 mm of tunnel is truly needed with that chip, not 31. **That alone gives about 35 mm (est.).**
- With a sensor that reads from 1 mm (VL53L4CD), the tunnel can shrink to a few millimetres. The height is then set by the battery (about 5–6 mm), the circuit board, walls and the pocket rim: **about 22–28 mm (est.)**. InSee is about 29 mm [#101 group].
- **Do not thin the pocket rim.** It is what keeps the spirometer aligned.

#### Other shapes

| Shape | Size | Fits more models? | Alignment | Verdict |
|---|---|---|---|---|
| **Full tray** (current; InSee uses it [#102]) | Largest | No: the pocket is one base shape | Best: the whole base is held | **Keep for the pilot, but thinner** |
| **Tray with a swappable insert** | Same | **Yes**: one insert per spirometer model | Good | **The route to more models (H-7)** |
| Puck under the volume tube only | Small | Possibly | Poor: nothing stops it sliding; the spirometer would rock on it | Reject |
| Clip-on collar round the volume tube, sensor on an arm underneath | Small | Per tube diameter | Fair; clips fatigue and snap, and it covers part of the printed scale | Reject |
| Side pod with a camera | Small | Yes | Lighting-dependent | Not now (H-10) |

#### Materials and cleaning
- **PLA** (the usual hobby printing plastic) softens in a hot car and is brittle. Demo only.
- A plastics maker's bulletin, tested by an independent lab with hospital disinfectants on bars held under 1% and 2% strain for three days, ranks housings from worst to best: **PC+ABS → PC → PC+PET → PC+PBT → PPSU** [H9, vendor, grade C]. It did not test plain 70% alcohol, ABS alone or PETG.
- Search results add: PC+ABS is rated "poor" against healthcare cleaners; polycarbonate crazes in isopropyl alcohol at about 1.2% strain; cracks start at sharp corners, gates and sudden thickness changes (snippets).
- **No source found comparing PETG, ABS and PC+ABS against 70% alcohol wipes.** – NOT CONFIRMED. So test it: print six strips of each candidate, bend each over a curved block, wipe twice a day for a week with the hospital's actual wipes, and look for cracks or whitening.
- **Recommendation:** prototype in **PETG**; pilot in PETG or a machined/cast part after the wipe test; 1,000 units in an injection-moulded **PC+PBT or PC+PET** blend, smooth surface, no texture that traps dirt. Get the grade from the moulder with its chemical-resistance sheet.

#### Strength targets (figures from summaries of IEC 60601-1, the medical electrical safety standard; not the standard's own text)

| Test | Figure | Source | Use as our target? |
|---|---|---|---|
| Drop, hand-held parts | **1 m** | [H4]; a test house adds: three orientations most likely in use (snippet) | **Yes.** The unit is carried home in a bag and will be dropped from a table |
| Drop, portable equipment under 10 kg | 5 cm | [H4] | Too easy; use 1 m |
| Impact | 0.5 kg steel ball, 50 mm, dropped 1.3 m | [H4] | Yes, on the lid and the sensor window surround |
| Push | 250 N for 5 s over a 30 mm circle | [H4] | Yes: the lid must not flex onto the battery |
| Water, home-use equipment | **IP21** at least; **IP22** if hand-held or carried in use (IEC 60601-1-11 clause 8.3.1) | [H8] | **Target IP22**, plus wipe-down |

**IP rating in one line:** two digits; the first is protection against solid objects, the second against water. IP22 = fingers cannot reach inside, and dripping water does not harm it even when tilted 15°. The IP22 test is 3 mm of "rain" a minute for 2.5 minutes in each of four tilted positions [H8]. The same source warns that a 3D-printed prototype may not behave like the final part, and that "tell users to keep it dry" does not count as protection [H8].

- **Status:** SINGLE SOURCE each (secondary summaries, grade B/C). We are not claiming compliance with any standard; these are sensible targets. Whether the standards apply to us at all is a regulatory question.

#### Design details
- **Walls:** 2.5 mm with ribs under the pocket and round the battery bay; all inside corners rounded (at least 1 mm radius) because sharp corners are where cleaned plastics crack.
- **Sensor window:** a small flat window, recessed 1–2 mm so a cloth and a fingernail cannot scratch it, glued and sealed all round. Material that passes 940 nm light; ST's cover-glass guide gives the rules (thin, close to the sensor, small air gap) [#14]. Then run the chip's cross-talk calibration with the window fitted [H1]. Keep the dark tunnel walls matt.
- **Seams:** one seam, on the underside, with a gasket or a tongue-and-groove joint. No seam on the top face where spills land.
- **Button:** a moulded flexible dome that is part of the lid, pressing a switch inside. No hole.
- **Beeper:** behind a thinned wall. No hole.
- **USB-C:** recessed, with a tethered silicone plug; the connector soldered **and** held by the case, so a yanked cable pulls on plastic, not on solder joints.
- **Battery:** in its own ribbed bay with foam above and below (already in the model, `3D_SOURCES.md:144`); not reachable by the user; lid closed with tamper screws (a screw head that needs a special bit).
- **Alignment (this is the calibration):** a pocket with a firm, wipeable liner; a keyed shape so the spirometer fits one way only; a soft lip or strap that clicks so the spirometer cannot lift off when the patient pulls on the hose. The laser itself checks seating at every start: at rest the distance must be inside a narrow window, otherwise the app says "re-seat the spirometer".
- **Air:** never block the spirometer's air inlets (`HARDWARE.md:185`; arches B06b unmeasured). Thinner base, same rule.
- **Feet:** four wide silicone feet glued into recesses; a low, wide unit so pulling the hose does not tip it.
- **Label and QR code:** laser-etched or printed **under** a clear moulded window or on a polyester label with an over-laminate, in a recess on the underside and again on the side. No paper. No patient name ever (`DEVICE_LIFECYCLE.md:266`).
- **Foam:** the model lines the pocket with open EVA foam (`3D_SOURCES.md:135`). Open foam soaks up fluid and cannot be disinfected. **Replace it with a closed-cell silicone or TPE liner** that can be wiped, or moulded rubber ribs.

#### What is most likely to "break it the second time", and the answer

| # | Failure | Why it happens | Design answer |
|---|---|---|---|
| 1 | **Readings drift after a few days** | Spirometer re-seated slightly differently; sensor board moved after a knock | Keyed pocket + click-in lip; sensor screwed to a rigid rib, not taped; seating check at every start; per-session zero at rest |
| 2 | Cracks around screws and corners after weeks of alcohol wipes | Stress cracking of the plastic [H9] | Right plastic, rounded corners, metal inserts for screws, wipe test before the pilot |
| 3 | USB socket torn off the board | Cable yanked or unit dropped on the plug | Recessed socket held by the case; later, a magnetic or contact charging pad |
| 4 | Sensor window scratched or cloudy; dust in the tunnel | Wiping, pockets, bags | Recessed sealed window; app warns when signal strength falls |
| 5 | Battery flat on arrival, or dead after storage | Left asleep for months in a cupboard | Shipping-off mode; nurse's return checklist shows battery; charge before issue |
| 6 | Battery swollen or damaged by a drop | Impact, over-charge | Ribbed foam-lined bay, protected cell, slow charge |
| 7 | Liquid inside after cleaning | Sprayed rather than wiped; seams on top | IP22 target, one bottom seam, no holes on top, "wipe, do not spray or soak" in the checklist |
| 8 | Button fails | Mechanical switch behind a hole | Moulded dome, switch rated for many presses |
| 9 | Unit tips over when the patient pulls the hose | Tall and narrow | Thinner, wide base, silicone feet |
| 10 | Wire to the sensor breaks | Loose jumper wires (`HARDWARE.md:229` already lists this) | No loose wires in the pilot: sensor on a small board joined by a locking connector or a flat flex cable |
| 11 | Firmware bug found after units are in homes | No update path today | Signed updates over Bluetooth from the first pilot unit (H-2) |

- **Verdict:** CHANGE (thinner, sealed, tougher, wipeable). The tray idea stays.

---

### H-7: Fit across spirometer models

- **What we know:** InSee, with FDA clearance and funding, fits **only** the Vyaire AirLife 2500 and 4000 [RESEARCH_REPORT §4.1, F-COMP-1]. The US research add-on, built for the Voldyne 5000, was "near but incompletely aligned" on the Voldyne 2500 [H2]. **So nobody has shown one unit fitting many models.** – CONFIRMED (two independent sources).
- **What we could not find:** published base sizes or tube diameters for the Voldyne 2500/5000, Coach 2, Polymed, Portex or Hudson RCI models. One search this round returned no dimensions. Romsons publishes none for the Breazer (`3D_SOURCES.md:48`). – NOT FOUND.
- **Flow-type devices are out.** The Romsons SH 6082 and Teleflex Triflo lift three balls with airflow [#33]. There is no piston whose height means volume, so a distance sensor has nothing to read. A ball being up or down says "flow reached a level", not how much air went in.
- **What one base could share between volume-type models:** the electronics, the sensor, the battery and the lid shape. **What must differ:** the pocket shape, the sideways position of the volume tube over the sensor, the sensor-to-piston distance, and the calibration table.
- **What an adapter insert needs:** (1) a moulded pocket for that model's base; (2) it places that model's volume tube over the fixed sensor window (or the sensor sits on a slot with two or three click positions); (3) a way for the unit to know which insert is fitted, for example a pattern of small bumps read by two switches, so the right calibration table loads by itself; (4) it leaves that model's air inlets open; (5) it is wipeable or replaceable.
- **Cannot be known without a caliper and the actual devices:** every base outline; every tube's sideways position; resting piston height; whether each floor is open; mark spacing.
- **Verdict:** Breazer 2500 only for the pilot. Design the lid so the pocket is a separate part. Buy one each of two other volume-type models sold locally and measure them before promising "works with any spirometer".

---

### H-8: Calibration and accuracy

**How distance becomes millilitres.** The unit sends millimetres. A table, recorded once per spirometer **model** at the printed marks, turns millimetres into millilitres, with straight lines between marks (`HARDWARE.md:198-209`). The printed scale is a factory calibration and not the tube's swept volume, so never compute volume from diameter (`3D_SOURCES.md:108`). **Keep this.**

**What adds error, and the answer to each**

| Source of error | Size (source) | Answer |
|---|---|---|
| Sensor's own offset, different on every unit | VL53L4CD ±7–8 mm incl. part-to-part [H1]; VL53L1X ±20–25 mm [#118]. At about 22.4 mL per mm (est.) that is about ±160 mL or ±450 mL | **One-point offset per unit** at the factory or first use: seat the spirometer, read the rest distance, store the difference. The per-model table then applies to every unit |
| Reading noise with the piston still | about 1%, less with longer readings [#118] | Average a few readings; measure it on the bench |
| Wall echoes and the window (cross-talk) | makes it under-read [#136, #14] | Narrowest view, dark tunnel, the chip's cross-talk calibration with the window fitted [H1] |
| Temperature | an offset, not a scale error; the chip has a compensation function to call when temperature changes [H1] | Call it at each wake |
| Seating | "even 2 mm of wobble shows up as volume" (`HARDWARE.md:182`) = about 45 mL (est.) | Keyed pocket, click-in lip, zero at rest each session |
| The spirometer itself | Two devices read by eye differed by −469 to +567 mL on single readings in one study [#120] | Be honest: we report what the **scale** shows, not true lung volume |
| A tilted piston | unknown | Bench test |

**What accuracy is realistic.** Unknown until measured. The only comparable published number is the US add-on's "within 7.5%" [H2, #50]. **The repo's rule stands: report the measured number, never a target.** Do not say "±100 mL" (`HARDWARE.md:207`) in any pitch.

**How to measure it**
1. **Against the printed scale (primary).** Film the piston and the scale with a phone at 60 frames a second while the sensor logs. Read the piston position from the video at 20 moments per breath, 20 breaths, 3 units, 3 re-seatings. Report the average difference and the spread in mL.
2. **Against a calibration syringe (secondary).** A calibration syringe is a large, precise hand pump (usually 3 litres) used to check breathing instruments. Pull known volumes through the mouthpiece at slow, medium and fast speeds. This tests the **spirometer's scale** as much as our sensor, so report it separately. **No Indian price found**; abroad, 3-litre syringes list at about US$384–644 and £268 (snippets). Borrow one from a hospital lung-function lab.
3. Repeat in bright daylight, in the dark, and after a 1 m drop.

- **Verdict:** KEEP the method; ADD the per-unit offset step, the seating check and the measurement plan.

---

### H-9: Parts lists for three builds

All prices: Evelta, single unit, before GST, 10 Oct 2026, unless stated. GST on these parts is 18% (shown on the probots listing [H5]). "Not sourced" means no price was found this round and none is invented.

#### (a) Cheapest working prototype this month (cable to a laptop, no battery)

| Part | Supplier | Price | Source |
|---|---|---|---|
| XIAO ESP32-C3 | Evelta | ₹620 | [H10] |
| VL53L1X board (7Semi) | Evelta, 144 in stock | ₹745 | [H11] |
| Jumper wires, black foam, tape, piezo beeper | local shop | not sourced (small) | – |
| USB-C data cable | already owned | ₹0 | – |
| Printed PLA cradle | college lab or a print shop | not sourced | – |
| **Sourced subtotal** | | **₹1,365** (₹1,611 with GST) | |
| Spirometer: Romsons Breazer 2500 | pharmacy / online | about ₹200–1,000 | RESEARCH_REPORT §4.1 |

#### (b) Recommended pilot unit (about 10–50 units)

| Part | Supplier | Price | Source |
|---|---|---|---|
| XIAO nRF52840 (charger and 2 MB memory on board) | Evelta, 4 in stock | ₹1,030 | [H10] |
| Distance sensor board: VL53L1X (7Semi) **or** VL53L4CD if the bench test picks it | Evelta / import | ₹745 (VL53L4CD: not sourced) | [H11] |
| Motion sensor: LIS3DH board (7Semi) | Evelta, 22 in stock | ₹225 | [H20] |
| LiPo cell about 1,000–1,200 mAh, protected, BIS-marked | quote needed | not sourced (plan estimate ₹200–400) | Plan §3 |
| Beeper, LEDs, button, connector, silicone feet, screws, window | local / Evelta | not sourced | – |
| Small carrier circuit board (so there are no loose wires) | Indian PCB maker | not sourced; quote | [#281] |
| PETG case, printed, with liner | print service | not sourced; quote | – |
| **Sourced subtotal** | | **₹2,000** | |
| Unsourced lines, using the repo's own estimate of ₹300–500 for "battery, buzzer, case" | | + ₹300–500 (estimate, not a quote) | RESEARCH_REPORT §4.6 |
| **Working total** | | **about ₹2,300–2,500 before GST (about ₹2,700–2,950 with GST)** | |
| Optional speaker + amplifier for a no-phone trial | Evelta | + ₹567–730 plus a speaker | [H14] |

#### (c) Design for 1,000 units (our own circuit board)

| Part | Supplier | Single-unit price found | Source |
|---|---|---|---|
| Radio module, nRF52840 class | Evelta (IndieSemiC module; approval status not stated) | ₹539 (bare chip ₹357) | [H18] |
| – or ESP32-C3 / C6 module | Evelta | ₹265 / ₹285 | [H17] |
| Distance sensor chip (bare) | distributor quote | **not sourced** – no bare chip listed at Evelta | [H16] |
| Motion chip LIS3DHTR | Evelta | ₹59 | [H20] |
| Charger chip (TP4056 family) | Evelta | ₹6.20–31.19 | [H13] |
| Protection chip (DW01A / DW06D) | Evelta | ₹7.50–11.50 | [H13] |
| LiPo cell, BIS-marked | quote | not sourced | – |
| Circuit board + assembly | quote | not sourced | [#281] |
| Injection-moulded case (tool cost + per piece) | quote | not sourced | [#275] |
| Beeper, LEDs, window, feet, connector, label | quote | not sourced | – |
| **Sourced subtotal (nRF route)** | | **about ₹620** for four small lines only | |
| **Total** | | **cannot be stated honestly.** The four biggest lines (sensor chip, battery, board, case) have no price | |

**Does the repo's ₹1,000–1,700 hold?**
- **For build (a): yes**, at ₹1,365 before GST, with no battery and no proper case.
- **For build (b): no.** About ₹2,300–2,500 before GST. The plan's other figure, ₹1,400–2,600 (`RESEARCH_REPORT.md:267`), is the honest one for a pilot. **Use "about ₹2,500 a unit at pilot scale, our estimate from shop prices".**
- **For build (c): unknown.** Under ₹1,000 is possible only if the sensor chip, cell, board and case together come in under about ₹400–500. Nothing found this round supports or disproves that. Do not quote a volume price until four quotes are in hand.
- **Status:** build (a) CONFIRMED from listings; (b) partly estimated; (c) NOT CONFIRMED.

---

### H-10: Technology watch. What could change in 12–24 months, and the rule that keeps a change cheap

| # | Technology | How mature (what we found) | Realistic when | Threat or opportunity | Design rule that protects us |
|---|---|---|---|---|---|
| 1 | **Phone camera reads the spirometer, no hardware** | A 2025 paper: tablet camera, more than 95% detection, but **simulated patients only**, needs a stand, lighting-sensitive [H3]. A 2016 paper used a phone camera on chest movement, error about 19% (snippet) | A careful app could exist in 12–24 months | **Both.** It could make the base unit unnecessary for families who own a good smartphone and can prop it up. It does not help the many older patients with no smartphone (`DEVICE_LIFECYCLE.md:18`), in poor light, or who cannot aim a phone | **The app and server accept breaths from any "source"** (the contract already has a source field). Our value is coaching, dashboard and family link. Keep the breath-data format independent of the sensor. Consider building the camera reader ourselves as a no-hardware entry tier |
| 2 | **Newer and multi-zone laser sensors** | VL53L4CD exists now with 1 mm minimum and 55 µA watch mode [H1]; 8 × 8-zone parts could look only at the piston's centre, but use 216–313 mW (snippet) | Now / 12 months for lower-power multi-zone | Opportunity: thinner unit, safer beam margin | **Sensor on its own small plug-in board** with a fixed connector (power, two data wires, interrupt, shutdown). Swap the board, not the product |
| 3 | **Spirometer makers adding electronics themselves** | No Indian smart incentive spirometer found (RESEARCH_REPORT §11.2). InSee is an add-on, not built in | 24+ months, if ever at ₹200–1,000 price points | Threat at the top end; opportunity to be their software | Per-model calibration tables and a published unit-to-app message format; be the partner, not the rival |
| 4 | **Cellular modules with built-in SIM (LTE Cat-1 bis, eSIM)** | Modules listed in India at ₹450–720 (`DEVICE_LIFECYCLE.md:113`, snippet); operator registration reported slow | 12–24 months for us | Opportunity: no phone needed | Leave space and a connector for a radio daughterboard; keep breath scoring portable so it can move into the unit |
| 5 | **On-device machine learning (TinyML)** | The nRF52840 class runs small models; our classifier is rule-based plus a small model | Now | Opportunity: works offline | One shared set of test breaths that phone and unit must both pass (`DEVICE_LIFECYCLE.md:344`) |
| 6 | **nRF54L-class chips, Bluetooth 6 "Channel Sounding", LE Audio** | Channel Sounding measures phone-to-gadget distance to within tens of centimetres; development kits exist; early bugs reported; a few 2025–26 phones support it (snippets) | 12–24 months | Minor. Distance to the phone does not help read a piston. LE Audio could one day send the coach's voice to hearing aids | Use standard Bluetooth services and a versioned message format so the chip can change without the app changing |
| 7 | **60 GHz radar chips** | Makers claim sub-millimetre motion **detection**; range step about 3 cm; no published accuracy for a piston in a tube through plastic (snippets) | Research only | Low for now; cost and signal processing are high | Same as 2: sensor on a daughterboard |
| 8 | **Matter (smart-home standard)** | not researched this round | – | Irrelevant: no Indian patient's home needs the spirometer on a smart-home network | None |
| 9 | **Energy harvesting, printed flexible batteries** | not researched this round | 24+ months | Low. Our energy goes on a 22 mA laser, far beyond what harvesting gives | Keep the battery a standard, replaceable-by-us part |
| 10 | **Rules getting stricter** (battery capacity checks from 2027; radio approval changes in 2026) | snippets | 12 months | Threat to anyone who hard-codes one supplier | Buy certified modules and BIS-marked cells; keep certificates on file |

**The honest answer on item 1:** yes, a camera-only product would remove the need for our base in some homes. It would not remove the need for someone to coach the patient, tell the nurse, and tell the family. That is the part to own.

---

### H-11: What to buy first, the first three experiments, and when to change course

#### Shopping list for the first bench test

| # | Item | Qty | Supplier | Unit price (ex GST) | Line total | Source |
|---|---|---|---|---|---|---|
| 1 | **Romsons Breazer 2500** (one to keep whole, one to experiment on) | 2 | pharmacy / online | about ₹200–1,000 | ₹400–2,000 | RESEARCH_REPORT §4.1 |
| 2 | **Digital caliper** | 1 | hardware shop / online | ₹500–1,000 | ₹500–1,000 | `3D_SOURCES.md:17` |
| 3 | XIAO ESP32-C3 (runs today's sketch) | 1 | Evelta | ₹620 | ₹620 | [H10] |
| 4 | XIAO nRF52840 (the pilot board) | 1 | Evelta | ₹1,030 | ₹1,030 | [H10] |
| 5 | VL53L1X board, 7Semi | 2 | Evelta | ₹745 | ₹1,490 | [H11] |
| 6 | VL53L4CX board, Adafruit (the only 18°-family part found in India; **read its datasheet first**) | 1 | Evelta | ₹1,759 | ₹1,759 | [H7] |
| 7 | LIS3DH motion board, 7Semi | 1 | Evelta | ₹225 | ₹225 | [H20] |
| 8 | Small LiPo cell, jumper wires, breadboard, black foam, matt black tape, piezo beeper, a TV remote (for the infrared test) | – | local shop | not sourced | – | – |
| 9 | USB power meter or a multimeter that reads microamps (borrow from the college lab) | 1 | borrow | ₹0 | ₹0 | – |
| | **Electronics subtotal (items 3–7)** | | | | **₹5,124 (₹6,046 with 18% GST)** | |
| | **All sourced items (1–7)** | | | | **about ₹6,950–9,050 incl. GST on the electronics**, plus item 8 and delivery | |

Also try to source a **VL53L4CD** board (Pololu or a distributor such as Mouser or DigiKey India; not checked this round). It is the part most likely to shrink the unit.

#### The first three experiments, in order

**Experiment 1 – Look and measure (one hour, no electronics).**
1. Turn a Breazer over. Shine a torch up under the big tube. Is there an opening? Measure it. (B26)
2. If there is blue or clear plastic in the way: point a TV remote through it at a phone camera and press a button. If the camera sees the remote's light flicker, infrared passes.
3. With the caliper, measure every bold row in the Step 1 table. Write them into `docs/3D_SOURCES.md`.
4. Re-do the beam arithmetic in H-1 with real numbers.

**Experiment 2 – Does the sensor see the piston, smoothly? (half a day).**
1. Fix the sensor rigidly under the big tube, looking up, with a dark tube around it. Use today's sketch on the XIAO ESP32-C3 over USB.
2. Read the distance with the piston at rest. Turn the spirometer upside down so the piston slides to the other end; read again. That gives both ends with no breathing.
3. Have one person breathe in and hold at each printed mark, three times each (`HARDWARE.md:202-206`). Log distance against mark.
4. Repeat with: view window 4 and 8; the second sensor type; foam ring on and off; room light, darkness, and beside a sunny window.
5. Write down, for each combination: is distance against mark a smooth one-way curve; how much the reading wanders with the piston held still; any jumps.

**Experiment 3 – Moving breaths and real power numbers (one day).**
1. Film 20 breaths at 60 frames a second with the scale in view while logging the sensor. Compare the sensor's curve with the video. Report the differences in mL.
2. Move to the XIAO nRF52840 with a Bluetooth example sketch. Measure the current: asleep and advertising; awake and streaming; with the laser sensor in its watch mode.
3. Replace the assumptions in the H-3 table with the measured numbers and re-do the battery sum.
4. Wake test: does a pick-up wake it every time; does the piston-watch mode catch the first breath?

#### Results that should make the team change the sensing method

| Result | Change to |
|---|---|
| The floor under the piston is closed **and** infrared does not pass (remote test fails) | First try a side bracket looking at the piston through the clear wall at an angle; if that fails, the camera route (H-10 item 1). Do **not** cut the spirometer for anything a patient will use |
| Distance against printed mark is not a smooth one-way curve even with the narrowest view and a dark tunnel | Try the other chip; then an 8 × 8-zone sensor using only its centre zones; then the camera |
| With the piston held still, the reading wanders by more than about half a mark spacing (about 5.5 mm ≈ 125 mL, est.) at the top of travel | Same sequence |
| Sunlight by a window breaks the reading | Add a shroud round the tube base; if still broken, restrict use or change sensor |
| Re-seating the spirometer changes the reading by more than a few millimetres | This is an enclosure problem, not a sensor problem: fix the pocket before blaming the chip |

---

## The direct answer to "how do we detect the device is on?"

1. **Do not give the patient an on/off switch.** The unit is always in a very light sleep.
2. **While asleep it broadcasts a tiny "I'm here" radio message about once a second.** This is called Bluetooth advertising. On a low-power chip it costs about 16 µA, which is about 0.4 mAh a day (est. from forum measurements).
3. **That message carries the unit's ID, battery level, charging state, "spirometer seated" and a fault flag.** The app reads it without even connecting.
4. **The app's rule:** message heard in the last 5 seconds = "ready"; none for 10 seconds = "can't find your unit" (which covers off, flat battery and out of range; the app cannot tell these apart, so the unit's own light must).
5. **The unit wakes fully** on a button press, on being picked up (motion chip), when the phone connects, or (to be tested) when the laser sensor notices the piston move.
6. **The server knows** because the phone passes on "last heard" and battery level each time; the nurse sees "unit seen 2 h ago, battery 64%".
7. **With no phone at all**, a light and a beep tell the patient: woke up, ready, low battery, not seated, fault.
8. **For storage and shipping**, a hidden long-press puts the unit fully off; plugging in the charger or a long-press wakes it.
9. **This needs a chip change** (nRF52840 instead of ESP32-C3) because the ESP32 cannot broadcast while deeply asleep, and staying half-awake drains a 500 mAh cell in under two days (est.).

---

## Risks and open questions

### Needs a caliper and a real spirometer
- **B26: is the floor under the piston open?** Everything in H-1 depends on it.
- Total height (B02), base size (B04–B06), tube outer diameter and wall (B09, B10), piston size and rest height (B11, B12), mark heights (B14), air arches (B06b).
- The same measurements on two other volume-type spirometers before claiming wider fit.

### Needs a bench test
- Does either laser chip read the Breazer's piston smoothly over the full travel? (No published test exists.)
- Measured accuracy in mL against the printed scale. Do not quote a target.
- Real currents: asleep, advertising, awake. The battery table is arithmetic, not measurement.
- Does the piston-watch wake mode work, and does it miss the first breath?
- Does the WS2812B light drain the battery when dark?
- 70% alcohol wipe test on PETG and on the final plastic.
- 1 m drop, three orientations, then re-check calibration.
- Sunlight by a window.
- Whether a wipeable liner holds the spirometer as firmly as foam.

### Needs a quote or a professional
- LiPo cell, 1,000–1,200 mAh, protected, BIS-marked, with its UN 38.3 summary: three suppliers.
- Bare laser-sensor chip price at 1,000 units; circuit board + assembly; injection-mould tool and piece price.
- A VL53L4CD board delivered to India.
- A calibration syringe to borrow (no Indian price found).
- **WPC radio approval:** does a product built on an already-approved module need its own approval, and at what cost? Our reading is "yes, a self-declaration per model"; confirm with a WPC consultant.
- **BIS:** does a device containing a BIS-registered cell need anything more? Confirm with a BIS consultant.
- **Regulatory class** of a unit that only reads the piston from outside: already open in RESEARCH_REPORT §7.1. A sensor in the air path would make it worse; we recommend against it.

### What this review could not do
- Open the ST datasheets on st.com (timed out; the VL53L4CD was read from Pololu's mirror), the Espressif ESP32-C3 datasheet (server error), or robu.in (blocked). ESP32-C3 and nRF52840 current figures are therefore **search snippets**, not opened documents. Re-check them before they go into a pitch.
- Find any single-cell LiPo price, a VL53L4CD seller, or XIAO nRF52840 Sense / ESP32-C6 boards in India.
- Find spirometer dimensions for any brand.
- Read the IEC standards themselves (paid documents); drop and water figures come from test-house summaries.
- Research Matter, energy harvesting, printed batteries or UN 38.3 beyond a mention.
- Several search requests near the end were refused for rate limits (Web Bluetooth auto-reconnect; a second spirometer-dimension search).

---

## Sources opened this round

| # | URL | Title | Publisher | Grade | Used in |
|---|---|---|---|---|---|
| H1 | https://pololu.com/file/0J2060/vl53l4cd.pdf | VL53L4CD datasheet DS13812 Rev 8 (July 2024); mirror of st.com/resource/en/datasheet/vl53l4cd.pdf | STMicroelectronics via Pololu | A (maker datasheet) | H-1, H-3, H-6, H-8 |
| H2 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11041496/ | Burns et al. 2023, data capture device for clinical incentive spirometers (full text; same paper as ledger #49/#50, where only the abstract was read) | JMIR Biomed Eng via PMC | A | H-1, H-4, H-7, H-8 |
| H3 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12609343/ | Artificial-intelligence-assisted incentive spirometry (tablet camera), Healthcare (Basel), Oct 2025 | PMC | A | H-1, H-10 |
| H4 | https://601help.com/Requirements/mechanical.html | Mechanical strength requirements of IEC 60601-1 (summary) | 601help (consultancy) | C | H-6 |
| H5 | https://probots.co.in/vl53l1x-tof-laser-ranging-sensor-module.html | VL53L1X ToF module, ₹677.12 + GST, out of stock | Probots (retailer) | C | H-1, H-9 |
| H6 | https://kspelectronics.in/product/seeed-studio-xiao-esp32c3/ | XIAO ESP32C3 listing | KSP Electronics (retailer) | – | nothing useful (price not in the part read) |
| H7 | https://evelta.com/search.php?search_query=VL53L4CD | Search: VL53L4CD (none; Adafruit VL53L4CX ₹1,759) | Evelta (retailer) | C | H-1, H-11 |
| H8 | https://starfishmedical.com/resource/addressing-ingress-protection-for-home-healthcare-medical-devices/ | Ingress protection for home healthcare devices (IEC 60601-1-11 clause 8.3.1, IP21 / IP22) | StarFish Medical (design firm) | B | H-6 |
| H9 | https://www.formerra.com/sites/default/files/2021-07/chemical-resistance-healthcare-technical-bulletin.pdf | Medical device disinfection: how to prevent cracking and crazing (2020) | Avient (plastics maker), hosted by Formerra | C | H-6 |
| H10 | https://evelta.com/search.php?search_query=xiao | Search: XIAO boards and prices | Evelta | C | H-2, H-9, H-11 |
| H11 | https://evelta.com/search.php?search_query=VL53L1X | Search: VL53L1X (7Semi ₹745) | Evelta | C | H-1, H-9, H-11 |
| H12 | https://evelta.com/search.php?search_query=VL53L0X | Search: VL53L0X (Grove ₹693) | Evelta | C | H-1 |
| H13 | https://evelta.com/search.php?search_query=lithium+polymer+battery+500mAh | Search: charger, protection and gauge chips | Evelta | C | H-4, H-9 |
| H14 | https://evelta.com/search.php?search_query=MAX98357 | Search: MAX98357 amplifier boards ₹567–730 | Evelta | C | H-5, H-9 |
| H15 | https://wiki.seeedstudio.com/XIAO_BLE/ | Getting started with XIAO nRF52840 | Seeed Studio (maker docs) | B | H-2, H-3, H-4, H-5 |
| H16 | https://evelta.com/search.php?search_query=time+of+flight | Search: time-of-flight (VL6180 ₹1,339; no bare chips) | Evelta | C | H-1, H-9 |
| H17 | https://evelta.com/search.php?search_query=ESP32-C3-MINI | Search: ESP32-C3-WROOM-02 ₹265; ESP32-C6-MINI-1 ₹285 | Evelta | C | H-2, H-9 |
| H18 | https://evelta.com/search.php?search_query=nRF52840+module | Search: nRF52840 module ₹539, chip ₹357, XIAO ₹1,030 | Evelta | C | H-2, H-9 |
| H19 | https://evelta.com/search.php?search_query=lipo+battery+3.7V | Search: no single cells on page 1; protection module ₹195 | Evelta | C | H-4 |
| H20 | https://evelta.com/search.php?search_query=LIS3DH | Search: LIS3DHTR ₹59; 7Semi board ₹225 | Evelta | C | H-3, H-9, H-11 |
| H21 | https://evelta.com/search.php?search_query=reed+switch | Search: reed switch ₹105 | Evelta | C | H-3 (option rejected) |
| H22 | https://thinkrobotics.com/search?q=VL53L4CD | Search: VL53L4CD, 0 results | ThinkRobotics (retailer) | C | H-1 |
| H23 | https://robocraze.com/search?q=3.7V+500mAh+lipo+battery | Search: LiPo cells | Robocraze (retailer) | – | nothing read (page cut off before results) |
| – | https://www.st.com/resource/en/datasheet/vl53l4cd.pdf | VL53L4CD datasheet | ST | – | timed out; read via H1 |
| – | https://robu.in/?s=xiao+nrf52840&post_type=product | Robu search | Robu | – | HTTP 403, not read |
| – | https://documentation.espressif.com/api/resource/doc/file/aYwvqd1B/FILE/esp32-c3_datasheet_en.pdf | ESP32-C3 datasheet | Espressif | – | server error, not read |

**Search snippets only (not opened; grade C; check before quoting):**

| What | Where it appeared |
|---|---|
| VL53L4CD and VL53L1X ultra-low-power drivers: 55 µA and 65 µA at one reading a second; "window" threshold behaviour not well defined | ST product pages for STSW-IMG034 / STSW-IMG032; ST community thread on VL53L4CD interrupts; ST AN6172 |
| VL53L5CX: 4 × 4 or 8 × 8 zones, 63–65° diagonal, 20 mm minimum, 216–313 mW running, autonomous mode hard to reach in practice | ST datasheet listing; Pololu listing; ST community threads |
| TMF8806: 10 mm to 5 m or 10 m, ultra-low-power mode, 2.2 × 3.6 × 1.0 mm | ams OSRAM datasheet listings at Mouser and Farnell |
| nRF52840: System OFF 0.4 µA, sleep with clock 1.5 µA, radio 4.8 mA send / 4.6 mA receive | Nordic nRF52840 Product Specification v1.8 listing |
| Advertising once a second ≈ 9.5–16 µA average; the formula for average current | Nordic DevZone threads; hubble.com guide |
| ESP32-C3: chip deep sleep 5 µA, light sleep about 130 µA; XIAO ESP32-C3 board 44 µA deep sleep, 9.7 mA light sleep with Bluetooth, 26.8 mA modem-sleep with Bluetooth | Espressif datasheet and low-power guide listings; a third-party board test (mischianti.org) |
| LIS2DH12 "down to 2 µA"; LIS2DW12 lower | ST product and application-note listings |
| IEC 60601-1 drop test: three most likely orientations; clause 15.3.4 | StarFish Medical article |
| PC+ABS "poor" against healthcare cleaners; polycarbonate critical strain 1.21% in isopropyl alcohol; cracks at corners and gates | UL Prospector webinar, a polymer paper, PlasticsToday, Covestro brochure |
| WPC: a module's approval does not automatically cover the finished product; ₹10,000 per model self-declaration; March 2026 notice on the 6 GHz band | Freyr, Granite River Labs, Seyecs, Singhania notes; ST module ETA document |
| BIS: IS 16046 parts 1 and 2 cover lithium cells and packs under compulsory registration; rated-capacity order of 3 Feb 2026 effective about 1 May 2027 | Agile Regulatory, Nemko, Aleph India, Corpseed, SIQ notes |
| Bluetooth Channel Sounding: about ±20 cm in early implementations; nRF54L15 kits; a few 2025–26 phones support it | Bluetooth SIG, imec, Silicon Labs, Novelbits, Android 16 release notes |
| 60 GHz radar: "sub-millimetre" detection claim, 3 cm range step, no accuracy figure through plastic | Infineon BGT60TR13C page; TI IWR6843 datasheet listing |
| Phone camera on chest movement, error about 19%, 12 subjects (2016) | Reyes et al., Sensors 2016 (PMC4813972) |
| 3-litre calibration syringes: about US$384–644, £268; no Indian price | US, UK and Australian retailer listings |
| Voldyne 5000 / Coach: no dimensions published in results | McKesson, Zonamed, a 2005 Brazilian study |

**Count:** 23 URLs opened and read (21 useful, 2 with nothing useful), 3 that failed, and 17 groups of search snippets. Ledger rows reused without re-opening: #14, #23, #33, #50, #86, #101–103, #118, #120, #136, #149, #201, #275, #281, #294, #295, #300, #304. These new sources are **not yet in `SOURCES_LEDGER.md`** (this session was told to write only this file); the research agent should add them.
