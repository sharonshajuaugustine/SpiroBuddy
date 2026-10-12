"""Final assembly of the script and on-screen text: fit them to the patient who was actually recorded.
- The agents wrote the script with the placeholder name Kamala; the recording's fictional patient is read from run.json.
- The call subtitles use the app's own English wording of the same scripted lines (backend/app/comms/sarvam.py, common.py).
Usage: python assemble.py <narration_in.md> <spec_in.json> <rec_dir> <out_dir>"""
import json, re, sys, pathlib
narr_in, spec_in, rec, out = (pathlib.Path(a) for a in sys.argv[1:5]); out.mkdir(parents=True, exist_ok=True)
info = json.load(open(rec / 'run.json', encoding='utf-8'))['info']; NAME = info['name']; FIRST = NAME.split()[0]
def rename(s): return s.replace('Kamala Devi', NAME).replace('Kamala', FIRST)

md = rename(narr_in.read_text(encoding='utf-8'))
md = re.sub(r'\*\*Who reads the nurse-feedback line:\*\*[^\n]*',
            '**Who reads the nurse-feedback line:** as written ("a nurse in a team member\'s family") it is true for either speaker. '
            'If you are the team member whose mother gave the feedback, you may say "a nurse in my family" instead.', md)
md = md.replace('Read this with `spec.json` in the same folder.', 'The on-screen text for every block is in `docs/video/spec_v4.json`.')
(out / 'narration.md').write_text(md, encoding='utf-8')

spec = json.loads(rename(spec_in.read_text(encoding='utf-8')))
# Two short lines each (the checker's limit) so a viewer can read them in ~8 s: the app's own lines, condensed,
# keeping its safety advice (urgent help, 112).
spec['demo']['call_subs'] = [
    f'Assistant (scripted): "Namaste, SpiroBuddy\'s automated care assistant here.\n{FIRST} ji, you missed your exercise {{missed}} times. Are you okay? Why?"',
    f'{FIRST} (sample answer): "Mild pain near my stitches this morning."\nAssistant: "If severe or breathless, get urgent help. Should your nurse call?"',
    f'{FIRST}: "Yes, please call me."\nAssistant: "Request sent to your care team. In an emergency, call 112."']
spec['demo']['nurse_sub'] = 'Fixed rules, not AI. "Patient\'s own words" here = the preset sample answer.'
# The device link is drawn as a clear five-step path instead of a blurry crop of the architecture page (judges' note),
# with wording from the rulebook (claims.md item 8); the architecture page itself is zoomed onto its diagram.
DEVICE = {"type": "strip", "head": "How the clip-on unit would connect", "steps": [
    {"title": "Laser sensor", "text": "Would read how high the piston rises", "cue": None},
    {"title": "Controller", "text": "Small board; its firmware is written", "cue": None},
    {"title": "USB cable", "text": "To Chrome or Edge on a laptop", "cue": None},
    {"title": "Web app", "text": "The \"Connect device (USB)\" control", "cue": None},
    {"title": "Coach", "text": "Calibration would estimate the volume", "cue": None}],
    "footer": "USB unit: In development, no unit built or tested · Bluetooth: Planned · Today: built-in simulator (Simulated)"}
for blk in spec['part1']:
    gs = blk['graphics']
    for i, g in enumerate(gs):
        if g['type'] == 'image' and g.get('img') == 'arch_device':
            gs[i] = dict(DEVICE, cue=g.get('cue'))
            blk['graphics'] = gs = [x for j, x in enumerate(gs) if not (j > i and x['type'] == 'image' and x.get('img') == 'slide8')]
            break
    for g in gs:
        if g['type'] == 'image' and g.get('img') == 'arch': g['zoom'] = [0.5, 0.73, 1.75]
json.dump(spec, open(out / 'spec.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
left = [w for w in ('Kamala',) if w in md or w in json.dumps(spec, ensure_ascii=False)]
print('patient', NAME, '| leftover placeholder names:', left or 'none')
