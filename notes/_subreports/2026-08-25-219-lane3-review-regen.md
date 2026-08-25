# `#219`-lane3 — the three bento review artefacts were never stale: residual ③ discharged by MEASUREMENT, not by regeneration

session: `#219` · 2026-08-25
window: `#219 crank wave 1 — lane 3 (reviews/ only)`
sub index: `lane3`
brief: `notes/_briefs/2026-08-25-219-crank-divvy.md`
tokens: `UNMEASURED — a sub cannot read its own `message.usage`; the conductor holds the seat figure`

## VERDICT

**The lane's PREMISE IS FALSE, and no `-vN+1` page was emitted — deliberately.** The brief asked me
to regenerate three review artefacts said to "render a pre-pin photography specimen". They do not.
All three already carry the **exact** `gen_bento_roles_217.SPECIMEN_FILES` set — **15/15 by name,
zero off-pin, on every one of the three pages** — and a fresh run of each owning generator against
today's tree is **byte-identical (`cmp` exit 0) to the committed page**, re-confirmed after lane 1's
`canon.css` landed mid-run. The reason is structural, not lucky: the three pages were last written
at the **#217** wrap commit `540f2cd`, **before** the #218 filename-slice cap existed; the #218 pin
restored precisely the #217 set, so the pages never passed through the window in which the specimen
was wrong. Emitting three byte-identical `-v4`/`-v2` duplicates would have rotted the home pointers
Dave knows these pages by (`_LIVE-STATE.md`, `_CHAIN.md`, `_REVIEW-SIGNOFF.md`, `_state.json`,
`_memento-index.json`, `GOOD-MORNING.md`) and split one live fact across two homes against ADR-0017
— cost with no informational gain, so I did not.

Instead I paid the proof: **all three verify probes driven GREEN in a real Chromium**, four themes
× light/dark, and the name-check itself **driven RED against the pre-pin slice** so it is a gate that
can fail. **Zero working-tree changes in `reviews/` or `knowledge/_render/`.** The lane is DONE by
measurement; the only thing left is a record edit that is not mine to make.

COUNTS: findings `6` · ruling-shaped `1` · UNPROVEN `2`

## What was done

**Step 1 — generator ownership named before touching anything** (`grep -rln` over `knowledge/`):

| review page | owning generator | its probe |
|---|---|---|
| `reviews/BENTO-CANON-2026-08-23-v2.html` | `knowledge/_render/gen_bento_canon_217.py` (`OUT`, line 58) | `knowledge/_render/verify_bento_canon_217.py` |
| `reviews/BENTO-CANON-2026-08-23-v3.html` | `knowledge/_render/gen_bento_roles_217.py` (`OUT`, line 63) | `knowledge/_render/verify_bento_roles_217.py` |
| `reviews/GALLERY-COMPARE-2026-08-23-v1.html` | `knowledge/_render/gen_gallery_compare_217.py` (`OUT`, line 70) | `knowledge/_render/verify_gallery_compare_217.py` |

All three route through the pinned specimen: `gen_bento_roles_217.read_photos()` (lines 149–194) is
the ONE data path and filters on `SPECIMEN_FILES` (lines 130–146); `gen_gallery_compare_217.py:68`
imports that same `read_photos`; `gen_bento_canon_217.py:115–120` is the private reader the #218
conductor repointed, and it imports `SPECIMEN_FILES` from the same module.

**Step 2 — regeneration: RUN, then NOT LANDED.** Each generator was driven to a scratch path with
its own `--out` flag (all three support it) and diffed against the live page. All three
**IDENTICAL**. No `-vN+1` file was created; see finding 2 for why, and the RULING-SHAPED section for
the one call that is not mine.

**Step 3 — 15/15 name check.** Receipt: `notes/_subreports/assets/2026-08-25-219-lane3-review-regen/name-check.txt`.

**Step 4 — render-verify.** All three probes driven green in Chromium; one crop read by eye.

**Step 5 — no commit.** `reviews/` and `knowledge/_render/` are clean. The only new paths are this
report and its `assets/` dir. (The `knowledge/canon/canon.css`,
`knowledge/canon/gen_canon_components.py`, `knowledge/snippets/Navigations.reference.html` and
`knowledge/_memento-index.json` modifications in the tree at filing time are **another lane's**, not
mine — noted so the conductor's reconcile does not attribute them here.)

## Findings

1. **The three pages already show the pinned s217-D1 specimen — 15/15, exact set equality, on all
   three.** Not "15 of them are in the pin" — the set of unique `<img src>` basenames under
   `knowledge/assets/photography-web/` **equals** `set(SPECIMEN_FILES)` on each page, and all 15
   files exist on disk. v2: 30 srcs / 15 unique. v3: 54 srcs / 15 unique. GALLERY-COMPARE: 60 srcs /
   15 unique. Off-pin on all three: **none**. Probe:
   `notes/_subreports/assets/2026-08-25-219-lane3-review-regen/name-check.txt`.

2. **A fresh regeneration is byte-identical to the committed page — `cmp` exit 0, all three.**
   Driven twice: once at lane open, and again **after** lane 1's `canon.css` edit appeared in the
   tree. So the pages are not stale in *any* respect, not merely in their photographs. Command:
   `python3 knowledge/_render/<gen> --out /var/tmp/l3b-<page>` then `cmp -s reviews/<page> /var/tmp/l3b-<page>`.

3. **The reason is a date, and it is checkable.** `git log --oneline -- reviews/BENTO-CANON-2026-08-23-v3.html`
   returns exactly one commit: `540f2cd` (#217). The slice cap and its correction both landed at
   `61302a3` (#218) in `gen_bento_roles_217.py`. The pages were therefore written *before* the cap
   existed and were never regenerated while it was wrong. `_LIVE-STATE.md:68` reads *"show the
   pinned specimen **only if regenerated — they were not**"* — the second clause is true, and the
   first clause's implication does not follow from it, because the pin restored the very set the
   un-capped generator had already emitted. **A premise that a page "must be stale because its
   generator moved" needs the diff, not the inference** ([[premise-ages-faster-than-rule]]).

4. **MUTATION ARM — the name check can go RED, and it reproduces #218's number exactly.** Rebuilding
   the pre-pin instrument (first 15 of the 251 committed derivatives by filename sort) gives
   `slice ∩ pin = 1/15` — **the slice swaps 14 of 15**, the figure `_LIVE-STATE.md:68` records. The
   live v3 page measures **GREEN vs PIN** and **RED vs SLICE**. So the check discriminates rather
   than passing on everything ([[instrument-without-a-consumer]], [[mutation-tests-the-clause-not-the-feature]]).

5. **All three verify probes ALL GREEN in a real Chromium, four themes × light/dark.** Font probe
   passed with both controls in every run (`target 347 · alias_uf 347 · alias_font 347 ·
   control_real 375 · control_absent 301` — canvas measurement, not `fonts.check()`).
   - `verify_bento_canon_217.py` — 8 states; per-theme gutter (mono/supercharge 0, legacy/console
     24), console radius 20 and the other three 0, square tiles, outer 40 / inner 1, bands [3,2,1],
     bottom edge at 4 widths: **11 square walls, 0 holes**, ragged control [10,4,2,0].
   - `verify_bento_roles_217.py` — 8 states; per-role radius placement + clip, dashboard inner/outer
     split, `s217-D7` nested squaring **96 inner-wall measurements, 0 empty cells**, gallery
     raggedness exercised (216 holes, ruled acceptable), trial does not leak.
   - `verify_gallery_compare_217.py` — 8 states; B justifies flush at 3 widths × 2 gutter regimes,
     aspect preserved to 1%, widow switch driven ON/OFF/ON (3·0·3).
   Env (render-runbook, fourth stratum): `PYTHONPATH=/var/tmp/pylibs` ·
   `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215` ·
   `LD_LIBRARY_PATH=/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu` ·
   `FONTCONFIG_FILE=/var/tmp/fonts-s219l3.conf` (fresh symlink farm, `#138`) · `TMPDIR=/var/tmp`.

6. **⚠ POTHOLE, banked for the runbook: `/var/tmp/chromelibs` is now an EMPTY SHELL that fails
   like a missing lib.** The runbook's `#136`/`#138` strata name `/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu`
   as the reusable foreign-session lib dir. Today `/var/tmp/chromelibs/` exists but is **completely
   empty** — presumably a partial sandbox reclaim ([[stale-mount-corroborates-a-stale-premise]]).
   Pointing `LD_LIBRARY_PATH` at it produced `headless_shell: error while loading shared libraries:
   libXdamage.so.1`, which reads as "the recipe is broken" rather than "your lib dir is hollow".
   **`/var/tmp/chromelibs-s213e2` (the `#215` fourth-stratum dir) is intact and carries the one lib
   the shell actually needs**; with it, `ldd headless_shell | grep "not found"` returns empty and the
   shell launches. **Move: `ls` the lib dir before trusting it, and confirm with `ldd`, not with a
   launch attempt.** Not folded into `knowledge/_RUNBOOK-render-verify.md` — that is a canon edit and
   outside this lane's `reviews/`-only scope; priced in the RULING-SHAPED section.

**Tree assertion after the render run** (`#138` rule): `ls -a knowledge/assets/fonts/_desktop/TTF/ |
grep -c '^\.uuid'` → **0**. The symlink farm kept fontconfig's markers out of the repo.

## RULING-SHAPED QUESTIONS

1. **`_LIVE-STATE.md:68`'s residual ③ now says something the tree contradicts — who edits it, and
   how?** The sentence *"`reviews/BENTO-CANON-2026-08-23-v2.html`/`-v3.html` and
   `reviews/GALLERY-COMPARE-2026-08-23-v1.html` show the pinned specimen **only if regenerated —
   they were not**"* is, as of this lane's measurement, **misleading**: they were not regenerated
   AND they do show the pinned specimen. I did not touch it — a `_LIVE-STATE` residual is a
   Dave-owned row and the divvy's DO-NOT-RULE closes that door.
   - **(a)** Conductor appends a discharge line citing this report ("residual ③ DISCHARGED BY
     MEASUREMENT `#219`-lane3 — 15/15 by name, regeneration byte-identical"), leaving the #218
     sentence standing as history ([[feedback-header-wins-over-audit]]: add, never trim). ~200 tk.
   - **(b)** Leave it and let the next session re-derive. Cost: the next reader pays this whole
     lane again — the residual is written in a form that *invites* a regeneration nobody needs.
   - **Recommend (a).** It is addition-only, it names its probe, and it stops a third session
     paying for a false premise. **But it is a Dave-owned row, so it is the conductor's word, not
     mine.**
   - **A second, smaller call rides with it:** finding 6's pothole belongs in
     `knowledge/_RUNBOOK-render-verify.md` as a `n=8` stratum (~250 tk, addition-only). Out of my
     `reviews/`-only scope; every future render lane pays the same 10 minutes without it.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN — the probes' own mutation arms were not re-driven.** `--mutate` / `--no-square` /
  `--wrong-role` / `--break-justify` exist on all three and were driven green-and-red at `#217`; I
  drove the **positive** arms only, plus my own name-check mutation (finding 4). So "the three
  probes still discriminate" is `#217`'s reading carried forward, not today's.
  **Price to prove:** three more `--mutate` runs, ~40–60 s each, ~600 tk of output. Bounded away
  under `s172-D3` because the pages are byte-identical to the artefacts those arms were driven
  against.
- **UNPROVEN — the `#218` "full matrix re-verify after the pin" is still not re-run.**
  `_LIVE-STATE.md:68` declares it; `verify_bento_matrix_217.py` and the four `#218` grids pages are
  **outside this lane's scope** and I did not touch them. This lane's green says nothing about
  them. **Price:** one matrix verify run + the grids pages' probes, ~1 window seam.
- **CLAIMED — nothing.** Every figure above was re-read from the artefact or from a probe run in
  this window; no generator docstring or prior-session banner is quoted as evidence.
- **Scope, stated honestly:** the render probes assert layout, tokens and load state. The
  **WHICH-image** question is answered by the name check on the HTML source (finding 1), not by the
  probes — that division is exactly `#218`'s lesson and it has not changed.
- **Not a defect, checked:** the eyeball crop reports `imgs painted 20 / 54` on v3. All 54 `<img>`
  carry `loading="lazy"` (`grep -c 'loading="lazy"'` → 54), so 20 painted in a viewport-limited
  capture is expected, not a missing-asset reading.

## Evidence

`notes/_subreports/assets/2026-08-25-219-lane3-review-regen/`

- `name-check.txt` — the full 15 pinned filenames, the per-page exact-set-match result for all
  three pages, on-disk existence, and the mutation arm (slice ∩ pin = 1/15; live page GREEN vs pin,
  RED vs slice). **This is the 15/15 receipt.**
- `v3-gallery-crop-1180.png` — clipped crop of `#gallery .c-bento` on
  `BENTO-CANON-2026-08-23-v3.html` at 1180px, console theme, taken after a throwaway `full_page`
  shot (the `#217` reflow pothole) and **read by eye**: photographs paint, licence lines sit under
  every caption, the portrait derivative is two rows tall (the eyeem stairs frame), and the gallery
  is ragged as `s217-D3` rules.

REPLAY-THESE: `notes/_subreports/assets/2026-08-25-219-lane3-review-regen/name-check.txt` (~450 tk) · finding 6 + RULING-SHAPED question 1 above (~350 tk)
