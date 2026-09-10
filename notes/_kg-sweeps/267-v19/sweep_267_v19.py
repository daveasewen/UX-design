"""#267 lane K — v1.9 sphere sweep. 24 angles x 3 digs, wrong-colour centres + sector-label distance
+ driven rotate-drag + v1.4 stall guard. Run: python3 notes/_kg-sweeps/267-v19/sweep_267_v19.py"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

REPO = "/sessions/friendly-clever-sagan/mnt/UX-design"
PAGE = "file://" + (sys.argv[1] if len(sys.argv)>1 else REPO + "/notes/_KG-EXPLORER.html")
TAG = sys.argv[2] if len(sys.argv)>2 else "v19"
OUT = REPO + "/notes/_kg-sweeps/267-v19"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

SETUP = """(label)=>{
  if(!three) document.getElementById('three').click();
  for(const k in famOn){famOn[k]=1}
  try{recount();renderLegend();renderStats()}catch(e){}
  spin=false; document.getElementById('spin').classList.toggle('on',false);
  const n=NODES.find(x=>x.label===label);
  if(!n) return {ok:false};
  setFocus(n);
  for(const m of NODES){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}
  draw();
  return {ok:true, id:n.id, nb:[...new Set(adj.get(n.id).filter(x=>alive(x.e)&&alive(byId.get(x.other))&&NODEON(byId.get(x.other))&&famOn[FAMILY[x.e.type]]&&famOK(x.e)).map(x=>x.other))].length};
}"""

# wrong-colour centre := the pixel at the node's own DRAWN centre (n._sx,n._sy, i.e. after the v1.9 nudge)
# is nearer in RGB to some other type colour, or to the background, than to its own type colour.
PROBE = """(ry)=>{
  rot.x=0.35; rot.y=ry;
  for(const m of NODES){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}
  draw();
  const g=document.getElementById('cv').getContext('2d');
  const dpr=window.devicePixelRatio||1;
  const hex=s=>{const t=document.createElement('div');t.style.color=s;document.body.appendChild(t);
    const c=getComputedStyle(t).color;t.remove();const m=c.match(/\\d+/g);return [+m[0],+m[1],+m[2]];};
  const pal={}; for(const k in C.t) pal[k]=hex(C.t[k]);
  const bg=hex(C.bg);
  const uniq=[...new Set(adj.get(focus.id).filter(x=>alive(x.e)&&alive(byId.get(x.other))&&NODEON(byId.get(x.other))&&famOn[FAMILY[x.e.type]]&&famOK(x.e)).map(x=>byId.get(x.other)))];
  let wrong=0,total=0,rows=[];
  for(const n of uniq){
    total++;
    let px0=n._sx,py0=n._sy; if(px0==null){const pp=P(n);px0=pp.x;py0=pp.y}
    const px=g.getImageData(Math.round(px0*dpr), Math.round(py0*dpr), 1, 1).data;
    const p=[px[0],px[1],px[2]];
    const d2=(a,b)=>(a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2;
    let best='__bg',bd=d2(p,bg);
    for(const k in pal){const dd=d2(p,pal[k]); if(dd<bd){bd=dd;best=k}}
    if(best!==n.type){wrong++;rows.push([n.label,n.type,best])}
  }
  const [fx,fy,fz]=base(focus);
  let mx=0,labrows=[];
  for(const s of (sectors||[])){
    let q; if(s.dir){q=proj(fx+s.dir[0],fy+s.dir[1],fz+s.dir[2])}
    else if(typeof basis==='function'){const bb=basis();const rr=s.R*1.5*0.8+40,ca=Math.cos(s.mid)*rr,sa=Math.sin(s.mid)*rr;
      q=proj(focus.x+ca*bb.R[0]+sa*bb.U[0],focus.y+ca*bb.R[1]+sa*bb.U[1],focus.z+ca*bb.R[2]+sa*bb.U[2])}
    else continue;
    const g2=[...new Set(adj.get(focus.id).filter(x=>alive(x.e)&&alive(byId.get(x.other))&&NODEON(byId.get(x.other))&&famOn[FAMILY[x.e.type]]&&famOK(x.e)&&x.e.type===s.type).map(x=>byId.get(x.other)))];
    if(!g2.length) continue;
    let sx=0,sy=0,k=0; for(const m of g2){const p=P(m);sx+=p.x;sy+=p.y;k++}
    const d=Math.hypot(q.x-sx/k, q.y-sy/k);
    if(d>mx)mx=d; labrows.push([s.type,Math.round(d)]);
  }
  return {wrong,total,rows,maxlab:Math.round(mx),labrows};
}"""

LABDIST = """()=>{const [fx,fy,fz]=base(focus);let mx=0,rows=[];
  for(const s of (sectors||[])){let q;if(s.dir){q=proj(fx+s.dir[0],fy+s.dir[1],fz+s.dir[2])}
    else if(typeof basis==='function'){const bb=basis();const rr=s.R*1.5*0.8+40,ca=Math.cos(s.mid)*rr,sa=Math.sin(s.mid)*rr;
      q=proj(focus.x+ca*bb.R[0]+sa*bb.U[0],focus.y+ca*bb.R[1]+sa*bb.U[1],focus.z+ca*bb.R[2]+sa*bb.U[2])}else continue;
    const g2=[...new Set(adj.get(focus.id).filter(x=>alive(x.e)&&alive(byId.get(x.other))&&NODEON(byId.get(x.other))&&famOn[FAMILY[x.e.type]]&&famOK(x.e)&&x.e.type===s.type).map(x=>byId.get(x.other)))];
    if(!g2.length)continue;let sx=0,sy=0,k=0;for(const m of g2){const p=P(m);sx+=p.x;sy+=p.y;k++}
    const d=Math.hypot(q.x-sx/k,q.y-sy/k);if(d>mx)mx=d;rows.push([s.type,Math.round(d)])}
  return {max:Math.round(mx),rows,roty:+rot.y.toFixed(3)}}"""

DIGS = ["Pagination", "Button", "2.4.4 Link Purpose (In Context)"]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    errs = []
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto(PAGE)
    pg.wait_for_timeout(2500)
    report = {}

    for label in DIGS:
        s = pg.evaluate(SETUP, label)
        if not s.get("ok"):
            report[label] = {"error": "node not found"}
            print("MISSING", label)
            continue
        pg.wait_for_timeout(300)
        tw = tt = 0; worst = 0; badrows = []; labworst = 0; labdet = []
        for i in range(24):
            r = pg.evaluate(PROBE, i * 6.283185307 / 24)
            tw += r["wrong"]; tt += r["total"]
            if r["maxlab"] > labworst: labworst = r["maxlab"]; labdet = r["labrows"]
            if r["wrong"] > worst: worst = r["wrong"]; badrows = r["rows"]
        report[label] = {"wrong": tw, "total": tt, "neighbours": s["nb"],
                         "worst_angle_wrong": worst, "worst_rows": badrows[:12],
                         "max_sector_label_px": labworst, "label_rows": labdet}
        print(label, tw, "/", tt, "· max sector-label px", labworst, flush=True)

    # driven rotate-drag mid-dig: halo must not go stale (mousemove calls draw() without tick())
    pg.evaluate(SETUP, "Pagination"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{rot.x=0.35;rot.y=0;for(const m of NODES){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}draw()}")
    box = pg.locator("canvas").bounding_box()
    cx0, cy0 = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    pg.mouse.move(cx0, cy0); pg.mouse.down()
    mid = []
    for k in range(1, 15):
        pg.mouse.move(cx0 + k * 18, cy0 + k * 4)
        mid.append(pg.evaluate(LABDIST))
    pg.mouse.up()
    report["drag"] = {"samples": mid, "max_during_drag": max(m["max"] for m in mid)}
    print("drag: max sector-label px during a 14-step rotate-drag =", report["drag"]["max_during_drag"], flush=True)

    # v1.4 stall guard — a node behind the camera / on the camera plane must not throw
    report["stall_guard"] = pg.evaluate("""()=>{try{
      const n=NODES.find(x=>x!==focus);n.x=ctr[0];n.y=ctr[1];n.z=ctr[2]+100000;rot.x=0.35;rot.y=Math.PI;draw();
      const m=NODES.find(x=>x!==focus&&x!==n);m.x=ctr[0];m.y=ctr[1];m.z=ctr[2]+2600;draw();
      const q=NODES.find(x=>x!==focus&&x!==n&&x!==m);q.z=ctr[2]+2601;draw();
      return 'no-throw'}catch(e){return 'THREW: '+e.message}}""")
    print("stall guard:", report["stall_guard"], flush=True)

    # screenshots — Pagination dig, 3 angles, light + dark
    shots = []
    for theme in ("dark", "light"):
        pg.evaluate("(t)=>{document.documentElement.setAttribute('data-theme',t);palette()}", theme)
        pg.evaluate(SETUP, "Pagination"); pg.wait_for_timeout(400)
        for j, ry in enumerate((0.0, 2.094, 4.188)):
            pg.evaluate("(ry)=>{rot.x=0.35;rot.y=ry;for(const m of NODES){m.x=m.tx;m.y=m.ty;m.z=m.tz;m.a=m.ta}draw()}", ry)
            pg.wait_for_timeout(150)
            p = f"{OUT}/pagination-{TAG}-{theme}-a{j+1}.png"
            pg.screenshot(path=p); shots.append(p.split("/notes/")[-1])
    report["screenshots"] = shots
    report["page_errors"] = errs[:20]
    b.close()

with open(OUT + f"/sweep-267-{TAG}.json", "w") as f:
    json.dump(report, f, indent=1)
print("ERRORS:", errs[:5])
