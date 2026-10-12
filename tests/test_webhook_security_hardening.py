"""Provider callback authentication, exercised without any outbound network requests."""
from urllib.parse import parse_qs, urlparse

import pytest

from backend.app import service
from backend.app.comms import calls


C = '/api/comms'
BASE = 'https://callbacks.example.test'


def _call(monkeypatch):
    monkeypatch.setenv('CALL_PROVIDER', 'dry_run')
    monkeypatch.setattr(calls.audio, 'tts_url', lambda *a, **kw: None)
    p = service.get_patient_row(1)
    return calls.place_call(p, 'reminder', 'patient', p['name'], None, 'en', consent=True)


def test_twilio_signed_get_uses_canonical_url_including_query(fresh, anon, monkeypatch):
    from twilio.request_validator import RequestValidator
    call = _call(monkeypatch)
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', 'fixture-twilio-token')
    monkeypatch.setenv('PUBLIC_BASE_URL', BASE)
    path = f"{C}/twilio/voice/{call['id']}?retry=1"
    signature = RequestValidator('fixture-twilio-token').compute_signature(BASE + path, {})
    assert anon.get(path, headers={'X-Twilio-Signature': 'wrong'}).status_code == 403
    assert calls.get_call(call['id'])['status'] == 'ringing'
    result = anon.get(path, headers={'X-Twilio-Signature': signature})
    assert result.status_code == 200 and '<Response>' in result.text
    assert calls.get_call(call['id'])['status'] == 'in-progress'


def test_twilio_validation_cannot_be_disabled_with_configured_credentials(fresh, anon, monkeypatch):
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', 'fixture-twilio-token')
    monkeypatch.setenv('PUBLIC_BASE_URL', BASE)
    monkeypatch.setenv('TWILIO_VALIDATE', '0')
    assert anon.post(f'{C}/webhooks/whatsapp', data={'Body': 'STOP'}).status_code == 403


def test_unconfigured_twilio_callback_is_closed_outside_demo(fresh, anon, monkeypatch):
    monkeypatch.setenv('DEMO_MODE', '0')
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', '')
    assert anon.post(f'{C}/webhooks/whatsapp', data={'Body': 'STOP'}).status_code == 403


@pytest.mark.parametrize('endpoint', ['greeting', 'gather', 'passthru', 'status'])
def test_all_exotel_callbacks_require_secret_before_mutation(fresh, anon, monkeypatch, endpoint):
    call = _call(monkeypatch)
    monkeypatch.setenv('EXOTEL_WEBHOOK_SECRET', 'fixture-secret')
    if endpoint == 'status':
        response = anon.post(f"{C}/exotel/status/{call['id']}", data={'Status': 'completed'})
    else:
        response = anon.get(f"{C}/exotel/{endpoint}?CustomField={call['id']}&digits=1&token=wrong")
    assert response.status_code == 403
    assert calls.get_call(call['id'])['status'] == 'ringing'


def test_exotel_valid_secret_allows_expected_callback_contracts(fresh, anon, monkeypatch):
    call = _call(monkeypatch)
    secret = 'fixture+secret=with/slash'
    monkeypatch.setenv('EXOTEL_WEBHOOK_SECRET', secret)
    headers = {'X-SpiroBuddy-Webhook-Token': secret}
    cid = call['id']
    assert anon.get(f'{C}/exotel/greeting', params={'CustomField': cid}, headers=headers).status_code == 200
    assert calls.get_call(cid)['status'] == 'in-progress'
    gather = anon.get(f'{C}/exotel/gather', params={'CustomField': cid, 'token': secret})
    assert gather.status_code == 200 and gather.json()['max_input_digits'] == 1
    assert anon.get(f'{C}/exotel/passthru', params={'CustomField': cid, 'digits': '1', 'token': secret}).status_code == 200
    assert anon.post(f'{C}/exotel/status/{cid}', params={'token': secret}, data={'Status': 'completed'}).status_code == 200
    assert calls.get_call(cid)['status'] == 'completed'
    monkeypatch.setenv('PUBLIC_BASE_URL', BASE)
    generated = urlparse(calls._exotel_status_url(cid))
    assert generated.path == f'{C}/exotel/status/{cid}'
    assert parse_qs(generated.query)['token'] == [secret]


def test_exotel_outbound_is_not_ready_without_callback_secret(monkeypatch):
    for key in ('EXOTEL_SID', 'EXOTEL_API_KEY', 'EXOTEL_API_TOKEN', 'EXOTEL_CALLER_ID'):
        monkeypatch.setenv(key, 'fixture-value')
    monkeypatch.setenv('EXOTEL_WEBHOOK_SECRET', '')
    assert calls.exotel_ready() is False
    assert calls._exotel_call(1, '+919800000002', 30) == 'Exotel callback authentication is not configured'
