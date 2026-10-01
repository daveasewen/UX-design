#!/usr/bin/env python3
"""#313 lane QQ — re-point the date picker's spec tree at the calendar part (row W-307qq).

Dave, 2026-09-28, by click (s307-D49): 'Yes, the date picker uses the calendar'. The snippet's
panel now carries Calendar's markup (injected CSS block `calendar`, component-types.json). This
script rewrites ONLY the panel's subtree in knowledge/components/date-picker.meta.json and the
state sources that named the old .dp-* selectors. L4's day-cell spec (#313 L4, ae464d01) is kept:
the day is a part of its own with today, selected, empty and disabled as its states. Written
through extract_spec.write_meta (proves every field outside the spec block unchanged).
`reviewed` stays false. Re-running is idempotent (it starts from whatever is on disk and only
replaces the panel's children by name).
Usage: python3 notes/_lanes/313/QQ/repoint_panel.py [--write]
"""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge", "components"))
import extract_spec as X  # noqa: E402

META = os.path.join(ROOT, "knowledge", "components", "date-picker.meta.json")
P = "body > div.dp > div.dp-panel"
PART = "calendar (injected from knowledge/snippets/Calendar.reference.html, PARTIAL calendar; change it there)"
RULING = ("s307-D49, Dave 2026-09-28, by click, verbatim: 'Yes, the date picker uses the calendar; show me "
          "the tree mark and the ring as pictures'")

def panel_children():
    icon = lambda sel: {"part": "arrow-icon", "tag": "svg", "attrs": {"viewbox": "0 0 18 18"},
                        "aria": {"aria-hidden": "true"}, "$sel": sel}
    G = P + " > table.cal-grid"
    return [
        {"part": "cal-head", "tag": "div", "attrs": {"class": "cal-head"}, "$sel": P + " > div.cal-head",
         "$partial": PART,
         "children": [
             {"part": "cal-nav", "tag": "button", "attrs": {"type": "button", "class": "cal-nav", "id": "dp-prev-y"},
              "aria": {"aria-label": "Previous year"}, "$sel": P + " > div.cal-head > button.cal-nav",
              "children": [icon(P + " > div.cal-head > button.cal-nav > svg")], "$repeat": 4},
             {"part": "cal-title", "tag": "span", "attrs": {"class": "cal-title t-cm-label", "id": "dp-title"},
              "aria": {"aria-live": "polite"}, "text": "July 2026",
              "$sel": P + " > div.cal-head > span.cal-title.t-cm-label"},
         ]},
        {"part": "cal-grid", "tag": "table", "attrs": {"class": "cal-grid", "id": "dp-grid"},
         "aria": {"role": "grid", "aria-labelledby": "dp-title"}, "$sel": G, "$partial": PART,
         "children": [
             {"part": "weekday-head", "tag": "thead", "$sel": G + " > thead",
              "children": [
                  {"part": "weekday-row", "tag": "tr", "aria": {"role": "row"}, "$sel": G + " > thead > tr",
                   "children": [
                       {"part": "weekday", "tag": "th", "attrs": {"scope": "col", "abbr": "Monday"},
                        "aria": {"role": "columnheader"}, "$sel": G + " > thead > tr > th", "$repeat": 7,
                        "children": [
                            {"part": "weekday-label", "tag": "span", "attrs": {"class": "cal-wk t-cm-caption"},
                             "text": "Mo", "$sel": G + " > thead > tr > th > span.cal-wk.t-cm-caption"}]}]}]},
             {"part": "days", "tag": "tbody", "attrs": {"id": "dp-body"}, "$sel": G + " > tbody",
              "children": [day()]},
         ]},
    ]

def day():
    return {
        "part": "day", "tag": "button",
        "attrs": {"type": "button", "class": "cal-day t-cm-figure-5", "disabled": "{state.disabled}"},
        "aria": {"aria-selected": "{state.selected}", "aria-current": "{state.today}"},
        "$stateClasses": ["is-today", "is-empty"],
        "$visual": ("built by the snippet's script, not in the static markup: build() writes one tr role=row per "
                    "week and one td per cell (35 or 42); a day of the month is a button.cal-day in its td (the "
                    "td is the grid cell); a pad cell before the 1st or after the last day is span.cal-day.is-empty "
                    "with aria-hidden (not a control). The same markup as the calendar part draws."),
        "$host": P + " > table.cal-grid > tbody",
        "$each": "one per cell of the month grid; an empty cell pads the first and last week",
        "$states": ["today", "selected", "empty", "disabled"],
        "$sources": {
            "today": ["style .cal-day.is-today", "style .cal-day.is-today[aria-selected=\"true\"]"],
            "selected": ["style .cal-day.is-today[aria-selected=\"true\"]", "style .cal-day[aria-selected=\"true\"]",
                         "style button.cal-day[aria-selected=\"true\"]:hover:not(:disabled)"],
            "empty": ["style .cal-day.is-empty"],
            "disabled": ["style .cal-day:disabled (a day outside minDate/maxDate)"],
        },
        "$rest": "a plain day carries none of the four",
        "$aria-current": "the value is the word date when the day is today",
        "$partial": PART,
        "$note": ("the styles also draw hover and focus on a day (button.cal-day:hover:not(:disabled), "
                  ".cal-day:focus-visible); they stay in the field's list until phase 2 (18c, Dave took the "
                  "recommendation: each piece carries its own states (phase 2))"),
    }

SRC_MAP = {
    "style .dp-day:hover": "style button.cal-day:hover:not(:disabled)",
    "style .dp-nav.full:hover": "style .cal-nav.full:hover",
    "style .dp-nav.is-disabled:hover": "style .cal-nav.is-disabled:hover",
    "style .dp-nav:disabled:hover": "style .cal-nav:disabled:hover",
    "style .dp-nav:hover": "style .cal-nav:hover",
    "style .dp-day:focus-visible": "style .cal-day:focus-visible",
    "style .dp-nav:focus-visible": "style .cal-nav:focus-visible",
    "style .dp-day:disabled": "style .cal-day:disabled",
    "style .dp-nav:active": "style .cal-nav:active",
}

def main():
    meta = json.load(open(META, encoding="utf-8"))
    block = {k: meta[k] for k in X.FIELDS + (X.MARK,)}
    panel = [c for c in block["anatomy"]["children"] if c["part"] == "dp-panel"][0]
    panel["children"] = panel_children()
    panel["$partial-note"] = ("the panel is the anchored overlay surface (.dp-panel, the seat's) around the calendar "
                              "part: its children are Calendar's markup and their CSS is injected from Calendar (" + RULING + ")")
    srcs = block["states"]["$sources"]
    for k, lst in srcs.items():
        if isinstance(lst, list):
            srcs[k] = sorted(set(SRC_MAP.get(x, x) for x in lst))
    mk = block[X.MARK]
    if "313-QQ" not in mk["by"]:
        mk["by"] += " · panel on the calendar part @ 313-QQ"
    hand = mk.setdefault("$hand", [])
    what = ("the panel's children re-pointed at the calendar part: cal-head (cal-nav ×4, cal-title), cal-grid "
            "(table: weekday-head › weekday-row › weekday ×7 › weekday-label; days › day); the day keeps L4's four "
            "states (today, selected, empty, disabled), now on button.cal-day in a td; the old dp-head, dp-nav, "
            "dp-title, dp-week and dp-grid are gone from the markup; state sources renamed to the .cal-* selectors")
    if not any(h.get("what") == what for h in hand):
        hand.append({"what": what, "why": RULING + " (row W-307qq)"})
    if "--write" in sys.argv:
        print("written" if X.write_meta(META, block) else "unchanged")
    else:
        print(json.dumps(panel, indent=1, ensure_ascii=False)[:1500])

if __name__ == "__main__":
    main()
