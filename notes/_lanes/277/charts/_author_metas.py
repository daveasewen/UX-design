#!/usr/bin/env python3
"""_author_metas.py — lane CO (#277, enacting s276-D5). PROPOSE the authored
`edges.obeys` block for chart-line, chart-pie and chart-bar. READ-ONLY on
knowledge/.

AUTHORED, not inferred. Every rule id below came from a FILENAME JOIN on
knowledge/guidelines/_rules-index.json (`file == data-visualisation-<x>-charts.md`),
never from a regex over rule prose — that is the route s274-D12 refused after
va25-013 matched 'Avatar', and s276-D5 refuses again by name. Every `$why` was
written by reading the rule text and the component meta together, one line each,
reviewed by eye.

REVIEWED BY EYE is part of the ruling, so three rules are DECLARED DROPS: a
spec file can carry a rule about something else, and a silent drop is the
s214-D6 failure. The drops and their reasons live in DROPPED below and are
printed by --build and --table.

There is NO schema diff in this lane: `edges.obeys` ({ref, $why}, $why
REQUIRED) already exists in meta.schema.json, landed by s276-D3 at 577c82d.

s276-D5 scopes this lane to the FILENAME JOIN on the three chart spec files.
`ux:` grade-A laws (lane TO's second half) are therefore NOT authored here —
that is not an oversight, it is the ruling's scope, and it is declared in
REPORT.md §7.

Output: notes/_lanes/277/charts/proposed-metas/<stem>.meta.json — each one a
BYTE-FOR-BYTE copy of the live meta with a single textual span inserted inside
its existing "edges": { … } object. The live metas are never opened for writing
and no existing JSON is ever re-serialised (#179).

  --build     write the three proposed metas (default)
  --table     print the per-rule bind/no-bind table and the Q2 family matrix
  --selftest  bites, no writes
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
K = os.path.join(REPO, "knowledge")
COMPONENTS = os.path.join(K, "components")
OUT = os.path.join(HERE, "proposed-metas")
INDEX = os.path.join(K, "guidelines", "_rules-index.json")

# stem -> guideline file whose rules are joined by FILENAME (s276-D5)
SPEC_FILE = {
    "chart-line": "data-visualisation-line-charts.md",
    "chart-pie": "data-visualisation-pie-charts.md",
    "chart-bar": "data-visualisation-bar-charts.md",
}

FAMILY_FILE = "data-visualisation.md"

# ---------------------------------------------------------------------------
# THE AUTHORED TABLE. stem -> [(node-id, one-line why it binds)]
# ---------------------------------------------------------------------------
RULES = {
    "chart-line": [
        ("rule:dv-line-001", "The zero y-axis is OPTIONAL for a line and MANDATORY for a bar, and this meta is the line side of that deliberate asymmetry — it carries no data-domain-min antiPattern, where chart-bar carries one."),
        ("rule:dv-line-002", "Shape per data set, not colour alone: the meta's `series` prop already names this rule and fixes the three marker geometries (circle r4.2 · square 8.4 · diamond ±4.9), so the rule IS the prop."),
        ("rule:dv-line-003", "Axis titles, per-category X labels, incremental Y labels and gridlines are the parts DV-D07 mints tokens for (data/axis, data/grid) — the rule says which parts must exist, the meta says what colour they are."),
        ("rule:dv-line-004", "The reference point plus a tooltip repeating BOTH axis values is the dvTip popover in this meta's `motion.hover`, and the both-axes clause is why the popover cannot be a bare value."),
        ("rule:dv-line-005", "Comparable intervals and a gridline density that can be dropped when it confuses is a judgement this meta hands to the author; it is TASTE, and it is the reason `responsive` pins the viewBox 1:1 rather than rescaling intervals."),
        ("rule:dv-line-006", "Dual y-axes only for different units is the rule this meta OBEYS BY YIELDING: its `when` hands the different-units case to chart-combo, so on this component the rule reads as a prohibition, and that is the binding worth recording."),
        ("rule:dv-line-007", "Filter/focus on multi-set charts is this meta's `legendFilter` prop — the rule is why that prop defaults to true rather than being an option."),
        ("rule:dv-line-008", "End-line markers plus a key when intervals are tight, and explicit labelling of projected states, govern the multi-series variant this meta declares; nothing else in the meta supplies that labelling contract."),
        ("rule:dv-line-011", "Straight segments only, never gratuitous curves — the meta's first antiPattern cites this rule by id, so the edge makes an existing prose citation a graph edge."),
    ],
    "chart-pie": [
        ("rule:dv-pie-001", "Start at 12 o'clock, largest to smallest unless the categories have an inherent order — the angle contract for the segments this meta bakes as data-a1/-a2 at generation time."),
        ("rule:dv-pie-002", "Label plus exact proportional value per slice, with indicator lines when segments crowd, is precisely this meta's `labelling` = spider default: the leader line IS the indicator line the rule asks for."),
        ("rule:dv-pie-004", "Direct labelling adjacent to segments is the meta's second declared variant ('direct labels'), so the rule names one of the two things this component can be."),
        ("rule:dv-pie-005", "Labels inside a slice only where they stay readable is the TASTE half of the labelling choice, and it is why this meta's antiPatterns ban white type on the fills and put labels outside the ring."),
        ("rule:dv-pie-006", "Slice-ordering direction has to be checked against assistive technology, and this meta makes every segment a focus stop with aria-label == data-tip == table — the order those stops are read in is what the rule is about."),
        ("rule:dv-pie-007", "Never enlarge or pull out a slice to emphasise it: the meta has no exploded variant and its motion block moves segments only by a radial sweep that ends flush, so the rule is the reason no such variant exists."),
        ("rule:dv-pie-008", "Proportion of a set total ONLY, never group-to-group comparison — this is the `when` gate of the meta stated from the guidance side, and it is what sends comparison to chart-bar."),
        ("rule:dv-pie-009", "Maximum 6 slices, pie and doughnut alike: the meta's `slices` prop cites this rule by id and carries the 'combine the smallest into Other' remedy, so the edge records a binding the meta already states in prose."),
        ("rule:dv-pie-010", "Values must add up to the declared total: this meta prints NO centre figure, so data-total is the only place the total lives and the arithmetic is unverifiable by eye — the rule binds harder here than on the donut, not less."),
        ("rule:dv-pie-011", "Always indicate rounding: the value ⇄ percent toggle in this meta's `valueMode` prop is exactly where rounded percentages appear, and the rule is the contract that toggle has to honour."),
    ],
    "chart-bar": [
        ("rule:dv-bar-001", "A title that reflects the main insight is this meta's optional `title` prop, and the rule is why the slot exists at all rather than a bare chart frame."),
        ("rule:dv-bar-002", "Axis titles on both axes unless the labels are obvious — the get-out clause is the reason this is a judgement the author makes per instance, and the meta's axis tokens have to carry either way."),
        ("rule:dv-bar-003", "Categorical X with per-category labels, incremental Y values, gridlines for scale: the structural parts DV-D07's data/axis and data/grid roles exist to colour."),
        ("rule:dv-bar-004", "A key is required whenever labelling is alphanumeric, which is exactly this meta's on-chart letter keys (.dv-barkey) and its lettered legend swatches in the grouped and stacked variants."),
        ("rule:dv-bar-005", "Filtering and configuration tools sit ABOVE the chart — the placement contract for this meta's sort segmented control and its table-view dropdown."),
        ("rule:dv-bar-006", "Group separators, group category labels and a group key for alphanumeric group labels are the anatomy of this meta's 'grouped column' variant; no other rule supplies it."),
        ("rule:dv-bar-007", "Negative values on a horizontal bar are banned — the meta's antiPatterns cite this rule by id, and its `orientation` prop's 'bar' value carries the positives-only note."),
        ("rule:dv-bar-008", "Past versus projected must always be labelled. This meta declares no projected variant today, and the rule is what any future one would have to satisfy — a binding constraint, not a described feature."),
        ("rule:dv-bar-009", "The zero baseline is mandatory for every bar chart: the meta's antiPatterns cite this rule by id and name data-domain-min=\"0\" as the mechanism."),
        ("rule:dv-bar-010", "Well spaced, evenly distributed, and not too many categories — the arrangement rule the meta's span.cols 4–12 and its DV-D02 compress-never-scale responsive rule between them have to satisfy."),
    ],
}

# ---------------------------------------------------------------------------
# DECLARED DROPS — reviewed by eye, s276-D5. A dropped rule that is declared is
# a finding; a silent drop is the s214-D6 failure.
# ---------------------------------------------------------------------------
DROPPED = {
    "chart-line": [
        ("dv-line-009", "Sits under the file's '## Spark charts' heading and governs the SPARK's aspect ratio against surrounding content. chart-sparkline is a separate meta in knowledge/components/; this rule is its, not chart-line's."),
        ("dv-line-010", "Also under '## Spark charts' — 'in tables, group all data related to the spark sequentially'. It is a table-composition rule about sparklines. chart-line is never placed inside a table row; chart-sparkline is."),
    ],
    "chart-pie": [
        ("dv-pie-003", "'Doughnut centre: total value + descriptor together' is donut-only. chart-pie's purpose says the DV-D13 centre-total wiring was REMOVED ('donut-only, per brief') and its antiPatterns ban porting it across. A pie with no centre has no centre contract to obey."),
    ],
    "chart-bar": [],
}

CONTRACT = ("AUTHORED, not inferred (s276-D5, lane CO #277). `rule:` refs are joined by FILENAME from "
            "knowledge/guidelines/_rules-index.json — never by a regex over rule prose (s274-D12 / "
            "s276-D5: the name-match tier produced 'Avatar' from va25-013 and is NOT widened). Each "
            "$why is one line, written by reading the rule and this meta together, reviewed by eye. "
            "Rules of the spec file that do NOT bind are DECLARED DROPS, listed in "
            "notes/_lanes/277/charts/REPORT.md §3, never silently omitted. The 19 family-level rules "
            "in data-visualisation.md are NOT attached here: that is Q2, open for Dave. PROPOSED — "
            "not ratified.")


# ---------------------------------------------------------------------------
def index_rules():
    return json.load(open(INDEX, encoding="utf-8"))["rules"]


def by_file():
    out = {}
    for r in index_rules():
        out.setdefault(r["file"], set()).add(r["id"])
    return out


def obeys_block(stem, indent):
    """The literal JSON text to splice in, already indented for the target file."""
    entries = [{"ref": ref, "$why": why} for ref, why in RULES[stem]]
    txt = json.dumps(entries, indent=2, ensure_ascii=False)
    pad = " " * indent
    body = ("\n" + pad).join(txt.split("\n"))
    note = json.dumps(CONTRACT, ensure_ascii=False)
    return '%s"$obeys-contract": %s,\n%s"obeys": %s,' % (pad, note, pad, body)


def splice(stem, parts=False):
    src = os.path.join(COMPONENTS, stem + ".meta.json")
    text = open(src, encoding="utf-8").read()
    m = re.search(r'^(\s*)"edges"\s*:\s*\{[ \t]*\n', text, re.M)
    if not m:
        raise SystemExit("no edges object in " + src)
    indent = len(m.group(1)) + 2
    at = m.end()
    ins = obeys_block(stem, indent) + "\n"
    out = text[:at] + ins + text[at:]
    return (text, at, ins, out) if parts else out


def build():
    os.makedirs(OUT, exist_ok=True)
    written = []
    for stem in SPEC_FILE:
        out = os.path.join(OUT, stem + ".meta.json")
        new = splice(stem)
        json.loads(new)  # must still parse
        open(out, "w", encoding="utf-8").write(new)
        written.append(out)
    return written


# ---------------------------------------------------------------------------
# Q2 — the 19 family-level rules of data-visualisation.md, per component.
# MEASURED FOR THE PAGE, NOT ATTACHED. Option (b) of Q2 is this subset; the
# lane does not decide Q2 (s276-D5 gives Dave the word).
# Each entry: rule id -> {stem: (binds?, one-line reason)}
# ---------------------------------------------------------------------------
FAMILY = {
    "dv-001": {"chart-line": (True, "A truncated y-range on a trend line is the classic distortion; dv-line-001 relaxes the zero baseline and this rule is the fence that relaxation sits inside."),
               "chart-bar": (True, "Bars are read by length, so any scale alteration misstates the comparison directly."),
               "chart-pie": (False, "A pie has no scale range to display or truncate — proportion is the whole of its geometry.")},
    "dv-002": {"chart-line": (True, "The TASTE companion to dv-001 on the same continuous axis."),
               "chart-bar": (True, "The TASTE companion to dv-001 on this component's value axis, same reading."),
               "chart-pie": (False, "Same as dv-001: there is no scale on a pie to make reasonable or unreasonable.")},
    "dv-003": {"chart-line": (True, "Omitting points from a series changes the trend it draws."),
               "chart-bar": (True, "Omitting categories changes which is highest."),
               "chart-pie": (True, "Omitting a slice breaks the sum, which dv-pie-010 already makes BLOCKING here.")},
    "dv-004": {"chart-line": (False, "Lines are strokes, not adjacent colour blocks; the meta cites no 2px separation and has no touching fills to separate."),
               "chart-bar": (True, "Adjacent bars in a grouped or stacked column ARE touching colour blocks."),
               "chart-pie": (True, "The meta's `tokens.separation` cites dv-004 by id — 2px page stroke on every segment.")},
    "dv-005": {"chart-line": (True, "The meta cites dv-005 by id: a real <table class=\"dv-table\"> in the figure."),
               "chart-bar": (True, "Cited by id in the meta's `data` prop and its fallback prose."),
               "chart-pie": (True, "Cited by id in the meta's behaviour fallback.")},
    "dv-006": {"chart-line": (True, "Cited by id in the meta's `title` prop — the title must reflect the main insight."),
               "chart-bar": (True, "Title, key, alphanumeric labels and tooltips are all parts this meta declares."),
               "chart-pie": (True, "The 'direct labelling adjacent to segments in circular charts' clause is this component by name.")},
    "dv-007": {"chart-line": (True, "The DV-D02 baked-fraction relayout is this meta's answer to the responsive clause."),
               "chart-bar": (True, "Same DV-D02 relayout, restricted to horizontal positions; the viewBox stays pinned 1:1."),
               "chart-pie": (True, "The meta takes the DV-D02 EXCLUSION and scrolls instead — a declared answer to this rule, not an escape from it.")},
    "dv-008": {"chart-line": (True, "JS-off fallback is fixed 580×260 plus horizontal scroll — exactly the last resort this rule fences."),
               "chart-bar": (True, "Same JS-off fallback — fixed geometry plus horizontal scroll as the last resort."),
               "chart-pie": (True, "`.dv-stage` scrolls when the container is narrower than the fixed ring.")},
    "dv-009": {"chart-line": (True, "The markers ARE filled shapes — the meta's `markers` prop sets a series-colour fill plus a page stroke, so the flat-fill rule reaches this component through them, not through the strokes."),
               "chart-bar": (True, "The meta's antiPatterns cite dv-009 by id — flat fills only."),
               "chart-pie": (True, "The meta's antiPatterns ban gradient/3D ring fills.")},
    "dv-010": {"chart-line": (True, "The dvTip popover overlays the plot and must not obscure the data it reports."),
               "chart-bar": (True, "Value tip plus table popover, same constraint."),
               "chart-pie": (True, "Segment popover plus table panel, same constraint.")},
    "dv-011": {"chart-line": (True, "Cited by id in the meta's `series` prop — colour is never the only channel."),
               "chart-bar": (True, "Shape plus letter plus name on multi-series; the status ramp is direct-labelled."),
               "chart-pie": (True, "Letter keys and names carry identity; the meta's a11y block states 1.4.1 explicitly.")},
    "dv-012": {"chart-line": (True, "The meta's surface token is background/default — colour is on the data, never behind it."),
               "chart-bar": (True, "Same background/default surface token; the status ramp uses colour to focus, not to fill the ground."),
               "chart-pie": (True, "Same background/default surface token — colour sits on the segments, not behind them.")},
    "dv-013": {"chart-line": (False, "Combination charts are chart-combo's job; this meta's `when` explicitly yields the two-measures case to it."),
               "chart-bar": (True, "Positive/negative is the rule's own example and this meta's `orientation` prop handles exactly that case."),
               "chart-pie": (False, "A pie holds one variable's parts; there are no data sets to differentiate between.")},
    "dv-014": {"chart-line": (True, "Cited by id in the meta's mustNotNeighbour."),
               "chart-bar": (True, "Cited by id in the meta's mustNotNeighbour."),
               "chart-pie": (True, "Cited by id in the meta's mustNotNeighbour.")},
    "dv-015": {"chart-line": (True, "The rule NAMES line and spark as the change-over-time answers; this meta is the line half."),
               "chart-bar": (False, "The rule's list is line, spark, bullet, candlestick — a bar is not one of the four it names for change over time."),
               "chart-pie": (False, "The rule is about choosing a change-over-time chart; a pie answers composition, so the choice never reaches it.")},
    "dv-016": {"chart-line": (True, "Cited by id in the meta's tokens and nonText; BLOCKING and measured clean."),
               "chart-bar": (True, "Cited by id in the meta's tokens; BLOCKING and measured green by the DataViz gate."),
               "chart-pie": (True, "Partially: the meta's $survey records that pie carries NO axis or gridline CSS, so only the title/label arm of the rule reaches it — which is why (b) needs per-component authoring, not a batch.")},
    "dv-017": {"chart-line": (True, "Cited by id in the meta's antiPatterns — raw hex strokes banned."),
               "chart-bar": (True, "Cited by id in the meta's antiPatterns — raw hex series fills banned, var() tokens only."),
               "chart-pie": (True, "The meta's $survey states no new tokens were minted; palette only.")},
    "dv-018": {"chart-line": (True, "The rule names 'different colours per line' explicitly."),
               "chart-bar": (True, "The rule names 'different colour per data set variable (bar)' explicitly."),
               "chart-pie": (True, "The rule names 'different colours within a single-variable circular chart' explicitly.")},
    "dv-019": {"chart-line": (False, "INDEX DEFECT, read from source: _rules-index.json gives dv-019 dv-017's sentence, but data-visualisation.md:70 shows dv-019 is the Apollo-added vibrating-boundaries rule. It needs ADJACENT SATURATED FILLS; a line has none."),
               "chart-bar": (True, "Adjacent bars in a grouped or stacked column are the exact adjacent-saturated-pair case, and dv-004's 2px gap — which this meta enacts — is named in the rule as the structural defence."),
               "chart-pie": (True, "Adjacent segments share a boundary all the way round the ring; the meta's 2px page stroke on every segment is exactly the defence this rule names.")},
}


def family_counts():
    return {s: sum(1 for r in FAMILY if FAMILY[r][s][0]) for s in SPEC_FILE}


def table():
    idx = {r["id"]: r for r in index_rules()}
    bf = by_file()
    print("\n=== PART A — per-rule bind / no-bind (filename join) ===")
    for stem, f in SPEC_FILE.items():
        bound = [r.split(":", 1)[1] for r, _ in RULES[stem]]
        drops = {d: w for d, w in DROPPED[stem]}
        print("\n%s  <-  %s   (%d in file · %d bind · %d dropped)"
              % (stem, f, len(bf[f]), len(bound), len(drops)))
        for rid in sorted(bf[f]):
            mark = "BIND" if rid in bound else "DROP"
            print("  %-4s %-14s %-9s %s" % (mark, rid, idx[rid]["destiny"],
                                            (drops.get(rid, "") or idx[rid]["rule"])[:96]))
    print("\n=== Q2 — the %d family rules of %s, MEASURED not attached ==="
          % (len(bf[FAMILY_FILE]), FAMILY_FILE))
    print("  %-10s %s" % ("rule", "  ".join("%-11s" % s for s in SPEC_FILE)))
    for rid in sorted(FAMILY):
        print("  %-10s %s" % (rid, "  ".join(
            "%-11s" % ("binds" if FAMILY[rid][s][0] else "—") for s in SPEC_FILE)))
    fc = family_counts()
    print("  %-10s %s" % ("(b) count", "  ".join("%-11d" % fc[s] for s in SPEC_FILE)))
    print("  (a) would attach %d to each = %d edges; (b) = %d edges"
          % (len(bf[FAMILY_FILE]), len(bf[FAMILY_FILE]) * 3, sum(fc.values())))


# ------------------------------------------------------------------ selftest
def selftest():
    fails = []

    def bite(n, claim, ok):
        print("  %s bite %2d — %s" % ("OK  " if ok else "FAIL", n, claim))
        if not ok:
            fails.append(n)

    idx = index_rules()
    by_id = {r["id"]: r for r in idx}
    bf = by_file()

    print("selftest — _author_metas.py (lane CO, #277)")
    bite(1, "three components authored, each with a live meta on disk",
         len(SPEC_FILE) == 3 and all(os.path.exists(os.path.join(COMPONENTS, s + ".meta.json"))
                                     for s in SPEC_FILE))
    allrefs = [r for s in RULES for r, _ in RULES[s]]
    bite(2, "every rule: ref resolves to a real id in _rules-index.json (470 rules)",
         len(idx) == 470 and all(r.split(":", 1)[1] in by_id for r in allrefs))
    bite(3, "FILENAME JOIN holds with NO cross-file binding: every ref's file is its own spec file",
         all(by_id[r.split(":", 1)[1]]["file"] == SPEC_FILE[s]
             for s in RULES for r, _ in RULES[s]))
    bite(4, "the measured per-file counts are 11 line / 11 pie / 10 bar / 19 family",
         (len(bf["data-visualisation-line-charts.md"]), len(bf["data-visualisation-pie-charts.md"]),
          len(bf["data-visualisation-bar-charts.md"]), len(bf[FAMILY_FILE])) == (11, 11, 10, 19))
    bite(5, "BIND + DROP partition each spec file EXACTLY — nothing invented, nothing silently lost",
         all({r.split(":", 1)[1] for r, _ in RULES[s]} | {d for d, _ in DROPPED[s]} == bf[SPEC_FILE[s]]
             and not ({r.split(":", 1)[1] for r, _ in RULES[s]} & {d for d, _ in DROPPED[s]})
             for s in SPEC_FILE))
    bite(6, "every drop carries a declared reason of at least 60 characters (s214-D6)",
         all(len(w) >= 60 for s in DROPPED for _, w in DROPPED[s]))
    bite(7, "the two spark rules are dropped from chart-line and the donut-centre rule from chart-pie",
         {d for d, _ in DROPPED["chart-line"]} == {"dv-line-009", "dv-line-010"}
         and {d for d, _ in DROPPED["chart-pie"]} == {"dv-pie-003"}
         and DROPPED["chart-bar"] == [])
    bite(8, "NO family rule leaks into a proposed meta — Q2 is Dave's, so 0 dv-0NN refs are attached",
         not any(by_id[r.split(":", 1)[1]]["file"] == FAMILY_FILE for r in allrefs))
    bite(9, "no ux: ref is authored — s276-D5 scopes this lane to the filename join",
         all(r.startswith("rule:") for r in allrefs))
    bite(10, "every id matches the corpus's ^[a-z][a-z0-9-]*-\\d{3}$ shape",
          all(re.match(r"^[a-z][a-z0-9-]*-\d{3}$", r.split(":", 1)[1]) for r in allrefs))
    bite(11, "every entry carries a non-empty authored $why of at least 40 chars (the schema minimum)",
          all(len(w) >= 40 for s in RULES for _, w in RULES[s]))
    bite(12, "no $why is reused verbatim across two entries — each was written for its own rule",
          len({w for s in RULES for _, w in RULES[s]}) == sum(len(RULES[s]) for s in RULES))
    bite(13, "no $why is a restatement: none is a prefix of the rule's own index text",
          not any(by_id[r.split(":", 1)[1]]["rule"].startswith(w[:40])
                  for s in RULES for r, w in RULES[s]))
    bite(14, "the spliced meta still parses as JSON and gains exactly the two new keys",
          all(set(json.loads(splice(s))["edges"]) -
              set(json.load(open(os.path.join(COMPONENTS, s + ".meta.json")))["edges"])
              == {"obeys", "$obeys-contract"} for s in SPEC_FILE))
    bite(15, "the splice is EXACTLY one insertion: cut the span back out and the live file returns byte for byte",
          all(_cut_back(*splice(s, parts=True)) for s in SPEC_FILE))
    bite(16, "not one value outside edges.obeys changes — every other key is identical",
          all(_same_except_edges(s) for s in SPEC_FILE))
    bite(17, "the live schema ALREADY admits rule: in obeysEdge — there is no schema diff in this lane",
          bool(re.match(json.load(open(os.path.join(COMPONENTS, "meta.schema.json"),
                                       encoding="utf-8"))["definitions"]["obeysEdge"]
                        ["properties"]["ref"]["pattern"], "rule:dv-bar-009"))
          and "$why" in json.load(open(os.path.join(COMPONENTS, "meta.schema.json"),
                                       encoding="utf-8"))["definitions"]["obeysEdge"]["required"])
    bite(18, "the Q2 family matrix covers all 19 family rules × 3 components with a reason each",
          set(FAMILY) == bf[FAMILY_FILE] and
          all(set(FAMILY[r]) == set(SPEC_FILE) and all(len(FAMILY[r][s][1]) >= 40 for s in SPEC_FILE)
              for r in FAMILY))
    bite(19, "OUT is inside this lane; knowledge/components/ is never a write target",
          OUT.startswith(os.path.join(REPO, "notes", "_lanes", "277", "charts"))
          and COMPONENTS not in OUT)
    # Bites 15/16 are round-trip invariants: they hold against whatever text
    # splice() started from, so a RE-DUMP of the meta satisfies both. That is
    # the #179 defect exactly, and _mutate.py's M9 SURVIVED until this bite
    # existed. It re-reads the bytes independently and demands the proposal be
    # the live file's bytes on either side of one inserted span.
    bite(20, "the proposal is the LIVE FILE'S BYTES either side of the span — a re-dump is caught (#179, M9)",
          all(_no_redump(s) for s in SPEC_FILE))
    print("selftest: %d/%d bites green" % (20 - len(fails), 20))
    return 0 if not fails else 1


def _cut_back(text, at, ins, out):
    return (out == text[:at] + ins + text[at:]
            and out[:at] + out[at + len(ins):] == text
            and len(out) == len(text) + len(ins))


def _no_redump(stem):
    """Read the live file's bytes here, independently of splice(), and demand
    the proposal be exactly those bytes with one span inserted. A builder that
    re-serialises the JSON still satisfies _cut_back (its own round trip holds)
    but fails this."""
    with open(os.path.join(COMPONENTS, stem + ".meta.json"), "rb") as f:
        live = f.read()
    text, at, ins, _ = splice(stem, parts=True)
    out = splice(stem).encode("utf-8")
    # `at` indexes CHARACTERS; the comparison is over BYTES, so convert.
    b_at = len(text[:at].encode("utf-8"))
    n = len(ins.encode("utf-8"))
    return (len(out) == len(live) + n
            and out[:b_at] == live[:b_at]
            and out[b_at + n:] == live[b_at:])


def _same_except_edges(stem):
    live = json.load(open(os.path.join(COMPONENTS, stem + ".meta.json"), encoding="utf-8"))
    new = json.loads(splice(stem))
    if {k: v for k, v in live.items() if k != "edges"} != {k: v for k, v in new.items() if k != "edges"}:
        return False
    le, ne = dict(live["edges"]), dict(new["edges"])
    ne.pop("obeys", None)
    ne.pop("$obeys-contract", None)
    return le == ne


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    if "--table" in sys.argv[1:]:
        table()
        return
    w = build()
    print("wrote %d proposed metas to %s" % (len(w), OUT))
    for p in w:
        d = json.load(open(p, encoding="utf-8"))
        stem = os.path.basename(p)[: -len(".meta.json")]
        print("  %-22s obeys %2d   dropped %d %s" % (
            os.path.basename(p), len(d["edges"]["obeys"]), len(DROPPED[stem]),
            "(" + ", ".join(d for d, _ in DROPPED[stem]) + ")" if DROPPED[stem] else ""))
    print("  TOTAL obeys edges proposed: %d" % sum(len(RULES[s]) for s in RULES))


if __name__ == "__main__":
    main()
