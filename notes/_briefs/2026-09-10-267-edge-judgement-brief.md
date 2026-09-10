# #267 lane E brief — THE 78 PROPOSED RULING EDGES: a judgement pass so Dave can accept in tiers

**Model: Fable (Dave's word: "im going to lean on you judgement for some of these, go to town"). Conductor: Fable (#267). This lane RECOMMENDS; nothing is applied, ruled or inscribed. Dave's question, verbatim: "how safe is it for me to accept all the rulings, or can you make some recommendations… its a lot to go through."**

## WHAT THE 78 ARE

`knowledge/_build_kg_explorer.py:181-193`: for every ruling `r` in `knowledge/_rulings.json`, every ruling id mentioned in `r.says` becomes a derived `mentions` edge r → t. If a VERB STEM (`VERB_STEMS`, `:78-81`: supersed / retir / narrow / refin / correct / enact / extend / bound / confirm / overrid) occurs within **±80 characters** of the mention, the FIRST stem in dict order that matches is recorded as `proposedType`. 78 of 284 mentions carry one. They are published, unapplied, on `notes/_PROPOSED-266-ruling-edges.html` (lane V, #266: one card per edge, Accept / Reword / Reject).

⚠ The generator is crude by design: dict-order first match, stem match (`confirm` hits "confirmed", "confirmation"; `bound` hits "boundary"; `extend` hits "extended"), a ±80 window that may belong to a DIFFERENT mention in the same sentence, and no direction check (the verb may describe t acting on r, or a third ruling). So "accept all" means ratifying a regex's guesses as facts in a governance graph. Your job is to say, edge by edge, whether the guess is right.

## THE JOB

1. **Extract the 78 structurally** — import `extract_extra` / reuse the mention loop from `_build_kg_explorer.py` (read-only) or replicate it exactly; do not scrape the HTML. For each: source id, target id, proposedType, the ±80 window, the full `says` of the source, and the `ruled` + `date` of BOTH rulings.
2. **Judge each one.** Read both rulings. Decide:
   - **ACCEPT** — the verb is the true relation, in that direction, between those two rulings.
   - **RETYPE → <type>** — a real relation exists but the verb is wrong (name the right one from the ten, or `mentions` if it is only a citation).
   - **REVERSE** — the relation is real but t → r.
   - **REJECT** — the window's verb belongs to something else; keep as plain `mentions`.
   - **DAVE** — you cannot decide without him; say exactly what the question is in one sentence.
   Each verdict carries: confidence (high / medium / low), the quoted phrase that earned it (≤ 20 words), and one line of reasoning. Test yourself: for every ACCEPT, would a mutation of the verb (e.g. supersedes ↔ extends) be detectably wrong from the quoted phrase? If not, it is medium at best.
3. **Cross-checks that are cheap and decisive:** date order (a ruling cannot supersede/retire/correct one ruled LATER — flag any); self-consistency (if A supersedes B and elsewhere B extends A, one is wrong); the status field of the target (a `superseded`/`retired` status in the store corroborates; its absence does not refute); duplicates (same pair, two verbs).
4. **Tiers for Dave:**
   - **Tier 1 — accept in bulk**: high-confidence ACCEPT/REJECT/RETYPE where the phrase is unambiguous. State the count and the risk of bulk-accepting the tier in one honest sentence.
   - **Tier 2 — accept with my retype/reverse**: medium confidence; he can skim.
   - **Tier 3 — his**: the DAVE items and anything where the two rulings conflict. Keep this SHORT — the point of the pass is that he reads only these.
   Answer his question directly at the top of the page: **how safe is "accept all"?** — with the number that would be wrong if he did.
5. **Deliverables:**
   - `reviews/EDGE-JUDGEMENT-267-2026-09-10-v1.html` — swiss-design-system idiom (`.claude/skills/swiss-design-system`), self-contained, light/dark via `prefers-color-scheme` (TWO-RED LAW: `#DA1A00` on white, `#F6604C` on dark). Top: the answer + the three tier counts + the top-5 with weight. Then Tier 3 in full, Tier 2 as compact rows, Tier 1 as a compact table (source → target, proposed, verdict, phrase). Every row links to nothing external; ids are text.
   - `notes/_lanes/267/E/edge-recs.json` — machine-readable: `[{s, t, proposed, verdict, type, confidence, phrase, tier, reason}]` for all 78, so the conductor can apply his tiered word with one script.
   - `notes/_lanes/2026-09-10-267-E-edge-judgement.md` — done / NOT done / counts / tokens (ESTIMATED) / the generator defects you found, as findings with line numbers (not fixed here).
6. Commit the three files, one commit, `during #267 2026-09-10 — #267 E: …`. No push.

## RULES
- ⛔ Do NOT read _CHAIN.md, GOOD-MORNING.md, _LIVE-STATE.md, _CARRIES.md. No edits to `_rulings.json`, `_build_kg_explorer.py`, or anything under `knowledge/` except reading. No `_build_all.py`, `gen_kg_edges.py`, `git stash`; never delete `.git/index.lock`.
- ⛔ RULE NOTHING. A recommendation is worded as one. Where a ruling's text is Dave's, quote it, never paraphrase it into something stronger.
- Claims carry a probeable token (ruling id, quoted phrase, date).
- Return under 350 words: the answer to "how safe is accept all" with the number · tier counts · the Tier 3 list (id pairs + one-line question each) · top-3 generator defects · paths · commit sha · tokens.
