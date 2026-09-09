# Knowledge-base integrity report

> CI gate over the authored canon. **ERROR** = the graph is inconsistent (fix before relying on it); **WARNING** = best-effort / probably fine but worth a look. Regenerate: `python3 knowledge/_build_integrity.py` (exits non-zero on any ERROR).

**Result:** FAIL ❌ — 17 errors, 25 warnings. Schema: 132/137 metas valid. Token store: 1035 leaf tokens, groups 42.

## Errors (17)

**Data grid**
- schema: provenance/source: "gap-report; #261 design pass, Dave's nomination" is not one of ['figma', 'code', 'both', 'gap-report', 'proforma-promot
- schema: relationships: Additional properties are not allowed ('$composes-verbatim', 'composes' were unexpected)
- schema: stateModel: {'$scope': "the COLUMN HEADER (#261); the grid's live/loading/empty modes stay on the `state` prop", 'states': ['rest', 
- schema: with/0: 'selection-controls (the checkbox — CONSUMED byte-identically, not restated; #261 G3)' is not of type 'object'
- schema: with/1: 'filter-toolbar-bar' is not of type 'object'
- schema: with/2: 'pagination' is not of type 'object'
- schema: with/3: 'search-field' is not of type 'object'
- schema: with/4: 'tags' is not of type 'object'

**Filter-toolbar-bar**
- schema: edges: Additional properties are not allowed ('composedOf', 'drivesConsumer', '$contract', 'delegatesTo' were unexpected)
- schema: stateModel: {'attribute': 'data-ftb-state', 'states': [{'name': 'no-filters', 'shows': 'the total count and a `No filters applied` h

**Footer**
- schema: edges: Additional properties are not allowed ('composes' was unexpected)
- schema: provenance/source: 'redesign' is not one of ['figma', 'code', 'both', 'gap-report', 'proforma-promotion']
- schema: variants/3: 'recipe', 'status', 'why' do not match any of the regexes: '^\\$'

**KPI tile**
- schema: stateModel: {'states': ['ready', 'loading', 'empty', 'error', 'stale'], 'loading': 'role=group + aria-busy=true, an sr-only sentence

**Legend**
- schema: provenance/source: 'hand-authored' is not one of ['figma', 'code', 'both', 'gap-report', 'proforma-promotion']
- schema: stateModel: {'rest': 'every series shown; Reset disabled', 'check': "one or more swatches unchecked; the unchecked series ghost at 1
- schema: with/0: 'when' does not match any of the regexes: '^\\$'

## Warnings (best-effort) (25)

**Account card**
- token path may not resolve: 'size/role'

**Back to top**
- token path may not resolve: 'target/--glyph'

**Butterfly chart (horizontal)**
- token path may not resolve: 'data/series-1-hc'
- token path may not resolve: 'data/series-3-hc'

**Butterfly chart (vertical)**
- token path may not resolve: 'data/series-1-hc'
- token path may not resolve: 'data/series-3-hc'

**Eyebrow**
- token path may not resolve: 'size/role'

**Footer**
- token path may not resolve: 'target/floor'
- token path may not resolve: 'text/reverse-secondary'

**Hero**
- token path may not resolve: 'icon/arrow'
- token path may not resolve: 'padding/arrow'

**Hero-variants**
- token path may not resolve: 'rag/success/rag/error'

**Histogram**
- token path may not resolve: 'data/series-1-hc'

**Legend**
- token path may not resolve: 'data/control/swatch-off'

**Line chart**
- token path may not resolve: 'text/ticks'

**Modals**
- token path may not resolve: 'overlay/background-blur'

**Template dashboard (bento)**
- token path may not resolve: 'layout/bento/packing'

**Template settings**
- token path may not resolve: 'background/hover'
- token path may not resolve: 'border/default'
- token path may not resolve: 'border/active'
- token path may not resolve: 'border/disabled'

**Template — create / edit form**
- token path may not resolve: 'background/hover'
- token path may not resolve: 'border/default'
- token path may not resolve: 'border/active'
- token path may not resolve: 'border/disabled'
