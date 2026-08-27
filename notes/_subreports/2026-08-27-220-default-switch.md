# `#220`-default-switch — the console gallery default becomes chord two, and no option is removed

session: `#220` · 2026-08-27
window: bento lane — enacting `s220-D2`, Dave's *"if you are asking for a default lets go with
rounded corner image with transparent capsule"*
sub index: `default-switch`
tokens: `UNMEASURED` — a sub cannot read its own `message.usage`; the conductor's panel is the only
place this spend is real.

## VERDICT

**DONE.** The console gallery ships **`rounding: corners` + `capBg: transparent`**, **identical in
light and dark**, enacted **AT CAUSE** as a **supersession LAYER** over Dave's #219 tuner export in
`knowledge/_render/role_defaults_219.py` and derived everywhere else. **The receipt is untouched.**
**No option was removed**, asserted three ways. **Mono is untouched**, asserted in both directions.

Measured **in the browser**, on the regenerated `showroom/_foundations/photography.html`:

```
console/light  tileR [0] · imgR [20] · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(26, 26, 26)']   17.4:1
console/dark   tileR [0] · imgR [20] · cap ['rgba(0, 0, 0, 0)'] ink ['rgb(255, 255, 255)'] 17.4:1
mono/light     tileR [0] · imgR [0]  · cap ['rgb(240, 240, 240)']  15.27:1   ← UNCHANGED
mono/dark      tileR [0] · imgR [0]  · cap ['rgb(31, 31, 31)']     16.48:1   ← UNCHANGED
```

The two console rows are the **same dials in both modes** — that is `s220-D2 (2)`'s "default for the
two modes", read off the live document rather than argued from the table.

COUNTS: files changed by this lane `6` + `1` new page + `13` new asset files · matrix bites
`103 → 104` · foundations bites `41 → 44` · role-defaults selftest clauses `+7` · browser verifier
states driven `38` · mutation arms `5`, **before/after MEASURED** · findings `7` ·
ruling-shaped `4` · UNPROVEN `3`

## THE MINT SITE, QUOTED

⛔ **THE DEFAULT MOVED WITHOUT THE RECEIPT MOVING, AND THAT IS THE WHOLE SHAPE OF THE ENACTMENT.**
`role_defaults_219.py` **parses** Dave's twelve verbatim exports out of
`notes/_receipts/2026-08-25-219-role-defaults-exports.md` — that receipt is the module's only source
of defaults, and s219-D1(3) makes it the RECEIPT of what he approved. Editing a row of it to match a
later ruling would have destroyed the evidence and left the supersession invisible. So the parse is
kept whole as `RECEIPT_DEFAULTS` and a **layer** is applied over it:

`knowledge/_render/role_defaults_219.py:221` — the whole decision, one table:

```python
SUPERSESSIONS = [
    {
        "type": "gallery", "theme": "console", "dial": "rounding",
        "was": "capsule", "now": "corners",
        "ruled_by": "s220-D2 (2)",
        "supersedes": "s219-D2 (3) · the s219-D1 (3) console gallery export",
        "modes": "both — one default, identical in light and dark",
        "dave": "if you are asking for a default lets go with rounded corner image with "
                "transparent capsule",
    },
    {
        "type": "gallery", "theme": "console", "dial": "capBg",
        "was": "grey", "now": "transparent",
        ...
    },
]

# (type, theme) pairs a ruling has EXPRESSLY left alone, so an absence can be read as a decision.
NO_SUPERSESSION = {
    ("gallery", "mono"): "s220-D2 (3) — mono's gallery default (capBg: grey) is EXPRESSLY OPEN: "
                         "asked in chat, not ruled. It keeps grey until Dave's word.",
}
```

⛔ **`was` IS A GATE, NOT A COMMENT.** `_apply_supersessions()` refuses **by name** if the receipt no
longer says what the supersession claims to supersede, if a supersession names an intersection in
`NO_SUPERSESSION`, or if `was == now` (an override that changes nothing is a record of a decision
that did not happen). A "tidied" receipt is a LOUD refusal, not a silently absorbed change.

**Everything else derives from it**, and nothing is typed twice:

| Consumer | Where | What it now answers |
|---|---|---|
| `DEFAULTS` | `role_defaults_219.py:302` | the SHIPPED table — receipt + ruled overrides |
| `RECEIPT_DEFAULTS` | `:188` | the parse, frozen. Both are in scope so the two can be compared |
| `RESOLVED_SUPERSEDED` | `:302` | which `resolved` **readbacks** a supersession made stale, and why |
| `default_for_mode(t,th,m)` | `:331` | `s220-D2 (2)` as machinery: the SAME block for light and dark, a NAMED refusal for a third mode |
| `gen_foundations_217.ROLE_DEFAULTS` | `:316` (receipt at `:326`, stale map at `:333`) | the compiled per-theme settings block |
| `gen_bento_matrix_217._defaults_block` | `:1224` | the manifest's `values` **plus** `supersessions` + `receipt_values` |
| `verify_foundations_217.ROUNDING` | `:81` | derived — the browser probe followed with no edit |

### The generated CSS, verbatim from `showroom/_foundations/photography.html`

```css
/* ---- console · spacing 40 (40px) · keylines off · bento · square edge · rounding corners ·
   page transparent · bento transparent · caption transparent ---- */
[data-apollo-theme="console"] … .c-bento__tile{border-radius:0;}
[data-apollo-theme="console"] … .c-bento__tile .px-open{border-radius:0; overflow:visible;}
[data-apollo-theme="console"] … .c-bento__tile .px-img{
  border-radius:var(--border-radius-container,0px); overflow:hidden;}
[data-apollo-theme="console"] … .c-bento__tile .px-cap{
  background:transparent; color:var(--text-secondary,#545454);}
```

⛔ **ONE BLOCK, NO MODE AXIS — AND THAT IS THE RULING, NOT A SHORTCUT.** The `#220` mode-flat fence
(bite `6f`) still bites and is still un-tripped: `transparent` carries no `CAPTION_GROUND_MINT`, so
one declaration per theme serves both modes. `s220-D2 (2)`'s "default for the two modes" needed **no
new machinery at all** — what it needed was for the mode-flatness to become **asserted** rather than
incidental, which is what `default_for_mode()` and bite `6h` do.

## BEFORE / AFTER — THE WHOLE TABLE

### The twelve shipped defaults, gallery row (the other eight are byte-unchanged)

| theme | rounding BEFORE | rounding AFTER | capBg BEFORE | capBg AFTER | moved? |
|---|---|---|---|---|---|
| mono | corners | corners | **grey** | **grey** | **no — s220-D2 (3) EXPRESSLY OPEN** |
| legacy | corners | corners | transparent | transparent | no |
| **console** | **capsule** | **corners** | **grey** | **transparent** | **YES — s220-D2 (2)** |
| supercharge | corners | corners | transparent | transparent | no |

Console now carries the default legacy and supercharge already had: **three of four agree**.

### What the browser paints, console gallery

| state | tile radius | image radius | caption ground | ink | ratio |
|---|---|---|---|---|---|
| light BEFORE | 20px | 0px | `rgb(240,240,240)` `#F0F0F0` | `rgb(26,26,26)` | 15.27:1 |
| **light AFTER** | **0px** | **20px** | **transparent → `rgb(255,255,255)`** | `rgb(26,26,26)` | **17.40:1** |
| dark BEFORE | 20px | 0px | `rgb(31,31,31)` `#1F1F1F` | `rgb(255,255,255)` | 16.48:1 |
| **dark AFTER** | **0px** | **20px** | **transparent → `rgb(26,26,26)`** | `rgb(255,255,255)` | **17.40:1** |

Both AFTER states clear the ruled 4.5:1 floor by **12.9**. The AFTER pair's **dials are identical**;
only canon's own token resolution differs by mode.

### Artefacts

| Artefact | Changed by this lane? | How that is known |
|---|---|---|
| `showroom/_foundations/photography.html` | **YES** | the settings block + the receipt table |
| `showroom/_foundations/bento-rails.html` | **YES** | reads the regenerated manifest (`defaults.values`, the page-rail specimen strip) |
| `knowledge/_render/_bento_edit_rails.json` | **YES** | `defaults.values` + new `supersessions` / `receipt_values` |
| `bento.html`, `grids-{12col,dashboard,display,gallery}.html`, `logos.html` | **NO** | the writer reported "8 page(s) → 2 written" then "1 written"; `bento.html` and `grids-gallery.html` md5 verified byte-identical across the lane |
| `knowledge/_render/index` / library | **NO** | `gen_library_214.py --check` **OK, 143 components in sync** — driven, not assumed |

## THE THREE GUARANTEES, EACH ASSERTED SEPARATELY

⛔ A single "console is corners now" bite would go green on a build that silently removed the capsule
option or dragged mono along with it — the exact two things `s220-D2` (1) and (3) forbid
([[green-tests-cannot-see-scope]]). Three bites, three different claims:

**`6h` — THE SWITCH, AND THE RECEIPT IT DID NOT REWRITE.** Eight clauses: the live console pair is
`("corners","transparent")`; the **receipt's** console pair is still `("capsule","grey")`; mono's
live block **equals** its receipt block; no supersession names mono; mono's ground is still `grey`;
`default_for_mode(…,'light') == default_for_mode(…,'dark')`; and both compiled CSS declarations are
byte-present in the settings block.

**`6i` — NO OPTION WAS REMOVED.** The four treatments the ruling names are each driven through
`caption_legal` / `capsule_legal` / `capbg_for` / `chord_refusals` — **all legal, all reachable,
zero refusals**; `ROUNDINGS` still carries both members; the caption ramp is unnarrowed in all four
themes; `X1`/`X2` are still `proposed`; and the **capsule branch is compiled** on a settings table
this page no longer ships, so the branch nothing reaches is still driven
([[instrument-without-a-consumer]]).

**`6j` — THE SIZE OF THE OPTION SPACE.** `counts_by_theme()` enumerates every legal state out of the
matrix's own option lists and never consults a default, so these numbers move **only** if an option
was added or taken away: gallery **648 / 648 / 864 / 648**, display **48**, dashboard **288**,
unchanged. Console's extra 216 is the capsule chord's `darkgrey` (X6).

**`R6e` (matrix) — THE MANIFEST CARRIES BOTH RECORDS.** `_bento_edit_rails.json` is what the library
page reads (s219-D3(6)). Left alone it would print `corners` with nothing saying a ruling moved it
there, and Dave's export would look as though it had always said so. It now carries
`defaults.supersessions` (dial, `was`, `now`, ruling, what it supersedes, Dave's sentence) **and**
`defaults.receipt_values` (the frozen parse), and the bite asserts the two **disagree in exactly the
ruled way**.

## WHAT WAS DRIVEN

**`role_defaults_219.py --selftest` → OK, 12 exports parsed** (+7 new clauses, listed above).
**`gen_bento_matrix_217.py --selftest` → OK, 104 bites** (was 103; **+1**: `R6e`).
**`gen_foundations_217.py --selftest` → OK, 44 bites** (was 41; **+3**: `6h`, `6i`, `6j`).
**`gen_foundations_217.py --check` → OK, 8 pages in sync.**
**`gen_library_214.py --check` → OK, 143 components, index + index.json + stub in sync.**

**`verify_foundations_217.py`** — `--page photography` **8/8**, `--page bento-rails` **8/8**,
`--page logos` **8/8**. No dangling property; the theme reached the paint in all four.
**`verify_bento_matrix_217.py`** — `console` **2 states**, `mono,legacy` **4**, `supercharge` **2**
(sliced to stay inside the sandbox wall). All green. The line that matters, read off the live
document:

```
⬛ s219-D3(3) counts · base themes 984 · console 1200 (+216, the chord's own dark caption ground)
legality · P2 refuses same-on-same with a reason and the click is inert · P3 refuses the edgeless capsule
⬛ s219-D3 chords · capsule/light grey 15.27:1 · capsule/light white 17.4:1 · capsule/light darkgrey
17.4:1 · capsule/dark grey 16.48:1 · capsule/dark white 16.48:1 · capsule/dark darkgrey 13.01:1
```

**All six capsule chord members still offered, still contrast-gated, in the browser** — the option
space seen rather than asserted.

**`verify_photography_218.py`** — `--themes console` **2 states**, `--themes mono,legacy` **4
states**, both `✅ OK`. This is the strongest evidence in the lane: it is the probe that reads the
251-photograph wall's real paint.

### Mutation arms — **before/after MEASURED, not reasoned**

A NON-REPO driver (`/var/tmp/ds220/arm.py`, `varm.py`) generates each mutant, and runs each
verifier, twice from the *same* code with **one variable changed** — `SUPERSESSIONS` emptied, which
is exactly the pre-switch state. No git, no stash, no tree mutation.

| Arm | Before | After | Result |
|---|---|---|---|
| `gen_foundations --break-default` + `verify_photography --default-mutation --themes mono` | **2** | **2** | red by name (`SETTINGS CAPTION`, `SETTINGS CAPTION GROUND`) |
| `gen_foundations --break-settings` + `verify_photography --settings-mutation --themes mono,console` | **18** | **19** | red by name — **+1, and the +1 is the point** (below) |
| `gen_bento_matrix --break-legality` + `verify_bento_matrix --mutation --themes console` | **11** | **11** | red by name; mutant **byte-identical** either side (md5 `ab8b17be…`) |
| `gen_bento_matrix --break-keylines` | — | — | mutant **byte-identical** either side (md5 `583a6f43…`); the count is the theme-lift lane's **306** on a proven-identical input — see UNPROVEN |
| in-generator `6i` — the capsule branch compiled, `capsule+darkgrey` refused by name | — | armed | both self-assert |

⬛ **THE `18 → 19` IS A REAL RESULT AND IT IS THE RIGHT DIRECTION.** With console ruled `capsule`,
the settings-stripped mutant still happened to render capsule geometry, so the `SETTINGS ROUNDING`
family **never fired in console** — an assertion family the arm could not reach. With console ruled
`corners`, the stripped mutant's leftover 20px tile radius is caught. **The default switch made an
existing mutation arm strictly sharper**, and it is measured, not claimed.

## THE PROOF PAGE

`reviews/DEFAULT-SWITCH-2026-08-27-v1.html` (42,861 bytes, new, `-v1`). Seven sections, **10 live
specimens**: *Two sentences, two different decisions* → **Console in light, before beside after** →
**Console in dark, before beside after** → **All four treatments, still there to pick from** (the
best pointing surface) → *Mono did not move* → *Where it is written* → *Not decided here* → footer.

⛔ **NEITHER SIDE OF THE PAIR IS TYPED, AND FOR A *DEFAULT* SWITCH THAT IS THE WHOLE METHOD.**

- **AFTER** reads its dials from `gen_foundations_217.GALLERY_SETTINGS['console']` — the **shipped
  default**. Move the default and the card moves; nothing on the page has to be edited.
- **BEFORE** reads its dials from `RECEIPT_ROLE_DEFAULTS['gallery']['console']` — **Dave's own #219
  export**, parsed from its receipt. It is not a memory of what the page used to look like; it is
  the receipt, still on disk, rendered.
- The build **REFUSES** if the two agree, or if they differ on anything but the two ruled dials.
- The **four option specimens** are each put through `caption_legal` / `capsule_legal` /
  `capbg_for` / `chord_refusals` before being drawn, and the build refuses if any has stopped being
  an option. **The page cannot claim an option survives while the code refuses it.**
- The compiled console rules are lifted out of `showroom/_foundations/photography.html` **by
  selector and asserted byte-present**, so a proof page over a stale artefact **raises** instead of
  going green ([[ritual-output-is-not-evidence]]). The `s220-D1` mint block is likewise asserted
  present in `bento-rails.html`.
- Specimen markup and specimen CSS are copied between explicit `COPIED-FROM-ARTEFACT` markers; the
  `.cdl-`/`.br-`/`.bm-` names come **with** the copy, because a copy that is renamed is a
  transcription.

**Render-verified, driven not asserted**, at **1180 and 480**:

```
before-light  capsule  grey        rgb(240,240,240)  PIXELS rgb(240,240,240)  15.27  tileR 20px imgR 0px
after-light   corners  transparent rgb(255,255,255)  PIXELS rgb(255,255,255)  17.40  tileR 0px  imgR 20px
before-dark   capsule  grey        rgb(31,31,31)     PIXELS rgb(31,31,31)     16.48  tileR 20px imgR 0px
after-dark    corners  transparent rgb(26,26,26)     PIXELS rgb(26,26,26)     17.40  tileR 0px  imgR 20px
mono-light    corners  grey        rgb(240,240,240)  PIXELS rgb(240,240,240)  15.27  tileR 0px  imgR 0px
mono-dark     corners  grey        rgb(31,31,31)     PIXELS rgb(31,31,31)     16.48  tileR 0px  imgR 0px
```

**13 named claims, 0 failed** — including *"ONE DEFAULT, BOTH MODES — the two AFTER cards carry
identical dials"* (`rounding=corners · capbg=transparent · spacing=40 · edge=square · keylines=off ·
bentobg=transparent`) and *"MONO still ships a GREY caption ground, both modes"*. Plus **0**
pixel-vs-computed disagreements · **0** printed-vs-measured disagreements (the page's own numbers
parsed back out of the DOM and checked against the raster) · **0** hue-rule violations (split assert
carried from the theme-lift probe) · **0** broken images · **0** horizontal overflow · **0** boxes
moved between measure and capture (the `#217` registration pothole) · every specimen in canon's
**single-column** band at both widths (ds-054) · font probe **green against both controls** (target
346.88 = both aliases; DejaVu 375.39; nonexistent 301.07).

⚠ **One defect seen and fixed on the page**, and it is the `#220` ladder's own lesson one level
down: the AFTER read-out's first value wraps to three lines and the BEFORE's to two, so **every row
below it sat at a different height** and the two read-outs could not be compared line by line —
which is the entire job of a read-out under a pair. A `min-height` floor on the row, with the reason
written beside it.

## Findings

1. **⛔ THE RECEIPT IS THE MODULE'S ONLY SOURCE, SO THE SUPERSESSION HAD TO BE A LAYER — NOT AN
   EDIT.** `role_defaults_219.py` exists precisely because a default re-typed into Python is a
   second copy of a decision. That design is what made the ruling's own instruction ("supersede in
   the generator, never rewrite the receipt") **mechanically possible**: the parse is kept whole,
   the layer sits on top, and both are exported so any consumer can compare them. Had the module
   held a typed table, "supersede without rewriting" would have had no place to live.

2. **⛔ A `resolved` READBACK GOES STALE WITH THE DIAL, AND IT WOULD HAVE RED-LIT THE ENACTMENT.**
   `verify_photography_218.py:432` (the guard at `:419`) cross-checks the page's painted caption ground against Dave's
   #219 export readback, in light, per theme. Console's export resolved `rgb(240,240,240)`; the
   enacted page paints `rgba(0,0,0,0)`. **That check would have gone RED on the correct answer** —
   a gate failing the ruling it is meant to protect. Fixed at cause: `RESOLVED_SUPERSEDED` is
   derived **from the supersession layer**, so the verifier declares the divergence **by name**
   (the same pattern the transparent-page divergence already used) instead of skipping it, and the
   **next** supersession is covered with nobody remembering to come back
   ([[gate-dont-patch]]). Driven: the line prints in the browser —
   `⚠ console: the export resolved captionBackground rgb(240, 240, 240), RETIRED — s220-D2 (2)
   moved capBg from 'grey' to 'transparent' …; the page resolves rgba(0, 0, 0, 0)`.
   ⚠ **This is a THIRD file, outside the brief's two generators.** Named rather than left: shipping
   an enactment that reds an existing verifier is not an enactment.

3. **⛔ THE DEFAULT SWITCH MADE AN EXISTING MUTATION ARM SHARPER, AND ONLY A MEASURED BEFORE COULD
   SHOW IT.** `--break-settings` went `18 → 19` because `SETTINGS ROUNDING` could not fire in
   console while console was ruled `capsule` (the stripped mutant's leftover geometry *was* the
   ruled geometry). A lane that reported "19, unchanged" from reasoning would have missed a real
   improvement, and a lane that reported it as a regression would have been wrong twice.

4. **⚠ TWO BITES HAD TO MOVE *WITH* THE RULING, AND WIDENING THEM WOULD HAVE BLINDED THEM.** Bite
   `6b` asserted the compiled radius set `["0","inherit","var(--border-radius-container,0px)"]` —
   `inherit` was the capsule's own radius and no shipped default is a capsule any more. Bite `25`
   asserted the grey-caption themes were `["console","mono"]`; it is now `["mono"]`. Both were
   **re-pointed at the new ruled answer**, not loosened: left tolerant they would have gone green on
   a regression, which is worse than no bite. Bite `25` is now also the tripwire for a lane that
   "aligns" mono with console without a ruling.

5. **⛔ THE CAPSULE BRANCH IS NOW A BRANCH NO DEFAULT REACHES — SO IT IS DRIVEN DELIBERATELY.** Both
   arms of `settings_css`'s rounding split survive, because `capsule` stays a legal edit-pass option
   in every theme. Deleting the branch is how an option quietly becomes unreachable. Bite `6i`
   compiles it on a settings table the page does not ship, and asserts `border-radius:inherit` comes
   out — the same discipline as [[instrument-without-a-consumer]], read the other way round.

6. **⚠ ONE TREATMENT IS LEGAL AND STILL CANNOT BE *SHIPPED* ON THE PHOTOGRAPHY PAGE, AND SAYING WHY
   MATTERS.** `capsule + darkgrey` passes every legality and reachability rule, but that page's
   compiled block is **mode-flat** and `darkgrey` is the one ground whose value differs by mode (the
   `s220-D1` lift). The generator refuses **by name** rather than painting the unminted value. That
   is a property of that page, **not a narrowing of the rails** — recorded on the proof page as its
   own footnote, because a refusal that names the first obstacle is not evidence about the binding
   one ([[refusal-names-the-first-obstacle]]).

7. **⚠ `s220-D2 (4)`'s DISCHARGE IS NOT ENACTED AND IS NOT THIS LANE'S.** The ruling says the
   `notes/_receipts/2026-08-25-219-role-defaults-exports.md` **PARKED CORRECTION** (2026-08-26,
   *"this would never exist"*) is **superseded** and its discharge cites `s220-D2`. That section is
   still on disk marked `NOT ENACTED`, and the receipt is outside this lane's regions. Checked
   rather than assumed: the parked correction **never reached** either generator or
   `bento-rails.html` (`grep -c "would never exist"` → `0` in all three), so nothing in the code
   contradicts the ruling — the residue is one **addition** to the receipt. Price: ~1K tk, and it is
   an ADDITION to a ratified record, never a trim ([[header-wins-over-audit]]).

## RULING-SHAPED QUESTIONS

*(All four are Dave's. Nothing below is decided and the proof page says so in its own footer.)*

1. **⬛ MONO'S GALLERY DEFAULT — still open, and the stakes just changed.** `s220-D2 (3)` leaves it
   expressly open and mono keeps `grey`. **Mono is now the ONLY theme shipping a grey caption
   ground** — three of four agree on transparent. Section 5 of the proof page draws mono in both
   modes so the choice is visible. **(a)** leave it grey; **(b)** align it with the other three;
   **(c)** rule it separately with the dark-grey ramp gap in view. ⚠ Under (a) the one theme that
   ships a caption block also ships the one that is nearly invisible in dark — `#1F1F1F` on a
   `#1A1A1A` page, ΔL\* **+2.49** (the theme-lift lane's open question 1, unchanged here).

2. **Does the `s220-D2 (4)` PARKED CORRECTION discharge get written into the receipt?** Finding 7.
   The code already agrees with the ruling; what is missing is the **record**. **(a)** append a
   discharge note under the parked section citing `s220-D2 (4)`; **(b)** leave it and let the
   ruling be the only home. ⚠ Under (b) a reader of the receipt sees a parked correction that
   reads as live, which is exactly [[premise-ages-faster-than-rule]].

3. **Do `X1` / `X2` ever get promoted?** They stay `proposed` because `s220-D2 (1)` declined to
   promote them — but `X2` (the edgeless-capsule refusal, P3) **is already enforced** by
   `capsule_legal` in `validate_settings` and refused in the browser, while its manifest status says
   `proposed`. ⚠ **A rule that refuses in the product while its record says "proposed" is a
   disagreement between the machinery and the manifest**, and it predates this lane. Not touched
   here; the ruling's instruction was to leave the status alone. Price to reconcile: one question,
   ~0 tk.

4. **Should `default_for_mode()` ever branch?** It exists to make "one default, both modes" a thing
   a caller has to ASK rather than a coincidence. Widening it to return different blocks per mode
   would be a ruling — and `s220-D1` already showed that a *value* can legitimately differ by mode
   while the *decision* does not. ⚠ The day a dial needs a genuine per-mode default, this function
   and the settings block's mode-flat fence are the two places that must change together.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** this sub's own token spend — a sub cannot read `message.usage`. Price to prove: the
  conductor's panel, ~0 tk.
- **UNPROVEN:** the `--break-keylines` arm's **count**. The mutant is **byte-identical** either side
  of the switch (measured here, md5 `583a6f43…`), so the count cannot have moved; the figure
  **306** is the theme-lift lane's measurement on that identical input, carried forward rather than
  re-run. Price to measure in this lane: one browser run, ~2K tk.
- **UNPROVEN:** the proof page in a **real browser on Dave's Mac**. Verified in the sandbox headless
  shell at 1180 and 480 only; `-webkit-line-clamp` and `@container` are both in play and both are
  copied from the artefact. Price: the runbook's Claude-in-Chrome fallback, ~2K tk.
- **PARTIALLY MEASURED — this lane's per-file `+/-`.** `role_defaults_219.py` (**282 → 514**,
  `+240/−8`) and `verify_photography_218.py` (**622 → 641**, `+20/−1`) are **exact**: the parallel
  `#220` theme-lift lane's uncommitted work touches neither. For `gen_bento_matrix_217.py`,
  `gen_foundations_217.py`, `_bento_edit_rails.json` and the two HTML artefacts the working-tree
  diff vs `HEAD` is **shared with that lane** and cannot be split by `git` without a stash (banned
  here). Classified by hunk content, this lane's share is approximately `+58/−3` (matrix),
  `+98/−7` (foundations), `+128/−2` (manifest), `+30/−1` (photography.html), `0` (bento-rails.html
  — its change is entirely the regenerated manifest's). **Stated as approximate, with the method
  named**, rather than presented as a measurement ([[planning-estimate-is-not-a-measurement]]).
- **CLAIMED — nothing.** Every mechanical statement above quotes a probe, a file and line, or a
  measured raster value.

## Fences honoured

**NO git** — nothing staged, nothing committed, no branch touched, no stash, no worktree. Only
read-only `git status` / `git diff`. **No `_rulings.json`, no `_state.json`, no memory** — the
`_rulings.json` line in `git status` was **already dirty before this lane opened** (recorded at
`/var/tmp/ds220/before-status.txt`, 27 lines) and is the conductor's inscription, not opened here.
**No release paths** (`knowledge/_release/*`, `apollo-spider/*` untouched). **No promotions, NO NEW
TOKENS.** **No light-mode value change beyond the default switch itself** — light and dark move
together because that IS `s220-D2 (2)`; every other theme's light values are byte-identical.
**⛔ THE RECEIPT IS UNTOUCHED** — `notes/_receipts/2026-08-25-219-role-defaults-exports.md` is
byte-identical, asserted by the module's own `was`-gate on every import.
**No option removed**, asserted by bites `6i`, `6j`, `R6e` and by the proof page's build refusal.
**X1/X2 still PROPOSED**, asserted in the generator and in the build script.
**Two-red law + mono error ink camp untouched** — no red, no yellow, no green in the diff or on the
page; the build script refuses if a two-red hex appears in its own output (`grep -c` → `0`).
`ls -a knowledge/assets/fonts/_desktop/TTF | grep -c '^\.uuid'` → **0**.

**My paths (20):**
`knowledge/_render/role_defaults_219.py` · `knowledge/_render/gen_foundations_217.py` ·
`knowledge/_render/gen_bento_matrix_217.py` · `knowledge/_render/verify_photography_218.py` ·
`knowledge/_render/_bento_edit_rails.json` · `showroom/_foundations/photography.html` ·
`showroom/_foundations/bento-rails.html` · `reviews/DEFAULT-SWITCH-2026-08-27-v1.html` ·
this report · `notes/_subreports/assets/2026-08-27-220-default-switch/` (13 files, counted as one).
⚠ `showroom/_foundations/{bento,grids-12col,grids-dashboard,grids-display,grids-gallery,logos}.html`
appear dirty in `git status` but are **NOT this lane's** — they are the theme-lift lane's, and the
writer's own "8 page(s) → 2 written / 1 written" plus md5 checks confirm this lane left them
byte-identical.

## Evidence

`notes/_subreports/assets/2026-08-27-220-default-switch/`

- `measured-1180.txt` / `measured-480.txt` — the full probe at both widths: the canvas font triple
  with **both** controls, then all ten specimens with dials, **computed** caption ground,
  **raster-sampled** caption ground, ink ratio, tile and image radius, caption height and column
  count, then the **13 named claims** and the verdict block. This is the file the numbers above are
  read out of.
- `evidence-four-options.png` — **the best single pointing surface**: all four legal treatments side
  by side in console, the default marked, the retired default marked, with what each paints in
  light and dark printed underneath.
- `evidence-pair-light.png` / `evidence-pair-dark.png` — before beside after, in each mode, with the
  aligned read-outs.
- `evidence-mono-open.png` — mono in both modes, unchanged, the still-open question drawn.
- `evidence-where-it-stands.png` · `evidence-where-written.png` · `evidence-not-decided.png` ·
  `evidence-foot.png` — the rest of the page.
- `build.py.txt` — the proof page's generator. **Canonical home**, not a transcription: copied to
  `/var/tmp/ds220/build.py` **(NON-REPO: sandbox-local `/var/tmp/ds220/`, `s191-D2`)** and run
  there, verified byte-identical (`cmp`). It writes exactly one path.
- `probe.py.txt` — the render-verify probe, likewise **(NON-REPO: `/var/tmp/ds220/`)**. Adapted
  from the `#220` theme-lift lane's probe; the verdicts are re-aimed from ΔL\* bands at a
  **default**: dials, geometry and the two-mode identity. The hue assertion is kept and kept split.
- `shots.py.txt` — the section-shot banker **(NON-REPO: `/var/tmp/ds220/`)**.
- ⚠ **NOT banked, and named:** `arm.py` / `varm.py`, the mutation before/after drivers, live only at
  `/var/tmp/ds220/` **(NON-REPO, `s191-D2`)**. They are eight lines each of "empty `SUPERSESSIONS`,
  re-derive, `runpy` the target" and are reproducible from that sentence; banking them would have
  added two more files that say the same thing as this paragraph.

REPLAY-THESE: `notes/_subreports/2026-08-27-220-default-switch.md` §THE MINT SITE, QUOTED (~450 tk) ·
§THE THREE GUARANTEES (~400 tk) · §Findings 2, 3 and 7 (~550 tk) ·
§RULING-SHAPED QUESTIONS 1 and 2 (~350 tk)
