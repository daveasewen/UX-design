# REPORT — #273 lane LC: LIST vs CARD (P-272-1, pulled forward by s273-D3)

**Output page:** `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html`
**Nothing enacted.** No meta, `roles.json`, `when-fields.json`, `_parked.json`, gate or commit was touched. No ruling made — P-272-1's owner is Dave.

## The finding, five lines

1. **No system in the record draws the list/card line on field count or on columns-inside-a-row.** Thirteen systems consulted; zero use arithmetic on a record's contents.
2. **Three predicates actually appear:** the record's own bordered, self-contained **surface** (NN/g, USWDS, Ant, Carbon tile, M3); **record-level actions + a title** (GOV.UK summary card, M3, Ant); and **same-shape vs different-shape records in the SET** (NN/g — homogeneous records belong in a list because a list is scannable).
3. **Dave's "column-list" is a LIST in both systems that ship it.** IBM Carbon's structured list has column headers and explicitly allows stacking; GOV.UK's summary list is unbounded key/value rows. Carbon's exit from a list is *nesting*, and it exits to a **data table**, never to a card. So "columns within a list ⇒ card" is contradicted, not supported.
4. **Dave's "list-card" is real and has one exact precedent:** GOV.UK's **summary card** — "Summary cards are a variant within this component" — stacked without limit, gated on a repeated same-type record needing its own title and its own actions. Not on size.
5. **The 3×2 threshold has zero external support.** The only numbers found in thirteen systems are USWDS's 6 items per *collection*, Polaris's 50 before pagination, Carbon's 3 paragraphs per row — all measure the SET or the TEXT. Also: media does **not** promote a row to a card (Polaris resource items carry avatar/thumbnail *and* shortcut actions and stay list items).

**Our library:** `record-list`'s 8 providers all carry a `roles.json` `when` and are all **silent on their metas**. A 5-field-plus-status stacked row fits **nowhere** today — `list-items` refuses it (≤ 3 fields), `table`/`data-grid` only by flattening the stack, the three `-row` providers are kind-gated, `timeline` needs time, `tree` needs nesting. Our ingested `knowledge/guidelines/` are **SILENT** on the line (three "card" hits, all elevation/padding in `web-foundations.md`).

**One correction to the brief's premise:** `cards` is **not** `$not-a-provider`. It provides **`arrangement`**, `when` = "a bordered surface per item". Only `account-card` is in the `$not-a-provider` line. This is stated on the page.

## Proposal (all options open, recommendation marked as the lane's)

- **LC-1 the line** — recommends (a) `surface = bordered AND actions >= 1` ⇒ CARD, at any field count. Options (b) Dave's threshold as written, (c) both ANDed, (d) NN/g heterogeneity.
- **LC-2 the shapes** — recommends (a) one meta, three variants on `list-items` (GOV.UK's own construction). (b) three metas, (c) two metas.
- **LC-3 account-card** — recommends (a) stays `$not-a-provider`, the stacking is the list-card variant. (b) joins `record-list` kind-gated, (c) stays + a `with` edge.
- **LC-4 the cardinality numbers** — recommends (a) none as a gate; the comparison test, numbers as prose.

### `when`-field names LC-1 needs (the RD-3 question, still open)
- **Already legal:** `surface`. `rows` is legal but means "how many rows the reading carries" — the rows of a LIST, not the rows inside one record; (b)/(c) would re-read it or need a second name.
- **NOT legal, and needed:** `fields` (datapoints per record) · `columns` (columns within one record) · `actions` (independent actions the record owns). Option (a) needs only `actions` — the cheapest of the three.

## Gates — verbatim

**1. Quote gate.**
- `knowledge/_quote_gate.py`: `QUOTE-GATE ADVISORY — 0 verbatim · 2 not in the record`. **Known index limitation, not a miss** — the Memento index covers neither lane files nor decision-sheet `notes` (recorded at #272: "quote gate 0/13 on his notes"). Dave's four notes live in `notes/_lanes/272/harvest-decisions-2026-09-14.json`, which the index does not carry.
- Byte-exact check against that file instead (`_quotecheck.py`, exit 0):
```
quoted spans found on page: 45
Dave spans: 9  external spans: 32  over-length external: 0
blockquote B-10            verbatim-exact: True
blockquote B-20            verbatim-exact: True
blockquote B-09            verbatim-exact: True
blockquote N-account-card  verbatim-exact: True
```
Every Dave span on the page is a verbatim substring of one of the four notes, spelling kept; the four blockquotes are byte-exact against source; every external quote is under 15 words and carries a receipt.

**2. Screenshots** (`_shots.py`, after the `code{overflow-wrap}` fix):
```
shot-1280-light.png scrollWidth 1280 viewport 1280 no body overflow | console errors: 0
shot-1280-dark.png  scrollWidth 1280 viewport 1280 no body overflow | console errors: 0
shot-400-light.png  scrollWidth 400  viewport 400  no body overflow | console errors: 0
```
Looked at, cropped per section. Light 1280 and 400 read; dark carries `#F6604C` (two-red law s151-D1). The three wireframes render as intended. The only wide element at 400 is the sources table, inside its own `overflow-x:auto`.

**3. Drive** (`_drive.py`): `GATE 3 GREEN — all checks pass`
- 4 radio groups `LC-1..LC-4`, 17 inputs, every one named and labelled, no stray group.
- Export shape exact: `{page, at, decisions:[{id, choice, note}]}`, ids in order, values as driven.
- After reload: `{'a': True, 'c': True, 'b': True, 'n1': 'driver note one', 'n3': 'driver note three', 'said': '3 of 4 decided · saved 12:41'}`
- Clear leaves 0 radios checked. **console errors: 0.**

**4. This file.**

## First obstacle
One, found and fixed: the first screenshot pass reported `HORIZONTAL OVERFLOW` at both 1280 (1364px) and 400 (896px). Cause was a long `raw.githubusercontent.com` URL inside an inline `<code>`, which has no wrapping by default. Fixed by adding `overflow-wrap:anywhere;word-break:break-word` to `code`; re-shot green. Nothing else failed.

Secondary, recorded not fixed: `m3.material.io/components/cards/guidelines` is still client-rendered (as the #271 harvest recorded). The one Material 3 line quoted comes from the page's **server-rendered meta description** and is labelled as such on the page, not passed off as body prose. Apple HIG, Atlassian and Fluent 2 remain unreachable from the #271 refused list and were not re-probed within budget — recorded as unreachable, never inferred.

## Files this lane wrote
`notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html` · `notes/_lanes/273/list-vs-card/{REPORT.md,_shots.py,_drive.py,_quotecheck.py,shot-1280-light.png,shot-1280-dark.png,shot-400-light.png}`
