# SpiroBuddy – device life cycle: how the unit connects, logs in, and moves between patients

**Written:** 10 Oct 2026, systems-design session · **Status:** design proposal. Nothing here is built unless section 2 says so. No contract in `ARCHITECTURE.md` is changed by this file.
**Sources:** `[#n]` = row in `docs/research/SOURCES_LEDGER.md` (reused, not re-opened). `[D1]`… = sources opened for this document (table at the end). **(est.)** = our own estimate. **(snippet)** = seen in a search result only, page not opened.
**Scope:** software and connectivity only. Pricing, hygiene rules and consumer law are in the business research (`docs/research/business/`).
**Sizes used:** S = up to 1 day · M = 2–5 days · L = 1–4 weeks.

---

## 1. In plain English (10 lines)

1. **Today the unit is a sensor on a USB cable.** It sends one number, 30 times a second, to a laptop browser. It has no Bluetooth, no memory, no identity, and no idea who the patient is. In the demo it is simulated.
2. **The unit should stay "dumb" about people.** It never stores a name. Target volume, hold time, language, voice, schedule and family contacts all live with the **patient's record on our server**.
3. **So "swapping the software for the next patient" is not a software swap.** The nurse ends one **assignment** (a record saying "unit SB-0007 belongs to patient X from this time to that time") and starts another. The settings follow the patient automatically.
4. **The patient never logs in.** For a lent unit, the nurse "logs the unit in" as a patient by scanning the QR code on the unit and choosing the patient. For a sold unit, the buyer scans the QR once and confirms a phone number.
5. **Staff log in** with the hospital's own account, or a phone number plus a one-time code. **Family** get an expiring link on WhatsApp. No one else gets in.
6. **For the pilot, connect by Bluetooth to a phone that stays with the unit**: the family's Android phone if they have one, otherwise a cheap Android phone the hospital lends in the same box. The phone is the speaker, the screen and the internet link. A USB cable is the fallback and already works in code.
7. **For scale, the unit talks to the internet by itself** with a built-in 4G module and SIM, and speaks through its own small speaker. No phone is needed in the patient's hand. This matters because most older Indians do not own a smartphone [#65, #184].
8. **Wrong-patient mix-ups are stopped three ways:** a QR scan at handover, a time window on every assignment, and a rule that breaths arriving when no assignment is open are held aside and never attached to anyone.
9. **Sold and shared units run the same firmware and the same server.** A sold unit is simply an assignment with no end date, owned by a family account instead of a hospital.
10. **For tomorrow's demo, mock one thing:** a "Units" screen where the nurse assigns a (simulated) unit to Ravi, returns it, assigns it to another patient, and the same patient screen changes name, language and target by itself.

**Everyday comparison:** the unit is like a library book with a barcode. The book does not know who is reading it. The library's computer knows who borrowed it and when. Returning it and lending it again changes nothing inside the book.
**Where the comparison breaks:** a book has no memory. Our unit will hold a few days of breaths while it is offline, and (at scale) a voice pack in one language. Those two things must be wiped or replaced at each handover. Section 5.4 covers this.

---

## 2. How it works TODAY (honest)

```
 REAL (written, but never run on real hardware)              SIMULATED / DEMO
 ───────────────────────────────────────────────             ─────────────────────────────
 [laser sensor] → [ESP32 board] ──USB cable──► Chrome on a laptop
   one text line per reading:                    │   or: SimulatorSource makes fake breaths
   D,<ms>,<distance_mm>                          ▼
                                   breath detection + scoring in the browser
                                                 │  POST /api/sessions {patient_id, breaths}
                                                 ▼
                                   FastAPI server (no login, DEMO_MODE=1)
                                      │                         │
                               nurse dashboard            family page (magic link) / WhatsApp
```

| Fact | Evidence (file:line) |
|---|---|
| The unit sends text lines over **USB serial only** at 115200 baud: `D,<millis>,<distance_mm>`, plus `S,` status and `E,` error lines | `firmware/spirobuddy_serial/spirobuddy_serial.ino:5-9, 171-176`; `docs/ARCHITECTURE.md:51-58` (CONTRACT A) |
| The only commands it accepts are `B` (beep) and `I` (re-send status) | `spirobuddy_serial.ino:11-12, 210-218` |
| **No Bluetooth or Wi-Fi code exists.** The chip can do both, but the antenna is "not needed for USB" | `docs/HARDWARE.md:56` |
| **The unit has no identity.** At start-up it prints only the board type and sensor type (`S,BOOT,XIAO_ESP32C3`, `S,READY,VL53L1X`). No serial number, no key | `spirobuddy_serial.ino:115-117, 260` |
| **The unit stores nothing** and has no battery or clock. If nothing is listening on the cable, readings are lost | whole sketch; `HARDWARE.md:3` |
| The firmware has **never been compiled or run** on a board here | `docs/HARDWARE.md:235` |
| The browser has two inputs: `SimulatorSource` (fake breaths) and `SerialSource` (Web Serial, "Chrome or Edge on a laptop") | `web/js/sources.js:34-65, 67-128, 75` |
| The patient phone app is an installable web page (manifest + service worker). It **starts in Simulator mode**; USB is a hidden demo-drawer button | `web/app.html:11, 337, 389, 414` |
| **The patient is chosen by the link**: `?id=` in the address, else the last one saved in the browser, else patient 1 | `web/app.html:207, 268` |
| The app sends `patient_id` to the server and the server believes it. **No login anywhere**; any website may call the API (`allow_origins=["*"]`) | `web/app.html:349`; `backend/app/main.py:44`; `docs/ARCHITECTURE.md:13` |
| The phone app does not calibrate USB readings yet (millimetres are treated as mL) | `web/app.html:209, 303` |
| **The voice comes from the phone or laptop speaker**: recorded clip → Sarvam speech → the browser's own voice | `web/js/voice.js:17-18`; `ARCHITECTURE.md:205-207` |
| Family access is a link with a random token, `guardian.html?t=…`. 128 random bits, stored in plain text, **never expires** | `backend/app/comms/guardians.py:135-137, 151-154, 242`; `web/guardian.html:30` |
| There are no `devices` or `assignments` tables. `sessions.source` is just a word: demo, device or app | `docs/ARCHITECTURE.md:188-196` |

**Note on `FUTURE_ARCHITECTURE.md`:** its section 0 says the family token is 72 bits. The code has since moved to 128 bits (`guardians.py:137`). The "no expiry, plain text" part is still true.

**One-line summary of today:** cable only, laptop only, no Bluetooth, no login, patient picked by a link, and the unit does not know who the patient is.

---

## 3. How everything connects – target design

### 3.1 The picture

```
                    (link A)                    (link B)
 [ BASE UNIT ] ◄──────────────► [ PHONE or HUB ] ◄────────► [ SERVER, India ] ──► nurse dashboard
  sensor, chip,   Bluetooth LE     web app:        mobile       patients, devices,  ──► doctor view
  button, light,  (USB cable as    voice, screen,  data         assignments,        ──► family: WhatsApp
  small memory    fallback)        breath scoring  (4G)         sessions, alerts         + expiring link

 At scale, the PHONE/HUB box disappears:
 [ BASE UNIT + 4G module + SIM + speaker + voice pack ] ◄──── mobile network ────► [ SERVER ]
```

"Bluetooth LE" (BLE) is the low-power kind of Bluetooth used by fitness bands. A "hub" is any always-nearby gadget that passes the unit's data on to the internet.

### 3.2 Recommendation

| | **Pilot (1 hospital, ~50 patients)** | **Scale (many hospitals)** |
|---|---|---|
| Link | **BLE from the unit to an Android phone that stays with the unit.** Use the family's own Android phone if there is one in the home; otherwise the hospital lends a low-cost Android phone in the same box (the "hub kit"). USB cable (USB-OTG) as fallback | **4G module (LTE Cat-1) with an M2M SIM inside the unit.** BLE kept for nurse set-up and for families who want the app |
| Voice | Phone speaker (already built, 11 languages) | Small speaker in the unit playing stored clips |
| Why | Re-uses the web app we already have. No app store. Chrome on Android supports Web Bluetooth and Web Serial [D1, D2]. No telecom paperwork | Works with no smartphone and no home Wi-Fi. One box, nothing to pair. Removes the lent phone, which is the most likely thing to be lost or broken |
| Cost of being wrong | Low: phones can be re-used for anything | High: a hardware change and telecom registration, so do it only after the pilot proves the product |

**Decision rule for the pilot:** at enrolment the nurse asks one question, "Is there an Android smartphone in the home that stays near the patient most of the day?"
- **Yes** → install the web app on it (scan the QR; no store, no password).
- **No, or iPhone only** → hand over the hub kit. (iPhones cannot use this route: Safari has no Web Bluetooth and no Web Serial [D1, D2].)
- **If the hospital will not lend phones** → nurse-tablet model: the unit stores breaths and the ward tablet or a home-visit nurse collects them (option 6 below). The daily dashboard then becomes a "last visit" dashboard, which weakens the product. Say so to the hospital.

**How this fits `FUTURE_ARCHITECTURE.md` §4:** it already chose BLE to the patient app or a home hub, device identity, an assignments table and a ≥7-day buffer. This document keeps all of that. It differs in three places, on purpose:
1. **USB-OTG added as a pilot fallback.** Web Serial reached Chrome on Android in 2026 [D1; Chrome 148 beta, Apr 2026 (snippet)], so today's firmware could feed a phone with zero new firmware. Unverified on a real phone.
2. **Built-in 4G plus an on-unit speaker for scale**, instead of the "Wi-Fi ESP32 hub" mentioned there. Reason: only about 9% of rural and 24% of urban households report a fixed or Wi-Fi connection, while about 99% have mobile coverage (NSO telecom survey, Jan–Mar 2025, **snippet**, not opened [D12]).
3. **A `wiped` step and an "unassigned readings" quarantine** are added to the life cycle (section 5).

### 3.3 All options compared (for an elderly patient at home in India)

| # | Option | Who must do what | What fails | Extra parts cost | Battery | Works with NO smartphone in the patient's hand? |
|---|---|---|---|---|---|---|
| 1 | **USB cable to a phone/laptop** (today) | Someone plugs a cable into the phone each session; phone must support USB-OTG (acting as the host for a gadget) | Loose cable, wrong cable (charge-only), phone cannot charge while in use, iPhone unsupported [D1]. Needs a recent Chrome | ~₹0 (an OTG adapter) | Unit runs off the phone; drains the phone | No |
| 2 | **BLE to the family's Android phone** (web app) | One-time QR scan. Page must be open during the session | Web pages cannot keep BLE running in the background, so stored breaths sync only when the page is open. No iPhone [D2]. Family phone leaves the house with its owner | ~₹0 (radio is already in the ESP32-C3) | Needs a small rechargeable cell in the unit | No (needs a family phone nearby) |
| 3 | **BLE to a native Android app** | Install from Play Store, grant permissions | Android limits background work; a foreground service or "companion device" set-up is needed to stay connected [D4]. Cheap phones kill background apps. A second codebase | ~₹0 hardware; **L+** software | Same as 2 | No |
| 4 | **BLE to a lent hub phone** (hub kit) ← **pilot** | Nurse pairs once at the hospital. Patient only presses Start (or nothing, if auto-start) | Phone lost, sold, uncharged, SIM out of data. Two things to return and clean | Phone ~₹5,400–6,000 each (2026 listings, **snippet** [D13]) + a data SIM | Unit: small cell. Hub stays on its charger | **Yes** (the hub is ours, locked to one screen) |
| 5 | **Wi-Fi from the unit to the cloud** | Someone types the home Wi-Fi password into a set-up app. Espressif's standard method sends it over BLE or a temporary hotspot, protected by a per-device secret on a QR sticker [D3] | Most homes have no Wi-Fi [D12]. Router changes, password changes. Every home is a support call | ~₹0 | Wi-Fi is power-hungry: mains adapter needed (est.) | Only for set-up it needs one |
| 6 | **Store-and-forward** (unit keeps breaths, nurse tablet or kiosk collects them) | Patient does nothing. Nurse or health worker brings a tablet near the unit | Data arrives days late, so missed-session alerts and family updates stop being daily | Flash memory + clock chip, small | Good | **Yes** |
| 7 | **Built-in 4G (LTE Cat-1) + M2M SIM** ← **scale** | Patient does nothing | Weak indoor signal. We must register as an M2M service provider with DoT and keep a record of who holds each unit [D5]; one team reported about six months to get set up with an operator [D6] | Module about ₹450–720 at single-unit Indian listings (2025–26, **snippet** [D14]); SIM plans quoted "as low as ₹30 a month" by one Indian blog [D6] | Needs a larger cell or mains | **Yes** |
| 8 | NB-IoT or 2G module | as 7 | NB-IoT in India is sold in bulk to registered firms and one developer reports patchy coverage (forum, **snippet** [D15]). Jio has no 2G at all [D15] | not sourced | Best | Yes, where it works |

**Why the others lost.** 1: a cable is a trip hazard and a daily chore for an older person, but it stays as the fallback because it already works. 3: a second app to build and maintain, before we know the product works. 5: too few homes have Wi-Fi. 6: on its own it kills the daily dashboard, but **every option should include it as a safety net** (the unit keeps 7 days of breaths, as `FUTURE_ARCHITECTURE` §4 already says). 8: not dependable enough yet. 7 is the right end state but too slow and too costly for a first pilot.

### 3.4 Where the voice comes from

| Option | Voice source | What it means for the hardware |
|---|---|---|
| 1–4 (any phone or hub) | The phone's speaker, using the app we have: recorded clip → server speech → browser voice (`web/js/voice.js:17-18`) | **Nothing extra in the unit.** A buzzer for reminders is enough. Hub phones need the volume locked high |
| 5–7 (no phone) | **A speaker in the unit** playing stored clips | Add a small amplifier board (about ₹150–300 in India, **snippet** [D16]) and a speaker. Add flash memory for one language's 31 clips at a time; about 3 MB as raw sound, far less if compressed (est.). The XIAO C3 has 4 MB in total, so more memory is needed. A popular ESP32 audio library does not support the C3 chip (**snippet** [D16]), so plan for a different chip or simpler playback code. Needs more power than a coin cell |
| 6 (store-and-forward only) | Speaker in the unit, or just beeps and lights | Same as above, or accept "no spoken coaching at home", which removes the main feature |

**Consequence for shared units at scale:** the voice pack is the one patient setting that physically sits inside the unit. On each new assignment the unit downloads the new patient's language pack. It is not personal data (the clips are the same for everyone), so it does not need wiping, only replacing.

**What moves into the unit at scale:** breath detection and scoring (today in the browser, `web/js/breath.js`) must also run on the chip, because there is no phone to do it. That is CONTRACT C re-written in C++ and tested against the same sample breaths. Size: L.

---

## 4. Mode A – the unit is SOLD (owned by one patient or family)

**Who this suits:** a family that has at least one smartphone (pilot hardware), or anyone at all (scale hardware with built-in 4G).

### 4.1 Set-up steps for the buyer (target)
1. Open the box. Stand the spirometer on the unit. Charge or plug in.
2. Scan the **QR code on the unit** with the phone camera. It opens our web app. The QR holds the unit's serial number and a one-time **claim code** (a per-unit secret that proves you are holding it; Espressif's set-up scheme calls this "proof of possession" and suggests a QR sticker [D3]).
3. Type a mobile number. A one-time code arrives on WhatsApp. Type it in. This creates the **household account**. No password, ever.
4. **Press the button on the unit** when asked. This proves the unit is in your hands, so a photo of someone else's QR is useless.
5. Answer four questions: patient's first name, age band, language, and the breathing goal written on the discharge paper (default 2,000 mL if none; the AI never sets or changes it).
6. Do one test breath. The app says "connected". Done.

### 4.2 What each thing means underneath
| Step | What the server records |
|---|---|
| Account created | `accounts` row (type = household), phone number verified |
| Unit claimed | `devices.owner_account_id` set; `device_assignments` row with **no end date** |
| Pairing | The phone and unit exchange keys once ("bonding": both sides remember each other, so they reconnect without asking again [D7]) |
| Patient profile | `patients` row owned by the household, not by a hospital |

### 4.3 Everyday situations
| Situation | What happens |
|---|---|
| **New phone** | Open the web app on the new phone, enter the same mobile number and one-time code. Scan the unit's QR and press its button again. History is on the server, so nothing is lost |
| **Second family member wants to see progress** | The owner sends them the same kind of expiring WhatsApp link we have today (30 days, renewable, read-only) |
| **Family wants their doctor or physio to see it** | Owner creates a "clinician link" (read-only, expiring) or types the clinic's code if that clinic uses our dashboard |
| **Recovery ends** | App offers: keep exercising (no reminders), pause, or **finish**. Finish stops reminders and messages. Data is kept until the family deletes the account, then erased within the period our privacy notice states |
| **Resale or hand-me-down** | Owner taps "Release this unit" in the app, **or** holds the unit's button for 10 seconds (factory reset). Both: wipe stored breaths and pairing keys on the unit and end the assignment on the server. The next person scans the QR and claims it. The old owner's history stays in the old owner's account; the new owner sees none of it |
| **Reset without internet** | The unit raises its own "reset counter". The server sees the higher counter on the next contact and closes the old assignment from the last breath it received |
| **Support** | Our support staff see the unit's health (battery, firmware, last seen), not the breaths, unless the owner grants time-limited access |
| **Updates** | Signed firmware delivered through the phone (pilot) or the SIM (scale), installed when idle, with automatic roll-back (`FUTURE_ARCHITECTURE` §4, [#201]) |

### 4.4 What the software lacks today for Mode A
Accounts and one-time-code login · unit identity (serial, claim code, key) · claim and release flow · BLE firmware and a BLE input in `web/js/sources.js` · on-unit storage · consent screen for a household (not a hospital) · delete-my-data · firmware update channel · a support view. None exist.

---

## 5. Mode B – the unit is LENT and SHARED (the hospital owns it)

### 5.1 The life cycle

```
            ┌────────────────────────────────────────────────────────────────┐
            ▼                                                                │
       IN STOCK ──assign──► ASSIGNED ──first home breath──► IN USE AT HOME   │
                                                              │              │
                                                           return            │
                                                              ▼              │
                                 WIPED ◄── CLEANED & CHECKED ◄── RETURNED    │
                                   └─────────────────────────────────────────┘
   Side exits from any state:  LOST  ·  FAULTY (→ repair → IN STOCK, or → RETIRED)  ·  RETIRED
```

| # | State | Who does it | On which screen | What the software does |
|---|---|---|---|---|
| 1 | **In stock** | Ward clerk or nurse | Units list (new) | Unit has a serial, a key, a QR sticker. No assignment open. Any breath it sends is quarantined |
| 2 | **Assigned** | Nurse at discharge teaching | "Assign unit": scan unit QR, pick or scan patient | Opens an assignment (start = now). Sends the unit a new **assignment number** and, at scale, the patient's language pack. Nurse and patient do one test breath; it must appear on that patient's row before they leave |
| 3 | **In use at home** | Patient | Nothing, or one Start button | Breaths carry the unit ID, the assignment number and a running count. Server attaches them to the patient via the open assignment |
| 4 | **Returned** | Nurse, clinic clerk or courier desk | "Return unit": scan unit QR | Pulls any breaths still stored on the unit, **then** closes the assignment (end = now). (One vendor does it in this order too: readings taken while un-assignment is pending stay with the user until the final sync [D11, snippet].) |
| 5 | **Cleaned and checked** | Nurse or technician | Return checklist | Records who, when, what cleaning step. Runs a 20-second self-test: sensor reads a known distance, battery level, buzzer/speaker. Fail → FAULTY |
| 6 | **Wiped** | Automatic, on the same screen | One "Wipe and re-stock" button | Unit erases stored breaths and pairing keys and raises its reset counter. Server stores the wipe time and who pressed it. Hub phone (if any) is reset to its standard image |
| 7 | **In stock** | – | Units list | Ready for the next patient |
| – | **Lost** | Nurse or admin | Unit page → "Mark lost" | Closes the assignment, blocks the unit's key so it can no longer post, suspends the SIM (scale) |
| – | **Faulty** | Anyone | Unit page → "Report fault" | Unit cannot be assigned until a check passes |
| – | **Retired** | Admin | Unit page | Key revoked for good. History of which patients used it is kept for audit |

This is the same list as `FUTURE_ARCHITECTURE.md` §4 (`in_stock → assigned → returned → cleaning → ready`, plus lost, faulty, retired) with two additions: `in_use` (so "handed over but never used at home" is visible) and an explicit `wiped` step.

**Lesson from hospitals that lend tablets:** one US hospital group needed 71 steps and 45–75 minutes to wipe each loaner tablet between patients, and cut it to one step and about 90 seconds with a purpose-built wipe app [D8]. If our return takes more than one scan and one button, nurses will skip it.

### 5.2 What the nurse sees
- **Units list:** serial, state, who has it, days out, battery, last seen, "not seen for 24 h".
- **On each patient row:** a small unit badge (SB-0007 · seen 2 h ago). A dead battery shows as a unit problem, not as "patient missed sessions".
- **Assign unit** (two scans, one confirm) and **Return unit** (one scan, one checklist, one button).
- **Overdue list:** units still out 7 days after the planned return date.

### 5.3 How settings "swap" automatically

**Nothing personal lives in the unit, so there is nothing to swap.** These all sit on the patient's record in the cloud (several already do; see `patients` and `care_settings` in `ARCHITECTURE.md` §6 and §10):

target volume · hold time · language · voice · exercise schedule and quiet hours · family contacts and consent · history and personal best

When a breath arrives, the server asks one question: *"Which patient had this unit at that moment?"* The answer comes from the assignment. The phone or hub asks the same question when it starts: *"I am connected to unit SB-0007. Whose settings do I load?"* It then shows that patient's greeting, goal and language. Ending one assignment and starting another is the whole "swap".

### 5.4 What is wiped on the unit, and what is kept in the cloud
| On the unit: wiped at return | In the cloud: kept |
|---|---|
| Stored breaths not yet uploaded (uploaded first, then erased) | The old patient's full history, under the old patient |
| Pairing keys for the last phone or hub | The assignment record (which unit, which patient, from, to, who assigned, who returned) |
| The current assignment number | Cleaning and self-test records for the unit |
| – | Unit health history (battery, faults, firmware) |
| **Not wiped:** serial, device key, firmware, calibration for the spirometer model, voice pack (replaced, not personal) | |

A plain factory reset can leave data recoverable on ordinary storage (general practitioner guidance, **snippet** [D17]). So the rule is: **the unit never holds anything that identifies a person in the first place**, and its storage is encrypted (ESP32 flash encryption [#201]). Then a wipe only has to remove anonymous numbers.

### 5.5 How wrong-patient data is prevented
1. **QR scan, not typing.** The nurse scans the unit and selects the patient from her own ward list. No serial numbers are typed.
2. **One open assignment per unit, one unit per patient.** The server refuses to assign a unit that is not "in stock", and refuses a second unit for a patient who already holds one.
3. **A spoken, name-free confirmation.** After assigning, the unit (or hub) says a two-digit code, for example "Ready. Code four-seven." The nurse's screen shows the same code. No name is spoken or shown on the unit, so nothing leaks if the box is seen by others.
4. **Test breath at the bedside.** The first breath must land on that patient's row while the nurse watches.
5. **Assignment number on every breath.** The unit stamps each breath with the assignment number it was given. A breath stamped with an old number can never be attached to the new patient, even if it is uploaded late.
6. **Time window.** A breath is accepted only if it was taken between the assignment's start and end.
7. **Fixing a mistake.** If a unit was assigned to the wrong patient, the nurse uses "Move this assignment". All breaths inside the window move together, with a reason, and the change is written to the audit log. (Other platforms handle a wrong assignment in a similar un-assign and re-assign way [D11, snippet].)

### 5.6 Readings while unassigned
Breaths that arrive with no open assignment (in the stock room, during cleaning, after a return, from a lost unit) go to a **quarantine list**. They are never shown on a patient and never counted. A nurse can see "SB-0007 recorded 3 breaths while unassigned on 12 Oct" on the unit's page, which is useful for spotting a unit that went home without being assigned. Quarantined breaths are deleted after 30 days (est. policy). One vendor's developer guide warns that mismatched IDs cause "orphaned device records" [D9]; the quarantine list is how we make orphans visible instead of silent.

**The unit has no trustworthy clock when its battery is flat.** So the unit sends a running count, and the phone, hub or network supplies the real time at upload. Breaths stored offline get their time worked out from the count and the unit's own timer, and are marked "time estimated".

---

## 6. Login and access for each person

| Person | Today | Target | Notes |
|---|---|---|---|
| **Nurse** | No login. Picks her name from a list in the browser (`web/js/comms.js:57`) | Hospital account (single sign-on) where the hospital has one; otherwise mobile number + one-time code on WhatsApp, plus a 6-digit PIN on shared ward tablets. Sees only her ward | Same as `FUTURE_ARCHITECTURE` §2.1 |
| **Doctor** | No login | Same as nurse; can also change targets | |
| **Hospital admin** | – | Same login; manages staff, units, exports. Cannot change care plans | |
| **Patient (lent unit)** | No login; chosen by `?id=` in the link (`web/app.html:207`) | **Still no login.** The nurse's assignment is the login. The hub or family phone is bound to the unit by QR; the unit is bound to the patient by the assignment | "Never require the patient to log in" stays the rule |
| **Patient / family (sold unit)** | – | Household account: mobile number + one-time code, once per phone. Then a long-lived token on that phone | |
| **Family (guardian)** | Link with a random token, never expires, stored in plain text (`guardians.py:135-137`) | Same idea, but the link expires in 30 days, is renewed over WhatsApp, is stored as a hash, shows first name only, and can be cancelled by the patient or nurse | |
| **The unit itself** | Nothing; anyone can post breaths for any patient | Its own key, put in at manufacture. The server rejects breaths from unknown or blocked units | Stops fake breaths |
| **Our support staff** | – | Separate login with a hardware security key. Sees unit health only. Patient data only by "break-glass": typed reason, 60 minutes, hospital admin told at once | |

---

## 7. Data: what lives where

| Place | What is there | Deleted when |
|---|---|---|
| **On the unit** | Serial number, device key, firmware, calibration table for the spirometer model, reset counter. Up to 7 days of breath summaries (numbers only: peak, hold, speed, count). Pairing keys. Current assignment number. At scale: one language's voice clips | Breaths: on upload confirmation, and at wipe. Keys and assignment number: at wipe. **Never on the unit:** name, phone number, diagnosis, hospital number |
| **On the phone or hub** | The web app, voice clips, a queue of breaths waiting to upload. Family phone: a token for that household. Hub phone: a token for that **unit**, not for a person | Queue: on upload. Hub: reset to standard image at each return. Family phone: on "log out" or account deletion |
| **In the cloud (India)** | Patients and their settings, assignments, sessions and breaths, alerts, messages, consent records, audit log, unit registry and health | Patient data: per the hospital's record rules and the patient's rights under the DPDP Act (see `FUTURE_ARCHITECTURE` §3.3, §3.7). Assignment and audit records outlive the unit |

**Privacy basics for the unit, in one list:** no patient name on or in the unit · the QR shows only a serial and a claim code · one key per unit, so one stolen unit cannot pretend to be another · firmware accepted only if signed by us, checked at every start-up [#201] · storage encrypted · pairing uses the modern Bluetooth method with a confirmation step, because the simplest pairing mode ("Just Works") gives no protection against someone in the middle [D7].

---

## 8. Side by side: sold vs shared (software differences only)

| Topic | SOLD | SHARED |
|---|---|---|
| Who owns the unit record | Household account | Hospital (tenant) |
| Accounts | Family creates one with a mobile number + one-time code | Staff accounts only; patient has none |
| How the unit is tied to a person | Buyer claims it: QR + button press | Nurse assigns it: QR + pick patient |
| Assignment | One, open-ended | Many, each with a start and an end |
| Who sets the breathing goal | Family types what the discharge paper says | Nurse or doctor on the dashboard |
| Who sees the data | Family; anyone they invite | Ward staff; family by link |
| Who owns the data | The patient/family | Hospital is responsible; patient keeps their rights |
| Reset | Owner releases it or holds the button | "Wipe and re-stock" as part of return |
| Readings with no owner | Held until someone claims the unit, then discarded | Quarantined, visible to the hospital, deleted after 30 days |
| Updates | Offered in the app; installed when idle | Pushed by us in stages; hospital admin sees versions |
| Support | Family contacts us; unit-health view | Hospital's admin first, then us |
| Analytics | Per household; anonymous totals for us | Per ward and hospital; unit utilisation (days out, turnaround, losses) |
| Extra screens needed | Claim, profile, release, delete account | Units list, assign, return, overdue |

**Shared code:** the firmware, the BLE or 4G protocol, the `devices` and `device_assignments` tables, breath ingestion, quarantine, firmware updates. Build Mode B first; Mode A is then mostly new screens.

---

## 9. What to build, in order

| # | Item | Size | Needed for | Notes |
|---|---|---|---|---|
| 1 | **Mock "Units" screen**: list of simulated units with state; Assign and Return buttons | S | **Hackathon demo** | Front-end only, or in-memory. See below |
| 2 | **Patient screen opened by unit** (`app.html?unit=SB-0007` looks up the open assignment and loads that patient) | S | **Hackathon demo** | Makes the "settings swap" visible |
| 3 | `devices` and `device_assignments` tables + `/api/devices` endpoints | M | Pilot | An addition to CONTRACT D: update `ARCHITECTURE.md` in the same step |
| 4 | Breath ingestion by unit + assignment window + **quarantine** for unassigned breaths | M | Pilot | Add `device_id`, assignment number and count to each breath |
| 5 | Real Assign / Return / Wipe screens with camera QR scan and checklist | M | Pilot | One scan, one button |
| 6 | QR sticker and serial for each unit; two-digit spoken confirmation | S | Pilot | |
| 7 | **Staff login** + roles + audit log | L | Pilot | From `FUTURE_ARCHITECTURE` §2 |
| 8 | **BLE firmware** (unit info, live stream, stored breaths, control) + `BleSource` in `web/js/sources.js` | L | Pilot | Add a rechargeable cell and a button to the hardware |
| 9 | On-unit storage (7 days), running count, reset counter | M | Pilot | Part of the BLE firmware work |
| 10 | Hub-phone set-up: locked to one screen, auto-start, reset-to-image at return | M | Pilot (only if the hospital lends phones) | |
| 11 | Verify USB-OTG + Web Serial on two real Android phones | S | Pilot fallback | Zero firmware change |
| 12 | Per-unit key, signed breath batches, key blocking for lost units | M | Pilot | |
| 13 | Expiring, hashed family links | S | Pilot | |
| 14 | Unit health view (battery, last seen, firmware) | S | Pilot | |
| 15 | Signed firmware updates with roll-back and staged roll-out | L | Scale | |
| 16 | Household accounts, claim and release flow (Mode A) | L | Scale (or a consumer launch) | |
| 17 | 4G unit: Cat-1 module, M2M SIM, on-unit breath scoring, speaker and voice packs | L+ (hardware revision) | Scale | Start the DoT M2M registration early; it is slow [D6] |
| 18 | Support console with break-glass | M | Scale | |

**Worth mocking in the demo (items 1 and 2, about half a day together):**
1. Open the Units screen. Three simulated units. Click **Assign** on SB-0007, pick **Ravi Kumar**. Open the patient screen for SB-0007: it greets Ravi in Hindi with his goal.
2. Click **Return**, tick "cleaned", click **Wipe and re-stock**. Click **Assign** again and pick a Tamil-speaking patient. Refresh the same patient screen: new name, Tamil voice, different goal. Ravi's history is still on Ravi's page.
3. Optional third beat: press "demo breath" on a unit in stock. A banner says "Held. This unit is not assigned to anyone."

Judges see the hand-over in under a minute, and it needs no hardware. Label it "simulated unit" on screen, in line with the DEMO badge.

---

## 10. Open questions, risks, and sources

### Open questions
| Question | Why it matters | Who can answer |
|---|---|---|
| Will the pilot hospital lend a phone with the unit? | Decides hub kit vs nurse-tablet model (section 3.2) | The hospital's nursing lead |
| Does USB-OTG + Web Serial really work with the XIAO ESP32-C3 on common low-cost Android phones? | It is the zero-firmware fallback | One afternoon of testing with two phones |
| Do the DoT M2M rules apply to us, and from when? The 2022 guidelines also name Bluetooth/Wi-Fi used for commercial M2M connectivity, not only SIMs [D5] | May need registration even for the BLE pilot. **Our reading is uncertain; confirm with a telecom lawyer before acting** | Lawyer; the business research owner |
| Real price of a Cat-1 module and M2M SIM at 1,000 units | Our figures are single-unit listings and a blog | Quotes from Airtel Business / Jio and a module distributor |
| Indoor 4G signal in the homes we serve | Option 7 fails silently without it | Pilot data: log signal strength from hub phones |
| Battery life of the unit on BLE with 14 sessions a day | Not measured; no hardware yet | Bench test |
| Is the base unit's surface cleanable to the hospital's standard, and does cleaning change the "medical device" paperwork? | Sets the return checklist | Business agent's hygiene research; infection-control nurse |
| How long may a hospital keep the "who had which unit" record? | We keep it for audit; rules may differ | Hospital records officer |
| Could the patient's wristband carry a QR we can scan? | Removes the last manual step in assigning | Hospital IT |

### Risks
1. **Hub phones go missing or get used for other things.** Mitigation: lock to one screen, low-value phone, deposit or sign-out (business side).
2. **Return step is skipped**, so the next patient's breaths land in quarantine. Mitigation: a unit not returned cannot be assigned; overdue list; one-button return.
3. **Web Bluetooth and Web Serial are not official web standards** [D1, D2] and could change. Mitigation: keep the unit protocol independent of the browser; a native app (option 3) is the escape route.
4. **No hardware exists yet.** Every hardware statement here is a plan. The firmware has never run on a board (`HARDWARE.md:235`).
5. **Moving scoring into the unit** (scale) means two copies of CONTRACT C. Mitigation: one shared set of test breaths that both must pass.
6. **Time on stored breaths is estimated**, so a slot may be credited to the wrong hour. Mitigation: mark them, and never raise a missed-session alert from estimated times alone.

### What we could not find
- A public, step-by-step "return, clean, wipe, re-issue" procedure from a remote-monitoring vendor. Vendors say they "process returns and refurbish devices" [D10] without detail.
- Official 2026 operator prices for M2M SIMs. Only a blog and reseller listings.
- An FDA or IMDRF text on wiping patient identity from a re-issued home device. IMDRF's cybersecurity guidance is about patient harm, not privacy (**snippet**). The UK NHS decommissioning page and one vendor help page refused our request (HTTP 403).

### Sources opened for this document
None of these were in `SOURCES_LEDGER.md`. The research agent should add them in its next round (this session was told to write only this file).

| ID | URL | Title | Publisher | Grade | Used in |
|---|---|---|---|---|---|
| D1 | https://caniuse.com/web-serial | Web Serial API support table (Chrome for Android: supported in current version; iOS Safari: none; "unofficial" spec) | caniuse | B | §3.2, §3.3, §10 |
| D2 | https://caniuse.com/web-bluetooth | Web Bluetooth support table (Chrome for Android and Samsung Internet: yes; iOS Safari and Firefox: no) | caniuse | B | §3.2, §3.3, §10 |
| D3 | https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/provisioning/provisioning.html | Unified Provisioning (BLE or hotspot set-up, per-device proof of possession, QR sticker) | Espressif (company docs) | B | §3.3, §4.1 |
| D4 | https://developer.android.com/develop/connectivity/bluetooth/ble/background | Communicate in the background (BLE) | Google, Android Developers | B | §3.3 |
| D5 | https://khaitanco.com/thought-leaderships/DoT-issues-guidelines-for-regulating-M2M-Service-Providers | DoT issues guidelines for regulating M2M service providers (8 Feb 2022) | Khaitan & Co (law firm note on a DoT rule) | B | §3.3, §10 |
| D6 | https://circuitdigest.com/articles/how-can-you-get-and-use-an-m2m-iot-sim-card-in-india | How can you get and use an M2M IoT SIM card in India? (25 May 2026) | CircuitDigest (blog) | C | §3.3, §9 |
| D7 | https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/ble/smp.html | BLE Security Manager: pairing, bonding, Just Works has no man-in-the-middle protection | Espressif (company docs) | B | §4.2, §7 |
| D8 | https://insights.samsung.com/2018/08/13/how-samsung-knox-and-data-eraser-help-uchealth-protect-patient-privacy/ | How Samsung Knox and Data Eraser help UCHealth protect patient privacy (71 steps → 1 step) | Samsung (vendor case study, US) | C | §5.1 |
| D9 | https://docs.tenovi.com/guides/common-interfaces-and-best-practices/ | Common interfaces and best practices (link and unlink a device and a patient) | Tenovi (remote-monitoring vendor docs, US) | B | §5.6 |
| D10 | https://www.prevounce.com/devices/fulfillment-and-logistics | Device fulfilment and logistics (pre-configured cellular devices, returns, refurbishing) | Prevounce (vendor marketing, US) | C | §10 |
| – | https://ruralindiaonline.org/en/library/resource/comprehensive-modular-survey-telecom-2025 | Comprehensive Modular Survey: Telecom, 2025 | PARI library | – | opened, page gave no figures |
| – | https://digital.nhs.uk/cyber-and-data-security/guidance-and-resources/guidance-on-protecting-connected-medical-devices/step-7.-have-a-decommissioning-replacement-plan | Step 7: have a decommissioning/replacement plan | NHS England | – | HTTP 403, not read |
| – | https://support.glooko.com/hc/en-us/articles/360001526737-What-happens-if-I-assign-a-device-to-the-wrong-patient-account | What happens if I assign a device to the wrong patient account | Glooko | – | HTTP 403, not read |

**Search snippets only (not opened; grade C; check before quoting in the pitch):**

| ID | What | Where it appeared |
|---|---|---|
| D11 | Un-assigning a device: readings stay with the user until the final sync (Radetco dosimeter help page); un-assign and re-assign after a wrong assignment (Glooko help page) | search results |
| D12 | NSO Comprehensive Modular Survey: Telecom, Jan–Mar 2025: 86.3% of households have internet at home; fixed/Wi-Fi 9.1% rural, 24% urban; mobile network 98.9% | search result quoting CEDA (Ashoka University) and PARI |
| D13 | Entry-level 4G Android phones at about ₹5,400–6,000 (2026 price lists) | pricekeeda, mysmartprice, magicdrop |
| D14 | SIMCom A7670C LTE Cat-1 module at ₹450–720 per piece, single-unit listings | IndiaMART sellers, Hubtronics |
| D15 | NB-IoT in India sold in bulk to registered firms; patchy coverage reported by one developer; Jio is 4G-only | Nordic DevZone thread (2026), maker blogs |
| D16 | MAX98357 audio amplifier board ₹150–300 in India; ESP32-audioI2S library does not support the ESP32-C3 | KSP Electronics, Zbotic, GitHub README |
| D17 | "Factory reset alone may leave recoverable data"; IMDRF N60 covers patient harm, not privacy | Censinet, ECRI and Paubox articles |

**Count:** 13 URLs opened (10 useful, 1 empty, 2 blocked) and 7 groups of search snippets. Ledger sources reused without re-opening: #65, #184, #201.
