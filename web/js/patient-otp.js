/* OTP flow never puts the code or challenge in URL/storage. Only a demo code is displayed. */
(() => {
  const $ = s => document.querySelector(s);
  let challenge = null, loginIdentity = null, sample = null, sending = false, hospitalsReady = false;
  let resendAt = 0, cooldownTimer = null;
  const currentCode = document.createElement('button');
  currentCode.type = 'button'; currentCode.hidden = true; $('#otp-form').append(currentCode);
  const language = () => document.documentElement.lang === 'hi' ? 'hi' : 'en';
  function updateCooldown() {
    const hi = language() === 'hi', seconds = Math.max(0, Math.ceil((resendAt - Date.now()) / 1000));
    $('#request').disabled = !hospitalsReady || sending || seconds > 0;
    $('#again').disabled = sending || seconds > 0;
    $('#request').textContent = seconds ? (hi ? `फिर कोड भेजने के लिए ${seconds} सेकंड रुकें` : `Send another code in ${seconds}s`) : translations[language()][4];
    $('#again').textContent = seconds ? (hi ? `दूसरे कोड के लिए ${seconds} सेकंड रुकें` : `Another code available in ${seconds}s`) : (hi ? 'नंबर बदलें / दूसरा कोड माँगें' : 'Change number / request another code');
    currentCode.textContent = hi ? 'मौजूदा कोड डालें' : 'Use my current code';
    if (!seconds && cooldownTimer) {clearInterval(cooldownTimer); cooldownTimer = null;}
  }
  function startCooldown() {
    resendAt = Date.now() + 60000;
    if (cooldownTimer) clearInterval(cooldownTimer);
    cooldownTimer = setInterval(updateCooldown, 250); updateCooldown();
  }
  window.addEventListener('pagehide', () => {if (cooldownTimer) clearInterval(cooldownTimer); cooldownTimer = null;});
  window.addEventListener('pageshow', () => {if (resendAt > Date.now() && !cooldownTimer) cooldownTimer = setInterval(updateCooldown, 250); updateCooldown();});
  currentCode.onclick = () => {$('#otp-form').hidden = true; $('#verify-section').hidden = false; $('#code').focus();};
  const translations = {
    en: ['Patient login','Use your hospital number. Your code goes to the phone number registered at the hospital.','Hospital','Hospital registration number','Send my code','6-digit code','Open my medicines'],
    hi: ['मरीज़ लॉगिन','अस्पताल का पंजीकरण नंबर डालें। कोड अस्पताल में दर्ज फ़ोन नंबर पर भेजा जाता है।','अस्पताल','अस्पताल का पंजीकरण नंबर','मेरा कोड भेजें','6 अंकों का कोड','मेरी दवाइयाँ खोलें']
  };
  function showError(e) { $('#error').textContent = e.message; $('#error').hidden = false; }
  async function api(path, body) {
    const r = await fetch(path, {method: body ? 'POST' : 'GET', cache:'no-store', credentials:'same-origin',
      headers: {'Content-Type':'application/json','X-SB':'1'}, body:body ? JSON.stringify(body) : undefined});
    const d = await r.json(); if (!r.ok) throw new Error(d.error || 'Please try again.'); return d;
  }
  document.querySelectorAll('[data-lang]').forEach(b => b.onclick = () => {
    const lang = b.dataset.lang, t = translations[lang]; document.documentElement.lang = lang;
    ['h1','#intro','#hospital-label','#number-label','#request','#code-label','#verify'].forEach((s,i) => $(s).textContent = t[i]);
    try {localStorage.setItem('sb_meds_lang',lang);} catch (_) {}
    updateCooldown();
  });
  $('#otp-form').onsubmit = async e => {
    e.preventDefault(); if (sending || Date.now() < resendAt) return; sending = true; $('#error').hidden = true; updateCooldown();
    try {
      const requestedIdentity = {hospital_id:Number($('#hospital').value),registration_no:$('#number').value.trim()};
      const d = await api('/api/me/otp/request',requestedIdentity); challenge = d.challenge_id; loginIdentity = requestedIdentity;
      currentCode.hidden = false; startCooldown();
      $('#request-message').textContent = d.message; $('#sample-phone').hidden = !d.demo_code;
      $('#sample-code').textContent = d.demo_code || ''; $('#otp-form').hidden = true; $('#verify-section').hidden = false; $('#code').value = ''; $('#code').focus();
    } catch(e) { showError(e); } finally {sending = false; updateCooldown();}
  };
  $('#verify-form').onsubmit = async e => {
    e.preventDefault(); if (sending) return; sending = true; $('#verify').disabled = true; $('#error').hidden = true;
    try { await api('/api/me/otp/verify',{...loginIdentity,challenge_id:challenge,code:$('#code').value.trim()}); location.assign('/meds.html'); }
    catch(e) {showError(e); $('#code').value = ''; $('#code').focus(); sending = false; $('#verify').disabled = false;}
  };
  $('#again').onclick = () => {if (sending || Date.now() < resendAt) return; $('#verify-section').hidden = true; $('#otp-form').hidden = false; $('#error').hidden = true; };
  $('#fill').onclick = () => {if(sample){$('#hospital').value=String(sample.hospital_id || 1);$('#number').value=sample.registration_no;}};
  (async () => {
    try {
      const hospitals = await api('/api/me/otp/hospitals');
      hospitals.forEach(h => {const o=document.createElement('option');o.value=h.id;o.textContent=h.name;$('#hospital').append(o);});
      hospitalsReady = hospitals.length > 0; updateCooldown();
      const preset = new URLSearchParams(location.search).get('hospital'); if(preset) $('#hospital').value=preset;
      const demo = await api('/api/me/login-demo'); if (demo.registration_no) {sample=demo;$('#sample').hidden=false;}
    } catch(e) {showError(e);$('#request').disabled=true;}
  })();
})();
