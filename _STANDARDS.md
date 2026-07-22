# Apollo — Engineering & Design Standards

> STANDING: the Apollo standards hub — read before designing anything. Reachability-gated (STAND-003).

*This is a standing, load-bearing document. It defines the standards every part of Apollo is held to.
It is not aspirational and it is not optional: where a standard here can be gated, it is gated, and the
gate is the enforcement (see §0). This is a professional product, not a hobby project — treat deviations
as defects, not preferences. Reachability-gated by `_validate_standing_instructions.py` (STAND-002).*

Last substantive update: 2026-07-19 (token-tier architecture ratified; elevation is the reference example).

---

## §0 — First principles (these govern everything below)

1. **Retrieval, not recall.** Brand and design values are retrieved from the token stores. Generated or
   hand-written work must not embed values that could drift off-source. If you typed a hex into a
   component, you did it wrong.
2. **Verification = enforcement.** Judgment is encoded as **blocking gates**. "Done" is withheld until
   they pass. *If a standard is not gated, assume it will be broken.* A standard added here should come
   with a gate, or a note on why it can't yet be gated and what interim check stands in.
3. **Single source of truth, resolved at build time.** Every value has exactly one authoritative
   definition; everything else references it. Resolved copies (caches) are permitted only when a gate
   proves the cache equals its source. This is the Style Dictionary model and it is the project default.
4. **Accessibility is a floor, not a target.** WCAG 2.2 AA is the minimum, applied as a build gate, not a
   review checklist. Where a ruling and the floor conflict, the floor wins and the ruling is re-cut.
5. **Canonical, not conformant** (Dave 2026-07-20). Apollo is the **canonical source of truth** — it serves or
   replaces any codebase; consumers (Sutherland React, Common Toolkit, others) are reached by **automated adapters**,
   never by bending our architecture to theirs. **Diverge for quality; keep every divergence expressible as an
   automated transform** (respect ≠ follow). Quality beats conformance; if forced, we build what's right and map
   after the fact. Memory `apollo-canonical-core-adapters`; formal ADR owed.

---

## §1 — Design token architecture: the three-tier stack

Apollo tokens follow the W3C **Design Tokens Community Group (DTCG)** format and a strict **three-tier
reference model**, the same taxonomy used by Material Design 3 (*ref → sys → comp*), Adobe Spectrum,
Salesforce Lightning, and USWDS. The tiers, top (rawest) to bottom (most specific):

### Tier 1 — Primitives (a.k.a. reference / global / option tokens)
Raw, context-free values. The palette and the raw scales. A primitive **means nothing on its own** — it
is just a number with a name.
- Home: `knowledge/tokens/colour.json` (`color/*`), plus the raw scales in `typography.json`,
  `spacing.json`, etc.
- Examples: `color/mono/1..15`, `color/white`, `color/mono/raise-1`.
- Rule: primitives hold a literal value and **never reference another token**.

### Tier 2 — Semantic (a.k.a. system / alias / decision tokens)
Intent and purpose. A semantic token answers *"what is this for?"* and **references a primitive**. This
is where light/dark and other mode decisions live.
- Home: `knowledge/tokens/semantic-colour.json`.
- Examples: `text/default`, `border/subtle`, `surface/raised` → `{color.mono.raise-1}` (dark).
- Rule: a semantic token references **exactly one primitive per mode**, never a raw value of its own,
  never another semantic or component token.

### Tier 3 — Component
Component-scoped decisions. A component token answers *"what does THIS component use here?"* and
**references a semantic token**.
- Home: `knowledge/tokens/semantic-colour.json` (component-named groups) → the snippet `#token-manifest`
  → the component's CSS var.
- Examples: `tertiary/background/default` → `{surface.raised}`, `tabs/background` → `{surface.raised}`.
- **THE RULE (Dave, 2026-07-19): a component token references a semantic token — NEVER a primitive, and
  never a raw value.** If no semantic token fits, you add a semantic token; you do not reach past the
  tier. This is gated by `_validate_token_tiers.py`.

```
  component  →  semantic  →  primitive  →  value
  tertiary/background/default → surface/raised → color/mono/raise-1 → #1F1F1F   (dark)
```

### How the reference is stored (the value/alias contract)
Each token carries **both** a resolved `$value` (per mode) **and** an `$alias` (per mode) naming the token
it references. The **`$alias` is the source of truth**; the `$value` is a build-time **resolved cache**.
`_validate_token_tiers.py` gates that `$value == resolve($alias)` for every aliased token, following the
chain to a primitive — so the cache can never drift from the reference, and every hex-consuming gate can
keep reading `$value` cheaply. `gen_canon_tokens.py` emits the real `var()` chain into `canon.css` from
the `$alias`, so the cascade — not a baked hex — carries the value at runtime.

### Naming
`group/role/state` in the token store; flattened to `--group-role-state` as a CSS var. Modes (`light`/
`dark`) are leaves, stripped from the var name and split into `:root` / `[data-theme="dark"]`.

---

## §2 — Colour & elevation

- **Apollo Mono baseline:** monochrome throughout; colour appears **only** in RAG status and data-vis.
  Neutral scale is `color/mono/1..15` (a designed dual-end brightness curve), not `color/grey/*` (Legacy).
- **Digital black `#1A1A1A` (`mono/4`)** is the page ground and the general substitute for `#000` where
  light/reverse text sits on the dark ground. Pure `#000` remains correct for borders, marks, and rules.
- **Dark-mode elevation (the reference example of the three-tier stack).** The mono ramp jumps from the
  `#1A1A1A` ground straight to `mono/5 #313131`, so raised surfaces need a dedicated, subtle elevation
  scale. Primitives `color/mono/raise-1/2/3` = `#1F1F1F / #232323 / #272727` (dialled by Dave on the v2
  tuner, 2026-07-19). Semantic surface tokens sit on them:
  - `surface/raised` — light `#FFFFFF`, dark `#1F1F1F`. White-in-light raised surfaces.
  - `surface/subtle` — light `#F0F0F0`, dark `#1F1F1F`. Grey-in-light filled surfaces (table headers,
    scrollbar track).
  - `surface/raised-hover` — light `#F0F0F0`, dark `#232323`.
  - Press/active states **recede to the `#1A1A1A` ground** — that IS the press feedback (raised →
    ground), so they need no raise token; `raise-3 #272727` is reserved for the highest-elevation /
    interaction-state work in the button-state migration.
- **Colour stability (astigmatic calibration, Dave):** blue + green are the stable isoluminant pair;
  **red and amber each carve out** their own handling. Categorical colour is isoluminant (no dominance);
  status colour is a salience ramp (loudness tracks severity).

---

## §3 — Accessibility (WCAG 2.2 AA floor, gated)

- Text contrast ≥ **4.5:1** (≥ 3:1 for large text); non-text/UI (borders, icons carrying meaning) ≥
  **3:1** (SC 1.4.11). Gated by the contrast audits; disabled elements are exempt per spec.
- Contrast is checked **against the actual ground**. A neutral that passes on white can fail on the
  `#1A1A1A` ground — see the R-D16 carve-outs (dark borders on `mono/8`, text-bearing pressed fills on
  `mono/7`).
- Glyph contrast is **by role** (R-D6): a glyph paired with a meaning-carrying label needs 3:1; a glyph
  carrying the meaning alone needs 4.5:1.
- Keyboard focus visible (SC 2.4.7); focus ring is a token (`focus/ring`), not a component decision.
- Every interactive state (hover/pressed/active) must be **more** than a single-colour change and must
  itself clear the floor.
- Aspiration (ADR-0004): the most digitally accessible bank. AA is the floor, not the ceiling.
- **Theme carve-out (R-D24): Apollo Legacy is EXEMPT from this floor** — it faithfully reproduces the
  existing HSBC legacy interfaces, so its historically sub-AA pairs stand as-built and are recorded as
  *exempted* (not passes) via `RULED_PAIR_EXCLUSIONS` tagged `theme=legacy`. Mono / Console / Supercharge
  are unaffected — the floor holds for every theme except Legacy.

---

## §4 — Component authoring

- **No hardcoded styling.** Colour, spacing, radius, and border-stroke are tokens (`var(--…)`), never raw
  values, so a mode can override them (gates: universal colour gate + DEF-004). px is allowed only inside
  a `var()` fallback.
- **Snippets are styled BY the tokens.** A reference snippet's `[data-theme]` values are **generated**
  from the token store by `gen_snippet_tokens.py` via the snippet's own `#token-manifest`; they are never
  hand-typed and cannot drift (`_validate_snippets.py` enforces fidelity; the generator establishes it).
- **Icons:** real assets only (sprite + manifest + gate); never invent an icon. New surfaces must wire
  their icon gate before shipping.
- **Grid:** 4px. **Corners:** square in Mono. **Type:** sentence case; component text uses the canon
  `type.css` composites, never raw font shorthand. **Weights:** five licensed only —
  100/300/400/500/700, no 600; no light/ultra on body sizes.

---

## §5 — Process & governance

- **Promotion is Dave's alone.** The engine never derives-and-promotes. DS errors go to
  `_DS-IMPROVEMENTS.md`, not silent fixes.
- **Decisions ship as reviewable artefacts.** Material/feel decisions ship as a review HTML with the
  comment overlay; for "how much" dials (colour steps, elevation, spacing) default to a **live
  controller** that previews real components and emits the token values.
- **Docs ship clean + REVIEW.** Every review doc has a clean source and a generated `.REVIEW.html`.
- **Gate, don't patch.** A recurring cross-file fix becomes a gate on the condition, not an Nth patch.
- **The record is the repo.** Durable decisions are inscribed in their repo home (ledgers, this file),
  never memory-only. Mark what was OBSERVED vs INFERRED; stamp dates from `date`.

---

## §6 — Cited standards (align to these; don't reinvent)

- **W3C Design Tokens Community Group** format specification — the token file format.
- **Material Design 3** token tiers (reference / system / component) — the three-tier model.
- **Style Dictionary** (Amazon) — reference resolution, build-time resolved values.
- **WCAG 2.2 AA** (W3C) — the accessibility floor, esp. SC 1.4.3, 1.4.11, 2.4.7.
- **DTCG `$type` / `$value` / alias `{group.token}`** conventions throughout.

---

*Change control: this file is edited deliberately, dated, and re-gated. If you are a fresh session,
read it before designing anything, and CONSULT (`python3 knowledge/_consult.py "<x>"`) for the rule that
governs a specific case.*
