# #219 seam 5 — the reconcile: every path claimed, and four probes caught asserting a superseded ruling

**Lane:** seam 5 (reconcile), #219 wave 1. **Model:** Opus. **Base:** `8486e09`, clean plus the
conductor's telemetry. **Scope:** reconcile the working tree lanes A and B wrote concurrently,
repair the cross-lane staleness lane B flagged, regenerate what drifted, re-drive both lanes'
probes. **No commit. No push.**

**COUNTS:** findings 9 · ruling-shaped 0 · UNPROVEN 5 · paths reconciled **33 at hand-off**
(23 modified · 10 untracked — 30 inherited, 3 added by this seam) · UNCLAIMED **0** ·
probes re-pointed 4 · new gates 5 assertion bites · source files edited 8 · artefacts regenerated 8
(`_CHAIN.md`, 5 Foundations pages, `_bento_edit_rails.json`, `_state.json`) · new artefacts 5
(3 re-cut pages, SITTING v2, this report) · store rows minted 3 (W-183/184/185)

⛔ **This seam put NO question of its own, and it resolved none of Dave's.** The write-once
two-homes rail question (enact-A Q6) and every one of lane B's Q-list are UNTOUCHED and still open.
Where a repair would have required answering one of them, the page says so on its own face instead
— see §4.

---

## VERDICT

Tree is reconciled and green. Every one of the 30 working-tree paths is claimed by lane A, lane B
or the conductor; **nothing is unclaimed**. `knowledge/_rulings.json` carries exactly the
conductor's two inscriptions and nothing else. The five drifted Foundations pages are regenerated
and `--check` is clean. Lane B's blocking finding 12 is repaired at cause and gated. Both lanes'
probes are re-driven green, **including the two things each lane declared UNPROVEN and could not
prove from inside its own lane**.

The regen serial is **DECLARED SKIPPED**, on a probe, not on a belief: no canon or token source
changed (§5).

---

## 1 · The reconcile — 33 paths at hand-off, 0 unclaimed

The tree the seam INHERITED was 30 paths (15 `git status` lines at entry, of which the 9 untracked
and 6 of the modified were the two lanes'; the rest are listed below). At hand-off it is **23
modified + 10 untracked = 33**, the difference being this seam's own work. Both states are
reconciled below; the table is the hand-off state.

`knowledge/_rulings.json` was verified before it was included, not assumed:
`git diff --numstat` reads **30 insertions, 0 deletions**, and the diff is two whole appended
objects — `s219-D1` and `s219-D2` — inserted after the last existing entry with the closing `]`
untouched. Byte-clean append, no edit to any standing ruling. **INCLUDED.**

| path | claimed by |
|---|---|
| `knowledge/_render/gen_bento_matrix_217.py` · `verify_bento_matrix_217.py` · `_bento_edit_rails.json` (new) | **lane A** |
| `knowledge/_render/gen_foundations_217.py` · `verify_foundations_217.py` · `verify_photography_218.py` · `role_defaults_219.py` (new) · `showroom/_foundations/photography.html` · `logos.html` · `reviews/SQUARING-PORTRAIT-2026-08-25-v1.html` (new) | **lane B** |
| `knowledge/_rulings.json` (the two inscriptions) · `knowledge/_state.json` (5 appended rows, 65 insertions / 0 deletions, W-99zm/zn/zo/zp/zq) · `notes/_receipts/2026-08-25-219-role-defaults-exports.md` (Dave's twelve exports, transcribed — the receipt `s219-D1(3)` names by path) · `notes/_subreports/…-enactA-rails.md` · `…-enactB-defaults.md` | **conductor** |
| `knowledge/_render/_bento_recut_219.py` · `gen_bento_canon_217.py` · `gen_bento_roles_217.py` · `gen_gallery_compare_217.py` · `verify_bento_canon_217.py` · `verify_bento_roles_217.py` · `verify_gallery_compare_217.py` · `verify_grids_218.py` · `_CHAIN.md` · `showroom/_foundations/bento.html` · `grids-12col/-dashboard/-display/-gallery.html` · `reviews/BENTO-CANON-2026-08-25-v6.html` (new) · `-v7.html` (new) · `GALLERY-COMPARE-2026-08-25-v3.html` (new) · `SITTING-219-2026-08-25-v2.html` (new) · this report (new) | **seam 5** |
| `_to_delete/` incl. `_219-entry-inputs/` | gitignored scratch — confirmed against `.gitignore`'s `_to_delete/` clause |

**UNCLAIMED: none.** Two paths the sitting-index lane flagged as "NOT MINE"
(`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`) do **not** appear in the
working tree at this seam — they are already clean, so there is nothing to attribute.

## 2 · `_CHAIN.md` — stale, and the cause is not what a first read suggests

`_gen_chain.py --check` was RED. ⚠ It is worth naming why, because the obvious reading is wrong:
`GOOD-MORNING.md`, `knowledge/_LIVE-STATE.md` and `_CHAIN.md` are all **clean at HEAD** — none was
edited by anyone today. The chain was stale because it is generated FROM THE STORE, and the store
gained five rows (`W-99zm`…`zq`) that lanes A/B and the conductor minted. Regenerated: the diff is
the five new rows plus the counts they move (`241 → 246 items`, `85 → 90` Dave's) and the fixed-point
size line. **`GOOD-MORNING.md` and `_LIVE-STATE.md` were not touched**, as briefed.

## 3 · Lane B finding 12 — repaired at cause, and gated

`knowledge/_render/_bento_recut_219.py` is the ONE home for the bento decision ledger and three
review pages render it. It still stated `s218-D6 (1)` as ruled law and still painted its retired
dark caption ground — hours after `s219-D2 (1)` retired it. Updated **from the store**, reading
`s219-D1` / `s219-D2` verbatim out of `knowledge/_rulings.json`:

| row | before | after | receipt |
|---|---|---|---|
| **Q6** ragged-or-square edge | PARTIAL — residue *"whether the ROLE's default flips"* | **RULED, struck** | `s219-D2 (2)` |
| **Q7** mono caption ground | RULED at `s218-D6 (1)`, DARK | **re-struck**, light grey; `s218-D6 (1)` kept as frozen history in `also` | `s219-D2 (1)` |
| **Q4** keylines | `also` = `s218-D3` "off in all four themes" | `also` = the supersession; the #218 record kept beside it | `s219-D2 (4)` |
| **Q3** crop bound | PARTIAL at `s218-D6 (4)`, scoped to one page | PARTIAL at the **wider** ruling — scope grows, residue **expressly** stays open | `s219-D2 (2)` |
| **Q13** console gallery rounding | *(absent)* | **NEW, struck** — capsule; resolves `s217-D5`'s open P3 | `s219-D2 (3)` |
| **Q14** the spacing rail | *(absent)* | **NEW, struck** — six stops; strikes v5's "same three spacings" | `s219-D1 (4)` |

**Struck/open per page: canon `5/3 → 6/3` · roles `6/2 → 8/1` · compare `7/4 → 9/3`.**

⛔ **Nothing was rounded UP, and the ledger's own discipline is what proved it.** `open_control_html`
REFUSES to render a RULED row as a live control. Flipping Q6 therefore *broke two generators* —
`gen_bento_roles_217` and `gen_gallery_compare_217` both called `open_control_html("Q6")`. That
refusal is the instrument doing its job: it made a silent laundering impossible and forced the two
pages to be edited deliberately. Q3 went the other way: `s219-D2 (2)` widens the squaring and in
the *same sentence* says the orphan/flattening refinement *"is expressly NOT ruled here"*, so the
row stays PARTIAL with that sentence quoted at the residue.

**`mono_caption_css` was re-pointed, not renamed away.** It now ADDRESSES
`gen_foundations_217.BG_FALLBACK["--surface-subtle"]` and `.CAP_INK` — the ratified enactment — and
**fails loud** if either address moves. The retired pair survives by name as
`RETIRED_MONO_CAPTION_218`, uncalled, so a reader can tell a superseded ground from one nobody ruled.

**Gated, so the class cannot recur silently** ([[gate-dont-patch]]): five new assertion bites —
`_bento_recut_219` bites 6/6b/6c (the mirror carries the enacted tokens, paints neither retired one,
and agrees with Q7's receipt) plus the flipped `gen_bento_canon_217` 7f/7f2, `gen_bento_roles_217`
8c/8c2 and `gen_gallery_compare_217` 7g/7g2, each asserting **both halves** — new ground present AND
retired ground absent. Asserting only presence would pass a page that painted both and let the
cascade pick what Dave saw.

**Pages regenerated as new versions** (the generators' own convention: `BENTO-CANON-<date>-vN` is a
series *shared* by two generators, so the numbers move in pairs):
`BENTO-CANON-2026-08-25-v6.html` (canon) · `-v7.html` (roles) · `GALLERY-COMPARE-2026-08-25-v3.html`.
**v4, v5 and v2 are untouched on disk.** Paint verified clean: `var(--surface-digital-black,` and
`var(--text-reverse,` appear **zero** times in all three; the token NAMES appear twice each, both as
quoted history (the supersession comment and Q7's `also` clause), which is the point.

## 4 · The declared divergence — what this seam refused to enact

`s219-D2 (2)` makes square the gallery-role **default**. The default lives in the token store, and
`knowledge/tokens/layout.json`'s `layout/bento/$roles/gallery/squaring` still reads `false`, so
`role_policy("gallery")` still answers EXEMPT and the gallery walls on these pages are still ragged.

Flipping it is a canon regeneration reaching **every** gallery bento anywhere — and it is lane B's
Q1, **Dave's**. So it was not done. What was done instead: v5's sentence *"the wall above is still
ragged, and why that is still correct"* — now false — is replaced on both pages by the ruling, then
by a paragraph that says the wall is ragged *because the store has not been flipped*, that flipping
it is his call, and that **the paragraph is a divergence and not the ruling**. Same construction
lane B used for `pageBg: transparent`. The ledger's Q6 `baked` field says the same thing.

## 5 · The serial — declared SKIPPED, on a probe

Lane B's squaring canon-flag question was NOT enacted, so the ordered regen serial should not run.
Confirmed by measurement rather than by memory:

```
git status --porcelain -- knowledge/tokens/ knowledge/canon/ showroom/_css/   → EMPTY
layout.json /layout/bento/$roles/gallery/squaring                            → False
```

**No canon or token source changed. The ordered serial (ramp first, index last) is DECLARED SKIPPED
on that probe.** The five drifted pages were regenerated by their **owning generator only** —
`gen_foundations_217.py` is the one writer of `showroom/_foundations/*.html` (`gen_grids_218`
supplies the grids content through it), so one run covers `bento.html` (lane A's grammar drift) and
the four `grids-*.html`. `--check` after: **7 pages in sync**. `_gen_chain.py --check`: **FRESH**.

## 6 · FOUR PROBES WERE ASSERTING A SUPERSEDED RULING — the finding of this seam

Three of these surfaced **only after the regen**, which is the argument for re-driving rather than
trusting a lane's own green. In every case the probe would have **redded the RULING, not the page** —
the failure mode lane B named when it re-pointed `verify_photography_218`.

1. **`verify_bento_canon_217`** — hard-typed `MONO_CAP_GROUND = "rgb(26, 26, 26)"` /
   `MONO_CAP_INK = "rgb(255, 255, 255)"`, mode-stable. Red 12×. Re-pointed to READ THE TOKEN live in
   each state (a scratch element, because a custom property returns its declared *text* while a
   background-color returns the resolved *rgb*), pinned additionally in mono/**light** to
   `rgb(240, 240, 240)` — the pixel Dave's own export resolved — and the non-mono scope check
   sharpened from "≠ the mono ground" to "**unpainted**".
   ⚠ **The expectation is no longer mode-stable, and that is a real consequence of the
   supersession**: `--surface-subtle` is `rgb(240,240,240)` in mono light and `rgb(31,31,31)` in mono
   dark. Dark falls out of the tokens; **no dark-mode value was invented**.
2. **`verify_grids_218`, the snap ladder** — drove `((7,8),(13,12),(22,20),(40,24),(1,1))`, the
   `s217-D6` eight-stop ladder. Three of those five stops **no longer exist** under `s219-D1 (4)`.
   The raw off-snap probes stay (landing between stops is the whole point); the wanted stop is now
   computed by `gen_bento_matrix_217.snap()`, the one home for the rule.
3. **`verify_grids_218`, the tight ABSENCE** — asserted *"no Tight button on dashboard main
   spacing"*, a hard-typed absence from `s217-D5`. `s219-D1 (2)` puts every option on every dial and
   lane A enacted it, so the button is present and the probe went red.
   ⛔ **This one is a ruling-shaped question and the probe must not settle it.** Whether "never
   tight" survives as a ROLE rule is enact-A's **Q2, open, Dave's**. So the assertion was re-pointed
   AT CAUSE: the dial must offer **exactly** the option space `gen_bento_matrix_217.DASH_MAIN`
   defines. That statement is true under *either* reading — whichever way Dave rules, the ruling
   lands in `DASH_MAIN` and the probe follows without an edit — and the printed line names the open
   question so a green cannot be read as an answer.
4. **The three re-cut generators' selftests** — bites asserting the retired ground by name (§3).

⚠ **`verify_bento_roles_217` and `verify_gallery_compare_217` never measured the caption ground at
all**, so they were blind to this class rather than wrong about it. Their pages ARE gated, but
statically, by their generators' selftests. Named as a gap, not repaired: a browser assertion on
those two is real work and nothing today needs it.

## 7 · The sitting index, re-struck — 34 → 33

The sitting index has **no generator**; its own report says the page IS its source, deliberately
(*"a one-sitting index whose content is a snapshot of one day's open calls has nothing to regenerate
from"*). So the re-strike is an edit to the page, emitted as
**`reviews/SITTING-219-2026-08-25-v2.html`** beside a frozen v1.

- **EYE 2** — *"Does the gallery role's default edge flip from ragged to square?"* → **STRUCK**,
  `Ruled · s219-D2 (2)`, with the verbatim clause and the store divergence from §4 named on the card.
- **EYE 4** — the crop bound → receipt moves to `s219-D2 (2)` and it carries a second tag,
  **"Left open BY NAME"**. This call got *bigger* today: the pass now reaches more walls and the
  ruling declined to bound it. Now links `SQUARING-PORTRAIT-2026-08-25-v1.html` — lane B's evidence
  page for the flattened portrait (tile 247, `stocksy-6629948`, 1×2 → 3×1).
- **EYE 11** — the photography sign-off. Not closed; **re-described**, because the page is no longer
  the page he would have been signing off: grey captions, console capsules, legacy keylines,
  per-theme gutters 40/24/40/1.
- **Every link re-pointed** to v6/v7/v3 (14 rewrites).
- **⚠ Keys are NOT renumbered.** `EYE 5` means what it meant this morning in every report that cites
  it; sliding numbers up to close a gap silently repoints every citation.

**Counts reconcile by probe, not by typing:** 34 cards · 1 struck · **33 open** = 10 EYE + 18 WORD +
5 REC; header 33, footer 33, tally 10/18/5. **68 of 69 hrefs resolve** (file exists *and* the named
fragment id is present in the target's bytes); the 69th is this report, which now exists.

⬛ **DECLARED, and it is the honest half of the count:** the two enact lanes filed **fourteen**
further ruling-shaped questions. They are **named in a banner on the page and cited by path**, and
they are **not indexed as cards** — indexing is a derivation with its own dedupe and store probe, and
that is the sitting lane's job, not the reconcile seam's. The page says *"33 indexed, 14 filed and
un-indexed"* in as many words rather than rounding them into the number at the top.

## 8 · Verification — driven, verdicts quoted

Env: `PYTHONPATH=/var/tmp/pylibs-s219l1` · `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215` ·
`FONTCONFIG_FILE=/var/tmp/fonts-219eb.conf` · `TMPDIR=/var/tmp` ·
`LD_LIBRARY_PATH=/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu`. `tiktoken` installed
first. Per lane B's finding 11 the font farm was **`ls -la`'d, not trusted**: every symlink in
`fonts-219eb/` resolves into *this* session's mount. `chromelibs-s213e2` `ls -A`'d — 2 entries, not
hollow.

| probe | verdict |
|---|---|
| `_bento_recut_219 --selftest` | `OK (8 bites) — struck/open per page: canon 6/3 · roles 8/1 · compare 9/3` |
| `gen_bento_canon_217 --selftest` | `OK (8 bites: … squaring + control · every wall square · mutation handle)` |
| `gen_bento_roles_217 --selftest` | `OK (9 bites: … gallery unsquared but still aspect-mapped · non-exempt walls square · role mutation handle)` |
| `gen_gallery_compare_217 --selftest` | `OK (8 bites: A is canon's own output · B cannot reach A · … the mutation handle mutates)` |
| `gen_bento_matrix_217 --selftest` | `OK — 73 bites.` (after `--rails` re-run: rail `[1,2,4,16,24,40]`, 10 dials, defaults `gen_foundations_217.ROLE_DEFAULTS`) |
| `role_defaults_219 --selftest` | `OK — 12 exports parsed …` |
| `gen_foundations_217 --check` | `OK — 7 page(s) in sync.` |
| `_gen_chain.py --check` | `✅ _CHAIN.md is FRESH — byte-matches the live chain` |
| `_state.py --selftest` | `57 bites, all GREEN` |
| `_gate_doc_rows.py --check` | `✅ PASS — every in-scope document has a store row.` (population 81, unrowed 0) |
| `verify_foundations_217 --page photography` | `OK — 8 state(s), no dangling property, theme reached the paint in all four.` |
| `verify_bento_matrix_217` (**no `--src`**, the SHIPPED page) | `OK — 4 state(s), three types driven, 7 dial(s) measured in pixels, both legality rules refused with reasons, export parity green, no dangling property.` |
| `verify_bento_canon_217` | `ALL GREEN — 8 states: … bottom edge at 4 widths · portrait two-row.` |
| `verify_bento_roles_217` | `ALL GREEN — 8 states: … gallery ragged-tolerance exercised …` |
| `verify_gallery_compare_217` | `ALL GREEN — 8 states: B justifies flush … widows unscaled and the switch driven both ways …` |
| `verify_photography_218 --static` | `✅ … 251 tile(s) parsed from the shipped markup` |
| `verify_photography_218 --themes` ×2 | `✅` — all four themes × light/dark. Legacy shows `borders [0, 1]`: `s219-D2 (4)` visible in the paint |
| `verify_grids_218 --page` ×4 + `--library` | `OK — 8 state(s) …, controls driven.` ×4 · `OK — the Grids group renders …` |
| `verify_segmented_219` | `PASS — every track and thumb radius equals its theme's minted token …` (128 measurements, 32 cells) |
| SITTING v2 browser drive | `OK — 8 state(s): strike renders struck with its receipt · new chrome takes every theme and clears AA · ground byte-matches the page the chrome was copied from, at settle.` 0 pageerrors / 0 console / 0 failed requests; lowest contrast **6.26:1** |

**Both lanes' declared UNPROVEN items that this seam could discharge, discharged:**
- lane A ①: `showroom/_foundations/bento.html` was never regenerated, so their green was measured on
  a non-repo build. **Regenerated, and their verifier re-run against the SHIPPED page with no
  `--src`. Green.**
- lane B ②: the explorer and the four `grids-*` pages were not regenerated. **All five regenerated
  and all five re-driven. Green** — and that is what surfaced findings 6.2 and 6.3.

## 9 · Findings

1. **A ledger can go stale inside one working day** — and the interval that matters is not "since
   the last session", it is "since the last inscription". [[read-chain-is-where-staleness-is-free]]
   in its sharpest form: the copy was written and superseded by the same afternoon's rulings.
2. **The refusal is what made the repair honest.** `open_control_html`'s "a settled question may not
   be re-put as a live control" turned Q6's flip into two hard generator errors instead of a silent
   pass. A gate that costs you work at exactly the moment you would have cut a corner.
3. **★ A hard-typed expectation cannot tell a page that broke from a ruling that moved** — and it
   fails in the *dangerous* direction, redding the ruling. Four instances in one seam (§6). The
   general repair is the same each time: address the one home for the ruled value
   (`matrix.snap()`, `matrix.DASH_MAIN`, `foundations.BG_FALLBACK`/`CAP_INK`), never re-type it.
4. **A red probe is not a licence to answer an open question.** The tight-button red (§6.3) sat
   exactly on enact-A's Q2. Re-pointing the assertion to the *option space* rather than to either
   reading kept it green **and** kept the question open — and the probe now prints the open question
   beside its green so nobody can read the pass as a ruling.
5. **`--check` red is not always the checking lane's fault, and the reverse is also true.** Lane B
   correctly warned the conductor not to read their `--check` red as theirs. But three of the five
   pages they named carried drift from BOTH lanes, which is only visible once both have landed —
   the seam is the first place the question can be asked at all.
6. **The store's own refusal caught a real ordering error.** `_state.add()` REFUSED `W-185` with
   *"home UNRESOLVABLE"* because this report did not exist yet, and rolled the transaction back
   clean — `_state.json` was unchanged after the failure. The row was minted after the file existed.
7. **The chain's staleness had a cause nobody edited.** `_CHAIN.md` was red with all three of its
   inputs clean at HEAD — it is generated from the STORE, and the store grew. Worth naming because
   the reflex reading of a stale chain is "somebody edited GOOD-MORNING".
8. **`s219-D2 (1)` cost mode-stability, and that is a consequence rather than a defect.** The #218
   rider resolved `#1A1A1A` in mono light AND dark by construction; `--surface-subtle` does not.
   Dark now falls out of the tokens in both directions and no dark-specific value was invented — but
   the probe that asserts it had to become mode-aware to stay honest.
9. **Two Dave-owned store rows have rotted their home pointers**, and neither was reworded (§10).

## 10 · ⬛ FOR THE CONDUCTOR — not repaired here, deliberately

- **`W-172` (owner `dave`)** — its title names `BENTO-CANON-2026-08-25-v4.html`, `-v5.html` and
  `GALLERY-COMPARE-2026-08-25-v2.html`, all three now superseded; its `closes_when` lists **Q6**,
  which `s219-D2 (2)` closed today.
- **`W-181` (owner `dave`)** — home is `reviews/SITTING-219-2026-08-25-v1.html`, superseded by v2.

Both are the [[home-pointer-rot-class]]. **Rewording a Dave row is not this seam's to do**, so the
new rows **address** the old ones through `links` (`W-183 → W-172`, `W-184 → W-181`) and the rot is
named here for his eye.

**Store rows minted** (nothing existing touched): `W-183` the three seam-5 pages · `W-184` the
re-struck sitting index · `W-185` this report.

## 11 · UNPROVEN / CLAIMED (ADR-0016)

1. **Nothing was looked at by eye.** Every verdict above is a MEASUREMENT — computed styles,
   rendered boxes, byte comparisons, link resolution. **No screenshot was opened in this seam.**
   Dave's eye is owed on all four new pages, and lane B's is owed on the photography page.
   Bounded verification (`s172-D3`); the residual is named rather than implied.
2. **The four re-cut/index pages were driven at ONE viewport width** — 1180 for the sitting index,
   the probes' own widths for the three bento pages (which do drive 1500/900/680/560 for the bottom
   edge). No narrow-width pass over the sitting index's new banner and struck card.
3. **The mutation arms were NOT re-driven after the regen.** `--no-square`, `--wrong-role`,
   `--break-justify`, `--break-settings`, `--break-default`, `--group-mutation`, `--dash-mutation`,
   `--overlay-mutation` and lane A's four page-level arms all BUILT before this seam and were seen
   red by their own lanes, but none was re-run against today's regenerated pages. Priced small;
   not done. ⚠ Pothole inherited from lane A: `/var/tmp` is shared and a foreign session owns
   `bento-matrix-*.html`, so `BM_MUTANT_DIR` must point at a fresh session-suffixed directory.
4. **`verify_bento_roles_217` / `verify_gallery_compare_217` do not measure the caption ground**
   (§6). Those two pages' captions are gated statically by their generators' selftests only.
5. **No repo-wide CI sweep was run**, and no `_build_all.py` end-to-end. Steps were driven
   individually, as briefed.

## 12 · REPLAY-THESE (conductor)

- `python3 knowledge/_render/_bento_recut_219.py --selftest` — the 3 new bites are the finding-12 gate.
- `python3 knowledge/_gen_chain.py --check` · `python3 knowledge/_state.py --selftest` ·
  `python3 knowledge/_gate_doc_rows.py --check`
- `python3 knowledge/_render/gen_foundations_217.py --check` — must read `7 page(s) in sync`.
- **Dave's eye owed on FOUR new pages:** `reviews/BENTO-CANON-2026-08-25-v6.html`, `-v7.html`,
  `reviews/GALLERY-COMPARE-2026-08-25-v3.html`, `reviews/SITTING-219-2026-08-25-v2.html`.
- **Put to Dave, unresolved by this seam:** enact-A Q1–Q7 and enact-B Q1–Q7 (fourteen), the two
  rotted Dave rows (§10), and the four un-indexed-in-the-sitting-page questions the v2 banner names.
- ⛔ **The one that changes the most if he says yes:** enact-B **Q1** — flipping
  `layout/bento/$roles/gallery/squaring` to `true`. It is a canon regeneration, it runs the ordered
  serial, and it changes every gallery bento in the repo including surfaces nobody has opened. Three
  pages currently carry a **declared divergence** paragraph waiting on that one word.
