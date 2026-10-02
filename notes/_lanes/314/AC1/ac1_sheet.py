"""#314 AC1 - contact sheets: one PNG per mode, rows = surfaces, columns = the four themes, plain labels.
Run from the repo root at the seat:  python3 notes/_lanes/314/AC1/ac1_sheet.py"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "renders")
sys.path.insert(0, HERE)
from ac1_render import CASES, DASH
THEMES = [("mono", "Mono (Apollo)"), ("legacy", "Legacy"), ("console", "Console"), ("supercharge", "Supercharge")]
CELL_W, CELL_H, LAB_W, HEAD_H, GAP = 520, 300, 260, 56, 14

def font(sz):
    for f in ["/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f):
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
    return ImageFont.load_default()

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def sheet(mode):
    rows = CASES + [DASH]
    W = LAB_W + 4 * (CELL_W + GAP) + GAP; H = HEAD_H + 40 + len(rows) * (CELL_H + GAP) + GAP
    bg = (246, 246, 246) if mode == "light" else (40, 40, 40); ink = (20, 20, 20) if mode == "light" else (235, 235, 235)
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    fh, fl, fs = font(26), font(18), font(14)
    d.text((GAP, 12), f"Floating surfaces open, {mode} mode - border all round, mega menu bottom edge only (s313-D58)", font=fh, fill=ink)
    for i, (_, lab) in enumerate(THEMES):
        d.text((LAB_W + GAP + i * (CELL_W + GAP), HEAD_H + 8), lab, font=fl, fill=ink)
    for r, case in enumerate(rows):
        y = HEAD_H + 40 + r * (CELL_H + GAP)
        for k, line in enumerate(wrap(d, case[1], fl, LAB_W - 2 * GAP)):
            d.text((GAP, y + 8 + k * 24), line, font=fl, fill=ink)
        for i, (t, _) in enumerate(THEMES):
            x = LAB_W + GAP + i * (CELL_W + GAP)
            p = os.path.join(R, f"{case[0]}-{t}-{mode}.png")
            d.rectangle([x - 1, y - 1, x + CELL_W, y + CELL_H], outline=(150, 150, 150))
            if not os.path.exists(p):
                d.text((x + 10, y + 10), "missing", font=fs, fill=(200, 0, 0)); continue
            c = Image.open(p).convert("RGB"); s = min(CELL_W / c.width, CELL_H / c.height)
            c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
            im.paste(c, (x + (CELL_W - c.width) // 2, y + (CELL_H - c.height) // 2))
    out = os.path.join(HERE, "renders", f"_SHEET-{mode}.png"); im.save(out, optimize=True); print(out, im.size)

for m in ["light", "dark"]:
    sheet(m)
