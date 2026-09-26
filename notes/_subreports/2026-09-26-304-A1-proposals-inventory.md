# #304 lane A1 — every proposed development of Apollo on record, and its true status

provenance: #304 lane A1 (Opus 5.5, read-only) · 2026-09-26 · for the Fable roadmap seat
status: observed (every status claim carries a receipt; estimates are labelled)
scratch: notes/_lanes/304/A1/ (inventory.json = 140 proposal-shaped files with first/last commit; doc2rulings.json; notenacted_cands.json)

Dave's ask, verbatim (15:33): "I think we need an analysis of all the proposed development of Apollo we already have and, check out the future state too. then lets layout a proposed roadmap so we can make some progress. Put together a plan, lets leverage some big pushes over this weekend that I can leave you to churn though, recommend the models, effort levels and subs structure you propose to get some work nailed by early next week. don't worry about token spend. lets get ripping, you know the usual instructions, watch the externalities, dependancies and test it hard :)"

---

## 0. The answer first

1. The ruling store cannot, on its own, say what is "ruled not enacted". Of 638 rulings, 424 carry the bare status `ruled` (measured: `json.load` over `rulings`, `status.strip().lower()=='ruled'`), and only 32 open with `ENACTED`. `s295-D2` (2026-09-21) made "the enacting lane stamps `status: enacted`" the rule, advisory and forward-only; it back-stamped only the eleven `s294-D*`. Every `ruled` row before #295 is therefore ambiguous by construction: many are enacted (receipts below), some are not. Any consumer that reads `status` reads a false backlog (the defect `s295-D2` names in its own text). A back-stamp lane is one of the highest-value, lowest-risk moves available (section 5, item 6).
2. Verified by probe against the tree, eleven rulings are genuinely RULED and NOT ENACTED today (section 2a). The most concrete: the console radius set `s245-D10` (ruled 2026-09-03, canon still carries the old values), the 44px blocking tier `s114-D6` and the marks blocking half `s116-D1` (both still `"warn"` in code), the notification borders `s135-D1`, the theme publish tier `s216-D1`, tokens-into-the-graph `s277-D12`, and the fifth KG step (`s269-D1` step 5) plus the two new entity kinds (`s269-D6`).
3. Five separate proposals are one undecided question — what Apollo actually hands to a developer or a host: the factory north-star (`W-329`, "is it build ready?"), `s216-D1` (minted theme-specific code), ADR-0008 (canonical core + automated adapters), `P-277-5` (NPM with Angular/React emitters, parked) and the Apollo-MCP proposal (an A2UI catalogue plus Apollo's own renderer). They overlap and none has been ruled against the others. This is the biggest duplicate cluster in the record.
4. The largest pile of built-but-unratified work is 27 Layer-2 organisms (3+4 app shells, 5+5 templates, 2+7 lock-ups…) built at #210 as "BUILT PROPOSED-NOT-RULED", parked in the store as `W-75`…`W-84` with Dave's eye owed on roughly 80+ named questions (the rows' own counts: 48 + 33, plus lane counts). The showroom and the metas disagree on their status (section 4).
5. The live strategic proposal is Apollo-MCP v2 (`notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`, "Status: a recommendation for you to rule on. Nothing here is decided."). It is untracked in git (no commit touches it — `git --no-optional-locks log -- <path>` empty), and it depends on three unbuilt KG items (lifecycle status per part, tokens at group grain, the delivery-shape ruling).

---

## 1. The inventory, by theme

Legend. PROPOSED = on the page for a ruling, none given. RULED-NOT-ENACTED = Dave's ruling in the store, not in the tree. PARTLY = some clauses in the tree. ENACTED = in the tree with a receipt. PARKED = explicitly parked with a home. SUPERSEDED = replaced by a later ruling or artefact. BANKED = his words filed, nothing ruled. HISTORY = dated record, no live claim.

Dates are the proposal's own date or first commit (`git --no-optional-locks log --format='%h %cs' -- <path>`, captured in inventory.json).

### 1.1 Strategy, product shape and the engine

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `archive/apollo-pipeline-spec_v0.1_2026-05-31.html`, `_v0.2_2026-06-20.html` | 05-31 / 06-20 | Apollo as an agentic design pipeline with its own orchestration tiers | SUPERSEDED | ADR-0005 (07-02, accepted) "the knowledge engine is the product; orchestration is inherited" |
| `digital-experience-transformation/strategy/00`–`05` | 07-01 | Team transformation thesis, operating model, prove → encode → shift → scale roadmap, people transition | PROPOSED (drafts) | `00_READ-FIRST_strategy-status.md:3` "drafts for your review, not settled positions"; last commit `be3c3647` 07-14 |
| ADR-0001…0004 | 05-31 | Own orchestration · open standards · per-stage knowledge · WCAG 2.2 AA | ENACTED as principle; ADR-0001 in effect SUPERSEDED by ADR-0005 | `knowledge/_ENACTMENT-REGISTER.md` rows (all UNPROVEN by that register's test, i.e. no executable check names them) |
| ADR-0005 knowledge-engine pivot | 07-02 | The KG/canon is the product | ENACTED | register verdict PROVEN (`_validate_receipt.py`, `gen_provenance_receipt.py`) |
| ADR-0006 flexing engine | 07-03 | One governed core, dial settings per work-type (factory mode etc.) | PARTLY — factory is the only mode built | ADR-0006 "Honesty — status of the mock"; `W-329` open |
| ADR-0008 canonical core + automated adapters | 07-20 | Consumers reached by generated adapters | PARTLY (partials generator only) | register verdict CLAIMED (`gen_component_partials.py`) — no React/Angular/other adapter exists; `P-277-5` parks the emitters |
| `notes/_VISION-northstar-front-end_2026-07-02.html`, `_VISION-iteration-machine_2026-07-03.html` | 07-02/03 | A front end for the engine; the iteration machine | PARKED (vision facades) | `_FUTURE-STATE.md:412` "Iteration-machine front-end mock — vision facade, proves alignment only" |
| `notes/_VISION-contextual-dashboard_2026-06-29.md` | 06-29 | Apollo as a run-time "trust layer for assembled UI"; first vehicle a per-user contextual dashboard | PARKED → REVIVED by Apollo-MCP | note's own guardrail "horizon-3 … NOT a roadmap change"; revived as the POC vehicle in the MCP v2 page |
| `notes/_briefs/2026-08-31-231-factory-north-star-brief.md` | 08-31 | The north-star test: "is the code it produces useful to a dev team, is it build ready?"; four delivery shapes | BANKED | brief header "Status: BANKED, nothing ruled"; store row `W-329` open, owner dave |
| `_BUILDOUT-STRATEGY-2026-07-21.md` | 07-21 | Component build-out order | ENACTED / HISTORY (library 91 → 135 at #210) | commit `9772db64` "THE LIBRARY WENT 91 → 135, LAYER 2 CLOSED" |
| `_PLAN-designers-brain-2026-09-02-v1/v2.html` | 09-02 | The designer's brain: graded principles, obligations, polarities, licence tiering | ENACTED for the ruled half (12/12 questions ruled; principles and polarities in the graph by #275) · 28 open items listed in v2 §10 | `s237-D1…D10`, `s238-D1…D7`; v2 §0 "28 Open items, listed"; principles landed `s275-D*` |
| `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` | 09-02 | The behaviour address as a typed meta object | ENACTED | `s234-D5`, `s245-D1…D6`; commit `5ae4d32c` "v1.0.6 content: L2/L3/L4 enacted" |
| `_REVIEW-L3-composition-edge-2026-09-03-v1.html` | 09-03 | `groupsWith` composition edge | ENACTED | `s245-D7`; `knowledge/components/meta.schema.json` carries `groupsWith` (grep) |
| `notes/_PROPOSAL-compose-time-door-2026-09-14-v1.html` | 09-14 | A task sentence → a closed context slice; step 1 of generate, advisory, one check later blocking | PARTLY — built and wired as step 1 (advisory); the "every component on the page is in the page's slice" blocking check not found | `knowledge/_compose_slice.py` (2,623 lines) header cites `s277-D10` + `s277-D13`; `s279-D1` ships it in the pack |
| #288 composition probe ("Apollo composes, not traces") | 09-19 | Compose pages without the template as dot-to-dot | PROPOSED direction; Dave's verdict mixed | commit `71b3363c`; his carried words at `_CARRIES.md:108` "so better is someways and worse in others…" |
| One-shot dashboard / cold-start acceptance | 08-28 → | A cold seat reaches his fettled dashboard from one prompt | OPEN — no cold run since 2026-09-02 at the strand-map read | `W-304` open (owner dave); `notes/_STRAND-MAP-2026-09-19.html` strand 03 "Nothing has been run cold since" |
| Overview dashboard definition | 09-19 | Define what an overview dashboard must answer | OWED, his: "I also think we need a definition of an 'Overview dashboard' lets work on this together" | strand map strand 03 (quoted there, Dave 2026-09-19) |
| `notes/_TEST-PLAN-novel-screen-proof.md`, `reviews/DP-TEST-PLAN-2026-09-05-v1.html` | 07 / 09-05 | Test plans for the first external proof and for the 29 dashboard principles (W0–W8) | PARTLY — W1, W2 landed | `s247-D1…D5`, `s248-D1…D4`; later waves not found in commits |

### 1.2 Apollo-MCP and GenUI

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html`, `-v2.html` | 09-26 | Don't invent a protocol: publish Apollo as a versioned A2UI catalogue over MCP, MCP Apps as the fallback shell carrying Apollo's renderer; Apollo owns when-to-use, pre-render gates, entitlements, the record; POC = June's contextual dashboard on mock data for four mock banking roles | PROPOSED | v2 header "Status: a recommendation for you to rule on. Nothing here is decided."; both files UNTRACKED (no commit) |
| Research: `notes/_subreports/2026-09-26-303-G1-genui-archaeology.md`, `…-G2-agent-ui-landscape.md` | 09-26 | The repo's GenUI ancestry and 40 dated external sources | FILED | `_HANDOFF-154` § WHAT LANDED |
| "gates as a service" (July) | 07 | Serve the validators as MCP tools | PARKED / ancestor of Apollo-MCP | `_FUTURE-STATE.md:837` "In-flight targets — gates-as-a-service …: `_LIVE-STATE.md`"; G1 found it (`_HANDOFF-154` "Apollo-MCP has an ancestor in the record") |

Constraint that binds it: `s294-D10` "JEV IS A DEV-TIME INSTRUMENT ONLY AND NEVER A BLOCKING DEPENDENCY", with his rider verbatim: "In the future if we decided to actually integrate jev as a tool for Apollo (It's doubtful we will be able to on a work computer) I'd like to have the option, but this probably doesn't change the decision." v2 says it corrected Jev accordingly ("v2 answers your 14:51 and 14:52 messages: a proof of concept in full, Jev corrected, entitlements guessed").

### 1.3 Knowledge graph and the rulings brain

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `_RESEARCH-graph-engineering-2026-08-05-v1…v3.html` | 08-05 | Field scan; candidates 1–3 | PARTLY — candidates 1, 3 and the mark half of 2 landed | commit `2a231f94` "THREE GRAPH-ENGINEERING CANDIDATES LANDED: 1, 3, AND THE MARK-HALF OF 2" |
| `s131-D2` KG "as robust as the Memento graphs" + `s133-D1` scope widening | 08-08 | Typed edges, parse gate, prose targets become real nodes | PARTLY — mechanical half enacted; Dave's-eye batch presented | commit `5b590996` "s131-D2 mechanical half enacted"; `s133-D1` status "Enactment split: MECHANICAL … DAVE'S-EYE batch … presented for his review" |
| `reviews/TIER-MAP-PROPOSAL-2026-08-08-s135-v2.html` (`s135-D3`) | 08-08 | Atomic tier for every node + mutation-key grammar | RULED as requirement, mechanism never designed; in effect overtaken by `s136-D1` three-axis model | `s135-D3` status "RULED #135 as REQUIREMENT; mechanism NOT designed"; no code file names it (grep) |
| `s136-D1` three-axis model (params/variants/slots) | 08-08 | Every node flexes on three axes; rollout lanes | PARTLY — schema amendment `s140-D1` enacted; "enforcement gate + intent vocabulary are separate lanes" | `s140-D1` status; commits `0cff8055`, `8b548b87` |
| `_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html` (#269) | 09-14 | 13 families at zero in the graph; order 1–5: roles/DESK · 470 rules · 145 principles + polarities · icons then logos · four edge types (setIn / behaviourFrom / capturedFrom / acceptsCapability) | PARTLY — steps 1–4 ENACTED; step 5 NOT; `s269-D6` new kinds NOT | `s269-D1…D6`; step 5 edge names appear only in `_rulings.json`/`_memento-index.json` (grep of knowledge/*.py and json); step 4 via `s277-D4…D7` + `s282-D*` |
| `notes/_PROPOSAL-kg-roles-desk-2026-09-14-v1.html` | 09-14 | Four role/DESK edge types into the closed vocabulary | ENACTED | `s270-D2`; `knowledge/gen_kg_roles_desk.py` |
| `notes/_REVIEW-when-predicates-…-v1.html`, `_REVIEW-when-harvest-whole-library-…-v2.html` | 09-14 | When-to-use rules for 132 components; single-select cut-off | ENACTED (93 rulings `s272-D1…D93`); cut-off PROVISIONAL | `s270-D1` "PROVISIONAL BECAUSE ITS SOURCE IS DAVE'S RECOLLECTION"; `P-270-1` parked (confirm against HSBC Common Toolkit Figma) |
| `notes/_REVIEW-roles-drift-2026-09-15-v1.html` | 09-15 | Roles vocabulary drift | ENACTED | `s273-D1` |
| `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html` | 09-15 | Where the list/card line sits | ENACTED | `s274-D1…D5`; `P-274-2`, `P-274-3` enacted |
| `notes/_PROPOSED-266-ruling-edges.html` | 09-10 | Ruling-to-artefact edges | ENACTED | `knowledge/_ruling_edges.json`, commit `b858080a` (#267) "authored ruling-edge store — 48 edges (47 from lane E's ratified recs…)" |
| `notes/_lanes/281/orphan-plan/ORPHAN-PLAN-2026-09-17.html` | 09-17 | A recommendation for every orphan set | ENACTED (all eleven back as yes) | `s281-D1…D6` |
| `s277-D4…D13` (the Constitution wave) | 09-16 | Icons/logos as nodes; three views; scope per guideline file; thin slice as step 1; twelve verbs; tokens at group grain; ASK door | ENACTED 11 of 13 at #279; `s277-D12` NOT (see 2a) | `_DECISION-HISTORY/2026-09-16-279-…md:120` "`s277-D12` (tokens at group+tier) was never started" and `:129` "Eleven of thirteen `s277` rulings are in the tree" |
| Explorer layouts / front door `s280-D1`, `s280-D2` | 09-16/17 | FORCE/STRATA/SHELLS matrix; INSPECT opens the artefact | ENACTED (explorer v1.27) | `_HANDOFF-154` "rebuilt, v1.27, 4,888 nodes, 8,756 edges" |
| `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` | 09-21 | Jev as build-time selector over the KG | PROPOSED ("Idea, not a lane"), bounded by `s294-D10` | file title; uncommitted tail declared dirty in `_HANDOFF-154` |
| `notes/_lanes/293/J5/jev-recall-proposal.html` | 09-21 | Pay Jev at index time to fix recall, not ranking | PROPOSED, after-Friday by Dave's words | page: "Status Proposal for ruling — nothing enacted"; Dave: "any chages with impact will need to be made after the presentations and demos." |
| `_RESEARCH-ngram-lookups-2026-09-13-v1.html` | 09-13 | n-gram doors (quote gate, near-dupes, ranking, typo) | PARTLY — three advisory doors built; five uses PARKED | `s269-D7` (quote gate); `P-269-1…P-269-5` parked |
| `P-269-6…P-269-9` | 09-14 | Temporal ADR-0007 half · blast radius as pre-flight · compiled views 2–6 · persona/JTBD nodes | PARKED | `knowledge/_parked.json` |
| `P-272-2`, `P-272-3`, `P-273-1` | 09-15 | Modal taxonomy · navigation strategy session · ingest HSBC Common Toolkit specs | PARKED | `knowledge/_parked.json` |
| Dave's three observations into the graph | 09-24 | "these are observations that we will role into the graph at some point" | OWED, his | `_HANDOFF-154` § OWED item 4 |

### 1.4 Components and canon

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `_BRIEF-component-scaffold-2026-08-14-v1.md` | 08-14 | Gates 1–6 for a new component | ENACTED | `s173-D1`, `s174-D1` |
| Wave 3/3b foundations briefs (#203) | 08-19 | Six fenced Opus lanes, P1 foundations | ENACTED as PROPOSED builds | `_BRIEF-wave3-foundations-2026-08-19-v1.md` ("`$status: PROPOSED #203, Dave's eye owed`") |
| #210 Layer-2 waves 5–6 | 08-20 | 27 organisms: app shells, page templates, form templates, lock-ups | BUILT PROPOSED-NOT-RULED, parked | `_state.json` `W-75`…`W-84` state `parked`, titles "BUILT PROPOSED-NOT-RULED — Daves eye owed" |
| `notes/_PROPOSED-263.html` eleven defaults | 09-09 | Eleven lane defaults | ENACTED | `s263-D1…D11` (e.g. `s263-D7` status "enacted #263") |
| Six dashboard components (#261) | 09-08 | Designed then revised on his sentences | ENACTED (v1.0.9) | `s261-D1…D9`; `s262-D*` |
| Bento canon + template generation arm | 08-22 → 09-19 | Per-theme structural and embedded gutters generated, not pinned | ENACTED 2026-09-19 (after the strand map) | `knowledge/canon/canon.css:22012–22034` AUTO-BENTO-ROLE-VARS per theme; `git log -S` → `71b3363c` |
| `s246-D3` spans chord dial (TRIAL) | 09-05 | 4+2 · 2+4 · 3+3 · 6 as an edit-rail dial | RULED-NOT-ENACTED (hedged) | no commit names `s246-D3`; not in `knowledge/_render/_bento_edit_rails.json` (grep) |
| `W-116` bento tuner, `W-125` gallery span/justified, `W-126` matrix explorer | 08-22 | Three bento decision pages | PROPOSED, open 34 sessions | `_state.json` rows open, owner dave |
| `_PROPOSAL-size-ramp-theme-modes-2026-08-18-v1.md` | 08-18 | Master size ramp + per-theme size modes | PROPOSED ("FLOATED, Dave's, #200") | file title; no ruling names the file (doc2rulings.json) |
| Logo system (`s282-D3…D6`, `s287-D2`) | 09-18 | Height scale 24–40, masters per size, clear space | ENACTED | 40 masters registered (`s287-D2`); `_logo_nodes.json` |
| `notes/_REVIEW-264-*` active glyphs | 09-09 | Active-glyph derivation | ENACTED / 4 glyphs ungraded at the time | `s264-D1…D3`; `_CARRIES.md:294` |
| `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md` | 07-25 | 44px control target, 24px marks, markup-driven gate | PARTLY — measurement enacted; both blocking halves NOT | `s114-D5` "ENACTED #116"; `knowledge/_validate_a11y.py:64` `CONTROL_TIER_44 = "warn"` and `:65` `MARK_TIER = "warn"` |
| `s114-D2` adoption-time citation gate | 08-06 | Advisory citation gate with named promotion trigger | RULED-NOT-ENACTED (hedged) | status "NOT BUILT"; no file named `*citation*`/`*adopt*` in `knowledge/`; `W-99n` open |
| `s165-D6` interactive dashboard v2 | 08-13 | Dig-deeper and manipulate | PARKED as direction | status "v2 is a declared future lane, UNSCHEDULED and UNSPECIFIED" |
| `_FUTURE-STATE.md` component ideas (mobile variants, loader atom, heatmaps, one legend for many charts, context-aware responsive behaviours) | 07-22 → 09-09 | Various | PARKED | `_FUTURE-STATE.md:15`, `:33`, `:339`, `:366`, `:463` (lane A3 owns this ledger) |

### 1.5 Data visualisation

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| ADR-0015 behaviour partials | 07-23 | Dataviz interaction layer as generated JS | ENACTED | commits to `b8796f81` 09-08; `s250-D1`, `s260-D1` |
| Chart waves 1–2 briefs | 07-24, 08-05 | Bar/scatter/donut/sparkline/combo, then bar family, statistical, pie/area | ENACTED | chart metas in `knowledge/components/`; `s276-D5`/`s277` charts enacted (87 obeys) |
| Data-driven chart engine (#259) | 09-08 | dv-render core + type partials | ENACTED | commit `f6f762ab` "THE CHART ENGINE: dv-render core + six type partials" |
| `s116-D1` marks held to 24×24 blocking | 08-06 | Blocking half | RULED-NOT-ENACTED | `knowledge/_validate_a11y.py:65` `MARK_TIER = "warn"` |
| Heatmaps, mini chart ramp | 07-22/23 | — | PARKED | `_FUTURE-STATE.md:366`, `:812` |

### 1.6 Tokens and themes

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| ADR-0009, 0010, 0011, 0014 | 07-20/22 | Colour as substrate; nullable flex slots; themes as override sets; per-theme neutrals | ENACTED | register: 0010 PROVEN (`_validate_radius.py`), 0009 CLAIMED; override sets in `knowledge/tokens/themes/` |
| `s216-D1` theme publishing = minted, dev-ready, theme-specific code (ADR-0011 publish tier) | 08-22 | A publish tier | RULED-NOT-ENACTED | only commit naming it is the inscription `175246f8`; no per-theme CSS artefact exists (`find` for `*console*.css` etc.: none); `W-138` open; not mentioned in ADR-0011 text (grep) |
| `notes/_briefs/2026-08-24-217-css-delivery-strategy.md` | 08-24 | Subset mints, critical CSS, font-display | PROPOSED ("MEASURED SIMULATION + priced techniques. Nothing here is ruled.") | brief header; `W-138` |
| `s200-D1` mint-time radius/padding derivation | 08-18 | Generator writes concrete tokens | ENACTED (mechanism) | `knowledge/gen_radius_derive.py`; `canon/gen_canon_bento.py:170` |
| `s245-D10` console radius set | 09-03 | control 6 · surface 8 · container 12; segmented xs 4/2 · s 6/4 · m 8/6 · l 10/6 | RULED-NOT-ENACTED | ruling text "ENACTMENT … is #246's build, NOT done at #245"; `canon.css` console block reads `--border-radius-control: 8px`, `-surface: 20px`, `-container: 20px`; `tokens/themes/apollo-console.overrides.json:12–25` |
| Colour rulings of #130–#155 flagged NOT ENACTED in the store | 08-08 → 08-11 | Banner ghost, check labels ink, chips pressed, legacy RAG, two-red law, green mirror, plus/minus rung | ENACTED later (store stale) — see 2b | `canon.css:6679` (s149-D1 amends s130-D4); `s145-D1`, `s158-D1…D4`, `s168-D4/D5`, `s170-D2` |
| `s135-D1` contextual notification shell per theme | 08-08 | Legacy+SC keep 1px border; mono+console tint-only; console radius via surface | RULED-NOT-ENACTED | `canon.css:2046` `.note.tint{… border:1px solid var(--accent) …}` for every theme; no canon/snippet file names `s135-D1` |
| `knowledge/tokens/_proposals/*.proposals.json` (dataviz ranges, neutral blacks, semantic colour, supporting palette) | 07 | Candidate values | PROPOSED/HISTORY — not probed individually | directory listing |
| APCA research | 08-28 | Successor to WCAG 2.x contrast | PARKED | `W-262` parked; `notes/_briefs/2026-08-28-223-apca-research-parked.md` |
| Photography assets (251 JPEGs) | 08-21 | Image blocks / carousel; per-theme settings | ENACTED (settings, derivatives) | `s218-D3`; `W-137` "per-theme photography settings enacted, all 251 derivatives minted" |

### 1.7 Release, packaging (Spider, designer pack, Memento package)

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `notes/_briefs/2026-08-28-222-release-plan-v1.md` | 08-28 | Every loose end to the bake | ENACTED (v1.0.3 → v1.0.13 shipped) | thirteen Spider releases on disk (strand map strand 01, measured 09-19) |
| Designer pack v2 / v2.1 with the reader + Constitution | 09-16 | Ship `_compose_slice.py` and `_rulings.json` in-pack | ENACTED | `s279-D1` |
| Three-option salutation opener, `/goal` amendment | 09-09 | Interview / typed brief / goal | ENACTED | `W-262o` done; `s262-D5` → `W-262q` "the v1.0.9 re-cut at dd129e8" |
| Pack ships gates red at bake (Q1) | 08-26 | Whether a designer's first CI run may be red for inherited reasons | PROPOSED, unruled since #219 | `W-99zz` open ("chiefly Q1, whether the pack ships with four gates that are red at bake") |
| Ruled-value signalling in the pack | 09-19 | Tell a reading agent a value is ruled, not accidental | PROPOSED (conductor finding) | strand map strand 01 "Nothing in the pack tells a reading agent that a value is ruled rather than accidental" |
| `P-277-5` NPM distribution with Angular and React emitters | 09-16 | Tokens + components on a registry, framework emitters | PARKED | `knowledge/_parked.json` |
| `memento-package/_PACKAGE-SPEC.md`, harness spin-off note | 07-23/31 | Memento as a shareable pack | ENACTED v0.1.1 then DISABLED on Dave's machine | spec `status: scaffold`; plugin disabled #69 (harness in `knowledge/` is sole canon) |
| Spider pack currency | 09-24 | Which pack is on his work machine; email bundle carried v1.0.13 while seven commits since touched components/canon | OPEN question | `_HANDOFF-154` § OWED item 5 and "The email bundle's pack is older than the tree" |

### 1.8 The harness, Memento, boot and the window

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `_MEMENTO-REBUILD-PROPOSAL-2026-08-02-v1.md` | 08-02 | Items with identity and close conditions | ENACTED in reduced form | `knowledge/_state.py` docstring "#88 … this file is smaller than the proposal asked for" |
| `notes/_STATE-MACHINE-TARGET.md` | 07 | The context machine north star | PARTLY ("agreed target, partially built") | file header |
| GM compaction architecture (GM-D1…D9) | 07-27 | Typed-content contract, retirement tests | RULED; audit state "unaudited" in the table | `notes/_MEMENTO-DECISIONS.md:71–73` |
| Roll-at-open plan | 07-29 | Roll at open, not at wrap | ABANDONED | `_MEMENTO-DECISIONS.md:1414` "D7 · RULED (b) — drop roll-at-open; the premise is gone." |
| Borrowed instruments B1/B2/B3 | 08-12 | Gardener, dashboard wiring, grades sidecar | ENACTED with a first-cycle return OWED | `s179-D1` status "return-with-numbers OWED after one full cycle"; `s182-D1` |
| PM topology + mechanisation programme | 08-19 | Fable judgment / Opus build-PM / verifier-PM; items 1–5 | PARTLY — items 1, 2 built; 3/4/5 scope only | `notes/_claims/204-*`, `knowledge/_join_claim_tables.py`, `knowledge/_probe_registry/`; `W-44`, `W-45`, `W-46` open |
| Effort gauge, links backfill | 08-13 | Better effort input; `links` on the store | ENACTED (links) / RULED (gauge) | `s170-D1` "ENACTED AND VERIFIED"; `s168-D2` |
| Compaction strategy (#181) | 08-15 | Research | PARKED | page "Parked research — nothing here is ruled, built, or scheduled" |
| Context-territory strategy, 200–256K conditional band | 08-21 | Window use | RULED | `s214-D1`, `s214-D4` |
| Boot band derived + shrink-only ceiling | 09-02 | `s240-D1` / `s240-D2` | ENACTED | `W-386` done; `s295-D3/D4` re-based ceiling 72,768 and boundary #295 |
| `notes/_PLAN-300-boot-diet-2026-09-23-v1.html` | 09-23 | Four before-Friday moves; after Friday move the conductor to Claude Code on his Mac (~30K boot, projected) | PARTLY — moves 01–02 enacted by his act (new Project instructions: no memory at the opener or while live); seat move PROPOSED | plan page; `_CARRIES.md:60` (instructions pasted at #300); Project instructions step 4 |
| Notice board for concurrent seats; wrap-is-slow levers | 09-21 | Present-tense board; five levers to speed the wrap | PROPOSED, post-Friday | lane notes under `notes/_lanes/293/` (memory areas point there; not re-probed) |
| Jev integration (`_jev.py`) | 09-21 | Typed judgment model in Apollo | RULED dev-time only | `s294-D10` |
| Dream passes 6–13 | 08 → 09 | 39 proposals | 22 enacted · 1 ruled-not-enacted (then built) · 13 never ruled · 3 overtaken, then #294 ruled and enacted twelve | `_DECISION-HISTORY/2026-09-21-293-…md:45–46`; `s294-D1…D12` |

### 1.9 Presentation and demo

| Proposal | Date | What it proposes | Status | Receipt |
|---|---|---|---|---|
| `notes/_PROPOSAL-apollo-story-2026-09-19-v1.html`, `-v2.html` | 09-19/20 | The Apollo story arc | SUPERSEDED by his own copy | `_CARRIES.md:104` "he wrote the deck's copy himself, in seven beats" |
| `notes/_STRAND-MAP-2026-09-19.html` | 09-19 | Six strands, the path to Friday | HISTORY (Friday passed); its bento item since ENACTED; its one-shot item still OPEN | this report §1.4, §1.1 |
| Deck v14 plain (16 slides) + demo prompt with Common | 09-22 → 09-24 | Friday 2026-09-25 internal | ENACTED for Friday; outcome NOT IN THE RECORD | `_HANDOFF-154` "FRIDAY 2026-09-25 HAPPENED. ITS OUTCOME IS NOT IN THIS RECORD." |
| Slide 15 ask | 09-24 | "BETA to Enterprise Capability." | ENACTED by his act, the draft ask parked in a comment | `_HANDOFF-154` strike 5 |
| `system-manager/capturing-decisions-proposal.html` (DDR) | 06-22 | Design decision records with deciders/consulted/informed | SUPERSEDED by ADR-0007/ADR-0012 decision graph and `_rulings.json` | ADR-0012 (07-21, accepted) |

---

## 2. RULED NOT ENACTED — the full list I could establish

### 2a. Verified not in the tree today (probe receipts)

| Ruling | Date | What Dave ruled | Probe that shows it is not in the tree |
|---|---|---|---|
| `s245-D10` | 09-03 | Console radius set: control 6 · surface 8 · container 12; segmented per scale | `canon.css` console block `--border-radius-control: 8px`, `-surface: 20px`, `-container: 20px`; ruling text "NOT done at #245"; no commit after `04099a86` (#246) names it |
| `s114-D6` | 08-06 | 44px promoted to BLOCKING for controls (re-priced by `s116-D4`, "Dave's ruling STANDS") | `knowledge/_validate_a11y.py:64` `CONTROL_TIER_44 = "warn"`; `W-99n` open |
| `s116-D1` (blocking half) | 08-06 | Data marks held to 24×24 | `knowledge/_validate_a11y.py:65` `MARK_TIER = "warn"`; `W-99p` open ("the 107 sub-24 marks + 11 UNMEASURED") |
| `s114-D2` | 08-06 | Adoption-time citation gate, advisory, named promotion trigger | status "NOT BUILT"; no gate file found by name (hedged — a differently named file could exist); `W-99n` open |
| `s135-D1` | 08-08 | Notification shell per theme (mono+console tint-only) | `canon.css:2046` one border rule for all themes; no canon/snippet file cites it |
| `s135-D3` | 08-08 | Tier mapping + mutation-key grammar | "mechanism NOT designed"; no file cites it; likely overtaken by `s136-D1` (needs his word to retire) |
| `s216-D1` | 08-22 | Theme publishing = minted, dev-ready, theme-specific code | no per-theme CSS artefact on disk; only its inscription commit `175246f8` names it; `W-138` open |
| `s246-D3` | 09-05 | Spans chord dial in the edit rails (TRIAL) | zero commits name it; absent from `_bento_edit_rails.json` (hedged) |
| `s269-D1` step 5 | 09-14 | Edge types setIn / behaviourFrom / capturedFrom / acceptsCapability | names appear only in `_rulings.json` and `_memento-index.json` (grep over knowledge/*.py, *.json) |
| `s269-D6` | 09-14 | Content standard and lifecycle status as new entity kinds | no generator or node file carries either kind (grep) |
| `s277-D12` | 09-16 | Tokens at group grain with tier, `bindsToken` edge | "was never started" (`_DECISION-HISTORY/…279…md:120`); zero commits name it; no generator emits `bindsToken` |

Also standing, of the same shape: `s136-D1` (enforcement gate and intent vocabulary lanes not found — PARTLY), `s133-D1` (Dave's-eye batch), `s179-D1` (return-with-numbers after one cycle owed), `W-46` mechanisation items 3–5, `s151-D3` parts (1) and (2) were later covered by `s158-D*` (see 2b).

### 2b. The store says NOT ENACTED, but later rulings or commits enacted them (store is stale)

`s130-D4` → amended and enacted by `s149-D1` (`canon.css:6679–6683`). `s130-D5` → `s149-D1`; `selection-controls.meta.json:143` cites it. `s130-D6` (chips pressed charcoal) → in effect SUPERSEDED by `s151-D2` ("CHIP PRESSED = NO REVERSAL, tint-symmetric"), enacted in commits `ed1f930c`, `ee091eff`; the store carries no `superseded_by` on `s130-D6`. `s131-D1` → enacted (commits `6e6a6504`, `a1995c0c`; `s158-D1`). `s131-D2` → mechanical half `5b590996`. `s135-D2`, `s135-D4` → `b22e16b9` "s135-D4 ENACTED — 82/82 KG VERDICTS". `s144-D1` → name `s145-D1` enacted; minted `rag/success-ink`, `rag/error-ink` (`semantic-colour.json:609`). `s149-D1`, `s151-D1`, `s151-D2`, `s155-D1` → `s158-D1…D4`, `s168-D4/D5`, `s170-D2` (all "ENACTED"). `s152-D1` → commit `8dee1d1f` "s152-D1 is ENACTED AND VERIFIED". `s157-D2` → built `s158-D4`, ratified as-built `s167-D1`. `s165-D4` → `s170-D1`. `s172-D1` → `s172-D2`, `s194-D1`. `s173-D1` → `s174-D1`. `s198-D2` → commit `eba1ef0f`. `s240-D1/D2/D3` → `W-386`, `W-387` done.

That is 17 rulings whose store status still reads NOT ENACTED while the tree says otherwise (measured by the cross-check script, `notes/_lanes/304/A1/notenacted_cands.json`, then read by hand).

### 2c. What cannot be established from this seat

The 424 bare `ruled` rows. I checked the ones tied to proposals (sections 1 and 2a); I did not probe all 424 against the tree. A mechanical back-stamp lane could: for each ruling, find commits whose body names the id with an enactment verb, and the files the ruling `governs`, and propose `enacted <sha>` / `not-found` rows for Dave's review. `knowledge/_inscribe_ruling.py --set-status` exists since #295 (`s295-D2` status) — the sanctioned writer; hand edits of `_rulings.json` are banned (#179).

---

## 3. Duplicates and contradictions

1. The delivery-shape cluster (duplicate, unruled). Factory north-star `W-329` (his words: "The question we need to answer is, 'is the code it produces useful to a dev team, is it build ready?'"), `s216-D1` publish tier, ADR-0008 adapters, `P-277-5` NPM + Angular/React emitters, and Apollo-MCP's catalogue + renderer are five answers to one question. Apollo-MCP route B makes Apollo's own renderer the output for hosts; `P-277-5` makes framework components the output for devs; `s216-D1` makes minted CSS the output. They can co-exist, but only by a ruling that orders them. Nothing orders them today.
2. The window lines (contradiction). `s272-D93` (180,000 working / ~220,000 tolerated / 256,000 hard, amended #287) versus his #301 lines as carried in `_HANDOFF-154` ("working 256,000, hard 300,000 (his, #301); stop 180,000 and tolerance 220,000 unmoved"). His #301 words are not inscribed ("inscribe his window words?" on `_HANDOFF-152` § OWED). Two sets of numbers are live at once.
3. The boot ceiling versus the seat (contradiction). `BOOT_CEILING_TK` 72,768 (`s295-D3`) against cloud boots of 126,178–128,437 (#297–#302, `_HANDOFF-154` post-wrap item 1). Every wrap since #297 has gone on the DECLARED not-a-wrap path because the wrap gate's boot arm is structurally red. `_PLAN-300` offers the seat move as the lever; nobody has ruled whether the ceiling is per-seat.
4. Template status (contradiction). The bento dashboard template's own meta says proposed and not registered; the showroom index says beta (strand map strand 02, "Two statuses for one artefact … since #231"). The 27 #210 organisms likely share the same split — not probed per file.
5. Stale parked rows that later rulings answered (duplicates). `P-272-1` list-vs-card sidequest is still `parked` although `s274-D1…D5` ruled it; `P-277-4` logo review is `parked` although `s282-D3…D6` and `s287-D2` ruled the logo system. Each needs a close with receipt, not a re-ask.
6. `s130-D6` versus `s151-D2` (superseded without a pointer), and `s135-D3` versus `s136-D1` (requirement overtaken by a model). The store should carry `superseded_by` so the trigger index stops printing a dead ruling at anyone touching chips.
7. Brain versus KG plans (overlap, resolved in practice). `_PLAN-designers-brain` (#236–#238) and the KG-gaps order (#269) both planned the principles into the graph; #275 did it once. Plan v2's 28 open items were never re-read against #269–#281 — some are likely closed.
8. Dashboard proof (duplicate asks). `W-304` cold-start acceptance (#228), the frozen-prompt cold runs (#258), the one-shot strand (#288) and the overview-dashboard definition (09-19) are one piece of work asked four times. The Apollo-MCP POC names the same dashboard as its vehicle — a fifth.

---

## 4. Externalities and dependencies worth the roadmap seat's attention

The Apollo-MCP files are untracked, so a clean checkout or a fresh cloud seat does not have them. The Friday outcome and which Spider pack is on his work machine are both unknown and both change priorities. Jev is dev-time only, so anything in a POC that needs run-time judgement has to be mechanical (`s294-D10`). A2UI is v0.9.1 with v1.0 due Q4 2026 (v2 page, "Re-checked today, 26 September") — a catalogue built now targets a moving spec. The CI gate job carries six inherited fails (`[3] [13] [38] [125] [128] [136]`, `_HANDOFF-154` post-wrap item 5), so any weekend lane that reads "gates green" must diff against that set, not against zero. The mount strands `.git/index.lock` on every `--wrap` run (seven wraps running). `API-KEY.txt` sits at the repo root (seen in `ls`, not opened); it is gitignored (`.gitignore:72`), so the risk is the mount and any zip built from the working tree, not git — lane A4's call.

---

## 5. My read — the most value per effort right now

Effort is my estimate, not a measurement.

1. Rule Apollo-MCP v2 and cut the POC as a thin vertical: catalogue generated from the metas (about 15 parts, the page's own figure), `_compose_slice.py` as the chooser, the existing gates run server-side before render, entitlements mocked for four roles, the KG as the record. It is his live ask, the research is filed, and most of the parts exist. Effort: large, but a weekend POC slice is feasible. Depends on items 2 and 3.
2. One decision page for the delivery-shape cluster (§3.1): five proposals, one ordering. Small effort, unblocks the MCP POC and `W-329` together.
3. Land `s269-D6` lifecycle status as a node field (MCP v2 wants "each with a name, level and status") and `s277-D12` tokens at group grain with `bindsToken` (the catalogue needs token bindings). Medium, mechanical, gateable, and both are already ruled.
4. Enact `s245-D10` through `gen_radius_derive.py` for console. Small, fully specified, ruled three weeks ago; render four themes for his eye after.
5. Enact `s135-D1` (notification borders per theme). Small, ruled seven weeks ago.
6. Back-stamp the ruling store (§2c) with `_inscribe_ruling.py --set-status`, proposing, never asserting, with a review page for the uncertain rows. Medium, mechanical, and it turns every future "what is ruled and not built" question into a query.
7. Run the one-shot cold, against the overview-dashboard definition he asked to write with you. The definition is a half hour of his time; the cold run is the proof both the demo story and the MCP POC rest on. Medium.
8. A review page for the 27 built-proposed Layer-2 organisms (`W-75`…`W-84`), grouped so he can rule them in batches, and reconcile the showroom/meta status split. Medium for the page, his time for the ruling.
9. The a11y blocking flips (`s114-D6`, `s116-D1` blocking half): re-measure the 72 controls and 107 marks, fix or declare, then flip with mutation tests. Medium; a real compliance gain; test hard because it can turn the library red.
10. Close the stale parked rows (`P-272-1`, `P-277-4`), put `superseded_by` on `s130-D6`, and put the window lines (§3.2) and the per-seat boot ceiling (§3.3) to him as two plain questions. Small, and it removes noise the roadmap would otherwise re-plan.

Not recommended this weekend: `s216-D1` publish tier and `P-277-5` emitters until item 2 is ruled; J5/J7 Jev work beyond analysis (his "after the presentations and demos" is now satisfied by date, but `s294-D10` still bounds it); the after-Friday seat move (`_PLAN-300`) until he says which machine he is on.

---

## Method

Swept `notes/_PROPOSAL-*`, `_VISION-*`, `_PLAN-*`, `_REVIEW-*`, `_PROPOSED-*`, root `_PROPOSAL/_PLAN/_BRIEF/_RESEARCH/_REVIEW/_TRIAGE-*`, `notes/_briefs/*` (208 files, filtered to proposal/plan/strategy/research/north-star/programme/idea/parked names), `docs/decisions/ADR-0001…0017`, `archive/`, `digital-experience-transformation/strategy/`, `memento-package/_PACKAGE-SPEC.md`, `system-manager/`, `notes/2026-07*/08*.md` research notes, `knowledge/_parked.json` (25 rows: 23 parked, 2 enacted), `_state.json` (855 items; 20 parked), `_CARRIES.md`, `_HANDOFF-150…154`, `_DECISION-HISTORY/*279*`, `*293*`. Rulings loaded with `json.load(...)['rulings']` (638, newest `s295-D4`). Cross-checks: rulings naming each doc (`doc2rulings.json`); for every ruling whose status says NOT ENACTED/NOT BUILT, later rulings and commit bodies naming its id (`notenacted_cands.json`); code greps and `canon.css` reads for the eleven in §2a. Read-only git only (`git --no-optional-locks log`). Not done: a per-ruling probe of all 424 bare `ruled` rows; per-file status of the 27 #210 organisms; the `_FUTURE-STATE.md` ledger in depth (lane A3).
