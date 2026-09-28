# #305 lane A2 — add a `loose-ends` section to notes/_lanes/305/A/CALL-MAP.json, by addition; round-trip proven first.
import json
P = 'notes/_lanes/305/A/CALL-MAP.json'
src = open(P, encoding='utf-8').read()
d = json.loads(src)
fmt = lambda o: json.dumps(o, ensure_ascii=False, indent=1) + ('\n' if src.endswith('\n') else '')
assert fmt(d) == src, 'CALL-MAP does not round-trip byte-identical; refuse'
assert 'loose-ends' not in d
R = lambda rid, status, needs_build, what: {"ruling_id": rid, "status": status, "needs_build": needs_build, "what": what}
W = lambda row, what: {"row": row, "status": "open", "owner": "dave", "what": what}
wr = {"1": "filter-toolbar-bar", "2": "footer", "3": "template-dashboard-bento", "5": "button", "7": "breadcrumbs", "8": "chart-bar",
      "9": "headers", "10": "kpi-tile", "11": "layout-utilities", "12": "legend", "13": "navigations", "14": "stat-card",
      "15": "status-indicator", "16": "summary", "17": "view-options"}
items = {
 "1a": {"row": "W-305e5", "status": "open", "owner": "dave", "what": "CEO three groups, run 1: verdict 'Yes, three groups' and his comment 'the donut and stacked bar could be side by side' - recorded on the grouping thread, not ruled"},
 "1b": {"rows": ["W-305e5", "W-305e4"], "status": "open", "owner": "dave", "what": "CEO three groups, run 2: 'No'; the header-component wish is W-305e4"},
 "1c": {"rows": ["W-305e5", "W-305e4"], "status": "open", "owner": "dave", "what": "CEO three groups, run 3: 'No'; the UX question (two intimately linked subjects as one group) is W-305e5"},
 "1d": R("s305-D59", "ruled", True, "ring run 1 'Agree: fails' + his words: chart set to fill, container constrains (smaller, or more than one element); amends s305-D9's hug half by addition, confirms its half-width column"),
 "1e": R("s305-D59", "ruled", True, "ring run 2 'Agree: fails'"),
 "1f": R("s305-D59", "ruled", True, "ring run 3 'Agree: passes'"),
 "2a": R("s305-D58", "ruled", True, "data grid: columns a setting, filters a slot (the applied terms, today's `filters` setting, need a new name)"),
 "2b": R("s305-D58", "ruled", True, "lightbox: items a setting"),
 "2c": R("s305-D58", "ruled", True, "stepper: steps a slot"),
 "2d": R("s305-D58", "ruled", True, "tab bar: items a setting (the setting carries icon and label, not only the count)"),
 "3a": {"ruling_id": "s155-D1", "status": "enacted", "sha": "a1995c0c", "needs_build": False, "what": "'Settled at #155': the two greens #137F3C on white, #66CC8D else, mono only; leaves kind 5; residual (e) stays Dave's. The other six of kind 5 (s234-D4, s212-D1, s216-D1, s244-D1, s256-D1, s262-D5) stamped 'ruled — NOT BUILT, ON THE NOT-BUILT LIST'; s305-D38 stays ruled (kinds 1-5 discharged, 28 of kind 6 remain)"},
 "3b": {"ruling_id": "s229-D3", "status": "enacted", "sha": "baf5458e", "needs_build": False, "what": "'Read as built': the segmented partial group and $scan sweep, built at baf5458e"},
 "4a": {"ruling_id": "s305-D25", "status": "enacted", "sha": "27efb7b6", "needs_build": False, "what": "'Accept the wording': R4a's `when` in modals, split-button, dropdown, landed 27efb7b6"},
 "4b": {"ruling_id": "s305-D61", "status": "enacted", "sha": "e4ff4284", "needs_build": False, "what": "'Accept' + his words: webf-036's sentence is his wording"},
 "4c": {"ruling_id": "s305-D60", "status": "ruled", "needs_build": True, "what": "fifteen when-rules accepted; 11 already in their metas at HEAD 01fb005a, 4 draft only (filter-toolbar-bar, footer, template-dashboard-bento, button) + layout.grammar in when-fields.json, being built by lane B6",
        "rows": {**{k: {"part": s, "ruling_id": "s305-D60"} for k, s in wr.items()},
                 "4": {"part": "list-items", "row": "W-305e1", "verdict": "Change"},
                 "6": {"part": "app-shell-top-nav", "row": "W-305e2", "verdict": "Change"}},
        "note": "4c-9 page title also opened W-305e3 (the lock-up)"},
 "5": {"record": "notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md", "what": "'Used on my work machine and used in the room' - appended by addition, dated 2026-09-28; a record, not a ruling"},
}
d['loose-ends'] = {"provenance": "305 · 2026-09-28 · lane A2 (inscription seat)",
                   "source": "notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md",
                   "page": "notes/_DECIDE-305-loose-ends-2026-09-27-v1.html",
                   "items": items}
out = fmt(d)
assert out.startswith(src.rstrip('\n}').rstrip()[:len(src) - 10])
open(P, 'w', encoding='utf-8').write(out)
print('ok', len(items))
