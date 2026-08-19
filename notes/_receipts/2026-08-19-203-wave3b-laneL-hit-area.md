# Receipt — #203 Wave 3b, Lane L: the 44px hit-area consumer (ADVISORY)

*Opus work sub, 2026-08-19. Nothing here is a ruling. Every "landed" claim names its evidence —
gate rc, file path, or a quoted measurement.*

**Context-gauge stamp — DECLARED UNMEASURED, not guessed.** `knowledge/_checkin.py`'s subject is
"newest mounted transcript", i.e. **the conductor's window, not a sub's** (`--help`, run, quoted:
`path  Transcript jsonl (default: newest mounted)`). A sub stamping the conductor's fill would be a
confident false inscription, so no figure is given. ⬛ **Instrument gap for the conductor:** there is
no per-sub gauge; sub spend is measurable only from the parent side (`effort-gauge-token-banded-168`).

---

## ⚠ READ THIS FIRST — the brief's premise was FALSE, and the store said so

The lane brief says *"The token is minted at base tier; **no gate reads it**."* **A hit-area gate
already exists and is already wired into `_build_all.py`**, and Dave has already ruled on it four
times. I found this only after building — the store grep should have been step 0, not step 8.
`[[retrieval-default-hides-the-ruling]]` and `[[unrun-search-indistinguishable-from-absent-record]]`,
paid for in full.

Probe (quoted): `grep '"hit[- ]area|44px|tap target|touch target"' knowledge/_rulings.json` → 10 hits.

| ruling | Dave says (verbatim fragments) | bearing on this lane |
|---|---|---|
| `s114-D5` #114 | *"The hit-area checker MEASUREMENT REDESIGN (markup-driven) is SIGNED OFF — 'good lets do it.'"* status: **ENACTED #116 — `_validate_a11y.py` rebuilt markup-driven on `_a11y_target.py`; 25-clause selftest wired into `_build_all.py`; 16/16 mutations killed** | the consumer EXISTS |
| `s114-D6` #114 | *"44px is promoted to BLOCKING for controls — 'Promoting 44 to blocking for controls, good.'"* status: **RULED, NOT ENACTED**; watch: *"the sweep found 72 controls in the 24-43 band, not 6, so the promote is a remediation lane, not a flag flip"* | the tier question is **already ruled**; only the remediation lane is open |
| `s116-D1` #116 | *"Data marks are held to the 24x24 WCAG 2.5.8 dense-case MINIMUM — exempt from the 44 CONTROL target, **NOT exempt from the check**"*; watch: *"OWED MEASUREMENT before the gate goes blocking: how many marks fall BELOW 24. Measure it; do not assume either way."* | **my first draft exempted marks outright — that contradicted a ruling. Corrected; the owed measurement is delivered below.** |
| `s116-D3` #116 | *"the hit-area sweep scope is ALL CONTROLS across the whole canon snippet library — 'all controls' + 'yes 75'"*; watch: *"75 files, not 67. A sweep that reports 67 has used the stale figure and did not measure."* | my report states **77 scanned / 67 with candidates**, both measured today |
| `s201-D2` #201 | *"THE 44 MIN-HIT-AREA IS A HIT ZONE, NOT A VISUAL HEIGHT… controls keep their visual size and present an invisible padded interactive target"*; and, in the same ruling, *"Enforcement remains ABSENT — no gate reads the 44"* | ⚠ **this is where the brief's false premise came from.** `s201-D2`'s enforcement clause disagrees with `s114-D5`'s ENACTED status. One of the two records is stale — flagged for Dave, **not resolved here**. The hit-ZONE half is exactly what this instrument measures. |

**So the honest framing of this lane's output is not "the first consumer".** It is: a **second,
independent, RENDER-DRIVEN** consumer that measures what the markup-driven one states it must not
guess at — `_a11y_target.py` verbatim: *"the other axis is layout-determined … this gate must not
guess a size"*. Both of Lane C's breaches are exactly that shape (padding/flex resolution at a
breakpoint), which is why a wired, green, blocking-capable gate never saw them.

---

## Step 0 — premise table

| Claim | Verdict | Probe, quoted |
|---|---|---|
| `_validate_hit_area.py` is absent | ✅ TRUE | `ls knowledge/_validate_*.py` → 39 validators, no `_validate_hit_area.py` (and `s114-D5` `governs` says so too: *"CORRECTED #116: no _validate_hit_area file exists"*) |
| **No gate reads the 44 token** | ❌ **FALSE** | `knowledge/_a11y_target.py:60-63` → `TARGET_CONTROL = 44` · `TARGET_MARK = 24` · `FLOOR = 24`; `_validate_a11y.py:65` → `MARK_TIER = "warn"`. Wired into `_build_all.py` |
| Token exists at base tier | ✅ TRUE | `tokens/layout.json` → `/target/min = 44px`; `$description`: *"RULED by Dave 2026-07-24… Dial-down floor is 24… Reference impl: snippets/Segmented-control.reference.html"* |
| Amount-input standard field is 39px (Lane C) | ✅ **REPRODUCED EXACTLY** | rendered: `.ai-box` **380 × 39** @1180 (Lane C: 380 × 39) |
| Secure-entry OTP cell is 42px ≤480px (Lane C) | ⚠ **CORRECTED — it is 40px** | see finding 2 |
| Render harness available | ✅ TRUE | `/var/tmp/pylibs-s203e` + `pw-browsers-s197` + `chromelibs-s201` reused read-only per `_RUNBOOK-render-verify.md` n=6; own font farm `/var/tmp/fonts-s203L`; `document.fonts.check('16px HSBC_MtUnivers_Latin')` → **True on all 67 files that produced rows** |

⚠ **Tree state.** One read-only `git status --short --untracked-files=all` was run before I re-read
my binding's "⛔ no git commands"; **no further git command was run, and no HEAD sha is quoted** (the
base brief asks for one — I chose the stricter lane fence and am declaring the gap rather than
filling it silently). What that query showed is not suppressed: `knowledge/canon/canon.css`,
`gen_canon_components.py` and ~20 snippets were **already modified** — Lane G's repair is in flight.
**These are working-tree numbers, not HEAD numbers.** Snippets carry their CSS inline, so canon.css
regeneration does not move them; a snippet another lane edits mid-wave could move its row.

---

## What landed

| File | Status |
|---|---|
| `knowledge/_validate_hit_area.py` | **NEW** — 588 ln, ADVISORY, `--selftest`, three mutation levers |
| `knowledge/_HIT-AREA-ADVISORY.md` | **NEW** — full sweep, 77 snippets × 1180/480px |
| `knowledge/_HIT-AREA-ADVISORY.json` | **NEW** — machine-readable sidecar (every row, tier, exemption) |
| `notes/_receipts/2026-08-19-203-wave3b-laneL-hit-area.md` | this file |

⛔ **NOT wired into `_build_all.py`** · ⛔ **no breach fixed, no component file touched** · ⛔ **no
generator run** · ⛔ **`_validate_a11y.py` NOT run** (it rewrites the shared `_A11Y-GATE.md`, which
another lane has already modified — running it would clobber; declared, not skipped silently).

---

## Acceptance — both known breaches caught, three known-goods cleared

`python3 knowledge/_validate_hit_area.py --selftest` → **rc 0**, verbatim:

```
  ✔ Amount-input   @1180  .ai-box    want UNDER got UNDER   (380 × 39)   39px standard money field
  ✔ Amount-input   @480   .ai-box    want UNDER got UNDER   (440 × 39)   39px at the narrow breakpoint too
  ✔ Secure-entry   @480   .se-cell   want UNDER got UNDER   (40 × 48)    OTP cell ≤480px
  ✔ Secure-entry   @1180  .se-cell   want PASS  got PASS    (48 × 56)    desktop — must NOT fire
  ✔ Button         @1180  button     want PASS  got PASS    (105.9 × 44) known-good 44px control
  ✔ Input-fields   @1180  .help-btn  want PASS  got PASS    (44 × 44)    18px box + 44px ::before expander
SELFTEST PASS
```

The three PASS arms are the point: a gate that fires on everything has caught nothing. `.help-btn`
(18 × 18 visible, 44 × 44 hit zone) proves no false positive on the canon expander idiom — which is
`s201-D2`'s "hit zone, not visual height" made measurable.

### Driven mutations (the clause AND the feature)

| lever | control | mutated | reading |
|---|---|---|---|
| `--min 60 --strict` on `Button` | rc **0** | rc **1** | the gate CAN go red; the threshold is live |
| `--ignore-shell` on `Amount-input` | `380 × 39` UNDER −5 | `297.6 × 21` **BREACH-FLOOR −23** | the field-shell union is load-bearing |
| `--ignore-hittest` on `Breadcrumbs` | `39.4 × 18` | `39.4 × **10.1**` | the hit test is load-bearing |
| `--ignore-pseudo` on `Input-fields` | `44 × 44` PASS | `44 × 44` PASS — **no change** | ⬛ declared: the pseudo union is REDUNDANT with the hit test (an invisible `::before` is hit-testable). Kept only for the fallback path |
| playwright not importable (`env -u PYTHONPATH`) | — | rc **2** `✖ HIT-AREA: HARNESS UNAVAILABLE … this is NOT a pass` | an instrument that cannot run says so; never a green meaning "I did not look" |

---

## Findings

### 1 · A bounding rect is NOT a hit region — my own first draft was wrong on every leading-trimmed link

The first working draft measured `getBoundingClientRect()` and reported `Breadcrumbs .crumb` at
**39.4 × 10.1** — a −34px BREACH-FLOOR. Phantom. The canon leading trim (`text-box-trim:trim-both`,
ds-005) shrinks an anchor's *box* to its cap-height span, but Chromium hit-tests the **line box**.
Probed with `document.elementFromPoint` at the crumb's centre ± N px:

| offset | returns |
|---|---|
| −10px, −6px | **the anchor** |
| +6px | **the anchor** |
| +10px | `ol` — past the line box |

Real target ≈ **18px**: still a breach, −26 not −34. The gate now walks `elementFromPoint` outward
from the centre and takes the contiguous span it owns (occlusion truncates the walk — an overlapped
strip is not clickable), calibrated sides-only so `Button`'s 44 reads **44, not 45**; a +1 bias would
silently pass a 43px control. ⇒ The plausible instrument produced plausible numbers that were wrong
by 8px on every trimmed text link, and only a positive control exposed it.

### 2 · Lane C's "42px" OTP cell is arithmetic, not a measurement — the real figure is 40px, so the breach is DOUBLE what was recorded

Lane C corrected itself *upward*: *"From the CSS I first wrote 40px, 4px under. The **rendered** box
is **42px** (40px content + 1px border each side)."* That correction is wrong here, because
`box-sizing:border-box` is declared in both places:

- `knowledge/snippets/Secure-entry.reference.html:116` → `*{box-sizing:border-box;}`
- `knowledge/canon/canon.css:915` → `.canon, .canon *{ box-sizing:border-box; }`

Measured, not derived: `.se-cell` renders **40 × 48** @480 (48 × 56 @1180). Under border-box the 1px
border sits *inside* the declared 40px. **The breach is −4px, not −2px.** Same class as
`[[premise-ages-faster-than-rule]]`: arithmetic was applied on top of a real measurement and won.
⛔ Not fixed — Dave's. The line is `Secure-entry.reference.html:185`
(`.se-cell{width:40px; height:48px;}`, inside the ≤480px query). Lane C's proposed `44 × 48` still clears.

### 3 · The measurement `s116-D1` declared OWED is delivered — on rendered geometry

`s116-D1`'s watch: *"OWED MEASUREMENT before the gate goes blocking: how many marks fall BELOW 24
(thin donut slices, narrow bars). Measure it; do not assume either way."*

**510 mark-tier rows measured across 11 chart snippets; 332 fall below 24 (≈166 distinct marks, each
seen at both widths). Zero charts are clean at the mark tier.** By snippet (rows):
`Chart-line 96 · Chart-candlestick 80 · Chart-combo 37 · Chart-bar 33 · Chart-butterfly-h 24 ·
Chart-stacked-area 24 · Chart-butterfly-v 16 · Chart-donut 12 · Chart-bullet 6 · Chart-histogram 2 ·
Chart-sparkline 2`. Worst: `Chart-candlestick .dv-body` at **8.1 × 2** (−22).
⚠ **Unit care:** #116 measured **107 marks below 24** from the markup; this is 166-ish from rendered
geometry at two widths. Different instruments, different populations, **not a contradiction and not
a like-for-like delta** — do not subtract them. `[[measure-dont-convert-units]]`.
⛔ Whether this flips `MARK_TIER` from `"warn"` to `"fail"` is Dave's, per the ruling.

### 4 · The advisory sweep, control tier — 428 findings across 36 of 67 components

Full table: `knowledge/_HIT-AREA-ADVISORY.md`. Frame: **77 snippets scanned · 67 with interactive
candidates · 1,553 targets measured (1,043 control @44, 510 mark @24) · 465 exempt, each reason named
and counted · 760 findings (428 control, 332 mark)**. HSBC face asserted on every file.
Exemptions, counted: `zero-box 218 · disabled/inert 90 · aria-hidden subtree 60 · inline link in text
(2.5.8 inline exception) 59 · not rendered 36 · sr-only 2`.

| component | control targets | findings | worst |
|---|---|---|---|
| Date-range-picker | 94 | 86 | `input#f-from` 194 × 24 (−20) |
| Date-picker | 82 | 74 | `input#f-date` 346 × 24 (−20) |
| Input-fields | 36 | 26 | `input#b1` 256.8 × 24 (−20) |
| Secure-entry | 44 | 22 | `.se-cell` 40 × 48 (−4) |
| Selection-controls | 20 | 20 | `button.x` 24 × 24 (−20) |
| Form-layout | 24 | 18 | `input#f-name` 420 × 42 (−2) |
| Reorder | 18 | 18 | `button` 30 × 30 (−14) |
| Tags | 16 | 16 | `button.x` 24 × 24 (−20) |
| Links | 15 | 15 | `a.icon-lnk` 231.5 × 16 (−28) |
| Amount-input | 14 | 12 | `input#a1` 380 × 39 (−5) |
| Breadcrumbs | 12 | 12 | `a.crumb` 39.4 × 18 (−26) |
| Notifications | 16 | 12 | `button.x` 24 × 24 (−20) |
| Time-picker | 20 | 12 | `input#f-time` 346 × 24 (−20) |
| Popover | 16 | 10 | `button.pop-trigger` 131.5 × 21 (−23) |
| Cards | 18 | 6 | `a.arrow` 336 × 13.6 (−30.4) |
| File-upload | 10 | 6 | `button.fu-remove` 36 × 36 (−8) |
| Tooltip | 6 | 6 | `button.trigger` 24 × 24 (−20) |
| Video-player | 10 | 6 | `button` 32 × 32 (−12) |
| Chart-line · Data-grid · Headers · Progress-tracker · Table · Toast · View-options | 4–46 | 4 each | `button#back` 84.7 × 38 (−6) · `button` 40 × 40 (−4) |
| Command-palette | 16 | 3 | `input.t-cm-input` 364 × 31 (−13) |
| Chart-combo · Drawer · Empty-state · Hero · List-items · Modal-lightbox · Modals · Search-field · Skeleton-loader · Status-indicator | 2–18 | 2 each | `input#dense` 13 × 13 (−31) · `button#open` 116.8 × 15.2 (−28.8) |

*(counts are target × viewport rows, so a control breaching at both widths counts 2.)*
**31 components are clean at the control tier**, including `Segmented-control` (the token's own
reference impl), `Button`, `Tabs`, `Pagination`, `Icon-button`, `Dropdown`, `Slider`, `Textarea`.
**10 snippets have no interactive candidate** — `Account-card · Amount-display · Badge ·
Countdown-timer · Divider · Eyebrow · Loading-indicator · Progress-bar · Stat-card · Summary` — named
in the report rather than left to vanish from the table.
⚠ **Re-run variance observed:** two full sweeps of the same tree differed by **one row**
(`Command-palette` 4 → 3) — a borderline hit-test at a sub-pixel boundary. Treat single-row deltas as
noise; treat the classes below as the signal.

**Triage shape (all PROPOSED, none ruled):**
1. **The `.x` close-button class, 24 × 24** — `Notifications`, `Tags`, `Selection-controls`,
   `Search-field`, `Tooltip`. One idiom, one fix: the canon `::before` expander already at
   `canon.css:1805`. Best findings-per-fix ratio in the sweep, and it is the shape `s201-D2` ruled.
2. **The date/time family, 24px inputs** — 172 of the 428 control findings. ⚠ read §5 first.
3. **The money pair** — `Amount-input` −5, `Secure-entry` −4 (Lane C's two, independently re-measured).
4. **Specimen demo triggers** — `Modals #open`, `Toast #spawnOk`, `Drawer #open`,
   `Skeleton-loader #resolveDemo`, `Modal-lightbox #open`: demo scaffolding, not component surface.
   Reported because no structural signal separates furniture from content — probed:
   `el.closest('[class*="cn-"]')` is **false on every snippet** (the `cn-` prefix exists only in
   `canon.css`). Deprioritise; do not delete.

### 5 · Known conservatism, declared, NOT worked around

The field-shell union refuses a wrapper holding **more than one** interactive descendant — that
refusal is what stops `.se-cells` masking its six OTP inputs. Consequence: a date field, whose shell
holds an input **and** a trailing calendar button, is scored on the bare input's **24px** rather than
the ~46px shell a thumb meets. That is why the date family dominates. Both readings are arguable
(tapping shell padding does not focus an input unless something makes it), so the gate reports the
harsher one and says so here rather than quietly choosing. ⬛ **PROPOSED, Dave's:** should a
multi-control field shell union? It moves ~172 findings.

Also declared (and carried in the module docstring, so they travel with the code): the pseudo union
takes the expander's *size* and assumes canon centring, not the 9-point anchor matrix; WCAG 2.5.8's
**spacing exception** is unmodelled, so UNDER is a signal to look, not a proof of non-conformance;
the hit-test walk is capped at 48px per side.

---

## Gates run

| gate | rc | note |
|---|---|---|
| `_validate_help_gate.py` | **0** | `help-gate OK — 146 script(s) scanned; every entry point answers --help before it can write` — my script is in that 146 |
| `python3 -m py_compile knowledge/_validate_hit_area.py` | **0** | — |
| `_validate_hit_area.py --help` | **0** | prints the contract, writes nothing |
| `_validate_hit_area.py --selftest` | **0** | acceptance above |
| `--min 60 --strict` (Button) | **1** | mutation: the red path exists |
| harness-missing leg | **2** | loud, named refusal |
| bare invocation (no argv) | **2** | `✖ HIT-AREA: no input files` |

**Declared gaps.** This lane created no HTML/CSS, so it contributes 0 rows to `_validate_snippets.py`,
`_validate_a11y.py`, `_validate_state_contrast.py` and **0** to the 1,101 type-composite debt; none
were run on my files because none apply. `_validate_a11y.py` deliberately NOT run (shared
`_A11Y-GATE.md`, already dirty). No generator run — Lane G owns that surface. **Left to the
conductor:** `_build_all.py` at reconcile.

---

## Decisions needed (Dave's — PROPOSED only)

1. **The stale-record collision, first.** `s201-D2` (#201) says *"no gate reads the 44"*; `s114-D5`
   says the checker was ENACTED at #116 and `_a11y_target.py` is in the tree reading exactly that
   number. **One of those is stale and it is propagating into briefs** — this lane was briefed off the
   `s201-D2` wording. Which record wins is Dave's; the fix is a store correction, not a code change.
2. **Wire `_validate_hit_area.py` into `_build_all.py`?** If yes, ADVISORY or blocking? Note `s114-D6`
   already ruled *44 blocking for controls*, ordered after `s114-D5` — and its own watch calls the
   promote *"a remediation lane, not a flag flip"*. 428 control findings today says the same thing
   louder. A shrink-only ratchet (the type-composite shape) is the plausible form. Not started.
3. **`MARK_TIER` `"warn"` → `"fail"`?** `s116-D1`'s owed measurement is now delivered (finding 3):
   332 of 510 mark rows below 24, no clean chart. Dave's call, explicitly reserved to him.
4. **The multi-control field-shell question** (§5) — moves ~172 findings.
5. **The `.x` 24 × 24 class** — apply the canon `::before` expander library-wide?
6. **`Amount-input` −5 / `Secure-entry` −4** — Lane C's proposals stand; the Secure-entry figure is
   now −4, not −2.
7. **A per-sub context gauge** — no instrument exists (stamp at top).

*Store searched before framing these as open (`s202-D3`): `_memento_search.py "44px hit area gate"`
(hits: lane records + GOOD-MORNING, nothing dispositive) **and** a direct grep of
`knowledge/_rulings.json` for `hit-area|44px|tap target|touch target` → **10 rulings, five of them
material and quoted at the top of this receipt**. The lexical search did NOT surface them; the store
grep did. `[[retrieval-default-hides-the-ruling]]`.*

## Friction log

- **The brief's premise was false and the store knew.** I built first and grepped `_rulings.json`
  late; the grep changed the instrument (marks became a tier, not an exemption) and re-framed the
  whole deliverable. Store grep belongs in step 0, beside `ls`.
- The obvious measurement (bounding rects) was **wrong**, invisibly, until a positive control
  contradicted it (finding 1). `[[mutation-tests-the-clause-not-the-feature]]` — drive the thing.
- First full sweep emitted **861** findings, ~350 of them chart marks scored against 44. An
  instrument whose output nobody can triage is not yet an instrument — and the fix was not "exempt
  them" (which a ruling forbids) but "tier them", which `s116-D1` had already specified.
- Runbook held verbatim: `/var/tmp` farms from s197/s201/s203e reusable **read-only**, no browser
  download, `goto file://` only, chunked at 13 files (~15s) against the 45s wall.
