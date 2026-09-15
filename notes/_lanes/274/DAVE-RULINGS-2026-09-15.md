# DAVE — #274 — 2026-09-15 — verbatim, in order

Context: the four LC decisions on `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html` (P-272-1, s273-D3). Opener put the recommendation (a) on each.

- *"we have intersecting components here, so we have a simple-list-row, structured-list-row card-list-row - (this is basically the same as simple-list-row i guess, so we may not need the differentiation ). then we have simple-list, structured, card-list (the containers). I think that both simple and structured have optional headers, in banking these data in a structured list are obvious and often don't need headings. I think this makes sense to me. And I'm in two minds about the optional  headings in a card-list. does this change or help any on the decisions in _PROPOSAL-list-vs-card-2026-09-15-v1.html"*
  → Conductor's reading back: two levels — containers (simple-list, structured-list, card-list) and rows; card-list-row = simple-list-row; LC-1 becomes surface alone (actions clause struck); LC-2 (a) with the three variants being CONTAINERS; LC-3 (a); LC-4 (a); headers: list-level heading optional on all three, per-card title lives on the row.
- *"I think that actions might be allowable in a simple list in actuality"*
  → LC-1 closed: the line is surface alone; actions are a row property allowed in any container.
- *"okay i think you are right on 'headers on card lists' lets get this done"*
  → the header split accepted; inscribe + enact.

Inscribed as `s274-D1` (LC-1) · `s274-D2` (LC-2) · `s274-D3` (LC-3) · `s274-D4` (LC-4) · `s274-D5` (headers).
- On "who is the default for record-list" (options: 1 list-items default, table takes the comparison test · 2 table stays default): *"1"* → `s274-D6`.
- After s274-D6: *"note that in edit mode, when we build it, the user can be presented with the alternatives we have defined."* → a requirement on the composer's EDIT MODE, not a ruling on a mechanism: the resolver's runner-up providers (table, data-grid, the three containers, kind-gated rows) are the alternatives shown at edit time. Parked P-274-1.
- On "next is the presentation": *"sort of, is isn't part of the presentation, well it will be in the presentation when I show the explorer but this is just getting teh KG working harder we'll work on the demo/prez after we get this all sorted"* → the KG-gaps page is KG WORK (fill the gaps), not demo prep; demo/prez waits until the KG is sorted.
- Rules-into-graph export (`notes/_lanes/274/rules-kg/rules-kg-decisions-2026-09-15.json`, 14:14Z): RK-1 **a** · RK-2 **a** · RK-3 **null**, note: *"I need to understand this better, which is the more durable/scalable solution, and if we have both will this cause unneeded complexity? "* · RK-4 **a**, note: *"Can we have A and then C, surly the compliance fix isn't egregious??   "* · RK-5 **a**, note: *"I've gone with your recommendation with one caveat --- 'The generator writes knowledge/_rule_nodes.json — the shape of _ruling_edges.json (s267-D3). Nothing reads that file yet.' this concerns me should we be fixing this first rather than making a decision because nothing reads it, should we make sure that it is read? "* · RK-6 **a**, note: *"So A for now I guess and then D, is that correct?"*
- On the read-back (RK-1 a · RK-2 a · RK-3 a · RK-4 a then C as follow-up · RK-5 a · RK-6 a then D): *"go"* → `s274-D7..D12`.
