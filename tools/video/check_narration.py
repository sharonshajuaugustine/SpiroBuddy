# -*- coding: utf-8 -*-
"""Timing and format check for the version 4 video narration and its on-screen spec.

Usage:  python check_narration.py <narration.md> <spec.json>
Exit:   0 = no errors (warnings may still be printed), 1 = at least one error, 2 = wrong usage.

The narration is parsed exactly the way build_v4.py parses it (same split, same regex, same body rule),
so anything the build would silently drop or mis-time is reported here first.
ERROR   = breaks a stated rule of the format, or the build would fail / drop / mis-time something.
WARNING = allowed by the rules, but worth a look (on-screen time too short, text that wraps, and so on).
"""
import json, math, re, sys

# ------------------------------------------------------------------ fixed facts of version 4
SHOTS = [('s1_register', 9), ('s2a_admit', 6), ('s2b_overview', 4), ('s3_prescribe', 18), ('s4_publish', 6),
         ('s5a_login', 16), ('s5b_meds', 4.5), ('s5c_pharmacy', 6), ('s6_ack', 5), ('s7a_device', 3),
         ('s7b_breathing', 28), ('s8a_request', 14), ('s8b_confirm', 8), ('s8c_confirmed', 4), ('s9a_call', 25),
         ('s9b_nurse', 9), ('s10_branding', 8)]
RAW = dict(SHOTS)
KEYS = [k for k, _ in SHOTS]
PHONE = {'s5a_login', 's5b_meds', 's5c_pharmacy', 's6_ack', 's7a_device', 's7b_breathing', 's8a_request', 's8c_confirmed'}
TRACKER = {'s1_register': 'Doctor', 's2a_admit': 'Admin', 's2b_overview': 'Admin', 's3_prescribe': 'Doctor',
           's4_publish': 'Doctor', 's5a_login': 'Patient', 's5b_meds': 'Patient', 's5c_pharmacy': 'Patient',
           's6_ack': 'Patient', 's7a_device': 'Patient', 's7b_breathing': 'Patient', 's8a_request': 'Patient',
           's8b_confirm': 'Doctor', 's8c_confirmed': 'Patient', 's9a_call': 'Doctor', 's9b_nurse': 'Nurse',
           's10_branding': 'Admin'}
BASE_GROUPS = [['s1_register'], ['s2a_admit', 's2b_overview'], ['s3_prescribe'], ['s4_publish'],
               ['s5a_login', 's5b_meds', 's5c_pharmacy'], ['s6_ack'], ['s7a_device', 's7b_breathing'],
               ['s8a_request', 's8b_confirm', 's8c_confirmed'], ['s9a_call', 's9b_nurse'], ['s10_branding']]
CHIPS = ['PROBLEM SIGNIFICANCE', 'UNDERSTANDING OF USERS', 'INNOVATION', 'SOLUTION QUALITY', 'SOCIAL IMPACT',
         'SUSTAINABILITY / BUSINESS MODEL  ·  SCALABILITY', 'RESPONSIBLE TECHNOLOGY']
CHIPS_SPLIT = ['SUSTAINABILITY / BUSINESS MODEL', 'SCALABILITY']      # allowed if the shared block is split in two
DEMO_CHIP = 'MVP / PROTOTYPE'
IMAGES = {'slide7', 'slide8', 'arch', 'arch_device', 'trust_icmr'}
SLIDE7_TAG = '3D concept render, not built'
ARCH_DEVICE_ZOOM = [0.325, 0.765, 2.3]
ACCENTS = {'teal', 'amber', 'green', 'violet', 'grey'}
STYLES = {'solid', 'dashed'}
PACE = {1: 2.2, 2: 1.9, 3: 2.2}
P1_END = (160, 177); P2_END = (332, 340); VIDEO_END = 355
RATIO = (0.62, 1.5)
LIM = dict(head=48, sub=90, cards=4, card_title=34, card_lines=4, card_line=46, kicker=34, tag=34, big=9,
           steps=5, step_title=16, step_text=44, footer=110, journey=14, scene_sub=44, caption=70,
           phone_title=26, phone_desc=120, call_line=78, nurse_sub=80)
TR = re.compile(r'(\d):(\d\d)–(\d):(\d\d)')                          # the build's own time-range pattern (EN DASH)

ERR, WARN = [], []
def E(msg): ERR.append(msg)
def Wn(msg): WARN.append(msg)
def mmss(s):
    s = float(s); m = int(s // 60); r = s - 60 * m
    return '%d:%02d' % (m, r) if abs(r - round(r)) < 1e-9 else '%d:%05.2f' % (m, r)
def cp(ch): return 'U+%04X' % ord(ch)


# ------------------------------------------------------------------ (a) parse exactly like the build
def parse_blocks(text):
    blocks = []
    for sec in re.split(r'\n(?=### |## Part 3)', text):
        h = sec.split('\n', 1)[0]
        tm = TR.search(h)
        body = ' '.join(l[1:].strip() for l in sec.split('\n') if l.startswith('>')).replace('★', '').strip()
        if tm and body:
            blocks.append(dict(a=int(tm.group(1)) * 60 + int(tm.group(2)), b=int(tm.group(3)) * 60 + int(tm.group(4)),
                               text=re.sub(r'\s+', ' ', body), head=h))
    for b in blocks:
        b['dur'] = b['b'] - b['a']
        b['words'] = len(b['text'].split())                          # same count the build uses for cue timing
        b['spoken'] = len([w for w in re.split(r'[\s\-/]+', b['text']) if re.search(r'\w', w)])   # hyphen parts apart
    return blocks


def read_text(path):
    raw = open(path, 'rb').read()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as ex:
        E('%s is not valid UTF-8 (%s); the build reads it as UTF-8 and would stop' % (path, ex))
        text = raw.decode('utf-8', 'replace')
    return raw, text.replace('\r\n', '\n').replace('\r', '\n')        # what Python's text mode gives the build


# ------------------------------------------------------------------ strict line checks on the narration file
def lint_narration(raw, text):
    if raw.startswith(b'\xef\xbb\xbf'): Wn('narration: file starts with a UTF-8 BOM (harmless to the build; remove it to be safe)')
    if b'\r\n' in raw: Wn('narration: Windows line endings (CRLF); the build copes, other parsers may not')
    lines = text.split('\n')
    head3 = ' '.join(lines[:6])
    for need in ('version 4', '11:30 PM', '12 October 2026'):
        if need.lower() not in head3.lower(): E('narration header: "%s" is missing from the first lines' % need)
    cur = None            # the build section this line falls into: dict(line, head, tm, closed, spoken, screen)
    sections = []
    p3_seen = 0
    for n, ln in enumerate(lines, 1):
        is_head = ln.startswith('### ') or ln.startswith('## Part 3')
        if is_head:
            tm = TR.search(ln)
            cur = dict(line=n, head=ln, tm=tm, closed=False, spoken=0, screen=False); sections.append(cur)
            if ln.startswith('## Part 3'):
                p3_seen += 1
                if not re.match(r'^## Part 3 — Close \(\d:\d\d–\d:\d\d\) · \d+ words$', ln):
                    E('narration line %d: the closing heading must look exactly like "## Part 3 — Close (5:38–5:50) · NN words"; found %r' % (n, ln))
            loose = re.search(r'(\d+):(\d\d)(\s*)(to|[^\w\s]{1,3})(\s*)(\d+):(\d\d)', ln)
            if not tm:
                if loose:
                    why = []
                    if loose.group(4) != '–': why.append('the separator is %r (%s), it must be an EN DASH U+2013' % (loose.group(4), ' '.join(cp(c) for c in loose.group(4))))
                    if loose.group(3) or loose.group(5): why.append('there are spaces around the dash')
                    if len(loose.group(1)) > 1 or len(loose.group(6)) > 1: why.append('minutes have two digits')
                    E('narration line %d: heading time range is not readable by the build (%s); this block would be dropped: %r' % (n, '; '.join(why) or 'bad format', ln))
                else:
                    E('narration line %d: block heading has no time range m:ss–m:ss; this block would be dropped: %r' % (n, ln))
            else:
                s, e = tm.start(), tm.end()
                if (s > 0 and ln[s - 1].isdigit()) or (e < len(ln) and ln[e].isdigit()):
                    E('narration line %d: a time in the heading has too many digits (minutes must be one digit, seconds two); the build would read the wrong time: %r' % (n, ln))
                if int(tm.group(2)) > 59 or int(tm.group(4)) > 59: E('narration line %d: seconds above 59 in %r' % (n, ln))
                a = int(tm.group(1)) * 60 + int(tm.group(2)); b = int(tm.group(3)) * 60 + int(tm.group(4))
                if b <= a: E('narration line %d: the block ends at or before it starts: %r' % (n, ln))
                if len(TR.findall(ln)) > 1 and not ln.startswith('## Part 3'): Wn('narration line %d: more than one time range in the heading; the build uses the first' % n)
            continue
        if ln.startswith('#'):
            if re.match(r'^#{1,6}\s*\d{1,2}:\d\d', ln):
                E('narration line %d: looks like a block heading but does not start with "### " (the build would not split here, so its spoken lines join the block above): %r' % (n, ln))
            if cur is not None: cur['closed'] = True
        elif ln.strip() in ('---', '***', '___'):
            if cur is not None: cur['closed'] = True
        if ln.startswith('**Screen:**') and cur is not None and not cur['closed']: cur['screen'] = True
        if ln.startswith('>'):
            if not ln.startswith('> '): E('narration line %d: a spoken line must start with "> " (a ">" then one space): %r' % (n, ln[:60]))
            if not ln[1:].replace('★', '').strip(): Wn('narration line %d: empty spoken line' % n)
            if cur is None: E('narration line %d: stray ">" line before the first block heading (the build ignores it): %r' % (n, ln[:60]))
            elif not cur['tm']: E('narration line %d: ">" line under a heading with no valid time range (the build drops it): %r' % (n, ln[:60]))
            elif cur['closed']: E('narration line %d: stray ">" line after the end of its block (the build would still add it to "%s"): %r' % (n, cur['head'], ln[:60]))
            else: cur['spoken'] += 1
        elif ln.lstrip(' \t').startswith('>'):
            E('narration line %d: a ">" line is indented, so the build does not read it as spoken text: %r' % (n, ln[:60]))
        if '\t' in ln: Wn('narration line %d: contains a TAB character' % n)
        for ch in ln:
            if ch in '\u200b\u200c\u200d\u2060\ufeff\u00ad' and n > 1: E('narration line %d: invisible character %s (breaks cue matching)' % (n, cp(ch)))
    if p3_seen != 1: E('narration: expected exactly one "## Part 3" heading, found %d' % p3_seen)
    for s in sections:
        if s['tm'] and s['spoken'] == 0: E('narration line %d: heading has a time range but no "> " spoken lines; the build skips it silently: %r' % (s['line'], s['head']))
        if s['tm'] and not s['screen']: Wn('narration line %d: block has no "**Screen:**" line: %r' % (s['line'], s['head']))
    if not re.search(r'^## Never say', text, re.M): E('narration: the "Never say" list is missing')
    if not re.search(r'^## Timing rule', text, re.M): E('narration: the "Timing rule" section with the timing table is missing')
    return lines


def lint_spoken(blocks):
    for b in blocks:
        t = b['text']; where = 'block %s–%s' % (mmss(b['a']), mmss(b['b']))
        dg = re.findall(r'\S*\d\S*', t)
        if dg: E('%s: digits in the spoken text (numbers must be written as words): %s' % (where, ', '.join(dg)))
        md = sorted(set(re.findall(r'[*_`\[\]<>|#\\~]', t)))
        if md: E('%s: markdown or stray symbols inside spoken text %s (they would show on the teleprompter and break cues)' % (where, ' '.join(md)))
        sy = sorted(set(re.findall(r'[%&+=/@→←·•₹$]', t)))
        if sy: Wn('%s: symbols that cannot be read aloud as written: %s' % (where, ' '.join(sy)))
        cq = sorted(set(re.findall(r'[\u2018\u2019\u201c\u201d]', t)))
        if cq: Wn('%s: curly quotes in spoken text (%s); a cue typed with straight quotes will not match' % (where, ' '.join(cp(c) for c in cq)))
        ds = sorted(set(re.findall(r'[\u2012\u2013\u2014\u2212]', t)))
        if ds: Wn('%s: a long dash in spoken text (%s); write a comma or a full stop instead' % (where, ' '.join(cp(c) for c in ds)))
        junk = [w for w in t.split() if not re.search(r'\w', w)]
        if junk: Wn('%s: %d token(s) with no letters are counted as words: %s' % (where, len(junk), ' '.join(junk)))
        for s in re.split(r'(?<=[.!?])\s+', t):
            n = len(s.split())
            if n > 30: Wn('%s: one sentence has %d words (hard to read aloud): "%s..."' % (where, n, ' '.join(s.split()[:8])))


# ------------------------------------------------------------------ spec.json loading with strict checks
def load_spec(path):
    raw, text = read_text(path)
    if raw.startswith(b'\xef\xbb\xbf'):
        E('spec.json starts with a UTF-8 BOM; json.load(open(..., encoding="utf-8")) in the build fails on it'); text = text.lstrip('\ufeff')
    dup = []
    def pairs(p):
        seen = set()
        for k, _ in p:
            if k in seen: dup.append(k)
            seen.add(k)
        return dict(p)
    def const(c): E('spec.json: non-standard number %s (not valid JSON)' % c); return None
    try:
        spec = json.loads(text, object_pairs_hook=pairs, parse_constant=const)
    except json.JSONDecodeError as ex:
        near = text[max(0, ex.pos - 40):ex.pos + 40].replace('\n', '\\n')
        hint = ''
        if re.search(r'[\u201c\u201d\u2018\u2019]', near): hint = ' (there is a smart quote here; JSON needs straight ")'
        elif re.search(r',\s*[\]}]', text[max(0, ex.pos - 3):ex.pos + 3]): hint = ' (looks like a trailing comma)'
        E('spec.json is not valid JSON: %s at line %d column %d, near %r%s' % (ex.msg, ex.lineno, ex.colno, near, hint))
        return None
    for k in dup: E('spec.json: the key "%s" appears twice in one object (the second silently wins)' % k)
    if '\t' in text: Wn('spec.json: contains TAB characters')
    return spec


class Spec:
    """Walks spec.json, records every text field with its path, and validates shapes and limits."""
    def __init__(self): self.texts = []                              # (path, string) of everything drawn on screen

    def s(self, o, key, path, limit=None, nullable=False, required=True, lines=None, line_limit=None):
        p = '%s.%s' % (path, key)
        if not isinstance(o, dict) or key not in o:
            if required and not nullable: E('%s is missing' % p)
            return None
        v = o[key]
        if v is None:
            if not nullable: E('%s must be text, not null' % p)
            return None
        if not isinstance(v, str): E('%s must be text, found %s' % (p, type(v).__name__)); return None
        if not v.strip() and not nullable and required: E('%s is empty' % p)
        self.texts.append((p, v))
        if limit is not None and len(v) > limit:
            E('%s is %d characters, the limit is %d (cut %d): %r' % (p, len(v), limit, len(v) - limit, v))
        if lines is not None:
            parts = v.split('\n')
            if len(parts) > lines: E('%s has %d lines, the limit is %d: %r' % (p, len(parts), lines, v))
            if line_limit:
                for i, x in enumerate(parts):
                    if len(x) > line_limit: E('%s line %d is %d characters, the limit is %d (cut %d): %r' % (p, i + 1, len(x), line_limit, len(x) - line_limit, x))
        elif '\n' in v and key not in ('text', 'source'):
            Wn('%s contains a line break; this field is drawn as one line' % p)
        return v

    def keys(self, o, allowed, path):
        if isinstance(o, dict):
            for k in o:
                if k not in allowed: Wn('%s has an unknown key "%s" (a typing mistake? the build ignores it)' % (path, k))

    def cue(self, o, key, path, out, required_key=False):
        p = '%s.%s' % (path, key)
        if not isinstance(o, dict) or key not in o:
            if required_key: Wn('%s is missing (treated as null)' % p)
            return
        v = o[key]
        if v is None: return
        if not isinstance(v, str) or not v.strip(): E('%s must be a phrase or null, found %r' % (p, v)); return
        if v != v.strip(): Wn('%s has a space at its start or end: %r' % (p, v))
        out.append((p, v))

    def graphic(self, g, path, first_in_block, very_first):
        """Returns the ordered list of (path, phrase) cues of this graphic, and its own cue entry (or None)."""
        cues = []
        if not isinstance(g, dict): E('%s must be an object' % path); return cues, None
        t = g.get('type')
        own = []
        if t != 'title': self.cue(g, 'cue', path, own, required_key=True)
        elif g.get('cue') is not None: E('%s.cue: a title graphic takes no cue' % path)
        if first_in_block and own: E('%s.cue must be null: the first graphic of a block starts with the block (found %r)' % (path, own[0][1]))
        if not first_in_block and not own and t != 'title': Wn('%s.cue is null: a later graphic should name the phrase it appears on (the build would guess the time)' % path)
        cues += own
        if t == 'title':
            if not very_first: E('%s: the "title" graphic is only allowed as the very first graphic of the video' % path)
            self.keys(g, {'type', 'cue', 'name', 'line1', 'line2', 'pill1', 'pill2', 'team', 'foot'}, path)
            for k in ('name', 'line1', 'line2', 'pill1', 'pill2', 'team', 'foot'): self.s(g, k, path)
        elif t == 'stats':
            self.keys(g, {'type', 'cue', 'head', 'cards', 'footer', 'footer_cue'}, path)
            self.s(g, 'head', path, LIM['head'])
            cs = g.get('cards')
            if not isinstance(cs, list) or len(cs) != 3: E('%s.cards must hold exactly 3 cards, found %s' % (path, len(cs) if isinstance(cs, list) else type(cs).__name__)); cs = cs if isinstance(cs, list) else []
            for i, c in enumerate(cs):
                cpth = '%s.cards[%d]' % (path, i)
                self.keys(c, {'big', 'text', 'source', 'cue'}, cpth)
                self.s(c, 'big', cpth, LIM['big']); self.s(c, 'text', cpth, lines=2); self.s(c, 'source', cpth, lines=2)
                self.cue(c, 'cue', cpth, cues, required_key=True)
            self.s(g, 'footer', path, LIM['footer'])
            self.cue(g, 'footer_cue', path, cues, required_key=True)
        elif t == 'cards':
            self.keys(g, {'type', 'cue', 'head', 'sub', 'cards', 'footer', 'footer_cue'}, path)
            self.s(g, 'head', path, LIM['head']); self.s(g, 'sub', path, LIM['sub'], nullable=True)
            cs = g.get('cards')
            if not isinstance(cs, list) or not cs: E('%s.cards must be a list with 1 to 4 cards' % path); cs = []
            if len(cs) > LIM['cards']: E('%s has %d cards, the limit is %d' % (path, len(cs), LIM['cards']))
            for i, c in enumerate(cs):
                cpth = '%s.cards[%d]' % (path, i)
                if not isinstance(c, dict): E('%s must be an object' % cpth); continue
                self.keys(c, {'kicker', 'title', 'lines', 'tag', 'accent', 'style', 'big', 'cue'}, cpth)
                self.s(c, 'kicker', cpth, LIM['kicker'], nullable=True); self.s(c, 'title', cpth, LIM['card_title'])
                self.s(c, 'tag', cpth, LIM['tag'], nullable=True); self.s(c, 'big', cpth, LIM['big'], nullable=True)
                ls = c.get('lines')
                if not isinstance(ls, list): E('%s.lines must be a list of text lines' % cpth); ls = []
                if len(ls) > LIM['card_lines']: E('%s has %d lines, the limit is %d' % (cpth, len(ls), LIM['card_lines']))
                for j, x in enumerate(ls):
                    if not isinstance(x, str): E('%s.lines[%d] must be text' % (cpth, j)); continue
                    self.texts.append(('%s.lines[%d]' % (cpth, j), x))
                    if len(x) > LIM['card_line']: E('%s.lines[%d] is %d characters, the limit is %d (cut %d): %r' % (cpth, j, len(x), LIM['card_line'], len(x) - LIM['card_line'], x))
                    if '\n' in x: E('%s.lines[%d] contains a line break; use a separate entry in "lines"' % (cpth, j))
                if c.get('accent') not in ACCENTS: E('%s.accent must be one of %s, found %r' % (cpth, sorted(ACCENTS), c.get('accent')))
                if c.get('style') not in STYLES: E('%s.style must be "solid" or "dashed", found %r' % (cpth, c.get('style')))
                self.cue(c, 'cue', cpth, cues)
            self.s(g, 'footer', path, LIM['footer'], nullable=True)
            self.cue(g, 'footer_cue', path, cues)
            if g.get('footer_cue') and not g.get('footer'): E('%s.footer_cue is set but there is no footer' % path)
        elif t == 'strip':
            self.keys(g, {'type', 'cue', 'head', 'steps', 'footer'}, path)
            self.s(g, 'head', path, LIM['head'])
            st = g.get('steps')
            if not isinstance(st, list) or not st: E('%s.steps must be a list with 1 to 5 steps' % path); st = []
            if len(st) > LIM['steps']: E('%s has %d steps, the limit is %d' % (path, len(st), LIM['steps']))
            for i, x in enumerate(st):
                spth = '%s.steps[%d]' % (path, i)
                self.keys(x, {'title', 'text', 'cue'}, spth)
                self.s(x, 'title', spth, LIM['step_title']); self.s(x, 'text', spth, LIM['step_text'])
                self.cue(x, 'cue', spth, cues)
            self.s(g, 'footer', path, LIM['footer'], nullable=True)
        elif t == 'image':
            self.keys(g, {'type', 'cue', 'img', 'tag', 'zoom'}, path)
            img = g.get('img')
            if img not in IMAGES: E('%s.img must be one of %s, found %r' % (path, sorted(IMAGES), img))
            tag = self.s(g, 'tag', path, LIM['tag'], nullable=True)
            if img == 'slide7' and tag != SLIDE7_TAG: E('%s: slide7 must carry the tag "%s", found %r' % (path, SLIDE7_TAG, tag))
            z = g.get('zoom')
            if z is not None:
                ok = isinstance(z, list) and len(z) == 3 and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in z)
                if not ok: E('%s.zoom must be null or [cx, cy, z] with three numbers, found %r' % (path, z))
                elif not (0 <= z[0] <= 1 and 0 <= z[1] <= 1 and z[2] >= 1): E('%s.zoom: cx and cy must be between 0 and 1 and z at least 1, found %r' % (path, z))
            if img == 'arch_device' and z != ARCH_DEVICE_ZOOM: E('%s: arch_device must use zoom %s, found %r' % (path, ARCH_DEVICE_ZOOM, z))
        else:
            E('%s.type must be title, stats, cards, strip or image; found %r' % (path, t))
        return cues, (own[0] if own else None)


TIME = re.compile(r'^\d:\d\d$')
def tsec(v, path):
    if not isinstance(v, str) or not TIME.match(v) or int(v[2:]) > 59:
        E('%s must be a time written m:ss (one digit, a colon, two digits), found %r' % (path, v)); return None
    return int(v[0]) * 60 + int(v[2:])


def cue_time(block, phrase):
    """The build's rule: first match, case-insensitive; time is proportional to the words before it."""
    low = block['text'].lower(); i = low.find(phrase.lower())
    if i < 0: return None, -1
    return block['a'] + block['dur'] * len(low[:i].split()) / max(len(block['text'].split()), 1), i


def norm(s):
    for a, b in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"'), ('\u2013', '-'), ('\u2014', '-'), ('\u00a0', ' ')):
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip().lower()


def check_cues(cues, block, where):
    """Each cue must be found in its own block, and cues must come in speaking order. Returns {path: time}."""
    times = {}; prev = None
    if block is None: return times
    low = block['text'].lower()
    for path, ph in cues:
        t, i = cue_time(block, ph)
        if t is None:
            why = ''
            if norm(ph) in norm(block['text']): why = ' (it differs only in quote marks, dashes or spacing: copy the words straight from the narration)'
            elif re.sub(r'[^\w ]', '', norm(ph)) in re.sub(r'[^\w ]', '', norm(block['text'])): why = ' (the words are there, but the punctuation between them is different)'
            else:
                ws = ph.split(); k = len(ws)
                while k > 0 and ' '.join(ws[:k]).lower() not in low: k -= 1
                why = ' (matches only as far as %r)' % ' '.join(ws[:k]) if k else ' (not even its first word is in this block)'
            E('%s: cue %r is not in the spoken text of %s%s' % (path, ph, where, why)); continue
        times[path] = t
        if low.count(ph.lower()) > 1: Wn('%s: cue %r occurs %d times in %s; the build uses the first one' % (path, ph, low.count(ph.lower()), where))
        j = i + len(ph)
        if (i > 0 and low[i - 1].isalnum() and ph[0].isalnum()) or (j < len(low) and low[j].isalnum() and ph[-1].isalnum()):
            Wn('%s: cue %r starts or ends in the middle of a word in %s' % (path, ph, where))
        if prev is not None:
            if i < prev[1]: E('%s: cue %r is spoken BEFORE the earlier cue %r (%s); cues must be in speaking order' % (path, ph, prev[2], prev[0]))
        prev = (path, i, ph) if prev is None or i >= prev[1] else prev
    return times


# ------------------------------------------------------------------ optional: measure text with the build's own fonts
def render_fit(spec):
    try:
        from PIL import Image, ImageDraw, ImageFont
        FD = 'C:/Windows/Fonts/'
        def F(size, w='r'): return ImageFont.truetype(FD + {'r': 'segoeui.ttf', 'b': 'segoeuib.ttf', 's': 'seguisb.ttf', 'l': 'segoeuil.ttf'}[w], size)
        F(20)
    except Exception as ex:
        print('\n(render-fit checks skipped: %s)' % ex); return
    D0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    def tw(text, font): b = D0.textbbox((0, 0), text, font=font); return b[2] - b[0]
    def th(text, font): b = D0.textbbox((0, 0), text, font=font); return b[3] - b[1]
    def wrap_px(text, font, w):                                       # copied from build_v4.py
        out = []
        for para in text.split('\n'):
            cur = ''
            for word in para.split():
                trial = (cur + ' ' + word).strip()
                if tw(trial, font) <= w or not cur: cur = trial
                else: out.append(cur); cur = word
            out.append(cur)
        return out
    def fit(text, w, size, weight='b', min_size=18):
        while size > min_size and tw(text, F(size, weight)) > w: size -= 2
        return size
    def pill_w(text, font, padx): return tw(text, font) + 2 * padx
    try:
        for bi, blk in enumerate(spec.get('part1') or []):
            for gi, g in enumerate(blk.get('graphics') or []):
                if not isinstance(g, dict) or g.get('type') != 'stats': continue
                p = 'part1[%d].graphics[%d]' % (bi, gi); cs = g.get('cards') or []; n = max(len(cs), 1); cw = (1620 - 40 * (n - 1)) // n
                for i, c in enumerate(cs):
                    tl = wrap_px(str(c.get('text') or ''), F(36, 's'), cw - 80); sl = wrap_px(str(c.get('source') or ''), F(23), cw - 80)
                    if len(tl) > 4: E('%s.cards[%d].text wraps to %d lines in its %d px card; the build draws only 4, so %r is cut off' % (p, i, len(tl), cw, ' / '.join(tl[4:])))
                    if len(sl) > 4: E('%s.cards[%d].source wraps to %d lines; the build draws only 4, so %r is cut off' % (p, i, len(sl), ' / '.join(sl[4:])))
                    gap = (524 - 32 * min(len(sl), 4)) - (210 + 48 * min(len(tl), 4))
                    if gap < 8: Wn('%s.cards[%d]: the text (%d drawn lines) and the source (%d drawn lines) nearly touch or overlap inside the card (gap %d px); shorten one of them by a line' % (p, i, min(len(tl), 4), min(len(sl), 4), gap))
                    bs = fit(str(c.get('big') or ''), cw - 80, 104)
                    if bs < 80: Wn('%s.cards[%d].big %r is shrunk to %d px to fit (104 px is the design size)' % (p, i, c.get('big'), bs))
                if g.get('footer') and len(wrap_px(g['footer'], F(30, 's'), 1600)) > 2: E('%s.footer wraps to more than 2 lines; the build draws only 2' % p)
        demo = spec.get('demo') or {}
        right = 'Live site  ·  spirobuddy.onrender.com  ·  fictional patients'; rw = tw(right, F(21))
        for si, sc in enumerate(demo.get('scenes') or []):
            for hi, sh in enumerate(sc.get('shots') or []):
                p = 'demo.scenes[%d].shots[%d] (%s)' % (si, hi, sh.get('key')); tag = sh.get('tag')
                phone = sh.get('key') in PHONE or sh.get('key') == 's9a_call'
                if not phone and isinstance(sh.get('caption'), str):
                    cx = 166 + ((pill_w(tag, F(22, 'b'), 14) + 14) if tag else 0); avail = W_ - 40 - rw - cx - 30
                    size = fit(sh['caption'], avail, 28, 's')
                    if tw(sh['caption'], F(size, 's')) > avail: E('%s: the caption does not fit beside its tag even at the smallest size (%d px wide, %d px free)' % (p, tw(sh['caption'], F(size, 's')), avail))
                    elif size < 24: Wn('%s: the caption is shrunk to %d px to fit beside its tag (28 px is the design size); shorten the caption or the tag' % (p, size))
                if phone:
                    title = sh.get('phone_title') or sc.get('sub') or ''; desc = sh.get('phone_desc') or sh.get('caption') or ''
                    tl = wrap_px(title, F(56, 'b'), 900); dl = wrap_px(desc, F(32, 'l'), 900)
                    if len(tl) > 1: Wn('%s: the big phone title wraps to %d lines: %r' % (p, len(tl), ' / '.join(tl)))
                    bottom = 250 + 72 * len(tl) + 18 + 46 * len(dl) + (26 + th(tag, F(24, 'b')) + 18 if tag else 0)
                    if sh.get('key') == 's9a_call':
                        y = max(bottom + 40, 600)
                        for i, s in enumerate((demo.get('call_subs') or [])[:3]):
                            s2 = str(s).replace('{missed}', '10'); ls = [l for para in s2.split('\n') for l in wrap_px(para, F(29, 's'), 940 - 48)]
                            if len(ls) != len(s2.split('\n')): Wn('demo.call_subs[%d]: the subtitle box is 892 px wide, so it is drawn as %d lines, not %d: %s' % (i, len(ls), len(s2.split('\n')), ' / '.join(ls)))
                            if y + 43 * len(ls) + 28 > 1030: E('demo.call_subs[%d]: drawn %d lines tall, it runs off the bottom of the frame' % (i, len(ls)))
                    elif bottom > 1010: E('%s: the phone text block is too tall for the frame' % p)
        ns = demo.get('nurse_sub')
        if isinstance(ns, str):
            ls = wrap_px(ns, F(30, 's'), 1300 - 48)
            if len(ls) > 1: Wn('demo.nurse_sub wraps to %d lines in its 1252 px box: %s' % (len(ls), ' / '.join(ls)))
        # glyphs the font does not have are drawn as an empty box
        f = F(40, 's'); nd = f.getmask('\uffff'); ndb = (nd.size, bytes(nd))
        return lambda ch: (lambda m: (m.size, bytes(m)) == ndb)(f.getmask(ch))
    except Exception as ex:
        Wn('render-fit checks stopped early: %r' % ex)
    return None
W_ = 1920


# ------------------------------------------------------------------ main
def main():
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
    if len(sys.argv) != 3:
        print(__doc__); return 2
    raw, text = read_text(sys.argv[1])
    lines = lint_narration(raw, text)
    blocks = parse_blocks(text)
    lint_spoken(blocks)
    spec = load_spec(sys.argv[2])
    if not blocks: E('narration: no spoken blocks were found')

    # ---------- split the blocks into Part 1 / Part 2 / Part 3 (Part 2 = the blocks that belong to spec demo.scenes)
    sp = Spec()
    p2a = p2b = None
    scenes = []
    if isinstance(spec, dict):
        d = spec.get('demo') if isinstance(spec.get('demo'), dict) else {}
        scenes = d.get('scenes') if isinstance(d.get('scenes'), list) else []
        ts = [(tsec(s.get('start'), 'demo.scenes[%d].start' % i), tsec(s.get('end'), 'demo.scenes[%d].end' % i)) for i, s in enumerate(scenes) if isinstance(s, dict)]
        ts = [t for t in ts if None not in t]
        if ts: p2a, p2b = ts[0][0], ts[-1][1]
    if p2a is None:
        m = re.search(r'^## Part 2[^\n]*?\((\d):(\d\d)–(\d):(\d\d)\)', text, re.M)
        if m: p2a = int(m.group(1)) * 60 + int(m.group(2)); p2b = int(m.group(3)) * 60 + int(m.group(4)); Wn('Part 2 limits taken from the narration heading because spec demo.scenes could not be read')
    for b in blocks:
        b['part'] = 1 if (p2a is None or b['a'] < p2a) else (2 if b['b'] <= p2b else 3)
    P1 = [b for b in blocks if b['part'] == 1]; P2 = [b for b in blocks if b['part'] == 2]; P3 = [b for b in blocks if b['part'] == 3]

    # ---------- (b) timeline
    if blocks:
        if blocks[0]['a'] != 0: E('timeline: the first block starts at %s, it must start at 0:00' % mmss(blocks[0]['a']))
        for p, q in zip(blocks, blocks[1:]):
            if q['a'] != p['b']:
                E('timeline: %s between the block ending %s and the block starting %s; blocks must touch (headings: %r -> %r)' % ('a gap of %d s' % (q['a'] - p['b']) if q['a'] > p['b'] else 'an overlap of %d s' % (p['b'] - q['a']), mmss(p['b']), mmss(q['a']), p['head'], q['head']))
        if P1 and not (P1_END[0] <= P1[-1]['b'] <= P1_END[1]): E('timeline: Part 1 ends at %s; it must end between %s and %s' % (mmss(P1[-1]['b']), mmss(P1_END[0]), mmss(P1_END[1])))
        if not P1: E('timeline: no Part 1 blocks found')
        if P2 and not (P2_END[0] <= P2[-1]['b'] <= P2_END[1]): E('timeline: Part 2 ends at %s; it must end between 5:32 and 5:40' % mmss(P2[-1]['b']))
        if not P2: E('timeline: no Part 2 blocks found (none match spec demo.scenes)')
        if blocks[-1]['b'] > VIDEO_END: E('timeline: the last block ends at %s; it must end at or before %s' % (mmss(blocks[-1]['b']), mmss(VIDEO_END)))
        if len(P3) != 1: E('timeline: expected exactly one closing block after Part 2, found %d' % len(P3))
        elif not P3[0]['head'].startswith('## Part 3'): E('timeline: the last block is not the "## Part 3" block: %r' % P3[0]['head'])

    # ---------- (c) the table
    print('%-5s %-5s %4s %5s %5s  %-6s %5s  %s' % ('start', 'end', 'sec', 'words', 'w/s', 'limit', 'room', 'block'))
    for b in blocks:
        lim = PACE[b['part']]; pace = b['words'] / b['dur'] if b['dur'] > 0 else float('inf')
        maxw = int(math.floor(lim * b['dur'] + 1e-9)); over = b['words'] - maxw
        flag = ''
        if over > 0:
            need = int(math.ceil(b['words'] / lim - 1e-9)) - b['dur']
            flag = '  <-- TOO FAST'
            E('pace: block %s–%s "%s" has %d words in %d s = %.2f words a second, above the Part %d limit of %.1f. Cut %d word(s), or give it %d more second(s)'
              % (mmss(b['a']), mmss(b['b']), re.sub(r'^#+ ', '', b['head'])[:50], b['words'], b['dur'], pace, b['part'], lim, over, need))
        name = re.sub(r'^#+\s*', '', b['head']); name = re.sub(r'^\d:\d\d–\d:\d\d\s*·\s*', '', name)
        print('%-5s %-5s %4d %5d %5.2f  P%d %-3.1f %+5d  %s%s' % (mmss(b['a']), mmss(b['b']), b['dur'], b['words'], pace, b['part'], lim, maxw - b['words'], name[:46], flag))
        if b['spoken'] != b['words'] and b['spoken'] > lim * b['dur'] + 1e-9 and over <= 0:
            Wn('pace: block %s–%s is inside the limit only because hyphenated words count as one: said aloud it is %d words in %d s = %.2f a second (limit %.1f)'
               % (mmss(b['a']), mmss(b['b']), b['spoken'], b['dur'], b['spoken'] / b['dur'], lim))
    for part, name in ((P1, 'Part 1'), (P2, 'Part 2'), (P3, 'Part 3')):
        if part:
            w = sum(b['words'] for b in part); s = part[-1]['b'] - part[0]['a']
            print('%s: %s–%s  %d s  %d words  %.2f words a second  (%d blocks)' % (name, mmss(part[0]['a']), mmss(part[-1]['b']), s, w, w / s if s else 0, len(part)))
    print('("room" = how many more words fit before the pace limit; negative = words to cut)')

    # ---------- the narration's own numbers (Part headings and the timing table)
    for part, n in ((P1, 1), (P2, 2), (P3, 3)):
        m = re.search(r'^## Part %d[^\n]*?\((\d):(\d\d)–(\d):(\d\d)\) · (\d+) (?:spoken )?words' % n, text, re.M)
        if not m: E('narration: the "## Part %d — ... (m:ss–m:ss) · NN words" heading is missing or malformed' % n); continue
        if not part: continue
        a = int(m.group(1)) * 60 + int(m.group(2)); b = int(m.group(3)) * 60 + int(m.group(4)); w = sum(x['words'] for x in part)
        if (a, b) != (part[0]['a'], part[-1]['b']): E('narration: the Part %d heading says %s–%s but its blocks run %s–%s' % (n, mmss(a), mmss(b), mmss(part[0]['a']), mmss(part[-1]['b'])))
        if int(m.group(5)) != w: E('narration: the Part %d heading says %s words; the blocks hold %d' % (n, m.group(5), w))
    rows = re.findall(r'^\|\s*([^|\n]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+\.\d+)\s*\|\s*$', text, re.M)
    if not rows: E('narration: the timing table (Block | Seconds | Words | Words a second) is missing')
    elif len(rows) != len(blocks): E('narration: the timing table has %d rows but there are %d blocks' % (len(rows), len(blocks)))
    else:
        for r, b in zip(rows, blocks):
            want = (b['dur'], b['words'], '%.2f' % (b['words'] / b['dur']))
            if (int(r[1]), int(r[2]), r[3]) != want: E('narration: timing table row "%s" says %s s, %s words, %s; the block has %d s, %d words, %s' % ((r[0], r[1], r[2], r[3]) + want))
    for name, part in (('Part 1', P1), ('Part 2', P2), ('Part 3', P3)):
        m = re.search(r'^\|\s*%s[^|\n]*\|\s*(\d):(\d\d)\s*\|' % name, text, re.M)
        if m and part and int(m.group(1)) * 60 + int(m.group(2)) != part[-1]['b'] - part[0]['a']:
            E('narration: the summary table gives %s a target of %s:%s but its blocks add up to %s' % (name, m.group(1), m.group(2), mmss(part[-1]['b'] - part[0]['a'])))
    m = re.search(r'^\|\s*\*\*Total\*\*\s*\|\s*\*\*(?:about )?(\d):(\d\d)', text, re.M)
    if m and blocks and int(m.group(1)) * 60 + int(m.group(2)) != blocks[-1]['b']: E('narration: the summary table total says %s:%s but the last block ends at %s' % (m.group(1), m.group(2), mmss(blocks[-1]['b'])))

    # ---------- (d) spec.json
    sync = []                                                        # (text for the sync table)
    if isinstance(spec, dict):
        sp.keys(spec, {'version', 'part1', 'demo', 'outro'}, 'spec')
        if spec.get('version') != 4: E('spec.version must be 4, found %r' % spec.get('version'))
        part1 = spec.get('part1')
        if not isinstance(part1, list) or not part1: E('spec.part1 must be a list with one entry per Part 1 block'); part1 = []
        if len(part1) != len(P1): E('spec.part1 has %d entries but the narration has %d Part 1 blocks; they must match one to one' % (len(part1), len(P1)))
        used_chips = []
        for i, e in enumerate(part1):
            p = 'part1[%d]' % i
            if not isinstance(e, dict): E('%s must be an object' % p); continue
            sp.keys(e, {'start', 'end', 'chip', 'graphics'}, p)
            a, b = tsec(e.get('start'), p + '.start'), tsec(e.get('end'), p + '.end')
            blk = P1[i] if i < len(P1) else None
            if blk is not None and None not in (a, b) and (a, b) != (blk['a'], blk['b']):
                E('%s is %s–%s but Part 1 narration block %d is %s–%s (%r)' % (p, e.get('start'), e.get('end'), i + 1, mmss(blk['a']), mmss(blk['b']), blk['head'])); blk = next((x for x in P1 if (x['a'], x['b']) == (a, b)), blk)
            chip = e.get('chip'); used_chips.append(chip)
            if chip not in CHIPS and chip not in CHIPS_SPLIT: E('%s.chip %r is not an official criterion name (%s)' % (p, chip, ' | '.join(CHIPS)))
            elif blk is not None and norm(chip) not in norm(blk['head']): Wn('%s.chip %r is not the name in the narration heading %r' % (p, chip, blk['head']))
            gs = e.get('graphics')
            if not isinstance(gs, list) or not gs: E('%s.graphics must be a list with at least one graphic' % p); continue
            cues = []; own = []
            for gi, g in enumerate(gs):
                c, o = sp.graphic(g, '%s.graphics[%d]' % (p, gi), gi == 0, i == 0 and gi == 0)
                cues += c; own.append(o)
            times = check_cues(cues, blk, 'block %s–%s' % (e.get('start'), e.get('end')))
            if blk is None or None in (a, b): continue
            # when each graphic is on screen (the build's rule), and how long each cued item stays visible
            starts = [float(a)] + [times.get(o[0]) if o else None for o in own[1:]]
            for k in range(1, len(starts)):
                if starts[k] is None: starts[k] = starts[k - 1] + (b - starts[k - 1]) / (len(gs) - k + 1)
            ends = starts[1:] + [float(b)]
            for gi, g in enumerate(gs):
                gp = '%s.graphics[%d]' % (p, gi); dur = ends[gi] - starts[gi]; kind = g.get('type') if isinstance(g, dict) else '?'
                chars = sum(len(v) for pth, v in sp.texts if pth.startswith(gp + '.') and not pth.endswith('.source'))
                sync.append('  %-5s–%-7s %5.1f s  %-6s %4d chars  %s' % (mmss(round(starts[gi], 2)), mmss(round(ends[gi], 2)), dur, kind, chars, gp + (' (%s)' % g.get('img') if kind == 'image' else '')))
                if dur < 3.0: Wn('sync: %s (%s) is on screen for only %.1f s (from %s to %s)%s' % (gp, kind, dur, mmss(round(starts[gi], 2)), mmss(round(ends[gi], 2)), '; its cue comes too soon after the block starts' if gi == 0 else ''))
                elif kind in ('cards', 'stats', 'strip') and chars / dur > 26: Wn('sync: %s shows %d characters of text for %.1f s (%.0f a second; a viewer reads about 15 to 20)' % (gp, chars, dur, chars / dur))
                for pth, ph in cues:
                    if pth.startswith(gp + '.') and not pth.endswith('graphics[%d].cue' % gi) and pth in times:
                        rel = min(max(times[pth] - starts[gi], 0.1), max(dur - 0.6, 0.1)); vis = dur - rel
                        if times[pth] >= ends[gi] - 1e-9: E('sync: %s (cue %r) is spoken after its graphic has already been replaced, so it never properly appears' % (pth, ph))
                        elif vis < 2.0: Wn('sync: %s (cue %r) appears only %.1f s before its graphic is replaced' % (pth, ph, vis))
        for c in CHIPS:
            if c not in used_chips and not (c == CHIPS[5] and all(x in used_chips for x in CHIPS_SPLIT)): Wn('spec.part1: no block carries the chip "%s"' % c)

        # ---- demo
        d = spec.get('demo')
        if not isinstance(d, dict): E('spec.demo must be an object'); d = {}
        sp.keys(d, {'chip', 'journey', 'scenes', 'call_subs', 'nurse_sub'}, 'demo')
        if d.get('chip') != DEMO_CHIP: E('demo.chip must be "%s", found %r' % (DEMO_CHIP, d.get('chip')))
        j = d.get('journey')
        if not isinstance(j, list) or len(j) != 5: E('demo.journey must hold five step names, found %r' % (len(j) if isinstance(j, list) else j)); j = j if isinstance(j, list) else []
        for i, x in enumerate(j):
            if not isinstance(x, str): E('demo.journey[%d] must be text' % i)
            else:
                sp.texts.append(('demo.journey[%d]' % i, x))
                if len(x) > LIM['journey']: E('demo.journey[%d] is %d characters, the limit is %d: %r' % (i, len(x), LIM['journey'], x))
        if not scenes: E('demo.scenes must be a list with one entry per Part 2 block')
        if len(scenes) != len(P2): E('demo.scenes has %d entries but the narration has %d Part 2 blocks; they must match one to one' % (len(scenes), len(P2)))
        seen = []; groups = []
        print('\nPart 2 scenes (length against the recorded footage; allowed %.2f to %.2f):' % RATIO)
        for i, sc in enumerate(scenes):
            p = 'demo.scenes[%d]' % i
            if not isinstance(sc, dict): E('%s must be an object' % p); continue
            sp.keys(sc, {'start', 'end', 'sub', 'journey_step', 'shots'}, p)
            a, b = tsec(sc.get('start'), p + '.start'), tsec(sc.get('end'), p + '.end')
            blk = P2[i] if i < len(P2) else None
            if blk is not None and None not in (a, b) and (a, b) != (blk['a'], blk['b']):
                E('%s is %s–%s but Part 2 narration block %d is %s–%s (%r)' % (p, sc.get('start'), sc.get('end'), i + 1, mmss(blk['a']), mmss(blk['b']), blk['head'])); blk = next((x for x in P2 if (x['a'], x['b']) == (a, b)), blk)
            sp.s(sc, 'sub', p, LIM['scene_sub'])
            js = sc.get('journey_step')
            if not isinstance(js, int) or isinstance(js, bool) or not (0 <= js <= 4): E('%s.journey_step must be a whole number 0 to 4, found %r' % (p, js))
            shots = sc.get('shots')
            if not isinstance(shots, list) or not shots: E('%s.shots must be a list with at least one shot' % p); continue
            ks = []
            for hi, sh in enumerate(shots):
                hp = '%s.shots[%d]' % (p, hi)
                if not isinstance(sh, dict): E('%s must be an object' % hp); continue
                k = sh.get('key'); ks.append(k)
                if k not in RAW: E('%s.key %r is not a known shot (%s)' % (hp, k, ', '.join(KEYS))); continue
                hp += ' (%s)' % k
                sp.keys(sh, {'key', 'tracker', 'tag', 'phone_title', 'phone_desc'} if k in PHONE else {'key', 'tracker', 'tag', 'caption'}, hp)
                if sh.get('tracker') not in ('Doctor', 'Patient', 'Admin', 'Nurse'): E('%s.tracker must be Doctor, Patient, Admin or Nurse, found %r' % (hp, sh.get('tracker')))
                elif sh['tracker'] != TRACKER[k]: E('%s.tracker is %r but this shot is on the %s screen' % (hp, sh['tracker'], TRACKER[k]))
                if k in PHONE:
                    sp.s(sh, 'phone_title', hp, LIM['phone_title']); sp.s(sh, 'phone_desc', hp, LIM['phone_desc'])
                    if 'caption' in sh: E('%s: a patient-phone shot uses phone_title and phone_desc, not caption' % hp)
                else:
                    sp.s(sh, 'caption', hp, LIM['caption'])
                    if 'phone_title' in sh or 'phone_desc' in sh: E('%s: a doctor, admin or nurse shot uses caption, not phone_title or phone_desc' % hp)
                if 'tag' not in sh: Wn('%s.tag is missing (treated as null)' % hp)
                sp.s(sh, 'tag', hp, LIM['tag'], nullable=True)
            seen += ks; groups.append(ks)
            if None not in (a, b) and all(k in RAW for k in ks):
                rawsum = sum(RAW[k] for k in ks); dur = b - a; r = dur / rawsum
                lo, hi = int(math.ceil(RATIO[0] * rawsum - 1e-9)), int(math.floor(RATIO[1] * rawsum + 1e-9))
                bad = not (RATIO[0] - 1e-9 <= r <= RATIO[1] + 1e-9)
                print('  %-5s–%-5s %3d s  footage %5.1f s  ratio %.2f  (allowed %d to %d s)%s  %s' % (sc.get('start'), sc.get('end'), dur, rawsum, r, lo, hi, '  <-- OUT OF RANGE' if bad else '', '+'.join(ks)))
                if bad: E('%s (%s): the scene is %d s for %.1f s of footage (ratio %.2f); it must be %d to %d s long, so %s it by at least %d s' % (p, '+'.join(ks), dur, rawsum, r, lo, hi, 'lengthen' if r < RATIO[0] else 'shorten', (lo - dur) if r < RATIO[0] else (dur - hi)))
                if blk is not None:                                   # which words are spoken while each shot is on screen
                    words = blk['text'].split(); t = float(a)
                    for k in ks:
                        t2 = t + dur * RAW[k] / rawsum
                        i1 = int(round((t - a) / dur * len(words))); i2 = int(round((t2 - a) / dur * len(words)))
                        said = ' '.join(words[i1:i2])
                        print('      %-13s %s–%s (%4.1f s)  "%s"' % (k, mmss(round(t, 1)), mmss(round(t2, 1)), t2 - t, said if len(said) < 96 else said[:46] + ' ... ' + said[-44:]))
                        t = t2
        if seen != KEYS:
            miss = [k for k in KEYS if k not in seen]; dupes = sorted({k for k in seen if seen.count(k) > 1 and k in RAW})
            if miss: E('demo.scenes: these shots are never used: %s' % ', '.join(miss))
            if dupes: E('demo.scenes: these shots are used more than once: %s' % ', '.join(dupes))
            if not miss and not dupes: E('demo.scenes: the shots are not in care order; found %s, expected %s' % (' '.join(str(k) for k in seen), ' '.join(KEYS)))
        else:
            allowed = []
            for m34 in (False, True):
                for m56 in (False, True):
                    g = [list(x) for x in BASE_GROUPS]
                    if m56: g[4:6] = [g[4] + g[5]]
                    if m34: g[2:4] = [g[2] + g[3]]
                    allowed.append(g)
            if groups not in allowed: E('demo.scenes: the shots are not grouped as the ten slots allow (only slot 4 may join slot 3, and slot 6 may join slot 5); found %s' % ' | '.join('+'.join(g) for g in groups))
        cs = d.get('call_subs')
        if not isinstance(cs, list) or len(cs) != 3: E('demo.call_subs must hold exactly three subtitle strings, found %r' % (len(cs) if isinstance(cs, list) else cs)); cs = cs if isinstance(cs, list) else []
        for i, s in enumerate(cs):
            if not isinstance(s, str): E('demo.call_subs[%d] must be text' % i); continue
            sp.texts.append(('demo.call_subs[%d]' % i, s))
            ls = s.split('\n')
            if len(ls) > 2: E('demo.call_subs[%d] has %d lines, the limit is 2' % (i, len(ls)))
            for n, x in enumerate(ls):
                if len(x) > LIM['call_line']: E('demo.call_subs[%d] line %d is %d characters, the limit is %d (cut %d): %r' % (i, n + 1, len(x), LIM['call_line'], len(x) - LIM['call_line'], x))
            for ph in re.findall(r'\{[^}]*\}?', s):
                if ph != '{missed}': E('demo.call_subs[%d]: unknown placeholder %r (only {missed} is filled in)' % (i, ph))
            if '{missed}' in s and (i != 0 or '{missed}' not in ls[0]):
                Wn('demo.call_subs[%d]: {missed} is on line %d of subtitle %d; the format puts it on line one of the first subtitle (the build still fills it in)' % (i, 1 + next(n for n, x in enumerate(ls) if '{missed}' in x), i + 1))
        sp.s(d, 'nurse_sub', 'demo', LIM['nurse_sub'])

        # ---- outro
        o = spec.get('outro')
        if not isinstance(o, dict): E('spec.outro must be an object'); o = {}
        sp.keys(o, {'start', 'end', 'chip', 'graphics', 'link', 'team'}, 'outro')
        a, b = tsec(o.get('start'), 'outro.start'), tsec(o.get('end'), 'outro.end')
        last = blocks[-1] if blocks else None
        if last is not None and None not in (a, b) and (a, b) != (last['a'], last['b']): E('outro is %s–%s but the last narration block is %s–%s' % (o.get('start'), o.get('end'), mmss(last['a']), mmss(last['b'])))
        if not isinstance(o.get('chip'), str): E('outro.chip must be text (an empty string is fine)')
        sp.s(o, 'link', 'outro'); sp.s(o, 'team', 'outro')
        gs = o.get('graphics')
        if not isinstance(gs, list) or len(gs) != 1: E('outro.graphics must hold exactly one graphic'); gs = gs if isinstance(gs, list) else []
        for gi, g in enumerate(gs):
            c, _ = sp.graphic(g, 'outro.graphics[%d]' % gi, gi == 0, False)
            times = check_cues(c, last, 'the closing block')
            if gi == 0 and last is not None and None not in (a, b):
                dur = b - a; d2 = min(3.2, dur * 0.25); d1 = dur - d2      # the build: recap card for d1, then the link and team card
                sync.append('  %-5s–%-7s %5.1f s  %-6s recap card, then the link and team card until %s (+2 s hold: the file ends at %s)' % (mmss(a), mmss(round(a + d1, 2)), d1, 'outro', mmss(b), mmss(b + 2)))
                for pth, ph in c:
                    if pth in times:
                        rel = min(max(times[pth] - a, 0.1), d1 - 0.8); vis = d1 - rel
                        if vis < 2.0: Wn('sync: %s (cue %r, spoken at %s) is visible for only %.1f s before the recap card gives way to the link card' % (pth, ph, mmss(round(times[pth], 1)), vis))
                if b + 2 > 360: E('timeline: with the 2 s hold on the end card the file would pass 6:00')
                elif b + 2 > VIDEO_END: Wn('timeline: the build holds the end card 2 s after the last word, so the file is %s long (the hackathon limit is 6:00)' % mmss(b + 2))

        # ---- every on-screen string: stray characters
        for pth, v in sp.texts:
            if v != v.strip(): Wn('%s has a space at its start or end: %r' % (pth, v))
            if '\\n' in v or '\\"' in v: E('%s contains a literal backslash sequence (double-escaped in the JSON?): %r' % (pth, v))
            if re.search(r'[\t\r]', v): E('%s contains a TAB or carriage return' % pth)
            bad = sorted(set(re.findall(r'[\u200b\u200c\u200d\u2060\ufeff\u00ad\u00a0]', v)))
            if bad: Wn('%s contains invisible or non-breaking characters: %s' % (pth, ' '.join(cp(c) for c in bad)))
            cq = sorted(set(re.findall(r'[\u2018\u2019\u201c\u201d]', v)))
            if cq: Wn('%s contains smart quotes (%s): %r' % (pth, ' '.join(cp(c) for c in cq), v))
            if re.search(r'  ', v) and not re.search(r'  ·  ', v): Wn('%s contains a double space: %r' % (pth, v))
        missing = render_fit(spec)
        if missing:
            for pth, v in sp.texts:
                bad = sorted({ch for ch in v if not ch.isspace() and missing(ch)})
                if bad: E('%s uses character(s) the video font cannot draw (they show as empty boxes): %s' % (pth, ' '.join('%s %s' % (c, cp(c)) for c in bad)))

    if sync:
        print('\nPart 1 and close: when each graphic is on screen (worked out the way the build does it):')
        print('\n'.join(sync))

    # ---------- (e) verdict
    if WARN:
        print('\nWARNINGS (%d) - allowed, but look at them:' % len(WARN))
        for w in WARN: print(' - ' + w)
    if ERR:
        print('\nERRORS (%d):' % len(ERR))
        for e in ERR: print(' - ' + e)
        return 1
    print('\nOK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
