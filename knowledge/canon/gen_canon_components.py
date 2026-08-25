#!/usr/bin/env python3
"""
Generate the canon COMPONENT layer FROM the gated snippets — verbatim CSS +
every decision comment, theme colours rewritten to token refs, scoped per
component so nothing collides. The snippets are the source of truth (they are
the final reviewed components); canon regenerates from them, so the review
decisions can never again be lost or diverge.

Per snippet knowledge/snippets/<Name>.reference.html:
  • slug = lowercased name; scope class = .cn-<slug>
  • #token-manifest vars {--v: "token/path"} -> .cn-<slug>{ --v: var(--token-path) }
    (auto light+dark via the token spine). driftAllow vars keep the snippet's
    OWN per-mode value (the intentional a11y deviation) + the reason as a comment.
  • :root non-colour vars (font/ease/sizes) carried verbatim into the scope.
  • all other CSS rules carried VERBATIM (comments + states + @media), each
    selector prefixed with .cn-<slug>; @keyframes namespaced to avoid collisions.
  • a header comment carries component + requiredAria + knownFindings + contrastPairs.
Harness rules (:root, [data-theme], body, *, html, .demo-controls, demo helpers) dropped.
Writes the block between AUTO-COMPONENTS markers in canon/canon.css (idempotent).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "snippets")
CANON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.css")

DROP_FIRST = ("body", "html", "*", ".demo-controls", ".cap", ".stateLabel")

def slug(name): return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

# ds-039, SECOND SPECIES (#213): manifest PROSE goes into a CSS comment, and CSS comments do
# not nest — the first `*/` in that prose CLOSES the header early, after which the remaining
# words parse as garbage selectors and Chromium drops EVERY RULE BELOW, the whole AUTO-THEMES
# cascade included. Measured live at #213: a `Finding:` quoting the shell probe
# `ls knowledge/assets/icons/**/ | grep ...` truncated canon.css at 4,094 parsed rules with
# ZERO [data-apollo-theme] rules reaching the browser; two such globs (Payment-card-visual #204
# and Standing-order-mandate-row #209) cost 3,135 rules and the entire four-theme layer.
# The #122 guard above only refused a literal '<'; a glob ending in `*/` walked straight past it.
# FIX THE CLASS AT THE EMITTER: no authored string can close the comment it is written into.
def cmt(text):
    """Make arbitrary prose safe to sit inside a CSS comment.

    The only unsafe sequence is the comment terminator; a single ASCII space breaks it
    without hiding anything from a reader (`icons/**/` reads as `icons/** /`). Deliberately
    NOT a zero-width character: an invisible fix is how this class survives the next audit.
    """
    return str(text).replace("*/", "* /")

def tokenvar(path): return "--" + path.replace("/", "-")

# ---------- tiny brace-aware CSS walker ----------
def walk(css):
    """Yield ('comment',text) | ('rule',selector,body) | ('at',header,inner) | ('decl',text)."""
    i, n = 0, len(css)
    while i < n:
        # whitespace
        if css[i].isspace():
            i += 1; continue
        # comment
        if css.startswith("/*", i):
            j = css.find("*/", i + 2); j = n if j < 0 else j + 2
            yield ("comment", css[i:j]); i = j; continue
        # at-rule
        if css[i] == "@":
            br = css.find("{", i); semi = css.find(";", i)
            if semi != -1 and (br == -1 or semi < br):
                yield ("decl", css[i:semi+1]); i = semi + 1; continue
            header = css[i:br].strip()
            depth, j = 1, br + 1
            while j < n and depth:
                if css[j] == "{": depth += 1
                elif css[j] == "}": depth -= 1
                j += 1
            yield ("at", header, css[br+1:j-1]); i = j; continue
        # normal rule
        br = css.find("{", i)
        if br == -1: break
        sel = css[i:br].strip()
        depth, j = 1, br + 1
        while j < n and depth:
            if css[j] == "{": depth += 1
            elif css[j] == "}": depth -= 1
            j += 1
        yield ("rule", sel, css[br+1:j-1]); i = j

# A GLOBAL-ROOT ancestor: :root / html (with any attribute tail), or a bare [data-*] state
# on the root. Mirrors the pattern prefix_selector uses to keep such an ancestor at the FRONT.
ROOT_ANCESTOR = re.compile(r'^((?::root|html)(?:\[[^\]]*\])*|\[[^\]]*\])\s+(.+)$')

def is_harness(sel):
    first = sel.split(",")[0].strip()
    if first in (":root",): return True
    # #203 Lane G — THE DARK-DROP REPAIR. A root-level ancestor followed by a DESCENDANT is a
    # real component rule, NOT a harness var block: `[data-theme="dark"] .se-msg .ic{color:#FFF}`
    # is a reviewed dark-mode decision. Judge such a selector by its DESCENDANT — prefix_selector
    # already knows how to hold the ancestor at the front and scope what follows; the old test
    # `first.startswith("[data-theme")` fired FIRST and so that machinery never saw these rules.
    # Measured blast radius before the fix: 33 rules across 19 snippets, silently absent from
    # canon.css with every gate green (Lane C receipt, 2026-08-19, finding 1).
    m = ROOT_ANCESTOR.match(first)
    if m: return is_harness(m.group(2))
    if first.startswith("[data-theme"): return True   # BARE [data-theme=…]{--v:…} = harness vars
    base = re.split(r"[ >.:\[]", first.lstrip(".#"))[0]
    fs = first.split()[0] if first.split() else first
    for d in DROP_FIRST:
        if fs == d or fs.startswith(d): return True
    if first in ("body", "html", "*"): return True
    return False

# #215 — THE ABSORB PREFIXER IS SPECIFICITY-NEUTRAL. Read this before "simplifying" it.
#
# The scope class this function adds is SCAFFOLDING: it exists to stop one component's rules
# reaching another component's markup in a shared stylesheet. It is NOT an authoring decision and
# it must NOT change which of the snippet's OWN rules beats which. A bare `.cn-x ` prefix does
# change that, because it is not added evenly:
#
#   snippet trim  :is(…,input[type=text],…):not(:has(svg))                     (0,1,2)
#   canon   trim  .cn-x :is(…,.cn-x input[type=text],…):not(:has(svg))         (0,3,2)   +2 classes
#   snippet ovr   .sn .sn-label                                                (0,2,0)
#   canon   ovr   .cn-x .sn .sn-label                                          (0,3,0)   +1 class
#
# (The trim collects TWO because `sel.split(",")` below splits inside `:is(…)` too, so the prefix
# lands on the :is() ARGUMENTS as well as the whole selector.) The trim gained one class more than
# the override did, so a ds-005 descender repair that WINS in the reviewed snippet LOSES in canon.
# Measured #214: 48 cascade-dead descender overrides in canon.css, none of them authored wrong.
#
# THE FIX AT CAUSE: wrap the ADDED scope in `:where()`, which contributes ZERO specificity
# (Selectors-4). `:where(.cn-x) .foo` matches EXACTLY the same elements as `.cn-x .foo` — the
# containment is unchanged — but the authored selector's specificity now passes through untouched,
# so the snippet's own cascade is reproduced verbatim in canon. Only the scope we add is wrapped;
# nothing authored is ever wrapped.
#
# ⛔ Do NOT go back to a bare `.{scope}` prefix. The descender gate's specificity leg
# (knowledge/_validate_descender_clip.py, SPECIFICITY_RATCHET) will go red, and the labels really
# do clip — that is a render-measured defect, not a lint.
def prefix_selector(sel, scope):
    out = []
    for part in sel.split(","):
        p = part.strip()
        if not p: continue
        # A leading GLOBAL-ROOT ancestor (:root[...], html[...], or a bare [data-*] state on the
        # root) must stay at the FRONT — scope the descendant AFTER it. Otherwise ".scope :root ..."
        # asks for a :root nested inside .scope, which never matches (e.g. the input-modality
        # ring-suppression rule :root[data-modality="pointer"] .box{...}).
        m = re.match(r'^((?::root|html)(?:\[[^\]]*\])*|\[[^\]]*\])\s+(.+)$', p)
        if m:
            out.append(f"{m.group(1)} :where(.{scope}) {m.group(2)}")
        else:
            out.append(f":where(.{scope}) {p}")
    return ", ".join(out)

def process(css, scope, kf_names):
    """Return component CSS (verbatim, comments kept) with selectors scoped."""
    lines = []
    for item in walk(css):
        if item[0] == "comment":
            lines.append(item[1]); continue
        if item[0] == "decl":
            lines.append(item[1]); continue
        if item[0] == "at":
            header, inner = item[1], item[2]
            kw = header.split()[0].lower()
            if kw == "@keyframes":
                name = header.split()[1]
                new = f"cn-{scope.split('cn-')[-1]}-{name}" if not name.startswith("cn-") else name
                kf_names[name] = new
                lines.append(f"@keyframes {new}{{{inner}}}")
            elif kw in ("@media", "@container", "@supports"):
                inner_scoped = process(inner, scope, kf_names)
                lines.append(f"{header}{{\n{inner_scoped}\n}}")
            else:
                lines.append(f"{header}{{{inner}}}")
            continue
        # rule
        sel, body = item[1], item[2]
        if is_harness(sel): continue
        lines.append(f"{prefix_selector(sel, scope)}{{{body.strip()}}}")
    return "\n".join(lines)

def theme_blocks(style):
    """Return {var:(light,dark)} from [data-theme=light/dark] blocks (and :root colour, if any)."""
    out = {}
    for mode in ("light", "dark"):
        m = re.search(r'\[data-theme="%s"\]\s*\{([^}]*)\}' % mode, style)
        if not m: continue
        for v, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)):
            out.setdefault(v, {})[mode] = val.strip()
    return out

def root_vars(style):
    """All :root custom props (colour + non-colour), across every :root block — verbatim into scope."""
    out = []
    for blk in re.findall(r":root\s*\{([^}]*)\}", style):
        out += [(v, val.strip()) for v, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", blk)]
    return out

# ds-039, THIRD SPECIES (#219): THE MARKUP SNIFFER DID NOT KNOW CSS'S OWN GRAMMAR.
#
# The guard below asks "is there a literal '<' left in the harvested <style> once CSS comments are
# gone?" — its intent is "markup leaked into what I am about to inject into canon.css". But '<' is
# also ORDINARY CSS: an @property descriptor names its type inside a QUOTED STRING —
#
#     @property --dvf1{syntax:"<number>"; inherits:true; initial-value:1;}
#
# — and there is no way to write @property without it. `Chart-bar.reference.html` gained three such
# registrations at #218 (crank seam 2, 8247c52) and from that commit on the generator REFUSED every
# run, so `gen_canon_components.py` and `--check` both exited 1 in CI and locally. Nothing was
# stale: the canon regen simply never got to run. This is the "no gate parses the artefact" class
# again (#122 ds-039) — the fix is to sniff in the CONSUMER'S grammar, so a '<' inside a CSS string
# is not markup, exactly as a '<' inside a CSS comment already was not.
#
# ⛔ Do NOT widen this to "strip everything in quotes anywhere" — the strings are stripped only for
# the SNIFF; the harvested CSS itself is still carried verbatim, quotes and all.
_CSS_STRING = re.compile(r'"(?:\\.|[^"\\])*"' + r"|'(?:\\.|[^'\\])*'")

def strip_css_noise(style):
    """The harvested <style> with CSS comments and CSS strings blanked — for the ds-039 sniff only."""
    no_comments = re.sub(r"/\*.*?\*/", "", style, flags=re.S)
    return _CSS_STRING.sub('""', no_comments)

def gen_one(path):
    html = open(path).read()
    name = os.path.basename(path).replace(".reference.html", "")
    sc = "cn-" + slug(name)
    # ds-039 (#122): strip HTML comments BEFORE harvesting — a '<style>' merely MENTIONED
    # in a documentation comment (Chart-butterfly-h) made the lazy regex swallow the
    # comment tail + <link> tag into canon.css, killing the CSS parser at that line and
    # silently dropping EVERY rule after it (the whole AUTO-THEMES block included).
    html_nc = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    style = re.search(r"<style>(.*?)</style>", html_nc, re.S).group(1)
    if "<" in strip_css_noise(style):
        raise SystemExit(f"gen_canon_components: HARVEST NOT CSS — literal '<' outside comments "
                         f"or CSS strings in harvested <style> of {os.path.basename(path)}; "
                         f"refusing to inject markup into canon.css (ds-039)")
    mm = re.search(r'id="token-manifest">(.*?)</script>', html, re.S)
    manifest = json.loads(mm.group(1)) if mm else {}
    vars_map = manifest.get("vars", {})
    drift = manifest.get("driftAllow", {})
    declared = theme_blocks(style)

    # ---- scope var block ----
    vb = [f".{sc}{{"]
    for v, val in root_vars(style):
        if v in declared: continue          # theme-block value takes precedence
        vb.append(f"  {v}: {val};")
    dark_over = []
    for v, token in vars_map.items():
        dmodes = drift.get(v, []) if isinstance(drift.get(v), list) else []
        if dmodes:
            # intentional deviation: keep snippet's own per-mode values
            lv = declared.get(v, {}).get("light"); dv = declared.get(v, {}).get("dark")
            vb.append(f"  {v}: {lv if lv else 'var(%s)'%tokenvar(token)};")
            if dv: dark_over.append(f"  {v}: {dv};")
        elif tokenvar(token) == v:
            # local var name == token css-var name: emitting --X:var(--X) is circular.
            # Skip — the global :root token already provides the value (and flips in dark).
            continue
        else:
            vb.append(f"  {v}: var({tokenvar(token)});")
    # vars present in theme blocks but NOT in manifest (local/proposed) -> carry literal both modes
    extra = [v for v in declared if v not in vars_map]
    for v in extra:
        lv = declared[v].get("light"); dv = declared[v].get("dark")
        if lv: vb.append(f"  {v}: {lv};")
        if dv and dv != lv: dark_over.append(f"  {v}: {dv};")
    vb.append("}")
    if dark_over:
        vb.append(f'[data-theme="dark"] .{sc}{{')
        vb += dark_over
        vb.append("}")

    # ---- component rules ----
    kf = {}
    body_css = process(style, sc, kf)
    for old, new in kf.items():  # rewrite animation name references
        body_css = re.sub(r"(animation(?:-name)?\s*:\s*[^;]*?)\b%s\b" % re.escape(old), r"\1%s" % new, body_css)

    # ---- decision header ----
    hdr = [f"/* ============================================================",
           f"   {name}  (from snippets/{name}.reference.html)"]
    if manifest.get("requiredAria"): hdr.append(f"   Aria: {cmt(', '.join(manifest['requiredAria']))}")
    if manifest.get("reuses"): hdr.append(f"   Reuses: {cmt(', '.join(manifest['reuses']) if isinstance(manifest['reuses'],list) else manifest['reuses'])}")
    for fnd in manifest.get("knownFindings", []) or []:
        hdr.append(f"   Finding: {cmt(fnd if isinstance(fnd,str) else json.dumps(fnd))}")
    if drift.get("$reason"): hdr.append(f"   Drift: {cmt(drift['$reason'])}")
    hdr.append(f"   Scope: .{sc}   ============================================================ */")
    return "\n".join(hdr) + "\n" + "\n".join(vb) + "\n" + body_css + "\n"

ORDER = ["Button","List-items","Cards","Headers","Navigations","Notifications","Modals","Input-fields",
 "Progress-tracker","Badge","Links","Tags","Status-indicator","Avatar","Divider","Table","Tabs",
 "Selection-controls","Search-field","Breadcrumbs","Pagination","Accordion","Tooltip","Quick-actions",
 "Dropdown","Hero","Slider","Reorder","Countdown-timer","View-options","Video-player","Loading-indicator"]

def build(css):
    """(new_full_css, made_names) — the regenerated file content, side-effect free."""
    blocks = ["/* ===== AUTO-COMPONENTS START =====",
              "   Generated from knowledge/snippets/*.reference.html by gen_canon_components.py.",
              "   VERBATIM component CSS + decision comments; theme colours -> token refs;",
              "   scoped .cn-<component>. Do NOT hand-edit between AUTO-COMPONENTS markers —",
              "   edit the snippet (the reviewed source of truth) and regenerate. */"]
    # curated order first, then any new snippets (e.g. reviewed gap-patterns) auto-appended
    all_files = sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))
    ordered = [os.path.join(SNIP, nm + ".reference.html") for nm in ORDER
               if os.path.exists(os.path.join(SNIP, nm + ".reference.html"))]
    extra = [f for f in all_files if f not in ordered]
    made = []
    for p in ordered + extra:
        blocks.append(gen_one(p)); made.append(os.path.basename(p).replace(".reference.html", ""))
    blocks.append("/* ===== AUTO-COMPONENTS END ===== */")
    comp_css = "\n".join(blocks)

    if "AUTO-COMPONENTS START" in css:
        new = re.sub(r"/\* ===== AUTO-COMPONENTS START =====.*?AUTO-COMPONENTS END ===== \*/",
                     comp_css, css, flags=re.S)
    else:
        new = css.rstrip() + "\n\n\n" + comp_css + "\n"
    return new, made

def main():
    # ADR-0013 ruling 4: this projector joins _build_all — regenerate-always (snippet
    # RULE-text changes self-heal into canon) + --check (determinism guard: a write step
    # followed by --check catches non-idempotent generator bugs, the project_canon
    # stomp class caught live 2026-07-21).
    import sys
    css = open(CANON).read()
    new, made = build(css)
    if "--check" in sys.argv:
        if new != css:
            print("gen_canon_components --check: canon.css AUTO-COMPONENTS is OUT OF SYNC with "
                  "the snippets. Run: python3 knowledge/canon/gen_canon_components.py")
            sys.exit(1)
        print(f"gen_canon_components --check OK — {len(made)} components in sync.")
        return
    if new != css:
        open(CANON, "w").write(new)
        print(f"generated {len(made)} components -> .cn-<scope>")
        print("components:", ", ".join(made))
    else:
        print(f"gen_canon_components: no change ({len(made)} components in sync).")

if __name__ == "__main__":
    main()
