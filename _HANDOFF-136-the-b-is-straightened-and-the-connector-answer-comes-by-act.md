# HANDOFF #136 — #285 → #286 — THE B IS STRAIGHTENED AND THE #284 ACCEPTANCE IS REOPENED BY DAVE HIMSELF; THE SEAM RE-QUOTES THE STANDING CONSTRAINTS; THE CONNECTOR ANSWER COMES BY ACT

provenance: 285 · 2026-09-18
status: observed

*Written by the delegated OPUS 5 wrap sub at the close of #285 (conductor Fable 5.1) — on the
SECOND attempt, the first sub having died mid-ritual on a network error. Every figure here was
MEASURED at this seat unless it says otherwise; where a measurement disagrees with the brief's
declaration, both readings are published and neither is rewritten.*

✅ **NO DATE SPLIT.** #285 opened, ran and wrapped inside **2026-09-18**.
⛔ **NO RULING WAS INSCRIBED. `knowledge/_rulings.json` STAYS AT 620**, verified here by
`json.load` over the `rulings` list.

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-135`.** Every open item on those six still stands
   except the two closed below, each with a receipt. **Strike nothing else without one.**
4. `notes/_lanes/285/DAVE-RULINGS-2026-09-18.md` — his words, verbatim. **Quote them; never
   paraphrase them.**
5. `_CARRIES.md` § `residual → #286` when you need the bodies — **543 probeable items**. Do not
   read it at boot; fetch the section (`_memento_search.py` → `--fetch carries:residual-286`).

---

## ⛔⛔ DAVE'S — VERBATIM

- *"the scaling is wonky"* — on the #284 contact sheet, with the 4× shots.
- *"Is thre anything here we can use"* — with a pasted research note on the *lost in the middle*
  phenomenon.
- *"Maybe we misunderstand each other on the logo scaling, see image the word mark is distorted,
  look at the B"* — with a 4× crop. ⛔ **This is him REOPENING HIS OWN #284 ACCEPTANCE.**
- *"Okay this sound good."* — to the read that only tactic 1 (front-load rules, re-quote
  constraints at the tail) is usable in Cowork.
- **"go on both this and: yes to the seam re-quoting the standing constraints"** — the two lanes.
- *"excellent work!"* — on the regenerated masters, the STANDING block and the 16/16.
  ⚠ **ENTHUSIASM, NOT A RULING** (`s271-D4`).
- **"1. go"** — the showroom re-sync, cut as its own commit lane.
- **"2. accept"** — ⛔ **THE REGENERATED MASTERS ARE ACCEPTED BY EYE.** This replaces the #284
  acceptance he reopened himself. The `_standing.md` wording is NOT covered by it.
- *"what about the context management part?"* · *"this is how the setup stand now"* · *"I havnt
  touched anything and computer use is off"* · *"but deep research might be useful no? is it big"*.

**Still his, by his own words:** the wording of the eight lines in `knowledge/_standing.md`
(DRAFT); **HOW** the accepted masters get registered in `_logo_nodes.json` (the `gen_kg_icons.py`
fence).

---

## ★ WHAT LANDED — 2 commits, both UNPUSHED when this ritual opened

| sha | what |
|---|---|
| `b99d092c` | the LM2 masters regen + the SC seam STANDING block |
| `ff354475` | the showroom re-sync — 108 pages, `:is(` → `:where(` — and the `W-285lm` row amended with his acceptance |

Remote stood at `77b491b8` (#284's post-wrap addendum). Lane P's push **refused, correctly**, on
a dirty tree; this wrap's own commit and push close it. **This wrap's sha, the push verdict line
and the CI read are in the ★ LATEST banner and the filed report** — a commit cannot name itself.

---

## ★★★ THE MASTERS — DISTORTED, REGENERATED, RE-ACCEPTED, STILL NOT REGISTERED

**#284's acceptance was reopened by Dave, not by us.** The crop showed it; the code confirmed it;
there were **two** causes, not the one he named:

1. **per-node snapping inside curved glyphs.** Every on-path node in a straight `H`/`V` run inside
   S, B and C was rounded to whole pixels while its **cubic control points** stayed scaled only. A
   bowl leaves the stem at such a node; move the node and leave the handle and the curve kinks at
   the join and flattens on the way out.
2. ⛔ **the wordmark was never scaled uniformly.** `kx = (W-Lx)/(R-L)` and `ky = capH/(B-T)` were
   used on the two axes. `kx/ky` measures **1.0039 / 0.9949 / 1.0436 / 0.9949 / 0.9896** — at
   **h=32 the wordmark was drawn 4.4% wider than tall**, independent of any snapping.

⚠ **Why #284 could not see it: its probes counted anti-aliased pixels and stem runs, and neither
instrument has an axis for an aspect error.** The acceptance was a claim published at the
resolution the session could measure, and his eye had a higher one.

**The fix is a subtraction.** `quantise_runs()` **deleted** (32 lines); `snap_wordmark()` rewritten
43 → 30 lines as a **rigid move** — one uniform scale `s = h/85` (the hexagon's own factor, so the
lockup relationship stays exact) plus one translation applied to **nodes AND control points**
through the existing `coords()` iterator. `snapped_nodes` is `0` **and the report asserts it**. The
H was **not** exempted. The 20 `hexagon-*` masters are **byte-identical to HEAD**.

**Lane V, adversarial, 16/16 PASS** — max residual **5.4e-5 px** against the Figma source. Two
caveats carried (one wording, one a sub-pixel property inherited from the source); neither a
defect. ★ **The commit lane was cut on THAT pass, not on his *"excellent work!"*.**

⛔ **NOT REGISTERED IN `_logo_nodes.json`.** The `gen_kg_icons.py` fence stands, **HOW to run it is
his word**, and row `W-285lm` stays OPEN with `closes_when` UNCHANGED — the eye-half is recorded
in the row's `body`, not by inventing a close condition.

---

## ★★ THE SEAM RE-QUOTES THE STANDING CONSTRAINTS — AND THE FILE IS A DRAFT

His two words cut the lane; the finding behind them is the reason it is at the TAIL. Everything a
session reads at its opener — handoff, chain, check-in, ~80K — becomes **the middle** of the
context the moment work starts, and standing rules buried there drift out of attention (U-shaped
attention / lost-in-the-middle). `_seam.py` already runs before every lane is cut and after every
lane lands. So it now prints a **FOURTH block, LAST, after SCRATCH** — the recency end.
**Position IS the mechanism**, and the docstring forbids moving it above SCRATCH.

```
STANDING
<the eight lines, verbatim>
STANDING 8 lines · 246 cl100k
```

`--no-standing` suppresses it; a missing file prints `ABSENT` and still exits 0; an unavailable
tiktoken prints `?`, **never a guessed number**, and the selftest FAILS on `?` rather than passing
a blind arm.

⛔ **`knowledge/_standing.md` IS A DRAFT — its own header says so — and the WORDING OF THE EIGHT IS
HIS, LINE BY LINE.** Each was drafted **from the record** with its receipt in parentheses. **The
seam re-quotes; it never inscribes.** Row `W-285sc` closes on his word.

⚠ **And the block's counter was born unregistered** — see STRUCTURAL REDS below.

---

## ⛔★ THE CONNECTOR ANSWER CAME BY ACT — #286'S FIRST MOVE IS A MEASUREMENT

#284 asked *which connectors Apollo needs* and carried it unanswered. **He answered it in the Tool
permissions panel: the built-in Browser's SEVENTEEN tools are set to BLOCKED**, and the
`mcp__Claude_Browser__*` server dropped out of the conductor's tool set inside the same session.

⇒ ★ **#286 OPENS WITH A READING, NOT A LANE: measure boot COLD and compare against today's
80,863 real. ONE variable changed.**

⚠ **Skills are untouched BY DESIGN** so the cause is unambiguous if the figure moves; a second run
follows only if the first one does. His setup as he described it: connectors Browser (now
blocked), Claude Docs, Claude in Chrome, GitHub; skills dave-voice, dream-pass,
swiss-design-system, gtb-brand (off), docs, deep-research, import-memory; computer use OFF.
deep-research was **kept** — a skill costs its description only, ~80 tokens.

⛔ **`BOOT_CEILING_TK` STAYS 70,000 AND IS SHRINK-ONLY.** Today is the **TENTH** post-diet reading
over it. **Cut the boot; never raise the literal** — raising it is his word alone.

---

## ★★ THE DELEGATION RULE WAS OBEYED — MEASURED, NOT ASSERTED

#284's carry ① is Dave's own sentence about delegation, ruling-shaped and uninscribed. #285 is
the counter-measurement, taken at this seat from the conductor's transcript:

**SEVEN lanes, every one an `Agent` at `spawnDepth 1`, model opus** — LM2 (masters regen, 154,244)
· SC (seam standing, 89,857) · V (verifier, 117,752) · C (commit, 113,858) · C2 (showroom commit,
94,747) · P (push, 77,788) · W (this wrap; its first attempt died at 90,605). **No lane work was
done in seat.** The conductor's in-seat tool output was three seam reads, one tiktoken measure,
two directory listings, four image reads and one shot read.

★★ **THE PRICE, BOTH SIDES: the seven lane replies cost the conductor's window 3,382 cl100k IN
TOTAL — the `s218-D7` stub contract working — against ≈738,851 real of sub FILL.**

⛔ **THIS DOES NOT CLOSE THE CARRY.** One session's obedience is evidence that the shape is
affordable, not a rule that it is required. **Inscribing is his.**

---

## ⚠ THREE THINGS THAT WENT WRONG, AND WHAT EACH IS EVIDENCE OF

**(a) A WRAP SUB DIED MID-RITUAL AND WROTE NOTHING.** Five reads, **90,605 real**, then
`API Error: Can't reach the API server — check your internet or DNS (ENOTFOUND)` at **14:52:22Z**,
eleven usage records in. ✅ `notes/_lanes/285/W/` was empty when the retry opened and the tree
stood as the lanes left it. ⛔ **THAT IS LUCK, NOT DESIGN** — `_gm_move.py` is all-or-nothing **per
transaction**, never across the ritual. A death after a 2c move and before its receipt was read
back leaves a half-rolled banner with green receipts nobody read: the #166 stale-msgfile shape by
another door. **Whether the ritual owes a RESUME contract is ruling-shaped and NOT inscribed.**

**(b) THE PUSH REFUSED, CORRECTLY.** Lane P ran the only sanctioned path and got
`✗ push refused: tree not clean — commit first (s133-D2 …)`; the three dirty paths belonged to
other lanes and the lane was forbidden to commit. ★ **A lane that will not widen its own scope to
clear its own blocker is the lane contract working.**

**(c) `W-285lm2` WAS REFUSED BY THE STORE'S ID PATTERN.**
`REFUSED: W-285lm2: id does not match '^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$'` — at most
two trailing lowercase letters and **no digit after them**. The row is `W-285lm`. **A finding, not
fixed**: the brief named an id the store cannot hold and the store said so rather than coercing it.

⚠ **AND ONE CARRIED, NOT FIXED:** `_seam.py`'s SCRATCH arm **deletes a lane's own `/tmp` working
files mid-run, by design** (keep-list: `/tmp/gitshim` only). The lane is not the process that
cleans, so it gets no warning and no receipt. This wrap's defence was a **convention** — every ops
file, builder and msgfile under `notes/_lanes/285/W/` — **not a guard.** Changing what an
instrument removes changes what it claims, so it is named here and left to him.

---

## ⬛ #286 — FIRST MOVES, IN ORDER

1. ★ **MEASURE BOOT COLD at the opener** against today's **80,863**, ONE variable changed (the
   Browser's 17 tools blocked). A reading, not a lane. Skills untouched by design; a second run
   only if the first moves.
2. **The eight lines of `knowledge/_standing.md`** — his word, line by line, to take the file out
   of DRAFT (row `W-285sc`).
3. **Register the 40 accepted masters in `_logo_nodes.json`** — needs a sanctioned run of
   `gen_kg_icons.py`, one of the four generators that undo hand-authored state. **HOW is his.**
4. **The `_gauge_tokens.py` 256,000 wording fix** — carried from #284, his to order.
5. **The seam's in-seat arm** and **`--quiet` on `_git_commit.sh`** — #285's moves 2 and 3, still
   unbuilt; the commit ran as a lane today, which was the third of them.
6. Everything still open on `_HANDOFF-130`…`-135`. **Strike nothing without a receipt.**

---

## ⬛ OPEN, RULING-SHAPED, NOT INSCRIBED — the `s271-D4` form: every one is a QUESTION PUT

1. **The `_standing.md` wording** — eight DRAFT lines, his line by line.
2. **The masters' registration** in `_logo_nodes.json` (the `gen_kg_icons.py` fence) — **HOW**.
3. **The `_gauge_tokens.py` 256,000 wording fix** — the finding is measured; the edit is his.
4. **The delegation rule** — his sentence, obeyed today, still uninscribed.
5. **The boot ceiling** — 80,863, the tenth breach. Cut the boot; never raise the literal.
6. **The skills second run** — only if the connector reading moves.
7. **A RESUME contract for the ritual** after a mid-ritual sub death.
8. **`_seam.py`'s SCRATCH arm** — keep-list, opt-in, or lanes forbidden `/tmp`.
9. **The third dial** · **the theory door** · **`col26-012`** · **`jade-lifestyle`** ·
   **`s277-D12`** · **what a session should DO at the hard wall** · **the four generators** ·
   **the git-lock runbook line** · **the instrumentation-append policy** · **the two-probe-shape
   question on the §A digest** — all carried, all aged, none touched.
10. **Everything on `_HANDOFF-130`…`-135` not closed today.**

⛔ **CLOSED TODAY, WITH RECEIPTS, AND NOTHING ELSE:** the masters' acceptance (re-given at #285
after his own reopening — `b99d092c`, `ff354475`) and the showroom's *"108 stale"* (re-synced,
`ff354475`; **138 files remain = 137 generator-owned + `index.html`**, so 108 ⊂ 137 ⊂ 138).

---

## ⛔ STRUCTURAL REDS — inherited, measured here, NOT repairable by a wrap

**SEVEN blocking gate fails stood at this ritual's open; SIX stand at its close.**

The six are carried in the `#243` DECLARED not-a-wrap form — **the ELEVENTH consecutive wrap on
that path**. Every one is another session's append-only testimony in `notes/_GAUGE-LOG.md`:

- **boot-drift CEILING BREACH** — `BOOT_CEILING_TK` 70,000, seven post-diet readings over it
  (#277 83,636 · #278 72,110 · #279 72,447 · #280 75,740 · #281 77,400 · #282 77,474 · #283
  80,871). **The remedy is to CUT THE BOOT, never to raise the literal**, and raising it is Dave's
  word alone [[gate-must-quote-what-it-forbids]].
- **five boot double-counts** — #243 (×5), #264, #272, #273, #274.

⚠ **THE SEVENTH WAS THIS SEAT'S OWN AND IS CLOSED HERE.** `ds-021 (C)` fired on
`knowledge/_seam.py` — lane SC gave it a cl100k counting site in **this session's own commit**
`b99d092c` and nothing registered it. Entered as **`estimate-only`** (it never calls
`_gauge_tokens.count()`, has no API path, and its figure is never a FILL or budget claim), the
`_compose_slice.py` precedent from the #270 wrap. ⛔ **A DECLARATION, NOT A RULING.**
★ **The general form: a lane that adds a counter adds a gate obligation, and the gate finds out at
the wrap.**

Also standing and NOT repaired here: `carry_wording_check()` is **blind** — both residual lines
are pointers, so it has nothing to pair and goes quiet; re-pointing it at `_CARRIES.md` is OWED
(`notes/_subreports/2026-08-30-225-carries-home.md`).

---

## ⚙ THE NUMBER THIS SESSION MUST HAND FORWARD

Measured at this seat against the conductor's own transcript
`62add8e4-a016-4881-9b21-af4571354a1e.jsonl` — this wrap seat being
`agent-a1d288ef03329a515.jsonl` beneath it, which is what makes the subtraction legal
[[measure-dont-convert-units]].

| term | measured | declared at the brief cut | delta |
|---|---|---|---|
| **FILL** | **197,852 real / 31 turns** | 191,785 / 28 | **6,067** — the hand-over's cost, not a disagreement |
| **BOOT** | **80,863 real, n=1** | 80,863 | agrees to the token, **and that agreement is what identifies the window** |
| **subs** | **738,851 real (n=7)** | ≈740K across 7 lanes | agrees |
| `/sessions` | 1.7% used, 9,512,108 KB free | — | measured here |

⛔ **THE 180,000 STOP LINE WAS PASSED BY 17,852.** ✅ **22,148 INSIDE the ≤220,000 tolerance.**
✅ **256,000 clear for the third session running.** ⚠ **Per Dave's own #284 correction the 180,000
is the QUALITY line and 256,000 is not a wall for this model** — so this is a quality breach, and
**no constant moved.**

⛔ **BOOT 80,863 IS THE TENTH POST-DIET READING OVER THE 70,000 CEILING AND IS NOT A RE-BASE.**
It is also, for the first time in ten, a figure with a lever aimed at it: see the connector act.

---

## ★ NEXT CHAT TITLE

Generated by `python3 knowledge/_gen_titles.py --session 285`; the receipt is at
`knowledge/_gen_titles_receipt.json` and the line stands at the top of `GOOD-MORNING.md`.
