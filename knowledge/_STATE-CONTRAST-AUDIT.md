# State-contrast audit — rendered hover / pressed states (light + dark)
*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**0 text failure(s) across 2 snippet(s).**

**0 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**

**0 CARRIER failure(s) — declarations that carry meaning by colour alone, plus declarations this gate could not READ (s151-D1).**

## Footer — ✅ clean

## Footer-doormat-lockup — ✅ clean

---
**s151-D1 — THE MEANING-CARRIER VOCABULARY (Dave, #151).** The rule this gate enforces, quoted: "colour alone must not carry meaning" — NOT "every surface must clear 4.5". A composition may declare `data-carries="symbol label"` on the element that seats meaning on a status colour; legal carriers are `symbol`, `label`, `colour`. Three clauses: (a) REDUNDANCY — a declaration naming no carrier other than colour, or a declared seat containing neither a symbol nor a label, is a HARD FAIL reading "state carries meaning by colour alone"; (b) CARRIER LEGIBILITY — the symbol and label keep their normal thresholds (text 4.5, icon 3.0) against THEIR backgrounds and still ❌ if they miss; (c) SEAT DEMOTION — the declared seat's own fill reading is ADVISORY 🟡, never ❌. ⛔ Clause (c) applies ONLY where a valid declaration exists: an UNDECLARED seat behaves exactly as it did before this change, because nothing may pass by silence. An unreadable declaration — empty, or naming a word outside the legal set, or claiming a symbol/label the DOM does not contain — is a NAMED failure, never a default. The count above is RE-READ off this artefact and asserted equal to the carrier lines in the body on every write.
