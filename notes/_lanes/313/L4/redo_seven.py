"""#313 lane L4 — redo the seven cohort-one trees Dave sent back on 2026-10-01 (review page
notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html; his export
notes/_lanes/313/DAVE-RULINGS-2026-10-01-1752-cohort-one-trees-complete.md). On all seven he chose
"Change it (comment)", each on the page's own recommendation, with no comment of his own, so the
page's recommended change is the instruction. Quoted per part in RULED below.

He also took the three word calls on their recommendations: 18a plain words where the markup has
none, set by hand per part; 18b the rest state takes each part's own word ("initial names it");
18c each piece carries its own states (phase 2). 18a and 18b are applied to the seven trees here;
18c is applied only where the instruction already names the piece (the slider's thumb and track,
the date picker's day, the switch's knob and thumb) and is otherwise left to phase 2.

L2's extractor (knowledge/components/extract_spec.py) has no override input beyond ROOT_HINTS, so
the trees are SET BY HAND here, from the base draft at BASE, every change carrying a provenance
line in `$extracted.$hand`. extract_spec.py now refuses to overwrite a meta that carries `$hand`
without --force, so a re-run cannot put the guess back. Writes go through extract_spec.write_meta
(textual addition; every pre-existing field proven equal). Re-running this script is byte-identical:
it always starts from the drafts at BASE, never from its own output.

Usage (repo root): python3 notes/_lanes/313/L4/redo_seven.py [--write]     dry run by default
"""
import copy, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge", "components"))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import extract_spec as X  # noqa: E402

BASE = "e5e0f355"
BY = "extract_spec.py @ 312-L2 · hand-set @ 313-L4"
PAGE = "notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html"
EXPORT = "notes/_lanes/313/DAVE-RULINGS-2026-10-01-1752-cohort-one-trees-complete.md"
SEVEN = ["button", "table", "date-picker", "metric", "slider", "selection-controls", "modals"]

# Verbatim from the page (each part's recommendation), which Dave took at 17:52 with no comment.
RULED = {
    "button": (3, "The tree is the Loading specimen, not the button. The right tree is the button with its type and its label field, and the spinner shown only while processing. … the states and bindings can stay."),
    "table": (5, "start the tree at the table, with the scrolling box as an optional wrapper rather than the part itself; take pressed out (it belongs to the demo switcher above the table, not the table); and make the caption and the cells holes for the title and rows the table already has as choices, not the demo's account names and balances. The caption, header row, body rows and number cells are right."),
    "date-picker": (6, "Add the day part: a day cell in the grid, with today, selected, empty and disabled as its states."),
    "metric": (7, "Name the two figures: the value and the change are what a tile is read for, and the draft calls them span and span-2 … Take busy out; it is loading said twice. The five declared states, the trend choice on the delta and the spark slot are right and stay."),
    "slider": (10, "Name the thumb and the track as parts, with hover, active and disabled, even though the markup has no element for them."),
    "selection-controls": (11, "Give the switch its own tree (switch, label, knob, thumb; states off, on, disabled, error), and the same for checkbox, radio and chip. … Whether that is four metas or four roots in one is the comment to leave."),
    "modals": (14, "Take inert and disabled out of the dialog's states; they belong to the page. The parts are right."),
}
WORDS_A = "18a, Dave took the recommendation: plain words where the markup has none, set by hand per part"
WORDS_B = "18b, Dave took the recommendation: the rest state takes each part's own word, initial names it"
WORDS_C = "18c, Dave took the recommendation: each piece carries its own states (phase 2)"


def base_meta(mid):
    raw = subprocess.check_output(["git", "-C", ROOT, "show", "%s:knowledge/components/%s.meta.json" % (BASE, mid)])
    return json.loads(raw)


def hand(rows, what, why):
    rows.append({"what": what, "why": why})


def find(n, part):
    if n.get("part") == part:
        return n
    for c in n.get("children", []):
        r = find(c, part)
        if r:
            return r
    return None


def rename(n, old, new, rows=None, why=WORDS_A):
    """rows=None: the caller records the renames as one line."""
    node = find(n, old)
    assert node, (old, new)
    node["part"] = new
    if rows is not None:
        hand(rows, "part %s renamed %s" % (old, new), why)
    return node


def drop_states(st, words, rows, why):
    st["states"] = [s for s in st["states"] if s not in words]
    st["transitions"] = [t for t in st.get("transitions", [])
                         if t["to"] not in words and t["from"] not in words
                         and not (t["on"] == "props.disabled" and "disabled" in words)]
    for w in words:
        st.get("$sources", {}).pop(w, None)
    hand(rows, "states " + ", ".join(words) + " taken out (and their arrows)", why)


# ─────────────────────────────── the seven ───────────────────────────────
def button(m, rows):
    r = RULED["button"][1]
    a = m["anatomy"]
    a["text"] = "{props.label}"
    hand(rows, "the button's words: the literal \"Loading\" replaced by the label field {props.label}", r)
    spin = a["children"][0]
    spin["$when"] = "{state.processing}"
    spin["$note"] = "present only while processing; a button at rest has no spinner"
    hand(rows, "the spinner kept as the one child, marked present only while processing", r)
    a["$note"] = ("the button, read from its first instance (the default primary); its type is the class hole "
                  "{props.type}, its words the label field (s305-D17). The 312 draft took the richest of six "
                  "instances, the Loading specimen.")
    hand(rows, "root re-read as the default button, not the Loading specimen ($sel already names the first instance)", r)
    hand(rows, "states (7, rest default) and bindings (29) unchanged", "\"the states and bindings can stay\"")
    m["$extracted"]["$root"] = "name affinity 3 (button.btn.primary) → the first instance, the default button (hand-set 313-L4; the 312 draft took the richest of 6, the Loading one)"


def table(m, rows):
    r = RULED["table"][1]
    scroll = m["anatomy"]
    tbl = scroll["children"][0]
    wrapper = {k: v for k, v in scroll.items() if k != "children"}
    wrapper["aria"] = dict(wrapper["aria"], **{"aria-label": "{props.title}"})
    wrapper["$optional"] = True
    wrapper["$note"] = ("an optional wrapper, not the part: a focusable region you can tab into and pan when the "
                        "table is wider than its box. Its name is the table's title (the demo's words were the "
                        "caption plus the date and ', scrollable').")
    tbl["$wrapper"] = wrapper
    m["anatomy"] = tbl
    hand(rows, "the tree starts at the table; the scrolling box is an optional wrapper on it ($wrapper), named by the title", r)
    cap = find(tbl, "caption")
    cap["text"] = "{props.title}"
    sub = find(tbl, "sub")
    sub.pop("text", None)
    sub["$note"] = "the caption's second line; no setting carries it yet, so the demo's date line is taken out, not kept"
    hand(rows, "caption's words: \"Account balances\" replaced by the title field {props.title}; the sub-line's demo date removed", r)
    names = [("thead", "head"), ("tr", "header-row"), ("th", "column-header"), ("num", "number-header"),
             ("tbody", "body"), ("tr-2", "row"), ("th-2", "row-header"), ("v", "row-header-value"),
             ("td", "cell"), ("v-2", "cell-value"), ("num-2", "number-cell"), ("v-3", "number-value")]
    for old, new in names:
        rename(tbl, old, new)
    hand(rows, "plain words for the tag names: " + ", ".join("%s → %s" % p for p in names), WORDS_A)
    heading = "the column's heading, from the rows setting (its first entry when headers run along the top, headerType)"
    for part in ("column-header", "number-header"):
        n = find(tbl, part)
        n["text"] = "{props.rows}"
        n["$hole"] = heading
    find(tbl, "row")["$each"] = "{props.rows}"
    for part in ("row-header-value", "cell-value", "number-value"):
        n = find(tbl, part)
        n["text"] = "{props.rows}"
        n["$hole"] = "this cell's value, from its row in the rows setting"
    for part in ("row-header", "cell", "number-cell"):
        n = find(tbl, part)
        n["attrs"]["data-label"] = "{props.rows}"
        n["$hole-data-label"] = "the column's heading again, shown as the card label when the table collapses"
    hand(rows, "every header cell, body cell and card label is a hole on the rows field {props.rows}; the body row repeats once per row ($each); the demo's account names and balances removed", r)
    st = m["states"]
    drop_states(st, ["pressed"], rows, r)
    drop_states(st, ["disabled"], rows,
                "same reason as pressed: its only source was the demo switcher (style .seg button:disabled), not the table — flagged on the re-look page")
    st["$sources"]["hover"] = [s for s in st["$sources"]["hover"] if ".seg" not in s]
    st["$sources"]["focus"] = [s for s in st["$sources"]["focus"] if ".seg" not in s]
    st["$sources"]["$removed"] = "pressed and disabled were read only from the demo's header-type switcher (.seg), which sits above the table and is not part of it"
    st["$sources"]["$pieces"] = "hover is the body row's highlight, focus the wrapper's ring; giving each its own piece is phase 2 (" + WORDS_C + ")"
    hand(rows, "hover and focus keep only the table's own sources (the row highlight, the scroll region's ring); the switcher's lines removed", r)
    m["$extracted"]["$listeners"] = []
    m["$extracted"]["$listeners-note"] = "the page's only click listener is the demo switcher's; the table itself listens to nothing"
    hand(rows, "listens: click removed (it was the demo switcher's)", r)
    m["$extracted"]["$root"] = "name affinity 3 (table.table); the 312 draft climbed to div.scroll, now an optional $wrapper (hand-set 313-L4)"


def date_picker(m, rows):
    r = RULED["date-picker"][1]
    a = m["anatomy"]
    grid = find(a, "dp-grid")
    st = m["states"]
    moved = {w: st["$sources"].get(w, []) for w in ("today", "selected", "empty")}
    moved["disabled"] = ["style .dp-day:disabled (a day outside minDate/maxDate)"]
    grid["children"] = [{
        "part": "day",
        "tag": "button",
        "attrs": {"type": "button", "class": "dp-day t-cm-figure-5", "disabled": "{state.disabled}"},
        "aria": {"role": "gridcell", "aria-selected": "{state.selected}", "aria-current": "{state.today}"},
        "$stateClasses": ["is-today", "is-empty"],
        "$visual": "built by the snippet's script, not in the static markup: build() makes one button.dp-day per cell of the month (35 or 42), role gridcell, seven to a div role=row (display: contents)",
        "$host": grid["$sel"],
        "$each": "one per cell of the month grid; an empty cell pads the first and last week",
        "$states": ["today", "selected", "empty", "disabled"],
        "$sources": moved,
        "$rest": "a plain day carries none of the four",
        "$aria-current": "the value is the word date when the day is today",
        "$note": "the styles also draw hover and focus on a day (.dp-day:hover, .dp-day:focus-visible); they stay in the field's list until phase 2 (" + WORDS_C + ")",
    }]
    hand(rows, "the day part added inside the grid (button.dp-day, role gridcell) with its own states today, selected, empty, disabled; marked $visual (built by the script) and resolved through the grid", r)
    st["states"] = [s for s in st["states"] if s not in ("today", "selected", "empty")]
    for w in ("today", "selected", "empty"):
        st["$sources"].pop(w, None)
    st["$sources"]["$moved"] = "today, selected and empty moved to the day's own list (anatomy › day › $states)"
    st["$sources"]["$pieces"] = "the message's words (ok, info, warning, success) and the panel's (open, static) still sit in the field's list; per piece in phase 2 (" + WORDS_C + ")"
    hand(rows, "today, selected and empty moved off the field's list onto the day (the piece the instruction names); disabled stays on both", WORDS_C)
    rename(a, "span", "weekday")
    rename(a, "icn", "calendar-icon")
    rename(a, "icn-2", "arrow-icon")
    hand(rows, "plain words: span → weekday, icn → calendar-icon, icn-2 → arrow-icon (the extractor's count)", WORDS_A)
    hand(rows, "rest state stays default (no word of its own in the meta)", WORDS_B)


def metric(m, rows):
    r = RULED["metric"][1]
    a = m["anatomy"]
    v = rename(a, "span", "value", rows, r)
    v["$note"] = "the figure a tile is read for; the unit sits beside it"
    c = rename(a, "span-2", "change", rows, r)
    c["$note"] = "the change figure; its direction is the delta's trend choice"
    a["aria"]["aria-busy"] = "{state.loading}"
    hand(rows, "aria-busy now reads the loading state", r)
    st = m["states"]
    drop_states(st, ["busy"], rows, r)
    st["$sources"]["loading"] = st["$sources"]["loading"] + ["attribute aria-busy on a twin of body > div.board > div.metric (was a separate busy state; folded in)"]
    hand(rows, "the five declared states (ready, loading, empty, error, stale), the trend choice and the spark slot unchanged; rest stays ready, the metric's own word", WORDS_B)


def slider(m, rows):
    r = RULED["slider"][1]
    a = m["anatomy"]
    inp = find(a, "input")
    host = inp["$sel"]
    src_thumb = {"hover": ["Dave's ruling (review 312 call 10); the snippet styles no :hover on the thumb — the meta's handleState names it"],
                 "active": ["Dave's ruling (review 312 call 10); the meta's handleState calls this look pressed"],
                 "disabled": ["Dave's ruling (review 312 call 10); the snippet styles no disabled slider"],
                 "focus-ring": ["style input[type=range]:focus-visible::-webkit-slider-thumb (the ring is drawn on the thumb; focus stays the field's state until phase 2)"]}
    thumb = {
        "part": "thumb", "tag": "span",
        "$visual": "drawn by the browser from the range input (::-webkit-slider-thumb, ::-moz-range-thumb); no element in the markup",
        "$host": host,
        "$tag": "span is a placeholder for a library that draws the thumb as an element; the reference page has none",
        "$states": ["default", "hover", "active", "disabled"], "$initial": "default",
        "$sources": src_thumb,
        "$note": "the double type has two thumbs on one track",
    }
    track = {
        "part": "track", "tag": "span",
        "$visual": "drawn by the browser from the range input (::-webkit-slider-runnable-track, ::-moz-range-track); no element in the markup",
        "$host": host,
        "$tag": "span is a placeholder for a library that draws the track as an element; the reference page has none",
        "$states": ["default", "hover", "active", "disabled"], "$initial": "default",
        "$sources": {"hover": ["Dave's ruling (review 312 call 10)"], "active": ["Dave's ruling (review 312 call 10)"],
                     "disabled": ["Dave's ruling (review 312 call 10)"]},
        "$note": "the filled length is the track's own background up to --pct, which the script sets on input (filled scrollbar/foreground, unfilled scrollbar/background)",
        "children": [thumb],
    }
    inp["children"] = [track]
    hand(rows, "track and thumb named as parts inside the range input, each with its own states default, hover, active, disabled; both marked $visual (browser-drawn) and resolved through the input", r)
    hand(rows, "the pieces' rest word is default, the meta's own handleState default", WORDS_B)
    m["states"]["$sources"]["$pieces"] = "the thumb's and the track's states sit on those pieces (anatomy › input › track › thumb); the field keeps default and focus"


def modals(m, rows):
    r = RULED["modals"][1]
    st = m["states"]
    drop_states(st, ["inert", "disabled"], rows, r)
    st["$sources"]["$removed"] = ("inert is what the open dialog does to the page behind it, and disabled is what it does to "
                                  "the button that opened it; both read from the script's click handler, neither is a look of the dialog")
    a = m["anatomy"]
    t = rename(a, "h2", "title")
    t["text"] = "{props.title}"
    b = rename(a, "p", "body")
    b["text"] = "{props.body}"
    hand(rows, "title and body take their words from the title and body fields; the demo's payment sentence removed", WORDS_A + " (and s305-D17: a part's own words are a field on the part)")
    rename(a, "btn", "confirm", rows, WORDS_A + " — the markup's own ids, confirm and cancel; btn-2 was the extractor's count")
    rename(a, "btn-2", "cancel", rows, WORDS_A + " — the markup's own ids")
    hand(rows, "rest state stays closed, the dialog's own word", WORDS_B)


# ───────────────────────── the switch and its family ─────────────────────────
SC = "body > div.sc"


def message(sel, idv):
    return {"part": "message", "tag": "p", "attrs": {"class": "err-msg", "id": idv}, "$sel": sel,
            "$when": "{state.error}", "$note": "a sibling after the row, tied to the control by aria-describedby"}


def selection_controls(m, rows):
    r = RULED["selection-controls"][1]
    old = m["anatomy"]
    st_err = ["class .is-error on a twin row (.field.is-error)", "attribute aria-invalid=\"true\" on its input"]
    st_dis = ["class .is-disabled on a twin row", "attribute disabled on its input"]
    four_states = ["off", "on", "disabled", "error"]
    switch = {
        "part": "switch", "tag": "div", "attrs": {"class": "field"}, "$stateClasses": ["is-disabled", "is-error"],
        "$sel": SC + " > div.field",
        "$states": four_states, "$initial": "off",
        "$transitions": [{"from": "off", "on": "change", "to": "on"}, {"from": "on", "on": "change", "to": "off"}],
        "$sources": {"on": ["attribute checked on a twin input[role=switch]", "style input:checked + label .switch"],
                     "disabled": st_dis + ["style input:disabled + label .switch"],
                     "error": st_err + ["style .field.is-error .switch"]},
        "$note": "the styles also draw hover and a focus ring on the knob (label:hover .switch, input:focus-visible + label .switch); not in the ruled four",
        "$message": message(SC + " > p.err-msg", "s4e"),
        "children": [
            {"part": "input", "tag": "input", "attrs": {"type": "checkbox", "checked": "{state.on}", "disabled": "{state.disabled}"},
             "aria": {"role": "switch", "aria-invalid": "{state.error}"}, "$sel": SC + " > div.field > input[role=switch]",
             "$note": "the native checkbox under the drawing: hidden, it carries the state and the name for a screen reader"},
            {"part": "label", "tag": "label", "text": "{props.label}", "$sel": SC + " > div.field > label",
             "children": [
                 {"part": "knob", "tag": "span", "attrs": {"class": "switch"}, "$sel": SC + " > div.field > label > span.switch",
                  "$states": four_states, "$initial": "off",
                  "$sources": {"on": ["style input:checked + label .switch"], "disabled": ["style input:disabled + label .switch"],
                               "error": ["style .field.is-error .switch", "style .field.is-error input:checked + label .switch"]},
                  "children": [
                      {"part": "thumb", "tag": "span", "attrs": {"class": "thumb"}, "$sel": SC + " > div.field > label > span.switch > span.thumb",
                       "$states": four_states, "$initial": "off",
                       "$sources": {"on": ["style input:checked + label .switch .thumb"], "disabled": ["style input:disabled + label .switch .thumb"],
                                    "error": ["style .field.is-error .switch .thumb"]}}]}]}],
    }
    checkbox = {
        "part": "checkbox", "tag": "div", "attrs": {"class": "field"}, "$stateClasses": ["is-disabled", "is-error"],
        "$sel": SC + " > div.field",
        "$states": ["unchecked", "checked", "indeterminate", "hover", "active", "focus", "disabled", "error"], "$initial": "unchecked",
        "$transitions": [{"from": "unchecked", "on": "change", "to": "checked"}, {"from": "checked", "on": "change", "to": "unchecked"},
                         {"from": "indeterminate", "on": "change", "to": "checked"}],
        "$sources": {"checked": ["attribute checked on a twin input", "style input:checked + label .box"],
                     "indeterminate": ["script: input.indeterminate = true, aria-checked mixed", "style input:indeterminate + label .box"],
                     "hover": ["style label:hover .box"], "active": ["style input:active + label .box"],
                     "focus": ["style input:focus-visible + label .box"], "disabled": st_dis, "error": st_err + ["style .field.is-error .box"]},
        "$message": message(SC + " > p.err-msg", "c5e"),
        "children": [
            {"part": "input", "tag": "input", "attrs": {"type": "checkbox", "checked": "{state.checked}", "disabled": "{state.disabled}"},
             "aria": {"aria-checked": "{state.indeterminate}", "aria-invalid": "{state.error}"}, "$sel": SC + " > div.field > input",
             "$aria-checked": "the value is the word mixed while indeterminate, set by the script",
             "$note": "the native checkbox under the drawing: hidden, it carries the state and the name"},
            {"part": "label", "tag": "label", "text": "{props.label}", "$sel": SC + " > div.field > label",
             "children": [
                 {"part": "box", "tag": "span", "attrs": {"class": "box"}, "$sel": SC + " > div.field > label > span.box",
                  "children": [
                      {"part": "tick", "tag": "svg", "attrs": {"viewbox": "0 0 18 18"}, "$sel": SC + " > div.field > label > span.box > svg",
                       "$note": "the tick path, or the dash when indeterminate (checkboxKind); drawn by stroke"}]}]}],
    }
    radio = {
        "part": "radio", "tag": "div", "attrs": {"class": "field"}, "$stateClasses": ["is-disabled", "is-error"],
        "$sel": SC + " > fieldset > div.field",
        "$wrapper": {"part": "radio-group", "tag": "fieldset", "$sel": SC + " > fieldset",
                     "$legend": {"part": "legend", "tag": "legend", "$sel": SC + " > fieldset > legend"},
                     "$note": "radios always come in a group: the fieldset and its legend wrap the rows; arrow keys move within it (the browser's own)"},
        "$states": ["unchecked", "checked", "hover", "active", "focus", "disabled", "error"], "$initial": "unchecked",
        "$transitions": [{"from": "unchecked", "on": "change", "to": "checked"}],
        "$sources": {"checked": ["attribute checked on a twin input", "style input:checked + label .radio"],
                     "hover": ["style label:hover .radio"], "active": ["style input:active + label .radio"],
                     "focus": ["style input:focus-visible + label .radio"], "disabled": st_dis,
                     "error": st_err + ["style .field.is-error .radio"]},
        "$message": message(SC + " > fieldset > p.err-msg", "r4e"),
        "children": [
            {"part": "input", "tag": "input", "attrs": {"type": "radio", "checked": "{state.checked}", "disabled": "{state.disabled}"},
             "aria": {"aria-invalid": "{state.error}"}, "$sel": SC + " > fieldset > div.field > input",
             "$note": "the native radio under the drawing: hidden, it carries the state, the group and the name"},
            {"part": "label", "tag": "label", "text": "{props.label}", "$sel": SC + " > fieldset > div.field > label",
             "children": [
                 {"part": "ring", "tag": "span", "attrs": {"class": "radio"}, "$sel": SC + " > fieldset > div.field > label > span.radio",
                  "$name": "ring, the stylesheet's own word for it (\"radio ring+dot\"); the class radio would repeat the part's name",
                  "children": [{"part": "dot", "tag": "span", "attrs": {"class": "dot"}, "$sel": SC + " > fieldset > div.field > label > span.radio > span.dot"}]}]}],
    }
    chip = {
        "part": "chip", "tag": "button", "attrs": {"type": "button", "class": "chip", "disabled": "{state.disabled}"},
        "aria": {"aria-pressed": "{state.on}"}, "text": "{props.label}",
        "$sel": SC + " > div.chips > button.chip",
        "$wrapper": {"part": "chip-group", "tag": "div", "attrs": {"class": "chips"}, "$sel": SC + " > div.chips",
                     "$role-by-kind": {"toggle": "group", "single-selection": "radiogroup", "delete": "none (named by aria-label only)"}},
        "$kinds": {"toggle": "a button whose aria-pressed carries on and off; an optional star icon",
                   "single-selection": "a button with role radio whose aria-checked carries on and off, in a radiogroup with roving arrow keys",
                   "delete": "a span.chip.chip-del holding the words and a remove button (the root is a span, not a button, so the remove button is not nested in a button)",
                   "multiple-selection": "named by the chipType setting; not drawn on the reference page"},
        "$states": ["off", "on", "hover", "active", "focus", "disabled"], "$initial": "off",
        "$transitions": [{"from": "off", "on": "click", "to": "on"}, {"from": "on", "on": "click", "to": "off", "guard": "toggle kind"}],
        "$keys": {"ArrowRight": "next", "ArrowDown": "next", "ArrowLeft": "previous", "ArrowUp": "previous", "Home": "first", "End": "last"},
        "$keys-source": "single-selection kind only; read from the snippet's keydown handler",
        "$sources": {"on": ["attribute aria-pressed=\"true\" (toggle)", "attribute aria-checked=\"true\" (single selection)", "style .chip[aria-pressed=\"true\"], .chip[aria-checked=\"true\"]"],
                     "hover": ["style .chip:hover"], "active": ["style .chip:active"], "focus": ["style .chip:focus-visible"],
                     "disabled": ["attribute disabled on a twin chip", "style .chip:disabled"]},
        "children": [
            {"part": "icon", "tag": "svg", "aria": {"aria-hidden": "true"}, "attrs": {"viewbox": "0 0 24 24"},
             "$sel": SC + " > div.chips > button.chip > svg", "$when": "toggle kind, optional", "$note": "the star, outline at off, filled at on"},
            {"part": "remove", "tag": "button", "attrs": {"type": "button", "class": "x"}, "aria": {"aria-label": "{props.label}"},
             "$sel": SC + " > div.chips > span.chip.chip-del > button.x", "$when": "delete kind only",
             "$aria-label": "the demo reads 'Remove GBP filter': the word Remove before the chip's label"}],
    }
    m["anatomy"] = {
        "part": "selection-controls", "tag": "div", "attrs": {"class": "sc"}, "$sel": SC,
        "$members": ("four trees in one part, one per control, switch first (your word). Each carries its own states "
                     "($states, $initial, $transitions) on its own root. Part names are unique within each tree, so a "
                     "four-meta split renames nothing."),
        "$split": ("if the four become four metas (switch, checkbox, radio, chip): each child here becomes that meta's "
                   "anatomy; its $states/$initial/$transitions become the meta's states; its bindings are the "
                   "$by-member list; the shared label prop and the control setting go with each; this family meta "
                   "would keep only what is shared or become an alias seat"),
        "children": [switch, checkbox, radio, chip],
    }
    hand(rows, "the family's 29-node tree replaced by four trees, one per control (switch, checkbox, radio, chip), each a root under the family wrapper", r)
    hand(rows, "the switch's tree: switch (the row), input (role switch), label, knob, thumb; states off, on, disabled, error on the switch and on knob and thumb", r + " · " + WORDS_C)
    hand(rows, "plain words for the numbered names (field-3, label-3, span-2, input-2, button-2, chips-2 …): knob, ring, tick, remove, chip-group, radio-group", WORDS_A)
    hand(rows, "each control rests in its own word: off (switch, chip), unchecked (checkbox, radio)", WORDS_B)
    hand(rows, "every label's words are the label field {props.label}; the demo's sentences removed", "s305-D17 (a part's own words are a field on the part), as on the button")
    st = m["states"]
    union = []
    for t in (switch, checkbox, radio, chip):
        for s in t["$states"]:
            if s not in union:
                union.append(s)
    m["states"] = {
        "states": union, "initial": "off",
        "keys": st.get("keys", {}),
        "$keys-source": st.get("$keys-source", "") + "; they are the single-selection chip group's (also on chip › $keys)",
        "$initial": ("the family has no rest of its own: each control's is on its own root (off for switch and chip, "
                     "unchecked for checkbox and radio). off is written here because the schema asks for one and the "
                     "switch is drafted first; a four-meta split removes this union."),
        "$members": "this list is the union of the four controls' own lists; read each control's machine on its root",
    }
    hand(rows, "the family's one state list replaced by the union of the four, each control's own machine on its root", WORDS_C)
    m["bindings"]["$by-member"] = {
        "switch": ["--ctrl-border", "--ctrl-border-active", "--ctrl-border-disabled", "--checked", "--glyph", "--error-atom", "--focus", "--label", "--label-disabled"],
        "checkbox": ["--ctrl-border", "--ctrl-border-active", "--ctrl-border-disabled", "--checked", "--glyph", "--chip-hover", "--error-atom", "--focus", "--label", "--label-disabled", "--border-radius-control"],
        "radio": ["--ctrl-border", "--ctrl-border-active", "--ctrl-border-disabled", "--checked", "--error-atom", "--focus", "--label", "--label-disabled"],
        "chip": ["--ctrl-border", "--ctrl-border-disabled", "--checked", "--glyph", "--chip-hover", "--chip-pressed", "--focus", "--label", "--label-disabled", "--border-radius-control"],
        "message": ["--error"], "page": ["--page"],
        "$unused": "--reverse is in the manifest and the light/dark blocks but no rule in the snippet reads it",
        "$source": "which rules read each var, from the snippet's <style> (313-L4, by hand)",
    }
    hand(rows, "bindings unchanged (15); a $by-member list says which control reads each, for the split", r)
    m["$extracted"]["$root"] = "name affinity 2 (div.sc) — the family wrapper; four control trees under it, hand-set 313-L4"


DO = {"button": button, "table": table, "date-picker": date_picker, "metric": metric, "slider": slider,
      "selection-controls": selection_controls, "modals": modals}


def redo(mid):
    m = base_meta(mid)
    before = copy.deepcopy(m)
    rows = []
    DO[mid](m, rows)
    n, r = RULED[mid]
    ex = m["$extracted"]
    ex["by"] = BY
    ex["reviewed"] = False
    ex["$hand"] = rows
    ex["$hand-source"] = ("Dave, review page %s call %d, 'Change it (comment)' on the page's recommendation, no comment "
                          "of his own; export %s (2026-10-01 17:52). The recommendation, verbatim: \"%s\"" % (PAGE, n, EXPORT, r))
    ex["$hand-note"] = "set by hand (the extractor has no override input); extract_spec.py refuses to overwrite a meta carrying $hand without --force"
    block = {k: m[k] for k in X.FIELDS + (X.MARK,)}
    return before, block, rows


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    write = "--write" in sys.argv
    for mid in SEVEN:
        before, block, rows = redo(mid)
        path = os.path.join(ROOT, "knowledge", "components", mid + ".meta.json")
        print("%s — %d hand changes" % (mid, len(rows)))
        if write:
            changed = X.write_meta(path, block)
            print("   wrote" if changed else "   unchanged (byte-identical)")
        kind, reasons = X.coverage_of_meta(path) if write else ("(dry run)", [])
        print("   coverage on disk:", kind, reasons or "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
