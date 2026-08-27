#!/usr/bin/env python3
"""_build_memento_index.py — THE INDEX BOOTSTRAP for a fresh project (Gumdrop cut).

Builds `_memento-index.json` beside the Memento door (`_memento_search.py`) so retrieval
can START in a project that is not Apollo. Without it the door refuses, correctly, and
points at a build script the pack does not carry — retrieval, one of the two things
Memento IS, cannot be brought up at all.

⛔ WHY THIS FILE EXISTS, AND WHY IT IS NOT A COPY OF APOLLO'S BUILDER.
`memento-package/machinery/_MACHINERY-MANIFEST.md` states the spec rule for this cut:

    "copies only ... These are VERBATIM copies — Apollo names (GOOD-MORNING.md,
     _LIVE-STATE.md, knowledge/ paths) are still inside them, on purpose.
     Generalisation is a build step, not a copy step; a half-renamed copy would be
     neither auditable nor runnable."

and then lists, in its own ordered "Generalisation debt" list:

    "3. Index bootstrap for a fresh project (the no-chain arm of the ratified boot rule)."

This is that item. The pointer inside `_search_core.py` is NOT the defect — it is the
declared consequence of the verbatim rule, and rewriting it in the pack would be the
half-rename the rule forbids (measured #220: `_build_all.py` is named at 80 sites across
38 packed files). Apollo's own `knowledge/_build_memento_index.py` cannot be shipped
instead: driven in a fresh stage it dies on `_gen_lanes`, and its declared corpus is the
whole Apollo memory — GM/LS archives, the gauge log, the decisions ledger, the briefs,
the lanes and the component registry — none of which an adopting project has, and it
REFUSES when a source class contributes zero. The closure cannot carry a corpus.

WHAT IT INDEXES — declared, and every class is named in the run's own output:

All four are read from THE CUT'S OWN DIRECTORY (the one holding `_GUMDROP-MANIFEST.md`),
which is the same root `_gen_chain.py` reads — so the chain and the index never disagree
about which GOOD-MORNING.md is yours.

  REQUIRED  runbooks/*.md      -> `runbook-section`   (`##`/`###` sections)
  OPTIONAL  GOOD-MORNING.md    -> `gm-section`        (`##` sections, FIRST-SESSION §4b)
  OPTIONAL  _LIVE-STATE.md     -> `ls-section`        (`##` sections, FIRST-SESSION §4b)
  OPTIONAL  _rulings.json      -> `ledger-section`    (one record per ruling)

OPTIONAL means ABSENT-BY-DESIGN on day one: the stores ship empty (`s219-D5` Q1) and the
designer writes GOOD-MORNING/_LIVE-STATE at FIRST-SESSION §4a/§4b. An optional source
that is absent is SKIPPED BY NAME in the printed roster, never silently. An optional
source that is PRESENT and contributes zero records REFUSES — that is a broken parser,
not a quiet corpus. A REQUIRED source missing REFUSES. Zero records overall REFUSES.

⛔ THE KIND CONSTRAINT, DERIVED AND NOT TYPED. `_memento_search.py`'s `bucket_for()`
returns None for any kind outside its `KIND_ORDER`, and `_search_core.search()` SKIPS a
None bucket silently (`_search_core.py:100-101`). A record with a kind the door does not
know is indexed and then invisible. So this builder reads `KIND_ORDER` out of the door
that sits beside it, by AST, at build time, and REFUSES to emit a kind that door does not
carry. The door is the authority on its own vocabulary; nothing here re-states it.

Determinism: records sorted by (file, line, id); duplicate ids suffixed `-2`, `-3` in
document order; `--check` regenerates and byte-compares.

Usage:
  python3 machinery/_build_memento_index.py            # write the index
  python3 machinery/_build_memento_index.py --check    # determinism / staleness gate
  python3 machinery/_build_memento_index.py --selftest # refusal + determinism bites
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import ast, glob as globlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "_memento-index.json")
DOOR_PATH = os.path.join(HERE, "_memento_search.py")

H2_RE = re.compile(r"^##\s")
RUNBOOK_HEADING_RE = re.compile(r"^###?\s")
GENERATED_BY = ("machinery/_build_memento_index.py — never hand-edit; regenerate after any "
                "change to the runbooks, GOOD-MORNING.md, _LIVE-STATE.md or _rulings.json")


# ------------------------------------------------------------------ where the corpus lives
def corpus_root(here=None):
    """The Memento cut's own directory — the nearest ancestor holding `_GUMDROP-MANIFEST.md`.

    Walked, never assumed: the door ships in TWO machinery dirs (`memento-package/machinery`
    and `memento-package/claude-plugin/memento/machinery`) and only one of them has a
    `runbooks/` sibling. A builder that assumed `../runbooks` would refuse in the plugin copy
    for a reason that has nothing to do with the project."""
    d = here or HERE
    while True:
        if os.path.exists(os.path.join(d, "_GUMDROP-MANIFEST.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def door_kinds(door_path=None):
    """`KIND_ORDER` READ OUT OF THE DOOR, by AST — the door owns its vocabulary."""
    p = door_path or DOOR_PATH
    if not os.path.exists(p):
        return None, ("the Memento door is not beside this builder (%s) — an index with no "
                      "door to read it is not a corpus. REFUSING." % os.path.basename(p))
    with open(p, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "KIND_ORDER":
                    try:
                        return set(ast.literal_eval(node.value)), None
                    except ValueError:
                        break
    return None, ("%s carries no literal KIND_ORDER — this builder cannot verify that the "
                  "kinds it emits are ones the door can show. REFUSING." % os.path.basename(p))


# ------------------------------------------------------------------ helpers
def slug(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].strip("-") or "untitled"


def head_of(lines, limit=140):
    for ln in lines:
        t = ln.strip().lstrip("#").strip()
        if t:
            return t[:limit]
    return "(empty)"


def rec(rid, kind, relfile, line, head, text):
    return {"id": rid, "kind": kind, "file": relfile, "line": line, "head": head, "text": text}


def _dedupe(records):
    seen = {}
    for r in records:
        n = seen.get(r["id"], 0) + 1
        seen[r["id"]] = n
        if n > 1:
            r["id"] = "%s-%d" % (r["id"], n)
    return records


def split_sections(records, errors, path, relfile, prefix, kind, heading_re=H2_RE):
    """Split a prose file on headings. Returns the number of records added."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if heading_re.match(ln)]
    if not starts:
        errors.append("%s: present but carries no %s heading — a source that contributes "
                      "nothing is a broken parser, not a quiet corpus. REFUSING."
                      % (relfile, heading_re.pattern))
        return 0
    n = 0
    for a, b in zip(starts, starts[1:] + [len(lines)]):
        body = lines[a:b]
        title = lines[a].lstrip("#").strip()
        records.append(rec("%s:%s" % (prefix, slug(title)), kind, relfile, a + 1,
                           head_of(body), "\n".join(body)))
        n += 1
    return n


# ------------------------------------------------------------------ the build
def build_records(root=None, project=None, door=None):
    """Returns (records, errors, roster). `roster` names every declared class and what it gave."""
    root = root or corpus_root()
    if root is None:
        return None, ["no `_GUMDROP-MANIFEST.md` in any ancestor of %s — this builder cannot "
                      "find the Memento cut it belongs to. REFUSING." % HERE], []
    project = project or os.path.dirname(root)
    records, errors, roster = [], [], []

    rb_dir = os.path.join(root, "runbooks")
    rbs = sorted(globlib.glob(os.path.join(rb_dir, "*.md")))
    if not rbs:
        errors.append("runbooks/*.md: REQUIRED source missing at %s — refuse, never index "
                      "around a hole." % rb_dir)
    for p in rbs:
        stem = os.path.splitext(os.path.basename(p))[0].replace("_RUNBOOK-", "")
        rel = os.path.relpath(p, project)
        n = split_sections(records, errors, p, rel, "runbook:%s" % stem, "runbook-section",
                           heading_re=RUNBOOK_HEADING_RE)
        roster.append(("runbooks/%s" % os.path.basename(p), "runbook-section", n))

    # ⛔ THE STATE FILES LIVE IN THE CUT, NOT AT THE PROJECT ROOT. `FIRST-SESSION.md` §4b:
    # "These go in `memento-package/`, and the chain generator reads them by their exact
    # headings". That is the same root `_gen_chain.py` uses, so the index and the chain read
    # ONE pair of files. Driven, not assumed: the first version of this builder looked at the
    # pack root and the cold start found GOOD-MORNING.md written one directory away.
    for fname, prefix, kind in (("GOOD-MORNING.md", "gm", "gm-section"),
                                ("_LIVE-STATE.md", "ls", "ls-section")):
        p = os.path.join(root, fname)
        rel = os.path.relpath(p, project)
        if not os.path.exists(p):
            roster.append((rel, kind, "ABSENT — optional, written at FIRST-SESSION §4b"))
            continue
        n = split_sections(records, errors, p, rel, prefix, kind)
        roster.append((rel, kind, n))

    rp = os.path.join(root, "_rulings.json")
    if not os.path.exists(rp):
        roster.append(("_rulings.json", "ledger-section", "ABSENT — optional"))
    else:
        try:
            with open(rp, encoding="utf-8") as f:
                data = json.load(f)
        except ValueError as e:
            errors.append("_rulings.json: unparseable (%s) — refuse, never index around a "
                          "hole." % e)
            data = None
        if data is not None:
            rulings = data.get("rulings", []) if isinstance(data, dict) else data
            rel = os.path.relpath(rp, project)
            for i, r in enumerate(rulings):
                rid = str(r.get("id") or r.get("ruled") or "ruling-%d" % (i + 1))
                title = str(r.get("says") or r.get("title") or rid)
                records.append(rec("ledger:%s" % slug(rid), "ledger-section", rel, i + 1,
                                   title[:140],
                                   json.dumps(r, indent=2, ensure_ascii=False)))
            roster.append(("_rulings.json", "ledger-section",
                           len(rulings) if rulings else "EMPTY — ships empty on purpose "
                                                        "(s219-D5 Q1)"))

    if errors:
        return None, errors, roster
    if not records:
        return None, ["the whole declared corpus produced ZERO records — a door with nothing "
                      "behind it is a broken door, not a quiet one. REFUSING."], roster

    kinds_ok, kerr = door_kinds(door)
    if kerr:
        return None, [kerr], roster
    stray = sorted({r["kind"] for r in records} - kinds_ok)
    if stray:
        return None, ["kinds the door beside this builder cannot show: %s — it would index "
                      "them and never display them (_search_core.search skips an unknown "
                      "bucket silently). REFUSING." % stray], roster

    records.sort(key=lambda r: (r["file"], r["line"], r["id"]))
    _dedupe(records)
    return records, [], roster


def render(records):
    return json.dumps({"$generated_by": GENERATED_BY, "records": records},
                      indent=2, ensure_ascii=False) + "\n"


def print_roster(roster):
    for name, kind, n in roster:
        print("    %-28s %-16s %s" % (name, kind, n))


# ------------------------------------------------------------------ selftest
def selftest():
    import shutil, tempfile
    fails, ran = [], []

    def bite(name, got, want=True):
        ok = got == want
        ran.append(name)
        print("  [%s] %s%s" % ("OK" if ok else "RED", name,
                               "" if ok else "  got %r wanted %r" % (got, want)))
        if not ok:
            fails.append(name)

    def scaffold(d, runbooks=True, rulings=True, gm=False):
        proj = os.path.join(d, "proj")
        root = os.path.join(proj, "memento-package")
        os.makedirs(os.path.join(root, "machinery"), exist_ok=True)
        open(os.path.join(root, "_GUMDROP-MANIFEST.md"), "w").write("# cut\n")
        if runbooks:
            os.makedirs(os.path.join(root, "runbooks"), exist_ok=True)
            open(os.path.join(root, "runbooks", "_RUNBOOK-x.md"), "w").write(
                "# t\n\n## Alpha\nbody a\n\n### Beta\nbody b\n")
        if rulings:
            open(os.path.join(root, "_rulings.json"), "w").write(
                '{"rulings": [{"id": "s1-D1", "says": "the thing"}]}\n')
        if gm:
            open(os.path.join(root, "GOOD-MORNING.md"), "w").write("## A\nalpha\n## B\nbeta\n")
        return proj, root

    # A SYNTHETIC door, never the real one: in the repo this builder has no door beside it —
    # the door arrives in the pack — so a selftest keyed on the real file would be green only
    # where it is not the subject. The REAL door's vocabulary is proved on the STAGE, which is
    # the only place the two files actually sit together.
    DOOR_STUB = ('KIND_ORDER = ["lane", "gm-section", "ls-section", "ledger-section",\n'
                 '              "runbook-section", "gauge-block", "brief", "dream"]\n')

    d = tempfile.mkdtemp(prefix="gumdrop-idx-selftest-")
    try:
        proj, root = scaffold(d, gm=True)
        door = os.path.join(root, "machinery", "_memento_search.py")
        open(door, "w").write(DOOR_STUB)
        recs, errs, roster = build_records(root, proj, door)
        bite("builds from a scaffolded cut", errs == [] and recs is not None)
        kinds = sorted({r["kind"] for r in (recs or [])})
        bite("emits runbook/gm/ledger sections",
             kinds, ["gm-section", "ledger-section", "runbook-section"])
        bite("runbook `###` is its own record", any(r["id"] == "runbook:x:beta" for r in recs or []))
        bite("deterministic", render(recs) == render(build_records(root, proj, door)[0]))

        # THE KIND CONSTRAINT — a kind the door cannot show must REFUSE, not index-and-hide.
        kinds_ok, _ = door_kinds(door)
        bite("KIND_ORDER read out of the door by AST",
             kinds_ok is not None and "runbook-section" in kinds_ok)
        narrow = os.path.join(d, "narrow_door.py")
        open(narrow, "w").write("KIND_ORDER = ['lane']\n")
        ko, _ = door_kinds(narrow)
        bite("a door that lists only `lane` yields only `lane`", ko, {"lane"})
        _, errsK, _ = build_records(root, proj, narrow)
        bite("a door that cannot show our kinds REFUSES the build",
             any("cannot show" in e for e in errsK))
        _, kerr = door_kinds(os.path.join(d, "absent.py"))
        bite("no door beside the builder REFUSES", bool(kerr))
        nolit = os.path.join(d, "nolit_door.py")
        open(nolit, "w").write("KIND_ORDER = list(SOMETHING)\n")
        _, kerr2 = door_kinds(nolit)
        bite("a non-literal KIND_ORDER REFUSES rather than guesses", bool(kerr2))

        # REQUIRED missing
        d2 = tempfile.mkdtemp(prefix="gumdrop-idx-selftest2-")
        p2, r2 = scaffold(d2, runbooks=False)
        open(os.path.join(r2, "machinery", "_memento_search.py"), "w").write(DOOR_STUB)
        _, errs2, _ = build_records(r2, p2, os.path.join(r2, "machinery", "_memento_search.py"))
        bite("REQUIRED runbooks missing REFUSES",
             any("REQUIRED source missing" in e for e in errs2))
        shutil.rmtree(d2, ignore_errors=True)

        # OPTIONAL absent is SKIPPED BY NAME, never silently
        _, _, roster3 = build_records(root, proj, door)
        bite("optional absent source is named in the roster",
             any(n.endswith("_LIVE-STATE.md") and str(v).startswith("ABSENT")
                 for n, _k, v in roster3))
        # ⛔ the state files are read from the CUT, the home FIRST-SESSION.md §4b names —
        # a copy at the project root must NOT be picked up instead.
        open(os.path.join(proj, "_LIVE-STATE.md"), "w").write("## Wrong home\nnope\n")
        _, _, rosterH = build_records(root, proj, door)
        bite("a _LIVE-STATE.md at the PROJECT root is not the cut's copy",
             any(n.endswith("_LIVE-STATE.md") and str(v).startswith("ABSENT")
                 for n, _k, v in rosterH))
        os.remove(os.path.join(proj, "_LIVE-STATE.md"))

        # present-but-empty optional REFUSES
        open(os.path.join(root, "_LIVE-STATE.md"), "w").write("no headings here\n")
        _, errs4, _ = build_records(root, proj, door)
        bite("optional source PRESENT but contributing zero REFUSES",
             any("_LIVE-STATE.md" in e and "REFUSING" in e for e in errs4))
        os.remove(os.path.join(root, "_LIVE-STATE.md"))

        # unparseable store REFUSES
        open(os.path.join(root, "_rulings.json"), "w").write("{ not json\n")
        _, errs5, _ = build_records(root, proj, door)
        bite("unparseable _rulings.json REFUSES", any("unparseable" in e for e in errs5))
        open(os.path.join(root, "_rulings.json"), "w").write('{"rulings": []}\n')
        _recs6, errs6, roster6 = build_records(root, proj, door)
        bite("EMPTY rulings store is legal (ships empty on purpose)", errs6 == [])
        bite("empty store is named EMPTY in the roster",
             any(n == "_rulings.json" and str(v).startswith("EMPTY") for n, _k, v in roster6))

        # no manifest anywhere -> refuse rather than guess a root
        bite("no _GUMDROP-MANIFEST.md ancestor REFUSES", corpus_root(d) is None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # COUNTED, never typed — a bite total that is a literal goes stale the first time a bite
    # is added and then reads as evidence that nothing changed.
    print("selftest: %d bites, %d fail(s)" % (len(ran), len(fails)))
    return 1 if fails else 0


# ------------------------------------------------------------------ main
def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        return selftest()
    records, errors, roster = build_records()
    if errors:
        print("⛔ index build REFUSED:")
        for e in errors:
            print("   " + e)
        if roster:
            print("  sources:")
            print_roster(roster)
        return 1
    payload = render(records)
    if args and args[0] == "--check":
        if not os.path.exists(OUT_PATH):
            print("⛔ %s is MISSING — run the build." % os.path.basename(OUT_PATH))
            return 1
        with open(OUT_PATH, encoding="utf-8") as f:
            on_disk = f.read()
        if on_disk != payload:
            print("⛔ %s is STALE — regenerate it." % os.path.basename(OUT_PATH))
            return 1
        print("✅ %s is FRESH — %d record(s)." % (os.path.basename(OUT_PATH), len(records)))
        return 0
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(payload)
    print("✅ wrote %s — %d record(s)." % (OUT_PATH, len(records)))
    print("  sources:")
    print_roster(roster)
    print("  next: python3 %s \"<your question>\"" % os.path.join(
        os.path.basename(HERE), "_memento_search.py"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
