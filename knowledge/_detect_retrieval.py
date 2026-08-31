#!/usr/bin/env python3
"""
_detect_retrieval.py — the RETRIEVAL-vs-INTERPRETATION detector (#231, W-325).

THE CLASS THIS CLOSES. Dave, testing Apollo-Spider v1.0.2 (2026-08-31, receipt
`notes/_receipts/2026-08-31-230-postwrap-dave-v102-test.md`), verbatim:

    "it seems to interpreted rather than get the component, it was really close but I
     could tell it was built locally rather than retrieved... bit odd"

NO SHIPPED GATE CAN SEE THAT. A builder that reconstructs a component from its own
understanding of the design system — instead of SPLICING the markup out of
`knowledge/snippets/` — produces output that passes compose, icon-source, a11y and the
screen gate, because every one of those reads properties the paraphrase reproduces.
The thing it does NOT reproduce is the canon SKELETON: the exact nesting and ordering of
the class-bearing elements. This instrument reads only that.

WHAT IT MEASURES (structure only — Dave's data, copy, labels and aria text can never move
the reading; that is proven by selftest arm B, a content-only mutation that must stay
byte-identical in score):

  element token   = tag + its CANON classes, sorted.  A class is CANON if it occurs in a
                    snippet body; every other class is DROPPED (a page-local wrapper class
                    such as `dashboard-tile` must not be evidence either way).
  ANC shingle     = `A>B>C` — an element and its 2 nearest CANON-CLASS-BEARING ancestors.
                    Elements with no canon class are TRANSPARENT: they are skipped in the
                    chain, so wrapping a canon component in page furniture cannot red it
                    (selftest arm D).
  SEQ shingle     = `P:[a<b]` — ORDERED PAIRS over a canon parent's distinct canon
                    children (again lifting through transparent wrappers). This is what
                    catches a REORDERED or RE-COMPOSED skeleton, and pairs rather than
                    windows because a window reds on a legitimate TRIM (selftest arm P).

  FIDELITY(F) = |built shingles belonging to F that EXIST in F's snippet| / |built shingles
                belonging to F|.  Precision, not recall — because TRIMMING a canon
                component (dropping the sort switch, keeping the chart) is legitimate and
                must stay green, while INVENTING structure is the tell. COVERAGE (recall) is
                reported beside it as information, never as the grade.

GRADES, per component family the built file ATTEMPTS:
  SPLICED     fidelity >= --threshold-spliced   — the markup came out of the snippet.
  PARAPHRASE  --threshold-absent <= fidelity < --threshold-spliced — Dave's "really close".
  ABSENT      fidelity < --threshold-absent     — attempted, structurally unrelated.
  NO-VERDICT  fewer than --min-shingles belonging shingles — NAMED, never defaulted to a
              pass ([[measuring-tool-must-not-guess]]).

⛔ THE THRESHOLD IS NOT THIS FILE'S TO CHOOSE. The defaults below are PLACEHOLDERS carried
so the script runs; where SPLICED ends and PARAPHRASE begins is Dave's dial, put to him on
`reviews/DETECTOR-READINGS-2026-08-31-v1.html`. Change them only on his word.

EVERYTHING IS DERIVED AT RUN TIME from `knowledge/snippets/*.reference.html` — the family
list, the canon class vocabulary, the distinctive ("own") classes and the shingle
vocabularies. There is no baked list, because a baked list rots the day a snippet lands
(s200-D1 mint-time idiom).

REFUSALS are loud, named and non-zero ([[a-crash-is-not-a-fail]]):
  rc 0  every attempted family SPLICED
  rc 1  at least one PARAPHRASE or ABSENT  (the red this instrument exists to raise)
  rc 2  REFUSED — bad arguments, missing/empty snippet corpus, unreadable or empty target
  rc 3  NO VERDICT — nothing gradeable (no family attempted, or all below --min-shingles)

USAGE
  python3 knowledge/_detect_retrieval.py <built.html> [more.html ...] [options]
    --snippets DIR          default: <this file's dir>/snippets
    --threshold-spliced F   default 0.90   (PLACEHOLDER — Dave's dial)
    --threshold-absent F    default 0.55   (PLACEHOLDER — Dave's dial)
    --min-shingles N        default 8
    --df-own N              default 3   a class is a family's OWN if <= N snippets carry it
    --evidence N            default 6   missed-shingle lines printed per family
    --only NAME[,NAME]      grade only these families
    --json                  emit a machine-readable report on stdout instead of text
    --selftest              run the mutation matrix (drives real snippet files) and exit
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import json
import os
import random
import re
import sys
from html.parser import HTMLParser

from _htmlmask import mask_comments   # the ONE comment mask (#211) — a class named only

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SNIPPETS = os.path.join(HERE, "snippets")

# ⛔ PLACEHOLDERS. Dave's dial — see the docstring and the readings page.
T_SPLICED = 0.90
T_ABSENT = 0.55
MIN_SHINGLES = 8
DF_OWN = 3
ANC_K = 3               # element + 2 canon ancestors
SEQ_MAX_CHILDREN = 20   # ordered-pair cap per canon parent (distinct child tokens)

REFUSAL = "REFUSED (detect-retrieval)"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
SKIP_SUBTREE = {"script", "style"}


class DetectorRefusal(Exception):
    """A named refusal. Never swallowed, never defaulted to a verdict."""


# --------------------------------------------------------------------------- parsing

class Node(object):
    __slots__ = ("tag", "classes", "children", "parent")

    def __init__(self, tag, classes, parent=None):
        self.tag = tag
        self.classes = classes          # tuple, source order preserved for the record
        self.children = []
        self.parent = parent

    def clone(self, parent=None):
        n = Node(self.tag, self.classes, parent)
        n.children = [c.clone(n) for c in self.children]
        return n


class _TreeBuilder(HTMLParser):
    """Tolerant tree builder. Comments are masked BEFORE feeding, script/style skipped."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("#document", ())
        self.stack = [self.root]
        self.body = None
        self._skip = 0

    def _open(self, tag, attrs, closed):
        if self._skip:
            return
        if tag in SKIP_SUBTREE:
            self._skip += 1
            return
        cls = ""
        for k, v in attrs:
            if k == "class" and v:
                cls = v
        node = Node(tag, tuple(cls.split()), self.stack[-1])
        self.stack[-1].children.append(node)
        if tag == "body" and self.body is None:
            self.body = node
        if not closed and tag not in VOID:
            self.stack.append(node)

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag in SKIP_SUBTREE:
            if self._skip:
                self._skip -= 1
            return
        if self._skip:
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return
        # unmatched close tag: ignore, exactly as a browser does


def parse(html, where="<string>"):
    """-> (root, body_node_or_root, used_body: bool). Raises DetectorRefusal on empty."""
    if not html or not html.strip():
        raise DetectorRefusal("%s: file is EMPTY — nothing to grade." % where)
    tb = _TreeBuilder()
    try:
        tb.feed(mask_comments(html))
        tb.close()
    except Exception as exc:                                   # loud, never silent
        raise DetectorRefusal("%s: HTML could not be parsed (%s: %s)."
                              % (where, type(exc).__name__, exc))
    scope = tb.body if tb.body is not None else tb.root
    n = count_elements(scope)
    if n == 0:
        raise DetectorRefusal("%s: parsed to ZERO elements — not HTML, or all of it was "
                              "inside <script>/<style>/comments." % where)
    return tb.root, scope, tb.body is not None


def count_elements(node):
    return sum(1 + count_elements(c) for c in node.children)


def walk(node):
    for c in node.children:
        yield c
        for g in walk(c):
            yield g


# ------------------------------------------------------------------- fingerprinting

def token(node, vocab):
    """tag + its CANON classes, sorted. Foreign classes are dropped by construction."""
    keep = sorted(c for c in node.classes if c in vocab)
    return node.tag + ("." + ".".join(keep) if keep else "")


def is_canon(node, vocab):
    return any(c in vocab for c in node.classes)


def canon_children(node, vocab):
    """Direct canon children, LIFTING THROUGH transparent (non-canon) wrappers."""
    out = []
    for c in node.children:
        if is_canon(c, vocab):
            out.append(c)
        else:
            out.extend(canon_children(c, vocab))
    return out


def canon_ancestors(node, vocab, k):
    """The k nearest canon-class-bearing ancestors, outermost-first."""
    chain = []
    p = node.parent
    while p is not None and len(chain) < k:
        if is_canon(p, vocab):
            chain.append(p)
        p = p.parent
    chain.reverse()
    return chain


def shingles(scope, vocab):
    """-> dict[str shingle] = (frozenset canon classes, frozenset id(anchor element)).

    Every shingle emitted carries at least one canon class BY CONSTRUCTION (the anchor
    element, or the parent, must be canon), so there is no low-information tail to
    silently pad a score with. The anchor ids are what let a reading be confined to the
    REGION of the page a family actually occupies (see `regions`).
    """
    out = {}

    def note(s, nodes, anchor):
        cs = set()
        for n in nodes:
            cs.update(c for c in n.classes if c in vocab)
        prev = out.get(s)
        if prev is None:
            out[s] = (frozenset(cs), frozenset([id(anchor)]))
        else:
            out[s] = (frozenset(prev[0] | cs), frozenset(prev[1] | {id(anchor)}))

    for el in walk(scope):
        if not is_canon(el, vocab):
            continue
        chain = canon_ancestors(el, vocab, ANC_K - 1) + [el]
        note(">".join(token(n, vocab) for n in chain), chain, el)

        # ORDERED PAIRS of DISTINCT canon children, not sliding windows.
        # ⚠ FOUND BY DRIVING IT (#231, selftest arm P): a sliding window reds on a
        # LEGITIMATE TRIM — deleting one canon child turns `P:[a,b,c]` into `P:[a,c,d]`,
        # a sequence canon never contained, and the score fell to ~0.72-0.84 on five real
        # snippets. Ordered pairs are SUBSEQUENCE-STABLE: a trim only ever REMOVES pairs,
        # so precision holds at 1.000, while a REORDER manufactures reversed pairs and an
        # INSERTED canon child manufactures new ones. Children are de-duplicated by token
        # first, so a chart with 5 bars and one with 12 read identically.
        kids = canon_children(el, vocab)
        if kids:
            seen, toks = {}, []
            for kid in kids:
                t = token(kid, vocab)
                if t not in seen:
                    seen[t] = kid
                    toks.append(t)
            if len(toks) > SEQ_MAX_CHILDREN:
                toks = toks[:SEQ_MAX_CHILDREN]
            pt = token(el, vocab)
            for i in range(len(toks)):
                for j in range(i + 1, len(toks)):
                    note("%s:[%s<%s]" % (pt, toks[i], toks[j]),
                         [el, seen[toks[i]], seen[toks[j]]], el)
    return out


# ------------------------------------------------------------------------- regions
# THE FALSE-ATTRIBUTION CLASS, found by DRIVING THE THING on a real file (#231): the
# dashboard's ONE line chart made Chart-combo and Template-report go red, because those
# families share `dv-target-label` / `dv-toggle-seg` / `dv-ghost` with Chart-line, and
# Template-report's reading then swept in the page's KPI cards as well. Two remedies,
# both reported and both switchable, because a false red kills the instrument on day one:
#   REGION   a family is graded only over the part of the page its own distinctive
#            classes actually sit in — the region grows upward from each anchor and STOPS
#            before it would swallow another family's anchor.
#   SHADOW   overlapping regions can have only ONE provenance: within a cluster of
#            families whose regions overlap, the best-fitting family carries the verdict
#            and the rest are reported SHADOWED-BY — named, never silently dropped.

def subtree_ids(node):
    out = {id(node)}
    for c in node.children:
        out |= subtree_ids(c)
    return out


def regions(scope, vocab, anchors_by_family):
    """-> dict[family] = frozenset(element ids in that family's region)."""
    all_anchor_ids = set()
    for s in anchors_by_family.values():
        all_anchor_ids |= s
    scope_ids = subtree_ids(scope)
    by_id = {id(el): el for el in walk(scope)}
    out = {}
    for fam, anc in anchors_by_family.items():
        foreign = all_anchor_ids - anc
        region = set()
        for aid in anc:
            el = by_id.get(aid)
            if el is None:
                continue
            best = el
            cur = el
            while True:
                nxt = None
                p = cur.parent
                while p is not None and p is not scope and not is_canon(p, vocab):
                    p = p.parent
                if p is None or p is scope:
                    break
                nxt = p
                if subtree_ids(nxt) & foreign:
                    break
                best = cur = nxt
            region |= subtree_ids(best)
        out[fam] = frozenset(region & scope_ids)
    return out


def cluster_shadows(recs, region_by_family, overlap=0.5):
    """Mark every graded family that shares a region with a BETTER-fitting one."""
    graded = [r for r in recs if r["fidelity"] is not None]
    graded.sort(key=lambda r: -r["fidelity"])
    for i, r in enumerate(graded):
        ri = region_by_family.get(r["family"], frozenset())
        if not ri:
            continue
        for better in graded[:i]:
            if better.get("shadowed_by"):
                continue
            rb = region_by_family.get(better["family"], frozenset())
            if not rb:
                continue
            if len(ri & rb) / float(len(ri)) >= overlap:
                r["shadowed_by"] = better["family"]
                r["grade"] = "SHADOWED"
                r["why"] = ("region overlaps %s, which fits it better (%.3f vs %.3f) — a "
                            "region has ONE provenance; not counted as a red"
                            % (better["family"], better["fidelity"], r["fidelity"]))
                break
    return recs


# ------------------------------------------------------------------------- corpus

class Corpus(object):
    """Families + vocabularies, DERIVED AT RUN TIME from the snippet directory."""

    def __init__(self, snippet_dir, df_own=DF_OWN):
        self.dir = snippet_dir
        if not os.path.isdir(snippet_dir):
            raise DetectorRefusal("snippet corpus MISSING: %s is not a directory. The "
                                  "fingerprints are derived from it at run time; without "
                                  "it there is nothing to compare against."
                                  % snippet_dir)
        files = sorted(glob.glob(os.path.join(snippet_dir, "*.reference.html")))
        if not files:
            raise DetectorRefusal("snippet corpus EMPTY: no *.reference.html in %s."
                                  % snippet_dir)
        self.files = files
        self.trees = {}
        raw = {}
        for p in files:
            name = os.path.basename(p)[:-len(".reference.html")]
            with open(p, encoding="utf-8") as fh:
                _, scope, _ = parse(fh.read(), where=p)
            self.trees[name] = scope
            raw[name] = set()
            for el in walk(scope):
                raw[name].update(el.classes)

        self.vocab = set()
        for s in raw.values():
            self.vocab |= s
        if not self.vocab:
            raise DetectorRefusal("snippet corpus carries NO classes at all (%d files) — "
                                  "the class vocabulary is the whole instrument."
                                  % len(files))

        self.df = {}
        for s in raw.values():
            for c in s:
                self.df[c] = self.df.get(c, 0) + 1

        self.classes = raw
        self.own = {n: {c for c in s if self.df[c] <= df_own} for n, s in raw.items()}
        self.shingles = {n: shingles(t, self.vocab) for n, t in self.trees.items()}

    def attempted(self, built_classes):
        """Families the built file ATTEMPTS: it carries >=1 class distinctive to them."""
        return sorted(n for n, own in self.own.items() if own & built_classes)


# ------------------------------------------------------------------------- grading

def grade_one(built_sh, family, corpus, t_spliced, t_absent, min_sh, region=None):
    """Grade ONE family against one built file's shingle map, optionally region-confined."""
    fam_classes = corpus.classes[family]
    fam_sh = corpus.shingles[family]
    belong = {s: cs for s, (cs, anch) in built_sh.items()
              if cs and cs <= fam_classes and (region is None or (anch & region))}
    matched = [s for s in belong if s in fam_sh]
    missed = [s for s in belong if s not in fam_sh]
    n = len(belong)
    rec = {
        "family": family,
        "belonging": n,
        "matched": len(matched),
        "missed": len(missed),
        "canon_shingles": len(fam_sh),
        "own_classes": sorted(corpus.own[family]),
        "fidelity": None,
        "coverage": None,
        "grade": None,
        "evidence_missed": sorted(missed),
        "evidence_matched": sorted(matched),
    }
    if n < min_sh:
        rec["grade"] = "NO-VERDICT"
        rec["why"] = ("only %d belonging shingle(s), below --min-shingles %d — "
                      "NOT graded, NOT passed" % (n, min_sh))
        return rec
    fid = len(matched) / float(n)
    rec["fidelity"] = fid
    rec["coverage"] = (len(matched) / float(len(fam_sh))) if fam_sh else None
    rec["grade"] = ("SPLICED" if fid >= t_spliced
                    else "PARAPHRASE" if fid >= t_absent else "ABSENT")
    return rec


def grade_file(path, corpus, t_spliced=T_SPLICED, t_absent=T_ABSENT,
               min_sh=MIN_SHINGLES, only=None, html=None, use_region=True,
               use_shadow=True):
    if html is None:
        if not os.path.isfile(path):
            raise DetectorRefusal("target NOT FOUND: %s" % path)
        with open(path, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
    _, scope, used_body = parse(html, where=path)
    built_classes = set()
    for el in walk(scope):
        built_classes.update(el.classes)
    built_sh = shingles(scope, corpus.vocab)

    fams = corpus.attempted(built_classes)
    if only:
        fams = [f for f in fams if f in only]

    anchors = {}
    for f in fams:
        own = corpus.own[f]
        anchors[f] = {id(el) for el in walk(scope) if own & set(el.classes)}
    region_by = regions(scope, corpus.vocab, anchors) if use_region else {}

    recs = [grade_one(built_sh, f, corpus, t_spliced, t_absent, min_sh,
                      region_by.get(f) if use_region else None) for f in fams]
    for r in recs:
        r["region_elements"] = len(region_by.get(r["family"], ())) if use_region else None
    if use_shadow:
        cluster_shadows(recs, region_by)

    report = {
        "target": path,
        "scope": "<body>" if used_body else "WHOLE DOCUMENT (no <body> element found)",
        "elements": count_elements(scope),
        "built_shingles": len(built_sh),
        "region_confined": bool(use_region),
        "shadowing": bool(use_shadow),
        "foreign_classes": sorted(c for c in built_classes if c not in corpus.vocab),
        "thresholds": {"spliced": t_spliced, "absent": t_absent,
                       "min_shingles": min_sh},
        "families": recs,
    }
    if only:
        missing = sorted(set(only) - set(fams))
        report["requested_not_attempted"] = missing
    return report


def verdict(reports):
    """-> (rc, one-line summary). UNKNOWN is never defaulted to a pass."""
    grades = [f["grade"] for r in reports for f in r["families"]]
    if not grades:
        return 3, ("NO VERDICT — no component family was ATTEMPTED in %d target(s). "
                   "Nothing was graded; this is NOT a pass." % len(reports))
    bad = [g for g in grades if g in ("PARAPHRASE", "ABSENT")]
    nv = [g for g in grades if g == "NO-VERDICT"]
    sh = [g for g in grades if g == "SHADOWED"]
    ok = [g for g in grades if g == "SPLICED"]
    if bad:
        return 1, ("RED — %d family reading(s) not spliced (%d PARAPHRASE, %d ABSENT); "
                   "%d SPLICED, %d NO-VERDICT, %d SHADOWED."
                   % (len(bad), grades.count("PARAPHRASE"), grades.count("ABSENT"),
                      len(ok), len(nv), len(sh)))
    if not ok:
        return 3, ("NO VERDICT — %d reading(s) below --min-shingles, %d SHADOWED, none "
                   "graded. This is NOT a pass." % (len(nv), len(sh)))
    return 0, ("GREEN — %d family reading(s) SPLICED, %d NO-VERDICT, %d SHADOWED, 0 red."
               % (len(ok), len(nv), len(sh)))


# -------------------------------------------------------------------------- output

def print_text(report, evidence_n):
    print("=" * 78)
    print("TARGET  %s" % report["target"])
    print("scope   %s · %d elements · %d structural shingles"
          % (report["scope"], report["elements"], report["built_shingles"]))
    t = report["thresholds"]
    print("dial    SPLICED >= %.2f · PARAPHRASE >= %.2f · min-shingles %d   "
          "(PLACEHOLDERS — Dave's to rule)" % (t["spliced"], t["absent"], t["min_shingles"]))
    if not report["families"]:
        print("  NO FAMILY ATTEMPTED — nothing graded. This is not a pass.")
        return
    for f in report["families"]:
        if f["grade"] in ("NO-VERDICT", "SHADOWED"):
            print("\n  %-26s %-11s %s" % (f["family"], f["grade"], f["why"]))
            continue
        print("\n  %-26s %-11s fidelity %.3f  (matched %d of %d belonging)"
              % (f["family"], f["grade"], f["fidelity"], f["matched"], f["belonging"]))
        print("  %-26s %-11s coverage %.3f  of %d canon shingles · own-classes: %s"
              % ("", "", f["coverage"] or 0.0, f["canon_shingles"],
                 ", ".join(f["own_classes"][:6]) or "(none)"))
        if f["evidence_missed"]:
            print("      NOT IN CANON (structure this build invented) — %d, first %d:"
                  % (f["missed"], min(evidence_n, f["missed"])))
            for s in f["evidence_missed"][:evidence_n]:
                print("        · %s" % s)


# ------------------------------------------------------------------------ mutators
# Text-level mutators must NOT move the score. Tree-level mutators MUST move it.

_TEXT_ATTRS = ("aria-label", "aria-description", "title", "alt", "placeholder",
               "aria-labelledby", "aria-describedby", "id", "for", "value", "content",
               "href", "d", "points", "x", "y", "cx", "cy", "width", "height", "viewBox")


def mutate_content(html):
    """Replace every text node and every content-bearing attribute. class UNTOUCHED."""
    out = re.sub(r">([^<>]+)<", lambda m: ">" + ("Z" * len(m.group(1))) + "<", html)
    for a in _TEXT_ATTRS:
        out = re.sub(r'(\b%s=")([^"]*)(")' % re.escape(a),
                     lambda m: m.group(1) + ("q" * len(m.group(2))) + m.group(3), out)
    out = re.sub(r'(\bdata-(?!theme|apollo)[\w-]+=")([^"]*)(")',
                 lambda m: m.group(1) + ("q" * len(m.group(2))) + m.group(3), out)
    return out


def mutate_class_order(html, seed=7):
    rnd = random.Random(seed)

    def f(m):
        toks = m.group(2).split()
        rnd.shuffle(toks)
        return m.group(1) + " ".join(toks) + m.group(3)
    return re.sub(r'(\bclass=")([^"]*)(")', f, html)


def mutate_whitespace(html):
    return re.sub(r">\s+<", ">\n\n   <", html)


def mutate_wrapper(html):
    """Wrap the whole body in FOREIGN page furniture — must be transparent."""
    return re.sub(r"(<body[^>]*>)",
                  r'\1<div class="zz-page-shell"><section class="zz-tile">', html, count=1)\
             .replace("</body>", "</section></div></body>")


def tree_drop_class(scope, vocab, k=6):
    """Drop a canon class from the first k canon elements — the 'close paraphrase'."""
    hit = 0
    for el in walk(scope):
        if hit >= k:
            break
        keep = [c for c in el.classes if c in vocab]
        if len(keep) >= 1 and el.tag not in ("html", "body"):
            drop = keep[0]
            el.classes = tuple(c for c in el.classes if c != drop)
            hit += 1
    return hit


def tree_unwrap(scope, vocab, k=4):
    """Splice k canon elements' children into their parents — invented/lost nesting."""
    victims = [el for el in walk(scope)
               if is_canon(el, vocab) and el.children and el.parent is not None][:k]
    n = 0
    for el in victims:
        p = el.parent
        if el not in p.children:
            continue
        i = p.children.index(el)
        for c in el.children:
            c.parent = p
        p.children[i:i + 1] = el.children
        n += 1
    return n


def tree_reorder(scope, vocab, k=6, seed=11):
    rnd = random.Random(seed)
    n = 0
    for el in walk(scope):
        if n >= k:
            break
        if len(el.children) > 2:
            rnd.shuffle(el.children)
            n += 1
    return n


def tree_add_foreign(scope, vocab, name="zz-page-local"):
    """Hang a PAGE-LOCAL class on every canon element — `class="dv dv-animate
    dashboard-chart"` is what a real page does (the #227 dashboard does exactly this).
    It must be invisible to the reading. Selftest arm D2; it is the arm that kills the
    'keep foreign classes in the token' mutant, which arm D alone could not see."""
    n = 0
    for el in walk(scope):
        if is_canon(el, vocab):
            el.classes = tuple(el.classes) + (name,)
            n += 1
    return n


def tree_insert_wrapper(scope, vocab, k=12, name="zz-layout"):
    """Push a page-local wrapper BETWEEN a canon parent and its canon children — the
    flex/grid div a real page adds inside a component. Legitimate; must be invisible.
    Selftest arm D3; it is the arm that kills the 'stop lifting through transparent
    wrappers' mutant, which arms D and D2 could not see."""
    n = 0
    for el in list(walk(scope)):
        if n >= k:
            break
        if is_canon(el, vocab) and len(el.children) > 1:
            w = Node("div", (name,), el)
            w.children = el.children
            for c in w.children:
                c.parent = w
            el.children = [w]
            n += 1
    return n


def tree_trim(scope, vocab, keep_every=2):
    """DELETE canon subtrees — a builder legitimately trims a component (keeps the chart,
    drops the sort switch and the CSV button). Trimming must NOT red. This is the arm that
    proves FIDELITY IS PRECISION, not recall: under a recall score a trim reads as drift.
    Selftest arm P."""
    n = 0
    for el in list(walk(scope)):
        kids = [c for c in el.children if is_canon(c, vocab)]
        if len(kids) < 2:
            continue
        for i, c in enumerate(kids):
            if i % keep_every == 1 and c in el.children:
                el.children.remove(c)
                n += 1
    return n


def tree_swap_tag(scope, vocab, k=8):
    n = 0
    for el in walk(scope):
        if n >= k:
            break
        if el.tag == "div" and is_canon(el, vocab):
            el.tag = "section"
            n += 1
    return n


# ------------------------------------------------------------------------ selftest

def _fid(scope, corpus, family):
    r = grade_one(shingles(scope, corpus.vocab), family, corpus, T_SPLICED, T_ABSENT, 1)
    return r["fidelity"], r["grade"], r["belonging"]


def selftest(snippet_dir):
    """MUTATION MATRIX, driven on REAL snippet files. Prints every arm, returns rc."""
    fails = []
    arms = []
    applied = {}          # mutation class -> how many times it actually CHANGED the tree

    def arm(name, ok, detail):
        arms.append((name, "OK", detail))
        if not ok:
            arms[-1] = (name, "FAIL", detail)
            fails.append(name)

    def arm_mut(cls, name, k, ok, detail):
        """A mutation arm. k == 0 means the mutation DID NOT APPLY to this subject —
        that is NOT a pass ([[instrument-without-a-consumer]]: a mutation that changed
        nothing cannot prove the clause). It is recorded INAPPLICABLE and the class must
        still be proven on at least one subject, or the selftest goes red at the end."""
        applied.setdefault(cls, 0)
        if k == 0:
            arms.append((name, "N/A ", detail + "  [mutation did not apply — proves nothing]"))
            return
        applied[cls] += 1
        arm(name, ok, detail)

    corpus = Corpus(snippet_dir)
    print("corpus: %d families · %d classes · df-own <= %d"
          % (len(corpus.files), len(corpus.vocab), DF_OWN))

    # The subjects are REAL FILES, not fixtures ([[green-tests-cannot-see-scope]]).
    subjects = [f for f in ("Chart-bar", "Chart-line", "Kpi-tile", "Cards", "Accordion")
                if f in corpus.trees]
    if len(subjects) < 3:
        raise DetectorRefusal("selftest needs >=3 of its named real subjects present in "
                              "%s; found %d." % (snippet_dir, len(subjects)))

    for fam in subjects:
        path = os.path.join(snippet_dir, fam + ".reference.html")
        src = open(path, encoding="utf-8").read()

        # A · POSITIVE CONTROL on the real file: a snippet IS its own splice.
        base_fid, base_grade, base_n = _fid(parse(src, path)[1], corpus, fam)
        arm("A/%s positive control SPLICED" % fam,
            base_grade == "SPLICED" and base_fid == 1.0,
            "fidelity %.3f grade %s over %d shingles" % (base_fid or 0, base_grade, base_n))

        # B · CONTENT-ONLY mutation MUST NOT MOVE THE READING (the false-red guard).
        f2, g2, n2 = _fid(parse(mutate_content(src), path)[1], corpus, fam)
        arm("B/%s content-only mutation is INERT" % fam,
            (f2, g2, n2) == (base_fid, base_grade, base_n),
            "fidelity %.3f (was %.3f), %d shingles (was %d)"
            % (f2 or 0, base_fid or 0, n2, base_n))

        # C · class-order + whitespace + attribute-order noise MUST NOT MOVE IT.
        noisy = mutate_whitespace(mutate_class_order(src))
        f3, g3, n3 = _fid(parse(noisy, path)[1], corpus, fam)
        arm("C/%s class-order+whitespace is INERT" % fam,
            (f3, g3, n3) == (base_fid, base_grade, base_n),
            "fidelity %.3f, %d shingles" % (f3 or 0, n3))

        # D · FOREIGN page furniture wrapped round it MUST NOT MOVE IT.
        f4, g4, n4 = _fid(parse(mutate_wrapper(src), path)[1], corpus, fam)
        arm("D/%s foreign wrapper is TRANSPARENT" % fam,
            (f4, g4) == (base_fid, base_grade),
            "fidelity %.3f grade %s, %d shingles (was %d)" % (f4 or 0, g4, n4, base_n))

        # D2 · a PAGE-LOCAL class hung on every canon element MUST NOT MOVE IT.
        t = parse(src, path)[1].clone()
        k = tree_add_foreign(t, corpus.vocab)
        fd2, gd2, nd2 = _fid(t, corpus, fam)
        arm_mut("D2", "D2/%s page-local class on %d canon elements is INERT" % (fam, k), k,
                (fd2, gd2, nd2) == (base_fid, base_grade, base_n),
                "fidelity %.3f grade %s, %d shingles (was %d)"
                % (fd2 or 0, gd2, nd2, base_n))

        # D3 · a page-local wrapper INSIDE the component MUST NOT MOVE IT.
        t = parse(src, path)[1].clone()
        k = tree_insert_wrapper(t, corpus.vocab, 12)
        fd3, gd3, nd3 = _fid(t, corpus, fam)
        arm_mut("D3", "D3/%s %d page-local wrappers inside it are INERT" % (fam, k), k,
                (fd3, gd3, nd3) == (base_fid, base_grade, base_n),
                "fidelity %.3f grade %s, %d shingles (was %d)"
                % (fd3 or 0, gd3, nd3, base_n))

        # P · TRIMMING the component MUST STAY SPLICED (fidelity is precision, not recall)
        # while COVERAGE falls — the pair of readings is the proof, not either alone.
        t = parse(src, path)[1].clone()
        k = tree_trim(t, corpus.vocab)
        rp = grade_one(shingles(t, corpus.vocab), fam, corpus, T_SPLICED, T_ABSENT, 1)
        base_cov = grade_one(shingles(parse(src, path)[1], corpus.vocab), fam, corpus,
                             T_SPLICED, T_ABSENT, 1)["coverage"]
        arm_mut("P", "P/%s trimmed %d canon subtrees STAYS SPLICED, coverage falls"
                % (fam, k), k,
                rp["grade"] == "SPLICED" and rp["fidelity"] == 1.0
                and rp["coverage"] is not None and rp["coverage"] < base_cov,
                "fidelity %.3f (kept 1.000) · coverage %.3f -> %.3f"
                % (rp["fidelity"] or 0, base_cov or 0, rp["coverage"] or 0))

        # E · DROP CANON CLASSES — the close paraphrase. MUST degrade.
        t = parse(src, path)[1].clone()
        k = tree_drop_class(t, corpus.vocab, 6)
        f5, g5, _ = _fid(t, corpus, fam)
        arm_mut("E", "E/%s dropped %d canon classes goes DOWN" % (fam, k), k,
                f5 is not None and f5 < base_fid,
                "fidelity %.3f (was %.3f)" % (f5 or 0, base_fid))

        # F · UNWRAP canon elements — lost nesting. MUST degrade.
        t = parse(src, path)[1].clone()
        k = tree_unwrap(t, corpus.vocab, 4)
        f6, g6, _ = _fid(t, corpus, fam)
        arm_mut("F", "F/%s unwrapped %d canon elements goes DOWN" % (fam, k), k,
                f6 is not None and f6 < base_fid,
                "fidelity %.3f (was %.3f)" % (f6 or 0, base_fid))

        # G · REORDER siblings — re-composed skeleton. MUST degrade.
        t = parse(src, path)[1].clone()
        k = tree_reorder(t, corpus.vocab, 6)
        f7, g7, _ = _fid(t, corpus, fam)
        arm_mut("G", "G/%s reordered %d sibling sets goes DOWN" % (fam, k), k,
                f7 is not None and f7 < base_fid,
                "fidelity %.3f (was %.3f)" % (f7 or 0, base_fid))

        # H · WRONG TAG under right classes. MUST degrade.
        t = parse(src, path)[1].clone()
        k = tree_swap_tag(t, corpus.vocab, 8)
        f8, g8, _ = _fid(t, corpus, fam)
        arm_mut("H", "H/%s swapped %d div->section goes DOWN" % (fam, k), k,
                f8 is not None and f8 < base_fid,
                "fidelity %.3f (was %.3f)" % (f8 or 0, base_fid))

        # I · RESTORE — the unmutated file must be green again (so the test CAN fail).
        f9, g9, n9 = _fid(parse(src, path)[1], corpus, fam)
        arm("I/%s restore is green again" % fam,
            (f9, g9, n9) == (base_fid, base_grade, base_n), "fidelity %.3f" % (f9 or 0))

    # J · A HAND-WRITTEN PARAPHRASE must NOT grade SPLICED (the too-loose guard).
    fam = subjects[0]
    own = sorted(corpus.own[fam])[:2]
    canon_some = sorted(c for c in corpus.classes[fam] if corpus.df[c] > 1)[:6]
    para = ("<html><body><div class='%s'><div class='%s'><span class='%s'>x</span>"
            "<span class='%s'>y</span></div><div class='%s'><p class='%s'>z</p>"
            "<p class='%s'>w</p></div></div></body></html>"
            % tuple(((own + canon_some) * 4)[:7]))
    rj = grade_one(shingles(parse(para, "<paraphrase>")[1], corpus.vocab), fam, corpus,
                   T_SPLICED, T_ABSENT, 1)
    arm("J/%s hand-written paraphrase is NOT spliced" % fam,
        rj["grade"] != "SPLICED",
        "fidelity %s grade %s" % (rj["fidelity"], rj["grade"]))

    # K · REFUSALS are loud, named and non-zero.
    try:
        Corpus(os.path.join(snippet_dir, "__no_such_dir__"))
        arm("K1 missing corpus REFUSES", False, "no refusal raised")
    except DetectorRefusal as e:
        arm("K1 missing corpus REFUSES", "MISSING" in str(e), str(e)[:70])
    try:
        parse("", "<empty>")
        arm("K2 empty target REFUSES", False, "no refusal raised")
    except DetectorRefusal as e:
        arm("K2 empty target REFUSES", "EMPTY" in str(e), str(e)[:70])
    try:
        parse("<html><body><script>var a=1;</script></body></html>", "<scriptonly>")
        arm("K3 zero-element target REFUSES", False, "no refusal raised")
    except DetectorRefusal as e:
        arm("K3 zero-element target REFUSES", "ZERO elements" in str(e), str(e)[:70])

    # L · NO-VERDICT is not a pass, and no-family-attempted is not a pass.
    rc_nv, msg_nv = verdict([{"families": []}])
    arm("L1 no family attempted -> rc 3", rc_nv == 3, msg_nv[:70])
    rc_nv2, msg2 = verdict([{"families": [{"grade": "NO-VERDICT"}]}])
    arm("L2 all NO-VERDICT -> rc 3", rc_nv2 == 3, msg2[:70])
    rc_red, msg3 = verdict([{"families": [{"grade": "PARAPHRASE"}, {"grade": "SPLICED"}]}])
    arm("L3 any PARAPHRASE -> rc 1", rc_red == 1, msg3[:70])
    rc_ok, _ = verdict([{"families": [{"grade": "SPLICED"}]}])
    arm("L4 all SPLICED -> rc 0", rc_ok == 0, "rc %d" % rc_ok)

    # N · DRIVE THE THING ON A REAL BUILT PAGE — not a fixture, not a snippet
    # ([[green-tests-cannot-see-scope]]). The pair below is the only real
    # built-vs-canon pair in the tree: `.canon.html` is Dave's own hand-polished demo
    # artefact and `.regen-v1.html` is the #227 sub's rebuild WITH the snippet markup in
    # hand. The rebuild must score HIGHER on every family they share, or this instrument
    # does not measure what it claims to.
    repo = os.path.dirname(os.path.abspath(snippet_dir))
    repo = os.path.dirname(repo) if os.path.basename(repo) == "knowledge" else repo
    pair = [os.path.join(repo, "dashboards", "international-banking-dashboard.%s.html" % s)
            for s in ("canon", "regen-v1")]
    if all(os.path.isfile(p) for p in pair):
        rr = [grade_file(p, corpus) for p in pair]
        fid = [{f["family"]: f["fidelity"] for f in r["families"]
                if f["fidelity"] is not None} for r in rr]
        shared = sorted(set(fid[0]) & set(fid[1]))
        wins = [f for f in shared if fid[1][f] > fid[0][f]]
        losses = [f for f in shared if fid[1][f] < fid[0][f]]
        # The honest claim, measured: the snippet-in-hand rebuild is NEVER WORSE, and is
        # strictly better on most families. Ties are real (both spliced the same markup).
        arm("N1 real pair: the snippet-in-hand rebuild is never worse, mostly better",
            bool(shared) and not losses and len(wins) > len(shared) / 2.0,
            "%d better, %d tied, %d worse of %d shared (%s)"
            % (len(wins), len(shared) - len(wins) - len(losses), len(losses), len(shared),
               ", ".join("%s %.3f->%.3f" % (f, fid[0][f], fid[1][f]) for f in shared)))
        # N2 · the FALSE-ATTRIBUTION guard, mutation-tested BOTH WAYS: with region+shadow
        # off, the one line chart drags sibling chart families red; with them on it must not.
        off = grade_file(pair[1], corpus, use_region=False, use_shadow=False)
        on = grade_file(pair[1], corpus)
        red_off = {f["family"] for f in off["families"]
                   if f["grade"] in ("PARAPHRASE", "ABSENT")}
        red_on = {f["family"] for f in on["families"]
                  if f["grade"] in ("PARAPHRASE", "ABSENT")}
        arm("N2 region+shadow REMOVE false attributions (and the flag can restore them)",
            red_off > red_on,
            "reds %d -> %d; suppressed: %s"
            % (len(red_off), len(red_on), ", ".join(sorted(red_off - red_on)) or "none"))
        # N3 · content-only mutation of a REAL BUILT PAGE is inert (not just of a snippet).
        raw = open(pair[1], encoding="utf-8").read()
        a1 = grade_file(pair[1], corpus)
        a2 = grade_file(pair[1], corpus, html=mutate_content(raw))
        s1 = [(f["family"], f["grade"], f["fidelity"]) for f in a1["families"]]
        s2 = [(f["family"], f["grade"], f["fidelity"]) for f in a2["families"]]
        arm("N3 content-only mutation of the REAL page is INERT", s1 == s2,
            "%d family readings, identical" % len(s1))
    else:
        arms.append(("N/A ", "N/A ", ""))
        arms[-1] = ("N1-N3 real built-page arms", "N/A ",
                    "dashboards/international-banking-dashboard.{canon,regen-v1}.html "
                    "NOT PRESENT — the real-data arms did not run and prove nothing")

    # O · THIN EVIDENCE IS NEVER A PASS, driven on a REAL file end-to-end (arm L2 only
    # drives the verdict function; this drives grade_one and the rc together).
    o_path = os.path.join(snippet_dir, subjects[0] + ".reference.html")
    o_rep = grade_file(o_path, corpus, min_sh=10 ** 6)
    o_rc, o_msg = verdict([o_rep])
    arm("O real file with an unreachable --min-shingles -> all NO-VERDICT, rc 3",
        bool(o_rep["families"])
        and all(f["grade"] in ("NO-VERDICT", "SHADOWED") for f in o_rep["families"])
        and o_rc == 3,
        "%d families, rc %d" % (len(o_rep["families"]), o_rc))

    # M · every MUTATION CLASS must have applied to at least one real subject, or the
    # class is unproven and the selftest must say so rather than pass on N/A rows.
    for cls in sorted(applied):
        arm("M/%s mutation class PROVEN on >=1 real subject" % cls, applied[cls] >= 1,
            "applied on %d subject(s)" % applied[cls])

    for name, status, detail in arms:
        print("  %-4s  %-52s %s" % (status, name, detail))
    n_na = sum(1 for a in arms if a[1] == "N/A ")
    print("\n%d arms · %d failed · %d inapplicable (N/A, proves nothing)"
          % (len(arms), len(fails), n_na))
    if fails:
        print("FAILED: %s" % ", ".join(fails))
        return 1
    return 0


# ---------------------------------------------------------------------------- main

def _argv_error(msg):
    sys.stderr.write("✖ %s: %s\n  %s --help for the contract.\n"
                     % (REFUSAL, msg, os.path.basename(__file__)))
    sys.exit(2)


def main(argv):
    if not argv:
        _argv_error("no target given. This instrument grades a BUILT html file against "
                    "the snippet corpus; a bare run is not a stated intention (#158).")
    targets, snippets = [], DEFAULT_SNIPPETS
    t_sp, t_ab, min_sh, ev, as_json, only = T_SPLICED, T_ABSENT, MIN_SHINGLES, 6, False, None
    df_own = DF_OWN
    use_region, use_shadow = True, True
    want_selftest = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--selftest":
            # PARSED, not dispatched — dispatching here made `--selftest --snippets DIR`
            # silently ignore the DIR (found by driving the mutants, #231).
            want_selftest = True
        elif a == "--json":
            as_json = True
        elif a == "--no-region":
            use_region = False
        elif a == "--no-shadow":
            use_shadow = False
        elif a in ("--snippets", "--threshold-spliced", "--threshold-absent",
                   "--min-shingles", "--evidence", "--only", "--df-own"):
            if i + 1 >= len(argv):
                _argv_error("%s needs a value" % a)
            v = argv[i + 1]
            i += 1
            try:
                if a == "--snippets":
                    snippets = v
                elif a == "--threshold-spliced":
                    t_sp = float(v)
                elif a == "--threshold-absent":
                    t_ab = float(v)
                elif a == "--min-shingles":
                    min_sh = int(v)
                elif a == "--df-own":
                    df_own = int(v)
                elif a == "--evidence":
                    ev = int(v)
                elif a == "--only":
                    only = set(x for x in v.split(",") if x)
            except ValueError:
                _argv_error("%s got a non-numeric value %r" % (a, v))
        elif a.startswith("-"):
            _argv_error("unknown option %r" % a)
        else:
            targets.append(a)
        i += 1

    if want_selftest:
        return selftest(snippets)
    if not targets:
        _argv_error("no target file given.")
    if not (0.0 <= t_ab <= t_sp <= 1.0):
        _argv_error("thresholds must satisfy 0 <= absent (%s) <= spliced (%s) <= 1"
                    % (t_ab, t_sp))

    corpus = Corpus(snippets, df_own=df_own)
    reports = [grade_file(p, corpus, t_sp, t_ab, min_sh, only,
                          use_region=use_region, use_shadow=use_shadow) for p in targets]
    rc, summary = verdict(reports)

    if as_json:
        print(json.dumps({"corpus": {"dir": snippets, "families": len(corpus.files),
                                     "classes": len(corpus.vocab), "df_own": df_own},
                          "reports": reports, "rc": rc, "summary": summary},
                         indent=1, ensure_ascii=False))
    else:
        for r in reports:
            print_text(r, ev)
        print("=" * 78)
        print(summary)
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except DetectorRefusal as exc:
        sys.stderr.write("✖ %s: %s\n" % (REFUSAL, exc))
        sys.exit(2)
