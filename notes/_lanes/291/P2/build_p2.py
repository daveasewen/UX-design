#!/usr/bin/env python3
"""291 / P2 — slide 10 becomes a THREE-UP, and Parts takes the gearbox back.

Provenance. Dave, with a screenshot of a three-up (Parts = the gearbox drawing,
Knowledge = books, Proficiency = brain), said verbatim:

    lets just have these the three on slide 10

Edits v12 IN PLACE. Idempotent only from a fresh copy of
notes/_lanes/291/P2/v12-before-p2.html; every cut asserts on its anchor.
"""
import io, sys, pathlib

P = pathlib.Path('/sessions/fervent-affectionate-carson/mnt/UX-design'
                 '/notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html')
s = P.read_text(encoding='utf-8')
n0 = len(s.splitlines())


def sub(old, new, why):
    global s
    assert s.count(old) == 1, 'anchor %r x%d — %s' % (old[:70], s.count(old), why)
    s = s.replace(old, new, 1)
    print('ok  ', why)


GB = "var cv = document.getElementById('gb');"


def sub_gb(old, new, why):
    """Replace inside the gearbox IIFE: the anchor must be unique AFTER its head."""
    global s
    i = s.index(GB)
    assert s.count(GB) == 1
    tail = s[i:]
    assert tail.count(old) == 1, 'gb anchor %r x%d — %s' % (old[:60], tail.count(old), why)
    s = s[:i] + tail.replace(old, new, 1)
    print('ok  ', why)


# 1 ---- the gearbox gets an off-screen host, the #bkHost pattern (v11/#290).
sub("/* v11: the books likewise - baked for 10, no card of their own now. */\n"
    "#bkHost{position:fixed;left:-3000px;top:0;width:600px;height:420px;pointer-events:none;z-index:-2;}",
    "/* v11: the books likewise - baked for 10, no card of their own now. */\n"
    "#bkHost{position:fixed;left:-3000px;top:0;width:600px;height:420px;pointer-events:none;z-index:-2;}\n"
    "/* v12/P2: and the gearbox - slide 4 is the workers now, but 10's Parts cell\n"
    "   bakes from gbPrint, so the gearbox draws once, off-screen, and stays still. */\n"
    "#gbHost{position:fixed;left:-3000px;top:0;width:600px;height:420px;pointer-events:none;z-index:-2;}",
    'CSS: #gbHost')

sub("  #bkHost{display:none!important}\n",
    "  #bkHost{display:none!important}\n"
    "  #gbHost{display:none!important}\n",
    'print CSS: #gbHost hidden')

sub('<div id="bkHost"><canvas id="bk"></canvas><img id="bkPrint" alt="" style="display:none"></div>\n',
    '<div id="bkHost"><canvas id="bk"></canvas><img id="bkPrint" alt="" style="display:none"></div>\n'
    '<div id="gbHost"><canvas id="gb"></canvas><img id="gbPrint" alt="" style="display:none"></div>\n',
    'markup: #gbHost host div')

# 2 ---- the gearbox IIFE: never animate off-screen, observe its host not #s4.
sub_gb("  function start(){ if (running || reduce || paused) return; running = true; lastT = -1; raf = requestAnimationFrame(loop); }",
    "  function start(){ if (running || reduce || paused || (cv.parentNode && cv.parentNode.id === 'gbHost')) return; /* v12/P2: off-screen, still */ running = true; lastT = -1; raf = requestAnimationFrame(loop); }",
    'gearbox start() fenced on #gbHost')

sub_gb("    var s4 = document.getElementById('s4'); if (s4) io3.observe(s4);   /* v9: the gearbox card is s4 */",
    "    var gbh = document.getElementById('gbHost'); if (gbh) io3.observe(gbh);   /* v12/P2: no card - the host, and start() is fenced */",
    'gearbox IO observes #gbHost')

sub_gb("  window.addEventListener('focus', function(){ var s4=document.getElementById('s4'), r=s4&&s4.getBoundingClientRect(); if (r && r.bottom>0 && r.top<innerHeight) start(); });\n",
    "  window.addEventListener('focus', function(){ var h=document.getElementById('gbHost'); if (h) start(); });   /* v12/P2: start() no-ops off-screen */\n",
    'gearbox focus handler off #s4')

# 3 ---- slide 10: five-up -> three-up.
sub('<h2 class="rv d1"><b>Five things she is made of.</b></h2>',
    '<h2 class="rv d1"><b>Three things she is made of.</b></h2>',
    'slide 10 headline')

sub('''      <div class="rv d3"><img class="pic" id="an4" alt="Line drawing of a robot arm"><p class="ix">04</p><h3>Tools</h3><p>The host agent, in the editor designers already have.</p></div>\n''',
    '', 'slide 10: cell 04 Tools removed')

sub('''      <div class="rv d4"><img class="pic" id="an5" alt="Line drawing of two robots and a conveyor"><p class="ix">05</p><h3>Process</h3><p>Runbooks: how a build is generated, retrieved and reviewed.</p></div>\n''',
    '', 'slide 10: cell 05 Process removed')

sub('''<div class="rv d2"><img class="pic" id="an1" alt="Line drawing of an open parts catalogue on a stand">''',
    '''<div class="rv d2"><img class="pic" id="an1" alt="Line drawing of a gearbox">''',
    'slide 10: 01 Parts alt text = gearbox')

# 4 ---- three equal columns, same gutters and rules.
sub('.grid5{grid-template-columns:repeat(5,1fr)}',
    '.grid5{grid-template-columns:repeat(3,1fr)}   /* v12/P2: three-up */',
    '.grid5 columns -> 3')
sub('#s10 .grid4{grid-template-columns:repeat(5,1fr)}',
    '#s10 .grid4{grid-template-columns:repeat(3,1fr)}   /* v12/P2: three-up */',
    '#s10 .grid4 columns -> 3')
sub('@media(max-width:820px){.grid5{grid-template-columns:1fr 1fr}}',
    '@media(max-width:820px){.grid5{grid-template-columns:1fr}}',
    '.grid5 narrow -> one column (no orphan of three)')

# 5 ---- the anatomy MAP: three cells, 01 Parts back on the gearbox.
sub("""  var MAP = [['an1','ctPrint'], ['an2','bkPrint'], ['an3','brPrint'],   /* v11: 01 Parts = the catalogue */
             ['an4','amPrint'], ['an5','lnPrint']];""",
    """  var MAP = [['an1','gbPrint'], ['an2','bkPrint'], ['an3','brPrint']];
  /* v12/P2: three cells. 01 Parts = the GEARBOX (read from Dave's screenshot;
     v11 had the catalogue here). 04 Tools (amPrint) and 05 Process (lnPrint)
     are gone with their cells. */""",
    'anatomy MAP -> three, 01 = gbPrint')

# 6 ---- the prose in the two headers that says "five".
sub("""/* ---- 10 - the five-up anatomy (v10): .grid4 with five cells and a baked""",
    """/* ---- 10 - the anatomy (v10 five-up, v12/P2 THREE-up): .grid4 with a baked""",
    'CSS header comment')
sub("""   v10 - 10 - THE FIVE-UP ANATOMY.

   Nothing is re-drawn here. Each of the five drawings already bakes its
   own resting frame to a print <img> at load (setTimeout(snap, 1200) in
   every IIFE, the gearbox's pattern). This copies those five baked
   data-URLs into the five small <img>s on 10 once they exist, and the
   .grid5 rule sizes them with mix-blend-mode:multiply so the white card
   ground drops out over the grey card. Polls 400 ms apart, and stops as
   soon as all five have arrived.""",
    """   v10 - 10 - THE ANATOMY. v12/P2: THREE cells, not five.

   Nothing is re-drawn here. Each drawing already bakes its own resting
   frame to a print <img> at load (setTimeout(snap, 1200) in every IIFE,
   the gearbox's pattern). This copies those baked data-URLs into the
   small <img>s on 10 once they exist, and the .grid5 rule sizes them
   with mix-blend-mode:multiply so the white card ground drops out over
   the grey card. Polls 400 ms apart, and stops as soon as all have
   arrived.""",
    'MAP header comment')

sub("<!-- ===== 10 - What she is made of - v10: the FIVE-UP ANATOMY ========= -->",
    "<!-- ===== 10 - What she is made of - v12/P2: the THREE-UP ANATOMY ===== -->",
    'slide 10 html comment')

P.write_text(s, encoding='utf-8')
print('\nlines: %d -> %d' % (n0, len(s.splitlines())))
