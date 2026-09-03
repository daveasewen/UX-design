"""V3 mutations — applied to the MIRROR copy only; the repo file is never touched."""
import hashlib, os, shutil, subprocess, sys
M = "/sessions/awesome-festive-hamilton/v3/mirror"
F = os.path.join(M, "knowledge/_validate_polarities.py")
REPO_F = "/sessions/awesome-festive-hamilton/mnt/UX-design/knowledge/_validate_polarities.py"
GOLD = open(REPO_F, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
MUTS = {
 "M1 check_receipt ACCEPTS a $seed absent from the store (R1-DANGLING loop skips '$seed')":
   ('    for key in ("$seed", "retiredBy"):\n        v = node.get(key)',
    '    for key in ("retiredBy",):\n        v = node.get(key)'),
 "M2 retired_map() returns EMPTY":
   ('    return {n["id"]: n["retiredBy"] for n in nodes\n            if isinstance(n, dict) and isinstance(n.get("id"), str) and isinstance(n.get("retiredBy"), str)}',
    '    return {}'),
 "M3 the WRITER skips the gate's verdict (add_entry: refusal branch disabled)":
   ('    if rc != 0 and not only_stale:\n        print(buf.getvalue(), end="")',
    '    if False:\n        print(buf.getvalue(), end="")'),
 "M4 Q5 haystack joined PER FIELD with NUL (a phrase may not span two register fields)":
   ('            texts[r["id"]] = " ".join(str(v) for v in r.values() if isinstance(v, str))',
    '            texts[r["id"]] = "\\x00".join(str(v) for v in r.values() if isinstance(v, str))'),
 "M4b load_register PREPENDS a fabricated token to every row text (the arm's 'verbatim' phrase is now NOT in the R1 file)":
   ('            texts[r["id"]] = " ".join(str(v) for v in r.values() if isinstance(v, str))',
    '            texts[r["id"]] = "FABRICATED " + " ".join(str(v) for v in r.values() if isinstance(v, str))'),
 "M4c row text joined per field with ' \\n ' (a phrase may not span two fields; whitespace only)":
   ('            texts[r["id"]] = " ".join(str(v) for v in r.values() if isinstance(v, str))',
    '            texts[r["id"]] = " \\n ".join(str(v) for v in r.values() if isinstance(v, str))'),
 "M5 check_receipt: NEITHER receipt is silently accepted (tautology probe for the $seed green arms)":
   ('    elif not has_src and not has_seed:\n        fails.append(("S-SOURCE", f"{nid}: carries NO receipt',
    '    elif False:\n        fails.append(("S-SOURCE", f"{nid}: carries NO receipt'),
}
which = sys.argv[1:] or list(MUTS)
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
    for l in lines:
        if "FAIL" in l[:14] or l.startswith("arms ") or "selftest" in l[:12]:
            print(l[:260])
    # verbatim notes for the NEW arms only
    for i, l in enumerate(lines):
        if "FAIL" in l[:14] and "#243 s243-D1" in l:
            for k in range(i + 1, min(i + 4, len(lines))):
                if lines[k].startswith(" " * 6) and not lines[k][:14].strip().isdigit():
                    print("   " + lines[k].strip()[:300])
                else:
                    break
    print(f"rc={r.returncode}")
    open(F, "wb").write(GOLD)
    print("restored mirror sha", sha(open(F, "rb").read())[:16], "== gold", sha(GOLD)[:16], "| repo sha", sha(open(REPO_F, "rb").read())[:16])
    print()
