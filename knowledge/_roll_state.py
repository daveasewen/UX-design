#!/usr/bin/env python3
"""_roll_state.py — T1 of the handoff testing regime (RULED #77, ledger § ★ #77;
notes/2026-08-02-handoff-testing-regime-plan.md).

A MEASURER, not a narrator. It reads the repo and emits ONE canonical line — the roll-residual
that the ★ LATEST banner should carry instead of authored prose. Per
[[measuring-tool-must-not-guess]]: observe, publish, never guess. UNKNOWN is never defaulted —
an unparseable surface raises `Unparseable` and the caller (a session, or `_capture_gate.py`'s
`roll_claim_check`, T2) gets a NAMED refusal, never a silent zero.

Measures, from the repo:
  (a) GM banner-block count      — ★ LATEST + ★ PRIOR blocks in GOOD-MORNING.md (2c: cap 2)
  (b) LS delta-block count       — ⏱ LATEST/PRIOR DELTA blocks in _LIVE-STATE.md (2d: cap 3)
  (c) GM stratum-block count     — live (non-STRATA_EXEMPT) blocks under
                                    `### ⏱ SESSION STRATA` (2f: cap 1)
  (d) newest session key         — notes/_GAUGE-LOG.md's `#### <date> #<N>` keys, MAX not first
                                    (Dave #44: highest number wins, file order is not consulted —
                                    _GAUGE-LOG.md is append-only but NOT append-in-order: keys
                                    have been added retroactively, out of sequence)
  (e) newest archive batch keys  — _GM-ARCHIVE.md's `## Batch <date> #<N>` and
                                    _LIVE-STATE-ARCHIVE.md's `## ⏱ PRIOR DELTA … #<N>` headings.
                                    Returned in the measurement dict for a caller to cross-check
                                    "did the roll actually land" (T2 uses this for the AUTHORED
                                    roll-claim's evidence, alongside (d) for 2f) — it does not
                                    appear in the printed canonical line, which has no slot for
                                    it; parseability is still asserted (a missing archive is a
                                    hard refusal, not a silently-assumed-empty one).

Session #N is read from the GM ★ LATEST banner ONLY — no stratum fallback, unlike
`_capture_gate.py`'s degraded-but-documented `_current_session_no`. This tool exists to be the
exact source; a fallback here would just be a second guess wearing this one's authority.

⚠ STRATA_KEY_RE / STRATA_EXEMPT are DUPLICATED from `_capture_gate.py`, not imported — forced by
the import direction (T2's `roll_claim_check` imports THIS module, so this module importing
`_capture_gate` back would cycle). `_capture_gate.py`'s own selftest pins the two copies equal
(ds-022's "one shape declared once" lesson, applied the only way the cycle allows).

Usage:  python3 knowledge/_roll_state.py             # prints ONE line, or a named refusal, exit
                                                       # 0/1 respectively
        python3 knowledge/_roll_state.py --selftest  # bite-test: green control · each surface
                                                       # corrupted → named refusal · an OVER
                                                       # state per rule (2c/2d/2f)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


class Unparseable(Exception):
    """Carries the exact refusal text (`UNPARSEABLE — <file> — <anchor sought>`). Raised, never
    swallowed into a guessed value — the HARD RULE this whole file exists to hold."""


# ---------------------------------------------------------------- anchors (line-start, per the
# #37 lesson: match the STRUCTURE — a blockquoted heading — never an unanchored substring).
BANNER_LATEST_RE = re.compile(r"^\s*>?\s*#{1,6}\s*★\s*LATEST\b.*?#(\d+)\b", re.M)
BANNER_BLOCK_RE = re.compile(r"^\s*>?\s*#{1,6}\s*★\s*(LATEST|PRIOR)\b", re.M)
LS_DELTA_BLOCK_RE = re.compile(r"^##\s*⏱\s*(LATEST|PRIOR) DELTA\b", re.M)
STRATA_HEAD_RE = re.compile(r"^###\s*⏱\s*SESSION STRATA\b", re.I | re.M)
STRATA_BLOCK_RE = re.compile(r"^####\s")
# ds-022's key shape, DUPLICATED (see module docstring) from `_capture_gate.py`'s
# `STRATA_KEY_RE`/`_key_session` — same regex, same session-number extraction.
STRATA_KEY_RE = re.compile(r"^####\s+\d{4}-\d{2}-\d{2}\s+#\d+\b")
_SESSION_NO_RE = re.compile(r"#(\d+)\b")
# #58 (Dave): the closed exempt list — permanently-unrollable strata, never a licence to
# accumulate a fourth. DUPLICATED from `_capture_gate.py`'s `STRATA_EXEMPT` (see module note).
# ⚠ 95/96 added on DAVE'S #96-D4 ruling (ONE WRITER: only roll_2f writes gauge-log sections;
# pre-existing collisions are marked exceptions by addition, not merged) — SYNCED #107, found
# drifted: `_capture_gate.py` carried {40,41,42,95,96} while this copy still read {40,41,42},
# which is exactly the parity failure this module's own selftest cross-check exists to catch
# (it never ran between #96 and #107, or it would have failed loud).
STRATA_EXEMPT = {40, 41, 42, 95, 96}
GM_ARCHIVE_BATCH_RE = re.compile(r"^##\s*Batch\s+\d{4}-\d{2}-\d{2}\s+#(\d+)\b", re.M)
LS_ARCHIVE_BATCH_RE = re.compile(r"^##\s*⏱\s*PRIOR DELTA\b.*?#(\d+)\b", re.M)


def _key_session(line):
    """Session number off a `#### <date> #<N>` heading, or None — mirrors
    `_capture_gate.py`'s `_key_session` exactly (same shape, duplicated per the module note)."""
    body = line[len("#### "):] if line.startswith("#### ") else line
    m = _SESSION_NO_RE.search(body)
    return int(m.group(1)) if m else None


def _read(repo, rel):
    p = os.path.join(repo, rel)
    if not os.path.exists(p):
        raise Unparseable(f"UNPARSEABLE — {rel} — file not found")
    with open(p, encoding="utf-8") as f:
        return f.read()


def _gm_banner_state(gm_text):
    m = BANNER_LATEST_RE.search(gm_text)
    if not m:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md — no `> ## ★ LATEST … #<N>` banner "
                          "heading (blockquoted, line-start — the #37 anchor)")
    session_no = int(m.group(1))
    banners = len(BANNER_BLOCK_RE.findall(gm_text))
    if banners == 0:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md — no ★ LATEST/★ PRIOR banner block "
                          "found, though the LATEST heading matched — contradictory state")
    return session_no, banners


def _gm_strata_state(gm_text, session_no):
    hm = STRATA_HEAD_RE.search(gm_text)
    if not hm:
        raise Unparseable("UNPARSEABLE — GOOD-MORNING.md — no `### ⏱ SESSION STRATA` marker")
    lines = gm_text[hm.end():].splitlines()
    end = len(lines)
    for i, ln in enumerate(lines):
        if re.match(r"^#{1,3}\s", ln):   # next same-or-higher heading = the strata region's end
            end = i
            break
    keys = [_key_session(ln) for ln in lines[:end] if STRATA_BLOCK_RE.match(ln)]
    # An unparseable heading (`None`) can never match STRATA_EXEMPT, so it counts as LIVE —
    # identical behaviour to `_capture_gate.py::check_budgets` for the same reason.
    live = sum(1 for k in keys if k not in STRATA_EXEMPT)
    return live, keys


def _ls_delta_count(repo):
    text = _read(repo, "_LIVE-STATE.md")
    n = len(LS_DELTA_BLOCK_RE.findall(text))
    if n == 0:
        raise Unparseable("UNPARSEABLE — _LIVE-STATE.md — no `## ⏱ LATEST/PRIOR DELTA` block "
                          "found")
    return n


def _gauge_log_newest(repo):
    text = _read(repo, "notes/_GAUGE-LOG.md")
    keys = [_key_session(ln) for ln in text.splitlines() if STRATA_KEY_RE.match(ln)]
    keys = [k for k in keys if k is not None]
    if not keys:
        raise Unparseable("UNPARSEABLE — notes/_GAUGE-LOG.md — no `#### <date> #<N>` key found")
    return max(keys)   # #44: highest number wins, file order is not consulted


def _archive_newest(repo, rel, rx):
    text = _read(repo, rel)   # missing file = UNPARSEABLE (a required surface, not an optional one)
    keys = [int(m.group(1)) for m in rx.finditer(text)]
    return max(keys) if keys else None   # zero batches so far is a legitimate state, not corruption


def measure(repo=REPO):
    """Returns a dict — every field a fact, no guess. Raises `Unparseable`, named, on the first
    surface that cannot be read honestly."""
    gm_text = _read(repo, "GOOD-MORNING.md")
    session_no, banners = _gm_banner_state(gm_text)
    strata_live, strata_keys = _gm_strata_state(gm_text, session_no)
    deltas = _ls_delta_count(repo)
    log_newest = _gauge_log_newest(repo)
    gm_archive_newest = _archive_newest(repo, "_GM-ARCHIVE.md", GM_ARCHIVE_BATCH_RE)
    ls_archive_newest = _archive_newest(repo, "_LIVE-STATE-ARCHIVE.md", LS_ARCHIVE_BATCH_RE)
    return {
        "session_no": session_no, "banners": banners,
        "deltas": deltas, "strata_live": strata_live, "strata_keys": strata_keys,
        "log_newest": log_newest,
        "gm_archive_newest": gm_archive_newest, "ls_archive_newest": ls_archive_newest,
    }


def render_line(m, today=None):
    """The ONE canonical line — this is what a banner carries verbatim (T1's whole point: the
    banner stops authoring this sentence and starts copying it)."""
    today = today or datetime.date.today()
    c2c = "OK" if m["banners"] <= 2 else "OVER"
    c2d = "OK" if m["deltas"] <= 3 else "OVER"
    c2f = "OK" if m["strata_live"] <= 1 else "OVER"
    return (f"> **residual (GENERATED #{m['session_no']}):** 2c {c2c} (banners {m['banners']}/2)"
            f" · 2d {c2d} (deltas {m['deltas']}/3) · 2f {c2f} (strata {m['strata_live']}, "
            f"log #{m['log_newest']}) — _roll_state.py · {today.isoformat()}")


def main():
    try:
        m = measure(REPO)
    except Unparseable as e:
        print(str(e))
        return 1
    print(render_line(m))
    return 0


# ---------------------------------------------------------------- selftest
def _fixture(session_no=77, banners=2, deltas=3, strata_keys=(77,), log_keys=(76,),
             gm_archive_keys=(76,), ls_archive_keys=(75,), drop=()):
    """A minimal synthetic tree. `drop` removes a named surface entirely (missing-file arm);
    pass e.g. `strata_keys=()` for a present-but-empty SESSION STRATA marker (a different arm
    from `drop=("gm_strata",)`, which removes the marker itself)."""
    gm = ["# Good morning", ""]
    if "gm_banner" not in drop:
        gm.append(f"> ## ★ LATEST — 2026-08-02 (Sun **#{session_no}**, fixture)")
        for i in range(banners - 1):
            gm.append(f"> ## ★ PRIOR — fixture prior {i}")
    if "gm_strata" not in drop:
        gm.append("### ⏱ SESSION STRATA")
        for k in strata_keys:
            gm.append(f"#### 2026-08-0{k % 9 + 1} #{k}")
    gm_text = "\n".join(gm) + "\n"

    if "ls_delta" in drop:
        ls = []   # no block of any kind — the "no ⏱ DELTA block found" arm
    else:
        ls = [f"## ⏱ LATEST DELTA — 2026-08-02 (Sun **#{session_no}**, fixture)"]
        for i in range(deltas - 1):
            ls.append(f"## ⏱ PRIOR DELTA — fixture prior {i}")
    ls_text = "\n".join(ls) + "\n"

    log_text = "" if "gauge_log" in drop else "\n".join(
        f"#### 2026-08-0{k % 9 + 1} #{k}" for k in log_keys) + "\n"
    gma_text = "\n".join(f"## Batch 2026-08-0{k % 9 + 1} #{k} — fixture" for k in gm_archive_keys) + "\n"
    lsa_text = "\n".join(f"## ⏱ PRIOR DELTA — 2026-08-0{k % 9 + 1} (**#{k}**, fixture)"
                         for k in ls_archive_keys) + "\n"
    return gm_text, ls_text, log_text, gma_text, lsa_text


def _write_tree(td, gm, ls, log, gma, lsa, drop=()):
    os.makedirs(os.path.join(td, "notes"), exist_ok=True)
    files = {"GOOD-MORNING.md": gm, "_LIVE-STATE.md": ls, "notes/_GAUGE-LOG.md": log,
             "_GM-ARCHIVE.md": gma, "_LIVE-STATE-ARCHIVE.md": lsa}
    for rel, body in files.items():
        surface = {"GOOD-MORNING.md": "gm_banner", "_LIVE-STATE.md": "ls_delta",
                   "notes/_GAUGE-LOG.md": "gauge_log", "_GM-ARCHIVE.md": "gm_archive",
                   "_LIVE-STATE-ARCHIVE.md": "ls_archive"}[rel]
        if surface in drop and surface in ("gm_archive", "ls_archive", "gauge_log"):
            continue   # the whole-file-missing arms for these three
        with open(os.path.join(td, rel), "w", encoding="utf-8") as f:
            f.write(body)


def selftest():
    import tempfile
    failures = []

    with tempfile.TemporaryDirectory() as td:
        gm, ls, log, gma, lsa = _fixture()
        _write_tree(td, gm, ls, log, gma, lsa)
        m = measure(td)
        line = render_line(m, today=datetime.date(2026, 8, 2))
        expect = ("> **residual (GENERATED #77):** 2c OK (banners 2/2) · 2d OK (deltas 3/3) · "
                 "2f OK (strata 1, log #76) — _roll_state.py · 2026-08-02")
        if line != expect:
            failures.append(f"green control: got {line!r}, expected {expect!r}")
        if m["gm_archive_newest"] != 76 or m["ls_archive_newest"] != 75:
            failures.append(f"green control: archive newest keys wrong: {m}")

    # ---- each surface corrupted individually → a NAMED refusal
    corruptions = [
        ("gm_banner missing",  dict(drop=("gm_banner",))),
        ("gm_strata marker missing", dict(drop=("gm_strata",))),
        ("ls_delta missing",   dict(drop=("ls_delta",))),
        ("gauge_log missing",  dict(drop=("gauge_log",))),
        ("gauge_log unkeyed",  dict(log_keys=())),
        ("gm_archive missing", dict(drop=("gm_archive",))),
        ("ls_archive missing", dict(drop=("ls_archive",))),
    ]
    for name, kw in corruptions:
        with tempfile.TemporaryDirectory() as td:
            gm, ls, log, gma, lsa = _fixture(**kw)
            _write_tree(td, gm, ls, log, gma, lsa, drop=kw.get("drop", ()))
            try:
                measure(td)
                failures.append(f"[{name}]: expected Unparseable, measured cleanly instead")
            except Unparseable as e:
                if "UNPARSEABLE" not in str(e):
                    failures.append(f"[{name}]: raised but not named UNPARSEABLE: {e}")

    # ---- an OVER state, one per rule
    overs = [
        ("2c OVER", dict(banners=3), "2c OVER"),
        ("2d OVER", dict(deltas=4), "2d OVER"),
        ("2f OVER", dict(strata_keys=(77, 78)), "2f OVER"),
    ]
    for name, kw, needle in overs:
        with tempfile.TemporaryDirectory() as td:
            gm, ls, log, gma, lsa = _fixture(**kw)
            _write_tree(td, gm, ls, log, gma, lsa)
            m = measure(td)
            line = render_line(m)
            if needle not in line:
                failures.append(f"[{name}]: expected {needle!r} in {line!r}")

    # ---- STRATA_EXEMPT / STRATA_KEY_RE must stay pinned equal to _capture_gate.py's own copies
    # — the cross-check the module docstring promises (ds-022's "one shape declared once", the
    # only way the import direction allows it here).
    sys.path.insert(0, HERE)
    try:
        import _capture_gate as cg
        if STRATA_EXEMPT != cg.STRATA_EXEMPT:
            failures.append(f"STRATA_EXEMPT drifted from _capture_gate.py: {STRATA_EXEMPT} vs "
                            f"{cg.STRATA_EXEMPT} — the two copies must stay pinned equal")
        if STRATA_KEY_RE.pattern != cg.STRATA_KEY_RE.pattern:
            failures.append("STRATA_KEY_RE drifted from _capture_gate.py's own copy")
    except Exception as e:
        failures.append(f"cross-check import of _capture_gate.py failed: {e}")

    if failures:
        for x in failures:
            print(f"  ❌ roll_state selftest: {x}")
        return 1
    print("  ✅ _roll_state.py selftest: green control renders exactly; every corrupted "
         "surface refuses named; every OVER state bites")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
