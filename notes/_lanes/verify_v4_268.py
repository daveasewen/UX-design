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

    # --- VISUAL no-void grid, over 18 phases of the 90 s revolution.
    #     v4's check passed on stars nobody could see. The bar is now:
    #     per 12x7 cell, mean luminance >= 8 AND >= 6 star peaks at L >= 120.
    probe = pg.evaluate("""() => {
      const out=[]; const cv=document.getElementById('sky');
      const c=document.createElement('canvas'); c.width=cv.width; c.height=cv.height;
      const g=c.getContext('2d');
      const CW=Math.floor(c.width/12), CH=Math.floor(c.height/7);
      for(let i=0;i<18;i++){
        const t=i*90000/18; window.skyFrame(t);
        const v=window.skyVoidCheck(12,7);
        g.clearRect(0,0,c.width,c.height); g.drawImage(cv,0,0);
        const D=g.getImageData(0,0,c.width,c.height).data;
        const W=c.width;
        // full-frame luminance map, once
        const L=new Float32Array(c.width*c.height);
        for(let k=0,n=0;k<D.length;k+=4,n++) L[n]=(D[k]*2+D[k+1]*5+D[k+2])/8;
        let minMean=1e9, maxMean=0, minPeaks=1e9, maxLum=0, sumAll=0, nAll=0;
        for(let r=0;r<7;r++) for(let col=0;col<12;col++){
          const x0=col*CW, y0=r*CH;
          let sum=0, n=0, peaks=0, mx=0;
          for(let y=y0;y<y0+CH;y++){
            const row=y*W;
            for(let x=x0;x<x0+CW;x++){
              const l=L[row+x]; sum+=l; n++; if(l>mx)mx=l;
              if(l>=120 && x>0 && x<W-1 && y>0 && y<c.height-1){
                if(l>=L[row+x-1] && l>=L[row+x+1] && l>=L[row-W+x] && l>=L[row+W+x]) peaks++;
              }
            }
          }
          const mean=sum/n;
          if(mean<minMean)minMean=mean; if(mean>maxMean)maxMean=mean;
          if(peaks<minPeaks)minPeaks=peaks; if(mx>maxLum)maxLum=mx;
          sumAll+=sum; nAll+=n;
        }
        out.push({phase:i, starMin:v.min, starMax:v.max, visMin:v.minVisible,
                  cellMeanMin:Math.round(minMean*10)/10,
                  cellMeanMax:Math.round(maxMean*10)/10,
                  cellPeaksMin:minPeaks, maxLum:Math.round(maxLum),
                  frameMean:Math.round(sumAll/nAll*10)/10});
      }
      return out;
    }""")
    R["phases18"] = probe
    R["void_min_over_18"]      = min(p["starMin"] for p in probe)
    R["visible_star_min"]      = min(p["visMin"] for p in probe)
    R["cell_mean_lum_min"]     = min(p["cellMeanMin"] for p in probe)
    R["cell_star_peaks_min"]   = min(p["cellPeaksMin"] for p in probe)

    # --- exposure OUTSIDE the text vignette: the right 55% of the frame,
    #     which the vignette's 52%x44%@31% core never reaches.
    R["exposure_outside_vignette"] = pg.evaluate("""() => {
      const cv=document.getElementById('sky');
      const c=document.createElement('canvas'); c.width=cv.width; c.height=cv.height;
      const g=c.getContext('2d');
      const x0=Math.floor(cv.width*0.55), w=cv.width-x0;
      let lo=1e9, hi=0, acc=0;
      for(let i=0;i<18;i++){
        window.skyFrame(i*90000/18);
        g.clearRect(0,0,c.width,c.height); g.drawImage(cv,0,0);
        const d=g.getImageData(x0,0,w,cv.height).data;
        let s=0,n=0; for(let k=0;k<d.length;k+=4){s+=(d[k]*2+d[k+1]*5+d[k+2])/8;n++;}
        const m=s/n; acc+=m; if(m<lo)lo=m; if(m>hi)hi=m;
      }
      return {min:Math.round(lo*10)/10, max:Math.round(hi*10)/10,
              mean:Math.round(acc/18*10)/10};
    }""")

    R["nebula_seat"] = pg.evaluate("window.skyNebula()")

    # --- wordmark: mean luminance of the canvas region behind the type,
    #     measured through the vignette, over the same 18 phases
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

    # --- wordmark contrast, COMPOSITED: 18 phases, type hidden, screenshot
    #     exactly the glyph-ink rect. Contrast is white vs the worst pixel.
    from PIL import Image
    import io as _io
    ink = pg.evaluate("""() => {
      const wm=document.querySelector('#s1 .wordmark');
      const r=document.createRange(); r.selectNodeContents(wm);
      const b=r.getBoundingClientRect();
      return {x:Math.floor(b.left), y:Math.floor(b.top),
              width:Math.ceil(b.width), height:Math.ceil(b.height)};
    }""")
    pg.evaluate("window.skyStop && window.skyStop()")
    pg.evaluate("document.querySelector('#s1 .type').style.visibility='hidden'")

    def lin(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    worst_mean = 0.0
    worst_max = 0
    worst_phase = 0
    for k in range(18):
        pg.evaluate("(ms)=>window.skyFrame(ms)", k * 90000 / 18.0)
        im = Image.open(_io.BytesIO(pg.screenshot(clip=ink))).convert("RGB")
        px = list(im.getdata())
        lums = [(2 * r + 5 * g + b) / 8.0 for (r, g, b) in px]
        m = sum(lums) / len(lums)
        mx = max(lums)
        if m > worst_mean:
            worst_mean, worst_phase = m, k
        if mx > worst_max:
            worst_max = mx
        if k in (0, 9):
            im.save(str(OUT / f"wordmark-phase-{k:02d}.png"))
    pg.evaluate("document.querySelector('#s1 .type').style.visibility=''")
    pg.evaluate("window.skyFrame(0)")
    R["wordmark_contrast"] = {
        "worstMeanL": round(worst_mean, 1),
        "worstMaxL": round(worst_max, 1),
        "worstPhase": worst_phase,
        "contrast_vs_mean": round(1.05 / (lin(worst_mean) + 0.05), 2),
        "contrast_vs_brightest_px": round(1.05 / (lin(worst_max) + 0.05), 2),
        "note": "white #fff wordmark against the composited backdrop through the vignette, 18 phases",
    }

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
