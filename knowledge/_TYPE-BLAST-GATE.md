# Type-binding blast-radius gate — guards canon/type.css

Every selector appended to a composite list is a GLOBAL rule. Registry: `canon/_type-bindings.json`. Corpus: snippets + _proforma (151 files).

| radius | kind | selector | status |
|---:|---|---|---|
| 28 | class | `.btn` | PASS |
| 15 | class | `.chip` | PASS |
| 14 | scoped-element | `.seg button` | PASS |
| 12 | class | `.stateLabel` | PASS |
| 8 | class | `.status` | PASS |
| 8 | scoped-element | `.seg.sm button` | PASS |
| 7 | scoped-element | `.search input` | PASS |
| 5 | class | `.spec-h` | PASS |
| 4 | class | `.eyebrow` | PASS |
| 4 | class | `.label` | PASS |
| 4 | scoped-element | `.seg.l button` | PASS |
| 4 | scoped-element | `.seg.md button` | PASS |
| 3 | class | `.action-bar .btn` | PASS |
| 3 | class | `.avatar` | PASS |
| 2 | class | `.badge` | PASS |
| 2 | class | `.confirm .btn` | PASS |
| 2 | class | `.hero .cta` | PASS |
| 2 | class | `.pg .ctrl` | PASS |
| 2 | class | `.qbtn` | PASS |
| 2 | scoped-element | `.pg a` | PASS |
| 2 | scoped-element | `nav.main a` | PASS |
| 1 | class | `.loader` | PASS |
| 1 | class | `.sim` | PASS |
| 1 | class | `.time` | PASS |
| 1 | scoped-element | `.nav button` | PASS |
| 1 | scoped-element | `.note.global .actions button` | PASS |
| 1 | scoped-element | `.seg.lg button` | PASS |
| 0 | class | `.tabbar .tabbar__item` | PASS |

## Findings

- ✓ every appended selector is registered and within its acknowledged blast radius.

## Housekeeping (non-gating)

- shrunk: `.eyebrow` no longer matches ['Template-wizard.reference.html'] (safe; tidy the registry with --update).
- shrunk: `.action-bar .btn` no longer matches ['Template-list-index.reference.html'] (safe; tidy the registry with --update).
- shrunk: `.badge` no longer matches ['Page-header-lockup.reference.html'] (safe; tidy the registry with --update).

---
Guard-rail for the T-D9 binding mechanism (T-D12 §5). Waived entries are DEBT to burn down (namespace them) — priority `h2` (25 files) in the non-/1 batch. This gate does NOT reopen T-D9.
