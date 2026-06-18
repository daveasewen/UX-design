# Token ingestion — gaps & edits log

Running record of issues found while ingesting the HSBC Common Toolkit **"Gaps and edits"** branch (Figma fileKey `Cgbtrmfp15ruNFkIAClpkI`) into the DTCG token store. Each item is for Dave to confirm; nothing is edited in Figma without sign-off.

## Breakpoints, grids and scales (page `471:15986`, web guide `13967:90189`)

1. **Deprecated duplicate border token.** ✅ DONE — Dave deleted `non-interactive (depricate)/border/on-light/neutral-3`. Canon never included it.

### ⚠️ Broader issue: a "host" of `depricate` variables across the file
There are many variables under a misspelled `depricate` namespace, not just the border one. The connector can only see variables bound to a queried node, so it can't list them all. **Bulk fix (Dave):** search "depricate" in Figma's Variables panel and delete the matches. **Claude:** will log every `depricate` variable encountered per Foundations page below as a running hit-list. Canon (the DTCG store) excludes all deprecated aliases by default.

Deprecated variables seen so far:
- `non-interactive (depricate)/border/on-light/neutral-3` (#d7d8d6) — deleted ✅

2. **"Scales applied differently" note.** ✅ EXPLAINED (Dave): this is the type scale — it changes across breakpoints. Not an error. Confirm exact per-scale values on the Font scales page.

3. **Type-size differences across breakpoints/files.** ✅ EXPLAINED (Dave): expected — `scale-1/2/3` are responsive type+space scales, so a step like `font-4` resolves to different px per breakpoint (e.g. 24 vs 19). Reconcile exact values when ingesting Font scales and tokens.

4. **Separate margin token.** ✅ DONE (Dave: yes, may change). `layout.json` now splits `grid.main` and `grid.flyout`, each with separate `gutter` and `margin` per breakpoint. Main margin mirrors gutter (single source value); flyout margins are 0 until Large then 40.

## Font scales and tokens (page frame `46048:7963`)

5. **TScale vs grid-scale breakpoint mismatch.** ✅ DECISION (Dave): the **TScale mapping ending at 1600+ is authoritative** — TScale:1 = 320–959, TScale:2 = 960–1599, TScale:3 = 1600+. The Breakpoints page's "scale (font and space)" column (scale-1 320–759 / scale-2 760–1279 / scale-3 1280+) is the older mapping and should be reconciled to match. **Open edit:** update the Breakpoints page scale ranges to the TScale ranges (or confirm intentional difference).

6. **Per-TScale type sizes were in images.** ✅ RESOLVED via OCR (specimen node 46048:10725). Full 7-size × 3-TScale table now in `typography.json`. The connector's resolved variable mode was TScale:3.

7. **Missing `font-3`/`font-6`/`font-7`.** ✅ RESOLVED via OCR — all seven steps (font-1…font-7) captured. font-N = specimen S-N.

8. **`font-4 = 24` here vs `19` in accordion.** ✅ EXPLAINED — 24 is TScale:3, 19 is TScale:1 (confirmed by the table). Component metadata should reference the type step (e.g. font-5) rather than a fixed px, since px varies by TScale.

9. **New token found: `layout/web/margin = 16px`** (added to `layout.json`), alongside `layout/web/gutter = 40px`.

10. **RAG status colours seen** (for the Colour tokens page): `colour/rag/green #00847f`, `green-tint #e5f2f2`, `red #a8000b`, `red-tint #f9f2f3`; plus `rag/icon/success/container #00847f`, `rag/border/error/default #a8000b`. Will formalise on the Colour tokens page.

## Spacing scale and tokens (page `475:16246`)

Captured into `spacing.json`. Two tables on the page: right-hand **"Space scale (responsive spacing)"** documentation table (space-0…space-12 + space-0.5) and left-hand **variable-mode table** (R0–R12 under "Responsive spacing", columns = `RScale:1/2/3 (pixels)`). Fixed spacing table (F4/F8/F12/F16). `get_variable_defs` returned "nothing selected" for this node — values read via high-res screenshot OCR, not API.

11. **`get_variable_defs` can't read this page via API.** Returned "You currently have nothing selected." Same quirk as before — the connector reads the desktop app's current selection, not the URL node. `get_metadata` also failed here (repeated `net::ERR_HTTP2_PROTOCOL_ERROR`). Worked from screenshots. **If Dave wants variable-verified values, he needs to select the table layer in the Figma desktop app before I call get_variable_defs.**

12. **⚠️ DOC table vs VARIABLE table disagree (the big one).** The right-hand "Space scale" doc table and the left-hand R0–R12 variable-mode table **agree perfectly for space-1…space-8** (all three scales) but diverge at:
    - **space-0:** doc `0/2/4` (micro +2 steps) vs variable `R0 = 0/4/8` (+4 steps).
    - **space-0.5:** exists in doc only (`2/4/6`); **no R0.5 variable** in the variable table.
    - **space-9 scale-3:** doc shows `+4 = 48`, but 40+4 = **44**, and variable `R9 scale-3 = 44`. Doc 48 looks like a typo.
    - **space-10/11/12:** doc continues `40/48/56`, `44/52/60`, `48/56/64`. Variable table **restarts** at R10 under a second sub-header and gives `R10 24/28/32`, `R11 28/32/36`, `R12 32/36/40` — far below the doc values.
    `spacing.json` captures the **doc table** as canonical and flags each divergence with `$review`. **Decision needed (Dave): which table is canonical — the doc "Space scale" or the R-token variable modes?** This is core "gaps and edits" material.

13. **Variable table internal inconsistency.** The second sub-header in the variable table reads "Default / **+8 pixels** / **+16 pixels**", but its rows step by +4 (R10 = 24/28/32, i.e. +4 not +8). Header label contradicts the row values. Flag for Dave.

14. **Both responsive and fixed tables truncate with "…".** Steps beyond space-12 / beyond F16 exist in Figma but aren't shown on the page. If higher steps are needed, capture from the Variables panel.

15. **scale-3 is marketing-only.** Page note "*scale-3" → "Scale-3 is only used for marketing-based websites — check with your design lead." Consistent with layout.json xl breakpoint note. Recorded in spacing.json `$meta`.

16. **Scale-mode → viewport mapping still unreconciled** (carries over from item 5). Spacing uses the same scale-1/2/3 modes; the layout.json mapping (scale-1=[xs,s], scale-2=[ms,m], scale-3=[l,xl]) vs Dave's authoritative TScale mapping (1=320–959, 2=960–1599, 3=1600+) still need to be reconciled into one source.

No new `depricate` variables surfaced on this page (none visible in either table). Hit-list unchanged.

## Colour tokens (page '↳ Colour tokens', canvas `11:116`)

Primitives captured into `colour.json` (126 colours). Semantic layer deferred per Dave.

17. **Semantic light/dark layer DEFERRED (Dave's call).** The intent-token mapping (Name / light / dark — e.g. `text/on-light/default` → light `neutral/grey-8`, dark `neutral/white`) lives in the **'Colour tokens semantic' frame `52780:24956`**, which is **18 pasted screenshots dated 2026-02-27** (node names "Screenshot 2026-02-27 at 10.0x…"), not live variables. Decision: **hold this layer; ingest from live variables, not the stale images.** This is the layer the accordion's `text/default`, `border/subtle`, `tertiary/background/hover` etc. resolve through, and where dark-mode swap logic lives — needed before component token bindings can be fully validated. **Dave to provide live semantic variables (select layer in desktop app, or another export).**

18. **`get_variable_defs` unusable on this page (confirmed images).** Returns "nothing selected" for the canvas and child nodes; the swatch frames and semantic tables are flattened, so OCR is the only path. (Dave flagged this: "some of the tables are just images.") Primitives OCR'd from the live swatch frames at high res — values are reliable.

19. **Spelling: 'complimentary' (sic).** Figma uses `complimentary` instead of `complementary` in BOTH the brand Complementary reds (`brand-hsbc-colour-complimentary-red-1/2/3`) and the Illustration sub-palette (`…-illustration-complimentary-brown/mid-brown/tan/cream-*`). Captured verbatim (token names must match Figma). **Candidate rename for Dave** — but renaming variables is a breaking change; leave as-is unless Dave decides to fix on the branch.

20. **Dark-mode-only primitive families.** `neutral-dark-mode-grey-1..6` (#656565 #474747 #404040 #212121 #1D1D1D #101010) and `rag-dark-{red,amber,green,blue}-tint` (#260005 #221701 #001615 #000D1B) exist as additive primitives. The actual light↔dark substitution is in the deferred semantic layer (item 17).

21. **RAG reconciled (closes item 10).** Confirmed `rag/green #00847F`, `rag/red #A8000B`, `green-tint #E5F2F2`, `red-tint #F9F2F3`; plus newly captured `rag/amber #FFBB33`, `rag/blue #305A85`, `amber-tint #FFF8EA`, `blue-tint #EBEFF4`. The earlier semantic names (`rag/icon/success/container`, `rag/border/error/default`) belong to the deferred semantic layer.

22. **No `depricate` colour variables visible** in the swatch frames. Hit-list unchanged. (Can't rule out deprecated entries hiding in the Variables panel / semantic layer.)

23. **Other primitive frames on the page captured:** Foundation (Core, Complementary, Neutrals, Neutrals dark-mode-only), Data visualisation (blue/purple/pink/orange/green ×4), RAG (+dark), Illustration (blue/green/pink/yellow/orange ×8 + complimentary brown/mid-brown/tan/cream ×8). The hidden `Colours components` frame `12:117` (intent tiles) was NOT captured — it's part of the deferred semantic layer.

## 2026-06-17 — AUTHORITATIVE VARIABLE EXPORT (re-base)

Dave exported the live Figma variables via native **Export modes** (right-click collection → Export modes → DTCG per mode). Files in `_raw/{brand,semantic-color,semantic-scale}/`. This is now the **source of truth**; the OCR-sourced token files were overwritten in place from it (transform script + provenance in each file's `$description`). See memory `token-collection-architecture` and `sutherland-figma-mapping`.

Generated/overwritten:
- `colour.json` ← brand/hsbc (133 primitives, real names color/grey/800 etc; transparent tokens now carry alpha as #RRGGBBAA).
- `semantic-colour.json` (NEW) ← semantic-color light+dark, **111 live tokens** (147 depricate excluded), each with light/dark hex + brand alias ref.
- `typography.json`, `spacing.json`, `layout.json` ← semantic-scale scale-1/2/3 (overwritten). Added `icon-scale.json`, `elevation.json` (NEW).
- `_manifests/depricate-tokens.json` (NEW) — 147 deprecated tokens for Dave's bulk-delete.
- `_manifests/sutherland-diffs.json` (NEW) — Sutherland-vs-HSBC remap worklist (6 brand + 85 semantic diffs).

Threads resolved by the export:
- **item 12 (spacing doc-vs-variable conflict) — RESOLVED.** There is no `space-0..12` variable; real spacing is `gap/*` + `padding/*`. `gap/responsive/content` (4/8/12, 8/12/16…) == the old responsive space scale. The doc "Space scale" and R-token tables were documentation scaffolding. `spacing.json` rebuilt on gap+padding.
- **items 9/12/13/14 (spacing page) — superseded** by gap/padding tokens.
- **item 5/16 (TScale↔scale mapping)** — scale modes are scale-1/2/3 (+scale-1-200 = 200% a11y text-zoom). Authoritative viewport mapping retained in `layout.json` scale block.
- **`depricate` hunt — DONE.** All 147 enumerated in the manifest (no more per-page hit-listing needed). They live in semantic-color under `non-interactive (depricate)`, `interactive (depricate)`, and inline `… (depricate)` leaves.
- **typography — validated**: export font sizes matched the OCR table exactly. Added letter-spacing + weights (thin/bold).

New flags from the export:
- **F1. `font-weight/bold` export glitch**: scale-3 exported as literal `"String value"`. Coerced to `bold` with `$review` in typography.json. Verify in Figma.
- **F2. Naming mismatch doc vs variables**: doc swatches `brand-hsbc-colour-core-hsbc-red` / `neutral-grey-8` vs real variables `color/primary` / `color/grey/800`. Canon uses the real variable names. (Part of the "structure isn't quite right" remap.)
- **F3. 'complimentary' (sic)** confirmed in the actual variable names (`color/complimentary/*`, `color/illustration/complimentary/*`). Still a candidate rename for Dave (breaking).
- **F4. Sutherland modes** (`Sutherland-core`, `Sutherland-light`) captured as a diff manifest, NOT canon — they're the in-progress React remap. Expect them to change.

## 2026-06-17 — depricate deletion safety + replacement map

- **No VARIABLE references the deprecated tokens.** Checked alias targets across light/dark/Sutherland-light: 0 live (or any) variables alias a `depricate` token. So deleting them cannot cascade-break the variable graph.
- **Remaining risk = component-layer bindings**, which the export can't see. If a component layer still binds a `depricate` variable directly, deleting detaches it (keeps last resolved value, loses theming/dark-mode link). The alphabetical component-ingest pass doubles as the usage audit (each component read via get_variable_defs reveals its bound tokens) — flag any depricate binding before deletion.
- **`_manifests/depricate-replacement-map.json` (+ .txt)** — contingency rebind map. Summary: 23 confident (9 medium + 14 medium-group; all `rag/surface`+`rag/border` → `rag/error|warning|success|information`), 48 low (multiple value candidates listed), 76 review (no live equivalent → just delete). Caveat: some cross-group value matches are colour coincidences (e.g. any #000000), not semantic — only same-group/rag picks are trustworthy without review.

## 2026-06-17 — Foundations: Dark mode page (node 46025:22918)

GUIDANCE-ONLY page — **no new tokens**. Consumes existing tokens (colour/rag/*, typography/*, gap/*). Dark-mode token VALUES already captured in `semantic-colour.json` (dark) + `neutral-dark-mode`/`rag-dark` primitives. Prose captured to `knowledge/guidelines/dark-mode.md` (via get_design_context text extraction; note get_design_context errors on image-heavy nodes >context limit — recovered do/don't captions by ripgrep -o on the saved tool-result files). Key rules: not a straight inversion; desaturate; maintain 3:1 contrast; in dark mode make HIGHER elevation levels LIGHTER (reverse of light mode). Confirms external guidance base URL: **create.hsbc/Guidelines/Foundations/**.

## 2026-06-17 — Foundations: Icons page (node 2107:29115)

No new tokens (sizes in icon-scale.json, colours in semantic-colour.json icon/*). Usage guidance → `knowledge/guidelines/icons.md`. Icon SVG catalogue export pipeline in `knowledge/assets/icons/` (pilot done; full run blocked on Dave's token — see project memory).

**⚠️ Sourcing rule (flag):** HSBC guidance says **do NOT export SVGs from the Icon Library/artwork files for development — use the UI Centre**. Our Figma export is therefore PROTOTYPE-ONLY; dev handoff icons must come from the UI Centre. Recorded in icons.md.

Other findings: default state = line icons, active state = solid fill (not all icons have active; manifest flags `active`). Thicker-weight variants = 1.8px line on the 18×18 grid for small sizes (chevrons, some state icons). create.hsbc = most up-to-date icon source.

## 2026-06-17 — Foundations: Elevation page (node 873:34991)

No new tokens (values in elevation.json: decorative blur 8 / functional blur 16). Guidance → `knowledge/guidelines/elevation.md`. Sections: Types (decorative vs functional), Usage (do/don'ts — don't mix both types on one element; don't use shadows for pure decoration), Behaviour (level system; triggered on appearance / on scroll; conditional scroll shadow). Dark mode reverses (higher = lighter), cross-refs dark-mode.md. (2 of 4 do/don't captions not transcribed — image-heavy nodes; node ids logged in elevation.md.)

## 2026-06-17 — Components pass (depricate usage audit alongside)

Each component ingested via get_variable_defs doubles as the deprecated-token usage check.

- **Badge** (node 617:78931) → `knowledge/components/badge.meta.json`. Tokens: surface=`color/primary` (primitive, not semantic — flagged), number text=`text/reverse` (medium weight), disabled=`icon/disabled`. **⚠️ DEPRICATE-IN-USE (first hit):** the `.Badge on icon` set (2450:109105) binds `interactive (depricate)/on-light/surface/primary/default` (#FFFFFF). Recommended rebind: `background/default`. **Must rebind before the depricate bulk-delete** or the white surround detaches. Annotated in `_manifests/depricate-replacement-map.json` ($usage_audit). `specs/*` (specs-component-stroke #7B61FF etc.) are Figma annotation scaffolding, excluded.

- **Avatar** (node 2136:31172 light / 2136:31221 dark) → `knowledge/components/avatar.meta.json`. Variants initials/image/icon × small/med/large (36/44/56) × default/disabled × on-light/on-dark. Live tokens: text/default, text/disabled, icon/default, icon/disabled, text/reverse, icon/default-reverse, image/opacity/default(=1)+disabled(=0.2). **⚠️ 6 DEPRICATE-IN-USE, NONE with a live equivalent (all replacement-map confidence=review):** non-interactive surface/neutral-1 + black, border/on-light/neutral-2 + neutral-6, text/on-dark/disabled, icon/on-dark/disabled. **BLOCKER: these cannot be auto-rebound — the live semantic layer is missing a subtle surface + border family (and on-dark disabled text/icon). Do NOT bulk-delete these until live equivalents exist and Avatar is rebound.** Escalate to Dave / Sutherland remap. Annotated in replacement-map $usage_audit. NEW confirmation: `image/opacity/*` tokens live in semantic-colour.json (not a gap).

- **Breadcrumbs** (node 41590:108466) → `knowledge/components/breadcrumbs.meta.json`. States: default / hover-pressed (combined) / no-link. **No depricate tokens (clean).** All states bind `text/default` (#333333) at font-6 regular — NO colour differentiation between states; relies on link styling (underline). WCAG flags: hover & pressed combined into one state, and no colour change between states (non-colour cue required). Separator = a "/" text character (text/default, font-6), not an icon (confirmed by Dave).

- **Button** (node 64:90) → `knowledge/components/button.meta.json`. 4 types (primary/secondary/tertiary/quaternary) × on-light/on-dark × default+Large, states default/hover/pressed/disabled (+processing/success on primary). **On-light MOSTLY MIGRATED** (live primary/secondary/tertiary background/* + border + text/icon); minor depricate: `interactive (depricate)/on-light/surface/brand-1/default` (primary→primary/background/default, same value) and `tertiary/text/default (depricate)` (tertiary+quaternary, #545454→text/default #333333, value change). **⚠️ ON-DARK HEAVILY DEPRECATED (biggest cluster yet):** on-dark primary (641:103685) binds `interactive (depricate)/on-dark/surface/brand-1/{default,hover,pressed,disabled,processing}` + on-dark/on-light depricate text/icon + rag(depricate)/success; only text/reverse + icon/default-reverse live. **Migration: live primary/background/*, text/reverse, rag/success are MODE-AWARE → rebind on-dark to the SAME semantic tokens as on-light (don't keep separate on-dark surface tokens).** secondary = clean. Annotated in replacement-map $usage_audit + $button_on_dark_note.

- **Cards** (node 2298:53278) → `knowledge/components/cards.meta.json` (family of 5: actions, basic, basic-non-interactive, image-with-border, image-without-border). **4 of 5 clean.** Only **Card Basic** (interactive) carries a depricate: `tertiary/text/default (depricate)` (#545454→text/default) — the recurring one (also Button tertiary/quaternary). Pattern: INTERACTIVE cards use `tertiary/background/{default,hover,pressed}` for state tints (+pressed flips text/icon to reverse); STATIC/image cards use `background/default` + `border/subtle` and are clean. Common: border/subtle, border-width/small, padding/responsive+fixed/medium(16)+large(20), color/primary arrow, icon/arrow+padding/arrow chevron, headline=font-3 on image cards. (Card Image without border not separately queried — expected clean.)

- **Countdown timer** (node 277:9284) → `knowledge/components/countdown-timer.meta.json`. Styles inline/stacked/undecorated × small/med/large + circular graphic indicator (60s/40s/10s/0s depletion). **No depricate (fully migrated, clean).** Uses dedicated `timer/background` (#D7D8D6 track) + `timer/foreground` (#000000 fill) + text/default + font-5. Ring colour does not escalate by time (no RAG).

- **Divider** (node 2120:30972) → `knowledge/components/divider.meta.json`. Variants subsection/subsection-inset/section (1px) + break (4px), on-light/on-dark. On-light CLEAN (`divider/border/{subsection,subsectionInset,section,break}`). **On-dark uses 2 depricate** `non-interactive (depricate)/border/on-light/neutral-3` (#d7d8d6) + `neutral-6` (#767676) → rebind to the mode-aware `divider/border/*` (same fix-pattern as Button on-dark; divider/border/* carry dark values). inset = padding/responsive/medium. Confirms on-dark debt pattern + that the divider case of those border-neutral depricates HAS a live home (divider/border/*), unlike Avatar's generic surfaces.

- **Dropdown** (node 45024:56778) → `knowledge/components/dropdown.meta.json`. Two families: non-native (single-select, filterable, multi-select + list items) and native; states default/hover/active/completed/disabled/error × open. First FORM component → surfaces live `form/*` (field bg/border), `scrollbar/*`, `elevation/functional` (menu shadow), divider/*, rag/error. **Depricate-heavy on the triggers, esp. NATIVE (less migrated):** 9 distinct interactive(depricate) surface/border + icon/on-light(depricate)/hover + rag/border(depricate)/error + non-interactive surface-1/6. **Most have clean form/* rebinds** (border/active→form/border/active, high-contrast→form/border/default, low-contrast/disabled→form/border/disabled, surface/primary/hover→form/background/hover, icon hover→icon/default, rag/border error→rag/error). Migration = move triggers (esp. native) onto the form/* family. List items clean. Annotated in replacement-map $usage_audit.

- **Forms** (node 45226:146957) → `knowledge/guidelines/forms.md`. Umbrella forms GUIDANCE (4 frames; main guide ~15,000px, 14 sections), no bound tokens. Captured: purpose + 4 design principles (readability>aesthetics; only ask what you need; guide people; design for the format) + full 14-section outline (Design principles, How to design an HSBC form, Usage, Structure, Input controls, Label alignment, Field sets, Contextual help, Actions, Placement, Multi-step processes, Confirmation, Behaviour, Copy guidance). Per-section deep prose extractable on demand from node 45226:149920.

- **Headers** (node 2298:118794) → `knowledge/components/headers.meta.json`. App-only family of 3: Header Content (action Button/Close/None — CLEAN, font-4 title + font-5 button + icon/default), Header Section Titles (index/amount, font-6/medium — 1 depricate non-interactive/surface/neutral-2 #ededed, no live subtle-surface), Headers Display (default/processing × image, font-1 — 2 depricate: surface/white→background/default, border/on-light/neutral-2→divider/border/subsection). Annotated replacement-map $usage_audit.

- **Hero** (node 41362:3440) → `knowledge/components/hero.meta.json`. Large responsive marketing banner: breakpoints XL/M+L/MS/S+XS, fixed/full height, primary message (bg solid/transparent/none × text dark/light) + secondary message (image/video × bg × text), corner variant, image/video assets. **NEW live token group `blur/*`** (background blur for glass message panels; radius blur/background-surface=12) — first component to use it. Depricate (clean rebinds): surface/white→background/default, surface/transparent/white→color/grey/transparent/white-75 (identical), transparent/black→black-85, border/on-light/neutral-3→border/subtle, on-dark/surface/brand-1→primary/background/default. **NEW finding: a SECOND legacy namespace beyond 'depricate'** — `Non-interactive/Content/On Light/colour-content-primary` (#333333→text/default); logged $legacy_namespace_note. Solid bg = primary/background/default (#DB0011); glass = transparent primitive + blur/surface.

- **Input fields** (node 45011:112934) → `knowledge/components/input-fields.meta.json`. Family: single-line (+ Large), multi-line, date-picker (input + `.Date` calendar cells + `.Arrow` nav + modal/dropdown overlay), input label. States default/hover/active/completed/disabled/error. **Migrated to `form/*`**: bg transparent `#ffffff00` / hover `#f3f3f3` / pressed `#767676`; border default `#767676` / active `#000000` / disabled `#d7d8d6`. Text `text/default` (font-5 medium value / light placeholder), helper+error font-7. `icon/default`+`icon/disabled`, error `rag/error`. Date-picker overlay adds `elevation/functional` + `background/default` + `divider/border/subsection`. **`.Date` cell (512:17414) fully clean.** **2 deprecated EFFECT colours** (same as Dropdown — "bottom stroke" inner-shadows): `interactive (depricate)/on-light/border/active/default` (#000000 → `form/border/active`) + `rag/border (depricate)/error/default` (#A8000B → `rag/error`) — both clean value-identical rebinds. Audited 2298:166741, 818:123202, 512:17414; not individually queried: Large, Multi-line, Input label (expected same / label clean). All 15 live refs resolve — PASS. Annotated replacement-map $usage_audit.

- **Links** (node 45015:45858, page "Text links (browser)") → `knowledge/components/links.meta.json`. Family of 4: **Arrow link** (chevron after text, font-1…7, multiline; arrow icon = PRIMITIVE `color/primary` #db0011 on light / `icon/default-reverse` on dark; text/default|reverse; font-N/regular-link + 5/6/7 medium-link + icon/arrow/font-N + padding/arrow/font-N — CLEAN), **Back link** (chevron before text, font-5/6/7; back arrow NEUTRAL `icon/default` not red — CLEAN), **Icon link** (leading icon, S5/6/7, only type with explicit disabled), **Inline link** (in body copy, font-5 **light**-link weight 350 — CLEAN). States: hover+pressed combined (as Breadcrumbs). **Depricate-in-use = 4, ALL on Icon link ON-DARK:** icon/text `on-dark (depricate)/hover` #fff → icon/default-reverse / text/reverse (clean); icon/text `on-dark (depricate)/disabled` #767676 → **REVIEW no live equiv**. **KEY: the on-dark disabled blocker (#767676), previously Avatar-ONLY, is now also Icon link → no longer an edge case; a live on-dark disabled text/icon token is needed before deleting these.** On-light disabled already migrated (icon/disabled+text/disabled). Primitive-binding flag: arrow uses color/primary directly (like Badge/Hero) — consider semantic icon/brand. All 9 live refs resolve — PASS. Annotated replacement-map $usage_audit. Do/don't: chevron must stay attached to last word (never own line); back/icon glyph aligns to first line, not vertically centred; don't overload page with links.

- **List items** (node 45129:305498, page "Lists") → `knowledge/components/list-items.meta.json`. Big family: 6 tappable row types (Account, Badge, Item, Review, Review Detail, Transaction) + typeset bullet/ordered/custom lists. Rows share states default/hover(web)/pressed/disabled/processing × visual icon/avatar/image; Transaction adds detail tag/status (rag/success+tint). **MAJOR FINDING: two row-surface conventions coexist, value-identical** — LIVE `tertiary/background/default|hover|pressed|disabled` (#fff/#f3f3f3/#767676/#fff: Account, Review, Review Detail) vs DEPRECATED `interactive (depricate)/on-light/surface/primary/*` (same values: Item, Badge, Transaction). So migration = rebind surface/primary/* → tertiary/background/* (clean). **Per-type depricate:** account/review-detail/bullets = clean; review = 1 (pressed surface, clean); badge ≈7; item ≈12 (incl on-dark blockers); transaction ≈8. Clean rebinds also: text/icon on-light(depricate)/hover → text/default,icon/default; text/icon on-dark(depricate)/pressed → text/reverse,icon/default-reverse; tertiary/text/default(depricate) #545454 → text/default (value change). **No-equiv blockers (same gap family as Avatar/Headers):** non-interactive surface/neutral-1+2 (#f3f3f3/#ededed), border/on-light/neutral-2 (#ededed → divider/border/subsection?), surface/black (#000, Item on-dark) + border/on-light/neutral-6 (#767676, Item on-dark = Avatar blocker). Primitive leaks: Badge color/primary #db0011, bullets colour/neutral/grey-1. All 18 live refs resolve — PASS. Annotated replacement-map $usage_audit. Bullets guidance: bullets/numbers use SAME font/colour as text (no decorative shapes/colours); lead-in ends with colon, items completing it not capitalised + no end punctuation; ordered lists never complete a lead-in.

_Add subsequent pages below as they are ingested._
