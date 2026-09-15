#!/usr/bin/env python3
"""_proof.py — #273 lane WR: enact s273-D4 by TEXTUAL SPAN into knowledge/when-fields.json.

THE PROOF (the `_inscribe_ruling.py` way, R2/A2/A3):
  R2  removing the two inserted spans gives back the ORIGINAL BYTES, `==` on the raw string.
  A3  the result PARSES, and the parsed diff is EXACTLY +13 keys in `fields`
      plus the one `$description` change (append-only: the old string is a PREFIX of the new).

⛔ never json.dump the target file. Two spans only:
   S1 — one appended paragraph inside the `$description` string (before its closing quote).
   S2 — 13 entries inserted into `fields`, after the last existing entry.

Usage: python3 _proof.py            # dry run, prints the proof
       python3 _proof.py --write    # same proof, then writes
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "knowledge", "when-fields.json"))

# ── S1: the registry paragraph, appended to $description (s273-D4, by addition) ──
DESC_ADD = (
    " s273-D4 (Dave, #273) amends that item's \\\"only Dave adds\\\": the list is a REGISTRY, "
    "not a whitelist. A lane MAY ADD a name BY ADDITION \\u2014 one definition sentence and one "
    "example clause (the real one), textual span into `fields`, listed in the lane's report; the "
    "resolver still REFUSES a name that is not defined here, so the #254 typo defence stands; "
    "Dave sees the additions at wrap, not before. Synonym drift is watched by the existing "
    "advisory door `_near_dupes.py` over these definitions \\u2014 no new instrument."
)

# ── S2: the 13 names ruled at #272, defined here under s273-D4 (no gate rewritten) ──
NEW = [
    ("baseline", "where the value axis of the bars starts (`0` = every column is measured from zero, so the bar heights are comparable)", "number", "baseline = 0"),
    ("primaryNavigation", "whether the frame carries primary navigation (`absent` = it deliberately carries none)", "enum", "primaryNavigation = absent"),
    ("breadcrumbs", "whether the frame carries a breadcrumb trail (`absent` = it deliberately carries none)", "enum", "breadcrumbs = absent"),
    ("search", "whether the frame carries a search affordance (`absent` = it deliberately carries none)", "enum", "search = absent"),
    ("exits", "how many deliberate ways out of the frame the person is given", "count", "exits = 1"),
    ("job.count", "how many jobs the frame is asked to hold at once", "count", "job.count = 1"),
    ("entry", "what the person is asked to type into the control (`free text` = words they compose themselves, not a value chosen from a fixed list)", "enum", "entry = free text"),
    ("full", "what a FULL reading of the meter means (`BLOCKED, not done` = the cap is spent and the next action is refused)", "enum", "full = BLOCKED, not done"),
    ("position", "where in a flow the page sits", "enum", "position = end of an instruction"),
    ("order", "the fixed order the page's blocks are read in, where that order is the design argument", "enum", "order = message, then FACTS, then actions, then what-happens-next"),
    ("cause", "what failed (`404` the address is wrong, `500` something failed at our end)", "enum", "cause in (404, 500)"),
    ("steps", "how many ordered steps the task is broken into", "count", "steps >= 2"),
    ("records", "how many already-happened records the reading carries", "count", "records >= 2"),
]

ANCHOR_DESC = ").\",\n  \"$grammar\""          # end of the $description string
ANCHOR_FIELDS = "\"kind\": \"enum\" }\n  }\n}"  # end of the last `fields` entry


def build(original):
    # S1 — append inside the $description string literal
    at1 = original.index(ANCHOR_DESC) + 2   # just after the closing ")." , before the string's quote
    span1 = DESC_ADD
    text = original[:at1] + span1 + original[at1:]

    # S2 — 13 entries after the last existing entry in `fields`
    at2 = text.index(ANCHOR_FIELDS) + len("\"kind\": \"enum\" }")
    lines = []
    for name, defn, kind, ex in NEW:
        lines.append('    %s: { "definition": %s, "kind": %s, "example": %s }' % (
            json.dumps(name, ensure_ascii=False), json.dumps(defn, ensure_ascii=False),
            json.dumps(kind, ensure_ascii=False), json.dumps(ex, ensure_ascii=False)))
    span2 = ",\n" + ",\n".join(lines)
    text = text[:at2] + span2 + text[at2:]
    return text, (at1, span1), (at2, span2)


def main():
    original = open(TARGET, encoding="utf-8").read()
    before = json.loads(original)
    text, (a1, s1), (a2, s2) = build(original)
    assert original[a1 - 1] == "." and original[a1] == '"', "S1 anchor is not the end of $description"

    # R2 — remove BOTH spans, innermost/last first, and demand the original bytes back
    back = text[:a2] + text[a2 + len(s2):]
    back = back[:a1] + back[a1 + len(s1):]
    ok_r2 = back == original
    print("[%s] R2  removing both inserted spans gives back the ORIGINAL BYTES" % ("OK" if ok_r2 else "FAIL"))
    if not ok_r2:
        sys.exit("⛔ REFUSED (not textual) — something outside the two spans moved. The #179 defect.")

    after = json.loads(text)
    print("[OK] A3a the result PARSES")

    added = [k for k in after["fields"] if k not in before["fields"]]
    removed = [k for k in before["fields"] if k not in after["fields"]]
    changed = [k for k in before["fields"] if k in after["fields"] and before["fields"][k] != after["fields"][k]]
    ok_keys = sorted(added) == sorted(n for n, _, _, _ in NEW) and not removed and not changed
    print("[%s] A3b parsed diff in `fields` = EXACTLY +13 keys (%d added, %d removed, %d changed)"
          % ("OK" if ok_keys else "FAIL", len(added), len(removed), len(changed)))

    other = [k for k in set(list(before) + list(after))
             if k != "fields" and before.get(k) != after.get(k)]
    ok_other = other == ["$description"] and after["$description"].startswith(before["$description"])
    print("[%s] A3c the ONLY other change is `$description`, APPEND-ONLY (old string is a prefix): %r"
          % ("OK" if ok_other else "FAIL", other))

    ok_defs = all(after["fields"][n].get("definition") and after["fields"][n].get("example")
                  for n, _, _, _ in NEW)
    print("[%s] A3d every added name carries a definition sentence AND an example clause (s273-D4)"
          % ("OK" if ok_defs else "FAIL"))

    print("  bytes %d -> %d   span1 %d at %d   span2 %d at %d"
          % (len(original), len(text), len(s1), a1, len(s2), a2))

    if not (ok_r2 and ok_keys and ok_other and ok_defs):
        sys.exit("⛔ PROOF FAILED — nothing written.")

    if "--write" in sys.argv:
        with open(TARGET, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("WROTE", TARGET)
    else:
        print("DRY RUN — pass --write to inscribe.")


if __name__ == "__main__":
    main()
