"""R1 lane 1b(iii) — step [82] type-binding blast radius. PREMISE (probed #304 R1): the gate's matcher
is approximate (every simple part present in the FILE). #261 N2 added <button class="menu-fab"> to
Tab-bar beside <nav class="seg">, so `.seg button` "matches" Tab-bar; in the DOM the button is a
SIBLING of nav.seg, not a descendant (0 <button> inside any .seg element), so no Tab-bar element
takes the rule and no pixel moves. The gate's sanctioned remedy `--update` is run and its diff
reviewed: (+) Tab-bar on `.seg button`; (-) `.tabbar .tabbar__item` shrinks to [] (the #261 N rename
dropped the class; a shrink never fails); `_generated` date. The note records why. Idempotent."""
import json, subprocess, sys, os
repo = sys.argv[1]; K = os.path.join(repo, "knowledge"); P = os.path.join(K, "canon", "_type-bindings.json")
subprocess.run([sys.executable, os.path.join(K, "_validate_type_blast_radius.py"), "--update"], check=True)
reg = json.load(open(P))
ADD = (" Tab-bar.reference.html acknowledged #304 R1 by --update with the diff reviewed: the approximate "
       "matcher sees `.seg` (the segmented island nav) and a <button> (the #261 N2 menu-fab) in the same file; "
       "in the DOM the button is a sibling of nav.seg, not a descendant, so no Tab-bar element takes this rule.")
for b in reg["bindings"]:
    if b["selector"] == ".seg button" and "#304 R1" not in b.get("note", ""):
        b["note"] = b.get("note", "") + ADD
open(P, "w").write(json.dumps(reg, indent=2) + "\n")
print("seg note ok")
