#!/usr/bin/env python3
"""Generate knowledge/_render/apollo-fab-meta.json — the FAB provenance inspector's
lookup table, keyed by the `cn-*` class a rendered page actually carries.

Input : knowledge/components/*.meta.json   (136 files at #227)
Output: knowledge/_render/apollo-fab-meta.json

WHY A GENERATED MAP AND NOT A LIVE READ
The overlay is a single view-time <script>. It cannot walk the repo, and a page opened
from file:// often cannot fetch anything at all. So the inspector degrades in two steps:
  1. map present + fetch succeeded -> name, category, purpose, token verdict
  2. anything else                 -> the component name derived from the class alone
Step 2 is the DEFAULT-SAFE path, not an error state. This file only ever upgrades it.

KEYING
Class vocabulary in canon.css is `cn-<lowercased meta filename stem>`
(alert.meta.json -> .cn-alert, Chart-boxplot.meta.json -> .cn-chart-boxplot).
Chart components additionally appear as `cn-chart-<x>-dv`; the overlay strips a
trailing `-dv` before lookup, so no duplicate rows are minted here.

This script writes ONE file and reads nothing outside knowledge/components/.
No ruling is encoded here — the field selection is a build choice, restated in
notes/_subreports/2026-08-30-227-fab-overlay.md.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "knowledge" / "components"
OUT = ROOT / "knowledge" / "_render" / "apollo-fab-meta.json"

PURPOSE_CAP = 240


def first_sentence(text: str) -> str:
    """First sentence of `purpose`, capped. Never mid-word."""
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return ""
    m = re.search(r"(?<=[a-z0-9)\"'])\.\s", text)
    if m and m.start() + 1 <= PURPOSE_CAP:
        return text[: m.start() + 1]
    if len(text) <= PURPOSE_CAP:
        return text
    cut = text[:PURPOSE_CAP].rsplit(" ", 1)[0]
    return cut + "…"


def verdict(meta: dict) -> str:
    """One word for the token-validation state, or '' when the meta never claims one."""
    tv = meta.get("tokenValidation")
    if isinstance(tv, dict):
        result = str(tv.get("result", "")).strip()
        if result:
            head = re.split(r"[\s—\-:,]", result, 1)[0].strip()
            if head:
                return head.upper()[:12]
    return ""


def main() -> int:
    if not SRC.is_dir():
        print(f"FAIL: no component directory at {SRC}", file=sys.stderr)
        return 1

    rows = {}
    skipped = []
    for path in sorted(SRC.glob("*.meta.json")):
        try:
            meta = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # a malformed meta must fail LOUD and NAMED
            skipped.append(f"{path.name}: {exc}")
            continue
        if not isinstance(meta, dict) or "name" not in meta:
            skipped.append(f"{path.name}: no 'name' key")
            continue
        slug = path.name[: -len(".meta.json")].lower()
        row = {
            "n": meta.get("name", slug),
            "c": meta.get("category", ""),
            "p": first_sentence(meta.get("purpose", "")),
        }
        v = verdict(meta)
        if v:
            row["v"] = v
        rows[slug] = row

    payload = {
        "$generatedBy": "knowledge/_render/gen_fab_meta.py",
        "$keyedBy": "cn-<key> class in canon.css; overlay strips a trailing -dv",
        "$fields": {
            "n": "component name",
            "c": "category (atom/molecule/organism/template)",
            "p": "purpose, first sentence",
            "v": "tokenValidation verdict, first word (absent when the meta claims none)",
        },
        "components": rows,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"wrote {OUT.relative_to(ROOT)} — {len(rows)} components, {OUT.stat().st_size} bytes")
    if skipped:
        print(f"SKIPPED {len(skipped)}:", file=sys.stderr)
        for line in skipped:
            print("  " + line, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
