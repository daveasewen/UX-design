#!/usr/bin/env python3
"""_registry.py — the verifier PROBE REGISTRY: manifest schema, loud loader, runner (W-45, `s204-D1` item 2).

THE CLASS this serves: every wave's verifier re-derives the same hunt from cold. A defect class
found at #184 (dangling dataviz var → silent black) or #204 (duplicate ids across theme panes)
is caught once, written into a receipt, and then has to be REMEMBERED by the next verifier.
A remembered hunt is a hunt that decays. This registry makes each historically-found class a
SCRIPT the next verifier RUNS — and then hunts free, which the brief text below keeps explicit.

THE MANIFEST (`manifest.jsonl`, one JSON object per line = one probe):

  REQUIRED
    id           str  — stable probe id (`P-1`…). NEVER reused, NEVER renumbered.
    klass        str  — the defect class, in the words the receipts use.
    title        str  — one line a verifier can read in a table.
    script       str  — filename inside this directory. Must exist.
    environment  str  — "sandbox" (pure python, runs anywhere) |
                        "sandbox-render" (needs Chromium+Playwright per
                        `_RUNBOOK-render-verify.md`; #173 environment-split applies) |
                        "unknown" (never defaulted — a measuring tool must not guess)
    blind        str  — what the probe CANNOT see, in prose. A registry without this field
                        invites the trust that narrows free hunting.
    caught       list — the LEDGER (below). May be empty ONLY for a probe with no receipt.

  OPTIONAL
    argv         list[str] — extra args the runner passes (default `["--check"]`)
    note         str       — FREE TEXT, deliberately unconstrained (the schema-too-tight price).

  A LEDGER ENTRY (`caught[]`) — the promotion evidence IS this list:
    session     int  — the session number the class was caught in. The promotion rule counts
                       DISTINCT sessions, so this is the join key, not a decoration.
    date        str  — YYYY-MM-DD.
    defect      str  — what was actually found, in one line.
    receipt     str  — a PROBEABLE POINTER (`s182-D1`): repo path, optionally `:line`.
    provenance  str  — "historical-mined" (mined from a receipt by the W-45 build, i.e. the
                       probe did NOT catch it — a human/agent did, before the probe existed) |
                       "live-run" (this probe, running, found it).
                       ⛔ The distinction exists so a mined receipt is never read as a live
                       catch. Both count toward twice-caught; the emitted candidature says
                       WHICH, so Dave promotes knowing the evidence is retrospective.
    kind        str  — "exact" (the same defect class this probe scans for) |
                       "species" (a same-species defect on another surface — e.g. #204's
                       `--x: var(--x)` cycle is the #184 silent-black species, not the same
                       scan). `_promote.py` counts EXACT only unless `--include-species`.

  ⛔ UNKNOWN KEYS ARE A PARSE FAILURE, not a silent drop (the `_claimtable.py` rule, same
  reason: a typo'd field that vanishes quietly is a row nobody decided to lose).

FAILURE IS LOUD AND NAMED: every unparseable line is reported with file, line number, reason;
the loader never skips silently and the runner prints a RESIDUAL count.

USAGE
  python3 knowledge/_probe_registry/_registry.py --list          # the manifest as a table
  python3 knowledge/_probe_registry/_registry.py --run           # drive every probe (rc=1 on findings)
  python3 knowledge/_probe_registry/_registry.py --run --survey  # drive every probe, rc=0 always
  python3 knowledge/_probe_registry/_registry.py --run --probe P-2
  python3 knowledge/_probe_registry/_registry.py --run --skip-env sandbox-render
  python3 knowledge/_probe_registry/_registry.py --selftests     # every probe's own --selftest
  python3 knowledge/_probe_registry/_registry.py --selftest      # THIS loader's plant-then-detect

CONSUMER AT BIRTH: the verifier-PM brief of every wave — the ready-to-paste paragraph lives in
`README.md` in this directory. DECLARED: not wired into `_build_all.py` or CI. `s204-D1` forbids
that until the registry has been driven in >= 1 real wave, and promotion of any probe to a build
gate is DAVE'S (derivation governance), never this tool's.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MANIFEST = os.path.join(HERE, "manifest.jsonl")

ENVIRONMENTS = ("sandbox", "sandbox-render", "unknown")
PROVENANCE = ("historical-mined", "live-run")
KINDS = ("exact", "species")
REQUIRED = ("id", "klass", "title", "script", "environment", "blind", "caught")
OPTIONAL = ("argv", "note")
ALLOWED = set(REQUIRED) | set(OPTIONAL)
CAUGHT_REQUIRED = ("session", "date", "defect", "receipt", "provenance", "kind")
CAUGHT_ALLOWED = set(CAUGHT_REQUIRED) | {"note"}
FINDINGS_RE = re.compile(r"findings=(\d+)")


class Defect:
    """One named parse failure. Carries WHERE — nothing is reported as a bare count."""

    def __init__(self, path, lineno, reason, excerpt=""):
        self.path, self.lineno, self.reason, self.excerpt = path, lineno, reason, excerpt

    def __str__(self):
        ex = (" · " + self.excerpt[:100]) if self.excerpt else ""
        return "  ⛔ %s:%d — %s%s" % (self.path, self.lineno, self.reason, ex)


def validate_row(row, path="<mem>", lineno=0, check_script=True):
    out = []
    if not isinstance(row, dict):
        return [Defect(path, lineno, "row is %s, not a JSON object" % type(row).__name__)]
    unknown = sorted(set(row) - ALLOWED)
    if unknown:
        out.append(Defect(path, lineno, "unknown field(s) %s — a typo'd field is a lost probe, "
                                        "not a silent drop; free text belongs in `note`" % unknown))
    for f in REQUIRED:
        if f == "caught":
            continue
        if not str(row.get(f, "")).strip():
            out.append(Defect(path, lineno, "missing required field `%s`" % f))
    if row.get("environment") not in ENVIRONMENTS and "environment" in row:
        out.append(Defect(path, lineno, "environment=%r not one of %s — UNKNOWN is never "
                          "defaulted" % (row.get("environment"), list(ENVIRONMENTS))))
    if check_script and row.get("script"):
        if not os.path.exists(os.path.join(HERE, row["script"])):
            out.append(Defect(path, lineno, "script %r does not exist in %s — a dead pointer "
                              "reads as evidence" % (row["script"], HERE)))
    if "argv" in row and (not isinstance(row["argv"], list)
                          or any(not isinstance(a, str) for a in row["argv"])):
        out.append(Defect(path, lineno, "`argv` must be a list of strings"))
    caught = row.get("caught")
    if not isinstance(caught, list):
        out.append(Defect(path, lineno, "`caught` must be a list (the ledger) — got %s"
                          % type(caught).__name__))
        return out
    for i, c in enumerate(caught):
        tag = "caught[%d]" % i
        if not isinstance(c, dict):
            out.append(Defect(path, lineno, "%s is not an object" % tag))
            continue
        unk = sorted(set(c) - CAUGHT_ALLOWED)
        if unk:
            out.append(Defect(path, lineno, "%s unknown field(s) %s" % (tag, unk)))
        for f in CAUGHT_REQUIRED:
            if f not in c or not str(c.get(f, "")).strip():
                out.append(Defect(path, lineno, "%s missing required field `%s`" % (tag, f)))
        if "session" in c and not isinstance(c["session"], int):
            out.append(Defect(path, lineno, "%s session=%r is not an int — it is the join key "
                              "the twice-caught rule counts on" % (tag, c["session"])))
        if c.get("provenance") not in PROVENANCE and "provenance" in c:
            out.append(Defect(path, lineno, "%s provenance=%r not one of %s"
                              % (tag, c.get("provenance"), list(PROVENANCE))))
        if c.get("kind") not in KINDS and "kind" in c:
            out.append(Defect(path, lineno, "%s kind=%r not one of %s"
                              % (tag, c.get("kind"), list(KINDS))))
        rec = str(c.get("receipt", ""))
        rec_path = rec.split(":")[0].strip()
        if rec_path and not os.path.exists(os.path.join(ROOT, rec_path)):
            out.append(Defect(path, lineno, "%s receipt path %r does not exist — a dead "
                              "evidence pointer is worse than none" % (tag, rec_path)))
    return out


def load(path=MANIFEST, check_script=True):
    """(rows, defects). NEVER skips a line silently — every skipped line IS a defect."""
    rows, defects, seen = [], [], {}
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            s = raw.strip()
            if not s or s.startswith("//"):
                continue
            try:
                obj = json.loads(s)
            except Exception as e:
                defects.append(Defect(path, lineno, "not valid JSON — %s" % e, s))
                continue
            errs = validate_row(obj, path, lineno, check_script=check_script)
            if errs:
                defects.extend(errs)
                continue
            if obj["id"] in seen:
                defects.append(Defect(path, lineno, "duplicate probe id %r (first seen line %d) "
                                      "— a shadowed probe is a probe nobody runs"
                                      % (obj["id"], seen[obj["id"]])))
                continue
            seen[obj["id"]] = lineno
            obj["_lineno"] = lineno
            rows.append(obj)
    return rows, defects


def report_defects(defects, label="manifest"):
    if not defects:
        return 0
    print("⛔ %s: %d UNPARSEABLE ROW(S) — declared, never skipped:" % (label, len(defects)))
    for d in defects:
        print(str(d))
    print("   RESIDUAL: %d row(s) are NOT in anything printed below." % len(defects))
    return len(defects)


# ---- runner -------------------------------------------------------------------------------

def _run_one(row, extra=()):
    argv = list(row.get("argv") or ["--check"]) + list(extra)
    cmd = [sys.executable, os.path.join(HERE, row["script"])] + argv
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    m = None
    for m2 in FINDINGS_RE.finditer(out):
        m = m2
    findings = int(m.group(1)) if m else None
    return p.returncode, findings, out, " ".join(cmd[1:])


def run(rows, only=None, skip_env=(), survey=False, quiet=False, extra=()):
    """Drive the probes. Returns (rc, results). rc=1 if any probe found something or errored,
    unless --survey. A probe that CANNOT run in this environment is REPORTED, never defaulted."""
    results = []
    for row in rows:
        if only and row["id"] not in only:
            continue
        if row["environment"] in skip_env:
            results.append((row, None, None, "SKIPPED (--skip-env %s)" % row["environment"]))
            print("\n=== %s %s — SKIPPED by --skip-env (%s)" % (row["id"], row["title"],
                                                               row["environment"]))
            continue
        print("\n=== %s · %s [%s]" % (row["id"], row["title"], row["environment"]))
        rc, findings, out, cmd = _run_one(row, extra)
        if not quiet:
            print(out.rstrip())
        print("--- rc=%d findings=%s · %s" % (rc, findings if findings is not None else "UNKNOWN",
                                              cmd))
        results.append((row, rc, findings, out))
    print("\n" + "=" * 78)
    print("REGISTRY RUN SUMMARY (%d probe(s))" % len(results))
    print("%-6s %-15s %-5s %-9s %s" % ("id", "env", "rc", "findings", "class"))
    bad = 0
    for row, rc, findings, _out in results:
        if rc is None:
            print("%-6s %-15s %-5s %-9s %s" % (row["id"], row["environment"], "-", "SKIP",
                                               row["klass"]))
            continue
        print("%-6s %-15s %-5d %-9s %s" % (row["id"], row["environment"], rc,
                                           findings if findings is not None else "UNKNOWN",
                                           row["klass"]))
        if rc != 0 or findings is None or findings > 0:
            bad += 1
    print("⚠ %d probe(s) reported findings, an UNKNOWN count, or a non-zero rc." % bad
          if bad else "✅ every probe ran and reported findings=0.")
    print("⛔ A green registry run proves THE PROBES RAN, not that the tree is clean. Each "
          "probe's `blind` field says what it cannot see; the verifier brief keeps free hunting "
          "mandatory for exactly that reason.")
    return (0 if survey else (1 if bad else 0)), results


def selftests(rows, only=None, skip_env=()):
    rc_total, table = 0, []
    for row in rows:
        if only and row["id"] not in only:
            continue
        if row["environment"] in skip_env:
            table.append((row["id"], "SKIP", row["script"]))
            continue
        p = subprocess.run([sys.executable, os.path.join(HERE, row["script"]), "--selftest"],
                           cwd=ROOT, capture_output=True, text=True)
        print("\n=== %s --selftest" % row["script"])
        print(((p.stdout or "") + (p.stderr or "")).rstrip())
        table.append((row["id"], str(p.returncode), row["script"]))
        rc_total |= (1 if p.returncode else 0)
    print("\nSELFTEST rc TABLE")
    for pid, rc, script in table:
        print("  %-6s rc=%-4s %s" % (pid, rc, script))
    return rc_total


def show(rows):
    print("%-5s %-15s %-42s %s" % ("id", "environment", "class", "caught (distinct sessions)"))
    for r in rows:
        sess = sorted({c["session"] for c in r["caught"]})
        print("%-5s %-15s %-42s %s" % (r["id"], r["environment"], r["klass"][:42],
                                       sess if sess else "— none yet"))
    print("\n%d probe(s) in %s" % (len(rows), MANIFEST))


# ---- selftest: plant-then-detect on the LOADER, both directions ---------------------------

_GOOD = {"id": "T-1", "klass": "test class", "title": "t", "script": "_registry.py",
         "environment": "sandbox", "blind": "everything",
         "caught": [{"session": 204, "date": "2026-08-19", "defect": "d",
                     "receipt": "knowledge/_probe_registry/_registry.py",
                     "provenance": "historical-mined", "kind": "exact"}]}


def _write(tmp, name, objs):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        for o in objs:
            f.write((json.dumps(o) if isinstance(o, dict) else o) + "\n")
    return p


def selftest():
    import copy
    fails, tmp = [], tempfile.mkdtemp(prefix="probe-registry-selftest-")
    plants = [
        ("malformed JSON", '{"id": "T-2", '),
        ("unknown field", dict(copy.deepcopy(_GOOD), id="T-3", scrpt="typo'd")),
        ("missing required", {k: v for k, v in _GOOD.items() if k != "blind"}),
        ("bad environment", dict(copy.deepcopy(_GOOD), id="T-5", environment="production")),
        ("dead script pointer", dict(copy.deepcopy(_GOOD), id="T-6", script="nope.py")),
        ("ledger: bad provenance", dict(copy.deepcopy(_GOOD), id="T-7",
                                        caught=[dict(_GOOD["caught"][0], provenance="vibes")])),
        ("ledger: bad kind", dict(copy.deepcopy(_GOOD), id="T-8",
                                  caught=[dict(_GOOD["caught"][0], kind="sort-of")])),
        ("ledger: session not an int", dict(copy.deepcopy(_GOOD), id="T-9",
                                            caught=[dict(_GOOD["caught"][0], session="204")])),
        ("ledger: dead receipt pointer", dict(copy.deepcopy(_GOOD), id="T-10",
                                              caught=[dict(_GOOD["caught"][0],
                                                           receipt="notes/_receipts/nope.md")])),
        ("ledger: missing field", dict(copy.deepcopy(_GOOD), id="T-11",
                                       caught=[{k: v for k, v in _GOOD["caught"][0].items()
                                                if k != "receipt"}])),
    ]
    for label, plant in plants:
        p = _write(tmp, "plant.jsonl", [_GOOD, plant])
        rows, defects = load(p)
        if not defects:
            fails.append("PLANT NOT CAUGHT: %s — loader returned %d rows, 0 defects"
                         % (label, len(rows)))
        else:
            print("  ✅ plant caught (%s): %s" % (label, defects[0].reason[:78]))

    p = _write(tmp, "dup.jsonl", [_GOOD, dict(_GOOD)])
    rows, defects = load(p)
    if not any("duplicate probe id" in d.reason for d in defects):
        fails.append("PLANT NOT CAUGHT: duplicate probe id — a shadowed probe is never run")
    else:
        print("  ✅ plant caught (duplicate probe id): shadowing named")

    p = _write(tmp, "clean.jsonl", [_GOOD, dict(_GOOD, id="T-20", caught=[],
                                                note="free text survives · unicode ⛔ ok")])
    rows, defects = load(p)
    if defects or len(rows) != 2:
        fails.append("REMOVAL NOT GREEN: clean file gave %d rows, %d defects (expected 2, 0)"
                     % (len(rows), len(defects)))
    else:
        print("  ✅ removal green: the clean manifest parses to 2 rows, 0 defects")
    if rows and rows[1].get("note", "").endswith("ok"):
        print("  ✅ free-text `note` survives the round trip (the schema-too-tight price)")
    else:
        fails.append("FREE TEXT LOST: `note` did not survive the round trip")

    # the LIVE manifest must itself parse — a registry whose own manifest is broken is worse
    # than none, and this arm is the one that fails when somebody hand-edits it.
    live_rows, live_defects = load(MANIFEST)
    if live_defects:
        report_defects(live_defects, "LIVE manifest.jsonl")
        fails.append("LIVE MANIFEST UNPARSEABLE: %d defect(s)" % len(live_defects))
    else:
        print("  ✅ live manifest parses: %d probe(s), 0 defects" % len(live_rows))

    if fails:
        print("⛔ _registry selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _registry selftest PASS — every planted manifest defect is named, and its removal "
          "goes green (both directions).")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    rows, defects = load()
    residual = report_defects(defects, "manifest.jsonl")
    only = None
    if "--probe" in argv:
        only = {argv[argv.index("--probe") + 1]}
    skip_env = set()
    while "--skip-env" in argv:
        i = argv.index("--skip-env")
        skip_env.add(argv[i + 1])
        del argv[i:i + 2]
    if "--selftests" in argv:
        return (selftests(rows, only, skip_env) or (1 if residual else 0))
    if "--run" in argv:
        rc, _ = run(rows, only, skip_env, survey="--survey" in argv, quiet="--quiet" in argv)
        return rc or (1 if residual else 0)
    show(rows)
    return 1 if residual else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
