/* /architecture.html: colours every diagram box from the status registry (GET /api/features) and draws the legend.
 * The SVG ships with the statuses as they stood when it was drawn; this script keeps it in step with the registry. */
(function () {
  const P = window.SBPub;
  const ui = window.SB.ui;
  const STATES = ['live', 'simulated', 'in_development', 'planned'];

  const legend = document.getElementById('arch-legend');
  if (legend) {
    legend.innerHTML = STATES.map((k) =>
      `<span class="legend-line"><span class="swatch ${k}" aria-hidden="true"></span><b>${P.esc(ui.FSTATUS[k].word)}</b></span>`).join('');
  }

  ui.loadFeatures().then((list) => {
    const by = {};
    (list || []).forEach((f) => { if (f && f.key) by[f.key] = f; });
    document.querySelectorAll('.arch-svg .box[data-key]').forEach((g) => {
      const f = by[g.getAttribute('data-key')];
      if (!f || !ui.FSTATUS[f.status]) return;               // unknown key: keep what the drawing shows
      STATES.forEach((s) => g.classList.remove('s-' + s));
      g.classList.add('s-' + f.status);
      const word = ui.FSTATUS[f.status].word;
      const st = g.querySelector('.st');
      if (st) st.textContent = word;
      const label = g.getAttribute('aria-label') || '';
      g.setAttribute('aria-label', label.replace(/:[^:]*$/, ': ' + word));
    });
  });
})();
