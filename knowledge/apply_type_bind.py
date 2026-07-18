#!/usr/bin/env python3
"""apply_type_bind.py — bind component selectors to canon type composites (TYPE-002).

Enacts Dave's rulings T-D9 (binding mechanism) + T-D10 (Component Medium is drift) from
_proforma/_TYPE-DECISIONS.md. Sibling to apply_type_snap.py: that one fixed VALUES (TYPE-003),
this one moves type SPECIFICATION out of components and into the composites (TYPE-002).

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

Usage:  python3 knowledge/apply_type_bind.py            # dry run — proposal only
        python3 knowledge/apply_type_bind.py --apply    # write changes
        python3 knowledge/apply_type_bind.py --verify   # render + pixel-diff the touched files
"""
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


COMMENT = re.compile(r"/\*.*?\*/", re.S)


def plan():
    ramp = component_ramp()
    binds = collections.defaultdict(set)   # composite -> {selectors}
    edits = collections.defaultdict(list)  # file -> [(selector, old, composite)]
    skipped = []
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
            if weight == 500 and size in (12, 14, 24) and head not in FAMILY_A_HOLD:
                weight = 400
            comp = ramp.get((int(size), weight))
            if not comp:
                skipped.append((os.path.basename(path), sel, f"{weight} {size:g}px", "no composite at this size+weight"))
                continue
            binds[comp].add(sel)
            edits[path].append((sel, m.group(0), comp))
    return binds, edits, skipped


def main():
    apply_ = "--apply" in sys.argv
    binds, edits, skipped = plan()
    n = sum(len(v) for v in edits.values())
    print(f"{'APPLY' if apply_ else 'DRY RUN'} — {n} binding(s) across {len(edits)} file(s)\n")
    for comp in sorted(binds):
        print(f"  {comp}")
        for s in sorted(binds[comp]):
            print(f"      {s}")
    if skipped:
        print(f"\n  ⚠ {len(skipped)} skipped (no composite at that size+weight) — these need a ruling:")
        for f, s, sw, why in skipped[:20]:
            print(f"      {f:34} {s[:40]:40} {sw:12} {why}")
    if not apply_:
        print("\n(dry run — nothing written. re-run with --apply)")
        return
    for path, items in edits.items():
        css = open(path, encoding="utf-8").read()
        for sel, old, comp in items:
            css = css.replace(old, f"/* type: {comp} (bound in canon/type.css — T-D9) */")
        open(path, "w", encoding="utf-8").write(css)
    print(f"\n  ✓ {n} declaration(s) removed from {len(edits)} file(s)")
    print("  → now add the selectors above to their composite's list in canon/type.css")
    json.dump({k: sorted(v) for k, v in binds.items()},
              open(os.path.join(HERE, "canon", "_bindings-applied.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
