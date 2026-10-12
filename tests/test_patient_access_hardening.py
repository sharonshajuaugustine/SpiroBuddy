"""Patient login keeps reusable challenges and rejects public access to non-sample records."""
from datetime import timedelta
from types import SimpleNamespace

import pytest

from backend.app import audit, patient_otp, ratelimit, service
from backend.app.config import now_local


@pytest.fixture(autouse=True)
def clean_access_limits():
    for bucket in ('otp_request', 'otp_verify', 'patient_session'):
        ratelimit.reset(bucket)
    yield
    for bucket in ('otp_request', 'otp_verify', 'patient_session'):
        ratelimit.reset(bucket)


def test_client_ip_uses_server_peer_not_forwarded_headers():
    request = SimpleNamespace(client=SimpleNamespace(host='192.0.2.17'),
        headers={'x-forwarded-for': '203.0.113.3, 203.0.113.4', 'x-real-ip': '203.0.113.5'})
    assert audit.client_ip(request) == '192.0.2.17'
    request.client = None
    assert audit.client_ip(request) is None
    assert audit.client_ip(None) is None


def test_resend_keeps_challenge_without_recovering_code(fresh, anon, monkeypatch):
    number = service.get_patient_row(1)['mrn']
    identity = {'hospital_id': 1, 'registration_no': number}
    stamp = now_local()
    monkeypatch.setattr(patient_otp, 'now', lambda: stamp)
    first = anon.post('/api/me/otp/request', json=identity).json()
    monkeypatch.setattr(patient_otp, 'now', lambda: stamp + timedelta(seconds=20))
    second = anon.post('/api/me/otp/request', json=identity).json()
    assert second['challenge_id'] == first['challenge_id']
    assert 'demo_code' not in second
    assert second['expires_in'] <= first['expires_in']
    state = service.store().select('app_settings', [('key', 'eq', patient_otp._key(1, number))])[0]['value']
    assert state['requests'] == 1 and state['attempts'] == 0
    assert first['demo_code'] not in str(state)
    verification = {**identity, 'challenge_id': second['challenge_id'], 'code': first['demo_code']}
    assert anon.post('/api/me/otp/verify', json=verification).status_code == 200
    third = anon.post('/api/me/otp/request', json=identity).json()
    assert third['challenge_id'] != first['challenge_id']
    assert 'demo_code' not in third
    assert anon.post('/api/me/otp/verify', json=verification).status_code == 401


def test_only_known_seed_identity_can_use_demo_id(fresh, anon):
    assert anon.post('/api/me/session', json={'patient_id': 1}).status_code == 200
    anon.cookies.clear()
    service.store().update('patients', [('id', 'eq', 1)], {'name': 'Replacement patient'})
    assert anon.post('/api/me/session', json={'patient_id': 1}).status_code == 403
    assert anon.get('/api/me/medicines').status_code == 401


def test_new_patient_requires_hospital_issued_token(fresh, login_as, anon):
    doctor = login_as('meera.nair@demo-general.example')
    registration = doctor.post('/api/patients', json={'registration_no': 'ACCESS-NEW-1',
        'name': 'Sample private patient', 'age': 40, 'sex': 'F', 'language': 'en'}).json()
    pid = registration['patient']['id']
    assert anon.post('/api/me/session', json={'patient_id': pid}).status_code == 403
    token = registration['app_link'].split('t=')[1]
    assert anon.post('/api/me/session', json={'token': token}).status_code == 200
    assert anon.get(f'/api/patients/{pid}').status_code == 200
    assert anon.get('/api/patients/1').status_code == 404


def test_demo_shortcut_is_disabled_in_real_mode(fresh, anon, monkeypatch):
    monkeypatch.setenv('DEMO_MODE', '0')
    assert anon.post('/api/me/session', json={'patient_id': 1}).status_code == 403
