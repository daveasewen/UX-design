"""#308 lane I - build the 15 ruling entries (s308-D1..D15) and one _wrap_rows spec from
Dave's review-page export. Every label, question and comment is read from the export's
machine copy, never retyped; the plain meanings and records are lane I's reading."""
import json, re, os
ROOT = os.getcwd()
EXP = "notes/_lanes/307/DAVE-RULINGS-2026-09-29-what-you-asked-to-see.md"
WORDS = "notes/_lanes/308/DAVE-WORDS-2026-09-29-0838.md"
PAGE = "notes/_REVIEW-307-what-you-asked-to-see-2026-09-28-v1.html"
CREP = "notes/_subreports/2026-09-28-307-C-what-you-asked-to-see.md"
OUT = "notes/_lanes/308/I"

t = open(EXP, encoding="utf-8").read()
mc = json.loads(re.search(r"```json\n(.*?)\n```", t, re.S).group(1))
calls = {c["id"]: c for c in mc["calls"]}
ans = mc["answers"]
w = open(WORDS, encoding="utf-8").read()
w0838 = re.search(r"^> (threat this as a ruling.*)$", w, re.M).group(1).strip()
assert w0838.startswith("threat this as a ruling: \"The red is correct")

SEC = {
 "c1": "1 of 5 · the dark caption", "c2a": "2 of 5 · the tree mark and the ring",
 "c2b": "2 of 5 · the tree mark and the ring", "c4": "4 of 5 · the five the build did not make",
 "c5a": "5 of 5 · the third red and the 29 forks", "c5b": "5 of 5 · the third red and the 29 forks",
 "c6": "6 · the fresh-session dashboard run"}
for i in range(1, 9): SEC[f"c3-{i}"] = "3 of 5 · the other eight wave-3 parts"

# order = page order; each: id, what, meaning, record, closes (rows closed with this ruling as last), mint
P = []
def add(cid, what, meaning, record, mint=None, extra_ev=()):
    P.append(dict(cid=cid, what=what, meaning=meaning, record=record, mint=mint, extra_ev=list(extra_ev)))

add("c1", "THE DARK CAPTION LIFT",
    "The dark caption lift stands in all four themes as the page drew it: mono, legacy and console lift 11 points of lightness from neutral 5 (#313131), supercharge lifts 9 from its own warm 5 (#312C26); light mode did not move. He has now seen the four side by side, which is what the review row W-307qi (from W-208, under s307-D38) owed him.",
    "W-307qi is closed by addition in knowledge/_state.json, `closed_by` naming this ruling. No work row: the answer closes it.")
add("c2a", "THE TREE'S CHOSEN MARK",
    "The tree's chosen mark stops being one rule for every theme and becomes a choice each theme makes: red in Supercharge and Common, black in Console and Mono. Not the page's recommendation (keep the black bar for chosen, apart from the navigation's red). On the page he ticked 'Keep it open' and wrote the decision beside it; at 08:34 BST the #308 conductor read the note back as a ruling and asked for the one word, and at 08:38 BST he confirmed it (his message below, verbatim).",
    "a live work row, W-308i1, carries the per-theme mark. The review row W-307qr (the tree mark and the ring, as pictures) closes with s308-D3, which answers its other half.",
    mint="i1", extra_ev=[WORDS])
add("c2b", "THE RING ON A DAY BOTH TODAY AND CHOSEN",
    "For a day that is both today and chosen, the today ring is set inside the chosen square, by the page's proposal: one rule, not in canon when he ruled, 'box-shadow: inset 0 0 0 3px var(--text), inset 0 0 0 5px var(--page)', drawn on the real Calendar part. The date picker follows, since it uses the calendar (s307-D49, W-307qq).",
    "a live work row, W-308i2, carries the change into the Calendar part. W-307qr is closed by addition, `closed_by` naming s308-D2 and this ruling: both its pictures have been seen and ruled.",
    mint="i2")
add("c3-1", "THE STANDING ORDER AND DIRECT DEBIT ROW",
    "The standing order and Direct Debit row is not its own part: it is reworked as a variant of list items, as the transaction row was (s307-D51). His comment asks to see options for it; his own first idea is to range the tag to the right.",
    "a live work row, W-308i3, carries the rework AND a page of options shown to him (his first idea among them). One of the eight answers that close W-307qu.",
    mint="i3")
add("c3-2", "THE LIMITS METER",
    "Nothing is left to rule: he folded the limits meter into one Meter with the progress bar on 20 August ('keep as one meter'), and the fold is done.",
    "no work row. One of the eight answers that close W-307qu (closed with s308-D11).")
add("c3-3", "THE RANGE SLIDER",
    "The range slider is not its own part: it is reworked as Slider's two-handle form, under his slider rules of 15 September.",
    "a live work row, W-308i4. One of the eight answers that close W-307qu.", mint="i4")
add("c3-4", "THE RATING",
    "The rating is kept and reworked, not deleted. Not the page's recommendation (delete it: no banking page asks for stars today). The fault the page showed: the average row's filled stars sit on the empty ones out of step. What follows the rework is left to him.",
    "a live work row, W-308i5, carries the rework and a showing to him. One of the eight answers that close W-307qu.", mint="i5")
add("c3-5", "THE TRANSFER LIST",
    "The transfer list is reworked, then promoted. The two faults the page showed: the 'move all' arrows are drawn with only half of the double-arrow icon, so they look the same as 'move one'; and the select-all box sits above its label, not beside it.",
    "a live work row, W-308i6. One of the eight answers that close W-307qu.", mint="i6")
add("c3-6", "THE SPLIT BUTTON",
    "The split button is promoted. It looked right in both modes, and a rule in the graph already names it (a modal gives way to a split button or a drop-down when either would do).",
    "a live work row, W-308i7, carries the promotion. One of the eight answers that close W-307qu.", mint="i7")
add("c3-7", "THE FLOATING ADD BUTTON",
    "The floating add button is reworked, then promoted. The rework is the repair already queued from #307 on W-307qy (three stray page rules in its overlay).",
    "a live work row, W-308i8, carries the promotion after W-307qy's repair. One of the eight answers that close W-307qu.", mint="i8")
add("c3-8", "BACK TO TOP",
    "Back to top is reworked, then promoted. The part is right; its reference page is not: the live demo text falls back to Times, a font the house never uses, and a note shows an empty box where a symbol should be.",
    "a live work row, W-308i9. The last of the eight answers: W-307qu is closed by addition, `closed_by` naming s308-D4..s308-D11.", mint="i9")
add("c4", "THE FIVE PARTS THE WAVE-3 BUILD DID NOT MAKE",
    "There were never five unbuilt parts: the wave-3 alpha lane of 25 August found all eight form parts it was sent for already built, made none, and left five questions. Four are done; the fifth, whether wave 3 is finished, closes with the rest, since he did not choose 'Keep the first question open (is wave 3 finished?)'.",
    "W-307qw is closed by addition in knowledge/_state.json, `closed_by` naming this ruling. No work row: the answer closes it.")
add("c5a", "THE THIRD RED IN MONO",
    "The third red, #A8000B (mono's error message box; legacy's red throughout), is NOT folded into mono's error red. Not the page's recommendation (fold it). He thinks there was a reason for it and wants it investigated separately. This is a keep-open, recorded as a ruling as s307-D41 recorded W-229's; nothing is folded.",
    "a live investigation row of its own, W-308ia. W-229 is closed as answered (with s308-D14): its forks question is handed on to W-308ib, its third-red question to W-308ia.",
    mint="ia", extra_ev=["notes/_subreports/2026-08-27-221-laneB.md"])
add("c5b", "THE 29 COLOUR FORKS",
    "The 29 forks are handed to Claude to settle within his rules, bringing back only the ones that are a real colour choice (the page's recommendation), with his caveat: some may have been chosen for both halation and contrast, and that must be investigated before any is treated as a repair.",
    "a live work row, W-308ib, carries the settling with his caveat verbatim. W-229 is closed by addition, `closed_by` naming s308-D13 and this ruling.",
    mint="ib", extra_ev=["notes/_subreports/2026-08-27-221-laneB.md"])
add("c6", "THE FRESH-SESSION DASHBOARD RUN",
    "The page's three fixes are taken and the frozen prompt is run again on the next cut. His comment: he wants to work on it together, he liked the blind run, and his own prompted dashboard (fettled over five rounds) is not an exemplar of any kind; it is never to be treated as the benchmark.",
    "W-307y7 (the run he asked for under s307-D66) is closed by addition: the run was filed and he has ruled on it. A live work row, W-308ic, carries the fixes, the next run and his comment verbatim.",
    mint="ic", extra_ev=["notes/_subreports/2026-09-28-307-E-cold-run.md"])
assert len(P) == 15

entries = []
for n, p in enumerate(P, 1):
    cid = p["cid"]; c = calls[cid]; a = ans[cid]
    label = a["verdict"]; rec = (label == c["recommendation"])
    rtag = "the recommendation" if rec else "NOT the recommendation"
    note = a.get("comment") or a.get("decision")
    note = note.strip() if note else None
    head = f"THE REVIEW PAGE'S CALL ON {p['what']} IS ANSWERED BY CLICK: {label.upper()}."
    if cid == "c2a":
        head = f"THE REVIEW PAGE'S CALL ON {p['what']} IS RULED IN HIS WORDS: A CHOICE EACH THEME MAKES, RED IN SUPERCHARGE AND COMMON, BLACK IN CONSOLE AND MONO."
    ruled = (f"{head} {p['meaning']} Dave's answer, by click, verbatim: '{label}' ({rtag}"
             + ("" if rec else f", which was '{c['recommendation']}'") + f"), to the call's question, verbatim: '{c['title']}'.")
    if note:
        kind = "His words on the call, verbatim" if cid == "c2a" else "His comment on the call, verbatim"
        ruled += f" {kind}: \"{note}\"."
    if cid == "c2a":
        ruled += f" His confirmation in chat #308 at 08:38 BST, verbatim: \"{w0838}\" (the last three sentences are the conductor's 08:34 read-back, which he pasted back as his ruling)."
    ruled += f" The #307 review page, section '{SEC[cid]}'. RECORD: {p['record']}"
    says = (f"review page export, Tue 2026-09-29 08:05 BST ({PAGE}, saved verbatim as {EXP}, committed at #308 in 00c12dd6; 15 of 16 answered, the whole-page note not answered by button) · section '{SEC[cid]}' · call {c['num']}, verbatim: '{c['title']}' — his answer, by click at {a['at'][-5:]} BST, verbatim: '{label}' ({rtag})")
    if note: says += f" · his {'words' if cid=='c2a' else 'comment'}, verbatim: \"{note}\""
    if cid == "c2a": says += f" · made a ruling by his 08:38 BST message in chat #308, saved verbatim as {WORDS}"
    gov = []
    ev = [f"chat #308 2026-09-29 (live) - his 08:05 BST export of the review page; his click on this call is in it, quoted verbatim in `says`",
          f"{EXP}#dd-{cid}", PAGE, CREP] + p["extra_ev"] + ["commit 00c12dd6 - his export (and his 08:38 words) committed at #308"]
    e = {"id": f"s308-D{n}", "date": "2026-09-29", "by": "Dave", "status": "ruled",
         "ruled": ruled, "says": says, "governs": None, "evidence": ev}
    p["id"] = e["id"]; p["label"] = label; p["rtag"] = rtag; p["note"] = note; p["at"] = a["at"][-5:]; p["q"] = c["title"]
    entries.append(e)

# governs: rows touched + the store
G = {"c1": ["W-307qi"], "c2a": ["W-307qr", "W-308i1"], "c2b": ["W-307qr", "W-308i2"], "c3-1": ["W-307qu", "W-308i3"],
     "c3-2": ["W-307qu"], "c3-3": ["W-307qu", "W-308i4"], "c3-4": ["W-307qu", "W-308i5"], "c3-5": ["W-307qu", "W-308i6"],
     "c3-6": ["W-307qu", "W-308i7"], "c3-7": ["W-307qu", "W-308i8"], "c3-8": ["W-307qu", "W-308i9"], "c4": ["W-307qw"],
     "c5a": ["W-229", "W-308ia"], "c5b": ["W-229", "W-308ib"], "c6": ["W-307y7", "W-308ic"]}
for p, e in zip(P, entries):
    e["governs"] = G[p["cid"]] + ["knowledge/_state.json"]
    json.dump(e, open(f"{OUT}/entries/{e['id']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

byc = {p["cid"]: p for p in P}
def clk(cid):
    p = byc[cid]; return f"{p['id']} (#308, Dave by click 2026-09-29 {p['at']} BST, verbatim: '{p['label']}')"
def minted_under(cid):
    p = byc[cid]
    s = (f"Minted #308 lane I under {p['id']} — Dave, by click at {p['at']} BST on 2026-09-29, verbatim: '{p['label']}' ({p['rtag']}), "
         f"answering the #307 review page call, verbatim: '{p['q']}'.")
    if p["note"]:
        s += f" His {'words' if p['cid']=='c2a' else 'comment'} on the call, verbatim: \"{p['note']}\"."
    return s
TAIL = f" Export: {EXP}; page: {PAGE}."
ops = []
def mint(i, cid, title, links, closes_when, extra):
    body = minted_under(cid) + " " + extra + TAIL
    ops.append({"op": "mint", "id": f"W-308{i}", "live": True, "owner": "claude", "title": title,
                "home": f"{EXP}#dd-{cid}", "links": links + [PAGE], "closes_when": closes_when, "body": body})

mint("i1", "c2a", "#308 review call 2a ruled - the tree's chosen mark per theme: red in Supercharge and Common, black in Console and Mono",
     ["W-307qr", WORDS, "knowledge/snippets/Tree.reference.html"],
     "the Tree part marks a chosen item per theme - red in Supercharge and Common, black in Console and Mono - in its reference file and canon, shown by a render of every theme in light and dark",
     f"Made a ruling by his 08:38 BST message in chat #308, verbatim: \"{w0838}\" (saved as {WORDS}). The mark stops being one rule for every theme and becomes a choice each theme makes. The builder settles which canon theme scope his 'Common' names (the page showed mono, legacy, console and supercharge; canon sets common alongside legacy) and says so in its report.")
mint("i2", "c2b", "#308 review call 2b ruled - set the today ring inside the chosen square on the calendar (the date picker follows)",
     ["W-307qr", "W-307qq", "knowledge/snippets/Calendar.reference.html", "knowledge/snippets/Date-picker.reference.html"],
     "the Calendar part draws a day that is both today and chosen with the ring set inside the square (the page's proposal rule or its equal), in canon, and the date picker shows the same, shown by a render in light and dark",
     "The page's proposal, one rule not in canon when he ruled: 'box-shadow: inset 0 0 0 3px var(--text), inset 0 0 0 5px var(--page)'.")
mint("i3", "c3-1", "#308 review call 3.1 ruled - rework the standing order and Direct Debit row as a list-items variant, and show Dave options for its tag",
     ["W-307qu", "W-307qt", "knowledge/snippets/Standing-order-mandate-row.reference.html", "knowledge/snippets/List-items.reference.html"],
     "the standing order and Direct Debit row exists as a list-items variant (not its own part), and a page has shown Dave options for it - his own first, the tag ranged to the right, beside others - and he has seen it and ruled",
     "His comment asks for options, so this row includes showing them to him; his own idea is one option, not the ruling.")
mint("i4", "c3-3", "#308 review call 3.3 ruled - rework the range slider as Slider's two-handle form",
     ["W-307qu", "knowledge/snippets/Slider.reference.html", "notes/_receipts/2026-08-20-209-wave3-laneB-selection-controls.md"],
     "the range slider exists as Slider's two-handle form (not its own part), under the slider rules of 15 September, shown by the metas and a render",
     "A range is a slider with two handles; his slider rules already cover it.")
mint("i5", "c3-4", "#308 review call 3.4 ruled - rework the rating (not deleted: it will be in some apps)",
     ["W-307qu", "knowledge/snippets/Rating.reference.html", "notes/_receipts/2026-08-20-209-wave3-laneB-selection-controls.md"],
     "the rating is reworked - the average row's filled stars in step with the empty ones - rendered in light and dark, and Dave has seen it and ruled what follows",
     "Not the recommendation (delete). He chose 'Rework' alone, not promote, so what follows the rework is his.")
mint("i6", "c3-5", "#308 review call 3.5 ruled - rework the transfer list, then promote it",
     ["W-307qu", "knowledge/snippets/Transfer-list.reference.html", "notes/_receipts/2026-08-20-209-wave3-laneB-selection-controls.md"],
     "'move all' is drawn with the full double-arrow icon (not half of it), the select-all box sits beside its label, and the transfer list is promoted, shown by a render and its meta",
     "The two faults the page showed are the rework.")
mint("i7", "c3-6", "#308 review call 3.6 ruled - promote the split button",
     ["W-307qu", "knowledge/snippets/Split-button.reference.html", "notes/_receipts/2026-08-20-209-wave3-laneC-action-chrome.md"],
     "the split button is promoted, shown by its meta and the catalogue",
     "No fault to fix; a graph rule already names it.")
mint("i8", "c3-7", "#308 review call 3.7 ruled - rework the floating add button (W-307qy), then promote it",
     ["W-307qu", "W-307qy", "knowledge/snippets/Fab.reference.html", "notes/_receipts/2026-08-20-209-wave3-laneC-action-chrome.md"],
     "W-307qy (the three stray body rules in the overlay) is closed and the floating add button is promoted, shown by a render and its meta",
     "The rework is the repair already queued on W-307qy; this row is the promotion after it.")
mint("i9", "c3-8", "#308 review call 3.8 ruled - rework back to top's reference page, then promote it",
     ["W-307qu", "knowledge/snippets/Back-to-top.reference.html", "notes/_receipts/2026-08-20-209-wave3-laneC-action-chrome.md"],
     "back to top's reference page is repaired (the live demo text no longer falls back to Times; the note's empty box shows its symbol) and the part is promoted, shown by a render and its meta",
     "The part is right; only the page that shows it is wrong.")
mint("ia", "c5a", "#308 review call 5a kept open - investigate the third red in mono (#A8000B) separately; not folded",
     ["W-229", "notes/_subreports/2026-08-27-221-laneB.md"],
     "a filed investigation finds why mono's error message box paints the third red #A8000B (and how it relates to legacy's red), shows it to Dave, and he has ruled",
     "Not the recommendation (fold it into mono's error red). Nothing is folded. The page's facts: mono's field paints #F6604C in both modes, mono's message box paints #A8000B, legacy uses #A8000B throughout, console and supercharge use #B92F1E; and his two-red law puts the dark red on white while mono's field on white paints the light red.")
mint("ib", "c5b", "#308 review call 5b ruled - Claude settles the 29 colour forks within his rules, after checking each for halation and contrast",
     ["W-229", "notes/_subreports/2026-08-27-221-laneB.md", "knowledge/_TOKEN-FORK-LEDGER.json"],
     "each of the 29 forks is settled within his rules and filed with a line each, every one first checked for whether its value was chosen for halation and contrast, and only the real colour choices are brought back to Dave",
     "His caveat governs the order: investigate before repairing. The #221 --err forks in mono are the third red and wait on W-308ia.")
mint("ic", "c6", "#308 review call 6 ruled - the three fixes, then the fresh-session run again on the next cut with Console, worked through with Dave",
     ["W-307y7", "notes/_subreports/2026-09-28-307-E-cold-run.md", "reviews/COLDRUN-307-2026-09-28-v1.html"],
     "the fixes have landed (one headless load with a console read as the skill's default last step; the screen gate stops reading comments), the frozen prompt has been run again on the next cut with Console as the theme answer, and the result is filed and gone through with Dave; his own prompted dashboard is not used as the benchmark",
     "The page's three fixes, verbatim: 'the three fixes: one headless load with a console read as the skill's default last step; the screen gate stops reading comments (it fails the page on a word inside the chart engine's own comment); then run again on the next cut, theme answered as Console.' His comment means his own prompted dashboard is NOT the benchmark for this or any later run.")

def close(rid, closed_by):
    ops.append({"op": "close", "id": rid, "closed_by": closed_by})
close("W-307qi", f"{clk('c1')}: answered. He has seen the four themes' dark captions side by side; the lifts stand. No work row.")
close("W-307qr", f"{clk('c2a')} and {clk('c2b')}: both pictures seen and ruled. The tree's chosen mark is a per-theme choice (red in Supercharge and Common, black in Console and Mono; his words, made a ruling at 08:38 BST in chat #308); the ring is set inside the square. The doing is live rows W-308i1, W-308i2.")
close("W-307qu", "s308-D4..s308-D11 (#308, Dave by click 2026-09-29 07:29-07:33 BST): all eight seen and ruled. Standing order row: rework as a list-items variant (W-308i3); limits meter: closed, already part of Meter; range slider: Slider's two-handle form (W-308i4); rating: rework, not deleted (W-308i5); transfer list: rework then promote (W-308i6); split button: promote (W-308i7); floating add button: rework then promote (W-308i8); back to top: rework then promote (W-308i9).")
close("W-307qw", f"{clk('c4')}: answered. Nothing was left unbuilt; four of the five questions were done and the fifth (is wave 3 finished?) closes with it. No work row.")
close("W-229", f"{clk('c5a')} and {clk('c5b')}: answered on the #307 review page, where he saw what he asked to check visually. The 29 forks are handed to Claude to settle within his rules, with his caveat on halation and contrast (W-308ib); the third red is kept open and investigated separately, as he asked, on its own row (W-308ia).")
close("W-307y7", f"{clk('c6')}: answered. The run was filed and he ruled on it. The doing is live row W-308ic.")
spec = {"session": 308, "by": "#308 I (2026-09-29)", "ops": ops}
json.dump(spec, open(f"{OUT}/rows.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entries), "entries;", len(ops), "ops")
