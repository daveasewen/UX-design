# `#237`-`G` — seven declared gaps from the designer's-brain lanes, discharged

session: `#237` · 2026-09-02
window: lane G (gap discharge), conductor Fable
sub index: `G`
brief: `notes/_briefs/2026-09-02-237-G-gap-discharge-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`

## VERDICT

All seven gaps are **DISCHARGED**, each with a receipt, and none was filled from memory. The two
that were expected to be hard both broke the same way and both yielded to the same instrument:
EUR-Lex and web.dev returned nothing useful to the sandbox fetcher and rendered completely in the
browser — the EUR-Lex HTML route that gave `#236` HTTP 202 with zero bytes, and gave this lane an
empty body three times over three routes, is the *same URL* that rendered 418,837 characters in
Chrome. The client was the problem, not the route. The twelve unfetched academy lessons all carry a
verdict: eleven **equivalent**, one **DIVERGES**, and the one that diverges is the closing lesson,
which is not a play and carries no borrow-matrix cell. **No matrix cell is falsified.** Three cells
could move in Apollo's favour and are reported for Dave, not moved. One gap carries a named
residual that this lane could not close by any means available to it: `R2-3`'s user-level hook
question, because `Read` and `Glob` both refuse `/Users/daviewen/**` as outside the session's
connected folders — three of five filesystem layers are proved clear, two are undetermined, and the
price of closing them is two commands in Dave's own terminal.

COUNTS: gaps 7 · DISCHARGED 7 · STAYS-UNPROVEN 0 · fetches 20 (ok 15 / failed 5) · addenda files 8

*(template-shape counts, for the doc gate: findings `9` · ruling-shaped `4` · UNPROVEN `3`)*

## STATUS TABLE — one row per gap

| Gap | Verdict | Receipt |
|---|---|---|
| **R1-1** ISO 9241-110 seven principle names | **DISCHARGED** | `iso-9241-110-addendum.json#principles` — seven names, each with a ≤15-word quote; edition and year at `#edition_and_year_as_the_page_states_it` |
| **R1-4** DSA Art. 25 from EUR-Lex itself | **DISCHARGED** | `dsa-art25-eurlex.json#article_25` — paragraphs 1–3, route that worked at `#routes_tried_in_order[3]`, diff verdict at `#diff_against_the_mirror_r1_used` |
| **R1-5** INP "good" threshold | **DISCHARGED** | `inp-threshold.json#thresholds` — 200 / 500 ms boundaries read off the rendered page; percentile at `#the_percentile_the_threshold_is_stated_at` |
| **R2-1** twelve academy lessons match their blog sections | **DISCHARGED** | `academy-lessons-parity.json#lessons` — 12 verdicts: 11 equivalent, 1 DIVERGES (lesson 14, no cell at risk) |
| **R2-3** no hook layer anywhere on this machine | **DISCHARGED as a probe** — every path has a stated result, none left as "not tried". ⛔ **RESIDUAL:** Dave's user-level and managed layers NOT determined | `hooks-probe.json#paths` (6 paths, each naming its filesystem) · `#verdict_by_layer` · `#residual` |
| **R2-4** `CLAUDE.md` + `AGENTS.md` play the rails-file role | **DISCHARGED** — verdict **PARTLY** | `rails-files-reread.json#does_it_function_as_a_rails_file_for_a_generating_agent` · row-4 verdict at `#does_r2_matrix_row_4_stand` |
| **R2-5** does ADR-0017 cover briefs? | **DISCHARGED** — verdict **SILENT**, grep count 0 | `adr-0017-briefs.json#verdict` · `#grep_counts` |

## What was done

**Ground first.** Read `2026-09-02-236-R1-principles-survey.md` § UNPROVEN items 1, 4, 5;
`2026-09-02-236-R2-sdlc-playbook.md` § UNPROVEN items 1, 3, 4, 5 (item 2, the video, **dropped by
Dave, not chased**); `assets/2026-09-02-236-R2-sdlc-playbook/fetch-receipts.json` for the lesson
URLs; `assets/2026-09-02-236-R2-sdlc-playbook/borrow-matrix.json` for the twelve cells; and
`2026-09-02-236-R2-sdlc-playbook.md` §1 for the blog play summaries that R2-1's parity test is
judged against. Then `notes/_subreports/_TEMPLATE.md`.

**Departure from the #236 handoff's suggested path, as the brief instructs me to say plainly.**
The #236 handoff suggested filing the ISO addendum at
`notes/_subreports/assets/2026-09-02-236-R1-principles-survey/iso-9241-110-addendum.json` — inside
#236's asset folder. **Nothing was written there.** All eight files live in this lane's own folder,
`notes/_subreports/assets/2026-09-02-237-G-gap-discharge/`, so provenance is one lane, one folder.
The reason is ADR-0017 Rule 3 read back at me by this lane's own last gap: the #236 assets are a
dated period record, and adding today's readings to them is the falsification Rule 3 forbids. The
plan's next version should point here.

**Files written — all new, none edited.** Nine, under exactly the two paths the brief permits:

- `notes/_subreports/2026-09-02-237-G-gap-discharge.md` (this file)
- `notes/_subreports/assets/2026-09-02-237-G-gap-discharge/iso-9241-110-addendum.json`
- `…/dsa-art25-eurlex.json`
- `…/inp-threshold.json`
- `…/academy-lessons-parity.json`
- `…/hooks-probe.json`
- `…/rails-files-reread.json`
- `…/adr-0017-briefs.json`
- `…/fetch-receipts.json`

**Not touched:** no dated report, no `_PLAN-designers-brain-2026-09-02-v1.html`, no
`_rulings.json`, no `_state.json`, no `_CARRIES.md`, no `GOOD-MORNING.md`, no `_LIVE-STATE.md`, no
memory file. No `git` command of any kind. No `_build_all.py`, no `_gen_chain.py`.

## Findings

1. **The EUR-Lex failure is a CLIENT failure, not a route failure — and that is a reusable
   finding.** Three sandbox-fetcher routes returned nothing: the CELEX HTML route and the PDF route
   each returned a resolved-URL line and zero document bytes; the ELI route returned HTTP 200 with
   the page shell only, ending at the Help/Print controls with no articles in it. The browser then
   rendered **the same CELEX HTML URL** as attempt 2 in full — `document.body.innerText.length` =
   418,837. *Probe:* `fetch-receipts.json#attempts[1]` versus `#attempts[4]`. The consequence for
   later lanes: an EU-law fetch that comes back empty is not evidence the document is unreachable,
   and a mirror is not the next step — the browser is.

2. **A false absence hid Article 25 on a page that contained it.** The first in-page search,
   `innerText.indexOf('Article 25')`, returned `-1`. EUR-Lex separates the word from the number with
   a non-breaking space (U+00A0). The regex `/Article[\s ]{0,3}2[4-6]/` found the heading at
   index 254,755 immediately. *Probe:* `dsa-art25-eurlex.json#probe_note_worth_keeping`. Any future
   gate that greps EU law for an article heading must allow ` `, or it will report live
   articles as missing — [[unmatched-grep-is-not-an-absence]] with a concrete instance attached.

3. **The mirror R1 used was accurate.** The fragment R1 quoted from
   `eu-digital-services-act.com` — *"shall not design, organise or operate their online interfaces
   in a way that deceives or manipulates"* — appears **verbatim** in the EUR-Lex text of paragraph 1,
   and R1's own register statement is faithful to it. The gap was never a meaning gap; it was a
   source-authority gap, and it is now closed. What is genuinely **new** is paragraphs 2 and 3,
   which the register did not hold at all: a carve-out routing practices already covered by the
   Unfair Commercial Practices Directive or GDPR away from Article 25, and three named example
   practices — prominence-weighting a choice, re-asking a choice already made, and making
   cancellation harder than sign-up. All three are decisions a generator makes.
   *Probe:* `dsa-art25-eurlex.json#diff_against_the_mirror_r1_used`.

4. **The INP figure is a population statistic, not a budget.** 200 ms good, above 200 and up to
   500 needs improvement, above 500 poor — but stated at the **75th percentile of page loads
   recorded in the field, segmented mobile and desktop**. The page opens the section by conceding
   the labels are difficult because device capability varies. A node that carries "200 ms" without
   the percentile-and-population qualifier will be cited as a per-interaction target, which is what
   the page argues against. The page's own last-updated date is **2025-09-02**, exactly one year
   before this read — a conclusions-are-debt row that wants a re-check date. *Probe:*
   `inp-threshold.json#the_percentile_the_threshold_is_stated_at`.

5. **All twelve lessons carry a verdict and no borrow-matrix cell is falsified.** Eleven
   **equivalent**; one **DIVERGES** — lesson 14, the closing, whose prose is course-specific and
   does **not** contain the blog's closing line (a substring probe for `loop keeps running` returned
   false). It is not a play, so **no cell is at risk**. Six lessons carry the exact sentence R2
   quoted from the blog for that play, which is stronger evidence of parity than paraphrase
   agreement. *Probe:* `academy-lessons-parity.json#totals` and the per-lesson `receipt` fields.

6. **Three borrow-matrix cells could move — all in Apollo's favour. Reported, NOT moved.**
   (a) **P7 / target P**: R2's named change, "add a mock-diff round to the three browser gates", is
   the play's own step 5 — *"Implement, screenshot, compare, and adjust. Two or three rounds is
   normal."* The cell could move from ADAPT-with-our-change to ADOPT-as-written, which is a stronger
   position: the visual loop stops being our invention and becomes a play we had not yet taken.
   (b) **P2 / target P**: the lesson names an intent → mock in Claude Design → iterate → export
   route for front-end work, where the reviewable artefact is the mock rather than a written spec —
   a different shape from R2's proposed one-screen spec.
   (c) **P10 / target M**: the playbook splits hooks in two and puts them in different places —
   build-phase hooks **block**, fast and scoped to the changed file, while hooks that **ask** belong
   at deploy, because an approval prompt during build puts a person back on the critical path of
   every parallel session. Memento's two most-breached rules are commit-time concerns, so the shape
   of R2's proposal may want revisiting even though its verdict does not.
   *Probe:* the `cell_it_could_move` / `cell_it_could_refine` blocks in `academy-lessons-parity.json`.

7. **R2's §1 description of the course is wrong in two places — descriptions, not verdicts.**
   R2 recorded four blog sections as having "no course lesson". **Three of the four have course
   homes**: auto mode and the legacy-systems sidebar are trailing sections of lesson 4, build-time
   hook guardrails is a trailing section of lesson 6, and Claude Tag is a trailing section of lesson
   13. Only *scheduled codebase scans* was not seen anywhere in the twelve. Separately, R2 says every
   play has the same five parts; **four lessons have four parts** — 5, 6, 9 and 11 have no "What
   changes" table. Neither correction touches a matrix verdict. *Probe:* the `correction_to_r2`
   blocks in `academy-lessons-parity.json`.

8. **`CLAUDE.md` and `AGENTS.md` are one artefact with two filenames, and it is a behaviour
   contract rather than a rails file.** Both are generated from `cold-start/DESIGN-CONTRACT.md` by
   `gen_projections.py`, and `diff` of the two files from line 2 onward is **empty** — the entire
   15-byte difference is the host named in the generated-from comment. Verdict on the rails-file
   role: **PARTLY**. It occupies the slot exactly (root, versioned, one page, read before building)
   and its five rules are the playbook's "things Claude gets wrong" category. But it has **no
   Commands section, no Architecture section, and no separate mistakes list** — it governs how the
   agent must behave, not where things are. This is ADR-0017 done right, not a duplication defect,
   and worth saying out loud because a naive audit would flag two identical files as a violation.
   *Probe:* `rails-files-reread.json#identity_probe`.

9. **ADR-0017 never says "brief".** Grep count **0** for `brief` case-insensitive, **0** for
   `_briefs`, **0** for `notes/_briefs`. Rule 3's history exemption is an enumeration of four
   classes — *"ledger entries, ds-entries, decision-history dossiers, ratified records"* — and a
   brief is not among them. But Rule 5 speaks of **"a new document"** without qualification, and
   Rules 1–2 are written about facts rather than document types, so all three reach a brief by
   implication. The ADR therefore leaves a brief **governed but unclassified**: bound by the
   live-fact rules, not granted the frozen-history protection. That is precisely what makes R2's
   question 2 a question. *Probe:* `adr-0017-briefs.json#grep_counts` and `#verdict`.

## RULING-SHAPED QUESTIONS

⛔ **MANDATORY SECTION.** Nothing below is decided. Each is Dave's. Where this lane's brief fenced
a recommendation, no recommendation is offered and the fence is named.

1. **Do the three movable borrow-matrix cells move?** (a) Leave the matrix as `#236` filed it and
   carry the three notes as annotations; (b) let a later lane re-issue the matrix with P7/P moved to
   ADOPT, P2/P gaining the mock-first route as a second option, and P10/M's proposal re-shaped
   block-versus-ask. **No recommendation** — the brief fences this lane from improving the matrix,
   and all three are reported rather than applied. Price of (b): one re-issue of `borrow-matrix.json`
   as a new dated artefact, ~2,900 tk.

2. **Does `pr-dsa25`'s `refutation_probe` get updated?** The field currently reads *"Re-verify
   against EUR-Lex before any client-facing use"* — a condition now met, with paragraphs 2 and 3 held
   for the first time. (a) Leave the `#236` register frozen and let the graph build read this lane's
   addendum as the live source; (b) re-issue the register row. **Recommend (a)** on ADR-0017 Rule 3
   grounds: the register is dated history, and the addendum is the newer reading with its own home.

3. **Do the seven ISO names enter the graph at names-only depth?** The page is a licensed
   practitioner summary reproducing the **FDIS draft** with permission from Danish Standards, not the
   published standard, and the standard's own scale is *"20 categories of recommendations, 65
   recommendations, and about 140 examples"*. (a) Enter the seven names with the draft-source caveat
   on the row; (b) hold the family out until the published standard is bought. **Recommend (a)** with
   the caveat carried as a field rather than as prose, because a name-level node is honest about its
   own depth and a missing family is not.

4. **Does the `R2-3` residual get closed by Dave, or stay declared?** Three filesystem layers are
   proved clear; Dave's user-level and managed layers are undetermined because the file tools fence
   `/Users/daviewen/**`. (a) Dave runs `ls -a ~/.claude/` and `grep -l '"hooks"' ~/.claude/settings*.json`
   and pastes the output — ten seconds, and the claim closes completely; (b) the residual stays
   declared and `P10/M` keeps a stated dependency. **Recommend (a)**, and ⛔ **not** by connecting his
   home directory to a session — the two commands are cheaper and narrower than a directory grant.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** *That no hook layer exists at Dave's user level or in managed settings.* Three of
  five layers are proved absent — the repo (`agents/` and three `.md` files, nothing else), the whole
  mount (no `.claude/settings*` anywhere; the only `settings*.json` hits are three `.vscode/` files,
  none containing `"hooks"`), and the sandbox's own home (no `~/.claude` at all). The user-level and
  managed layers were refused, verbatim: *"`/Users/daviewen/.claude/settings.json` is outside this
  session's connected folders, so Read can't reach it."* Two different tools (`Read`, `Glob`) were
  tried and both refused for the same reason — a session-scope fence, not a filesystem error.
  **Price to prove:** two commands in Dave's own terminal (question 4a).

- **UNPROVEN:** *That the two course-side passages are course-ONLY.* Lesson 3's Claude Design
  mock-then-export route and lesson 11's managed-settings key list are absent from R2's one-line blog
  summaries, but absence from a summary is not absence from the source, and this lane did not re-fetch
  the blog. Both are flagged inline in the parity file rather than claimed as course additions.
  **Price to prove:** one fetch of `https://claude.com/blog/the-ai-native-sdlc-playbook` plus two
  targeted searches, ~1K.

- **UNPROVEN:** *The published ISO 9241-110:2020 wording, and everything below the seven names.*
  The page reproduces the **draft** (`ISO/FDIS 9241-110.2020`) with permission, so the definition
  sentences are draft text, and the 20 recommendation categories, 65 recommendations and ~140
  examples were not fetched at all. The seven names, their order and one definition sentence each are
  what this lane holds. **Price to prove:** purchase of the standard.

- **Not a defect, stated plainly:** neither fetch tool returns a byte count or an HTTP status line,
  so `fetch-receipts.json` records status as *what the tool's behaviour demonstrated* and marks every
  unmeasured size `NOT MEASURED` rather than estimating one. The three real sizes in that file were
  measured in-page and name their method. Likewise, per-fetch UTC timestamps were not available; the
  file gives the anchored window (12:00Z–12:18Z) and quotes the three wall-clock readings that fix it,
  rather than inventing twenty stamps.

- **Honesty note carried in `hooks-probe.json`:** this lane's first hook grep was piped into `head`,
  so the `$?` it printed was **head's** exit status, not grep's. The probe was re-run unpiped to
  capture grep's own exit code (1) and line count (0). The receipt is the re-run, not the first
  reading. [[a-crash-is-not-a-fail]] · [[feedback-measuring-tool-must-not-guess]].

## Evidence

`notes/_subreports/assets/2026-09-02-237-G-gap-discharge/` — eight files.

- **`iso-9241-110-addendum.json`** — the seven principle names in order, each in our words with a
  ≤15-word quoted receipt, plus the edition/year as the page states it, the draft-reproduction
  licence sentence, and the scale of what remains unfetched. Proves R1-1 discharged from a named
  source rather than from memory.
- **`dsa-art25-eurlex.json`** — Article 25 paragraphs 1–3 in our words with one quote each, the four
  routes tried in order with each outcome, the U+00A0 probe note, and the diff verdict against R1's
  mirror. Proves the text came from `eur-lex.europa.eu` and that the mirror was accurate.
- **`inp-threshold.json`** — the three boundaries in ms, the 75th-percentile-of-field qualifier, the
  page's own hedge, and the page's published/last-updated dates. Proves the figure was read off the
  rendered page.
- **`academy-lessons-parity.json`** — twelve lessons, each with URL, blog section, verdict, receipt,
  and where relevant the matrix cell that could move or the correction to R2 §1. Proves all twelve
  carry a verdict and that no cell is falsified.
- **`hooks-probe.json`** — six paths, each naming **which filesystem** it is on, each with
  reachable/exists/contains-hooks and the probe that produced it, plus a verdict-by-layer block and
  the named residual. Proves nothing was left as "not tried" and that the sandbox was never mistaken
  for Dave's Mac.
- **`rails-files-reread.json`** — sizes, the generator both files are projected from, the empty
  `diff`, what they instruct in our words, the PARTLY verdict with its quote, and the row-4 verdict
  cell by cell. Proves both files were read in full.
- **`adr-0017-briefs.json`** — the ADR's own four-class list quoted, the three grep counts at zero,
  each rule tested for whether it reaches a brief, and the verdict. Proves the SILENT verdict with a
  counted probe rather than an impression.
- **`fetch-receipts.json`** — all 20 attempts in order with tool, outcome, status-as-demonstrated,
  size-or-NOT-MEASURED, and the verbatim failure text for each of the 5 failures; plus the three URLs
  deliberately not fetched and why, and the read-only browser conduct note.

**Token spend:** `UNMEASURED — no message.usage at a sub's seat`. **Shape:** ~57 tool calls — 17
`web_fetch` (12 ok, 5 failed), 8 Claude-in-Chrome calls (3 navigate, 5 read-only JS, all ok), 2
`ToolSearch`, 5 `bash`, 9 `Read`, 1 `Glob` (refused), 1 `Grep`, 9 `Write`. 20 URL attempts, 15 ok, 5
failed. 9 files written, 0 files edited, 0 git commands.

REPLAY-THESE: `R1-1` DISCHARGED — seven ISO names held at names-only depth, from Molich's licensed **draft** reproduction, not the published standard · `R1-4` DISCHARGED — Art. 25 §§1–3 from EUR-Lex; mirror verdict **SAME**; §§2–3 are NEW, and §3's three named practices are all generator decisions · `R1-5` DISCHARGED — good ≤200 ms, needs-improvement >200–500, poor >500, **at the 75th percentile of field page loads, mobile and desktop separately**; page last updated 2025-09-02 · `R2-1` DISCHARGED — 12/12 verdicts, 11 equivalent, **1 DIVERGES: lesson 14 closing, no matrix cell at risk**; three cells could move in Apollo's favour (P7/P → ADOPT, P2/P mock-first route, P10/M block-vs-ask) — reported, not moved · `R2-3` DISCHARGED as a probe, **RESIDUAL OPEN** — repo, mount and sandbox layers proved clear; Dave's user-level and managed layers refused by the tool fence; closes on two terminal commands · `R2-4` DISCHARGED — one artefact, two filenames, generated from `DESIGN-CONTRACT.md`; rails-file role **PARTLY**; row 4 stands, its D-cell why-clause is in tension with a file that IS a behaviour contract without enforcement · `R2-5` DISCHARGED — **SILENT**, grep count **0**; Rule 3 names four history classes and a brief is not one, while Rule 5 says "a new document" — governed but unclassified
