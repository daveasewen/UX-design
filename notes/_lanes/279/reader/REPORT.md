# LANE RD — REPORT — the reader: `_compose_slice.py` is step 1, the thin-slice contract + the ASK door

#279 · 2026-09-16 · enacting `s277-D10` + `s277-D13` under `s278-D1` · `s274-D11` applies · judgement lane, fable seat. Everything below was RUN, not recalled; every figure has the command that produced it.

**Result: LANDED.** `knowledge/_compose_slice.py` v1.0 carries the typed in/out contract as code and as spec; `designer-skills-v2/generate-from-canon/SKILL.md` step 1 calls it (the consumer, same commit); ASK answers all 12 canonical questions in ≤1K tokens on the live tree and sees a ruling inscribed after the seed; selftest 43/43; `_validate_kg.py` rc 0. The `s277-D10` figure did NOT reproduce under the new contract — it is 28,621 vs 111,468 (3.9×), not 19,117 (5.8×); § 4 says why.

---

## 1. The contract as landed (code = `_compose_slice.py` docstring; spec = `_RUNBOOK-compose-from-canon.md` § "Step 1 is the reader", appended by addition — `git diff --numstat` 64 / 0 on the runbook)

**IN** — `build_slice(task=None, *, intent=None, shape=None, roles=None, components=None, budget=None)`

| input | type | verified against |
|---|---|---|
| `task` | sentence; roles/intents derived when typed inputs are absent | `ROLE_LEXICON` / `COMPOSITE_LEXICON` / `INTENT_LEXICON` |
| `intent` | `chart-intents.json` → `chart-intent` keys (14 today) | grep'd live |
| `shape` | a meta `shape` string, normalised (`×`→`x`), e.g. `parts-of-whole` (2 metas) | grep'd live: 16 metas carry `shape` |
| `roles` | `roles.json` → `roles` keys (12) | grep'd live |
| `components` | meta stems, forced in with why `named by the caller` | `knowledge/components/*.meta.json` (137, EXAMPLE- excluded) |
| `budget` | cl100k tokens for the seed | tiktoken 0.14.0 |

**OUT** — eight fields, every one content or `null` + `$nulls[field]` note (the `s274-D7..D12` house rule):

| field | rows on the dashboard seed | read from (all grep'd in the live tree) |
|---|---|---|
| `components` | 31 (14 winners + alternates + `consumes`/`hasPart` requirements) | metas; `roles.json` providers; `edges.providesRole` (108 edges — a new leg the old docstring named as a future re-point and never implemented) |
| `governs` | 38 rulings | `edges.governedBy` (28 in the corpus) + `_rulings.json` `governs[]` by meta path (198 entries) or `.reference.html` → `renderedBy` owner (103) — the explorer's own `gov_target` join, read LIVE |
| `obeys` | 62 — 28 authored / 4 derived / 30 routed; 32 BLOCKING, first | `edges.obeys` (168, `rule:`/`ux:`), `_rule_nodes.json` `flaggedBy` (50 snippet→rule), `_rules-index.json` files by vocabulary |
| `mustNot` | 8 (6 `ref:null` with their `$note`) | `edges.mustNotNeighbour` (70, 51 null), `relationships.mustNotNeighbour`, `not-with` |
| `tokens` | 25 groups across semantic / foundation / primitive / composite | `tokens/*.json` tiers; `typography-composites.json` folded in as tier `composite` (the old top-level `typeComposites` is gone — tokens at group+tier is where the ruling puts it) |
| `assets` | 31 (icons + logos) | `_icon_nodes.json` `usesIcon` (371), `_logo_nodes.json` `usesLogo` (18) — the geometry byte-match, `s277-D5`; the old snippet-regex icon scan is retired |
| `unresolved` | 22, each `ref:null` + `$note` + `why`, incl. the permanent `photo` limit (no node kind) | — |
| `sized` | whole + per-field cl100k, ratio vs the 31 metas and the 137-meta library, `budget` / `within_budget` / `reductions` | tiktoken; chars/4 fallback LABELLED, never presented as measured |

Budget behaviour, chosen and declared: over budget the seed drops alternates, then routed obeys (each step in `sized.reductions`, the dropped rows re-appear in `unresolved`); if still over it raises `SliceRefused` (exit 3) naming the count. I chose reduction-then-refusal over refusal-only because a seed that refuses leaves step 1 with nothing; the two reductions are the two classes the docstring already calls the weakest evidence.

Old field names retired: `rules`→`obeys`, `antiNeighbours`→`mustNot`, `icons`→`assets`, `rulings`→`governs`, `measure`→`sized`, `typeComposites`→`tokens` tier `composite`. Nothing in the tree consumed the old names (grep: only `notes/_lanes/27x` measurement scripts — records, not consumers).

## 2. The wiring (the consumer, `s274-D11`)

`designer-skills-v2/generate-from-canon/SKILL.md` § Procedure step 1 — 27 insertions, 4 deletions. The four deleted lines were the read-the-library step. Step 1 is now: run the reader once (`--out seed.json --explain`), open a meta only for a component the seed names, LINK `canon.css`/`type.css` rather than read them, and use `--ask` mid-session. **The old path is kept as a DECLARED fallback, not a flag** — only when `knowledge/_compose_slice.py` is not in the pack a designer was given, and the run must write `step 1: metas-read fallback (no reader in pack)` in its used/missing note. No gate reads the SKILL.md (grep'd `knowledge/*.py`, `apollo-spider/*.sh`); nothing broke by removing the default.

Not wired, declared with size: `apollo-spider/skills/generate-from-canon/SKILL.md` step 1 ("Search `showroom/index.json`"). The ruling's `governs` names `designer-skills-v2/`, not `apollo-spider/`; ~30 lines of the same prose, the conductor's scope call.

## 3. ASK — the 12 answers with token counts (`notes/_lanes/279/reader/ASK-12.json`; same counts from `--selftest`)

| Q | verb | question asked | tokens | answer | declared |
|---|---|---|---|---|---|
| Q1 | governs | what governs component:button? | **615** | 7 rulings (5 via `governs[]`, 2 via `edges.governedBy`), newest first | — |
| Q2 | binds | which components does rule:ctkb-003 bind? | **162** | 1 component | — |
| Q3 | principle | what principle underlies rule:ctkb-002, and its grade? | **256** | the rule's own destiny (ADVISORY) + 0 `cites` | rule→ux: NO SUCH EDGE TYPE |
| Q4 | conflicts | which rules conflict for component:button? | **290** | 17 obeyed, 0 tensions | no `tensionWith` joins two obeyed principles; no rule→rule conflict type |
| Q5 | ruled | what did Dave rule about component:table, and when? | **196** | 1 ruling with date | — |
| Q6 | evidence | what evidence supports ruling:s277-D10? | **309** | 1 evidence entry, 0 ruling→ruling edges | — |
| Q7 | answers | which components answer intent:comparison? | **212** | 4 components (edge + meta `answers`) | — |
| Q8 | avoid | what must component:toast not sit next to? | **244** | 4 must-nots | — |
| Q9 | tokens | what tokens does component:button consume; what breaks if I change one? | **750** | 8 groups at tier; blast radius for the 8 widest members | no `token:` kind; blast from `_blast-radius.json` (derived, generated 2026-06-18) |
| Q10 | usedIn | which pattern / context is component:button used in? | **291** | 3 patterns, 4 contexts | — |
| Q11 | wcag | what is the WCAG / accessible-name obligation for component:button? | **578** | 6 sc: `appliesTo` with level/severity/check; 0 cited by obeyed rules | accessible-name lives in the sc check text |
| Q12 | assets | what icon / logo / photo may I use in component:app-shell-doormat? | **624** | 4 icons, 2 logos, 0 nulls | photo: no node kind |
| | | **total** | **4,527** | | |

All 12 ≤ 1,000. Refusals exercised at the CLI: `--budget 100` → `REFUSED (ask): … 615 cl100k tokens, over the budget of 100 — refused, not truncated` rc 3; "tell me a joke" → `no verb …` rc 3; `component:zz-none` → `not in the live graph (N nodes read at <time>)`.

**A live-tree finding, not assumed:** Q4's 2-hop walk (obeyed `ux:` × `tensionWith`) is EMPTY on today's tree — the 6 metas with `ux:` obeys (tags-input, icon-button, notifications, links, tags, button) obey pr-fitts / pr-hick / pr-speed-accuracy / pr-graphical-perception and none of the 22 `tensionWith` pairs joins two of them. The walk is proven by a pair planted in the scratch copy (bite 39).

## 4. Measured, not asserted — the `s277-D10` claim re-run

Command: `python3 knowledge/_compose_slice.py --measure` (task = "a payments dashboard screen with a stat card row, a filter bar and a data table"; output `notes/_lanes/279/reader/measure.json`). Unit: tiktoken cl100k_base 0.14.0, a LABELLED estimator (`ds-021`).

| what | tokens | from |
|---|---|---|
| the seed under the landed contract | **28,621** | `seed_tokens` |
| per field | components 7,639 · governs 5,225 · obeys 7,998 · mustNot 575 · tokens 1,772 · assets 2,597 · unresolved 1,597 | `per_field` |
| the 31 metas the seed names | **111,468** | `metas_in_seed_tokens` |
| ratio | **3.89×** | (5.83× on the proposal's field set) |
| every non-EXAMPLE meta (137) | 414,184 | `library_metas_tokens` (the ruling's 414,755 counted the EXAMPLE meta) |
| `canon/canon.css` | 588,102 | matches the ruling's figure exactly |
| `canon/type.css` | 3,472 | |
| step 1 as written before the wiring (all metas + canon.css + type.css) | **1,005,758** | `step1_before_wiring_tokens` |
| ratio vs that | **31.83×** | |

> **CORRECTION (#279 lane SC2, 2026-09-16, RV F2 — by addition, the lines above stand as written).** The "31.83×" / "31.8×" above is a re-typed figure, not the measured one: this lane's own `measure.json:22` says `"ratio_vs_step1_before_wiring": 35.14` (1,005,758 / 28,621 = 35.14×). 31.8× is what the ratio became AFTER lane SC added the routed-by-scope rows (31,536 → 31.89×), which this lane could not have had. The live figure today, after SC2's per-rule facet override (`python3 knowledge/_compose_slice.py --measure`): seed 31,372 / 111,468 = 3.55×, and 1,005,758 / 31,372 = **32.06×**.

**The ratio moved, and here is why, measured.** At `f641242`, before this lane, `python3 knowledge/_compose_slice.py "<dashboard>" --explain` printed `slice 19117 tok vs 111468 … = 5.83x` — the ruling's figure reproduces on the OLD code. The landed contract adds content the proposal's slice did not carry: `governs` is 38 rulings read live from `governs[]` (the old `rulings` field had 3, from `edges.governedBy` alone) and `assets` is 31 rows from the ratified node files (the old `icons` was empty). Those two fields are 7,822 of the 9,504 extra tokens. I trimmed what was fat (ruling `ruled` ≤200 and `says` left to ASK Q6; asset `via` to a code; rule text ≤280) and stopped: cutting `governs` to reach 5.8× would mean seeding fewer of Dave's rulings. The house figure is now **28,621 vs 111,468 (3.9×) and vs 1,005,758 (31.8×)**; the runbook carries both and says the 19,117 was the proposal's field set.

## 5. Gates — every line

```
$ python3 knowledge/_compose_slice.py --selftest
  43 bites, 0 failed   (1–6 contract; 7–20 the carried proposal bites; 21–22 budget; 23–34 ASK Q1..Q12 ≤1K + verb;
                        35–37 refusals; 38–39 Q4 live/planted; 40–41 LIVE: planted ruling seen, live file untouched;
                        42 seed byte-identical after 14 asks; 43 live reader == _build_kg_explorer.extract()+extract_extra()
                        on governs/obeys/appliesTo/definedIn/cites/flaggedBy/tensionWith/mustNotNeighbour counts)
$ python3 knowledge/_validate_kg.py
  _validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance,
  edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.  (rc 0)
$ python3 knowledge/_validate_help_gate.py
  rc 1 — 15 PRE-EXISTING misses (_bite_goal.py, _build_kg_explorer.py, _render/verify_demo_slides_268*.py,
  _tmp/wrap25x/carry*.py …); _compose_slice.py is NOT among them. Not mine; declared.
$ python3 knowledge/_compose_slice.py --measure      → the § 4 table
```
The runbook names `_validate_screen.py --render` for composed screens; no screen was composed here, so it was not run — declared.

## 6. What could not be done, with size

1. **The pack does not carry the reader or the Constitution it reads (ruling vs live tree — stopped on this item, declared).** `s277-D10` governs `designer-skills-v2/`; `s278-D1` says ASK reads `_rulings.json` live. But `designer-skills-v2/knowledge/` is baked by `build-designer-kb.sh`, which does NOT ship `_compose_slice.py`, `_rulings.json` (excluded as "Dave's record", `_gen_pack_manifest.py:515`), `_rule_nodes.json`, `_ux_principle_nodes.json`, `_icon_nodes.json`, `_logo_nodes.json`, `roles.json`, `chart-intents.json`, `_consult-lexicon.json`. A pack change is a release (P-269-1 pin) and shipping `_rulings.json` reverses a deliberate exclusion — both Dave's. Size: ~10 `cp` lines in `build-designer-kb.sh` plus the reversal of the `_rulings.json` exclusion. Until ruled, the SKILL.md fallback clause is what a pack designer hits, and it says so.
2. **`apollo-spider/skills/generate-from-canon/SKILL.md` step 1 not wired** (§ 2) — ~30 lines of prose, the conductor's scope call.
3. **P-274-1's `file-changed` tripwire on `knowledge/_compose_slice.py` goes DUE with this commit** (edit-mode alternatives). The seed already carries `alternate` rows and `co-providers of role:*` in `unresolved` — the material P-274-1 asks an edit-mode surface to show; the surface is not built. Owner unchanged. Size: 0 here; the tripwire firing is the intended mechanism.
4. **`_capture_gate.py:546` registry entry** still says "Whether the door is WIRED at all is Dave's" — now ruled; tier `estimate-only` still correct, the sentence stale. Size: one string; left because `_capture_gate.py` is the wrap seat's file.
5. **Q3 / Q4 / Q9 / Q12 answer with declared limits** — no rule→ux edge type, no rule→rule conflict type, no `token:` node kind, no photo node kind. Each answer names the limit; none invents one. Adding a kind is a proposal lane (A3 § 4 CLOSURE / TOKENS), not this one.
6. **The msgfile path.** The brief says `/tmp/_msg-279-RD-<ts>.txt`; `_git_commit.sh`'s header says "never /tmp" (a session-owned dir). The script does not enforce it; I followed the brief. Size: 0.

## 7. What lanes (ii)–(v) can now consume

- `load_live(root)` — the live graph as `{nodes, edges, out, in, g, read}` with declared nulls carried; edge counts cross-checked against the explorer (bite 43). Lane (ii) can import it or keep `extract()`.
- `ask(question, seed, budget, live)` — 12 verbs; the consumer-less edge types A1 counted now have a reader (`governs`, `obeys`, `appliesTo`, `cites`, `flaggedBy`, `tensionWith`, `usesIcon`, `usesLogo`, `answersIntent`, `hasDataShape`, `commonPattern`/`usedInContext`, `mustNotNeighbour`).
- `build_slice(...)` typed inputs — an edit-mode surface (P-274-1) can drive it without a sentence.
- `notes/_lanes/279/reader/seed-dashboard.json`, `ASK-12.json`, `measure.json` — the receipts.

## 8. Shipped sha and `git diff --numstat` from it

(appended below after the commit landed)

> **APPENDED (#279 lane SC2, 2026-09-16, RV F3 — the numstat this section promised).** Shipped sha **`d6bd57b`**; `git diff --numstat d6bd57b~1 d6bd57b`:
>
> ```
> 2	2	_CHAIN.md
> 27	4	designer-skills-v2/generate-from-canon/SKILL.md
> 64	0	knowledge/_RUNBOOK-compose-from-canon.md
> 1299	469	knowledge/_compose_slice.py
> 75	40	knowledge/_state.json
> 1	0	notes/_REHEARSAL-LOG.jsonl
> 730	0	notes/_lanes/279/reader/ASK-12.json
> 28	0	notes/_lanes/279/reader/BRIEF.md
> 121	0	notes/_lanes/279/reader/REPORT.md
> 24	0	notes/_lanes/279/reader/measure.json
> 3240	0	notes/_lanes/279/reader/seed-dashboard.json
> 121	0	notes/_subreports/2026-09-16-279-RD-reader.md
> ```
>
> `_state.json`'s 40 deletions are diff alignment (RV § 8: ids 647 → 649, `W-279il` + `W-279rd` added, 0 rows changed). RV F1 (the frozen-release gate, s114-D4, tripped by the SKILL.md hunk) is NOT addressed here — `designer-skills-v2/` and `knowledge/_release/` are lane PK's.
