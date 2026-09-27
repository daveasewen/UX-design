# #305 lane A — compose the s305 ruling entries from Dave's export (verbatim) + the sitting page's calls.
# Writes notes/_lanes/305/A/entries/sNNN.json (one per ruling) and CALL-MAP.json. Writes NOTHING else.
import json, os, re, sys
sys.path.insert(0, 'knowledge')
import _governs
EXPORT = 'notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md'
PAGE = 'notes/_SITTING-304-tuesday-2026-09-29-v1.html'
BRIEF = 'notes/_lanes/305/_COMMON-BRIEF.md'
OUT = 'notes/_lanes/305/A/entries'
md = open(EXPORT, encoding='utf-8').read()
machine = json.loads(md.split('```json', 1)[1].split('```', 1)[0])['answers']
heads = {}
for ln in md.splitlines():
    m = re.match(r'^## (\d\d|41[bce])[a-z]? · (.*?)\s*$', ln)
    m = re.match(r'^## ((\d\d)|(41[bce])) · (.*?)\s*$', ln)
    if m:
        heads[m.group(1)] = ln[3:].rstrip()

def anchor(call):
    h = heads[call]
    cuts = [m.start() for m in re.finditer(r'[ :?,]', h)] + [len(h)]
    for n in cuts:
        if n < 20:
            continue
        a = h[:n].rstrip()
        ln, err = _governs.resolve_anchor(f'{EXPORT}#{a}')
        if not err:
            return a
    raise SystemExit('no unique anchor for ' + call)

def ans(call):
    d = machine['decision-' + (call.lstrip('0') if not call.startswith('41') or call == '41' else call)]
    return d.get('decision', '').strip(), d.get('comment', '').strip(), d['at']

DATE = '2026-09-27'
RULED = 'ruled'
def enacted(sha, what):
    return (f"ENACTED #305 {DATE} — RATIFIES WHAT IS ALREADY IN THE TREE at commit {sha}: {what} "
            f"Stamped at inscription by lane A of #305 on the sitting brief's instruction (a call that ratifies "
            f"something already built carries the building commit as its proof, `s295-D2`'s sha discipline).")
def sha_ev(sha, rid, what):
    return f"commit {sha} - {what}; `{rid}` ratifies it, the commit is the proof (`s295-D2`: the sha is the pointer)"

R = 'notes/_subreports/'
C = []   # (call, ruled, governs, extra_evidence, status, needs_build, build_line, brief_anchor)
def add(call, ruled, governs, extra=(), status=RULED, needs_build=True, build='', brief=None):
    C.append(dict(call=call, ruled=ruled, governs=governs, extra=list(extra), status=status,
                  needs_build=needs_build, build=build, brief=brief))

add('01', "V1.0.14 IS CUT FROM CANDIDATE 2 ON TUESDAY 29 SEPTEMBER, ON THE WAVE-FIVE CANON AND CHART ENGINE, WITH NO NEW COLD RUN — the page's recommendation taken whole. What stands in for a cold run is candidate 2's three runs restaged on the wave-five canon and engine (the page's figures, quoted from its seats: own-size findings 82/104/146 → 0/0/0, ink per view 5.10 → 2.10). The page's reading rides with it: of seat R4s's four conditions, Common's gutter has landed and the other three are calls 4, 5 and 11 of this sitting (`s305-D5`, `s305-D6`, `s305-D12`), so the cut carries whichever of those lands in the same wave, and calls 5–13 and 41b reach the zip if their fix lands before the rebuild. The cut runs the page's recipe: the next wave committed, the candidate rebuilt from that sha, the version stamp that rewrites three historical rulings fixed, the frozen-release gate, CI read back, the zip to Dave's machine. ⚠ THE RATIFICATION WORD FOR v1.0.14 IS A SEPARATE RULING, inscribed at the cut: this ruling decides the cut, it does not ratify the release. Dave's answer, verbatim: \"{A}\".",
    ['knowledge/_release/_gate_frozen_release.py', 'knowledge/_release/_frozen-releases.json', 'knowledge/_release/_gen_pack_manifest.py'],
    [R + '2026-09-27-304-R4s2-candidate-2-scores.md', R + '2026-09-27-304-F5-wave-five-fixes.md'],
    build="Cut v1.0.14 from candidate 2 on Tue 29 Sep by the page's recipe: next wave committed, rebuild from that sha, fix the Gumdrop stamp that rewrites three rulings, frozen-release gate, CI read-back, zip to Dave; ratification word inscribed then")
add('02', "THE GEOMETRY AND OWN-SIZE GATES SHIP IN THE PACK, TOGETHER OR NOT AT ALL, AND THE PACK'S GATE ROSTER IS NAMED 60. Dave's answer, verbatim: \"{A}\" — the recommendation, 'yes, and name 60'. The roster the page names as 58 was held in `knowledge/_release/_gen_pack_manifest.py` under the `s223-D6` lineage before either gate existed, and the manifest tool refuses to move the number by itself; this ruling is the word that moves it. `s223-D6` and `s232-D2` are NOT edited. ⚠ DECLARED, NOT FIXED BY THIS RULING (the page's two riders): the pack's self-tests for these gates cannot run from the zip because the fixtures do not ship (page mode works); and the two ship as a pair because `_validate_own_size.py` borrows `_validate_geometry.py`'s browser harness.",
    ['knowledge/_release/_gen_pack_manifest.py', 'knowledge/_release/_pack_manifest.json', 'knowledge/_validate_geometry.py', 'knowledge/_validate_own_size.py'],
    [R + '2026-09-26-304-R4b-geometry-and-size.md'],
    build="Ship _validate_geometry.py + _validate_own_size.py in the pack as a pair; move the pack gate roster to 60 in the manifest generator/manifest")
add('03', "THE GEOMETRY AND OWN-SIZE GATES STAY ADVISORY THROUGH THE V1.0.14 CUT; WHETHER EITHER BLOCKS IS LOOKED AT AGAIN AFTER ONE COLD RUN HAS BEEN BUILT UNDER THEM. Dave's answer, verbatim: \"{A}\" — the recommendation's own words. The reason on the page: the reference bento itself reads 17 true findings at 390, so blocking today turns the library red before anything was built for a phone. ⚠ The re-look after one cold run is OWED and is not discharged by this ruling's stamp; under `s305-D1` this call is listed for re-review at a later sitting.",
    ['knowledge/_validate_geometry.py', 'knowledge/_validate_own_size.py', 'knowledge/_build_all.py'],
    [R + '2026-09-26-304-R4b-geometry-and-size.md', R + '2026-09-27-304-C2-commit-seat-wave-two.md',
     sha_ev('4be130e5', 's305-D4', 'both gates built ADVISORY (#304 wave two, build steps 147-148, exit 77 declared; CI 36275037261)')],
    status=enacted('4be130e5', "both gates entered the build ADVISORY in #304 wave two (steps 147–148, exit 77 declared, CI 36275037261 read back as designed) and have stayed advisory through 3100da99, 52049781 and 8a5fa863. The wave's one new red, [121], was the chain's step-count figure and went green at 86249459; it is not this gate's. Nothing to build; the re-look after one cold run under them stays owed."),
    needs_build=False, build="Nothing now — already advisory since 4be130e5; re-look owed after one cold run built under them", brief='call 3 "advisory through the cut"')
add('04', "A CHART REGION'S RECEIPT NAMES `knowledge/canon/dv-render.js` — THE META'S ANSWER — AND THE MINT FOLLOWS THE META. Dave's answer, verbatim: \"{A}\" — option (a), which seat W5a and the page both recommended. The mint (`gen_provenance_receipt.behaviour_address`) reads the chart meta's `script` line instead of taking the first registered behaviour block in the snippet's order (today `dv-behaviour.js`); one function, no meta or page changes. Consistent with `s234-D5` (the meta owns the behaviour address) and `s260-D1` (dv-render.js is the core, priced once per page); neither is edited. The receipt gate's FAIL:BEHAVIOUR-ADDRESS-DISAGREES on pack-minted chart regions closes once the two agree.",
    ['knowledge/gen_provenance_receipt.py', 'knowledge/_validate_receipt.py'],
    [R + '2026-09-27-304-W5a-gate-bugs-and-trim.md'],
    build="gen_provenance_receipt.behaviour_address reads the chart meta's script (dv-render.js); receipt gate green on composed charts")
add('05', "THE KPI LABEL CROP IS FIXED IN THE CLIP-VISIBLE FORM: descenders whole, the 22px label-to-value lock-up Dave ruled at #261 kept, the ellipsis kept, the tile at 155px; the descender gate gains one small leg that knows this form (today it knows only the trim form). Dave's answer, verbatim: \"{A}\" — the recommendation, read by the conductor as the clip-visible form and put to Dave in chat. NOT the trim form, which also clears the crop but grows the label box 14 → 18px so the value sits 4px lower and the tile 4px taller (label to value 26px, tile 159px), against his \"as tight as the original\" (`s261-D4`). `s261-D4` is kept, not amended; the ruled trim form (the page's ds-005) is not edited and stands where it applies — this ruling takes the other form for the KPI tile's label only.",
    ['knowledge/snippets/Kpi-tile.reference.html', 'knowledge/components/kpi-tile.meta.json', 'knowledge/canon/canon.css', 'knowledge/_validate_descender_clip.py'],
    [R + '2026-09-27-304-V3-verifier-wave-three.md', 'notes/_lanes/304/W3a/held-back/README.txt'],
    build="KPI tile label in the clip-visible form (V3's alternative; lock-up 22px, tile 155px, ellipsis kept) + one descender-gate leg for that form",
    brief='call 5 "as recommended" = the CLIP-VISIBLE form')
add('06', "LABEL THINNING IS RATIFIED, ALL THREE PARTS, INSCRIBED AS ONE RULING AS THE PAGE ASKED: category and date labels MAY be hidden (every category stays in the chart's table and in every mark's tip), the clearance is 8px, and the LAST category is the anchor. The right-hand twin is ratified with it, as the page says a yes does: the plot's right edge follows the widest label as the left does under ds-012(b), with the same two provisional numbers Dave left to his eye there. Dave's answer, verbatim: \"{A}\". ⚠ THE TENSION STAYS DECLARED, NOT RESOLVED: an advisory brand rule asks for a label per category (the page's dv-line-003 / dv-010). ⬛ HIS COMMENT, VERBATIM, IS NOT PART OF THIS RULING — it opens a thread (store row W-305n1, his) on labelling rules for complex charts: \"{C}\"",
    ['knowledge/canon/dv-behaviour.js', 'knowledge/canon/dv-render.js'],
    [R + '2026-09-27-304-W4a-chart-engine-ink.md', R + '2026-09-27-304-V4-verifier-wave-four.md', R + '2026-09-27-304-W5a-gate-bugs-and-trim.md',
     sha_ev('3100da99', 's305-D7', 'label thinning built WITHOUT a ruling and declared in the commit body (#304 wave four, W4a, on V4\'s recommendation)'),
     sha_ev('52049781', 's305-D7', 'the right-hand twin (right chart gutter computed from labels, ds-012b twin) built in #304 wave five (W5a, verified V5)')],
    status=enacted('3100da99', "the thinning (hide allowed, 8px clearance, last-category anchor) was built WITHOUT a ruling in #304 wave four and declared in that commit's body; the right-hand twin landed at 52049781 (wave five). CI at both read back with the predicted reds only, 0 green to red. His comment opens thread W-305n1; nothing here to build."),
    needs_build=False, build="Nothing — built at 3100da99 (thinning) and 52049781 (right-hand twin); the complex-chart labelling thread is W-305n1")
add('07', "DENSE SERIES: ABOVE 12 POINTS A SERIES DRAWS ITS END MARKER ONLY, AND A STACKED AREA CARRIES ONE LETTER PER BAND — 12 is RULED. Dave's answer, verbatim: \"{A}\" — the recommendation, 'yes, at 12'. 12 is the count the marker recipe was authored at and the count the geometry gate's G11 already declares (declared, never ruled until now). The brand rule gives the behaviour (end-line markers, and a key when markers would obscure small intervals); the one-letter-per-band half changes a reviewed recipe, which is why it needed his word.",
    ['knowledge/canon/dv-render-line.js', 'knowledge/canon/dv-render-stacked-area.js', 'knowledge/canon/dv-render.js', 'knowledge/_validate_geometry.py'],
    [R + '2026-09-27-304-W4a-chart-engine-ink.md'],
    build="Engine marker rule: >12 points = end marker only, one letter per band (stacked area); mark geometry G11's 12 as ruled")
add('08', "A RING'S TILE HUGS THE DRAWING, AND A WHEN-RULE HANDS A DONUT OR PIE A HALF-WIDTH COLUMN, THE LEGEND UNDER THE RING. Dave's answer, verbatim: \"{A}\" — the recommendation ('hug, and a when-rule that hands a donut or pie a half-width column'). It rests on ds-030 (a ring is not stretched; the page reads it as fixed-diameter), which is not edited. ⬛ HIS COMMENT, VERBATIM, QUALIFIES THAT READING AND OPENS A THREAD (store row W-305n2, his) — it is not decided here: \"{C}\"",
    ['knowledge/components/chart-donut.meta.json', 'knowledge/components/chart-pie.meta.json', 'knowledge/components/template-dashboard-bento.meta.json', 'knowledge/canon/dv-render-donut.js'],
    [R + '2026-09-27-304-W4a-chart-engine-ink.md'],
    build="Ring tile hugs the drawing; when-rule on donut/pie metas hands them a half-width column with the legend under the ring")
add('09', "THE GROUND: IN LIGHT, THE PAGE AND THE TITLE AREA ARE WHITE AND THE BENTO SECTION TAKES THE LIGHTEST GREY; IN DARK, THE SECTION SITS ONE STEP BELOW THE TILES, THAT STEP MINTED FROM THE TOKEN LADDER, NOT TYPED. Dave's answer, verbatim: \"{A}\". The light half is his Thursday 24 September sentence (\"this doesn't mean the full page\"). ⚠ AMENDS `s219-D1`'s SHIPPED DASHBOARD DEFAULT (the 25 August export that set the page ground grey and the bento's own ground clear) WITHIN `s219-D3`'s RAILS, as the when-rules page reads it — `s219-D3` (page ground is the page's decision, bento ground the section's) is not contradicted, and neither entry is edited. In dark today section and tiles are both #1F1F1F, so the tiles have no edge.",
    ['knowledge/canon/gen_canon_bento.py', 'knowledge/canon/gen_bento_role_vars.py', 'knowledge/canon/canon.css'],
    ['notes/_DECIDE-304-when-rules-2026-09-26-v1.html'],
    build="Light: page + title white, bento section lightest grey; dark: section one ladder step below tiles, minted not typed (rails + tokens)")
add('10', "THE MUTED LABELS IN COMMON TAKE A SOLID INK THAT READS AT LEAST 4.5:1, REPLACING THE TRANSPARENCY. Dave's answer, verbatim: \"{A}\". Measured on the page: the KPI label and period 3.71:1 and the side-nav group label 3.75:1, on 14px text that needs 4.5:1; the cause is an alpha on the ink, which the #99 licence reserves for state changes only — this ruling brings the labels inside that licence and does not amend it. The grey it becomes is Dave's by eye at the wrap.",
    ['knowledge/canon/canon.css', 'knowledge/canon/gen_canon_tokens.py'],
    [],
    build="Common theme: replace the alpha on the muted label ink (KPI label/period, side-nav group label) with a solid ink >= 4.5:1; grey to Dave's eye at the wrap")
add('11', "THE APP SHELL GAINS A FULL-HEIGHT FORM, AND 640PX STAYS AS THE SPECIMEN FRAME; THE COMPONENT AND THE SKILL MOVE TOGETHER. Dave's answer, verbatim: \"{A}\". The case on the page: six of nine cold runs shipped the side-nav shell as a 640px box with 360px of blank under it at 1440, because the skill's own rule against resizing a part (the page's `s230-D1` rule 3a) kept it there. The skill gains one line naming the full-height form; `s230-D1` is not edited.",
    ['knowledge/components/app-shell-side-nav.meta.json', 'apollo-spider/skills/generate-from-canon/SKILL.md'],
    [],
    build="Add a full-height form to the app shell (side-nav) component, keep 640px as the specimen frame, and one skill line naming it")
add('12', "THE NAV BADGE MOVES FROM 7PX TO 8PX, ON THE 4PX GRID — NO EXEMPTION. Dave's answer, verbatim: \"{A}\" — the recommendation. It moves two pixels on two-digit counts (\"12\" grows 27.9 → 29.9px wide) and none on one; an exemption would have been the grid check's first spacing exception. It closes the CI red the page calls [81].",
    ['knowledge/components/badge.meta.json', 'knowledge/snippets/Badge.reference.html', 'knowledge/snippets/Sidebar-nav.reference.html', 'knowledge/_validate_grid.py'],
    ['notes/_DECIDE-304-ci-calls-2026-09-26-v1.html'],
    build="Nav badge 7px -> 8px (component + snippets); closes CI red [81]")
add('13', "THE CONSOLE RADIUS SET IS ACCEPTED BY EYE: CONTROL 6, SURFACE 8, CONTAINER 12, WITH THE CARD PADDING THE DERIVATION LAW BRINGS WITH IT (20 → 8). Dave's answer, verbatim: \"{A}\". The values are his 3 September numbers (`s245-D10`, console theme only), built and stamped in #304 wave two; the padding follows `s201-D4` / `s200-D1`(c) without moving a pixel (nothing reads that token yet); the other three themes are pixel-identical before and after. His eye closes the row; `s245-D10` is not edited.",
    ['knowledge/canon/canon.css', 'knowledge/canon/gen_theme_cascade.py'],
    [R + '2026-09-27-304-C2-commit-seat-wave-two.md',
     sha_ev('4be130e5', 's305-D14', 'the console radius set (s245-D10) and the derived card padding built in #304 wave two, stamped enacted at aaf3bb7e')],
    status=enacted('4be130e5', "the console radius set of `s245-D10` (control 6, surface 8, container 12) and the card padding 20 → 8 were built in #304 wave two and `s245-D10` stamped enacted at aaf3bb7e; this ruling is his eye accepting the built result. Nothing to build."),
    needs_build=False, build="Nothing — built at 4be130e5 (s245-D10 stamped at aaf3bb7e); his eye closes the row")
add('14', "THE SCHEMA ACCEPTS A PART'S STATES, IN ONE SHAPE: A LIST OF STATE NAMES (ready, loading, empty, error, stale) WITH ONE SENTENCE PER STATE. Dave's answer, verbatim: \"{A}\" — 'widen the schema, one shape'. A live screen has to draw loading, empty and error as well as ready, and a catalogue can only carry what the schema allows; four of the thirteen schema errors are this. With `s305-D16` it closes the CI reds the page calls [94] and [132] (renumbered [98] and [136] after #304 wave five).",
    ['knowledge/components/meta.schema.json'],
    ['notes/_DECIDE-304-schema-2026-09-26-v1.html'],
    build="Widen meta.schema.json: states = list of names + one sentence each (ready/loading/empty/error/stale)")
add('15', "THE OTHER NINE SCHEMA ERRORS ARE CLOSED BY BRINGING THE METAS BACK TO THE SCHEMA, ALL NINE: the data grid's six companions as slug objects, its composes list into the existing `subComponents` field, the legend's provenance to \"code\", and its when-note to a note with a `recommends` link. Dave's answer, verbatim: \"{A}\". A catalogue never reads these fields and the schema already has a legal place for each (the page cites `s251-D6`). With `s305-D15` this closes CI reds [94] and [132] (renumbered [98] and [136]).",
    ['knowledge/components/data-grid.meta.json', 'knowledge/components/legend.meta.json', 'knowledge/components/meta.schema.json'],
    ['notes/_DECIDE-304-schema-2026-09-26-v1.html'],
    build="Fix the nine metas to the schema (data-grid companions as slugs, composes -> subComponents, legend provenance 'code', when-note -> note + recommends)")
add('16', "A PART'S OWN TEXT IS A FIELD ON THE PART — THE BUTTON'S LABEL, THE HEADER'S TITLE — NOT A SEPARATE TEXT PART INSIDE IT; 45 PARTS GAIN ONE. Dave's answer, verbatim: \"{A}\" — the recommendation. Because the words are checked with the part: the label's length, its wrap, the 44px target and the name a screen reader hears.",
    ['knowledge/components/meta.schema.json'],
    ['notes/_DECIDE-304-schema-2026-09-26-v1.html'],
    build="Schema text field on the part; add it to the 45 metas that need one")
add('17', "FOUR PARTS SIDE BY SIDE ARE HELD BY APOLLO'S BENTO WALL, WITH A TILES SLOT THAT ACCEPTS PARTS BY WHAT THEY PROVIDE — NOT BY A2UI'S ROWS AND COLUMNS. Dave's answer, verbatim: \"{A}\" — the recommendation. The spans, the gutters and the no-orphan rule are ruled on the wall and A2UI's rows and columns know none of them (the page cites `s140-D1`, not edited).",
    ['knowledge/components/template-dashboard-bento.meta.json', 'knowledge/components/meta.schema.json'],
    ['notes/_DECIDE-304-schema-2026-09-26-v1.html'],
    build="Bento wall meta gains a tiles slot that accepts parts by `provides`")
add('18', "ONE RULE FOR A PART THAT NAMES A SETTING AND A SLOT THE SAME: DATA IS A SETTING BOUND TO A DATA SHAPE; A SLOT ONLY EVER HOLDS ANOTHER PART. Dave's answer, verbatim: \"{A}\" — the recommendation. Of the 27 clashes, 16 read as settings and 7 as slots under it. ⚠ THE FOUR THE PAGE LEFT FOR HIS EYE ON THE SCHEMA PAGE — data grid, lightbox, stepper, tab bar — ARE NOT DECIDED BY THIS YES and stay his.",
    ['knowledge/components/meta.schema.json'],
    ['notes/_DECIDE-304-schema-2026-09-26-v1.html'],
    build="Apply the rule to 23 clashes (16 settings, 7 slots); put data grid, lightbox, stepper, tab bar to Dave's eye")
add('19', "THE FIVE BETA DASHBOARD PARTS GO INTO THE PROOF-OF-CONCEPT CATALOGUE, ALL FIVE, MARKED AS PROPOSALS, WITH EVERY SCREEN'S RECORD NAMING ANY IT USED. Dave's answer, verbatim: \"{A}\". ⛔ HIS COMMENT IS PART OF THE RULING, VERBATIM: \"{C}\" — the beta parts are EVIDENCE, never a tracing source. The page cites `s182-D2` (not edited). The catalogue is built on `s305-D50`'s timing.",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    ['notes/_DECIDE-304-schema-2026-09-26-v1.html'],
    needs_build=False, build="Nothing before the PoC catalogue (October, s305-D50): then the five beta parts ship marked as proposals, evidence not a tracing source")
add('20', "THE LINE CHART'S RULE GAINS TWO CLAUSES: SAME UNITS, AND ONE TO FIVE LINES OVER TIME. Dave's answer, verbatim: \"{A}\". The chart's own sentence already says it gives way when units differ or when all four prices are the point; the clauses let the chooser read it (with them the rules-only chooser picked 19 of 20 in the probe).",
    ['knowledge/components/chart-line.meta.json'],
    ['notes/_DECIDE-304-when-rules-2026-09-26-v1.html'],
    build="chart-line meta when-rule: + 'same units' and + 'one to five lines over time'")
add('21', "THE CHOOSER ALSO READS EACH PART'S OWN QUESTION AND DATA SHAPE, NOT ONLY ITS WHEN-RULE. Dave's answer, verbatim: \"{A}\". Those two fields are already the one home he ruled for a part's question and shape, so reading them adds no second source.",
    ['knowledge/components/meta.schema.json', 'notes/_lanes/304/R5/when_eval.py'],
    ['notes/_DECIDE-304-when-rules-2026-09-26-v1.html'],
    build="Chooser reads each meta's `answers` and data shape alongside the when-rule")
add('22', "THE DATA GRID GETS A WHEN-RULE, WITH A NEW FIELD `needs` (sort, filter, select, edit). Dave's answer, verbatim: \"{A}\". The list's own rule already says it yields to the grid when any of the four is required, and nothing could read that until now.",
    ['knowledge/components/data-grid.meta.json', 'knowledge/components/meta.schema.json'],
    ['notes/_DECIDE-304-when-rules-2026-09-26-v1.html'],
    build="data-grid when-rule + new schema field `needs` (sort/filter/select/edit)")
add('23', "THE GRAPH SAYS A PART IS ALWAYS DRAWN AT ITS OWN REFERENCE SIZE, AND THE OWN-SIZE GATE IS THE CHECK THAT MEASURES IT. Dave's answer, verbatim: \"{A}\". The check exists (`knowledge/_validate_own_size.py`, advisory by `s305-D4`); this is the rule it enforces. ⚠ ITS FIRST CONSEQUENCE AT THE ROOT — whether canon's default label trim reaches into the twelve components that carry none of their own — IS NOT TAKEN BY THIS YES: Dave answered that separately at call 41c, keep today's through the cut (`s305-D43`).",
    ['knowledge/gen_kg_rules.py', 'knowledge/_validate_own_size.py'],
    ['notes/_DECIDE-304-when-rules-2026-09-26-v1.html'],
    build="Add the own-reference-size rule to the graph, citing _validate_own_size.py as its check")
add('24', "THE GRAPH SAYS A MODAL GIVES WAY TO A SPLIT BUTTON OR A DROP-DOWN WHEN EITHER WOULD DO — AS A PROPOSED RULE WITH 'GIVES WAY TO' LINKS; THE WORDING IS DAVE'S. Dave's answer, verbatim: \"{A}\". Today the three have no when-rule and no such links, so the graph had nowhere to say it.",
    ['knowledge/components/modals.meta.json', 'knowledge/components/split-button.meta.json', 'knowledge/components/dropdown.meta.json'],
    ['notes/_DECIDE-304-when-rules-2026-09-26-v1.html'],
    build="Proposed rule + 'gives way to' links modal -> split button / drop-down; the wording goes to Dave")
add('25', "STEP 5'S SCHEMA DIFF IS RATIFIED: THE FOUR EDGE TYPES setIn, behaviourFrom, capturedFrom AND acceptsCapability GO IN; LIFECYCLE STATUS IS A FIELD, NOT A KIND; CONTENT STANDARD IS PARKED. Dave's answer, verbatim: \"{A}\". This discharges `s269-D1`'s ratification clause for step 5 (steps 1–4 each had their diff; step 5 had none and stopped there). ⚠ AMENDS `s269-D6`, which put two new entity kinds in scope: lifecycle status becomes a field (as `s263-D12` already has it on variants), and content standard is parked because it has no source to map. Neither earlier entry is edited.",
    ['knowledge/gen_kg_edges.py', 'knowledge/_build_kg_explorer.py'],
    [R + '2026-09-26-304-R3-ruled-now-built.md'],
    build="Four step-5 edge types into the KG generators and explorer; lifecycle as field; content standard parked")
add('26', "THE NOTIFICATION BORDER FOR LEGACY AND SUPERCHARGE IS ONE NUMBER TOKEN DRAWN WITH THE VARIANT'S OWN COLOUR — NOT FOUR COLOUR TOKENS PER THEME. Dave's answer, verbatim: \"{A}\" — the recommendation. It keeps the 1px slot `s135-D1` asks for and adds one name, not twelve; `s135-D1`'s radius half is already live and its border half stopped at its own clause, which this discharges. ⚠ THE TOKEN'S NAME IS STILL DAVE'S by the #145 precedent (`s145-D1`); this yes does not name it.",
    ['knowledge/snippets/Notifications.reference.html', 'knowledge/components/notifications.meta.json', 'knowledge/canon/gen_theme_cascade.py'],
    [R + '2026-09-26-304-R3-ruled-now-built.md'],
    build="Mint one border-width number token through the cascade, drawn in each variant's colour (legacy, supercharge); the name to Dave")
add('28', "THE CONTEXT WINDOW LINES ARE INSCRIBED: WORKING LINE 256,000, HARD LINE 300,000; UNDER THEM THE STOP LINE MOVES TO 236,000 AND THE TOLERANCE LINE TO 276,000. Dave's answer, verbatim: \"{A}\". The two window lines are his own words of 23 September as the housekeeping page quotes them (\"Lets try 300k and cross our fingers\" · \"200k isnt enough make it 256\"), acts in the handoffs until now, not inscribed rulings — and a line that is not inscribed is one no gate can read. ⚠ SUPERSEDES the stop and window figures of `s271-D1` (one stop line, 180,000), `s272-D93` (180,000 working, about 220,000 tolerated, 256,000 hard) and `s260-D2` (200,000 working wall, 256,000 hard wall). None of the three is edited; this ruling crosses their numbers out.",
    ['knowledge/_gauge_tokens.py', 'knowledge/_capture_gate.py'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="_gauge_tokens: working 256,000, hard 300,000, stop 236,000, tolerance 276,000; gates read them")
add('29', "THE BOOT CEILING IS 130,000 UNTIL THE MAC SEAT; THEN IT IS MEASURED THERE AND SHRUNK. Dave's answer, verbatim: \"{A}\". ⚠ SUPERSEDES `s295-D3` (the ceiling re-based to 72,768, shrink-only from there) for the period until the Mac seat — his word over his own word twice, as the page put it: \"I can't cut anything else permanently, this is possibly the new ceiling\" (#295) and his choice of the window over the ceiling at 19:47 on #301. The case: the cloud seat boots at about 128,000 (126,767 measured 23 September), so every wrap since #297 has gone on the declared not-a-wrap path and the check reads nothing. After the Mac seat (planned for the second half of October) the ceiling is re-measured there and shrinks; shrink-only (`s240-D2`/`s241-D1`) resumes from that reading. `s295-D3` is not edited. ⬛ HIS COMMENT, VERBATIM, OPENS A THREAD (store row W-305n3, his): \"{C}\"",
    ['knowledge/_gauge_tokens.py', 'knowledge/_capture_gate.py'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="BOOT_CEILING_TK 72,768 -> 130,000 until the Mac seat (then re-measure and shrink); wraps return to the wrap path")
add('30', "THE PUSH TOKEN LEAVES THE REMOTE ADDRESS FOR A CREDENTIAL HELPER BEFORE THE NEXT PUSH. Dave's answer, verbatim: \"{A}\". The token sits in plain text inside the repo's remote address, so anything that prints the address can print the token; a helper keeps it out. The credential's expiry (6 November, `s294-D5`) is unchanged and re-issuing it still takes Dave's hands.",
    ['knowledge/_git_commit.sh'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Move the GitHub token out of the remote URL into a credential helper before Tuesday's push")
add('31', "THE 95 DECK, DRAWING AND PRESENTATION ROWS WHOSE CLOSE IS \"FRIDAY'S DECK IS FINAL\" ARE CLOSED; EVERY FILE STAYS. Dave's answer, verbatim: \"{A}\". They are records, not questions. What came back from Friday is recorded separately in his words at notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md.",
    ['knowledge/_state.json'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Close the 95 deck/drawing/presentation rows through the sanctioned _state writer, receipts quoted")
add('32', "THE 102 RULING-SHAPED QUESTIONS TWO WEEKS OLD OR MORE ARE PARKED, EACH WITH A TRIPWIRE — AND SURFACED FOR DAVE TO SCAN. Dave's answer, verbatim: \"{A}\" — the recommendation with a condition he added: the park is not silent. Parked costs nothing and loses nothing; anything he names in one line after his scan stays open. The surfacing is owed by the conductor (store row W-305n5).",
    ['knowledge/_state.json', 'knowledge/_parked.json'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Park the 102 with tripwires AND build Dave a scan page/list of them (W-305n5)")
add('33', "THE 22 RELEASE ROWS FOR v1.0.1 TO v1.0.12 ARE CLOSED AS SUPERSEDED BY v1.0.13. Dave's answer, verbatim: \"{A}\". They are records of cuts already made; the v1.0.14 cut is `s305-D2`.",
    ['knowledge/_state.json'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Close the 22 release rows as superseded by v1.0.13")
add('34', "DAVE'S 17 ROWS WHOSE CLOSING EVENT HAS ALREADY HAPPENED ARE CLOSED, EACH WITH ITS RECEIPT QUOTED. Dave's answer, verbatim: \"{A}\". A wrap landed, a report was filed or a push went through, and the row only waited for someone to say so.",
    ['knowledge/_state.json'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Close the 17 rows, each closed_by quoting its receipt")
add('35', "THE 14 OLDEST ROWS WITH NO CLOSE CONDITION TAKE THE DISPOSITION PROPOSED FOR EACH, AS ONE BATCH: three close outright, four fold into rows that exist, and the rest get a close a script can check. Dave's answer, verbatim: \"{A}\". The rows are the inherited unconditioned set (`_state.LEGACY_IDS`), which may only shrink; the per-row dispositions are the housekeeping page's table, and rows it marks 'estimate' rest on later text, not a probe.",
    ['knowledge/_state.json', 'knowledge/_state.py'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Apply the housekeeping page's per-row disposition to the 14 legacy rows in one batch")
add('36', "THE CARRY DIET: 342 OF THE 709 ITEMS LEAVE THE LIVE CARRY LIST. They stay in history, and recurring series keep one line each. Dave's answer, verbatim: \"{A}\". Nearly half the live list is struck-through, boilerplate, fragments and repeats, and it hides the 367 that are real.",
    ['_CARRIES.md', 'knowledge/_capture_gate.py'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Cut 342 items from the live carry list (history kept; recurring series one line each)")
add('37', "THE 12 COMPONENT-WAVE ROWS AND THE 20 DECISION PAGES WHOSE EXPORT NEVER CAME BACK ARE PARKED, WITH THE TRIPWIRE \"REOPEN WHEN THE CATALOGUE LISTS THE COMPONENT\". Dave's answer, verbatim: \"{A}\". Each page is still there if he wants it.",
    ['knowledge/_state.json', 'knowledge/_parked.json'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Park the 12 rows + 20 pages with the tripwire 'reopen when the catalogue lists the component'")
add('38', "THE 109 UNCERTAIN BACK-STAMPS ARE SETTLED IN THE PAGE'S SIX KINDS, ALL SIX: done through a later ruling (6), superseded (10), in force with nothing to build (14), part-enacted with the open half parked (7), added to the not-built list (8), and stamped by a probe lane on a file-and-line receipt after Tuesday (64, one Opus lane plus a checking seat that did not stamp). Dave's answer, verbatim: \"{A}\". Each id is sorted into exactly one kind on the uncertain-stamps page. ⚠ NOT ANSWERED BY THIS YES: for the eight with no trace, the page asked him for the two green values or to say they were settled; that is still his.",
    ['knowledge/_rulings.json', 'knowledge/_inscribe_ruling.py'],
    ['notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html'],
    build="Stamp/sort the 109 by kind via _inscribe_ruling --set-status; the 64 by a probe lane after Tuesday on file-and-line receipts")
add('39', "RETIRE, PARK, YES: THE LIBRARY-SHAPE REQUIREMENT IS RETIRED AS OVERTAKEN BY THE THREE-AXIS MODEL; THE CITATION GATE AND THE SPANS DIAL ARE PARKED WITH TRIPWIRES; THE TWO PARKED DECLINES THAT LATER RULINGS ANSWERED MOVE TO ENACTED. Dave's answer, verbatim: \"{A}\". (1) `s135-D3` (8 August: a fully hierarchical library, atoms up to templates) is SUPERSEDED — retired, never given a mechanism; `s136-D1`'s three-axis model is the mechanism the record uses. (2) `s114-D2` (the citation gate) is parked, reopening when the next gate is added; `s246-D3` (the spans dial, a trial) is parked, reopening when bento edit mode is built — both parked, not superseded. (3) P-272-1 (list against card, answered by the six rulings of 15 September) and P-277-4 (the logo review, answered by his export of 18 September) move to enacted in the parked register. None of the earlier entries is edited.",
    ['knowledge/_parked.json', 'knowledge/_rulings.json'],
    ['notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html'],
    build="Mark s135-D3 retired/superseded, park s114-D2 + s246-D3 with tripwires, P-272-1 + P-277-4 -> enacted in _parked.json")
add('40', "THE STORE STOPS REGROWING: DOCUMENT ROWS ARE CLOSED AT BIRTH FROM NOW, AND THE REGROWTH CHECK IS TURNED ON ONCE THE 75 STANDING DOCUMENT ROWS ARE CLOSED OR PARKED. Dave's answer, verbatim: \"{A}\". The store opened 169 rows in twenty sessions and closed 4 before the weekend; turned on today the check would stop every wrap, so it goes on after the batches of `s305-D31`–`s305-D37` land.",
    ['knowledge/_state.py', 'knowledge/_state.json'],
    ['notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
    build="Close doc rows at birth now; flip the _state regrowth arm to blocking once the 75 are closed/parked")
add('41', "DECLARE, PORT NOW, RETIRE: THE FOUR INK FORKS ARE DECLARED AS MEANT; THE CHAIN SCRIPT IS PORTED INTO THE PACKAGE NOW; THE SEVEN ONE-OFF DECK CHECKERS ARE RETIRED. Dave's answer, verbatim: \"{A}\". The forks, as the page corrected them: three chart colour forks and one table cell-padding fork, each doing a job (fills take the lighter tone, thin lines the darker, compact rows are meant tighter); \"declare\" closes the fork ban the page calls [86] (renumbered [90]). The port copies `knowledge/_gen_chain.py` into the Memento package's two copies, closing [127] and [128] (renumbered [131] and [132]). The checkers checked deck v7 and nothing calls them; they move to an archive folder, nothing deleted.",
    ['knowledge/_gen_chain.py', 'memento-package/machinery/_gen_chain.py', 'memento-package/claude-plugin/memento/machinery/_gen_chain.py'],
    ['notes/_DECIDE-304-ci-calls-2026-09-26-v1.html'],
    build="Declare the 3 chart + 1 table forks (closes [86]/[90]); copy _gen_chain.py into both package copies (closes [127][128]); move 7 deck checkers to an archive folder")
add('41b', "A KPI TILE INSIDE THE BENTO KEEPS ITS OWN 40PX SPARKLINE; THE BENTO'S 44PX RULE STOPS REACHING IT. Dave's answer, verbatim: \"{A}\" — the recommendation, which reads call 23 (`s305-D24`: a part is drawn at its own size wherever it sits). The fix is one line in the bento, not a generator rule, because the general cure would also cut the bento's deliberate rules for its children (the fitted chart, the ring rule). Measured on candidate 2's third run: 44 against 40.",
    ['knowledge/snippets/Template-dashboard-bento.reference.html', 'knowledge/canon/gen_canon_bento.py'],
    [R + '2026-09-27-304-W5a-gate-bugs-and-trim.md'],
    build="One line in the bento so a nested KPI tile keeps its 40px sparkline (not the bento's 44px)",
    brief='call 41b "40px, the tile\'s own"')
add('41c', "CANON'S DEFAULT LABEL TRIM STAYS AS TODAY'S THROUGH THE V1.0.14 CUT. Today's is what #304 wave five shipped: the root default as it was, with only the fourteen chart scopes putting the trim back so legends, Reset and chart tables sit at their own size (seat F5 measured 88 pages against HEAD; every changed text part is inside a chart). W5a's held-back version, whose default stops at every component (notes/_lanes/304/W5a/held-back/), is NOT taken now. Dave's answer, verbatim: \"{A}\" — the recommendation's own words. The page's rider: the held-back version comes back only with call 23 (`s305-D24`, now yes) AND his eye on the pairs; under `s305-D1` this call is listed for re-review after the cut.",
    ['knowledge/canon/canon.css'],
    [R + '2026-09-27-304-F5-wave-five-fixes.md', R + '2026-09-27-304-V5-verifier-wave-five.md', 'notes/_lanes/304/W5a/held-back/root-default-bounded.patch',
     sha_ev('52049781', 's305-D43', "today's trim (root default unchanged, fourteen chart-scope restores) built in #304 wave five, narrowed by F5, verified V5")],
    status=enacted('52049781', "today's label trim — the root default unchanged and the fourteen chart-scope restores — is what #304 wave five shipped (F5's narrowing, verified by V5; CI 36306939769 with the predicted reds plus [117], a live-state index red closed at 8a5fa863 and not this change's). Keeping it is the ruling; nothing to build before the cut. The held-back root version waits for re-review after the cut."),
    needs_build=False, build="Nothing before the cut — today's trim is in the tree at 52049781; held-back root version re-reviewed after the cut",
    brief='call 41c "keep today\'s through the cut"')
add('41e', "THE EXPLORER'S CANVAS PRINTS THE CODE ALONE; THE TITLE STAYS WHEREVER ONE READS RATHER THAN SCANS — SEARCH, THE RULING PANEL AND INSPECT — AND THE 49 LABELS STILL BARE ARE TITLED. Dave's answer, verbatim: \"{A}\" — the recommendation: code alone on the canvas, the title everywhere you read, and yes to titling the 49. ⚠ THIS IS NOT THE CANVAS AS BUILT: #304 wave five (52049781) prints code AND title on the canvas, cut at 34 characters, so a dug ruling's neighbours print `#133 session of 2026-…`; this ruling changes that one template line back to code alone. The 49 are 30 polarities (titled from their mediating variable), 13 WCAG guidelines (WCAG's own names) and 6 artefacts — each one more kind in `knowledge/gen_kg_titles.py`. Titles as a derived display from the node's own record are ratified by `s305-D56`.",
    ['knowledge/_build_kg_explorer.py', 'knowledge/_kg_explorer.template.html', 'knowledge/gen_kg_titles.py'],
    [R + '2026-09-27-304-W5c-node-titles.md'],
    build="Explorer canvas prints code only (title kept in search, panel, INSPECT); gen_kg_titles.py titles the 49 bare labels (30 polarities, 13 WCAG guidelines, 6 artefacts)")
add('42', "THE ROUTE IS B: APOLLO AS AN A2UI CATALOGUE OVER MCP, WITH MCP APPS AS THE FALLBACK SHELL. Dave's answer, verbatim: \"{A}\" — route B, as the proposal and the page recommended. It reaches every major host today and Apollo owns only what is its own; the probe generated the catalogue from the metas in 1.6 seconds, ran the accessibility gate in memory in 61 milliseconds, and a rules-only chooser picked 18 of 20 parts. Nothing is built before `s305-D50`'s start.",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md', R + '2026-09-26-304-R5-mcp-probe.md'],
    needs_build=False, build="Nothing now — the PoC route; built from October (s305-D50)",
    brief='call 42 "b" = route B as recommended')
add('43', "THE PROOF OF CONCEPT IS SCOPED AS WRITTEN: THE LANDING DASHBOARD, ABOUT 15 PARTS, MOCK DATA, FOUR BEST-GUESS ROLES, SHOW AND PREPARE ONLY. Dave's answer, verbatim: \"{A}\". It proves the whole loop without touching anything real.",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md'],
    needs_build=False, build="Nothing now — PoC scope, October (s305-D50)")
add('44', "JEV SITS IN THE GENUI LAYER AS A RANKER BEHIND A SWITCH THAT IS OFF BY DEFAULT — FOR THE PROOF OF CONCEPT. Dave's answer, verbatim: \"{A}\" — the recommendation's own words. The layer never depends on Jev, which is what `s294-D10` protects (Jev a dev-time instrument, never a blocking dependency); this uses the option its rider kept open, for the PoC only. `s294-D10` is not amended.",
    ['knowledge/_jev.py', 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md', R + '2026-09-27-304-J-jev-edge-node-probe.md'],
    needs_build=False, build="Nothing now — in the PoC build: Jev ranker behind a switch, off by default")
add('45', "THE NAME IS LAUNCHPAD, NOT APOLLO LIVE: WRITTEN THE WAY APOLLO IS WRITTEN ON THE VISUALISATIONS, WITH \"APOLLO\" AS THE EYEBROW AND \"LAUNCHPAD\" BELOW IT. Dave's answer, verbatim: \"{A}\" ⚠ HE OVERRODE THE RECOMMENDATION: the page and the proposal (v2) recommended \"Apollo Live\". The proposal is not a ruling, so no store entry is superseded; this ruling crosses the proposal's name out. Under his Friday note (notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md) the proof of concept is a surprise, so the name does not go on shared material yet (store row W-305n6).",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md'],
    needs_build=False, build="Nothing now — the PoC's name and lock-up (Apollo eyebrow / Launchpad) used on PoC material from October; not on shared material (W-305n6)",
    brief='call 45 = the name is **Launchpad**')
add('46', "SCREENS THAT MOVE MONEY: DATA ONLY IN THE TARGET, NEVER RAW HTML, AND CONFIRMATION KEPT IN THE BANK'S OWN FLOW. Dave's answer, verbatim: \"{A}\". The bank's identity provider and its own flow stay the only places a payment is confirmed. The proof of concept moves no money at all.",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md'],
    needs_build=False, build="Nothing now — a constraint on the GenUI layer from October")
add('47', "THE PROOF OF CONCEPT STARTS IN OCTOBER, ONCE THE SCHEMA CALLS (14 TO 19, `s305-D15`–`s305-D20`) ARE IN THE TREE — the plan's order, not the proposal's \"now\". Dave's answer, verbatim, with his hedge kept: \"{A}\". Thirteen of the dashboard metas break the schema today, and a catalogue built from them would publish the drift. ⚠ The proposal is not a ruling; its \"now\" is crossed out here, no store entry superseded. Under his Friday note the PoC is a surprise (W-305n6).",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md', R + '2026-09-26-304-F-roadmap-plan.md'],
    needs_build=False, build="Nothing now — the PoC starts in October once s305-D15..D20 are in the tree",
    brief='call 47 "yes" = the PoC starts in October')
add('48', "THE DELIVERY SHAPE, IN ORDER: HOSTS FIRST (THE CATALOGUE AND THE RENDERER); MINTED CSS, WITH THE REFERENCE SNIPPETS AS THE TEST, SECOND; ADAPTERS AND EMITTERS PARKED. Dave's answer, verbatim: \"{A}\". It builds on what exists, and the renderer needs a per-theme stylesheet anyway, so the second step rides on the first.",
    ['notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html'],
    ['notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html'],
    needs_build=False, build="Nothing now — the PoC's delivery order from October; adapters/emitters parked")
add('49', "WHAT WAKES THE PARKED ADAPTERS AND EMITTERS IS ONE TRIPWIRE FOR BOTH: A TECHNOLOGY TEAM NAMING ITSELF AS THE OWNER OF A CONSUMER. Dave's answer, verbatim: \"{A}\". An adapter or an emitter with nobody to use it is an instrument without a consumer, the programme's own named failure. The page cites P-277-5 (npm distribution with Angular and React emitters) and ADR-0008; neither is edited here.",
    ['knowledge/_parked.json'],
    ['notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html'],
    build="Write the tripwire 'a technology team names itself owner of a consumer' onto the parked adapters/emitters entry (P-277-5) in the parked register")
add('50', "THE BUILD-READY TEST: THE PROOF-OF-CONCEPT DASHBOARD GOES TO A DEVELOPER WHO HAS NOT SEEN IT, AND WHAT THEY REDO IS COUNTED BY KIND. Dave's answer, verbatim, with his hedge kept: \"{A}\". It turns his north-star question into a number every later answer can be judged by. ⚠ His hedge is part of the record: the test may not be available in time; under `s305-D1` it is listed for re-review.",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-M-apollo-mcp-proposal.md'],
    needs_build=False, build="Nothing now — run once the PoC dashboard exists (a developer who has not seen it; count redo by kind)")
add('51', "THE MOTION CHECK ON COMPOSED PAGES RUNS PER PART, BEFORE GATES RUN ON ASSEMBLED SCREENS. Dave's answer, verbatim: \"{A}\". Today one reduced-motion block anywhere on a page silences the check for every part on it. It is in the Apollo-MCP group, which builds nothing before the schema calls land (`s305-D50`).",
    ['notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
    [R + '2026-09-26-304-R5-mcp-probe.md'],
    needs_build=False, build="Nothing now — per-part motion check lands with the PoC gates service (October)")
add('52', "JEV IS ADOPTED AS A HAND-RUN LINK CHECKER ON FOUR EDGE TYPES (obeys, providesRole, answersIntent, hasDataShape) WITH A TWO-BAND RULE: BELOW 0.2 COMES TO DAVE AS \"THIS LINK LOOKS WRONG\", ABOVE 0.8 IS SILENT, THE MIDDLE IS IGNORED. Dave's answer, verbatim: \"{A}\". A script under notes, never a gate, never in the build — inside `s294-D10`, which is not amended. The probe's figures: on fifty edges every edge under 0.2 was a fake and every edge over 0.8 was real (area under the curve 0.954); a full sweep of the four types is about 330 calls and two minutes.",
    ['knowledge/_jev.py'],
    [R + '2026-09-27-304-J-jev-edge-node-probe.md'],
    build="A hand-run sweep script under notes/ over the four edge types, printing the <0.2 list for Dave; exits clean without a key; never a gate")
add('53', "THE EXPLORER'S RULINGS, RULES AND SESSIONS READ AS CODE PLUS A TITLE TAKEN FROM THEIR OWN RECORD — RATIFIED. Dave's answer, verbatim: \"{A}\". Mechanical, no model: seat W5c titled all 1,203 (638 rulings, 473 rules, 92 sessions) with one generator and a build step that checks them; the code stays first, so search by code still works; two hand checks of 45 titles found none misstated; seat F5 fixed six session titles that said \"0 rulings\". How the canvas prints the pair, and the 49 still bare, is `s305-D44`.",
    ['knowledge/gen_kg_titles.py', 'knowledge/_node_titles.json', 'knowledge/_build_kg_explorer.py'],
    [R + '2026-09-27-304-W5c-node-titles.md', R + '2026-09-27-304-F5-wave-five-fixes.md',
     sha_ev('52049781', 's305-D56', 'the 1,203 derived titles (gen_kg_titles.py, _node_titles.json, explorer v1.29) and the session-count fix built in #304 wave five')],
    status=enacted('52049781', "the derived titles (knowledge/gen_kg_titles.py → knowledge/_node_titles.json, explorer builder v1.29, four KG build steps wired) and F5's session-count fix landed in #304 wave five; W5c's clone survey 0 green to red; CI 36306939769 four new KG steps green. Nothing to build here; the canvas change is `s305-D44`."),
    needs_build=False, build="Nothing — built at 52049781")

ORDER = [c['call'] for c in C]
ids = {}
n = 2
for c in C:
    ids[c['call']] = f's305-D{n}'; n += 1

entries = []
d1 = {
 "id": "s305-D1",
 "ruled": "A YES ON A SITTING CALL MEANS INSCRIBE AND BUILD; A RULING IS SET IN INK, NOT STONE, AND CAN BE CROSSED OUT LATER. When Dave answers a sitting call yes, or in the recommendation's words, the answer is both inscribed in this store and built by a lane in the same session — it does not wait for a second word to be built. A ruling may be crossed out in the future only by a LATER ruling that names it and supersedes it; nothing is erased, and the earlier entry stays in the store as written. A call he marks as one to review (his \"we might need to test a bit after\") is built as ruled AND listed for re-review at a later sitting. HIS WORDS, 13:59 BST, VERBATIM: \"most of these I want to do both but we might need to test a bit after, I guess we can just have a review on some of these decisions in the future, they are not set in stone they are set in ink and can be crossed out in the future\". CONTEXT: at 13:56 BST he asked \"whats the difference between 'do it' and 'inscribe'\"; the conductor explained that inscribing is the record of the decision in this store and doing it is the lane work that builds it, and recommended that a yes count as both; his 13:59 answer takes that recommendation. ⚠ The phrase 'on review' is the conductor's label for his 'we might need to test a bit after', not his word. The 2026-09-27 sitting's rulings `s305-D2`–`s305-D56` are the first inscribed under it.",
 "date": DATE, "by": "Dave",
 "says": "chat #305 2026-09-27 13:59 BST, answering the conductor's recommendation that a yes on a sitting call count as both inscribe and build, after his 13:56 question \"whats the difference between 'do it' and 'inscribe'\": \"most of these I want to do both but we might need to test a bit after, I guess we can just have a review on some of these decisions in the future, they are not set in stone they are set in ink and can be crossed out in the future\"",
 "governs": ["knowledge/_rulings.json", "knowledge/_inscribe_ruling.py"],
 "evidence": ["chat #305 2026-09-27 (live) - 13:56 BST his question and 13:59 BST his answer, quoted verbatim in `says`",
              f"{BRIEF}#they are not set in stone they are set in ink"],
 "status": "standing — in force from #305 2026-09-27; a process rule every later sitting applies, nothing to build",
}
entries.append(d1)
callmap = {'standing-rule': dict(ruling_id='s305-D1', status='standing', needs_build=False,
           what='A yes on a sitting call = inscribe AND build; later rulings supersede, nothing erased; review-marked calls re-listed')}
for c in C:
    call = c['call']
    a, cm, at = ans(call)
    ruled = c['ruled'].replace('{A}', a).replace('{C}', cm)
    num = call if call.startswith('41') and len(call) == 3 else str(int(call))
    ctitle = heads[call].split(' · ', 1)[1]
    says = (f"sitting page #304 (Tuesday 29 September v1), taken by Dave on Sunday 2026-09-27 and exported 14:53 BST; "
            f"call {num} ({ctitle}) saved {at[11:]} BST — decision, verbatim: \"{a}\"")
    if cm:
        says += f" · comment, verbatim: \"{cm}\""
    ev = [f"{EXPORT}#{anchor(call)}", PAGE] + c['extra']
    if c['brief']:
        ev.append(f"{BRIEF}#{c['brief']}")
    e = {"id": ids[call], "ruled": ruled, "date": DATE, "by": "Dave", "says": says,
         "governs": c['governs'], "evidence": ev, "status": c['status']}
    assert '{A}' not in ruled and '{C}' not in ruled
    if '{C}' in c['ruled']:
        assert cm, call
    entries.append(e)
    callmap[num] = dict(ruling_id=ids[call], status=('enacted' if c['status'].startswith('ENACTED') else 'ruled'),
                        needs_build=c['needs_build'], what=c['build'])
callmap['27'] = dict(ruling_id=None, status='not ruled', needs_build=True,
                     what="NOT RULED (comment only: \"" + machine['decision-27']['comment'] + "\") — a visuals page is owed (W-305n4, conductor's) before he can rule")
for e in entries:
    json.dump(e, open(f"{OUT}/{e['id']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def keyf(k):
    if k == 'standing-rule': return (0, 0, '')
    m = re.match(r'(\d+)([a-z]?)', k); return (1, int(m.group(1)), m.group(2))
cm2 = {k: callmap[k] for k in sorted(callmap, key=keyf)}
json.dump({"provenance": "305 · 2026-09-27 · lane A (inscription seat)",
           "source": EXPORT, "page": PAGE,
           "note": "ruling ids run s305-D1 (standing rule) then one per answered call in page order 1-53 with 41b/41c/41e after 41; call 27 is NOT ruled. status 'enacted' = ratifies what is already in the tree, the sha is in the ruling's evidence.",
           "calls": cm2}, open('notes/_lanes/305/A/CALL-MAP.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(entries), 'entries;', entries[0]['id'], '..', entries[-1]['id'])
