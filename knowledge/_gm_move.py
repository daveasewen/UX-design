#!/usr/bin/env python3
"""_gm_move.py — the hardened GOOD-MORNING / _LIVE-STATE mover (M5).

Ruled: `notes/_briefs/2026-07-27-memento-hardening-brief.md` §11 · `notes/_MEMENTO-DECISIONS.md`
§ ★ M-SET. Built 2026-07-28 #21, after FIVE consecutive wraps hand-rolled these moves with the
same discipline this file now enforces mechanically.

THE CONTRACT — every behaviour exists because its absence already cost a session:

  · line-START anchors ONLY. An anchor is a literal line PREFIX or a ^-anchored regex; a bare
    substring is REFUSED (silent-lookup class: a mid-line hit reads as authoritative and
    targets the wrong thing). Every locating anchor must match EXACTLY ONE line.
  · §A sha256 asserted BEFORE and AFTER on every projected write, via
    `_capture_gate.section_a_digest()` — the region is located by marker SEARCH, never line
    numbers, and the digest shape is pinned THERE (#17: a wrong-shape probe read a wrong
    digest that looked just as authoritative and cost an abort mid-wrap). §A is standing by
    ruling (GM-D7-am); there is deliberately NO flag to relax this — a §A edit is not a
    "move" and does not come through the mover.
  · projected-line-count guard. Caps are IMPORTED (`_capture_gate.SECTION_CAPS`) and the
    projected text is charged by the gate's own `charged_line_counts()` (strata exclusion
    included) — never re-derived. warn ≠ block (#19: prose stricter than its own gate nearly
    cost a live line): a projected count in the BLOCK band refuses; the warn band proceeds
    and SAYS so on stdout.
  · identical-string no-op = loud FAIL — per-op (find == replace refused up front) AND
    per-file (staged ops that leave a file byte-identical are a lookup that failed while
    reading as success, the ds-018 class).
  · all-or-nothing. Ops stage in memory across ALL files; every guard runs before ANY write.
    A content failure anywhere means NOTHING is written. (Residual risk, stated honestly:
    writes are per-file atomic via same-dir tmp + os.replace; an OS-level write error midway
    is not transactional across files — guards, not the OS, are the all-or-nothing layer.)
  · one-line receipt per op to stdout, printed only AFTER the writes land (a receipt for an
    unwritten move would be a false inscription). --dry-run prints them prefixed DRY.

WHAT THE MOVER DOES NOT CHECK, deliberately: the D7 `size:` stamp (it runs MID-ritual,
before re-stamping — freshness is the wrap gate's check) · verbatim-ness of a `replace`
(that is the caller's ritual discipline; `move` is verbatim BY CONSTRUCTION — the inserted
lines are the extracted list, untouched) · whether the ritual's EXIT CHECKS ran (a line
count is blind to them — see the runbook, steps 2c–2f).

OPS — a JSON list (via `--ops <file|->`), or the `Transaction` API:

  {"op": "move", "src": F, "start": A, "end": A | "EOF", "dst": F, "at": A,
   "where": "after" | "before"}
      Block = [start-line .. line before the FIRST end-match AFTER start), or to EOF.
      Extracted from src and inserted VERBATIM into dst at the anchor. Receipts carry the
      line count, so a wrong extent is visible, not silent.
  {"op": "replace", "file": F, "find": [lines], "replace": [lines]}
      `find` matches FULL LINES (list equality — inherently line-start), exactly once.
      `replace` may be shorter, longer, or empty (a ritual-licensed trim).
  {"op": "insert", "file": F, "at": A, "where": "after" | "before", "lines": [lines]}

  Anchors: a string = literal line prefix · {"regex": "^..."} = regex, MUST begin with '^'.
  Files are repo-relative. The mover NEVER creates a file — a new file must declare its own
  contract first (splitting never buys headroom).

CLI:
  python3 knowledge/_gm_move.py --ops ops.json [--repo DIR] [--dry-run]
  python3 knowledge/_gm_move.py --selftest
"""
import argparse
import io
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _capture_gate as cg  # section_spans · section_a_digest · SECTION_CAPS ·
#                             charged_line_counts · SECTION_REQUIRED · _gm_fixture (selftest)


class MoveError(Exception):
    """Any refusal. Reaching the CLI boundary it means: NOTHING was written."""


def _show(anchor):
    s = anchor["regex"] if isinstance(anchor, dict) else str(anchor)
    return repr(s if len(s) <= 48 else s[:45] + "…")


def _find_anchor(lines, anchor, lo=0, hi=None, what="anchor", first=False):
    """Index of the line matching a line-START anchor in [lo, hi).

    Literals match via startswith at position 0 of the line; regexes MUST declare '^'
    (re.match anchors anyway — demanding the '^' refuses patterns that READ as bare
    substrings). Default: exactly ONE match or refuse; `first=True` (end anchors only)
    takes the first match — the receipt's line count is what keeps that honest."""
    hi = len(lines) if hi is None else hi
    if isinstance(anchor, dict) and set(anchor) == {"regex"}:
        pat = anchor["regex"]
        if not pat.startswith("^"):
            raise MoveError(f"{what}: regex {pat!r} is not ^-anchored — line-START anchors "
                            f"only, bare substrings refused")
        try:
            rx = re.compile(pat)
        except re.error as e:
            raise MoveError(f"{what}: bad regex {pat!r} ({e})")
        hits = [i for i in range(lo, hi) if rx.match(lines[i])]
    elif isinstance(anchor, str):
        if not anchor.strip():
            raise MoveError(f"{what}: empty/whitespace anchor refused")
        hits = [i for i in range(lo, hi) if lines[i].startswith(anchor)]
    else:
        raise MoveError(f"{what}: {anchor!r} is neither a string nor {{'regex': '^…'}}")
    if first and hits:
        return hits[0]
    if len(hits) != 1:
        raise MoveError(f"{what}: {_show(anchor)} matched {len(hits)} lines "
                        f"(need exactly 1) — an ambiguous anchor targets nothing")
    return hits[0]


def _lines_arg(v, what):
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise MoveError(f"{what}: must be a LIST of line strings (got {type(v).__name__})")
    if any("\n" in x for x in v):
        raise MoveError(f"{what}: a line may not contain a newline — one string per line")
    return list(v)


def _where_arg(w):
    if w not in ("after", "before"):
        raise MoveError(f"where={w!r} — must be 'after' or 'before'")
    return w


class _File:
    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf-8") as f:
            self.before = f.read()
        self.lines = self.before.splitlines()
        self.had_nl = (self.before == "") or self.before.endswith("\n")

    def text(self):
        return "\n".join(self.lines) + ("\n" if self.had_nl else "")


class Transaction:
    """Stage ops across files, guard everything, then write everything — or nothing."""

    def __init__(self, repo):
        self.repo = os.path.abspath(repo)
        self.files = {}     # rel path -> _File
        self.receipts = []  # printed AFTER writes succeed
        self.warns = []

    def _file(self, rel):
        if rel not in self.files:
            p = os.path.join(self.repo, rel)
            if not os.path.isfile(p):
                raise MoveError(f"{rel}: no such file — the mover never creates files "
                                f"(a new file must declare its own contract first)")
            self.files[rel] = _File(p)
        return self.files[rel]

    # ---------------------------------------------------------------- ops
    def move(self, src, start, end, dst, at, where="after"):
        where = _where_arg(where)
        fs, fd = self._file(src), self._file(dst)
        if fs is fd:
            raise MoveError(f"move within {src}: src == dst — use replace/insert for "
                            f"in-file edits, a 'move' that stays is a rewrite")
        s = _find_anchor(fs.lines, start, what=f"move start ({src})")
        if end == "EOF":
            e = len(fs.lines)
        else:
            e = _find_anchor(fs.lines, end, lo=s + 1, what=f"move end ({src})", first=True)
        block = fs.lines[s:e]
        if not block:
            raise MoveError(f"{src}: move block is empty ({_show(start)} .. {_show(end)})")
        pos = _find_anchor(fd.lines, at, what=f"move insertion anchor ({dst})")
        del fs.lines[s:e]
        i = pos + 1 if where == "after" else pos
        fd.lines[i:i] = block  # VERBATIM by construction — the extracted list, untouched
        self.receipts.append(f"MOVE {len(block)} ln {src}[{_show(start)}…] → {dst} "
                             f"{where} {_show(at)}")

    def replace(self, file, find, replace):
        find = _lines_arg(find, f"replace.find ({file})")
        replace = _lines_arg(replace, f"replace.replace ({file})")
        if not find:
            raise MoveError(f"{file}: empty find-block matches everywhere — refused")
        if find == replace:
            raise MoveError(f"{file}: find == replace — identical-string no-op, the edit "
                            f"you meant did not happen")
        fl = self._file(file)
        n = len(find)
        hits = [i for i in range(len(fl.lines) - n + 1) if fl.lines[i:i + n] == find]
        if len(hits) != 1:
            raise MoveError(f"{file}: find-block ({n} ln, first {find[0][:40]!r}) matched "
                            f"{len(hits)} times — need exactly 1")
        i = hits[0]
        fl.lines[i:i + n] = replace
        self.receipts.append(f"REPLACE {n}→{len(replace)} ln in {file} at {find[0][:40]!r}")

    def insert(self, file, at, lines, where="after"):
        where = _where_arg(where)
        lines = _lines_arg(lines, f"insert.lines ({file})")
        if not lines:
            raise MoveError(f"{file}: insert of zero lines — no-op refused")
        fl = self._file(file)
        pos = _find_anchor(fl.lines, at, what=f"insert anchor ({file})")
        i = pos + 1 if where == "after" else pos
        fl.lines[i:i] = lines
        self.receipts.append(f"INSERT {len(lines)} ln into {file} {where} {_show(at)}")

    # ---------------------------------------------------------------- guards + write
    def _guard(self, rel, fl):
        after_text = fl.text()
        if after_text == fl.before:
            raise MoveError(f"{rel}: staged ops leave the file byte-identical — a compound "
                            f"no-op; the edit you meant did not happen")
        b_lines = fl.before.splitlines()
        b_spans = cg.section_spans(b_lines)
        if "§A" in b_spans and "§C" not in b_spans:
            raise MoveError(f"{rel}: has a §A marker but no §C — §A's extent cannot be "
                            f"located, refusing to touch the file at all")
        if "§A" not in b_spans:
            return  # not GM-shaped: no §A assert, no caps (LS, archives, gauge log)
        a_lines = fl.lines
        a_spans = cg.section_spans(a_lines)
        gone = [nm for nm in cg.SECTION_REQUIRED if nm in b_spans and nm not in a_spans]
        if gone:
            raise MoveError(f"{rel}: staged ops DESTROY required marker(s) {gone} — refused")
        d0 = cg.section_a_digest(b_lines, b_spans)
        d1 = cg.section_a_digest(a_lines, a_spans)
        if d0 != d1:
            raise MoveError(f"{rel}: §A digest {d0[:8]}… → {d1[:8]}… — §A is standing by "
                            f"ruling (GM-D7-am); the mover refuses, no flag exists")
        counts = cg.charged_line_counts(a_lines, a_spans)
        for name, (warn_at, block_at) in sorted(cg.SECTION_CAPS.items()):
            if name not in counts:
                continue
            n = counts[name]
            if n >= block_at:
                raise MoveError(f"{rel} {name}: projected {n} charged lines ≥ block "
                                f"{block_at} — the wrap gate would fail this; refused")
            if n > warn_at:
                self.warns.append(f"{rel} {name}: projected {n} charged lines > cap "
                                  f"{warn_at} (block {block_at}) — proceeding; warn ≠ block")

    def commit(self, dry_run=False):
        if not self.receipts:
            raise MoveError("no ops staged — an empty transaction is a no-op")
        for rel, fl in sorted(self.files.items()):
            self._guard(rel, fl)
        for w in self.warns:
            print(f"⚠ {w}")
        if not dry_run:
            for rel, fl in sorted(self.files.items()):
                d = os.path.dirname(fl.path) or "."
                fd, tmp = tempfile.mkstemp(dir=d, prefix=".gm_move.")
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(fl.text())
                    os.replace(tmp, fl.path)
                finally:
                    if os.path.exists(tmp):
                        os.unlink(tmp)
        tag = "DRY " if dry_run else ""
        for r in self.receipts:
            print(f"✔ {tag}{r}")


def run_ops(repo, ops, dry_run=False):
    """The whole mover as one call. Returns 0, or 2 with NOTHING written."""
    tx = Transaction(repo)
    try:
        if not isinstance(ops, list):
            raise MoveError("--ops must be a JSON LIST of op objects")
        for k, o in enumerate(ops):
            if not isinstance(o, dict) or "op" not in o:
                raise MoveError(f"op {k}: not an object with an 'op' key")
            o = dict(o)
            kind = o.pop("op")
            try:
                if kind == "move":
                    tx.move(**o)
                elif kind == "replace":
                    tx.replace(**o)
                elif kind == "insert":
                    tx.insert(**o)
                else:
                    raise MoveError(f"op {k}: unknown op {kind!r} (move|replace|insert)")
            except TypeError as e:
                raise MoveError(f"op {k} ({kind}): bad/missing argument — {e}")
        tx.commit(dry_run=dry_run)
    except MoveError as e:
        print(f"✖ FAIL: {e} — NOTHING written", file=sys.stderr)
        return 2
    return 0


# ==================================================================== selftest
# Every behaviour gets a bite that proves it FIRES on bad input, plus green controls that
# prove the refusals are attributable (a mover that refuses everything is as broken as one
# that refuses nothing). Fixtures reuse `_capture_gate._gm_fixture` — same synthetic GM the
# gate's own bites trust.

def _write(td, rel, text):
    p = os.path.join(td, rel)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


def _read(td, rel):
    with open(os.path.join(td, rel), encoding="utf-8") as f:
        return f.read()


def _fixture_repo(td, **gm_kw):
    _write(td, "GOOD-MORNING.md", cg._gm_fixture(**gm_kw))
    _write(td, "_GM-ARCHIVE.md", "# _GM-ARCHIVE\n\n## Batch 2026-07-28 #21\n\nold entry\n")
    _write(td, "_LIVE-STATE.md", "# _LIVE-STATE\n\nls line 1\nls line 2\nls line 3\n")


def _run(td, ops, dry_run=False):
    """run_ops with stdout/stderr captured. Returns (rc, out, err)."""
    out, err = io.StringIO(), io.StringIO()
    o_out, o_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        rc = run_ops(td, ops, dry_run=dry_run)
    finally:
        sys.stdout, sys.stderr = o_out, o_err
    return rc, out.getvalue(), err.getvalue()


def selftest():
    failures = []

    def bite(name, cond):
        if not cond:
            failures.append(name)

    with tempfile.TemporaryDirectory() as td:
        # ---- green control: a real move (LS → archive) + an in-cap GM replace ----------
        _fixture_repo(td, do_first=6, sec_a=8, sec_c=10)
        gm0, ls0 = _read(td, "GOOD-MORNING.md"), _read(td, "_LIVE-STATE.md")
        d0 = cg.section_a_digest(gm0.splitlines(), cg.section_spans(gm0.splitlines()))
        rc, out, err = _run(td, [
            {"op": "move", "src": "_LIVE-STATE.md", "start": "ls line 2", "end": "EOF",
             "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-07-28 #21", "where": "after"},
            {"op": "replace", "file": "GOOD-MORNING.md",
             "find": ["c line 3"], "replace": ["c line 3 (amended)"]},
        ])
        gm1, ls1, ar1 = (_read(td, "GOOD-MORNING.md"), _read(td, "_LIVE-STATE.md"),
                         _read(td, "_GM-ARCHIVE.md"))
        bite("green control: exit 0", rc == 0)
        bite("green control: src shrank", "ls line 2" not in ls1 and "ls line 1" in ls1)
        bite("green control: VERBATIM block landed in dst",
             "## Batch 2026-07-28 #21\nls line 2\nls line 3\n" in ar1)
        bite("green control: GM edit landed", "c line 3 (amended)" in gm1)
        d1 = cg.section_a_digest(gm1.splitlines(), cg.section_spans(gm1.splitlines()))
        bite("green control: §A digest stable across a legal edit", d0 == d1)
        bite("receipts: one line per op, stdout",
             out.count("✔ ") == 2 and "MOVE 2 ln" in out and "REPLACE 1→1 ln" in out)

        # ---- refusals: anchors ---------------------------------------------------------
        _fixture_repo(td, do_first=6, sec_a=8, sec_c=10)
        gm0 = _read(td, "GOOD-MORNING.md")
        rc, _o, err = _run(td, [{"op": "insert", "file": "GOOD-MORNING.md",
                                 "at": {"regex": "PRIOR"}, "lines": ["x"]}])
        bite("bare-substring regex REFUSED (fires)", rc != 0 and "^-anchored" in err)
        rc, _o, err = _run(td, [{"op": "insert", "file": "GOOD-MORNING.md",
                                 "at": "  ", "lines": ["x"]}])
        bite("empty anchor REFUSED (fires)", rc != 0 and "empty" in err)
        rc, _o, err = _run(td, [{"op": "insert", "file": "GOOD-MORNING.md",
                                 "at": "no such line anywhere", "lines": ["x"]}])
        bite("zero-match anchor REFUSED (fires)", rc != 0 and "matched 0" in err)
        rc, _o, err = _run(td, [{"op": "insert", "file": "GOOD-MORNING.md",
                                 "at": "c line ", "lines": ["x"]}])
        bite("ambiguous anchor REFUSED (fires)", rc != 0 and "need exactly 1" in err)
        bite("anchor refusals wrote NOTHING", _read(td, "GOOD-MORNING.md") == gm0)

        # ---- §A protection -------------------------------------------------------------
        rc, _o, err = _run(td, [{"op": "replace", "file": "GOOD-MORNING.md",
                                 "find": ["a line 3"], "replace": ["a line 3 CHANGED"]}])
        bite("§A edit REFUSED via digest (fires)", rc != 0 and "§A digest" in err)
        bite("§A refusal wrote NOTHING", _read(td, "GOOD-MORNING.md") == gm0)
        rc, _o, err = _run(td, [{"op": "move", "src": "GOOD-MORNING.md",
                                 "start": "# §C · QUEUE", "end": "EOF",
                                 "dst": "_GM-ARCHIVE.md", "at": "# _GM-ARCHIVE"}])
        bite("marker-destroying move REFUSED (fires)", rc != 0 and "DESTROY" in err)
        bite("marker refusal wrote NOTHING", _read(td, "GOOD-MORNING.md") == gm0
             and "§C" not in _read(td, "_GM-ARCHIVE.md"))

        # ---- projected caps: block refuses, warn proceeds and says so ------------------
        pad = [f"pad {i}" for i in range(230)]
        rc, _o, err = _run(td, [{"op": "insert", "file": "GOOD-MORNING.md",
                                 "at": "c line 9", "lines": pad}])
        bite("block-band projection REFUSED (fires)", rc != 0 and "≥ block" in err)
        bite("block refusal wrote NOTHING", _read(td, "GOOD-MORNING.md") == gm0)
        rc, out, _e = _run(td, [{"op": "insert", "file": "GOOD-MORNING.md",
                                 "at": "c line 9", "lines": pad[:145]}])
        bite("warn band PROCEEDS (warn ≠ block)", rc == 0 and "pad 144" in _read(td, "GOOD-MORNING.md"))
        bite("warn band SAYS SO on stdout", "warn ≠ block" in out and "> cap" in out)

        # ---- strata exclusion: mover charges what the gate charges ---------------------
        _fixture_repo(td, do_first=6, sec_a=8, sec_c=60, strata_blocks=1, strata_pad=300)
        rc, _o, err = _run(td, [{"op": "replace", "file": "GOOD-MORNING.md",
                                 "find": ["c line 3"], "replace": ["c line 3 (amended)"]}])
        bite("strata exclusion honoured (gross §C > block, charged §C under cap)",
             rc == 0, )

        # ---- no-ops --------------------------------------------------------------------
        _fixture_repo(td, do_first=6, sec_a=8, sec_c=10)
        gm0 = _read(td, "GOOD-MORNING.md")
        rc, _o, err = _run(td, [{"op": "replace", "file": "GOOD-MORNING.md",
                                 "find": ["c line 3"], "replace": ["c line 3"]}])
        bite("identical-string replace REFUSED loud (fires)",
             rc != 0 and "identical-string" in err)
        rc, _o, err = _run(td, [
            {"op": "replace", "file": "GOOD-MORNING.md",
             "find": ["c line 3"], "replace": ["TEMP"]},
            {"op": "replace", "file": "GOOD-MORNING.md",
             "find": ["TEMP"], "replace": ["c line 3"]},
        ])
        bite("compound byte-identical result REFUSED loud (fires)",
             rc != 0 and "byte-identical" in err)
        rc, _o, err = _run(td, [])
        bite("empty transaction REFUSED (fires)", rc != 0 and "no ops staged" in err)
        bite("no-op refusals wrote NOTHING", _read(td, "GOOD-MORNING.md") == gm0)

        # ---- all-or-nothing across files ----------------------------------------------
        ls0 = _read(td, "_LIVE-STATE.md")
        rc, _o, err = _run(td, [
            {"op": "insert", "file": "_LIVE-STATE.md", "at": "ls line 1",
             "lines": ["a perfectly valid line"]},                      # valid
            {"op": "replace", "file": "GOOD-MORNING.md",
             "find": ["a line 3"], "replace": ["a line 3 CHANGED"]},    # §A violation
        ])
        bite("all-or-nothing: one bad op vetoes the whole set (fires)", rc != 0)
        bite("all-or-nothing: the VALID op's file also untouched",
             _read(td, "_LIVE-STATE.md") == ls0)

        # ---- misc contract edges -------------------------------------------------------
        rc, _o, err = _run(td, [{"op": "move", "src": "_LIVE-STATE.md", "start": "ls line 1",
                                 "end": "EOF", "dst": "NOPE.md", "at": "x"}])
        bite("mover never creates files (fires)", rc != 0 and "never creates" in err)
        rc, out, _e = _run(td, [{"op": "insert", "file": "_LIVE-STATE.md",
                                 "at": "ls line 1", "lines": ["dry line"]}], dry_run=True)
        bite("dry-run: receipts prefixed, NOTHING written",
             rc == 0 and "✔ DRY" in out and "dry line" not in _read(td, "_LIVE-STATE.md"))

    if failures:
        for x in failures:
            print(f"  ❌ gm-move selftest: {x}")
        return 1
    print("  ✅ gm-move selftest: every refusal fires · green controls pass · receipts + "
          "warn≠block + all-or-nothing proven")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="hardened GM/LS mover (M5) — see module docstring")
    ap.add_argument("--ops", help="JSON ops file, or - for stdin")
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="repo root (default: parent of knowledge/)")
    ap.add_argument("--dry-run", action="store_true", help="stage + guard + receipts, no writes")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.ops:
        ap.error("--ops required (or --selftest)")
    raw = sys.stdin.read() if a.ops == "-" else open(a.ops, encoding="utf-8").read()
    try:
        ops = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"✖ FAIL: --ops is not valid JSON ({e}) — NOTHING written", file=sys.stderr)
        return 2
    return run_ops(a.repo, ops, dry_run=a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
