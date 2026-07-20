# 2026-07-20 — worker: button/* three-tier stack (component → semantic → primitive)

Follow-on to a prior worker's flat `button/{secondary,tertiary,quaternary}` group, which aliased
straight to primitives (`color/mono/*`, `color/white`, `color/black`, `color/grey/transparent/white-0`),
skipping the semantic middle tier. This pass inserts that tier — no resolved-value drift except on
four contrast-exempt disabled leaves, called out below.

## Task 1 — new semantic tokens added

Into `knowledge/tokens/semantic-colour.json`, following `surface/*` conventions (per-mode `$alias` +
`$value` + short `$description`):

`surface/*`
- `surface/action` — light `{color/mono/7}` `#626262` · dark `{color/mono/8}` `#808080`
- `surface/action-hover` — light `{color/mono/6}` `#484848` · dark `{color/mono/9}` `#9D9D9D`
- `surface/action-pressed` — light `{color/mono/5}` `#313131` · dark `{color/mono/10}` `#B7B7B7`
- `surface/action-disabled` — light `{color/mono/12}` `#E1E1E1` · dark `{color/mono/6}` `#484848`
- `surface/transparent` — light/dark `{color/grey/transparent/white-0}` `#FFFFFF00`

`text/*`
- `text/on-action` — light `{color/white}` `#FFFFFF` · dark `{color/black}` `#000000` (intentional
  per-mode flip, same shape as the existing `text/on-inverse` but a distinct token — `on-inverse`'s
  dark value is `#333333`, not `#000000`, so the two must not be collapsed)

`border/*`
- `border/action-strong` — light `{color/mono/4}` `#1A1A1A` · dark `{color/white}` `#FFFFFF`
  (carries a `$darkNote` — see Task 3 below)

All five new tokens' resolved values were checked against the button leaves they now back: exact
match in every case, so no cascading drift.

## Task 2 — button/* re-pointed onto the new semantics

`button/secondary`, `button/tertiary`, `button/quaternary` `$alias` fields re-pointed per the brief's
mapping (`surface/action*`, `text/on-action`, `border/action-strong`, plus the pre-existing
`surface/raised-hover`, `text/default`, `text/disabled`, `border/subtle`). Verified independently
(re-implemented the gate's `resolve()` walk in a scratch script) — **0 mismatches**, every button leaf's
`$value == resolve($alias)`.

**Four disabled leaves got a small, deliberate value shift**, per the brief's explicit carve-out
(disabled = contrast-exempt, so adopt the existing semantic's canonical value rather than keep the
prior bespoke shade):
- `button/secondary/label/disabled` — light `#9D9D9D` → `#E1E1E1` (now aliases `text/disabled`)
- `button/tertiary/border/disabled` — dark `#484848` → `#808080` (now aliases `border/subtle`)
- `button/tertiary/label/disabled` — light `#B7B7B7` → `#E1E1E1` (now aliases `text/disabled`)
- `button/quaternary/label/disabled` — light `#B7B7B7` → `#E1E1E1` (now aliases `text/disabled`)

No non-disabled, non-exempt token's value changed. Nothing needed flagging under the "STOP if a
non-exempt value would shift" clause — every non-disabled mapping (secondary background/label-default,
tertiary background-default/hover/label-default, quaternary background-default/hover/label-default)
already matched its target semantic's value exactly before the re-point.

`secondary/*`, `tertiary/*`, `primary/*` (the overloaded Legacy component groups) were **not touched**.

## Task 3 — regenerate + gate

- `gen_canon_tokens.py` — button vars now emit `var()` chains through the new semantic vars (e.g.
  `--button-secondary-background-default: var(--surface-action);`), not baked hex. 451 root vars / 164
  dark overrides, same totals as before the edit.
- `gen_snippet_tokens.py` / `--check` — 1127 manifest bindings, 0 values would change. Tranches stay in
  sync (they bind to `button/*`, which is unchanged from their perspective).
- `_build_all.py` — **first run hit 2 pre-existing-mechanism false positives**, both fixed rather than
  worked around:
  1. **Contrast gate** flagged `text/on-action` (dark `#000000` vs the generic page surface `#1D1D1D`,
     1.25:1) — because the generic surface-resolver in `_contrast_utils.py` doesn't know `on-action`
     tokens only ever sit on `surface/action`, never the page ground. This is the exact same shape of
     false positive the codebase already solved for `text/on-inverse` (an explicit carve-out in
     `resolve_dark_surface()`). Added the equivalent carve-out for `text/on-action`, same file, same
     pattern — it's validated correctly elsewhere in the same audit via
     `button/secondary/label/default` (10.47:1 dark, passing).
  2. **Dark-surface flatness gate** flagged `border/action-strong` (dark `#FFFFFF`, flat-white) — the
     existing exemption mechanism is a `$darkNote` annotation, which `button/tertiary/border/default`
     already carries for the identical value/rationale. Added the matching `$darkNote` to the new
     semantic token.
  - Also updated `_validate_token_tiers.py`: added the 5 `surface/action*` + `surface/transparent` +
    `text/on-action` + `border/action-strong` tokens to a new `SEMANTIC_ACTION` list (semantic tier,
    must alias a primitive) and all 16 `button/*` leaves to `COMPONENTS_ON_SEMANTIC` (component tier,
    must alias the named semantic) — otherwise the gate would only report these as **advisory**, not
    actually enforce the three-tier discipline the whole exercise is for.
- Final `_build_all.py`: **green, 35/35** — `✅ all generators ran and the integrity + contrast gates
  passed.`
- `_validate_token_tiers.py` standalone: **`token-tier gate: 0 strict failure(s), 4 advisory.`** All 4
  advisories are pre-existing, unrelated legacy drift (`border/strong`, `form/border/default`,
  `form/border/pressed`, `primary/border/hover` — all dark-mode `color/grey/dark-mode/200` cache drift,
  none touch `button/*` or the new tokens).

## Files touched

- `knowledge/tokens/semantic-colour.json` — new semantic tokens + button/* re-point
- `knowledge/_validate_token_tiers.py` — extended `MIGRATED` set (`SEMANTIC_ACTION` + button/* entries)
- `knowledge/_contrast_utils.py` — `on-action` surface-resolution carve-out
- `knowledge/canon/canon.css` — regenerated (auto)
- Build-artifact regens (audits, blast-radius, xref, consult index, tranche HTML re-projections, etc.)
  — all from running the standard generators; tranche content itself reported 0 changes for button/*.

## Nothing flagged / stopped on

Every non-disabled button value matched its target semantic exactly pre-re-point; the two gate
failures hit were audit-mechanism false positives with a direct existing precedent to extend, not
real value regressions — fixed rather than left open. Did not touch `GOOD-MORNING.md`, `_LIVE-STATE.md`,
memory, or the Legacy `secondary/*`/`tertiary/*`/`primary/*` groups. No git add/commit/stash performed;
tree left dirty for the conductor.
