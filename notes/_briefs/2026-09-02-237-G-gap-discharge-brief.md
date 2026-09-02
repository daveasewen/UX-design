# #237 — LANE G: DISCHARGE SEVEN DECLARED GAPS from the designer's-brain lanes (R1 · R2)

*Conductor: Fable, #237. Sub: Opus. Filed report, chat gets a stub (`s218-D7`). Session #237 is NOT this sub's to wrap or commit.*

## WHY THIS LANE EXISTS (Dave's words, #237 opener)

The plan `_PLAN-designers-brain-2026-09-02-v1.html` § "Eight declared gaps" lists R1-1 · R1-4 · R1-5 · R2-1 · R2-2 · R2-3 · R2-4 · R2-5. Dave, on each: **R1-1** *"try this: https://www.dialogdesign.dk/isos-dialogue-principles-2019/"* · **R1-4** *"1 fetch from a working EUR-Lex route: do it"* · **R1-5** *"browser-rendered fetch: do it"* · **R2-1** *"~12 fetches: do it"* · **R2-2** *"Dont worry about this, it was a youtube video… not worth the effort"* — ⛔ **DROPPED by Dave, do not chase it** · **R2-3** *"One `ls` — but outside that lane's fence: lets try it"* · **R2-4** *"Re-read ~3–4K, do it"* · **R2-5** *"~1.5K. do it."*

Seven gaps to discharge. Each either becomes **DISCHARGED** with a receipt, or **STAYS UNPROVEN** with the exact failure named. A declared gap passes; a silent one fails. A gap "closed" from memory is the defect this lane exists to refuse (ADR-0016).

## GROUND FIRST (~10 min, before any fetch)

1. `notes/_subreports/2026-09-02-236-R1-principles-survey.md` § UNPROVEN items **1, 4, 5** only (lines ~221–245) — the exact claims.
2. `notes/_subreports/2026-09-02-236-R2-sdlc-playbook.md` § UNPROVEN (lines ~401–418) — items 1, 3, 4, 5. Item 2 (the video) is DROPPED.
3. `notes/_subreports/assets/2026-09-02-236-R2-sdlc-playbook/fetch-receipts.json` — the academy/blog URLs R2 fetched; the other twelve lesson URLs derive from the same course index.
4. `notes/_subreports/_TEMPLATE.md` — the filing skeleton.

## THE DELIVERABLE — seven addenda + one report

Asset dir: `notes/_subreports/assets/2026-09-02-237-G-gap-discharge/`. One JSON per gap, plus `fetch-receipts.json` (every URL tried: route, HTTP status, bytes, UTC time, tool used). ⚠ Departure from the #236 handoff's suggested path (`…/2026-09-02-236-R1-principles-survey/iso-9241-110-addendum.json`): all addenda live in THIS lane's folder, so provenance is one lane, one folder; the plan's next version points here. Say so in the report.

| Gap | Do | Addendum file | Discharged means |
|---|---|---|---|
| **R1-1** ISO 9241-110 seven principle names | `mcp__workspace__web_fetch` https://www.dialogdesign.dk/isos-dialogue-principles-2019/ | `iso-9241-110-addendum.json` — seven names, each **in our words** + ≤ 15-word quoted receipt + URL + edition/year as the page states it | seven names present, each with its quote; note the page is a practitioner summary (Molich), not the standard |
| **R1-4** DSA Art. 25 from EUR-Lex itself | Regulation (EU) 2022/2065, CELEX `32022R2065`. Try in order, one per call, record each: `https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065` · `https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng` · the PDF route · then a browser-rendered fetch | `dsa-art25-eurlex.json` — Art. 25 paragraphs 1–3 **in our words** + one ≤ 15-word quote per paragraph + the route that worked; and a diff verdict against the mirror text R1 used (same / differs where) | text obtained from a `eur-lex.europa.eu` route, verdict stated |
| **R1-5** INP "good" threshold | web.dev/inp is JS-rendered: use **Claude in Chrome** (`mcp__claude-in-chrome__navigate` + `get_page_text`; load via ToolSearch in ONE call); if Chrome is offline, the built-in browser (`mcp__Claude_Browser__preview_start` + `get_page_text`). Page: https://web.dev/articles/inp (and the thresholds table) | `inp-threshold.json` — good / needs-improvement / poor boundaries in ms, the percentile the threshold is stated at, ≤ 15-word quote, URL, date seen | the 200 ms figure (or whatever the page states) read off the RENDERED page |
| **R2-1** the other twelve academy lessons match their blog sections | ~12 fetches, ONE PER CALL (sandbox kill wall ~178 s). For each lesson: fetch, compare MEANING to the blog section R2 mapped it to, verdict `equivalent` / `light copy-edit` / `DIVERGES (where, and which borrow-matrix cell it could move)` | `academy-lessons-parity.json` — per lesson: URL, blog section, verdict, one ≤ 15-word quote where it diverges | all twelve carry a verdict; any DIVERGES names the matrix cell at risk |
| **R2-3** no hook layer anywhere on this machine | One `ls` outside the repo fence — but ⚠ **your shell is a SANDBOX, `~` there is not Dave's home.** Probe BOTH and say which filesystem each is: (a) `Read`/`Glob` on `/Users/daviewen/.claude/settings.json`, `settings.local.json`, and `/Users/daviewen/.claude/hooks/` (Dave's Mac, via the file tools — may be refused: declare it); (b) `ls -a /sessions/dreamy-relaxed-noether/mnt/.claude/` (the mounted skills cache); (c) `ls -a .claude/` in the repo (R2's original probe, re-run). Grep any settings file found for `"hooks"` | `hooks-probe.json` — per path: reachable? exists? contains `hooks`? which filesystem | every path has a stated result; NONE is left as "not tried" |
| **R2-4** `apollo-spider/CLAUDE.md` + `AGENTS.md` play the rails-file role | Read both files in full | `rails-files-reread.json` — per file: size, what it instructs (our words), does it function as a rails file for a generating agent (yes / partly / no, with a ≤ 15-word quote), and whether R2's matrix row 4 stands | both read; row-4 verdict stated |
| **R2-5** does ADR-0017 cover briefs? | Read `docs/decisions/ADR-0017-write-once-live-facts.md` in full | `adr-0017-briefs.json` — the ADR's own class list (quoted ≤ 15 words), whether "brief" or `notes/_briefs/` appears (grep count), and the verdict: covers briefs explicitly / by implication / silent | verdict stated with the grep count; ⛔ do NOT recommend what Dave should rule — he already has |

## METHOD RULES

- **Our words + a short quote.** Every fact enters as OUR statement with a ≤ 15-word quoted receipt and URL. Never a paragraph of someone else's text. Never song-lyric-length copying of a standard.
- **A failed fetch stays UNPROVEN.** If dialogdesign.dk, EUR-Lex or web.dev cannot be read, the gap STAYS UNPROVEN with the HTTP status / error quoted. ⛔ Do not fill from memory — not the seven names, not the 200 ms, not the Article text.
- **One fetch per tool call.** The sandbox kills at the call boundary (~178 s measured). Batch nothing.
- **Browser tools:** Claude in Chrome is the preferred browser; the built-in browser is the fallback. Read-only: navigate + read text. No clicks on consent banners beyond declining non-essential; no downloads; no forms.
- **Dated history is NOT edited.** `2026-09-02-236-R1-*.md`, `2026-09-02-236-R2-*.md`, `_PLAN-designers-brain-2026-09-02-v1.html` and their asset folders are frozen. You write ONLY under `notes/_subreports/2026-09-02-237-G-gap-discharge.md` and `notes/_subreports/assets/2026-09-02-237-G-gap-discharge/`.

## DO NOT RULE

- Nothing about schema (tensions as edges/nodes), node types, which principles enter, or names for the evidence grades — Dave's, being ruled in the conductor's window this morning.
- Do not write to `knowledge/_rulings.json`, `knowledge/_state.json`, `_CARRIES.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, memory, or the plan. The conductor mints your store row and commits.
- No `git add`, no `git commit`, no `git add -A`, no `_build_all.py`, no `_gen_chain.py`.
- Do not chase R2-2 (the video). Dave dropped it.
- Do not "improve" R1's or R2's grades or the borrow matrix; report what would MOVE and leave the move to Dave.

## FILING

Copy `notes/_subreports/_TEMPLATE.md`; `sub index` = `G`; `brief:` = this file. Report path: `notes/_subreports/2026-09-02-237-G-gap-discharge.md`. Counts line: **gaps 7 · DISCHARGED n · STAYS-UNPROVEN n · fetches n (ok n / failed n) · addenda files n.** Every gap gets one row in a status table: `R1-1 … DISCHARGED — receipt <file>#<key>` or `STAYS UNPROVEN — <named failure>`. Close with **REPLAY-THESE** (≤ 7 lines: the seven verdicts, one each, plus any DIVERGES). Token spend: `UNMEASURED — no message.usage at a sub's seat`, plus the SHAPE (tool calls, fetches, files written). Return to the conductor a STUB only: the report path, the counts line, and the REPLAY-THESE block.

## PITFALLS (consequences replayed, #165)

1. **Names from memory.** The seven ISO principles are well known; the temptation is to type them. A name typed from memory carries no receipt, and the brain would then cite a standard it never read. If the page is unreachable, the gap stays open — that outcome is fine.
2. **EUR-Lex's 202-with-zero-bytes.** It happened to R1. Try the routes in order and record every one; a browser-rendered read is legitimate; a mirror is not (that is the gap).
3. **The sandbox is not Dave's Mac.** R2-3's whole point is the filesystem outside the repo. An `ls ~/.claude` in the sandbox answers a different question. Name the filesystem on every path.
4. **Parity is meaning, not bytes.** The academy pages are copy-edited; a byte diff will always "diverge". Judge whether the borrow-matrix cell would move.
5. **Over-quoting.** ≤ 15 words per quote, one quote per fact. Standards and EU law are copyrighted or database-protected text; our words carry the fact.
6. **Scope creep.** R1 has 15 other UNPROVEN items and an EAA date question. Not this lane. Seven gaps, then file.
7. **Call-boundary kills.** A fetch that takes > ~170 s dies silently. One fetch per call, and if a call returns nothing, record it as a failed attempt, not as an absence.
