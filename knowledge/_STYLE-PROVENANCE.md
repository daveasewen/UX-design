# _STYLE-PROVENANCE — what theme every artefact is on, and what's left to align

*The durable record Dave asked for on 2026-07-20 ("this is too loose … have a clear record of what
we've done … make sure we don't miss this in the future"). Classifies every HTML artefact and every
divergent token role across `snippets`, `_proforma`, `_review`, `_fitness-test` by **theme-era**, so
"align to Apollo Mono, with Apollo Legacy in mind" is a tracked, gated state rather than a manual
chase. Read alongside **ADR-0011** (four-theme token architecture) and **R-D19** (Legacy red vs Mono
red). Machine mirror: `reviews/_style-clusters.json`. Visual review screen (per-cluster, open/fullscreen per variant):
`reviews/STYLE-CONSOLIDATION-REVIEW-2026-07-20-v2.html` (v1 COMPARE was the first cut, superseded).*

---

## The model (ADR-0011 + R-D19, in one breath)

**One token store · one baseline library · four themes as override sets** (R-D15, now mechanised in
ADR-0011): **Apollo Legacy · Apollo Mono · Apollo Console · Apollo Supercharge.** Mono is the base;
Legacy is the populated override (reds/teal/grey ramp); Console + Supercharge are declared **nullable**
override slots (ADR-0010). A component binds a semantic role; the active theme decides the hex.

**Red is themed, not universal (R-D19):** Legacy red `#DB0011`/`#A8000B` = Apollo Legacy only (CTA,
tabs, progress, Legacy error). Apollo Mono's only red is `#B92F1E`, used **only** for status/RAG +
dataviz. **Any Legacy red resolving in a Mono surface is drift.**

## Style-eras (how each artefact is tagged)

| Tag | Meaning | Action |
|---|---|---|
| **MONO-clean** | Resolves entirely on Mono values (mono ramp; no Legacy red/teal/grey) | Keeper. |
| **MONO+drift** | Mono-era but still pulls a Legacy value (red/teal/grey) in live CSS | **Align** — re-home the drift. |
| **LEGACY/old** | Pre-Mono build on the old HSBC palette | Legacy-theme reference, or mine + supersede. |
| **neutral** | Uses canon classes, no explicit palette hex in live CSS | Inherits theme; check on render. |

## Scope — what aligns, what doesn't

- **LIBRARY — align to Mono:** `snippets` (canon), `_proforma` (interactive specimens), `_review`
  (review copies — *derivative*, regenerated from source via `_make_review.py`, so fixing source fixes
  them; don't hand-edit).
- **`_fitness-test` — mixed (Dave, 2026-07-20 "there's good work in _fitness-test"):**
  - **Exploration (pre-canon)** — the AB-showcases / responsive studies that seeded the canon snippets.
    *Good work* — compare beside canon, carry forward anything the snippet dropped, then supersede.
  - **Research / inference** — register-spread bands, cold-inference diagnostics, KB-only route tests,
    the token-proposal studies. *Preserve* — these carry findings (`_PROBE-and-selfcheck.md`,
    `_FINDINGS.md`); not for Mono alignment.
  - **JOURNEY — ignore (Dave's ruling):** the SME-payments journey variants (11) are **test pages**.
    Excluded from alignment and from the compare grid.

## Per-area status (2026-07-20)

| Area | Files | MONO-clean | MONO+drift | LEGACY/old | Role |
|---|---|---|---|---|---|
| `snippets` | 40 | 21 | 19 | – | Canon — the alignment target |
| `_proforma` | 12 | – | 12 | – | Mono specimens carrying pre-R-D18 teal + Legacy red |
| `_review` | 9 | – | 9 | – | Derivative review copies (fix at source) |
| `_fitness-test` | 60 | 1 | 1 | ~42 + 16 research/neutral | Exploration + research + journeys |

## Duplicate patterns — compare visually, then rule

Open **`reviews/STYLE-CONSOLIDATION-REVIEW-2026-07-20-v2.html`** (per-cluster review screen; Open ↗ /
fullscreen per variant): 20 component clusters render old
*exploration* beside *canon* so the keeper is obvious and dropped ideas are visible. Rule per cluster
(keep / migrate / archive); this table records the standing recommendation.

| Cluster | Variants | Keeper (recommended) | Notes |
|---|---|---|---|
| Pro-forma tranches | 11 | the proforma specimen | all MONO+drift — align in the T1–T9 sweep |
| Tabs | 8 | `snippets/Tab-bar` + `Tabs` (canon) | + route-a/route-b research, tabs-responsive exploration |
| Button | 6 | `snippets/Button` (canon) | 3 fitness-test showcases = exploration |
| Masthead | 3 | `_proforma/Masthead-interactive` | + 2 review copies |
| DataViz | 2 | `_proforma/DataViz-interactive` | + review copy |
| Amount display | 2 | `snippets/Amount-display` (MONO-clean) | review copy is derivative |
| Cards / Tags / Dropdown / Input / Links / Modals / Selection / Notifications / Status / Tooltip / List-items / Progress / Badge / Icon | 2–4 each | the canon `snippets/*` | fitness-test twins = exploration to mine + supersede |

## ★ Mono-alignment backlog (the drift to re-home)

**A. Snippets carrying Legacy drift (19)** — re-home to Mono values:
`Action-bar, Badge, Cards, Confirmation, Dropdown, Hero, Input-fields, Links, List-items, Modals,
Navigations, Notifications, Progress-tracker, Selection-controls, Status-indicator, Tabs, Video-player`
(legacy-red) · `Avatar, Quick-actions` (legacy-grey). *Much of the red is the bare `rag/error` role —
blocked on the error/warning/info ruling (R-D17); grey inks re-home to `color/mono/*`.*

**B. Pro-forma tranches (12)** — all carry pre-R-D18 teal + Legacy red; align in one T1–T9 sweep
(Sonnet, against ADR-0011), then regenerate the `_review` copies.

**C. Red-roles needing a Mono value ruled before their Legacy red can be gate-seeded (R-D19):**
`tabs/active` (Mono = ink indicator, not red — **ruling owed**) · `progress/complete` (Mono = ink/green —
**ruling owed**) · bare `rag/error` (Mono = `#B92F1E`, rebinds with error/warning/info per R-D17).

## The gate — how we don't miss this in future

**`_validate_theme_provenance.py`** (advisory now, blocking after migration — ADR-0011). It reads
*this file's* file→theme map, resolves each Mono-designated surface under the Mono theme, and flags any
value belonging to another theme's override set — plus **hardcoded** Legacy hexes the token-resolution
leak gate can't see. Report: `knowledge/_THEME-PROVENANCE-GATE.md` each build.

**Standing rule:** a new library file is Mono unless recorded here otherwise; adding it puts it in the
gate's scope. Promotion of the gate to blocking is tracked in ADR-0011.
