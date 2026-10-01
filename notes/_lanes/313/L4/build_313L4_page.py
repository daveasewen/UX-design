"""#313 lane L4 — builds notes/_REVIEW-313-L4-seven-trees-redone-2026-10-01-v1.html, the re-look page for the
seven cohort-one trees Dave sent back on 2026-10-01 17:52 (his export:
notes/_lanes/313/DAVE-RULINGS-2026-10-01-1752-cohort-one-trees-complete.md), redone by
notes/_lanes/313/L4/redo_seven.py.

Shell, stylesheet and the save / Copy as text / Export / Clear script are lifted VERBATIM at build time from
notes/_lanes/312/L/build_312L_page.py (lane L3's page), so the export mechanism is identical; only the storage
key, the header line of the copied text and the download name change. Pictures are L3's
(notes/_lanes/312/L/img/), no new renders. The old tree (as Dave saw it) is read from git at BASE; the new
tree from the meta on disk.
Usage (repo root): python3 notes/_lanes/313/L4/build_313L4_page.py      (pure python; needs git for BASE)"""
import html, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUT = "notes/_REVIEW-313-L4-seven-trees-redone-2026-10-01-v1.html"
SHELL = "notes/_lanes/312/L/build_312L_page.py"
IMG = "_lanes/312/L/img"
BASE = "e5e0f355"
KEY = "review-313-L4-seven-trees-v1"
SEVEN = ["button", "table", "date-picker", "metric", "slider", "selection-controls", "modals"]
SNIP = {"button": "Button", "table": "Table", "date-picker": "Date-picker", "metric": "Metric", "slider": "Slider",
        "selection-controls": "Selection-controls", "modals": "Modals"}
WORD = {"button": "Button", "table": "Table", "date-picker": "Date picker", "metric": "Metric", "slider": "Slider",
        "selection-controls": "Switch (drafted as the selection-controls family)", "modals": "Dialog (drafted as the modals family)"}
YES = "Yes, it describes the part"
CHANGE = "Change it (comment)"
FOUR = "Four parts"
ONE = "Four trees in one part"

# What the page recommended and Dave took (verbatim from the 312 page; he left no comment of his own).
ASKED = {
    "button": "The tree is the Loading specimen, not the button. The right tree is the button with its type and its label field, and the spinner shown only while processing. … the states and bindings can stay.",
    "table": "Start the tree at the table, with the scrolling box as an optional wrapper rather than the part itself; take pressed out (it belongs to the demo switcher above the table, not the table); and make the caption and the cells holes for the title and rows the table already has as choices, not the demo's account names and balances. The caption, header row, body rows and number cells are right.",
    "date-picker": "Add the day part: a day cell in the grid, with today, selected, empty and disabled as its states.",
    "metric": "Name the two figures: the value and the change are what a tile is read for, and the draft calls them span and span-2 … Take busy out; it is loading said twice. The five declared states, the trend choice on the delta and the spark slot are right and stay.",
    "slider": "Name the thumb and the track as parts, with hover, active and disabled, even though the markup has no element for them.",
    "selection-controls": "Give the switch its own tree (switch, label, knob, thumb; states off, on, disabled, error), and the same for checkbox, radio and chip. … Whether that is four metas or four roots in one is the comment to leave.",
    "modals": "Take inert and disabled out of the dialog's states; they belong to the page. The parts are right.",
}

P = {
"button": dict(
  h2="The button is now the button: its type, its words, and a spinner only while it is processing.",
  changed="Was the Loading specimen, with the fixed word Loading and a spinner always drawn. Now the default button: its type is the choice on it, its words are its label field, and the spinner is present only while processing. States and bindings unchanged.",
  facts=[("The words", "The label field fills the button. Nothing in the tree is the demo's word any more."),
         ("The spinner", "Still the one child, now marked as shown only in the processing state. A button at rest has none."),
         ("Kept", "The seven states (rest, hover, pressed, disabled, processing, success, focus) and the 29 lines to tokens, as you said.")],
  rec=YES, why="It is the button you described: type, words, and the spinner only while processing."),
"table": dict(
  h2="The table now starts at the table, its words come from its title and rows, and pressed is gone.",
  changed="Was rooted at the scrolling box, carried the demo's account names and balances, and listed pressed and disabled. Now rooted at the table with the scrolling box as an optional wrapper; the caption and every cell take the title and rows fields; pressed is out, and disabled with it; the rows and cells have plain names.",
  facts=[("Disabled, one step past your words", "Disabled came from the same demo switcher as pressed (its greyed button), and from nothing else on the page. It is taken out for the same reason. If you want it kept, say so in the comment."),
         ("The wrapper", "The scrolling box is drawn above the tree as optional: it is the region a keyboard user tabs into to pan a wide table. Its name is now the table's title."),
         ("The words", "Caption: the title field. Header cells, body cells and the card labels when the table collapses: the rows field. The body row repeats once per row. The caption's second line (the demo's date) is taken out; no setting carries a second line yet."),
         ("The names", "head, header row, column header, number header, body, row, row header, cell, number cell, and a value inside each cell. The markup has no class on these, so the names were set by hand, as you ruled."),
         ("Listens", "Nothing now. The page's only click was the demo switcher's.")],
  rec=YES, why="All three changes are in, and the caption, header row, body rows and number cells are as they were."),
"date-picker": dict(
  h2="The grid now holds its day: a day cell with today, selected, empty and disabled as its own states.",
  changed="The grid was empty. Now it holds the day, with its four states on the day itself; today, selected and empty moved off the field's list; three numbered names made plain (weekday, calendar icon, arrow icon).",
  facts=[("Built when it opens", "The reference page builds the days with its script when the calendar opens, so there is no day in the static page. The tree marks the day as built, and checks it through the grid that holds it."),
         ("Its own states", "Today, selected, empty and disabled sit on the day, not on the field. A plain day carries none of them. Disabled stays on the field's list too, because the field has its own."),
         ("Still on the field", "The message's words (ok, info, warning, success) and the panel's (open, static) stay on the field's list until every piece carries its own states, the later step you ruled. The styles also draw hover and focus on a day; those stay on the field's list for now.")],
  rec=YES, why="The day is in the grid with exactly the four states you named."),
"metric": dict(
  h2="The two figures are named, value and change, and busy is gone.",
  changed="span became value and span-2 became change. Busy is out; the busy attribute now reads the loading state. The five declared states, the trend choice and the spark slot are untouched.",
  facts=[("Value", "The figure the tile is read for, with its unit beside it."),
         ("Change", "The change figure on the delta line; its direction is still the trend choice on the delta."),
         ("Rest", "Still ready, the metric's own word.")],
  rec=YES, why="Both figures are named and busy is folded into loading; nothing else moved."),
"slider": dict(
  h2="The slider names its track and thumb, each with hover, active and disabled.",
  changed="Was a field, a label, a readout and the range input. Now the track sits inside the input and the thumb on the track, each with its own states: rest, hover, active, disabled. The field keeps rest and focus.",
  facts=[("No element", "The browser draws both from the range input. The tree marks them so and checks them through the input. The element type written for them is a stand-in for a library that draws them as elements."),
         ("Active", "The meta's handle setting already calls this look pressed. The tree uses your word, active; the two are the same look."),
         ("Not drawn yet", "The reference page styles no hover, active or disabled on the thumb or track. These states come from your word, not from the page, so the picture cannot show them."),
         ("The range", "The double slider has two thumbs on one track.")],
  rec=YES, why="Both pieces are named with the three states you asked for, and marked as having no element."),
"selection-controls": dict(
  h2="The family is now four trees, one per control: switch, checkbox, radio and chip, each with its own states.",
  changed="One 29-part tree for four controls became four trees under the family. The switch: switch, input, label, knob, thumb, with off, on, disabled and error. The checkbox with its box and tick; the radio with its ring and dot inside its group; the chip with its star or its remove button.",
  facts=[("The switch's fifth part", "Inside the switch row sits a hidden native input that carries on and off and the name a screen reader hears. The four you named are the row (switch), the label, the knob and the thumb; the input is written beside them, not instead of one."),
         ("Knob and thumb", "Both carry the switch's four states themselves, so a library knows which piece changes."),
         ("Rest words", "Off for the switch and the chip, unchecked for the checkbox and the radio: each control's own word."),
         ("Words", "Every label takes the label field, as the button does. The demo's sentences are gone."),
         ("The error line", "Each control's message sits after its row and shows only in error. It is written beside the tree, not inside it, because the page places it outside the row."),
         ("The chip", "The page draws three kinds: a toggle (pressed on or off, with a star), a single choice in a group (arrow keys move it), and a removable chip with a remove button. The tree is the chip with its star and remove button, each marked for the kind that has it."),
         ("Not in the four", "The styles also draw hover and a focus ring on the switch. They are not in the four states you named and are left out.")],
  rec=YES, why="The switch has its own tree with exactly your four parts' names and four states, and checkbox, radio and chip have theirs."),
"modals": dict(
  h2="The dialog's states are its own: inert and disabled are gone.",
  changed="Inert and disabled are out, with the arrows to and from them. Title and body take the title and body fields; the two action buttons are named confirm and cancel, the markup's own words for them.",
  facts=[("Where they went", "Inert is what the open dialog does to the page behind it; disabled is what it does to the button that opened it. Both belong to the page, as you said."),
         ("States now", "Closed (rest, its own word), open, hover, focus, active."),
         ("Names", "h2 and p became title and body; btn and btn-2 became confirm and cancel. The action buttons' words are still the demo's; they are buttons with their own label field.")],
  rec=YES, why="Inert and disabled are out and the parts are as they were, with plain names."),
}


def esc(s):
    return html.escape(str(s), quote=True)


def hole(v):
    v = str(v)
    if v.startswith("{props.") and v.endswith("}"):
        return "prop", v[7:-1]
    if v.startswith("{state.") and v.endswith("}"):
        return "st", v[7:-1]
    return None, None


def outline(n, wrapper=True):
    """The 312 outline, plus: optional wrappers, words from a field, built/drawn parts, a piece's own states."""
    if wrapper and n.get("$wrapper"):
        w = n["$wrapper"]
        inner = outline(n, wrapper=False)
        tag = '<i class="h">optional wrapper</i>' if w.get("$optional") else '<i class="h">group</i>'
        return f'<li><span class="pn">{esc(w["part"])}</span> <span class="tg">{esc(w["tag"])}</span> {tag}<ul>{inner}</ul></li>'
    bits = []
    for k, v in list(n.get("attrs", {}).items()) + list(n.get("aria", {}).items()):
        kind, word = hole(v)
        if k == "role":
            bits.append(f'<i class="h role">role {esc(v)}</i>')
        elif kind == "prop" and k not in ("data-label", "aria-label"):
            bits.append(f'<i class="h prop">prop {esc(word)}</i>')
        elif kind == "st":
            bits.append(f'<i class="h st">state {esc(word)}</i>')
        elif "{props." in str(v):
            s = str(v); bits.append(f'<i class="h prop">prop {esc(s[s.index("{props.")+7:s.index("}", s.index("{props."))])}</i>')
    if n.get("slot"):
        bits.append(f'<i class="h slot">slot {esc(n["slot"])}</i>')
    if n.get("$repeat"):
        bits.append(f'<i class="h rep">×{esc(n["$repeat"])}</i>')
    if n.get("$each"):
        bits.append('<i class="h rep">one per row</i>' if "rows" in str(n["$each"]) else '<i class="h rep">one per day</i>')
    if n.get("$when"):
        w = str(n["$when"]); kind, word = hole(w)
        bits.append(f'<i class="h st">only while {esc(word)}</i>' if kind == "st" else f'<i class="h">{esc(w)}</i>')
    if n.get("$visual"):
        bits.append('<i class="h vis">' + ("built by the script" if "script" in n["$visual"] else "drawn by the browser, no element") + '</i>')
    if n.get("text"):
        kind, word = hole(n["text"])
        if kind == "prop":
            bits.append(f'<i class="h prop">words: {esc(word)} field</i>')
        else:
            t = str(n["text"]); t = t if len(t) <= 32 else t[:31] + "…"
            bits.append(f'<span class="tx">“{esc(t)}”</span>')
    s = f'<li><span class="pn">{esc(n["part"])}</span> <span class="tg">{esc(n["tag"])}</span> {" ".join(bits)}'
    if n.get("$states"):
        ini = n.get("$initial")
        s += '<div class="own">' + "".join(f'<span class="sc{" on" if x == ini else ""}">{esc(x)}{" · rest" if x == ini else ""}</span>' for x in n["$states"]) + "</div>"
    if n.get("$message"):
        s += f'<div class="beside">beside it: <b>{esc(n["$message"]["part"])}</b> {esc(n["$message"]["tag"])}, shown only in error</div>'
    if n.get("children"):
        s += "<ul>" + "".join(outline(c) for c in n["children"]) + "</ul>"
    return s + "</li>"


def chips(states, initial):
    return '<div class="sts">' + "".join(
        f'<span class="sc{" on" if x == initial else ""}">{esc(x)}{" · rest" if x == initial else ""}</span>' for x in states) + "</div>"


def call(id_, q, options, rec, prompt):
    chips_ = "".join(f'<button type="button" class="chip" data-v="{esc(o)}">{esc(o)}{"<em>recommended</em>" if o == rec else ""}</button>' for o in options)
    return f'''<div class="call" data-id="{esc(id_)}" data-q="{esc(q)}" data-rec="{esc(rec)}">
      <p class="q">{prompt}</p>
      <div class="chips">{chips_}</div>
      <label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>'''


def tech(i, new, old):
    ex = new["$extracted"]
    rows = "".join(f'<li>{esc(r["what"])} <span class="why">— {esc(r["why"])}</span></li>' for r in ex.get("$hand", []))
    return (f'<ol><li>Meta <code>knowledge/components/{esc(i)}.meta.json</code>, set by hand by '
            f'<code>notes/_lanes/313/L4/redo_seven.py</code> from the draft at <code>{BASE}</code>; <code>reviewed: false</code>; '
            f'the extractor now refuses to overwrite a hand-set draft without <code>--force</code>.</li>'
            f'<li>Root: <code>{esc(new["anatomy"].get("$sel", ""))}</code> ({esc(ex.get("$root", ""))}). Old root: <code>{esc(old["anatomy"].get("$sel", ""))}</code>.</li>'
            f'<li>Reference <code>knowledge/snippets/{SNIP[i]}.reference.html</code>; picture from <code>{IMG}/</code> (lane L3, seat render, not re-rendered).</li>'
            f'<li>Every change, with its reason:<ol>{rows}</ol></li></ol>')


def part_section(k, i, new, old):
    p = P[i]
    st, ost = new["states"], old["states"]
    grey = ' class="grey"' if k % 2 == 0 else ""
    pics = f'<figure><img src="{IMG}/{i}.png" srcset="{IMG}/{i}.png 2x" alt="{esc(WORD[i])} from its reference page, light theme"><figcaption>{esc(WORD[i].split(" (")[0])} · light · from its reference page</figcaption></figure>'
    if i == "selection-controls":
        pics = (f'<figure><img src="{IMG}/selection-controls-switch.png" srcset="{IMG}/selection-controls-switch.png 2x" alt="The four switch rows">'
                f'<figcaption>The switch rows · off, on, disabled, error</figcaption></figure>'
                f'<figure><img src="{IMG}/selection-controls.png" srcset="{IMG}/selection-controls.png 2x" alt="The whole selection-controls family">'
                f'<figcaption>The family · checkbox, radio, switch, chips</figcaption></figure>')
    facts = "".join(f'<li><span class="k">{esc(a)}</span><span>{esc(b)}</span></li>' for a, b in p["facts"])
    rec_word = "Yes" if p["rec"] == YES else "Change it"
    q = f"{k}. {WORD[i]}: does the redone tree describe the part?"
    return f'''
<section id="p-{i}"{grey}>
  <div class="wrap">
    <p class="label">{k:02d} · {esc(WORD[i])} · redone</p>
    <h2>{esc(p["h2"])}</h2>
    <p class="quote">What you took: “{esc(ASKED[i])}”</p>
    <p class="changed"><span class="k">What changed</span> {esc(p["changed"])}</p>
    <div class="part">
      <div class="pic">{pics}<p class="links"><a href="../showroom/{i}.html">Showroom page</a> · <a href="../knowledge/snippets/{SNIP[i]}.reference.html">Reference page</a></p></div>
      <div class="tree">
        <h4>Anatomy, redone <small>the parts, nested as they sit</small></h4>
        <ul class="outline">{outline(new["anatomy"])}</ul>
        <h4>States <small>{len(st["states"])}, rest state marked{"; a piece's own states sit under it in the tree" if any(x in json.dumps(new["anatomy"]) for x in ('"$states"',)) else ""}</small></h4>
        {chips(st["states"], st["initial"])}
        <details class="old"><summary>The tree you sent back</summary>
          <ul class="outline">{outline(old["anatomy"])}</ul>
          {chips(ost["states"], ost["initial"])}
        </details>
      </div>
    </div>
    <ul class="facts">{facts}</ul>
    {call(i, q, [YES, CHANGE], p["rec"], f'Does the redone tree describe the part? <span class="rw">Recommendation: {rec_word}.</span> {esc(p["why"])}')}
    <details class="tech"><summary>Technical</summary>{tech(i, new, old)}</details>
  </div>
</section>'''


def shell_parts():
    """The 312 page's <style> and <script>, verbatim, un-doubled from its f-string source."""
    s = open(os.path.join(ROOT, SHELL), encoding="utf-8").read()
    style = s[s.index("<style>"): s.index("</style>") + len("</style>")]
    script = s[s.index("<script>\n(function(){{"): s.index("</script>\n</body></html>") + len("</script>")]
    pairs = [("'review-312-L-cohort-one-trees-v1'", "'%s'" % KEY),
             ("'{OUT}'", "'%s'" % OUT),
             ("Session 312 · Cohort one: fifteen trees · decisions", "Session 313 · Seven trees redone · decisions"),
             ("'{len(IDS)+4}. Note on the page: '", "'%d. Note on the page: '" % (len(SEVEN) + 3)),
             ("review-312-L-cohort-one-trees.txt", "review-313-L4-seven-trees-redone.txt")]
    for a, b in pairs:
        assert a in script, a
        script = script.replace(a, b)
    style, script = (x.replace("{{", "{").replace("}}", "}") for x in (style, script))
    script = script.replace("\\\\n", "\\n")   # the f-string source's '\\n' is JS '\n' once evaluated
    extra = (".changed{font-size:17px;line-height:1.55;max-width:46em;margin:0 0 var(--s2);color:var(--g8)}"
             ".changed .k,.beside{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);margin-right:.5em}"
             ".beside{display:block;margin:.15rem 0 0 0;letter-spacing:.04em;text-transform:none;font-size:12px}"
             ".own{display:flex;flex-wrap:wrap;gap:.25rem;margin:.2rem 0 .1rem}.own .sc{font-size:11px;padding:.1rem .4rem}"
             ".h.vis{border-style:dashed}"
             "details.old{margin-top:var(--s2);font-size:13px;color:var(--g7)}details.old summary{cursor:pointer;font-size:12px;color:var(--g6);padding:.3rem 0}"
             "details.old .outline li{font-size:13px;color:var(--g7)}"
             ".why{color:var(--g6)}"
             ".split{margin:var(--s3) 0 0;padding:0;list-style:none}")
    style = style.replace("</style>", extra + "\n</style>")
    return style, script


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    os.chdir(ROOT)
    new = {i: json.load(open(f"knowledge/components/{i}.meta.json", encoding="utf-8")) for i in SEVEN}
    old = {i: json.loads(subprocess.check_output(["git", "show", f"{BASE}:knowledge/components/{i}.meta.json"])) for i in SEVEN}
    style, script = shell_parts()
    parts = "".join(part_section(k, i, new[i], old[i]) for k, i in enumerate(SEVEN, start=2))
    nq = len(SEVEN) + 2
    total_calls = len(SEVEN) + 2
    toc = "".join(f'<a href="#p-{i}">{esc(WORD[i].split(" (")[0])}</a>' for i in SEVEN)
    yes = sum(1 for i in SEVEN if P[i]["rec"] == YES)
    sc = new["selection-controls"]
    split = sc["anatomy"].get("$split", "")
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seven trees redone</title>
{style}
</head>
<body>
<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;background:#000;color:#fff;font:500 13px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>

<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#ruled">What you ruled</a>
  {toc}
  <a href="#four">Four parts or one</a>
  <a href="#else">Anything else</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 313 · re-look · Seven trees redone</p>
      <h1>The seven trees you sent back tonight, redone the way the page recommended, for one more look.</h1>
      <p class="sub">You took Change it on seven, each on the page's own recommendation and with no comment of your own, so each recommendation was the instruction. Every draft is still marked reviewed: false; nothing stands until you say.</p>
    </div>
    <div class="meta">
      <span>Thursday 1 October 2026</span>
      <span>{total_calls} calls: one per redone part, the switch question you left open, and a note.</span>
      <span>Yes means the redone tree stands as the part's spec. Change it means say how in the comment.</span>
      <span>Pictures are the ones from last night's page; nothing was re-rendered.</span>
    </div>
  </div>
</header>

<section id="ruled">
  <div class="wrap">
    <p class="label">01 · What you ruled, and how it was applied</p>
    <h2>Seven trees changed on the page's words, and two of your three rules on words applied to all seven.</h2>
    <ul class="facts">
      <li><span class="k">Plain words</span><span><b>Applied.</b> Where the markup gives a piece no name, the tree now uses a plain word set by hand: the table's row and cell, the dialog's title and body, the metric's value and change, the switch's knob. Where the markup has its own word (btn, spin, dp-box) it stays.</span></li>
      <li><span class="k">Rest state</span><span><b>Applied.</b> Each part rests in its own word: the button and table in default, the metric in ready, the dialog in closed, the switch and chip in off, the checkbox and radio in unchecked.</span></li>
      <li><span class="k">States per piece</span><span><b>Started where you named the piece.</b> The slider's track and thumb, the date picker's day, and the switch's knob and thumb now carry their own states. Every other piece waits for the later step you ruled; each tree says which.</span></li>
      <li><span class="k">Parts with no element</span><span>The thumb, the track and the day have no element in the reference page (the browser draws the first two, the script builds the third). The tree marks them so, and the coverage check finds them through the element that draws or holds them. Everything else in every tree still points at a real element; every line to a token still resolves.</span></li>
      <li><span class="k">Left as it was</span><span>The eight parts you said yes to are untouched. Nothing is inscribed and no reference page was edited.</span></li>
    </ul>
    <p class="record">Recommendation on the seven: Yes on {yes}, Change it on {len(SEVEN) - yes}. One thing goes past your words and is said where it happens: the table's disabled state is taken out with pressed, because it came from the same demo switcher.</p>
  </div>
</section>
{parts}

<section id="four" class="grey">
  <div class="wrap">
    <p class="label">{nq:02d} · The switch and its family · four parts, or four trees in one part?</p>
    <h2>You left this one open. The four trees are drawn so that either answer works without redrawing them.</h2>
    <p class="lead">Today they sit as four trees inside the one selection-controls part. Four parts would make the switch, the checkbox, the radio and the chip each a part of its own, looked up by its own name.</p>
    <ul class="facts">
      <li><span class="k">What a split moves</span><span>Each tree becomes its part's tree; the states on its root become that part's states; its lines to tokens come from the list already written of which control reads which colour; the label field and the kind setting go with each. The family part keeps only what is shared, or becomes a pointer to the four.</span></li>
      <li><span class="k">What stays the same</span><span>The four trees as drawn above, their names and their states. Names are unique within each tree, so nothing is renamed by a split.</span></li>
      <li><span class="k">What it costs</span><span>Four new parts in the library instead of one, each needing its own showroom page in time.</span></li>
    </ul>
    {call("four", f"{nq}. Switch, checkbox, radio and chip: four parts, or four trees in one part?", [FOUR, ONE], FOUR, 'Four parts, or four trees in one part? <span class="rw">Recommendation: four parts.</span> A client library looks each one up by its own name: it asks for a switch, not for the second tree inside selection controls.')}
    <details class="tech"><summary>Technical</summary><ol><li>On disk the four trees are the children of the family root in <code>knowledge/components/selection-controls.meta.json</code>; each member carries <code>$states</code>, <code>$initial</code>, <code>$transitions</code> on its root; the family's top-level <code>states</code> is the union; <code>bindings.$by-member</code> lists which control reads each variable. The split note on disk: {esc(split)}</li><li>No meta was created; a four-meta split would add four and re-base the meta count check in the same change.</li></ol></details>
  </div>
</section>

<section id="else">
  <div class="wrap">
    <p class="label">{nq + 1:02d} · Anything else</p>
    <h2>Anything you want changed or looked at again.</h2>
    <div class="call" data-id="page" data-q="{nq + 1}. Note on the page" data-rec="">
      <p class="q">Anything else on this page?</p>
      <label class="field"><span>Your note</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · re-look page · Seven trees redone · v1 · 2026-10-01 · session 313 lane L4</span>
  <span>No draft stands until you say.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of {total_calls} answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

{script}
</body></html>
'''
    open(OUT, "w", encoding="utf-8").write(page)
    print(OUT, len(page), "bytes;", total_calls, "calls; Yes", yes, "Change", len(SEVEN) - yes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
