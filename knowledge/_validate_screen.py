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

Exits non-zero if any gate fails. Writes ONE record per subject —
`_screen-gate/<subject>.md` — plus `_SCREEN-GATE.md`, an index rebuilt from that directory
(#230 T5: the old wholesale rewrite meant gating one screen erased the record of every other).
Usage:  python3 _validate_screen.py [--render] [path ...]   (default: _fitness-test/*.canon.html)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
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

# ---------- #230 T5 — THE GATE MUST NOT WIPE ITS OWN RECORD.
# Until now this runner rewrote _SCREEN-GATE.md wholesale from the files given on the command
# line, so gating ONE screen deleted the record of every other — the file held 7 subjects, and
# SKILL step 5 tells every user to run it on their own screen. That is ADR-0017's write-once
# principle broken in miniature: many live facts sharing one home, so writing one erases the rest.
# THE SHAPE (not append — appending re-creates the same unbounded-file defect slowly):
#   • each subject gets its OWN home, knowledge/_screen-gate/<subject>.md, rewritten only when
#     that subject is gated;
#   • _SCREEN-GATE.md becomes an INDEX rebuilt from the DIRECTORY, never from this run's
#     argument list — so a run that touches one subject still leaves the other six addressed.
GATE_DIR = os.path.join(HERE, "_screen-gate")

def subject_file(name):
    """One home per subject. `name` is the screen's basename."""
    return os.path.join(GATE_DIR, re.sub(r"\.html?$", "", name) + ".md")

def write_index():
    """Rebuild _SCREEN-GATE.md from what is ON DISK — the whole population, not this run's."""
    rows = ["# Composed-screen gate — index\n",
            "One file per subject under `_screen-gate/`; this index is rebuilt from that",
            "directory on every run, so gating one screen never erases another (#230 T5).\n"]
    for f in sorted(glob.glob(os.path.join(GATE_DIR, "*.md"))):
        head = ""
        for line in open(f, encoding="utf-8"):
            if line.startswith("- verdict:"):
                head = line.strip()[len("- verdict:"):].strip(); break
        rows.append(f"- [`{os.path.basename(f)}`](_screen-gate/{os.path.basename(f)})"
                    + (f" — {head}" if head else ""))
    rows.append(f"\n{len(rows) - 3} subject(s) on record.")
    open(os.path.join(HERE, "_SCREEN-GATE.md"), "w").write("\n".join(rows) + "\n")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    render = "--render" in sys.argv
    files = args or sorted(glob.glob(os.path.join(HERE, "_fitness-test", "*.canon.html")))
    report = ["# Composed-screen gate — full pipeline on *.canon.html\n"]
    subjects = {}          # name -> its own lines (its own home)
    ok = True
    for path in files:
        name = os.path.basename(path)
        html = open(path, encoding="utf-8").read()
        lines = []
        report.append(f"## {name}")
        # 1. compose
        cf = gate_compose(path)
        lines.append("- compose: " + ("✅" if not cf else "❌ " + "; ".join(cf)))
        # 2. icons
        icf = gate_icons(html)
        lines.append("- icon-source: " + ("✅ all paths library-matched" if not icf
                     else f"❌ {len(icf)} UNKNOWN — " + "; ".join(icf[:6])))
        # 3. a11y
        _, af, aw, *_rest = a11y.check(path)
        lines.append("- a11y: " + ("✅" if not af else "❌ " + "; ".join(af)) +
                     (f"  (warn: {'; '.join(aw)})" if aw else ""))
        if cf or icf or af:
            ok = False
        lines.insert(0, "- verdict: " + ("PASS ✅" if not (cf or icf or af) else "FAIL ❌"))
        subjects[name] = lines
        report += lines[1:]
    if render:
        report.append("\n## state-contrast (rendered)")
        try:
            sc_lines = run_state_contrast(files)
            report += sc_lines
            # route each rendered line back to the subject it names (run_state_contrast
            # prefixes every line with the screen's basename) — same one-home rule.
            for name in subjects:
                mine = [ln for ln in sc_lines if ln.startswith(f"- {name} ")]
                if mine:
                    subjects[name] += ["", "### state-contrast (rendered)"] + mine
            if globals().get("_SC_FAIL"): ok = False
        except Exception as e:
            report.append(f"- ⚠ could not run: {e}")
    os.makedirs(GATE_DIR, exist_ok=True)
    for name, lines in subjects.items():
        open(subject_file(name), "w", encoding="utf-8").write(
            f"# {name}\n\n" + "\n".join(lines) + "\n")
    write_index()
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
