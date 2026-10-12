/* Optional patient choice. No provider request or prescription is issued here. */
(() => {
  let generation = 0;
  const T = {
    en: {title:'Optional AI processing', text:'If you allow it, your doctor’s prescription notepad text may be sent to Google Gemini to prepare a draft. AI does not give medical advice. Your doctor must review the draft. You can use the manual prescription workflow without AI and turn this choice off later.', label:'I allow this optional AI processing', save:'Save my choice', saved:'Your choice was saved.', error:'Your choice could not be saved. Please try again.', loading:'Loading your choice…', demo:'Prototype choice for this demo. Real patient use requires an appropriate hospital consent process.'},
    hi: {title:'वैकल्पिक AI प्रोसेसिंग', text:'अनुमति देने पर डॉक्टर की दवा संबंधी नोटपैड सामग्री Google Gemini को ड्राफ्ट बनाने के लिए भेजी जा सकती है। AI चिकित्सा सलाह नहीं देता। डॉक्टर को ड्राफ्ट जाँचना होगा। बिना AI भी पर्ची बनाई जा सकती है। आप बाद में अनुमति बंद कर सकते हैं।', label:'मैं इस वैकल्पिक AI प्रोसेसिंग की अनुमति देता/देती हूँ', save:'मेरी पसंद सेव करें', saved:'आपकी पसंद सेव हो गई।', error:'पसंद सेव नहीं हो सकी। फिर कोशिश करें।', loading:'आपकी पसंद लोड हो रही है…', demo:'यह डेमो का प्रोटोटाइप विकल्प है। असली मरीजों के लिए अस्पताल की उचित सहमति प्रक्रिया चाहिए।'}
  };
  async function mount() {
    const current = ++generation;
    const foot = document.getElementById('m-foot');
    if (!foot) return;
    const previous = document.getElementById('patient-ai-consent');
    if (previous) previous.remove();
    let stored = null;
    try { stored = localStorage.getItem('sb_meds_lang'); } catch (_) {}
    const selected = document.querySelector('#m-lang [aria-pressed="true"]');
    const lang = (selected && selected.dataset.l) || stored || new URLSearchParams(location.search).get('lang') || document.documentElement.lang;
    const t = T[lang] || T.en;
    const section = document.createElement('section');
    section.id = 'patient-ai-consent';
    section.className = 'm-card';
    const title = document.createElement('h2'); title.textContent = t.title;
    const text = document.createElement('p'); text.textContent = t.text;
    const label = document.createElement('label');
    label.style.cssText = 'display:flex;gap:12px;align-items:flex-start;margin:16px 0';
    const input = document.createElement('input'); input.type = 'checkbox'; input.disabled = true;
    input.style.cssText = 'width:24px;height:24px;flex-shrink:0';
    label.append(input, document.createTextNode(t.label));
    const button = document.createElement('button'); button.className = 'm-btn'; button.textContent = t.save; button.disabled = true;
    const status = document.createElement('p'); status.setAttribute('role','status'); status.textContent = t.loading;
    section.append(title,text,label,button,status);
    foot.before(section);
    try {
      let r;
      // A patient link can establish its session asynchronously on this page.
      for (let attempt = 0; attempt < 6; attempt++) {
        r = await fetch('/api/me/ai-consent', {credentials:'same-origin',cache:'no-store'});
        if (current !== generation) return;
        if (r.status !== 401) break;
        await new Promise(resolve => setTimeout(resolve, 400));
      }
      if (!r.ok) { section.remove(); return; }
      const data = await r.json();
      if (current !== generation) return;
      input.checked = data.ai_use === true;
      status.textContent = ''; input.disabled = false; button.disabled = false;
      if (data.demo) { const note = document.createElement('p'); note.textContent = t.demo; section.append(note); }
    } catch (_) { section.remove(); return; }
    button.addEventListener('click', async () => {
      button.disabled = true; input.disabled = true;
      try {
        const r = await fetch('/api/me/ai-consent', {method:'POST',credentials:'same-origin', headers:{'Content-Type':'application/json','X-SB':'1'},
          body:JSON.stringify({ai_use:input.checked,language:['en','hi','ta','ml'].includes(lang)?lang:'en'})});
        if (!r.ok) throw new Error();
        const data = await r.json(); input.checked = data.ai_use === true; status.textContent = t.saved;
      } catch (_) { status.textContent = t.error; }
      finally { button.disabled = false; input.disabled = false; }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
  document.addEventListener('click', (event) => {
    if (!event.target.closest('#m-lang [data-l]')) return;
    ++generation;
    const old = document.getElementById('patient-ai-consent');
    if (old) old.remove();
    setTimeout(mount, 0);
  }, true);
})();
