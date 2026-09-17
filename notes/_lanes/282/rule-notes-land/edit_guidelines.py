#!/usr/bin/env python3
"""#282 lane RN — the ELEVEN guideline edits of s282-D1, in Dave's own words.

Each edit is a CLAUSE ADDED to the existing rule's bullet, placed immediately before the
destiny tag so guidelines/gen_rules_index.py picks it up (rule_text() reads the bullet up
to the tag and nothing after it). The stored sentence is never rewritten and no {#id} is
added, moved or removed. Every clause ends "(s282-D1, Dave 2026-09-17)".

col26-012 is NOT touched — he ruled (c) "Discuss first". IDEMPOTENT: a second run is a no-op.
"""
import sys, pathlib

G = pathlib.Path(__file__).resolve().parents[4] / 'knowledge' / 'guidelines'
CITE = '(s282-D1, Dave 2026-09-17)'

EDITS = [
 ('aca-003', 'accessibility-content-authoring.md',
  '  thing a speech-output user hears. [BLOCKING — GATED,',
  '  thing a speech-output user hears.\n'
  '  The first heading need not repeat the page title — an active navigation state or a\n'
  '  salutation may lead; the title, not the H1, is what orientation rests on.\n'
  '  ' + CITE + ' [BLOCKING — GATED,'),
 ('aid-009', 'accessibility-interaction-design.md',
  '  considered the default requirement." [BLOCKING — RULED 2026-07-03',
  '  considered the default requirement." The 44 default and the 24 floor are measured on\n'
  '  the HIT AREA, not on the visible target. ' + CITE + '\n'
  '  Beside that floor, a graded heuristic the designer weighs: the size of the visible\n'
  '  target, the clear space around it — spacing is also emphasis — and compact views,\n'
  '  which are a user choice. ' + CITE + ' [BLOCKING — RULED 2026-07-03'),
 ('col26-009', 'colour-standards-2026.md',
  "- **Don't use the supporting palette as text.** [BLOCKING-derivable",
  "- **Don't use the supporting palette as text.** Two reasons, not one: the contrast floor\n"
  '  and brand consistency — "if designers were allowed to use the supporting palette we\n'
  '  would get dramatically varied designs". ' + CITE + ' [BLOCKING-derivable'),
 ('dv-bar-007', 'data-visualisation-bar-charts.md',
  '  horizontal bar chart.** [BLOCKING-derivable',
  '  horizontal bar chart.** Scope: positive-scale bar charts. Negative values use the\n'
  '  vertical below-zero form, which is the sanctioned way to show them.\n'
  '  ' + CITE + ' [BLOCKING-derivable'),
 ('icon-006', 'icons.md',
  '- **Minimum 16px, maximum 48px; scale proportionately in 2px increments.**\n'
  '  [BLOCKING-derivable',
  '- **Minimum 16px, maximum 48px; scale proportionately in 2px increments.**\n'
  '  The floor is legibility; the ceiling is the icon/illustration boundary — at the ceiling\n'
  '  an icon is close to illustration dimensions; and the fixed set holds consistency.\n'
  '  ' + CITE + '\n'
  '  [BLOCKING-derivable'),
 ('logo26-001', 'brand-refresh-assets.md',
  '  journey.** [BLOCKING-derivable at journey/screen level',
  "  journey.** In a native app the journey's logon or splash screen satisfies the rule —\n"
  '  "the user summoned an HSBC app, they know where the destination is".\n'
  '  ' + CITE + ' [BLOCKING-derivable at journey/screen level'),
 ('photo26-002', 'brand-refresh-assets.md',
  '  retrieval from licensed libraries, full stop. [BLOCKING-derivable',
  '  retrieval from licensed libraries, full stop. The gen-AI clause carries a review date —\n'
  '  review by 2027-03 — which changes nothing about the ban until then.\n'
  '  ' + CITE + ' [BLOCKING-derivable'),
 ('pict-001', 'pictograms.md',
  "  (unlike icons' universal-meaning carve-out). [BLOCKING-derivable",
  "  (unlike icons' universal-meaning carve-out). The usage boundary: a pictogram supports a\n"
  '  concept; an icon signals an action. ' + CITE + ' [BLOCKING-derivable'),
 ('pict-010', 'pictograms.md',
  '  60px, use an icon instead. [BLOCKING-derivable',
  '  60px, use an icon instead. The figures are consistency and enforcement against misuse by\n'
  '  designers, not a perceptual threshold. ' + CITE + ' [BLOCKING-derivable'),
 ('col26-016', 'colour-standards-2026.md',
  "- **Don't use red typography — red text is reserved for call to actions.** [BLOCKING-derivable —",
  "- **Don't use red typography — red text is reserved for call to actions.** One exception:\n"
  '  RAG red text for downward and RAG green text for upward position movement, stat-card\n'
  '  style — the delta clause under `data-visualisation.md` {#dv-017} ({#dv-019} (a)) carries\n'
  '  the semantics and is not restated here. ' + CITE + ' [BLOCKING-derivable —'),
 ('neuro-026', 'neurodiversity.md',
  '  with all images and icons removed. [BLOCKING-derivable kin',
  '  with all images and icons removed. Carve-out by reference: unpaired icons are allowed\n'
  '  only for the universal set named in `icons.md` ({#icon-004}); pictograms stay\n'
  '  no-exception ({#pict-001}). ' + CITE + ' [BLOCKING-derivable kin'),
]


def main():
    done, already, fail = [], [], []
    for rid, fn, old, new in EDITS:
        p = G / fn
        txt = p.read_text(encoding='utf-8')
        if new in txt:
            already.append(rid); continue
        n = txt.count(old)
        if n != 1:
            fail.append(f'{rid}: anchor matched {n}x in {fn}'); continue
        p.write_text(txt.replace(old, new), encoding='utf-8')
        done.append(rid)
    for f in fail:
        print('FAIL ' + f)
    print(f'edited {len(done)}: ' + ' '.join(done))
    if already:
        print(f'already present {len(already)}: ' + ' '.join(already))
    # col26-012 untouched, by his word
    c = (G / 'colour-standards-2026.md').read_text(encoding='utf-8')
    assert 's282-D1' not in c.split('{#col26-012}')[1].split('{#col26-013}')[0], 'col26-012 touched'
    print('col26-012: untouched (he ruled (c) Discuss first)')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
