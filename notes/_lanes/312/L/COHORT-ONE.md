# Cohort one — Dave's fifteen, mapped to meta ids (for L2's extraction and L3's page)

Written by #312 lane L1 (Fable, cloud), Thu 2026-10-01, on the worktree at `97c7793` with the schema edit applied.
Dave's list (#312, 12:51, `notes/_lanes/312/DAVE-RULINGS-2026-10-01-1251-wave-2-calls.md`, as the conductor relayed it):
the five M2 sampled — button, tabs, table, date picker, metric — plus ten interactive neighbours: menus, accordion,
slider, switch, text input, select, dialog, tooltip, pagination, notification. Where a word is not a meta slug the
nearest meta is taken and the choice is said (brief: "take the nearest and say so in the report").

Counts in the last four columns are pasted from a grep over each snippet at this sha (`:hover|:active|:focus-visible|:disabled|:checked|:invalid`
occurrences · distinct `.is-*` classes · distinct `[aria-*` selectors · `vars` keys in `#token-manifest`); they size the extraction, nothing more.

| # | Dave's word | meta id (`knowledge/components/<id>.meta.json`) | snippet (`knowledge/snippets/`) | nearest-match note | pseudo | .is-* | [aria-* | manifest vars |
|---|---|---|---|---|---|---|---|---|
| 1 | button | `button` | `Button.reference.html` | exact | 16 | 3 | 0 | 29 |
| 2 | tabs | `tabs` | `Tabs.reference.html` | exact | 11 | 0 | 1 | 14 |
| 3 | table | `table` | `Table.reference.html` | exact; meta says `interactive: false` — expect `states` to be a one-state machine and `emits` to be `[]`, both positive declarations | 8 | 0 | 1 | 12 |
| 4 | date picker | `date-picker` | `Date-picker.reference.html` | exact (not `date-range-picker`, not `calendar`); the only cohort meta with a typed `behaviour.script` (`…#script`, 5 DOM events) | 19 | 11 | 1 | 19 |
| 5 | metric | `metric` | `Metric.reference.html` | exact; carries a `stateModel` object (5 states: ready/loading/empty/error/stale) — `states.states` should name the same five, `stateModel` is NOT edited | 8 | 3 | 0 | 14 |
| 6 | menus | `split-button` | `Split-button.reference.html` | NEAREST, not exact: no meta is named menu. `split-button` is the APG menu-button pattern (its snippet carries 13 `role="menu…"` attributes, the most of any snippet; `navigations` has 5 inside masthead flyouts, `dropdown` has 0 — it is a listbox). Caveat: `split-button` is marked PROPOSED #209, NOT GATED, NOT RULED in its own purpose line. Alternative if the conductor prefers: `navigations` (organism, 565 lines, flyout menus) | 22 | 1 | 1 | 24 |
| 7 | accordion | `accordion` | `Accordion.reference.html` | exact | 2 | 0 | 1 | 6 |
| 8 | slider | `slider` | `Slider.reference.html` | exact (single/double handle; not `range-slider`, the min/max pair) | 3 | 0 | 0 | 8 |
| 9 | switch | `selection-controls` | `Selection-controls.reference.html` | NEAREST: switch has no meta of its own; it is one member of the Selection-controls family (checkbox, radio, chips, switch — `role="switch"` ×4 in the snippet). The draft will cover the whole family; the review page should show the switch part first | 52 | 1 | 2 | 15 |
| 10 | text input | `input-fields` | `Input-fields.reference.html` | NEAREST: the family of single-line, large, multi-line and date-picker inputs; `textarea`, `search-field`, `amount-input` are separate metas and NOT in cohort one | 20 | 7 | 0 | 15 |
| 11 | select | `dropdown` | `Dropdown.reference.html` | NEAREST: the non-native (custom listbox) and native `<select>` families live in one meta; `combobox` and `multi-select` are separate metas, not in cohort one | 5 | 0 | 2 | 14 |
| 12 | dialog | `modals` | `Modals.reference.html` | NEAREST: Dialog is the first member of the Modals family (`role="dialog"` ×1); `modal-lightbox`, `confirmation`, `popconfirm`, `drawer` are separate metas, not in cohort one | 15 | 1 | 0 | 18 |
| 13 | tooltip | `tooltip` | `Tooltip.reference.html` | exact | 1 | 0 | 0 | 6 |
| 14 | pagination | `pagination` | `Pagination.reference.html` | exact | 8 | 0 | 2 | 9 |
| 15 | notification | `notifications` | `Notifications.reference.html` | exact (the RAG family in four placements; `toast`, `alert`, `banner` are separate metas, not in cohort one); `stateModel: "simple"` | 13 | 5 | 0 | 12 |

The id list, one line, for `extract_spec.py --only`:

```
button tabs table date-picker metric split-button accordion slider selection-controls input-fields dropdown modals tooltip pagination notifications
```

None of the fifteen carries `aliasOf` (the s210-D5 fence bans the four fields on `kpi-tile`, `limits-meter`, `progress-bar`, `stat-card`; none is in the cohort). Every snippet except `Metric` carries one executable `<script>` beside its `#token-manifest`; Metric's states come from `.is-*` classes and the meta's `stateModel`. No cohort snippet uses `[data-state]`.

## What the schema accepts (L2 writes exactly this shape)

`knowledge/_probe_registry/probe_meta_schema.py` `SPEC_DRAFT` is the proven shape — the selftest's positive control validates it on `button.meta.json` with zero findings. The rules the schema enforces, so the extraction does not learn them from a red gate:

1. `anatomy` is ONE root node `{part, tag, attrs?, aria?, slot?, text?, children?[]}`; `part` and `tag` are lower-kebab; `aria` takes only `role` and `aria-*` keys; a state attribute is a hole `"{state.open}"`, a prop hole `"{props.label}"`, each the WHOLE value. `$`-notes allowed on any node.
2. `states` requires `states[]` (unique, ≥1) and `initial`; `transitions[{from,on,to,guard?}]` and `keys{Key: action}` are optional inside the field (a passive part has none).
3. `emits` is an array of `{name, detail{}}` (+ optional `when`); `name` lower-kebab (convention `apollo-…`); `detail` maps payload key → type word; `[]` is a positive "fires nothing". `behaviour.events` is untouched.
4. `bindings` keys match `^--[A-Za-z0-9_-]+$`; values are references `{…}` with no `{`, `}` or whitespace inside (DTCG `{group.token}`, dot-joined; today's slash path `text/default` is REFUSED — write `{text.default}`; resolution against `knowledge/tokens/` by swapping `.` → `/` is L2's coverage rule, not the schema's).
5. Any of the four on a meta REQUIRES `$extracted` `{by, date (YYYY-MM-DD), reviewed:false, source?, sha?, fields?[]}` (Draft 7 `dependencies`).
6. An `aliasOf` meta may carry none of the five (the s210-D5 fence, extended).
7. Nothing else in the meta is renamed or required; `tokens`, `stateModel`, `behaviour`, `codeBindings` stay as they are.
