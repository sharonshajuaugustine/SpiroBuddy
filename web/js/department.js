/* Admin operational prototype. Direct API reads deliberately have no fake-data fallback. */
(() => {'use strict';
const $=s=>document.querySelector(s), esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let state=null,busy=false,filter='';
async function api(path,body){const r=await fetch(path,{credentials:'same-origin',cache:'no-store',method:body?'POST':'GET',headers:body?{'Content-Type':'application/json','X-SB':'1'}:{},body:body?JSON.stringify(body):undefined});const d=await r.json();if(!r.ok){if(r.status===401)location.assign('login.html?next=%2Fdepartment.html');throw new Error(typeof d.detail==='string'?d.detail:'Request failed');}return d;}
function message(t,bad=false){$('#message').textContent=t;$('#message').className=bad?'error':'';}
function render(){
 $('#identity').textContent=state.hospital.name+' · '+state.actor.name+' · Admin-operated workspace';
 const options=Object.keys(state.departments).map(d=>`<option value="${esc(d)}">${esc(d)}</option>`).join('');
 const departmentSelect=$('#create-bed [name=department]'),wardSelect=$('#create-bed [name=ward]');
 const selectedDepartment=departmentSelect.value,selectedWard=wardSelect.value;
 $('#create-bed [name=department]').innerHTML=options;$('#create-bed [name=ward]').innerHTML=state.wards.map(w=>`<option value="${esc(w)}">${esc(w)}</option>`).join('');
 if(Object.hasOwn(state.departments,selectedDepartment))departmentSelect.value=selectedDepartment;
 if(state.wards.includes(selectedWard))wardSelect.value=selectedWard;
 $('#department-filter').innerHTML='<option value="">All departments</option>'+options;$('#department-filter').value=filter;
 const patients=new Map(state.patients.map(p=>[p.id,p]));
 $('#board').innerHTML=state.beds.filter(b=>!filter||b.department===filter).map(b=>{
 const p=patients.get(b.patient_id);const candidates=state.patients.filter(x=>!x.admission||x.admission.id!==b.id);
 const select=`<label>Patient<select data-patient="${esc(b.id)}"><option value="">Choose a patient</option>${candidates.map(x=>`<option value="${x.id}">${esc(x.name)} · ${esc(x.mrn||'No hospital number')}${x.admission?' · Transfer':''}</option>`).join('')}</select></label>`;
 const action=(a,t)=>`<button type="button" data-bed="${esc(b.id)}" data-action="${a}">${t}</button>`;
 return `<article class="bed ${b.status}"><h3>${esc(b.ward)} · ${esc(b.label)}</h3><p>${esc(b.department)} · ${esc(b.status)}</p>${p?`<p><a href="patient.html?id=${p.id}">${esc(p.name)}</a> · ${esc(p.doctor)}</p>`:''}${b.status==='available'?select+action('allocate','Admit / transfer here')+action('clean','Mark cleaning'):b.status==='cleaning'?action('ready','Mark ready'):action('discharge','Discharge from bed')}</article>`;
 }).join('')||'<p>No beds configured for this view.</p>';
 $('#patients').innerHTML='<table><thead><tr><th>Patient / hospital number</th><th>Doctor</th><th>Admission</th><th>Record</th></tr></thead><tbody>'+state.patients.map(p=>`<tr><td>${esc(p.name)}<small>${esc(p.mrn||'Not recorded')}</small></td><td>${esc(p.doctor)}</td><td>${p.admission?esc(p.admission.department+' · '+p.admission.ward+' · '+p.admission.label):'Not admitted on this board'}${!p.admission&&(p.ward||p.bed)?'<small>Chart label: '+esc([p.ward,p.bed].filter(Boolean).join(' · '))+'</small>':''}</td><td><a href="patient.html?id=${p.id}">Chart</a><small><a href="prescribe.html?id=${p.id}">Prescription workspace</a> · doctor login required</small></td></tr>`).join('')+'</tbody></table>';
 $('#history').innerHTML=state.history.length?'<ol>'+state.history.slice().reverse().slice(0,100).map(e=>`<li>${esc(e.action)} · ${esc(e.department)} · ${esc(e.ward)} ${esc(e.label)}${e.patient_id?' · Patient '+esc(e.patient_id):''}<small>${esc(e.actor_name)} · ${esc(e.at)}</small></li>`).join('')+'</ol>':'No operations recorded.';
 document.querySelectorAll('button').forEach(b=>b.disabled=busy);
}
async function load(){state=await api('/api/department-ops');render();}
async function change(path,body){if(busy)return;busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);try{state=await api(path,{...body,version:state.version});message('Operation recorded.');render();}catch(e){message(e.message,true);try{await load();}catch(_){} }finally{busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);}}
$('#create-bed').addEventListener('submit',e=>{e.preventDefault();if(!state)return;const f=new FormData(e.target);change('/api/department-ops/beds',{department:f.get('department'),ward:f.get('ward'),label:f.get('label')});});
$('#department-filter').onchange=e=>{filter=e.target.value;if(state)render();};$('#refresh').onclick=()=>load().then(()=>message('Board refreshed.')).catch(e=>message(e.message,true));
$('#board').onclick=e=>{const b=e.target.closest('[data-action]');if(!b||!state||busy)return;let action=b.dataset.action,body={};if(action==='allocate'){const value=$(`[data-patient="${b.dataset.bed}"]`).value;if(!value){message('Choose a patient.',true);return;}body.patient_id=Number(value);const p=state.patients.find(p=>p.id===body.patient_id);action=p.admission?'transfer':'admit';}if(action==='discharge'&&!confirm('Record discharge from this bed? This does not change medicines or publish a discharge summary.'))return;change('/api/department-ops/beds/'+encodeURIComponent(b.dataset.bed)+'/'+action,body);};
load().catch(e=>message(e.message,true));
})();
