"""#308 lane I round 4 - close W-308ih/ik/im as superseded by s308-D26/D27/D28 and re-mint each
(W-308io/ip/iq) with a closes_when that matches the ruling as it now stands."""
import json
W2 = "notes/_lanes/308/DAVE-RULINGS-2026-09-29-1213-edge-definitions-v2.md"
V2 = "notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v2.html"
A = {4: "4. Say each type’s shape, and move the 22 self-lines to the fields they mean Changed in v2 — Take it",
     7: "7. Keep Apollo’s words and write the outside term beside them Changed in v2 — Take it",
     9: "9. Five edges the outside world has and Apollo lacks Changed in v2 — Take it"}
R = lambda d: f'knowledge/_rulings.json#"id": "s308-D{d}"'
SETS = [
 ("W-308ih", "W-308io", 26, 4, "s308-D19",
  "#308 edge-definitions item 4 (v2, re-minted) - (d) each type's shape in the register; the 22 self-lines moved, the four part-names to a subcomponent kind",
  "each type's register row records its shape (may it point at itself; may it loop; does it point both ways; does it chain), and the 22 self-lines are moved: the 7 one-on-screen lines to a count on the component, the 9 family lines to a field, the 4 part-names to a subcomponent kind (as in Canonical's ontology, with a flag for 'can stand alone'), and the carousel and cards containment loop shown to Dave and ruled by him"),
 ("W-308ik", "W-308ip", 27, 7, "s308-D22",
  "#308 edge-definitions item 7 (v2, re-minted) - the neatest name per edge type; the outside term adopted outright where neatest; graded column where a mapping is still needed; Open UI names",
  "each edge type carries its neatest name - the established outside term adopted directly where that is neatest, preferred over Apollo's word with a parallel mapping - and where a mapping is still needed the register's nearest-outside-term column is graded exact, close or loose, pointing first at Canonical's ds:/dt: or Spectrum's vocabulary and otherwise at SKOS, Dublin Core or PROV; each component carries its Open UI name; nothing moves to RDF"),
 ("W-308im", "W-308iq", 28, 9, "s308-D24",
  "#308 edge-definitions item 9 (v2, re-minted) - (i) four of the five new edges, a-d, with (c) a theme node kind ((e) is W-308in)",
  "four edges exist in the register and the graph: (a) token to token alias, with a loop check; (b) provides capability, the other half of acceptsCapability; (c) a theme node kind, which 'default for a theme' points at; (d) component to ARIA role. The fifth, (e) replaced-by, closes on its own row, W-308in"),
]
ops = []
for old, new, d, n, v1, title, cw in SETS:
    ops.append({"op": "close", "id": old, "closed_by":
        f"superseded by s308-D{d} (#308, Dave 12:13 BST, v2 item {n} 'Take it'), which amends {v1}: this row's `closes_when` no longer matches the ruling as it now stands, so it is closed and re-minted as {new} with a `closes_when` that does (conductor's order, #308 lane I round 4). Nothing on this row was built or done; the work carries to {new} whole."})
    ops.append({"op": "mint", "id": new, "live": True, "owner": "claude", "title": title,
        "home": f"{W2}#{A[n]}", "links": [old, R(d), V2], "closes_when": cw,
        "body": f"Re-minted #308 lane I round 4 from {old}, which is closed as superseded by s308-D{d} (Dave, pasted in chat #308 at 12:13 BST, verbatim: '{A[n]}'" + (" — with his note" if n == 7 else "") + f"; extends {v1}). The `closes_when` above is the ruling as it now stands; {old}'s note carries the amendment's history. His words: {W2}."})
json.dump({"session": 308, "by": "#308 I round 4 (2026-09-29)", "ops": ops}, open("notes/_lanes/308/I/rows4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(ops))
