# Fixed / Flex charter — governing brand-true generation

*"A wide road with high curbs."* The rules that let generation be **creative where it matters** while it **respects the components and brand that exist**. Drafted 2026-06-30 from the SME-Payments fitness tests (sober → desktop → Swiss → portfolio).

---

## 1. The two dials

Every generated screen is the product of **two independent dials**, and confusing them is the root of the differing results:

| Dial | Governs | Today | Risk |
|---|---|---|---|
| **Canon** (vocabulary) | tokens + components — *what is retrieved* | gated (`_validate_compose`, snippet/meta/icon/a11y gates) | strong below the component line, **silent above it** |
| **Register** (temperature/voice) | concept, density, how hot the craft runs — *how it is composed* | **ungoverned** — buried in brief adjectives ("sober", "bold") | every run guesses; un-repeatable |

The four SME versions used the **same canon** at **opposite registers**. The sober↔portfolio gap was mostly the *register* dial — a word ("sober"), not the canon. **Make register an explicit, named input**, not an adjective.

---

## 2. Fixed — the curbs (always *retrieved*, never typed)

These are non-negotiable and must come from the knowledge graph at generation time. Recall is not allowed (recall drifts; retrieval can't).

- **Brand colour values** — the red and the core palette, pulled from the token store.
- **Type** — Univers + the type ramp (sizes/weights from the scale).
- **Accessibility floor** — contrast thresholds, focus-visible / keyboard ring, target size, reduced-motion, ARIA roles.
- **Safety / UX patterns** — high-value confirmation (no one-click), masked sort/account numbers, the input-modality focus ring.
- **Official brand assets** — the logo/mark is *placed*, never *drawn*.

## 3. Flex — the wide road (invent freely)

- **Composition** — layout, grid, page templates (the canon has *no* template layer — this is always inferred).
- **Concept / narrative / voice / register.**
- **Motion choreography** — what animates and in what sequence — **expressed through canon easing tokens** (`--spring`, `--press`), not re-invented.
- **Data-viz** — the encoding and the story — **on a canon data palette** (see gaps).
- **Density, scale, emphasis.**

## 4. Ratified curbs — decided 2026-07-02 (Dave)

Formerly "Undecided". All four rules are now explicit; no run guesses:

| Rule | Ruling |
|---|---|
| **Flatness** | Fixed (flat) in *sober* and *balanced*. **Unlocked in *expressive* only**, via a defined elevation/gradient ramp derived from brand neutrals — never free-hand. *(Ramp itself: promotion queue.)* **Carve-out (brand rule, `guidelines/data-visualisation.md`): data-chart fills stay flat in ALL registers — the gradient licence never enters a chart.** |
| **Brand dark / inverse surface** | **Promoted.** An `inverse/surface` role derived from the existing dark-theme values, usable in light mode (the balanced register's "one bold moment"). *(Token promotion: queue.)* |
| **Red-forward ceiling** | *Sober*: red = destructive/accent only. ***Balanced* and *expressive*: red may lead the primary action** — aligns the charter with brief v2 §2 and the approved balanced SME screen. |
| **Corner radius** | **Fixed square in ALL registers, including expressive — rounding is forbidden.** A rounded **version of the design system** is named as possible future work; if it comes, it is a system variant, not a register privilege. *(The previously recorded Badge + Avatar round exemption stands unless separately revoked.)* |

**Parked (2026-07-02, Dave):** register reach beyond colour/flatness — whether registers also
tier the flex dials (spacing, density, layout licence). Not ratified; see `_NEXT-SESSION.md` §📌.

## 4b. Register temperature — wit licence per band (PROVISIONAL, 2026-07-02)

The temperature dial now has its brand source: the intelligent-wit gradient
(tov-016), the mid-scale formality anchor (tov-045) and stress-≠-stiffness
(tov-027). Mapping adopted **provisionally** by Dave 2026-07-02:

| Band | Wit licence | Brand-source stop |
|---|---|---|
| **expressive** | **ON — surface-scoped**: headlines, good-news moments, marketing surfaces only; NEVER functional/action copy (the F2 partition: expressive licence is surface-scoped, literalness is function-scoped) | "advertising = dial it up" · "headlines + good news = home turf" |
| **balanced** | **subtle** — a flourish at most, headline-only; body and functional copy stay literal | "functional messages = quite subtle" |
| **sober** | **ZERO wit — warmth stays.** More human, not more formal (tov-027); never dress bad news as good | "important = don't distract" · "difficult situations = zero" |

**Locale/formality is a parameter on any band, not a band** (tov-045): Australia
runs informal, India/Malaysia a few degrees formal, and clarity always outranks
the local adjustment.

*Status: PROVISIONAL — may need adjusting; a separate build-time temperature
control may supersede how this is expressed. tov-016's REVIEW stays OPEN until
that settles (Dave, 2026-07-02).*

---

## 5. Recall vs retrieval

The portfolio "looked HSBC" on **~4 primitives** (the red trio + the teal) — but I *typed them from memory*. Right output, wrong mechanism. **The fix is cheap and total:** if those few primitives are *retrieved from the graph*, the craft layer can run as hot as it likes and **cannot drift off-brand**. Lock the cheap primitives hard; that buys all the freedom above them.

---

## 6. The generate-new mechanism

When retrieval finds nothing that fits, generate — but inside the curbs:

1. **Retrieval-first.** Query the graph for a component/token that fits *before* generating. (The portfolio's whole failure was skipping this — it recalled and invented instead.)
2. **Derive from fixed.** A new value must be *derived from* a brand primitive (a dark ramp from brand neutrals; a data series from brand red + canon teal), not invented free-hand.
3. **Gate against the curbs.** Run the new candidate through the existing gates (contrast, brand-derivation, icon-source, a11y).
4. **Flag for promotion.** Name it a **candidate token/component** and queue it — this is the *same machine we already built* (snippet → meta → gate → gated `.cn-*`). It just needs to run **at generation time**, not only in review.

## 7. Multi-variant per run

Generate a **spread across the register** (e.g. sober → balanced → expressive) on the **same fixed curbs**, differing only on the road. This:

- gives **divergent options** (keep convergent/divergent separate),
- makes **register a visible dial** instead of a buried adjective,
- literally **shows the width of the road between the curbs.**

## 8. Tiering (how the gates apply)

| Tier | What it is | Gate |
|---|---|---|
| **T1 — canon** | 100% retrieved tokens + gated components | `_validate_compose` green (0 rogue hex, all resolve) |
| **T2 — candidate** | retrieved fixed + *flagged* candidate tokens/patterns, derived + a11y-gated | curbs pass; candidates logged for promotion |
| **T3 — exploration** | free craft, brand primitives recalled | no gate (the portfolio piece) — a *signal*, not a deliverable |

The balanced version (`sme-payments-balanced.html`) is **T2** by design.

---

*Related: `_COMPONENT-GAPS.md` (the promotion queue), `_RUNBOOK-gated-component.md` (the promote machine), the compose gate (`_validate_compose.py`).*
