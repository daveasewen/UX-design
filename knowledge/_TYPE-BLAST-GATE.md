# Type-binding blast-radius gate — guards canon/type.css

Every selector appended to a composite list is a GLOBAL rule. Registry: `canon/_type-bindings.json`. Corpus: snippets + _proforma (79 files).

| radius | kind | selector | status |
|---:|---|---|---|
| 12 | class | `.btn` | PASS |
| 8 | scoped-element | `.seg button` | PASS |
| 7 | class | `.stateLabel` | PASS |
| 5 | class | `.spec-h` | PASS |
| 4 | class | `.chip` | PASS |
| 4 | scoped-element | `.seg.sm button` | PASS |
| 3 | class | `.label` | PASS |
| 3 | scoped-element | `.search input` | PASS |
| 2 | class | `.avatar` | PASS |
| 1 | class | `.action-bar .btn` | PASS |
| 1 | class | `.badge` | PASS |
| 1 | class | `.confirm .btn` | PASS |
| 1 | class | `.eyebrow` | PASS |
| 1 | class | `.hero .cta` | PASS |
| 1 | class | `.loader` | PASS |
| 1 | class | `.pg .ctrl` | PASS |
| 1 | class | `.qbtn` | PASS |
| 1 | class | `.sim` | PASS |
| 1 | class | `.status` | PASS |
| 1 | class | `.tabbar .tabbar__item` | PASS |
| 1 | class | `.time` | PASS |
| 1 | scoped-element | `.nav button` | PASS |
| 1 | scoped-element | `.note.global .actions button` | PASS |
| 1 | scoped-element | `.pg a` | PASS |
| 1 | scoped-element | `.seg.lg button` | PASS |
| 1 | scoped-element | `.seg.md button` | PASS |
| 1 | scoped-element | `nav.main a` | PASS |

## Findings

- ✓ every appended selector is registered and within its acknowledged blast radius.

---
Guard-rail for the T-D9 binding mechanism (T-D12 §5). Waived entries are DEBT to burn down (namespace them) — priority `h2` (25 files) in the non-/1 batch. This gate does NOT reopen T-D9.
