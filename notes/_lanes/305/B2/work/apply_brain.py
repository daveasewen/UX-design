#!/usr/bin/env python3
"""305 B2 — the brain, authored as ONE re-runnable script (idempotent: every edit checks the current value
first and skips if already applied). Writes through jspan.py so each file changes only in the lines meant.
Sitting 2026-09-27 (notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md), calls 8 (when half), 14, 15, 20, 22, 24.
Run from the repo root:  python3 notes/_lanes/305/B2/work/apply_brain.py [--dry]
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jspan as J

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
K = os.path.join(ROOT, "knowledge")
C = os.path.join(K, "components")
DRY = "--dry" in sys.argv
log = []

def edit(path, fn):
    raw = open(path, encoding="utf-8").read()
    new = fn(raw)
    json.loads(new)                                   # still parses
    if new != raw:
        log.append("CHANGED " + os.path.relpath(path, ROOT))
        if not DRY:
            open(path, "w", encoding="utf-8").write(new)
    else:
        log.append("same    " + os.path.relpath(path, ROOT))

# ---------------------------------------------------------------- call 14: the schema accepts a part's states
STATE_DESC_ADD = (" · #305 sitting call 14 (Dave, 2026-09-27, \"yes\"; notes/_DECIDE-304-schema-2026-09-26-v1.html "
    "question 1, the recommended ONE shape): a part may instead carry its STATES — an object whose `states` is the "
    "list of state names (ready, loading, empty, error, stale, …), with ONE SENTENCE PER STATE under the state's own "
    "name saying what the part shows in it, an optional `attribute` naming what selects the state, and `$`-notes. "
    "A catalogue publishes this; a live screen draws every state the list names.")
STATE_OBJ = {"type": "object", "required": ["states"],
             "properties": {"states": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"type": "string"}},
                            "attribute": {"type": "string"}},
             "patternProperties": {"^\\$": {}},
             "additionalProperties": {"type": "string"}}

def schema(raw):
    s = json.loads(raw)
    sm = s["properties"]["stateModel"]
    if "oneOf" in sm:
        return raw
    new = {"description": sm["description"] + STATE_DESC_ADD,
           "oneOf": [{"enum": sm["enum"]}, STATE_OBJ]}
    return J.replace_value(raw, ["properties", "stateModel"], new)

def legend(raw):
    m = json.loads(raw)
    if "states" not in m["stateModel"]:                                        # call 14: the legend gains its list of names
        raw = J.insert_first(raw, ["stateModel"], "states", [k for k in m["stateModel"] if not k.startswith("$")])
    m = json.loads(raw)
    if m["provenance"]["source"] == "hand-authored":                           # call 15: provenance -> code
        raw = J.replace_string(raw, ["provenance", "source"], "code")
    m = json.loads(raw)
    w0 = m["with"][0]
    if "when" in w0:                                                           # call 15: when-note -> a note, recommends
        new = {"slug": w0["slug"], "rel": "recommends", "$when": w0["when"]}
        raw = J.replace_value(raw, ["with", 0], new)
    return raw

def filter_bar(raw):
    m = json.loads(raw)
    sm = m["stateModel"]
    if sm["states"] and isinstance(sm["states"][0], dict):                     # call 14: pairs -> a sentence under each name
        names = [x["name"] for x in sm["states"]]
        shows = {x["name"]: x["shows"] for x in sm["states"]}
        n = J.node_at(raw, ["stateModel", "states"])
        raw = raw[:n["s"]] + json.dumps(names, ensure_ascii=False) + raw[n["e"]:]
        after = "states"
        for nm in names:
            raw = J.insert_after_key(raw, ["stateModel"], after, nm, shows[nm]); after = nm
    m = json.loads(raw)
    if "chipStates" in m["stateModel"]:                                        # the chip's own states: kept, as a note
        raw = J.rename_key(raw, ["stateModel"], "chipStates", "$chipStates")
    return raw

DG_WHEN = ("records >= 2 AND needs in (sort, filter, select, edit) — the record-list for rows the person works on as a "
           "set: it beats list-items (the role's default, s274-D6) whenever sorting, filtering, selecting or editing is "
           "required, and yields to list-items when needs = none.")

def data_grid(raw):
    m = json.loads(raw)
    if m["with"] and isinstance(m["with"][0], str):                            # call 15: six companions as slug objects
        new = []
        for w in m["with"]:
            if " (" in w and w.endswith(")"):
                slug, note = w.split(" (", 1)
                new.append({"slug": slug, "$note": note[:-1]})
            else:
                new.append({"slug": w})
        raw = J.replace_value(raw, ["with"], new)
    m = json.loads(raw)
    rel = m["relationships"]
    if "composes" in rel:                                                      # call 15: composes -> subComponents
        comp, verb = rel["composes"], rel.get("$composes-verbatim")
        last = list(m["subComponents"])[-1]
        raw = J.insert_after_key(raw, ["subComponents"], last, "$composes", comp)
        if verb is not None:
            raw = J.insert_after_key(raw, ["subComponents"], "$composes", "$composes-verbatim", verb)
        raw = J.delete_key(raw, ["relationships"], "$composes-verbatim")
        raw = J.delete_key(raw, ["relationships"], "composes")
    m = json.loads(raw)
    if not m.get("when"):                                                      # call 22: the grid's rule
        raw = J.insert_after_key(raw, [], "provides", "when", DG_WHEN)
    return raw

LINE_OLD_GATE = "answers=change-over-time AND series 1–5 on ONE continuous time axis AND axes=present AND span.cols ≥ 6 —"
LINE_NEW_GATE = ("answers=change-over-time AND series 1–5 on ONE continuous time axis AND axes=present AND span.cols ≥ 6 "
                 "AND units = same AND shape = time-series × 1–5-series —")

def chart_line(raw):                                                           # call 20: both clauses
    w = json.loads(raw)["when"]
    if LINE_NEW_GATE in w:
        return raw
    assert w.startswith(LINE_OLD_GATE), w[:120]
    return J.replace_string(raw, ["when"], LINE_NEW_GATE + w[len(LINE_OLD_GATE):])


LIST_OLD = "records >= 2 AND the records are the same kind, each read ACROSS its own row AND surface in (none, bordered-per-record) —"
LIST_NEW = "records >= 2 AND the records are the same kind, each read ACROSS its own row AND surface in (none, bordered-per-record) AND needs = none —"

def list_items(raw):                                                           # call 22, the list's half: its yield to the grid made readable
    w = json.loads(raw)["when"]
    if LIST_NEW in w:
        return raw
    assert w.startswith(LIST_OLD), w[:140]
    return J.replace_string(raw, ["when"], LIST_NEW + w[len(LIST_OLD):])

RING_CLAUSE = " AND span.cols ≤ 6"
RING_PROSE = (" A ring does not stretch with its tile (ds-030), so it takes a half-width column and never a full-width "
              "row (s305-D9).")
RING_PROSE_V1 = (" A ring is drawn at a fixed diameter (ds-030), so it takes a half-width column and never a full-width "
                 "row (#305, the sitting's call 8).")   # first wording, withdrawn: Dave's s305-D9 comment says not responsive ≠ fixed

def ring(raw):                                                                 # call 8, when half: a narrow column by rule
    w = json.loads(raw)["when"]
    if RING_PROSE_V1 in w:
        return J.replace_string(raw, ["when"], w.replace(RING_PROSE_V1, RING_PROSE))
    if RING_CLAUSE.strip() in w.split("—", 1)[0]:
        return raw
    gate, prose = w.split(" —", 1)
    return J.replace_string(raw, ["when"], gate + RING_CLAUSE + " —" + prose + RING_PROSE)

NEW_WHEN = {   # call 24 — the lightest pattern that does the job; wording from notes/_lanes/304/R4a/drafts/when-rules.proposed.json
    "modals": ("interrupts = required — the person must stop: confirm a consequential action, or finish a task that "
               "cannot share the screen; yields to split-button when interrupts = none AND actions >= 2 (one main action "
               "with a few related ones beside it), and to dropdown when interrupts = none AND options >= 5 (one choice "
               "from a list, made in place, s270-D1)."),
    "split-button": ("actions >= 2 AND interrupts = none — one main action plus a menu of related ones, offered in place "
                     "(button's own `when` already hands this case here); beats modals whenever the related actions can "
                     "be offered without stopping the person."),
    "dropdown": ("options >= 5 AND interrupts = none — one choice from a list, made in place (s270-D1: \"we use dropdowns "
                 "for 5 and above\"); beats modals whenever the choice does not need to stop the person."),
}

def new_when(slug):
    def fn(raw):
        m = json.loads(raw)
        if m.get("when"):
            assert m["when"] == NEW_WHEN[slug], slug
            return raw
        return J.insert_after_key(raw, [], "provides", "when", NEW_WHEN[slug])
    return fn

NEW_FIELDS = [   # calls 22 and 24 — added by addition (s273-D4), definitions from R4a's drafts
    ("needs", "what the person must do to the records as a set (`sort`, `filter`, `select`, `edit`; `none` = they only read them)", "enum", "needs in (sort, filter, select, edit)"),
    ("interrupts", "whether the moment must stop the person until they answer (`required` = a confirmation or a task that cannot share the screen; `none` = the choice can be made in place)", "enum", "interrupts = required"),
    ("actions", "how many related actions hang off one trigger", "count", "actions >= 2"),
    ("options", "how many choices one selection offers", "count", "options >= 5"),
]

def when_fields(raw):
    have = json.loads(raw)["fields"]
    anchor = '    "records": { "definition": "how many already-happened records the reading carries", "kind": "count", "example": "records >= 2" }'
    assert anchor in raw
    add = ""
    for k, d, kind, ex in NEW_FIELDS:
        if k in have:
            continue
        add += ",\n    %s: { \"definition\": %s, \"kind\": %s, \"example\": %s }" % (
            json.dumps(k), json.dumps(d, ensure_ascii=False), json.dumps(kind), json.dumps(ex, ensure_ascii=False))
    if not add:
        return raw
    return raw.replace(anchor, anchor + add, 1)

edit(os.path.join(C, "meta.schema.json"), schema)
edit(os.path.join(C, "legend.meta.json"), legend)
edit(os.path.join(C, "filter-toolbar-bar.meta.json"), filter_bar)
edit(os.path.join(C, "data-grid.meta.json"), data_grid)
edit(os.path.join(C, "chart-line.meta.json"), chart_line)
edit(os.path.join(C, "list-items.meta.json"), list_items)
edit(os.path.join(C, "chart-donut.meta.json"), ring)
edit(os.path.join(C, "chart-pie.meta.json"), ring)
for s in NEW_WHEN:
    edit(os.path.join(C, s + ".meta.json"), new_when(s))
edit(os.path.join(K, "when-fields.json"), when_fields)
print("\n".join(log))
