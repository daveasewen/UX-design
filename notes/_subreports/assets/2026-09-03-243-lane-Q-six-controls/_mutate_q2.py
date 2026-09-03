"""Q2 mutations — applied to the MIRROR copy only; the repo file is never touched.
usage: _mutate_q2.py <gold-script> <mut-prefix>..."""
import hashlib, os, subprocess, sys
M = "/sessions/awesome-festive-hamilton/q2/mirror"
F = os.path.join(M, "knowledge/_validate_polarities.py")
REPO_F = "/sessions/awesome-festive-hamilton/mnt/UX-design/knowledge/_validate_polarities.py"
GOLD_PATH = sys.argv[1]
GOLD = open(GOLD_PATH, "rb").read()
REPO_BYTES = open(REPO_F, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
JOIN = '            texts[r["id"]] = " ".join(str(v) for v in r.values() if isinstance(v, str))'
MUTS = {
 "R3a the source ALLOW-LIST clause alone removed (Q3: 'a node may not name its own oracle')":
   ('            if s["path"] not in SOURCE_ALLOW:\n                fails.append(("S-SOURCE", f"{sw}.path',
    '            if False:\n                fails.append(("S-SOURCE", f"{sw}.path'),
 "M4b load_register PREPENDS 'FABRICATED ' to every row text (V3's mutation, verbatim)":
   (JOIN, '            texts[r["id"]] = "FABRICATED " + " ".join(str(v) for v in r.values() if isinstance(v, str))'),
 "M4c row text joined per field with ' \\n ' (whitespace only; a phrase may not span two fields)":
   (JOIN, '            texts[r["id"]] = " \\n ".join(str(v) for v in r.values() if isinstance(v, str))'),
 "M4d the STUB haystack alone (all_rows_text, Q5's check_stubs input) is built WITHOUT R1 row 0 — the gate stops 'saying' row 0; every other use of row_texts untouched":
   ('    all_rows_text = " \\n ".join(row_texts.values())',
    '    all_rows_text = " \\n ".join(t for i, t in enumerate(row_texts.values()) if i)'),
 "G1 the driver DROPS $seed handling (check_receipt: has_seed forced False) — lane Q's G1, re-run for the new 225 arms":
   ('    has_seed = isinstance(seed, str) and seed.strip() != ""',
    '    has_seed = False'),
 "M5 check_receipt silently accepts BOTH receipts (the BOTH clause disabled) — probe for 225 TWO RECEIPTS":
   ('    if has_src and has_seed:\n        first_id',
    '    if False:\n        first_id'),
 "M4b2 load_register REPLACES every row text with 'FABRICATED <id>' (the haystack no longer says what the R1 file says)":
   (JOIN, '            texts[r["id"]] = "FABRICATED " + r["id"]'),
}
which = sys.argv[2:]
print(f"gold script: {GOLD_PATH} sha {sha(GOLD)[:16]}")
for label in MUTS:
    if which and not any(label.startswith(w) for w in which):
        continue
    old, new = MUTS[label]
    src = GOLD.decode()
    assert src.count(old) == 1, (label, src.count(old))
    open(F, "w").write(src.replace(old, new))
    r = subprocess.run([sys.executable, F, "--selftest"], capture_output=True, text=True, cwd=M)
    lines = r.stdout.splitlines()
    print(f"=== MUTATION {label}")
    for i, l in enumerate(lines):
        if "FAIL" in l[:14] or l.startswith("arms ") or "selftest" in l[:12]:
            print(l[:300])
        if "FAIL" in l[:14] and "#243 s243-D1" in l:
            for k in range(i + 1, min(i + 4, len(lines))):
                if lines[k].startswith(" " * 6) and not lines[k][:14].strip().isdigit():
                    print("   " + lines[k].strip()[:330])
                else:
                    break
    # the 235 LEGAL / 225 rows, PASS or FAIL, so a green-stays-green is visible too
    for l in lines:
        if ("235 LEGAL" in l or "225 " in l) and l[:4].strip().isdigit():
            print("   row: " + l[:200])
    print(f"rc={r.returncode}")
    open(F, "wb").write(GOLD)
    print("restored mirror sha", sha(open(F, "rb").read())[:16], "== gold", sha(GOLD)[:16],
          "| repo sha", sha(open(REPO_F, "rb").read())[:16], "(repo unchanged:", sha(open(REPO_F, "rb").read()) == sha(REPO_BYTES), ")")
    print()
