#!/usr/bin/env python3
"""Doc-gardener (B1) — RULED s179-D1 (Dave, #179), built #179 as an arm of the dream-pass.

WHO CONSUMES THIS, NAMED BEFORE THE BUILD (P15, and the ~65-session lesson of
`_surface_recorder.py` — an instrument nobody read):

  1. THE REVIEW-QUEUE CONTROLLER (brief §3c-②, the priority build per the #179 promotion
     probe). It renders `notes/_dream/_GARDENER-QUEUE.json` as one card per item —
     canon quote · evidence quote · probe · [accept / flag / reject] — and compiles the
     clicks into ONE ruling message. THE SCHEMA BELOW IS THAT CONTROLLER'S INPUT CONTRACT.
  2. THE DREAM-PASS LANE (`knowledge/_RUNBOOK-dream-pass.md`). The gardener runs as its
     FINDINGS arm, same cadence, same governance. Its pass receipt is the dream-pass's.
  3. B3's REFRESH ARM (not built — see `refresh_arm()`, which REFUSES rather than pretends).

WHAT IT DOES. Sweeps a MODEST, RESOLVABLE target list of runbooks + canon docs for claims
the repo contradicts, and files them as a machine-readable queue. It does not garden prose,
it does not summarise, it does not judge. It mechanises VERIFICATION, never JUDGMENT.

★ THE THREE-TIER MODEL (brief §3b). AMBIGUITY RESOLVES UPWARD, always.
    Tier 1 — MECHANICAL pointer rot. Auto-applicable ONLY under the narrow s179-D1
             carve-out and ONLY when ALL FOUR machine conditions hold:
               (1) the claim is a POINTER — not a measurement, not a ruling, not prose;
               (2) the old target is PROVABLY ABSENT;
               (3) the new target is PROVABLY PRESENT and UNAMBIGUOUS (exactly one);
               (4) the git blob hash of the old path at its deletion commit EQUALS the
                   hash of the candidate — the thing MOVED, it did not CHANGE.
             Every repair writes a REGISTER entry (before/after/probe/hash) FIRST, and is
             reversible via git. ANY condition unmet or unprovable ⇒ NOT Tier 1 (P19).
    Tier 2 — FACTUAL DRIFT. Machine quotes both sides; Dave rules in one line.
             ⛔ NEVER auto-applied. A "corrected" ruled datapoint is the boot-floor-band
             defect generalised — that is why this path has no apply code at all.
    Tier 3 — MEANING. Never mechanised. Full finding, Dave's eyes.

★ EVERY FENCE IS A BLOCK, NOT A WARN. There is no WARN state in this module.
    P4  write outside the allowed set               → GardenerBlock, exit nonzero
    P5  finding missing any of the three legs       → finding REFUSED (never filed)
    P6  findings > N (=10, s179-D1)                 → truncate, truncation DECLARED in-file
    P7  finding against a ratified record           → flag_only=true, set MECHANICALLY
    P8  target list does not resolve                → LOUD exit nonzero, NOTHING filed
    P19 auto-apply failing ANY Tier-1 condition     → BLOCK (resolves upward instead)
    P20 Tier-1 repair with no register entry        → BLOCK (register is written FIRST)
    P22 proposal arm generating while queue > Q=15  → BLOCK: arm PAUSES, refresh continues

⚠ DECLARED SCOPE CONFLICT, NOT PAPERED OVER. Brief §3 fence 1 permits the Tier-1 carve-out
  to repair a pointer IN PLACE (a third write target); the #179 lane brief states the sole
  targets are the queue file and the register. Ambiguity resolves UPWARD: by DEFAULT this
  module writes ONLY those two files and records Tier-1 candidates as PENDING. In-place
  repair happens only under the explicit `--apply-tier1` flag, only into a file on the
  resolved target list, and only after its register entry is on disk. Absent Dave's word on
  the narrower reading, the default never touches canon.

⛔ NEVER WRITES: memory files (read-only sweep scope — the #80 class), GOOD-MORNING.md,
  _CHAIN.md, _LIVE-STATE.md, anything outside `notes/_dream/` (see WRITE FENCE below).
⛔ This module never invokes `knowledge/_build_all.py` and never commits.

CLI
    _gardener.py --sweep                  # real pass: self-check, sweep, file the queue
    _gardener.py --sweep --dry-run        # sweep + print receipt, file nothing
    _gardener.py --sweep --apply-tier1    # additionally apply Tier-1 repairs (register first)
    _gardener.py --selftest               # the five mutation tests, plant-then-detect
    _gardener.py --show                   # print the current queue receipt
Optional: --root DIR (fixture repo, used by --selftest), --cap N, --queue-cap Q.
Exit 0 = clean. Nonzero = a fence bit, or the self-check refused. Nothing is ever filed on
a nonzero exit."""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# ── s179-D1 constants. NOT tunable prose — Dave's numbers. ────────────────────────────────
CAP_N = 10          # findings per pass (s179-D1 clause 2)
QUEUE_CAP_Q = 15    # backpressure cap (s179-D1 clause 3)

SCHEMA_ID = "gardener-queue/1"

# ── THE TARGET LIST. Modest and resolvable by construction (P8 self-check runs FIRST). ────
# Groups exist so a group can be absent-but-declared rather than silently skipped.
TARGET_GLOBS = [
    "knowledge/_RUNBOOK-*.md",
    "knowledge/_RUNBOOKS.md",
]
TARGET_FILES = [
    "AGENTS.md",
    "MODEL-ROUTING.md",
    "_STANDARDS.md",
    "_HOW-TO-RUN-SESSIONS.md",
    "knowledge/README.md",
]
# Ratified records: findings against these are FLAG-ONLY, mechanically (P7).
RATIFIED_GLOBS = ["docs/decisions/ADR-*.md"]
RATIFIED_PREFIXES = ("docs/decisions/", "_DECISION-HISTORY/")

# Read-only sweep extras (never a write target under ANY flag): the memory store, whose
# hooks name moved/absent files — the #80 class the brief §3 fence 5 puts in scope.
MEMORY_DIRS = [
    os.path.abspath(os.path.join(REPO, "..", ".auto-memory")),
]

QUEUE_BASENAME = "_GARDENER-QUEUE.json"
REGISTER_BASENAME = "_GARDENER-REGISTER.jsonl"
OUT_DIRNAME = os.path.join("notes", "_dream")


class GardenerBlock(RuntimeError):
    """A fence bit. Never caught to continue — only to report and exit nonzero."""


def _die(code: int, *lines: str) -> None:
    """Fail LOUD and NAMED. Nothing is filed after this point."""
    print("", file=sys.stderr)
    print("⛔ GARDENER BLOCKED — nothing filed.", file=sys.stderr)
    for ln in lines:
        print(f"   {ln}", file=sys.stderr)
    sys.exit(code)


# ══ WRITE FENCE (P4) ══════════════════════════════════════════════════════════════════════
class WriteFence:
    """The ONLY door to the filesystem. Every write in this module goes through `write()`.

    Allowed, and nothing else:
      · <root>/notes/_dream/_GARDENER-QUEUE.json      (the proposals/queue file)
      · <root>/notes/_dream/_GARDENER-REGISTER.jsonl  (the Tier-1 register)
      · a file on the RESOLVED TARGET LIST — only when apply_tier1 is True.
    """

    def __init__(self, root: str, targets: list[str], apply_tier1: bool):
        self.root = os.path.abspath(root)
        self.out_dir = os.path.join(self.root, OUT_DIRNAME)
        self.queue_path = os.path.join(self.out_dir, QUEUE_BASENAME)
        self.register_path = os.path.join(self.out_dir, REGISTER_BASENAME)
        self.apply_tier1 = apply_tier1
        self._targets = {os.path.abspath(p) for p in targets}
        self.writes: list[str] = []

    def check(self, path: str) -> str:
        p = os.path.abspath(path)
        if p in (self.queue_path, self.register_path):
            return p
        if self.apply_tier1 and p in self._targets:
            return p
        raise GardenerBlock(
            "P4 FILE-ONLY fence: refused write to a path outside the allowed set.\n"
            f"        attempted : {p}\n"
            f"        allowed   : {self.queue_path}\n"
            f"                    {self.register_path}\n"
            + ("                    + resolved target list (--apply-tier1)\n"
               if self.apply_tier1 else
               "        (--apply-tier1 not given, so canon is not writable at all)\n")
        )

    def write(self, path: str, text: str) -> None:
        p = self.check(path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        self.writes.append(p)

    def append(self, path: str, text: str) -> None:
        p = self.check(path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(text)
        self.writes.append(p)


# ══ TARGET RESOLUTION + SELF-CHECK (P8 — the FIRST act of every run) ══════════════════════
def resolve_targets(root: str) -> tuple[list[str], list[str]]:
    """Return (resolved absolute paths, unresolvable descriptions). Never guesses."""
    import glob as _glob
    resolved: list[str] = []
    unresolved: list[str] = []
    for g in TARGET_GLOBS:
        hits = sorted(_glob.glob(os.path.join(root, g)))
        if not hits:
            unresolved.append(f"glob matched NOTHING: {g}")
        resolved.extend(hits)
    for f in TARGET_FILES:
        p = os.path.join(root, f)
        if os.path.isfile(p):
            resolved.append(p)
        else:
            unresolved.append(f"file MISSING: {f}")
    for g in RATIFIED_GLOBS:
        resolved.extend(sorted(_glob.glob(os.path.join(root, g))))
    # dedupe, stable
    seen, out = set(), []
    for p in resolved:
        a = os.path.abspath(p)
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out, unresolved


def self_check(root: str) -> list[str]:
    """P8. Runs before anything is read for content and before ANY write is opened."""
    targets, unresolved = resolve_targets(root)
    if unresolved:
        _die(2,
             "P8 SELF-CHECK FAILED — the gardener's own target list does not resolve.",
             f"root: {root}",
             *[f"· {u}" for u in unresolved],
             "REFUSING TO GUESS a replacement target. Fix the target list in "
             "knowledge/_gardener.py (TARGET_GLOBS / TARGET_FILES) and re-run.")
    if not targets:
        _die(2, "P8 SELF-CHECK FAILED — target list resolved to zero files.", f"root: {root}")
    return targets


# ══ REPO INDEX ════════════════════════════════════════════════════════════════════════════
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}


def build_index(root: str, extra_dirs: list[str]) -> tuple[dict[str, list[str]], set[str]]:
    """basename → [repo-relative paths], plus the set of all repo-relative paths."""
    by_base: dict[str, list[str]] = {}
    rels: set[str] = set()
    roots = [(root, root)] + [(d, d) for d in extra_dirs if os.path.isdir(d)]
    for base_root, walk_root in roots:
        for dirpath, dirnames, filenames in os.walk(walk_root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, base_root)
                rels.add(rel)
                by_base.setdefault(fn, []).append(rel)
    return by_base, rels


# ══ CLAIM EXTRACTION ══════════════════════════════════════════════════════════════════════
BACKTICK = re.compile(r"`([^`\n]{2,120})`")
EXTS = (".md", ".py", ".json", ".css", ".html", ".js", ".svg", ".yml", ".yaml", ".jsonl")
# Lines that are measurements, rulings or prose-about-meaning can never be Tier 1 (cond. 1).
NOT_A_POINTER_LINE = re.compile(
    r"(s\d+-D\d+|\bRULED\b|\bmeasured\b|\bbytes\b|\btokens\b|≈|\bmeans\b|\bwhy\b)",
    re.IGNORECASE)
BYTES_CLAIM = re.compile(r"([\d][\d,]{2,})\s*bytes", re.IGNORECASE)


def looks_like_path(tok: str) -> bool:
    if any(c in tok for c in " \t*<>?|…"):
        return False
    if tok.startswith("/"):
        return False        # absolute paths (e.g. /var/tmp/…) are runtime, not repo pointers
    if tok.startswith("."):
        return False        # bare extensions and dotfile fragments are not pointers
    if tok.startswith("-") or "--" in tok:
        return False
    if not re.fullmatch(r"[A-Za-z0-9._/#-]+", tok):
        return False
    if "YYYY" in tok or "MM-DD" in tok or "<n>" in tok:
        return False
    if not tok.lower().endswith(EXTS):
        return False
    return True


def resolve_pointer(tok: str, root: str, by_base: dict, rels: set,
                    doc_dir: str = "") -> tuple[bool, list[str]]:
    """(resolves?, candidate repo-relative paths sharing the basename).

    TWO legal resolution roots, and no others: the repo root, and the DOCUMENT'S OWN
    DIRECTORY. The second is not a guess — `knowledge/_RUNBOOKS.md` writing `canon/canon.css`
    is a doc-relative pointer that resolves; calling it rot would file ~14 false cards into
    Dave's queue on the first real pass (measured #179, before this clause existed).
    """
    clean = tok.lstrip("./")
    if clean in rels or os.path.isfile(os.path.join(root, clean)):
        return True, []
    if doc_dir and os.path.isfile(os.path.join(root, doc_dir, clean)):
        return True, []
    base = os.path.basename(clean)
    cands = by_base.get(base, [])
    if "/" not in clean and cands:
        # a bare filename that exists SOMEWHERE resolves — it names a file, not a location
        return True, cands
    return False, cands


# ══ FINDINGS ══════════════════════════════════════════════════════════════════════════════
def _stars(text: str) -> int:
    return text.count("★")


def _is_ratified(rel: str) -> bool:
    return rel.startswith(RATIFIED_PREFIXES)


def _git(root: str, *args: str) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    except FileNotFoundError:
        return 127, ""
    return r.returncode, r.stdout.strip()


def tier1_hash_probe(root: str, old_rel: str, new_rel: str) -> tuple[bool, dict]:
    """Condition 4: did it MOVE, or did it CHANGE? Answered by git blob hashes, never guessed."""
    ev = {"probe": f"git log --diff-filter=D -1 -- {old_rel} ; git rev-parse <sha>^:{old_rel} ; "
                   f"git hash-object {new_rel}"}
    rc, sha = _git(root, "log", "--format=%H", "--diff-filter=D", "-1", "--", old_rel)
    if rc != 0 or not sha:
        ev["result"] = "UNPROVABLE — no deletion commit for the old path in git history"
        return False, ev
    rc, old_blob = _git(root, "rev-parse", f"{sha}^:{old_rel}")
    if rc != 0 or not old_blob:
        ev["result"] = "UNPROVABLE — old blob not retrievable at the deletion commit's parent"
        return False, ev
    rc, new_blob = _git(root, "hash-object", os.path.join(root, new_rel))
    if rc != 0 or not new_blob:
        ev["result"] = "UNPROVABLE — could not hash the candidate"
        return False, ev
    ev["old_blob"] = old_blob
    ev["new_blob"] = new_blob
    ev["deletion_commit"] = sha
    ev["result"] = "MATCH — moved, not changed" if old_blob == new_blob else \
                   "MISMATCH — the file moved AND changed"
    return old_blob == new_blob, ev


def classify(finding: dict, root: str) -> dict:
    """Three-tier classifier. AMBIGUITY RESOLVES UPWARD (brief §3b, P19)."""
    reasons: list[str] = []
    if finding["detector"] == "byte-figure":
        finding["tier"] = 2
        finding["tier_reason"] = ("a stated FIGURE is a measurement, never a pointer — "
                                  "Tier 2 by construction, never auto-applied")
        finding["disposition"] = "UPDATE-OR-FLAG"
        return finding

    line = finding["canon"]["quote"]
    cands = finding.get("_candidates") or []

    c1 = not NOT_A_POINTER_LINE.search(line)
    if not c1:
        reasons.append("cond1 FAIL: the line carries a ruling/measurement/meaning marker")
    c2 = True  # established by construction: the finding exists because the path is absent
    c3 = len(cands) == 1
    if not c3:
        reasons.append(f"cond3 FAIL: new target not unambiguous ({len(cands)} candidates)")
    c4 = False
    hash_ev: dict = {"probe": "not run — earlier condition already failed"}
    if c1 and c3:
        c4, hash_ev = tier1_hash_probe(root, finding["_token_rel"], cands[0])
        if not c4:
            reasons.append(f"cond4 FAIL: {hash_ev.get('result')}")
    finding["tier1_conditions"] = {"c1_is_pointer": c1, "c2_old_absent": c2,
                                   "c3_new_present_unique": c3, "c4_hash_match": c4}
    finding["tier1_hash_probe"] = hash_ev

    if c1 and c2 and c3 and c4:
        finding["tier"] = 1
        finding["tier_reason"] = "all four s179-D1 machine conditions hold — moved, not changed"
        finding["disposition"] = "AUTO-APPLY-PENDING"
        finding["proposed"] = {"before": finding["_token"], "after": cands[0]}
    else:
        # UPWARD. A pointer touching a ruling line is meaning; anything else is drift.
        if not c1:
            finding["tier"] = 3
            finding["disposition"] = "DAVE-ONLY"
        else:
            finding["tier"] = 2
            finding["disposition"] = "UPDATE-OR-FLAG"
            if cands:
                finding["proposed"] = {"before": finding["_token"], "after": cands[0]}
        finding["tier_reason"] = "NOT Tier 1 — " + "; ".join(reasons) + \
                                 " (ambiguity resolves UPWARD, P19)"
    return finding


def validate_finding(f: dict) -> None:
    """P5 quote-both. A finding missing ANY leg is REFUSED — never filed, never softened."""
    missing = []
    if not f.get("canon", {}).get("quote"):
        missing.append("canon quote (verbatim)")
    if not f.get("canon", {}).get("path") or not f.get("canon", {}).get("line"):
        missing.append("canon path:line")
    if not f.get("evidence", {}).get("quote"):
        missing.append("contradicting evidence (verbatim)")
    if not f.get("evidence", {}).get("probe"):
        missing.append("probe name")
    if missing:
        raise GardenerBlock("P5 finding REFUSED — missing leg(s): " + ", ".join(missing))


def sweep(root: str, targets: list[str], memory_dirs: list[str]) -> tuple[list[dict], list[dict]]:
    by_base, rels = build_index(root, memory_dirs)
    findings: list[dict] = []
    swept: list[dict] = []
    for path in targets:
        rel = os.path.relpath(path, root)
        try:
            text = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError) as exc:
            _die(2, f"P8 target unreadable AFTER self-check: {rel}", f"{type(exc).__name__}: {exc}")
        stars = _stars(text)
        ratified = _is_ratified(rel)
        claims = 0
        for i, line in enumerate(text.splitlines(), 1):
            # ── detector 1: path-pointer rot ──────────────────────────────────────────
            for tok in BACKTICK.findall(line):
                if not looks_like_path(tok):
                    continue
                claims += 1
                ok, cands = resolve_pointer(tok, root, by_base, rels, os.path.dirname(rel))
                if ok:
                    continue
                f = {
                    "detector": "path-pointer",
                    "canon": {"path": rel, "line": i, "quote": line.strip(),
                              "star_weight": stars, "ratified": ratified},
                    "evidence": {
                        "quote": (f"os.path.isfile({os.path.join(root, tok.lstrip('./'))}) "
                                  f"is False; basename index for '{os.path.basename(tok)}' "
                                  f"= {cands or 'NO MATCH ANYWHERE IN SWEEP SCOPE'}"),
                        "probe": ("path-resolve: os.path.isfile(root/token) + repo basename "
                                  "index walk (SKIP_DIRS excluded)"),
                    },
                    "_token": tok,
                    "_token_rel": tok.lstrip("./"),
                    "_candidates": cands,
                    "proposed": None,
                }
                findings.append(f)
            # ── detector 2: byte-figure drift ─────────────────────────────────────────
            m = BYTES_CLAIM.search(line)
            if m:
                toks = [t for t in BACKTICK.findall(line) if looks_like_path(t)]
                for tok in toks:
                    clean = tok.lstrip("./")
                    cand = None
                    if os.path.isfile(os.path.join(root, clean)):
                        cand = os.path.join(root, clean)
                    else:
                        hits = by_base.get(os.path.basename(clean), [])
                        if len(hits) == 1:
                            cand = os.path.join(root, hits[0])
                    if not cand or not os.path.isfile(cand):
                        continue
                    claims += 1
                    stated = int(m.group(1).replace(",", ""))
                    actual = os.path.getsize(cand)
                    if stated == actual:
                        continue
                    findings.append({
                        "detector": "byte-figure",
                        "canon": {"path": rel, "line": i, "quote": line.strip(),
                                  "star_weight": stars, "ratified": ratified},
                        "evidence": {
                            "quote": f"wc -c {os.path.relpath(cand, root)} = {actual} bytes "
                                     f"(doc states {stated})",
                            "probe": "byte-figure: os.path.getsize on the named file",
                        },
                        "_token": tok, "_token_rel": clean, "_candidates": [],
                        "proposed": None,
                    })
        swept.append({"path": rel, "bytes": len(text.encode()), "claims_scanned": claims,
                      "star_weight": stars, "ratified": ratified})
    return findings, swept


# ══ QUEUE ═════════════════════════════════════════════════════════════════════════════════
def _fingerprint(f: dict) -> str:
    return "|".join([f["detector"], f["canon"]["path"], f["_token"], f["canon"]["quote"][:120]])


def load_queue(path: str) -> dict:
    if not os.path.isfile(path):
        return {"$schema": SCHEMA_ID, "items": []}
    try:
        q = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _die(3, f"queue file unreadable/corrupt: {path}", f"{type(exc).__name__}: {exc}",
             "REFUSING TO GUESS its contents — a silently re-created queue would lose "
             "Dave's rulings on already-reviewed items.")
    if q.get("$schema") != SCHEMA_ID:
        _die(3, f"queue schema mismatch: found {q.get('$schema')!r}, expect {SCHEMA_ID!r}",
             "REFUSING TO GUESS a migration.")
    return q


OPEN_STATES = {"open"}


def build_queue(root: str, findings: list[dict], swept: list[dict], targets: list[str],
                cap_n: int, queue_cap_q: int, existing: dict, pass_id: str) -> dict:
    today = _dt.date.today().isoformat()
    prior = {it.get("fingerprint"): it for it in existing.get("items", [])}
    open_prior = [it for it in existing.get("items", []) if it.get("status") in OPEN_STATES]
    oldest = min((it.get("first_seen", today) for it in open_prior), default=None)
    paused = len(open_prior) > queue_cap_q  # P22 backpressure

    # rank: ★-weight of the canon touched, then tier (1 cheapest to act on), then path:line
    ranked = sorted(findings, key=lambda f: (-f["canon"]["star_weight"], f["tier"],
                                             f["canon"]["path"], f["canon"]["line"]))
    kept, dropped = ranked[:cap_n], ranked[cap_n:]

    items: list[dict] = list(existing.get("items", []))
    added = 0
    if not paused:
        for n, f in enumerate(kept, 1):
            fp = _fingerprint(f)
            if fp in prior:
                continue
            item = {
                "id": f"GQ-{today}-{len(items) + 1:03d}",
                "fingerprint": fp,
                "status": "open",
                "first_seen": today,
                "pass_id": pass_id,
                "tier": f["tier"],
                "tier_reason": f["tier_reason"],
                "disposition": f["disposition"],
                "flag_only": bool(f["canon"]["ratified"]),   # P7, set MECHANICALLY
                "detector": f["detector"],
                "canon": f["canon"],
                "evidence": f["evidence"],
                "proposed": f.get("proposed"),
                "tier1_conditions": f.get("tier1_conditions"),
                "tier1_hash_probe": f.get("tier1_hash_probe"),
            }
            validate_finding(item)      # P5 — refuses rather than files a half-finding
            items.append(item)
            added += 1

    open_now = [it for it in items if it.get("status") in OPEN_STATES]
    return {
        "$schema": SCHEMA_ID,
        "$description": ("Doc-gardener findings queue (B1, RULED s179-D1). One item = one "
                         "reviewable card in the review-queue controller (brief §3c-②): "
                         "canon quote · evidence quote · probe · [accept/flag/reject]. "
                         "Generated by knowledge/_gardener.py --sweep; statuses are written "
                         "back by the controller's compiled ruling, never by the gardener."),
        "generator": "knowledge/_gardener.py",
        "generated": _dt.datetime.now().isoformat(timespec="seconds"),
        "pass_id": pass_id,
        "cap_n": cap_n,
        "queue_cap_q": queue_cap_q,
        "truncated": {
            "declared": bool(dropped),
            "found": len(findings),
            "filed": len(kept) if not paused else 0,
            "dropped": len(dropped),
            "note": (f"P6: {len(dropped)} finding(s) above cap N={cap_n} were NOT filed this "
                     f"pass. They are not lost — they re-surface on the next sweep, ranked "
                     f"again by ★-weight." if dropped else "no truncation this pass"),
        },
        "backpressure": {
            "open_count": len(open_now),
            "oldest_open": oldest,
            "proposal_arm": "PAUSED" if paused else "RUNNING",
            "note": (f"P22: queue held {len(open_prior)} open items > Q={queue_cap_q} — the "
                     f"proposal arm PAUSED and filed nothing. Tier-1 repairs and the refresh "
                     f"arm are unaffected. Queued items NEVER expire (P21)."
                     if paused else "queue under Q; proposal arm running"),
            "added_this_pass": added,
        },
        "swept": swept,
        "targets_resolved": len(targets),
        "items": items,
    }


# ══ TIER-1 REGISTER + APPLY ═══════════════════════════════════════════════════════════════
def apply_tier1(fence: WriteFence, root: str, queue: dict, pass_id: str) -> list[dict]:
    """Register FIRST (P20), then the edit. Any doubt ⇒ no edit (P19)."""
    done = []
    for item in queue["items"]:
        if item.get("status") != "open" or item.get("tier") != 1:
            continue
        if item.get("flag_only"):
            continue                                    # P7 — ratified records are never edited
        conds = item.get("tier1_conditions") or {}
        if not all(conds.get(k) for k in ("c1_is_pointer", "c2_old_absent",
                                          "c3_new_present_unique", "c4_hash_match")):
            raise GardenerBlock(f"P19 — {item['id']} reached the apply path without all four "
                                f"conditions: {conds}")
        before, after = item["proposed"]["before"], item["proposed"]["after"]
        canon_abs = os.path.join(root, item["canon"]["path"])
        entry = {
            "ts": _dt.datetime.now().isoformat(timespec="seconds"),
            "pass_id": pass_id, "item_id": item["id"],
            "canon": f"{item['canon']['path']}:{item['canon']['line']}",
            "before": before, "after": after,
            "probe": item["tier1_hash_probe"].get("probe"),
            "old_blob": item["tier1_hash_probe"].get("old_blob"),
            "new_blob": item["tier1_hash_probe"].get("new_blob"),
            "reversible_via": f"git -C {root} diff -- {item['canon']['path']}",
        }
        fence.append(fence.register_path, json.dumps(entry, ensure_ascii=False) + "\n")
        lines = open(canon_abs, encoding="utf-8").read().splitlines(keepends=True)
        idx = item["canon"]["line"] - 1
        if f"`{before}`" not in lines[idx]:
            raise GardenerBlock(f"P19 — {item['id']}: the canon line no longer contains "
                                f"`{before}`. REFUSING TO GUESS where it went.")
        lines[idx] = lines[idx].replace(f"`{before}`", f"`{after}`")
        fence.write(canon_abs, "".join(lines))
        item["status"] = "applied"
        done.append(entry)
    return done


def refresh_arm() -> dict:
    """B3 REFRESH ARM — STUB, deliberately inert (P15/P9/P10).

    It re-runs the probes behind B3 staleness grades and restamps them. B3's sidecar grades
    file does not exist and its schema is DAVE'S at B3 review (s179-D1, brief §7). Building a
    grades file here would mint the exact instrument-without-a-consumer this programme exists
    to stop, and would pre-empt a Dave gate. So this returns a DECLARED GAP, never a number.
    """
    return {"arm": "refresh", "status": "NOT BUILT",
            "reason": "B3 sidecar grades file + schema are Dave's gate (s179-D1); "
                      "a refresh arm with no grades file would grade nothing and claim a pass",
            "blocks": "B3 build"}


# ══ RECEIPT ═══════════════════════════════════════════════════════════════════════════════
def receipt(queue: dict, applied: list[dict], dry: bool) -> str:
    t, b = queue["truncated"], queue["backpressure"]
    tiers = {1: 0, 2: 0, 3: 0}
    for it in queue["items"]:
        if it.get("status") == "open":
            tiers[it["tier"]] = tiers.get(it["tier"], 0) + 1
    L = [
        "── GARDENER PASS RECEIPT ─────────────────────────────────────────────",
        f"pass            : {queue['pass_id']}   ({'DRY RUN — nothing filed' if dry else 'filed'})",
        f"swept           : {len(queue['swept'])} files, "
        f"{sum(s['claims_scanned'] for s in queue['swept'])} path/figure claims scanned",
        f"findings        : {t['found']} found · {t['filed']} filed · {t['dropped']} dropped",
        f"truncation      : {t['note']}",
        f"queue           : {b['open_count']} open (cap Q={queue['queue_cap_q']}), "
        f"oldest {b['oldest_open'] or '—'} · proposal arm {b['proposal_arm']}",
        f"open by tier    : T1 {tiers.get(1,0)} · T2 {tiers.get(2,0)} · T3 {tiers.get(3,0)}",
        f"tier-1 applied  : {len(applied)}"
        + ("" if applied else "  (default is PENDING — canon untouched without --apply-tier1)"),
        f"refresh arm     : {refresh_arm()['status']} — {refresh_arm()['reason']}",
        "──────────────────────────────────────────────────────────────────────",
    ]
    return "\n".join(L)


# ══ MAIN ══════════════════════════════════════════════════════════════════════════════════
def run_sweep(root: str, cap_n: int, queue_cap_q: int, dry: bool, apply_t1: bool,
              memory_dirs: list[str] | None = None) -> tuple[int, dict]:
    root = os.path.abspath(root)
    targets = self_check(root)                                   # P8, FIRST ACT
    fence = WriteFence(root, targets, apply_t1)
    pass_id = f"gardener-{_dt.datetime.now().strftime('%Y%m%dT%H%M%S')}"
    findings, swept = sweep(root, targets,
                            MEMORY_DIRS if memory_dirs is None else memory_dirs)
    findings = [classify(f, root) for f in findings]
    existing = load_queue(fence.queue_path)
    queue = build_queue(root, findings, swept, targets, cap_n, queue_cap_q, existing, pass_id)
    applied: list[dict] = []
    if not dry:
        fence.write(fence.queue_path, json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
        if apply_t1:
            applied = apply_tier1(fence, root, queue, pass_id)
            fence.write(fence.queue_path, json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
    print(receipt(queue, applied, dry))
    return 0, queue


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply-tier1", action="store_true")
    ap.add_argument("--root", default=REPO)
    ap.add_argument("--cap", type=int, default=CAP_N)
    ap.add_argument("--queue-cap", type=int, default=QUEUE_CAP_Q)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.show:
        q = load_queue(os.path.join(os.path.abspath(a.root), OUT_DIRNAME, QUEUE_BASENAME))
        if not q.get("items"):
            print("queue empty — honest empty state, nothing filed.")
            return 0
        print(receipt(q, [], dry=True))
        return 0
    if not a.sweep:
        _die(64, "no arm named. Use --sweep, --selftest or --show.",
             "REFUSING TO GUESS an arm — a bare invocation must never do work (#158).")
    try:
        rc, _ = run_sweep(a.root, a.cap, a.queue_cap, a.dry_run, a.apply_tier1)
    except GardenerBlock as exc:
        _die(4, *str(exc).splitlines())
    return rc


# ══ MUTATION TESTS — plant, THEN detect. A green that cannot fail certifies nothing. ══════
FIX_DOC = "knowledge/_RUNBOOK-fixture.md"


def _mkrepo() -> str:
    root = tempfile.mkdtemp(prefix="gardener-fixture-")
    os.makedirs(os.path.join(root, "knowledge"))
    os.makedirs(os.path.join(root, "docs", "decisions"))
    os.makedirs(os.path.join(root, "notes", "_dream"))
    for f in TARGET_FILES:
        p = os.path.join(root, f)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(f"# {f}\n\nplain prose, no pointers.\n")
    open(os.path.join(root, "knowledge", "_RUNBOOKS.md"), "w").write("# runbooks index\n")
    open(os.path.join(root, FIX_DOC), "w").write("# fixture runbook ★★\n\nbody.\n")
    subprocess.run(["git", "-C", root, "init", "-q"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", root, "config", "user.name", "t"], check=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", root, "commit", "-qm", "fixture"], check=True,
                   capture_output=True)
    return root


def _sweep_fixture(root: str, cap: int = CAP_N, q: int = QUEUE_CAP_Q):
    targets = self_check(root)
    findings, swept = sweep(root, targets, memory_dirs=[])
    findings = [classify(f, root) for f in findings]
    return findings, swept, targets


def _t(name: str, ok: bool, detail: str) -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    return ok


def selftest() -> int:
    print("GARDENER MUTATION TESTS (plant → detect; every case shows its CONTROL)")
    ok = True

    # (a) plant a known-false canon line → found with all three legs. Control: absent ⇒ 0.
    root = _mkrepo()
    try:
        f0, _, _ = _sweep_fixture(root)
        control = len(f0)
        with open(os.path.join(root, FIX_DOC), "a") as fh:
            fh.write("\nSee `knowledge/_no_such_instrument.py` for the probe.\n")
        f1, _, _ = _sweep_fixture(root)
        planted = [f for f in f1 if f["_token"] == "knowledge/_no_such_instrument.py"]
        legs = planted and all([planted[0]["canon"]["quote"], planted[0]["canon"]["line"],
                                planted[0]["evidence"]["quote"], planted[0]["evidence"]["probe"]])
        ok &= _t("(a) false canon line found w/ 3 legs", bool(legs and control == 0),
                 f"control(clean)={control} findings; planted={len(planted)}; "
                 f"quote={planted[0]['canon']['quote'][:48]!r}" if planted else "NOT FOUND")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # (b) target list points at a moved file → LOUD nonzero exit, nothing filed.
    root = _mkrepo()
    try:
        os.rename(os.path.join(root, "AGENTS.md"), os.path.join(root, "AGENTS-moved.md"))
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--sweep",
                            "--root", root], capture_output=True, text=True)
        filed = os.path.isfile(os.path.join(root, OUT_DIRNAME, QUEUE_BASENAME))
        ok &= _t("(b) unresolvable target ⇒ loud exit, nothing filed",
                 r.returncode != 0 and "P8 SELF-CHECK FAILED" in r.stderr and not filed,
                 f"rc={r.returncode}; stderr names P8={'P8' in r.stderr}; queue filed={filed}")
        os.rename(os.path.join(root, "AGENTS-moved.md"), os.path.join(root, "AGENTS.md"))
        r2 = subprocess.run([sys.executable, os.path.abspath(__file__), "--sweep", "--dry-run",
                             "--root", root], capture_output=True, text=True)
        ok &= _t("(b-control) resolvable target ⇒ rc 0", r2.returncode == 0, f"rc={r2.returncode}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # (c) out-of-bounds write → BLOCK. Control: the queue path is allowed.
    root = _mkrepo()
    try:
        targets = self_check(root)
        fence = WriteFence(root, targets, apply_tier1=False)
        blocked = False
        try:
            fence.write(os.path.join(root, "GOOD-MORNING.md"), "nope")
        except GardenerBlock as exc:
            blocked = "P4" in str(exc)
        allowed = False
        try:
            fence.write(fence.queue_path, "{}")
            allowed = os.path.isfile(fence.queue_path)
        except GardenerBlock:
            allowed = False
        canon_blocked = False
        try:
            fence.write(os.path.join(root, FIX_DOC), "x")
        except GardenerBlock:
            canon_blocked = True
        ok &= _t("(c) out-of-bounds write BLOCKED (P4)", blocked and allowed and canon_blocked,
                 f"GOOD-MORNING blocked={blocked}; canon blocked w/o --apply-tier1="
                 f"{canon_blocked}; control queue write allowed={allowed}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # (d) plant 15 findings-worth → caps at 10, truncation DECLARED. Control: 5 ⇒ no truncation.
    root = _mkrepo()
    try:
        with open(os.path.join(root, FIX_DOC), "a") as fh:
            for i in range(5):
                fh.write(f"row {i}: see `knowledge/_ghost_{i}.py`\n")
        _, q5 = run_sweep(root, CAP_N, QUEUE_CAP_Q, dry=True, apply_t1=False, memory_dirs=[])
        with open(os.path.join(root, FIX_DOC), "a") as fh:
            for i in range(5, 15):
                fh.write(f"row {i}: see `knowledge/_ghost_{i}.py`\n")
        _, q15 = run_sweep(root, CAP_N, QUEUE_CAP_Q, dry=True, apply_t1=False, memory_dirs=[])
        ok &= _t("(d) 15 findings ⇒ capped at 10, truncation declared",
                 q15["truncated"]["found"] == 15 and q15["truncated"]["filed"] == CAP_N
                 and q15["truncated"]["declared"] and not q5["truncated"]["declared"],
                 f"control 5: found={q5['truncated']['found']} declared="
                 f"{q5['truncated']['declared']}; planted 15: found="
                 f"{q15['truncated']['found']} filed={q15['truncated']['filed']} "
                 f"dropped={q15['truncated']['dropped']}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # (e) moved WITH content change ⇒ NOT Tier 1, queues as Tier 2.
    #     Control: moved WITHOUT change ⇒ Tier 1.
    for label, mutate, want_tier in (("moved+CHANGED", True, 2), ("moved only", False, 1)):
        root = _mkrepo()
        try:
            old = os.path.join(root, "knowledge", "_moved_probe.py")
            open(old, "w").write("print('probe')\n")
            with open(os.path.join(root, FIX_DOC), "a") as fh:
                fh.write("Run `knowledge/_moved_probe.py` before the pass.\n")
            subprocess.run(["git", "-C", root, "add", "-A"], capture_output=True, check=True)
            subprocess.run(["git", "-C", root, "commit", "-qm", "add probe"],
                           capture_output=True, check=True)
            new = os.path.join(root, "_moved_probe.py")
            subprocess.run(["git", "-C", root, "mv", "knowledge/_moved_probe.py",
                            "_moved_probe.py"], capture_output=True, check=True)
            if mutate:
                open(new, "a").write("print('and now it does more')\n")
                subprocess.run(["git", "-C", root, "add", "-A"], capture_output=True, check=True)
            subprocess.run(["git", "-C", root, "commit", "-qm", "move"],
                           capture_output=True, check=True)
            fs, _, _ = _sweep_fixture(root)
            hit = [f for f in fs if f["_token"] == "knowledge/_moved_probe.py"]
            got = hit[0]["tier"] if hit else None
            ok &= _t(f"(e) pointer {label} ⇒ tier {want_tier}", got == want_tier,
                     f"tier={got}; conds={hit[0].get('tier1_conditions') if hit else '—'}; "
                     f"probe={hit[0]['tier1_hash_probe'].get('result') if hit else '—'}")
        finally:
            shutil.rmtree(root, ignore_errors=True)

    print("ALL MUTATION TESTS PASSED" if ok else "MUTATION TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
