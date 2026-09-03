"""Render-proof for reviews/RADIUS-TUNER-2026-09-03-v1.html — #244 lane B, 2026-09-03.

Run from the repo root, in ONE bash call (the seat env is per-call):

    export TMPDIR=/dev/shm && source knowledge/_render/seat_env.sh && python3 <this file>

Loads the page with goto("file://…") — never set_content, which drops the inlined stylesheets
silently. Asserts COMPUTED borderTopLeftRadius on 17 specimens x 2 modes x 4 themes against the
token store as it sits on disk, then drives two mutation arms:
  MUT1  mono border-radius/surface -> 18: card/banner/dialog must move, button must NOT (role isolation)
  MUT2  console segmented-container/m -> 16: thumb/m must become 14 (concentric max(16-2,0)),
        scale l must NOT move (per-scale isolation)
Exit reading is the FAILS count at the foot; 0 was the reading on 2026-09-03.
"""
import json, os
from playwright.sync_api import sync_playwright

URL = "file://" + os.path.abspath("reviews/RADIUS-TUNER-2026-09-03-v1.html")
STORE = {
 "mono":        dict(default=0, control=0, surface=0, indicator=0, container=0, segc=dict(xs=0,s=0,m=0,l=0), segt=dict(xs=0,s=0,m=0,l=0)),
 "legacy":      dict(default=0, control=0, surface=0, indicator=0, container=0, segc=dict(xs=0,s=0,m=0,l=0), segt=dict(xs=0,s=0,m=0,l=0)),
 "console":     dict(default=4, control=8, surface=20, indicator=4, container=20, segc=dict(xs=6,s=8,m=10,l=12), segt=dict(xs=4,s=6,m=8,l=8)),
 "supercharge": dict(default=0, control=0, surface=0, indicator=0, container=0, segc=dict(xs=0,s=0,m=0,l=0), segt=dict(xs=0,s=0,m=0,l=0)),
}
PROBE = """(() => {
  const q = (s) => document.querySelector(s);
  const br = (el) => el ? getComputedStyle(el).borderTopLeftRadius : null;
  const out = {};
  for (const mode of ["light","dark"]) {
    const p = `.tn-pane[data-theme="${mode}"] `;
    out[mode] = {
      button: br(q(p+".cn-button .btn.primary")), input: br(q(p+".cn-input-fields .box")),
      tag: br(q(p+".cn-tags .tag")), chip: br(q(p+".cn-status-indicator .chip")),
      card: br(q(p+".cn-cards .card.action")), banner: br(q(p+".cn-banner .banner.err")),
      dialog: br(q(p+".cn-modals .dialog")), dlgbtn: br(q(p+".cn-modals .btn.primary")),
      shell: br(q(p+".cn-container-shell .shell")),
      seg_xs: br(q(p+".cn-segmented-control .seg.xs")), seg_s: br(q(p+".cn-segmented-control .seg.s")),
      seg_m: br(q(p+".cn-segmented-control .seg.m")), seg_l: br(q(p+".cn-segmented-control .seg.l")),
      thumb_xs: br(q(p+".cn-segmented-control .seg.xs .ind")), thumb_s: br(q(p+".cn-segmented-control .seg.s .ind")),
      thumb_m: br(q(p+".cn-segmented-control .seg.m .ind")), thumb_l: br(q(p+".cn-segmented-control .seg.l .ind")),
      indw: (q(p+".cn-segmented-control .seg.m .ind")||{}).offsetWidth
    };
  }
  out.rows = document.querySelectorAll("#readoutBody tr").length;
  return out;
})()"""

fails, rep = [], {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    pg = b.new_page(viewport={"width":1600,"height":1200})
    errs = []
    pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: "+str(e)))
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(400)
    for theme in ["mono","legacy","console","supercharge"]:
        pg.evaluate("t => window.__radiusTuner.setTheme(t)", theme); pg.wait_for_timeout(150)
        r = pg.evaluate(PROBE); st = STORE[theme]; rep[theme] = r
        exp = {"button":st["control"],"input":st["control"],"tag":st["control"],"chip":st["indicator"],
               "card":st["surface"],"banner":st["surface"],"dialog":st["surface"],"dlgbtn":st["control"],
               "shell":st["container"],"seg_xs":st["segc"]["xs"],"seg_s":st["segc"]["s"],
               "seg_m":st["segc"]["m"],"seg_l":st["segc"]["l"],"thumb_xs":st["segt"]["xs"],
               "thumb_s":st["segt"]["s"],"thumb_m":st["segt"]["m"],"thumb_l":st["segt"]["l"]}
        for mode in ("light","dark"):
            for k, v in exp.items():
                if r[mode][k] != f"{v}px": fails.append(f"{theme}/{mode}/{k}: want {v}px got {r[mode][k]}")
            if not r[mode]["indw"]: fails.append(f"{theme}/{mode}: segmented indicator width 0")
    pg.evaluate("() => window.__radiusTuner.setTheme('mono')")
    pg.evaluate("() => window.__radiusTuner.setDial('role','surface',18)"); pg.wait_for_timeout(120)
    m = pg.evaluate(PROBE); rep["MUT1"] = m
    for mode in ("light","dark"):
        for k in ("card","banner","dialog"):
            if m[mode][k] != "18px": fails.append(f"MUT1 mono/{mode}/{k}: want 18px got {m[mode][k]}")
        if m[mode]["button"] != "0px": fails.append(f"MUT1 mono/{mode}/button leaked {m[mode]['button']}")
    pg.evaluate("() => window.__radiusTuner.setTheme('console')")
    pg.evaluate("() => window.__radiusTuner.setDial('segc','m',16)"); pg.wait_for_timeout(120)
    m2 = pg.evaluate(PROBE); rep["MUT2"] = m2
    for mode in ("light","dark"):
        if m2[mode]["seg_m"]   != "16px": fails.append(f"MUT2 seg_m {m2[mode]['seg_m']}")
        if m2[mode]["thumb_m"] != "14px": fails.append(f"MUT2 thumb_m want 14px got {m2[mode]['thumb_m']}")
        if m2[mode]["seg_l"]   != "12px": fails.append(f"MUT2 seg_l leaked {m2[mode]['seg_l']}")
    rep["console_errors"] = errs
    b.close()

print(json.dumps(rep, indent=1))
print("=== FAILS:", len(fails))
for f in fails: print("  -", f)
