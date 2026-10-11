/* /trust.html: draws the rule tables from /data/trust.json and the live AI audit numbers from GET /api/impact
 * (public, so this page needs no login). Statuses come from the registry through data-feature badges. */
(function () {
  const P = window.SBPub;
  const { esc, lbl, src, badge, nf } = P;
  const $ = (id) => document.getElementById(id);

  function renderRules(groups) {
    $('rule-groups').innerHTML = groups.map((g) => `
      <h3>${esc(g.name)} <span class="src">${esc(g.source)}</span></h3>
      <div class="table-scroll" style="margin-bottom:var(--sp-4)"><table class="pub-table stack-table">
        <thead><tr><th>Rule</th><th>What SpiroBuddy does</th><th>Status</th></tr></thead>
        <tbody>${g.rows.map((r) => `
          <tr><th scope="row" data-label="Rule">${esc(r.rule)}</th><td data-label="What SpiroBuddy does">${esc(r.does)}</td>
          <td data-label="Status"><div class="tags" style="margin:0">${r.keys.map(badge).join('')}</div></td></tr>`).join('')}
        </tbody></table></div>`).join('');
  }

  function stat(big, what, empty) {
    return `<div class="stat${empty ? ' no-data' : ''}"><span class="big">${empty ? 'No data yet' : big}</span><span class="what">${esc(what)}</span><div class="tags">${lbl('demo')}</div></div>`;
  }
  function renderAi(m) {
    const drafts = m.ai_drafts || 0;
    const reviewed = m.ai_reviewed || 0;
    const lines = m.ai_lines_total || 0;
    $('ai-stats').innerHTML = [
      stat(nf(drafts), 'AI drafts made on this site', drafts === 0),
      stat(`${nf(m.ai_lines_edited_pct || 0, 1)}<small>%</small>`, `of lines were changed by a person (${nf(lines)} lines in ${nf(reviewed)} reviewed drafts)`, reviewed === 0 || lines === 0),
      stat(`${nf(m.ai_rejected_pct || 0, 1)}<small>%</small>`, 'of reviewed drafts were rejected', reviewed === 0),
    ].join('');
    $('ai-foot').textContent = drafts === 0
      ? 'No AI draft has been made yet. That is expected: the AI is optional, and without a key (or when a patient chose no AI) the typed route is used. The numbers fill in as people review drafts.'
      : `${m.hospital || 'Fictional hospital'} · ${m.label || 'sample patients'}. A high share of changed lines is useful to know, not a failure: it shows people are checking.`;
  }
  async function loadAi() {
    try { renderAi(await P.getJSON('/api/impact')); }
    catch (e) {
      $('ai-stats').innerHTML = '<div class="callout warn"><p>The live AI numbers are not available right now.</p><button class="btn sm" id="retry" type="button">Try again</button></div>';
      const r = $('retry'); if (r) r.addEventListener('click', loadAi);
    }
  }

  loadAi();
  P.getJSON('/data/trust.json').then((d) => {
    renderRules(d.rule_groups);
    $('safe-rules').innerHTML = d.safe_rules.map((t) => `<li>${esc(t)}</li>`).join('');
    $('safe-src').textContent = d.safe_source;
    $('checklist').innerHTML = d.checklist.map((t) => `<li>${esc(t)}</li>`).join('');
    $('check-src').textContent = d.checklist_source;
    $('gemini-points').innerHTML = d.gemini_points.map((p) =>
      `<li>${esc(p.text)} ${(p.keys || []).map(badge).join(' ')}</li>`).join('');
    P.hydrate();
  }).catch((e) => {
    console.warn('trust data failed', e);
    $('rule-groups').innerHTML = '<div class="callout warn"><p>The data file for this page did not load. Please reload.</p></div>';
  });
})();
