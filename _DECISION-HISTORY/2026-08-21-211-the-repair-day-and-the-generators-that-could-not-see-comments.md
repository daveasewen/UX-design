# #211 — the repair day, and the generators that could not see comments

```
provenance: 211 · 2026-08-21
status: observed
```

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #211 · banner: `GOOD-MORNING.md` ★ LATEST #211 ·
store rows: `W-86`…`W-94` in `knowledge/_state.json` · receipts: `notes/_receipts/2026-08-21-211-*.md`.
Both-way links per `_DECISION-HISTORY/README.md`.*

---

## Why this session existed at all

Dave opened it with almost no quota — the panel read, verbatim, *"All models Resets in 27 min 86%
used · Fable Resets in 27 min 92% used"* — and with four words: **"drill!"**, then *"I want some
work that doesnt need me"*, then *"pedal to the metal"*, then *"keep gpomg"*, then *"go for it"*.
That is a very specific commission: **spend the day on work whose value does not depend on Dave
looking at anything.** The week's quota reset mid-morning, which is why the day could run four
delegated waves; **no post-reset panel reading was ever taken, and none is invented here.**

The obvious candidate for work-that-needs-nobody was the **#210 findings pile**. #210 built a great
deal (the library went 91 → 135) and, in doing so, measured a stack of defects it did not repair —
each one already licensed by an existing ruling, so repairing them required no new decision from
Dave. That is the whole shape of #211: **four waves, seven repair lanes, zero rulings inscribed**
(`knowledge/_rulings.json` is byte-untouched), nothing built new, and Dave's eye queue untouched.

## The finding that reframed the day: generators cannot see HTML comments

Lane **R1** (`notes/_receipts/2026-08-21-211-wave1-laneR1-token-ramp.md`) went looking for a
reported 46 dead token declarations and found **120**. The premise in the brief was wrong, and it
was wrong for an instructive reason: `gen_token_ramp` was injecting its `AUTO-TOKENS` block
**inside an HTML comment**. Everything downstream then behaved exactly as designed on text that
the browser would never render. The repair was a comment-mask plus a **refusing post-condition** —
the generator now fails loudly rather than writing into a comment — and P-8's finding count fell
**58 → 12**. ⚠ The remaining 12 ABSENT declarations are **colour choices and therefore Dave's**;
they were priced, not picked.

That single defect turned out to be a **class**, and the rest of the day was mostly its shape
recurring in different organs:

- **R6** (`…-wave3-laneR6-declared-value.md`) found the same comment-blindness in
  `declared_value` / `check_contracts` / `manifest_vars` inside `gen_component_partials.py`.
  Fixed with `mask_comments` + `live_text`; **7/7 mutants bite**, including a fence over the
  **132 injection sites**; the sync came out a **byte-level no-op on 159 files**, which is the
  proof that the fix changed the generator's *vision* and not its *output*.
- **R7** (`…-wave4-laneR7-figure-re.md`) is the one that was worse than anybody expected.
  `FIGURE_RE` was non-greedy **across newlines**, so a match starting at a **commented-out**
  `<figure>` ran to the first **real** `</figure>` and swallowed Image-block's first live figure —
  measured span **368-7777** against the live span **6915-7777**. This was recorded going in as a
  *latent* exposure. It was not latent. It had already eaten something. Repaired by a
  locate-live / slice-raw split across three selectors; **5/5 mutants bite**; sync no-op on 147
  files.

**The through-line, worth saying plainly:** a generator that reads its own output as flat text
cannot tell live markup from commented markup, and every check built on top of it inherits the
blindness silently. Nothing crashed. Nothing went red. The gates all passed, on text that did not
exist as far as the rendered page was concerned.

## The repairs that were about ink, not boxes

Lane **R3** (`…-wave1-laneR3-a11y-repairs.md`) carried three a11y repairs — the Date-picker
today+selected ring from **1.21:1 to 17.40:1** (redrawn in `var(--page)`, at the token layer, so
all four themes move together — ⚠ the four rendered specimens are **UNPROVEN**), the Drawer's
two-frame focus strand to zero, and an input descender clip of **3.25px to 0**.

Its *finding* mattered more than its repairs. **P-6 measures box height, but inputs cut ink.**
The probe's own fixture clips glyphs today and reports green. Gate-extension options were priced,
and the honest conclusion is recorded rather than smoothed: **rendered-ink comparison is the only
sound predicate** for this, and adopting it is Dave's call, not a lane's.

**R5** (`…-wave3-laneR5-descender-clips.md`) then applied R3's enacted shape to the last three
offenders — Multi-select, Tags-input, Combobox, each **3.25px → 0.00**, driven with R3's own
instrument. ⚠ The **ds-005 class choice is untouched and still Dave's**: these are per-instance
repairs standing in for a class fix nobody may make on his behalf.

## The container query that was asking the wrong element

**R2** (`…-wave2-laneR2-lsplit.md`) repaired `.l-split`'s container self-query **at cause**, by
moving the collapse onto the children via an `@container` child rule, which fires with no wrapper
at all and therefore repairs eight consumers from one file. P-7 went **6 findings + 3 WARN → 0**.
Transfer-list needed the ruled `.hv-frame` wrapper, and the flex parent-property asymmetry is
named in the receipt rather than worked around. Premise corrected again by measurement: **three**
workaround templates, not four.

## The lane that stopped instead of finishing

**R4** (`…-wave1-laneR4-probe-hygiene.md`) converted P-3/P-6 launch crashes into an honest
**refusal, `rc=77`** under the COULD-NOT-ASK contract — a crash is not a fail, and a probe that
dies should say it could not ask rather than imply an answer.

Then it **stopped, honestly**, on `error-solid.svg`. The icon has been empty since its first
commit; the pipeline is an all-or-nothing Figma export needing `FIGMA_TOKEN`, and the manifest
recorded `fills:[]` at generation time — so the defect is **plausibly upstream in the Figma node**,
not in this repo at all. ⚠ Nothing was faked to make the file non-empty. It is carried as owed.

## The corrections the session made against itself

Three, and they are the reason this dossier is worth its tokens:

1. **The conductor missed his own serial set.** Wave 2's snippet changes needed the canon layer
   regenerated; he did not run the whole serial, CI went red on `[45]`, and he repaired it in a
   separate commit (`652d432`) and named the miss as **his**. This is the **second conductor
   instance** of the regen-serial-set-is-ordered class.
2. **R6's own first mutation matrix lied.** A stale `.pyc` served M1's arm for M2 and M3 —
   i.e. the harness reported bites that the harness itself had produced. R6 **caught this itself**
   and re-ran. A mutation test proves the clause only if the clause is the thing actually driven.
3. **Two briefed premises were wrong and were corrected by measurement, not argument** —
   46 dead declarations (really 120), four workaround templates (really three). Both corrections
   are inscribed in their receipts' claim tables.

## Where CI stood, and why this wrap is the healer

Every #210 push was red (#379–#392), and the #210 wrap's banner roll **did not heal `[115]`** —
that wrap re-measured rather than assumed, found the chain still at roughly 42% against a <40%
demand, and carried it as a residual instead of trimming anything. #393 was red on `[13]` + `[115]`
with render annotations that *looked* red while the render job itself succeeded. #394 (`91b3270`)
added `[45]` (the serial miss). #395 (`652d432`) took `[45]` green and returned the failure set to
exactly `[13]` + `[115]`. #396 (`95973cd`) held at `[13]` + `[115]` — **wave 3 added zero CI debt.**
⚠ **#397 (`da35003`) is UNREAD at this wrap and is declared unread; its read-back is the
conductor's** (`s203-D1`).

Both standing reds trace to the same physical fact: **`[115]` measures `_CHAIN.md` against
`GOOD-MORNING.md` at the tape tier, and the chain IS the ★ LATEST banner.** #210's banner is
**26,455 real**. So the healer was never a threshold — **it is a lean banner**, which is what this
wrap wrote: the session's new items as tight numbered bullets, and the deep carry tail carried
**by reference** to the ★ PRIOR (#210) banner, with the resulting `carry_wording_check` blindness
**declared beside the carries** rather than reported as a clean run.

⛔ **No threshold was touched all session.** Dialling the `0.40` constant is Dave's, under his own
`s208-D1` rider that a re-base must arrive with a reduction option priced beside it.

## And then 2.5GB of photographs arrived

Mid-session Dave dropped **251 Getty/EyeEm JPEGs, 2.5GB**, into `knowledge/assets/photography/`.
They arrived **untracked and un-ignored**, which means the next `git add -A` would have swept
licensed stock into git history permanently. The conductor **fenced them in `.gitignore` before
any commit could run** (verified at this wrap: 251 files present, `git ls-files` → 0 tracked).
The arrival record is `notes/_briefs/2026-08-21-211-photography-assets-arrival.md`, and `W-93`
carries what is owed: a committed manifest, KG nodes and edges to the consumers, a tagging pass
(the EXIF descriptions are the seed), and **Dave's pipeline ruling** — NON-REPO vs LFS vs
committed derivatives. He named **Image-block and Carousel** as the first consumers.

## What is resolved, and what is still open

**Resolved:** seven repair lanes landed across four commits, all pushed and remote-verified
(`91b3270` · `652d432` · `95973cd` · `da35003`); the comment-blindness class is closed in both
generators it was found in; the descender-clip table is fully closed at the instance level; P-7 is
at zero and P-8 is at twelve; the probe launch path refuses honestly; the photography originals are
fenced.

**Still open, and all of it Dave's:** the 12 ABSENT tints · the `ds-005` class choice · the P-6
ink-verdict gate extension · P-7/P-8/P-6 promotion or parking (`W-85`) · REVIEW-204's 7th `.l-split`
instance · the four canon `border-radius:0` literals · `error-solid.svg` / `FIGMA_TOKEN` · the
photography pipeline ruling · the `[115]` `0.40` constant and every other threshold · the 34
proposed organisms and the REVIEW-210 pages · the gauge-constant re-base.

⚠ **Nothing in this file is a ruling.** It is the arc; the WHAT lives in the store rows and the
receipts, and every promotion out of "priced" into "ruled" is Dave's alone.
