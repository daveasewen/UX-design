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

★ PHASE 5 (`s306-D8`, #312 lane E-build, 2026-10-01, by addition; design `notes/_lanes/312/E/DESIGN.md` § 6):
  delta   APPEND one small block for `## residual → #M (delta from #N)` — the base (the last FULL line at or
          before N), the new items, the struck titles with receipts — instead of a whole copied line with
          every age +1. `--new FILE` and `--struck FILE` (one `**TITLE** — VERDICT — receipt` per line) or
          `--block FILE` (a block `_wrap_views.py` already wrote). Growth per wrap ≤ 20,000 B (limit 10).
  render  MATERIALISE the full line for section M: the newest FULL line at or before M, then every delta
          block after it in order (ages +1 per wrap, strikes as `~~title~~ ⛔ note` in place with the
          `s183-D1` form, new items first). Prints it, or `--write` puts it in the gitignored
          `knowledge/_tmp/carries-<M>.md` — never committed. `count --section M` reads the rendered line
          when M is a delta section, so the count stays the gate's own `_carry_items`.
  rebase  Commit a new FULL line for M (`render` written INTO `_CARRIES.md` as `## residual → #M`, above the
          delta block it replaces) so a render never replays more than twenty deltas (PICKED, not ruled).
  The RECONSTRUCTION PROOF (`s183-D1`): rendering the deltas and diffing against a hand-written full line
  must agree byte for byte — `render --prove-against N` does that for a section that has both.

  ⚠ THE `[NEW — 0]` COUNT DEFECT, fixed here and declared: `_capture_gate._AGE_RE` is
  `\[(\d+)(?:\s*[,—-][^\]]*)?\]`; its docstring says `[NEW — 0]` "is stripped to 0", but the bracket starts
  with `NEW`, so it never matches and NEW items are NOT counted — hence every banner's "(which count from
  #N+2)". This file carries its own `AGE_RE` with the one alternation that fixes it, uses it for `bump_ages`
  (NEW_RE runs first, so the roll is unchanged) and for `count --with-new`; `count` says which regex it
  counted with. The one-line change to `_capture_gate.py` is NOT this file's path (reported under
  Found-not-fixed by lane E-build); until it lands, the gate's count stays low by the new items.
  ⚠ AND THE GATE: `_capture_gate._resolve_residual_pointer` looks for the `**residual → #M:**` line INSIDE
  `_CARRIES.md`; a delta section has none, so until that resolver calls `resolve_line()` here (one call), a
  wrap that writes ONLY a delta block fails the 2c carry gate. The runbook says which path the wrap takes.

Usage:
  python3 knowledge/_wrap_carries.py count [--section N] [--file _CARRIES.md] [--at SHA] [--json]
  python3 knowledge/_wrap_carries.py strike --section N --title '**① TITLE**' --note TEXT|--note-file F [--write]
  python3 knowledge/_wrap_carries.py roll --from N --to M --new FILE [--write]
  python3 knowledge/_wrap_carries.py delta --from N --to M (--new FILE [--struck FILE] --date D | --block FILE) [--write]
  python3 knowledge/_wrap_carries.py render --section M [--write] [--prove-against N] [--file F]
  python3 knowledge/_wrap_carries.py rebase --section M [--write]
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
DELTA_HEAD_RE = re.compile(r"^## residual → #(\d+) \(delta from #(\d+)\)\s*$")
AGE_RE = re.compile(r"\[(?:NEW\s*[—-]\s*)?(\d+)(?:\s*[,—-][^\]]*)?\]")   # the gate's _AGE_RE + the NEW alternation
RENDERED_DIR = os.path.join("knowledge", "_tmp")
REBASE_EVERY = 20                 # PICKED: a render replays at most this many deltas before a FULL line is committed


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
        secs = [s for s, _ in sections(lines)] + [t for t, _, _ in delta_sections(lines)]
        if not secs:
            raise CarryError("no `## residual → #N` section in the file")
        n = max(secs)
    rendered = not any(s == n for s, _ in sections(lines))
    if rendered:
        line, replayed = render_text(text, n)
    else:
        _, line = list_line(lines, n)
    cg = _cg()
    items = len(cg._carry_items(line))
    probe_line = line if rendered else next((l for l in lines if f"**residual → #{n}:**" in l), None)
    probe = len(cg._carry_items(probe_line)) if probe_line is not None else None
    if probe != items:
        raise CarryError(f"the contract's probe form reads {probe} and the section's own line reads "
                         f"{items} for #{n} — two readings of one count; refused, not averaged")
    with_new = len([s for s in re.sub(r"^> \*\*residual → #\d+:\*\*", "", line).split("·") if AGE_RE.search(s) and len(cg._carry_norm(s)) >= 20])
    return {"section": n, "items": items, "probe_form": probe, "segments": line.count("·") + 1,
            "struck_this_line": line.count("~~") // 2, "items_with_new": with_new,
            "counted_with": "_capture_gate._AGE_RE (NEW items not counted until its alternation lands); items_with_new = this file's AGE_RE",
            "rendered": rendered}


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
    """AGES +1 on every bracket; `[NEW — 0…]` becomes `[1…]`. The gate's `_AGE_RE` shape, with the NEW
    alternation (`AGE_RE` here); NEW_RE runs first so the result is the same the gate's regex gave."""
    age = AGE_RE
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


# ------------------------------------------------------------------------------------ phase 5: delta / render / rebase
def delta_block(n_to, n_from, new_items, struck, date, count=None):
    """The block a wrap APPENDS (s306-D8). `struck` = [(title, verdict, receipt)]; `date` = the ritual date the
    strike notes carry (`STRUCK #<n_from> <date> BY THE WRAP SEAT …`)."""
    for it in new_items:
        if "·" in it:
            raise CarryError(f"a new item contains `·`: {it[:70]!r}")
        if not NEW_RE.search(it):
            raise CarryError(f"a new item carries no `[NEW — 0…]` bracket: {it[:70]!r}")
    for t, v, r in struck:
        if "·" in r or "·" in t:
            raise CarryError(f"a strike contains `·`: {t[:50]!r}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date or ""):
        raise CarryError("delta_block needs the ritual date, YYYY-MM-DD")
    L = [f"## residual → #{n_to} (delta from #{n_from})", "",
         f"> **base:** `residual → #{n_from}` (the last FULL line at or before #{n_from}; every item on it is one wrap older here)",
         f"> **wrap:** #{n_from} on {date} (the strike notes read `STRUCK #{n_from} {date} BY THE WRAP SEAT`)",
         f"> **new → #{n_to}:** " + (" · ".join(new_items) if new_items else "none"),
         f"> **struck → #{n_to}:** " + (" · ".join(f"**{t}** — {v} — {r}" for t, v, r in struck) if struck else "none"),
         f"> **count → #{n_to}:** " + (f"{count} " if count is not None else "") + f"(PROBE `python3 knowledge/_wrap_carries.py count --section {n_to}`; rendered by `render --section {n_to}`)", ""]
    return "\n".join(L) + "\n"


def delta_sections(lines):
    """[(M, N, header_index)] of every delta block, file order."""
    return [(int(m.group(1)), int(m.group(2)), i) for i, ln in enumerate(lines) for m in [DELTA_HEAD_RE.match(ln)] if m]


def parse_delta(lines, start):
    """The new items and strikes of the delta block whose header is at `start`."""
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    body = lines[start:end]
    def line(prefix):
        hits = [l for l in body if l.startswith(prefix)]
        if len(hits) != 1:
            raise CarryError(f"delta block at line {start + 1}: {len(hits)} lines start `{prefix}` — exactly one is required")
        return hits[0][len(prefix):].strip()
    m = DELTA_HEAD_RE.match(lines[start])
    n_to = int(m.group(1))
    wm = re.match(r"#(\d+) on (\d{4}-\d{2}-\d{2})", line("> **wrap:**"))
    if not wm or int(wm.group(1)) != int(m.group(2)):
        raise CarryError(f"delta block at line {start + 1}: the `> **wrap:**` line must read `#{m.group(2)} on YYYY-MM-DD`")
    date = wm.group(2)
    new = line(f"> **new → #{n_to}:**")
    struck = line(f"> **struck → #{n_to}:**")
    new_items = [] if new == "none" else [x.strip() for x in new.split(" · ") if x.strip()]
    strikes = []
    if struck != "none":
        for seg in struck.split(" · "):
            mm = re.match(r"\*\*(.+?)\*\*\s*—\s*([A-Z ]+?)\s*—\s*(.*)$", seg.strip(), re.S)
            if not mm:
                raise CarryError(f"a struck entry is `**TITLE** — VERDICT — receipt`: {seg[:60]!r}")
            strikes.append((mm.group(1).strip(), mm.group(2).strip(), mm.group(3).strip()))
    return n_to, int(m.group(2)), new_items, strikes, end, date


def _apply_delta(line, n_to, n_from, date, new_items, strikes):
    """One wrap forward: ages +1, strikes in place (the s183-D1 form, `STRUCK #<n_from> <date>`), new items first."""
    body = re.sub(r"^> \*\*residual → #\d+:\*\*", "", line).strip()
    body = bump_ages(body)
    for t, v, r in strikes:
        title = f"**{t}**"
        k = body.count(title)
        if k != 1:
            raise CarryError(f"render: struck title found {k} times on the line (exactly one is required): {t[:60]!r}")
        a = body.index(title)
        if body[max(0, a - 2):a] == "~~":
            raise CarryError(f"render: `{t[:40]}` is already struck")
        note = f" ⛔ **STRUCK #{n_from} {date} BY THE WRAP SEAT (`s183-D1` strike form, `s188-D2` receipt) — {v}.** {r}"
        body = body[:a] + "~~" + title + "~~" + note + body[a + len(title):]
    return f"> **residual → #{n_to}:** " + " · ".join(list(new_items) + ([body] if body else []))


def resolve_line(text, m):
    """The FULL `> **residual → #m:**` line for section m: as written when m is a FULL section, else rendered
    from the newest FULL line at or before m and every delta after it. Returns (line, replayed_deltas)."""
    lines = text.split("\n")
    full = {s: i for s, i in sections(lines)}
    if m in full:
        return list_line(lines, m)[1], 0
    deltas = {t: (f, i) for t, f, i in delta_sections(lines)}
    if m not in deltas:
        raise CarryError(f"no `## residual → #{m}` section, FULL or delta, in the file")
    chain = []
    cur = m
    while cur not in full:
        if cur not in deltas:
            raise CarryError(f"render #{m}: the chain breaks at #{cur} — no FULL line and no delta block for it")
        f, i = deltas[cur]
        chain.append((cur, i))
        if f >= cur:
            raise CarryError(f"delta #{cur} names a base #{f} that is not earlier")
        cur = f
    line = list_line(lines, cur)[1]
    for t, i in reversed(chain):
        n_to, n_from, new_items, strikes, _, date = parse_delta(lines, i)
        line = _apply_delta(line, n_to, n_from, date, new_items, strikes)
    return line, len(chain)


def render_text(text, m):
    line, replayed = resolve_line(text, m)
    if replayed > REBASE_EVERY:
        raise CarryError(f"render #{m} replays {replayed} deltas, over {REBASE_EVERY}: run `rebase --section {m} --write` first")
    return line, replayed


def delta_append(text, n_from, n_to, new_items, strikes, date=None, block=None):
    lines = text.split("\n")
    if any(s == n_to for s, _ in sections(lines)) or any(t == n_to for t, _, _ in delta_sections(lines)):
        raise CarryError(f"`## residual → #{n_to}` already exists — a delta runs once")
    try:
        resolve_line(text, n_from)
    except CarryError as e:
        raise CarryError(f"the base #{n_from} cannot be resolved: {e}")
    blk = block if block is not None else delta_block(n_to, n_from, new_items, strikes, date)
    if block is not None:
        m = DELTA_HEAD_RE.match(blk.split("\n")[0])
        if not m or int(m.group(1)) != n_to or int(m.group(2)) != n_from:
            raise CarryError(f"--block's header is not `## residual → #{n_to} (delta from #{n_from})`")
    if len(blk.encode("utf-8")) > 20000:
        raise CarryError(f"the delta block is {len(blk.encode('utf-8')):,} B, over the 20,000 B a wrap (limit 10)")
    # the block goes at the TOP (newest first, as the FULL sections are ordered)
    first = min([i for _, i in sections(lines)] + [i for _, _, i in delta_sections(lines)])
    new = "\n".join(lines[:first] + blk.rstrip("\n").split("\n") + [""] + lines[first:])
    line, replayed = render_text(new, n_to)
    cg = _cg()
    items = len(cg._carry_items(line))
    with_new = len([s for s in line.split("·") if AGE_RE.search(s)])
    return new, {"from": n_from, "to": n_to, "block_bytes": len(blk.encode("utf-8")), "added_chars": len(new) - len(text),
                 "rendered_items": items, "rendered_items_with_new": with_new, "replayed_deltas": replayed}


def rebase_text(text, m):
    """Write the rendered line for m INTO the file as a FULL `## residual → #m` section above its delta block."""
    lines = text.split("\n")
    if any(s == m for s, _ in sections(lines)):
        raise CarryError(f"#{m} is already a FULL section")
    line, replayed = resolve_line(text, m)
    d = [i for t, _, i in delta_sections(lines) if t == m]
    if len(d) != 1:
        raise CarryError(f"#{m} has {len(d)} delta blocks; exactly one")
    i = d[0]
    lines[i:i] = [f"## residual → #{m}", "", line, "", f"> *(rebased at #{m}: the FULL line above replays {replayed} delta block(s); the delta blocks below are history)*", ""]
    return "\n".join(lines), {"section": m, "replayed": replayed, "items": len(_cg()._carry_items(line))}


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
    # ★ phase 5: delta / render / rebase, and the AGE_RE fix
    bite("AGE_RE counts `[NEW — 0]` (the gate's _AGE_RE does not; the defect, declared)",
         AGE_RE.search("[NEW — 0, DAVE'S]") and AGE_RE.search("[NEW — 0, DAVE'S]").group(1) == "0" and not _cg()._AGE_RE.search("[NEW — 0]"))
    c12 = count_text(FIX, 12)
    bite("count reports items (gate regex, 2) and items_with_new (this file's, 3)", c12["items"] == 2 and c12["items_with_new"] == 3 and not c12["rendered"])
    blk = delta_block(13, 12, ["⚠ **④ DELTA NEW ITEM LONG ENOUGH** [NEW — 0] — body four"],
                      [("② BETA ITEM THAT IS LONG ENOUGH", "ANSWERED", "His line, `s13-D1`.")], "2026-01-02")
    bite("delta_block: header, base, wrap, new, struck, count lines", blk.startswith("## residual → #13 (delta from #12)\n") and "> **wrap:** #12 on 2026-01-02" in blk
         and "> **struck → #13:** **② BETA" in blk)
    dt, rec = delta_append(FIX, 12, 13, [], [], block=blk)
    bite("delta appends the block ABOVE the FULL sections (newest first) and renders 3 items", dt.index("## residual → #13 (delta") < dt.index("## residual → #12") and rec["rendered_items"] == 3)
    line, replayed = render_text(dt, 13)
    expect = ("> **residual → #13:** ⚠ **④ DELTA NEW ITEM LONG ENOUGH** [NEW — 0] — body four · ⬛ **① ALPHA ITEM THAT IS LONG ENOUGH** [1, DAVE'S] — body one · "
              "⚠ ~~**② BETA ITEM THAT IS LONG ENOUGH**~~ ⛔ **STRUCK #12 2026-01-02 BY THE WRAP SEAT (`s183-D1` strike form, `s188-D2` receipt) — ANSWERED.** His line, `s13-D1`. [4] — body two · "
              "⬛ **③ GAMMA ITEM THAT IS LONG ENOUGH** [2, DAVE'S] — body three")
    bite("render: new first, ages +1, the strike in place in the s183-D1 form (byte-exact)", line == expect and replayed == 1)
    bite("render = roll + strike (the two paths agree byte for byte)",
         line == strike_text(roll_text(FIX, 12, 13, ["⚠ **④ DELTA NEW ITEM LONG ENOUGH** [NEW — 0] — body four"])[0], 13, "**② BETA ITEM THAT IS LONG ENOUGH**",
                             "**STRUCK #12 2026-01-02 BY THE WRAP SEAT (`s183-D1` strike form, `s188-D2` receipt) — ANSWERED.** His line, `s13-D1`.")[0].split("\n")[4])
    bite("count --section 13 on a delta section reads the RENDERED line (3)", count_text(dt, 13)["items"] == 3 and count_text(dt, 13)["rendered"])
    dt2, _ = delta_append(dt, 13, 14, [], [], block=delta_block(14, 13, [], [], "2026-01-03"))
    bite("a second delta chains on the first (render #14 replays 2, ages +1 again)", render_text(dt2, 14)[1] == 2 and "[5] — body two" in render_text(dt2, 14)[0])
    rb, rrec = rebase_text(dt2, 14)
    bite("rebase writes a FULL `## residual → #14` line above its delta block; render then replays 0", rrec["replayed"] == 2 and render_text(rb, 14)[1] == 0
         and render_text(rb, 14)[0] == render_text(dt2, 14)[0])
    for name, fn in [("delta refuses a second delta for the same section", lambda: delta_append(dt, 12, 13, [], [], block=blk)),
                     ("delta refuses a base that cannot be resolved", lambda: delta_append(FIX, 9, 13, [], [], block=delta_block(13, 9, [], [], "2026-01-02"))),
                     ("delta refuses a block whose header names another pair", lambda: delta_append(FIX, 12, 13, [], [], block=delta_block(13, 11, [], [], "2026-01-02"))),
                     ("delta refuses a new item without [NEW — 0]", lambda: delta_block(13, 12, ["⚠ **X ITEM** — b"], [], "2026-01-02")),
                     ("delta refuses `·` in a receipt", lambda: delta_block(13, 12, [], [("② BETA ITEM THAT IS LONG ENOUGH", "ANSWERED", "a · b")], "2026-01-02")),
                     ("delta refuses a missing date", lambda: delta_block(13, 12, [], [], None)),
                     ("render refuses a strike whose title is not on the line", lambda: render_text(delta_append(FIX, 12, 13, [], [], block=delta_block(13, 12, [], [("⑨ NOPE", "DROPPED", "x")], "2026-01-02"))[0], 13)),
                     ("render refuses an unknown section", lambda: render_text(FIX, 99))]:
        try:
            fn(); bite(name, False)
        except CarryError:
            bite(name, True)
    big = delta_block(13, 12, ["⚠ **⑤ BIG ITEM LONG ENOUGH** [NEW — 0] — " + "x" * 20000], [], "2026-01-02")
    try:
        delta_append(FIX, 12, 13, [], [], block=big); bite("delta refuses a block over 20,000 B (limit 10)", False)
    except CarryError:
        bite("delta refuses a block over 20,000 B (limit 10)", True)
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
    dl = sub.add_parser("delta"); dl.add_argument("--from", dest="n_from", type=int, required=True)
    dl.add_argument("--to", dest="n_to", type=int, required=True); dl.add_argument("--new"); dl.add_argument("--struck")
    dl.add_argument("--block"); dl.add_argument("--date", help="the ritual date, YYYY-MM-DD (with --new)")
    dl.add_argument("--file", default=CARRIES); dl.add_argument("--write", action="store_true")
    rn = sub.add_parser("render"); rn.add_argument("--section", type=int, required=True); rn.add_argument("--file", default=CARRIES)
    rn.add_argument("--write", action="store_true"); rn.add_argument("--prove-against", type=int)
    rb = sub.add_parser("rebase"); rb.add_argument("--section", type=int, required=True); rb.add_argument("--file", default=CARRIES)
    rb.add_argument("--write", action="store_true")
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
                  f"carries #{res['section']} ({res['at']}{', rendered from deltas' if res['rendered'] else ''}): {res['items']} items "
                  f"(`_capture_gate._carry_items`, probe form agrees; {res['items_with_new']} counting the NEW items with this file's AGE_RE) "
                  f"· {res['segments']} segments on the line")
            return 0
        if a.verb == "render":
            text = read_text(a.file)
            line, replayed = render_text(text, a.section)
            if a.prove_against is not None:
                hand = list_line(text.split("\n"), a.prove_against)[1]
                same = hand == line
                print(f"RECONSTRUCTION {'PASSED' if same else 'FAILED'}: rendered #{a.section} vs the FULL line of #{a.prove_against} — "
                      + ("byte-identical" if same else f"first difference at char {next(i for i, (x, y) in enumerate(zip(hand, line)) if x != y) if any(x != y for x, y in zip(hand, line)) else min(len(hand), len(line))}"))
                return 0 if same else 1
            if a.write:
                os.makedirs(os.path.join(REPO, RENDERED_DIR), exist_ok=True)
                outp = os.path.join(REPO, RENDERED_DIR, f"carries-{a.section}.md")
                _write(outp, line + "\n"); print(f"rendered #{a.section} ({replayed} delta(s) replayed) → {outp} (gitignored, never committed)")
            else:
                print(line)
            return 0
        path = a.file if os.path.isabs(a.file) else os.path.join(REPO, a.file)
        text = read_text(path)
        if a.verb == "strike":
            note = a.note if a.note is not None else (open(a.note_file, encoding="utf-8").read() if a.note_file else None)
            if not note:
                raise CarryError("--note or --note-file is required")
            new, rec = strike_text(text, a.section, a.title, note)
        elif a.verb == "delta":
            if a.block:
                new, rec = delta_append(text, a.n_from, a.n_to, [], [], block=open(a.block, encoding="utf-8").read())
            else:
                if not a.new:
                    raise CarryError("delta needs --new FILE (or --block FILE)")
                items = [l.strip() for l in open(a.new, encoding="utf-8").read().split("\n") if l.strip()]
                strikes = []
                if a.struck:
                    for l in open(a.struck, encoding="utf-8").read().split("\n"):
                        if l.strip():
                            m = re.match(r"\*\*(.+?)\*\*\s*—\s*([A-Z ]+?)\s*—\s*(.*)$", l.strip(), re.S)
                            if not m:
                                raise CarryError(f"--struck line is `**TITLE** — VERDICT — receipt`: {l[:60]!r}")
                            strikes.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
                new, rec = delta_append(text, a.n_from, a.n_to, items, strikes, a.date)
        elif a.verb == "rebase":
            new, rec = rebase_text(text, a.section)
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
