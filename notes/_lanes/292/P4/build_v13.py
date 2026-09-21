#!/usr/bin/env python3
"""#292 / P4 — build deck v13 from v12 by inserting ONE slide after slide 10.

Dave, verbatim: "the design system map is good for now as a placeholder, we'll
refine later. we can slot it after slide 10".

v12 is NEVER edited. v13 is `cp`'d from it and this script makes exactly ONE
insertion — a new <section class="slide grey" id="s10map"> plus its own scoped
<style data-lane="P4"> — immediately before the slide-11 comment banner.

Nav is POSITIONAL (`document.querySelectorAll('.slide')` in the chassis IIFE),
so ids are CSS/IIFE handles only: s11 and s12 are NOT renamed, and no other
slide is touched. The new slide's id `s10map` is deliberately outside the
`s<N>` sequence.

Idempotent from a fresh cp; asserts on every anchor it cuts on.

Run:
  cd <repo>
  cp notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html \
     notes/_DEMO-SLIDES-apollo-2026-09-21-v13.html
  python3 notes/_lanes/292/P4/build_v13.py
"""
import io, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
V12 = os.path.join(ROOT, "_DEMO-SLIDES-apollo-2026-09-20-v12.html")
V13 = os.path.join(ROOT, "_DEMO-SLIDES-apollo-2026-09-21-v13.html")

ANCHOR = "<!-- ===== 11 · The ask — v8 s10, the draft stamp kept =================== -->"

# --------------------------------------------------------------------------
# the twelve, in the map's own clockwise order. (title, short line, src|None)
# The lines are CUT SHORTER than lane H's poster: a deck card is read in
# fifteen seconds, and the tile has ~2 lines of room at this size.
# --------------------------------------------------------------------------
TILES = [
    # cls,   edge,    state,  idx,  title,                     line,                                                src / badge
    ("p01", "down",  "have", "01", "Brand Standards",          "Logo masters, marks and colour rules.",              "knowledge/guidelines/brand-principles.md"),
    ("p02", "down",  "soon", "02", "User Research &amp; Insights", "Studies, participants and findings.",             None),
    ("p03", "down",  "have", "03", "Design Patterns",          "Page templates — the shape before the parts.",   "knowledge/components/template-report.meta.json"),
    ("p04", "down",  "have", "04", "Tone of Voice",            "How the product speaks, and what it will not say.",  "knowledge/guidelines/tone-of-voice.md"),
    ("p05", "left",  "have", "05", "Accessibility Standards",  "Contrast, focus, hit area — run as gates.",      "knowledge/_A11Y-GATE.md"),
    ("p06", "left",  "have", "06", "Governance &amp; Operations", "Every ruling inscribed with its receipt.",         "knowledge/_rulings.json"),
    ("p07", "up",    "have", "07", "Data &amp; Insights",      "Instruments that measure the system’s own state.", "knowledge/_INSTRUMENT-FIT.md"),
    ("p08", "up",    "have", "08", "Design Tokens",            "The values every component resolves to.",            "knowledge/canon/canon.css"),
    ("p09", "up",    "have", "09", "Content Guidelines",       "Labels, errors, numbers, dates, calls to action.",   "knowledge/guidelines/copywriting.md"),
    ("p10", "up",    "have", "10", "UX Principles",            "Ratified, each bound to its published evidence.",    "knowledge/_ux_principle_nodes.json"),
    ("p11", "right", "soon", "11", "CX Principles",            "The service-level counterpart, across channels.",    None),
    ("p12", "right", "have", "12", "UX Components",            "Governed components, each with a meta and a build.", "knowledge/components/"),
]

LOCKUP = """      <svg class="lockup" viewBox="0 0 315 85" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Masterbrand lockup">
        <g class="wordmark">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M299.725 60.8888C288.304 60.8888 283.159 53.5583 283.159 42.7359C283.159 32.0127 288.844 23.9949 300.118 23.9949C307.175 23.9949 314.037 27.1429 314.233 35.2094H306.293C305.9 31.668 303.547 29.7984 300.118 29.7984C293.206 29.7984 291.098 37.2759 291.098 42.9815C291.098 48.6394 293.206 55.2309 299.871 55.2309C303.351 55.2309 305.9 53.3622 306.439 49.7709H314.428C313.547 57.8386 307.077 60.8888 299.725 60.8888Z"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M232.501 60.8888C224.855 60.8888 218.582 57.8386 218.435 49.3288H226.13C226.228 53.117 228.433 55.3792 232.649 55.3792C235.786 55.3792 239.315 53.8047 239.315 50.2625C239.315 47.5088 236.914 46.6233 232.942 45.4914L230.394 44.7537C224.808 43.1306 219.268 40.965 219.268 34.5704C219.268 26.6504 226.621 23.9949 233.335 23.9949C240.245 23.9949 246.176 26.4053 246.225 34.2757H238.531C238.236 31.029 236.374 29.1594 232.746 29.1594C229.904 29.1594 227.062 30.6843 227.062 33.8323C227.062 36.44 229.414 37.2272 234.413 38.8012L237.354 39.7362C243.432 41.6544 247.254 43.7688 247.254 49.673C247.254 57.7886 239.461 60.8888 232.501 60.8888Z"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M264.675 54.9364C268.252 54.9364 271.782 54.0996 271.782 49.771C271.782 45.5403 268.743 44.5557 265.115 44.5557H259.039V54.9364H264.675ZM263.94 39.489C267.322 39.489 270.751 38.8013 270.751 34.6684C270.751 30.9801 267.517 29.9951 264.43 29.9951H259.039V39.489H263.94ZM251.588 24.6832H263.89C267.763 24.6832 269.331 24.7819 270.85 25.1253C275.163 26.109 278.398 28.9127 278.398 33.6855C278.398 38.2597 275.507 40.6205 271.34 41.7037C276.143 42.5892 279.672 45.0495 279.672 50.3122C279.672 58.3795 271.732 60.2491 265.508 60.2491H251.588V24.6832Z"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M206.382 45.0489H191.041V60.2494H183.346V24.6826H191.041V39.2437H206.382V24.6826H214.076V60.2494H206.382V45.0489Z"/>
        </g>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M42.5 85H127.5V0H42.5V85Z" fill="#FFFFFF"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M42.5 8.58307e-05L85 42.5L127.5 8.58307e-05H42.5Z" fill="#DB0011"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M42.5 85H127.5L85 42.5L42.5 85Z" fill="#DB0011"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M127.5 85L170 42.5L127.5 0V85Z" fill="#DB0011"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M0 42.5L42.3107 84.9311L42.5 85V0L0 42.5Z" fill="#DB0011"/>
      </svg>"""


def tile_html(cls, edge, state, idx, title, line, src):
    foot = ('<p class="src">%s</p>' % src) if src else '<p class="badge">Coming soon</p>'
    return (
        '      <article class="tile %s" data-edge="%s" data-state="%s">\n'
        '        <div class="ink-block">\n'
        '          <p class="idx">%s</p>\n'
        '          <h3>%s</h3>\n'
        '          <p class="d">%s</p>\n'
        '        </div>\n'
        '        <div class="tfoot">%s</div>\n'
        '        <span class="tick"></span>\n'
        '      </article>\n' % (cls, edge, state, idx, title, line, foot)
    )


SECTION = """<!-- ===== 10A · The design system map — #292 lane H, inlined ==============
     Dave, verbatim: "the design system map is good for now as a placeholder,
     we'll refine later. we can slot it after slide 10".

     Lane H's poster (notes/_lanes/292/H/design-system-map.html) re-cut for a
     720/900-high card: the 4x4 frame, the twelve on the perimeter, the hub in
     the middle 2x2, the hairline grid made of the grid's own 1px gaps, and the
     inward tick on each tile. What is dropped is the poster's masthead (the
     card carries its own eyebrow and headline), its key panel and its footer
     (folded into one .foot line), and each tile's description is CUT SHORTER.
     Nothing is an image: the map is markup and scoped CSS, so it scales with
     the card and prints as type, not as a screenshot.

     The id is s10map, NOT s11: the chassis navigates positionally
     (querySelectorAll('.slide')), so the existing s1..s12 ids are untouched
     and this one is kept out of their sequence. The pagenum reads 10A / 12 for
     the same reason — no other card's counter is disturbed. ============== -->
<section class="slide grey" id="s10map">
  <div class="inner">
    <p class="label rv">The design system</p>
    <h2 class="rv d1"><b>Twelve around one.</b></h2>

    <section class="dsm rv d2" aria-label="Twelve parts of a design system around one core">
%(tiles)s
      <div class="hub">
%(lockup)s
        <div class="accent-rule" role="presentation"></div>
        <p class="hubh">Intelligent Design System</p>
        <p class="strap">One governed source. Every surface, component and token resolves back to&nbsp;it.</p>
        <div class="ring">
          <span>People</span><span>Technology</span><span>Data</span><span>Insights</span><span>Governance</span><span>Continuous improvement</span>
        </div>
      </div>
    </section>

    <p class="foot rv d3">Ten of the twelve stand in the repository today, each citing one file it is held in. Two are faded and badged &mdash; absent is a state of the map, not a hole in it. Placeholder: not yet ruled.</p>
  </div>
  <div class="pagenum">10A / 12</div>
</section>

<style data-lane="P4">
/* ============================================================
   10A · THE DESIGN SYSTEM MAP — every rule scoped to #s10map, so nothing
   here can reach another card. Lane H's tokens are re-declared LOCALLY on
   the section (canon values, same citations) rather than imported, and the
   type is the deck's own --font, not the poster's --uf: the card belongs to
   the deck first.

   The frame fills whatever height the card has left — rows are
   minmax(0,1fr) inside a flex column — so the map can never push past the
   slide box. Tile copy is sized to fit that row at 900 high.
   ============================================================ */
#s10map{padding:var(--s5) max(var(--s6),6vw);justify-content:stretch;}
#s10map .inner{display:flex;flex-direction:column;flex:1 1 auto;min-height:0;}
#s10map h2{font-size:clamp(28px,3.4vw,42px);margin:0 0 var(--s3);}
#s10map .foot{margin-top:var(--s2);padding-top:10px;font-size:11.5px;line-height:1.55;}

/* --- local roles; canon values, cited as lane H cites them --- */
#s10map .dsm{
  --dsm-rule:var(--g3);            /* canon.css:17 grey-300 */
  --dsm-surface:var(--white);
  --dsm-ink:var(--black);
  --dsm-ink-2:var(--g8);           /* canon.css:22 grey-800 */
  --dsm-ink-3:var(--g6);           /* canon.css:20 grey-600 — min safe for text */
  --dsm-mute:var(--g5);            /* canon.css:19 grey-500 */
  --dsm-band:var(--g1);            /* canon.css:15 grey-100 */
  --dsm-brand:#DB0011;             /* the hexagon's own red: BRAND, not accent */
  flex:1 1 auto;min-height:0;
  display:grid;
  grid-template-columns:repeat(4,minmax(0,1fr));
  grid-template-rows:repeat(4,minmax(0,1fr));
  gap:1px;
  background:var(--dsm-rule);
  border:1px solid var(--dsm-rule);
}
/* if the card is ever put on a dark ground, the map follows it */
#s10map.dark .dsm{--dsm-rule:var(--g7);--dsm-surface:#1D1D1D;--dsm-ink:var(--white);
  --dsm-ink-2:#B7B7B7;--dsm-ink-3:#B7B7B7;--dsm-mute:#8A8A8A;--dsm-band:#171717;}
#s10map .dsm > *{background:var(--dsm-surface);position:relative;min-width:0;min-height:0;}

/* clockwise from top-left: 01..12; centre 2x2 is the hub */
#s10map .p01{grid-area:1/1} #s10map .p02{grid-area:1/2} #s10map .p03{grid-area:1/3} #s10map .p04{grid-area:1/4}
#s10map .p05{grid-area:2/4} #s10map .p06{grid-area:3/4}
#s10map .p07{grid-area:4/4} #s10map .p08{grid-area:4/3} #s10map .p09{grid-area:4/2} #s10map .p10{grid-area:4/1}
#s10map .p11{grid-area:3/1} #s10map .p12{grid-area:2/1}
#s10map .hub{grid-area:2/2 / 4 / 4}

/* --- a tile --- */
#s10map .tile{padding:13px 15px;display:flex;flex-direction:column;}
#s10map .tile .idx{margin:0 0 5px;font-size:9.5px;letter-spacing:.14em;color:var(--dsm-mute);}
#s10map .tile h3{margin:0;font-size:15px;line-height:1.24;font-weight:500;letter-spacing:0;color:var(--dsm-ink);}
#s10map .tile .d{margin:5px 0 0;font-size:11.5px;line-height:1.36;font-weight:400;color:var(--dsm-ink-2);}
#s10map .tile .tfoot{margin-top:auto;padding-top:8px;}
#s10map .tile .src{margin:0;font-size:8.5px;line-height:1.35;letter-spacing:0;color:var(--dsm-ink-3);
  word-break:break-all;font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}
#s10map .tile .src::before{content:"";display:block;width:14px;height:1px;background:var(--dsm-rule);margin-bottom:5px;}
#s10map .badge{display:inline-block;margin:0;padding:2px 6px;font-size:8.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--dsm-ink-2);border:1px solid var(--dsm-rule);background:var(--dsm-surface);
  font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}

/* the inward tick — a stem, not an arrowhead; it gets its own margin so it
   never crosses a line of type */
#s10map .tick{position:absolute;background:var(--dsm-ink);}
#s10map [data-edge="down"]  .tick{left:50%%;bottom:0;width:1px;height:16px;}
#s10map [data-edge="up"]    .tick{left:50%%;top:0;width:1px;height:16px;}
#s10map [data-edge="left"]  .tick{top:50%%;left:0;height:1px;width:16px;}
#s10map [data-edge="right"] .tick{top:50%%;right:0;height:1px;width:16px;}
#s10map [data-edge="down"] {padding-bottom:22px;}
#s10map [data-edge="up"]   {padding-top:22px;}
#s10map [data-edge="left"] {padding-left:22px;}
#s10map [data-edge="right"]{padding-right:22px;}

/* absent: reduced ink, not removed */
#s10map .tile[data-state="soon"]{background:var(--dsm-band);}
#s10map .tile[data-state="soon"] .ink-block{opacity:.45;}
#s10map .tile[data-state="soon"] .tick{background:var(--dsm-mute);}

/* --- the hub --- */
#s10map .hub{display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:18px 22px;text-align:center;}
#s10map .lockup{width:clamp(108px,11vw,150px);height:auto;display:block;}
#s10map .lockup .wordmark{fill:var(--dsm-ink);}
#s10map .hub .accent-rule{width:56px;height:2px;background:var(--accent);margin:14px 0;}
#s10map .hub .hubh{margin:0;font-size:clamp(16px,1.5vw,20px);line-height:1.25;font-weight:300;color:var(--dsm-ink);}
#s10map .hub .strap{margin:8px 0 0;font-size:12px;line-height:1.42;color:var(--dsm-ink-2);max-width:40ch;}
#s10map .ring{margin-top:14px;padding-top:8px;border-top:1px solid var(--dsm-rule);
  width:100%%;display:flex;flex-wrap:nowrap;justify-content:center;white-space:nowrap;
  font-size:8px;letter-spacing:.10em;text-transform:uppercase;color:var(--dsm-ink-3);
  font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}
#s10map .ring span{padding:0 7px;border-right:1px solid var(--dsm-rule);line-height:1.5;}
#s10map .ring span:last-child{border-right:0;}

/* print: the card is 1280x720, ~180px shorter in content than the screen
   card, so the tile line stands down and the numeral + name + citation carry
   the tile. Declared, not silent. */
@media print{
  #s10map{padding:40px 72px;}
  #s10map h2{font-size:30px;margin:0 0 16px;}
  #s10map .tile .d{display:none;}
  #s10map .tile h3{font-size:14px;}
  #s10map .foot{margin-top:12px;font-size:10.5px;}
  #s10map .hub .strap{font-size:11px;}
}
</style>

"""


def main():
    if not os.path.exists(V13):
        sys.exit("v13 missing — cp it from v12 first: %s" % V13)
    src = io.open(V13, encoding="utf-8").read()

    assert "id=\"s10map\"" not in src, "already built — re-cp from v12 first"
    assert src.count(ANCHOR) == 1, "slide-11 anchor not unique (%d)" % src.count(ANCHOR)
    # 13 = twelve real sections + the one quoted inside the head comment (line 20)
    assert src.count('<section class="slide') == 13, "expected 12 real + 1 quoted"
    assert src.count('id="s11"') == 1 and src.count('id="s12"') >= 1

    tiles = "".join(tile_html(*t) for t in TILES)
    block = SECTION % {"tiles": tiles, "lockup": LOCKUP}

    out = src.replace(ANCHOR, block + ANCHOR, 1)

    assert out.count('<section class="slide') == 14
    assert out.count('id="s10map"') == 1
    assert out.count('id="s11"') == 1                      # NOT renamed
    assert out.count('class="tile ') == 12
    io.open(V13, "w", encoding="utf-8").write(out)
    print("built %s: +%d lines, 13 slide sections" %
          (os.path.basename(V13), out.count("\n") - src.count("\n")))


if __name__ == "__main__":
    main()
