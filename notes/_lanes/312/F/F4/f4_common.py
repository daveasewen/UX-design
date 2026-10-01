"""#312 lane F4 — shared scratch builders for render_F4.py. Every page is a SCRATCH copy in /dev/shm
built from the committed sha (git show), never the mount's working tree; canon.css and type.css too."""
import os, re, json, subprocess
R = os.getcwd(); SH = "/dev/shm/f4_312"; OUT = "notes/_lanes/312/F/F4/img"
os.makedirs(SH, exist_ok=True); os.makedirs(OUT, exist_ok=True)
THEMES = ["mono", "legacy", "supercharge", "console"]
_sha = None
def sha(ref="HEAD"):
    global _sha
    if _sha is None:
        _sha = subprocess.run(["git", "rev-parse", ref], capture_output=True, text=True, check=True).stdout.strip()
        open(f"{SH}/canon.css", "w").write(show("knowledge/canon/canon.css"))
        open(f"{SH}/type.css", "w").write(show("knowledge/canon/type.css"))
    return _sha
def show(p):
    return subprocess.run(["git", "show", f"{_sha}:{p}"], capture_output=True, text=True, check=True).stdout

def body_of(snippet):
    """the snippet's <body> inner markup, scripts/styles/comments dropped, asset paths absolute"""
    s = show(f"knowledge/snippets/{snippet}")
    s = re.sub(r'<!--[\s\S]*?-->', '', s)
    b = s[s.find('<body'):]; b = b[b.find('>') + 1:]; b = b[:b.rfind('</body>')]
    b = re.sub(r'<script[\s\S]*?</script>', '', b); b = re.sub(r'<style[\s\S]*?</style>', '', b)
    return b.replace('src="../', f'src="file://{R}/knowledge/').replace('href="../', f'href="file://{R}/knowledge/')

def sprite(snippet):
    s = show(f"knowledge/snippets/{snippet}")
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(re.findall(r'<symbol[\s\S]*?</symbol>', s)) + '</svg>'

def page(name, theme, mode, body, head_extra="", body_cls="canon"):
    html = f"""<!DOCTYPE html><html lang="en" data-apollo-theme="{theme}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="file://{SH}/type.css"><link rel="stylesheet" href="file://{SH}/canon.css">{head_extra}</head>
<body class="{body_cls}" data-theme="{mode}">{body}</body></html>"""
    p = f"{SH}/{name}.html"; open(p, "w").write(html); return "file://" + p

COLOR_JS = r"""
window.f4hex = c => { if (!c) return null; const m = c.match(/[\d.]+/g); if (!m) return c; const [r,g,b,a] = m.map(Number);
  if (a === 0) return 'transparent'; return '#' + [r,g,b].map(x => Math.round(x).toString(16).padStart(2,'0')).join('').toUpperCase(); };
window.f4lum = h => { const v = [1,3,5].map(i => parseInt(h.substr(i,2),16)/255).map(c => c <= .03928 ? c/12.92 : Math.pow((c+.055)/1.055, 2.4));
  return .2126*v[0] + .7152*v[1] + .0722*v[2]; };
window.f4cr = (a,b) => { if (!a || !b || a[0] !== '#' || b[0] !== '#') return null; const x = f4lum(a), y = f4lum(b);
  return Math.round(100 * (Math.max(x,y) + .05) / (Math.min(x,y) + .05)) / 100; };
"""

def compose(b, fn, tag, notes, cells, cols=2, width=1440, cell_w=None):
    """a sheet of already-rendered PNGs with captions: cells = [(png path, caption html), ...]"""
    cw = cell_w or (width - 48 - 24 * (cols - 1)) // cols
    items = "".join(f'<figure><img src="file://{R}/{p}" style="width:{cw}px"><figcaption>{c}</figcaption></figure>' for p, c in cells)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff;font:13px/1.45 Helvetica,Arial,sans-serif;color:#1F1F1F}}
.tag{{background:#1F1F1F;color:#fff;font:700 12px/1 Helvetica,Arial,sans-serif;letter-spacing:.08em;padding:12px 24px}}
.notes{{background:#FFF3B0;padding:8px 24px;border-bottom:1px solid #C9A800;display:flex;gap:32px}} .notes span{{flex:1}}
.grid{{display:grid;grid-template-columns:repeat({cols},{cw}px);gap:24px;padding:24px}}
figure{{margin:0}} img{{display:block;border:1px solid #BDBDBD}} figcaption{{padding-top:6px}}
</style></head><body><div class="tag">{tag}</div><div class="notes">{''.join('<span>'+n+'</span>' for n in notes)}</div>
<div class="grid">{items}</div></body></html>"""
    p = f"{SH}/compose.html"; open(p, "w").write(html)
    pg = b.new_page(viewport={"width": width, "height": 600}); pg.goto("file://" + p); pg.wait_for_timeout(300)
    pg.screenshot(path=fn, full_page=True); pg.close()
