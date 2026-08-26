# #219 lane C (enact) — the CHORD/CONSTRAINT LAYER, the pageBg re-scope, and the rails library

**Lane:** enact-C, #219. **Model:** Opus. **Charter:** `s219-D3`, verbatim.
**Scope:** the whole bento surface — the option grammar, the constraint layer, the resolver, the
foundations pages and one new library page. No concurrent lane.

**Files this lane owns and touched:** `knowledge/_render/gen_bento_matrix_217.py`,
`knowledge/_render/gen_foundations_217.py`, `knowledge/_render/gen_grids_218.py` (one filter line),
`knowledge/_render/gen_library_214.py` (one FOUNDATIONS entry),
`knowledge/_render/verify_bento_matrix_217.py`, `knowledge/_render/_bento_edit_rails.json`
(regenerated), `showroom/_foundations/bento.html`, `showroom/_foundations/bento-rails.html` (NEW),
`showroom/_foundations/grids-{display,gallery,dashboard}.html`,
`showroom/_foundations/photography.html`. (`logos.html` and `grids-12col.html` were rebuilt and
came out byte-identical — they carry no bento dial.)

**Not touched:** `knowledge/_rulings.json`, `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md`,
constants/bands/thresholds/stop lines, any Dave-owned row, `notes/_receipts/**` (frozen history),
canon, the project-types axis (`s219-D3(7)`, PARKED). No commit. No regen serial.

**COUNTS:** findings 11 · ruling-shaped 5 · UNPROVEN 4 · new gates 21 selftest bites + 2 browser
arms + 1 blocking mint-time sweep · files changed 6 + 1 new page · store rows minted 2

---

## 1 · The constraint layer — one vocabulary for every refusal

`s219-D3(2)` asks for "legal chords plus exclusion rules per theme × type intersection", and a
validator that "refuses illegal combinations". Three things landed in
`gen_bento_matrix_217.py`, and they are deliberately not the same thing:

| | what it is | where |
|---|---|---|
| **The ink rule** | ground word → ink token. A DERIVATION, not a dial. | `INK_FOR_GROUND` / `ink_for()` |
| **The chords** | named sets of dial values that settle together, SCOPED to theme × type | `CHORDS` / `chord_members()` / `chords_for()` |
| **The exclusions** | named refusals, each with plain words | `EXCLUSIONS` / `chord_refusals()` |

**The #217 legality rules were EXTENDED, not replaced.** P2 and P3 are now X1 and X2 and the chord
validator **calls** `caption_legal()` / `capsule_legal()` rather than restating them, so a rule
fixed in one place is fixed in both. The manifest's `legality` block keeps its `P2`/`P3` ids and
gains a `now` field pointing at the X-name, so the older receipts still resolve.

**Six exclusions, and every one carries `plain` — the words the library page prints:**

| | in plain words | from | status |
|---|---|---|---|
| **X1** | A caption cannot sit on its own colour. Grey on grey has no edge. | P2 | proposed |
| **X2** | A capsule needs an edge. Give the caption a ground, or turn keylines on. | P3 | proposed |
| **X3** | Text colour is not a dial. It follows the ground underneath it. | s219-D3(2) | ruled |
| **X4** | Every ground on offer has to be readable. Anything under 4.5:1 is not offered. | s219-D3(2) | ruled |
| **X5** | Capsule and Rounded are two answers to one question. Pick one. | s219-D3(2) | ruled |
| **X6** | The dark caption ground belongs to the console capsule chord. Whether mono may have it is an open question for Dave. | s219-D3(3) | **OPEN** |

**Both directions are driven.** `C1c` asserts the ruled chords come back with an EMPTY refusal
list at their own intersection — an empty list is a positive statement, not the absence of a test —
and `C2b`–`C2e` assert the named refusals. `C2c` drives the scope check across all four themes and
both chordless types.

## 2 · The two ruled chords (s219-D3(3)) — console gallery only

```
capsule   settles rounding=capsule
          ranges  capBg over the grey ramp: grey · white · DARK GREY
          ink     follows capBg, automatically
rounded   settles rounding=corners + capBg=transparent
```

**Two is the whole set.** No third chord was inferred for the other three themes, for the other two
types, or for dials the ruling did not name. `scope` is a list, so a widening is data rather than a
rewrite.

**`settles` is fixed; `ranges` is the choice inside the chord.** "Caption ground from the grey ramp"
is a SET, and flattening it to one ground would have picked for him. The capsule chord therefore has
three members and the rounded chord has one.

**The dark ground is s218-D6(1)'s, returning at a different permission level.** It was retired as
the mono DEFAULT by s219-D2(1); it comes back as a console chord OPTION. Same colour, different
level — which is s219-D1's default-vs-option split working exactly as ruled.

**Measured live in the browser, console, both modes** (`--text-secondary` on the light grounds,
`--text-reverse` on the dark, never picked by a solver — the pairing is Dave's own):

| chord ground | light | dark |
|---|---|---|
| grey (`--surface-subtle`) | 15.27:1 | 16.48:1 |
| white (`--surface-raised`) | 17.40:1 | 16.48:1 |
| **dark grey (`--surface-digital-black`)** | **17.40:1** | **17.40:1** |

## 3 · The blocking contrast sweep, and the thing it is measured against

`chord_sweep()` gates **27 rows**: every chord ground at every scoped intersection, every section
ground in all four themes (`s219-D3(5)`), and every page-rail member (`s219-D3(4)`) — because the
effective-ground chain ends at the page, and a sweep that stopped at the wall would leave the
commonest state on any page unmeasured. Light AND dark. A reading under 4.5:1 is a selftest
**FAILURE**, not a note.

**Lowest reading 5.93:1 — legacy dark, the same floor lane B measured live.**

**The measurement reuses lane B's, it does not duplicate it.** `effective_ground_word()` is named in
the source as the WORD-LEVEL TWIN of `verify_photography_218._effective_ground` — same rule, different
unit (dial words at mint time vs resolved `rgba()` in the browser). The ratio itself is
`knowledge/_contrast_utils.contrast_ratio`, the repo's one implementation, addressed not re-written.

**The token resolver is cross-checked before any gate stands on it.** `theme_tokens()` reads
`canon.css` by canon's own cascade (`:root` → `[data-theme="dark"]` → theme block → theme dark
block). Bite `C0` asserts eight of its values against pixels **lane B measured in a browser** at
#219 — `#F0F0F0`, `#1F1F1F`, `#545454`, `#9B9B9B`, `#F7F6F4`, `#DFDEDC`, `#1A1A1A`, `#FFFFFF`. All
eight agree. `C0b` asserts a dangling token RAISES rather than returning a plausible black
([[dangling-dataviz-var-renders-silent-black]]).

## 4 · pageBg leaves the grammar (s219-D3(4)) — and NOTHING REGRESSED

**The dial is gone.** `pageBg` is absent from `dials`, absent from every type's dial list, and
absent from the bento enumeration. It is present as a sibling, `page_rail`, with `level: "page"`.

**The rail is three words, and the first one is why nothing moved:**

| word | token | mono light | mono dark |
|---|---|---|---|
| `page` | `--background-default` | `#FFFFFF` | `#1A1A1A` |
| `white` | `--surface-raised` | `#FFFFFF` | `#1F1F1F` |
| `grey` | `--surface-subtle` | `#F0F0F0` | `#1F1F1F` |

The twelve shipped defaults spell the page ground `grey`/`white`/`transparent`. On a page body
`transparent` **never meant "paint nothing"**: `gen_foundations_217.page_bg_decl()` already
compiled it to `--background-default`, because a body that paints nothing falls through to the UA
canvas (white, in dark mode too — lane B's finding 6). So the rail names that ground `page`, and
`PAGE_RAIL_WORD` — typed once — sends the old word to it. **Same declaration, same pixels, a word
that no longer lies.** Receipts and exports under `notes/` keep the old word and were not touched.

**NO DARK EQUIVALENT NEEDED A CHOICE, so nothing landed PROPOSED.** Every rail member is a token
that already carries its own dark value; `s219-D3(4)`'s "dark equivalents to be derived from
tokens" is satisfied by derivation.

**THE NO-REGRESSION PROOF, MEASURED, not asserted** (new browser arm, mono, both modes):

```
⬛ s219-D3(4) page rail · light · page ground rgb(255,255,255) == body rgb(255,255,255)
                       · dark  · page ground rgb(26,26,26)    == body rgb(26,26,26)
                       · one page-level control, survives the type switch
```

The explorer's `.bm-stage` paints no ground of its own, so `transparent` fell through to the page
body; `page` declares that same colour by name. The arm reds if they ever diverge.

**Second proof, on the shipped gallery.** `verify_photography_218 --themes` re-driven in all four
themes × light/dark: **all eight states identical to lane B's pre-re-scope readings**, page grounds
included (mono `rgb(255,255,255)`/`rgb(26,26,26)`, legacy white, supercharge `rgb(247,246,244)`,
contrast floor 5.93). Zero pixels moved.

**On screen it is now ONE control, owned by `page`, that survives a type change** — which is what
"page-level" means when you can see it. The four `grids-*` pages keep it: `gen_grids_218.controls_for()`
now names the page group explicitly, so the re-scope did not silently delete a dial from four pages.

## 5 · bentoBg is the section ground (s219-D3(5))

The dial stays and widens to the full light AND dark ramp: `grey` · `white` · **`darkgrey`** ·
`transparent`. The ramp is the TOKENS — `--surface-subtle`, `--surface-raised`,
`--surface-digital-black` — and no fourth was minted. A transparent caption's ink is measured
against the effective ground, which is this one, and the stylesheet says so:
`[data-bento-bg="darkgrey"][data-cap-bg="transparent"] .bm-cap{color:var(--bm-ink-rev)}`.

**The reachable counts move, and the shape that reports them was already right.** pageBg's ×3
leaves; the section ground goes 3 → 4; the caption ground is theme-dependent again:

| | display | gallery | dashboard | total |
|---|---|---|---|---|
| mono / legacy / supercharge | 48 | 648 | 288 | **984** |
| **console** | 48 | **864** | 288 | **1200** |

Console is larger **by a chord scope, not a theme lock** — no dial is removed anywhere, the keyline
switch is still present in all four themes, and the browser arm asserts the difference is exactly
`darkgrey` and that it has not leaked out of the gallery.

## 6 · The rails library — `showroom/_foundations/bento-rails.html` (NEW, generated)

`s219-D3(6)`, enacted literally: **the page reads `_bento_edit_rails.json` and nothing else.** Not
the option lists, not the chord objects, not `capbg_for()` — the FILE. If it could reach the Python
it would be a second consumer of the source and the manifest would stop being load-bearing. The
page says this in its own first paragraph.

Written for Dave's eye: short lines, **one chord per card**, live specimens.

- **Chords** — one card per chord member, each with a **live specimen**: real photograph, real
  canon tile, painted by the **explorer's own stylesheet**. The console capsule measures a 20px tile
  radius; the rounded chord measures a 20px image box and a square tile. The default is pilled
  `THE DEFAULT`; every card prints its ground, its ink token and its light/dark ratios.
- **Page background** — its own section, three specimens, the re-scope and the light-mode collapse
  stated in plain words.
- **What excludes what** — the six rules, plain words first, then where each comes from and whether
  it is ruled, proposed or **OPEN**. X6's open question is repeated below the table in full.
- **The full option space** — three tables, one per type, all four themes, every dial's options with
  the shipped default in bold, the chords at that intersection and the exclusions that reach it.

Registered as a Foundations entry (`foundation-bento-rails`, sibling of `bento.html`, not grouped —
grouping would pre-empt the library IA v2 word-set, W-99zg).

**Verified in the browser, all four themes × light and dark, no dangling property** — and looked at
first-hand: eight full-page shots plus eight section shots at `/var/tmp/shots-219c/`, copied to
`_to_delete/_shots219c/` for the conductor.

## 7 · Three defects found by LOOKING, not by a gate

1. ⛔ **A pinned theme on a nested element rendered the PAGE's theme, silently.** The explorer
   defines `--bm-container-radius: var(--border-radius-container,0px)` on `.bm` — the BODY — so it
   resolves once, against the page's theme. A specimen carrying `data-apollo-theme="console"` on a
   nested div inherited the already-resolved value: **the console capsule measured 0px radius while
   the console theme was 20px, and every var resolved to something, so nothing could go red.**
   Fixed at cause: `_spec_vars()` lifts the `.bm{…}` block out of the captured stylesheet by its
   selector and re-emits it under `.br-spec`, so the vars re-resolve at the specimen. **DERIVED,
   never retyped** — a new `--bm-*` arrives on the next build — and it RAISES if the selector ever
   stops matching.
2. **The exclusions table overlapped its own columns**, and two fixes failed before the cause was
   measured: the shared Foundations stylesheet puts `white-space:nowrap` on table cells, so
   `max-width` (advisory under auto layout) and then `table-layout:fixed` both looked right in the
   markup and still clipped on screen. Asked the DOCUMENT what it computed; fixed in one line.
3. **Two tiles per specimen** put the second photograph below the fold of every card. One tile.

## 8 · A gate that had never been seen to fail

The `--break-legality` mutant removed the refusal rules and reported **OK** with 5 assertions red —
and said **nothing at all about X6**, because the new arm's failures were not tagged
`legality=True` and so were not in the falsifiability bucket the arm counts. Tagged. The arm now
reports **11 assertions red**, including all six X6 assertions across mono, legacy and supercharge.
[[instrument-without-a-consumer]] — caught by driving the mutant, not by reading the code.

## 9 · The three required mutants, each RED BY NAME

- **`C5` — AN ILLEGAL CHORD SNEAKS IN.** A third chord granting mono the dark caption ground.
  ⚠ **It measured only half of what it was written to measure, and the bite says so:** the scope
  check PASSES, because the arm declared its own scope — the refusal machinery cannot catch a chord
  that grants itself permission. What it cannot fake is the DERIVATION: `capbg_for()` is computed
  from `CHORDS`, so the arm widens mono's reachable grounds, and that is what the bite asserts.
- **`C6` — A CHORD VIOLATES AN EXCLUSION.** The capsule chord's ground set widened to
  `transparent`; **X2** refuses it by name (a capsule with no edge).
- **`C7` — INK DOES NOT FOLLOW GROUND.** The dark ground re-pointed at the light ink. **X3** reds by
  name AND the blocking sweep reds: `#1A1A1A` on `#1A1A1A` is 1.0:1.
  ⚠ **It reds in LIGHT only, and that is a measurement not a gap:** in dark mode `--text-secondary`
  already resolves to white, so the wrong token happens to paint the right colour. **A gate that ran
  in one mode would have called this arm green.**

Plus the deep-copy trap: `[dict(c) for c in CHORDS]` shares each chord's `ranges` object, so an arm
mutating a range survived its own `finally` and poisoned every bite after it. Caught by a red.

## 10 · Green

```
gen_bento_matrix_217  --selftest     94 bites   (was 73; 21 new: C0–C9)
gen_bento_matrix_217  --rails                   manifest regenerated, drift gate R6d green
gen_foundations_217   --selftest     39 bites
gen_foundations_217   --check                   8 page(s) in sync
gen_grids_218         --selftest     16 bites
gen_library_214       --selftest     38 bites
role_defaults_219     --selftest                12 exports parsed
verify_bento_matrix_217 --themes mono,console            OK
verify_bento_matrix_217 --themes legacy,supercharge      OK
verify_bento_matrix_217 --mutation                       11 refusals falsifiable
verify_photography_218 --static                          251 tiles, 0 holes
verify_photography_218 --themes (all four)               8 states, min 5.93:1
verify_photography_218 --default-mutation                RED as required, 2 by name
verify_foundations_217 --page bento                      8 states
verify_foundations_217 --page bento-rails                8 states
```

Render-verify env: fifth stratum `/var/tmp/chromelibs-s213e2` (`ldd` → 0 "not found"),
`PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215`, `PYTHONPATH=/var/tmp/pylibs-s219l1`,
`FONTCONFIG_FILE=/var/tmp/fonts-219eb.conf` (lane B's farm, `ls -la`'d — it points at THIS
session's mount, `fc-match` confirms `HSBC_MtUnivers_Latin`), `TMPDIR=/var/tmp`. tiktoken first.
Font probe on every browser run: target **347** · real control **375** · absent control **301**.

## 11 · Findings

1. The constraint layer is ONE vocabulary: P2/P3 became X1/X2 by being CALLED, not restated.
2. The static token resolver and lane B's live browser readings agree on all eight shared values.
3. The whole 27-row sweep clears the floor; the worst reading is legacy dark, 5.93:1.
4. The pageBg re-scope moved **zero pixels** — proved twice, in the explorer and on the shipped
   photography wall.
5. `page` and `white` are the SAME colour in LIGHT mode in all four themes and differ only in dark.
   Both kept; the pair is a real distinction the tokens make. **Surfaced, never swapped.**
6. ⚠ **`grey` and `white` collapse in DARK mode** (`--surface-raised` = `--surface-subtle` = `#1F1F1F`
   in mono/legacy/console). This is lane B's finding 9 arriving in the chord layer: the capsule
   chord's grey and white members are **indistinguishable in dark mode**, and the sweep prints both
   at 16.48:1. The chord offers a choice that is invisible in half the modes. **Surfaced, not
   repaired** — a dark-specific ground would be a CHOICE and Dave's.
7. **The capsule's WHITE member is invisible on a white page.** On the library card the white
   caption ground sits on a white page ground, so the capsule reads as no capsule at all. That is
   the honest truth of the option and it is worth his eye rather than a staged darker card.
8. Console gallery's count is larger by a **chord scope**, not a theme lock — a distinction the
   per-theme count shape lane A kept deliberately was able to express without being changed.
9. `supercharge`'s ramp is warm throughout (`#F7F6F4` / `#DFDEDC` / `#13110E`). Standing grey-tint
   rule: surfaced, never auto-swapped.
10. The `--bm-*` variable block is now consumed in two places (the explorer body and `.br-spec`).
    It is DERIVED from the one home by selector, so there is no second copy — but the derivation is
    a regex over generated CSS and it raises rather than degrading.
11. ⛔ **`showroom/index.html` + `index.json` are OUT OF SYNC** because the new Foundations entry
    needs the library index regenerated — and that is the regen serial's LAST step, which this lane
    was told not to run. Owed at the regen seam. The new page is on disk and reachable by URL; it
    is the INDEX that has not caught up.

## 12 · RULING-SHAPED QUESTIONS — for Dave

1. ⬛ **MONO'S ACCESS TO THE DARK-CAPTION CHORD.** `s219-D3(3)` says EXPRESSLY OPEN. **Nothing here
   grants it:** `capbg_for('gallery','mono')` does not carry `darkgrey`, exclusion **X6** refuses
   it in mono, legacy and supercharge, and the refusal prints the OPEN QUESTION as its reason
   rather than a preference — an option refused with a preference reads as settled, one refused
   with a question reads as open. The dial still OFFERS the option (struck through, with the
   reason beside it), so the question is visible on the page rather than absent from it.
   **Does mono get the capsule chord's dark caption ground?**
2. **Does the dark caption ground belong to the capsule chord, or to the caption dial?** Enacted as
   the chord's (X6), because `s219-D3(3)` introduces it inside a chord. The alternative reading is
   that the ramp widens for `capBg` everywhere and the CHORD merely names a coherent selection —
   which would grant mono the ground by implication, so it is not a reading this lane could take.
3. **`grey` and `white` are indistinguishable in dark mode** (finding 6). The capsule chord
   therefore offers three grounds in light and two in dark. Acceptable, or does the caption ground
   want a dark-mode ramp of its own? That would be a dark-specific CHOICE — nothing was invented.
4. **X1 and X2 are still PROPOSED** (they were P2/P3 and `s217-D5` left them open). They now sit
   in a layer whose other four rules are RULED, and the library page prints all six side by side
   with their status. **Promote, or keep the mixed status visible?**
5. **The page rail's `page` and `white` collapse in light mode** (finding 5). Three words, two
   distinct light colours. Keep both, or is the rail two members plus a dark-mode note?

## 13 · UNPROVEN, declared

1. **The library index is stale** (finding 11). `gen_library_214 --check` reds on
   `showroom/index.html` and `index.json`. NOT RUN — index is the serial's last step and the brief
   forbids the serial. **Owed at the regen seam.**
2. **The new page has no thumbnail.** `gen_library_214 --selftest` reports
   `residual · missing thumbnail: 1` — `gen_thumbs.py` is a browser pass and was not run for it.
   Degrades to a placeholder and is REPORTED, never faked.
3. **The other three matrix mutation arms were not driven.** `--break-layout`, `--break-inner` and
   `--break-keylines` remain lane A's UNPROVEN ② — only `--break-legality` (which is the arm the
   new refusals live in) and lane B's `--break-default` were driven this lane.
4. **The chord specimens were driven at 1280×900 only.** The library page's cards are a responsive
   grid (`auto-fit, minmax(320px,1fr)`); the canon container-query bands were not re-driven at
   narrow widths on this page. The explorer and the grids pages WERE (1000/700/500, green).

## 14 · REPLAY-THESE (conductor)

- `python3 knowledge/_render/gen_bento_matrix_217.py --selftest` (94 bites, C0–C9 are s219-D3's)
- `python3 knowledge/_render/gen_bento_matrix_217.py --rails` — after ANY option-grammar change
- `python3 knowledge/_render/gen_foundations_217.py --selftest` then `--check`
- `python3 knowledge/_render/verify_bento_matrix_217.py --themes mono,console` — the s219-D3 chord
  and page-rail arms print their readings
- `BM_MUTANT_DIR=/var/tmp/mut-<session> python3 knowledge/_render/gen_bento_matrix_217.py
  --break-legality` then `… verify_bento_matrix_217.py --mutation --themes mono,console` — must
  report **11** falsifiable refusals, not 5
- `python3 knowledge/_render/verify_foundations_217.py --page bento-rails`
- ⛔ **At the regen seam:** run the ordered serial and let `gen_library_214.py` (index LAST) pick up
  the new Foundations entry, then `gen_thumbs.py` for `foundation-bento-rails`.
- **Dave's eye owed on:** `showroom/_foundations/bento-rails.html` — the three capsule grounds side
  by side (finding 7, the white member is invisible on white), and the dark-mode collapse
  (finding 6). Shots at `_to_delete/_shots219c/`.
- Put questions 1–5 to Dave. **Question 1 is the one `s219-D3(3)` expressly left him.**
