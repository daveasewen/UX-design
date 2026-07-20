# ADR-0008 — Apollo is the canonical core; consumers are reached by automated adapters

**Date:** 2026-07-20 · **Status:** accepted (Dave) · **Extends:** ADR-0002, ADR-0005, ADR-0006

## Context

Building Apollo Mono surfaced a recurring tension: how closely should Apollo's own
token/component structure track an existing consumer codebase — specifically **Sutherland**
(the HSBC React library, the sparse ~36-component working file that is also the live Figma
library)? Two failure modes pull in opposite directions:

- **Follow too closely** and Apollo inherits the consumer's flaws. Concrete case this week:
  Sutherland/Legacy overloads a single `secondary` token to mean *both* a button surface *and*
  a checkbox fill. Matching that would import a naming defect into the canonical source.
- **Diverge freely** and every handoff to another team becomes a manual port — expensive,
  error-prone, and exactly the Figma → code → docs friction Apollo exists to remove.

ADR-0002 already ruled that handoff is *"a git pull, not a port"* and that model-specific
syntax lives only in *"clearly-marked adapters."* ADR-0005 ruled the knowledge engine is the
product. This ADR resolves the conformance tension those two leave open: **what is Apollo the
source *of*, and how do other codebases consume it without either constraining it or forking
from it?**

## Decision

**1. Apollo is the canonical source, not a mirror of any one consumer.** Apollo is the smart
design system meant to replace the Figma → code → docs triptych and to **serve or replace any
codebase**. Its architecture must be good enough to be *the* source of truth — a well-formed
superset — not a reflection of whichever consumer happens to be in front of us. Sutherland is a
*consumer* (and the first live-fire test), never the template.

**2. Quality is the vote-winner; never inherit a flaw to match a consumer.** Where a consumer's
structure is sound, stay cleanly mappable to it. Where it carries a defect, **do it properly in
Apollo and map across the gap**. Proof-of-pattern this week: rather than adopt the overloaded
`secondary`=checkbox-fill token, Apollo Mono minted a clean **decoupled `button/{secondary,
tertiary,quaternary}` tier** (commit `ded4900`) and left the legacy overloaded tokens untouched.
Solidity is what makes teams *want* to adopt; conformance for its own sake is not.

**3. Respect but don't follow — consumers are reached by an automated adapter/mapping layer.**
"Respect" = keep Apollo's structure a well-formed, cleanly mappable superset (not gratuitously
different). "Don't follow" = never import a consumer's flaw. Consumers (Sutherland React, the
Common Toolkit, and others later) are bridged by **machine-runnable adapters**, not hand-ports.
The seed already exists: `tokens/_manifests/sutherland-diffs.json` plus the hub-and-spoke
`codeBindings` (Figma node ID = identity; per-namespace code names).

**4. Operating principle — diverge for quality, keep every divergence expressible as an
automated transform.** *Mappable-by-machine* is the standing condition on every deliberate
divergence. A divergence that cannot be expressed as an adapter rule is not permitted; a
divergence that can is free. This is what keeps handoffs to other teams cheap rather than
onerous, and it is the concrete meaning of ADR-0002's "git pull, not a port" one layer down.

**5. Designers run the full architecture — Apollo is not a guidance-only cut.** Designers have
Python, so Apollo runs on their machines as the **full engine** (gates + generators, in-editor),
not a no-Python guidance subset. **`designer-skills-v1` must be revisited before it ships** — it
was shaped around a no-Python assumption that no longer holds.

## Consequences

- **Ground-truth plan (Sutherland as case #1).** Run Apollo in **VS Code + Copilot beside the
  real Sutherland repo** → read the actual components/tokens → build the real Apollo↔Sutherland
  map, and field-test "serve any codebase" against it. This doubles as the first live-fire of the
  designer pack.
- **`designer-skills-v1` is now on the revisit list** before it ships (see decision 5).
- **The button ladder is the reference implementation** of decision 2 — the first place Apollo
  deliberately diverged from a consumer for quality while staying mappable. Its greys/tiers go on
  the full-review backlog (`knowledge/_REVIEW-SIGNOFF.md`); the legacy `secondary/tertiary` →
  `button/*` migration + snippet-button rebind is the eventual adapter/cleanup work (flagged in
  `notes/_receipts/2026-07-20-worker-button-3tier.md`).
- **Low disruption risk, recorded.** Neither Sutherland nor the Common Toolkit is in flight; both
  teams are receptive to small, automated changes. Where friction arises, Apollo builds what is
  right and maps to it.
- **No architecture re-litigation without new evidence** — the Sutherland field test is the
  arbiter, not further desk debate (consistent with ADR-0006).

## Related

`ADR-0002` (open standards / git-pull handoff) · `ADR-0005` (engine is the product) ·
`ADR-0006` (flexing engine) · `tokens/_manifests/sutherland-diffs.json` ·
`notes/_receipts/2026-07-20-worker-button-3tier.md` · memory `apollo-canonical-core-adapters`
(+ `output-modes-portability`, `sutherland-figma-mapping`, `token-tier-architecture`).
