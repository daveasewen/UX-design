#!/usr/bin/env python3
"""
_validate_example_fence.py — the EXAMPLE fence: page templates are looked at, never built from.

Dave, 14:55 2026-10-02 (#314 review, call 7), verbatim: "the page templates are only example or
inspiration in the library for designers. automated build need to ignore these, I don't want builds
to trace pages. However we probably need to create some standardised templates for some programs.
They all need to be properly built. for now we have the prepped properly but we ignore them until we
are working with programs to define them."

So a template is BOTH: properly composed of parts (s313-D72) AND fenced as an example. This gate is
the fence's teeth. It extends the fence the library already had — the door skips `EXAMPLE-*` metas,
roles.json lists template-* under `$not-a-provider`, the generate-from-canon skill's rule 1a says
"Compose, never trace" — with one declared field, `fence: "example"` on the meta, and bites it:

  FAIL (gating):
    1 META   — a PAGE template's meta (slug template-*; the app-shell-* frames are shells a page sits
               in, not pages) that does not declare `fence: "example"` with the plain words beside it
               in `$fence` (a fence nobody can read is not a fence);
    2 DOOR   — the compose door (_compose_slice.load_graph) still holds a fenced meta, or its seed
               for the reference task names one (a build could start from a page);
    3 SKILL  — the generate-from-canon skill no longer carries the fence sentence (the one-shot path
               reads the skill, not this file);
    4 TRACE  — a BUILT page passed on the command line (or found under outputs/**/*.html) wears a
               template's scope (`cn-template-*`), or shares template body that no part supplies:
               >= TRACE_SHINGLES distinct 48-char runs of a template's body (styles, scripts,
               comments and the APOLLO-DEMO harness stripped) that appear in no part snippet.
               That is a page "whose structure is a template's with the words changed" (skill 1a).
  ADVISORY (declared, counted, never hidden):
    * template-dashboard-bento.meta.json without the fence while its own lane (Dave 14:55 call 27)
      is rebuilding it — named here with its reason; the advisory clears the moment the fence lands.

Usage:
  python3 knowledge/_validate_example_fence.py                 # checks 1-3 + 4 over outputs/**/*.html
  python3 knowledge/_validate_example_fence.py page.html ...   # 4 over the pages named
  python3 knowledge/_validate_example_fence.py --selftest      # the bites can bite
Writes knowledge/_EXAMPLE-FENCE-GATE.md and exits non-zero on any failure.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SKILL = os.path.join(REPO, "apollo-spider", "skills", "generate-from-canon", "SKILL.md")
SKILL_SENTENCE = "automated build need to ignore these, I don't want builds to trace pages"
TRACE_SHINGLES = 12      # distinct template-only 48-char runs a built page may share before it has traced
SHINGLE = 48
OWED = {  # advisory, not a failure: the fence is owed by another lane, with the reason
    "template-dashboard-bento": "its own lane rebuilds it (Dave 14:55, call 27: \"Yes, its own lane, rebuilt the same way\"); the fence lands with that lane",
}
REPORT = os.path.join(HERE, "_EXAMPLE-FENCE-GATE.md")

_STRIP = re.compile(r"<!-- ===== APOLLO-DEMO .*? END ===== -->|/\* ===== APOLLO-DEMO .*? END ===== \*/"
                    r"|<(script|style)\b[\s\S]*?</\1>|<!--[\s\S]*?-->", re.S)


def metas(root=HERE):
    out = {}
    for f in sorted(glob.glob(os.path.join(root, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith("EXAMPLE-"):
            continue
        try:
            out[slug] = json.load(open(f, encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            out[slug] = {"$unparseable": str(e)}
    return out


def fenced(ms):
    return sorted(s for s, m in ms.items() if m.get("fence") == "example")


def body_of(path):
    h = open(path, encoding="utf-8", errors="replace").read()
    b = h[h.find("<body"):] if "<body" in h else h
    b = _STRIP.sub(" ", b)
    return re.sub(r"\s+", " ", b)


def shingles(text):
    return {text[i:i + SHINGLE] for i in range(0, max(0, len(text) - SHINGLE), 8)}


def template_only_shingles(root=HERE, fenced_slugs=()):
    """48-char runs of every fenced template's body that NO part snippet also carries."""
    snips = os.path.join(root, "snippets")
    tpl, parts = set(), set()
    for f in glob.glob(os.path.join(snips, "*.reference.html")):
        slug = os.path.basename(f)[:-len(".reference.html")].lower()
        (tpl if slug in fenced_slugs else parts).update(shingles(body_of(f)))
    return tpl - parts


def check_meta(ms):
    fails, advis = [], []
    for slug, m in sorted(ms.items()):
        if not slug.startswith("template-"):
            continue
        ok = m.get("fence") == "example" and SKILL_SENTENCE in re.sub(r"\s+", " ", str(m.get("$fence", "")))
        if ok:
            continue
        if slug in OWED and m.get("fence") != "example":
            advis.append("%s — UNFENCED, owed: %s" % (slug, OWED[slug]))
        else:
            fails.append("META %s: a page template without `fence: \"example\"` + Dave's words in `$fence`" % slug)
    return fails, advis


def check_door(fenced_slugs):
    fails = []
    try:
        sys.path.insert(0, HERE)
        import _compose_slice as cs
        g = cs.load_graph()
        leaked = [s for s in fenced_slugs if s in g["metas"]]
        if leaked:
            fails.append("DOOR load_graph holds fenced meta(s): %s" % ", ".join(leaked))
        seed = cs.build_slice(cs.TASK_A, graph=g)
        named = [c["id"] for c in seed["components"] if c["id"].split(":", 1)[-1] in fenced_slugs]
        if named:
            fails.append("DOOR the reference seed names fenced page(s): %s" % ", ".join(named))
    except Exception as e:  # noqa: BLE001
        fails.append("DOOR could not be asked: %r" % (e,))
    return fails


def check_skill():
    if not os.path.exists(SKILL):
        return ["SKILL missing: %s" % os.path.relpath(SKILL, REPO)]
    txt = re.sub(r"\s+", " ", open(SKILL, encoding="utf-8").read())
    return [] if SKILL_SENTENCE in txt else ["SKILL generate-from-canon no longer carries the fence sentence (%r)" % SKILL_SENTENCE]


def check_pages(pages, fenced_slugs, root=HERE):
    """4 TRACE. Returns (fails, rows). A page under knowledge/snippets or showroom/ IS a template's own
    page and is never judged here (it wears its own scope by right)."""
    fails, rows = [], []
    only = None
    scope_rx = re.compile(r"\bcn-(%s)\b" % "|".join(re.escape(s) for s in fenced_slugs)) if fenced_slugs else None
    for p in pages:
        rp = os.path.relpath(p, REPO)
        if rp.startswith("knowledge/snippets/") or rp.startswith("showroom/") or "/_fitness-test/" in rp:
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        wears = sorted(set(scope_rx.findall(txt))) if scope_rx else []
        if only is None:
            only = template_only_shingles(root, set(fenced_slugs))
        shared = len(shingles(body_of(p)) & only)
        rows.append((rp, wears, shared))
        if wears:
            fails.append("TRACE %s wears a template's scope: %s" % (rp, ", ".join("cn-" + w for w in wears)))
        if shared >= TRACE_SHINGLES:
            fails.append("TRACE %s shares %d template-only runs (>= %d): a page built from a page" % (rp, shared, TRACE_SHINGLES))
    return fails, rows


def default_pages():
    return sorted(glob.glob(os.path.join(REPO, "outputs", "**", "*.html"), recursive=True))


def run(pages=None, write=True, root=HERE):
    ms = metas(root)
    fz = fenced(ms)
    f1, advis = check_meta(ms)
    f2 = check_door(fz) if root == HERE else []
    f3 = check_skill()
    pages = pages if pages is not None else default_pages()
    f4, rows = check_pages(pages, fz, root)
    fails = f1 + f2 + f3 + f4
    if write:
        lines = ["# EXAMPLE-FENCE GATE — page templates are looked at, never built from (Dave 14:55 2026-10-02, call 7)", "",
                 "RESULT: %s — %d failure(s), %d advisory, %d fenced meta(s), %d page(s) judged" % ("PASS" if not fails else "FAIL", len(fails), len(advis), len(fz), len(rows)), "",
                 "Fenced: " + ", ".join(fz), ""]
        lines += ["- ❌ " + x for x in fails] + ["- 🟡 " + x for x in advis]
        lines += ["", "| page | wears | template-only runs shared |", "|---|---|---|"]
        lines += ["| %s | %s | %d |" % (rp, ", ".join(w) or "—", n) for rp, w, n in rows]
        open(REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return fails, advis, fz, rows


def selftest():
    import shutil, tempfile
    fails = []

    def bite(name, cond, detail=""):
        print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else "  %s" % (detail,)))
        if not cond:
            fails.append(name)

    ms = metas()
    fz = fenced(ms)
    bite("the live tree fences at least ten templates", len(fz) >= 10, fz)
    f1, _ = check_meta(ms)
    bite("the live metas pass check 1", not f1, f1)
    m2 = dict(ms)
    m2["template-report"] = dict(m2["template-report"], fence=None)
    f1b, _ = check_meta(m2)
    bite("MUTATION: a template meta with the fence removed FAILS check 1", any("template-report" in x for x in f1b), f1b)
    bite("the skill carries the sentence", not check_skill())
    # TRACE bites on scratch pages
    tmp = tempfile.mkdtemp()
    try:
        clean = os.path.join(tmp, "clean.html")
        open(clean, "w").write("<!DOCTYPE html><html><body class='canon'><div class='cn-button'><button class='btn primary'>Go</button></div></body></html>")
        wears = os.path.join(tmp, "wears.html")
        open(wears, "w").write("<!DOCTYPE html><html><body class='canon'><main class='cn-template-dashboard'><h1>x</h1></main></body></html>")
        src = os.path.join(HERE, "snippets", "Template-report.reference.html")
        traced = os.path.join(tmp, "traced.html")
        b = open(src, encoding="utf-8").read()
        open(traced, "w").write(b.replace("cn-template-report", "cn-page").replace("Receipts and settlement", "Payments and fees"))
        fc, rc = check_pages([clean], fz)
        fw, _ = check_pages([wears], fz)
        ft, rt = check_pages([traced], fz)
        bite("a page made of parts PASSES check 4", not fc, (fc, rc))
        bite("a page wearing cn-template-* is REFUSED", any("wears" in x for x in fw), fw)
        bite("a template copied with its words changed is REFUSED as traced", any("built from a page" in x for x in ft), (ft, rt))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selftest: %d fail(s)" % len(fails))
    return 1 if fails else 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()
    pages = [a for a in argv if not a.startswith("--")] or None
    fails, advis, fz, rows = run(pages)
    for x in fails:
        print("❌ " + x)
    for x in advis:
        print("🟡 " + x)
    print("example-fence gate: %d fenced template(s), %d page(s) judged, %d failure(s), %d advisory -> %s"
          % (len(fz), len(rows), len(fails), len(advis), os.path.relpath(REPORT, REPO)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
