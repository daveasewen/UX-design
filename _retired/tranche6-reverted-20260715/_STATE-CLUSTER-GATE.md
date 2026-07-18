# Pro-forma state-cluster gate (DEF-001) — report

Enforces rule 11: `.btn`/`.card-link` bind the canonical `var(--hs)`/`var(--ps)` scale-physics
(via `sizeScale()`), press = `brightness(.85)`; `.ib:active` also holds `brightness(.85)`.
Approved literal `scale()` on `.ib`/`.av`/`.chip-x`/`.pb-action` (constant-px pops) is NOT flagged.

## ✓ _proforma/Tranche-1-interactive.html — PASS
- .btn present: True
- .btn:hover binds var(--hs): True
- .btn:active binds var(--ps) + brightness(.85): True
- .ib:active present: True
- sizeScale() wired (sets --hs and --ps): True

## ✓ _proforma/Tranche-2-interactive.html — PASS
- .btn present: True
- .btn:hover binds var(--hs): True
- .btn:active binds var(--ps) + brightness(.85): True
- .ib:active present: True
- sizeScale() wired (sets --hs and --ps): True

## ✓ _proforma/Tranche-3-interactive.html — PASS
- .btn present: True
- .btn:hover binds var(--hs): True
- .btn:active binds var(--ps) + brightness(.85): True
- .ib:active present: True
- sizeScale() wired (sets --hs and --ps): True

## ✓ _proforma/Tranche-4-interactive.html — PASS
- .btn present: True
- .btn:hover binds var(--hs): True
- .btn:active binds var(--ps) + brightness(.85): True
- .ib:active present: True
- sizeScale() wired (sets --hs and --ps): True

## ✓ _proforma/Tranche-5-interactive.html — PASS
- .btn present: True
- .btn:hover binds var(--hs): True
- .btn:active binds var(--ps) + brightness(.85): True
- .card-link:active binds var(--ps) + brightness(.85): True
- .ib:active present: True
- sizeScale() wired (sets --hs and --ps): True

## ✓ _proforma/Tranche-6-interactive.html — PASS
- .btn present: True
- .btn:hover binds var(--hs): True
- .btn:active binds var(--ps) + brightness(.85): True
- .ib:active present: True
- sizeScale() wired (sets --hs and --ps): True

---
Floor: canonical Button scale-physics only — width-derived var(--hs)/var(--ps) via sizeScale(), press brightness(.85). Bespoke/flat/variant-only hover or a different press-brightness = FAIL (DEF-001).
