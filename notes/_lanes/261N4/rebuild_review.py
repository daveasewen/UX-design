"""#261 N4 — re-point the nav review page at ORIGINAL (7647aaf) vs #261 N4 (working tree).

Same shape as notes/_lanes/261-N2-rebuild-review.py: it edits the srcdoc payloads and the
captions in place, so the rest of the page (state grid, composed frame, projected cascade,
theme switcher) cannot drift as a side effect. The N3 BAKE is reapplied here — a srcdoc has no
base URL, so `<link href="../canon/type.css">` 404s inside a frame and the page falls back to a
serif; the stylesheet is inlined instead.
"""
import html, re, subprocess, sys

ROOT = "/sessions/zen-funny-hawking/mnt/UX-design"
PAGE = ROOT + "/notes/_lanes/261-N-nav-review.html"
LINK = '<link rel="stylesheet" href="../canon/type.css">'
BAKE_HEAD = "<style>/* BAKED from knowledge/canon/type.css - srcdoc has no base URL, the link 404'd (N3) */\n"
TYPECSS = open(ROOT + "/knowledge/canon/type.css").read()
PAIRS = [
    ("Sidebar nav", "knowledge/snippets/Sidebar-nav.reference.html"),
    ("Navigations (top nav)", "knowledge/snippets/Navigations.reference.html"),
    ("Tab bar", "knowledge/snippets/Tab-bar.reference.html"),
]


def bake(text):
    if LINK in text:
        text = text.replace(LINK, BAKE_HEAD + TYPECSS + "\n</style>")
    return text


def orig(rel):
    return subprocess.check_output(["git", "-C", ROOT, "show", "7647aaf:" + rel]).decode()


src = open(PAGE).read()
done = 0
for title, rel in PAIRS:
    for which, text in (("before", orig(rel)), ("after", open(ROOT + "/" + rel).read())):
        pat = re.compile(r'(<iframe class="frame" data-frame title="%s, %s" height="\d+" srcdoc=")'
                         r'.*?("></iframe>)' % (re.escape(title), which), re.S)
        m = pat.search(src)
        if not m:
            sys.exit("no frame for %s / %s" % (title, which))
        src = src[:m.start()] + m.group(1) + html.escape(bake(text), quote=True) + m.group(2) + src[m.end():]
        done += 1

src = src.replace("<figcaption class=\"t-cm-legal\">#261 N2 — Dave's six sentences enacted</figcaption>",
                  "<figcaption class=\"t-cm-legal\">#261 N4 — labels uncropped, selected state de-greyed</figcaption>")
src = src.replace("<title>#261 N2 — nav family, Dave’s review enacted</title>",
                  "<title>#261 N4 — nav family, labels uncropped and the selected state de-greyed</title>")
src = src.replace('<h1 class="t-ed-display-2">Nav family — #261 N2</h1>',
                  '<h1 class="t-ed-display-2">Nav family — #261 N4</h1>')

N4 = """  <p class="t-ed-body"><b>#261 N4 — two sentences from Dave, both enacted.</b> Verbatim:
  <b>"the subagents need to be much more careful with the line-height cropping CSS pattern we have
  for labels, remove the background grey on the selected state"</b>.</p>
  <ol class="t-ed-body" style="max-width:78ch">
    <li><b>The crop.</b> The leading-trim default pasted into each snippet was a bare
    <code>:is(button,a,…,input[type=text],…)</code>. <code>:is()</code> takes the specificity of its
    heaviest branch, so it sat at (0,1,1) — above every one-class label override in the same file.
    <code>.nv-label{text-box-edge:text text}</code> was written and cascade-dead: the labels computed
    <code>cap alphabetic</code>, the box ended on the baseline, and the <code>overflow:hidden</code>
    that the ellipsis needs cut the descender off "Payments and transfers". The list is now wrapped in
    <code>:where()</code>, exactly as canon.css wraps it and for the reason canon.css gives — a default
    must not out-bid the authoring above it. <b>Driven in Chromium:</b> 336 label boxes × 4 themes × 2
    modes, <b>272 clipped, worst cut 5.5px → 0 clipped, worst cut 0.0px</b>; the 16px label box goes
    11px → 17px against 15px of ink. The specificity gate agrees: Sidebar-nav went from 4 cascade-dead
    overrides to none.</li>
    <li><b>The grey.</b> The current row's fill is removed on all three surfaces. It was the hover
    state's own signal worn permanently, which left hover nothing of its own to say. Current is now
    carried by <code>aria-current="page"</code>, the 3px indicator bar (a shape, not a hue) and a
    weight step on the label (400 → 500); the grey fill means hover, and only hover.</li>
  </ol>
"""
anchor = "</header>\n"
i = src.index(anchor)
src = src[:i] + N4 + src[i:]
open(PAGE, "w").write(src)
print("re-pointed %d frame(s); captions now ORIGINAL / #261 N4" % done)
