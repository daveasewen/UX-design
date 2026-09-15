# LANE TO — BRIEF — tie off the loose ends: 17 WCAG criteria + the authored pass on four components
#276 · 2026-09-15 · P-274-2 + P-274-3/s275-D5 · written by the conductor · model: opus

## Dave's words, verbatim (source: the #276 chat, 2026-09-15)
- *"1. fix"* — on the two-seat hazard. Read back as "make it impossible"; the RULE (own-lane-only vs one-seat) is NOT ratified. Do not inscribe a ruling.
- *"2. push"* — done, `2740d3b..3b9d89b`.
- *"3. edit mode can wait until we do edit mode, park it has a tripwire. 19 missing WCAG criteria, I wasn't aware of this. rule→component authored the other way --- maybe we just tie off these loose ends first."*
- *"yes, and maybe flag any extra you think are applicable"* — on the four components (tags/chips · notifications · links · buttons) as the starter set.

## The job in one line
Mirror lanes RK (#274) / RP (#275): PROPOSE read-only, dry-run, selftest + mutants, a review page of ≤ 6 decisions, **NOTHING LANDED**. Dave's export ratifies; a land lane lands.

## Read first, in this order (all read-only)
1. `notes/_lanes/275/principles-kg/BRIEF.md` + `REPORT.md` — the shape of your report and page.
2. `knowledge/_parked.py --check` → P-274-2 and P-274-3 bodies (they are the spec).
3. `python3 -c "import json;[print(r['id'],r['ruled']) for r in json.load(open('knowledge/_rulings.json'))['rulings'] if r['id'] in ('s269-D5','s274-D12','s275-D4','s275-D5')]"` — adjust the top-level key if it is not `rulings`.
4. `knowledge/compliance/rules/wcag-2.5.7-dragging-movements.json` + `rule.schema.json` + `README.md` — the corpus shape and provenance.
5. `knowledge/components/meta.schema.json` + `tags.meta.json` `notifications.meta.json` `links.meta.json` `button.meta.json` — the metas you will author against.
6. `knowledge/guidelines/_rules-index.json` — the 470 rules; the four `common-toolkit-*.md` files hold 14+15+17+23 = 69 of them (plus `common-toolkit-foundations.md` 4).

## PART A — the 17 missing WCAG success criteria (P-274-2)
1.2.3 · 1.2.4 · 1.3.3 · 1.4.2 · 1.4.5 · 1.4.8 · 2.4.13 · 2.5.1 · 2.5.2 · 2.5.3 · 3.1.1 · 3.1.2 · 3.1.4 · 3.2.2 · 3.2.4 · 3.3.7 · 3.3.8
- Source = the W3C "Understanding WCAG 2.2" page for each (`https://www.w3.org/WAI/WCAG22/Understanding/<slug>.html`), fetched with WebFetch. Title and Level come from the W3C page, never from memory. If a fetch fails, DECLARE it in the report and leave that rule's `title`/`level` marked `UNFETCHED` — never guess.
- Write 17 files into `notes/_lanes/276/tie-off/proposed-rules/` (NOT into `knowledge/compliance/rules/`) in the corpus's exact schema: `sc / title / level / severity / check / sources{wcag_url, en301549_clause, internal_policy_ref} / external_automatable_refs`. Validate each against `rule.schema.json`.
- `severity` is OUR grade, not the W3C's: propose one per rule with one sentence of reasoning, following the corpus's existing pattern (look at how A vs AA vs AAA map today).
- Mark 2.4.13, 3.3.7, 3.3.8 as WCAG 2.2 additions with the "pending EN 301 549 alignment" clause, exactly as 2.5.7 does. 2.4.13 is AAA — say so; propose whether an AAA criterion belongs in an AA-minimum corpus (this is a page decision, see D-2).
- Dry-run: with the 17 present, how many of the 19 `cites` nulls in `_rule_nodes.json` would resolve? Measure it (do not land; simulate the id lookup). Expect 19 → 0.

## PART B — the authored pass on four components (P-274-3 + s275-D5)
- Components: `tags` (+ `tags-input` if the chips spec covers it — say which), `notifications`, `links`, `button` (+ `icon-button`, `split-button` if the buttons spec covers them — say which).
- For each: the rules it OBEYS (from the matching `common-toolkit-*.md` rule ids in `_rules-index.json` — a filename join, NOT a regex over prose; P-274-3 records that regex gave false positives) and the A-grade LAWS it rests on (the six named in s269-D5; read the ruling for their ids). Authored means: you read the rule and the component and say why it binds, in one line each. Reviewed by eye.
- Propose ONE `meta.schema.json` diff adding the field(s). Name the field; do not invent two. Write the diff to `notes/_lanes/276/tie-off/meta.schema.diff` and the four proposed metas to `notes/_lanes/276/tie-off/proposed-metas/`. Do NOT touch `knowledge/components/`.
- **Flag extras (Dave's ask):** list further components where the binding is equally obvious — with the count of rules that would bind and WHY it is obvious (e.g. a guideline file that IS that component; a rule that names the component in its id). Ranked. Not authored, just flagged.

## PART C — the small fix (his "fix", advisory)
`knowledge/_validate_lane_ownership.py`: read this session's number from `_CHAIN.md` (`YOU ARE #(\d+)`), list staged paths (`git diff --cached --name-only`), and WARN on any path under `notes/_lanes/<M>/` where M ≠ N. ADVISORY by declaration (exit 0, print the offending paths); the blocking tier is Dave's. `--selftest` with a fixture. ≤ 60 lines. This one file MAY be written under `knowledge/` — it is the fix he asked for and it is inert.

## Review page — `REVIEW-tie-off-2026-09-15-v1.html`
≤ 6 decisions, recommendation first, (a)/(b) options, export button that writes JSON the way RP's page did (copy `_build_page.py` from lane 275 and adapt). Suggested:
- D-1 accept the 17 proposed severities as a batch (a) / review each (b)
- D-2 2.4.13 (AAA): include marked AAA (a) / exclude (b)
- D-3 the meta field name + shape (a = your proposal)
- D-4 the four authored metas land as proposed (a) / per-component review (b)
- D-5 the flagged extras: author in the NEXT lane (a) / park (b)
- D-6 lane-ownership guard: keep advisory (a) / make blocking (b)
Bake `type.css` into the srcdoc (label crop pattern, #261). Screenshot with chromium (`source knowledge/_render/seat_env.sh`).

## Gates before you report
`python3 knowledge/_validate_kg.py` (must stay OK — you landed nothing) · your own `--selftest` on the rule builder + `_mutate.py`-style mutants (≥ 10) · schema validation of all 17 · `git status` shows changes ONLY under `notes/_lanes/276/tie-off/` and `knowledge/_validate_lane_ownership.py`.

## Report — `notes/_lanes/276/tie-off/REPORT.md`
Measured, not narrated: counts, the fetch receipts (URL + HTTP status), the nulls-resolved figure, the flagged extras ranked, every gate's output line, FILL at close. Commit once at the end: `#276 2026-09-15 — lane TO: …` with `--stat` in the report. Never `git stash`. Never re-dump a JSON — textual span only if you must edit an existing file (you should not need to).
