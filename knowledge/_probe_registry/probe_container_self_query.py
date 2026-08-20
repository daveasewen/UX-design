#!/usr/bin/env python3
"""probe_container_self_query.py — P-7: A `@container` RULE AIMED AT ITS OWN CONTAINER (W-45 registry).

THE CLASS, from the receipts — caught THREE times in ONE session (#210) and never by a gate:
an element declares `container-type` AND a `@container` rule in the same file targets THAT SAME
element. **A container query resolves against the matched element's nearest ANCESTOR container,
and an element is never its own ancestor.** So the rule can never match on that element, the
layout never collapses, and every gate stays green because nothing parses the artefact in the
consumer's grammar [[no-gate-parses-the-artefact]].

  · `notes/_receipts/2026-08-20-210-wave5-laneC-form-templates.md:20` — Template-auth's first
    draft put `container-type:inline-size` on `.auth` and then wrote
    `@container (max-width:880px){ .auth{ grid-template-columns:1fr } }`. The two panels NEVER
    collapsed; the 420px screenshot "looked plausible enough to accept". Repaired by moving the
    container onto `.auth-shell`. The same receipt (:286) PRICED this probe and did not build it:
    *"for every `@container` rule whose selector matches an element that itself declares
    `container-type`, and which has no other container ancestor, the rule cannot fire."*
  · `notes/_receipts/2026-08-20-210-wave6-laneC-lockups.md:152` — Hero-variants declared
    `container-type:inline-size` on `.hv-media` and queried `.hv-media`'s own
    `grid-template-columns`. Repaired by introducing the `.hv-frame` wrapper.
  · `knowledge/snippets/Template-dashboard.reference.html:264` — COMPOSITION RULE 12, measured
    the same session: Layout-utilities' `.l-split` carries the defect IN THE GATED PRIMITIVE
    ("the split NEVER COLLAPSES … a 44-pixel content column"). That lane could not edit the
    primitive, so it added a `.tpl-split-host` wrapper and wrote: *"⬛ THE REAL REPAIR IS DAVE'S"*.

WHAT THIS PROBE DOES, per file: parses the `<style>` blocks, collects (a) every selector whose
rule declares `container-type` / the `container` shorthand, and (b) every top-level selector
targeted by a rule nested inside an `@container` at-rule. An EXACT selector-string overlap
between the two sets is the class.

⛔ TIERS, and the fence is deliberate — a false positive here is worse than a miss:
  FAIL  the overlapping selector is the file's ONLY container selector. Nothing else in the
        file can supply an ancestor container, so the rule is dead for every element that
        matches it except one nested inside another element matching the same selector.
  WARN  the file declares OTHER container selectors too. The query may LEGALLY resolve against
        one of those (that is exactly the `.tpl-split-host` repair shape), so this is REPORTED
        and NOT counted as a finding. Widening this to a finding would re-litigate a repair the
        receipts already accepted.

⛔ WHAT IT CANNOT SEE:
  · anything but an EXACT, whitespace-normalised selector-string match. `@container{ .a .b{} }`
    against `.b{container-type}` is the same defect and this probe is BLIND to it — the
    conservative matching is the price of zero false positives, and it is declared, not designed
    away. Equally `.a, .b{container-type}` vs `@container{ .a{} }` IS seen (comma lists split).
  · the DOM. It never asks whether an element matching the selector exists, nor whether one
    nests inside another matching the same selector — a nested pair means the INNER element
    fires legally while the outer stays dead (Layout-utilities' demo is exactly that shape).
    A finding therefore means "this rule is dead for the outermost match", not "dead for all".
  · NAMED containers where the name is carried on a different rule than `container-type`
    (`container-name` split across selectors) — the prelude name is matched against names
    declared on the SAME rule only; a mismatch SKIPS, never flags.
  · `@container` queries written against a container established in ANOTHER file (canon/type.css
    declares none today, measured — but the probe cannot see one if it appears).
  · anything outside the glob, and any container established by JavaScript.

GLOB — this probe rules only as wide as this list [[gate-glob-scope-rule]]:
    knowledge/snippets/*.reference.html
Widen with `--glob '<pattern>'` (repeatable); widening is a visible argument, never an inference.

ENVIRONMENT: sandbox (pure python, CSS text — no browser).

USAGE
  python3 knowledge/_probe_registry/probe_container_self_query.py --check
  python3 knowledge/_probe_registry/probe_container_self_query.py --check --glob 'reviews/*.html'
  python3 knowledge/_probe_registry/probe_container_self_query.py --selftest
EXIT: 0 clean · 1 findings.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob as globmod, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_GLOBS = ["knowledge/snippets/*.reference.html"]

STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
# `container-type: …` or the `container: <name> / <type>` shorthand. NOT `container-name:` alone
# — a name without a type establishes no container.
CONTAINER_DECL_RE = re.compile(r"(?<![\w-])container(?:-type)?\s*:", re.I)
CONTAINER_NAME_RE = re.compile(r"(?<![\w-])container-name\s*:\s*([^;}]+)", re.I)
SHORTHAND_NAME_RE = re.compile(r"(?<![\w-])container\s*:\s*([^;}/]+)/", re.I)


def _blank_out(pattern, text):
    """Erase matches but KEEP the line count — line numbers stay honest."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def stylesheets(raw):
    """The file's ACTIVE css, with html-commented regions blanked (a commented-out block is not
    css) and css comments blanked. Line numbers are preserved throughout."""
    live = _blank_out(HTML_COMMENT_RE, raw)
    out, pos = [], 0
    for m in STYLE_RE.finditer(live):
        out.append((m.start(1), m.group(1)))
    return [(off, _blank_out(CSS_COMMENT_RE, css)) for off, css in out]


def _blocks(css):
    """[(prelude, body, body_offset)] for every brace block at THIS level. Non-recursive."""
    res, buf, i, start = [], "", 0, 0
    while i < len(css):
        c = css[i]
        if c == "{":
            depth, j = 1, i + 1
            while j < len(css) and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            res.append((buf.strip(), css[i + 1:j - 1], i + 1))
            buf, i, start = "", j, j
            continue
        if c == "}":            # stray close — resynchronise, never crash [[a-crash-is-not-a-fail]]
            buf, i = "", i + 1
            continue
        buf += c
        i += 1
    return res


def _norm(sel):
    return re.sub(r"\s+", " ", sel).strip()


def _selectors(prelude):
    return [_norm(s) for s in prelude.split(",") if _norm(s)]


def _prelude_container_name(prelude):
    """The optional container NAME in an `@container` prelude, or None.
    `@container card (max-width:400px)` → 'card' · `@container (max-width:400px)` → None."""
    body = prelude[len("@container"):].strip()
    m = re.match(r"([A-Za-z_-][\w-]*)\s*(?=[({]|$)", body)
    if not m:
        return None
    tok = m.group(1)
    return None if tok.lower() in ("not", "style", "scroll-state") else tok


def _walk(css, offset, at_stack, containers, targets, lineof):
    for prelude, body, boff in _blocks(css):
        low = prelude.lower()
        if low.startswith("@"):
            if not low.startswith(("@media", "@supports", "@container", "@layer", "@scope")):
                continue        # @font-face / @keyframes / @property carry no selectors
            _walk(body, offset + boff, at_stack + (prelude,), containers, targets, lineof)
            continue
        if not prelude or prelude.startswith("@"):
            continue
        decls = body
        line = lineof(offset + boff)
        if CONTAINER_DECL_RE.search(decls):
            names = set()
            for rx in (CONTAINER_NAME_RE, SHORTHAND_NAME_RE):
                for m in rx.finditer(decls):
                    names |= {n for n in m.group(1).split() if n and n.lower() != "none"}
            for sel in _selectors(prelude):
                containers.setdefault(sel, []).append((line, frozenset(names)))
        for at in at_stack:
            if at.lower().startswith("@container"):
                want = _prelude_container_name(at)
                for sel in _selectors(prelude):
                    targets.setdefault(sel, []).append((line, want, _norm(at)))


def scan_file(path):
    """(findings, warns, containers, targets) for one file."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    containers, targets = {}, {}
    for off, css in stylesheets(raw):
        base = raw[:off].count("\n")
        _walk(css, 0, (), containers, targets,
              lambda p, base=base, css=css: base + css.count("\n", 0, p) + 1)
    findings, warns = [], []
    rel = os.path.relpath(path, ROOT)
    for sel in sorted(set(containers) & set(targets)):
        declared_names = set().union(*[n for _l, n in containers[sel]])
        hits = [(line, want, at) for line, want, at in targets[sel]
                # a NAMED query only ever resolves to a container carrying that name; if this
                # element does not carry it, the query is aimed elsewhere and is NOT this class.
                if want is None or want in declared_names]
        if not hits:
            continue
        others = sorted(s for s in containers if s != sel)
        cline = containers[sel][0][0]
        for line, _want, at in hits:
            detail = ("%s:%d `%s { container-type }` (line %d) is ALSO the target of `%s` — a "
                      "container query resolves against the nearest ANCESTOR container and an "
                      "element is never its own, so this rule cannot fire"
                      % (rel, line, sel, cline, at))
            if others:
                warns.append((rel, "CONTAINER-SELF-QUERY-WITH-HOST",
                              detail + " · WARN tier: this file ALSO declares container(s) %s, "
                              "which may legally host the query (the `.tpl-split-host` repair "
                              "shape) — reported, not counted" % others))
            else:
                findings.append((rel, "CONTAINER-SELF-QUERY", detail + " · this is the file's "
                                 "ONLY container selector, so nothing can host the query"))
    return findings, warns, containers, targets


def scan(paths, verbose=True):
    findings, warns = [], []
    for path in paths:
        f, w, containers, targets = scan_file(path)
        findings += f
        warns += w
        if verbose and (containers or targets):
            print("  %-3s %-52s containers=%-2d @container-targets=%-3d FAIL=%d WARN=%d"
                  % ("⛔" if f else ("⚠" if w else "OK"),
                     os.path.relpath(path, ROOT)[-52:], len(containers), len(targets),
                     len(f), len(w)))
    if verbose:
        for rel, kind, detail in findings:
            print("  ⛔ %s · %s" % (kind, detail))
        for rel, kind, detail in warns:
            print("  ⚠ %s" % detail)
    return findings, warns


def resolve(patterns, root=ROOT):
    out = []
    for pat in patterns:
        out += sorted(globmod.glob(os.path.join(root, pat)))
    return out


def check(patterns=None):
    patterns = patterns or DEFAULT_GLOBS
    paths = resolve(patterns)
    findings, warns = scan(paths)
    print("P-7 container self-query scan: %d file(s) over %s · %d finding(s) · %d WARN-tier"
          % (len(paths), patterns, len(findings), len(warns)))
    if not paths:
        print("⚠ THE GLOB MATCHED NOTHING — an empty population is not a pass "
              "(unmatched-grep-is-not-an-absence).")
        print("PROBE P-7 — findings=1")
        return 1
    print("PROBE P-7 — findings=%d" % len(findings))
    return 1 if findings else 0


def selftest():
    """PLANT-THEN-DETECT on a REAL snippet — and the PLANT IS VERIFIED TO HAVE PLANTED before
    any catch is asserted. ⛔ [[mutation-tests-the-clause-not-the-feature]]: the blind-harness
    class (a plant that never planted, then a green assert) has been paid for four times in this
    repo. The arms below therefore check the PARSED STATE of the fixture — the selector must
    appear in `containers` AND in `targets` — before checking that a finding came out."""
    fails = []
    tmp = tempfile.mkdtemp(prefix="p7-selftest-", dir=os.environ.get("TMPDIR", "/var/tmp"))

    # pick a real snippet that HAS a container and an @container rule but NO overlap today
    src = None
    for p in resolve(DEFAULT_GLOBS):
        f, w, containers, targets = scan_file(p)
        if containers and targets and not f and not w and len(containers) == 1:
            src = p
            break
    if not src:
        print("⛔ selftest cannot run: no snippet with exactly one container, at least one "
              "@container rule and no existing overlap (declared, never assumed).")
        return 1
    work = os.path.join(tmp, os.path.basename(src))
    shutil.copyfile(src, work)
    base_f, base_w, base_c, base_t = scan_file(work)
    victim = sorted(base_c)[0]
    print("  · fixture %s — containers=%s targets=%d baseline FAIL=%d WARN=%d"
          % (os.path.basename(src), sorted(base_c), len(base_t), len(base_f), len(base_w)))
    if victim in base_t:
        fails.append("FIXTURE UNFIT: %r is already an @container target on the pristine file"
                     % victim)

    raw = open(work, encoding="utf-8", errors="replace").read()
    plant = ("\n@container (max-width: 401px){ %s { outline:1px solid transparent; } }\n"
             % victim)

    # ---- ARM 1: the plant must PLANT (parsed state), then it must BITE (a FAIL-tier finding).
    m = list(STYLE_RE.finditer(HTML_COMMENT_RE.sub(lambda x: " " * len(x.group(0)), raw)))
    if not m:
        print("⛔ selftest cannot run: the fixture has no live <style> block to plant into.")
        return 1
    end = m[-1].end(1)
    open(work, "w", encoding="utf-8").write(raw[:end] + plant + raw[end:])
    f1, w1, c1, t1 = scan_file(work)
    planted = victim in c1 and victim in t1
    print("  · PLANT VERIFICATION — fixture re-parsed: %r in containers=%s, in @container "
          "targets=%s" % (victim, victim in c1, victim in t1))
    if not planted:
        fails.append("THE PLANT DID NOT PLANT: after injecting %r the parser does NOT see the "
                     "selector as both a container and an @container target — any 'catch' "
                     "below would be a blind harness" % plant.strip())
    new = [x for x in f1 if x not in base_f]
    if not new:
        fails.append("PLANT NOT CAUGHT: a verified container-self-query produced no finding")
    elif planted:
        print("  ✅ plant caught (CONTAINER-SELF-QUERY): %s" % new[0][2][:110])

    # ---- ARM 2: HEAL. Remove the plant, the probe must return to baseline.
    shutil.copyfile(src, work)
    f2, w2, _c, _t = scan_file(work)
    if (f2, w2) != (base_f, base_w):
        fails.append("REMOVAL NOT GREEN: restored fixture gave FAIL=%d WARN=%d, baseline "
                     "FAIL=%d WARN=%d" % (len(f2), len(w2), len(base_f), len(base_w)))
    else:
        print("  ✅ removal green: with the plant gone the probe returns to baseline (FAIL=%d)"
              % len(base_f))

    # ---- ARM 3: TIER CONTROL. The same overlap, but with a SECOND container in the file, must
    # be WARN and must NOT be a finding — the `.tpl-split-host` repair shape.
    host = "\n.p7-selftest-host{ container-type:inline-size; }\n"
    open(work, "w", encoding="utf-8").write(raw[:end] + plant + host + raw[end:])
    f3, w3, c3, t3 = scan_file(work)
    if "p7-selftest-host" not in " ".join(c3):
        fails.append("TIER CONTROL DID NOT PLANT: the second container is not in the parsed "
                     "container set %s" % sorted(c3))
    elif [x for x in f3 if x not in base_f]:
        fails.append("TIER LEAKED: an overlap with another container present in the file became "
                     "a FINDING — the accepted host repair would be re-litigated every run")
    elif not [x for x in w3 if x not in base_w]:
        fails.append("TIER BLIND: an overlap with a host present was not even reported as WARN")
    else:
        print("  ✅ tier control: the same overlap WITH a second container present is WARN, "
              "not a finding")

    # ---- ARM 4: PRECISION. A NAMED query aimed at a DIFFERENT name must not fire.
    named = ("\n@container p7-other (max-width: 401px){ %s { outline:0; } }\n" % victim)
    open(work, "w", encoding="utf-8").write(raw[:end] + named + raw[end:])
    f4, w4, _c, _t = scan_file(work)
    if [x for x in f4 if x not in base_f] or [x for x in w4 if x not in base_w]:
        fails.append("FALSE POSITIVE: a NAMED @container query for a name this element does not "
                     "declare was flagged — that query resolves elsewhere and is legal")
    else:
        print("  ✅ precision: `@container p7-other (…)` aimed at an element that declares no "
              "such name is NOT flagged")

    shutil.rmtree(tmp, ignore_errors=True)
    if fails:
        print("⛔ P-7 selftest: %d failure(s)" % len(fails))
        for x in fails:
            print("   " + x)
        return 1
    print("✅ P-7 selftest PASS — the plant was VERIFIED to have planted (parsed state, not "
          "assumed), it bit, its removal went green, the WARN tier held and a differently-named "
          "query stayed quiet.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    pats = [argv[i + 1] for i, a in enumerate(argv) if a == "--glob"]
    sys.exit(check(pats or None))
