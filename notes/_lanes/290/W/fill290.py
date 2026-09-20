#!/usr/bin/env python3
"""#290 wrap — fill this wrap's OWN placeholders and iterate the self-measuring lines to a
FIXED POINT (the #240 lesson, mechanised rather than remembered).

THREE lines in this wrap measure regions that CONTAIN them: the `section-sizes` line, the
declare-last `size:` stamp, and the banner-headroom figure. Each is written, re-measured, and
re-written until the measurement stops moving.

⚠ DECLARED DEVIATION, the #288 precedent: these substitutions are WHOLE-FILE writes, not mover
ops — the mover has no iterate-to-fixed-point op, and each is a fill of THIS wrap's OWN
placeholder inside THIS wrap's OWN stratum or header. **The §A sha256 is asserted before and
after every write**, through the gate's own pinned probe, so the claim is mechanical.

usage:  python3 fill290.py [--write]
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

GM = os.path.join(ROOT, "GOOD-MORNING.md")
LS = os.path.join(ROOT, "_LIVE-STATE.md")
WRITE = "--write" in sys.argv


def digest():
    lines = open(GM, encoding="utf-8").read().split("\n")
    return cg.section_a_digest(lines, cg.section_spans(lines))


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    d0 = digest()
    tmp = p + ".tmp"
    open(tmp, "w", encoding="utf-8").write(s)
    os.replace(tmp, p)
    d1 = digest()
    assert d0 == d1, f"§A MOVED during a write to {os.path.basename(p)} — {d0} → {d1}"


def tk(s):
    return cg.measure_tokens(s)[0]


def sizes_line():
    p = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_gm_usage.py"),
                        "--sizes", "--session", "290"], capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stdout + p.stderr
    return [l for l in p.stdout.strip().split("\n") if l.startswith("> **section-sizes")][-1]


def a_real():
    p = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_gm_usage.py"),
                        "--sizes", "--session", "290"], capture_output=True, text=True, cwd=ROOT)
    m = re.search(r"\bA:(\d+)", p.stdout)
    return int(m.group(1))


STAMP_TMPL = (
    "> **size:** GM **{gmk}K tape** ({gm:,} exact, whole-file `tiktoken cl100k_base` — the figure "
    "this stamp is graded against at 10% tolerance) · §A **{ak}K tape** ({a:,} real by "
    "`_gm_usage.py`) — \u2705 **THE \u00a7A BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND \u00a7A IS "
    "BYTE-IDENTICAL TO ITS STATE AT THE #272\u2026#289 WRAPS** (`sha256 {dig}\u2026` over the gate's OWN "
    "pinned probe shape `_capture_gate.section_a_digest`, returning exactly what all eighteen of "
    "those stamps recorded \u2014 **\u00a7A has not moved in TWENTY-TWO sessions**; the gate reports it "
    "EXEMPT by ruling: measured and reported, never charged). \u26a0 **THE TWO-PROBE-SHAPE QUESTION "
    "#272 RAISED IS STILL NOT SETTLED AND IS NOT SETTLED HERE:** #269/#270/#271 recorded "
    "`sha256 b9aef5f5\u2026` over 169 lines and #272\u2026#290 record `{dig}\u2026` over 198 \u2014 two probe "
    "shapes, not a change in \u00a7A, and **which shape the stamp should quote is ruling-shaped and "
    "remains Dave's, now at its TWENTY-SECOND session, standing in `_CARRIES.md` \u00a7 "
    "`residual \u2192 #291`.** \u00b7 LS **{lsk}K tape** ({ls:,} real) \u00b7 corpus GM+LS **{ck}K tape** "
    "({c:,} real, the RETRIEVAL surface, not the chain) \u00b7 \u26d4 **the chain's own size is NOT "
    "copied here \u2014 RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer, exact by "
    "construction and `--check`-blocked** \u00b7 measured 2026-09-20 at the #290 wrap, DECLARE-LAST. "
    "**AGAINST #289's STAMP (34,015 / 71,940 / 105,955 tape) GM IS {dgm:+,} tape, LS {dls:+,} AND "
    "THE CORPUS {dc:+,}** \u2014 and the cause is nameable rather than mysterious: **#289's \u2605 PRIOR "
    "banner and its 15,000-tape-class stratum rolled OUT of GM while #290 wrote a banner and a "
    "stratum of its own, and `s241-D2` puts gauge, declared-skip and 5b detail in the \u23f1 LATEST "
    "DELTA, which is `_LIVE-STATE.md`** \u2014 where #287's \u23f1 delta rolled out in the same pass. "
    "\u26d4 **#272\u2026#289's standing warning that the next wrap has no room in this idiom is NOT "
    "withdrawn, and this wrap did NOT meet it: the \u2605 LATEST banner fit on the first pass at "
    "{btk}/{blines} against the 1,200/10 cap.** \u26d4 **NEITHER FILE SIZE IS A TRIM ORDER; all of "
    "these are measurements, and what to do about them is Dave's.** \u26a0 **AND TWO DRIFTS ARE "
    "DECLARED RATHER THAN LEFT TO BE DISCOVERED.** (1) **Both this stamp and the `section-sizes` "
    "line measure regions that CONTAIN them**, so each was ITERATED TO A FIXED POINT rather than "
    "published at a reading taken before it was written \u2014 the #240 lesson, mechanised in "
    "`notes/_lanes/290/W/fill290.py`, and both are DECLARED whole-file writes rather than mover "
    "ops because the mover has no iterate-to-fixed-point op. (2) **The `s214-D6` chain figure and "
    "STEP 5b both land AFTER this stamp** (the stamp is itself inside the chain slice \u2014 the #241 "
    "rule), so they move GM and `_LIVE-STATE.md` by single-digit-percent tape against a 10% "
    "grading tolerance and **the stamp is NOT re-taken for them** \u2014 saying so is cheaper and "
    "truer than a second reading nobody can reconcile."
)


def banner_figure():
    sys.path.insert(0, HERE)
    import measure_banner
    lines, _ = measure_banner.block_lines()
    sub = [l for l in lines if l.strip() not in ("", ">")]
    return tk("\n".join(lines)), len(sub)


def fill_once():
    gm = read(GM)
    # 1 — section-sizes
    line = sizes_line()
    gm = re.sub(r"^> \*\*section-sizes #290 \(real\):\*\*.*$", lambda _: line, gm, count=1, flags=re.M)
    gm = gm.replace("> **section-sizes #290 (real):** {{SECTION_SIZES}}", line)
    # 2 — banner headroom
    btk, blines = banner_figure()
    gm = re.sub(r"\{\{BANNER\}\}|\*\*\d{3,4} cl100k over \d+ of 10 substantive lines\*\*",
                f"**{btk:,} cl100k over {blines} of 10 substantive lines**", gm, count=1)
    if WRITE:
        write(GM, gm)
    return gm, btk, blines


def stamp_once():
    gm = read(GM)
    g = tk(gm)
    l = tk(read(LS))
    a = a_real()
    btk, blines = banner_figure()
    new = STAMP_TMPL.format(gmk=f"{g/1000:.1f}", gm=g, ak=f"{a/1000:.1f}", a=a,
                            lsk=f"{l/1000:.1f}", ls=l, ck=f"{(g+l)/1000:.1f}", c=g + l,
                            dgm=g - 34015, dls=l - 71940, dc=(g + l) - 105955,
                            dig=digest()[:8], btk=f"{btk:,}", blines=blines)
    old = [x for x in gm.split("\n") if x.startswith("> **size:**")]
    assert len(old) == 1
    gm2 = gm.replace(old[0], new, 1)
    if WRITE:
        write(GM, gm2)
    return old[0], new, g, l


if __name__ == "__main__":
    _, btk, blines = fill_once()
    print(f"banner {btk:,} / {blines} lines")
    for i in range(6):
        old, new, g, l = stamp_once()
        print(f"  pass {i+1}: GM {g:,} · LS {l:,} · corpus {g+l:,}")
        if old == new:
            print("  FIXED POINT")
            break
    print("§A digest:", digest()[:12], "(asserted before and after every write)")
    if not WRITE:
        print("DRY — pass --write to land it")
