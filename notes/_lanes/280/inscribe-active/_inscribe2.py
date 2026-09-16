#!/usr/bin/env python3
"""_inscribe2.py — read Dave's answers to the six questions and inscribe the five he settled.

  python3 notes/_lanes/280/inscribe-active/_inscribe2.py            # read + print, touch nothing
  python3 notes/_lanes/280/inscribe-active/_inscribe2.py --apply    # edit knowledge/_icon_nodes.json by span
  python3 notes/_lanes/280/inscribe-active/_inscribe2.py --defects [--apply]
  python3 notes/_lanes/280/inscribe-active/_inscribe2.py --selftest # assert the live file, one bite per base

His export is notes/_lanes/280/inscribe-active/DAVE-EXPORT-ask-2026-09-16.json (20:23Z), written by
the ASK page lane IN built for the six rows where his tick and his note said different things. Same
envelope as the #279 sheet: `answers: {<base>: {choice, twin, flags[], note}}`.

THE RULE, unchanged from lane IN: nothing is guessed. A row is landed only where HIS OWN ANSWER
names a twin. `jade-lifestyle` came back `choice: "open"` with a null twin — so it stays a declared
null, and his note is written onto that null verbatim so the record carries his lean without a
default being invented from it.

`choice` is his answer to the question the ASK page put, and it is carried into the record:
  tick       — the twin he named is the twin, and the drawings he ticked are their own icon
  note       — same, with the wrongly-labelled drawing named in his note rather than ticked
  name-only  — the other drawing is NOT its own icon: it is the right picture under a wrong name
  open       — he has not decided; land nothing

Edits are textual spans on knowledge/_icon_nodes.json — replacements and insertions, never a
regenerate. (gen_kg_icons.py now READS these exports, so a regenerate keeps his answers; that is
lane IN2's second half, and `--selftest` there proves it.)
"""
import json
import re
import sys
from pathlib import Path

import _inscribe  # the lane IN classifier and the span helpers — the same shapes, reused

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
NODES = REPO / "knowledge" / "_icon_nodes.json"
EXPORT = LANE / "DAVE-EXPORT-ask-2026-09-16.json"
EXPORT_REL = "notes/_lanes/280/inscribe-active/DAVE-EXPORT-ask-2026-09-16.json"
RULING = "s277-D6"

# The six rows lane IN asked back. ASSERTED against his export, never used as its input.
ASKED = {"electricity", "employee-banking-solution", "financial-health-check",
         "jade-lifestyle", "reward", "traditional-chinese-medicine"}

# What each `choice` means for the defect list, in plain words. His answer, not a reading of it.
DEFECT_OF = {
    "tick": "its own icon — needs an inactive version drawn",
    "note": "its own icon — needs an inactive version drawn",
    "name-only": "name only — the right drawing under a wrong name, no inactive owed",
}


def load():
    pay = json.loads(NODES.read_text(encoding="utf-8"))
    ex = json.loads(EXPORT.read_text(encoding="utf-8"))
    answers = ex["answers"]
    assert set(answers) == ASKED, "his ASK export answers %s, not the six rows lane IN asked" % sorted(answers)
    cands = {}
    for u in list(pay["unresolved"]) + list(pay.get("ruled") or []):
        if u["type"] != "defaultActive":
            continue
        head, _, tail = u["note"].partition(":")
        cands[head.strip()] = [c.strip() for c in tail.split(",") if c.strip()]
    return pay, ex, cands


def derive(pay, ex, cands):
    """-> (land {base: answer}, open {base: answer}) — split by HIS twin, not by our reading."""
    land, opn = {}, {}
    for base in sorted(ex["answers"]):
        a = ex["answers"][base]
        assert base in cands, "%s is not a declared null in the node file" % base
        (opn if (a.get("twin") is None or a.get("choice") == "open") else land)[base] = a
    for base, a in opn.items():
        assert a.get("choice") == "open" and a.get("twin") is None, \
            "%s has no twin but is not marked open" % base
    for base, a in land.items():
        assert a["twin"] in cands[base], \
            "%s: he named %s, which is not one of its drawings" % (base, a["twin"])
        assert a.get("choice") in DEFECT_OF, "%s: unknown choice %r" % (base, a.get("choice"))
    return land, opn


# ------------------------------------------------------------------ the spans
def ruled_sentence(base, a, at):
    return ("Dave answered the question lane IN put to him on this row and named %s the active twin "
            "of %s; his answer was %r. Exported %s (%s) under %s. Inscribed by hand (#280 lane IN2); "
            "gen_kg_icons.py reads this export, so a regenerate keeps it."
            % (a["twin"], base, a["choice"], at, EXPORT_REL, RULING))


def open_sentence(base, a, at):
    return ("STILL OPEN. Dave was asked which drawing is the twin of %s and answered %r — he named "
            "no twin, so none is drawn and none is inferred. His own words, verbatim, are in "
            "$his_note. Exported %s (%s)." % (base, a["choice"], at, EXPORT_REL))


def open_edge_block(base, note, a, at):
    return ('    {\n'
            '      "s": "icon:%s",\n'
            '      "t": null,\n'
            '      "type": "defaultActive",\n'
            '      "fam": "assets",\n'
            '      "$note": %s,\n'
            '      "$open": %s,\n'
            '      "$his_note": %s\n'
            '    },\n' % (base, json.dumps(note, ensure_ascii=False),
                          json.dumps(open_sentence(base, a, at), ensure_ascii=False),
                          json.dumps(a.get("note") or "", ensure_ascii=False)))


def ruled_row(base, a, cands, at):
    return {
        "source": "icon:" + base,
        "type": "defaultActive",
        "t": "icon:" + a["twin"],
        "why": "Dave looked at the %d drawings and named %s the active twin. This was a declared "
               "null under %s; it is one no longer." % (len(cands[base]), a["twin"], RULING),
        "note": "%s: %s" % (base, ", ".join(cands[base])),
        "his_note": a.get("note") or "",
        "his_flags": ["icon:" + f for f in (a.get("flags") or [])],
        "his_choice": a.get("choice"),
        "flagged_as": ("drawings he says are their own icon and need an inactive version drawn; "
                       "they are on the mislabelled list in knowledge/_ICON-GAPS.md in his words"
                       if a.get("flags") else
                       "he named no drawing as its own icon here: his answer was %r — the other "
                       "drawing is the right picture under a wrong name, and it is on the "
                       "mislabelled list in knowledge/_ICON-GAPS.md in his words" % a.get("choice")),
        "source_of_truth": "%s (%s)" % (EXPORT_REL, at),
    }


def apply_edits(text, pay, ex, cands, land, opn):
    at = ex.get("exportedAt") or ex.get("at")
    n_ruled = len(pay["ruled"]) + len(land)
    n_open = len(opn)

    # 1. edge_types.defaultActive — the count moves, and the reason the rest are null changes.
    old = [ln for ln in text.splitlines() if ln.startswith('    "defaultActive": "DRAWN ONLY')]
    assert len(old) == 1, "edge_types.defaultActive line not found exactly once"
    old = old[0]
    new = ('    "defaultActive": "DRAWN ONLY WHERE DAVE\'S OWN MANUAL REVIEW NAMES THE TWIN '
           '(%s, his two exports %s and %s): %d of the %d multi-active bases carry a resolved edge '
           'with a $ruled sentence; the remaining %d (%s) is still open — he was asked and named no '
           'twin, so the edge stays a declared null and carries his words in $his_note. Never '
           'inferred."'
           % (RULING, "2026-09-16T15:55:41.531Z", at, n_ruled, n_ruled + n_open, n_open,
              ", ".join(sorted(opn))))
    text = text.replace(old, new)

    # 2. $description — the generator learned to read his exports, so say what is true now.
    i = text.index('"$description": "')
    j = text.index('",\n', i)
    desc = ('"$description": "RATIFIED _icon_nodes.json under s277-D4 (#277 lane RI; s269-D1 STEP 4). '
            'Regenerate with `gen_kg_icons.py --land --ratified s277-D4`; never hand-edit — EXCEPT '
            'the %d defaultActive edges inscribed by hand from Dave\'s own review (#280 lanes IN and '
            'IN2, his exports %s and %s). gen_kg_icons.py now READS both exports and reproduces those '
            '%d edges and the `ruled` ledger below, so a regenerate KEEPS his answers; its selftest '
            'proves it. %s is the one row he has not settled and stays a declared null.'
            % (n_ruled, "2026-09-16T15:55:41.531Z", at, n_ruled, ", ".join(sorted(opn))))
    text = text[:i] + desc + text[j:]

    # 3. per base: the null edge becomes his twin; the open one keeps its null and gains his words.
    for base in sorted(land):
        note = "%s: %s" % (base, ", ".join(cands[base]))
        old_edge = _inscribe.null_edge_block(base, note)
        assert text.count(old_edge) == 1, "the declared-null edge for %s is not in the file once" % base
        blk = _inscribe.edge_block(base, land[base]["twin"], note, at)
        blk = blk.replace(json.dumps(
            "Dave named %s the active twin of %s in his own manual review of the fifteen bases, "
            "exported %s (notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json) under "
            "%s. Inscribed by hand (#280 lane IN); gen_kg_icons.py still declares this edge a null, "
            "so a regenerate would drop his answer." % (land[base]["twin"], base, at, RULING),
            ensure_ascii=False),
            json.dumps(ruled_sentence(base, land[base], at), ensure_ascii=False))
        assert "#280 lane IN2" in blk, "the $ruled sentence was not swapped for lane IN2's"
        text = text.replace(old_edge, blk)

        head = _inscribe.unresolved_block(base)
        i = text.index(head)
        j = text.index("    },\n", i) + len("    },\n")
        text = text[:i] + text[j:]

    for base in sorted(opn):
        note = "%s: %s" % (base, ", ".join(cands[base]))
        old_edge = _inscribe.null_edge_block(base, note)
        assert text.count(old_edge) == 1, "the declared-null edge for %s is not in the file once" % base
        text = text.replace(old_edge, open_edge_block(base, note, opn[base], at))
        # and his words onto the ledger row too, so `unresolved` carries them as well
        head = _inscribe.unresolved_block(base)
        i = text.index(head)
        j = text.index("    },\n", i)
        row = text[i:j]
        assert row.rstrip().endswith('"'), "the unresolved row for %s does not end on its note" % base
        row = (row.rstrip("\n") + ',\n      "his_note": %s,\n      "his_answer": %s\n'
               % (json.dumps(opn[base].get("note") or "", ensure_ascii=False),
                  json.dumps(open_sentence(base, opn[base], at), ensure_ascii=False)))
        text = text[:i] + row + text[j:]

    # 4. the ruled ledger — rewritten whole, existing rows kept byte-for-byte in their own fields.
    rows = list(pay["ruled"]) + [ruled_row(b, land[b], cands, at) for b in sorted(land)]
    rows.sort(key=lambda r: r["source"])
    blob = json.dumps(rows, ensure_ascii=False, indent=2)
    blob = "\n".join(("  " + ln) if ln.strip() else ln for ln in blob.splitlines()).lstrip()
    i = text.index('  "ruled": [')
    j = text.index('\n  ],\n', i) + len('\n  ],\n')
    text = text[:i] + '  "ruled": %s,\n' % blob + text[j:]

    # 5. the $ruled header — it now also has to explain the row that came back open.
    old = ('Rows he has not answered stay in `unresolved`.')
    assert text.count(old) == 1
    text = text.replace(old, "Rows he has not answered — and the row he was asked again and left "
                             "open — stay in `unresolved`, where they carry his own words in "
                             "`his_note` and no default.")
    return text


# ------------------------------------------------------------------ the stale sentence
# Lane IN wrote a true sentence onto each of its nine edges: a regenerate would drop his
# answer. Lane IN2 taught gen_kg_icons.py to read his exports, so that sentence is now
# FALSE and a false sentence in the store is worse than none. Replaced verbatim, nine
# spans, nothing else on those edges touched.
STALE = ("gen_kg_icons.py still declares this edge a null, so a regenerate would drop his "
         "answer.")
FRESH = ("gen_kg_icons.py now READS his export (#280 lane IN2), so a regenerate reproduces "
         "this edge instead of dropping it.")


def repair_stale(text):
    n = text.count(STALE)
    assert n == 9, "expected lane IN's nine stale sentences, found %d" % n
    return text.replace(STALE, FRESH)


# ------------------------------------------------------------------ the defect list
GAPS = REPO / "knowledge" / "_ICON-GAPS.md"
GAPS_ANCHOR = "## The `-active` convention (for when these are filled in)"
GAPS_HEAD = ("## The six he was asked again (2026-09-16, his answers to the ASK page)")
GAPS_STALE = "**6 rows of his review are not on this list yet**"


def defects_of(base, a, cands):
    """The defect rows his answer carries, DERIVED from his own words line by line.

    A line of his note that calls something wrongly labelled and NAMES a drawing is a defect on
    that drawing; the same line naming NO drawing is a defect on the pair the question was about
    (the base and the twin he named). Every drawing he TICKED is its own icon whether or not a
    line of the note says so. Ticked -> needs an inactive drawn; named but not ticked -> the name
    is the whole defect.
    """
    universe = set(cands[base]) | {base}
    flags = list(a.get("flags") or [])
    rows, seen = [], set()

    def add(drawing, kind):
        if drawing in seen:
            return
        seen.add(drawing)
        rows.append((drawing, kind))

    for d in flags:
        add(d, DEFECT_OF["tick"])
    for line in (a.get("note") or "").splitlines():
        if not line.strip() or not _inscribe.WRONG_RX.search(line):
            continue
        named = _inscribe.slugs_in(line, universe)
        if named:
            for d in sorted(named):
                add(d, DEFECT_OF["tick"] if d in flags else DEFECT_OF["name-only"])
        else:
            add("%s + %s" % (base, a["twin"]),
                "name only — he calls this the correct twin pairing and says it is mislabelled, so "
                "the pair is a picture of something else wearing this name")
    return rows


def defect_section(ex, land, opn, cands):
    at = ex.get("exportedAt") or ex.get("at")
    out = [GAPS_HEAD, ""]
    out.append("On six of the fifteen bases his tick and his note said different things, so lane IN "
               "wrote down nothing and put one question per row to him. These are his answers. Five "
               "rows are settled and their drawings are below; `%s` came back open — he named no "
               "twin, nothing was written down, and his own lean is quoted under the table."
               % ", ".join(sorted(opn)))
    out.append("")
    out.append("His export: `%s` (%s). The words in the last column are his, verbatim — the typo in "
               "the last row is his too." % (EXPORT_REL, at))
    out.append("")
    out.append("| Drawing | Base it was exported under | The twin he named | What is wrong with it | "
               "His words |")
    out.append("|---|---|---|---|---|")
    for base in sorted(land):
        a = land[base]
        note = (a.get("note") or "").strip().replace("\n", "<br>").replace("|", "\\|")
        for drawing, kind in defects_of(base, a, cands):
            out.append("| %s | `%s` | `%s` | %s | %s |"
                       % (" + ".join("`%s`" % d for d in drawing.split(" + ")),
                          base, a["twin"], kind, note))
    out.append("")
    for base in sorted(opn):
        out.append("**`%s` is still open.** He was asked and did not choose. His words, verbatim: "
                   "*“%s”*. Nothing is written down from that — no twin, no drawing on this list — "
                   "and the base keeps its declared null in `knowledge/_icon_nodes.json`."
                   % (base, (opn[base].get("note") or "").strip()))
    out.append("")
    return "\n".join(out)


def write_defects(ex, land, opn, cands):
    text = GAPS.read_text(encoding="utf-8")
    if GAPS_HEAD in text:
        print("the second-pass defect list is already in %s — not written twice" % GAPS.name)
        return
    assert text.count(GAPS_ANCHOR) == 1, "the -active convention heading is not in %s once" % GAPS.name
    # the stale paragraph lane IN left ("6 rows … not on this list yet") is now answered
    i = text.index(GAPS_STALE)
    j = text.index("\n", i)
    text = (text[:i] + "**Five of those six rows are now answered** — the answers, and the one row "
            "he left open, are in the next section." + text[j:])
    text = text.replace(GAPS_ANCHOR, defect_section(ex, land, opn, cands) + "\n" + GAPS_ANCHOR)
    GAPS.write_text(text, encoding="utf-8")
    print("wrote the second-pass defect list into %s" % GAPS.relative_to(REPO))


# ------------------------------------------------------------------ selftest
def selftest(ex, cands, land, opn):
    pay = json.loads(NODES.read_text(encoding="utf-8"))
    at = ex.get("exportedAt") or ex.get("at")
    E = {(e["s"], e["type"]): e for e in pay["edges"]}
    AVO = {(e["s"], e["t"]) for e in pay["edges"] if e["type"] == "activeVariantOf"}
    U = {u["source"]: u for u in pay["unresolved"] if u["type"] == "defaultActive"}
    R = {r["source"]: r for r in pay.get("ruled", [])}
    gaps = GAPS.read_text(encoding="utf-8")
    fails = []

    def bite(name, ok):
        try:
            good = bool(ok())
        except Exception as exc:
            good = False
            name += "  [%s: %s]" % (type(exc).__name__, exc)
        print("  %s  %s" % ("ok   " if good else "FAIL ", name))
        if not good:
            fails.append(name)

    bite("the answers are his: the six rows lane IN asked are the six he answered, %d name a twin "
         "and %d came back open" % (len(land), len(opn)),
         lambda: set(ex["answers"]) == ASKED and len(land) == 5 and len(opn) == 1)

    for base in sorted(land):  # one bite per base he settled
        a = land[base]
        bite("%s: the default is his twin %s, the variant edge stands, the null is retired, his own "
             "words and his answer %r are kept, and his drawings are on the list in his words"
             % (base, a["twin"], a["choice"]),
             lambda base=base, a=a: (
                 E[("icon:" + base, "defaultActive")]["t"] == "icon:" + a["twin"]
                 and at in E[("icon:" + base, "defaultActive")]["$ruled"]
                 and a["twin"] in E[("icon:" + base, "defaultActive")]["$ruled"]
                 and ("icon:" + a["twin"], "icon:" + base) in AVO
                 and all(("icon:" + c, "icon:" + base) in AVO for c in cands[base])
                 and "icon:" + base not in U
                 and R["icon:" + base]["his_note"] == (a.get("note") or "")
                 and R["icon:" + base]["his_choice"] == a["choice"]
                 and R["icon:" + base]["his_flags"] == ["icon:" + f for f in (a.get("flags") or [])]
                 and (a.get("note") or "").strip().splitlines()[0] in gaps))

    for base in sorted(opn):  # and one for the row he left open
        a = opn[base]
        bite("%s is still open: no default is drawn, it is still a declared null in both ledgers, "
             "his note is on the null verbatim, and no drawing of his went on the defect list"
             % base,
             lambda base=base, a=a: (
                 E[("icon:" + base, "defaultActive")]["t"] is None
                 and "$ruled" not in E[("icon:" + base, "defaultActive")]
                 and E[("icon:" + base, "defaultActive")]["$his_note"] == (a.get("note") or "")
                 and "icon:" + base in U and U["icon:" + base]["his_note"] == (a.get("note") or "")
                 and "icon:" + base not in R
                 and (a.get("note") or "").strip() in gaps
                 and "| `%s-active" % base not in gaps))

    bite("the file still parses, the population is unchanged (676 nodes / 1294 edges / 15 defaults) "
         "and no edge type appeared",
         lambda: len(pay["nodes"]) == 676 and len(pay["edges"]) == 1294
         and len([e for e in pay["edges"] if e["type"] == "defaultActive"]) == 15
         and {e["type"] for e in pay["edges"]} == {"inGroup", "usesIcon", "activeVariantOf",
                                                   "defaultActive", "ruledBy"})
    bite("nothing is dropped: 14 of the 15 bases are ruled, 1 is unresolved, and the two ledgers "
         "together still carry all 19 rows the file owned",
         lambda: len(pay["unresolved"]) + len(pay["ruled"]) == 19
         and len([r for r in pay["ruled"] if r["type"] == "defaultActive"]) == 14
         and len(U) == 1)
    bite("no edge in the file still claims a regenerate would drop his answer: the generator "
         "reads his exports now, and every ruled edge says so",
         lambda: "would drop his answer" not in NODES.read_text(encoding="utf-8")
         and all("regenerate" in e.get("$ruled", "") for e in pay["edges"]
                 if e["type"] == "defaultActive" and e["t"]))

    bite("every ruled row carries his own words and the export they came from, and no row carries a "
         "twin he did not name",
         lambda: all(r.get("his_note") is not None and "DAVE-EXPORT" in r["source_of_truth"]
                     for r in pay["ruled"]))
    print("SELFTEST %s" % ("PASS" if not fails else "FAIL — " + "; ".join(fails)))
    return 1 if fails else 0


def main():
    args = sys.argv[1:]
    pay, ex, cands = load()
    land, opn = derive(pay, ex, cands)
    if "--selftest" in args:
        return selftest(ex, cands, land, opn)
    if "--repair-stale" in args:
        out = repair_stale(NODES.read_text(encoding="utf-8"))
        json.loads(out)
        NODES.write_text(out, encoding="utf-8")
        print("repaired lane IN's nine now-false sentences in %s" % NODES.relative_to(REPO))
        return 0
    if "--defects" in args:
        print(defect_section(ex, land, opn, cands))
        if "--apply" in args:
            write_defects(ex, land, opn, cands)
        return 0
    for b in sorted(ex["answers"]):
        a = ex["answers"][b]
        print("%-6s %-32s twin=%-42s flags=%s"
              % ("LAND" if b in land else "OPEN", b, a["twin"], ",".join(a.get("flags") or []) or "-"))
    print("\n%d to land, %d left open" % (len(land), len(opn)))
    if "--apply" not in args:
        print("(dry run — nothing written)")
        return 0
    text = NODES.read_text(encoding="utf-8")
    out = apply_edits(text, pay, ex, cands, land, opn)
    json.loads(out)
    NODES.write_text(out, encoding="utf-8")
    print("landed %d bases into %s" % (len(land), NODES.relative_to(REPO)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
