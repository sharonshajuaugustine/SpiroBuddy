# Mobile app and Bluetooth plan

**Written:** 10 Oct 2026 · **Sources opened this round:** 35 (33 useful, 2 gave nothing) · **Confidence overall:** medium. Store fees and platform rules are high (official pages). Effort, battery and field behaviour are low (no hardware exists, nothing here has been run on a phone).

**How to read this file**
- `M-n` = a finding. Each has a status: **CONFIRMED** (primary source or two sources), **SINGLE SOURCE**, **NOT CONFIRMED**.
- `[S n]` = a source opened this round (table at the end). `[#n]` = a row in `docs/research/SOURCES_LEDGER.md`. `[D n]` = a source already opened for `docs/DEVICE_LIFECYCLE.md` (not re-opened). `B4-n` = a finding in `docs/research/business/04_legal_and_regulatory.md`.
- **(est.)** = our own estimate. **(snippet)** = seen in a search result only, page not opened, grade C. **(eng.)** = common engineering knowledge that we did not check against a source this round; verify before relying on it.
- **Money:** US$1 = ₹96 is used throughout. Basis: a newspaper headline of ₹95.79 on 11 Sep 2026 and an RBI reference rate of ₹96.29 on 18 May 2026, both **snippets**. We could not find the rate for 9–10 Oct 2026. Note that `FUTURE_ARCHITECTURE.md` §11 uses ₹88; the cost agent should settle one rate.
- **Chip:** the hardware reviewer is choosing it. This file assumes "an ESP32-C3-class or nRF52-class Bluetooth Low Energy chip, final part pending `docs/plan/01_HARDWARE_REVIEW.md`". Everything below works with either.
- This is not legal advice. Where a rule is involved, our reading is given; confirm with a regulatory consultant or lawyer before acting.

---

## Answer in 12 lines

1. **Today there is no Bluetooth anywhere.** The patient app is an installable web page that runs a simulator or a USB cable. The firmware has never run on a board.
2. **A web page cannot give "connects automatically every time".** Web Bluetooth works in Chrome on Android but only while the page is open, and iPhones do not have it at all. So the founder is right: a real app is needed.
3. **Pilot path: keep today's web code and wrap it in an Android app (Capacitor), plus one small piece of native Android code that owns the Bluetooth link.** About 80–90% of today's code is reused (est.).
4. **Scale path: the same shell, with the Bluetooth part written natively on each platform (Kotlin for Android, Swift for iPhone).** Rewrite the screens natively only if cheap phones prove too slow.
5. **Automatic connection on Android is done with three official pieces:** "companion device" pairing, its "device presence" wake-up, and a visible "foreground service" while a session runs. Cheap Xiaomi, Samsung, Oppo and Vivo phones still kill background apps, so the design never depends on the app staying alive: **the unit stores breaths and the unit itself beeps the reminders.**
6. **"Is the unit on?" is answered by one thing: the unit's Bluetooth heartbeat (advertising).** If the phone hears it, the unit is on. The app turns nine separate technical states into one big picture and one spoken sentence.
7. **Google Play costs US$25 once (about ₹2,400). Apple costs US$99 every year (about ₹9,500).** Neither store takes a cut if hospitals pay us outside the app.
8. **The hidden blocker is not money, it is paperwork:** an organisation account on either store needs a D-U-N-S number, which needs a registered company. The team has no company yet.
9. **Skip iPhone for the pilot.** Android is about 94% of phones in use in India, and a lent hub phone is Android anyway. Decide on iPhone from real enrolment data.
10. **Do not put the pilot app on the public store.** Install it directly or as a private app. A public health listing forces a choice between "this is a medical device" and "this is not a medical device", and that choice is not made yet (B4-1, B4-8).
11. **Realistic effort:** bench prototype 3–5 weeks, pilot Android app another 6–9 weeks, Play release 3–4 weeks, iPhone 6–9 weeks, for one competent developer (est.).
12. **We missed about 30 things** (section 13). The top ones: no company for the store accounts, account and signing-key ownership, the delete-my-data rule, a possible Bluetooth SIG listing fee, and phones that kill background apps.

---

## Step 1 – What exists today (facts from the code)

| What | Fact | Evidence (file:line) |
|---|---|---|
| Patient app | An installable web page, not a store app. Hindi by default, browser auto-translate switched off | `web/app.html:2, 9, 11` |
| Install and offline | A manifest (name, icons, "standalone" display, portrait) and a service worker that caches the app shell and the voice clips; API calls are never cached | `web/manifest.webmanifest:2-18`; `web/sw.js:5-7, 17, 19-20`; `web/app.html:419` |
| Which patient | Chosen by `?id=` in the link, else the last one saved in the browser, else patient 1. No login | `web/app.html:207, 268` |
| Inputs | Two only: `SimulatorSource` (fake breaths at 30 per second) and `SerialSource` (USB cable through Web Serial, "Chrome or Edge on a laptop"). **There is no Bluetooth source** | `web/js/sources.js:34-65, 67-128, 75`; `web/app.html:334` |
| USB safety check | The app refuses a USB unit that has no calibration, so millimetres are never shown as mL | `web/app.html:329-333` |
| Breath detection | Runs in the browser: median filter, calibration, a four-state detector, features, score, rule fallback | `web/js/breath.js:4, 29, 51, 67, 150`; `docs/ARCHITECTURE.md:65-98` (CONTRACT C) |
| Saving a session | `POST /api/sessions` with `patient_id`, start time and the breaths. If it fails, the data is lost (no queue) | `web/app.html:354`; `docs/ARCHITECTURE.md:109` |
| Safety button | "I do not feel well": a fixed message, a `tel:112` button, and a red-flag post to the nurse. Never AI | `web/app.html:187, 374-383` |
| Voice | Recorded clip → server speech → the browser's own voice | `web/js/voice.js:18, 192, 194` |
| Family page | A link with a token, `guardian.html?t=…`, refreshed every 15 seconds | `web/guardian.html:30, 171, 183` |
| What the unit sends | CONTRACT A: text lines `D,<millis>,<distance_mm>` about 30 times a second, plus `S,` status and `E,` error lines; the browser may send `B` to beep | `docs/ARCHITECTURE.md:51-58`; `web/js/sources.js:105-119` |
| The API | CONTRACT D: plain JSON under `/api`, no version prefix, no login | `docs/ARCHITECTURE.md:100-120` |
| The plan on paper | `FUTURE_ARCHITECTURE.md` §5 already asks for: offline-first with an outbox, a sync contract "CONTRACT F", `/api/v1`, Android 8+, install size ≤ 30 MB, 2 GB RAM, voice-first screens | `docs/FUTURE_ARCHITECTURE.md:196-210` |
| Device link on paper | `FUTURE_ARCHITECTURE.md` §4 and `DEVICE_LIFECYCLE.md` §3 choose Bluetooth to a phone or hub, a 7-day buffer, unit identity and assignments | `docs/FUTURE_ARCHITECTURE.md:183-190`; `docs/DEVICE_LIFECYCLE.md:86-96` |

**One line:** the coaching, voice, scoring and safety screens exist and are reusable. Bluetooth, background work, login, a local database, a sync queue and store accounts do not exist.

---

## Step 2 – Findings

### 1. Which kind of app

#### M-1: A web page alone cannot meet "connects automatically every time"
- Detail: Web Bluetooth works in Chrome and Samsung Internet on Android and not in Safari on iPhone [D2]. In Sept 2024 a Chrome engineer wrote that "The WebKit project continues to be opposed to generic peripheral access APIs such as Web Bluetooth" and that it "has not been added to a major browser on iOS" [S34]. We found no later change. A web page talks to the unit only while it is open on screen (DEVICE_LIFECYCLE §3.3 row 2, citing [D4]). The calls that would let a page re-find a known unit without the user picking it again (`getDevices`, scanning) are still behind a Chrome setting on the web, according to the Capacitor Bluetooth plugin's notes [S25].
- Source: [S34] grade B; [S25] grade B; [D2] grade B.
- Status: CONFIRMED for "no iPhone" (two sources). SINGLE SOURCE for "re-find needs a Chrome setting" (test on a real phone).
- What it means: the web app is good for bench tests and demos. It cannot be the pilot app if the founder's rule is "no steps each time".

#### M-2: Comparison of the four options for THIS product

| | (a) Web app + Web Bluetooth | (b) Web app wrapped for the stores | (c) Cross-platform native | (d) Fully native |
|---|---|---|---|---|
| What it is | Today's page plus a `BleSource` | **Capacitor**: today's web code inside an app shell, with native plug-ins. (A "Trusted Web Activity" is a thinner wrapper that just shows Chrome full-screen) | Flutter, React Native or Kotlin Multiplatform: one new codebase for both phones | Kotlin for Android, Swift for iPhone: two codebases |
| Background Bluetooth | No | **Yes, but only through native code we add.** The community Bluetooth plug-in covers Android, iPhone and web, MIT licence, but documents no auto-reconnect and no background use [S25]. A Trusted Web Activity has the same limits as (a) (eng.; we could not confirm how Web Bluetooth behaves inside one) | Yes on screen. For background work every framework still needs native code for Android's companion-device pieces and iPhone's state restoration (eng.) | Yes, full control |
| Auto-reconnect | Manual tap each session | Yes with a small Kotlin plug-in (section 2) | Yes, with native glue | Yes |
| Today's code reused | ~100% | **~80–90%** (est.): screens, `breath.js`, `voice.js`, `api.js`, clips | ~0–10%: screens, breath detection and voice are rewritten | ~0% |
| Skill needed | Web | Web + some Kotlin (later some Swift) | Dart or React Native **plus** some Kotlin and Swift | Kotlin and Swift, two people or one senior |
| Time to first Play release | Not a store app | 6–9 weeks after the bench prototype (est.) | 10–14 weeks (est.) | 10–14 weeks Android, the same again for iPhone (est.) |
| Long-term cost | Lowest, but capped | Low: one UI, two small native modules | Medium. One popular Flutter Bluetooth library, `flutter_blue_plus`, now needs a **paid commercial licence** for any for-profit use, including development; price not shown on the licence page [S35] | Highest |
| Main risk | Fails the founder's requirement | The phone's built-in web engine on old, cheap phones; Apple may reject apps that are only "a repackaged website" (guideline 4.2) [S8] | A rewrite before we know the product works | Same, twice |

- Not checked this round: `react-native-ble-plx`, `flutter_reactive_ble`, Kotlin Multiplatform Bluetooth libraries, Bubblewrap. They are judged above from general knowledge only. **NOT CONFIRMED.**
- Status: SINGLE SOURCE per cell where a source is given; the rest is (est.)/(eng.).

#### M-3: Recommendation
- **Bench (now → first board):** (a). Add a `BleSource` next to `SerialSource` in `web/js/sources.js`, emitting the same `{t, raw}` samples (CONTRACT B). No store, no fee, proves the firmware.
- **Pilot:** (b) with Capacitor, **Android only**, plus one native Kotlin module, the "link service", that owns pairing, reconnection, the session notification and the sync of stored breaths. Reason: it is the only path that both keeps today's working code and meets "connects automatically".
- **Scale:** keep the Capacitor shell and write the link module natively for each platform (Kotlin, then Swift). Reason: the hard, breakable part of a connected-device app is the background Bluetooth code, and that part is native in every option. The screen is one big button. Also, the scale design in `DEVICE_LIFECYCLE.md` §3.2 gives the unit its own 4G and speaker, so the phone app becomes optional; that argues against paying for two full native apps.
- **Switch rule:** move the screens to native only if, on the two weakest phones in the test matrix, the app takes more than about 4 seconds to open or the live gauge drops below about 20 frames a second (est. thresholds; measure first).

---

### 2. Bluetooth design, end to end

Plain words first, the technical name in brackets.

#### M-4: How the unit announces itself (advertising)
- The unit sends a tiny radio "I am here" message several times a second (**advertising packet**). It carries: a short name such as `SB-0007` (serial only, **never a patient name**), our own 128-bit **service ID (service UUID)** so phones can filter for SpiroBuddy units, and a few status bits in the maker-data field: battery band, "has stored breaths", "on base / off base" if the hardware can sense it, firmware major version, and a set-up flag.
- Timing (est., to be tuned on hardware): fast, about every 100–250 ms, for the first 30 s after power-on, a button press or a spirometer being placed; then slow, about every 1–2 s. Slow advertising is what makes a coin-size battery last, but it makes the phone take longer to notice the unit. iPhones in the background scan more slowly still [S16].
- Source: design choice; [S16] grade A (platform owner's documentation).
- Status: design (est.). Advertising intervals NOT CONFIRMED until measured.

#### M-5: First-time pairing by QR code, not by picking from a list
1. The nurse (lent unit) or the family (sold unit) scans the **QR sticker on the unit**. It holds the serial and a one-time **claim code** (DEVICE_LIFECYCLE §4.1).
2. The app asks Android to look only for the unit with that serial. Android's **Companion Device Manager** shows one system box, "Allow SpiroBuddy to connect to SB-0007?". This scan needs no location permission, though the phone's Location switch must be on [S14].
3. The person presses **the button on the unit**. This proves the unit is in their hands.
4. The phone and unit exchange keys (**bonding**, using **LE Secure Connections**). Both remember each other.
5. The app sends the claim code inside the now-encrypted link; the unit checks it. The server records the claim or the assignment.
- Source: [S14] grade A; [D3], [D7] for the claim-code and pairing ideas.
- Status: CONFIRMED that Companion Device Manager scans without the location permission [S13, S14]. The rest is design.

#### M-6: Bonding – use it
- **Use bonding.** It lets the two sides reconnect with encryption and no questions. It also unlocks Android's companion-device permissions.
- Caution: the simplest pairing mode ("Just Works") does not stop someone sitting in the middle [D7]. The button press plus the claim code from the QR is our out-of-band check. On each **return and wipe**, the unit deletes its bond and the app deletes its side (`disassociate()`), otherwise the next patient's phone is refused or the last patient's phone still connects [S14].
- Field trap (eng.): "bond lost on one side only" is the most common cause of "it worked yesterday". The app needs a visible **"Pair again"** path that needs no engineer.

#### M-7: Automatic reconnection on Android
| Piece | What it does for us | Limit | Source |
|---|---|---|---|
| **Auto-connect flag** (`connectGatt(autoConnect = true)`) | Android keeps a standing request: "connect whenever this unit is heard". No scanning by our app | Slow to notice (seconds to a minute or more); lost if Bluetooth is toggled on some phones (eng.) | [D4] |
| **Companion Device Manager association** | Marks the unit as "belonging" to our app. Lets the app be started from the background and start a foreground service from the background | Needs a one-time system consent box. Does not connect by itself | [S14] |
| **Device presence** (`startObservingDevicePresence`) | Android binds (starts) our `CompanionDeviceService` "when the companion device is within BLE range or connected using Bluetooth" and unbinds it when it leaves. **This is the "wake the app when the unit appears" feature** | API changed in Android 16 (old call deprecated, new `ObservingDevicePresenceRequest`); we must code both. First Android version with presence: Android 12 (eng., not stated on the page) | [S14] |
| **Foreground service, type `connectedDevice`** | Keeps the link alive during a session, with a visible notification ("Breathing session in progress") | From Android 14 every foreground service must declare a type; needs the `FOREGROUND_SERVICE_CONNECTED_DEVICE` permission and a granted Bluetooth permission; must be **declared in Play Console** | [S15] |
| **WorkManager** (a job scheduler) | Uploads the sync queue when there is internet; retries | Does not run in Doze; minimum repeat 15 minutes. Not for holding a Bluetooth link | [S23, S24] |
| **Battery-optimisation exemption** | Lets the app use network in Doze | Play allows asking for it only in listed cases. A companion app that keeps a constant link to give the unit internet is listed as acceptable; one that "only connects to a peripheral periodically to sync" is listed as **not** acceptable. We are closer to the second. **Do not rely on it** | [S24] |

- **Phones that kill apps.** dontkillmyapp.com scores makers by how hard they kill background apps: Xiaomi 5/5, Samsung 5/5, OnePlus 5/5, Huawei 5/5, Oppo 4/5, Vivo 3/5, realme 3/5 [S17]. These are the brands most Indian patients will have. The site gives per-brand settings a user can change ("autostart", "no battery restriction"); an elderly patient will not do this.
- **So the design rule is: assume the app will be killed.** Three things make that harmless: (1) the unit stores breaths and loses nothing; (2) the unit, not the phone, beeps the hourly reminder; (3) the moment the patient opens the app, or Android wakes it through device presence, it reconnects and drains the unit's store. On a **lent hub phone** we control the settings, so we switch the battery limits off once at set-up.
- Status: CONFIRMED (official Android pages) for the pieces; SINGLE SOURCE for the brand scores; field behaviour NOT CONFIRMED until tested on the matrix in section 11.

#### M-8: Automatic reconnection on iPhone (for later)
- The app declares the `bluetooth-central` background mode. iOS then wakes it when a Bluetooth event arrives; "an app has around 10 seconds to complete a task" [S16].
- A connection request to a known unit **does not time out**: "the iOS device will reconnect when the user returns home" [S16]. This is iPhone's equivalent of the auto-connect flag.
- **State preservation and restoration:** if iOS removes the app to free memory, it remembers our pending connection and relaunches the app when the unit appears, if we set a restore identifier [S16].
- Limits: background scanning is slower and repeated sightings are merged [S16]. If the user swipes the app away (force-quit), iOS generally does not relaunch it until they open it again (eng.; not on the page we read).
- Status: CONFIRMED [S16] (Apple archive document; old but still the reference). Force-quit behaviour NOT CONFIRMED.

#### M-9: The data service (a custom GATT service)
"GATT" is the menu of readable and writable values a Bluetooth device offers; each value is a "characteristic". Use two standard services and one of our own, versioned.

| Service | Characteristic | Direction | Content | Encrypted? |
|---|---|---|---|---|
| **Device Information** (standard) | model, serial, firmware version, hardware revision | read | text | no (nothing personal) |
| **Battery** (standard) | battery level 0–100% | read, notify | 1 byte | no |
| **SpiroBuddy v1** (custom, our own ID) | `live` | notify | distance samples while a session is open (M-10) | **yes** |
| | `status` | read, notify | on/off base, sensor OK, stored-record count, reset counter, current assignment number, uptime | yes |
| | `store` | notify + write | stored breath records, sent in order; the phone acknowledges the last sequence number it has saved | yes |
| | `time` | write | the phone's current time at every connect (M-12) | yes |
| | `control` | write | start/stop live stream, beep, set reminder schedule, set assignment number, wipe, enter update mode | yes, bonded only |
| **Firmware update** | the chip maker's standard update service | write | signed image (M-14) | yes |

- This is the same shape as `FUTURE_ARCHITECTURE.md` §4 (`info`, `breath_summary`, `live`, `control`). CONTRACT A stays for the USB cable. **When this is built it is a new contract; `ARCHITECTURE.md` must be updated in the same step.**
- Status: design.

#### M-10: 30 samples a second fits easily (the arithmetic)
- One sample = distance in millimetres as a 2-byte number (0–2,000 mm fits; CONTRACT A drops readings above 2,000).
- Without any tuning, one Bluetooth notification carries **20 bytes** (23-byte default packet minus 3 bytes of header) [S22].
- Phones talk to the unit once per "connection interval". The shortest is 7.5 ms on Android and 15 ms on iPhone [S22]. Choose **30–50 ms during a session**.
- At 50 ms there are 20 radio slots a second and 30 samples a second, so each notification carries 1 or 2 samples: 4 bytes of header (sequence number, sample count, 2-byte time stamp) + up to 4 bytes of samples = **8 bytes, inside the 20-byte limit**.
- Total: 30 × 2 + 20 × 4 = **140 bytes a second**. A measured figure for modern phones with larger packets switched on is about 50,000 bytes a second [S22]. We use about **0.3%** of that. Even in the worst case (20 bytes, one packet per 50 ms = 400 bytes a second) we use 35%.
- A session of 10 breaths lasting about 3 minutes sends about 140 × 180 ≈ **25 kB** over the air.
- Delay added: at most one interval (50 ms). The "too fast" warning looks at a 0.3-second window (CONTRACT C), so this is fine.
- Between sessions: stretch the interval to about 0.5–1 s, or disconnect and let the unit advertise slowly. Which one saves more battery must be measured (hardware reviewer).
- The sequence number in every packet lets the app **see lost packets** and mark a breath "incomplete" rather than score a curve with a hole.
- Status: arithmetic is ours; the limits are SINGLE SOURCE [S22] (a well-known Bluetooth engineering firm, grade B).

#### M-11: Store-and-forward – what the unit keeps when the phone is away
- **Problem nobody had written down:** to store "breath summaries", the unit would have to detect and score breaths itself. Today that logic lives only in the browser (`web/js/breath.js`). Porting it means two copies of CONTRACT C (a risk already listed in DEVICE_LIFECYCLE §10).
- **Pilot answer: the unit stores the raw curve, not the score.** A simple trigger ("disc is above the rest position") starts recording; the unit saves the 2-byte samples until the disc is back down. When the phone returns, it replays the samples through the **existing** `breath.js`. One copy of the logic, and the stored data can be re-scored if the model improves.
- Size (est.): a breath lasts about 8.4 s in the contract example; with a 1-second margin, 10 s × 30 samples × 2 bytes = 600 bytes, plus a 12-byte header (sequence number, assignment number, reset counter, uptime) ≈ **612 bytes a breath**. At 14 sessions × 10 breaths = 140 breaths a day: **≈ 86 kB a day, ≈ 600 kB for 7 days**. That fits in the spare flash of either chip family (hardware reviewer to confirm the part).
- Sync time (est.): at a slow 10 kB a second, one day takes about 9 s and a full week about 60 s. At the untuned worst case (about 670 bytes a second) a day takes about 2 minutes, so the app should ask for larger packets (**MTU** and **data length extension**) before a sync [S22].
- Rules: the store is a ring (oldest overwritten first, with a "records lost" counter the nurse can see); every record has a **sequence number that only goes up**; the phone acknowledges the highest number it has safely written to its own database, and only then may the unit erase; the server ignores repeats using `(unit, reset counter, sequence)`, as `FUTURE_ARCHITECTURE.md` §4 already says.
- Stored breaths get **no voice coaching** (nobody was listening). The app should say so kindly on the next open: "You did 6 breaths while your phone was away. Well done."
- Status: design (est.). No hardware has run it.

#### M-12: Time-stamping when the unit has no clock
- The unit counts milliseconds since it was switched on (**uptime**) and keeps a **reset counter** that goes up by one at every restart.
- At every connect the phone writes its own time into `time`. The app then knows: real time of a record = phone time now − (unit uptime now − uptime in the record). This is exact as long as the reset counter is unchanged.
- If the unit restarted while away (battery died), records from before the restart have no anchor. They are kept in order, placed just before the first anchored record, and marked **"time estimated"** (already a rule in DEVICE_LIFECYCLE §5.6). Never raise a missed-session alert from estimated times alone.
- Use the phone's network time in UTC. Convert to India time only for display. Guard against a wrong phone clock by comparing with the server's time at upload and storing both.
- Status: design.

#### M-13: Security in six plain rules
1. **LE Secure Connections** pairing with bonding; our characteristics need an encrypted, bonded link. Only the standard device-information and battery values are open.
2. **A per-unit key**, put in at manufacture, signs each batch of stored breaths, so a fake unit cannot post breaths (`FUTURE_ARCHITECTURE.md` §4; DEVICE_LIFECYCLE §7).
3. **No patient name on, or in, the unit.** The advertised name is the serial only.
4. The QR holds a **claim code**; scanning a photo of someone else's QR is useless without pressing that unit's button.
5. Commands that change things (wipe, set assignment, update mode) are accepted only from a bonded phone **and** carry a short-lived token from our server.
6. The unit's storage is encrypted and firmware is accepted only if signed [#201].
- Status: design; the weakness of "Just Works" is CONFIRMED [D7].

#### M-14: Firmware updates over Bluetooth
- **Two slots.** The unit keeps the running firmware and downloads the new one into a second slot. On restart a small, fixed program (the **bootloader**) checks our **digital signature**; if the new firmware fails its self-test, the bootloader goes back to the old one.
- ESP32 family: Espressif's own update system with Secure Boot v2, roll-back and anti-roll-back [#201]. nRF52 family: the **MCUboot** bootloader with updates sent over Bluetooth by the **MCUmgr / SMP** service; Nordic's documentation has pages for signature keys, image versions, downgrade protection and A/B updates [S33]. (We could read only the page index of the Nordic docs, so details are NOT CONFIRMED.)
- Size check (est.): a 1 MB image at 10–50 kB a second takes about 20–100 s on a tuned link, and much longer on an untuned one. iPhone gives a background app only about 10 s per wake [S16], so **updates run only with the app open, the unit on its charger or above 50% battery, and never during a session**.
- Status: SINGLE SOURCE per chip family; never tried.

---

### 3. "Is the unit on?" – from the app's side

#### M-15: One heartbeat answers the founder's question
- The app never asks the unit "are you on?". It listens. **If the phone hears the unit's advertising, the unit is on.** If it does not, the app cannot tell "off" from "far away" from "flat battery", so the message to the patient covers all three: "Put your breathing unit close to the phone and press its button."
- The unit's own side (a power button, a light, wake-on-lift, sleep) belongs to the hardware review. The app needs three things from it: a button that restarts fast advertising, one status light, and the status bits listed in M-4.

#### M-16: Every state, what the patient gets, what the nurse sees

Patient rule: one picture, one sentence in large text, the same sentence spoken, one button at most. No word such as "Bluetooth", "pair" or "firmware" unless the phone's own settings screen is about to show it.

| # | State | How the app detects it | What the patient sees and hears | Nurse dashboard |
|---|---|---|---|---|
| 1 | Bluetooth is off on the phone | The phone reports the radio state | Picture of the phone with a switch. "Your phone's wireless link is off. Tap here to turn it on." One button opens the system prompt | "Phone link off" on the unit badge; no alert for 1 hour |
| 2 | Permission not granted | Permission check at start-up | "SpiroBuddy needs your permission to find the breathing unit. Tap Allow on the next screen." If refused twice, a picture guide to Settings and a "Call my nurse" button | "App set-up not finished" |
| 3 | Unit not found | No advertising heard for 20 s (est.) | Picture of the unit. "I cannot find your breathing unit. Keep it close and press its button." After 2 minutes: "It may need charging." | "Unit not seen for X h", shown apart from "patient missed sessions" |
| 4 | Unit heard but not connected | Advertising seen, connection not up yet | A gentle "Connecting…" for up to 10 s, no sound. Then silent retry. After 3 failures: "Please press the button on your unit again." | "Connecting problems: N today" (a support signal) |
| 5 | Connected | Link up, encrypted, `status` read | Green tick. "Ready. Press Start." | "Seen just now", battery %, signal strength band |
| 6 | Spirometer on the base or not | Status bit, **if** the hardware can sense it (question for the hardware reviewer) | "Please stand the spirometer on the unit." | Counted as a set-up problem, not a missed session |
| 7 | Low battery | Battery characteristic below 20% (est.), or the bits in the advertising | "Please charge your unit tonight." Below 10%: say it before the session, and still allow the session | Battery % in amber or red; "low for 2 days" list |
| 8 | Unit assigned to a different patient, or to nobody | After connecting, the app asks the server "whose settings do I load for SB-0007?" (DEVICE_LIFECYCLE §5.3) | **No coaching and no saving.** "This unit is not set up for you yet. Please call your nurse." One call button | Breaths go to quarantine; "SB-0007 used while unassigned" |
| 9 | Firmware out of date | Firmware version compared with the server's minimum | Nothing, unless the update is required. Then: "Your unit needs a 2-minute update. Keep it next to the phone." Progress bar, spoken "Done." | Firmware version per unit; "update pending" count |
| 10 | Phone has no internet | Network check | Nothing changes. Coaching works from the cached clips. Small cloud icon with a line through it | "Last upload X h ago" |
| 11 | Stored breaths are syncing | `status` shows a count above zero | "Collecting your earlier breaths…" then the kind summary in M-11 | Breaths appear with a "synced later" mark |
| 12 | Sensor fault | Error flag in `status` (today's `E,` line) | "Your unit has a problem. Please call your nurse." | Unit state → FAULTY |

- **"Last seen"** on the nurse side is the time of the last successful contact between any phone and the unit, sent to the server with battery, firmware version and signal strength (**RSSI**). Already asked for in `FUTURE_ARCHITECTURE.md` §4 ("Telemetry").
- Status: design.

---

### 4. Permissions and platform rules that trip teams up

#### M-17: Android Bluetooth permissions
- Android 12 and later: `BLUETOOTH_SCAN` and `BLUETOOTH_CONNECT` are asked at run time; the user sees one box, "Nearby devices" [S13].
- Add the **`neverForLocation`** flag to `BLUETOOTH_SCAN`. It tells Android we never use Bluetooth to work out location, so no location permission is needed. Side effect: "some BLE beacons are filtered from the scan results" [S13]. Our unit is not a beacon; test that it still appears.
- Android 11 and older: the app needs `ACCESS_FINE_LOCATION` to scan, and background location to scan from a service on Android 10–11 [S13]. Asking an elderly patient for "location" is confusing. **Using Companion Device Manager avoids it** (scan without the location permission from Android 8; the Location switch must still be on) [S13, S14].
- Status: CONFIRMED [S13, S14].

#### M-18: Foreground services, notifications, alarms, Doze
- Every foreground service needs a declared type from Android 14; ours is `connectedDevice`, and it must be declared and justified in **Play Console → Policy → App content** [S15]. Teams usually discover this at first upload.
- From Android 15, a data-sync foreground service may not be started at phone boot [S15]. Use device presence instead.
- **Notification permission** must be asked at run time from Android 13 (eng.; not read this round). If refused, reminders are silent: one more reason the unit should beep.
- **Exact alarms:** on Android 14, `SCHEDULE_EXACT_ALARM` is "denied by default" for newly installed apps. `USE_EXACT_ALARM` is granted at install but Play allows it only for apps that qualify under its policy (calendar and alarm-clock apps are the examples) [S23]. Our reading: a breathing-exercise reminder probably does not qualify; **confirm before using it**.
- **Doze** (Android's deep sleep): network is cut, WorkManager jobs do not run, normal alarms wait. `setAndAllowWhileIdle()` still fires, at most once per nine minutes per app [S24]. An hourly reminder that may be a few minutes late is fine with this inexact alarm and needs no special permission.
- Status: CONFIRMED [S15, S23, S24], except the Android 13 notification rule (eng.).

#### M-19: iPhone rules
- `Info.plist` needs a plain-language reason string for Bluetooth (`NSBluetoothAlwaysUsageDescription`) and the `bluetooth-central` background mode [S16; the key name is eng.]. Apple's review rule 2.5.4 says background services may be used only for their intended purpose [S8].
- Bluetooth does not work in the iPhone simulator; a real iPhone is needed for every test [S25].
- Status: CONFIRMED for the background mode; key name (eng.).

#### M-20: Play's yearly "target API level" deadline
- From **31 Aug 2026**, new apps and updates must target **Android 16 (API level 36)**; an extension to 1 Nov 2026 can be requested. Existing apps must target at least Android 15 (API 35) to stay visible to new users on newer phones [S3].
- The pattern repeats every year at the end of August. Plan one to two weeks of work each summer (est.) to raise the target and re-test Bluetooth, because each Android version changes background rules.
- Status: CONFIRMED [S3].

---

### 5. Publishing: every step and every fee

#### M-21: Google Play – steps, fees, rules
| Step | Rule | Fee | Source |
|---|---|---|---|
| Developer account | "US$25 one-time registration fee"; card must not be prepaid; holder must be 18 or older; a government ID and card "under your legal name" may be asked; not refunded if details are invalid | **US$25 ≈ ₹2,400, once** | [S1] |
| Account type | Personal or Organisation. An organisation **must** have a D-U-N-S number: "You will not be able to create a developer account for an organization without one." Organisation listings show legal name, address, developer email and phone publicly; personal ones show legal name, country and email | – | [S12] |
| Does a health app need an organisation account? | We believe Play requires it for health apps but **did not find it on the pages we opened. NOT CONFIRMED.** Check in Play Console before paying | – | – |
| D-U-N-S number | A nine-digit company identity number from Dun & Bradstreet. Apple says it is free and takes up to 5 business days, plus 2 for Apple to receive it [S11]. Indian consultancy pages say the standard route can take up to 30 business days and charge ₹3,999–₹10,000 for help (**snippets**, grade C). **It needs a registered legal entity, which the team does not have** | Free from D&B; ₹0–₹10,000 if a consultant is used (snippet) | [S11], snippets |
| Device check | New personal accounts must show they have a real Android phone, using the Play Console phone app | – | [S1] |
| Closed test (personal accounts only) | Accounts created after 13 Nov 2023 "must run a closed test … with a minimum of 12 testers" who have been "opted in continuously for at least 14 days" before applying for public release; review of that application "usually takes seven days or less" | – | [S2] |
| Health apps declaration | Every app must complete it, "even … apps that do not offer any health features". Categories include "Physical Therapy and Rehabilitation" and "Diseases and Conditions Management". "Please select 'Medical Device Apps' if your app is regulated." **Private apps are exempt** | – | [S4] |
| Health content and services policy | Non-device health apps need a disclaimer in the description that the app is "not a medical device and does not diagnose, treat, cure, or prevent any medical condition". Apps must "remind users to consult a healthcare professional". Apps that need hardware must "clearly disclose these external hardware requirements in the app description". Regulated apps are labelled "Medical Device" and "must provide proof of approval, clearance or certification … upon request" | – | [S18] |
| Privacy policy | A public web page (not a PDF), linked in Play Console and inside the app | hosting only | [S18] |
| Account and data deletion | If the app lets people create an account: an in-app path **and** a web link to delete the account and its data; retention must be explained | – | [S19] |
| Data safety form, target audience, content rating, app signing | All required in Play Console before release. Not opened this round. **NOT CONFIRMED in detail**; no fee that we know of | ₹0 (eng.) | – |
| Target API level | M-20 | – | [S3] |
| Service fee | Charged on "apps and in-app products sold through Google Play's billing system": 15% of the first US$1 million a year, 30% above, 15% on subscriptions (rates for markets outside the US, UK, EEA, Japan, Australia). Our reading: **a free app paid for by hospitals under a contract outside the app owes nothing** | 0% in the hospital-pays model | [S5] |
| Review time | "up to seven days or longer in exceptional cases" | – | [S30] |

- Status: CONFIRMED for every row with a source (official Google pages, grade A as the platform's own rules).

#### M-22: Apple App Store – steps, fees, rules
| Step | Rule | Fee | Source |
|---|---|---|---|
| Apple Developer Program | "99 USD per membership year or in local currency where available". One forum post reports ₹8,700 a year in India (**snippet**, not confirmed) | **US$99 ≈ ₹9,500 every year** | [S9, S10] |
| Individual or organisation | Individual: your personal legal name is shown as the seller. Organisation: must be a legal entity, **D-U-N-S number required**, a work email on the organisation's domain and a real public website; trade names are not accepted | – | [S10] |
| Fee waiver | For a nonprofit, an accredited educational institution or a government body that is a legal entity and sells nothing through its apps; not for individuals. No country list is given, so **India is not confirmed**. A college could ask; a student team cannot | ₹0 if granted | [S7] |
| Mac and Xcode | iPhone apps are built with Apple's Xcode, which runs on a Mac (eng.). A cloud build service avoids buying one: Codemagic gives 500 free Mac build minutes a month, then US$0.095 (≈ ₹9) a minute [S31]. A real iPhone is still needed for Bluetooth tests [S25] | ₹0–a few hundred rupees a month at our volume (est.) | [S31] |
| TestFlight (Apple's test channel) | Up to 100 internal testers and 10,000 external testers; the first external build must pass App Review | included | [S27] |
| Health data (guideline 5.1.3) | No use of health data for advertising; "may not store personal health information in iCloud"; research apps need consent and, on request, proof of ethics-board approval | – | [S8] |
| Medical apps (guideline 1.4.1) | "may be reviewed with greater scrutiny"; apps "must clearly disclose data and methodology to support accuracy claims relating to health measurements"; "should remind users to check with a doctor"; "If your medical app has received regulatory clearance, please submit a link" | – | [S8] |
| Hardware apps (3.1.4) and payment (3.1.3) | Features that depend on specific hardware may be unlocked without in-app purchase. Apps "only sold directly by you to organizations" need not use in-app purchase (3.1.3(c)); a free companion to a paid web tool is allowed if there is no purchasing in the app (3.1.3(f)). Our reading: **no Apple commission in the hospital-pays model** | 0% | [S8] |
| Account deletion (5.1.1(v)) | "If your app supports account creation, you must also offer account deletion within the app" | – | [S8] |
| HealthKit | **Not needed.** We do not read or write Apple Health. Leaving it out avoids extra rules | – | [S8] |
| Privacy "nutrition label" | Required in App Store Connect (eng.; not opened). **NOT CONFIRMED in detail** | ₹0 | – |
| Review time | "at least 50% of submissions in less than 24 hours and 90% in less than 48 hours" | – | [S29] |

#### M-23: Ways to avoid the public stores during the pilot
| Route | How | Limits | Source |
|---|---|---|---|
| **Installable web app** (today) | Open a link, "Add to home screen" | No background Bluetooth (M-1) | code |
| **Direct install file (APK)** on hub phones we own | Copy the file and install; switch "install unknown apps" on once | No automatic updates unless we add them; Play Protect warnings on personal phones (eng.) | – |
| **Managed Google Play private app** | The hospital, or we, run Android's device-management console; the app is visible only to chosen organisations, "available … within a few minutes", up to 1,000 organisations per app; **exempt from the Health declaration and from the account-deletion rule** | Still needs a Play developer account and its fee; needs managed phones | [S26, S4, S19] |
| **Play closed testing** | Invite testers by email list | Still under Play's policies; this is also the compulsory 14-day test for personal accounts | [S2] |
| **TestFlight** (iPhone) | Up to 10,000 outside testers | First build is reviewed; builds expire after a set number of days (number not on the page we read) | [S27] |
| **Apple custom apps** | A private app offered to named organisations through Apple Business Manager | Goes through review; needs the paid programme | [S28] |

- **Recommendation for the pilot:** hub phones we own, with the app installed directly or as a managed private app. No public listing until the regulatory position is settled (M-26).

#### M-24: Fee table
| Item | Google Play | Apple | One-time or yearly | ₹ (at ₹96 = US$1) | Source |
|---|---|---|---|---|---|
| Developer account | US$25 | – | One-time | ≈ ₹2,400 | [S1] |
| Developer programme | – | US$99 | **Yearly** | ≈ ₹9,500 (₹8,700 reported, snippet) | [S9, S10] |
| Enterprise programme (in-house apps only; not for us) | – | US$299 | Yearly | ≈ ₹28,700 | [S10] |
| D-U-N-S number | needed for organisation | needed for organisation | One-time | ₹0 from D&B [S11]; ₹3,999–₹10,000 if a consultant is used (snippet) | [S11, S12] |
| Fee waiver | none found | nonprofit / education / government only | – | – | [S7] |
| Closed test before launch | 12 testers × 14 days (personal accounts) | not required | One-time per app | ₹0 | [S2] |
| Commission, hospital-pays model | 0% | 0% | – | ₹0 | [S5, S8] |
| Commission, if families buy inside the app | 15% of first US$1M; 15% on subscriptions | not read this round | Ongoing | – | [S5] |
| Build machine | any PC | a Mac, or cloud: 500 free min/month then US$0.095/min | Ongoing | ₹0 to ≈ ₹9 a minute | [S31] |
| App signing | Play App Signing (eng.) | certificates included in the programme (eng.) | – | ₹0 | – |
| Privacy-policy page, support email | needed | needed | Yearly | domain and hosting only (cost agent) | [S18] |
| Review time | up to 7 days or longer | 90% within 48 hours | – | – | [S29, S30] |

**Total store fees for year 1, both stores: about ₹11,900. Each later year: about ₹9,500 (Apple only).** Android only: about ₹2,400 once.

---

### 6. Do we even need iPhone at first?

#### M-25: No. Android first, with a decision rule
- **Share of phones in use in India, Sept 2026:** Android **93.89%**, iOS **6.05%** [S20]. This counts web traffic by phone type, so it leans towards people who browse more; among older and lower-income users the iPhone share is likely lower still (est.).
- Most older Indians do not own a smartphone at all [#65, #184], so the lent hub phone, which is Android, is the main route anyway (DEVICE_LIFECYCLE §3.2).
- iPhone costs: ≈ ₹9,500 a year, a Mac or cloud builds, at least one test iPhone, a Swift Bluetooth module, and 6–9 weeks of work (est.).
- **Decision rule:** at enrolment the nurse already asks "Is there an Android smartphone in the home?". Add one tick-box: "iPhone only". Build the iPhone app when **either** more than 15% of enrolled households over a full pilot month are iPhone-only and refuse the hub kit, **or** a paying hospital writes it into a contract (est. threshold; adjust with data).
- Status: CONFIRMED for the share [S20]; the rule is ours.

---

### 7. Regulatory status of the app itself

#### M-26: The store listing forces the "medical device or not" decision
- Not repeated here: B4-1 (a unit that shows a body measurement in units is a "measuring" device), B4-2 (software inside or with a device takes the device's class), B4-8 (alerts and disease mentions take software out of "wellness"), B4-20 (the 1954 advertising law). Read those first.
- **What is new:** both stores make us choose in public. Play: either declare "Medical Device Apps" (and hold proof "upon request"), or print "not a medical device and does not diagnose, treat, cure, or prevent any medical condition" in the description [S4, S18]. Apple: disclose the method behind any accuracy claim, and give a link to regulatory clearance if there is one [S8].
- Our reading: if CDSCO treats the unit plus app as a device (B4-1, B4-2), the "not a medical device" sentence would be untrue for the app that drives it. **Do not publish a public listing until a regulatory consultant has answered this.** A private pilot app is exempt from Play's declaration [S4], which is why M-23 recommends it.
- A pilot that is a study on people also triggers Apple's research rules (consent; ethics approval "upon request") if it runs through TestFlight or the App Store [S8]. See B4-6 and B4-7.
- Status: CONFIRMED for the store rules; the conclusion is our reading, not advice.

#### M-27: Listing wording that stays inside "coaching, not diagnosis"
- **Use:** "Voice coaching for the breathing exercise your hospital taught you." · "Works only with the SpiroBuddy base unit and an incentive spirometer supplied by your hospital." (the hardware disclosure Play requires [S18]) · "Shows how many exercises you did today." · "Does not diagnose. Always follow your doctor's and nurse's advice." (both stores ask for this reminder [S8, S18]) · "If you feel unwell, contact your nurse or call 112."
- **Avoid:** "prevents pneumonia", "improves lung function", "detects", "monitors your lungs", "clinically proven", "accurate lung volume", star-ratings of health. The 1954 advertising law applies to store text and screenshots just as to a poster (B4-20). Avoid volume numbers in screenshots unless the accuracy method is published (Apple 1.4.1 [S8]).
- Choose the store category with the consultant: "Health & Fitness" suits a coaching claim; "Medical" invites the closer review Apple describes [S8].
- Status: our drafting; confirm with the consultant.

---

### 8. Accessibility and elderly-first rules

#### M-28: Design rules for the patient app
- **Text:** 24 px default, never below 18 px (already in `FUTURE_ARCHITECTURE.md` §5). Respect the phone's own font-size setting up to 200% without clipping.
- **Tap targets:** at least 48 × 48 dp on Android and 44 × 44 pt on iPhone; for this audience use 64 dp or more for the one main button (platform guidelines, eng.; not opened this round).
- **Screen readers:** every button and picture labelled for TalkBack and VoiceOver. The live gauge must also announce progress in words, or the app is unusable without sight.
- **Contrast:** at least 4.5 : 1 for text (WCAG AA, eng.); never signal by colour alone (tick and cross shapes as well as green and red).
- **Language without typing:** chosen by the nurse on the patient record and pulled down automatically; on the phone, a row of big buttons each written in its own script, with a spoken sample. Never a drop-down in English.
- **Offline:** coaching, scoring and voice must work with no internet. Clips for the patient's language are downloaded at set-up, not on first use.
- **One action per screen. No typing. No passwords.** The patient never logs in (DEVICE_LIFECYCLE §6).
- **Sound:** check the media volume at session start and say "Please turn up the sound" with a picture; lock the volume high on hub phones.
- Status: design; sizes (eng.).

#### M-29: Which Android versions, and what share that covers
- India, Sept 2026 (share of Android web traffic): Android 16 38.78%, 15 19.85%, 14 10.03%, 13 10.14%, 12 7.23%, 11 6.75% [S21]. So **Android 12 and later ≈ 86%; Android 11 and later ≈ 93%**; the rest (about 7%) is Android 10 and older, not itemised.
- Chrome stopped updating on Android 8 and 9 in August 2025; Chrome 139 needs Android 10 (**snippet**). That matters for the web-app route and for the phone's built-in web engine.
- **Recommendation:** install floor **Android 8 (API 26)**, because Companion Device Manager starts there [S13] and the existing plan says Android 8+; **support promise and test matrix: Android 11 and later**; automatic wake-up (device presence) only on Android 12 and later, with "open the app" as the fallback on older phones. Confirm that the chosen Capacitor version supports the floor (not checked).
- Lent hub phones: buy one model, Android 14 or later, and freeze it.
- Status: CONFIRMED for the shares [S21] (with the web-traffic caveat); the floor is our choice.

#### M-30: App size and data use
- **App size:** target ≤ 30 MB to download (existing plan). The web code is small; the voice clips dominate: about 3 MB per language uncompressed (est., DEVICE_LIFECYCLE §3.4). Ship one language in the app and fetch others on demand.
- **Mobile data per day (computed from the design):** 140 breaths × about 250 bytes of features ≈ 35 kB; with request overhead about 50–100 kB. If raw curves are also uploaded for model training: 140 × 250 samples × about 6 bytes ≈ 210 kB before compression. **Under 0.5 MB a day (est.)**, small enough for the cheapest data pack. Firmware updates (about 1 MB) should wait for Wi-Fi or be rare.
- **Memory:** phones with 2–3 GB of RAM kill background apps sooner; another reason for M-7's "assume the app is killed" rule.
- Status: (est.).

---

### 9. Offline-first data in the app

#### M-31: Local store, sync queue, conflict rules
- **Local database:** SQLite on the phone. In the Capacitor path, a SQLite plug-in; Room (Android) or Drift (Flutter) are the equivalents in other paths. Browser storage alone is not safe enough: the system may clear it.
- **Sync queue (outbox):** every session and breath is written to the phone's database first, with an ID made on the phone, and only then sent. It stays in the queue until the server says "accepted" or "duplicate".
- **Idempotent** means "safe to send twice": the server recognises a repeat by its ID and does not store it again. Use the unit's `(serial, reset counter, sequence number)` as the ID for device breaths and a random ID for app-made records, plus the `Idempotency-Key` header already planned (`FUTURE_ARCHITECTURE.md` §5).
- **Conflict rules:** the server wins for care-plan fields (target, hold time, language, schedule); the device wins for measurements (already decided). Measurements are never edited, only added, so real conflicts are rare.
- **What is on the phone, and for how long:** the queue (deleted on confirmed upload); the last 7 days of the patient's own results for the "today" screen; the patient's first name, language and target; the unit's serial and bond; a token for the household or, on a hub phone, for the **unit** not a person. Nothing older than 7 days after upload (est. policy).
- **Encryption at rest:** modern Android encrypts app storage with the phone's lock by default (eng.); add database encryption (SQLCipher or the platform's encrypted storage) with the key in the Android Keystore / iOS Keychain, switch off cloud backup for the app's data, and never write health data to iCloud (Apple 5.1.3(ii) [S8]).
- Status: design, in line with `FUTURE_ARCHITECTURE.md` §5.

#### M-32: When a unit is re-assigned while a phone still holds old data
1. Every record on the phone carries the **assignment number** it was made under.
2. On every connect, and every time the app opens with internet, the app asks the server for the open assignment of the unit.
3. If the assignment has changed or closed: finish uploading what is queued under the **old** number (the server files it under the old patient, inside the old time window), then **erase the local cache, the first name and the token**, and show state 8 in M-16.
4. If the phone cannot reach the server, it may keep coaching for the assignment it last knew for a limited time (est. 24 hours), still storing under that number. The server's time window decides in the end (DEVICE_LIFECYCLE §5.5).
5. A family phone that leaves with the old patient simply stops: the unit's bond was wiped at return, so the phone can no longer connect, and the app says "Your loan has ended. Thank you."
- Status: design.

---

### 10. Notifications and reminders

#### M-33: The unit is the primary reminder; the phone is the backup
- **Primary: the unit beeps and blinks on schedule.** The schedule and quiet hours are sent to the unit at each connect. The unit does not suffer from Doze, killed apps or refused notification permissions. It needs only a rough clock (M-12).
- **Backup: a local alarm on the phone**, set with the inexact `setAndAllowWhileIdle()`, which fires in Doze at most once per nine minutes per app [S24]. No exact-alarm permission needed (M-18).
- **Push messages** (Firebase Cloud Messaging on Android, APNs on iPhone) are for things only the server knows: a nurse's change of target, a family "cheer", an urgent update notice. High-priority messages wake the app and should be used only "for messages that result in a notification" [S24]. Never depend on push for the hourly reminder (already the rule in `FUTURE_ARCHITECTURE.md` §5).
- **WhatsApp stays the family channel** and the missed-session channel. Nothing here changes `docs/COMMS.md`.
- Status: CONFIRMED for the Android limits; the rest is design.

---

### 11. Testing and release

#### M-34: A device test matrix for India
Aim: the brands that kill apps hardest [S17], the oldest supported Android, the weakest memory, and one clean reference phone. Prices are 2026 web listings seen in search results only (**snippets**, grade C); models and Android versions must be checked on the day of purchase. Second-hand phones are the cheap way to cover old Android versions.

| # | Phone (class) | Why it is in the matrix | Price seen (snippet) |
|---|---|---|---|
| 1 | Xiaomi Redmi A5 (3 GB, Android 15 Go-class) | Cheapest new Xiaomi; aggressive app-killing; low memory | ₹6,499 at launch; ₹10,990 on one later listing |
| 2 | Xiaomi Redmi 14C | Very common budget Xiaomi | ₹8,499 |
| 3 | Poco C75 5G (HyperOS, Android 14) | Xiaomi's other skin | ₹8,990–₹10,999 |
| 4 | Samsung Galaxy M06 5G or F06 5G (Android 15) | Samsung One UI, scored 5/5 for killing apps | ₹9,999–₹13,999 |
| 5 | Samsung Galaxy A06 | Samsung's cheapest line | ₹9,299 |
| 6 | Realme C65 5G | realme UI | ₹9,499 |
| 7 | Vivo Y19s 5G (Funtouch OS 15) | Vivo's skin | ₹10,999 at launch |
| 8 | An Oppo A-series budget phone | ColorOS, scored 4/5 | not found |
| 9 | A Lava, Itel or Tecno phone under ₹8,000 | Indian and Transsion brands, common outside metros; unusual chipsets | not found |
| 10 | A second-hand phone on Android 11 and one on Android 12 | The floor of our support promise | not sourced |
| 11 | A Google Pixel or Motorola (near-stock Android) | Reference: if it fails here, the bug is ours | not sourced |

Budget for 8–10 phones: **about ₹70,000–₹1,00,000 (est., from the snippet prices above)**. The same model chosen as the hub phone must be in the matrix.

#### M-35: Tools, tests and safe release
- **Bluetooth tools:** nRF Connect for Mobile (free app from Nordic; lets a tester read and write our characteristics by hand; eng.). A **Bluetooth sniffer** records the radio conversation: a Nordic nRF52840 dongle runs Nordic's sniffer firmware with Wireshark; one India listing showed ₹2,900 in July 2026 (**snippet**). It listens to one channel at a time, so it can miss packets (snippet).
- **Automated tests:** (1) feed recorded breath curves through `breath.js` and compare with expected features: the same test set the firmware must pass later; (2) a fake unit (a second phone or a dev board running a script) that drops the link, restarts, sends repeats and sends out-of-order records; (3) Android's own Doze and standby test commands [S24]; (4) kill-and-recover: force-stop the app mid-session and check nothing is lost.
- **Field checks no simulator covers:** two phones near one unit, one phone with two units, Bluetooth switched off mid-session, phone restart, phone clock changed, 48 hours without the app, flat unit battery.
- **Staged roll-out:** Play lets a release go to a small share of users first (eng.; not opened). Use internal → closed → 10% → 100%.
- **Crash reporting and analytics with no personal data:** send only event names and counts (connect time, failed connects, sync size, app version, phone model, Android version), keyed by a random install ID, never the patient ID, name or breath values. Whatever SDK is used must be declared in the Data safety form and privacy label.
- **Firmware in the field:** signed images; the unit's battery above 50% or on charge; the app open and near; one unit, then the team's units, then 10% of the fleet, then all (`FUTURE_ARCHITECTURE.md` §4); automatic roll-back if the self-test fails; **the app must keep working with the previous firmware version** for at least one full roll-out; a server-side "stop" switch and a "minimum safe version" the app enforces (state 9 in M-16).
- Status: tool prices are snippets; the rest is design.

---

### 12. Effort, team and cost

#### M-36: Phased plan (all figures are estimates for one competent developer; nothing has been built)
| Phase | What is delivered | Weeks | Skills | One-time cost | Yearly cost |
|---|---|---|---|---|---|
| **0. Bench prototype** | Firmware speaks the v1 Bluetooth service; `BleSource` in the web app (Android Chrome); live curve on screen from a real board | App side 1–2; firmware 2–3 (hardware plan) | Web; embedded C | 2 dev boards (hardware budget); sniffer ≈ ₹2,900 (snippet); 2 test phones ≈ ₹15,000–₹20,000 (est.) | ₹0 |
| **1. Pilot Android app** | Capacitor shell; Kotlin link service (QR pairing, bonding, auto-connect, presence wake-up, session notification); on-unit store and sync; local database and upload queue; all 12 states with voice; unit-driven reminders; private install on hub phones | 6–9 | Web + Kotlin/Android Bluetooth | Rest of the test matrix ≈ ₹50,000–₹80,000 (est.); Play account ≈ ₹2,400 if the managed-private route is used | ₹0 |
| **2. Public Play release** | Organisation account (after company + D-U-N-S), or personal account + 12 testers × 14 days; declarations; privacy policy and deletion pages; listing in English and Hindi at least; staged roll-out; crash reporting | 3–4, of which 2–3 is waiting | Same, plus someone who owns policy forms | ≈ ₹2,400 if not yet paid; D-U-N-S ₹0–₹10,000 (snippet) | Target-API update each August: 1–2 weeks of work |
| **3. iPhone app** | Swift link module with state restoration; Capacitor iOS build; TestFlight; App Review | 6–9 | Swift/Core Bluetooth | A test iPhone (not priced); Mac or cloud builds | Apple ≈ ₹9,500; cloud builds ₹0 to a few hundred rupees a month (est.) [S31] |
| **Ongoing** | Bug fixes for new phone models, yearly platform updates, firmware compatibility | about 1 day a week (est.) | – | – | Stores ≈ ₹9,500 (Apple only) |

- **Team:** one developer who knows web and Android Bluetooth can do phases 0–2. Add Swift for phase 3. The firmware developer and the app developer must share one written protocol (M-9) and one set of test curves from the first day.
- **The biggest schedule risk is not code:** it is the wait for a company, a D-U-N-S number, account verification and the 14-day test.
- Status: (est.) throughout.

---

### 13. What we missed

#### M-37: Checklist a first connected-device team usually forgets
**Accounts and ownership**
1. **No company, so no organisation store account and no D-U-N-S number.** A personal account shows a student's legal name as the seller and (on Play) triggers the 12-tester, 14-day rule [S2, S10, S12].
2. **Account ownership must sit with the company**, on a shared company email with two owners and two-step sign-in, not on one student's personal Gmail or Apple ID.
3. **The app's package ID (Android) and bundle ID (iPhone) are permanent**; the app name can change, the ID cannot (eng.). Choose it under a domain we own.
4. **The signing key.** Lose the upload key and you cannot update the app without a reset by the store (eng.). Store it in a password manager with two keepers. The same applies, more severely, to the **firmware signing key**: lose it and no unit in the field can ever be updated.
5. Apple needs a work email on our own domain and a real website for an organisation [S10]. We have neither.

**Store rules**
6. **Delete my account and data**: in-app and on a web page, both stores [S8, S19].
7. A **privacy policy web page** (not a PDF) that names every data type, in the app and in the listing [S18].
8. A **support email and phone line** that someone answers; Play shows an organisation's phone publicly [S12].
9. The **health declaration** and the "medical device or not" wording (M-26).
10. The hardware requirement must be stated in the listing; reviewers cannot test without a unit. Give App Review a **demo mode and a video**, or expect rejection (eng.). Today's simulator is exactly this demo mode; keep it.
11. **Listing localisation**: title, description and screenshots per language; a Hindi-speaking patient searching in Hindi must find it.
12. The yearly target-API deadline every 31 August [S3].

**Bluetooth and radio**
13. **Bluetooth SIG listing.** Products sold with Bluetooth normally have to be listed with the Bluetooth SIG (the standards body), which involves a membership and a fee per product (eng.). **We did not check the amount or whether a pre-certified module reduces it. NOT CONFIRMED. Flag for the hardware and cost agents.** This is separate from India's WPC approval (B4-11).
14. Phones that kill background apps (M-7), and the support burden of "autostart" settings.
15. Bond lost on one side only; a "Pair again" path the nurse can run.
16. **Two phones near one unit** (family phone and hub phone): the unit accepts one bonded phone at a time; the second gets a clear message.
17. **One phone with several units in a ward** (the nurse's tablet): always choose by QR scan, never "the nearest"; show the serial in large text.
18. Location switch must be on for pairing on many Android versions even though no location permission is asked [S14, S25]; patients turn it off.

**Time and data**
19. Clock changes on the phone, a unit with no clock, restarts, and midnight boundaries; store UTC, show India time (M-12).
20. Repeats and out-of-order uploads (M-31); old data on a re-assigned phone (M-32).
21. A full unit store: what is overwritten and how the nurse knows.
22. The app is updated but the firmware is not, and the other way round: version the protocol and support one version back.

**Safety and operations**
23. **A recalled or faulty firmware**: a server "stop" switch, a minimum safe version, and a way to roll back a fleet (M-35).
24. The safety button must work with no unit, no internet and no login (it does today; keep it so in the native shell, including the `tel:112` link).
25. Battery warnings, charging habits, and a unit left on charge for days.
26. Hub phones: SIM data running out, phone lost, phone used for other things, the lock-to-one-app set-up, reset at return (DEVICE_LIFECYCLE §9 item 10).
27. Accessibility testing with real older users and a screen reader, not only by the team.
28. A status page or at least a WhatsApp broadcast for outages; a way to tell users "update the app now".
29. Open-source licences inside the app (one Flutter Bluetooth library now charges for-profit users [S35]); keep a licence list.
30. Security testing of the app and the Bluetooth link before the first real patient (`FUTURE_ARCHITECTURE.md` §9.2).

---

## The fee table (short form)

| | One-time | Yearly | Source |
|---|---|---|---|
| **Google Play** | US$25 ≈ **₹2,400** | ₹0 | [S1] |
| **Apple App Store** | ₹0 | US$99 ≈ **₹9,500** (₹8,700 reported in India, snippet) | [S9, S10] |
| D-U-N-S number (organisation accounts on both) | ₹0 from D&B; up to ₹10,000 with a consultant (snippet) | ₹0 | [S11, S12] |
| Commission when hospitals pay us directly | 0% | 0% | [S5, S8] |

Rate used: ₹96 = US$1 (snippets, Sept and May 2026; today's rate not found).

## Recommended app path

- **Pilot:** today's web app wrapped as an **Android-only Capacitor app**, with one native Kotlin "link service" for Bluetooth. Installed privately on lent hub phones (and on willing families' Android phones). The plain web app with Web Bluetooth is used only for bench tests.
- **Scale:** the same shell, with the link module written natively per platform (Kotlin, then Swift for iPhone when the decision rule in M-25 is met). Go fully native only if cheap phones prove too slow. Keep in mind that the scale hardware (unit with its own 4G and speaker) makes the phone app optional.

## The auto-connect design in 8 plain steps

1. **The unit calls out.** Whenever it is on, it sends a short "I am SB-0007" radio message, quickly after a button press and slowly otherwise.
2. **One-time introduction.** Scan the QR on the unit, press the unit's button, tap "Allow" once. The phone and unit exchange keys and remember each other.
3. **The phone is told to keep watch.** Android itself, not our app, listens for that one unit from then on.
4. **The unit appears; Android wakes our app.** No tapping. (On older phones, or if the phone's maker blocks this, opening the app does the same.)
5. **The app connects and locks the link** with the saved keys, sets the unit's clock, and reads battery and status.
6. **It collects anything the unit stored** while the phone was away, saves it on the phone, then tells the unit it may erase it.
7. **During a session** a visible notification keeps the link alive and the live readings flow to the coach.
8. **When the link drops** (out of range, phone asleep, app killed), nothing is lost: the unit keeps recording and beeping its reminders, and steps 3–6 repeat by themselves the next time the two are near.

## Build order

Sizes as in `DEVICE_LIFECYCLE.md`: S = up to 1 day · M = 2–5 days · L = 1–4 weeks.

| # | Item | Size | Needs |
|---|---|---|---|
| 1 | Write the Bluetooth protocol (M-9 to M-12) as a contract in `ARCHITECTURE.md`, with byte layouts and a version number | M | chip choice |
| 2 | Record 20–30 reference breath curves as test files shared by app and firmware | S | – |
| 3 | `BleSource` in `web/js/sources.js` using Web Bluetooth; live curve on Android Chrome | M | a board running the service |
| 4 | Local database + upload queue with idempotent IDs in today's web app (works for USB and simulator too) | M | `/api/v1` sync endpoint |
| 5 | Capacitor Android shell around the web app; offline clips bundled | M | – |
| 6 | Kotlin link service: QR pairing through Companion Device Manager, bonding, auto-connect flag | L | 3, 5 |
| 7 | Device presence wake-up + `connectedDevice` foreground service + session notification | M | 6 |
| 8 | Stored-breath sync, time anchoring, "time estimated" marking | L | firmware store |
| 9 | The 12 states of M-16 with pictures and voice clips in each language | L | new clips recorded |
| 10 | Reminder schedule pushed to the unit; phone backup alarm | M | firmware buzzer |
| 11 | Re-assignment handling and local wipe (M-32) | M | `devices` and assignments API |
| 12 | Test matrix run (M-34), kill-and-recover tests, 48-hour soak | L | phones bought |
| 13 | Hub-phone image: one-app lock, battery limits off, volume locked | M | hub model chosen |
| 14 | Firmware update through the app, with roll-back | L | signing keys |
| 15 | Company, D-U-N-S, Play organisation account, privacy and deletion pages, declarations | L (mostly waiting) | company registered |
| 16 | Public Play listing after the regulatory answer | M | consultant's view |
| 17 | iPhone: Swift link module, TestFlight, App Review | L+ | decision rule met |

## Open questions

| Question | Why it matters | Who can answer |
|---|---|---|
| Is the app, as the driver of a measuring unit, itself a regulated device in India, and what may the store listing say? | Decides M-26 and whether a public listing is possible at all | Regulatory consultant (B4-1, B4-2, B4-8) |
| Does Play require an organisation account for a health app? | Decides personal vs organisation and whether the 12-tester rule applies | Play Console during sign-up; Google's "choose an account type" help |
| Bluetooth SIG listing: is it required for us, what is the fee, does a certified module reduce it? | Possibly the largest single fee in this file; not checked | Hardware reviewer; bluetooth.com |
| When will a company exist, and in whose name are the accounts until then? | Blocks D-U-N-S and both organisation accounts | Founder |
| Real D-U-N-S time and cost in India | Sources disagree (5 to 30 business days) | dnb.co.in |
| Apple's rupee price and whether a college can get the fee waiver | ₹8,700 is a forum snippet; the waiver page lists no countries | Apple enrolment page; Apple Developer Support |
| Can the hardware sense "spirometer on the base"? | State 6 in M-16 | Hardware reviewer |
| Advertising interval, battery life, flash size for 7 days of raw curves | All (est.) | Bench tests |
| Does device presence really wake the app on Xiaomi, Samsung, Oppo and Vivo budget phones? | The heart of "connects automatically" | The test matrix |
| Does Web Bluetooth work inside a Trusted Web Activity, and can a page re-find a known unit without the chooser? | Would make a thinner pilot possible | One afternoon with a board |
| Today's rupee–dollar rate, and one rate for all plan files | We used ₹96; another file uses ₹88 | Cost agent |
| Would an exercise-reminder app qualify for Play's exact-alarm permission? | Only matters if inexact alarms prove too late | Play policy page; a test submission |

## What we could not find or did not check
- React Native, `flutter_reactive_ble`, Kotlin Multiplatform and Bubblewrap were not researched; option (c) is judged from general knowledge.
- Play's Data safety, content rating, target audience, app signing and staged roll-out help pages; Apple's privacy-label page; Apple's rule on Xcode needing a Mac; tap-size guidelines. All are well known but were not opened this round.
- Nordic's firmware-update documentation returned only its page index.
- A smartphone-platform split specifically for older or low-income Indians. Only the all-India figure [S20] and the ownership figures already in the ledger [#65, #184].

## Sources opened this round

| # | URL | Title | Publisher | Grade | Used in |
|---|---|---|---|---|---|
| S1 | https://support.google.com/googleplay/android-developer/answer/6112435 | Get started with Play Console (US$25 fee, age 18, ID, device check) | Google | A | M-21, M-24 |
| S2 | https://support.google.com/googleplay/android-developer/answer/14151465 | App testing requirements for new personal developer accounts (12 testers, 14 days) | Google | A | M-21, M-23 |
| S3 | https://support.google.com/googleplay/android-developer/answer/11926878 | Target API level requirements (API 36 from 31 Aug 2026) | Google | A | M-20 |
| S4 | https://support.google.com/googleplay/android-developer/answer/14738291 | Health apps declaration | Google | A | M-21, M-23, M-26 |
| S5 | https://support.google.com/googleplay/android-developer/answer/112622 | Service fees | Google | A | M-21, M-24 |
| S6 | https://developer.apple.com/support/compare-memberships/ | Compare memberships (no fee figures on the page) | Apple | A | background only |
| S7 | https://developer.apple.com/support/fee-waiver/ | Apple Developer Program fee waivers | Apple | A | M-22 |
| S8 | https://developer.apple.com/app-store/review/guidelines/ | App Review Guidelines (1.4.1, 2.5.4, 3.1.3, 3.1.4, 4.2, 5.1.1(v), 5.1.3) | Apple | A | M-2, M-19, M-22, M-26, M-27, M-31 |
| S9 | https://developer.apple.com/programs/whats-included/ | Apple Developer Program: what's included (99 USD a year) | Apple | A | M-22, M-24 |
| S10 | https://developer.apple.com/help/account/membership/program-enrollment/ | Program enrolment (individual vs organisation, D-U-N-S, 299 USD enterprise) | Apple | A | M-22, M-24, M-37 |
| S11 | https://developer.apple.com/help/account/membership/D-U-N-S/ | D-U-N-S Number (free, up to 5 + 2 business days) | Apple | A | M-21, M-24 |
| S12 | https://support.google.com/googleplay/android-developer/answer/13628312 | Choose a developer account type (D-U-N-S for organisations; what is shown publicly) | Google | A | M-21, M-37 |
| S13 | https://developer.android.com/develop/connectivity/bluetooth/bt-permissions | Bluetooth permissions | Google, Android Developers | A | M-17, M-29 |
| S14 | https://developer.android.com/develop/connectivity/bluetooth/companion-device-pairing | Companion device pairing (presence, background start permissions) | Google, Android Developers | A | M-5, M-6, M-7, M-17 |
| S15 | https://developer.android.com/develop/background-work/services/fgs/service-types | Foreground service types (`connectedDevice`, Play declaration) | Google, Android Developers | A | M-7, M-18 |
| S16 | https://developer.apple.com/library/archive/documentation/NetworkingInternetWeb/Conceptual/CoreBluetooth_concepts/CoreBluetoothBackgroundProcessingForIOSApps/PerformingTasksWhileYourAppIsInTheBackground.html | Core Bluetooth background processing for iOS apps | Apple (archive) | A | M-4, M-8, M-14, M-19 |
| S17 | https://dontkillmyapp.com/ | Don't kill my app! (maker scores) | Urbandroid team (community site) | B | M-7, M-34 |
| S18 | https://support.google.com/googleplay/android-developer/answer/16679511 | Health content and services policy | Google | A | M-21, M-26, M-27 |
| S19 | https://support.google.com/googleplay/android-developer/answer/13327111 | Account deletion requirements | Google | A | M-21, M-23 |
| S20 | https://gs.statcounter.com/os-market-share/mobile/india | Mobile operating system market share, India, Sept 2026 | StatCounter | B | M-25 |
| S21 | https://gs.statcounter.com/android-version-market-share/mobile-tablet/india | Android version market share, India, Sept 2026 | StatCounter | B | M-29 |
| S22 | https://punchthrough.com/ble-throughput-part-4/ | Maximising BLE throughput, part 4 (packet size, intervals, ~50 kB/s) | Punch Through (engineering firm) | B | M-10, M-11 |
| S23 | https://developer.android.com/about/versions/14/changes/schedule-exact-alarms | Schedule exact alarms are denied by default (Android 14) | Google, Android Developers | A | M-18 |
| S24 | https://developer.android.com/training/monitoring-device-state/doze-standby | Optimise for Doze and App Standby | Google, Android Developers | A | M-7, M-18, M-33, M-35 |
| S25 | https://github.com/capacitor-community/bluetooth-le | Capacitor Bluetooth Low Energy plug-in (README) | Capacitor Community (open source) | B | M-1, M-2, M-19 |
| S26 | https://support.google.com/googleplay/work/answer/6145139 | Publish private apps (managed Google Play) | Google | A | M-23 |
| S27 | https://developer.apple.com/testflight/ | TestFlight | Apple | A | M-22, M-23 |
| S28 | https://developer.apple.com/custom-apps/ | Custom apps | Apple | A | M-23 |
| S29 | https://developer.apple.com/distribute/app-review/ | App Review (review times) | Apple | A | M-22 |
| S30 | https://support.google.com/googleplay/android-developer/answer/9859751 | Publish your app (review time) | Google | A | M-21 |
| S31 | https://codemagic.io/pricing/ | Pricing (500 free Mac minutes; US$0.095 a minute) | Codemagic (vendor) | B | M-22, M-24, M-36 |
| S32 | https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/app_dev/bootloaders_dfu/index.html | Bootloaders and DFU | Nordic Semiconductor | – | redirected, nothing read |
| S33 | https://nrfconnectdocs.nordicsemi.com/ncs/latest/nrf/app_dev/bootloaders_dfu/index.html | Bootloaders and DFU (page index only was readable) | Nordic Semiconductor | B | M-14 |
| S34 | https://lists.w3.org/Archives/Public/public-web-bluetooth/2024Sep/0002.html | Message to the Web Bluetooth list, 13 Sep 2024 (WebKit opposed; not in a major iOS browser) | W3C list; author a Google Chrome engineer | B | M-1 |
| S35 | https://pub.dev/packages/flutter_blue_plus/license | FlutterBluePlus License v1.6 (commercial licence for for-profit use) | pub.dev / the package author | B | M-2, M-37 |

**Search snippets only (not opened; grade C; check before quoting):**

| What | Where it appeared |
|---|---|
| US$1 ≈ ₹95.79 (11 Sep 2026); RBI reference rate ₹96.2948 (18 May 2026) | Deccan Chronicle headline; MSEI archive listing |
| D-U-N-S in India: free from D&B; consultants charge ₹3,999–₹10,000; standard route up to 30 business days | incorpx.io, charteredhelp.com, patronaccounting.com, startupgrantsindia.com |
| Apple Developer Program at ₹8,700 a year in India; reports of payment failures | Apple Developer Forums threads |
| Phone prices: Redmi A5 ₹6,499 at launch; Redmi 14C ₹8,499; Poco C75 5G ₹8,990–₹10,999; Galaxy M06 5G ₹9,999–₹13,999; Galaxy A06 ₹9,299; Realme C65 5G ₹9,499; Vivo Y19s 5G ₹10,999 | The Statesman, 91mobiles, Smartprix, other listing sites |
| nRF52840 dongle ₹2,900 on Amazon.in (July 2026); usable as a Bluetooth sniffer with Wireshark | pricehistory.app; Nordic documentation listing |
| Chrome 139 (Aug 2025) needs Android 10; Android 8 and 9 get no more Chrome updates | Business Standard, PhoneArena, 9to5Google |
| `flutter_blue_plus` documentation: auto-connect and reconnection notes | pub.dev documentation pages |

**Reused without re-opening:** ledger #65, #184, #201; DEVICE_LIFECYCLE sources D2, D3, D4, D7.

**Count:** 35 URLs opened (33 useful, 1 redirect with nothing read, 1 with no figures) and 7 groups of search snippets. None was already in `SOURCES_LEDGER.md`; the research agent should add them in its next round, since this session was told to write only this file.
