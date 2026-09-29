"""#308 lane I round 5 - Dave's five cards-and-tiles answers (18:56 BST) -> s308-D39..D43; build rows
W-308ir..iv; Dave's naming row W-308iw; his page note recorded verbatim (not ruled); W-308o5 closed.
Calls (question, paragraph, options, recommendation) are parsed from the page's own CALLS script."""
import json, re
W = "notes/_lanes/308/DAVE-RULINGS-2026-09-29-1856-cards-and-tiles.md"
P = "notes/_RESEARCH-308-cards-tiles-containers-2026-09-29-v1.html"
REP = "notes/_subreports/2026-09-29-308-O-ontology-research.md"
OUT = "notes/_lanes/308/I"
h = open(P, encoding="utf-8").read()
blk = re.search(r"var CALLS=\[(.*?)\n  \];", h, re.S).group(1)
calls = []
for m in re.finditer(r"\{t:'(.*?)',p:'(.*?)',\s*o:\[(.*?)\],r:(\d)\}", blk, re.S):
    opts = re.findall(r"'(.*?)'", m.group(3))
    calls.append(dict(t=m.group(1), p=m.group(2), o=opts, r=int(m.group(4))))
assert len(calls) == 5 and all("'" not in c["p"] for c in calls)
w = open(W, encoding="utf-8").read()
qs = re.findall(r"^> ([1-5])\. (.+)$", w, re.M)
ch = re.findall(r"^> Chose: (.+)$", w, re.M)
assert len(qs) == 5 and len(ch) == 5
for (n, q), c, cc in zip(qs, calls, ch):
    assert q == c["t"], (q, c["t"])
    assert cc == c["o"][c["r"]] + " (the recommendation)", cc
note = w.split("> Page note: ", 1)[1].rstrip("\n")
note = "\n".join(l[2:] if l.startswith("> ") else (l[1:] if l.startswith(">") else l) for l in note.split("\n")).strip()
NOTE_PLAIN = note.replace("\n\n", " / ").replace("\n", " / ")
ROWS = ["W-308ir", "W-308is", "W-308it", "W-308iu", "W-308iv"]
HEAD = ["WHERE THE LINE SITS BETWEEN A CARD AND A TILE", "HOW CONTAINMENT IS CHECKED", "WHAT HAPPENS TO CONTAINER, SURFACE AND PANEL",
        "WHETHER THE STAT CARD AND THE KPI TILE BECOME ONE BLOCK, METRIC", "WHICH NESTING LIMITS ARE WRITTEN IN"]
entries = []
for i, c in enumerate(calls):
    n = i + 1; lab = c["o"][c["r"]]
    ruled = (f"THE CARDS-AND-TILES CALL ON {HEAD[i]} IS ANSWERED BY CLICK: {lab.upper()}. "
             f"Dave's answer, by click, verbatim: '{lab}' (the recommendation), to the call's question, verbatim: '{c['t']}'. "
             f"The page's recommendation in full, verbatim: 'Recommendation: {lab}', set under the call's text, verbatim: '{c['p']}'. "
             f"The research page {P} (lane O round 3), which marks its five kinds and accept rules as proposals, not rulings, until ruled. "
             f"His page note (three naming questions) is NOT part of this ruling; it is recorded on W-308iw and waits for his words. "
             f"RECORD: a live work row, {ROWS[i]}, owner claude, carries the build; nothing is built by this ruling.")
    says = (f"chat #308, Tue 2026-09-29 18:56 BST, his answers pasted as the cards-and-tiles page's 'Copy as text', saved verbatim as {W} "
            f"(5 of 5 answered, all the recommendation, with a page note) · call {n}, verbatim: '{c['t']}' — his click, verbatim: 'Chose: {lab} (the recommendation)'")
    ev = [f"chat #308 2026-09-29 (live) - his 18:56 BST answers; call {n} is quoted verbatim in `says`",
          f"{W}#> {n}. {c['t']}", f"{P}#{c['t']}", REP]
    e = {"id": f"s308-D{38+n}", "date": "2026-09-29", "by": "Dave", "status": "ruled", "ruled": ruled, "says": says,
         "governs": [ROWS[i], "knowledge/_state.json"], "evidence": ev}
    json.dump(e, open(f"{OUT}/entries5/{e['id']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    entries.append(e)
CW = [
 "the register or knowledge/roles.json carries Canonical's line (card = one of a set of like records; tile = one bento cell, surfaced, holding one thing) and the five kinds the page proposed (layout, holder, record, block, part), each component declaring one kind; the kind named 'holder' is written as a PENDING placeholder, marked so, until Dave's word on W-308iw is inscribed",
 "a check reads each container slot's 'accepts' clause by kind and reports any containedBy line the parent does not accept (NOT-ACCEPTED, TOO-MANY/MISSING, MIXED-SLOTS), ADVISORY first, wired into the build; the pair 'a carousel holds cards' is derived by the check, not authored",
 "container is the register's umbrella word (never a component name except the layout utility), surface is a property (ground, border or none), panel means a region of the screen frame (side panel, drawer, splitter pane), and the chart-panel role is renamed chart, shown in the register, roles and metas",
 "one block, Metric, replaces the stat card and the KPI tile, with the trend as an optional slot and the old slugs kept as aliases, shown by its meta, a render with and without the trend, and the aliases resolving",
 "the four nesting limits are written in, each driven red once: (1) a card never holds a layout, a holder or another record; (2) a tile holds exactly one thing and never sits directly in a tile (nest through a bento); (3) a carousel's slides all hold the same kind - these three REFUSE; (4) a card always has peers, a lone card being a tile - this one WARNS",
]
TITLE = ["(a) write the card/tile definitions and the five kinds into the register or roles ('holder' pending)",
         "(b) the 'accepts' containment check by kind, advisory first",
         "(c) container the umbrella word, surface a property, panel a screen region; chart-panel role renamed chart",
         "(d) Metric: the stat card and KPI tile merged, trend an optional slot, old names as aliases",
         "(e) the four nesting limits: three refuse, the lone-card rule warns"]
ops = []
for i in range(5):
    n = i + 1; c = calls[i]; lab = c["o"][c["r"]]
    ops.append({"op": "mint", "id": ROWS[i], "live": True, "owner": "claude",
        "title": f"#308 cards-and-tiles call {n} ruled - {TITLE[i]}", "home": f"{W}#> {n}. {c['t']}",
        "links": ["W-308o5", P, f'knowledge/_rulings.json#"id": "s308-D{38+n}"'], "closes_when": CW[i],
        "body": f"Minted #308 lane I round 5 under s308-D{38+n} — Dave, by click, pasted in chat #308 at 18:56 BST, verbatim: 'Chose: {lab} (the recommendation)', answering '{c['t']}' on {P}. His words: {W}."})
ops.append({"op": "mint", "id": "W-308iw", "live": True, "owner": "dave",
    "title": "#308 the three naming words: cell, holder/housing, container types",
    "home": f"{W}#> Page note: Do you think", "links": ["W-308ir", "W-308it", P],
    "closes_when": "his words are saved and inscribed",
    "body": "Minted #308 lane I round 5 on his page note on the cards-and-tiles page (18:56 BST), which is NOT a ruling: three naming questions. His one-word answers are owed; W-308ir keeps the kind 'holder' as a pending placeholder until they come."})
PARA = (f"#308 I round 5 (2026-09-29) — BY ADDITION, NOT A RULING: Dave's page note on the cards-and-tiles page, 18:56 BST, verbatim: \"{NOTE_PLAIN}\" "
        "(' / ' marks his line breaks). It asks three naming questions: reserving 'cell' for bento sub-elements rather than tile; the word 'holder' (he suggests 'housing'); and whether Apollo needs container types such as section, division, sector and panel. "
        "The conductor answered in chat, as recommendations, not rulings: cell = the grid position only, not a part; holder → housing recommended; section yes, as a landmark-mapped layout region; division and sector no; panel already defined (s308-D41). His one-word answers are owed on W-308iw.")
for rid in ("W-308iw", "W-308ir", "W-308it"):
    ops.append({"op": "note", "id": rid, "para": PARA})
ops.append({"op": "close", "id": "W-308o5", "closed_by":
    f"s308-D39..s308-D43 (#308, Dave by click 2026-09-29 18:56 BST, 5 of 5, all the recommendation): his export from the cards-and-tiles page is saved verbatim at {W} and inscribed. The builds are W-308ir..W-308iv; his page note's three naming questions are W-308iw, owed to him."})
json.dump({"session": 308, "by": "#308 I round 5 (2026-09-29)", "ops": ops}, open(f"{OUT}/rows5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entries), len(ops)); print(NOTE_PLAIN)
