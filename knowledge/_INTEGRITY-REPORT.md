# Knowledge-base integrity report

> CI gate over the authored canon. **ERROR** = the graph is inconsistent (fix before relying on it); **WARNING** = best-effort / probably fine but worth a look. Regenerate: `python3 knowledge/_build_integrity.py` (exits non-zero on any ERROR).

**Result:** PASS ✅ — 0 errors, 9 warnings. Schema: 76/76 metas valid. Token store: 1008 leaf tokens, groups 41.

## Errors (0)

_No errors — the canon is internally consistent. 🎉_

## Warnings (best-effort) (9)

**Butterfly chart (horizontal)**
- token path may not resolve: 'data/series-1-hc'
- token path may not resolve: 'data/series-3-hc'

**Butterfly chart (vertical)**
- token path may not resolve: 'data/series-1-hc'
- token path may not resolve: 'data/series-3-hc'

**Hero**
- token path may not resolve: 'icon/arrow'
- token path may not resolve: 'padding/arrow'

**Histogram**
- token path may not resolve: 'data/series-1-hc'

**Line chart**
- token path may not resolve: 'text/ticks'

**Modals**
- token path may not resolve: 'overlay/background-blur'
