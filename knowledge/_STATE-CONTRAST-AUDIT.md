# State-contrast audit — rendered hover / pressed states (light + dark)
*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**0 text failure(s) across 3 snippet(s).**

**0 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**

**0 CARRIER failure(s) — declarations that carry meaning by colour alone, plus declarations this gate could not READ (s151-D1).**

## Combobox — 🟡 2 declared seat(s) · 2 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 SEAT (declared, advisory) [light/base] div#cb5-msg.cb-msg "Choose a country from th" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div#cb5-msg.cb-msg "Choose a country from th" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Multi-select — 🟡 2 declared seat(s) · 2 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 SEAT (declared, advisory) [light/base] div#ms4-msg.ms-msg "Choose at least one acco" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div#ms4-msg.ms-msg "Choose at least one acco" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

## Tags-input — 🟡 4 declared seat(s)
- 🟡 SEAT (declared, advisory) [light/base] div#ti4-msg.ti-msg "That reference is alread" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [light/base] div#ti5-msg.ti-msg "Remove a reference befor" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div#ti4-msg.ti-msg "That reference is alread" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote
- 🟡 SEAT (declared, advisory) [dark/base] div#ti5-msg.ti-msg "Remove a reference befor" — carriers `symbol label` — no fill reading: the declared seat paints no background of its own (background-color is absent or fully transparent), so it has no fill reading to demote

---
**s151-D1 — THE MEANING-CARRIER VOCABULARY (Dave, #151).** The rule this gate enforces, quoted: "colour alone must not carry meaning" — NOT "every surface must clear 4.5". A composition may declare `data-carries="symbol label"` on the element that seats meaning on a status colour; legal carriers are `symbol`, `label`, `colour`. Three clauses: (a) REDUNDANCY — a declaration naming no carrier other than colour, or a declared seat containing neither a symbol nor a label, is a HARD FAIL reading "state carries meaning by colour alone"; (b) CARRIER LEGIBILITY — the symbol and label keep their normal thresholds (text 4.5, icon 3.0) against THEIR backgrounds and still ❌ if they miss; (c) SEAT DEMOTION — the declared seat's own fill reading is ADVISORY 🟡, never ❌. ⛔ Clause (c) applies ONLY where a valid declaration exists: an UNDECLARED seat behaves exactly as it did before this change, because nothing may pass by silence. An unreadable declaration — empty, or naming a word outside the legal set, or claiming a symbol/label the DOM does not contain — is a NAMED failure, never a default. The count above is RE-READ off this artefact and asserted equal to the carrier lines in the body on every write.
