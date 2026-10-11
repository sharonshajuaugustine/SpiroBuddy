/* SpiroBuddy - patient login page (patient-login.html).
 * The patient types the hospital registration number from the slip and the 6-digit PIN. The server
 * checks them (POST /api/me/login) and opens the patient session; then the page goes to /app.html.
 * Words: English, Hindi, Tamil, Malayalam. Tamil and Malayalam need a check by a native speaker before real use.
 * The demo box (Ravi's number and PIN) is filled from GET /api/me/login-demo, which answers only in DEMO_MODE.
 * The PIN is never written to the address bar, to storage or to the console. */
(function () {
  'use strict';
  const $ = (s) => document.querySelector(s);
  const LANGS = ['hi', 'en', 'ta', 'ml'];
  const NATIVE = { hi: 'हिंदी', en: 'English', ta: 'தமிழ்', ml: 'മലയാളം' };
  const LS = 'sb_meds_lang';                 // the same key the medicines page uses, so the choice follows the patient

  const T = {
    en: {
      sub: 'Patient login', h: 'Log in', lead: 'Use the number and the 6-digit PIN from the slip the hospital gave you.',
      noL: 'Hospital registration number', noH: 'It is on your slip. For example ABC-000123.',
      pinL: '6-digit PIN', pinH: 'The 6 numbers on your slip.', show: 'Show', hide: 'Hide',
      go: 'Open my medicines', going: 'Please wait…',
      demoH: 'Demo patient (fictional)', demoP: 'Only on this demo site. Tap the button and the boxes fill in.',
      demoNo: 'Number', demoPin: 'PIN', demoFill: 'Fill in the boxes',
      demoChanged: 'The PIN of this demo patient was changed. Use the number and PIN on the new slip.',
      help: 'Cannot find your slip? Ask the nurse or the hospital desk for a new PIN.', staff: 'Hospital staff? Log in here',
      foot: 'This page opens your own medicines on this phone. It does not diagnose and it cannot change your medicines.',
      fl: 'Status of this login:',
      format: 'Please type your hospital number and the 6 numbers of your PIN.',
      wrong: "That number and PIN don't match. Please check the slip or ask the hospital.",
      locked: 'Too many wrong tries. Please wait 15 minutes and try again, or ask the hospital for a new PIN.',
      ip: 'Too many tries from this phone. Please wait 15 minutes and try again.',
      notSet: 'This login is not set up yet. Please ask the hospital.',
      offline: 'Cannot reach the server. Please check your internet and try again.',
      other: 'Something went wrong. Please try again.',
    },
    hi: {
      sub: 'मरीज़ लॉगिन', h: 'लॉगिन करें', lead: 'अस्पताल की पर्ची पर लिखा नंबर और 6 अंकों का PIN डालिए।',
      noL: 'अस्पताल का पंजीकरण नंबर', noH: 'यह आपकी पर्ची पर है। जैसे ABC-000123।',
      pinL: '6 अंकों का PIN', pinH: 'पर्ची पर लिखे 6 अंक।', show: 'दिखाएँ', hide: 'छिपाएँ',
      go: 'मेरी दवाइयाँ खोलें', going: 'कृपया रुकिए…',
      demoH: 'डेमो मरीज़ (नकली)', demoP: 'यह सिर्फ़ इस डेमो साइट पर है। बटन दबाइए, खाने भर जाएँगे।',
      demoNo: 'नंबर', demoPin: 'PIN', demoFill: 'खाने भर दें',
      demoChanged: 'इस डेमो मरीज़ का PIN बदल दिया गया है। नई पर्ची का नंबर और PIN डालिए।',
      help: 'पर्ची नहीं मिल रही? नर्स या अस्पताल की डेस्क से नया PIN माँगिए।', staff: 'अस्पताल का स्टाफ़? यहाँ लॉगिन करें',
      foot: 'यह पन्ना इस फ़ोन पर आपकी अपनी दवाइयाँ खोलता है। यह कोई निदान नहीं करता और आपकी दवाएँ नहीं बदल सकता।',
      fl: 'इस लॉगिन की स्थिति:',
      format: 'कृपया अस्पताल का नंबर और PIN के 6 अंक डालिए।',
      wrong: 'यह नंबर और PIN मेल नहीं खाते। कृपया पर्ची देखिए या अस्पताल से पूछिए।',
      locked: 'बहुत ज़्यादा गलत कोशिशें हुईं। कृपया 15 मिनट रुककर फिर कोशिश कीजिए, या अस्पताल से नया PIN माँगिए।',
      ip: 'इस फ़ोन से बहुत ज़्यादा कोशिशें हुईं। कृपया 15 मिनट रुककर फिर कोशिश कीजिए।',
      notSet: 'यह लॉगिन अभी चालू नहीं है। कृपया अस्पताल से पूछिए।',
      offline: 'सर्वर से जुड़ नहीं पाए। कृपया इंटरनेट देखकर फिर कोशिश कीजिए।',
      other: 'कुछ गड़बड़ हो गई। कृपया फिर कोशिश कीजिए।',
    },
    ta: {
      sub: 'நோயாளர் உள்நுழைவு', h: 'உள்நுழைக', lead: 'மருத்துவமனை கொடுத்த சீட்டில் உள்ள எண்ணையும் 6 இலக்க PIN-ஐயும் உள்ளிடுங்கள்.',
      noL: 'மருத்துவமனை பதிவு எண்', noH: 'இது உங்கள் சீட்டில் உள்ளது. எடுத்துக்காட்டு: ABC-000123.',
      pinL: '6 இலக்க PIN', pinH: 'சீட்டில் உள்ள 6 எண்கள்.', show: 'காட்டு', hide: 'மறை',
      go: 'என் மருந்துகளைத் திற', going: 'சற்று காத்திருங்கள்…',
      demoH: 'டெமோ நோயாளர் (கற்பனை)', demoP: 'இந்த டெமோ தளத்தில் மட்டும். பொத்தானை அழுத்தினால் கட்டங்கள் நிரம்பும்.',
      demoNo: 'எண்', demoPin: 'PIN', demoFill: 'கட்டங்களை நிரப்பு',
      demoChanged: 'இந்த டெமோ நோயாளரின் PIN மாற்றப்பட்டுள்ளது. புதிய சீட்டில் உள்ள எண்ணையும் PIN-ஐயும் பயன்படுத்துங்கள்.',
      help: 'சீட்டு கிடைக்கவில்லையா? செவிலியரிடம் அல்லது மருத்துவமனை மேசையில் புதிய PIN கேளுங்கள்.', staff: 'மருத்துவமனை ஊழியரா? இங்கே உள்நுழைக',
      foot: 'இந்தப் பக்கம் இந்த ஃபோனில் உங்கள் சொந்த மருந்துகளைத் திறக்கிறது. இது நோயைக் கண்டறியாது; உங்கள் மருந்துகளை மாற்றாது.',
      fl: 'இந்த உள்நுழைவின் நிலை:',
      format: 'மருத்துவமனை எண்ணையும் PIN-இன் 6 எண்களையும் உள்ளிடுங்கள்.',
      wrong: 'அந்த எண்ணும் PIN-உம் பொருந்தவில்லை. சீட்டைப் பாருங்கள் அல்லது மருத்துவமனையிடம் கேளுங்கள்.',
      locked: 'பலமுறை தவறாக உள்ளிட்டுவிட்டீர்கள். 15 நிமிடம் காத்திருந்து மீண்டும் முயலுங்கள், அல்லது மருத்துவமனையிடம் புதிய PIN கேளுங்கள்.',
      ip: 'இந்த ஃபோனிலிருந்து அதிக முயற்சிகள். 15 நிமிடம் காத்திருந்து மீண்டும் முயலுங்கள்.',
      notSet: 'இந்த உள்நுழைவு இன்னும் தயாராகவில்லை. மருத்துவமனையிடம் கேளுங்கள்.',
      offline: 'சர்வரை அடைய முடியவில்லை. இணையத்தைச் சரிபார்த்து மீண்டும் முயலுங்கள்.',
      other: 'ஏதோ தவறு நடந்தது. மீண்டும் முயலுங்கள்.',
    },
    ml: {
      sub: 'രോഗിയുടെ ലോഗിൻ', h: 'ലോഗിൻ ചെയ്യുക', lead: 'ആശുപത്രി തന്ന സ്ലിപ്പിലെ നമ്പറും 6 അക്ക PIN-ഉം നൽകുക.',
      noL: 'ആശുപത്രി രജിസ്ട്രേഷൻ നമ്പർ', noH: 'ഇത് നിങ്ങളുടെ സ്ലിപ്പിലുണ്ട്. ഉദാഹരണം: ABC-000123.',
      pinL: '6 അക്ക PIN', pinH: 'സ്ലിപ്പിലെ 6 അക്കങ്ങൾ.', show: 'കാണിക്കുക', hide: 'മറയ്ക്കുക',
      go: 'എന്റെ മരുന്നുകൾ തുറക്കുക', going: 'ദയവായി കാത്തിരിക്കൂ…',
      demoH: 'ഡെമോ രോഗി (സാങ്കൽപ്പികം)', demoP: 'ഈ ഡെമോ സൈറ്റിൽ മാത്രം. ബട്ടൺ അമർത്തിയാൽ കളങ്ങൾ നിറയും.',
      demoNo: 'നമ്പർ', demoPin: 'PIN', demoFill: 'കളങ്ങൾ നിറയ്ക്കുക',
      demoChanged: 'ഈ ഡെമോ രോഗിയുടെ PIN മാറ്റി. പുതിയ സ്ലിപ്പിലെ നമ്പറും PIN-ഉം ഉപയോഗിക്കുക.',
      help: 'സ്ലിപ്പ് കണ്ടില്ലേ? നഴ്സിനോടോ ആശുപത്രി ഡെസ്കിലോ പുതിയ PIN ചോദിക്കുക.', staff: 'ആശുപത്രി ജീവനക്കാരനാണോ? ഇവിടെ ലോഗിൻ ചെയ്യുക',
      foot: 'ഈ പേജ് ഈ ഫോണിൽ നിങ്ങളുടെ സ്വന്തം മരുന്നുകൾ തുറക്കുന്നു. ഇത് രോഗനിർണയം നടത്തില്ല, മരുന്നുകൾ മാറ്റാനും കഴിയില്ല.',
      fl: 'ഈ ലോഗിനിന്റെ നില:',
      format: 'ആശുപത്രി നമ്പറും PIN-ലെ 6 അക്കങ്ങളും നൽകുക.',
      wrong: 'ആ നമ്പറും PIN-ഉം ചേരുന്നില്ല. സ്ലിപ്പ് നോക്കുക, അല്ലെങ്കിൽ ആശുപത്രിയോട് ചോദിക്കുക.',
      locked: 'ഒരുപാട് തവണ തെറ്റി. 15 മിനിറ്റ് കാത്തിരുന്ന് വീണ്ടും ശ്രമിക്കുക, അല്ലെങ്കിൽ ആശുപത്രിയോട് പുതിയ PIN ചോദിക്കുക.',
      ip: 'ഈ ഫോണിൽ നിന്ന് വളരെയധികം ശ്രമങ്ങൾ. 15 മിനിറ്റ് കാത്തിരുന്ന് വീണ്ടും ശ്രമിക്കുക.',
      notSet: 'ഈ ലോഗിൻ ഇതുവരെ ഒരുക്കിയിട്ടില്ല. ആശുപത്രിയോട് ചോദിക്കുക.',
      offline: 'സെർവറിൽ എത്താൻ കഴിഞ്ഞില്ല. ഇന്റർനെറ്റ് നോക്കി വീണ്ടും ശ്രമിക്കുക.',
      other: 'എന്തോ തകരാറുണ്ടായി. വീണ്ടും ശ്രമിക്കുക.',
    },
  };

  const q = new URLSearchParams(location.search);
  function stored() { try { const v = localStorage.getItem(LS); return T[v] ? v : null; } catch (_) { return null; } }
  function guess() {
    const l = String((navigator.language || 'en')).slice(0, 2).toLowerCase();
    return T[l] ? l : 'en';
  }
  let lang = (T[q.get('lang')] && q.get('lang')) || stored() || guess();
  let demo = null, busy = false, pinShown = false;
  const tr = (k) => (T[lang] && T[lang][k]) || T.en[k] || '';
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ic = (n, o) => (window.SB && SB.icon ? SB.icon(n, o) : '');

  /* ---------- the words ---------- */
  function paintLang() {
    $('#pl-lang').innerHTML = LANGS.map((l) =>
      `<button type="button" data-l="${l}" lang="${l}" aria-pressed="${l === lang}">${esc(NATIVE[l])}</button>`).join('');
  }
  function paint() {
    document.documentElement.lang = lang;
    const set = (id, k) => { $(id).textContent = tr(k); };
    set('#pl-sub', 'sub'); set('#pl-h', 'h'); set('#pl-lead', 'lead');
    set('#pl-no-l', 'noL'); set('#pl-no-h', 'noH'); set('#pl-pin-l', 'pinL'); set('#pl-pin-h', 'pinH');
    set('#pl-help', 'help'); set('#pl-staff', 'staff'); set('#pl-foot', 'foot'); set('#pl-fl', 'fl');
    $('#pl-show').textContent = pinShown ? tr('hide') : tr('show');
    $('#pl-go').innerHTML = ic('lock', { size: 28 }) + '<span>' + esc(busy ? tr('going') : tr('go')) + '</span>';
    paintLang();
    paintDemo();
    if (lastError) showError(lastError);
  }

  /* ---------- the demo box ---------- */
  function paintDemo() {
    const box = $('#pl-demo');
    if (!demo || !demo.demo) { box.hidden = true; return; }
    box.hidden = false;
    const pinRow = demo.pin
      ? `<dt>${esc(tr('demoPin'))}</dt><dd>${esc(demo.pin)}</dd>` : '';
    box.innerHTML = `<h2 id="pl-demo-h">${ic('flask', { size: 22 })}<span>${esc(tr('demoH'))}</span></h2>
      <p>${esc(demo.pin ? tr('demoP') : tr('demoChanged'))}</p>
      <dl><dt>${esc(tr('demoNo'))}</dt><dd>${esc(demo.registration_no)}</dd>${pinRow}</dl>
      ${demo.pin ? `<button type="button" class="pl-btn outline small" id="pl-fill">${esc(tr('demoFill'))}</button>` : ''}`;
    const fill = $('#pl-fill');
    if (fill) fill.addEventListener('click', () => {
      $('#pl-no').value = demo.registration_no;
      $('#pl-pin').value = demo.pin;
      clearError();
      $('#pl-go').focus();
    });
  }
  async function loadDemo() {
    try {
      const r = await fetch('/api/me/login-demo', { cache: 'no-store', credentials: 'same-origin', headers: { Accept: 'application/json' } });
      demo = r.ok ? await r.json() : null;
    } catch (_) { demo = null; }
    paintDemo();
  }

  /* ---------- errors ---------- */
  let lastError = null;
  function showError(key) {
    lastError = key;
    const box = $('#pl-error');
    box.innerHTML = ic('alert-octagon', { size: 22 }) + '<span>' + esc(tr(key)) + '</span>';
    box.hidden = false;
    try { box.scrollIntoView({ block: 'center', behavior: 'smooth' }); } catch (_) { /* old browser */ }
  }
  function clearError() {
    lastError = null;
    $('#pl-error').hidden = true;
    $('#pl-no').removeAttribute('aria-invalid');
    $('#pl-pin').removeAttribute('aria-invalid');
  }
  function errorKey(status, message) {
    if (status === 400) return 'format';
    if (status === 401) return 'wrong';
    if (status === 429) return /wrong tries/i.test(message || '') ? 'locked' : 'ip';
    if (status === 503) return 'notSet';
    if (status === 0) return 'offline';
    return 'other';
  }

  /* ---------- log in ---------- */
  function setBusy(on) {
    busy = on;
    $('#pl-go').disabled = on;
    $('#pl-go').setAttribute('aria-busy', String(on));
    $('#pl-go').innerHTML = ic('lock', { size: 28 }) + '<span>' + esc(on ? tr('going') : tr('go')) + '</span>';
  }
  async function submit(ev) {
    ev.preventDefault();
    if (busy) return;
    clearError();
    const number = $('#pl-no').value.trim();
    const pin = $('#pl-pin').value.replace(/\s+/g, '');
    if (!number) { $('#pl-no').setAttribute('aria-invalid', 'true'); $('#pl-no').focus(); return showError('format'); }
    if (!/^\d{6}$/.test(pin)) { $('#pl-pin').setAttribute('aria-invalid', 'true'); $('#pl-pin').focus(); return showError('format'); }
    setBusy(true);
    try {
      const r = await fetch('/api/me/login', {
        method: 'POST', credentials: 'same-origin', cache: 'no-store',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json', 'X-SB': '1' },
        body: JSON.stringify({ registration_no: number, pin: pin }),
      });
      let data = null;
      try { data = await r.json(); } catch (_) { /* not JSON */ }
      if (!r.ok) {
        setBusy(false);
        $('#pl-pin').value = '';
        if (r.status === 401) $('#pl-pin').setAttribute('aria-invalid', 'true');
        showError(errorKey(r.status, data && (data.error || data.detail)));
        if (r.status === 401) $('#pl-pin').focus();
        return;
      }
      if (data && data.language && T[data.language]) { try { localStorage.setItem(LS, data.language); } catch (_) { /* private mode */ } }
      // app.html picks its patient from ?id= (it does not read the session by itself yet), so hand the id over.
      // The login itself is the cookie the server just set; the id in the address opens nothing on its own.
      const next = data && Number(data.patient_id) ? '/app.html?id=' + encodeURIComponent(Number(data.patient_id)) : '/app.html';
      location.assign(next);                         // keep the button busy while the next page loads
    } catch (_) {
      setBusy(false);
      showError('offline');
    }
  }

  /* ---------- wire up ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    paint();
    $('#pl-lang').addEventListener('click', (e) => {
      const b = e.target.closest('button[data-l]');
      if (!b) return;
      lang = b.dataset.l;
      try { localStorage.setItem(LS, lang); } catch (_) { /* private mode */ }
      paint();
    });
    $('#pl-show').addEventListener('click', () => {
      pinShown = !pinShown;
      $('#pl-pin').type = pinShown ? 'text' : 'password';
      $('#pl-show').setAttribute('aria-pressed', String(pinShown));
      $('#pl-show').textContent = pinShown ? tr('hide') : tr('show');
    });
    $('#pl-form').addEventListener('submit', submit);
    if (window.SB && SB.ui && SB.ui.loadFeatures) SB.ui.loadFeatures();      // fills the status badge (names come from /api/features)
    $('#pl-no').addEventListener('input', clearError);
    $('#pl-pin').addEventListener('input', clearError);
    loadDemo();
  });
})();
