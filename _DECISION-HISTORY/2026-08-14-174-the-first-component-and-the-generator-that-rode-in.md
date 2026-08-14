# #174 — the first component through the route, and the deferred change that rode in on a generator

provenance: 174 · 2026-08-14
status: ruled — `knowledge/_rulings.json` § `s174-D1`

*Written at the #174 wrap by a delegated OPUS wrap sub. Spine entry: `_LIVE-STATE.md` ⏱ LATEST
DELTA #174 · ledger: `knowledge/_rulings.json` entry 154 (`s174-D1`) · banner: `GOOD-MORNING.md`
★ LATEST #174. ⚠ Every gauge figure, every Dave quotation and every measurement made inside the
build sub's window is **RELAYED by the conductor** — a wrap sub cannot measure the conductor's
window or read another sub's transcript, and ⛔ nothing here was estimated in to cover the gap
[[feedback-measuring-tool-must-not-guess]].*

---

## Why the session existed

#173 closed **gate 1** of the component-scaffold brief (`s173-D1`: the progress bar is the first
component through the route) and left **gates 2–6 explicitly with Dave for the weekend**. The brief
had already produced its most useful output before anyone built anything: **it found its own
inherited premise stale.** The scaffold largely already existed — a runbook, a meta schema and 76
metas, 75 snippets, the canon generator, the four-theme cascade, a 76-page showroom and a twelve-step
gate chain. What was genuinely missing was narrower: a scaffolder, a standard per-theme render
harness, and any index over the metas.

So #174 opened on a decision, not a build: **does the missing convenience get built, or does the
component get built through the route as it stands?**

## Finding 1 — Dave closed all five remaining gates, and the grounds are the interesting part

`s174-D1`, taken on a plain-prose read-back in chat [[feedback-decisions-in-plain-prose]]:

- **Gate 2 — BUILD THE COMPONENT, NOT A SCAFFOLDER**, and keep a friction log while building it.
  The grounds are `s172-D3`'s observed-failure rule applied to its first real case: the route
  already exists, so **what is missing is convenience, not capability**, and a scaffolder built
  today would be a speculative instrument with no observed failure behind it. The friction log is
  the deliverable that decides whether a scaffolder is ever built at all — evidence first,
  instrument second.
- **Gate 3 — DETERMINATE ONLY.** The indeterminate state overlaps the existing `Loading-indicator`
  component and that ownership is unruled; building it would seat an unruled overlap.
- **Gate 4 — DO NOT MINT A `component-type` FAMILY.** Queued as a proposal;
  `component-types.json` untouched.
- **Gate 5 — the two stale inventory documents are corrected as a SEPARATE LANE, after the build,
  never during it.**
- **Gate 6 — one Opus sub, one window, ~110–130K.** No Sonnet subs [[feedback-no-sonnet-subs]].

⇒ **all six gates of the brief are now closed and the brief is CONSUMED.**

## Finding 2 — step 0 caught two stale premises before a line was written

The anti-stale-premise step earned its place for the **second session running**
[[premise-ages-faster-than-rule]]:

1. HEAD was `be1e0a7`, not the brief's `e5ab8ee` — benign, but the brief's file-line citations were
   written against a different tree.
2. The brief's claim that an unregistered component *"will not appear in the index"* is **FALSE**.
   `gen_showroom.py:483` reads `CAT_OF.get(slug, "More")`, so an unregistered component lands in
   **"More"** rather than vanishing. A build that had trusted the brief would have registered the
   component to fix a problem that does not exist — and registering it would have violated the
   in-code convention *"workers never edit this file"*.

## Finding 3 — the contrast failure that was found first and NOT faked into a pass

Before building, the four-theme contrast of fill-on-track was computed **by hand**. It **fails 3:1
in Legacy dark (1.75:1) and Supercharge dark (2.38:1)**.

The tempting move was to declare a gated `contrastPair` and let the gate bless it. That was
deliberately **not** done: a `contrastPair` here would have been **a green that cannot fail in two
themes** [[green-tests-cannot-see-scope]]. Meaning is carried instead by a **numeric value in text
plus `aria-valuetext`**, so the component is legible without relying on the failing pair. The
failure is **pre-existing** — the identical pair already sits under `Progress-tracker` — and it was
**queued to `_DS-IMPROVEMENTS.md` with a four-theme table and three options**. ⛔ **Dave rules it.**

## Finding 4 — ★ THE FINDING OF THE SESSION: a deferred, Dave-owned change rode in as a build side-effect

Regenerating `canon.css` for the new component also ran the theme-cascade generator. That run:

- **stripped 25 explicit `--status-*` declarations** from Legacy, Console and Supercharge — verified
  first-hand by the conductor: **25 removed, 0 added**; and
- **deleted the hand-written `#168`/`#168-A` comment block** from inside the generated region.

Those are precisely residual items **`[50]`** (~10K, *"needs Dave's eye — a visible 3-theme colour
change"*) and **`[45]`** (~5K) from #173 — **both on this session's do-not-rule list.**

★ **The lesson is structural, not a scolding: a queued-and-priced change re-entered the tree through
a generator that another lane legitimately had to run.** A do-not-rule list names **decisions**; it
cannot fence a **generator's blast radius**. This is the same root as friction item 7 below — step 6
of the runbook lists the generators that own regions of `canon.css` and its list is incomplete.

In fairness to the build sub, it chased the `#168` deletion hard and its reasoning holds: `#3F6FB5`
was superseded twice (`s168-D5`) and the live value `#6893D3` is emitted **identically before and
after**, so what went was a **stale hand-edit inside a generated region** — the `[45]` defect itself,
removed by the generator that owns the region.

## Finding 5 — ⬛ Dave's response is FLOATED, not ruled

Asked whether to revert or keep, Dave answered, verbatim:

> *"lets keep it nice and simple, all of them use the appropriate dark ink on white and the lightest
> ink for dark"*

The conductor read this back as a **background-keyed ink rule** — the two-red-law shape
[[two-red-law-ruled-151]] — rather than a per-theme bespoke palette, **declared the ambiguity
openly** (whether he means the status colours themselves or the text on them), and left the
regenerated state in place, **uncommitted at the time of the read-back**.

⛔ **This is a FLOAT awaiting his confirmation. It is NOT `s174-D1` and it is not a ruling of any
number.** It is recorded here verbatim precisely so the record cannot later quote it as one
[[memento-three-registers]].

## Finding 6 — the friction log, all nine, because it is the deliverable

1. ★★ **The snippet gate is single-theme by construction.** `resolve()` reads only
   `semantic-colour.json` (the Mono base) and cannot see the Legacy/Supercharge legs, so **any
   four-theme contrast claim must be computed by hand, outside the gate**. *"A single-theme green is
   not a green"* is doctrine — but the gate can only ever give the single-theme green. **This is the
   biggest gap found.**
2. ★ **A token NAME is not an ADDRESS, demonstrated live** [[canon-pri-hover-fork-108]].
   `progress/incomplete` has **no override in any theme file** yet resolves differently in
   Supercharge, because its `$alias` targets `color/neutral/13` and Supercharge rebinds the whole
   neutral ramp warm. **Nothing warns you** — it was caught only by grepping the generated CSS per
   theme.
3. **The runbook is 54 lines and omits half the gates it must clear** — no icon gate, no
   type-composite ratchet, no radius `MIGRATED_SNIPPETS`, no registry step.
4. **The icon gate fails any SVG-based component silently** — `<circle>`-only shapes read as
   "shape-only icons"; the remedy (`data-bespoke="why"`) is in the gate's docstring and nowhere in
   the runbook.
5. ★ **The type ratchet makes every new snippet a failure by construction.** The boilerplate
   `body{font-family:var(--font)}` every snippet carries is itself a TYPE-002 violation, so a new
   component adds one and trips a shrink-only ratchet. Removed here (all text is composed) — but
   **the DEFAULT snippet shape fails the gate.**
6. **The brief contradicts itself on `CATEGORIES`** — §4 step 5 says register it, §2.2 quotes the
   in-code convention *"workers never edit this file"*. The in-code convention was honoured, so the
   component lands in "More". **One line is owed from the conductor.**
7. **Step 6's generator list is incomplete** — `gen_theme_cascade.py` and `gen_canon_tokens.py` also
   own regions of `canon.css`. ★ **Same root as finding 4.**
8. **Sandbox: `rm`/`rmdir`/`unlink` were denied on the repo mount for the sub**, so
   `git checkout -- <file>` failed; truncate-in-place (`cat HEAD > file`) was the working
   substitute. ⚠ The conductor later obtained the delete grant — **the runbook's step-0 grant was
   not in the sub's brief** [[feedback-read-the-runbook]].
9. ⚠ **`rc=$?` after a pipe reads the PIPE's status.** It gave a false green baseline on a gate that
   is red at baseline. Caught and re-measured. **Known class, bitten again**
   [[check-after-its-own-remedy]].

## Finding 7 — what was proved with controls rather than asserted

Two reds were **proved pre-existing**, not claimed to be [[attribute-the-diff]]:

- `gen_theme_cascade --check` was **already rc=1 at HEAD** — the regeneration *healed* it.
- The `gen_canon_components.py` deletion was isolated by **moving the component out of tree and
  restoring `canon.css` to HEAD**.

And one thing could not be run, declared rather than smoothed: `_validate_state_contrast.py` over
the full 76-snippet population **exceeds the ~178s call cap**. Filtered to `Progress-bar` it is
clean, rc=0, driven in a real browser. **That filtered run overwrote the tracked
`knowledge/_STATE-CONTRAST-AUDIT.md`, which was restored byte-identical**; it does not yet list
Progress-bar, and **a full run is owed to CI**.

## The machinery line

`machinery: 0 instrument / 274 feature`. No gate, checker or harness was built; the review-page
builder and the renderer live in `/var/tmp`, outside the repo. **A four-theme contrast checker was
QUEUED, NOT BUILT** — it has a named failure class (finding 6, item 1), but building it in the same
breath as the finding is exactly what `s172-D3`'s observed-failure rule forbids
[[bounded-verification-ruled-172]].

## Resolved state, and what is still open

**Resolved:** all six gates of the component-scaffold brief are closed and the brief is consumed;
the progress bar exists as a snippet, a meta, a showroom page and a four-theme review; the gate
chain is green over it, including a **type-composite debt contribution of 0 — the only clean file
of 91**.

**Open, and none of it is this wrap's:** Dave's ink float and the uncommitted `--status-*` strip
that rides on it · the fill-on-track contrast finding in Legacy dark and Supercharge dark · the full
`_validate_state_contrast.py` population run owed to CI · the four-theme contrast checker, queued
not built · the runbook's four documented omissions (friction 3, 4, 5, 7) · the brief's `CATEGORIES`
contradiction, one line owed · the `progress-family` proposal · gate 5's inventory-correction lane ·
and `[45]`/`[113]`/`[107]` from #173.
