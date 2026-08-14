# Receipt — #174 build sub · Progress bar, the first component through the scaffold route

*Worker receipt per the parallel-conductor checklist. Written 2026-08-14 against HEAD `be1e0a7`.*
*⛔ Nothing here is a ruling. No commit, no push. `knowledge/_rulings.json` untouched.*

## What was ruled into this build

- `s173-D1` (Dave, #173) — the progress bar, determinate, linear and circular, is the first
  component through the scaffold route.
- Dave, #174 — build the component, not a scaffolder; keep a friction log; **determinate only**;
  do **not** mint a `component-type` family; do **not** correct the two stale inventory documents.

## Step 0 — the premise, confirmed first-hand before building

| Claim inherited from the brief | Verified? | Evidence |
|---|---|---|
| HEAD is `e5ab8ee` | **STALE** — HEAD is `be1e0a7` (#173 wrap landed after the brief) | `git log --oneline -3` |
| No `Progress-bar.reference.html` exists | ✅ TRUE | `ls knowledge/snippets/` |
| `role="progressbar"` improvised in 3 snippets | ✅ TRUE, quoted | `Progress-tracker:172`, `File-upload:291` + `:404`, `Stepper:261` |
| A new component absent from `CATEGORIES` "will not appear in the index" | **FALSE** | `gen_showroom.py:483` — `CAT_OF.get(slug, "More")`; unlisted slugs land in **More** |

The stale HEAD was benign (a wrap commit, no bearing on the route). The `CATEGORIES` claim was
overstated and is corrected here.

## Deliverables

| File | State |
|---|---|
| `knowledge/snippets/Progress-bar.reference.html` | NEW — the canon artefact |
| `knowledge/components/progress-bar.meta.json` | NEW — all ten required fields |
| `showroom/progress-bar.html` | NEW — generated, byte-identical on `--check` |
| `reviews/REVIEW-174-progress-bar-four-themes-v1.html` | NEW — 4 themes x light/dark, Dave's review surface |
| `knowledge/_validate_radius.py` | `MIGRATED_SNIPPETS` += `Progress-bar.reference.html` (strict from birth) |
| `knowledge/_DS-IMPROVEMENTS.md` | contrast finding queued as a proposal (not fixed) |
| `knowledge/canon/canon.css` + audit `.md`s + `showroom/index.html` | regenerated, never hand-edited |

## Gates

Baseline measured BEFORE any change, so failures are attributable. ⚠ The first baseline reading was
void — `rc=$?` after a pipe reads `tail`'s status; re-measured with the exit code captured directly.

| Gate | Baseline | After | Verdict |
|---|---|---|---|
| `_validate_snippets` | 75, 0 fail | 76, 0 fail | ✅ |
| `_validate_a11y` | 75, 0 fail | 76, 0 fail | ✅ |
| `_validate_radius` | 0 strict fail | 0 strict fail | ✅ |
| `_validate_coverage` | 75/75 | 76/76 | ✅ |
| `_validate_icons` | 0 UNKNOWN | 0 UNKNOWN | ✅ (needed `data-bespoke` — see friction) |
| `_validate_type_composites` | 1101, rc=1 | 1101, rc=1 | ✅ ratchet held; my file contributes **0**, the only clean file of 91 |
| `_validate_state_contrast` | — | Progress-bar ✅ clean | ⚠ filtered run only — see residual |
| `gen_showroom --check` | — | in sync | ✅ |
| `gen_snippet_tokens --check` | — | in sync | ✅ |
| `gen_canon_components --check` | — | in sync | ✅ |
| `gen_component_partials --check` | — | in sync | ✅ |
| `gen_theme_cascade --check` | **rc=1 AT HEAD** | rc=0 | ⚠ pre-existing drift, healed — see below |

⛔ `_build_all.py` was NOT run, per the brief.

## Two findings that are NOT mine, proved with controls

**1 · `gen_theme_cascade.py --check` was already red at HEAD.** Proved on a true control: canon.css
restored byte-identical to HEAD, `Progress-bar` snippet + meta moved out of the tree, `--check` still
`rc=1`. My regeneration healed it. CI would have been red on `be1e0a7` independently of this build.

**2 · `gen_canon_components.py` drops a hand-authored comment from `canon.css` — and it is correct to.**
Same control (no `Progress-bar` present): regenerating deletes a `#168`/`#168-A` provenance comment and
the string `#3F6FB5`. **No ruled value was lost.** `#3F6FB5` was superseded twice — `s168-D5`, Dave
verbatim *"ink this will do"* — and the live value is `#6893D3` light / `#2674DC` dark, emitted
**identically** by HEAD and by the regenerated file. What was removed was a **stale hand-edit to a
generated region** that still described the superseded state. The full ruling provenance survives in
`tokens/palettes/rag/mono.json`'s `$note` and `_rulings.json`.

## Contrast seam — checked BEFORE building (runbook step 3)

Fill-on-track (`progress/complete` on `progress/incomplete`) measured across all four themes:
Mono 15.27/9.15 ✅ · Console 15.27/9.15 ✅ · Legacy 4.58 ✅ / **1.75 ❌** · Supercharge 4.48 ✅ / **2.38 ❌**.

**Not declared as a gated `contrastPair`** — it would be a green that cannot fail in the two themes
where it is false. Meaning carried by a numeric value in text plus `aria-valuetext`. Queued to
`_DS-IMPROVEMENTS.md`; pre-existing (the same pair sits under `Progress-tracker`).

Declared pairs were each verified to hold in **all four themes**, not just the Mono base the gate reads.

## Render proof

`goto("file://…")`, never `set_content()`. Font asserted with a canvas measurement against two
controls, not `fonts.check`: target 347 · both aliases 347 · DejaVu 375 · nonexistent face 301 ⇒ the
real HSBC cut, both aliases landing on it.

All 8 panes measured numerically and each matches the token maths exactly; `fillW/trackW =
260.4/420 = 62.0%`, matching `aria-valuenow="62"`. Tree asserted clean of fontconfig strays (0 `.uuid`).

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` could not be run over the full population in-sandbox.** It exceeds
  the ~178s call cap on 76 snippets. Run filtered to `Progress-bar` ⇒ **clean, rc=0**, driven in a real
  browser. The filtered run *overwrote* the tracked 75-snippet `_STATE-CONTRAST-AUDIT.md`; it was
  **restored to HEAD, byte-identical**. That artefact therefore does not yet list `Progress-bar` —
  a full-population regeneration is owed and belongs to CI or a longer runner.
- `_s174_hold/` — an empty directory left in the repo root. The sandbox cannot `rmdir` on the repo
  mount. Needs removing by the conductor (delete grant).
- `.git/index.lock` + `.git/index.lock.s174-stale` — stale, zero-length; the sandbox cannot unlink
  them. Clear before the first commit.
- `notes/_REHEARSAL-LOG.jsonl` — was **already modified at session open** (pre-existing, not mine);
  my `_checkin.py` run then appended to it.
- The rehearsal gate reports a pre-existing STRUCTURAL fail (stale memento index). Not mine; a wrap item.

## Gauge

`_checkin.py`: FILL **94,056 real** · boot **56,342 real** (inside the ruled 56,158 ±849 band) ·
peak 94,056 across 12 turns · conversation half 86,637 real.

`machinery: 0 instrument / ~205 feature` — no new gate, checker or harness was built. The two
throwaway scripts (`/var/tmp/s174-mkreview.py`, `/var/tmp/s174-render.py`) live outside the repo and
are not instruments the repo carries.
