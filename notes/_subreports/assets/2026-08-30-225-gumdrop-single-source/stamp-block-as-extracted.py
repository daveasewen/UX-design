import json, os, re, sys
stage, want = sys.argv[1], sys.argv[2]
# The same spelling family arm 5 of _gate_pack_docs.py sweeps (GUMDROP_RE): em dash, en dash or
# hyphen, so a stamp can never be narrower than the gate that grades it.
RE = re.compile(r"(Memento\s*[—–\-]\s*Gumdrop\s+v)(\d+\.\d+\.\d+)")
carry, moved = 0, []
for root, dirs, files in os.walk(stage):
    dirs.sort()
    for name in sorted(files):
        p = os.path.join(root, name)
        try:
            src = open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue                       # binary (the vendored encoder blob) — nothing to stamp
        if "Gumdrop" not in src:
            continue
        out, k = RE.subn(lambda m: m.group(1) + want.lstrip("v"), src)
        if not k:
            continue
        carry += 1
        rel = os.path.relpath(p, stage)
        if out != src:
            was = sorted({"v" + m.group(2) for m in RE.finditer(src)})
            open(p, "w", encoding="utf-8").write(out)
            moved.append((rel, ", ".join(was)))
        if p.endswith(".json"):
            with open(p, encoding="utf-8") as fh:
                json.load(fh)               # a stamp that breaks the JSON dies here, not later
print("carried-cut version stamped from the manifest: %s — %d staged file(s) carry the literal, "
      "%d rewritten" % (want, carry, len(moved)))
for rel, was in moved:
    print("  ⚠ DRIFT: %s typed %s and was stamped to %s. Its committed blob no longer matches "
          "what ships, so `--check` will name this path until the repo copy is synced."
          % (rel, was, want))
