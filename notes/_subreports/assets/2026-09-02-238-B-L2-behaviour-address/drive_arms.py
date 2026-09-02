#!/usr/bin/env python3
"""
drive_arms.py — #238 lane B. THE DRIVE: the extended gate and the generator against a REAL
composed page on the fixture (fixture_build.py), with the brief's mutation arms —
address PRESENT / ABSENT / WRONG — plus the arms the two-sided check earns.

  python3 drive_arms.py <fixture_root> <evidence_dir>

Every arm re-derives its input from the fixture files, runs the REAL command line, and writes
its transcript (command · output · rc) to <evidence_dir>/drive-<letter>-<slug>.txt. The arm's
expectation is asserted here, so a green transcript is one this script has checked, not one
it has merely saved. [[mutation-tests-the-clause-not-the-feature]]: nothing calls an internal
helper — each arm is `python3 knowledge/_validate_receipt.py <page>` or the generator's --check.
"""
import json, os, re, shutil, subprocess, sys

root, ev = sys.argv[1], sys.argv[2]
K = os.path.join(root, "knowledge")
PAGE = os.path.join(root, "dashboards", "l2-fixture.html")
DP_META = os.path.join(K, "components", "date-picker.meta.json")
DP_SNIP = os.path.join(K, "snippets", "Date-picker.reference.html")
os.makedirs(ev, exist_ok=True)
sys.path.insert(0, K)
import _validate_receipt as VR

results = []


def run(cmd):
    p = subprocess.run(cmd, cwd=root, shell=True, capture_output=True, text=True, timeout=120)
    return p.returncode, (p.stdout + p.stderr).rstrip()


def arm(letter, slug, title, setup, cmd, expect_rc, expect_in, restore):
    """setup() mutates the fixture; cmd runs; expect_in: substrings that MUST appear; restore()."""
    try:
        setup()
        rc, out = run(cmd)
    finally:
        restore()
    out = out.replace(root, "<FIXTURE>")
    missing = [s for s in expect_in if s not in out]
    good = (rc == expect_rc) and not missing
    results.append((letter, title, good, rc, expect_rc, missing))
    body = ("# DRIVE %s — %s\n# fixture: %s (rebuilt by fixture_build.py in this call)\n$ %s\n%s\nrc=%d\n"
            "# EXPECT rc=%d and: %s\n# VERDICT: %s\n"
            % (letter, title, root, cmd.replace(root, "<FIXTURE>"), out, rc, expect_rc, expect_in,
               "as expected ✅" if good else "NOT as expected ❌ (missing %s)" % missing))
    open(os.path.join(ev, "drive-%s-%s.txt" % (letter, slug)), "w", encoding="utf-8").write(body)
    print(("✅ " if good else "❌ ") + "DRIVE %s %s -> rc=%d%s" % (letter, title, rc, "" if not missing else " missing " + str(missing)))


page0 = open(PAGE, encoding="utf-8").read()
meta0 = open(DP_META, encoding="utf-8").read()
snip0 = open(DP_SNIP, encoding="utf-8").read()
gate = "python3 knowledge/_validate_receipt.py dashboards/l2-fixture.html"
check = "python3 knowledge/gen_component_partials.py --check"


def restore_all():
    open(PAGE, "w", encoding="utf-8").write(page0)
    open(DP_META, "w", encoding="utf-8").write(meta0)
    open(DP_SNIP, "w", encoding="utf-8").write(snip0)


def set_meta_script(addr):
    d = json.loads(meta0)
    d["behaviour"]["script"] = addr
    json.dump(d, open(DP_META, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def remint():
    rc, out = run("python3 knowledge/gen_provenance_receipt.py --mint dashboards/l2-fixture.html")
    assert rc == 0, out


# A — PRESENT (control): the typed metas' addresses are loaded by the composed page
arm("A", "present-control", "address PRESENT — Date-picker + Textarea typed, page carries both scripts verbatim; Stat-card meta:NONE",
    lambda: None, gate, 0,
    ["Date-picker#markup", "knowledge/snippets/Date-picker.reference.html#script LOADED",
     "knowledge/snippets/Textarea.reference.html#script LOADED", "Stat-card#markup", "meta:NONE",
     "UNPROVEN:behaviour-address — 1 with meta:NONE (Stat-card#markup)", "RESULT: PASS"],
    restore_all)


# B — ABSENT: the page no longer carries Date-picker's script (region removed, receipt re-minted
#     so the receipt is consistent and the ONLY defect is the meta clause)
def _absent():
    p = re.sub(r"<!-- ===== APOLLO-SPLICE Date-picker#script START.*?APOLLO-SPLICE Date-picker#script END ===== -->\n",
               "", page0, flags=re.S)
    assert p != page0
    open(PAGE, "w", encoding="utf-8").write(p)
    remint()
arm("B", "absent", "address ABSENT from the page — Date-picker's script removed and the receipt re-minted",
    _absent, gate, 1,
    ["FAIL:BEHAVIOUR-NOT-LOADED — `Date-picker#markup`", "declares script `knowledge/snippets/Date-picker.reference.html#script`",
     "the page carries 1 inline executable script(s), none hashing to Date-picker#script[0]",
     "Textarea.reference.html#script LOADED", "RESULT: FAIL"],
    restore_all)

# C — WRONG (meta side, unresolvable): the meta names a file that does not exist
arm("C", "wrong-unresolvable-meta", "address WRONG — meta names knowledge/canon/nope.js (no such file)",
    lambda: set_meta_script("knowledge/canon/nope.js"), gate, 1,
    ["FAIL:BEHAVIOUR-ADDRESS-UNRESOLVABLE — `Date-picker#markup`", "names a file that does not exist", "RESULT: FAIL"],
    restore_all)
arm("C2", "wrong-unresolvable-generator", "…and the GENERATOR refuses the same meta (the derived block cannot be minted from a bad address)",
    lambda: set_meta_script("knowledge/canon/nope.js"), check, 1,
    ["behaviour-manifest/date-picker:", "declares script `knowledge/canon/nope.js`, which names a file that does not exist"],
    restore_all)

# D — WRONG (meta side, foreign): the meta points at ANOTHER component's snippet — one the page
#     even carries (Textarea) — and is refused as FOREIGN, not passed because 'some script' is there
arm("D", "wrong-foreign", "address WRONG — meta points at Textarea's #script (which the page DOES carry): FOREIGN",
    lambda: set_meta_script("knowledge/snippets/Textarea.reference.html#script"), gate, 1,
    ["FAIL:BEHAVIOUR-ADDRESS-FOREIGN — `Date-picker#markup`", "ANOTHER component's snippet (Textarea)", "RESULT: FAIL"],
    restore_all)
arm("D2", "wrong-foreign-generator", "…and the GENERATOR refuses it too",
    lambda: set_meta_script("knowledge/snippets/Textarea.reference.html#script"), check, 1,
    ["behaviour-manifest/date-picker:", "ANOTHER component's snippet (Textarea)"],
    restore_all)

# E — WRONG (page side): ONE byte flipped inside the page's copy of Date-picker's script. The
#     receipt names the region (HASH-MISMATCH) AND the meta clause names the missing script.
def _tamper():
    m = re.search(r"(APOLLO-SPLICE Date-picker#script START.*?)(addEventListener\('keydown')", page0, re.S)
    assert m
    p = page0[:m.start(2)] + "addEventListener('keyup'" + page0[m.end(2):]
    open(PAGE, "w", encoding="utf-8").write(p)
arm("E", "wrong-page-tampered", "address WRONG on the PAGE side — one token edited inside the copied script ('keydown'→'keyup')",
    _tamper, gate, 1,
    ["FAIL:HASH-MISMATCH — `Date-picker#script`", "FAIL:BEHAVIOUR-NOT-LOADED — `Date-picker#markup`",
     "diverges from it at byte", "RESULT: FAIL"],
    restore_all)

# F — the receipt's own `script` copy drifts from the meta (a copy-chain defect, caught)
def _drift():
    rec, err = VR.parse_receipt(page0)
    for r in rec["regions"]:
        if r["region"] == "Date-picker#markup":
            r["script"] = "knowledge/canon/dv-behaviour.js"
    block = '<script type="application/json" id="%s">\n%s\n</script>' % (VR.RECEIPT_ID, json.dumps(rec, indent=1))
    open(PAGE, "w", encoding="utf-8").write(VR.RECEIPT_RE.sub(lambda m: block, page0, count=1))
arm("F", "receipt-drift", "the receipt's `script` for Date-picker#markup says dv-behaviour.js; the meta says #script — DISAGREES",
    _drift, gate, 1,
    ["FAIL:BEHAVIOUR-ADDRESS-DISAGREES — `Date-picker#markup`", "the meta is the one home", "RESULT: FAIL"],
    restore_all)

# G — the DERIVED block: hand-edited in the snippet → --check out of sync; meta reverted to prose
#     while the block stays → orphan refused
arm("G", "derived-block-tampered", "the snippet's #behaviour-manifest hand-edited (events changed) — --check reports it out of sync",
    lambda: open(DP_SNIP, "w", encoding="utf-8").write(snip0.replace('"blur",', '"blurp",', 1)),
    check, 1, ["OUT OF SYNC", "Date-picker (behaviour-manifest)"], restore_all)


def _orphan():
    d = json.loads(meta0)
    d["behaviour"] = d["behaviour"]["$note"]          # the prose comes back, the block stays
    json.dump(d, open(DP_META, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
arm("G2", "derived-block-orphan", "meta reverted to PROSE while the snippet still carries the derived block — orphan refused",
    _orphan, check, 1, ["carries a #behaviour-manifest block but", "has no TYPED behaviour (PROSE)"], restore_all)

# H — the passive declaration: Textarea's meta re-typed as script:null while the page carries
#     its script — a positive 'no script' is noted, never failed (the schema/ratchet owns it)
TX_META = os.path.join(K, "components", "textarea.meta.json")
tx0 = open(TX_META, encoding="utf-8").read()
def _passive():
    d = json.loads(tx0); d["behaviour"]["script"] = None
    json.dump(d, open(TX_META, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
arm("H", "passive-null", "Textarea's meta says script:null (passive) — noted as meta:NO-SCRIPT, not a fail",
    _passive, gate, 0, ["Textarea#markup", "meta:NO-SCRIPT", "RESULT: PASS"],
    lambda: (restore_all(), open(TX_META, "w", encoding="utf-8").write(tx0)))

# I — the L1 gate's own arms on the SAME page: one byte inside a MARKUP region still trips the
#     receipt (nothing in L2 loosened L1)
def _l1():
    p = page0.replace("Choose a date", "Choose a dote", 1) if "Choose a date" in page0 else None
    if p is None:
        m = re.search(r"APOLLO-SPLICE Stat-card#markup START.*?-->\n(.)", page0, re.S)
        p = page0[:m.start(1)] + ("X" if page0[m.start(1)] != "X" else "Y") + page0[m.end(1):]
    open(PAGE, "w", encoding="utf-8").write(p)
arm("I", "l1-intact", "L1 intact — one byte inside a markup region still reds HASH-MISMATCH beside the L2 checks",
    _l1, gate, 1, ["FAIL:HASH-MISMATCH", "RESULT: FAIL"], restore_all)

ok = all(r[2] for r in results)
print("\nDRIVE ARMS: %d/%d as expected — %s" % (sum(1 for r in results if r[2]), len(results), "PASS ✅" if ok else "FAIL ❌"))
json.dump([{"arm": r[0], "title": r[1], "as_expected": r[2], "rc": r[3], "expect_rc": r[4], "missing": r[5]} for r in results],
          open(os.path.join(ev, "drive-arms-summary.json"), "w"), indent=1)
sys.exit(0 if ok else 1)
