# Common Toolkit survey — rigorous pass, tranche 0 (enumeration + deltas)

*2026-07-03, via Figma MCP library search (`search_design_system`) scoped to
**HSBC Common Toolkit (MCP)**. Source of truth per Dave's ruling 2026-07-03: his
"Gaps and edits" branch `Cgbtrmfp15ruNFkIAClpkI` (faithful; prior use was ad hoc).
Library key: `lk-5dab86a0…e66ba`. Branch also subscribes to: Wholesale-Foundations,
CIB-Responsive web, CIB-App — context libraries, NOT in this pass's scope.*

**Completeness boundary (honest):** search is semantic and result-capped (~20/query);
this survey is a high-coverage sample, not a proven-complete census. The create.hsbc
`web/design-toolkits.html` + `app/design-toolkits.html` pages remain the enumeration
skeleton — capture deferred with the channels batch (meter). Treat "not found" as
"not yet found".

## Structure findings

- **S1 — theme pairing confirmed**: component sets ship as `On Light:` / `On Dark:`
  pairs (Button ×4 ranks, Tag, Tag link, Avatar, Divider, Checkbox, Carousel,
  Arrow links, Icon links, Loading indicators, Inline Links…).
- **S2 — THIRD naming register found: `On white:`** (Accordion) — breaks the
  On Light/On Dark convention. Toolkit-side inconsistency, kin of the `(depricate)`
  variable families. → log as toolkit-delta td-001; naming hygiene is exactly what
  our hub-and-spoke binding absorbs (node ID = identity), but the inconsistency
  matters for retrieval and for the reconciliation story.
- **S3 — `00 <Component> guide` doc frames** are components themselves (one per
  family): found 29 so far — Input Field, Tags, Tabs, Table, Badge, Logos, Chips,
  Avatar, Switch, Search, Slider, Tooltip, Reorder, Nav bar, Favicon, Video player,
  App tile, Carousel, View options, Pagination, Global/Inline/Snackbar/Contextual
  notification (×4), Partial modal, Modal non-native, Dropdown native, Dropdown
  (non-native), Icon link, Link-Expander, Progress tracker, Progress indicator,
  Accordion, Header Content, Headers Display, Header Section Titles. These are the
  rule-bearing surfaces for the rigorous pass — the guide frame is the toolkit's
  equivalent of our meta files.
- **S4 — platform splits**: Loading indicator ships per-platform (Web / iOS /
  Android); iOS Nav Bar Top exists; date picker splits input-field vs modal.
  The toolkit encodes platform variance as separate sets, not variants.
- **S5 — breakpoint splits as separate sets**: Hero ×4 (XL / M+L / MS / S+XS),
  Video modal ×3, Search logged-in (S/XS) vs Search without dropdown (all sizes),
  Masthead logged-on (XL/L). Composition-relevant: the toolkit bakes responsive
  behaviour into set enumeration rather than constraints.
- **S6 — status/trend micro-sets** live as bare names (Success, Error, Information,
  Indeterminate ±Thick, Trend Positive, Position Up, No/No Thick, Bullet Diamond,
  Dial) — almost certainly the RAG/indicator family; names are context-poor at
  search level (needs the guide frame to disambiguate). Kin of our Status-indicator.
- **S7 — brand-refresh vintage check**: hexagon components present = Iconic Hexagon,
  Open Hexagon, Cropped Hexagon 1:1. No 3-/4-edge crops surfaced — CONSISTENT with
  hex26-002 (retirement). Logo sets: Masterbrand / Masterbrand-with-identifier /
  Hexagon, each On Light + On Dark — matches logo26 variant-selection rules.

## Inventory (found so far; keys stable, dates cluster 06-18 → 06-23)

| Family | Sets found | Canon (38) equivalent |
|---|---|---|
| Button | primary / secondary / tertiary / **quaternary** / primary **Large** — OL+OD pairs | Button ★ (no quaternary, no Large rank) |
| Links | Inline Links, Arrow links, Icon links fixed-size, Tag link, Link-Expander (guide) | Links (next ★) — external-link variant just ruled in (CA-6) |
| Tag / Chips | Tag OL+OD, Chip toggle ("Pill response") | Tags ★ + Selection-controls chips |
| Notification | **global / inline / contextual / snackbar** (4 taxa) + Alert + form multi-link | Notifications (single component) |
| Dropdown | **native / single-select / filterable / multi-select** (4 taxa) + Pagination dropdown ×2 | Dropdown (single) |
| Modal | New modal, Partial modal, Video modal ×3 breakpoints, Date picker modal | Modals |
| Table | First-row / first-col / row+col header configs | Table |
| Form controls | Checkbox, Radio Button, Switch, Slider (+marker), Date picker input field, Input Field (guide) | Selection-controls, Slider, Input-fields |
| Progress | Progress tracker, Progress indicator (guide), Loading indicator ×3 platforms OL+OD | Progress-tracker, Loading-indicator |
| Navigation | Nav bar (guide), iOS Nav Bar Top, Masthead logged-on, Breadcrumb, Tabs, Pagination | Navigations, Tab-bar, Breadcrumbs, Tabs, Pagination |
| Headers | Header Content, Headers Display, Header Section Titles (3 families) | Headers (deferred revisit) |
| Hero | Hero ×4 breakpoints + hero-image assets ±fixed-height | Hero (deferred revisit) |
| Media | Carousel ±arrows OL+OD, Video player - hero, Image, Video modals | Video-player (no Carousel in canon) |
| Identity | Logos ×3 sets OL+OD, Favicon (guide), hexagons (Iconic/Open/Cropped 1:1) | — (icon/logo assets live outside canon) |
| Status | Success/Error/Information/Indeterminate/Trend/Dial micro-sets | Status-indicator, Countdown-timer(?) |
| Misc | Quick actions, List Item, List Badge, Avatar OL+OD, Divider OL+OD, App tile (guide), Search ×3, Reorder (guide + drop-zone), View options, Accordion (On white), Body, Account Service Guide, Security digital identity | Quick-actions, List-items, Avatar, Divider, Search-field, Reorder, View-options, Accordion |

## Deltas vs canon — the reconciliation frontier

**Toolkit-has / canon-lacks (gap-pattern candidates, in likely value order):**
1. **Carousel** (±arrows, OL+OD) — real component class, canon has none; swipe rules
   aid-010 (ID-16) bind it the day it lands.
2. **Date picker** (input field + modal) — Input-fields supercharge adjacency.
3. **Button quaternary + primary Large** — vocabulary gap in canon's Button ★.
4. **Notification 4-taxa split** — canon's single Notifications vs global/inline/
   contextual/snackbar; affects criteria contracts.
5. **Dropdown 4-taxa split** — same class of gap; canon Dropdown is single-select only.
6. **App tile, Masthead-logged-on** — journey-blocking kin (payments-journey gaps).

**Canon-has / toolkit-lacks (so far):** Account-card (our gap-pattern promotion),
Confirmation, Countdown-timer, Eyebrow, Summary, Action-bar, Tab-bar (islands) —
these are canon inventions; the fixed/flex charter's "inspire from canon+existing,
don't force-fit" rule applies at generation time.

**Toolkit-internal deltas to log (td-…):**
- td-001 — `On white:` register break (S2).
- td-002 — Loading indicator description reads "Day: Progress Indicator" — stale
  "Day/Night" vintage naming inside descriptions (pre-On Light/Dark era). Same on
  Inline Links ("Day: Text Links"), Headers Display ("Day: Headers Display").
  LAYERED VINTAGES inside the toolkit itself — same tell as the framework pages.
- td-003 — guide frames are `component` type (publishable), not annexed docs: they
  travel with the library. Useful: our review pass can screenshot them directly.

## Queue — the rigorous pass (per-family, guide frame first)

Method per family: `get_screenshot` the `00 … guide` → distill rules (IDs `ctk-…`,
destiny tags) → `get_design_context`/`get_variable_defs` on the OL+OD sets → variant/
state census vs canon meta → deltas to `_DS-IMPROVEMENTS.md` (ds-…) or here (td-…) →
xref to component-review program (★ pipeline).

Tranche 1 (aligns with the ★ program — Links next, then Notifications/Tags, Button finish):
1. Links family (Inline/Arrow/Icon/Tag link + Link-Expander guide) — feeds the Links ★
   pass with CA-6 external-link + :visited already ruled in.
2. Notification family (4 guides + Alert) — taxonomy ruling for Dave: adopt the
   4-way split or map onto canon's single Notifications?
3. Tags + Chips (Tags guide, Chips guide, Chip toggle) — Tags ★ adjacency; tab-bar
   islands revisit touches Chip toggle.
4. Button ranks (quaternary + Large) — finish Button ★ with the full rank ladder.

Tranche 2: Dropdown ×4 · Input Field + Date picker · Progress/Loading (platform
policy needed) · Table header configs.
Tranche 3: Headers ×3 + Masthead + Hero ×4 (the deferred revisit pile, now with
toolkit receipts) · Carousel (new class) · status micro-sets (needs guide frames to
name them properly).

## Open questions for Dave

1. Notification/Dropdown taxonomy: reconcile canon to the toolkit's 4-way splits,
   or keep canon's consolidated components with variant coverage? (Affects criteria
   contracts and the compose layer.)
2. Platform-variant policy: canon is web-first; do iOS/Android loading indicators
   and iOS Nav Bar enter the knowledge base as RECORDED (out-of-scope) or queued?
3. Carousel: admit as a new component class (gap-pattern pipeline) or hold?
