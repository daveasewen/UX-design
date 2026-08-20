# Receipt — #210 Wave 5 · Lane A · the three app shells

**Lane:** A (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave5-layer2-p2-fanout-brief-v1.md` (THE JOB, Lane A)
**Members:** App-shell-top-nav (row 97, P2) · App-shell-side-nav (row 98, P2) · App-shell-multi-column (row 99, P2)
**Store row:** see § 8 — minted at creation per [[forgotten-document-class]]

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every shell decision below is PROPOSED and is
> Dave's. No registry, `MIGRATED_SNIPPETS`, `CATEGORIES`, `component-types.json`, `canon.css`,
> `_rulings.json`, showroom or git operation was touched — this lane created **NEW FILES ONLY**.

---

## 0 · THE HEADLINE: THE GATES WERE GREEN OVER SIX REAL DEFECTS, AND A BROWSER FOUND ALL SIX

Every gate this repo owns passed over the three shells at a point when they contained **six
defects, two of them serious**. Not one gate could see any of them. They were found by driving a
real browser and by *looking at the picture*, in that order, and every one is repaired and
re-measured below.

| # | defect | how it was found | why no gate saw it |
|---|---|---|---|
| 1 | **The modal drawer opened with no keyboard entry point.** `document.activeElement` stayed on `<body>`; Escape then reached nothing, so the sheet could not be closed by keyboard at all. | driven | The Tab *order* was already correct, and the markup carried every required ARIA attribute. Gates read attributes; this is a runtime sequencing fault. |
| 2 | **The hamburger rendered beside a fully visible primary nav at every width.** | LOOKED AT | `.sh-menu{display:none}` was silently overridden by `.sh-close{display:inline-flex}` — same specificity, declared later, button carries both classes. No gate resolves the cascade. |
| 3 | **The footer's legal links rendered on top of one another** at narrow width — link tops 10.5px apart inside 44px boxes. | LOOKED AT, then measured | An `inline-flex` child's `min-height` does not grow its `<li>`'s line box. Nothing in the markup is wrong. |
| 4 | **The breadcrumb trail opened with an orphan "/"** once ancestors were dropped at phone width. | LOOKED AT | Each separator lives inside the `li` it precedes. A markup-shape consequence, invisible to every checker. |
| 5 | **Breadcrumb links were 10.1px tall** — under the repo's own 44px `target/min` and under WCAG 2.5.8's 24px floor. | measured | **No gate reads `target/min` for hit area.** Inherited from the gated `Breadcrumbs`, which has no hit-area rule at all. |
| 6 | **ds-005: every nav label clipped 4.00px of its descenders.** | LOOKED AT, then measured against a control | `_validate_descender_clip.py` reads the **declaration**, not the computed value. It is green over a label whose override loses the cascade. A gate blind to the thing it is named after. |

★★ **Defect 1 is the one worth carrying forward**, because its cause is not obvious and it will
recur in every dialog anyone composes. Two independent things had to be sequenced correctly:

- **(a)** `visibility` is *transitioned* on the sheet, so it computes `hidden` for **two more
  frames** after `.open` lands, and `focus()` on a hidden element is a silent no-op. Measured
  time series on the real file: `t0 hidden · rAF1 hidden · rAF2 visible`. **A forced reflow
  (`void offsetWidth`) does NOT help** — the before-change style is still `hidden`.
- **(b)** Setting the background `inert` **blurs whatever holds focus** — the trigger the user
  just pressed — and that blur lands asynchronously, wiping an earlier `focus()`.

The correct order, now in both files with the reasoning inline:
**1** show the sheet · **2** wait two frames · **3** move focus in · **4** *only then* set inert.
This is [[mutation-tests-the-clause-not-the-feature]] and the write-side twin of
[[settle-the-transition-before-you-read]]: **you must settle the transition before you ACT on it,
not only before you read it.**

⚠ **Defect 6 is a THIRD catch of ds-005 in this wave, not a new finding.** `W-74`'s own body
already records it: *"ds-005 trim-block specificity beats single-class overrides (6/6 sampled
gated snippets compute cap alphabetic today, twice-caught same wave)"*. This lane is the third,
and it is the first to carry a **repair plus a control** (§ 3, claim 14). The cross-lane decision
named in `W-74` is still Dave's; nothing here settles it.

---

## 1 · FILE LIST — six new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/App-shell-top-nav.reference.html` | 49,404 |
| 2 | `knowledge/components/app-shell-top-nav.meta.json` | 20,963 |
| 3 | `knowledge/snippets/App-shell-side-nav.reference.html` | 58,825 |
| 4 | `knowledge/components/app-shell-side-nav.meta.json` | 19,817 |
| 5 | `knowledge/snippets/App-shell-multi-column.reference.html` | 47,794 |
| 6 | `knowledge/components/app-shell-multi-column.meta.json` | 20,876 |
| 7 | `notes/_receipts/2026-08-20-210-wave5-laneA-app-shells.md` | this file |

**No existing file was edited. Not one.** Renders live OUTSIDE the repo
(`(NON-REPO: the session outputs folder, laneA-renders/*.png)` per `s191-D2`) — 18 layout PNGs
(3 shells × 3 widths × light/dark), 3 behaviour PNGs, 2 high-DPI label crops. Working artefacts,
not deliverables.

---

## 2 · THE ARTEFACT-CLASS CONVENTION EARNED ITSELF, AND THAT IS A MEASURED CLAIM

The brief PROPOSED that Layer-2 rows ship in the library grammar (`snippets/` + `components/`)
so *"the one grammar keeps every existing gate watching these files for free"*. **That paid
during this build, not in theory:** `_validate_descender_clip.py` caught a genuine truncating
label with no override — the record title in the multi-column detail header, which would clip
the tail of a *g/y/p/q* in an account name — purely because the file sat where the gate looks.
A shell shipped in a parallel pipeline would have been born ungated and that defect would have
shipped. **Recorded as evidence FOR the convention; the convention itself is still Dave's.**

⚠ **And the same placement produced a schema finding the brief could not have known:** the
brief's proposed `"layer": "2 Shell"` key **would fail probe P-1**. `meta.schema.json` sets
`additionalProperties:false` with `patternProperties {"^\\$": {}}` and has no `layer` property.
All three metas therefore carry **`$layer`**, the legal form, and say so on their own face.
A second, sharper one: **`relationships` permits only four keys and has NO `^\$` escape** — a
`consumes` key *or even a `$note`* inside it is a violation. Found by driving P-1, not by
reading. The legal home is a top-level `$consumes`.

`category` is `"template"` on all three — the closest **legal** enum value. There is no `shell`
value and inventing one fails the gate. **Declared as a compromise, not presented as correct.**

---

## 3 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | Snippet gate clean with all three present | `python3 knowledge/_validate_snippets.py` → *"snippet gate: 119 snippet(s), 0 failure(s)"* | ✅ |
| 2 | 4px-grid gate clean | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS — all layout dimensions on the 4px grid (135 file(s))"* | ✅ |
| 3 | a11y gate: zero failures | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 119 snippet(s), 0 failure(s), 249 warning(s)"* | ✅ |
| 4 | Descender-clip gate passes — **after a real catch** | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS … (135 file(s))"*. It first FAILED on `.sh-detail-head h1`; the repair is `text-box-edge:text text` on the two-part selector. | ✅ **caught something** |
| 5 | ⛔ **Type-composite debt did NOT grow. The three files add ZERO** | `python3 knowledge/_validate_type_composites.py \| grep -c "App-shell"` → **0**, and the total reads *"1097 violation(s)"* — **exactly the `#203` measured baseline**. ⚠ A mid-build reading of 1118 was **NOT mine**: it was a sibling lane's transient state, confirmed by the same grep returning 0 for my files at that moment. Attribute by grep, never by the total. | ✅ |
| 6 | Metas are schema-valid | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"114 meta(s) checked · 0 finding(s)"* → *"PROBE P-1 — findings=0"* | ✅ |
| 7 | ★ **Every hex in every theme block is the STORE's value, not a typed one** | `python3 knowledge/gen_snippet_tokens.py --check` → *"4007 manifest bindings across 119 snippets … **0 value(s) would change**"*. This is stronger than "the gate passes": the generator that projects tokens into theme blocks reports it would change nothing, so no value was hand-typed and drifted. | ✅ |
| 8 | ⛔ **binds-resolve check D FAILS for all three — DECLARED, not hidden** | `python3 knowledge/_validate_binds_resolve.py` → *"108/119 canon blocks · 11 failure(s)"*, naming `.cn-app-shell-top-nav`, `.cn-app-shell-side-nav`, `.cn-app-shell-multi-column` (+ 8 sibling-lane files) | ⛔ **CONDUCTOR'S** |
| 9 | The real HSBC cut rendered — **asserted with two controls, not a boolean** | canvas `measureText('Handgloves 12345')` at 40px: `HSBC_MtUnivers_Latin` **346.88** · `"Univers Next HSBC"` **346.88** · `"Univers Next for HSBC"` **346.88** · `DejaVu Sans` **375.39** · nonexistent face **301.07**. Both aliases land on the target and on neither control. | ✅ **DRIVEN** |
| 10 | Zero horizontal overflow, every shell, every width, both modes | `documentElement.scrollWidth − clientWidth` = **0** at 1400/900/420 × light/dark, all three files (18 readings) | ✅ **DRIVEN** |
| 11 | The collapse is real and it is the CONTAINER's, not the viewport's | Each file carries a **392px container** specimen. At a **1400px viewport** it is fully collapsed while its siblings at 1352px are not — top-nav menu `display:"flex"` vs `"none"`; side-nav column width `0` vs `248`; multi-column list `false` vs `[360,582]`. | ✅ **DRIVEN** |
| 12 | The three-band side-nav collapse behaves exactly as specified | `data-nav="auto"` column width: **248px @1352 · 64px @852 · absent @372**. `data-nav="rail"`: **64 · 64 · absent** — the user's toggle holds in both wide bands and the narrowest band wins outright. | ✅ **DRIVEN** |
| 13 | The multi-column pane collapse, and the inactive pane leaves the a11y tree | rail/list/detail = **[64,582]/[360,582]/[926,582] @1352** · **absent/[320,582]/[530,582] @852** · **absent/absent/[370,582] @372**. Focusable count in the hidden pane: **0**. | ✅ **DRIVEN** |
| 14 | ★★ **ds-005 repaired here, and the probe CAN fail — the gated parent still fails it** | Range-vs-box measurement of every *visible* descender label: `Sidebar-nav` **4 of 4 clipping, 4.00px each, computed `text-box-edge: cap alphabetic`**; `App-shell-top-nav` **0 of 12**; `App-shell-side-nav` **0 of 8**; `App-shell-multi-column` **0 of 6**, all computing `text`. Before the two-class fix my files measured **identically to the parent** (box 11.56 / text 21 / clip 4.00), which is what proves it was INHERITED and not introduced. | ✅ **DRIVEN + CONTROLLED** |
| 15 | The drawer is a real modal: focus in, background inert, Esc out, focus returned | top-nav @420: closed `{expanded:false, focusInSheet:false, tabbableOutside:9}` → open `{expanded:true, focusInSheet:**true**, active:"Close main menu", mainInert:true, tabbableOutside:**0**}` → Escape `{expanded:false, active:"**Open main menu**", tabbableOutside:9}`. Same three readings on the side-nav shell. | ✅ **DRIVEN** |
| 16 | The nav toggle updates every name it owns, and the rail keeps its accessible names | expanded `{w:248, aria-expanded:"true", label:"Collapse navigation", nav aria-label:"Main"}` → rail `{w:64, "false", "Expand navigation", "Main, collapsed"}`, and the label box goes **185×11.6 → 1×1** while the link's accessible name stays **"Overview"** — hidden, not removed. | ✅ **DRIVEN** |
| 17 | Choosing a list row retitles the detail, moves the current mark, and BACK restores focus to the row | pick 3rd row → `{pane:"detail", title:"**Client money account**", current:"Client money account…", listTabbable:0}`; back → `{pane:"list", focus:"**Client money account**…"}` — focus lands on the row, not the top of the list. | ✅ **DRIVEN** |
| 18 | The one real loading region is Skeleton-loader's own behaviour, unchanged | `{busy:"true", role:"status", srText:"**Loading content**", anim:"shimmer", animDur:"1.4s", bones:4}` → after resolve `{busy:"false", srText:**null**, anim:null, bones:0}` | ✅ **DRIVEN** |
| 19 | The static furniture does NOT announce, and only the genuine loaders do | `staticBonesWithStatus` = **0** (every static bone sits under an `aria-hidden` ancestor); `statusRegions` = **2** — exactly the two real loaders in the multi-column detail panes | ✅ **DRIVEN** |
| 20 | Reduced motion is honoured, including Skeleton-loader's own fallback | context `reduced_motion:"reduce"` → `{animationName:"**none**", animationDuration:"1e-05s", backgroundImage:"**none**"}` — static bones, shape alone reads as loading (2.3.3) | ✅ **DRIVEN** |
| 21 | The current-location mark carries THREE channels in both modes, not colour alone | side-nav: `box-shadow:"rgb(219,0,17) 3px 0px 0px 0px inset"` + `background rgb(240,240,240)` light / `rgb(35,35,35)` dark + `aria-current`. top-nav: `inset 0 -3px 0` in the same red. | ✅ **DRIVEN** |
| 22 | Theme inversion is real | body `rgb(255,255,255)/rgb(26,26,26)` fg `rgb(26,26,26)/rgb(255,255,255)`, bone `rgb(240,240,240)/rgb(35,35,35)` — read in all 18 combinations | ✅ **DRIVEN** |
| 23 | The library has **no selected list row** — the finding behind the multi-column's largest judgment | `grep -c 'aria-current\|aria-selected' knowledge/snippets/List-items.reference.html` → **0** | ✅ **and it argues for the borrow** |
| 24 | The brand-mark gap is real and this lane did not paper over it | `grep -rl 'assets/logos' knowledge/snippets/` → **0 of the 108 pre-existing snippets**, against **12 official SVGs** in `knowledge/assets/logos/`. Row 86's own derived verdict is `ASSET-ONLY`. | ✅ **NAMED GAP** |
| 25 | The three rail rules the shell adds are ADDITIONS, not edits of the gated parent | `grep -c 'is-rail .sn-group-toggle' knowledge/snippets/Sidebar-nav.reference.html` → **0**; and `grep -c 'sn-link\[aria-current\]' …/Sidebar-nav.reference.html` → **0**. The parent's own rail specimen contains no collapsible group, which is why its rail rules never had to say what happens to one. | ✅ **and it is arguably a gap in the parent** |
| 26 | No breakpoint scale exists to bind to | `python3 -c "import json;print('breakpoint' in json.dumps(json.load(open('knowledge/tokens/layout.json'))).lower())"` → **False** | ✅ **OPEN, and it is the biggest one** |
| 27 | The render run left no strays in the tree (`s133-D2` clean-tree gate) | `ls -a knowledge/assets/fonts/_desktop/TTF/ \| grep -c '^\.uuid'` → **0**, after every render pass (symlink-farm recipe, #138) | ✅ |
| 28 | No RAG value is painted in any of the three | The only red anywhere is `primary/border/default` on the current-location mark, which is `Navigations`'/`Sidebar-nav`'s own approved bar. Two-red law (`s151-D1`) and the mono error ink camp (`s149-D1`) untouched; no `rag/*` token is bound in any of the three manifests. | ✅ |

---

## 4 · WHAT WAS DRIVEN — a real browser, both modes, three widths, three files

Headless Chromium (`chromium_headless_shell-1234`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`), `goto("file://…")` per `_RUNBOOK-render-verify.md`, symlink-farm fontconfig
(#138) with the two-alias block and the mandatory `<include>`. **18 layout screenshots taken and
LOOKED AT** (3 shells × 1400/900/420 × light/dark), plus 3 behaviour stills and 2 high-DPI label
crops, plus scripted measurement of computed styles, hit boxes, focus, inertness, tab order and
container-query state.

**Defects 2, 3, 4 and 6 in § 0 were found by looking at a picture after the numbers said the
page was fine.** Defect 2 is the sharpest example: my own probe *reported* the menu button as
present at 1400px and I read that as "the control exists" — I had no assertion that it should be
**absent**. The screenshot showed a hamburger sitting beside five visible nav links.
⇒ ★ **A measurement without an expected value is not a test.** That is [[green-tests-cannot-see-scope]]
arriving through my own instrument rather than through someone else's gate.

---

## 5 · WHAT WAS COMPOSED, AND WHAT IS GENUINELY NEW

**Borrowed verbatim, every region diff-nameable:** `Sidebar-nav` (the entire `.sn-*` rule set,
sprite symbols, markup shape, the three current-location carriers, the `.is-rail` clip-path
collapse) · `Navigations` (masthead geometry, the inset red current bar, 44×44 action buttons) ·
`Breadcrumbs` (nav landmark + `ol` + "/" separator + `a.crumb` underline and focus shapes) ·
`Footer` (the slim legal bar and the `a.lnk` atom Footer itself took from `Links`) ·
`Skeleton-loader` (the bone shape kit; and **verbatim and complete**, announcement included, for
the one genuinely-loading region) · `Drawer` (scrim, translateX sheet, inert, Esc, focus return) ·
`Headers` (the 56px in-app header height and the back control) · `Command-palette` line 36 (the
leading-trim block, byte-identical). **⛔ No parent file was edited.**

**Genuinely new, and it is small on purpose:** the `.sh-*` frame classes, which position parts
and style none of them — plus **five declared additions**, each named in the file that carries it:
the three rail rules for a collapsible group (claim 25), the `.sn-link[aria-current]` selector
widening for a list row, the list row's additive `min-height: 44 → 64`, the breadcrumb 44px
target, and the two-class `text-box-edge` overrides.

★ **Two approved artefacts disagreed and the gated one won.** `Skeleton-loader` announces
(`role="status"`, `aria-busy`, "Loading content"); the gated `Sidebar-nav`'s `.sn-canvas` bars do
not. A shell specimen is a frame with the content deliberately left out — it is **not loading** —
so copying the loader whole would make every shell announce a load that never completes, forever,
to every screen reader. The **shape kit** is copied and the **announcement** is not; one region
in the multi-column shell keeps the real loader so the genuine composition is demonstrated
somewhere. **PROPOSED — `$decisionsForDave` 6/7 asks Dave to confirm it once for all three.**

★ **The type divergence is the Footer #204 finding repeating, class-identical.** "Copy the
approved artefact verbatim" and "add zero to the shrink-only ratchet" **conflict when the approved
artefact is itself in debt**: `Navigations` writes `font-weight:500`/`font-size:20px` on `.logo`,
`Breadcrumbs` writes `font:400 14px/1.5` on `nav ol`. Geometry copied, type re-keyed to markup
composites (T-D14). **Ratchet contribution: 0** (claim 5). Neither parent edited.

---

## 6 · EVERY OPEN DESIGN QUESTION — `$decisionsForDave`, named and NOT settled

All of these are Dave's; none is answered by construction. Full text lives on each meta's face.

1. ⛔ **THE BREAKPOINT SCALE — the biggest one, and it spans the wave.** Three shells built in
   one wave carry **three different pairs**: 900/600 · 1040/720 · 1200/840. `layout.json` has no
   breakpoint scale (claim 26). Nothing binds them and nothing ever will until one is minted.
2. ⛔ **THE SELECTED LIST ROW.** `List-items` models no selected state (claim 23). The row here
   is `Sidebar-nav`'s nav link, borrowed for its three "you are here" carriers. Live outcomes:
   keep the borrow · give `List-items` a selected state · make the list a `role="listbox"`.
3. **`aria-current="true"` or `aria-selected`** for a master-list row?
4. **THE BRAND MARK.** 12 official SVGs, nothing binds them, zero of 108 snippets reference them;
   row 86 is P1 and `ASSET-ONLY`. A component, or a direct embed? Until answered, every shell
   carries a text wordmark stand-in.
5. **DOES A SHELL BELONG IN `knowledge/snippets/` AT ALL?** § 2 is the evidence for; the evidence
   against is that the showroom, the KG and `component-types.json` all assume components.
6. **`category: "template"` and `$layer`** — should the schema gain a real `layer` property and a
   `shell` category value?
7. **THE PLACEHOLDER CONVENTION** — static `aria-hidden` furniture for a frame, the real
   announcing loader only where something genuinely loads. Confirm or overturn, once, for all three.
8. **THE THREE-WAY COLLAPSE PRECEDENCE** — query sets the default, the user's toggle overrides
   inside the band where both states are legal, the narrowest band wins outright.
9. **THE THREE NEW RAIL RULES** — should they go back into the **gated parent**, where they
   arguably belong? A worker lane could not touch a gated file to find out.
10. **INLINE OR STACKED** as the product's default top nav?
11. **THE TRAIL AT PHONE WIDTH** — drop ancestors (drawn) vs an ellipsis disclosure vs a single
    "Back to <parent>" link.
12. **WHAT THE DETAIL PANE SHOWS BEFORE A ROW IS CHOSEN** — drawn pre-selected, which quietly
    makes a choice for the user. `Empty-state` exists and is the alternative.
13. **DOES CHOOSING A ROW CHANGE THE URL?** Drawn as a pane swap with no history entry, so the
    browser back button leaves the shell. On a phone that is very likely wrong.
14. **SHOULD `Breadcrumbs` ITSELF GROW 44px TARGETS?** Its links measure **10.1px tall** today
    (defect 5). The shell grew them; the gated parent still has none.
15. **THE `Sidebar-nav` / `Navigations` OVERLAP**, carried open from #203. This shell consumes
    both. Whatever Dave rules, the composition is unaffected.
16. **THE RAIL TOOLTIP**, carried open from #203 — a rail item has no visible name.

---

## 7 · WHAT STAYS UNPROVEN — declared, not smoothed

1. **THREE OF THE FOUR THEMES ARE UNPROVEN FOR ALL THREE SHELLS.** No `.cn-app-shell-*` block
   exists in `canon.css` (claim 8), so theme-cascade projection is silently OFF and **only the
   light and dark legs authored in each snippet have been seen. Console, Legacy and Supercharge
   have not been looked at.** The canon block is the conductor's.
2. **The Supercharge contrast figure is CARRIED, NOT RE-MEASURED.** `Sidebar-nav`'s meta records
   `primary/border/default` on `tertiary/background/hover` at 4.58/3.01 in mono, legacy and
   console and **3.89 light / 2.73 dark in Supercharge — a FAIL**. Quoted, not re-measured at
   #210. ⚠ In the multi-column shell it now applies on **two** surfaces (rail and list), not one.
3. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration Lane M made at #204 and
   Lane A at #209. **OWED.**
4. **Measured in ONE browser at ONE zoom** (headless Chromium, 1400/900/420, `deviceScaleFactor`
   1 except the two label crops at 3). No second engine, no zoom pass, no real touch device.
5. **No screen reader was run.** Focus, inertness, roles and accessible names were measured
   programmatically; nothing was *heard*.
6. **`_validate_kg.py` was not run by this lane**, and the metas name contexts and patterns that
   do not exist as nodes (`context:app-shell`, `pattern:page-frame`, `pattern:desktop-app-frame`,
   `pattern:list-detail`). Every one is `ref: null` with prose — **flagged, never guessed**.
   `gen_kg_edges.py` is the conductor's.
7. **Two short breadcrumb links are 39.4px WIDE** — above WCAG 2.5.8's 24px floor, below the
   repo's 44px figure. **Not padded, deliberately:** an underline wider than the word it underlines
   is a worse defect than a narrow target. Declared rather than fixed.
8. **The multi-column rail's head is an empty 56px box** (the brand is clip-path hidden and this
   shell drops the toggle, because the frame owns the collapse). It aligns with the list and
   detail headers, which reads as deliberate — but it was not designed to, and it is noted rather
   than defended.
9. **Nothing here has been seen by Dave**, and nothing is registered anywhere.

---

## 8 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. `.cn-app-shell-top-nav`, `.cn-app-shell-side-nav`, `.cn-app-shell-multi-column` blocks in
   `canon/canon.css` — clears **3 of the 11** check-D failures and unblocks the three unseen themes.
2. Re-run `gen_kg_edges.py` — the four `ref: null` nodes above.
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` ·
   `_validate_radius.MIGRATED_SNIPPETS` registrations, **if** the three are kept.
4. ⚠ **THE OTHER 8 check-D FAILURES ARE SIBLING LANES'** (`Filter-toolbar-bar`,
   `Page-header-lockup`, `Template-create-edit`, `Template-dashboard`, `Template-wizard`,
   `Template-auth`, …). Named here so they are not attributed to Lane A.
5. ⚠ **RUNNING THE GATES REWROTE TRACKED FILES, AND THAT IS DECLARED, NOT HIDDEN.**
   `knowledge/_A11Y-GATE.md`, `knowledge/_SNIPPET-AUDIT.md` and `knowledge/_ICON-SOURCE-AUDIT.md`
   are modified as a **side effect** of the gate runs in this receipt. **No lane edited them by
   hand**, and Lanes B/C/D ran the same gates, so attribution is **the wave's, not any one
   lane's**. Same class Lane A declared at #209. ⛔ **Reconcile every path deliberately — never
   `git add -A`** [[feedback-worktree-reconcile-trail]].
6. **`knowledge/_state.json` is being written by four lanes concurrently this session.** This
   lane re-read it after its own write and confirmed its row landed intact; a conductor-side
   re-read before commit is still owed.
7. **The ds-005 cross-lane decision named in `W-74` is now THREE-times caught** and this lane
   carries the first repair-with-a-control. A repo-wide answer is Dave's, and the natural shape of
   it is a gate that reads the **computed** edge rather than the declaration.
8. Consider whether `Breadcrumbs` should gain 44px targets (open question 14) — this lane
   demonstrated the fix in a shell and **did not repair the gated parent**.
