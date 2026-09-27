"""#305 B4: builds the two review pages from their sources, copying the house CSS and the decisions overlay
from the #304 housekeeping decision page (never re-drawn). Run from the repo root."""
import re, os, json
SRC = 'notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'
LANE = 'notes/_lanes/305/B4/'
s = open(SRC).read()
head_css = ''.join(re.findall(r'<style>.*?</style>', s[:s.index('</head>')], re.S))
ov_start = s.index("<!-- ===== DAVE'S DECISIONS")
overlay = s[ov_start:s.index('</body>')]
ov_css = re.search(r'<style>.*?</style>', overlay, re.S).group(0)
ov_js = re.search(r'<script>.*?</script>', overlay, re.S).group(0)
BACK = ('<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;'
        'background:#000;color:#fff;font:500 13px/1 \'Helvetica Neue\',Helvetica,Arial,sans-serif;letter-spacing:.04em;'
        'padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>')
DARK = open(LANE + 'dark.css').read()
def build(src, out, cfg=None):
    t = open(LANE + src).read()
    t = t.replace('{{HOUSE_CSS}}', head_css).replace('{{DARK_CSS}}', '<style>\n' + DARK + '\n</style>').replace('{{BACK}}', BACK)
    t = t.replace('{{OVERLAY_CSS}}', ov_css)
    if '{{DIAG_WIDE}}' in t:
        import subprocess, sys; subprocess.check_call([sys.executable, LANE + 'diag.py'])
        t = t.replace('{{DIAG_WIDE}}', open(LANE + 'diag-wide.svg.txt').read()).replace('{{DIAG_TALL}}', open(LANE + 'diag-tall.svg.txt').read())
    if cfg:
        js = ov_js
        js = re.sub(r"var CFG = \{.*?\n  \};", cfg, js, count=1, flags=re.S)
        assert cfg in js
        t = t.replace('{{OVERLAY_JS}}', js)
    assert '{{' not in t, re.findall(r'\{\{\w+\}\}', t)
    open(out, 'w').write(t)
    print('wrote', out, len(t))
CFG1 = """var CFG = {
    page:'review-305-call-27-visuals-v1', title:'Call 27 in pictures, review page v1', path:'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'.dd-call', kind:'Decision', title:'.q', host:'.dd-slot', prefix:'call27', num:'.idx' }
    ]
  };"""
build('page1.src.html', 'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html', CFG1)
if os.path.exists(LANE + 'page2.src.html'):
    import subprocess, sys
    subprocess.check_call([sys.executable, LANE + 'make_page2.py'])
    build('page2.gen.html', 'notes/_SCAN-305-parked-questions-2026-09-27-v1.html')
