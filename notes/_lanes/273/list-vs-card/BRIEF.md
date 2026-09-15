# BRIEF — #273 lane LC: LIST vs CARD — research the definitions (P-272-1, pulled forward by s273-D3)

Repo: `/sessions/elegant-determined-planck/mnt/UX-design` (bash) = `/Users/daviewen/Documents/Claude/Projects/UX-design` (file tools).
Lane folder: `notes/_lanes/273/list-vs-card/`. Output page: `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html`.

## Why this lane exists — Dave's words, verbatim (the question is HIS; you research, you do not define)
- B-10 (declined): *"This is more complicated than this suggests, we have list items that have 4 or five datapoints, but tehy are stacked in a couple of columns, I think we might have a few variants of list-items that complicate this a bit. I think we might have simple-list a column-list (2 row three column)  and a list-card as a way to define tihis further. lets discuss."*
- B-20 (declined): *"… we have list items that stack fields vertically, they may have four or five data items plus a status. now there is an argument around definitions here, maybe when we have columns within a list it's actually a card, we need to think about this. This is not a decision but maybe we allow three columns and two rows in a list and anything beyond that is a stacked card, I'm not sure right now, beras some research into these definitions."*
- B-09 (ratified with a note): *"this might clash with our redefinition of a card, maybe we have a list-card type that can be stacked in any amount, lets explore, see above"*
- N-account-card: *"I think that there is another rule here where account cards can stack like a list … I want to return to teh whole qustion of whan does a list item become a card or a hybrid list-card"*
Register entry: `python3 knowledge/_parked.py --list | grep -A6 P-272-1`. Ruling that pulls it forward: `s273-D3` in `knowledge/_rulings.json`. Why it matters now: `record-list`'s 8 providers cannot get their `when` gates (s273-D2) until list-items / cards have a definition.

## Read first
`knowledge/roles.json` → role `record-list` (8 providers + their `when` strings) · `knowledge/components/list-items.meta.json`, `cards.meta.json`, `account-card.meta.json`, `table.meta.json`, `data-grid.meta.json` (and any `*-row.meta.json` under record-list) · the harvest: `notes/_lanes/271/harvest/B/DECISION-TABLE.json` rows B-09, B-10, B-20 and `SOURCES.json` (13 systems, quotes < 15 words, every quote has a receipt) · `notes/_lanes/271/harvest/BRIEF.md` + `knowledge/_RUNBOOK-external-claims.md` for the citation method · `knowledge/guidelines/` for anything already ingested on lists / cards / summary-list.

## What to produce
1. **The definitions the 13 systems actually use** for list item · card · summary/description list · data table, and — the crux — where each draws the LINE between a list row and a card (field count? columns inside a row? presence of an image/media? a container boundary? actionability? stacking?). Quote < 15 words per system, receipt per quote, "silent" where silent. Use the harvested SOURCES first; fetch a system's live docs only when the harvest is silent, via `mcp__workspace__web_fetch`, and record the URL. No invented positions — a system that is silent is written as silent.
2. **Dave's three-shape hypothesis tested against them**: simple-list · column-list (his "2 row three column") · list-card ("stackable in any amount"), plus his threshold sketch "three columns and two rows in a list and anything beyond that is a stacked card". For each shape: which systems have an equivalent, under what name, and what gates it. Where the evidence contradicts the sketch, say so plainly.
3. **What OUR library already has**: the record-list providers and their roles.json `when`; `cards` and `account-card` (both `$not-a-provider` — say why, from roles.json) — and where the current metas would put a 5-field-plus-status stacked row today (probably nowhere — say so if so).
4. **A proposal for Dave, recommendation first**, as 2–4 numbered decisions with options (a/b/c), radios + a notes box each + Export JSON `{page, at, decisions:[{id, choice, note}]}` (copy the export / `focusout`+`beforeunload` flush pattern from `notes/_REVIEW-when-harvest-whole-library-2026-09-14-v2.html`). Likely decisions: LC-1 the line (what makes a row a card — a testable predicate in the closed `when` grammar if one exists, see `knowledge/when-fields.json`; if the predicate needs a field name not in the list, SAY WHICH — the field list is itself under review, RD-3); LC-2 the shapes (are simple-list / column-list / list-card three metas, three variants of one meta, or two metas); LC-3 account-card (does it stay `$not-a-provider` or join `record-list`). Every option stays open; the recommendation is marked as the lane's.
5. **Receipts** section + footer "Nothing on this page is a ruling."

## Design
Follow `/sessions/elegant-determined-planck/mnt/.claude/skills/swiss-design-system/SKILL.md`. One red `#DA1A00` on white (dark theme: `#F6604C` — the TWO-RED LAW s151-D1); dark via `prefers-color-scheme`; must read at 1280 and 400 (tables in `overflow-x:auto`). Self-contained, no CDN. Wireframe sketches of the three shapes are welcome as inline SVG (grey boxes, no product imagery).

## Gates before you report
1. Quote gate: every quoted sentence of Dave's on the page must be one of the four above, verbatim (spelling included — a spelling-corrected quote is still his words, but do not paraphrase and call it a quote). Every system quote < 15 words with a receipt (source file + row, or URL).
2. Screenshots 1280 light, 1280 dark, 400 light → lane folder (`source knowledge/_render/seat_env.sh`; playwright; the driving pattern is in `notes/_lanes/273/roles-drift/_shots.py` — copy it). LOOK at them (Read the PNGs, crop per section if tall).
3. Drive the page: every radio named, export shape exact, localStorage restore after reload, zero console errors.
4. `REPORT.md` in the lane folder: what you found (5 lines), the gates, the first obstacle if anything failed.

⛔ Write only inside the lane folder and the one output page. No commits. No edits to metas, roles.json, when-fields.json, _parked.json. Never `git stash`. Do not rule — Dave is P-272-1's owner.
