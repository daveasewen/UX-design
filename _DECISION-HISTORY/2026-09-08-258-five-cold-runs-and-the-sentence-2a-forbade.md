# Five cold runs, and the one sentence rule 2a forbade

provenance: 258 · 2026-09-08
status: observed

*The WHY and HOW of Apollo session #258. The WHAT is the ★ LATEST banner of `GOOD-MORNING.md`
and the ⏱ LATEST delta of `_LIVE-STATE.md`; the four rulings are `knowledge/_rulings.json`
§ `s258-D1` … § `s258-D4`. This file holds the arc — the dead ends, the corrections, and the
order the thinking actually moved in. Lands whole, dated from `date`, never silently edited.*

---

## 1. Why the day opened with a cold run, and why it ran five times

#257 was named for making dashboards one-shotable and spent its whole window on two releases.
The carry into #258 said so bluntly: *nothing about the prompt changed; only the window was
spent* — so every claim about one-shotability was a claim about the prompt's **text** rather
than about its **behaviour** [[mutation-tests-the-clause-not-the-feature]]. The first act of
#258 was therefore to stop reasoning about the prompt and drive it.

The choice that made the day worth recording was running it **five** times rather than once.
A single cold run produces a score and an anecdote; it cannot separate a defect in the subject
from a defect in the instrument. Run **v1** was against the ratified **v1.0.7 zip**
`13a593de…` — the artefact a stranger would actually download — and scored **3/2/0/2** against
#246's 2/2/0/2 on the same prompt. Its most useful output was not the score: it was the
discovery that *the pack's own gate fails the bento template*. At that moment the instrument
and the subject were both suspect, and only repetition could tell them apart.

Every run was **blind** (an Opus lane that had not seen the library) and every run was
**verified by a separate lane that drove the page**, because a build's own report of itself is
a claim. Twice the verifier earned its cost: it corrected the v2 grid from *"~400px"* to
**213px**, and it found that the `.dgseg` element the report named was **absent** — the state
switcher was three unstyled buttons. Both corrections are on the record rather than smoothed
out, because a verifier that only ever confirms is an instrument nobody is reading
[[instrument-without-a-consumer]].

The series: **v1 3/2/0/2** (zip) → **v2 3/2/3/3** (tree at `e774fb7`) → **v3 3/2/3/2**
(`5c241f7`) → **v4 3/2/3/3** (`84f0a17`) → **v5 3/3/3/2**, at which **both gates passed for the
first time in the series** and the grid rendered **1,328px in a 1,376px tile**.

## 2. The finding, and why it was invisible before the runs

Across v1 and v2 one pattern held with no exceptions:

> **Everything that worked was self-contained inside one component. Everything dead reached
> across one.**

A filter that drives a grid. A nav whose state drives a strip. A KPI that answers a toolbar.
Each of those needs a sentence of JavaScript that **no snippet can carry, because the sentence
is about two snippets**. And rule 2a of `ADS-generate-from-canon` — *"Copy the script address
with the markup; author no JS"* — forbade the author from writing it. The prompt was asking
for wiring while banning the only place wiring can live.

This is worth naming as a class: **2a was a correct rule solving the wrong failure.** It exists
because authors invent markup and drift from canon; that danger is real and the rule reduced it.
What nobody had measured was the cost on the other side, and the cost was every cross-component
behaviour on every generated page. It took a driven page to see it, because the rule's damage is
invisible in the source — the page **looks** complete.

Dave's ruling was immediate and went further than the finding asked: *"definitely remove 2a I'd
like to see not only the wiring work it might deliver some code creativity"* (`s258-D1`). He
then widened it from permission to expectation in `s258-D2` — ambitious by default, everything
on the page assumed to work, mock data rich and deep enough to make behaviours possible, and
*"writing code might be an avenue to innovation, the interface is pretty tied down."* The
`/goal` skill he floated in the same breath he parked himself.

Enacted in one wave of three Opus lanes (`e774fb7`): skill rules **13–17** (data model first ·
every control works · state persists · zero JS errors · footer mandatory), procedure 2a
rewritten to *"Model the data"*, step 6 to *"Drive it"*, and `_validate_receipt.py` relaxed so
authored JavaScript stops failing the receipt.

## 3. A premise corrected before a wave was spent on it

Lane 2 was sent at the bento template's *"146 hex literals"* and came back with the **premise**
instead of the fix: **36 of the 146 are session numbers inside CSS comments** (`/* #248 … */`),
and `check_screen` never strips comments before counting. The remainder are declared theme
splices. Had the lane obeyed rather than checked, a wave would have been spent chasing
thirty-six phantoms.

The same lane established what `_validate_screen.py` actually is: it reds **all eight shells
unmodified**, because it is the **composed-screen** gate and not a snippet gate. Snippets carry
two themes; the four Apollo themes live on `data-apollo-theme`, which **0 of 137** snippets
link. None of that is a defect — it is the gate's contract, and it had been read as a defect.

## 4. The fence, and the second finding: a fence protects a page, not a generator

v2's one blind-condition defect was a payments grid rendered **213px wide** in a 1,296px tile,
because the Data-grid snippet spliced its demo-state switcher **and its `--demo-width` dial**
into the page. Put to Dave as retain-for-library / strip-for-build versus strip entirely, he
chose the first and called it a **"sweep"** (`s258-D3`).

Fencing rather than deleting was the right shape — the showroom needs the chrome, the build must
never see it — and a probe first measured the surface honestly: **61 snippets carried chrome, 27
of them dangerous** (`notes/_subreports/2026-09-08-258-P-demo-chrome-probe.md`). Lanes A/B/C
fenced **53** snippets with `APOLLO-DEMO <what> START/END`, moved every dangerous `--demo-width`
read to a real component default, and split five template scripts component/chrome. Lane G
taught the skill never to copy inside a fence and `_validate_receipt.py` a named
`FAIL:DEMO-CHROME-COPIED` (selftest 46 arms).

And then **v4 found the fenced `.dg{--dg-max:760px}` sitting in `canon.css:10538`.**

The fence had protected the page and not the generator. `gen_canon_components` had been
projecting fenced CSS into canon all along, so the chrome the build was told to ignore was
arriving through the front door as canon. The repair was at the generator — it now **strips**
`APOLLO-DEMO` fenced CSS, removing **335 lines of chrome** from `canon.css` — and
`--<component>-max` were declared page-owned **runtime** vars in `_validate_compose.py`.

★ The general form is worth keeping: **a marker is only as strong as the set of readers that
honour it.** Three readers honoured the fence; the fourth was a generator nobody had asked.

## 5. What v3 caught that no gate could have

v3 scored 3/2/3/2 with three toolbar filters dead. They died on an **open contract**: the
`behaviour` meta says how a component is wired, and the skill never told the author to read it.
**21 of 136** metas carry `behaviour` at all, and none of data-grid, filter-toolbar-bar or
sidebar-nav did until this session typed three. The remaining **51** scripted components are a
listed backlog (`notes/_subreports/2026-09-08-258-L3-behaviour-metas.md`).

v3 also showed the receipt gate never firing, because nothing was minted — so step 5 now mints
first. Both are the same lesson in two places: **a contract nobody is instructed to read is not
a contract**, and a gate that cannot fire is not a gate.

## 6. Where the day ended, and what is deliberately unfinished

`s258-D4` (*"1. Okay lets do it"*) chose the honest repair over the convenient one: Data-grid
**composes** its checkboxes from Selection-controls — 44px targets, indeterminate driven,
compose gate PASS on a v5 copy, mutation-proved — rather than the gate exempting the component
that fails it. That is the `s253-D2` shape run the right way round for once: the **page** was
repaired, not the reader.

Rule **18** ("Charts from data — the interim recipe") landed last, quoting the `dv-behaviour`
grammar and driven green on a 78-line test page. ⛔ **It is a recipe in a skill, not an engine in
the library**, and lane R named the trap that will bite: canon namespaces every `.dv-*` rule
under `:where(.cn-chart-*)`, and cold runs v4 and v5 emitted chart geometry with **no
`cn-chart-*` wrapper** — so their bars never animated in canon terms. That is #259's stated job.

Two things about the day's own conduct belong here rather than in a banner. The conductor's
running FILL estimate was **≈95K against a measured 187,384** — half — and the cause is not
carelessness: **sixteen lanes' returns are the FILL**. A lane is cheap in the window's budget
only until it reports, and sixteen reports are sixteen documents resident in the window that
read them. The check-in ran at the opener and once at the end and **not between the lanes**
[[checkin-at-the-ends-cannot-catch-the-lane]], which is exactly how an estimate halves. He also
typed a `git stash` by reflex during a compose check and popped it the next call; nothing was
lost, and it is recorded because the reflex is the hazard, not the outcome.

## 7. Resolved state, and what is still open

**Resolved:** rule 2a is gone and the author writes JavaScript · builds are ambitious by default
· demo chrome is fenced in 53 snippets and stripped at the generator · Data-grid composes
Selection-controls · both gates pass on a cold-run artefact for the first time · the boot ceiling
reads under the literal for a second consecutive session.

**Open, and his:** the **chart engine** (six charts for the demo, five after) · the **v1.0.8 cut**
and the sixth cold run that is its receipt · **his rulings page**, unbuilt for a third session at
a store of 402 · the parked **`/goal`** skill · the **51 blank `behaviour` metas** · the
`_screen-gate` ledger clobbering tracked files because it keys on basename · `check_screen`
counting hex inside comments · **ten of eleven chart types unused five runs running** · and his
element list for the design pass (KPI tile, grid header, filter toolbar).

*Links: ★ LATEST banner and ⏱ LATEST delta for #258 · `knowledge/_rulings.json` § `s258-D1`…`D4`
· `_CARRIES.md` § `residual → #259` · the fifteen filed reports `notes/_subreports/2026-09-08-258-*.md`
· reviews `reviews/COLDRUN-258-2026-09-08-v1.html` … `-v5.html` · commits `70ed8c7..1c9c6ae`.*
