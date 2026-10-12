(() => {
  const SB=window.SB,$=s=>document.querySelector(s),esc=SB.ui.esc;
  const pid=Number(new URLSearchParams(location.search).get('id')); if(!pid)return;
  async function start(){
    const me=await SB.auth.me();if(!me.authenticated || me.kind!=='staff')return;
    const host=document.createElement('section');host.className='card';host.id='consultation-card';
    $('#profile-card').after(host);
    host.innerHTML=`<h2>Consultation &amp; staff notes</h2><p>Notes written by the care team. Only doctors record consultations.</p>${me.role==='doctor'?'<form id="consultation-form"><label for="consultation-text">Consultation note</label><textarea id="consultation-text" required maxlength="6000" rows="5" style="width:100%"></textarea><button class="btn primary" type="submit">Save consultation note</button></form>':''}<p id="note-error" role="alert" hidden></p><div id="note-list"></div>`;
    const careLink=document.createElement('a');careLink.className='btn';careLink.href=`discharge-editor.html?id=${encodeURIComponent(pid)}`;careLink.textContent=me.role==='doctor'?'Discharge care document':'View discharge care document';host.querySelector('h2').after(careLink);
    async function load(){try{const rows=await SB.api.get(`/api/patients/${pid}/notes`);$('#note-list').innerHTML=rows.length?rows.map(r=>`<article style="padding:12px 0;border-bottom:1px solid var(--border)"><strong>${esc(r.kind)}</strong><p style="white-space:pre-wrap">${esc(r.text)}</p><small>${esc(new Date(r.created_at).toLocaleString('en-IN'))} · Staff #${r.author_id}</small></article>`).join(''):'<p>No notes recorded yet.</p>';}catch(e){$('#note-error').hidden=false;$('#note-error').textContent=e.message;}}
    const form=$('#consultation-form');if(form)form.onsubmit=async e=>{e.preventDefault();const b=form.querySelector('button');b.disabled=true;try{await SB.api.post(`/api/patients/${pid}/notes`,{kind:'consultation',text:$('#consultation-text').value});$('#consultation-text').value='';await load();}catch(e){$('#note-error').hidden=false;$('#note-error').textContent=e.message;}finally{b.disabled=false;}};
    await load();
  }
  document.addEventListener('DOMContentLoaded',()=>start().catch(()=>{}));
})();
