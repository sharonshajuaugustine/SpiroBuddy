// SpiroBuddy digital twin – the procedural 3D model of a Romsons Breazer 2500 standing on the SpiroBuddy
// base unit. Used by the 3D showroom (/showcase/), the public twin (/twin.html) and the live twin in the
// hospital (/hospital/twin.html, js/twin-panel.js).
//
// ES module with NO imports: the caller passes THREE (three@0.169.0 from jsdelivr, same as the showroom)
// and, if it has it, RoundedBoxGeometry from three/addons. Units: millimetres, y up.
//
//   import { buildSetup } from '/js/twin-model.js';
//   const twin = buildSetup(THREE, { RoundedBoxGeometry });
//   scene.add(twin.group, twin.fx.beam, twin.fx.glowSprite);
//   twin.setVolumeMl(1500); twin.setLed('inhale'); twin.setBattery(82); twin.setConnection('simulator');
//   twin.showBeam(true); twin.update(dt);   // call update() once per frame
//
// Every real-world size lives in CFG below. The row IDs (B.., E.., D.., P.., C..) point to
// docs/3D_SOURCES.md, which gives the source URL, how it was verified and the confidence.

// =====================================================================================
// CONFIG — the ONE place for every number. See docs/3D_SOURCES.md for each row.
// =====================================================================================
export const CFG = {
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
  // Breath curves (sine-eased rise, flat hold, sine-eased fall) — task brief, verified against CONTRACT C.
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
export const S = CFG.spiro, U = CFG.unit, E = CFG.elec;
export const SX = x => x - S.baseW / 2;                   // spirometer-local x from "mm from left edge"
export const D = {
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

// Showroom light colours (the videos and the showroom keep these exactly).
export const COL = { idle: 0x2f7cf6, breathe: 0x14b8a6, fast: 0xf59e0b, good: 0x22c55e, soft: 0x93c5fd };
// Digital-twin LED: FIXED meanings everywhere (DESIGN_SYSTEM §1): teal = breathing in, green = good,
// amber = slow down / watch, red = a person is needed. "idle" = the same teal, dimmed.
export const LED = { idle: 0x14b8a6, inhale: 0x14b8a6, good: 0x22c55e, slow: 0xf59e0b, alert: 0xdc2626 };
export const LED_WORD = { idle: 'Ready', inhale: 'Breathing in', good: 'Good breath', slow: 'Slow down', alert: 'A person is needed' };
export const LED_CSS = { idle: '#14b8a6', inhale: '#14b8a6', good: '#22c55e', slow: '#f59e0b', alert: '#dc2626' };
export const FONT = "Inter, 'Noto Sans Devanagari', system-ui, sans-serif";

// =====================================================================================
// MATERIALS & HELPERS (one kit per THREE instance)
// =====================================================================================
export function makeKit(THREE, opts = {}) {
  const RoundedBoxGeometry = opts.RoundedBoxGeometry || null;
  const M = {
    clear: () => new THREE.MeshPhysicalMaterial({ color: 0xf4fbff, roughness: 0.04, metalness: 0, transparent: true, opacity: 0.22,
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
  function rbox(w, h, d, r, mat, name) {
    if (!RoundedBoxGeometry) return box(w, h, d, mat, name);   // no addon passed: square corners
    return mesh(new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2 - 0.01, h / 2 - 0.01, d / 2 - 0.01)), mat, name);
  }
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
  // materials that fade in X-ray mode: { mat, base }
  const xrayMats = [];
  function xr(mat, base = mat.opacity) { xrayMats.push({ mat, base }); return mat; }
  return { THREE, M, mesh, box, rbox, cyl, at, roundRect, circlePath, circleShape, extrudeY, canvasTex, xr, xrayMats, RoundedBoxGeometry };
}

// =====================================================================================
// BUILD THE SETUP (spirometer + base unit + laser beam + LED glow) — same geometry as the showroom
// =====================================================================================
export function buildSetup(THREE, opts = {}) {
  const kit = makeKit(THREE, opts);
  const { M, mesh, box, rbox, cyl, at, roundRect, circlePath, circleShape, extrudeY, canvasTex, xr, xrayMats } = kit;
  const lerp = (a, b, u) => a + (b - a) * u;

  // ---------------------------------------------------------------- SPIROMETER — Romsons Breazer 2500
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
      const pm = M.blueTrans(); pm.opacity = 0.97; pm.color.set(0x1b86c8);   // the moving disc is the thing to watch
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
  // groupWorldPos = the spirometer group's position; fig 0..1 lifts the hose end to figEnd (the showroom's patient outline).
  function updateHose(groupWorldPos, fig = 0, figEnd = null) {
    // The hose starts at the connector-tube port and lies on the table; the end stays put in the world.
    const start = new THREE.Vector3(D.midX, S.portY, S.midOD / 2 + 11);
    const endW = new THREE.Vector3(-150, S.hoseOD / 2, 128);
    if (figEnd) endW.lerp(figEnd, fig);
    const end = endW.clone().sub(groupWorldPos);
    const k = `${end.x.toFixed(1)},${end.y.toFixed(1)},${end.z.toFixed(1)},${fig.toFixed(3)}`;
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
    if (fig > 0) {   // lifted to the patient's mouth: a loose arc from the port up to the mouthpiece
      const up = [
        start,
        new THREE.Vector3(start.x - 2, start.y - 4, start.z + 14),
        new THREE.Vector3(start.x - 12, start.y - 14, start.z + 42),
        new THREE.Vector3(lerp(start.x, end.x, 0.5), (start.y + end.y) / 2 - 62, end.z + 48),
        new THREE.Vector3(end.x + 62, end.y - 26, end.z + 14),
        new THREE.Vector3(end.x + 26, end.y - 4, end.z + 2),
        end,
      ];
      pts.forEach((q, i) => q.lerp(up[i], fig));
    }
    const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
    spiro.parts.hose.geometry.dispose();
    spiro.parts.hose.geometry = ribbedTube(curve, S.hoseOD / 2 - S.hoseRib / 2, S.hosePitch, S.hoseRib / 2);
    const dir = curve.getTangentAt(1).normalize();
    spiro.parts.mouth.position.copy(end);
    spiro.parts.mouth.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    spiro.parts.hoseLength = curve.getLength();
  }

  // ---------------------------------------------------------------- SPIROBUDDY BASE UNIT — our design (D rows)
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
      P.lipoLabelTex = lab;
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

  // ---------------------------------------------------------------- ASSEMBLE
  const group = new THREE.Group(); group.name = 'SpiroBuddy_setup';
  const spiro = buildSpirometer(); group.add(spiro.group);
  const unit = buildUnit(); group.add(unit.group);
  // laser beam (illustration — the real 940 nm beam is invisible). Lives in WORLD space: add fx.beam to the scene.
  const beam = new THREE.Group(); beam.name = 'fx_laser'; beam.userData.fx = true;
  const beamCone = new THREE.Mesh(new THREE.ConeGeometry(1, 1, 40, 1, true), new THREE.MeshBasicMaterial({ color: 0xe0284f, transparent: true, opacity: 0.25, depthWrite: false, side: THREE.DoubleSide }));
  beamCone.geometry.rotateX(Math.PI); beamCone.geometry.translate(0, 0.5, 0);
  const beamCore = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 1, 10), new THREE.MeshBasicMaterial({ color: 0xd61f45, transparent: true, opacity: 0.9, depthWrite: false }));
  beamCore.geometry.translate(0, 0.5, 0);
  const beamSpot = new THREE.Mesh(new THREE.CircleGeometry(1, 40), new THREE.MeshBasicMaterial({ color: 0xd61f45, transparent: true, opacity: 0.6, depthWrite: false, side: THREE.DoubleSide }));
  beamSpot.rotation.x = Math.PI / 2;
  beam.add(beamCone, beamCore, beamSpot);
  // LED glow sprite (WORLD space too: add fx.glowSprite to the scene)
  const glowSprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: canvasTex(128, 128, (c) => { const gr = c.createRadialGradient(64, 64, 2, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = gr; c.fillRect(0, 0, 128, 128); }), blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
  glowSprite.scale.set(90, 26, 1); glowSprite.userData.fx = true;

  // ---------------------------------------------------------------- TWIN API (used by /twin.html and the live twin)
  // The showroom drives the parts directly (its own applyState); everything below is for the twin pages.
  const tw = { vol: 0, flow: 0, led: 'idle', battery: null, connection: 'simulator', beam: 0, ring: null };
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const _c = new THREE.Color(), _s = new THREE.Vector3();
  function seat() {                          // spirometer standing in the pocket, hose on the table
    spiro.group.position.set(0, D.seatY, 0);
    updateHose(spiro.group.position, 0, null);
  }
  function setVolumeMl(ml) {
    tw.vol = clamp(Number(ml) || 0, 0, S.scaleMax);
    spiro.parts.piston.position.y = D.pistonRestBottom + tw.vol * D.mmPerMl;
  }
  // flow (mL/s over the last 0.3 s) lifts the flow-indicator float (illustrative mapping B27)
  function setFlow(r03) {
    tw.flow = Math.max(0, Number(r03) || 0);
    const fl = tw.flow, zoneMid = (S.zoneBottomY + S.zoneTopY) / 2, restTop = S.seatTop + S.floatH;
    const lift = fl <= CFG.floatFlowForTarget ? (fl / CFG.floatFlowForTarget) * (zoneMid - restTop)
      : (zoneMid - restTop) + Math.min(1, (fl - CFG.floatFlowForTarget) / (CFG.floatMaxFlow - CFG.floatFlowForTarget)) * (S.zoneTopY - zoneMid);
    spiro.parts.float.position.y = S.seatTop + Math.max(0, lift);
  }
  function paintLed() {
    const on = tw.connection !== 'offline';
    const dim = tw.led === 'idle';
    _c.set(LED[tw.led] ?? LED.idle);
    unit.parts.ledMat.emissive.copy(_c); unit.parts.lightBarMat.emissive.copy(_c);
    unit.parts.ledMat.emissiveIntensity = on ? (dim ? 1.0 : 2.5) : 0;
    unit.parts.lightBarMat.emissiveIntensity = on ? (dim ? 0.55 : 1.7) : 0;
    unit.parts.glow.color.copy(_c); unit.parts.glow.intensity = on ? (dim ? 500 : 1800) : 0;
    glowSprite.material.color.copy(_c); glowSprite.material.opacity = on ? (dim ? 0.35 : 0.75) : 0;
  }
  // idle | inhale | good | slow | alert  →  teal (dim) / teal / green / amber / red. Fixed meanings.
  function setLed(state) {
    const s = Object.prototype.hasOwnProperty.call(LED, state) ? state : 'idle';
    if (s === 'good' && tw.led !== 'good') ping('good');
    if (s === 'slow' && tw.led !== 'slow') ping('slow');
    tw.led = s; paintLed();
  }
  // battery 0..100 → drawn on the LiPo label (visible in the X-ray / inside views); null = unknown
  function setBattery(pct) {
    const v = pct == null || !isFinite(pct) ? null : Math.round(clamp(Number(pct), 0, 100));
    if (v === tw.battery) return;
    tw.battery = v;
    const c = unit.parts.lipoLabelTex.userData.canvas, g = c.getContext('2d'), ww = c.width, hh = c.height;
    g.fillStyle = '#1b2a3a'; g.fillRect(0, 0, ww, hh); g.fillStyle = '#fff'; g.textAlign = 'center';
    g.font = `700 40px ${FONT}`; g.fillText('3.7 V', ww / 2, 64); g.fillText(`${E.lipo.mAh} mAh`, ww / 2, 112);
    if (v != null) {
      g.strokeStyle = '#fff'; g.lineWidth = 4; g.strokeRect(40, 136, ww - 92, 40); g.fillRect(ww - 52, 146, 10, 20);
      g.fillStyle = v <= 15 ? '#dc2626' : v <= 35 ? '#f59e0b' : '#22c55e'; g.fillRect(44, 140, (ww - 100) * v / 100, 32);
    }
    unit.parts.lipoLabelTex.needsUpdate = true;
  }
  // 'simulator' | 'usb' | 'ble' | 'idle' | 'offline' – offline turns the light off
  function setConnection(state) { tw.connection = String(state || 'offline'); paintLed(); }
  function showBeam(on) { tw.beam = on === true ? 1 : on === false ? 0 : clamp(Number(on) || 0, 0, 1); }
  // short beep rings: green after a good breath, amber on "slow down"
  function ping(kind) { tw.ring = { t: 0, col: kind === 'slow' ? COL.fast : COL.good }; }
  function update(dt = 1 / 60) {
    // laser beam from the sensor up to the underside of the piston (world space)
    const sensorW = unit.parts.sensor.localToWorld(_s.set(0, D.sensorFaceY, 0)).clone();
    const pistonW = spiro.parts.piston.getWorldPosition(new THREE.Vector3());
    const dist = Math.max(1, pistonW.y - sensorW.y);
    beam.visible = tw.beam > 0.01;
    beam.position.copy(sensorW);
    const rr = Math.tan(THREE.MathUtils.degToRad(E.vlRoiDeg / 2)) * dist;
    beamCone.scale.set(rr, dist, rr); beamCore.scale.set(1, dist, 1);
    beamSpot.position.set(0, dist - 0.3, 0); beamSpot.scale.set(rr, rr, rr);
    beamCone.material.opacity = 0.26 * tw.beam; beamCore.material.opacity = 0.9 * tw.beam; beamSpot.material.opacity = 0.7 * tw.beam;
    unit.parts.lightBar.getWorldPosition(glowSprite.position); glowSprite.position.z += 3;
    // rings
    const on = tw.connection !== 'offline';
    if (tw.ring) tw.ring.t += dt;
    unit.parts.rings.forEach((r, i) => {
      const u = !tw.ring ? -1 : (tw.ring.t - i * 0.22) / 1.1;
      r.visible = u > 0 && u < 1 && on;
      if (r.visible) { const s = lerp(70, 190, u); r.scale.set(s, s, s); r.material.opacity = (1 - u) * 0.9; r.material.color.set(tw.ring.col); r.position.y = 30 + 20 * u; }
    });
    if (tw.ring && tw.ring.t > 2) tw.ring = null;
    return { dist, vol: tw.vol };
  }

  return {
    group, spiro, unit, kit, xrayMats,
    fx: { beam, beamCone, beamCore, beamSpot, glowSprite },
    updateHose, seat,
    setVolumeMl, setFlow, setLed, setBattery, setConnection, showBeam, ping, update,
    get state() { return { ...tw }; },
  };
}

// =====================================================================================
// VIEWER for the twin pages (renderer + scene + camera + optional orbit controls). The showroom has its own.
// =====================================================================================
export function createViewer(THREE, opts) {
  const { canvas, RoomEnvironment, OrbitControls, RoundedBoxGeometry } = opts;
  const transparent = opts.transparent !== false;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: transparent, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  if (transparent) renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  if (RoomEnvironment) {
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  }
  const camera = new THREE.PerspectiveCamera(30, 1, 5, 20000);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 0.55));
  const key = new THREE.DirectionalLight(0xffffff, 2.2);
  key.position.set(260, 520, 360); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  Object.assign(key.shadow.camera, { left: -300, right: 300, top: 300, bottom: -300, near: 50, far: 1600 });
  key.shadow.bias = -0.0004; key.shadow.radius = 6;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xcfe8ff, 1.1); rim.position.set(-400, 300, -380); scene.add(rim);
  // soft round floor (fades out at the edge, so it sits on any page background)
  const floorMat = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const g = c.getContext('2d'), gr = g.createRadialGradient(128, 128, 20, 128, 128, 128);
    gr.addColorStop(0, '#fff'); gr.addColorStop(0.6, '#777'); gr.addColorStop(1, '#000');
    g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
    return new THREE.MeshStandardMaterial({ color: 0xc5d0db, roughness: 0.85, metalness: 0, transparent: true, alphaMap: new THREE.CanvasTexture(c), depthWrite: false, opacity: 0.9 });
  })();
  const floor = new THREE.Mesh(new THREE.CircleGeometry(420, 96), floorMat);
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; floor.name = 'floor';
  scene.add(floor);

  const twin = buildSetup(THREE, { RoundedBoxGeometry });
  twin.seat();
  scene.add(twin.group, twin.fx.beam, twin.fx.glowSprite);

  // camera: 3/4 front view, distance fitted to the box (≈ 330 × 260 mm incl. the hose on the table)
  const view = Object.assign({ az: 18, el: 13, tx: 0, ty: 112, tz: 20, w: 340, h: 270 }, opts.view || {});
  let controls = null;
  if (OrbitControls && opts.interactive !== false) {
    controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true; controls.dampingFactor = 0.08; controls.minDistance = 150; controls.maxDistance = 1600;
    controls.maxPolarAngle = Math.PI * 0.495; controls.target.set(view.tx, view.ty, view.tz);
    controls.enablePan = false;
  }
  let lastW = 0, lastH = 0;
  function frame(w, h) {
    const aspect = w / Math.max(1, h), half = THREE.MathUtils.degToRad(camera.fov / 2);
    const dist = Math.max((view.h / 2) / Math.tan(half), (view.w / 2) / (Math.tan(half) * aspect)) * 1.12;
    const az = THREE.MathUtils.degToRad(view.az), el = THREE.MathUtils.degToRad(view.el);
    camera.position.set(view.tx + dist * Math.sin(az) * Math.cos(el), view.ty + dist * Math.sin(el), view.tz + dist * Math.cos(az) * Math.cos(el));
    camera.lookAt(view.tx, view.ty, view.tz);
    if (controls) { controls.target.set(view.tx, view.ty, view.tz); controls.update(); }
  }
  function resize() {
    const r = canvas.getBoundingClientRect(), w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
    if (w === lastW && h === lastH) return false;
    const first = !lastW; lastW = w; lastH = h;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    if (first || !controls) frame(w, h);
    return true;
  }
  function setTheme(dark) {
    floorMat.color.set(dark ? 0x3a4a5c : 0xc5d0db);
    floorMat.opacity = dark ? 0.55 : 0.9;
  }
  let last = performance.now();
  function render() {
    const now = performance.now(), dt = Math.min(0.1, (now - last) / 1000); last = now;
    resize();
    if (controls) controls.update();
    twin.update(dt);
    renderer.render(scene, camera);
  }
  function resetView() { lastW = 0; resize(); frame(lastW, lastH); }
  return { renderer, scene, camera, controls, twin, render, resize, resetView, setTheme };
}
