# RAG Roundel Matrix — brief (2026-08-08, s134, Lane D)

Deliverable: `reviews/RAG-ROUNDEL-MATRIX-2026-08-08-s134-v1.html` — self-contained, no iframes/deps.
Icon+enclosure only (no copy). Grid: 4 theme rows (Mono, Legacy, Console, Supercharge) × light/dark
columns, each cell the four marks (error, warning, success, information) at real size on that theme's
surface. Under each roundel: shape/mark hex pair + computed WCAG contrast for mark-on-shape and
shape-on-surface, plus a DECLARED/FALL-THROUGH tag.

## Sources, per theme

**Mono** (base, `knowledge/tokens/semantic-colour.json`)
- error fill `#F6604C` :461-471 · warning `#E0A61F` :483-493 · success `#66CC8D` :505-515 ·
  info `#78A7E8` :527-537 — all mode-invariant (s122-D2).
- marks: all four = `#1A1A1A`, per the canon `--mark-*` block quoted in `Alert.reference.html:70-73`
  (s122-D2 ruling receipts).
- surface: `#FFFFFF` / `#1A1A1A` — the canonical mono ground referenced throughout the store; no
  single "page" token was found by that name, so this is the value used everywhere else in the repo
  for mono light/dark ground, not a literal `page/default` lookup.

**Legacy** (`knowledge/tokens/themes/apollo-legacy.overrides.json`)
- error `#A8000B` (~L106) · warning `#FFBB33` (~L128) · success `#00847F` (~L62) ·
  info `#305A85` (~L161) — these are Dave's own Figma values, ruled s131-D1, confirmed present
  verbatim in the file.
- marks block (~L349-392): error/success/info = `#FFFFFF`, warning = `#000000` (amber carve-out,
  always-black text/mark rule).
- surface: file declares NO page/surface override → renders the Mono ground by fall-through.
  Labelled FALL-THROUGH in the matrix.

**Console** (`knowledge/tokens/themes/apollo-console.overrides.json`)
- error `#B92F1E` :8-17 · warning `#D5990B` :40-49 · success `#5DAC7B` :73-82 ·
  info `#5A85C1` :106-115 (re-hued from `#4F77B0` at s132-D1 — info mark flipped white→ink at the
  same ruling, making error the sole white mark on Console/Supercharge).
- marks (:196-239): error white, warning black, success/info `#1A1A1A`.
- surface: file's own `$description` states shape (radius) is the only live divergence and
  "everything absent here falls back to Mono" — no surface override present. FALL-THROUGH.

**Supercharge** (`knowledge/tokens/themes/apollo-supercharge.overrides.json`)
- error/warning/success/info + marks: byte-identical block to Console, declared independently in
  this file (:8-115 fills, :294-334 marks) — not inherited, genuinely re-declared per Dave's
  "Console + Supercharge share ONE RAG map" ruling (s122-D3). Tagged DECLARED.
- surface: **approximated**, not a literal page-token hit. No `page/default` key exists for SC;
  used `color/warm/15` (`#F7F6F4`, light) and `color/warm/2` (`#13110E`, dark — the ADR-0014 SC ink
  anchor) from `knowledge/tokens/colour.json:292+`, per that override file's own description
  ("page ... follow by step index"). Flagged in the HTML cell note — if a dedicated SC page override
  exists elsewhere it should replace this approximation.

## Fall-through cells
Legacy light/dark surface, Console light/dark surface — 4 of 8 surface cells. All 16 mark/fill
value-cells (4 statuses × 4 themes) are DECLARED; none of the icon colours themselves fall through.

## Not done / out of scope per DO-NOT-RULE
No token or snippet file edited. No values invented for undeclared cells — SC surface is flagged as
an approximation from a declared ramp, not a page token, rather than presented as authoritative.
