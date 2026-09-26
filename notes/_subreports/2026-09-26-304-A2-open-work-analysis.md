# #304 lane A2 — the open-work backlog, analysed

Session #304, Saturday 2026-09-26. Read-only lane. Author: lane A2 (Opus 5.5). Scope: the open-work store, the carries, the last seven handoffs' owed lists and the GOOD-MORNING worklist, clustered and boiled down for the Fable synthesis seat.

Dave's ask, verbatim (15:33): "I think we need an analysis of all the proposed development of Apollo we already have and, check out the future state too. then lets layout a proposed roadmap so we can make some progress. Put together a plan, lets leverage some big pushes over this weekend that I can leave you to churn though, recommend the models, effort levels and subs structure you propose to get some work nailed by early next week. don't worry about token spend. lets get ripping, you know the usual instructions, watch the externalities, dependancies and test it hard :)"

Every count below is MEASURED by a script in `notes/_lanes/304/A2/` unless it says ESTIMATED. The theme clustering is keyword-based and I spot-checked about ninety rows by eye; roughly one in thirty sat in the wrong theme (for example W-364, the polarity gate under `knowledge/brain/`, first landed in the deck theme until I narrowed the word "brain"). Treat theme counts as plus or minus a few; the kind, owner, close-type and age counts are exact.

---

## 0. The answer in one screen

The store says 746 live items, and it is true, but it is not a backlog of 746 pieces of work. 632 of the 746 (85%) are document rows: briefs, filed reports, wrap briefs, handoffs, memory hooks, dossiers and review pages that were rowed so the doc-row gate would pass. Only 114 rows describe work in the ordinary sense. The store is also one-way: across the last twenty sessions (#284 to #303) it opened 169 rows and closed 4. Across #204 to #303 it opened 792 and closed 61.

The real weight sits on Dave. 482 live rows close only on his word (436 outright, 46 "his word or an explicit carry"), and the 104 of those rows that state a number carry at least 531 named questions between them. 316 of the 482 are two weeks old or more. Nobody can answer 531 questions in a sitting; the only route through is a handful of blanket decisions, and section 6 gives eight of them. Answered as recommended, they would settle or park about 305 rows (41% of the store) and about half the carries.

What Claude can do this weekend without asking: close 93 of its own rows whose close event has provably passed (git and file receipts in `autonomous_close_candidates.json`), enact decisions Dave has already ruled but nobody built (a named list in section 3), fix the store so it cannot regrow like this, and work the machinery rows he has already ordered (for instance s204-D1, "This is great lets get this working!", 38 days old and unbuilt).

The carry list is worse than the store. `_CARRIES.md` § `residual → #304` holds 709 items (the capture gate's own splitter), median age 37 wraps. 342 of them (48%) are dead weight by construction: 111 struck (~~) but still carried, 58 about the deck or Friday (now past), 57 splitter fragments, 23 copies of the "what this wrap did not do" and "consequences and pitfalls" boilerplate, and 93 repeats of recurring series (CI read-back owed, boot-ceiling breaches, fill over a line, memory unwritten, index.lock). `_CARRIES.md` itself is 36,276,633 bytes.

---

## 1. What the record holds, and how it was read

Sources, each read as the brief asked:

- `knowledge/_state.json`: schema 1, three keys (`_README`, `meta`, `items`); 855 items; states `open` 746, `done` 89, `parked` 20. `python3 knowledge/_state.py` prints "live 746 · conditioned 841 · UNCONDITIONED 14", live by owner dave 443 / claude 303, and the declared debt line naming W-0b and W-01…W-13. Every item carries `id title state opened owner condition closes_when links home project`; 724 carry a `body`, 89 a `closed_by`, one a `deadline`, none an `effort`. The legacy tuple `_state.LEGACY_IDS` holds 19 ids; five are done (W-0c, W-0d, W-14, W-15, W-16), fourteen are live and unconditioned.
- `_CARRIES.md` § `residual → #304`: fetched only through `_capture_gate._carry_items`, 709 items (matches the brief), saved as `notes/_lanes/304/A2/carries304.json`.
- `_HANDOFF-148` to `_HANDOFF-154`, § OWED of each. #154's owed list, in order: the Apollo-MCP page; what came back from Friday; whether the Common prompt ran; his three observations into the graph; which Spider pack is on his work machine; the HSBC face in the deck's font stack; the callipers' overrun; everything standing from `_HANDOFF-152`.
- GOOD-MORNING via `_memento_search.py`: `gm:DOFIRST` (items 0b to 26, the legacy worklist), `gm:C1` (next strands), `gm:C2` (the ruling batch, "15 REMAIN of 16"), `gm:C4` (enact queue and standing carries, most bodies offloaded to rows W-99k…W-99p at #213).
- Session dates: the first commit date carrying `#N` in `git --no-optional-locks log` (saved `gitlog.txt`, 1,632 commits). Ages in days are measured from those dates to 2026-09-26.

Scripts (all read-only against the record): `analyse.py` (kind, theme, close type, age), `verify.py` (has the close event already happened?), `daveq.py` (what kind of act each Dave-close row needs), `carries.py` (carry classes), `decisions.py` (what each proposed decision unblocks).

---

## 2. The backlog, clustered

### 2a. By kind: what each row is

| Kind | Live | Dave's | Claude's | Median age |
|---|---:|---:|---:|---:|
| Filed report (lane reports, receipts, verifies, cold runs) | 347 | 223 | 124 | 20 d |
| Wrap artefact (wrap brief, W report, handoff, hook, dossier, words-verbatim) | 144 | 80 | 64 | 16 d |
| Brief (lane or sub brief, divvy) | 96 | 36 | 60 | 26 d |
| Review surface (review page, decision page, plan page) | 28 | 27 | 1 | 30 d |
| Drawing or deck version | 17 | 17 | 0 | 6 d |
| Work item | 82 | 45 | 37 | 32 d |
| Instrument (gate or probe awaiting wiring or promotion) | 27 | 10 | 17 | 32 d |
| Built, proposed, not ruled | 5 | 5 | 0 | 37 d |

Document rows (the first five kinds) total 632; work rows total 114. W-398 and W-399 say it themselves: "this row is a document row, not a work item".

### 2b. By theme

| Theme | Live | Dave's | Claude's | Median age | Oldest |
|---|---:|---:|---:|---:|---:|
| T2 Wrap ritual, boot, context window, Memento machinery | 184 | 104 | 80 | 18 d | 55 d |
| T5 Knowledge graph, rules, principles, icons, logos | 106 | 68 | 38 | 24 d | 40 d |
| T7 Dashboards, bento, one-shot composition | 99 | 62 | 37 | 23 d | 37 d |
| T8 Components, tokens, themes | 77 | 48 | 29 | 32 d | 39 d |
| T6 Charts and the data-viz engine | 69 | 37 | 32 | 21 d | 55 d |
| T3 Designer pack, releases, cold start | 63 | 34 | 29 | 29 d | 36 d |
| T1 Friday deck and presentation | 61 | 54 | 7 | 6 d | 36 d |
| T4 Gates, CI, verifiers | 56 | 18 | 38 | 27 d | 38 d |
| T9 Research strands (Jev, MCP and GenUI, taxonomy, APCA) | 24 | 12 | 12 | 19 d | 36 d |
| Other | 7 | 6 | 1 | 24 d | 55 d |

The fourteen legacy rows have `opened: 0` and no measurable age; their bodies say they were born between #27 and #59 (late July), so about two months (ESTIMATED from the body text).

### 2c. By close type: who can close it

| What closes it | Live | Dave's | Claude's |
|---|---:|---:|---:|
| Dave's word only | 436 | 361 | 75 |
| Dave's word, or an explicit carry | 46 | 14 | 32 |
| An event: a wrap landing, an opener reading, a report filed, a parent row closing | 177 | 38 | 139 |
| A build or a fix | 73 | 30 | 43 |
| Nothing: unconditioned legacy | 14 | 0 | 14 |

What Dave is being asked to do, across the 482 rows that need his word (`daveq.py`): answer ruling-shaped questions on a filed report, 144 rows (at least 383 named questions); an unclassified word of his, 111 rows; look at something by eye or sign it off, 58 rows; deck and presentation calls, 59 rows; release ratify, cut or cold test, 49 rows (at least 90 named questions); promote or park an instrument, 41 rows; return an export from a decision page he was given, 20 rows.

### 2d. Age and flow

Median age of a live row: 23 days (quartiles 10 and 30). By age and owner: 148 are a week old or less (130 Dave's), 60 are 8 to 14 days, 348 are 15 to 30 days, 176 are over 30 days, 14 are legacy. Opened against closed, by session band: #204–#233 opened 348, closed 38; #234–#263 opened 207, closed 13; #264–#283 opened 68, closed 6; #284–#303 opened 169, closed 4. A doc row is now minted for every file a wrap writes (h, k, v, w, dh for every session since #295), and the close conditions of those rows point at the next session's opener. So each session creates about five rows that the next session makes true and nobody closes.

---

## 3. What Claude can do this weekend without asking

Each lane below rests on a ruling or on a mechanical condition already in the record. None of it needs a new word from Dave. Each still needs its render proof or gate run at Dave's seat, and his eye afterwards where the row says so.

### Lane H — close by addition, and stop the regrowth

1. Close, by addition with the receipt quoted, the 93 Claude-owned rows whose close event provably passed: 76 where the named session's wrap commit or next opener exists in git (for example W-47 "the #204 wrap commit…", receipt `3a887773`; W-239 "#221 wrap commit lands", receipt `f2d0f024`; W-354, receipt `65161872`), and 16 where the report the brief commissioned exists at the path its close names (for example W-205 → `notes/_subreports/2026-08-27-220-replay-discharge.md`). The full list with receipts is `notes/_lanes/304/A2/autonomous_close_candidates.json`. ⚠ `verify.py` matches git subjects by pattern; a closing lane must re-read each receipt before writing `closed_by`, and the "relayed to Dave in chat" half of some conditions (W-41, W-43, W-47) cannot be checked from git. Where that half is unprovable, close with the gap declared or leave the row.
2. Five memory-hook rows carry their own placement receipt on disk: W-298k, W-299k, W-300k, W-301k and W-302k (`notes/_lanes/<n>/WRAP-MEMORY-HOOK.md`, § RECEIPT at lines 64–69 of each). W-296k and W-297k have none; W-303k says "NOT PLACED BY THE #303 WRAP SEAT — A SEAT LIMIT". Leave those three.
3. About 47 more Claude-owned EVENT rows are past-session events that `verify.py` could not receipt automatically, because they name a seam commit or say "retired with the #219 record" (W-164, W-165, W-171, W-177, W-182, W-185, W-186, W-187 and others). They are probably met (ESTIMATED) and each needs one look.
4. The prevention, which is the part that matters (it is the "instrument without a consumer" lesson turned round): teach `_state.check()` (or the capture gate) to find rows whose close names a past session's wrap or opener, and to refuse a wrap while such rows stand unclosed. Also stop minting h/k/v/w/dh rows whose only close is "the next opener read it". A doc row should close at birth when the only obligation is that it exists.

Expected effect: live 746 → about 650 from the receipted set alone (MEASURED 93 + 5), and lower once the probable set is looked at.

### Lane E — enact what Dave has already ruled

The rulings store flags 23 rulings as ruled and not enacted in free text. At least one flag is stale: s131-D1 ("legacy RAG fills take the legacy system's OWN colours") says "NOT ENACTED", yet `knowledge/tokens/semantic-colour.json:803` carries "s131-D1 (#131): MINTED". So step one is an enactment audit against the tree. Step two enacts what survives the audit and has its values in hand:

- Token and canon rulings with values given: s130-D4 (banner actions ghost/tint), s130-D5 (check and selection labels always ink), s130-D6 (chips pressed from each theme's own ramp), s149-D1 (mono error joins the ink camp), s151-D1 and s151-D2 (the two-red law re-keyed by background; chip pressed without reversal), s135-D1 (notification shell border and radius), s157-D2 (the palette tier, brief at `notes/_briefs/2026-08-12-s157-palette-tier-brief.md`).
- Store rows already ruled: W-99 (ds-018 disabled grey, s212-D1, #9D9D9D light / #808080 dark), W-99a (the RAG A+B+C pick, s212-D2), W-97 (the bar half of the intro-motion law), W-59 (five var collisions renamed to component-local names), W-437 (VFIT into `dv-behaviour.js`, s248-D2: Dave, "the charts should probably be vertically responsive to"), W-303 (roster drift fixed as an explicit act, s228-D5: "hold at 58 but i want this fixed, its just an annoyance").
- Excluded, because the value is still his: s155-D1 (the two green values "are still Dave's and have never" been given) and s144-D1 (the rung's name is unruled).

The visual ones end at a render page for his eye. The rulings exist; the eye closes the row.

### Lane M — machinery he has already ordered

- s204-D1 mechanisation item 1 (W-44: claim/challenge JSONL, generated join, evidence linter), ruled "BUILD NEXT" 38 days ago. Item 2's registry exists (`knowledge/_probe_registry/`), but W-45 and W-48 wait on "one real verifier wave" to run `_registry.py --run`. Run it in the weekend's verifier wave and both close.
- An `--amend-status` path in `knowledge/_inscribe_ruling.py`. W-295i records that no tool can stamp `status: enacted`, and s295-D2 rules that "the enacting lane stamps the status". Without this path Lane E cannot record what it enacts.
- W-189 (`run-gates.py` per-gate argv from the pack's `_MANIFEST.json`), W-99zv (manifest skills group repointed to designer-skills-v3), W-355 (the post-wrap handoff commit deadlock), W-13 (three runbooks still mention /tmp; measured grep counts 2, 7 and 47, some of them legitimate).

### Lane C — the six inherited CI reds

The same six gates fail on every pushed tree: `[3] [13] [38] [125] [128] [136]`, plus the help gate's 12 failures (`_HANDOFF-154` § POST-WRAP item 5, run `36244018143`, "IDENTICAL to #302's"). They are Claude's to repair, and while they stand red a new red cannot be seen behind them. Lane A4 owns health, so I only flag the dependency: every weekend push reads CI against these six. One of them, `_gen_chain.py --check` (W-519 Q3), is red by construction on every pushed tree, and whether it stays blocking is Dave's question (section 6, D8).

### Lane K — graph work already ruled

s234-D4 (the composition edge, "ruled and unbuilt" for 69 wraps in the carries, proposed at #245 lane L3), s273-D2 (authoring pass two, ruled, not started), and drafting the universal-icon list for W-282a (the draft is Claude's; Dave ratifies the members). His three observations into the graph (`_HANDOFF-154` owed 4) are his words, "at some point"; drafting the nodes is doable, landing them wants his nod.

### Externalities every weekend lane must plan around

These are measured in the record, not guessed.

- The mount strands `.git/index.lock` on the wrap gate and on `git reset`, "the seventh wrap running (#297–#303)", and it forbids unlink (`_HANDOFF-154` § COLD SEAT). Locks can only be moved, to `notes/_lanes/_orphan-locks/`. One committer at a time.
- `BOOT_CEILING_TK` is 72,768 and the cloud seat boots at about 127,000 to 128,000 (six readings, #297 to #302), so every `--wrap` commit is refused and wraps go by the declared not-a-wrap path.
- The GitHub token sits in the remote URL in `.git/config` (carry ③, age 3). Any push this weekend uses it.
- Renders run only at Dave's seat, after `ensure_env.sh`. The seat's fallback face is not Univers unless `HSBC_MtUnivers_Latin` is forced (`_HANDOFF-154` "the fallback face bit again").
- `device_bash` kills background jobs, and each call caps at 180 s. The full build does not fit one call (GM pointer: "~49s for all 75 steps" at #62; it is 142 steps now).
- The doc-row gate refuses a new report without a `_state` row, so Lane H's prevention change and every other lane's reports interact. Lane H should land first, or the other lanes will mint rows it then has to close.

---

## 4. What is blocked on Dave, and the word that unblocks it

Grouped by the act he has to make. The exact questions, with recommended answers, are in section 6.

| Blocked set | Rows | The word that unblocks it |
|---|---:|---|
| Friday deck, drawings, and the handoffs and dossiers whose close is "Friday's deck is final" | 95 (61 in the deck theme + 34 ritual rows bound to it) | "The deck is done." Then one question: what came back from Friday. |
| Ruling-shaped questions on filed reports, two weeks old or more (deck rows excluded) | 105 | "Park them" (with tripwires), or a sitting. |
| Releases v1.0.1 to v1.0.12: ratify, cut, cold test | 23 (14 Dave's) | "Superseded by v1.0.13", plus "cut v1.0.14" and which pack is on his work machine. |
| Window and boot lines | about 20 rows, 39 carries (keyword upper bound 58 rows) | "Inscribe", "236K and 276K", and a ceiling number. |
| Legacy unconditioned | 14 | One close condition each (proposed in section 7). |
| Proposed, not ruled, component and Layer-2 waves | 12 live, plus 10 already parked | "Park until the MCP catalogue needs them", or a sitting. |
| Decision-page exports never returned | 20 | "Park", or he returns the export. |
| Dave-owned rows whose close event already passed | 17 | "Yes, close them." |

---

## 5. Dead weight: closable by addition, with receipts

In the store:

- 93 Claude-owned rows with passed close events and git or file receipts (section 3, Lane H; list in the JSON). Plus 17 Dave-owned rows of the same shape (`verify.json`, verdict EVENT-PASSED or FILED, owner dave). Those need his yes, not his reading.
- Rows whose own text says they are done:
  - W-10: "✅ PER-GATE TEST PLAN — CLOSED #64: 5/5 DRAFTED AND 5/5 RATIFIED (9bc34af)", still open.
  - W-267c: "v1.0.10 is released and pushed (done at de8ed57)".
  - W-263: carry age 79, "W-263 IS STILL state: open THOUGH ITS FORENSICS ARE FILED AND SETTLED".
  - W-99zx: its close is that "the new release job has run green on GitHub at least once". `_HANDOFF-154` § POST-WRAP 5 reads "release ✅".
- Release rows superseded by a later shipped release. `knowledge/_release/_frozen-releases.json` holds apollo-spider v1.0.13 (re-seeded at `df648957`, 2026-09-11). `RATIFY_IDS` in `_gen_pack_manifest.py:960` already keys v1.0.3 to s225-D1 and v1.0.4 to s228-D4, yet W-268 (v1.0.3) and W-302 (v1.0.4) stay open. There are 23 such rows (list in `decision_unblocks.json` under D3).
- Drawing versions superseded by a later version of the same drawing: W-291la to W-291le (workers v1 to v5, superseded by v6, which went onto deck v12 per W-291pa), and W-289ga, W-289gb, W-289gc, W-289da, W-289db (deck v8 to v10, superseded by v14-plain). Their closes need Dave's word (D1).
- Rows that ride a parent: W-309, W-310 and W-311 close with W-305, W-306 and W-307; W-327 and W-328 with W-325 and W-326; W-439 and W-440 with W-435 and W-438; W-297 and W-299 with W-296 and W-298. All the parents are open, so these are not closable yet. They collapse the moment their parents do.

In the carries (`carries_classified.json`):

| Class | Items | Share | Median age |
|---|---:|---:|---:|
| Substantive | 367 | 51.8% | 37 wraps |
| Struck (~~) but still carried | 111 | 15.7% | 58 |
| Deck, Friday, demo (the event has passed) | 58 | 8.2% | 12 |
| Splitter fragments (no marker; `_carry_items` cut mid-item) | 57 | 8.0% | 81 |
| Series: fill or window over a line | 23 | 3.2% | 37 |
| Series: "what this wrap did not do" and "consequences and pitfalls" boilerplate | 23 | 3.2% | 71 |
| Series: index.lock and mount warts | 18 | 2.5% | 22 |
| Series: CI read-back owed (s203-D1) | 18 | 2.5% | 63 |
| Series: boot ceiling and boot breach readings | 16 | 2.3% | 43 |
| Series: memory unwritten or hook owed | 11 | 1.6% | 38 |
| Series: push, local commits unpushed | 4 | 0.6% | 43 |
| Series: recall probe not planted | 3 | 0.4% | 55 |

Some substantive carries repeat the same obligation at three ages ("THE s208-D1 RE-BASE IS STILL HIS" at 77, 78 and 79; "THE POLARITY-RECEIPT BUILD" at 62 and 63). 97 carries cite a W-id, so they duplicate a store row. The splitter fragments are a defect in `_carry_items` or in the wrap's line shape; one line of `_CARRIES.md` now holds the entire residual (the #304 line alone is 638,315 characters of item text, MEASURED).

In GOOD-MORNING's DOFIRST: items 10 (✅ closed #64), 0c, 0d, 14, 15 and 16 are closed in the store but still sit in the worklist prose. `gm:C2` opens "15 REMAIN of 16" for a batch whose ruled items were rolled at #38.

---

## 6. The Dave decision queue: eight questions

Ordered by how much each unblocks. Rows are counted once, in the first decision that settles them (`decisions.py`); the union of the eight is 305 of 746 rows. Each is written as he would be asked it.

D1. The Friday deck is done. May I close every deck, drawing and presentation row, and the handoffs and dossiers whose close is "Friday's deck is final", keeping every file? And what came back from Friday?
Recommended: yes. The files stay; only the rows close. Answer the Friday question in one line so the presentation strand can be closed or reopened on his words.
Unblocks 95 rows (54 of them Dave's) and 58 carries.

D2. Questions put to you on filed reports more than two weeks ago and never answered: may I park them, each with a tripwire that reopens it when its component or strand is next touched, instead of carrying them open?
Recommended: yes, park rather than drop. Parked costs a session nothing (`_state.LIVE_STATES` excludes it) and loses nothing. Anything you still care about you name in one line, and it stays open.
Unblocks 105 rows, holding at least 250 named questions (ESTIMATED share of the 383).

D3. Spider v1.0.13 shipped on 11 September. May I close every ratify, cut and cold-test row for v1.0.1 to v1.0.12 as superseded, cut v1.0.14 from today's tree this weekend (it is armed and version-gated), and hand you one cold test? Which pack is on your work machine?
Recommended: yes to all three. Carry ⑥ at age 24 says the v1.0.14 cut is "armed, version-gated and un-fired". `_HANDOFF-154` says the email bundle's pack is older than the tree, with seven commits since.
Unblocks 23 rows (21 not counted above).

D4. The window and boot lines. Do I inscribe your three window messages as rulings? Do the stop and tolerance lines move to 236,000 and 276,000? Does `BOOT_CEILING_TK` move to the measured cloud-seat boot (about 128,000, shrink-only from there), so wraps can go through `--wrap` again?
Recommended: yes, yes, and yes at 130,000. His words already point there: "okay what we'll do is just raise the ceiling until we do the Mac seat fix" (#301), and "I can't cut anything else permanently, this is possibly the new ceiling" (s295-D3). The regime is already red on six cloud readings.
Unblocks about 20 rows and 39 carries (the fill and boot series), and ends the declared not-a-wrap path.

D5. The fourteen legacy items with no close condition: take the proposed condition or disposal for each (section 7) as one batch?
Recommended: yes. Three close outright (W-10 done at #64, W-09 superseded by s204-D1, W-12 dropped). Four fold into rows that already exist. The rest get a checkable close.
Unblocks 14 rows, and lets `LEGACY_IDS` shrink, which its own comment says is the only direction allowed.

D6. The component and Layer-2 waves built at #209 to #210 and never ruled (wave-3's nine, wave-4's heavy seven, and the review surfaces over them): park them until the Apollo-MCP catalogue or the one-shot needs them, or sit with them now?
Recommended: park, with the tripwire "reopen when the catalogue lists the component". Focus has moved to bento, the one-shot and MCP; a 37-day-old eye pass on 43 components is the most expensive sitting on the list.
Unblocks 12 live rows (7 not counted above).

D7. Seventeen of your rows are closed by an event that has already happened (a wrap landed, a report was filed): may I close them with the receipt?
Recommended: yes. These are records, not questions.
Unblocks 17 rows (8 not counted above).

D8. Two CI and carry-hygiene questions. Should `_gen_chain.py --check`, red on every pushed tree by construction, stay blocking in CI or go advisory there and blocking only at the wrap? And may the next wrap drop struck, boilerplate, fragment and repeated-series items from the residual (they stay in `_CARRIES.md` history), keeping one line per recurring series?
Recommended: advisory in CI and blocking at the wrap, then yes to the carry diet.
Unblocks: CI can then read green, which Lane C needs; 342 of 709 carries leave the live residual.

Two questions I did not fold in, because they are his and small: moving the GitHub token out of the remote URL into a credential helper (carry ③; recommended yes, before any weekend push), and the Apollo-MCP proposal headline (`_HANDOFF-154` owed 1, lanes A1 and A3).

---

## 7. The fourteen unconditioned legacy items, named

All fourteen are owned by claude (owner inferred at #88), with `home` pointing into GOOD-MORNING's DOFIRST, and "Each needs Dave's word, not an agent's guess" (`_state.py`). The proposed dispositions are mine. The ones marked ESTIMATED rest on the record's later text, not on a probe of the tree.

1. W-0b — "★★ ENCODE BEFORE THE WAVE" (born #27). Chart encoding gaps; brief at `notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md`; finding 1 "measured not fixed". Proposed close: when finding 1's remedy is ruled, or ruled superseded by the #259 and #260 chart engine (ESTIMATED to be superseded).
2. W-01 — "ds-018 C2 follow-through". C2 was ruled and enacted at #121 (s121-D1); the remainder is his mark-map values and ds-018's own render proof. Proposed: fold into W-99 (the s212-D1 disabled-grey enactment) and close with it.
3. W-02 — "dv-legend/dv-behaviour CEILING". The group sat at 32,690 of 32,768 B at #80. Proposed close: when the page-budget rulings (s250-D1, s260-D1 "core priced once per page") are confirmed to replace the ceiling (ESTIMATED).
4. W-03 — "ds-012(b) gutter-relative plot area". Proposed close: Chart-bar renders the real HSBC labels unclipped at the narrow floor, render-proved, and Dave's eye passes the floor.
5. W-04 — "DV-D16 floating growth". Wording ② was enacted on Chart-bar at #218 (W-142), and on 2 of 3 stacked surfaces (W-175). Proposed: fold into W-175 and close when the third surface carries it.
6. W-05 — "Instrument-fit remainder". Part (5) is done (#66); part (2) is ruled and unbuilt; part (4) is a discussion he wanted. Proposed: park (2) with a tripwire, turn (4) into one question, close the row.
7. W-06 — "ds-016, UNRULED". Its remedy (a) is s114-D2, ruled and not built (it is in the rulings store's not-enacted list). Proposed: fold into the s114-D2 enactment and close.
8. W-07 — "ds-017, UNRULED" (a floated item that supersedes a standing instruction has no path into the handoff). Proposed: ruled superseded by the task store and the strike-by-addition regime (s183-D1 and s188-D2) (ESTIMATED).
9. W-08 — "STILL OWED, unchanged, none superseded" (six sub-items from #62). Proposed: split any still-live sub-item into its own conditioned row, and close the bundle.
10. W-09 — "DELEGATION TOPOLOGY, UNSCOPED" ("Dave wants RESEARCH, not a guess"). Proposed: close as answered by s204-D1, the PM topology "ADOPTED WITH FOUR AMENDMENTS".
11. W-10 — "✅ PER-GATE TEST PLAN". Its own body says "CLOSED #64 … 9bc34af". Proposed: close.
12. W-11 — "THE 2c-ROLL / INDEX-VOCABULARY DEADLOCK" ("an unreachable cap, HIS"). Proposed: close when W-17's "rolls retired" lands, or rule it superseded now.
13. W-12 — "THE #57 1b DOSSIER — STILL OWED". A July narrative. The only #57-era dossier on disk is #58's (`_DECISION-HISTORY/2026-07-30-the-ritual-and-the-two-stale-clauses.md`). Proposed: drop.
14. W-13 — "/tmp RUNBOOK EXPOSURE, UNFIXED". The three runbooks still mention /tmp (measured grep counts 2, 7 and 47). Proposed close: no runbook instructs a write to /tmp, and a grep arm in a gate proves it. Claude-doable once the condition is his.

---

## 8. Limits of this reading

- Theme is keyword-matched (see the header). Kind is matched on the title. Close type is matched on the `closes_when` text, and about one row in fifteen that needs Dave was first misread as a build until the pattern was widened (the "BUILD" count fell from 110 to 73 after the fix). All three are regenerable by `analyse.py`.
- `verify.py` proves an event happened from git subjects and file existence. It cannot see chat, so the "relayed to Dave in chat" halves are unproven.
- I did not read or write Project memory. Whether the #296 and #297 hooks were placed is therefore unknown here: their files carry no receipt.
- The rulings store's `status` is free text: 424 bare "ruled", 106 "enacted" in free text, 23 "not enacted" in free text, and the rest other. Which rulings are enacted cannot be computed without the audit Lane E starts with. s131-D1 is proof that the flags are stale.

---

## Files

- `notes/_subreports/2026-09-26-304-A2-open-work-analysis.md`: this report.
- `notes/_lanes/304/A2/live_clustered.json`: every live row with kind, theme, close type, age in sessions and days, horizon.
- `notes/_lanes/304/A2/verify.json`: every live row's close-event verdict and receipts.
- `notes/_lanes/304/A2/autonomous_close_candidates.json`: the 93 Claude-owned rows with receipts.
- `notes/_lanes/304/A2/dave_queue.json`: the 482 Dave-close rows with the act each needs and its named question count.
- `notes/_lanes/304/A2/decision_unblocks.json`: row ids per decision D1 to D8.
- `notes/_lanes/304/A2/carries304.json` and `carries_classified.json`: the 709 carries, split and classed.
- `notes/_lanes/304/A2/summary.json`: headline counts.
- Scripts: `analyse.py`, `verify.py`, `daveq.py`, `carries.py`, `decisions.py`; inputs `gitlog.txt`, `live_titles.tsv`.
