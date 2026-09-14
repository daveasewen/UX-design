# GATE-SHAPE — how the existing gates could check a page against the slice

#270 lane 2 (the compose-time door). **PROPOSAL ONLY. No gate was edited, and none should be
until Dave rules the tier.** Everything below names the file, the function and the line the
change would touch, so the cost is readable without opening anything.

## The idea in one sentence

The slice that ANSWERED "what do I compose with?" is the same object that can answer "did you
compose with it?" — so the compose-time door is also a **gate input**, and the gate stops being
a list of hand-written checks about a page in general and becomes a comparison against *this
page's own declared slice*.

  [[no-gate-parses-the-artefact]] — nine release gates parsed the manifest and not one opened
  the pack and looked at the demo. The same shape is available here in reverse: a gate that
  parses the PAGE but has no statement of what the page was supposed to contain can only check
  universals (rogue hex, unresolved classes). A slice is that missing statement.

## The seam that already exists: the provenance receipt

`_validate_screen.py::gate_receipt` (step 0) already PARSES a `#provenance-receipt` block on the
page and re-hashes every spliced region against it (`s235-D1`/`s234-D6`). That is the seam. A
composed page would carry **one extra key in the receipt it already carries**:

```
"compose-slice": { "task": "<the task sentence>", "sha256": "<hash of the slice JSON>",
                   "path": "notes/_lanes/.../SLICE-n.json", "tool": "_compose_slice.py v0.1" }
```

No new file format, no new discovery mechanism, no new place for a page to declare anything.
A page with no `compose-slice` key reports `UNPROVEN:NO-SLICE` and does **not** block — the same
ADR-0016 posture `gate_receipt` already takes for `UNPROVEN:NO-RECEIPT`, and for the same reason
([[gate-cannot-pass-in-one-environment]]: every page in the repo predates the slice).

## The four checks, cheapest first

| # | check | gate | what it reads | posture |
|---|---|---|---|---|
| S1 | **OUT-OF-SLICE COMPONENT** — every `.cn-<component>` scope class on the page is a component in the slice (or an `alternate`, which reports ⚠ and names the primary it displaced) | `_validate_compose.py::check_screen` — it already extracts every `.c-*`/`.cn-*` class for check 6 (CLASSES RESOLVE); the slice membership test is one set-difference on a list it already has | the page + the slice | **the candidate for BLOCKING**: this is the anti-invention check the generate skill's hard rule 1 states in prose and nothing enforces |
| S2 | **ANTI-NEIGHBOUR VIOLATED** — no two components in the page are a `mustNotNeighbour` pair from the slice's `antiNeighbours` | `_validate_composition.py` (already the adjacency home: C8 ID-9 adjacency is there) | the page's DOM order + the slice | advisory at birth. 51 of the 70 `mustNotNeighbour` edges carry `ref: null`, so most pairs are PROSE and cannot be mechanically checked yet — that is the honest limit, and it is in the slice as `ref:null` + `$note` |
| S3 | **BLOCKING RULE UNADDRESSED** — every rule in the slice with `blocking:true` and `confidence:"authored"` has a check that ran. Today `aca-003` (unique title) and `aid-009` (44×44 target) are already checked inside `_validate_compose` and `_validate_a11y`; the slice's job is to say **which blocking rules applied to THIS page**, so a page whose slice carries `dv-017` (palette-only chart colour) and never ran a dataviz check reports the gap instead of passing silently | `_validate_screen.py::main` — the step list, as a report line per rule | the slice + which gates ran | advisory: it reports COVERAGE, it does not judge the page. This is the [[instrument-without-a-consumer]] fix for `_rules-index.json`'s `destiny` field, which today no page-level gate reads |
| S4 | **TOKEN TIER ESCAPE** — every `var(--x)` the page's own style sets resolves to a token GROUP that is in the slice's `tokens`. A page reaching for `--data-series-7` when no chart is in its slice is a drift signal | `_validate_compose.py::check_screen` (checks 4/5 already walk the page's own `<style>` for exactly this class of escape) | the page + the slice | advisory |

`_validate_demo_page.py` needs **no change**: it drives the real page in a browser and grades
what it sees. Its relationship to the slice is the other direction — the slice is what the
DEMO PROMPT should have produced, so a future bite could compare the generated page's component
set against the slice built from the same prompt. That is a cold-run instrument, not a gate.

## What it would cost

- `_compose_slice.py` gains `--check <page.html> --slice <slice.json>` (returns S1/S2/S4 rows as
  JSON; the gates call it, so the comparison logic has ONE home, the same way `_search_core.py`
  is the one home for ranking).
- `_validate_compose.py`: ~20 lines in `check_screen`, all behind `if slice is None: return`.
- `_validate_screen.py`: one extra step in the docstring's numbered list + one report line.
- No meta, no registry, no schema, no skill changes. The receipt key is additive.

## What would make S1 blocking honest

Three things, none of them this lane's to rule:

1. The generate skill's step 1 actually emits a slice (the decision on the proposal page).
2. A composed page carries the receipt key — today most composed pages carry no receipt at all,
   so S1 would be `UNPROVEN` on nearly the whole population on day one.
3. `provides` authored on more than 24 of 138 metas, so "out of slice" is a statement about
   ROLES and not about a text-match. **Lane 1 of #270 is exactly this.** Until then S1 is
   checkable but its denominator is soft, and a gate whose denominator is soft should report,
   not refuse.
