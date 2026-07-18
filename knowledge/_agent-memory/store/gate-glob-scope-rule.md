---
name: gate-glob-scope-rule
description: "RULE: a rule is only as wide as its gate's glob. 'Blocking' describes the rule; the glob decides where it bites. Any new surface needs its gates wired explicitly."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0ca1a754-0be4-4e9b-a84b-a28410f8f19e
---

**A rule is only as wide as its gate's glob.** "Blocking" describes the *rule*; the **glob** decides where
it actually **bites**.

**Why:** `{#type26-019}` (no uppercase outside acronyms, brand-wide, dyslexia rationale) was promoted
advisory→**blocking** by Dave on 2026-07-02. But it was only ever implemented in
`_validate_snippets.py`, which globs `snippets/*.reference.html`. **`_proforma/` was never scanned** — so
four tranche files carried `text-transform:uppercase` past a blocking rule for weeks, with a green build
the whole time. Found 2026-07-18 *by accident*, while grepping for letter-spacing.

**How to apply:**
1. **When a new SURFACE appears** (`_proforma/` was one; `_review/`, `reviews/`, future template/shell
   dirs are others) — enumerate which gates should cover it and wire them **explicitly**. A surface is
   ungated until proven otherwise.
2. **When promoting a rule to blocking** — check every surface the rule claims to govern is inside some
   gate's glob. "Brand-wide" in the rule text means nothing to a glob.
3. **Put the check in the gate that owns the surface**, not by widening another gate's glob.
   On 07-18 the fix went into `_validate_proforma.py` (which already declares itself home to "the
   UNIVERSAL rules") rather than pointing `_validate_snippets` at `_proforma` — the latter would also
   have fired token-parity, ARIA, contrast and focus checks calibrated to a different surface.
4. **Bite-test every new check** — reintroduce the violation and confirm the gate fails. A gate that
   cannot fail is worse than no gate, because it manufactures confidence.

**Same family as:** [[gate-blindspot-state-contrast]] (declared-pairs-only contrast hid real fails),
[[icon-source-rule]] (new surfaces need their icon gate wired), and the 07-18 type gate that reported
"clean across 50 files" because it skipped anything containing a `var()` — green on the very badge that
motivated it.

**The measurable version of this problem:** `42 of 54 BLOCKING rules are cited by no gate` — today's
blind-spot is one instance of that backlog. The `verified_by` edge mechanism in the compliance graph
already exists for WCAG SCs; extending it to house rules turns the unknown into a triaged list. See
[[compliance-verified-by-edges]], [[procedural-debt-and-method]].
