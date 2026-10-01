# apollo-launchpad

The proof of concept of Apollo as an A2UI catalogue over MCP (route B, `s305-D45`): the landing dashboard,
about fifteen parts, mock data, four best-guess roles, show and prepare only (`s305-D46`, `s305-D49`). The
build spec every step builds to is `notes/_lanes/312/C/SPEC-launchpad-day-one.md`; the proposal is
`notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`. The name Launchpad is this folder's and never appears on
shared material (`s305-D48`).

Nothing here is in the pack's ship set; no build step is wired into `knowledge/_build_all.py`; nothing under
`knowledge/` is edited from here. Python 3, stdlib except `requirements.txt`. Run every script with
`PYTHONDONTWRITEBYTECODE=1`.

## The A2UI dependency

A2UI v0.9.1 (`catalogue/a2ui-v0.9.1/`, the spec files as fetched on 2026-09-26, hashes in `FETCHED.txt`) is
JSON Schema draft 2020-12. The seat's own python3 has jsonschema 3.2 (draft-7 only), so the A2UI checks run
in a venv outside the repo:

    python3 -m venv $HOME/.launchpad-venv
    $HOME/.launchpad-venv/bin/pip install -r apollo-launchpad/requirements.txt

The generator itself runs on either python (it validates the metas against `meta.schema.json`, draft-7).

## Step one · the catalogue (`catalogue/`, #312 lane C1)

From the metas of the dashboard parts to A2UI v0.9.1 catalogue entries with their when-rules, versioned like
an API. The metas are the source; `catalogue/out/catalogue-dashboard.json` is the API and is committed.

    PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/catalogue/gen_catalogue.py            # build out/
    PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/catalogue/gen_catalogue.py --check    # the gate: exit 1 when out/ is stale
    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/catalogue/validate_a2ui.py             # C1, C2, E0–E4, N1, N2
    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/catalogue/validate_a2ui.py --mutations # five breaks, all caught
    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/catalogue/selftest.py                  # T1.0–T1.9, writes nothing

- The dashboard set is derived, not typed: the `$composes` of `template-dashboard` and `template-dashboard-bento`,
  the worked example's `chart-line` and `list-items`, the #261 dashboard metas, and the wall itself (`s305-D18`);
  aliases resolve to their owner (`stat-card`, `kpi-tile` → `metric`, `s210-D5`), a part whose `when` is NEVER
  drops out. The derivation is printed in `catalogue-report.json` under `dashboard`.
- Per entry: `component` const (the slug in PascalCase); `description` = purpose + " When: " + the gate half of
  the when-rule; every meta setting as an A2UI property (a data setting is A2UI data with `x-apollo.shape`,
  never a `ComponentId`, `s305-D19`; a part's own words are settings marked `x-apollo.ownText`, `s305-D17`);
  every slot as `ComponentId` or `ChildList` with `x-apollo.accepts` (A2UI cannot say what a slot accepts; the
  gate does); one `x-apollo` block per entry (level, status, proposal, provides, answers, shape, span, priority,
  when {gate, prose, fields}, variants, states, slots, a11y, snippet, rulings, aliases, and `spec` when the meta
  carries `s311-D4`'s anatomy/states/emits/bindings). Required: a required slot; a data setting with a data shape
  and no default; an own-words setting with no default.
- Not published: alias metas (listed on the owner's `aliases`), deprecated parts, any meta `meta.schema.json`
  rejects (the catalogue never publishes drift). Every loss is a line in `catalogue-report.json`.
- Versioning: `catalogId` = `https://apollo.invalid/catalogs/apollo-launchpad/dashboard/<version>/catalog.json`
  (reserved domain until a host is real). `x-apollo.catalogue` carries `version`, `sha256` (of the canonical
  `components` + `$defs`), `metas_sha` (the git sha the metas were read at; `--metas-sha` overrides HEAD),
  `metas_sha256` (the metas' bytes) and `previous`. The patch bumps when any entry's bytes change; otherwise a
  re-run is byte-identical. The catalogue carries no clock.
- The gate: `gen_catalogue.py --check` refuses when the committed `out/` no longer matches the metas; `selftest.py`
  refuses when any of T1.0–T1.9 fails. Both exit non-zero; neither writes under the repo.

## Step three · gates as a service (`gates/`, #313 lane C3)

One screen in memory in, one verdict out, served as MCP tools over stdio. The surface layer needs the venv's
jsonschema (as the catalogue harness does); the page layer is the repo's own gates under `knowledge/`, called on
the string. Nothing under `knowledge/` is edited from here.

    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/gates/gate_mem.py <surface.json> [--splice]   # or <page.html>
    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/gates/server.py                               # the MCP server (a client spawns it)
    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/gates/selftest.py [--json]                    # T3.1–T3.6, writes nothing under the repo

- Tools: `gate_surface {surface, splice?}` and `gate_page {html}`; both return the spec's verdict object
  `{verdict, checks: [{id, name, result, reasons}], timing_ms, catalogue}`. Only a `fail` fails the verdict;
  `unmeasured` is said, never rounded. A refused screen is a successful call; a call that cannot run is `isError`.
- Surface layer S1–S9: messages against A2UI v0.9.1 with this catalogue; each part against its own entry; one root;
  unique ids; references resolve; a slot's children provide what the slot accepts (the wall's four kinds of tile,
  kept by `s313-D41`; a tier; a capability no registry can answer is UNMEASURED); no deprecated part; states; data
  within its shape's series count (a binding is resolved through the surface's own `updateDataModel`).
- Page layer P0–P4: receipt, accessibility (motion judged per part, `s305-D54`), composition, icon source, compose.
  Receipt and compose take a path today, so each page is written once to `/dev/shm` and removed: the one write.
- `gate_surface` with `splice` gates the page the surface stands for, made by splicing each part's reference markup
  (canon.css linked, behaviour loaded by address). It is a stand-in, not a renderer.
- Warm-up reads the catalogue, the spec, the snippets and the icon library once and builds the compose gate's
  canon memo (seconds, paid once per process); after it, `gate_surface` reads and writes no file.
- `gates/fixtures/` holds the worked example's two surfaces (treasurer, operations analyst) the selftest gates.

## Step four · the chooser (`chooser/`, #313 lane C4)

Given a mock role, a question, a clock and the items the agent asks to show, the chooser returns the screen's
parts with their reasons, every grant and refusal, and the ranker's record. Stdlib only; reads the catalogue,
`knowledge/` and `mock/`; writes nothing; no clock, no socket, no Jev.

    PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/chooser/choose.py treasurer-0910 --brief   # or analyst-0910; full JSON without --brief
    PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/chooser/entitle.py                         # the 4 × 7 grant matrix
    PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/chooser/selftest.py                        # T4.1–T4.8

- Order: entitle (role × tool × scope, before any data is read; a refused item is a `not_chosen` row naming the
  part it would have taken) → fetch (mock) → the item's intent context → the when-rules, variant B (`s305-D22`)
  → the ranker seam (off by default, `s305-D47`; never imports `knowledge/_jev.py`, `s294-D10`) → place: the
  part is a tile only if it provides one of the kinds the bento wall's `tiles` slot accepts (`s305-D18`; the
  four kept by `s313-D41`).
- `mock/roles.json` the four mock roles and grants (£500,000 limit); `mock/data.json` the worked example's data;
  `mock/requests.json` the two requests and three fixtures, with expectations written before the run.

The record per screen (`records/`) and the worked example end to end are the verifier's (CV); step two (the
renderer) is superseded by `s311-D9`: the renderer that draws an A2UI screen is the HTML emitter of the new
architecture.

## The worked example end to end (`verify/`, `records/`, #313 lane CV)

The two requests of the worked example (`mock/requests.json`) run through choose → compose → gate → record:
the chooser picks the parts, `verify/worked_example.py` composes the A2UI surface from the picks and the mock
data (a stand-in for the agent, not a renderer), the gate refuses or passes it in memory and again over stdio,
and the record of § 8 of the spec is written. Then five bad screens and one bad page go through the same gate.

    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/verify/worked_example.py           # prints, writes nothing
    PYTHONDONTWRITEBYTECODE=1 $HOME/.launchpad-venv/bin/python apollo-launchpad/verify/worked_example.py --write   # also writes records/

`BLKD` lines are steps the chain cannot take yet (data bound to the data model); they are neither a pass nor a fail.
