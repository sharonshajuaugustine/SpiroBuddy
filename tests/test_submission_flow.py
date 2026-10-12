"""New patient, approved prescription, OTP and truthful exercise completion."""
from datetime import timedelta

import pytest

from backend.app import patient_otp as otp, ratelimit, service
from backend.app.config import now_local, iso


@pytest.fixture(autouse=True)
def clean_limits():
    ratelimit.reset("otp_request")
    ratelimit.reset("otp_verify")
    service.store().delete("app_settings", [("key", "eq", "otp:1:FLOW-123")])


def register(doctor):
    r = doctor.post('/api/patients', json={"registration_no":"FLOW-123","name":"Sample New Patient",
        "age":45,"sex":"F","language":"en","phone":"+910000000321","condition":"Sample follow-up"})
    assert r.status_code == 200, r.text
    return r.json()['patient']['id']


def test_registration_prescription_otp_and_scope(fresh, login_as, anon):
    doctor = login_as('meera.nair@demo-general.example')
    pid = register(doctor)
    assert doctor.post('/api/patients', json={"registration_no":"flow-123","name":"Other","age":20,
        "sex":"M"}).status_code == 409
    assert doctor.post(f'/api/patients/{pid}/notes',json={"kind":"consultation","text":"Sample consultation recorded."}).status_code == 200
    rx = doctor.post(f'/api/patients/{pid}/prescriptions',json={"lines":[{"drug_name":"Sample medicine",
        "strength":"sample strength","dose_qty":1,"dose_unit":"tablet","form":"tablet",
        "frequency_raw":"1-0-1","duration_days":3}]})
    assert rx.status_code == 200, rx.text
    identity = {"hospital_id":1,"registration_no":"FLOW-123"}
    challenge = anon.post('/api/me/otp/request',json=identity).json()
    assert challenge['delivery']=='simulated'
    stored = service.store().select('app_settings',[("key","eq","otp:1:FLOW-123")])[0]['value']
    assert stored['code_hash'] != challenge['demo_code'] and 'code' not in stored
    verified = anon.post('/api/me/otp/verify',json={**identity,"challenge_id":challenge['challenge_id'],"code":challenge['demo_code']})
    assert verified.status_code == 200, verified.text
    assert anon.get('/api/me/medicines').json()['has_prescription']
    assert anon.get('/api/patients/1').status_code == 404
    assert anon.post('/api/me/otp/verify',json={**identity,"challenge_id":challenge['challenge_id'],"code":challenge['demo_code']}).status_code == 401
    assert login_as('admin@demo-riverside.example').get(f'/api/patients/{pid}/notes').status_code==404


def test_otp_expiry_lock_and_hospital_scope(fresh, login_as, anon, monkeypatch):
    pid = register(login_as('meera.nair@demo-general.example'))
    identity={"hospital_id":1,"registration_no":"FLOW-123"}
    d=anon.post('/api/me/otp/request',json=identity).json()
    t=now_local()
    monkeypatch.setattr(otp,'now',lambda:t+timedelta(minutes=11))
    assert anon.post('/api/me/otp/verify',json={**identity,"challenge_id":d['challenge_id'],"code":d['demo_code']}).status_code==401
    monkeypatch.setattr(otp,'now',lambda:t+timedelta(minutes=12))
    d=anon.post('/api/me/otp/request',json=identity).json()
    bad='000000' if d['demo_code']!='000000' else '111111'
    for _ in range(5):
        r=anon.post('/api/me/otp/verify',json={**identity,"challenge_id":d['challenge_id'],"code":bad})
    assert r.status_code==429
    assert anon.post('/api/me/otp/verify',json={**identity,"challenge_id":d['challenge_id'],"code":d['demo_code']}).status_code==429
    wrong=anon.post('/api/me/otp/request',json={**identity,"hospital_id":2}).json()
    assert 'demo_code' not in wrong


def test_unknown_no_phone_and_non_demo_hide_codes(fresh, login_as, anon, monkeypatch):
    pid=register(login_as('meera.nair@demo-general.example'))
    service.store().update('patients',[("id","eq",pid)],{"phone":None})
    a=anon.post('/api/me/otp/request',json={"hospital_id":1,"registration_no":"FLOW-123"}).json()
    b=anon.post('/api/me/otp/request',json={"hospital_id":1,"registration_no":"UNKNOWN-123"}).json()
    assert a['message']==b['message'] and 'demo_code' not in a and 'demo_code' not in b
    service.store().update('patients',[("id","eq",pid)],{"phone":"+910000000321"})
    monkeypatch.setattr(otp,'demo_mode',lambda:False)
    assert 'demo_code' not in anon.post('/api/me/otp/request',json={"hospital_id":1,"registration_no":"FLOW-123"}).json()


def test_partial_empty_and_forged_scores(fresh, patient_client):
    c=patient_client(1)
    at=now_local()
    base={"patient_id":1,"started_at":iso(at),"source":"demo"}
    assert c.post('/api/sessions',json={**base,"breaths":[]}).status_code==400
    breath={"features":{"peak_ml":1800,"time_to_peak_s":4,"duration_s":9,"hold_s":3,"mean_rise_ml_s":450,"max_rise_ml_s":600},"label":"good","score":999}
    partial=c.post('/api/sessions',json={**base,"breaths":[breath]}).json()
    assert partial['slot_status']=='partial' and 0<=partial['avg_score']<=10
    full=c.post('/api/sessions',json={**base,"breaths":[breath]*10}).json()
    assert full['slot_status']=='done'


def test_registration_and_consultation_roles(fresh, login_as, patient_client):
    nurse=login_as('anjali@demo-general.example')
    assert nurse.post('/api/patients',json={}).status_code==403
    assert nurse.post('/api/patients/1/notes',json={"kind":"consultation","text":"x"}).status_code==403
    assert patient_client(1).post('/api/patients/1/notes',json={"text":"x"}).status_code in (401,403)


def test_manual_notepad_never_issues_a_prescription(fresh, login_as):
    doctor=login_as('meera.nair@demo-general.example')
    pid=register(doctor)
    r=doctor.post(f'/api/patients/{pid}/prescriptions/draft-text',json={"text":"Sample drug | 10 mg | tablet | 1 | tablet | BD | 3 | Sample instruction"})
    assert r.status_code==200, r.text
    assert r.json()['source']=='manual_format'
    assert r.json()['lines'][0]['dose_qty']==1
    assert service.store().select('prescriptions',[("patient_id","eq",pid)])==[]
    r=doctor.post(f'/api/patients/{pid}/prescriptions/draft-text',json={"text":"Unclear writing"}).json()
    assert not r['lines'][0].get('dose_qty')


def test_ai_notepad_review_and_draft_scope(fresh, login_as, monkeypatch):
    from backend.app import ai_gemini as ai
    doctor=login_as('meera.nair@demo-general.example')
    pid=register(doctor)
    monkeypatch.setattr(ai,'ai_allowed',lambda *a:(True,''))
    monkeypatch.setattr(ai,'_run',lambda *a:({"lines":[{"drug_name":"Sample drug","strength":"10 mg","form":"tablet","dose_qty":1,"dose_unit":"tablet","frequency_raw":"BD","duration_days":3,"food_timing":"after_food"}]},None,10))
    d=doctor.post(f'/api/patients/{pid}/prescriptions/draft-text',json={"text":"Sample drug"}).json()
    assert d['source']=='gemini' and d['ai_event_id']
    assert service.store().select('dose_events',[("patient_id","eq",pid)])==[]
    issued=doctor.post(f'/api/patients/{pid}/prescriptions',json={"lines":d['lines'],"draft_event_id":d['ai_event_id']})
    assert issued.status_code==200, issued.text
    event=service.store().select('ai_events',[("id","eq",d['ai_event_id'])])[0]
    assert event['reviewed_by']==2 and event['decision'] in ('approved','edited')
    assert doctor.post(f'/api/patients/{pid}/prescriptions',json={"lines":d['lines'],"draft_event_id":d['ai_event_id']}).status_code==409
    assert doctor.post('/api/patients/1/prescriptions',json={"lines":d['lines'],"draft_event_id":d['ai_event_id']}).status_code==404


def test_notepad_missing_review_fields_cannot_publish(fresh, login_as, monkeypatch):
    from backend.app import ai_gemini as ai
    doctor = login_as('meera.nair@demo-general.example')
    pid = register(doctor)
    monkeypatch.setattr(ai, 'ai_allowed', lambda *a: (True, ''))
    monkeypatch.setattr(ai, '_run', lambda *a: ({"lines": [{"drug_name": "Sample drug", "dose_qty": 1,
        "frequency_raw": "BD", "duration_days": 3}]}, None, 10))
    draft = doctor.post(f'/api/patients/{pid}/prescriptions/draft-text', json={"text": "Sample note"}).json()
    result = doctor.post(f'/api/patients/{pid}/prescriptions', json={"lines": draft['lines'],
        "draft_event_id": draft['ai_event_id']})
    assert result.status_code == 400
    assert service.store().select('prescriptions', [("patient_id", "eq", pid)]) == []


def test_phone_change_invalidates_otp_and_checks_scope(fresh, login_as, anon):
    doctor=login_as('meera.nair@demo-general.example')
    pid=register(doctor)
    identity={"hospital_id":1,"registration_no":"FLOW-123"}
    d=anon.post('/api/me/otp/request',json=identity).json()
    assert doctor.put(f'/api/patients/{pid}/phone',json={"phone":"+910000000322"}).status_code==200
    assert anon.post('/api/me/otp/verify',json={**identity,"challenge_id":d['challenge_id'],"code":d['demo_code']}).status_code==401
    assert login_as('admin@demo-riverside.example').put(f'/api/patients/{pid}/phone',json={"phone":""}).status_code==404


def test_breathing_is_optional_and_can_be_assigned(fresh, login_as, patient_client):
    doctor=login_as('meera.nair@demo-general.example')
    pid=register(doctor)
    c=patient_client(pid)
    assert c.get('/api/me/medicines').json()['breathing_enabled'] is False
    assert c.post('/api/sessions',json={"patient_id":pid,"breaths":[]}).status_code==403
    assert doctor.put(f'/api/patients/{pid}/breathing',json={"enabled":True}).status_code==200
    assert c.get('/api/me/medicines').json()['breathing_enabled'] is True
    assert login_as('admin@demo-riverside.example').put(f'/api/patients/{pid}/breathing',json={"enabled":False}).status_code==404


def test_registration_number_change_invalidates_otp(fresh, login_as, anon):
    doctor = login_as('meera.nair@demo-general.example')
    pid = register(doctor)
    identity = {"hospital_id": 1, "registration_no": "FLOW-123"}
    challenge = anon.post('/api/me/otp/request', json=identity).json()
    assert doctor.put(f'/api/patients/{pid}/regno', json={"registration_no": "FLOW-456"}).status_code == 200
    assert anon.post('/api/me/otp/verify', json={**identity, "challenge_id": challenge['challenge_id'],
        "code": challenge['demo_code']}).status_code == 401
    assert service.store().select('app_settings', [("key", "eq", "otp:1:FLOW-123")]) == []
    identity['registration_no'] = 'FLOW-456'
    challenge = anon.post('/api/me/otp/request', json=identity).json()
    assert anon.post('/api/me/otp/verify', json={**identity, "challenge_id": challenge['challenge_id'],
        "code": challenge['demo_code']}).status_code == 200


def test_missed_medicine_alert_dedupes_and_resolves(fresh, monkeypatch):
    from backend.app.meds import service as meds, reminders
    stamp=now_local().replace(hour=12,minute=0,second=0)
    monkeypatch.setattr(meds,'now_local',lambda:stamp)
    reminders.tick(force=True)
    rows=service.store().select('alerts',[("patient_id","eq",1),("kind","eq","missed_dose")])
    assert len(rows)==1 and rows[0]['severity']=='amber'
    reminders.tick(force=True)
    assert len(service.store().select('alerts',[("patient_id","eq",1),("kind","eq","missed_dose")]))==1
    for d in meds.today_doses(1):
        if d['status']=='missed':meds.report_dose(d['id'],'patient',1)
    reminders.tick(force=True)
    assert service.store().select('alerts',[("id","eq",rows[0]['id'])])[0]['status']=='resolved'
