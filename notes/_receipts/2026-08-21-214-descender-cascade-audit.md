# #214 — descender-clip cascade audit (Opus audit sub, READ-ONLY)

**Brief:** Dave, verbatim — *"a lot of the labels don't render properly, the line-height trim is clipping
the descenders, we fixed this ages ago. This worries me that decisions we make that should be applied
globally or have a wide blast radius don't cascade through the components. I don't think that these
components are wired properly still, I'm not confident that it is properly tokenised or an atomic build."*

**Status:** FINDINGS ONLY. Nothing edited, nothing committed, nothing ruled. All prices are candidates.

---

## 1 — THE ORIGINAL FIX: found, still live, and NOT the thing that failed

**Provenance — ds-005**, `knowledge/_DS-IMPROVEMENTS.md:137`:

> `## ds-005 — descender clip on trimmed labels inside icon+label controls. **KEEP — cross-component.**`
> `**Status:** LOGGED 2026-07-18 (Dave: *"a finding we have to keep… it applies to buttons"*).`
> `**GATED + CLOSED 2026-07-19** — Dave: *"do it right — use your suggestion"* (gate, don't blanket the CSS)`
> `and *"I don't want other sessions viewing it as a bug and trying to fix it"*. `_validate_descender_clip.py``
> `is now a blocking build step (27/34): every truncating label (`text-overflow:ellipsis`) must carry`
> `text-box-edge:text text` (or `overflow:visible`).`

Antecedent: the retired memory hook `leading-trim-label-decision` (DECISION 2026-06-29, adopt native
`text-box-trim:trim-both; text-box-edge:cap alphabetic`), gotcha 2 — *"TRUNCATING LABELS — `text-box-edge:cap
alphabetic` + `overflow:hidden` (ellipsis) CLIPS descenders/ascenders (List-items g,y,p cut off)"*.

**PREMISE VERIFIED TODAY (not trusted from the record):**
- `knowledge/_validate_descender_clip.py` EXISTS and runs. Driven this sitting:
  `selftest OK` · `DESCENDER-CLIP GATE PASS — every truncating label is descender-safe (151 file(s)).` rc=0.
- The fix's mechanism is present in canon: `knowledge/canon/canon.css` carries 231 `text-box-trim`
  occurrences and 20+ `text-box-edge:text text` overrides.

So the fix is **not missing and not regressed away**. Dave's instinct that "we fixed this ages ago" is
correct, and the fix is still standing. **The cascade is what failed.**

---

## 2 — THE MEASUREMENT: 6 of 43 REVIEW-213 components, 9 of 135 snippets, 18 dead override selectors

### Method (artefact parsed in the consumer's grammar, per [[no-gate-parses-the-artefact]])

Every component on `reviews/REVIEW-213-wave-components-four-theme-v1.html` mounts
`showroom/<slug>.html`, which srcdoc-mounts `knowledge/snippets/<Name>.reference.html`
(`knowledge/_render/gen_review_213_wave_components.py:14-19`). So the snippet CSS **is** the rendered CSS.

For each snippet I parsed the `<style>` blocks, computed **CSS specificity** for (a) every selector
declaring `text-box-edge:cap alphabetic` and (b) every selector declaring the ds-005 override
`text-box-edge:text text`, applying real `:is()` semantics (**`:is()` takes the specificity of its MOST
SPECIFIC argument**), and flagged any override that loses.

### The mechanism, exactly

Every one of the 43 snippets carries an identical copy of the global trim block:

```
:is(button,a,label,span,small,strong,em,b,i,th,td,dt,dd,li,figcaption,legend,caption,summary,
    output,time,input[type=text],input[type=search],…):not(:has(svg))
    { text-box-trim:trim-both; text-box-edge:cap alphabetic; }
```

Because `input[type=text]` is inside the `:is()`, **the whole rule's specificity is (0,1,1)** — measured
uniformly `(0, 1, 1)` across all 43. A bare single-class override — `.sn-label{text-box-edge:text text;}` —
is **(0,1,0)**. It **loses**. The label keeps `cap alphabetic`, and every descender below the alphabetic
baseline is clipped by the label's own `overflow:hidden`.

This is not inference. `knowledge/canon/canon.css:4713-4721` is a prior session's **first-hand
render measurement of exactly this**, verbatim:

> `/* ⚠⚠ ds-005 IS LIVE, AND IT WAS RE-MEASURED HERE RATHER THAN CITED. The leading-trim rule at`
> `   the top of this file is `:is(button,a,label,span,…):not(:has(svg))`, and the borrowed`
> `   `.sn-label{text-box-edge:text text}` is a SINGLE-class override. Driven in a real browser:`
> `   the computed text-box-edge came back `cap alphabetic`, not `text text`, and every label`
> `   carrying a descender clipped 4.00px below its box (box 11.56px, text 21px, overflow:hidden).`
> `   ⛔ THE FIGURES ARE BYTE-IDENTICAL IN THE GATED Sidebar-nav.reference.html — same 11.56 /`
> `   21 / 4.00 — so this is INHERITED, not introduced, and the parent still carries it.`
> `   ⛔ AND `_validate_descender_clip.py` IS GREEN OVER BOTH, because it reads the DECLARATION`
> `   and not the computed value. A gate that cannot see the thing it is named after.`
> `   The two-class form below out-specifies the trim. Measured after: clipBelow 0.00. */`

`.cn-app-shell-multi-column .sn .sn-label, .cn-app-shell-multi-column .sn .sn-brand{text-box-edge:text text;}`
(canon.css:4724) is the **winning** form. Canon was repaired. **The snippets were not.**

### AFFECTED — REVIEW-213 wave set: **6 of 43**

| # | Component | Wave | Store row | Dead override selectors | trim spec | ovr spec |
|---|---|---|---|---|---|---|
| 1 | Transaction row | 3 | W-63 | `.ldg-name`, `.ldg-ref` (2/2 — **all** its overrides dead) | (0,1,1) | (0,1,0) |
| 2 | Standing order / mandate row | 3 | W-63 | `.mr-payee`, `.mr-meta` (2/2 — **all** dead) | (0,1,1) | (0,1,0) |
| 3 | App shell · side nav | 5 | W-78 | `.sn-brand`, `.sn-label` (2/4) | (0,1,1) | (0,1,0) |
| 4 | App shell · multi-column | 5 | W-78 | `.sn-brand`, `.sn-label` (2/8) | (0,1,1) | (0,1,0) |
| 5 | Template · list / index | 5 | W-77 | `.dr-title`, `.dr-meta` (2/4) | (0,1,1) | (0,1,0) |
| 6 | Template · detail | 5 | W-77 | `.tl-title`, `.dr-title`, `.dr-meta` (3/6) | (0,1,1) | (0,1,0) |

**13 dead override selectors** across the review set.

### AFFECTED — full snippet library: **9 of 135**, **18 dead override selectors of 49 total**

The three beyond the review set are the **PARENT ATOMS the six copied from**:

| Snippet | Dead selectors | Note |
|---|---|---|
| `Sidebar-nav.reference.html` | `.sn-brand`, `.sn-label` (2/2) | ⛔ **gated component**; named unrepaired in `notes/_receipts/2026-08-20-210-wave4-laneA-calendar-tree.md:90` |
| `Document-row.reference.html` | `.dr-title`, `.dr-meta` (2/2) | parent of Template-list-index + Template-detail |
| `Timeline.reference.html` | `.tl-title` (1/1) | parent of Template-detail |

**The propagation is legible in the selector names** — `.sn-*` Sidebar-nav → App-shell-side-nav →
App-shell-multi-column; `.dr-*` Document-row → Template-list-index → Template-detail; `.tl-title`
Timeline → Template-detail. Each child **copied the parent's broken CSS verbatim**, which is
[[specimen-starts-from-reference]] working exactly as ruled — and faithfully copying a defect.

### CLEAN (34 of 43)
The other 34 review components either declare no truncating label at all (28), or their overrides are
already two-class / descendant-scoped and out-specify the trim (6: `cascader`, `tree`, `transfer-list`,
`app-shell-nav-rail`, `template-settings`, `template-empty`).

---

## 3 — TOKENISATION AUDIT (n = 12, includes all 9 affected)

Axes tested: type composites (`.t-cm-*` / `.t-ed-*`, FIRM per canon), font literals, colour literals.

| Component | `.t-cm-*` bound | `font-family` decls | `font-size` decls | `font-weight` lit | `line-height` lit | hex outside token mint | **Verdict** |
|---|---|---|---|---|---|---|---|
| Transaction-row | 6 composites | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Standing-order-mandate-row | 4 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Document-row | 4 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Sidebar-nav | 2 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Timeline | 5 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| App-shell-side-nav | 3 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| App-shell-multi-column | 3 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Template-list-index | 9 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Template-detail | 10 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Limits-meter | 5 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Page-header-lockup | 4 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |
| Card-header-lockup | 5 | 0 | 0 | 0 | 0 | 0 | **TOKENISED** |

**Distribution: 12 TOKENISED / 0 PARTIALLY / 0 HAND-ROLLED.**

Across the whole 43: **zero** literal `font-size`, `font-weight` or `line-height` declarations in any
component rule. Every hex found sits inside a `:root` / `[data-theme]` **token mint block**
(`--surface:#1F1F1F; --hover:#232323; --page:#1A1A1A;` at `Transaction-row.reference.html:165`) —
the ruled resolved-token pattern, not a hardcode.

**⚠ ANSWER TO DAVE'S SECOND WORRY, PLAINLY: the components ARE properly tokenised.** His instinct that
something is unwired is right, but the unwired thing is **the cascade, not the tokens**. The type
composites are bound, the colours are minted from tokens, no literals. This is the one place the audit
contradicts the brief's framing, and the evidence is above.

**⚠ ADJACENT, NAMED NOT FIXED (glob-scope, per [[gate-glob-scope-rule]]):** `_validate_no_hardcode.py`
run this sitting reports `✅ No-hardcode gate passed (11 tranche file(s)).` — **11 files, not 135**.
The tokenisation cleanliness above is my own measurement, NOT that gate's; the gate does not cover the
snippet library.

---

## 4 — THE CLASS DEFECT (one sentence)

> **The ds-005 fix was gated by comparing authored selector STRINGS, so when the fix was later re-derived
> correctly in canon as a cascade-winning two-class selector, the 135 reference snippets each kept their
> own private copy of the global trim rule plus a bare single-class override that silently loses the
> cascade — and the gate certified all 151 files green because it reads the declaration, never the
> computed edge.**

Three compounding sub-causes, each independently worth naming:

1. **THE GATE IS TEXTUAL.** `_validate_descender_clip.py:check()` builds a `covered` set of selector
   strings and asks only "does a rule with this exact selector string declare the override somewhere in
   the file". It has **no model of specificity, source order, or the cascade**. Its own docstring names
   the target as the *authored* string. This is [[mutation-tests-the-clause-not-the-feature]]: it proves
   the CLAUSE was written, never that the FEATURE renders.
2. **THE GATE'S TRIGGER IS TOO NARROW.** It fires only on `text-overflow:ellipsis`. A trimmed label that
   clips via a fixed-height or `overflow:hidden` parent with no ellipsis is invisible to it entirely.
3. **THE FIX HAS NO SINGLE HOME.** canon.css holds the repaired scoped selectors; each snippet holds an
   independent, unsynchronised copy of the trim rule. Nothing reconciles them. This is a
   [[write-once-principle-floated-192]] / ADR-0017 violation on a live fact: the trim rule and its
   overrides have **136 homes**.

**Why it did not cascade, in Dave's terms:** a global decision landed in canon, but canon is not what the
showroom renders. The showroom renders the snippets, and every snippet is a **frozen copy** taken at its
birth. A later global fix cannot reach a copy. The gate that was supposed to be the safety net for exactly
this could not see the difference between a copy that works and a copy that does not.

---

## 5 — PRICED GATE CANDIDATES (candidates, not rulings)

### G1 — specificity leg for `_validate_descender_clip.py` **[RECOMMENDED — do this one]**
Resolve the cascade statically: for each element-bearing override, compute the specificity of the
override rule and of every `cap alphabetic` rule that could match the same element; fail when the
override cannot win (specificity lower, or equal-but-earlier in source order). Requires an `:is()`-aware
specificity function (~60 lines; **already written and driven this sitting** — `/tmp/aud/spec2.py` in the
sandbox, reproducible from this receipt).
**Price: ~90 min · ~18K.** Catches all 18 dead selectors today. Zero new dependencies, runs in CI, works
in both environments (no [[gate-cannot-pass-in-one-environment]] exposure).

### G2 — `--computed` leg (render-based)
Drive each snippet in headless Chromium, read `getComputedStyle(el).textBoxEdge` plus
`scrollHeight > clientHeight` on every trimmed text node. This is the only thing that proves the FEATURE.
Already priced twice before, unbuilt — `notes/_receipts/2026-08-20-210-wave6-laneB-p3-templates.md:694`
and `notes/_receipts/2026-08-20-210-wave5-laneB-templates.md:574`.
**Price: ~3 h · ~45K**, plus a per-build render cost. ⚠ CI-environment risk is real.
**Verdict: G1 first — it catches 18/18 at a fifth of the price. G2 is the residual net, not the fix.**

### G3 — trigger widening (fold into G1)
Extend the trigger from `text-overflow:ellipsis` to *any* trimmed text element whose own or ancestor rule
carries `overflow:hidden` or a fixed `height`. **Price: ~40 min · ~8K**, expected to surface new debt —
**run it in report-only mode first**, do not make it blocking on day one.

### G4 — the write-once repair (the actual cure, and it is NOT a gate)
The 136 copies of the trim rule are the disease; G1 only detects it. Candidate: the trim block becomes a
single generated include stamped by one generator, with the override table beside it.
**Price: UNKNOWN — needs a scoping pass first.** Named, not costed. ⛔ Dave's call; touches every snippet.

### Repair of the 18 live selectors (separate from any gate)
Mechanical: promote each bare `.x{text-box-edge:text text;}` to the two-class descendant form canon
already proved (`clipBelow 0.00`). **Price: ~60 min · ~12K for 18 selectors across 9 files.**
⛔ `Sidebar-nav.reference.html` is a **gated** component — its repair needs Dave's nod, not a lane's.

---

## 6 — PROBES RUN WITH NO MATCH (an unrun search ≡ an absent record)

- `grep -i "descender|leading-trim|text-box-trim|half-leading" knowledge/_rulings.json` → **no match.**
  ds-005 is **not** in the rulings store; it lives only in `_DS-IMPROVEMENTS.md` prose. ⚠ That is itself a
  [[forgotten-document-class]] exposure — a retrieval-by-default query against the store would say
  "never decided". Worth a store row. Named, not fixed.
- `font-size:` / `font-weight:` / `line-height:` numeric literals in component rules across all 43 → **zero.**
- `.t-ed-*` / `.t-cm-*` absent from any audited component → **zero** (all 12 sampled bind composites).
- Hex colour literals outside token-mint blocks → **zero.**
- `_validate_descender_clip.py` run in build mode → **PASS, 151 files, rc 0** — i.e. the gate is green
  over all 18 defects. The pass IS the finding.
- Not chased, deliberately (named per brief): status-indicator canon jump; the fixed-`height` clip class
  (subsumed into G3); the `1097→1099` type-composite ratchet tension named in the #213 review prose.

---

*Audit sub, session #214. READ-ONLY — no repo file altered except this receipt. No commits. No rulings.*
