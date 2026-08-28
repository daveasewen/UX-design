# `#222`-mono-default-switch — mono's gallery default becomes square + transparent, and the last grey caption ground goes by ruling

session: `#222` · 2026-08-28
window: bento lane — enacting `s222-D1`, Dave's *"yes the defaults for mono are fine"* and, on the
reflected firm reading, *"yes this is correct"*
sub index: `mono-default-switch`
brief: `notes/_briefs/2026-08-28-222-mono-default-switch-brief.md`
tokens: `UNMEASURED` — a sub cannot read its own `message.usage`; the conductor's panel is the only
place this spend is real. Turn count from my seat: **~58 tool calls, one lane, no re-drives.**

## VERDICT

**DONE.** Mono's gallery ships **square image + transparent caption, identical in light and dark**,
enacted **AT CAUSE** as a **third entry in the supersession LAYER** of
`knowledge/_render/role_defaults_219.py` and derived everywhere else. **The #219 receipt is
byte-untouched** (md5 `127d222630ebab56398a531041f3602a`, `git diff notes/_receipts/` empty).
**ONE dial moved** — `capBg: grey → transparent`. **No option was removed**, asserted four ways and
visible as a one-line diff on the shipped rails page. **Console, legacy and supercharge are
untouched**, asserted in both directions. **The dark-chord question is untouched and still refuses
by name in the browser.**

Measured **in the browser**, on the regenerated `showroom/_foundations/photography.html`:

```
mono/light     tileR [0] · imgR [0]  · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(26, 26, 26)']   17.4:1
mono/dark      tileR [0] · imgR [0]  · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(255, 255, 255)'] 17.4:1
console/light  tileR [0] · imgR [20] · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(26, 26, 26)']   17.4:1  ← UNCHANGED
console/dark   tileR [0] · imgR [20] · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(255, 255, 255)'] 17.4:1  ← UNCHANGED
legacy/light   tileR [0] · imgR [0]  · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(84, 84, 84)']    7.57:1 ← UNCHANGED
legacy/dark    tileR [0] · imgR [0]  · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(155, 155, 155)'] 5.93:1 ← UNCHANGED
supercharge/light tileR [0] · imgR [0] · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(19, 17, 14)']  17.45:1 ← UNCHANGED
supercharge/dark  tileR [0] · imgR [0] · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(247, 246, 244)'] 16.11:1 ← UNCHANGED
```

The two mono rows carry the **same dials in both modes** — that is `s222-D1`'s "both modes", read
off the live document rather than argued from the table. `imgR [0]` beside console's `imgR [20]`,
**under the identical compiled rule**, is the whole "the square is the theme's own radius token"
claim, measured.

COUNTS: findings `7` · ruling-shaped `4` · UNPROVEN `4` · files changed by this lane `8` + 1 new report + 6 new asset files ·
role-defaults selftest clauses `+7` · foundations bites `44 → 46` · matrix bites `104 → 104` ·
browser verifier states driven `28` · mutation arms `5`, **before/after MEASURED** ·
advisory gates re-driven `2`

## THE MINT SITE, QUOTED

⛔ **THE DEFAULT MOVED WITHOUT THE RECEIPT MOVING** — the #220 shape, copied, not re-derived.
`role_defaults_219.py` **parses** Dave's twelve verbatim exports out of
`notes/_receipts/2026-08-25-219-role-defaults-exports.md`; that receipt is the module's only source
of defaults and `s219-D1 (3)` makes it the RECEIPT of what he approved. The parse is kept whole as
`RECEIPT_DEFAULTS` and the ruling is a **layer** over it. One new entry:

```python
    {
        "type": "gallery", "theme": "mono", "dial": "capBg",
        "was": "grey", "now": "transparent",
        "ruled_by": "s222-D1",
        "supersedes": "s220-D2 (3)'s EXPRESSLY OPEN clause · the s219-D1 (3) mono gallery "
                      "export's grey capBg (the s219-D2 (1) light-grey ground)",
        "modes": "both — one default, identical in light and dark",
        "dave": "yes the defaults for mono are fine — and on the reflected firm reading: "
                "yes this is correct",
    },
```

⛔ **AND ONE ENTRY HAD TO LEAVE A DIFFERENT TABLE, WHICH IS WHERE THE CARE WENT.**
`NO_SUPERSESSION` carried `("gallery", "mono")` as a **positive statement** that `s220-D2 (3)` had
left it open, and `_apply_supersessions` **refuses by name** when a supersession names an
intersection in it. That entry could not stay — but deleting it outright would erase the record
that the clause was ever open, and a later reader could not tell a ruling from an oversight. So:

```python
NO_SUPERSESSION = {}

NO_SUPERSESSION_CLOSED = {
    ("gallery", "mono"): "s220-D2 (3) left mono's gallery default (capBg: grey) EXPRESSLY OPEN — "
                         "asked in chat, not ruled. CLOSED by s222-D1 (#222, 2026-08-28), Dave: …",
}
```

⛔ **NO `rounding` ENTRY, AND THE PREMISE WAS RE-VERIFIED AT HEAD BEFORE THAT WAS DECIDED.** The
brief's premise ("mono's `--border-radius-container` resolves 0 in both modes") was **driven**, not
carried: `matrix.theme_tokens("mono", m)["--border-radius-container"]` →
`var(--border-radius-default)` → `0`, in **both** modes, against console's `20px`. Mono's #219
export already says `rounding: corners`, so the SAME compiled rule
(`border-radius:var(--border-radius-container,0px)` on `.px-img`) rounds console and squares mono.
A `rounding` supersession would have been an override that changes nothing, which the module's own
`was == now` gate refuses by name. **This is now bite `6k`, not a comment.**

### The generated CSS, verbatim from `showroom/_foundations/photography.html`

```css
/* ---- mono · spacing 40 (40px) · keylines off · bento · square edge · rounding corners ·
   page transparent · bento transparent · caption transparent ---- */
[data-apollo-theme="mono"] … .c-bento__tile{border-radius:0;}
[data-apollo-theme="mono"] … .c-bento__tile .px-img{
  border-radius:var(--border-radius-container,0px); overflow:hidden;}
[data-apollo-theme="mono"] … .c-bento__tile .px-cap{
  background:transparent; color:var(--text-secondary,#545454);}
```

Byte-for-byte console's rule, except the token each theme resolves. `transparent` carries no
`CAPTION_GROUND_MINT`, so the `#220` mode-flat fence (bite `6f`) is still un-tripped and one
declaration per theme serves both modes — `s222-D1`'s "both modes" needed **no new machinery**.

## BEFORE / AFTER — THE WHOLE TABLE

### The twelve shipped defaults, gallery row (the other eight are byte-unchanged)

| theme | rounding BEFORE | rounding AFTER | capBg BEFORE | capBg AFTER | moved? |
|---|---|---|---|---|---|
| **mono** | corners | corners | **grey** | **transparent** | **YES — s222-D1** |
| legacy | corners | corners | transparent | transparent | no |
| console | corners | corners | transparent | transparent | no — moved at #220 |
| supercharge | corners | corners | transparent | transparent | no |

**All four gallery defaults now agree on `transparent`.** Three of the twelve #219 exports carry a
supersession; nine are the receipt's own words, untouched.

### What the browser paints, mono gallery

| state | tile radius | image radius | caption ground | ink | ratio |
|---|---|---|---|---|---|
| light BEFORE | 0px | 0px | `rgb(240,240,240)` `#F0F0F0` | `rgb(26,26,26)` | 15.27:1 |
| **light AFTER** | **0px** | **0px** | **transparent → `rgb(255,255,255)`** | `rgb(26,26,26)` | **17.40:1** |
| dark BEFORE | 0px | 0px | `rgb(31,31,31)` `#1F1F1F` | `rgb(255,255,255)` | 16.48:1 |
| **dark AFTER** | **0px** | **0px** | **transparent → `rgb(26,26,26)`** | `rgb(255,255,255)` | **17.40:1** |

⚠ **THE TWO BEFORE ROWS ARE CARRIED, NOT RE-MEASURED IN A BROWSER THIS LANE** — they are the
`#220` receipt's own mono rows (`notes/_subreports/2026-08-27-220-default-switch.md`, VERDICT
block) and the pre-switch generator's computed values, which this lane **did** re-derive
(`--break-settings` BEFORE arm prints `dial says grey (--surface-subtle)` and the mutant resolves
`rgb(240,240,240)` in light). Declared rather than presented as this lane's raster
([[planning-estimate-is-not-a-measurement]]). Both AFTER states clear the ruled 4.5:1 floor by
**12.9**, and the dark caption's `#1F1F1F`-on-`#1A1A1A` near-invisibility (ΔL\* +2.49, the
theme-lift lane's open question 1) **is gone with the block** — the caption now sits on the page.

### Artefacts

| Artefact | Changed by this lane? | How that is known |
|---|---|---|
| `showroom/_foundations/photography.html` | **YES** (`+13/−7`) | the settings block + the receipt table's RETIRED marker |
| `showroom/_foundations/bento-rails.html` | **YES** (`+1/−1`) | reads the regenerated manifest — see below |
| `knowledge/_render/_bento_edit_rails.json` | **YES** (`+12/−1`) | `defaults.values` + a third `supersessions` row |
| `bento.html`, `grids-{12col,dashboard,display,gallery}.html`, `logos.html` | **NO** | the writer reported "8 page(s) → 2 written"; md5 before/after identical for all six |
| `knowledge/_render/index` / library | **NO** | `gen_library_214.py --check` **OK, 143 components in sync** — driven, not assumed |
| `reviews/MONO-GALLERY-DEFAULT-2026-08-27-v1.html` | **NO** | `cmp` byte-identical after the generator was re-run and REFUSED — finding 3 |
| `notes/_receipts/2026-08-25-219-role-defaults-exports.md` | **NO** | `git diff notes/_receipts/` empty; the module's own `was`-gate asserts it on every import |

⛔ **THE RAILS PAGE'S ENTIRE DIFF IS ONE LINE, AND IT IS THE "NO OPTION REMOVED" CLAIM MADE
VISIBLE.** `showroom/_foundations/bento-rails.html` moved mono's gallery `capBg` row from
`<b>grey</b> · white · transparent` to `grey · white · <b>transparent</b>`. **The option list is
character-identical; only the bold moved.** A reader of the shipped rails page can see that the
default changed and that nothing left the ramp.

## THE FOUR GUARANTEES, EACH ASSERTED SEPARATELY

⛔ A single "mono is transparent now" bite would go green on a build that silently dropped `grey`
from mono's ramp, dragged another theme along, or answered the dark-chord question
([[green-tests-cannot-see-scope]]).

**`6k` (foundations) — THE SWITCH, THE RECEIPT IT DID NOT REWRITE, AND THE RADIUS TOKEN.** Eight
clauses: the live mono pair is `("corners","transparent")`; the **receipt's** mono pair is still
`("corners","grey")`; `superseded_dials("gallery","mono")` is exactly `{"capBg": "grey"}`; only
`capBg` differs between live and receipt; `default_for_mode(…,'light') == default_for_mode(…,'dark')`;
the compiled `background:transparent` declaration is byte-present under the mono selector; so is the
`var(--border-radius-container,0px)` image rule; and the two-step token resolution is
`[("var(--border-radius-default)","0"), ("var(--border-radius-default)","0")]` for the two modes.

**`6l` (foundations) — NO OPTION WAS REMOVED FROM MONO.** `(corners,grey)`, `(corners,white)`,
`(corners,transparent)` and `(capsule,grey)` are each driven through `caption_legal` /
`capsule_legal` / `capbg_for` — **all legal, all reachable**; `capbg_for("gallery","mono")` is still
`["grey","white","transparent"]`; the **grey branch is COMPILED** on a settings table this page no
longer ships and emits `var(--surface-subtle,#F0F0F0)` ([[instrument-without-a-consumer]]); and the
live block carries that literal **nowhere**. ⚠ The bite also pins that mono's **darkgrey is still
refused by name** (X6, "not ruled yet") and **still absent from the ramp** — the status quo of an
open question, asserted so this lane cannot be read as having granted it.

**`6j` (foundations) — THE SIZE OF THE OPTION SPACE.** `counts_by_theme()` enumerates every legal
state out of the matrix's own option lists and never consults a default, so these numbers move only
if an option was added or taken away: gallery **648 / 648 / 864 / 648**, display **48**, dashboard
**288** — **including mono's 648, unmoved.** The bite now also asserts the supersession roster by
`(theme, dial, ruling)`, so a fourth entry nobody ruled reds here.

**`R6e` (matrix) — THE MANIFEST CARRIES BOTH RECORDS, FOR BOTH SWITCHES.**
`_bento_edit_rails.json` is what the library page reads (`s219-D3(6)`). It now carries three
`defaults.supersessions` rows against the frozen `defaults.receipt_values`, and the bite asserts
mono's live pair is `("corners","transparent")` **while the receipt's is `("corners","grey")`** —
the two records disagreeing in exactly the ruled way — plus mono's unnarrowed ramp.

**`role_defaults_219 --selftest`, +7 clauses** — the five above at the mint site, plus two the
#220 lane had no reason to need: `gen_bento_matrix_217.capbg_for` is **imported and driven** to
prove the retired word is still reachable (a failure to import is a NAMED failure, never a silent
skip), and the now-empty `NO_SUPERSESSION` fence is **crossed with a synthetic entry** through the
real code path — see finding 5.

## WHAT WAS DRIVEN

**`role_defaults_219.py --selftest` → OK, 12 exports parsed** (+7 clauses; two old mono clauses
re-pointed, one asked of the receipt instead of the live table).
**`gen_bento_matrix_217.py --selftest` → OK, 104 bites** (unchanged count; `R6e` widened).
**`gen_bento_matrix_217.py --rails` → manifest written** (the ordered serial, manifest FIRST).
**`gen_foundations_217.py` → 8 page(s), 2 written** (the pages, SECOND).
**`gen_foundations_217.py --selftest` → OK, 46 bites** (was 44; **+2**: `6k`, `6l`).
**`gen_foundations_217.py --check` → OK, 8 pages in sync.**
**`gen_library_214.py --check` → OK, 143 components, index + index.json + stub in sync** (index LAST).

**`verify_foundations_217.py`** — `--page photography` **8/8**, `--page bento-rails` **8/8**,
`--page logos` **8/8**. No dangling property; the theme reached the paint in all four.
**`verify_photography_218.py`** — all four themes, **8 states**, `✅ OK`. The strongest evidence in
the lane: the probe that reads the 251-photograph wall's real paint.
**`verify_bento_matrix_217.py`** — `mono,legacy` **4 states**, `console,supercharge` **4 states**,
all green. The line that matters, read off the live document:

```
⬛ s219-D3 chords · dark caption ground · console OFFERS · mono/legacy/supercharge REFUSE with the
open question printed · capsule/light grey · --text-secondary on rgb(240, 240, 240) = 15.27:1 ·
capsule/light white 17.4:1 · capsule/light darkgrey 17.4:1 · capsule/dark grey 16.48:1 ·
capsule/dark white 16.48:1 · capsule/dark darkgrey 13.01:1
⬛ s219-D3(3) counts · base themes 984 · console 1200 (+216, the chord's own dark caption ground)
```

**All six chord members still offered and still contrast-gated, and mono still REFUSING the dark
ground with the open question printed on the page** — the option space and the open question both
SEEN rather than asserted.

**Advisory gates, still advisory, re-driven over the regenerated files:**
`knowledge/_render/_gate_fallback_drift_221.py` → **`✅ every var() fallback literal in the glob is
one of canon's own answers`, 0 drifted** (11 UNCHECKED declared, unchanged).
`knowledge/_validate_property_resolves.py` (C2) → **147 file(s), 0 failure(s).**

### Mutation arms — **before/after MEASURED, not reasoned**

Two NON-REPO drivers (`/var/tmp/ds222/arm.py`, `varm.py`, banked as `.txt` beside this report)
generate and run each side twice from the *same* code with **one variable changed** — the `s222-D1`
mono supersession removed and the table re-derived, which is exactly the pre-switch state. No git,
no stash, no tree mutation; artefact md5s verified unchanged after every arm.

| Arm | BEFORE | AFTER | Result |
|---|---|---|---|
| `role_defaults_219 --selftest` | **3 named ❌** | **OK** | fires and clears; each ❌ names `s222-D1` |
| `gen_foundations_217 --selftest` | **5 named ❌** (`6f`,`6j`,`6k`,`6l`,`25`) | **OK, 46** | fires and clears |
| `gen_bento_matrix_217 --selftest` | **2 named ❌** (`R6e`,`R6d`) | **OK, 104** | fires and clears; `R6d` is correct — the on-disk manifest IS the AFTER generation |
| `--break-default` + `verify_photography --default-mutation --themes mono` | **2** (light only) | **2** (light **and dark**) | red by name; **same count, different clauses — the arm reaches a mode it could not** |
| `--break-settings` + `verify_photography --settings-mutation --themes mono,console` | **19** | **16** | red by name; **−3, and the −3 is a real loss** — finding 2 |

⛔ **BOTH SIDES WERE PATCHED FOR THE BROWSER ARMS.** A first pass patched only the generator and
compared a pre-switch page against the post-switch dial — a number that measures the cross-wiring,
not the arm. `varm.py` exists so the verifier sees the same table the generator did.

## Findings

1. **⛔ THE `#220` FIX AT CAUSE PAID OFF WITH NOBODY REMEMBERING TO COME BACK, AND IT IS QUOTED.**
   `verify_photography_218.py:419` reads `RESOLVED_SUPERSEDED`, which is **derived from the
   supersession layer**. Mono's `resolved` readback (`rgb(240, 240, 240)`, the pixel Dave's #219
   export measured) would otherwise have red-lit the enactment — a gate failing the ruling it
   protects, exactly the `#220` finding-2 shape. Instead the verifier declared it by name, first
   run, with no edit to the verifier at all:
   `⚠ mono: the export resolved captionBackground rgb(240, 240, 240), RETIRED — s222-D1 moved capBg
   from 'grey' to 'transparent'; … the page resolves rgba(0, 0, 0, 0)`.
   ⬛ **This is the first independent test of a gate-don't-patch fix from a later ruling, and it
   passed.** The `#220` lane touched a third file to build it; this lane touched none.

2. **⛔ THE SWITCH MADE ONE MUTATION ARM STRICTLY BLUNTER — 19 → 16 — AND ONLY A MEASURED BEFORE
   COULD SHOW IT.** `--break-settings` **strips the whole settings block**. A stripped page paints
   no caption ground, i.e. **transparent** — which is now mono's *ruled* answer. So the three named
   assertions `SETTINGS CAPTION GROUND — mono/light`, `mono/dark` and `SETTINGS CAPTION — mono/light`
   **can no longer fire**: the mutant coincidentally renders the ruled state.
   ⚠ **The coverage moved, it did not vanish.** The sharper arm, `--break-default`, went from
   firing in **light only** (grey vs white differ in light; in mono *dark*, `--surface-subtle` and
   `--surface-raised` both resolve `rgb(31,31,31)`, so the mutation was invisible) to firing in
   **both modes** (transparent vs white differ in both). Net: `--break-settings` lost 3, and the
   dial-level arm gained a mode. ⛔ **This is a class, not a case:** *any* dial whose ruled default
   equals the no-CSS fallback is invisible to a block-strip arm. Priced as a ruling-shaped question.
   Measured, both ways, both sides patched — see `mutation-arms-browser.txt`.

3. **⛔ A DECISION-SURFACE GENERATOR CANNOT REBUILD ITS OWN PAGE ONCE THE CANDIDATE SHIPS, AND THAT
   IS CORRECT.** `knowledge/_render/gen_mono_gallery_221.py` draws TODAY beside CANDIDATE and
   guards `TODAY == RECEIPT`. With mono switched it now **REFUSES by name** — driven, not reasoned:
   the generator was re-run and exited 1, and `cmp` proves
   `reviews/MONO-GALLERY-DEFAULT-2026-08-27-v1.html` **byte-identical** afterwards. The page is the
   surface Dave ruled off and must stay frozen ([[feedback-version-dont-overwrite]]). ⚠ Its refusal
   message still cited `s220-D2 (3)`'s *"expressly open"* — a **stale premise inside a live
   refusal**, which is the class that misleads next ([[premise-ages-faster-than-rule]]). Re-pointed
   at `s222-D1` with the frozen-evidence reason written into the message. **Behaviour unchanged: it
   refused before and it refuses now.** This is a fourth file, outside the brief's named two, and
   is named rather than left.

4. **⚠ THREE BITES HAD TO MOVE *WITH* THE RULING, AND WIDENING THEM WOULD HAVE BLINDED THEM.**
   `6f` asserted the shipped caption-ground set was `["grey","transparent"]`; mono was the last
   grey, so it is now `["transparent"]`. Bite `25` asserted `var(--surface-subtle,#F0F0F0)` was
   **in the live block** and that the grey-ground themes were `["mono"]`; both are now false *by
   ruling*. ⛔ **`25` was re-pointed, not deleted:** the `s219-D2 (1)` identification (`grey` **is**
   `--surface-subtle`, `#F0F0F0` in mono) is still true **of the option**, so the clause is now
   asked of a **grey-dialled build** and paired with a clause that the literal appears **nowhere in
   the shipped block**. Dropping it would have stopped watching a ground the edit pass can still
   choose. `6h`'s three mono clauses were **moved to `6k`**, re-pointed at the new ruled answer —
   left tolerant they would have gone green on a regression.

5. **⛔ A FENCE WHOSE TABLE IS NOW EMPTY IS AN UNFIRED FENCE, SO IT IS CROSSED DELIBERATELY.**
   `s222-D1` closed the only entry `NO_SUPERSESSION` carried. The refusal path in
   `_apply_supersessions` therefore had **no input that reaches it** — the
   [[instrument-without-a-consumer]] shape, arriving by ruling rather than by neglect. The selftest
   now pushes a **synthetic entry** through the real code path and requires the refusal, restoring
   the table in a `finally`. And `NO_SUPERSESSION_CLOSED` keeps the record: an open clause that
   simply vanishes leaves no trace it was ever open, and the next reader cannot tell a ruling from
   an oversight ([[header-wins-over-audit]]).

6. **⬛ MONO IS THE FIRST SWITCH WHERE THE RULED DIAL AND THE THEME'S OWN TOKEN DO DIFFERENT HALVES
   OF THE JOB, AND THE MACHINERY REFUSES TO RECORD THE HALF IT DID NOT DO.** Dave's sentence names
   *square image + transparent caption*, two visible changes; the layer carries **one**. The other
   is `--border-radius-container: 0`, already true in mono, reached through the *same* `corners`
   rule that gives console 20px. The `was == now` gate would have refused a `rounding` entry as "a
   record of a decision that did not happen" — so the module physically cannot store the tidier,
   wronger version. **The premise was re-driven at HEAD before this was decided** (brief's own
   instruction) and is now bite `6k`'s eighth clause, not a comment.

7. **⚠ `s220-D2 (4)`'s DISCHARGE IS STILL NOT WRITTEN, ONE SESSION ON.**
   `notes/_receipts/2026-08-25-219-role-defaults-exports.md:439` still reads `## PARKED CORRECTION
   — 2026-08-26, Dave's words, NOT ENACTED`, and `s220-D2 (4)` supersedes it. Checked at HEAD, not
   carried: the receipt is outside this lane's regions and untouched. The `#220` lane priced this
   at ~1K tk as an **ADDITION** to a ratified record; it has now been open across two enactments of
   the same file's supersession layer, which is how a residue becomes invisible
   ([[forgotten-document-class]]).

## RULING-SHAPED QUESTIONS

*(All four are Dave's or the conductor's. Nothing below is decided.)*

1. **⬛ MONO'S DARK CAPTION CHORD — expressly still open, and the stakes have changed shape.**
   `s219-D3` / X6 scope the dark caption ground to console gallery; mono/legacy/supercharge refuse
   it by name, and `s222-D1` says in its own words that this is *"a separate call and left open"*.
   ⚠ **What changed today:** with all four gallery defaults now `transparent`, the dark ground is
   no longer a difference between two shipped walls — it is purely an **edit-pass reach** question.
   **(a)** leave X6 console-only; **(b)** widen the chord's scope to mono (`+216` legal states for
   mono, mirroring console's 864); **(c)** widen to all four. ⚠ Under (b)/(c) the `s220-D1` caption
   mint is mode-scoped, so the photography page's **mode-flat settings block would refuse to
   compile** a shipped default on it (bite `6f`/`6g`) — reach and default are separable, and only
   the reach is being asked. Price to enact (b): one `scope` row + the counts bites re-pointed,
   ~4K tk. **Nothing here recommends a change.**

2. **Does `W-217` close?** The store row `W-217` (`notes/_subreports/2026-08-27-220-default-switch.md`,
   owner **dave**) reads `closes_when: "Dave has seen reviews/DEFAULT-SWITCH-2026-08-27-v1.html and
   ruled mono's gallery default (switch or keep grey), or parked it"`. `s222-D1` **is** that ruling.
   ⛔ **Not closed here** — the brief fences a sub out of Dave's rows, and a sub closing a row on
   its own reading is [[sub-ruled-daves-open-item-110]]. **(a)** conductor closes it citing
   `s222-D1`; **(b)** Dave confirms first. Price: ~0 tk either way.

3. **Should there be a mutation arm that can see a `transparent` ruled ground?** Finding 2: a
   block-strip arm is structurally blind to any dial whose ruled default equals the no-CSS
   fallback, and **all four gallery caption grounds are now `transparent`** — so the whole
   `SETTINGS CAPTION` family is now carried by `--break-default` alone. **(a)** leave it: the
   sharper arm covers it, in both modes, measured today; **(b)** add a `--break-caption` arm that
   mutates the ground to a **legal non-default option** (grey) instead of stripping, so a stripped
   *and* a mis-dialled page are both caught (~3K tk); **(c)** widen `--break-default` to sweep all
   four themes rather than mono (~2K tk). ⚠ Under (a), if `--break-default`'s mono arm is ever
   re-aimed, the family loses its last consumer silently. Recommend **(b)** — it is the arm that
   tests the clause rather than the block ([[mutation-tests-the-clause-not-the-feature]]) — **but
   it adds an arm to the standing serial, which is a cost Dave carries.**

4. **Does the `s220-D2 (4)` PARKED CORRECTION discharge get written into the receipt?** Finding 7,
   unchanged from the `#220` lane's question 2 and now one session older. **(a)** append a
   discharge note under the parked section citing `s220-D2 (4)`; **(b)** leave it and let the
   ruling be the only home. ⚠ Under (b) a reader of the receipt sees a parked correction that
   reads as live, on the *one document* both default switches point at as evidence. ~1K tk, and it
   is an ADDITION to a ratified record, never a trim.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** this sub's own token spend — a sub cannot read `message.usage`. Price to prove: the
  conductor's panel, ~0 tk.
- **UNPROVEN:** the **BEFORE raster** for mono's two rows in the before/after table. The dial words
  and their token resolutions were re-derived this lane (the patched arms print
  `dial says grey (--surface-subtle)` and the mutant resolves `rgb(240,240,240)`), but the
  15.27:1 / 16.48:1 figures are the `#220` receipt's measurements carried forward, not this lane's
  raster. Price to measure: one browser run over a pre-switch page, ~2K tk.
- **UNPROVEN:** the regenerated pages in a **real browser on Dave's Mac**. Verified in the sandbox
  headless shell only. Price: the runbook's Claude-in-Chrome fallback, ~2K tk.
- **UNPROVEN — the advisory-gate sweep is NAMED, NOT EXHAUSTIVE.** Two gates were driven
  (`_gate_fallback_drift_221.py`, `_validate_property_resolves.py`) because they read the
  regenerated files. `knowledge/_build_all.py` was **not** run (brief fence) and neither generator
  appears in it or in `.github/workflows/gates.yml` — probed by `grep -rn "gen_foundations_217\|
  gen_bento_matrix_217" knowledge/_build_all.py .github/workflows/*.yml` → **no match**, so no CI
  arm covers them today. Whether a gate outside that grep touches these artefacts is UNPROVEN.
  Price to sweep the fleet: ~5K tk.
- **COULD-NOT-RUN — nothing.** Every step in the brief's DONE list ran.
- **CLAIMED — nothing.** Every mechanical statement above quotes a probe, a file and line, or a
  measured browser value.

## Fences honoured

**NO git** — nothing staged, committed, stashed or checked out; only read-only `git status` /
`git diff` / `git log`. **`knowledge/_rulings.json` READ ONLY** — it is dirty in `git status`, and
it was **already dirty before this lane opened** (recorded in this lane's first `git status`,
before any edit: `M knowledge/_rulings.json`, alongside `notes/_REHEARSAL-LOG.jsonl` and
`notes/_dream/_GRADE-DECISIONS.jsonl`). That is the conductor's inscription, not opened here.
**No `_state.json` row of Dave's touched** — `W-217` named in question 2, NOT closed. **No advisory
promoted**, no threshold, band or constant moved. **The dark-chord question untouched** — not
answered, not priced as a change, its status quo asserted by bite `6l` and printed by the live
verifier. **⛔ THE #219 RECEIPT IS UNTOUCHED** — byte-identical, asserted by the module's own
`was`-gate on every import. **No option removed from any grammar, any theme** — asserted by `6l`,
`6j`, `R6e`, the rails page's one-line diff, and the live chord line. **`X1`/`X2` still PROPOSED**
(`R6e`). **No `_build_all.py`, no `_capture_gate.py --selftest`.** **No token minted, no colour
value changed.** **Two-red law + mono error ink camp untouched** — `git diff -U0 | grep -iE
"^\+.*(#DA1A00|#F6604C|#EE3524|#D7153A)"` → **0**. `ls -a knowledge/assets/fonts/_desktop/TTF |
grep -c '^\.uuid'` → **0**.

**One store row MINTED, for this report only (forgotten-document class).** `W-242`, written by
`knowledge/_state.py`'s own `add()` — the store's writer, never by hand — `owner: claude`,
`opened: 222`, `closes_when: "the conductor has reconciled and committed this lane's 7 paths and
replayed the report's REPLAY-THESE sections; or Dave has ruled on its RULING-SHAPED QUESTIONS 1
and 3"`. `_state.check()` green, `git diff --stat knowledge/_state.json` → **`+12/−0`, purely
additive**: no existing row read, reworded, re-scoped or closed.

**My paths (8):**
`knowledge/_render/role_defaults_219.py` (`+146/−20`) ·
`knowledge/_render/gen_foundations_217.py` (`+129/−36`) ·
`knowledge/_render/gen_bento_matrix_217.py` (`+18/−9`) ·
`knowledge/_render/gen_mono_gallery_221.py` (`+9/−3`) ·
`knowledge/_render/_bento_edit_rails.json` (`+12/−1`, generated) ·
`showroom/_foundations/photography.html` (`+13/−7`, generated) ·
`showroom/_foundations/bento-rails.html` (`+1/−1`, generated) ·
`knowledge/_state.json` (`+12/−0`, the `W-242` row above, via the store's own writer) ·
this report + `notes/_subreports/assets/2026-08-28-222-mono-default-switch/` (6 files).
⚠ **The per-file `+/−` are EXACT** (`git diff --numstat`): no parallel lane shares these paths this
window — the only other dirty paths are the conductor's three, listed above.

## Evidence

`notes/_subreports/assets/2026-08-28-222-mono-default-switch/`

- `measured-photography-mono-console.txt` / `measured-photography-legacy-supercharge.txt` — the
  full `verify_photography_218` runs over the regenerated wall, all four themes, both modes: gutter,
  tile count, borders, **tile radius**, **image radius**, page/bento/caption grounds, ink, contrast
  and caption space, plus the RETIRED-readback declarations. **This is the file the VERDICT's dial
  table is read out of.**
- `mutation-arms-selftests.txt` — arms A/B/C, before and after, with every named ❌ quoted.
- `mutation-arms-browser.txt` — the two browser arms, before and after, **both sides patched**, with
  the 2-vs-2 (light-only → both modes) and 19-vs-16 results and the exact assertions that moved.
- `arm.py.txt` / `varm.py.txt` — the drivers. **Canonical home is here**; they were run from
  `/var/tmp/ds222/` **(NON-REPO: sandbox-local, `s191-D2`)** and copied back verbatim.

REPLAY-THESE: `notes/_subreports/2026-08-28-222-mono-default-switch.md` §THE MINT SITE, QUOTED (~500 tk) · §Findings 2, 3 and 5 (~600 tk) · §RULING-SHAPED QUESTIONS 1, 2 and 3 (~450 tk) · §UNPROVEN (~250 tk)

---

## CONDUCTOR ADDENDUM — #222, same day (addition, nothing above trimmed)

⛔ **FINDING 7 AND QUESTION 4 REST ON A FALSE PREMISE AND ARE WITHDRAWN.** The `s220-D2 (4)`
discharge IS written in the receipt: `notes/_receipts/2026-08-25-219-role-defaults-exports.md`
carries `**DISCHARGED 2026-08-27 (#220), BY ADDITION — s220-D2.**` directly under the parked
section (committed at `707e5aa`, verified by `git log` on the file). The finding read the
section HEADING (`NOT ENACTED`) without reading to the discharge paragraph below it — the
heading is frozen history and correctly keeps its original words; the discharge is the addition
beneath, exactly the addition-only form Q4 option (a) asks for. Nothing is owed. The other six
findings and Q1–Q3 stand.
