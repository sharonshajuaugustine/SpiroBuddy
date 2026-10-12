"""Isolated operational bed workflow, role/hospital boundaries and allocation races."""
from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi import HTTPException
from backend.app import authz, service
from backend.app.department_ops import service as ops


@pytest.fixture(autouse=True)
def clean_operations(fresh):
    service.store().delete('app_settings', [('key', 'in', ['department_ops:1', 'department_ops:2'])])


def add(c, label='T-1'):
    s=c.get('/api/department-ops').json()
    r=c.post('/api/department-ops/beds', json={'version':s['version'], 'department':'General Surgery',
        'ward':'Surgical Ward A','label':label})
    assert r.status_code==200, r.text
    return r.json()


def change(c,s,bed,action,**body):
    return c.post(f'/api/department-ops/beds/{bed}/{action}',json={'version':s['version'],**body})


def test_admit_transfer_discharge_totals_and_history(fresh):
    s=add(fresh); s=add(fresh,'T-2'); a,b=[x['id'] for x in s['beds']]
    s=change(fresh,s,a,'admit',patient_id=1).json()
    assert s['counts']['current_admissions']==1 and s['counts']['admissions_today']==1
    assert s['counts']['available']==1
    p=service.get_patient_row(1); assert (p['ward'],p['bed'])==('Surgical Ward A','T-1')
    s=change(fresh,s,b,'transfer',patient_id=1).json()
    assert s['counts']['admissions_today']==1 and s['counts']['cleaning']==1
    assert service.get_patient_row(1)['bed']=='T-2'
    s=change(fresh,s,b,'discharge').json()
    assert s['counts']['discharges_today']==1 and s['counts']['current_admissions']==0
    assert s['counts']['cleaning']==2
    assert service.get_patient_row(1)['bed'] is None
    s=change(fresh,s,b,'ready').json()
    assert s['counts']['available']==1 and s['counts']['cleaning']==1
    assert s['departments']['General Surgery']['total_beds']==2
    assert [e['action'] for e in s['history']]==['create','create','admit','transfer','discharge','ready']
    assert all(e['actor_id']==1 and e['actor_name'] and e['at'] for e in s['history'])


def test_conflicts_and_transition_validation(fresh):
    s=add(fresh);s=add(fresh,'T-2');a,b=[x['id'] for x in s['beds']]
    assert change(fresh,s,a,'transfer',patient_id=1).status_code==409
    assert change(fresh,s,a,'ready').status_code==409
    old=s;s=change(fresh,s,a,'admit',patient_id=1).json()
    assert change(fresh,old,b,'admit',patient_id=2).status_code==409
    assert change(fresh,s,a,'admit',patient_id=2).status_code==409
    assert change(fresh,s,b,'admit',patient_id=1).status_code==409
    assert change(fresh,s,a,'clean').status_code==409
    assert change(fresh,s,'not-a-bed','admit',patient_id=2).status_code==404
    assert change(fresh,s,b,'admit',patient_id=999999).status_code==404
    for bad in [True,'1',0,None]:
        assert change(fresh,s,b,'admit',patient_id=bad).status_code==400
    assert change(fresh,s,b,'create').status_code==400
    for version in [True,-1,'1',None]:
        assert fresh.post(f'/api/department-ops/beds/{b}/clean',json={'version':version}).status_code==400
    assert fresh.post('/api/department-ops/beds',json={'version':s['version'],'department':'Foreign Department','ward':'Surgical Ward A','label':'T-3'}).status_code==400
    assert fresh.post('/api/department-ops/beds',json={'version':s['version'],'department':'General Surgery','ward':'Other hospital ward','label':'T-3'}).status_code==400
    assert fresh.post('/api/department-ops/beds',json={'version':s['version'],'department':'General Surgery','ward':'Surgical Ward A','label':'t-1'}).status_code==409


def test_role_and_hospital_boundaries(fresh,anon,login_as,patient_client,riverside_patient):
    s=add(fresh); bed=s['beds'][0]['id']
    for c,code in [(anon,401),(login_as('meera.nair@demo-general.example'),403),
                   (login_as('anjali@demo-general.example'),403),(patient_client(1),401)]:
        assert c.get('/api/department-ops').status_code==code
        assert c.post('/api/department-ops/beds',json={'version':0}).status_code==code
    other=login_as('admin@demo-riverside.example')
    assert other.get('/api/department-ops').json()['beds']==[]
    assert change(other,{'version':0},bed,'ready').status_code==404
    assert change(other,{'version':99},bed,'ready').status_code==404
    assert change(fresh,s,bed,'admit',patient_id=100).status_code==404
    # A hospital id in the body never changes the server-derived tenant.
    result=change(fresh,s,bed,'admit',patient_id=1,hospital_id=2)
    assert result.status_code==200 and result.json()['hospital']['id']==1


def test_allocation_race_is_serialized(fresh):
    s=add(fresh);bed=s['beds'][0]['id']
    actor=authz.Actor('staff',1,'admin',1,'Admin desk')
    def attempt(pid):
        try:
            ops.mutate(actor,'admit',{'version':s['version'],'patient_id':pid},bed)
            return 200
        except HTTPException as e:
            return e.status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(attempt,[1,2]))
    assert sorted(results)==[200,409]
    assert ops.snapshot(actor)['counts']['current_admissions']==1


def test_save_failure_restores_patient_labels(fresh,monkeypatch):
    s=add(fresh);before=service.get_patient_row(1)
    def fail(*args): raise RuntimeError('storage unavailable')
    monkeypatch.setattr(ops,'save',fail)
    actor=authz.Actor('staff',1,'admin',1,'Admin desk')
    with pytest.raises(RuntimeError):
        ops.mutate(actor,'admit',{'version':s['version'],'patient_id':1},s['beds'][0]['id'])
    after=service.get_patient_row(1)
    assert (after['ward'],after['bed'])==(before.get('ward'),before.get('bed'))
    assert ops.read(actor)['version']==s['version']


def test_demo_reset_removes_operational_assignments_only(fresh):
    s=add(fresh)
    s=change(fresh,s,s['beds'][0]['id'],'admit',patient_id=1).json()
    assert s['counts']['current_admissions']==1
    service.store().upsert('app_settings',[{'key':'department_reset_unrelated','hospital_id':1,
                                           'value':{'keep':True}}])
    assert fresh.post('/api/demo/reset').status_code==200
    s=fresh.get('/api/department-ops').json()
    assert s['beds']==[] and s['history']==[] and s['version']==0
    assert s['counts']['current_admissions']==0
    assert service.store().select('app_settings',[('key','eq','department_reset_unrelated')])[0]['value']=={'keep':True}
    service.store().delete('app_settings',[('key','eq','department_reset_unrelated')])
