# Knowledge-base integrity report

> CI gate over the authored canon. **ERROR** = the graph is inconsistent (fix before relying on it); **WARNING** = best-effort / probably fine but worth a look. Regenerate: `python3 knowledge/_build_integrity.py` (exits non-zero on any ERROR).

**Result:** PASS ✅ — 0 errors, 6 warnings. Schema: 65/65 metas valid. Token store: 918 leaf tokens, groups 36.

## Errors (0)

_No errors — the canon is internally consistent. 🎉_

## Warnings (best-effort) (6)

**Bar chart**
- token path may not resolve: 'data/grid'

**Hero**
- token path may not resolve: 'icon/arrow'
- token path may not resolve: 'padding/arrow'

**Modals**
- token path may not resolve: 'overlay/background-blur'

**Scatter plot**
- token path may not resolve: 'data/axis'
- token path may not resolve: 'data/grid'
