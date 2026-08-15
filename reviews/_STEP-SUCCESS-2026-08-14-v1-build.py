#!/usr/bin/env python3
"""Build reviews/STEP-SUCCESS-SYSTEM-2026-08-14-v1.html.

Composes LIVE specimens from the REAL snippet markup and the REAL canon.css:
  AFTER  = ../knowledge/canon/canon.css   (working tree, regenerated this lane)
  BEFORE = ./_STEP-SUCCESS-2026-08-14-v1-BEFORE-canon.css  (git show HEAD:knowledge/canon/canon.css)
Each cell is an iframe so the two canon.css versions can never contaminate each other.
Contrast is measured with the repo's own _contrast_utils, never typed by hand.
"""
import os, sys, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "knowledge"))
from _contrast_utils import contrast_ratio as CR           # noqa: E402
sys.path.insert(0, os.path.join(REPO, "knowledge", "canon"))
import gen_theme_cascade as G                              # noqa: E402

THEMES = [("Apollo Mono", "mono", "apollo-mono"),
          ("Apollo Legacy", "legacy", "apollo-legacy"),
          ("Apollo Console", "console", "apollo-console"),
          ("Apollo Supercharge", "supercharge", "apollo-supercharge")]
MODES = [("Light", "light"), ("Dark", "dark")]

ts = {t["key"]: t for t in G.load_themes()}


def eff(key, path, mode):
    v = (ts[key]["overrides"].get(path) or {}).get(mode)
    return v or G.base_value(path, mode)


# ── markup, lifted from the reference snippets ────────────────────────────────
TRACKER = """
<div class="cn-progress-tracker"><div class="pt" style="--demo-width:100%">
  <ol class="steps" aria-label="Payment setup progress">
    <li class="done"><span class="dot" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#pt-check"/></svg></span><span class="step-label">Details</span></li>
    <li class="done"><span class="dot" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#pt-check"/></svg></span><span class="step-label">Amount</span></li>
    <li class="current" aria-current="step"><span class="dot" aria-hidden="true">3</span><span class="step-label">Review</span></li>
    <li><span class="dot" aria-hidden="true">4</span><span class="step-label">Confirm</span></li>
    <li><span class="dot" aria-hidden="true">5</span><span class="step-label">Receipt</span></li>
  </ol>
</div></div>"""

COLLAPSED = """
<div class="cn-progress-tracker"><div class="pt" style="--demo-width:320px">
  <div class="collapse" style="display:block">
    <div class="head"><span class="count">Step 3 of 5</span><span class="title">Review your payment</span></div>
    <div class="track" role="progressbar" aria-valuemin="1" aria-valuemax="5" aria-valuenow="3"
         aria-valuetext="Step 3 of 5" aria-label="Payment setup progress"><span class="fill" style="width:60%"></span></div>
  </div>
</div></div>"""

STEPPER = """
<div class="cn-stepper"><div class="st" style="--demo-width:100%">
  <ol class="steps">
    <li class="done"><span class="dot" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#pt-check"/></svg></span><span class="step-label">Account</span></li>
    <li class="done"><span class="dot" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#pt-check"/></svg></span><span class="step-label">Payee</span></li>
    <li class="current" aria-current="step"><span class="dot" aria-hidden="true">3</span><span class="step-label">Amount</span></li>
    <li><span class="dot" aria-hidden="true">4</span><span class="step-label">Review</span></li>
  </ol>
</div></div>"""

BAR = """
<div class="cn-progress-bar"><div class="pb">
  <div class="pb-head"><span class="pb-label t-cm-label">Transferring funds</span><span class="pb-value t-cm-figure-6">62%</span></div>
  <div class="pb-track" role="progressbar" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100"
       aria-valuetext="62 percent complete" aria-label="Transferring funds"><div class="pb-fill" style="width:62%"></div></div>
</div></div>"""

SYMBOL = ('<svg style="display:none" aria-hidden="true"><symbol id="pt-check" viewBox="0 0 18 18">'
          '<path fill-rule="evenodd" clip-rule="evenodd" d="M5.82617 15.685L0.0761719 9.93502L0.924172 9.08802L5.82617 '
          '13.988L17.0762 2.73901L17.9242 3.58701L5.82617 15.685Z" fill="currentColor"/></symbol></svg>')

SPECIMENS = [("The step tracker, wide", TRACKER),
             ("The same tracker, collapsed to a bar", COLLAPSED),
             ("The stepper", STEPPER),
             ("The progress bar, alongside", BAR)]

AFTER_CSS = "../knowledge/canon/canon.css"
BEFORE_CSS = "_STEP-SUCCESS-2026-08-14-v1-BEFORE-canon.css"
TYPE_CSS = "../knowledge/canon/type.css"


def frame(css, attr, mode, body):
    doc = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
           f'<link rel="stylesheet" href="{TYPE_CSS}"><link rel="stylesheet" href="{css}">'
           f'<style>html,body{{margin:0;}}'
           f'body{{padding:16px 12px;font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;'
           f'background:var(--background-default);color:var(--text-default);}}</style></head>'
           f'<body data-apollo-theme="{attr}" data-theme="{mode}">{SYMBOL}{body}</body></html>')
    return f'<iframe loading="lazy" srcdoc="{html.escape(doc, quote=True)}"></iframe>'


def swatch(hex_):
    return f'<span class="sw" style="background:{hex_}"></span>'


def verdict(v, floor):
    return "pass" if v >= floor else "fail"


rows = []
for label, attr, key in THEMES:
    for mlabel, mode in MODES:
        page = eff(key, "background/default", mode)
        fill = eff(key, "step/complete", mode)
        track = eff(key, "progress/incomplete", mode)
        prog = eff(key, "progress/complete", mode)
        rows.append(dict(theme=label, attr=attr, key=key, mlabel=mlabel, mode=mode,
                         page=page, fill=fill, track=track, prog=prog,
                         fp=CR(fill, page), ft=CR(fill, track), mf=CR(page, fill),
                         pt=CR(prog, track), pp=CR(prog, page)))

# ── page ──────────────────────────────────────────────────────────────────────
P = []
A = P.append
A('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
  '<meta name="viewport" content="width=device-width, initial-scale=1">'
  '<title>The completed step now uses the success system — for Dave\'s eye</title>'
  '<link rel="stylesheet" href="../knowledge/canon/type.css">')
A("""<style>
:root{--ink:#1A1A1A;--paper:#FFFFFF;--rule:#E1E1E1;--soft:#F7F7F7;--dim:#545454;
  --uf:"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif;}
*{box-sizing:border-box;}
body{margin:0;padding:48px 40px 96px;font-family:var(--uf);background:var(--paper);color:var(--ink);
  line-height:1.45;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1360px;margin:0 auto;}
h1{font:500 34px/1.2 var(--uf);margin:0 0 8px;}
h2{font:500 24px/1.25 var(--uf);margin:56px 0 4px;padding-top:24px;border-top:1px solid var(--rule);}
h3{font:500 17px/1.3 var(--uf);margin:32px 0 10px;}
p{font:400 16px/1.55 var(--uf);margin:0 0 14px;max-width:74ch;}
.lede{font-size:19px;color:var(--dim);max-width:74ch;}
.sw{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;
  margin-right:5px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.22);}
table{border-collapse:collapse;width:100%;font:400 14px/1.4 var(--uf);margin:8px 0 4px;}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);white-space:nowrap;}
th{font-weight:500;background:var(--soft);}
td.num{text-align:right;font-variant-numeric:tabular-nums;}
.pass{color:#137F3C;} .fail{color:#DA1A00;font-weight:500;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0 26px;}
.cell{border:1px solid var(--rule);}
.cap{font:500 13px/1.3 var(--uf);padding:8px 10px;background:var(--soft);border-bottom:1px solid var(--rule);}
.cap span{font-weight:400;color:var(--dim);}
iframe{width:100%;height:190px;border:0;display:block;background:#fff;}
iframe.tall{height:230px;}
.note{background:var(--soft);border-left:3px solid var(--ink);padding:14px 18px;margin:18px 0;}
.note p{margin:0 0 8px;} .note p:last-child{margin:0;}
.flag{border-left-color:#DA1A00;}
ul{font:400 16px/1.55 var(--uf);max-width:74ch;} li{margin-bottom:8px;}
code{font:400 14px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft);padding:1px 5px;}
</style></head><body><div class="wrap">""")

A("<h1>The completed step now borrows the success system</h1>")
A('<p class="lede">Everything on this page is a working change, uncommitted and unruled. '
  'It is here to be looked at. Nothing has been written into the decision record.</p>')

A("<h2>What changed, in plain words</h2>")
A("<p>A completed step used to be painted with ink — black in light mode, white in dark. "
  "You asked for it to use the same system as the success roundels, and to inherit that "
  "system wholesale rather than have each theme carry its own copied colour. That is what it now does. "
  "The completed step reads the same chain a success roundel reads, so each theme brings its own "
  "green with it: Mono a bright green, Console and Supercharge a slightly deeper one. None of those "
  "greens is new — they are the greens those themes already use for success elsewhere.</p>")
A("<p>Legacy is the exception you named. It does not take the green. In light mode a completed step "
  "is Legacy's error red, and in dark mode it is white — which is what the Legacy roundels already do "
  "in dark. This is the error red, not the brand red and not the amber: you said "
  "&ldquo;Legacy error, sorry my mistake&rdquo;, and that is the one that has been used.</p>")
A("<p>The tick inside a completed step changed too, and for the same reason. It used to be a fixed "
  "white mark. It now cuts through to whatever the page behind it is, exactly as the tick inside a "
  "success roundel does. On a light page the tick is white; on a dark page it is dark. The mark "
  "travels with the system instead of being restated.</p>")
A("<p>Separately, and unrelated to the green: the Legacy progress bar — the continuous one, not the "
  "step tracker — was quietly painting itself with Mono&rsquo;s black. Legacy&rsquo;s own ink is a "
  "softer grey. It was inheriting a value it had never actually agreed to, simply because nobody had "
  "written Legacy&rsquo;s answer down. It is written down now. In dark mode the value does not move.</p>")

A('<div class="note"><p><strong>One thing to look at hardest.</strong> In light mode the green sits '
  'very close to the white page and very close to the grey track behind it. Measured, that is under '
  'the usual 3:1 floor. This is not something introduced here — it is a property of the success '
  'colour itself, which the success roundels already carry everywhere else in the system, and you '
  'asked to inherit that system whole. The numbers are printed against every specimen below so you '
  'can judge it by eye and by figure at the same time. Nothing has been softened or adjusted to make '
  'it look better.</p></div>')

A("<h2>Before and after, side by side</h2>")
A("<p>Left is the system as it stands committed today. Right is the change. Both are the real "
  "component markup, rendered through the real stylesheet — the left through the committed one, the "
  "right through the regenerated one.</p>")
A('<div class="note"><p><strong>Why some of the left-hand cells look broken.</strong> They are. '
  'In Mono and Console the committed stylesheet paints the completed step with <em>nothing at all</em> '
  '— the colour was minted as a token but the stylesheet had never been regenerated to carry it, so '
  'the step fell back to the incomplete grey. That was a real defect sitting in the tree, not an '
  'artefact of this page, and regenerating is part of what fixed it.</p></div>')

for r in rows:
    A(f'<h3>{r["theme"]} &mdash; {r["mlabel"].lower()} mode</h3>')
    A('<table><tr><th>What is measured</th><th>Colours</th><th class="num">Contrast</th>'
      '<th class="num">Floor</th><th>Reading</th></tr>')
    for name, val, floor, fg, bg in [
            ("Completed step against the page", r["fp"], 3.0, r["fill"], r["page"]),
            ("Completed step against the remaining track", r["ft"], 3.0, r["fill"], r["track"]),
            ("Tick against the completed step", r["mf"], 3.0, r["page"], r["fill"]),
            ("Progress bar fill against its track", r["pt"], 3.0, r["prog"], r["track"])]:
        v = verdict(val, floor)
        A(f'<tr><td>{name}</td><td>{swatch(fg)}{fg} on {swatch(bg)}{bg}</td>'
          f'<td class="num">{val:.2f}:1</td><td class="num">{floor:.1f}:1</td>'
          f'<td class="{v}">{"clears it" if v == "pass" else "under the floor"}</td></tr>')
    A("</table>")
    A('<div class="grid">')
    for title, markup in SPECIMENS:
        A(f'<div class="cell"><div class="cap">Before <span>&mdash; {title}</span></div>'
          f'{frame(BEFORE_CSS, r["attr"], r["mode"], markup)}</div>')
        A(f'<div class="cell"><div class="cap">After <span>&mdash; {title}</span></div>'
          f'{frame(AFTER_CSS, r["attr"], r["mode"], markup)}</div>')
    A("</div>")

A("<h2>The whole picture in one table</h2>")
A('<table><tr><th>Theme</th><th>Mode</th><th>Completed step</th><th class="num">vs page</th>'
  '<th class="num">vs track</th><th class="num">tick vs step</th><th>Progress bar fill</th>'
  '<th class="num">vs track</th></tr>')
for r in rows:
    A(f'<tr><td>{r["theme"]}</td><td>{r["mlabel"]}</td><td>{swatch(r["fill"])}{r["fill"]}</td>'
      f'<td class="num {verdict(r["fp"],3)}">{r["fp"]:.2f}</td>'
      f'<td class="num {verdict(r["ft"],3)}">{r["ft"]:.2f}</td>'
      f'<td class="num {verdict(r["mf"],3)}">{r["mf"]:.2f}</td>'
      f'<td>{swatch(r["prog"])}{r["prog"]}</td>'
      f'<td class="num {verdict(r["pt"],3)}">{r["pt"]:.2f}</td></tr>')
A("</table>")
A("<p>The collapsed bar inside the step tracker uses the same two colours as the wide form, so its "
  "numbers are the &ldquo;vs track&rdquo; column exactly — it is the same component in a narrow "
  "container, not a second thing to measure.</p>")

A("<h2>What is still open</h2>")
A("<ul>"
  "<li>The light-mode green against the page and against the track, in Mono, Console and Supercharge. "
  "Measured under 3:1. Inherited from the success system by your instruction, and left exactly as it "
  "resolved. Yours to accept or send back.</li>"
  "<li>Nothing here has been written into the decision record. The token files carry the change and "
  "the reasoning, marked as working and awaiting your eye.</li>"
  "<li>The Legacy progress-bar grey is a separate judgement from the green. It can be accepted or "
  "refused on its own.</li>"
  "</ul>")
A("</div></body></html>")

out = os.path.join(HERE, "STEP-SUCCESS-SYSTEM-2026-08-14-v1.html")
open(out, "w").write("\n".join(P))
print("wrote", out, os.path.getsize(out), "bytes")
