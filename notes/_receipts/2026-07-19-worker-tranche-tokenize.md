# Worker receipt — tokenize the pro-forma tranches T1–T8

*Written 2026-07-19. Worker session, task: `notes/_BRIEF-tranche-tokenize-T1-T8.md`. Worked directly in
the existing tree (`/sessions/keen-zen-einstein/mnt/UX-design`, no worktree). **No git writes** —
`git add`/`commit`/`stash` never called. I did run two read-only commands (`git status --short`, `git
diff`) once, early, purely to sanity-check a projected diff; the second one surfaced a
`.git/index.lock: Operation not permitted` warning (another process — presumably the conductor — holding
the index). The commands still returned correct output, but I stopped using git entirely after that and
did all further verification via plain file reads / Python, to stay clear of any concurrent git activity.
Flagging this so the conductor can check nothing of theirs was disturbed; I touched no git state.*

## Files touched (confirmed via mtime — nothing else in the tree changed)
```
knowledge/gen_snippet_tokens.py                 — extended (see diff summary below)
knowledge/_proforma/Tranche-1-interactive.html  — #token-manifest added, theme-block values projected
knowledge/_proforma/Tranche-2-interactive.html  — same
knowledge/_proforma/Tranche-3-interactive.html  — same
knowledge/_proforma/Tranche-4-interactive.html  — same
knowledge/_proforma/Tranche-5-interactive.html  — same
knowledge/_proforma/Tranche-6-interactive.html  — same
knowledge/_proforma/Tranche-7-interactive.html  — same
knowledge/_proforma/Tranche-8-interactive.html  — same
```
`Tranche-9-interactive.html` does not exist in the tree — untouched, as instructed. `knowledge/tokens/`
untouched. No memory/GOOD-MORNING/_LIVE-STATE files touched.

## Generator diff summary (`knowledge/gen_snippet_tokens.py`)
- Added `PROFORMA = os.path.join(HERE, "_proforma")`.
- `main()` now globs `Tranche-[1-8]-interactive.html` (bracket range, not bare `Tranche-*` — deliberately
  won't sweep in Tranche-9 the moment it appears; that inclusion should be a deliberate follow-up edit,
  not a side-effect of this glob) and runs the same `process()`/`selfcheck()` over `snip_files +
  tranche_files`. No change to `process()`, `selfcheck()`, `resolve()`, or the theme-block regex — the
  brief's premise held exactly: tranches use the identical bare `[data-theme="mode"]{ }` shape and
  `#token-manifest` mechanism, so the existing logic applied unmodified.
- `project_canon()` left untouched — snippet-only by design (tranches have no `.cn-<slug>` canon.css
  block), confirmed correct, no change needed.
- Final summary line now reports snippets/tranches counts separately; `--check` covers tranches
  automatically since it's the same `write=not check_only` flag threaded through the same `process()`.
- Docstring updated to record the tranche scope and the Tranche-9 exclusion reasoning.

## Per-tranche vars — verified before writing (no surprises)
Dumped both theme blocks for all 8 files before touching anything. **T2–T8 are byte-identical** in their
`[data-theme]` blocks (27 vars each, same order, same values) — confirms the brief's "descend from the
same `_PROFORMA` base." **T1 is the reduced 21-var base** (no `--warn/--warn-t/--success/--success-t/
--info/--info-t` — it simply doesn't declare status colours at all, not a binding gap). No renamed or
extra vars anywhere; the mapping table applied uniformly. Each manifest carries 18 (T1) or 24 (T2–T8)
bound vars (27/21 total minus the 3 left as local literals — see FLAGGED below).

## Gate results

**`python3 knowledge/gen_snippet_tokens.py`** (write mode):
```
gen_snippet_tokens: 1007 manifest bindings across 39 snippets + 8 tranches; 184 value(s) projected; 0 canon.css literal(s) projected.
OK — snippets + tranches + canon.css in sync with tokens.
```
Snippets: 0 changes (already correct — confirms I didn't disturb the existing 39). Second run after that
= 0 projected (idempotent, confirmed).

**`python3 knowledge/gen_snippet_tokens.py --check`**:
```
gen_snippet_tokens: 1007 manifest bindings across 39 snippets + 8 tranches; 0 value(s) would change; 0 canon.css literal(s) would change.
OK — snippets + tranches + canon.css in sync with tokens.
```

**`python3 knowledge/_build_all.py`** — final line:
```
✅ all generators ran and the integrity + contrast gates passed.
```
Exit code 0. All **35/35** steps ran; `rc` stayed 0 throughout (verified by capturing full log and
grepping for `❌`/`FAIL` — none found). Tranche-specific detail from the log:
```
[PASS] _proforma/Tranche-1-interactive.html … hardcode_leaks: 0, refs 10/10, asset_paths 11/11 real, allcaps 0
[PASS] _proforma/Tranche-2-interactive.html … hardcode_leaks: 0, refs 11/11, asset_paths 39/39 real, allcaps 0
[PASS] _proforma/Tranche-3-interactive.html … hardcode_leaks: 0, refs 3/3,  asset_paths 39/39 real, allcaps 0
[PASS] _proforma/Tranche-4-interactive.html … hardcode_leaks: 0, refs 7/7,  asset_paths 39/39 real, allcaps 0
[PASS] _proforma/Tranche-5-interactive.html … hardcode_leaks: 0, refs 14/14, asset_paths 39/39 real, allcaps 0
[PASS] _proforma/Tranche-6-interactive.html … hardcode_leaks: 0, refs 7/7,  asset_paths 40/40 real, allcaps 0
[PASS] _proforma/Tranche-7-interactive.html … hardcode_leaks: 0, refs 14/14, asset_paths 44/44 real, allcaps 0
[PASS] _proforma/Tranche-8-interactive.html … hardcode_leaks: 0, refs 23/23, asset_paths 57/57 real, allcaps 0
✅ pro-forma universal gate passed (10 tranche file(s)).
✅ CSS-governed gate passed (10 tranche file(s)).
✅ No-hardcode gate passed (10 tranche file(s)).
```
(The "10" is not a miscount of mine — `_validate_proforma.py`'s glob is `_proforma/*.html` filtered by
`id="icon-manifest"`, which also catches the pre-existing `DataViz-interactive.html` and
`Masthead-interactive.html`. Both PASS and both are untouched by me — file mtimes confirm only the 8
Tranche files + `gen_snippet_tokens.py` changed.) One pre-existing advisory finding surfaced in the
edge-extremity check on Tranche-6 (`EDGE-WEIGHT 12px @ weight 400` on `.ib.f-tip::after`) — that's a
font-weight rule unrelated to colour/tokens, advisory-only (non-gating), and not something my change
touched or introduced.

## FLAGGED — for the composer/Dave to rule on

**1. The mono PRIMARY-ACTION trio + its icon twin — genuine token-store gap, likely needs new tokens.**
`--pri`/`--pri-h`/`--pri-lbl`/`--icon-rev` are the near-black/near-white primary button and its icon
buttons (`.btn.pri`, `.ib.pri`, `.ib.sec`, stepper dots, toast, checkbox-indeterminate, back-to-top,
active floating tab). No `action/primary/*` semantic token exists. Handled as follows:
- `--pri` → bound to `text/default` as suggested (light `#1A1A1A` exact match; dark `#FFFFFF` vs the
  prior literal `#F2F2F2` — slightly brighter near-white, cosmetic only).
- `--pri-h` → left as a local literal (brief said so explicitly — no token exists for hover).
- **`--pri-lbl` → NOT bound to the brief's suggested `text/reverse` — left as a local literal instead.
  This is a deviation I made deliberately, not a judgment call I'm asking you to rubber-stamp after the
  fact: I checked the maths before deciding.** `text/reverse` resolves flat `#FFFFFF` in *both* modes, but
  `--pri` (the surface `--pri-lbl` sits on) *inverts* lightness by mode — near-black background in light
  theme, near-white background in dark theme. Binding `--pri-lbl` to `text/reverse` would put `#FFFFFF`
  label text on a `#FFFFFF`-resolved dark-mode button: **1.0:1 contrast, the label vanishes** (checked via
  WCAG relative-luminance — see below). Left as the existing literal (light `#FFFFFF` / dark `#1A1A1A`,
  17.4:1). **Candidate for your ruling:** the token store already has `text/on-inverse` (light `#FFFFFF` /
  dark `#333333`, 12.6:1), whose own `$note` is written for exactly this case — *"Label for surfaces whose
  lightness INVERTS between modes: secondary buttons, primary pressed, checked selection controls…
  text/reverse stays flat white for primary-on-red (binding the flat token here would give white-on-white
  in dark, 1.0:1)."* That note is describing this exact bug. I did not bind to it myself — that's your/
  Dave's call (promotion + judgment calls are explicitly not mine) — but it's sitting right there,
  already-approved, if you want a same-day fix rather than waiting on a new `action/primary/*` token.
- **`--icon-rev` → same treatment, same reasoning, also left as a local literal.** It was on the brief's
  *clean* list (→ `icon/default-reverse`), but I traced its usage first (per the "survey before build"
  habit) and found it's used **exclusively** on the same `--pri` surface as `--pri-lbl` (`.ib.pri`,
  `.ib.sec`, checkbox-indeterminate fill, back-to-top button, active floating tab) — and
  `icon/default-reverse` is *also* flat `#FFFFFF` both modes. Identical 1.0:1 dark-mode break. There is
  **no `icon/on-inverse` token in the store** — a genuine gap, not just an imprecise match. Left as the
  existing literal (light `#FFFFFF` / dark `#1A1A1A`). Recommend this gets solved together with
  `--pri-lbl` (either a new `icon/on-inverse` mirroring `text/on-inverse`, or fold icon-on-inverted-surface
  into the eventual `action/primary/*` component tokens).
- Contrast maths I ran (WCAG relative luminance, both are flat colour swatches so this is exact, not an
  approximation): `contrast(#FFFFFF, #FFFFFF) = 1.00`; `contrast(#FFFFFF, #1A1A1A) = 17.4` (current
  literal); `contrast(#FFFFFF, #333333) = 12.63` (the `text/on-inverse` candidate, matches its own
  documented "12.6:1 dark" claim).

**2. Five vars bound to the brief's suggested interim, values shift (as anticipated) — no deviation, just recording the deltas per the brief's own request:**
- `--disi` → `text/disabled`: light `#B7B7B7→#E1E1E1`, dark `#767676→#808080` (lighter; disabled is
  contrast-exempt per `_STANDARDS.md` §3).
- `--line2` → `divider/border/break`: light close (`#EDEDED→#F0F0F0`); **dark shifts noticeably**
  (`#3A3A3A→#808080`, a much more visible divider).
- `--surf` → `surface/subtle`: light close (`#F3F3F3→#F0F0F0`); dark close (`#212121→#1F1F1F`, the new
  `raise-1` elevation primitive).
- `--scrim` → `overlay/version1`: light `#00000066→#00000080`, dark `#00000099→#00000080` (both paths
  resolved — did not need the "keep as local literal" fallback).
- `--shadow` → `elevation/functional`: light `#00000026→#00000033`; dark is an **exact match**
  (`#000000D9→#000000D9`).

**3. Not flagged in the brief but worth naming — the two values this task exists to fix, confirmed
correctly propagated:**
- `--raised` (`surface/raised`) dark: `#1D1D1D → #1F1F1F` — the pre-R-D16 → dark-elevation drift the
  brief's "Why" section names directly, now closed by construction (re-running the projector after any
  future token change keeps it closed).
- `--focus` (`focus/ring`): was hard-pinned to `--ink`'s near-black/near-white (`#1A1A1A`/`#FFFFFF`) in
  every tranche — not a real focus-ring colour. Now resolves to the proper blue focus tokens
  (`#305A85`/`#4587A7`). This is a meaningful, correct fix, not just a drift correction — flagging so it
  isn't mistaken for noise in the diff.

## ⚠️ CONDUCTOR — read this: build-artifact churn beyond the 9 files above
Running `_build_all.py` (step 4 of the brief, mandatory) regenerated **~60 derived/report files
tree-wide** — `_PROFORMA-GATE.md`, `_DARK-MODE-AUDIT.*`, `_TEXT-CONTRAST-AUDIT.*`,
`_INDICATOR-CONTRAST-AUDIT.*`, `_INTEGRITY-REPORT.md`, `compliance/graph-index.json` +
`compliance/rules/wcag-*.json`, `_XREF-INDEX.*`, `tokens/_blast-radius.json`, `_consult-index.json`,
`guidelines/_rules-index.json`/`_RECONCILIATION.md`, and more. **This is not scope creep or an accident —
every `_build_all.py` run rewrites these wholesale by design** (its own docstring: "any
verification{}/external_automatable_refs{} block from a PRIOR run is gone after this step... must be
rebuilt fresh every run"), regardless of who triggers it or what changed. I did not hand-edit any of
them. Full list via `find knowledge -newer _STANDARDS.md -type f` (minus my 9 target files) is available
on request.

**Why I'm flagging instead of just noting it in passing:** early on, a read-only `git status`/`git diff`
I ran hit `.git/index.lock: Operation not permitted` — evidence something else (presumably you) was
touching git concurrently. If anyone else's uncommitted edit to tokens/guidelines/compliance rules was on
disk at the moment I ran the build, my regenerated reports reflect *that* transient snapshot, not
necessarily the final reconciled tree. **Recommend you re-run `python3 knowledge/_build_all.py` yourself
as the last step before committing** (cheap, idempotent, ~35 steps) so every derived artifact you commit
reflects the fully-reconciled tree rather than my isolated view of it — standard practice per your own
protocol, just calling it out explicitly here so it isn't missed.

## Recommendation
Everything above is already in the working tree, gate-clean, idempotent. Nothing is blocking a commit —
the only open question is item 1 (whether to switch `--pri-lbl`/`--icon-rev` to `text/on-inverse` /
a new `icon/on-inverse` right now, or leave the literals in place until the `action/primary/*` token
work happens). Either way the build stays green; I left the safe literals in place so there is no
regression sitting in the tree either way you decide.
