"""#312 lane L3 — builds notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html from the fifteen drafted metas
(knowledge/components/<id>.meta.json: anatomy, states, emits, bindings, $extracted) and the prose below.
Shell: the house review page (notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html), new localStorage key.
Pictures: notes/_lanes/312/L/img/<id>.png from render_312L.py shots (2x, light theme).
Usage: python3 notes/_lanes/312/L/build_312L_page.py   (from the repo root; pure python)"""
import json, html, os

OUT = "notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html"
IMG = "_lanes/312/L/img"
IDS = "button tabs table date-picker metric split-button accordion slider selection-controls input-fields dropdown modals tooltip pagination notifications".split()
SNIP = {"button": "Button", "tabs": "Tabs", "table": "Table", "date-picker": "Date-picker", "metric": "Metric",
        "split-button": "Split-button", "accordion": "Accordion", "slider": "Slider",
        "selection-controls": "Selection-controls", "input-fields": "Input-fields", "dropdown": "Dropdown",
        "modals": "Modals", "tooltip": "Tooltip", "pagination": "Pagination", "notifications": "Notifications"}
# Dave's word → meta, from notes/_lanes/312/L/COHORT-ONE.md
WORD = {"button": "Button", "tabs": "Tabs", "table": "Table", "date-picker": "Date picker", "metric": "Metric",
        "split-button": "Menus (drafted as the split button)", "accordion": "Accordion", "slider": "Slider",
        "selection-controls": "Switch (drafted as the selection-controls family)", "input-fields": "Text input (drafted as the input-fields family)",
        "dropdown": "Select (drafted as the dropdown)", "modals": "Dialog (drafted as the modals family)", "tooltip": "Tooltip",
        "pagination": "Pagination", "notifications": "Notification"}
# Pasted from notes/_subreports/2026-10-01-312-L2-extract.md (the --report run)
COVERAGE = dict(cohort=15, full=15, library=139, refused=0, undrafted=119, fenced=4, exempt=1, bindings=215)

YES = "Yes, it describes the part"
CHANGE = "Change it (comment)"

# Per part: the designer's reading of the draft. h2 = one sentence; lead = what the picture and tree show;
# facts = what to know (plain); fires = the proposed events; rec = YES or CHANGE; why = the recommendation in words.
P = {
"button": dict(
  h2="The draft is wrong: the extractor took the Loading button as the button.",
  lead="The reference page shows the primary button in five looks (default, pressed, disabled, loading, done). The picture is the default one. The extractor picked the richest of the primary buttons on the page, and the richest is the Loading specimen, so the drafted tree is a button whose words are literally \u201cLoading\u201d and whose only inner part is the spinner. That describes one state of a button, not a button.",
  facts=[("What is wrong","The words are the fixed text Loading where the button's own label belongs, and the spinner is drawn as if every button has one. A client library reading this tree would build a Loading button."),
         ("The right tree","One part, the button, with its type (primary, secondary, tertiary, quaternary) as a choice on it and its words as its label field, as you ruled at session 305 (a part's own words are a field on the part, not a part inside it). The spinner is a child that appears only while processing. If icon-and-label buttons belong in the spec, an icon slot beside the label."),
         ("What is right","The seven states (rest, hover, pressed, disabled, processing, success, focus) and the colour bindings were read from all six specimens and the styles, not only the Loading one, and they stand."),
         ("Not here","The icon button is its own part and is not in this cohort.")],
  fires=[("press","when the button is activated by pointer or keyboard; carries its type")],
  rec=CHANGE, why="The tree is the Loading specimen, not the button. The right tree is the button with its type and its label field, and the spinner shown only while processing. Leave that in the comment (or your own words) and the draft is redone in phase 2; the states and bindings can stay."),
"tabs": dict(
  h2="Tabs are a strip of tab buttons with a sliding indicator and a More menu, over a set of panels.",
  lead="The tree reads the strip (tablist) with its tabs, the overflow trigger and its menu, and the indicator line, then the panels, one per tab, with their text. Six tabs and six panels collapse to one of each, marked ×6.",
  facts=[("The More menu","Its items are built by the page's script when tabs overflow, so the menu in the tree has no children. The items will need to be named when the fixture is generated."),
         ("The colour sets","The meta's list of looks (unselected-hover, selected-first and so on) is a colour-set list, not taken as states. The nine states here are the machine ones: rest, hover, focus, active, selected, expanded, open, disabled, hidden."),
         ("Keys","Left and Right move between tabs, Home and End jump to the ends, Escape closes the More menu.")],
  fires=[("tab-change","when a different tab is chosen; carries the tab's index and id")],
  rec=YES, why="The strip, the indicator, the overflow and the panels are all there and named by their own class words."),
"table": dict(
  h2="The draft has the table's pieces, but it starts at the scrolling box around the table and keeps the demo's words.",
  lead="The tree starts at the scroll region (so keyboard users can scroll it), then the table, its caption and sub-line, the header row with its cells, and the body rows with a row-header cell, three cells and a number cell, each holding a value span.",
  facts=[("The names","The rows and cells have no class names in the markup, so the draft calls them tr, tr-2, td, v-2. The call on words, below, decides whether those become row, cell, header-cell, value."),
         ("The states","The meta says a table is not interactive, yet the draft lists hover, focus and pressed. Hover is the row highlight and focus is the scroll region, both real. Pressed was read from the demo's header-type switcher above the table, which is not part of it."),
         ("Listens","The only click on the page is that demo switcher, so the table itself listens to nothing."),
         ("The root and the words","The root is the scrolling box (a region you can tab into on a narrow screen), not the table; the extractor climbed one level up from the table. Every cell carries the demo's words (Current account, the balances, the caption's date) where the spec wants holes for the title and the rows.")],
  fires=[("sort","if column sorting is wanted; carries the column and direction. Today the reference table does not sort, so the honest draft is: fires nothing")],
  rec=CHANGE, why="Three things, none of them covered by the calls below: start the tree at the table, with the scrolling box as an optional wrapper rather than the part itself; take pressed out (it belongs to the demo switcher above the table, not the table); and make the caption and the cells holes for the title and rows the table already has as choices, not the demo's account names and balances. The caption, header row, body rows and number cells are right."),
"date-picker": dict(
  h2="A date picker is a labelled field with a calendar button, a message line, and a panel with month arrows, a title, the weekday row and the day grid.",
  lead="The picture has the panel open. The tree reads the label row, the help line, the box (input and calendar button), the message, then the panel: its head (four arrows, the month title), the weekday row and the grid.",
  facts=[("No day part","The day cells are drawn by the page's script, so the grid in the tree is empty and there is no day part, although today, selected and empty are in the state list because the styles name them."),
         ("Eighteen states","The list mixes the field's states (rest, hover, focus, disabled, invalid, error, completed) with the message's words (ok, info, warning), the panel's (expanded, open, static) and a day's (today, selected, empty). Each says where it was read from."),
         ("Keys","The full set: arrows move a day, PageUp and PageDown a month, Home and End to the ends of the week, Enter and Space choose, Escape closes.")],
  fires=[("change","when a date is chosen or typed; carries the value"),("open","when the panel opens"),("close","when the panel closes")],
  rec=CHANGE, why="Add the day part: a day cell in the grid, with today, selected, empty and disabled as its states. A designer sees the days first; the tree should too. Say so in the comment, or write your own list."),
"metric": dict(
  h2="A metric is a label, a value with its unit, a delta line (arrow, figure, period), and a spark chart in its own slot.",
  lead="The tree reads the label, the value with its unit span and figure span, the delta with its glyph (an icon), figure and period, and the spark container holding the inline chart. The delta's direction (up, down) is a prop hole on its class.",
  facts=[("Ready first","The five states the meta already declares (ready, loading, empty, error, stale) come first and ready is the rest state. Hover, focus and busy were added from the styles and the aria-busy attribute; busy says the same as loading."),
         ("Two unnamed spans","The value figure and the delta figure are spans with no class, so they are called span and span-2. These are the two parts that matter most on a tile, so they are worth naming here and not left to the general rule on words below."),
         ("No script","The metric page has no script, so it listens to nothing; the transitions are only the ones the styles imply.")],
  fires=[("nothing","a metric displays; it does not act. If a retry on error is ever wanted, that would be a retry event")],
  rec=CHANGE, why="Name the two figures: the value and the change are what a tile is read for, and the draft calls them span and span-2, the two least telling names in the tree. Take busy out; it is loading said twice. The five declared states, the trend choice on the delta and the spark slot are right and stay."),
"split-button": dict(
  h2="A split button is a main button and a caret button side by side, with a menu of items (and a separator) that opens under the caret.",
  lead="The picture has the menu open. The tree reads the main button, the caret button with its icon, and the menu with three items and a separator. Its tier (primary, secondary) is a prop hole on the class, and the menu's open state is a hole on its data attribute.",
  facts=[("This is your menus","Of the fifteen, this is the only part that carries a true menu (a list of actions, role menu). The dropdown is a select: one value chosen from a list. The mapping call above is where that is decided."),
         ("Expanded and open","Both are listed: expanded is the caret's attribute, open is the menu's. They are one fact read from two places."),
         ("Not yet ruled","The split button meta is proposed at session 209 and has not been ruled. Drafting its tree does not change that.")],
  fires=[("press","when the main button is activated"),("select","when a menu item is chosen; carries the item"),("open","when the menu opens"),("close","when it closes")],
  rec=YES, why="Main, caret, menu, items: a designer would name the same five. The expanded/open doubling is a cleanup for the rule on words, not a reason to redraw."),
"accordion": dict(
  h2="An accordion is a list of items, each a head button with its words and a chevron, over a panel with the content inside.",
  lead="The picture has the first item open. The tree reads the accordion, an item (two collapse to one), its head with the words span and the chevron with its icon, and the panel with its inner wrapper.",
  facts=[("The words","The head's text is an unnamed span. The words call below covers it."),
         ("Expanded","The head's expanded attribute is the one real state beyond rest, hover, pressed and focus. The meta also has an open state; the draft kept the meta's own rest word, default.")],
  fires=[("toggle","when an item opens or closes; carries the item and whether it is now expanded")],
  rec=YES, why="Item, head, chevron, panel: the tree is the part."),
"slider": dict(
  h2="The draft sees a field with a label, a value readout and the range input, and nothing else.",
  lead="The picture shows a track and a thumb; the tree does not. The browser draws those two from the range input, so the extractor, which reads elements, cannot see them. The draft has four parts and two states (rest, focus).",
  facts=[("What is missing","Thumb and track, and their states: the thumb's hover and active (dragging) live on browser pseudo-elements and were not read; disabled is not in the list either."),
         ("Listens","The page's script listens to input and writes the value into the readout.")],
  fires=[("input","while the thumb is being dragged; carries the value"),("change","when the thumb is released; carries the value")],
  rec=CHANGE, why="Name the thumb and the track as parts, with hover, active and disabled, even though the markup has no element for them. A client library will have elements for both; the tree should describe what you see, not what the browser hides."),
"selection-controls": dict(
  h2="The draft is the whole family in one tree: checkbox rows, a radio group, the switch rows, and three kinds of chip.",
  lead="Your word was switch. Switch has no meta of its own; it is one branch of the selection-controls family, so the picture shows the switch rows first and the whole family below. In the tree the switch is field-3: the switch input with its label, and inside the label the knob (span-2) holding the thumb.",
  facts=[("Twenty-nine parts","Six checkbox rows, a fieldset of four radio rows, four switch rows, and three chip groups, each collapsed to one with its count. Every control shares one state list: checked, indeterminate, invalid, pressed, selected and the usual rest, hover, focus, disabled, error."),
         ("The names","field, field-2, field-3, input-2, label-3, span-2: the markup reuses the same class on every row, so the draft numbers them. Only the switch input and the chip-del wrapper are named by role or class."),
         ("Keys","Arrows move within the radio and chip groups; Home and End to the ends.")],
  fires=[("change","when a control is checked, unchecked or chosen; carries the control's value and whether it is checked")],
  rec=CHANGE, why="Give the switch its own tree (switch, label, knob, thumb; states off, on, disabled, error), and the same for checkbox, radio and chip. One tree for four controls will not describe any of them to a client library. Whether that is four metas or four roots in one is the comment to leave."),
"input-fields": dict(
  h2="A text input is a label row (label and a help button with its tooltip), help text, the box (prefix, input, tail button) and a count line.",
  lead="Your word was text input. The input-fields family is the nearest meta: single-line, large and multi-line inputs in one. The tree reads the first one on the page, an amount field with a prefix (GBP) and a tail button.",
  facts=[("Twelve states","Rest, hover, active, focus, completed, disabled, error and invalid are the box's. Ok, info, warning and success are the message line's words; they sit in the same list because the draft has one list per part. The call on per-part states, below, covers that."),
         ("Hover and active","Both were lent by the gallery's s-hover and s-active classes on a twin box, so a reader can see them drawn."),
         ("Keys and listens","Tab moves on. The script listens to input, keydown, mousedown and touchstart (for the count and the clear button).")],
  fires=[("input","on every keystroke; carries the value"),("change","when the field is left; carries the value")],
  rec=YES, why="Label row, help, box, count: the tree is the field. The mixed state list is a schema question asked once below, not a reason to send this back."),
"dropdown": dict(
  h2="A dropdown is a label, a trigger button showing the chosen value with a chevron, and a list of options with a tick on the chosen one and a separator.",
  lead="Your word was select. The dropdown meta holds the custom listbox and the native select in one; the tree is the custom one, with its list open in the picture. Five options collapse to one, marked ×5.",
  facts=[("Found by elimination","Nothing in the markup shares a word with dropdown, so the root is the first candidate that is not page chrome. It is the right element, but the method is worth knowing."),
         ("Eleven states","Rest, hover, active, focus, disabled, error, completed and active-message come from the meta's own state prop; selected is the option's; expanded and open are the trigger's attribute and the list's style, one fact twice."),
         ("Not drafted","The boxed and grouped variant on the same page is a different look and was not drafted; the native select is not in the tree.")],
  fires=[("change","when an option is chosen; carries the value"),("open","when the list opens"),("close","when it closes")],
  rec=YES, why="Trigger, value, chevron, list, option, tick: it describes the part. The native select can join in phase 2."),
"modals": dict(
  h2="A dialog is a scrim with the dialog box on it: a close button, a title, the body text, and an actions row with two buttons.",
  lead="Your word was dialog. The modals family's first member is the dialog, so the tree starts at the scrim (overlay) and the dialog inside it, whose kind (dialog, sheet) is a prop hole on its class. The picture is the dialog open on its scrim.",
  facts=[("The names","Title and body are h2 and p in the draft, the tags, because the markup gives them no class. The words call below covers them."),
         ("Inert and disabled","The draft lists them as states of the dialog. They are what the dialog does to the page behind it (made inert) and to its own open button (disabled) while it is open. They are not looks of the dialog."),
         ("Keys","Escape closes; Tab is trapped inside the dialog while it is open.")],
  fires=[("open","when the dialog opens"),("close","when it closes; carries the reason: confirm, cancel, dismiss, escape")],
  rec=CHANGE, why="Take inert and disabled out of the dialog's states; they belong to the page. The parts are right."),
"tooltip": dict(
  h2="A tooltip is a trigger (the help button with its icon) and the tip bubble that shows beside it.",
  lead="The picture has the tip shown. The tree is small: the wrapper, the trigger with its icon, and the tip. The words the trigger sits beside (Available balance) are context on the page, not part of the tooltip.",
  facts=[("Show","The tip's show state is the script's class; focus is the trigger's. Those two and rest are the whole machine."),
         ("Listens","mouseenter, mouseleave, focus, blur and Escape, all on the trigger.")],
  fires=[("nothing","a tooltip is a hint. If shows are ever counted, that would be show and hide events, but they are not needed to describe the part")],
  rec=YES, why="Trigger, icon, tip: there is nothing else to a tooltip."),
"pagination": dict(
  h2="Pagination is a nav holding a list: a previous and a next control with icons, page links with the current one marked, and an ellipsis.",
  lead="The tree reads the nav, its list, a control item (two collapse to one: previous and next) with its button and icon, a page item (five collapse to one) with its link, and the ellipsis item with its span. The current page is a hole on the link's aria-current.",
  facts=[("The names","li, li-2, li-3, a and ul are the tags because the items have no class. The words call below covers them."),
         ("Completed","It is in the state list because the meta's own state prop names it, not because the page draws it."),
         ("Keys","Left and Right for previous and next, Home and End for the first and last page, Space to activate.")],
  fires=[("page-change","when a page is chosen or previous/next pressed; carries the page number")],
  rec=YES, why="Controls, pages, current, ellipsis: it describes the part once the words are plain."),
"notifications": dict(
  h2="A notification is a bar with a status icon, the message (a bold title, the text, a link) and a dismiss button.",
  lead="The tree reads the bar (role alert), the icon wrapper with its icon, the main span with the bold title, text spans (three collapse to one) and a link, and the dismiss button with its icon. The picture is the error one, the richest of the two on the page.",
  facts=[("The kind","tint and err are literal classes on the root in the draft, because the meta's variants do not name them as a prop. The kind (error, warning, info, success) wants to be a prop hole, like the button's type."),
         ("Ten states","Rest, hover, focus and active are the dismiss button's and the link's; error, warning, info, ok and success are the bar's kind written as states; removing is the exit animation the script adds."),
         ("Listens","click on dismiss and transitionend for the exit.")],
  fires=[("dismiss","when the bar is closed by its button")],
  rec=YES, why="Icon, message, title, link, dismiss: the parts are right. Making the kind a prop instead of five states is a cleanup for the rule on words."),
}

def esc(s): return html.escape(str(s), quote=True)

def nodes(n):
    c = 1 + sum(nodes(k) for k in n.get("children", []))
    return c
def collapsed(n):
    c = max(0, int(n.get("$repeat", 1)) - 1)
    return c + sum(collapsed(k) for k in n.get("children", []))

def outline(n):
    bits = []
    attrs = n.get("attrs", {}); aria = n.get("aria", {})
    for k, v in list(attrs.items()) + list(aria.items()):
        v = str(v)
        if k == "role":
            bits.append(f'<i class="h role">role {esc(v)}</i>')
        elif "{props." in v:
            bits.append(f'<i class="h prop">prop {esc(v[v.index("{props.")+7:v.index("}", v.index("{props."))])}</i>')
        elif "{state." in v:
            bits.append(f'<i class="h st">state {esc(v[v.index("{state.")+7:v.index("}", v.index("{state."))])}</i>')
    if n.get("slot"): bits.append(f'<i class="h slot">slot {esc(n["slot"])}</i>')
    if n.get("$repeat"): bits.append(f'<i class="h rep">×{esc(n["$repeat"])}</i>')
    if n.get("text"):
        t = str(n["text"]); t = t if len(t) <= 32 else t[:31] + "\u2026"
        bits.append(f'<span class="tx">\u201c{esc(t)}\u201d</span>')
    s = f'<li><span class="pn">{esc(n["part"])}</span> <span class="tg">{esc(n["tag"])}</span> {" ".join(bits)}'
    if n.get("children"):
        s += "<ul>" + "".join(outline(c) for c in n["children"]) + "</ul>"
    return s + "</li>"

def chips(states, initial):
    out = []
    for s in states:
        cls = "sc on" if s == initial else "sc"
        out.append(f'<span class="{cls}">{esc(s)}{" · rest" if s == initial else ""}</span>')
    return '<div class="sts">' + "".join(out) + "</div>"

def bindings_html(b):
    items = [f'<li><code>{esc(k)}</code> <span class="arr">→</span> {esc(v.strip("{}").replace(".", " / "))}</li>' for k, v in b.items()]
    head = "".join(items[:6]); rest = "".join(items[6:])
    s = f'<ul class="binds">{head}</ul>'
    if rest:
        s += f'<details class="more"><summary>and {len(items)-6} more</summary><ul class="binds">{rest}</ul></details>'
    return s

def keys_line(keys):
    if not keys: return ""
    return '<p class="keys"><span class="k">Keys</span> ' + " · ".join(f'<b>{esc(k)}</b> {esc(v)}' for k, v in keys.items()) + "</p>"

def tech(i, m):
    ex = m["$extracted"]; st = m["states"]; src = st.get("$sources", {})
    tr = st.get("transitions", [])
    lines = []
    lines.append(f'Root: <code>{esc(m["anatomy"]["$sel"])}</code>, found by {esc(ex.get("$root", "?"))}. Parts {nodes(m["anatomy"])} after collapsing {collapsed(m["anatomy"])} repeated siblings. Source {esc(ex.get("source",""))}; drafted by {esc(ex["by"])} on {esc(ex["date"])}; <code>reviewed: {str(ex["reviewed"]).lower()}</code>.')
    srcs = "; ".join(f'<b>{esc(k)}</b> ← {esc(v[0]) if isinstance(v, list) and v else esc(v)}' + (f' (+{len(v)-1})' if isinstance(v, list) and len(v) > 1 else "") for k, v in src.items() if not k.startswith("$"))
    lines.append(f'States, first source each: {srcs or "none"}. Rest state: {esc(src.get("$initial", ""))}.')
    lines.append('Transitions: ' + ("; ".join(f'{esc(t["from"])} →<i>{esc(t["on"])}</i>→ {esc(t["to"])}' for t in tr) if tr else "none") + '.')
    if st.get("keys"):
        lines.append('Keys: ' + ", ".join(f'{esc(k)} = {esc(v)}' for k, v in st["keys"].items()) + f'. {esc(st.get("$keys-source", ""))}')
    lines.append(f'Listens (DOM events the page script attaches): {", ".join(ex.get("$listeners") or []) or "none"}. <code>emits: []</code> on disk: {esc(ex.get("$emits-note",""))}')
    lines.append(f'Bindings: {len(m["bindings"])}, every one resolved against knowledge/tokens/ by the extractor\'s coverage gate (light, then dark or modeless).')
    lines.append(f'Showroom <code>showroom/{i}.html</code>; reference <code>knowledge/snippets/{SNIP[i]}.reference.html</code>; picture cut at the root selector by <code>notes/_lanes/312/L/render_312L.py shots</code>.')
    return "<ol>" + "".join(f"<li>{l}</li>" for l in lines) + "</ol>"

def call(id_, q, options, rec, prompt):
    chips_ = "".join(f'<button type="button" class="chip" data-v="{esc(o)}">{esc(o)}{"<em>recommended</em>" if o == rec else ""}</button>' for o in options)
    return f'''<div class="call" data-id="{esc(id_)}" data-q="{esc(q)}" data-rec="{esc(rec)}">
      <p class="q">{prompt}</p>
      <div class="chips">{chips_}</div>
      <label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>'''

def part_section(k, i, m):
    p = P[i]; st = m["states"]; ex = m["$extracted"]
    grey = ' class="grey"' if k % 2 == 0 else ""
    pics = f'<figure><img src="{IMG}/{i}.png" srcset="{IMG}/{i}.png 2x" alt="{esc(WORD[i])} from its reference page, light theme"><figcaption>{esc(WORD[i].split(" (")[0])} · light · cut at the draft\'s root</figcaption></figure>'
    if i == "button":
        pics = pics.replace("light · cut at the draft's root", "light · the default button; the draft was read from the Loading one beside it")
    if i == "selection-controls":
        pics = f'<figure><img src="{IMG}/selection-controls-switch.png" srcset="{IMG}/selection-controls-switch.png 2x" alt="The four switch rows"><figcaption>The switch rows · your word</figcaption></figure>' + pics.replace("cut at the draft's root", "the whole family, the draft's root")
    listens = ", ".join(ex.get("$listeners") or []) or "nothing"
    fires = "".join(f'<li><b>{esc(n)}</b> {esc(d)}</li>' for n, d in p["fires"])
    facts = "".join(f'<li><span class="k">{esc(a)}</span><span>{esc(b)}</span></li>' for a, b in p["facts"])
    rec_word = "Yes" if p["rec"] == YES else "Change it"
    return f'''
<section id="p-{i}"{grey}>
  <div class="wrap">
    <p class="label">{k:02d} · {esc(WORD[i])} · does this tree describe the part?</p>
    <h2>{esc(p["h2"])}</h2>
    <p class="lead">{esc(p["lead"])}</p>
    <div class="part">
      <div class="pic">{pics}<p class="links"><a href="../showroom/{i}.html">Showroom page</a> · <a href="../knowledge/snippets/{SNIP[i]}.reference.html">Reference page</a></p></div>
      <div class="tree">
        <h4>Anatomy <small>the parts, nested as they sit</small></h4>
        <ul class="outline">{outline(m["anatomy"])}</ul>
        <h4>States <small>{len(st["states"])}, rest state marked</small></h4>
        {chips(st["states"], st["initial"])}
        {keys_line(st.get("keys"))}
        <h4>Events</h4>
        <p class="ev"><span class="k">Listens</span> {esc(listens)}</p>
        <p class="ev"><span class="k">Fires</span> <b>nothing yet</b> — the reference page sends no message out. Proposed:</p>
        <ul class="fires">{fires}</ul>
        <h4>Bindings <small>{len(m["bindings"])} lines to tokens</small></h4>
        {bindings_html(m["bindings"])}
      </div>
    </div>
    <ul class="facts">{facts}</ul>
    {call(i, f"{k}. {WORD[i]}: does this tree describe the part?", [YES, CHANGE], p["rec"], f'Does this tree describe the part? <span class="rw">Recommendation: {rec_word}.</span> {esc(p["why"])}')}
    <details class="tech"><summary>Technical</summary>{tech(i, m)}</details>
  </div>
</section>'''

def main():
    metas = {i: json.load(open(f"knowledge/components/{i}.meta.json")) for i in IDS}
    c = COVERAGE
    yes = sum(1 for i in IDS if P[i]["rec"] == YES)
    parts = "".join(part_section(k, i, metas[i]) for k, i in enumerate(IDS, start=3))
    toc = "".join(f'<a href="#p-{i}">{esc(WORD[i].split(" (")[0])}</a>' for i in IDS)
    total_calls = 1 + len(IDS) + 3 + 1
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cohort one trees</title>
<style>
:root{{--accent:#DA1A00;--fg:#000;--bg:#fff;--g1:#F3F3F3;--g2:#EDEDED;--g3:#D7D8D6;--g5:#9B9B9B;--g6:#767676;--g7:#545454;--g8:#333;--card:#fff;--code:#F3F3F3;
  --s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem;--s7:6rem;--max:1180px}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--accent:#FF6A55;--fg:#F2F2F2;--bg:#0E0E0E;--g1:#1A1A1A;--g2:#262626;--g3:#3A3A3A;--g5:#8A8A8A;--g6:#A3A3A3;--g7:#BDBDBD;--g8:#D6D6D6;--card:#141414;--code:#1F1F1F}}}}
:root[data-theme="dark"]{{--accent:#FF6A55;--fg:#F2F2F2;--bg:#0E0E0E;--g1:#1A1A1A;--g2:#262626;--g3:#3A3A3A;--g5:#8A8A8A;--g6:#A3A3A3;--g7:#BDBDBD;--g8:#D6D6D6;--card:#141414;--code:#1F1F1F}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
body{{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:16px;line-height:1.7;color:var(--fg);background:var(--bg);-webkit-font-smoothing:antialiased;overflow-x:hidden;padding-bottom:64px}}
.wrap{{max-width:var(--max);margin:0 auto;padding:0 32px}}
.label{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;gap:10px;align-items:center;margin:0 0 var(--s3);line-height:1.5}}
.label::before{{content:"";width:20px;height:1px;background:var(--accent);flex:none}}
p{{margin:0 0 var(--s2)}}
code{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.86em;background:var(--code);padding:.08em .35em;overflow-wrap:anywhere}}
a{{color:inherit}}
nav.toc{{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:1px solid var(--g2)}}
nav.toc .wrap{{display:flex;gap:var(--s3);align-items:center;height:52px;overflow-x:auto;scrollbar-width:none;padding-left:200px}}
nav.toc .wrap::-webkit-scrollbar{{display:none}}
nav.toc a{{font-size:13px;letter-spacing:.04em;color:var(--g6);text-decoration:none;white-space:nowrap}}
nav.toc a:hover{{color:var(--fg)}}
header{{padding:var(--s6) 0 var(--s5);border-bottom:1px solid var(--g2)}}
header .grid{{display:grid;grid-template-columns:2fr 1fr;gap:var(--s5);align-items:end}}
h1{{font-size:57px;font-weight:200;line-height:1.06;margin:0}}
.sub{{font-size:24px;font-weight:300;line-height:1.4;margin:var(--s3) 0 0;max-width:30em}}
.meta{{font-size:13px;line-height:1.7;color:var(--g7)}}
.meta span{{display:block}}
h2{{font-size:34px;font-weight:300;line-height:1.18;margin:0 0 var(--s3)}}
section{{padding:var(--s6) 0;border-bottom:1px solid var(--g2)}}
section.grey{{background:var(--g1)}}
.lead{{font-size:21px;font-weight:300;line-height:1.5;max-width:34em}}
.quote{{border-left:2px solid var(--accent);padding:.2rem 0 .2rem 1rem;margin:0 0 var(--s3);font-size:18px;font-weight:300;line-height:1.5;max-width:40em}}
/* the count */
.count{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g3);border:1px solid var(--g3);margin:var(--s3) 0}}
.count div{{background:var(--card);padding:var(--s2) var(--s3);min-width:0}}
.count b{{display:block;font-size:40px;font-weight:200;line-height:1.1}}
.count span{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);line-height:1.5}}
/* the words */
.words{{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s3);margin:var(--s3) 0 0}}
.words h3{{font-size:18px;font-weight:500;margin:0 0 var(--s1);line-height:1.3}}
.words p{{font-size:15px;line-height:1.55;color:var(--g8)}}
/* picture beside tree */
.part{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:var(--s3);margin:var(--s3) 0 var(--s2);align-items:start}}
.pic figure{{margin:0 0 var(--s2);background:var(--card);border:1px solid var(--g3);padding:var(--s2);display:flex;flex-direction:column;gap:var(--s1)}}
.pic img{{display:block;max-width:100%;width:auto;height:auto;align-self:flex-start;background:#fff;border:1px solid var(--g2)}}
.pic figcaption{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);line-height:1.5}}
.pic .links{{font-size:13px;color:var(--g7)}}
.tree{{border-top:1px solid var(--fg);min-width:0}}
.tree h4{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);font-weight:500;margin:var(--s2) 0 var(--s1);line-height:1.5}}
.tree h4 small{{font-size:11px;letter-spacing:0;text-transform:none;color:var(--g6);font-weight:400;margin-left:.5em}}
.outline,.outline ul{{list-style:none;margin:0;padding:0}}
.outline ul{{padding-left:1.1rem;border-left:1px solid var(--g3);margin-left:.35rem}}
.outline li{{font-size:14px;line-height:1.5;padding:2px 0;overflow-wrap:anywhere}}
.outline .pn{{font-weight:500}}
.outline .tg{{color:var(--g6);font-size:12px}}
.outline .tx{{color:var(--g6);font-size:12px;margin-left:3px}}
.h{{font-style:normal;font-size:10px;letter-spacing:.06em;text-transform:uppercase;padding:1px 5px;border:1px solid var(--g3);color:var(--g7);margin-left:3px;white-space:nowrap;vertical-align:1px}}
.h.st{{border-color:var(--accent);color:var(--accent)}}
.h.prop{{background:var(--g2)}}
.sts{{display:flex;flex-wrap:wrap;gap:.3rem}}
.sc{{font-size:12px;letter-spacing:.04em;padding:.25rem .55rem;border:1px solid var(--g3);color:var(--g8);line-height:1.35}}
.sc.on{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
.keys,.ev{{font-size:14px;line-height:1.55;margin:var(--s1) 0 0;color:var(--g8)}}
.keys .k,.ev .k{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);margin-right:.4em}}
.fires{{margin:.3rem 0 0;padding-left:1.2em;font-size:14px;line-height:1.55;color:var(--g8)}}
.fires li{{margin:0 0 3px}}
.binds{{list-style:none;margin:0;padding:0;font-size:13px;line-height:1.5;color:var(--g8)}}
.binds li{{overflow-wrap:anywhere}}
.binds .arr{{color:var(--g5);margin:0 .3em}}
details.more summary{{cursor:pointer;font-size:12px;color:var(--g6);padding:.3rem 0}}
.facts{{margin:var(--s3) 0 0;padding:0;list-style:none}}
.facts li{{display:grid;grid-template-columns:150px 1fr;gap:var(--s3);padding:var(--s2) 0;border-top:1px solid var(--g3);font-size:15px;line-height:1.6;color:var(--g8)}}
.facts li:last-child{{border-bottom:1px solid var(--g3)}}
.facts .k{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);line-height:1.5;padding-top:3px}}
.facts li b{{font-weight:500;color:var(--fg)}}
/* calls */
.call{{border:1px solid var(--g3);background:var(--card);padding:var(--s3);margin-top:var(--s3)}}
.call .q{{font-size:21px;font-weight:300;line-height:1.35;margin:0 0 var(--s2)}}
.call .q .rw{{font-weight:500}}
.chips{{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:var(--s2)}}
.chip{{font:inherit;font-size:12px;letter-spacing:.06em;padding:.5rem .8rem;border:1px solid var(--g3);background:var(--bg);color:var(--g8);cursor:pointer;border-radius:0;text-align:left;line-height:1.35}}
.chip:hover{{border-color:var(--fg);color:var(--fg)}}
.chip.on{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
.chip em{{font-style:normal;display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-top:2px}}
.chip.on em{{color:var(--bg)}}
.field{{display:flex;flex-direction:column;gap:.3rem}}
.field span{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);font-weight:500;line-height:1.5}}
.field textarea{{font:inherit;font-size:15px;line-height:1.5;color:var(--fg);background:var(--g1);border:0;border-bottom:1px solid var(--g3);padding:.6rem .75rem;min-height:4.5rem;resize:vertical;width:100%;border-radius:0}}
section.grey .field textarea{{background:var(--bg)}}
.field textarea:focus{{outline:none;border-bottom-color:var(--accent)}}
.stamp{{font-size:11px;color:var(--g6);margin-top:.4rem;min-height:1em}}
.bar{{position:fixed;left:0;right:0;bottom:0;z-index:99;background:#000;color:#fff;font-size:12px;letter-spacing:.04em;border-top:1px solid #333}}
.bar .in{{max-width:var(--max);margin:0 auto;padding:.6rem 32px;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}}
.bar b{{font-weight:500}}
.bar button{{font:inherit;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:.5rem .9rem;border:1px solid #767676;background:transparent;color:#fff;cursor:pointer;border-radius:0;line-height:1.4}}
.bar button:hover{{border-color:#fff}}
.bar button.pri{{background:#DA1A00;border-color:#DA1A00}}
.bar .msg{{color:#B7B7B7;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
details.tech{{font-size:13px;color:var(--g7);margin-top:var(--s2)}}
details.tech summary{{cursor:pointer;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--fg);font-weight:500;padding:var(--s1) 0}}
details.tech ol{{padding-left:1.6em;margin:var(--s2) 0 0}}
details.tech li{{margin:0 0 8px;line-height:1.6;overflow-wrap:anywhere}}
footer{{padding:var(--s5) 0;font-size:12px;color:var(--g6)}}
@media(max-width:900px){{
  .count,.words{{grid-template-columns:1fr 1fr}}
  .part{{grid-template-columns:1fr}}
}}
@media(max-width:760px){{
  .wrap{{padding:0 16px}}
  nav.toc .wrap{{padding-left:180px}}
  body{{padding-bottom:112px}}
  .bar .in>b{{display:none}}
  header{{padding-top:72px}}
  header .grid{{grid-template-columns:1fr;gap:var(--s3)}}
  h1{{font-size:38px}}.sub{{font-size:19px}}h2{{font-size:27px}}.lead{{font-size:18px}}
  .count,.words{{grid-template-columns:1fr}}
  .count b{{font-size:32px}}
  .facts li{{grid-template-columns:1fr;gap:4px}}
  .call{{padding:var(--s2)}}
  .bar .in{{padding:.55rem 16px;gap:.5rem}}
  .bar .msg{{flex-basis:100%;order:3}}
  section{{padding:var(--s5) 0}}
}}
@media print{{.bar,nav.toc,#rv-back{{display:none}}body{{padding-bottom:0}}}}
</style>
</head>
<body>
<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;background:#000;color:#fff;font:500 13px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>

<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#words">How to read a tree</a>
  <a href="#mapping">Menus and select</a>
  {toc}
  <a href="#rules">The words</a>
  <a href="#else">Anything else</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 312 · review page · Cohort one: fifteen trees, read by eye</p>
      <h1>Fifteen parts now carry a first draft of their spec. Here is each one, drawn as a tree beside its picture, for you to say whether the tree describes the part.</h1>
      <p class="sub">This morning you ruled that each part's spec lives in its meta: its anatomy, its states, what it fires, and its bindings to tokens. An extractor read those four out of the fifteen reference pages this afternoon. Nothing is inscribed until you answer; every draft is marked reviewed: false.</p>
    </div>
    <div class="meta">
      <span>Thursday 1 October 2026</span>
      <span>Read tonight, rule Friday. {total_calls} calls: the menus and select mapping, one per part, three on the words, and a note.</span>
      <span>Yes means the tree stands as the part's spec and the proposed events go in. Change it means say how in the comment.</span>
      <span>Revised after the verifier: button, table and metric moved from Yes to Change it.</span>
    </div>
  </div>
</header>

<section id="words">
  <div class="wrap">
    <p class="label">01 · Where it stands, and how to read a tree</p>
    <h2>All fifteen are drafted at full coverage: every part name points at a real element, every binding at a real token.</h2>
    <div class="count">
      <div><b>{c["full"]} of {c["cohort"]}</b><span>cohort parts drafted, full coverage</span></div>
      <div><b>{c["full"]} of {c["library"]}</b><span>library parts drafted so far</span></div>
      <div><b>{c["refused"]}</b><span>refused by name</span></div>
      <div><b>{c["bindings"]}</b><span>bindings, none unresolved</span></div>
    </div>
    <p class="record">Pasted from the extractor's report: {c["undrafted"]} parts not yet drafted, {c["fenced"]} fenced (alias seats), {c["exempt"]} exempt (the example). Recommendation on the fifteen: Yes on {yes}, Change it on {len(IDS) - yes}.</p>
    <p class="record">Full coverage is not the same as right. It means every name points at something real; it does not mean the tree describes the part. An independent check read all fifteen by eye this evening: the button's tree is plainly wrong (it is the Loading specimen), and the table's and the metric's are weak. All three now recommend Change it, and each says why. The other twelve were read the same way and their recommendations stand.</p>
    <p class="lead">Four words run through every tree. Here is what each means to a designer, so the trees below read without a glossary.</p>
    <div class="words">
      <div><h3>Anatomy</h3><p>The named pieces a part is made of, nested the way they sit: a date picker is a label, a box with an input and a calendar button, a message, and a panel with a head, a weekday row and a grid. Names are what you would point at. A small red tag marks where a state lands on a piece (disabled, selected); a grey tag marks where a choice of yours lands (the button's type, the metric's trend). ×6 means six of the same, drawn once.</p></div>
      <div><h3>States</h3><p>The looks a part can be in, with the one it rests in marked. Rest, hover, pressed, focus, disabled are the usual five; open, selected, expanded, error and the rest are the part's own. Keys say what the keyboard does. The draft also records how each look moves to the next; that is behind Technical.</p></div>
      <div><h3>Events</h3><p>What a part listens to (clicks, keys) and what it fires: the messages it sends out to the page when something happens in it, such as a tab chosen or a date picked. Every draft today says fires nothing, because the reference pages only react and never send a message out. So each part comes with a proposal in plain names; Yes takes the proposal.</p></div>
      <div><h3>Bindings</h3><p>The lines from a part's colours and measures to the tokens: the primary fill at rest is button / primary / background / default. Each line was checked against the token store. This is what lets another library paint the part in Apollo's colours.</p></div>
    </div>
  </div>
</section>

<section id="mapping" class="grey">
  <div class="wrap">
    <p class="label">02 · Menus and select · which part is which?</p>
    <h2>Your list said menus and select. Neither is a part's name in the library, so two parts were drafted as the nearest: the split button for menus, the dropdown for select.</h2>
    <p class="lead">The split button's flyout is the only true menu in the cohort, a list of actions. The dropdown is a select: one value chosen from a list of options. Another lane's name-matcher sends both your words to the dropdown, which is why this is a call and not a footnote.</p>
    <ul class="facts">
      <li><span class="k">Menus</span><span><b>Drafted as the split button.</b> Its menu carries the menu role and menu items, the most of any reference page. One thing to know: the split button meta is proposed at session 209 and has not been ruled. The alternative with real menus is the navigation header's flyouts, a much bigger part.</span></li>
      <li><span class="k">Select</span><span><b>Drafted as the dropdown.</b> It holds the custom list and the native select in one meta; the combobox and multi-select are separate parts, not in this cohort.</span></li>
      <li><span class="k">If you meant something else</span><span>Say which part you had in mind in the comment; it joins cohort two.</span></li>
    </ul>
    {call("mapping", "2. Menus and select: which part is which?", ["Menus = split button, select = dropdown", "Both = dropdown", "Change it (comment)"], "Menus = split button, select = dropdown", 'Which parts are menus and select? <span class="rw">Recommendation: menus = split button, select = dropdown.</span> They are the two parts that actually carry a menu and a select.')}
  </div>
</section>
{parts}

<section id="rules">
  <div class="wrap">
    <p class="label">{len(IDS) + 3:02d} · The words · three rules the fifteen trees need</p>
    <h2>The extractor names things the way the reference pages do. Three places it needs a rule from you rather than a guess.</h2>
    <p class="lead">Each of these shows up in several trees above. Settling them once here means the drafts can be fixed by rule in phase 2 instead of part by part.</p>

    <div class="sub3">
      <h3>Plain words where the markup has none</h3>
      <p>Where a piece has no class in the markup, the draft uses its tag: the table's rows and cells are tr, tr-2, td, v-2; the dialog's title and body are h2 and p; pagination's items are li, li-2, li-3, a. A designer would say row, cell, value, title, body, item, page link. The reference pages are not edited today, so the names would be set by hand, once per part, when a cohort is ratified.</p>
      {call("words", f"{len(IDS)+3}a. Plain words where the markup has none", ["Plain words, set by hand per part", "Keep the tag words as drafted", "Change it (comment)"], "Plain words, set by hand per part", 'When the markup gives a piece no name, what should the tree call it? <span class="rw">Recommendation: plain words, set by hand when each cohort is ratified.</span> A client library will map to the names; tr-2 will not survive that.')}
    </div>

    <div class="sub3">
      <h3>The rest state's name</h3>
      <p>Ten parts rest in default (their meta says so). The split button and the dialog rest in closed, because they open. The metric rests in ready, from its own state model. Three words for one idea. The schema has an initial field that names the rest state whatever it is called, so the choice is between one word everywhere and each part's own word.</p>
      {call("rest", f"{len(IDS)+3}b. The rest state's name", ["Each part's own word, initial names it", "One word everywhere: default", "Change it (comment)"], "Each part's own word, initial names it", 'What is the rest state called? <span class="rw">Recommendation: each part’s own word.</span> A closed dialog is closed, not default; the initial field already says which state is rest.')}
    </div>

    <div class="sub3">
      <h3>One state list per part, or per piece</h3>
      <p>Today a tree has one list of states for the whole part. So the date picker's list holds the field's states, the message's words (ok, info, warning), the panel's and a day's (today, selected) all together, each marked with where it was read from. The text input and the notification have the same mix. The alternative is for each piece to carry its own states: the message has ok, info, warning; the day has today, selected, empty; the field has rest, hover, focus, disabled, error. That is a schema change, done in phase 2.</p>
      {call("perpart", f"{len(IDS)+3}c. One state list per part, or per piece", ["Each piece carries its own states (phase 2)", "One list per part, as drafted", "Change it (comment)"], "Each piece carries its own states (phase 2)", 'Should states live on the pieces that show them? <span class="rw">Recommendation: yes, in phase 2.</span> A message’s warning and a day’s today are not states of the field; a client library needs to know which piece changes.')}
    </div>
  </div>
</section>

<section id="else" class="grey">
  <div class="wrap">
    <p class="label">{len(IDS) + 4:02d} · Anything else</p>
    <h2>Anything you want changed or looked at again.</h2>
    <div class="call" data-id="page" data-q="{len(IDS)+4}. Note on the page" data-rec="">
      <p class="q">Anything else on this page?</p>
      <label class="field"><span>Your note</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · review page · Cohort one: fifteen trees · v1, revised after the verifier · 2026-10-01 · session 312 lanes L3 and L3b</span>
  <span>No draft stands until you say.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of {total_calls} answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

<script>
(function(){{
  var KEY='review-312-L-cohort-one-trees-v1';
  var PATH='{OUT}';
  var state={{}};
  try{{ state=JSON.parse(localStorage.getItem(KEY)||'{{}}')||{{}}; }}catch(e){{ state={{}}; }}
  function save(){{ try{{ localStorage.setItem(KEY, JSON.stringify(state)); }}catch(e){{}} refresh(); }}
  function now(){{ var d=new Date(),p=function(n){{return (n<10?'0':'')+n;}}; return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes()); }}
  var calls=[].slice.call(document.querySelectorAll('.call'));
  function has(s){{ return s && (s.v || (s.note||'').trim()); }}
  function refresh(){{
    var n=0;
    calls.forEach(function(el){{
      var s=state[el.dataset.id]||{{}};
      if(has(s)) n++;
      [].forEach.call(el.querySelectorAll('.chip'),function(c){{ c.classList.toggle('on', c.dataset.v===s.v); c.setAttribute('aria-pressed', c.dataset.v===s.v?'true':'false'); }});
      el.querySelector('.stamp').textContent = s.at ? 'saved '+s.at : '';
    }});
    document.getElementById('count').textContent = n+' of '+calls.length+' answered';
  }}
  calls.forEach(function(el){{
    var id=el.dataset.id, s=state[id]||{{}};
    var ta=el.querySelector('textarea'); if(ta) ta.value=s.note||'';
    el.addEventListener('click',function(e){{
      var b=e.target.closest('.chip'); if(!b) return;
      var cur=state[id]||{{}}; cur.v=(cur.v===b.dataset.v)?'':b.dataset.v; cur.at=now(); state[id]=cur; save();
    }});
    el.addEventListener('input',function(e){{
      if(!e.target.dataset || e.target.dataset.f!=='note') return;
      var cur=state[id]||{{}}; cur.note=e.target.value; cur.at=now(); state[id]=cur; save();
    }});
  }});
  function text(){{
    var L=['Session 312 · Cohort one: fifteen trees · decisions','','Page: '+PATH,'Copied: '+now(),''];
    var page=null;
    calls.forEach(function(el){{
      var id=el.dataset.id, s=state[id]||{{}}, rec=el.dataset.rec||'', opts=el.querySelector('.chip');
      if(id==='page'){{ page=s; return; }}
      L.push(el.dataset.q);
      if(opts){{
        L.push('   Chose: '+(s.v? s.v+(rec?(s.v===rec?' (the recommendation)':' (not the recommendation)'):'') : 'not answered'));
      }}
      L.push('   Comment: '+((s.note||'').trim()? s.note.trim() : 'none'));
      L.push('');
    }});
    L.push('{len(IDS)+4}. Note on the page: '+(page && (page.note||'').trim()? page.note.trim() : 'none'));
    return L.join('\\n');
  }}
  window.__reviewText=text;
  function msg(t){{ document.getElementById('msg').textContent=t; }}
  function fallback(t){{
    var ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select();
    try{{ document.execCommand('copy'); msg('Copied. Paste it into the chat'); }}catch(e){{ msg('Copy blocked. Use Export instead'); }}
    ta.remove();
  }}
  document.getElementById('copy').onclick=function(){{
    var t=text();
    try{{ if(navigator.clipboard && navigator.clipboard.writeText){{ navigator.clipboard.writeText(t).then(function(){{msg('Copied. Paste it into the chat');}},function(){{fallback(t);}}); }} else fallback(t); }}catch(e){{ fallback(t); }}
  }};
  document.getElementById('export').onclick=function(){{
    try{{
      var blob=new Blob([text()],{{type:'text/plain'}}), a=document.createElement('a');
      a.href=URL.createObjectURL(blob); a.download='review-312-L-cohort-one-trees.txt';
      document.body.appendChild(a); a.click(); setTimeout(function(){{ URL.revokeObjectURL(a.href); a.remove(); }},500);
      msg('Exported as a text file');
    }}catch(e){{ msg('Export blocked. Use Copy as text'); }}
  }};
  document.getElementById('clear').onclick=function(){{
    if(!confirm('Clear every answer on this page?')) return;
    state={{}}; save(); [].forEach.call(document.querySelectorAll('.call textarea'),function(t){{t.value='';}}); msg('Cleared');
  }};
  refresh();
}})();
</script>
</body></html>
'''
    open(OUT, "w").write(page)
    print(OUT, len(page), "bytes;", total_calls, "calls; Yes", yes, "Change", len(IDS) - yes)

if __name__ == "__main__":
    main()
