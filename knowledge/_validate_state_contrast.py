#!/usr/bin/env python3
"""
State-contrast gate — renders each gated snippet in light + dark, drives the real interactive
states (hover, pressed = hover+mousedown) on every interactive element, and checks the COMPUTED
foreground (text colour / svg fill) against the EFFECTIVE rendered background.

Closes the blind spot that let Cards score 9/9 with real failures (decided 2026-06-22, Dave):
the declared-pairs contrast check only verifies the pairs an author remembers to declare, so
undeclared state×theme combos (dark hover, pressed) escaped. This drives the actual states and
measures them — the automated version of the manual checks. (DevTools forcePseudoState was tried
first but applies the forced colour without the forced background — unreliable — so we use real
hover, which the render screenshots proved correct.)

TEXT below threshold (4.5, or 3.0 for large text) FAILS the gate.
ICONS (svg) below 3.0 are reported as WARN (many are aria-hidden/decorative — judgement needed).
DISABLED controls are skipped (WCAG-exempt from contrast).

Usage:  python3 _validate_state_contrast.py [name-filter ...]   (default: all snippets)
Needs:  headless Chromium via Playwright (see memory: sandbox-html-rendering).
Writes: _STATE-CONTRAST-AUDIT.md.  Exit non-zero on any TEXT failure.
"""
import os, sys, glob
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
SEL = 'a, button, [role="radio"], [role="button"], [role="switch"], [role="tab"], [tabindex]:not([tabindex="-1"]), label, summary'

MEASURE = r"""
(el) => {
  const lum=p=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return 0.2126*f(p[0])+0.7152*f(p[1])+0.0722*f(p[2])};
  const ratio=(a,b)=>{const L1=lum(a),L2=lum(b),hi=Math.max(L1,L2),lo=Math.min(L1,L2);return (hi+0.05)/(lo+0.05)};
  const parse=c=>{const m=(c||'').match(/rgba?\(([^)]+)\)/);if(!m)return null;return m[1].split(',').map(s=>parseFloat(s.trim()))};
  function effBg(node){while(node){const cs=getComputedStyle(node);const p=parse(cs.backgroundColor);if(p){const a=p.length===4?p[3]:1;if(a>=1)return [p[0],p[1],p[2]];const u=node.parentElement?effBg(node.parentElement):[255,255,255];return [Math.round(p[0]*a+u[0]*(1-a)),Math.round(p[1]*a+u[1]*(1-a)),Math.round(p[2]*a+u[2]*(1-a))]}node=node.parentElement}return [255,255,255]}
  const out=[], nodes=[el, ...el.querySelectorAll('*')];
  for(const n of nodes){
    const cs=getComputedStyle(n);
    if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0) continue;
    if(n.closest('[disabled],[aria-disabled="true"],.is-disabled,.demo-controls,.controls') || (n.matches&&n.matches(':disabled'))) continue;
    if([...n.childNodes].some(c=>c.nodeType===3&&c.textContent.trim().length)){
      const fg=parse(cs.color);
      if(fg){const bg=effBg(n),fs=parseFloat(cs.fontSize)||16,bold=(parseInt(cs.fontWeight)||400)>=700,large=fs>=24||(fs>=18.66&&bold),thr=large?3.0:4.5,r=ratio(fg,bg);
        if(r<thr) out.push({kind:'text',text:n.textContent.trim().slice(0,32),ratio:Math.round(r*100)/100,thr});}
    }
    if(n.tagName.toLowerCase()==='svg'){
      const fc=(cs.fill&&cs.fill!=='none')?cs.fill:cs.color, fg=parse(fc);
      if(fg){const bg=effBg(n),r=ratio(fg,bg); if(r<3.0) out.push({kind:'icon',ariaHidden:!!n.closest('[aria-hidden="true"]'),ratio:Math.round(r*100)/100,thr:3.0});}
    }
  }
  return out;
}
"""

def audit_page(pg, theme, sink):
    for el in pg.query_selector_all(SEL):
        try:
            if not el.is_visible(): continue   # skip hidden (e.g. a closed modal) — avoids slow hover timeouts
        except Exception:
            continue
        # Never DRIVE demo chrome (2026-07-03): pressed = mouse down+up = a CLICK, and the
        # snippets' own #themeToggle is the first button in document order — clicking it flipped
        # the theme mid-sweep, so each pass measured the OTHER theme (the "light 4.02" fail on
        # Selection-controls was the dark theme wearing a light label). Measurement already
        # excluded .demo-controls/.controls; driving must too.
        try:
            if el.evaluate("e=>!!e.closest('.demo-controls,.controls')"): continue
        except Exception:
            continue
        for label in ("hover", "pressed"):
            try:
                # re-assert the theme before every drive — belt-and-braces against any
                # state-mutating click putting the page in the wrong theme silently
                pg.evaluate("t=>document.body.setAttribute('data-theme',t)", theme)
                el.hover(timeout=250); pg.wait_for_timeout(20)
                if label == "pressed": pg.mouse.down(); pg.wait_for_timeout(25)
                fails = pg.evaluate(MEASURE, el)
                if label == "pressed": pg.mouse.up()
            except Exception:
                try: pg.mouse.up()
                except Exception: pass
                continue
            for fl in fails:
                sink.append((theme, label, fl))

def run(filters):
    files = sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))
    if filters:
        files = [f for f in files if any(x.lower() in os.path.basename(f).lower() for x in filters)]
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--force-color-profile=srgb"])
        for f in files:
            name = os.path.basename(f).replace(".reference.html","")
            sink = []
            for theme in ("light","dark"):
                pg = b.new_page(viewport={"width":900,"height":1200})
                pg.goto("file://"+f); pg.evaluate("t=>document.body.setAttribute('data-theme',t)", theme)
                pg.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important;}")  # states apply instantly -> no mid-transition artifacts
                pg.wait_for_timeout(40)
                audit_page(pg, theme, sink)
                pg.close()
            results[name] = sink
        b.close()
    return results

def main():
    res = run(sys.argv[1:])
    out = ["# State-contrast audit — rendered hover / pressed states (light + dark)",
           "*Drives each interactive element's real hover/pressed states and measures computed foreground "
           "vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). "
           "Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*",
           ""]
    total = 0
    for name in sorted(res):
        seen=set(); uniq=[]
        for theme,state,fl in res[name]:
            k=(theme,state,fl["kind"],fl.get("text"),fl["ratio"])
            if k in seen: continue
            seen.add(k); uniq.append((theme,state,fl))
        tf=[u for u in uniq if u[2]["kind"]=="text"]; iw=[u for u in uniq if u[2]["kind"]=="icon"]
        total += len(tf)
        out.append(f"## {name} — {'✅ clean' if not tf else f'❌ {len(tf)} TEXT fail(s)'}{f' · {len(iw)} icon warn(s)' if iw else ''}")
        for theme,state,fl in tf: out.append(f"- ❌ TEXT [{theme}/{state}] {fl['ratio']}:1 (need {fl['thr']}) — \"{fl['text']}\"")
        for theme,state,fl in iw: out.append(f"- 🟡 icon [{theme}/{state}] {fl['ratio']}:1 (need 3.0){' (decorative)' if fl.get('ariaHidden') else ''}")
        out.append("")
    out[3] = f"**{total} text failure(s) across {len(res)} snippet(s).**"
    open(os.path.join(HERE,"_STATE-CONTRAST-AUDIT.md"),"w",encoding="utf-8").write("\n".join(out))
    print("\n".join(out))
    sys.exit(1 if total else 0)

if __name__ == "__main__":
    main()
