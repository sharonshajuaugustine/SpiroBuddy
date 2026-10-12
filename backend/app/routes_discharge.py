"""Protected discharge APIs. No admission/bed transitions or prescribing."""
from fastapi import APIRouter, Body, HTTPException, Response
from . import authz, audit, service
from .discharge_docs import service as docs

router=APIRouter(tags=['discharge'])

def staff(pid,write=False):
    a=authz.require_staff('doctor') if write else authz.require_staff('doctor','nurse','admin')
    action='rx.create' if write else 'patient.view'
    if not authz.can(a,action,pid):
        if pid not in authz.visible_patient_ids(a): raise HTTPException(404,'Patient not found')
        raise HTTPException(403,'You do not have permission for this document')
    return a

def envelope(pid,a,state,history=False):
    p=service.get_patient_row(pid)
    hospitals=service.store().select('hospitals',[('id','eq',a.hospital_id)],columns='id,name',limit=1)
    return {'patient':{'id':pid,'name':p['name'],'mrn':p.get('mrn'),'breathing_enabled':(p.get('routine') or {}).get('breathing_enabled',True)},
        'hospital':hospitals[0] if hospitals else {'id':a.hospital_id,'name':'Hospital'},
        'revision':state['revision'],'can_edit':a.kind=='staff' and a.role=='doctor','document':docs.current(state),**({'versions':state['versions']} if history else {})}

@router.get('/api/patients/{pid}/discharge')
def staff_read(pid:int,response:Response):
    a=staff(pid); response.headers['Cache-Control']='no-store'
    return envelope(pid,a,docs.read(a.hospital_id,pid),a.role=='doctor')

@router.get('/api/patients/{pid}/discharge/versions/{version}')
def version_read(pid:int,version:int,response:Response):
    a=staff(pid); state=docs.read(a.hospital_id,pid)
    v=next((v for v in state['versions'] if v['version']==version),None)
    if not v or (v['status']=='draft' and a.role!='doctor'): raise HTTPException(404,'Document not found')
    response.headers['Cache-Control']='no-store'
    result=envelope(pid,a,state);result['document']=v
    return result

def change(pid,a,action,body,version=None):
    state,v=docs.transition(a.hospital_id,pid,a,action,body,version)
    audit.write('discharge.'+action,'discharge_document',f'{pid}:{v["version"]}',patient_id=pid,actor=a,
        detail={'version':v['version'],'status':v['status'],'revision':state['revision'],'replaces_version':v.get('replaces_version')})
    return envelope(pid,a,state,True)

@router.post('/api/patients/{pid}/discharge/drafts')
def create(pid:int,body:dict=Body(...)):
    return change(pid,staff(pid,True),'create',body)

@router.put('/api/patients/{pid}/discharge/versions/{version}')
def update(pid:int,version:int,body:dict=Body(...)):
    return change(pid,staff(pid,True),'update',body,version)

@router.post('/api/patients/{pid}/discharge/versions/{version}/publish')
def publish(pid:int,version:int,body:dict=Body(...)):
    return change(pid,staff(pid,True),'publish',body,version)

@router.post('/api/patients/{pid}/discharge/versions/{version}/withdraw')
def withdraw(pid:int,version:int,body:dict=Body(...)):
    return change(pid,staff(pid,True),'withdraw',body,version)

def patient():
    a=authz.current_actor()
    if not a: raise HTTPException(401,'Patient login needed')
    if a.kind!='patient' or not a.patient_id: raise HTTPException(403,'Use your patient login')
    authz.require('patient.view',a.patient_id)
    return a

@router.get('/api/me/discharge')
def me_read(response:Response):
    a=patient(); response.headers['Cache-Control']='no-store'
    return envelope(a.patient_id,a,docs.read(a.hospital_id,a.patient_id))

@router.post('/api/me/discharge/acknowledge')
def acknowledge(body:dict=Body(...)):
    a=patient();pid=a.patient_id
    version=body.get('version')
    if isinstance(version,bool) or not isinstance(version,int): raise HTTPException(400,'Choose the current version')
    with docs.LOCK:
        state=docs.read(a.hospital_id,pid);v=docs.current(state)
        if not v or v['version']!=version: raise HTTPException(409,'The current document changed. Reload your care page.')
        if v['acknowledgement']: return envelope(pid,a,state)
        state,v=docs.transition(a.hospital_id,pid,a,'ack',{'revision':state['revision']},version)
        audit.write('discharge.ack','discharge_document',f'{pid}:{version}',patient_id=pid,actor=a,detail={'version':version})
    return envelope(pid,a,state)
