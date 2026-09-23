# WRAP BRIEF — #301 — 2026-09-23 (Wed) — conductor Opus 5.5, CLOUD seat linked to Dave's computer

Opened under the v2 Project instructions (first real test): one shell call · `_HANDOFF-151` · `_CHAIN.md` · NO Project memory read or write while live. `ensure_env.sh` OK. Nothing was read from or written to memory by the conductor or its lane.

## HIS WORDS — VERBATIM, BST (quote, never paraphrase)

> 19:11 — Boot probe, not a session. Do not run the start-of-session steps, and do not touch Project memory or the repo. Run this one command in your own shell and reply with its three lines only: (his python one-liner) → reply `BOOT 126767` · `LOADED 0 {}` · `MEMORY LIST AT BOOT True`

> 19:14 — Good Morning!

> 19:26 — 1. no chapter mention on the index, thats fine
> 2. this  is fine for Friday
> 3. don't worry about this
> 4. can you surface that doc again for me, 'judgement' is correct
> 5. Yes lets not worry about that until tomorrow

(Answering the conductor's numbered polish list: 1 = "The ask" has a chapter on the rail but no line in the order of play on 02 · 2 = the laptop headlines on 07 and 08 · 3 = whether 07, 08 and 13's graph rest at −27 like 09 and 10 · 4 = the 26 unanswered review suggestions, and judgment or judgement · 5 = the demo brief.)

> 19:37 — The memory list wasn't sent again. what is this?

> 19:39 — I cant work like this though

> 19:45 — okay what we'll do is just raise the ceiling until we do the Mac seat fix, hopefully there wont be too many consequences. let just use subs to stretch the window as much as possible.
>
> Lets try 300k and cross our fingers

> 19:47 — 1. is right, might be a good experiment.

(Choosing option 1 — the WINDOW's hard line to 300K — over option 2, the boot ceiling `BOOT_CEILING_TK`, which stays 72,768 shrink-only; the declared not-a-wrap path stays until the Mac seat.)

> 20:21 — 200k isnt enough make it 256

(Answering whether the mechanical-only band should run to 300K: the WORKING line to 256K.)

> 20:57 — okay do we have room to do ant work?

> 20:58 — lets just wrap then

## THE FACTS

1. **THE NEW OPENER, MEASURED (owed item 2 of `_HANDOFF-151`)** — hand sum over `/root/.claude/projects/-home-claude/74cdcbf9-60d1-5cdc-b597-746ee64610b0.jsonl`, input + cache creation + cache read per distinct message id: boot **126,767** (#300: 126,185) · 128,311 when "Good Morning!" landed (his probe turn ~1.5K) · 154,294 after handoff + chain + dave-voice skill · 162,688 after a read of slide 15 · **163,380 going into the first reply** (#300: 184,309; page projected ~156,300) · **187,604 after his first message** (#300: 211,454; page projected ~161K) = 163,380 + that reply's output 24,060 + his message ~164 ⇒ **NO memory re-send** (his v2 instructions work on that front). ⛔ **NEW FINDING: the conductor's own reasoning STAYS in the window** — the reply's 24,060 output (~22K of it reasoning) carried forward whole; conductor output 45,995 over the first nine calls. **240,294 at 20:57** (21 calls). The boot figure did not move.
2. **HIS PROBE:** `LOADED 0 {}` is a blind line — this transcript has no `prompt_snapshot` record carrying tools; `MEMORY LIST AT BOOT True` = the ~19K is still inside the boot (the v2 instructions stop the re-send, not the boot copy).
3. **JUDGEMENT (his 19:26 item 4)** — the only "Judgment" in the deck, slide 12's plate title (`<h3>Judgment</h3>`), changed to "Judgement" in the SOURCE `notes/_lanes/296/C/v14-plain-before-c.html`; deck rebuilt by `build_c.py` (530,658 B); proof: new deck == old with that one swap reversed (delta 1 char); judgment 0 / judgement 4 in both files. NOT rendered. UNCOMMITTED.
4. **THE REVIEW SURFACED (19:26 item 4)** — `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain-REVIEW.html`; the 26 unanswered by number from lane R's reconcile O9 (`notes/_subreports/2026-09-23-299-R-reconcile-decided-changes.md`): copy 18–28, 31, 32, 34 · type and style 9, 10, 11, 12, 13, 37 · after Friday by the review's own label 7, 14, 15, 16 · on the day 35, 36. He picked none yet.
5. **THE WINDOW LINES MOVED (19:45 · 19:47 · 20:21)** — lane G (one Opus helper, resumed once): `BUDGET_HARD` 256,000 → **300,000** and `BUDGET_WORKING` 200,000 → **256,000**, both PICKED by Dave #301 with his words quoted, old SOURCED text kept; `BUDGET_AMBER` 160,000 and `BOOT_CEILING_TK` 72,768 UNCHANGED. `_capture_gate.py` pin → `(160_000, 256_000, 300_000)`, test cases moved; `_seam.py` / `_recall_probe.py` docstrings; `_standing.md:19` updated with his three lines (291 tokens, under the 300 limit); runbook by dated addition; `_memento-index.json` rebuilt. Gauge + seam selftests and the budget checks PASS (mutation back to old values fails them); full `_capture_gate.py --selftest` still fails ONLY the 4 inherited s282-D2..D5 evidence-pointer checks; `_recall_probe.py` selftest flaky on the unedited file too. Report: `notes/_subreports/2026-09-23-301-G-hard-line-300k.md` (+ § Follow-up). UNCOMMITTED.
6. **UNANSWERED, PUT TO HIM (20:21 reply):** the stop line (180,000) and tolerance line (220,000) now sit under the 256K working line — move them to 236K and 276K (same offsets)? No answer before "wrap". Carry it.
7. **CLOSED BY HIS 19:26 WORDS** (strike by addition with receipts, `_HANDOFF-151` owed items): 8 ("The ask" on 02 — no chapter mention on the index, fine) · 3 (07/08 laptop headlines — fine for Friday) · 4 (07/08/13 at −27 — don't worry) · 6's second half (judgement is correct — enacted, fact 3; the 26 stay open, surfaced) · 5 (demo brief — tomorrow, NOT struck: deferred). The chain's delta says "−35" where the handoff says "−27" — now moot, note it.
8. **STILL OPEN, FIRST FOR #302:** ⬛★★★ the ask on slide 15 — asked at the opener twice this session, unanswered; still stamped Draft ("Help and support to develop it further"); Friday 2026-09-25 · the demo brief (tomorrow, his word) · which of the 26 suggestions · the stop/tolerance lines · everything else in `_HANDOFF-151` owed 7, 9–14.
9. **ROUTING:** conductor Opus 5.5 at max reasoning effort in the cloud; one Opus helper (lane G). Conductor practice adopted this session after fact 1: keep own reasoning short, send edits/renders/checks to helpers.

Title the next chat: `Apollo - #302: the ask on slide 15 and the demo brief`
