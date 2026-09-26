# SPEC — the deterministic when-evaluator (R5 · 5a writes, 5c executes) · probe, not canon

Input: an INTENT CONTEXT — a flat dict whose keys are names from knowledge/when-fields.json `fields`
(39 today) and an optional ROLE (a knowledge/roles.json slug). Output: the ONE winning part, the ranked
eligible list, and for every candidate the per-clause verdicts. Same input, same output, no network,
no model, no Jev.

1. Candidates = metas carrying `when` (39 today). With a role: only metas that provide it
   (meta.provides, an edges.providesRole ref, or the role's providers list in roles.json).
2. Parse each `when` by its own registry grammar (when-fields.json `$grammar`): GATE = text before the
   first U+2014; clauses joined by AND / OR (AND binds tighter); a clause opening with a registered
   field name followed by an operator (= == != >= <= ≥ ≤ < > in spans, or a bare range `N–M`) is a
   FIELD CLAIM; anything else is PROSE and is not judged. The prose half after the dash is never parsed.
3. Evaluate each field claim against the context: TRUE / FALSE, or UNKNOWN when the context lacks the
   field. Prose clauses are UNKNOWN. Three-valued AND/OR. `series none` = 0. Address fields (answers,
   shape) match the longest registered address (chart-intents.json / shapes.json) at the value's head.
   `answers spans A AND B` consumes the AND-joined addresses and is TRUE only if the context's answers
   include all of them.
4. A candidate is ELIGIBLE unless its gate evaluates FALSE (open world: UNKNOWN does not exclude).
5. Rank eligible candidates by (a) the number of TRUE field claims, descending — the more specific
   claim that holds beats the default; (b) meta `priority`, descending (absent = 0); (c) slug, ascending.
   The first is the pick. A seam sits between 4 and 5: a ranker (Jev, per Dave 26 Sept 14:51, not used
   here) may only re-order the ELIGIBLE list, never add to it; off by default, and the order in 5 is the
   fallback when it is off, slow or down.
6. Report every miss by name: a part with no `when` cannot be chosen; a context key no gate reads is
   ignored; prose clauses that decided nothing are listed.
Compared against THE READER (knowledge/_compose_slice.py build_slice with the typed intent/shape/role):
the reader's pick is its first non-alternate row carrying the role.
