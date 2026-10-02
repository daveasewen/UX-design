"""#315 LA: does any field's help text wrap? (s314-D11, his words: 'The help text, it shouldn't wrap').
Read-only render of every snippet at 1280px: every element whose class names a help/hint line under a field
(.help .hint .uhelp .fl-help .field-help .msg-help .tf-help ...), outside the APOLLO-DEMO fence and not a
tooltip/popover body; counts its line boxes. Writes help_wrap.json."""
import json, os, glob
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../..'))
JS = r"""() => {
  const fenced = new Set(); let on = 0;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ALL); let n;
  while ((n = w.nextNode())) { if (n.nodeType === 8) { if (/APOLLO-DEMO[^\n]*START/.test(n.nodeValue)) on++; else if (/APOLLO-DEMO[^\n]*END/.test(n.nodeValue)) on = Math.max(0, on-1); continue; } if (on && n.nodeType === 1) fenced.add(n); }
  const out = [];
  document.querySelectorAll('[class]').forEach(el => {
    const c = el.getAttribute('class');
    if (!/(^|[\s_-])(help|hint|uhelp|helper|assist)([\s_-]|$)|(-|^)help(-text)?\b/.test(c)) return;
    if (/help-btn|tip|popover|pop\b|tooltip/.test(c) || el.closest('[role=tooltip],[role=dialog]')) return;
    if (fenced.has(el)) return;
    const t = (el.innerText || '').trim(); if (!t) return;
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.4;
    const r = el.getBoundingClientRect(); if (r.width < 2) return;
    // count distinct line tops of the text
    const range = document.createRange(); range.selectNodeContents(el);
    const tops = new Set([...range.getClientRects()].filter(q => q.width > 0).map(q => Math.round(q.top)));
    out.push({cls: c.slice(0,50), text: t.slice(0,140), chars: t.length, lines: tops.size, width: Math.round(r.width), ws: cs.whiteSpace});
  });
  return out; }"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for s in sorted(glob.glob(os.path.join(ROOT, 'knowledge/snippets/*.reference.html'))):
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        try:
            pg.goto('file://' + s, wait_until='load', timeout=20000); pg.wait_for_timeout(150)
            r = pg.evaluate(JS)
            if r: res[os.path.basename(s)] = r
        except Exception as ex:
            res[os.path.basename(s)] = [{'error': str(ex)[:120]}]
        pg.close()
    b.close()
json.dump(res, open(os.path.join(HERE, 'help_wrap.json'), 'w'), indent=1)
wr = {k: [x for x in v if x.get('lines', 0) > 1] for k, v in res.items()}
print('pages with help lines', len(res), 'help lines', sum(len(v) for v in res.values()), 'wrapping', sum(len(v) for v in wr.values()))
for k, v in wr.items():
    for x in v: print(k, x['lines'], x['chars'], x['width'], x['text'][:90])
