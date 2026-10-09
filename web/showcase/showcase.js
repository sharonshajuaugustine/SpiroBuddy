// SpiroBuddy 3D showroom — Three.js r169, no build step. Units: millimetres, y up.
// Every real-world size lives in CFG below. The row IDs (B.., E.., D.., P.., C..) point to
// docs/3D_SOURCES.md, which gives the source URL, how it was verified and the confidence.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';

// =====================================================================================
// CONFIG — the ONE place for every number. See docs/3D_SOURCES.md for each row.
// =====================================================================================
const CFG = {
  // ---- Romsons Breazer 2500 (REF SH-6083). x = mm from the body's left edge (front view),
  //      y = mm above the spirometer's own floor. Most sizes are DERIVED from the official
  //      Romsons diagram (scale 0.2667 mm/px, anchored on B02) → "confirm with caliper".
  spiro: {
    H: 200,                    // B02 overall height incl. cap (anchor, LOW confidence)
    W: 177.1,                  // B03 overall width incl. handle (DERIVED)
    baseW: 172.5,              // B04 base width (DERIVED)
    baseH: 28.0,               // B05 base height (DERIVED)
    baseD: 80,                 // B06 base depth (DERIVED, LOW; must be < 90 mm box depth)
    archW: 30, archH: 8,       // B06 air arches in the base front/back (DERIVED from photo, LOW)
    archX: [-55, 25],          // B06 arch centres, spirometer-local x (DERIVED, LOW)
    capT: 17.3, capW: 144.0,   // B07 cap thickness / width (DERIVED)
    capLobeDV: 65.3,           // B08 cap lobe Ø over the volume chamber (DERIVED) = cap depth
    capLobeDF: 61.3,           // B08 cap lobe Ø over the flow chamber (DERIVED)
    capWaist: 0.62,            // B08 waist depth as a fraction of the volume lobe (DERIVED, LOW)
    volOD: 47.2, volCX: 106.8, // B09 volume chamber OD / centre x (DERIVED)
    wall: 1.5,                 // B10 chamber wall thickness (NOT PUBLISHED – placeholder)
    chamberBottom: 14.7,       // B11 chamber bottom (DERIVED)
    seatTop: 21.3, seatH: 6.6, // B11 blue seat dish under piston / float (DERIVED)
    pistonD: 40.5, pistonH: 30.7, // B12 piston ("plunger") Ø / height (DERIVED)
    scaleStep: 250, scaleMax: 2500, // B13 printed scale 250…2500 mL in 250 mL steps (VERIFIED, photo)
    mark250Y: 61.9,            // B14 height of the 250 mL mark (DERIVED)
    mmPer250: 11.14,           // B14 spacing between printed marks (DERIVED)
    flowOD: 32.3, flowCX: 37.2, // B15 flow-indicator chamber OD / centre x (DERIVED)
    floatTopD: 22.7, floatBotD: 14.4, floatH: 36.0, // B16 flow float (cup) (DERIVED)
    zoneBottomY: 98.7, zoneTopY: 128.0, // B17 three emoji boxes; middle = target (DERIVED)
    midOD: 12.0, midCX: 76.4,  // B18 connector tube OD / centre x (DERIVED)
    portY: 57,                 // B18 hose port height on the connector tube (DERIVED)
    handle: { holeX0: 140.5, holeX1: 160.5, holeTop: 121.3, holeBottom: 40, outerX: 177.1,
              shoulderY: 95, thick: 12, gripPitch: 14, gripDepth: 2.4 }, // B19 (DERIVED; thick NOT PUBLISHED)
    goalMl: 2000,              // B20 goal-indicator slider set to the prescribed target (C01)
    hoseOD: 18.7, hosePitch: 3.2, hoseRib: 0.9, // B21 corrugated hose OD / rib pitch / rib depth (DERIVED, LOW)
    filterD: 20, filterL: 22, mouthL: 34.6, mouthW: 18.7, // B22 filter housing + mouthpiece (DERIVED, LOW)
    frameT: 2,                 // B10 clear body panel thickness (NOT PUBLISHED – placeholder)
  },
  // ---- Electronics (published sizes) ----
  elec: {
    xiao: { l: 21, w: 17.8, pcb: 1.0, h: 5 },        // E01 21×17.8 (Seeed wiki) · E02 ~5 mm overall (retailer) · PCB 1.0 NOT PUBLISHED
    usbc: { w: 8.9, h: 3.2, l: 7.3 },                // E03 USB-C receptacle shell (NOT PUBLISHED for XIAO – typical, placeholder)
    chipEsp: 5,                                      // E13 illustrative chip block (not a size claim)
    vlChip: { l: 4.9, w: 2.5, h: 1.56 },             // E04 VL53L1X package (ST DS12385 Rev 8)
    vlFovDeg: 27, vlRoiDeg: 15,                      // E05 full FoV 27°, ROI down to 15° (ST)
    vlBoard: { l: 18, w: 13, t: 2, holePitch: 12.7 },// E08 Pololu #3415 carrier 13×18×2 mm, holes 0.5″ apart
    lipo: { l: 36, w: 29, t: 4.75, mAh: 500 },       // E09 Adafruit #1578 500 mAh LiPo
    piezo: { d: 11.9, h: 6.53 },                     // E10 Adafruit #160 (PS1240) passive piezo
    ledPcb: { s: 9.1, t: 3.2 }, ledPkg: { s: 5.0, t: 1.57 }, // E11 Adafruit #1612 NeoPixel mini PCB · WS2812B 5050 package
    tact: { s: 6.0, h: 5.0 },                        // E12 Adafruit #367 6 mm tactile switch
  },
  // ---- SpiroBuddy base unit: OUR OWN DESIGN, derived from B/E rows + plan design rules ----
  unit: {
    wall: 2.0,                 // D01 plan rule "walls about 2 mm"
    foam: 2.0, clear: 0.5,     // D02 foam lining (2–3 mm EVA, plan) + fit clearance
    outerW: 181.5, outerD: 89, cornerR: 10, // D02 = base 172.5×80 + 2×(foam 2 + clearance 0.5 + wall 2)
    trayH: 34, lidH: 12, pocketDepth: 8, floorT: 2, // D03
    pad: 2,                    // D03 foam pads → spirometer floor sits at y = 40
    standoff: 3,               // D04 sensor board standoff above the tray floor
    tunnelID: 20, tunnelOD: 24, foamRingOD: 32, foamRingH: 2, // D07
    vent: { w: 12, h: 4, n: 4 },   // D08 air slots per long side (keep air openings open)
    usbCut: { w: 11, h: 5 },       // D09 USB-C access cut-out
    lightBar: { w: 60, h: 5 }, buttonCapD: 8, // D10
    xiaoAt: [-78, -14], batteryAt: [-22, 16], buzzerAt: [64, -22], ledAt: [12], buttonAt: [66], // D11 (x,z)
    frontY: 22,                // D11 height of light bar / button centre
  },
  phone: { w: 76, h: 160, t: 8.5, r: 9, screenW: 70, screenH: 148, at: [205, 0, 52], yaw: -0.36, tilt: -0.24 }, // P01 ILLUSTRATIVE
  // ---- Coaching rules (CONTRACT C, docs/ARCHITECTURE.md §5) ----
  coach: { target: 2000, holdTarget: 3, fastRate: 1200, riseWin: 0.3, fps: 30, session: 10 }, // C01
  // Breath curves (sine-eased rise, flat hold, sine-eased fall) — task brief, verified against CONTRACT C below.
  breaths: {
    good:        { peak: 1800, rise: 3.5, hold: 3.0, fall: 2.2 },
    too_fast:    { peak: 1700, rise: 0.9, hold: 1.6, fall: 1.6 },
    too_shallow: { peak: 750,  rise: 2.8, hold: 2.6, fall: 1.6 },
    no_hold:     { peak: 1850, rise: 3.0, hold: 0.0, fall: 1.0 },
  },
  // Flow-indicator float response: NOT PUBLISHED by Romsons → illustrative mapping (B27).
  floatFlowForTarget: 600, floatMaxFlow: 1300,
  video: { w: 1920, h: 1080, fps: 30, jpegQ: 0.92 },
};

// Derived numbers (all computed from CFG — no new facts here)
const S = CFG.spiro, U = CFG.unit, E = CFG.elec;
const SX = x => x - S.baseW / 2;                          // spirometer-local x from "mm from left edge"
const D = {
  capBottom: S.H - S.capT,                                // B28 chamber tops / cap underside
  zeroY: S.mark250Y - S.mmPer250,                         // B14 0 mL level of the piston top
  mmPerMl: S.mmPer250 / S.scaleStep,                      // B14
  volX: SX(S.volCX), flowX: SX(S.flowCX), midX: SX(S.midCX),
  pocketW: S.baseW + 2 * (U.foam + U.clear), pocketD: S.baseD + 2 * (U.foam + U.clear),
  lidTop: U.trayH + U.lidH,                               // 46
  plateTop: U.trayH + U.lidH - U.pocketDepth,             // 38
  seatY: U.trayH + U.lidH - U.pocketDepth + U.pad,        // 40 → spirometer floor on the unit
  sensorFaceY: U.floorT + U.standoff + E.vlBoard.t + E.vlChip.h, // D04 = 8.56
};
D.pistonRestBottom = D.zeroY - S.pistonH;                 // B12/B14
D.restDist = D.seatY + D.pistonRestBottom - D.sensorFaceY;  // D05
const LBL = { good: 'Good', too_fast: 'Too fast', too_shallow: 'Too shallow', no_hold: 'No hold' };
const LBL_HI = { good: 'बहुत बढ़िया!', too_fast: 'अगली बार धीरे', too_shallow: 'और गहरी साँस लें', no_hold: 'थोड़ा रोकें' };
const TIP = { good: 'Great breath!', too_fast: 'Too fast – slower next time', too_shallow: 'Breathe in deeper', no_hold: 'Hold a little longer' };
const COL = { idle: 0x2f7cf6, breathe: 0x14b8a6, fast: 0xf59e0b, good: 0x22c55e, soft: 0x93c5fd };

// =====================================================================================
// BREATH MATH — CONTRACT C (port of ml/features.py; same names and formulas)
// =====================================================================================
const breathDur = type => { const b = CFG.breaths[type]; return b.rise + b.hold + b.fall; };
function curveVol(type, tau) {
  const b = CFG.breaths[type];
  if (tau <= 0) return 0;
  if (tau < b.rise) return b.peak * (1 - Math.cos(Math.PI * tau / b.rise)) / 2;
  tau -= b.rise;
  if (tau < b.hold) return b.peak;
  tau -= b.hold;
  if (tau < b.fall) return b.peak * (1 + Math.cos(Math.PI * tau / b.fall)) / 2;
  return 0;
}
function extractFeatures(samples, target) {
  const KEYS = ['peak_ml', 'pct_target', 'time_to_peak_s', 'mean_rise_ml_s', 'max_rise_ml_s', 'hold_s', 'smoothness', 'duration_s'];
  const zero = Object.fromEntries(KEYS.map(k => [k, 0]));
  if (!samples.length) return zero;
  const t = samples.map(s => s.t), v = samples.map(s => s.ml);
  let pi = 0; for (let i = 1; i < v.length; i++) if (v[i] > v[pi]) pi = i;
  const peak = v[pi]; if (peak <= 0) return zero;
  let onset = v.findIndex(x => x >= 0.1 * peak), end = onset;
  for (let i = 0; i < v.length; i++) if (v[i] >= 0.1 * peak) end = i;
  const ttp = t[pi] - t[onset];
  const rt = t.slice(onset, pi + 1), rv = v.slice(onset, pi + 1);
  const meanRise = ttp > 0 ? (peak - v[onset]) / ttp : 0;
  let maxRise = meanRise;
  if (ttp > CFG.coach.riseWin && rt.length >= 2) {
    let best = -Infinity, j = 0;
    for (let i = 0; i < rt.length; i++) {
      while (j < rt.length && rt[j] < rt[i] + CFG.coach.riseWin) j++;      // numpy searchsorted(side="left")
      if (j >= rt.length) break;
      const dt = rt[j] - rt[i]; if (dt > 0) best = Math.max(best, (rv[j] - rv[i]) / dt);
    }
    if (best > -Infinity) maxRise = Math.max(best, meanRise);
  }
  let hold = 0;
  for (let i = 0; i < v.length - 1; i++) if (v[i] >= 0.9 * peak) hold += t[i + 1] - t[i];
  const d = []; for (let i = 1; i < rv.length; i++) d.push(rv[i] - rv[i - 1]);
  let smooth = 0;
  if (d.length >= 2) { const m = d.reduce((a, b) => a + b, 0) / d.length; if (m > 0) smooth = Math.sqrt(d.reduce((a, b) => a + (b - m) ** 2, 0) / d.length) / m; }
  const r = (x, n) => Math.round(x * 10 ** n) / 10 ** n;
  return { peak_ml: r(peak, 1), pct_target: r(peak / target, 3), time_to_peak_s: r(ttp, 3), mean_rise_ml_s: r(meanRise, 1),
           max_rise_ml_s: r(maxRise, 1), hold_s: r(hold, 3), smoothness: r(smooth, 3), duration_s: r(t[end] - t[onset], 3) };
}
function scoreOf(f, target = CFG.coach.target, holdTarget = CFG.coach.holdTarget) {
  const depth = 4 * Math.min(f.peak_ml / target, 1);
  const speed = f.max_rise_ml_s <= 900 ? 3 : (f.max_rise_ml_s <= 1400 ? 1 : 0);
  const hold = 3 * Math.min(f.hold_s / holdTarget, 1);
  return Math.round((Math.max(depth, 0) + speed + Math.max(hold, 0)) * 10) / 10;
}
function ruleLabel(f) {
  if (f.max_rise_ml_s > 1400) return 'too_fast';
  if (f.pct_target < 0.5) return 'too_shallow';
  if (f.hold_s < 1.0) return 'no_hold';
  return 'good';
}
// Sample every breath type at 30 Hz and check it gets its intended label.
const BREATH_RESULTS = {};
for (const type of Object.keys(CFG.breaths)) {
  const samples = [], dur = breathDur(type), fps = CFG.coach.fps;
  for (let i = -Math.round(0.5 * fps); i <= Math.round((dur + 0.5) * fps); i++) samples.push({ t: i / fps, ml: curveVol(type, i / fps) });
  const f = extractFeatures(samples, CFG.coach.target);
  BREATH_RESULTS[type] = { features: f, label: ruleLabel(f), score: scoreOf(f), samples, ok: ruleLabel(f) === type };
}
console.table(Object.fromEntries(Object.entries(BREATH_RESULTS).map(([k, r]) => [k, { label: r.label, ok: r.ok, score: r.score, ...r.features }])));

// Rise rate over the last 0.3 s (live "too fast" check, CONTRACT C)
const rate03 = (type, tau) => (curveVol(type, tau) - curveVol(type, tau - CFG.coach.riseWin)) / CFG.coach.riseWin;

// Evaluate a breath schedule [{t0, type}] at time t → pure function of (schedule, t)
function breathEval(sched, t) {
  const out = { vol: 0, flow: 0, r03: 0, state: 'IDLE', active: null, done: [], lastDone: null, fastAt: null };
  for (const b of sched) {
    const dur = breathDur(b.type), tau = t - b.t0;
    if (tau >= dur) { out.done.push(b); out.lastDone = b; continue; }
    if (tau >= 0 && !out.active) {
      out.active = b;
      const bb = CFG.breaths[b.type];
      out.vol = curveVol(b.type, tau);
      out.flow = (curveVol(b.type, tau) - curveVol(b.type, tau - 1 / 30)) * 30;
      out.r03 = rate03(b.type, tau);
      out.phase = tau < bb.rise ? 'rise' : (tau < bb.rise + bb.hold ? 'hold' : 'fall');
      if (out.vol < 150 && out.phase === 'rise') out.state = 'IDLE';
      else if (out.phase === 'rise') out.state = Math.abs(out.flow) < 150 && tau > 0.3 ? 'HOLDING' : 'INHALING';
      else if (out.phase === 'hold') out.state = 'HOLDING';
      else out.state = out.vol < 100 ? 'IDLE' : 'FALLING';
      // first moment the 0.3 s rise rate crossed FAST_RATE during this rise
      for (let k = 0; k <= Math.min(tau, bb.rise) * 30; k++) {
        if (rate03(b.type, k / 30) > CFG.coach.fastRate) { out.fastAt = b.t0 + k / 30; break; }
      }
    }
  }
  out.lastEnd = out.lastDone ? out.lastDone.t0 + breathDur(out.lastDone.type) : -1e9;
  out.result = out.lastDone ? BREATH_RESULTS[out.lastDone.type] : null;
  return out;
}
function coachEval(be, t) {
  if (be.active) {
    // once the 0.3 s rise rate crossed FAST_RATE, stay amber for the rest of this breath so the patient sees it
    if (be.fastAt !== null && t >= be.fastAt) return { led: COL.fast, en: 'Slower…', hi: 'धीरे…', tone: 'fast' };
    if (be.phase === 'rise') return { led: COL.breathe, en: 'Breathe in slowly', hi: 'धीरे-धीरे साँस लें', tone: 'breathe' };
    if (be.phase === 'hold') return { led: COL.breathe, en: 'Hold…', hi: 'साँस रोकें…', tone: 'breathe' };
    return { led: COL.breathe, en: 'Now breathe out', hi: 'अब साँस छोड़ें', tone: 'breathe' };
  }
  if (be.lastDone && t - be.lastEnd < 4.5) {
    const lab = be.result.label;
    return { led: lab === 'good' ? COL.good : (lab === 'too_fast' ? COL.fast : COL.soft), en: TIP[lab], hi: LBL_HI[lab], tone: lab, result: be.result };
  }
  return { led: COL.idle, en: 'Ready – slow, deep breath', hi: 'तैयार – धीरे, गहरी साँस', tone: 'idle' };
}

// =====================================================================================
// RENDERER, SCENE, LIGHTS
// =====================================================================================
const params = new URLSearchParams(location.search);
const RENDER_ID = params.get('render');
const RENDER = !!RENDER_ID;
const glCanvas = document.getElementById('gl');
const ovCanvas = document.getElementById('ov');
const renderer = new THREE.WebGLRenderer({ canvas: glCanvas, antialias: true, preserveDrawingBuffer: RENDER });
renderer.setPixelRatio(RENDER ? 1 : Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.background = gradientTexture();
const camera = new THREE.PerspectiveCamera(30, 16 / 9, 5, 20000);

const hemi = new THREE.HemisphereLight(0xffffff, 0x8899aa, 0.55); scene.add(hemi);
const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(260, 520, 360); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
Object.assign(key.shadow.camera, { left: -420, right: 420, top: 420, bottom: -420, near: 50, far: 1600 });
key.shadow.bias = -0.0004; key.shadow.radius = 6;
scene.add(key);
const rim = new THREE.DirectionalLight(0xcfe8ff, 1.1); rim.position.set(-400, 300, -380); scene.add(rim);

function gradientTexture() {
  const c = document.createElement('canvas'); c.width = 16; c.height = 512;
  const g = c.getContext('2d'), gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, '#f4f6f9'); gr.addColorStop(0.55, '#e3e9ef'); gr.addColorStop(1, '#bfcad6');
  g.fillStyle = gr; g.fillRect(0, 0, 16, 512);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
// Table / floor with soft radial fade
{
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'), gr = g.createRadialGradient(128, 128, 20, 128, 128, 128);
  gr.addColorStop(0, '#fff'); gr.addColorStop(0.7, '#888'); gr.addColorStop(1, '#000');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  const alpha = new THREE.CanvasTexture(c);
  const floor = new THREE.Mesh(new THREE.CircleGeometry(1400, 96),
    new THREE.MeshStandardMaterial({ color: 0xe9eef2, roughness: 0.85, metalness: 0, transparent: true, alphaMap: alpha, depthWrite: false }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; floor.name = 'floor';
  scene.add(floor);
}

// =====================================================================================
// MATERIALS & HELPERS
// =====================================================================================
const M = {
  clear: () => new THREE.MeshPhysicalMaterial({ color: 0xf4fbff, roughness: 0.04, metalness: 0, transparent: true, opacity: 0.17,
    clearcoat: 1, clearcoatRoughness: 0.04, side: THREE.DoubleSide, depthWrite: false, envMapIntensity: 1.4 }),
  frosted: () => new THREE.MeshPhysicalMaterial({ color: 0xf1f5f8, roughness: 0.45, transparent: true, opacity: 0.86, clearcoat: 0.4 }),
  blue: () => new THREE.MeshPhysicalMaterial({ color: 0x3aa7d9, roughness: 0.32, clearcoat: 0.6, clearcoatRoughness: 0.2 }),
  blueTrans: () => new THREE.MeshPhysicalMaterial({ color: 0x5bb9e8, roughness: 0.25, transparent: true, opacity: 0.82, clearcoat: 0.6 }),
  shellWhite: () => new THREE.MeshPhysicalMaterial({ color: 0xf5f7f9, roughness: 0.5, clearcoat: 0.25, transparent: true, opacity: 1 }),
  shellDark: () => new THREE.MeshPhysicalMaterial({ color: 0x24303a, roughness: 0.42, clearcoat: 0.35, transparent: true, opacity: 1 }),
  foam: () => new THREE.MeshStandardMaterial({ color: 0x141414, roughness: 1, transparent: true, opacity: 1 }),
  pcbBlack: () => new THREE.MeshStandardMaterial({ color: 0x1d2328, roughness: 0.55 }),
  pcbBlue: () => new THREE.MeshStandardMaterial({ color: 0x1f4fa0, roughness: 0.55 }),
  metal: () => new THREE.MeshStandardMaterial({ color: 0xc9ced3, roughness: 0.28, metalness: 1 }),
  pouch: () => new THREE.MeshStandardMaterial({ color: 0xb9bec4, roughness: 0.38, metalness: 0.75 }),
  black: () => new THREE.MeshStandardMaterial({ color: 0x0b0d10, roughness: 0.6 }),
  teal: () => new THREE.MeshPhysicalMaterial({ color: 0x0b6e8a, roughness: 0.35, clearcoat: 0.5 }),
  wire: c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.5, transparent: true, opacity: 1 }),
};
function mesh(geo, mat, name, { cast = true, receive = true } = {}) {
  const m = new THREE.Mesh(geo, mat); m.name = name || ''; m.castShadow = cast; m.receiveShadow = receive; return m;
}
function box(w, h, d, mat, name) { return mesh(new THREE.BoxGeometry(w, h, d), mat, name); }
function rbox(w, h, d, r, mat, name) { return mesh(new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2 - 0.01, h / 2 - 0.01, d / 2 - 0.01)), mat, name); }
function cyl(rt, rb, h, mat, name, seg = 48, open = false) { return mesh(new THREE.CylinderGeometry(rt, rb, h, seg, 1, open), mat, name); }
function at(o, x, y, z) { o.position.set(x, y, z); return o; }
function roundRect(w, d, r, cx = 0, cz = 0) {
  const s = new THREE.Shape(), x0 = cx - w / 2, y0 = cz - d / 2;
  s.moveTo(x0 + r, y0); s.lineTo(x0 + w - r, y0); s.quadraticCurveTo(x0 + w, y0, x0 + w, y0 + r);
  s.lineTo(x0 + w, y0 + d - r); s.quadraticCurveTo(x0 + w, y0 + d, x0 + w - r, y0 + d);
  s.lineTo(x0 + r, y0 + d); s.quadraticCurveTo(x0, y0 + d, x0, y0 + d - r); s.lineTo(x0, y0 + r); s.quadraticCurveTo(x0, y0, x0 + r, y0);
  return s;
}
function circlePath(r, cx = 0, cy = 0) { const p = new THREE.Path(); p.absarc(cx, cy, r, 0, Math.PI * 2, false); return p; }
function circleShape(r, cx = 0, cy = 0) { const p = new THREE.Shape(); p.absarc(cx, cy, r, 0, Math.PI * 2, false); return p; }
// Extrude a top-view shape (x, z=−shapeY) upward from y0 by h.
function extrudeY(shape, y0, h, curveSegments = 32) {
  const g = new THREE.ExtrudeGeometry(shape, { depth: h, bevelEnabled: false, curveSegments });
  g.rotateX(-Math.PI / 2); g.translate(0, y0, 0); return g;
}
function canvasTex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData.canvas = c; return t;
}
const FONT = "Inter, 'Noto Sans Devanagari', system-ui, sans-serif";

// =====================================================================================
// SPIROMETER — Romsons Breazer 2500
// =====================================================================================
const xrayMats = [];    // materials that fade in X-ray mode: { mat, base }
function xr(mat, base = mat.opacity) { xrayMats.push({ mat, base }); return mat; }

function buildSpirometer() {
  const g = new THREE.Group(); g.name = 'Romsons_Breazer_2500';
  const parts = {};
  // --- base (front-profile extrusion with air arches), frosted white (B04–B06, B23)
  {
    const sh = new THREE.Shape(), w = S.baseW / 2, r = 6;
    sh.moveTo(-w, 0);
    for (const ax of [...S.archX].sort((a, b) => a - b)) {
      sh.lineTo(ax - S.archW / 2, 0);
      sh.quadraticCurveTo(ax - S.archW / 2, S.archH, ax, S.archH);
      sh.quadraticCurveTo(ax + S.archW / 2, S.archH, ax + S.archW / 2, 0);
    }
    sh.lineTo(w, 0); sh.lineTo(w, S.baseH - r); sh.quadraticCurveTo(w, S.baseH, w - r, S.baseH);
    sh.lineTo(-w + r, S.baseH); sh.quadraticCurveTo(-w, S.baseH, -w, S.baseH - r); sh.lineTo(-w, 0);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: S.baseD - 6, bevelEnabled: true, bevelThickness: 3, bevelSize: 2.5, bevelSegments: 4, curveSegments: 16 });
    geo.translate(0, 0, -(S.baseD - 6) / 2);
    parts.base = mesh(geo, xr(M.frosted()), 'spiro_base');
    g.add(parts.base);
  }
  // --- chambers (clear), seat dishes, collars
  const clearMat = M.clear();
  const chamber = (x, od, name) => {
    const h = D.capBottom - S.chamberBottom, y = S.chamberBottom + h / 2;
    const outer = at(cyl(od / 2, od / 2, h, clearMat, name, 64, true), x, y, 0); outer.castShadow = false;
    const inner = at(cyl(od / 2 - S.wall, od / 2 - S.wall, h, clearMat, name + '_inner', 64, true), x, y, 0); inner.castShadow = false;
    const collar = at(cyl(od / 2 + 1.2, od / 2 + 1.2, 9, M.blue(), name + '_collar'), x, D.capBottom - 4.5, 0);
    const dish = at(cyl(od / 2 + 0.5, od / 2 + 0.5, S.seatH, M.blueTrans(), name + '_seat'), x, S.seatTop - S.seatH / 2, 0);
    g.add(outer, inner, collar, dish);
    return outer;
  };
  parts.volChamber = chamber(D.volX, S.volOD, 'volume_chamber');
  parts.flowChamber = chamber(D.flowX, S.flowOD, 'flow_chamber');
  // connector tube (clear) + hose port sleeve
  {
    const h = D.capBottom - S.chamberBottom;
    const t = at(cyl(S.midOD / 2, S.midOD / 2, h, clearMat, 'connector_tube', 32, true), D.midX, S.chamberBottom + h / 2, 0); t.castShadow = false;
    g.add(t, at(cyl(S.midOD / 2 + 1.5, S.midOD / 2 + 1.5, 8, M.blue(), 'connector_collar'), D.midX, D.capBottom - 4, 0));
    g.add(at(cyl(S.midOD / 2 + 1.5, S.midOD / 2 + 1.5, S.seatH, M.blueTrans(), 'connector_seat'), D.midX, S.seatTop - S.seatH / 2, 0));
    const port = cyl(S.hoseOD / 2 - 0.6, S.hoseOD / 2 - 0.6, 14, M.frosted(), 'hose_port', 32);
    port.rotation.x = Math.PI / 2; at(port, D.midX, S.portY, S.midOD / 2 + 5);
    g.add(port);
    parts.port = port;
    // "BREAZER 2500" print on the connector tube (vertical)
    const tex = canvasTex(128, 512, (c, w, h) => {
      c.translate(w / 2, h / 2); c.rotate(-Math.PI / 2); c.fillStyle = '#2a6fb5';
      c.font = `italic 800 70px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('BREAZER', -30, 4);
      c.font = `700 34px ${FONT}`; c.fillText('2500', 180, 6);
    });
    const p = mesh(new THREE.CylinderGeometry(S.midOD / 2 + 0.25, S.midOD / 2 + 0.25, 48, 24, 1, true, -0.9, 1.8),
      new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }), 'connector_print', { cast: false });
    g.add(at(p, D.midX, 112, 0));
  }
  // printed volume scale on BOTH sides of the volume chamber (B13, B14)
  {
    const r = S.volOD / 2 + 0.25, span = D.capBottom - D.zeroY;
    const tex = canvasTex(512, 2048, (c, w, h) => {
      c.fillStyle = '#2b5f9e'; c.strokeStyle = '#2b5f9e'; c.textAlign = 'center'; c.textBaseline = 'middle';
      for (let ml = S.scaleStep; ml <= S.scaleMax; ml += S.scaleStep) {
        const y = h - (ml / S.scaleStep) * S.mmPer250 / span * h;
        c.font = `800 74px ${FONT}`; c.fillText(String(ml), w / 2, y);
        c.lineWidth = 9; c.beginPath(); c.moveTo(w / 2 - 175, y); c.lineTo(w / 2 - 140, y); c.moveTo(w / 2 + 140, y); c.lineTo(w / 2 + 175, y); c.stroke();
        c.lineWidth = 4; const yh = y + (S.mmPer250 / 2) / span * h; c.beginPath(); c.moveTo(w / 2 - 50, yh); c.lineTo(w / 2 + 50, yh); c.stroke();
      }
      c.font = `600 40px ${FONT}`; c.fillText('ml Inspired Volume', w / 2, h - 30);
    });
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.FrontSide });
    for (const start of [-0.75, Math.PI - 0.75]) {
      const m = mesh(new THREE.CylinderGeometry(r, r, span, 48, 1, true, start, 1.5), mat, 'volume_scale', { cast: false });
      g.add(at(m, D.volX, D.zeroY + span / 2, 0));
    }
  }
  // emoji flow zones on the flow chamber (B17)
  {
    const r = S.flowOD / 2 + 0.25, y0 = S.zoneBottomY, y1 = S.zoneTopY, span = y1 - y0;
    const tex = canvasTex(256, 768, (c, w, h) => {
      const bh = h / 3, bw = 190, x0 = (w - bw) / 2;
      c.strokeStyle = '#2b6cb0'; c.fillStyle = '#2b6cb0';
      for (let i = 0; i < 3; i++) {
        const y = i * bh; c.lineWidth = i === 1 ? 14 : 6; c.strokeRect(x0 + 8, y + 10, bw - 16, bh - 20);
        const cx = w / 2, cy = y + bh / 2; c.lineWidth = 7;
        c.beginPath(); c.arc(cx, cy, 62, 0, Math.PI * 2); c.stroke();
        c.beginPath(); c.arc(cx - 22, cy - 15, 9, 0, Math.PI * 2); c.arc(cx + 22, cy - 15, 9, 0, Math.PI * 2); c.fill();
        c.beginPath(); c.arc(cx, cy + 6, 32, 0.15 * Math.PI, 0.85 * Math.PI); c.stroke();
      }
      c.lineWidth = 8; const my = bh * 1.5; // arrows → ← on the target box
      for (const s of [-1, 1]) { const xa = w / 2 + s * 118; c.beginPath(); c.moveTo(xa + s * 0, my); c.lineTo(xa - s * 0 + s * 0, my); c.moveTo(w / 2 + s * 128, my); c.lineTo(w / 2 + s * 104, my); c.lineTo(w / 2 + s * 114, my - 9); c.moveTo(w / 2 + s * 104, my); c.lineTo(w / 2 + s * 114, my + 9); c.stroke(); }
    });
    const m = mesh(new THREE.CylinderGeometry(r, r, span, 32, 1, true, -0.62, 1.24),
      new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }), 'flow_zones', { cast: false });
    g.add(at(m, D.flowX, y0 + span / 2, 0));
    const brand = canvasTex(256, 64, (c, w, h) => { c.fillStyle = '#2a6fb5'; c.font = `italic 700 44px Georgia, serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('Romsons', w / 2, h / 2); });
    const b = mesh(new THREE.CylinderGeometry(r, r, 7, 32, 1, true, -0.7, 1.4), new THREE.MeshBasicMaterial({ map: brand, transparent: true, depthWrite: false }), 'flow_brand', { cast: false });
    g.add(at(b, D.flowX, 42, 0));
  }
  // piston / plunger (B12) — moves; "ml Inspired Volume" print, side vent slots
  {
    const p = new THREE.Group(); p.name = 'piston';
    const pm = M.blueTrans(); pm.opacity = 0.9;
    p.add(at(cyl(S.pistonD / 2, S.pistonD / 2, S.pistonH, pm, 'piston_body', 48), 0, S.pistonH / 2, 0));
    p.add(at(cyl(S.pistonD / 2 - 1, S.pistonD / 2 - 1, 1.2, M.blue(), 'piston_top'), 0, S.pistonH - 0.6, 0));
    p.add(at(cyl(4, 4, 2.5, M.blue(), 'piston_knob'), 0, S.pistonH + 1.0, 0));
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2, s = box(2.2, 4.5, 1.2, M.black(), 'piston_slot');
      s.position.set(Math.sin(a) * (S.pistonD / 2 - 0.2), S.pistonH * 0.42, Math.cos(a) * (S.pistonD / 2 - 0.2)); s.rotation.y = a; p.add(s);
    }
    const lab = canvasTex(256, 96, (c, w, h) => { c.fillStyle = '#ffffff'; c.textAlign = 'center'; c.font = `600 30px ${FONT}`; c.fillText('ml Inspired', w / 2, 38); c.fillText('Volume', w / 2, 76); });
    p.add(at(mesh(new THREE.CylinderGeometry(S.pistonD / 2 + 0.1, S.pistonD / 2 + 0.1, 9, 32, 1, true, -0.6, 1.2),
      new THREE.MeshBasicMaterial({ map: lab, transparent: true, depthWrite: false }), 'piston_print', { cast: false }), 0, S.pistonH * 0.72, 0));
    p.position.set(D.volX, D.pistonRestBottom, 0);
    g.add(p); parts.piston = p;
  }
  // flow float (B16) — moves with flow (illustrative mapping B27)
  {
    const f = new THREE.Group(); f.name = 'flow_float';
    const fm = M.blueTrans(); fm.opacity = 0.75; fm.side = THREE.DoubleSide;
    f.add(at(cyl(S.floatTopD / 2, S.floatBotD / 2, S.floatH, fm, 'float_cup', 40, true), 0, S.floatH / 2, 0));
    f.add(at(cyl(S.floatBotD / 2, S.floatBotD / 2, 1.2, fm, 'float_bottom', 32), 0, 0.6, 0));
    f.add(at(new THREE.Mesh(new THREE.TorusGeometry(S.floatTopD / 2, 0.7, 8, 40), M.blue()), 0, S.floatH, 0));
    f.children[2].rotation.x = Math.PI / 2;
    f.position.set(D.flowX, S.seatTop, 0);
    g.add(f); parts.float = f;
  }
  // goal indicator slider (B20)
  {
    const gi = new THREE.Group(); gi.name = 'goal_indicator';
    const tri = new THREE.Shape(); tri.moveTo(0, 0); tri.lineTo(9, 4.2); tri.lineTo(9, -4.2); tri.lineTo(0, 0);
    const tg = new THREE.ExtrudeGeometry(tri, { depth: 2.4, bevelEnabled: false }); tg.translate(0, 0, -1.2);
    gi.add(mesh(tg, M.blue(), 'goal_pointer'));
    gi.add(at(box(2.6, 13, 6, M.blue(), 'goal_clip'), 9.5, 0, 0));
    const ang = 0.55, rr = S.volOD / 2 + 0.6;
    gi.position.set(D.volX + Math.sin(ang + Math.PI / 2) * rr * 0.98, D.zeroY + S.goalMl * D.mmPerMl, Math.cos(ang + Math.PI / 2) * rr + 10);
    gi.position.set(D.volX + S.volOD / 2 + 0.4, D.zeroY + S.goalMl * D.mmPerMl, 8);
    g.add(gi); parts.goal = gi;
  }
  // cap (figure-8, blue) + label (B07, B08)
  {
    const pts = [], xa = D.flowX - S.capLobeDF / 2, xb = D.volX + S.capLobeDV / 2, N = 160, k = 2.6;
    const rF = S.capLobeDF / 2, rV = S.capLobeDV / 2, waist = S.capWaist * rV;
    const top = x => {
      const cF = Math.abs(x - D.flowX) <= rF ? Math.sqrt(rF * rF - (x - D.flowX) ** 2) : -60;
      const cV = Math.abs(x - D.volX) <= rV ? Math.sqrt(rV * rV - (x - D.volX) ** 2) : -60;
      const w = (x > D.flowX && x < D.volX) ? waist : -60;
      return k * Math.log(Math.exp(cF / k) + Math.exp(cV / k) + Math.exp(w / k));
    };
    for (let i = 0; i <= N; i++) { const x = xa + (xb - xa) * (1 - Math.cos(Math.PI * i / N)) / 2; pts.push(new THREE.Vector2(x, Math.max(0, top(x)))); }
    const shp = new THREE.Shape();
    shp.moveTo(pts[0].x, 0);
    for (const p of pts) shp.lineTo(p.x, p.y);
    for (let i = pts.length - 1; i >= 0; i--) shp.lineTo(pts[i].x, -pts[i].y);
    const geo = new THREE.ExtrudeGeometry(shp, { depth: S.capT - 3, bevelEnabled: true, bevelThickness: 1.5, bevelSize: 1.5, bevelSegments: 4, curveSegments: 8 });
    geo.rotateX(-Math.PI / 2); geo.translate(0, D.capBottom + 1.5, 0);
    parts.cap = mesh(geo, M.blue(), 'cap'); g.add(parts.cap);
    const lab = canvasTex(512, 160, (c, w, h) => {
      c.fillStyle = '#f7f9fb'; c.beginPath(); c.ellipse(w / 2, h / 2, w / 2 - 4, h / 2 - 4, 0, 0, Math.PI * 2); c.fill();
      c.fillStyle = '#2a6fb5'; c.textAlign = 'center'; c.font = `italic 700 54px Georgia, serif`; c.fillText('Romsons', w / 2, 74);
      c.font = `600 30px ${FONT}`; c.fillStyle = '#4a5868'; c.fillText("PATIENT'S NAME", w / 2, 118);
    });
    const lp = mesh(new THREE.PlaneGeometry(44, 14), new THREE.MeshBasicMaterial({ map: lab, transparent: true }), 'cap_label', { cast: false });
    lp.rotation.x = -Math.PI / 2; g.add(at(lp, (D.flowX + D.volX) / 2, S.H + 0.05, 0));
  }
  // clear body: left side wall + back plate + handle (B19)
  {
    const bm = M.clear(); bm.opacity = 0.2;
    const h = D.capBottom - S.baseH, y = S.baseH + h / 2;
    const side = at(box(S.frameT, h, S.capLobeDF - 6, bm, 'body_side'), -S.baseW / 2 + S.frameT / 2, y, 0); side.castShadow = false;
    const back = at(box(D.volX + S.volOD / 2 + S.baseW / 2, h, S.frameT, bm, 'body_back'), (-S.baseW / 2 + D.volX + S.volOD / 2) / 2, y, -S.capLobeDV / 2 + 3);
    back.castShadow = false;
    g.add(side, back);
    const hd = S.handle, x0 = D.volX + S.volOD / 2 - 1, xo = SX(hd.outerX), hx0 = SX(hd.holeX0), hx1 = SX(hd.holeX1);
    const sh = new THREE.Shape();
    sh.moveTo(x0, S.baseH - 2); sh.lineTo(xo - 2, S.baseH - 2); sh.quadraticCurveTo(xo, S.baseH - 2, xo, S.baseH + 6);
    sh.lineTo(xo, hd.shoulderY); sh.quadraticCurveTo(xo, 150, (xo + SX(S.capW)) / 2, 168);
    sh.quadraticCurveTo(SX(S.capW) - 2, D.capBottom, SX(S.capW) - 6, D.capBottom); sh.lineTo(x0, D.capBottom); sh.lineTo(x0, S.baseH - 2);
    const hole = new THREE.Path(), rTop = (hx1 - hx0) / 2;
    hole.moveTo(hx0, hd.holeBottom + 4); hole.lineTo(hx0, hd.holeTop - rTop);
    hole.absarc((hx0 + hx1) / 2, hd.holeTop - rTop, rTop, Math.PI, 0, true);
    const n = 60;
    for (let i = 0; i <= n; i++) {
      const yy = hd.holeTop - rTop - i * (hd.holeTop - rTop - hd.holeBottom - 4) / n;
      const ph = (yy - hd.holeBottom - 6) / hd.gripPitch;
      const bump = (ph > 0 && ph < 4) ? hd.gripDepth * Math.sin(Math.PI * (ph % 1)) ** 2 : 0;
      hole.lineTo(hx1 - bump, yy);
    }
    hole.quadraticCurveTo(hx1, hd.holeBottom, hx1 - 4, hd.holeBottom); hole.lineTo(hx0 + 4, hd.holeBottom); hole.quadraticCurveTo(hx0, hd.holeBottom, hx0, hd.holeBottom + 4);
    sh.holes.push(hole);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: hd.thick - 3, bevelEnabled: true, bevelThickness: 1.5, bevelSize: 1.2, bevelSegments: 3, curveSegments: 24 });
    geo.translate(0, 0, -(hd.thick - 3) / 2);
    const hm = M.clear(); hm.opacity = 0.32; hm.roughness = 0.1;
    parts.handle = mesh(geo, hm, 'handle'); parts.handle.castShadow = false; g.add(parts.handle);
  }
  // hose + mouthpiece (built/updated by updateHose)
  parts.hose = mesh(new THREE.BufferGeometry(), new THREE.MeshPhysicalMaterial({ color: 0xf2f6f8, roughness: 0.3, transparent: true, opacity: 0.8, clearcoat: 0.5 }), 'corrugated_hose');
  parts.mouth = new THREE.Group(); parts.mouth.name = 'mouthpiece_filter';
  {
    const fm = M.frosted(); fm.opacity = 0.92;
    const filt = cyl(S.filterD / 2, S.filterD / 2, S.filterL, fm, 'filter_housing', 32); filt.position.y = S.filterL / 2;
    const mg = new THREE.CylinderGeometry(S.filterD / 2 - 1, S.filterD / 2 - 0.5, S.mouthL, 32, 8);
    const pa = mg.attributes.position;
    for (let i = 0; i < pa.count; i++) {
      const f = (pa.getY(i) + S.mouthL / 2) / S.mouthL;
      pa.setX(i, pa.getX(i) * (1 + f * (S.mouthW / (S.filterD - 1) - 1)));
      pa.setZ(i, pa.getZ(i) * (1 - 0.58 * f));
    }
    mg.computeVertexNormals();
    const mp = mesh(mg, fm, 'mouthpiece'); mp.position.y = S.filterL + S.mouthL / 2;
    parts.mouth.add(filt, mp);
  }
  g.add(parts.hose, parts.mouth);
  return { group: g, parts };
}

// Corrugated hose: a tube along a curve with a sinusoidal rib profile (B21)
const _v = new THREE.Vector3();
function ribbedTube(curve, r, pitch, amp, radial = 16) {
  const len = curve.getLength(), segs = Math.max(60, Math.round(len / pitch * 4));
  const g = new THREE.TubeGeometry(curve, segs, r, radial, false);
  const pos = g.attributes.position, ring = radial + 1, c = new THREE.Vector3();
  for (let i = 0; i <= segs; i++) {
    const u = i / segs; curve.getPointAt(u, c);
    const k = 1 + (amp / r) * Math.sin(2 * Math.PI * u * len / pitch);
    for (let j = 0; j < ring; j++) {
      const idx = i * ring + j; _v.fromBufferAttribute(pos, idx).sub(c).multiplyScalar(k).add(c); pos.setXYZ(idx, _v.x, _v.y, _v.z);
    }
  }
  g.computeVertexNormals(); return g;
}
let hoseKey = '';
function updateHose(spiro, groupWorldPos) {
  // The hose starts at the connector-tube port and lies on the table; the end stays put in the world.
  const p = spiro.parts.port, start = new THREE.Vector3(D.midX, S.portY, S.midOD / 2 + 11);
  const endW = new THREE.Vector3(-150, S.hoseOD / 2, 128);
  const end = endW.clone().sub(groupWorldPos);
  const k = `${end.x.toFixed(1)},${end.y.toFixed(1)},${end.z.toFixed(1)}`;
  if (k === hoseKey) return; hoseKey = k;
  const floorY = -groupWorldPos.y + S.hoseOD / 2;
  // forward out of the port, down in front of the base unit, then to the left along the table
  const frontZ = U.outerD / 2 + S.hoseOD / 2 + 8 - groupWorldPos.z;
  const pts = [
    start,
    new THREE.Vector3(start.x - 2, start.y - 4, start.z + 14),
    new THREE.Vector3(start.x - 8, Math.max(floorY + 24, start.y - 26), Math.max(start.z + 30, frontZ)),
    new THREE.Vector3(start.x - 22, floorY + 6, frontZ + 34),
    new THREE.Vector3(end.x + 70, floorY, end.z + 10),
    new THREE.Vector3(end.x + 30, floorY, end.z + 3),
    end,
  ];
  const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
  spiro.parts.hose.geometry.dispose();
  spiro.parts.hose.geometry = ribbedTube(curve, S.hoseOD / 2 - S.hoseRib / 2, S.hosePitch, S.hoseRib / 2);
  const dir = curve.getTangentAt(1).normalize();
  spiro.parts.mouth.position.copy(end);
  spiro.parts.mouth.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
  spiro.parts.hoseLength = curve.getLength();
}

// =====================================================================================
// SPIROBUDDY BASE UNIT — our design (D rows)
// =====================================================================================
function buildUnit() {
  const g = new THREE.Group(); g.name = 'SpiroBuddy_unit';
  const P = {};
  const W = U.outerW, Dp = U.outerD, R = U.cornerR, w = U.wall;
  const sensorX = D.volX;           // sensor sits right under the volume-chamber axis
  // ---- tray (bottom shell)
  const trayMat = xr(M.shellWhite());
  P.tray = new THREE.Group(); P.tray.name = 'tray';
  P.tray.add(mesh(extrudeY(roundRect(W, Dp, R), 0, U.floorT), trayMat, 'tray_floor'));
  { const s = roundRect(W, Dp, R); s.holes.push(roundRect(W - 2 * w, Dp - 2 * w, R - w)); P.tray.add(mesh(extrudeY(s, U.floorT, U.trayH - U.floorT), trayMat, 'tray_wall')); }
  // light bar (frosted, glows with the WS2812B behind it)
  P.lightBarMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: COL.idle, emissiveIntensity: 1.6, roughness: 0.4 });
  P.lightBar = at(rbox(U.lightBar.w, U.lightBar.h, w + 0.8, 1.2, P.lightBarMat, 'light_bar'), U.ledAt[0], U.frontY, Dp / 2 - w / 2 + 0.3);
  P.tray.add(P.lightBar);
  // USB-C cut-out on the left wall
  P.usbPort = at(rbox(w + 0.6, U.usbCut.h, U.usbCut.w, 1.6, M.black(), 'usb_c_port'), -W / 2 + w / 2 - 0.2, U.floorT + 8 + E.xiao.pcb + E.usbc.h / 2, U.xiaoAt[1]);
  P.tray.add(P.usbPort);
  // start button cap through the front wall
  P.button = new THREE.Group(); P.button.name = 'start_button';
  P.button.add(at(rbox(E.tact.s, E.tact.s, E.tact.h, 0.6, M.black(), 'tactile_switch'), 0, 0, Dp / 2 - w - E.tact.h / 2 - 0.5));
  const cap = cyl(U.buttonCapD / 2, U.buttonCapD / 2, w + 3, M.teal(), 'button_cap', 32); cap.rotation.x = Math.PI / 2; cap.position.z = Dp / 2 - w / 2 + 1.2;
  P.button.add(cap);
  P.button.position.set(U.buttonAt[0], U.frontY, 0);
  g.add(P.tray, P.button);
  // ---- lid (top shell) with the pocket the spirometer stands in
  const lidMat = xr(M.shellDark());
  P.lid = new THREE.Group(); P.lid.name = 'lid';
  { const s = roundRect(W, Dp, R); s.holes.push(roundRect(D.pocketW, D.pocketD, R - w)); P.lid.add(mesh(extrudeY(s, U.trayH, U.lidH), lidMat, 'lid_ring')); }
  { const s = roundRect(D.pocketW, D.pocketD, R - w); s.holes.push(circlePath(U.tunnelID / 2, sensorX, 0)); P.lid.add(mesh(extrudeY(s, D.plateTop - 2, 2), lidMat, 'pocket_floor')); }
  // foam collar lining the pocket + foam pads + foam ring around the sensor window
  const foamMat = M.foam();
  { const s = roundRect(D.pocketW, D.pocketD, R - w); s.holes.push(roundRect(D.pocketW - 2 * U.foam, D.pocketD - 2 * U.foam, R - w - U.foam)); P.lid.add(mesh(extrudeY(s, D.plateTop, U.pocketDepth), foamMat, 'foam_collar')); }
  for (const [px, pz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) P.lid.add(at(box(22, U.pad, 12, foamMat, 'foam_pad'), px * (D.pocketW / 2 - 18), D.plateTop + U.pad / 2, pz * (D.pocketD / 2 - 10)));
  { const s = circleShape(U.foamRingOD / 2, sensorX, 0); s.holes.push(circlePath(U.tunnelID / 2, sensorX, 0)); P.foamRing = mesh(extrudeY(s, D.plateTop, U.foamRingH), foamMat, 'sensor_foam_ring'); P.lid.add(P.foamRing); }
  // air vents: slots in the lid ring on both long sides (drawn as dark openings)
  for (const side of [-1, 1]) for (let i = 0; i < U.vent.n; i++) {
    const x = (i - (U.vent.n - 1) / 2) * 34;
    P.lid.add(at(rbox(U.vent.w, U.vent.h, w + 0.6, 1.5, M.black(), 'air_vent'), x, D.plateTop + U.vent.h / 2 + 0.2, side * (Dp / 2 - w / 2)));
  }
  // logo on the lid front
  const logo = canvasTex(512, 64, (c, ww, hh) => { c.fillStyle = '#e3f2f6'; c.font = `700 40px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('SpiroBuddy', ww / 2, hh / 2 + 2); });
  P.lid.add(at(mesh(new THREE.PlaneGeometry(56, 7), new THREE.MeshBasicMaterial({ map: logo, transparent: true }), 'logo', { cast: false }), 52, U.trayH + U.lidH / 2 - 1.5, Dp / 2 + 0.05));
  g.add(P.lid);
  // ---- light tunnel (black tube) from just above the sensor up to the pocket floor (D07)
  { const s = circleShape(U.tunnelOD / 2, sensorX, 0); s.holes.push(circlePath(U.tunnelID / 2, sensorX, 0));
    const y0 = D.sensorFaceY + 0.6; P.tunnel = mesh(extrudeY(s, y0, D.plateTop - 2 - y0), xr(M.foam()), 'light_tunnel'); g.add(P.tunnel); }
  // ---- VL53L1X on a Pololu-size carrier, face up (E04, E08)
  P.sensor = new THREE.Group(); P.sensor.name = 'VL53L1X_sensor';
  {
    const b = E.vlBoard, yb = U.floorT + U.standoff;
    P.sensor.add(at(box(b.w, b.t, b.l, M.pcbBlue(), 'vl53l1x_board'), 0, yb + b.t / 2, 0));
    P.sensor.add(at(box(E.vlChip.l, E.vlChip.h, E.vlChip.w, M.black(), 'vl53l1x_chip'), 0, yb + b.t + E.vlChip.h / 2, 0));
    for (const s of [-1, 1]) P.sensor.add(at(cyl(1.1, 1.1, U.standoff, M.metal(), 'standoff', 12), s * b.holePitch / 2, U.floorT + U.standoff / 2, -b.l / 2 + 2.5));
    const glass = at(cyl(0.7, 0.7, 0.2, new THREE.MeshBasicMaterial({ color: 0x5a1020 }), 'emitter', 12), -1.2, D.sensorFaceY + 0.1, 0);
    P.sensor.add(glass);
    P.sensor.position.set(sensorX, 0, 0);
    g.add(P.sensor);
  }
  // ---- XIAO ESP32-C3 with the USB-C at the left wall (E01–E03)
  P.xiao = new THREE.Group(); P.xiao.name = 'XIAO_ESP32C3';
  {
    const x = E.xiao, y = U.floorT + 8;
    P.xiao.add(at(box(x.l, x.pcb, x.w, M.pcbBlack(), 'xiao_pcb'), 0, y + x.pcb / 2, 0));
    P.xiao.add(at(rbox(E.usbc.l, E.usbc.h, E.usbc.w, 1.2, M.metal(), 'xiao_usb_c'), -x.l / 2 + E.usbc.l / 2 - 1, y + x.pcb + E.usbc.h / 2, 0));
    P.xiao.add(at(box(E.chipEsp, 0.9, E.chipEsp, M.black(), 'esp32c3_chip'), 3, y + x.pcb + 0.45, 0));
    P.xiao.add(at(box(2.4, 1.2, 1.6, M.metal(), 'u_fl'), x.l / 2 - 2.5, y + x.pcb + 0.6, x.w / 2 - 2.5));
    for (const s of [-1, 1]) for (let i = 0; i < 7; i++) P.xiao.add(at(box(1.5, 0.12, 1.2, M.metal(), 'pad'), -x.l / 2 + 2.8 + i * 2.54, y + x.pcb + 0.06, s * (x.w / 2 - 0.7)));
    for (const s of [-1, 1]) P.xiao.add(at(cyl(1.2, 1.2, 8, M.metal(), 'standoff', 10), s * 7, U.floorT + 4, 0));
    P.xiao.position.set(-W / 2 + w + x.l / 2 - 0.2, 0, U.xiaoAt[1]);
    g.add(P.xiao);
  }
  // ---- LiPo 500 mAh in its own compartment (E09)
  P.battery = new THREE.Group(); P.battery.name = 'LiPo_500mAh';
  {
    const b = E.lipo;
    P.battery.add(at(rbox(b.l, b.t, b.w, 1.5, M.pouch(), 'lipo_pouch'), 0, U.floorT + b.t / 2 + 0.2, 0));
    const lab = canvasTex(256, 200, (c, ww, hh) => { c.fillStyle = '#1b2a3a'; c.fillRect(0, 0, ww, hh); c.fillStyle = '#fff'; c.font = `700 40px ${FONT}`; c.textAlign = 'center'; c.fillText('3.7 V', ww / 2, 80); c.fillText(`${b.mAh} mAh`, ww / 2, 135); c.font = `500 22px ${FONT}`; c.fillText('LiPo · protected', ww / 2, 175); });
    const lp = mesh(new THREE.PlaneGeometry(b.l * 0.8, b.w * 0.7), new THREE.MeshStandardMaterial({ map: lab, roughness: 0.6 }), 'lipo_label', { cast: false });
    lp.rotation.x = -Math.PI / 2; P.battery.add(at(lp, 0, U.floorT + b.t + 0.25, 0));
    P.battery.add(at(box(4, 1.2, 8, M.black(), 'lipo_pcm'), -b.l / 2 - 1.5, U.floorT + 1.5, 0));
    const ribs = new THREE.Group(); ribs.name = 'battery_ribs';
    const rm = trayMat;
    ribs.add(at(box(b.l + 6, 7, 1.2, rm, 'rib'), 0, U.floorT + 3.5, b.w / 2 + 2), at(box(b.l + 6, 7, 1.2, rm, 'rib'), 0, U.floorT + 3.5, -b.w / 2 - 2));
    ribs.add(at(box(1.2, 7, b.w + 4, rm, 'rib'), b.l / 2 + 2.5, U.floorT + 3.5, 0));
    P.battery.position.set(U.batteryAt[0], 0, U.batteryAt[1]);
    P.ribs = ribs; ribs.position.copy(P.battery.position); g.add(ribs);
    g.add(P.battery);
  }
  // ---- passive piezo buzzer (E10)
  P.buzzer = new THREE.Group(); P.buzzer.name = 'piezo_buzzer';
  P.buzzer.add(at(cyl(E.piezo.d / 2, E.piezo.d / 2, E.piezo.h, M.black(), 'piezo_body', 40), 0, U.floorT + 0.5 + E.piezo.h / 2, 0));
  P.buzzer.add(at(cyl(1.0, 1.0, 0.3, M.metal(), 'piezo_hole', 16), 0, U.floorT + 0.5 + E.piezo.h + 0.1, 0));
  P.buzzer.position.set(U.buzzerAt[0], 0, U.buzzerAt[1]); g.add(P.buzzer);
  // ---- WS2812B mini PCB behind the light bar (E11)
  P.led = new THREE.Group(); P.led.name = 'WS2812B_LED';
  P.led.add(at(box(E.ledPcb.s, E.ledPcb.s, 1.0, M.pcbBlack(), 'ws2812b_pcb'), 0, 0, 0));
  P.ledMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: COL.idle, emissiveIntensity: 2.5 });
  P.led.add(at(box(E.ledPkg.s, E.ledPkg.s, E.ledPkg.t, P.ledMat, 'ws2812b_5050'), 0, 0, 0.5 + E.ledPkg.t / 2));
  P.led.position.set(U.ledAt[0], U.frontY, Dp / 2 - w - 0.5 - E.ledPkg.t - 0.5); g.add(P.led);
  P.glow = new THREE.PointLight(COL.idle, 0, 260, 2); P.glow.position.set(U.ledAt[0], U.frontY, Dp / 2 + 12); g.add(P.glow);
  // ---- wires (thin silicone wire, colour-coded)
  P.wires = new THREE.Group(); P.wires.name = 'wires';
  const xiaoPin = (i, side) => new THREE.Vector3(P.xiao.position.x - E.xiao.l / 2 + 2.8 + i * 2.54, U.floorT + 8 + E.xiao.pcb + 0.2, U.xiaoAt[1] + side * (E.xiao.w / 2 - 0.7));
  const wire = (pts, color) => {
    const c = new THREE.CatmullRomCurve3(pts.map(p => p.clone ? p : new THREE.Vector3(...p)));
    const m = mesh(new THREE.TubeGeometry(c, 64, 0.45, 6, false), M.wire(color), 'wire', { cast: false }); P.wires.add(m);
  };
  const sb = [sensorX, U.floorT + U.standoff + E.vlBoard.t, -E.vlBoard.l / 2 + 1];
  [[0xd62828, 3, 1], [0x111111, 2, 1], [0x2563eb, 4, -1], [0xeab308, 5, -1], [0x16a34a, 6, 1]].forEach(([c, pin, side], i) => {
    const s = new THREE.Vector3(sb[0] - 4 + i * 2, sb[1], sb[2]);
    wire([s, s.clone().add(new THREE.Vector3(0, 6, -6)), new THREE.Vector3(-10 + i * 2, 15, -30 + i), new THREE.Vector3(-50, 14, U.xiaoAt[1] - 12 + i), xiaoPin(pin, side).add(new THREE.Vector3(0, 4, side * 2)), xiaoPin(pin, side)], c);
  });
  [[0xd62828, 2, -1], [0x111111, 1, -1]].forEach(([c, pin, side], i) => {
    const s = new THREE.Vector3(U.buzzerAt[0] - 2 + i * 4, U.floorT + 0.5 + E.piezo.h, U.buzzerAt[1] + 4);
    wire([s, s.clone().add(new THREE.Vector3(0, 5, 2)), new THREE.Vector3(20, 16, -34 + i * 2), new THREE.Vector3(-40, 15, -36 + i), xiaoPin(pin, side).add(new THREE.Vector3(0, 4, -2)), xiaoPin(pin, side)], c);
  });
  [[0xd62828, 0, 1], [0x111111, 1, 1], [0x16a34a, 3, 1]].forEach(([c, pin, side], i) => {
    const s = new THREE.Vector3(U.ledAt[0] - 2 + i * 2, U.frontY - 4, P.led.position.z - 1);
    wire([s, new THREE.Vector3(s.x, 14, 26), new THREE.Vector3(-60 + i * 2, 13, 6), xiaoPin(pin, side).add(new THREE.Vector3(0, 4, 3)), xiaoPin(pin, side)], c);
  });
  [[0x7c3aed, 0, -1], [0x111111, 1, -1]].forEach(([c, pin, side], i) => {
    const s = new THREE.Vector3(U.buttonAt[0] - 1 + i * 2, U.frontY - 3, Dp / 2 - w - E.tact.h - 1);
    wire([s, new THREE.Vector3(s.x, 13, 20), new THREE.Vector3(10, 12, 2 + i * 2), new THREE.Vector3(-50, 13, -2 + i), xiaoPin(pin + 4, side).add(new THREE.Vector3(0, 4, -3)), xiaoPin(pin + 4, side)], c);
  });
  [[0xd62828, 0], [0x111111, 1]].forEach(([c], i) => {
    const s = new THREE.Vector3(U.batteryAt[0] - E.lipo.l / 2 - 3, U.floorT + 1.5, U.batteryAt[1] - 2 + i * 4);
    wire([s, new THREE.Vector3(-52, 5, 4 + i * 2), new THREE.Vector3(-66, 6, U.xiaoAt[1] + 6), new THREE.Vector3(P.xiao.position.x + 4 + i * 2, U.floorT + 8, U.xiaoAt[1] + 1)], c);
  });
  g.add(P.wires);
  // beep rings (sound illustration)
  P.rings = [];
  for (let i = 0; i < 3; i++) {
    const r = new THREE.Mesh(new THREE.TorusGeometry(1, 0.016, 8, 96), new THREE.MeshBasicMaterial({ color: COL.good, transparent: true, opacity: 0, depthWrite: false }));
    r.rotation.x = Math.PI / 2; r.position.y = 24; r.name = 'fx_ring'; r.userData.fx = true; g.add(r); P.rings.push(r);
  }
  return { group: g, parts: P, sensorX };
}

// =====================================================================================
// PHONE on a stand (ILLUSTRATIVE, P01) with a live canvas screen
// =====================================================================================
function buildPhone() {
  const ph = CFG.phone, g = new THREE.Group(); g.name = 'phone_on_stand';
  const stand = new THREE.Group(); stand.name = 'stand';
  const al = new THREE.MeshStandardMaterial({ color: 0xaab4bd, roughness: 0.35, metalness: 0.9 });
  stand.add(at(rbox(70, 4, 70, 2, al, 'stand_base'), 0, 2, 0));
  const back = rbox(60, 110, 4, 2, al, 'stand_back'); back.rotation.x = ph.tilt; at(back, 0, 58, -18); stand.add(back);
  stand.add(at(rbox(64, 8, 6, 2, al, 'stand_lip'), 0, 8, 22));
  g.add(stand);
  const phone = new THREE.Group(); phone.name = 'phone';
  phone.add(mesh(new RoundedBoxGeometry(ph.w, ph.h, ph.t, 5, ph.r), new THREE.MeshPhysicalMaterial({ color: 0x1a1d22, roughness: 0.3, metalness: 0.6, clearcoat: 1 }), 'phone_body'));
  const canvas = document.createElement('canvas'); canvas.width = 540; canvas.height = Math.round(540 * ph.screenH / ph.screenW);
  const tex = new THREE.CanvasTexture(canvas); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const scr = mesh(new THREE.PlaneGeometry(ph.screenW, ph.screenH), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }), 'phone_screen', { cast: false });
  scr.position.z = ph.t / 2 + 0.05; phone.add(scr);
  phone.rotation.x = ph.tilt;
  phone.position.set(0, ph.h / 2 + 6, 14);
  g.add(phone);
  g.position.set(...ph.at); g.rotation.y = ph.yaw;
  return { group: g, canvas, tex, ctx: canvas.getContext('2d'), phone };
}

// =====================================================================================
// ASSEMBLE
// =====================================================================================
const model = new THREE.Group(); model.name = 'SpiroBuddy_setup'; scene.add(model);
const spiro = buildSpirometer(); model.add(spiro.group);
const unit = buildUnit(); model.add(unit.group);
const phone = buildPhone(); model.add(phone.group);
// laser beam (illustration — the real 940 nm beam is invisible)
const beam = new THREE.Group(); beam.name = 'fx_laser'; beam.userData.fx = true;
const beamCone = new THREE.Mesh(new THREE.ConeGeometry(1, 1, 40, 1, true), new THREE.MeshBasicMaterial({ color: 0xe0284f, transparent: true, opacity: 0.25, depthWrite: false, side: THREE.DoubleSide }));
beamCone.geometry.rotateX(Math.PI); beamCone.geometry.translate(0, 0.5, 0);
const beamCore = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 1, 10), new THREE.MeshBasicMaterial({ color: 0xd61f45, transparent: true, opacity: 0.9, depthWrite: false }));
beamCore.geometry.translate(0, 0.5, 0);
const beamSpot = new THREE.Mesh(new THREE.CircleGeometry(1, 40), new THREE.MeshBasicMaterial({ color: 0xd61f45, transparent: true, opacity: 0.6, depthWrite: false, side: THREE.DoubleSide }));
beamSpot.rotation.x = Math.PI / 2;
beam.add(beamCone, beamCore, beamSpot); scene.add(beam);
// LED glow sprite
const glowSprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: canvasTex(128, 128, (c) => { const gr = c.createRadialGradient(64, 64, 2, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = gr; c.fillRect(0, 0, 128, 128); }), blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
glowSprite.scale.set(90, 26, 1); glowSprite.userData.fx = true; scene.add(glowSprite);

// X-ray outline: edges of the shell parts, shown when the shell turns see-through
const xrayEdges = [];
for (const part of [unit.parts.tray, unit.parts.lid]) {
  part.traverse(o => {
    if (!o.isMesh || !['tray_floor', 'tray_wall', 'lid_ring', 'pocket_floor'].includes(o.name)) return;
    const l = new THREE.LineSegments(new THREE.EdgesGeometry(o.geometry, 30), new THREE.LineBasicMaterial({ color: 0x0b6e8a, transparent: true, opacity: 0, depthWrite: false }));
    l.name = 'fx_xray_edges'; l.userData.fx = true; o.add(l); xrayEdges.push(l);
  });
}

// Exploded-view offsets (world mm per unit of "explode")
const EXPLODE = [
  [spiro.group, [0, 135, 0]], [unit.parts.lid, [0, 78, 0]], [unit.parts.tunnel, [0, 46, 0]], [unit.parts.sensor, [0, 26, 0]],
  [unit.parts.xiao, [-26, 36, 0]], [unit.parts.battery, [0, 16, 8]], [unit.parts.ribs, [0, 8, 8]], [unit.parts.buzzer, [16, 30, -8]],
  [unit.parts.led, [0, 34, 34]], [unit.parts.button, [0, 18, 40]],
];
for (const [o] of EXPLODE) o.userData.home = o.position.clone();

// Labels: [text, object, local offset]
const LABELS = [
  ['VL53L1X laser sensor', unit.parts.sensor, [0, D.sensorFaceY, 0], 'unit'],
  ['Light tunnel + foam ring', unit.parts.tunnel, [unit.sensorX + 12, 24, 0], 'unit'],
  ['XIAO ESP32-C3', unit.parts.xiao, [0, 12, 0], 'unit'],
  ['USB-C charging port', unit.parts.usbPort, [0, 0, 0], 'unit'],
  ['LiPo 500 mAh', unit.parts.battery, [0, 7, 0], 'unit'],
  ['Piezo beeper', unit.parts.buzzer, [0, 9, 0], 'unit'],
  ['WS2812B status light', unit.parts.led, [0, 0, 2], 'unit'],
  ['Start button', unit.parts.button, [0, 0, 44], 'unit'],
  ['Air vents', unit.parts.lid, [-17, 40, U.outerD / 2], 'unit'],
  ['Lid with foam-lined pocket', unit.parts.lid, [-70, 46, -20], 'unit'],
  ['Piston (disc)', spiro.parts.piston, [0, S.pistonH / 2, 0], 'spiro'],
  ['Volume chamber + mL scale', spiro.parts.volChamber, [0, 30, S.volOD / 2], 'spiro'],
  ['Flow indicator', spiro.parts.float, [0, S.floatH / 2, 0], 'spiro'],
  ['Goal marker', spiro.parts.goal, [0, 0, 0], 'spiro'],
  ['Corrugated hose', spiro.parts.hose, null, 'spiro'],
  ['Mouthpiece + filter', spiro.parts.mouth, [0, 30, 0], 'spiro'],
];

// =====================================================================================
// SCENE STATE → apply (pure function of the state object)
// =====================================================================================
const tmpV = new THREE.Vector3();
const lerp = (a, b, u) => a + (b - a) * u;
const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = u => u * u * (3 - 2 * u);
function applyState(st) {
  // positions
  unit.group.position.set(st.unitX || 0, 0, 0);
  const ex = st.explode || 0;
  for (const [o, off] of EXPLODE) o.position.copy(o.userData.home).add(tmpV.set(...off).multiplyScalar(ex));
  spiro.group.position.set(0, (st.spiroY ?? D.seatY) + 135 * ex, 0);
  phone.group.position.set(CFG.phone.at[0] + (st.phoneX || 0), CFG.phone.at[1], CFG.phone.at[2]);
  phone.group.visible = (st.phoneX || 0) < 900;
  updateHose(spiro, spiro.group.position);
  // breath
  const be = breathEval(st.sched || [], st.tB ?? 0);
  const co = coachEval(be, st.tB ?? 0);
  const vol = be.vol;
  spiro.parts.piston.position.y = D.pistonRestBottom + vol * D.mmPerMl;
  const fl = Math.max(0, be.r03);
  const zoneMid = (S.zoneBottomY + S.zoneTopY) / 2, restTop = S.seatTop + S.floatH;
  const lift = fl <= CFG.floatFlowForTarget ? (fl / CFG.floatFlowForTarget) * (zoneMid - restTop)
    : (zoneMid - restTop) + Math.min(1, (fl - CFG.floatFlowForTarget) / (CFG.floatMaxFlow - CFG.floatFlowForTarget)) * (S.zoneTopY - zoneMid);
  spiro.parts.float.position.y = S.seatTop + Math.max(0, lift);
  // LED
  const ledOn = (st.unitX || 0) < 400;
  const c = new THREE.Color(co.led);
  unit.parts.ledMat.emissive.copy(c); unit.parts.lightBarMat.emissive.copy(c);
  unit.parts.lightBarMat.emissiveIntensity = ledOn ? 1.7 : 0;
  unit.parts.glow.color.copy(c); unit.parts.glow.intensity = ledOn ? 1800 : 0;
  glowSprite.material.color.copy(c); glowSprite.material.opacity = ledOn ? 0.75 : 0;
  unit.parts.lightBar.getWorldPosition(glowSprite.position); glowSprite.position.z += 3;
  // beep rings: good breath end (green) and the live "too fast" moment (amber)
  let ringT = null, ringCol = COL.good;
  if (be.lastDone && be.result.label === 'good' && st.tB - be.lastEnd < 1.6) ringT = st.tB - be.lastEnd;
  if (be.active && be.fastAt !== null && st.tB - be.fastAt < 1.6 && st.tB >= be.fastAt) { ringT = st.tB - be.fastAt; ringCol = COL.fast; }
  unit.parts.rings.forEach((r, i) => {
    const u = ringT === null ? -1 : (ringT - i * 0.22) / 1.1;
    r.visible = u > 0 && u < 1 && ledOn;
    if (r.visible) { const s = lerp(70, 190, u); r.scale.set(s, s, s); r.material.opacity = (1 - u) * 0.9; r.material.color.set(ringCol); r.position.y = 30 + 20 * u; }
  });
  // X-ray
  const xa = st.xray || 0;
  for (const l of xrayEdges) { l.material.opacity = 0.55 * xa; l.visible = xa > 0.02; }
  for (const { mat, base } of xrayMats) { mat.opacity = lerp(base, Math.min(base, 0.14), xa); mat.depthWrite = mat.opacity > 0.95; }
  // wires fade during explode
  for (const w of unit.parts.wires.children) { w.material.opacity = 1 - clamp01(ex * 4); w.visible = w.material.opacity > 0.01; }
  // laser
  const sensorW = new THREE.Vector3(); unit.parts.sensor.localToWorld(sensorW.set(0, D.sensorFaceY, 0));
  const pistonBottomW = spiro.group.position.y + spiro.parts.piston.position.y;
  const dist = pistonBottomW - sensorW.y;
  const la = st.laser || 0;
  beam.visible = la > 0.01;
  beam.position.copy(sensorW);
  const rr = Math.tan(THREE.MathUtils.degToRad(E.vlRoiDeg / 2)) * dist;
  beamCone.scale.set(rr, dist, rr); beamCore.scale.set(1, dist, 1);
  beamSpot.position.set(0, dist - 0.3, 0); beamSpot.scale.set(rr, rr, rr);
  beamCone.material.opacity = 0.26 * la; beamCore.material.opacity = 0.9 * la; beamSpot.material.opacity = 0.7 * la;
  // phone screen
  if (phone.group.visible) drawPhone(st, be, co);
  return { be, co, dist, vol };
}

// =====================================================================================
// PHONE SCREENS (illustrative patient-app look)
// =====================================================================================
function rr(c, x, y, w, h, r) { c.beginPath(); c.roundRect(x, y, w, h, r); }
function chip(c, x, y, text, bg, fg = '#fff', size = 26) {
  c.font = `700 ${size}px ${FONT}`; const w = c.measureText(text).width + 28; rr(c, x, y, w, size + 18, (size + 18) / 2); c.fillStyle = bg; c.fill();
  c.fillStyle = fg; c.textBaseline = 'middle'; c.fillText(text, x + 14, y + (size + 18) / 2 + 1); c.textBaseline = 'alphabetic'; return w;
}
const LABEL_BG = { good: '#2e9d4e', too_fast: '#d97706', too_shallow: '#2563eb', no_hold: '#7c3aed' };
let phoneKey = '';
function drawPhone(st, be, co) {
  const p = st.phone || { screen: 'live' };
  const key = JSON.stringify([p.screen, Math.round(be.vol / 5), co.en, be.done.length, Math.round((p.progress || 0) * 60), be.lastDone && be.lastDone.t0, st.countOffset]);
  if (key === phoneKey) return; phoneKey = key;
  const c = phone.ctx, W = phone.canvas.width, H = phone.canvas.height;
  c.save(); c.textAlign = 'left';
  c.fillStyle = '#f4f6f9'; c.fillRect(0, 0, W, H);
  // status bar
  c.fillStyle = '#13202e'; c.font = `600 22px ${FONT}`; c.fillText('9:41', 30, 40); c.textAlign = 'right'; c.fillText('BT ● 92%', W - 30, 40); c.textAlign = 'left';
  if (p.screen === 'live') {
    c.fillStyle = '#0b6e8a'; c.font = `800 34px ${FONT}`; c.fillText('SpiroBuddy', 30, 96);
    const n = Math.min(CFG.coach.session, (st.countOffset || 0) + be.done.length + (be.active ? 1 : 0));
    c.fillStyle = '#4a5868'; c.font = `600 26px ${FONT}`; c.textAlign = 'right'; c.fillText(`Breath ${Math.max(1, n)} of ${CFG.coach.session}`, W - 30, 96); c.textAlign = 'left';
    // gauge (vertical bar) with target line
    const gx = 60, gy = 140, gw = 150, gh = 560, max = S.scaleMax;
    rr(c, gx, gy, gw, gh, 26); c.fillStyle = '#dbe1e8'; c.fill();
    const fh = gh * Math.min(1, be.vol / max);
    const tone = co.tone === 'fast' ? '#f0a020' : (co.tone === 'good' ? '#2e9d4e' : '#0b6e8a');
    c.save(); rr(c, gx, gy, gw, gh, 26); c.clip(); c.fillStyle = tone; c.fillRect(gx, gy + gh - fh, gw, fh); c.restore();
    const ty = gy + gh - gh * CFG.coach.target / max;
    c.strokeStyle = '#13202e'; c.lineWidth = 4; c.setLineDash([12, 8]); c.beginPath(); c.moveTo(gx - 16, ty); c.lineTo(gx + gw + 16, ty); c.stroke(); c.setLineDash([]);
    c.fillStyle = '#13202e'; c.font = `700 22px ${FONT}`; c.fillText('Target', gx + gw + 24, ty - 6); c.font = `600 22px ${FONT}`; c.fillText(`${CFG.coach.target} mL`, gx + gw + 24, ty + 20);
    c.font = `800 92px ${FONT}`; c.fillStyle = '#13202e'; c.fillText(String(Math.round(be.vol / 10) * 10), 250, 470);
    c.font = `600 32px ${FONT}`; c.fillStyle = '#4a5868'; c.fillText('mL', 250, 512);
    // speed meter
    const sx = 250, sy = 560, sw = 240;
    c.fillStyle = '#4a5868'; c.font = `600 22px ${FONT}`; c.fillText('Speed', sx, sy + 48);
    const segs = [['#2e9d4e', 0.5], ['#f0a020', 0.25], ['#c62828', 0.25]]; let ox = sx;
    for (const [col, f] of segs) { c.fillStyle = col; c.fillRect(ox, sy, sw * f, 18); ox += sw * f; }
    const fr = Math.min(1, Math.max(0, be.r03) / 2000);
    c.fillStyle = '#13202e'; c.beginPath(); c.moveTo(sx + sw * fr, sy - 2); c.lineTo(sx + sw * fr - 10, sy - 18); c.lineTo(sx + sw * fr + 10, sy - 18); c.fill();
    // coaching text
    rr(c, 30, 740, W - 60, 190, 28); c.fillStyle = co.tone === 'fast' ? '#fff5e0' : (co.tone === 'good' ? '#e7f6ec' : '#e3f2f6'); c.fill();
    c.fillStyle = '#13202e'; fitText(c, co.en, 56, 812, W - 112, 800, 46);
    c.fillStyle = '#4a5868'; fitText(c, co.hi, 56, 880, W - 112, 700, 46);
    // last breath result
    const res = be.result;
    c.fillStyle = '#13202e'; c.font = `700 26px ${FONT}`; c.fillText('Last breath', 30, 990);
    if (res) {
      c.font = `800 64px ${FONT}`; c.fillText(`${res.score.toFixed(1)}`, 30, 1070); const sw2 = c.measureText(`${res.score.toFixed(1)}`).width;
      c.font = `600 30px ${FONT}`; c.fillStyle = '#4a5868'; c.fillText('/ 10', 40 + sw2, 1070);
      chip(c, 250, 1022, LBL[res.label], LABEL_BG[res.label], '#fff', 30);
      c.fillStyle = '#6b7888'; c.font = `500 20px ${FONT}`; c.fillText('labelled by our own ML model', 250, 1100);
    } else { c.fillStyle = '#6b7888'; c.font = `600 30px ${FONT}`; c.fillText('—', 30, 1060); }
  } else if (p.screen === 'checklist') {
    c.fillStyle = '#0b6e8a'; c.font = `800 34px ${FONT}`; c.fillText("Today's breathing", 30, 96);
    c.fillStyle = '#4a5868'; c.font = `600 24px ${FONT}`; c.fillText('Ravi Kumar · 10 breaths every hour', 30, 134);
    const hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];
    const doneN = 8 + Math.floor(clamp01(p.progress || 0) * 2.999);
    hours.forEach((h, i) => {
      const y = 170 + i * 66, done = i < doneN, missed = i === 3;
      rr(c, 30, y, W - 60, 56, 16); c.fillStyle = done ? (missed ? '#fdecec' : '#e7f6ec') : '#ffffff'; c.fill();
      c.fillStyle = '#13202e'; c.font = `700 26px ${FONT}`; c.fillText(`${String(h).padStart(2, '0')}:00`, 54, y + 37);
      c.font = `600 22px ${FONT}`; c.fillStyle = '#4a5868';
      c.fillText(done ? (missed ? 'missed' : `done · best ${1500 + ((i * 137) % 400)} mL`) : (i === doneN ? 'now' : 'upcoming'), 170, y + 36);
      const cx = W - 70, cy = y + 28;
      c.beginPath(); c.arc(cx, cy, 18, 0, Math.PI * 2); c.fillStyle = done ? (missed ? '#c62828' : '#2e9d4e') : '#dbe1e8'; c.fill();
      c.strokeStyle = '#fff'; c.lineWidth = 5; c.beginPath();
      if (done && !missed) { c.moveTo(cx - 9, cy); c.lineTo(cx - 2, cy + 7); c.lineTo(cx + 10, cy - 7); } else if (missed) { c.moveTo(cx - 7, cy - 7); c.lineTo(cx + 7, cy + 7); c.moveTo(cx + 7, cy - 7); c.lineTo(cx - 7, cy + 7); }
      c.stroke();
    });
  } else if (p.screen === 'whatsapp') {
    c.fillStyle = '#075e54'; c.fillRect(0, 56, W, 96);
    c.fillStyle = '#fff'; c.font = `700 30px ${FONT}`; c.fillText('SpiroBuddy updates', 104, 102); c.font = `500 20px ${FONT}`; c.fillText('Family group · Ravi', 104, 132);
    c.beginPath(); c.arc(60, 104, 28, 0, Math.PI * 2); c.fillStyle = '#0b6e8a'; c.fill();
    c.fillStyle = '#efeae2'; c.fillRect(0, 152, W, H - 152);
    const msgs = [
      ['Good evening! Ravi did 9 of 14 breathing sessions today.', 'Best breath: 1,850 mL (92% of his target). He held each breath well.', 'आज रवि ने 14 में से 9 सत्र पूरे किए। शाबाश!', '— sent automatically by SpiroBuddy · not medical advice'],
    ];
    const lines = msgs[0], prog = clamp01(p.progress || 0);
    const shown = Math.max(1, Math.ceil(prog * lines.length * 1.25));
    rr(c, 30, 190, W - 80, 470, 22); c.fillStyle = '#ffffff'; c.fill();
    c.fillStyle = '#111b21'; let y = 238;
    lines.slice(0, shown).forEach((ln, i) => {
      c.font = i === 3 ? `italic 500 20px ${FONT}` : (i === 2 ? `600 26px ${FONT}` : `500 26px ${FONT}`);
      c.fillStyle = i === 3 ? '#667781' : '#111b21';
      for (const wl of wrap(c, ln, W - 130)) { c.fillText(wl, 54, y); y += 36; }
      y += 14;
    });
    c.fillStyle = '#667781'; c.font = `500 18px ${FONT}`; c.fillText('20:01 ✓✓', W - 150, 640);
  }
  c.restore();
  phone.tex.needsUpdate = true;
}
function fitText(c, text, x, y, maxW, weight, size) {
  let s = size; do { c.font = `${weight} ${s}px ${FONT}`; s -= 2; } while (c.measureText(text).width > maxW && s > 18);
  c.fillText(text, x, y);
}
function wrap(c, text, maxW) {
  const words = text.split(' '), out = []; let line = '';
  for (const w of words) { const t = line ? line + ' ' + w : w; if (c.measureText(t).width > maxW && line) { out.push(line); line = w; } else line = t; }
  if (line) out.push(line); return out;
}

// =====================================================================================
// CAMERA (spherical around a target) + KEYFRAME TRACKS
// =====================================================================================
function camFrom(cs) {
  const az = THREE.MathUtils.degToRad(cs.az), el = THREE.MathUtils.degToRad(cs.el);
  camera.position.set(cs.tx + cs.dist * Math.sin(az) * Math.cos(el), cs.ty + cs.dist * Math.sin(el), cs.tz + cs.dist * Math.cos(az) * Math.cos(el));
  camera.lookAt(cs.tx, cs.ty, cs.tz);
}
const C = (az, el, dist, tx = 40, ty = 100, tz = 10) => ({ az, el, dist, tx, ty, tz });
function lerpAny(a, b, u) {
  if (typeof a === 'number') return lerp(a, b, u);
  const o = {}; for (const k in a) o[k] = lerp(a[k], b[k], u); return o;
}
function track(keys, t) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) {
    const [t0, a] = keys[i - 1], [t1, b] = keys[i];
    return lerpAny(a, b, smooth(clamp01((t - t0) / Math.max(1e-6, t1 - t0))));
  }
  return keys[keys.length - 1][1];
}
function captionAt(list, t) {
  for (const [a, b, text] of list) if (t >= a && t < b) return { text, alpha: Math.min(clamp01((t - a) / 0.4), clamp01((b - t) / 0.4)) };
  return null;
}

// =====================================================================================
// VIDEO / TOUR SCRIPTS — every frame is a pure function of time t
// =====================================================================================
const SEAT = D.seatY;
const VIDEOS = {
  tour: {
    title: 'SpiroBuddy – guided tour', duration: 92,
    chapters: [[0, 'The problem'], [10, 'Meet SpiroBuddy'], [20, "What's inside"], [34, 'How it measures'], [47, 'Live voice coaching'], [64, 'Our own AI model'], [77, 'Progress & family updates'], [86, 'SpiroBuddy']],
    sched: [{ t0: 3.2, type: 'too_fast' }, { t0: 34.8, type: 'good' }, { t0: 49.0, type: 'too_fast' }, { t0: 54.6, type: 'good' }, { t0: 65.0, type: 'too_shallow' }, { t0: 72.6, type: 'no_hold' }],
    countOffset: 2,
    tracks: {
      cam: [[0, C(28, 12, 560, 0, 100, 0)], [9, C(-12, 12, 520, 0, 100, 0)], [11, C(-6, 14, 660, 0, 125, 0)], [17, C(22, 16, 660, 10, 115, 0)], [20.5, C(32, 22, 760, 0, 150, 0)],
            [26, C(-34, 24, 800, 0, 165, 0)], [30.5, C(-26, 22, 800, 0, 165, 0)], [33.5, C(-18, 18, 680, 0, 125, 0)],
            // chapter 4 – close-up from the front-right so the two chambers sit side by side (looking along the x axis
            // lines them up one behind the other and, with X-ray on, reads as a doubled spirometer)
            [35, C(32, 12, 520, D.volX, 80, 0)], [41, C(42, 10, 540, D.volX, 84, 0)], [46, C(36, 11, 530, D.volX, 84, 0)],
            [48.5, C(14, 12, 560, 90, 108, 25)], [63, C(-6, 13, 545, 90, 108, 25)], [65, C(18, 11, 545, 90, 110, 25)], [76, C(6, 10, 530, 90, 110, 25)],
            [78, C(24, 6, 330, 200, 86, 60)], [85.5, C(18, 7, 320, 200, 86, 60)], [88.5, C(14, 16, 760, 60, 105, 10)], [92, C(4, 16, 800, 60, 105, 10)]],
      unitX: [[0, 560], [11.6, 560], [14.2, 0]],
      spiroY: [[0, 0], [10.6, 0], [12.0, SEAT + 34], [14.4, SEAT + 34], [16.0, SEAT]],
      phoneX: [[0, 1000], [44, 1000], [47, 0]],
      explode: [[0, 0], [20.5, 0], [23.5, 1], [30.5, 1], [33.5, 0]],
      xray: [[0, 0], [20.5, 0], [22, 1], [45, 1], [47, 0]],
      labels: [[0, 0], [23, 0], [24, 1], [30.5, 1], [31.5, 0]],
      laser: [[0, 0], [33.8, 0], [34.6, 1], [45.5, 1], [46.5, 0]],
    },
    phone: t => (t < 77.5 ? { screen: 'live' } : t < 81.8 ? { screen: 'checklist', progress: (t - 78) / 3 } : { screen: 'whatsapp', progress: (t - 82) / 2.6 }),
    captions: [
      [0.3, 5, 'After surgery, patients go home with an incentive spirometer.'],
      [5, 9.8, 'At home nobody sees if they use it — or if they breathe too fast, too shallow, or skip the hold.'],
      [10, 15.6, 'Meet SpiroBuddy: a base unit. The spirometer simply stands on it.'],
      [15.6, 19.8, "Nothing touches the patient's breath — the air path stays exactly as Romsons designed it."],
      [20, 27, 'Inside: a VL53L1X laser distance sensor, a XIAO ESP32-C3 and a 500 mAh LiPo battery…'],
      [27, 33.8, '…a piezo beeper, a WS2812B status light, a start button, and USB-C charging.'],
      [34, 39.6, 'The sensor looks up through a light tunnel at the underside of the piston, 30 times a second.'],
      [39.6, 46.8, 'Distance → mL, calibrated with the spirometer’s own printed marks. (The 940 nm beam is invisible – drawn for illustration.)'],
      [47, 54.4, 'Too fast? The light turns amber and the phone says “Slower…” – “धीरे…”'],
      [54.4, 63.8, 'A slow, deep breath with a 3-second hold: green light, a beep, and a score out of 10.'],
      [64, 71, 'Our own trained model labels every breath — here: too shallow…'],
      [71, 76.8, '…and no hold. Each label comes with one simple tip.'],
      [77, 81.6, "Each hourly session ticks itself off on today's checklist."],
      [81.6, 85.8, 'Every evening the family gets a short WhatsApp update. Alerts come from rules, not AI.'],
      [86, 92, 'SpiroBuddy — coaching every breath at home.'],
    ],
    labelGroups: t => (t < 64 ? ['unit'] : []),
    hud: t => t < 77,
  },
  hero: {
    title: 'SpiroBuddy – 360°', duration: 20, chapters: [[0, 'SpiroBuddy']],
    sched: [{ t0: 1.0, type: 'good' }, { t0: 11.2, type: 'too_fast' }, { t0: 15.6, type: 'good' }], countOffset: 4,
    tracks: { cam: [[0, C(0, 14, 660, 60, 105, 20)], [20, C(360, 14, 660, 60, 105, 20)]], unitX: [[0, 0]], spiroY: [[0, SEAT]], phoneX: [[0, 0]], explode: [[0, 0]], xray: [[0, 0]], labels: [[0, 0]], laser: [[0, 0]] },
    phone: () => ({ screen: 'live' }), captions: [[0.3, 4.5, 'SpiroBuddy — a smart base for an ordinary Romsons Breazer 2500.']], labelGroups: () => [],
  },
  'breath-types': {
    title: 'Four breath types', duration: 35, chapters: [[0, 'Good'], [10.5, 'Too fast'], [16.5, 'Too shallow'], [25.5, 'No hold']],
    sched: [{ t0: 1.0, type: 'good' }, { t0: 11.0, type: 'too_fast' }, { t0: 17.0, type: 'too_shallow' }, { t0: 26.0, type: 'no_hold' }], countOffset: 0,
    tracks: { cam: [[0, C(-10, 10, 700, 165, 105, 20)], [35, C(10, 10, 690, 165, 105, 20)]], unitX: [[0, 0]], spiroY: [[0, SEAT]], phoneX: [[0, 0]], explode: [[0, 0]], xray: [[0, 0.65]], labels: [[0, 0]], laser: [[0, 1]] },
    phone: () => ({ screen: 'live' }),
    captions: [[0.3, 10, 'Good: slow rise, deep, held for 3 s.'], [10.5, 16.4, 'Too fast: the disc shoots up — amber light, “Slower…”'], [16.5, 25.4, 'Too shallow: under half the 2000 mL target.'], [25.5, 35, 'No hold: deep, but let go straight away.']],
    labelGroups: () => [], panel: true,
  },
  exploded: {
    title: 'Exploded view', duration: 15, chapters: [[0, "What's inside"]], sched: [], countOffset: 0,
    tracks: { cam: [[0, C(-40, 22, 720, 0, 130, 0)], [15, C(60, 24, 720, 0, 130, 0)]], unitX: [[0, 0]], spiroY: [[0, SEAT]], phoneX: [[0, 1000]], explode: [[0, 0], [1, 0], [4, 1], [11, 1], [14, 0]], xray: [[0, 0], [1, 0], [2.5, 1], [12.5, 1], [14, 0]], labels: [[0, 0], [3.5, 0], [4.5, 1], [10.6, 1], [11.6, 0]], laser: [[0, 0]] },
    phone: () => ({ screen: 'live' }), captions: [[0.3, 3.5, 'SpiroBuddy base unit — exploded view'], [11.8, 15, 'Everything fits in a 46 mm-tall base under the spirometer.']], labelGroups: () => ['unit', 'spiro'],
  },
};
function videoState(id, t) {
  const v = VIDEOS[id], T = v.tracks;
  return {
    cam: (c => ({ ...c, dist: c.dist * (v.camScale ?? 1.25) }))(track(T.cam, t)), hud: v.hud ? v.hud(t) : true, unitX: track(T.unitX, t), spiroY: track(T.spiroY, t), phoneX: track(T.phoneX, t),
    explode: track(T.explode, t), xray: track(T.xray, t), labels: track(T.labels, t), laser: track(T.laser, t),
    sched: v.sched, tB: t, countOffset: v.countOffset, phone: v.phone(t), caption: captionAt(v.captions, t),
    labelGroups: v.labelGroups(t), chapters: v.chapters, duration: v.duration, t, panel: v.panel, title: v.title,
  };
}

// =====================================================================================
// 2D OVERLAY: labels, captions, HUD, logo, chapter bar
// =====================================================================================
const ov = ovCanvas.getContext('2d');
function project(obj, off, Wpx, Hpx) {
  if (off === null) { // hose: pick a point along the hose geometry
    const pos = obj.geometry.attributes.position; if (!pos) return null;
    tmpV.fromBufferAttribute(pos, Math.floor(pos.count * 0.55)); obj.localToWorld(tmpV);
  } else { tmpV.set(...off); obj.localToWorld(tmpV); }
  const p = tmpV.clone().project(camera);
  if (p.z > 1) return null;
  return { x: (p.x * 0.5 + 0.5) * Wpx, y: (-p.y * 0.5 + 0.5) * Hpx };
}
function drawLabels(ctx, Wpx, Hpx, alpha, groups, bounds, scale = 1) {
  if (alpha <= 0.01) return;
  const items = [];
  for (const [text, obj, off, grp] of LABELS) {
    if (!groups.includes(grp)) continue;
    if (!obj.visible) continue;
    const p = project(obj, off, Wpx, Hpx); if (!p) continue;
    items.push({ text, ...p });
  }
  const midX = Wpx / 2, left = items.filter(i => i.x < midX).sort((a, b) => a.y - b.y), right = items.filter(i => i.x >= midX).sort((a, b) => a.y - b.y);
  const gap = 34 * scale, top = bounds.top, bottom = Hpx - bounds.bottom;
  const place = arr => { let y = top; for (const it of arr) { it.ly = Math.max(y, Math.min(it.y, bottom)); y = it.ly + gap; } for (let i = arr.length - 1; i >= 0; i--) { const lim = i === arr.length - 1 ? bottom : arr[i + 1].ly - gap; if (arr[i].ly > lim) arr[i].ly = lim; } };
  place(left); place(right);
  ctx.save(); ctx.globalAlpha = alpha; ctx.font = `600 ${15 * scale}px ${FONT}`; ctx.textBaseline = 'middle';
  const drawSide = (arr, isLeft) => {
    for (const it of arr) {
      const tw = ctx.measureText(it.text).width, pad = 9 * scale, bh = 26 * scale;
      const bx = isLeft ? bounds.left : Wpx - bounds.right - tw - pad * 2;
      const ex = isLeft ? bx + tw + pad * 2 : bx;
      ctx.strokeStyle = 'rgba(19,32,46,0.75)'; ctx.lineWidth = 1.4 * scale;
      ctx.beginPath(); ctx.moveTo(ex, it.ly); ctx.lineTo(lerp(ex, it.x, 0.18), it.ly); ctx.lineTo(it.x, it.y); ctx.stroke();
      ctx.fillStyle = '#0b6e8a'; ctx.beginPath(); ctx.arc(it.x, it.y, 4 * scale, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5 * scale; ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,0.94)'; rr(ctx, bx, it.ly - bh / 2, tw + pad * 2, bh, 7 * scale); ctx.fill();
      ctx.strokeStyle = 'rgba(11,110,138,0.5)'; ctx.lineWidth = 1 * scale; ctx.stroke();
      ctx.fillStyle = '#13202e'; ctx.fillText(it.text, bx + pad, it.ly + 1);
    }
  };
  drawSide(left, true); drawSide(right, false);
  ctx.restore();
}
function drawBeamNote(ctx, Wpx, Hpx, alpha, scale, info, callout = false) {
  if (alpha <= 0.01) return;
  ctx.save(); ctx.globalAlpha = alpha; ctx.textBaseline = 'middle';
  const l2 = 'Beam drawn for illustration – 940 nm IR is invisible';
  if (!callout || !info) {
    // phone at home (interactive mode, breath-types video): small tag under the sensor, clear of the phone
    const p = project(unit.parts.sensor, [0, D.sensorFaceY + 30, 0], Wpx, Hpx); if (!p) { ctx.restore(); return; }
    ctx.font = `600 ${14 * scale}px ${FONT}`; const tw = ctx.measureText(l2).width;
    const x = p.x + 40 * scale, y = p.y + 50 * scale;
    ctx.fillStyle = 'rgba(253,236,236,0.96)'; rr(ctx, x, y - 14 * scale, tw + 20 * scale, 28 * scale, 8 * scale); ctx.fill();
    ctx.strokeStyle = 'rgba(198,40,40,0.55)'; ctx.stroke();
    ctx.fillStyle = '#c62828'; ctx.fillText(l2, x + 10 * scale, y + 1);
    ctx.restore(); return;
  }
  // phone away (tour chapter 4): live "distance → mL" callout beside the beam, half-way up, clear of the caption
  const up = D.sensorFaceY + Math.max(24, info.dist * 0.5);
  const p = project(unit.parts.sensor, [S.volOD / 2 + 10, up, 0], Wpx, Hpx), tip = project(unit.parts.sensor, [0, up, 0], Wpx, Hpx);
  if (!p) { ctx.restore(); return; }
  const l1 = `Laser ${info.dist.toFixed(1)} mm  →  ${Math.round(info.vol)} mL`;
  ctx.font = `800 ${17 * scale}px ${FONT}`; const w1 = ctx.measureText(l1).width;
  ctx.font = `600 ${13 * scale}px ${FONT}`; const w2 = ctx.measureText(l2).width;
  const pad = 10 * scale, bw = Math.max(w1, w2) + pad * 2, bh = 54 * scale;
  const x = Math.min(Wpx - bw - 16, p.x + 24 * scale), y = Math.max(16, Math.min(Hpx - 260 * scale - bh, p.y - bh / 2));
  if (tip) { ctx.strokeStyle = 'rgba(19,32,46,0.6)'; ctx.lineWidth = 1.4 * scale; ctx.beginPath(); ctx.moveTo(tip.x, tip.y); ctx.lineTo(x, y + bh / 2); ctx.stroke(); }
  ctx.fillStyle = 'rgba(255,255,255,0.95)'; rr(ctx, x, y, bw, bh, 8 * scale); ctx.fill();
  ctx.strokeStyle = 'rgba(11,110,138,0.55)'; ctx.lineWidth = 1 * scale; ctx.stroke();
  ctx.fillStyle = '#0b6e8a'; ctx.font = `800 ${17 * scale}px ${FONT}`; ctx.fillText(l1, x + pad, y + 18 * scale);
  ctx.fillStyle = '#c62828'; ctx.font = `600 ${13 * scale}px ${FONT}`; ctx.fillText(l2, x + pad, y + bh - 14 * scale);
  ctx.restore();
}
function drawVideoOverlay(ctx, st, info, Wpx, Hpx) {
  ctx.clearRect(0, 0, Wpx, Hpx);
  drawLabels(ctx, Wpx, Hpx, st.labels, st.labelGroups, { left: 60, right: 60, top: 150, bottom: 230 }, 1.25);
  drawBeamNote(ctx, Wpx, Hpx, st.laser, 1.3, info, (st.phoneX || 0) > 0);
  // chapter title
  const ch = currentChapter(st.chapters, st.t);
  ctx.save();
  ctx.fillStyle = 'rgba(255,255,255,0.88)'; rr(ctx, 48, 40, 560, 74, 16); ctx.fill();
  ctx.fillStyle = '#0b6e8a'; ctx.font = `700 18px ${FONT}`; ctx.fillText(st.chapters.length > 1 ? `CHAPTER ${ch.i + 1} / ${st.chapters.length}` : st.title.toUpperCase(), 70, 70);
  ctx.fillStyle = '#13202e'; ctx.font = `800 30px ${FONT}`; ctx.fillText(ch.name, 70, 102);
  // logo
  ctx.textAlign = 'right'; ctx.fillStyle = '#0b6e8a'; ctx.font = `800 40px ${FONT}`; ctx.fillText('SpiroBuddy', Wpx - 56, 88);
  ctx.beginPath(); ctx.arc(Wpx - 56 - ctx.measureText('SpiroBuddy').width - 26, 74, 14, 0, Math.PI * 2); ctx.fillStyle = '#0b6e8a'; ctx.fill();
  ctx.fillStyle = '#4a5868'; ctx.font = `500 17px ${FONT}`; ctx.fillText('Healthcare & Wellbeing · hackathon demo', Wpx - 56, 116);
  ctx.textAlign = 'left';
  // HUD
  if (st.unitX < 300 && st.hud) drawHUD(ctx, info, 48, 136);
  // breath-type panel
  if (st.panel) drawBreathPanel(ctx, st, info, Wpx);
  // caption
  if (st.caption) {
    ctx.globalAlpha = st.caption.alpha; ctx.font = `600 34px ${FONT}`;
    const lines = wrap(ctx, st.caption.text, Wpx - 520), lh = 46, bh = lines.length * lh + 34, bw = Math.max(...lines.map(l => ctx.measureText(l).width)) + 60;
    ctx.fillStyle = 'rgba(19,32,46,0.82)'; rr(ctx, (Wpx - bw) / 2, Hpx - 96 - bh, bw, bh, 18); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.textAlign = 'center';
    lines.forEach((l, i) => ctx.fillText(l, Wpx / 2, Hpx - 96 - bh + 50 + i * lh));
    ctx.textAlign = 'left'; ctx.globalAlpha = 1;
  }
  // outro
  if (st.title.startsWith('SpiroBuddy – guided') && st.t > 87) {
    const a = clamp01((st.t - 87) / 1.2);
    ctx.globalAlpha = a; ctx.fillStyle = 'rgba(255,255,255,0.9)'; rr(ctx, Wpx / 2 - 600, 290, 1200, 240, 12); ctx.fill();
    ctx.textAlign = 'center'; ctx.fillStyle = '#0b6e8a'; ctx.font = `800 84px ${FONT}`; ctx.fillText('SpiroBuddy', Wpx / 2, 410);
    ctx.fillStyle = '#4a5868'; ctx.font = `600 28px ${FONT}`; ctx.fillText('Fits Indian spirometers · coaches in Indian languages · updates families', Wpx / 2, 470);
    ctx.textAlign = 'left'; ctx.globalAlpha = 1;
  }
  // honesty tag + chapter progress bar
  ctx.font = `500 17px ${FONT}`; ctx.fillStyle = 'rgba(19,32,46,0.72)'; ctx.textAlign = 'right';
  ctx.fillText('3D concept model · dimensions from published specs (see sources)', Wpx - 48, Hpx - 34); ctx.textAlign = 'left';
  const n = st.chapters.length, y = Hpx - 16, x0 = 48, x1 = Wpx - 48, gap = 8;
  for (let i = 0; i < n; i++) {
    const a = st.chapters[i][0], b = i + 1 < n ? st.chapters[i + 1][0] : st.duration;
    const sx = lerp(x0, x1, a / st.duration) + (i ? gap / 2 : 0), ex = lerp(x0, x1, b / st.duration) - (i < n - 1 ? gap / 2 : 0);
    ctx.fillStyle = 'rgba(19,32,46,0.18)'; rr(ctx, sx, y - 6, ex - sx, 6, 3); ctx.fill();
    const f = clamp01((st.t - a) / (b - a)); if (f > 0) { ctx.fillStyle = '#0b6e8a'; rr(ctx, sx, y - 6, (ex - sx) * f, 6, 3); ctx.fill(); }
  }
  ctx.restore();
}
function currentChapter(chs, t) { let i = 0; for (let k = 0; k < chs.length; k++) if (t >= chs[k][0]) i = k; return { i, name: chs[i][1] }; }
function hudRows(info) {
  const be = info.be;
  return [['Volume', `${Math.round(be.vol)} mL`], ['Flow', `${Math.round(Math.max(0, be.flow))} mL/s`], ['Laser distance', `${info.dist.toFixed(1)} mm`], ['State', be.state]];
}
function drawHUD(ctx, info, x, y) {
  const rows = hudRows(info), w = 330, h = 44 + rows.length * 38 + 16;
  ctx.fillStyle = 'rgba(255,255,255,0.9)'; rr(ctx, x, y, w, h, 16); ctx.fill();
  ctx.fillStyle = '#0b6e8a'; ctx.font = `700 16px ${FONT}`; ctx.fillText('LIVE READOUT', x + 22, y + 32);
  const col = '#' + new THREE.Color(info.co.led).getHexString();
  ctx.beginPath(); ctx.arc(x + w - 30, y + 27, 10, 0, Math.PI * 2); ctx.fillStyle = col; ctx.fill();
  rows.forEach(([k, v], i) => {
    const yy = y + 72 + i * 38; ctx.fillStyle = '#4a5868'; ctx.font = `600 19px ${FONT}`; ctx.fillText(k, x + 22, yy);
    ctx.fillStyle = '#13202e'; ctx.font = `800 22px ${FONT}`; ctx.textAlign = 'right'; ctx.fillText(v, x + w - 22, yy); ctx.textAlign = 'left';
  });
}
function drawBreathPanel(ctx, st, info, Wpx) {
  const types = ['good', 'too_fast', 'too_shallow', 'no_hold'], x = Wpx - 560, w = 510, h = 168, y0 = 150;
  const be = info.be;
  types.forEach((type, i) => {
    const b = st.sched.find(s => s.type === type), y = y0 + i * (h + 14);
    const active = be.active && be.active.type === type, done = b && st.t >= b.t0 + breathDur(type);
    ctx.fillStyle = active ? 'rgba(227,242,246,0.97)' : 'rgba(255,255,255,0.9)'; rr(ctx, x, y, w, h, 16); ctx.fill();
    if (active) { ctx.strokeStyle = '#0b6e8a'; ctx.lineWidth = 3; ctx.stroke(); }
    const r = BREATH_RESULTS[type], cb = CFG.breaths[type];
    ctx.fillStyle = '#13202e'; ctx.font = `800 24px ${FONT}`; ctx.fillText(LBL[type], x + 20, y + 36);
    ctx.fillStyle = '#6b7888'; ctx.font = `500 15px ${FONT}`; ctx.fillText(`peak ${cb.peak} · rise ${cb.rise}s · hold ${cb.hold}s · fall ${cb.fall}s`, x + 20, y + 60);
    // mini curve
    const px = x + 20, py = y + 72, pw = 230, ph = 80, tmax = 9;
    ctx.strokeStyle = 'rgba(19,32,46,0.15)'; ctx.lineWidth = 1; ctx.strokeRect(px, py, pw, ph);
    const ty = py + ph - ph * CFG.coach.target / S.scaleMax; ctx.setLineDash([5, 4]); ctx.beginPath(); ctx.moveTo(px, ty); ctx.lineTo(px + pw, ty); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle = LABEL_BG[type]; ctx.lineWidth = 3; ctx.beginPath();
    const tEnd = b ? Math.min(st.t - b.t0, tmax) : 0;
    for (let k = 0; k <= 120; k++) { const tt = -0.3 + k / 120 * tmax; if (tt > tEnd) break; const xx = px + (tt + 0.3) / tmax * pw, yy = py + ph - ph * curveVol(type, tt) / S.scaleMax; k ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); }
    ctx.stroke();
    // features + result
    const f = r.features, fx = x + 270;
    ctx.font = `600 15px ${FONT}`; ctx.fillStyle = '#4a5868';
    [[`peak`, `${f.peak_ml} mL`], ['max rise', `${f.max_rise_ml_s} mL/s`], ['hold', `${f.hold_s.toFixed(2)} s`]].forEach(([k, v], j) => {
      ctx.fillText(k, fx, y + 92 + j * 22); ctx.textAlign = 'right'; ctx.fillText(done || active ? v : '—', x + w - 20, y + 92 + j * 22); ctx.textAlign = 'left';
    });
    if (done) {
      ctx.fillStyle = '#13202e'; ctx.font = `800 26px ${FONT}`; ctx.textAlign = 'right'; ctx.fillText(`${r.score.toFixed(1)} / 10`, x + w - 20, y + 38); ctx.textAlign = 'left';
      chip(ctx, fx, y + 22, `rule: ${LBL[r.label]}`, LABEL_BG[r.label], '#fff', 15);
    }
  });
}

// =====================================================================================
// GLB EXPORT
// =====================================================================================
async function exportGLB() {
  const hidden = [];
  model.traverse(o => { if (o.userData.fx && o.visible) { o.visible = false; hidden.push(o); } });
  const prev = { ...ui };
  applyState({ ...baseInteractiveState(), explode: 0, xray: 0, laser: 0 });
  const exporter = new GLTFExporter();
  const buf = await exporter.parseAsync(model, { binary: true, onlyVisible: true });
  hidden.forEach(o => (o.visible = true));
  Object.assign(ui, prev);
  return buf;
}

// =====================================================================================
// INTERACTIVE MODE
// =====================================================================================
const ui = { explode: 0, xray: 0, laser: 1, labels: 0, auto: false, autoIdx: 0 };
let simT = 0, sched = [], lastAutoEnd = 0;
let tour = null; // { t, playing }
let camTween = null;
function baseInteractiveState() {
  return { unitX: 0, spiroY: SEAT, phoneX: 0, explode: ui.explode, xray: ui.xray, laser: ui.laser, labels: ui.labels, sched, tB: simT, countOffset: 0, phone: { screen: 'live' }, labelGroups: ['unit', 'spiro'] };
}
function queueBreath(type) {
  const busyUntil = sched.reduce((m, b) => Math.max(m, b.t0 + breathDur(b.type)), 0);
  sched.push({ t0: Math.max(simT + 0.15, busyUntil + 0.6), type });
  sched = sched.filter(b => b.t0 + breathDur(b.type) > simT - 30 || b === sched[sched.length - 1]);
}
const AUTO_ORDER = ['good', 'too_fast', 'good', 'too_shallow', 'no_hold'];
const PRESETS = {
  front: C(0, 10, 640, 40, 105, 10), side: C(72, 6, 430, 20, 105, 0), top: C(10, 62, 560, 10, 90, 0),
  inside: C(-28, 30, 380, 0, 45, 0), phone: C(22, 6, 320, 200, 86, 60), wide: C(24, 16, 760, 50, 105, 10),
};
const controls = RENDER ? null : new OrbitControls(camera, glCanvas);
if (controls) {
  controls.enableDamping = true; controls.dampingFactor = 0.08; controls.minDistance = 120; controls.maxDistance = 2200;
  controls.maxPolarAngle = Math.PI * 0.495; controls.target.set(40, 105, 10);
  camFrom(PRESETS.wide); controls.update();
}
function sphericalNow() {
  const t = controls.target, d = camera.position.clone().sub(t), dist = d.length();
  return { az: THREE.MathUtils.radToDeg(Math.atan2(d.x, d.z)), el: THREE.MathUtils.radToDeg(Math.asin(d.y / dist)), dist, tx: t.x, ty: t.y, tz: t.z };
}
function goPreset(name) {
  const from = sphericalNow(), to = { ...PRESETS[name] };
  while (to.az - from.az > 180) to.az -= 360; while (to.az - from.az < -180) to.az += 360;
  camTween = { from, to, t: 0, dur: 1.1 };
}

// ---- UI wiring (interactive page only)
function $(id) { return document.getElementById(id); }
function setupUI() {
  document.querySelectorAll('[data-breath]').forEach(b => b.addEventListener('click', () => { stopTour(); queueBreath(b.dataset.breath); }));
  $('auto').addEventListener('change', e => { ui.auto = e.target.checked; });
  $('explode').addEventListener('input', e => { ui.explode = +e.target.value; });
  for (const k of ['xray', 'laser', 'labels']) $(k).addEventListener('change', e => { ui[k] = e.target.checked ? 1 : 0; });
  document.querySelectorAll('[data-cam]').forEach(b => b.addEventListener('click', () => { stopTour(); goPreset(b.dataset.cam); }));
  $('tourBtn').addEventListener('click', () => (tour ? (tour.playing = !tour.playing, syncTourUI()) : startTour()));
  $('tourStop').addEventListener('click', stopTour);
  $('tourPrev').addEventListener('click', () => jumpChapter(-1));
  $('tourNext').addEventListener('click', () => jumpChapter(1));
  $('glbBtn').addEventListener('click', async () => {
    const btn = $('glbBtn'); btn.disabled = true; btn.textContent = 'Exporting…';
    try { const buf = await exportGLB(); const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([buf], { type: 'model/gltf-binary' })); a.download = 'spirobuddy_setup.glb'; a.click(); }
    catch (e) { console.error(e); alert('Export failed: ' + e.message); }
    btn.disabled = false; btn.textContent = 'Download 3D model (.glb)';
  });
  $('fsBtn').addEventListener('click', () => (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()));
  window.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT') return;
    if (e.key === 'ArrowRight') jumpChapter(1); else if (e.key === 'ArrowLeft') jumpChapter(-1);
    else if (e.key === ' ' && tour) { tour.playing = !tour.playing; syncTourUI(); e.preventDefault(); }
    else if (e.key === 'Escape') stopTour();
    else if ('1234'.includes(e.key) && e.key.length === 1) queueBreath(['good', 'too_fast', 'too_shallow', 'no_hold'][+e.key - 1]);
  });
  const chs = $('chapters');
  VIDEOS.tour.chapters.forEach(([t, name], i) => { const b = document.createElement('button'); b.textContent = `${i + 1}. ${name}`; b.addEventListener('click', () => { if (!tour) startTour(); tour.t = t + 0.01; }); chs.appendChild(b); });
  // breath verification table
  const tb = $('verify');
  tb.innerHTML = '<tr><th>Curve</th><th>peak</th><th>max rise</th><th>hold</th><th>score</th><th>rule label</th></tr>' +
    Object.entries(BREATH_RESULTS).map(([k, r]) => `<tr><td>${LBL[k]}</td><td>${r.features.peak_ml}</td><td>${r.features.max_rise_ml_s}</td><td>${r.features.hold_s.toFixed(2)}</td><td>${r.score.toFixed(1)}</td><td class="${r.ok ? 'ok' : 'bad'}">${LBL[r.label]} ${r.ok ? '✓' : '✗'}</td></tr>`).join('');
  const dimList = $('dims');
  dimList.innerHTML = [
    ['Spirometer height (B02)', `${S.H} mm`], ['Spirometer width incl. handle (B03)', `${S.W} mm`], ['Volume chamber OD (B09)', `${S.volOD} mm`],
    ['Mark spacing per 250 mL (B14)', `${S.mmPer250} mm`], ['Base unit (D02/D03)', `${U.outerW} × ${U.outerD} × ${D.lidTop} mm`],
    ['Sensor → piston at rest (D05)', `${D.restDist.toFixed(1)} mm (rule ≥ 50)`], ['Sensor → piston at 2500 mL', `${(D.restDist + S.scaleMax * D.mmPerMl).toFixed(1)} mm`],
  ].map(([k, v]) => `<li><span>${k}</span><b>${v}</b></li>`).join('');
}
function startTour() { tour = { t: 0, playing: true }; document.body.classList.add('touring'); syncTourUI(); }
function stopTour() {
  if (!tour) return; tour = null; document.body.classList.remove('touring');
  const cs = sphericalNow(); controls.target.set(cs.tx, cs.ty, cs.tz); syncTourUI(); $('caption').classList.remove('show');
}
function jumpChapter(d) {
  if (!tour) { if (d > 0) startTour(); return; }
  const chs = VIDEOS.tour.chapters, cur = currentChapter(chs, tour.t).i, n = Math.max(0, Math.min(chs.length - 1, cur + d));
  tour.t = chs[n][0] + 0.01;
}
function syncTourUI() {
  $('tourBtn').textContent = !tour ? '▶ Play guided tour' : (tour.playing ? '❚❚ Pause' : '▶ Resume');
  $('tourbar').classList.toggle('show', !!tour);
}
function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  const dpr = Math.min(window.devicePixelRatio, 2); ovCanvas.width = w * dpr; ovCanvas.height = h * dpr; ov.setTransform(dpr, 0, 0, dpr, 0, 0);
}
let lastNow = performance.now();
function loopInteractive(now) {
  const dt = Math.min(0.1, (now - lastNow) / 1000); lastNow = now;
  simT += dt;
  if (ui.auto && !tour) {
    const busy = sched.reduce((m, b) => Math.max(m, b.t0 + breathDur(b.type)), 0);
    if (simT > busy + 1.6) { queueBreath(AUTO_ORDER[ui.autoIdx++ % AUTO_ORDER.length]); }
  }
  let st;
  if (tour) {
    if (tour.playing) tour.t += dt;
    if (tour.t >= VIDEOS.tour.duration) { stopTour(); st = baseInteractiveState(); }
    else { st = videoState('tour', tour.t); camFrom(st.cam); controls.target.set(st.cam.tx, st.cam.ty, st.cam.tz); }
  }
  if (!st) {
    st = baseInteractiveState();
    if (camTween) {
      camTween.t += dt; const u = smooth(clamp01(camTween.t / camTween.dur));
      const cs = lerpAny(camTween.from, camTween.to, u); camFrom(cs); controls.target.set(cs.tx, cs.ty, cs.tz);
      if (u >= 1) camTween = null;
    } else controls.update();
  }
  const info = applyState(st);
  renderer.render(scene, camera);
  // overlay
  const w = window.innerWidth, h = window.innerHeight;
  ov.clearRect(0, 0, w, h);
  const panelW = document.body.classList.contains('panel-hidden') ? 0 : ($('panel').getBoundingClientRect().right || 0);
  drawLabels(ov, w, h, st.labels, st.labelGroups, { left: panelW + 16, right: ($('readout').getBoundingClientRect().width || 0) + 32, top: 90, bottom: 120 }, 1);
  drawBeamNote(ov, w, h, st.laser, 1, info);
  // readout
  const rows = hudRows(info);
  $('r_vol').textContent = rows[0][1]; $('r_flow').textContent = rows[1][1]; $('r_dist').textContent = rows[2][1]; $('r_state').textContent = rows[3][1];
  $('r_led').style.background = '#' + new THREE.Color(info.co.led).getHexString();
  $('r_coach').textContent = info.co.en; $('r_coach_hi').textContent = info.co.hi;
  const res = info.be.result;
  $('r_last').innerHTML = res ? `<b>${res.score.toFixed(1)}</b>/10 <span class="lab" style="background:${LABEL_BG[res.label]}">${LBL[res.label]}</span>` : '—';
  if (tour) {
    const cap = st.caption, el = $('caption');
    if (cap) { el.textContent = cap.text; el.classList.add('show'); el.style.opacity = cap.alpha; } else el.classList.remove('show');
    const ch = currentChapter(VIDEOS.tour.chapters, tour.t);
    $('tourTitle').textContent = `${ch.i + 1}/${VIDEOS.tour.chapters.length} · ${ch.name}`;
    $('tourProg').style.width = `${(tour.t / VIDEOS.tour.duration) * 100}%`;
  }
  requestAnimationFrame(loopInteractive);
}

// =====================================================================================
// RENDER MODE — deterministic frame-by-frame → local server → ffmpeg
// =====================================================================================
async function postLog(msg) { try { await fetch('/log', { method: 'POST', body: String(msg) }); } catch (e) { /* ignore */ } }
async function renderVideo(id) {
  const v = VIDEOS[id]; if (!v) throw new Error('unknown video ' + id);
  const { w, h, fps, jpegQ } = CFG.video;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  ovCanvas.width = w; ovCanvas.height = h;
  const comp = document.createElement('canvas'); comp.width = w; comp.height = h; const cc = comp.getContext('2d');
  if (params.get('glb') === '1') {
    const buf = await exportGLB();
    await fetch('/glb', { method: 'POST', body: buf });
  }
  const N = Math.round(v.duration * fps), beeps = [];
  // beep times for the soundtrack: good-breath ends (one tone) and live too-fast moments (two low tones)
  for (const b of v.sched) {
    const r = BREATH_RESULTS[b.type];
    if (r.label === 'good') beeps.push({ t: b.t0 + breathDur(b.type), f: 1760, d: 0.18 });
    const be = breathEval([b], b.t0 + CFG.breaths[b.type].rise);
    if (be.fastAt !== null) beeps.push({ t: be.fastAt, f: 520, d: 0.12 }, { t: be.fastAt + 0.2, f: 440, d: 0.12 });
  }
  const start = parseInt(params.get('from') || '0', 10), end = Math.min(N, parseInt(params.get('to') || String(N), 10));
  for (let i = start; i < end; i++) {
    const t = i / fps, st = videoState(id, t);
    camFrom(st.cam);
    const info = applyState(st);
    renderer.render(scene, camera);
    drawVideoOverlay(ov, st, info, w, h);
    cc.drawImage(glCanvas, 0, 0, w, h); cc.drawImage(ovCanvas, 0, 0);
    const blob = await new Promise(res => comp.toBlob(res, 'image/jpeg', jpegQ));
    for (let attempt = 1; ; attempt++) {   // retry: a busy local server can drop a request now and then
      try { const r = await fetch(`/frame/${id}/${i}`, { method: 'POST', body: blob }); if (r.ok) break; throw new Error('HTTP ' + r.status); }
      catch (e) { if (attempt >= 8) throw new Error(`frame ${i} upload failed: ${e.message}`); await new Promise(res => setTimeout(res, 250 * attempt)); }
    }
    window.__renderStatus = { id, frame: i, of: N };
  }
  if (end === N) await fetch(`/done/${id}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ frames: N, fps, beeps, duration: v.duration }) });
  window.__renderStatus = { id, done: true };
}

// =====================================================================================
// BOOT
// =====================================================================================
async function boot() {
  try { await Promise.all([document.fonts.load(`700 40px Inter`), document.fonts.load(`700 40px 'Noto Sans Devanagari'`, 'धीरे'), document.fonts.load(`800 40px Inter`), document.fonts.load(`600 20px Inter`)]); } catch (e) { /* offline: system fonts */ }
  await document.fonts.ready;
  if (RENDER) {
    document.body.classList.add('render');
    try { await renderVideo(RENDER_ID); }
    catch (e) { console.error(e); await postLog('ERROR ' + RENDER_ID + ': ' + (e.stack || e)); await fetch(`/fail/${RENDER_ID}`, { method: 'POST', body: String(e) }).catch(() => {}); }
    return;
  }
  setupUI(); resize(); window.addEventListener('resize', resize);
  requestAnimationFrame(loopInteractive);
  window.__showcase = { CFG, D, BREATH_RESULTS, videoState, applyState, exportGLB };
}
boot();
