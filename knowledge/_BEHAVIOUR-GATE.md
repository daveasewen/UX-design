# Behaviour-contract gate (ADR-0015)

Per source ≤16KB (legibility) · per group ≤32KB (page weight) · no polling/network · ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.

- **dataviz/dv-behaviour** — `knowledge/canon/dv-behaviour.js` · 12048 bytes (11.8 KB of 16 KB) · 6 member(s)
- **dataviz/dv-legend** — `knowledge/canon/dv-legend.js` · 17035 bytes (16.6 KB of 16 KB) · 6 member(s)

- **dataviz — page budget:** 29083 bytes (28.4 KB of 32 KB, 89%) across 2 source(s)

## ✗ FAILURES
- dataviz/dv-legend (canon/dv-legend.js): 17035 bytes > 16384 (ADR-0015 size gate)
