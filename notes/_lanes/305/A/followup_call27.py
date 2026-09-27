# #305 lane A follow-up — s305-D57 (call 27), five evidence amends, CALL-MAP call 27. Entry/amend files only; the
# writes themselves go through knowledge/_inscribe_ruling.py (run by the shell step after this).
import json, sys
sys.path.insert(0, 'knowledge')
import _governs as g
EX27 = 'notes/_lanes/305/DAVE-RULINGS-2026-09-27-call-27.md'
EX = 'notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md'
PAGE27 = 'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html'
PAGE = 'notes/_SITTING-304-tuesday-2026-09-29-v1.html'
V1 = 'notes/_subreports/2026-09-27-305-V1-verifier-wave-one.md'
SK = 'apollo-spider/skills/generate-from-canon/SKILL.md'
e = {
 "id": "s305-D57", "date": "2026-09-27", "by": "Dave",
 "status": ("ENACTED #305 2026-09-27 — RATIFIES WHAT IS ALREADY IN THE TREE at commit 4be130e5: both halves were built by "
            "#304 Run 4's skill lane (R4a) into apollo-spider/skills/generate-from-canon/SKILL.md in #304 wave two — rule 3a "
            "(the page arranges parts and never resizes them; width named with font-size, height, min-height, padding, zoom "
            "and transform) and procedure step 1 (seed: ask the graph through the reader, knowledge/_compose_slice.py, before "
            "any markup). Both read the same at HEAD. The wave's one new red, [121], was the chain's step-count figure and "
            "went green at 86249459; it is not the skill's. The skill ships to designers at the v1.0.14 cut (`s305-D2`). "
            "Stamped at inscription by lane A of #305 (a call that ratifies something already built carries the building "
            "commit as its proof, `s295-D2`'s sha discipline)."),
 "ruled": ("THE TWO THINGS THE SKILL LANE WIDENED ARE RATIFIED, BOTH HALVES OF SITTING CALL 27 AS ONE RULING: (A) THE PAGE NEVER "
           "SIZES A PART, WIDTH INCLUDED — a page's own style may place a part (which tile, which span, which order) and nothing "
           "else, and width is named alongside height and type; (B) THE READER IS THE SKILL'S FIRST STEP — after the brief and the "
           "theme question, the skill's first building step asks the graph (the reader) and writes down which part answers which "
           "question, and why, before any markup. Dave's answers, verbatim: half A \"yes\"; half B \"yes\" — the review page's "
           "recommendation on both. At the sitting (14:24 BST) call 27 carried only his comment, verbatim: \"I need to visuals for "
           "this\"; the visuals page was built for it and he ruled from it at 16:04 and 16:05 BST. ⚠ HALF A IS THE ONE WIDENING THAT "
           "WAS CLAUDE'S, NOT HIS, UNTIL NOW: `s305-D24` (call 23, the part drawn at its own reference size) did not name width, "
           "and the #304 wave-two verifier flagged the width ban as broader than any ruling; this ruling is his word on it. "
           "⬛ THE COST THE PAGE NAMED, AND WHERE IT IS PAID: the same rule stops a page stretching the app shell, so the fix goes "
           "in the part, not the page — the shell's full-height form, which is `s305-D12` (call 11), not this ruling. Half B is his "
           "#232 idea built (\"surely the KG is the brain and some of this could be offloaded from the skill\", as the page quotes it); "
           "the page's honest limit stands beside it: by eye the pages score the same (10.0 against 10.0) — the reader changes where "
           "the parts come from, it does not fix the parts. `s305-D24` is not edited."),
 "says": ("review page #305 'Call 27, in pictures' (notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html), exported 16:05 BST, "
          "received in chat 16:06 BST; half A (Ratify \"the page never sizes a part\", with width included?) saved 16:04 BST — "
          "decision, verbatim: \"yes\" · half B (Ratify \"the reader is the skill's first step\"?) saved 16:05 BST — decision, "
          "verbatim: \"yes\" · earlier, the sitting page #304 call 27 saved 14:24 BST — comment, verbatim: \"I need to visuals for this\""),
 "governs": [SK, "knowledge/_validate_own_size.py", "knowledge/_compose_slice.py"],
 "evidence": [
   EX27 + "#Call 27 · half A · Ratify",
   EX27 + "#Call 27 · half B · Ratify",
   PAGE27,
   EX + "#27 · Two things the skill lane widened",
   PAGE,
   "notes/_subreports/2026-09-26-304-R4a-skill-composes.md",
   "notes/_subreports/2026-09-27-304-V2-verifier-wave-two.md",
   SK,
   "commit 4be130e5 - rule 3a (width named) and step 1 (the reader first) built into the skill by R4a in #304 wave two; `s305-D57` ratifies them, the commit is the proof (`s295-D2`: the sha is the pointer)",
 ],
}
json.dump(e, open('notes/_lanes/305/A/entries/s305-D57.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for ev in e['evidence']:
    if g.evidence_form(ev) == 'anchor':
        ln, err = g.resolve_anchor(ev); assert not err, err

store = {r['id']: r for r in json.load(open('knowledge/_rulings.json'))['rulings']}
adds = {
 's305-D13': [
   "knowledge/snippets/Navigations.reference.html - the 7px badge this ruling moves is `.nv-count`, carried by Navigations, Sidebar-nav and Tab-bar, NOT by Badge (Badge carries no `nv-count`); the governs list names badge.meta.json and Badge.reference.html by mistake and cannot be edited from the sanctioned writer, so the real homes are pointed at here (#305 V1 verifier)",
   "knowledge/snippets/Sidebar-nav.reference.html - `.nv-count`, the badge moved 7px to 8px under this ruling",
   "knowledge/snippets/Tab-bar.reference.html - `.nv-count`, the badge moved 7px to 8px under this ruling",
   V1 + " - the mis-address found: the badge is `.nv-count` in Navigations, Sidebar-nav and Tab-bar, 0 hits in Badge",
 ],
 's305-D26': [
   "knowledge/gen_kg_sources.py - the generator that lands step 5's four edge types (setIn, behaviourFrom, capturedFrom, acceptsCapability); named here because the governs list cannot be edited from the sanctioned writer (#305 V1 verifier, at B2's request)",
   "knowledge/_source_nodes.json - the nodes and edges gen_kg_sources.py writes for step 5",
 ],
 's305-D9': [
   V1 + " - finding F2, and a correction of READING, not of his words: his \"yes\" took the page's recommendation, which is the tile hugs the drawing plus a when-rule that hands a donut or pie a half-width column (a narrow column by rule). NO LEGEND PLACEMENT IS BUILT OR DECIDED BY THIS RULING. The headline's \"the legend under the ring\" describes the page's render-only mock B; it is not a build instruction and nothing may be built from it without his word",
 ],
 's305-D25': [
   V1 + " - finding F3: the page put this as a PROPOSED rule and left its wording to Dave (\"the wording is yours\"). The wording now in the three metas' `when` fields (modals, split-button, dropdown) is R4a's draft, carried in by lane B2, and it AWAITS HIS WORD; it is not his wording and must not be read as settled",
 ],
 's305-D11': [
   V1 + " - finding F1: this ruling is scoped to COMMON's muted labels, as his call was worded (\"The muted labels in Common\"). It decides nothing for mono, console or supercharge; the #305 conductor has asked lane B1 to keep those three themes as they were. A real secondary-ink token for them, if he wants one, is his (`s145-D1`)",
 ],
}
out = {}
for rid, new in adds.items():
    out[rid] = store[rid]['evidence'] + new
    json.dump(out[rid], open(f'notes/_lanes/305/A/entries/amend-{rid}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# path-token hygiene: every '/' token in the new lines must exist (the _governs selftest reads them this way)
import os
for rid, new in adds.items():
    for ln in new:
        for t in g.PATHISH_RE.findall(ln):
            t = t.rstrip('.')
            assert os.path.exists(t), (rid, t)
print('ok')
