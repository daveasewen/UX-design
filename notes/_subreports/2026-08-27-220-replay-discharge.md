# `#220`-replay-discharge — every `REPLAY-THESE` item from the #219 filed reports, replayed

session: `#220` · 2026-08-27
window: conductor's #220 verification lane
sub index: `replay-discharge`
brief: `notes/_briefs/2026-08-27-220-replay-discharge.md`
tokens: `UNMEASURED` — a sub cannot read its own `message.usage`; the conductor's panel is the
only honest reading of this lane's spend.

## VERDICT

**DONE.** All 21 #219 filed reports carrying a `REPLAY-THESE` section were enumerated and every
item in them replayed as written — **116 items** (four items were split where one bullet carried
several independently-checkable claims: seam 1's four verdict lines, seam 3's two CI reds, seam
5's three gate commands, N1's two ledger instructions). **Nothing was repaired, promoted or
ruled.** The repo working tree is byte-for-byte what it was when this lane opened (10 dirty
lines, none of them mine; see § THE TREE for the one self-inflicted write and its reversal).

The queue is in far better shape than the reports left it: the #219 release landed and cleared
its own designed reds. **79 GREEN · 12 RED · 25 COULD-NOT-RUN** — and 22 of the 25
could-not-runs are "put it to Dave" items, which no probe can discharge.

⛔ **One headline RED, and it is in a SHIPPED v1.0.0 release.** In
`apollo-spider/dist/Apollo-Spider-v1.0.0.zip`, the file
`memento-package/claude-plugin/memento/machinery/_gen_chain.py` **cannot import** —
`ModuleNotFoundError: No module named '_could_not_ask'`. Its sibling copy at
`memento-package/machinery/_gen_chain.py` runs. The two directories differ by **exactly one
file**, `_could_not_ask.py`, and the package delta gate is **GREEN** over the difference. This
is N3's finding-1 class, half-fixed, and it is precisely the argument N3's ruling-shaped Q1
makes for a RUN arm. Not repaired here.

COUNTS: items 116 · green 79 · red 12 · could-not-run 25

*(Counted mechanically off this file's own table, not by hand: 116 item rows, verdict cell
parsed, `green + red + could-not-run = 116`, no duplicate ids. The stub in chat is copied from
this line.)*

---

## ⓪ HOW THIS WAS DRIVEN — the premise checks that came first

**The tree.** `git log` reads `367b418` at HEAD with the whole #219 arc landed —
`801fe7c` (release stage 1) → `9ebd94c` (stage 2) → `416e1a6` (Spider stage 1) → `aa74faa`
(Spider stage 2) → `2f7c47b` (pre-bake seam) → `ce9e064` → `3fdaf35` (ratification) →
`ef44b1a` (THE BAKE) → `3b6824f` (post-bake ledger) → `aa26947` → `367b418`. **Every
"do not push before X" item in the queue is therefore a moment that has passed**, and was
graded on its outcome, not its instruction. [[premise-ages-faster-than-rule]]

**The render env is REAL, not assumed.** This is a fresh sandbox: `/var/tmp/chromelibs-s213e2`,
`/var/tmp/pw-browsers-215` and `/var/tmp/pylibs` — every foreign-session stratum the runbook
names — **do not exist here**. Rather than write COULD-NOT-RUN over six browser-bound items,
the runbook was read and the env re-staged from scratch:

```
pip install --target /var/tmp/pylibs playwright
PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-220 python3 -m playwright install chromium
curl ports.ubuntu.com/…/libxdamage1_1.1.6-1build1_arm64.deb ; dpkg-deb -x … /var/tmp/chromelibs-220
ldd …/headless_shell | grep "not found"        →  (nothing)
```

⚠ **`apt-get download libxdamage1` FAILS in this sandbox** (`E: Unable to locate package`; the
apt lists cannot be updated without root). The working move is a direct `curl` from
`ports.ubuntu.com/pool/main/libx/libxdamage/`. **This is a new sixth stratum for
`_RUNBOOK-render-verify.md` and is not in it** — recorded as a finding, not written (the runbook
is not this lane's region).

**The font control assert, per the runbook's own rule (never a boolean):**

| probe | reading |
|---|---|
| `HSBC_MtUnivers_Latin` | **300.48** |
| `"Univers Next HSBC"` (`--uf`) | **300.48** — alias resolves |
| `"Univers Next for HSBC"` (`--font`) | **300.48** — alias resolves |
| `DejaVu Sans` — control | 324.49 — genuinely different face |
| `"NoSuchFaceXYZ"` — control | 261.07 — absent face |

Target differs from **both** controls. The env is honest. Every verifier below then printed its
own font line independently: `font: target 347 = aliases 347/347, controls 375 (real) / 301 (absent)`.

---

## ① THE TABLE — 110 items, source · item · verdict · evidence

### `notes/_subreports/2026-08-25-219-enactA-rails.md` § 9

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| A1 | "Re-run `gen_bento_matrix_217.py --rails` at the reconcile … and re-run `--selftest` (bite `R6d` will red if the file is stale)" | **GREEN** | `⬛ EDIT-PASS RAILS written … rail [1, 2, 4, 16, 24, 40] · 9 dial(s)`; **dirty count unchanged either side ⇒ the manifest on disk already equalled a fresh generation.** `--selftest` `OK — 94 bites` |
| A2 | "Regenerate `showroom/_foundations/bento.html` …, then run `verify_bento_matrix_217.py` with no `--src` against the shipped page" | **GREEN** | `gen_foundations_217 --check OK — 8 page(s) in sync`; verifier: `OK — 4 state(s), three types driven, 7 dial(s) measured in pixels, both legality rules refused with reasons, export parity green, no dangling property` |
| A3 | "Reconcile finding 1 / Q6 (two homes for the ruled rail) and finding 3 (two readings of 'never tight') ACROSS the two lanes" | ⛔ **RED** | **Neither reconciled.** `gen_bento_matrix_217.py:189` still opens *"⛔ TWO NAMES, AND THE PAIR IS THE GATE"*, `:194-195` `RULED_SPACING_RAIL = (1,2,4,16,24,40)` / `SPACING_STOPS = list(...)`, while `role_defaults_219.py:73` independently declares `SPACING_STOPS = ["1","2","4","16","24","40"]`. Bite `R4c` gates the drift but **ADR-0017's one-home clause is not satisfied.** "Never tight": `gen_foundations_217.py:381` still carries *"⛔ THE DASHBOARD MAIN SPACING HAS NO TIGHT MEMBER"* against a matrix whose option space reaches 1px |
| A4 | "Put Q1–Q7 to Dave. Q1 and Q2 are the two that change what the product exposes." | **COULD-NOT-RUN** | Dave's, not a probe. Store proxy: **49 open `#219` rows, 30 owner=`dave`**; none of `s219-D1..D10` answers an enact-A question |
| A5 | "`gen_bento_matrix_217.py --selftest` # 73 bites, 19 new" | **GREEN** *(number superseded)* | Reads `94 bites`. enactC § 14 re-states the same command at **94** — enactA's 73 is the pre-chord figure and is history, not drift |
| A6 | "`verify_bento_matrix_217.py --src /var/tmp/bento-matrix-s219.html --themes mono,console`" | **COULD-NOT-RUN** | The `--src` target is a **foreign session's `/var/tmp` file** and this sandbox's `/var/tmp` holds only `cloud-init` + a systemd private dir. The binding check — the same verifier with **no** `--src`, against the shipped page — is A2 and is GREEN |

### `notes/_subreports/2026-08-25-219-enactB-defaults.md` § 9

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| B1 | "`role_defaults_219.py --selftest`" | **GREEN** | `OK — 12 exports parsed … ruled rails ['1', '2', '4', '16', '24', '40']` |
| B2 | "`role_defaults_219.py --table` — the twelve, as parsed" | **GREEN** | Twelve rows printed; e.g. `gallery console spacing=40 · keylines=off · mode=bento · edge=square · rounding=capsule · pageBg=transparent · bentoBg=transparent · capBg=grey` |
| B3 | "`gen_foundations_217.py --selftest` (39 bites, ~60s)" | **GREEN** | `OK — 39 bites. photography: 251 derivative(s) drawn · logos: 12 variant(s) drawn` |
| B4 | "`verify_photography_218.py --static`" | **GREEN** | `✅ verify_photography_218 OK` · `squared (s218-D6): 0 hole(s) over ladder (4, 3, 2, 1) — 251 tile(s)` · 5 over the 300 KB ceiling, **DECLARED RESIDUAL, unchanged** |
| B5 | "`verify_photography_218.py --themes mono,legacy`" | **GREEN** | `mono/light … cap ['rgb(240, 240, 240)'] ink ['rgb(26, 26, 26)'] · contrast 15.27` — the `s219-D2 (1)` light-grey caption ground, live |
| B6 | "`--themes console,supercharge`" | **GREEN** | `console/light … tileR [20] … cap ['rgb(240,240,240)'] · contrast 15.27`; `supercharge/light gutter 1px … contrast 17.45` |
| B7 | "`BM_MUTANT_DIR=… --break-default` then `… --default-mutation --themes mono,console`" | **GREEN** | `✅ MINTED-DEFAULT ARM RED AS REQUIRED — 2 SETTINGS CAPTION assertion(s) failed by name`, naming `dial says grey (--surface-subtle), resolved rgb(255,255,255)` |
| B8 | "⛔ Conductor action, cross-lane: finding 12 — `_bento_recut_219.py`'s ledger still states `s218-D6 (1)` as ruled and still paints the retired dark caption on three review pages" | **GREEN** — fixed | Ledger now reads `Q7 re-struck (s219-D2 (1) supersedes s218-D6 (1); the ground goes LIGHT GREY)`; the rider is quarantined as `RETIRED_MONO_CAPTION_218` with **bite 6b** failing if it is painted. On the pages the phrase survives **only as history**: `…s218-D6 (1) also records: "…#1A1A1A via --surface-digital-black…" …FROZEN HISTORY. s219-D2 (1) sa…` |
| B9 | "Dave's eye owed on `reviews/SQUARING-PORTRAIT-2026-08-25-v1.html` and the photography page in all four themes" | **COULD-NOT-RUN** | Dave's. Both surfaces exist and render; the four-theme readings are B5/B6 above |

### `notes/_subreports/2026-08-25-219-enactC-chords.md` § 14

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| C1 | "`gen_bento_matrix_217.py --selftest` (94 bites, C0–C9 are s219-D3's)" | **GREEN** | `OK — 94 bites` · `reachable console {'display': 48, 'gallery': 864, 'dashboard': 288} (total 1200)` |
| C2 | "`--rails` — after ANY option-grammar change" | **GREEN** | See A1; idempotent, no repo write |
| C3 | "`gen_foundations_217.py --selftest` then `--check`" | **GREEN** | `OK — 39 bites`; `--check OK — 8 page(s) in sync` |
| C4 | "`verify_bento_matrix_217.py --themes mono,console` — the s219-D3 chord and page-rail arms print their readings" | **GREEN** | `⬛ s219-D3 chords · dark caption ground · console OFFERS · mono/legacy/supercharge REFUSE with the open question printed`; `⬛ s219-D3(4) page rail · light · page ground rgb(255,255,255) == body rgb(255,255,255) · dark · rgb(26,26,26) == rgb(26,26,26) · one page-level control, survives the type switch` |
| C5 | "`--break-legality` then `--mutation …` — must report **11** falsifiable refusals, not 5" | **GREEN** | `⬛ MUTATION ARM — 11 legality assertion(s) went RED` — **exactly 11**, including `⛔ s219-D3(3)/X6 — mono reaches the dark caption ground. Mono's access is EXPRESSLY OPEN and nothing here may grant it` |
| C6 | "`verify_foundations_217.py --page bento-rails`" | **GREEN** | `OK — 8 state(s), no dangling property, theme reached the paint in all four` |
| C7 | "⛔ At the regen seam: run the ordered serial and let `gen_library_214.py` (index LAST) pick up the new Foundations entry, then `gen_thumbs.py` for `foundation-bento-rails`" | **GREEN** | `grep -c 'bento-rails' showroom/index.html` → **3**. The page is reachable from the library index |
| C8 | "Dave's eye owed on `showroom/_foundations/bento-rails.html` … Shots at `_to_delete/_shots219c/`" | **COULD-NOT-RUN** | Dave's. Page and shots dir both present |
| C9 | "Put questions 1–5 to Dave. Question 1 is the one `s219-D3(3)` expressly left him." | **COULD-NOT-RUN** | Dave's. The verifier confirms the question is still *printed on the page as open* (C4) — nothing has quietly settled it |

### `notes/_subreports/2026-08-25-219-lane1-segmented-adoption.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| L1-1 | "`reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html` — Dave's eye, ruling-shaped Q1 (open it, do not read it)" | **COULD-NOT-RUN** | Dave's. File present |
| L1-2 | "finding 1 (the `s202-D1` size restoration, ~400 tk)" | **GREEN** — enacted, confirmed | `layout.json` now carries `size/segmented-control/{xs,s,m,l,min-hit-area}` = **24 / 36 / 44 / 48 / 44**, and the generator resolves it live: `base_value('size/segmented-control/s','light') = 36px`. The `KeyError: 'size'` lane 1 recorded **does not reproduce** |
| L1-3 | "finding 6 orphan table (~500 tk)" — 47 orphans of 394 per-theme vars | **GREEN** *(one wired)* | ⚠ The preserved probe **cannot run as written**: `sweep.py:3` hardcodes `ROOT = "/sessions/pensive-cool-galileo/mnt/UX-design"` → `PermissionError`. Re-driven from a `/var/tmp` copy with ROOT repointed: `MINTED per-theme vars examined: 394` (unchanged) · `WITH ZERO CONSUMERS …: 46`. `comm` against the filed listing: **`--color-neutral-15` gained a consumer; nothing new became an orphan.** `--padding-card-internal` (finding 5) is still orphaned — `grep var(--padding-card-internal)` outside `reviews/` returns nothing |

### `notes/_subreports/2026-08-25-219-lane3-review-regen.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| L3-1 | "`notes/_subreports/assets/…/name-check.txt` (~450 tk)" | **GREEN** — reproduced verbatim | Re-derived independently from `gen_bento_roles_217.SPECIMEN_FILES` (n=15): `all 15 files present on disk: True`; and, line for line identical to the filed asset — `BENTO-CANON-2026-08-23-v2.html srcs=30 unique=15 exact-set-match-to-PIN=True off-pin=none` · `-v3.html srcs=54 unique=15 True none` · `GALLERY-COMPARE-2026-08-23-v1.html srcs=60 unique=15 True none` |
| L3-2 | "finding 6 + RULING-SHAPED question 1 above (~350 tk)" | **COULD-NOT-RUN** | Dave's (lane 3's item 8, the v4/v5 series cut, was a filename question and is moot — v4…v7 all exist) |

### `notes/_subreports/2026-08-25-219-lane4-dv16.md` § 7

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| L4-1 | "1. `verify_dv_d16_render.py --target all` — ~90 s" | **GREEN** | Four blocks, all `GREEN (0 failures)`: STATIC+RENDER over the showroom target and over `snippets/Chart-bar.reference.html`. `no stacked rect declares its own timing (wording ① cannot come back unseen)` · `REDUCED-MOTION: 16 rects rest at full height` · `JS-OFF: 16 rects rest at full height` |
| L4-2 | "2. `apply_dv_d16_region_219.py --selftest` — **Run this before ever regenerating the pro-forma**" | **GREEN** | `SELFTEST GREEN — transplant output is byte-identical to the generator's (102798 bytes)`. Writes go to a temp dir outside the repo |
| L4-3 | "3. `_verify_dv_stacked_enactment.py` — ~40 s" | **GREEN** | `ALL ASSERTIONS PASS`; `snippet@1180 … (b) worst contrast= 4.61:1 over 12 on-fill keys` — matching the standing `series-3 4.61:1` reading at all four cells |
| L4-4 | "⚠ Shared-tree note … **verify all three ids are present before the seam commit**" (`W-174`/`W-175`/`W-176`) | **GREEN** | All three present. `W-174` → `knowledge/_render/apply_dv_d16_region_219.py`; `W-175`/`W-176` → the lane-4 report. **No row was dropped by the concurrent writer** |

### `notes/_subreports/2026-08-25-219-lane5-unconsumed-mints.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| L5-1 | "`reviews/UNCONSUMED-MINTS-2026-08-25-v1.html` — **open it, do not read it**; Rows A and B are Dave's eye" | **COULD-NOT-RUN** | Dave's. File present. The gate behind it re-drives clean: `minted-token consumption inventory (ADVISORY) — canon.css declares 973 custom properties (base tier 972 · theme tier 394) · consumed 600 · unconsumed 373` and `✅ selftest PASS … (10 bites)`. **Left ADVISORY, per the brief** |
| L5-2 | "ruling-shaped Q1 and Q2 (~600 tk)" | **COULD-NOT-RUN** | Dave's. The gate's own footer says it: *"Promotion to blocking needs a `$consumer`/`$reserved` declaration on the token, and is Dave's word"* |
| L5-3 | "finding 7, the stale `s149-D1` status (~120 tk, conductor's to correct or leave)" | ⛔ **RED** — still stale | `_rulings.json` `s149-D1.status` still reads *"RULED #149, **NOT ENACTED**. No value moved in any token or canon file. Enactment is #150 lane 1…"* while the enactment is live at `Tabs.reference.html:107`: `/* round badge — s149-D1 re-point off --tabs-active/--text-reverse onto its own badge seat */`. **The conductor's "correct or leave" was neither done nor recorded.** [[conclusions-are-debt-s129-d5]] in the ruling store itself |

### `notes/_subreports/2026-08-25-219-seam1-reconcile.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S1-1a | §③ "`[40] gen_token_ramp: 0 file(s) DRIFTED …, 147 already in sync. rc=0`" | **GREEN** | Reproduces **character for character** |
| S1-1b | §③ "`[45] gen_canon_components --check OK — 135 components in sync. rc=0`" | **GREEN** | Reproduces character for character |
| S1-1c | §③ "`[50] gen_theme_cascade --check OK — 230 override path(s), 387 component projection(s) in sync. rc=0`" | **GREEN** | Reproduces character for character — **387**, seam 1's own corrected figure |
| S1-1d | §③ "`[107] memento index --check: current (1791 records) rc=0`" | ⛔ **RED IN THE TREE — GREEN AT HEAD, PROVEN** | Reads `memento index --check: STALE — regenerate`, `rc=1`. **Attribution driven, not guessed**: `build_records()` in-process vs the index on disk → `NEW in fresh (3): ['brief:2026-08-27-220-charts-sparkline', 'brief:2026-08-27-220-readings-capsule-correction', 'brief:2026-08-27-220-replay-discharge']` · `GONE from fresh (0): []`. The corpus includes `notes/_briefs/*.md` (`_build_memento_index.py:333`), so **the three untracked #220 briefs — one of them this lane's own — are the entire cause.** Zero records lost. ⇒ conductor action below. *(Record count is 1796 on disk, not seam 1's 1791: five later #219 sub-reports.)* |
| S1-2 | "the blast-radius HEAD/WORKTREE matcher readings … ⛔ STILL RED" | **GREEN** — the red is cleared | `✅ type-binding blast-radius gate passed (27 appended selector(s), corpus 149 files)`, with `[PASS] scoped-element .search input (4)`. Cleared at **`416e1a6`**: `git show` on the gate doc is `-\| 5 \| … \`.search input\` \| FAIL·escaped \|` → `+\| 4 \| … \| PASS \|`. The radius went **back to 4** — the escaping match was removed at cause, not `--update`d away |
| S1-3 | "§① the UNCLAIMED pair with its writer evidence (~150 tk)" | **COULD-NOT-RUN** | The pre-commit worktree it describes no longer exists; that tree landed at `d178313` |
| S1-4 | "**Q1**, or a deliberate decision to commit with `_validate_type_blast_radius.py` red" | **GREEN** — moot | The gate is green (S1-2); the choice was taken by fixing, not by deciding to ship red |
| S1-5 | "`_capture_gate.py --selftest` — 3 failures, ALL THREE PRE-EXISTING AT HEAD" | **GREEN** — reproduces exactly | `capture gate [wrap]: 5 in scope · 4 fail · 2 warn` **verbatim**, and exactly three `❌ selftest:` lines, same names: `M10: a fat §A/§C warned the CHAIN`, `M10: an ordinary chain warned — the budget fires on everything`, `#70/#71 non-catch: _gen_chain.py --selftest is NOT green`. Confirmed downstream: `_gen_chain.py --selftest` → `✗ _gen_chain selftest: 1 bite(s) failed` (while `--check` is green — it is the SELFTEST that is red). ⚠ **These three are UNFIXED and still ruling-shaped.** Repo integrity: `notes/_REHEARSAL-LOG.jsonl` md5 identical either side — the gate wrote nothing |

### `notes/_subreports/2026-08-25-219-seam2-reconcile.md` § ⑧

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S2-1 | "REPLAY-THESE from lane 4 … were driven at this seam and are green — items 1 and 2" | **GREEN** | Re-driven here: L4-1, L4-2 |
| S2-2 | "Item 3, `_verify_dv_stacked_enactment.py` (~40 s), was **not** re-driven here … lane 4's own run is the standing reading" | **GREEN** — no longer standing on lane 4's word | Re-driven here first-hand: L4-3, `ALL ASSERTIONS PASS` |
| S2-3 | "Cite both filed reports BY PATH in the `#219` receipt" | **COULD-NOT-RUN** | The conductor's, and the commits it applies to have landed |

### `notes/_subreports/2026-08-25-219-seam3-reconcile.md` § 7

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S3-1 | "Lane 5's five questions + REPLAY-THESE: `UNCONSUMED-MINTS-…-v1.html` — open it, do not read it" | **COULD-NOT-RUN** | Dave's |
| S3-2 | "Lane 6's Q1 (memento-package mirror), Q2 (a session that wrapped TWICE), Q3 (three CERTAIN `dv-empty-frame` findings + promotion)" | **COULD-NOT-RUN** | Dave's. Q1's *subject* has moved — see S3-4a |
| S3-3 | "The `s149-D1` status field, above" | ⛔ **RED** | Duplicate of L5-3; the same probe, still stale |
| S3-4a | "⚠ Both CI reds `[120]` and `[18]` will still be red after this commit" — **[120]** `_validate_package_delta.py` | **GREEN** — no longer red | `memento-package delta-audit: 0 failure(s)` · `✅ VERBATIM SET byte-identical (both copies) · shim provenance clean (both chains) · copies identical to each other · no unknown files`. ⚠ **This green is exactly the green N3's Q1 warns about** — see N3-3 |
| S3-4b | "… **[18]**" `_gm_usage.py --selftest` | ⛔ **RED** — still red, at cause | `rc=1` · `✗ real-repo usage history reads clean (got: ['session #218 testifies DIFFERENTLY in notes/_GAUGE-LOG.md and notes/_GAUGE-LOG.md — one of them is false and this reader cannot tell which. REFUSED.'])` · `✗ real-repo report closes in exactly ONE of its two legal states`. **Lane 6's diagnosis reproduces unchanged: `#218` wrapped twice. Ruling-shaped** |
| S3-5 | "UNPROVEN: `_build_all.py` end-to-end … CI delivers that verdict on push" | **COULD-NOT-RUN** | Sandbox-impossible by the brief's own rule (never run partially; a full run does not fit a call). CI-bound: **no `gh`, GitHub API 404s unauthenticated.** Stays the conductor's |

### `notes/_subreports/2026-08-25-219-seam5-reconcile.md` § 12

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S5-1 | "`_bento_recut_219.py --selftest` — the 3 new bites are the finding-12 gate" | **GREEN** | `_bento_recut_219 selftest OK (8 bites) — struck/open per page: canon 6/3 · roles 8/1 · compare 9/3` |
| S5-2a | "`_gen_chain.py --check`" | **GREEN** | `✅ _CHAIN.md is FRESH — byte-matches the live chain · … FILE 45,918 real = slice 30,339 + wrapper 15,579 · fixed point in 2 pass(es)` |
| S5-2b | "`_state.py --selftest`" | **GREEN** | `_state selftest: 57 bites, all GREEN` |
| S5-2c | "`_gate_doc_rows.py --check`" | **GREEN** | `✅ PASS — every in-scope document has a store row` · `population 96 … unrowed 0` |
| S5-3 | "`gen_foundations_217.py --check` — must read `7 page(s) in sync`" | **GREEN** *(number superseded)* | Reads **`8 page(s) in sync`**. Cause named: `showroom/_foundations/bento-rails.html` was added by lane C at `71bb2f7`, **after seam 5 filed**. The gate's own subject — sync — holds |
| S5-4 | "Dave's eye owed on FOUR new pages: `BENTO-CANON-…-v6`, `-v7`, `GALLERY-COMPARE-…-v3`, `SITTING-219-…-v2`" | **COULD-NOT-RUN** | Dave's. All four present |
| S5-5 | "Put to Dave: enact-A Q1–Q7 and enact-B Q1–Q7 (fourteen), the two rotted Dave rows, and the four un-indexed questions" | **COULD-NOT-RUN** | Dave's. `W-181`/`W-184` (the sitting index, *"33 open calls"*) are both still `open`, owner `dave` |
| S5-6 | "⛔ The one that changes the most if he says yes: enact-B **Q1** — flipping `layout/bento/$roles/gallery/squaring` to `true`" | ⛔ **RED / STILL OPEN** | `layout/bento/$roles/gallery/squaring = **False**` (dashboard `True`, brochureware `True`). And the three pages seam 5 named are still waiting on the word: `declared divergence` present in `BENTO-CANON-2026-08-25-v7.html`, `GALLERY-COMPARE-2026-08-25-v3.html`, `SITTING-219-2026-08-25-v2.html` |

### `notes/_subreports/2026-08-25-219-seam6-reconcile.md` § 11

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S6-1 | "The tree is prepared and NOT committed … `git status --porcelain \| wc -l` → **22** is the number to re-read before staging" | **COULD-NOT-RUN** | The staging moment has passed; that tree landed at `71bb2f7` |
| S6-2 | "⛔ `W-99zs`'s close condition is HALF met … The row is correctly still `open`; do not close it on the index alone" | **GREEN** | `W-99zs` `state: open`, `owner: dave`, home `showroom/_foundations/bento-rails.html`. **Index half satisfied and quoted** — `grep -c bento-rails showroom/index.html` → 3. Dave's eye still owed, exactly as the row says |
| S6-3 | "⛔ A store row was minted by this seat: `W-186` … do not double-mint" | **GREEN** | `W-186` present, once, homed at the seam-6 report |
| S6-4 | "`_CHAIN.md` was regenerated and must be staged **with** `_state.json`" | **GREEN** | Chain is FRESH against the current store (S5-2a) — the pair did land together |
| S6-5 | "⚠ Re-run `_gen_chain.py` once more AFTER any further store write" | **GREEN** | Chain FRESH at HEAD across every store write since |
| S6-6 | "Put lane C's five ruling-shaped questions to Dave, untouched" | **COULD-NOT-RUN** | Dave's; = C9 |
| S6-7 | "Dave's eye owed … `bento-rails.html` … Shots at `_to_delete/_shots219c/`" | **COULD-NOT-RUN** | Dave's. Page + shots dir present |
| S6-8 | "New for his eye: on a **supercharge** page the page-ground cards print mono's hexes over supercharge's ramp" | **COULD-NOT-RUN** | Dave's. The verifier does read supercharge's own ground correctly on the shipped Foundations page (`supercharge/light ground rgb(247,246,244) ink rgb(19,17,14) contrast 17.45`), so the divergence is page-local, as seam 6 said |
| S6-9 | "`knowledge/_consult-index.json` is **in** the tree, regenerated and idempotent" | **GREEN** | Full regeneration run; `git status --porcelain knowledge/_consult-index.json` → **empty**. Byte-identical. Inventory: `rule 470 · open-item 105 · ruling 63 · defect 54 · gate 43 · assertion 8` |

### `notes/_subreports/2026-08-26-219-N1-snoopy-rename.md` § ⑧

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| N1-1 | "`_gate_release_audit.py --check` is RED and `--selftest` is 8/1, BY DESIGN … Do not push before it is cleared" | **GREEN** — cleared | `PASS — the manifest at knowledge/_release/_pack_manifest.json is byte-identical to a fresh generation at 2f7c47bb904b (1610 files, sha256 a8c3c961fc722329)`; `selftest: 8 bites, 0 fail(s)` |
| N1-2 | "STAGE 2 … `python3 knowledge/_make_review.py …`" | ⛔ **RED on the recipe line** | **`knowledge/_make_review.py` does not exist.** `find . -name '_make_review.py'` → `./knowledge/_review/_make_review.py`, one hit. Both N1 § ⑧ and seam 8 § ⑧ carry the wrong path; R2's version of the same item cites it correctly. A conductor following N1's block verbatim gets `No such file or directory`. *(Not repaired — reports are frozen history, ADR-0017.)* |
| N1-3 | "Expected: 1,594 paths … fonts 54, skills 5, ci-template 3, all under `apollo-snoopy/`" | **GREEN** *(count superseded, cause named)* | Manifest totals: **1610 files** · fonts **54** ✓ · `SKILL.md` under the pack **5** ✓ · ci-template **3** ✓ (`apollo-spider/ci-template/{README.md,gates.yml,run-gates.py}`) · **zero** `apollo-snoopy`/`designer-skills-v3` paths. The delta is exactly one group: `gumdrop` = **18 files** (N3's cold start), 1592 + 18 = 1610. Prefix is `apollo-spider/` — `s219-D8` superseded the Snoopy name |
| N1-4 | "The two generated artefacts are STALE ON DISK and were deliberately NOT regenerated" | **COULD-NOT-RUN** | The stale-on-disk state was stage 1's; stage 2 regenerated at the landing commit and the audit is green over it |
| N1-5a | "**Do not drop `renamed_from`**" | **GREEN** | `_frozen-releases.json` third row carries `"renamed_from": "designer-skills-v3"` |
| N1-5b | "and do not re-seed the whole ledger at HEAD — that would move `baseline_commit` on v1 and v2 and light the laundering arm for both" | ⛔ **RED — the instruction was breached AND its prediction was wrong** | The whole ledger **was** re-seeded at the bake commit: at `2f7c47b` `seeded_at: 71bb2f77ff59` with all three baselines `71bb2f77ff59`; at HEAD `seeded_at: ef44b1a…` with **all three moved to `ef44b1a`**. Yet the gate is `PASS — 3 arm(s) asked, no frozen surface moved` and **no** laundering line fired. Cause: the laundering arm keys on `content_sha256` (v1 `b83d048483b7` and v2 `e1d8019b97cc` are unchanged), **not** on `baseline_commit`. ⇒ **the warning names the wrong mechanism**, and a future seat obeying it would be protecting against the wrong thing |
| N1-6 | "`knowledge/canon/canon.css` in the tree is N2's content, materialised by my run" | **COULD-NOT-RUN** | Pre-commit tree state; landed. Downstream proxy is green: `gen_token_ramp`/`gen_canon_components`/`gen_theme_cascade` all `in sync`, canon.css clean |
| N1-7 | "Store ids: `W-191` and `W-192` … The `W-99z*` range is still exhausted" | **GREEN** | Both present (`W-191` → `_gen_pack_manifest.py`, `W-192` → the N1 report). `W-99z*` count 27 |
| N1-8 | "N2's `W-189` handoff is DONE except for its verdict … Its 35-pass figure needs N2's `--check` arm in the commit — read it at stage 2" | **GREEN** — read | Driven from the **shipped zip**, extracted to `/var/tmp/packrun`: `35 pass · 0 FAIL · 0 could-not-ask`, exit 0 |

### `notes/_subreports/2026-08-26-219-N2-four-reds.md` — handoffs

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| N2-1 | "HANDOFF 1 … make it `(gate, path, argv)` and have `run_one()` call `[sys.executable, path] + argv`" | **GREEN** — enacted verbatim | `run-gates.py:93` `def run_one(path, cwd, pack, timeout, argv=()):` · `:97` `r = subprocess.run([sys.executable, path] + list(argv), …)` · `:151-152` `for name, path, argv in gates:` The argv is **declared in the manifest**, not hand-edited: `_validate_hit_area.py -> --all`, `_validate_type_composites.py -> --check` |
| N2-2 | "⚠ **Do NOT hand the runner `--ratchet` instead.** It rewrites `_type_ratchet.json` in the designer's checkout" | **GREEN** — honoured | The declared invocation is `--check`. `git status --porcelain` on `knowledge/_type_ratchet.json` after a full pack run → **empty** |
| N2-3 | "HANDOFF 2 — the manifest is STALE against N1's own rename … Re-probe + re-generate at the landing commit" | **GREEN** | Manifest `version: v1.0.0`, `commit: 2f7c47bb904b…`, `pack: Apollo — Spider`; **zero** `designer-skills-v3` paths. The eight missing paths N2 measured are all present, at the new prefix |
| N2-4 | "HANDOFF 3 — the pack runner has THREE verdicts; the repo has FOUR … the same shape as R2's un-enabled `--baseline` (its Q4), and the two should be answered together" | ⛔ **RED / STILL OPEN** | Still three: `35 pass · 0 FAIL · 0 could-not-ask`. No ADVISORY bucket in the pack runner. Costs nothing today (the evidence linter refuses with 77 because `notes/` is not shipped) — **named, not decided, and it should be put to Dave beside R2's Q4** |
| N2-5 | "HANDOFF 4 — the `s219-D7` rename has ORPHANED THREE STORE ROWS' home pointers" | **GREEN** — all three repointed | `_state.check()` → `home pointers: 253 resolve by ANCHOR (rot-proof), 17 are still 'path:line', **0 UNRESOLVABLE**`. `W-99zt` → `knowledge/_release/_pack_manifest.json`, `W-99zv` → `apollo-spider/skills/`, `W-99zy` → `apollo-spider/ci-template/` — repointed to the **Spider** paths, not N2's proposed Snoopy ones |

### `notes/_subreports/2026-08-26-219-N3-gumdrop-coldstart.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| N3-1 | "`apollo-spider/FIRST-SESSION.md` (~2,600 tk — it is the deliverable and it is PROPOSED text)" | **COULD-NOT-RUN** | Dave's. Present in the repo and shipped in the zip as `Apollo-Spider-v1.0.0/FIRST-SESSION.md`; the page's unzipping note names it (2 hits) |
| N3-2 | "ruling-shaped question 1, the delta gate's missing RUN arm (~400 tk — it is the finding most likely to recur)" | ⛔ **RED / STILL OPEN — and it recurred** | `_validate_package_delta.py` still has **four** arms and no run arm: `grep -c 'ImportError\|importlib\|AttributeError'` → **0**. Its green print names exactly what it checks: *"VERBATIM SET byte-identical (both copies) · shim provenance clean (both chains) · copies identical to each other · no unknown files"* — nothing about whether either copy **runs** |
| N3-3 | "finding 1 + finding 9 (~900 tk — **the released package is affected** and the re-sync may need repeating at the seam)" | ⛔ **RED — HEADLINE, IN THE SHIPPED ZIP** | Driven against the extracted release. Import-probe of every machinery file in both copies: **11 OK, 1 ERR** — <br>`ERR claude-plugin/memento/machinery/_gen_chain.py :: ModuleNotFoundError: No module named '_could_not_ask'`<br>Run as a designer would: `python3 _gen_chain.py --check` in that dir → traceback at `_gen_chain.py:68`, `import _could_not_ask as cna`. The sibling copy, same invocation, runs and refuses honestly: `✗ _CHAIN.md check FAILED — GOOD-MORNING.md is missing`. `diff` of the two dir listings is **one line**: `< _could_not_ask.py`. In the repo **neither** copy carries it (`find . -name '_could_not_ask.py'` → `knowledge/` and `apollo-spider/gumdrop/machinery/` only) — the bake supplies it into `memento-package/machinery/` from the gumdrop group and **not** into the plugin copy. Not repaired |
| N3-4 | "⚠ One thing the seam must decide … the pack README still says *'Memento's machinery, and only the machinery. No chain, no rulings, no record of any kind.'* **It must be corrected before the bake**" | **GREEN** — corrected in all four surfaces, verified in the bake | `build-designer-pack.sh:256` now reads *"`memento-package/` — **Memento — Gumdrop v1.0.0**: Memento's machinery, plus the cold start. … The record it ships is **empty on purpose**"*. In the extracted zip: `grep -rl "no record of any kind" .` → **nothing**; `_MANIFEST.json` and `PROVENANCE.json` both carry the corrected `carries.what` |

### `notes/_subreports/2026-08-26-219-R1-v3-manifest.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| R1-1 | "The **four page questions** are Dave's go/no-go … the script enforces that mechanically (`status: PROPOSED` ⇒ `--release` refuses)" | **GREEN** — all ruled | Manifest `status: RATIFIED — s219-D10, Dave's word 'bake' (2026-08-26); s219-D4(2) satisfied by the store, not by prose`. Every card answered: Q1–Q5 → `s219-D5 (Qn)`, Q6 → `s219-D9` |
| R1-2 | "**Q5 and Q6 are not on the page** — if the conductor wants them in front of him, regenerate after adding them to `OPEN_QUESTIONS`" | **GREEN** | Six cards on the page, Q5 (*"Four of the packed gates are RED the day the pack is unzipped"*) and Q6 (*"Answering Q5 quietly took two gates OUT of the pack"*) both present and both ruled |
| R1-3 | "The manifest is a **function of the commit** … `--manifest` must be re-run at the new commit or `--dry-run` refuses on the mismatch" | **GREEN** | Re-run and byte-identical at `2f7c47bb904b` (N1-1) |
| R1-4 | "The v2 receipt's flag repeats here: the pack's contents are only as fresh as the commit named" | **GREEN** — and the gate says so unprompted | `ADVISORY — the manifest was generated at 2f7c47bb904b; HEAD is 367b41822764, 6 commit(s) later. … ⬛ WHETHER TO RE-CUT IS DAVE'S (s219-D4(2))` |

### `notes/_subreports/2026-08-26-219-R2-release-ci.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| R2-1 | "Re-run `--probe` + `--manifest` at the landing commit … the three ci-template files enter the ship list only from that commit" | **GREEN** | Three ci-template paths in the manifest; `_gate_ci_template.py --check` → `PASS — the template parses, ships what it calls, and hides nothing` (`2 job(s), 1 referenced script(s), README present`; actionlint absent and **declared**, not silently skipped) |
| R2-2 | "The ledger does not need re-seeding to land … Expect one `COULD-NOT-ASK` line from the laundering arm on the landing commit itself" | **GREEN** *(prediction not met, harmlessly)* | `PASS — 3 arm(s) asked, no frozen surface moved` — **zero** could-not-ask. The ledger *was* re-seeded (N1-5b), which is why the arm had a baseline to ask against |
| R2-3 | "**Q1 wants a card on Dave's page**, not just a line in this report — four gates arriving red is the kind of thing that gets discovered by a designer" | **GREEN** | It became Q5 on the page and was ruled `s219-D5 (Q5)`; the follow-on (two gates removed) became Q6 / `s219-D9` |
| R2-4 | "**R3's `W-99zv` line-number citations are stale** … re-derive the repoint targets by name" | **GREEN** | `W-99zv`'s home is now the anchor `apollo-spider/skills/`, not a `path:line` |
| R2-5 | "After any `build-designer-pack.sh --dry-run`, re-run `_make_review.py reviews/RELEASE-V3-MANIFEST-*.html` — the bake rewrites the page and strips the review pair's stamps" | **GREEN** *(filename superseded)* | No `RELEASE-V3-MANIFEST-*` remains — the pair is `RELEASE-SPIDER-2026-08-26-v1.html` + `.REVIEW.html`. **The pair is intact at HEAD**: the clean page carries `APOLLO-REVIEW-OVERLAY` **0** times, the `.REVIEW.html` **2**, with `rv-file content="reviews/RELEASE-SPIDER-2026-08-26-v1.html"` pointing back at the clean source. The bake was **not** re-run by this lane |

### `notes/_subreports/2026-08-26-219-R3-skills.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| R3-1 | "**Q1 is blocking the bake.** Until `_gen_v3_manifest.py:284` is repointed, `--manifest` at any commit ships v2's four skills and not these five" | **GREEN** — repointed, generator renamed | `knowledge/_release/_gen_v3_manifest.py` **no longer exists**; it is `_gen_pack_manifest.py`. The manifest ships the **five**: `apollo-spider/skills/{check-against-design-system,check-with-gates,draft-a-new-pattern,generate-from-canon,usability-review}/SKILL.md`, and **no** v2 skill |
| R3-2 | "The manifest must be re-run at the commit that carries these files" | **GREEN** | At `2f7c47b`, audit byte-identical |
| R3-3 | "**Q3** (empty `_proforma`/`_fitness-test` + READMEs) pairs naturally with R1's Q1 … Worth putting to Dave together" | **COULD-NOT-RUN** | Dave's. R1's Q1 was ruled (`s219-D5 (Q1)`, empty stores ship); **R3's Q3 has no matching ruling** and should travel with it |
| R3-4 | "**Consequences replayed (Dave #165):** if the skills ship without Q2's path rewrite, designers get a `designer-skills-v3/` folder inside `Apollo-designer-skills-v3.0.0/` and most will not find the skills at all" | **GREEN** — flattened | In the shipped zip the skills sit at `Apollo-Spider-v1.0.0/skills/…`, one level. Top-level dirs are exactly `.github, ci-template, knowledge, memento-package, showroom, skills` — no nested pack folder |

### `notes/_subreports/2026-08-26-219-seam7-reconcile.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S7-1 | "⛔ `release-audit --check` and `--selftest` are RED at the landing commit and stay red until stage 2 … do not push before stage 2" | **GREEN** — cleared at stage 2 | N1-1 |
| S7-2 | "Expected ship-list size after stage 2: **1,594 paths** … If `--manifest` produces a different number, something else moved" | **GREEN** *(and something else did move — named)* | 1610. The mover is the `gumdrop` group, 18 files, added between seam 7 and the bake. The item's own instruction — find out what moved — is discharged |
| S7-3 | "**`check-with-gates` is now the settled name** … It is no longer a question" | **GREEN** | Ships as `apollo-spider/skills/check-with-gates/SKILL.md`, in the repo and in the zip |
| S7-4 | "**R3's Q2 is still open and is the loudest unanswered one** … a one-line path rewrite in the stager and it was **not** made this seam" | **GREEN** — made at stage 2 | = R3-4 |
| S7-5 | "**The `W-99z*` id range is exhausted.** Twelve #219 rows sort after every numeric row" | **GREEN** *(count superseded)* | **17** `W-99z*` rows carry `opened: 219` (27 in the range overall). Five more were minted after seam 7 |
| S7-6 | "**Dave's open questions are now five, not four**" | **GREEN** *(count superseded, upward then closed)* | Six cards shipped, and **all six are ANSWERED** |

### `notes/_subreports/2026-08-26-219-seam8-reconcile.md` § ⑧

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S8-1 | "`_gate_release_audit.py --check` is RED and `--selftest` is 8/1, BY DESIGN … Do not push before it is cleared" | **GREEN** — cleared | N1-1 |
| S8-2 | "The three generated artefacts are STALE ON DISK and were deliberately RESTORED to that state after the bake" | **COULD-NOT-RUN** | Pre-commit state, superseded by stage 2. The reasoning held: the audit is green at a **real** commit, not a dangling one |
| S8-3 | "STAGE 2 … **Expect 1,592 paths**, fonts 54, skills 5, ci-template 3, all under `apollo-spider/`; probe `35 RUNNABLE · 3 NEEDS-DEP · 9 REPO-BOUND`; the pack's own runner `35 pass · 0 FAIL · 0 could-not-ask`, exit 0. **The fifth card's four gate names should be re-read**" | **GREEN** on every reading but the count | Probe artefact: `Counter({'RUNNABLE': 35, 'REPO-BOUND': 9, 'NEEDS-DEP': 3})` — **exact**. Pack runner, driven from the shipped zip: `35 pass · 0 FAIL · 0 could-not-ask`, exit 0 — **exact**. fonts 54 ✓ skills 5 ✓ ci-template 3 ✓ prefix `apollo-spider/` ✓. Count 1610, not 1592 (N1-3). Q5's card is ruled, and `Q5_RED_GATES` is bitten for existence, which the 165-bite selftest confirms |
| S8-4 | "**Do not drop `renamed_from` and do not re-seed the whole ledger at HEAD**" | ⛔ **RED** | = N1-5b. `renamed_from` survived; the whole-ledger re-seed happened anyway, at `ef44b1a` |
| S8-5 | "The § ⑤ fix is a change to four canon generators mid-wave … canon.css is byte-identical either side" | **GREEN** | All three canon `--check` arms in sync (S1-1a/b/c), `canon.css` clean in the tree |

### `notes/_subreports/2026-08-26-219-seam9-final.md`

| # | item verbatim | verdict | evidence |
|---|---|---|---|
| S9-1 | "§③ the `GROUP_LEAD` KeyError (~500 tk — a green selftest over an unrenderable page, and the fix pattern of hoisting data so a bite can reach it)" | **GREEN** — fix present AND falsifiable | `GROUP_LEAD` is module scope at `_gen_pack_manifest.py:1322`. `selftest: 165 bites, 0 fail(s)`. **Mutation driven** against a `/var/tmp` copy with the gumdrop lead deleted: `RED [page/every-group-has-a-lead] got ['gumdrop'], wanted [] a group with no GROUP_LEAD entry is a KeyError at render, not a missing paragraph` |
| S9-2 | "§④ the OWED-inscription shape (~400 tk — the reusable answer to 'Dave said it, nobody has written it down')" | **GREEN** | `s219-D9` present in `_rulings.json`, `status: ruled`, and the `says` carries the clause: *"the ship list carries only gates that can actually run in a designer's project - **55 files in the gates group** (35 runnable + 3 needs-dep + helpers/data/ci-template)"*. Manifest `totals.by_group.gates.files` = **55** — the clause is true of the artefact, not just of the prose |
| S9-3 | "§② the three-file false claim and its assembled-phrase gate (~350 tk)" | **GREEN** | Three bites present at `:2049`, `:2053`, `:2058` — `cut/no-record-claim-is-dead:generator`, `:bake-script`, `cut/readme-points-at-the-cold-start`. Verified **in the bake, not the diff**: over the unzipped stage `grep -rl "no record of any kind"` returns nothing, and both `_MANIFEST.json` and `PROVENANCE.json` carry the corrected `carries.what` |
| S9-4 | "§ STAGE 2 FINAL Ⓑ the `GROUP_ORDER` omission (~400 tk — the THIRD copy of the group set, and the quiet-lie variant of §③)" | **GREEN** — fix present AND falsifiable | `GROUP_ORDER` module scope at `:1380`. **Mutation driven** (gumdrop removed from the list): two named REDs — `RED [page/every-group-is-a-card] got ['gumdrop'], wanted [] a group missing from GROUP_ORDER renders no card — the lede counts it, the page never shows it` and `RED [page/order-ends-with-the-memento-pair] got ['skills','memento-clean-cut'], wanted ['memento-clean-cut','gumdrop']`. On the shipped page the lede is derived and correct: *"It is seven groups. Five of them are things you already work in; the last two are Memento with its memory emptied out, and the day-one wal…"* |

---

## ② BONUS — a declared UNPROVEN discharged en route

enactA § UNPROVEN 2 declared: *"The four existing mutation arms BUILD but were not DRIVEN … the
browser verifier was NOT re-run in `--mutation` / `--layout-mutation` / `--inner-mutation` /
`--keyline-mutation`, so those buckets are unproven against today's page."* With the render env
staged, **all four were driven**, each against a non-repo mutant:

```
⬛ MUTATION ARM — 11 legality assertion(s) went RED
⬛ LAYOUT MUTATION ARM — 94 layout assertion(s) went RED
⬛ INNER-SQUARING MUTATION ARM — 16 inner assertion(s) went RED
⬛ KEYLINE MUTATION ARM (s217-D8) — 333 ruled assertion(s) went RED
```

The layout arm names Dave's own two `#217` defects back: `⛔ DISPLAY TIGHT IS A DIFFERENT
COMPOSITION — tight resolved 2 column(s) at 571px, standard resolved 4 at 1166px` and
`⛔ DASHBOARD ORPHAN GAP — 1 empty cell(s) of 4 at 2 column(s)`. **enactA's UNPROVEN 2 is
discharged.** [[mutation-tests-the-clause-not-the-feature]] — each arm was driven, not read.

---

## ③ FINDINGS — nine, none repaired

1. ⛔ **The shipped `Apollo-Spider-v1.0.0.zip` contains an unrunnable `_gen_chain.py`.**
   `memento-package/claude-plugin/memento/machinery/_gen_chain.py` dies on import for want of
   `_could_not_ask.py`; the sibling `memento-package/machinery/` copy has the file and runs. The
   two dirs differ by exactly that one line of `ls`. **The package delta gate is green over it**
   — it compares a VERBATIM SET that does not include the file, and it has no RUN arm. This is
   N3's finding 1 half-fixed and N3's Q1 vindicated on the very next release.
2. ⛔ **`s149-D1`'s `status` field is still false** (lane 5's finding 7, restated by seam 3). The
   ruling says NOT ENACTED; the enactment is live in `Tabs.reference.html:107`.
3. ⛔ **CI red `[18]` (`_gm_usage.py --selftest`) is unchanged**, at cause: `#218` wrapped twice
   under one session number. `[120]` (package delta) has gone green — but see finding 1 for what
   that green does and does not mean.
4. ⛔ **N1's and seam 8's STAGE-2 recipes cite `knowledge/_make_review.py`, which does not exist.**
   The path is `knowledge/_review/_make_review.py`. R2's copy of the same item is correct. A
   conductor following the § ⑧ block verbatim gets a `No such file or directory`.
5. ⛔ **The "do not re-seed the ledger at HEAD" warning was breached, and it names the wrong
   mechanism.** All three `baseline_commit`s moved `71bb2f7` → `ef44b1a`, the laundering arm did
   not fire, and it never would have: it keys on `content_sha256`.
6. ⛔ **The ruled spacing rail still has two homes** (`gen_bento_matrix_217.RULED_SPACING_RAIL` and
   `role_defaults_219.SPACING_STOPS`), gated by bite `R4c` but not reconciled — ADR-0017's
   one-home clause is unsatisfied, and the generator's own comment says so out loud.
7. ⚠ **A preserved evidence probe is pinned to a dead mount.**
   `assets/2026-08-25-219-lane1-segmented-adoption/sweep.py:3` hardcodes
   `ROOT = "/sessions/pensive-cool-galileo/mnt/UX-design"` and raises `PermissionError` in any
   later session. Preserved probes should derive ROOT, or declare the mount.
   [[non-repo-home-or-declare]]
8. ⚠ **New render-verify stratum, not in the runbook.** In this sandbox `apt-get download
   libxdamage1` fails (`E: Unable to locate package`; apt lists unlockable without root). The
   working move is `curl` straight from `ports.ubuntu.com/pool/main/libx/libxdamage/` then
   `dpkg-deb -x`. Every foreign-session `/var/tmp` stratum the runbook names is **gone** here —
   `ls` before trusting, as the fifth stratum already warns.
9. ⚠ **The #220 briefs stale the memento index.** `notes/_briefs/*.md` is in the corpus
   (`_build_memento_index.py:333`), so the three untracked #220 briefs make `[107]` red in any
   working tree that holds them. Zero records are lost — it is purely additive. **The conductor
   must run `python3 knowledge/_build_memento_index.py` and stage it before the #220 wrap**, or
   ritual step 2g bites.

---

## ④ THE TREE — what this lane did to the repo

**Nothing, net.** Opening state: 6 dirty lines (3 M from concurrent lanes, 3 untracked #220
briefs). Closing state: 10 lines — the extra 4 are other #220 lanes filing beside me
(`notes/_subreports/2026-08-27-220-charts-sparkline.md`,
`notes/_subreports/2026-08-27-220-readings-capsule.md`, its assets dir, and
`reviews/CORRECTION-READINGS-2026-08-27-v1.html`). **No line is mine**, other than this report.

⚠ **One self-inflicted write, declared.** Chasing a mutation I copied a patched generator to
`knowledge/_release/_gpm_mut_220_TEMP.py`. `rm` and `mv` both returned `Operation not permitted`;
the delete grant was requested and the file removed the same minute. `git status --porcelain`
before and after the incident is identical, and the mutation was then re-driven correctly from
`/var/tmp` with `ROOT` repointed. Recorded because a write I did not declare would be the worse
failure. [[a-crash-is-not-a-fail]]

Write-protection driven where the brief required it: `_capture_gate.py --selftest` was run with
`notes/_REHEARSAL-LOG.jsonl` md5-snapshotted either side — **`5683730ec1cd28a25df096ef9250e97c`
both times**, so the #158 write-by-default class did not fire on the selftest arm. Both
`gen_bento_matrix_217 --rails` and `_build_consult_index.py` were run with the dirty count
snapshotted either side and both proved **idempotent** — a stronger reading than "did not write".

Both #219 advisory gates were left **ADVISORY**: `_gate_minted_consumption.py` and
`verify_dv_d16_render.py`'s `WORDING-1`. Nothing promoted.

---

## RULING-SHAPED QUESTIONS → DAVE (nothing decided here)

1. **The shipped release has a broken file in it. Re-cut, or patch-release?** Finding 1. The zip
   is frozen (`_frozen-releases.json`, surface `apollo-spider/dist/`), and by `s219-D4(2)` a
   release is explicit, versioned, Dave's word. The fix is one file into one directory; **the act
   of shipping it again is not.** Options: (a) v1.0.1 re-cut; (b) leave v1.0.0 and fix at the
   next release; (c) fix the tree now and let the standing ADVISORY (*"a pack cut now would ship
   the tree as it stood at 2f7c47b"*) carry it. **PROPOSED: (a)** — the broken file is the
   cold-start chain generator, which is the first thing a Gumdrop designer touches.
2. **Should the delta gate gain a RUN arm?** N3's Q1, unchanged and now with a second instance
   behind it. It widens a gate's glob, so it is Dave's. **PROPOSED: yes** — the gate went green
   over a shipped ImportError, which is the exact failure it exists to prevent.
3. **`s149-D1`'s `status` field: correct it, or rule that status fields are historical?** A
   `_rulings.json` write either way. The stale field has now been carried by two reports and
   survived a seam.
4. **The pack runner's three verdicts versus the repo's four.** N2's HANDOFF 3, to be answered
   beside R2's Q4 (`--baseline`), as N2 asked. Costs nothing today; discovered by a designer
   tomorrow.
5. **The ruled rail's two homes** (finding 6) — ADR-0017 says one should address the other.
   `R4c` gates the drift, which is why it has been survivable, but the write-once principle is
   Dave's ruling and this is a live exception to it.
6. **And the fourteen-plus questions the enact lanes never got answered.** enact-A Q1–Q7,
   enact-B Q1–Q7 (its **Q1**, the gallery squaring flip, still literally `False` in
   `layout.json` with three review pages carrying a declared-divergence paragraph waiting on the
   word), enact-C Q1–5, lane 4's Q1–4, lane 5's Q1–2, lane 6's Q1–3, lane 1's Q1, lane 3's Q1,
   R3's Q3. `reviews/SITTING-219-2026-08-25-v2.html` is the single surface that indexes them.
   **30 open store rows carry `owner: dave` at `opened: 219`.**

---

## REPLAY-THESE (conductor)

- ⛔ **Finding 1 — the broken `_gen_chain.py` in the shipped zip.** Reproduce in three lines and
  see it for yourself before deciding anything:
  ```
  python3 -c "import zipfile;zipfile.ZipFile('apollo-spider/dist/Apollo-Spider-v1.0.0.zip').extractall('/var/tmp/pk')"
  cd /var/tmp/pk/Apollo-Spider-v1.0.0/memento-package/claude-plugin/memento/machinery && python3 _gen_chain.py --check
  diff <(ls -1 ../../../machinery) <(ls -1 .)      #  ->  < _could_not_ask.py
  ```
- ⛔ **Run `python3 knowledge/_build_memento_index.py` and stage it before the #220 wrap**
  (finding 9). `[107]` is red in this tree and it is the #220 briefs, nothing else. Proven, not
  assumed — but it must actually be regenerated, or the wrap ritual's step 2g bites.
- **CI-bound, stays yours — COULD-NOT-RUN by name here:** no `gh` in this sandbox and the GitHub
  API 404s unauthenticated, so no Actions run was read. `_build_all.py` end-to-end likewise
  (never run partially; a full run does not fit a sandbox call). Steps `[135]`/`[136]`
  (release audit) are green locally; step `[18]` (`_gm_usage`) is **red** locally and will be red
  in CI.
- **Findings 4, 5, 7 are one-line repairs in three different files and I made none of them.**
  Finding 4 lives in frozen history (ADR-0017) so it needs a note forward rather than an edit;
  findings 5 and 7 are live surfaces.
- **The render env recipe is worth inscribing** (finding 8) — `_RUNBOOK-render-verify.md` has
  five strata and this sandbox needed a sixth. Six browser-bound replay items turned on it.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: anything CI says.** No Actions run was read; every CI verdict above is a local
  reading of the same script. Named, priced at one authenticated `gh run view`.
- **UNPROVEN: `_build_all.py` as a runner.** Individual steps were driven; the runner loop was
  not entered. Unchanged from seam 3's declaration.
- **UNPROVEN: the assembled-phrase gate's falsifiability.** The three `cut/…` bites were read in
  source and the 165-bite selftest is green, but the phrase was not reassembled in a mutant to
  watch them go red. Priced at ~10 minutes. The `GROUP_LEAD` and `GROUP_ORDER` bites beside them
  **were** mutation-driven, so the pattern is proven; this specific trio is not.
- **CLAIMED, then re-read:** every figure in this report was taken from a probe run in this
  window and quoted from its own output, not from the report that asked for it.
