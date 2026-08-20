# Receipt — #210 Wave 6 · Lane A · the four P3 app shells

**Lane:** A (Opus) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave6-layer2-p3-fanout-brief-v1.md` (THE JOB, Lane A)
**Members:** App-shell-split (row 100) · App-shell-focused (row 101) · App-shell-doormat (row 102) · App-shell-nav-rail (row 103) — all P3, all `NO-ARTEFACT-CLASS`
**Sibling precedent + composition source:** `notes/_receipts/2026-08-20-210-wave5-laneA-app-shells.md`
**Store row:** see § 9 — minted at creation per [[forgotten-document-class]]

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every shell decision below is PROPOSED and is
> Dave's. No registry, `MIGRATED_SNIPPETS`, `CATEGORIES`, `component-types.json`, `canon.css`,
> `_rulings.json`, showroom or git operation was touched — this lane created **NEW FILES ONLY**.

---

## 0 · THE HEADLINE: SIX DEFECTS, AND THE FIFTH ONE WAS IN MY OWN INSTRUMENT

Wave 5's lane A found six defects that every gate was green over. This lane found six more, and
the sharpest lesson is different: **three of them were in the probes, not the pages.** A probe
that is confidently wrong is worse than no probe, because it produces a number you can put in a
receipt.

| # | defect | how it was found | why no gate saw it |
|---|---|---|---|
| 1 | **Pane-head action buttons were 36×36**, under the repo's own `target/min`. | driven hit-area sweep | **No gate reads `target/min` for hit area.** 36px clears WCAG 2.5.8's 24px floor, so nothing complained. Identical blind spot to wave 5's Breadcrumbs catch. |
| 2 | **An in-page anchor jump landed its heading UNDER the sticky masthead** — and then, once fixed, landed it **1px** under. | driven, with an expected value | Nothing throws. A screenshot of an un-jumped page is perfect. No gate in this repo models a sticky occlusion. |
| 3 | ⛔ **The label flyout failed SC 1.4.13's HOVERABLE clause** — it vanished the instant the pointer reached it. | driven | The markup was flawless and the CSS was plausible. The failure lives in `pointer-events`, three levels down a hover chain. **I had written a comment justifying the very line that broke it.** |
| 4 | **The nav rail sat BESIDE the content at phone width**, not below it — `order` cannot turn a parent's main axis, and the parent was the query container. | driven | `railIsBelowBody: false` while every other number was green. In a thumbnail it reads as a plausible narrow layout. |
| 5 | ⛔ **The phone bar's five labels collided and two ran off the end** — while **document overflow measured 0**, because `.sh{overflow:hidden}` ate the excess. | **LOOKED AT**, then re-measured with a rail-scoped probe | ★★ **My overflow probe had the wrong SUBJECT.** It asked the document a question about a 370px bar. |
| 6 | **A stray `*/` broke the doormat stylesheet mid-file**, silently reverting `scroll-margin-top` to 0. | the mutation control caught it | A broken comment produces no error. The page renders; one property just stops existing. |

★★★ **And the instrument itself failed four times before it was right.** The descender-clip probe
went through five versions, and versions 1–4 were each confidently wrong about the page for a
reason that had nothing to do with the page:

| v | what it claimed | why it was wrong |
|---|---|---|
| 1 | 13 clipped labels | `<h2>`/`<p>` sit **outside** the trim block by design and hang their descenders over `overflow:visible` — that is not a clip |
| 2 | 8 clipped labels | flagged anything under **any** clipping ancestor; a 2px descender 400px inside a frame is not cut by it |
| 3 | 20 "clipped", cuts of 135px | treated a **scroller** as a clipper — content below the fold is *paged*, not clipped |
| 4 | still over-reporting | fixed the scroller one level up and met it again one level out (`.sh-scroll` inside `.sh`) |
| **5** | **0, and it can fail** | a scrollable ancestor **stops the walk**; only `hidden`/`clip` cuts. Mutation control: plant a 6px `overflow:hidden` box → **exactly 1 finding, named `clip-bite`, 25px cut**; remove it → **0** |

⇒ ★ **A measurement without an expected value is not a test** — wave 5's lesson, arriving five
times through my own hands. Every claim in § 3 that carries a mutation control carries it because
of this.

---

## 1 · FILE LIST — eight new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/App-shell-split.reference.html` | 58,246 |
| 2 | `knowledge/components/app-shell-split.meta.json` | 22,637 |
| 3 | `knowledge/snippets/App-shell-focused.reference.html` | 30,920 |
| 4 | `knowledge/components/app-shell-focused.meta.json` | 20,832 |
| 5 | `knowledge/snippets/App-shell-doormat.reference.html` | 50,889 |
| 6 | `knowledge/components/app-shell-doormat.meta.json` | 21,053 |
| 7 | `knowledge/snippets/App-shell-nav-rail.reference.html` | 57,338 |
| 8 | `knowledge/components/app-shell-nav-rail.meta.json` | 26,451 |
| 9 | `notes/_receipts/2026-08-20-210-wave6-laneA-p3-shells.md` | 31,571 (this file, at the moment it was measured) |

**Totals: 197,393 bytes of snippet · 90,973 bytes of meta.** ⚠ **Every snippet count in § 3 reads
135, and that is the WHOLE WAVE, not this lane.** Wave 5 landed the library at 119; wave 6's four
lanes are writing concurrently, so 135 = 119 + this lane's 4 + the sibling lanes' 12. **Attribute
by name, never by the total** — every claim below that could be attributed is.

**No existing file was edited. Not one.** Renders live OUTSIDE the repo
(`(NON-REPO: the session outputs folder, laneA6/renders/*.png)` per `s191-D2`) — 24 layout PNGs
(4 shells × 3 widths × light/dark) plus 3 behaviour stills. Working artefacts, not deliverables.

---

## 2 · WHAT WAS COMPOSED — and the composition that is new in kind

★ **This lane composed a WHOLE SHELL, not a set of atoms.** App-shell-split is
App-shell-top-nav's frame with its `.sh-main` replaced by a Splitter; App-shell-doormat is the
same frame with a sticky masthead and Footer's full mat; App-shell-focused is that frame with
almost everything **removed**. That is a stronger form of composition than wave 5 could attempt,
because wave 5 had no shell to compose from — and it means these four inherit wave 5's two
measured defect repairs (`.sh-legal li{display:flex}`, the two-class `.sh .sh-menu`) rather than
re-discovering them.

| region | source | carried |
|---|---|---|
| `.sh` frame, skip link, masthead, 44×44 actions, off-canvas sheet + its four-step open sequence, slim legal bar | **App-shell-top-nav** (#210 wave 5) | all four files |
| `.sp` grid, fences, `role=separator` + % `aria-valuenow`, 24px `::before`, three-stroke grip **with its `data-bespoke` string unchanged**, key map, ratio-on-resize rule | **Splitter** | split |
| `.pb-track`/`.pb-fill`, `role=progressbar`, the **named** reduced-motion fill suppression | **Progress-bar** | focused |
| `.ft-inner`/`.ft-brand`/`.ft-mat`/`.ft-legal`, `a.lnk`, `a.arrow`, the 44px-at-every-width rule, **Footer's own `@container (max-width:560px)`** | **Footer** | doormat |
| `.btt-stage`/`.btt-content` scrolling frame + the region-scoped scroll handler | **Back-to-top** | doormat |
| `.sn-*` rail atoms in `.is-rail` form + the six icon symbols byte-for-byte + **the expanded `.sn-label` ellipsis rule** | **Sidebar-nav** | nav-rail |
| flyout panel skin: `background/default` on `elevation/border`, `0 0 16px` on `elevation/functional` | **Popover** | nav-rail |
| bone shape kit, **announcement NOT copied** | **Skeleton-loader** | all four |
| leading-trim block, byte-identical | **Command-palette** line 36 | all four |

**Genuinely new, and small on purpose:** the `.sh-pane`/`.sh-split` frame classes, the
`--axis` mechanism, the `.sh-fly` flyout, `scroll-margin-top`, and `.sh-inner`.
⛔ **No parent file was edited.**

---

## 3 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | Snippet gate clean with all four present | `python3 knowledge/_validate_snippets.py` → *"snippet gate: 135 snippet(s), 0 failure(s)"* | ✅ |
| 2 | 4px-grid gate clean — **after a real catch** | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS — all layout dimensions on the 4px grid (151 file(s))"*. It first FAILED: *"✗ off-grid: padding: 6px (App-shell-nav-rail…)"* | ✅ **caught something** |
| 3 | a11y gate: zero failures | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 135 snippet(s), 0 failure(s), 285 warning(s)"* | ✅ |
| 4 | Descender-clip gate passes | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS … (151 file(s))"* | ✅ |
| 5 | ⛔ **Type-composite debt did NOT grow. The four files add ZERO** | `python3 knowledge/_validate_type_composites.py \| grep -c "App-shell-split\|App-shell-focused\|App-shell-doormat\|App-shell-nav-rail"` → **0**, total *"1097 violation(s)"* — exactly the `#203` baseline. Attribute by grep, never by the total. | ✅ |
| 6 | Metas are schema-valid — **after a real catch** | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"136 meta(s) checked · 0 finding(s)"* → *"PROBE P-1 — findings=0"*. It first reported **19 findings**: `slots/*/accepts` permits **`tier` and `capability` ONLY** (`s140-D1`, `additionalProperties:false` — *"a child list has nowhere legal to go"*). Component lists moved to `$acceptsInPractice`. | ✅ **caught something** |
| 7 | Icon-source gate: zero unknowns | `python3 knowledge/_validate_icons.py` → *"0 UNKNOWN, 97 bespoke, across 135 snippet(s)"*. Every glyph is byte-copied from a gate-passing snippet; `chevron-left.svg` and `arrow-up.svg` were byte-diffed against the library by hand. | ✅ |
| 8 | ★ **Every hex in every theme block is the STORE's value, not a typed one** | `python3 knowledge/gen_snippet_tokens.py --check` → *"4696 manifest bindings across 135 snippets + 9 tranches; **0 value(s) would change**; 0 canon.css literal(s) would change"* | ✅ |
| 9 | ⛔ **binds-resolve check D FAILS for all four — DECLARED, not hidden** | `python3 knowledge/_validate_binds_resolve.py` → *"119/135 canon blocks · 16 failure(s)"*, naming `App-shell-split`, `App-shell-focused`, `App-shell-doormat`, `App-shell-nav-rail` **+ 12 sibling-lane files** | ⛔ **CONDUCTOR'S** |
| 10 | The real HSBC cut rendered — **asserted with two controls** | canvas `measureText('Handgloves 12345')` at 40px: `HSBC_MtUnivers_Latin` **346.88** · `"Univers Next HSBC"` **346.88** · `"Univers Next for HSBC"` **346.88** · `DejaVu Sans` **375.39** · nonexistent **301.07**. Identical on all four files. Matches the runbook's own canonical table exactly. | ✅ **DRIVEN** |
| 11 | Zero horizontal overflow, every shell, every width, both modes | `documentElement.scrollWidth − clientWidth` = **0** at 1400/900/420 × light/dark, all four files (**24 readings**). ⚠ **AND THIS NUMBER IS WEAKER THAN IT LOOKS — see defect 5 and claim 21.** | ✅ **but see 21** |
| 12 | ★★ **The axis flip is real, and the script and the CSS cannot disagree** | Same shell, three container widths: **1352 → `--axis:x`, tracks `638px 8px 638px`, `aria-orientation="vertical"`, separator tabbable · 852 → `--axis:y`, tracks turned, `aria-orientation="horizontal"`, still tabbable · 512 → `display:flex`, divider `display:none`, tabbable separators 0.** The script reads the computed `--axis`, never the attribute. | ✅ **DRIVEN** |
| 13 | The collapse is the CONTAINER's, not the viewport's — all four files | Each file's third specimen is a **392px container at a 1400px viewport** and is fully collapsed while its 1352px siblings are not. Split: divider `display:none`, tabbable 0. Focused: card border 0px. Doormat: mat 1 column, nav `display:none`. Rail: rail below body, labels visible. | ✅ **DRIVEN** |
| 14 | Splitter's fences hold, and both input paths share one clamp | `#sp-h`: 50 → **55** after 4×ArrowRight; **Home → 19, not 0**, with pane width 240px against `--min-pri: 240px` — the fence wins, which is the proof; F6 → **50**. | ✅ **DRIVEN** |
| 15 | Coequality is constructed, not asserted | pane head heights **[48, 48]** · pane classes **["sh-pane", "sh-pane"]** · `--min-pri` 240px == `--min-sec` 240px · `document.querySelectorAll('.is-primary').length` → **0** | ✅ **DRIVEN** |
| 16 | The drawer is a real modal: focus in, background inert, Esc out, focus returned | split @420: closed `{tabbableOutside:10}` → open `{focusInSheet:true, active:"Close main menu", tabbableOutside:0}` → Escape `{active:"Open main menu", tabbableOutside:10}` | ✅ **DRIVEN** |
| 17 | ★★★ **The sticky-anchor occlusion fix works, AND THE PROBE CAN FAIL** | **as authored:** `scroll-margin-top 68px`, target top **68.0**, masthead bottom **65.0**, gap **+3.0**, `targetClearsMasthead: true`. **MUTATED (property removed):** target top **0.0**, gap **−65.0**, `targetClearsMasthead: false`. And the picture agrees — see § 4. | ✅ **DRIVEN + MUTATION CONTROL** |
| 18 | The masthead really pins | `position: "sticky"`, measured height **65.0**; after `scrollTop=400`, masthead top − scrollport top = **0.0**. ⚠ v1 of this probe read back `scrollTop: 0` — `scroll-behavior:smooth` **animates** an assignment. [[settle-the-transition-before-you-read]], arriving through scrolling. | ✅ **DRIVEN** |
| 19 | Non-duplication is measured, and the rule is Footer's own | masthead **4** links · mat **16** links · **intersection = [] (size 0)**. Footer's own antiPattern: *"a doormat that duplicates the masthead is a doormat that has stopped being read."* | ✅ **DRIVEN** |
| 20 | The mat re-flows with **no query at all** | `grid-template-columns` at three container widths: **`260px ×4` @1352 (one row)** · **`192.5px ×4` @852 (one row)** · **`478px` @512 (four rows)**. `auto-fit`/`minmax(180px,1fr)` is Footer's line; no breakpoint duplicates it. | ✅ **DRIVEN** |
| 21 | ⛔ **The rail's own overflow — the question the document probe could not answer** | rail-scoped probe at a 370px bar. **BEFORE:** `itemsPastRightEdge: 2`, `railScrollOverflow: 120px`, labels touching. **AFTER:** `0` and `0`. Document overflow read **0 in both states**. | ✅ **DRIVEN, after a LOOKED-AT catch** |
| 22 | ★★★ **SC 1.4.13, all three clauses, and the HOVERABLE one failed first** | Six-state sequence on one rail item: rest `hidden` → hover `visible` → **Escape with the pointer still on the icon** `hidden`, `data-fly-dismissed="true"` → leave-and-re-hover `visible` → **pointer parked at the panel's own centre `visible`** (was **`hidden`** before `pointer-events:auto`) → focus `visible`. Panel `left` 88.0 vs link `right` 89.0 = **1px overlap, no dead space.** | ✅ **DRIVEN + BEFORE/AFTER** |
| 23 | The two flyout contracts are honoured | 6 of 6 label flyouts `aria-hidden="true"` with the link's clip-path name intact; **`labelFlyoutsAnnounced: 0`**. Menu flyouts: `aria-hidden` **null**, `<nav aria-label="Money">`, 4 links. | ✅ **DRIVEN** |
| 24 | Menu flyouts are a disclosure, not a hover | closed `{expanded:"false"}` → **hover → still `"false"`, still hidden** → click `{expanded:"true", visible, active:"Money"}` → open a sibling → **first closes** → Escape → `{expanded:"false", active:"Money"}` (focus returned to its opener) | ✅ **DRIVEN** |
| 25 | ★★ **The rail moves BELOW the content — after the self-query trap sent me the wrong way** | **BEFORE:** railTop **1245** == bodyTop **1245**, `railIsBelowBody: false`, rail **283px wide** and beside the content. **AFTER (`.sh-inner` split):** railTop **1792** > bodyTop **1249**, `railIsBelowBody: true`, rail **390px**, `flex-direction: row`, current mark rotated to `inset 0 3px`. | ✅ **DRIVEN + BEFORE/AFTER** |
| 26 | The rail label is hidden, never removed — and comes back at phone width | wide: label box **1×1**, `clip-path: inset(50%)`, text "Overview". phone: **69.5×21**, `clip-path: none`, same text; label flyout `display: none`. | ✅ **DRIVEN** |
| 27 | The full-bleed card, measured rather than asserted | `border-top-width` **1px** @1352 and @852; **0px** @512 and @392, padding `0px 16px`, and card width **390.0** == shell inner width **390.0**. | ✅ **DRIVEN** |
| 28 | The exit control keeps its name and loses its label | **150.8×44.0** with a **102.8×11.6** label at 1352cqi → **44.0×44.0** with a **1×1** label at 392cqi; accessible name *"Save this payment and return to Accounts"* **byte-identical in both**. | ✅ **DRIVEN** |
| 29 | One progress statement per shell | `shell-auth` **0** progressbars / **0** `aria-current="step"` · `shell-task` **1** / **0**, `aria-valuetext: "Step 2 of 4, Recipient"`, fill 643px of a 1286px track. | ✅ **DRIVEN** |
| 30 | ⛔ **Not one red pixel in App-shell-focused** — stronger than the siblings can claim | Full-document sweep of every computed `color`/`background`/`border`/`box-shadow` for `r>120, g<80, b<80` → **`redPaintCount: 0`**, and `--indicator` is **not declared at all**. | ✅ **DRIVEN** |
| 31 | Back-to-top moves the view AND the focus | from `scrollTop 625`, focus on `BODY` → activation → focus on **`H1` "Personal banking"**, `tabindex="-1"` applied **at activation**, never authored. | ✅ **DRIVEN** |
| 32 | Hit areas: every control ≥44px, one declared exception | Driven sweep, all four files, both themes, three widths → **empty** for focused / doormat / nav-rail. Split names only the two separators (**8×416** and **1284×8**), whose 24px `::before` is Splitter's own declared inherited-restraint call. | ✅ **DRIVEN** |
| 33 | Descender clip: zero, and the probe CAN fail | v5 probe: `clipped: []` in **light and dark on all four files**, and in the rail's phone band where labels are visible, with `trimmedMaxOverhang: 0`. **Mutation:** plant a 6px `overflow:hidden` wrapper → **1 finding, `clipper: "clip-bite"`, 25px** → remove → **0**. | ✅ **DRIVEN + MUTATION CONTROL** |
| 34 | Theme inversion is real, all four | body `rgb(255,255,255)/rgb(26,26,26)` ↔ fg `rgb(26,26,26)/rgb(255,255,255)`; split divider `rgb(225,225,225)/rgb(128,128,128)`; focused fill `rgb(26,26,26)/rgb(255,255,255)` on track `rgb(240,240,240)/rgb(72,72,72)`; **flyout border `rgba(255,255,255,0)` light / `rgb(128,128,128)` dark** — Popover's own transparent-in-light choice, carried; current mark `rgb(219,0,17)` in both. | ✅ **DRIVEN** |
| 35 | No RAG value is painted in any of the four | The only red anywhere is `primary/border/default` on a current-location mark — Navigations'/Sidebar-nav's own approved bar. No `rag/*` token is bound in any of the four manifests. Two-red law (`s151-D1`) and the mono error ink camp (`s149-D1`) untouched. | ✅ |
| 36 | The render run left no strays in the tree (`s133-D2`) | `ls -a knowledge/assets/fonts/_desktop/TTF/ \| grep -c '^\.uuid'` → **0**. The fontconfig farm and its cache live on the outputs mount, never in the repo. | ✅ |

---

## 4 · WHAT WAS DRIVEN — and a new sandbox pothole worth banking

Headless Chromium (`chromium_headless_shell-1234`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`), `goto("file://…")` per `_RUNBOOK-render-verify.md`, symlink-farm fontconfig
(#138) with the two-alias block and the mandatory `<include>`. **24 layout screenshots taken and
LOOKED AT** (4 shells × 1400/900/420 × light/dark), plus three behaviour stills: a menu flyout
open, the doormat scrolled, and the doormat **after a real anchor jump**.

⚙ **NEW POTHOLE, n=8 — `TMPDIR` ON THE SHARED MOUNT HANGS PLAYWRIGHT INDEFINITELY.**
The runbook's ENOSPC strata (n=3…n=7) all point at putting scratch somewhere with room, and the
outputs mount has 316 G free against `/` at 99 %. Pointing `TMPDIR` there made
`sync_playwright()` **hang forever** — not ENOSPC, not an error, no output at all; two 120 s
calls died on the timeout with nothing in the log. The browser binary itself ran fine standalone
(`--dump-dom about:blank`, rc 0), which is what isolated it to the node driver's temp files.
**`TMPDIR=/var/tmp` and it launches in 0.3 s.** ⇒ **`PLAYWRIGHT_BROWSERS_PATH` and the font farm
go on the shared mount; `TMPDIR` must stay on the local filesystem.** Worth folding into
`_RUNBOOK-render-verify.md` — that is the conductor's call, not this lane's.

★ **Defects 5 and 6 were found by LOOKING at a picture after the numbers said the page was
fine**, and defect 5 is the sharper one: the bottom bar's five labels were touching and two had
run off the end, while my overflow probe returned a confident **0** — because the excess was
being eaten by `.sh{overflow:hidden}` and I had asked the *document*, not the *bar*.

---

## 5 · EVERY OPEN DESIGN QUESTION — `$decisionsForDave`, named and NOT settled

Full text lives on each meta's face. Thirty-two in total; these are the ones that span the wave
or that a reviewer should not miss.

1. ⛔ **THE BREAKPOINT SCALE — carried from wave 5, still the biggest.** All four of this lane's
   shells deliberately reuse App-shell-top-nav's **900/600** pair rather than adding a fourth to
   wave 5's three-way spread. **Reusing an unruled number is not the same as having one.**
   `layout.json` still has no breakpoint scale. ⚠ App-shell-doormat sharpens it: it now carries
   **two thresholds from two different owners** (900/600 mine, **560 Footer's**), and neither is ruled.
2. ⛔ **WHAT DOES THE FOCUSED SHELL'S ONE EXIT DO?** The central question of row 101 and
   deliberately unanswered. Does "Save and exit" save a draft? Does "Exit" on a half-finished
   payment discard it? Does it need a Popconfirm or a Modal? The library has both.
3. ⛔ **ONE PROGRESS STATEMENT PER SCREEN.** App-shell-focused's band and Template-wizard's step
   rail both say where you are. Hosted together they say it twice, in two vocabularies. Drawn as:
   the shell owns the band, a hosted rail is decorative. **This must be ruled once for the
   library, not per file.**
4. ⛔ **THE TWO-CONTRACT FLYOUT RULE** — a flyout that repeats a name is decorative and hidden; a
   flyout that offers destinations is a disclosure and announced. Same pixels, opposite markup.
   This is App-shell-nav-rail's central proposal and it answers the **#203 rail-tooltip question**
   — which may not be the answer Dave wants: a real Tooltip, or permanent micro-labels, or
   accepting that a rail is for experts, are all live alternatives.
5. ⛔ **THE PHONE BAR NEEDS A SHORT-NAME CONVENTION OR A CAP, and this is measured.** Four short
   names fit a 390px bar with **zero truncation**. Five names including "Payments and transfers"
   truncate to 62px boxes and read as *"Overv… Acco… Paym… Cards Spen…"*. The library has no
   short-name convention. Options: mint one · cap at four with a **More** disclosure (Tab-bar's
   own answer) · make the phone form **be** Tab-bar.
6. ⛔ **SHOULD `scroll-margin-top` BECOME A LIBRARY-WIDE RULE?** Every sticky region in this repo
   has the same defect latent in it and nothing gates it. The natural shape is a gate that fails
   any `position:sticky` ancestor whose in-page anchor targets carry no scroll-margin. A
   proposal, not a build.
7. **IS THE MASTHEAD CAP OF FOUR THE RULE?** The whole doormat shell rests on it, and the number
   is not measured from anything.
8. **SHOULD SPLITTER'S SEPARATOR GROW TO 44px?** Its `::before` is 24px on an inherited-restraint
   argument; every other control this repo ships is 44. And **should the `--axis` custom-property
   pattern go back into Splitter?** It is strictly more general than reading the attribute once.
9. **THE BRAND MARK.** 12 official SVGs, nothing binds them, row 86 is P1 / `ASSET-ONLY`. Carried
   from wave 5. ⚠ Two of this lane's shells make it bite harder: an **auth screen** is the most
   likely home for a real masterbrand lock-up, and a **64px rail head** is the hardest place in
   the library to put one.
10. **DOES A SHELL BELONG IN `knowledge/snippets/` AT ALL?** Carried from wave 5 unchanged. ⚠ The
    evidence FOR grew this lane: the grid gate caught a real off-grid value and P-1 caught a real
    schema violation, purely because these files sit where the gates look.
11. **`display:contents` ON THE PHONE BAND'S LISTS** — accepted with a declared AT risk and **no
    screen-reader test**. Worth a real device.
12. **THE BRAND IN INK RATHER THAN RED** in App-shell-focused, diverging from Navigations and
    App-shell-top-nav. Confirm or overturn.
13. **IS THE DOORMAT NAVIGATION OR END MATTER?** This shell says navigation — a stronger claim
    than Footer's own meta makes. If navigation, it arguably wants one `<nav>` around the whole mat.
14. **ALL DOMAIN PROSE IS PLACEHOLDER** (`s182-D2`): pane names, destination names, group names,
    the statement block. None is a semantic this lane may mint.

---

## 6 · BLAST RADIUS — the selectors this lane extended (lesson 6)

⛔ **Do NOT read this as a list of edits. No parent file was touched.** These are global
selectors whose *reach* now extends into four new files, which is the expected gate escape. The
conductor re-seeds; **this lane did not run `--update`.**

| selector | source | extended by |
|---|---|---|
| `.sh`, `.sh-skip`, `.sh-masthead`, `.sh-logo`, `.sh-nav`, `.sh-actions`, `.sh-menu`, `.sh-crumbs`, `.sh-main`, `.sh-foot`, `.sh-legal`, `.sh-scrim`, `.sh-sheet`, `.sh-sheet-head`, `.sh-sheet-body`, `.sh-close`, `.sh-panel`, `.sh-cols`, `.sh-title` | App-shell-top-nav (wave 5) | all four |
| `.bone`, `.bone.line`, `.bone.body`, `.bone.media`, `.bone.control` | Skeleton-loader | all four |
| `.sp`, `.sp-div`, `.grip` | Splitter | split |
| `.pb`, `.pb-head`, `.pb-label`, `.pb-value`, `.pb-track`, `.pb-fill` | Progress-bar | focused |
| `.ft-inner`, `.ft-mat`, `.ft-group`, `.ft-brand`, `.ft-legal`, `a.lnk`, `a.arrow`, `.tip`, `.lbl`, `.copy` | Footer / Links | doormat |
| `.sn-body`, `.sn-group`, `.sn-link`, `.sn-label`, `.si`, `.sn-foot` | Sidebar-nav | nav-rail |
| `.specimens`, `.spec-note`, `.visually-hidden` | the specimen convention | all four |

**Newly minted by this lane** (no prior reach, nothing to re-seed *from*): `.sh-split`,
`.sh-split-head`, `.sh-pane`, `.sh-pane-head`, `.sh-pane-body`, `.sh-col`, `.sh-card`,
`.sh-lede`, `.sh-exit`, `.sh-progress`, `.sh-actions-row`, `.sh-scroll`, `.sh-doormat`,
`.sh-sec`, `.sh-jump`, `.sh-inner`, `.sh-rail`, `.sh-rail-head`, `.sh-rail-brand`, `.sn-item`,
`.sh-fly`, `.sh-fly-label`, `.sh-fly-menu`, `.sh-body`, `.sh-head`.

---

## 7 · WHAT STAYS UNPROVEN — declared, not smoothed

1. **THREE OF THE FOUR THEMES ARE UNPROVEN FOR ALL FOUR SHELLS.** No `.cn-app-shell-*` block
   exists in `canon.css` (claim 9), so theme-cascade projection is silently OFF and **only the
   light and dark legs authored in each snippet have been seen. Console, Legacy and Supercharge
   have not been looked at.** The canon block is the conductor's.
2. **NO SCREEN READER WAS RUN**, and that matters more in this lane than in wave 5 because
   App-shell-nav-rail's central claims are *about announcement*. Roles, names, `aria-hidden`,
   `aria-expanded`, focus and inertness were measured programmatically; **nothing was heard.**
3. **`display:contents` ON A `<ul>`** has a history of dropping list semantics in older AT. Not
   tested. Declared in the meta, named again here.
4. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, outside this lane's fence. Same declaration wave 5 lane A made.
   **OWED.**
5. **`_validate_kg.py` was not run by this lane**, and the metas name contexts and patterns that
   do not exist as nodes (`context:nothing-this-is-the-outermost-frame`,
   `pattern:review-and-reconcile`, `pattern:authentication`, `pattern:marketing-and-product-pages`,
   `pattern:dense-back-office-application`, and the capability strings in every `accepts`). Every
   one is flagged rather than guessed. `gen_kg_edges.py` is the conductor's.
6. **THE CAPABILITY VOCABULARY IS INVENTED BY THIS LANE.** `site-navigation`, `page-content`,
   `overlay-panel`, `progress-statement`, `single-exit-control`, `end-matter`,
   `secondary-navigation`, `record-list`, `tabular-data`, `form-content`, `page-heading`,
   `ancestor-trail`, `summary`, `brand-mark`. `s140-D1` requires a capability and the schema
   accepts any string, so **nothing validated these against anything.** If a capability registry
   exists or should exist, this is fourteen unregistered strings. **Named, not smoothed.**
7. **Measured in ONE browser at ONE zoom** (headless Chromium, 1400/900/420, `deviceScaleFactor`
   1). No second engine, no zoom pass, no real touch device — which is a real gap for a
   component whose phone form is the thing under question.
8. **The Supercharge contrast figures Sidebar-nav and Navigations carry are NOT re-measured
   here.** Sidebar-nav's meta records `primary/border/default` on `tertiary/background/hover` at
   **3.89 light / 2.73 dark in Supercharge — a FAIL**. App-shell-nav-rail paints exactly that
   pair on its current-location mark. Quoted, not re-measured.
9. **The rail's phone-band truncation is a mitigation, not an answer** (claim 21, decision 5).
   The bar fits; four of five labels are unreadable.
10. **Nothing here has been seen by Dave**, and nothing is registered anywhere.

---

## 8 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. `.cn-app-shell-split`, `.cn-app-shell-focused`, `.cn-app-shell-doormat`,
   `.cn-app-shell-nav-rail` blocks in `canon/canon.css` — clears **4 of the 16** check-D failures
   and unblocks the three unseen themes for these files.
2. Re-run `gen_kg_edges.py` — the `ref: null` nodes named in § 7 item 5.
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` ·
   `_validate_radius.MIGRATED_SNIPPETS` registrations, **if** the four are kept.
4. ⚠ **THE OTHER 12 check-D FAILURES ARE SIBLING LANES'** — `Template-settings`, `Template-empty`,
   `Template-error`, `Template-report`, `Template-confirmation`, `Section-heading-lockup`,
   `Card-header-lockup`, `Hero-variants`, `Stats-band-lockup`, `Footer-doormat-lockup`,
   `CTA-lockup`, `Feature-grid-lockup`. Named here so they are not attributed to Lane A.
5. ⚠ **RUNNING THE GATES REWROTE TRACKED FILES, AND THAT IS DECLARED, NOT HIDDEN.**
   The four modified tracked files, read from `git status --short` rather than assumed, are
   `knowledge/_A11Y-GATE.md`, `knowledge/_SNIPPET-AUDIT.md`, `knowledge/_ICON-SOURCE-AUDIT.md`
   and `knowledge/_COMPOSE-AUDIT.md` — plus `knowledge/_state.json` (the doc rows, § 9) and
   `notes/_REHEARSAL-LOG.jsonl` (already dirty at lane open). ⚠ **`_GRAPH-REPORT.md` is NOT
   modified** — an earlier draft of this list named it from memory and the tree disagreed.
   These are a **side effect** of the gate runs in this receipt. **No lane edited them by
   hand**, and Lanes B/C/D ran the same gates, so attribution
   is **the wave's, not any one lane's**. ⛔ **Reconcile every path deliberately — never
   `git add -A`** [[feedback-worktree-reconcile-trail]].
6. **`knowledge/_state.json` is being written by four lanes concurrently.** This lane re-read it
   after its own write and confirmed its row landed intact (§ 9); a conductor-side re-read before
   commit is still owed.
7. ⚙ **FOLD THE `TMPDIR` POTHOLE INTO `_RUNBOOK-render-verify.md`** (§ 4). It is a *hang*, not an
   error, and it will cost the next lane two dead calls before they think to suspect it.
8. ★ **The `scroll-margin-top` gate proposal (decision 6)** is the one candidate in this lane
   that looks like a real instrument rather than a component decision.
9. ⚠ **Fourteen unregistered capability strings** (§ 7 item 6) entered the store this session in
   four metas. If capabilities are meant to be a controlled vocabulary, this is where to catch it.

---

## 9 · STORE DOC ROW

**Row: `W-83`** · owner `dave` · state `open` · condition `stated` · opened `210` ·
home `notes/_receipts/2026-08-20-210-wave6-laneA-p3-shells.md`

Minted at creation per [[forgotten-document-class]] via `knowledge/_state.py add()`. **The id was
derived from a LIVE RE-READ AT WRITE TIME, not from the brief's counts** — four lanes were writing
`_state.json` concurrently and `W-80`, `W-81` and `W-82` had already been taken by siblings
between this lane's first look at the store and its write. Had the id been chosen when the brief
was read, it would have collided.

**Confirming re-read, after the write:** `W-83` present exactly once · title and `home` intact ·
`W-8x` now reads `['W-80', 'W-81', 'W-82', 'W-83']` · `_state.check(doc)` → **ok=True, 0
failures**. ⚠ **A conductor-side re-read before commit is still owed** — the sibling lanes may
write again after this one.

`closes_when` names the four structural questions (§ 5 items 2–6) as well as the per-shell
promote/rework/delete calls, and explicitly carries the breakpoint scale and the
does-a-shell-belong-in-snippets question as **NOT closed by this lane**.
