#!/usr/bin/env python3
"""gen_brief.py — MINT-TIME BRIEF GENERATION (W-46 proposal 2, `s204-D1` item 4).

Built to the settled scope in `notes/_briefs/2026-08-19-207-w46-three-scoped-proposals-v1.md`
§ "PROPOSAL 2 — Mint-time brief generation". Nothing here re-opens one of that section's
choices; where the spec named a mechanism, this file is that mechanism and nothing more.

★ WHAT IT IS. A script that writes the FIRST DRAFT of a PM brief by READING THE LIVE STORE
instead of a person remembering what is open — and that re-measures every premise it prints by
RUNNING THE PROBE at mint time, so a brief can no longer ship a fact that was true last week.

CONSUMER AT BIRTH: the conductor at the brief-writing seat. That seat is the named failure
point of `s202-D3` — "five builds argued about a component that does not exist because the
store was never asked at the brief-writing seat". This file is that ruling made mechanical
rather than remembered.

--------------------------------------------------------------------------------
THE SEVEN REGIONS (spec table (a)) — and OWNERSHIP IS PROVABLE, NOT STATED

  region                owner              source
  TITLE-GOVERNANCE      machine            ruling id · programme brief · store row · provenance
  THE-JOB               HUMAN              the conductor writes it; the generator never invents scope
  PREMISE-TABLE         machine            probes RUN at mint; each row = command · rc · timestamp
  OPEN-ITEMS            machine            knowledge/_state.json
  DO-NOT-RULE           machine            store items state=open+owner=dave · rulings with `open`
  DO-NOT-RULE-APPEND    HUMAN              the lane-specific block that is derivable from neither
  FENCES-ENVIRONMENT    machine            runbook extraction + measured environment
  RETURN-CONTRACT       HUMAN              what the sub owes back

DO-NOT-RULE is the spec's "machine + human append": it is TWO marker blocks, one owned each
way, so the append survives re-mint by construction rather than by care.

⛔ MACHINE REGIONS ARE DELIMITED BY MARKERS AND CARRY A CHECKSUM of their own generated body.
On re-mint a mismatch means a HUMAN EDITED MACHINE TEXT — the generator REFUSES and NAMES THE
REGION rather than overwriting the edit. There is deliberately no `--force`: the refusal names
the two legal moves instead (move the edit into a human region, or mint to a NEW dated path —
a brief is a dated period record, so a second file is a legal answer, not a workaround).
[[honest-refusal-needs-a-legal-form]].

⛔ HUMAN REGIONS ARE NEVER PARSED, NEVER VALIDATED, NEVER REWRITTEN. They are carried across a
re-mint BYTE FOR BYTE. (The bytes are of course read in order to be carried — what is promised,
and what the selftest proves, is that nothing inspects, checks or regenerates them.)

`--regions` IS THE FENCE ([[do-not-rule-list-cannot-fence-a-generator]]): it prints exactly
which marker-delimited regions this generator writes, and it is DERIVED FROM THE SAME `REGIONS`
TABLE THE WRITER USES — never a second, hand-kept list that can drift from the writer. The
selftest bites that identity directly: the names `--regions` reports as WRITTEN must equal the
names `mint()` reports having written.

--------------------------------------------------------------------------------
THE PREMISE TABLE — the dangerous region, and its containment

[[premise-ages-faster-than-rule]]: at #203 a derived snapshot's Status column briefed six lanes
at 18/18 false-Gap. Auto-filling a premise table is that same machine at higher speed. The
containment is NON-NEGOTIABLE and it is enforced here in code: EVERY ROW PRINTS THE COMMAND,
THE RETURN CODE AND THE TIMESTAMP, plus the probe's own last line VERBATIM. No row carries a
summary word — no "clean", no "PASS", no "no findings". A row a reader cannot re-run is a
claim, not a measurement ([[measure-dont-convert-units]], `s182-D1`).

WHICH PROBES RUN is derived from the registry manifest's own `environment` field, not from a
list typed here: `environment == "sandbox"` probes are RUN (P-1, P-2, P-4, P-5 — measured at
~0.72s total in the #207 scoping lane); anything else is printed as a DECLARED, NOT-RUN row
naming its environment (P-3, `sandbox-render`). ⛔ P-3 IS NEVER OMITTED. A declared gap passes;
a silent one fails.

--------------------------------------------------------------------------------
WHAT THIS GENERATOR CANNOT SEE — declared, per [[gate-glob-scope-rule]]

It rules only as wide as the stores it reads: `_state.json`, `_rulings.json`, `_lanes.json`,
the probe registry manifest and `knowledge/_RUNBOOK-*.md`. Memory hooks live outside the repo
entirely; rulings made in chat and not yet inscribed are invisible; anything a human knows and
has not written down is invisible. Every minted brief prints that sentence in its own
FENCES-ENVIRONMENT region, so the reader is told, not trusted to remember.

--------------------------------------------------------------------------------
ADR-0017 / [[write-once-principle-floated-192]] — the debt this creates, stated

A generated brief is one more derived view that can go stale. The containment the spec chose,
and which the minted header states in the brief itself: the brief is a DATED PERIOD RECORD of a
lane; THE STORE STAYS THE ONE LIVE HOME; the brief is NEVER citable as the source of a live fact.

USAGE
  python3 knowledge/gen_brief.py --regions
  python3 knowledge/gen_brief.py --mint --lane lane-2-apollo-charts --out notes/_briefs/<file>.md
  python3 knowledge/gen_brief.py --parse notes/_briefs/<file>.md     # structured parse, no write
  python3 knowledge/gen_brief.py --selftest

EXIT CODES
  0   minted / parsed / listed
  1   a MEASURED refusal: a machine region was hand-edited, or the file does not parse
  2   bad arguments
  77  COULD-NOT-ASK (`s193-D1`, `_could_not_ask.py`): an INPUT could not be reached — today the
      only such input is the probe registry directory. Keyed on the unreachable input, NEVER on
      "am I in CI" [[gate-cannot-pass-in-one-environment]].

⬛ NOT WIRED. This generator is not a `_build_all.STEPS` entry and not a CI step — wiring is
Dave's call and a proposed build step is priced in the #209 report. Declared at birth so that
[[instrument-without-a-consumer]] is a stated debt rather than a discovered one; the generator
WAS driven on a real lane in the wave it was built (the demo brief named in its store row).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
from _helpgate import write_gate as _write_gate; _write_gate(__file__)

import argparse
import datetime
import hashlib
import json
import operator
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _could_not_ask as cna  # noqa: E402 — the #193 three-verdict convention

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOW = os.path.join(ROOT, "knowledge")
STORE = os.path.join(KNOW, "_state.json")
RULINGS = os.path.join(KNOW, "_rulings.json")
LANES = os.path.join(KNOW, "_lanes.json")
REGDIR = os.path.join(KNOW, "_probe_registry")
WRITER = "knowledge/gen_brief.py"

MACHINE, HUMAN = "machine", "human"
HUMAN_SHA = "NONE-HUMAN-OWNED"

# The runbooks whose ⛔ lines are extracted into FENCES-ENVIRONMENT. A DECLARED subset, not
# every runbook: the glob is stated in the region itself so the reader knows the scope of what
# they are being shown [[gate-glob-scope-rule]].
FENCE_RUNBOOKS = (
    "_RUNBOOK-git-commit.md",
    "_RUNBOOK-parallel-conductor.md",
    "_RUNBOOK-render-verify.md",
    "_RUNBOOK-capture-ritual.md",
)
FENCE_LINES_PER_RUNBOOK = 6


class BriefError(Exception):
    """A named, loud failure. Never raised with a bare count."""


class Defect:
    """One named parse failure. Carries WHERE — nothing is reported as a bare count."""

    def __init__(self, path, lineno, reason, excerpt=""):
        self.path, self.lineno, self.reason, self.excerpt = path, lineno, reason, excerpt

    def __str__(self):
        ex = (" · " + self.excerpt[:100]) if self.excerpt else ""
        return "  ⛔ %s:%d — %s%s" % (self.path, self.lineno, self.reason, ex)


# ---- THE REGION TABLE — the single source for the writer, for --regions and for the parser ----

class Region:
    def __init__(self, name, owner, source, builder=None):
        self.name, self.owner, self.source, self.builder = name, owner, source, builder

    @property
    def written(self):
        return self.owner == MACHINE


def _later(fn_name):
    """Bind a builder by name so REGIONS can be declared above the builders it points at."""
    return lambda ctx, _n=fn_name: globals()[_n](ctx)


REGIONS = [
    Region("TITLE-GOVERNANCE", MACHINE,
           "ruling id · programme brief path · store row · generator provenance",
           _later("build_title")),
    Region("THE-JOB", HUMAN,
           "the conductor writes it; the generator never invents scope"),
    Region("PREMISE-TABLE", MACHINE,
           "the registry's sandbox probes RUN at mint; each row = command · rc · timestamp",
           _later("build_premise")),
    Region("OPEN-ITEMS", MACHINE,
           "knowledge/_state.json", _later("build_open_items")),
    Region("DO-NOT-RULE", MACHINE,
           "store items state=open+owner=dave · rulings carrying a non-empty `open` field",
           _later("build_do_not_rule")),
    Region("DO-NOT-RULE-APPEND", HUMAN,
           "the lane-specific block derivable from neither store — survives re-mint"),
    Region("FENCES-ENVIRONMENT", MACHINE,
           "knowledge/_RUNBOOK-*.md extraction + the environment measured at mint",
           _later("build_fences")),
    Region("RETURN-CONTRACT", HUMAN,
           "what the sub owes back"),
]
BY_NAME = {r.name: r for r in REGIONS}


def regions_written():
    """The names this generator WRITES. `--regions` and the writer both read THIS."""
    return [r.name for r in REGIONS if r.written]


def regions_preserved():
    return [r.name for r in REGIONS if not r.written]


# ---- markers + checksum -------------------------------------------------------------------

BEGIN_RE = re.compile(
    r"^<!-- GEN-BRIEF BEGIN (?P<name>[A-Z0-9-]+) · owner=(?P<owner>machine|human) "
    r"· sha256=(?P<sha>[0-9a-f]{64}|NONE-HUMAN-OWNED) · writer=(?P<writer>\S+) -->$")
END_RE = re.compile(r"^<!-- GEN-BRIEF END (?P<name>[A-Z0-9-]+) -->$")


def body_sha(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def begin_marker(region, body):
    sha = body_sha(body) if region.written else HUMAN_SHA
    writer = WRITER if region.written else "none"
    return ("<!-- GEN-BRIEF BEGIN %s · owner=%s · sha256=%s · writer=%s -->"
            % (region.name, region.owner, sha, writer))


def end_marker(region):
    return "<!-- GEN-BRIEF END %s -->" % region.name


class Parsed:
    def __init__(self, name, owner, declared_sha, body, begin_line, end_line):
        self.name, self.owner, self.declared_sha = name, owner, declared_sha
        self.body, self.begin_line, self.end_line = body, begin_line, end_line


def parse_regions(text, path="<mem>"):
    """STRUCTURED PARSE in the consumer's grammar — not a grep [[no-gate-parses-the-artefact]].

    Returns `(regions: list[Parsed], defects: list[Defect])`. Every failure is NAMED and carries
    its line number. Text outside any region is a defect: the brief has legal homes for human
    prose (the human regions), so a stray paragraph between regions is an edit that a re-mint
    would silently drop — and a silently dropped edit is the failure this whole file exists to
    prevent.
    """
    out, defects = [], []
    cur = None
    body = []
    for i, line in enumerate(text.splitlines(), start=1):
        mb = BEGIN_RE.match(line)
        me = END_RE.match(line)
        if mb:
            if cur is not None:
                defects.append(Defect(path, i, "region %s BEGIN inside open region %s — nesting "
                                               "is not legal" % (mb.group("name"), cur["name"])))
                continue
            name = mb.group("name")
            if name not in BY_NAME:
                defects.append(Defect(path, i, "unknown region name %r — the legal names are %s"
                                      % (name, ", ".join(BY_NAME))))
                continue
            if any(p.name == name for p in out):
                defects.append(Defect(path, i, "duplicate region %s — each region appears once"
                                      % name))
                continue
            declared_owner = mb.group("owner")
            if declared_owner != BY_NAME[name].owner:
                defects.append(Defect(path, i, "region %s declares owner=%s; the generator's "
                                               "table says owner=%s — ownership is not editable "
                                               "in the artefact"
                                      % (name, declared_owner, BY_NAME[name].owner)))
            cur = {"name": name, "owner": declared_owner, "sha": mb.group("sha"), "line": i}
            body = []
            continue
        if me:
            if cur is None:
                defects.append(Defect(path, i, "region END %s with no open BEGIN"
                                      % me.group("name")))
                continue
            if me.group("name") != cur["name"]:
                defects.append(Defect(path, i, "region END %s closes open region %s"
                                      % (me.group("name"), cur["name"])))
                cur = None
                continue
            out.append(Parsed(cur["name"], cur["owner"], cur["sha"], "\n".join(body),
                              cur["line"], i))
            cur = None
            continue
        if cur is None:
            if line.strip():
                defects.append(Defect(path, i, "ORPHAN TEXT outside every region — the legal "
                                               "homes for human prose are the human-owned "
                                               "regions (%s)" % ", ".join(regions_preserved()),
                                      line.strip()))
        else:
            body.append(line)
    if cur is not None:
        defects.append(Defect(path, cur["line"], "region %s is never closed" % cur["name"]))
    missing = [n for n in BY_NAME if not any(p.name == n for p in out)]
    if missing:
        defects.append(Defect(path, 0, "region(s) absent from the artefact: %s"
                              % ", ".join(sorted(missing))))
    return out, defects


def machine_mismatches(parsed, eq=operator.eq):
    """Names of MACHINE regions whose body no longer matches its declared checksum.

    `eq` is injectable ONLY so the selftest can mutate the comparison and prove the green arm's
    detection depends on it [[mutation-tests-the-clause-not-the-feature]].
    """
    bad = []
    for p in parsed:
        if BY_NAME[p.name].owner != MACHINE:
            continue
        if not eq(body_sha(p.body), p.declared_sha):
            bad.append(p)
    return bad


# ---- measured inputs ------------------------------------------------------------------------

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sh(args, cwd=ROOT, timeout=90):
    """Run and return (rc, stdout+stderr). A crash is not a fail: a timeout or a missing binary
    is reported as its own named rc string, never as a silent empty result."""
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return "TIMEOUT(%ss)" % timeout, "⛔ the command did not return inside %ss" % timeout
    except FileNotFoundError as e:
        return "NO-SUCH-BINARY", "⛔ %s" % e


def load_json(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:  # noqa: BLE001 — a crash is not a fail: name the file and the reason
        raise BriefError("cannot read %s (%s): %s" % (path, what, e))


def read_manifest(reg_dir):
    """The registry manifest, or a COULD-NOT-ASK if the directory is not reachable."""
    path = os.path.join(reg_dir, "manifest.jsonl")
    if not os.path.isdir(reg_dir) or not os.path.exists(path):
        return None, path
    rows = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, start=1):
            s = line.strip()
            if not s or s.startswith("//"):
                continue
            try:
                rows.append(json.loads(s))
            except json.JSONDecodeError as e:
                raise BriefError("manifest.jsonl:%d does not parse — %s" % (i, e))
    return rows, path


class Ctx:
    """Everything the region builders read. Built once per mint, at mint time."""

    def __init__(self, lane_id, out_rel, reg_dir=REGDIR, session=None):
        self.lane_id = lane_id
        self.out_rel = out_rel
        self.reg_dir = reg_dir
        self.session = session
        self.minted_at = now_iso()
        self.store = load_json(STORE, "the open-items store")
        self.rulings = load_json(RULINGS, "the rulings store")["rulings"]
        self.lanes = load_json(LANES, "the lane records")["lanes"]
        self.lane = next((l for l in self.lanes if l.get("id") == lane_id), None)
        if self.lane is None:
            raise BriefError("no lane %r in knowledge/_lanes.json — the ids are: %s"
                             % (lane_id, ", ".join(l.get("id", "?") for l in self.lanes)))
        self.manifest, self.manifest_path = read_manifest(reg_dir)
        self.probe_rows = None  # filled by build_premise; probes run exactly once per mint


# ---- region builders --------------------------------------------------------------------------

def build_title(ctx):
    rc_head, head = sh(["git", "log", "--oneline", "-1"])
    head = head.strip().splitlines()[0] if head.strip() else "UNKNOWN"
    if rc_head != 0:
        head = "UNKNOWN (git log rc=%s) — never defaulted" % rc_head
    return "\n".join([
        "# PM brief — lane `%s` (%s)" % (ctx.lane_id, ctx.lane.get("name", "?")),
        "",
        "> ⛔ **THIS FILE IS A DATED PERIOD RECORD, NOT A LIVE HOME.** It was minted at "
        "`%s` by `%s`." % (ctx.minted_at, WRITER),
        "> **The store stays the one live home** (`knowledge/_state.json`, "
        "`knowledge/_rulings.json`). ADR-0017 / [[write-once-principle-floated-192]]: "
        "nothing in this brief may be cited as the source of a live fact — re-ask the store.",
        "> **Nothing generated here is a ruling.** Only `knowledge/_inscribe_ruling.py` writes "
        "`knowledge/_rulings.json`, and only on Dave's word.",
        "",
        "| governance | value |",
        "|---|---|",
        "| ruling this brief serves | `s204-D1` item 4 (mint-time brief generation) |",
        "| programme brief | `notes/_briefs/2026-08-19-207-w46-three-scoped-proposals-v1.md` "
        "§ PROPOSAL 2 |",
        "| generator | `%s` — run `python3 %s --regions` to see exactly what it overwrites |"
        % (WRITER, WRITER),
        "| this artefact | `%s` |" % ctx.out_rel,
        "| lane record | `knowledge/_lanes.json` → `%s` · state `%s` |"
        % (ctx.lane_id, ctx.lane.get("state", "?")),
        "| lane born | %s |" % ctx.lane.get("born", "—"),
        "| lane until | %s |" % ctx.lane.get("until", "—"),
        "| repo HEAD at mint | `%s` |" % head,
        "",
        "**Lane sequence, as the lane record has it** (state is the record's word, not a "
        "reading of it):",
        "",
    ] + [
        "- `%s` — %s" % (s.get("state", "?"), s.get("step", "?"))
        for s in ctx.lane.get("sequence", [])
    ] or ["- (the lane record carries no `sequence`)"])


def run_probes(ctx):
    """Run every `environment == sandbox` probe in the manifest; DECLARE every other one.

    ⛔ Which probes run is derived from the manifest's own `environment` field — not from a list
    typed into this file, which would drift the moment a probe is added.
    """
    rows = []
    for p in ctx.manifest:
        pid = p.get("id", "?")
        script = p.get("script", "?")
        argv = p.get("argv") or ["--check"]
        rel = os.path.relpath(os.path.join(ctx.reg_dir, script), ROOT)
        cmd = "python3 %s %s" % (rel, " ".join(argv))
        env = p.get("environment", "unknown")
        if env != "sandbox":
            rows.append({
                "id": pid, "title": p.get("title", ""), "env": env, "cmd": cmd,
                "rc": "NOT RUN AT MINT", "ts": ctx.minted_at, "wall": "—",
                "line": "NOT RUN AT MINT — environment `%s`. This probe cannot be asked in a "
                        "plain shell; see `s204-D1` item 5 (the CI pixel leg). A DECLARED GAP, "
                        "never an omission." % env,
                "declared_only": True,
            })
            continue
        t0 = datetime.datetime.now()
        ts = now_iso()
        rc, out = sh(["python3", os.path.join(ctx.reg_dir, script), *argv])
        wall = "%.2fs" % (datetime.datetime.now() - t0).total_seconds()
        lines = [l for l in out.splitlines() if l.strip()]
        verbatim = next((l for l in reversed(lines) if "findings=" in l),
                        lines[-1] if lines else "(the probe printed nothing)")
        if cna.is_refusal(rc):
            verbatim = next((l for l in lines if l.startswith(cna.MARKER)), verbatim)
        rows.append({
            "id": pid, "title": p.get("title", ""), "env": env, "cmd": cmd,
            "rc": rc, "ts": ts, "wall": wall, "line": verbatim.strip(),
            "declared_only": False,
        })
    return rows


def p3_declared(rows, manifest):
    """True iff every non-sandbox probe IN THE MANIFEST has a DECLARED row in `rows`.

    ⛔ The expected population is taken from the MANIFEST, never from `rows` — a clause that
    derives its own expectation from the thing it is checking cannot see an omission, which is
    exactly the failure the first draft of this function had and the mutation arm caught.
    """
    expected = [p.get("id") for p in manifest if p.get("environment") != "sandbox"]
    return all(any(r["id"] == pid and r["declared_only"] for r in rows) for pid in expected)


def build_premise(ctx):
    if ctx.probe_rows is None:
        ctx.probe_rows = run_probes(ctx)
    rows = ctx.probe_rows
    if not p3_declared(rows, ctx.manifest):
        raise BriefError("a non-sandbox probe has no DECLARED row — the premise table would "
                         "ship a silent omission. Refusing to mint.")
    head = [
        "## PREMISE TABLE — every row was RE-MEASURED at mint",
        "",
        "⛔ **No row carries a summary word.** Each row prints the COMMAND, the RETURN CODE, the "
        "TIMESTAMP and the probe's own last line VERBATIM. A row a reader cannot re-run is a "
        "claim, not a measurement (`s182-D1`, [[measure-dont-convert-units]]). Read the rc; do "
        "not read a mood into it.",
        "",
        "Population: every probe in `%s` — probes whose `environment` is `sandbox` were RUN; "
        "every other probe is a DECLARED, NOT-RUN row." % os.path.relpath(ctx.manifest_path, ROOT),
        "",
        "| probe | command | rc | timestamp | wall | the probe's own last line |",
        "|---|---|---|---|---|---|",
    ]
    body = ["| `%s` | `%s` | `%s` | `%s` | %s | %s |"
            % (r["id"], r["cmd"], r["rc"], r["ts"], r["wall"],
               r["line"].replace("|", "\\|"))
            for r in rows]
    tail = [
        "",
        "**How to read an rc**, in this repo's ruled vocabulary: `0` the probe ran and reported "
        "`findings=0` · `1` the probe ran and MEASURED something · `77` COULD-NOT-ASK "
        "(`s193-D1`, `knowledge/_could_not_ask.py`) — the probe could not reach its input and "
        "said so; that is a third verdict, not a pass and not a failure.",
        "⚠ A green premise table means THESE PROBES RAN. It does not mean the tree is clean "
        "[[green-tests-cannot-see-scope]] — every probe's `blind` field in the manifest names "
        "what it cannot see, and free hunting is still owed.",
    ]
    return "\n".join(head + body + tail)


def build_open_items(ctx):
    items = ctx.store["items"]
    live = [i for i in items if i.get("state") in ("open", "blocked", "parked")]
    unconditioned = [i for i in items if i.get("condition") == "UNCONDITIONED"]
    out = [
        "## OPEN ITEMS — read from `knowledge/_state.json` at mint",
        "",
        "Counts are GENERATED, never typed: **%d items total · %d live · %d open · %d blocked · "
        "%d parked**, measured at `%s`."
        % (len(items), len(live),
           sum(1 for i in items if i.get("state") == "open"),
           sum(1 for i in items if i.get("state") == "blocked"),
           sum(1 for i in items if i.get("state") == "parked"), ctx.minted_at),
        "",
        "| id | owner | state | condition | title |",
        "|---|---|---|---|---|",
    ]
    for i in sorted(live, key=lambda x: x.get("id", "")):
        out.append("| `%s` | %s | %s | %s | %s |"
                   % (i.get("id"), i.get("owner"), i.get("state"), i.get("condition"),
                      str(i.get("title", "")).replace("|", "\\|")))
    out += [
        "",
        "### DECLARED DEBT — %d item(s) are `condition: UNCONDITIONED`" % len(unconditioned),
        "",
        "These are the frozen legacy set: items opened without a stated close condition. They "
        "are PRINTED, never omitted — a declared gap passes, a silent one fails. An agent may "
        "not invent Dave's close conditions.",
        "",
        "`" + "` · `".join(i.get("id", "?") for i in
                           sorted(unconditioned, key=lambda x: x.get("id", ""))) + "`",
    ]
    return "\n".join(out)


def build_do_not_rule(ctx):
    items = ctx.store["items"]
    daves = [i for i in items if i.get("state") == "open" and i.get("owner") == "dave"]
    open_rulings = [r for r in ctx.rulings if str(r.get("open") or "").strip()]
    by_counter = {}
    for r in ctx.rulings:
        by_counter[r.get("by")] = by_counter.get(r.get("by"), 0) + 1
    by_str = " · ".join("%s=%d" % (k, v) for k, v in sorted(by_counter.items(),
                                                            key=lambda kv: -kv[1]))
    out = [
        "## DO-NOT-RULE — generated half",
        "",
        "⛔ **`by: Dave` IS NOT USED AS A FILTER, and that is a correction to `s204-D1`'s own "
        "item-4 wording.** Measured at mint over `knowledge/_rulings.json`: **%s** across %d "
        "rulings. A field with one value selects everything and is therefore not a filter "
        "(#207 finding (b))." % (by_str, len(ctx.rulings)),
        "",
        "The two generated sources are:",
        "",
        "**1 · Store items `state=open` AND `owner=dave` — %d item(s):**" % len(daves),
        "",
        "| id | condition | title |",
        "|---|---|---|",
    ]
    for i in sorted(daves, key=lambda x: x.get("id", "")):
        out.append("| `%s` | %s | %s |" % (i.get("id"), i.get("condition"),
                                           str(i.get("title", "")).replace("|", "\\|")))
    out += [
        "",
        "**2 · Rulings carrying a non-empty `open` field — %d of %d:**"
        % (len(open_rulings), len(ctx.rulings)),
        "",
        "| ruling | ruled | what is still open, in the ruling's own words |",
        "|---|---|---|",
    ]
    for r in open_rulings:
        txt = str(r.get("open")).replace("|", "\\|").replace("\n", " ")
        out.append("| `%s` | %s | %s |" % (r.get("id"), r.get("ruled"),
                                           txt if len(txt) <= 400 else txt[:397] + "…"))
    out += [
        "",
        "⚠ **THIS LIST IS NOT COMPLETE AND CANNOT BE.** It sees two stores. It cannot see memory "
        "hooks, a ruling Dave made in chat that is not yet inscribed, or a lane-specific "
        "do-not-rule item nobody has written into a store. That is what the human-appended "
        "block below is for — and a generated list that silently loses an entry is worse than a "
        "hand list, because nobody notices the gap.",
    ]
    return "\n".join(out)


def build_fences(ctx):
    rc_head, head = sh(["git", "rev-parse", "--short", "HEAD"])
    head = head.strip() if rc_head == 0 else "UNKNOWN (git rc=%s) — never defaulted" % rc_head
    rc_st, st = sh(["git", "status", "--short"])
    dirty = len([l for l in st.splitlines() if l.strip()]) if rc_st == 0 else "UNKNOWN"
    out = [
        "## FENCES + ENVIRONMENT — extracted at mint",
        "",
        "### Environment, measured",
        "",
        "| fact | value | how it was taken |",
        "|---|---|---|",
        "| minted at | `%s` | the generator's clock |" % ctx.minted_at,
        "| python | `%s` | `sys.version.split()[0]` |" % sys.version.split()[0],
        "| platform | `%s` | `sys.platform` |" % sys.platform,
        "| repo root | `%s` | resolved from `%s` |" % (ROOT, WRITER),
        "| HEAD | `%s` | `git rev-parse --short HEAD` (rc=%s) |" % (head, rc_head),
        "| dirty paths | `%s` | `git status --short` (rc=%s) |" % (dirty, rc_st),
        "",
        "⚠ **Sandbox warts that bite every sub, replayed:** nothing survives a tool-call "
        "boundary (~45s wall) — chunk long builds; `/tmp` may be full, scratch in `/var/tmp`; "
        "`git checkout -- <path>` cannot restore a file on this mount (`git show HEAD:<path> > "
        "<path>` is the working revert); `rm` inside `.git` is denied, `mv` is not.",
        "",
        "### Runbooks in the tree",
        "",
        "| runbook | bytes | mtime |",
        "|---|---|---|",
    ]
    books = sorted(f for f in os.listdir(KNOW) if f.startswith("_RUNBOOK-") and f.endswith(".md"))
    for b in books:
        p = os.path.join(KNOW, b)
        stt = os.stat(p)
        out.append("| `knowledge/%s` | %d | %s |"
                   % (b, stt.st_size,
                      datetime.datetime.fromtimestamp(stt.st_mtime).isoformat(timespec="seconds")))
    out += [
        "",
        "### ⛔ lines extracted from the declared runbook subset",
        "",
        "Glob: `%s` — a DECLARED subset of the %d runbooks above, not all of them. Each line is "
        "quoted VERBATIM with its `path:line` so it can be re-read in place; the per-runbook "
        "count says how many were found and how many are shown."
        % (" · ".join(FENCE_RUNBOOKS), len(books)),
        "",
    ]
    for b in FENCE_RUNBOOKS:
        p = os.path.join(KNOW, b)
        if not os.path.exists(p):
            out.append("- ⛔ `knowledge/%s` — NOT PRESENT in the tree at mint (not silently "
                       "skipped)" % b)
            continue
        hits = [(i, l.strip()) for i, l in
                enumerate(open(p, encoding="utf-8").read().splitlines(), start=1) if "⛔" in l]
        out.append("**`knowledge/%s`** — %d ⛔ line(s) found, %d shown:"
                   % (b, len(hits), min(len(hits), FENCE_LINES_PER_RUNBOOK)))
        out.append("")
        for i, l in hits[:FENCE_LINES_PER_RUNBOOK]:
            out.append("- `knowledge/%s:%d` — %s" % (b, i, l if len(l) <= 300 else l[:297] + "…"))
        out.append("")
    out += [
        "### ⛔ WHAT THIS GENERATOR CANNOT SEE",
        "",
        "It rules only as wide as what it reads [[gate-glob-scope-rule]]: "
        "`knowledge/_state.json`, `knowledge/_rulings.json`, `knowledge/_lanes.json`, "
        "`knowledge/_probe_registry/manifest.jsonl` and `knowledge/_RUNBOOK-*.md`. **Memory "
        "hooks live outside the repo entirely. A ruling made in chat and not yet inscribed is "
        "invisible. Anything a human knows and has not written into a store is invisible.** "
        "Treat every region below as a floor, not a ceiling.",
    ]
    return "\n".join(out)


# ---- human region defaults (written ONCE, on first mint; never rewritten) ---------------------

HUMAN_DEFAULTS = {
    "THE-JOB": (
        "## THE JOB — human-owned\n\n"
        "*The generator never invents scope. Write the job here, in plain prose, in the words "
        "you would say out loud. This block is HUMAN-OWNED: `%s` will never read it, never "
        "validate it and never rewrite it — it is carried byte-for-byte across every re-mint.*\n"
        % WRITER),
    "DO-NOT-RULE-APPEND": (
        "## DO-NOT-RULE — human-appended half\n\n"
        "*The generated half above sees two stores. Everything else goes here: the lane-specific "
        "items, the questions already put to Dave, the vocabulary calls, the choices a sub must "
        "return rather than settle. HUMAN-OWNED — carried byte-for-byte across re-mint.*\n\n"
        "- (append lane items here)\n"),
    "RETURN-CONTRACT": (
        "## RETURN CONTRACT — human-owned\n\n"
        "*What the sub owes back: the claim table with a probeable token per claim (`s182-D1`), "
        "the paths, what was driven and what refused, the commit hash and the subject read back "
        "from `git log` as TEXT, what stays UNPROVEN. HUMAN-OWNED — never touched on re-mint.*\n"),
}


# ---- the writer -------------------------------------------------------------------------------

def render(ctx, carried=None):
    """Return (text, names_written). `carried` maps human region name → its preserved body."""
    carried = carried or {}
    chunks, written = [], []
    for r in REGIONS:
        if r.written:
            body = r.builder(ctx)
            written.append(r.name)
        else:
            body = carried.get(r.name, HUMAN_DEFAULTS[r.name].rstrip("\n"))
        chunks.append("%s\n%s\n%s" % (begin_marker(r, body), body, end_marker(r)))
    return "\n\n".join(chunks) + "\n", written


def mint(lane_id, out_path, reg_dir=REGDIR, stream=None):
    """Mint or re-mint. Returns (rc, names_written). Every refusal is loud and NAMED."""
    out = stream or sys.stdout
    out_rel = os.path.relpath(os.path.abspath(out_path), ROOT)

    manifest, mpath = read_manifest(reg_dir)
    if manifest is None:
        return cna.refuse(
            out_rel,
            "the probe registry manifest is not reachable at `%s`, so the PREMISE TABLE cannot "
            "be measured. A brief minted without re-run probes would carry premises nobody "
            "measured, which is the whole defect this generator exists to close. Reachable "
            "wherever `knowledge/_probe_registry/` is checked out." % mpath,
            stream=out), []

    carried = {}
    if os.path.exists(out_path):
        existing = open(out_path, encoding="utf-8").read()
        parsed, defects = parse_regions(existing, out_rel)
        if defects:
            print("⛔ REFUSED — `%s` does not parse as a gen_brief artefact:" % out_rel, file=out)
            for d in defects:
                print(str(d), file=out)
            print("  Nothing was written. Fix the file, or mint to a NEW dated path (a brief is "
                  "a dated period record — a second file is a legal answer).", file=out)
            return 1, []
        bad = machine_mismatches(parsed)
        if bad:
            print("⛔ REFUSED — a MACHINE-OWNED region was hand-edited. Nothing was written.",
                  file=out)
            for p in bad:
                print("  ⛔ %s:%d-%d — region `%s` (owner=machine) no longer matches its declared "
                      "checksum: declared sha256=%s, on-disk sha256=%s"
                      % (out_rel, p.begin_line, p.end_line, p.name, p.declared_sha[:16] + "…",
                         body_sha(p.body)[:16] + "…"), file=out)
            print("  This generator will NOT overwrite a human edit. The two legal moves: "
                  "(1) move the edit into a human-owned region (%s) and restore the machine "
                  "text — `git show HEAD:%s > %s` restores it on this mount; or (2) mint to a "
                  "NEW dated path and leave this one as the period record it is."
                  % (", ".join(regions_preserved()), out_rel, out_rel), file=out)
            print("  Run `python3 %s --regions` to see exactly which regions are machine-owned."
                  % WRITER, file=out)
            return 1, []
        for p in parsed:
            if BY_NAME[p.name].owner == HUMAN:
                carried[p.name] = p.body  # carried VERBATIM: not parsed, not validated

    ctx = Ctx(lane_id, out_rel, reg_dir=reg_dir)
    text, written = render(ctx, carried)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return 0, written


# ---- --regions (THE FENCE) -----------------------------------------------------------------

def print_regions(stream=None):
    out = stream or sys.stdout
    print("REGIONS OF A gen_brief ARTEFACT — derived from the writer's own table "
          "(`REGIONS` in %s), not a second list." % WRITER, file=out)
    print("", file=out)
    print("%-20s %-8s %-10s %s" % ("region", "owner", "on re-mint", "source"), file=out)
    print("%-20s %-8s %-10s %s" % ("-" * 20, "-" * 8, "-" * 10, "-" * 40), file=out)
    for r in REGIONS:
        print("%-20s %-8s %-10s %s"
              % (r.name, r.owner, "OVERWRITTEN" if r.written else "preserved", r.source),
              file=out)
    print("", file=out)
    print("WRITTEN   (this generator overwrites these, every mint): %s"
          % " ".join(regions_written()), file=out)
    print("PRESERVED (never read, never validated, never rewritten): %s"
          % " ".join(regions_preserved()), file=out)
    print("", file=out)
    print("⛔ A machine region whose body no longer matches its declared sha256 is a HUMAN EDIT: "
          "the generator refuses and names the region rather than overwriting it.", file=out)
    return 0


# ---- selftest ---------------------------------------------------------------------------------

def selftest():
    """Drives the REAL generator on the REAL stores, in a temp output path.

    Every green arm has a mutation control that makes it provably able to fail.
    """
    fails = []

    def bite(name, ok, detail=""):
        detail = "" if detail is None else str(detail)
        print(("  ✓ " if ok else "  ✗ ") + name + (("  — " + detail) if detail else ""))
        if not ok:
            fails.append(name)

    tmp = tempfile.mkdtemp(prefix="gen_brief_selftest_", dir="/var/tmp")
    path = os.path.join(tmp, "brief.md")
    lane = "lane-2-apollo-charts"

    print("A · MINT and STRUCTURED PARSE (the consumer's grammar, not a grep)")
    rc, written = mint(lane, path)
    bite("first mint returns rc 0", rc == 0, "rc=%s" % rc)
    text = open(path, encoding="utf-8").read()
    parsed, defects = parse_regions(text, path)
    bite("the artefact parses with 0 defects", not defects,
         "; ".join(str(d) for d in defects))
    bite("all %d regions present, in table order" % len(REGIONS),
         [p.name for p in parsed] == [r.name for r in REGIONS],
         str([p.name for p in parsed]))
    bite("declared owners match the generator's table",
         all(p.owner == BY_NAME[p.name].owner for p in parsed))
    bite("every machine region's checksum verifies on a fresh mint",
         not machine_mismatches(parsed))

    print("B · --regions IS THE FENCE (derived from the same table as the writer)")
    bite("names --regions reports WRITTEN == names mint() reported writing",
         regions_written() == written, "%s vs %s" % (regions_written(), written))
    import io
    buf = io.StringIO()
    print_regions(buf)
    rep = buf.getvalue()
    bite("--regions output names every machine region as OVERWRITTEN",
         all(re.search(r"^%s\s+machine\s+OVERWRITTEN" % n, rep, re.M) for n in regions_written()))
    bite("--regions output names every human region as preserved",
         all(re.search(r"^%s\s+human\s+preserved" % n, rep, re.M)
             for n in regions_preserved()))

    print("C · PREMISE TABLE — command · rc · timestamp, and P-3 declared not omitted")
    prem = next(p for p in parsed if p.name == "PREMISE-TABLE")
    bite("P-3 appears as a DECLARED NOT-RUN row, never omitted",
         "`P-3`" in prem.body and "NOT RUN AT MINT" in prem.body)
    bite("every sandbox probe row carries a `python3 knowledge/_probe_registry/` command",
         prem.body.count("python3 knowledge/_probe_registry/") >= 5)
    bite("no summary word in the premise rows (no bare PASS/clean/OK verdicts written by us)",
         not re.search(r"\|\s*(PASS|CLEAN|OK|no findings)\s*\|", prem.body, re.I))
    fake_manifest = [{"id": "P-X", "environment": "sandbox-render"},
                     {"id": "P-1", "environment": "sandbox"}]
    ctx_rows = [{"id": "P-X", "env": "sandbox-render", "declared_only": True},
                {"id": "P-1", "env": "sandbox", "declared_only": False}]
    bite("p3_declared() PASSES when the non-sandbox probe has a declared row",
         p3_declared(ctx_rows, fake_manifest))
    bite("MUTATION — p3_declared() FAILS when that row is dropped",
         not p3_declared([r for r in ctx_rows if r["env"] == "sandbox"], fake_manifest))
    bite("MUTATION — p3_declared() FAILS when the row is present but not marked declared",
         not p3_declared([{**r, "declared_only": False} for r in ctx_rows], fake_manifest))

    print("D · CLEAN RE-MINT is quiet, and human regions survive byte-for-byte")
    human_before = {p.name: p.body for p in parsed if BY_NAME[p.name].owner == HUMAN}
    buf2 = io.StringIO()
    rc2, written2 = mint(lane, path, stream=buf2)
    bite("clean re-mint returns rc 0", rc2 == 0, "rc=%s" % rc2)
    bite("clean re-mint prints NOTHING (silent)", buf2.getvalue() == "",
         repr(buf2.getvalue()[:120]))
    parsed2, defects2 = parse_regions(open(path, encoding="utf-8").read(), path)
    bite("re-minted artefact still parses with 0 defects", not defects2)
    human_after = {p.name: p.body for p in parsed2 if BY_NAME[p.name].owner == HUMAN}
    bite("human regions byte-identical across re-mint", human_before == human_after)

    print("E · A HUMAN EDIT IN A HUMAN REGION is preserved, not refused")
    t = open(path, encoding="utf-8").read()
    marker = "- (append lane items here)"
    t = t.replace(marker, marker + "\n- W-99 the vocabulary question is DAVE'S, do not settle it")
    open(path, "w", encoding="utf-8").write(t)
    buf3 = io.StringIO()
    rc3, _ = mint(lane, path, stream=buf3)
    bite("re-mint after a HUMAN-region edit returns rc 0", rc3 == 0, buf3.getvalue()[:200])
    bite("the human edit survives verbatim",
         "W-99 the vocabulary question is DAVE'S" in open(path, encoding="utf-8").read())

    print("F · A HUMAN EDIT IN A MACHINE REGION — the named refusal MUST fire")
    t = open(path, encoding="utf-8").read()
    victim = "OPEN-ITEMS"
    pv = next(p for p in parse_regions(t, path)[0] if p.name == victim)
    hand = pv.body.replace("## OPEN ITEMS", "## OPEN ITEMS (I edited this by hand)", 1)
    bite("the plant actually changed the machine body", hand != pv.body)
    t2 = t.replace(pv.body, hand, 1)
    open(path, "w", encoding="utf-8").write(t2)
    buf4 = io.StringIO()
    rc4, written4 = mint(lane, path, stream=buf4)
    msg = buf4.getvalue()
    bite("re-mint REFUSES with rc 1", rc4 == 1, "rc=%s" % rc4)
    bite("the refusal NAMES the region", victim in msg, msg.splitlines()[:2])
    bite("the refusal says nothing was written", "Nothing was written" in msg)
    bite("the refusal names the legal moves", "legal moves" in msg)
    bite("the hand edit was NOT overwritten",
         "(I edited this by hand)" in open(path, encoding="utf-8").read())
    bite("nothing was reported as written", written4 == [])
    parsed4, _ = parse_regions(open(path, encoding="utf-8").read(), path)
    bite("MUTATION — with an always-equal comparison the SAME plant is NOT caught "
         "(so the green above is the checksum, not a tautology)",
         machine_mismatches(parsed4, eq=lambda a, b: True) == [])
    bite("CONTROL — the real comparison DOES catch it",
         [p.name for p in machine_mismatches(parsed4)] == [victim])

    print("G · ORPHAN TEXT outside every region is a named parse defect")
    t3 = open(path, encoding="utf-8").read().replace(hand, pv.body, 1)  # restore machine text
    open(path, "w", encoding="utf-8").write(t3)
    buf5 = io.StringIO()
    rc5, _ = mint(lane, path, stream=buf5)
    bite("restoring the machine text clears the refusal", rc5 == 0, buf5.getvalue()[:200])
    t4 = open(path, encoding="utf-8").read()
    t4 = t4.replace(end_marker(BY_NAME["THE-JOB"]),
                    end_marker(BY_NAME["THE-JOB"]) + "\n\nI wrote this between two regions.", 1)
    open(path, "w", encoding="utf-8").write(t4)
    _, d6 = parse_regions(t4, path)
    bite("orphan text is a defect", any("ORPHAN TEXT" in str(d) for d in d6))
    bite("the orphan defect carries a line number",
         any("ORPHAN TEXT" in str(d) and d.lineno > 0 for d in d6))
    buf6 = io.StringIO()
    rc6, _ = mint(lane, path, stream=buf6)
    bite("mint REFUSES rc 1 on an unparseable artefact", rc6 == 1, "rc=%s" % rc6)
    bite("MUTATION CONTROL — the same text WITHOUT the orphan line parses clean",
         not parse_regions(t4.replace("\n\nI wrote this between two regions.", "", 1), path)[1])

    print("H · COULD-NOT-ASK (`s193-D1`) — keyed on the unreachable INPUT, never on the runner")
    buf7 = io.StringIO()
    rc7, _ = mint(lane, os.path.join(tmp, "cna.md"),
                  reg_dir=os.path.join(tmp, "no-such-registry"), stream=buf7)
    bite("an unreachable probe registry REFUSES with rc 77", cna.is_refusal(rc7), "rc=%s" % rc7)
    bite("its first line carries the COULD-NOT-ASK marker",
         buf7.getvalue().startswith(cna.MARKER), buf7.getvalue()[:120])
    bite("no artefact was written on the refusal",
         not os.path.exists(os.path.join(tmp, "cna.md")))
    bite("CONTROL — with the real registry reachable the same call mints",
         mint(lane, os.path.join(tmp, "cna.md"))[0] == 0)

    print("I · A MISSING LANE fails loud and NAMED (never a plausible empty brief)")
    try:
        Ctx("lane-does-not-exist", "x.md")
        bite("unknown lane raises", False)
    except BriefError as e:
        bite("unknown lane raises BriefError naming the legal ids",
             "lane-2-apollo-charts" in str(e))

    print("")
    if fails:
        print("✗ gen_brief selftest: %d ARM(S) FAILED — %s" % (len(fails), "; ".join(fails)))
        return 1
    print("✓ gen_brief selftest: all arms green (mutation controls included). Scratch: %s" % tmp)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=False, description="mint-time PM brief generation")
    ap.add_argument("--regions", action="store_true",
                    help="print exactly which regions this generator writes")
    ap.add_argument("--mint", action="store_true", help="mint or re-mint a brief")
    ap.add_argument("--lane", help="lane id from knowledge/_lanes.json")
    ap.add_argument("--out", help="output path for the brief")
    ap.add_argument("--parse", help="structured-parse an existing brief; write nothing")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.regions:
        return print_regions()
    if args.selftest:
        return selftest()
    if args.parse:
        text = open(args.parse, encoding="utf-8").read()
        parsed, defects = parse_regions(text, args.parse)
        for p in parsed:
            ok = "—" if BY_NAME[p.name].owner == HUMAN else (
                "checksum OK" if body_sha(p.body) == p.declared_sha else "⛔ CHECKSUM MISMATCH")
            print("%-20s %-8s lines %4d-%-4d  %s" % (p.name, p.owner, p.begin_line, p.end_line, ok))
        if defects:
            print("⛔ %d parse defect(s):" % len(defects))
            for d in defects:
                print(str(d))
            return 1
        return 1 if machine_mismatches(parsed) else 0
    if args.mint:
        if not args.lane or not args.out:
            print("⛔ --mint needs both --lane and --out", file=sys.stderr)
            return 2
        try:
            rc, _ = mint(args.lane, args.out)
        except BriefError as e:
            print("⛔ REFUSED — %s" % e, file=sys.stderr)
            return 1
        return rc
    print("⛔ nothing asked. Try --regions, --mint --lane <id> --out <path>, --parse <path>, "
          "or --selftest.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
