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
Edges: amends(ADR-0015, scope=size-clause-and-one-source-posture) · enables(DV-D11, scope=legend-model-needs-its-own-source)

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
Edges: amends(ADR-0015, scope=group-wide-injection-becomes-manifest-gated)

## Consequences

- The gate work rides the Chart-line exemplar build: size + pattern checks + sync `--check` +
  selftest, wired into `_build_all` (selftests-are-build-steps rule).
- The showroom needs no change: snippet `<script>` already executes inside pane payloads (the
  review-overlay precedent).
- Legend/toolbar controls become pressables with a **quiet utility state** — deliberately NOT
  B-D7 press physics (chart-revisit Q5; flagged to Dave, standing).
- When the theme builder arrives, behaviour joins the partial bin like everything else — one more
  organ the tool absorbs (see `_FUTURE-STATE` theme-generator entry).
