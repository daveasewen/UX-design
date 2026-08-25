# #219 lane 5 — unconsumed mints, disposed

**Sub:** Opus, lane 5 of the #219 crank. **Base:** `04655de`, clean tree. **Committed:** nothing.
**Brief:** `notes/_briefs/2026-08-25-219-crank-divvy.md` (DO-NOT-RULE observed — no `_rulings.json`
write, no constant, no promotion, no Dave-owned row touched, no memory write).

COUNTS: 9 findings · 5 ruling-shaped · 4 UNPROVEN · 0 class-(a) wirings · 3 class-(b) · 3 class-(c) · 1 gate built (advisory, 10 arms) · 1 review page · 3 store rows · subs 0

---

## The headline, in one paragraph

Lane 1 reported ~47 per-theme minted vars with zero consumers, ~20 a declared false-positive class,
"leaving ~27 genuine". **I reproduce the 47 exactly and the ~27 does not survive.** Two mechanisms —
not one — consume tokens outside CSS, and once both are subtracted the genuine population is **six**.
Of those six, **none is the segmented shape**: there is no orphan where a ruling names an existing
consumer that is simply unwired. Three are taste calls with real, measured consequences (one of them
would make a theme *worse*), and three are DNA-tier rungs that ADR-0014 reserves by design.
**So: nothing was wired, and that is the finding, not a shortfall.** What was built instead is the
instrument that makes this class visible at all, plus a live decision surface for the three taste calls.

---

## 1 · The sweep, re-run first-hand

Definition used, stated so it can be argued with: a declared custom property is **CONSUMED** if its
name appears inside a `var(…)` in any `.css/.html/.js/.py/.json/.md/.svg` file in the repo, **outside**
`reviews/`, `_review/`, `notes/`, `runs/`, `outputs/`, the archives, the vendored `designer-skills-v*`
copies — and outside the generators that emit `canon.css` (a generator printing a name is not a
consumer of it). The glob is published in the gate's docstring, not inferred.

Instrument: **`knowledge/_gate_minted_consumption.py`** (new, this lane). Run:
`python3 knowledge/_gate_minted_consumption.py --orphans`.

```
canon.css declares 973 custom properties (base tier 972 · theme tier 394)
  consumed by a var() in the glob ......... 600
  unconsumed .............................. 373
    ├─ ALIAS-TARGET (mint-time $alias) ..... 84
    ├─ ALIAS-SHADOW (alias expansion) ...... 24
    └─ ORPHAN (declared, never read) ...... 265   [6 of them minted per-theme]

per-theme minted: 394 · of which zero-consumer: 47  =  17 ALIAS-TARGET + 24 ALIAS-SHADOW + 6 ORPHAN
```

**47 reproduced.** The split is where I part company with lane 1.

⚠ **One self-inflicted defect, caught on the first real run and named because it is instructive:** the
gate's own docstring quotes `var(--color-neutral-15)` as a worked example, so the gate read its own
prose and reported the example token as consumed — 46 instead of 47. Fixed by an explicit, commented
`SELF` exclusion. An instrument that scans the repo can scan *itself*; that is a general trap for any
future gate of this shape.

## 2 · The false-positive classes, subtracted with the mechanism named

### (i) ALIAS-TARGET — 17 of the 47. Lane 1's class, identified mechanically rather than by family.

`gen_theme_cascade.base_value()` follows `$alias` and `_expand_aliases()` materialises effective
overrides — **in Python, at mint time**. A token that is an `$alias` *target* is therefore consumed by
its path, never by a CSS `var()`.

**Proof, one example, four measured lines:**

| where | `--color-neutral-15` | `--background-default` |
|---|---|---|
| `canon.css` base `:root` | `#FFFFFF` (`:71`) | `#FFFFFF` (`:276`) |
| `canon.css` supercharge block | `#F7F6F4` (`:23679`) | `#F7F6F4` (`:23650`) |

`semantic-colour.json` gives `background/default` `"$alias": {"light": "color/neutral/15"}`;
supercharge's override set declares `color/neutral/15` (`$alias → color/warm/15`) and declares
nothing for `background/default`. `grep -rn "var(--color-neutral-15" --include=*.css --include=*.html
--include=*.js .` (minus `reviews/`) returns **zero**. The supercharge value can only have arrived
down the alias edge. Consumed — not an orphan.

Lane 1 counted this class as ~20 by family (`--color-neutral-*`); mechanically it is **17**, because
`--color-neutral-2`, `-3` and `-raise-3` are *not* alias targets. Three members of the family Dave
would have been told were fine are in fact orphans, and three that look like orphans are fine.

### (ii) ALIAS-SHADOW — 24 of the 47. A second class lane 1 did not separate, and it is the bigger half.

Supercharge's override file declares **28 keys**. The supercharge block in `canon.css` carries far
more, because `_expand_aliases` materialises an effective override for **every path alias-reachable
from a declared one**. Twenty-four of the "orphans" are that: theme-tier declarations **no override
file declares and no component reads**.

Probed directly against `gen_theme_cascade.alias_map()` and the override sets:

```
tooltip/background          declared=False  alias={light: color/neutral/15, dark: color/neutral/4}
primary/border/hover        declared=False  alias={light: color/neutral/4,  dark: color/red/700}
tertiary/text/pressed       declared=False  alias={light: color/neutral/15, dark: color/neutral/15}
tabs/badge/background       declared=False  alias={light: badge/background, dark: badge/background}
```

Nobody authored these. Calling them twenty forgotten wires would be twenty findings where there is
**one generator-scope question** (ruling-shaped Q3). The full 24:
`--tooltip-{background,border}` · `--primary-border-{hover,pressed,disabled}` ·
`--secondary-border-{hover,pressed,disabled}` ·
`--tertiary-{background-active,pressed,text-disabled,text-pressed}` ·
`--tabs-{badge-background,hover,pressed}` · `--data-vis-border-on-{dark,light}-{baseline-2,gridline}` ·
`--divider-border-subsectioninset` · `--form-border-pressed` · `--badge-host` · `--drop` · `--pri-icon`.

## 3 · The disposition table — every genuine orphan

Six. Line numbers are from the tree at `04655de` (lane 1's differ; `canon.css` moved at seam 2 —
[[premise-ages-faster-than-rule]], verify the line before quoting it).

| var | where | class | disposition / receipt |
|---|---|---|---|
| `--tabs-inactive` | base `:379` · legacy `:20068` · supercharge `:23775` | **(b)** ruled, consumer ambiguous | **NOT WIRED.** R-D23 + ADR-0014 cl.4 rule a per-theme state *mechanism*; the snippet fades all four themes with `--alpha-72`. Wiring measured live: legacy 5.25→**12.63** light, 9.06→**16.48** dark; supercharge 7.32→**9.47** light but 7.93→**5.59** dark. Nothing is below 4.5 today ⇒ **no breach to repair**, so this is a taste call. Row A of the review page. |
| `--padding-card-internal` | **no base declaration** · console `:22167` | **(b)** ruled, consumer ambiguous | **NOT WIRED.** s201-D4 ratifies the formula, s200-D3 narrows the mint to console. Two blockers: (1) it is the **only** one of the 394 per-theme mints with *no base declaration* — a consumer renders `padding:0` in mono/legacy/supercharge (rendered, not asserted, in Row B); (2) five card snippets carry three different paddings and the ruling names no surface. |
| `--size-segmented-control-min-hit-area` | base `:565` · console `:22191` | **(b)** ruled, consumer ambiguous | **NOT WIRED, and deliberately not re-put.** s201-D2/D3 rule the hit zone as `max(44, visual height)`; the mechanism *is* implemented, off `--target-min`. Two names, one 44 — that is lane 1 finding 7 / its ruling-shaped Q4, already Dave's. Re-asking it here would be a second surface for one decision. |
| `--color-neutral-2` | base `:58` · supercharge `:23680` | **(c)** no ruling names a consumer | **PROPOSED-for-park.** Probes below. ADR-0014 cl.1: *"A theme swaps its entire neutral substrate by overriding `neutral/1–15` — one 15-line block"*. A rung with no semantic alias pointing at it is the design working. |
| `--color-neutral-3` | base `:59` · supercharge `:23681` | **(c)** no ruling names a consumer | as above |
| `--color-neutral-raise-3` | base `:74` · supercharge `:23692` | **(c)** no ruling names a consumer | as above; ADR-0014 cl.3 calls the SC `raise-1..3` set *"CALCULATED … provisional-agent, on the review sheet"*. `raise-1`/`raise-2` are alias targets; `raise-3` is not. |

### The probes run before writing "no ruling" (verbatim)

Against **`knowledge/_rulings.json`**, all 250 records, whole-record case-insensitive substring match
(`/var/tmp/s219l5/probe.py`, copied to the evidence dir):

| probe string | hits | verdict |
|---|---|---|
| `neutral/2` | 0 | — |
| `neutral/3` | 0 | — |
| `neutral/raise` | 1 | s144-D1 (plus/minus coloured text) — inspected, unrelated |
| `elevation` | 1 | s142-D1 (binds authoring wave) — inspected, unrelated |
| `inactive` | 0 | — |
| `subsectioninset` | 0 | — |
| `tabs` · `badge` · `tooltip` · `pressed` · `icon/default` · `tertiary` · `card padding` · `segmented` | 5·6·6·8·2·0·5·11 | all read; the ones that bear are cited in this report by id |

Second surface, per [[unrun-search-indistinguishable-from-absent-record]] —
`python3 knowledge/_memento_search.py "tabs inactive token consumer"` and
`… "color neutral raise elevation supercharge"`: no ruling naming a consumer for any of the three.
ADR-0014 was found by reading the ADR, not by the ruling store — which is itself the point of
[[reference-the-adr-dont-duplicate]].

## 4 · Findings

**1 · There is no class-(a) work in this population.** Every orphan is either a taste call with a
measured downside or a designed reservation. The brief's premise — *"a consumer gap on
`--padding-card-internal` is an enactment gap, same class as the segmented radii"* — does not survive
contact: s201-D4 ratifies a **formula and a value**; it names no surface, and s200-D3 explicitly
withholds the mint from three of four themes. Enacting it would have been an invention of scope on
top of a dangling var in three themes. [[feedback-dont-launder-a-premise-into-a-ruling]]

**2 · Wiring `--tabs-inactive` would have been a silent regression, and only measurement caught it.**
The ruled remedy reads like a fix — supercharge's dark leg was re-picked to `warm/11 #AA9B92` *because*
the DNA index sat at 3.89:1. But the tab's ground is `tabs/background` (`#2A2621`), not the page: today's
fade lands **7.93:1** there and the ruled colour lands **5.59:1**. Wiring the ruled mechanism *lowers*
the contrast it was ruled to raise. I nearly filed this as an a11y defect off arithmetic before driving
it in a browser. [[green-tests-cannot-see-scope]]

**3 · `--padding-card-internal` is the only per-theme mint with no base declaration.** 394 mints, one
in that position. Any consumer of it renders **`padding: 0`** in mono, legacy and supercharge —
verified by rendering, not reasoned: the three "wired, NO base mint" cells on the review page read
`resolved padding 0px`. This is the padding twin of [[dangling-dataviz-var-renders-silent-black]], and
no gate sees it because the gates all check *uses*, and this one has none yet.

**4 · The theme cascade emits declarations nobody authored.** 24 of the 47. This is not a defect —
`_expand_aliases` is doing exactly what ADR-0014 designed — but it means the "unconsumed mint" signal
is 51% noise on the theme tier before any judgement is applied. Suppressing unconsumed shadows is a
generator-scope change (Q3), not a repair.

**5 · The base tier is where the number actually lives, and it is mostly by design.** 265 base-tier
orphans. The family histogram says why: `color-illustration` 72 · `color-supporting` 35 · `data-vis`
26 · `color-warm` 15 · `typography-letter-spacing` 9 · `typography-paragraph-spacing` 9 ·
`gap-fixed` 8 · `color-grey` 7 · `typography-font-weight` 6 · `motion-duration` 6 · `elevation-decorative`
5. These are **whole primitive ramps and DTCG metric families exported from Figma** — and ADR-0011
tier 1 says primitives belong to no theme. A primitive tier is *supposed* to be wider than what the
semantic tier selects. **This is the single strongest argument for keeping the new gate advisory:**
a blocking version would fire 265 times on day one, and would be wrong ~250 of them.

**6 · Two ratified values paint nothing, and both are recorded as questions rather than acted on.**
`--tabs-badge-background`: s123-D4 ratified supercharge's value ("SC badge is fine"), and s149-D1 then
wrote an explicit guard into the cascade — *"s149-D1 is MONO ONLY … preserve the pre-existing `.ovcount`
paint (`--tabs-active`/`--text-reverse`) rather than inherit mono's new badge seat"* (`canon.css:21590`,
`:23291`, `:26666`). So the ratified colour is fenced off by a later ruling. `--pri-icon`: s170-D4
ruled the legacy primary-button icon white and it is minted `#FFFFFF` in the legacy `.cn-button` block
— but `grep -c "<svg" knowledge/snippets/Button.reference.html` = **0**. The Button snippet has no
icon. The ruled value is correct and has no picture; `--pri-label` is the same `#FFFFFF`, so wiring it
would be a null visual delta plus an invented icon variant.

**7 · s149-D1 IS enacted, contrary to its own `status` field.** The record still reads *"RULED #149,
NOT ENACTED. No value moved in any token or canon file. Enactment is #150 lane 1"*. The `.ovcount`
re-point is live in `Tabs.reference.html:105-107` and `canon.css:2896`, with the s149-D1 comment
attached. A stale `status` on a ruling is the [[conclusions-are-debt-s129-d5]] class in the store
itself. **Not corrected — `_rulings.json` is DO-NOT-RULE for this lane.** Flagged for the conductor.

**8 · Nothing was regenerated.** No generator this lane owns emitted anything: no token store changed,
so `gen_theme_cascade` / `gen_canon_tokens` / `gen_snippet_tokens` have nothing to re-run, and the
regen serial set was correctly not entered. The only repo edits are one new gate, two lines of wiring
in `_build_all.py`, one new review page, and three store rows.

**9 · Three new documents need store rows (#185) — added, not left owed.** `W-99zj`
(`_gate_minted_consumption.py`), `W-99zk` (the review page), `W-99zl` (this report), all via
`_state.py add()`. `_gate_doc_rows.py` re-run: **PASS, unrowed 0** — but note it reports
"staged-in-THIS-commit 0", the #207 single-commit blindspot lane 1 also hit, so its green is not
evidence for the new files until they are staged.

## 5 · What was built

**`knowledge/_gate_minted_consumption.py`** — ADVISORY, the mirror of `_gate_dataviz_vars.py`.
That gate asks *"does this use resolve?"*; nothing asked *"is this mint read?"*. Reports
declared / consumed / ALIAS-TARGET / ALIAS-SHADOW / ORPHAN split by tier, every orphan named with
theme and line. **Exits 0 always** — only an unrunnable inventory (exit 2) can surface.

Wired into `_build_all.py` as steps **100** (ADVISORY) and **101** (selftest, ABORT — an inventory
whose mutants stop going red is a measuring tool that has quietly stopped measuring). It has a
consumer on purpose: [[instrument-without-a-consumer]].

Selftest — 10 arms, **all green**, both directions plus a mutant per subtraction:

```
[1]  green control: real canon.css parses and classifies      PASS  declared=973 consumed=600 orphan=265
[2]  a heavily-consumed var (--border-radius-default) unflagged PASS  (bite-the-bite)
[3]  plant --gate-selftest-orphan in a console block           PASS  -> ORPHAN, by name
[4]  same name, now var()-ed from inside the glob              PASS  -> not flagged
[5]  consumer moved to reviews/ (excluded)                     PASS  -> ORPHAN again (the glob is real)
[6]  $alias target --color-neutral-15                          PASS  -> ALIAS-TARGET, not ORPHAN
[7]  MUTANT subtract_alias_targets=False                       PASS  -> --color-neutral-15 goes ORPHAN
[8]  --tooltip-background ALIAS-SHADOW / mutant ORPHAN         PASS  -> both legs
[9]  missing canon.css                                         PASS  -> GateError, named
[10] empty consumer population                                 PASS  -> GateError, named
```

`python3 knowledge/_build_all.py --selftest` → **`selftest PASS — exact-ID failure routing over 130
steps`** (was 128; both new rows resolve, no stale rows).

`python3 knowledge/_gate_doc_rows.py` → **PASS, unrowed 0**.
`python3 knowledge/_validate_help_gate.py` → **7 reds, none mine** — all seven are pre-existing
`knowledge/_render/verify_*_218.py` files (`verify_behaviour_218w3_{media,nav,overlay}`,
`verify_phantom_surfaces_218`, `verify_wave3_{alpha,beta,gamma}_218`). The new gate carries the help
gate and is not in the list. Named so the conductor does not attribute the red to this lane
[[a-crash-is-not-a-fail]].

**`reviews/UNCONSUMED-MINTS-2026-08-25-v1.html`** — PROPOSED decision surface. Real `canon.css`, real
`[data-apollo-theme]`, markup copied from the reference snippets ([[specimen-starts-from-reference]]).
The "wired" column is a page-local projection scoped to `.proj`; **every contrast and padding figure is
measured in the browser off `getComputedStyle`**, not typed into the page and not computed by a script
that emulated the cascade — my own hand-rolled emulation got legacy-dark and supercharge-dark wrong
before the browser corrected it. 19 cells, **0 page errors, 0 unmeasured**.

**Mutation arm, red by name** (`verify.py --mutate` repoints the projection at an undeclared var):
every Row-A "wired" cell changed (supercharge dark 5.59→15.03, supercharge light 9.47→16.11), every
Row-B "wired" cell collapsed 20px→0px, and **every "today" cell was unchanged** — so the projection
was genuinely reading the minted token and the control genuinely controls.

---

## RULING-SHAPED QUESTIONS

**1 · Does the inactive tab keep its fade?** R-D23 and ADR-0014 cl.4 rule the state mechanism as a
theme property — supercharge *colour*, legacy *none* — and the snippet fades all four. Wiring the ruled
mechanism is measured on Row A: legacy improves markedly both modes, supercharge-light improves,
**supercharge-dark drops 7.93→5.59**. Nothing is below 4.5 today, so there is no breach forcing the
call. **(a)** wire it as ruled and accept the SC-dark drop; **(b)** wire legacy only; **(c)** leave the
fade and retire `tabs/inactive`; **(d)** re-tune the SC dark leg against `tabs/background` (its note
computed 7.01:1 against the *page*, a different ground) and then wire. Recommendation withheld — this
is a curve/ink judgement on your own ramp.

**2 · Which surfaces are "the card", and does the base padding mint?** s201-D4 ratified the formula and
s200-D3 kept the mint console-only. Two decisions, in order: does `padding/card/internal` mint for
mono/legacy/supercharge by the ruled formula (their `border-radius/surface` values are the inputs and
are already on disk), or does the consumer carry a declared fallback token? And *then*: which of
`Cards` (body 16, action 12, media 16, option 16), `Account-card`, `Stat-card`,
`Card-header-lockup`, `Payment-card-visual` is in scope? Until the first is answered a wire is
unsafe — Row B renders the collapse.

**3 · Should the cascade emit an alias-shadow at all?** 24 theme-tier declarations no override file
declares and no component reads, each a mechanical consequence of the DNA override. Priced: a
`_expand_aliases` post-filter that drops an expanded path with no manifest binding and no `var()`
consumer, plus a selftest arm asserting the emitted block shrinks and no *consumed* path is lost. It
changes generated output for three themes, so it is a promotion decision, not a repair.

**4 · Do reserved slots get to say so?** A `$reserved` (or `$consumer`) field on a token is the only
thing that can separate a forgotten wire from a deliberate one — and therefore **the only thing that
could ever promote the new gate from advisory to blocking**. Priced: one schema field, a `_validate_dtcg`
arm, and the gate reading it. Without it, the honest posture is permanent advisory. This is the same
shape as the ADR-0010 "declared slots" idea, so it may already have a home.

**5 · The ratified-but-fenced pair.** `--tabs-badge-background` — s123-D4 ratified supercharge's badge
colour, s149-D1's guard then kept supercharge off the badge seat; the ratified value paints nothing.
`--pri-icon` — s170-D4 ruled the legacy primary-button icon white, and no primary button in the library
has an icon. For each: does the ruling stand as a reservation, retire, or is a consumer owed?

---

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: `_build_all.py` end-to-end.** A full single-process run is sandbox-impossible (declared
  in the brief). The two new steps were driven **individually** (`python3
  knowledge/_gate_minted_consumption.py` → rc 0; `--selftest` → rc 0) and the routing table was proved
  by `_build_all.py --selftest` over 130 steps. `--range 100-101` **refuses by design** ("a pass must
  START at step 1"), so the steps have not been observed executing *inside the runner loop*. Price to
  prove: one full build, which does not fit a sandbox call.
- **UNPROVEN: that the 265 base-tier orphans are all by-design primitive breadth.** The family
  histogram is strong evidence and ADR-0011 tier 1 supports it, but I inspected the families, not the
  265 names. Some *are* likely real gaps (the 26 `data-vis` ones sit next to the DV programme). Price:
  one pass reading the 265 against their stores, ~1 window. Named rather than assumed.
- **UNPROVEN: that no consumer reaches these tokens through a runtime-built name.** The gate cannot
  see `style.setProperty('--' + k)`. I did not grep for that construction. Price: one grep plus a
  judgement call on each hit.
- **CLAIMED (declared, not re-read): lane 1's report is the source for "17 sessions dark" and for the
  `.seg` duplication count.** I read its findings section; I did not re-derive them.
- **NON-REPO, declared per s191-D2:** the exploratory sweep (`/var/tmp/s219l5/sweep.py`), the ruling
  probe (`/var/tmp/s219l5/probe.py`) and the render driver (`/var/tmp/s219l5/verify.py`) are non-repo.
  All three are **copied into the evidence directory** so they survive the window. The durable
  instrument is `knowledge/_gate_minted_consumption.py`; the render driver is deliberately not
  promoted, because the review page measures itself and the driver only reports what the page produced.

## Files left in the working tree (for the conductor's reconcile — no blind `git add -A`)

| path | what |
|---|---|
| `knowledge/_gate_minted_consumption.py` | **NEW** — the advisory inventory gate |
| `knowledge/_build_all.py` | **EDITED, 2 hunks** — STEPS rows 100/101 + their ROUTE_ROWS rows. No other line touched. |
| `knowledge/_state.json` | **EDITED** — 3 rows appended via `_state.py add()` (`W-99zj`/`W-99zk`/`W-99zl`) |
| `reviews/UNCONSUMED-MINTS-2026-08-25-v1.html` | **NEW** — PROPOSED decision surface |
| `notes/_subreports/2026-08-25-219-lane5-unconsumed-mints.md` | **NEW** — this report |
| `notes/_subreports/assets/2026-08-25-219-lane5-unconsumed-mints/` | **NEW** — evidence, below |
| `knowledge/_graph-mark-observations.jsonl` | **EDITED, +47 lines, PARTLY MINE.** 30 are my two ruling probes (`"tabs inactive token consumer"` 12 · `"color neutral raise elevation supercharge"` 18) — written as a side effect of `_memento_search.py`. The other **17** (`"memento-package verbatim set re-sync authori…"`) are **another lane's**. |

⚠ **NOT MINE, present at reconcile time:** `knowledge/_validate_hidden_display.py` and
`notes/_subreports/2026-08-25-219-lane6-gates-backlog.md` — a concurrent lane 6 appeared in the tree
during this lane. My `_build_all.py` diff is **insertions only, 16 lines, two hunks**, so it cannot
have clobbered a concurrent edit to that file; verify with `git diff --stat` before staging.

⚠ Gates that rewrite files as a side effect were **not** run this lane (`gen_thumbs`, the type
ratchet, the memento index), so none of lane 1's incidental-churn class is mine.

## Evidence

`notes/_subreports/assets/2026-08-25-219-lane5-unconsumed-mints/`

- `unconsumed-mints.png` — the review page, full-page render, seen.
- `verify.py` — the render driver, with its `--mutate` arm.
- `sweep.py` — the independent exploratory sweep, run before the gate existed (it is what produced
  the first 394/47 reading, so the gate's agreement with it is a second measurement, not a restatement).

REPLAY-THESE: `reviews/UNCONSUMED-MINTS-2026-08-25-v1.html` — **open it, do not read it**; Rows A and B
are Dave's eye · ruling-shaped Q1 and Q2 (~600 tk) · finding 7, the stale `s149-D1` status (~120 tk,
conductor's to correct or leave).
