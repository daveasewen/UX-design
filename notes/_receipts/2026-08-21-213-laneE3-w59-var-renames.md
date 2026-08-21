# Receipt — #213 LANE E3 · `W-59`: rename the ledgered local-var collisions

> ⛔ **DATED PERIOD RECORD, NOT A LIVE HOME.** Written 2026-08-21 by the #213 Lane E3 Opus sub.
> **Nothing in this file is a ruling.** Open choices below are PROPOSED-not-ruled and are Dave's.
> The store (`knowledge/_state.json`, `knowledge/_rulings.json`) stays the one live home.

| governance | value |
|---|---|
| lane | E3 (Opus), #213 mine-side burn-down fan-out |
| row served | `W-59` — home `knowledge/_TOKEN-FORK-LEDGER.json`, opened #209 |
| brief | `notes/_briefs/2026-08-21-213-mine-burn-fanout-brief-v1.md` |
| git | **none run** (FENCE 1). All edits left UNCOMMITTED. |
| serial set | **not run** (conductor's) — obligated steps named in §6 |

---

## 1. PREMISE TABLE — every claim in the brief re-probed before building (#202)

| # | premise (as briefed) | probe run | result | verdict |
|---|---|---|---|---|
| P1 | "5 local-var collisions are LEDGERED somewhere in-repo" | `grep -ril collision notes/_receipts/ knowledge/` → 18 receipts + `knowledge/_TOKEN-FORK-LEDGER.json` | Ledger FOUND: `knowledge/_TOKEN-FORK-LEDGER.json`, 46 entries, exactly **4** carry a non-baseline status | ⚠ **PARTLY FALSE — 4 keys, not 5** |
| P2 | the ledger names 5 entries | `python3` walk of `declared_forks`, filtering `status != UNRULED-BASELINE-s139` | 4 keys: `--ring`, `--rule`, `--scrim`, `--tail-x` | ⚠ drift |
| P3 | reconcile "5" vs "4" | ran the gate itself: `_validate_token_forks.py --strict` | **5 FORK RECORDS across 4 NAMES** — `--rule` forks TWICE (mono *and* supercharge) | ✅ **RECONCILED — the brief's 5 and the row's 4 are the same set** |
| P4 | W-59's own `closes_when` | `knowledge/_state.json` row `W-59` | *"the 4 var names are component-local in snippets, canon regenerated, fork gate green WITHOUT these ledger entries, zero-visual-change proven"* — the store itself says **4 names** | ✅ store agrees with P3 |
| P5 | "the class fix is component-local names" | `W-59` body | *"unique local names (e.g. `--pc-tail-x`) in the snippet sources + canon regen + zero-visual-change proof (byte-identical under masking, the P-2 wave-3 method)"* | ✅ worked to these words |
| P6 | Dave sanctioned the fork at #209 | `_DECISION-HISTORY/2026-08-20-209-the-descent-and-the-inversion.md:79` | *"The fork gate's 5 collisions: **"Ledger the 5"** → ledgered as local name collisions, row **`W-59`** minted for the rename **class** fix rather than five point repairs."* | ✅ verbatim |
| P7 | canon.css is the live cascade the gate reads | `_validate_token_forks.py` docstring + run | **the gate CRASHES on today's canon.css (exit 2)** — see §5 BLOCKER | ⛔ **NEW, not briefed** |

All probes run 2026-08-21, 15:43–16:2x BST, against `/Users/daviewen/Documents/Claude/Projects/UX-design`.

## 2. THE 5 LEDGERED COLLISIONS — quoted verbatim (brief line 59)

The ledger entries, verbatim from `knowledge/_TOKEN-FORK-LEDGER.json` (all four carry the **identical** status string):

> `"status": "SANCTIONED-#209 (Dave, live: 'Ledger the 5' from the three-option control). Read as component-LOCAL name collisions from the #203/#204 waves, not deliberate spine forks; RENAME-to-local-names stays the open class fix (see W-59)."`

| ledger key | `instances` | `first_evidence` (verbatim) |
|---|---|---|
| `--ring` | 2 | `knowledge/canon/canon.css:2282 .cn-avatar (#D7D8D6) vs :4082 .cn-avatar-group (var(--border-subtle))` |
| `--rule` | 4 | `knowledge/canon/canon.css:1435 .cn-headers vs :6916 .cn-command-palette (mono); :13298 accordion vs :13931 command-palette (supercharge)` |
| `--scrim` | 2 | `knowledge/canon/canon.css:3399 .cn-video-player (overlay-version2) vs :6912 .cn-command-palette (overlay-version1)` |
| `--tail-x` | 2 | `knowledge/canon/canon.css:3014 .cn-tooltip .tip (50%) vs :9292 .cn-popconfirm .pc (24px) — pure local geometry` |

**The "5" is 5 FORK RECORDS, measured today, not 5 keys** — `--rule` forks in two theme axes:

```
FORK  --ring    theme=mono        canon.css:2307  .cn-avatar (#d7d8d6)            vs :5774  .cn-avatar-group (#e1e1e1)
FORK  --rule    theme=mono        canon.css:1460  .cn-headers (#e1e1e1)           vs :9368  .cn-command-palette (#f0f0f0)
FORK  --rule    theme=supercharge canon.css:23245 .cn-accordion (#cdc8c6)         vs :24251 .cn-command-palette (#dfdedc)
FORK  --scrim   theme=mono        canon.css:3424  .cn-video-player (#000000d9)    vs :9364  .cn-command-palette (#00000080)
FORK  --tail-x  theme=mono        canon.css:3039  .cn-tooltip .tip (50%)          vs :13023 .cn-popconfirm .pc (24px)
```

In every one of the five, **`.cn-command-palette` or `.cn-avatar-group` or `.cn-popconfirm` is the divergent side** — so four component-local renames retire all five records.

## 3. WHAT LANDED — the renames (UNCOMMITTED)

Applied at the **snippet sources** (W-59's own words), not canon.css — the generator is the class fix (ds-018 history, brief pitfall 5). Regex `(?<![-\w])--NAME(?![-\w])`, whole-file, so no consumer can be left behind.

| # | file | rename | sites |
|---|---|---|---|
| 1 | `knowledge/snippets/Popconfirm.reference.html` | `--tail-x` → **`--pc-tail-x`** | 3 |
| 2 | `knowledge/snippets/Command-palette.reference.html` | `--scrim` → **`--cp-scrim`** | 4 |
| 3 | `knowledge/snippets/Command-palette.reference.html` | `--rule` → **`--cp-rule`** | 9 |
| 4 | `knowledge/snippets/Avatar-group.reference.html` | `--ring` → **`--avg-ring`** | 4 |

`--pc-tail-x` is W-59's own worked example, adopted verbatim.

**Collateral checks (all quoted, matched ≠ presence rule):**
- `--stack-ring` in `Avatar-group.reference.html` — **7 occurrences, untouched** (the lookbehind excludes it).
- the CSS *class* `.cp-scrim` survives: `.cp-scrim{position:absolute; inset:0; background:var(--cp-scrim);}` — class renamed nowhere, only the var.
- `--sub-rule` (Anchor-nav) — untouched; the rename is file-scoped to Command-palette.
- residual old names in the three edited files: **grep exit 1 — ZERO**.
- the `"vars"` binding keys were renamed with the CSS so the semantic binding stays attached (`"--cp-rule": "divider/border/subsection"`, `"--cp-scrim": "overlay/version1"`, `"--avg-ring": "border/subtle"`). `_validate_binds_resolve.py` green confirms no binding was orphaned. **No binding VALUE was changed** — no semantic re-binding was made (FENCE 3).

## 4. PROOF

### 4a. The collisions are resolved — the fork gate, DRIVEN
Regenerated canon in a scratch tree (`/var/tmp/w59`, generators run from the repo's own code):
`gen_canon_components.py` → *"generated 135 components"*, then `--check` → *"OK — 135 components in sync"*, then `gen_theme_cascade.py` → *"wrote AUTO-THEMES block — 228 override path(s), 386 component projection(s)"*.

| measurement | before | after |
|---|---|---|
| `_validate_token_forks.py --strict` total | **GATE RED: 103 fork(s)** | **GATE RED: 98 fork(s)** |
| delta | — | **exactly −5 fork records** |
| `--ring` / `--rule` / `--scrim` / `--tail-x` still forking | 5 records | **none** (grep of the strict report → `(none)`) |
| fork on any NEW local name (`--cp-rule`/`--cp-scrim`/`--avg-ring`/`--pc-tail-x`) | — | **none** |
| distinct names measured | 915 | 919 (the 4 new locals) |

### 4b. The ledger entries are safely retirable
Gate re-run against a probe ledger with the 4 entries deleted (42 entries): **the undeclared-fork set is unchanged** — the same 5 pre-existing reds of §5b, no red attributable to the retirement. The four entries are dead weight.

### 4c. Zero visual change — a DRIVEN render, all FOUR themes × light+dark
Harness `/var/tmp/w59_render_probe.py`: mounts `.cn-avatar-group`, `.cn-command-palette`, `.cn-popconfirm` under their canon scopes against a given canon.css, Chromium 151.0.7922.34 headless (Playwright, `_RUNBOOK-render-verify.md` env), dumps 12 computed properties for every element in each subtree across mono/legacy/console/supercharge × light/dark. Transitions and animations disabled before reading (the settle requirement) — the first pass without it produced one flake, which is recorded in §5c rather than hidden.

- markup identity asserted first: body markup of all three snippets **identical** before/after — the renames are CSS-only.
- BEFORE canon rebuilt deterministically from the *pre-rename* snippet copies, so the comparison is immune to any concurrent lane's edits to the repo canon.css.

> **8 theme/mode dumps · 1,808 element readings each · 23,504 computed-value comparisons · DIFFS: 0**

### 4d. The bite CAN FAIL — mutation-proven by DRIVING THE THING (#104, #171, #184)
Two independent mutants, both fired:
- **fork-gate bite:** reverted `--pc-tail-x` → `--tail-x` in the regenerated canon. Gate re-reds with `FORK --tail-x theme=mono … .cn-tooltip .tip (50%) vs .cn-popconfirm .pc (24px)`, exit 1.
- **render bite (the #184 silent-black class):** made ONE consumer dangle — `background:var(--cp-scrim)` → `var(--cp-scrim-DANGLING)` — a half-done rename, exactly the failure mode this lane risks. The render diff fired **16 diffs**, `.cp-scrim` background-color `rgba(0, 0, 0, 0.5)` → `rgba(0, 0, 0, 0)`, in **all 8** theme/mode combinations. The zero-diff green in §4c is therefore a measurement, not a self-comparison.

### 4e. Downstream gates green after the rename (scratch tree)
| gate | result |
|---|---|
| `_validate_snippets.py` | `135 snippet(s), 0 failure(s)` — exit 0 |
| `_validate_binds_resolve.py` | `135 snippets (135 with manifests, 2110 vars) · 116 binds addresses · 135/135 canon blocks · 0 failure(s)` — exit 0 |
| `gen_snippet_tokens.py --check` | `4696 manifest bindings … 0 value(s) would change; 0 canon.css literal(s) would change` — exit 0 |
| `_validate_palette_tier.py` | OK — exit 0 |
| `_validate_legacy_leak.py` | OK — exit 0 |
| `gen_canon_components.py --check` | `OK — 135 components in sync` — exit 0 |

## 5. RESIDUALS AND FINDINGS — declared, none ruled

### 5a. ⛔ BLOCKER, NOT THIS LANE — **the fork-ban gate is DOWN, and it is a CI gate**
`python3 knowledge/_validate_token_forks.py` on today's repo:

```
FAIL _validate_token_forks.py: knowledge/canon/canon.css: unbalanced '}' at line 15374
```

Exit **2** — the gate itself failed (a crash is not a fail). It is wired into CI at `knowledge/_build_all.py:357`, so **the gates workflow is red on this today**.

Cause, probed to source: two snippets carry an **orphan declaration block with a stray closing brace** — a rule whose selector and opening brace were lost, which the canon generator faithfully prefixes and carries through:

- `knowledge/snippets/Template-confirmation.reference.html:193` → `canon.css:15374`
- `knowledge/snippets/Template-error.reference.html:182` → `canon.css:16919`

both reading `    display:inline-flex; align-items:center; justify-content:center; transition:background var(--ease), filter var(--press); }` with no owning selector. Same class, two files — a `Template-*` wave artefact; the fork gate parsed clean at #209, so it arrived at #210/#211.

**PROPOSED, not made** (out of this lane's named edits, FENCE 2): repair the orphan block in both snippet sources — either restore the lost `.confirm .btn{` / `.err .btn{` selector or delete the orphan — then regen. Neither line declares a custom property, so neither can affect any fork measurement; that is asserted mechanically in the probe harness. **Which of restore-vs-delete is correct is a design question — Dave's / the template lane's, not mine.** This lane worked around it by stripping the two lines in a throwaway probe copy only; **the repo files were not touched.**

### 5b. FINDING — 5 **NEW** undeclared forks, unrelated to W-59 (a regression since #209)
With W-59's five retired, the gate still reds on five forks that are **not** in the ledger and **not** the ones Dave saw at #209:

```
--l-min    mono        .cn-layout-utilities .l-grid (240px)   vs .cn-template-report .tpl-stats (200px)
--min-pri  mono        .cn-app-shell-split .sp (240px)        vs .cn-splitter .sp (160px)
--min-sec  mono        .cn-app-shell-split .sp (240px)        vs .cn-splitter .sp (160px)
--move     mono        .cn-tabs (220ms …)                     vs .cn-template-settings (200ms …)
--panel    supercharge/dark  .cn-app-shell-multi-column (#2A2621) vs .cn-app-shell-nav-rail (#1A1A1A)
```

Four of the five are pure component-local geometry/timing — **the same class W-59 exists to fix**; `--panel` is a colour divergence and is *not* obviously the same class. **PROPOSED, not ruled:** a successor row applying this lane's rename recipe to the four geometry/timing collisions, with `--panel` held out for Dave's eye as a possible real value question. Not minted — row minting is the conductor's.

### 5c. Declared: the transition flake, and why it is recorded
The first render pass (150 ms settle, transitions live) reported exactly **one** diff — `legacy/light .cp-opt background-color rgb(237,237,237) → rgb(240,240,240)`. Re-interrogated element-by-element, both sides read `rgb(240, 240, 240)` with `--hover:#F0F0F0` in both, and the value tracks `--hover` (which this lane never touched), not `--rule`. It was an unsettled transition, not a change. Re-run with transitions disabled: **0 diffs**. Recorded rather than quietly dropped, because a single-diff "flake" is exactly the shape a real regression also takes.

### 5d. Declared: scope boundaries held
- `designer-skills-v1/` and `designer-skills-v2/` carry the old names in their frozen copies. **Not synced** — packs are RELEASES.
- `knowledge/_proforma/Tranche-*.html` and `Masthead-interactive.html` declare their own `--scrim`; they are separate documents (CROSS_DOCUMENT, cannot fork in cascade) and were **not touched**.
- `Tooltip` and `Popover` keep `--tail-x`; `Avatar` keeps `--ring`; `Video-player` keeps `--scrim`; `Headers`/`Accordion`/`Anchor-nav`/`App-shell-*` keep `--rule`. Only the divergent side was localised — the minimum that retires the collision.
- `Popconfirm` has no JS touching the var; `Tooltip`/`Popover` set `--tail-x` via `style.setProperty` and were deliberately left alone, so no script was orphaned.

### 5e. ⚠ Shared-file hazard for the conductor
`knowledge/canon/canon.css` is regenerated by **three** of this fan-out's lanes (E1 ds-018, E2 RAG, E3 here) but the brief assigns it to none. This lane therefore regenerated **only in scratch** and left the repo canon.css alone. If E1/E2 regenerated in place, their output does not yet contain these renames.

## 6. SERIAL-SET STEPS THIS WORK OBLIGATES (conductor's to run, ORDERED — #210)

Nothing below was run here.

1. `python3 knowledge/canon/gen_canon_components.py` — **required**; the snippet sources are now out of sync with the repo canon.css (`--check` reds until it runs).
2. `python3 knowledge/canon/gen_canon_components.py --check` — determinism.
3. `python3 knowledge/canon/gen_theme_cascade.py` (then `--check`) — the theme layer projects the renamed binding keys; the supercharge `--cp-rule` override moves with the name.
4. `python3 knowledge/gen_snippet_tokens.py --check --quiet` — token projection (proven 0 changes in scratch).
5. `python3 knowledge/_validate_binds_resolve.py` / `_validate_snippets.py` — binding-key rename consumers.
6. `python3 knowledge/_validate_token_forks.py` — **will still exit 2 until §5a is repaired**; it cannot certify this lane in CI until then.
7. registry · MIGRATED_SNIPPETS · CATEGORIES · spine · git — the conductor's, unchanged by this lane (no snippet added, no category moved).

**Not obligated:** no `knowledge/_rulings.json` write, no `_state.json` write, no `_GOVERNING-RECORDS.md` row edit.

## 7. OPEN CHOICES — PROPOSED, NOT RULED (Dave's, in his terms)

1. **"Are these four renames the names you want?"** — `--pc-tail-x` came from W-59's own example; `--cp-rule`, `--cp-scrim`, `--avg-ring` follow the same shape (component initials + the old word). An alternative is the full component name (`--command-palette-rule`). Longer, unambiguous, noisier in the CSS. **Not ruled.**
2. **"Retire the four ledger entries?"** — proven to change no gate verdict (§4b). The exact edit proposed, **not made**: delete keys `--ring`, `--rule`, `--scrim`, `--tail-x` from `declared_forks` in `knowledge/_TOKEN-FORK-LEDGER.json`, 46 → 42. The file's own `$do_not` says no script may add to it automatically; this lane read that as "a human's call to remove too."
3. **"Only the divergent side was renamed — is that the class fix, or should both sides go local?"** — e.g. `--ring` now belongs to Avatar alone. Renaming *both* sides would leave no shared name at all, at the cost of a wider blast radius. This lane took the minimum that retires the collision. **Not ruled.**
4. **The five NEW forks of §5b** — same recipe for the four geometry/timing ones, `--panel` held out as a possible real colour question. **Not ruled, no row minted.**
5. **The §5a orphan-block repair** — restore the lost selector, or delete the orphan? A design call on two `Template-*` snippets. **Not ruled.**

---

*Evidence artefacts (NON-REPO: sandbox `/var/tmp`, this session only — regenerate from §4 if needed):* `/var/tmp/w59` (after tree) · `/var/tmp/w59before` (before tree) · `/var/tmp/w59_render_probe.py` · `/var/tmp/w59-BEFORE2.json`, `/var/tmp/w59-AFTER2.json`, `/var/tmp/w59-MUTANT.json`.
