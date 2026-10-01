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

Steps three (gates as a service, `gates/`), four (the chooser, `chooser/`), the mock fixtures (`mock/`) and the
record per screen (`records/`) are Friday's lanes (C3, C4, CV); step two (the renderer) is superseded by `s311-D9`:
the renderer that draws an A2UI screen is the HTML emitter of the new architecture.
