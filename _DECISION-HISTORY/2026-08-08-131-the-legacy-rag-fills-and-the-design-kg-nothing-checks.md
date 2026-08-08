# #131 — the legacy RAG fills Dave gave us, and the design KG that nothing re-checks

```
provenance: 131 · 2026-08-08
status: ruled → knowledge/_rulings.json § s131-D1 · notes/_MEMENTO-DECISIONS.md § ★ #131
```

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #131 · **Ruling:** `knowledge/_rulings.json` § `s131-D1`
· **Banner:** `GOOD-MORNING.md` ★ LATEST #131 · **Render-proof:**
`reviews/LEGACY-RAG-BANNERS-2026-08-08-s131-v1.html` (registered in `knowledge/_REVIEW-SIGNOFF.md`)
· **Measurements:** `notes/_GAUGE-LOG.md` § `#### 2026-08-08 #131`.
Both-way links per `_DECISION-HISTORY/README.md`.

---

## Why this dossier exists

#130 ruled six things and enacted three. Item ① of its residual was the enactment lane: `s130-D4`/`D5`/`D6`
plus tabs plus "legacy success + info banners take reversed white text, exact values **owed at
enactment**". #131 did not enact that lane. It did something better and narrower: **Dave supplied the
legacy system's own Figma values directly**, which made the owed half of the colour question a ruling
rather than a derivation — and the derivation #130 had floated (`#4F77B0`, reached by moving legacy info
toward console/SC) was superseded by it.

The session is worth a narrative for three reasons: the ruling replaced a *derived* value with a
*sourced* one; the enactment crossed four different strata (spine values, snippet consumption, generated
canon, component-spec prose) and only three of them had anything that would ever re-check them; and the
fourth — the component-spec KG — was found stale **by Dave's own question**, not by any gate.

---

## Finding 1 — a sourced value beats a derived one, and the record has to say which it is

**The arc.** #130 had legacy information moving toward `#4F77B0`. That value was not Dave's; it was
reached by measurement, chosen partly because it also fixed the console/SC information REST failure. It
was recorded as a *floated direction* with the exact values explicitly owed. #131 opened with Dave
handing over the Figma-file values for all four legacy RAG fills:

| severity | fill | ink | measured |
|---|---|---|---|
| error | `#A8000B` | white | 7.87 |
| warning | `#FFBB33` | **dark ink** | 11.57 |
| success | `#00847F` | white | 4.56 |
| information | `#305A85` | white | 7.17 |

**Why the amber is the exception, stated rather than implied.** White on `#FFBB33` measures **1.69** — it
is not a stylistic exception, it is the only leg where reversal is impossible. Writing the reason next to
the exception is the difference between a rule a later session can apply and a rule a later session will
"tidy" into consistency.

**The precedent conflict, surfaced before the move and not after.** `s123-D1` had ruled amber
`#F0B13A`. The conductor put the conflict to Dave explicitly and he confirmed the supersession in his own
words. This matters procedurally more than chromatically: a supersession discovered *after* the write
reads as an accident; one confirmed before it reads as a ruling. The precedent was not quietly
overwritten — `s131-D1` names what it supersedes, both `s123-D1`'s amber and #130's floated `#4F77B0`.

**A discrepancy declared instead of corrected.** The pre-existing `on-success` token note carried a
figure of **3.47:1**. Against `#00847F` the measurement is **4.56**. We do not know what the 3.47 was
measured against, and inventing a reconciliation would have been a confident false inscription. The note
was amended **by addition** to carry both figures and say the old one does not reproduce. The tight leg
(4.56, AA-normal-text pass with no margin) was re-measured on the *committed* bytes specifically because
a boundary value measured on a draft is not a receipt for what shipped.

---

## Finding 2 — enactment crossed four strata, and they are not equally defended

The values half and the consumption half are the split the derivation-governance rule already names.
#131's enactment touched, in order:

1. **Spine (values).** `knowledge/tokens/themes/apollo-legacy.overrides.json` — warning-bg, information-bg,
   `text/on-success`, and the theme half of `rag/text/on-information`. `knowledge/tokens/semantic-colour.json`
   — a **minted base slot** `rag/text/on-information`, whose base value is the dark on-light ink `#1A1A1A`,
   the licence carried in the note. Every note amended **by addition** with `s131-D1` provenance.
2. **Consumption.** `knowledge/snippets/Banner.reference.html` — `.banner.info` ink rebound from
   `--on-light` to a new `--on-info` var resolving to `rag/text/on-information`; manifest and
   `contrastPairs` updated in the same pass; the snippet's `$note` amended because its "white only on
   error" clause was now **base-scoped**, not universal.
3. **Generated canon.** `gen_canon_tokens.py` (541 root vars) → `gen_theme_cascade.py`
   (201 paths / 206 projections, `--check` rc=0, in sync) → `gen_canon_components.py` (75 components).
4. **Component-spec KG.** `knowledge/components/banner.meta.json` — three prose claims that had gone
   false: the error "ONE white-type surface" line (now base-scoped) and the success and information ink
   lines. Amended by addition, hand-formatted JSON edited surgically, re-validated.

Strata 1–3 have machinery that would eventually notice a lie: the cascade `--check`, the generators,
the snippet validator. **Stratum 4 has nothing.** Which is Finding 3.

---

## Finding 3 — the component-spec KG is not indexed and nothing re-checks it (REPORTED, NOT REPAIRED)

`knowledge/components/*.meta.json` — **76** (⚠ **MEASURED at the wrap and it corrected this session's own figure: the brief and every first draft said 78 — 78 is the DIRECTORY's entry count; 76 are metas, plus `meta.schema.json` and `_ACCESSIBILITY-CONFORMANCE.md`; 77 repo-wide, one lives at `knowledge/_proforma/icon-button.meta.json`. Registered as `ASSERT-009` so the count is re-tested, not repeated**) of component specification, including token claims in
prose — is **not in the memento index**, and **no enactment checklist names it**. `banner.meta.json` sat
stale against `s131-D1` through the whole values-and-consumption enactment and was found only because
**Dave asked** whether the design KG had been updated.

This is precisely #130's class: *a record true when written, gone false, with nothing that re-checks it*
— and it is the fifth medium that class has now appeared in. The remedy is **not** taken here, because
which remedy is Dave's call:

- **(a)** add the metas to the memento index, so retrieval at least surfaces them;
- **(b)** a **parse-gate** on meta token-claims — the strongest option, and the one the "first gate =
  PARSE in the consumer's grammar" rule points at, since a claim like *"white type on error only"* is
  checkable against the token store;
- **(c)** an enactment-checklist line, the cheapest and the weakest — a convention with no gate is a
  preference.

⬛ **OPEN → #132, owner DAVE.** Dave also asked, in the same beat, **how the design KG is used, indexed
and checked** — the honest answer today is: *used* by hand and by whoever reads it, *indexed* nowhere,
*checked* by nothing. That answer belongs beside the gap, which is why both are recorded here.

---

## Finding 4 — the control that could not run, and why the number is still honest

`_validate_snippets.py` reports **156 ❌**. The intended attribution method was a `git stash` control —
run the validator with and without this session's diff. **`git stash` returned rc=1** (the known
zero-byte `.git/index.lock` on the mount), so **the control could not run**.

Attribution fell back to **content**: no fail line names the minted slot `rag/text/on-information`; the
12 Banner fails are the pre-existing #130 drift family (mono base vs legacy-reference hexes) and the
value-pairs they name are untouched by this diff. That is a reasonable reading. **It is not a proof, and
it is written as UNPROVEN** — the difference between "unchanged" and "unchanged, attributed by content
because the control refused" is the whole discipline. The 156 are **reported, not repaired**; repairing
them is not this session's licence.

---

## Finding 5 — a new pothole in the render lane: the home volume was full

The render-proof was produced under the render runbook's recipe with a **`/var/tmp` rehome**, because
`$HOME`'s volume was **100% full**. This is a sibling of the ENOSPC finding #129 adjudicated (the
98%-full shared `/sessions` volume presenting as *"Download failure, code=1"*), on a different volume,
and it is worth one line in the render runbook's addition style. It is recorded here rather than written
into the runbook as a rule, because a single observation is a datapoint, not a threshold.

The proof itself is the strong part: computed values asserted **EXACT on all 8 legs** (4 severities ×
light/dark) at **1180** and **480**, real HSBC face (`document.fonts.check` true), and **the conductor
viewed the crop**. Drive the thing — a green assertion plus an unviewed render is still an assertion.

---

## Where this leaves us

**Resolved.** `s131-D1` ruled and **enacted end-to-end**, values → consumption → regen → component spec →
render-proof, with the tight leg re-measured on committed bytes and one discrepancy declared rather than
smoothed.

**Still open.** The component-spec-KG remedy (Dave's, three options above, with his "how is the design KG
used/indexed/checked" question attached) · the console/SC lighter information blue, **direction only, no
value**, controller owed · the remainder of `s130-D4`/`D5`/`D6` and tabs — note that the *legacy
reversed-text* half of #130's residual item ① is **DONE** by `s131-D1` and the rest is not · the
error-mark image confirm, **still owed** — Dave sent RAG-fill images, not the error-mark image · the
`mark-vs-fill 3.0` gate · `_validate_state_contrast --selftest` environment-dependence, a named refusal ·
and the 156 validator fails, reported.

**Not closed by this session, and it matters:** the **four REAL contrast-failure records** stay open. The
two console/SC information-rest items and legacy-success-washed were **not** fixed by `s131-D1`; the
legacy fills are a different surface from the state-contrast worklist, and marking them fixed because a
neighbouring value moved is exactly the class of false inscription this project keeps paying for.
