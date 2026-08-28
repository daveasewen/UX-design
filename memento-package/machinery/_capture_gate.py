#!/usr/bin/env python3
"""_capture_gate shim — lets the verbatim `_gen_chain.py` in this folder run standalone.

WHAT THIS IS. `_gen_chain.py` (copied verbatim into this package) does `import _capture_gate as
cg` and calls exactly four of its functions: `cg.chain_parts`, `cg.measure_tokens`,
`cg.measurement_degraded`, `cg.read_chain_tk`. The real `knowledge/_capture_gate.py` is ~2,500
Apollo-laced lines (provenance/status gates, section-size budgets, band arithmetic, etc.) that
`_gen_chain.py` never touches. This module is NOT a copy of that file — it is a small, standalone
module that reproduces the behaviour of those four functions and nothing else, so the package
does not have to drag Apollo's gate machinery along for the ride.

PROVENANCE. Ported from `knowledge/_capture_gate.py` @ HEAD `ba2c9f5` (2026-08-28, that file's own
last touch), these names — ⚠ names, not line ranges: the source file has grown well past 4,000
lines since the first port, so its line numbers no longer address the right text and the
delta-audit gate addresses everything BY NAME (AST source-segment hashing):
  - `chain_parts`            (re-ported #149 @ `9dcf62d`; was `91d7528`)
  - `read_chain_tk`          (unchanged since `91d7528`)
  - `measure_tokens`         ★ RE-PORTED #114 — the #82-D1 three-tier cascade (real → cl100k →
                             ESTIMATE) plus `_TIERS_SEEN` bookkeeping; see its own docstring for
                             the one DECLARED difference (optional `_gauge_tokens` import)
  - `measurement_degraded`   ★ RE-PORTED #114 — now `_tier_probe() == "estimate"`; MEANING
                             unchanged on purpose (still "is this a GUESS?", not "is this REAL?")
  - `measurement_tier`       ★ PORTED #219 — `_gen_chain.py` has CALLED this since the #193
                             re-sync and the shim did not have it, so the packaged chain
                             generator died on `AttributeError` the moment it reached
                             `unit_word()`. Found by RUNNING the packaged generator in a staged
                             pack, not by reading either file
                             [[mutation-tests-the-clause-not-the-feature]]
  - `dofirst_index`          (unchanged since `91d7528`; helper `chain_parts` calls internally)
  - `_heal_tiktoken`         (unchanged since `91d7528`; helper `measure_tokens` calls internally)
  - `_TIKTOKEN_HEAL_TRIED`   (unchanged since `91d7528`)
  - `BYTES_PER_TOKEN`        (unchanged since `91d7528`)
  - `DOFIRST_ITEM_RE` / `DOFIRST_HOOK_MAX` / `DOFIRST_INDEX_TK_MAX`  — ★ `DOFIRST_INDEX_TK_MAX`
                             RE-PORTED #114 at its source VALUE **700** (raised in the source
                             after the first port; the value is Dave's, #111-D4, and is the same
                             700 on both sides — this port carries it, it does not set it)
  - `LS_DELTA_RE`            (unchanged since `91d7528`)
  Two names introduced by the re-port and ported with it: `_REAL_TIER_ENV` / `_TIERS_SEEN`, and
  the helpers `_tier_of` / `_tier_probe` that `measurement_degraded` now reads through.

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
  - the cascade is three-tier since #82-D1 (REAL Claude tokens where a gauge is reachable, then
    tiktoken, then the byte divisor) and every tier LABELS itself; inside this package the real
    tier is normally unreachable (`_gauge_tokens` is not shipped), so the effective cascade is
    tiktoken → ESTIMATE — which is exactly what the source does when the gauge reaches nothing.
    tiktoken (`cl100k_base`) is the instrument when it is importable and its encoding file
    loads; the byte-divisor fallback (`BYTES_PER_TOKEN = 3.53`) is used ONLY when tiktoken is
    absent or its encoder is unloadable, and it labels itself "ESTIMATE" rather than passing
    silently as a real measurement.
  - `measurement_degraded()` asks the SAME `measure_tokens()` call path a real measurement would
    use (a 1-character probe) rather than a second, hand-rolled health check — so it cannot drift
    from what an actual measurement would report.
  - `chain_parts` / `dofirst_index` REFUSE (return `None` + a reason) rather than emit a
    confident-but-empty chain or worklist index on any parse failure — a declared gap, never a
    silent one.

ONE THING HERE IS NOT A PORT, AND SAYS SO (`s222-D2`, #222). Immediately below the imports there
is a small bootstrap that points `TIKTOKEN_CACHE_DIR` at the encoder data VENDORED INSIDE THE
PACK, through the single helper `_encoder_home.py`. It is pack-only wiring, not ported
behaviour: it changes no tier, no label and no refusal — it only makes the `cl100k_base` tier
REACHABLE on a machine that cannot download anything. The block declares all of this in place.
"""
import importlib
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------------------------
# s222-D2 — THE PACK MEASURES TOKENS OUT OF THE BOX. Dave, #222, off the first live
# Copilot-bridge session: the chain inscription refused because tiktoken could not FETCH its
# encoding file from `openaipublic.blob.core.windows.net`. The refusal was right; needing a
# reachable blob host was not. The encoding data now SHIPS INSIDE THE PACK, and exactly one
# helper knows where — `_encoder_home.py`, beside this file. This block is the only place in
# this module that calls it, and it runs before anything below asks for an encoder.
#
# ⛔ IT ADDS NOTHING TO A MEASUREMENT AND SUBTRACTS NOTHING FROM A REFUSAL. All it does is
# `os.environ.setdefault("TIKTOKEN_CACHE_DIR", …)` — so a designer's own value still wins. If
# the vendored data is missing or the wrong size, `_encoder_home` says so LOUD and BY NAME on
# stderr, `measure_tokens` falls to the SAME self-labelling ESTIMATE tier it falls to today,
# and `_gen_chain.py` refuses to write a chain on an estimate exactly as it does today. The
# no-estimate principle is untouched: this makes the real measurement REACHABLE, never quieter.
#
# ⚠ DECLARED, FOR THE DELTA-AUDIT GATE: this is NOT a ported name. Every function and constant
# this shim declares as ported from `knowledge/_capture_gate.py` is addressed by the gate BY
# NAME and is byte-identical to its source; `_ENCODER_HOME_*` is pack-only wiring, which is
# precisely what a purpose-written shim is for. Nothing ported was edited to add it.
#
# ⚠ THE IMPORT IS OPTIONAL BY DESIGN, NOT BY CARELESSNESS. This file has two homes: the PACK,
# where `_encoder_home.py` and `_encoder-cache/` ride beside it, and the source repo, where
# neither does (Apollo measures through its own gauge). A hard import would make the repo copy
# UNIMPORTABLE — shipping an unimportable machinery file is the v1.0.0 defect this release
# shape exists to end. Absence is not silence: `_ENCODER_HOME_NOTE` records exactly what
# happened and `encoder_home_note()` states it, and every tier below still labels itself.
_ENCODER_HOME_OK = False
_ENCODER_HOME_NOTE = "not attempted"
try:
    import importlib.util as _ehu
    # ⚠ TWO COPIES OF THIS SHIM SHIP, AT DIFFERENT DEPTHS, AND THERE IS ONLY ONE HELPER.
    # `memento-package/machinery/` has it as a sibling; `memento-package/claude-plugin/memento/
    # machinery/` does not — the helper is not duplicated into the plugin, because two copies of
    # a path-resolver is the drift class this package argues against everywhere else. So look
    # for it beside this file AND under `machinery/` of every ancestor, which reaches the one
    # copy from both homes. ⬛ DECLARED: a plugin EXTRACTED on its own, away from the pack, has
    # no helper and no `_encoder-cache/` above it — it degrades loudly through the same named
    # path below, exactly as this shim did before `s222-D2`.
    _eh_d = os.path.dirname(os.path.abspath(__file__))
    _eh_path, _eh_tried = None, []
    while True:
        for _c in (os.path.join(_eh_d, "_encoder_home.py"),
                   os.path.join(_eh_d, "machinery", "_encoder_home.py")):
            _eh_tried.append(_c)
            if _eh_path is None and os.path.isfile(_c):
                _eh_path = _c
        _eh_up = os.path.dirname(_eh_d)
        if _eh_path is not None or _eh_up == _eh_d:
            break
        _eh_d = _eh_up
    if _eh_path is None:
        raise ImportError("no _encoder_home.py at any of: %s" % ", ".join(_eh_tried))
    _eh_spec = _ehu.spec_from_file_location("_encoder_home", _eh_path)
    if _eh_spec is None:
        raise ImportError("no module spec at %s" % _eh_path)
    _eh_mod = _ehu.module_from_spec(_eh_spec)
    _eh_spec.loader.exec_module(_eh_mod)
    _ENCODER_HOME_OK, _ENCODER_HOME_NOTE = _eh_mod.ensure()
except Exception as _eh_ex:                       # noqa: BLE001 — the reason is kept, not eaten
    _ENCODER_HOME_NOTE = (
        "no `_encoder_home.py` beside this file (%s: %s) — this copy of the shim resolves no "
        "vendored encoder data, and token measurement uses whatever tiktoken can reach on its "
        "own. In the released pack the helper and `_encoder-cache/` ride beside this file."
        % (type(_eh_ex).__name__, _eh_ex))


def encoder_home_note():
    """What the vendored-encoder bootstrap did in THIS process, as a sentence.

    ★ Exists so that a reader of a refusal can be told which encoder path was tried without
    having to read this module. A state nobody can ask about is a state nobody will check."""
    return _ENCODER_HOME_NOTE


def encoder_home_module():
    """The `_encoder_home` module this file's bootstrap loaded, or None when it found none.

    ⚠ A READ of what the bootstrap already did — it never imports, never searches, never
    falls back. Apollo's own tree carries no `_encoder_home.py` above `knowledge/`, so
    `_eh_mod` is never bound there, this returns None, and the measurement cascade below is
    byte-for-byte the behaviour it had before `s222-D3`. In the released pack the bootstrap
    DOES bind it, and `measure_tokens` can reach the pack's own exact encoder."""
    return globals().get("_eh_mod")


# ---------------------------------------------------------------------------------------------
# ds-021 / M6 — THE ONE UNIT AND THE HONEST FALLBACK.
# Ported verbatim, `knowledge/_capture_gate.py` line 361.
BYTES_PER_TOKEN = 3.53     # MEASURED on GM, tiktoken cl100k_base, 2026-07-27. NOT the chars/4 rule.

# ---------------------------------------------------------------------------------------------
# THE PRESENCE-INDEX CONSTANTS. Ported verbatim, `knowledge/_capture_gate.py` lines 1092-1094.
DOFIRST_ITEM_RE = re.compile(r"^>\s*\*\*(\d+[a-z]?)\.\s*(.+)$")
DOFIRST_HOOK_MAX = 46            # chars per hook — a BYTE bound, deliberately
DOFIRST_INDEX_TK_MAX = 700       # ⚠ the whole index, MEASURED — see below

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


# ---------------------------------------------------------------------------------------------
# THE TIER VOCABULARY (#82-D1 in the source). Ported with the three-tier cascade below.
_REAL_TIER_ENV = "CAPTURE_GATE_NO_REAL"   # set to force the pre-#82 cascade (selftests use it)
_TIERS_SEEN = set()                       # every tier this PROCESS has actually measured with


def _real_gauge():
    """The source's REAL tier comes from `import _gauge_tokens as gauge` — a `knowledge/` module
    that is NOT in this package and is not going to be (it is Apollo-side budget machinery; see
    LEFT BEHIND in the module docstring). The source's own cascade already treats an unreachable
    real tier as "fall through to tiktoken, labelled", so the honest port is an OPTIONAL import:
    where `_gauge_tokens` is importable the shim behaves exactly like the source; where it is
    not — the normal case inside this package — the cascade is tiktoken → ESTIMATE, which is
    precisely the source's own behaviour when `gauge.count()` cannot reach anything. No tier is
    ever returned unlabelled on either path."""
    try:
        return importlib.import_module("_gauge_tokens")
    except Exception:
        return None


def _tier_of(method):
    """The TIER a method string belongs to: `'real'` · `'cl100k'` · `'estimate'`. ONE place,
    because two readers of one vocabulary is the drift class this entire file argues against.

    Ported verbatim, `knowledge/_capture_gate.py` `_tier_of`."""
    if method == "real":
        return "real"
    return "estimate" if "ESTIMATE" in method else "cl100k"


def measure_tokens(text):
    """Returns (tokens, method). REAL Claude tokens when reachable (#82-D1, Dave's); otherwise
    tiktoken when present (OBSERVED); otherwise — `s222-D3` — the pack's OWN exact cl100k
    engine over its vendored data, which names itself; otherwise the MEASURED byte divisor,
    labelled ESTIMATE. Every tier is declared and they are never silently mixed — a number
    whose method is unstated is the thing this gate exists to prevent.

    Ported from `knowledge/_capture_gate.py`'s `measure_tokens` (including the #59 fix: the
    `get_encoding()` call is guarded too, not just the import — a healthy `import tiktoken`
    followed by a failed cold-cache fetch of the cl100k_base ranks file must fall back to the
    ESTIMATE path, not crash). The one DECLARED difference from the source: the real tier is
    reached through `_real_gauge()` (optional import) rather than a hard module-level
    `import _gauge_tokens`, because that module is deliberately not shipped here — see
    `_real_gauge`'s docstring."""
    # ---- #82-D1: the REAL tier. ⚠ `count()` raises when it can reach NOTHING, and that is not
    # this function's failure to report: control falls into the cascade below, which labels
    # itself. Never to silence — there is no path here that returns an unlabelled number.
    if not os.environ.get(_REAL_TIER_ENV):
        gauge = _real_gauge()
        if gauge is not None:
            try:
                n, how = gauge.count(text)
                if how == "real":
                    _TIERS_SEEN.add("real")
                    return n, "real"
            except Exception:
                pass
    try:
        tiktoken = importlib.import_module("tiktoken")
    except Exception:
        if not _heal_tiktoken():
            # ---- s222-D3: the PACK'S OWN EXACT ENGINE, before any estimate. Same vendored
            # cl100k data, real pretokenizer + merges, equality-gated against tiktoken. It
            # NAMES ITSELF (`purepy cl100k_base (exact, equality-gated)`) — never borrows the
            # library's label, because a fallback wearing the real library's name is a silent
            # fallback. This is the cl100k TIER, not a new one: the numbers are byte-identical
            # by construction and by gate, so a chain stamped by one engine still byte-matches
            # a check by the other. Nothing here can return an unlabelled number.
            _eh = encoder_home_module()
            if _eh is not None:
                try:
                    _n, _which = _eh.count(text)
                    _TIERS_SEEN.add("cl100k")
                    return _n, _which
                except Exception:
                    pass
            _TIERS_SEEN.add("estimate")
            return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                    f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)")
        tiktoken = importlib.import_module("tiktoken")
    try:
        out = len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"
    except Exception:
        _TIERS_SEEN.add("estimate")
        return (int(len(text.encode("utf-8")) / BYTES_PER_TOKEN),
                f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken installed, encoder unloadable)")
    _TIERS_SEEN.add("cl100k")
    return out


def _tier_probe():
    """The tier a measurement taken RIGHT NOW would use — WITHOUT recording it.

    ★ The snapshot/restore is the point. A health probe is not a measurement, and a probe that
    wrote into `_TIERS_SEEN` would let a mixed-tier check fire on its own footprint — an
    instrument manufacturing the very condition it reports.

    Ported verbatim, `knowledge/_capture_gate.py` `_tier_probe`."""
    snapshot = set(_TIERS_SEEN)
    try:
        return _tier_of(measure_tokens("x")[1])
    finally:
        _TIERS_SEEN.clear()
        _TIERS_SEEN.update(snapshot)


def measurement_tier():
    """`'real'` · `'cl100k'` · `'estimate'` — what a measurement taken now would be. ★ THIS is
    the word the vocabulary lacked (#80's root cause, confirmed at source #81): the reason a
    RULED unit sat unenacted for 26 sessions was that no function in this file could SAY 'real',
    so `measurement_degraded()` asked *'is this an estimate?'* and cl100k answered *no, healthy*.
    A stamp that names its tier can be checked; one that cannot, cannot.

    Ported verbatim, `knowledge/_capture_gate.py` `measurement_tier`."""
    return _tier_probe()


def measurement_degraded():
    """True iff `measure_tokens()` is running on the ESTIMATE fallback right now, rather than
    a real encoder. Probes a 1-character string — cheap, and it is the SAME call a real
    measurement makes, so this cannot drift from what a real measurement would report.

    Call this to gate a VERDICT (stale vs. cannot-measure-reliably), never to gate a MEASUREMENT
    itself — a caller that skips measuring because this returned True would just be adding a
    second, undeclared fallback next to the one this file already owns.

    ⛔ #82-D1 — ITS MEANING IS UNCHANGED ON PURPOSE. It still asks *"is this reading a GUESS?"*,
    NOT *"is this reading REAL?"*. Widening it to mean 'not real' would turn `_gen_chain.py`'s
    refusal into an offline build-killer.

    Ported verbatim, `knowledge/_capture_gate.py` `measurement_degraded`."""
    return _tier_probe() == "estimate"


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

    # ★ s125-D1 (Dave, RULED #125, ENACTED #126) — THE BUILD-STEP FIGURE IS SUBSTITUTED **HERE**,
    # inside the ONE SLICER, for the identical reason the presence index is composed here and not
    # in the generator: `read_chain_tk` measures exactly what this function returns and
    # `_gen_chain.py` writes exactly what it returns. Text injected in the generator would be
    # WRITTEN BUT NOT MEASURED — the second-consumer drift #41 extracted this function to make
    # impossible. The AST READER lives in `_gen_chain.py`, as the ruling names; only the splice is
    # here. [[instruction-right-cause-wrong]]
    # ⛔ A FAILED SUBSTITUTION DECLARES ITSELF AND DOES NOT REFUSE THE CHAIN — same posture as the
    # index directly above, and for the same reason: the chain depends on ★ LATEST and ⏱ DELTAS,
    # and nothing else may break it. A DECLARED gap passes; a SILENT one fails.
    if "{{BUILD_VERDICT}}" in gm_part:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import _gen_chain
            _verdict = _gen_chain.build_verdict_line(repo)
        except Exception as e:                                # pragma: no cover - import guard
            _verdict = ("⛔ **BUILD VERDICT: NOT RENDERED** — the generated step figure could not "
                        f"be produced ({e}). This is a REFUSAL, not a green build.")
        gm_part = gm_part.replace("{{BUILD_VERDICT}}", _verdict)

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
