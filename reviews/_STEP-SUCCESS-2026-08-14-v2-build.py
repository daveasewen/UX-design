#!/usr/bin/env python3
"""Build reviews/STEP-SUCCESS-SYSTEM-2026-08-14-v2.html.

v2 = v1 plus the four refinements Dave ruled off the rendered v1 page.

Composes LIVE specimens from the REAL snippet markup and the REAL canon.css:
  AFTER  = ../knowledge/canon/canon.css (working tree, regenerated this lane)
  BEFORE = the SAME stylesheet with the three v1 values restored inline, so the
           left column is exactly what Dave looked at on the v1 page. This is an
           honest reconstruction of three named properties, not a second build of
           the whole tree — it is labelled as such on the page.
Contrast is measured with the repo's own _contrast_utils, never typed by hand.
Gated legs (tick-on-fill 3:1, label-on-page 4.5:1) are visually separated from
the declared-absence legs (fill-on-page, fill-on-track) per Dave's #176 doctrine.
"""
import os, sys, json, html

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
    v = (ts[key]["overrides"].get(path) or {}).get(mode) if key in ts else None
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

# the two tick weights, both byte-matched library assets
D_THIN = ("M5.82617 15.685L0.0761719 9.93502L0.924172 9.08802L5.82617 13.988"
          "L17.0762 2.73901L17.9242 3.58701L5.82617 15.685Z")          # status-icons/yes.svg
D_THICK = ("M5.91547 15.9421L0.105469 10.1341L1.37747 8.86011L5.91547 13.3971"
           "L16.6215 2.69312L17.8935 3.96712L5.91547 15.9421Z")        # status-icons/yes-thick.svg


def symbol(d):
    return ('<svg style="display:none" aria-hidden="true"><symbol id="pt-check" viewBox="0 0 18 18">'
            f'<path fill-rule="evenodd" clip-rule="evenodd" d="{d}" fill="currentColor"/></symbol></svg>')


SPECIMENS = [("The step tracker, wide", TRACKER),
             ("The same tracker, collapsed to a bar", COLLAPSED),
             ("The stepper", STEPPER),
             ("The progress bar, alongside", BAR)]

AFTER_CSS = "../knowledge/canon/canon.css"
TYPE_CSS = "../knowledge/canon/type.css"


def frame(attr, mode, body, before=False, key=None):
    """One isolated iframe. BEFORE restores the three v1 values inline."""
    extra = ""
    if before:
        v1_fill = "#A8000B" if key == "apollo-legacy" and mode == "light" else eff(key, "step/complete", mode)
        v1_mark = eff(key, "background/default", mode)      # v1 policy: the mark knocked to the page
        extra = (f'<style>[data-apollo-theme] .cn-progress-tracker,[data-apollo-theme] .cn-stepper{{'
                 f'--complete:{v1_fill};--on-complete:{v1_mark};}}</style>')
    doc = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
           f'<link rel="stylesheet" href="{TYPE_CSS}"><link rel="stylesheet" href="{AFTER_CSS}">{extra}'
           f'<style>html,body{{margin:0;}}'
           f'body{{padding:12px 4px;font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;'
           f'background:var(--background-default);color:var(--text-default);}}</style></head>'
           f'<body data-apollo-theme="{attr}" data-theme="{mode}">'
           f'{symbol(D_THIN if before else D_THICK)}{body}</body></html>')
    return f'<iframe loading="lazy" srcdoc="{html.escape(doc, quote=True)}"></iframe>'


def swatch(hex_):
    return f'<span class="sw" style="background:{hex_}"></span>'


rows = []
for label, attr, key in THEMES:
    for mlabel, mode in MODES:
        page = eff(key, "background/default", mode)
        fill = eff(key, "step/complete", mode)
        tick = eff(key, "step/on-complete", mode)
        track = eff(key, "progress/incomplete", mode)
        ink = eff(key, "text/default", mode)
        prog = eff(key, "progress/complete", mode)
        rows.append(dict(theme=label, attr=attr, key=key, mlabel=mlabel, mode=mode,
                         page=page, fill=fill, tick=tick, track=track, ink=ink, prog=prog,
                         tick_fill=CR(tick, fill), label_page=CR(ink, page),
                         fill_page=CR(fill, page), fill_track=CR(fill, track),
                         prog_track=CR(prog, track)))

json.dump(rows, open(os.path.join(HERE, "_STEP-SUCCESS-2026-08-14-v2-contrast.json"), "w"), indent=1)
FAILS = [r for r in rows if r["tick_fill"] < 3.0 or r["label_page"] < 4.5]

P = []
A = P.append
A('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
  '<meta name="viewport" content="width=device-width, initial-scale=1">'
  '<title>The completed step, refined — for Dave\'s eye</title>'
  '<link rel="stylesheet" href="../knowledge/canon/type.css">')
A("""<style>
:root{--ink:#1A1A1A;--paper:#FFFFFF;--rule:#E1E1E1;--soft:#F7F7F7;--dim:#545454;
  --uf:"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif;}
*{box-sizing:border-box;}
body{margin:0;padding:48px 22px 96px;font-family:var(--uf);background:var(--paper);color:var(--ink);
  line-height:1.45;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1360px;margin:0 auto;}
h1{font:500 34px/1.2 var(--uf);margin:0 0 8px;}
h2{font:500 24px/1.25 var(--uf);margin:56px 0 4px;padding-top:24px;border-top:1px solid var(--rule);}
h3{font:500 17px/1.3 var(--uf);margin:32px 0 10px;}
h4{font:500 14px/1.3 var(--uf);margin:16px 0 4px;color:var(--dim);}
p{font:400 16px/1.55 var(--uf);margin:0 0 14px;max-width:74ch;}
.lede{font-size:19px;color:var(--dim);max-width:74ch;}
.sw{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;
  margin-right:5px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.22);}
table{border-collapse:collapse;width:100%;font:400 14px/1.4 var(--uf);margin:4px 0 4px;}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);white-space:nowrap;}
th{font-weight:500;background:var(--soft);}
td.num{text-align:right;font-variant-numeric:tabular-nums;}
.pass{color:#137F3C;} .fail{color:#DA1A00;font-weight:500;}
table.gated{box-shadow:inset 3px 0 0 var(--ink);}
table.gated th{background:#EFEFEF;}
table.absent{opacity:.86;}
table.absent th,table.absent td{border-bottom-style:dashed;}
table.absent th{background:transparent;font-style:normal;color:var(--dim);}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0 26px;}
.cell{border:1px solid var(--rule);}
.cap{font:500 13px/1.3 var(--uf);padding:8px 10px;background:var(--soft);border-bottom:1px solid var(--rule);}
.cap span{font-weight:400;color:var(--dim);}
iframe{width:100%;height:190px;border:0;display:block;background:#fff;}
.note{background:var(--soft);border-left:3px solid var(--ink);padding:14px 18px;margin:18px 0;}
.note p{margin:0 0 8px;} .note p:last-child{margin:0;}
.flag{border-left-color:#DA1A00;background:#FDF3F1;}
ul{font:400 16px/1.55 var(--uf);max-width:74ch;} li{margin-bottom:8px;}
code{font:400 14px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft);padding:1px 5px;}
</style></head><body><div class="wrap">""")

A("<h1>The completed step, refined</h1>")
A('<p class="lede">This is the previous page with your four corrections applied. '
  'Everything is still working and uncommitted. Nothing has been written into the decision record.</p>')

A("<h2>What you changed, in plain words</h2>")
A("<p><strong>The tick is now dark ink, not the page.</strong> You said Apollo Mono uses the dark "
  "ink colour for its glyphs, in the same way the roundels do. It does now: the tick inside a "
  "completed step is the same near-black the success roundel's tick already uses, and it stays that "
  "colour in both light and dark, exactly as the roundel mark does. Console and Supercharge already "
  "declare the same near-black for their own roundels, so they simply agree with it rather than "
  "needing their own copy. That was checked by reading their files, not assumed from the name.</p>")
A("<p><strong>Legacy is the one theme that cannot just follow.</strong> Legacy's roundel tick is "
  "white, because Legacy's roundels are dark fills. So on Legacy's red step, the tick is white — "
  "that is Legacy's own existing rule doing its normal job. But Legacy's completed step in dark mode "
  "is itself white, and a white tick on a white disc is no tick at all. So in Legacy dark, and only "
  "there, the tick has been turned dark. You have not ruled on that one, and it is flagged below.</p>")
A("<p><strong>The tick is the thick one.</strong> Every completed-step tick now uses the thick "
  "library asset rather than the thin one. It is the real asset from the icon library, not a redrawn "
  "path — the icon gate matches it character-for-character against the library file, and it passes.</p>")
A("<p><strong>Legacy's red is the primary red again.</strong> You looked at the page and said to use "
  "the primary red. It is back to that. The full sequence is recorded so no one re-opens it: it "
  "started as the primary red, moved to the darker error red in conversation, and has come back to "
  "the primary red having been seen. The white in dark mode is untouched.</p>")

A("<h2>Your rule about where contrast has to live</h2>")
A('<div class="note"><p>You said, of this component: the meaning is carried by the glyph and the '
  'label, so the track and the roundels matter less for contrast &mdash; <strong>the label and the '
  'symbol must carry the contrast, not the decoration.</strong></p>'
  '<p>That has been taken as the rule and written into the component files, the token files and the '
  'comments that explain the missing measurements. It changes what gets measured and what gets '
  'enforced. From here on, two things are checked on every build and will stop it if they fail: '
  '<strong>the tick against the step it sits on</strong>, and <strong>the step label against the '
  'page</strong>. Two things are recorded but deliberately not enforced: the step fill against the '
  'page, and the step fill against the remaining track. Those are decoration.</p>'
  '<p>Both kinds are printed below. The enforced ones are in the bordered table. The recorded ones '
  'are in the lighter dashed table underneath, and a low number there is not a defect.</p></div>')

if FAILS:
    A('<div class="note flag"><p><strong>Something enforced is failing.</strong> '
      + "; ".join(f'{r["theme"]} {r["mlabel"].lower()}' for r in FAILS) +
      '. It has been left exactly as it measured &mdash; not adjusted, not softened.</p></div>')
else:
    A('<div class="note"><p><strong>Every enforced leg passes.</strong> The lowest tick-against-step '
      f'reading anywhere is {min(r["tick_fill"] for r in rows):.2f}:1 against a 3:1 floor, and the '
      f'lowest label-against-page reading is {min(r["label_page"] for r in rows):.2f}:1 against 4.5:1. '
      'Nothing was changed to achieve that.</p></div>')

A("<h2>Before and after, side by side</h2>")
A("<p>Left is the version you looked at last: the thin tick, the tick knocked through to the page, "
  "and Legacy's darker red. Right is the same components with your four corrections. Both are the "
  "real component markup rendered through the real regenerated stylesheet; the left-hand cells put "
  "the three old values back over the top, so the comparison is of those three things and nothing "
  "else.</p>")

for r in rows:
    A(f'<h3>{r["theme"]} &mdash; {r["mlabel"].lower()} mode</h3>')
    A("<h4>Enforced &mdash; the symbol and the label carry the meaning</h4>")
    A('<table class="gated"><tr><th>What is measured</th><th>Colours</th><th class="num">Contrast</th>'
      '<th class="num">Floor</th><th>Reading</th></tr>')
    for name, val, floor, fg, bg in [
            ("The tick against the step it sits on", r["tick_fill"], 3.0, r["tick"], r["fill"]),
            ("The step label against the page", r["label_page"], 4.5, r["ink"], r["page"])]:
        v = "pass" if val >= floor else "fail"
        A(f'<tr><td>{name}</td><td>{swatch(fg)}{fg} on {swatch(bg)}{bg}</td>'
          f'<td class="num">{val:.2f}:1</td><td class="num">{floor:.1f}:1</td>'
          f'<td class="{v}">{"clears it" if v == "pass" else "UNDER THE FLOOR"}</td></tr>')
    A("</table>")
    A("<h4>Recorded, not enforced &mdash; decoration, by your rule</h4>")
    A('<table class="absent"><tr><th>What is measured</th><th>Colours</th><th class="num">Contrast</th>'
      '<th>Status</th></tr>')
    for name, val, fg, bg in [
            ("The completed step against the page", r["fill_page"], r["fill"], r["page"]),
            ("The completed step against the remaining track", r["fill_track"], r["fill"], r["track"]),
            ("The progress bar fill against its track", r["prog_track"], r["prog"], r["track"])]:
        A(f'<tr><td>{name}</td><td>{swatch(fg)}{fg} on {swatch(bg)}{bg}</td>'
          f'<td class="num">{val:.2f}:1</td><td>recorded, not gated</td></tr>')
    A("</table>")
    A('<div class="grid">')
    for title, markup in SPECIMENS:
        A(f'<div class="cell"><div class="cap">Before <span>&mdash; {title}</span></div>'
          f'{frame(r["attr"], r["mode"], markup, before=True, key=r["key"])}</div>')
        A(f'<div class="cell"><div class="cap">After <span>&mdash; {title}</span></div>'
          f'{frame(r["attr"], r["mode"], markup)}</div>')
    A("</div>")

A("<h2>The whole picture in one table</h2>")
A('<table><tr><th>Theme</th><th>Mode</th><th>Step</th><th>Tick</th>'
  '<th class="num">tick vs step</th><th class="num">label vs page</th>'
  '<th class="num">step vs page</th><th class="num">step vs track</th></tr>')
for r in rows:
    A(f'<tr><td>{r["theme"]}</td><td>{r["mlabel"]}</td>'
      f'<td>{swatch(r["fill"])}{r["fill"]}</td><td>{swatch(r["tick"])}{r["tick"]}</td>'
      f'<td class="num {"pass" if r["tick_fill"]>=3 else "fail"}">{r["tick_fill"]:.2f}</td>'
      f'<td class="num {"pass" if r["label_page"]>=4.5 else "fail"}">{r["label_page"]:.2f}</td>'
      f'<td class="num">{r["fill_page"]:.2f}</td>'
      f'<td class="num">{r["fill_track"]:.2f}</td></tr>')
A("</table>")
A("<p>The first two number columns are enforced. The last two are recorded only &mdash; they are the "
  "decoration your rule releases from the contrast requirement. The collapsed bar inside the step "
  "tracker uses the same two colours as the wide form, so its numbers are the &ldquo;step vs "
  "track&rdquo; column exactly.</p>")

A("<h2>What is still open, and what is not mine to settle</h2>")
A("<ul>"
  "<li><strong>Legacy in dark mode: the tick.</strong> Your rule says match the roundels exactly, and "
  "Legacy's roundel tick is white. But Legacy's completed step is also white in dark, so an exact "
  "match would be invisible. The tick has been made dark there instead, on the reasoning that your "
  "own sentence &mdash; the symbol must carry the contrast &mdash; forbids an invisible symbol. "
  "That is a judgement, not your ruling. It is written down as an exception and flagged here.</li>"
  "<li><strong>The name of the new value.</strong> The tick colour needed somewhere to live, so a "
  "new entry was created alongside the step colour. Naming is yours; the name in the files is "
  "marked provisional.</li>"
  "<li><strong>Nothing is committed and nothing is in the decision record.</strong> The files carry "
  "the change and the reasoning, marked as working, awaiting your eye.</li>"
  "</ul>")
A("</div></body></html>")

out = os.path.join(HERE, "STEP-SUCCESS-SYSTEM-2026-08-14-v2.html")
open(out, "w").write("\n".join(P))
print("wrote", out, os.path.getsize(out), "bytes")
