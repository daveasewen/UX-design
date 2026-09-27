"""pair.py <out.png> <left.png> <right.png> [labelL] [labelR] [maxw] — side by side, top-aligned, labelled."""
import sys
from PIL import Image, ImageDraw, ImageFont
out, a, b = sys.argv[1:4]; la = sys.argv[4] if len(sys.argv) > 4 else 'before'; lb = sys.argv[5] if len(sys.argv) > 5 else 'after'
mw = int(sys.argv[6]) if len(sys.argv) > 6 else 1400
A, B = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
def fit(im):
    if im.width > mw: im = im.resize((mw, round(im.height * mw / im.width)))
    return im
A, B = fit(A), fit(B)
H = max(A.height, B.height) + 50; W = A.width + B.width + 30
C = Image.new('RGB', (W, H), (128, 128, 128)); d = ImageDraw.Draw(C)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
except Exception: f = ImageFont.load_default()
d.text((10, 8), la, fill=(255, 255, 255), font=f); d.text((A.width + 40, 8), lb, fill=(255, 255, 255), font=f)
C.paste(A, (0, 50)); C.paste(B, (A.width + 30, 50)); C.save(out, optimize=True); print(out, C.size)
