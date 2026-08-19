# Brief — Wave 3: the P1 Foundations components, six fenced Opus lanes

*Written #203, 2026-08-19, by the FABLE conductor. Dave is the decision-maker throughout; this
brief rules nothing. Version 1 — never overwrite; write `-v2`.*
*Panel at fire: All models 47% used · Fable 61% used · resets Thu 11pm. Subs bind on the
all-models pool (QUOTA); conductor FILL at fire ~70K real, advisory stop 150,929, wall 256K.*

---

## 1. The job, in plain words

The itinerary (`reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx`) carries 20 P1 gaps.
Six lanes each build THREE components end-to-end through the existing gated-component route —
the route #174 walked and receipted (`notes/_receipts/2026-08-14-s174-first-component-progress-bar.md`,
READ IT FIRST — it is the worked example, including its step-0 premise table and friction log).
The deliverable per component is a real, reviewable component for Dave's eye, not scaffolding.

## 2. Read before building (in this order)

1. `notes/_receipts/2026-08-14-s174-first-component-progress-bar.md` — the walked route + its corrections
2. `knowledge/_RUNBOOK-gated-component.md` — the seven-step procedure
3. `knowledge/components/EXAMPLE-button.meta.json` + `knowledge/components/meta.schema.json`
4. `knowledge/snippets/Progress-bar.reference.html` — the freshest gated snippet; copy its grammar
5. Your nearest gated sibling snippet(s) — **specimens COPY the approved artefact, never re-draw**
6. Worker checklist, `knowledge/_RUNBOOK-parallel-conductor.md:126` — including step 0

## 3. Step 0 — verify the premise first-hand (mandatory)

Open your receipt with a premise table like #174's: HEAD sha via `git log --oneline -1`, the
claimed absence of your components (`ls knowledge/snippets/`), and any brief claim you rely on.
A carried claim is verified, not trusted [[premise-ages-faster-than-rule]]. An unrun search is
indistinguishable from an absent record — name every probe you run.

## 4. The fence — what a worker MAY and MAY NOT touch

**MAY create (NEW files only, unique names — this is the whole fence):**
- `knowledge/snippets/<Name>.reference.html` (one per component)
- `knowledge/components/<slug>.meta.json` (one per component)
- `reviews/REVIEW-203-<slug>-four-themes-v1.html` (Dave's live review surface: 4 themes ×
  light/dark, responsive, per `feedback-review-live-variant-spread`)
- `notes/_receipts/2026-08-19-203-wave3-lane<X>-<topic>.md` (ONE receipt per lane)

**MAY NOT, under any framing:**
- ⛔ `git checkout` / `git restore` / `git stash` on ANY path — #202's sub destroyed uncommitted
  work this way; undo your own mistake by re-editing. No commits either — the conductor commits.
- ⛔ Edit ANY shared file: `GOOD-MORNING.md` · `_LIVE-STATE.md` · `_FUTURE-STATE.md` · `MEMORY.md` ·
  `knowledge/_rulings.json` · any `knowledge/tokens/*.json` · `_validate_radius.py`
  (MIGRATED_SNIPPETS) · `gen_showroom.py` (CATEGORIES) · `knowledge/_DS-IMPROVEMENTS.md`.
  Missing-token or DS findings go in your RECEIPT as proposals; the conductor merges them.
- ⛔ Run any generator that REWRITES shared outputs (`gen_canon_components`, `gen_canon_tokens`,
  `gen_showroom` without `--check`, `gen_theme_cascade`, audits) — six lanes would clobber each
  other. The conductor regenerates once at reconcile. `--check` (read-only) is fine; expect it to
  report your file as missing from generated outputs — that is the fence working, declare it.
- ⛔ `_build_all.py` — any partial run strands the tree.
- ⛔ Delete anything. Version, don't overwrite (`-vN`).

**Gates you DO run, filtered to your own files:** `_validate_snippets.py`, `_validate_a11y.py`,
`_validate_state_contrast` where runnable, `_validate_type_composites` (your files must contribute
**0** to the 1,101 debt — the ratchet is shrink-only). Report every rc. Declare, by name, the
gates left to the conductor. A declared gap passes; a silent one fails.

## 5. Rules that bind the pixels (non-negotiable, all RULED)

- **Four themes** — mono · legacy · console · supercharge, each light AND dark. A single-theme
  green is not a green. Flexibility across themes IS the requirement.
- **Two-red law** (`s151-D1`): `#DA1A00` on white / `#F6604C` elsewhere; green mirrors; MONO only.
- **Mono error ink camp** (`s149-D1`/`s194-D1`): `#1A1A1A` on `#F6604C`; white-on-error ABOLISHED.
- **Type composites mandatory**: `.t-cm-*` / `.t-ed-*`, real type scale only (12/14/16 — the 11px
  #202 caught was off-scale). No raw font-size declarations.
- **Square corners** by default (radius 0); Badge/Avatar are the known exceptions.
- **Ink is ruled** (`s175-D1`/`s176-D1`): blackest-not-pure-black per theme; resolve from tokens.
- **44px min-hit-area** on interactive targets (token exists at base tier; no gate enforces it —
  enforce it by hand and say so in the receipt).
- Real ARIA, `:focus-visible`, standard-ease motion, embedded `#token-manifest` with PASSING
  contrastPairs — the manifest is the proof-of-done.
- Colour caution: Dave is astigmatic; red/yellow are problem hues — never lean on hue alone.

## 6. PROPOSED vs RULED — the line you must not cross

Every judgment call you make (scope cut, variant set, a token you wish existed, a label size)
is **PROPOSED**, marked `$status: "PROPOSED #203, Dave's eye owed"` in the meta, surfaced on the
review page, and listed under "Decisions needed" in your receipt. ⛔ Nothing a sub writes is a
ruling. If you frame a question as OPEN, run `python3 knowledge/_memento_search.py "<q>"` first
and quote the hits beside it (`s202-D3` — the store has refused a "new" question before).

**DO-NOT-RULE list (Dave's, live right now — do not touch, do not "helpfully" resolve):**
segmented-label type-scale bindings (#203's namesake) · the push / CI read-back · the glossary
build · the 5-dimension proposal · W-38 ramp semantics · `data-mark` · component promotion of any
kind · grey-tint or ink swaps (surface, never swap).

## 7. Pitfalls, replayed (Dave #165 — mandatory reading)

- **Call-boundary kills**: nothing survives a tool-call boundary; builds >45s wall die — chunk.
- **Render proofs**: `set_content()` is BANNED (drops type.css silently) — `goto("file://…")`.
- **A crash is not a fail** — parse helpers fail loud and named; declare the residual.
- **Green tests can't see scope** — drive your component on real content, all four themes, by eye
  via screenshot before claiming it renders.
- **The receipt's every "landed" claim names its evidence** (gate rc, file path, render proof).
  Ritual output is not evidence — re-read the generated file, never quote your own banner.
- Author's context-gauge stamp goes at the top of the receipt.

## 8. Autonomy clause (ratified, routing audit #9)

The user is not watching; proceed on reversible actions that follow from this brief; an
end-of-turn promise is not a completion — do the work or flag the blocker.

## 9. The lanes

| Lane | Components (itinerary rows) | Mine from | Notes |
|---|---|---|---|
| A — forms core | Form layout + validation (13) · Textarea (20) · Alert / inline callout (68) | Carbon / Ant / GOV.UK | The biggest single gap. Validation messaging and Alert interlock — build Alert first, use it in Form. Error colours: two-red law + mono ink camp. |
| B — date & time | Date picker (14) · Date-range picker (15) · Time picker (16) | Ant / Carbon / MD3 | Share one calendar grid grammar across all three; range = extension of single. |
| C — money & secure | Number/currency input (17) · Amount/currency display primitive (89) · OTP/PIN entry (19) | Stripe / Wise / Plaid | The fintech differentiators. Display primitive is used BY the input — build it first. Tabular figures. |
| D — overlays | Toast/snackbar (69) · Drawer/side sheet (70) · Popover (71) | Ant / MD3 / Untitled | Distinct from Notifications (persistent) and Tooltip — read those gated snippets first and say in the meta how yours differs. |
| E — data display | Empty state (54) · Stat/metric card (52) · Data grid (51) **scope-boxed** | Untitled / Tailwind / Carbon | Data grid = sort + select + pagination composed ON the gated Table grammar; inline edit is OUT of scope (PROPOSED cut, Dave's). Stat card: the `spark` slot is a known candidate — mark PROPOSED. |
| F — flow & load | Skeleton loader (72) · File upload / dropzone (18) · Stepper interactive (34) | Ant / Carbon / MD3 | Stepper: Progress-tracker is display-only and GATED — copy its visual grammar, add interaction. File-upload snippet already improvises `role="progressbar"` (#174 finding) — reconcile with gated Progress-bar. |

Each lane: work the three in the stated order, receipt as you go. If the third won't fit before
your window strains, land two clean rather than three ragged — say so in the receipt.

## 10. Report back to the conductor (≤400 words)

Files created (paths) · gate rcs (baseline→after where measurable) · decisions-needed list ·
proposals for the conductor to merge (tokens, DS-improvements, CATEGORIES entries) · friction log
highlights · your context gauge at close. The conductor replays sub reports to Dave — write for
that audience.
