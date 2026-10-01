#!/usr/bin/env python3
"""#313 lane B123 — builds notes/_REVIEW-313-B123-two-list-rows-2026-10-01-v1.html.

Two calls for Dave, both rows drawn LIVE on canon (the page links knowledge/canon/canon.css and
type.css and wraps every specimen in .cn-list-items, light and dark), so opened from the repo the
pictures are canon as committed; nothing here is a screenshot.

  1. W-308i3 / s308-D4 — the standing order and Direct Debit row as a list-items row: where its tag
     goes. His own idea first ("range the tag to the right"), then three others.
  2. W-307qt / s307-D51 — the statement line (the #209 Transaction row) as a list-items row: where the
     running balance goes.

Shell (CSS, export bar, glance table script) is copied from the #312 F page so the export reads the
same. Run from the repo root:  python3 notes/_lanes/313/B123/build_list_rows_page.py
"""
import os, re, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "notes", "_REVIEW-312-F-the-pictures-you-are-owed-2026-10-01-v1.html")
OUT = os.path.join(ROOT, "notes", "_REVIEW-313-B123-two-list-rows-2026-10-01-v1.html")
PATH = "notes/_REVIEW-313-B123-two-list-rows-2026-10-01-v1.html"
KEY = "review-313-B123-two-list-rows-v1"

src = open(SRC, encoding="utf-8").read()
shell_css = src[src.index("<style>") + 7:src.index("</style>")]
shell_js = src[src.index("<script>\n(function(){") + 8:src.rindex("</script>")]
shell_js = (shell_js.replace("review-312-F-the-pictures-you-are-owed-v1", KEY)
            .replace("notes/_REVIEW-312-F-the-pictures-you-are-owed-2026-10-01-v1.html", PATH)
            .replace("Session 312 · The pictures you are owed · comments", "Session 313 · Two list rows · comments")
            .replace("review-312-F-the-pictures-you-are-owed.txt", "review-313-B123-two-list-rows.txt"))
assert KEY in shell_js and PATH in shell_js

E = html.escape

# ---------------------------------------------------------------- the data (from the #209 snippets)
MANDATES = [  # payee, initials, type, rhythm, when, amount, state (cls, word) or None
    ("Wrenfield Property Ltd", "WP", "Standing order", "Monthly on the 1st", "Next 1 July", "£2,150.00", None),
    ("Severn Energy Business", "SE", "Direct Debit", "Monthly, around the 14th · amount varies", "Last taken 14 June", "£486.20", None),
    ("Harbour Fitness", "HF", "Direct Debit", "Monthly on the 5th", "Resumes 5 August", "£44.00", ("warn", "Paused")),
    ("Bristol Trade Supplies", "BT", "Standing order", "Weekly on Fridays", "Retry 19 June", "£780.00", ("warn", "Last payment failed")),
    ("Kestrel Asset Finance — equipment loan agreement 44-20916", "KA", "Standing order", "Monthly on the 20th", "Next 20 July", "£1,204.55", ("inf", "2 payments left")),
]
# statement lines: day, title, initials, how, ref, amount, balance, state
STATEMENT = [
    ("Tuesday 23 June", [
        ("Tesco Stores 3217", "TS", "Card", "Ref 4471", "−£62.40", "—", ("warn", "Pending")),
        ("Northgate Logistics", "NL", "Faster Payment in", "Ref INV-2291", "+£2,500.00", "£6,147.60", None),
    ]),
    ("Monday 22 June", [
        ("Wrenfield Property Ltd", "WP", "Standing order", "Ref RENT-JUN", "−£2,150.00", "£3,647.60", None),
        ("Harbour Fitness", "HF", "Direct Debit", "Ref 8800213", "+£44.00", "£5,797.60", ("inf", "Reversed")),
    ]),
]


def chip(state):
    cls, word = state
    return f'<span class="status {cls} t-cm-legal" data-carries="label"><span class="dot" aria-hidden="true"></span>{E(word)}</span>'


def tag(word):
    return f'<span class="tag t-cm-legal">{E(word)}</span>'


def row(title, initials, right1, desc, amount, extra2=""):
    return (f'<li><a class="row" href="#" onclick="return false">'
            f'<span class="avatar t-cm-caption" role="img" aria-label="{E(title)}">{E(initials)}</span>'
            f'<span class="body">'
            f'<span class="line"><span class="title">{E(title)}</span>{right1}</span>'
            f'<span class="line"><span class="desc">{E(desc)}</span>{extra2}<span class="amount">{E(amount)}</span></span>'
            f'</span></a></li>')


def mandate_rows(opt):
    out = []
    for payee, ini, typ, rhythm, when, amt, st in MANDATES:
        if opt == 1:      # his: the type tag ranged right, the state chip beside it
            right = tag(typ) + (chip(st) if st else "")
            desc = f"{rhythm} · {when}"
        elif opt == 2:    # one chip on the right: the state when there is one, else the type
            right = chip(st) if st else tag(typ)
            desc = f"{typ} · {rhythm} · {when}"
        elif opt == 3:    # no type tag: the type is a word; only a state shows a chip
            right = chip(st) if st else ""
            desc = f"{typ} · {rhythm} · {when}"
        else:
            raise ValueError(opt)
        out.append(row(payee, ini, right, desc, amt))
    return out


def mandate_list(opt):
    if opt == 4:          # grouped by type under two list headings; only a state shows a chip
        parts = []
        for head, typ in (("Standing orders", "Standing order"), ("Direct Debits", "Direct Debit")):
            rows = [row(p, i, chip(s) if s else "", f"{r} · {w}", a)
                    for p, i, t, r, w, a, s in MANDATES if t == typ]
            parts.append(f'<h3 class="opt-head t-cm-caption">{E(head)}</h3><ul class="list">{"".join(rows)}</ul>')
        return "".join(parts)
    return f'<ul class="list">{"".join(mandate_rows(opt))}</ul>'


def statement_list(opt):
    parts = []
    for day, lines in STATEMENT:
        rows = []
        for title, ini, how, ref, amt, bal, st in lines:
            right = chip(st) if st else ""
            if opt == 1:   # the balance on the reference line (the #209 'signed' form), amount right
                rows.append(row(title, ini, right, f"{how} · {ref} · Balance {bal}", amt))
            else:          # the balance as a second figure, right, under the amount
                rows.append(
                    f'<li><a class="row" href="#" onclick="return false">'
                    f'<span class="avatar t-cm-caption" role="img" aria-label="{E(title)}">{E(ini)}</span>'
                    f'<span class="body">'
                    f'<span class="line"><span class="title">{E(title)}</span>{right}<span class="amount">{E(amt)}</span></span>'
                    f'<span class="line"><span class="desc">{E(how)} · {E(ref)}</span><span class="opt-bal">Balance {E(bal)}</span></span>'
                    f'</span></a></li>')
        parts.append(f'<h3 class="opt-head t-cm-caption">{E(day)}</h3><ul class="list">{"".join(rows)}</ul>')
    return "".join(parts)


def pair(builder, opt, cap):
    cells = []
    for mode in ("light", "dark"):
        cells.append(
            f'<figure><figcaption>{E(cap)} · Mono {mode}</figcaption>'
            f'<div class="opt-ground" data-theme="{mode}"><div class="cn-list-items"><div class="wrap">'
            f'{builder(opt)}</div></div></div></figure>')
    return f'<div class="pair">{"".join(cells)}</div>'


PAGE_CSS = """
/* page-only: grounds for the live specimens, and the two deltas the options need */
.opt-ground{padding:16px;background:var(--page,#fff);overflow:hidden}
.opt-ground[data-theme="light"]{background:#FFFFFF}
.opt-ground[data-theme="dark"]{background:#1A1A1A}
.opt-ground .cn-list-items .wrap{margin-bottom:0;max-width:none;padding:0}   /* the shell's own .wrap padding must not reach the specimen */
.opt-ground .cn-list-items a.row{display:flex;text-decoration:none}   /* the shell's `.pair a{display:block}` would otherwise beat the row */
.opt-ground .opt-head{margin:16px 0 8px;color:var(--text)}
.opt-ground .opt-head:first-child{margin-top:0}
.opt-ground .opt-bal{flex:none;font:400 14px/1.3 var(--font);font-variant-numeric:tabular-nums;color:var(--muted);white-space:nowrap;margin-left:auto}
.opt-ground .line .status + .amount{margin-left:12px}
"""


def call(cid, q, rec, options, ask, note_label="Your comment"):
    chips = "".join(
        f'<button type="button" class="chip" data-v="{E(v)}">{E(lbl)}{"<em>Recommended</em>" if v == rec else ""}</button>'
        for v, lbl in options)
    chips += '<button type="button" class="chip" data-v="None of these (comment)">None of these (say below)</button>'
    return (f'<div class="call" data-id="{cid}" data-q="{E(q)}" data-rec="{E(rec)}">'
            f'<p class="q">{E(ask)}</p><p class="rec">Recommended: {E(rec)}.</p>'
            f'<div class="chips">{chips}</div>'
            f'<label class="field"><span>{note_label}</span><textarea data-f="note"></textarea></label>'
            f'<div class="stamp"></div></div>')


so_opts = [(1, "Option 1 · your idea: the type tag ranged right, the state beside it"),
           (2, "Option 2 · one chip, ranged right: the state when there is one, otherwise the type"),
           (3, "Option 3 · no type tag: the type is a word on the second line; only a state shows a chip"),
           (4, "Option 4 · grouped: standing orders and Direct Debits under their own list headings")]
st_opts = [(1, "Option 1 · the balance on the second line, after the reference"),
           (2, "Option 2 · the balance as a second figure, right, under the amount")]

so_section = f"""
<section id="mandate">
  <div class="wrap">
    <p class="label">01 · The standing order and Direct Debit row · your call</p>
    <h2>The row becomes a list-items row. The type tag moves to the right, and only one chip shows at a time: the state when there is one, otherwise the type.</h2>
    <p class="quote">"my immediate improvement would be to range the tag to the right but lets see some other options"<small>Your comment on the 29 September review page, when you ruled the row a variant of list items</small></p>
    <p class="lead">Each picture is the list-items row as canon draws it today: the round avatar, the title and one detail on the first line, the description and the amount on the second. Only the tag moves between the options; the five payments are the ones the old part showed. The old part's manage button is left out of every picture so the tag is the only thing that changes; it is a second action on the row and comes back as built.</p>
    {"".join(pair(mandate_list, o, lbl.split(' · ')[0]) + f'<p class="opt-cap">{E(lbl)}</p>' for o, lbl in so_opts)}
    <ul class="facts">
      <li><span class="k">Option 1 · your idea</span><span>The type tag sits at the right of the first line, where a list-items row keeps its detail, and a state chip sits beside it when the mandate has one. A failed payment shows two chips, and at phone width the two chips leave no room for the payee's name at all and run past the row's edge.</span></li>
      <li><span class="k">Option 2 · one chip</span><span>Your placement, with list items' own rule: the first line has one detail slot, a tag or a status. The state wins when there is one; otherwise the type shows. The type is also written on the second line, so it is never lost.</span></li>
      <li><span class="k">Option 3 · no tag</span><span>The type is a word on the second line; the right of the first line is empty unless something needs attention. Quietest, and the type is easiest to miss.</span></li>
      <li><span class="k">Option 4 · grouped</span><span>Two lists under their own headings, so no row needs to say its type. Costs a heading and splits one list into two.</span></li>
      <li><span class="k">Why option 2</span><span>It keeps your move to the right and stays inside the row as list items already build it: one detail on the first line, never two chips competing. The type is still on every row, as text.</span></li>
      <li><span class="k">What it changes</span><span>The standing order part stops being its own part: it becomes list items' mandate row, built on the list-items reference file, and its old file is retired. Closes the rework you ruled on 29 September.</span></li>
    </ul>
    {call("mandate-tag", "1. Where the standing order row's tag goes", "Option 2, one chip ranged right", [("Option 1, your idea: tag right, state beside it", "Option 1 · your idea"), ("Option 2, one chip ranged right", "Option 2"), ("Option 3, no type tag", "Option 3"), ("Option 4, grouped under two headings", "Option 4")], "Which placement stands for the tag?")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Drawn live: this page links <code>knowledge/canon/canon.css</code> and <code>type.css</code> and wraps each specimen in <code>.cn-list-items</code>; every row is the list-items row (<code>.row &gt; .avatar + .body &gt; .line × 2</code>), the chips are its <code>.tag</code> and <code>.status</code>. Page-only CSS: the grounds, the list headings (the optional list-level heading, <code>s274-D5</code>). Built by <code>notes/_lanes/313/B123/build_list_rows_page.py</code>, #313 lane B123, in the cloud: fonts there are fallbacks, so the seat's render is the one to look at.</li>
      <li>Ruling: <code>s308-D4</code> (rework as a list-items variant, show options, his idea among them). Row <code>W-308i3</code>. The old part: <code>knowledge/snippets/Standing-order-mandate-row.reference.html</code> (#209 wave 3, proposed, never ruled).</li>
      <li>If taken: the mandate row is drawn into <code>knowledge/snippets/List-items.reference.html</code> as its own section on the existing row classes (option 2 needs no new CSS), <code>list-items.meta.json</code> gains the <code>mandate</code> row variant, and <code>standing-order-mandate-row.meta.json</code> becomes an alias seat (the <code>kpi-tile</code> shape, <code>s308-D42</code>). Still the old part's own open questions, carried: the word for each type, a variable Direct Debit's figure, whether a failed payment takes the error seat, the second action's form.</li>
    </ol></details>
  </div>
</section>
"""

st_section = f"""
<section id="statement" class="grey">
  <div class="wrap">
    <p class="label">02 · The statement line, the old transaction row · your call</p>
    <h2>The statement line becomes a list-items row, days as list headings, and the running balance is written on the second line after the reference.</h2>
    <p class="lead">You made the transaction row a variant of list items on 28 September. As its own part it was a ledger: money out, money in and a running balance in columns. As a list row only its signed form fits: one amount with a minus sign, the balance moved onto the reference line, which is how that part already drew a phone width. Pending shows a dash for the balance; a reversal says so in a chip.</p>
    {"".join(pair(statement_list, o, lbl.split(' · ')[0]) + f'<p class="opt-cap">{E(lbl)}</p>' for o, lbl in st_opts)}
    <ul class="facts">
      <li><span class="k">Option 1 · balance on the second line</span><span>The row as list items builds it: title and chip on the first line, how, reference and balance on the second, the amount at the right. Each payment is read across its own row. The cost, seen in these pictures: at this width the second line is cut and the balance is the part that goes first (\u201cBalance £5,\u2026\u201d). Built, the reference would have to give way to the balance, or the balance would come first on the line.</span></li>
      <li><span class="k">Option 2 · balance under the amount</span><span>The amount moves up to the first line and the balance becomes a second figure at the right. Balances then stack in a column, and a column read down is a table, by the line you ruled tonight.</span></li>
      <li><span class="k">Why option 1</span><span>It is the list-items row unchanged, and it keeps your line: read across, a list; read down, a table. If you would rather never see a cut balance, option 2 is the honest alternative.</span></li>
      <li><span class="k">Not asked here</span><span>Your comment tonight, that a natural order such as transactions by date may itself make something a list, is yours to think through and stays open. These pictures are in date order because statements are; they do not answer it.</span></li>
      <li><span class="k">What it changes</span><span>The transaction row stops being its own part: list items gains a statement row, its old file is retired, and its own open questions come with it (the reference line's contents, whether a line opens a receipt).</span></li>
    </ul>
    {call("statement-balance", "2. Where the statement line's running balance goes", "Option 1, balance on the second line", [("Option 1, balance on the second line", "Option 1"), ("Option 2, balance under the amount", "Option 2")], "Which placement stands for the running balance?")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Ruling: <code>s307-D51</code> (the transaction row a variant of list items). Row <code>W-307qt</code>. The old part: <code>knowledge/snippets/Transaction-row.reference.html</code> (#209, proposed, never ruled; its <code>signed</code> variant is option 1's source).</li>
      <li>Option 2 adds one page-only class (<code>.opt-bal</code>) for the balance figure; option 1 uses the row's classes only.</li>
      <li>The list rule tonight: <code>s313-D27</code> (option 1, the toolbar does not change the shape), written into <code>list-items.meta.json</code> and <code>data-grid.meta.json</code> <code>when</code> by this lane. The natural-order question is <code>W-313d2</code>, his.</li>
    </ol></details>
  </div>
</section>
"""

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Two list rows</title>
<link rel="stylesheet" href="../knowledge/canon/type.css">
<link rel="stylesheet" href="../knowledge/canon/canon.css">
<style>{shell_css}
.opt-cap{{font-size:13px;color:var(--g7);margin:-8px 0 var(--s3)}}
{PAGE_CSS}</style>
</head>
<body>
<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#glance">Glance</a>
  <a href="#mandate">Standing orders</a>
  <a href="#statement">Statement line</a>
  <a href="#else">Note</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 313 · review page · Two list rows</p>
      <h1>Two old parts become list-items rows. Where their extra detail goes is yours.</h1>
      <p class="sub">The standing order row's tag, and the statement line's running balance. Each drawn live on canon, light and dark, with a recommendation.</p>
    </div>
    <div class="meta">
      <span>Thursday 1 October 2026</span>
      <span>Drawn live from canon.css when opened from the repo; built in the cloud by lane B123, so the seat renders the real type.</span>
      <span>A drawn option is not a ruling. Nothing is built into list items until you answer.</span>
    </div>
  </div>
</header>

<section id="glance">
  <div class="wrap">
    <p class="label">At a glance · every call and its recommendation</p>
    <h2>If you take both recommendations, this is what you are saying.</h2>
    <p class="lead">One row per call. The answer column fills as you click.</p>
    <div class="scroll"><table class="ctab" id="glance-table"><thead><tr><th>#</th><th>The call</th><th>Recommended</th><th>Your answer</th></tr></thead><tbody></tbody></table></div>
  </div>
</section>
{so_section}
{st_section}
<section id="else">
  <div class="wrap">
    <p class="label">03 · Anything else</p>
    <h2>Anything you want changed, drawn again, or asked a different way.</h2>
    <div class="call" data-id="page" data-q="3. Note on the page" data-rec="">
      <p class="q">Anything else on this page?</p>
      <label class="field"><span>Your note</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · review page · Two list rows · v1 · 2026-10-01 · session 313 lane B123</span>
  <span>A drawn option is not a ruling. Nothing stands until you say.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of 2 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

<script>{shell_js}</script>
</body></html>
"""
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", os.path.relpath(OUT, ROOT), len(page), "bytes")
