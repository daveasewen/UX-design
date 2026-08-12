#!/usr/bin/env python3
"""apply_type_bind.py — bind component selectors to canon type composites (TYPE-002).

Enacts Dave's rulings T-D9 (binding mechanism) + T-D10 (Component Medium is drift) from
_proforma/_TYPE-DECISIONS.md. Sibling to apply_type_snap.py: that one fixed VALUES (TYPE-003),
this one moves type SPECIFICATION out of components and into the composites (TYPE-002).

THE SPLIT (T-D12 proposal, 2026-07-18 - the fix for T-D11's failure)
  A composite binding now answers TWO questions, and they are bound SEPARATELY:
      TYPE  - `.t-cm-<size>`  family/size/weight.  Bound for EVERY selector in the batch.
      BOX   - `.t-cm-slot`    display/align/line-height/min-height/cap-trim.  OPT-IN.
  The slot binds ONLY where the element ALREADY DECLARES a flex display - i.e. where it is already
  shaped as a single-line control and the box therefore tells it nothing new. That is the exact
  condition `.btn` met when it bound cleanly, stated as a rule instead of assumed. Everything else
  takes TYPE ONLY and keeps its own box.

THE MECHANISM (T-D9, Dave 2026-07-18: "fine lets move on D it is")
  A component binds by being APPENDED TO THE SELECTOR LIST of the composite it uses, in
  canon/type.css. Plain CSS. No generator, no build step, no markup change.

      .t-cm-button,
      .btn { font-size:16px; font-weight:500; min-height:20px; }

  ⚠️ LOAD ORDER IS LOAD-BEARING. `.t-cm-button` and `.btn` are both specificity 0-1-0, so source
  order decides. type.css MUST be linked BEFORE the component's own styles.

SCOPE OF THIS SCRIPT — the `/1` BATCH ONLY, and that limit is deliberate.
  Of 465 font shorthands carrying a line-height, 208 use `/1`. Those are already Component-tier
  (line-height:1 is exactly what the Component composite sets), so binding them is expected to be
  a VISUAL NO-OP — proved on `.btn`: pixel diff = 417px, all of it the loading spinner caught at a
  different animation frame.

  The other 257 carry unitless line-heights of 1.1–1.6. A composite would REPLACE those with the
  canon value, which MOVES THINGS. That is not mechanical and is NOT in this script. It needs a
  reviewed batch of its own.

WEIGHT RULING (T-D10)
  Families B/C/D/E + unclassified — 88 declarations at weight 500, sizes 12/14/24 — are DRIFT and
  snap to 400. Family A (reverse text on near-black) HOLDS AT 500: it sits inside {#col26-020}(c),
  and the sheet's specimen (a small black chip on a white page) does not reproduce the halation
  condition at real extent. FAMILY_A_HOLD below is that carve-out. Do not widen it casually.

VERIFICATION IS PART OF THE JOB
  --verify renders every touched file before and after with real HSBC Univers and pixel-diffs them.
  A binding that is supposed to be a no-op must be SHOWN to be one. Fonts:
      mkdir -p ~/.fonts && cp knowledge/assets/fonts/_desktop/TTF/*.ttf ~/.fonts/ && fc-cache -f

ISOLATION CONTROL — `NO_SNAP=1` suppresses the T-D10 weight snap.
  This is a measuring instrument, not a mode. Re-running a batch with the snap held constant is what
  separates diffs the binding CAUSED from diffs T-D10 INTENDED — it turned T-D12's "8 files still
  differ" into "6 intended, 2 to rule on". A diff you cannot attribute is not evidence; pixel count
  alone would have condemned a correct change. Never ship with it set.

Usage:  python3 knowledge/apply_type_bind.py            # dry run — proposal only
        python3 knowledge/apply_type_bind.py --apply    # write changes
        python3 knowledge/apply_type_bind.py --verify   # render + pixel-diff the touched files
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, glob, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
TYPE_CSS = os.path.join(HERE, "canon", "type.css")

# ---- Component composites: (size, weight) -> composite class ------------------------
# Read from type.css so this can never drift from the source (same discipline as the gate).
def component_ramp():
    t = open(TYPE_CSS).read()
    ramp = {}
    for m in re.finditer(r"\.(t-cm-[a-z0-9-]+)[^{]*\{([^}]*)\}", t):
        name, body = m.group(1), m.group(2)
        s = re.search(r"font-size:(\d+)px", body)
        w = re.search(r"font-weight:(\d+)", body)
        if s and w:
            ramp.setdefault((int(s.group(1)), int(w.group(1))), name)
    return ramp

# Family A — reverse text on near-black. HELD AT 500 per T-D10; inside {#col26-020}(c).
FAMILY_A_HOLD = {".toast", ".skip-link", ".count-badge"}

# HELD — one selector, two different composites across files. The selector-list mechanism cannot
# express that (one shared type.css, so last-in-file wins for BOTH), and it should not: a colliding
# selector means the same-named atom has drifted to two sizes. Surfacing it is the mechanism doing
# its job. `.tag` is 14px in its canonical Tags.reference but 12px where Account-card and
# List-items say they are REUSING that atom. Needs a ruling: one atom at one size, or an explicit
# `.tag--sm` modifier. Do not bind until ruled.
COLLISION_HOLD = {".tag"}

# demo/harness scaffolding — never shipped, not gated (matches the gate's CHROME_SEL)
CHROME_SEL = re.compile(r"\.demo|\bdemo-|harness|\.dossier|\.swatch|\.spec-|#rv-|\.rv-", re.I)

# a font shorthand that is Component-tier: `<weight> <size>px/1 var(--font)`
FONT_1 = re.compile(
    r"font\s*:\s*(?P<w>\d{3})\s+(?P<s>\d+(?:\.\d+)?)px\s*/\s*1\s+var\(--font\)\s*;?")


def targets():
    return sorted(glob.glob(os.path.join(HERE, "snippets", "*.html")))


# A selector earns the BOX only if it already declares a flex display. Conservative by design: the
# box is what moved 13 files in T-D11, so it binds on OBSERVED shape, never on inference from the
# font shorthand. Widening this is a ruling, not a tweak.
FLEXY = re.compile(r"display\s*:\s*[^;{}]*flex")


def is_control_shaped(css, sel):
    for blk in re.finditer(r"([^{}]*)\{([^{}]*)\}", css):
        if blk.group(1).strip() == sel and FLEXY.search(blk.group(2)):
            return True
    return False


COMMENT = re.compile(r"/\*.*?\*/", re.S)


def plan():
    ramp = component_ramp()
    binds = collections.defaultdict(set)   # composite -> {selectors}
    edits = collections.defaultdict(list)  # file -> [(selector, old, composite)]
    skipped = []
    slots = set()                          # selectors that also earn `.t-cm-slot`
    for path in targets():
        raw = open(path, encoding="utf-8").read()
        # Strip CSS comments FIRST — otherwise a comment sitting above a rule is swallowed into
        # the selector by the block regex and the binding is recorded against nonsense.
        # (Blank the comment rather than deleting it so offsets, and therefore the literal text
        #  we later .replace() in the untouched source, stay valid.)
        css = COMMENT.sub(lambda m: " " * len(m.group(0)), raw)
        for blk in re.finditer(r"([^{}]*)\{([^{}]*)\}", css):
            sel, body = blk.group(1).strip(), blk.group(2)
            if not sel or CHROME_SEL.search(sel):
                continue
            m = FONT_1.search(body)
            if not m:
                continue
            size, weight = float(m.group("s")), int(m.group("w"))
            head = sel.split(",")[0].strip()
            if head in COLLISION_HOLD:
                skipped.append((os.path.basename(path), sel, f"{weight} {size:g}px", "COLLISION — held, needs a ruling"))
                continue
            # T-D10: Medium at 12/14/24 is drift -> 400, EXCEPT family A
            if (weight == 500 and size in (12, 14, 24) and head not in FAMILY_A_HOLD
                    and not os.environ.get('NO_SNAP')):
                weight = 400
            comp = ramp.get((int(size), weight))
            if not comp:
                skipped.append((os.path.basename(path), sel, f"{weight} {size:g}px", "no composite at this size+weight"))
                continue
            binds[comp].add(sel)
            if is_control_shaped(css, sel):
                slots.add(sel)
            edits[path].append((sel, m.group(0), comp,
                                blk.start(2) + m.start(), blk.start(2) + m.end()))
    return binds, edits, skipped, slots


def link_type_css(raw):
    """TYPE-001 + load order: link canon/type.css BEFORE the component's own <style>.
    A <link>, never an inline copy - Dave 2026-07-18: the project must stay portable, and 49
    inlined copies would be 49 things to keep in sync."""
    if re.search(r'<link[^>]+href=["\'][^"\']*type\\.css', raw, re.I):
        return raw, False
    m = re.search(r"<style[^>]*>", raw, re.I)
    if not m:
        return raw, False
    return raw[:m.start()] + '<link rel="stylesheet" href="../canon/type.css">\n' + raw[m.start():], True


def write_lists(binds, slots):
    """Append bound selectors to their composite's list, and to `.t-cm-slot`, in canon/type.css.

    `.t-cm-slot` appears THREE times - the base rule and both @supports trim branches. A slotted
    selector must join ALL of them or it gets the box WITHOUT the cap-trim, which is a different
    bug wearing the same clothes. So: patch every occurrence for the slot, the first for type.
    Idempotent - a selector already in a list is not added twice."""
    css = open(TYPE_CSS, encoding="utf-8").read()
    added = 0
    jobs = [(c, v, False) for c, v in binds.items()] + [("t-cm-slot", slots, True)]
    for comp, sels, every in jobs:
        anchor = "." + comp
        starts, i = [], css.find(anchor)
        while i != -1:
            if css[i + len(anchor)] in ",{\n ":
                starts.append(i)
                if not every:
                    break
            i = css.find(anchor, i + 1)
        if not starts:
            print(f"  ! no such composite in type.css: {anchor}")
            continue
        for i in reversed(starts):                 # reversed: keeps earlier offsets valid
            brace = css.index("{", i)
            head = css[i:brace]
            existing = {x.strip() for x in head.split(",")}
            fresh = [x for x in sorted(sels) if x.strip() not in existing]
            if not fresh:
                continue
            css = css[:i] + head.rstrip() + ",\n" + ",\n".join(fresh) + css[brace:]
            added += len(fresh)
    open(TYPE_CSS, "w", encoding="utf-8").write(css)
    return added


def main():
    apply_ = "--apply" in sys.argv
    binds, edits, skipped, slots = plan()
    n = sum(len(v) for v in edits.values())
    print(f"{'APPLY' if apply_ else 'DRY RUN'} - {n} binding(s) across {len(edits)} file(s)")
    print(f"  TYPE only: {n - len(slots)}   |   TYPE + BOX (.t-cm-slot): {len(slots)}\n")
    for comp in sorted(binds):
        print(f"  {comp}")
        for sel in sorted(binds[comp]):
            print(f"      {'[+slot] ' if sel in slots else '        '}{sel}")
    if skipped:
        print(f"\n  {len(skipped)} skipped - these need a ruling:")
        for f, sel, sw, why in skipped[:20]:
            print(f"      {f:34} {sel[:40]:40} {sw:12} {why}")
    if not apply_:
        print("\n(dry run - nothing written. re-run with --apply)")
        return
    for path, items in edits.items():
        css = open(path, encoding="utf-8").read()
        # right-to-left so earlier offsets stay valid; SPAN-scoped, never a global replace
        for sel, old, comp, a, b in sorted(items, key=lambda t: -t[3]):
            assert css[a:b] == old, f"offset drift in {path} for {sel}"
            css = css[:a] + (f"/* type: {comp}"
                             + (" + .t-cm-slot" if sel in slots else "")
                             + " (bound in canon/type.css - T-D9/T-D12) */") + css[b:]
        css, _ = link_type_css(css)
        open(path, "w", encoding="utf-8").write(css)
    added = write_lists(binds, slots)
    print(f"\n  {n} declaration(s) removed from {len(edits)} file(s)")
    print(f"  {added} selector(s) appended to composite lists in canon/type.css")
    json.dump({"type": {k: sorted(v) for k, v in binds.items()}, "slot": sorted(slots)},
              open(os.path.join(HERE, "canon", "_bindings-applied.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
