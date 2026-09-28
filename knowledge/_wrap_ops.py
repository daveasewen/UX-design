#!/usr/bin/env python3
"""_wrap_ops.py — builds the wrap's ONE move file for `_gm_move.py`, from arguments.

Built #306 lane W1 for `s306-D4` phase 1 (Dave, 2026-09-28 16:58 BST, "go on both"; the design
page's proof for this phase is "move files from 9 to 1"). It replaces the per-wrap
`build_ops_30N.py` (54 of 56 lines differed between #304's and #305's because the prose was
embedded in the script) AND the follow-up move files each wrap then wrote to fill placeholders
(#305: `_ops-305W-sizes.json`, `-gen.json`, `-s214.json`, `-s214b.json`, `-fix-*.json` …).

WHAT IS CODE (the same every wrap) — the anchors and the rolls, found by reading GM and LS:
  1. `> **TITLE THE NEXT CHAT →**` replaced (if --title)
  2. the date-split line inserted after the last `> ⚠ **WRAP DATE SPLIT` line (if --date-split)
  3. the new ★ LATEST banner inserted above the current one; 4. that one renamed ★ PRIOR   (2c)
  5. `## Batch <date> #N` opened in `_GM-ARCHIVE.md`; 6. the old ★ PRIOR banner(s) MOVED there (2c)
  7. `roll_2f` of #N-1's stratum (post-mortem → `notes/_GAUGE-LOG.md`, commit state → archive) (2f)
  8. the new stratum inserted where #N-1's stood
  9. the `*Last refreshed:` stamp inserted after the last one
 10. the new ⏱ LATEST delta inserted; 11. the old one renamed ⏱ PRIOR                     (2d)
 12. `## Rolled <date> #N …` opened in `_LIVE-STATE-ARCHIVE.md`; 13. every delta beyond
     LATEST + 2 PRIOR MOVED there, newest first                                          (2d)
WHAT VARIES (the prose, which is judgment and stays the story seat's): the banner, stratum,
delta, stamp and date-split texts, each a FILE named on the command line.

PLACEHOLDERS, so no second move file is needed: a line `{{SECTION_SIZES}}` in any text becomes
`_gm_usage.sizes_line(N)` and `{{ROLL_STATE}}` becomes `_roll_state.render_line()`, BOTH measured
on a PROJECTED copy of the five files with the ops applied (by `_gm_move.py --repo <tmp>`, the
real mover), exactly as the wrap seats measured them after the main move. The projection is
re-run with the filled ops, so the file written is one the mover has already accepted.
⚠ BOTH GENERATED LINES ALREADY START `> ` — write the placeholder BARE on its own line. Since #307
(2026-09-28, by addition; the #306 wrap wrote `> {{…}}` and hand-fixed the `> >` it produced), a
placeholder at the start of a line or list item that is written after `>` or `> ` is folded:
the `>` is dropped so the line comes out with ONE `> `, never `> >`.
Not done here, and declared: 2d's `Previous:` chain trim (none is left in `_LIVE-STATE.md`),
2e (DO-FIRST carries no session-keyed stratum), and the `size:` stamp (`_gen_size_stamp.py`).

Usage:
  python3 knowledge/_wrap_ops.py --session 306 --date 2026-09-28 [--session-date 2026-09-28]
      --banner B.md --stratum S.md --delta D.md --stamp STAMP.md [--title T] [--date-split F]
      [--batch-note F] [--rolled-note F] --out notes/_lanes/306/W/_ops-306W.json [--repo DIR]
  python3 knowledge/_wrap_ops.py --selftest
  python3 knowledge/_wrap_ops.py --fill-token PLACEHOLDER-306W --fill-file _LIVE-STATE.md
      --fill-text 5b.md --out notes/_lanes/306/W/_ops-306W-5b.json
      # the 5b addendum ONLY: it records the wrap commit's own sha, which the first move file
      # cannot carry; one `replace` op of the one line holding the token
Then: python3 knowledge/_gm_move.py --ops <out> --dry-run, and without --dry-run to write.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
FILES = ["GOOD-MORNING.md", "_LIVE-STATE.md", "_GM-ARCHIVE.md", "_LIVE-STATE-ARCHIVE.md", "notes/_GAUGE-LOG.md"]
GM, LS, GMA, LSA = FILES[:4]
LATEST = "> ## ★ LATEST — "
PRIOR = "> ## ★ PRIOR — "
DLATEST = "## ⏱ LATEST DELTA"
DPRIOR = "## ⏱ PRIOR DELTA"
PH_SIZES, PH_ROLL = "{{SECTION_SIZES}}", "{{ROLL_STATE}}"


class OpsError(Exception):
    """A named refusal. At the CLI it means: no move file was written."""


def _lines(repo, rel):
    with open(os.path.join(repo, rel), encoding="utf-8") as f:
        return f.read().split("\n")


def _one(lines, pred, what):
    hits = [i for i, l in enumerate(lines) if pred(l)]
    if len(hits) != 1:
        raise OpsError(f"{what}: {len(hits)} matching lines — exactly one is required")
    return hits[0]


def _text(path):
    with open(path, encoding="utf-8") as f:
        return f.read().rstrip("\n").split("\n") + [""]


def build(repo, n, date, sdate, banner, stratum, delta, stamp, title=None, date_split=None,
          batch_note=None, rolled_note=None):
    gm, ls = _lines(repo, GM), _lines(repo, LS)
    gma, lsa = _lines(repo, GMA), _lines(repo, LSA)
    ops = []
    if title:
        t = _one(gm, lambda l: l.startswith("> **TITLE THE NEXT CHAT →**"), "title line")
        ops.append({"op": "replace", "file": GM, "find": [gm[t]], "replace": ["> **TITLE THE NEXT CHAT →** `" + title + "`"]})
    if date_split:
        ds = [i for i, l in enumerate(gm) if l.startswith("> ⚠ **WRAP DATE SPLIT")]
        if not ds:
            raise OpsError("no `> ⚠ **WRAP DATE SPLIT` line to insert after")
        ops.append({"op": "insert", "file": GM, "at": gm[ds[-1]], "where": "after", "lines": [l for l in date_split if l != ""] })
    li = _one(gm, lambda l: l.startswith(LATEST), "★ LATEST banner")
    if f"**#{n}**" in gm[li]:
        raise OpsError(f"the ★ LATEST banner is already #{n}'s — this move file was applied")
    priors = [i for i, l in enumerate(gm) if l.startswith(PRIOR)]
    if not priors:
        raise OpsError("no ★ PRIOR banner — nothing to roll (2c needs LATEST + 1 PRIOR)")
    ops.append({"op": "insert", "file": GM, "at": gm[li], "where": "before", "lines": banner})
    ops.append({"op": "replace", "file": GM, "find": [gm[li]], "replace": [gm[li].replace(LATEST, PRIOR, 1)]})
    batch_head = f"## Batch {sdate} #{n}"
    if any(l == batch_head for l in gma):
        raise OpsError(f"`{batch_head}` already exists in {GMA}")
    first_batch = next((l for l in gma if l.startswith("## Batch ")), None)
    if first_batch is None:
        raise OpsError(f"{GMA} has no `## Batch ` line to insert above")
    note = batch_note or [f"*Rolled at the #{n} wrap (2c, ritual {date}). The old ★ PRIOR banner, moved VERBATIM "
                          f"by `_gm_move.py` — a move, never a rewrite.*"]
    ops.append({"op": "insert", "file": GMA, "at": first_batch, "where": "before", "lines": [batch_head, ""] + [l for l in note if l != ""] + [""]})
    for p in priors:
        end = next((gm[j] for j in range(p + 1, len(gm)) if gm[j].startswith("## ") or gm[j].startswith(PRIOR)), None)
        if end is None:
            raise OpsError("the ★ PRIOR banner has no following heading to end its block")
        ops.append({"op": "move", "src": GM, "start": gm[p], "end": end, "dst": GMA, "at": batch_head, "where": "after"})
    prev = n - 1
    key = re.compile(r"^#### \d{4}-\d{2}-\d{2} #%d\b" % prev)
    pm = _one(gm, lambda l: bool(key.match(l)), f"stratum key `#### <date> #{prev}`")
    cs_pre = f"> **COMMIT STATE #{prev}:**"
    cs = _one(gm, lambda l: l.startswith(cs_pre), f"`{cs_pre}`")
    nxt = next((gm[j] for j in range(cs + 1, len(gm)) if gm[j].startswith("#### ") or gm[j].startswith("## ")
                or gm[j].startswith("### ")), None)
    if nxt is None:
        raise OpsError(f"nothing follows #{prev}'s commit state to end the stratum")
    ops.append({"op": "roll_2f", "session": prev, "pm_start": gm[pm], "pm_end": cs_pre, "cs_start": cs_pre, "cs_end": nxt})
    ops.append({"op": "insert", "file": GM, "at": nxt, "where": "before", "lines": stratum})
    stamps = [i for i, l in enumerate(ls) if l.startswith("*Last refreshed:")]
    if not stamps:
        raise OpsError("no `*Last refreshed:` line in _LIVE-STATE.md")
    ops.append({"op": "insert", "file": LS, "at": ls[stamps[-1]], "where": "after", "lines": [l for l in stamp if l != ""]})
    dl = _one(ls, lambda l: l.startswith(DLATEST), "⏱ LATEST DELTA")
    if f"**#{n}**" in ls[dl]:
        raise OpsError(f"the ⏱ LATEST DELTA is already #{n}'s — this move file was applied")
    ops.append({"op": "insert", "file": LS, "at": ls[dl], "where": "before", "lines": delta})
    ops.append({"op": "replace", "file": LS, "find": [ls[dl]], "replace": [ls[dl].replace(DLATEST, DPRIOR, 1)]})
    dps = [i for i, l in enumerate(ls) if l.startswith(DPRIOR)]
    roll = dps[1:]                       # after the rename the old LATEST is PRIOR #1; keep 2 PRIOR in all
    if roll:
        first_rolled = next((l for l in lsa if l.startswith("## Rolled ")), None)
        if first_rolled is None:
            raise OpsError(f"{LSA} has no `## Rolled ` line to insert above")
        head = f"## Rolled {sdate} #{n} (2d, at the #{n} wrap, ritual {date}) — via the mover"
        rn = rolled_note or [f"*The {len(roll)} oldest ⏱ delta block(s), moved VERBATIM by `_gm_move.py`.*"]
        ops.append({"op": "insert", "file": LSA, "at": first_rolled, "where": "before", "lines": [head, ""] + [l for l in rn if l != ""] + [""]})
        for i in roll:
            end = next((ls[j] for j in range(i + 1, len(ls)) if ls[j].startswith("## ")), "EOF")
            ops.append({"op": "move", "src": LS, "start": ls[i], "end": end, "dst": LSA, "at": first_rolled, "where": "before"})
    return ops


def fill_op(repo, rel, token, text):
    """One `replace` op: the ONE line of `rel` holding `token`, with the token replaced by `text`."""
    lines = _lines(repo, rel)
    i = _one(lines, lambda l: token in l, f"`{token}` in {rel}")
    t = " ".join(x for x in text if x != "") if isinstance(text, list) else text
    if "\n" in t:
        raise OpsError("the fill text must be one line")
    return [{"op": "replace", "file": rel, "find": [lines[i]], "replace": [lines[i].replace(token, t, 1)]}]


def _mover(repo, ops_path, dry_run):
    r = subprocess.run([sys.executable, os.path.join(HERE, "_gm_move.py"), "--ops", ops_path, "--repo", repo]
                       + (["--dry-run"] if dry_run else []), capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def _projection(src_repo):
    base = "/dev/shm" if os.path.isdir("/dev/shm") and os.access("/dev/shm", os.W_OK) else None
    td = tempfile.mkdtemp(prefix="wrapops-", dir=base)
    for f in FILES:
        os.makedirs(os.path.dirname(os.path.join(td, f)) or td, exist_ok=True)
        shutil.copyfile(os.path.join(src_repo, f), os.path.join(td, f))
    return td


def _has(ops, ph):
    return any(ph in json.dumps(o, ensure_ascii=False) for o in ops)


def fill(ops, subs):
    """Replace each placeholder with its line. A placeholder written after a leading `>` / `> `
    (at the start of a JSON string or just after an escaped newline, i.e. at the start of a line)
    takes that quote marker with it when the filled line already starts `> ` — so `> {{ROLL_STATE}}`
    and a bare `{{ROLL_STATE}}` both come out as ONE `> ` line (#307; the #306 wrap's `> >`)."""
    s = json.dumps(ops, ensure_ascii=False)
    for k, v in subs.items():
        ek, ev = json.dumps(k, ensure_ascii=False)[1:-1], json.dumps(v, ensure_ascii=False)[1:-1]
        if v.startswith(">"):
            s = re.sub(r'(?:(?<=")|(?<=\\n))> ?' + re.escape(ek), lambda m: ev, s)
        s = s.replace(ek, ev)
    return json.loads(s)


def _real_sizes(n, repo):
    import _gm_usage
    return _gm_usage.sizes_line(n, repo=repo)


def project_and_fill(repo, ops, n, date, sizes=_real_sizes):
    """Apply `ops` to a projected copy with the real mover; measure the placeholders there; return
    (filled_ops, receipts). ORDER, as the wrap seats measured: `{{ROLL_STATE}}` first (it lands in
    the banner), then `{{SECTION_SIZES}}` on a projection that already carries the filled roll line,
    then one more mover pass over the fully filled ops. Raises OpsError if the mover refuses any pass."""
    need = [p for p in (PH_ROLL, PH_SIZES) if _has(ops, p)]
    td = _projection(repo)
    op1 = os.path.join(td, "_ops.json")

    def apply(o, what):
        for f in FILES:
            shutil.copyfile(os.path.join(repo, f), os.path.join(td, f))
        json.dump(o, open(op1, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc, out = _mover(td, op1, dry_run=False)
        if rc != 0:
            raise OpsError(f"the mover REFUSED the {what} ops on the projection:\n" + out[-1500:])
        return out
    try:
        out = apply(ops, "built")
        filled, done = ops, []
        if PH_ROLL in need:
            import _roll_state
            line = _roll_state.render_line(_roll_state.measure(td), today=datetime.date.fromisoformat(date))
            filled = fill(filled, {PH_ROLL: line}); done.append(PH_ROLL)
            if PH_SIZES in need:
                out = apply(filled, "roll-filled")
        if PH_SIZES in need:
            line, errs = sizes(n, td)
            if errs:
                raise OpsError("section sizes could not be measured on the projection: " + "; ".join(errs))
            filled = fill(filled, {PH_SIZES: line}); done.append(PH_SIZES)
        if done:
            out = apply(filled, "fully filled")
        return filled, {"filled": done, "mover_receipts": [l for l in out.splitlines() if l.strip()][-20:]}
    finally:
        shutil.rmtree(td, ignore_errors=True)


# ------------------------------------------------------------------------------------ selftest
def selftest():
    ok = True

    def bite(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok = ok and bool(cond)

    import _capture_gate as cg
    td = tempfile.mkdtemp(prefix="wrapops-st-")
    try:
        gm, ls, log, gma, lsa = _fixture(cg)
        for rel, txt in zip(FILES, (gm, ls, gma, lsa, log)):
            os.makedirs(os.path.dirname(os.path.join(td, rel)) or td, exist_ok=True)
            open(os.path.join(td, rel), "w", encoding="utf-8").write(txt)
        w = lambda name, s: (open(os.path.join(td, name), "w", encoding="utf-8").write(s), os.path.join(td, name))[1]
        B = _text(w("b.md", "> ## ★ LATEST — 2026-01-03 (Sat **#79**, fixture)\n>\n> - ① new banner item\n{{ROLL_STATE}}\n"))
        S = _text(w("s.md", "#### 2026-01-03 #79\n\n> **pre-flight #79:** fixture\n\n{{SECTION_SIZES}}\n\n> **COMMIT STATE #79:** fixture\n"))
        D = _text(w("d.md", "## ⏱ LATEST DELTA — 2026-01-03 (**#79**, fixture)\n\n> fixture delta\n"))
        ST = _text(w("st.md", "*Last refreshed: 2026-01-03 (fixture — **#79 wrap**)*\n"))
        ops = build(td, 79, "2026-01-03", "2026-01-03", B, S, D, ST, title="Fixture - #80: next")
        kinds = [o["op"] for o in ops]
        bite("the op order is #305's: title, banner, rename, batch, move, roll_2f, stratum, stamp, delta, rename, rolled, move",
             kinds == ["replace", "insert", "replace", "insert", "move", "roll_2f", "insert", "insert", "insert", "replace", "insert", "move"])
        bite("roll_2f rolls #78 with its commit state", ops[5]["session"] == 78 and ops[5]["cs_start"] == "> **COMMIT STATE #78:**")
        bite("only deltas beyond LATEST + 2 PRIOR move (one here)", sum(1 for o in ops if o["op"] == "move" and o["src"] == LS) == 1)
        rc, out = _mover(td, (json.dump(ops, open(os.path.join(td, "o.json"), "w"), ensure_ascii=False) or os.path.join(td, "o.json")), True)
        bite("the real mover accepts the built ops (dry run)", rc == 0)
        try:
            project_and_fill(td, ops, 79, "2026-01-03")
            bite("the REAL sizes measurer on a fixture without the vocabulary REFUSES, never a partial line", False)
        except OpsError as e:
            bite("the REAL sizes measurer on a fixture without the vocabulary REFUSES, never a partial line",
                 "vocabulary marker not found" in str(e))
        # stub measurer: proves the line is measured on the PROJECTED tree (the new banner is in it)
        stub = lambda n, r: ("> **section-sizes #%d (stub):** LATEST says %s" % (
            n, "#79" if "**#79**" in open(os.path.join(r, GM), encoding="utf-8").read() else "NOT-PROJECTED"), [])
        filled, rec = project_and_fill(td, ops, 79, "2026-01-03", sizes=stub)
        fj = json.dumps(filled, ensure_ascii=False)
        bite("{{SECTION_SIZES}} and {{ROLL_STATE}} are filled from the projection",
             PH_SIZES not in fj and PH_ROLL not in fj and "section-sizes #79 (stub):** LATEST says #79" in fj and "residual (GENERATED #79)" in fj)
        bite("the projection wrote nothing to the tree it copied", open(os.path.join(td, GM), encoding="utf-8").read() == gm)
        json.dump(filled, open(os.path.join(td, "f.json"), "w"), ensure_ascii=False)
        rc, out = _mover(td, os.path.join(td, "f.json"), False)
        g2 = open(os.path.join(td, GM), encoding="utf-8").read()
        a_gma = open(os.path.join(td, GMA), encoding="utf-8").read()
        a_lsa = open(os.path.join(td, LSA), encoding="utf-8").read()
        a_log = open(os.path.join(td, "notes/_GAUGE-LOG.md"), encoding="utf-8").read()
        bite("applied for real: #79 LATEST, #78 PRIOR, #77's banner in the archive under Batch #79",
             rc == 0 and "> ## ★ LATEST — 2026-01-03 (Sat **#79**" in g2 and "> ## ★ PRIOR — 2026-01-02 (Fri **#78**" in g2
             and "**#77**" not in g2 and a_gma.index("## Batch 2026-01-03 #79") < a_gma.index("**#77**"))
        bite("applied for real: #78's post-mortem in the gauge log, its commit state in the archive, #79's stratum in GM",
             "#### 2026-01-02 #78" in a_log and "> **COMMIT STATE #78:**" in a_gma and "#### 2026-01-03 #79" in g2
             and "#### 2026-01-02 #78" not in g2)
        bite("applied for real: the #76 delta rolled, newest-first under Rolled #79",
             "(**#76**" in a_lsa and a_lsa.index("## Rolled 2026-01-03 #79") < a_lsa.index("(**#76**")
             < a_lsa.index("## Rolled 2026-01-02 #78"))
        import _roll_state
        m = _roll_state.measure(td)
        bite("after the move: 2 banners, 3 deltas, 1 stratum (_roll_state reads OK)",
             m["banners"] == 2 and m["deltas"] == 3 and m["strata_live"] == 1)
        try:
            build(td, 79, "2026-01-03", "2026-01-03", B, S, D, ST); bite("a second build on the moved tree is refused", False)
        except OpsError:
            bite("a second build on the moved tree is refused", True)
        fo = fill_op(td, LS, "fixture delta", "the 5b line")
        bite("--fill: one replace op of the one line holding the token", len(fo) == 1 and fo[0]["replace"] == ["> the 5b line"])
        try:
            fill_op(td, LS, "fixture", "x"); bite("--fill refuses a token on more than one line", False)
        except OpsError:
            bite("--fill refuses a token on more than one line", True)
        # #307: a placeholder written as `> {{…}}` must not come out `> >` (the #306 wrap's hand fix)
        ln = "> **residual (GENERATED #79):** fixture"
        qf = fill([{"lines": ["> " + PH_ROLL, ">" + PH_ROLL, PH_ROLL], "text": "a\n> " + PH_SIZES + "\nb"}],
                  {PH_ROLL: ln, PH_SIZES: "> **section-sizes #79:** fixture"})
        bite("`> {{ROLL_STATE}}`, `>{{ROLL_STATE}}` and a bare one all fill to ONE `> ` line, never `> >`",
             qf[0]["lines"] == [ln, ln, ln] and "> >" not in json.dumps(qf, ensure_ascii=False))
        bite("`> {{SECTION_SIZES}}` inside a multi-line text fills to ONE `> ` line",
             qf[0]["text"] == "a\n> **section-sizes #79:** fixture\nb")
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print("wrap-ops selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def _fixture(cg):
    """A five-file tree in the real shapes: GM from the gate's own `_gm_fixture` (the one the
    mover's bites trust) with a #78 LATEST, a #77 PRIOR and a #78 stratum patched in; LS with a
    LATEST + 2 PRIOR delta stack; the two archives and the gauge log."""
    gm = cg._gm_fixture(strata_keys=[40])
    old = "> ## ★ LATEST — 2026-07-28 (fixture session)\n> - one session-record line\n"
    assert old in gm, "the gate's fixture changed shape"
    gm = gm.replace(old, "> ## ★ LATEST — 2026-01-02 (Fri **#78**, fixture)\n> - #78 line\n\n"
                         "> ## ★ PRIOR — 2026-01-01 (Thu **#77**, fixture)\n> - #77 line\n\n")
    gm = gm.replace("#### 2026-07-20 #40", "#### 2026-01-02 #78\n> post-mortem #78\n\n> **COMMIT STATE #78:** fixture\n\n#### 2026-07-20 #40")
    ls = ("# _LIVE-STATE\n\n*Last refreshed: 2026-01-02 (fixture — **#78 wrap**)*\n\n"
          "## ⏱ LATEST DELTA — 2026-01-02 (**#78**, fixture)\n\nd78\n\n"
          "## ⏱ PRIOR DELTA — 2026-01-01 (**#77**, fixture)\n\nd77\n\n"
          "## ⏱ PRIOR DELTA — 2025-12-31 (**#76**, fixture)\n\nd76\n\n## 🕓 OPEN — fixture\n\nopen\n")
    gma = "# _GM-ARCHIVE\n\n## Batch 2026-01-02 #78\n\nold entry\n"
    lsa = "# _LIVE-STATE archive\n\n## Rolled 2026-01-02 #78 (fixture)\n\nold\n"
    log = "# _GAUGE-LOG\n\n#### 2026-01-01 #77\nolder block\n"
    return gm, ls, log, gma, lsa


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--session", type=int); ap.add_argument("--date"); ap.add_argument("--session-date")
    for f in ("banner", "stratum", "delta", "stamp", "date-split", "batch-note", "rolled-note"):
        ap.add_argument("--" + f)
    ap.add_argument("--title"); ap.add_argument("--out"); ap.add_argument("--repo", default=REPO)
    ap.add_argument("--no-projection", action="store_true", help="skip the projection (placeholders stay unfilled)")
    ap.add_argument("--fill-token"); ap.add_argument("--fill-file"); ap.add_argument("--fill-text")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.fill_token:
        if not (a.fill_file and a.fill_text and a.out):
            ap.error("--fill-token needs --fill-file, --fill-text and --out")
        try:
            if os.path.exists(a.out):
                raise OpsError(f"{a.out} exists — name a new move file")
            ops = fill_op(a.repo, a.fill_file, a.fill_token, _text(a.fill_text))
        except OpsError as e:
            print("⛔ REFUSED:", e); return 1
        json.dump(ops, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"wrote {a.out}: 1 replace op on {a.fill_file}")
        return 0
    need = [k for k in ("session", "date", "banner", "stratum", "delta", "stamp", "out") if getattr(a, k) is None]
    if need:
        ap.error("missing: " + ", ".join("--" + k for k in need))
    try:
        rd = lambda p: _text(p) if p else None
        ops = build(a.repo, a.session, a.date, a.session_date or a.date, rd(a.banner), rd(a.stratum), rd(a.delta),
                    rd(a.stamp), a.title, rd(a.date_split), rd(a.batch_note), rd(a.rolled_note))
        rec = {}
        if not a.no_projection:
            ops, rec = project_and_fill(a.repo, ops, a.session, a.date)
        if os.path.exists(a.out):
            raise OpsError(f"{a.out} exists — one move file per wrap, named once")
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(ops, f, ensure_ascii=False, indent=1)
    except OpsError as e:
        print("⛔ REFUSED:", e); return 1
    print(f"wrote {a.out}: {len(ops)} ops, {os.path.getsize(a.out):,} bytes"
          + (f" · filled {rec.get('filled')} on a projection the mover accepted" if rec else " · NOT projected"))
    print("next: python3 knowledge/_gm_move.py --ops", a.out, "--dry-run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
