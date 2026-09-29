"""#309 lane C - Kpi-tile.reference.html becomes Metric.reference.html (s308-D42, s309-D2).
Run once after `git mv knowledge/snippets/Kpi-tile.reference.html knowledge/snippets/Metric.reference.html`.
Renames the class and symbol vocabulary kpi-tile -> metric, kpi-* -> metric-* (a class token only:
never inside a path or a file name), retitles the file, prepends the Metric header, and names the
component in the token manifest. Everything else in the file - the CSS values, the markup, the
history prose - is kept as it was."""
import re, sys
P = "knowledge/snippets/Metric.reference.html"
t = open(P, encoding="utf-8").read()
TOK = r"(?<![A-Za-z0-9/_-])"
t = re.sub(TOK + r"kpi-tile(?![A-Za-z0-9_]|\.meta|\.reference)", "metric", t)
t = re.sub(TOK + r"kpi-(?=[a-z])", "metric-", t)
old_title = "<title>KPI tile — reference implementation (PROPOSED #203, redesigned #261)</title>"
assert t.count(old_title) == 1
HEAD = """<title>Metric — reference implementation (one block: s308-D42, rebuilt #309)</title>
<!--
  ★ METRIC — ONE BLOCK. s308-D42 (Dave, #308, by click): "One block, Metric, with the trend as an
  optional slot; old names kept as aliases". s309-D2 (Dave, #309, in chat, 21:37 BST): "go", to
  "Metric: rebuild it properly, one lane, canon and the 27 chart proofs re-run."
  Built #309 lane C. This file WAS snippets/Kpi-tile.reference.html (renamed with git mv, so its
  history follows it). The KPI tile was the superset - the stat card's anatomy (label · value ·
  delta · period) plus two optional slots - so it is the one block's reference, and its class and
  symbol vocabulary is renamed kpi-tile -> metric, kpi-* -> metric-*. Nothing else in the drawing
  moved: every value, span, state and Dave's #261 K2/K3 corrections are kept byte for byte.
  THE TREND IS AN OPTIONAL SLOT: .metric-spark (the Chart-sparkline atom at inline scale). A
  Metric without a series leaves the slot out - that is the reading the stat card used to be,
  and the compact row below draws it. The target row stays the second optional slot.
  THE OLD NAMES: component:stat-card and component:kpi-tile are alias seats of component:metric
  (knowledge/components/stat-card.meta.json, kpi-tile.meta.json; the s210-D5 alias seat).
  snippets/Stat-card.reference.html is KEPT, byte-untouched, as the stat-card reading's retained
  markup: pages built before the merge carry .cn-stat-card (the #227 banking demo, which two gates
  measure, and the progress dashboard), and moving them is a look change that is Dave's to see.
  The history below is the KPI tile's record, kept as it was written (class names renamed only).
-->"""
t = t.replace(old_title, HEAD, 1)
old_c = '"component": "KPI tile",'
assert t.count(old_c) == 1
t = t.replace(old_c, '"component": "Metric",\n    "$aliases": ["kpi-tile", "stat-card"],', 1)
old_s = '"$status": "PROPOSED #203, redesigned #261 on Dave\'s nomination, Dave\'s eye owed — the trend-card component is FLOATED, NOT RULED (s182-D2). This manifest is a proposal, not a proof-of-done.",'
assert t.count(old_s) == 1, "status"
t = t.replace(old_s, '"$status": "RULED s308-D42 (one block, Metric, the trend an optional slot, old names kept as aliases) and s309-D2 (rebuilt properly). Built #309 lane C from the KPI tile; Dave\'s eye owed on the with/without-trend render. Before #309: PROPOSED #203, redesigned #261 on Dave\'s nomination (s182-D2 had floated the trend card).",', 1)
open(P, "w", encoding="utf-8").write(t)
print("kpi left:", len(re.findall(TOK + r"kpi-", t)), "metric tokens:", len(re.findall(r"metric", t)))
