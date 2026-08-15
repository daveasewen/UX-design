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
  3. B3's REFRESH ARM (BUILT #180 under s179-D1 — see `refresh_arm()`). It produces the
     SIDECAR `notes/_dream/_MEMORY-GRADES.json`; its consumers are the boot chain-read in
     `knowledge/_checkin.py` (the ONE bounded mitigation: starred/blocked alerts, cost
     MEASURED, not ruled permanent) and the B3 review itself, which reads
     `notes/_dream/_GRADE-DECISIONS.jsonl` for the two numbers Dave is owed.
     ⚠ THE GRADE SCHEMA IS PROVISIONAL — Dave rules it at that review (brief §7).

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
    _gardener.py --refresh                # B3 REFRESH ARM: re-probe + restamp the sidecar grades
    _gardener.py --refresh --dry-run      # grade, print the receipt, write nothing
    _gardener.py --selftest-grades        # the B3 mutation tests (grades + alert + fence)
    _gardener.py --grade-decision ID --changed yes|no --note "..."
                                          # log ONE retrieval decision (the return-with-numbers
                                          # counter s179-D1 owes Dave). Never inferred.
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

# ── B3 (s179-D1 clause 1, B-THEN-REVIEW). THE SIDECAR. ────────────────────────────────────
# Grades live HERE, never in MEMORY.md: boot cost zero, no boot-floor re-base, reversible.
# ⚠ THE GRADE SCHEMA BELOW IS **PROVISIONAL**. Dave rules it at the B3 review (brief §7:
#   "Grade schema and vocabulary" is on the DO-NOT-RULE list). Every constant in this block
#   is a PROPOSAL carrying its own reasoning, not a ruling, and the sidecar header says so.
GRADES_BASENAME = "_MEMORY-GRADES.json"
GRADE_LOG_BASENAME = "_GRADE-DECISIONS.jsonl"
GRADE_SCHEMA_ID = "memory-grades/0-PROVISIONAL"
# vocabulary (PROVISIONAL): four grades, and UNPROVABLE is a FIRST-CLASS one — an entry whose
# claim no machine can decide is NEVER silently called FRESH [[measuring-tool-must-not-guess]].
GRADE_VOCAB = ("FRESH", "AGING", "STALE", "UNPROVABLE")
GRADE_AGING_DAYS = 30        # PROVISIONAL: probe passes but the claim itself hasn't been touched
# Alert filter (PROVISIONAL). s179-D1: alerts for STARRED/BLOCKED entries ONLY.
ALERT_MARKS = ("⛔", "★★")   # ★★ or more, or a ⛔ — the marks MEMORY.md already carries
ALERT_LIST_GRADES = ("STALE",)              # printed one line each
ALERT_COUNT_GRADES = ("UNPROVABLE", "AGING")  # summarised as ONE count line — surface control
MEMORY_INDEX_BASENAME = "MEMORY.md"


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
      · <root>/notes/_dream/_MEMORY-GRADES.json       (B3 sidecar grades)
      · <root>/notes/_dream/_GRADE-DECISIONS.jsonl    (B3 return-with-numbers log)
      · a file on the RESOLVED TARGET LIST — only when apply_tier1 is True.

    ⛔ THE SIDECAR IS THE ONLY GRADES WRITER'S DOOR. Nothing in this programme may write a
    grade into MEMORY.md — that would be Option A (inline), which s179-D1 did NOT rule and
    which requires a boot-floor re-base Dave has not given. The memory store stays READ-ONLY
    here exactly as it is for the sweep (the #80 class).
    """

    def __init__(self, root: str, targets: list[str], apply_tier1: bool):
        self.root = os.path.abspath(root)
        self.out_dir = os.path.join(self.root, OUT_DIRNAME)
        self.queue_path = os.path.join(self.out_dir, QUEUE_BASENAME)
        self.register_path = os.path.join(self.out_dir, REGISTER_BASENAME)
        self.grades_path = os.path.join(self.out_dir, GRADES_BASENAME)
        self.grade_log_path = os.path.join(self.out_dir, GRADE_LOG_BASENAME)
        self.apply_tier1 = apply_tier1
        self._targets = {os.path.abspath(p) for p in targets}
        self.writes: list[str] = []

    def check(self, path: str) -> str:
        p = os.path.abspath(path)
        if p in (self.queue_path, self.register_path,
                 self.grades_path, self.grade_log_path):
            return p
        if self.apply_tier1 and p in self._targets:
            return p
        raise GardenerBlock(
            "P4 FILE-ONLY fence: refused write to a path outside the allowed set.\n"
            f"        attempted : {p}\n"
            f"        allowed   : {self.queue_path}\n"
            f"                    {self.register_path}\n"
            f"                    {self.grades_path}\n"
            f"                    {self.grade_log_path}\n"
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


# ══ B3 — THE REFRESH ARM AND THE SIDECAR ══════════════════════════════════════════════════
# RULED s179-D1 clause 1 (Dave, #179): B-THEN-REVIEW. Grades in a SIDECAR, boot cost zero, no
# boot-floor re-base; ONE bounded mitigation = the boot chain-read prints grade alerts for
# starred/blocked entries ONLY, its real cost MEASURED before it can be ruled permanent; after
# one full dream-pass cycle the fork RETURNS TO DAVE WITH NUMBERS.
#
# WHO CONSUMES THIS, NAMED BEFORE THE BUILD:
#   1. `knowledge/_checkin.py` boot chain-read → `render_grade_alerts()` (the mitigation, and
#      the thing whose token cost is being measured). That call is the CONSUMER; without it
#      this arm would be another [[instrument-without-a-consumer]].
#   2. The B3 REVIEW itself → `_GRADE-DECISIONS.jsonl`, which is the ONLY place the two
#      return-with-numbers figures can come from: `kind:"alert"` rows carry the measured
#      surface cost per boot, `kind:"decision"` rows carry the human statement that a grade
#      DID or DID NOT change a retrieval decision. A decision row is NEVER inferred from an
#      alert row — that inference is the whole question Dave is being asked to rule on.
#
# ⛔ EVERY FAILURE HERE IS LOUD AND NAMED. A corrupt sidecar BLOCKS; an unresolvable memory
#    index BLOCKS; a hook whose staleness no machine can decide is graded UNPROVABLE and
#    COUNTED, never silently skipped and never quietly called FRESH.

class GradesBlock(GardenerBlock):
    """A B3 fence bit. Subclasses GardenerBlock so `--refresh` exits through the same door."""


_HOOK_RE = re.compile(r"^-\s+\[(?P<title>[^\]]+)\]\((?P<slug>[^)\s]+\.md)\)(?P<rest>.*)$")


def memory_index_path(memory_dir: str) -> str:
    return os.path.join(os.path.abspath(memory_dir), MEMORY_INDEX_BASENAME)


def parse_memory_index(memory_dir: str) -> tuple[list[dict], list[str]]:
    """(hooks, unlinked_lines). LOUD if the index is missing — never an empty success."""
    p = memory_index_path(memory_dir)
    if not os.path.isfile(p):
        raise GradesBlock(
            "P8/B3 — the memory index does not resolve, so NOTHING can be graded.\n"
            f"        expected : {p}\n"
            "        REFUSING TO GUESS another index. An empty grade set here would read as "
            "'nothing is stale', which is the exact false-confidence B3 exists to remove.")
    hooks, unlinked = [], []
    for i, line in enumerate(open(p, encoding="utf-8").read().splitlines(), 1):
        s = line.strip()
        if not s or not s.startswith("- "):
            continue
        m = _HOOK_RE.match(s)
        if not m:
            unlinked.append(f"{i}: {_flat(s)}")     # DECLARED, never silently dropped
            continue
        title = m.group("title")
        hooks.append({
            "id": m.group("slug"),
            "line": i,
            "title": title,
            "marks": "".join(sorted({c for c in ALERT_MARKS if c in title})),
            "starred": any(c in title for c in ALERT_MARKS),
            "hook": s,
            "hook_sha": _sha(s),
        })
    return hooks, unlinked


def _flat(s: str, n: int = 90) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _sha(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def derive_probe(hook: str, root: str) -> dict:
    """A probe is MECHANICAL or it does not exist (PROVISIONAL kinds).

    kind `path-present` — the hook names exactly ONE backticked repo path. Decidable.
    kind `none`         — it does not. The entry grades UNPROVABLE, and says why.
    """
    cands = [t for t in re.findall(r"`([^`]+)`", hook) if looks_like_path(t)]
    cands = [t for t in dict.fromkeys(cands)]
    if len(cands) == 1:
        return {"kind": "path-present", "path": cands[0]}
    if len(cands) > 1:
        return {"kind": "none",
                "why": f"{len(cands)} path-like tokens in one hook ({', '.join(cands[:4])}) — "
                       "AMBIGUOUS, and ambiguity resolves UPWARD, never to a guess."}
    return {"kind": "none", "why": "no backticked repo path in the hook — no mechanical claim "
                                   "to re-run; staleness here is a JUDGMENT, Dave's or a "
                                   "reader's, not a machine's."}


def resolve_claimed_path(rel: str, root: str, by_base: dict | None) -> tuple[bool, str]:
    """Does the repo contain what the hook names? (found, evidence).

    ⚠ THE FIRST DRIVE OF THIS ARM ON REAL DATA reported 6 STALE grades for files that EXIST —
    memory hooks name BASENAMES (`_gauge_tokens.py`), the probe joined them to the repo root,
    and `os.path.exists` said no. A probe that reports STALE for a present file is worse than
    no probe: it teaches the reader to ignore the alert. So a bare basename resolves through
    the repo INDEX, and only a name the index cannot place anywhere is ABSENT.
    """
    if os.path.exists(os.path.join(root, rel)):
        return True, f"`{rel}` EXISTS at that exact path (probe: os.path.exists)"
    base = os.path.basename(rel)
    hits = (by_base or {}).get(base, [])
    if "/" not in rel and hits:
        return True, (f"`{rel}` EXISTS as {hits[0]}" + (f" (+{len(hits)-1} more)"
                                                        if len(hits) > 1 else "")
                      + " (probe: repo basename index)")
    if "/" in rel and hits:
        return False, (f"`{rel}` IS ABSENT at that path; a file of that NAME exists at "
                       f"{hits[0]} — MOVED, not gone (probe: repo basename index)")
    return False, f"`{rel}` IS ABSENT — no file of that name anywhere in {os.path.basename(root)}"


def run_probe(probe: dict, root: str, by_base: dict | None = None) -> tuple[bool | None, str]:
    """(passed | None-if-unprovable, evidence sentence). NEVER raises for a normal outcome."""
    kind = probe.get("kind")
    if kind == "path-present":
        return resolve_claimed_path(probe["path"], root, by_base)
    if kind == "text-present":
        rel, needle = probe["path"], probe["needle"]
        abs_p = os.path.join(root, rel)
        if not os.path.exists(abs_p):
            return False, f"`{rel}` IS ABSENT, so the quoted text cannot be present"
        ok = needle in open(abs_p, encoding="utf-8", errors="replace").read()
        return ok, f"{'found' if ok else 'DID NOT find'} {needle!r} in `{rel}`"
    if kind == "none":
        return None, probe.get("why", "no probe")
    raise GradesBlock(
        f"B3 — unknown probe kind {kind!r} in the sidecar. REFUSING TO GRADE.\n"
        f"        known kinds: path-present · text-present · none\n"
        "        An unknown kind is a schema drift, not a pass. Fix the sidecar or the "
        "PROVISIONAL schema in knowledge/_gardener.py.")


def grade_entry(hook: dict, probe: dict, root: str, memory_dir: str,
                now: float | None = None, aging_days: int = GRADE_AGING_DAYS,
                by_base: dict | None = None) -> dict:
    """Grade ONE hook. Every branch names its evidence; no branch returns a bare FRESH."""
    now = _dt.datetime.now().timestamp() if now is None else now
    target = os.path.join(os.path.abspath(memory_dir), hook["id"])
    if not os.path.isfile(target):
        return {"grade": "STALE", "why": f"the hook's own target `{hook['id']}` is ABSENT from "
                                         f"the memory store (probe: os.path.isfile)",
                "probe_ran": True}
    passed, ev = run_probe(probe, root, by_base)
    if passed is None:
        return {"grade": "UNPROVABLE", "why": ev, "probe_ran": False}
    if not passed:
        return {"grade": "STALE", "why": ev, "probe_ran": True}
    age_days = (now - os.path.getmtime(target)) / 86400.0
    if age_days > aging_days:
        return {"grade": "AGING", "why": f"{ev}; but the claim itself has not been touched in "
                                         f"{age_days:.0f} days (limit {aging_days}, PROVISIONAL)",
                "probe_ran": True}
    return {"grade": "FRESH", "why": ev, "probe_ran": True}


def load_grades(path: str) -> dict:
    """Read the sidecar. A CORRUPT sidecar is a BLOCK, never an empty dict (silent-skip class)."""
    if not os.path.isfile(path):
        return {}
    raw = open(path, encoding="utf-8").read()
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GradesBlock(
            f"B3 — the sidecar grades file is NOT VALID JSON: {path}\n"
            f"        json error: {exc}\n"
            "        REFUSING to treat an unreadable grades file as 'no grades'. A silent "
            "skip here would print a clean boot while every grade is unknown.") from exc
    if not isinstance(doc, dict) or doc.get("schema") != GRADE_SCHEMA_ID:
        raise GradesBlock(
            f"B3 — sidecar schema mismatch in {path}\n"
            f"        found : {doc.get('schema') if isinstance(doc, dict) else type(doc).__name__}\n"
            f"        want  : {GRADE_SCHEMA_ID}\n"
            "        The schema is PROVISIONAL and Dave's to rule; a mismatch means the file "
            "and the code disagree about the grammar. Re-run `--refresh` deliberately.")
    for e in doc.get("entries", []):
        if e.get("grade") not in GRADE_VOCAB:
            raise GradesBlock(
                f"B3 — entry {e.get('id')!r} carries grade {e.get('grade')!r}, which is not in "
                f"the PROVISIONAL vocabulary {GRADE_VOCAB}. REFUSING to read it as anything.")
    return doc


def refresh_arm(root: str, memory_dir: str, fence: "WriteFence | None" = None,
                dry: bool = True, now: float | None = None) -> dict:
    """B3 REFRESH ARM — BUILT #180 under s179-D1. Consumes and produces the sidecar.

    Re-derives a probe for every MEMORY.md hook, re-runs it, restamps the grade. Writes ONLY
    through the fence, ONLY to the sidecar. Fails LOUD and NAMED on anything unprovable-as-a-
    file (missing index, corrupt sidecar, unknown probe kind); an unprovable CLAIM is not an
    error — it is the grade UNPROVABLE, counted and surfaced.
    """
    root = os.path.abspath(root)
    hooks, unlinked = parse_memory_index(memory_dir)
    prev_doc = load_grades(fence.grades_path) if fence else {}
    prev = {e["id"]: e for e in prev_doc.get("entries", [])}
    by_base, _rels = build_index(root, [])       # basename → paths; see resolve_claimed_path
    entries, counts, changed = [], {g: 0 for g in GRADE_VOCAB}, []
    for h in hooks:
        old = prev.get(h["id"], {})
        probe = old.get("probe") if old.get("probe_pinned") else derive_probe(h["hook"], root)
        g = grade_entry(h, probe, root, memory_dir, now=now, by_base=by_base)
        counts[g["grade"]] += 1
        if old and old.get("grade") != g["grade"]:
            changed.append(f"{h['id']}: {old.get('grade')} → {g['grade']}")
        entries.append({
            "id": h["id"], "title": h["title"], "marks": h["marks"], "starred": h["starred"],
            "index_line": h["line"], "hook_sha": h["hook_sha"],
            "probe": probe, "probe_pinned": bool(old.get("probe_pinned")),
            "grade": g["grade"], "why": g["why"], "probe_ran": g["probe_ran"],
            "graded_at": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        })
    doc = {
        "schema": GRADE_SCHEMA_ID,
        "PROVISIONAL": (
            "⚠ THE GRADE SCHEMA AND VOCABULARY IN THIS FILE ARE PROVISIONAL. Brief §7 puts "
            "them on the DO-NOT-RULE list; Dave rules them at the B3 review. Nothing here is "
            "a ruling. s179-D1 ruled only the SHAPE: sidecar, boot cost zero, alerts for "
            "starred/blocked entries only, return to Dave with numbers after one cycle."),
        "ruled_by": "s179-D1 clause 1 (B-THEN-REVIEW) — built #180",
        "vocabulary": {
            "FRESH": "a mechanical probe RE-RAN and PASSED, and the claim was touched recently",
            "AGING": f"probe passes, but the claim is older than {GRADE_AGING_DAYS}d (PROVISIONAL)",
            "STALE": "a mechanical probe RE-RAN and FAILED, or the hook's target is absent",
            "UNPROVABLE": "no mechanical probe exists — staleness here is a JUDGMENT, not a "
                          "measurement. NEVER read as FRESH.",
        },
        "alert_rule": {
            "marks": list(ALERT_MARKS), "listed": list(ALERT_LIST_GRADES),
            "counted": list(ALERT_COUNT_GRADES),
            "note": "s179-D1: alerts for STARRED/BLOCKED entries ONLY. Surface control "
                    "(list vs count) is PROVISIONAL and is what the cost measurement prices.",
        },
        "refreshed_at": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "memory_index": memory_index_path(memory_dir),
        "counts": counts,
        "hooks_seen": len(hooks),
        "unlinked_index_lines": unlinked,
        "grade_changes_this_pass": changed,
        "entries": entries,
    }
    if not dry:
        if fence is None:
            raise GradesBlock("B3 — refresh asked to WRITE with no WriteFence. Refused: every "
                              "write in this module goes through the fence (P4).")
        fence.write(fence.grades_path, json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return doc


def grades_status(root: str) -> dict:
    """Cheap read for the pass receipt. Never grades, never writes."""
    p = os.path.join(os.path.abspath(root), OUT_DIRNAME, GRADES_BASENAME)
    if not os.path.isfile(p):
        return {"arm": "refresh", "status": "NO SIDECAR YET",
                "reason": f"{os.path.join(OUT_DIRNAME, GRADES_BASENAME)} absent — run "
                          f"`_gardener.py --refresh`"}
    doc = load_grades(p)
    c = doc.get("counts", {})
    return {"arm": "refresh", "status": "BUILT (#180)",
            "reason": f"{doc.get('hooks_seen')} hooks graded {doc.get('refreshed_at')} — "
                      + " · ".join(f"{k} {c.get(k, 0)}" for k in GRADE_VOCAB)}


# ── THE BOUNDED MITIGATION: the boot alert surface (rendered here, PRINTED by _checkin.py) ──
def render_grade_alerts(doc: dict) -> list[str]:
    """The ONE bounded mitigation of s179-D1: starred/blocked entries ONLY.

    Returned as lines so the consumer can MEASURE them (that measurement is the precondition
    on ruling this surface permanent). An empty list means 'no starred entry is stale' — an
    honest silence, and the caller says so rather than printing nothing.
    """
    ent = [e for e in doc.get("entries", []) if e.get("starred")]
    listed = [e for e in ent if e.get("grade") in ALERT_LIST_GRADES]
    counted = {g: sum(1 for e in ent if e.get("grade") == g) for g in ALERT_COUNT_GRADES}
    lines: list[str] = []
    for e in sorted(listed, key=lambda e: e["id"]):
        lines.append(f"⛔ {e['grade']}  {e['id']} — {_flat(e.get('why', ''), 96)}")
    if any(counted.values()):
        lines.append("· " + " · ".join(f"{v} {k}" for k, v in counted.items() if v)
                     + f"  (of {len(ent)} starred/blocked entries; not listed — surface control)")
    return lines


def log_grade_event(root: str, event: dict) -> str:
    """Append ONE row to _GRADE-DECISIONS.jsonl through the fence. Returns the path."""
    fence = WriteFence(root, [], apply_tier1=False)
    row = dict(event)
    row.setdefault("at", _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    fence.append(fence.grade_log_path, json.dumps(row, ensure_ascii=False) + "\n")
    return fence.grade_log_path


# ══ RECEIPT ═══════════════════════════════════════════════════════════════════════════════
def receipt(queue: dict, applied: list[dict], dry: bool, root: str = None) -> str:
    try:
        _rs = grades_status(root or REPO)
    except GardenerBlock as exc:                 # LOUD in the receipt, never a green blank
        _rs = {"status": "BLOCKED", "reason": _flat(str(exc), 160)}
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
        f"refresh arm     : {_rs['status']} — {_rs['reason']}",
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
    print(receipt(queue, applied, dry, root))
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
    # ── B3 (s179-D1 clause 1) ──
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--selftest-grades", action="store_true")
    ap.add_argument("--memory-dir", default=None)
    ap.add_argument("--grade-decision", default=None, metavar="ENTRY_ID")
    ap.add_argument("--changed", default=None, choices=["yes", "no"])
    ap.add_argument("--note", default=None)
    ap.add_argument("--session", default=None)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.show:
        q = load_queue(os.path.join(os.path.abspath(a.root), OUT_DIRNAME, QUEUE_BASENAME))
        if not q.get("items"):
            print("queue empty — honest empty state, nothing filed.")
            return 0
        print(receipt(q, [], dry=True, root=a.root))
        return 0
    # ── B3 arms ────────────────────────────────────────────────────────────────────────────
    if a.selftest_grades:
        return selftest_grades()
    if a.grade_decision:
        if a.changed not in ("yes", "no"):
            _die(64, "--grade-decision needs --changed yes|no.",
                 "REFUSING TO GUESS whether the grade changed your retrieval decision — that "
                 "answer IS the number s179-D1 owes Dave; an inferred one is worthless.")
        p = log_grade_event(a.root, {"kind": "decision", "entry": a.grade_decision,
                                     "changed_retrieval": a.changed == "yes",
                                     "note": a.note or "", "session": a.session or "UNSTATED"})
        print(f"logged: decision on {a.grade_decision} (changed={a.changed}) → {p}")
        return 0
    if a.refresh:
        mem = a.memory_dir or (MEMORY_DIRS[0] if MEMORY_DIRS else None)
        try:
            root = os.path.abspath(a.root)
            fence = WriteFence(root, [], apply_tier1=False)
            doc = refresh_arm(root, mem, fence, dry=a.dry_run)
        except GardenerBlock as exc:
            _die(4, *str(exc).splitlines())
        c = doc["counts"]
        print("── B3 REFRESH RECEIPT (grade schema PROVISIONAL — Dave's at review) ──")
        print(f"index           : {doc['memory_index']}")
        print(f"hooks graded    : {doc['hooks_seen']}  "
              + " · ".join(f"{k} {c[k]}" for k in GRADE_VOCAB))
        print(f"unlinked lines  : {len(doc['unlinked_index_lines'])} DECLARED, not graded")
        print(f"grade changes   : {len(doc['grade_changes_this_pass'])}"
              + ("  (" + "; ".join(doc["grade_changes_this_pass"][:5]) + ")"
                 if doc["grade_changes_this_pass"] else ""))
        alerts = render_grade_alerts(doc)
        print(f"alert surface   : {len(alerts)} line(s) at boot")
        for ln in alerts:
            print(f"    {ln}")
        print("sidecar         : " + ("NOT WRITTEN (--dry-run)" if a.dry_run
                                      else fence.grades_path))
        return 0
    if not a.sweep:
        _die(64, "no arm named. Use --sweep, --refresh, --selftest, --selftest-grades or --show.",
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


# ══ B3 MUTATION TESTS — plant a grade, THEN look for the alert. Every arm has its CONTROL. ═
def _mkmem(hooks: list[str]) -> str:
    """A memory store fixture: MEMORY.md + one file per hook slug."""
    d = tempfile.mkdtemp(prefix="gardener-mem-")
    open(os.path.join(d, MEMORY_INDEX_BASENAME), "w", encoding="utf-8").write(
        "\n".join(hooks) + "\n")
    for h in hooks:
        m = _HOOK_RE.match(h.strip())
        if m:
            open(os.path.join(d, m.group("slug")), "w", encoding="utf-8").write("body\n")
    return d


def _grade_fixture(hooks: list[str], make_target: bool = False):
    root = _mkrepo()
    mem = _mkmem(hooks)
    if make_target:
        open(os.path.join(root, "knowledge", "_probe_target.py"), "w").write("x\n")
    fence = WriteFence(root, [], apply_tier1=False)
    return root, mem, fence


def selftest_grades() -> int:
    print("B3 GRADE MUTATION TESTS (plant a grade → detect the alert; each shows its CONTROL)")
    ok = True
    STARRED = "- [★★ Thing](thing.md) — see `knowledge/_probe_target.py` for the probe"
    PLAIN = "- [Thing](thing.md) — see `knowledge/_probe_target.py` for the probe"
    NOPROBE = "- [⛔ Judgment call](judgment.md) — prose only, nothing a machine can re-run"

    # (g1) starred + probe FAILS ⇒ STALE and an alert LINE. Control: probe passes ⇒ no alert.
    for label, target, want_grade, want_alert in (("target absent", False, "STALE", True),
                                                  ("target present", True, "FRESH", False)):
        root, mem, fence = _grade_fixture([STARRED], make_target=target)
        try:
            doc = refresh_arm(root, mem, fence, dry=True)
            g = doc["entries"][0]["grade"]
            alerts = render_grade_alerts(doc)
            got_alert = any("thing.md" in a for a in alerts)
            ok &= _t(f"(g1) starred, {label} ⇒ {want_grade}, alert={want_alert}",
                     g == want_grade and got_alert == want_alert,
                     f"grade={g}; alerts={alerts}")
        finally:
            shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    # (g2) THE STARRED-ONLY CLAUSE (s179-D1). Same stale entry, marks removed ⇒ NO alert.
    root, mem, fence = _grade_fixture([PLAIN], make_target=False)
    try:
        doc = refresh_arm(root, mem, fence, dry=True)
        alerts = render_grade_alerts(doc)
        ok &= _t("(g2) UNSTARRED stale entry ⇒ NO alert (starred/blocked ONLY)",
                 doc["entries"][0]["grade"] == "STALE" and alerts == [],
                 f"grade={doc['entries'][0]['grade']}; alerts={alerts} "
                 f"(control (g1) with ★★ DID alert)")
    finally:
        shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    # (g3) CORRUPT SIDECAR ⇒ LOUD NAMED refusal. Control: the file it just wrote loads clean.
    root, mem, fence = _grade_fixture([STARRED], make_target=True)
    try:
        refresh_arm(root, mem, fence, dry=False)
        control = load_grades(fence.grades_path).get("schema") == GRADE_SCHEMA_ID
        open(fence.grades_path, "w", encoding="utf-8").write('{"schema": "memory-grades/0-PRO')
        named = False
        try:
            load_grades(fence.grades_path)
        except GradesBlock as exc:
            named = "NOT VALID JSON" in str(exc)
        # and a VALID json with the WRONG schema is refused too, by its own name
        open(fence.grades_path, "w", encoding="utf-8").write('{"schema": "something/9"}')
        named2 = False
        try:
            load_grades(fence.grades_path)
        except GradesBlock as exc:
            named2 = "schema mismatch" in str(exc)
        ok &= _t("(g3) corrupt/foreign sidecar ⇒ LOUD named BLOCK, never a silent skip",
                 control and named and named2,
                 f"control loads={control}; bad-json named={named}; bad-schema named={named2}")
    finally:
        shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    # (g4) NO MECHANICAL PROBE ⇒ UNPROVABLE (never FRESH), counted not listed.
    root, mem, fence = _grade_fixture([NOPROBE], make_target=True)
    try:
        doc = refresh_arm(root, mem, fence, dry=True)
        e = doc["entries"][0]
        alerts = render_grade_alerts(doc)
        ok &= _t("(g4) unprobeable hook ⇒ UNPROVABLE, counted in the alert not listed",
                 e["grade"] == "UNPROVABLE" and not e["probe_ran"]
                 and any(a.startswith("· ") and "1 UNPROVABLE" in a for a in alerts),
                 f"grade={e['grade']}; why={_flat(e['why'], 60)!r}; alerts={alerts}")
    finally:
        shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    # (g5) THE HOOK'S OWN TARGET IS GONE ⇒ STALE naming it. Control: present ⇒ not that reason.
    root, mem, fence = _grade_fixture([STARRED], make_target=True)
    try:
        os.remove(os.path.join(mem, "thing.md"))
        doc = refresh_arm(root, mem, fence, dry=True)
        e = doc["entries"][0]
        ok &= _t("(g5) hook target absent ⇒ STALE, reason NAMES the target",
                 e["grade"] == "STALE" and "thing.md" in e["why"] and "ABSENT" in e["why"],
                 f"grade={e['grade']}; why={_flat(e['why'], 70)!r}")
    finally:
        shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    # (g6) FENCE — the sidecar + log are writable; MEMORY.md is NOT (Option A stays unruled).
    root, mem, fence = _grade_fixture([STARRED], make_target=True)
    try:
        allowed = True
        try:
            fence.write(fence.grades_path, '{"schema": "%s"}' % GRADE_SCHEMA_ID)
            fence.append(fence.grade_log_path, "{}\n")
        except GardenerBlock:
            allowed = False
        blocked = False
        try:
            fence.write(memory_index_path(mem), "graded inline")
        except GardenerBlock as exc:
            blocked = "P4" in str(exc)
        ok &= _t("(g6) sidecar+log writable, MEMORY.md write BLOCKED (P4, boot cost stays zero)",
                 allowed and blocked, f"sidecar/log allowed={allowed}; MEMORY.md blocked={blocked}")
    finally:
        shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    # (g7) MISSING MEMORY INDEX ⇒ BLOCK, never an empty (and therefore reassuring) grade set.
    root = _mkrepo()
    mem = tempfile.mkdtemp(prefix="gardener-nomem-")
    try:
        named = False
        try:
            refresh_arm(root, mem, WriteFence(root, [], False), dry=True)
        except GradesBlock as exc:
            named = "memory index does not resolve" in str(exc)
        ok &= _t("(g7) no memory index ⇒ LOUD block, not an empty pass", named,
                 f"named refusal={named}")
    finally:
        shutil.rmtree(root, ignore_errors=True); shutil.rmtree(mem, ignore_errors=True)

    print("ALL B3 MUTATION TESTS PASSED" if ok else "B3 MUTATION TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
