"""v4 recorder: the whole demo in care order with one persona-matching fictional patient (68, Hindi).
Logs shot marks, click points (for click rings), success-element boxes (for zooms) and a sync flash per video.
run.json is rewritten after every shot, so a failure never loses the log. Fictional sample data only.
Usage: python live_run_v4.py <base_url> <out_dir> "<patient name>" """
import json, re, sys, time, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/'); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
NAME = sys.argv[3]; FIRST = NAME.split()[0]; AGE = '68'
RX = ('Paracetamol | 500 mg | tablet | 1 | tablet | 1-1-1 | 5 | \n'
      'Pantoprazole | 40 mg | tablet | 1 | tablet | 1-0-0 | 5 | Before breakfast')
DOC = {'condition_summary': 'Recovering after planned lung surgery (sample patient).',
       'home_care': 'Keep the wound dry for 48 hours. Walk a little every few hours.',
       'exercise_instructions': 'Ten slow breaths on your spirometer every hour while awake, as taught on the ward.',
       'follow_up': 'Call the ward, or 112 in an emergency, if you have fever, redness at the wound or new breathlessness.'}
SW, SH = 1280, 720
T0, marks, events, info, vids, sync = {}, [], [], {'name': NAME}, {}, {}

def log(*a): print(time.strftime('%H:%M:%S') + f'.{int(time.time() * 1000) % 1000:03d}', *a, flush=True)
def t(ctx): return round(time.monotonic() - T0[ctx], 2)
def wait_text(page, text, timeout=45000):
    page.wait_for_function('t => document.body && document.body.innerText.includes(t)', arg=text, timeout=timeout)
def pause(s): time.sleep(s)
def btn(page, name): return page.get_by_role('button', name=name, exact=True).first
def ev(name, ctx, **kw): events.append(dict(name=name, ctx=ctx, t=t(ctx), **kw))
def dump():
    json.dump(dict(marks=marks, events=events, info=info, videos=vids, sync=sync, size={'doc': [SW, SH], 'staff': [SW, SH], 'pat': [412, 860]}),
              open(OUT / 'run.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

class Shot:
    def __init__(self, scene, ctx): self.scene, self.ctx = scene, ctx
    def __enter__(self): self.a = t(self.ctx); log('START', self.scene, self.ctx, self.a); return self
    def __exit__(self, et, ev_, tb):
        b = t(self.ctx); marks.append(dict(scene=self.scene, ctx=self.ctx, a=self.a, b=b, ok=et is None)); dump()
        log('END  ', self.scene, self.ctx, b, 'OK' if et is None else f'FAILED: {ev_}'); return False

def click(page, ctx, loc):
    loc.scroll_into_view_if_needed()
    bb = loc.bounding_box()
    if bb: ev('click', ctx, x=bb['x'] + bb['width'] / 2, y=bb['y'] + bb['height'] / 2)
    loc.click()

def focus(page, ctx, loc, scene):
    try:
        bb = loc.bounding_box()
        if bb: ev('focus', ctx, scene=scene, x=bb['x'], y=bb['y'], w=bb['width'], h=bb['height'])
    except Exception as e: log('focus failed', scene, e)

def pick(page, js_find):
    page.evaluate('() => document.querySelectorAll("[data-pick]").forEach(e => e.removeAttribute("data-pick"))')
    ok = page.evaluate(f'() => {{ const el = ({js_find}); if (!el) return false; el.setAttribute("data-pick", "1"); return true; }}')
    if not ok: raise RuntimeError('element not found: ' + js_find[:80])
    return page.locator('[data-pick="1"]')
def pick_retry(page, js, tries=40):
    for i in range(tries):
        try: return pick(page, js)
        except RuntimeError: time.sleep(0.5)
    return pick(page, js)
def sim(page, kind, until):
    for i in range(8):
        page.locator(f'button[data-sim="{kind}"]:visible').first.click()
        try: wait_text(page, until, 5000); return
        except Exception: pass
    raise RuntimeError('simulated breath not accepted: ' + kind)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge')
    def ctx(name, w, h):
        c = browser.new_context(viewport={'width': w, 'height': h}, record_video_dir=str(OUT / name),
                                record_video_size={'width': w, 'height': h}, locale='en-IN', timezone_id='Asia/Kolkata')
        pg = c.new_page(); T0[name] = time.monotonic(); pg.on('dialog', lambda d: d.accept()); pg.set_default_timeout(45000)
        pg.set_content('<body style="margin:0;background:#000"></body>'); time.sleep(0.8)      # sync flash: black, then white at a logged time
        sync[name] = t(name); pg.evaluate("document.body.style.background='#fff'"); time.sleep(0.6)
        return c, pg
    dctx, doc = ctx('doc', SW, SH); pctx, pat = ctx('pat', 412, 860); sctx, staff = ctx('staff', SW, SH)
    try:
        # ---------------- off camera: logins, a free hospital number, a free bed in the chest ward
        doc.goto(BASE + '/api/health'); log('health', doc.inner_text('body')[:110])
        doc.goto(BASE + '/login.html'); btn(doc, 'Try as Doctor').click(); doc.wait_for_url(re.compile('doctor-day'))
        staff.goto(BASE + '/login.html'); btn(staff, 'Try as Admin').click(); staff.wait_for_load_state('networkidle')
        pat.goto(BASE + '/patient-login.html'); pat.wait_for_selector('#number')
        pats = doc.request.get(BASE + '/api/patients').text()
        if NAME in pats: raise RuntimeError(f'a patient named {NAME} already exists here; choose another name')
        n = 412
        while f'DGH-26-{n:04d}' in pats: n += 1
        MRN = f'DGH-26-{n:04d}'; PHONE = f'+91000000{n:04d}'; info['mrn'] = MRN; log('using', MRN)
        staff.goto(BASE + '/department.html'); wait_text(staff, 'Configure a bed'); staff.wait_for_load_state('networkidle'); pause(2)
        def chest_beds(): return re.findall(r'Chest Ward · (C-\d+)\s*\n\s*Chest Medicine · (\w+)', staff.inner_text('main'))
        beds = chest_beds(); free = [b for b, s in beds if s == 'available']; log('chest ward beds', beds)
        if free: BED = free[0]
        else:
            BED = f'C-{max([int(b[2:]) for b, _ in beds] + [6]) + 1:02d}'; sels = staff.locator('main select')
            for attempt in range(3):
                sels.nth(0).select_option(label='Chest Medicine'); sels.nth(1).select_option(label='Chest Ward')
                staff.locator('input[placeholder="For example A-01"]').fill(BED); btn(staff, 'Add bed').click()
                try: wait_text(staff, f'Chest Ward · {BED}', 25000); break
                except Exception: log('bed retry', BED); staff.reload(); wait_text(staff, 'Configure a bed'); pause(2); sels = staff.locator('main select')
        info['bed'] = BED; log('bed', BED)
        doc.goto(BASE + '/register.html'); doc.wait_for_selector('input[name=registration_no]'); pause(1)

        # ---------------- 1. In hospital: the doctor registers the patient
        with Shot('s1_register', 'doc'):
            pause(0.8)
            doc.locator('input[name=registration_no]').type(MRN, delay=45)
            doc.locator('input[name=name]').type(NAME, delay=40)
            doc.locator('input[name=age]').type(AGE, delay=80)
            doc.locator('select[name=sex]').select_option('F'); pause(0.25)
            doc.locator('input[name=phone]').type(PHONE, delay=22)
            doc.locator('select[name=language]').select_option('hi'); pause(0.3)
            doc.locator('input[name=condition]').type('Recovery after lung surgery', delay=16)
            mod = doc.locator('input[name=breathing_enabled]'); mod.scroll_into_view_if_needed()
            focus(doc, 'doc', mod.locator('xpath=..'), 's1_module'); click(doc, 'doc', mod); pause(1.0)
            if not mod.is_checked(): raise RuntimeError('breathing module box is not ticked')
            click(doc, 'doc', btn(doc, 'Register patient'))
            wait_text(doc, 'registered'); ev('registered', 'doc'); pause(0.4)
            focus(doc, 'doc', doc.get_by_text(f'{NAME} registered').first.locator('xpath=..'), 's1_register'); pause(2.6)
        PID_LINK = doc.get_by_role('link', name='Write prescription').get_attribute('href'); PID = re.search(r'id=(\d+)', PID_LINK).group(1); info['pid'] = PID

        # ---------------- 2. The admin admits her to a chest-ward bed, then the hospital overview
        staff.reload(); wait_text(staff, 'Bed board'); pause(1)
        staff.locator('main select').nth(2).select_option(label='Chest Medicine'); pause(1.5)
        card_js = f'''[...document.querySelectorAll("main *")].filter(e => e.innerText && e.innerText.startsWith("Chest Ward · {BED}") && e.querySelector("select")).pop()'''
        pick_retry(staff, card_js).scroll_into_view_if_needed(); pause(1)
        with Shot('s2a_admit', 'staff'):
            pause(0.9)
            bed = pick(staff, card_js)
            val = staff.evaluate(f'''() => [...document.querySelector("[data-pick] select").options].find(o => o.text.includes("{MRN}")).value''')
            click(staff, 'staff', bed.locator('select')); bed.locator('select').select_option(val); pause(0.9)
            click(staff, 'staff', bed.get_by_role('button', name='Admit / transfer here', exact=True))
            staff.wait_for_function(f'''() => [...document.querySelectorAll("main *")].some(e => e.innerText && e.innerText.startsWith("Chest Ward · {BED}") && e.innerText.includes("occupied") && e.innerText.includes("{NAME}"))''')
            ev('admitted', 'staff'); pause(0.5)
            focus(staff, 'staff', pick(staff, f'''[...document.querySelectorAll("main *")].filter(e => e.innerText && e.innerText.startsWith("Chest Ward · {BED}") && e.innerText.includes("occupied") && e.innerText.length < 260).pop()'''), 's2a_admit'); pause(2.2)
        staff.goto(BASE + '/hospital-overview.html'); wait_text(staff, 'Current admissions')
        staff.wait_for_function("() => !document.body.innerText.includes('Checking hospital session')"); pause(1.4)
        with Shot('s2b_overview', 'staff'):
            pause(0.9); focus(staff, 'staff', staff.get_by_text('Current admissions').first.locator('xpath=..'), 's2b_overview'); pause(2.6)
        info['overview'] = staff.inner_text('body')[:600]

        # ---------------- 10. (recorded here while the admin is logged in) the hospital's own name and colour: preview only, Undo, nothing saved
        staff.goto(BASE + '/branding.html'); wait_text(staff, 'What patients see')
        staff.wait_for_function("() => (document.querySelector('#f-hex')||{value:''}).value.length === 7 && document.querySelector('#bd-preview').children.length > 0")
        form = lambda: staff.evaluate("() => [document.querySelector('#f-name').value, document.querySelector('#f-short').value, document.querySelector('#f-hex').value]")
        info['brand_before'] = form(); log('branding before', info['brand_before']); pause(1.2)
        with Shot('s10_branding', 'staff'):
            pause(1.3); focus(staff, 'staff', staff.locator('.bd-phone'), 's10_before')
            nm = staff.locator('#f-name'); click(staff, 'staff', nm); nm.press('Control+A'); nm.type('Riverside Care', delay=70); pause(0.9)
            hx = staff.locator('#f-hex'); click(staff, 'staff', hx); hx.fill('#7a2e8c'); ev('recolour', 'staff'); pause(0.5)
            focus(staff, 'staff', staff.locator('.bd-phone'), 's10_branding'); pause(2.8)
            click(staff, 'staff', staff.locator('#bd-undo')); ev('undo', 'staff'); pause(1.8)
        info['brand_after'] = form(); log('branding after', info['brand_after'])
        if info['brand_after'] != info['brand_before']: raise RuntimeError('branding form did not return to the saved values')

        # ---------------- 3. The doctor writes the prescription (a draft she reviews)
        doc.goto(f'{BASE}/prescribe.html?id={PID}'); doc.wait_for_selector('#notepad-text'); pause(1)
        with Shot('s3_prescribe', 'doc'):
            pause(0.7); doc.locator('#notepad-text').click(); doc.locator('#notepad-text').type(RX, delay=9); pause(0.5)
            click(doc, 'doc', doc.locator('#draft-text'))
            doc.wait_for_function('() => (document.querySelector("#draft-result")||{}).textContent.trim().length > 0'); ev('drafted', 'doc'); pause(1)
            foods = doc.locator('select:has(option[value="after_food"])')
            foods.nth(0).scroll_into_view_if_needed(); pause(0.8)
            info['food_before'] = foods.nth(0).locator('option:checked').inner_text()
            focus(doc, 'doc', foods.nth(0), 's3_needs_review'); pause(2.2)
            click(doc, 'doc', foods.nth(0)); foods.nth(0).select_option('after_food'); ev('after_food', 'doc'); pause(1.0)
            foods.nth(1).scroll_into_view_if_needed(); pause(0.4); foods.nth(1).select_option('before_food'); pause(0.7)
            send = btn(doc, "Send to the patient's phone"); click(doc, 'doc', send)
            btn(doc, 'Send now').wait_for(); ev('dialog', 'doc'); focus(doc, 'doc', btn(doc, 'Send now').locator('xpath=../..'), 's3_dialog'); pause(1.5)
            click(doc, 'doc', btn(doc, 'Send now'))
            wait_text(doc, 'Sent to'); ev('sent', 'doc'); pause(0.6)
            cm = doc.get_by_text('Current medicines').first; cm.scroll_into_view_if_needed(); pause(0.4)
            focus(doc, 'doc', doc.get_by_text('Prescription of').first.locator('xpath=../..'), 's3_prescribe'); pause(2.4)
        info['draft_result'] = doc.locator('#draft-result').text_content()

        # off camera: the doctor saves the discharge draft
        doc.goto(f'{BASE}/discharge-editor.html?id={PID}'); doc.wait_for_load_state('networkidle')
        if doc.get_by_role('button', name='Create replacement / new draft').count(): btn(doc, 'Create replacement / new draft').click()
        doc.wait_for_selector('textarea[name=home_care]')
        for k_, v_ in DOC.items(): doc.locator(f'textarea[name={k_}]').fill(v_)
        btn(doc, 'Save draft').click(); wait_text(doc, 'Draft saved'); pause(1)
        doc.goto(f'{BASE}/discharge-editor.html?id={PID}'); doc.wait_for_selector('#publish'); pause(1.2)

        # ---------------- 4. Discharge: the doctor publishes the care instructions
        with Shot('s4_publish', 'doc'):
            pause(1.4); click(doc, 'doc', doc.locator('#publish'))
            wait_text(doc, 'Published version'); ev('published', 'doc'); doc.evaluate('window.scrollTo(0,0)'); pause(0.5)
            focus(doc, 'doc', doc.get_by_text('Published version').first, 's4_publish'); pause(2.4)

        # off camera: her consent for automated calls is recorded on her chart, through the normal form, and read back
        def care(): return doc.request.get(f'{BASE}/api/comms/care/{PID}').json()['settings']
        doc.goto(f'{BASE}/patient.html?id={PID}')
        doc.wait_for_selector('#cc-steps label', state='attached')   # these rows are drawn only after her saved settings have loaded
        doc.locator('#cc-consent').check()
        sv = doc.locator('#cc-save'); sv.scroll_into_view_if_needed(); sv.click()
        wait_text(doc, 'Settings saved', 30000)
        if not care().get('consent_ok'): raise RuntimeError('consent was not saved')
        info['consent_at'] = care().get('consent_at'); log('consent saved and read back', info['consent_at'])

        # ---------------- 5. At home: login (code delivery simulated), medicines in Hindi then English, pharmacy screen
        with Shot('s5a_login', 'pat'):
            pause(0.7); pat.locator('#number').type(MRN, delay=55); pause(0.4)
            click(pat, 'pat', btn(pat, 'Send my code'))
            wait_text(pat, 'This code appears here instead of an SMS.'); ev('code', 'pat')
            code = re.search(r'\d{6}', pat.inner_text('#sample-code')).group(0)
            pause(0.4); focus(pat, 'pat', pat.locator('#sample-code'), 's5a_login'); pause(1.8)
            pat.locator('#code').type(code, delay=90); pause(0.4)
            click(pat, 'pat', btn(pat, 'Open my medicines')); pat.wait_for_url(re.compile('meds'))
            pat.wait_for_function("() => /(9:00 PM|रात|PM)/.test(document.body.innerText)"); ev('meds_hindi', 'pat'); pause(3.4)
        with Shot('s5b_meds', 'pat'):
            click(pat, 'pat', btn(pat, 'English')); ev('english', 'pat'); pause(1.2)
            card = pat.get_by_text('9:00 PM').first; card.scroll_into_view_if_needed(); pat.mouse.wheel(0, 120); pause(0.6)
            focus(pat, 'pat', pat.get_by_text('9:00 PM').first.locator('xpath=../../..'), 's5b_meds'); pause(2.6)
        with Shot('s5c_pharmacy', 'pat'):
            ph = btn(pat, 'Show at the pharmacy'); click(pat, 'pat', ph)
            wait_text(pat, 'Pharmacist: scan'); ev('pharmacy', 'pat'); pause(2.0)
            qr = pat.get_by_text('Pharmacist: scan').first; qr.scroll_into_view_if_needed(); pause(0.5)
            focus(pat, 'pat', qr.locator('xpath=..'), 's5c_pharmacy'); pause(2.4)
        btn(pat, 'Close').click(); pause(0.4)

        # ---------------- 6. Care instructions read at home
        pat.goto(BASE + '/my-care.html?lang=en'); wait_text(pat, 'I have read this version'); pause(1)
        with Shot('s6_ack', 'pat'):
            pause(1.4); click(pat, 'pat', btn(pat, 'I have read this version'))
            wait_text(pat, 'Read acknowledgement saved'); ev('ack', 'pat'); pause(0.4)
            focus(pat, 'pat', pat.get_by_text('Read acknowledgement saved').first, 's6_ack'); pause(2.4)

        # ---------------- 7. SpiroBuddy: where the unit will connect, then a short simulated session
        pat.goto(BASE + '/meds.html?lang=en'); wait_text(pat, 'My breathing exercise')
        lk = pat.get_by_role('link', name='My breathing exercise (Simulated)'); lk.scroll_into_view_if_needed(); lk.click()
        wait_text(pat, 'Start my exercise'); wait_text(pat, FIRST); pause(1)
        pat.evaluate("() => { const d=document.querySelector('#d-auto').closest('details'); if(d) d.open=true; }")
        pat.locator('#d-usb').scroll_into_view_if_needed(); pat.mouse.wheel(0, 600); pause(1)
        with Shot('s7a_device', 'pat'):
            pause(0.6); focus(pat, 'pat', pat.locator('#d-usb'), 's7a_device')
            focus(pat, 'pat', pat.locator('#d-usb').locator('xpath=ancestor::details[1]'), 's7a_panel'); pause(3)
        pat.evaluate('window.scrollTo(0,0)'); pause(1)
        with Shot('s7b_breathing', 'pat'):
            pause(0.6); click(pat, 'pat', pat.locator('#start')); wait_text(pat, 'Breath 1 of 10'); ev('breath1', 'pat'); pause(1)
            sim(pat, 'good', 'Breath 2 of 10'); ev('breath2', 'pat'); pause(2)
            sim(pat, 'too_fast', 'Breath 3 of 10'); ev('breath3', 'pat'); pause(2.2)
            for i in range(10):
                f = pat.get_by_role('button', name='Finish now', exact=True)
                if f.count() and f.first.is_visible(): f.first.click()
                try: wait_text(pat, 'Session saved', 4000); break
                except Exception: pass
            ev('saved', 'pat'); pause(0.4)
            sv_ = pat.get_by_text('Session saved').first.locator('xpath=..'); info['session_saved'] = sv_.inner_text()
            focus(pat, 'pat', sv_, 's7b_breathing'); pause(2.8)

        # ---------------- 8. A follow-up visit: request, the doctor confirms, the phone shows Confirmed
        pat.goto(BASE + '/patient-visits.html?lang=en'); btn(pat, 'Ask for a visit').wait_for(); pause(1)
        with Shot('s8a_request', 'pat'):
            pause(0.6); click(pat, 'pat', btn(pat, 'Ask for a visit')); wait_text(pat, 'Choose a day'); pause(1.1)
            click(pat, 'pat', pat.locator('button:visible', has_text='Tomorrow').first); wait_text(pat, 'Choose a time'); pause(1.1)
            slot = pat.locator('button:visible:not([disabled])', has_text=re.compile(r'^\s*\d{1,2}:\d{2} [AP]M\s*$')).first
            info['slot'] = slot.inner_text().strip(); click(pat, 'pat', slot); pause(0.8)
            click(pat, 'pat', btn(pat, 'Check-up')); pause(0.6)
            click(pat, 'pat', btn(pat, 'Send request')); wait_text(pat, 'Your request was sent'); ev('requested', 'pat'); pause(0.4)
            focus(pat, 'pat', pat.get_by_text('Your request was sent').first, 's8a_request'); pause(2.2)
        doc.goto(BASE + '/doctor-day.html'); wait_text(doc, 'Needs your answer'); wait_text(doc, NAME); pause(1)
        card_v = f'''[...document.querySelectorAll("main *")].filter(e => e.innerText && e.innerText.includes("{NAME}") && e.innerText.includes("{info['slot']}") && e.innerText.includes("Requested") && [...e.querySelectorAll("button")].some(b => b.innerText.trim()==="Confirm")).pop()'''
        pick_retry(doc, card_v).scroll_into_view_if_needed(); pause(0.8)
        done_v = f'''[...document.querySelectorAll("main *")].filter(e => e.innerText && e.innerText.includes("{NAME}") && e.innerText.includes("{info['slot']}") && e.innerText.includes("Confirmed") && e.innerText.length < 400).pop()'''
        with Shot('s8b_confirm', 'doc'):
            pause(1); card = pick(doc, card_v); focus(doc, 'doc', card, 's8b_request_card'); pause(1.3)
            click(doc, 'doc', card.get_by_role('button', name='Confirm', exact=True))
            wait_text(doc, 'Visit confirmed.'); ev('confirmed', 'doc'); pause(1)
            click(doc, 'doc', btn(doc, 'Tomorrow'))
            got = pick_retry(doc, done_v); got.scroll_into_view_if_needed(); ev('tomorrow', 'doc'); pause(0.5)
            focus(doc, 'doc', pick(doc, done_v), 's8b_confirm'); pause(2.0)
        pat.goto(BASE + '/patient-visits.html?lang=en'); wait_text(pat, 'Confirmed'); pause(1.2)
        with Shot('s8c_confirmed', 'pat'):
            pause(0.6); focus(pat, 'pat', pat.get_by_text('Confirmed').first.locator('xpath=../..'), 's8c_confirmed'); pause(2.6)

        # ---------------- 9. A concern: simulated Hindi check-in call, then the nurse takes it
        staff.goto(BASE + '/login.html'); btn(staff, 'Try as Nurse').click(); staff.wait_for_url(re.compile('dashboard')); wait_text(staff, 'Alerts inbox')
        doc.goto(BASE + '/demo.html'); wait_text(doc, 'Calls & WhatsApp')
        doc.wait_for_function("() => !document.body.innerText.includes('Loading patients')"); pause(1.5)
        doc.get_by_text('Calls & WhatsApp – live simulators').first.scroll_into_view_if_needed(); pause(1)
        sel = doc.locator('select:has(option:text-is("Ravi Kumar ★"))').first
        opts = [o for o in sel.locator('option').all_inner_texts() if NAME in o]
        if len(opts) != 1: raise RuntimeError(f'expected one {NAME} in the simulator list, found {opts}')
        sel.select_option(label=opts[0]); pause(1.5)
        with Shot('s9a_call', 'doc'):
            pause(0.7); click(doc, 'doc', btn(doc, 'AI check-in call – optional, where consent allows'))
            ans = doc.locator('button.acc:visible').first; ans.wait_for(); ev('ringing', 'doc')
            doc.locator('.phone-screen').first.scroll_into_view_if_needed(); pause(1.2)
            focus(doc, 'doc', doc.locator('.phone-screen').first, 's9a_phone')
            click(doc, 'doc', ans); wait_text(doc, 'क्या आप बताना चाहेंगे'); ev('ai_line_1', 'doc')
            mm = re.search(r'(\d+) बार', doc.locator('.phone-screen').first.inner_text()); info['missed'] = int(mm.group(1)) if mm else None; log('missed in call', info['missed']); pause(4.6)
            click(doc, 'doc', doc.locator('button:visible', has_text='आज सुबह टांकों के पास हल्का दर्द था').first)
            doc.locator('button:visible', has_text='हाँ, कॉल कीजिए').first.wait_for(); ev('ai_line_2', 'doc'); pause(5)
            click(doc, 'doc', doc.locator('button:visible', has_text='हाँ, कॉल कीजिए').first)
            wait_text(doc, 'Nurse review requested'); ev('ai_line_3', 'doc'); pause(0.6)
            focus(doc, 'doc', doc.locator('.phone-screen').first.get_by_text('Nurse review requested').first.locator('xpath=..'), 's9a_call'); pause(3.6)
        info['call_screen'] = doc.locator('.phone-screen').first.inner_text()

        ALERT_JS = f'''[...document.querySelectorAll("main *")].filter(e => e.innerText && e.innerText.includes("{NAME}: check-in call") && [...e.querySelectorAll("button")].some(b => b.innerText.trim()==="Acknowledge")).sort((a,b)=>a.innerText.length-b.innerText.length)[0]'''
        staff.reload(); wait_text(staff, 'Alerts inbox'); wait_text(staff, f'{NAME}: check-in call')
        pick_retry(staff, ALERT_JS).scroll_into_view_if_needed(); staff.mouse.wheel(0, 160); pause(1.2)
        with Shot('s9b_nurse', 'staff'):
            pause(0.9); alert = pick_retry(staff, ALERT_JS)
            click(staff, 'staff', alert.locator('summary').first); pause(0.5)
            alert = pick_retry(staff, ALERT_JS); focus(staff, 'staff', alert, 's9b_nurse'); ev('own_words', 'staff')
            info['alert_text'] = alert.inner_text(); pause(3.2)
            mine_btn = alert.get_by_role('button', name='Assign to me', exact=True)
            if mine_btn.count():
                click(staff, 'staff', mine_btn.first); wait_text(staff, 'Assigned to you', 20000); ev('assigned', 'staff'); pause(1.6)
                alert = pick_retry(staff, ALERT_JS); focus(staff, 'staff', alert, 's9b_assigned')
            click(staff, 'staff', alert.get_by_role('button', name='Acknowledge', exact=True))
            try: wait_text(staff, 'Acknowledged', 20000); ev('acknowledged', 'staff')
            except Exception as e: log('no Acknowledged toast seen', e)
            pause(2.8)

        # architecture stills
        actx = browser.new_context(viewport={'width': 1920, 'height': 1080}); ap = actx.new_page()
        ap.goto(BASE + '/architecture.html'); ap.get_by_text('1. The system').first.scroll_into_view_if_needed(); ap.evaluate('window.scrollBy(0, -20)'); pause(1)
        ap.screenshot(path=str(OUT / 'arch.png')); actx.close()
    finally:
        for name, c, pg in (('doc', dctx, doc), ('pat', pctx, pat), ('staff', sctx, staff)):
            try:
                v = pg.video; c.close(); vids[name] = str(v.path())
            except Exception as e: log('video close failed', name, e)
        dump(); browser.close()
log('DONE', [(m['scene'], m['ok']) for m in marks])
