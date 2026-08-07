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
import os, re, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "snippets")
CANON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.css")

DROP_FIRST = ("body", "html", "*", ".demo-controls", ".cap", ".stateLabel")

def slug(name): return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

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

def is_harness(sel):
    first = sel.split(",")[0].strip()
    if first in (":root",) or first.startswith("[data-theme"): return True
    base = re.split(r"[ >.:\[]", first.lstrip(".#"))[0]
    fs = first.split()[0] if first.split() else first
    for d in DROP_FIRST:
        if fs == d or fs.startswith(d): return True
    if first in ("body", "html", "*"): return True
    return False

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
            out.append(f"{m.group(1)} .{scope} {m.group(2)}")
        else:
            out.append(f".{scope} {p}")
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
    if "<" in re.sub(r"/\*.*?\*/", "", style, flags=re.S):
        raise SystemExit(f"gen_canon_components: HARVEST NOT CSS — literal '<' outside comments "
                         f"in harvested <style> of {os.path.basename(path)}; refusing to inject markup into canon.css (ds-039)")
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
    if manifest.get("requiredAria"): hdr.append(f"   Aria: {', '.join(manifest['requiredAria'])}")
    if manifest.get("reuses"): hdr.append(f"   Reuses: {', '.join(manifest['reuses']) if isinstance(manifest['reuses'],list) else manifest['reuses']}")
    for fnd in manifest.get("knownFindings", []) or []:
        hdr.append(f"   Finding: {fnd if isinstance(fnd,str) else json.dumps(fnd)}")
    if drift.get("$reason"): hdr.append(f"   Drift: {drift['$reason']}")
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
