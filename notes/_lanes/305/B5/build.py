"""#305 B5: builds the loose-ends decision page. House CSS, dark mode and the decisions overlay are copied from
lane B4's call-27 review page (never re-drawn); the overlay script gains a chip set per item (data-chips), a compact
box for the when-rule rows, and the item's recommendation in the copied text. Run from the repo root."""
import re
SRC = 'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html'
LANE = 'notes/_lanes/305/B5/'
OUT = 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html'
s = open(SRC).read()
head = s[:s.index('</head>')]
house_css = ''.join(re.findall(r'<style>.*?</style>', head, re.S))          # includes B4's dark block (last)
back = re.search(r'<a id="rv-back".*?</a>', s, re.S).group(0)
ov_start = s.index('<style>\n.dd-box')
overlay = s[ov_start:s.index('</body>')]
CFG = """var CFG = {
    page:'decide-305-loose-ends-v1', title:'The loose ends, decision page v1', path:'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'.dd-call', kind:'Decision', title:'.q', host:'.dd-slot', prefix:'item', num:'.idx', rec:'.rec' },
      { sel:'.wr', kind:'When-rule', title:'.pn', host:'.dd-slot', prefix:'wr', num:'.idx', rec:'.rule', compact:true }
    ]
  };"""
def sub1(pat, rep, t, flags=0):
    t2, n = re.subn(pat, rep, t, count=1, flags=flags)
    assert n == 1, pat
    return t2
o = overlay
o = sub1(r"var CFG = \{.*?\n  \};", lambda m: CFG, o, re.S)
o = sub1(r"items\.push\(\{ id:id, kind:t\.kind, num:num, title:title, ",
         "items.push({ id:id, kind:t.kind, num:num, title:title, chips:(el.getAttribute('data-chips')||'').split('|').filter(Boolean), compact:!!t.compact, rec: t.rec ? txt(el.querySelector(t.rec)) : '', ", o)
o = sub1(r"box\.className = 'dd-box';", "box.className = 'dd-box'+(it.compact?' dd-compact':'');", o)
o = sub1(r"CHIPS\.map\(function\(c\)", "((it.chips&&it.chips.length)?it.chips:CHIPS).map(function(c)", o)
o = sub1(r"lines\.push\('<sub>'\+it\.kind", "if(it.rec) lines.push('_On the page: '+it.rec+'_  ');\n      lines.push('<sub>'+it.kind", o)
o = o.replace("drop it in notes/_lanes/304/", "drop it in notes/_lanes/305/")
t = open(LANE + 'page.src.html').read()
t = t.replace('{{HOUSE_CSS}}', house_css).replace('{{DARK_CSS}}', '').replace('{{BACK}}', back).replace('{{OVERLAY}}', o)
assert '{{' not in t, re.findall(r'\{\{\w+\}\}', t)
open(OUT, 'w').write(t)
print('wrote', OUT, len(t))
