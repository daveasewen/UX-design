"""#261 N2 — re-point the nav review page at ORIGINAL (7647aaf) vs #261 N2 (working tree).

The page already carries a working theme/mode toggle that reaches into the srcdoc frames, so
this rewrites only the two things that went stale: the srcdoc payloads and the captions. It
edits in place rather than regenerating, so nothing else on the page (the state grid, the
composed frame, the projected cascade) can drift as a side effect.
"""
import html, re, subprocess, sys

ROOT = "/sessions/zen-funny-hawking/mnt/UX-design"
PAGE = ROOT + "/notes/_lanes/261-N-nav-review.html"
PAIRS = [
    ("Sidebar nav", "knowledge/snippets/Sidebar-nav.reference.html"),
    ("Navigations (top nav)", "knowledge/snippets/Navigations.reference.html"),
    ("Tab bar", "knowledge/snippets/Tab-bar.reference.html"),
]


def orig(rel):
    return subprocess.check_output(["git", "-C", ROOT, "show", "7647aaf:" + rel]).decode()


def now(rel):
    return open(ROOT + "/" + rel).read()


src = open(PAGE).read()
done = 0
for title, rel in PAIRS:
    for which, text in (("before", orig(rel)), ("after", now(rel))):
        pat = re.compile(r'(<iframe class="frame" data-frame title="%s, %s" height="\d+" srcdoc=")'
                         r'.*?("></iframe>)' % (re.escape(title), which), re.S)
        m = pat.search(src)
        if not m:
            sys.exit("no frame for %s / %s" % (title, which))
        src = src[:m.start()] + m.group(1) + html.escape(text, quote=True) + m.group(2) + src[m.end():]
        done += 1

src = src.replace('<figcaption class="t-cm-legal">Before — #260</figcaption>',
                  '<figcaption class="t-cm-legal">ORIGINAL — 7647aaf</figcaption>')
src = src.replace('<figcaption class="t-cm-legal">After — #261 nav design pass</figcaption>',
                  '<figcaption class="t-cm-legal">#261 N2 — Dave\'s six sentences enacted</figcaption>')
open(PAGE, "w").write(src)
print("re-pointed %d frame(s); captions now ORIGINAL / #261 N2" % done)
