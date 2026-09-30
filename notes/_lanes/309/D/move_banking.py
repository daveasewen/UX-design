"""#309 lane D (s309-D3) - move the #227 banking demo's four stat tiles from .cn-stat-card to Metric.
Mechanical and idempotent-refusing: every replacement must match exactly the expected number of times.
The two arrow symbols are READ from knowledge/snippets/Metric.reference.html (byte-matched library
`direction` arrows), never retyped. Styles stay canon's (.cn-metric); the page keeps its own layout rules,
renamed from .stat-card to .metric."""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
P = os.path.join(ROOT, "dashboards", "international-banking-dashboard.canon.html")
snip = open(os.path.join(ROOT, "knowledge", "snippets", "Metric.reference.html"), encoding="utf-8").read()
sym = {k: re.search(r'<symbol id="%s".*?</symbol>' % k, snip).group(0) for k in ("metric-up", "metric-down")}
s = open(P, encoding="utf-8").read()
def rep(old, new, n):
    global s
    c = s.count(old)
    if c != n: sys.exit("REFUSED: %r found %d times, expected %d" % (old[:60], c, n))
    s = s.replace(old, new)
rep('<symbol id="trend-up" viewBox="0 0 18 18"><path data-bespoke="financial trend indicator" d="M16 12H2L9 5L16 12Z" fill="currentColor"/></symbol>'
    '<symbol id="trend-down" viewBox="0 0 18 18"><path data-bespoke="financial trend indicator" d="M2 6H16L9 13L2 6Z" fill="currentColor"/></symbol>',
    sym["metric-up"] + sym["metric-down"], 1)
rep('.dashboard-tile .stat-card{height:100%}.dashboard-stat-tile .stat-card{padding:24px;border:none}',
    '.dashboard-tile .metric{height:100%}.dashboard-stat-tile .metric{padding:24px;border:none}', 1)
rep('dashboard-stat-tile cn-stat-card"', 'dashboard-stat-tile cn-metric"', 4)
rep('<div class="stat-card" role="group"', '<div class="metric" role="group"', 4)
rep('<p class="lbl16 t-cm-caption">', '<p class="metric-lbl t-cm-caption">', 4)
rep('<span class="amt t-cm-figure-4"><span>£</span>', '<span class="metric-val t-cm-figure-4"><span class="unit">£</span>', 3)
rep('<span class="amt t-cm-figure-4"><span>6</span>', '<span class="metric-val t-cm-figure-4"><span>6</span>', 1)
rep('<span class="delta up" data-carries="symbol label"><span class="arrow" aria-hidden="true"><svg><use href="#trend-up"/></svg></span>',
    '<span class="metric-delta up" data-carries="symbol label"><span class="glyph" aria-hidden="true"><svg><use href="#metric-up"/></svg></span>', 1)
rep('<span class="delta down" data-carries="symbol label"><span class="arrow" aria-hidden="true"><svg><use href="#trend-down"/></svg></span>',
    '<span class="metric-delta down" data-carries="symbol label"><span class="glyph" aria-hidden="true"><svg><use href="#metric-down"/></svg></span>', 1)
rep('<span class="delta"><span class="t-cm-figure-6">', '<span class="metric-delta"><span class="t-cm-figure-6">', 2)
rep('<span class="per t-cm-legal">', '<span class="metric-per t-cm-legal">', 4)
for bad in ("cn-stat-card", "stat-card", "trend-up", "trend-down", 'class="amt', 'class="lbl16', 'class="per '):
    if bad in s: sys.exit("REFUSED: %r still present" % bad)
open(P, "w", encoding="utf-8").write(s)
print("moved: 4 tiles to .cn-metric, 2 symbols from Metric.reference.html, 2 page rules renamed")
