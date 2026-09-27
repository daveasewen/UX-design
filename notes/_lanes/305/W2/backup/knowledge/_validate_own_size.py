#!/usr/bin/env python3
"""_validate_own_size.py — every part at its own size: a generated page against the reference render. ADVISORY.

WHY THIS EXISTS
---------------
Dave, Thursday 24 September 2026, 15:46: *"can we make sure it retrieves the components well,
sometimes it made buttons and table headings way smaller than they should."* The #304 when-rules
decision page (question 5) proposes the rule in the graph's words — "A part keeps its own size on
any page. The page arranges parts; it never shrinks them." — and a check that measures it. No gate
measured size before this one: `_validate_grid.py` reads declared CSS, `_validate_hit_area.py` holds
controls to 44px but not to THEIR OWN size, and a page that shrinks a 44px button to 36px passes both.

WHAT IT COMPARES
----------------
The reference snippet is the reviewed artefact (`knowledge/snippets/<Name>.reference.html`), the same
premise `_validate_descender_computed.py` stands on. For every canon component on the page (an
element wearing `cn-<slug>` where `<Name>.reference.html` exists and slug(Name) == slug, the
`gen_canon_components.slug` rule), every PART inside it is matched to the same part in that
component's reference render, at the same viewport width, in the same browser:

  controls  button, [role=button], .btn, input (text-like), select, textarea, [role=tab]
  headers   th, [role=columnheader]   (a header in <thead> or scope=col is keyed apart from a row header)
  cells     td                        (type size only)

A part belongs to its NEAREST canon component. Its key is tag + role + head/body position + its
classes that the reference itself uses (state classes is-/has-/js- dropped; a class the page invented,
like #288's `.mini`, is dropped from the key so the part is still matched, and its effect is what
gets measured). Matching falls back from the exact key to tag + role, EXCEPT for a part none of
whose classes the reference uses at all: that is the page's own control inside the wrapper, and it
is listed as unmatched rather than judged against an unrelated button. Every value the reference shows
for the key (all its variants and states) forms the legal RANGE.

  S1 height   a control or column header rendered below 0.92 x the reference's smallest, or a control
              above 1.25 x its largest (squashed / stretched).
  S2 width    a control narrower than 0.92 x the reference's computed `min-width` (the ruled minimum,
              e.g. the button's 96px), when the reference sets one.
  S3 type     a part's font-size below 0.92 x the reference's smallest or above 1.15 x its largest.

THE TOLERANCES
  0.92   the canon's type steps are at least 12.5% apart (16→14, 14→12), and a control's height moves on
         the 4px grid (44→40 is −9.1%): 0.92 catches one step down in either and absorbs sub-pixel and
         border-box rounding (≤3px on a 44px control).
  1.25   (controls taller) a control stretched by its row (`align-items:stretch`) grows by a quarter or more;
         smaller growth is padding or wrap noise, and a wrapping header only ever grows, so headers are
         held on the shrink side only.
  1.15   (type larger) one step up the scale is ≥12.5%; 15% keeps a single-step upscale in, rounding out.

THE FACE. A fallback font is not a size reading (#304 plan, lane 4c): each render reports whether the
HSBC face is really drawing (measured: the string's width in "<face>, monospace" against monospace).
If either render fell back, the page's verdict is UNPROVEN-FONT and its findings are listed but not scored.

OUTPUT: a verdict object per page `{"gate":"own-size","page","verdict":"CLEAN|FINDINGS|UNPROVEN-FONT|
NO-PARTS","findings":[{clause,component,part,width,measured,reference,fix}],"matched","unmatched",
"runtime_ms"}` (with `--json`) and a plain list a designer can act on.

ADVISORY: exit 0 whatever it finds (`--strict` exits 1 on any finding). Exit 77 COULD-NOT-ASK when the
browser is unavailable (the `_validate_hit_area` convention). Exit 2 on a crash or bad usage.

USAGE
  python3 knowledge/_validate_own_size.py PAGE.html [...]            # 1440 by default
  python3 knowledge/_validate_own_size.py PAGE.html --widths 1440,390 --json out.json
  python3 knowledge/_validate_own_size.py --showroom showroom/button.html   # the showroom's iframe
  python3 knowledge/_validate_own_size.py --selftest   # planted fixture + clean fixture + showroom + mutations
  python3 knowledge/_validate_own_size.py --build      # selftest, then the tracked generated pages
  python3 knowledge/_validate_own_size.py PAGE --mutate S2            # switch one clause off
Built #304 lane R4b. Writes nothing unless `--json`/`--out` name a path.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import argparse, glob, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNIPPETS = os.path.join(HERE, "snippets")
FIX_DIR = os.path.join(HERE, "_tests", "geometry")
FIX_PLANTED = os.path.join(FIX_DIR, "own-size-planted.html")
FIX_CLEAN = os.path.join(FIX_DIR, "own-size-clean.html")
SHOWROOM_SELFTEST = [os.path.join(ROOT, "showroom", "button.html"), os.path.join(ROOT, "showroom", "table.html")]
BUILD_SWEEP = [
    "notes/_lanes/288/P/composed-dashboard.html",
    "notes/_lanes/292/D/overview-dashboard-oneshot-v1.html",
    "dashboards/international-banking-dashboard.canon.html",
]
CLAUSES = ["S1", "S2", "S3"]
NAMES = {"S1": "height off its own size", "S2": "narrower than its own minimum", "S3": "type off its own size"}
SHRINK, GROW_CTL, GROW_TYPE = 0.92, 1.25, 1.15

sys.path.insert(0, HERE)
try:
    from _validate_geometry import Harness  # one browser discipline for both gates
except Exception:  # pragma: no cover - a pack without the sibling
    Harness = None


def slug(name):   # the gen_canon_components.slug rule, restated so this gate has no canon import
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def snippet_map():
    out = {}
    for p in glob.glob(os.path.join(SNIPPETS, "*.reference.html")):
        out[slug(os.path.basename(p).replace(".reference.html", ""))] = p
    return out


PARTS_JS = r"""
(args) => {
  const {mode, slugs, only} = args;   // mode: 'page' (cn- instances) | 'whole' (the whole document is one component)
  const doc = document;
  const cls = el => (typeof el.className === 'string' ? el.className : (el.getAttribute('class') || ''));
  const shown = el => { const c = getComputedStyle(el); if (c.display === 'none' || c.visibility === 'hidden') return false;
    // a closed <details> (a chart's data table) is laid out but never drawn: not a part anyone sees
    if (el.checkVisibility && !el.checkVisibility({contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true})) return false;
    const r = el.getBoundingClientRect(); return r.width > 2 && r.height > 2; };
  // the showroom harness is fenced by APOLLO-DEMO comments (s258-D3): never measure it
  const demo = new Set();
  const tw = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_COMMENT);
  let on = 0, n;
  while ((n = tw.nextNode())) {
    if (n.nodeType === 8) { if (/APOLLO-DEMO[^\n]*START/.test(n.nodeValue)) on++; else if (/APOLLO-DEMO[^\n]*END/.test(n.nodeValue)) on = Math.max(0, on - 1); continue; }
    if (on) demo.add(n);
  }
  const isDemo = el => { let e = el; while (e) { if (demo.has(e) || /(^|\s)demo-bar(\s|$)/.test(cls(e))) return true; e = e.parentElement; } return false; };
  const SEL = 'button,[role="button"],.btn,input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]):not([type="range"]),select,textarea,[role="tab"],th,[role="columnheader"],td';
  const owner = el => {
    if (mode === 'whole') return only;
    let e = el;
    while (e && e !== doc.body) { for (const t of cls(e).split(/\s+/)) { const m = /^cn-([a-z0-9-]+)$/.exec(t); if (m && slugs.includes(m[1])) return m[1]; } e = e.parentElement; }
    return null;
  };
  const kind = el => { const t = el.tagName.toLowerCase(), r = el.getAttribute('role') || '';
    if (t === 'th' || r === 'columnheader') return 'header'; if (t === 'td') return 'cell'; return 'control'; };
  const out = [];
  for (const el of doc.querySelectorAll(SEL)) {
    if (!shown(el) || isDemo(el)) continue;
    // a control nested in a control (a button inside [role=button]) is measured once, as the outer
    if (el.parentElement && el.parentElement.closest('button,[role="button"],.btn') && kind(el) === 'control') continue;
    const comp = owner(el); if (!comp) continue;
    const c = getComputedStyle(el); const r = el.getBoundingClientRect();
    const k = kind(el);
    const head = k === 'header' ? ((el.closest('thead') || el.getAttribute('scope') === 'col' || el.getAttribute('role') === 'columnheader') ? 'head' : 'body') : '';
    const mw = parseFloat(c.minWidth);
    out.push({comp, kind: k, tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '', pos: head,
      classes: cls(el).split(/\s+/).filter(x => x && !/^(is|has|js)-/.test(x)).sort(),
      h: Math.round(r.height * 10) / 10, w: Math.round(r.width * 10) / 10, fs: parseFloat(c.fontSize),
      minw: isFinite(mw) ? mw : 0, text: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 32)});
  }
  let fontOk = null; try {
    const cx = document.createElement('canvas').getContext('2d'); const s = 'Programmes in flight 0123456789';
    cx.font = '16px monospace'; const mono = cx.measureText(s).width;
    fontOk = ['Univers Next HSBC', 'HSBC_MtUnivers_Latin'].some(f => { cx.font = '16px "' + f + '", monospace'; return Math.abs(cx.measureText(s).width - mono) > 0.5; });
  } catch (e) {}
  return {parts: out, fontOk, root: {cls: document.documentElement.className, theme: document.documentElement.getAttribute('data-theme'), apollo: document.documentElement.getAttribute('data-apollo-theme')}};
}
"""


def _key(p, vocab=None):
    classes = p["classes"] if vocab is None else [c for c in p["classes"] if c in vocab]
    return "%s[%s]%s.%s" % (p["tag"], p["role"], p["pos"], ".".join(classes))


def _loose(p):
    return "%s[%s]%s" % (p["tag"], p["role"], p["pos"])


class RefCache:
    def __init__(self, h, smap):
        self.h, self.smap, self.cache = h, smap, {}

    def get(self, comp, width):
        k = (comp, width)
        if k not in self.cache:
            path = self.smap.get(comp)
            if not path:
                self.cache[k] = None
            else:
                m = self.h.eval(path, width, PARTS_JS, {"mode": "whole", "slugs": [], "only": comp})
                parts = m["parts"]
                vocab = set(c for p in parts for c in p["classes"])
                exact, loose = {}, {}
                for p in parts:
                    exact.setdefault(_key(p), []).append(p)
                    loose.setdefault(_loose(p), []).append(p)
                self.cache[k] = {"parts": parts, "vocab": vocab, "exact": exact, "loose": loose,
                                 "fontOk": m["fontOk"], "path": path}
        return self.cache[k]


def judge(parts, ref_for, width, off=()):
    """parts: the page's measured parts; ref_for(comp) -> reference record. Returns (findings, matched, unmatched)."""
    F, matched, unmatched = [], 0, []

    def add(clause, p, comp, measured, reference, fix):
        if clause in off:
            return
        F.append({"clause": clause, "name": NAMES[clause], "component": comp, "width": width,
                  "part": "%s %s'%s'" % (p["tag"], ("." + ".".join(p["classes"]) + " ") if p["classes"] else "", p["text"]),
                  "measured": measured, "reference": reference, "fix": fix})

    for p in parts:
        ref = ref_for(p["comp"])
        if not ref:
            unmatched.append("%s: no reference snippet" % p["comp"])
            continue
        # a part whose classes the reference NEVER uses is not this component's part (a page's own
        # control dropped inside the wrapper, e.g. a KPI tile's call-to-action inside cn-tabs): it is
        # listed as unmatched, never judged against whatever button the reference happens to hold
        foreign = bool(p["classes"]) and not any(c in ref["vocab"] for c in p["classes"])
        cand = None if foreign else (ref["exact"].get(_key(p, ref["vocab"])) or ref["loose"].get(_loose(p)))
        if not cand:
            unmatched.append("%s %s" % (p["comp"], _key(p)))
            continue
        matched += 1
        hs = [c["h"] for c in cand]; fss = [c["fs"] for c in cand]
        if p["kind"] in ("control", "header"):
            lo, hi = min(hs), max(hs)
            if p["h"] < SHRINK * lo:
                add("S1", p, p["comp"], "%gpx tall" % p["h"], "%gpx in its reference (%s)" % (lo, os.path.basename(ref["path"])),
                    "Restore the part's own height: remove the page rule that overrides its height/padding.")
            elif p["kind"] == "control" and p["h"] > GROW_CTL * hi:
                add("S1", p, p["comp"], "%gpx tall" % p["h"], "%gpx at most in its reference" % hi,
                    "Stop the row stretching the control (align-self:center / align-items:start on its container).")
        if p["kind"] == "control":
            mws = [c["minw"] for c in cand if c["minw"] > 0]
            if mws:
                mw = min(mws)
                if p["w"] < SHRINK * mw:
                    add("S2", p, p["comp"], "%gpx wide" % p["w"], "min-width %gpx in its reference" % mw,
                        "Keep the component's own minimum width: drop the page class that resets min-width.")
        lo, hi = min(fss), max(fss)
        if p["fs"] < SHRINK * lo:
            add("S3", p, p["comp"], "font-size %gpx" % p["fs"], "%gpx in its reference" % lo,
                "Use the component's own type size; the page must not restyle a part's text.")
        elif p["fs"] > GROW_TYPE * hi:
            add("S3", p, p["comp"], "font-size %gpx" % p["fs"], "%gpx at most in its reference" % hi,
                "Use the component's own type size; the page must not restyle a part's text.")
    return F, matched, unmatched


def _harness_eval(self, path, width, js, arg, frame_child=False):
    pg = self.b.new_page(viewport={"width": width, "height": 900})
    try:
        pg.emulate_media(reduced_motion="reduce")
        # a showroom page opens in EMBED MODE (#chrome=0, #214): the payload is cut at the
        # APOLLO-REVIEW-OVERLAY marker, so the review overlay's own buttons are never measured
        pg.goto("file://" + os.path.abspath(path) + ("#chrome=0" if frame_child else ""))
        pg.wait_for_timeout(400)
        if frame_child:
            kids = [f for f in pg.frames if f != pg.main_frame]
            if not kids:
                raise RuntimeError("OWN-SIZE: %s has no iframe to measure" % path)
            kids[0].wait_for_load_state()
            pg.wait_for_timeout(300)
            return kids[0].evaluate(js, arg)
        return pg.evaluate(js, arg)
    finally:
        pg.close()


def run_pages(h, paths, widths, off=(), showroom=False, quiet=False):
    smap = snippet_map()
    refs = RefCache(h, smap)
    out = []
    for path in paths:
        t0 = time.time()
        rec = {"gate": "own-size", "page": os.path.relpath(path, ROOT), "findings": [], "matched": 0,
               "unmatched": [], "widths": {}}
        font_ok = True
        for w in widths:
            if showroom:
                comp = os.path.basename(path).replace(".html", "")
                m = h.eval(path, w, PARTS_JS, {"mode": "whole", "slugs": [], "only": comp}, frame_child=True)
            else:
                m = h.eval(path, w, PARTS_JS, {"mode": "page", "slugs": sorted(smap), "only": None})
            ref_for = lambda c: refs.get(c, w)
            f, n, un = judge(m["parts"], ref_for, w, off)
            rec["findings"] += f
            rec["matched"] += n
            rec["unmatched"] += un
            comps = sorted({p["comp"] for p in m["parts"]})
            ref_fonts = [refs.get(c, w)["fontOk"] for c in comps if refs.get(c, w)]
            font_ok = font_ok and bool(m["fontOk"]) and all(ref_fonts)
            rec["widths"][str(w)] = {"parts": len(m["parts"]), "components": comps, "findings": len(f)}
        rec["unmatched"] = sorted(set(rec["unmatched"]))
        rec["font_ok"] = font_ok
        rec["runtime_ms"] = int((time.time() - t0) * 1000)
        rec["counts"] = {c: sum(1 for x in rec["findings"] if x["clause"] == c) for c in CLAUSES}
        if not any(v["parts"] for v in rec["widths"].values()):
            rec["verdict"] = "NO-PARTS"
        elif not font_ok:
            rec["verdict"] = "UNPROVEN-FONT"
        else:
            rec["verdict"] = "FINDINGS" if rec["findings"] else "CLEAN"
        out.append(rec)
        if not quiet:
            print(render_text(rec))
    return out


def render_text(rec):
    L = ["", "OWN-SIZE %s — %s · %d part(s) matched · %d finding(s) · %d ms" % (
        rec["page"], rec["verdict"], rec["matched"], len(rec["findings"]), rec["runtime_ms"])]
    for f in rec["findings"]:
        L.append("  ⚠ %s @%s %s — %s in %s: %s (reference: %s)" % (f["clause"], f["width"], f["name"], f["part"],
                                                                  f["component"], f["measured"], f["reference"]))
        L.append("       fix: %s" % f["fix"])
    if rec["unmatched"]:
        L.append("  · %d part key(s) with no counterpart in a reference (not judged): %s"
                 % (len(rec["unmatched"]), "; ".join(rec["unmatched"][:6])))
    return "\n".join(L)


# ── selftest ──
PLANTED_EXPECT = {  # clause -> the part text that must be named
    "S1": ["Approve", "Programme", "Owner", "Spend"],   # a button and the table headings under their reference height
    "S2": ["Review"],                      # a button squashed below its own 96px minimum (#288's .mini)
    "S3": ["Approve", "Programme", "Owner", "Spend"],   # their type shrunk
}


def selftest(h, verbose=True):
    fails = []
    t0 = time.time()
    for p in (FIX_PLANTED, FIX_CLEAN):
        if not os.path.exists(p):
            return ["fixture missing: %s" % os.path.relpath(p, ROOT)]
    planted = run_pages(h, [FIX_PLANTED], [1440], quiet=True)[0]
    clean = run_pages(h, [FIX_CLEAN], [1440], quiet=True)[0]
    shows = run_pages(h, [p for p in SHOWROOM_SELFTEST if os.path.exists(p)], [1440], showroom=True, quiet=True)
    for c, texts in PLANTED_EXPECT.items():
        for t in texts:
            hit = [f for f in planted["findings"] if f["clause"] == c and ("'%s'" % t) in f["part"]]
            if not hit:
                fails.append("PLANTED %s (%s) not named on '%s'" % (c, NAMES[c], t))
            elif verbose:
                print("  ✓ planted %s %-30s caught on '%s': %s vs %s" % (c, NAMES[c], t, hit[0]["measured"], hit[0]["reference"]))
    named = {t for ts in PLANTED_EXPECT.values() for t in ts}
    stray = [f for f in planted["findings"] if not any(("'%s'" % t) in f["part"] for t in named)]
    if stray:
        fails.append("PLANTED page: %d finding(s) on unplanted parts, e.g. %s %s" % (len(stray), stray[0]["clause"], stray[0]["part"]))
    if planted["verdict"] == "UNPROVEN-FONT" or clean["verdict"] == "UNPROVEN-FONT":
        # every leg below is a size reading, and a fallback face is not one: refuse, never pass
        raise RuntimeError("OWN-SIZE: HARNESS UNAVAILABLE — the HSBC face is not drawing on this box, "
                           "and a fallback render is not a size reading (#304 plan, lane 4c). NOT a pass.")
    if clean["findings"] or clean["matched"] == 0:
        fails.append("CLEAN fixture: %d finding(s), %d part(s) matched" % (len(clean["findings"]), clean["matched"]))
    elif verbose:
        print("  ✓ clean fixture: %d part(s) matched, 0 findings" % clean["matched"])
    for s in shows:
        if s["findings"] or s["matched"] == 0:
            fails.append("SHOWROOM %s: %d finding(s), %d matched" % (s["page"], len(s["findings"]), s["matched"]))
        elif verbose:
            print("  ✓ showroom %s: %d part(s) matched, 0 findings" % (s["page"], s["matched"]))
    # mutation per clause, re-judged on the planted page's own measurement
    for c in CLAUSES:
        m = run_pages(h, [FIX_PLANTED], [1440], off={c}, quiet=True)[0]
        if any(f["clause"] == c for f in m["findings"]):
            fails.append("MUTATION %s: switched off but still reported" % c)
        if {f["clause"] for f in m["findings"]} != set(CLAUSES) - {c}:
            fails.append("MUTATION %s: other clauses moved: %s" % (c, sorted({f["clause"] for f in m["findings"]})))
    if verbose:
        print("  %s %d mutations" % ("✓" if not any(x.startswith("MUTATION") for x in fails) else "✖", len(CLAUSES)))
        print("  selftest runtime %d ms" % int((time.time() - t0) * 1000))
    return fails


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--widths", default="1440")
    ap.add_argument("--json", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--mutate", default="")
    ap.add_argument("--showroom", action="store_true", help="the files are showroom pages: measure their iframe")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    off = {x.strip() for x in a.mutate.split(",") if x.strip()}
    if off - set(CLAUSES):
        print("✖ OWN-SIZE: unknown clause(s) %s — known: %s" % (sorted(off - set(CLAUSES)), ", ".join(CLAUSES)), file=sys.stderr)
        return 2
    if not (a.files or a.selftest or a.build):
        print("✖ OWN-SIZE: no input files. Pass pages, --selftest or --build (`--help` for the contract).", file=sys.stderr)
        return 2
    if Harness is None:
        raise RuntimeError("OWN-SIZE: HARNESS UNAVAILABLE — _validate_geometry.py (the shared browser harness) is not importable")
    Harness.eval = _harness_eval
    widths = [int(x) for x in a.widths.split(",") if x.strip()]
    rc = 0
    with Harness() as h:
        if a.selftest or a.build:
            print("Own-size selftest — planted fixture, clean fixture, showroom button + table, %d mutations" % len(CLAUSES))
            fails = selftest(h)
            for f in fails:
                print("  ✖ " + f)
            print("OWN-SIZE SELFTEST " + ("FAILED — the INSTRUMENT is broken, not the pages" if fails else "OK"))
            rc = 1 if fails else 0
        files = list(a.files)
        if a.build:
            files += [os.path.join(ROOT, p) for p in BUILD_SWEEP if os.path.exists(os.path.join(ROOT, p))]
        if files:
            recs = run_pages(h, files, widths, off, showroom=a.showroom)
            n = sum(len(r["findings"]) for r in recs)
            print("\nADVISORY: %d page(s), %d finding(s)" % (len(recs), n))
            if a.json:
                with open(a.json, "w") as fh:
                    json.dump(recs if len(recs) > 1 else recs[0], fh, indent=1)
                print("wrote %s" % a.json)
            if n and a.strict:
                rc = rc or 1
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        if "HARNESS UNAVAILABLE" in str(e):
            print("COULD-NOT-ASK: %s" % str(e).replace("GEOMETRY", "OWN-SIZE"), file=sys.stderr)
            sys.exit(77)
        print("✖ %s" % e, file=sys.stderr)
        sys.exit(2)
