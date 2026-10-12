# Builds assets/trust_icmr.png (1920x1080) from today's screenshots of the LIVE trust page (assets/trust/*.png).
# Three excerpts, kept in page order, each cut straight from a screenshot (no text is redrawn or edited):
#   1. ICMR National Ethical Guidelines 2017: the heading, then its Privacy and Ethics committee review rows
#      (the Consent and Vulnerable participants rows are left out; never show "Vulnerable participants":
#      it says the patient screens take no typing, but the video shows typing)
#   2. ICMR Guidelines on AI in health 2023: the heading and the whole table (4 rows with status badges)
#   3. Section 4 "What we do not claim": "Designed to follow these guidelines. Not reviewed or approved by ICMR,
#      an ethics committee or CDSCO."
# Run: python make_trust_icmr.py
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, 'assets', 'trust')
BG = (244, 246, 248)                     # the page background
X0, X1 = 404, 1516                       # table borders sit at x 416 and 1503


def crop(name, y0, y1):
    return Image.open(os.path.join(T, name)).convert('RGB').crop((X0, y0, X1, y1))


parts = [
    (crop('trust_icmr2017.png', 18, 54), 0),     # heading "ICMR National Ethical Guidelines 2017"
    (crop('trust_icmr2017.png', 255, 397), 2),   # Privacy + Ethics committee review rows (divider line on top)
    (crop('trust_icmr2023.png', 16, 308), 24),   # heading + the whole AI-in-health 2023 table
    # section 4's banner is left out: "Designed to follow these guidelines" is stronger than the approved "informed by"
]
CW, CH = 1280, 720                       # 16:9; the build stretches any image to 16:9, so keep it exact
canvas = Image.new('RGB', (CW, CH), BG)
y = 28
for im, gap in parts:
    y += gap
    canvas.paste(im, ((CW - im.width) // 2, y))
    y += im.height
print('content ends at y', y, 'of', CH, '(the image tag covers the bottom-left from about y 655)')
out = os.path.join(HERE, 'assets', 'trust_icmr.png')
canvas.resize((1920, 1080), Image.LANCZOS).save(out)
print('wrote', out)
