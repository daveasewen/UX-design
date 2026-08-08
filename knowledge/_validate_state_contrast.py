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
THE EFFECTIVE BACKGROUND IS THE PAINT STACK under the element, read from the browser's own hit
stack, not the ancestor chain: an absolutely-positioned SIBLING paints the selected pill in every
`.seg` in canon.css and an ancestor walk cannot see it (2026-08-07). Where the box is not
hit-testable, the OLD ancestor walk runs as a DECLARED fallback and the audit says so per snippet.

Usage:  python3 _validate_state_contrast.py [name-filter ...]   (default: all snippets)
        python3 _validate_state_contrast.py --selftest          (bites, no snippets)
        An unknown option is a NAMED failure, never a silent name-filter, and a name-filter
        that matches no snippet is a NAMED failure too — a filter that quietly selects
        nothing writes an empty audit that looks like a clean one.
Needs:  headless Chromium via Playwright (see memory: sandbox-html-rendering) — for --selftest
        as well: this gate cannot be proven without a browser, so an unavailable browser is a
        selftest FAILURE, never a silent skip.
Writes: _STATE-CONTRAST-AUDIT.md.  Exit non-zero on any TEXT failure.
"""
import os, re, sys, glob, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
SEL = 'a, button, [role="radio"], [role="button"], [role="switch"], [role="tab"], [tabindex]:not([tabindex="-1"]), label, summary'


class StateContrastArgError(Exception):
    """An argument this script cannot honour. NAMED — never quietly defaulted to a name-filter."""


class StateContrastReportError(Exception):
    """The rendered audit disagrees with the counters it was rendered from."""


class StateContrastSelftestError(Exception):
    """The selftest could not be RUN. That is a failure, not a skip."""


HOLE_REASON_UNRECORDED = ("reason NOT RECORDED by the measurement that produced this record — "
                          "re-run the gate; do not infer one")


def _fallback_holes(records):
    """Every un-hit-testable box, as (where, reason) — DECLARED HOLES, `s129-D3`.

    ⛔ These were called "ancestor-fallback backgrounds" and filed as provenance. Dave ruled
    at #129 that they are NAMED HOLES: each one stays in the report, labelled UNMEASURABLE,
    carrying the reason its paint stack could not be observed. The alternative on the table —
    REFUSING them — was rejected because it turns 60 measured records into nothing; and the
    alternative nobody offered — quietly publishing the ancestor-walk number as if it were a
    hit-stack measurement — is the invented-number class this file exists to kill.

    ⚠ WHAT A HOLE DOES **NOT** MEAN HERE: it does not waive a failure. The ancestor walk still
    runs, its ratios are still reported, and a failing one is still ❌. The hole is a statement
    about the BACKGROUND's provenance, not a licence to stop reporting.

    The reason is MEASURED at the browser, not classified afterwards: `samplePoint()` returning
    null means the box has no on-screen geometry; a live point whose hit stack does not contain
    the node means it opted out of hit-testing or something over it did.
    """
    seen = {}
    for r in records:
        if r[2]["kind"] == "fallback":
            seen.setdefault(r[2]["where"], r[2].get("reason") or HOLE_REASON_UNRECORDED)
    return sorted(seen.items())

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
  // ---- effective background: a PAINT STACK, not an ancestor chain (2026-08-07) ---------------
  // THE CLASS: the old effBg() walked node.parentElement upwards, which models the paint stack as
  // the ANCESTOR CHAIN. CSS does not paint that way — it paints BOXES in z-order, and any box that
  // geometrically covers the element and paints beneath it contributes, ancestor or not. Ancestors
  // are a SUBSET of that set, so an ancestor walk is not a cheap approximation; it is blind by
  // construction to the commonest idiom in canon.css: `.seg .ind{position:absolute; background:
  // var(--sel); z-index:0}` slides UNDER a `position:relative; z-index:1` button whose own
  // background is `transparent`. The selected pill's label was therefore measured against a pale
  // ANCESTOR and reported 1:1 (light) / 1.3:1 (dark) where it renders far above threshold.
  // 32 FALSE failures: Segmented-control x12, Charts x16, View-options x4. Rendering was fine.
  // Distinct from s125-D3, which was a PARSE defect in the same function's neighbour: that one
  // misread a colour, this one reads the right colour off the wrong box.
  // document.elementsFromPoint() IS the browser's own hit stack in paint order (topmost first), so
  // the fix borrows the engine's stacking rules instead of re-implementing z-index, stacking
  // contexts and paint phases — a re-implementation would be a second model to go silently wrong.
  // KNOWN AND MEASURED RESIDUAL: hit-testing skips `pointer-events:none` boxes, so a painted
  // overlay that opts out of hit-testing would still be missed by the stack walk. Measured across
  // all 75 snippets in light+dark on 2026-08-07: exactly ONE painted such element exists
  // (Dropdown's `li.sep`, a 1px flow separator overlapping no text). Named, not defended against
  // speculatively. The other half — a MEASURED node that is itself un-hit-testable — is real and
  // common (tooltips, decorative svg, cells below the fold) and takes the declared fallback below.
  const samplePoint=(node)=>{                     // a point inside the node AND inside the viewport
    const r=node.getBoundingClientRect();
    if(!(r.width>0&&r.height>0)) return null;
    const l=Math.max(r.left,0), t=Math.max(r.top,0);
    const rt=Math.min(r.right,innerWidth-1), bt=Math.min(r.bottom,innerHeight-1);
    if(!(rt>=l&&bt>=t)) return null;               // nothing of the node is on screen
    return [(l+rt)/2,(t+bt)/2];
  };
  // A box's paint is scaled by its own `opacity` AND by every opacity above it. MEASURED, not
  // assumed: `.dv-toggle-seg .ind{background:var(--ink); opacity:0}` on the UNPRESSED toggles in
  // Chart-line/Chart-combo is a fully-opaque background that paints NOTHING. Reading its
  // background-color and ignoring its opacity invented 12 fresh false failures at 1.17:1 — the
  // same class of wrong answer this whole change exists to remove, one property to the left.
  const groupAlpha=(el)=>{let o=1;for(let n=el;n&&n.nodeType===1;n=n.parentElement){
    const v=parseFloat(getComputedStyle(n).opacity); if(isFinite(v)) o*=v; if(o<=0) break} return o};
  // The DECLARED FALLBACK, kept verbatim from the pre-2026-08-07 implementation: hit-testing sees
  // neither an off-screen box nor a `pointer-events:none` one (tooltips, decorative svg, a header
  // cell below the fold). For those the paint stack is not observable, so the OLD ancestor walk
  // runs and the audit SAYS SO per snippet. It is deliberately unimproved — being byte-for-byte
  // the previous algorithm is what makes the before/after delta of this change attributable.
  function ancestorBg(node){while(node){const cs=getComputedStyle(node);const p=parse(cs.backgroundColor,'background-color',node);if(p){const a=p.length===4?p[3]:1;if(a>=1)return [p[0],p[1],p[2]];const u=node.parentElement?ancestorBg(node.parentElement):[255,255,255];return [Math.round(p[0]*a+u[0]*(1-a)),Math.round(p[1]*a+u[1]*(1-a)),Math.round(p[2]*a+u[2]*(1-a))]}node=node.parentElement}return [255,255,255]}
  function effBg(node){
    const pt=samplePoint(node);
    const stack=pt?document.elementsFromPoint(pt[0],pt[1]):[];
    const i=stack.indexOf(node);
    // Not hit-testable here. DECLARED, never hidden: a record is emitted so the audit can say
    // which backgrounds carry the weaker measurement. ✅ s129-D3, Dave, #129: this record is now
    // a NAMED HOLE — reported UNMEASURABLE — and it carries the REASON, which is MEASURED here
    // rather than guessed downstream. Two distinguishable causes, and only two: no on-screen
    // geometry at all (samplePoint refused), or a live sample point whose hit stack does not
    // contain this node (pointer-events:none, or something over it eating the hit).
    if(i<0){out.push({kind:'fallback',where:desc(node),
            reason:(pt?'not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit)'
                      :'no on-screen box at measurement time (zero-size, or entirely outside the viewport)'),
            text:(node.textContent||'').trim().slice(0,32)});
            return ancestorBg(node);}
    let R=0,G=0,B=0,rem=1;                          // src-over compositing, top-down from the node
    for(let k=i;k<stack.length&&rem>0.0005;k++){
      const p=parse(getComputedStyle(stack[k]).backgroundColor,'background-color',stack[k]);
      if(!p) continue;                              // absent paint: keep descending, as before
      const a=(p.length===4?p[3]:1)*groupAlpha(stack[k]); if(!(a>0)) continue;
      R+=rem*a*p[0]; G+=rem*a*p[1]; B+=rem*a*p[2]; rem*=(1-a);
    }
    return [Math.round(R+rem*255),Math.round(G+rem*255),Math.round(B+rem*255)];   // canvas base = white
  }
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
        # A filter that matches nothing used to write an EMPTY audit, which reads exactly like a
        # clean one. Same class as the unknown-option default: the tool guessed what you meant.
        if not files:
            raise StateContrastArgError(
                "no snippet matches " + ", ".join(repr(x) for x in filters) +
                " — refusing to write an empty audit that would read as a clean one")
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

HEADLINE_RE = re.compile(r"^\*\*(\d+) text failure\(s\) across (\d+) snippet\(s\)\.\*\*$", re.M)
# ✅ s129-D3 — the holes count is a STATED FIGURE, so it gets the same treatment as the other two:
# parsed back out of the artefact and asserted against the body. A stated number with nothing
# re-reading it is exactly how this file came to claim 38 snippets while carrying 37.
HOLES_RE = re.compile(r"^\*\*(\d+) DECLARED HOLE\(s\) — un-hit-testable box\(es\), reported "
                      r"UNMEASURABLE by name \(s129-D3\)\.\*\*$", re.M)
HOLE_PREFIX = "- ⬛ UNMEASURABLE (declared hole)"

def verify_report(text, n_snippets, total_text, n_holes=None):
    """Re-READ the rendered artefact and check it says what the counters say.

    The committed audit claimed "across 38 snippet(s)" and carried 37 sections for three sessions:
    a stated figure with nothing re-checking it. A number computed in the same breath as the prose
    it describes is not a check — parsing the artefact back, in the artefact's own grammar, is.
    """
    lines = text.split("\n")
    heads = [l for l in lines if l.startswith("## ")]
    fails = [l for l in lines if l.startswith("- ❌ TEXT ")]
    m = HEADLINE_RE.search(text)
    if not m:
        raise StateContrastReportError("the audit carries no headline count line")
    said_fail, said_snips = int(m.group(1)), int(m.group(2))
    if said_snips != n_snippets or len(heads) != n_snippets:
        raise StateContrastReportError(
            f"snippet count disagrees — headline says {said_snips}, counters say {n_snippets}, "
            f"artefact carries {len(heads)} section heading(s)")
    if said_fail != total_text or len(fails) != total_text:
        raise StateContrastReportError(
            f"text-failure count disagrees — headline says {said_fail}, counters say {total_text}, "
            f"artefact carries {len(fails)} failure line(s)")
    # ✅ s129-D3 — HOLES ARE ASSERTED ON EVERY WRITE. Three numbers must agree: the counter, the
    # stated header figure, and the ⬛ lines actually in the body. A hole that is counted but not
    # written, or written but not counted, is the failure mode that matters — a hole going quiet
    # is indistinguishable from a clean run to every downstream reader.
    if n_holes is not None:
        holes = [l for l in lines if l.startswith(HOLE_PREFIX)]
        mh = HOLES_RE.search(text)
        if not mh:
            raise StateContrastReportError(
                "the audit carries no DECLARED HOLE(s) header line — s129-D3 requires the count "
                "to be stated on every write, including when it is zero")
        if int(mh.group(1)) != n_holes or len(holes) != n_holes:
            raise StateContrastReportError(
                f"declared-hole count disagrees — header says {int(mh.group(1))}, counters say "
                f"{n_holes}, artefact carries {len(holes)} ⬛ line(s). A silently dropped hole "
                f"reads as a measured pass (s129-D3)")

def render_report(res):
    """Render the audit markdown from a results dict.

    PURE — no browser, no IO — so --selftest can bite the report's own arithmetic without
    rendering anything. Returns (text, total_text, refused, ancestor_fallbacks).
    """
    out = ["# State-contrast audit — rendered hover / pressed states (light + dark)",
           "*Drives each interactive element's real hover/pressed states and measures computed foreground "
           "vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). "
           "Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*",
           ""]
    total = 0; refused = 0; fellback = 0
    for name in sorted(res):
        seen=set(); uniq=[]
        for theme,state,fl in res[name]:
            k=(theme,state,fl["kind"],fl.get("text"),fl.get("ratio"),fl.get("prop"),fl.get("value"),fl.get("where"))
            if k in seen: continue
            seen.add(k); uniq.append((theme,state,fl))
        tf=[u for u in uniq if u[2]["kind"]=="text"]; iw=[u for u in uniq if u[2]["kind"]=="icon"]
        rf=[u for u in uniq if u[2]["kind"]=="refusal"]; fb=_fallback_holes(uniq)
        total += len(tf); refused += len(rf); fellback += len(fb)
        bits=[]
        if tf: bits.append(f"❌ {len(tf)} TEXT fail(s)")
        # a refusal is UNMEASURED, so this snippet may NOT be reported as clean
        if rf: bits.append(f"⛔ {len(rf)} PARSE REFUSAL(s) — UNMEASURED")
        if iw: bits.append(f"{len(iw)} icon warn(s)")
        # ✅ s129-D3: a NAMED HOLE, not a footnote. The snippet may not read as fully measured.
        if fb: bits.append(f"⬛ {len(fb)} UNMEASURABLE box(es)")
        out.append(f"## {name} — {' · '.join(bits) if bits else '✅ clean'}")
        for theme,state,fl in tf: out.append(f"- ❌ TEXT [{theme}/{state}] {fl['ratio']}:1 (need {fl['thr']}) — \"{fl['text']}\"")
        for theme,state,fl in rf: out.append(f"- ⛔ StateContrastParseError [{theme}/{state}] cannot parse {fl['prop']}: `{fl['value']}` on {fl['where']}")
        for theme,state,fl in iw: out.append(f"- 🟡 icon [{theme}/{state}] {fl['ratio']}:1 (need 3.0){' (decorative)' if fl.get('ariaHidden') else ''}")
        for w, why in fb:
            out.append(HOLE_PREFIX + f" — {w} — {why}. The paint stack under it cannot be "
                       "observed, so the pre-2026-08-07 ancestor-only walk ran instead: any "
                       "ratio reported over this box is that weaker measurement, NOT a hit-stack "
                       "one. Nothing is invented and nothing is waived (s129-D3).")
        out.append("")
    # INSERT the headline — do NOT assign it. `out[3] = …` overwrote whatever already occupied
    # index 3, which was the FIRST snippet's heading (Accordion, eaten; the audit then claimed 38
    # sections and carried 37), and raised IndexError outright when no snippet was in scope,
    # because index 3 only exists once a section has been appended. A summary is a NEW line.
    out[3:3] = [f"**{total} text failure(s) across {len(res)} snippet(s).**", "",
                f"**{fellback} DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE "
                f"by name (s129-D3).**", ""]
    if refused:
        out += ["---",
                f"**⛔ {refused} PARSE REFUSAL(s) — `StateContrastParseError`.** A colour value above "
                "could not be READ, so nothing was measured against it. These are not passes and not "
                "failures: they are holes. Teach `parse()` the syntax, or the value is wrong (s125-D3).",
                ""]
    if fellback:
        out += ["---",
                f"**⬛ {fellback} DECLARED HOLE(s) — UNMEASURABLE, `s129-D3` (Dave, #129).** Each box "
                "above is not hit-testable — it has no on-screen geometry, or it opts out of hit "
                "testing (`pointer-events:none`), or something over it takes the hit — so the paint "
                "stack beneath it CANNOT BE OBSERVED. Every one is listed BY NAME with its measured "
                "reason. The pre-2026-08-07 ancestor-only walk still runs over them, so no failure is "
                "waived and no threshold moved; but an overlapping sibling would still be missed, and "
                "those readings may NOT be quoted as hit-stack measurements. ⛔ Dave ruled DECLARE, "
                "not REFUSE: refusing them would have turned ~60 measured records into nothing, and "
                "publishing the fallback number as if it were the real one is the invented-number "
                "class this gate exists to kill. The count above is RE-READ off this artefact and "
                "asserted equal to the number of ⬛ lines on every write — a hole that goes quiet is "
                "a failed write, not a clean run.",
                ""]
    text = "\n".join(out)
    verify_report(text, len(res), total, n_holes=fellback)
    return text, total, refused, fellback

def parse_args(argv):
    """Bare words are snippet-name filters; anything starting with '-' must be a KNOWN flag.

    The old code handed sys.argv[1:] straight to run() as filters, so `--selftest` — or any typo —
    became a filter that matched nothing, silently. An unknown argument is now named and refused.
    """
    filters, want_selftest = [], False
    for a in argv:
        if a == "--selftest":
            want_selftest = True
        elif a in ("-h", "--help"):
            print((__doc__ or "").strip()); raise SystemExit(0)
        elif a.startswith("-"):
            raise StateContrastArgError(
                f"unknown option {a!r} — valid: --selftest, --help, or bare snippet-name filters")
        else:
            filters.append(a)
    if want_selftest and filters:
        raise StateContrastArgError(
            f"--selftest takes no name-filters (got {filters!r}) — it drives its own fixtures")
    return filters, want_selftest

# --- selftest fixtures: real files, loaded with goto("file://…"). set_content() is BANNED
# (_RUNBOOK-render-verify.md) because it silently drops linked CSS. -----------------------------
_FIX_HEAD = ('<!doctype html><meta charset="utf-8"><title>state-contrast selftest</title>'
             '<style>body{margin:0;background:#ffffff;font:16px/1.4 sans-serif}'
             '.seg{position:relative;display:inline-flex;background:#ffffff}'
             '.ind{position:absolute;top:0;bottom:0;left:0;width:120px;z-index:0}'
             '.seg button{position:relative;z-index:1;width:120px;height:40px;border:0;'
             'background:transparent;color:#ffffff;font:inherit}</style>')
FIXTURES = {
    # canon.css's commonest idiom in miniature: an absolutely-positioned SIBLING paints the pill.
    # White label on BLACK renders 21:1; the ancestor walk measured the white .seg and said 1:1.
    "sibling_paint_is_seen":
        _FIX_HEAD + '<div class="seg"><span class="ind" style="background:#000000"></span>'
                    '<button id="target" type="button">Sel</button></div>',
    # THE NEGATIVE CONTROL, and the load-bearing arm: same geometry, sibling painted WHITE.
    # White on white is a REAL failure and must still be reported. Without this arm, a fix that
    # simply stopped reporting anything would pass every other arm in this file.
    "white_on_white_still_fails":
        _FIX_HEAD + '<div class="seg"><span class="ind" style="background:#ffffff"></span>'
                    '<button id="target" type="button">Sel</button></div>',
    # The ANCESTOR path must survive the rewrite — no sibling at all, painted parent.
    "ancestor_paint_is_seen":
        _FIX_HEAD + '<div class="seg" style="background:#000000">'
                    '<button id="target" type="button">Sel</button></div>',
    # s125-D3's clause, guarded against THIS change: unreadable syntax still refuses BY NAME.
    "unreadable_colour_still_refuses":
        _FIX_HEAD + '<div class="seg" style="background:#000000">'
                    '<button id="target" type="button" style="color:oklab(0.5 0 0)">Sel</button></div>',
    # A sibling that paints an OPAQUE colour at opacity:0 paints NOTHING. Reading its
    # background-color and ignoring its opacity invented 12 false failures on the chart toggles.
    # Ink label on a white control, with an INK indicator hidden at opacity:0 sitting between them:
    # honouring opacity gives 18:1 (no failure); ignoring it gives 1:1 (an invented failure).
    "opacity_zero_sibling_paints_nothing":
        _FIX_HEAD + '<div class="seg"><span class="ind" style="background:#111111;opacity:0"></span>'
                    '<button id="target" type="button" style="color:#111111">Sel</button></div>',
    # The measured node is not hit-testable, so the paint stack under it cannot be observed. The
    # old ancestor walk runs and the run DECLARES it — a fallback that is counted, not hidden.
    "unhittable_node_declares_its_fallback":
        _FIX_HEAD + '<div class="seg" style="background:#000000">'
                    '<button id="target" type="button" style="pointer-events:none">Sel</button></div>',
}

def _measure_fixtures():
    """Load each fixture and return {name: MEASURE records for #target}."""
    tmp = tempfile.mkdtemp(prefix="state-contrast-selftest-")
    got = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--force-color-profile=srgb"])
        except Exception as e:                     # a gate that needs a browser cannot be proven
            raise StateContrastSelftestError(      # without one — FAILURE, never a silent skip
                f"chromium would not launch ({e!r}); this gate cannot be proven without a browser")
        try:
            for name, html in FIXTURES.items():
                path = os.path.join(tmp, name + ".html")
                open(path, "w", encoding="utf-8").write(html)
                pg = b.new_page(viewport={"width":400,"height":200})
                pg.goto("file://" + path)
                got[name] = pg.evaluate(MEASURE, pg.query_selector("#target"))
                pg.close()
        finally:
            b.close()
    return got

def selftest():
    fails = []
    ARMS_RUN = []
    def check(name, cond, detail=""):
        ARMS_RUN.append(name)
        (print(f"  ok   {name}") if cond else fails.append(f"{name}: {detail}"))

    # ---- report shape: the out[3] defect, both of its faces ----------------------------------
    fake = {"Aaa-first":  [("light","hover",{"kind":"text","text":"Eaten?","ratio":1.0,"thr":4.5})],
            "Bbb-second": [("light","hover",{"kind":"fallback","where":'span.tip "Tip"',"text":"Tip",
                                             "reason":"no on-screen box at measurement time"}),
                           ("dark","hover", {"kind":"fallback","where":'span.tip "Tip"',"text":"Tip",
                                             "reason":"no on-screen box at measurement time"})],
            "Ccc-third":  [("dark","pressed",{"kind":"icon","ratio":2.0,"thr":3.0,"ariaHidden":True})]}
    text, total, refused, fellback = render_report(fake)
    check("arm_first_heading_survives_the_headline", "## Aaa-first" in text,
          "the first snippet's heading was eaten — headline ASSIGNED, not inserted")
    check("arm_all_sections_present", text.count("\n## ") == 3, f"expected 3 sections, got {text.count(chr(10)+'## ')}")
    check("arm_headline_counts_are_right", "**1 text failure(s) across 3 snippet(s).**" in text, text.split("\n")[3])
    check("arm_fallback_is_declared_not_clean",
          fellback == 1 and "⬛ 1 UNMEASURABLE box(es)" in text and "Bbb-second — ✅ clean" not in text,
          f"a hole must be declared per snippet and must not read as clean (fellback={fellback})")
    # ---- s129-D3: the holes are NAMED, REASONED, HEADED and RE-COUNTED ------------------------
    check("arm_hole_header_states_the_count",
          "**1 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**" in text,
          "the holes count is not stated in the header — s129-D3 requires it on every write")
    check("arm_hole_line_names_box_and_reason",
          text.count(HOLE_PREFIX) == 1 and 'span.tip "Tip"' in text
          and "no on-screen box at measurement time" in text,
          "a declared hole must name the box AND carry its measured reason")
    # THE BITE THAT MATTERS: a hole that goes quiet must be a failed write, not a clean run.
    dropped = "\n".join(l for l in text.split("\n") if not l.startswith(HOLE_PREFIX))
    try:
        verify_report(dropped, 3, total, n_holes=fellback)
        check("arm_dropped_hole_bites", False, "a ⬛ line was removed from the artefact and verify_report passed")
    except StateContrastReportError as e:
        check("arm_dropped_hole_bites", "declared-hole count disagrees" in str(e), f"wrong refusal: {e}")
    # …and so must a header that under-states the count while the body still carries it.
    try:
        verify_report(text, 3, total, n_holes=fellback + 5)
        check("arm_miscounted_hole_bites", False, "counters said 6 holes, artefact carried 1, and it passed")
    except StateContrastReportError:
        check("arm_miscounted_hole_bites", True)
    # A record with NO reason must be named as unrecorded, never rendered blank or inferred.
    nore = {"Zzz": [("light","hover",{"kind":"fallback","where":"svg","text":""})]}
    ntext, _, _, nfb = render_report(nore)
    check("arm_hole_without_reason_is_named",
          nfb == 1 and HOLE_REASON_UNRECORDED in ntext,
          "a hole whose reason was not recorded must SAY so, not render an empty reason")
    check("arm_fallback_is_not_a_failure", total == 1 and "- ❌ TEXT" in text and text.count("- ❌ TEXT") == 1,
          "a fallback must not be counted as a text failure")
    try:
        zero_text, zt, _, _ = render_report({})
        check("arm_zero_snippets_does_not_crash", "**0 text failure(s) across 0 snippet(s).**" in zero_text, zero_text)
    except Exception as e:
        check("arm_zero_snippets_does_not_crash", False, f"{type(e).__name__}: {e}")
    for wrong, why in ((("n", 99, total), "snippet count"), (("t", 3, total + 7), "failure count")):
        try:
            verify_report(text, wrong[1], wrong[2]); check(f"arm_verify_report_bites_on_{why.split()[0]}", False, "no raise")
        except StateContrastReportError:
            check(f"arm_verify_report_bites_on_{why.split()[0]}", True)

    # ---- arguments: named, never guessed ------------------------------------------------------
    check("arm_selftest_flag_is_a_flag", parse_args(["--selftest"]) == ([], True))
    check("arm_bare_word_is_a_filter", parse_args(["Button"]) == (["Button"], False))
    for bad, label in ((["--wat"], "unknown_option"), (["--selftest", "Button"], "selftest_plus_filter")):
        try:
            parse_args(bad); check(f"arm_{label}_is_named", False, f"{bad} was accepted silently")
        except StateContrastArgError as e:
            check(f"arm_{label}_is_named", str(e) != "", "raised with no message")
    try:
        run(["definitely-not-a-snippet-name"]); check("arm_unmatched_filter_is_named", False, "empty audit accepted")
    except StateContrastArgError:
        check("arm_unmatched_filter_is_named", True)

    # ---- geometry: driven in a real browser, on real files ------------------------------------
    got = _measure_fixtures()
    sib = got["sibling_paint_is_seen"]
    check("arm_sibling_paint_is_seen", sib == [], f"expected no failure, got {sib}")
    wow = [r for r in got["white_on_white_still_fails"] if r["kind"] == "text"]
    check("arm_white_on_white_still_fails", len(wow) == 1 and wow[0]["ratio"] == 1,
          f"a REAL white-on-white failure was not reported: {got['white_on_white_still_fails']}")
    anc = got["ancestor_paint_is_seen"]
    check("arm_ancestor_paint_is_seen", anc == [], f"the ancestor path regressed: {anc}")
    ref = [r for r in got["unreadable_colour_still_refuses"] if r["kind"] == "refusal"]
    check("arm_unreadable_colour_still_refuses", len(ref) == 1 and ref[0]["prop"] == "color",
          f"s125-D3's refusal clause regressed: {got['unreadable_colour_still_refuses']}")
    op = got["opacity_zero_sibling_paints_nothing"]
    check("arm_opacity_zero_sibling_paints_nothing", op == [],
          f"an opacity:0 box was composited as if it painted: {op}")
    fbk = got["unhittable_node_declares_its_fallback"]
    check("arm_unhittable_node_declares_its_fallback",
          [r["kind"] for r in fbk] == ["fallback"],
          f"an un-hit-testable box must measure by ancestor walk AND declare it: {fbk}")
    # s129-D3 at the browser end: the REASON is measured there, not classified afterwards, and a
    # `pointer-events:none` box has a live sample point — so it must give the hit-stack reason,
    # never the off-screen one. Getting these two the wrong way round would be an invented reason.
    check("arm_unhittable_node_records_its_reason",
          len(fbk) == 1 and "hit stack" in (fbk[0].get("reason") or ""),
          f"the hole's reason was not measured at the browser: {fbk}")

    if fails:
        print(f"selftest FAILED — {len(fails)} bite(s):", file=sys.stderr)
        for f in fails: print(f"  ✗ {f}", file=sys.stderr)
        return 1
    print(f"selftest OK — {len(ARMS_RUN)} arms. Headline INSERTED (first heading survives, 0 snippets "
          "does not crash); artefact re-parsed against its own counters; unknown/unmatched arguments "
          "named; sibling paint seen; opacity:0 paints nothing; ancestor paint still seen; "
          "white-on-white STILL FAILS; un-hit-testable box falls back and declares it; "
          "s125-D3's refusal intact.")
    return 0

def main(argv):
    filters, want_selftest = parse_args(argv)
    if want_selftest:
        return selftest()
    res = run(filters)
    text, total, refused, fellback = render_report(res)
    open(os.path.join(HERE,"_STATE-CONTRAST-AUDIT.md"),"w",encoding="utf-8").write(text)
    print(text)
    if refused:
        print(f"StateContrastParseError: {refused} unreadable colour value(s) — see _STATE-CONTRAST-AUDIT.md",
              file=sys.stderr)
    if fellback:
        # NOT a failure: the measurement happened, by the older and weaker method. Said out loud
        # so it is countable, never inferred from silence.
        print(f"note: {fellback} background(s) took the ancestor-walk fallback (not hit-testable) "
              "— see _STATE-CONTRAST-AUDIT.md", file=sys.stderr)
    return 1 if (total or refused) else 0

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (StateContrastArgError, StateContrastReportError, StateContrastSelftestError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
