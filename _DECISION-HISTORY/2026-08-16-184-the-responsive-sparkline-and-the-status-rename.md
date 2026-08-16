# #184 — the sparkline is responsive by default, and the status vocabulary is renamed

provenance: s184 · 2026-08-16
status: ruled — `knowledge/_rulings.json` § `s184-D1` · `s184-D2` · `s184-D3`

*Session #184 (2026-08-16, Sun from `date`). FABLE conductor + TWO OPUS build subs + this OPUS wrap
sub. Dave LIVE throughout. THREE RULINGS, all his, all inscribed via `knowledge/_inscribe_ruling.py`
— the only sanctioned writer of `_rulings.json`. Opener, verbatim: **"We have space to push today,
behind pace, fable is slightly ahead but that fine for now."** Close, verbatim: **"good lets wrap."***

Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #184 · banner: `GOOD-MORNING.md` ★ LATEST #184.

---

## Finding 1 — the scaling call was carried for two sessions and took one sentence to settle

The item *"the scaling call at tuner v2 is Dave's eye / #184's natural opener"* had been carried since
#182 at age [2], parked behind a tuner page that presented **scaling as the only open decision**. It
was the session's natural opener and it opened it.

**Why it settled so fast:** the page had already been narrowed by `s182-D3`. The 37-chip colour picker
was gone, the semantic strokes rendered live in both directions, and the only thing left to look at was
the geometry. A decision surface with one question on it gets answered; the same question buried under
thirty-seven chips had waited two sessions.

**The ruling, `s184-D1`, verbatim:** *"the line should be responsive to its enclosure by default."*
Readback confirmed with *"this is all correct."*

**And the part that was NOT ruled, which matters as much:** the page also offered a **4px height-snap**,
in the manner of the `EDIT-MODE-UX-PROTOTYPE-2026-07-19-v3` countdown dial. **Dave did not pick it.** It
is recorded as **open direction** — not deferred, not rejected, not queued as a build. Heights **64/44
stay UNCHANGED and pinned**, and the enactment was explicitly checked to confirm no grid-snap arrived
under the cover of the width change. A pick from an incomplete set reads as a ruling
[[feedback-readback-sensation-not-mechanism]]; the discipline here was to enact exactly one of the two
things on the page.

## Finding 2 — every gate we own is blind to width, and the only reason we know is that we drove it

The `s184-D1` enactment (Opus build sub A) is small: `Chart-sparkline.reference.html` **+55/−12**.
`width:100%` on `.spark-standalone`, `.spark-inline` and `.dv-empty-frame`; the **JS-gated `.dv-fit-on`
release DELETED**; the old 200px moved into a **specimen-only** `.spark-kpi-slot` so the showroom keeps
a fixed-width exhibit without the component carrying one.

The interesting half is the proof. NEW `knowledge/_render/verify_sparkline_responsive.py` — 60 lines,
Playwright, `goto("file://…")` (never `set_content()`, which drops `type.css` silently) — measures
**used width against enclosure content width at 420 / 900 / 1440, with JS ON and JS OFF**.

**The mutation drive is what turned it from a script into evidence.** A restored **fixed 340px**
sparkline passed `_validate_snippets`, `_validate_dataviz`, `_validate_partials` and `_validate_grid`,
**all rc=0**. The render proof failed it, and also failed **the exact pre-#184 shape**. The
discriminating leg is **JS-OFF**: with JS on, the old `.dv-fit-on` release made the component look
responsive, so a JS-ON-only proof would have certified the very build the ruling replaced. *"Responsive
by default"* and *"responsive once the script runs"* are different claims and only one of the two legs
can tell them apart.

**A dead end, recorded because it was nearly a conclusion:** the proof's first red was its own. Body
padding polluted the enclosure measurement and the comparison reported a failure that did not exist.
The bug was in the instrument, not the artefact [[a-crash-is-not-a-fail]]. It was found and fixed before
anything was concluded from it — but a false red that arrives while you are expecting a real one is the
cheapest way to inscribe a wrong fact.

**Declared unproven:** the theme sweep was **not driven**. Only light was measured. Width is
theme-independent *by construction* — which is an argument, and this file is careful about the
difference between an argument and a measurement.

## Finding 3 — the contradiction was in the reading, not in the text

`s151-D1` (the two-red law) and `s149-D1` (the mono error-ink camp) both carry **MONO-ONLY** riders.
`s182-D3` keys the sparkline's semantic stroke across **all four themes**. Carried since #182 as a
**live contradiction in the record**, with both readings defensible from the text.

**`s184-D2` reconciles it to all-themes keying:** the MONO-ONLY riders do **not** restrict the
sparkline's semantic stroke keying; `s182-D3`'s all-four-themes reading **stands**.

**And the riders were not re-stamped.** No text was amended, no rider re-scoped, no value minted. This
is the shape a reconciliation should take when the defect is interpretive: the record was not wrong, the
*join* between two records was unstated. Rewriting either rider would have been supersession by
addition applied to something that was never superseded.

## Finding 4 — Dave named the smell and the cure in the same sentence

**`s184-D3`**, verbatim: *"(breach/watch/healthy/info') is too explicit, it should be something like:
positive, negative, monitor, neutral for this type of status chart."*

⇒ **breach → negative · watch → monitor · healthy → positive · info → neutral**, in the **chart-consumer
alias layer ONLY**. The `rag-*` names are the semantic spine and are **untouched**.

**The double-meaning was surfaced BEFORE the ruling, not discovered after it.** `neutral` now means two
things: a sparkline's neutral *trend* (default ink) and a status chart's neutral *category* (blue). That
was put to Dave explicitly and he accepted it knowingly, verbatim: *"sparks are to indicate trends, and
its teh positive and negative trends that are important. the bars indicate values and allow comparison,
i think it's important to have all 4 categories explicitly indicated with specific category colours."*
Two vocabularies for two jobs, ruled as such.

## Finding 5 — proving a rename is value-neutral, rather than asserting it

The enactment (Opus build sub B) is a **pure rename with equal +/− on every file**: `canon.css` 4/4
(lines 4127–4130, **outside every AUTO region** — generator ownership **disproven with positive-control
greps**, not assumed), `Chart-bar.reference.html` 8/8, `sutherland-fixtures.json` 4/4, plus the new
review page `reviews/STATUS-CHART-RENAME-2026-08-16-v1.html`.

**The proof: HEAD vs working tree, full-page PNGs, BYTE-IDENTICAL** — 115,915 bytes, sha256
`5da382519c1bc905…` on both. Seven gates rc=0 before and after with **output-identical** text. That is
the difference between *"a rename cannot change pixels"* (true, and therefore untested) and *"these
pixels did not change"* [[attribute-the-diff]].

**A correction caught in flight, and it is a repeat of a known class.** The pre-existing
`gen_canon_components` / `gen_theme_cascade` `--check` failures were first reported as **rc=0** —
because `$?` was read from inside a command substitution and belonged to the substitution, not the
program. The sub self-caught it; the corrected reading is **rc=1 before and byte-identically rc=1
after**, which is what the "unchanged" claim now rests on [[check-after-its-own-remedy]].

## Finding 6 — the black bar nobody would have questioned

While mutating the rename, sub B introduced a `fill="var(--status-breach)"` with **no declaration
anywhere** — the exact residue a half-finished rename leaves behind.

**It renders SILENT BLACK, and zero of thirteen gates catch it.** Black is a plausible chart colour; a
reader who was not hunting for it would read the defect as a design choice. Cause named:
`_validate_property_resolves` does not parse a snippet's `fill=` attributes against **that snippet's own
theme blocks** — it resolves what is declared, and never asks whether what is USED is declared.

This session's rename was safe **because a human counted the sites**, not because anything could have
caught a miss. Registered as a priced build candidate — the **chart var-resolution gate** — in
`knowledge/_DS-IMPROVEMENTS.md`, per derivation governance. It is **mine and needs no ruling**: a gate
candidate is not a value. Same class as ds-039: no gate parses the artefact in the consumer's grammar
[[no-gate-parses-the-artefact]].

## Finding 7 — a plain description is not a decision

On the carried `#174` item Dave said: *"I'll need a plain description of this while you enact."* The
conductor delivered it, with three options — **bless the deletion**, **a generator-emitted pointer
line**, or **restore corrected**.

**He did not pick.** The item returns on the residual **re-plained, aged, and open**. Recorded here
because the failure mode is specific and cheap to fall into: a well-written description of a choice
feels like progress on the choice, and a wrap under time pressure is exactly where "we explained it" gets
inscribed as "we settled it" [[feedback-dont-launder-a-premise-into-a-ruling]].

---

## Where this leaves things

**Resolved:** `s184-D1` (responsive by default, enacted, render-proven) · `s184-D2` (all-themes keying,
riders untouched) · `s184-D3` (renamed, enacted, byte-identical). Two carried items **consumed**.

**Open, and named on the residual:** the sparkline render proof has **no consumer** — nothing invokes
it, so the regression it was built to catch is undetected today [[instrument-without-a-consumer]] · tuner
v2 still presents scaling as open and needs a cheap re-scope · the dangling-var gate is a candidate, not
a build · the theme sweep is unproven, light only · the renamed fixture keys feed the fenced
`gen_theme_cascade` defect and must be re-checked under the new names when it is unblocked · and
`_DS-IMPROVEMENTS.md:249`'s old-name prose stands, shown to Dave and unruled.

**Not taken, and not to be laundered:** the **4px height-snap** is open direction; the **`#174`
adjudication** has a description and no pick.
