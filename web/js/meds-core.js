/* SpiroBuddy - medicines: the words in four languages (English, Hindi, Tamil, Malayalam) and the
 * shared drawing code for a medicine line. Used by meds.html (the patient), prescribe.html (the
 * doctor's preview of what the patient sees) and rx.html (the pharmacist, English only).
 * Tamil and Malayalam text needs a check by a native speaker before real use.
 * All text comes from the doctor's own entries or the fixed words below - no AI writes any of it.
 */
(function () {
  const SB = (window.SB = window.SB || {});
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ic = (n, o) => (SB.icon ? SB.icon(n, o) : '');

  const LANGS = ['hi', 'en', 'ta', 'ml'];
  const NATIVE = { hi: 'हिंदी', en: 'English', ta: 'தமிழ்', ml: 'മലയാളം' };
  const SPEECH = { hi: 'hi-IN', en: 'en-IN', ta: 'ta-IN', ml: 'ml-IN' };

  const T = {
    en: {
      title: 'My medicines', hello: 'Hello, {n}', today: 'Today', all: 'All my medicines', pharmacy: 'Show at the pharmacy',
      took: 'I took it', reported: 'Reported', reportedAt: 'Reported at {t}', saving: 'Saving…', notYet: 'Not reported yet',
      asNeeded: 'Only when needed', ask: 'Please ask your doctor or nurse', back: 'Back',
      none: 'No medicines yet. Your doctor will send your prescription to this phone.',
      noneToday: 'Nothing is planned for today.', allDone: 'Everything for today is reported.',
      issued: 'Prescribed by {d} on {date}', note: "Doctor's note", readAloud: 'Read aloud', stopRead: 'Stop reading',
      close: 'Close', showTitle: 'Show this screen to the pharmacist',
      foot: 'Sample patient. This page shows what your doctor prescribed. It does not diagnose or change your medicines.',
      retry: 'Try again', errLoad: 'Could not load your medicines. Please check your internet and try again.',
      errOpen: 'Please open this page from your SpiroBuddy app.', openApp: 'Open SpiroBuddy',
      errReport: 'Could not save. Please try again.',
      morning: 'Morning', afternoon: 'Afternoon', night: 'Night', bedtime: 'At bedtime',
      before: 'before food', after: 'after food', with: 'with food',
      forDays: 'for {n} days', untilStop: 'until your doctor says stop', unclearWhen: 'As your doctor wrote: {w}',
      fake: 'Sample patient', fPhone: 'Prescription on this phone', fPharmacy: 'Pharmacy screen', fQr: 'Pharmacist check',
      status: 'Status of these features',
    },
    hi: {
      title: 'मेरी दवाइयाँ', hello: 'नमस्ते, {n} जी', today: 'आज', all: 'मेरी सभी दवाइयाँ', pharmacy: 'दवा की दुकान पर दिखाएँ',
      took: 'मैंने ले ली', reported: 'बता दिया', reportedAt: '{t} पर बताया', saving: 'सहेज रहे हैं…', notYet: 'अभी बताया नहीं',
      asNeeded: 'ज़रूरत पड़ने पर ही', ask: 'कृपया अपने डॉक्टर या नर्स से पूछें', back: 'पीछे',
      none: 'अभी कोई दवा नहीं है। आपके डॉक्टर पर्ची इसी फ़ोन पर भेजेंगे।',
      noneToday: 'आज के लिए कोई दवा तय नहीं है।', allDone: 'आज की सब दवाइयाँ बता दी गईं।',
      issued: '{d} ने {date} को लिखी', note: 'डॉक्टर का नोट', readAloud: 'सुनें', stopRead: 'सुनना बंद करें',
      close: 'बंद करें', showTitle: 'यह स्क्रीन दवा की दुकान पर दिखाइए',
      foot: 'नमूना मरीज़। यह पन्ना वही दिखाता है जो आपके डॉक्टर ने लिखा है। यह कोई निदान नहीं करता और आपकी दवाएँ नहीं बदलता।',
      retry: 'फिर कोशिश करें', errLoad: 'दवाइयाँ नहीं खुलीं। कृपया इंटरनेट देखें और फिर कोशिश करें।',
      errOpen: 'कृपया यह पन्ना अपने SpiroBuddy ऐप से खोलें।', openApp: 'SpiroBuddy खोलें',
      errReport: 'सहेज नहीं पाए। कृपया फिर कोशिश करें।',
      morning: 'सुबह', afternoon: 'दोपहर', night: 'रात', bedtime: 'सोने से पहले',
      before: 'खाने से पहले', after: 'खाने के बाद', with: 'खाने के साथ',
      forDays: '{n} दिन तक', untilStop: 'जब तक डॉक्टर रुकने को न कहें', unclearWhen: 'डॉक्टर ने लिखा: {w}',
      fake: 'नमूना मरीज़', fPhone: 'फ़ोन पर पर्ची', fPharmacy: 'दवा की दुकान की स्क्रीन', fQr: 'दुकानदार की जाँच',
      status: 'इन सुविधाओं की स्थिति',
    },
    ta: {
      title: 'என் மருந்துகள்', hello: 'வணக்கம், {n}', today: 'இன்று', all: 'என் எல்லா மருந்துகளும்', pharmacy: 'மருந்தகத்தில் காட்டு',
      took: 'நான் எடுத்துக்கொண்டேன்', reported: 'தெரிவிக்கப்பட்டது', reportedAt: '{t} மணிக்கு தெரிவிக்கப்பட்டது', saving: 'சேமிக்கிறது…', notYet: 'இன்னும் தெரிவிக்கவில்லை',
      asNeeded: 'தேவைப்படும்போது மட்டும்', ask: 'உங்கள் மருத்துவர் அல்லது செவிலியரிடம் கேளுங்கள்', back: 'பின்',
      none: 'இன்னும் மருந்துகள் இல்லை. உங்கள் மருத்துவர் மருந்துச் சீட்டை இந்த ஃபோனுக்கு அனுப்புவார்.',
      noneToday: 'இன்றைக்கு மருந்துகள் எதுவும் இல்லை.', allDone: 'இன்றைய எல்லா மருந்துகளும் தெரிவிக்கப்பட்டன.',
      issued: '{d} அவர்கள் {date} அன்று எழுதியது', note: 'மருத்துவரின் குறிப்பு', readAloud: 'படித்துக் காட்டு', stopRead: 'நிறுத்து',
      close: 'மூடு', showTitle: 'இந்தத் திரையை மருந்தகத்தில் காட்டுங்கள்',
      foot: 'மாதிரி நோயாளி. உங்கள் மருத்துவர் எழுதியதை இந்தப் பக்கம் காட்டுகிறது. இது நோயறிதல் செய்யாது; உங்கள் மருந்துகளை மாற்றாது.',
      retry: 'மீண்டும் முயற்சி', errLoad: 'மருந்துகளை ஏற்ற முடியவில்லை. இணையத்தைச் சரிபார்த்து மீண்டும் முயலுங்கள்.',
      errOpen: 'இந்தப் பக்கத்தை உங்கள் SpiroBuddy செயலியிலிருந்து திறக்கவும்.', openApp: 'SpiroBuddy திற',
      errReport: 'சேமிக்க முடியவில்லை. மீண்டும் முயலுங்கள்.',
      morning: 'காலை', afternoon: 'மதியம்', night: 'இரவு', bedtime: 'தூங்கும் முன்',
      before: 'உணவுக்கு முன்', after: 'உணவுக்குப் பின்', with: 'உணவுடன்',
      forDays: '{n} நாட்களுக்கு', untilStop: 'மருத்துவர் நிறுத்தச் சொல்லும் வரை', unclearWhen: 'மருத்துவர் எழுதியது: {w}',
      fake: 'மாதிரி நோயாளி', fPhone: 'ஃபோனில் மருந்துச் சீட்டு', fPharmacy: 'மருந்தகத் திரை', fQr: 'மருந்தாளர் சரிபார்ப்பு',
      status: 'இந்த வசதிகளின் நிலை',
    },
    ml: {
      title: 'എന്റെ മരുന്നുകൾ', hello: 'നമസ്കാരം, {n}', today: 'ഇന്ന്', all: 'എന്റെ എല്ലാ മരുന്നുകളും', pharmacy: 'ഫാർമസിയിൽ കാണിക്കുക',
      took: 'ഞാൻ കഴിച്ചു', reported: 'അറിയിച്ചു', reportedAt: '{t} ന് അറിയിച്ചു', saving: 'സേവ് ചെയ്യുന്നു…', notYet: 'ഇതുവരെ അറിയിച്ചിട്ടില്ല',
      asNeeded: 'ആവശ്യമുള്ളപ്പോൾ മാത്രം', ask: 'നിങ്ങളുടെ ഡോക്ടറോടോ നഴ്സിനോടോ ചോദിക്കുക', back: 'തിരികെ',
      none: 'ഇതുവരെ മരുന്നുകളില്ല. നിങ്ങളുടെ ഡോക്ടർ കുറിപ്പടി ഈ ഫോണിലേക്ക് അയയ്ക്കും.',
      noneToday: 'ഇന്നത്തേക്ക് മരുന്നുകളൊന്നുമില്ല.', allDone: 'ഇന്നത്തെ എല്ലാ മരുന്നുകളും അറിയിച്ചു.',
      issued: '{d} {date} ന് എഴുതിയത്', note: 'ഡോക്ടറുടെ കുറിപ്പ്', readAloud: 'വായിച്ചു കേൾപ്പിക്കുക', stopRead: 'നിർത്തുക',
      close: 'അടയ്ക്കുക', showTitle: 'ഈ സ്ക്രീൻ ഫാർമസിയിൽ കാണിക്കുക',
      foot: 'സാമ്പിൾ രോഗി. നിങ്ങളുടെ ഡോക്ടർ എഴുതിയത് ഈ പേജ് കാണിക്കുന്നു. ഇത് രോഗനിർണയം നടത്തുന്നില്ല, നിങ്ങളുടെ മരുന്നുകൾ മാറ്റുന്നുമില്ല.',
      retry: 'വീണ്ടും ശ്രമിക്കുക', errLoad: 'മരുന്നുകൾ തുറക്കാനായില്ല. ഇന്റർനെറ്റ് പരിശോധിച്ച് വീണ്ടും ശ്രമിക്കുക.',
      errOpen: 'ഈ പേജ് നിങ്ങളുടെ SpiroBuddy ആപ്പിൽ നിന്ന് തുറക്കുക.', openApp: 'SpiroBuddy തുറക്കുക',
      errReport: 'സേവ് ചെയ്യാനായില്ല. വീണ്ടും ശ്രമിക്കുക.',
      morning: 'രാവിലെ', afternoon: 'ഉച്ചയ്ക്ക്', night: 'രാത്രി', bedtime: 'ഉറങ്ങുന്നതിനു മുമ്പ്',
      before: 'ഭക്ഷണത്തിന് മുമ്പ്', after: 'ഭക്ഷണത്തിനു ശേഷം', with: 'ഭക്ഷണത്തോടൊപ്പം',
      forDays: '{n} ദിവസത്തേക്ക്', untilStop: 'ഡോക്ടർ നിർത്താൻ പറയുന്നതുവരെ', unclearWhen: 'ഡോക്ടർ എഴുതിയത്: {w}',
      fake: 'സാമ്പിൾ രോഗി', fPhone: 'ഫോണിൽ കുറിപ്പടി', fPharmacy: 'ഫാർമസി സ്ക്രീൻ', fQr: 'ഫാർമസിസ്റ്റ് പരിശോധന',
      status: 'ഈ സൗകര്യങ്ങളുടെ നില',
    },
  };

  /* unit words: [singular, plural] per language; an unknown unit is shown as the doctor wrote it */
  const UNITS = {
    tablet: { en: ['tablet', 'tablets'], hi: ['गोली', 'गोली'], ta: ['மாத்திரை', 'மாத்திரைகள்'], ml: ['ഗുളിക', 'ഗുളികകൾ'] },
    capsule: { en: ['capsule', 'capsules'], hi: ['कैप्सूल', 'कैप्सूल'], ta: ['காப்ஸ்யூல்', 'காப்ஸ்யூல்கள்'], ml: ['ക്യാപ്സ്യൂൾ', 'ക്യാപ്സ്യൂളുകൾ'] },
    ml: { en: ['ml', 'ml'], hi: ['मि.ली.', 'मि.ली.'], ta: ['மி.லி.', 'மி.லி.'], ml: ['മി.ലി.', 'മി.ലി.'] },
    drop: { en: ['drop', 'drops'], hi: ['बूँद', 'बूँदें'], ta: ['சொட்டு', 'சொட்டுகள்'], ml: ['തുള്ളി', 'തുള്ളികൾ'] },
    puff: { en: ['puff', 'puffs'], hi: ['पफ़', 'पफ़'], ta: ['பஃப்', 'பஃப்'], ml: ['പഫ്', 'പഫ്'] },
    sachet: { en: ['sachet', 'sachets'], hi: ['पैकेट', 'पैकेट'], ta: ['பொட்டலம்', 'பொட்டலங்கள்'], ml: ['സാഷെ', 'സാഷെ'] },
  };
  const UNIT_ALIAS = { tab: 'tablet', tabs: 'tablet', cap: 'capsule', caps: 'capsule' };

  function tr(lang, key, vars) {
    const s = (T[lang] && T[lang][key]) || T.en[key] || key;
    return String(s).replace(/\{(\w+)\}/g, (_, k) => (vars && vars[k] != null ? vars[k] : ''));
  }

  function qtyText(q) {
    const n = Number(q);
    if (!isFinite(n)) return '';
    const whole = Math.floor(n), frac = Math.round((n - whole) * 100) / 100;
    const sym = { 0.5: '½', 0.25: '¼', 0.75: '¾' }[frac];
    if (frac === 0) return String(whole);
    if (sym) return (whole ? String(whole) : '') + sym;
    return String(Math.round(n * 100) / 100);
  }

  function unitKey(raw) {
    const r = String(raw || '').trim().toLowerCase();
    if (UNITS[r]) return r;
    if (UNIT_ALIAS[r]) return UNIT_ALIAS[r];
    return UNITS[r.replace(/s$/, '')] ? r.replace(/s$/, '') : '';
  }
  function unitWord(unit, qty, lang) {
    const k = unitKey(unit);
    return k ? UNITS[k][lang || 'en'][Number(qty) > 1 ? 1 : 0] : String(unit || '').trim();
  }

  /* "1 tablet", "½ गोली", "5 ml" */
  function doseText(line, lang) {
    const unit = line.dose_unit || (unitKey(line.form) ? unitKey(line.form) : '');
    return (qtyText(line.dose_qty) + ' ' + unitWord(unit, line.dose_qty, lang)).trim();
  }

  function clock(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return '';
    return d.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: 'numeric', minute: '2-digit', hour12: true }).toUpperCase();
  }
  function hhmm(t) {
    const m = /^(\d{1,2}):(\d{2})$/.exec(String(t || ''));
    if (!m) return String(t || '');
    const h = Number(m[1]);
    return (h % 12 || 12) + ':' + m[2] + ' ' + (h < 12 ? 'AM' : 'PM');
  }
  function dateText(iso, lang) {
    const d = new Date(String(iso).length <= 10 ? iso + 'T12:00:00+05:30' : iso);
    if (isNaN(d)) return '';
    const loc = { hi: 'hi-IN', ta: 'ta-IN', ml: 'ml-IN', en: 'en-IN' }[lang] || 'en-IN';
    return d.toLocaleDateString(loc, { timeZone: 'Asia/Kolkata', day: 'numeric', month: 'long', year: 'numeric' });
  }

  const SLOT_ICON = { morning: 'sun', afternoon: 'sun', night: 'moon', bedtime: 'moon' };

  /* when to take it: [{icon, text}] */
  function whenParts(line, lang) {
    if (line.as_needed) return [{ icon: 'clock', text: tr(lang, 'asNeeded') }];
    if (line.slots && line.slots.length) return line.slots.map((s) => ({ icon: SLOT_ICON[s] || 'clock', text: tr(lang, s) }));
    if (line.times && line.times.length) return line.times.map((t) => ({ icon: 'clock', text: hhmm(t) }));
    if (line.frequency_raw) return [{ icon: 'info', text: tr(lang, 'unclearWhen', { w: line.frequency_raw }) }];
    return [];
  }
  const foodText = (line, lang) => ({ before_food: 'before', after_food: 'after', with_food: 'with' }[line.food_timing] ? tr(lang, { before_food: 'before', after_food: 'after', with_food: 'with' }[line.food_timing]) : '');
  function durationText(line, lang) {
    if (line.as_needed && !line.duration_days && !line.until_stopped) return '';
    if (line.until_stopped) return tr(lang, 'untilStop');
    return line.duration_days ? tr(lang, 'forDays', { n: line.duration_days }) : '';
  }

  /* one medicine as a card (the "All my medicines" list, the doctor's preview) */
  function medCard(line, lang, opts) {
    opts = opts || {};
    const when = whenParts(line, lang).map((w) => `<li>${ic(w.icon, { size: 26 })}<span>${esc(w.text)}</span></li>`).join('');
    const food = foodText(line, lang), dur = durationText(line, lang);
    return `<article class="m-med${line.as_needed ? ' as-needed' : ''}">
      <h3 class="m-med-name">${ic('pill', { size: 28 })}<span>${esc(line.drug_name)}${line.strength ? ` <span class="m-med-str">${esc(line.strength)}</span>` : ''}</span></h3>
      <p class="m-med-dose">${esc(doseText(line, lang))}</p>
      ${when ? `<ul class="m-med-when">${when}</ul>` : ''}
      ${food ? `<p class="m-med-line">${esc(food)}</p>` : ''}
      ${dur ? `<p class="m-med-line">${esc(dur)}</p>` : ''}
      ${line.instructions ? `<p class="m-med-note"><b>${esc(tr(lang, 'note'))}:</b> ${esc(line.instructions)}</p>` : ''}
      ${line.as_needed ? `<p class="m-med-ask">${ic('info', { size: 22 })}<span>${esc(tr(lang, 'ask'))}</span></p>` : ''}
      ${opts.extra || ''}</article>`;
  }

  /* the same line as one spoken sentence (for "Read aloud") */
  function speakText(line, lang) {
    const parts = [line.drug_name + (line.strength ? ' ' + line.strength : ''), doseText(line, lang)];
    whenParts(line, lang).forEach((w) => parts.push(w.text));
    [foodText(line, lang), durationText(line, lang)].forEach((x) => { if (x) parts.push(x); });
    return parts.join('. ') + '.';
  }

  /* English summary for staff screens and the pharmacist: "1 tablet · morning and night · after food · 5 days" */
  function summary(line) {
    if (line.summary) return line.summary;
    const p = [doseText(line, 'en')];
    if (line.as_needed) p.push('only when needed');
    else if (line.slots && line.slots.length) p.push(line.slots.map((s) => tr('en', s).toLowerCase()).join(' and '));
    else if (line.times && line.times.length) p.push('at ' + line.times.join(', '));
    else if (line.frequency_raw) p.push('as written: ' + line.frequency_raw);
    const f = foodText(line, 'en'); if (f) p.push(f);
    const d = durationText(line, 'en'); if (d) p.push(d.replace('your doctor says stop', 'the doctor says stop'));
    return p.filter(Boolean).join(' · ');
  }

  SB.meds = { LANGS, NATIVE, SPEECH, T, tr, esc, qtyText, doseText, unitWord, clock, hhmm, dateText, whenParts, foodText, durationText, medCard, speakText, summary };
})();
