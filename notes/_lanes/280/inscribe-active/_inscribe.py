#!/usr/bin/env python3
"""_inscribe.py — read Dave's 15-base active review and inscribe the rows that are his sentence.

  python3 notes/_lanes/280/inscribe-active/_inscribe.py            # classify + print, touch nothing
  python3 notes/_lanes/280/inscribe-active/_inscribe.py --apply    # edit knowledge/_icon_nodes.json by span
  python3 notes/_lanes/280/inscribe-active/_inscribe.py --selftest # assert the live file, one bite per base

His export is notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json, written by the
sheet lane AR built for the manual review s277-D6 names. Its shape is
`answers: {<base>: {choice, twin, flags[], note}}` — `flags` are the drawings he ticked as "its own
icon, needs an inactive version drawn", `note` is free text in his own words.

THE RULE THIS SCRIPT ENACTS (the #279 wrap's standing instruction): where his flag and his note
disagree, the NOTE is his sentence and the row is ASKED, never guessed. So a row is inscribed only
when flag, note and twin agree (or the note is empty); every other row is left byte-untouched and
goes on the ASK page.

The classification is DERIVED from the note text here, not typed in: the five rows the #279 wrap
already named are ASSERTED to come out ASK, they are not the input.

Edits are textual spans — replacements and insertions on the exact blocks — never a regenerate.

WHEN THIS RAN, a regenerate would have DROPPED Dave's answers: gen_kg_icons.py declared
defaultActive a null and knew nothing of his export. That was this lane's finding F1, and #280
lane IN2 fixed it — the generator now reads his exports and reproduces these edges, its bites
20–22 prove it, and the sentence this script wrote onto each edge saying otherwise was repaired
by `_inscribe2.py --repair-stale`. The selftest below is scoped by his second export where it
exists: the rows he settled on the ASK page are lane IN2's and are asserted landed, not untouched.
"""
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
NODES = REPO / "knowledge" / "_icon_nodes.json"
EXPORT = REPO / "notes" / "_lanes" / "279" / "active-review" / "DAVE-EXPORT-active-2026-09-16.json"
RULING = "s277-D6"

# The rows the #279 wrap named out loud. ASSERTED against the derivation, never used as the input.
WRAP_NAMED_ASK = {"electricity", "employee-banking-solution", "financial-health-check",
                  "reward", "jade-lifestyle"}

WRONG_RX = re.compile(r"(mislabel\w*|wrong label|incorrectly labell?ed|labell?ed wrong)", re.I)
RIGHT_RX = re.compile(r"((?<!in)correctly labell?ed|is correct\b)", re.I)  # "incorrectly" is NOT this
UNSURE_RX = re.compile(r"(not certain|not sure|i think|unsure|maybe|probably)", re.I)


def slugs_in(line, universe):
    """Every candidate/base slug the line names, longest first so -active-2 wins over -active."""
    found, seen = [], line
    for s in sorted(universe, key=len, reverse=True):
        if re.search(r"(?<![A-Za-z0-9-])" + re.escape(s) + r"(?![A-Za-z0-9-])", seen):
            found.append(s)
            seen = seen.replace(s, " " * len(s))
    return set(found)


def classify(answers, cands):
    """-> {base: {"verdict": "INSCRIBE"|"ASK", "why": <plain sentence>, ...}} , derived from his words."""
    out = {}
    for base in sorted(answers):
        a = answers[base]
        note = a.get("note") or ""
        flags = set(a.get("flags") or [])
        twin = a.get("twin")
        universe = set(cands[base]) | {base}
        wrong, right, named = set(), set(), set()
        for line in note.splitlines():
            if not line.strip():
                continue
            hit = slugs_in(line, universe)
            named |= hit
            if WRONG_RX.search(line):
                wrong |= hit
            if RIGHT_RX.search(line):
                right |= hit
        unsure = bool(UNSURE_RX.search(note))
        reasons = []
        if a.get("choice") != "twin" or not twin:
            reasons.append("he did not name a twin on this row")
        if unsure:
            reasons.append("his note says he is not certain")
        if note.strip() and not named:
            reasons.append("his note names no drawing this script can read")
        if wrong and flags and wrong != flags:
            reasons.append("his note names %s and his ticks name %s"
                           % (", ".join(sorted(wrong)) or "nothing", ", ".join(sorted(flags))))
        if wrong and not flags:
            reasons.append("his note names %s as wrongly labelled but he ticked nothing"
                           % ", ".join(sorted(wrong)))
        if flags and not wrong:
            reasons.append("he ticked %s but his note does not say what is wrong with it"
                           % ", ".join(sorted(flags)))
        if twin and twin in wrong:
            reasons.append("his note calls the twin he named (%s) wrongly labelled" % twin)
        if base in wrong:
            reasons.append("his note calls the base itself wrongly labelled")
        if right & flags:
            reasons.append("his note calls %s correctly labelled and his tick calls it its own icon"
                           % ", ".join(sorted(right & flags)))
        out[base] = {"verdict": "ASK" if reasons else "INSCRIBE",
                     "why": "; ".join(reasons), "twin": twin, "flags": sorted(flags),
                     "note": note, "wrong": sorted(wrong), "cands": cands[base]}
    return out


def load():
    pay = json.loads(NODES.read_text(encoding="utf-8"))
    cands = {}
    # the candidate list per base is the ledgers' own note, whichever ledger the row sits in
    for u in list(pay["unresolved"]) + list(pay.get("ruled") or []):
        if u["type"] != "defaultActive":
            continue
        head, _, tail = u["note"].partition(":")
        cands[head.strip()] = [c.strip() for c in tail.split(",") if c.strip()]
    for e in pay["edges"]:
        if e["type"] == "defaultActive":
            head, _, tail = e["$note"].partition(":")
            cands.setdefault(head.strip(), [c.strip() for c in tail.split(",") if c.strip()])
    ex = json.loads(EXPORT.read_text(encoding="utf-8"))
    return pay, ex, cands


def derive():
    pay, ex, cands = load()
    answers = ex["answers"]
    assert len(answers) == 15, "expected 15 answered bases, got %d" % len(answers)
    assert set(answers) == set(cands), "his export and the node file name different bases"
    verdicts = classify(answers, cands)
    ask = {b for b, v in verdicts.items() if v["verdict"] == "ASK"}
    missed = WRAP_NAMED_ASK - ask
    assert not missed, "rows the #279 wrap named as disagreeing came out INSCRIBE: %s" % sorted(missed)
    return pay, ex, cands, verdicts


# ------------------------------------------------------------------ the spans
def edge_block(base, twin, note, at):
    return ('    {\n'
            '      "s": "icon:%s",\n'
            '      "t": "icon:%s",\n'
            '      "type": "defaultActive",\n'
            '      "fam": "assets",\n'
            '      "$note": %s,\n'
            '      "$ruled": %s\n'
            '    },\n'
            % (base, twin, json.dumps(note, ensure_ascii=False),
               json.dumps("Dave named %s the active twin of %s in his own manual review of the "
                          "fifteen bases, exported %s (notes/_lanes/279/active-review/"
                          "DAVE-EXPORT-active-2026-09-16.json) under %s. Inscribed by hand (#280 "
                          "lane IN); gen_kg_icons.py still declares this edge a null, so a "
                          "regenerate would drop his answer."
                          % (twin, base, at, RULING), ensure_ascii=False)))


def null_edge_block(base, note):
    return ('    {\n'
            '      "s": "icon:%s",\n'
            '      "t": null,\n'
            '      "type": "defaultActive",\n'
            '      "fam": "assets",\n'
            '      "$note": %s\n'
            '    },\n' % (base, json.dumps(note, ensure_ascii=False)))


def unresolved_block(base):
    return ('    {\n'
            '      "source": "icon:%s",\n'
            '      "type": "defaultActive",\n' % base)


def apply_edits(text, pay, ex, verdicts):
    at = ex.get("exportedAt") or ex.get("at")
    done = []
    # 1. the edge_types line — it said "never drawn, never resolved", and that stops being true here.
    old = '    "defaultActive": "DECLARED-NULL ONLY — never drawn, never resolved"'
    assert text.count(old) == 1, "edge_types.defaultActive line not found exactly once"
    n_ins = sum(1 for v in verdicts.values() if v["verdict"] == "INSCRIBE")
    n_ask = len(verdicts) - n_ins
    new = ('    "defaultActive": "DRAWN ONLY WHERE DAVE\'S OWN MANUAL REVIEW NAMES THE TWIN '
           '(%s, his export %s): %d of the %d multi-active bases carry a resolved edge with a '
           '$ruled sentence; the other %d stay declared nulls until he answers the questions put '
           'to him on notes/_lanes/280/inscribe-active/ASK-2026-09-16.html. Never inferred."'
           % (RULING, at, n_ins, len(verdicts), n_ask))
    text = text.replace(old, new)

    # 2. the $description — a regenerate would drop his answers, and the file should say so.
    old = ('Regenerate with `gen_kg_icons.py --land --ratified s277-D4`; never hand-edit.')
    assert text.count(old) == 1, "$description sentence not found exactly once"
    text = text.replace(old, old[:-1] + " — EXCEPT the %d defaultActive edges inscribed by hand "
                        "from Dave's own review (#280 lane IN, his export %s): gen_kg_icons.py "
                        "still declares defaultActive a null, so regenerating this file DROPS his "
                        "answers until the generator learns to read his export."
                        % (n_ins, at))

    # 3. per base: the edge, and the declared null it stops being.
    ruled = []
    for base in sorted(verdicts):
        v = verdicts[base]
        if v["verdict"] != "INSCRIBE":
            continue
        note = "%s: %s" % (base, ", ".join(v["cands"]))
        old_edge = null_edge_block(base, note)
        assert text.count(old_edge) == 1, "the declared-null edge for %s is not in the file once" % base
        text = text.replace(old_edge, edge_block(base, v["twin"], note, at))

        head = unresolved_block(base)
        i = text.index(head)
        j = text.index("    },\n", i) + len("    },\n")
        text = text[:i] + text[j:]
        ruled.append({
            "source": "icon:" + base,
            "type": "defaultActive",
            "t": "icon:" + v["twin"],
            "why": "Dave looked at the %d drawings and named %s the active twin. This was a declared "
                   "null under %s; it is one no longer." % (len(v["cands"]), v["twin"], RULING),
            "note": note,
            "his_note": v["note"],
            "his_flags": ["icon:" + f for f in v["flags"]],
            "flagged_as": "drawings he says are their own icon and need an inactive version drawn; "
                          "they are on the mislabelled list in knowledge/_ICON-GAPS.md in his words"
                          if v["flags"] else "",
            "source_of_truth": "notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json (%s)" % at,
        })
        done.append(base)

    # 4. the ruled ledger, inserted beside the unresolved one.
    tail = '  "ratified": "s277-D4"'
    assert text.count(tail) == 1
    blob = json.dumps(ruled, ensure_ascii=False, indent=2)
    blob = "\n".join(("  " + ln) if ln.strip() else ln for ln in blob.splitlines()).lstrip()
    text = text.replace(tail,
                        '  "$ruled": "EVERY declared null this file owned that DAVE HIMSELF has '
                        'since answered, with his own words kept. A row here is no longer in '
                        '`unresolved` and its edge in `edges` carries a resolved `t` and a '
                        '`$ruled` sentence. Rows he has not answered stay in `unresolved`.",\n'
                        '  "ruled": %s,\n%s' % (blob, tail))
    return text, done


GAPS = REPO / "knowledge" / "_ICON-GAPS.md"
GAPS_ANCHOR = "## The `-active` convention (for when these are filled in)"
GAPS_HEAD = "## The drawings Dave says are their own icon (2026-09-16, his review of the 15 multi-active bases)"


def defect_section(verdicts, ex):
    """The exporter-defect list, in his words. Only rows that are his sentence; the asked rows wait."""
    at = ex.get("exportedAt") or ex.get("at")
    rows, asked = [], []
    for b in sorted(verdicts):
        v = verdicts[b]
        if v["verdict"] == "ASK":
            asked.append(b)
            continue
        for f in v["flags"]:
            rows.append((f, b, v["twin"], v["note"].strip()))
    out = [GAPS_HEAD, ""]
    out.append("Dave looked at every base that came out of the export with two or three drawings all "
               "named “… Active” and said, drawing by drawing, which one is the twin and which "
               "is a different icon wearing an active name. A drawing in this table is **not** the "
               "active state of its base: it is its own icon, it needs an inactive version drawn, and "
               "the name it carries came from the exporter's collision counter, not from a designer.")
    out.append("")
    out.append("His export: `notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json` (%s). "
               "The words in the last column are his, verbatim." % at)
    out.append("")
    out.append("| Drawing | Base it was exported under | The twin he named | His words |")
    out.append("|---|---|---|---|")
    for f, b, twin, note in rows:
        out.append("| `%s` | `%s` | `%s` | %s |"
                   % (f, b, twin, note.replace("\n", "<br>").replace("|", "\\|")))
    out.append("")
    out.append("**%d rows of his review are not on this list yet** — %s. On each of those his tick "
               "and his note say different things, or he wrote that he was not certain, so nothing "
               "was written down from them and the question is back with him on "
               "`notes/_lanes/280/inscribe-active/ASK-2026-09-16.html`. The drawings they name join "
               "this table when he answers."
               % (len(asked), ", ".join("`%s`" % a for a in asked)))
    out.append("")
    return "\n".join(out)


def write_defects(verdicts, ex):
    text = GAPS.read_text(encoding="utf-8")
    if GAPS_HEAD in text:
        print("the defect list is already in %s — not written twice" % GAPS.name)
        return
    assert text.count(GAPS_ANCHOR) == 1, "the -active convention heading is not in %s once" % GAPS.name
    text = text.replace(GAPS_ANCHOR, defect_section(verdicts, ex) + "\n" + GAPS_ANCHOR)
    GAPS.write_text(text, encoding="utf-8")
    print("wrote the defect list into %s" % GAPS.relative_to(REPO))


def main():
    args = sys.argv[1:]
    pay, ex, cands, verdicts = derive()
    if "--defects" in args:
        print(defect_section(verdicts, ex))
        if "--apply" in args:
            write_defects(verdicts, ex)
        return 0
    ins = [b for b in sorted(verdicts) if verdicts[b]["verdict"] == "INSCRIBE"]
    ask = [b for b in sorted(verdicts) if verdicts[b]["verdict"] == "ASK"]
    if "--selftest" in args:
        return selftest(verdicts, ins, ask)
    for b in sorted(verdicts):
        v = verdicts[b]
        print("%-8s %-30s twin=%-40s %s" % (v["verdict"], b, v["twin"], v["why"]))
    print("\n%d to inscribe, %d to ask" % (len(ins), len(ask)))
    if "--apply" not in args:
        print("(dry run — nothing written)")
        return 0
    text = NODES.read_text(encoding="utf-8")
    out, done = apply_edits(text, pay, ex, verdicts)
    json.loads(out)  # it must still parse before it is written
    NODES.write_text(out, encoding="utf-8")
    print("inscribed %d bases into %s" % (len(done), NODES.relative_to(REPO)))
    return 0


# ------------------------------------------------------------------ selftest
def selftest(verdicts, ins, ask):
    pay = json.loads(NODES.read_text(encoding="utf-8"))
    ex = json.loads(EXPORT.read_text(encoding="utf-8"))
    at = ex.get("exportedAt") or ex.get("at")
    E = {(e["s"], e["type"]): e for e in pay["edges"]}
    AVO = {(e["s"], e["t"]) for e in pay["edges"] if e["type"] == "activeVariantOf"}
    U = {u["source"] for u in pay["unresolved"] if u["type"] == "defaultActive"}
    R = {r["source"]: r for r in pay.get("ruled", [])}
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

    bite("the classification is his: 15 rows read, %d inscribed, %d asked, and every row the #279 "
         "wrap named as disagreeing is among the asked" % (len(ins), len(ask)),
         lambda: len(verdicts) == 15 and WRAP_NAMED_ASK <= set(ask))

    for b in ins:  # one bite per inscribed base
        v = verdicts[b]
        bite("%s: the default is his twin %s, the variant edge stands, the null is retired, and his "
             "own words are kept" % (b, v["twin"]),
             lambda b=b, v=v: (
                 E[("icon:" + b, "defaultActive")]["t"] == "icon:" + v["twin"]
                 and at in E[("icon:" + b, "defaultActive")]["$ruled"]
                 and v["twin"] in E[("icon:" + b, "defaultActive")]["$ruled"]
                 and ("icon:" + v["twin"], "icon:" + b) in AVO
                 and all(("icon:" + c, "icon:" + b) in AVO for c in v["cands"])
                 and "icon:" + b not in U
                 and R["icon:" + b]["his_note"] == v["note"]
                 and R["icon:" + b]["his_flags"] == ["icon:" + f for f in v["flags"]]))

    # The asked rows were untouched by THIS lane. Lane IN2 then landed the ones he answered on the
    # ASK page, so the assertion is scoped by his own second export when it exists: rows he settled
    # must be ruled, rows he left open must still be byte-untouched nulls.
    ASK_EXPORT = LANE / "DAVE-EXPORT-ask-2026-09-16.json"
    later = {}
    if ASK_EXPORT.exists():
        later = json.loads(ASK_EXPORT.read_text(encoding="utf-8"))["answers"]
    settled = {b for b in ask if (later.get(b) or {}).get("twin")}
    still = [b for b in ask if b not in settled]
    bite("the %d row%s he has not settled are untouched: no default drawn, still declared nulls, "
         "nothing in the ruled ledger%s" % (len(still), "" if len(still) == 1 else "s", (" (and the %d he answered on the ASK page "
         "are ruled, lane IN2)" % len(settled)) if settled else ""),
         lambda: all(E[("icon:" + b, "defaultActive")]["t"] is None
                     and "$ruled" not in E[("icon:" + b, "defaultActive")]
                     and "icon:" + b in U and "icon:" + b not in R for b in still)
         and all(E[("icon:" + b, "defaultActive")]["t"] == "icon:" + later[b]["twin"]
                 and "icon:" + b in R for b in settled))
    bite("the file still parses, the population is unchanged (676 nodes / 1294 edges / 15 defaults) "
         "and no edge type appeared",
         lambda: len(pay["nodes"]) == 676 and len(pay["edges"]) == 1294
         and len([e for e in pay["edges"] if e["type"] == "defaultActive"]) == 15
         and {e["type"] for e in pay["edges"]} == {"inGroup", "usesIcon", "activeVariantOf",
                                                   "defaultActive", "ruledBy"})
    bite("nothing is dropped: every null that left `unresolved` is in `ruled`, and the ledgers "
         "together still carry all 19 rows the file owned",
         lambda: len(pay["unresolved"]) + len(pay["ruled"]) == 19
         and set(R) == {"icon:" + b for b in ins} | {"icon:" + b for b in settled})
    print("SELFTEST %s" % ("PASS" if not fails else "FAIL — " + "; ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
