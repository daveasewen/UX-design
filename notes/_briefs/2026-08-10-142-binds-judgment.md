# Binds judgment — conductor (Fable), session #142, 2026-08-10

STATUS: PROPOSED — nothing here is ruled until Dave ratifies. Basis tags: CANON (follows a named ruling) ·
PROSE (recovers meta prose intent) · JUDGMENT (best-practice/robustness argument, mine).
Objective per Dave (#142): binds must be robust enough that automatic build proceeds with highest confidence.
Frame: Apollo = "lovable on rails" — the rails are class mechanisms, not per-prop picks. A class-level
ruling is MORE robust than 64 row picks: one mechanism, uniformly enforced, gateable.

Schema note (measured, not assumed): the s141 draft supports ARRAY binds (`proposedBinds` arrays exist on
7 rows) and FAMILY/ramp addresses (accordion.fontSize → `typography.font-size` is a ramp address, not a
leaf). Enum→ramp-map binds are therefore schematically legal.

---

## C1 — `state` enums are SELECTORS, never single-token binds — NO-BIND (class) [JUDGMENT, high]
Rows (16): accordion·avatar·badge·breadcrumbs·button·cards·data-grid·dropdown·headers·icon-button·
input-fields·links·list-items·pagination·quick-actions·reorder·search-field·segmented-control·
selection-controls·status-indicator·tags·video-player·view-options — every `state` row; plus
dropdown.itemState, tabs.tabState (same class).
Why: a state enum (default/hover/disabled…) selects among per-state token SETS; its consequences are
colour-semantic (text/border/background per state) and live in the colour spine (not yet migrated).
Binding `state` → `text.default` (the pick-list head) is a category error — it binds the selector to one
of its consequences. Robust mechanism: per-state maps in the colour layer, authored when the colour spine
migrates. Ruling this class NOW permanently removes the substring-trap picks and unblocks nothing-lost
deferral: verdict recorded as `no-bind:state-selector`, colour-spine lane inherits the per-state map job.

## C2 — `size` enums bind to the icon-scale ramp as MAPS + target.min floor for interactives [PROSE+JUDGMENT, high]
Rows (11): accordion·amount-display·amount-input·avatar·badge·button·countdown-timer·loading-indicator·
segmented-control·stat-card·tags — every `size` row. Also chart-sparkline.scale (same class, MEDIUM —
icon-scale over spacing-gap for consistency).
Why: the icon-scale ramp is the ONLY migrated size ramp and the prose co-mentions icon.* across these
metas — it is de facto the component scale ramp (its name says "icon"; renaming is a separate vocab
question, not a binds question). Map form: small→icon.small … large→icon.large. Interactive components
(button, segmented-control, amount-input, quick-actions class) additionally carry `target.min` as a floor
constraint — that is an accessibility robustness argument (tap target), CANON-adjacent.
Bind: `icon` ramp map; `+ target.min floor` where interactive. Exact addresses grounded per spine file at
build time and parse-verified.

## C3 — `fontSize` binds to the typography ramp [PROSE+CANON, high — already v2-recommended]
Rows (2): accordion.fontSize, links.fontSize → `typography.font-size` (ramp). Follows s141-D1(A) encoding.

## C4 — `status`/`sign` bind to the RAG family as MAPS [PROSE, high]
Rows (4): alert.status, banner.status, toast.status → rag map (success/warning/error/neutral);
amount-display.sign → rag.success|rag.error (positive/negative).
Why: status IS the RAG semantic — the pick-lists came from prose naming exactly the rag set. The addresses
are recommendable now even though rag values live in the unmigrated colour spine: the bind names the
ADDRESS; the colour migration later supplies values. Recording the address now is what makes the colour
lane mechanical instead of a re-decision. (account-card.status is the co-mentioned-set class → C10.)

## C5 — `variant` rows route to the VARIANTS axis — NO-BIND here [CANON s136-D1, high]
Rows (6, the gated set): accordion·avatar·divider·notifications·quick-actions·video-player.
Why: under the three-axis model a variant is not a param bind. This routing is decidable NOW without the
intent-map vocab ruling — vocab decides what the variants axis CALLS them, not whether they are binds.
Verdict `no-bind:variants-axis`. The gate dissolves rather than resolves.

## C6 — `type` rows are also the variants axis — NO-BIND here [JUDGMENT via s136-D1, high]
Rows (12): button·cards·headers·icon-button·input-fields·links·list-items·modals·navigations·
notifications·pagination·slider·tags·view-options `type` (survey candidates: NONE for all).
Why: `type` is structural variance (a different assembly, not a scaled param). Note preserved: button.type
prose names `font-5/medium` — under the variants axis that becomes the variant's typographic parameter,
inscribed so the intent isn't lost. Verdict `no-bind:variants-axis`.

## C7 — `mode` rows are the THEME layer's job — NO-BIND [CANON (four-themes) + s136-D1, high]
Rows (3): links.mode, loading-indicator.mode, tags.mode (pick-list `background.default` is another
consequence-not-selector trap). Four themes are the standing flexibility requirement; a per-component mode
prop duplicates the theme layer and would fork against it. Verdict `no-bind:theme-layer`.

## C8 — `breakpoint` rows bind to the `scale` ramp [CANON s141-D1(B), high]
Rows (3): hero.breakpoint, modals.breakpoint, navigations.breakpoint → `scale` (B1: dimension +
$extensions carries the breakpoint set verbatim). Candidate `breakpoint` rejected — the ruled home is scale.

## C9 — booleans split by consequence [JUDGMENT, high for the no-binds; medium for sticky]
- action-bar.sticky → `elevation.decorative` COMPOSITE (not one scalar of it) — stuck state's visual
  consequence is the shadow; composite bind survives shadow re-tuning. [MEDIUM-HIGH]
- chart-line.highContrast, chart-stacked-area.highContrast → `data.series-high-contrast` (v2 rec stands);
  chart-stacked-area.fillAlpha → `alpha` (opacity primitives, ds-026 amended — CANON). [high]
- accordion.open, dropdown.open — behavioural state, no token consequence → `no-bind:behavioural`.
- headers.image, secure-entry.masked, amount-display.redacted, tabs.overflow — content/behaviour presence
  → `no-bind:behavioural`.
- shimmer (skeleton-loader): prose names an UNMINTED token ("color-mix 50% bone/page") → verdict
  `mint-required` inscribed for the colour lane; binding anything else would erase Dave's recorded intent.

## C10 — geometry: two honest REJECTIONS + radius maps [JUDGMENT, high on rejections]
- drawer.width, skeleton-loader.width → candidates are `border-width.*` — a SUBSTRING TRAP (a drawer's
  width is not a border width). Verdict `none-of-these:candidates-invalid`; real home is a layout
  dimension that doesn't exist yet → authoring item, colour/layout lane.
- segmented-control.shape, skeleton-loader.shape → `border-radius` map (enum values → radius tokens;
  control-class → border-radius.control head). [MEDIUM-HIGH]
- hero.height → no candidates, layout-authoring item. drawer.side, popover.placement, table.orientation,
  chart-bar.orientation, stat-card.direction, table.cellAlign, tooltip.tipAlignment, tabs.track →
  structural/positional params, no token consequence → `no-bind:structural-param`.

## C11 — UNCLASSIFIED rows: classification verdicts [JUDGMENT, high]
NON-VISUAL (binds-irrelevant): dismissible ×3 (alert/banner/popover — composition/slot concern),
toast.duration, time-picker.step, textarea.maxlength, textarea.counter, tab-bar.current.
VISUAL but routed: table.headerType (variants axis), tabs.tabState (C1), tags.background (colour-spine
boolean). Each recorded as a classification verdict, which is exactly what those 16 doubt rows asked for.

## C12 — the 7 co-mentioned-set rows: CONFIRM-SET sittings, arrays shown [no recommendation without data]
account-card.status · account-selector.selected · icon-button.glyph · input-fields.dateCellState ·
selection-controls.control · slider.handleState · stat-card.delta — the draft's proposedBinds arrays must
be displayed verbatim; the ask is "is this set the PROP's or the COMPONENT's". I do not have the arrays in
view and will not guess them. These stay row-level.

## C13 — `surface` enums bind to the surface family as MAPS [PROSE, medium-high] *(added after v3 build found these 3 unmapped)*
Rows (3): avatar.surface, button.surface, divider.surface → surface map (background.default /
surface.raised / surface.subtle / surface.action). Why: unlike `state`, a surface enum selects ONE
surface token directly — a legitimate family-map bind, same mechanism as C4 rag. Avatar's prose carries a
deprecation note ('non-interactive (depricate)/surface/neutral-1') — inscribed, the deprecation is a
colour-lane item, not erased by the bind. Addresses are colour-spine: recorded as address-intent like C4.

## C10 addendum — tooltip.tip *(missed in first pass; v3 flags it OPEN)*
tooltip.tip = the pointer/arrow geometry — structural param like tipAlignment → `no-bind:structural-param`.

## Reconciliation note (v3 build, measured): my "57 of 64 + 7 C12" projection was WRONG — C6/C11 members
are draft-roster rows outside the 64 (type/unclassified rows carried no candidates, so they never entered
the controller), and C12's 7 are likewise draft-roster. v3 reports the measured mapping: 61 of 64
class-mapped + 3 surface (C13) + tooltip.tip; 114 per-row export records across both rosters. The v3 page
is the authority on membership; this file is the authority on verdicts.

---

## Projection
Class-ruled: C1–C11 cover 57 of the 64 controller rows + resolve all 16 classification doubts + dissolve
the 6-row vocab gate. Row-level remaining: the 7 C12 sets. Dave's review load: 11 class ratifications + 7
set confirms. Every class verdict exports per-row so the record stays row-granular.
