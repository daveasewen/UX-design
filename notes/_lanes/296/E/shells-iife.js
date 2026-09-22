/* ---- §7 · the shells graph (#296 lane E) ------------------------------
   Dave: "add another one of our 3d illustrations that has a representation
   of a knowledge graph the shells construction is probably best it can be a
   simplfied version, not the full thing, to replace the brain".
   The explorer's three layers as three concentric shells (graph-layers-are-
   shells-280): the system at the core, the obligations in the middle, the
   reasons outside. Each shell is a construction sphere: its outline, its
   equator and one meridian; the half of every ring, node and edge that lies
   behind the picture plane through the centre is the hidden run, dashed in
   the deck's hidden grey, exactly as the books and the gearbox dash theirs.
   26 nodes, 26 edges (e2: 5 / 9 / 12); one chain (core -> middle -> outer) and its end node
   carry the one accent red. Same camera as the books and the gearbox
   (YAW0 -35 / PIT0 20, YAW_R 25 / PIT_R 12, TAU 1.0), same setView, same
   orthographic projection, same plate idiom, same ink weights. */
(function(){
  var cv = document.getElementById('shl');
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var INK = '#111', HIDC = '#BDBDBD', CONC = '#9B9B9B', RED = '#DA1A00';
  var D2R = Math.PI/180;

  /* ---- 1 · the shells, the nodes, the edges ------------------------- */
  var RS = [44, 90, 138];                 /* core, middle, outer radius   */
  function onShell(k, lat, lon){
    var r = RS[k], p = lat*D2R, t = lon*D2R;
    return [r*Math.cos(p)*Math.cos(t), r*Math.cos(p)*Math.sin(t), r*Math.sin(p)];   /* [a,u,b] */
  }
  var NODES = [
    [0, 14, 20], [0,-28,150], [0, 48,235], [0,-38,320], [0, 30,110],                                  /* core   0-4   */
    [1, 22, 88], [1,-16, 12], [1, 42,140], [1,-20,110], [1,  8,212], [1, 30,300], [1,-22, 50],
    [1, 58,215], [1, 18,165],                                                                         /* middle 5-13  */
    [2, 30,122], [2, -4, 78], [2, 56,  2], [2,-16,-24], [2, 16,164], [2, 20,250], [2, 44,305],
    [2,-30,120], [2, 65,190], [2, -8,340], [2, 38,200], [2,-40, 30]                                   /* outer 14-25  */
  ].map(function(n){ return {k:n[0], p:onShell(n[0], n[1], n[2])}; });
  var EDGES = [
    [0,3],[1,2],                                                   /* within the core      */
    [0,5,1],[0,6],[1,8],[2,7],[3,10],[2,9],[4,13],[4,11],          /* core -> middle       */
    [6,5],[7,9],[12,7],[11,6],                                     /* within the middle    */
    [5,14,1],[6,16],[6,17],[8,15],[7,18],[9,19],[10,20],[8,21],
    [12,22],[10,23],[11,24],[11,25]                                /* middle -> outer      */
  ];
  var RED_NODE = 14;

  /* each shell: the equator, and one meridian at its own azimuth */
  var RINGS = [], NSEG = 120;
  function ring(k, kind, az){
    var pts = [], i, t, r = RS[k];
    for (i=0;i<=NSEG;i++){
      t = i/NSEG*2*Math.PI;
      if (kind === 'eq') pts.push([r*Math.cos(t), r*Math.sin(t), 0]);
      else pts.push([r*Math.cos(t)*Math.cos(az*D2R), r*Math.cos(t)*Math.sin(az*D2R), r*Math.sin(t)]);
    }
    RINGS.push(pts);
  }
  ring(0,'eq'); ring(1,'eq'); ring(2,'eq');
  ring(0,'mer',-10); ring(1,'mer',-10); ring(2,'mer',-10);

  /* ---- 2 · the plate and the construction lines --------------------- */
  var BASE_T = -RS[2] - 14, BASE_B = BASE_T - 12;
  var PA = RS[2] + 22, PU = RS[2] + 22;
  function boxEdges(a0,a1,u0,u1,b0,b1){
    var V = [[a0,u0,b0],[a1,u0,b0],[a1,u1,b0],[a0,u1,b0],
             [a0,u0,b1],[a1,u0,b1],[a1,u1,b1],[a0,u1,b1]];
    var E = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
    return E.map(function(e){ return [V[e[0]], V[e[1]]]; });   /* [a,u,b] */
  }
  var PLATE = boxEdges(-PA, PA, -PU, PU, BASE_B, BASE_T);
  var AXES = [
    [[0,0,BASE_B-18],[0,0,RS[2]+34]],                          /* the vertical axis */
    [[-PA-16,0,BASE_T],[PA+16,0,BASE_T]],                      /* ground cross      */
    [[0,-PU-16,BASE_T],[0,PU+16,BASE_T]]
  ];

  /* ---- 3 · the camera: the books' and the gearbox's, verbatim ------- */
  var YAW0 = -35*Math.PI/180, PIT0 = 20*Math.PI/180;
  var YAW_R = 25*Math.PI/180, PIT_R = 12*Math.PI/180;
  var TAU = 1.0;
  var m00=1,m02=0,m10=0,m11=1,m12=0,m20=0,m21=0,m22=1;
  function setView(yaw, pit){
    var cy=Math.cos(yaw), sy=Math.sin(yaw), cp=Math.cos(pit), sp=Math.sin(pit);
    m00=cy;      m02=sy;
    m10=sp*sy;   m11=cp;   m12=-sp*cy;
    m20=-cp*sy;  m21=sp;   m22=cp*cy;
  }
  function springStep(x,v,target,w,dt){ var a=-2*w*v-w*w*(x-target); v+=a*dt; x+=v*dt; return [x,v]; }
  var mnx=0,mny=0,mouseSeen=false,yawOff=0,yawVel=0,pitOff=0,pitVel=0;
  function onMove(e){
    if (e.pointerType && e.pointerType !== 'mouse') return;
    var w = window.innerWidth||1, h = window.innerHeight||1;
    mnx=(e.clientX-w/2)/(w/2); mny=(e.clientY-h/2)/(h/2);
    if (mnx<-1) mnx=-1; else if (mnx>1) mnx=1;
    if (mny<-1) mny=-1; else if (mny>1) mny=1;
    mouseSeen=true;
  }
  window.addEventListener('pointermove', onMove, {passive:true});
  function updateView(dt){
    var tY = mouseSeen ?  mnx*YAW_R : 0, tP = mouseSeen ? -mny*PIT_R : 0;
    var w=1/TAU, left=dt, h, A, B;
    while (left>1e-5){
      h = left>0.008?0.008:left; left-=h;
      A=springStep(yawOff,yawVel,tY,w,h); yawOff=A[0]; yawVel=A[1];
      B=springStep(pitOff,pitVel,tP,w,h); pitOff=B[0]; pitVel=B[1];
    }
    setView(YAW0+yawOff, PIT0+pitOff);
  }

  /* ---- 4 · the fit (the brain's slot, the brain's pads and K) ------- */
  var W=800,H=600,DPR=1,SC=1,OX=0,OY=0,PAD_X=72,PAD_Y=40,BOXU=null;
  function everyVertex(cb){
    RINGS.forEach(function(r){ r.forEach(function(p){ cb(p[0],p[1],p[2]); }); });
    /* the outline of each shell is a circle of radius r on screen: its
       extremes are the shell's own extremes on every axis */
    RS.forEach(function(r){ cb(0,0,r); cb(0,0,-r); });
    PLATE.forEach(function(s){ s.forEach(function(v){ cb(v[0],v[1],v[2]); }); });
    AXES.forEach(function(s){ s.forEach(function(v){ cb(v[0],v[1],v[2]); }); });
  }
  function sweepBox(){
    var lo=[1e9,1e9], hi=[-1e9,-1e9], rlo=[1e9,1e9], rhi=[-1e9,-1e9];
    var saved=[m00,m02,m10,m11,m12,m20,m21,m22], i, j;
    function acc(L,Hh){ return function(a,u,b){
      var sx=m00*a+m02*u, sy=m10*a+m11*b+m12*u;
      if (sx<L[0]) L[0]=sx; if (sx>Hh[0]) Hh[0]=sx;
      if (sy<L[1]) L[1]=sy; if (sy>Hh[1]) Hh[1]=sy;
    };}
    for (i=-1;i<=1;i++) for (j=-1;j<=1;j++){
      setView(YAW0+i*YAW_R, PIT0+j*PIT_R); everyVertex(acc(lo,hi));
      if (i===0 && j===0) everyVertex(acc(rlo,rhi));
    }
    /* the outlines: +-r about the centre, both ways, in any view */
    RS.forEach(function(r){ for (var q=0;q<2;q++){ lo[q]=Math.min(lo[q],-r); hi[q]=Math.max(hi[q],r); rlo[q]=Math.min(rlo[q],-r); rhi[q]=Math.max(rhi[q],r); } });
    m00=saved[0];m02=saved[1];m10=saved[2];m11=saved[3];m12=saved[4];
    m20=saved[5];m21=saved[6];m22=saved[7];
    return {lo:lo,hi:hi,rlo:rlo,rhi:rhi};
  }
  function size(){
    var host=cv.parentNode;
    W=Math.max(240, host.clientWidth||800); H=Math.max(200, host.clientHeight||600);
    DPR=Math.min(2, window.devicePixelRatio||1);
    cv.width=Math.round(W*DPR); cv.height=Math.round(H*DPR);
    cv.style.width=W+'px'; cv.style.height=H+'px';
    ctx.setTransform(DPR,0,0,DPR,0,0);
    PAD_X=Math.min(72,W*0.07); PAD_Y=Math.min(40,H*0.06);
    if (!BOXU) BOXU=sweepBox();
    var K=0.42;
    var rw=BOXU.rhi[0]-BOXU.rlo[0], rh=BOXU.rhi[1]-BOXU.rlo[1];
    var bw=rw+K*((BOXU.hi[0]-BOXU.lo[0])-rw), bh=rh+K*((BOXU.hi[1]-BOXU.lo[1])-rh);
    SC=Math.min((W-2*PAD_X)/bw,(H-2*PAD_Y)/bh)*0.98;
    OX=W/2-(BOXU.rlo[0]+BOXU.rhi[0])/2*SC;
    OY=H/2+(BOXU.rlo[1]+BOXU.rhi[1])/2*SC;
  }

  /* ---- 5 · the ink -------------------------------------------------- */
  function px(a,u,b){ return OX+(m00*a+m02*u)*SC; }
  function py(a,u,b){ return OY-(m10*a+m11*b+m12*u)*SC; }
  function dep(p){ return m20*p[0]+m21*p[2]+m22*p[1]; }     /* + toward the eye */
  function lerp(p,q,t){ return [p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t, p[2]+(q[2]-p[2])*t]; }
  function seg2(p,q){ return [px(p[0],p[1],p[2]),py(p[0],p[1],p[2]),px(q[0],q[1],q[2]),py(q[0],q[1],q[2])]; }
  /* split one 3D segment at the picture plane through the centre */
  function split(p, q, front, back){
    var d0=dep(p), d1=dep(q);
    if (d0>=0 && d1>=0){ front.push(seg2(p,q)); return; }
    if (d0<0 && d1<0){ back.push(seg2(p,q)); return; }
    var m=lerp(p,q,d0/(d0-d1));
    if (d0>=0){ front.push(seg2(p,m)); back.push(seg2(m,q)); }
    else { back.push(seg2(p,m)); front.push(seg2(m,q)); }
  }
  function strokeSegs(arr, col, dash, w){
    if (!arr.length) return;
    ctx.beginPath();
    for (var i=0;i<arr.length;i++){ ctx.moveTo(arr[i][0],arr[i][1]); ctx.lineTo(arr[i][2],arr[i][3]); }
    ctx.strokeStyle=col; ctx.lineWidth=w; ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
  }
  var drawBox=[0,0,0,0], LAST={};
  function render(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
    ctx.lineCap='round'; ctx.lineJoin='round';
    var ringF=[], ringB=[], edgeF=[], edgeB=[], redF=[], redB=[], plate=[], axes=[];
    RINGS.forEach(function(r){ for (var i=0;i<r.length-1;i++) split(r[i], r[i+1], ringF, ringB); });
    EDGES.forEach(function(e){
      if (e[2]) split(NODES[e[0]].p, NODES[e[1]].p, redF, redB);
      else split(NODES[e[0]].p, NODES[e[1]].p, edgeF, edgeB);
    });
    PLATE.forEach(function(s){ plate.push(seg2(s[0],s[1])); });
    AXES.forEach(function(s){ axes.push(seg2(s[0],s[1])); });

    /* 1 · the hidden runs, laid down first */
    strokeSegs(ringB, HIDC, [5,4], 1);
    strokeSegs(edgeB.concat(redB), HIDC, [5,4], 1);
    /* 2 · the construction and the plate */
    strokeSegs(axes, CONC, [9,3,2,3], 1);
    strokeSegs(plate, INK, [], 1);
    /* 3 · the shells' outlines — each shell's silhouette is a circle */
    var cx=px(0,0,0), cy=py(0,0,0);
    ctx.beginPath();
    RS.forEach(function(r){ ctx.moveTo(cx+r*SC, cy); ctx.arc(cx, cy, r*SC, 0, 2*Math.PI); });
    ctx.strokeStyle=INK; ctx.lineWidth=1; ctx.setLineDash([]); ctx.stroke();
    /* 4 · the visible rings and edges, the accent last */
    strokeSegs(ringF, INK, [], 1);
    strokeSegs(edgeF, INK, [], 1);
    strokeSegs(redF, RED, [], 1.4);
    /* 5 · the nodes, back to front: white-filled so the lines stop at them */
    var NR = Math.max(2.6, Math.min(4.2, 3.0*SC));
    var order = NODES.map(function(n,i){ return {i:i, d:dep(n.p)}; }).sort(function(x,y){ return x.d-y.d; });
    var nFront=0, nBack=0;
    order.forEach(function(o){
      var n=NODES[o.i], x=px(n.p[0],n.p[1],n.p[2]), y=py(n.p[0],n.p[1],n.p[2]);
      ctx.beginPath(); ctx.arc(x, y, o.i===RED_NODE ? NR+0.6 : NR, 0, 2*Math.PI);
      if (o.i===RED_NODE){ ctx.fillStyle=RED; ctx.fill(); ctx.strokeStyle=RED; ctx.lineWidth=1.4; }
      else { ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle = o.d>=0 ? INK : HIDC; ctx.lineWidth=1; }
      ctx.stroke();
      if (o.d>=0) nFront++; else nBack++;
    });
    drawBox=[1e9,1e9,-1e9,-1e9];
    function hit(x,y){ if(x<drawBox[0])drawBox[0]=x; if(x>drawBox[2])drawBox[2]=x; if(y<drawBox[1])drawBox[1]=y; if(y>drawBox[3])drawBox[3]=y; }
    [ringF,ringB,edgeF,edgeB,plate,axes].forEach(function(g){ g.forEach(function(s){ hit(s[0],s[1]); hit(s[2],s[3]); }); });
    RS.forEach(function(r){ hit(cx-r*SC,cy-r*SC); hit(cx+r*SC,cy+r*SC); });
    LAST={nFront:nFront, nBack:nBack, redEdgeSegs:redF.length, redEdgeHidden:redB.length, nodeR:NR};
  }

  /* ---- 6 · the frame, the observer, the print ----------------------- */
  var lastT=-1, raf=null, running=false;
  function frame(now){
    if (lastT<0) lastT=now;
    var dt=(now-lastT)/1000; lastT=now;
    if (dt<0) dt=0; if (dt>0.1) dt=0.1;
    updateView(dt); render();
  }
  size(); setView(YAW0,PIT0); render();
  var _min=1000/30, _last=0;
  function loop(now){ if (now-_last>=_min-1){ _last=now; frame(now); } raf=requestAnimationFrame(loop); }
  function start(){ if (running||reduce) return; running=true; lastT=-1; raf=requestAnimationFrame(loop); }
  function stop(){ running=false; if (raf) cancelAnimationFrame(raf); raf=null; }
  function still(){ yawOff = pitOff = 0; yawVel = pitVel = 0; setView(YAW0, PIT0); render(); }
  if ('IntersectionObserver' in window){
    var ioS = new IntersectionObserver(function(es){
      es.forEach(function(x){ if (x.isIntersecting) start(); else stop(); });
    }, {threshold:0.05});
    var sEl = document.getElementById('s7'); if (sEl) ioS.observe(sEl);
  } else start();
  document.addEventListener('visibilitychange', function(){ if (document.hidden) stop(); });
  window.addEventListener('blur', stop);
  window.addEventListener('focus', function(){ var e=document.getElementById('s7'), r=e&&e.getBoundingClientRect(); if (r && r.bottom>0 && r.top<innerHeight) start(); });
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
      var im = document.getElementById('shlPrint');
      if (im) im.src = out.toDataURL('image/png');
      yawOff = yo; pitOff = po; setView(YAW0 + yawOff, PIT0 + pitOff);
      if (was) start(); else if (!reduce) render();
    } catch(e){}
  }
  window.addEventListener('beforeprint', snap);
  if (window.matchMedia){
    var mqS = window.matchMedia('print');
    if (mqS.addEventListener) mqS.addEventListener('change', function(e){ if (e.matches) snap(); });
  }
  setTimeout(snap, 1200);
  window.shlSnap = snap;
  var rt=null;
  window.addEventListener('resize', function(){ clearTimeout(rt); rt=setTimeout(function(){ BOXU=null; size(); render(); },160); });
  window.shlSet = function(yawDeg, pitDeg){
    stop(); mouseSeen=false; yawVel=pitVel=0;
    yawOff=(yawDeg||0)*Math.PI/180; pitOff=(pitDeg||0)*Math.PI/180;
    setView(YAW0+yawOff, PIT0+pitOff); render();
  };
  window.shlState = function(){
    return {yaw0:YAW0/D2R, pit0:PIT0/D2R, yawR:YAW_R/D2R, pitR:PIT_R/D2R, radii:RS.slice(),
            nodes:NODES.length, edges:EDGES.length, redEdges:EDGES.filter(function(e){return e[2];}).length,
            rings:RINGS.length, outlines:RS.length, plate:[2*PA,2*PU,BASE_T-BASE_B],
            SC:SC, W:W, H:H, drawBox:drawBox.slice(), last:LAST};
  };
  window.shlReady = true;
})();
