# #306 lane U — his six wrap-redesign answers inscribed, and his bloat question measured

session: `#306` · 2026-09-28
window: lane U (Opus 5.5, at Dave's seat through device bash)
sub index: `U`
brief: the conductor's launch message (verbatim in the conductor's transcript); his export `notes/_lanes/306/DAVE-RULINGS-2026-09-28-wrap-redesign.md` (16:01 BST)
provenance: 306 · 2026-09-28
status: observed
tokens: UNMEASURED — this seat cannot read its own transcript while it is still growing

His words, verbatim from the export: "lets go with all the recommendations, one thing to check is whether this bloats anything else, we used to have a running tally I think but it bloated the boot"

## VERDICT

DONE. Six rulings `s306-D4`..`s306-D9` inscribed, status `ruled` (705 → 711). The bloat check is measured below. In short: phases 1, 2 and 5 add nothing to the boot, and phase 5 shrinks the repo a lot. Phases 3 and 6 can grow the boot through the generated handoff. Phase 6 can also grow the conductor's window through the seam. Both risks are the same shape as the thing that bloated the boot in July, and both have a cheap guard. The guards are proposed, not ruled.

## 1. The bloat check, in plain words

### What a cold opener reads today (measured, tiktoken cl100k; `notes/_lanes/306/U/measure.py` → `measure.json`)

| term | bytes | cl100k | source |
|---|---|---|---|
| newest handoff `_HANDOFF-156-…md` | 25,270 | **8,106** | measure.py |
| `_CHAIN.md` (whole file) | 24,974 | **7,906** | measure.py |
| — of which GM header + ★ LATEST banner | 18,792 | 5,942 | slice at `## ⏱ LATEST DELTA` |
| — of which the LS ⏱ LATEST delta | 4,508 | 1,513 | slice to `## ⬛ OPEN WORK` |
| — of which the generated open-work block and footer | 1,674 | 451 | slice |
| first turn (system prompt, tools, memory instructions and listing) | — | 127,826 ± 1,742 **real** | `python3 knowledge/_gauge_tokens.py`, DERIVED band #298–#304 |

Real tokens for the two disk files are not measured here: the gauge fell back to cl100k (no API key reachable at this seat). The gate's own ratio is ×1.57 and is marked PROVISIONAL in its output, which puts them at roughly 12,700 and 12,400 real. That is an estimate, not a reading.

Three things this table shows that nobody had written down:

1. **The handoff is the largest disk term at boot, and nothing gates its size.** The gauge's boot figure (`measure_boot` in `knowledge/_gauge_tokens.py`) counts `_CHAIN.md` and the first turn. It does not count the handoff, although the Project instructions have the opener read it first. There is a cap on the ★ LATEST banner (`s241-D2`, 1,200 cl100k, `knowledge/_capture_gate.py:1099`) and an advisory cap on the chain (`CHAIN_BUDGET_TK = (7700, 10000)`, `:1208`), but there is no handoff cap in `_capture_gate.py`.
2. **The handoff has been growing on its own.** It was 4,880 B / 1,561 cl100k at #127 (`_HANDOFF-127`), peaked at 42,385 B / 12,515 at #145, and is 25,270 B / 8,106 now. The last ten (#147–#156) run from 4,717 to 8,106 cl100k, and #156 is the largest of the ten. 1,659 cl100k of #156 (20%) are two post-wrap addenda (5b, lane L), written after the wrap.
3. **The chain is already over its advisory warn**: 7,906 against 7,700 (7,907 after this lane's regen) (it was 7,541 at #305's pre-wrap gate, `notes/_lanes/305/W/_gate-prewrap.log`).

### Phase by phase

| phase | (i) boot | (ii) conductor window | (iii) repo / CI | (iv) generated views |
|---|---|---|---|---|
| 1 · the mechanics become permanent tools | no | no; the wrap seat's own window shrinks (8 to 11 re-authored scripts, 280–394 lines a wrap, gone) | a one-time set of tools and self-tests. The per-wrap scripts stop. CI gains the self-tests' seconds (unmeasured until built) | adds `FACTS.json`, a few KB a wrap |
| 2 · summary at the push, no second CI wait | **small, and only if bounded.** The next opener gains one CI read. The run summary is 301 bytes (`notes/_lanes/305/W/_ci-runs-eb2630bb.txt`). The gates log is 510,368 bytes (`_ci-gates-W.log`), which must never be read raw | no | no change: the same commits and CI runs | the 5b addendum (1,277 cl100k of #156) can leave the handoff |
| 3 · one story, every view generated | **yes, a real risk.** The generated handoff is on the boot and has no ceiling. See below | no | adds `STORY.md` (≈35k chars, the page's estimate) a wrap. Removes the ≈20k-char memory body written three times. The new freshness arm costs seconds per gate run if it checks the newest wrap only, and grows with every session if it re-checks every past wrap | **yes.** The handoff, banner and delta sizes are now whatever the generator emits |
| 4 · three seats | no | **a little.** Three briefs and three returns instead of one of each. Today's one brief is 1,683 cl100k (`notes/_lanes/305/WRAP-BRIEF.md`) | no. Quota, not window: each seat pays its own start-up. Unmeasured for #303–#305. #292 measured 115,674 for the wrap seat plus 85,536 for a second commit seat (`notes/_subreports/2026-09-28-306-R-wrap-redesign.md`, UNPROVEN 1) | no |
| 5 · carried items written as changes | no (`_CARRIES.md` is not on the chain) | no | **shrinks a lot.** `_CARRIES.md` is 37,018,756 bytes, grows 368,624–803,996 chars a wrap, and `_capture_gate.py` reads it (9 references). After: a few thousand a wrap | **a risk only if** the generated full list is written to a committed file every wrap. That is the same copy again |
| 6 · wrap as you go | **no, if the draft stays off the chain.** It lives at `notes/_lanes/<n>/W/STORY.md`. The opener reads only the newest `_HANDOFF-*.md` and `_CHAIN.md`, and `_gen_chain.py` reads GM and LS. The draft reaches the boot only through what the generator copies from it into the handoff | **yes, if the seam prints it.** `_seam.py`'s output is quoted in chat at every seam, about five a session (`notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md:43`) | a small file, committed with the wrap | **yes.** His words and the tally flow into the handoff |

### The generated handoff: could it grow larger than today's?

Yes, on two paths. Both are arithmetic from today's files, not a run.

- **If the generator renders the whole story into the handoff.** The page estimates ≈35k chars of hand-written story per wrap. At #156's own density (24,845 chars / 8,106 cl100k = 3.07 chars a token), that is ≈11,400 cl100k, **about 40% over today's handoff.** If it renders only the sections today's handoff carries, it lands about where it is: 6,447 cl100k before the addenda.
- **If phase 6 copies his page exports whole into the story.** #305's three `DAVE-RULINGS-*` exports are 36,176 B / 11,453 cl100k (the machine copies included). Rendered under "his words", they would take the handoff to about 18,000 cl100k, **more than double.** Today's handoff carries his words in 306 cl100k (`## ⛔⛔ HIS WORDS`).
- **The tally.** Today's delta is 1,165 cl100k (`notes/_lanes/305/W/_work/delta_305.txt`). If the seam appends a delta-so-far at each of ~5 firings, the draft holds ~5,800 by the wrap. If it replaces the block in place, it holds ~1,165.

The same design can also make the handoff **smaller** than today's. Every view is cut from one source, so nothing has to be told twice, and the post-wrap addenda become generated lines.

## 2. The old running tally: what it was and what it cost

**The record never calls the boot-bloating thing a "running tally".** The only "running tally" in the record is the context gauge's in-head estimate (`knowledge/_RUNBOOK-context-gauge.md:523`, "Half 1 — cheap, always-on: the running tally (near-free)"; `knowledge/_context_gauge.py:5`). It is kept in-head and costs nothing at boot. `_memento_search.py` returned no record for "running tally", "tally", "delta so far", "boot diet", "boot bloat", "LS growth", "⏱ delta" or "chain diet" beyond the GM and LS section headers (`notes/_lanes/306/U/search1.log`).

**What matches his memory is the per-session running record that every opener read whole**: the ⏱ delta stack in `_LIVE-STATE.md` and the stratum stack in `GOOD-MORNING.md`. Each session appended to them, nothing rolled them, and the read chain told every session to read both files end to end.

- **The delta stack.** Roll rule 2d was born 2026-07-26 (dream pass P1). `knowledge/_RUNBOOK-capture-ritual.md:300–301`: "First roll same day cut `_LIVE-STATE.md` 205KB→62KB; it had exceeded a single Read call."
- **The stratum stack.** `notes/_briefs/2026-07-27-gm-compaction-architecture-proposal-v1.md:23`: GM "90,204 B · 910 lines … it grew **+70 lines in ~1 day**". Line 25: "~146 ln is a stratum stack". Line 34: "sessions #12, #8, #7, #6 all present". Ruled GM-D5(a) 2026-07-27 (`notes/_MEMENTO-DECISIONS.md:75`): "Stratum stack … keeps **LATEST only**; post-mortems roll to NEW `notes/_GAUGE-LOG.md`". Enacted #15.
- **The cut.** #33, 2026-07-28, on Dave's "lets do it your way" (`_DECISION-HISTORY/2026-07-28-cutting-the-eager-read-chain.md:18–19`). Lines 36–40 and `knowledge/_capture_gate.py:1175–1176`: old chain, GM plus LS whole, "34,094 tk cl100k ≈ 52,846 charged ≈ 26.4 pts". New chain, header plus ★ LATEST plus the LS latest delta, "3,410 … 2.6 pts". A 90.0% saving. Since then `_CHAIN.md` is generated and is the whole read chain (`GOOD-MORNING.md:1–5`).
- **Not found:** the session the ⏱ delta itself was born in. It predates the first roll rule.

**The lesson for this design.** What bloated the boot was not a tally as such. It was **append with no roll, in a file the opener reads whole.** Phase 6 is written in that shape: the plan's lever 4 says "append the delta-so-far and his entries verbatim to a draft" (`notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md:42–45`). The draft itself is off the boot. What reaches the boot is whatever the generator copies from it into the handoff, and the handoff has no ceiling. Today `_LIVE-STATE.md` is 203,555 bytes again, the size that broke a Read in July, but it has been off the chain since #33.

## 3. Proposed guards (PROPOSED, NOT RULED; each a gate arm)

1. **The story draft is never on the boot chain** (phase 6). The arm fails if `_gen_chain.py` reads any path under `notes/_lanes/`, or if a draft is ever named `_HANDOFF-*.md` (the opener's glob).
2. **A ceiling on the generated handoff** (phase 3). 25,270 B / 8,106 cl100k, which is `_HANDOFF-156` whole and the largest of the last ten. Block over it. Also count the handoff in the gauge's boot figure beside the chain.
3. **The tally is one block, replaced, never appended** (phase 6). The arm fails on a second tally block, or on a block over 1,513 cl100k (today's delta in the chain).
4. **His words enter the draft verbatim as free text with their times. Page exports are cited by path, never copied** (phase 6). The arm warns when the words section passes 3,000 cl100k.
5. **The seam prints one line for the draft** (bytes added, draft size), never the draft (phase 6). A bite checks the line count.
6. **The chain takes nothing new from the story** (phase 3). Only the banner (still under `s241-D2`'s 1,200) and the delta (capped at 1,513) are generated into it, and the M10 warn stays as it is.
7. **The freshness arm checks the newest wrap's views only** (phase 3), so CI time does not grow with every session.
8. **The opener's CI read prints the run summary** (the 301-byte form), never the gates log (phase 2).
9. **Seat returns are one line each for the story and mechanics seats; only the commit seat reports. One shared brief plus a short line per seat** (phase 4).
10. **The full carried list is generated on read, to stdout or a gitignored file, never committed per wrap. `_CARRIES.md` grows at most 20,000 bytes a wrap** (phase 5; the number is picked, not ruled).
11. **The generated memory note stays one file per wrap**, so the memory listing the harness loads grows by one row a wrap, as today (phase 3).

## 4. The rulings (Job 1)

Inscribed through `knowledge/_inscribe_ruling.py`, dry run first, one write per call, reconstruction proof passed on each (`notes/_lanes/306/U/inscribe-dry.log`, `inscribe.log`). Built by `notes/_lanes/306/U/build_entries.py`, which reads his answers and words from the export and never retypes them. Eight keys only.

| id | his answer, verbatim | enacted by |
|---|---|---|
| `s306-D4` | "a · Yes, story plus measured figures, all views generated", plus his free-text words verbatim in `says`, citing W-305wr | phase 3, built on phase 1 |
| `s306-D5` | "Yes" (a generated wrap report counts as the filed report, `s218-D7`) | phase 3 |
| `s306-D6` | "Yes" (three seats) | phase 4 |
| `s306-D7` | "a · Yes, the next opener reads the follow-up's CI" | phase 2 |
| `s306-D8` | "Yes" (carried items written as changes) | phase 5 |
| `s306-D9` | "Yes, in a later phase" (seam writes to the story draft) | phase 6 |

All are `ruled`, not `enacted`: the build is six phases, each proven on a real wrap. W-305wr gains, by addition, a paragraph saying the design was ruled at 16:01 BST. It stays open: its `closes_when` is a wrap run on the redesign.

## 5. Store and commit

- The store is written through `_state.load → check → save`, by addition (`notes/_lanes/306/U/store_batch.py`). W-305wr gets its body paragraph. Two rows are born closed (`s305-D40`, `DOC_BIRTH_FROM_SESSION = 306`): W-306r (lane R's report, linking the decision page, the export and `notes/_lanes/306/R/`) and W-306u (this report).
- The commit carries lane R's report, `notes/_lanes/306/R/` whole (21 files, 6.6 MB; the largest is a 1.26 MB render, under #305's committed 3–5 MB logs, so nothing is held), the decision page, his export, this report and `notes/_lanes/306/U/`. Backups under `notes/_lanes/306/U/backup/` are held.

REPLAY-THESE: `python3 notes/_lanes/306/U/measure.py` · `python3 knowledge/_gauge_tokens.py` · `python3 notes/_lanes/306/U/build_entries.py`
