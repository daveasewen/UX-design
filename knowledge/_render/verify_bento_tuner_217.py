#!/usr/bin/env python3
"""
verify_bento_tuner_217.py — the render-verify probe for knowledge/_fitness-test/bento-tuner-v1.html

s191-D2 home-or-declare: this probe lives in the repo, not in /var/tmp.

WHAT IT PROVES, and what each leg would INVALIDATE if it went red:

  L1  FONT, asserted against TWO CONTROLS (never a boolean).
      `document.fonts.check()` returns true in both a working and a broken fontconfig, so it
      cannot discriminate. A canvas width in the target cut must differ from a real other face
      AND from a face that does not exist. RED ⇒ every screenshot below is in the wrong cut and
      says nothing about how the page looks in the licensed face.

  L2  DANGLING VARS, all 8 states (4 themes x light/dark).
      Every FOREIGN custom property the page's stylesheet reads but does not declare must resolve
      NON-EMPTY, in every state. Negative control: a name that does not exist must resolve EMPTY,
      so the leg can fail. RED ⇒ some surface, ink, border or radius is silently falling back —
      the dangling-dataviz-var / silent-black class.

  L3  LIGHT != DARK ground, per theme. RED ⇒ the page only "works" because everything fell back.

  L4  THE DIALS ACTUALLY MOVE THE GRID.
      Drive gap / row / columns / radius through the page's own state object and MEASURE
      getComputedStyle on the live grid before and after. RED ⇒ the tuner is a picture of
      controls, not a controller, and every decision taken on it would be taken on a lie.

  L5  EXPORT PARITY — the pitfall this whole build was briefed against.
      After driving the dials to non-default values, the JSON rendered ON THE PAGE must agree
      with (a) the page's own state object and (b) the MEASURED computed style of the preview.
      RED ⇒ the export describes a wall Dave did not see, which is worse than no tuner.

  L6  RESPONSIVE BANDS are answered by the CONTAINER.
      Narrow the stage across each dialled band and count the tracks actually laid out; then MOVE
      a band dial and prove the collapse point moved with it. RED ⇒ the band dials are inert
      (this is the leg that would have caught inline custom properties beating container queries).

  L7  EMPHASIS RHYTHM. Change N and the offset; the set of promoted tiles must change to match.
      RED ⇒ the rhythm dial does not do what its label says.

Environment: see knowledge/_RUNBOOK-render-verify.md. Re-stage the farms; do not assume.
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
import re
import sys

from playwright.sync_api import sync_playwright

REPO = os.environ.get("REPO", "/sessions/lucid-sharp-curie/mnt/UX-design")
PAGE = "file://" + REPO + "/knowledge/_fitness-test/bento-tuner-v1.html"
SHOTS = os.environ.get("SHOTS", "/sessions/lucid-sharp-curie/mnt/outputs")

THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]

# every custom property the page's stylesheet READS but does not DECLARE
FOREIGN = [
    "--background-default", "--surface-raised", "--surface-subtle",
    "--tertiary-background-default", "--border-subtle", "--border-strong",
    "--text-default", "--text-secondary", "--focus-ring", "--focus-ring-width",
    "--border-radius-surface", "--border-radius-control",
    "--layout-app-gutter", "--layout-app-margin", "--target-min",
]

FAILS = []
NOTES = []


def check(ok, label, detail=""):
    tag = "PASS" if ok else "FAIL"
    line = "  [%s] %s%s" % (tag, label, ("  — " + detail if detail else ""))
    print(line)
    if not ok:
        FAILS.append(label + (" — " + detail if detail else ""))
    return ok


def px(s):
    try:
        return float(str(s).replace("px", "").strip())
    except (TypeError, ValueError):
        return None


def tracks(s):
    return len([t for t in str(s).strip().split() if t])


def main():
    shell = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))
    shell += glob.glob(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/var/tmp/pw-browsers-215")
                       + "/chromium_headless_shell-*/chrome-linux/headless_shell")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1440, "height": 1400})
        pg.goto(PAGE)
        pg.wait_for_timeout(1400)

        # ---------------- L1 · font, against two controls ----------------
        print("\nL1 · FONT — target vs two controls")
        widths = pg.evaluate("""() => {
          const c = document.createElement('canvas').getContext('2d');
          const m = f => { c.font = '40px ' + f; return c.measureText('Handgloves 12345').width; };
          return {
            target: m('HSBC_MtUnivers_Latin'),
            alias1: m('"Univers Next HSBC"'),
            alias2: m('"Univers Next for HSBC"'),
            dejavu: m('"DejaVu Sans"'),
            ghost:  m('"NoSuchFaceAnywhere12345"')
          };
        }""")
        print("     " + json.dumps(widths))
        check(widths["target"] != widths["ghost"] and widths["target"] != widths["dejavu"],
              "target cut differs from BOTH controls",
              "target=%s dejavu=%s ghost=%s" % (widths["target"], widths["dejavu"], widths["ghost"]))
        check(widths["alias1"] == widths["target"] and widths["alias2"] == widths["target"],
              "both canon font aliases land on the target cut")

        # ---------------- L2/L3 · dangling vars + light != dark ----------------
        print("\nL2 · DANGLING VARS — 8 states, every FOREIGN property non-empty")
        grounds = {}
        for t in THEMES:
            for m in MODES:
                pg.evaluate("""([t,m]) => {
                  document.documentElement.setAttribute('data-apollo-theme', t);
                  document.documentElement.setAttribute('data-theme', m);
                }""", [t, m])
                pg.wait_for_timeout(220)  # settle past the 160ms chrome transition before reading
                res = pg.evaluate("""(names) => {
                  const cs = getComputedStyle(document.body);
                  const out = {};
                  names.forEach(n => { out[n] = cs.getPropertyValue(n).trim(); });
                  out['__ghost'] = cs.getPropertyValue('--no-such-property-anywhere').trim();
                  out['__ground'] = getComputedStyle(document.body).backgroundColor;
                  out['__tileRadius'] = getComputedStyle(
                      document.querySelector('#gridPhoto .bt-photo')).borderTopLeftRadius;
                  return out;
                }""", FOREIGN)
                empties = [n for n in FOREIGN if not res[n]]
                check(not empties, "%s/%s — no dangling custom property" % (t, m),
                      "empty: " + ", ".join(empties) if empties else "%d resolved" % len(FOREIGN))
                check(res["__ghost"] == "", "%s/%s — negative control resolves EMPTY (the leg CAN fail)" % (t, m))
                grounds[(t, m)] = res["__ground"]
                NOTES.append("%s/%s ground=%s tile-radius=%s" % (t, m, res["__ground"], res["__tileRadius"]))

        print("\nL3 · LIGHT != DARK ground, per theme")
        for t in THEMES:
            check(grounds[(t, "light")] != grounds[(t, "dark")], "%s light != dark" % t,
                  "%s vs %s" % (grounds[(t, "light")], grounds[(t, "dark")]))

        # back to mono/light for the drive legs
        pg.evaluate("""() => {
          document.documentElement.setAttribute('data-apollo-theme','mono');
          document.documentElement.setAttribute('data-theme','light');
        }""")
        pg.wait_for_timeout(240)

        # ---------------- L4 · the dials actually move the grid ----------------
        print("\nL4 · DIAL DRIVE — measured before and after, on the live grid")
        before = pg.evaluate("""() => {
          const g = document.getElementById('gridPhoto');
          const cs = getComputedStyle(g);
          return {gap: cs.columnGap, row: cs.gridAutoRows, cols: cs.gridTemplateColumns,
                  radius: getComputedStyle(document.querySelector('#gridPhoto .bt-photo')).borderTopLeftRadius};
        }""")
        pg.evaluate("""() => {
          const T = window.__BENTO_TUNER__;
          T.set('gap', 34); T.set('row', 244); T.set('cols', 6);
        }""")
        pg.wait_for_timeout(240)
        after = pg.evaluate("""() => {
          const g = document.getElementById('gridPhoto');
          const cs = getComputedStyle(g);
          return {gap: cs.columnGap, row: cs.gridAutoRows, cols: cs.gridTemplateColumns};
        }""")
        print("     before: " + json.dumps(before))
        print("     after : " + json.dumps(after))
        check(px(after["gap"]) == 34, "gap dial moved the COMPUTED gap to 34px",
              "%s -> %s" % (before["gap"], after["gap"]))
        check(px(before["gap"]) != px(after["gap"]), "the gap actually CHANGED (not already 34)")
        check(px(after["row"]) == 244, "row dial moved grid-auto-rows to 244px",
              "%s -> %s" % (before["row"], after["row"]))
        check(tracks(after["cols"]) == 6, "column dial laid out 6 tracks",
              "%d -> %d" % (tracks(before["cols"]), tracks(after["cols"])))

        # radius dial — explicit mode
        pg.evaluate("""() => {
          document.querySelector('#rvRadiusMode button[data-v="explicit"]').click();
          window.__BENTO_TUNER__.set('radiusPx', 18);
        }""")
        pg.wait_for_timeout(240)
        rad = pg.evaluate("""() => getComputedStyle(
            document.querySelector('#gridPhoto .bt-photo')).borderTopLeftRadius""")
        check(px(rad) == 18, "radius dial moved the COMPUTED tile radius to 18px",
              "%s -> %s" % (before["radius"], rad))

        # ---------------- L5 · export parity ----------------
        print("\nL5 · EXPORT PARITY — page JSON vs state vs MEASURED preview")
        pg.evaluate("""() => {
          const T = window.__BENTO_TUNER__;
          T.set('th3', 3.20); T.set('th2', 1.10); T.set('thT', 1.60);
          T.set('rhythm', 4); T.set('offset', 2); T.set('b2', 900);
          document.querySelector('#rvShape button[data-v="wide"]').click();
        }""")
        pg.wait_for_timeout(260)
        parity = pg.evaluate("""() => {
          const shown = JSON.parse(document.getElementById('outJson').textContent);
          const live = window.__BENTO_TUNER__.exportObject();
          const g = document.getElementById('gridPhoto');
          const cs = getComputedStyle(g);
          return {
            shown: shown, live: live,
            same: JSON.stringify(shown) === JSON.stringify(live),
            measured: {
              gap: parseFloat(cs.columnGap),
              row: parseFloat(cs.gridAutoRows),
              cols: cs.gridTemplateColumns.trim().split(/\\s+/).filter(Boolean).length,
              radius: parseFloat(getComputedStyle(
                  document.querySelector('#gridPhoto .bt-photo')).borderTopLeftRadius)
            },
            css: document.getElementById('outCss').textContent
          };
        }""")
        s = parity["shown"]
        m = parity["measured"]
        check(parity["same"], "the JSON ON THE PAGE is byte-identical to the live state's export")
        check(s["grid"]["gutter_px"] == m["gap"], "export gutter == MEASURED gap",
              "%s vs %s" % (s["grid"]["gutter_px"], m["gap"]))
        check(s["grid"]["row_unit_px"] == m["row"], "export row unit == MEASURED grid-auto-rows",
              "%s vs %s" % (s["grid"]["row_unit_px"], m["row"]))
        check(s["grid"]["columns"] == m["cols"], "export columns == MEASURED track count",
              "%s vs %s" % (s["grid"]["columns"], m["cols"]))
        check(s["emphasis_rhythm"]["every_nth"] == 4 and s["emphasis_rhythm"]["starting_at_tile"] == 2
              and s["emphasis_rhythm"]["promoted_to"] == "2×1",
              "export carries the DIALLED rhythm, offset and shape",
              json.dumps(s["emphasis_rhythm"]))
        check(abs(s["aspect_thresholds"]["three_columns_at_or_wider_than"] - 3.20) < 1e-9
              and abs(s["aspect_thresholds"]["two_columns_at_or_wider_than"] - 1.10) < 1e-9
              and abs(s["aspect_thresholds"]["two_rows_at_or_taller_than"] - 1.60) < 1e-9,
              "export carries the DIALLED aspect thresholds")
        check(any(bd["container_max_width_px"] == 900 for bd in s["responsive_bands"]),
              "export carries the DIALLED band width (900px)")
        radius_export = s["tile_radius"]["resolved_px"]
        check(all(v == "18px" for v in radius_export.values()),
              "export radius is the DIALLED value in all 8 states", json.dumps(radius_export))
        # ⚠ STRIP THE COMMENTS FIRST. The export's own header says the words "no var() chain",
        # and a naive scrape of the flattened text reads that prose as the thing it forbids —
        # the document was right and the instrument was wrong (render-verify runbook, #11
        # pothole 3). Assert against the DECLARATIONS, which is the consumer's grammar.
        css_decls = re.sub(r"/\*.*?\*/", "", parity["css"], flags=re.S)
        check("var(" not in css_decls,
              "the CSS export's DECLARATIONS contain no live var() chain (s200-D1)",
              "offending: " + "; ".join(l.strip() for l in css_decls.splitlines() if "var(" in l))
        check_gap = str(int(m["gap"])) + "px"
        check(check_gap in css_decls, "the CSS export literally contains the measured gap", check_gap)
        # ⛔ the export must not carry the TUNER's private names, or it is inert when pasted
        leaked = [n for n in ["--bt-", ".bt-grid", ".bt-tile", ".bt-wrap", "btstage"] if n in css_decls]
        check(not leaked, "no page-private name leaks into the CSS export",
              "leaked: " + ", ".join(leaked) if leaked else "clean")
        check(css_decls.count("@container bento") == 3,
              "the export declares its OWN container and three bands",
              str(css_decls.count("@container bento")))

        # ---- and the same discipline in TOKEN mode, which is the DEFAULT position ----
        pg.evaluate("""() => { document.querySelector('#rvRadiusMode button[data-v="token"]').click(); }""")
        pg.wait_for_timeout(260)
        tok = pg.evaluate("""() => ({
            json: JSON.parse(document.getElementById('outJson').textContent),
            css: document.getElementById('outCss').textContent,
            measured: getComputedStyle(
                document.querySelector('#gridPhoto .bt-photo')).borderTopLeftRadius
        })""")
        tok_css = re.sub(r"/\*.*?\*/", "", tok["css"], flags=re.S)
        check("var(" not in tok_css,
              "TOKEN mode still exports CONCRETE radii — no var() in the declarations",
              "offending: " + "; ".join(l.strip() for l in tok_css.splitlines() if "var(" in l))
        check(tok["json"]["tile_radius"]["resolved_px"]["mono/light"] == tok["measured"],
              "TOKEN-mode export's mono/light radius == the MEASURED live radius",
              "%s vs %s" % (tok["json"]["tile_radius"]["resolved_px"]["mono/light"], tok["measured"]))
        print("     per-theme resolved tile radius: "
              + json.dumps(tok["json"]["tile_radius"]["resolved_px"]))
        pg.evaluate("""() => {
          document.querySelector('#rvRadiusMode button[data-v="explicit"]').click();
          window.__BENTO_TUNER__.set('radiusPx', 18);
        }""")
        pg.wait_for_timeout(200)

        # ---------------- L6 · bands answered by the CONTAINER ----------------
        print("\nL6 · RESPONSIVE BANDS — the container decides, and the band DIAL moves it")
        pg.evaluate("""() => { window.__BENTO_TUNER__.set('cols', 4);
                               window.__BENTO_TUNER__.set('b3',1100);
                               window.__BENTO_TUNER__.set('b2',820);
                               window.__BENTO_TUNER__.set('b1',520); }""")
        pg.wait_for_timeout(200)
        band_reads = {}
        for w in ["full", "1100", "820", "520"]:
            pg.evaluate("""(w) => {
              document.querySelector('#rvWidth button[data-v="' + w + '"]').click();
            }""", w)
            pg.wait_for_timeout(260)
            band_reads[w] = pg.evaluate("""() => getComputedStyle(document.getElementById('gridPhoto'))
                .gridTemplateColumns.trim().split(/\\s+/).filter(Boolean).length""")
        print("     " + json.dumps(band_reads))
        check(band_reads["full"] == 4, "full stage lays out 4 tracks", str(band_reads["full"]))
        check(band_reads["1100"] == 3, "at 1100px the stage collapses to 3", str(band_reads["1100"]))
        check(band_reads["820"] == 2, "at 820px the stage collapses to 2", str(band_reads["820"]))
        check(band_reads["520"] == 1, "at 520px the stage collapses to 1", str(band_reads["520"]))

        # move the band dial and prove the collapse point moved with it
        pg.evaluate("""() => {
          document.querySelector('#rvWidth button[data-v="1100"]').click();
          window.__BENTO_TUNER__.set('b2', 1200);
        }""")
        pg.wait_for_timeout(260)
        moved = pg.evaluate("""() => getComputedStyle(document.getElementById('gridPhoto'))
            .gridTemplateColumns.trim().split(/\\s+/).filter(Boolean).length""")
        check(moved == 2, "moving the 2-column band dial to 1200px collapses a 1100px stage to 2",
              "was 3 at this width, now %d" % moved)
        pg.evaluate("""() => { window.__BENTO_TUNER__.set('b2', 820);
                               document.querySelector('#rvWidth button[data-v="full"]').click(); }""")
        pg.wait_for_timeout(240)

        # ---------------- L7 · emphasis rhythm ----------------
        print("\nL7 · EMPHASIS RHYTHM — which tiles are promoted, and does N move them")
        def promoted_set():
            return pg.evaluate("""() => Array.from(
                document.querySelectorAll('#gridPhoto .bt-tile'))
                .map((t,i) => ({n:i+1, c:t.getAttribute('data-c'), r:t.getAttribute('data-r')}))
                .filter(t => t.c === '2' && t.r === '2').map(t => t.n)""")
        pg.evaluate("""() => {
          const T = window.__BENTO_TUNER__;
          document.querySelector('#rvShape button[data-v="big"]').click();
          T.set('rhythm', 5); T.set('offset', 1);
          T.set('th3', 4.0); T.set('th2', 1.45); T.set('thT', 1.15);
        }""")
        pg.wait_for_timeout(220)
        five = promoted_set()
        check(five == [1, 6, 11], "rhythm 5 from tile 1 promotes tiles 1, 6, 11", str(five))
        pg.evaluate("""() => { window.__BENTO_TUNER__.set('rhythm', 3); }""")
        pg.wait_for_timeout(220)
        three = promoted_set()
        check(three == [1, 4, 7, 10], "rhythm 3 promotes tiles 1, 4, 7, 10", str(three))
        pg.evaluate("""() => { window.__BENTO_TUNER__.set('rhythm', 0); }""")
        pg.wait_for_timeout(220)
        off = promoted_set()
        check(off == [], "rhythm 0 turns emphasis OFF entirely", str(off))

        # ---------------- L8 · the photographs actually paint ----------------
        # ⚠ the first mono/light shot showed twelve GREY BOXES: the tiles are `loading="lazy"`
        # and the element screenshot never scrolled them into view, so a page that was fine
        # rendered as a page with no photographs in it. Force-load, then ASSERT naturalWidth —
        # a screenshot alone could not tell "no image" from "grey image".
        print("\nL8 · PHOTOGRAPHS PAINT — forced eager, naturalWidth asserted")
        pg.evaluate("""() => {
          document.querySelectorAll('#gridPhoto img').forEach(i => { i.loading = 'eager'; });
        }""")
        pg.wait_for_timeout(300)
        pg.evaluate("""async () => {
          const imgs = Array.from(document.querySelectorAll('#gridPhoto img'));
          await Promise.all(imgs.map(i => i.complete ? Promise.resolve()
              : new Promise(r => { i.onload = r; i.onerror = r; })));
        }""")
        pg.wait_for_timeout(600)
        imgstat = pg.evaluate("""() => Array.from(document.querySelectorAll('#gridPhoto img'))
            .map(i => ({src: i.getAttribute('src').split('/').pop(), w: i.naturalWidth}))""")
        broken = [i["src"] for i in imgstat if not i["w"]]
        check(len(imgstat) == 12, "twelve photograph tiles built", str(len(imgstat)))
        check(not broken, "every photograph decoded (naturalWidth > 0)",
              "broken: " + ", ".join(broken) if broken else "12/12")

        # ---------------- L9 · clamped captions keep their descenders (ds-005) ----------------
        print("\nL9 · CLAMPED CAPTIONS — the cap/alphabetic trim must be opted out of")
        edges = pg.evaluate("""() => {
          const d = document.querySelector('#gridPhoto .bt-desc');
          const l = document.querySelector('#gridPhoto .bt-lic');
          const g = window.getComputedStyle;
          return {desc: g(d).textBoxEdge || g(d).getPropertyValue('text-box-edge'),
                  lic:  g(l).textBoxEdge || g(l).getPropertyValue('text-box-edge')};
        }""")
        check("cap" not in str(edges["desc"]), "clamped description is NOT cap-trimmed",
              json.dumps(edges))
        check("cap" not in str(edges["lic"]), "licence line is NOT cap-trimmed")

        # ---------------- L10 · the readout panel is not left STALE by the band transition -------
        # `.bt-stage` transitions max-width, so the readout taken in the same task as a width
        # change is the PRE-transition value. The panel showed "1 column" over a four-column wall.
        print("\nL10 · READOUTS SETTLE — the panel agrees with the wall after a band change")
        for w, want in [("520", 1), ("full", 4)]:
            pg.evaluate("""(w) => document.querySelector('#rvWidth button[data-v="' + w + '"]').click()""", w)
            pg.wait_for_timeout(600)   # past the 160ms transition AND the 240ms re-read
            shown = pg.evaluate("""() => parseInt(document.getElementById('r-cols').textContent, 10)""")
            live = pg.evaluate("""() => getComputedStyle(document.getElementById('gridPhoto'))
                .gridTemplateColumns.trim().split(/\\s+/).filter(Boolean).length""")
            check(shown == live == want,
                  "at stage %s the readout says %d and the grid IS %d" % (w, shown, live),
                  "expected %d" % want)

        # ---------------- screenshots: the smallest crop that carries the verdict ---------------
        print("\nSHOTS")
        pg.evaluate("""() => {
          const T = window.__BENTO_TUNER__;
          document.querySelector('#btnReset').click();
          document.querySelector('#rvWidth button[data-v="full"]').click();
        }""")
        # decode() every image before shooting — naturalWidth proves the file loaded, it does NOT
        # prove the frame was painted, and two tiles came out blank on the previous run
        pg.evaluate("""async () => {
          await Promise.all(Array.from(document.querySelectorAll('#gridPhoto img'))
            .map(i => i.decode().catch(() => {})));
        }""")
        pg.wait_for_timeout(900)
        os.makedirs(SHOTS, exist_ok=True)
        for t, m, name in [("mono", "light", "s217-tuner-stage-mono-light.png"),
                           ("supercharge", "dark", "s217-tuner-stage-supercharge-dark.png")]:
            pg.evaluate("""([t,m]) => {
              document.documentElement.setAttribute('data-apollo-theme', t);
              document.documentElement.setAttribute('data-theme', m);
            }""", [t, m])
            pg.wait_for_timeout(420)
            pg.locator("#btStage").screenshot(path=os.path.join(SHOTS, name))
            print("     " + name)
        pg.evaluate("""() => {
          document.documentElement.setAttribute('data-apollo-theme','mono');
          document.documentElement.setAttribute('data-theme','light');
        }""")
        pg.wait_for_timeout(300)
        # a second WIDTH — one width proves one layout and nothing else (runbook)
        pg.evaluate("""() => { document.querySelector('#rvWidth button[data-v="520"]').click();
                               document.querySelector('#rvShow button[data-v="photo"]').click(); }""")
        pg.wait_for_timeout(700)
        pg.locator("#btStage").screenshot(path=os.path.join(SHOTS, "s217-tuner-stage-520.png"))
        print("     s217-tuner-stage-520.png")
        pg.evaluate("""() => { document.querySelector('#rvWidth button[data-v="full"]').click();
                               document.querySelector('#rvShow button[data-v="both"]').click(); }""")
        pg.wait_for_timeout(800)   # past the stage transition AND the deferred readout re-read
        pg.locator("#dials").screenshot(path=os.path.join(SHOTS, "s217-tuner-dials.png"))
        pg.locator("#readouts").screenshot(path=os.path.join(SHOTS, "s217-tuner-readouts.png"))
        pg.locator("#export").screenshot(path=os.path.join(SHOTS, "s217-tuner-export.png"))
        print("     s217-tuner-dials.png / -readouts.png / -export.png")

        # VERDICT BEFORE ANY CLEANUP (2026-07-27 pothole: a teardown error can eat the verdict)
        print("\n=== VERDICT ===")
        if FAILS:
            print("RED — %d failing assertion(s):" % len(FAILS))
            for f in FAILS:
                print("   · " + f)
        else:
            print("GREEN — every leg passed.")
        print("\nper-state record:")
        for n in NOTES:
            print("   " + n)
        b.close()
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
