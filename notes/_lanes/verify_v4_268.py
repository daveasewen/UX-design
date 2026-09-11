#!/usr/bin/env python3
"""#268 — verification harness for notes/_DEMO-SLIDES-apollo-2026-09-11-v4.html."""
import glob, json, os, sys, pathlib
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
PAGE = REPO / "notes" / "_DEMO-SLIDES-apollo-2026-09-11-v4.html"
OUT  = REPO / "notes" / "_subreports" / "slides-268-v4"
OUT.mkdir(parents=True, exist_ok=True)

PB = os.environ["PLAYWRIGHT_BROWSERS_PATH"]
exe = (sorted(glob.glob(os.path.join(PB, "chromium*", "chrome-linux", "*", "chrome")))
       or sorted(glob.glob(os.path.join(PB, "chromium*", "chrome-linux", "chrome")))
       or sorted(glob.glob(os.path.join(PB, "chromium*", "chrome-linux", "headless_shell"))))
EXE = exe[0]
R = {}

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox", "--disable-dev-shm-usage",
                                                       "--enable-gpu-rasterization", "--force-device-scale-factor=1"])
    pg = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
    pg.goto(PAGE.as_uri()); pg.wait_for_timeout(2500)
    R["pageerrors"] = errs

    R["stats"] = pg.evaluate("window.skyStats()")

    # --- canvas lit + no-void grid, over 18 phases of the 90 s revolution
    probe = pg.evaluate("""() => {
      const out=[]; const cv=document.getElementById('sky');
      const c=document.createElement('canvas'); c.width=cv.width; c.height=cv.height;
      const g=c.getContext('2d');
      for(let i=0;i<18;i++){
        const t=i*90000/18; window.skyFrame(t);
        const v=window.skyVoidCheck(12,7);
        g.clearRect(0,0,c.width,c.height); g.drawImage(cv,0,0);
        // per-cell max luminance of the RIGHT half (away from the vignette+type)
        let lit=0, cellmin=1e9;
        for(let r=0;r<7;r++) for(let col=0;col<12;col++){
          const x=Math.floor(col*c.width/12), y=Math.floor(r*c.height/7);
          const w=Math.floor(c.width/12), h=Math.floor(c.height/7);
          const d=g.getImageData(x,y,w,h).data; let mx=0,sum=0;
          for(let k=0;k<d.length;k+=16){const L=(d[k]*2+d[k+1]*5+d[k+2])/8; if(L>mx)mx=L; sum+=L;}
          if(mx>lit) lit=mx; if(mx<cellmin) cellmin=mx;
        }
        out.push({phase:i, min:v.min, max:v.max, maxLum:Math.round(lit), minCellPeakLum:Math.round(cellmin)});
      }
      return out;
    }""")
    R["phases18"] = probe
    R["void_min_over_18"] = min(p["min"] for p in probe)
    R["cellpeak_min_over_18"] = min(p["minCellPeakLum"] for p in probe)

    # --- wordmark unobstructed: mean luminance of the canvas region behind the
    #     type block, measured through the vignette, over the same 18 phases
    R["wordmark_backdrop"] = pg.evaluate("""() => {
      const wm=document.querySelector('#s1 .wordmark').getBoundingClientRect();
      const cv=document.getElementById('sky');
      const sx=wm.x/cv.clientWidth*cv.width, sy=wm.y/cv.clientHeight*cv.height;
      const sw=wm.width/cv.clientWidth*cv.width, sh=wm.height/cv.clientHeight*cv.height;
      const c=document.createElement('canvas'); c.width=cv.width; c.height=cv.height;
      const g=c.getContext('2d'); let worst=0;
      for(let i=0;i<18;i++){
        window.skyFrame(i*90000/18);
        g.clearRect(0,0,c.width,c.height); g.drawImage(cv,0,0);
        const d=g.getImageData(sx,sy,Math.max(1,sw),Math.max(1,sh)).data;
        let s=0,n=0; for(let k=0;k<d.length;k+=16){s+=(d[k]*2+d[k+1]*5+d[k+2])/8;n++;}
        const m=s/n; if(m>worst) worst=m;
      }
      return {worstMeanLum: Math.round(worst*10)/10};
    }""")

    # --- fps over 3 s of the live loop
    pg.evaluate("window.skyStart && window.skyStart()")
    R["fps"] = pg.evaluate("""() => new Promise(res=>{
      let n=0; const t0=performance.now();
      (function tick(){ n++; if(performance.now()-t0<3000) requestAnimationFrame(tick);
        else res(Math.round(n/((performance.now()-t0)/1000)*10)/10); })();
    })""")

    # --- overflow on all 11 sections + scroll snap
    R["overflow"] = pg.evaluate("""() => {
      const bad=[]; document.querySelectorAll('.slide').forEach(s=>{
        if(s.scrollWidth>s.clientWidth+1||s.scrollHeight>s.clientHeight+1)
          bad.push({id:s.id, sw:s.scrollWidth, cw:s.clientWidth, sh:s.scrollHeight, ch:s.clientHeight});
      }); return bad;
    }""")
    R["sections"] = pg.evaluate("document.querySelectorAll('.slide').length")
    snap = []
    for i in range(11):
        pg.evaluate(f"window.deckGo({i})"); pg.wait_for_timeout(260)
        snap.append(pg.evaluate("Math.round(document.getElementById('deck').scrollTop/document.getElementById('deck').clientHeight*100)/100"))
    R["snap_lands"] = snap

    # --- three title frames
    pg.evaluate("window.deckGo(0)"); pg.wait_for_timeout(300)
    for sec in (0, 30, 60):
        pg.evaluate(f"window.skyStop && window.skyStop(); window.skyFrame({sec*1000})")
        pg.wait_for_timeout(120)
        pg.screenshot(path=str(OUT / f"title-t{sec:02d}s.png"))
    pg.evaluate("window.skyStart && window.skyStart()")
    for i in range(11):
        pg.evaluate(f"window.deckGo({i})"); pg.wait_for_timeout(420)
        pg.screenshot(path=str(OUT / f"card-{i+1:02d}.png"))

    # --- reduced motion still frame
    pg2 = br.new_page(viewport={"width": 1920, "height": 1080}, reduced_motion="reduce")
    pg2.goto(PAGE.as_uri()); pg2.wait_for_timeout(1800)
    R["reduced_motion_running"] = pg2.evaluate("window.skyRunning()")
    pg2.screenshot(path=str(OUT / "title-reduced-motion.png"))
    pg2.close()

    # --- PDF
    pdf = OUT / "demo-cards-v4.pdf"
    pg.evaluate("window.skySnap && window.skySnap()"); pg.wait_for_timeout(600)
    pg.pdf(path=str(pdf), landscape=True, format="A4", print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"})
    R["pdf_bytes"] = pdf.stat().st_size
    br.close()

try:
    import re
    raw = open(OUT / "demo-cards-v4.pdf", "rb").read()
    R["pdf_pages"] = len(re.findall(rb"/Type\s*/Page[^s]", raw))
except Exception as e:
    R["pdf_pages"] = "err:" + str(e)

print(json.dumps(R, indent=1)[:6000])
open(OUT / "verify.json", "w").write(json.dumps(R, indent=1))
