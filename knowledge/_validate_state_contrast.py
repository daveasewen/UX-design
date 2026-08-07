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
UNPARSEABLE colour syntax REFUSES — `StateContrastParseError`, named and attributable, counted
and exit-non-zero. It is never measured against a guessed background (s125-D3, Dave 2026-08-07).

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
  // ---- colour parsing (s125-D3, Dave 2026-08-07) --------------------------------------------
  // Chromium serialises every color-mix() result as `color(srgb r g b[ / a])`, components 0-1.
  // The old rgba()-only regex could not match it, so parse() returned null and effBg() SILENTLY
  // walked up to a pale ancestor and measured against the wrong background: Button .primary
  // hover reported 1:1 when it is 6.01:1; Stepper "Next" 1:1 when it is 6.39:1. 26 color-mix()
  // rules in canon.css, nearly all on :hover/:active — the exact states this gate exists to drive.
  // The fix is the CLASS, not the instance: syntax we cannot READ now REFUSES, named and
  // attributable. oklab()/lab()/hwb() would land the identical defect the day someone uses one.
  // The line: EMPTY and `none` are legitimately-absent paint and still return null (effBg walks
  // up, as designed); `transparent` parses as rgba(0,0,0,0) and composites, as designed. The
  // refusal is only for a non-empty value whose SYNTAX cannot be read — and for a value whose
  // shape is wrong (rgb() without 3-4 finite components), which used to silently yield NaN.
  const desc=n=>{const id=n.id?'#'+n.id:'';const c=(n.getAttribute&&n.getAttribute('class')||'').trim();
    const cl=c?'.'+c.split(/\s+/).join('.'):'';const t=(n.textContent||'').trim().slice(0,24);
    return n.tagName.toLowerCase()+id+cl+(t?' "'+t+'"':'')};
  const refuse=(value,prop,node)=>{const e=new Error('cannot parse '+prop+': "'+value+'" on '+desc(node));
    e.name='StateContrastParseError';e.value=value;e.prop=prop;e.where=desc(node);return e};
  const num=t=>{t=t.trim();const n=parseFloat(t);return t.endsWith('%')?n/100:n};
  const parse=(c,prop,node)=>{
    const s=(c||'').trim();
    if(!s||s==='none') return null;                       // genuinely absent paint -> effBg walks up
    let m=s.match(/^rgba?\(([^)]*)\)$/i);
    if(m){const v=m[1].split(',').map(x=>parseFloat(x.trim()));
      if((v.length!==3&&v.length!==4)||v.some(x=>!isFinite(x))) throw refuse(s,prop,node);
      return v;}
    m=s.match(/^color\(\s*srgb\s+([^)]*)\)$/i);
    if(m){const parts=m[1].split('/');
      const v=parts[0].trim().split(/\s+/).map(num), a=parts.length>1?num(parts[1]):1;
      if(parts.length>2||v.length!==3||v.some(x=>!isFinite(x))||!isFinite(a)) throw refuse(s,prop,node);
      // components are 0-1 FLOATS here, not 0-255. Scale, clamp to gamut (what the display does),
      // and ROUND to the 8-bit channel actually rendered — the rgba() path is already integer-only,
      // so without this the same colour measures differently depending on which syntax it arrived in
      // (Button .primary hover: 5.98 unrounded vs 6.01 at the rendered rgb(99,99,99)).
      const to255=x=>Math.round(Math.min(255,Math.max(0,x*255)));
      const r=[to255(v[0]),to255(v[1]),to255(v[2])];
      return parts.length>1?[r[0],r[1],r[2],a]:r;}
    throw refuse(s,prop,node);                            // oklab()/lab()/hwb()/anything new: never guess
  };
  function effBg(node){while(node){const cs=getComputedStyle(node);const p=parse(cs.backgroundColor,'background-color',node);if(p){const a=p.length===4?p[3]:1;if(a>=1)return [p[0],p[1],p[2]];const u=node.parentElement?effBg(node.parentElement):[255,255,255];return [Math.round(p[0]*a+u[0]*(1-a)),Math.round(p[1]*a+u[1]*(1-a)),Math.round(p[2]*a+u[2]*(1-a))]}node=node.parentElement}return [255,255,255]}
  const out=[], nodes=[el, ...el.querySelectorAll('*')];
  for(const n of nodes){
   try{
    const cs=getComputedStyle(n);
    if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0) continue;
    if(n.closest('[disabled],[aria-disabled="true"],.is-disabled,.demo-controls,.controls') || (n.matches&&n.matches(':disabled'))) continue;
    if([...n.childNodes].some(c=>c.nodeType===3&&c.textContent.trim().length)){
      const fg=parse(cs.color,'color',n);
      if(fg){const bg=effBg(n),fs=parseFloat(cs.fontSize)||16,bold=(parseInt(cs.fontWeight)||400)>=700,large=fs>=24||(fs>=18.66&&bold),thr=large?3.0:4.5,r=ratio(fg,bg);
        if(r<thr) out.push({kind:'text',text:n.textContent.trim().slice(0,32),ratio:Math.round(r*100)/100,thr});}
    }
    if(n.tagName.toLowerCase()==='svg'){
      const fc=(cs.fill&&cs.fill!=='none')?cs.fill:cs.color, fg=parse(fc,'fill',n);
      if(fg){const bg=effBg(n),r=ratio(fg,bg); if(r<3.0) out.push({kind:'icon',ariaHidden:!!n.closest('[aria-hidden="true"]'),ratio:Math.round(r*100)/100,thr:3.0});}
    }
   }catch(e){
    // A refusal is a RESULT, not a skip: it is carried out as a first-class record, counted,
    // and it fails the gate. Anything else is a real bug and is re-thrown, loudly.
    if(e&&e.name==='StateContrastParseError'){out.push({kind:'refusal',prop:e.prop,value:e.value,where:e.where,text:(n.textContent||'').trim().slice(0,32)});continue}
    throw e;
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
            except Exception:
                # DRIVING may legitimately fail (element not hoverable, moved, detached) — skip.
                try: pg.mouse.up()
                except Exception: pass
                continue
            # MEASURING may not. s125-D3: the same silent-default class lived one level up —
            # a blanket except here swallowed every JS error, refusals included. A measurement
            # error is now loud. (Unparseable colour is NOT an error: it returns a refusal record.)
            try:
                fails = pg.evaluate(MEASURE, el)
            finally:
                if label == "pressed":
                    try: pg.mouse.up()
                    except Exception: pass
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
    total = 0; refused = 0
    for name in sorted(res):
        seen=set(); uniq=[]
        for theme,state,fl in res[name]:
            k=(theme,state,fl["kind"],fl.get("text"),fl.get("ratio"),fl.get("prop"),fl.get("value"),fl.get("where"))
            if k in seen: continue
            seen.add(k); uniq.append((theme,state,fl))
        tf=[u for u in uniq if u[2]["kind"]=="text"]; iw=[u for u in uniq if u[2]["kind"]=="icon"]
        rf=[u for u in uniq if u[2]["kind"]=="refusal"]
        total += len(tf); refused += len(rf)
        bits=[]
        if tf: bits.append(f"❌ {len(tf)} TEXT fail(s)")
        # a refusal is UNMEASURED, so this snippet may NOT be reported as clean
        if rf: bits.append(f"⛔ {len(rf)} PARSE REFUSAL(s) — UNMEASURED")
        if iw: bits.append(f"{len(iw)} icon warn(s)")
        out.append(f"## {name} — {' · '.join(bits) if bits else '✅ clean'}")
        for theme,state,fl in tf: out.append(f"- ❌ TEXT [{theme}/{state}] {fl['ratio']}:1 (need {fl['thr']}) — \"{fl['text']}\"")
        for theme,state,fl in rf: out.append(f"- ⛔ StateContrastParseError [{theme}/{state}] cannot parse {fl['prop']}: `{fl['value']}` on {fl['where']}")
        for theme,state,fl in iw: out.append(f"- 🟡 icon [{theme}/{state}] {fl['ratio']}:1 (need 3.0){' (decorative)' if fl.get('ariaHidden') else ''}")
        out.append("")
    out[3] = f"**{total} text failure(s) across {len(res)} snippet(s).**"
    if refused:
        # appended at the END on purpose: out[3] is a known separate defect (it overwrites the
        # first snippet's heading rather than inserting) and is NOT in this change's scope.
        out += ["---",
                f"**⛔ {refused} PARSE REFUSAL(s) — `StateContrastParseError`.** A colour value above "
                "could not be READ, so nothing was measured against it. These are not passes and not "
                "failures: they are holes. Teach `parse()` the syntax, or the value is wrong (s125-D3).",
                ""]
    open(os.path.join(HERE,"_STATE-CONTRAST-AUDIT.md"),"w",encoding="utf-8").write("\n".join(out))
    print("\n".join(out))
    if refused:
        print(f"StateContrastParseError: {refused} unreadable colour value(s) — see _STATE-CONTRAST-AUDIT.md",
              file=sys.stderr)
    sys.exit(1 if (total or refused) else 0)

if __name__ == "__main__":
    main()
