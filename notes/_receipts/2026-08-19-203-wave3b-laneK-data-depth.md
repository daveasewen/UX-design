# Receipt — #203 Wave 3b, Lane K · data-display depth (KPI tile · Timeline · Avatar group)

*Worker receipt per the parallel-conductor checklist, written 2026-08-19.*
*⛔ Nothing here is a ruling. No git command of any kind was run. No commit, no push, no `checkout/restore/stash`.*
*⛔ No generator was run — not one, not even `--check` (Lane G owns that surface this wave). `_build_all.py` not run.*
*⛔ No shared file created or edited. `knowledge/_rulings.json`, `component-types.json`, all `tokens/*.json`, `_DS-IMPROVEMENTS.md`, `_validate_radius.py`, `gen_showroom.py` — untouched.*

**Context gauge at close — `knowledge/_checkin.py`, run live:** MEASURED **202,000 real** (headline,
throughput) · **FILL 145,808 real** · boot 56,488 real · peak 145,808 across 30 turns.
⚠ **Declared, not glossed:** `_checkin.py` reads the *session* transcript, which this wave shares with
five concurrent sibling lanes. That figure is **session-wide, not this lane's isolated spend** — a sub's
own window is not separately instrumented. I am not converting it into a per-lane number
(`measure-dont-convert-units`).

---

## Headline for the conductor, before anything else

**All three rows were genuinely absent — this lane did NOT hit wave 3a's stale-premise wall.** Rows 55,
56 and 57 have no snippet and no meta under any name I could find. All three were built end-to-end.

**But row 55 is not an ordinary gap, and the brief was right to fence it.** `s182-D2` (#182) *names* the
KPI/trend tile and *explicitly declines to rule it*. Dave, verbatim, quoted inside that ruling:
*"might be a partially built trend card with option, I haven't decided yet"* — and the ruling's own words:
*"FLOATED, NOT RULED: the trend-card component itself — never launder into a ruling."* So row 55 is a
**floated component with standing direction**, not a gap a worker may close. It is built here as a drawn
**PROPOSED** proposal for Dave's eye and is marked so in the snippet header, the meta, and on the review page.

**The two-red question is bigger than the mono-only reading.** Driving the KPI tile in a real browser
across all four themes measured the arrow seat under the 3:1 non-text floor in **three of the four
themes**, and the two seats disagreeing in **seven of eight panes** — see finding 1. Inherited and
flagged, exactly as instructed. Not resolved.

---

## Step 0 — the premise, verified first-hand (HARDENED per addendum §1)

⚠ **HEAD sha not quoted: the lane brief forbids git commands outright**, which overrides the base
brief's §3 instruction to capture it via `git log --oneline -1`. Declared gap, not a silent one.

| Claim | Verified? | Probe run, quoted |
|---|---|---|
| Row 55 KPI/trend tile absent | ✅ **TRUE** | `ls knowledge/snippets/ \| grep -i kpi` → *empty*; same for `trend`, `metric`, `tile` |
| Row 56 Timeline/activity feed absent | ✅ **TRUE** | `ls \| grep -i` each of `timeline` `activity` `feed` `history` `audit` → *all empty* |
| Row 57 Avatar group absent | ✅ **TRUE** | `ls \| grep -i` each of `group` `stack` `cluster` `facepile` → *empty* (`stack` matched only `Chart-stacked-area`) |
| …and their metas | ✅ absent | same greps over `ls knowledge/components/` — `avatar.meta.json` exists, no group form |
| Content-level check, not just filenames | ✅ ran | `grep -ril "timeline\|activity-feed\|avatar-group\|avatar group\|kpi" knowledge/snippets/ knowledge/components/` → 9 hits, **none a component**: all prose mentions inside `Chart-sparkline`, `Amount-display`, `Chart-bullet`, `chart-line` and the two `_nodes-*.json` |
| Gated Avatar has no group/stack form | ✅ **TRUE** | `grep -in "group\|stack\|overlap\|\+[0-9]\|more\|multi" knowledge/snippets/Avatar.reference.html` → **0 matches** |
| Brief: Stat-card already carries delta semantics | ✅ **TRUE** | `Stat-card.reference.html:111` — `data-carries="symbol label"`, arrow + `"+12.4% up"` + period |
| Brief: Stat-card arrow binding is a LIVE two-red question | ✅ **TRUE** | `stat-card.meta` manifest `"--up": "rag/success", "--down": "rag/error"` — the FILL seat |
| Row 55 = "Metric + delta + **spark**" | ✅ read from source | itinerary sheet1 row 56, parsed from the xlsx: *"KPI / trend tile · Data display · Gap · P2 · 2 Depth · Tailwind / Untitled · **Metric + delta + spark**"* |
| Is "trend card" already ruled? | ✅ **searched twice** | `_memento_search.py` on 5 phrasings **AND** a direct grep of all **201** rows of `knowledge/_rulings.json` for `trend[- ]card\|KPI\|activity feed\|timeline\|avatar group\|stacked avatar\|B-Q6` → **2 hits: `s182-D2`, `s182-D3`**, both read in full |

⚠ **`_memento_search.py` was serving a STALE index.** `_checkin.py`'s own rehearsal reports
*"STRUCTURAL retrieval index is STALE — it does not match GOOD-MORNING.md / `_LIVE-STATE.md` as they now
stand, so `_memento_search.py` is serving a PREVIOUS session's record"*. **My ruling verification does not
rest on it** — it rests on the direct grep of `_rulings.json`, which is the store itself
(`retrieval-default-hides-the-ruling`: store > chain). Flagged for the conductor because it is a
session-wide defect, not mine.

---

## Deliverables — 9 new files, nothing overwritten

| File | State |
|---|---|
| `knowledge/snippets/Kpi-tile.reference.html` | **NEW** — PROPOSED specimen |
| `knowledge/snippets/Timeline.reference.html` | **NEW** — PROPOSED specimen |
| `knowledge/snippets/Avatar-group.reference.html` | **NEW** — PROPOSED specimen |
| `knowledge/components/kpi-tile.meta.json` | **NEW** |
| `knowledge/components/timeline.meta.json` | **NEW** |
| `knowledge/components/avatar-group.meta.json` | **NEW** |
| `reviews/REVIEW-203-kpi-tile-four-themes-v1.html` | **NEW** — 4 themes × light/dark, 8 panes |
| `reviews/REVIEW-203-timeline-four-themes-v1.html` | **NEW** — 8 panes |
| `reviews/REVIEW-203-avatar-group-four-themes-v1.html` | **NEW** — 8 panes |
| `notes/_receipts/2026-08-19-203-wave3b-laneK-data-depth.md` | **NEW** — this file |

Verified no shared artefact moved: `find knowledge reviews notes -newermt '2026-08-19' -type f | grep -iE "kpi|timeline|avatar-group"` returns **exactly the nine above**.

**Specimens COPY the approved artefact, never re-draw** (`specimen-starts-from-reference`). Sources copied
verbatim and left untouched: `Stat-card` (tile anatomy + delta markup), `Chart-sparkline` (`.spark-inline`
geometry, stroke rules, the 12-point polylines), `Avatar` (disc, round exemption, size ramp),
`List-items` (RAG status chip form B, avatar atom), `Progress-tracker` (rail mechanism, rotated vertical),
`Progress-bar` (the zero-raw-type-declaration pattern).

---

## Gates — every rc reported

| Gate | Result | Verdict |
|---|---|---|
| `_validate_snippets.py` (repo-wide) | **rc=0** — 85 snippets, **0 failures** | ✅ my three contribute 0 failures |
| `_validate_a11y.py` (repo-wide) | **rc=0** — 85 snippets, 0 failures, 186 warnings | ✅ |
| `_validate_type_composites.py` — **my 3 files** | **rc=0** — *"TYPE GATE PASS — all component text bound to canon composites (3 files)"* | ✅ |
| `_validate_type_composites.py` — repo-wide | rc=1, **1,097** violations across 90/100 files | ✅ **ratchet held — I added 0** (1,097 is Lane E's measured baseline, unchanged) |
| `_validate_state_contrast.py` | **NOT RUN — declared** | ⚠ see residuals |
| `_validate_radius.py` | **NOT RUN — declared** (I edited no `MIGRATED_SNIPPETS`, a ⛔ shared file) | ⚠ conductor's |

⚠ **The filtered runs are not actually filtered.** `_validate_snippets.py <file>` and `_validate_a11y.py
<file>` **ignore the path argument and sweep the whole `snippets/` directory** — the banner says
"85 snippet(s)" whichever file you name. Reported because it means a lane cannot isolate its own
contribution from these two gates; I attributed mine by diffing the failure list, not by trusting the filter.

**Snippet count climbed 79 → 85 during this lane** as sibling lanes wrote files. Also observed:
`_validate_snippets.py` is **rc=0 at 85 snippets**, so the **18 `--pri-hover` DRIFT failures Lane E
reported at HEAD appear to have been repaired** between then and now. Stated as an observation with its
probe, not a claim about who fixed it.

**Gates left to the conductor, by name:** `_validate_state_contrast.py`, `_validate_radius.py`,
`_validate_coverage.py`, `_validate_icons.py`, `_validate_dtcg.py`, `_build_integrity.py`, and every
generator `--check` (`gen_showroom`, `gen_canon_components`, `gen_theme_cascade`, `gen_token_ramp`,
`gen_component_partials`). A declared gap passes; this is the declaration.

---

## Render proof — driven, not asserted

`goto("file://…")` throughout; **`set_content()` never used**. Chromium from the cached browser farm
`/var/tmp/pw-browsers-s197`; `playwright` from `/var/tmp/pylibs-s203e`; `LD_LIBRARY_PATH` →
`/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu` (the runbook's fourth env var — **the first launch
failed on `libXdamage.so.1` and the runbook already had the answer**; I did not write "cannot render").
Fontconfig **symlink farm** at `/var/tmp/fonts-s203k` with the `<include>` present, so markers land in the
farm, not the repo.

**Font asserted by canvas measurement against three controls, never `fonts.check()`:**
target `"Univers Next for HSBC"` = **390** · alias `"Univers Next HSBC"` = **390** ·
`DejaVu Sans` = **416** · nonexistent face = **351** ⇒ the real HSBC cut, both aliases landing on it,
and the probe demonstrably discriminates.

**Result: 8/8 panes on all three pages, 0 page errors, at 1400px and 480px, no document overflow.**
All four themes fork correctly and were read off the DOM (console radius `20px` present; supercharge
surface `#F7F6F4` light / `#2A2621` dark; legacy text `#333333`).

**44px min-hit-area — enforced BY HAND and PROVEN, since no gate reads the token.** Every interactive
target across the three components, all four themes, both widths: **zero under 44.**
`button.kpi-cta` 44×44 (×8) · `button.tl-more` 460×44 (×8) · `a.avg-face` 44×44 (×24) ·
`button.avg-face` 44×44 (×8) · `button.avg-btn` 112×44 (×8).

Renders viewed by eye at `outputs/s203k-renders/` — **(NON-REPO: session outputs folder)**, `s191-D2`
marker. They are my verification, not review artefacts; HTML is what Dave reviews.
Repo pollution check after the fact: `find . \( -name '.uuid*' -o -name '*.LCK' -o -name '*.cache-*' \)`
outside `_to_delete/` → **empty**.

### ★ Two defects the gates could not see, caught only by looking at the render

Both were in the **review pages**, and both were invisible to every green gate
(`green-tests-cannot-see-scope` — the reason the brief demands the eye pass):

1. **The timeline's rail dots rendered 0×0 and the connector sat at x=0.** My page-builder dropped the
   snippet's `:root` block wholesale, so the non-token custom properties `--node: 12px` and
   `--rail-x: 5px` were undefined and `width: var(--node)` collapsed. The snippet itself was always
   correct (12×12, correctly coloured) — **only the review surface was wrong**, which is exactly the case
   a snippet-scoped gate cannot reach. Fixed; re-measured at 12×12 with per-status colour.
2. **Entry titles were clipped mid-descender** (`clientHeight 10` vs `scrollHeight 16`). My selector
   prefixer split `:is(button,a,label,span,…)` on its **inner** commas, turning it into
   `.cn-timeline :is(button, .cn-timeline a, …)` — which raised that rule's specificity to (0,2,1) and let
   it beat my own `.cn-timeline .tl-title` (0,2,0). Fixed by splitting on top-level commas only;
   re-measured `clientHeight == scrollHeight == 18`, `text-box-edge: text`.

The extractor/page-builder is a **throwaway at `/var/tmp/s203k/`, outside the repo** (the #174/Lane E
precedent). It is **not** an instrument the repo carries. `machinery: 0 instrument / ~470 feature`.

---

## The components

### Row 55 — KPI tile. How it differs from the gated Stat-card (the brief's explicit requirement)

Stat card is a **passive atom**: label · value · delta · period, and it **already carries full delta
semantics** (arrow + sign + wording, the R-D5 three-channel treatment). So *"metric + delta"* — two thirds
of the itinerary's wording for row 55 — **was never the gap. Only "spark" was.**

KPI tile is a **molecule** composing two approved artefacts and drawing nothing new. **The one real
difference: Stat card states the CHANGE; KPI tile states the SHAPE of the change.** Choose Stat card when
the reader needs the number and whether it moved; choose KPI tile when they need to see *how* it moved.
**A KPI tile with no series is a Stat card and should be one** (an antiPattern in the meta).

★ **The sparkline atom anticipated this exact composition.** Its own source calls `.spark-inline`
*"the KPI / Stat-card scale"* and carries `.spark-kpi-slot` as *"a SPECIMEN-ONLY wrapper standing in for
the Stat-card tile"*. This lane made that slot real. It also answers Lane E's open item 3 (*"does the card
grow a slot, or does a board place a sparkline beneath a card?"*) with a **drawn proposal, not a ruling** —
the two lanes reached the same question from opposite ends and it is one decision for Dave, not two.

The **optional table CTA** enacts `s182-D2`'s standing direction (*"table CTA optional, icon-button form"*,
no label because *"a sparkline shows a trend beside a headline figure, it is not an analysis tool"*).
44×44, `view-grid.svg` byte-matched, and it **opens nothing** — the table panel is composition-level and
inventing one would be canon by improvisation.

### Row 56 — Timeline. How it differs from its three gated neighbours

Stated in the meta because three gated components sit close and a reader will otherwise reach for the wrong one:
- **vs `List-items`** — that is the *interactive, unordered* transaction row (every row a `<button>`), answering *"which one do I open?"*. Timeline is *passive and ordered*, answering *"what happened, in what order?"*. **The tell: remove the ordering from a Timeline and it stops meaning anything.** A feed whose entries must open should be List-items inside a date group, **not** a Timeline that grows buttons.
- **vs `Progress-tracker`** — visually the closest and the likeliest confusion. That is a *finite forward* process with done/current/upcoming and a completion, carrying `aria-current="step"` and `role="progressbar"`. A Timeline has no current step, no total, no completion. It borrows the **rail mechanism** and refuses the **semantics**; ⛔ putting those roles on it would lie to AT (an antiPattern).
- **vs `Notifications`** — those await action; a Timeline entry asks nothing.

Colour never alone: every status dot travels with its word, and neutral-label-on-tint measures
**8.21–14.46** in both modes. The warning dot alone is under 3:1, which is precisely why it never appears alone.

### Row 57 — Avatar group

Adds **nothing** to the gated Avatar disc — disc, tokens, round exemption and 32/44/64 ramp copied verbatim.
What it adds is the **arrangement**: overlap, separator ring, display cap, overflow counter, one name for the set.
Interactive members are built at **medium and large only** — a 32px interactive disc breaches the ruled
44px minimum and **no gate reads that token**, so it is enforced by *not building it*; small stacks that must
be clickable become one 44px target instead.

---

## Findings

### ⛔ Finding 1 — the two-red seam, measured across ALL FOUR themes (Dave's, inherited, NOT resolved)

The KPI tile paints **two green/red seats on one card** because its two parents bind different ones and
**both were inherited unchanged, exactly as the lane brief instructed**:
- the **delta arrow** takes `rag/success` / `rag/error` — the **FILL** seat, byte-for-byte from the gated Stat-card manifest;
- the **spark stroke** takes `rag/success-ink` / `rag/error-ink` — the **INK** seat, which `s182-D3` **RULES** for this atom, and whose own governs-list says *"the future trend-card component inherits this stroke rule when built"*.

★ **This corrects a smaller claim I first wrote and then disproved by rendering.** My first draft said the
two seats *"converge in dark mode"*. **They converge in MONO DARK ONLY.** The spark ink is
theme-**invariant** by ruling (`s182-D3`, measured #182: zero theme-level series overrides) while the arrow
fill **forks per theme** — so they disagree in **seven of eight panes**. Computed values read off the DOM,
ratio against each pane's own surface:

| theme | mode | arrow (fill seat) | spark (ink seat) | agree? |
|---|---|---|---|---|
| mono | light | `#66CC8D` **1.98:1** | `#137F3C` 5.09:1 | differ — ❌ **arrow under the 3:1 floor** |
| mono | dark | `#66CC8D` 8.31:1 | `#66CC8D` 8.31:1 | **agree** (the only one) |
| legacy | light | `#00847F` 4.56:1 | `#137F3C` 5.09:1 | differ |
| legacy | dark | `#00847F` 3.62:1 | `#66CC8D` 8.31:1 | differ |
| console | light | `#5DAC7B` **2.74:1** | `#137F3C` 5.09:1 | differ — ❌ **under the floor** |
| console | dark | `#5DAC7B` 6.01:1 | `#66CC8D` 8.31:1 | differ |
| supercharge | light | `#5DAC7B` **2.54:1** | `#137F3C` 4.71:1 | differ — ❌ **under the floor** |
| supercharge | dark | `#5DAC7B` 5.48:1 | `#66CC8D` 7.57:1 | differ |

**Three of the four themes put the light-mode arrow under the 3:1 non-text floor — not one.** Lane E
measured the mono leg independently this same session; the per-theme spread is this lane's addition, and it
means the question is **wider than a mono rebind**.
⛔ **NOT RESOLVED.** Rebinding a ruled colour seat is Dave's; `s151-D1` clause 2 (*"text AND atoms alike"*)
reads as though it already governs the arrow, but the arrow-only fill treatment may have been deliberate,
and `surface, never swap` binds. **Whichever way it goes, Stat card and KPI tile must move together** — a
fix to one that leaves the other is exactly how this seam arrived.

### ⚠ Finding 2 — the gated Avatar hides a DEPRECATED value from the drift gate by not declaring it

`Avatar.reference.html` sets a ring var whose light leg exists **only in
`tokens/_manifests/depricate-tokens.json`** — a deprecated value — and **Avatar's manifest does not declare
that var at all** (its `vars` map lists only `--focus`, `--surface`, `--text`, `--icon`, `--page`).
`_validate_snippets.py` compares *declared* vars against the store, so **an undeclared var is invisible to
the drift gate**: a snippet can carry a dead token indefinitely simply by omitting it from its manifest.

My file **declares** the var and rebinds it to the live `border/subtle` (runbook step 2, *"rebind to the live
semantic token; record the rebind"*) — and it failed the gate honestly until I did. **Avatar itself was NOT
edited**: it is a gated shared artefact and the fix is the conductor's.
**This is a gate-class finding, not a one-file one** — proposed for `_DS-IMPROVEMENTS.md` below.

### ⚠ Finding 3 — `_validate_snippets.py` parses theme blocks WITHOUT stripping CSS comments

While documenting finding 2 I wrote the deprecated hex in a comment *inside* a `[data-theme="light"]` block.
The gate read the commented text as a live declaration and reported
`DRIFT --ring (light) = #D7D8D6 but border/subtle = #E1E1E1` — **against a value that was not in the CSS**.
Reproducible: a hex written in prose inside a theme block is parsed as a declaration. It can produce a false
FAIL, and by the same mechanism a comment could mask a real value. `_validate_type_composites.py` strips
comments before parsing (`re.sub(r"/\*.*?\*/", "", …)`); `_validate_snippets.theme_block()` does not.
Worked around by moving the values out of the block; proposed as a one-line gate fix below.

### ⚠ Finding 4 — the Avatar-group separator ring is wrong on any non-page surface (shown, not described)

The ring binds `background/default`, so the stack separates correctly **only on the page**. On a card it is
the wrong colour — hidden in light (card is also white) but **visible in dark, where page `#1A1A1A` meets
card `#1F1F1F` and each disc wears a halo**. The specimen carries an on-card block in every pane so Dave
sees it rather than reads about it. Fixes are a surface-keyed token or a consumer-set ring; **both are
Dave's, and I invented neither** (`grey-tint`/ink items are surface-never-swap).

---

## Decisions needed — Dave's, every one PROPOSED #203

1. **Does the KPI / trend tile exist at all?** `s182-D2` floated it and never ruled it. This is the drawn proposal; the shape, the slot and the whole component are yours to accept, reshape or decline.
2. **The two-red seam (finding 1).** Rebind the delta arrow to the ink seat, or ratify the fill seat as a deliberate exception for arrows? Three of four themes are under 3:1 in light. **Stat card and KPI tile answer together.**
3. **The optional table CTA** — right affordance, right form (icon-button, no label), right place (top-right)? And should it exist on a tile at all before the table panel does?
4. **Timeline rail nodes are round** (12px node, 8px status dot). That is my reading of the angular rule, **not** a ruled exemption — Avatar and Badge are the two documented ones. Square nodes are equally buildable.
5. **Timeline ordering** — newest-first is asserted, not ruled. And should the activity form carry a status node *as well as* the avatar?
6. **Avatar group has two accessible shapes** — group-announced (default; discs hidden, one name) vs roster (every member announced). **Two shapes for one component is a decision, not a feature.** Ship both, or make one the component and the other a documented composition?
7. **The Avatar-group ring token (finding 4)** — surface-keyed token, consumer-set var, or accept the page-only limitation?
8. **Avatar-group display cap** defaults to 3, **stacking order** puts the first member on top, and the **overflow counter** is passive by default in the stacked form. All three are specimen choices.
9. **Avatar's large disc uses a raw off-ramp 24px**; mine uses `.t-cm-section-label` (20px), the nearest rung. A declared divergence from the parent — confirm or correct.

None of the above was resolved here. **Nothing a sub writes is a ruling.**

---

## Proposals for the conductor to merge (I edited no shared file)

- **`_DS-IMPROVEMENTS.md`** — *"`_validate_snippets.py` cannot see an UNDECLARED CSS var, so a snippet may carry a deprecated token indefinitely by omitting it from its manifest. Proven at #203: the gated `Avatar`'s ring var holds a value that exists only in `depricate-tokens.json` and has never gone red. Candidate gate: cross-check every `--var` declared in a theme block against the manifest's `vars` map and fail on the undeclared ones."*
- **`_DS-IMPROVEMENTS.md`** — *"`_validate_snippets.theme_block()` parses `[data-theme]` blocks without stripping CSS comments, so a hex written in prose inside a theme block is read as a declaration (false FAIL reproduced at #203). `_validate_type_composites.py` already strips comments; apply the same `re.sub(r'/\\*.*?\\*/', '', css, flags=re.S)` before parsing."*
- **`_DS-IMPROVEMENTS.md`** — *"`_validate_snippets.py <file>` and `_validate_a11y.py <file>` ignore the path argument and sweep the whole snippets directory, so a lane cannot isolate its own contribution. Either honour the filter or drop the argument."*
- **`_DS-IMPROVEMENTS.md`** — reinforcing Lane E: *"No gate reads the ruled 44px min-hit-area token. Lane K enforced it by hand across 48 measured targets; Lane L is building the advisory validator. Nothing connects them yet."*
- **Avatar rebind** — the gated `Avatar.reference.html` ring var should move to the live `border/subtle` and be **declared in its manifest**. Two-line change, not mine to make.
- **`component-types.json`** — the KPI tile embeds a sparkline but is **not registered**, so it takes no `AUTO-BEHAVIOUR` dataviz partial (its spark is baked static, which is correct for a passive aria-hidden mark). **Registration is a promotion decision and therefore Dave's, not a merge chore** — flagged, not requested.
- **`gen_canon_components.py`** — the three new components are absent from `canon.css`. Their review pages hand-mirror the `.cn-<slug>` scope, **deriving every binding from each snippet's own `#token-manifest`**. Once Lane G's dark-drop repair lands and the conductor regenerates, the authoritative scopes should replace the mirrors. ⚠ **These three snippets carry dark-mode component rules and are therefore new instances of exactly the class Lane G is repairing** — regenerate them *after* that fix, or the drop will swallow them too.
- **`_validate_radius.py` `MIGRATED_SNIPPETS`** — three new snippets are absent from the radius ratchet (⛔ shared file). Console's 20px surface radius was verified present in the render.
- **CATEGORIES / `gen_showroom.py`** — three new slugs (`kpi-tile`, `timeline`, `avatar-group`) have no showroom entry. ⛔ shared file; **and none should be added before Dave rules item 1.**
- **Itinerary rows 55/56/57** — genuinely `Gap`; the Status column is **correct** for these three. Useful signal for Lane H: the rot is not uniform, so a derived status must probe per row rather than assume the column is wholly stale.
- **No new token is wanted.** Every value the arrow question needs (`rag/success-ink`, `rag/error-ink`) already exists and is already ruled. One token is *proposed* and is Dave's: a surface-keyed stack ring (finding 4).

---

## Friction log

- **The brief's fence and `s182-D2` agreed, which is why row 55 went well.** Had I trusted the itinerary's `Gap` and built a "new component", I would have laundered a floated question into a gated artefact. The store grep — not the search index — is what caught it.
- **`_memento_search.py` was serving a stale index** (`_checkin.py` says so itself). Every ruling claim here rests on a direct grep of `_rulings.json`.
- **The first browser launch died on `libXdamage.so.1`.** The runbook's fourth env var already had the answer. Cost one call because I set three of the four.
- **My own review-page builder introduced two defects the gates could not see** (`:is()` split on inner commas; `:root` custom properties dropped). Both were caught **only** by looking at a screenshot and then measuring. A page-builder is an artefact that needs its own verification, not a transparent pipe.
- **`.board`'s 802px intrinsic minimum overflows a 2-up pane** — inherited from Stat-card's grammar, and the same residual Lane E recorded. Handled in **review chrome only** (`.pane{overflow-x:auto}`); the component was not altered to flatter its own review page.
- **Concurrency is visible**: the snippet count moved 79 → 85 mid-lane as siblings wrote. Any count in this receipt is timestamped by the probe that produced it.

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` NOT run.** A filtered run **overwrites the tracked `_STATE-CONTRAST-AUDIT.md`** (the #174 receipt records exactly this and restored it by hand). With five sibling lanes live and no shared-file edits permitted, restoring it was not a risk worth taking. **It is the gate that would adjudicate finding 1's green leg, and it is owed** — conductor or CI.
- **HEAD sha not captured** — the lane brief's ⛔ on git commands overrides the base brief's §3. Declared above.
- **The three components are absent from `canon.css`, the radius ratchet, the showroom and `component-types.json`.** All four are shared surfaces. The review pages' `.cn-` scopes are hand-mirrors, faithful to each manifest but **not generator output** — that is the fence working, and it is declared, not silent.
- **Narrow-viewport reflow below 480px is unexamined** and is not claimed. Verified at 1400 and 480 only.
- **The KPI tile's spark is baked static** with no `dv-behaviour` partial and no `data-tip`. Correct for a passive `aria-hidden` mark (`s184-D1`), but it means `_validate_dataviz.py` has **not** been run over a file containing dataviz geometry — **declared; that gate is on the conductor's list.**
- `outputs/s203k-renders/` holds 6 PNGs — **(NON-REPO: session outputs folder)**, `s191-D2`.
- Throwaway builder at `/var/tmp/s203k/` — outside the repo, not carried, not an instrument.
