# Type-binding blast-radius gate — guards canon/type.css

Every selector appended to a composite list is a GLOBAL rule. Registry: `canon/_type-bindings.json`. Corpus: snippets + _proforma (149 files).

| radius | kind | selector | status |
|---:|---|---|---|
| 25 | class | `.btn` | PASS |
| 13 | scoped-element | `.seg button` | PASS |
| 12 | class | `.stateLabel` | PASS |
| 11 | class | `.status` | PASS |
| 9 | class | `.chip` | PASS |
| 7 | scoped-element | `.seg.sm button` | PASS |
| 5 | class | `.spec-h` | PASS |
| 5 | scoped-element | `.search input` | FAIL·escaped |
| 4 | class | `.label` | PASS |
| 3 | class | `.badge` | PASS |
| 3 | class | `.confirm .btn` | PASS |
| 3 | class | `.eyebrow` | PASS |
| 3 | scoped-element | `.seg.md button` | PASS |
| 2 | class | `.avatar` | PASS |
| 2 | class | `.hero .cta` | PASS |
| 2 | class | `.pg .ctrl` | PASS |
| 2 | class | `.qbtn` | PASS |
| 2 | scoped-element | `.pg a` | PASS |
| 1 | class | `.action-bar .btn` | PASS |
| 1 | class | `.loader` | PASS |
| 1 | class | `.sim` | PASS |
| 1 | class | `.tabbar .tabbar__item` | PASS |
| 1 | class | `.time` | PASS |
| 1 | scoped-element | `.nav button` | PASS |
| 1 | scoped-element | `.note.global .actions button` | PASS |
| 1 | scoped-element | `.seg.lg button` | PASS |
| 1 | scoped-element | `nav.main a` | PASS |

## Findings

- ✗ ESCAPED: `.search input` now matches ['Navigations.reference.html'] — outside its acknowledged radius. Namespace it, or `--update` and review the diff.

---
Guard-rail for the T-D9 binding mechanism (T-D12 §5). Waived entries are DEBT to burn down (namespace them) — priority `h2` (25 files) in the non-/1 batch. This gate does NOT reopen T-D9.
