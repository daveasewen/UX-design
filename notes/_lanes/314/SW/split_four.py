"""#314 lane SW — split the selection-controls family into four parts: switch, checkbox, radio, chip.

RULED (quoted from knowledge/_rulings.json, never paraphrased):
  s313-D10 — the page's recommendation Dave took at 17:52 Thu 2026-10-01: "Give the switch its own tree
    (switch, label, knob, thumb; states off, on, disabled, error), and the same for checkbox, radio and chip.
    One tree for four controls will not describe any of them to a client library."
  s313-D56 — 23:17, call 9, Dave by click: "Four parts (the recommendation)". The page: "Four parts, or four
    trees in one part? Recommendation: four parts. A client library looks each one up by its own name: it asks
    for a switch, not for the second tree inside selection controls."
  s313-D54 — 23:17, call 7, Dave by click on the redone four-tree page: "Yes, it describes the part".
  s311-D4 — the neutral spec lives in the meta as four fields: anatomy, states, emits, bindings.

WHAT IT DOES (always from the family meta at BASE, never from its own output, so a re-run is byte-identical):
  1. Writes knowledge/components/{switch,checkbox,radio,chip}.meta.json. Each member's tree is the family's
     child of that name EXACTLY as Dave passed it at call 7 (lane L4, s313-D54), carried out as the family's own
     `$split` note says: "each child here becomes that meta's anatomy; its $states/$initial/$transitions become
     the meta's states; its bindings are the $by-member list; the shared label prop and the control setting go
     with each". Nothing in a tree is renamed, added or removed: only the root's machine notes ($states,
     $initial, $transitions, $keys, $keys-source, $sources) move from the root into the meta's `states` field.
     The catalogue fields the schema requires of a non-alias meta (props, tokens, relationships, accessibility,
     antiPatterns, tokenValidation, provenance) are SLICED from the family meta, entry by entry, each slice
     naming where it came from where the schema allows a note (relationships allows none: its entries are the
     family's livesInside and commonPatterns words that name or fit the control); no new prose claim is made
     about a control beyond its plain-words `purpose`.
  2. Takes the four spec fields and their `$extracted` marker off the family meta (the spec moved, it is not
     deleted: it now lives once, on the members) and leaves a `$split` record in their place. The family meta
     STAYS: the snippet's manifest names "Selection controls" (the coverage gate needs its meta), it is the
     `input` role's provider in knowledge/roles.json, data-grid's selection-checkbox is containedBy it, and its
     catalogue identity (props, variants, edges) is untouched. Its text before the spec block is kept byte-for-byte.

Usage (repo root): python3 notes/_lanes/314/SW/split_four.py [--write]     dry run by default
"""
import copy, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BASE = "8d8e91da"
FAMILY = "knowledge/components/selection-controls.meta.json"
SNIPPET = "Selection-controls.reference.html"
BY = "extract_spec.py @ 312-L2 · hand-set @ 313-L4 · split into four parts @ 314-SW"
DATE = "2026-10-02"
SPEC = ("anatomy", "states", "emits", "bindings", "$extracted")
D56 = ("s313-D56 (#313, Dave by click, Thu 2026-10-01 23:17 BST, seven-trees-redone page call 9): "
       "'Four parts (the recommendation)', comment: none. The page, verbatim: 'Four parts, or four trees in one part? "
       "Recommendation: four parts. A client library looks each one up by its own name: it asks for a switch, not for "
       "the second tree inside selection controls.' Export: notes/_lanes/313/DAVE-RULINGS-2026-10-01-2317-seven-trees-redone.md.")
D10 = ("Give the switch its own tree (switch, label, knob, thumb; states off, on, disabled, error), and the same for "
       "checkbox, radio and chip. One tree for four controls will not describe any of them to a client library.")
MACHINE = ("$states", "$initial", "$transitions", "$keys", "$keys-source", "$sources")

# Per member: the slices of the family meta. Every entry is the family's own text; the keys say which entry.
MEMBERS = {
    "switch": {
        "name": "Switch",
        "purpose": "An on/off control for one setting, with its label: a rounded pill (the knob) whose thumb slides "
                   "across when it is on. One of the four selection controls (s313-D56); drawn by the Switch rows of "
                   "the Selection-controls reference.",
        "variant": "switch",
        "props": ["label"],
        "tokens": ["label", "error", "$darkDecision-selected-fill", "chip/switch selected-surface (DEPRECATED)",
                   "chip/switch off+delete-surface (DEPRECATED)", "on-dark glyph/text (DEPRECATED)",
                   "switch disabled track (DEPRECATED)"],
        "livesInside": ["Form", "Settings (switch)"],
        "commonPatterns": ["on/off setting toggle"],
        "a11y": ["semantics", "switch", "error", "focus"],
        "anti": [0, 2],
        "usedBy": ("Switch",),
        "audited": "Switch 1503:74680",
        "message": True,
        "listeners": [],
        "listeners-note": "the snippet attaches no listener to a switch: the native checkbox under it carries on and off",
    },
    "checkbox": {
        "name": "Checkbox",
        "purpose": "A square box the user ticks to choose an option, with its label; it can also show a dash for a "
                   "partly chosen set (indeterminate). One of the four selection controls (s313-D56); drawn by the "
                   "Checkbox rows of the Selection-controls reference.",
        "variant": "checkbox",
        "props": ["checkboxKind", "label"],
        "tokens": ["box/control-surface", "box/control-border", "check-radio-glyph", "label", "error",
                   "$darkDecision-selected-fill"],
        "livesInside": ["Form", "Field set", "List/Card select"],
        "commonPatterns": ["checkbox/radio group", "selectable list/card"],
        "a11y": ["semantics", "indeterminate", "error", "focus"],
        "anti": [0, 1],
        "usedBy": ("Checkbox",),
        "audited": "Checkbox 811:68448 (clean)",
        "message": True,
        "listeners": ["change"],
        "listeners-note": "the one listener is the indeterminate specimen's change handler (it clears the dash)",
    },
    "radio": {
        "name": "Radio",
        "purpose": "A round control for picking one option from a group, with its label: a ring that fills with a dot "
                   "when chosen. Radios always come in a group. One of the four selection controls (s313-D56); drawn "
                   "by the Radio rows of the Selection-controls reference.",
        "variant": "radio",
        "props": ["label"],
        "tokens": ["box/control-border", "check-radio-glyph", "label", "error", "$darkDecision-selected-fill"],
        "livesInside": ["Form", "Field set"],
        "commonPatterns": ["checkbox/radio group"],
        "a11y": ["semantics", "error", "focus"],
        "anti": [0, 1],
        "usedBy": ("Radio",),
        "audited": "Radio button 1533:80165 (clean)",
        "message": True,
        "listeners": [],
        "listeners-note": "the snippet attaches no listener to a radio: the native radio and its group carry the choice and the arrow keys",
    },
    "chip": {
        "name": "Chip",
        "purpose": "A small square-cornered button the user presses to choose: a toggle (on or off, with an optional "
                   "star), a single choice in a group (arrow keys move it), or a removable chip with a remove button. "
                   "One of the four selection controls (s313-D56); drawn by the Chips rows of the Selection-controls "
                   "reference.",
        "variant": "chip",
        "props": ["chipType", "label"],
        "tokens": ["label", "$darkDecision-selected-fill", "chip/switch selected-surface (DEPRECATED)",
                   "chip/switch off+delete-surface (DEPRECATED)", "chip-delete border (DEPRECATED)",
                   "on-dark glyph/text (DEPRECATED)"],
        "livesInside": ["Filter bar (chips)"],
        "commonPatterns": ["filter chips"],
        "a11y": ["focus"],
        "anti": [0, 2],
        "usedBy": ("Chip",),
        "audited": ("Chip toggle 1719:84595", "Chip delete 1738:86848"),
        "message": False,
        "listeners": ["click", "keydown"],
        "listeners-note": "click (toggle chips, single-selection chips, the remove button through the filters group) and keydown (the single-selection group's roving keys)",
    },
}
ORDER = ("switch", "checkbox", "radio", "chip")


def slug(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def base_text():
    return subprocess.check_output(["git", "-C", ROOT, "show", "%s:%s" % (BASE, FAMILY)]).decode("utf-8")


def build_member(mid, fam):
    cfg = MEMBERS[mid]
    tree = copy.deepcopy(next(c for c in fam["anatomy"]["children"] if c["part"] == mid))
    machine = {k: tree.pop(k) for k in MACHINE if k in tree}
    states = {"states": machine["$states"], "initial": machine["$initial"]}
    if machine.get("$transitions"):
        states["transitions"] = machine["$transitions"]
    if machine.get("$keys"):
        states["keys"] = machine["$keys"]
    if machine.get("$keys-source"):
        states["$keys-source"] = machine["$keys-source"]
    if machine.get("$sources"):
        states["$sources"] = machine["$sources"]
    states["$moved"] = ("this machine sat on the control's root inside the family tree ($states, $initial, $transitions"
                        + (", $keys" if machine.get("$keys") else "") + "); moved here unchanged by 314-SW, as the "
                        "family's $split note said")
    own = set(fam["bindings"]["$by-member"][mid]) | ({"--error"} if cfg["message"] else set())
    bindings = {k: v for k, v in fam["bindings"].items() if not k.startswith("$") and k in own}
    bindings["$source"] = ("the family's bindings, kept for the variables this control's rules read (the family's "
                           "$by-member list for %s%s, read from the snippet's <style> by 313-L4)"
                           % (mid, ", plus --error for its message line" if cfg["message"] else ""))
    bindings["$left-with-family"] = ("--page (the reference page's own background, demo chrome) and --reverse (in the "
                                     "manifest, read by no rule) are not this control's")
    props = [copy.deepcopy(p) for p in fam["props"] if p["name"] in cfg["props"]]
    for p in props:
        if p["name"] == "label" and mid != "switch":
            p.pop("$wasSwitch", None)   # the old switch's boolean label: a switch fact, kept on the switch only
    tokens = {k: fam["tokens"][k] for k in cfg["tokens"]}
    tokens["$from"] = "the family meta's `tokens` entries that name this control (selection-controls.meta.json), copied verbatim"
    a11y = {k: fam["accessibility"][k] for k in cfg["a11y"]}
    a11y["relatedSC"] = fam["accessibility"]["relatedSC"]
    a11y["$from"] = "the family meta's `accessibility` entries that bear on this control, copied verbatim"
    anti = [fam["antiPatterns"][i] for i in cfg["anti"]]
    tv0 = fam["tokenValidation"]
    du = tv0["depricateUsage"]
    used = lambda row: any(u in row["usedBy"] for u in cfg["usedBy"])
    audited = cfg["audited"] if isinstance(cfg["audited"], tuple) else (cfg["audited"],)
    tv = {"date": tv0["date"], "against": tv0["against"], "result": tv0["result"],
          "depricateUsage": {"tokens": [r for r in du["tokens"] if used(r)],
                             "blockersNoEquivalent": [r for r in du["blockersNoEquivalent"] if used(r)],
                             "auditedNodes": list(audited)},
          "$from": "the family meta's tokenValidation (2026-06-18), sliced to the rows whose usedBy names this control; "
                   "the result line is the family's, verbatim"}
    edges = {"renderedBy": [{"ref": "snippet:" + SNIPPET}],
             "usedInContext": [{"ref": "context:" + slug(t), "$note": t} for t in cfg["livesInside"]],
             "commonPattern": [{"ref": "pattern:" + slug(p)} for p in cfg["commonPatterns"]]}
    variant = next(v for v in fam["variants"] if v["name"] == cfg["variant"])
    ex = {"by": BY, "date": DATE, "reviewed": True,
          "$why": ("s313-D54 (#313, Dave by click, Thu 2026-10-01 23:17 BST, seven-trees-redone page call 7): 'Yes, it "
                   "describes the part' (the recommendation), comment: none, on the four-tree page, which drew this "
                   "control's tree; then " + D56 + " The tree moved here from the family unchanged, so his review stands."),
          "source": "knowledge/snippets/" + SNIPPET,
          "fields": ["anatomy", "states", "emits", "bindings"],
          "$root": "the %s tree, a root of its own (was the family's child of that name, hand-set 313-L4)" % mid,
          "$listeners": cfg["listeners"],
          "$listeners-note": cfg["listeners-note"],
          "$emits-note": fam["$extracted"]["$emits-note"],
          "sha": fam["$extracted"]["sha"],
          "$hand": [h for h in fam["$extracted"]["$hand"]] + [
              {"what": "this control's tree, machine and bindings moved out of the family meta into a meta of its own; "
                       "nothing in the tree renamed, added or removed",
               "why": "s313-D56: 'Four parts (the recommendation)' — 'A client library looks each one up by its own name: "
                      "it asks for a switch, not for the second tree inside selection controls.'"}],
          "$hand-source": fam["$extracted"]["$hand-source"] + " Split: " + D56,
          "$hand-note": fam["$extracted"]["$hand-note"]}
    meta = {"name": cfg["name"], "category": fam["category"], "kind": fam["kind"], "purpose": cfg["purpose"],
            "$memberOf": {"family": "component:selection-controls", "ruling": "s313-D56",
                          "$note": "one of the family's four parts; the family meta keeps the catalogue entry, the "
                                   "reference snippet and the `input` role; this meta holds this control's spec"},
            "props": props,
            "variants": [variant],
            "tokens": tokens,
            "relationships": {"livesInside": cfg["livesInside"], "mustNotNeighbour": [], "commonPatterns": cfg["commonPatterns"]},
            "accessibility": a11y,
            "antiPatterns": anti,
            "tokenValidation": tv,
            "provenance": {"source": "figma", "figma_node": fam["provenance"]["figma_node"], "code_path": "",
                           "$control-node": ("the family canvas node; this control's own audited node(s), as the family's "
                                             "tokenValidation records them: " + ", ".join(audited))},
            "edges": edges,
            "anatomy": tree, "states": states, "emits": [], "bindings": bindings, "$extracted": ex}
    return meta


def family_after(raw, fam):
    i = raw.find('\n  "anatomy":')
    assert i > 0, "family spec block not found"
    head = raw[:i].rstrip()
    assert head.endswith(","), "unexpected text before the spec block"
    split = {"into": ["component:" + m for m in ORDER],
             "ruling": "s313-D56",
             "why": D56,
             "instruction": "s313-D10, the page's recommendation Dave took: '" + D10 + "'",
             "moved": "anatomy, states, emits, bindings and $extracted: each control's tree, machine and bindings now "
                      "live once, on its own meta (switch, checkbox, radio, chip), moved unchanged by 314-SW "
                      "(notes/_lanes/314/SW/split_four.py); the four-tree draft is at " + BASE + ":" + FAMILY,
             "kept": "the catalogue entry (props incl. the control setting, variants, tokens, relationships, accessibility, "
                     "tokenValidation, build, edges), the reference snippet's manifest name, the `input` role "
                     "(knowledge/roles.json) and data-grid's selection-checkbox line",
             "$fence": "extract_spec.py refuses to draft a spec onto a meta carrying $split (the spec lives on the members)"}
    body = json.dumps(split, indent=2, ensure_ascii=False)
    body = "\n".join(("  " + ln if ln else ln) for ln in body.split("\n")).lstrip()
    out = head + "\n" + '  "$split": ' + body + "\n}\n"
    after = json.loads(out)
    for k, v in fam.items():
        if k in SPEC:
            assert k not in after
        else:
            assert after[k] == v, "family field %r changed" % k
    assert raw.startswith(head)
    return out


def main():
    write = "--write" in sys.argv
    raw = base_text()
    fam = json.loads(raw)
    outs = {}
    for mid in ORDER:
        m = build_member(mid, fam)
        outs["knowledge/components/%s.meta.json" % mid] = json.dumps(m, indent=2, ensure_ascii=False) + "\n"
    outs[FAMILY] = family_after(raw, fam)
    for rel, text in outs.items():
        p = os.path.join(ROOT, rel)
        old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        state = "unchanged" if old == text else ("new" if old is None else "changed")
        print("%-48s %6d lines  %s" % (rel, text.count("\n"), state))
        if write and old != text:
            open(p, "w", encoding="utf-8").write(text)
    print("WRITTEN" if write else "(dry run)")


if __name__ == "__main__":
    main()
