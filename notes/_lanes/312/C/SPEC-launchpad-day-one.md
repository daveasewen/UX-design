# Launchpad, day one — the build spec the three build lanes build to

Written by #311 lane CS (Fable, cloud) on Wed 2026-09-30 for the overnight wave (`notes/_lanes/312/OVERNIGHT-CHAINS.md`, addendum 22:20 BST) from `notes/_lanes/312/C/BRIEF.md`. It is one drawing for lanes C1 (the catalogue), C3 (gates as a service), C4 (the chooser), C2 (the renderer, a stretch) and CV (the verifier). It invents nothing the proposal did not say: every shape here is lifted from `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` (§ The proof of concept, § The build path, § Four mock roles, § Worked example), from the R5 probe (`notes/_subreports/2026-09-26-304-R5-mcp-probe.md`, files under `notes/_lanes/304/R5/`) and from the rulings named in § 1. Where a build lane needs a name or a number that neither source gives, this page gives one and marks it **[spec]**; a build lane may change a **[spec]** choice only by saying so in its report. Nothing on this page is Dave's ruling; nothing here goes to him tonight (the brief: "Dave's one moment: none tomorrow").

The name Launchpad is the folder's name and this page's; it never appears on shared material (`s305-D48`, store row W-305n6).

## 1 · What binds, and what tonight is

Ruled and read by every lane:

- `s305-D45` route B: Apollo as an A2UI catalogue over MCP, MCP Apps the fallback shell.
- `s305-D46` the PoC as written: the landing dashboard, about 15 parts, mock data, four best-guess roles, show and prepare only. `s305-D49`: money screens data-only; the PoC moves no money.
- `s305-D47` Jev as a ranker behind a switch that is off by default, for the PoC; `s294-D10` still in force: nothing may require Jev.
- `s305-D50` start once schema calls 14–19 are in the tree: `s305-D15`, `s305-D16`, `s305-D21`, `s305-D22`, `s305-D23`, `s305-D54` read enacted; `s305-D17`, `s305-D18`, `s305-D19`, `s305-D58` are lane C0's tonight. Rule 5 of the addendum: C1 builds on C0's **committed** schema sha, never on its working tree.
- `s305-D20` the five beta dashboard parts go into the catalogue, marked as proposals; every screen's record names any it used; Dave's rider verbatim: "I guess this is safe as evidence not as a tracing source".
- `s305-D51` hosts first (catalogue and renderer); `s305-D53` the build-ready test is later, not tonight.

Tonight builds the proposal's steps one (catalogue), three (gates as a service) and four (chooser); step two (renderer) is a stretch nothing depends on. Steps five (the dashboard end to end: mock data behind the tools, the two hosts, the record written) and six (Jev side by side) are **not** tonight. This page still fixes the tool surface and the record now, because steps one, three and four return the material step five writes, and three lanes building to three different shapes is the risk the brief names.

## 2 · Folder layout **[spec]**

Everything new lives under `apollo-launchpad/`, job C's only folder. Nothing in the pack's ship set changes; no new build step is wired into `_build_all.py`; nothing under `knowledge/` is edited by C1, C3 or C4 (a canon change C3 wants is named under Found-not-fixed, see § 7).

```
apollo-launchpad/
  README.md                 what this is, how to run each selftest, the A2UI dependency
  requirements.txt          jsonschema==4.23.0 (draft 2020-12; the seat's own is 3.2), referencing
  catalogue/                step one (C1)
    gen_catalogue.py        the generator, grown from notes/_lanes/304/R5/gen_catalogue.py
    validate_a2ui.py        the harness, grown from R5's (C1, E0–E3, mutation set)
    selftest.py
    out/catalogue-dashboard.json     the PoC catalogue (committed: it is the API)
    out/catalogue-report.json        losses, tallies, publication map (committed)
    a2ui-v0.9.1/            the spec files as R5 fetched them, with FETCHED.txt (copied, hashes unchanged)
  gates/                    step three (C3)
    gate_mem.py             the in-memory gate, grown from R5's
    server.py               the MCP stdio server exposing the gate tools of § 6
    selftest.py
  chooser/                  step four (C4)
    when_eval.py            the evaluator, grown from R5's (variant B is now the rule, s305-D22)
    entitle.py              role × tool × scope, the grant/refuse table of § 6
    rank.py                 the ranker seam: the fixed order, and the off-by-default Jev hook
    selftest.py
  mock/                     shared fixtures (C4 writes them; C1, C3, CV read them)
    roles.json              the four mock banking roles and their grants (§ 6)
    data.json               the mock company data behind the worked example (§ 9)
    requests.json           the worked example's two requests as intent contexts (§ 9)
  records/                  one JSON per screen sent (§ 8); empty tonight but for CV's runs
  renderer/                 step two (C2, stretch): render.js grown from knowledge/canon/dv-render.js
  hosts/                    step five, not tonight: mcp-apps/ and a2ui-host/
```

Python 3 only, stdlib except where `requirements.txt` says. The venv is `$HOME/.launchpad-venv` at the seat (**[spec]**, replacing R5's `$HOME/.r5venv`, which dies with the VM) and lives outside the repo; the cloud clone makes its own. Every script runs under `PYTHONDONTWRITEBYTECODE=1` (R5 refreshed two caches under `knowledge/__pycache__` by forgetting this).

## 3 · Words, so three lanes mean the same thing

- **part** — one Apollo component, one meta, one catalogue entry. Its A2UI `component` name is the slug in PascalCase, as R5 did (`chart-line` → `ChartLine`).
- **setting** — an A2UI property that takes a kind of data; **slot** — an A2UI property that takes another part by what it provides (`s305-D19`; the house rule under `s305-D58`: a slot takes a kind of part, a setting takes a kind of data). **data shape** — one of the 23 in `knowledge/shapes.json`; a data setting is bound to one.
- **when-rule** — the meta's `when`, gate half before the dash, prose after; the gate is what the evaluator parses.
- **provides role** — a slug from `knowledge/roles.json` (`headline-metric`, `record-list`, `page-frame` …): what a slot asks for. **mock role** — one of the four banking roles of § 6. The two never mix; a lane that writes `role` must say which.
- **request** — what the agent sends: a mock role, a question, a clock (`asked_at`). **intent context** — the flat dict the chooser reads, keyed by `knowledge/when-fields.json` names (44 fields today), derived from the request and the data fetched.
- **surface** — the A2UI v0.9.1 `updateComponents` message (plus `beginRendering`) that describes one screen as data. **page** — the canon HTML the renderer draws from a surface (step two); tonight's stand-in is R5's splice of reference snippets.
- **screen** — one answer to one request: a surface, its record, and (when step two exists) its page.
- **record** — the per-screen JSON of § 8.

## 4 · The dashboard part set

The proposal says "about 15 parts: headline figures, status, lists, a few charts, the page frame". Nobody has listed fifteen by name; the probe derived 18 by script (the union of the `$composes` of template-dashboard and template-dashboard-bento, the worked example's line chart and list, and the #261 metas) and said "the dashboard's parts are a derived set, not Dave's list". This page keeps the derivation and applies what changed since 26 September:

| kind (proposal's words) | part (slug) | status in the meta | note |
|---|---|---|---|
| page frame | `app-shell-top-nav` | PROPOSED #210 (beta) | the frame; its `content` slot takes one child, the wall |
| page frame | `template-dashboard-bento` | PROPOSED #231 (beta) | **the wall** that holds the tiles (`s305-D18`); the tiles slot's name is C0's |
| page frame | `navigations`, `breadcrumbs`, `headers`, `footer` (beta #261), `layout-utilities` (beta #204) | | frame furniture; `layout-utilities` stays in the set as the probe derived it but is not the container (`s305-D18` chose the wall) |
| headline figures | `metric` | ruled `s308-D42`, built #309 | **replaces** `stat-card` and `kpi-tile`, which are now aliases of it (`aliasOf: component:metric`, readings "without trend" / "with trend"); an alias meta holds no spec, so the generator emits the block once and lists both alias slugs on it |
| status | `status-indicator` | stable | |
| lists | `list-items`, `summary`, `data-grid` | stable | data-grid has its when-rule and `needs` since `s305-D23` |
| charts | `chart-line`, `chart-bar`, `legend` (beta #261) | stable / beta | chart-line's two clauses landed (`s305-D21`) |
| controls | `button`, `filter-toolbar-bar` | stable | |
| dropped | `view-options` | deprecated | never eligible (its when-rule is NEVER); not published |

That is 17 parts published (18 derived − view-options − stat-card − kpi-tile + metric + template-dashboard-bento). C1 derives the set by script, as R5 did, from the metas at C0's sha, prints it, and the count in its report is the script's, not this table's. The five beta parts publish marked `x-apollo.proposal: true` (`s305-D20`); the record names any a screen used.

## 5 · Step one · the catalogue's shape (C1)

The catalogue is the API. Its shape copies the official A2UI basic catalogue, as R5 did and validated 137/137: `{catalogId, components, $defs}`, each entry `allOf[ComponentCommon, CatalogComponentCommon, {component: const, props…}]` with `unevaluatedProperties: false`. Everything Apollo knows sits under one `x-apollo` annotation per entry (the spec ignores unknown `x-` keys; R5 proved the metaschema accepts it).

`catalogId` **[spec]**: `https://apollo.invalid/catalogs/apollo-launchpad/v0.1.0/catalog.json` — the reserved domain stays until a host is real; the real domain is a later question, not tonight's. The version is API-like, per Google's guidance the proposal quotes: `v0.1.0` for the first PoC catalogue; the generator bumps the patch when any entry's bytes change and writes `x-apollo.catalogue.sha256` (of the canonical JSON) beside it, so the record can pin a screen to a catalogue by hash as well as by version. The catalogue is built from the metas at one git sha, which it names in `x-apollo.catalogue.metas_sha`.

Per entry, in this order, from the meta:

1. `component` const (PascalCase slug); `description` = the meta's `purpose`, then " When: " + the when-rule's gate half (R5's form).
2. **Settings** as A2UI properties: every meta prop and every data setting. A data setting carries `x-apollo.shape` = its data shape address, and is typed as A2UI data (`DynamicString`/`DynamicNumber`/`DynamicBoolean`, or an object for a series) — never as a `ComponentId`. The `s305-D19` sort (16 became settings, 7 stayed slots) and the `s305-D58` four are read from C0's committed metas, not from this page.
3. **The part's own words** as settings (`s305-D17`): whatever fields C0 adds to the 45 parts (the decision page illustrates `label`, `title`, `items`, `rows`, `trail`). C1 reads the names from the schema at C0's sha; it does not guess them. If C0's commit is not in the tree when C1 starts, C1 stops and says so (addendum rule 5).
4. **Slots** as `ComponentId` (one child) or `ComponentId[]` (several), with `x-apollo.accepts` = the meta's `accepts` (by tier or capability, `s140-D1`). A2UI cannot say what a slot accepts (R5); Apollo's gate enforces it (§ 7, check S6). The wall's tiles slot is the one `ComponentId[]` in the set.
5. `x-apollo`: `level`, `status`, `proposal` (true for beta, `s305-D20`), `provides`, `answers`, `shape`, `span`, `priority`, `when: {gate, prose}`, `needs` (data-grid), `variants`, `states` (the `s305-D15` list, one sentence each), `slots.accepts`, `a11y: {role, sc}`, `snippet`, `rulings` (from the reader's own `governs_for`/`obeys_for`, never re-implemented), `aliases` (metric: `["stat-card","kpi-tile"]`).
6. Required: a required slot is `required`; a data setting whose shape is not `no-data × …` is required; own-words fields are required when the meta says so.

Not published: deprecated parts; anything the meta schema rejects (the catalogue never publishes drift: R5's L2 rule; with `s305-D15`/`D16` in the tree the expected L2 count for the set is 17 of 17, and C1 reports the measured one). `catalogue-report.json` keeps every loss line as R5 did (`G-SLOT-PROP-SAME-NAME` should read 0 after `s305-D19`/`D58`; C1 reports the number).

The generator also writes `out/catalogue-all.json` for all parts as a by-product (R5 did; it costs 1.6 s) but nothing tonight reads it.

## 6 · The tool surface

One MCP server over stdio (`s305-D45`: MCP is the wire). Tool names are plain words from the proposal's role table, snake_cased **[spec]**. Every tool call carries the mock role; the server checks role × tool × scope **before any data is fetched**, and writes every grant and refusal into the screen's record (proposal § How it is enforced). The four mock roles are the proposal's, verbatim in `mock/roles.json`:

| mock role (`mock/roles.json` slug) | side | tools it may call | data it may see (scope) |
|---|---|---|---|
| `corporate-treasurer` | client | `dashboard` · `positions` · `payments_queue` · `prepare_approval` | own company's accounts, all entities; payments awaiting approval up to the mock limit of **£500,000**; anything above needs a second approver |
| `relationship-manager` | bank | `dashboard` · `positions` (summary) · `client_book` | own book of client companies, balances at summary level only; no payment detail; cannot prepare approvals |
| `operations-analyst` | bank | `dashboard` · `payments_queue` (status only) · `exceptions` | payments in their region's queue, by stage; repairs and exceptions in full; no balances; cannot prepare approvals |
| `auditor` | read only | `dashboard` · `audit_record` | the records of screens sent and decisions made; no live balances or payments; cannot call anything that prepares or changes |

Scopes are strings the server compares, **[spec]** names: `positions: all-entities | summary`, `payments_queue: full | status-only`, `prepare_approval: up-to-limit` (limit 500000 GBP; a payment above it is returned flagged `second-approver`, never prepared), `exceptions: full`, `client_book: own-book`, `audit_record: read`. A tool not in the role's row is refused with reason `tool-not-granted`; a scope the role lacks is refused with `scope-not-granted`.

The data tools (step five, not built tonight; C4's `entitle.py` answers for them tonight and returns the grant/refuse rows):

- `positions(role)` → balances by entity (shape `rows × name-value-pairs`), plus today's cash position and its delta (shape `one-measure × value-and-delta`) and the 30-day series (`time-series × 1–5-series`).
- `payments_queue(role)` → payments awaiting approval (full) or the region's queue by stage (status only): records for `list-items`/`data-grid`, and `categories × series` for the bar chart.
- `prepare_approval(role, payment_id)` → prepares, never executes (`s305-D49`); above the limit returns the second-approver flag.
- `client_book(role)`, `exceptions(role)`, `audit_record(role, screen_id)` → as the table says.
- `dashboard(role, question, asked_at)` → one screen: runs choose → entitle → gate → send, returns `{surface, record_id}` or a refusal with the gate's reasons ("fails: refused, nothing is sent").

The Launchpad tools built tonight, each also callable on its own so CV can drive them:

- `catalogue()` → `{catalogId, version, sha256, components: [names]}` (C1).
- `choose(role, context)` → § 7's eligible list with reasons and the grant/refuse rows (C4).
- `gate_surface(surface)` and `gate_page(html)` → § 7's verdict object (C3). A screen in memory, in and out; no file written, no file read after warm-up (R5 T3: 0 writes, 0 reads).

Time triggers ("cut-offs and month end") act on **what is shown**, not on eligibility: `mock/data.json` carries the cut-off clock and the month-end date; the server derives the status part's words ("Cut-off in 2 hours") from `asked_at`. `when-fields.json` has no time field, so the chooser does not read the clock tonight; whether it should is a later question (§ 11).

## 7 · Step three · gates as a service (C3) and step four · the chooser (C4)

### The gate

`gate_mem.py` grows R5's two layers and returns one verdict object **[spec]**:

```
{ "verdict": "pass" | "fail",
  "checks": [ {"id": "S1", "name": "…", "result": "pass"|"fail"|"unmeasured"|"n/a", "reasons": [ "…" ]} … ],
  "timing_ms": {"surface": n, "page": n, "total": n},
  "catalogue": {"version": "v0.1.0", "sha256": "…"} }
```

Surface layer, on the A2UI messages against our catalogue (R5's list, kept): S1 message valid against `server_to_client.json` with `catalog.json` resolved to ours; S2 each part valid against its own entry (readable reasons, not `oneOf`'s); S3 one root; S4 unique ids; S5 child references resolve; S6 a slot's children provide what `x-apollo.accepts` asks (the check A2UI cannot make); S7 no deprecated part; S8 a state value inside the entry's `states`; S9 a data setting's value matches its shape's arity (a `time-series × 1–5-series` with six series fails).

Page layer, on the page string (tonight R5's splice stand-in; step two's output when it exists): the static checks of `knowledge/_validate_screen.py` that take a string today, called **in memory**: P1 a11y via `_validate_a11y` (target size, reduced motion **per part** by the splice markers, `s305-D54` enacted); P2 composition via `_validate_composition.check(html)` (C9 span legality blocks, C1/C7/C8/C4 advisory, as the disk runner does); P3 icon source via `_validate_icons` on `markup_only(html)`. P4 compose (`_validate_compose.check_screen(path)`) and P0 receipt take a path today: C3 writes the page to `/dev/shm` for those two only, reports that as the one file write, and names the split it wants under Found-not-fixed (a `check_text()` for each, three lines, like the one the probe named for a11y). The render leg (state-contrast, geometry, own-size) is deferred by the brief; C3 does not run it, but times one cold run of `_validate_screen.py --render` on one dashboard page at the seat if a seat is free, else reports UNMEASURED with the price.

`server.py` serves `gate_surface` and `gate_page` over stdio with the MCP tool schema (input: the JSON; output: the verdict object). One round trip is timed and reported.

### The chooser

`when_eval.py` grows R5's evaluator (`notes/_lanes/304/R5/SPEC-when-evaluator.md` is the base; its six steps stand) with what was ruled since: variant B is the rule (`s305-D22`: the part's own `answers` and `shape` are claims beside the when-rule); data-grid's `needs` is a field (`s305-D23`); chart-line's two clauses are in the meta (`s305-D21`). Three-valued clauses; a part is out only when its gate is false; rank by true claims, then `priority`, then slug. Aliases: `stat-card` and `kpi-tile` resolve to `metric` and the reading (`without trend` / `with trend`) becomes `metric`'s `spark` slot filled or empty, decided by whether a series exists in the data (metric's own when-rule says so).

`entitle.py` runs **before** the evaluator: it takes the mock role and the parts' data needs (each part's shape → which tool supplies it, a small table in `mock/roles.json` **[spec]**: `positions` supplies `one-measure × value-and-delta`, `time-series × 1–5-series`, `rows × name-value-pairs`; `payments_queue` supplies the records and `categories × series`; `exceptions` supplies its records; `no-data × …` needs nothing). A part whose tool was refused is out **before** choosing ("refused data never reaches the chooser"), and the refusal is a row in the result.

`choose()` returns **[spec]**:

```
{ "role": "operations-analyst", "context": {…},
  "eligible": [ {"part": "chart-bar", "rank": 1, "true_claims": 2, "priority": 60, "reasons": ["shape = categories × series", "answers = comparison"]} … ],
  "not_chosen": [ {"part": "metric", "why": "positions refused for this role"}, {"part": "chart-candlestick", "why": "gate false: shape != periods × ohlc"} … ],
  "grants": [ {"tool": "payments_queue", "scope": "status-only", "allowed": true}, {"tool": "positions", "scope": null, "allowed": false, "reason": "tool-not-granted"} … ],
  "ranker": {"switch": "off", "answer": null, "fallback": "rules-order"} }
```

`rank.py` is the seam: `rank(eligible, context, switch)`; with the switch off (the default, `s305-D47`) it returns the evaluator's order untouched and never imports `knowledge/_jev.py`. With it on it may only re-order the eligible list, never add to it, under a time limit, falling back to the rules' order and saying so in `ranker.fallback`. Tonight the on-branch is a stub that raises `NotImplemented` with the two words "step six"; `_jev.py` is not called anywhere (selftest asserts no import and no socket).

## 8 · The record per screen

One JSON per screen under `records/<screen_id>.json`, `screen_id` = `<asked_at ISO>-<role>-<8 hex of the surface's sha256>` **[spec]**. Fields, every one from the proposal's own sentences ("Catalogue version, parts used, rulings obeyed", "every grant and every refusal … role, tool, scope, allowed or refused", "the record keeps Jev's answer beside the screen", "a screen replays from the record", `s305-D20`'s "naming any it used"):

```
{ "screen_id", "asked_at", "question", "role",
  "catalogue": {"id", "version", "sha256", "metas_sha"},
  "parts": [ {"id", "component", "slug", "proposal": bool, "provides"} ],
  "rulings_obeyed": [ "s…", … ]            (the union of the used parts' x-apollo.rulings)
  "entitlement": [ {"tool", "scope", "allowed", "reason"} ],
  "not_chosen": [ {"part", "why"} ],
  "gate": <the § 7 verdict object>,
  "ranker": {"switch", "answer", "fallback"},
  "host": "mcp-apps" | "a2ui-host" | "none",
  "surface_sha256", "surface": <the messages, so the screen replays without asking again> }
```

The proposal says the graph keeps the record; how a record becomes a node in `knowledge/_kg*` is not tonight's (the KG build is offline, 107 s) and is listed in § 11. Tonight the file is the record.

## 9 · The worked example is the shared fixture

Both requests are the proposal's, verbatim: **"What needs my attention this morning?"**, at **09:10 on month end, two hours before the payments cut-off** (so `mock/data.json` puts the cut-off at 11:10 and marks the day month end). C4 writes `mock/requests.json` with the two intent contexts and `mock/data.json`; the counts and shapes below are the proposal's and must hold; the figures inside (balances, names, amounts) are mock and the lane's to type, except the limit (£500,000) and that exactly one of the three payments is above it.

Corporate treasurer — expected parts: `metric` (cash position today with the change since yesterday: `one-measure × value-and-delta`, spark empty), `status-indicator` (cut-off in 2 hours), `list-items` (3 payments awaiting approval: two within the limit, one flagged for a second approver — `needs = none`, so the list, not the grid, `s274-D6`), `chart-line` (balance over the last 30 days: `time-series × 1–5-series`, one series, same units). Grants: positions all-entities · payments_queue full · prepare_approval up-to-limit. Four tiles in the wall, inside the frame.

Operations analyst — expected parts: `metric` (5 payments in repair), `status-indicator` (cut-off in 2 hours), `list-items` (exceptions to clear, oldest first), `chart-bar` (region's queue by stage: `categories × series`). Not chosen: the cash position, "positions refused for this role". Grants: positions refused · payments_queue status-only · exceptions full.

The same request, two roles, two different correct screens, the reasons on record: that is the sentence CV checks.

## 10 · Step two · the renderer (C2, a stretch)

Grown from `knowledge/canon/dv-render.js`, which already draws charts from a data spec. Input: a surface (§ 3) plus the catalogue; output: canon markup, the same classes the reference snippets use, no new CSS (canon.css is A1's tonight and unchanged by C2). One file, so the same script later runs inside the MCP Apps frame (proposal: "The same file runs inside the MCP Apps frame"). The check: the treasurer's screen rendered from § 9's surface, put through `gate_page`, and screenshotted beside the parts' reference snippets at the seat; "matches its reference, by eye and by gate" is the proposal's test, and the by-eye half is Dave's later, not tonight's. If C2 gets only as far as the four tile parts without the wall, it says so; nothing depends on it.

## 11 · Tests each step must pass (the lane's selftest, run at the seat or in its clone, and pasted into its report)

Step one (C1):
- T1.1 the document validates against the 2020-12 metaschema (R5's C1) and each entry passes E0–E3 (entry is a valid schema; a minimal instance validates; an unknown property is refused; an `updateComponents` message validates with `catalog.json` resolved to ours). Baseline: 137/137 and 18/18 at the probe; expected tonight: every published part.
- T1.2 the five one-change mutations of `validate_mutations.py` are all caught (R5: 5/5 after the E0 fix).
- T1.3 L2 = L1 for the published set (nothing published breaks the schema); the report prints L1/L2/L3 by R5's `summarise_catalogue.py` rule and the reasons for any part short of L3.
- T1.4 no `G-SLOT-PROP-SAME-NAME` loss on the 23 parts `s305-D19`/`D58` settled; the count is printed.
- T1.5 `metric` carries `aliases: ["stat-card","kpi-tile"]` and neither alias is its own entry.
- T1.6 two consecutive runs on the same metas sha give byte-identical output (R5 proved this; the `metas_sha` and `sha256` fields make it checkable).
- T1.7 the generator's own time, n=3, and the reserved-domain `catalogId`.

Step three (C3):
- T3.1 same verdict as the disk gate on all 137 reference snippets (R5: 137/137) and on the six planted pages (R5: 6/6, four FAILs) — comparing fails, warns, notes and every control verdict.
- T3.2 the fourteen planted defects of R5 T2 all refused by name, plus three new ones: a slot child that does not provide what `accepts` asks (S6); a series count outside the shape's arity (S9); two parts spliced where only one has a reduced-motion block and the other animates — refused **per part** (`s305-D54`), which R5's K1 could not do.
- T3.3 a clean four-tile surface passes at the surface layer, and the treasurer's spliced page passes at the page layer.
- T3.4 warm per-surface time, n=25, median and max (R5: 61 ms / 70 ms); cold time; the audit hook reports 0 writes and 0 file reads for `gate_surface` and for `gate_page` other than the declared `/dev/shm` write for P0/P4.
- T3.5 one stdio round trip through `server.py` for each tool, timed.
- T3.6 `--render` on one page: timed once at the seat, or UNMEASURED with the price.

Step four (C4):
- T4.1 R5's selftest bites (15/15) still bite.
- T4.2 the W1–W18 table re-run with variant B as the rule: expected 19 of 20 (`s305-D21`'s own figure), every miss named. `kpi-tile`/`stat-card` expectations become `metric` with/without spark.
- T4.3 the worked example: both § 9 screens come back with exactly the expected parts and the expected `not_chosen` row for the analyst; `grants` match the § 6 table row for row; the treasurer's third payment carries `second-approver`.
- T4.4 every role × every tool: the 4 × 7 grant matrix printed from `entitle.py` and equal to § 6's table (the auditor is refused `positions`, `payments_queue`, `prepare_approval`; the treasurer is refused `client_book`, `exceptions`, `audit_record`; and so on).
- T4.5 determinism: the same request twice gives byte-identical `choose()` output; median time over n=25 (R5: 0.27 ms).
- T4.6 with the switch off, `knowledge/_jev.py` is never imported (assert on `sys.modules`) and no socket is opened; with the switch on, the stub raises and the result still carries `fallback: "rules-order"`.

Every lane: `python3 knowledge/_wrap_commit.py unlock --tag 311-<lane>` after gate runs; `knowledge/_tests/test_gates.py` green at the seat before its commit (addendum rule 4); the report at `notes/_subreports/2026-10-01-311-<lane>-<topic>.md` with the `COUNTS:` line, a born-closed store row, `## Found, not fixed` and `## Ruling-shaped questions`.

## 12 · Dependencies and seats

- C1, C3, C4 run in the cloud workspace on a /tmp clone (the brief), one clone at a time under `/tmp/apollo-prepush.lock`, cleared with `rm -rf` when done. Their outputs are committed at the seat, inside `/tmp/apollo-commit.lock`, own paths only: `apollo-launchpad/<their folder>/**`, `apollo-launchpad/mock/**` (C4), `apollo-launchpad/README.md` and `requirements.txt` (C1 writes them; C3 and C4 append their sections in their own commits).
- jsonschema 4.23 is a launchpad dependency, not a repo one: the gates under `knowledge/` stay stdlib; `gate_mem.py` imports the launchpad venv's jsonschema for the surface layer only and the repo's own modules for the page layer.
- C1 waits for C0's schema commit sha and names it. C3 and C4 do not need C0 (they read when-rules, shapes and snippets that are already in the tree) and may start at once; C4's alias resolution reads `aliasOf`, already in the tree at 879f9aae.
- The render leg needs the seat (`ensure_env.sh` + `seat_env.sh`, `executable_path=$RENDER_SHELL`); nothing else here does.

## 13 · What this page did not decide, and who decides it later

None of these is for Dave tonight (the brief); they are for the next sitting page, priced by the lanes' measurements:

1. The real `catalogId` domain and the versioning policy beyond patch-on-change.
2. How a screen's record becomes a graph node (kind, edges to parts and rulings) — the proposal's "the graph keeps a record".
3. A time field for when-rules (cut-offs, month end) so the chooser, not only the data, can read the clock.
4. The three `check_text()` splits under `knowledge/` (compose, receipt, and the icon gate's builder) that would let the page layer run with zero file writes — canon changes, so a later lane with a verifier.
5. Whether `layout-utilities` stays in the PoC set now that the wall is the container.
