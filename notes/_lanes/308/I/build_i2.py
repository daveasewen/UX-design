"""#308 lane I round 2 - Dave's nine answers on the edge-definitions research (s308-D16..D24)
and the nine work rows (W-308ie..W-308im). Items are quoted from v1's HTML as written (he answered
v1: his copy header has no "(v2)" and item 9 reads "Four edges"); his lines from his words file."""
import json, re, html, os
WORDS = "notes/_lanes/308/DAVE-RULINGS-2026-09-29-0926-edge-definitions.md"
V1 = "notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v1.html"
V2 = "notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v2.html"
REP = "notes/_subreports/2026-09-29-308-O-ontology-research.md"
OUT = "notes/_lanes/308/I"

def text(p):
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"<(style|script)\b.*?</\1>", "", t, flags=re.S)
    t = re.sub(r"<svg.*?</svg>", "", t, flags=re.S)
    t = re.sub(r"<(br|/p|/div|/li|/h\d|/tr|/section|/td|/th)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t); t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n+", "\n", t)
    return [l.strip() for l in t.split("\n")]

w = open(WORDS, encoding="utf-8").read()
assert "Session 308 · edge definitions · answers\n" in w and "(v2)" not in w.split("> Session 308")[1].split("\n")[0]
lines = re.findall(r"^> ([1-9])\. (.+?) — Take it$", w, re.M)
assert len(lines) == 9, lines
L1 = text(V1)
start = L1.index("Nine items. Take it, change it or leave it")
end = L1.index("Copy my answers")
block = L1[start + 2:end]
titles = [t for _, t in lines]
items = []
for i, t in enumerate(titles):
    a = block.index(t); b = block.index(titles[i + 1]) if i < 8 else len(block)
    items.append(" ".join(block[a + 1:b]))
assert titles[8].startswith("Four edges")
L2 = text(V2)
def v2line(prefix):
    hits = [l for l in L2 if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits); return hits[0]
V2NOT = {
 4: "v2's change, not ruled; his: v2 sends the four part-names to a subcomponent kind instead, verbatim: '" + v2line("The 4 part-names become a subcomponent kind").replace(" Changed in v2", "") + "' He answered v1, which sends them to slot names or declared nulls.",
 7: "v2's change, not ruled; his: v2 points the outside-term column first at a design-system vocabulary and adds each component's Open UI name, verbatim: 'Point it first at a design-system vocabulary (Canonical’s ds: and dt:, or Spectrum’s) where one covers the type, and at SKOS, Dublin Core or PROV otherwise. Add each component’s Open UI name, the shared cross-system name.' He answered v1, which grades the nearest outside term without that order and adds no Open UI name.",
 9: "v2's change, not ruled; his: v2 adds a fifth edge, verbatim: '" + v2line("e) Replaced-by on components and tokens") + "' Also v2's lean on (c), not ruled; his: '" + v2line("c) A theme node kind") + "' He answered v1: four edges, and (c) is left as either a theme node kind or the theme as a qualifier on the edge.",
}
for k, s in V2NOT.items():
    pass
ROWS = ["ie", "if", "ig", "ih", "ii", "ij", "ik", "il", "im"]
anchor = lambda n: f"{WORDS}#{n}. {titles[n-1]} — Take it"
entries = []
for n in range(1, 10):
    rid = f"W-308{ROWS[n-1]}"
    ruled = (f"EDGE-DEFINITIONS ITEM {n} IS TAKEN: {titles[n-1].upper()}. Dave's answer, pasted in chat #308 at 09:26 BST, verbatim: "
             f"'{n}. {titles[n-1]} — Take it' (the page's recommendation; he took all nine). He answered v1 of the research page "
             f"(his copy header reads 'Session 308 · edge definitions · answers', without v2's '(v2)', and item 9 reads 'Four edges', v1's wording), "
             f"so the item is quoted from v1 as written, verbatim: '{items[n-1]}'")
    if n in V2NOT: ruled += " " + V2NOT[n]
    ruled += f" RECORD: a live work row, {rid}, owner claude, carries the build; nothing is built by this ruling."
    says = (f"chat #308, Tue 2026-09-29 09:26 BST, his answers pasted as the research page's 'Copy my answers' text, saved verbatim as {WORDS} "
            f"(that file's source line names v2; the copy header and item 9's wording are v1's, so the page answered is {V1}) · "
            f"item {n}, verbatim: '{n}. {titles[n-1]} — Take it'")
    ev = [f"chat #308 2026-09-29 (live) - his 09:26 BST answers; item {n} is quoted verbatim in `says`",
          anchor(n), V1 + "#recs", REP]
    if n in V2NOT: ev.append(V2 + "#recs")
    e = {"id": f"s308-D{15+n}", "date": "2026-09-29", "by": "Dave", "status": "ruled", "ruled": ruled, "says": says,
         "governs": [rid, "knowledge/_state.json"], "evidence": ev}
    json.dump(e, open(f"{OUT}/entries2/{e['id']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    entries.append(e)

CW = {
 1: "one register file defines every edge type once (every type in the graph; 65 at v1), one row per type with v1 item 1's fields as its columns (plain word, verb, starting kind, ending kind, opposite, shape, how many, reason rule, maker, nearest outside term), and the meta schema, the verbs map and the explorer read it instead of holding their own partial copies; the columns that rows W-308ig..W-308ik own may be filled by those rows",
 2: "a check reads the register and reports, by name, every edge whose start or end kind is not in its type's row, advisory first, wired into the build; and the 12 logo lines filed as governedBy that end on a rule are moved to obeys, governedBy kept for rulings only",
 3: "the register names each type's opposite and its stored side (governs over governedBy; containedBy over hasPart), the opposite is read by walking the graph backwards and never written as a second edge, and the one-off check of where the two sides disagree today (10 of 28 governedBy lines had no matching governs at v1) is run and filed before the switch",
 4: "each type's register row records its shape (may it point at itself; may it loop; does it point both ways; does it chain), and the 22 self-lines are moved: the 7 one-on-screen lines to a count on the component, the 9 family lines to a field, the 4 part-names to slot names or declared nulls, and the carousel and cards containment loop shown to Dave and ruled by him",
 5: "the reason field is named why everywhere, the register says per type whether it is required (required on obeys, restsOn, mustNotNeighbour, yieldsTo, groupsWith, composedOf, delegatesTo, drivesConsumer and governedBy; not on generated structure such as bindsToken, inGroup or usedInContext), the obeys 40-character floor is kept, and a check reports a required type without it",
 6: "every edge carries one maker field with three values - by hand (and whose), generated (and by which script), ratified (and by which ruling) - and the authored flag is retired",
 7: "the register carries a nearest-outside-term column graded exact, close or loose for every type; nothing is renamed to owl:, skos: or dcterms: terms and nothing moves to RDF",
 8: "each of the nine types of the older decision graph is mapped onto the ten in the ruling-edges file or retired, any with no match brought forward as a proposal (conflicts-with among them: 8 older lines use it), so one ruling-to-ruling vocabulary is read; 'depends on' is noted for later, not built",
 9: "the four edges exist in the register and the graph: (a) token to token alias, with a loop check; (b) provides capability, the other half of acceptsCapability; (c) something for 'default for a theme' to point at - a theme node kind or the theme as a qualifier on the edge, the pick brought to Dave with a recommendation; (d) component to ARIA role",
}
TITLE = {
 1: "(a) write the edge register: every edge type defined once",
 2: "(b) the ends check against the register, advisory first; the 12 logo lines moved to obeys",
 3: "(c) store one direction and read the other",
 4: "(d) each type's shape in the register; the 22 self-lines moved to the fields they mean",
 5: "(e) one why field, required by type",
 6: "(f) one maker field on every edge, replacing authored",
 7: "(g) the outside-term column, graded exact, close or loose",
 8: "(h) fold the two ruling-to-ruling vocabularies into one, with conflicts-with",
 9: "(i) the four new edges a-d",
}
ops = []
for n in range(1, 10):
    body = (f"Minted #308 lane I under s308-D{15+n} — Dave, pasted in chat #308 at 09:26 BST, verbatim: '{n}. {titles[n-1]} — Take it' "
            f"(he took all nine), answering v1 of the edge-definitions research page ({V1}). His words: {WORDS}; lane O's report: {REP}.")
    if n == 1:
        body += " A build lane (#308 lane E) is starting this row and W-308if in parallel and will close them against its own commits. The page left the file name to Dave ('perhaps knowledge/_edge_register.json, is yours to choose'); his 'Take it' does not name one, so the builder states the name it used."
    if n in V2NOT:
        body += " Not in this row: " + V2NOT[n].split(";")[0] + " (see the ruling); no row is minted for it."
    ops.append({"op": "mint", "id": f"W-308{ROWS[n-1]}", "live": True, "owner": "claude",
                "title": f"#308 edge-definitions item {n} taken - {TITLE[n]}", "home": anchor(n),
                "links": ["W-308o2", V1, REP], "closes_when": CW[n], "body": body})
json.dump({"session": 308, "by": "#308 I round 2 (2026-09-29)", "ops": ops}, open(f"{OUT}/rows2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entries), "entries;", len(ops), "ops")
