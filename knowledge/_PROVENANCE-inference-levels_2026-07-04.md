# Provenance of the inference levels — tightening "HSBC-ness"

*Morning task, 2026-07-04. Resolves the OPEN item on `register-inference-ramp` and the
GOOD-MORNING desk flag. Decision record for a proposed charter §9 patch — **not yet enacted**
(canon change = Dave's judgment). Related: `_FIXED-FLEX-CHARTER.md` §4b/§5/§9,
`_RECONCILIATION-charter-language.md`.*

---

## Summary (read this)

**The problem.** §9 governs the visual register with *vibe-words* — "must still read HSBC",
"hot but leashed", "brand-ness is retrieved". None of them say **where** that brand-ness is
retrieved *from*. An unanchored "HSBC-ness" standard silently defaults to the model's own
training notion of HSBC — which is exactly the §5 recall-drift you locked out at the **token**
layer sneaking back in at the **register** layer, one level up.

**The fix already exists in the same doc.** §4b (wit licence) solved this for *copy*: every
band carries a **"Brand-source stop"** pointing at a governed source (tov-016/027/045). The
visual register (§9) never got that column. **This task applies the §4b pattern to §9.**

**The finding that matters.** "Reads HSBC" was treated as an unanchorable feeling. It isn't.
It **decomposes** into four retrieval targets that all exist and are governed, plus one small
human residue:

1. **Primitives** → the token store (`tokens/colour.json` etc.) — already locked (§5).
2. **Composition** → the canon (`canon/canon.css`, 32 `.cn-*` components).
3. **Character** → `guidelines/brand-principles.md` — the **six design principles** ("angular,
   tactically red, clearly understood, internationally relatable, logical, creatively
   considered") + the supercharge direction ("simpler, stronger, superior"). *This is the
   pointer §9 was missing.*
4. **Tone** → §4b's stops (already done).
5. **Residual** whole-screen gestalt ("does it *feel* right?") → a **human taste call**. Small,
   named, and explicitly out-of-model — because gestalt is where LLM-as-judge fails.

**Net:** ~80% of "HSBC-ness" becomes a retrieval instruction; the rest becomes an honest
taste-call or a flagged gap. Nothing is left to the model's priors.

**On your desk:** three real judgment calls (D-1…D-3 below) are yours, not mine. Say the word
on those and I enact the §9 patch.

---

## The disposition map

Legend — **R** retrieve (pull from a named source, never recall) · **T** taste (human call,
out-of-model) · **G** gap (KB silent → flag at generation, don't improvise).

| # | Vibe-term (band / §) | Disp. | Provenance / action |
|---|---|---|---|
| 1 | **"must still read HSBC" / "brand-ness is retrieved"** (balanced, §9) | **R + T** | Decompose: primitives → token store · composition → `canon/canon.css` `.cn-*` · **character → `brand-principles.md` six principles + supercharge direction** · tone → §4b. Residual whole-screen gestalt → **T** (D-1). |
| 2 | **"hot but leashed"** (expressive, §9) | **R** | Already mechanical, just un-named. "Hot" = the **foundational curbs released** (the §9 list). "Leashed" = the **cardinal floor**, retrieved (token store) + a11y/safety gates. Rephrase to name the leash = the cardinal list. No new source. |
| 3 | **"Sober = don't infer, not boring"** (§9) | **R** | Already de-leaded. Sober = retrieve + assemble from canon/token store. Fine as-is; add explicit source pointer for symmetry. |
| 4 | **"composition from canon"** (balanced, §9) | **R** | Name the artifact: `canon/canon.css` (`.cn-*`) + `_XREF-INDEX.json` for the per-component contract. Currently says "canon" without the pointer. |
| 5 | **"tone from the guidelines corpus"** (balanced, §9) | **R** | Point at §4b (which points at tov-016/027/045 + `tone-of-voice.md`, `copywriting.md`). The corpus is named but not narrowed — §4b already narrowed it, so cross-ref it. |
| 6 | **"widest licence on composition and concept"** (expressive, §9) | **R (bounded)** | Licence is real but **bounded by the cardinal list**; anything genuinely new routes through §6 generate-new (derive-from-primitive + flag). Cross-ref §6; no new source. |
| 7 | **"red-forwardness"** (foundational curb, §9/§4) | **R** | Source exists: `guidelines/colour-usage.md` + `colour-standards-2026.md` govern when red may lead. Name it so "red-forward" isn't eyeballed. |
| 8 | **§4b copy glosses** ("dial it up", "home turf", "quite subtle", "don't distract", "difficult = zero") | **R ✓** | Already carry Brand-source stops (tov-016/045/027). **This is the model to copy** — no action, cited as the pattern. |
| 9 | **"does it *feel* HSBC?"** (whole-screen gestalt) | **T** | The honest residue after 1–8. Name it explicitly in §9 as a **human taste call**, not a model or gate judgment. Prevents the engine from faking a gestalt verdict. (D-1) |
| 10 | **A required "feel" the corpus doesn't cover** | **G** | §9-balanced already says "flag where the KB is silent" — promote that from a clause to a **named generation behaviour**: emit a candidate + flag (§6), never fill from priors. (D-2) |

---

## Proposed §9 patch (for approval — not yet applied)

Two additions to §9, both mirroring §4b. **A —** a provenance rule (one paragraph). **B —** a
"Brand-source stop" column on the band table.

**A. New paragraph after the ranked-curbs list:**

> **Provenance rule — "reads HSBC" is a retrieval instruction, not a feeling.** Every band's
> brand-ness resolves to a **named source**, never to the model's prior: **primitives** →
> token store · **composition** → `canon/canon.css` (`.cn-*`) · **character** →
> `guidelines/brand-principles.md` (the six design principles + supercharge direction) ·
> **tone** → §4b (tov-016/027/045). Where a required quality has **no source in the KB**, the
> engine emits a flagged candidate (§6) — it never improvises from priors. The **residual
> whole-screen gestalt** ("does it feel right?") is a **human taste call**, explicitly
> out-of-model: the engine assembles from sources and flags; a person judges the gestalt.

**B. Add a column to the §9 band table:**

| Band | Inference | Curbs in force | **Brand-source stop (new)** |
|---|---|---|---|
| **Sober** | OFF — retrieve/assemble | all | token store + `canon/.cn-*` (retrieve only) |
| **Balanced** | ON, bounded | cardinal + foundational | + `brand-principles.md` (character) + §4b (tone); flag-where-silent |
| **Expressive** | MAX | cardinal only | cardinals retrieved from token store; new = §6 derive-and-flag; gestalt = **human** |

---

## Decisions — RULED 2026-07-04 (Dave)

- **D-1 — the gestalt boundary → the two modes became a harness dial.** Rather than a single
  human/model line, Dave reframed it as **two working modes** that belong in the harness
  (mapping onto the flexing engine's floor/ceiling ends, ADR-0006):
  - **Converge / ship mode (Option B — ADOPTED):** an advisory brand self-check runs the six
    principles as a retrieved checklist, surfaced as a pre-flight card (not a gate; contrast-gate
    humility label). Floor/churn end.
  - **Explore / noodle mode (Option A — OPEN):** no automated verdict; open human judgment /
    dossier-style deliberation. Ceiling/novel end. **Kept open, not rejected.**
  - **Mode itself is a named-not-built harness dial.** Enacted to §9a.
- **D-2 — flag-where-silent → ADOPTED as an advisory generation behaviour** now (not left as
  prose). Enacted to §9a.
- **D-3 — character stop → base + conditional (my recommendation, adopted).**
  `brand-principles.md` (six principles + supercharge) is the sufficient **base** stop for
  product UI; `brand-refresh-assets.md` is a **conditional add-on** only on imagery/marketing
  surfaces (where it also drags in the hard gen-AI-imagery ban). Enacted to §9a.

*Enacted in `_FIXED-FLEX-CHARTER.md` §9 (Brand-source stop column) + new §9a (provenance rule,
self-check, two modes). This doc is the decision record.*

---

## Verification

Every source named above was confirmed to exist before writing: `tokens/colour.json`,
`canon/canon.css` (921 `.cn-*` references), `guidelines/brand-principles.md` (six principles at
line 14, supercharge at line 33), `guidelines/tone-of-voice.md` (tov-016/027/045 anchors
present), `guidelines/colour-usage.md` + `colour-standards-2026.md`. No retrieval target was
asserted without checking it resolves — asserting a fake source would itself be the drift this
task removes.
