"""#307 lane C — builds notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html.
Head (house CSS) and the decisions overlay + lightbox are COPIED from the approved
notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html; only what the content needs is changed:
per-call option buttons (data-options / data-rec), an export that carries every call, the
'Save as file' label and the drop-folder line. Pictures are the PNGs under shots/, referenced
by relative path from notes/."""
import json, re, html, pathlib
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
SRC = REPO / "notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html"
DST = REPO / "notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html"
REL = "_lanes/307/C/shots/"
e = html.escape

def img(name, alt, show_scale=None, cls="shot"):
    """show_scale = how many image pixels per CSS pixel on the page (the capture's device scale
    by default, so the part shows at its real size; 2 for a 4x capture shows it at twice size)."""
    p = HERE / "shots" / name
    w, h = Image.open(p).size
    if show_scale is None:
        show_scale = 4 if "-4x" in name or name.startswith("2-cal-") else (1 if name.startswith("4-") else 2)
    cw, ch = round(w / show_scale), round(h / show_scale)
    return f'<img class="{cls}" src="{REL}{name}" width="{cw}" height="{ch}" alt="{e(alt)}">'

def fig(name, alt, tag, ttl, lis=(), bad=False, scale=None):
    li = "".join(f"<li>{x}</li>" for x in lis)
    bc = ' class="bad"' if bad else ''
    return (f'<figure{bc}><figcaption><span class="tag">{tag}</span>'
            f'<span class="ttl">{ttl}</span></figcaption>{img(name, alt, scale)}'
            + (f"<ul>{li}</ul>" if li else "") + "</figure>")

def call(cid, idx, q, rec_lead, why, options, rec):
    assert rec in options, (cid, rec)
    return (f'<div class="dd-call" id="{cid}" data-options="{e("|".join(options))}" data-rec="{e(rec)}">'
            f'<span class="idx">{idx}</span><p class="q">{q}</p>'
            f'<p class="rec"><b>{rec_lead}</b></p><p class="why">{why}</p>'
            f'<div class="dd-slot"></div></div>')

def ids(t): return f'<p class="ids">{t}</p>'

cap = json.load(open(HERE / "shots/1-caption-measures.json"))
THEMES = [("mono", "Mono"), ("legacy", "Legacy"), ("console", "Console"), ("supercharge", "Supercharge")]

# ---------------------------------------------------------------- 1 · captions
def capfig(t, T, mode):
    m = cap[f"{t}-{mode}"]
    if mode == "dark":
        lis = [f"Caption {m['cap_hex']} on page {m['page_hex']}",
               f"Lifts {abs(m['dL']):.0f} points of lightness off the page",
               f"White text {m['ink_on_cap']:.1f} : 1"]
    else:
        lis = [f"Caption {m['cap_hex']} on page {m['page_hex']}", "Not moved by the lift"]
    return fig(f"1-caption-{t}-{mode}.png", f"{T} theme, {mode} mode: the capsule card with its dark caption",
               f"{T} · {mode}", "Capsule, dark-grey caption", lis)

s1 = f'''
<section id="item-1" class="grey">
  <div class="wrap">
    <p class="label">1 of 5 · the dark caption</p>
    <h2>Does the dark caption sit right in all four themes?</h2>
    <p class="ask">You asked to see the four themes' dark captions side by side once, then close. Each picture is the same capsule card from the bento rails page, in dark mode, with only the theme switched.</p>
    <div class="quad">{"".join(capfig(t, T, "dark") for t, T in THEMES)}</div>
    <p class="kicker">The same card in light mode, for reference</p>
    <div class="quad">{"".join(capfig(t, T, "light") for t, T in THEMES)}</div>
    <p class="show">Mono, legacy and console lift by the same amount, from neutral 5 (#313131). Supercharge lifts from its own warm ramp (warm 5, #312C26), a little less, and stays warm; before your ruling its caption sat darker than its page. Light mode is as it was in all four. Today only console and, from tonight, mono can pick this caption; legacy and supercharge have the lift ready for when they can.</p>
    {call("c1", "1 · The dark caption", "Close the dark caption lift in all four themes?", "Recommend close it.",
          "Because every theme now shows a capsule you can see, lifted by your own rule of aligning to the neutral primitives, and light mode did not move.",
          ["Close it: the four lifts are right", "Change one theme (say which in the note)", "Keep it open"],
          "Close it: the four lifts are right")}
    {ids("Store W-307qi (from W-208) · ruling s220-D1 · values from CAPTION_GROUND_MINTS, knowledge/_render/gen_bento_matrix_217.py · rendered from showroom/_foundations/bento-rails.html, card “Capsule — Dark grey”")}
  </div>
</section>'''

# ---------------------------------------------------------------- 2 · tree mark and ring
def cellrow(mode):
    cells = [("todayonly", "Today", "a ring"), ("selonly", "Chosen", "a filled square"),
             ("todaysel-now", "Both, now", "the ring is page colour"),
             ("todaysel-proposal", "Both, proposal", "ring set inside the square"),
             ("todaysel-old", "Both, before the repair", "black ring on black")]
    out = []
    for k, tag, ttl in cells:
        bc = ' class="bad"' if k in ("todaysel-now", "todaysel-old") else ''
        out.append(f'<figure{bc}><figcaption><span class="tag">{tag}</span>'
                   f'<span class="ttl">{ttl}</span></figcaption>'
                   f'{img(f"2-cal-{k}-{mode}.png", f"Calendar day, {tag.lower()}, {mode} mode, at twice size", 2)}</figure>')
    return '<div class="cells">' + "".join(out) + "</div>"

s2 = f'''
<section id="item-2">
  <div class="wrap">
    <p class="label">2 of 5 · the tree mark and the ring</p>
    <h2>How is a chosen tree item marked, and can you see today when it is also the chosen day?</h2>
    <p class="ask">You said yes, the date picker uses the calendar part, and asked to see these two marks as pictures. Both are drawn from the parts' own reference files, light and dark.</p>

    <p class="kicker">The tree's chosen item, beside the side navigation's “you are here”</p>
    <div class="quad">
      {fig("2-tree-states-light.png", "Tree states, light: the chosen node has a grey ground and a black bar on its left edge", "Tree · light", "Chosen: grey ground, black bar", ["3px bar in black, on the left", "Label not clipped (21 of 21px)"])}
      {fig("2-tree-states-dark.png", "Tree states, dark: the chosen node has a dark grey ground and a white bar", "Tree · dark", "Chosen: grey ground, white bar", ["3px bar in white, on the left"])}
      {fig("2-nav-current-light.png", "Side navigation, light: the current page has a red bar on its left", "Side navigation · light", "You are here: red bar", ["3px bar in red #DB0011, no ground"])}
      {fig("2-nav-current-dark.png", "Side navigation, dark: the current page has a red bar on its left", "Side navigation · dark", "You are here: red bar", ["The same red in dark"])}
    </div>
    <p class="show">The tree marks a chosen item with a grey ground and a black bar (white in dark). The side navigation marks the page you are on with a red bar. The builder kept them apart on purpose: “the thing I chose” and “the page I am on” mean different things, and whether they share a mark was left to you.</p>
    {call("c2a", "2 · first call · the tree mark", "Should the tree's chosen mark stay black, apart from the navigation's red?", "Recommend keep it black.",
          "Because red already means “you are here” in the navigation, and one mark with two meanings would make a page that has both hard to read.",
          ["Keep the black bar for chosen", "Use the red bar for both", "Keep it open"], "Keep the black bar for chosen")}

    <p class="kicker">The calendar day, at twice size · light</p>
    {cellrow("light")}
    <p class="kicker">The same, dark</p>
    {cellrow("dark")}
    <p class="show">Today is a ring; chosen is a filled square. When one day is both, the part now draws the ring in the page colour. That ring meets the page at the cell's edge, so it cannot be seen as a ring: the square just looks 2px smaller all round than a plain chosen day. Before the repair it was worse, a black ring on black. The fourth picture is a one-line change, drawn on the real part, that sets the ring inside the square so it reads as a ring.</p>

    <p class="kicker">The date picker, open on today (Monday 28 September) with today chosen</p>
    <div class="pair3">
      {fig("2-dp-panel-light.png", "Date picker panel, light, 28 September chosen and today", "Date picker · light", "28 is today and chosen", ["Fill #1A1A1A, ring #FFFFFF, 2px"], bad=True)}
      {fig("2-dp-panel-dark.png", "Date picker panel, dark, 28 September chosen and today", "Date picker · dark", "28 is today and chosen", ["Fill #FFFFFF, ring #1A1A1A, 2px"], bad=True)}
    </div>
    <p class="show">The date picker draws it the same way as the calendar, so whichever you choose holds for both once the date picker uses the calendar.</p>
    {call("c2b", "2 · second call · the ring", "For a day that is both today and chosen, keep the ring as it is or set it inside the square?", "Recommend setting the ring inside the square.",
          "Because the ring as it is only shows as a slightly smaller square, and today should be seen, not guessed.",
          ["Set the ring inside the square (the proposal)", "Keep it as it is now", "Keep it open"], "Set the ring inside the square (the proposal)")}
    {ids("Store W-307qr (from W-72); the date picker using the calendar is W-307qq · receipt notes/_receipts/2026-08-20-210-wave4-laneA-calendar-tree.md, questions 9 and 19 · the page-colour ring is #211 lane R3, in knowledge/snippets/Calendar.reference.html and Date-picker.reference.html · the proposal is one rule, not in canon: box-shadow: inset 0 0 0 3px var(--text), inset 0 0 0 5px var(--page)")}
  </div>
</section>'''

# ---------------------------------------------------------------- 3 · the eight parts
PROMOTE = ["Promote", "Rework", "Delete", "Keep it open"]
parts = [
 ("standing-order-mandate-row", "3.1 · Standing order and Direct Debit row", "-top",
  "One row per regular payment: who, how often, the amount, the next date, a status and a manage button. It has the same bones as the transaction row you made a variant of list items tonight.",
  "Should the standing order and Direct Debit row be its own part?", "Recommend rework it as a variant of list items.",
  "Because it is the same shape as the transaction row, and one list part with variants is easier to keep right than two.",
  ["Promote as its own part", "Rework: a variant of list items", "Delete", "Keep it open"], "Rework: a variant of list items", None),
 ("limits-meter", "3.2 · Limits meter", "-trim",
  "Daily and monthly limits as bars. You already folded it into one Meter with the progress bar on 20 August (“keep as one meter”), and its catalogue entry became a short name for Meter. Nothing is left to rule.",
  "Close the limits meter as Meter's limits form?", "Recommend close it: it is already part of Meter.",
  "Because you ruled it on 20 August and the fold is done.",
  ["Close: it is already part of Meter", "Promote on its own", "Delete", "Keep it open"], "Close: it is already part of Meter", None),
 ("range-slider", "3.3 · Range slider", "-trim",
  "Two handles on one track, for a range of amounts. A single Slider part already exists, and your rulings of 15 September on when a slider may be used apply to it.",
  "Should the range slider be its own part?", "Recommend rework it as Slider's two-handle form.",
  "Because a range is a slider with two handles, and your slider rules already cover it.",
  ["Promote as its own part", "Rework: Slider's two-handle form", "Delete", "Keep it open"], "Rework: Slider's two-handle form", None),
 ("rating", "3.4 · Rating", "-trim",
  "Stars, to rate something or to show an average. The average row is broken: the filled stars sit on top of the empty ones out of step (close-up above). The stars are ink, because there is no gold in the house colours.",
  "Promote, rework or delete the rating?", "Recommend delete it.",
  "Because no banking page asks for stars today, and it can come back when one does.",
  PROMOTE, "Delete", ("3-rating-aggregate-4x.png", "Close-up at twice size: the average row, filled stars out of step with the empty ones", "Close-up · twice size", "The average: stars out of step")),
 ("transfer-list", "3.5 · Transfer list", "-trim",
  "Two lists with buttons to move items across. Two faults show. The “move all” arrows are drawn with only half of the double-arrow icon, so they look the same as “move one” (close-up above). And the select-all box sits above its label, not beside it.",
  "Promote, rework or delete the transfer list?", "Recommend rework it, then promote.",
  "Because the part is sound and both faults are small and plain to see.",
  ["Promote as it is", "Rework, then promote", "Delete", "Keep it open"], "Rework, then promote",
  ("3-transfer-list-buttons-4x.png", "Close-up at twice size: the four move buttons, all single arrows", "Close-up · twice size", "Move one and move all look the same")),
 ("split-button", "3.6 · Split button", "-trim",
  "A main action with a small arrow that opens more actions. It looks right in both modes. The graph already has a rule that points at it: a modal gives way to a split button or a drop-down when either would do (your yes on 27 September).",
  "Promote, rework or delete the split button?", "Recommend promote it.",
  "Because a rule already names it and there is no fault to fix.",
  PROMOTE, "Promote", None),
 ("fab", "3.7 · Floating add button", "-trim",
  "A floating add button, bottom right, 56px square. You ruled on 15 September that it may be used at any screen size but never with back-to-top on the same screen. Three stray page rules in its overlay are already queued for repair from tonight's answers.",
  "Promote, rework or delete the floating add button?", "Recommend rework it, then promote.",
  "Because the repair is already queued, and once it lands nothing else stands in the way.",
  ["Promote as it is", "Rework, then promote", "Delete", "Keep it open"], "Rework, then promote", None),
 ("back-to-top", "3.8 · Back to top", "-trim",
  "A small button that takes you back to the top of a scrolling area. The button is right. The reference page around it is not: its live demo text falls back to Times, a font the house never uses, and a note shows an empty box where a symbol should be. You ratified when it appears on 15 September.",
  "Promote, rework or delete back to top?", "Recommend rework the reference page, then promote.",
  "Because the part itself is right; only the page that shows it is wrong.",
  ["Promote as it is", "Rework, then promote", "Delete", "Keep it open"], "Rework, then promote", None),
]
blocks = []
for i, (slug, kick, suf, show, q, rl, why, opts, rec, close) in enumerate(parts, 1):
    nm = kick.split(" · ", 1)[1]
    b = f'''<p class="kicker">{kick}</p>
    <div class="pair3">
      {fig(f"3-{slug}-light{suf}.png", f"{nm}, reference part, light", f"{nm} · light", "From its reference part")}
      {fig(f"3-{slug}-dark{suf}.png", f"{nm}, reference part, dark", f"{nm} · dark", "From its reference part")}
    </div>'''
    if close:
        b += f'<div class="pair3 one">{fig(close[0], close[1], close[2], close[3], bad=True, scale=2)}</div>'
    b += f'<p class="show">{show}</p>' + call(f"c3-{i}", f"3 · part {i} of 8", q, rl, why, opts, rec)
    blocks.append(b)
s3 = f'''
<section id="item-3" class="grey">
  <div class="wrap">
    <p class="label">3 of 5 · the other eight wave-3 parts</p>
    <h2>The other eight wave-3 parts: promote, rework or delete each?</h2>
    <p class="ask">You made the transaction row a variant of list items. Here are the other eight, each photographed from its own reference part, light and dark, with a call for each.</p>
    {"".join(blocks)}
    {ids("Store W-307qu (from W-63); the transaction row is W-307qt; the floating button's repair is W-307qy · receipts notes/_receipts/2026-08-20-209-wave3-laneA-fintech-rows.md, -laneB-selection-controls.md, -laneC-action-chrome.md · rulings s210-D1, s210-D5, s272-D36, s272-D40, s305-D25, s272-D5, s272-D73")}
  </div>
</section>'''

# ---------------------------------------------------------------- 4 · the five
FORMS = [("form-layout", "Form layout"), ("date-picker", "Date picker"), ("date-range-picker", "Date range picker"),
         ("time-picker", "Time picker"), ("amount-input", "Amount input"), ("file-upload", "File upload"),
         ("secure-entry", "Passcode and PIN"), ("textarea", "Text area")]
thumbs = "".join(f'<figure><figcaption><span class="tag">Built</span><span class="ttl">{n}</span></figcaption>{img(f"4-{s}.png", n + ", top of its reference part", 2)}</figure>' for s, n in FORMS)
s4 = f'''
<section id="item-4">
  <div class="wrap">
    <p class="label">4 of 5 · the five the build did not make</p>
    <h2>The five parts the wave-3 build chose not to make: what were they?</h2>
    <p class="ask">You asked to see the five and the reasons, rather than agree to leave them unbuilt.</p>
    <p class="glance" style="margin-top:var(--s3)">There were never five unbuilt parts. The build lane of 25 August was sent to make eight form parts, found all eight already built and checked, and made none. Its five were five questions it left for you. The card that asked you mixed the two up.</p>
    <p class="kicker">The eight it was sent to build, as they stand tonight</p>
    <div class="quad thumbs">{thumbs}</div>
    <p class="kicker">Its five questions, and where each stands now</p>
    <table class="stack five"><thead><tr><th>The question</th><th>Where it stands</th></tr></thead><tbody>
      <tr><td data-l="The question">Is wave 3 finished, or should it become a quality pass over the forms?</td><td data-l="Where it stands">Never answered. Nothing waits on it: all eight parts are built and pass their checks.</td></tr>
      <tr><td data-l="The question">The register's one real gap was the logo. Does it want a lane?</td><td data-l="Where it stands">Done. You ruled the logo sizes on 18 September and the masters were drawn.</td></tr>
      <tr><td data-l="The question">An old spreadsheet column misled a brief. Retire it, rename it, or leave it?</td><td data-l="Where it stands">Done the same day: renamed so it reads as frozen history.</td></tr>
      <tr><td data-l="The question">File upload marked errors differently from its seven siblings. Fault, or right?</td><td data-l="Where it stands">Fixed the same day: it now flags the field in error like the others.</td></tr>
      <tr><td data-l="The question">Should the two other wave-3 lanes stop?</td><td data-l="Where it stands">They did. Both found the same thing and built nothing.</td></tr>
    </tbody></table>
    {call("c4", "4 · The five", "Close it: nothing was left unbuilt, and four of the five questions are done?", "Recommend close it.",
          "Because the one question still open, whether wave 3 is finished, has nothing waiting on it.",
          ["Close it", "Keep the first question open (is wave 3 finished?)", "Keep it open"], "Close it")}
    {ids("Store W-307qw (from W-151) · receipt notes/_receipts/2026-08-25-wave3-alpha.md (“the lane built ZERO of its eight, on purpose”; “Decisions for Dave” 1–5) · the same day's commit 941c92d7 (frozen column fenced, forms family repaired) · reviews/ITINERARY-STATUS-2026-08-25-v4.json column itinerary_status_2026_07_14_FROZEN · ruling s282-D3 · sibling receipts …-wave3-beta.md, …-wave3-gamma.md")}
  </div>
</section>'''

# ---------------------------------------------------------------- 5 · reds and forks
reds = [("#DA1A00", "Dark red", "the one for red on white (your two-red law)"),
        ("#F6604C", "Light red", "the one for everywhere else (your two-red law)"),
        ("#A8000B", "The third red", "mono's message box; legacy throughout"),
        ("#B92F1E", "Console and supercharge's red", "both modes")]
sw = "".join(f'<div><span class="chip" style="background:{h}"></span><b>{n}</b><span>{h} · {w}</span></div>' for h, n, w in reds)
redq = lambda part, mode: "".join(fig(f"5-{part}-{t}-{mode}.png", f"{T} theme, {mode} mode, {part.replace('-', ' ')} in its error state", f"{T} · {mode}", "") for t, T in THEMES)
forks = json.load(open(HERE / "shots/5-forks-classified.json"))
real = [f for f in forks if f["bucket"] in ("A", "A2")]
real.sort(key=lambda f: (0 if f["prop"] == "--err" else 1, f["bucket"], f["prop"], f["theme"], f["mode"]))
def where(f):
    s = re.sub(r'\[data-apollo-theme="\w+"\]\s*', "", f["b_sel"]); s = re.sub(r'\[data-theme="dark"\]\s*', "", s)
    s = s.replace(":where(", "").replace(")", "").strip()
    return s
def hx(v): return v if re.match(r"^#[0-9a-fA-F]{6}$", v) else None
rows = []
for f in real:
    a, b = hx(f["a_val"]), hx(f["b_val"])
    led = "declared as meant (#215)" if f["ledger"].startswith("DECLARED") else "not ruled"
    kind = "typed instead of the token" if f["bucket"] == "A" else "near miss"
    ec = ' class="err"' if f["prop"] == "--err" else ''
    rows.append(f'<tr{ec}><td data-l="Name"><code>{e(f["prop"])}</code></td>'
                f'<td data-l="Theme">{e(f["theme"])} · {e(f["mode"])}</td><td data-l="Where">{e(where(f))}</td>'
                f'<td data-l="The two values"><span class="vals"><i style="background:{a}"></i>{a}<i style="background:{b}"></i>{b}</span></td>'
                f'<td data-l="Kind">{kind}</td><td data-l="Record">{led}</td></tr>')
nA = sum(1 for f in real if f["bucket"] == "A"); nA2 = len(real) - nA
s5 = f'''
<section id="item-5" class="grey">
  <div class="wrap">
    <p class="label">5 of 5 · the third red and the 29 forks</p>
    <h2>How many reds does an error use, and which colour forks are real faults?</h2>
    <blockquote>I want to check this visually<cite>Dave · your note on the third red · sitting page, Monday 28 September, 21:05</cite></blockquote>
    <p class="kicker">The reds, as values</p>
    <div class="reds">{sw}</div>
    <p class="kicker">The error field, in each theme · light</p>
    <div class="quad">{redq("input-fields", "light")}</div>
    <p class="kicker">The error field · dark</p>
    <div class="quad">{redq("input-fields", "dark")}</div>
    <p class="kicker">The error message box, in each theme · light</p>
    <div class="quad">{redq("notifications", "light")}</div>
    <p class="kicker">The error message box · dark</p>
    <div class="quad">{redq("notifications", "dark")}</div>
    <p class="show">Mono's field paints the light red, #F6604C, in both modes, and mono's message box paints #A8000B. So on one mono page an error field and an error message are two different reds: that is the third red. Legacy uses #A8000B throughout, as its own red. Console and supercharge use a fourth, #B92F1E, in both modes. One more thing for your eye: your two-red law puts the dark red on white, and mono's field on white paints the light red.</p>
    {call("c5a", "5 · first call · the third red", "In mono, fold the third red into the one error red?", "Recommend fold it: mono's message box takes mono's error red, and legacy keeps its own.",
          "Because one theme should say “error” in one red, and #A8000B is legacy's colour, not mono's.",
          ["Fold it into mono's error red", "Keep the third red as its own shade", "Keep it open"], "Fold it into mono's error red")}

    <p class="kicker">The 29 colour forks, run again tonight</p>
    <p class="src-note">A fork is one colour name carrying two values in different places. Each row shows both values side by side.</p>
    <div class="fk-wrap"><table class="stack fk"><thead><tr><th>Name</th><th>Theme</th><th>Where</th><th>The two values</th><th>Kind</th><th>Record</th></tr></thead><tbody>
    {"".join(rows)}
    </tbody></table></div>
    <p class="show">In August, 29 looked like real faults: 23 where a part typed a colour instead of using its token, and 6 near misses. Run again tonight by the same rule, all 29 are still there. The rule counts {nA + nA2} tonight: the extra one is a twin, because canon sets “common” alongside legacy. None of them was among the four you declared as meant on 27 September: those were chart line and fill tones and the compact table's padding. So the four were not what was left of the 29.</p>
    {call("c5b", "5 · second call · the forks", "The 29 forks: hand them to Claude to settle within your rules?", "Recommend hand them to Claude, and bring back only the ones that are a real colour choice.",
          "Because most are a part typing a colour its token already gives, which is a repair, not a decision.",
          ["Hand them to Claude to settle", "Show me each one", "Keep it open"], "Hand them to Claude to settle")}
    {ids("Store W-229 (kept open tonight) · report notes/_subreports/2026-08-27-221-laneB.md §9 · ledger knowledge/_TOKEN-FORK-LEDGER.json · rulings s151-D1, s305-D41 · rendered from showroom/input-fields.html and showroom/notifications.html · re-run: knowledge/_validate_token_forks.py --strict --json, ledger unchanged either side, classified by notes/_lanes/307/C/classify_forks.py")}
  </div>
</section>'''

s6 = '''
<section id="item-6">
  <div class="wrap">
    <p class="label mute">6 · the fresh-session dashboard run</p>
    <h2>The fresh-session dashboard run</h2>
    <div class="slot-note"><p>Another lane is running this now. The conductor puts the result here.</p>
    <!-- COLDRUN-SLOT -->
    </div>
  </div>
</section>'''

head_top = '''
<header>
  <div class="wrap">
    <div class="grid">
      <div>
        <p class="label">Apollo · review page · session 307</p>
        <h1>What you asked to see</h1>
        <p class="sub">Five things from your answers tonight, each drawn from the real parts, each with a call and a recommendation.</p>
      </div>
      <p class="meta"><b>Review page v1 · Monday 28 September 2026</b><br>Answers your 21:18 export of the sitting page<br>Session 307, lane C<br>Status: recommendations. Nothing here is decided.<br>Every picture is rendered at your seat from the parts' own reference files and canon.</p>
    </div>
  </div>
</header>

<section id="answer">
  <div class="wrap two">
    <p class="label">The answer first</p>
    <div>
      <p class="glance"><b>Recommend:</b> close the dark captions; keep the tree's mark black and set today's ring inside the chosen square; promote the split button, fold three parts into ones you have, rework three and delete the rating; close the “five unbuilt parts”, as nothing was unbuilt; take the third red out of mono and hand the 29 forks to Claude.</p>
      <div class="stats four">
        <div><span class="n">11</span><span class="c">points the dark caption lifts off the page in mono, legacy and console. Supercharge lifts 9, and stays warm.</span></div>
        <div><span class="n">2<small>px</small></span><span class="c">all that tells today from a plain chosen day now: the square is a little smaller.</span></div>
        <div><span class="n">3</span><span class="c">faults the pictures show on the eight parts: stars out of step, look-alike arrows, a stray font.</span></div>
        <div><span class="n">0</span><span class="c">parts the wave-3 build left unbuilt. All eight it was sent for already existed.</span></div>
      </div>
    </div>
  </div>
</section>'''

tech = '''
<section id="tech" class="grey">
  <div class="wrap">
    <p class="label mute">Technical</p>
    <div class="tech">
      <p>Every picture was rendered at your seat through the house path (<code>ensure_env.sh</code>, <code>seat_env.sh</code>, headless Chromium, <code>page.goto("file://…")</code>), from the parts' own files. Drivers: <code>notes/_lanes/307/C/shots_1_captions.py</code> (bento rails page, theme and mode switched the page's own way, the card's console scope taken off so it sits in the page theme), <code>shots_2_tree_ring.py</code> (Calendar, Date-picker, Tree and Sidebar-nav reference files; the “before” and “proposal” cells are one-rule mutations on the real part), <code>shots_3_wave3.py</code> and <code>shots_4_formparts.py</code> (reference files, light and dark), <code>shots_5_reds.py</code> (catalogue pages, theme and mode buttons clicked). Measures beside each driver's pictures in <code>notes/_lanes/307/C/shots/*.json</code>.</p>
      <p>Built by <code>notes/_lanes/307/C/build_page.py</code>; house CSS, decisions bar and lightbox copied from <code>notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html</code>, with option buttons per call and an export that lists every call. Nothing inscribed, no git write. Report: <code>notes/_subreports/2026-09-28-307-C-what-you-asked-to-see.md</code>.</p>
    </div>
  </div>
</section>

<footer>
  <div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
    <span>Apollo · review page · what you asked to see · v1 · 2026-09-28 · session 307 · lane C</span>
    <span>Nothing here is decided. Each call takes a decision below it.</span>
  </div>
</footer>'''

extra_css = '''<style>
/* #307 lane C additions */
.quad{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin:var(--s3) 0 var(--s2)}
.quad>figure,.cells>figure{margin:0;background:var(--white);padding:var(--s2)}
.quad figcaption,.cells figcaption{margin:0 0 var(--s1)}
.quad .tag,.cells .tag{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;line-height:1.5;color:var(--grey-6)}
.quad .ttl,.cells .ttl{display:block;font-size:14px;font-weight:500;line-height:1.4;margin-top:2px}
.quad ul{list-style:none;padding:0;margin:var(--s1) 0 0;font-size:13px;line-height:1.5;color:var(--grey-8)}
.quad li{padding:3px 0;border-top:1px solid var(--grey-2)}
.cells{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin:var(--s2) 0}
.cells .bad .tag{color:var(--accent)}
.pair3.one{grid-template-columns:1fr}
.quad.thumbs{grid-template-columns:repeat(4,1fr)}
.show{max-width:48em;color:var(--grey-8);margin:var(--s2) 0 0}
.ids{font-size:12px;line-height:1.55;color:var(--grey-6);margin:var(--s4) 0 0;max-width:72em;overflow-wrap:anywhere}
.reds{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin:var(--s2) 0}
.reds>div{background:var(--white);padding:var(--s2);font-size:13px;line-height:1.45}
.reds .chip{display:block;height:56px;margin-bottom:var(--s1)}
.reds b{display:block;font-weight:500;font-size:14px}
.reds span:not(.chip){color:var(--grey-7)}
.fk-wrap{overflow-x:auto}
table.fk{font-size:13px}
table.fk code{font-family:ui-monospace,Menlo,monospace;font-size:12px}
table.fk .vals{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
table.fk .vals i{display:inline-block;width:28px;height:18px;border:1px solid var(--grey-3)}
table.fk tr.err td{background:var(--grey-1)}
@media(min-width:821px){table.five td:first-child{width:45%}}
.slot-note{border:1px dashed var(--grey-5);padding:var(--s3);color:var(--grey-7);max-width:48em}
.slot-note p{margin:0}
.dd-box .dd-head{flex-direction:column;align-items:flex-start;justify-content:flex-start;text-align:left}
.dd-box .dd-chip{text-transform:none;letter-spacing:0;font-size:13px;line-height:1.35;text-align:left;padding:.45rem .7rem}
.dd-box .dd-chip em{font-style:normal;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-left:.4rem}
.dd-box .dd-chip.on em{color:inherit}
@media(max-width:820px){
  .quad.thumbs{grid-template-columns:1fr 1fr}.reds{grid-template-columns:1fr 1fr}
  .cells{grid-template-columns:repeat(3,1fr)}
}
@media(max-width:520px){
  .quad{grid-template-columns:1fr}.quad.thumbs{grid-template-columns:1fr 1fr}
  .cells{grid-template-columns:1fr 1fr}.cells>figure:last-child{grid-column:1/-1}
}
</style>'''

src = SRC.read_text()
i_head = src.index("</head>")
head = src[:i_head]
head = head.replace("<title>Call 27 in pictures</title>", "<title>What you asked to see</title>", 1)
assert "<title>What you asked to see</title>" in head
head += extra_css + "\n</head>\n"
i_body = src.index("<body>")
i_back_end = src.index("</a>", i_body) + 4
backlink = src[i_body:i_back_end]
assert "All review pages" in backlink
i_ov = src.index('<style>\n.dd-box')
overlay = src[i_ov:]

def rep(s, a, b, n=1):
    assert s.count(a) >= 1, a[:60]
    return s.replace(a, b, n)
overlay = rep(overlay, "page:'review-305-call-27-visuals-v1', title:'Call 27 in pictures, review page v1', path:'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html',",
              "page:'review-307-what-you-asked-to-see-v1', title:'What you asked to see, review page v1', path:'notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html',")
overlay = rep(overlay, "prefix:'call27'", "prefix:'c307'")
overlay = rep(overlay, "items.push({ id:id, kind:t.kind, num:num, title:title, host:",
              "items.push({ id:id, kind:t.kind, num:num, title:title, opts:(el.getAttribute('data-options')||'').split('|').filter(Boolean), rec:el.getAttribute('data-rec')||'', host:")
overlay = rep(overlay, "items.push({ id:'page', kind:'Whole page', num:'', title:'Anything that belongs to the page rather than one section', host:",
              "items.push({ id:'page', kind:'Whole page', num:'', title:'Anything that belongs to the page rather than one section', opts:[], rec:'', host:")
overlay = rep(overlay, """'<span class="dd-chips">'+CHIPS.map(function(c){return '<button type="button" class="dd-chip'+(s.verdict===c?' on':'')+'" data-v="'+c+'">'+c+'</button>';}).join('')+'</span></div>'+""",
              """'<span class="dd-chips">'+it.opts.map(function(c){return '<button type="button" class="dd-chip'+(s.verdict===c?' on':'')+(c===it.rec?' rec':'')+'" data-v="'+esc(c)+'">'+esc(c)+(c===it.rec?'<em>recommended</em>':'')+'</button>';}).join('')+'</span></div>'+""")
overlay = rep(overlay, "Decision — in your words</span>", "Your words, if the buttons do not say it</span>")
# the export: every call, answered or not, with its recommendation
i_md = overlay.index("  function markdown(){"); j_md = overlay.index("  function download(){")
overlay = overlay[:i_md] + r"""  function markdown(){
    var lines = ['# DAVE-RULINGS — '+CFG.title, '', 'source: `'+CFG.path+'`  ', 'exported: '+now()+'  ', 'status: his words, verbatim — quote, never paraphrase', ''];
    var n=0, calls=0;
    items.forEach(function(it){ if(it.opts.length) calls++; if(has(state[it.id])) n++; });
    lines.push(n+' of '+items.length+' answered ('+calls+' calls and the whole-page note)', '');
    items.forEach(function(it){
      var s=state[it.id]||{};
      lines.push('## '+(it.num?it.num+' · ':'')+it.title+'  ');
      lines.push('<sub>'+it.kind+' · anchor `#dd-'+it.id+'`'+(s.at?' · saved '+s.at:'')+'</sub>', '');
      if(it.rec) lines.push('Recommendation: '+it.rec+'  ');
      if(s.verdict) lines.push('**Chose:** '+s.verdict+(it.rec?(s.verdict===it.rec?' · the recommendation':' · not the recommendation'):''), '');
      else lines.push('_Not answered by button._', '');
      if((s.decision||'').trim()) lines.push('**In his words, verbatim:**', '', '> '+s.decision.trim().replace(/\n/g,'\n> '), '');
      if((s.comment||'').trim()) lines.push('**Comment, verbatim:**', '', '> '+s.comment.trim().replace(/\n/g,'\n> '), '');
    });
    lines.push('', '---', '', '<details><summary>machine copy</summary>', '', '```json', JSON.stringify({page:CFG.page, path:CFG.path, exported:now(), calls:items.map(function(it){return {id:it.id, num:it.num, title:it.title, options:it.opts, recommendation:it.rec};}), answers:state}, null, 2), '```', '', '</details>', '');
    return lines.join('\n');
  }
""" + overlay[j_md:]
overlay = rep(overlay, "drop it in notes/_lanes/304/", "drop it in notes/_lanes/307/")
overlay = rep(overlay, ">Export rulings .md</button>", ">Save as file</button>")
overlay = rep(overlay, "'Autosaves as you type'", "'Saves in this browser as you go'") if "'Autosaves as you type'" in overlay else overlay.replace(">Autosaves as you type<", ">Saves in this browser as you go<")

page = head + "<body>" + backlink[len("<body>"):] + "\n" + head_top + s1 + s2 + s3 + s4 + s5 + s6 + tech + "\n" + overlay
DST.write_text(page)
print(DST, len(page), "calls:", page.count('class="dd-call"'), "imgs:", page.count("<img class="))
