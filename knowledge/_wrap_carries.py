#!/usr/bin/env python3
"""_wrap_carries.py — the carried-items tool of the wrap: COUNT, STRIKE and ROLL `_CARRIES.md`.

Built #306 lane W1 for `s306-D4` phase 1 (Dave, 2026-09-28 16:58 BST, "go on both", to "Build
phases 1 and 2 now: turn the wrap's throwaway scripts into permanent tools"). It replaces the
per-wrap `carries_30N.py` scripts (#303 `carries_304.py`, #304 `carries_305.py`, #305
`carries_306.py`, each "modelled on" the last) and lane T's `notes/_lanes/306/T/carry_strike.py`.

THREE VERBS, and what varies per wrap is ONLY their arguments:

  count   the carried count of one `## residual → #N` section, by the repo's own definition of a
          carry: `_capture_gate._carry_items()` on the `> **residual → #N:**` line (IMPORTED,
          never re-derived). Also prints the `_CARRIES.md` contract's own probe form (first line
          containing `**residual → #N:**`) and refuses if the two disagree. `--at <sha>` reads the
          file at a commit through `git show` (no worktree).
  strike  the `s183-D1` strike form lane T used at #306, BY ADDITION, `s188-D2` receipt in the
          note: `~~` goes round the item's bold title and a ` ⛔ <note>` follows it; the original
          item follows unedited. PROVEN before any write: removing the inserted spans gives back
          the original bytes, and the section's count is unchanged.
  roll    the copy-forward the wrap still does until phase 5 (`s306-D8`) is built: a new section
          `## residual → #M` above `## residual → #N`, NEW items first (one per line of
          `--new FILE`, each must carry `[NEW — 0…]`), then the #N list with EVERY age bracket +1
          (`[NEW — 0…]` → `[1…]`, `[k…]` → `[k+1…]`, the #297–#305 rule). Wording is not touched.

⛔ No item may contain `·` — `_carry_items()` splits on it, so one would silently become two.
Every verb that writes is a DRY RUN unless `--write` is given, and `--file` points it anywhere.

Usage:
  python3 knowledge/_wrap_carries.py count [--section N] [--file _CARRIES.md] [--at SHA] [--json]
  python3 knowledge/_wrap_carries.py strike --section N --title '**① TITLE**' --note TEXT|--note-file F [--write]
  python3 knowledge/_wrap_carries.py roll --from N --to M --new FILE [--write]
  python3 knowledge/_wrap_carries.py --selftest
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CARRIES = "_CARRIES.md"
HEAD_RE = re.compile(r"^## residual → #(\d+)\s*$")
NEW_RE = re.compile(r"\[NEW — 0(,[^\]]*)?\]")


class CarryError(Exception):
    """A named refusal. At the CLI it means: nothing was written."""


def _cg():
    import _capture_gate as cg          # function-level: the gate is a large import
    return cg


def read_text(file=CARRIES, at=None, repo=REPO):
    if at:
        r = subprocess.run(["git", "--no-optional-locks", "show", f"{at}:{file}"], cwd=repo,
                           capture_output=True)
        if r.returncode != 0:
            raise CarryError(f"git show {at}:{file} failed: {r.stderr.decode(errors='replace').strip()[:200]}")
        return r.stdout.decode("utf-8")
    p = file if os.path.isabs(file) else os.path.join(repo, file)
    with open(p, encoding="utf-8") as f:
        return f.read()


def sections(lines):
    """[(N, header_index)] in file order (newest first by contract)."""
    return [(int(m.group(1)), i) for i, ln in enumerate(lines) for m in [HEAD_RE.match(ln)] if m]


def list_line(lines, n):
    """(index, line) of the `> **residual → #n:**` list line inside section n. Refuses if absent."""
    secs = sections(lines)
    hits = [i for s, i in secs if s == n]
    if len(hits) != 1:
        raise CarryError(f"`## residual → #{n}` found {len(hits)} times — exactly one is required")
    start = hits[0]
    end = next((i for s, i in secs if i > start), len(lines))
    pre = f"> **residual → #{n}:**"
    idx = [i for i in range(start, end) if lines[i].startswith(pre)]
    if len(idx) != 1:
        raise CarryError(f"section #{n} has {len(idx)} lines starting `{pre}` — exactly one is required")
    return idx[0], lines[idx[0]]


def count_text(text, n=None):
    """{'section', 'items', 'probe_form', 'struck_marks'} — the gate's own count, cross-checked."""
    lines = text.split("\n")
    if n is None:
        secs = sections(lines)
        if not secs:
            raise CarryError("no `## residual → #N` section in the file")
        n = max(s for s, _ in secs)
    _, line = list_line(lines, n)
    cg = _cg()
    items = len(cg._carry_items(line))
    probe_line = next((l for l in lines if f"**residual → #{n}:**" in l), None)
    probe = len(cg._carry_items(probe_line)) if probe_line is not None else None
    if probe != items:
        raise CarryError(f"the contract's probe form reads {probe} and the section's own line reads "
                         f"{items} for #{n} — two readings of one count; refused, not averaged")
    return {"section": n, "items": items, "probe_form": probe, "segments": line.count("·") + 1,
            "struck_this_line": line.count("~~") // 2}


def strike_text(text, n, title, note):
    """Return (new_text, receipt). The s183-D1 form, by addition, reconstruction-proven."""
    if "·" in note:
        raise CarryError("the note contains `·` — `_carry_items()` would split the item in two")
    if not (title.startswith("**") and title.endswith("**")):
        raise CarryError("the title must be the item's bold title, `**…**`, exactly as written")
    lines = text.split("\n")
    i, line = list_line(lines, n)
    k = line.count(title)
    if k != 1:
        raise CarryError(f"title found {k} times on the #{n} line — exactly one is required")
    a = line.index(title)
    if line[max(0, a - 2):a] == "~~":
        raise CarryError("that title is already struck")
    ins_note = " ⛔ " + note.strip()
    new_line = line[:a] + "~~" + title + "~~" + ins_note + line[a + len(title):]
    back = new_line[:a] + new_line[a + 2:a + 2 + len(title)] + new_line[a + 2 + len(title) + 2 + len(ins_note):]
    if back != line:
        raise CarryError("reconstruction proof FAILED — the strike is not a pure addition")
    lines[i] = new_line
    new = "\n".join(lines)
    c0, c1 = count_text(text, n)["items"], count_text(new, n)["items"]
    if c0 != c1:
        raise CarryError(f"the strike moved the count {c0} → {c1}; a strike keeps the item")
    return new, {"section": n, "inserted_chars": len(new) - len(text), "count": c1,
                 "reconstruction": "PASSED"}


def bump_ages(body):
    """AGES +1 on every bracket; `[NEW — 0…]` becomes `[1…]`. `_capture_gate._AGE_RE`, imported."""
    age = _cg()._AGE_RE
    s = NEW_RE.sub(lambda m: "[\x00" + (m.group(1) or "") + "]", body)
    s = age.sub(lambda m: "[" + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace("[\x00", "[1")


def roll_text(text, n_from, n_to, new_items):
    if n_to <= n_from:
        raise CarryError(f"--to #{n_to} must be later than --from #{n_from}")
    lines = text.split("\n")
    if any(s == n_to for s, _ in sections(lines)):
        raise CarryError(f"`## residual → #{n_to}` already exists — a roll runs once")
    for it in new_items:
        if "·" in it:
            raise CarryError(f"a new item contains `·`: {it[:70]!r}")
        if not NEW_RE.search(it):
            raise CarryError(f"a new item carries no `[NEW — 0…]` bracket: {it[:70]!r}")
    i, line = list_line(lines, n_from)
    body = re.sub(r"^> \*\*residual → #\d+:\*\*", "", line).strip()
    old = bump_ages(body)
    new_line = f"> **residual → #{n_to}:** " + " · ".join(list(new_items) + [old])
    head = next(j for s, j in sections(lines) if s == n_from)
    lines[head:head] = [f"## residual → #{n_to}", "", new_line, ""]
    new = "\n".join(lines)
    before = count_text(text, n_from)["items"]
    after = count_text(new, n_to)["items"]
    return new, {"from": n_from, "to": n_to, "prior_items": before, "items": after,
                 "new": len(new_items), "added_chars": len(new) - len(text)}


def _write(path, text):
    tmp = path + ".w1tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


# ------------------------------------------------------------------------------------ selftest
FIX = """# The carries

## residual → #12

> **residual → #12:** ⬛ **① ALPHA ITEM THAT IS LONG ENOUGH** [NEW — 0, DAVE'S] — body one · ⚠ **② BETA ITEM THAT IS LONG ENOUGH** [3] — body two · ⬛ **③ GAMMA ITEM THAT IS LONG ENOUGH** [1, DAVE'S] — body three

## residual → #11

> **residual → #11:** ⚠ **② BETA ITEM THAT IS LONG ENOUGH** [2] — body two
"""


def selftest():
    ok = True

    def bite(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok = ok and bool(cond)

    c = count_text(FIX)
    bite("count reads the newest section (#12) by default", c["section"] == 12)
    bite("count = _carry_items: the NEW item is not aged, so 2 of 3", c["items"] == 2)
    bite("count of #11 = 1", count_text(FIX, 11)["items"] == 1)
    new, rc = strike_text(FIX, 12, "**② BETA ITEM THAT IS LONG ENOUGH**",
                          "**STRUCK #13 BY ADDITION — RECEIPT `s13-D1`.** The original item follows unedited.")
    bite("strike inserts ~~title~~ and the note", "~~**② BETA ITEM THAT IS LONG ENOUGH**~~ ⛔ **STRUCK #13" in new)
    bite("strike keeps the count (2)", rc["count"] == 2)
    bite("strike changes nothing outside the #12 line",
         [l for l in new.split("\n") if "#11:**" in l] == [l for l in FIX.split("\n") if "#11:**" in l])
    for name, args in [
        ("strike refuses a `·` in the note", (12, "**② BETA ITEM THAT IS LONG ENOUGH**", "a · b")),
        ("strike refuses a title that is not on the line", (12, "**⑨ NOPE**", "x")),
        ("strike refuses a non-bold title", (12, "② BETA ITEM", "x")),
    ]:
        try:
            strike_text(FIX, *args); bite(name, False)
        except CarryError:
            bite(name, True)
    try:
        strike_text(new, 12, "**② BETA ITEM THAT IS LONG ENOUGH**", "again"); bite("strike refuses a double strike", False)
    except CarryError:
        bite("strike refuses a double strike", True)
    rolled, rr = roll_text(FIX, 12, 13, ["⚠ **④ DELTA NEW ITEM LONG ENOUGH** [NEW — 0] — body four"])
    l13 = [l for l in rolled.split("\n") if l.startswith("> **residual → #13:**")][0]
    bite("roll puts the new section above #12", rolled.index("## residual → #13") < rolled.index("## residual → #12"))
    bite("roll: new item first, still [NEW — 0]", l13.startswith("> **residual → #13:** ⚠ **④ DELTA NEW ITEM LONG ENOUGH** [NEW — 0]"))
    bite("roll: [NEW — 0, DAVE'S] → [1, DAVE'S]", "**① ALPHA ITEM THAT IS LONG ENOUGH** [1, DAVE'S]" in l13)
    bite("roll: [3] → [4] and [1, DAVE'S] → [2, DAVE'S]", "[4] — body two" in l13 and "[2, DAVE'S] — body three" in l13)
    bite("roll: count #13 = the three carried, the new one unaged (3)", rr["items"] == 3)
    bite("roll leaves the #12 line byte-identical",
         [l for l in rolled.split("\n") if l.startswith("> **residual → #12:**")] ==
         [l for l in FIX.split("\n") if l.startswith("> **residual → #12:**")])
    for name, a in [("roll refuses a second run", (rolled, 12, 13, [])),
                    ("roll refuses a new item without [NEW — 0]", (FIX, 12, 13, ["⚠ **X ITEM LONG ENOUGH HERE** — b"])),
                    ("roll refuses `·` in a new item", (FIX, 12, 13, ["⚠ **X** [NEW — 0] — a · b"])),
                    ("roll refuses --to not after --from", (FIX, 12, 12, []))]:
        try:
            roll_text(*a); bite(name, False)
        except CarryError:
            bite(name, True)
    two = FIX.replace("## residual → #11\n", "## residual → #11\n\n> **residual → #11:** dup [5] — xxxxxxxxxxxxxxxxxxxxxxxx\n")
    try:
        count_text(two, 11); bite("count refuses two list lines in one section", False)
    except CarryError:
        bite("count refuses two list lines in one section", True)
    # the CLI writes nothing without --write (drive it on a temp copy)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "c.md")
        _write(p, FIX)
        r = subprocess.run([sys.executable, __file__, "roll", "--file", p, "--from", "12", "--to", "13",
                            "--new", "/dev/null"], capture_output=True, text=True)
        bite("CLI roll without --write leaves the file unchanged", r.returncode == 0 and read_text(p) == FIX)
        r = subprocess.run([sys.executable, __file__, "roll", "--file", p, "--from", "12", "--to", "13",
                            "--new", "/dev/null", "--write"], capture_output=True, text=True)
        bite("CLI roll --write writes it", r.returncode == 0 and "## residual → #13" in read_text(p))
    print("wrap-carries selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="verb")
    c = sub.add_parser("count"); c.add_argument("--section", type=int); c.add_argument("--file", default=CARRIES)
    c.add_argument("--at"); c.add_argument("--json", action="store_true")
    s = sub.add_parser("strike"); s.add_argument("--section", type=int, required=True)
    s.add_argument("--title", required=True); s.add_argument("--note"); s.add_argument("--note-file")
    s.add_argument("--file", default=CARRIES); s.add_argument("--write", action="store_true")
    r = sub.add_parser("roll"); r.add_argument("--from", dest="n_from", type=int, required=True)
    r.add_argument("--to", dest="n_to", type=int, required=True); r.add_argument("--new", required=True)
    r.add_argument("--file", default=CARRIES); r.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.verb:
        ap.print_help(); return 2
    try:
        if a.verb == "count":
            res = count_text(read_text(a.file, a.at), a.section)
            res["at"] = a.at or "working tree"
            print(json.dumps(res) if a.json else
                  f"carries #{res['section']} ({res['at']}): {res['items']} items (`_capture_gate._carry_items`, "
                  f"probe form agrees) · {res['segments']} segments on the line")
            return 0
        path = a.file if os.path.isabs(a.file) else os.path.join(REPO, a.file)
        text = read_text(path)
        if a.verb == "strike":
            note = a.note if a.note is not None else (open(a.note_file, encoding="utf-8").read() if a.note_file else None)
            if not note:
                raise CarryError("--note or --note-file is required")
            new, rec = strike_text(text, a.section, a.title, note)
        else:
            items = [l.strip() for l in open(a.new, encoding="utf-8").read().split("\n") if l.strip()]
            new, rec = roll_text(text, a.n_from, a.n_to, items)
        print(("WRITE " if a.write else "DRY-RUN ") + a.verb + " " + json.dumps(rec, ensure_ascii=False))
        if a.write:
            _write(path, new); print("written", path)
        return 0
    except CarryError as e:
        print("⛔ REFUSED:", e); return 1


if __name__ == "__main__":
    sys.exit(main())
