"""Discharge router in an isolated app, authenticated with real seeded sessions."""
import concurrent.futures
import importlib
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app import authz, service
from backend.app.routes_discharge import router
from backend.app.discharge_docs import service as docs

CONTENT={'condition_summary':'Artificial follow-up condition','home_care':'Sample clinician instructions only.',
         'follow_up':'Contact the sample care team as documented.','language':'en'}

@pytest.fixture
def module(fresh,login_as,patient_client):
    service.store().delete('app_settings',[('key','eq','discharge:v1:1:1')])
    app=FastAPI();app.include_router(router)
    @app.middleware('http')
    async def context(request,call_next):
        staff,patient=authz.resolve_actors(request)
        actor,alt=(patient,None) if request.url.path.startswith('/api/me/') else (staff or patient,patient if staff else None)
        tokens=authz.set_actor(actor,alt)
        try:return await call_next(request)
        finally:authz.reset_actor(tokens)
    def clone(source):
        c=TestClient(app,headers={'X-SB':'1'});c.cookies.clear();c.cookies.update(source.cookies);return c
    anonymous=TestClient(app,headers={'X-SB':'1'});anonymous.cookies.clear()
    return {'doctor':clone(login_as('meera.nair@demo-general.example')),
        'patient':clone(patient_client(1)),'other':clone(patient_client(2)),
        'admin':clone(login_as('admin@demo-general.example')),
        'nurse':clone(login_as('anjali@demo-general.example')),
        'foreign':clone(login_as('admin@demo-riverside.example')),'anonymous':anonymous}

BASE='/api/patients/1/discharge'
def create(c,revision=0,content=CONTENT):
    r=c.post(BASE+'/drafts',json={'revision':revision,'content':content});assert r.status_code==200,r.text;return r.json()
def publish(c,version=1,revision=1):
    r=c.post(BASE+f'/versions/{version}/publish',json={'revision':revision,'confirm':True});assert r.status_code==200,r.text;return r.json()

def test_draft_publish_scope_roles(module):
    d=module['doctor'];create(d)
    assert module['patient'].get('/api/me/discharge').json()['document'] is None
    assert module['nurse'].get(BASE+'/versions/1').status_code==404
    assert module['nurse'].post(BASE+'/drafts',json={'revision':1}).status_code==403
    assert module['admin'].post(BASE+'/drafts',json={'revision':1}).status_code==403
    publish(d)
    assert module['patient'].get('/api/me/discharge').json()['document']['content']['home_care']==CONTENT['home_care']
    assert module['other'].get('/api/me/discharge?patient_id=1').json()['document'] is None
    assert module['other'].get(BASE).status_code==403  # staff route cannot serve a patient
    assert module['foreign'].get(BASE).status_code==404
    assert module['nurse'].get(BASE).json()['document']['version']==1
    assert module['anonymous'].get('/api/me/discharge').status_code==401
    assert module['anonymous'].get(BASE).status_code==401

def test_immutable_replace_ack_history(module):
    d,p=module['doctor'],module['patient'];create(d);publish(d)
    assert p.post('/api/me/discharge/acknowledge',json={'version':1}).status_code==200
    first=p.get('/api/me/discharge').json()
    second=p.post('/api/me/discharge/acknowledge',json={'version':1}).json()
    assert first==second
    rev=first['revision']
    assert d.put(BASE+'/versions/1',json={'revision':rev,'content':CONTENT}).status_code==409
    replacement=create(d,rev,{**CONTENT,'home_care':'Replacement instructions'})
    assert replacement['document']['version']==1
    publish(d,2,replacement['revision'])
    now=p.get('/api/me/discharge').json()
    assert now['document']['version']==2 and now['document']['acknowledgement'] is None
    assert p.post('/api/me/discharge/acknowledge',json={'version':1}).status_code==409
    history=d.get(BASE).json()['versions']
    assert history[0]['status']=='superseded' and history[0]['content']=={**CONTENT,'treatment_summary':'','warning_signs':'','exercise_instructions':'','follow_up_date':None,'discharge_date':None}
    assert history[0]['acknowledgement']['version']==1

def test_stale_failed_publish_withdraw_validation(module):
    d=module['doctor'];create(d);publish(d)
    state=create(d,2,{'language':'en'})
    assert d.post(BASE+'/versions/2/publish',json={'revision':state['revision'],'confirm':True}).status_code==400
    assert d.get(BASE).json()['document']['version']==1
    assert d.put(BASE+'/versions/2',json={'revision':2,'content':CONTENT}).status_code==409
    for content in ({**CONTENT,'discharge_date':'2026-02-30'},{**CONTENT,'home_care':'x'*4001}):
        assert d.put(BASE+'/versions/2',json={'revision':3,'content':content}).status_code==400
    assert d.post(BASE+'/versions/1/withdraw',json={'revision':3,'reason':''}).status_code==400
    r=d.post(BASE+'/versions/1/withdraw',json={'revision':3,'reason':'Sample correction required'})
    assert r.status_code==200
    assert module['patient'].get('/api/me/discharge').json()['document'] is None
    assert d.get(BASE+'/versions/1').json()['document']['withdrawal_reason']=='Sample correction required'
    assert d.post(BASE+'/versions/1/withdraw',json={'revision':4,'reason':'Again'}).status_code==409

def test_publication_confirmation_and_unknown_versions(module):
    d=module['doctor'];create(d)
    assert d.post(BASE+'/versions/1/publish',json={'revision':1}).status_code==400
    assert d.put(BASE+'/versions/99',json={'revision':1,'content':CONTENT}).status_code==404
    assert d.post(BASE+'/versions/1/withdraw',json={'revision':1,'reason':'Sample'}).status_code==409
    assert d.post(BASE+'/drafts',json={'revision':1}).status_code==409
    assert d.put(BASE+'/versions/1',json={'revision':1,'content':None}).status_code==400
    assert d.put(BASE+'/versions/1',json={'revision':1,'content':[]}).status_code==400
    assert d.post(BASE+'/versions/1/publish',json={'revision':True,'confirm':True}).status_code==409
    assert d.get(BASE).json()['versions'][0]['status']=='draft'

def test_plain_text_persistence_concurrent_publish(module):
    d=module['doctor'];html='<img src=x onerror=alert(1)>\nExact clinician text'
    create(d,content={**CONTENT,'home_care':html})
    importlib.reload(docs)
    assert docs.read(1,1)['versions'][0]['content']['home_care']==html
    actor=authz.Actor('staff',2,'doctor',1,'Sample doctor')
    def run():
        try:return docs.transition(1,1,actor,'publish',{'revision':1,'confirm':True},1)[0]['revision']
        except Exception as e:return getattr(e,'status_code',None)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda _:run(),range(2)))
    assert sorted(results)==[2,409]
    assert len([v for v in docs.read(1,1)['versions'] if v['status']=='published'])==1
    from pathlib import Path
    for path in ('web/js/my-care.js','web/js/discharge-print.js'):
        text=Path(path).read_text()
        assert '.textContent=' in text and 'innerHTML' not in text

def test_demo_reset_removes_discharge_aggregate(module,fresh):
    create(module['doctor']);publish(module['doctor'])
    assert docs.current(docs.read(1,1))
    assert fresh.post('/api/demo/reset').status_code==200
    assert docs.read(1,1)=={'revision':0,'versions':[]}
