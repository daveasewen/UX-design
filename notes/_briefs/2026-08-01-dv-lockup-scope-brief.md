# dv-lockup scope brief — the reusable chart header partial (#67, D4 of #66-D6)

**Status:** SCOPED, not built — shape approved #66-D6 D4; build is its own wave, priced below.
**Owner:** agent builds, Dave rules the parameter set + any visual change.

## ⬛ RESHAPED IN CHAT #67 (Dave live, "well aligned" — reflect-back done, ledger line owed at wrap)

1. **Two-tier split (Dave's):** the PRODUCT molecules — what screens are built from — are the
   **legend** and the **controls/header cluster** only. **Toggle theme + Replay motion are
   review-harness chrome**, never part of final components; they move to the harness layer.
   (Dissolves the "donut has no Replay" question — moot.)
2. **Title (Dave's):** NOT its own molecule — it is the **one mandatory item** of the header
   cluster, a type-composite atom in a mandatory slot (research concurs: text-only molecules
   are not a common pattern; Carbon treats chart title as chart anatomy, not a component —
   sources in chat #67).
3. **Variability (agreed direction):** header-cluster + legend contents vary by chart type +
   data shape. **Rules are the record** (per-type declarations in the registry, A2-strict,
   absent = fail loud) · **inference is the clerk** (a derivation script reads the data shape
   and DRAFTS the declaration for Dave to ratify; unknown shape = loud refusal, never a
   default) · a consistency gate re-runs the same logic as a checker, findings to Dave.
   This is derivation-governance + measuring-tool-must-not-guess applied verbatim.
4. **Related, FLOATED (not this wave):** edit-mode's three data-entry paths (edit values ·
   values generator · CSV upload) → `_FUTURE-STATE.md` § Apollo edit mode, 2026-08-01.

## RESEARCHED (measured on the seven pro-formas, #67)

Header drift is real and countable (`grep` over `knowledge/snippets/Chart-*.reference.html`, #67):

| snippet | `dv-title t-cm-section-label` h3 | View as table | Toggle theme | Replay motion |
|---|---|---|---|---|
| bar | 5 | 5 | 1 | 1 |
| combo | 1 | 1 | 1 | 1 |
| donut | 1 | 2 | 1 | **0** |
| line | 2 | 3 | 1 | 1 |
| scatter | **0** | 2 | 1 | 1 |
| sparkline | **0** | 1 | 1 | 1 |

Three drift classes: (a) scatter + sparkline never adopted the `dv-title` composite —
their titles are bare `h2`/caption forms; (b) "View as table" count varies with
per-page chart count but its markup is hand-copied per chart; (c) donut has no
Replay motion control at all. Combo count of chart-blocks per page also varies, so
the partial must be per-chart-block, not per-page.

## MECHANISM (the approved shape, from the ratified pack)

- New **ADR-0013 partial**, working name `dv-lockup`: one header block per chart —
  title (type composite `t-cm-section-label` via the existing `dv-title` form),
  optional "View as table" toggle, optional theme/replay controls slot.
- **Parameterised by data-attributes** on the consuming block (e.g.
  `data-lockup-title`, `data-lockup-table`, `data-lockup-controls`), **registry-gated**
  in `component-types.json` — and under A2 permanent-strict (enacted #67, `75343e8`)
  every member's participation is a **declaration, never a default**.
- Rides `gen_component_partials.py` unchanged — markup+CSS injection only, **no JS**,
  so the behaviour-page budget (32,768/group, the unit is the injected-JS accounting —
  see the 30,007 B unit lesson, ledger § ★ #66/#67) is untouched *by design claim*.

## PROBED

- The grep table above is the probe for drift (named probe: `grep -o` over six title/
  control forms; a matched grep is a candidate, the counts were read per file).
- NOT probed: whether donut's missing Replay is intent or drift — **Dave's call at build**.
- NOT probed: CSS weight of the injected header per snippet — measure at build, per
  snippet, before the ratchet commits anything.

## FALSIFIER (what would kill this shape)

- If any header variant needs **JS** — ✅ PROBED #67, does not fire: the table toggle's
  script lives in `knowledge/canon/dv-behaviour.js` (`dv-tbl-toggle`, one shared handler),
  already centralised. The lockup adds zero JS; the group budget stays out of scope.
  (Probe: `grep -rln dv-tbl-toggle knowledge/canon/` — quoted match, not absence.)
- If the seven pro-formas' headers turn out to be **deliberately** divergent (register/
  temperature dials) rather than drifted — surface to Dave, don't normalise by fiat.

## PLAN stamp (price, for the build wave — not this session)

- Touches **all 7 pro-formas + generator + registry + type.css check** ⇒ its own wave
  with the ratchet, never a drive-by (ruling's own words).
- Estimate: one Sonnet sub wave + in-window replay + render-proof ≥2 widths + commit ≈
  **35–50K real tokens** incl. render sandbox re-stage if cold. Sequence: partial +
  registry first, then per-member adoption member-by-member with the ratchet, bar last
  (it has 5 header instances — the stress case).
- Open questions for Dave before build: (1) donut Replay — add or leave? (2) is the
  per-page multi-chart case one lockup per chart-block (proposed) — confirm; (3) name:
  `dv-lockup` stays or renames at ADR inscription.
