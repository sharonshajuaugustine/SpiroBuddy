/* SpiroBuddy - the patient's visits screen (patient-visits.html).
 * Reads /api/me/appointments with the patient session cookie (the same one the patient app opens: a link with ?id= or ?t=
 * opens it first, exactly as meds.html does). Very simple and big: the status word with an icon and a colour, the day and time
 * in words, the doctor and the place. A proposed new time gets two big buttons (yes / no). "Ask for a visit" = a day, a time,
 * an optional reason, then Send. English, Hindi, Tamil and Malayalam (Tamil and Malayalam need a native-speaker check
 * before real use). The words are fixed text - nothing here is written by AI, nothing gives medical advice, no payments.
 */
(function () {
  'use strict';
  const SB = window.SB;
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ic = (n, o) => (SB.icon ? SB.icon(n, o) : '');
  const $ = (s, r) => (r || document).querySelector(s);
  const q = new URLSearchParams(location.search);
  const LS = 'sb_meds_lang';            // the same key the medicines page uses, so the language follows the patient
  const LANGS = ['hi', 'en', 'ta', 'ml'];
  const NATIVE = { hi: 'हिंदी', en: 'English', ta: 'தமிழ்', ml: 'മലയാളം' };
  const LOC = { en: 'en-IN', hi: 'hi-IN', ta: 'ta-IN', ml: 'ml-IN' };

  const T = {
    en: {
      title: 'My visits', back: 'Back', myApp: 'My app', ask: 'Ask for a visit',
      askSub: 'Choose a day and a time. The hospital will answer here.',
      answer: 'Please answer', coming: 'Coming up', earlier: 'Earlier visits', showEarlier: 'Show all earlier visits',
      none: 'You have no visits yet.', noneHint: 'You can ask for a visit with your doctor.',
      noDoctor: 'No doctor is assigned to you yet. Please ask the hospital.',
      yes: 'Yes, this time is fine', no: 'No', proposedAsk: '{d} suggests this time instead. Is it fine for you?',
      cancel: 'Cancel this visit', cancelSure: 'Cancel this visit?', yesCancel: 'Yes, cancel it', keep: 'No, keep it',
      step1: 'Choose a day', step2: 'Choose a time', step3: 'What is it about? You can skip this.',
      checkup: 'Check-up', problem: 'A problem', other: 'Other',
      emergency: 'If you feel very unwell, do not wait for a visit. Tell your nurse now or call 112.',
      today: 'Today', tomorrow: 'Tomorrow', noTimes: 'No times',
      noDays: 'There are no free times in the next 14 days. Please ask the hospital.',
      yourRequest: 'You are asking for', send: 'Send request', sending: 'Sending…', pickTime: 'Choose a time to continue',
      sent: 'Your request was sent. The hospital will answer here.',
      accepted: 'Thank you. This visit is confirmed.', declinedDone: 'Done. That time is cancelled.', cancelledDone: 'This visit is cancelled.',
      taken: 'That time was just taken. Please choose another.',
      retry: 'Try again', errLoad: 'Could not load your visits. Please check your internet and try again.',
      errOpen: 'Please open this page from your SpiroBuddy app.', openApp: 'Open SpiroBuddy', errSave: 'That did not work. Please try again.',
      because: 'Reason: {r}', foot: 'Sample patient',
      s_requested: 'Requested', s_proposed: 'Alternative proposed', s_confirmed: 'Confirmed', s_declined: 'Declined', s_cancelled: 'Cancelled', s_attended: 'Attended', s_no_show: 'No-show',
    },
    hi: {
      title: 'डॉक्टर से मुलाक़ातें', back: 'पीछे', myApp: 'मेरा ऐप', ask: 'मुलाक़ात का समय माँगें',
      askSub: 'दिन और समय चुनिए। अस्पताल यहीं जवाब देगा।',
      answer: 'कृपया जवाब दें', coming: 'आने वाली', earlier: 'पहले की मुलाक़ातें', showEarlier: 'पहले की सब मुलाक़ातें दिखाएँ',
      none: 'अभी कोई मुलाक़ात नहीं है।', noneHint: 'आप अपने डॉक्टर से मिलने का समय माँग सकते हैं।',
      noDoctor: 'अभी आपके लिए कोई डॉक्टर तय नहीं है। कृपया अस्पताल से पूछें।',
      yes: 'हाँ, यह समय ठीक है', no: 'नहीं', proposedAsk: '{d} ने इसके बदले यह समय सुझाया है। क्या यह आपको ठीक है?',
      cancel: 'यह मुलाक़ात रद्द करें', cancelSure: 'यह मुलाक़ात रद्द करें?', yesCancel: 'हाँ, रद्द करें', keep: 'नहीं, रहने दें',
      step1: 'दिन चुनिए', step2: 'समय चुनिए', step3: 'किस बारे में? आप छोड़ भी सकते हैं।',
      checkup: 'जाँच', problem: 'कोई तकलीफ़', other: 'कुछ और',
      emergency: 'अगर आप बहुत बीमार महसूस करें तो मुलाक़ात का इंतज़ार न करें। अभी नर्स को बताएँ या 112 पर फ़ोन करें।',
      today: 'आज', tomorrow: 'कल', noTimes: 'कोई समय नहीं',
      noDays: 'अगले 14 दिनों में कोई खाली समय नहीं है। कृपया अस्पताल से पूछें।',
      yourRequest: 'आप यह समय माँग रहे हैं', send: 'अनुरोध भेजें', sending: 'भेज रहे हैं…', pickTime: 'आगे बढ़ने के लिए समय चुनिए',
      sent: 'आपका अनुरोध भेज दिया गया। अस्पताल यहीं जवाब देगा।',
      accepted: 'धन्यवाद। यह मुलाक़ात पक्की हो गई।', declinedDone: 'ठीक है। वह समय रद्द कर दिया गया।', cancelledDone: 'यह मुलाक़ात रद्द हो गई।',
      taken: 'वह समय अभी-अभी भर गया। कृपया दूसरा चुनिए।',
      retry: 'फिर कोशिश करें', errLoad: 'मुलाक़ातें नहीं खुलीं। कृपया इंटरनेट देखें और फिर कोशिश करें।',
      errOpen: 'कृपया यह पन्ना अपने SpiroBuddy ऐप से खोलें।', openApp: 'SpiroBuddy खोलें', errSave: 'यह नहीं हो पाया। कृपया फिर कोशिश करें।',
      because: 'कारण: {r}', foot: 'नमूना मरीज़',
      s_requested: 'अनुरोध भेजा', s_proposed: 'नया समय सुझाया गया', s_confirmed: 'पक्की', s_declined: 'मना किया गया', s_cancelled: 'रद्द', s_attended: 'आप आए', s_no_show: 'आप नहीं आए',
    },
    ta: {
      title: 'என் மருத்துவ சந்திப்புகள்', back: 'பின்', myApp: 'என் செயலி', ask: 'சந்திப்புக்குக் கேளுங்கள்',
      askSub: 'நாளையும் நேரத்தையும் தேர்ந்தெடுங்கள். மருத்துவமனை இங்கே பதில் சொல்லும்.',
      answer: 'தயவுசெய்து பதில் சொல்லுங்கள்', coming: 'வரவிருப்பவை', earlier: 'முந்தைய சந்திப்புகள்', showEarlier: 'முந்தைய எல்லா சந்திப்புகளையும் காட்டு',
      none: 'இன்னும் சந்திப்புகள் இல்லை.', noneHint: 'உங்கள் மருத்துவரைச் சந்திக்க நேரம் கேட்கலாம்.',
      noDoctor: 'உங்களுக்கு இன்னும் மருத்துவர் நியமிக்கப்படவில்லை. மருத்துவமனையிடம் கேளுங்கள்.',
      yes: 'ஆம், இந்த நேரம் சரி', no: 'இல்லை', proposedAsk: '{d} இதற்குப் பதிலாக இந்த நேரத்தைப் பரிந்துரைக்கிறார். இது உங்களுக்குச் சரியா?',
      cancel: 'இந்த சந்திப்பை ரத்து செய்', cancelSure: 'இந்த சந்திப்பை ரத்து செய்யவா?', yesCancel: 'ஆம், ரத்து செய்', keep: 'இல்லை, இருக்கட்டும்',
      step1: 'நாளைத் தேர்ந்தெடுங்கள்', step2: 'நேரத்தைத் தேர்ந்தெடுங்கள்', step3: 'எதைப் பற்றி? தவிர்க்கவும் செய்யலாம்.',
      checkup: 'பரிசோதனை', problem: 'ஒரு பிரச்சனை', other: 'வேறு',
      emergency: 'மிகவும் உடல்நலக் குறைவாக உணர்ந்தால் சந்திப்புக்குக் காத்திருக்காதீர்கள். உடனே செவிலியரிடம் சொல்லுங்கள் அல்லது 112 அழையுங்கள்.',
      today: 'இன்று', tomorrow: 'நாளை', noTimes: 'நேரம் இல்லை',
      noDays: 'அடுத்த 14 நாட்களில் காலி நேரம் இல்லை. மருத்துவமனையிடம் கேளுங்கள்.',
      yourRequest: 'நீங்கள் கேட்கும் நேரம்', send: 'கோரிக்கையை அனுப்பு', sending: 'அனுப்புகிறது…', pickTime: 'தொடர ஒரு நேரத்தைத் தேர்ந்தெடுங்கள்',
      sent: 'உங்கள் கோரிக்கை அனுப்பப்பட்டது. மருத்துவமனை இங்கே பதில் சொல்லும்.',
      accepted: 'நன்றி. இந்த சந்திப்பு உறுதியானது.', declinedDone: 'சரி. அந்த நேரம் ரத்து செய்யப்பட்டது.', cancelledDone: 'இந்த சந்திப்பு ரத்து செய்யப்பட்டது.',
      taken: 'அந்த நேரம் இப்போதுதான் எடுக்கப்பட்டது. வேறொன்றைத் தேர்ந்தெடுங்கள்.',
      retry: 'மீண்டும் முயற்சி', errLoad: 'சந்திப்புகளை ஏற்ற முடியவில்லை. இணையத்தைச் சரிபார்த்து மீண்டும் முயலுங்கள்.',
      errOpen: 'இந்தப் பக்கத்தை உங்கள் SpiroBuddy செயலியிலிருந்து திறக்கவும்.', openApp: 'SpiroBuddy திற', errSave: 'அது நடக்கவில்லை. மீண்டும் முயலுங்கள்.',
      because: 'காரணம்: {r}', foot: 'மாதிரி நோயாளி',
      s_requested: 'கோரப்பட்டது', s_proposed: 'வேறு நேரம் பரிந்துரைக்கப்பட்டது', s_confirmed: 'உறுதியானது', s_declined: 'மறுக்கப்பட்டது', s_cancelled: 'ரத்து செய்யப்பட்டது', s_attended: 'வந்தீர்கள்', s_no_show: 'வரவில்லை',
    },
    ml: {
      title: 'എന്റെ ഡോക്ടർ സന്ദർശനങ്ങൾ', back: 'തിരികെ', myApp: 'എന്റെ ആപ്പ്', ask: 'സന്ദർശനത്തിന് ആവശ്യപ്പെടുക',
      askSub: 'ദിവസവും സമയവും തിരഞ്ഞെടുക്കുക. ആശുപത്രി ഇവിടെ മറുപടി നൽകും.',
      answer: 'ദയവായി മറുപടി നൽകുക', coming: 'വരാനിരിക്കുന്നവ', earlier: 'മുൻപത്തെ സന്ദർശനങ്ങൾ', showEarlier: 'മുൻപത്തെ എല്ലാ സന്ദർശനങ്ങളും കാണിക്കുക',
      none: 'ഇതുവരെ സന്ദർശനങ്ങളില്ല.', noneHint: 'നിങ്ങളുടെ ഡോക്ടറെ കാണാൻ സമയം ചോദിക്കാം.',
      noDoctor: 'നിങ്ങൾക്ക് ഇതുവരെ ഡോക്ടറെ നിശ്ചയിച്ചിട്ടില്ല. ദയവായി ആശുപത്രിയോട് ചോദിക്കുക.',
      yes: 'അതെ, ഈ സമയം ശരിയാണ്', no: 'അല്ല', proposedAsk: '{d} പകരം ഈ സമയം നിർദ്ദേശിക്കുന്നു. ഇത് നിങ്ങൾക്ക് ശരിയാണോ?',
      cancel: 'ഈ സന്ദർശനം റദ്ദാക്കുക', cancelSure: 'ഈ സന്ദർശനം റദ്ദാക്കണോ?', yesCancel: 'അതെ, റദ്ദാക്കുക', keep: 'വേണ്ട, നിലനിൽക്കട്ടെ',
      step1: 'ദിവസം തിരഞ്ഞെടുക്കുക', step2: 'സമയം തിരഞ്ഞെടുക്കുക', step3: 'എന്തിനെക്കുറിച്ചാണ്? ഒഴിവാക്കുകയും ചെയ്യാം.',
      checkup: 'പരിശോധന', problem: 'ഒരു പ്രശ്നം', other: 'മറ്റുള്ളത്',
      emergency: 'വളരെ അസ്വസ്ഥത തോന്നുന്നുവെങ്കിൽ സന്ദർശനത്തിനായി കാത്തിരിക്കരുത്. ഉടൻ നഴ്സിനോട് പറയുക അല്ലെങ്കിൽ 112 വിളിക്കുക.',
      today: 'ഇന്ന്', tomorrow: 'നാളെ', noTimes: 'സമയമില്ല',
      noDays: 'അടുത്ത 14 ദിവസങ്ങളിൽ ഒഴിവുള്ള സമയമില്ല. ദയവായി ആശുപത്രിയോട് ചോദിക്കുക.',
      yourRequest: 'നിങ്ങൾ ആവശ്യപ്പെടുന്നത്', send: 'അഭ്യർത്ഥന അയയ്ക്കുക', sending: 'അയയ്ക്കുന്നു…', pickTime: 'തുടരാൻ ഒരു സമയം തിരഞ്ഞെടുക്കുക',
      sent: 'നിങ്ങളുടെ അഭ്യർത്ഥന അയച്ചു. ആശുപത്രി ഇവിടെ മറുപടി നൽകും.',
      accepted: 'നന്ദി. ഈ സന്ദർശനം ഉറപ്പിച്ചു.', declinedDone: 'ശരി. ആ സമയം റദ്ദാക്കി.', cancelledDone: 'ഈ സന്ദർശനം റദ്ദാക്കി.',
      taken: 'ആ സമയം ഇപ്പോൾ തന്നെ എടുത്തു. മറ്റൊന്ന് തിരഞ്ഞെടുക്കുക.',
      retry: 'വീണ്ടും ശ്രമിക്കുക', errLoad: 'സന്ദർശനങ്ങൾ തുറക്കാനായില്ല. ഇന്റർനെറ്റ് പരിശോധിച്ച് വീണ്ടും ശ്രമിക്കുക.',
      errOpen: 'ഈ പേജ് നിങ്ങളുടെ SpiroBuddy ആപ്പിൽ നിന്ന് തുറക്കുക.', openApp: 'SpiroBuddy തുറക്കുക', errSave: 'അത് നടന്നില്ല. വീണ്ടും ശ്രമിക്കുക.',
      because: 'കാരണം: {r}', foot: 'സാമ്പിൾ രോഗി',
      s_requested: 'അഭ്യർത്ഥിച്ചു', s_proposed: 'മറ്റൊരു സമയം നിർദ്ദേശിച്ചു', s_confirmed: 'ഉറപ്പിച്ചു', s_declined: 'നിരസിച്ചു', s_cancelled: 'റദ്ദാക്കി', s_attended: 'വന്നു', s_no_show: 'വന്നില്ല',
    },
  };
  /* icon + tone for each state (colour is never the only sign: there is always the icon and the word) */
  const ST = {
    requested: { icon: 'hourglass', tone: 'warn' }, proposed: { icon: 'refresh', tone: 'info' }, confirmed: { icon: 'check-circle', tone: 'good' },
    declined: { icon: 'x-circle', tone: 'bad' }, cancelled: { icon: 'x-circle', tone: 'muted' }, attended: { icon: 'check', tone: 'good' }, no_show: { icon: 'alert-triangle', tone: 'warn' },
  };
  const REASONS = [['checkup', 'Check-up'], ['problem', 'A problem'], ['other', 'Other']];   // the doctor reads the English words

  let lang = pickLang(), langChosen = !!(q.get('lang') && T[q.get('lang')]) || !!stored();
  let data = null, failed = null, view = 'home', flash = null, busy = false, session = null, sessionTried = false;
  let confirmId = null, showAllEarlier = false, ask = null, lastJson = '';

  function stored() { try { const v = localStorage.getItem(LS); return T[v] ? v : null; } catch (_) { return null; } }
  function pickLang() { const l = q.get('lang'); return (T[l] && l) || stored() || 'hi'; }
  function tr(k, v) {
    let s = (T[lang] && T[lang][k]) || T.en[k] || k;
    if (v) Object.keys(v).forEach((x) => { s = s.split('{' + x + '}').join(v[x] == null ? '' : v[x]); });
    return s;
  }

  /* ---------------------------------------------------------------- dates and times (India time) */
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const pad = (n) => String(n).padStart(2, '0');
  function ist(iso) {
    const t = new Date(iso).getTime(); if (isNaN(t)) return null;
    const d = new Date(t + 330 * 60000);
    return { y: d.getUTCFullYear(), mo: d.getUTCMonth(), d: d.getUTCDate(), wd: d.getUTCDay(), h: d.getUTCHours(), m: d.getUTCMinutes(), ymd: d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate()) };
  }
  const todayYmd = () => ist(new Date().toISOString()).ymd;
  function addDays(ymd, n) { const d = new Date(ymd + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  function fmt(opts, date) { try { return new Intl.DateTimeFormat(LOC[lang] || 'en-IN', Object.assign({ timeZone: 'Asia/Kolkata' }, opts)).format(date); } catch (_) { return ''; } }
  function timeEn(p) { return (p.h % 12 || 12) + ':' + pad(p.m) + ' ' + (p.h < 12 ? 'AM' : 'PM'); }
  function timeText(iso) {
    const p = ist(iso); if (!p) return '';
    return lang === 'en' ? timeEn(p) : (fmt({ hour: 'numeric', minute: '2-digit', hour12: true }, new Date(iso)) || timeEn(p));
  }
  function whenText(a) {
    if (lang === 'en' && a.when_words) return a.when_words;
    const p = ist(a.start_at);
    if (lang !== 'en') {
      const s = fmt({ weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true }, new Date(a.start_at));
      if (s) return s;
    }
    return a.when_words || (p ? DAYS[p.wd] + ', ' + p.d + ' ' + MONTHS[p.mo] + ' ' + p.y + ', ' + timeEn(p) : '');
  }
  function dayParts(ymd) {                                   // {wd: "Thu", d: 15, mo: "October"} in the chosen language
    const date = new Date(ymd + 'T06:30:00Z'), p = ist(date.toISOString());
    if (lang === 'en') return { wd: DAYS[p.wd].slice(0, 3), d: p.d, mo: MONTHS[p.mo] };
    return { wd: fmt({ weekday: 'short' }, date) || DAYS[p.wd].slice(0, 3), d: p.d, mo: fmt({ month: 'long' }, date) || MONTHS[p.mo] };
  }
  function dayWords(ymd) {
    const date = new Date(ymd + 'T06:30:00Z'), p = ist(date.toISOString());
    if (lang === 'en') return DAYS[p.wd] + ', ' + p.d + ' ' + MONTHS[p.mo] + ' ' + p.y;
    return fmt({ weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }, date) || (DAYS[p.wd] + ', ' + p.d + ' ' + MONTHS[p.mo] + ' ' + p.y);
  }
  const future = (a) => new Date(a.start_at).getTime() > Date.now();

  /* ---------------------------------------------------------------- loading */
  async function openSession() {
    const t = q.get('t'), id = Number(q.get('id'));
    if (!t && !id) return null;
    try {
      const r = await SB.api.post('/api/me/session', t ? { token: t } : { patient_id: id });
      if (t) { q.delete('t'); try { history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : '') + location.hash); } catch (_) { /* keep the address */ } }
      return r || null;
    } catch (_) { return null; }
  }
  async function load(silent) {
    failed = null;
    try {
      if (!sessionTried && (q.get('t') || Number(q.get('id')))) { sessionTried = true; session = await openSession(); }
      let r;
      try { r = await SB.api.get('/api/me/appointments'); }
      catch (e) {
        if (e && e.status === 401 && !session && (q.get('t') || Number(q.get('id'))) && (session = await openSession())) r = await SB.api.get('/api/me/appointments');
        else throw e;
      }
      if (session && !langChosen && T[session.language]) lang = session.language;
      const json = JSON.stringify(r);
      if (silent && json === lastJson && !failed) return;       // nothing changed: do not redraw under the patient's finger
      lastJson = json; data = r || { doctor: null, items: [] };
    } catch (e) {
      if (silent) return;                                      // a quiet refresh never replaces the screen with an error
      failed = (e && e.status === 401) ? 'open' : 'load';
    }
    paint();
  }

  /* ---------------------------------------------------------------- drawing */
  function paintStatic() {
    document.documentElement.lang = lang;
    document.title = tr('title') + ' · SpiroBuddy';
    $('#pv-title').textContent = tr('title');
    $('#pv-foot').textContent = tr('foot');
    $('#pv-lang').innerHTML = LANGS.map((c) => `<button type="button" data-l="${c}" lang="${c}" aria-pressed="${c === lang}">${esc(NATIVE[c])}</button>`).join('');
  }
  const msg = (kind, icon, text) => `<div class="pv-msg ${kind}" role="${kind === 'bad' ? 'alert' : 'status'}">${ic(icon, { size: 28 })}<span>${esc(text)}</span></div>`;
  const appLink = () => {
    return 'meds.html?lang=' + encodeURIComponent(lang);
  };

  function card(a, isPast) {
    const s = ST[a.state] || ST.requested, can = a.can || {};
    const isFuture = future(a);
    const word = tr('s_' + a.state) || a.status_words || a.state;
    let h = `<section class="pv-card t-${s.tone}${isPast ? ' past' : ''}" aria-label="${esc(word + ', ' + whenText(a))}" data-id="${esc(a.id)}">
      <p class="pv-state"><span class="ic">${ic(s.icon, { size: 30 })}</span><span>${esc(word)}</span></p>
      <p class="pv-when">${esc(whenText(a))}</p>`;
    if (a.doctor_name) h += `<p class="pv-line">${ic('user', { size: 26 })}<span>${esc(a.doctor_name)}</span></p>`;
    if (a.location) h += `<p class="pv-line">${ic('hospital', { size: 26 })}<span>${esc(a.location)}</span></p>`;
    if (a.state === 'declined' && a.decline_reason) h += `<p class="pv-line">${ic('info', { size: 26 })}<span>${esc(tr('because', { r: a.decline_reason }))}</span></p>`;
    const canAnswer = a.state === 'proposed' && isFuture && (can.accept !== false);
    const canCancel = (can.cancel !== undefined ? !!can.cancel : (a.state === 'requested' || a.state === 'confirmed')) && isFuture && !canAnswer;
    if (canAnswer) {
      h += `<p class="pv-ask">${esc(tr('proposedAsk', { d: a.doctor_name || '' }))}</p>
        <div class="pv-btns"><button type="button" class="pv-btn" data-do="accept" data-id="${esc(a.id)}">${ic('check-circle', { size: 32 })}<span>${esc(tr('yes'))}</span></button>
        <button type="button" class="pv-btn plain" data-do="decline" data-id="${esc(a.id)}">${ic('x', { size: 30 })}<span>${esc(tr('no'))}</span></button></div>`;
    } else if (canCancel) {
      if (String(confirmId) === String(a.id)) {
        h += `<p class="pv-ask">${esc(tr('cancelSure'))}</p><div class="pv-btns">
          <button type="button" class="pv-btn sure" data-do="cancel" data-id="${esc(a.id)}">${ic('x-circle', { size: 30 })}<span>${esc(tr('yesCancel'))}</span></button>
          <button type="button" class="pv-btn plain" data-do="keep">${ic('arrow-left', { size: 28 })}<span>${esc(tr('keep'))}</span></button></div>`;
      } else {
        h += `<div class="pv-btns"><button type="button" class="pv-btn danger" data-do="ask-cancel" data-id="${esc(a.id)}">${ic('x', { size: 28 })}<span>${esc(tr('cancel'))}</span></button></div>`;
      }
    }
    return h + '</section>';
  }

  function renderHome() {
    const items = (data && data.items) || [];
    const doctor = data && data.doctor;
    const answer = items.filter((a) => a.state === 'proposed' && future(a));
    const coming = items.filter((a) => !answer.includes(a) && future(a) && ['requested', 'proposed', 'confirmed'].includes(a.state));
    const earlier = items.filter((a) => !answer.includes(a) && !coming.includes(a));
    let h = `<a class="pv-btn plain" href="${esc(appLink())}">${ic('arrow-left', { size: 28 })}<span>${esc(tr('myApp'))}</span></a>
      <h1 class="pv-h1">${esc(tr('title'))}</h1>`;
    if (flash) h += msg(flash.kind, flash.kind === 'bad' ? 'alert-triangle' : 'check-circle', flash.text);
    if (answer.length) h += `<h2 class="pv-sec ask">${ic('hourglass', { size: 32 })}<span>${esc(tr('answer'))}</span></h2>${answer.map((a) => card(a)).join('')}`;
    if (doctor) h += `<button type="button" class="pv-btn" data-do="ask">${ic('calendar', { size: 32 })}<span>${esc(tr('ask'))}</span></button>`;
    else h += msg('info', 'info', tr('noDoctor'));
    if (!items.length) {
      h += `<div class="pv-empty">${ic('calendar', { size: 56 })}<p>${esc(tr('none'))}</p>${doctor ? `<p style="color:var(--text-2);font-size:1.2rem">${esc(tr('noneHint'))}</p>` : ''}</div>`;
      return h;
    }
    if (coming.length) h += `<h2 class="pv-sec">${ic('calendar', { size: 32 })}<span>${esc(tr('coming'))}</span></h2>${coming.map((a) => card(a)).join('')}`;
    if (earlier.length) {
      const shown = showAllEarlier ? earlier : earlier.slice(0, 3);
      h += `<h2 class="pv-sec">${ic('clock', { size: 32 })}<span>${esc(tr('earlier'))}</span></h2>${shown.map((a) => card(a, true)).join('')}`;
      if (earlier.length > shown.length) h += `<button type="button" class="pv-btn plain pv-more" data-do="more">${esc(tr('showEarlier'))}</button>`;
    }
    return h;
  }

  /* ---- ask for a visit */
  function renderAsk() {
    let h = `<button type="button" class="pv-btn plain" data-do="home">${ic('arrow-left', { size: 28 })}<span>${esc(tr('back'))}</span></button>
      <h1 class="pv-h1">${esc(tr('ask'))}</h1><p class="pv-sub">${esc(tr('askSub'))}</p>`;
    if (!ask || ask.loading) return h + '<span class="skeleton pv-skel" style="height:72px;margin-bottom:12px"></span><span class="skeleton pv-skel" style="height:72px"></span>';
    if (ask.fatal) return h + msg('bad', 'alert-triangle', ask.fatal);
    if (ask.error) h += msg('bad', 'alert-triangle', ask.error);
    const anyFree = ask.days.some((d) => d.slots && d.slots.length);
    if (!anyFree) return h + msg('info', 'info', tr('noDays'));
    const today = todayYmd(), tomorrow = addDays(today, 1);
    h += `<h2 class="pv-step"><b>1</b><span>${esc(tr('step1'))}</span></h2><div class="pv-grid" role="group" aria-label="${esc(tr('step1'))}">` +
      ask.days.map((d) => {
        const p = dayParts(d.ymd), free = d.slots && d.slots.length;
        const small = d.ymd === today ? tr('today') : d.ymd === tomorrow ? tr('tomorrow') : p.mo;
        return `<button type="button" class="pv-pick" data-day="${d.ymd}" aria-pressed="${ask.day === d.ymd}"${free ? '' : ' disabled'}><span class="big">${esc(p.wd + ' ' + p.d)}</span><span class="small">${esc(free ? small : tr('noTimes'))}</span></button>`;
      }).join('') + '</div>';
    const day = ask.days.find((d) => d.ymd === ask.day);
    if (day && day.slots && day.slots.length) {
      h += `<h2 class="pv-step" id="pv-s2"><b>2</b><span>${esc(tr('step2'))}</span></h2><div class="pv-grid" role="group" aria-label="${esc(tr('step2'))}">` +
        day.slots.map((s) => `<button type="button" class="pv-pick time" data-start="${esc(s.start_at)}" aria-pressed="${ask.slot && ask.slot.start_at === s.start_at}"><span class="big">${esc(timeText(s.start_at))}</span></button>`).join('') + '</div>';
    }
    if (ask.slot) {
      h += `<h2 class="pv-step" id="pv-s3"><b>3</b><span>${esc(tr('step3'))}</span></h2><div class="pv-choices" role="group" aria-label="${esc(tr('step3'))}">` +
        REASONS.map(([k]) => `<button type="button" class="pv-choice" data-reason="${k}" aria-pressed="${ask.reason === k}"><span class="tick">${ic('check', { size: 20 })}</span><span>${esc(tr(k))}</span></button>`).join('') + '</div>';
      if (ask.reason === 'problem') h += `<div class="pv-msg info" style="margin-top:12px">${ic('info', { size: 28 })}<span>${esc(tr('emergency'))}</span></div>`;
      h += `<div class="pv-sum"><p class="l">${esc(tr('yourRequest'))}</p><p class="v">${esc(dayWords(ask.day))}, ${esc(timeText(ask.slot.start_at))}</p></div>
        <button type="button" class="pv-btn" data-do="send"${ask.sending ? ' disabled' : ''}>${ic('send', { size: 30 })}<span>${esc(tr(ask.sending ? 'sending' : 'send'))}</span></button>`;
    } else if (day) {
      h += `<p style="color:var(--text-2);margin-top:12px">${esc(tr('pickTime'))}</p>`;
    }
    return h;
  }

  function paint(keepScroll) {
    paintStatic();
    const main = $('#pv-main');
    const y = window.scrollY;
    if (failed === 'open') {
      main.innerHTML = `<div class="pv-empty">${ic('info', { size: 56 })}<p>${esc(tr('errOpen'))}</p><a class="pv-btn" href="app.html">${esc(tr('openApp'))}</a></div>`;
    } else if (failed) {
      main.innerHTML = msg('bad', 'alert-triangle', tr('errLoad')) + `<button type="button" class="pv-btn" data-do="retry">${ic('refresh', { size: 28 })}<span>${esc(tr('retry'))}</span></button>`;
    } else if (!data) {
      return;
    } else {
      main.innerHTML = view === 'ask' ? renderAsk() : renderHome();
    }
    if (keepScroll) window.scrollTo(0, y);
  }

  /* ---------------------------------------------------------------- actions */
  const errText = (e, fallbackKey) => {
    if (e && e.status === 409 && fallbackKey === 'taken') return tr('taken');
    if (lang === 'en' && e && e.message && e.status && e.status !== 500 && !/^HTTP \d+/.test(e.message) && !/^[[{]/.test(e.message) && e.message !== 'Not Found') return e.message;
    return tr(fallbackKey || 'errSave');
  };
  async function answer(act, id) {
    if (busy) return; busy = true;
    document.querySelectorAll('#pv-main .pv-btn').forEach((b) => { b.disabled = true; });
    try {
      await SB.api.post('/api/me/appointments/' + encodeURIComponent(id) + '/' + act, {});
      flash = { kind: 'good', text: tr(act === 'accept' ? 'accepted' : act === 'decline' ? 'declinedDone' : 'cancelledDone') };
    } catch (e) { flash = { kind: 'bad', text: errText(e) }; }
    confirmId = null; busy = false;
    await load();
    window.scrollTo(0, 0);
  }

  async function openAsk() {
    view = 'ask'; flash = null; confirmId = null;
    ask = { loading: true, days: [], day: null, slot: null, reason: '', error: '', fatal: '', sending: false };
    paint(); window.scrollTo(0, 0);
    const t0 = todayYmd();
    const days = Array.from({ length: 14 }, (_, i) => ({ ymd: addDays(t0, i), slots: null, err: null }));
    await Promise.all(days.map(async (d) => {
      try { const r = await SB.api.get('/api/me/slots?date=' + d.ymd); d.slots = Array.isArray(r) ? r : []; }
      catch (e) { d.slots = []; d.err = e; }
    }));
    ask.days = days; ask.loading = false;
    if (days.every((d) => d.err)) {
      const e = days[0].err;
      ask.fatal = e && e.status === 409 ? tr('noDoctor') : tr('errLoad');
    }
    if (view === 'ask') paint();
  }
  async function refreshDay(ymd) {
    const d = ask && ask.days.find((x) => x.ymd === ymd); if (!d) return;
    try { const r = await SB.api.get('/api/me/slots?date=' + ymd); d.slots = Array.isArray(r) ? r : []; } catch (_) { /* keep the old list */ }
  }
  async function send() {
    if (!ask || !ask.slot || ask.sending) return;
    ask.sending = true; ask.error = ''; paint(true);
    const body = { start_at: ask.slot.start_at };
    const why = REASONS.find(([k]) => k === ask.reason);
    if (why) body.reason_text = why[1];
    try {
      await SB.api.post('/api/me/appointments', body);
      flash = { kind: 'good', text: tr('sent') };
      view = 'home'; ask = null;
      await load();
      window.scrollTo(0, 0);
    } catch (e) {
      ask.sending = false; ask.error = errText(e, e && e.status === 409 ? 'taken' : 'errSave');
      if (e && e.status === 409) { await refreshDay(ask.day); ask.slot = null; }
      paint(); window.scrollTo(0, 0);
    }
  }

  /* ---------------------------------------------------------------- events */
  document.addEventListener('click', (e) => {
    const lb = e.target.closest('#pv-lang [data-l]');
    if (lb) {
      lang = lb.dataset.l; langChosen = true;
      try { localStorage.setItem(LS, lang); } catch (_) { /* private mode */ }
      paint(true); return;
    }
    const dayBtn = e.target.closest('[data-day]');
    if (dayBtn && ask) {
      ask.day = dayBtn.dataset.day; ask.slot = null; ask.error = ''; paint(true);
      const s2 = $('#pv-s2'); if (s2) s2.scrollIntoView({ block: 'start' });
      return;
    }
    const slotBtn = e.target.closest('[data-start]');
    if (slotBtn && ask) {
      const day = ask.days.find((d) => d.ymd === ask.day);
      ask.slot = (day && day.slots.find((s) => s.start_at === slotBtn.dataset.start)) || null; ask.error = ''; paint(true);
      const s3 = $('#pv-s3'); if (s3) s3.scrollIntoView({ block: 'start' });
      return;
    }
    const rs = e.target.closest('[data-reason]');
    if (rs && ask) { ask.reason = ask.reason === rs.dataset.reason ? '' : rs.dataset.reason; paint(true); return; }
    const b = e.target.closest('[data-do]'); if (!b || b.disabled) return;
    const a = b.dataset.do, id = b.dataset.id;
    if (a === 'ask') openAsk();
    else if (a === 'home') { view = 'home'; ask = null; flash = null; load(); window.scrollTo(0, 0); }
    else if (a === 'send') send();
    else if (a === 'accept' || a === 'decline' || a === 'cancel') answer(a, id);
    else if (a === 'ask-cancel') { confirmId = id; paint(true); }
    else if (a === 'keep') { confirmId = null; paint(true); }
    else if (a === 'more') { showAllEarlier = true; paint(true); }
    else if (a === 'retry') { $('#pv-main').innerHTML = '<div class="pv-empty"><span class="skeleton" style="height:72px"></span></div>'; load(); }
  });

  /* ---------------------------------------------------------------- start */
  (async function start() {
    paintStatic();
    try { await SB.api.init(); } catch (_) { /* a failed load shows the retry message */ }
    await load();
    // a quiet refresh now and then, so a new time suggested by the hospital shows up without a reload
    setInterval(() => { if (!document.hidden && !busy && view === 'home' && confirmId == null && !failed) load(true); }, 45000);
  })();
})();
