/* SpiroBuddy – MOCK unit list and hand-over record (demo only).
 *
 * Real design: docs/DEVICE_LIFECYCLE.md (a `devices` table and a `device_assignments` table on the server).
 * None of that exists yet and there is no real hardware, so this file keeps a pretend list in the browser's
 * localStorage. It lets the demo show the life of a lent unit: in stock → in use → returned → cleaned → wiped.
 * Nothing here is sent to the server and nothing personal is stored "on the unit" – exactly as in the design.
 */
(function () {
  const SB = (window.SB = window.SB || {});
  const KEY = 'sb_units_mock_v1';
  const STATES = {
    stock: { label: 'In stock', icon: 'check', cls: 'status-green', hint: 'Clean, wiped and ready to hand over' },
    in_use: { label: 'In use at home', icon: 'user', cls: 'status-blue', hint: 'On loan to one patient' },
    returned: { label: 'Returned', icon: 'refresh', cls: 'status-yellow', hint: 'Back from the patient – needs cleaning' },
    cleaned: { label: 'Cleaned', icon: 'sparkles', cls: 'status-yellow', hint: 'Cleaned and checked – needs wiping' },
    lost: { label: 'Not returned', icon: 'flag', cls: 'status-red', hint: 'Overdue or reported lost' },
    faulty: { label: 'Faulty', icon: 'x', cls: 'status-red', hint: 'Set aside for repair' },
  };
  const now = () => new Date().toISOString();
  const daysAgo = (d, h) => new Date(Date.now() - d * 864e5 - (h || 0) * 36e5).toISOString();

  function read() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (_) { return null; } }
  function write(db) { try { localStorage.setItem(KEY, JSON.stringify(db)); } catch (_) { /* private mode: lives for this page only */ } memo = db; return db; }
  let memo = null;
  const db = () => memo || read();

  /* First visit: build a believable ward stock from the demo patients. */
  function seed(patients) {
    const by = (i) => patients[i] || null;
    const loan = (p, d) => (p ? { patientId: p.id, name: p.name, from: daysAgo(d, 3), to: null } : null);
    const units = [
      { code: 'SB-0011', state: 'in_use', battery: 78, lastSeen: daysAgo(0, 0.3), loan: loan(by(0), 8), history: [] },
      { code: 'SB-0012', state: 'in_use', battery: 41, lastSeen: daysAgo(0, 2), loan: loan(by(2), 4), history: [] },
      { code: 'SB-0013', state: 'in_use', battery: 17, lastSeen: daysAgo(0, 9), loan: loan(by(4), 6), history: [] },
      { code: 'SB-0014', state: 'stock', battery: 100, lastSeen: daysAgo(1), loan: null, history: [{ name: 'Earlier patient', from: daysAgo(30), to: daysAgo(16) }] },
      { code: 'SB-0015', state: 'returned', battery: 55, lastSeen: daysAgo(0, 5), loan: null, history: [{ name: 'Earlier patient', from: daysAgo(15), to: daysAgo(0, 5) }] },
      { code: 'SB-0016', state: 'stock', battery: 96, lastSeen: daysAgo(2), loan: null, history: [] },
      { code: 'SB-0017', state: 'lost', battery: 0, lastSeen: daysAgo(19), loan: null, history: [{ name: 'Earlier patient', from: daysAgo(40), to: null }] },
    ].map((u) => { if (!u.loan && u.state === 'in_use') u.state = 'stock'; return u; });
    const log = [
      { at: daysAgo(0, 5), code: 'SB-0015', text: 'Returned by the family. Last sessions uploaded, loan closed.', by: 'Sister Anjali' },
      { at: daysAgo(4, 3), code: 'SB-0012', text: `Handed over${by(2) ? ' to ' + by(2).name : ''}. Test breath OK.`, by: 'Sister Anjali' },
      { at: daysAgo(5), code: 'SB-0017', text: 'Not returned after 14 days. Family called; marked "not returned".', by: 'Sister Meera' },
    ];
    return write({ units, log, seededAt: now() });
  }
  async function ensure(patients) {
    if (db()) return db();
    let list = patients;
    if (!list) { try { list = await SB.api.patients(); } catch (_) { list = []; } }
    return seed(list || []);
  }
  function reset() { try { localStorage.removeItem(KEY); } catch (_) { /* ignore */ } memo = null; }

  const find = (code) => (db() ? db().units.find((u) => u.code.toLowerCase() === String(code || '').toLowerCase()) : null);
  const unitOfPatient = (pid) => (db() ? db().units.find((u) => u.loan && String(u.loan.patientId) === String(pid) && u.state === 'in_use') : null);
  function note(code, text, by) { const d = db(); d.log.unshift({ at: now(), code, text, by: by || 'Sister Anjali' }); d.log = d.log.slice(0, 60); write(d); }

  /* ---- the five moves of the life cycle ---- */
  function assign(code, patient, by) {
    const d = db(), u = find(code);
    if (!u || u.state !== 'stock') throw new Error('Only a unit that is in stock can be handed over.');
    const other = unitOfPatient(patient.id);
    if (other) throw new Error(`${patient.name} already has unit ${other.code}. Take that one back first.`);
    u.state = 'in_use'; u.loan = { patientId: patient.id, name: patient.name, from: now(), to: null }; u.lastSeen = now();
    write(d); note(code, `Handed over to ${patient.name}. Test breath OK. Their settings (language, goal, family contacts) now apply to this unit.`, by);
    return u;
  }
  function giveBack(code, by) {
    const d = db(), u = find(code);
    if (!u || u.state !== 'in_use') throw new Error('This unit is not out on loan.');
    const l = u.loan; l.to = now(); u.history.unshift(l); u.loan = null; u.state = 'returned'; u.lastSeen = now();
    write(d); note(code, `Returned by ${l.name}. Last sessions uploaded, loan closed. Their history stays on their own record.`, by);
    return u;
  }
  function clean(code, by) {
    const d = db(), u = find(code);
    if (!u || u.state !== 'returned') throw new Error('Only a returned unit can be cleaned.');
    u.state = 'cleaned'; write(d); note(code, 'Cleaned with a 70% alcohol wipe, checked for cracks, sensor window clear, charged. Signed.', by);
    return u;
  }
  function wipe(code, by) {
    const d = db(), u = find(code);
    if (!u || u.state !== 'cleaned') throw new Error('Clean and check the unit before wiping it.');
    u.state = 'stock'; u.battery = 100; write(d); note(code, 'Wiped: pairing cleared, stored sessions erased. The unit holds nothing about any person. Back in stock.', by);
    return u;
  }
  function mark(code, state, by) {
    const d = db(), u = find(code);
    if (!u) throw new Error('Unit not found.');
    if (state === 'lost' && u.loan) { u.history.unshift(u.loan); u.loan = null; }
    if (state === 'stock' && !['lost', 'faulty'].includes(u.state)) throw new Error('Only a found or repaired unit can go straight back to stock.');
    u.state = state; write(d);
    note(code, state === 'lost' ? 'Marked "not returned". Breaths from this unit are no longer accepted for any patient.' : state === 'faulty' ? 'Set aside as faulty.' : 'Found or repaired, checked and put back in stock.', by);
    return u;
  }

  SB.units = { STATES, ensure, reset, find, unitOfPatient, assign, giveBack, clean, wipe, mark, all: () => (db() ? db().units : []), log: () => (db() ? db().log : []) };
})();
