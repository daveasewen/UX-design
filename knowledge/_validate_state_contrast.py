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

s151-D1 (Dave, #151) — THE MEANING-CARRIER VOCABULARY. The law is "colour alone must not carry
meaning", NOT "every surface must clear 4.5". A composition that seats meaning on a status colour
may DECLARE its carriers: `data-carries="symbol label"` (space-separated; legal words: symbol,
label, colour). Then: (a) a declaration naming no carrier but colour — or a declared seat holding
neither a symbol nor a label — is a HARD FAIL reading "state carries meaning by colour alone";
(b) the declared symbol/label keep their normal thresholds and still ❌ if they miss; (c) the
declared seat's OWN fill reading is advisory 🟡, never ❌. ⛔ (c) applies only where a valid
declaration exists — an UNDECLARED seat behaves exactly as before, because nothing passes by
silence. Declarations are swept page-wide (the commonest real seat, Status-indicator's `.stat`,
is a passive div outside SEL) and every unreadable or unfounded one is NAMED, never defaulted.

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
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, glob, tempfile
try:
    from playwright.sync_api import sync_playwright
    _PLAYWRIGHT_IMPORT_ERROR = None   # ⚠ ALWAYS BOUND, both branches. `main()` reads it as the
    # reachability probe (see `_playwright_unreachable()`); a name that exists only on the failing
    # branch would make the probe itself raise NameError on the box where the instrument is
    # PRESENT — a measuring tool that crashes where it can measure.
except ModuleNotFoundError as _e:
    _PLAYWRIGHT_IMPORT_ERROR = repr(_e)  # `as _e` is scoped to the except block (Python 3 deletes
    # it on exit), so the closure below must capture a plain string now, not the exception object.
    # ENV-DEPENDENCE (residual ⑥, #133): with the module missing, the OLD code let this raise
    # bare at import time — an unhandled ModuleNotFoundError, traceback to stderr, rc=1. rc=1 is
    # the SAME code `main()` returns for a real measured failure (total or refused truthy), so a
    # box with no playwright installed and a box with a genuine text-contrast failure were
    # INDISTINGUISHABLE by exit code — the class of silent variance this file exists to refuse
    # everywhere else (StateContrastParseError, the unknown-hole reason, the unmatched filter).
    # Fix: defer the failure to a NAMED, attributable exception on first actual use
    # (`sync_playwright()` calls below), so `python3 _validate_state_contrast.py --selftest` on a
    # box without the module still prints a StateContrastSelftestError and exits 2 — the same
    # contract as "chromium would not launch" a few lines below, not a bare traceback at rc=1.
    # #193 — the same refusal, now in the RULED SHAPE. #133 already made this a NAMED exception
    # at rc=2 instead of a bare traceback, which was the right instinct and half the fix: rc=2 is
    # this file's "bad arguments / refuses to run" code, so a survey still could not tell "you
    # typed a wrong flag" from "this box physically cannot host the browser this gate measures
    # with". `StateContrastUnreachable` carries the same words to `_could_not_ask.EXIT` (77) and
    # a `COULD-NOT-ASK:` line, so the refusal is countable rather than merely readable.
    # ⛔ Keyed on the IMPORT FAILING, never on a runner's identity — install playwright here and
    # the refusal disappears on this very machine.
    def sync_playwright():
        raise _playwright_unreachable()

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
SEL = 'a, button, [role="radio"], [role="button"], [role="switch"], [role="tab"], [tabindex]:not([tabindex="-1"]), label, summary'


sys.path.insert(0, HERE)
import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity


class StateContrastArgError(Exception):
    """An argument this script cannot honour. NAMED — never quietly defaulted to a name-filter."""


class StateContrastReportError(Exception):
    """The rendered audit disagrees with the counters it was rendered from."""


class StateContrastSelftestError(Exception):
    """The selftest could not be RUN. That is a failure, not a skip."""


class StateContrastUnreachable(StateContrastSelftestError):
    """The INSTRUMENT is absent — a browser this box cannot host, not a verdict about the CSS.

    ⚠ Subclasses the selftest error on purpose: every existing `except` that already handled
    "could not be run" keeps working unchanged. What is new is that `__main__` recognises THIS
    one and answers it in the #193 COULD-NOT-ASK convention (exit 77 + a marked line) instead of
    rc=2, so a survey can count it as a refusal rather than a failure — and so a reader is told
    WHERE the proof actually lives (the `render` job in `.github/workflows/gates.yml`, which
    installs chromium and runs these arms BLOCKING).
    """


def _playwright_unreachable():
    """The refusal's ONE home (ADR-0017 write-once): the stub `sync_playwright()` above and the
    early probe in `main()` must say the SAME words, or a reader gets two accounts of one fact."""
    return StateContrastUnreachable(
        f"the 'playwright' module is not installed ({_PLAYWRIGHT_IMPORT_ERROR}) — this gate cannot "
        "be proven without it; run `pip install playwright && playwright install chromium`")


# ⛔ #194 — THE FORK BOMB, AND WHY THE PROBE MUST COME FIRST.
# #193 gave this gate a COULD-NOT-ASK refusal and two arms to prove it, and those arms drive the
# real consumer path: a SUBPROCESS of this very file, `--selftest`, with a planted `playwright`
# package that raises on import. Correct instinct — the exit CODE is what a consumer reads, so it
# must be driven, not asserted [[mutation-tests-the-clause-not-the-feature]]. But at #193 the
# refusal fired only on FIRST USE of the browser, and the browser arms sit BELOW these subprocess
# arms in `selftest()`. So the child reached the same two arms and spawned a grandchild — with the
# planted PYTHONPATH inherited, so IT had no playwright either, so IT spawned a great-grandchild.
# An unbounded recursion of processes, each doing all the pure work of a full selftest first.
# MEASURED on 711bfd1: `--selftest` on a playwright-less box ran 40s+ with no end in sight (killed
# by `timeout`); CI's render job — where playwright IS present, so the step was BLOCKING and green
# before d44f023 — died on `subprocess.TimeoutExpired ... timed out after 180 seconds`, the parent
# waiting on a child that was waiting on a child.
# ⇒ FIX, at the seam rather than at the symptom: `main()` PROBES reachability before it runs a
# single arm, so a playwright-less invocation refuses in milliseconds and the recursion has no
# second level — the child's whole job is now the one thing the arms actually ask it. Timeouts are
# cut to the size of the answer and an arm MEASURES the child's wall clock, so the bomb cannot
# come back unnoticed. ⚠ Keyed on the IMPORT, never on a runner's identity — install playwright
# here and both the refusal and the fast path change on this very machine.
HOLE_REASON_UNRECORDED = ("reason NOT RECORDED by the measurement that produced this record — "
                          "re-run the gate; do not infer one")

# --- s151-D1 (Dave, #151): THE MEANING-CARRIER VOCABULARY -------------------------------------
# Dave's law, verbatim from the ruling: the a11y rule is "colour alone must not carry meaning",
# NOT "every surface must clear 4.5". Clause (4): "Symbols seated on a STATUS COLOUR take the
# DEFAULT ink; the status fill's own background contrast is SECONDARY - the symbol and label
# carry the meaning."
#
# The vocabulary is a DECLARATION, never an inference. A composition that seats meaning on a
# status colour may declare its carriers:
#
#     <span class="status" data-carries="symbol label"> … </span>
#
# THREE CLAUSES, and they are deliberately asymmetric:
#   (a) REDUNDANCY — a declaration must name at least one NON-COLOUR carrier. `data-carries="colour"`,
#       or a declared seat carrying neither a symbol nor a label, is a HARD FAIL. This clause can
#       only ever ADD failures; it never waives one.
#   (b) CARRIER LEGIBILITY — the symbol and label keep their normal thresholds (text 4.5, icon 3.0)
#       against THEIR backgrounds. A declaration buys the SEAT nothing for its carriers: an
#       illegible label is still ❌. This is the clause that stops the vocabulary becoming a waiver.
#   (c) SEAT DEMOTION — the seat FILL's own reading against what is painted beneath it is ADVISORY
#       🟡, never ❌ — but ONLY where a valid declaration exists. An UNDECLARED seat behaves exactly
#       as it did before this change: nothing passes by silence.
#
# ⛔ NOTHING IS GUESSED. An unknown carrier word, an empty declaration, or a declaration whose
# claim disagrees with the DOM (says `symbol`, contains no svg) is a NAMED failure — never
# defaulted to "probably fine", never silently dropped [[measuring-tool-must-not-guess]].
LEGAL_CARRIERS = ("symbol", "label", "colour")

# The verbatim reason the gate must emit for clause (a). Quoted here ONCE so the message, the
# selftest and this comment cannot drift apart [[gate-must-quote-what-it-forbids]].
CARRIER_COLOUR_ALONE = "state carries meaning by colour alone"

# What the gate FORBIDS, quoted in every message it emits under this vocabulary. A gate that
# names a violation without quoting the rule it is enforcing makes the author guess.
CARRIER_RULE_QUOTED = (
    'the rule being enforced, quoted: "colour alone must not carry meaning" (s151-D1, Dave, #151) '
    '— a `data-carries` declaration must name at least one of ' + ", ".join(
        repr(c) for c in LEGAL_CARRIERS if c != "colour") +
    ", and the composition must actually contain it. This gate reports the measurement; it does "
    "not prescribe which carrier you add.")


class StateContrastCarrierError(Exception):
    """A `data-carries` declaration this gate cannot READ. NAMED — never defaulted."""


def classify_carriers(raw):
    """PURE. Parse a `data-carries` attribute value into (carriers, non_colour).

    Raises StateContrastCarrierError on anything unreadable — an empty declaration or an
    unknown word. It NEVER returns a guess: a declaration the gate cannot read is not a
    declaration, and the alternative (defaulting to "no carriers" or to "all carriers") is
    exactly the silent-default class this file exists to refuse.
    """
    if raw is None:
        raise StateContrastCarrierError("no `data-carries` attribute — nothing to classify")
    toks = [t for t in str(raw).split() if t]
    if not toks:
        raise StateContrastCarrierError(
            f"empty `data-carries` declaration ({raw!r}) — an empty declaration is not a "
            f"statement that there are no carriers, it is an unreadable one. " + CARRIER_RULE_QUOTED)
    bad = [t for t in toks if t not in LEGAL_CARRIERS]
    if bad:
        raise StateContrastCarrierError(
            f"unknown carrier word(s) {', '.join(repr(b) for b in bad)} in `data-carries`="
            f"{raw!r} — legal carriers are {', '.join(repr(c) for c in LEGAL_CARRIERS)}. "
            + CARRIER_RULE_QUOTED)
    seen = []
    for t in toks:
        if t not in seen:
            seen.append(t)
    return seen, [t for t in seen if t != "colour"]


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
  const ratioOf=(a,b)=>{const L1=lum(a),L2=lum(b),hi=Math.max(L1,L2),lo=Math.min(L1,L2);return (hi+0.05)/(lo+0.05)};
  const ratio=ratioOf;
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
  // `skipSelf` (s151-D1): composite the paint stack BENEATH the node, excluding the node's own
  // background. That is the ONLY way to read a status SEAT's fill against what it sits on — the
  // normal call includes the seat itself and would measure the fill against itself.
  function effBg(node, skipSelf){
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
            // ⚠ the DECLARED fallback stays byte-for-byte the pre-2026-08-07 walk for the normal
            // call (`skipSelf` falsy) — that identity is what makes its delta attributable. Only
            // the new seat-fill call starts the walk at the parent.
            return ancestorBg(skipSelf?(node.parentElement||node):node);}
    let R=0,G=0,B=0,rem=1;                          // src-over compositing, top-down from the node
    for(let k=i+(skipSelf?1:0);k<stack.length&&rem>0.0005;k++){
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
        // s151-D1 clause (b): a record INSIDE a declared seat is a CARRIER's legibility. Its
        // threshold does not move — the tag exists so the report can say which clause applies.
        const st=n.closest?n.closest('[data-carries]'):null;
        if(r<thr) out.push({kind:'text',text:n.textContent.trim().slice(0,32),ratio:Math.round(r*100)/100,thr,seat:st?desc(st):null});}
    }
    if(n.tagName.toLowerCase()==='svg'){
      const fc=(cs.fill&&cs.fill!=='none')?cs.fill:cs.color, fg=parse(fc,'fill',n);
      if(fg){const bg=effBg(n),r=ratio(fg,bg); if(r<3.0) out.push({kind:'icon',ariaHidden:!!n.closest('[aria-hidden="true"]'),ratio:Math.round(r*100)/100,thr:3.0});}
      // s134-D1 (Dave, #134): "we only care about the glyph having enough contrast" / "the glyph
      // is all we care about ... it is always accompanied by a label". The internal MARK (an inner
      // path/use painted fill:var(--mark), a colour distinct from the shape's own fill) is the SOLE
      // GATED roundel leg — held to the small-text 4.5 threshold, as a real TEXT failure (never
      // waived). The shape-on-surface leg above (kind:'icon', 3.0) stays WARN-only, as it always
      // has — this file already never failed the gate on it, so s134-D1 needed no change there.
      // ⛔ s152-D1 (Dave, #152) — THE SHAPE FILL MUST ACTUALLY BE PAINTED BEFORE IT CAN BE A
      // BACKDROP. An `<svg>` element paints NO shape of its own: its `fill` is an INHERITED value
      // that descendant shapes may or may not wear. With no explicit fill it computes to the
      // UA-default BLACK — a colour nothing on screen is wearing — and #152 measured that phantom
      // as a 1.662 mark "failure" on the chip star. Light "passed" at 21:1 against the SAME
      // phantom, which is why it never read as an instrument fault [[attribute-the-diff]].
      // The mark leg therefore runs ONLY when some descendant SHAPE actually paints that fill.
      // Otherwise the comparison is SKIPPED — and the skip is DECLARED, never silent: a gate that
      // quietly stops reporting is indistinguishable from a gate that was fixed
      // [[enactment-register-adr-0016]].
      // CLASS, not instance: any <svg> with no explicit fill whose inner path paints currentColor.
      // ⚠ The presence test compares COMPUTED STRINGS, never parse(): probing every descendant
      // through parse() would mint refusals this change was not ruled to create, and the delta
      // would stop being attributable. Both sides come from getComputedStyle, so both are
      // normalised the same way and the comparison is exact.
      const shapeFillStr=(cs.fill&&cs.fill!=='none')?cs.fill:null;
      let bodyPaints=false;
      if(shapeFillStr){
        for(const sh of n.querySelectorAll('path,circle,rect,ellipse,line,polyline,polygon,use,text,tspan')){
          if(sh.closest('defs,clipPath,mask,symbol,marker,pattern')) continue;   // not rendered in place
          const shs=getComputedStyle(sh);
          if(shs.visibility==='hidden'||shs.display==='none'||parseFloat(shs.opacity)===0) continue;
          if(shs.fill===shapeFillStr){bodyPaints=true;break;}
        }
      }
      if(fg&&!bodyPaints){
        out.push({kind:'markskip',where:desc(n),fill:shapeFillStr,
          reason:(shapeFillStr
            ?'no descendant shape paints the fill this svg declares, so it is not a surface any mark sits on'
            :'the svg has no painted fill at all (fill is absent or none), so there is no shape for a mark to sit on')});
      }
      if(fg&&bodyPaints){
        for(const inner of n.querySelectorAll('*')){
          const ics=getComputedStyle(inner);
          const ifc=(ics.fill&&ics.fill!=='none')?ics.fill:null;
          if(!ifc) continue;
          const mfg=parse(ifc,'fill',inner);           // unreadable mark colour: refuse() propagates,
          if(!mfg) continue;                            // caught by the named-refusal path below (unchanged)
          if(mfg[0]===fg[0]&&mfg[1]===fg[1]&&mfg[2]===fg[2]) continue;  // same colour as the shape: not a distinct mark
          const mr=ratio(mfg,fg);
          if(mr<4.5) out.push({kind:'text',text:'[MARK] '+desc(inner),ratio:Math.round(mr*100)/100,thr:4.5});
        }
      }
    }
   }catch(e){
    // A refusal is a RESULT, not a skip: it is carried out as a first-class record, counted,
    // and it fails the gate. Anything else is a real bug and is re-thrown, loudly.
    if(e&&e.name==='StateContrastParseError'){out.push({kind:'refusal',prop:e.prop,value:e.value,where:e.where,text:(n.textContent||'').trim().slice(0,32)});continue}
    throw e;
   }
  }
  // ---- s151-D1: STATUS-SEAT DECLARATIONS -----------------------------------------------------
  // The browser reports FACTS ONLY — the raw attribute, whether a symbol/label is actually
  // present, and the measured fill-vs-beneath ratio. The PREDICATE lives in Python
  // (`classify_carriers`), in one place, so the rule cannot drift between two implementations
  // the way a mirrored word-list would. Nothing here decides pass or fail.
  const seats=[el, ...el.querySelectorAll('*')].filter(n=>n.nodeType===1&&n.hasAttribute&&n.hasAttribute('data-carries'));
  for(const s of seats){
   try{
    const scs=getComputedStyle(s);
    if(scs.visibility==='hidden'||scs.display==='none') continue;
    const own=parse(scs.backgroundColor,'background-color',s);
    const alpha=own?(own.length===4?own[3]:1):0;
    let ratio=null, why=null;
    if(!own||!(alpha>0)){
      why='the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote';
    }else{
      const under=effBg(s,true);
      const solid=[Math.round(own[0]*alpha+under[0]*(1-alpha)),
                   Math.round(own[1]*alpha+under[1]*(1-alpha)),
                   Math.round(own[2]*alpha+under[2]*(1-alpha))];
      ratio=Math.round(ratioOf(solid,under)*100)/100;
    }
    out.push({kind:'seatdecl', where:desc(s), raw:s.getAttribute('data-carries'),
              hasSymbol:!!s.querySelector('svg,[data-symbol]'),
              hasLabel:(s.textContent||'').trim().length>0,
              ratio:ratio, reason:why});
   }catch(e){
    if(e&&e.name==='StateContrastParseError'){out.push({kind:'refusal',prop:e.prop,value:e.value,where:e.where,text:''});continue}
    throw e;
   }
  }
  return out;
}
"""

def audit_page(pg, theme, sink):
    # ---- s151-D1: SWEEP THE WHOLE PAGE FOR SEAT DECLARATIONS, ONCE PER THEME ------------------
    # ⚠ FOUND BY DRIVING IT, not by reading it. The seat pass inside MEASURE only ever sees the
    # subtree of an element in SEL — and the commonest real status seat in this canon
    # (Status-indicator's `.stat` = dot + label) is a PASSIVE div that SEL does not select. A
    # declaration on it would have been silently invisible, which is the exact failure mode this
    # vocabulary exists to prevent: a clause that cannot see its subject cannot fail
    # [[instrument-without-a-consumer]]. The sweep runs on document.body in the RESTING state and
    # emits seat records ONLY — it does not widen this gate's text/icon scope, which stays
    # hover/pressed by design. Seats inside driven elements are still measured under those states
    # too, by MEASURE; the report de-duplicates on (theme, state, kind, where, ratio).
    try:
        for fl in pg.evaluate(MEASURE, pg.query_selector("body")):
            # SEATS ONLY. The sweep deliberately drops the text/icon/refusal records it also
            # produces: those would be RESTING-state findings, and this gate's scope is the DRIVEN
            # states. Widening the baseline silently, in the same change that adds a vocabulary,
            # would make the vocabulary's before/after delta unattributable [[attribute-the-diff]].
            if fl["kind"] == "seatdecl":
                sink.append((theme, "base", fl))
    except Exception as e:
        # A sweep that cannot run is NAMED, never a silent skip.
        raise StateContrastCarrierError(
            f"the s151-D1 seat sweep could not run on this page ({e!r}) — refusing to report a "
            f"page as carrying no declarations when the sweep did not happen")
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
# s151-D1 — the carrier clauses get the same treatment as the holes: a STATED figure, re-parsed
# out of the artefact and asserted against the body on every write. A clause whose count can go
# quiet is a clause that cannot be trusted to have run [[instrument-without-a-consumer]].
CARRIER_FAIL_PREFIX = "- ❌ CARRIER"
CARRIER_ERR_PREFIX = "- ⛔ StateContrastCarrierError"
# s152-D1 (Dave, #152) — a mark comparison that was SKIPPED is written into the artefact under its
# own prefix. Deliberately NOT one of the counted prefixes above: a skip is neither a failure nor a
# hole, and folding it into either would move a count Dave ratified. It is an advisory receipt, and
# its whole job is that a reader can see the leg did not run [[enactment-register-adr-0016]].
MARKSKIP_PREFIX = "- 🟡 MARK SKIP (declared, s152-D1)"
SEAT_PREFIX = "- 🟡 SEAT (declared, advisory)"
CARRIERS_RE = re.compile(r"^\*\*(\d+) CARRIER failure\(s\) — declarations that carry meaning by "
                         r"colour alone, plus declarations this gate could not READ \(s151-D1\)\.\*\*$",
                         re.M)


def carrier_lines(theme, state, fl):
    """Turn ONE browser-reported `seatdecl` fact-record into its report line(s) + a verdict.

    Returns (kind, [lines]) where kind is 'fail' (clause (a) or an unreadable declaration —
    both count against the gate) or 'seat' (a valid declaration; its fill reading is ADVISORY).

    The PREDICATE is here and only here. The browser reported facts; nothing was decided there.
    """
    where = fl.get("where") or "(element identity NOT RECORDED — re-run the gate)"
    try:
        carriers, non_colour = classify_carriers(fl.get("raw"))
    except StateContrastCarrierError as e:
        return "fail", [f"{CARRIER_ERR_PREFIX} [{theme}/{state}] on {where} — {e}"]
    # Clause (a), face 1: the declaration itself names no non-colour carrier.
    if not non_colour:
        return "fail", [
            f'{CARRIER_FAIL_PREFIX} [{theme}/{state}] {CARRIER_COLOUR_ALONE} — {where} declares '
            f'`data-carries="{fl.get("raw")}"`, which names no carrier other than colour. '
            f'{CARRIER_RULE_QUOTED}']
    # Clause (a), face 2: the declaration claims a carrier the composition does not contain, or
    # the seat contains NEITHER a symbol NOR a label. A declaration is a claim about the DOM, and
    # an unchecked claim is how a vocabulary becomes a rubber stamp.
    missing = [c for c in non_colour
               if (c == "symbol" and not fl.get("hasSymbol")) or (c == "label" and not fl.get("hasLabel"))]
    if missing:
        return "fail", [
            f'{CARRIER_FAIL_PREFIX} [{theme}/{state}] {CARRIER_COLOUR_ALONE} — {where} declares '
            f'`data-carries="{fl.get("raw")}"` but the composition contains no '
            f'{" and no ".join(missing)} '
            f'(measured at the browser: symbol present={bool(fl.get("hasSymbol"))}, '
            f'label present={bool(fl.get("hasLabel"))}). {CARRIER_RULE_QUOTED}']
    if not (fl.get("hasSymbol") or fl.get("hasLabel")):
        return "fail", [
            f'{CARRIER_FAIL_PREFIX} [{theme}/{state}] {CARRIER_COLOUR_ALONE} — {where} is a '
            f'status-seat composition carrying neither a symbol nor a label. {CARRIER_RULE_QUOTED}']
    # Clause (c): valid declaration -> the SEAT's own fill reading is advisory, never ❌.
    if fl.get("ratio") is None:
        return "seat", [f'{SEAT_PREFIX} [{theme}/{state}] {where} — carriers `{fl.get("raw")}` — '
                        f'no fill reading: {fl.get("reason") or HOLE_REASON_UNRECORDED}']
    return "seat", [
        f'{SEAT_PREFIX} [{theme}/{state}] {where} — carriers `{fl.get("raw")}` — the seat fill '
        f'measures {fl["ratio"]}:1 against what is painted beneath it. ADVISORY, never a failure: '
        f'under s151-D1 the status fill\'s own background contrast is SECONDARY because the symbol '
        f'and label carry the meaning. The measurement is reported, not a prescription — this gate '
        f'does not say what the value should be.']


def verify_report(text, n_snippets, total_text, n_holes=None, n_carriers=None):
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
    # s151-D1 — same contract for the carrier clauses.
    if n_carriers is not None:
        cl = [l for l in lines if l.startswith(CARRIER_FAIL_PREFIX) or l.startswith(CARRIER_ERR_PREFIX)]
        mc = CARRIERS_RE.search(text)
        if not mc:
            raise StateContrastReportError(
                "the audit carries no CARRIER failure(s) header line — s151-D1 requires the count "
                "to be stated on every write, including when it is zero")
        if int(mc.group(1)) != n_carriers or len(cl) != n_carriers:
            raise StateContrastReportError(
                f"carrier-failure count disagrees — header says {int(mc.group(1))}, counters say "
                f"{n_carriers}, artefact carries {len(cl)} carrier line(s). A carrier clause that "
                f"goes quiet reads as a measured pass (s151-D1)")

def render_report(res):
    """Render the audit markdown from a results dict.

    PURE — no browser, no IO — so --selftest can bite the report's own arithmetic without
    rendering anything. Returns (text, total_text, refused, ancestor_fallbacks, carrier_fails).
    """
    out = ["# State-contrast audit — rendered hover / pressed states (light + dark)",
           "*Drives each interactive element's real hover/pressed states and measures computed foreground "
           "vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). "
           "Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*",
           ""]
    total = 0; refused = 0; fellback = 0; carrier_fails = 0
    for name in sorted(res):
        seen=set(); uniq=[]
        for theme,state,fl in res[name]:
            k=(theme,state,fl["kind"],fl.get("text"),fl.get("ratio"),fl.get("prop"),fl.get("value"),fl.get("where"))
            if k in seen: continue
            seen.add(k); uniq.append((theme,state,fl))
        tf=[u for u in uniq if u[2]["kind"]=="text"]; iw=[u for u in uniq if u[2]["kind"]=="icon"]
        rf=[u for u in uniq if u[2]["kind"]=="refusal"]; fb=_fallback_holes(uniq)
        ms=[u for u in uniq if u[2]["kind"]=="markskip"]      # s152-D1 — declared, never silent
        # s151-D1 — classify the seat declarations HERE, in Python, from the browser's facts.
        cfail=[]; cseat=[]
        for theme,state,fl in uniq:
            if fl["kind"]!="seatdecl": continue
            verdict, lines = carrier_lines(theme, state, fl)
            (cfail if verdict=="fail" else cseat).extend(lines)
        total += len(tf); refused += len(rf); fellback += len(fb); carrier_fails += len(cfail)
        bits=[]
        if tf: bits.append(f"❌ {len(tf)} TEXT fail(s)")
        # A carrier failure is a HARD fail — the vocabulary can only ever ADD failures (s151-D1).
        if cfail: bits.append(f"❌ {len(cfail)} CARRIER fail(s)")
        if cseat: bits.append(f"🟡 {len(cseat)} declared seat(s)")
        # a refusal is UNMEASURED, so this snippet may NOT be reported as clean
        if rf: bits.append(f"⛔ {len(rf)} PARSE REFUSAL(s) — UNMEASURED")
        if iw: bits.append(f"{len(iw)} icon warn(s)")
        if ms: bits.append(f"🟡 {len(ms)} MARK SKIP(s)")
        # ✅ s129-D3: a NAMED HOLE, not a footnote. The snippet may not read as fully measured.
        if fb: bits.append(f"⬛ {len(fb)} UNMEASURABLE box(es)")
        out.append(f"## {name} — {' · '.join(bits) if bits else '✅ clean'}")
        for theme,state,fl in tf:
            # clause (b): a carrier keeps its threshold. Say WHICH clause is speaking, so a reader
            # cannot mistake a carrier-legibility failure for a demotable seat-fill reading.
            tag = (f" [CARRIER LEGIBILITY, s151-D1 clause (b) — inside declared seat {fl['seat']}; "
                   f"the threshold does NOT move for a carrier]" if fl.get("seat") else "")
            out.append(f"- ❌ TEXT [{theme}/{state}] {fl['ratio']}:1 (need {fl['thr']}) — \"{fl['text']}\"{tag}")
        out.extend(cfail)
        for theme,state,fl in rf: out.append(f"- ⛔ StateContrastParseError [{theme}/{state}] cannot parse {fl['prop']}: `{fl['value']}` on {fl['where']}")
        for theme,state,fl in iw: out.append(f"- 🟡 icon [{theme}/{state}] {fl['ratio']}:1 (need 3.0){' (decorative)' if fl.get('ariaHidden') else ''}")
        # s152-D1 — a SKIPPED mark comparison is WRITTEN DOWN. It is not a measured pass; the
        # reader is told which shape was skipped and why, so the skip can be argued with.
        for theme,state,fl in ms:
            out.append(MARKSKIP_PREFIX + f" [{theme}/{state}] {fl['where']} — {fl['reason']} "
                       f"(declared fill: `{fl['fill'] or 'none'}`). The mark leg did NOT run on "
                       "this shape, and this line is the receipt.")
        for w, why in fb:
            out.append(HOLE_PREFIX + f" — {w} — {why}. The paint stack under it cannot be "
                       "observed, so the pre-2026-08-07 ancestor-only walk ran instead: any "
                       "ratio reported over this box is that weaker measurement, NOT a hit-stack "
                       "one. Nothing is invented and nothing is waived (s129-D3).")
        out.extend(cseat)
        out.append("")
    # INSERT the headline — do NOT assign it. `out[3] = …` overwrote whatever already occupied
    # index 3, which was the FIRST snippet's heading (Accordion, eaten; the audit then claimed 38
    # sections and carried 37), and raised IndexError outright when no snippet was in scope,
    # because index 3 only exists once a section has been appended. A summary is a NEW line.
    out[3:3] = [f"**{total} text failure(s) across {len(res)} snippet(s).**", "",
                f"**{fellback} DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE "
                f"by name (s129-D3).**", "",
                f"**{carrier_fails} CARRIER failure(s) — declarations that carry meaning by "
                f"colour alone, plus declarations this gate could not READ (s151-D1).**", ""]
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
    out += ["---",
            "**s151-D1 — THE MEANING-CARRIER VOCABULARY (Dave, #151).** The rule this gate "
            f'enforces, quoted: "colour alone must not carry meaning" — NOT "every surface must '
            'clear 4.5". A composition may declare `data-carries="symbol label"` on the element '
            f'that seats meaning on a status colour; legal carriers are '
            f'{", ".join("`"+c+"`" for c in LEGAL_CARRIERS)}. Three clauses: (a) REDUNDANCY — a '
            f'declaration naming no carrier other than colour, or a declared seat containing '
            f'neither a symbol nor a label, is a HARD FAIL reading "{CARRIER_COLOUR_ALONE}"; '
            "(b) CARRIER LEGIBILITY — the symbol and label keep their normal thresholds (text 4.5, "
            "icon 3.0) against THEIR backgrounds and still ❌ if they miss; (c) SEAT DEMOTION — the "
            "declared seat's own fill reading is ADVISORY 🟡, never ❌. ⛔ Clause (c) applies ONLY "
            "where a valid declaration exists: an UNDECLARED seat behaves exactly as it did before "
            "this change, because nothing may pass by silence. An unreadable declaration — empty, "
            "or naming a word outside the legal set, or claiming a symbol/label the DOM does not "
            "contain — is a NAMED failure, never a default. The count above is RE-READ off this "
            "artefact and asserted equal to the carrier lines in the body on every write.",
            ""]
    text = "\n".join(out)
    verify_report(text, len(res), total, n_holes=fellback, n_carriers=carrier_fails)
    return text, total, refused, fellback, carrier_fails

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
    # ---- s151-D1 meaning-carrier fixtures ------------------------------------------------------
    # A VALID declaration: a status seat painted a low-contrast amber on white, carrying BOTH a
    # symbol and a label. The seat fill measures ~1.5:1 against the page — under s151-D1 that
    # reading is ADVISORY, because the symbol and the label carry the meaning.
    "carrier_valid_declaration_demotes_the_fill":
        _FIX_HEAD + '<div class="seg"><span id="target" class="seat" data-carries="symbol label" '
                    'style="display:inline-flex;align-items:center;gap:6px;background:#FFC107;color:#111111">'
                    '<svg viewBox="0 0 16 16" width="16" height="16" style="fill:#111111">'
                    '<path d="M2 8h12"/></svg>Pending</span></div>',
    # COLOUR ALONE: the same seat, declaring only colour, with no symbol and no label. HARD FAIL.
    "carrier_colour_only_hard_fails":
        _FIX_HEAD + '<div class="seg"><span id="target" class="seat" data-carries="colour" '
                    'style="display:inline-block;width:60px;height:20px;background:#FFC107"></span></div>',
    # The load-bearing NEGATIVE arm for clause (b): a VALID declaration whose LABEL is illegible.
    # Without this arm, "demote the fill" and "stop reporting anything" are indistinguishable.
    "carrier_declared_but_label_still_fails":
        _FIX_HEAD + '<div class="seg"><span id="target" class="seat" data-carries="symbol label" '
                    'style="display:inline-flex;align-items:center;gap:6px;background:#FFC107;color:#FFD54F">'
                    '<svg viewBox="0 0 16 16" width="16" height="16" style="fill:#111111">'
                    '<path d="M2 8h12"/></svg>Pending</span></div>',
    # A declaration this gate CANNOT READ must be a NAMED failure, never a default.
    "carrier_unknown_word_is_named":
        _FIX_HEAD + '<div class="seg"><span id="target" class="seat" data-carries="symbol vibes" '
                    'style="display:inline-block;background:#FFC107;color:#111111">Pending</span></div>',
    # A declaration that CLAIMS a symbol the DOM does not contain is a claim, not a fact.
    "carrier_claimed_symbol_absent_is_named":
        _FIX_HEAD + '<div class="seg"><span id="target" class="seat" data-carries="symbol" '
                    'style="display:inline-block;background:#FFC107;color:#111111">Pending</span></div>',
    # THE SILENCE ARM: the identical seat with NO declaration must behave exactly as before —
    # no seat record at all, and whatever text/icon failures it had, unchanged.
    "carrier_undeclared_seat_is_unchanged":
        _FIX_HEAD + '<div class="seg"><span id="target" class="seat" '
                    'style="display:inline-flex;align-items:center;gap:6px;background:#FFC107;color:#FFD54F">'
                    '<svg viewBox="0 0 16 16" width="16" height="16" style="fill:#111111">'
                    '<path d="M2 8h12"/></svg>Pending</span></div>',
    # ---- s152-D1 fixtures: the MARK leg must not measure a phantom -----------------------------
    # THE CLASS #152 MEASURED, in miniature: an <svg> with NO fill attribute whose inner path
    # paints with currentColor. The svg's computed fill is the UA-default BLACK — a colour nothing
    # on screen wears — and the old leg compared #333 against it and reported 1.662 as a failure.
    "mark_phantom_fill_is_skipped":
        _FIX_HEAD + '<div class="seg"><span id="target" style="display:inline-flex;'
                    'background:#ffffff;color:#333333">'
                    '<svg viewBox="0 0 16 16" width="16" height="16">'
                    '<path fill="currentColor" d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z"/>'
                    '</svg></span></div>',
    # THE DISCRIMINATING ARM'S fixture — a REAL black roundel. Its shape fill computes to exactly
    # the same rgb(0,0,0) as the phantom above, but a descendant ACTUALLY WEARS IT. The mark leg
    # must still run and still fail here. Without this fixture, "skip the phantom" and "skip
    # everything black" are indistinguishable, and so are "fix it" and "delete it".
    "mark_real_black_roundel_still_fails":
        _FIX_HEAD + '<div class="seg"><span id="target" style="display:inline-flex;background:#ffffff">'
                    '<svg viewBox="0 0 16 16" width="16" height="16" fill="#000000">'
                    '<circle cx="8" cy="8" r="8"/>'
                    '<path fill="#333333" d="M4 7h8v2H4z"/></svg></span></div>',
    # A shape inside <defs> is NOT rendered in place, so it cannot make a fill painted. Without the
    # non-rendered-container clause this fixture would look identical to a real roundel.
    "mark_body_only_in_defs_is_skipped":
        _FIX_HEAD + '<div class="seg"><span id="target" style="display:inline-flex;background:#ffffff">'
                    '<svg viewBox="0 0 16 16" width="16" height="16" fill="#000000">'
                    '<defs><circle cx="8" cy="8" r="8"/></defs>'
                    '<path fill="#333333" d="M4 7h8v2H4z"/></svg></span></div>',
}

def _measure_fixtures(script=MEASURE, only=None):
    """Load each fixture and return {name: MEASURE records for #target}.

    `script` exists SOLELY so the s152-D1 mutation control can drive a MEASURE whose guard has been
    cut out and demand the defect COME BACK; `only` keeps that second browser launch down to the
    single fixture that needs it. Both default to the real run, so every existing call is unchanged
    and the delta stays attributable [[attribute-the-diff]].
    """
    tmp = tempfile.mkdtemp(prefix="state-contrast-selftest-")
    got = {}
    items = [(k, v) for k, v in FIXTURES.items() if only is None or k in only]
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--force-color-profile=srgb"])
        except Exception as e:                     # a gate that needs a browser cannot be proven
            raise StateContrastSelftestError(      # without one — FAILURE, never a silent skip
                f"chromium would not launch ({e!r}); this gate cannot be proven without a browser")
        try:
            for name, html in items:
                path = os.path.join(tmp, name + ".html")
                open(path, "w", encoding="utf-8").write(html)
                pg = b.new_page(viewport={"width":400,"height":200})
                pg.goto("file://" + path)
                got[name] = pg.evaluate(script, pg.query_selector("#target"))
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
    text, total, refused, fellback, cfails = render_report(fake)
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
    ntext, _, _, nfb, _ = render_report(nore)
    check("arm_hole_without_reason_is_named",
          nfb == 1 and HOLE_REASON_UNRECORDED in ntext,
          "a hole whose reason was not recorded must SAY so, not render an empty reason")
    check("arm_fallback_is_not_a_failure", total == 1 and "- ❌ TEXT" in text and text.count("- ❌ TEXT") == 1,
          "a fallback must not be counted as a text failure")
    try:
        zero_text, zt, _, _, _ = render_report({})
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

    # ---- #193: THE COULD-NOT-ASK PATH, DRIVEN, BOTH DIRECTIONS -------------------------------
    # ⚠ These arms run the script AS A SUBPROCESS with a `playwright` package that raises on
    # import, because the refusal lives in the `__main__` handler and an import cannot see it —
    # and because the exit CODE is the thing consumers read [[mutation-tests-the-clause-not-the-
    # feature]]. Driving the real absence (rather than asserting about it) is what makes this a
    # test: this very process HAS playwright, so nothing here is proven by the environment.
    import subprocess as _sp
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _pkg = os.path.join(_td, "playwright")
        os.makedirs(_pkg)
        with open(os.path.join(_pkg, "__init__.py"), "w", encoding="utf-8") as _f:
            _f.write("raise ModuleNotFoundError(\"No module named 'playwright' (planted)\")\n")
        _env = dict(os.environ, PYTHONPATH=_td + os.pathsep + os.environ.get("PYTHONPATH", ""))
        # ⚠ #194: TIMEOUT CUT TO THE SIZE OF THE ANSWER. A refusal is a probe and an exit; 30s is
        # already two orders of magnitude of slack. The old 180s was large enough to hide the
        # recursion as a HANG rather than surface it as a bite — and in CI it became the failure.
        import time as _time
        _t0 = _time.monotonic()
        _blind = _sp.run([sys.executable, os.path.abspath(__file__), "--selftest"],
                         capture_output=True, text=True, env=_env, cwd=HERE, timeout=30)
        _blind_secs = _time.monotonic() - _t0
        _out = _blind.stdout + _blind.stderr
        # ★ THE FORK-BOMB GUARD, MEASURED not assumed. The refusal's whole contract is that it
        # fires BEFORE the expensive work; a child that took seconds of browser time to say "I
        # have no browser" would be honest and still wrong, and it is exactly what recursing
        # looked like. A wall clock is the only thing that can tell those two apart from here.
        check("arm_refusal_fires_before_any_expensive_work", _blind_secs < 10.0,
              f"the playwright-less child took {_blind_secs:.1f}s to refuse — it is doing work "
              f"before the probe (at #193 it re-entered --selftest recursively and never ended)")
        check("arm_no_playwright_is_a_refusal_not_a_failure", _blind.returncode == cna.EXIT,
              f"expected exit {cna.EXIT} (COULD-NOT-ASK), got {_blind.returncode}: {_out[-300:]}")
        check("arm_refusal_is_machine_readable_and_names_its_reason",
              (cna.reason_in(_out) or "") .startswith(cna.MARKER) and "playwright" in _out,
              f"no marked reason line in: {_out[-300:]}")
        check("arm_refusal_says_where_the_proof_lives", "render" in _out and "gates.yml" in _out,
              "a refusal that cannot point at the job that DOES prove this is a shrug")
        # ★ THE OTHER DIRECTION — the refusal must not swallow every other verdict on the same
        # box. With the instrument STILL absent, a bad argument is an ARGUMENT error (2), not a
        # could-not-ask: the refusal is keyed on the missing import, nothing wider.
        _bad = _sp.run([sys.executable, os.path.abspath(__file__), "--wat"],
                       capture_output=True, text=True, env=_env, cwd=HERE, timeout=30)
        check("arm_refusal_is_scoped_to_the_missing_import", _bad.returncode == 2,
              f"a bad flag returned {_bad.returncode} on a playwright-less box; the refusal has "
              f"widened into a catch-all")

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

    # ---- s151-D1: THE MEANING-CARRIER VOCABULARY ----------------------------------------------
    # (i) the PURE predicate, in isolation
    check("arm_carriers_parse_valid", classify_carriers("symbol label") == (["symbol","label"],["symbol","label"]))
    check("arm_carriers_colour_only_has_no_non_colour", classify_carriers("colour") == (["colour"], []))
    for bad, label in (("", "empty"), ("   ", "whitespace"), ("symbol vibes", "unknown_word"), (None, "absent")):
        try:
            classify_carriers(bad); check(f"arm_carriers_{label}_is_named", False, f"{bad!r} accepted silently")
        except StateContrastCarrierError as e:
            check(f"arm_carriers_{label}_is_named", str(e) != "", "raised with no message")
    # the message must QUOTE what it forbids, not merely name the offender
    try:
        classify_carriers("vibes")
    except StateContrastCarrierError as e:
        check("arm_carrier_error_quotes_the_rule", "colour alone must not carry meaning" in str(e), str(e))

    # (ii) the LINE-LEVEL verdicts, driven on constructed fact-records
    def seat_fact(**kw):
        f = {"kind":"seatdecl","where":'span.seat "Pending"',"raw":"symbol label",
             "hasSymbol":True,"hasLabel":True,"ratio":1.52,"reason":None}
        f.update(kw); return f
    v_ok, l_ok = carrier_lines("light","hover", seat_fact())
    check("arm_valid_declaration_is_advisory", v_ok == "seat" and l_ok[0].startswith(SEAT_PREFIX)
          and "1.52:1" in l_ok[0], f"{v_ok} / {l_ok}")
    check("arm_advisory_reports_the_measurement_not_a_region",
          "1.52:1" in l_ok[0] and "should be" in l_ok[0] and "does not say what the value should be" in l_ok[0],
          "the advisory must REPORT the measurement and explicitly not prescribe a region")
    v_c, l_c = carrier_lines("light","hover", seat_fact(raw="colour", hasSymbol=False, hasLabel=False))
    check("arm_colour_only_is_a_hard_fail", v_c == "fail" and l_c[0].startswith(CARRIER_FAIL_PREFIX)
          and CARRIER_COLOUR_ALONE in l_c[0] and 'span.seat "Pending"' in l_c[0],
          f"the hard fail must carry the verbatim reason AND the element identity: {l_c}")
    # ⚠ THE ARM THAT MUTATION TESTING ADDED. The arm above cannot discriminate clause (a) face 1
    # from face 3: its fixture carries neither a symbol nor a label, so disabling the "names no
    # non-colour carrier" test leaves the "contains neither" test to catch it and the selftest
    # stays green. A mutant SURVIVED that exact edit. This fixture HAS both carriers and declares
    # only `colour` — the only shape that isolates face 1 [[a-new-tier-silently-bypasses-its-tests]].
    v_c1, l_c1 = carrier_lines("light","hover", seat_fact(raw="colour", hasSymbol=True, hasLabel=True))
    check("arm_colour_only_declaration_fails_even_when_carriers_exist",
          v_c1 == "fail" and CARRIER_COLOUR_ALONE in l_c1[0] and "names no carrier other than colour" in l_c1[0],
          f"declaring only `colour` must fail on the DECLARATION, whatever the DOM contains: {l_c1}")
    v_m, l_m = carrier_lines("light","hover", seat_fact(raw="symbol label", hasSymbol=False))
    check("arm_claimed_carrier_absent_is_a_hard_fail",
          v_m == "fail" and CARRIER_COLOUR_ALONE in l_m[0] and "symbol" in l_m[0], f"{v_m} / {l_m}")
    v_e, l_e = carrier_lines("light","hover", seat_fact(raw="wat"))
    check("arm_unreadable_declaration_is_named_and_fails",
          v_e == "fail" and l_e[0].startswith(CARRIER_ERR_PREFIX), f"{v_e} / {l_e}")
    v_n, l_n = carrier_lines("light","hover", seat_fact(ratio=None, reason=None))
    check("arm_seat_without_a_reason_is_named",
          v_n == "seat" and HOLE_REASON_UNRECORDED in l_n[0],
          "a seat with no fill reading and no recorded reason must SAY so, never render blank")

    # (iii) the REPORT: counted, headed, re-parsed — and a carrier fail must reach the exit code
    cfake = {"Aaa": [("light","hover", seat_fact(raw="colour", hasSymbol=False, hasLabel=False)),
                     ("light","hover", seat_fact())]}
    ctext, ctot, _, _, ccar = render_report(cfake)
    check("arm_carrier_fail_counted_and_headed", ccar == 1 and
          "**1 CARRIER failure(s) — declarations that carry meaning by colour alone, plus "
          "declarations this gate could not READ (s151-D1).**" in ctext, f"ccar={ccar}")
    check("arm_carrier_fail_is_not_a_text_fail", ctot == 0 and ctext.count("- ❌ TEXT ") == 0,
          "a carrier failure must be its own kind, never folded into the text count")
    check("arm_report_quotes_what_it_forbids",
          '"colour alone must not carry meaning"' in ctext and "data-carries" in ctext
          and "an UNDECLARED seat behaves exactly as it did before" in ctext,
          "the report must quote the rule AND state that silence waives nothing")
    # ⚠ THE SECOND ARM MUTATION TESTING ADDED. Clause (b) was proven only at the MEASURE layer —
    # the browser records kept the carrier's failure — but the REPORT layer could still have
    # dropped it, and a mutant that filtered seat-tagged text records out of `tf` survived every
    # arm above. The clause has to be checked where the verdict is actually rendered.
    bfake = {"Aaa": [("light","hover",{"kind":"text","text":"Pending","ratio":1.16,"thr":4.5,
                                       "seat":'span.seat "Pending"'}),
                     ("light","hover", seat_fact())]}
    btext, btot, _, _, bcar = render_report(bfake)
    check("arm_declared_seat_does_not_waive_its_carrier_in_the_report",
          btot == 1 and btext.count("- ❌ TEXT ") == 1 and "CARRIER LEGIBILITY" in btext
          and bcar == 0,
          "clause (b): a text failure inside a DECLARED seat must still be rendered and counted "
          f"as a ❌ TEXT failure — a declaration demotes the SEAT's fill, never its carriers "
          f"(total={btot}, lines={btext.count('- ❌ TEXT ')})")
    # MUTATION CONTROL — drop the carrier line from the body and the write must FAIL.
    cdropped = "\n".join(l for l in ctext.split("\n") if not l.startswith(CARRIER_FAIL_PREFIX))
    try:
        verify_report(cdropped, 1, ctot, n_holes=0, n_carriers=ccar)
        check("arm_dropped_carrier_line_bites", False, "a carrier line was removed and verify_report passed")
    except StateContrastReportError as e:
        check("arm_dropped_carrier_line_bites", "carrier-failure count disagrees" in str(e), f"wrong refusal: {e}")
    try:
        verify_report(ctext, 1, ctot, n_holes=0, n_carriers=ccar + 4)
        check("arm_miscounted_carrier_bites", False, "counters said 5, artefact carried 1, and it passed")
    except StateContrastReportError:
        check("arm_miscounted_carrier_bites", True)

    # (iv) the FEATURE, driven in a real browser on real files — a mutation test proves the
    # CLAUSE, not the FEATURE, so every clause above is also driven end-to-end here.
    def _seat_records(recs): return [r for r in recs if r["kind"] == "seatdecl"]
    ok = got["carrier_valid_declaration_demotes_the_fill"]
    ok_seat = _seat_records(ok)
    okv = carrier_lines("light","-",ok_seat[0])[0] if ok_seat else None
    check("arm_browser_valid_declaration_demotes",
          len(ok_seat) == 1 and okv == "seat" and ok_seat[0]["ratio"] is not None
          and ok_seat[0]["ratio"] < 3.0 and not [r for r in ok if r["kind"] == "text"],
          f"a valid declaration over a low-contrast fill must yield ONE advisory seat and no text fail: {ok}")
    co = got["carrier_colour_only_hard_fails"]
    co_seat = _seat_records(co)
    check("arm_browser_colour_only_hard_fails",
          len(co_seat) == 1 and carrier_lines("light","-",co_seat[0])[0] == "fail",
          f"a colour-only declaration must HARD FAIL at the browser end too: {co}")
    lf = got["carrier_declared_but_label_still_fails"]
    lf_txt = [r for r in lf if r["kind"] == "text"]
    check("arm_browser_declared_carrier_that_fails_stays_a_failure",
          len(lf_txt) == 1 and lf_txt[0]["seat"] is not None
          and carrier_lines("light","-",_seat_records(lf)[0])[0] == "seat",
          f"clause (b): a declaration must NOT waive its own carrier's failure: {lf}")
    uw = _seat_records(got["carrier_unknown_word_is_named"])
    check("arm_browser_unknown_word_is_named",
          len(uw) == 1 and carrier_lines("light","-",uw[0])[1][0].startswith(CARRIER_ERR_PREFIX),
          f"an unreadable declaration must be NAMED at the browser end: {uw}")
    ca = _seat_records(got["carrier_claimed_symbol_absent_is_named"])
    check("arm_browser_claimed_symbol_absent_is_named",
          len(ca) == 1 and ca[0]["hasSymbol"] is False
          and carrier_lines("light","-",ca[0])[0] == "fail",
          f"a claimed-but-absent symbol must be measured at the browser and fail: {ca}")
    # THE SILENCE CONTROL: same DOM, no attribute. Identical text failure, and NO seat record.
    ud = got["carrier_undeclared_seat_is_unchanged"]
    ud_txt = [r for r in ud if r["kind"] == "text"]
    check("arm_browser_undeclared_seat_is_unchanged",
          _seat_records(ud) == [] and len(ud_txt) == 1
          and ud_txt[0]["ratio"] == lf_txt[0]["ratio"] and ud_txt[0]["seat"] is None,
          f"an UNDECLARED seat must behave exactly as before — nothing passes by silence: {ud}")

    # ---- s152-D1 (Dave, #152) — THE MARK LEG MUST NOT MEASURE A PHANTOM ------------------------
    # Driven end to end in the browser, because a mutation test proves the CLAUSE and not the
    # FEATURE [[mutation-tests-the-clause-not-the-feature]].
    def _marks(recs): return [r for r in recs if r["kind"] == "text"
                              and str(r.get("text", "")).startswith("[MARK] ")]
    def _skips(recs): return [r for r in recs if r["kind"] == "markskip"]
    ph = got["mark_phantom_fill_is_skipped"]
    # ⚠ NAME THE BRANCH. This arm first asserted the "no painted fill at all" reason and BIT on the
    # first real run (#153) — an <svg> with no fill attribute computes to rgb(0,0,0), which is NOT
    # `none`, so `shapeFillStr` is truthy and the DECLARED-BUT-UNWORN branch is the one that fires.
    # The bite was the arm's expectation, not the mechanism; the assertion below now names the
    # phantom colour explicitly so it cannot pass against the other branch by accident.
    check("arm_browser_phantom_shape_fill_is_skipped_and_declared",
          len(_skips(ph)) == 1 and _marks(ph) == []
          and _skips(ph)[0]["fill"] == "rgb(0, 0, 0)"
          and "no descendant shape paints" in _skips(ph)[0]["reason"],
          "an <svg> with no explicit fill paints nothing, so its UA-default black is not a surface "
          "any mark sits on: the leg must SKIP and SAY SO, never report 1.66 against a phantom "
          f"(#152 measured exactly this on the chip star): {ph}")
    # THE DISCRIMINATING ARM. Same computed rgb(0,0,0) as the phantom, but genuinely worn by a
    # descendant. If this ever goes quiet, the "fix" has become a deletion.
    rb = got["mark_real_black_roundel_still_fails"]
    check("arm_browser_real_black_roundel_still_fails",
          _skips(rb) == [] and len(_marks(rb)) == 1 and _marks(rb)[0]["ratio"] < 4.5,
          "a REAL black roundel wearing its own fill must STILL fail on a #333 mark — the clause "
          f"keys on PAINTED, never on the colour black: {rb}")
    df = got["mark_body_only_in_defs_is_skipped"]
    check("arm_browser_body_inside_defs_does_not_count_as_painted",
          len(_skips(df)) == 1 and _marks(df) == [],
          f"a shape inside <defs> is not rendered in place, so it cannot make a fill painted: {df}")

    # MUTATION CONTROL — cut the guard out of MEASURE itself and the phantom must COME BACK. An arm
    # that only asserts silence cannot tell a fix from a deletion, and a fixture that never
    # exercised the defect proves nothing at all. This re-runs the SAME fixture through a mutated
    # MEASURE and demands the 1.66 reappear.
    _mut = MEASURE.replace("if(fg&&bodyPaints){", "if(fg){", 1)
    check("arm_mutation_target_is_present_in_MEASURE", _mut != MEASURE,
          "the s152-D1 guard `if(fg&&bodyPaints){` was NOT found in MEASURE, so the mutation "
          "control below would silently prove nothing. An unmatched mutation target is a FAILURE, "
          "never a skip [[unmatched-grep-is-not-an-absence]]")
    if _mut != MEASURE:
        mres = _measure_fixtures(script=_mut, only=["mark_phantom_fill_is_skipped"])
        mm = _marks(mres["mark_phantom_fill_is_skipped"])
        check("arm_removing_the_skip_brings_the_phantom_back",
              len(mm) == 1 and abs(mm[0]["ratio"] - 1.66) < 0.02,
              "with the s152-D1 guard removed, the phantom 1.66 MUST reappear — if it does not, "
              "this fixture never exercised the defect and every arm above it is an assertion, "
              f"not a measurement: {mres}")

    # (v) THE SWEEP — the clause that was MISSING until the vocabulary was driven on a real
    # snippet. A declaration on a PASSIVE element (Status-indicator's `.stat` is a plain div) is
    # outside SEL, so the in-MEASURE seat pass can never reach it. This arm drives `run()` end to
    # end over a real file whose ONLY declaration is passive; without the page-wide sweep it
    # reports nothing at all — silently.
    swept = tempfile.mkdtemp(prefix="state-contrast-sweep-")
    open(os.path.join(swept, "Zsweep.reference.html"), "w", encoding="utf-8").write(
        _FIX_HEAD + '<div class="passive" data-carries="colour" style="background:#FFC107;'
                    'width:60px;height:20px"></div>'
                    '<div class="seg"><button type="button">Only interactive thing</button></div>')
    _real_snip = globals()["SNIP"]
    try:
        globals()["SNIP"] = swept
        sres = run([])
    finally:
        globals()["SNIP"] = _real_snip
    sdecl = [r for _t, _s, r in sres.get("Zsweep", []) if r["kind"] == "seatdecl"]
    check("arm_passive_declaration_is_swept",
          len(sdecl) >= 1 and all(carrier_lines("light", "base", r)[0] == "fail" for r in sdecl),
          "a declaration on a PASSIVE element (outside SEL) must still be seen and judged — "
          f"without the page-wide sweep it is invisible: {sres.get('Zsweep')}")

    if fails:
        print(f"selftest FAILED — {len(fails)} bite(s):", file=sys.stderr)
        for f in fails: print(f"  ✗ {f}", file=sys.stderr)
        return 1
    print(f"selftest OK — {len(ARMS_RUN)} arms. Headline INSERTED (first heading survives, 0 snippets "
          "does not crash); artefact re-parsed against its own counters; unknown/unmatched arguments "
          "named; sibling paint seen; opacity:0 paints nothing; ancestor paint still seen; "
          "white-on-white STILL FAILS; un-hit-testable box falls back and declares it; "
          "s125-D3's refusal intact; s151-D1 meaning-carriers driven END TO END in the browser — "
          "a valid declaration demotes its fill to advisory, a colour-only declaration HARD FAILS "
          "with the verbatim reason, a declared carrier that misses its own threshold is STILL ❌, "
          "an unreadable or unfounded declaration is NAMED, and an UNDECLARED seat is byte-for-byte "
          "unchanged.")
    return 0

def main(argv):
    filters, want_selftest = parse_args(argv)
    if want_selftest:
        # ⛔ #194 — BEFORE ANY WORK. See the fork-bomb note above `HOLE_REASON_UNRECORDED`. The
        # probe sits AFTER parse_args on purpose: a bad flag is still an ARGUMENT error (2) on a
        # playwright-less box, so the refusal stays scoped to the missing import and does not
        # widen into a catch-all that swallows every other verdict here.
        if _PLAYWRIGHT_IMPORT_ERROR is not None:
            raise _playwright_unreachable()
        return selftest()
    res = run(filters)
    text, total, refused, fellback, carrier_fails = render_report(res)
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
    if carrier_fails:
        print(f"s151-D1 CARRIER: {carrier_fails} declaration(s) failed the meaning-carrier clauses "
              f'("{CARRIER_COLOUR_ALONE}", or unreadable) — see _STATE-CONTRAST-AUDIT.md', file=sys.stderr)
    return 1 if (total or refused or carrier_fails) else 0

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except StateContrastUnreachable as e:
        # #193 — a refusal, not a verdict, and it says where the verdict IS.
        sys.exit(cna.refuse(
            "_validate_state_contrast.py",
            f"{e} ⇒ THIS IS NOT A SKIP: these arms (including the s152-D1 mutation control) run "
            f"BLOCKING in the `render` job of .github/workflows/gates.yml, which installs "
            f"chromium — that job is where this gate's proof of record lives. Nothing here is "
            f"claimed green; the question was unaskable on this box."))
    except (StateContrastArgError, StateContrastReportError, StateContrastSelftestError,
            StateContrastCarrierError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
