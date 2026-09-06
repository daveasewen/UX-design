# Behaviour-contract gate (ADR-0015)

Per source ≤16KB (legibility) · per group ≤32KB (page weight) · no polling/network · ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.

- **dataviz/dv-behaviour** — `knowledge/canon/dv-behaviour.js` · 19768 bytes (19.3 KB of 16 KB) · 15 member(s)
- **dataviz/dv-legend** — `knowledge/canon/dv-legend.js` · 15131 bytes (14.8 KB of 16 KB) · 15 member(s)
- **dataviz/dv-donut-sweep** — `knowledge/canon/dv-donut-sweep.js` · 5511 bytes (5.4 KB of 16 KB) · 15 member(s)

- **dataviz — page budget:** 40410 bytes (39.5 KB of 32 KB, 116%) across 3 source(s)

## ✗ FAILURES
- dataviz/dv-behaviour (canon/dv-behaviour.js): 19768 bytes > 16384 (ADR-0015 size gate)
- dataviz (page budget): 40410 bytes across 3 source(s) > 34816 (ADR-0015 page budget — splitting a source does not buy headroom)
