# `#219`-seam2 — the reconcile after the re-cut + DV-D16 lanes: 23 paths attributed, serial re-driven, store 5/5 intact, the pro-forma proven untouched

session: `#219` · 2026-08-25
window: `#219` crank, wave 2 — **seam-2 reconcile** (after the bento re-cut lane and lane 4 / DV-D16 filed)
sub index: `seam2`
brief: `notes/_briefs/2026-08-25-219-crank-divvy.md`
base: `d178313` (clean at wave open)
tokens: UNMEASURED — a sub cannot read its own `message.usage`; the conductor's gauge is the authority.

## VERDICT

**CLEAN TO COMMIT. No conflict, no clobber, nothing unattributed left unresolved.**

**COUNTS:** working-tree lines 23 (15 M · 8 ??) · attributed 23 · UNCLAIMED-at-open 2, both resolved
by investigation, 0 remaining · store rows verified 5/5 intact, 0 re-minted · serial steps driven 8,
all rc 0 · check verdicts quoted 9 · probes re-driven after the serial 5 (3 bento + DV static + DV
render), all GREEN · findings 4 · ruling-shaped 0 · UNPROVEN 2 · store rows minted 1 (`W-177`, this
report)

Headlines:

1. **The store did NOT clobber.** Both lanes wrote `knowledge/_state.json` concurrently and the diff
   is **+71 lines, 0 deletions**. `W-172` · `W-173` · `W-174` · `W-175` · `W-176` all present with
   intact bodies, owners and `closes_when`. **5/5. Nothing re-minted.** Lane 4's shared-tree warning
   (§7 of its report) was the right call and it did not fire.
2. **`knowledge/_proforma/DataViz-interactive.html` is byte-identical before and after the serial** —
   `b8dc63a5…6bb87d89`, 110,365 bytes, both readings. No serial step touched it. Lane 4's caution is
   **confirmed at the mechanism, not just at the outcome**: `_gen_dataviz_charts.py` appears **nowhere**
   in `knowledge/_build_all.py` (grep for `_gen_dataviz_charts` returns zero hits in that file).
3. **The serial produced exactly ONE new generated line and it is explained:** `showroom/chart-bar.html`,
   downstream of lane 4's `knowledge/snippets/Chart-bar.reference.html` edit. Every other serial step
   reported *no change / 0 written / in sync*.
4. **`_CHAIN.md` was STALE — and stale AT HEAD, not from either lane.** Regenerated and included.

---

## ① PATH-BY-PATH MANIFEST — 23 lines (15 M · 8 ??), 0 unaccounted

Ownership taken from each lane's own paths list where one exists; everything else was investigated by
diff and is marked how it was attributed.

### Modified — the bento re-cut lane (lane 3)

| path | disposition |
|---|---|
| `knowledge/_render/gen_bento_canon_217.py` | include — v4 emitter + the reversed selftest bite 6b |
| `knowledge/_render/gen_bento_roles_217.py` | include — v5 emitter + the reversed selftest bite 6c |
| `knowledge/_render/gen_gallery_compare_217.py` | include — compare v2 emitter + the A4 squared wall |
| `knowledge/_render/verify_bento_canon_217.py` | include — caption arm + `from <generator> import OUT as PAGE` |
| `knowledge/_render/verify_bento_roles_217.py` | include — same one-source-for-the-name fix |
| `knowledge/_render/verify_gallery_compare_217.py` | include — same |

### Modified — the DV-D16 lane (lane 4)

| path | disposition |
|---|---|
| `knowledge/_proforma/DataViz-interactive.html` | include — the transplanted DV-D16 region delta only (42 lines) |
| `knowledge/_review/_gen_dataviz_charts.py` | include — the CAUSE edit; wording ① retired, ② + `s218-D5` enacted |
| `knowledge/_render/verify_dv_d16_render.py` | include — profiles + `--target` + `WORDING-1` + `DV-004-STROKE` |
| `knowledge/snippets/Chart-bar.reference.html` | include — 12 inert `animation-delay` declarations stripped |

### Modified — co-written by BOTH lanes

| path | disposition |
|---|---|
| `knowledge/_state.json` | include — **+71 insertions, 0 deletions**; `W-172`/`W-173` (lane 3) + `W-174`/`W-175`/`W-176` (lane 4) all intact. §② |

### Modified — produced by THIS reconcile (seam)

| path | disposition |
|---|---|
| `showroom/chart-bar.html` | include — **generated at the seam** by `gen_showroom.py`, downstream of lane 4's Chart-bar snippet edit. Not present at either lane's filing; appeared with the serial. |
| `_CHAIN.md` | include — **regenerated at the seam**; `--check` was RED and the redness is PRE-EXISTING AT HEAD. §④ |

### Modified — telemetry (append-only)

| path | disposition |
|---|---|
| `notes/_REHEARSAL-LOG.jsonl` | include — **2 appended lines**, both `{"kind": "rehearse", "fails": 0, "structural": 0, "warns": 18}`. §③ finding 2. |

`notes/_dream/_GRADE-DECISIONS.jsonl` is **clean** — no check-in append landed on it this wave.

### Untracked — the bento re-cut lane

| path | disposition |
|---|---|
| `knowledge/_render/_bento_recut_219.py` | include — the ONE ledger home (ADR-0017), 5 selftest bites |
| `reviews/BENTO-CANON-2026-08-25-v4.html` | include — canon demo, successor to `-2026-08-23-v2` |
| `reviews/BENTO-CANON-2026-08-25-v5.html` | include — roles demo, successor to `-2026-08-23-v3` |
| `reviews/GALLERY-COMPARE-2026-08-25-v2.html` | include — successor to `-2026-08-23-v1` |
| `notes/_subreports/2026-08-25-219-recut-bento-surface.md` | include — filed report (`W-173`) |

### Untracked — the DV-D16 lane

| path | disposition |
|---|---|
| `knowledge/_render/apply_dv_d16_region_219.py` | include — the transplant bridge (`W-174`) |
| `notes/_subreports/2026-08-25-219-lane4-dv16.md` | include — filed report (`W-175`) |

### Untracked — this reconcile

| path | disposition |
|---|---|
| `notes/_subreports/2026-08-25-219-seam2-reconcile.md` | include — this report (`W-177`) |

**The #217 predecessor pages are on disk and untouched**: `reviews/BENTO-CANON-2026-08-23-v2.html`,
`-v3.html`, `reviews/GALLERY-COMPARE-2026-08-23-v1.html` — none appears in `git status`, so
version-don't-overwrite held and the mutation arm's mutant (v2) is still there to be driven against.

### UNCLAIMED AT OPEN — 2 lines, both resolved, 0 remaining

| path | how it resolved |
|---|---|
| `knowledge/_proforma/_DATAVIZ-DECISIONS.md` | **ATTRIBUTED BY CONTENT to lane 4, but ABSENT from lane 4's own file table (§2).** The diff is +24 lines, pure ADDITION under the existing `DV-D16` block, and it cites `notes/_subreports/2026-08-25-219-lane4-dv16.md` and row `W-175` by name. Nothing above it is amended (it says so in as many words and cites `[[header-wins-over-audit]]`). **Include — but see finding 1: a manifest that omits a path is how a real stray gets waved through.** |
| `notes/_REHEARSAL-LOG.jsonl` — **the second** appended line | Lane 3 named **one** `--rehearse` append; there are **two**, byte-identical in shape. Append-only telemetry with `fails 0 / structural 0`; the second is either lane 3's gate run twice or lane 4's unnamed one. **Benign and include** — but it is unattributed by name, and finding 2 records it rather than letting it pass silently. |

---

## ② STORE-ROW COLLISION CHECK — 5/5 INTACT, 0 RE-MINTED

`knowledge/_state.json` was written by both lanes. The store is a read-modify-write of one JSON file,
so the question is whether the later writer dropped the earlier writer's rows.

**It did not.** `git diff --stat knowledge/_state.json` → **`1 file changed, 71 insertions(+)`** — no
deletion line at all, which is the shape a clobber cannot have.

| id | present | owner | home | body intact |
|---|---|---|---|---|
| `W-172` | ✅ | dave | `knowledge/_render/_bento_recut_219.py` | ✅ full body + `closes_when` naming all five live controls (Q2/Q3/Q6/Q11/Q12) + `links` to `W-119`/`W-124`/`W-125` |
| `W-173` | ✅ | claude | `notes/_subreports/2026-08-25-219-recut-bento-surface.md` | ✅ links `W-172`; closes on the conductor citing it BY PATH |
| `W-174` | ✅ | claude | `knowledge/_render/apply_dv_d16_region_219.py` | ✅ closes when the pro-forma is reconciled with its generator (`W-176`) and the bridge is deleted |
| `W-175` | ✅ | dave | `notes/_subreports/2026-08-25-219-lane4-dv16.md` | ✅ body states in as many words that it does NOT close or reword `W-142` |
| `W-176` | ✅ | dave | `notes/_subreports/2026-08-25-219-lane4-dv16.md` | ✅ the 80,384-vs-73,242 measurement carried in the body |

All five carry the full `SCHEMA` key set (`body`, `closes_when`, `condition`, `home`, `id`, `links`,
`opened`, `owner`, `project`, `state`, `title`) — no row landed truncated.

**Store gates, verbatim:**

| gate | verdict |
|---|---|
| `python3 knowledge/_state.py --selftest` | `_state selftest: 57 bites, all GREEN` |
| `python3 knowledge/_gate_doc_rows.py` | `doc-row gate: population 74 (added >= 2026-08-15, PICKED) · of which staged-in-THIS-commit 0 (#207 postscript: the single-commit blindspot) · unrowed 0` / `✅ PASS — every in-scope document has a store row.` |
| `python3 knowledge/_state.py --check` | passes; four ⚠ lines are **the standing declared debt** — 14 unconditioned legacy items (frozen set 19, may only fall), 0-of-153 deadline/effort coverage, the #172 project-split defaults, and 17 `path:line` home pointers (the #168 rot class). **All four reproduce at HEAD and none is this wave's.** ⛔ Every one of them is Dave's to move; nothing was touched. |

⚠ `_gate_doc_rows` reports `staged-in-THIS-commit 0` because nothing is staged yet — that is the
**#207 single-commit blindspot named in its own output**, not a pass on the new documents. The
population reading (`unrowed 0`) is what covers them, and lane 3's `--rehearse` run
(`0 STRUCTURAL fail(s)`) is the second reading over the same corpus.

---

## ③ THE ORDERED SERIAL, RE-DRIVEN WHOLE — steps in order, each its own call

Order taken from `knowledge/_build_all.py::STEPS`, cross-read against `#219`-seam1's own run —
**ramp first, index last**. Never `_build_all.py` (a partial run strands the tree). `tiktoken`
installed first (`import tiktoken` → `tiktoken OK`) so no build-verdict red can be a cold-sandbox
artefact.

| # | step | verdict (verbatim) | rc |
|---|---|---|---|
| 0 | `canon/gen_canon_tokens.py` | `TOTAL: 577 root vars, 195 dark overrides` / `Wrote …/knowledge/canon/canon.css` | 0 |
| 1 | `gen_token_ramp.py` **(RAMP FIRST)** | `gen_token_ramp: 0 file(s) synced (0 with block, 0 block-removed), 147 already in sync.` | 0 |
| 2 | `canon/gen_canon_components.py` | `gen_canon_components: no change (135 components in sync).` | 0 |
| 3 | `gen_snippet_tokens.py` | `gen_snippet_tokens: 4804 manifest bindings across 135 snippets + 9 tranches; 0 value(s) projected; 0 canon.css literal(s) projected.` / `OK — snippets + tranches + canon.css in sync with tokens.` | 0 |
| 4 | `canon/gen_theme_cascade.py` | `gen_theme_cascade: no change (in sync).` | 0 |
| 5 | `gen_showroom.py` | `gen_showroom: 135 page(s) -> showroom/ (1 written, 0 orphan(s) pruned; index owned by knowledge/_render/gen_library_214.py)` | 0 |
| 6 | `_render/gen_library_214.py --check` | `gen_library_214 --check OK — 142 component(s), index + index.json + stub in sync.` | 0 |
| 7 | `_build_memento_index.py` **(INDEX LAST)** | `memento index: 1791 records → knowledge/_memento-index.json` | 0 |

**The `1 written` at step 5 is `showroom/chart-bar.html`** and it is the only file the serial created
or changed. It is the generated consequence of lane 4's `Chart-bar.reference.html` edit — the same
shape seam-1 saw with `showroom/navigations.html`. `canon.css` came back byte-stable across steps 0–4
(`no change` / `0 synced` / `in sync` at every position), so the two lanes' edits did not collide in
canon.

**`_render/gen_thumbs.py` was DELIBERATELY NOT RUN**, on seam-1's precedent and for its reason: no
upstream step reported a change to anything a thumbnail depends on, the generator has no `--check`
arm and re-shoots all 142 unconditionally, so running it manufactures encode churn. `gen_library_214
--check` (which bites on a missing thumbnail) and `gen_showroom.py` are the readings that matter and
both are green above.

### ⚠ THE PRO-FORMA CAUTION — DISCHARGED AT THE MECHANISM AND AT THE BYTES

Lane 4 asked that nothing in the serial regenerate or revert
`knowledge/_proforma/DataViz-interactive.html`. Two independent readings, because either alone can be
right while the tree is wrong:

- **Mechanism.** `grep -n "_gen_dataviz_charts\|dataviz" knowledge/_build_all.py` returns **zero hits
  for `_gen_dataviz_charts`**. The only `dataviz` entries in `STEPS` are `_validate_dataviz.py` and
  `_gate_dataviz_vars.py` — **gates, which read and never write**. There is no step that could write
  the artefact.
- **Bytes.** `sha256` **before** the serial `b8dc63a54421294876dd5fae4697f21747e3ffde9fe7a8cb82a3b0696bb87d89`
  (110,365 bytes) · **after** the serial, and again after all five probe runs,
  `b8dc63a54421294876dd5fae4697f21747e3ffde9fe7a8cb82a3b0696bb87d89`. **Identical.**

**No step had to be stopped.** Nothing tried.

---

## ④ CHECK BATTERY — 9 VERDICTS, QUOTED

| check | verdict (verbatim) |
|---|---|
| `canon/gen_canon_components.py --check` | `gen_canon_components --check OK — 135 components in sync.` |
| `canon/gen_theme_cascade.py --check` | `gen_theme_cascade --check OK — 230 override path(s), 387 component projection(s) in sync.` |
| `gen_token_ramp.py --check` | `gen_token_ramp: 0 file(s) DRIFTED (0 with block, 0 block-removed), 147 already in sync.` |
| `_build_memento_index.py --check` | `memento index --check: current (1791 records)` |
| `_gen_chain.py --check` (**BEFORE**) | ⛔ `✗ _CHAIN.md is STALE — it does not match GOOD-MORNING.md / _LIVE-STATE.md as they now stand, so a cold session would read a PREVIOUS session's record as if it were current. Run \`python3 knowledge/_gen_chain.py\` and stage the result.` |
| `_gen_chain.py` (regenerate) | `✅ _CHAIN.md: 42,055 real · GM header+LATEST 23644 tk · LS LATEST delta only (of 52 delta lines) 6330 tk · FILE 42,055 real = slice 29,974 + wrapper 12,081 · fixed point in 2 pass(es)` |
| `_gen_chain.py --check` (**AFTER**) | `✅ _CHAIN.md is FRESH — byte-matches the live chain · GM header+LATEST 23644 tk · LS LATEST delta only (of 52 delta lines) 6330 tk · FILE 42,055 real = slice 29,974 + wrapper 12,081 · fixed point in 2 pass(es)` |
| `_state.py --selftest` | `_state selftest: 57 bites, all GREEN` |
| `_gate_doc_rows.py` | `✅ PASS — every in-scope document has a store row.` |

### The `_CHAIN.md` red is PRE-EXISTING AT HEAD, and that is a finding

`GOOD-MORNING.md`, `notes/_LIVE-STATE.md` and `_CHAIN.md` are **all three clean in the working tree**
— `git status --porcelain` on them returned empty before the regenerate. Neither lane touched any of
the chain's three inputs. So the staleness is **`d178313`'s**: the previous seam committed without
regenerating the chain, and a cold session reading `_CHAIN.md` at HEAD would have read `#218`'s record
as current ([[read-chain-is-where-staleness-is-free]] — exactly the surface that hook names).

⛔ **The generator writes `_CHAIN.md` and nothing else** (`OUT_NAME = "_CHAIN.md"`, verified by reading
the module before running it). `GOOD-MORNING.md` and `_LIVE-STATE.md` are read-only inputs — the
DO-NOT-TOUCH list held.

### `knowledge/_graph-mention-map.json` — the #208 `[110]` class: **FRESH**

`_build_graph_mention_map.py` was driven and the file came back **byte-identical**:
`e7cdd1a24b1fbc74767ed3da003e6fce4e9781e8b0e48e0a5d72752a6f73d135` before and after.
Verdict: `graph mention map: 101 of 101 node(s) mentioned, 1176 record hit(s) total -> _graph-mention-map.json`.
**It does not appear in `git status` and is not part of the commit.** Regenerating rather than only
`--check`ing was deliberate: the map is what the `_git_commit.sh` MENTION-MAP gate reads, and a
`--check` that agrees with a stale generator is the [[no-gate-parses-the-artefact]] shape.

---

## ⑤ PROBES RE-DRIVEN **AFTER** THE SERIAL — 5 runs, all GREEN

The point of re-driving is that a serial can move canon under a page that was green before it. All
five were driven against the post-serial tree, staged per `knowledge/_RUNBOOK-render-verify.md`
(`LD_LIBRARY_PATH=/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu` — the fifth stratum,
`/var/tmp/chromelibs` is hollow · `PYTHONPATH=/var/tmp/pylibs` · `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215` ·
`FONTCONFIG_FILE=/var/tmp/fonts-s219l3.conf`, lane 3's farm, **`<include>` present, verified by reading the conf**
· `TMPDIR=/var/tmp`).

| probe | exit | verdict (verbatim tail) |
|---|---|---|
| `verify_bento_canon_217.py` (v4) | 0 | `ALL GREEN — 8 states: per-theme gutter · container radius + clip · square tiles · nested parameter sets · dangling sweep · band collapse · bottom edge at 4 widths · portrait two-row.` |
| `verify_bento_roles_217.py` (v5) | 0 | `ALL GREEN — 8 states: per-role radius placement + clip · per-role spacing (incl. the dashboard inner/outer split) · squaring where ratified · gallery ragged-tolerance exercised · portrait two-row survives the exemption · caption space · trial does not leak · dangling sweep.` |
| `verify_gallery_compare_217.py` (compare v2) | 0 | `ALL GREEN — 8 states: B justifies flush to the container at 3 widths x 2 gutter regimes · native aspect preserved to 1% on every box · one height per justified row · widows unscaled and the switch driven both ways · A still canon's own output (gutter, radius, cover, caption) · A's raggedness counted not enforced · dangling sweep.` |
| `verify_dv_d16_render.py --target all` (static + render) | **0** | 4 profile blocks, each `GREEN  (0 failures)`: STATIC proforma · RENDER proforma · STATIC snippet · RENDER snippet |
| `apply_dv_d16_region_219.py --selftest` | 0 | `SELFTEST GREEN — transplant output is byte-identical to the generator's (102798 bytes)` |

Two readings worth quoting because they are the discriminators the lanes built:

- **Gallery compare, `s218-D6 (4)` scope still enacted after the serial:**
  `A raggedness EXERCISED, not asserted (s217-D3 rules orphans acceptable): mono/light A#0:6, mono/light A#1:4, mono/light A#3:4, …`
  — A#2 (the squared instance) absent from the ragged list in every state, the other three ragged.
- **DV-D16 wording ② still live after the serial:** `t=0.25 … columns fully-growing: 4  keys lit: 0/12`
  and `no stacked rect declares its own timing (wording ① cannot come back unseen)`.

**No `.uuid` strays, no temp artefacts in the repo** — `git status --porcelain --ignored` grepped for
`uuid` / `.tmp` / `dvd16` returned nothing. `apply_dv_d16_region_219.py --selftest` writes its two
comparison copies **outside the repo** (`/sessions/…/tmp/dvd16-*/`), which is why the tree is clean
after it.

---

## ⑥ FINDINGS

**1 · A LANE'S OWN PATHS LIST CAN BE SHORT, AND A SHORT LIST IS WORSE THAN NO LIST.**
Lane 4's §2 table names five files. Its edit touched **six**:
`knowledge/_proforma/_DATAVIZ-DECISIONS.md` (+24 lines) is missing from it. The content is
unmistakably lane 4's — it cites lane 4's own report path and row `W-175` — so the reconcile
attributed it in one diff read. But the reconcile's method is *attribute every line to a claimant*,
and an omitted path arrives looking exactly like a stray from a third writer. Lane 3 got this right
by naming even the `--rehearse` append it did not intend to make (*"named here rather than left for
the reconcile to wonder about"*). ⬛ **Priced, small:** sub briefs already require a paths list; they
should require it to be generated from `git status` rather than recalled, because a recalled list
omits exactly the file the author thinks of as documentation rather than as a change.

**2 · TWO REHEARSE APPENDS, ONE CLAIMANT.** `notes/_REHEARSAL-LOG.jsonl` gained two identical
`{"kind": "rehearse", …, "warns": 18}` lines; lane 3 declares one. Append-only, `fails 0`,
`structural 0`, so it is benign — recorded because "benign" and "unattributed" are different
properties and only one of them was checked.

**3 · `showroom/chart-bar.html` EXISTED ONLY AFTER THE SERIAL.** Lane 4 edited a snippet and, per the
brief, ran no regen serial. The generated downstream therefore did not exist at filing and appears in
no lane's manifest. This is the intended division of labour — but it means the **seam** is the only
place the snippet→showroom consequence becomes visible, and a seam that spot-checked instead of
running the whole serial would have committed a snippet whose showroom page contradicted it. Second
consecutive wave with this shape (seam-1 had `showroom/navigations.html`).

**4 · THE CHAIN WAS STALE AT HEAD AND NO GATE STOPPED THE PREVIOUS COMMIT.** §④. `_gen_chain.py
--check` is a `STEPS` entry and `_git_commit.sh` runs it at the seam, so the mechanism exists; what
this reconcile cannot tell from the tree is whether it ran and was overridden, or did not run.
Recorded as a fact about HEAD (`_CHAIN.md` clean **and** stale) rather than as a diagnosis of the
commit path, because the second would need the previous seam's transcript
([[unmatched-grep-is-not-an-absence]]).

---

## ⑦ UNPROVEN — DECLARED

1. **The mutation arms were not re-driven at the seam.** Lane 3's `-NOSQUARE`/`-WRONGROLE`/`-BROKEN`
   arms and lane 4's `--mutate all` tables were green in their own lanes and nothing in the serial
   touched the mechanisms they exercise — but that is an inference. The serial is the thing that
   changed between their run and this one, and it reported `no change` at every canon position, which
   is *evidence* and not *the measurement*. Price: ~3 min static, ~4 min with render.
2. **No PNG was read and no eye has been on the three re-cut pages.** Every verdict above is a
   computed-style or geometry assertion. Dave's five live controls, and lane 3's ruling-shaped
   questions 1, 2 and 8 (including whether **v4/v5 is the right series cut** — a filename the
   conductor may re-cut before the commit), are all still owed his eye.

---

## ⑧ FOR THE CONDUCTOR — WHAT IS OWED AT THE COMMIT

- **Cite both filed reports BY PATH** in the `#219` receipt — `W-173` and `W-175` close on it:
  `notes/_subreports/2026-08-25-219-recut-bento-surface.md` ·
  `notes/_subreports/2026-08-25-219-lane4-dv16.md` · and this one,
  `notes/_subreports/2026-08-25-219-seam2-reconcile.md`.
- **REPLAY-THESE from lane 4** (its §7) were driven at this seam and are green — items 1 and 2 above.
  Item 3, `_verify_dv_stacked_enactment.py` (~40 s), was **not** re-driven here; it covers the font
  face for Chart-bar and lane 4's own run of it is the standing reading.
- **`_CHAIN.md` is in the commit** and must stay in it — dropping it re-strands the cold-start door.
- **Ruling-shaped questions: 8 from lane 3, 4 from lane 4, 0 from this reconcile.** None was decided
  here. Lane 3's item 8 (the v4/v5 series cut) is the only one that must be settled *before* the
  commit, because it is a filename.
- **`W-177` is minted for this report** (owner claude, `opened` 219). No other store row was written.

## ⑨ NOT DONE, ON PURPOSE

- **No commit, no push.**
- **No `knowledge/_rulings.json` write.** No constant, band, threshold, advisory or stop line touched.
- **`GOOD-MORNING.md` and `notes/_LIVE-STATE.md` untouched** — read as inputs by `_gen_chain.py`,
  written by nothing.
- **No row of Dave's closed, reworded or re-scoped.** `W-142`, `W-119`, `W-124`, `W-125`, `W-126`,
  `W-172`, `W-175`, `W-176` stand exactly as their lanes left them.
- **No memory write.**
- **Nothing dropped or reverted.** Unlike seam-1, no path needed restoring; every one of the 23 lines
  is in the commit.
