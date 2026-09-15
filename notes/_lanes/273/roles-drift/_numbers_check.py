#!/usr/bin/env python3
"""#273 lane RD — gate 2: no number on the page that the data does not contain.

Extracts every integer from the RENDERED page's headline + decisions + per-role
table and asserts each one is either

  * a literal integer value (or a container length) inside DRIFT.json, or
  * a figure in DERIVED.json, each of which carries the formula that produced
    it from DRIFT.json.

CITATION TOKENS are stripped BEFORE extraction and are printed, so the
exclusion list is auditable rather than convenient:

  s252-D1  #272  RD-1  P-272-1  b46ea90  ADR-0017  B-09  2026-09-15  WCAG 2.2
  _REVIEW-roles-drift-2026-09-15-v1.html

Prints PASS/FAIL per distinct number and exits non-zero on any FAIL.

  python3 notes/_lanes/273/roles-drift/_numbers_check.py
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PAGE = os.path.join(REPO, "notes", "_REVIEW-roles-drift-2026-09-15-v1.html")
DRIFT = json.load(open(os.path.join(HERE, "DRIFT.json")))
DERIVED = json.load(open(os.path.join(HERE, "DERIVED.json")))

SECTIONS = ["headline", "decisions", "perrole"]

CITATIONS = [
    (r"\bs\d+-D\d+\b", "ruling id"),
    (r"#\d+\b", "session number"),
    (r"\bRD-\d+\b", "decision id on this page"),
    (r"\bP-\d+-\d+\b", "tripwire id"),
    (r"\bDP-\d+\b", "dream-pass id"),
    (r"\bADR-\d+\b", "ADR id"),
    (r"\b[BNV]-\d+\b", "harvest row id"),
    (r"\bb46ea90\b|\b[0-9a-f]{7,40}\b", "commit sha"),
    (r"\b\d{4}-\d{2}-\d{2}\b", "date"),
    (r"\bv\d+(\.\d+)*\b", "version"),
    (r"\bWCAG\s*\d(\.\d)*\b", "standard"),
    (r"_REVIEW-[\w.\-]+", "page filename"),
    (r"[\w./\-]+\.(?:py|json|html|md|css|js)\b", "file path"),
]


class Slice(HTMLParser):
    """Collect the visible text of the named top-level sections."""

    def __init__(self, wanted):
        super().__init__(convert_charrefs=True)
        self.wanted = wanted
        self.depth = 0
        self.on = False
        self.skip = 0
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if self.on:
            self.depth += 1
        elif tag == "section" and a.get("id") in self.wanted:
            self.on = True
            self.depth = 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if self.on:
            self.depth -= 1
            if self.depth <= 0:
                self.on = False

    def handle_data(self, data):
        if self.on and not self.skip:
            self.buf.append(data)


def allowed_from(obj, out, lengths):
    if isinstance(obj, bool):
        return
    if isinstance(obj, int):
        out.add(obj)
    elif isinstance(obj, dict):
        lengths.add(len(obj))
        for v in obj.values():
            allowed_from(v, out, lengths)
    elif isinstance(obj, list):
        lengths.add(len(obj))
        for v in obj:
            allowed_from(v, out, lengths)


def main():
    src = open(PAGE).read()
    p = Slice(set(SECTIONS))
    p.feed(src)
    text = " ".join(p.buf)
    if not text.strip():
        print("FAIL  no text extracted for sections: %s" % ", ".join(SECTIONS))
        return 1

    stripped = {}
    for pat, why in CITATIONS:
        found = re.findall(pat, text)
        if found:
            stripped.setdefault(why, set()).update(
                m if isinstance(m, str) else m for m in re.findall(pat, text))
        text = re.sub(pat, " ", text)

    literals, lengths = set(), set()
    allowed_from(DRIFT, literals, lengths)
    derived = {v["value"]: k for k, v in DERIVED.items()}

    numbers = sorted({int(m) for m in re.findall(r"(?<![\w.])\d+(?![\w.])", text)})

    print("PAGE      %s" % PAGE)
    print("SECTIONS  %s" % ", ".join(SECTIONS))
    print("SOURCE    DRIFT.json (literals + container lengths) + DERIVED.json")
    print("")
    print("Citation tokens stripped before extraction:")
    for why in sorted(stripped):
        sample = sorted(stripped[why])
        print("  %-22s %s" % (why, ", ".join(sample[:8]) + (" …" if len(sample) > 8 else "")))
    print("")

    fails = 0
    for v in numbers:
        if v in literals:
            print("PASS  %-5s literal value in DRIFT.json" % v)
        elif v in lengths:
            print("PASS  %-5s container length in DRIFT.json" % v)
        elif v in derived:
            print("PASS  %-5s DERIVED.%s = %s"
                  % (v, derived[v], DERIVED[derived[v]]["formula"]))
        else:
            print("FAIL  %-5s not in DRIFT.json and not derived" % v)
            fails += 1

    print("")
    print("%d distinct numbers checked, %d FAIL" % (len(numbers), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
