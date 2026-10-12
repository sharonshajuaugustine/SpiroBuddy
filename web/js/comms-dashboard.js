/* SpiroBuddy – Alerts inbox on the dashboard (acknowledge / snooze / assign to me / resolve),
 * plus small alert badges on the triage-list rows. Needs api.js, ui.js, comms.js (icons.js optional). */
(function () {
  const SB = window.SB;
  const { esc, $, $$, link, toast, busy, ago, ic } = SB.ui;
  const C = SB.comms;
  const SEV_ICON = { red: 'alert-octagon', amber: 'alert-triangle', info: 'info' };
  const SEV_WORD = { red: 'Needs a person now', amber: 'Watch', info: 'Info' };

  function mountInbox(el) {
    let tab = 'active';
    let list = [];
    const TABS = [['active', 'Open'], ['acknowledged', 'Acknowledged'], ['snoozed', 'Snoozed'], ['resolved', 'Resolved'], ['all', 'All']];
    el.innerHTML = `
      <div class="card-head">
        <h2>${ic('bell')}Alerts inbox</h2>
        <span class="chip bad" id="ai-red" title="Red alerts: a person is needed now"><span class="dot"></span><b>–</b>&nbsp;red</span>
        <span class="chip warn" id="ai-amber" title="Amber alerts: watch"><span class="dot"></span><b>–</b>&nbsp;amber</span>
        <span class="chip" id="ai-mine" title="Assigned to you">${ic('user', { size: 13 })}<b>–</b>&nbsp;mine</span>
        <div class="spacer"></div>
        <label for="ai-me" class="small">I am</label>
        <select id="ai-me" class="sm-select" disabled><option>${esc(C.me())}</option></select>
      </div>
      <div class="seg" role="group" aria-label="Alert filter" id="ai-tabs">${TABS.map(([k, l]) => `<button type="button" data-tab="${k}" aria-pressed="${k === tab}">${l}</button>`).join('')}</div>
      <ul class="alerts" id="ai-list" aria-live="polite"><li><span class="skeleton" style="height:64px"></span></li><li><span class="skeleton" style="height:64px"></span></li></ul>
      <p class="card-sub" style="margin:.75rem 0 0">${ic('info', { size: 13 })} Care-team only – patients and families never see these. Alerts come from fixed rules (missed sessions, no answer, red-flag words, lower than usual), never from the AI.</p>`;
    $('#ai-me', el).addEventListener('change', (e) => { C.setMe(e.target.value); render(); });
    $('#ai-tabs', el).addEventListener('click', (e) => {
      const b = e.target.closest('button[data-tab]'); if (!b) return;
      tab = b.dataset.tab;
      $$('#ai-tabs button', el).forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.tab === tab)));
      refresh().catch(() => {});
    });

    function row(a) {
      const st = a.status;
      const mine = a.assigned_to && a.assigned_to === C.me();
      return `<li class="alert-item sev-${esc(a.severity)} st-${esc(st)}" data-id="${a.id}">
        <div class="alert-main">
          <div class="alert-top">
            <span class="sev sev-${esc(a.severity)}">${ic(SEV_ICON[a.severity] || 'info', { size: 12 })}${esc(SEV_WORD[a.severity] || a.severity)}</span>
            <span class="tag">${esc(a.kind_label || a.kind)}</span>
            ${st !== 'open' ? `<span class="tag ${st === 'resolved' ? 'sent' : 'dry'}">${esc(st)}${st === 'snoozed' && a.snooze_until ? ' until ' + esc(C.timeOnly(a.snooze_until).slice(0, 5)) : ''}</span>` : ''}
            ${a.assigned_to ? `<span class="chip${mine ? ' ok' : ''}" title="Assigned">${ic('user', { size: 12 })}${esc(a.assigned_to)}</span>` : ''}
            <span class="subtle small" style="margin-left:auto" title="${esc(a.created_at)}">${esc(ago(a.created_at))}</span>
          </div>
          <div class="alert-title"><a href="${link('patient.html?id=' + encodeURIComponent(a.patient_id))}">${esc(a.title)}</a></div>
          ${a.detail ? `<details class="alert-detail"><summary>Details</summary><div>${esc(a.detail)}</div></details>` : ''}
        </div>
        <div class="alert-actions">
          ${st !== 'resolved' ? `<button class="btn sm primary" data-act="call" type="button" title="Your phone rings first, then the patient">${ic('phone', { size: 14 })}Call patient</button>` : ''}
          ${st === 'open' || st === 'snoozed' ? `<button class="btn sm" data-act="ack" type="button">${ic('check', { size: 14 })}Acknowledge</button>` : ''}
          ${st !== 'resolved' ? `<button class="btn sm" data-act="snooze" type="button" title="Hide for 30 minutes">${ic('clock', { size: 14 })}Snooze 30 min</button>` : ''}
          ${st !== 'resolved' && !mine ? `<button class="btn sm" data-act="assign" type="button">${ic('user-check', { size: 14 })}Assign to me</button>` : ''}
          ${st !== 'resolved' ? `<button class="btn sm good" data-act="resolve" type="button">${ic('check-circle', { size: 14 })}Resolve</button>` : `<button class="btn sm" data-act="reopen" type="button">${ic('refresh', { size: 14 })}Re-open</button>`}
        </div></li>`;
    }

    function render() {
      const box = $('#ai-list', el);
      box.innerHTML = list.length ? list.map(row).join('') : `<li class="empty">${ic('check-circle', { size: 26 })}<b>${tab === 'active' ? 'No open alerts' : 'Nothing here'}</b>${tab === 'active' ? 'Everyone is on track or already handled.' : ''}</li>`;
    }

    $('#ai-list', el).addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-act]'); if (!btn) return;
      const li = btn.closest('[data-id]'); const id = li.dataset.id;
      const a = list.find((x) => String(x.id) === id);
      const act = btn.dataset.act;
      busy(btn, async () => {
        if (act === 'call') {
          const r = await C.api.callPatient(a.patient_id, C.me());
          toast(r.dry_run ? `Dry run – would ring ${C.me()}'s phone, then connect ${a.patient_name}` : `Calling – your phone rings first`, r.dry_run ? '' : 'good', 6000);
          return;
        }
        const body = { by: C.me() };
        if (act === 'snooze') body.minutes = 30;
        if (act === 'assign') body.to = C.me();
        await C.api.alertAct(id, act, body);
        toast({ ack: 'Acknowledged', snooze: 'Snoozed for 30 min', assign: 'Assigned to you', resolve: 'Resolved', reopen: 'Re-opened' }[act], 'good');
        await refresh();
      }).catch(() => {});
    });

    async function refresh() {
      if (SB.api.state.mock) { $('#ai-list', el).innerHTML = `<li class="empty">${ic('wifi-off', { size: 26 })}<b>Alerts need the live server</b>Mock mode shows patient data only.</li>`; return; }
      const res = await C.api.alerts(tab === 'active' ? 'active' : tab);
      const sig = JSON.stringify(res) + C.me();
      if (sig !== refresh.sig && !el.querySelector('.busy') && !el.querySelector('details[open]') && !el.querySelector('#ai-list').contains(document.activeElement)) { refresh.sig = sig; list = res; render(); }
    }
    document.addEventListener('sb:alert-counts', (e) => {
      const c = e.detail || {};
      $('#ai-red b', el).textContent = c.red ?? 0;
      $('#ai-amber b', el).textContent = c.amber ?? 0;
      $('#ai-mine b', el).textContent = c.mine ?? 0;
      decorateRows(c.by_patient || {});
    });
    SB.ui.poll(refresh, 3000);
  }

  /* small bell badge next to each patient's name in the triage list when they have open alerts */
  let lastBy = {};
  function decorateRows(by) {
    lastBy = by;
    $$('#patients tr[data-id]').forEach((tr) => {
      const slot = tr.querySelector('.alert-slot'); if (!slot) return;
      const b = by[tr.dataset.id];
      if (!b || !b.open) { slot.innerHTML = ''; return; }
      const txt = `${b.open} open alert${b.open === 1 ? '' : 's'}`;
      slot.innerHTML = `<span class="alert-badge${b.red ? ' red' : ''}" title="${txt}">${ic('bell', { size: 12 })}${b.open}<span class="sr-only"> ${txt}</span></span>`;
    });
  }
  const host = document.getElementById('patients');
  if (host) new MutationObserver(() => decorateRows(lastBy)).observe(host, { childList: true });

  SB.commsDashboard = { mountInbox };
})();
