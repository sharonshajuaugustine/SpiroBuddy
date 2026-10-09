# 3D model – sources for every dimension

**Rule:** every size in the 3D model comes from a cited web source, or is clearly flagged.
Each row ID (B.., E.., D.., P.., C..) appears as a comment next to the number in the `CFG` object at the top of `web/showcase/showcase.js`.

**Confidence:** HIGH = published by the maker / datasheet · MED = retailer listing or official photo read directly · LOW = derived from a photo with a weak reference.
**Flags:** `DERIVED – confirm with caliper` = worked out from an official photo (arithmetic shown). `NOT PUBLISHED – placeholder` = no source found; measure it.

Research date: 9 Oct 2026.

---

## How the spirometer sizes were derived (read this first)

Romsons does **not** publish any dimensions for the Breazer 2500 (checked: the official romsons.in product page and its product data, Medikabazaar, Netmeds, Amazon.in, IndiaMART, Globallinker; the official product data even lists weight as `0`). Retailers give only rough box-style sizes, and they disagree:

| Listing | Size given | Weight |
|---|---|---|
| Amazon.in (B0BDVLW63J) – "Product Dimensions" | 20 × 20 × 9 cm | 350 g |
| IndiaMART (Romsons Medsource) | 20 × 10 × 5 cm | 300 g |
| Hospimart (search snippet only; page would not load) | 20 × 15 × 5 cm | 250 g |
| TrueMeds (search snippet only) | "approx. 12 × 12 × 12 cm" | 320 g |

The only number that three listings agree on is **20 cm as the largest dimension**. So:

1. **Anchor (B02):** overall height including the cap = **200 mm**. This is an assumption (LOW). If your caliper says otherwise, change `CFG.spiro.H` and scale the other derived sizes by the same factor.
2. **Scale:** the official Romsons labelled diagram (image 5 on romsons.in, a near-front orthographic drawing, 1500 × 1500 px) shows the device from the cap top (y = 355 px) to the base bottom (y = 1105 px) = **750 px**. So **1 px = 200 / 750 = 0.2667 mm**.
3. Every other spirometer size below = (pixel distance measured on that drawing) × 0.2667. The front-view ratio width/height = 664/750 = 0.885 was cross-checked against the official in-use photo (image 4: 432/480 = 0.90) – they agree within 2 %.
4. Depth (front-to-back) is not visible in a front drawing. It comes from the cap lobes (which look circular in the official ¾ photo, image 2) and is bounded by the 9 cm box depth on Amazon.

Official images used (all from the romsons.in product page, product data at `https://www.romsons.in/products/romsons-breazer-2500-volumetric-respiratory-exerciser.json`):
- **IMG-D** (labelled diagram): https://cdn.shopify.com/s/files/1/0625/3402/5474/files/5_c51db912-8a72-422d-be3b-ba0d7590884b.jpg
- **IMG-34** (¾ product photo): https://cdn.shopify.com/s/files/1/0625/3402/5474/files/2_26373931-7d07-454f-a6ee-3d6ae0a5b90f.jpg
- **IMG-USE** (man using it, near-front): https://cdn.shopify.com/s/files/1/0625/3402/5474/files/4_227980a9-c2b1-4c09-912d-dfc84be9e304.jpg
- **IMG-IFU** (instructions for use): https://cdn.shopify.com/s/files/1/0625/3402/5474/files/6_6a26af5f-3ebc-4832-958b-02fe9cdaeff4.jpg
- **IMG-BOX**: https://cdn.shopify.com/s/files/1/0625/3402/5474/files/1_9465c39c-8719-453c-ab36-6878348ed61f.jpg

---

## B – Romsons Breazer 2500 (the spirometer we model)

| ID | Part | Dimension | Value | Source URL | How verified | Confidence |
|---|---|---|---|---|---|---|
| B01 | Product | Model, capacity, ref | Breazer 2500, volumetric, up to 2500 mL, REF SH-6083, SKU ORBRZ2500; two chambers, connecting tube, mouthpiece with inbuilt filter, built-in handle, goal indicator, latex-free | https://www.romsons.in/products/romsons-breazer-2500-volumetric-respiratory-exerciser | Official maker page + product data (.json) | HIGH |
| B02 | Whole device | Overall height incl. cap | **200 mm** | Amazon.in https://www.amazon.in/dp/B0BDVLW63J ; IndiaMART https://www.indiamart.com/ms-romsons-medsource/respiratory-exerciser.html | Retailer listings: largest dimension 20 cm in all three that give one. Used as the anchor. **DERIVED – confirm with caliper** | LOW |
| B03 | Whole device | Overall width incl. handle | 177.1 mm (664 px × 0.2667) | IMG-D | Derived from official drawing; cross-checked with IMG-USE ratio 0.90. **DERIVED – confirm with caliper** | LOW–MED |
| B04 | Base | Width | 172.5 mm (647 px) | IMG-D | **DERIVED – confirm with caliper** | LOW–MED |
| B05 | Base | Height | 28.0 mm (105 px: y 1000→1105) | IMG-D | **DERIVED – confirm with caliper** | LOW–MED |
| B06 | Base | Depth (front–back) | 80 mm | IMG-34 + Amazon box depth 9 cm | Base looks deeper than the cap in IMG-34; must fit the 90 mm box. **DERIVED – confirm with caliper** | LOW |
| B06 | Base | Air arches (2 at front/back), 30 × 8 mm, at x −55 / +25 mm | IMG-D, IMG-34 | Shape read from photo; sizes estimated. **DERIVED – confirm with caliper** | LOW |
| B07 | Cap (blue, figure-8) | Thickness / width | 17.3 mm (65 px) / 144.0 mm (540 px) | IMG-D | **DERIVED – confirm with caliper** | LOW–MED |
| B08 | Cap | Lobe Ø over volume / flow chamber (→ cap depth) | 65.3 mm (245 px) / 61.3 mm (230 px); waist ≈ 0.62 × lobe | IMG-D, IMG-34 | Lobes assumed circular (they look round in IMG-34). **DERIVED – confirm with caliper** | LOW |
| B09 | Volume chamber | Outer Ø; centre from left edge | 47.2 mm (177 px); 106.8 mm | IMG-D | **DERIVED – confirm with caliper** | LOW–MED |
| B10 | Chamber walls, clear body panels | Wall thickness | 1.5 mm / 2 mm | – | **NOT PUBLISHED – placeholder, measure with caliper** | – |
| B11 | Chambers | Bottom of chambers / top of blue seat dish | 14.7 mm / 21.3 mm above floor (y 1050 / 1025 px) | IMG-D | **DERIVED – confirm with caliper** | LOW |
| B12 | Piston ("Volume Indicator (Plunger)") | Ø × height | 40.5 mm (152 px) × 30.7 mm (115 px) | IMG-D (labelled "Volume Indicator (Plunger)") | **DERIVED – confirm with caliper** | LOW–MED |
| B13 | Volume scale | Printed marks | 250, 500 … 2500 mL every 250 mL; "ml Inspired Volume"; **printed on both sides** | IMG-D ("Volume Scale Printed on both sides"), IMG-34 | Read directly from official images | HIGH |
| B14 | Volume scale | Mark spacing; height of 250 mark; 0 mL level | 11.14 mm per 250 mL ((873−497)/9 = 41.8 px); 250 mark 61.9 mm above floor; 0 mL ≈ 50.8 mm (extrapolated) | IMG-D | 2500 mark at y 497 px, 250 at y 873 px. Piston top drawn at 53.3 mm at rest (2.5 mm drawing slop) – model uses the extrapolated 0 mark. **DERIVED – confirm with caliper** | LOW–MED |
| B15 | Flow-indicator chamber | Outer Ø; centre from left edge | 32.3 mm (121 px); 37.2 mm | IMG-D | **DERIVED – confirm with caliper** | LOW–MED |
| B16 | Flow float (cup) | Top Ø / bottom Ø / height | 22.7 / 14.4 / 36.0 mm (85 / 54 / 135 px) | IMG-D (labelled "Flow Indicator") | **DERIVED – confirm with caliper** | LOW–MED |
| B17 | Flow zones | 3 emoji boxes, target = middle box (arrows) | 98.7 → 128.0 mm above floor; each ≈ 9.8 mm | IMG-D, IMG-IFU step 4 ("flow indicator stays in the middle emoji window") | Layout HIGH (official IFU); heights **DERIVED – confirm with caliper** | LOW–MED |
| B18 | Connector tube (middle, "BREAZER 2500" print) | Outer Ø; centre; hose port height | 12.0 mm (45 px); 76.4 mm; port ≈ 57 mm above floor | IMG-D, IMG-34, IMG-USE | Hose plugs in at the bottom front of this tube (IMG-34). **DERIVED – confirm with caliper** | LOW |
| B19 | Handle (clear, right side) | Hole x 140.5–160.5 mm, hole top 121.3 mm, outer edge 177.1 mm, 4 finger grips; thickness 12 mm | IMG-D, IMG-34 | Outline **DERIVED – confirm with caliper**; thickness **NOT PUBLISHED – placeholder** | LOW |
| B20 | Goal indicator | Blue slider on the right side of the volume chamber; set to the prescribed level | IMG-D ("Goal Indicator"), IMG-IFU step 1 | Official. Model sets it to 2000 mL (our demo target, C01) | HIGH (position on scale is a setting) |
| B21 | Corrugated hose | Outer Ø; rib pitch; length | 18.7 mm (70 px); ≈ 3.2 mm (≈ 12 px); ≈ 270 mm (path traced in IMG-34 ≈ 1000 px vs 750 px device height) | IMG-D, IMG-34 | Rough. **DERIVED – confirm with caliper / tape** | LOW |
| B22 | Mouthpiece | "Removable mouth piece with inbuilt filter"; filter housing Ø 20 × 22 mm + flat mouthpiece 34.6 mm, tip width 18.7 mm (total ≈ 56.6 mm = 212 px) | IMG-D; romsons.in text | Feature HIGH; sizes **DERIVED – confirm with caliper** | LOW |
| B23 | Colours | Clear body, blue cap/collars/piston/float/seats, frosted white base, white hose & mouthpiece; listing colour "BlueGreen" | IMG-34, IMG-USE; Medikabazaar https://www.medikabazaar.com/products/romsons-breazer-2500-volumetric-lung-exerciser-mbpgmrsmmssrre15739 | Official photos | HIGH |
| B24 | Whole device | Weight | 300–350 g (not used by the model) | Amazon.in, IndiaMART | Retailer listings (disagree) | LOW |
| B25 | Air path / physics | Inhaling through the mouthpiece creates **negative pressure** above the piston and float, so both rise; outside air enters **below** them through the base. The piston height shows inspired volume; the float shows flow rate. | FDA 510(k) K182847 (Voldyne, same device class): https://fda.innolitics.com/submissions/AN/subpart-f%E2%80%94therapeutic-devices/BWF/K182847 ; IMG-IFU step 4 (arrows point up in both chambers and along the hose to the mouth) | Official IFU drawing + regulator summary of an equivalent design | MED |
| B26 | Base under the piston | Is there an open inlet straight under the piston (laser path)? | – | Air must enter under the piston (B25), so an opening must exist, but its size/position is not visible in any published photo. **NOT PUBLISHED – check on the real unit before choosing base mount** | – |
| B27 | Flow float response | mL/s needed to reach each emoji box | Model: middle box at 600 mL/s, top box at ≥ 1300 mL/s (illustrative) | – | **NOT PUBLISHED – illustrative mapping only** | – |
| B28 | Chamber tops (cap underside) | Height | 182.7 mm = B02 − B07 | derived | arithmetic | LOW |

> Note: the printed mL scale is **not** the piston's swept volume (a 40.5 mm piston rising 111 mm sweeps only ~143 mL). Like other volumetric incentive spirometers, the scale is a factory calibration. That is why SpiroBuddy converts laser distance → mL using the **printed marks** (calibration table, ARCHITECTURE Contract B), never piston geometry.

## E – Electronics

| ID | Part | Dimension | Value | Source URL | How verified | Confidence |
|---|---|---|---|---|---|---|
| E01 | Seeed XIAO ESP32-C3 | Board size | 21 × 17.8 mm | https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/ | Official Seeed wiki spec table | HIGH |
| E02 | XIAO ESP32-C3 | Overall thickness incl. parts | ≈ 5 mm (model: PCB 1.0 mm + parts) | Galaxus listing https://galaxus.ch/en/s1/product/seeed-studio-xiao-esp32-c3-development-boards-kits-25165349 (search snippet) | Retailer; PCB thickness **NOT PUBLISHED – placeholder** | LOW |
| E03 | XIAO ESP32-C3 | Pins & USB-C | D0–D10 = GPIO2,3,4,5,6,7,21,20,8,9,10; 5V, GND, 3V3; USB-C on a short edge; U.FL antenna; charging 380 mA | Seeed wiki (above) | Official wiki pin table; USB-C position from official photos. USB-C shell 8.9 × 3.2 × 7.3 mm is **NOT PUBLISHED for XIAO – placeholder** | HIGH / – |
| E04 | VL53L1X | Package | 4.9 × 2.5 × 1.56 mm | ST datasheet DS12385 Rev 8 (Aug 2024) https://www.st.com/resource/en/datasheet/vl53l1x.pdf | Datasheet feature list (note: its Table 1 says 4.4 × 2.5 × 1.56 – inconsistency inside the datasheet; 4.9 used) | HIGH |
| E05 | VL53L1X | Field of view / ROI | 27° full FoV; programmable 15–27° by ROI from 4×4 to 16×16 SPADs | ST DS12385 Rev 8 | Datasheet | HIGH |
| E06 | VL53L1X | Laser | 940 nm invisible, Class 1 (IEC 60825-1:2014) | ST DS12385 Rev 8 | Datasheet. **The beam in the model is drawn for illustration only** | HIGH |
| E07 | VL53L1X | Range & timing | Short mode max 136 cm (dark) / 135 cm (ambient); min. guaranteed 4 cm; timing budget ≥ 33 ms for all modes (20 ms short only); up to 50 Hz | ST DS12385 Rev 8 | Datasheet | HIGH |
| E08 | VL53L1X breakout | Pololu #3415 carrier | 13 × 18 × 2 mm; 2 holes 0.5″ (12.7 mm) apart; 2.6–5.5 V; pins VDD VIN GND SDA SCL XSHUT GPIO1 | https://www.pololu.com/product/3415 | Official product page. (If you buy a GY-VL53L1X module instead, measure it.) | HIGH |
| E09 | LiPo battery | 500 mAh pouch with protection | 29 × 36 × 4.75 mm, 10.5 g, JST-PH | Adafruit #1578 https://www.adafruit.com/product/1578 | Official product page (a typical 400–600 mAh cell) | HIGH (for that product) |
| E10 | Passive piezo buzzer | PS1240 | Ø 11.9 × 6.53 mm | Adafruit #160 https://www.adafruit.com/product/160 | Official product page | HIGH (for that product) |
| E11 | WS2812B module | NeoPixel Mini Button PCB; LED package | PCB 9.1 × 9.1 × 3.2 mm (page also says "8 × 10 mm"); LED 5050 = 5.0 × 5.0 mm, 1.57 mm tall | Adafruit #1612 https://www.adafruit.com/product/1612 ; Worldsemi WS2812B spec (5050 package) https://www.triopak.fi/files/product/Worldsemi/WS2812B.pdf ; height: Maplin listing https://pro.maplin.co.uk/products/ws2812b-rgb-programmable-5050-smd-led-plcc-4 | Official page (with its own inconsistency) + maker spec + retailer | MED |
| E12 | Tactile button | 6 mm switch | 6.0 × 6.0 × 5.0 mm | Adafruit #367 https://www.adafruit.com/product/367 | Official product page | HIGH |
| E13 | Small parts on boards (ESP32-C3 chip block, pads, U.FL, standoffs) | – | illustrative | – | **Illustrative only – not size claims** | – |

## D – SpiroBuddy base unit (OUR OWN DESIGN)

The unit is our design. Its sizes are **derived** from the spirometer rows (B), the component rows (E) and the design rules in `docs/plans/SpiroBuddy_Complete_Plan.md` §4.3 and §4.5 (≥ 5 cm sensor-to-disc, ~2 mm walls, air openings open, USB-C reachable, foam ring, own battery compartment).

| ID | Item | Value | Derivation |
|---|---|---|---|
| D01 | Wall thickness | 2.0 mm | Plan §4.5 rule |
| D02 | Footprint | Pocket 177.5 × 85 mm; outside 181.5 × 89 mm, corner R 10 | Base B04/B06 172.5 × 80 + 2 × (2 mm EVA foam lining + 0.5 mm clearance) + 2 × 2 mm wall |
| D03 | Heights | Tray 34 mm + lid 12 mm = **46 mm total**; pocket 8 mm deep (floor top at 38 mm); 2 mm foam pads → spirometer floor at 40 mm | Chosen so the sensor-to-piston rule (D05) holds |
| D04 | Sensor stack | Tray floor 2 + standoff 3 + Pololu board 2 (E08) + VL53L1X 1.56 (E04) → sensor face at **8.56 mm** | arithmetic |
| D05 | Sensor → piston underside | At rest: 40 + (50.8 − 30.7) − 8.56 = **51.5 mm** (rule ≥ 50 mm ✓, ST minimum 40 mm ✓). At 2500 mL: 51.5 + 10 × 11.14 = **162.9 mm** (far inside short-mode 1.3 m) | B11/B12/B14 + D03/D04 |
| D06 | Beam footprint | ROI 15°: 13.6 mm Ø at rest, 42.9 mm Ø at 2500 mL (chamber bore ≈ 44.2 mm, piston 40.5 mm). Full 27° FoV would be 79 mm at the top → **use the smallest ROI** and calibrate with the printed marks | E05 + D05 |
| D07 | Light tunnel | Black tube ID 20 / OD 24 mm from just above the sensor to the pocket floor; black EVA foam ring ID 20 / OD 32 × 2 mm on top | Plan: foam ring against stray light |
| D08 | Air openings | 4 slots 12 × 4 mm on each long side at pocket level + 2 mm gap under the spirometer (pads) + open sensor window, so outside air still reaches the inlet under the piston | Plan: "air openings stay open" |
| D09 | USB-C access | 11 × 5 mm cut-out in the left wall; XIAO's USB-C at the wall | Plan: "USB-C stays reachable" |
| D10 | Front | Frosted light bar 60 × 5 mm with the WS2812B behind it; Ø 8 mm start-button cap (6 mm switch E12) | our design |
| D11 | Layout (x, z mm from centre) | Sensor under the volume-chamber axis (x = +20.6); XIAO at the left wall (z −14); LiPo in its own ribbed bay (−22, +16); buzzer (+64, −22); LED (+12, front); button (+66, front) | our design |
| – | Mounting choice | **Base mount** (sensor looks up at the piston underside). Why: the official IFU shows air entering both chambers from below (B25), and the Breazer's cap is opaque blue plastic, so a top mount would have to look through it. **Risk:** B26 – if the floor under the piston turns out to be closed plastic, run VL53L1X crosstalk calibration through it or switch to a side/top bracket. | |

## P – Phone (illustrative)

| ID | Item | Value | Note |
|---|---|---|---|
| P01 | Phone on a stand | 76 × 160 × 8.5 mm, screen 70 × 148 mm | **ILLUSTRATIVE – a generic phone, not a real product.** The screens show the idea of the patient app (being built separately). |

## C – Coaching rules used by the animation

| ID | Item | Value | Source |
|---|---|---|---|
| C01 | Target / hold target / "too fast" live threshold / window | 2000 mL / 3 s / 1200 mL/s / 0.3 s | `docs/ARCHITECTURE.md` §5 CONTRACT C |
| C02 | Score and labels | depth 4 × min(peak/target,1) + speed (3 if max rise ≤ 900, 1 if ≤ 1400, else 0) + hold 3 × min(hold/3,1); rules too_fast > 1400 → too_shallow pct < 0.5 → no_hold hold < 1.0 → good | CONTRACT C; same code as `ml/features.py` |

**Breath curves check** (sampled at 30 Hz with the CONTRACT C code; shown on the showroom page under "Breath check"):

| Curve (peak / rise / hold / fall) | max rise mL/s | hold s | pct target | rule label | score |
|---|---|---|---|---|---|
| good 1800 / 3.5 / 3.0 / 2.2 | 805.0 | 4.167 | 0.900 | good ✓ | 9.6 |
| too_fast 1700 / 0.9 / 1.6 / 1.6 | 2833.3 | 2.100 | 0.850 | too_fast ✓ | 5.5 |
| too_shallow 750 / 2.8 / 2.6 / 1.6 | 418.7 | 3.500 | 0.375 | too_shallow ✓ | 7.5 |
| no_hold 1850 / 3.0 / 0 / 1.0 | 964.5 | 0.833 | 0.925 | no_hold ✓ | 5.5 |

Verified twice: the showroom's JavaScript port and the project's `ml/features.py` give identical numbers.
(Exact values are printed in the browser console and in the page's "Breath check" table.)

---

## Caliper checklist (what to measure on the real Breazer, in this order)
1. Overall height incl. cap (B02) – if it is not 200 mm, scale all DERIVED B rows by (measured / 200).
2. Base width, depth and height (B04–B06) → sets the pocket size D02.
3. Piston underside height at rest above the table, and the floor/inlet under the piston (B11, B12, B26) → decides base mount and D05.
4. Height of the 250 mL and 2500 mL marks above the table (B14) → calibration and the 3D scale.
5. Volume chamber outer Ø and wall (B09, B10); cap lobes (B08).
6. Hose length and Ø, mouthpiece (B21, B22) – cosmetic.
