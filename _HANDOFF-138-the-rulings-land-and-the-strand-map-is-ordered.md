# HANDOFF #138 — #287 → #288 — TWO SENTENCES BECOME RULINGS AND THE STORE MOVES 620 → 622; THE EXPLORER READS `sizes`; THE 256,000 WALL WORDING IS SWEPT; AND DAVE ORDERS A STRAND MAP AND A PATH TO FRIDAY THE 25TH

provenance: 287 · 2026-09-19
status: observed

*Written by the delegated OPUS 5 wrap sub at the close of #287 (conductor Fable 5.1). Every figure
here was MEASURED at this seat unless it says otherwise; where a measurement disagrees with the
brief's declaration, both readings are published and neither is rewritten.*

✅ **NO DATE SPLIT.** #287 opened, ran and wrapped inside **2026-09-19** (`date` read at this seat).
★★ **TWO RULINGS WERE INSCRIBED. `knowledge/_rulings.json` MOVES 620 → 622** — the first movement in
seven sessions — verified here by `json.load` over the `rulings` list: `s287-D1` and `s287-D2` both
present, no duplicate.

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-137`.** Every open item on those eight still stands
   except the four closed below, each with a receipt. **Strike nothing else without one.**
4. `notes/_lanes/287/DAVE-RULINGS-2026-09-19.md` — his words, verbatim. **Quote them; never
   paraphrase them.** It records the conductor's own *readings* as the conductor's, and it keeps a
   framing Dave corrected **beside** his correction rather than deleting it.
5. `_CARRIES.md` § `residual → #288` when you need the bodies — **560 probeable items**. Do not read
   it at boot; fetch the section (`_memento_search.py` → `--fetch carries:residual-288`).

---

## ⛔⛔ DAVE'S — VERBATIM, AND THERE ARE THREE MOMENTS

**At the opener**, his whole reply to a three-item question:

> 1. inscribe
> 2. keep `sizes` and rebuild.
> 3. do it

**Later**, correcting the conductor's framing of lane X's spacing finding:

> The problem with the gutters it that they are deliberately different for the themes and the
> gutters are also different for the inner and outer bentos we essentially have a structural bento
> and embedded bentos or tile groupings.

**At the wrap call**, four sentences:

> I'm not sure that 0 is right for mono, lets have a proper review and fix this: 'The generation arm
> that would do that was ruled at #219 and never built.' and any other problem with this, I just
> need the one-shot design to not disappoint, however it is getting better all the time.
>
> I'm not sure about the quality of the template we need to look at this too.
>
> I want to return to the presentation soon, so I need to understand how the multiple strands of
> Apollo stand and I need a clear path to presenting something cohesive for friday the 25th
>
> wrap with all of this in mind

**And on the GPT-6 Spider handoff he brought in:** *"don't take it on face value, use your judgment,
but what it did worked."*

⚠ **ONE THING IS THE CONDUCTOR'S AND IS MARKED AS HIS:** the *"two ruled spacing sources disagree"*
framing that provoked the gutters correction. **It stands in the rulings file beside the
correction** — a correction that erases what it corrects leaves no evidence the correction was
needed.

---

## ★ WHAT LANDED — 1 commit, pushed and verified BEFORE this ritual opened

| sha | what |
|---|---|
| `75a490cd` | lanes I · K · W — 2 rulings inscribed, the explorer reads `sizes`, the 256,000 wall reworded |

✅ **ONE COMMIT, ONE INVOCATION, NO GATE REFUSAL** — the first clean single-run commit lane in three
sessions, and lane C names the cause rather than the luck: it read the prior lane's report before
calling, so `SESSION_N=287` was on the first call and the four `--check`s that have refused commit
lanes before were each driven green *before* the script ran. Push verdict, **verbatim**:

> `✅ pushed and VERIFIED: remote master == local 75a490cda77db7065c6b866ba68fbc99d9d33279`

Re-verified at this seat: `git ls-remote origin HEAD` reads `75a490cda77db7065c6b866ba68fbc99d9d33279`
against the same local HEAD. ⚠ Four paths were inherited dirty or untracked and are committed by
this wrap: lane C's own filed report (it appended its sha, push verdict and CI table **after**
committing — the lane doing the honest thing in the wrong order, second session running), the
DAVE-RULINGS file with his wrap-call words, lane X's filed report, and the GPT-6 Spider handoff
saved into the repo. **This wrap's sha, push verdict and CI read are in the ★ LATEST banner and the
filed report** — a commit cannot name itself.

---

## ★★★ THE RULINGS — AND THE JOIN IS NAMED ON THEIR OWN FACE

**`s287-D1`** — the eight standing lines of `knowledge/_standing.md` are **RATIFIED AS WRITTEN**, the
file is out of DRAFT by HIS word rather than the conductor's reading of it, the seam re-quotes them
at its tail, and the 256,000 wording fix in `_gauge_tokens.py` is his.
`governs`: `_standing.md` · `_seam.py` · `_gauge_tokens.py`.

**`s287-D2`** — a per-size master is a **SIZE FIELD on its lockup's existing node** in
`knowledge/_logo_nodes.json` (`nodes[].sizes`, raw height 24/28/32/36/40 → master record,
merge-on-write), **never its own node and never a new kind**; the node count does not move — 8 nodes
/ 33 edges at inscription, read by `json.load`.
`governs`: `_logo_nodes.json` · `assets/logos/_gen_masters.py` · `_build_kg_explorer.py`.

★ **THE JOIN IS WRITTEN DOWN RATHER THAN SMOOTHED.** Reading #286's *"okay go on everything"* as
ratification-**as-written** was the **CONDUCTOR'S** reading at #286; the word that makes it HIS is
*"inscribe"*, said 2026-09-19. Same discipline on `s287-D2`: `sizes` was lane R2's reading of the
file's own plural vocabulary until *"keep `sizes` and rebuild."* made it his word.

⇒ **This is why #286's caution paid off.** Because the inference was recorded *as* an inference and
sat next to the act it licensed, #287 did not have to reconstruct anything — the question went back
to him in one line and came back in one word.

Both were inscribed through the sanctioned writer `knowledge/_inscribe_ruling.py`, `--dry-run` then
`--write`, **reconstruction proof PASSED on each with all other bytes identical**. No hand-edit was
needed and none was made. `notes/_RULINGS.html` was re-rendered in the same change — **622 rulings /
160 sessions**, `--check` **FRESH**.

---

## ★★ THE EXPLORER READS THE FIELD — #286's "NOTHING READS IT" IS DISCHARGED

Builder `VERSION 1.26 → 1.27`; three new reads in `knowledge/_kg_explorer.template.html`:

1. the aside panel's **`MASTERS 5 · 24 · 28 · 32 · 36 · 40 px`** row (a lockup with no map says so
   in words, not as an empty row);
2. INSPECT's **RECORD** listing each height as a link to its own master SVG with its stored
   width×height and sha256;
3. a third **MASTERS** tab drawing all five at their **true declared sizes** on the lockup's own
   ground — because the whole point of a per-size master is that it is cut for that size.

✅ **VERIFIED BY PARSING THE BUILT PAGE, NOT BY EYE: all 8 `logo:` nodes carry `sizes` with 5 keys,
40 entries byte-identical to `knowledge/_logo_nodes.json`, 8 nodes and 33 edges either side, and
`_logo_nodes.json` was never written by that lane.** Every inline `<script>` re-extracted and
`node --check`ed; the three new functions executed for real against the page's own baked data.

⚠ **2,256 BAKED COORDINATES MOVED AND 11 NODES / 18 EDGES APPEARED, AND NONE OF IT IS THE FIELD'S.**
The diff names the cause itself — the new nodes are `ruling:s287-D1`, `ruling:s287-D2`, three
evidence files and three artefacts: **the Constitution growing under the build's feet** while
another lane of the same session wrote `_rulings.json`. A force layout is a function of the nodes it
is given. ★ **The lane put the node list in its report and the reason in the builder's own version
note rather than claiming a byte-identical canvas it could not have.**

⚠ **The residual, named and not taken:** a rebuild of a graph whose sources move mid-session bakes a
snapshot nobody chose. The remedy (*rebuild after `_rulings.json` lands*) is a lane ordering and
therefore the conductor's.

---

## ★★ THE 256,000 "WALL" WORDING — SWEPT ON *"do it"*, 58 → 42, AND THE 42 ARE ACCOUNTED FOR

⛔ **NO NUMBER MOVED.** `BUDGET_HARD` is still `256_000` and `STOP_LINE_TK` still `180_000`; only
the word next to each figure changed.

Lane W re-ran lane G's own probe before and after (`256,000|256000|256_000|256K` ∧ *hard*|*wall*)
across the ten live files. **Genuine wall-assertions remaining: ZERO.** The 42 survivors fall in
five named classes:

| class | n | why it still matches |
|---|---|---|
| the correction's own words (*"not a context wall"*) | 16 | matches by construction — removing it would remove the fix |
| Dave's inscribed ruling text, ANNOTATED not rewritten | 11 | rule 3 forbids a lane re-wording a ruling |
| the live constant's own name `BUDGET_HARD` | 2 | renaming it is a code change, not a wording fix |
| #286's record of the owed work, now marked `⇒ ✅ SWEPT AT #287` | 3 | deleting it would erase what #286 declared |
| a false positive on the retired `HARD_STOP` percentage constant | 1 | *"No edit; it would be a wrong one."* |

⛔ **`says` FIELDS WERE NOT TOUCHED — those are Dave's quotes.** `gauge-band`, `s161-D1`, `s214-D2`
and `s214-D4` stand exactly as inscribed, including `s214-D2`'s *"256,000 remains the hard wall,
unqualified, band or no band"* — **his own sentence**, whose `ruled` now carries the amendment
beside it. That is the point of annotating rather than editing.

**The mechanism, stated because it is reusable:** `_inscribe_ruling.py` offers `--amend-evidence`
only, and its own comment block states the fence (*"`says` is never reachable from here… an 'amend'
that could reach them is a re-stamp wearing a tool's clothes"*). The fallback is an **appended
clause** applied as a byte-level span swap carrying the tool's own proof discipline: locate by
`json.dumps`, require exactly one occurrence, replace only that literal (no `json.load → dump`
reformat), re-parse and prove the only difference is the named field of the named record. Same
discipline on `knowledge/_state.json`'s seven rows.

Generated surfaces were **REGENERATED, never hand-edited**: `notes/_RULINGS.html`,
`dashboard/index.html`, `_CHAIN.md`, `knowledge/_memento-index.json`.

⚠ **ONE PIECE IS EXPRESSLY NOT DISCHARGED:** `knowledge/_seam.py`'s four printed
**"HARD LINE BREACHED"** strings — outside the ten-file prose list, and **the one remaining printed
wall wording in live code.** Re-minted as a carry rather than quietly widened.

---

## ★★★ THE SECOND COLD BOOT — THE LEVER IS NOW A MEASURED EFFECT

**BOOT COLD 74,120 real** against #286's **73,832** on the **same setup** — **Δ +288**. Two readings
within 300 tokens of each other where the prior seven-reading spread was **11,526** wide.

⇒ **#286's OWN ACCEPTANCE TEST — *"two readings within a few hundred tokens of each other would
make it measured"* — IS MET.** The **−7,031** from blocking the built-in Browser's 17
`mcp__Claude_Browser__*` tools is a **MEASURED EFFECT (n=2)**, no longer a direction.

★ **A session honouring an acceptance test written by the session that could not pass it is the
cheapest form of rigour this record has** — and #287 took the reading *first*, before any lane was
cut, which is what made it a reading rather than a hope.

⛔ **AND IT CHANGES NOTHING ABOUT THE CEILING. 74,120 is 4,120 over `BOOT_CEILING_TK` 70,000 — the
TWELFTH post-diet reading over it.** The literal is **SHRINK-ONLY** (`s240-D2` / `s241-D1`): cut the
boot, never raise the number, and raising it is his word alone. ⛔ **THIS IS NOT A RE-BASE.**

⛔ **THE NEXT LEVER IS STILL UNNAMED.** Boot is one undecomposed figure; its split into system
prompt / tool schemas / deferred-tool list / MCP instructions is `ds-025` item 1 and is **still dark
from every mount**. So no connector is ranked and no saving is stated — either the decomposition
becomes readable, or the one-variable experiment is repeated per connector.

⚠ Per `s241-D2` the figure is stated **ONCE**, in the `post-mortem #287:` line, and the finding file
`notes/_lanes/287/BOOT-COLD-2026-09-19.md` is deliberately **not** in `notes/_GAUGE-LOG.md`.

---

## ⛔★★★ THE AFTERNOON — A GPT-6 HANDOFF, AND A FRAMING DAVE CORRECTED

Dave brought a handoff from **Apollo Spider v1.0.13** running on his work machine (an HSBC CEO
banking prototype, a GPT agent with no vision). ✅ **It is SAVED INTO THE REPO** at
`notes/_lanes/287/GPT-SPIDER-SPACING-HANDOFF-2026-09-18.md` — ritual step 1's cited-uploads clause,
because a chat-only attachment is an un-retrievable citation.

Lane X tested only its **factual claims about our system**, at file:line, read-only, no gate and no
generator run: **5 of 6 VERIFIED, 1 PARTLY.**

- ✅ the template's 40/4 pin (`canon.css:18119`, `:18121` — literals, not theme-conditioned, and the
  source comment says so);
- ✅ `--layout-bento-gutter` resolving to 0 in the consuming scope — **but MIS-FRAMED as a failure**:
  `tokens/layout.json:114` states the intent outright and `s217-D2` ruled it from Dave's own tuner
  exports;
- ✅ supercharge's 2px inner gap is legal vocabulary with **no minting path and no binding**;
- ✅ the four-column lead rule is a deliberate override with twenty lines of receipt naming its
  ruling, its measurement and a rejected alternative — the report **under-credits** it;
- ✅ PROPOSED metadata against a skill that directs its use — **and worse than stated** (below);
- ⚠ **PARTLY: the 33 pass / 8 FAIL split.** The arithmetic is exact against v1.0.13's 41 RUNNABLE
  gates, but the attribution is roughly **3 screen-caused, 4 pack-baseline, 1 placement-dependent**,
  and the agent **ran no `--baseline`**, so it could not separate its own failures from inherited
  debt. The pack ships `--baseline` for exactly this and its own skill states the rule.

★ **Its one real analytical miss is the same miss twice: it read `0` and `40/4` as DEFECTS when both
are RULED values.**

**And then the conductor made a sharper version of the same error.** He took lane X's finding to
Dave as *"two ruled spacing sources disagree"*. Dave's correction, above, is the answer:

⇒ **There is NO contradiction to resolve by picking a winner. The OUTER (structural bento) gutter
and the INNER (embedded bento / tile-group) gutter are TWO DIFFERENT QUANTITIES, each deliberately
per-theme.**

⛔ **What survives the correction is real and narrower:** the template pins ONE theme's pair as
literals instead of delivering the selected theme's (outer, inner) pair, **because the `s219-D3`
GENERATION ARM WAS NEVER BUILT.** `knowledge/_render/_bento_edit_rails.json` declares itself
`$groundwork_only` in its own header and has sat un-consumed since #219.

⚠ **Whether `--layout-bento-gutter` (ruled 0 in Mono, `s217-D2`) IS the structural gutter is still
TO BE READ, not assumed.** That reading is the first beat of the review he ordered.

---

## ⚠ THREE SMALLER FINDINGS, EACH DECLARED BY THE LANE THAT MADE THE JUDGMENT

**(a) A COMMIT LANE WROTE THREE OTHER LANES' STORE ROWS.** `_gate_doc_rows.py` refuses a commit
staging a sub-report with no `_state.json` row (`s218-D7`), and at lane C's open only K had one.
Rows `W-287i`, `W-287w`, `W-287c` were written through `_state.py`'s **module API**, never by hand,
each `closes_when` taken from that lane's own filed verdict and re-worded nothing; the alternative
was `DOC_ROW_ACK`, which *"would have shipped three invisible documents to pass a gate"*.
⛔ **A close-condition you want changed is yours to correct, not to discover.** ⚠ Related and left
open on purpose: `W-286rb`'s `closes_when` asks for Dave to accept `sizes` as the field name, and
today he said *"keep `sizes`"* — half the condition is met by his own word, and closing lane R2's
row is the conductor's call.

**(b) THE DASHBOARD WAS ALREADY 11,617 LINES STALE AGAINST ITS OWN SOURCE.** `dashboard/index.html`
carries a 9,590-line diff and most of it is inherited, **measured rather than assumed**: a
regeneration from the **UNCHANGED HEAD `_state.json`** alone moves 11,617 lines; lane W's seven row
edits account for ~1,262, most of that `gen_dashboard.py`'s own re-ranking cascade. It is FRESH now
for the first time in several sessions, and the fact is on the face of the commit message.
⛔ **Ruling-shaped and not inscribed: nothing checks this file's freshness against its source** —
there is no `--check` arm the way `_gen_chain.py` and `_render_rulings.py` have one, so the
staleness was invisible until a lane happened to regenerate.

**(c) A 4.3 MB BEFORE-COPY SITS IN `_to_delete/287-K-before/`.** Lane K could not delete its own
evidence copy (`Operation not permitted` on `unlink` under the mount — the #284 finding still
standing), so lane C used the #284/#286 `mv` precedent into a gitignored directory. **`.gitignore`
was NOT edited and no path was excluded from staging**; the 807 KB `.gz` **is** committed, which is
the evidence in the form meant to be kept. ⛔ **`_to_delete/` is an accumulating squatter that `4c`
does not reach, and what to do about it is his.**

---

## ★★ THE DELEGATION RULE — OBEYED A THIRD SESSION, STILL UNINSCRIBED

Measured at this seat by **importing `_checkin.read_fill`** rather than re-implementing it, against
the conductor's own transcript `6ff1b408-192e-4f32-8c4c-889929239137.jsonl`:

**FIVE lanes, every one an `Agent` at `spawnDepth 1`, model opus** — X 142,327 · K 124,765 ·
W 122,129 · C 112,722 · I 71,588 ⇒ **subs 573,531 real (n=5)**, QUOTA and never FILL. **No lane work
was done in seat.**

⚠★★ **AND A DEFINITIONAL DISAGREEMENT WAS FOUND HERE AND IS PUBLISHED RATHER THAN RECONCILED AWAY.**
Read with `_checkin.read_fill` — input side only, which is the ONE definition of FILL this repo has
— the same five seats sum to **568,179**. The 573,531 above is each seat's last-turn input side
**plus that turn's `output_tokens`**, the convention this log has carried since #284. **The gap is
5,352 and it reconciles to the token on every one of the five.** ⇒ **Which one the `subs` line means
is ruling-shaped and is his** [[measure-dont-convert-units]]. ★ The conductor's declared FILL
figures ARE `read_fill` readings and agree to the token, so the split is confined to that one line.

⚠ **A SIXTH SUB — the wrap seat itself — is deliberately EXCLUDED**: its own total cannot be final
from inside itself, and `s214-D5` forbids turning an unknown into a number.

⛔ **THIS DOES NOT CLOSE THE CARRY.** Three sessions' obedience is evidence the shape is affordable,
not a rule that it is required. **Inscribing is his.**

---

## ⬛ #288 — FIRST MOVES, IN ORDER (his priorities, and #288 OPENS ON 1, NOT 2)

1. ⬛★★★ **THE STRAND MAP AND THE FRIDAY-25TH PATH.** *"I need to understand how the multiple
   strands of Apollo stand and I need a clear path to presenting something cohesive for friday the
   25th"* — **six days.** ★ **This is a Fable JUDGMENT beat at the opener, then ONE Opus lane
   producing the page.** Per `anthropic-skills:dave-voice` a long-form deliverable is a
   **swiss-design-system HTML page, never a `.md`**. It must lay out **every live strand** — the
   designer pack and Spider · the bento canon and its template · the dashboards one-shot · the KG
   explorer and the rulings brain · the logo masters · **and the presentation itself** — each with
   its state and with **what must land by Friday 2026-09-25**. ⚠ **The presentation strand's own
   location is NOT established from this seat and must be FOUND, not assumed:** grep the handoffs
   and notes for *presentation*, *deck*, *David Rice*, *HSBC demo* (the `#256` stray-provenance
   discipline applied to a strand — *"provenance not established from this seat"* is the honest form
   of a blind spot).
2. ⬛★★ **THE BENTO SPACING REVIEW, AND BUILD THE `s219-D3` ARM.** Mono's 0 is **DOUBTED, not
   overruled** — `s217-D2` still rules the value. **All four themes rendered side by side for his
   eye**, and **Mono's 0 read FROM SOURCE**, not from any report. *"and any other problem with
   this"* puts the whole delivery path in scope.
3. ⬛★ **THE TEMPLATE QUALITY REVIEW — a SECOND lane, not a clause of 2.** *"we need to look at this
   too"* is what separates them. Four `$awaitingDave` entries and two `$tokenGaps` have been
   unresolved since #231.
4. ⬛ **THE TWO CARRIED DECISIONS he did not answer:** an inline-style rule (**88 raw values** is the
   actionable number, not 596; **zero rulings on inline styles exist across all 622**), and the
   template's status (**meta `PROPOSED / NOT REGISTERED` versus showroom `beta`**).
5. Everything still open on `_HANDOFF-130`…`-137`. **Strike nothing without a receipt.**

---

## ⬛ OPEN, RULING-SHAPED, NOT INSCRIBED — the `s271-D4` form: every one is a QUESTION PUT

1. **The strand map and the Friday-25th path** — and where the presentation strand actually lives.
2. **Mono's 0 and the unbuilt `s219-D3` generation arm.**
3. **The bento template's QUALITY.**
4. **An inline-style rule** — 88 raw px/rem values with no `var()`, and `DEF-004`'s population.
5. **The template's two statuses** — and whether `showroom/index.json` can express *proposed* at all.
6. **Which definition the `subs` line means** — input-side or input-plus-output.
7. **A freshness check for `dashboard/index.html`.**
8. **`_to_delete/` accumulating on a persistent disk.**
9. **`INSEAT_WARN_TK = 10,000` and the INSEAT block's placement** — untouched, still picked.
10. **Whether a verifier lane may mutate the tree it verifies** — raised by #286's lane V.
11. **The delegation rule** — obeyed a THIRD session, still uninscribed.
12. **The store's id regex**, **a RESUME contract for the ritual**, **`_seam.py`'s SCRATCH arm**,
    **the memory archive at 48,990 of 49,152 B**, **the boot ceiling's twelfth breach**,
    **the two-probe-shape question on the §A digest** (its nineteenth session), **the third dial**,
    **the theory door**, **`col26-012`**, **`jade-lifestyle`**, **`s277-D12`**, **what a session
    should DO at the hard wall**, **the four generators**, **the git-lock runbook line**, **the
    instrumentation-append policy**, **the `#243` not-a-wrap form** — all carried, all aged, none
    touched.
13. **Everything on `_HANDOFF-130`…`-137` not closed today.**

⛔ **CLOSED TODAY, WITH RECEIPTS, AND NOTHING ELSE — four carries, each struck with the session that
proved it closed AND where the correction is inscribed (`s183-D1` / `s188-D2`):**

| struck carry | receipt |
|---|---|
| the two uninscribed sentences | *"inscribe"* → `s287-D1` / `s287-D2`, store 620 → 622, `75a490cd` |
| the masters' field key AND the unbuilt explorer | *"keep `sizes` and rebuild."* → `s287-D2` + lane K's v1.27 rebuild |
| the 58 prose wall locations | *"do it"* → lane W, 58 → 42, zero wall-assertions |
| `_seam.py`'s stale DRAFT line and the `:26`-vs-`:44` dispute | lane I amended the first clause only; `:44` measured |

⚠ **AND THE CONNECTOR-LEVER CARRY IS DELIBERATELY *NOT* STRUCK.** Its headline —
*"THE CONNECTOR LEVER READS −7,031 AND THE CEILING STILL STANDS"* — records a reading and a ceiling
that **both stay true**; what changed is the reading's standing. **A strike removes the headline,
not the clause**, so the n=2 upgrade is said in a new carry item instead. ★ **`s271-D4`: a strike
that is wrong is worse than an item that is merely stale.**

---

## ⛔ STRUCTURAL REDS — inherited, measured here, NOT repairable by a wrap

**SIX blocking gate fails stood at this ritual's open**, carried in the `#243` DECLARED not-a-wrap
form — **the THIRTEENTH consecutive wrap.** Every one is another session's append-only testimony in
`notes/_GAUGE-LOG.md`:

- **boot-drift CEILING BREACH** — `BOOT_CEILING_TK` 70,000, seven post-diet readings named in the
  gate (#277 83,636 · #278 72,110 · #279 72,447 · #280 75,740 · #281 77,400 · #282 77,474 ·
  #283 80,871). ⚠ **It does not yet count #286's 73,832 or #287's 74,120** — the `post-mortem` line
  is where those enter, and a commit lane does not write it.
- **five boot double-counts** — #243 (×5), #264, #272, #273, #274.

⚠ **A SEVENTH WAS BORN MID-SESSION AND HEALED BY ITS OWN PRESCRIBED REMEDY.** Lane W's edits to the
two chain sources took the structural fails 6 → 7 (retrieval index STALE, the #32 defect); running
exactly what the gate named — `_build_memento_index.py`, ritual step 2g, **not** on that lane's
fenced list — took them back to 6, measured both ways. ★ **A lane that causes a fail, is told what
to run, runs it, and re-measures is the gate working as designed.**

Also standing and NOT repaired: `carry_wording_check()` is **blind** (both residual lines are
pointers, so it has nothing to pair and goes quiet — the `s188-D2` invariant was held BY HAND here);
`_gate_scratch_hygiene.py` reports the fill of `/` rather than `/sessions`; `_seam.py`'s SCRATCH arm
still deletes a lane's `/tmp` files mid-run; two REGEN-SERIAL advisory warns stand uncleared because
their runner is `_build_all.py` and the lane was fenced from it.

---

## ⚙ THE NUMBERS THIS SESSION MUST HAND FORWARD

Measured at this seat against the conductor's own transcript
`6ff1b408-192e-4f32-8c4c-889929239137.jsonl` — this wrap seat being
`subagents/agent-addfe852130dd24e1.jsonl` beneath it, which is what makes the subtraction legal
[[measure-dont-convert-units]].

| term | measured | declared at the brief cut | delta |
|---|---|---|---|
| **FILL** | **181,277 real / 24 turns** | 180,375 / 23 | **902** — the smallest hand-over on this run |
| **BOOT** | **74,120 real, n=2 on this setup** | 74,120 | agrees to the token, **and that agreement is what identifies the window** |
| **subs** | **573,531 real (n=5)** — and **568,179** by `read_fill` | 573,531 | ⚠ two definitions, both published |
| peak / compaction | **181,277 · 0 records, 0 drops** | — | measured here |

⛔ **THE 180,000 QUALITY LINE WAS CROSSED BY 1,277, AND THE BRIEF SAYS WHERE: the stop line was
crossed by 375 ON THE WRAP CALL ITSELF.** The ritual fired *at* the line rather than past it, which
is what `ds-023` asks for; the 902 that followed is the hand-over, not the job. ✅ **38,723 inside
the ≤220,000 tolerance.** ✅ **256,000 clear for the fifth session running.** ✅ **No compaction
record and no fill drop**, so the reading is a fill and not an artefact.

⛔ **BOOT 74,120 IS THE TWELFTH POST-DIET READING OVER THE 70,000 CEILING AND IS NOT A RE-BASE** —
but it is the reading that turned last session's direction into a measured effect.

---

## ★ NEXT CHAT TITLE

Generated by `python3 knowledge/_gen_titles.py --session 287`; the receipt is at
`knowledge/_gen_titles_receipt.json` and the line stands at the top of `GOOD-MORNING.md`:

> `Apollo - #288: the strand map and the path to friday the 25th`
