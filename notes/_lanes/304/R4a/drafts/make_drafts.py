#!/usr/bin/env python3
"""R4a — writes the DRAFT when-rules and observation rules for Dave's Tuesday sitting.
DRAFTS ONLY: nothing here touches knowledge/. Every `current` value is READ from the live meta at run
time (never typed); every `proposed` value is the exact string/object the named field takes on his yes.
Run (seat): PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/304/R4a/drafts/make_drafts.py
Writes: when-rules.proposed.json · observations.proposed.json · rulings.proposed.json (this folder).
"""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
K = os.path.join(ROOT, "knowledge")
def meta(slug):
    return json.load(open(os.path.join(K, "components", slug + ".meta.json")))
def gate_prose(w):
    g, _, p = (w or "").partition("—")
    return g.strip(), p.strip()

THU = ("notes/_lanes/303/WRAP-BRIEF.md", "Thu 2026-09-24 15:46 BST")
DAVE_A = ("add is that bento sections must have the lightest grey background so there is definition between "
          "the white tiles and the background. but this doesn't mean the full page nor does it mean and top "
          "title section only the pages section on which the bento sits.")
DAVE_B = ("and can we make sure it retrieves the components well, sometimes it made buttons  and table headings "
          "way smaller than they should.")
DAVE_C = ("and question the choice of using a model when and a split button or drop-down would be better. these "
          "are observations that we will role into the graph at some point. If we can not make this to explicit, "
          "I don't want it to be a set of instructions as that should be part of the graph and I may share the "
          "prompt with the audience.")

# ---------------------------------------------------------------- registry additions (when-fields.json `fields`)
REGISTRY = {
    "needs": {"definition": "what the person must do to the records as a set (`sort`, `filter`, `select`, "
                            "`edit`; `none` = they only read them)",
              "kind": "enum", "example": "needs in (sort, filter, select, edit)"},
    "layout.grammar": {"definition": "the layout grammar the page is built on (`bento` = canon's bento-of-bentos, "
                                     "s217-D2; `grid` = the layout-utilities grid)",
                       "kind": "enum", "example": "layout.grammar = bento"},
    "interrupts": {"definition": "whether the moment must stop the person until they answer (`required` = a "
                                 "confirmation or a task that cannot share the screen; `none` = the choice can be "
                                 "made in place)",
                   "kind": "enum", "example": "interrupts = required"},
    "actions": {"definition": "how many related actions hang off one trigger",
                "kind": "count", "example": "actions >= 2"},
    "options": {"definition": "how many choices one selection offers",
                "kind": "count", "example": "options >= 5"},
}

# ---------------------------------------------------------------- the dashboard's parts (R5's derived 18 + the frame)
DASH = ["app-shell-top-nav", "breadcrumbs", "button", "chart-bar", "chart-line", "data-grid", "filter-toolbar-bar",
        "footer", "headers", "kpi-tile", "layout-utilities", "legend", "list-items", "navigations", "stat-card",
        "status-indicator", "summary", "view-options", "template-dashboard-bento"]

def amend_gate(slug, add):
    g, p = gate_prose(meta(slug).get("when"))
    return "%s AND %s — %s" % (g, add, p)

PROPOSED = {
    "chart-line": dict(change="AMEND", proposed=lambda: amend_gate("chart-line", "units = same AND shape = time-series × 1–5-series"),
        why="The line chart's own sentence already says it gives way when units differ (to chart-combo) and when OHLC "
            "is the claim (to Chart-candlestick); the two clauses make that sentence readable by the chooser. R5 "
            "what-if: closes W10 and W1c, no other pick changes.",
        page="_DECIDE-304-when-rules question 1"),
    "data-grid": dict(change="NEW", proposed=lambda: (
        "records >= 2 AND needs in (sort, filter, select, edit) — the record-list for rows the person works on as a "
        "set: it beats list-items (the role's default, s274-D6) whenever sorting, filtering, selecting or editing is "
        "required, and yields to list-items when needs = none."),
        why="R5 W18: the grid has no rule, so it can never be picked on evidence; list-items' own prose already "
            "hands this case to the grid.", page="_DECIDE-304-when-rules question 3",
        registry=["needs"]),
    "list-items": dict(change="AMEND", proposed=lambda: amend_gate("list-items", "needs = none"),
        why="Makes list-items' existing yield to the data grid machine-readable (the other half of question 3). An "
            "unknown `needs` stays unknown, so a brief that says nothing about sorting still gets the list.",
        page="_DECIDE-304-when-rules question 3 (drafted 'the same way, for you to see at the wrap')",
        registry=["needs"],
        also={"shape": {"proposed": "records × fields", "note": "shapes.json is a CLOSED store (s254-D2 item 1): "
              "`records × fields` is a proposed addition to it, for the same wrap. Without it list-items and "
              "data-grid stay the two record-list parts with no data shape (R5 L3 blocker)."}}),
    "filter-toolbar-bar": dict(change="NEW", proposed=lambda: (
        "records >= 2 AND needs in (filter, sort) — one row of controls that drives the record-list and the "
        "panels beside it (edges.drivesConsumer, s268-D5; the wiring is the author's, s258-D1); it is placed "
        "only above the thing it drives, never on its own."),
        why="R5: no when-rule, so the chooser cannot place it; its drivesConsumer edge already states its "
            "consumer.", page="_DECIDE-304-when-rules question 3 ('the filter bar … drafted the same way')",
        registry=["needs"]),
    "footer": dict(change="NEW", proposed=lambda: (
        "platform = app — every app page shell ends in the app footer, the body-level sibling after the main "
        "region and never inside the bento wall (the meta's own $finding-site-footer, #258: \"the page shells "
        "should include the footer\")."),
        why="R5: no when-rule. The field and the fact are already in the record; the rule states them where the "
            "chooser reads.", page="_DECIDE-304-when-rules question 3 ('the footer … drafted the same way')"),
    "template-dashboard-bento": dict(change="ENACT-RULED", proposed=lambda: (
        "the question is 'how are things, and what needs me?' AND layout.grammar = bento — the dashboard frame "
        "when the designer's answer to 'dashboard bento — is that right?' is yes (s230-D1 beat 2); its tiles are "
        "themselves bentos (s217-D2, s217-D3). A composer borrows its grammar ($bentoGrammar) and chooses every "
        "module from the graph; it yields to template-dashboard when layout.grammar = grid."),
        why="s272-D85 RATIFIED this gate (status: ruled) and it never reached the meta. The first clause stays "
            "prose inside the gate (no registry field says 'the question'); `layout.grammar` is a registry "
            "addition. The prose half is where the graph, not the skill, says 'compose, never trace'.",
        page="s272-D85 (already Dave's); the registry addition and the prose half are this seat's draft",
        registry=["layout.grammar"]),
    # observation (c) — the lightest pattern
    "modals": dict(change="NEW", proposed=lambda: (
        "interrupts = required — the person must stop: confirm a consequential action, or finish a task that "
        "cannot share the screen; yields to split-button when interrupts = none AND actions >= 2 (one main action "
        "with a few related ones beside it), and to dropdown when interrupts = none AND options >= 5 (one choice "
        "from a list, made in place, s270-D1)."),
        why="Dave's third Thursday observation as a rule the graph can read (observation C).",
        page="_DECIDE-304-when-rules question 6", registry=["interrupts", "actions", "options"], obs="C"),
    "split-button": dict(change="NEW", proposed=lambda: (
        "actions >= 2 AND interrupts = none — one main action plus a menu of related ones, offered in place "
        "(button's own `when` already hands this case here); beats modals whenever the related actions can be "
        "offered without stopping the person."),
        why="Observation C: the part a modal gives way to.", page="_DECIDE-304-when-rules question 6",
        registry=["actions", "interrupts"], obs="C"),
    "dropdown": dict(change="NEW", proposed=lambda: (
        "options >= 5 AND interrupts = none — one choice from a list, made in place (s270-D1: \"we use dropdowns "
        "for 5 and above\"); beats modals whenever the choice does not need to stop the person."),
        why="Observation C, with Dave's own 5-and-above cut-off (s270-D1) as the count.",
        page="_DECIDE-304-when-rules question 6", registry=["options", "interrupts"], obs="C"),
    "button": dict(change="AMEND", proposed=lambda: amend_gate("button", "actions <= 1"),
        why="Makes the button's existing 'yields to split-button when a menu hangs off the action' readable, so "
            "the chooser can hand an action with related actions to the split button (observation C). An unknown "
            "`actions` stays unknown: every existing button pick is unchanged.",
        page="_DECIDE-304-when-rules question 6 (this seat's addition, for his eye)", registry=["actions"], obs="C"),
}

def row(slug):
    m = meta(slug)
    cur = m.get("when") or None
    p = PROPOSED.get(slug)
    r = {"slug": slug, "meta": "knowledge/components/%s.meta.json" % slug, "field": "when",
         "provides": m.get("provides"), "current": cur}
    if not p:
        r.update(change="KEEP", proposed=cur,
                 why=("deprecated — its `when` is a redirect, not a predicate" if slug == "view-options"
                      else "authored, parses, and R5's tests pass on it; nothing in this draft changes it"))
        return r
    r.update(change=p["change"], proposed=p["proposed"](), why=p["why"], decision_page=p["page"],
             registry_fields_used=p.get("registry", []))
    if p.get("also"):
        r["also"] = p["also"]
    if p.get("obs"):
        r["observation"] = p["obs"]
    return r

when = {
    "$what": "DRAFT when-rules for the dashboard's parts (R5's 18, derived by script from the two dashboard "
             "templates' $composes + the #261 metas) plus the dashboard frame, and the four parts observation C "
             "touches. NOT IN CANON. Dave rules the wording on Tuesday 29 September.",
    "$how_to_enact": "On his yes, for each row with change != KEEP: set the meta's `when` to `proposed` (a plain "
                     "string replace of one field; rows marked AMEND append clauses to the gate half and keep the "
                     "prose half byte-identical), add the `registry` fields to knowledge/when-fields.json `fields` "
                     "by addition (s273-D4 lets a lane add a name with its definition and example), then run the "
                     "yieldsTo derivation and knowledge/_validate_roles_resolve.py (check 10 when-fields-known). "
                     "check_drafts.py in this folder rehearses every step on a scratch copy.",
    "$source": "R5 notes/_subreports/2026-09-26-304-R5-mcp-probe.md §5c; notes/_DECIDE-304-when-rules-2026-09-26-v1.html",
    "registry_additions": REGISTRY,
    "rows": [row(s) for s in DASH + ["modals", "split-button", "dropdown"]],
}
json.dump(when, open(os.path.join(HERE, "when-rules.proposed.json"), "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- observation A: the bento ground (SUPERSESSIONS rows)
THEMES = ["legacy", "mono", "console", "supercharge"]
sup = []
for th in THEMES:
    sup.append({"type": "dashboard", "theme": th, "dial": "pageBg", "was": "grey", "now": "white",
                "ruled_by": "{{ID_A}}", "supersedes": "the s219-D1 (3) dashboard %s export (pageBg grey)" % th,
                "modes": "both — one default (s220-D2 (2)); the dark leg of the grounds is the open "
                         "$awaitingDave question and this row does not answer it",
                "dave": DAVE_A})
    sup.append({"type": "dashboard", "theme": th, "dial": "bentoBg", "was": "transparent", "now": "grey",
                "ruled_by": "{{ID_A}}", "supersedes": "the s219-D1 (3) dashboard %s export (bentoBg transparent)" % th,
                "modes": "both — one default (s220-D2 (2)); the dark leg of the grounds is the open "
                         "$awaitingDave question and this row does not answer it",
                "dave": DAVE_A})
ALL_METAS = sorted("knowledge/components/" + os.path.basename(f) for f in glob.glob(os.path.join(K, "components", "*.meta.json"))
                   if not os.path.basename(f).startswith("EXAMPLE"))
obs = {
    "$what": "Dave's three Thursday observations (Thu 2026-09-24 15:46, %s) drafted in the exact graph form each "
             "would take, so enactment on his yes is mechanical. NOT IN CANON. He asked that they live in the "
             "graph, not as instructions: \"%s\"" % (THU[0], DAVE_C.split(". these are ")[1] if ". these are " in DAVE_C else DAVE_C),
    "A_bento_ground": {
        "dave": DAVE_A,
        "clash": "BUILT TODAY: s219-D1 (3) ships the dashboard default pageBg = grey, bentoBg = transparent, so the "
                 "whole page is grey, the title area included (template-dashboard-bento.meta.json $bentoGrammar). "
                 "His sentence swaps the two defaults. It does NOT contradict s219-D3: (4) already made pageBg a "
                 "page decision (white or the light greys) and (5) made bentoBg the section ground. R6a's finding, "
                 "confirmed here by reading _bento_edit_rails.json `page_rail` and `dials.bentoBg`.",
        "form": "knowledge/_render/role_defaults_219.py SUPERSESSIONS — the layer his later word is applied "
                "through (s220-D2, s222-D1 precedent); the receipt is never rewritten.",
        "supersessions_append": sup,
        "meta_text": {
            "file": "knowledge/components/template-dashboard-bento.meta.json",
            "$bentoGrammar.pageBg": "white ({{ID_A}}, superseding s219-D1's grey) - the page and the top title "
                                    "section are not grey. The DARK leg is DECLARED-PROVISIONAL and is Dave's, see $awaitingDave.",
            "$bentoGrammar.bentoBg": "grey ({{ID_A}}) - the section the bento wall sits on takes the lightest grey "
                                     "(surface/subtle, #F0F0F0 light) so the white tiles have definition against it.",
        },
        "regen": "After the SUPERSESSIONS append: gen_foundations_217.py (republishes _bento_edit_rails.json "
                 "`defaults`), gen_bento_role_vars.py, then the snippet/canon regen serial in its ruled order. The "
                 "template snippet paints its grounds from its own style (R6a's render override shows the three "
                 "declarations that move: body/.tpl-header on the page ground, main.tpl-page on the wall ground). "
                 "Canon regen is the commit seat's, after Run 3's canon wave.",
        "open": "The dark leg: surface/subtle dark = #1F1F1F = the module surface, 1.00:1. Unchanged by this row "
                "(the same collision exists today on the whole page). Dave's.",
        "decision_page": "_DECIDE-304-when-rules question 4",
    },
    "B_own_size": {
        "dave": DAVE_B,
        "form": "A ruling whose `governs` names every component meta, so the reader's Q1 join (governs[] naming the "
                "meta path, read LIVE) puts it in the `governs` of every seed, for every part. Plus the size check "
                "(Run 4 lane 4c) as its instrument — advisory until Dave promotes it.",
        "wording_proposed": "A part keeps its own size on any page. The page arranges parts; it never shrinks "
                            "them. (R6a's draft wording, shown to Dave on question 5.)",
        "governs_count": len(ALL_METAS),
        "decision_page": "_DECIDE-304-when-rules question 5",
    },
    "C_lightest_pattern": {
        "dave": DAVE_C.split(". these are ")[0] + ".",
        "form": "A ruling governing modals, split-button and dropdown, plus the four `when` rows marked "
                "observation C in when-rules.proposed.json. The `yields to` sentences in modals' prose half are "
                "what the yieldsTo derivation reads (meta.schema.json edges.yieldsTo: DERIVED from the prose half), "
                "so the edges below are the derivation's expected output, listed for review, not hand-written.",
        "yieldsTo_expected": {"knowledge/components/modals.meta.json": [
            {"ref": "component:split-button"}, {"ref": "component:dropdown"}]},
        "cross_role_note": "modals provides `overlay`, split-button `action`, dropdown `input`: three roles, so the "
                           "chooser never ranks them against each other inside one role. The hand-off is the "
                           "yield edge plus the `interrupts` field — a brief that says the choice can be made in "
                           "place rules the modal out.",
        "wording_proposed": "Use the lightest pattern that does the job. Before a modal, ask whether a split "
                            "button or a drop-down would do. (R6a's draft wording, question 6.)",
        "decision_page": "_DECIDE-304-when-rules question 6",
    },
}
json.dump(obs, open(os.path.join(HERE, "observations.proposed.json"), "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- the ruling entries (_inscribe_ruling.py R1 shape: exactly 8 keys)
EVID = ["chat #303 — Dave, %s, verbatim at %s" % (THU[1], THU[0]),
        "notes/_DECIDE-304-when-rules-2026-09-26-v1.html",
        "{{TUESDAY — chat #<n>, Dave's word on the decision page}}"]
rulings = {
    "$what": "Ruling entries in the exact shape _inscribe_ruling.py takes (R1: id/ruled/date/by/says/governs/"
             "evidence/status). Placeholders {{ID_*}}, {{DATE}} and the TUESDAY evidence line are filled at "
             "inscription; `says` then gains his Tuesday word after the Thursday sentence. check_drafts.py dry-runs "
             "each one with placeholder ids.",
    "entries": [
        {"id": "{{ID_A}}", "ruled": "THE BENTO SECTION TAKES THE LIGHTEST GREY; THE PAGE AND THE TITLE AREA DO "
            "NOT. On a dashboard the section the bento wall sits on takes the lightest grey (bentoBg = grey, "
            "surface/subtle) so the white tiles have definition against it; the page ground and the top title "
            "section stay white (pageBg = white). Moves s219-D1 (3)'s shipped dashboard default (pageBg grey, "
            "bentoBg transparent) within s219-D3 (4)(5)'s rails, through role_defaults_219 SUPERSESSIONS, all four "
            "themes; every option stays reachable in the edit pass. The dark leg stays open ($awaitingDave).",
         "date": "{{DATE}}", "by": "Dave", "says": "Dave verbatim (%s): \"%s\" {{TUESDAY_WORD}}" % (THU[1], DAVE_A),
         "governs": ["knowledge/_render/role_defaults_219.py", "knowledge/components/template-dashboard-bento.meta.json"],
         "evidence": EVID, "status": "ruled"},
        {"id": "{{ID_B}}", "ruled": "A PART KEEPS ITS OWN SIZE ON ANY PAGE. The page arranges parts; it never "
            "shrinks them. A component composed onto a page renders at the size of its own reference snippet; a "
            "page style may place a part but never sets its font size, height, padding, width, zoom or transform. "
            "The own-size check (Run 4 lane 4c) is its instrument, advisory until promoted.",
         "date": "{{DATE}}", "by": "Dave", "says": "Dave verbatim (%s): \"%s\" {{TUESDAY_WORD}}" % (THU[1], DAVE_B),
         "governs": ALL_METAS, "evidence": EVID, "status": "ruled"},
        {"id": "{{ID_C}}", "ruled": "USE THE LIGHTEST PATTERN THAT DOES THE JOB. Before a modal, ask whether a "
            "split button or a drop-down would do: the modal keeps its place only when the person must stop "
            "(interrupts = required). Machine-readable as the `when` rows on modals, split-button, dropdown and "
            "button, with modals yielding to split-button (actions >= 2) and dropdown (options >= 5, s270-D1).",
         "date": "{{DATE}}", "by": "Dave", "says": "Dave verbatim (%s): \"%s\" {{TUESDAY_WORD}}" % (THU[1], obs["C_lightest_pattern"]["dave"]),
         "governs": ["knowledge/components/modals.meta.json", "knowledge/components/split-button.meta.json",
                     "knowledge/components/dropdown.meta.json", "knowledge/components/button.meta.json"],
         "evidence": EVID, "status": "ruled"},
    ],
}
json.dump(rulings, open(os.path.join(HERE, "rulings.proposed.json"), "w"), ensure_ascii=False, indent=1)
print("rows", len(when["rows"]), "changes", sum(1 for r in when["rows"] if r["change"] != "KEEP"),
      "| supersessions", len(sup), "| rulings", len(rulings["entries"]), "| B governs", len(ALL_METAS))
