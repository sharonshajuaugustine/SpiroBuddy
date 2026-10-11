/* /impact.html: draws the tables from /data/impact.json, runs the calculator and shows the live demo numbers.
 * Every figure carries a source tag or one of the labels Counted / Estimate / Assumption / Target. */
(function () {
  const P = window.SBPub;
  const { esc, lbl, src, nf } = P;
  const $ = (id) => document.getElementById(id);

  function renderSegments(d) {
    $('segments').innerHTML = d.segments.map((s) => `
      <article class="pub-card">
        <div class="card-top"><h3>${esc(s.name)}</h3><span data-feature="${esc(s.key)}"></span></div>
        <p>${esc(s.text)}</p>
        <p class="small muted">${esc(s.caution)}</p>
        <div class="tags">${src(s.source)}</div>
      </article>`).join('');
    $('buyers').querySelector('tbody').innerHTML = d.buyers.map((b) => `
      <tr><td data-label="Rank">${b.rank}</td><td data-label="Who">${esc(b.who)}</td>
      <td data-label="Time to a yes">${esc(b.time)} ${lbl('estimate')}</td><td data-label="Source">${src(b.source)}</td></tr>`).join('');
  }

  function renderMarket(m) {
    $('counted').innerHTML = m.counted.map((c) => `
      <div class="stat"><span class="big">${esc(c.value)}</span><span class="what">${esc(c.text)}</span>
      <div class="tags">${lbl(c.label)}${src(c.source)}</div></div>`).join('');
    $('market').querySelector('tbody').innerHTML = m.steps.map((s) => `
      <tr><th scope="row" data-label="Step">${esc(s.step)}</th>
      <td data-label="Cautious" class="num">${esc(s.low)}</td><td data-label="Middle" class="num">${esc(s.mid)}</td><td data-label="Optimistic" class="num">${esc(s.high)}</td>
      <td data-label="Label and source">${lbl(s.label)} ${src(s.source)}</td></tr>`).join('');
    $('market-honest').innerHTML = m.honest.map((t) => `<li>${esc(t)}</li>`).join('');
  }

  function renderFunnel(f) {
    $('funnel-base').innerHTML = `${esc(f.base)}. ${src(f.tag)}`;
    $('journey').innerHTML = f.steps.map((s) => `
      <li><span class="jn" aria-hidden="true">${s.n}</span><div>
        <div class="jh"><b>${esc(s.name)}</b><span class="jwho">${esc(s.who)}</span></div>
        <div class="jnum">${esc(s.number)}</div>
        ${s.bar ? `<div class="meter jbar" role="img" aria-label="${s.bar} out of 100 of the eligible patients"><span style="width:${s.bar}%"></span></div>` : ''}
        <div class="tags">${lbl(s.label)}${s.label2 ? lbl(s.label2) : ''}</div>
      </div></li>`).join('');
    $('funnel-foot').textContent = f.footnote;
  }

  /* ---------- calculator ---------- */
  function retention(d7, d14) {
    // fraction of those who joined still going on each of days 1..14 (straight lines between the known points)
    const pts = [[1, 0.9], [3, 0.85], [7, d7], [14, d14]];
    const out = [];
    for (let day = 1; day <= 14; day++) {
      let a = pts[0], b = pts[pts.length - 1];
      for (let i = 0; i < pts.length - 1; i++) if (day >= pts[i][0] && day <= pts[i + 1][0]) { a = pts[i]; b = pts[i + 1]; break; }
      out.push(a[0] === b[0] ? a[1] : a[1] + (b[1] - a[1]) * (day - a[0]) / (b[0] - a[0]));
    }
    return out;
  }
  const DUE_PER_DAY = 14, DONE_SHARE = 0.58, DAY1 = 0.9;

  function calcModel(v) {
    const joined = v.hospitals * v.eligible * (v.join / 100);
    const personDays = retention(v.d7 / 100, v.d14 / 100).reduce((a, b) => a + b, 0);
    return {
      joined,
      coached: joined * DAY1,
      sessions: joined * personDays * DUE_PER_DAY * DONE_SHARE,
      families: joined * (v.family / 100),
      calls: joined * (1 - v.d14 / 100),
      personDays,
    };
  }

  function renderCalc(c) {
    const box = $('sliders');
    box.innerHTML = c.sliders.map((s) => `
      <div class="slider">
        <label for="sl-${s.id}"><span>${esc(s.label)}</span><output id="out-${s.id}" for="sl-${s.id}"></output></label>
        <input type="range" id="sl-${s.id}" min="${s.min}" max="${s.max}" step="${s.step}" value="${s.value}" data-id="${s.id}">
        <p class="hint">${esc(s.hint)} ${src(s.source)}</p>
      </div>`).join('');
    $('fixed').innerHTML = c.fixed.map((f) => `<li>${esc(f.text)}: <b>${esc(f.value)}</b> ${lbl(f.label)} ${src(f.source)}</li>`).join('');
    $('formula').innerHTML = [
      'Patients who join = hospitals × eligible patients × share who join.',
      'Patients coached = patients who join × the share who do a session on day 1.',
      'Sessions completed = patients who join × days of use over 14 days × 14 sessions due a day × 58% done. Days of use come from a straight line through day 1, day 3, day 7 and day 14.',
      'Families kept informed = patients who join × share of families who opt in.',
      'Nurse calls targeted = patients who join and are no longer going by day 14. These are the people the nurse list would point a call at; the nurse decides.',
    ].map((t) => `<li>${esc(t)}</li>`).join('');

    const get = () => {
      const v = {};
      c.sliders.forEach((s) => { v[s.id] = Number($('sl-' + s.id).value); });
      return v;
    };
    const paint = () => {
      const v = get();
      if (v.d14 > v.d7) { v.d14 = v.d7; $('sl-d14').value = v.d14; }
      c.sliders.forEach((s) => { $('out-' + s.id).textContent = nf(v[s.id]) + (s.unit || ''); });
      const m = calcModel(v);
      const cards = [
        ['Patients coached', m.coached, 'who join, then do a session on day 1'],
        ['Sessions completed', m.sessions, 'breathing sessions done in their 14 days'],
        ['Families kept informed', m.families, 'with the patient\'s consent'],
        ['Nurse calls targeted', m.calls, 'patients no longer going by day 14'],
      ];
      $('outputs').innerHTML = cards.map(([t, n, w]) => `
        <div class="stat"><span class="what"><b>${esc(t)}</b></span><span class="big">${nf(n)}</span><span class="what">${esc(w)}, per month</span>
        <div class="tags">${lbl('estimate')}</div></div>`).join('');
    };
    box.addEventListener('input', paint);
    paint();
  }

  /* ---------- live demo numbers ---------- */
  function tile(title, big, what, tags) {
    return `<div class="stat${big === null ? ' no-data' : ''}"><span class="what"><b>${esc(title)}</b></span>
      <span class="big">${big === null ? 'No data yet' : big}</span><span class="what">${esc(what)}</span><div class="tags">${tags || lbl('demo')}</div></div>`;
  }
  function renderMetrics(m) {
    const pct = (v) => `${nf(v, 1)}<small>%</small>`;
    const dosesN = (m.doses_reported || 0) + (m.doses_missed || 0);
    const visitsN = (m.follow_ups_attended || 0) + (m.follow_ups_missed || 0);
    $('metrics').innerHTML = [
      tile('Patients coached', m.patients_coached ? nf(m.patients_coached) : null, `of ${nf(m.patients_in_programme || 0)} fake patients in the programme`),
      tile('Sessions completed', m.sessions_completed ? nf(m.sessions_completed) : null, 'breathing sessions in the demo database'),
      tile('Sessions done of due, today', m.sessions_due_today ? pct(m.sessions_done_of_due_pct) : null, `${nf(m.sessions_done_today || 0)} done of ${nf(m.sessions_due_today || 0)} due so far`),
      tile('Medicine doses reported', dosesN ? pct(m.doses_reported_pct) : null, `${nf(m.doses_reported || 0)} reported, ${nf(m.doses_missed || 0)} missed. Patient taps count as reported.`),
      tile('Follow-up visits kept', visitsN ? pct(m.follow_ups_kept_pct) : null, `${nf(m.follow_ups_attended || 0)} attended, ${nf(m.follow_ups_missed || 0)} did not come`),
      tile('Families informed', m.families_informed ? nf(m.families_informed) : null, 'families who opted in with consent'),
    ].join('');
    const t = m.as_of ? new Date(m.as_of).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: '2-digit', year: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true }) : '';
    $('metrics-foot').textContent = `${m.hospital || 'Demo hospital (fictional)'} · ${m.label || 'demo data, fake patients'}${t ? ' · as of ' + t + ' IST' : ''}`;
    P.hydrate();
  }
  async function loadMetrics() {
    try { renderMetrics(await P.getJSON('/api/impact')); }
    catch (e) {
      $('metrics').innerHTML = '<div class="callout warn"><p>The live numbers are not available right now. The rest of the page is unaffected.</p><button class="btn sm" id="retry" type="button">Try again</button></div>';
      const r = $('retry'); if (r) r.addEventListener('click', loadMetrics);
    }
  }

  function renderSdg(d) {
    $('sdg-src').textContent = d.sdg_source;
    $('sdg-table').querySelector('tbody').innerHTML = d.sdg.map((s) => `
      <tr><th scope="row" data-label="Target">${esc(s.target)}${s.main ? ' <span class="lbl target">Main link</span>' : ''}${s.later ? ' <span class="lbl assumption">Later</span>' : ''}</th>
      <td data-label="The UN wording, short">${esc(s.wording)}</td><td data-label="Our honest link">${esc(s.link)}</td></tr>`).join('');
  }

  loadMetrics();
  P.getJSON('/data/impact.json').then((d) => {
    renderSegments(d); renderMarket(d.market); renderFunnel(d.funnel); renderCalc(d.calculator); renderSdg(d);
    P.hydrate();
  }).catch((e) => {
    console.warn('impact data failed', e);
    $('segments').innerHTML = '<div class="callout warn"><p>The data file for this page did not load. Please reload.</p></div>';
  });
})();
