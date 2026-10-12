"""No real provider calls: destination fencing and safe check-in simulator endings."""
import pytest

from backend.app import service
from backend.app.comms import calls, common, sarvam


ROUTE_KEYS = ('DEMO_PATIENT_PHONE', 'DEMO_NURSE_PHONE', 'DEMO_NURSE_WHATSAPP',
              'DEMO_GUARDIAN_PHONE', 'DEMO_FAMILY_WHATSAPP')


@pytest.mark.parametrize('role,key', [('patient', 'DEMO_PATIENT_PHONE'),
    ('nurse', 'DEMO_NURSE_PHONE'), ('guardian', 'DEMO_GUARDIAN_PHONE')])
def test_demo_destination_requires_explicit_team_route(monkeypatch, role, key):
    monkeypatch.setenv('DEMO_MODE', '1')
    for route in ROUTE_KEYS:
        monkeypatch.setenv(route, '')
    stored = '+919955012345'
    assert common.e164(stored)
    assert common.resolve_number(stored, role) is None
    monkeypatch.setenv(key, 'invalid')
    assert common.resolve_number(stored, role) is None
    monkeypatch.setenv(key, '+919800000002')
    assert common.resolve_number(stored, role) == '+919800000002'


def test_real_mode_uses_recorded_destination_not_demo_route(monkeypatch):
    monkeypatch.setenv('DEMO_MODE', '0')
    monkeypatch.setenv('DEMO_PATIENT_PHONE', '+919800000002')
    assert common.resolve_number('+919955012345', 'patient') == '+919955012345'
    assert common.resolve_number('not a number', 'patient') is None


def test_legacy_whatsapp_uses_same_team_only_fence(monkeypatch):
    from backend.app import whatsapp
    monkeypatch.setenv('DEMO_MODE', '1')
    for route in ROUTE_KEYS:
        monkeypatch.setenv(route, '')
    p = {'nurse_phone': '+919955012345', 'family_phone': '+919955012346'}
    assert whatsapp.resolve_number(p, 'nurse') is None
    assert whatsapp.resolve_number(p, 'family') is None
    monkeypatch.setenv('DEMO_NURSE_WHATSAPP', '+919800000002')
    monkeypatch.setenv('DEMO_FAMILY_WHATSAPP', '+919800000003')
    assert whatsapp.resolve_number(p, 'nurse') == 'whatsapp:+919800000002'
    assert whatsapp.resolve_number(p, 'family') == 'whatsapp:+919800000003'


def test_call_log_records_actual_team_destination_but_public_json_masks_it(fresh, monkeypatch):
    monkeypatch.setenv('DEMO_MODE', '1')
    monkeypatch.setenv('DEMO_PATIENT_PHONE', '+919800000002')
    monkeypatch.setenv('CALL_PROVIDER', 'dry_run')
    monkeypatch.setattr(calls.audio, 'tts_url', lambda *a, **kw: None)
    p = service.get_patient_row(1)
    public = calls.place_call(p, 'reminder', 'patient', p['name'], '+919955012345',
        'en', consent=True, style='agent')
    stored = calls.get_call(public['id'])
    assert stored['to_number'] == '+919800000002'
    assert stored['meta']['stored_number'] == '+919955012345'
    assert public['to_number'] == 'Ending 0002'
    assert '+919800000002' not in str(public)


def test_demo_nurse_bridge_does_not_dial_stored_nurse_when_team_route_missing(fresh, monkeypatch):
    monkeypatch.setenv('DEMO_MODE', '1')
    for route in ROUTE_KEYS:
        monkeypatch.setenv(route, '')
    monkeypatch.setenv('DEMO_PATIENT_PHONE', '+919800000002')
    monkeypatch.setattr(calls, 'provider', lambda *a: ('twilio', 'mock ready'))
    monkeypatch.setattr(calls, 'twilio_ready', lambda: True)
    monkeypatch.setattr(calls, 'exotel_ready', lambda: False)
    monkeypatch.setattr(calls, '_twilio_client', lambda: pytest.fail('Must not place a real bridge'))
    result = calls.click_to_call(service.get_patient_row(1), 'Sample nurse', '+919955012345',
        {'patient_phone': '+919955012346'})
    assert result['provider'] == 'dry_run'
    stored = calls.get_call(result['id'])
    assert stored['meta']['nurse_destination'] is None
    assert stored['to_number'] == '+919800000002'


@pytest.mark.parametrize('lang,pain,answer', [
    ('en', 'I had mild pain near the incision.', 'Yes, please call me.'),
    ('hi', 'आज सुबह टांकों के पास हल्का दर्द था।', 'हाँ, कॉल कीजिए।'),
    ('ta', 'இன்று காலை தையல் அருகே லேசான வலி இருந்தது.', 'ஆம், அழையுங்கள்.'),
])
def test_callback_closing_has_real_handoff_without_exercise_or_time_promise(
        fresh, monkeypatch, lang, pain, answer):
    monkeypatch.setenv('CALL_PROVIDER', 'dry_run')
    monkeypatch.setattr(calls.audio, 'tts_url', lambda *a, **kw: None)
    for route in ROUTE_KEYS:
        monkeypatch.setenv(route, '')
    p = service.get_patient_row(1)
    call = calls.place_call(p, 'reminder', 'patient', p['name'], '+919955012345',
        lang, consent=True, style='agent')
    assert call['provider'] == 'dry_run'
    assert not sarvam.sim_turn(call['id'], pain)['end']
    result = sarvam.sim_turn(call['id'], answer)
    assert result['end'] and result['result']['callback_requested']
    assert result['say'] == sarvam.line('bye_callback', lang)
    assert service.store().select('alerts', [('patient_id', 'eq', 1), ('kind', 'eq', 'call_review')])
    assert result['say'] != {
        'en': 'Okay, your nurse will call you back soon. Please try ten slow, deep breaths when you can. Goodbye.',
        'hi': 'ठीक है, नर्स जल्द ही आपको कॉल करेंगी। जब हो सके, दस धीमी, गहरी साँसें लीजिए। नमस्ते।',
        'ta': 'சரி, செவிலியர் விரைவில் அழைப்பார். முடிந்தபோது பத்து மெதுவான, ஆழ்ந்த மூச்சுகள் விடுங்கள். வணக்கம்.',
    }[lang]


def test_no_callback_closing_records_response_without_prescribing_exercise(fresh, monkeypatch):
    monkeypatch.setenv('CALL_PROVIDER', 'dry_run')
    monkeypatch.setattr(calls.audio, 'tts_url', lambda *a, **kw: None)
    p = service.get_patient_row(1)
    call = calls.place_call(p, 'reminder', 'patient', p['name'], None,
        'en', consent=True, style='agent')
    sarvam.sim_turn(call['id'], 'I had mild pain near the incision.')
    result = sarvam.sim_turn(call['id'], 'No, thank you.')
    assert result['end']
    assert result['say'] == sarvam.line('bye_ok', 'en')
    assert 'breaths' not in result['say'] and 'soon' not in result['say']
    assert result['result']['outcome'] == 'needs_nurse_review'
    assert service.store().select('alerts', [('patient_id', 'eq', 1), ('kind', 'eq', 'call_review')])
