"""V1 mkfix: canon fixtures (snippet body under .cn-<slug>, linking a given canon dir) for before/after."""
import os, re, sys
tag = sys.argv[1]
V = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
canon = os.path.join(V, tag, "canon"); snips = os.path.join(V, tag, "snips"); out = os.path.join(V, tag, "fix"); os.makedirs(out, exist_ok=True)
def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
for fn in sorted(os.listdir(snips)):
    n = fn.replace(".reference.html", "")
    src = open(os.path.join(snips, fn), encoding="utf-8").read()
    body = re.search(r"<body[^>]*>(.*)</body>", src, re.S).group(1)
    page = ('<!DOCTYPE html>\n<html lang="en" data-apollo-theme="mono" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
            '<title>%s V1 fixture %s</title>\n<link rel="stylesheet" href="file://%s/canon.css">\n<link rel="stylesheet" href="file://%s/type.css">\n'
            '<style>body{margin:0;padding:24px;background:var(--page);color:var(--text);}</style>\n</head>\n<body>\n<div class="cn-%s">\n%s\n</div>\n</body>\n</html>\n') % (n, tag, canon, canon, slug(n), body)
    open(os.path.join(out, n + ".html"), "w", encoding="utf-8").write(page)
print(tag, len(os.listdir(out)))
