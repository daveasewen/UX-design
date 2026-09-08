# 258-P — demo-chrome inventory across knowledge/snippets/*.reference.html

PROBE lane, read-only. 136 reference snippets scanned. **61 carry demo chrome**; **27 are DANGEROUS** (the component's own CSS or JS reads a demo var / demo element).

| slug | lines | chrome kinds | component rule reading a demo var/el | dangerous |
|---|---|---|---|---|
| Action-bar | 151 | demo-var | .action-bar-region | **YES** |
| Alert | 304 | demo-var | .awrap | **YES** |
| Amount-display | 153 | demo-class(col-demo) | — |  |
| Avatar-group | 356 | demo-class(demo-card,demo-h,demo-note) | — |  |
| Banner | 231 | demo-var | .bwrap | **YES** |
| Button | 311 | demo-var | .bar-wrap | **YES** |
| CTA-lockup | 230 | demo-var; demo-class(demo-col,demo-note,demo-stack) | — |  |
| Card-header-lockup | 308 | demo-class(demo-frame,demo-h,demo-note) | — |  |
| Cards | 232 | demo-var | .wrap | **YES** |
| Carousel | 327 | demo-var; demo-class(demo-h,demo-note) | .carousel | **YES** |
| Cascader | 642 | demo-class(demo-w); demo-comment | — |  |
| Confirmation | 139 | harness-label | — |  |
| Data-grid | 763 | demo-var; demo-JS(.dgseg button); harness-label; demo-comment | .dg | **YES** |
| Document-row | 447 | demo-var; demo-class(demo-h) | .wrap | **YES** |
| Drawer | 244 | harness-label | — |  |
| Feature-grid-lockup | 262 | demo-var; demo-class(demo-col,demo-note,demo-stack) | — |  |
| Filter-toolbar-bar | 473 | demo-var; demo-class(demo-col,demo-note,demo-stack) | — |  |
| Footer-doormat-lockup | 245 | demo-class(demo-note) | — |  |
| Footer | 324 | demo-class(demo-h,demo-note) | — |  |
| Hero-variants | 272 | demo-class(demo-h,demo-note) | — |  |
| Image-block | 221 | demo-var; demo-class(demo-h) | .grid | **YES** |
| Kpi-tile | 431 | demo-class(demo-h) | — |  |
| Layout-utilities | 388 | demo-class(demo-h,demo-note,l-demo) | — |  |
| Links | 152 | demo-var | .related | **YES** |
| List-items | 255 | demo-var | .wrap | **YES** |
| Meter | 785 | demo-class(demo-col,demo-frame,demo-stack); demo-comment | — |  |
| Notifications | 256 | demo-var | .nwrap | **YES** |
| Page-header-lockup | 452 | demo-var; demo-class(demo-col,demo-note,demo-stack) | — |  |
| Popconfirm | 393 | demo-var; demo-class(demo-h,demo-note,row-demo) | — |  |
| Progress-tracker | 301 | demo-var | .pt | **YES** |
| Qr-code | 736 | demo-comment | — |  |
| Range-slider | 132 | range-dial | — |  |
| Section-heading-lockup | 239 | demo-class(demo-frame,demo-h,demo-note) | — |  |
| Segmented-control | 294 | demo-class(demo-note) | — |  |
| Selection-controls | 338 | demo-var | .sc | **YES** |
| Skeleton-loader | 172 | demo-var | .skwrap | **YES** |
| Slider | 66 | range-dial | — |  |
| Splitter | 423 | demo-class(demo-box,demo-readout); demo-comment | — |  |
| Standing-order-mandate-row | 735 | demo-var; demo-class(demo-h) | .wrap | **YES** |
| Stats-band-lockup | 276 | demo-class(demo-frame,demo-h,demo-note) | — |  |
| Status-indicator | 231 | demo-var | .wrap | **YES** |
| Stepper | 480 | demo-var | .st | **YES** |
| Tab-bar | 164 | demo-comment | — |  |
| Table | 252 | demo-var; harness-label | .wrap | **YES** |
| Tabs | 262 | demo-var | .tabs | **YES** |
| Tags | 160 | demo-var | .filterbar | **YES** |
| Template-auth | 795 | demo-class(demo-note,demo-sec,demo-stack); demo-comment | — |  |
| Template-confirmation | 500 | demo-class(demo-bar,demo-h,demo-note); harness-label; demo-comment | — |  |
| Template-create-edit | 793 | demo-class(demo-frame,demo-note,demo-sec); demo-comment | — |  |
| Template-dashboard-bento | 1837 | demo-class(demo-bar); harness-label | — |  |
| Template-dashboard | 1086 | demo-var; demo-class(demo-bar); harness-label; demo-comment | ⛔ Data-grid's `.dg | **YES** |
| Template-detail | 703 | demo-var; demo-class(demo-bar); harness-label | Its `.wrap | **YES** |
| Template-empty | 487 | demo-class(demo-bar,demo-h,demo-note); harness-label; demo-comment | — |  |
| Template-error | 374 | demo-class(demo-bar,demo-h,demo-note); harness-label; demo-comment | — |  |
| Template-list-index | 944 | demo-var; demo-class(demo-bar,demo-h); harness-label | Its `.wrap | **YES** |
| Template-report | 945 | demo-class(demo-bar); harness-label; demo-comment | — |  |
| Template-settings | 899 | demo-class(demo-bar,demo-frame,demo-note); harness-label; demo-comment | — |  |
| Template-wizard | 797 | demo-class(demo-frame,demo-note,demo-sec); demo-comment | — |  |
| Timeline | 455 | demo-var; demo-class(demo-h); demo-comment | .tl | **YES** |
| Transaction-row | 494 | demo-var | .wrap | **YES** |
| Transfer-list | 236 | demo-var | .tl-frame, WAS: `.tl | **YES** |
## 2. How snippets are generated / maintained

* `knowledge/gen_component_partials.py` injects **only between existing marker pairs** —
  `AUTO-TOKENS` (from `gen_token_ramp.py`), `AUTO-PARTIAL <name>` (CSS), `AUTO-BEHAVIOUR <name>`
  (whole `<script>`), `AUTO-MARKUP <name>` (per-`<figure>`), `AUTO-BENTO` (canon.css grammar).
  Regex form: `(START marker)(.*?)(END marker)` — the file outside those spans is never rewritten.
* **Checked: no demo chrome currently sits inside any AUTO-* span** (scan of all 136 files, 0 hits).
  So a new fence placed around demo chrome CANNOT be clobbered by regeneration.
* `knowledge/gen_showroom.py` embeds the snippet **VERBATIM (base64) into an srcdoc iframe**, plus
  generated theme CSS and the review overlay. The showroom therefore keeps rendering the chrome as
  long as the bytes stay in the file — HTML comments are inert to it. It already honours a
  "strip from a marker onward" convention: `<!-- APOLLO-REVIEW-OVERLAY -->` onward is dropped
  before srcdoc.
* `knowledge/_validate_snippets.py` only parses `#token-manifest`; comments do not disturb it.
* Existing fence conventions to REUSE rather than invent: the `<!-- ===== AUTO-X <name> START … ===== -->`
  grammar, which `_validate_receipt.py` already borrowed for `APOLLO-SPLICE`; and the prose label
  precedent in the templates, `Reference harness — not part of the template`
  (`Template-dashboard.reference.html:609`).
* `--demo-width` is already typed as a RUNTIME var in `knowledge/_validate_compose.py:42`
  (`RUNTIME_VARS = {"--pct","--demo-width","--row-h"}`) and is set at runtime by
  `_render_links.py:32` and `_render_tags.py:13`. Moving it to a real default must keep that
  set working (an exception list, not a requirement — safe).

## 3. SKILL.md + the receipt gate

* `apollo-spider/skills/generate-from-canon/SKILL.md` rule 2 ("Copy the snippet, don't re-draw it",
  L46-49) and rule 2a (copy the snippet's own `<script>` verbatim, L50-61) are the two copy rules,
  and Procedure step 3 ("Drop each component in as its scope class + the snippet's own markup").
* **Insertion point:** a new sentence at the END of rule 2, before 2a — because rule 2 is the
  markup-copy rule and 2a inherits it: *"Never copy inside a fence: markup, CSS or script between
  `<!-- ===== APOLLO-DEMO … START ===== -->` and its END marker is showroom harness, not the
  component; a generated page containing a fenced marker is refused by the receipt gate."*
  Repeat one clause in 2a (the script fence) and one in Procedure step 3.
* **Gate:** `knowledge/_validate_receipt.py`, in `check(path)` (L629) after step 3
  (`REGION-UNRECEIPTED`). A marker-string check is enough:
  `re.search(r'APOLLO-DEMO[^\n]*(START|END)', html)` ⇒ `fails.append("DEMO-CHROME-COPIED")` with a
  named line `FAIL:DEMO-CHROME-COPIED — the page carries fenced snippet harness (<slug>); the fence
  is showroom-only, re-splice without it.` It sits naturally beside `splice_marker_start/end`
  (L185-193) and needs no parsing.

## 4. Proposed convention + apply plan

**Convention.** One marker grammar, borrowed verbatim from the AUTO-*/APOLLO-SPLICE family:
`<!-- ===== APOLLO-DEMO <what> START (showroom harness — never copy) ===== -->` … `<!-- ===== APOLLO-DEMO <what> END ===== -->`,
used identically in HTML, and inside `<style>`/`<script>` as `/* ===== APOLLO-DEMO <what> START … ===== */`.
Chrome CSS moves into ONE fenced block at the end of the snippet's `<style>` (after the AUTO-PARTIAL
block, so no injection span is disturbed); chrome JS moves into a SEPARATE fenced `<script>` at the
end of `<body>`, never mixed into the component's own script or an AUTO-BEHAVIOUR block; chrome
markup is fenced in place around the switcher/dial/bar. Demo-only vars the component READS are NOT
fenced — `.dg{width:var(--demo-width,760px)}` becomes `.dg{width:100%; max-width:var(--dg-max,760px)}`
(a real component default), and the harness sets the dial by writing that real var from inside the
fence. Rule: **after fencing, deleting every fenced span must leave a snippet that still renders the
component correctly** — that is the acceptance test for each file.

**Apply plan.** 61 snippets, 27 of them dangerous. Three parallel lanes, alphabetical:
* Lane A `Action-bar … Hero-variants` — 20 snippets, 8 dangerous
* Lane B `Image-block … Stats-band-lockup` — 20 snippets, 8 dangerous
* Lane C `Status-indicator … Transfer-list` — 21 snippets, 11 dangerous

**Do these 5 first (highest risk — the component reads the demo):**
1. `Data-grid` — `.dg{width:var(--demo-width,760px)}` (L144) + `.dgseg` state switcher (L322) + its
   click handler (L746); the actual cold-run defect.
2. `Template-dashboard` — 1086 lines, `.demo-bar`, inherits Data-grid's `.dg` width read.
3. `Template-list-index` — 944 lines, `.demo-bar` + `demo-h`, `.wrap` reads `--demo-width`.
4. `Table` — `.wrap` reads `--demo-width` and a `.seg` state switcher; the most-copied component.
5. `Standing-order-mandate-row` — 735 lines, `.wrap` reads `--demo-width`, harness-labelled.
(`Template-detail` is a close sixth.)
