#!/usr/bin/env python3
"""Lane PR #316: mint surface/dark-band (s315-D40) from the ladder — light color/neutral/4, dark color/neutral/5. String inserts only."""
import json, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
DESC = ("THE DARK BAND - s315-D40 (Dave, review page export 2026-10-02 22:32 BST, call 40, verbatim: \"if the footer is dark in light mode it should stay dark in dark mode, if the page is black it should be a different dark grey to differentiate them\"). "
        "A band that is DARK IN BOTH MODES: in light the near-black of the ladder (color/neutral/4, #1A1A1A, the Mono ink); in dark ONE STEP ABOVE THE PAGE on the neutral ladder (color/neutral/5, #313131) so the band never merges with the #1A1A1A dark page. "
        "Its label is text/reverse (flat white both modes: 17.4:1 light, 13.0:1 dark). It closes the light-mode half of the _COMPONENT-GAPS row 'Inverse / hero surface' (2026-06-30, verbatim 'no light-mode dark-band role'). "
        "NOT surface/action-primary: that ground INVERTS (#FAFAFA in dark) and drew the footer as a light band under a dark page, the look call 40 refused. "
        "MINTED FROM THE LADDER, NOT TYPED: both legs are $alias addresses, so ADR-0014 resolves them per theme. "
        "⚠ THE NAME IS PROPOSED - token names are Dave's (s145-D1 precedent, as surface/section at #305); the behaviour is his call-40 word. Consumer: Footer's --ft-band (#316 lane PR).")
def insert_after_section(path, entry_text, anchor):
    p = os.path.join(R, path); s = open(p, encoding='utf-8').read()
    assert s.count(anchor) == 1, (path, s.count(anchor))
    assert '"dark-band"' not in s
    s = s.replace(anchor, anchor + entry_text); json.loads(s)
    open(p, 'w', encoding='utf-8').write(s)
# base (light): the surface group's "section" entry ends with its $description line then "    }"
base = os.path.join(R, 'knowledge/tokens/semantic-colour.json'); bs = open(base, encoding='utf-8').read()
i = bs.index('    "section": {\n      "$value": "{color.neutral.13}"'); j = bs.index('\n    }', i) + len('\n    }')
anchor = bs[i:j]
insert_after_section('knowledge/tokens/semantic-colour.json',
    ',\n    "dark-band": {\n      "$value": "{color.neutral.4}",\n      "$type": "color",\n      "$description": ' + json.dumps(DESC, ensure_ascii=False) + '\n    }', anchor)
insert_after_section('knowledge/tokens/modes/dark/semantic-colour.json',
    ',\n    "dark-band": {\n      "$value": "{color.neutral.5}",\n      "$type": "color"\n    }',
    '    "section": {\n      "$value": "{color.neutral.4}",\n      "$type": "color"\n    }')
print('minted')
