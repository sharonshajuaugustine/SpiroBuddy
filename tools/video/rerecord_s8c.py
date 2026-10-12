"""Retake of one shot: the patient's visits page showing the confirmed visit (read-only; nothing is changed on the site
except a fresh login code for the same fictional patient). Adds the take to an existing run.json as video 'pat2'.
Usage: python rerecord_s8c.py <base_url> <rec_dir>"""
import json, re, sys, time, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/'); OUT = pathlib.Path(sys.argv[2])
run = json.load(open(OUT / 'run.json', encoding='utf-8')); MRN = run['info']['mrn']; SLOT = run['info']['slot']
def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
with sync_playwright() as p:
    br = p.chromium.launch(channel='msedge')
    c = br.new_context(viewport={'width': 412, 'height': 860}, record_video_dir=str(OUT / 'pat2'), record_video_size={'width': 412, 'height': 860},
                       locale='en-IN', timezone_id='Asia/Kolkata')
    pg = c.new_page(); T0 = time.monotonic(); t = lambda: round(time.monotonic() - T0, 2); pg.set_default_timeout(60000)
    pg.set_content('<body style="margin:0;background:#000"></body>'); time.sleep(0.8)
    sync = t(); pg.evaluate("document.body.style.background='#fff'"); time.sleep(0.6)
    try:
        pg.goto(BASE + '/patient-login.html'); pg.wait_for_selector('#number'); pg.locator('#number').fill(MRN)
        pg.get_by_role('button', name='Send my code', exact=True).first.click()
        pg.wait_for_function("() => /\\d{6}/.test((document.querySelector('#sample-code')||{}).innerText||'')")
        code = re.search(r'\d{6}', pg.inner_text('#sample-code')).group(0); pg.locator('#code').fill(code)
        pg.get_by_role('button', name='Open my medicines', exact=True).first.click(); pg.wait_for_url(re.compile('meds'))
        pg.goto(BASE + '/patient-visits.html?lang=en')
        card = pg.locator(':visible', has_text='Confirmed').filter(has_text=SLOT).last        # the visible card that shows Confirmed and her time
        pg.get_by_text('Confirmed', exact=True).first.wait_for(state='visible')
        pg.wait_for_function("t => [...document.querySelectorAll('main *, body *')].some(e => e.offsetParent && e.children.length === 0 && (e.innerText||'').includes(t))", arg=SLOT)
        time.sleep(1.5)
        lab = pg.get_by_text('Confirmed', exact=True).first; lab.scroll_into_view_if_needed(); pg.mouse.wheel(0, 160); time.sleep(1.0)
        a = t(); time.sleep(0.6)
        bb = lab.locator('xpath=../..').bounding_box(); ft = t(); time.sleep(3.0); b = t()
        text = pg.inner_text('body')
        if 'Confirmed' not in text or SLOT not in text: raise RuntimeError('confirmed visit not visible')
        log('visible text ok:', SLOT, 'Confirmed', 'a', a, 'b', b)
    finally:
        v = pg.video; c.close(); vpath = str(v.path()); br.close()
run['videos']['pat2'] = vpath; run['sync']['pat2'] = sync; run['size']['pat2'] = [412, 860]
run['marks'] = [m for m in run['marks'] if m['scene'] != 's8c_confirmed'] + [dict(scene='s8c_confirmed', ctx='pat2', a=a, b=b, ok=True, retake=True)]
run['events'] = [e for e in run['events'] if e.get('scene') != 's8c_confirmed'] + [dict(name='focus', ctx='pat2', scene='s8c_confirmed', t=ft, x=bb['x'], y=bb['y'], w=bb['width'], h=bb['height'])]
json.dump(run, open(OUT / 'run.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
log('DONE retake s8c', a, b)
