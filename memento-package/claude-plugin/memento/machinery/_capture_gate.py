#!/usr/bin/env python3
"""_capture_gate shim — lets the verbatim `_gen_chain.py` in this folder run standalone.

WHAT THIS IS. `_gen_chain.py` (copied verbatim into this package) does `import _capture_gate as
cg` and calls exactly four of its functions: `cg.chain_parts`, `cg.measure_tokens`,
`cg.measurement_degraded`, `cg.read_chain_tk`. The real `knowledge/_capture_gate.py` is ~2,500
Apollo-laced lines (provenance/status gates, section-size budgets, band arithmetic, etc.) that
`_gen_chain.py` never touches. This module is NOT a copy of that file — it is a small, standalone
module that reproduces the behaviour of those four functions and nothing else, so the package
does not have to drag Apollo's gate machinery along for the ride.

PROVENANCE. Ported from `knowledge/_capture_gate.py` @ HEAD `91d7528` (2026-07-31, that file's own
last touch; repo HEAD at port time was `13433cc`), these line ranges:
  - `chain_parts`            lines 1164-1243
  - `read_chain_tk`          lines 1246-1267
  - `measure_tokens`         lines 1350-1374
  - `measurement_degraded`   lines 1377-1395
  - `dofirst_index`          lines 1097-1161   (helper `chain_parts` calls internally)
  - `_heal_tiktoken`         lines 1330-1347   (helper `measure_tokens` calls internally)
  - `_TIKTOKEN_HEAL_TRIED`   line  1327
  - `BYTES_PER_TOKEN`        line  361
  - `DOFIRST_ITEM_RE` / `DOFIRST_HOOK_MAX` / `DOFIRST_INDEX_TK_MAX`   lines 1092-1094
  - `LS_DELTA_RE`            line  1072

★ A DEPENDENCY THE MANIFEST DID NOT NAME. `chain_parts` (and, through it, `dofirst_index`) reads
two small vocabularies — `GM_VOCAB` and `LS_VOCAB` — from a SEPARATE 833-line module,
`knowledge/_gm_usage.py`, which is not one of the four ported functions and is not in this
package at all. Porting the whole module would have re-imported the same "Apollo-laced" problem
the four-function shim exists to avoid (that file is itself full of session-usage/testimony
machinery `_gen_chain.py` never needs). Instead, the two tuples themselves are ported verbatim
below (`knowledge/_gm_usage.py` @ HEAD `ace3ed3` 2026-07-31, lines 66-76 and 81-93) — they are
plain `(id, compiled-regex)` data, not logic, and are exactly what `chain_parts`/`dofirst_index`
read from the module. **Flag for the conductor:** the manifest's "exactly four functions" framing
undercounts by this one data dependency; nothing here was invented, but the manifest is now
stale on this point and should be corrected or footnoted.

INVENTORY — ported vs left behind.
  PORTED (this file, in full): chain_parts, read_chain_tk, measure_tokens, measurement_degraded,
    dofirst_index, _heal_tiktoken, the tiktoken-heal state flag, BYTES_PER_TOKEN, the DOFIRST_*
    regex/constants, LS_DELTA_RE, and GM_VOCAB/LS_VOCAB (copied verbatim from `_gm_usage.py`,
    not derived or re-invented).
  LEFT BEHIND (everything else in `knowledge/_capture_gate.py`): the provenance/status build
    gate, WRAP mode, section-size budgets and bands (SECTION_CAPS, BANDS, CHAIN_BUDGET_TK, ...),
    §A digest/hashing, strata/session-key parsing, banner-budget statistics, the pre-flight-token
    checker, `chain_file_tk` (measures `_CHAIN.md` against a budget — a budget-check consumer,
    not one of the four `_gen_chain.py` calls), and all of `_capture_gate.py`'s own CLI/selftest
    surface. None of it is imported by `chain_parts`/`read_chain_tk`/`measure_tokens`/
    `measurement_degraded`, so none of it is here.

BEHAVIOUR HELD IDENTICAL, ON PURPOSE:
  - tiktoken (`cl100k_base`) is the real instrument when it is importable and its encoding file
    loads; the byte-divisor fallback (`BYTES_PER_TOKEN = 3.53`) is used ONLY when tiktoken is
    absent or its encoder is unloadable, and it labels itself "ESTIMATE" rather than passing
    silently as a real measurement.
  - `measurement_degraded()` asks the SAME `measure_tokens()` call path a real measurement would
    use (a 1-character probe) rather than a second, hand-rolled health check — so it cannot drift
    from what an actual measurement would report.
  - `chain_parts` / `dofirst_index` REFUSE (return `None` + a reason) rather than emit a
    confident-but-empty chain or worklist index on any parse failure — a declared gap, never a
    silent one.
"""
import importlib
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------------------------
# ds-021 / M6 — THE ONE UNIT AND THE HONEST FALLBACK.
# Ported verbatim, `knowledge/_capture_gate.py` line 361.
BYTES_PER_TOKEN = 3.53     # MEASURED on GM, tiktoken cl100k_base, 2026-07-27. NOT the chars/4 rule.

# ---------------------------------------------------------------------------------------------
# THE PRESENCE-INDEX CONSTANTS. Ported verbatim, `knowledge/_capture_gate.py` lines 1092-1094.
DOFIRST_ITEM_RE = re.compile(r"^>\s*\*\*(\d+[a-z]?)\.\s*(.+)$")
DOFIRST_HOOK_MAX = 46            # chars per hook — a BYTE bound, deliberately
DOFIRST_INDEX_TK_MAX = 420       # ⚠ the whole index, MEASURED — see below

# `knowledge/_capture_gate.py` line 1072.
LS_DELTA_RE = re.compile(r"^##\s*⏱")

# ---------------------------------------------------------------------------------------------
# THE TWO VOCABULARIES `chain_parts`/`dofirst_index` READ. Ported verbatim from
# `knowledge/_gm_usage.py` @ HEAD `ace3ed3` (2026-07-31) — GM_VOCAB lines 66-76, LS_VOCAB
# lines 81-93 — NOT the rest of that 833-line module (session-usage testimony/validation,
# §A subsection vocabulary, history readers: none of it is needed here). This package's own
# convention keeps the Apollo filenames `GOOD-MORNING.md` / `_LIVE-STATE.md` in v0.1
# (ruled — not made configurable), so these patterns are copied byte-for-byte rather than
# re-derived, to guarantee the shim parses the exact same shape `_gen_chain.py` was built
# against.
GM_VOCAB = (
    ("HDR",     None),  # implicit: file start → first explicit marker
    ("LATEST",  re.compile(r"^>\s*##\s*★\s*LATEST\b")),
    ("PRIOR",   re.compile(r"^>\s*##\s*★\s*PRIOR\b")),
    ("DOFIRST", re.compile(r"^##\s*⬛\s*DO TH", re.I)),
    ("A",       re.compile(r"^#\s*§A\b")),
    ("C1",      re.compile(r"^#\s*§C\b|^##\s*1\.\s")),
    ("C2",      re.compile(r"^##\s*2\.\s")),
    ("C4",      re.compile(r"^##\s*4\.\s")),
    ("STRATA",  re.compile(r"^###\s*⏱\s*SESSION STRATA\b", re.I)),
)

LS_VOCAB = (
    ("HDR",       None),
    ("LANES",     re.compile(r"^##\s*🛤")),
    ("SPIN",      re.compile(r"^##\s*🔀")),
    ("DELTAS",    re.compile(r"^##\s*⏱")),   # LATEST/PRIOR/OLDER all merge — one region
    ("WEBFONT",   re.compile(r"^##\s*🕓")),
    ("LIVE",      re.compile(r"^##\s*LIVE\b")),
    ("LIFECYCLE", re.compile(r"^##\s*DECISION-NODE LIFECYCLE\b")),
    ("DEAD",      re.compile(r"^##\s*SUPERSEDED\b")),
    ("OPEN",      re.compile(r"^##\s*OPEN\b")),
    ("TARGETS",   re.compile(r"^##\s*PLANNED\b")),
    ("SPINOFFS",  re.compile(r"^##\s*SPIN-OFF\b")),
)

# ---------------------------------------------------------------------------------------------
# M6 (2026-07-27): a fresh sandbox loses pip state, and tiktoken vanished TWICE inside 24 hours.
# Each time the gate did the honest thing — fell back to bytes/3.53 and SAID so — but a stamp
# measured by estimate is a weaker claim than one measured by the encoder, and nobody noticed
# until the second time. ONE quiet install attempt, at most once per process.
# ⚠ The fallback is NOT touched by this. Auto-heal must never make the estimate path quieter;
# healing is a convenience, the self-description is the contract.
# Ported verbatim, `knowledge/_capture_gate.py` lines 1327-1347.
_TIKTOKEN_HEAL_TRIED = False


def _heal_tiktoken():
    """One `pip install tiktoken` attempt per process. True iff the module imports afterwards.
    Never raises and never prints — a failed heal is a non-event, the fallback covers it.
    `CAPTURE_GATE_NO_HEAL=1` suppresses the attempt; that is how the selftest reaches the
    fallback path on a machine where tiktoken IS installed."""
    global _TIKTOKEN_HEAL_TRIED
    if _TIKTOKEN_HEAL_TRIED or os.environ.get("CAPTURE_GATE_NO_HEAL"):
        return False
    _TIKTOKEN_HEAL_TRIED = True
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "tiktoken",
                        "--break-system-packages", "-q"],
                       capture_output=True, timeout=60)
        importlib.invalidate_caches()
        importlib.import_module("tiktoken")
        return True
    except Exception:
        return False


def measure_tokens(text):
    """Returns (tokens, method). tiktoken when present (OBSERVED); otherwise the MEASURED byte
    divisor, labelled ESTIMATE. Both are declared and they are never silently mixed — a number
    whose method is unstated is the thing this gate exists to prevent.

    Ported verbatim, `knowledge/_capture_gate.py` lines 1350-1374 (including the #59 fix: the
    `get_encoding()` call is guarded too, not just the import — a healthy `import tiktoken`
    followed by a failed cold-cache fetch of the cl100k_base ranks file must fall back to the
    ESTIMATE path, not crash)."""
    try:
        tiktoken = importlib.import_module("tiktoken")
    except Exception:
        if not _heal_tiktoken():
            return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                    f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)")
        tiktoken = importlib.import_module("tiktoken")
    try:
        return len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"
    except Exception:
        return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken installed, encoder unloadable)")


def measurement_degraded():
    """True iff `measure_tokens()` is running on the ESTIMATE fallback right now, rather than
    the real tiktoken encoder. Probes a 1-character string — cheap, and it is the SAME call a
    real measurement makes, so this cannot drift from what a real measurement would report.

    Call this to gate a VERDICT (stale vs. cannot-measure-reliably), never to gate a MEASUREMENT
    itself — a caller that skips measuring because this returned True would just be adding a
    second, undeclared fallback next to the one this file already owns.

    Ported verbatim, `knowledge/_capture_gate.py` lines 1377-1395."""
    return "ESTIMATE" in measure_tokens("x")[1]


def dofirst_index(gm_lines):
    """Compact presence index of every open DO-FIRST item: `(text, how)` or `(None, reason)`.

    ⚠ BOUNDS MAGNITUDE, NOT JUST COUNT — the hook is truncated per item AND the assembled index
    is measured against a ceiling. A count of N is not a measurement of N items.

    ⚠ REFUSES rather than emitting an empty-but-plausible index: a chain that silently reports
    NO open work is worse than one that reports none at all.

    Ported verbatim, `knowledge/_capture_gate.py` lines 1097-1161, with the source's
    `import _gm_usage; _gm_usage.GM_VOCAB` replaced by the local `GM_VOCAB` ported above — same
    data, no module import. Everything else — including the exact refusal wording — is
    unchanged."""
    rx = dict(GM_VOCAB).get("DOFIRST")
    others = [r for k, r in GM_VOCAB if k != "DOFIRST" and r is not None]
    start = next((i for i, ln in enumerate(gm_lines) if rx.match(ln)), None)
    if start is None:
        return None, ("GOOD-MORNING.md has no ⬛ DO THIS FIRST section — presence index NOT built. "
                      "The chain would otherwise tell a cold session there is no open work, which "
                      "is a confident false negative, not a small index.")
    end = next((i for i in range(start + 1, len(gm_lines))
                if any(r.match(gm_lines[i]) for r in others)), len(gm_lines))

    items = []
    for ln in gm_lines[start:end]:
        m = DOFIRST_ITEM_RE.match(ln)
        if not m:
            continue
        num, rest = m.group(1), m.group(2)
        # Hook = the item's own opening clause, to the first em-dash or bold-close, truncated.
        hook = re.split(r"—|\*\*", rest, maxsplit=1)[0]
        hook = re.sub(r"[`*_]", "", hook).strip(" .,:;")
        hook = re.sub(r"\s+", " ", hook)
        if len(hook) > DOFIRST_HOOK_MAX:
            hook = hook[:DOFIRST_HOOK_MAX].rsplit(" ", 1)[0] + "…"
        items.append((num, hook or "(unhooked — see body)"))

    if not items:
        return None, (f"⬛ DO THIS FIRST found at line {start + 1} but ZERO items matched "
                      f"`{DOFIRST_ITEM_RE.pattern}` — presence index NOT built. Either the section "
                      f"is genuinely empty (say so deliberately) or the item form changed and this "
                      f"parser went blind; both are refusals, and a blind parser must never be "
                      f"mistaken for an empty queue.")

    body = " · ".join(f"`{n}` {h}" for n, h in items)
    text = (f"> **⬛ OPEN WORKLIST — PRESENCE INDEX ({len(items)} items, GENERATED). "
            f"Every open item is named; NO bodies are here — `--fetch gm:DOFIRST`.**\n"
            f"> {body}\n"
            f"> **QUEUE — `gm:C1` strands · `gm:C2` ruling batch (Dave's) · `gm:C4` enact-queue.**")
    tk = measure_tokens(text)[0]
    if tk > DOFIRST_INDEX_TK_MAX:
        return None, (f"presence index is {tk:,} tape, over its {DOFIRST_INDEX_TK_MAX:,} ceiling — "
                      f"NOT emitted. This is the bound doing its job: the index sits in the most "
                      f"expensive text in the repo, so it is capped by BYTES and not merely by item "
                      f"count. Shorten the item headings in GOOD-MORNING.md, or raise this ceiling "
                      f"deliberately with a reason — do not let it drift upward silently.")
    return text, f"{len(items)} items, {tk:,} tape (ceiling {DOFIRST_INDEX_TK_MAX:,})"


def chain_parts(repo, gm_lines):
    """The READ CHAIN as **TEXT**: `(gm_part, delta, how)`, or `(None, None, reason)` on refusal.

    ⚠ THIS IS THE ONE SLICER. `read_chain_tk` measures exactly what this returns and
    `_gen_chain.py` writes exactly what this returns, so the chain we measure and the chain
    we hand a cold session cannot describe different text.

    Ported verbatim, `knowledge/_capture_gate.py` lines 1164-1243, with the source's
    `import _gm_usage; _gm_usage.GM_VOCAB / _gm_usage.LS_VOCAB` replaced by the local
    `GM_VOCAB` / `LS_VOCAB` ported above — same data, no module import. Everything else,
    including the exact refusal wording, is unchanged."""

    def _region_end(lines, vocab, start_id):
        """First line index of `start_id`'s marker, and where its region ends — using the SAME
        regexes the vocab tuple defines, but WITHOUT demanding the whole vocabulary validate."""
        rx = dict(vocab).get(start_id)
        if rx is None:
            return None, None
        start = next((i for i, ln in enumerate(lines) if rx.match(ln)), None)
        if start is None:
            return None, None
        others = [r for k, r in vocab if k != start_id and r is not None]
        end = next((i for i in range(start + 1, len(lines))
                    if any(r.match(lines[i]) for r in others)), len(lines))
        return start, end

    # HDR runs file-top → LATEST, and LATEST → the next marker. Contiguous, so one slice carries
    # both: the chain's GM term is "everything above the end of the ★ LATEST banner".
    _s, l_end = _region_end(gm_lines, GM_VOCAB, "LATEST")
    if l_end is None:
        return None, None, ("GOOD-MORNING.md has no ★ LATEST banner — the chain's whole session "
                            "record is that banner, so this is a refusal to measure, not a small chain")
    gm_part = "\n".join(gm_lines[:l_end])

    # The presence index rides INSIDE the one slicer, deliberately — see `dofirst_index`.
    # ⛔ A FAILED INDEX DECLARES ITSELF; IT DOES NOT REFUSE THE CHAIN. A DECLARED gap passes, a
    # SILENT one fails: an unbuildable index emits a LOUD line saying the worklist is
    # unrepresented, rather than silently dropping it or refusing the whole chain.
    idx, idx_how = dofirst_index(gm_lines)
    gm_part = gm_part + "\n" + (idx if idx is not None else (
        "> ⚠ **PRESENCE INDEX UNAVAILABLE — the open worklist is NOT represented in this chain.** "
        f"{idx_how} ⇒ retrieve `gm:DOFIRST` by hand; do NOT read this chain as evidence that "
        "there is no open work."))

    ls_path = os.path.join(repo, "_LIVE-STATE.md")
    if not os.path.exists(ls_path):
        return gm_part, None, "_LIVE-STATE absent (no delta term)"
    with open(ls_path, encoding="utf-8") as f:
        ls_lines = f.read().splitlines()
    d_s, d_e = _region_end(ls_lines, LS_VOCAB, "DELTAS")
    if d_s is None:
        return None, None, "_LIVE-STATE.md has no ⏱ delta section — chain UNMEASURED, not assumed zero"
    body = ls_lines[d_s:d_e]
    # The LATEST delta ends where the next ⏱ heading begins. If there is no second one, the
    # whole section IS the latest delta — say which case was taken, never silently assume.
    nxt = next((i for i, ln in enumerate(body) if i > 0 and LS_DELTA_RE.match(ln)), None)
    delta = "\n".join(body[:nxt] if nxt else body)
    how = f"LATEST delta only (of {len(body)} delta lines)" if nxt else "whole ⏱ section (single delta)"
    return gm_part, delta, how


def read_chain_tk(repo, gm_lines):
    """Measure the READ CHAIN: GM header + ★ LATEST banner + the `_LIVE-STATE.md` LATEST delta.
    Returns `(chain_tk, detail)`; `(None, reason)` if a region cannot be isolated.

    ⚠ It REFUSES rather than guesses. Every failure path returns a REASON, never a number and
    never a zero: a budget check that defaults to 0 on a parse failure reports GREEN on a
    broken file, which is the "cheerful zero" failure class.

    Ported verbatim, `knowledge/_capture_gate.py` lines 1246-1267."""
    gm_part, delta, how = chain_parts(repo, gm_lines)
    if gm_part is None:
        return None, how
    gm_tk = measure_tokens(gm_part)[0]
    if delta is None:
        return gm_tk, f"GM header+LATEST {gm_tk} tk · {how}"
    d_tk = measure_tokens(delta)[0]
    return gm_tk + d_tk, f"GM header+LATEST {gm_tk} tk · LS {how} {d_tk} tk"
