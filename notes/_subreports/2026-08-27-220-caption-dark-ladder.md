# `#220`-caption-dark-ladder — the console dark caption ground, drawn as a ladder

session: `#220` · 2026-08-27
window: bento lane — Dave's dark-mode caption correction
sub index: `caption-dark-ladder`
brief: `notes/_briefs/2026-08-27-220-caption-dark-ladder.md`
tokens: `UNMEASURED` — a sub cannot read its own `message.usage`; the conductor's panel is the
only place this spend is real.

## VERDICT

**DONE.** `reviews/CAPTION-DARK-LADDER-2026-08-27-v1.html` is built and live: one focused page,
console theme, **dark primary**, the same capsule card Dave screenshotted repeated down a ladder
of **eleven** candidate caption grounds, with the light pair shown once, small, as the reference
that nothing on the ladder changes. **13 live specimens.** Token rungs and derived rungs are in
**separate sections with separate warnings** — no derived grey is presented as a token anywhere.
Render-verified in-sandbox at **1180 and 480**, font probe green against **both** controls, and
every printed number on the page **checked against the rendered pixels**, not against the token
name.

Nothing was enacted. My only repo writes are the deliverable, this report and its assets
directory.

The page found more than it was asked for. Three things matter to whichever rung Dave picks:
**console has no surface ramp of its own** (it inherits the base dark ramp and overrides only
radii and RAG hues); **that ramp is mode-inverted**, so no existing token can be repointed in
both modes without breaking the light card; and **the ramp has a hole exactly where the answer
probably lives** — the hover surface reaches 0.77× the light card's separation and the next token
up reaches 6.47×, with nothing between them and light parity falling in the gap.

COUNTS: findings `11` · ruling-shaped `6` · UNPROVEN `4`

## What was done

**Region 1 — `reviews/CAPTION-DARK-LADDER-2026-08-27-v1.html`** (69,382 bytes, new, `-v1`).

Page order: *Where it stands* (Dave's words, the light pair small, then both of today's dark
capsules at full size) → *How to read a rung* (the four numbers, and which single one has a rule
behind it) → *Rungs that already exist* (three token rungs) → *Rungs that do not exist* (five
derived rungs plus a sixth that draws what a 3:1 floor would look like) → *The same grounds
without the picture* (the ordered swatch strip) → *Every rung in one table* → *Not decided here*
→ footer.

Method, as briefed. The specimen markup is the same `<figure>` and the same photograph
(`eyeem-100014108-180570836-w1600.jpg`, real alt text and licence line on every card), and the
specimen CSS is copied between explicit `COPIED-FROM-ARTEFACT START/END` markers, taken from
`showroom/_foundations/bento-rails.html` by way of the `#220` banked source
`notes/_subreports/assets/2026-08-27-220-readings-capsule/build.py.txt`. Canon does the rest —
the page links `knowledge/canon/canon.css`, so the container, grid, role rules and the ruled 86px
gallery caption space come from canon.

**The one thing that changes between rungs is one custom-property value.** Every rung is
`data-cap-bg="darkgrey"` with a single inline substitution into `--bm-darkgrey`. No rung adds a
CSS rule, no rung redraws a card, and the ink-follows-ground pairing stays the artefact's own
two-declarations-one-decision rule (`s219-D3(3)`). Today's two rungs carry **no** override at
all, so they render through the canonical binding untouched.

**Values are solved at build time, never carried as literals** (`s200-D1` in spirit): light parity
and the 3:1 rung are both computed from the light pair and the graphics grade at mint time and
printed with their derivation named on the page.

**Region 2 — this report** and `notes/_subreports/assets/2026-08-27-220-caption-dark-ladder/`.

**Generator named.** No repo generator was run. The page is emitted by
`notes/_subreports/assets/2026-08-27-220-caption-dark-ladder/build.py.txt`, whose **canonical home
is that path** — it is copied to `/var/tmp/cdl220/build.py` **(NON-REPO: sandbox-local
`/var/tmp/cdl220/`, `s191-D2`)** and run there, so the banked source and the source that ran are
byte-identical rather than a transcription. It writes exactly one path.

**Fence honoured.** No generator, manifest, canon file, showroom page, `_rulings.json`,
`_state.json`, memory or git write. `git status --short --untracked-files=all -- knowledge/` shows
**5** lines at hand-off, the identical five that were there when I opened (`_graph-mark-
observations.jsonl`, three `_release/*` files and `_gate_pack_imports.py` — sibling lanes').
`ls -a knowledge/assets/fonts/_desktop/TTF | grep -c '^\.uuid'` → **0**.

## THE MEASURED TABLE

Console dark, page ground `rgb(26,26,26)` (`--background-default` → `--surface-digital-black`)
on every row. Ink is `--text-reverse` `#FFFFFF` except the two "today" rows as noted. **Ink** is
the ruled column (floor 4.5:1). **Separation** has no rule behind it. ΔL* is CIE L* (D65).
Every value below was read off the rendered card and cross-checked against the raster pixels.

| Rung | Ground | Token | Ink on ground | Ground vs ground | vs light parity |
|---|---|---|---|---|---|
| Today — dark-grey capsule | `#1A1A1A` | `--surface-digital-black` | 17.40:1 | **1.00:1 · ΔL\* 0.00** | 0.00× |
| Today — lightest-grey capsule | `#1F1F1F` | `--surface-subtle` (= `--surface-raised`) | 16.48:1 *(ink `--text-secondary`)* | 1.06:1 · ΔL\* 2.49 | 0.40× |
| Token 1 — hover surface | `#232323` | `--surface-raised-hover` | 15.72:1 | 1.11:1 · ΔL\* 4.45 | 0.77× |
| Derived 1 — **light parity** | `#252525` | none | 15.33:1 | 1.14:1 · ΔL\* 5.42 | **the anchor** |
| Derived 2 | `#2A2A2A` | none | 14.35:1 | 1.21:1 · ΔL\* 7.80 | 1.52× |
| Derived 3 | `#303030` | none | 13.20:1 | 1.32:1 · ΔL\* 10.60 | 2.28× |
| Derived 4 | `#383838` | none | 11.73:1 | 1.48:1 · ΔL\* 14.26 | 3.47× |
| Derived 5 | `#404040` | none | 10.37:1 | 1.68:1 · ΔL\* 17.83 | 4.86× |
| Token 2 — disabled-action | `#484848` | `--surface-action-disabled` (= `--form-background-pressed` = `--timer-background`) | 9.15:1 | 1.90:1 · ΔL\* 21.33 | 6.47× |
| *(the picture of a 3:1 floor)* | `#656565` | none | 5.83:1 | 2.99:1 · ΔL\* 33.52 | 14.22× |
| ~~Token 3 — action surface~~ | `#808080` | `--surface-action` (= `--border-subtle` = `--border-strong` = `--divider-border-*`) | **3.95:1 — BELOW THE FLOOR** | 4.41:1 · ΔL\* 44.32 | 24.40× |

**The light reference, for the parity column:** `#F0F0F0` caption on a `#FFFFFF` page =
**1.14:1 · ΔL\* 5.20**, ink 15.27:1. That is the only separation anywhere in the system that Dave
has looked at and not objected to.

## Findings

1. **Console has no surface ramp of its own.** `[data-apollo-theme="console"]` (canon.css:22160)
   and `[data-apollo-theme="console"] [data-theme="dark"]` (canon.css:22211) declare radii, RAG
   hues, segmented-control sizes and badge colours — and **no surface tokens**. The greys under
   this whole question come from the base `[data-theme="dark"]` block (canon.css:660-870). Any
   fix written "for console" is therefore a change to the shared ramp unless it is scoped
   deliberately.

2. **THE HOLE. The console dark ramp holds only three greys above the page ground, and the answer
   probably falls between two of them.** `#1F1F1F` (0.40× light parity), `#232323` (0.77×),
   `#484848` (6.47×), then `#808080`. The hover surface is the closest anything gets and it is
   **just short**; the next token is **well over**. Light parity (ΔL\* 5.20) lands in the gap.
   Probe: `assets/…/measured-ladder-1180.txt`, the `token-1` and `token-2` rows.

3. **The top of the token ramp is refused by a RULED constraint, not by taste.** `--surface-action`
   / `--border-subtle` / `--border-strong` resolve `#808080` in console dark; white
   `--text-reverse` on it measures **3.95:1**, below the ruled 4.5:1
   (`_bento_edit_rails.json` → `constraints.$ink_rule.floor`, `s219-D3(2)`). It is on the page,
   struck, with the number printed. It is the only ruled refusal on the ladder.

4. **THE STRUCTURAL ONE — the base dark surface ramp is MODE-INVERTED, so no existing token can be
   repointed in both modes.** `--surface-raised-hover` is `#232323` in dark and **`#F0F0F0`** in
   light; `--surface-action-disabled` is `#484848` in dark and **`#E1E1E1`** in light. Repoint the
   capsule's dark caption-ground slot to either of them in both modes and the light card takes a
   pale ground with white ink on it: **1.14:1** and **1.31:1** respectively, both far below the
   floor. A token rung is legal **only** as a dark-only repoint. Consequence: *any* fix that
   lightens dark while leaving light alone is either a mode-scoped alias or a new token — and a
   new token is a promotion. Both numbers are printed beside their rungs on the page.

5. **Light parity is derivable and it lands at `#252525`.** The light capsule sits 1.14:1 /
   ΔL\* 5.20 from its page. Solving for the neutral grey that gives the dark card the same ratio
   yields `#252525` (measured 1.14:1 · ΔL\* 5.42). It is drawn as Derived rung 1 and labelled in
   plain prose. **It is not a recommendation** — it is the one honest reference point for
   "enough" that exists.

6. **There is NO ruled floor for ground-against-ground, and I looked properly before saying so.**
   `_rulings.json` (260 rulings) carries nothing governing one surface against another —
   the nearest hits are `dv-2px-separation` (`#96`, a **geometric** remedy for adjacent dataviz
   blocks, not chromatic) and the **3:1 non-text grade** used by `s132-D1`, `s168-D4`, `s168-D5`
   and `s176-D2`. `_bento_edit_rails.json`'s only floor is `$ink_rule.floor: 4.5`, which gates
   **ink on its own ground**. Canon has no such rule. ⚠ If that 3:1 grade were ever applied to
   ground-against-ground, the caption ground would have to be **`#656565`** — lighter than every
   rung except the refused one. That cost is drawn on the page rather than left to imagination.

7. **NEW CLASS — page chrome inside a themed block renders in the WRONG MODE'S INK, and no gate
   catches it.** The first build wrapped the swatch strip in
   `[data-apollo-theme="console"] [data-theme="dark"]`; every label and figure beside the swatches
   went **black on black**. Two measured facts collide: (a) **canon paints a bare
   `[data-theme="dark"]` element** — the wrapper computed `background: rgb(26,26,26)` with no
   background declared by me; (b) a page-chrome custom property is substituted **at the element
   where it is DECLARED**, so `--ink-2` had already resolved to mono light's `--text-secondary`
   (`#1A1A1A`) on `<body>` and did **not** re-resolve inside the dark descendant. Measured:
   `.cdl-strip-lbl` `color: rgb(26,26,26)` on a `rgb(26,26,26)` ground. The working pattern, used
   by every specimen panel on the page, is to reference **canon tokens directly** inside a themed
   element (`var(--text-default,#1A1A1A)`), never a chrome alias. The fix and both measurements
   are inscribed in the page's own stylesheet where the mistake would be reintroduced.

8. **NEW CLASS — `opacity` as refusal vocabulary FALSIFIES a colour specimen.** The artefact dims
   a refused specimen to `.55`. Applied to the refused `#808080` rung, the raster read the ground
   as **`rgb(185,185,185)`** against `rgb(128,128,128)` computed, and the page ground beneath it
   as **`rgb(128,128,128)`** against `rgb(26,26,26)` — the dimming composited and falsified the
   exact two values the rung exists to show. **Caught by the pixel probe, not by the computed-style
   probe**, which is the whole argument for reading the raster. The refusal is now carried by the
   strike, the weight and the printed reason alone.

9. **A contrast-ratio solver must search DIRECTIONALLY.** The first parity solve returned
   **`#0A0A0A`** — *darker* than the page it was meant to lift off — because a contrast ratio is
   symmetric (max over min) and an unconstrained scan finds the dark solution first. Fixed to
   search upward from the page channel, with an assert. Gated in the build script with the reason
   written next to it.

10. **The arithmetic is calibrated against the repo's own recorded figure.** `_bento_edit_rails.json`
    records the capsule/grey chord member at **16.48** in console dark. The same figure computed
    here from the rendered pixels is **16.48**. The maths on this page and the maths in the
    manifest agree — stated on the page as a sanity check, not as a finding.

11. **The artefact's `loading="lazy"` defeats a naive render-verify.** The specimen markup is
    copied verbatim and carries `loading="lazy"`, so the six rungs below the fold never decoded:
    the first probe reported **6 broken images** and would have screenshot blank tiles. The probe
    now walks the document and waits on `every(i => i.complete && i.naturalWidth > 0)` before
    measuring. Worth carrying into `_RUNBOOK-render-verify.md` by whoever owns it — a long page of
    lazy specimens is now a standing shape here, and a blank tile is exactly the kind of red that
    reads as a broken build.

⚠ **One declared cosmetic:** the page-chrome `var()` fallback literals copied from the artefact
include `#D7D8D6`, which is very slightly warm. It is a **fallback only** — it paints nothing while
canon loads — and it is copied, not invented. Every **candidate ground** on the ladder is asserted
neutral (R=G=B) at build time and re-asserted from the raster: **0 non-neutral grounds** at both
widths.

## RULING-SHAPED QUESTIONS

*(All six are Dave's. Nothing below is decided, and the page says so in its own footer. No
recommendation is offered on question 1 — the brief's whole point is that we never build the
likeliest reading.)*

1. **Which rung?** The page draws eleven, ordered, with the token and derived sets visually
   separated. The cheapest answer is Token rung 1 (`--surface-raised-hover`, `#232323`) — an
   existing token, no promotion, and 0.77× the light card's separation. The nearest-to-reference
   answer is Derived rung 1 (`#252525`, light parity) — and it does not exist.

2. **Is a ground-against-ground floor minted from whatever he picks?** There is no such rule today
   (finding 6). (a) The rung is a **single value for a single chord member** and nothing general
   is written. (b) The rung's separation becomes a **floor** governing every caption ground against
   every page ground, in all four themes. ⚠ Under (b), the number he points at silently becomes a
   rule with a very large blast radius; under (a) the same collision recurs the next time a ground
   lands on a ground, because nothing prevents it.

3. **If a floor is minted, at what grade?** (a) **Light parity, 1.14:1 / ΔL\* 5.20** — the
   separation already accepted in light. (b) **The repo's 3:1 non-text grade**, which would force
   `#656565` and read as a distinctly lighter band rather than an edge (drawn on the page). (c)
   ΔL\* rather than a ratio — at these luminances ΔL\* discriminates far better than a contrast
   ratio does, which is why both are printed on every rung.

4. **Dark-only repoint, or a new token pair?** (a) **Dark-only alias** — point the capsule's dark
   caption-ground slot at an existing token in dark and leave light on `--surface-digital-black`.
   No promotion, but it makes the slot's binding mode-dependent, which nothing else in the ramp is.
   (b) **Mint a token** — a light value and a dark value together. That is a promotion, and
   promotions are his. ⚠ Finding 4 means there is no third option: repointing an existing token in
   both modes breaks the light card, with the numbers printed.

5. **Does `--surface-action`'s failure retire it from the caption-ground family altogether?** It
   fails the ruled ink floor in console dark at 3.95:1 (finding 3) but **passes** in light at
   6.10:1. (a) Refuse it for this slot in dark only. (b) Refuse it for reversed-ink grounds
   everywhere, which is a wider statement about `--border-subtle`/`--border-strong` being used as
   a ground at all.

6. **Do the other three themes get swept?** Only console was measured — the chord is
   console-scoped by `s219-D3(3)`. Given finding 6 (nothing anywhere governs ground against
   ground) I would expect collisions elsewhere. (a) Sweep now, as part of this ruling. (b) Rule
   console and book the sweep. Price to sweep: 4 themes × 2 modes × 4 caption grounds × 3 page
   grounds ≈ 96 measured pairs, one script, ~8–10K tk.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** this sub's own token spend — a sub cannot read `message.usage`. Price to prove:
  the conductor's panel, ~0 tk.
- **UNPROVEN:** whether the same collision exists in **mono, legacy and supercharge**. Console
  only was measured, by scope. Price to prove: question 6 above, ~8–10K tk.
- **UNPROVEN:** the page in a **real browser on Dave's Mac**. Verified in the sandbox headless
  shell at 1180 and 480 only. `-webkit-line-clamp` and `@container` are both in play and both are
  copied from the artefact, so a divergence would be the artefact's too. Price to prove: the
  runbook's Claude-in-Chrome fallback, ~2K tk.
- **UNPROVEN:** **which** of the two capsule members Dave was actually looking at. His words name
  "capsule mode" and not a caption ground. Both are drawn as "Today 1" and "Today 2" and both are
  defective in dark, so the ladder is correct either way — but the premise is unconfirmed and I am
  not going to launder it into a fact. Price to prove: one question to Dave, ~0 tk.
- **CLAIMED — nothing.** Every mechanical statement above quotes a probe, a file and line, or a
  measured raster value.

## Evidence

`notes/_subreports/assets/2026-08-27-220-caption-dark-ladder/`

- `measured-ladder-1180.txt` / `measured-ladder-480.txt` — the full probe at both widths: the
  canvas font triple with **both** controls (target/uf/ufor all `346.88`; DejaVu `375.39`;
  nonexistent `301.07` — the target differs from both, so this is the real HSBC cut and not a
  silent fallback), then all 13 specimens with **computed** caption ground, **raster-sampled**
  caption ground, computed and raster page ground, ink ratio, separation, ΔL\*, caption height and
  column count. This is the file the table above is read out of.
- `evidence-today-the-defect.png` — the two shipping dark capsules, the caption sitting on a
  ground you cannot tell from the page.
- `evidence-token-rungs.png` — the three token rungs, including the refused one, struck and
  **not dimmed**.
- `evidence-derived-rungs.png` — the five derived rungs plus the 3:1 rung.
- `evidence-strip-ordered-ladder.png` — the ordered swatch strip. **This is the best single
  pointing surface on the page**: eleven grounds, in order, on the page ground, with the picture
  taken away.
- `evidence-light-reference.png` — the light pair and the parity anchor.
- `evidence-480-stacked.png` — the narrow band, stacked, verifying the responsive collapse.
- `build.py.txt` — the generator. **Canonical home**, not a transcription: it is copied to
  `/var/tmp/cdl220/build.py` and run from there.

**Render-verify, driven not asserted.** At 1180 **and** 480: **8 sections, 11 rungs, 11 strip
rows, 13 specimens**; every `.c-bento__grid` resolves **1 column**; wall widths **360px** (rungs)
and **240px** (light references) — both inside canon's single-column band, so no two specimens are
compared across a layout band (the `ds-054` class rule); caption height **86px** on every
specimen, which is canon's ruled gallery caption space, so the copy really is running through
canon; tile radius `20px` with `overflow:hidden` on every capsule; **0** horizontal overflow;
**0** broken images; **0** non-neutral grounds; **0** pixel-vs-computed disagreements; **0**
printed-vs-measured disagreements — the page's own numbers were parsed back out of the DOM and
checked against the values measured from the raster. Registration was checked per the `#217`
pothole (throwaway `full_page` shot first, boxes re-measured after capture): **0** boxes moved.

**Colour law untouched.** No red, no yellow, no green anywhere. The two-red law and the mono error
ink camp are not involved. Refusal is carried by weight, a strike and a printed reason. Type is
`.t-cm-*` / `.t-ed-*` throughout — `t-ed-heading-3`, `t-ed-heading-4`, `t-ed-body`,
`t-ed-body-small`, `t-ed-caption`, `t-cm-legal`, `t-cm-figure-6`; no raw `font-size` or
`font-family` outside the copied-from-artefact block.

REPLAY-THESE: `notes/_subreports/2026-08-27-220-caption-dark-ladder.md` §THE MEASURED TABLE
(~700 tk) · §Findings 2, 4 and 6 (~800 tk) · §RULING-SHAPED QUESTIONS 1–4 (~700 tk)
