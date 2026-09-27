"""mkfix.py <tag> <canon.css path> <snippets dir> — canon fixture pages for lane B1 (#305).
Each fixture = a reviewed snippet's own <body> markup wrapped in its .cn-<slug> scope, linking the
given canon.css + type.css (the canon-gallery shape, gen_gallery.py). Writes notes/_lanes/305/B1/fix/<tag>/<Name>.html.
The snippet dir is read for MARKUP only; styling comes from the canon.css passed in, so a 'before'
fixture points at the backup copy and an 'after' fixture at the live canon."""
import os, re, sys
tag, canon, snips = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5))
TYPE = os.path.join(os.path.dirname(canon), "type.css")
OUT = os.path.join(ROOT, "notes/_lanes/305/B1/fix", tag); os.makedirs(OUT, exist_ok=True)
NAMES = ["Kpi-tile", "Template-dashboard-bento", "App-shell-side-nav", "Sidebar-nav", "Navigations",
         "Notifications", "Chart-line", "Chart-stacked-area", "Chart-donut", "Stat-card"]
def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
for n in NAMES:
    src = open(os.path.join(snips, n + ".reference.html"), encoding="utf-8").read()
    body = re.search(r"<body[^>]*>(.*)</body>", src, re.S).group(1)
    page = ('<!DOCTYPE html>\n<html lang="en" data-apollo-theme="mono" data-theme="light">\n<head>\n'
            '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s — B1 fixture (%s)</title>\n<link rel="stylesheet" href="file://%s">\n'
            '<link rel="stylesheet" href="file://%s">\n'
            '<style>body{margin:0;padding:24px;background:var(--page);color:var(--text);}</style>\n'
            '</head>\n<body>\n<div class="cn-%s">\n%s\n</div>\n</body>\n</html>\n') % (n, tag, canon, TYPE, slug(n), body)
    open(os.path.join(OUT, n + ".html"), "w", encoding="utf-8").write(page)
print("fixtures", tag, len(NAMES), "->", OUT)
