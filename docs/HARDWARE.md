# SpiroBuddy – Hardware guide

**In one sentence:** a small laser distance sensor looks at the spirometer's moving disc, a tiny board reads it 30 times a second, and sends the distance to the laptop over a USB cable.

**No hardware? No problem.** The website demo (Simulator mode) and the 3D showroom work without any of this. Hardware is a bonus for hackathon day, not a requirement.

The sketch (the Arduino program) is at `firmware/spirobuddy_serial/spirobuddy_serial.ino`.

---

## 1. Parts list

| # | Part | Needed? | Notes |
|---|---|---|---|
| 1 | Volumetric incentive spirometer (e.g. Romsons Breazer 2500) | Yes | Must be the **piston/disc** type, not the 3-ball type. |
| 2 | One board: **Seeed XIAO ESP32-C3** (first choice), or any **ESP32 DevKit**, or **Arduino Uno / Nano** | Yes | Any one works. |
| 3 | One sensor: **VL53L1X** (first choice) or **VL53L0X** (backup) | Yes | Small breakout board ("module") with pins VIN, GND, SDA, SCL, (XSHUT, GPIO1). |
| 4 | USB cable **that carries data** (USB-C for XIAO; micro-USB or USB-C for DevKit; USB-B for Uno; mini/micro for Nano) | Yes | Charge-only cables can't upload code. If the board doesn't show up, try another cable first. |
| 5 | 4–5 female-to-female (or male-to-female) jumper wires, or a breadboard | Yes | |
| 6 | Passive piezo buzzer | Optional | Beeps when the app asks. Harmless if missing. |
| 7 | Black EVA foam (2–3 mm) | Recommended | A ring around the sensor blocks stray light. |
| 8 | Tape, Velcro or a 3D-printed clip | Yes | Holds the sensor in place. It must not move. |

---

## 2. The voltage question (read this once)

- **ESP32 boards (XIAO, DevKit) work at 3.3 V.** Always power the sensor from the board's **3V3** pin. Simple and safe.
- **Arduino Uno / Nano work at 5 V.** Sensor modules come in two kinds:
  - **Module with a regulator** (seller says "VIN 3–5 V" or "2.6–5.5 V", e.g. Pololu boards, most purple GY-530 / GY-VL53L0XV2 boards): connect VIN to **5V**. Fine.
  - **Module that says "3.3 V only"** or you're not sure: connect VIN to the Uno/Nano **3.3V** pin. The sketch switches off the Uno's own 5 V pull-ups on the data wires (`AVR_DISABLE_INTERNAL_PULLUPS 1`), so the data lines stay at the module's safe level.
- **When in doubt, use 3.3 V.** The sensor works on 3.3 V with every board. Wrong way round (3.3 V-only module on 5 V) can damage it.

---

## 3. Wiring tables

"I2C" is the two-wire link the sensor talks on: **SDA** = data, **SCL** = clock. Both sensors use the same pins, so each table covers **VL53L1X and VL53L0X**. The only difference: on the VL53L0X module, XSHUT may be labelled "XSHUT" or "SHUT", and GPIO1 is not used by us.

Always connect **GND to GND**. Leave the sensor's **GPIO1** pin unconnected.

### 3a. Seeed XIAO ESP32-C3 (with VL53L1X or VL53L0X)
| Sensor pin | XIAO pin |
|---|---|
| VIN | **3V3** |
| GND | GND |
| SDA | **D4** |
| SCL | **D5** |
| XSHUT | D10 (optional – lets the board restart the sensor) |

| Buzzer | XIAO pin |
|---|---|
| + (long leg / red) | D2 |
| − | GND |

No status light on this board (the XIAO C3 has no user LED). Attach the small antenna only if you later use Bluetooth/Wi-Fi; not needed for USB.

### 3b. ESP32 DevKit (any "ESP32-WROOM DevKit V1" style board, with VL53L1X or VL53L0X)
| Sensor pin | DevKit pin |
|---|---|
| VIN | **3V3** |
| GND | GND |
| SDA | **GPIO 21** (often printed "D21") |
| SCL | **GPIO 22** ("D22") |
| XSHUT | leave unconnected |

| Buzzer | DevKit pin |
|---|---|
| + | GPIO 25 |
| − | GND |

Status light: the built-in blue LED (GPIO 2) blinks while the sensor is missing and stays on when it's running.

### 3c. Arduino Uno (with VL53L1X or VL53L0X)
| Sensor pin | Uno pin |
|---|---|
| VIN | **5V** if the module has a regulator, otherwise **3.3V** (see section 2) |
| GND | GND |
| SDA | **A4** (also the pin labelled SDA near AREF) |
| SCL | **A5** (also labelled SCL) |
| XSHUT | leave unconnected |

| Buzzer | Uno pin |
|---|---|
| + | 8 |
| − | GND |

Status light: built-in LED on pin 13 ("L").

### 3d. Arduino Nano (with VL53L1X or VL53L0X)
| Sensor pin | Nano pin |
|---|---|
| VIN | **5V** if the module has a regulator, otherwise **3V3** (see section 2) |
| GND | GND |
| SDA | **A4** |
| SCL | **A5** |
| XSHUT | leave unconnected |

| Buzzer | Nano pin |
|---|---|
| + | D8 |
| − | GND |

Status light: built-in LED on D13.

---

## 4. Install the Arduino software (once per laptop)

1. Download and install **Arduino IDE 2** from https://www.arduino.cc/en/software
2. **ESP32 boards only:** add Espressif's board list.
   1. Open **File → Preferences** (on Mac: Arduino IDE → Settings).
   2. In **Additional boards manager URLs**, paste:
      `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
   3. Click **OK**.
   4. Open **Tools → Board → Boards Manager**, search **esp32**, install **"esp32 by Espressif Systems"** (version 3.x).
3. **Uno / Nano:** nothing extra – "Arduino AVR Boards" is already included.
4. Install the sensor library: **Tools → Manage Libraries**, then search and install the one for your sensor:
   - **VL53L1X** by **Pololu** (for the VL53L1X sensor)
   - **VL53L0X** by **Pololu** (for the VL53L0X sensor)

   Careful: there are look-alike libraries (SparkFun, Adafruit, STM32duino). The sketch needs the **Pololu** ones.

---

## 5. Upload the sketch

1. Open `firmware/spirobuddy_serial/spirobuddy_serial.ino` in Arduino IDE.
2. Near the top, pick your sensor. Exactly one line must be active (no `//` in front):
   ```
   #define SENSOR_VL53L1X
   // #define SENSOR_VL53L0X
   ```
3. Plug the board in with the USB cable.
4. **Tools → Board** – choose:
   - XIAO: **esp32 → XIAO_ESP32C3**
   - ESP32 DevKit: **esp32 → ESP32 Dev Module**
   - Uno: **Arduino AVR Boards → Arduino Uno**
   - Nano: **Arduino AVR Boards → Arduino Nano**. If upload fails, also try **Tools → Processor → ATmega328P (Old Bootloader)** (common on cheap Nanos).
5. **XIAO only:** check **Tools → USB CDC On Boot → Enabled** (it's the default for this board). If it's Disabled, the Serial Monitor shows nothing.
6. **Tools → Port** – choose the new COM port that appeared when you plugged in.
7. Click **Upload** (the → arrow button). Wait for "Done uploading".

Upload problems:
- **ESP32 DevKit stuck on "Connecting…":** hold the **BOOT** button on the board until upload starts.
- **XIAO not showing a port:** hold **B** (BOOT), tap **R** (RESET), release B, then upload.
- **No port at all:** try another cable (data cable!). Cheap Nano/DevKit clones may need the **CH340** or **CP210x** USB driver.

---

## 6. Check that it works (Serial Monitor)

1. **Tools → Serial Monitor**. At the bottom right, set the speed to **115200 baud**.
2. Press the board's reset button (or unplug/replug). You should see:
   ```
   S,BOOT,XIAO_ESP32C3
   S,READY,VL53L1X
   D,1520,182
   D,1553,181
   D,1586,183
   ...
   ```
   - `D,<time in ms>,<distance in mm>` – about 30 lines per second.
   - Move your hand in front of the sensor: the last number should change.
3. Type `B` in the message box and press Enter: the buzzer beeps (if fitted).
4. **Close the Serial Monitor before using the website.** Only one program can use the port at a time.

What the other lines mean:
| Line | Meaning |
|---|---|
| `S,READY,VL53L1X` | Sensor found and running. |
| `E,SENSOR_NOT_FOUND` | Board can't see the sensor. It retries every 2 seconds by itself. Check wiring. |
| `E,TIMEOUT` | Sensor stopped answering for a moment. After 5 in a row the board restarts the sensor (`E,SENSOR_LOST_RESTARTING`). |
| `E,NO_TARGET` | Nothing within range (or too close). Shown at most every 2 s. |

---

## 7. Mounting the sensor on the spirometer

**Golden rules**
- Keep **at least 5 cm** between the sensor and the disc **at every position**. Closer than about 4 cm and readings go wrong.
- The sensor must **not move** during a session. Even 2 mm of wobble shows up as volume.
- **Never change the air path** of a spirometer a patient will use. Experiment on the spare.

**Option A – Base mount (try first).** The spirometer stands on a short stand; the sensor looks **up** at the underside of the disc. Often there's no plastic in the way, so readings are clean. Leave channels in the stand so air can still enter.

**Option B – Top mount.** The sensor sits on top and looks **down** through the plastic lid. Easier to clip on, but the laser passes through plastic, which can reflect back and fake a reading (this is called **crosstalk**: like seeing your own reflection in a window instead of what's outside). To reduce it:
1. Press the sensor **flat against the plastic**, no air gap.
2. Put a **black foam ring** around the sensor window.
3. Make sure the plastic is clean and not scratched in that spot.

**Foam ring:** cut a 2–3 mm black EVA foam ring that surrounds the sensor's two little windows (emitter and receiver) without covering them. It blocks stray light and reflections.

**Aim:** point the sensor at the **middle of the disc**. The sketch already narrows the VL53L1X's view (setting `VL53L1X_ROI_SIZE 8`, about 20° instead of 27°) so it sees the disc, not the walls. If readings jump when the disc is near the walls, try `4` (narrowest, ~15°). The VL53L0X can't narrow its view (fixed about 25°).

---

## 8. Calibration with the printed mL marks

The sensor gives **distance in mm**. The website turns that into **mL** using a small table you record once per spirometer model. Between marks it draws a straight line (called **interpolation**).

1. Mount the sensor firmly. Start the website in **Serial** mode and open the calibration screen.
2. With the disc at rest (0 mL), record a point.
3. One person breathes in slowly and **holds the disc steady** at the **500 mL** mark. A teammate presses record.
4. Repeat for **1,000, 1,500, 2,000** (and 2,500 if your model has it).
5. Do each mark **3 times**; the average is used.
6. Check: do 10–20 breaths and compare the screen with the mark you see by eye. Target: within ±100 mL.

Note: the distance gets **smaller** as the disc rises (base mount: bigger). That's normal; the website handles both directions.

---

## 9. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| No COM port appears | Charge-only cable, or missing driver | Try another cable; install CH340/CP210x driver for clones. |
| Serial Monitor is blank (XIAO) | USB CDC On Boot is off | Tools → USB CDC On Boot → Enabled, upload again. |
| Serial Monitor shows garbage | Wrong speed | Set 115200 baud. |
| `E,SENSOR_NOT_FOUND` repeating | Wiring | Check VIN/GND, and that SDA/SCL aren't swapped. Check the board's pins in section 3. Try the 3.3 V pin. |
| `E,SENSOR_NOT_FOUND` with a VL53L0X | Sketch set to VL53L1X (or the other way round) | Change the `#define SENSOR_...` line, install the matching Pololu library, upload. |
| Compile error "VL53L1X.h: No such file" | Library missing | Install "VL53L1X by Pololu" (or VL53L0X by Pololu). |
| Compile error about `begin` / wrong library | A look-alike library is installed | Remove the SparkFun/Adafruit one or make sure the Pololu one is installed. |
| `E,NO_TARGET` all the time | Disc out of range, or sensor too close (<4 cm) | Move the sensor so the disc is 5–100 cm away. |
| Numbers jump around a lot | Sensor wobbles, light leaking, or seeing walls | Fix it firmly, add foam ring, set `VL53L1X_ROI_SIZE 4`. |
| Numbers don't change when disc moves (top mount) | Crosstalk from the plastic lid | Press sensor flat on plastic, add foam ring, or switch to base mount. |
| Website can't connect | Serial Monitor still open, or not using Chrome/Edge | Close Serial Monitor; use Chrome or Edge on the laptop (Web Serial). |
| No beep on `B` | No buzzer, wrong pin, or an *active* buzzer | Check pin table. A passive piezo is expected; it's optional anyway. |
| Uno upload works but readings stop after a while | Loose jumper wire | Re-seat the wires; keep them short. |

---

## 10. What was verified (and where)

The sketch has **not** been compiled here (no Arduino tools on this laptop). Every library function and pin was checked against the official sources below.

- Pololu VL53L1X library (v1.3.1, name "VL53L1X"): `init()`, `setTimeout()`, `setDistanceMode(VL53L1X::Short)`, `setMeasurementTimingBudget(us)`, `setROISize(w,h)` (4–16), `setROICenter(spad)` (199 = centre), `startContinuous(ms)`, `dataReady()`, `read(bool blocking)`, `ranging_data.range_status` with `RangeValid` / `RangeValidMinRangeClipped`, `timeoutOccurred()`. Minimum timing budget in Short mode is 20 ms; we use 33 ms. ROI support was added in library v1.3.0.
  - https://github.com/pololu/vl53l1x-arduino
  - https://raw.githubusercontent.com/pololu/vl53l1x-arduino/master/VL53L1X.h
  - https://raw.githubusercontent.com/pololu/vl53l1x-arduino/master/VL53L1X.cpp
  - https://raw.githubusercontent.com/pololu/vl53l1x-arduino/master/README.md
  - https://raw.githubusercontent.com/pololu/vl53l1x-arduino/master/examples/Continuous/Continuous.ino
- Pololu VL53L0X library (v1.3.1, name "VL53L0X"): `init()`, `setTimeout()`, `setMeasurementTimingBudget(us)`, `startContinuous(period_ms = 0)`, `readRangeContinuousMillimeters()` (returns 65535 on timeout), `timeoutOccurred()`.
  - https://github.com/pololu/vl53l0x-arduino
  - https://raw.githubusercontent.com/pololu/vl53l0x-arduino/master/VL53L0X.h
  - https://raw.githubusercontent.com/pololu/vl53l0x-arduino/master/VL53L0X.cpp
- XIAO ESP32-C3 pins (D4 = GPIO6 = SDA, D5 = GPIO7 = SCL, D2 = GPIO4, D10 = GPIO10), board macro `ARDUINO_XIAO_ESP32C3`, and "USB CDC On Boot" default Enabled:
  - https://raw.githubusercontent.com/espressif/arduino-esp32/master/variants/XIAO_ESP32C3/pins_arduino.h
  - https://raw.githubusercontent.com/espressif/arduino-esp32/master/boards.txt
- ESP32 DevKit default I2C (SDA 21, SCL 22):
  - https://raw.githubusercontent.com/espressif/arduino-esp32/master/variants/esp32/pins_arduino.h
- Espressif board manager URL (stable):
  - https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html
