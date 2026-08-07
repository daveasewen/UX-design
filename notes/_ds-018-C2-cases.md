# ds-018 C2 — the three cases (#121, for Dave's ruling)

**Measured 2026-08-07** (`_validate_property_resolves.py`, live run this session): 114 failures / 87 files, but they are **three different defects**, not one:

| Family | Failures | What it actually is |
|---|---|---|
| `--alpha-*` | 104 | Values EXIST in canon (`canon.css:244–267`, minted #99). Snippets are standalone `<style>` files that can't reach them. **Reachability, not a missing value.** |
| `--mark` | 7 | Two-tone icon knockout colour. Declared locally in Tranche-6/9 (`--mark:var(--page)` on `.is-error/.is-ok`), used in 7 other proforma files' SVG symbols with NO declaration → silently renders at the SVG initial (black). **Missing canonical token.** |
| `--phys-size` | 3 | The control's physical px size feeding press-physics maths (`transform:scale(calc(1 ± var(--press-travel)/var(--phys-size)))`) in Alert / Empty-state / Popover. Alert's own comment proposes 24. **Missing component token.** |

Goal restated (Dave, #121): schema built on **mono as the base of all four themes** — flexible, robust, standards-adherent (W3C DTCG: define once, alias, distribute by build; never duplicate literals), reliable (no silent initial-value fallthrough).

---

## A — `--alpha-*` reachability (104 of 114)

**A1 · Generator-injected canon block (RECOMMENDED).** Build injects the canonical alpha ramp from `canon.css` into each snippet's `<style>` (the AUTO-MARKUP generator already owns injection — this is a 4th injection type, same machinery as dv-lockup). One source of truth, snippets stay standalone, a canon change propagates at next build. This is the DTCG "distribute by build" pattern.

**A2 · Use-site fallbacks** `var(--alpha-60, .6)`. Standards-legal, but writes the literal 104× — values drift from canon the first time the ramp changes. Violates single-source; rejected by the stated goal.

**A3 · Snippets link canon.css.** Kills the standalone property of reference files (they're specimens, meant to travel). Couples every snippet to the full canon cascade — heavier than the defect.

**⚠ scope flag, not conflated into this ruling:** ds-026 ruled alpha primitives STATE-CHANGES-ONLY. Some snippet uses look static (e.g. `opacity:var(--alpha-80)` on display text). That's a separate audit — queued, not smuggled into A.

## B — `--mark` (7)

**B1 · Mint as canonical semantic token (RECOMMENDED).** `--mark: var(--page)` in canon `:root` — knockout = page colour, the partner of `currentColor` in two-tone icons. Themes re-map it (console/SC dark get it free — this is exactly the theme-layer case from #108). Local state-class overrides (Tranche-6/9 pattern) remain the mechanism; they now override a defined default instead of conjuring an undeclared name.

**B2 · Use-site fallback** `var(--mark, var(--page))` everywhere. Works, but ~30 repetitions and `--mark` never enters the schema — it stays folklore. Fails "solid and reliable".

**⚠ your eye:** today the 7 undeclared files render the knockout BLACK (SVG initial). B1 changes visible output to page-colour knockouts. That's almost certainly the intent, but it's a visual change — specimen compare available on request.

## C — `--phys-size` (3)

**C1 · Component-scoped required token (RECOMMENDED).** Each press-physics component declares `--phys-size` at its own root with its measured control size (Alert: 24, per its own comment; Empty-state and Popover to be measured, not assumed). It's per-component data — the "component tokens" layer in every schema standard. C2 gate then enforces presence, so a new physics component without it refuses loudly.

**C2 · Global size ramp** (`--phys-size-sm/md/lg`). Invents a scale where three measured values exist. Flexible-looking, actually a conversion — "a count is not a measurement" applies to sizes too.

---

**After ruling:** enactment is mechanical (generator arm + 2 canon lines + 3 measured declarations) → Sonnet sub, replayed in-window; then promote C2 to `--strict` in `_build_all.py` and the build is 95/95 green.
