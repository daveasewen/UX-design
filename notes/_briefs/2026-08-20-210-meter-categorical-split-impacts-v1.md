# The Meter categorical split — impacts and benefits, priced (#210, 2026-08-20)

> **STATUS: NOTHING HERE IS A RULING. Every option below is PROPOSED.**
> Store row for THIS document: `W-69`. It exists because you asked for it in so many words:
> *"im not sure of the impacts and benefits"*. Written to answer that, and nothing else.
> ⛔ Nothing in this memo was acted on. `Progress-bar.reference.html`, `progress-bar.meta.json`,
> `Limits-meter.reference.html` and `limits-meter.meta.json` are **byte-untouched**. No registry,
> no `CATEGORIES` list, no `component-types.json`, no `canon.css` and no `_rulings.json` entry was
> written by the lane that produced this file.

---

## 0 · Your direction, verbatim — the thing this memo is measured against

> "Generic role meter, unless there is benefit in having two, so they are the same molecule but
> they are categorised and might actually be different items when selecting them from the store...
> For me the user, selecting the component, AI model or human need to understand the difference
> even though the physical shape might be the same."

> "I think the user, AI or User must understand the difference, even if it's only categorical."

Read literally, that is **one requirement with three parts**, and it is worth separating them
because they have different costs:

1. **ONE MOLECULE.** Already ruled and already true — `s210-D1`, "keep as one meter". Nothing in
   this memo reopens it. Every option below keeps exactly one snippet and one geometry.
2. **CATEGORISED.** The difference must be *legible at selection time* — when a human browses the
   store, or when a model retrieves a component to build with. This is the part that costs
   something, and it is what §2 prices.
3. **"MIGHT ACTUALLY BE DIFFERENT ITEMS."** You left this as a *might*, not an instruction. So it
   is put as a choice, with what it buys and what it costs, and not smoothed into a recommendation
   dressed up as your words.

Your three open questions (Q3 role, Q5 what retires, Q6 the vocabulary) are **one direction, not
three answers**. They firm together, on your word, once you pick a shape below — or name your own.

---

## 1 · What is actually in the tree today (measured this session, not recalled)

Every figure here came from a command run in this lane. Nothing is quoted from an earlier session.

| Fact | Measured value |
| --- | --- |
| Meter-family metas that exist right now | **THREE** — `knowledge/components/progress-bar.meta.json`, `limits-meter.meta.json`, `meter.meta.json` |
| Meter-family snippets | THREE — `Progress-bar.reference.html`, `Limits-meter.reference.html`, `Meter.reference.html` |
| Showroom pages already generated | **FOUR** — `showroom/progress-bar.html`, `limits-meter.html`, `meter.html`, `runway-bar.html` |
| Their showroom category | **All four sit in "More"** — i.e. *none of them is categorised at all today*. `gen_showroom.py CATEGORIES` (line 127) has no meter bucket; `CAT_OF` has no entry for any of the four, so they fall through to the uncategorised tail. |
| Snippets carrying `role="progressbar"` **in markup** | **EIGHT** files: the three meter-family files plus **Progress-tracker, File-upload, Stepper, Runway-bar, Timeline** |
| Snippets carrying `role="meter"` in markup | **ZERO.** Every hit for that string in the tree is prose in a comment. |
| `_rulings.json` mentions of "meter" before #210 | 0 — nothing in the store ruled the role either way, which is why both parents inherited `progressbar` |
| `_validate_kg.py` state today | **OK** — 103 metas, every ref parses and resolves, edges match schema, `gen_kg_edges.py` idempotent-clean |
| `Meter`'s own registration today | canon.css **DOES** carry a `.cn-meter` block and `showroom/meter.html` **DOES** exist (both projected by the conductor's serial step); `_validate_binds_resolve.py` is clean at 101/101 canon blocks, 0 failures. **Not** in `component-types.json`, **not** in `CATEGORIES`, **not** in `MIGRATED_SNIPPETS`. ⚠ Both the canon block and the showroom page were projected from the snippet's PRE-enactment bytes and need regenerating |
| Type-composite debt | 1,097 violations — the Meter work contributes **zero** and the debt did not grow |

⚠ **One premise in my own brief did not survive contact with the tree, and it matters to Q5.**
The brief named *three* snippets as already improvising `role="progressbar"` (Progress-tracker,
File-upload, Stepper) on `s173-D1`'s authority. The grep says **five** non-meter snippets do:
those three **plus Runway-bar and Timeline**. Runway-bar is a deliberate near-neighbour that the
Meter spec explicitly declines to merge; Timeline's hit is in a comment explaining why it is *not*
a progress bar, so the honest count of *markup* improvisers outside the meter family is **four**
(Progress-tracker, File-upload, Stepper, Runway-bar). Declared here rather than carried forward
as three, because a fold list built on the wrong count would retire the wrong things.

⚠ **The other thing worth knowing before choosing:** the meter family is *already* invisible in the
catalogue. Whatever you rule, the state you are moving *from* is not "two well-labelled components"
— it is four uncategorised pages in a "More" bucket. That makes the do-nothing option worse than it
looks, and it makes option (A) cheaper than it looks, because the category field has to be authored
either way.

---

## 2 · The three catalogue shapes, priced

All three keep ONE snippet, ONE geometry, ONE class vocabulary. They differ only in **how many
things a selector sees, and where the category lives.**

### Option A — ONE meta, the variants carry the category

`meter.meta.json` stays the single entry. Its existing `variants` and `semantics` prop gain
explicit, retrievable category fields — a "progress" reading and an "allowance" reading, each with
its own purpose sentence, its own use/don't-use pair, and its own worked example.

**What a human sees when selecting.** One card, "Meter", which opens to two clearly-named readings.
They must open the card to see the split.

**What a model sees.** One retrievable document with both readings inside it. This is actually the
*best* shape for a model: a retrieval hit returns the contrast — "progress = a task, full is
success; allowance = a cap, full is a blocked payment" — in the same breath as the geometry, so the
model cannot pick one reading without seeing the other.

**What gates/registries/KG see.** One node, one showroom page, one set of binds. No new addresses.
`_validate_kg.py` sees no new node keys. `gen_showroom.py` needs one slug placed in one category.

**Migration cost from today's three metas.** Lowest. `meter.meta.json` is edited in place; the two
parents' entries are dealt with under Q5 (§4) independently of this choice.

**⚠ CONSEQUENCES AND PITFALLS.**
- It gives you the *weakest* form of the thing you asked for: the difference is legible **after**
  selection, not **at** selection. If your worry is a designer scanning a grid of cards and picking
  wrong, this option does not fix that.
- Two readings inside one document is exactly the shape that drifts: someone updates the allowance
  prose and not the progress prose. There is no gate today that would catch that divergence.
- "Category" would live in a field no registry reads. **A field no consumer reads is an instrument
  without a consumer** — the class that has bitten this repo before. If you pick A, the field needs
  a reader on day one or it is decoration.

### Option B — TWO metas (`progress-meter` / `allowance-meter`) pointing at ONE snippet

Two catalogue entries, each with its own purpose, its own anti-patterns, its own examples — both
naming `knowledge/snippets/Meter.reference.html` as their implementation.

**What a human sees.** Two cards with two different names, in two different places in the store.
"Progress meter" can sit under *Feedback and status* next to Progress-tracker and Loading-indicator;
"Allowance meter" can sit with the money components. **This is the literal reading of your "might
actually be different items when selecting them from the store."**

**What a model sees.** Two retrievable documents. A query about a spending cap returns the allowance
document and never has to reason its way past task-progress prose. Sharper retrieval, at the cost of
the two documents no longer being forced to stay consistent with each other.

**What gates/registries/KG see.** **This is where the cost is.** Two metas naming one snippet is a
shape the repo has not run before: `probe_meta_schema.py` checks each meta independently and would
pass, but `_validate_kg.py` builds nodes from metas and `_validate_binds_resolve.py` checks that
each snippet has its canon block — a *one-to-many* meta→snippet relation has never been driven
through either. **That is an UNPROVEN claim about tooling, and it is the single biggest unknown in
this memo.** It needs a probe before B is ruled, not after.

**Migration cost from today's three metas.** Highest. Two new metas authored, both cross-referenced,
two showroom pages generated from one snippet (`gen_showroom.py` keys pages by snippet slug today —
another thing that would need changing, not just configuring), and Q5's fold executed underneath.

**⚠ CONSEQUENCES AND PITFALLS.**
- **Two documents describing one artefact WILL drift.** That is not a prediction, it is the
  duplication `s173-D1` was written to stop, reintroduced at the catalogue layer instead of the code
  layer. If you pick B, the two metas need a generated shared section, or a gate that compares them.
- It reopens, socially, the thing `s210-D1` closed. A designer who sees two cards will reasonably ask
  why they are not two components — and the answer lives only in prose.
- The tooling unknown above is real and unpriced. B should not be ruled on this memo alone; it
  should be ruled after someone drives one meta→two-metas fixture through the KG and binds gates and
  reports what actually breaks.

### Option C — the parents' metas stay, as category ALIASES referencing Meter

`progress-bar.meta.json` and `limits-meter.meta.json` are **not retired**. Each is rewritten down to
a short alias record: its name, its category, its one-sentence "when you want this reading", and a
pointer to `meter` as the implementation. Meter carries the full spec.

**What a human sees.** The names they already know — "Progress bar", "Limits meter" — still findable,
each landing on a page that says *this is the Meter, in this reading*. Nothing they have bookmarked
or referenced 404s.

**What a model sees.** Two thin documents that both route to one thick one. Retrieval on either name
succeeds and converges. **No duplicated spec prose exists to drift**, because the aliases hold no
spec — that is the structural difference from B, and it is the whole argument for C.

**What gates/registries/KG see.** Three metas, as today, so **no registry count changes and no
address moves**. But the alias records would be a *new kind* of meta: `probe_meta_schema.py` requires
`tokenValidation`, `props`, `provenance` and more on every meta, and a thin alias has none of them
honestly. Today exactly one file is exempted from that requirement (`EXAMPLE-button.meta.json`,
declared, never hidden). **C therefore needs either a schema seat for "alias" or two more declared
exemptions.** That is a smaller unknown than B's, and a known one.

**Migration cost from today's three metas.** Middle. Two files rewritten (not deleted — nothing is
lost, `home-by-addition-then-cut` is satisfied by construction), one schema decision, no new nodes,
no new showroom pages, existing showroom pages keep working.

**⚠ CONSEQUENCES AND PITFALLS.**
- Progress-bar is **GATED and PROMOTED**. Demoting a promoted component to an alias is a status move,
  and status moves are yours alone. C cannot be executed by a worker on this memo.
- Three metas for one component is more surface to keep true than one, even if two of them are thin.
- If the aliases are allowed to grow spec prose over time, C decays into B and inherits B's drift.
  If you pick C, the aliases need a *size* fence, not just a convention.

---

## 3 · The ARIA leg — `role="progressbar"` vs `role="meter"` (Q3)

This is a separate axis from §2 and should be ruled separately. A catalogue category is a *authoring*
distinction; an ARIA role is what a blind user's software says out loud. They can agree, and they do
not have to.

**What the two roles mean.**
- `role="progressbar"` says: *a task is underway and this is how far through it is.* It implies
  progression toward completion. Full means done.
- `role="meter"` says: *a scalar measurement within a known range.* It implies no task and no
  direction of travel. Full means at the top of the range — which might be good or bad.

On meaning alone, an allowance meter is a `meter` and a file upload is a `progressbar`. The semantics
genuinely differ, and your instinct that these are two things is correct at the ARIA layer.

**What assistive technology actually does with them — and this is the decisive part.**
- `progressbar` is **broadly and consistently supported**. It has been in ARIA since 1.0, every major
  screen reader announces it as a progress indicator, and `aria-valuenow`/`valuetext` are reliably
  read.
- `meter` was added later (ARIA 1.1) and its support has historically been **weak and inconsistent**
  across screen readers — variously announced as a generic group, as a progress bar anyway, or with
  the value dropped. It is the standard example of a semantically-correct role that under-serves the
  user in practice.

⚠ **Honest limit on that paragraph.** Those are general accessibility facts, not a measurement made
in this repo this session, and AT support moves. **Before `role="meter"` is ruled in, it should be
verified against current support tables — that is a real, small piece of work and it is not done.**
I am flagging it rather than letting a confident sentence stand in for a test.

**PROPOSED — my recommendation, and I am recommending rather than hedging:**

> **Keep `role="progressbar"` on every meter, in both readings. Do NOT split the ARIA role to
> mirror the catalogue split.**

Three reasons, in order of weight:

1. **The categorical requirement is already satisfied without it.** You said "even if it's only
   categorical" — the difference must be understood by *the person or model selecting the
   component*. That is an authoring-time audience. A screen-reader user is not selecting a component;
   they are reading a value. Splitting the role serves the wrong audience for your stated need.
2. **The user-facing meaning is already carried, and carried better.** Every meter in the spec
   renders its value as text *and* carries `aria-valuetext` in domain words — "3,200 pounds used of a
   5,000 pound daily transfer limit, leaving 1,800 pounds. Resets at midnight." That sentence tells
   a blind user everything `role="meter"` would imply and a great deal more, in every screen reader,
   today. `role="meter"` would add semantic tidiness and risk losing the value announcement.
3. **Consistency has real value here.** Eight snippets carry `progressbar` in markup and zero carry
   `meter`. Splitting the role makes the same visual object announce differently depending on an
   authoring category the user cannot see.

**⚠ CONSEQUENCES AND PITFALLS of this recommendation.**
- It leaves a component literally called **Meter** using `role="progressbar"`. That reads wrong in a
  code review and will be raised again by whoever next opens the file. If you accept it, it should be
  written down *as a decision with its reason*, not left as an inherited default — otherwise a future
  session re-litigates it for a fourth time.
- It is a bet that AT support has not improved. That bet has an expiry, and the honest form is a
  re-check date, not a permanent ruling.
- If you *do* want the roles split, the cost is small and known: it is a mechanical change to the
  markup of the allowance-reading specimens plus the `requiredAria` list — **but by
  `s202-D3`/`s210-D1` reasoning it would change three files together** (Limits-meter, Runway-bar and
  Meter), not one, and Runway-bar is outside the Meter fold's scope.

---

## 4 · What retires at fold time, per option (Q5)

Nothing in this section has been acted on. `Progress-bar` is GATED and PROMOTED; that status is
yours to move and no worker may move it.

| | Option A (one meta) | Option B (two metas) | Option C (aliases) |
| --- | --- | --- | --- |
| `progress-bar.meta.json` | Retires into `meter.meta.json` | Retires; its content splits into `progress-meter` | **Stays**, rewritten as a thin alias |
| `limits-meter.meta.json` | Retires into `meter.meta.json` | Retires; its content splits into `allowance-meter` | **Stays**, rewritten as a thin alias |
| `Progress-bar.reference.html` | Retires (its four specimens are already reproduced as Meter variants) | Retires | Retires |
| `Limits-meter.reference.html` | Retires (its readout and lock-up are already reproduced as Meter organisms) | Retires | Retires |
| Showroom pages | `progress-bar.html` + `limits-meter.html` retire; `meter.html` stays | Two pages regenerate under new slugs | All three pages stay; two become alias pages |
| Existing binds addresses | `.cn-progress-bar` / `.cn-limits-meter` canon blocks become orphans and need projecting to `.cn-meter` | Same, plus a one-to-many question the tooling has never seen | Same as A — the alias metas do not carry binds |
| KG nodes | Two nodes retire, one stays | Two retire, two new appear | No node count change |
| `_validate_radius.MIGRATED_SNIPPETS` | `Progress-bar.reference.html` is listed there (line 144) and would need reconciling in every option | same | same |

**In every option, `Meter` must first be FULLY REGISTERED.** ⚠ This paragraph was re-measured at the
enactment pass and corrected: it is **half done already**. `canon.css` carries a `.cn-meter` block and
`showroom/meter.html` exists — both projected by the conductor — and `_validate_binds_resolve.py` is
clean (101/101 canon blocks, 0 failures). What is still missing is `component-types.json`,
`CATEGORIES` and `_validate_radius.MIGRATED_SNIPPETS`. Registration is the conductor's serial step and
is **prior to** any fold. Whichever option you pick, the order is:
register Meter → prove it green → *then* move the parents. Folding first would leave the catalogue
with a hole.

**FUTURE WORK, NAMED AND NOT DONE.** The four non-meter snippets improvising `role="progressbar"` in
markup — **Progress-tracker, File-upload, Stepper, Runway-bar** — each hand-roll their own track and
fill. Whether they eventually *consume* Meter rather than re-drawing it is the natural next
duplication question and it is **exactly the shape of `s173-D1`**. It is named here so it is not
forgotten and **deliberately not scoped**: it is a separate lane, it touches four gated components,
and it must not ride along on a catalogue decision. Runway-bar in particular is a near-neighbour the
Meter spec explicitly declines to merge, and that declining should not be quietly reversed by a
consumption pass.

---

## 5 · Recommendation — PROPOSED, with the consequence you would be accepting

> **PROPOSED: Option C — keep the parents' metas as thin category aliases pointing at Meter — paired
> with keeping `role="progressbar"` on every reading.**

**Why C rather than A.** A gives you the *authoring* split but not the *selection* split, and
selection is the audience you named twice. C puts two names in the store, in two categories, exactly
as you described — "different items when selecting them from the store" — while keeping one and only
one place where the spec lives.

**Why C rather than B.** B and C look the same to the person selecting. They differ entirely in what
happens six months later: B has two full specs that will drift, C has two thin pointers that
structurally cannot. B also carries a real, unpriced tooling unknown (one snippet, two metas, through
KG and binds) that C does not.

**⚠ WHAT YOU WOULD BE ACCEPTING IF YOU PICK C.**
- A **status move only you can make**: Progress-bar goes from GATED and PROMOTED to an alias.
- A **schema decision**: `probe_meta_schema.py` has no seat for a thin alias, so either the schema
  gains one or two more declared exemptions join `EXAMPLE-button.meta.json`. Recommend the schema
  seat — an exemption list that grows is how a gate stops meaning anything.
- A **size fence on the aliases**, or C decays into B.
- A **written-down decision on the ARIA role with a re-check date**, so a component called Meter using
  `role="progressbar"` reads as a decision rather than an oversight.
- **The `CATEGORIES` question comes with it**: today all four meter-family pages sit uncategorised in
  "More". C's benefit only lands if the two aliases are actually *placed* — and where they go
  (Feedback and status? a new bucket?) is a call this memo does not make.

⛔ **If you disagree with any of the above, disagree with the recommendation and not with a fact.**
The measurements in §1 are reproducible; the recommendation in §5 is a judgement and yours to
overturn. Naming your own fourth shape is a legitimate answer too.

---

## 6 · What closes `W-69`

You pick A, B or C — or name your own shape — and the Q3 / Q5 / Q6 trio then firms together on your
word. Until then: no fold, no retirement, no role change, no registry edit. The four parent files
stay byte-untouched.
