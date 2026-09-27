"""scope_call10.py — #305 conductor follow-up: call 10 scoped to COMMON. Base rules back to HEAD's alpha
(call 5's overflow form kept); Common's solid ink as s158-D1 theme GUARDS in the legacy override set."""
import json
def edit(p, pairs):
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:80], s.count(old)); s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s)
edit('knowledge/snippets/Kpi-tile.reference.html', [
("""     #305 call 10 (Dave: "yes") — the ink is SOLID text/secondary, not an alpha on the text ink: the
     alpha read 3.71:1 in Common (#99 licenses alpha for state changes only). */
  .kpi-lbl{margin:0; color:var(--muted); min-width:0; overflow-x:clip; overflow-y:visible; white-space:nowrap;
    text-overflow:ellipsis;}""",
"""     #305 call 10 is COMMON ONLY ("The muted labels in Common"): the alpha stays here, as at HEAD, for
     mono, console and supercharge; Common's solid text/secondary ink (the muted var) is a theme GUARD in
     tokens/themes/apollo-legacy.overrides.json, emitted by gen_theme_cascade.py (the s158-D1 shape). */
  .kpi-lbl{margin:0; opacity:var(--alpha-60); min-width:0; overflow-x:clip; overflow-y:visible; white-space:nowrap;
    text-overflow:ellipsis;}"""),
("  .kpi-per{margin:0 0 0 4px; color:var(--muted);}   /* #305 call 10 — solid text/secondary */",
 "  .kpi-per{margin:0 0 0 4px; opacity:var(--alpha-60);}"),
("    --muted:#1A1A1A;        /* text/secondary — the label + period ink, SOLID (#305 call 10) */\n",
 "    --muted:#1A1A1A;        /* text/secondary — Common's solid label + period ink, read by its theme guard (#305 call 10) */\n"),
])
edit('knowledge/snippets/Template-dashboard-bento.reference.html', [
("  .kpi-tile .lbl16{margin:0; color:var(--muted);}   /* #305 call 10 — solid text/secondary, not an alpha (3.71:1 in Common) */",
 "  .kpi-tile .lbl16{margin:0; opacity:var(--alpha-60);}"),
("  .delta .per{color:var(--muted); margin-left:4px;}   /* #305 call 10 — solid text/secondary */",
 "  .delta .per{opacity:var(--alpha-60); margin-left:4px;}"),
("    --muted:#1A1A1A;   /* text/secondary — the KPI label + period ink, SOLID (#305 call 10) */\n",
 "    --muted:#1A1A1A;   /* text/secondary — Common's solid KPI label + period ink, read by its theme guard (#305 call 10) */\n"),
])
edit('knowledge/snippets/App-shell-side-nav.reference.html', [
("  .sn-group-label{display:block; padding:8px 16px; color:var(--muted);}   /* #305 call 10 — solid text/secondary; the .72 alpha read 3.75:1 in Common */",
 "  .sn-group-label{display:block; padding:8px 16px; color:var(--muted); opacity:.72;}")])
edit('knowledge/snippets/Sidebar-nav.reference.html', [
("  .sn-group-label{display:block; padding:8px 16px; color:var(--nav-muted);}   /* #305 call 10 — solid text/secondary; the .72 alpha read 3.75:1 in Common */",
 "  .sn-group-label{display:block; padding:8px 16px; color:var(--nav-muted); opacity:.72;}")])

def note(what, was):
    return ['#305 call 10 (Dave, 2026-09-27: "yes" to "The muted labels in Common: replace the transparency with a',
            'solid ink that reads 4.5:1?") is COMMON ONLY. ' + what + ' read ' + was + ' in Common (an alpha on the',
            'ink; #99 licenses alpha for state changes only); here it takes text/secondary SOLID. Mono, console and',
            'supercharge keep the snippet alpha exactly as at HEAD (their text/secondary IS the text ink).']
def rule(n, sel, body):
    return ('        {\n          "$note": [\n' + ",\n".join('            ' + json.dumps(l, ensure_ascii=False) for l in n) +
            '\n          ],\n          "selector": ' + json.dumps(sel) + ',\n          "body": ' + json.dumps(body) + '\n        }')
def block(slug, rules):
    return '    ' + json.dumps(slug) + ': {\n      "rules": [\n' + ',\n'.join(rules) + '\n      ]\n    }'
p = 'knowledge/tokens/themes/apollo-legacy.overrides.json'
s = open(p, encoding='utf-8').read()
anchor = '\n    "tabs": {'
assert s.count(anchor) == 1
ins = ',\n'.join([
    block("app-shell-side-nav", [rule(note("The side-nav group label", "3.75:1"), ".cn-app-shell-side-nav .sn-group-label", "opacity:1;")]),
    block("kpi-tile", [rule(note("The KPI label and period", "3.71:1"), ".cn-kpi-tile .kpi-lbl", "color:var(--muted);opacity:1;"),
                       rule(["#305 call 10 (Common only) - the period, with the label above."], ".cn-kpi-tile .kpi-per", "color:var(--muted);opacity:1;")]),
    block("sidebar-nav", [rule(note("The side-nav group label", "3.75:1"), ".cn-sidebar-nav .sn-group-label", "opacity:1;")]),
    block("template-dashboard-bento", [rule(note("The bento's own KPI label", "3.71:1"), ".cn-template-dashboard-bento .kpi-tile .lbl16", "color:var(--muted);opacity:1;"),
                       rule(["#305 call 10 (Common only) - the bento KPI period, with the label above."], ".cn-template-dashboard-bento .delta .per", "color:var(--muted);opacity:1;")]),
])
s = s.replace(anchor, '\n' + ins + ',' + anchor)
json.loads(s); open(p, 'w', encoding='utf-8').write(s)
print("ok", list(json.loads(s)["guards"]))
