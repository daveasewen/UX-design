#!/usr/bin/env python3
"""Make a REVIEW copy of ANY Apollo HTML doc by injecting the review overlay
(comment pins + export-to-prompt) before </body>.

Usage:  python3 knowledge/_review/_make_review.py <path/to/doc.html> [more.html ...]
        (run from the repo root)

Output location:
  - source under a gated dir (…/_proforma/…) -> knowledge/_review/<stem>-REVIEW.html
    (kept OUT of _proforma/ so the component gates never scan the review copy)
  - any other doc (e.g. reviews/…, notes/…) -> co-located <dir>/<stem>.REVIEW.html
    so the clean + review PAIR sit together and can be shared as a set.

The review copy is GENERATED — never hand-edited. Regenerate it after each batch of
edits to the clean source. The overlay is self-contained, uses no browser storage
(Export is the save), and all ids/classes are rv-prefixed. Single source of truth =
_review-overlay.html. Per _PROFORMA-RULES rule 16 (docs ship clean + review).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OVERLAY = os.path.join(HERE, "_review-overlay.html")
MARK = "<!-- APOLLO-REVIEW-OVERLAY -->"

def label_for(stem):
    return stem.replace("-interactive", "").replace("-", " ").strip()

def out_path(src):
    """Gated proforma sources -> central _review/ (gate avoidance); everything else co-locates."""
    stem = os.path.splitext(os.path.basename(src))[0]
    norm = os.path.normpath(src).replace(os.sep, "/")
    if "/_proforma/" in ("/" + norm) or norm.startswith("_proforma/"):
        return os.path.join(HERE, stem + "-REVIEW.html")
    return os.path.join(os.path.dirname(os.path.abspath(src)), stem + ".REVIEW.html")

def make(src):
    with open(src) as f:
        html = f.read()
    with open(OVERLAY) as f:
        overlay = MARK + "\n" + f.read()
    stem = os.path.splitext(os.path.basename(src))[0]
    # rv-file points at the CLEAN source (edits apply there, not to the review copy)
    rv_file = os.path.normpath(src).replace(os.sep, "/")
    meta = ('<meta name="rv-doc" content="%s">\n<meta name="rv-file" content="%s">\n'
            % (label_for(stem), rv_file))
    overlay = meta + overlay
    if MARK in html:  # already stamped — strip the old block first
        start = html.index(MARK)
        end = html.index("END APOLLO REVIEW OVERLAY", start)
        end = html.index("-->", end) + 3
        html = html[:start] + html[end:]
    if "</body>" in html:
        html = html.replace("</body>", overlay + "\n</body>", 1)
    else:
        html = html + overlay
    out = out_path(src)
    with open(out, "w") as f:
        f.write(html)
    return out

def main(argv):
    if not argv:
        print(__doc__); return 1
    rc = 0
    for src in argv:
        if not os.path.exists(src):
            print("  ! not found:", src); rc = 1; continue
        out = make(src)
        print("  ✓ review copy:", os.path.relpath(out))
    return rc

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
