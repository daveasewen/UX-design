# Design-system token gaps & wiring issues

> Consolidated from the full component-ingest sweep of the HSBC Common Toolkit "Gaps and edits" branch (fileKey `Cgbtrmfp15ruNFkIAClpkI`). Each item lists the evidence (components that surfaced it), the impact, and the recommended action. Prioritised P1→P5. Per-component detail lives in `knowledge/components/*.meta.json` and `_INGEST-NOTES.md`; per-token rebinds in `depricate-replacement-map.json` (`$usage_audit`, `$interactive_namespace_note`, `$tabs_wiring_note`).

> **⚠️ CORRECTION 2026-07-05 — NO LONGER BLOCKED.** The claim below that this is "blocked on the
> Sutherland tokens JSON … can't start until the JSON exists" is **STALE**: the export **landed
> 2026-06-17** (`tokens/_raw/brand/` + `semantic-color/` + `semantic-scale/`; diffs + fixtures already
> computed). The migration is **unblocked and is our work now, not a wait.** Full state + phased plan:
> **`knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`**. Read the strike-through below as history.
>
> **⏳ ~~PARKED (~1–2 weeks, blocked on the Sutherland tokens JSON)~~ — Sutherland token migration.** ~~This is NOT the immediate next task; it can't start until the JSON exists.~~ Sutherland will become the canonical token source, imported into Figma as a couple of modes. When the Sutherland tokens JSON is exported: (1) drop in `knowledge/tokens/_raw/`, reconcile into the store, re-validate all component metas; (2) check whether Sutherland supplies the **P1** subtle-surface family and **P4** `rag/neutral-tint` (likely closes those gaps); (3) build the final rebind worklist + deletion-safety check. **Order is strict: import modes → rebind every in-use depricate (layers + aliases) to its live target → re-verify zero references → THEN delete. Importing modes is NOT rebinding; do not delete on import.** Tabs (P3) is a good first rebind candidate.

---

## P1 — Missing subtle-surface token family (blocks depricate bulk-delete)

**Gap.** There is no live semantic token for the light neutral "subtle surface" tints, nor for the on-dark surfaces. Components still bind the deprecated `non-interactive (depricate)/surface/*`:
- `surface/neutral-1` (#f3f3f3) and `surface/neutral-2` (#ededed) — light subtle surfaces.
- `surface/black` (#000) and `border/on-light/neutral-6` (#767676) — on-dark surface/border.

**Evidence (in use, no clean rebind).** Avatar (6 tokens, original blocker), Headers (Section Titles surface), List items (Item/Badge/Transaction + Item on-dark), Navigation (user flyout), Quick actions (chip tint), Tags (filled tag fill, light + on-dark), Switch (disabled track).

**Impact.** These deprecated tokens **cannot be deleted** until live equivalents exist and the components are rebound — this is the top blocker for retiring the 147-token depricate set.

**Action.** Create a live subtle-surface family — e.g. `surface/subtle/1` (#f3f3f3), `surface/subtle/2` (#ededed) plus their on-dark mode values, and an on-dark surface/border pair to replace `surface/black` + `border/neutral-6`. Then rebind the components above and delete the depricates.

---

## P2 — `interactive/on-light/*` namespace: confirm canon vs Sutherland

**Gap.** The Navigation **search flyout** binds a LIVE `interactive/on-light/*` namespace (`surface/primary/default`, `border/active/default` #000, `surface/brand-1/default` #db0011 + `/disabled`) — the exact un-suffixed mirror of the `interactive (depricate)/on-light/*` set, and the obvious 1:1 migration target. **But it is absent from the canonical variable export/store.**

**Evidence.** Only the nav search-flyout instance uses it; the standalone Search field component uses live `form/*` + `tertiary/*` instead — suggesting the namespace is Sutherland-mode or an uncaptured collection, not canon.

**Impact.** Decides the migration strategy for the entire `interactive (depricate)/on-light/*` family.

**Action.** Confirm whether `interactive/on-light/*` is canonical.
- If **canon** → migrate by dropping the ` (depricate)` suffix (1:1, tidy).
- If **not** (Sutherland/uncaptured) → use the FALLBACK already proven across Dropdown/Input/List/Nav/Modals: rebind by context (surface/primary → background/default | form/background/* | tertiary/background/*; border/active → form/border/active; high-contrast → form/border/default; low-contrast/disabled → form/border/disabled; surface/brand-1 → primary/background/default; border/brand-1 → primary/border/default).
- **Either way the depricate bulk-delete is NOT blocked on this** — every token already has an in-store target. See `$interactive_namespace_note`.

---

## P3 — Tabs wired to the wrong tokens (loses dark mode)

**Gap.** A full **mode-aware `tabs/*` semantic group exists** (`tabs/active` #db0011/#fff, `tabs/background`, `tabs/overflow-background`, `tabs/overflow-border` #000/#fff, `tabs/standard-border` #d7d8d6/#fff) but the **Tabs component does not bind it**:
- selected indicator → `color/primary` primitive (no dark value)
- track → `divider/border/section`
- overflow border → `form/border/active`
- surfaces → `tertiary/background/*` + `interactive (depricate)/surface/primary`

**Impact.** Tabs render correctly in light mode but **lose every dark-mode swap** the `tabs/*` tokens were built to provide.

**Action.** Rewire Tabs onto `tabs/*`: selected → `tabs/active`, track → `tabs/standard-border`, overflow border → `tabs/overflow-border`, surfaces → `tabs/background` + `tabs/overflow-background`. See `$tabs_wiring_note`. (No new tokens needed — purely a binding fix.)

---

## P4 — Missing `rag/neutral-tint`

**Gap.** The `rag/*` tint set has `error-tint`, `warning-tint`, `success-tint`, `information-tint` — but **no `rag/neutral-tint`**, even though `rag/neutral` (#767676) exists.

**Evidence.** Status indicator: approved/declined/pending disabled dots use the rag/*-tint set, but the **cancelled-disabled** dot has no tint sibling, so it falls back to the deprecated `non-interactive (depricate)/surface/neutral-3`.

**Impact.** A small but clear inconsistency — one status can't be expressed with live tokens in its disabled state.

**Action.** Add `rag/neutral-tint` (completing the tint set), then rebind the cancelled-disabled Status indicator dot.

---

## P5 — `color/primary` primitive leaks (no semantic `icon/brand`)

**Gap.** Several components bind the brand-red **primitive** `color/primary` (#db0011) directly rather than a semantic token, so they can't respond to mode/theme changes and bypass the semantic layer.

**Evidence.** Badge (surface), Hero (arrow/CTA accent), Links (Arrow link chevron), Tabs (selected indicator — see P3). Also bullets/sections binding `colour/neutral/grey-1` directly.

**Impact.** Brand-colour usage isn't governed by the semantic layer; no single place to retheme.

**Action.** Introduce semantic tokens for these usages (e.g. an `icon/brand` for the red chevron/indicator, and route brand surfaces through `primary/background/*`), then rebind. Lower priority — values are correct today; this is governance/maintainability.

---

## Also noted

- **Bottom nav bar raw shadow** — uses a non-tokenised `DAY/colour-level-shadow-1` (#0000001A) instead of `elevation/functional`. Re-token.
- **Second legacy namespace** — beyond `(depricate)`, an older `Non-interactive/Content/On Light/colour-content-primary` (#333333 → text/default) appears on Hero. Watch for these when de-duping.
- **Dedicated semantic groups that DO exist and are used well** — `form/*`, `table/*`, `progress/*`, `overlay/*`, `blur/*`, `scrollbar/*`, `elevation/functional`, `rag/*` (minus neutral-tint). The pattern to fix (P3/P5) is components bypassing their own semantic group for primitives/tertiary.
