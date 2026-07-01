#!/usr/bin/env python3
"""
Composed-screen pipeline runner — puts a *.canon.html screen through the SAME gates the
snippets pass, instead of trusting a hand audit. "Verification = enforcement."

Runs, on each composed screen:
  1. compose      — _validate_compose checks (rogue hex, no .c-/.cn- redefinition, classes
                    resolve, no native/accent-color control reinvention)
  2. icon-source  — _validate_icons logic: every inline <svg> path must byte-match the
                    assets/icons library (or be marked data-bespoke); shape-only icons flagged
  3. a11y         — _validate_a11y.check: reduced-motion present if it animates; target-size
  4. state-contrast (optional, --render) — _validate_state_contrast.audit_page driven over
                    every screen × light/dark with real hover/pressed states

Exits non-zero if any gate fails. Writes _SCREEN-GATE.md.
Usage:  python3 _validate_screen.py [--render] [path ...]   (default: _fitness-test/*.canon.html)
"""
import os, re, sys, glob, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
icons = importlib.import_module("_validate_icons")
a11y  = importlib.import_module("_validate_a11y")

def gate_icons(html):
    lib = icons.build_library()
    fails = []
    for blk in icons.SVGRE.findall(html):
        paths = icons.DRE.findall(blk)
        if "data-bespoke" in blk[:blk.find(">") + 1]:
            continue
        for d in paths:
            if icons.norm(d) not in lib:
                fails.append("UNKNOWN path d=\"%s…\"" % d[:48])
        if not paths and icons.SHAPERE.search(blk):
            fails.append("shape-only icon: " + re.sub(r"\s+", " ", blk)[:54] + "…")
    return fails

def gate_compose(path):
    # reuse the compose gate's per-screen checks
    comp = importlib.import_module("_validate_compose")
    fails, _ = comp.check_screen(path)
    return fails

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    render = "--render" in sys.argv
    files = args or sorted(glob.glob(os.path.join(HERE, "_fitness-test", "*.canon.html")))
    report = ["# Composed-screen gate — full pipeline on *.canon.html\n"]
    ok = True
    for path in files:
        name = os.path.basename(path)
        html = open(path, encoding="utf-8").read()
        report.append(f"## {name}")
        # 1. compose
        cf = gate_compose(path)
        report.append("- compose: " + ("✅" if not cf else "❌ " + "; ".join(cf)))
        # 2. icons
        icf = gate_icons(html)
        report.append("- icon-source: " + ("✅ all paths library-matched" if not icf
                      else f"❌ {len(icf)} UNKNOWN — " + "; ".join(icf[:6])))
        # 3. a11y
        _, af, aw = a11y.check(path)
        report.append("- a11y: " + ("✅" if not af else "❌ " + "; ".join(af)) +
                      (f"  (warn: {'; '.join(aw)})" if aw else ""))
        if cf or icf or af:
            ok = False
    if render:
        report.append("\n## state-contrast (rendered)")
        try:
            report += run_state_contrast(files)
            if globals().get("_SC_FAIL"): ok = False
        except Exception as e:
            report.append(f"- ⚠ could not run: {e}")
    open(os.path.join(HERE, "_SCREEN-GATE.md"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    print("\nRESULT:", "PASS ✅" if ok else "FAIL ❌")
    sys.exit(0 if ok else 1)

def run_state_contrast(files):
    """Drive every screen × light/dark through the real state-contrast gate."""
    sc = importlib.import_module("_validate_state_contrast")
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 460, "height": 860}, device_scale_factor=1)
        for path in files:
            pg.goto("file://" + os.path.abspath(path)); pg.wait_for_timeout(150)
            screens = pg.eval_on_selector_all(".screen", "els=>els.map(e=>e.dataset.screen)")
            for s in (screens or [None]):
                for theme in ("light", "dark"):
                    pg.evaluate(
                        "([s,t])=>{document.documentElement.setAttribute('data-theme',t);"
                        "document.querySelectorAll('.screen').forEach(x=>x.classList.toggle('is-active',x.dataset.screen===s));}",
                        [s, theme])
                    pg.wait_for_timeout(120)
                    sink = []
                    sc.audit_page(pg, f"{s}/{theme}", sink)   # appends (theme,label,fail) per failure
                    tag = f"{os.path.basename(path)} {s}/{theme}"
                    out.append(f"- {tag}: " + ("✅" if not sink else f"❌ {len(sink)} — " +
                               "; ".join(str(r[1:]) for r in sink[:4])))
                    if sink: globals()["_SC_FAIL"] = True
        b.close()
    return out

if __name__ == "__main__":
    main()
