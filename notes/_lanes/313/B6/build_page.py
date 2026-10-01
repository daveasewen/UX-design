"""#313 B6 — builds notes/_REVIEW-313-B6-the-third-red-2026-10-01-v1.html (W-308ia).
Shell (house CSS, decisions overlay with per-call option buttons and the every-call export,
lightbox) is COPIED from notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html — the page
that asked him the question — with its page id, title, path and drop folder changed. Pictures:
img/*.png from shots_third_red.py; numbers: measures.json and scores.json beside this file.
Run from the repo root after shots_third_red.py and score_third_red.py."""
import html, json, pathlib
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
SRC = REPO / "notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html"
DST = REPO / "notes/_REVIEW-313-B6-the-third-red-2026-10-01-v1.html"
REL = "_lanes/313/B6/img/"
e = html.escape
M = json.load(open(HERE / "measures.json"))
S = json.load(open(HERE / "scores.json"))

def hexof(rgb):
    if not rgb: return "—"
    n = [int(x) for x in rgb[rgb.index("(") + 1:rgb.index(")")].split(",")[:3]]
    return "#%02X%02X%02X" % tuple(n)

def img(name, alt):
    w, h = Image.open(HERE / "img" / (name + ".png")).size
    return f'<img class="shot" src="{REL}{name}.png" width="{w}" height="{h}" alt="{e(alt)}">'

def fig(names, alt, tag, ttl, lis=()):
    li = "".join(f"<li>{x}</li>" for x in lis)
    return (f'<figure><figcaption><span class="tag">{tag}</span><span class="ttl">{ttl}</span></figcaption>'
            + "".join(img(n, alt) for n in names) + (f"<ul>{li}</ul>" if li else "") + "</figure>")

def probe_lis(key):
    m = M[key]; out = []
    if m.get("bar_fill"): out.append(f"Bar {hexof(m['bar_fill'])}, type {hexof(m['bar_text'])}")
    if m.get("ctx_fill"): out.append(f"Box tint {hexof(m['ctx_fill'])}, icon {hexof(m['ctx_icon'])}")
    if m.get("inline_icon"): out.append(f"Inline icon {hexof(m['inline_icon'])}")
    return out

def row(mode):
    return "".join([
        fig([f"A-mono-{mode}"], f"Mono {mode}: the message box as it ships", f"A · Mono · {mode}", "Keep: as it ships today", probe_lis(f"A-mono-{mode}")),
        fig([f"B-mono-{mode}"], f"Mono {mode}: the message box folded into Mono's reds", f"B · Mono · {mode}", "Fold into Mono's reds", probe_lis(f"B-mono-{mode}")),
        fig([f"C-mono-alert-{mode}", f"C-mono-banner-{mode}"], f"Mono {mode}: Alert and Banner, Mono's own message parts", f"C · Mono · {mode}", "Legacy's alone: Mono uses Alert and Banner",
            probe_lis(f"C-mono-alert-{mode}") + probe_lis(f"C-mono-banner-{mode}")),
        fig([f"ref-common-{mode}"], f"Common {mode}: the message box where #A8000B belongs", f"Common · {mode}", "For reference: Legacy's own", probe_lis(f"ref-common-{mode}")),
    ])

def call(cid, idx, q, lead, why, options, rec=""):
    return (f'<div class="dd-call" id="{cid}" data-options="{e("|".join(options))}" data-rec="{e(rec)}">'
            f'<span class="idx">{idx}</span><p class="q">{q}</p>'
            f'<p class="rec"><b>{lead}</b></p><p class="why">{why}</p><div class="dd-slot"></div></div>')

same = sum(1 for k in ("bar_fill", "bar_text", "ctx_fill", "ctx_icon", "inline_icon") for md in ("light", "dark")
           if M[f"A-mono-{md}"].get(k) == M[f"ref-common-{md}"].get(k))
assert same == 10, same

def srows():
    out = []
    for cand, rows in S.items():
        for r in rows:
            out.append(f'<tr><td>{e(cand.split(" · ")[0])}</td><td>{e(r["pair"])}</td>'
                       f'<td><span class="vals"><i style="background:{r["fg"]}"></i>{r["fg"]} on <i style="background:{r["bg"]}"></i>{r["bg"]}</span></td>'
                       f'<td>{r["wcag"]:.2f} : 1</td><td>{r["bloom"]}</td><td>{r["dance"]}</td></tr>')
    return "".join(out)

A_dark_bar = next(r for r in S["A · keep (Mono today = Common)"] if r["pair"] == "bar on the dark page")["wcag"]
B_ctx = next(r for r in S["B · fold into Mono's reds"] if r["pair"].startswith("contextual"))["wcag"]
trap = S["the trap · a bare re-point that keeps white type"][0]["wcag"]
A_type = S["A · keep (Mono today = Common)"][0]["wcag"]

head_top = f'''
<header>
  <div class="wrap">
    <div class="grid">
      <div>
        <p class="label">Apollo · review page · session 313</p>
        <h1>The third red</h1>
        <p class="sub">Why Mono's message box paints #A8000B, what it looks like folded into Mono's reds, and the three ways it can go. One call, and it is yours: no recommendation on this page.</p>
      </div>
      <p class="meta"><b>Review page v1 · Thursday 1 October 2026</b><br>Answers your note of 29 September: “I think there was a reason for this third red I think we have to investigate this separatly”<br>Session 313, lane B6<br>Status: an investigation. Nothing here is decided and nothing was changed.<br>Pictures are drawn in the cloud from the real part; your seat re-draws them with the real type.</p>
    </div>
  </div>
</header>

<section id="answer">
  <div class="wrap two">
    <p class="label">The answer first</p>
    <div>
      <p class="glance">There was a reason, and it is on record. On 20 July the message box (the Notifications part) was kept as Legacy's reference only, with no Mono message box yet, and the same day you ruled that Legacy's reds belong to Legacy. Two days later Mono's own message parts were briefed and built in Mono's colours: Alert, Toast and Banner. The plan was to tag Notifications to Legacy later. That never happened, so it still ships in every theme, and in Mono it paints Legacy's whole palette, not only the red.</p>
      <div class="stats four">
        <div><span class="n">20 July</span><span class="c">the sitting that kept the message box as Legacy's reference, and your ruling that Legacy's reds are Legacy's alone.</span></div>
        <div><span class="n">{same} of 10</span><span class="c">colours where Mono's message box equals Common's, measured tonight, light and dark: bar, type, tint, icon, inline icon. The one difference is Common's thin border, which you gave only Legacy and Supercharge.</span></div>
        <div><span class="n">{A_type:.2f} : 1</span><span class="c">white type on Legacy's red. On Mono's light red it is {trap:.2f} : 1, so folding means dark type, as your rule for Mono already says.</span></div>
        <div><span class="n">{A_dark_bar:.2f} : 1</span><span class="c">the bar against the dark page as it ships. The third red is the dimmest red on a dark Mono page.</span></div>
      </div>
    </div>
  </div>
</section>

<section id="why" class="grey">
  <div class="wrap">
    <p class="label">1 of 3 · why there is a third red</p>
    <h2>What the record says, in order</h2>
    <ol class="lists">
      <li>24 June. The message box is rebuilt to the full Figma family (four placements: contextual, global, inline, snackbar) in the old HSBC palette: #A8000B, #FFBB33, #305A85. <span class="src-note">knowledge/components/notifications.meta.json, $rebuild-2026-06-24</span></li>
      <li>20 July, your ruling R-D19. “these reds are valid for Legacy only — we have a new red for Mono and it is only used for status and RAG”. The record adds: any Legacy red resolving in a Mono surface is drift. <span class="src-note">knowledge/_proforma/_RAG-DECISIONS.md, R-D19</span></li>
      <li>20 July, the style sitting. Notifications is the one part given the verdict “keep-legacy”, with the note “keep for legacy reference only” and the flag “Kept only as legacy reference — no active Mono notification canon remains.” The written record turns it into an order: “DO NOT CONVERT — keep-legacy … its #A8000B is legitimate Apollo Legacy red (no active Mono notification canon exists yet). Retag as Legacy theme; never re-home.” <span class="src-note">reviews/_style-consolidation-decisions-2026-07-20.json · knowledge/_STYLE-PROVENANCE.md §A-AUTH</span></li>
      <li>20 July, R-D20. Mono's error, warning and information reds move onto Mono's own values and six parts are swept to match. “Notifications was NOT converted”: its Legacy colours are waived in the snippet check, “with the proper long-term fix being a retag to the Legacy theme (future build)”. <span class="src-note">knowledge/_proforma/_RAG-DECISIONS.md · the waiver: driftAllow in knowledge/snippets/Notifications.reference.html</span></li>
      <li>22 July. Mono's own message parts are briefed: Alert first, then Toast and Banner, “Mine snippets/Notifications for shape only (it is a LEGACY REFERENCE — do not convert it)”. <span class="src-note">notes/_briefs/2026-07-22-phase2-worker-B-brief.md</span></li>
      <li>8 and 11 August. You give Legacy's error red as #A8000B with white type (s131-D1); Mono's reds settle as #F6604C with dark type on it (s149-D1) and #DA1A00 for red on white (s151-D1).</li>
      <li>27 August to tonight. The fork is found (#221), put to you (#307), and kept open by you (#308). Tonight you took the drafted notification tree for cohort one, and that tree was drafted from this same Legacy reference file (s313-D16).</li>
    </ol>
    <p class="show">So the third red is not a typo. It is Legacy's red inside a part that was kept on purpose as Legacy's reference, whose move to Legacy was planned and never built. The waiver kept the checks quiet, and the showroom and canon show every part in every theme, so Mono has been drawing Legacy's message box ever since. It is not only the red: the amber (#FFBB33), the navy (#305A85) and the three tints in the same box are Legacy's too.</p>
  </div>
</section>

<section id="pictures">
  <div class="wrap">
    <p class="label">2 of 3 · the three ways, side by side</p>
    <h2>Mono's error message, three ways, with Common beside it</h2>
    <p class="src-note">Only the error placements are shown: contextual, the form version, the global bar with actions, and inline. Each picture is the real part with one style rule added for the candidate; Common is untouched in every candidate.</p>
    <p class="kicker">Light</p>
    <div class="quad">{row("light")}</div>
    <p class="kicker">Dark</p>
    <div class="quad">{row("dark")}</div>
    <p class="show">A keeps what ships: Mono and Common are the same box but for Common's thin border. B paints what Mono's own parts already paint: the box and its icon like Mono's Alert, the bar like Mono's Banner (light red, dark type), and the inline icon on white in the dark red your two-red law gives atoms on white. C keeps the message box for Legacy and lets Alert and Banner carry the message in Mono. One thing for your eye in B: the contextual icon on its pink tint reads {B_ctx:.2f} : 1, the same as Mono's Alert does today.</p>
  </div>
</section>

<section id="numbers" class="grey">
  <div class="wrap">
    <p class="label">3 of 3 · contrast and halation</p>
    <h2>Every pair the candidates paint, measured</h2>
    <p class="src-note">Contrast is WCAG. Bloom and dance are the repo's halation model (reviews/_rag_bloom_model.py), relative scores where 100 is a 40px white fill on #1A1A1A: higher bloom means the colour glows into what is around it, higher dance means fine type shimmers. Type is scored at a 2px stroke, icons at 20px (16px inline), the bar at 40px.</p>
    <div class="fk-wrap"><table class="stack fk"><thead><tr><th>Way</th><th>Pair</th><th>Colours</th><th>Contrast</th><th>Bloom</th><th>Dance</th></tr></thead><tbody>
    {srows()}
    </tbody></table></div>
    <p class="show">Your caveat on the forks was that some colours may have been chosen for halation and contrast together. Here that holds for the type: white on Legacy's red is strong ({A_type:.2f} : 1), and white on Mono's light red would fail ({trap:.2f} : 1), so a fold that only swapped the fill would break the bar. The fold on record changes the type with it.</p>
    {call("c1", "The call · the third red", "Which way should Mono's message box go?",
          "No recommendation: the conductor left this one to you.",
          "A keeps the July verdict as it is lived today. B makes one red per meaning in Mono, by rules you have already made, and carries the part forward to other libraries in Mono's colours. C finishes the July plan: the message box becomes Legacy's alone, and Mono's error messages come from Alert and Banner.",
          ["A · Keep it: Mono shows Legacy's message box", "B · Fold it into Mono's reds, like Alert and Banner", "C · Make it Legacy's alone; Mono uses Alert and Banner", "Keep it open"])}
    <p class="ids">Store W-308ia (open; closes when you have ruled) · rulings R-D19, R-D20, s131-D1, s149-D1, s151-D1, s308-D13, s313-D16 · whichever way you go, the amber, navy and tints in the same box follow it: the forks table's rows 1–6 and 21–23 (notes/_lanes/312/B/forks-29.json) wait on this call · pictures: notes/_lanes/313/B6/shots_third_red.py · numbers: notes/_lanes/313/B6/score_third_red.py</p>
  </div>
</section>
'''

tech = '''
<section id="tech">
  <div class="wrap">
    <p class="label mute">Technical</p>
    <div class="tech">
      <p>Pictures: <code>notes/_lanes/313/B6/shots_third_red.py</code> loads <code>showroom/notifications.html</code>, <code>alert.html</code> and <code>banner.html</code> over http from the repo root, sets theme and mode the page's own way, and adds one style block to the part's frame (candidate B's rule is written out in the driver). Drawn in the cloud with headless Chromium: the colours are exact, the type is a substitute for Univers. The seat re-draws them through the house path before this page is shown as final. Measured colours: <code>measures.json</code>; contrast and halation: <code>scores.json</code>, both beside the driver.</p>
      <p>Built by <code>notes/_lanes/313/B6/build_page.py</code>; house CSS, decisions bar and lightbox copied from <code>notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html</code>. Nothing inscribed, nothing in canon moved. Report: <code>notes/_subreports/2026-10-01-313-B6.md</code>.</p>
    </div>
  </div>
</section>

<footer>
  <div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
    <span>Apollo · review page · the third red · v1 · 2026-10-01 · session 313 · lane B6</span>
    <span>Nothing here is decided. The call takes a decision below it.</span>
  </div>
</footer>
'''

extra_css = '''
<style>
#why ol.lists{margin:0 0 var(--s4);padding-left:1.2em;max-width:52em}
#why ol.lists li{margin:0 0 .7em}
#why ol.lists .src-note{display:block;margin-top:.2em}
.quad figure img.shot + img.shot{margin-top:8px}
</style>'''

src = SRC.read_text()
head = src[:src.index("</head>")]
head = head.replace("<title>What you asked to see</title>", "<title>The third red</title>", 1)
assert "<title>The third red</title>" in head
head += extra_css + "\n</head>\n"
i_body = src.index("<body>"); i_back = src.index("</a>", i_body) + 4
backlink = src[i_body:i_back]
overlay = src[src.index('<style>\n.dd-box'):]

def rep(s, a, b):
    assert s.count(a) >= 1, a[:70]
    return s.replace(a, b, 1)
overlay = rep(overlay, "page:'review-307-what-you-asked-to-see-v1', title:'What you asked to see, review page v1', path:'notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html',",
              "page:'review-313-b6-the-third-red-v1', title:'The third red, review page v1', path:'notes/_REVIEW-313-B6-the-third-red-2026-10-01-v1.html',")
overlay = rep(overlay, "prefix:'c307'", "prefix:'c313b6'")
overlay = rep(overlay, "drop it in notes/_lanes/307/", "drop it in notes/_lanes/313/")

i_foot = src.index("<footer>")
page = head + "<body>" + backlink[len("<body>"):] + "\n" + head_top + tech + "\n" + overlay
DST.write_text(page)
print(DST.relative_to(REPO), len(page), "calls:", page.count('class="dd-call"'), "imgs:", page.count('<img class="shot"'))
