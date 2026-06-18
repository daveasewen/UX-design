# Confidence vocabulary

Every assertion in the knowledge base carries an implicit **confidence tier**. This formalises the in-prose convention already used across the component metas (Graphify-borrow #1) so that "what is observed fact vs. what is reasoned and needs checking" is gradeable and discoverable rather than buried in free text.

## Tiers

| Tier | Meaning | Graphify analogue | In the queue? |
|---|---|---|---|
| `asserted` | Observed directly from Figma (variant set, bound token, node) or an authoritative HSBC doc. The default. | EXTRACTED | No — not listed |
| `inferred` | Reasoned from context. Stated as fact but not directly observed; lower urgency to confirm. | INFERRED | Yes (🟡) |
| `review` | Inferred **and** explicitly flagged for human verification before it is treated as canon. | AMBIGUOUS | Yes (🔴) |

## Authoring convention

When writing a meta, mark anything not directly observed:

- Prefix a string with **`REVIEW`** (e.g. `REVIEW (inferred): …`, `REVIEW — no live equivalent`) to put it in the **review** tier — the human must confirm it.
- Use the words **inferred / assumed / likely / to confirm** (without `REVIEW`) for the **inferred** tier — reasoned, but not blocking.
- Anything else is **asserted** by default. Only assert what was actually observed in Figma or an authoritative source.

## Generated surface

`_build_review_queue.py` scans every `components/*.meta.json`, classifies each string by these rules, and writes:

- `_REVIEW-QUEUE.json` — machine list: component, field path, tier, category, text.
- `_REVIEW-QUEUE.md` — human worklist grouped by category (token-rebind, accessibility, anti-pattern, other) then component.

Regenerate after editing metas:

```
python3 knowledge/_build_review_queue.py
```

## Why it matters

The **token-rebind** review items gate the Sutherland migration — each names a best-guess replacement (or a "no live equivalent" blocker) that must be confirmed against the real Sutherland values before any rebind. The **accessibility** review items are the list to validate in code / with the accessibility team, since Figma shows visual states but not the programmatic semantics (focus indicators, accessible names, landmarks). Promote an item to `asserted` (drop the `REVIEW` marker) once verified, then regenerate.
