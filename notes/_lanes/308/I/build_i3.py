"""#308 lane I round 3 - his v2 answers (12:13 BST): three new rulings s308-D26..D28 for the
three 'Changed in v2' items; the six repeats recorded in one note; row notes; W-308in for (e);
and lane C's review page rows (W-308c1..c3). v2 item text is read from v2's HTML, never retyped."""
import json, re, html
W2 = "notes/_lanes/308/DAVE-RULINGS-2026-09-29-1213-edge-definitions-v2.md"
W1 = "notes/_lanes/308/DAVE-RULINGS-2026-09-29-0926-edge-definitions.md"
V2 = "notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v2.html"
REP = "notes/_subreports/2026-09-29-308-O-ontology-research.md"
OUT = "notes/_lanes/308/I"
def text(p):
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"<(style|script)\b.*?</\1>", "", t, flags=re.S); t = re.sub(r"<svg.*?</svg>", "", t, flags=re.S)
    t = re.sub(r"<(br|/p|/div|/li|/h\d|/tr|/section|/td|/th)[^>]*>", "\n", t); t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t); t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n+", "\n", t)
    return [l.strip() for l in t.split("\n")]
w = open(W2, encoding="utf-8").read()
assert "> Session 308 · edge definitions · answers (v2)\n" in w
ans = dict(re.findall(r"^> ([1-9])\. (.+)$", w, re.M)); assert len(ans) == 9
L = text(V2); s = L.index("Nine items. Take it, change it or leave it"); e = L.index("Copy my answers", s)
block = L[s + 2:e]
titles = {}
for n, line in ans.items():
    titles[n] = line.split(" — Take it")[0]
order = [titles[str(n)] for n in range(1, 10)]
def item(n):
    t = order[n - 1]; a = block.index(t); b = block.index(order[n]) if n < 9 else len(block)
    return " ".join(block[a + 1:b])
note7 = ans["7"].split(" — Take it — ", 1)[1]
assert note7.startswith("I don't mind about how we label things")
anchor = lambda n: f"{W2}#{n}. {titles[str(n)]} — Take it"
SAYS = (f"chat #308, Tue 2026-09-29 12:13 BST, his answers pasted as the v2 research page's 'Copy as text', saved verbatim as {W2} "
        f"(header 'Session 308 · edge definitions · answers (v2)', so the page answered is {V2}) · item {{n}}, verbatim: '{{line}}'")
P = {
 4: dict(d=26, ext="s308-D19", row="W-308ih",
    head="EDGE-DEFINITIONS ITEM 4, AS CHANGED IN v2, IS TAKEN: THE FOUR SELF-POINTING PART NAMES BECOME A SUBCOMPONENT KIND.",
    plain="This extends s308-D19 (v1's item 4, taken at 09:26 BST), which sent the four part-names to slot names or declared nulls and named v2's change as not ruled. With this answer v2's change is ruled: the four part-names become a subcomponent kind, as in Canonical's ontology, where a subcomponent carries a flag for 'can stand alone'. The rest of item 4 is unchanged from s308-D19.",
    record="W-308ih gains a dated note by addition: its `closes_when` clause 'the 4 part-names to slot names or declared nulls' is amended by this ruling to 'the 4 part-names to a subcomponent kind'."),
 7: dict(d=27, ext="s308-D22", row="W-308ik",
    head="EDGE-DEFINITIONS ITEM 7, AS CHANGED IN v2, IS TAKEN WITH HIS NOTE: FOR EDGE NAMES THE NEATEST SOLUTION WINS, AND ADOPTING THE OUTSIDE TERM OUTRIGHT IS ALLOWED AND PREFERRED OVER A PARALLEL MAPPING.",
    plain="This extends and amends s308-D22 (v1's item 7, 'keep Apollo's words and write the outside term beside them'). Read plainly, his note says three things. His preference for Anglo-Saxon words is a preference for naming PRODUCTS, not for edge labels. For edge names, do what is neatest, even where that changes his answer. And he dislikes a patch (a side mapping layered on top) more than he likes the plain words. So the builder picks the neatest form for each edge type. Where an established outside term is the neatest name, it is adopted directly as the edge's name, and that is preferred over keeping Apollo's word with a mapping column beside it. The page's own lines 'Do not adopt Canonical’s or anyone’s vocabulary outright' (v2) and 'Keep Apollo’s words' (v1) give way to his note for labels. v2's other parts of the item stand as taken: the outside-term column points first at a design-system vocabulary (Canonical’s ds: and dt:, or Spectrum’s) and otherwise at SKOS, Dublin Core or PROV, graded exact, close or loose, and each component's Open UI name is added. His note speaks to labels only, so 'do not move to RDF' is not changed by it.",
    record="W-308ik gains a dated note by addition: its `closes_when` clause 'nothing is renamed to owl:, skos: or dcterms: terms' is amended by this ruling. The neatest name wins per edge type, and adopting the outside term directly is allowed and preferred over a parallel mapping."),
 9: dict(d=28, ext="s308-D24", row="W-308im",
    head="EDGE-DEFINITIONS ITEM 9, AS CHANGED IN v2, IS TAKEN WHOLE: FIVE EDGES, ADDING (e) REPLACED-BY ON COMPONENTS AND TOKENS WITH THE VERSION IT HAPPENED IN; AND (c) IS A THEME NODE KIND.",
    plain="This extends s308-D24 (v1's item 9, four edges a–d, taken at 09:26 BST). s308-D24 named two v2 changes as not ruled: the fifth edge (e), and v2's lean on (c) to a theme node kind. v1 had left (c) as either a theme node kind or the theme as a qualifier on the edge, and s308-D24 left that pick to Dave. v2 carries that lean in its item text, and he took the item whole, 'Take it' with no letters named, so both are now ruled. (e) is a new edge: replaced-by on components and tokens, with the version it happened in. For (c), 'default for a theme' points at a theme node kind, not at a qualifier.",
    record="W-308im gains a dated note by addition: (c) is a theme node kind (its `closes_when` clause that brings the pick to Dave is answered by this ruling). A new live row, W-308in, carries (e) so it can close alone."),
}
entries = []
for n, p in P.items():
    line = ans[str(n)]
    v1id = p["ext"]
    ruled = (f"{p['head']} {p['plain']} Dave's answer, pasted in chat #308 at 12:13 BST, verbatim: '{n}. {line}' (the page's recommendation). "
             f"v2's item as written, verbatim: '{item(n)}'")
    if n == 7:
        ruled += f" His note on item 7, verbatim: \"{note7}\"."
    ruled += f" Extends {v1id}. RECORD: {p['record']} Nothing is built by this ruling."
    ev = [f"chat #308 2026-09-29 (live) - his 12:13 BST v2 answers; item {n} is quoted verbatim in `says`",
          anchor(n), f"{V2}#data-n=\"{n}\"", REP, f"{W1}#{n}. "]
    ent = {"id": f"s308-D{p['d']}", "date": "2026-09-29", "by": "Dave", "status": "ruled", "ruled": ruled,
           "says": SAYS.format(n=n, line=f"{n}. {line}") + f" · extends {v1id}",
           "governs": [p["row"]] + (["W-308in"] if n == 9 else []) + ["knowledge/_state.json"], "evidence": ev}
    entries.append(ent)
# the v1 words-file anchor must be unique: use the full v1 line
w1 = open(W1, encoding="utf-8").read()
for ent in entries:
    n = int(re.search(r"item (\d)", ent["evidence"][0]).group(1))
    full = re.search(rf"^> ({n}\. .+ — Take it)$", w1, re.M).group(1)
    ent["evidence"][4] = f"{W1}#{full}"
    json.dump(ent, open(f"{OUT}/entries3/{ent['id']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

ops = []
rep = "1–3, 5, 6 and 8"
ops.append({"op": "note", "id": "W-308ie", "para":
  f"#308 I round 3 (2026-09-29) — BY ADDITION, one note for the six repeated answers: at 12:13 BST Dave pasted the v2 page's answers ({W2}, header '(v2)'). Items {rep} are the same items as v1 and his answer is again 'Take it', verbatim: " +
  " · ".join(f"'{k}. {ans[str(k)]}'" for k in (1, 2, 3, 5, 6, 8)) +
  ". They repeat s308-D16, D17, D18, D20, D21 and D23; no new ruling is inscribed for them. Rows W-308ie, W-308if, W-308ig, W-308ii, W-308ij and W-308il are unchanged. The three 'Changed in v2' items are s308-D26 (item 4), s308-D27 (item 7) and s308-D28 (item 9)."})
ops.append({"op": "note", "id": "W-308ih", "para":
  "#308 I round 3 (2026-09-29) — BY ADDITION under s308-D26 (Dave, 12:13 BST, v2 item 4 'Take it'): the four self-pointing part names become a SUBCOMPONENT KIND (as in Canonical's ontology, where a subcomponent carries a flag for 'can stand alone'). `closes_when` above is AMENDED by s308-D26 in one clause: read 'the 4 part-names to slot names or declared nulls' as 'the 4 part-names to a subcomponent kind'. The rest of `closes_when` stands."})
ops.append({"op": "note", "id": "W-308ik", "para":
  f"#308 I round 3 (2026-09-29) — BY ADDITION under s308-D27 (Dave, 12:13 BST, v2 item 7 'Take it' with his note, verbatim: \"{note7}\"). THE NEATEST NAME WINS for each edge type. His Anglo-Saxon preference is for naming products, not edge labels, and he dislikes a patch (a side mapping) more than he likes the plain words. So adopting the established outside term directly as the edge's name is ALLOWED AND PREFERRED where it is neatest, over keeping Apollo's word with a parallel mapping. `closes_when` above is AMENDED by s308-D27: its clause 'nothing is renamed to owl:, skos: or dcterms: terms' no longer holds for labels. Read the whole as: each edge type carries its neatest name (the outside term adopted outright where that is neatest), with the nearest-outside-term column graded exact, close or loose where a mapping is still needed; the column points first at Canonical's ds:/dt: or Spectrum's vocabulary, else SKOS, Dublin Core or PROV; each component's Open UI name is added; nothing moves to RDF."})
ops.append({"op": "note", "id": "W-308im", "para":
  "#308 I round 3 (2026-09-29) — BY ADDITION under s308-D28 (Dave, 12:13 BST, v2 item 9 'Take it', taken whole): (c) IS A THEME NODE KIND. 'Default for a theme' points at a theme node, not at a qualifier on the edge. `closes_when`'s clause that brings the pick to Dave is ANSWERED by s308-D28. The fifth edge, (e) replaced-by on components and tokens, is its own row, W-308in, so that each can close alone."})
ops.append({"op": "mint", "id": "W-308in", "live": True, "owner": "claude",
  "title": "#308 edge-definitions item 9 (v2) taken - (e) replaced-by on components and tokens, with the version it happened in",
  "home": anchor(9), "links": ["W-308im", "W-308o3", V2, REP],
  "closes_when": "components and tokens carry a replaced-by edge that names the replacement and the version it happened in, defined in the edge register and drawn in the graph, shown by the register row and one real example",
  "body": f"Minted #308 lane I round 3 under s308-D28 — Dave, pasted in chat #308 at 12:13 BST, verbatim: '9. {ans['9']}', answering v2 of the edge-definitions research page ({V2}). v2's (e), verbatim: 'e) Replaced-by on components and tokens, with the version it happened in. Spectrum carries introduced, deprecatedIn, replacedBy and plannedRemoval on every entity, and the design-token format has $deprecated. Apollo has replacement only between rulings.' A row of its own so it can close apart from W-308im's four. His words: {W2}; lane O's report: {REP}."})
# JOB 2: lane C's review page
PAGE = "notes/_REVIEW-308-old-claim-tables-2026-09-29-v1.html"
CREP = "notes/_subreports/2026-09-29-308-C-claim-tables-page.md"
WD = "notes/_lanes/308/DAVE-WORDS-2026-09-29-1208.md"
ops.append({"op": "mint", "id": "W-308c1", "title": "#308 review page v1 - the old claim tables (nine stale rows in the #204 and #208 tables), lane C, for Dave to rule",
  "home": PAGE, "links": [CREP, WD], "body": f"Lane C's review page, built on Dave's 12:08 BST words, item 3, verbatim: 'I need to see this in a document to review properly' ({WD}). Committed by #308 lane I round 3."})
ops.append({"op": "mint", "id": "W-308c2", "title": "#308 FILED REPORT - lane C: the old claim tables review page (9 rows re-checked; renders 1440, 390, 390 dark)",
  "home": CREP, "links": [PAGE, WD], "body": "Lane C's filed report for the claim-tables review page. Committed by #308 lane I round 3."})
ops.append({"op": "mint", "id": "W-308c3", "live": True, "owner": "dave",
  "title": "#308 rule the old claim tables from the review page",
  "home": f"{WD}#3. I need to see this in a document to review properly", "links": [PAGE, CREP, "W-308c1"],
  "closes_when": "Dave's export from the page is saved and inscribed",
  "body": f"Minted #308 lane I round 3 on Dave's 12:08 BST words, item 3, verbatim: 'I need to see this in a document to review properly', answering the conductor's finding on the nine stale rows in the #204 and #208 claim tables ({WD}). The document is lane C's page {PAGE} (report {CREP}); its recommendation is (b), dated notes by addition on all nine, with the CI step kept advisory. Dave rules from the page; his export closes this row once inscribed."})
json.dump({"session": 308, "by": "#308 I round 3 (2026-09-29)", "ops": ops}, open(f"{OUT}/rows3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entries), "entries;", len(ops), "ops")
