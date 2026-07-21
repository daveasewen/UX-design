# Common Toolkit — Buttons family, rank-ladder pass (Figma-sourced distillation)

*Provenance: Figma file `mI8hvIkV98nquoqWzKh5Kn` "HSBC Common Toolkit (MCP)",
Buttons page `64:90`, captured 2026-07-03 (bridge text extraction, U+2028-safe).
Surfaces: `00 Buttons guide` 63641:9015 (an INSTANCE, 6,289px — the only guide
so far that isn't a component) · Standard frames "Buttons (browser)" 42354:43287
+ "Buttons (mobile app)" 43528:8479 (real create.hsbc text) · sets ×OL/OD:
primary 86:274/641:103685 · secondary 96:357/2261:54613 · tertiary
97:684/2261:55133 · quaternary 211:79907/645:103395 · primary Large
30053:23572/30053:23590. Guide vintage "0.0.0 | May 2023" (td-002 kin). Canon
counterpart button.meta.json ALREADY models all four ranks + size + processing/
success states, so as across tranche 1 the value is the rules layer: rank
semantics, cardinality, width/stacking/placement contracts, the app activity
pattern, and copy. Fourth `ctk*` file — closes the tranche-1 component families;
feeds the finish-Button-★ item.*

## Rank ladder and naming

- **The ladder is FOUR ranks + a size**: primary / secondary / tertiary /
  quaternary, plus `primary Large`. But the naming is split by surface: the
  guide says "Quaternary", the app standard calls the same rank "Undecorated
  buttons", and the BROWSER standard names only THREE ranks (no rank 4 at all).
  The Notifications pass already receipted "undecorated buttons" as the banner
  action style (ctkn-013) — same animal. [RECORDED — td-011; canon's `type`
  enum already carries quaternary; retrieval must know both names] {#ctkb-001}
- **Rank semantics**: PRIMARY — positive actions that progress the journey
  ("Log on", "Register", "Continue", "Done", "Save", "Confirm"), highest
  emphasis, browser: always red with white text. SECONDARY — moderate-to-high
  importance, strongly contrasts with the background; app: "available but not
  used by all programmes" (programme-gated). TERTIARY — "the default style for
  most page buttons", use as many as required; outline only, no fill in default
  AND disabled. QUATERNARY/UNDECORATED — even less emphasis than secondary;
  lives inside established patterns (eg card actions); transparent container;
  never inline within a section of body copy. [ADVISORY — rank-choice heuristics
  + two exact clauses (primary always red/white · tertiary no-fill) for the ★
  pass] {#ctkb-002}
- **Cardinality: only ONE primary and/or ONE secondary button per page; multiple
  tertiary allowed. NEVER primary and secondary in the same button group** (the
  guide adds: secondary "is never used in conjunction with a Primary button
  adjacent"). [ADVISORY — blocking candidate — exact, composition-time
  countable; the single-primary rule is also canon Button doctrine] {#ctkb-003}
- **Buttons vs links boundary**: buttons communicate actions the user can take
  (submit a form, save settings); "for less prominent actions, we use text
  links". [ADVISORY — mirror of ctkl-001's nav-first rule, from the button
  side] {#ctkb-004}

## Width, spacing, stacking, placement

- **Two width modes**: SET widths — column widths or a percentage of
  screen/container, minimum fixed padding either side of the label (app
  DEFAULT); DYNAMIC widths — width from label length, fixed side padding (web
  default and all inline use). Single buttons (app) are generally full width.
  [ADVISORY — layout contract; canon's responsive rules should name which mode
  each context uses] {#ctkb-005}
- **8px between buttons — both stacked and side-by-side — and the primary
  action ALWAYS comes first** (top when stacked, left when side-by-side,
  followed by tertiary/undecorated). [ADVISORY — blocking-capable numerics +
  ordering check, ctkn-009 kin] {#ctkb-006}
- **Stacking and full-width rules differ by platform**: app — stacked buttons
  are ALWAYS full width; web — stacked buttons KEEP dynamic widths, left
  aligned, and full width is used ONLY at the bottom of a form on the mobile
  viewport. [ADVISORY — exact full-width boundary; a render-axis check
  candidate] {#ctkb-007}
- **Placement**: web — left aligned by default; in forms the left alignment
  keeps "a single, straight path down the page, ending with the button". App —
  bottom of the page or dialog. Processes — back left, continue right, giving
  direction; adaptive so the PRIMARY stacks on TOP on small viewports; process
  buttons use dynamic widths. [ADVISORY — composition contracts; the
  straight-path form rule pairs with forms.md] {#ctkb-008}
- **Buttons are always rectangular — never rounded corners.** [ADVISORY —
  blocking candidate — exact; canon builds rectangular; guards the fixed/flex
  vocabulary at generation time] {#ctkb-009}
- **Label centred horizontally + vertically; fixed side padding in BOTH width
  modes; button copy should not wrap — if unavoidable, keep the same padding
  and alignment as single-line.** [ADVISORY — same wrap contract as chips
  (ctkt-026); render-axis testable] {#ctkb-010}

## Icons, activity, copy

- **Icons in buttons: globally recognised only, used SPARINGLY** ("avoid too
  much visual noise with other icons in the top and bottom navigation"); the
  blessed list: add new · delete · print · save · share · refresh · edit ·
  settings · search · calendar. Three structural variations: label, icon-label,
  icon-only. [ADVISORY — icon-source gate kin; the blessed-verb list is a
  vocabulary receipt] {#ctkb-011}
- **The app "button activity" pattern**: when an action needs processing time,
  the button shows a LOADING INDICATOR (colour reverts to default state) → then
  a NOTIFICATION state (button takes the appropriate RAG colour, NO copy
  displayed) → resolution (remain, or return to default, per instance). An
  accessible label MUST accompany the loading spinner and success tick. This is
  the contract behind the primary set's `processing` and `sucess (app)`
  variants. [ADVISORY — state-machine contract for canon's processing/success
  states; the no-copy-in-RAG-state clause is exact] {#ctkb-012}
- **Button copy**: sentence case · as short as possible, NEVER more than five
  words · action verbs (Save, Apply, Send) · precise about the action ("Cancel"
  not "Delete" when cancelling a recurring payment) · "Continue" instead of
  "Next" for multi-step processes · HSBC-preferred terms, never "Find out more"
  / "Click here" · marketing CTAs communicate the value of selecting · no
  jargon. [ADVISORY — ≤5-words + Continue-not-Next + banned-generics are cost-0
  lint candidates; sentence case already blocking; same verb doctrine as
  response/toggle pills (ctkt-028); link-side kin ctkl-022] {#ctkb-013}
- **Accessible name = the visible label** ("buttons always have alt text
  matching the button label") — 2.5.3 Label-in-Name kin. **Target ≥44×44
  including non-decorative buttons, covering the ENTIRE button container.**
  [ADVISORY — aid-009 receipt #6 with coverage clause; the name-matches-label
  rule is AT-testable] {#ctkb-014}
- **Inline-use contradiction**: the guide says quaternary buttons can be used
  "in-line on their own", but the app standard rules that inline buttons should
  "use a tertiary rather than an undecorated button" and bans undecorated
  inline within body copy. If quaternary = undecorated (td-011), these
  conflict. Likely vintage layering (guide May 2023 vs newer standard), but
  which wins shapes the rank-choice heuristic. 📌 DEFERRED (Dave, 2026-07-03):
  REVIEW stays open — probe the create.hsbc button standard at channels
  ingestion for a third source before fixing the heuristic; Button ★ stays
  gated. [REVIEW — Dave to rule after the channels probe: inline buttons =
  tertiary (app-standard reading) or quaternary-alone allowed (guide
  reading)?] {#ctkb-015}
  Edges: conflicts-with(app-inline-button-standard, resolution=deferred, ref=Dave 2026-07-03 — probe create.hsbc at channels ingestion)

## Census and tokens

- **Native focus states prescribed throughout** — canon exceeds with the custom
  ring, same as Links/Notifications/Tags. [RECORDED — ctkl-019 precedent]
  {#ctkb-016}
- **Set census**: primary = Label × Icon × 6 states (default / "hover (web)" /
  pressed / disabled / **"sucess (app)"** ← typo in a shipping variant value,
  td-012 / processing); quaternary = 4 states (no success/processing);
  **primary Large = 3 states only (Default/Hover/Pressed — Capitalised, a
  different register from the lowercase siblings), no disabled, and NO guide or
  standard text mentions the Large size anywhere** (td-013: an undocumented
  shipping set). [RECORDED — census deltas for the ★ pass; canon already
  models size=large and should document what the toolkit doesn't] {#ctkb-017}
- **Token census**: quaternary RIDES the tertiary/* interaction tokens
  (background/hover #f3f3f3 · background/pressed #767676) plus
  `tertiary/text/default (depricate)` #545454 — there is NO quaternary/* token
  family. primary Large binds the primary/background triplet (#db0011 default /
  #ba1110 hover / #000000 pressed) with NO typography variables surfaced on the
  set (type likely hard-styled, worth a look at the ★ pass). [IN FORCE — canon
  button.meta.json tokenValidation already flags the on-dark deprecate load;
  the missing quaternary token family is the one NEW observation → ds-log
  candidate at the ★ pass, not a value error] {#ctkb-018}
- **The guide's "Figma note" instructs authors to fix set-width overflow with a
  manual SOFT RETURN** — the documented source of U+2028 line separators inside
  component labels. Explains both the extraction poison (survey GOTCHAS) and a
  content-hygiene tell: shipped labels may carry hard-coded breaks that will
  not reflow. [RECORDED — provenance for the U+2028 gotcha; content-lint
  candidate at ingestion time] {#ctkb-019}

## Findings

- **F1 — the rank ladder is sourced but its naming is fractured** (ctkb-001,
  td-011): guide "quaternary" = app "undecorated" = absent from the browser
  standard. Canon keeps `quaternary` as the hub name; both aliases recorded for
  retrieval.
- **F2 — one genuine REVIEW** (ctkb-015): inline quaternary (guide) vs
  inline-prefers-tertiary + no-undecorated-in-body-copy (app standard). Vintage
  layering suspected; Dave's ruling shapes the rank-choice heuristic.
- **F3 — the activity pattern closes the census loop** (ctkb-012): processing +
  success variants now have their behavioural contract (spinner → RAG colour
  with NO copy → resolve), plus an AT clause (accessible labels on spinner and
  tick). Canon's processing/success states inherit a real spec.
- **F4 — platform split is sharpest here**: width modes (set vs dynamic),
  stacking (always-full-width vs dynamic-left), placement (bottom vs
  left-in-flow) all fork by platform (ctkb-005/007/008). Canon is web-first
  (Q2 ruling) but the payments-journey work composes forms — the web clauses
  bind now, the app clauses are RECORDED context.
- **F5 — hygiene deltas (appended to survey)**: td-011 quaternary/undecorated/
  absent three-way rank naming · td-012 "sucess (app)" variant-value typo in
  the shipping primary set · td-013 primary Large undocumented + Capitalised
  state register + no disabled state · the Buttons guide is an INSTANCE not a
  component (only family so far) · every guide section header eyebrow reads
  "Primary buttons" regardless of section (template debris) · "to much" typo ·
  the soft-return workaround note (ctkb-019).
- **F6 — 44×44 receipt #6** (ctkb-014), coverage = entire container, plus the
  name-matches-label AT rule — the aid-009 receipt set now spans Links,
  Notifications, Tags, Chips and Buttons: component-level unanimity across the
  toolkit.
