#!/usr/bin/env python3
"""_enact_s273_d1_address.py — s273-D1: write `provides: <role>` onto every roles.json provider
whose meta is silent, by TEXTUAL SPAN (the #179 class: never json.dump a meta).

The line is inserted immediately AFTER the meta's top-level `"purpose"` line (the seat the 24
first-pass metas use: `purpose` … `provides` … `answers`). Proof per file: removing exactly the
inserted span gives back the original bytes; the result parses; it has exactly one more key
and that key is `provides` with the roles.json value. Any file failing a proof is left untouched
and named. `--dry-run` (default) writes nothing.

  python3 knowledge/_enact_s273_d1_address.py            # dry run, lists what would change
  python3 knowledge/_enact_s273_d1_address.py --write    # enact
"""
from __future__ import annotations
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROLES = os.path.join(HERE, "roles.json")
COMP = os.path.join(HERE, "components")
PURPOSE_RE = re.compile(r'^  "purpose": .*?(?<!\\)"(,?)\n', re.M | re.S)


def plan() -> tuple[list, list]:
    roles = json.load(open(ROLES, encoding="utf-8"))
    todo, skipped = [], []
    for role, r in roles["roles"].items():
        for p in r["providers"]:
            slug = p["slug"] if isinstance(p, dict) else p
            path = os.path.join(COMP, f"{slug}.meta.json")
            if not os.path.exists(path):
                skipped.append((slug, role, "no meta file")); continue
            src = open(path, encoding="utf-8").read()
            m = json.loads(src)
            if m.get("provides") == role:
                continue
            if m.get("provides"):
                skipped.append((slug, role, f"provides already {m['provides']!r} — a contradiction, not mine")); continue
            todo.append((slug, role, path, src))
    return todo, skipped


def compose(src: str, role: str) -> tuple[str, str, int] | None:
    """Return (new_text, span, offset) or None when the purpose seat cannot be found once."""
    # find the top-level "purpose" line: 2-space indent, value ends at a quote followed by , or newline
    i = src.find('\n  "purpose": ')
    if i < 0:
        return None
    # the purpose value may be a long single-line string; find its terminating `",\n` at depth 0
    j = i + 1
    k = src.find('\n', j)
    while k > 0 and not src[j:k].rstrip().endswith('",') and not src[j:k].rstrip().endswith('"'):
        k = src.find('\n', k + 1)
    if k < 0:
        return None
    line = src[j:k]
    if not line.rstrip().endswith(','):
        return None  # purpose is the last key — the seat needs a trailing comma; leave it
    span = f'  "provides": "{role}",\n'
    off = k + 1
    return src[:off] + span + src[off:], span, off


def run(write: bool) -> int:
    todo, skipped = plan()
    done, refused = [], []
    for slug, role, path, src in todo:
        c = compose(src, role)
        if c is None:
            refused.append((slug, role, "purpose seat not found as one line with a trailing comma")); continue
        new, span, off = c
        # R2 textual: reconstruction
        if new[:off] + new[off + len(span):] != src:
            refused.append((slug, role, "reconstruction failed")); continue
        try:
            a, b = json.loads(src), json.loads(new)
        except json.JSONDecodeError as e:
            refused.append((slug, role, f"does not parse after insert: {e}")); continue
        if b.get("provides") != role or {k: v for k, v in b.items() if k != "provides"} != a:
            refused.append((slug, role, "parsed diff is not exactly +provides")); continue
        if write:
            open(path, "w", encoding="utf-8").write(new)
        done.append((slug, role))
    mode = "WRITTEN" if write else "DRY RUN"
    print(f"{mode}: {len(done)} metas gain `provides` · {len(refused)} refused · {len(skipped)} skipped")
    for s, r in done: print(f"  + {s:32} provides: {r}")
    for s, r, why in refused: print(f"  ⛔ {s:32} {r}: {why}")
    for s, r, why in skipped: print(f"  · {s:32} {r}: {why}")
    return 1 if refused else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    sys.exit(run(ap.parse_args().write))
