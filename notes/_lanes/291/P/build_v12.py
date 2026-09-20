import io, sys

REPO = "/sessions/fervent-affectionate-carson/mnt/UX-design/"
DECK = REPO + "notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html"
SRC  = REPO + "notes/_lanes/289/illustration/line-workers.html"

src = io.open(SRC, encoding="utf-8").read().split("\n")
# line-workers.html: IIFE opens at line 476 (index 475), probe surface header at
# line 1746 (index 1745). Keep 476..1733 (indices 475..1732) — everything up to
# the lane bootstrap; drop the lane bootstrap (1734..1744) and the lane probe
# surface (1746..2006), which carry linePage / lineGrip / lineClear.
assert src[475].startswith("(function(){"), src[475]
assert src[476].strip() == "var cv = document.getElementById('line');", src[476]
assert src[1711].strip().startswith("/* ---- 9 "), src[1711]
assert src[1733].strip() == "size();", src[1733]
assert src[1745].strip().startswith("/* ---- 10 "), src[1745]
assert src[2006].strip() == "})();", src[2006]

body = src[475:1733]
body[1] = "  var cv = document.getElementById('lw');"

TAIL = u"""  size();
  setView(YAW0, PIT0); render(0);
  /* v12 deck port: draw only while the slide is in view - the gearbox's pattern. */
  if ('IntersectionObserver' in window){
    var ioW = new IntersectionObserver(function(es){
      es.forEach(function(x){ if (x.isIntersecting) start(); else stop(); });
    }, {threshold:0.05});
    var secW = document.getElementById('s4'); if (secW) ioW.observe(secW);
  } else start();
  document.addEventListener('visibilitychange', function(){ if (document.hidden) stop(); });
  window.addEventListener('blur', stop);
  window.addEventListener('focus', function(){ var e=document.getElementById('s4'), r=e&&e.getBoundingClientRect(); if (r && r.bottom>0 && r.top<innerHeight) start(); });

  /* v12 deck port: print - the resting frame, baked to the <img>. */
  function snap(){
    try {
      var was = running; if (was) stop();
      var yo = yawOff, po = pitOff;
      still();
      var out = document.createElement('canvas');
      out.width = cv.width; out.height = cv.height;
      var o = out.getContext('2d');
      o.fillStyle = '#fff'; o.fillRect(0, 0, out.width, out.height);
      o.drawImage(cv, 0, 0);
      var im = document.getElementById('lwPrint');
      if (im) im.src = out.toDataURL('image/png');
      yawOff = yo; pitOff = po; setView(YAW0 + yawOff, PIT0 + pitOff);
      if (was) start(); else if (!reduce) render(frozen === null ? clock : frozen);
    } catch(e){}
  }
  window.addEventListener('beforeprint', snap);
  if (window.matchMedia){
    var mqW = window.matchMedia('print');
    if (mqW.addEventListener) mqW.addEventListener('change', function(e){ if (e.matches) snap(); });
  }
  setTimeout(snap, 1200);
  window.lwSnap = snap;
  var rt = null;
  window.addEventListener('resize', function(){
    clearTimeout(rt);
    rt = setTimeout(function(){ size(); render(frozen === null ? clock : frozen); }, 160);
  });

  /* ---- 10 - the probe surface, NAMESPACED lw* -------------------------
     The lane probes linePage() / lineGrip() / lineClear() are lane
     instrumentation and are NOT ported. What survives is the same shape
     the robots' scene exposes on 5, under lw* so the two line scenes on
     4 and 5 cannot collide. */
  window.lwStats = function(){
    var verts = 0; G.prims.forEach(function(p){ verts += p.v.length; });
    return {primitives:G.prims.length, vertices:verts, faces_drawn:nFace,
            faces_culled:nBack, edges_inked:nEdge, free_lines:PLATE.length + G.axes.length + 1,
            w:W, h:H, dpr:DPR, scale:+SC.toFixed(4),
            draw_box:drawBox.map(function(v){ return +v.toFixed(1); }),
            running:running, reduced:reduce};
  };
  window.lwView = function(){
    return {yaw_deg:+((YAW0+yawOff)/D2R).toFixed(2), pitch_deg:+((PIT0+pitOff)/D2R).toFixed(2),
            workerA_axis_depth:+dot(ARMS[0].axisDir, VD).toFixed(3),
            workerB_axis_depth:+dot(ARMS[1].axisDir, VD).toFixed(3),
            tau:TAU, mouse:[mnx,mny], seen:mouseSeen};
  };
  window.lwPose = function(){
    function A3(a){ return [+(a.abd/D2R).toFixed(1), +(a.t2/D2R).toFixed(1),
                            +((a.tw||0)/D2R).toFixed(1), +(a.t3/D2R).toFixed(1)]; }
    function V(p){ return p.map(function(v){ return +v.toFixed(1); }); }
    function Wk(w){ return {armL:A3(w.ang['-1']), armR:A3(w.ang['1']),
                            handL:V(toLocal(w.Fb, w.hands['-1'])),
                            handR:V(toLocal(w.Fb, w.hands['1'])),
                            footL:V(toLocal(w.Fb, w.feet['-1'])),
                            footR:V(toLocal(w.Fb, w.feet['1']))}; }
    return {A:Wk(POSE.A), B:Wk(POSE.B),
            red_station:+POSE.red_s.toFixed(1),
            belt_top:TOP, stand_off_A:WK_DA, stand_off_B:WK_D,
            station_A:ARM_SA, station_B:ARM_SB,
            figure_height:PEL_Z0 + TOR_LZ + NCK_LZ + HEAD_LZ + HEAD_H,
            head_height:HEAD_H};
  };
  window.lwAxisRuns = function(){
    function L(s){ return +Math.sqrt(Math.pow(s[2]-s[0],2)+Math.pow(s[3]-s[1],2)).toFixed(1); }
    var nm = ['A-STAND','A-SHOULDER','A-ELBOW','B-STAND','B-SHOULDER','B-ELBOW','BELT'];
    return RUNS.map(function(r,i){ return {line:nm[i], open:r.clear.map(L), buried:r.hid.map(L)}; });
  };
  window.lwOrder = function(){ return ORDER; };
  window.lwStill = still;
  window.lwSetTime = function(t){ frozen = t; render(t); };
  window.lwSetMouse = function(x,y){
    mnx = x; mny = y; mouseSeen = true;
    for (var i=0;i<400;i++) updateView(0.016);
    render(frozen === null ? clock : frozen);
  };
  window.lwStop = stop; window.lwStart = start;
})();
"""

HEAD = u"""/* ============================================================
   v12 - 4 - THE LINE SCENE, PEOPLED: TWO WORKERS AND A CONVEYOR.

   Dave, on Sunday: "the line slide - 4. could I have two workers in
   overalls in the place of the robots that are on slide 05. so two
   drawings one with humans and one with robots"; and today, on the v6
   workers drawing: "okay almost, but lets just get it in the slide".

   Lifted from notes/_lanes/289/illustration/line-workers.html (v6),
   unchanged in its geometry, its ink and its resting view. What the
   deck adds is the same three manners every other ported drawing got -
   draw only in view (#s4), the orbit spring that stays where the mouse
   left it, and a snap() that bakes the resting frame into #lwPrint for
   print - and the lane's caption is dropped, because the card carries
   its own type. The lane probes linePage / lineGrip / lineClear are
   instrumentation and are not ported; the rest is namespaced lw* so it
   cannot collide with the robots' line* on 5.
   ============================================================ */
"""

block = HEAD + "\n".join(body) + "\n" + TAIL

deck = io.open(DECK, encoding="utf-8").read().split("\n")

# --- 1 · slide 4 canvas + print img -----------------------------------------
i = deck.index('      <canvas id="gb"></canvas>')
assert deck[i+1] == '      <img id="gbPrint" alt="">'
deck[i]   = '      <canvas id="lw"></canvas>'
deck[i+1] = '      <img id="lwPrint" alt="">'

# --- 2 · print CSS rows ------------------------------------------------------
n = 0
for k, ln in enumerate(deck):
    if "#s4 #gbPrint" in ln:
        deck[k] = ln.replace("#s4 #gbPrint", "#s4 #lwPrint"); n += 1
assert n == 2, n

# --- 3 · the IIFE, inserted before the v10 three-ported-drawings header ------
j = None
for k, ln in enumerate(deck):
    if ln.startswith("   v10 - THE THREE FURTHER PORTED DRAWINGS"):
        j = k - 1
        break
assert j is not None and deck[j].startswith("/* ===="), deck[j]
deck[j:j] = block.split("\n") + [""]

io.open(DECK, "w", encoding="utf-8").write("\n".join(deck))
print("written; deck lines:", len(deck), "block lines:", len(block.split("\n")))
