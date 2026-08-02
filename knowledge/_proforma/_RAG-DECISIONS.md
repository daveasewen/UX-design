# RAG — decisions ledger

Per-pillar running record of Dave's review rulings and the WHY, so iterative feedback survives the
session that produced it. Sibling to `_TYPE-DECISIONS.md` / `_DATAVIZ-DECISIONS.md`.

---

## R-D25 — Supercharge carries its OWN warm neutral ramp; ink = warm/2 #13110E; Console LOCKED ≡ Mono on the shared DNA layers (2026-07-22). Source: Dave, in-chat rulings on the ADR-0014 reflect-back.

The theming clean-room's rulings, inscribed in full in **ADR-0014** (per-theme neutral primitives +
the opacity-snaps-to-ramp state test) — this entry exists so colour-recall finds them in the ledger:

1. **The neutral DNA tier** `color/neutral/1–15` + the warm primitive `color/warm/1–15` (OBSERVED,
   Figma `DS3tkWgaM1OsJg9ZC7nVLK` swatches, 2026-07-22) — items 1–2, "cool".
2. **SC ink = `warm/2 #13110E`** — *"just use this we can always change"* — enacted as the ANCHOR
   REMAP (`neutral/4 → warm/2`): ink ≡ digital-black ≡ action fill move together. SC **dark-mode**
   values are index-symmetric agent proposals for Dave's review sheet — *"lets calculate the dark
   mode values and I can review."*
3. **Console ≡ Mono on neutrals / interaction-opacity / status / dataviz — LOCKED**: *"lets lock
   this in, they should be the same"* — enforced by the registry sibling FENCE + cascade selftest.
4. **State mechanism = theme property** (Mono+Console opacity · SC colour · Legacy explicit) with
   the blocking snap gate `_validate_state_snap.py` — item 3, "cool"; R-D23's tabs values are the
   calibration consumers.

**Addendum (2026-07-22, post-push — Dave):** *"the inactive tabs still have to pass Ally, they're
inactive not disabled remember."* → text-state AA floor wired into `_validate_state_snap.py` (interactive
states carry NO contrast exemption, per theme, every non-exempt theme); first catch = SC dark inactive at
the DNA index (3.89:1) → SC override dark `warm/11 #AA9B92` (7.01:1), provisional-agent on the sheet.

Edges: refines(ADR-0011, scope=supercharge-neutrals) · refines(R-D19, scope=supercharge) · verified-by(theme-cascade-selftest) · verified-by(state-snap-gate)

---

## R-D23 — Tabs (Mono): ink bar · SEPARATE red-status badge · opacity-snap inactive; Legacy keeps red (2026-07-22). Source: Dave, live on the tabs review v4 (`reviews/TABS-ACTIVE-ink-vs-legacy-2026-07-21-v4.html`).

`tabs/active` was the last Mono surface resolving a Legacy red (the R-D19 drift class, flagged at R-D22).
Ruled by the R-D22 logic — **selection is structure, not status** — so the active-tab underline becomes
the **ink pair** (`#1A1A1A`/`#FFFFFF`, `$alias` `mono/4` + white); the Legacy override keeps `#DB0011`.

Three parts, ruled together on the harness:
1. **Bar = ink** (Mono) / red (Legacy).
2. **Badge is its OWN slot** (not shared with the bar): `tabs/badge/background` = Mono status red
   `#B92F1E` (white numeral, 6.02:1 — legal on red per type26-013) / Legacy `#DB0011`. Splitting the slot
   dissolves the type26-013 tension a black badge would have caused (a white numeral is red-only).
3. **Inactive-tab de-emphasis = opacity, snapped** — the primary-action button-hover mechanism (sheet v7):
   an operational α fades ink over the surface and **snaps to the nearest AA-passing mono rung**; two tokens
   stored (`tabs/inactive.opacity` operational + `tabs/inactive` portable colour). At α 0.70 → **mono/7 light
   / mono/10 dark** (both AA). **Weight is CONSTANT across states** (Dave: active differs by the bar, not a
   heavier label). Legacy mechanism = `[none]` (no opacity; bar-only differentiation) per R-D24.

Not yet enacted in tokens — lands with the theming clean-room (per-theme mechanism, brief
`notes/_briefs/2026-07-22-theme-primitives-architecture-brief.md`).
Edges: refines(R-D22) · relates(button-sheet-v7) · relates(ADR-0009) · verified-by(contrast-gate)

---

## R-D24 — Apollo Legacy is EXEMPT from the AA floor: it conforms to the existing HSBC system as-built (2026-07-22). Source: Dave.

Ruling, reflected back + confirmed: *"No AA for Legacy in this case, it should conform to what exists
already (the clue is in the name)."* Apollo Legacy is a **faithful reproduction of the existing legacy
interfaces**, not a redesign — so the AA floor (ADR-0004 / `_STANDARDS.md` §3) does **not** gate it. Its
historically sub-AA pairs stand as-built (e.g. white-on-teal `text/on-success` 3.47:1 · badge
white-on-`#DB0011` ~4.02:1).

**Scope: Legacy ONLY.** Mono, Console and Supercharge keep the AA floor unchanged — the "most accessible
bank" aspiration (ADR-0004) is untouched; Legacy is the single named exception, superseded over time not
perfected. **Enactment (theming clean-room):** Legacy pairs are recorded in the audit as **EXEMPTED
(documented), not as passes** — a theme-level carve-out via the `RULED_PAIR_EXCLUSIONS` mechanism
(tag `theme=legacy`, reason = this ruling).
Edges: bounds(ADR-0004, scope=theme=legacy) · bounds(_STANDARDS.md §3, scope=theme=legacy) · enacted-by(ADR-0014)

---

## R-D22 — `progress/complete` = INK (progress is structure, not status) + Badge mints the component slot `badge/background`; the Mono red-drift pair CLOSED (2026-07-21). Source: Dave, live on the showroom harness (Phase-1 worker-A session; verbatim quotes preserved from the worker receipt).

Phase-1's theme-response audit found the last two Mono surfaces resolving Legacy `#DB0011` (the R-D19
drift class): `progress/complete` (flat both modes, pre-R-D19 "brand red" note) and Badge's `--surface`
(via the OLD bare `primary/*` ladder — a path no theme override reaches, so Badge rendered `#DB0011` in
all four themes by accident of wiring, not by ruling).

**The trail — three moves in one evening, inscribed whole so no intermediate state reads as final:**

1. **First ruling:** *"resolve this to the newer red status color"* — the WHY, verbatim: *"mono is named
   mono for the very reason it only uses colour with intent, rag, status and dataviz only."* Both seated
   on the Mono status red. Dave's contrast hunt (*"is there a red value for glyphs that carry meaning
   like arrows etc"*) answered by arithmetic: **black FAILS both reds** (3.49:1 on `#B92F1E` · 4.42:1 on
   `#CC4333`); **white passes both** (6.02 / 4.75) — breach-is-white survives on numbers, not habit.
2. **Progress refined on the harness:** *"i think this is the right behavior and in mono and console it
   should be black. the colours in legacy and supercharge are fine."* → **`progress/complete` = the ink
   pair `#1A1A1A`/`#FFFFFF`** (`$alias` `mono/4` + white, mirroring `text/default`; literal black is
   invisible on the dark page — interpretation reflected back before enacting). Console inherits Mono;
   **Legacy keeps `#DB0011` via its override set; Supercharge gains its FIRST override**
   (`#B92F1E`/`#CC4333`, the exact pair on screen at ruling time — the file's "deliberately empty"
   description superseded for this one path). **Progress is STRUCTURE, not status.**
3. **Badge:** *"the colours are fine apart from Legacy, it should be the legacy primary red on both
   light and dark."* → minted **`badge/background`** (component tier, the `button/primary/*` precedent):
   Mono `$alias` bare `rag/error` (per-mode `#B92F1E`/`#CC4333`, numeral WHITE); **Legacy overrides it
   flat `#DB0011` both modes — brand-primary, deliberately NOT the Legacy error pair** (the slot exists
   precisely so badge ≠ error can diverge per theme). Known fidelity condition: white numeral on
   `#DB0011` ≈ 4.02:1 → **joins Legacy `text/on-success` (white-on-teal) as the Legacy
   fidelity-vs-AA family — rule the family together, queued.**

**Closes** the OWED `progress/complete` Mono ruling (deferred since R-D19/R-D20). **`tabs/active` is now
the LAST unruled red** (archived consumer). Verified: cascade 32 paths / 61 projections in sync; canon
projections spot-checked by worker AND conductor independently; full build green.

Edges: refines(R-D19, scope=progress-complete+badge) · relates(ADR-0011) · relates(B-D1) · verified-by(showroom/progress-tracker.html) · verified-by(showroom/badge.html)

## R-D21 — the decision-graph audit's two conflicts RESOLVED: role-uniformity superseded + red's mode-stability bounded to the fill (2026-07-21). Source: Dave, on the ADR-0012 rulings sheet ("I'm happy with all the recommendations").
The ADR-0012 corpus audit surfaced two live tensions, queued (never auto-resolved) and ruled on
`reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.REVIEW.html`:

1. **C1 — R-D2's "red/green/blue hold the SAME value in both roles" claim is SUPERSEDED** (claim only —
   R-D2's background/glyph token *shape* stands). The per-role split is the evolved truth: glyphs need
   glyph-strength contrast on the page, fills need salience against it — different jobs, different values.
   Evidence that decided it: success-glyph `#2B7E4F`/`#4A9568` ≠ success-background `#5DAC7B`/`#43AD6F`
   (R-D18/R-D14); error-glyph dark `#CC4333` ≠ error fill `#B92F1E` (R-D20). Amber stops being "the only
   divergent hue" — it was only the first.
2. **C2 — R-D7's "red = mode-stable, one value light+dark" is BOUNDED to the FILL role.** The status/fill
   red stays one value (`#B92F1E`, both modes, white text). The **glyph** role may diverge per-mode:
   `rag/error-glyph` = `#B92F1E`/`#CC4333` (R-D20) — the dark lift inherits R-D1's dark-red ruling and buys
   glyph contrast on `#1A1A1A`. No values change; the scope is now recorded instead of implied.

**This entry is the first written under the ADR-0012 edge convention** (accepted same day, all
recommendations): edges below in the ruled grammar; the corpus-wide inscription of the audited seed
(`notes/_decision-graph-seed-2026-07-21.json`) is the queued Sonnet pass, generator-verified.

Edges: supersedes(R-D2, claim=role-uniformity) · bounds(R-D7, scope=fill-role) · refines(ADR-0012) · verified-by(reviews/DECISION-GRAPH-CONVENTION-2026-07-21-v1.REVIEW.html)

## R-D20 — error / warning / information sets COMPLETED; the last Legacy RAG hexes evicted from Mono (2026-07-20). Source: Dave, on the live tuner.
Ruled the open tint slots on `reviews/RAG-ERROR-WARNING-INFO-2026-07-20-v1.html` (the R-D18 success tuner cloned
to three sets: OKLCh sliders + live label-contrast + salience-ramp guard). This closes the R-D17 debt for the
three non-success sets exactly the way R-D18 closed it for success.

**The signal colours were already ruled and were NOT re-decided** — breach red `#B92F1E` (R-D7), watch amber
`#F0B13A` fill / `#C58900` glyph (R-D3/R-D11), info blue `#5F92B9` fill / `#306EC6`·`#2674DC` glyph (R-D10/R-D14).
Only two things per set were open, and both are now settled:

- **Message TINT (the panel background), re-hued off Legacy toward the Mono signal hue:**
  | set | tint light (was Legacy) | tint dark (was Legacy) | label contrast |
  |---|---|---|---|
  | error | **`#F1E0DC`** (was `#F9F2F3`) | **`#2C120D`** (was `#260005`) | 13.62 / 16.77 |
  | warning | **`#F6E5CC`** (was `#FFF8EA`) | **`#3C2C13`** (was `#221701`) | 14.09 / 12.88 |
  | information | **`#D6E3EC`** (was `#EBEFF4`) | **`#092131`** (was `#000D1B`) | 13.31 / 15.80 |
  Dave lifted the warning-dark seed (`#261700`→`#3C2C13`) to keep it reading **amber, not brown** — the one
  judgement call the tuner surfaced. `$alias` dropped on all three tint tokens (they carry their own Mono
  values, matching the `-background`/`-glyph`/`success-tint` direct-value pattern).

- **Bare ROLE rebased off its Legacy alias onto the glyph** (the on-page indicator role), as `rag/success` did:
  `rag/error` → `rag/error-glyph` (`#B92F1E`/`#CC4333`); `rag/warning` → `rag/warning-glyph` (`#C58900`);
  `rag/information` → `rag/information-glyph` (`#306EC6`/`#2674DC`). Legacy red/amber/navy are Apollo Legacy's
  alone (R-D19).

**Effect.** Six Mono snippets that bound the bare roles were swept to match (Account-card, Dropdown,
Input-fields, List-items, Selection-controls, Status-indicator) — parallel to the seven de-tealed for success.
**Notifications was NOT converted** (§A-AUTH DO-NOT-CONVERT): it is an Apollo **Legacy reference** — its
`#A8000B`/`#FFBB33`/`#305A85` are legitimate Legacy hexes, so its RAG vars are `driftAllow`-waived in the snippet
gate, with the proper long-term fix being a retag to the Legacy theme (future build). Build green 37/37.

**Unblocks Alert / Banner / Toast** (§C·3). **Still deferred:** `tabs/active` + `progress/complete` (unruled Mono
values, R-D19 — their consumer components are archived). The theme-provenance gate stays **advisory** — flipping
it to blocking still needs the broader foreign-hex cleanup (58 hexes / 67 files remain, down from 68), which is
the parked archived-file relocation, not this ruling.

Edges: refines(R-D17) · refines(R-D18) · bounds(R-D19) · conflicts-with(R-D2, claim=red/green/blue hold the SAME value in both roles, resolution=ruled, ref=R-D21) · conflicts-with(R-D7, claim=red = mode-stable, one value light+dark, resolution=ruled, ref=R-D21)

## R-D19 — Red belongs to a THEME, not to Mono: Legacy red vs the Mono status red (2026-07-20). Source: Dave.
**Ruling (verbatim intent):** *"these reds are valid for Legacy only — we have a new red for Mono and it is
only used for status and RAG."* Reflected back and confirmed: red-as-**action/navigation** is an **Apollo
Legacy** signal; **Apollo Mono** carries its **own** red, used **only for status/RAG** (+ dataviz signal),
never for CTAs, tabs, or progress.

**The two reds, pinned:**
- **Legacy red** = `#DB0011` (brand primary) and `#A8000B` (Legacy error, light). Roles that currently hold it:
  `primary/background`, `primary/border`, `tabs/active`, `progress/complete`, and the bare `rag/error`
  (light `#A8000B` / dark `#DB0011`). **Valid in Apollo Legacy's override set only.**
- **Mono red** = `#B92F1E` — the ruled RAG **breach** value (R-D7/R-D14, WHITE text, mode-stable) and the
  dataviz **loss** signal (`data/delta/loss`). **This is Mono's only red, and only status/RAG/dataviz may
  use it.** It is a *different colour* from Legacy's `#DB0011`, deliberately (salience-ramp re-seat, R-D11).

**Consequence — this is the root of the "too loose" state.** Any Legacy red resolving in an **Apollo Mono**
surface is **drift**, not a pending choice. The bare `rag/error` red, `tabs/active`, `progress/complete`, and
any `primary/*` red bound by a Mono component must be re-homed to the Mono value (or to a Legacy override the
Mono theme does not select). Enforcement is the theme-provenance gate (below) + **ADR-0011** (four-theme
override sets), which is what makes "red = Legacy" mechanically true rather than a manual chase.

**Backlog opened (each needs its Mono value ruled before its Legacy red can be gate-seeded):** `tabs/active`
(Mono = ink indicator, not red — unruled), `progress/complete` (Mono = ink/green — unruled), bare `rag/error`
Mono red = `#B92F1E` (ready, but the bare-role rebind waits with error/warning/info per R-D17). Tracked in
`knowledge/_STYLE-PROVENANCE.md`.

Edges: bounds(R-D15) · relates(R-D7)

## R-D18 — Success GREEN set completed; teal fully evicted from Mono (2026-07-20). Source: Dave, on the live tuner.
Ruled the open green slots on `reviews/RAG-SUCCESS-GREEN-2026-07-20-v1.html` (OKLCh sliders + live contrast +
salience guard). Settled:
- **`rag/success-glyph`** (on-page indicator): light `#2B7E4F` (5.0:1 on white), **dark `#4A9568`** (4.8:1 on
  `#1A1A1A`) — the previously-MISSING dark slot, now filled (ADR-0010 pilot realised).
- **`rag/success-tint`** (message bg): light `#DCEDE3`, dark `#12291D` — re-hued off the Legacy teal
  (`#E5F2F2`/`#001615`); labels 14.31:1 / 14.79:1.
- **`rag/success`** bare role: rebased off `color/green/600` (teal) → tracks `rag/success-glyph` (values
  `#2B7E4F`/`#4A9568`). `rag/success-background` unchanged (R-D14 `#5DAC7B`/`#43AD6F`).

**Salience:** green leads info-blue on dark (4.8 > 3.82 ✓); on light it's effectively tied (green 5.0 vs blue
5.03) — Dave saw the guard flag it and **held** (a 0.03 hair, not worth darkening the green).

**Effect:** the seven components that bound the bare teal role (Button already done + Account-card, Confirmation,
Input-fields, List-items, Notifications, Reorder, Status-indicator) now resolve green; their snippet hexes were
swept to match. **Leakage gate: 0 waived, 0 leaks.** Teal `#00847F` no longer resolves in any Mono surface.
Bare `rag/error`/`warning`/`information` roles remain Legacy-drifted (see R-D17) — their own future rulings.

Edges: refines(R-D17) · relates(ADR-0010)

## R-D17 — The bare `rag/*` roles are Legacy-drifted; teal leak gated (2026-07-20). Source: Dave.
**Finding.** The bare RAG *role* tokens all still resolve to **Legacy** values, while the R-D14 palette
lives only in the `-background`/`-glyph` tokens: `rag/success` → `color/green/600` = **`#00847F` teal**;
`rag/error` = `#A8000B`/`#DB0011`; `rag/warning` = `#FFBB33`; `rag/information` = navy. So any Mono component
binding a bare role renders a Legacy colour. This is how the Mono "Done" button showed teal (→ B-D6).

**Ruled now (success only).** Mono success = R-D14 green (B-D6). The teal is **Legacy's alone** (R-D15).

**Gate (Dave: "how do we stop this leakage").** New build-blocking **`_validate_legacy_leak.py`**: every
reference-snippet manifest binding is resolved in both modes; any hex in `LEGACY_ONLY_HEXES` (seeded with the
ruled teal `#00847F`) is a leak. It immediately caught **7** teal-binding surfaces — two we hadn't enumerated
(**Reorder**, **Status-indicator**) plus Account-card, Confirmation, Input-fields, List-items, Notifications.
Button is FIXED (green); the other seven are **WAIVED with provenance** because a clean rebind needs the
R-D14 green **completed** — see debt below. Registry grows as each Legacy colour is ruled (error/warning/info
not yet ruled → not seeded).

**DEBT — R-D14 green set is INCOMPLETE (blocks the source-fix of the 7).** `rag/success-glyph` has **no dark
value** (light `#2B7E4F` only); `rag/success-tint` dark is still teal `#001615`; the bare `rag/success` role
still teal. To rebind on-page success *indicators* (which need the darker glyph-strength green to pass 3:1 on
white) we need Dave to rule the **dark glyph-green + tint greens**. Until then the 7 stay waived. `-background`
(`#5DAC7B`/`#43AD6F`) is complete both modes — that's why the button (a fill) could be fixed cleanly.

**Flexibility (Dave, 2026-07-20).** Tokens must stay flexible — a future RAG may set **light ≠ dark**
independently (not just shades). `text/on-success` was minted per-mode for exactly this. See the
placeholder-slots / style-builder direction in `_FUTURE-STATE.md`.

Edges: refines(R-D15) · verified-by(knowledge/_validate_legacy_leak.py) · relates(B-D6)

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

Edges: refines(R-D1)

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
- ~~Green + blue matting rungs~~ — **RULED, see R-D4.**
- Dark-mode green `#1AA05C` (3.37 white) — unfixed.
- Dark-mode red `#CC4333` (3.97) / blue `#2674DC` (4.15) as GLYPHS on `#111` — pass 1.4.11 for
  icons, **fail 4.5 for text**.
- The `dv-017` RAG-cell contradiction above.
- Build the amber gate.

Edges: refines(R-D2) · conflicts-with(dv-017, resolution=ruled, ref=R-D5)

---

## R-D4 — Matting rungs RULED + first token promotion (2026-07-18)

### The rungs — RULED
Source: Dave's second markup of `reviews/RAG-MATTING-2026-07-18.html` (3 pins) **plus a direct
readback** — the pins named the hue but not the step (every row shares `td.ask`; the R-D2 ⛔ OPEN
predicted exactly this), so the rung came from an explicit in-chat pick, not inference:

| hue | pick | value | note |
|---|---|---|---|
| **green** | **matted 15%** | **`#2B7E4F`** | L 0.530 · C 0.109 · H 154.9° · white 5.00 |
| **blue** | **matted 15%** | **`#306EC6`** | L 0.544 · C 0.151 · H 257.8° · white 5.03 |
| **red** | **as-is** | `#B92F1E` (R-D1) | Dave: leave; no matting pass on red |
| **amber** | — | absorbed by **R-D3** | pin "this for glyphs, not backgrounds" = the R-D2/R-D3 split, already ruled |

**Q1 resolved implicitly: one matting level (15%) across green + blue.** Q3 resolved: red as-is.
Q0/Q2 were overtaken by R-D3 (the AMBER-MATRIX sheet — `reviews/AMBER-MATRIX-2026-07-18.html` —
is where the amber background was re-cut; Dave's "there was definitely work done on this" verified
against that sheet and R-D3).

### First token promotion — ENACTED (additive)
`tokens/semantic-colour.json` gains the R-D2 role pairs as NEW flat keys under `rag/`
(`<hue>-background` + `<hue>-glyph`), values per R-D1/R-D3/R-D4. **Incumbent keys
(`error`/`warning`/`success`/`information` + tints) are UNTOUCHED — they are the future legacy
theme (R-D1 pin 12). No component rebinds yet** — that waits for the blast-radius gate, so this
promotion is zero-visual-change by construction.
**Dark-mode is promoted only where ruled:** red `#CC4333` (R-D1) · amber pair mode-stable (R-D3) ·
blue dark `#2674DC` (passes 4.55 for white text; glyph-as-text on `#111` 4.15 stays OPEN) ·
**green is promoted LIGHT-ONLY** — the first enactment attempt carried the incumbent dark
`#1AA05C` with an OPEN flag and **the contrast gate refused it** (3.37 vs 4.5): a known-failing
value behind a prose flag is exactly the pattern the gates exist to stop. The dark leaf lands with
the dark-green ruling. **No unruled value was invented.**
**Gate model extended, not weakened:** the promotion also added `RULED_PAIR_EXCLUSIONS` to
`_contrast_utils.py` — white `rag/text` × `rag/warning-background` is a pairing R-D3 rule 1
forbids outright, so the audit no longer tests a state that cannot occur (reason string carries
the ledger ref). Note the promotion made the fills VISIBLE to the surface-resolver for the first
time (incumbent keys never name-matched "background") — the gate seeing amber and dark-green at
all is new coverage, and it bit correctly both times.

### Still open after R-D4
Dark-mode green fix · dark-mode red/blue text-glyph lift · ~~the `dv-017` contradiction~~ (**RULED R-D5**) ·
the amber gate (rules 1+2) · component rebinding to the new role tokens (AFTER the blast-radius gate).

Edges: refines(R-D2) · verified-by(contrast-gate)

---

## R-D5 — the `dv-017`(a) contradiction, RESOLVED (2026-07-19)

**Dave, on `reviews/DV017-DELTA-VS-RAG-2026-07-19-v1`: *"good for me."*** The rule listed "RAG-style cells"
among the red/green **delta indicators**, but RAG includes amber and R-D3 rule 2 bars amber as a directional
colour — a palette the rule both permitted and excluded.

**RULED — split the clause (wording only, no values change):**
- **Directional deltas** (gain/loss) are **red/green ONLY** — amber has no direction.
- **RAG status** (health / watch / within-tolerance) is a **SEPARATE concern**, governed by R-D3 (red/amber/green
  backgrounds, black text where ruled). Its **component manifestation is specified separately** — NOT by the delta clause.

Enacted in `knowledge/guidelines/data-visualisation.md` `{#dv-017}`(a); rules-index regenerates on build.

⚠️ **This is wording only.** The *actual* RAG manifestation (cell / pill / dot+label / bar) and the dark-mode
opens (green has no ruled dark value; dark red/blue fail 4.5 as glyph-on-text) are **NOT settled here** — they
are the dedicated **RAG-colours review**, which Dave ruled the next deliverable (2026-07-19: *"lets do this next"*).
Home: `_FUTURE-STATE`. This was the source of Dave's earlier confusion (the status-cell example ≠ real manifestation).

Edges: bounds(dv-017)

---

## R-D6 — glyph contrast by role + halation as a third axis (2026-07-19)

Source: Dave's markup of `reviews/RAG-COLOURS-2026-07-19-v1.REVIEW.html` (4 pins) + in-chat confirmations
("correct" / "also correct"). Two rulings RULED; a model direction and two hypotheses OPEN.

### Ruling A — glyph contrast is RELATIVE to whether the glyph carries the meaning — RULED (R-D6.A)
Dave (pin 3, on the M3 dot+label): *"when paired with a label the contrast is less important so the brighter
yellow is fine here. It's only when the glyphs have meaning and the label is a number or the label doesn't
carry the meaning that it matters, like arrows for instance."*

> **THE RULE:** When a status glyph is **paired with a text label that carries the meaning**, the glyph's
> colour is reinforcement — it need only meet the **3:1 non-text** floor (1.4.11), and a brighter/less-
> contrasty hue is acceptable (use-of-colour 1.4.1 is satisfied by the label). When the **glyph itself
> carries the meaning** — arrows = direction, colour is the sole status signal, or the label is a bare
> number/value that does not encode status — the glyph must meet **4.5 text** (1.4.3).

Refines R-D3 "belt & braces" and `{#icon-013}`. **Gate-able:** the check is "does a text sibling carry the
status word?" — flag lone/meaning-carrying coloured glyphs below 4.5. Not yet built.

Edges: refines(R-D3) · refines(icon-013)

### Ruling A′ — sharpened: in THIS system no status glyph ever carries meaning by colour alone (2026-07-21). Source: Dave. (R-D6.A2)
Dave, reflecting on the amber `#C58900` passing at 3:1: *"the only coloured icons are the statuses, and the
warning roundel has a black exclamation mark — even in this case there is enough contrast. So the only glyphs
that need to conform to the contrast rule are ones where the meaning is carried exclusively by the glyph, like
an arrow and a figure."* Reflected back and confirmed firm.

> **THE SHARPENING.** The **only** coloured glyphs in Apollo are the **RAG statuses**, and every one is either
> (a) sat beside a **meaning-carrying label**, or (b) drawn as a **black mark on the coloured fill** (the
> warning roundel's `!` — black on `#F0B13A` = **11.06:1**, ample). Neither ever makes **colour** the sole
> carrier of meaning. Therefore **no status glyph is held to 4.5** — the 3:1 non-text floor governs the coloured
> roundel/dot, and the internal mark passes on its own (black-on-amber, white-on-dark). The 4.5 text rule's
> **entire live domain** is the **meaning-exclusive glyph**: an arrow whose direction *is* the datum, or a
> coloured mark whose only sibling is a bare number/value (dataviz deltas). **Guard kept in the wording:** this
> holds *because* a status ships with a label **or** a passing black/white mark — a bare coloured dot with
> neither would fail use-of-colour (1.4.1) independent of contrast. So the operative test is "labelled **or**
> contrast-passing mark," which every status already satisfies.

**Resolves the standing tension** between `{#icon-011}` ("icons 4.5 in all instances, labelled or not") and this
ruling: `{#icon-011}` reads stark, but its **real live scope** is the meaning-exclusive glyph — coloured icons
= statuses = always labelled or black/white-marked, so they answer to the 3:1 indicator floor per the roundel
policy (`{#icon-015}` "icons 4.5 · pictograms 3 · chart/RAG indicators 3"). Also subsumes the **R-D3 amber
roundel-leg exemption** (2026-07-02): the `#F0B13A`-on-white 1.9:1 "failure" was never a real fail because the
colour is not the channel — this ruling states the principle the exemption was reaching for. Scope note added to
`{#icon-011}`; reconciliation logged.

Edges: refines(R-D6.A) · bounds(icon-011) · subsumes(icon-015, claim=amber roundel-leg exemption 2026-07-02)

### Ruling B — halation is a THIRD design axis, beyond hue and intensity — RULED
Dave: bloom/shimmer is real and *"another dimension to this"*; *"thin lines and colour dance, thicker ones
bloom… that's the halation effect."* Confirmed as evidence for Band A / a saturation ceiling.

Two failure modes, and the levers were ALREADY in canon (`color/black` `$note`: "reduce the extremity of the
edge — the neutral-ground lever [luminance step] · its coloured-ground twin is the saturation ceiling ≤0.72"):
- **BLOOM** (irradiation) — bright feature spills across its edge; light-on-dark reads HEAVIER
  (`web-foundations` light-bleed compensation; `common-toolkit-foundations` "icon strokes appear heavier").
  Grows with bright-side luminance × step; **visible on thick fields.** Lever: lower the luminance step.
- **DANCE** (chromatic edge instability) — saturated colour at a **thin/high-spatial-frequency** edge, worst
  when luminance contrast is low. The chromatic channel is low-pass (~4 c/deg). Lever: saturation ceiling.

> **THE NEW DIMENSION — spatial frequency / stroke width.** WCAG's flat 4.5 ignores it; APCA only approximates
> it via size/weight tables. **Thickness (in degrees of visual angle) selects which mode you get** — thin →
> dance, thick → bloom. First-cut model: `reviews/_rag_bloom_model.py` (bloom & dance indices, 0..100,
> grounded in CSF + chromatic aberration; v0 heuristic). Sanity: white-fill = bloom 100, sat-blue-1px-text =
> dance 100, and dance collapses when the same blue is a thick fill — matches the observation.

**CALIBRATION INSTRUMENT — Dave's astigmatism.** Astigmatism smears edges directionally → heightened
sensitivity to bloom/dance → a stricter test. *"This is where my astigmatism is actually a benefit."*
Thresholds come from what the **most sensitive** observer can still see sit still → an accessibility
gold-standard, consistent with the accessibility aspiration (ADR-0004) and the dataviz delta astigmatism rule.
This is the **Apollo Labs** engine ([[_FUTURE-STATE]] spin-out).

### OPEN (leans, pending v2 markup + Dave's eye — NOT ruled)
1. **Sat-capped Band B.** Chroma → 0.72× drops dance ~28% (red 98→71, blue 97→70, green 72→51) at ~zero
   contrast cost (black-on-fill 5.75→5.89). Built into v2 for Dave to eyeball.
2. **Step-DOWN-on-colour hypothesis** (Dave: "the font step-up in dark mode maybe doesn't apply for text on
   colour"). Model: **supported for BLACK text on LIGHT fills** (bloom 2–7 vs 29 on the page → step-down
   unneeded) but **marginal for WHITE text on DARK Band-A fills** (bloom ~25 → may still apply). Depends on
   the luminance step, so it tracks the band. → a TYPE ruling once the band lands; home `_TYPE-DECISIONS`.
3. **Band choice** (A white-text fills / B black-text fills / sat-capped B) and **§1 manifestation** — still
   Dave's call on v2.

---

## R-D7 — red carve-out LOCKED + the weight-polarity finding (2026-07-19)

Source: Dave's markup of `reviews/RAG-COLOURS-2026-07-19-v3` (red ladder + weight matrix) and `-v4`.

### Red — RULED (locked)
Dave, on the deep-red ladder: *"they are all blooming but this is the best balance of the right colour and
white text"* → **red = `#B92F1E`, white text, MODE-STABLE (one value, light + dark).** This is already the
light-mode ruled red (R-D1), so light and dark red unify. **Red carves out of the isoluminant set** — a
second carve-out beside amber, for a DIFFERENT reason: amber = lightness/contrast; **red = perceptual
instability** (long-wavelength → worst chromatic aberration; astigmatism sees it first — *"in my experience
red is an issue"*). The lever for red is **depth, not desaturation**: deeper red RAISES white-text contrast
AND lowers bloom together (desaturation, the v2 B′ cap, cost readability — Dave: "calmer but less readable").
⇒ **The "balanced dark set" is really green+blue matched (isoluminant); red and amber each carve out.**

### Weight polarity — FINDING (lean, pending Dave's glasses/no-glasses look)
Dave picked **400 Regular** on the dark page / red and **500 Medium** on amber — *"weird"*. It is not weird,
it is **polarity**: the BRIGHT side blooms into the DARK side.
- **Light text on a bright/dark ground** (page, red) → stroke FATTENS → step **DOWN** (400).
- **Dark text on a light fill** (amber, green, blue) → fill blooms inward, THINS the text → step **UP** (500).
Consistent across all grounds (model: bloom 400→500 climbs on every ground; direction = sign of fg−bg
luminance). Lands as a **TYPE ruling** paired with R-D6 once Dave confirms after the glasses test. My bloom
index measured magnitude; **added a polarity term** (who-thins-whom). Sheet: `-v4`, §W2/§W3.

### OPEN
- Confirm the weight-polarity rule (or uniform 500) — needs Dave's astigmatic vs corrected look + the
  mixed-vs-uniform panel (v4 §W3). **Dual-observer tension:** mixed may help astigmatism but read "weird" to
  normally-sighted → the calibration principle (serve the sensitive without breaking the typical).
- Green/blue band (A / B / B′, v2) and §1 manifestation — still Dave's call.
- The missing ~450 rung (see _FUTURE-STATE) — licensed cut has no weight between 400 and 500.

### Weight — RESOLVED (2026-07-19, after the v4 side-by-side + glasses look)
Dave: *"I think medium is best on balance."* ⇒ **RAG status text = uniform Medium (500), both grounds, both
modes.** The polarity finding (down on bright ground, up on light fill) is REAL and retained as the WHY, but
the SHIPPED rule is **one weight, not a split** — chosen "on balance": simpler, and it resolves the
dual-observer tension (a mixed split could read "weird for normally sighted"; uniform 500 serves both). So the
dual-observer principle lands as **uniform**, with polarity kept as rationale, not a token. → mirror as a
TYPE ruling (T-D) when the RAG tokens are enacted. *(If Dave meant keep the 400/500 split, correct here — read
as uniform 500.)*

Edges: supersedes(R-D1, scope=fill role, claim=dark red #CC4333 as the status-fill red) · refines(R-D6.B)

---

## R-D8 — green/blue = Band A; the dark set closes (2026-07-19)

Dave, on the consistency argument (all fills white-text except amber, red prominent): *"that's actually okay
considering that red is a warning."* ⇒ **Green + blue take Band A (isoluminant, white text on darker fills).**
Red's distinct prominence (deep, white text, unmissable) is APPROPRIATE to its warning role, not an inconsistency.

**THE DARK SET — now complete (pending §1 manifestation):**
| hue | dark fill | text | notes |
|---|---|---|---|
| red | `#B92F1E` | white | mode-stable, carve-out (R-D7) |
| amber | `#F0B13A` bg / `#C58900` glyph | black | carve-out (R-D3) |
| green | **`#14874E`** | white | Band A, L≈0.55 — **closes the dark-green NULL** (open since R-D1) |
| blue | **`#1F6ED5`** | white | Band A, L≈0.55 |

- **All fills white text except amber.** Green+blue are the matched stable pair (R-D8), red carves out but sits
  near their L, amber is the lone black-text hue. Consistent with [[colour-stability-red-yellow-problem]].
- **Marks/glyphs on dark:** icon (≥3:1) or label-paired — never bare coloured text (R-D6 Band-A rule).
- **Weight:** uniform Medium 500 (R-D7 resolution).
- **CLOSES:** dark-green null · dark red/blue glyph-as-text (→ R-D6 usage rule) · band choice · weight.
- **STILL OPEN:** §1 manifestation (cell / pill / dot+label / bar). Then enact token promotion (green dark
  `#14874E`, blue dark `#1F6ED5`, red mode-stable) behind the blast-radius gate.

*(Values from the v2 isoluminant sweep, Band A L≈0.55: green #14874E white 4.56, blue #1F6ED5 white 4.94. If
Dave wants green/blue nudged to red's exact L for a fully even trio, that's a re-cut — not requested.)*

Edges: refines(R-D1)

---

## R-D9 — RAG is a salience RAMP, not isoluminant (2026-07-19)

Dave: *"so it's not isoluminance for this, it's actually a ramp."* ⇒ **Status colour is a SALIENCE RAMP —
loudness descends with severity: red › amber › green › blue.** Isoluminance was the wrong target: it's for
CATEGORICAL data (no category should dominate — the dataviz series rule). Status has a HIERARCHY, so intensity
must TRACK it. See [[colour-salience-ramp-vs-isoluminant]].

**Why this emerged:** the v7 isoluminant set left green (salience 30.3) sitting BELOW blue (31.0) — Dave felt
green was recessive and blue over-loud. Reframing to a ramp fixed it: lift green above blue, drop blue to calm.

**Salience metric** = mean OKLab distance of (fill, text) from the page. Resolved ramp (pending Dave's final
green/blue pin on v8):
| severity | value | text | salience |
|---|---|---|---|
| breach | `#B92F1E` | white | 56.6 shout |
| watch | `#F0B13A` | black | 40.9 shout |
| healthy | `#36A467` | black | 33.1 present |
| info | `#527EBE` | black | 30.3 calm |

Big step warnings→states (the loud break = "warning vs not"), gentle step healthy→info. Red+amber are the
carve-outs topping the ramp; green lifted (was too recessive), blue calmed via **lower chroma** (also fixes
Dave's astigmatic legibility — a saturated blue edge is what blurs). Supersedes v7's flat green/blue.

### OPEN
- Final green (#36A467 / lighter) + blue (#527EBE / calmest #5D7FB0) pin — v8 eyeball.
- Red-vs-page 2.89 flag (keep deep, steer keep).
- §1 manifestation. Then token promotion.

Edges: supersedes(R-D8, claim=isoluminant framing for status)

---

## R-D10 — RAG dark set LOCKED (2026-07-19)

Blue nailed to the readable-calm point + green re-seated to hold the ramp (Dave: "let's get blue nailed,
refocus to components"). Final mode-stable set, all AA, monotonic salience ramp:

| severity | value | text | text-contrast | vs page | salience |
|---|---|---|---|---|---|
| breach | `#B92F1E` | white | 6.02 | 2.89 | 56.6 |
| watch | `#F0B13A` bg / `#C58900` glyph | black | 11.06 | 9.16 | 40.9 |
| healthy | `#43AD6F` | black | 7.45 | 6.17 | 34.5 |
| info | `#5F92B9` (cyan-shifted, astigmatism-readable) | black | 6.30 | 5.22 | 32.4 |

- **Red-vs-page 2.89 flag — RESOLVED: keep deep.** White text (6.02) carries the signal; the deep red is the
  low-bloom, mode-stable value Dave chose. The subtle cell-boundary is acceptable (arguably desirable — calm).
- Weight uniform Medium 500. Marks icon/label-paired. Red alone in white; green/blue/amber black text.
- **Blue = cyan-shift `#5F92B9`** (hue ~242°): moved off the short-wavelength blue that astigmatism blurs
  worst; black text 6.30; stays recognisably info-blue; sits below green (ramp holds).
- **Green re-seated to `#43AD6F`** (sal 34.5) so healthy stays clearly above info.
- SUPERSEDES the v2 Band-A green/blue and the v7/v8 intermediate values. Full arc:
  `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md`.

### Enactment (deferred — next session, Sonnet-appropriate)
Promote `#B92F1E` / `#43AD6F` / `#5F92B9` to `tokens/semantic-colour.json` rag/* (mode-stable), rebind behind
the blast-radius gate. **STILL OPEN: §1 manifestation** (cell / pill / dot+label / bar) — reframed as a
COMPONENT/pattern task, not a colour one.

Edges: supersedes(R-D8, claim=Band-A green/blue values) · refines(R-D9)

---

## R-D11 — CORRECTION: status FILLS are not mode-stable; the salience ramp is GROUND-RELATIVE (2026-07-19)

Dave's screenshot of the Form-B filled cells on the LIGHT page exposed it: the R-D10 set was tuned entirely
against the dark page (#1A1A1A), and **on white the ramp INVERTS**.

Measured on WHITE:
| sev | fill | text | fill-vs-white | note |
|---|---|---|---|---|
| breach | `#B92F1E` | white | 6.02 | but now the QUIETEST cell — the alarm recedes |
| watch | `#F0B13A` | black | 1.90 | fill barely separates from the page |
| healthy | `#43AD6F` | black | 2.82 | washed out (<3) |
| info | `#5F92B9` | black | 3.33 | weak boundary; cyan-desat blue looks pale on white |

**Salience order flips by ground:** on DARK breach›watch›healthy›info (correct); on WHITE
info›healthy›watch›breach (backwards — the alarm is quietest, info loudest). So Dave's "red and green aren't
working, blue especially" = the light fills wash out and the deep-red alarm no longer shouts.

**THE CORRECTION:** **R-D8/R-D10's "mode-stable fills" claim is WRONG for the FILL role.** Salience =
contrast-with-ground, which inverts between light and dark, so a fill ramp tuned for one ground cannot hold on
the other. **Status FILLS need PER-MODE values** (light-mode fills must be darker/more saturated to hold their
boundary against white AND to order the ramp correctly). The **dot+label (glyph-on-page)** form may still be
near-mode-stable — its salience is the glyph vs page, a smaller object — but the FILLS are not.

**PARKED (both tired, late 2026-07-19):** derive the LIGHT-mode fill set next session (ground-aware ramp:
tune red/amber/green/blue as fills on WHITE so breach shouts and none wash out), then reconcile the two modes.
The DARK set (R-D10) stands for dark; light needs its own pass. Colours for the dark page are DONE; the
light-page fills are the reopened piece.

### Component-build notes carried out of this session (for the Sonnet build)
- **Filled status cells/tags need more VERTICAL padding** (Dave, 2026-07-19, on the Form-B cells — they read too
  tight top/bottom). Bump the cell/tag vertical padding when speccing the filled-cell + Status components.
- Rebind Status-indicator (dot+label) to R-D10 dark tokens; the filled-cell + bar forms await the §1 canon pick.
- Light-mode fill set is OPEN (R-D11 ground-relative correction).

Edges: supersedes(R-D10, scope=fill role; dark values stay ruled, claim=fills are mode-stable)

---

## R-D12 — light-fills direction: NO LINES + black-text states (2026-07-19)

Source: Dave's 3 review edits on `reviews/RAG-LIGHT-FILLS-2026-07-19-v1` (the light-fills derivation).

### Ruling A — NO borders/lines on the fills — RULED (aesthetic) (R-D12.A)
Dave, on the mode-continuity option: *"nope, cant have lines its not part of the aesthetic."* ⇒ **Filled status
cells carry NO stroke/border.** This **kills Option B** (the mode-continuity/border approach) outright, AND
removes the amber hairline border that Option 0 leaned on. The boundary must come from the FILL alone.
**Consequence:** amber's identity is lightness, so with no border it cannot reach fill-vs-white ≥3 while staying
amber (deepening only reaches 2.52 at L0.72 before it goes ochre/brown, R-D3-barred). So on white the watch fill
is soft and leans on its black label (11:1). **This is NOT a new problem or a call — R-D6 Ruling A already
governs it:** *"when paired with a label the contrast is less important."* Meaning is in the label (icon-013), so
the fill is reinforcement, not the signal. ⚠️ **I initially over-raised this as an open question in v2; Dave
corrected — *"amber is fine, it has a label that carries the meaning… we've ruled on this already."*** The wider
point: a status cell is a **labelled component**, so fill-vs-page contrast is a **salience/scan lever, not an
accessibility floor** (the floor is the LABEL's contrast). Stale-reading catch — should have CONSULTed R-D6
before flagging. Amber stays `#F0B13A` black text, no line: settled.

Edges: refines(R-D11) · verified-by(R-D6.A)

### Ruling B — black text on green + blue in light mode — RULED (R-D12.B)
Dave: *"no must be black text on colour for the blue and green this reinforces the salience."* ⇒ **In light mode
the state fills (green, blue) carry BLACK text, matching amber; only breach/red carries white.** The polarity
(loud/white breach vs calm/black states) reinforces the salience ramp. **Consequence:** black text needs the
fill light enough (blk/fill ≥4.5) while the fill still separates from white (≥3) — a narrow window. The R-D4
values are too dark for black text (green #2B7E4F blk 4.20, blue #306EC6 blk 4.17, both < AA), so green/blue
re-seat slightly lighter: **green ≈ `#429363`** (blk 5.59, white 3.76) holds cleanly. So Option 0's "restore
R-D4 values" is superseded — the HUES stay but the lightness is tuned for black-text-on-white.

Edges: supersedes(R-D4, claim=green/blue rung values for light fills)

### OPEN → v2 eyeball (`RAG-LIGHT-FILLS-2026-07-19-v2`)
- **Blue — CONFIRMED `#7D8CC2`** (purple-lean, lightened). Dave on v3: *"this one"* on the highlighted pick.
  H272, L0.65; black label 6.40, fill/white 3.28. The "lighter is fine" only holds because fill contrast is
  salience not a floor (the reframe) — the label carries meaning.
- **Green — POPPED, then desaturated; blue nudged toward true blue.** v3→v5 arc: green *"pop a bit more, go a bit
  lighter"* → `#439A67`; then *"this with less saturation"* → **`#57966E`** (L0.62 C0.090, fill/white 3.50). Blue
  *"move a tad to the blue, lighten a wee bit"* → **`#7A91C7`** (H266 from 272, L0.66; fill/white 3.13). **Constraint
  surfaced (first of its kind):** green must stay ABOVE blue in salience or the ramp order healthy›info ties — so
  green's pop is bounded by blue, not by contrast or the label floor. Green desaturation is *free* on the ramp
  (luminance-driven), so calming green doesn't cost its lead.
- **★ LIVE TUNER built (v6→v7).** Dave: *"give me a saturation slider, make it wide so i can fine tune."* In-browser
  OKLCh tuner — wide saturation + fine lightness sliders for green & blue (hue held), live hex + fill/ground +
  black-label floor + a ramp-order guard that reds if green ≤ blue. Red/amber locked. Reusable pattern → Apollo
  Labs / Layer-2 in-browser controls ([[dataviz-pillar-progress]], [[vision-contextual-dashboard]]).

---

## R-D13 — LIGHT fills locked; DARK reopened to match (2026-07-19)

- **LIGHT fills LOCKED off the tuner** (Dave gave the hex): **green `#6AB887`** (L0.72 C0.106), **blue `#8DA9EB`**
  (L0.74 C0.101), both black text. Verified: labels 8.82 / 9.01 (≫ 4.5 floor); ramp green 2.38 > blue 2.33 on white
  (healthy›info holds). These are **notably paler than the R-D10 dark values** — a pastel light palette. Fine on
  white: fill contrast is the salience lever, meaning is in the label (R-D6). Watch stays soft (amber carve-out,
  ruled).
- **★ DARK reopened to MATCH.** Dave: *"we need to adjust on dark too."* The locked light palette is paler than the
  R-D10 dark green/blue (#43AD6F / #5F92B9), so dark needs re-tuning for family coherence. Built a **two-mode
  tuner** (`RAG-LIGHT-FILLS-2026-07-19-v7`): a second panel on its own #1A1A1A ground with its own ramp guard
  (green must lead blue on dark = fill-vs-darkpage). Red + amber remain mode-stable; green + blue are per-mode
  (the R-D11 thesis, now fully realised — **four green/blue values, two per hue per mode**). **DARK green/blue
  pins PENDING** (Dave to lock off the v7 dark tuner). Reconciliation into the token table waits on the dark lock.
- **Reconciled table (light locked; dark pending):**

| severity | light fill | dark fill | text | mode |
|---|---|---|---|---|
| breach | `#B92F1E` | `#B92F1E` | white | mode-stable |
| watch | `#F0B13A` (glyph `#C58900`) | `#F0B13A` | black | mode-stable |
| healthy | **`#6AB887`** | *pending v7 dark pin* (R-D10 `#43AD6F`) | black | per-mode |
| info | **`#8DA9EB`** | *pending v7 dark pin* (R-D10 `#5F92B9`) | black | per-mode |

- Closes the **R-D11 light-fill open** (light half done). Dark-match is the last open before token promotion.

Edges: refines(R-D12.B)

---

## R-D14 — RAG light fills LOCKED; full set reconciled (2026-07-19)

- **Blue un-purpled.** Dave: *"I want the blue on white to have the same hue, I've changed my mind from the slight
  purple."* Light blue hue H266→**H241** (matches dark blue; drops the purple lean).
- **LIGHT set LOCKED — Option C** (Dave: *"c is the one, lets lock it"*, off `RAG-LIGHT-FILLS-2026-07-19-v8`):
  **green `#5DAC7B`** (L0.68 C0.108 H155), **blue `#7DABCD`** (L0.72 C0.070 H241). Green leads blue on white
  (fill/white 2.74 > 2.45) so healthy›info holds; labels 7.65 / 8.58 (≫ floor). Black text; no lines.
- **★ IMPOSSIBILITY PROVEN (not asserted).** Exhaustive pair search: **no single green/blue keeps green›blue on
  BOTH grounds** — "louder" = darker on white but lighter on dark, so green can't lead on both. ⇒ green/blue are
  **necessarily per-mode**. This is R-D11's thesis, now demonstrated. (Dave's mode-stable try #5EAE7C/#5898C6
  inverted on white — the evidence.)
- **DARK held at R-D10** (`#43AD6F` / `#5F92B9`): Option C's green came *down* to L0.68, landing close to dark's
  L0.67 (blues share the hue family), so the modes harmonise without re-cutting dark. *(Reconciliation call —
  pending Dave's ok; the v7 dark tuner stands if he wants dark moved.)*

### FINAL RECONCILED SET — ready for token promotion (Sonnet, behind the blast-radius gate)
| severity | token | LIGHT fill | DARK fill | text | mode |
|---|---|---|---|---|---|
| breach | `rag/breach` | `#B92F1E` | `#B92F1E` | white | mode-stable |
| watch | `rag/watch` (+ glyph `#C58900`) | `#F0B13A` | `#F0B13A` | black | mode-stable |
| healthy | `rag/healthy` | **`#5DAC7B`** | `#43AD6F` | black | per-mode |
| info | `rag/info` | **`#7DABCD`** | `#5F92B9` | black | per-mode |

No lines (R-D12 A). Fill contrast = salience lever, meaning in the label (R-D6); amber soft on white is ruled fine.
**Next:** promote to `tokens/semantic-colour.json` rag/* + rebind behind the blast-radius gate (deferred to a
Sonnet session). Closes R-D11 entirely.
- Green value `#429363` confirm (black text, label contrast 5.6).
- ~~Amber accept?~~ **NOT open — R-D6 governs (label carries meaning); over-raised, Dave corrected.**

Edges: supersedes(R-D13, claim=light green/blue values (#6AB887/#8DA9EB → #5DAC7B/#7DABCD)) · refines(R-D11) · verified-by(reviews/_rag_light_fills_calc.py)

---

## R-D15 — RAG promoted + the FOUR-THEME architecture (2026-07-19)

Source: Dave. The four-theme architecture was already captured in agent memory (`four-theme-architecture`)
from a prior session but had **never been inscribed in this ledger** (a memory-only record — the anti-pattern;
ledger stopped at R-D14). This entry closes that gap AND folds in today's refinements (the Apollo Mono
"very mono" scope + the confirmed theme renames). Provenance: architecture = prior ruling; Mono-scope + rename
detail = 2026-07-19.

### The architecture — RULED (firm, Dave stated it definitively and named the themes)
> **ONE token store + ONE baseline component library, toggling between FOUR themes** (Dave, 2026-07-19:
> "yes one token store with 4 themes"). Components bind a **theme-agnostic semantic role** ("success"); the
> active theme's override set decides the hex. Nothing hardcodes a theme's colour. The four themes, in Dave's
> canonical order: **Apollo Legacy · Apollo Mono · Apollo Console (UI) · Apollo Supercharge (SC).**
> - **Apollo Legacy** is the ONLY theme carrying the **teals** (`rag/success` #00847F, `rag/error`
>   #A8000B, `rag/warning` #FFBB33, `rag/neutral` #767676, `rag/information`) **AND the HSBC brand grey scale
>   `color/grey/100–800`** (Dave, 2026-07-19: "color/grey/100–800 — this stays for Apollo Legacy"). They are
>   retained + tokenised for legacy interfaces — **not deleted** (confirms R-D1 pin 12; supersedes the vaguer
>   "future legacy theme" note). New supersedes Legacy over time; both coexist under the toggle.
> - **Apollo Mono's neutral scale is the new `color/mono/*` ramp** (added 2026-07-19), NOT `color/grey/*`.
>   **LOCKED — dual-end brightness curve, γ=1.7, 15 steps** (Dave dialled it on the tuner
>   `reviews/APOLLO-MONO-GREY-CURVE-2026-07-19-v2.html`): steps pack toward black AND white, thinning the
>   low-value mid-greys; black + white are endpoints; **pinned through `#1A1A1A` = `mono/4`**. **Keys are a
>   STABLE index 1–15** (Dave: "just do 1-15, they will be remapped as a theme") — so a future curve re-tune
>   won't break aliases; themes remap semantic roles onto these indices. Set: `mono/1` #000000 · `2` #050505 ·
>   `3` #0F0F0F · `4` #1A1A1A · `5` #313131 · `6` #484848 · `7` #626262 · `8` #808080 · `9` #9D9D9D · `10`
>   #B7B7B7 · `11` #CECECE · `12` #E1E1E1 · `13` #F0F0F0 · `14` #FAFAFA · `15` #FFFFFF (per-step brightness in
>   the token `$description`). In `tokens/colour.json` + canon; build green. (First cut 21 linear, then
>   brightness-keyed — both superseded.)
> - **Console / Supercharge / Mono use the NEW colours** for RAG (R-D14 green/amber/red/blue), never teal.
> - **★ The baseline we are building IS Apollo Mono — and Mono is "very mono": monochrome throughout
>   (near-black · greys→black per [[feedback-grey-tint-check]] · black), colour appears ONLY in RAG status
>   and data-vis** (Dave, 2026-07-19: *"we are mono… it is very mono for now, only rags and data vis hold
>   colour"*). This supersedes the earlier "baseline default = new colours" phrasing — the baseline is NOT
>   broadly colourful; new colour is confined to the two meaning-carrying channels. Console/Supercharge carry
>   the broader brand palette; that's the later colour pass.
> - End-state = full tokenised 4-theme toggle. **We build Mono now; the broader colour/theming BUILD is
>   PARKED** ("we'll deal with colours later"). RAG is the first coloured slice; it proves the Legacy-vs-new split.

Renames captured: Apollo UI → **Apollo Console**; SC = **Apollo Supercharge**; **Apollo Mono**; + **Apollo Legacy** (new).

### What was ENACTED this session (values only — no component rebind; that waits for the colour pass)
- **Fills promoted** to `tokens/semantic-colour.json` `*-background` + propagated to `canon/canon.css`
  (light `#5DAC7B`/`#7DABCD`, dark `#43AD6F`/`#5F92B9`, breach `#B92F1E` now mode-stable, watch `#F0B13A`).
  These are the **baseline/new** theme's RAG fills.
- **`rag/text` polarity** (white on breach, black on all states — `type26-013` + R-D12 B) enacted in the
  contrast audit via the **existing `RULED_PAIR_EXCLUSIONS`** mechanism: white RAG text on green/blue is a
  **forbidden pair** (mirrors the amber exclusion already there). Build green on contrast. **No new ruling —
  the model was already governed;** the review sheet I built to "decide" it re-litigated settled rulings and
  was binned (stale-reading catch — [[stale-reading-failure-mode]]; CONSULT was skipped, then run).
- Components **NOT rebound** — they render RAG as dots (glyphs, bind incumbents, R-D6 fine) + chips (tints).
  The `-background` fills have no consumers until the §1 manifestation (filled cell) is picked. Rebind =
  theme-resolution, folded into the parked colour pass.

### Grey-tints — STANDING CHECK (Dave, 2026-07-19)
> When we find a **grey tint / grey ink**, SURFACE it — Dave "will usually say make it black, but we check
> first." Never auto-swap. Flagged so far: `rag/text/on-light` **#333** (fails AA on the dark fills 4.48/3.79;
> #000 clears 7.45/6.30) · `rag/neutral` **#767676**. Coloured `-tint` washes are out of scope. See
> [[feedback-grey-tint-check]].

Edges: refines(R-D1) · supersedes(R-D1, claim=the vaguer 'future legacy theme' phrasing)

## R-D16 — Apollo Mono semantic greys seated on the `color/mono/*` ramp (2026-07-19)
Dave ruled on the review sheet `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1` (5 pins). The 79 semantic
greys were surfaced against the new ramp (grey-tint check — nothing auto-swapped). Rulings:

1. **Primary text ink → `mono/4` `#1A1A1A`** (the "make it black" option). Covers `text/default`,
   `icon/default`, `rag/text/on-light` (light values `#333` → `#1A1A1A`; dark stays white).
   **★ SUPERSEDES `col25-011`** ("typography = white or Grey-8 `#333` only") **for Apollo Mono** — Mono text
   ink is digital-black; **Grey-8 stays Legacy-only.** Also clears the grey-tint flag on `rag/text/on-light`.
2. **Secondary text → DROPPED.** Mono carries **no second text grey**; `text/secondary` collapses to the
   single ink (light `#1A1A1A`, dark `#FFFFFF`). Muted/caption hierarchy = **weight + size, not colour**
   ("very mono"). Visible change library-wide (muted text goes full-ink).
3. **UI grey `#767676` (Grey-6) → `mono/8` `#808080`.** Borders/pressed fills/scrollbar/`rag/neutral`.
   `#808080` = 3.9:1 on white — fine as border/UI (3:1), below AA-text; `rag/neutral` is label-paired (R-D6)
   so OK. Clears the grey-tint flag on `rag/neutral`.
4. **Tinted `#D7D8D6` → `mono/12` `#E1E1E1`.** It was non-neutral (faint green cast); now a pure step.
   Borders/dividers/disabled fills.
5. **Mechanical nearest-step maps → APPROVED** ("all good"): `#1D1D1D`/`#212121`→`mono/4`,
   `#EDEDED`/`#F3F3F3`→`mono/13`, `#707070`/`#696969`/`#6C6C6C`→`mono/7`, `#404040`/`#474747`→`mono/6`,
   `#9B9B9B`→`mono/9`, `#787878`→`mono/8`. Already-exact (`#000`/`#1A1A1A`/`#808080`/`#B7B7B7`/`#FFF`) unchanged.

**Status: ✅ ENACTED 2026-07-19** (see enactment notes below). Original plan: write the Mono grey values into
`tokens/semantic-colour.json`, sync the component declarations, regenerate `canon/canon.css`, re-gate, annotate
`col25-011`. Sheet + `gen_mono_grey_sheet.py` carry the full table + contrasts.

### Enactment notes (2026-07-19)
**Method changed — snippets are now STYLED BY the tokens, not hand-synced** (Dave's ruling mid-enactment: "the
snippets need to be styled by the tokens"). New generator **`knowledge/gen_snippet_tokens.py`** projects
`semantic-colour.json` into each snippet's `[data-theme]` blocks via the snippet's own `#token-manifest`, and
into `canon.css` `.cn-*` literal declarations. It is idempotent, self-verifying, respects `driftAllow`, and
FAILS LOUD on any unresolved token. `canon/gen_canon_tokens.py` (the existing, NOT-orphaned spine generator —
it lives in `canon/`) regenerates the token spine. Re-run both after any token change; `_validate_snippets.py`
then passes by construction. 86 token values re-based; 245 snippet values projected; build green 34/34.

**★ TWO a11y CARVE-OUTS the contrast gate forced (do NOT "correct" these back to nearest-step — they are the
fix, provenance here):**
1. **Dark borders/dividers → `mono/8 #808080`, NOT the nearest-step `mono/7 #626262`.** `mono/7` is 2.76:1 on
   the `#1A1A1A` ground → fails 1.4.11 (needs 3:1); `mono/8` = 4.39:1. Also matches rule 3 ("borders → mono/8").
   Tokens (dark): `border/subtle`, `divider/border/{break,section,subsection,subsectionInset}`, `table/border`,
   `tooltip/border`, `data-vis/border/on-dark/{baseline-2,gridline}`.
2. **Text-bearing pressed fills → `mono/7 #626262`, NOT rule-3's `mono/8 #808080`.** White label on `mono/8` =
   3.95:1 → fails 4.5:1; `mono/7` = 6.18:1. Matches the review sheet's "keep text uses darker" note. Tokens
   (light): `tertiary/background/pressed`, `secondary/background/pressed` (latter was a gate blind-spot — same
   white-label defect, fixed proactively).

**OPEN — 11 `#333333` (Grey-8) non-text residuals left in place (rule 1 covered only text/icon ink).** Need a
ruling: usually→`#1A1A1A` per the Mono pattern, but data-vis is separately governed. UI (5): `primary/border/hover`,
`secondary/background/hover`, `secondary/border/hover` (light); `tertiary/border/disabled`, `text/on-inverse`
(dark). data-vis (6): `data-vis/border/on-light/*` + `on-dark/baseline-2,gridline` (light). `text/on-inverse` is
a signed-off calibrated label — likely leave.

**WATCH — dark surface/ground flattening.** The ruled mechanical maps send `#1D1D1D`/`#212121` (tertiary bg,
tabs, table, tooltip, form hover, scrollbar) → `mono/4 #1A1A1A`, which is now also the page ground → those dark
surfaces/hover states merge with the ground (no elevation/state separation by fill). Faithful to the maps + the
digital-black ground, but likely unintended; the dark-surface flatness gate does NOT catch surface==ground (only
dark==#FFFFFF) — a gate blind-spot. Revert = one-line token edit + regenerate.

**RECONFIRMED 2026-07-21 (Dave, live controller `reviews/MONO-SECONDARY-INK-2026-07-21-v1.html`):** the
rule-2 `text/secondary` collapse was re-examined when the Phase-1 projector made it visible on
Progress-tracker (`--muted` → single ink). Ruling, verbatim from the sheet export: *"KEEP the R-D16
collapse — single ink #1A1A1A/#FFFFFF; de-emphasis stays weight+size. No token change. R-D16 stands
unamended."* Nothing changed in the store.

Edges: supersedes(col25-011, scope=mono) · verified-by(contrast-gate)

---

**★ #86 (2026-08-02, triage-bankruptcy — inscribed #87): the RAG status-treatment manifestation is
a STANDING GOVERNING RECORD (G17).** Close condition ratified by Dave via the review export
(`reviews/TRIAGE-BANKRUPTCY-2026-08-02-v1.html`, 19/19): **closes at Dave's canon pick — A, A+B,
or A+B+C** (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`, `_LIVE-STATE.md:387`). ⚠ Whether one
treatment is provisionally rendering live was UNVERIFIED at #86 (declared residual, not a claim).
Register: `knowledge/_GOVERNING-RECORDS.md` G17 · ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #86-D1.
