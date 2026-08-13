# #169 — the audit's reader had no theme axis, and that is why red 30 could not answer "which theme?"

provenance: 169 · 2026-08-13
status: ruled — `knowledge/_rulings.json` § `s169-D1`

*Narrative dossier (capture-ritual step 1b). The terse WHAT lives on the `GOOD-MORNING.md` ★ LATEST
banner, the `_LIVE-STATE.md` ⏱ LATEST delta and `knowledge/_rulings.json`; this file holds the WHY
and the HOW, including the dead ends, because those are what evaporate with the chat.*

Links both ways: spine entry → `_LIVE-STATE.md` ⏱ LATEST DELTA #169 · ledger → `knowledge/_rulings.json`
§ `s169-D1` · banner → `GOOD-MORNING.md` ★ LATEST #169 · gauge → `notes/_GAUGE-LOG.md` `#### 2026-08-13 #169`.

---

## 1. The session opened by digesting the previous one's post-wrap corrections — CHAIN-DIET-2

#168 was a delegated wrap, and Dave ruled twice AFTER it closed (`#168-A`, then `s168-D5`). Each
post-wrap ruling was corrected **in place**, on the banner line, because a cold session reads the
GENERATED `_CHAIN.md` and an addition below a stale claim does not stop the stale claim being
believed. That discipline is right and it is expensive: three correction blocks accreted on one
banner and its title line, and the read chain paid for all of them at every boot.

**The class, named here so it is not re-discovered:** *post-wrap rulings on a delegated wrap multiply
in-place corrections, and the digest belongs at the NEXT opener, not at the end of the wrap that
caused them.* The remedy is the standing [[home-by-addition-then-cut]] move — home the correction
blocks by ADDITION somewhere durable, then cut them from the chain, never one motion.

Enacted as commit `e8ed189`: the three #168 correction blocks homed at
`notes/_MEMENTO-DECISIONS.md` § ★ #169 CHAIN-DIET-2; the title line cut **879 → 64 tape**
(cap 120, `#60-D8`); the chain **15,709 → 13,629 tape**; index rebuilt; rehearsal 0 structural fails.

⚠ And that commit itself demonstrated the live defect it had to be amended for: **the `SESSION_N`
prefix generator TRIPLED the `after #169 2026-08-13 —` prefix**, and the script's own "subject
identical" assertion is BLIND to it because the assertion checks line 1 of the **msgfile**, not the
**generated** subject. `e8ed189` was amended in place from a fresh msgfile. That is instance 2 of the
#164 class in this session alone, and the reason this dossier's sibling instruction — *read the
subject back with `git log -1 --format=%s` after EVERY commit* — is not advice but a step.

## 2. The disk fence was cleared at root cause, and the fix was Dave's, not the sandbox's

The `/var/tmp` disk fence has been carried as a residual for twelve sessions, re-measured each time
as "still 99% full", and each time worked around rather than diagnosed. This session diagnosed it.

The sandbox VM's disks held **~2G of caches from OLD sessions, owned by defunct uids** (they resolve
as `nobody`). Nothing inside the VM can delete them — not the delete grant, not `rm` as their nominal
owner. A VM restart did **not** recycle them. The fix was outside the VM entirely: with the app quit,
Dave deleted `~/Library/Application Support/Claude/vm_bundles` (20G), and the VM rebuilt fresh —
**root 51%, `/sessions` 1%, caches gone.**

★ The finding is about where a fence's root cause lives. Twelve sessions treated a **host-side
garbage-collection bug** as a sandbox constraint, because the sandbox is the only surface a session
can see. The residual carry is CONSUMED. The **upstream bug remains** — temp files of dead sessions
are not reaped — and Dave holds the report text. The in-VM workaround, if a future session meets a
full disk before that bug is fixed: **install to `/dev/shm`, per call.**

## 3. Red 30: the recommendation was accepted, and then the mechanism refused it

The carried residual read: *"RED 30 — 'which theme?' [NEW — DAVE'S], option C (theme-key the store)
recommended, UNCONFIRMED."* Dave confirmed it — *"okay go"* — and the build sub was dispatched.

**The build sub stopped without enacting, and it was right to.** Option C's mechanism collides with
`s158-D4` single-source: the per-theme RAG values **already live** in the palette tier
(`tokens/palettes/rag/*.json`, addressed via `tokens/themes/_themes.json` → `ragPalette`), and the
semantic store has **no theme axis to key**. Adding one would have made two tiers own the same
values — the exact shape `s158-D4` exists to prevent.

★ **The finding, and it generalises: the defect was in the READER, not in the data.**
`_build_surface_contrast_audit.py` did a single `json.load` of the semantic store and therefore
graded **apollo-mono's grounds for all four themes**. That is why red 30 could not answer *"which
theme?"* — **the instrument had no theme axis either**, so the question was unanswerable in the
instrument's own grammar, and the natural-looking repair was to change the data to fit the reader.
[[no-gate-parses-the-artefact]] is the same shape pointed the other way: here a reader that could not
parse the four-theme artefact made the artefact look like the problem.

⚠ **What was NOT done, deliberately:** the re-scope was not silently substituted for what Dave had
already approved. Re-authoring an approved option into a different one and calling it enacted is
[[feedback-dont-launder-a-premise-into-a-ruling]]. It went back to him as an **explicit option set**,
and he picked verbatim: ***"C′ — fix the audit's reader"***.

## 4. What C′ enacted, and how it was proved rather than asserted

`knowledge/_build_surface_contrast_audit.py`, **+270 / −2**:

- palette-owned grounds resolve **per theme**, walking `tokens/themes/_themes.json` → `ragPalette` →
  `tokens/palettes/rag/*.json`;
- **`apollo-mono` emits no theme row** — it *is* the activeBase, so a row would be a double count;
- a missing or unreadable palette raises **`PaletteRefusal`, a NAMED refusal** — never a crash, never
  a silent default [[a-crash-is-not-a-fail]] [[feedback-measuring-tool-must-not-guess]];
- **`--selftest`, 10 arms, rc=0**, and four of them are mutation controls rather than assertions
  [[mutation-tests-the-clause-not-the-feature]]: **A2a** a mutated legacy palette moves the legacy
  ground · **A2b** the mutation FLIPS the verdict (OK 7.87 → POOR 1.0) · **A2c** the mutation is
  SCOPED, console/supercharge unmoved · **A2d** the real store is untouched by the mutation arm ·
  **A3** the missing-palette refusal is named.

**What the audit now says — and it is a finding, not a closure.** Base pass **unchanged**: 18 OK,
4 allowed, **1 gating failure**, which is red 30 itself (`rag/text/on-dark`, `#FFFFFF` on `#F6604C`,
**3.14:1**). Per-theme: **6 pairs regraded, 3 NEW gating failures**, all of them
`rag/text/on-information` with ink `#1A1A1A` on a palette-owned error ground —
**apollo-legacy 2.21:1 on `#A8000B`** · **apollo-console 2.89:1 on `#B92F1E`** ·
**apollo-supercharge 2.89:1 on `#B92F1E`**.

## 5. The second leg of the same class — OPEN, and Dave's

The reader now applies per-theme **grounds**. It does **not** yet apply per-theme **token overrides**,
and that is almost certainly why the three new failures exist:

- `apollo-legacy` overrides `rag/text/on-information` → **`#FFFFFF`** at
  `tokens/themes/apollo-legacy.overrides.json:203` (**`s131-D1`**);
- and every citation points the same way — **`s122-D3`**, **`s122-D5`**, **`s132-D1`**, and
  **`s149-D1`'s scope line** all say white-on-error **outside mono** (`s149-D1`'s dark ink is
  **MONO ONLY**, explicitly).

So the three new failures are **LIKELY ARTEFACTS of the unapplied override leg**. ⛔ That is a
**recommendation, UNCONFIRMED**, and nothing in `s169-D1` rules it. Extending the reader — and then
re-adjudicating whatever survives — is the #170 item and it is Dave's.

★ The reason this is written down rather than just fixed: the honest reading is that we now have an
instrument that reports **more** failures than before and we do not yet know which of them are real.
A session that "fixes" the three by authoring colour values would be closing a measurement it had not
finished taking [[green-tests-cannot-see-scope]].

## 6. What the gauge says, and the class it re-demonstrates

Boot **56,693** real — **~660 above the 54,859 ±1,178 band**. A datapoint, declared out of band,
⛔ never corrected into the constant [[boot-floor-measured-109]].

**FILL at wrap-open 176,166 against the stop line 150,929 — a DECLARED BREACH of ~25K.** The cause is
attributable and is not a mystery: **two sub REPORTS landed in fill** (a sub is cheap in BUDGET and
expensive in QUOTA, but its *report* is charged to the window that reads it —
[[delegation-cost-inversion-110]]), plus the disk archaeology of §2, which was open-ended reading by
its nature.

★ **And the lane check-in caught it LATE, which is exactly the failure the class predicts:**
[[checkin-at-the-ends-cannot-catch-the-lane]] — *a check-in at the ENDS cannot catch the lane*. Both
build lanes ran well past ~15K with no check-in INSIDE them, so by the time the seam arrived the
overrun was already banked. The declared breach passes; a silent one fails. That asymmetry is the
whole mechanism, and it is the reason this paragraph exists rather than a rounded-down number.

Effort rung: job window ≈ FILL − boot ≈ **119K** ⇒ **L** band (edges DERIVED at build from gauge-log
quartiles — ⛔ never hand-banded, never "corrected" back to a remembered pair [[measure-dont-convert-units]]).
Sub spend, per the `s168-D3`(a) convention: **`subs 155855 tokens (n=2)`** — 68,035 + 87,820, the two
build subs; **this wrap sub's own spend is EXCLUDED and UNMEASURED**, and an unknown is not estimated in.

Dave's quota panel: **NOT ASKED-ANSWERED this session** after the Thursday reset. Written ABSENT,
⛔ never defaulted [[quota-panel-has-three-numbers]].

## 7. The carry that has now been titled twice and touched twice — neither time

`s165-D4`'s per-line link ratification stands at **6/37**. It was the titled item of #168 and it was
never started. It was the titled item of **#169** and it was **never started again**. Said plainly
because the alternative is a carry that reads identically at one session old and at three: it has now
been the headline of two consecutive sessions and has moved zero rows in either.

★ Writing the age is the whole defence [[premise-ages-faster-than-rule]]. What to do about it — press,
park, or delegate it as the first act of #170 — is Dave's, every time.

---

## Resolved state at close

- ✅ `s169-D1` RULED (Dave's) and **ENACTED + VERIFIED** in-window — the audit's reader is per-theme.
- ✅ CHAIN-DIET-2 landed (`e8ed189`, amended for the tripled prefix).
- ✅ The `/var/tmp` disk fence is **CONSUMED at root cause** — host-side, Dave's fix, VM rebuilt.
- ⬛ OPEN, DAVE'S: the per-theme **token-override** leg, and the adjudication of the 3 new failures.
- ⬛ OPEN, DAVE'S: `s165-D4` per-line link ratification, 6/37, titled twice and untouched twice.
- ⚠ OPEN, ungated: the T3 msgfile-prefix class — now **two committed instances this session** plus a
  **blind assertion** (it checks msgfile line 1, not the generated prefix).
