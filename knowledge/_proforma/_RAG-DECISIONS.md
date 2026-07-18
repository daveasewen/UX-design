# RAG — decisions ledger

Per-pillar running record of Dave's review rulings and the WHY, so iterative feedback survives the
session that produced it. Sibling to `_TYPE-DECISIONS.md` / `_DATAVIZ-DECISIONS.md`.

---

## R-D1 — RAG promotion, round one (2026-07-18)

Source: `reviews/RAG-PROMOTION-2026-07-18.html`, 12 pins.

### ⚠️ PIN ORDER IS NOT ROW ORDER — corrected against the numbers

In §5 the four pins mapped to rows in order and read perfectly. **In §1 they did not.** Taken in
order, pin 2 ("good with white text") would have landed on **amber**, whose delta `#C58720` gives
white **3.06:1** — below AA for normal text. And pin 4 ("bad with both") would have landed on blue,
which **passes** with white at 4.60:1.

Recomputed every pair from the hex. Only ONE hue fails with both white and `#333`: **amber**
(white 3.06 · `#333` 4.13, both large-text-only). That is also exactly the trap `GOOD-MORNING`
flagged. So the marks are:

> **METHOD, keep it:** pin ORDER records the order Dave marked things, not the order they appear.
> §5 agreed by coincidence. **Resolve pins against the DATA, never against sequence.** T-D10 was
> settled by pin POSITION; this one had to be settled by arithmetic. Both beat the pin's text.

### §1 · Light mode — RULED

| hue | delta | white | ruling |
|---|---|---|---|
| red | `#B92F1E` | 6.02 PASS | **good with white** |
| green | `#16864E` | 4.61 PASS | **good with white** |
| blue | `#2573DC` | 4.60 PASS | **good with white** |
| **amber** | `#C58720` | **3.06 FAIL** | **"bad with both white and black, we have to fix this"** |

**⭐ THE BIG ONE — the dark-text variant is DROPPED.** Dave, three times: *"good with white text,
we don't need the black text version."* **White is the RAG text colour, universally.** This kills a
whole variant axis: no `#333`-on-RAG anywhere, so the amber `#333` 4.13 trap stops being a variant
to maintain and becomes moot. **Simplification, not a constraint.**

### §2 · Dark mode — RULED
`red #CC4333` white 4.75 **good** · `blue #2674DC` white 4.55 (unmarked, passes) ·
**`amber #C0831F` white 3.23 — problem, fix** · **`green #1AA05C` white 3.37 — problem, fix**.

### §5 · The near-black — RULED, all four

| value | ruling | why (Dave's words) |
|---|---|---|
| `#000000` | **RETAIN IN THE KB** | *"black must be retained in the KB so that it's the source of truth… there will be a query bot for the KB, so as this is a brand colour it must be kept."* **Not a usage ruling — a SOURCE-OF-TRUTH ruling.** The KB answers questions about the brand, so it must carry the brand's real black even where screens use something else. |
| `#1A1A1A` | **THE DIGITAL BLACK** | *"a replacement on screens, for screens. We'll use this a lot in apollo mono."* |
| `#1D1D1D` | **DROP** | *"don't need this"* — `color/grey/dark-mode/600` is not needed alongside the digital black. |
| `#333333` | **CANON, STAYS** | *"This is canon and stays."* |

### §1 · Incumbents — RULED (pin 12)
*"we're ditching all of the incumbents for new components but they must remain when we create
legacy components, they will be in a theme in the future."*
⇒ Deltas win for all NEW work. Incumbent values are **NOT deleted** — they are retired into a
future **legacy theme**. Tombstone, do not remove. Consistent with `_retired/` (tracked, residual
value) vs `_to_delete/`.

---

## OPEN — carried out of R-D1

1. **Amber fails in BOTH modes and must be re-cut.** Darkening on the same hue (37°) and saturation
   (0.84) until white reaches AA:
   - light `#C58720` → **`#9E6C1A`** (white 4.55, value −20%)
   - dark `#C0831F` → **`#9D6B19`** (white 4.61, value −18%)
   **PROPOSED ONLY — not promoted.** A 20% value drop is a visible change to a semantic RAG colour
   and it is Dave's call whether that still reads as *amber* rather than brown. **Needs a specimen
   at real extent** (per T-D10: a specimen must reproduce the condition, not just the element).
2. **Dark-mode green `#1AA05C` (3.37)** — same treatment needed, not yet computed.
3. **⚠️ THIN MARGINS on the values Dave passed** — green light **+0.11**, blue light **+0.10**, blue
   dark **+0.05** over the 4.5 threshold. These pass, but by less than a rounding step. Any later
   nudge to those hues silently drops them below AA. **Recommend the contrast gate pin these four
   with an explicit margin note**, so a future edit fails loudly rather than quietly.

---

## R-D2 — Background/glyph split + matting (2026-07-18)

### The token shape — RULED
Dave: *"I think we'll have one for backgrounds and one for glyphs maybe."*
⇒ **Two tokens per hue: `background` (fills — tag, badge, chip) and `glyph` (icons, arrows, text
on the page).** "Glyph" is Dave's word and it is better than my "ink" — it covers icon, arrow and
text in one term. Use it.

**Structure uniform, values diverge only where the hue forces it.** Red/green/blue hold the SAME
value in both roles (they sit at mid luminance and work either way). **Only amber diverges.**

### ⭐ AMBER IS AN ACKNOWLEDGED CARVE-OUT — not a new problem
Dave, closing the question: *"amber is always an issue, that's why only this has black text, we
have no choice, it already has a carve out."*

**This corrects my framing.** I presented the ground/glyph divergence as a new cost with "three
ways out" (accept it · forbid bare amber glyphs · outline the fill) and recommended forbidding
them. **Wrong emphasis.** Amber had ALREADY broken the pattern at the text-colour level. A separate
glyph value is not a second exception — it is **the same exception appearing in a second place**.

> **THE PRINCIPLE, stated once:** *Amber is the light hue. One carve-out, two consequences —
> it takes DARK ink on its fill, and its glyph is a DARKER value than its background.*
> Do not re-litigate this per artefact. Do not "fix" the mismatch later; it is intentional.

**WHY it is unavoidable, for whoever asks next:** amber's identity IS its lightness. To clear
4.5:1 on a white page a glyph must sit near **L 0.57**, where the hue reads as ochre. There is no
amber that is simultaneously light enough to be amber and dark enough to be a glyph. Red, green and
blue have no such conflict. This is the hue, not the palette.

### Matting — method + measurement
**OKLCh, not HSL.** HSL "saturation" is not perceptual — equal HSL sat across hues does not look
equally vivid, and pulling it bends the hue. OKLCh separates L/C/H perceptually so chroma drops
with the **hue held to the decimal** (Dave: *"correct hue"*).

**Measuring corrected the brief.** Green is ALREADY less chromatic than red (**0.72×**) and blue is
EQUAL to it (**1.00×**). So "Benetton" was not purely saturation — blue and amber also sit
**lighter**. Ladders move L as well as C.

**Matting repays the R-D1 margin debt.** Green (+0.11) and blue (+0.10) cleared 4.5 by less than a
rounding step. All candidates target **5.0** (white text) / **7.0** (dark ink), so "more grown up"
and "no longer one nudge from failing AA" are **one move, not two**.

### Marks taken
- **blue** — *"I like this for both"* → one value, both roles. Step **OPEN**.
- **green** — *"This for both"* → one value, both roles. Step **OPEN**.
- **amber** — *"this for glyphs, but not for backgrounds"* → confirms the divergence; the GLYPH
  ladder is right, the BACKGROUND ladder is **NOT**.

### ⛔ OPEN — first thing next session
1. **Which rung?** Three pins, one per hue, four rows each, and **nothing to resolve them against**
   — contrast is deliberately near-identical across steps (green/blue 5.00–5.05, amber 7.01–7.06),
   so there is no numerical tell and pin position was not in the export. **Do not guess.** Needs:
   `as now` · `matted 15%` · `matted 28%` · `matted 40%`, per hue.
   > **METHOD DEBT:** three sheets, three different disambiguation routes — pin POSITION (T-D10),
   > ARITHMETIC (R-D1), and here NEITHER. **The review overlay should capture the row identity
   > with the comment.** That is a product fix to the overlay, not a process fix — register it
   > against [[review-layer-product-feature]].
2. **Rebuild the amber BACKGROUND ladder lighter.** Mine targeted 7.0:1 with dark ink, forcing every
   candidate to L≈0.72 — all four DARKER than the current `#FFBB33` (L 0.834) and back toward the
   brown Dave rejected. Correct window is roughly **L 0.76–0.81**: still AAA against `#1A1A1A`,
   still recognisably amber. The amber glyph ladder stands as built.
3. Dark-mode green `#1AA05C` (3.37 white) — still unfixed.
4. Dark-mode red `#CC4333` (3.97) and blue `#2674DC` (4.15) as GLYPHS on `#111` — pass 1.4.11 for
   icons, **fail 4.5 for text**. Dark-mode glyph tokens may need their own lift.

---

## R-D3 — AMBER, SOLVED (2026-07-18)

### The values — RULED
| token | value | L | job | measured |
|---|---|---|---|---|
| **`amber/background`** | **`#F0B13A`** | 0.800 | fills — tag, badge, status/tolerance cell | ink on it **9.16** |
| **`amber/graphic`** | **`#C58900`** | 0.673 | chart series, standalone marks | **3.02** on white · **6.25** on `#111` |

Hue held at **79.5°** in both; chroma C 0.147. Dave picked the background as the exact centre of
`#F7B326` / `#EFB64F` / `#F0AD19` / `#E8B048` — midway on BOTH axes.

### The two rules — RULED
1. **Amber is always paired with black text.**
2. **Amber is not a *directional* delta colour** (up/down/gain/loss). It REMAINS valid for **status
   and tolerance** — RAG health, watch states, within-tolerance variance. Narrowed from my broader
   "not a data colour" after Dave pushed back: *"this is for finance, we might not get away with
   this one."* He was right — amber is pervasive in financial status reporting, and variance-to-
   tolerance is delta-adjacent. The narrow rule costs nothing: a status cell is a fill with black
   text, which rule 1 already covers.

**⚠️ GATE IT.** An ungated rule will be broken — `{#type26-019}` was BLOCKING for two weeks while
four tranches breached it. Both rules are mechanically checkable: flag any amber used as `color` on
a text-bearing element, and any amber inside `.delta`. **Not yet built.**

### Why there are two ambers — it was NOT a design compromise
I spent much of the session treating the second amber as a cost to be argued away. **`{#dv-016}` had
already decided it**: ≥3:1 rendered contrast for **series fills**, blocking, enforced in
`_validate_dataviz.py`. The light amber is **1.90** against white, so it cannot be a chart colour —
settled before today, independent of anything we discussed. The only open question was its value.

> **THE PATTERN, third instance today.** The ochre glyph, the 49-file inline sweep, and "no Univers
> in-sandbox" were all me solving a problem the system had already answered. Not stale FACTS this
> time — a stale READING of our own rules. **Check the KB and the gates before designing a solution.**
> Belongs in the consolidation track.

### Dave's framing, kept because it is the mechanism
*"The other colours are belt and braces, we only have the belt for amber."* Red/green/blue clear
4.5:1 unaided — label AND contrast. Amber only ever has the label. Remove the label and the belt is
gone, which is precisely when `amber/graphic` is required.

### Corrections I made and Dave caught
- Built the lone-glyph value at **4.5:1** (the TEXT threshold, 1.4.3) when a lone icon needs **3:1**
  (1.4.11). One rung too dark — that is what produced the ochre. Wrong rung, not wrong idea.
- The RAG-ARTEFACTS sheet painted arrows in the FILL colour, contradicting the background/glyph
  split it was built to demonstrate.

### ⚠️ FLAGGED FOR DAVE — a live contradiction in canon
**`{#dv-017}`(a)** permits **red/green** for delta indicators while naming **"RAG-style cells"** as
one of the indicator forms. RAG includes amber by definition. **The rule permits a palette it also
excludes.** Surfaced by Dave's finance challenge. Needs a ruling; not resolved here.

### Known consequence, stated before someone finds it
`amber/background` (L 0.800) and `amber/graphic` (L 0.673) are far enough apart in lightness that
**side by side in one view they read as two ambers, not one.** Unavoidable given dv-016. Expect it
where a status chip and a chart series share a dashboard.

### OPEN
- Green + blue matting rungs — Dave's pick, still needed (`as now` / `−15%` / `−28%` / `−40%`).
- Dark-mode green `#1AA05C` (3.37 white) — unfixed.
- Dark-mode red `#CC4333` (3.97) / blue `#2674DC` (4.15) as GLYPHS on `#111` — pass 1.4.11 for
  icons, **fail 4.5 for text**.
- The `dv-017` RAG-cell contradiction above.
- Build the amber gate.
