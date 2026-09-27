"""W4b: patch _validate_geometry.py — part 3, the selftest (new clauses, sub-legs, cause levers, W3b's real page)."""
P = "knowledge/_validate_geometry.py"
s = open(P).read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:100])
    s = s.replace(old, new)

rep('''PLANTED_EXPECT = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]''',
'''PLANTED_EXPECT = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
# W4b #304: planted SUB-CASES — each a blind spot found on the cold runs, planted under its own
# marker so it is proven separately from its clause's original case. (clause, data-planted value,
# the cause lever that must let it through — None when the clause switch is the only lever)
PLANTED_SUB = [("G6", "G6-lone", "X-lone"), ("G7", "G7-shell", "X-scroll"), ("G8", "G8-scroll", "X-scroll"),
               ("G11", "G11-letters", None)]''')

rep('''REFERENCE_KNOWN_TRUE = [("G10", "svg.spark-inline")]
''', '''REFERENCE_KNOWN_TRUE = [("G10", "svg.spark-inline")]
# W3b's receipt (#304): v1013-r2's overview at 1440 holds a ring chart in a 1,221px full-width tile
# with a hole under the ring that the R4b gate read as G6 = 0 (a one-panel group's panel was never
# measured). The real page is the frozen cold run beside the v1.0.13 pack it links (../pack/…);
# the selftest stages the two into $TMPDIR and asserts the gate now names the hole (G6) and the
# ring lost in its box (G12) on that tile. Absent run or pack = the leg is SKIPPED and said so.
REAL_W3B_RUN = os.path.join(ROOT, "notes", "_lanes", "304", "R4c", "cold", "v1013-r2", "out")
REAL_W3B_PACK = os.path.join(ROOT, "apollo-spider", "dist", "Apollo-Spider-v1.0.13.zip")
REAL_W3B_EXPECT = [("G6", "Cash by currency"), ("G12", "Cash by currency")]


def _stage_w3b():
    """Stage W3b's real page (frozen run + its pack) under $TMPDIR; None when either is absent."""
    import hashlib, shutil, tempfile, zipfile
    if not (os.path.isdir(REAL_W3B_RUN) and os.path.exists(REAL_W3B_PACK)):
        return None
    h = hashlib.sha256(open(REAL_W3B_PACK, "rb").read()).hexdigest()[:12]
    root = os.path.join(tempfile.gettempdir(), "geometry-w3b-" + h)
    if not os.path.exists(os.path.join(root, ".ok")):
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(os.path.join(root, "zip"))
        zipfile.ZipFile(REAL_W3B_PACK).extractall(os.path.join(root, "zip"))
        tops = [d for d in os.listdir(os.path.join(root, "zip")) if os.path.isdir(os.path.join(root, "zip", d))]
        src = os.path.join(root, "zip", tops[0]) if len(tops) == 1 else os.path.join(root, "zip")
        os.rename(src, os.path.join(root, "pack"))
        open(os.path.join(root, ".ok"), "w").write(h)
    shutil.rmtree(os.path.join(root, "out"), ignore_errors=True)
    shutil.copytree(REAL_W3B_RUN, os.path.join(root, "out"), ignore=shutil.ignore_patterns("_to_delete"))
    return os.path.join(root, "out", "index.html")
''')

rep('''    stray = [f for f in pf if not f["planted"]]''', '''    for c, sub, lever in PLANTED_SUB:
        hit = [f for f in pf if f["clause"] == c and f["planted"] == sub]
        if not hit:
            fails.append("PLANTED %s (%s) NOT CAUGHT on the planted element" % (sub, NAMES[c]))
        elif verbose:
            print("  ✓ planted %-11s %-21s caught: %s" % (sub, NAMES[c], hit[0]["measured"][:84]))
    stray = [f for f in pf if not f["planted"]]''')

rep('''    if verbose:
        print("  ✓ %d mutations: each clause switched off lets exactly its own planted defect through"
              % len(PLANTED_EXPECT) if not any(x.startswith("MUTATION") for x in fails) else "  ✖ mutation leg failed")''',
'''    # 5. the CAUSE levers (W4b): restoring each repaired blind spot lets exactly its sub-cases through
    #    and moves nothing else on the planted page
    base_keys = sorted((f["clause"], f["planted"], f["where"]) for f in pf)
    for lever in sorted(LEVERS):
        subs = {sub for c, sub, lv in PLANTED_SUB if lv == lever}
        lm = [f for w in widths for f in judge(h.model(FIX_PLANTED, w, [lever]), w, (), stops)]
        still = {f["planted"] for f in lm} & subs
        if still:
            fails.append("LEVER %s: the cause restored but %s still caught — the repair is not what catches it" % (lever, sorted(still)))
        rest = sorted((f["clause"], f["planted"], f["where"]) for f in lm)
        expect = [k for k in base_keys if k[1] not in subs]
        if rest != expect:
            fails.append("LEVER %s: other findings moved (%d → %d outside the sub-cases)" % (lever, len(expect), len(rest)))
        elif verbose and not still:
            print("  ✓ cause lever %-8s restores the blind spot: %s slip through, nothing else moves" % (lever, ", ".join(sorted(subs))))
    # 6. W3b's real page: the ring hole the R4b gate read as G6 = 0
    real = _stage_w3b()
    if real is None:
        print("  ⊘ W3b real-page leg SKIPPED: %s or %s is absent" % (os.path.relpath(REAL_W3B_RUN, ROOT), os.path.relpath(REAL_W3B_PACK, ROOT)))
    else:
        mw = h.model(real, 1440)
        wf = judge(mw, 1440, (), stops)
        if not mw.get("fontOk"):
            print("  ⊘ W3b real-page leg UNPROVEN-FONT (the HSBC face is not drawing)")
        for c, name in REAL_W3B_EXPECT:
            hit = [f for f in wf if f["clause"] == c and name in f["where"]]
            if not hit and mw.get("fontOk"):
                fails.append("REAL W3b page (v1013-r2): %s (%s) not named on '%s'" % (c, NAMES[c], name))
            elif hit and verbose:
                print("  ✓ real v1013-r2 %-4s named on '%s': %s" % (c, name, hit[0]["measured"][:70]))
        lw = judge(h.model(real, 1440, ["X-lone"]), 1440, (), stops)
        if any(f["clause"] == "G6" and "Cash by currency" in f["where"] for f in lw):
            fails.append("REAL W3b page: with the lone-leaf repair switched off, G6 still names the ring tile — the repair is not the cause")
        elif verbose:
            print("  ✓ real v1013-r2: X-lone switched on, the ring tile's G6 disappears (R4b's reading reproduced)")
    if verbose:
        print("  ✓ %d mutations: each clause switched off lets exactly its own planted defect through"
              % len(PLANTED_EXPECT) if not any(x.startswith("MUTATION") for x in fails) else "  ✖ mutation leg failed")''')
rep('''            print("Geometry selftest — planted fixture, clean fixture, reference bento, the #288 page, %d mutations"
                  % len(PLANTED_EXPECT))''', '''            print("Geometry selftest — planted fixture (%d clauses + %d sub-cases), clean fixture, reference bento, "
                  "the #288 page, W3b's v1013-r2 page, %d clause mutations + %d cause levers"
                  % (len(PLANTED_EXPECT), len(PLANTED_SUB), len(PLANTED_EXPECT), len(LEVERS)))''')
open(P, "w").write(s)
print("selftest patched")
