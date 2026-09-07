# HANDOFF #252 → #253 — FIRE THE 25-META LANES COLD (2026-09-07)

> ⚠ **NEWER than `_CHAIN.md`; OUTRANKS it** (same shape as `_HANDOFF-251`). Delete in the #253 wrap once
> its content is in the ⏱ delta and `_CARRIES.md`. `_HANDOFF-251-post-wrap-sitting.md` is discharged by
> the #252 wrap and deleted.

**Why it exists:** #252 adopted the roles list (`s252-D1`, `knowledge/roles.json`) and ran the premise
probe for the 25-meta pass, then hit the 150,929 advisory line (FILL 150,302 — the harness re-echoed
the 26 KB review page into context three times). The lanes are BRIEFED, not run. #253 fires them at the
opener with no re-thinking. Boot ≈ 70K; three lanes ≈ 19K conductor FILL each ⇒ fits with the wrap.

## Premise probe result (rule 7, done — do not redo)
- `knowledge/components/meta.schema.json` is `additionalProperties: false`; `^\$` keys pass; NINE scripts
  enforce it (`_validate_kg.py`, `_build_integrity.py`, `gen_component_partials.py`, …). ⇒ the eight terms
  MUST be added to the schema by addition (`s131-D2` shape) BEFORE lanes A/B write them, or every gate
  goes red on arrival. **Lane C does this first; A and B wait on C's schema commit.**
- No consumer of `provides/shape/span/…` exists anywhere (grep: only `_validate_descender_clip.py` matches
  the word "span", unrelated). The validator IS the first consumer — name it in every brief
  [[instrument-without-a-consumer]].
- `intent` already sits on 15 of the 25 (all 14 charts + one). **Call (strikeable):** the new field is
  `answers`; charts get `answers` = their `intent` value verbatim; the resolver asserts equality where
  both exist; NO rename of `intent` (its resolver `_validate_intent_resolve.py` stays).
- `roles.json` provider lists are MEMBERSHIP; priority/when there are illustrative. The metas become the
  source once authored; the validator then cross-checks roles.json against the metas.
- FILL at the stop line means: verifier in the SAME wave as each builder (#238), `--plant` at the opener,
  check-in inside any lane > 15K.

## The three lanes (Opus, `model: opus` — Fable bucket binds, #250)
**C — schema + validator (fires FIRST, alone).** Add to `meta.schema.json` `properties`, mirroring the
`intent` entry's style (description = ADDRESS into the store, resolver named, ADR-0017 write-once):
`provides` (string, address into `knowledge/roles.json` `roles`), `answers` (string|array, address into
`chart-intents.json` — extended by `s251-D11`; non-chart words such as `count-vs-threshold` are NEW keys
that lane A proposes and the page shows, never silently adds), `shape` (string, free for now — the
`data-shape` axis; the vocabulary is NOT ruled, list every value used on the review page), `span`
(`{cols:{min,max}}` in the 12-col canon `s251-D10`), `priority` (integer, in-role only), `when`
(string predicate, `s251-D5`; the field list on its right-hand side is NOT ruled — collect every field
used and put it on the page), `with` (array of `{slug, rel: recommends|suggests}` — lives on the ROLE
in roles.json, not on metas, `s251-D6`; schema entry only if a meta needs one), `not-with` (array of
`{slug, when}` — slug REQUIRED). Then write `knowledge/_validate_roles_resolve.py` on the
`_validate_intent_resolve.py` pattern: every `provides` resolves; every `not-with.slug` resolves to a meta
or a role; every `answers` resolves; `priority` unique within a role; DERIVE the reciprocals
(`instead-of` grades from FFF comparison, ISO 25964 rule, `s251-D6`) and PRINT them — never write them
into metas; `--selftest` with ≥4 bites; `--mutate` must bite (#244: probe `derived` first). Wire it into
whatever runs the other `_validate_*` (find the runner; do not invent a second one).
**A — the 11 `$composes` metas** (`template-dashboard-bento.meta.json` `$composes`: kpi-tile, stat-card,
chart-bar, summary, status-indicator, layout-utilities, breadcrumbs, headers, button, navigations,
app-shell-top-nav). Author `provides · answers · shape · span · priority · when` (+ `not-with` where the
page has one: kpi-tile ↛ status-surface) per `roles.json` membership, grounded in each meta's own
`purpose` prose. chart-bar is in A (it is a `$composes` slug) — B skips it. One review page
`reviews/META-TAGS-A-2026-09-NN-v1.html` (swiss, the ROLES page's shape: one section per meta, the six
values, the `when` predicate spelled out, a §"vocabulary this batch introduced" listing every new
`answers`/`shape` word and every `when` field, and a §Calls). Dave strikes by number.
**B — the 13 remaining charts.** Same, `answers` = `intent` verbatim; `provides: chart-panel` for all
but Chart-bullet (`headline-metric`) and chart-sparkline (`chart-panel` at 30 — see the ROLES page §03
note). Page `reviews/META-TAGS-B-…`.
**Verifiers:** one per builder, same wave, brief = "run `_validate_roles_resolve.py`, run the full gate
runner, read the review page's counts against the metas, report RED/GREEN with the probeable token".

## Wave order
1. Opener: `--plant --session 253`, check-in, re-title `Apollo - #253: 25-meta tags`.
2. Lane C → commit. 3. Lanes A + B + their verifiers in ONE wave → two pages → Dave. 4. Wrap.

## Owed at the #253 wrap
The three extension reminders (`roles-list-adopted-and-extensions-owed-252` memory; roles.json
`$extension`) go on the carry line verbatim — Dave: "so neither of us forgets".
