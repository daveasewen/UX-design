# Fixed / Flex charter — governing brand-true generation

*"A wide road with high curbs."* The rules that let generation be **creative where it matters** (the road / flex, §3) while it **respects the curbs that never move** (the cardinals, §9). Drafted 2026-06-30 from the SME-Payments fitness tests (sober → desktop → Swiss → portfolio).

---

## 1. The two dials

Every generated screen is the product of **two independent dials**, and confusing them is the root of the differing results:

| Dial | Governs | Today | Risk |
|---|---|---|---|
| **Canon** (vocabulary) | tokens + components — *what is retrieved* | gated (`_validate_compose`, snippet/meta/icon/a11y gates) | strong below the component line, **silent above it** |
| **Register** — the *level of inference* (§9) | concept, density, how hot the craft runs — the *felt effect* of the inference dial, not its definition | **governed** by the §9 ramp (was ungoverned/adjective-buried) | resolved — the ramp makes it explicit and repeatable |

The four SME versions used the **same canon** at **opposite registers**. The sober↔portfolio gap was mostly the *register* dial — a word ("sober"), not the canon. **Make register an explicit, named input**, not an adjective.

---

## 2. Fixed — the curbs (always *retrieved*, never typed)

These are non-negotiable and must be **retrieved from the token store** (`knowledge/tokens/`) **and canon** at generation time. Recall is not allowed (recall drifts; retrieval can't).

- **Brand colour values** — the red and the core palette, pulled from the token store.
- **Type** — Univers + the type ramp (sizes/weights from the scale).
- **Accessibility floor** — contrast thresholds, focus-visible / keyboard ring, target size, reduced-motion, ARIA roles.
- **Safety / UX patterns** — high-value confirmation (no one-click), masked sort/account numbers, the input-modality focus ring.
- **Official brand assets** — the logo/mark is *placed*, never *drawn*.

## 3. Flex — the wide road (invent freely *at expressive*)

**Per §9 these are *foundational* curbs — flex at expressive, held at sober & balanced.** "Invent freely" describes the *expressive* band; at sober & balanced, composition / density / motion are curbs, not open road. (Register, listed below, is now the inference dial of §9, not a flex item.)

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

**RESOLVED 2026-07-03 (Dave) → §9:** register reach — registers **do** tier the curbs.
The register is an **inference ramp** that lifts *foundational* curbs from sober→expressive
while the *cardinal* curbs never move. (Was: parked 2026-07-02.)

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

**§4b = the copy/tone dimension of the §9 ramp** — wit licence scales with the inference
band exactly as the curbs do (sober = zero wit, expressive = on). Resolve tov-016 to lift
the provisional tag.

---

## 5. Recall vs retrieval

The portfolio "looked HSBC" on **~4 primitives** (the red trio + the teal) — but I *typed them from memory*. Right output, wrong mechanism. **The fix is cheap and total:** if those few primitives are *retrieved from the graph*, the craft layer can run as hot as the register licenses (§9) and **cannot drift off-brand**. Lock the cheap primitives hard; that buys all the freedom above them.

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

**Machinery (§9):** generate each band in **isolation** (a cold pass from the same signed
contract — no anchoring) and run a **divergence probe** on the spread (flag if the bands
cluster). Register is the *inference ramp* of §9, not a set of looks.

## 8. Tiering (how the gates apply)

| Tier | What it is | Gate |
|---|---|---|
| **T1 — canon** | 100% retrieved tokens + gated components | `_validate_compose` green (0 rogue hex, all resolve) |
| **T2 — candidate** | retrieved fixed + *flagged* candidate tokens/patterns, derived + a11y-gated | curbs pass; candidates logged for promotion |
| **T3 — expressive** | max inference within the cardinal curbs (**retrieved**, not recalled) | cardinals enforced; divergence-probed; new candidates flagged (§9) — the leash the old ungated T3 lacked |

The balanced version (`sme-payments-balanced.html`) is **T2** by design.

Under §9 the tiers align with the inference ramp: **sober ≈ T1** (retrieve), **balanced ≈ T2**
(extend, derive-and-flag), **expressive ≈ T3 but *within the cardinal curbs*** — the leash the
old T3 lacked.

---

## 9. Register = an inference ramp (ranked curbs) — ratified 2026-07-03 (Dave)

Register is **not a look; it is the level of inference** the engine is licensed to use —
realised as a ramp that lifts curbs down to a floor that never moves. This supersedes the
"describe the output" framing (which was *leading*: it prescribed a dark band / a hero / a
gradient instead of setting the dial) and **resolves the §4 parked question** — registers
*do* tier the curbs; that tiering *is* the register.

**Two coupled dials move together across the ramp:**

| Band | Inference | Curbs in force |
|---|---|---|
| **Sober** *(retrieve)* | OFF — retrieve and assemble what exists; invent only if forced, then derive-from-canon + flag | all (cardinal + foundational) |
| **Balanced** *(extend)* | ON but bounded — invent, but its brand-ness is *retrieved*: cardinals from the token store, composition from canon, tone from the guidelines corpus; flag where the KB is silent | cardinal + foundational |
| **Expressive** *(invent)* | MAX — widest licence on composition and concept; anything new is derived from a cardinal and flagged (§6), never recalled | **cardinal only** |

Sober→balanced turns *inference* on; balanced→expressive *releases the foundational curbs*.
"Sober" means **don't infer** — not "boring".

**The curbs, ranked:**

- **Cardinal — never lifted, any register (the floor):** brand colour (retrieved), type
  (Univers + ramp), corner radius / angles (square), logo & brand assets (placed), the
  **a11y floor** (AA contrast, focus ring, target size, reduced-motion, ARIA), the **safety
  patterns** (high-value confirm, masked account/sort refs), and the **data-chart-flat**
  carve-out. *(= the §2 non-negotiables + §4 radius + §4 chart carve-out, now named.)*
  **The cardinal floor is what makes MAX inference safe:** retrieval-not-recall on these cheap
  primitives (§5) means the craft can run as hot as it likes and *cannot* drift off-brand.
  Expressive is "hot but leashed", not the ungated free-for-all the old T3 was.
- **Foundational — held at sober & balanced, released at expressive:** flatness / elevation
  (the §4 derived ramp), composition & layout templates, density / scale / emphasis, motion
  amount, red-forwardness (§4), new-component/cluster invention. Releasing these *is* what
  "expressive" means.
- Everything else is **road** (flex, §3); the inference dial sets how far onto it the engine drives.

**Generation machinery — two pieces, specced (not yet built):**

1. **Isolated generation.** Each band is produced in a **cold, independent pass from the
   *same signed contract*** — none seeing the others. Generating the spread sequentially in one
   context lets later bands *anchor* on earlier ones and collapse toward a shared mean (the
   "why were they so similar?" pollution). Isolation removes the anchoring — the
   isolated-context subagent pattern (`docs/research-dossier.md`).
2. **Divergence probe (advisory → earns blocking by bite-test).** After the spread lands,
   measure how far apart the bands actually are (structural diff / novelty count). If they
   cluster inside a threshold, the spread failed to span the road — flag it. Turns "did they
   pollute each other?" into a signal. **Threshold is screen-relative:** a cardinal-heavy
   screen (dense data, safety-critical — e.g. payments) has a *narrow road*, so the bands
   *should* look alike; that is not a failed spread. The probe accounts for how much flex the
   screen actually carries.

**Naming:** the bands keep their names (sober/balanced/expressive) — they appear in the brief,
the contract and the mock, so a rename carries blast radius. The *(retrieve / extend / invent)*
gloss is the plain-language meaning; a full rename is deferred, not rejected.

*Upgrades §7 (multi-variant) with the machinery above; relates to §5 (retrieval = the cardinal
leash) and §8 (tiers). The two machinery pieces are new named-not-built gaps.*

---

*Related: `_COMPONENT-GAPS.md` (the promotion queue), `_RUNBOOK-gated-component.md` (the promote machine), the compose gate (`_validate_compose.py`).*
