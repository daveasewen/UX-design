# #305 lane A2 — build the four new ruling entries (s305-D58..D61) and the status/evidence jobs from Dave's
# 2026-09-28 loose-ends export. Every quoted word of his is read from the export's machine copy, never retyped.
# Writes entry/job files only; the writes go through knowledge/_inscribe_ruling.py (run_writes.sh).
import json, re, os, sys
sys.path.insert(0, 'knowledge')
import _governs as g
EX = 'notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md'
PAGE = 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html'
B5 = 'notes/_subreports/2026-09-27-305-B5-loose-ends.md'
H1 = 'notes/_subreports/2026-09-27-305-H1-records.md'
DRAFT = 'notes/_lanes/304/R4a/drafts/when-rules.proposed.json'
C = 'knowledge/components/'
OUT = 'notes/_lanes/305/A2/entries/'
txt = open(EX, encoding='utf-8').read()
A = json.loads(re.search(r'```json\n(.*?)\n```', txt, re.S).group(1))['answers']
def v(k): return A[k]['verdict']
def at(k): return A[k]['at'].split(' ')[1]
def dec(k): return A[k]['decision'].strip()
q = lambda s: '"' + s + '"'          # a verbatim quote, newlines kept as real newlines (lane A's form, s305-D48)
# "On the page" sentence per when-rule, read from the export's markdown
ONPAGE = {}
for m in re.finditer(r'^## 4c · (\d+) · (.+?)\s*\n_On the page: (.+?)_\s*\n<sub>When-rule · anchor `#dd-(wr-[a-z-]+)`', txt, re.M):
    ONPAGE[m.group(4)] = (int(m.group(1)), m.group(2), m.group(3))
assert len(ONPAGE) == 17, len(ONPAGE)
SAYS0 = ("decision page #305 'The loose ends' (notes/_DECIDE-305-loose-ends-2026-09-27-v1.html, lane B5), exported "
         "2026-09-28 08:05 and received in chat; times are the export's saved stamps")

# ---------------------------------------------------------------- (a) s305-D58 — the four names
D58 = {
 "id": "s305-D58", "date": "2026-09-28", "by": "Dave", "status": "ruled",
 "ruled": ("THE FOUR SETTING-OR-SLOT NAMES `s305-D19` LEFT FOR HIS EYE ARE DECIDED, AS RECOMMENDED: DATA GRID COLUMNS ARE A "
           "SETTING AND DATA GRID FILTERS ARE A SLOT; LIGHTBOX ITEMS ARE A SETTING; STEPPER STEPS ARE A SLOT; TAB BAR ITEMS ARE A "
           f"SETTING. Dave's verdicts, verbatim: data grid {q(v('g2-data-grid'))}, lightbox {q(v('g2-lightbox'))}, stepper "
           f"{q(v('g2-stepper'))}, tab bar {q(v('g2-tab-bar'))} — each takes the page's recommendation. ⬛ WHAT HIS VERDICT TOOK "
           "WITH IT: the page decided all four by one house rule, which was the page's reading (lane B5's, measured on the metas) "
           "and not his words until now — A SLOT TAKES A KIND OF PART; A SETTING TAKES A KIND OF DATA (of the 23 clashes his call-18 "
           "rule settled, the 7 that stayed slots each name a part tier in `accepts`, the 16 that became settings name only a data "
           "capability; 23 of 23). He accepted it by accepting the four. This answers what `s305-D19` left open (\"THE FOUR THE PAGE "
           "LEFT FOR HIS EYE ... ARE NOT DECIDED BY THIS YES and stay his\"); `s305-D19` is not edited. ⬛ THE COSTS THE PAGE NAMED, "
           "TAKEN WITH THE VERDICT: the data grid's applied search terms, today's `filters` setting, need a name of their own once "
           "`filters` is the slot; the tab bar's setting must carry each destination's icon and label, not only the count (3 to 5) "
           "it holds today."),
 "says": (f"{SAYS0}; group 2 'Four names: a setting or a slot?' — 2a (Data grid: columns, and filters; recommend: columns a "
          f"setting, filters a slot) saved {at('g2-data-grid')} — verdict, verbatim: {q(v('g2-data-grid'))} · 2b (Lightbox: items; "
          f"recommend: a setting) saved {at('g2-lightbox')} — verdict, verbatim: {q(v('g2-lightbox'))} · 2c (Stepper: steps; "
          f"recommend: a slot) saved {at('g2-stepper')} — verdict, verbatim: {q(v('g2-stepper'))} · 2d (Tab bar: items; recommend: "
          f"a setting) saved {at('g2-tab-bar')} — verdict, verbatim: {q(v('g2-tab-bar'))}"),
 "governs": [C + 'data-grid.meta.json', C + 'modal-lightbox.meta.json', C + 'stepper.meta.json', C + 'tab-bar.meta.json'],
 "evidence": [EX + '#2a · data grid', EX + '#2b · lightbox', EX + '#2c · stepper', EX + '#2d · tab bar', PAGE, B5,
              'notes/_DECIDE-304-schema-2026-09-26-v1.html'],
}
# ---------------------------------------------------------------- (b) s305-D59 — the ring
D59 = {
 "id": "s305-D59", "date": "2026-09-28", "by": "Dave", "status": "ruled",
 "ruled": ("A RING'S CHART IS SET TO FILL, AND ITS CONTAINER CONSTRAINS IT: BY BEING SMALLER, OR BY HOLDING MORE THAN ONE ELEMENT. "
           f"Dave's words at run 1, verbatim: {q(dec('g1-ring-r1'))}. His ticks on the three candidate-2 runs, verbatim, each the "
           f"page's recommendation: run 1 {q(v('g1-ring-r1'))}, run 2 {q(v('g1-ring-r2'))}, run 3 {q(v('g1-ring-r3'))} (rings in "
           "tiles at 90%, 95% and 48% of the content width; B5 measured again 90.5%, 95.2%, 47.8%). ⬛ WHAT THIS DOES TO `s305-D9`, "
           "READ FROM ITS OWN TEXT (\"A RING'S TILE HUGS THE DRAWING, AND A WHEN-RULE HANDS A DONUT OR PIE A HALF-WIDTH COLUMN\"): it "
           "AMENDS it by addition. The second half is CONFIRMED — the three ticks apply it, and his \"smaller\" container reads as that "
           "narrow column. The first half is AMENDED: \"hugs the drawing\" sizes the tile to the ring; his words size the ring to its "
           "container (\"set to fill\") and put the constraint on the container, which he also lets be met by the container holding "
           "more than one element. `s305-D9` is not edited and its enacted half-width column (`span.cols ≤ 6` in the donut and pie "
           "`when`, 27efb7b6) stands. ⚠ NOT DECIDED HERE: how a chart set to fill squares with ds-030 (a ring is not stretched; "
           "`s305-D9` rests on it) and with his call-8 comment that the donut \"should not be responsive, however this does not mean "
           "that it will be fixed\" — that is open thread W-305n2, which this ruling feeds and does not close."),
 "says": (f"{SAYS0}; group 1 'Candidate 2: the six blanks', part 2 'The rings' — 1d (Run 1: a ring sits in a tile wider than half "
          f"the wall? recommend: agree, it fails) saved {at('g1-ring-r1')} — verdict, verbatim: {q(v('g1-ring-r1'))} · decision, "
          f"verbatim: {q(dec('g1-ring-r1'))} · 1e (run 2; recommend: agree, it fails) saved {at('g1-ring-r2')} — verdict, verbatim: "
          f"{q(v('g1-ring-r2'))} · 1f (run 3; recommend: agree, it passes) saved {at('g1-ring-r3')} — verdict, verbatim: "
          f"{q(v('g1-ring-r3'))}"),
 "governs": [C + 'chart-donut.meta.json', C + 'chart-pie.meta.json', C + 'template-dashboard-bento.meta.json',
             'knowledge/canon/dv-render-donut.js'],
 "evidence": [EX + '#1d · run 1', EX + '#1e · run 2', EX + '#1f · run 3', PAGE, B5, 'notes/_lanes/305/B5/rings.json',
              'notes/_REVIEW-304-candidate-2-2026-09-27-v1.html'],
}
# ---------------------------------------------------------------- (c) s305-D60 — the fifteen when-rules
DRAFTROWS = {r['slug']: r for r in json.load(open(DRAFT, encoding='utf-8'))['rows']}
WR2SLUG = {'wr-filter-bar': 'filter-toolbar-bar', 'wr-footer': 'footer', 'wr-bento': 'template-dashboard-bento',
           'wr-button': 'button', 'wr-breadcrumbs': 'breadcrumbs', 'wr-bar': 'chart-bar', 'wr-headers': 'headers',
           'wr-kpi': 'kpi-tile', 'wr-layout': 'layout-utilities', 'wr-legend': 'legend', 'wr-nav': 'navigations',
           'wr-stat': 'stat-card', 'wr-status': 'status-indicator', 'wr-summary': 'summary', 'wr-view-options': 'view-options'}
accepted = [k for k in ONPAGE if v(k) == 'Accept']
changed = [k for k in ONPAGE if v(k) == 'Change']
assert sorted(changed) == ['wr-list', 'wr-top-nav'], changed
assert len(accepted) == 15 and set(accepted) == set(WR2SLUG), accepted
accepted.sort(key=lambda k: ONPAGE[k][0])
inmeta, draftonly = [], []
for k in accepted:
    s = WR2SLUG[k]; r = DRAFTROWS[s]
    import subprocess
    head = subprocess.run(['git', '--no-optional-locks', 'show', 'HEAD:' + r['meta']], capture_output=True, text=True, check=True).stdout
    (inmeta if json.loads(head).get('when') == r['proposed'] else draftonly).append(s)
parts = []
for k in accepted:
    n, name, sent = ONPAGE[k]
    extra = f"; with his words, verbatim: {q(dec(k))}" if A[k].get('decision', '').strip() else ''
    parts.append(f"4c·{n} {name} (`{WR2SLUG[k]}`): {q(sent)} — {q(v(k))}{extra}")
D60 = {
 "id": "s305-D60", "date": "2026-09-28", "by": "Dave", "status": "ruled",
 "ruled": ("THE FIFTEEN DASHBOARD WHEN-RULES DAVE ACCEPTED ARE HIS WORDING NOW, EACH AS DRAFTED (plan lane 4d; R4a's "
           "`when-rules.proposed.json`). Per part, the page's sentence for the rule and his verdict, verbatim: " + " · ".join(parts) +
           ". ⬛ WHAT THE ACCEPTS TOOK: the page's recommendation, \"accept all seventeen as drafted\", on these fifteen — the drafted "
           "`when` of each row, which the page put to him in plain words (the plain words are lane B5's). With button it takes the "
           "one row the drafting lane added itself (\"the one row that came from the lane, not from your words or the probe\"); with "
           "the bento template it takes the `layout.grammar` field the row needs in knowledge/when-fields.json (not there at HEAD 01fb005a). "
           f"At HEAD 01fb005a, {len(inmeta)} of the fifteen already read in their metas byte for byte as drafted ({', '.join(inmeta)}); "
           f"{len(draftonly)} were draft only there and are to be built ({', '.join(draftonly)}) — lane B6 of this wave is building "
           "them, and the enacting commit stamps this ruling. ⛔ NOT IN THIS RULING: the list rule (4c·4, "
           "`list-items`) and the top-nav shell rule (4c·6, `app-shell-top-nav`) — he answered \"Change\" on both; each is its own "
           "open thread (W-305e1, W-305e2) and neither draft is accepted. The page-title lock-up he wants worked on is open thread "
           "W-305e3; his accept of the page-title rule stands."),
 "says": (f"{SAYS0}; group 4 part 4c 'The dashboard's when-rules' (seventeen rows, recommend: accept all seventeen as drafted) — "
          + " · ".join(f"4c·{ONPAGE[k][0]} {ONPAGE[k][1]} saved {at(k)} — verdict, verbatim: {q(v(k))}"
                       + (f", decision, verbatim: {q(dec(k))}" if A[k].get('decision', '').strip() else '') for k in accepted)),
 "governs": [DRAFTROWS[WR2SLUG[k]]['meta'] for k in accepted] + ['knowledge/when-fields.json'],
 "evidence": [f"{EX}#4c · {ONPAGE[k][0]} · {ONPAGE[k][1]}" for k in accepted] + [PAGE, B5, DRAFT],
}
# ---------------------------------------------------------------- (d) s305-D61 — own-size wording
WF = 'knowledge/guidelines/web-foundations.md'
SENT = "A part keeps its own size on any page. The page arranges parts; it never shrinks them."
assert f"- **{SENT}**" in open(WF, encoding='utf-8').read()
D61 = {
 "id": "s305-D61", "date": "2026-09-28", "by": "Dave",
 "status": ("enacted #305 2026-09-28 — THE WORDING IS ALREADY IN THE TREE at commit e4ff4284: rule webf-036 in "
            "knowledge/guidelines/web-foundations.md reads the accepted sentence byte for byte (checked at HEAD 01fb005a; "
            "`git log -S webf-036` names e4ff4284 as the commit that brought it in, and `s305-D24` was stamped enacted at the same "
            "sha). Nothing was re-worded. The own-size check stays advisory through the cut (`s305-D4`). Stamped at inscription by "
            "lane A2 of #305: a verdict that accepts what is already built carries the building commit as its proof (`s295-D2`)."),
 "ruled": (f"THE OWN-SIZE SENTENCE IS DAVE'S WORDING: {q(SENT)} (rule webf-036). Dave's verdict, verbatim: {q(v('g4-ownsize'))}, "
           f"with his words, verbatim: {q(dec('g4-ownsize'))}. The sentence went into web-foundations.md as the #304 when-rules page "
           "offered it (question 5) under `s305-D24`; it was offered \"for yours\" and had not had his word until now. ⬛ His \"I "
           "thought we'd decided this\" is right about the rule: `s305-D24` (call 23, \"yes\") ruled it and `s305-D57` half A "
           "ratified width with it; the page asked only about the sentence. `s305-D24` is not edited."),
 "says": (f"{SAYS0}; group 4 part 4b 'The own-size rule · call 23' (Accept this sentence, or change it? no recommendation) saved "
          f"{at('g4-ownsize')} — verdict, verbatim: {q(v('g4-ownsize'))} · decision, verbatim: {q(dec('g4-ownsize'))}"),
 "governs": [WF, 'knowledge/_validate_own_size.py'],
 "evidence": [EX + '#4b · own-size rule', PAGE, B5, WF,
              "commit e4ff4284 - rule webf-036 (the accepted sentence) landed in web-foundations.md in #305 wave three (W2's own-size "
              "rule); `s305-D61` accepts its wording, the commit is the proof (`s295-D2`: the sha is the pointer)"],
}
for e in (D58, D59, D60, D61):
    for ev in e['evidence']:
        if g.evidence_form(ev) == 'anchor':
            ln, err = g.resolve_anchor(ev); assert not err, (e['id'], ev, err)
    for p in e['governs']:
        assert os.path.exists(p), (e['id'], p)
    json.dump(e, open(OUT + e['id'] + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('entries ok', 'inmeta', inmeta, 'draftonly', draftonly)
