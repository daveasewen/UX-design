# ADR-0015 — Behaviour partials: the dataviz interaction layer as generated JS

**Date:** 2026-07-23 · **Status:** accepted (Dave, in-chat, confirming the brief's Decision #1 recommendation: *"I think [that] was the decision initially — as long as the JS is light. I want this to be fast and responsive"*) · **Extends:** ADR-0013 (component-type tier — retrieval now reaches BEHAVIOUR, not only CSS rules) · **Relates:** DV-D07 (the two-channel chrome roles this behaviour styles against) · DEF-003 (CSS-governed-motion boundary, unchanged by this ADR)

## Context

The chart-revisit programme (brief 2026-07-23) lifts all five canon chart snippets to the proforma's
Layer-2: interactive value popover, responsive `fitCharts()` reflow, table-view popover,
legend-as-filter, optional title, full motion parity. The proforma proves all of it in **one shared
script — measured 2026-07-23: 9.9 KB raw / 3.2 KB gzipped for the entire kit.** Five snippets each
re-typing that script is the exact anti-pattern ADR-0013 closed for CSS: a shared rule living as
N diverging local copies. Option (b) (a `<script src>` shared module) was rejected because snippets
must stay **self-contained single-file artefacts**; option (c) (inline ×5) rejected per ADR-0013.

## Decision

1. **One source of truth.** The behaviour lives in ONE hand-authored source file (home:
   `knowledge/canon/dv-behaviour.js` — the `type.css` precedent: hand-authored, generator-consumed).
   Modules: popover (`dvTip`) · fit reflow · table-view popover · legend-filter · shared helpers.
2. **Generated injection.** The partials generator injects it into each registered chart snippet
   between `AUTO-BEHAVIOUR` markers with a provenance comment, exactly the ADR-0013 CSS contract:
   regenerate-always where cheap, `--check` sync gate in the build, fails loud, byte-exact.
   Snippets remain portable AFTER generation — the injected block travels with the file.
3. **One registry, both halves — same file.** Chart snippets register in
   `knowledge/component-types.json` (a `dataviz` group): members + the behaviour partial contract
   (markers present · required hooks · manifest binds). Contracts fire on registration (ADR-0013
   posture); the ratchet walks census → advisory → blocking as consumers migrate.
4. **Performance contract (Dave's constraint — GATED, not aspirational):**
   - **Size gate (blocking):** source ≤ **16 KB raw** (observed baseline 9.9 KB covers the full kit;
     the cap is headroom, not a target).
   - **Banned patterns (blocking):** `setInterval` · network calls (`fetch`/XHR) · external
     `<script src>` · DOM polling. Resize handling = a **single rAF-debounced listener**; events
     **delegated** at the figure root, not per-element.
   - **Progressive enhancement:** the baked SVG must render with JS off (the proforma's try/catch
     posture); behaviour only ever *adds*.
   - **DEF-003 boundary restated:** behaviour + data-driven geometry only — no JS scale-physics,
     no `--hs`/`--ps`, no `transform:scale` assignment.
5. **Decorative motion stays CSS** (draws, fades, grows). JS touches geometry only where data
   demands it (fit reflow, arc growth, popover position).

## Amendment — 2026-07-26: ONE source becomes MANY, and the size gate becomes a PAGE budget

**Ruled by Dave, 2026-07-26** (option-select, legend-wave session). Amends §4's size clause and
§3's "one source" posture. Both beats are recorded because the first is still the reason for the
second.

**BEAT 1 — the original rule (2026-07-23).** Size gate: source ≤ 16 KB raw, per registered
behaviour source, against an observed 9.9 KB baseline. The ADR's own words: *"the cap is headroom,
not a target."*

**BEAT 2 — what happened.** The kit grew from the line exemplar to six charts, and DV-D11/12/13
turned the legend from a 3 KB filter into a ~14 KB interaction model. `dv-behaviour.js` measured
15,526 B — 858 B of headroom. Enacting the signed-off legend in one file would have landed at
**26,615 B**; stripping every comment still left **22,364 B**; abandoning DV-D12's sweep as well
still left **21,327 B**. No arrangement that kept one file passed. The question had already been
logged as a deferral in the registry's own `$description` ("amend the cap vs modularise per
family") and as §C·2 #18 in the queue.

**THE RULING — split AND re-scope, not either/or.**

1. **The group may carry MULTIPLE sources.** `canon/dv-legend.js` joins `canon/dv-behaviour.js`
   under `component-type/dataviz/$behaviour`. The generator and gate already iterated `$behaviour`
   entries, so this needed no tooling change — only a registry entry and a second
   `AUTO-BEHAVIOUR` marker pair per member.
2. **The 16 KB cap stays per-source, and its job is renamed: LEGIBILITY.** A behaviour source
   must stay small enough for one person to hold in their head.
3. **A per-group PAGE budget of 32 KB is added** (`PAGE_BYTES`, `check_group`). This is the clause
   that matters. Splitting a source must not buy headroom — without it, the 16 KB constraint
   silently degrades from a page budget to a file budget the moment anyone adds a second file, and
   the gate would read green while the page doubled. That failure shape — *a gate measuring the
   proxy instead of the thing* — is already in this project's record (the declared-pairs-only
   contrast blind spot). It is closed here by construction, and bitten by a selftest that feeds
   `check_group` two sources which each pass 16 KB and together fail 32 KB.
4. **The single-rAF-debounced-resize check moves to GROUP level in the same beat**, for the same
   reason: it was always a page invariant, and per-source it wrongly failed a second source for
   carrying zero resize listeners — which is correct for a source with nothing to reflow.

**Rejected, with reasons.** *Raise the cap to 32 KB and keep one file* — cheapest, but a 26 KB
single file is not legible, and a cap that moves once moves again. *Minify the source* (Dave asked,
2026-07-26) — declined: the cap is a complexity forcing function, and minifying shrinks the number
without simplifying the thing, while letting the source sprawl unpoliced. The reference snippets
carry the injected block inline and must stay readable; the comments are the provenance trail; and
a minifier adds a version-drift surface to a byte-exact `--check`. Transport compression already
takes the group from 28,332 B to 9,622 B gzipped, free. A true wire-weight answer belongs in the
ADR-0008 adapter layer, where a build pipeline is expected — not in canon, where the source is the
artefact.

**Measured at amendment:** dv-behaviour 12,682 B + dv-legend 15,650 B = 28,332 B (86% of the page
budget) once the transitional block is deleted; 31,268 B (95%) while it remains. ⚠ The next
behaviour addition therefore faces this same conversation — that is the forcing function working,
not a defect.

**Open, flagged not ruled:** injection is group-wide, so `Chart-sparkline` — the deliberately
compact, popover-only member — now carries an inert 15.6 KB payload. Per-member behaviour opt-in
is not supported by the registry schema today. Raised for Dave; not decided here.

Node: ADR-0015-A1
Edges: supersedes(ADR-0015, claim=size-clause-and-one-source-posture) · relates(DV-D11, scope=legend-model-needs-its-own-source)

## Amendment 2 — 2026-07-28: the consumes-manifest — universal by default, opt-out by declaration

**Ruled by Dave, 2026-07-28 (session #26; read-back confirmed in his own words: "universal
automatic opt-in with the option to opt-out individually"). Posture: TENTATIVE, revisit open** —
his framing kept: leaning per-member, *"working on instinct… flexible at the moment… might be
neater in the end for them to be global."* The shape was chosen for exactly that flexibility: a
later firm ruling in EITHER direction is a data edit, not a rebuild.

**What it resolves.** Amendment 1's closing flag (above) and the registry dv-legend
`$description`'s open item ("a per-member behaviour OPT-IN in the registry schema… Dave's call,
not a lane's"). The second live case forced the question: Chart-scatter joining the group for
**DV-J2** (chart-table-toggle accretion) would have carried dv-legend's 16,330 B inert, after
Chart-sparkline's first case — and the chart-expansion wave could add up to 8 more members,
multiplying the debt exactly as membership grows. Priced before the wave, not after.

**THE MECHANISM** (`gen_component_partials.py`: `consumes_behaviour` + `non_consumer_marker_fails`):

1. A member object may declare `"consumes": [<behaviour name>, …]`. **ABSENT = every group
   behaviour** — the universal default, today's behaviour; all five members unchanged at
   enactment. **PRESENT = only the listed behaviours'** AUTO-BEHAVIOUR blocks, and only their
   contracts.
2. **Fail-loud both ways:** unknown names REFUSE · an empty list REFUSES (omit the key for
   universal) · a non-consuming member carrying the markers REFUSES — declared-away payload
   present is a defect, not a warning.
3. The declaration is **positive** ("what I consume"), not a refusal list — the checkable form:
   a member using a behaviour without carrying it fails the build in both directions.
4. **Budgets untouched.** Membership never changed source bytes; 16 KB per source · 32 KB per
   page stand; `_validate_behaviour.py` unmodified.

**Proof at enactment.** Seven selftest bites (§5d) including a green control; the
universal-default bite proven able to FAIL by mutation control (default flipped → selftest exit 1
on the right message → restored green). `--check` clean with zero declarations = the
no-behaviour-change control.

**Measured at amendment:** dv-behaviour 13,004 B + dv-legend 16,330 B = 29,334 B (90% of the page
budget). First narrow declaration = DV-J2's enactment (Chart-scatter, `consumes:
["dv-behaviour"]`); Chart-sparkline may shed its inert payload by the same declaration when ruled.

**Drift corrected in the same beat:** the dv-legend `$description` called Chart-scatter a group
member; `$members` never listed it (and it carries 0 AUTO-BEHAVIOUR markers, measured). The #20
survey receipt was right; the prose is corrected where it lives.

**★ FIRST NARROW DECLARATION LANDED — 2026-07-28, session #27** (the amendment's own predicted
first case, enacted one window after it was ruled). Chart-scatter joined the group declaring
`"consumes": ["dv-behaviour"]`: **13,251 B injected, dv-legend's 16,271 B refused entry**, build
72/72 exit 0. The narrow path was exercised only by unit bites until this instance; a mutation
control on the live member now shows it refusing in **four** directions — unknown name, empty list,
declared-away markers present, and **the declaration removed**. That last one was not predicted:
dropping the key makes the member universal, which immediately demands the dv-legend markers it
deliberately does not carry, so the file goes non-conforming. **The declaration cannot be silently
deleted**, which is a stronger safety property than the mechanism was designed for — recorded as
observed, not inferred. Detail and measurements: the DataViz ledger, Open/pending, session #27.

Node: ADR-0015-A2
Edges: supersedes(ADR-0015, claim=group-wide-injection-becomes-manifest-gated)

## Amendment 3 — 2026-09-06 (#250, Dave, option (e)): the unit becomes CODE-ONLY bytes, the page sum becomes `consumes`-aware, and the caps do NOT move

**Ruled by Dave, 2026-09-06, session #250, in chat: option (e) of a five-way fork priced in
`notes/_subreports/2026-09-06-250-PROBE-byte-gate.md`.** Amends §4's size clause and Amendment 1
§3's page-budget clause. Nothing above is rewritten — this amendment is the correction, by
addition, in the ADR-0017 posture.

**⚠ PROSE CORRECTION, STATED FIRST.** Every "**32 KB**" in this document — Amendment 1 §3 ("A
per-group PAGE budget of **32 KB** is added"), Amendment 1 §3's closing bite sentence ("two
sources which each pass 16 KB and together fail **32 KB**"), and Amendment 2 §4 ("16 KB per source
· **32 KB** per page stand") — is **stale and reads 34 KB** as of `#96-D5` (Dave, 2026-08-05:
`PAGE_BYTES` re-dialled 32→34 KB; receipt `notes/_MEMENTO-DECISIONS.md:3874`). That re-dial moved
the constant in code and never reached this document, and it also left three printed strings in
`_validate_behaviour.py` saying "32 KB" for 32 days, so the published `_BEHAVIOUR-GATE.md` printed
the arithmetic contradiction `39.5 KB of 32 KB, 116%`. **Those three strings are corrected in the
same beat as this amendment** (`_validate_behaviour.py` report header, the per-group report line,
the `main()` PASS line). The two surviving "32KB" strings in that file are deliberate history: the
`PAGE_BYTES` comment narrating the #96 re-dial, and the page-budget bite's comment explaining why
it needs a third pad.

**BEAT 1 — what forced the question.** The #249 VFIT build (proposal (a), 19/19, committed
`c05ff59`) added 4,588 B to `canon/dv-behaviour.js`, taking it to 19,768 B raw against a 16,384 B
per-source cap, and the registry group to 40,410 B against a 34,816 B page budget. The kit had
exactly **zero** headroom before the addition: 14,174 + 15,131 + 5,511 = 34,816 = `PAGE_BYTES`
*to the byte*. Any byte added to any dataviz source failed the page gate.

**BEAT 2 — the fork, and what the probe found underneath it.** Four options were priced —
(a) re-dial both caps · (b) build a marked-waiver mechanism · (c) shave comments · (d) park the
lane. The probe surfaced two structural facts none of the four addressed:

1. **Of the 40,410 raw bytes, 15,573 are block comments and 23 are blank lines.** The three
   sources carry **zero** `//` comments. The code is 24,814 B; the provenance trail is the rest.
2. **The gate was not measuring a page.** `check_group` summed *every* source registered in the
   group, while Amendment 2 (2026-07-28) had added per-member `consumes` and **15 of 15 members
   declare one**. Only `Chart-donut` ever loads all three sources. Amendment 2's own sentence —
   *"Budgets untouched… `_validate_behaviour.py` unmodified"* — is the seam: the budget's ADR
   called it a PAGE budget while the code summed a REGISTRY.

**THE RULING — option (e): change the UNIT and the SUMMATION; leave the CAPS alone.**

1. **The measured unit is CODE-ONLY bytes.** `//` line comments, `/* */` block comments and blank
   lines are stripped **at measure time**, in memory, by a scanner in `_validate_behaviour.py`
   (`code_only()`). **No source file is modified; not one provenance byte is spent.** This is the
   whole difference between (e) and (c).
2. **The reason is Amendment 1's own words.** Rejecting minification on 2026-07-26 this ADR wrote:
   *"the cap is a complexity forcing function, and minifying shrinks the number without
   simplifying the thing."* A comment is not complexity. A cap written to force a conversation
   about complexity was, until today, also charging for the answers to that conversation — every
   time a lane documented WHY a routine exists, the gate read it as the routine getting harder.
   That is the gate measuring the proxy instead of the thing, which is the exact failure shape
   Amendment 1 §3 names and closes for the split case.
3. **Both caps are UNMOVED: `MAX_BYTES` = 16 KB per source, `PAGE_BYTES` = 34 KB per page.**
   Amendment 1's *"a cap that moves once moves again"* stands, unspent.
4. **The page budget sums per MEMBER PAGE from `consumes`.** The group's figure is the **worst
   member page** — the heaviest thing a browser actually loads. A member declaring
   `consumes: ["dv-behaviour"]` is no longer charged for `dv-legend`. `consumes` naming an unknown
   behaviour REFUSES (a fourth direction on Amendment 2's fail-loud list, now enforced in the byte
   gate too, not only the generator). Absent `consumes` still means universal, unchanged.
5. **Both figures are reported.** Raw and code-only, per source, with the comment/blank delta, and
   every member page listed. Nothing is hidden by the strip; the report shows exactly what was not
   counted.
6. **Banned-pattern scanning stays on the RAW text.** Only the size measure changes.

**Measured at amendment** (`python3 knowledge/_validate_behaviour.py`, exit 0):

| source | raw | comment/blank | **code-only** | of 16 KB |
|---|---|---|---|---|
| `canon/dv-behaviour.js` | 19,768 | 6,720 | **13,048** | 80% |
| `canon/dv-legend.js` | 15,131 | 7,397 | **7,734** | 47% |
| `canon/dv-donut-sweep.js` | 5,511 | 1,622 | **3,889** | 24% |

Worst member page: **`Chart-donut` 24,671** code-only B (71% of 34,816); the eight two-source
members 20,782; the six `dv-behaviour`-only members 13,048. Under the OLD registry sum the same
tree read 40,410 and was red twice.

**THE STRONGEST CASE AGAINST (e) — that it is a re-dial in disguise.** Stated in full, because it
is the honest objection and it is not weak:

> The cap did not move, but the *thing being measured* got smaller by 15,573 bytes overnight, and
> the file that was 27% over is now 20% under. Nothing about `dv-behaviour.js` changed. If the
> test of a cap is whether it still bites, a change that converts a red into a green with a
> comfortable margin, decided by the people the red was blocking, is a re-dial wearing a different
> word — and a worse one than (a), because (a) at least records honestly in an integer that the
> bar was lowered, while (e) hides the same relief inside a definition. `dv-behaviour.js` is still
> 19,768 bytes for a human to read. Amendment 1 §2 renamed the 16 KB cap's job **LEGIBILITY** —
> *"small enough for one person to hold in their head"* — and a person holds the comments too.

**THE ANSWER, in three parts.**

1. **A re-dial is unfalsifiable relief; this is a testable definition.** (a) makes the gate weaker
   against every future addition of any kind. (e) leaves the gate *exactly as strong against code*
   as it was — proven, not asserted, by `--mutate code-pad`: appending **4,000 bytes of real code**
   to `dv-behaviour.js` still goes RED at 17,054 > 16,384. Under (a) at `MAX_BYTES` = 20 KB, those
   same 4,000 bytes pass. The next behaviour addition faces the same conversation it always faced
   — which Amendment 1 line 90 calls *"the forcing function working, not a defect."*
2. **The objection's own premise is what makes it answerable.** "Nothing about the file changed" is
   true and is the point: the file did not become more complex, so a complexity gate should not
   have started failing it. The bytes that pushed it over were 6,720 B of provenance — VFIT's
   rationale among them. Under (c) the way to green was to **delete** that rationale: pay for a
   complexity budget in documentation. That is the incentive (e) removes, and removing a perverse
   incentive is a real solution rather than a patch (`s234-D6`).
3. **The legibility objection is real and is NOT answered here — it is re-pointed.** (e) concedes
   that 19,768 raw bytes is a long read. But the per-source cap was never able to measure that
   either: it measured bytes, and bytes are a proxy for legibility as poor as they are for
   complexity. If legibility is to be gated, the honest instrument is a *structural* one — module
   count, function length, cyclomatic depth — not a byte count with comments taxed. **Flagged for
   Dave, not decided:** whether a structural legibility check should join this gate. Until then
   the 16 KB code-only cap is what stands, and it is the tighter of the two readings of §4 that
   remains defensible.

**Bitten, not asserted** (`s182-D1` — mechanical claims carry a probeable token):
`python3 knowledge/_validate_behaviour.py --selftest` (green; adds nine new bites: five on the
scanner's string/regex/division handling, two on the comment-vs-code delta, four on the
`consumes`-aware sum, and the pre-existing size and page-budget pads **converted from comment
padding to real code** — a comment pad would have silently stopped biting the moment the unit
changed, which is the first rot this amendment could have caused). Plus three named mutations in
the `_validate_fit_physics.py --mutate` house style: `code-pad` → RED · `comment-pad` → GREEN ·
`string-slash` → RED.

**Declared limitation.** `code_only()` is a hand-rolled scanner, not a JS parser. It tracks string
and regex-literal state so `"http://x"` and `/a\/\/b/` are never read as comments, and it uses the
standard previous-significant-token heuristic for regex-vs-division. A regex opened immediately
after a keyword-like token outside `_KW_BEFORE_REGEX` would be mis-scanned. The failure mode errs
toward a **larger** figure (a stray tail counted as code), never a smaller one, so the gate cannot
be evaded by it. Every construct in the live canon sources is covered.

Node: ADR-0015-A3
Edges: supersedes(ADR-0015, claim=size-clause-unit-becomes-code-only) · supersedes(ADR-0015-A1, claim=page-budget-value-32-reads-34-and-sum-becomes-per-member) · supersedes(ADR-0015-A2, claim=budgets-are-no-longer-untouched-consumes-now-drives-the-page-sum) · relates(#96-D5, scope=the-prose-this-amendment-reconciles)

## Consequences

- The gate work rides the Chart-line exemplar build: size + pattern checks + sync `--check` +
  selftest, wired into `_build_all` (selftests-are-build-steps rule).
- The showroom needs no change: snippet `<script>` already executes inside pane payloads (the
  review-overlay precedent).
- Legend/toolbar controls become pressables with a **quiet utility state** — deliberately NOT
  B-D7 press physics (chart-revisit Q5; flagged to Dave, standing).
- When the theme builder arrives, behaviour joins the partial bin like everything else — one more
  organ the tool absorbs (see `_FUTURE-STATE` theme-generator entry).

## Amendment 4 — 2026-09-08 (#260, Dave, `s260-D1`): the engine core is a SHARED payload, priced ONCE PER PAGE

**Ruling:** `s260-D1` in `knowledge/_rulings.json`. Dave's words: *"11 but I feel like the budget might have to be raised at some point in the future"* — option 1 of the three shapes #259 handed back, with the caveat carried as a caveat and not as a raise.

**What it resolves.** #259 landed the renderer `knowledge/canon/dv-render.js` (9,309 code-only bytes) and six type partials that compose it. Amendment 3's `consumes`-aware sum priced the core into EVERY member that lists it, so `Chart-combo` read 43,518 and `Chart-donut` 37,787 against the 34,816 budget — not fat pages, but the same 9,309 bytes charged five times over. The core is one payload however many types compose it.

**What changes.** A `$behaviour` entry may carry `"shared": true` (today: `dv-render` only). A shared source is EXCLUDED from each member's page figure and REPORTED on its own line as "priced once per page". It still owes the per-source 16 KB cap — legibility is not amortised. ⛔ Only the registry may mark a behaviour shared; a member's `consumes` cannot declare its own way out of the sum. Bites in `_validate_behaviour.py --selftest`: a member composing two shared sources is not charged for them; marking ONE source shared does not excuse the others; a shared name that is not a group behaviour is refused.

**What does NOT change.** `MAX_BYTES` 16,384 and `PAGE_BYTES` 34,816 are UNMOVED. Dave's caveat that the budget "might have to be raised at some point" is recorded and is a SEPARATE future ruling, not a licence. Measured after: `Chart-combo` 34,209 (607 spare), `Chart-donut` 28,478.
