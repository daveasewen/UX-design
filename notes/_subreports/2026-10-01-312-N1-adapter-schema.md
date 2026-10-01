# #312 lane N1 — the adapter manifest schema, the gate, Sutherland React as the first manifest, and the Copilot kit for Dave's work machine

Lane N1 · Fable · CLOUD (git worktree of the noon push, HEAD `97c7793`) · Thu 2026-10-01 · never committed. Brief: `notes/_lanes/312/N/BRIEF.md`. Ruling enacted: `s311-D7` (an adapter manifest per client library; Apollo governs, theirs renders; the unmapped list is required) under `s311-D9` (the S2 schema starts now). Dave's call-5 comment on the wave-2 plan page, verbatim, is what the kit answers: "So whats the process for this, are we writing what we require and handing this to the sutherland team to map the components etc. I don't have access to Sutherland on this computer, but I do have access on my other work computer where I run the spider release, is tehre a way we can just get it done on the two computers, the other machine uses VS and co-pilot, maybe you could write a brief or something for the agent on my work machine?"

COUNTS: binding rows 4 (0 with a Sutherland component named; all unverified, 4 with open holes; nothing mapped) · unmapped 134 · metas in corpus 138 (139 files minus EXAMPLE-button) · token rows 0 · gate selftest 19 arms 0 failed (11 bites, 4 controls, 4 kit arms) · test_gates 37/0 · kit parts 17 · kit starter rows 17 (0 named) / unmapped 121 · kit token names 700 + 357 groups · STEPS 167 → 169.

Headline: Apollo has no Sutherland mapping yet (see Correction, 13:02). The schema, the gate and the first manifest are built and proven (the gate passes `adapters/sutherland-react.json`, fails three mutated copies and eleven planted bites, and runs inside `test_gates`); the Copilot kit is a self-contained folder that validates without the repo; `s311-D7` is ENACTED by this change and awaits AC's sha for the stamp. Nothing on the Sutherland side has been read, so every name on that side is `null`, said so, never guessed.

## Correction, 13:02

Dave, 13:02 BST, verbatim: "the four Sutherland bindings we already have? Im not sure I'm aware of these, this might be an assumption of your part, please be careful"

He is right. Apollo has no Sutherland mapping yet. The four "bindings" this report and the files first described are four `codeBindings.sutherland-react` placeholder slots added 2026-06-22 to cards, list-items, status-indicator and table; every field reads "TODO — confirm in Sutherland repo / via Code Connect", and none holds a Sutherland component, prop or import name. They were never bindings, existing mappings, or a head start. The kit is the list of Apollo parts for the Copilot agent to find in Sutherland; four of those parts once had empty placeholder slots, and that is all the order in `parts.json` means.

Lane N1b (cloud, same day) corrected the wording in `adapters/schema.json` (and the kit copy), `adapters/sutherland-react.json` and the kit `manifest.json` / `parts.json` (regenerated from `adapters/kits/_build_sutherland_kit.py`, whose strings were corrected), the gate's docstring, the kit's `README.md`, `FIRST-PROMPT.md` and `BRIEF-FOR-COPILOT.md` (which now tell the agent the `$legacy` blocks are empty TODOs, not hints), and this report. The gate summary line, in both the gate and the kit checker's shared core, now reads `binding rows N (M with their component named …)` so a row count can no longer read as a count of mappings; today M is 0. Every Sutherland-side name stays `null`. Proofs re-run after the change: gate PASS on the real manifest; `--selftest` 0 arms failed (core still byte-identical, kit schema copy equal); kit checker PASS outside the repo (rc 0); `test_gates` 37/0; help-gate OK (272); wiring 57 wired, 0 failures. The upstream wording in s311-D7 / s312-D7 ("from the four existing bindings") rests on the same overstatement; that is the conductor's to correct, not this lane's.

## What was built — paths

| Path | What |
|---|---|
| `adapters/schema.json` | The manifest shape (JSON Schema 2020-12). Per binding: `apollo` (exactly one of `meta` slug or `role`), `theirs` (component, import, export, file), `props` (typed holes: string / number / boolean / enum with a `values` map / data / node / handler; boolean = TRUE renders their attribute, FALSE renders nothing), `slots` (children / prop / slot), `states`, `events`, a per-binding `unmapped` block (props, slots, values, states, events, each with a reason), `status` (unverified → rendered → accepted) with `evidence` (`render` path; `accepted` = Dave + date), `source` cited, `$legacy` (the old empty placeholder slot verbatim). `tokens`: a DTCG resolver document (named `sets` of `$ref` sources, `resolutionOrder`) plus `map` rows their-name → `{apollo.semantic.path}`. `unmapped`: REQUIRED, `$why` + `items` (slug, reason, fallback `apollo-native` or `none`). |
| `knowledge/_validate_adapter.py` | The gate. AD-001 shape (a stdlib schema walker, so the kit gives the same verdict without jsonschema) · AD-002 one meta or one role, both known, none bound twice · AD-003 every Apollo prop named exists on that meta · AD-004 the status ladder on evidence; a jump refuses, Dave's word at a lower status refuses · AD-005 nothing null at rendered or above · AD-006 enum holes carry values; null states and events are echoed in the binding's unmapped · AD-007 token rows resolve in the DTCG spine (via `_validate_dtcg.build_spine`) and never onto `color.*` primitives (ADR-0008) · AD-008 the unmapped list is complete against the meta corpus on disk, nothing both bound and unmapped · AD-009 `--screen PAGE --library ID`: a composed screen's `cn-<slug>` parts must be bound or unmapped with fallback `apollo-native`; else REFUSED. Help-gate line in place; exit 77 `COULD-NOT-ASK:` when `adapters/` or `knowledge/components/` is unreachable (an installed pack), so it is not a #173-class red. |
| `knowledge/_tests/test_gates.py` | `SELFTEST_ARMS` gained the adapter gate's `--selftest`. 37/0 on this tree (36 before). |
| `knowledge/_build_all.py` | Two STEPS entries (gate + selftest) with their ROUTE_ROWS rows in the same edit; `--selftest` reports 169 steps routed. |
| `adapters/sutherland-react.json` | The first manifest. Apollo has no Sutherland mapping yet: it opens four empty rows for the parts that once had a `codeBindings.sutherland-react` placeholder slot (cards, list-items, status-indicator, table; 2026-06-22, every field TODO, no Sutherland name in any of them), every Sutherland-side name `null`, status unverified, each placeholder kept verbatim under `$legacy`; prop rows derived from each meta's props (enum values as `{apollo: null}` maps); cards' `content` slot as a slot row; `library.package/version/source` null; the resolver with Apollo's nine semantic files as one set and an empty Sutherland set; the unmapped list of all 134 other metas, fallback `none`. |
| `adapters/kits/sutherland-react/` | THE KIT (self-contained, USB-stick sized, 190 KB): `README.md` (Dave's one page: six steps), `FIRST-PROMPT.md` (paste into Copilot chat, agent mode), `BRIEF-FOR-COPILOT.md` (the agent's instructions: Apollo in two lines, the job, seven rules, seven steps, how to run the checker, what to hand back, a worked button row with button's real Apollo props), `manifest.json` (the starter: 17 empty rows, Apollo side only, Sutherland side null; 121 unmapped), `parts.json` (17 parts with role, props and their holes, slots, states, events, variants, meta file; plus `allSlugs`, `provides` and the 12 roles so the checker can hold completeness), `apollo-tokens.json` (700 semantic token paths + 357 groups, names only, no values, `color.*` excluded), `schema.json` (a copy), `check_manifest.py` (single file, stdlib only; its CORE region is byte-identical to the gate's and the gate's selftest checks that). |
| `adapters/kits/_build_sutherland_kit.py` | REPO SIDE, outside the kit: derives the manifest, the starter, `parts.json` and `apollo-tokens.json` from the metas and the spine so nothing in them is typed by hand. Dry by default, `--write` to regenerate. Not a gate, not wired. |
| `notes/_lanes/312/N/add_state_row.py` | Adds the born-closed row `W-312n1` (s305-D40 form). `knowledge/_state.json` is job A's single-writer file this wave, so N1 did not touch it: AC runs `python3 notes/_lanes/312/N/add_state_row.py --write` at the 15:00 wave (proven on a copy: the row is refused until this report exists on disk, then adds and round-trips). |

## Proofs (pasted from runs)

Gate on the real manifest (summary line as re-worded by N1b): `PASS adapters/sutherland-react.json — binding rows 4 (0 with their component named · unverified 4 · rendered 0 · accepted 0, 4 with open holes) · unmapped 134 · token rows 0 · 0 error(s), 0 warning(s)`.

Three mutated copies of the real manifest, each `rc=1`:
- no `unmapped` key → `⛔ $.unmapped: REQUIRED and missing — a manifest must say what it does not map, even when that is nothing`
- `bindings[0].status = accepted` → `⛔ $.bindings[0].status: STATUS JUMP — accepted needs evidence.accepted (Dave's word and the date)` and `status 'accepted' but a name is still null`
- `bindings[0].apollo = {role: widget}` → `⛔ $.bindings[0].apollo.role: UNKNOWN ROLE 'widget' — not in the role list (action, arrangement, chart, feedback, headline-metric, input, overlay, page-frame, page-title, record-list, status-surface, wayfinding)` plus `1 Apollo meta(s) neither bound nor listed as unmapped: cards`

`--selftest`: 19 arms, `selftest: 0 arm(s) failed` — the three bites the brief named (no unmapped list, unknown role, status jump to accepted) plus: jump to rendered, Dave's word at unverified, an incomplete unmapped list, bound-and-unmapped, a primitive token, an unresolvable token, an unknown meta, a prop the meta lacks, an unknown key, the screen refusal (`cn-button` unmapped fallback none → REFUSED; flipped to apollo-native → passes), the disk control, and the four kit arms (core byte-identical, schema copy equal, starter passes outside the repo in a tempdir, a mutant bites).

`--screen knowledge/_fitness-test/sme-payments-desktop.canon.html --library sutherland-react` → `table — bound by meta`, `REFUSED button`, `REFUSED modals`, `FAIL … 1 part(s) allowed, 2 refused` (correct: nothing is mapped yet and no fallback is declared).

`test_gates.py`: `37 test(s), 0 failure(s)` including `PASS adapter-manifest gate's own bites run (11 bites + 4 controls + 4 kit arms, s311-D7 #312)`. `_build_all.py --selftest`: `exact-ID failure routing over 169 steps`. `_validate_wiring.py`: `61 gate script(s) … 57 wired · 4 exempt · 0 failure(s)`. `_validate_help_gate.py`: `272 script(s) scanned`, OK.

Kit outside the repo (a tempdir copy, no `knowledge/`): the starter `PASS … binding rows 17 (0 with their component named …) … unmapped 121`; a button row filled the way the brief's example shows (`state` and `surface` left null and echoed in `unmapped.props`) `PASS … token rows 1`; the same with `status: rendered` → `FAIL`; a `{color.grey.600}` token row → `⛔ … PRIMITIVE palette path`; a missing neighbour file → `⛔ missing file`.

## Decisions a lane made, for the record (none of them Dave's)

- Cohort-one names to slugs (L's brief: take the nearest and say so): menus → `dropdown`, select → `dropdown` (one meta: its non-native family and its native variant), switch → `selection-controls`, text input → `input-fields`, dialog → `modals`, notification → `notifications`. So cohort one is 14 metas, not 15, and with the four parts that once had empty placeholder slots (table overlaps) the kit lists 17 parts. `parts.json` records `askedAs` on each.
- The meta corpus the unmapped list is held complete against is every `knowledge/components/*.meta.json` except `EXAMPLE-*` (138). Alias seats (`kpi-tile`, `stat-card`, …) are included by slug; a screen using `cn-kpi-tile` is graded under that slug.
- Unmapped fallback for all 134 is `none`, so a composed screen for Sutherland is refused today. Declaring `apollo-native` is a per-part decision, not a default a lane invents.
- A null prop that is echoed in the binding's `unmapped.props` is a CLOSED gap (allowed at any status); a null that is not echoed is an OPEN hole (counted, allowed only at unverified). The schema text says so.
- The token map's seed files (`knowledge/tokens/_manifests/sutherland-diffs.json`, `sutherland-fixtures.json`) name Figma variables, not Sutherland's code tokens, so they are cited in the resolver description and not carried as rows.
- `tokens.resolver` follows the DTCG Resolver Module draft shape (named sets with `$ref` sources, `resolutionOrder`), kept to the keys the schema can police; J's DTCG generator does not change the paths the map resolves against.

## Owed, named

1. The empty `codeBindings` placeholder slots in `cards`, `list-items`, `status-indicator`, `table` metas STAY (they are L's today). Their removal is owed to the first release whose gate reads the manifest; `$legacy` on each row carries them verbatim until then. They hold no mapping, so nothing is lost when they go.
2. The receipt-mint consumer (`gen_provenance_receipt.py` recording which library rendered each part) is named in the gate's docstring as owed, not built; today the gate's readers are `test_gates`, `_build_all` STEPS and the on-demand `--screen` mode.
3. The generated theme file for Sutherland (reads J's DTCG tokens) — Friday's day-one win per the brief, not today.
4. `s311-D7` stamp enacted by AC with the landing sha (`--set-status`); the born-closed row via `notes/_lanes/312/N/add_state_row.py --write`.
5. The pre-push survey chunk `141:167` becomes `141:169` with the two new STEPS (the chain re-derives `len(STEPS)` at the wrap).
6. When the pack manifest is next re-probed, this gate will refuse with exit 77 in a pack (no `adapters/`) and classify REPO-BOUND; that is the designed verdict, not a defect.

## Found, not fixed

- No composed screen in `knowledge/_fitness-test/` carries a `#provenance-receipt`, so the screen check reads parts from `cn-<slug>` scopes rather than from a receipt; when receipts land, AD-009 should read the receipt first (s234-D6's posture).
- `metric` is the only cohort-one meta with a `slots` block; the kit's brief therefore allows one added `children` slot row where a part takes content and the meta lists none. That is a gap in the metas' slot coverage, not the kit's.
- Only `date-picker` declares `behaviour.events` among the 17 parts; the others carry no event list for the agent to map. Phase 1 (L2's `emits` extraction) fills that.
- `git status` was run once in this cloud worktree out of habit; it is harmless off the mount but the rule is noted.

## Ruling-shaped questions

- None that block. One for later: which unmapped parts should declare `fallback: apollo-native` for Sutherland so a mixed screen can pass the gate — a per-part call that belongs with the first side-by-side render, by his eye.

## Hand-off to AC (15:00 wave)

Named, changed paths: `adapters/schema.json`, `adapters/sutherland-react.json`, `adapters/kits/_build_sutherland_kit.py`, `adapters/kits/sutherland-react/{README.md,FIRST-PROMPT.md,BRIEF-FOR-COPILOT.md,manifest.json,parts.json,apollo-tokens.json,schema.json,check_manifest.py}`, `knowledge/_validate_adapter.py`, `knowledge/_tests/test_gates.py`, `knowledge/_build_all.py`, `notes/_lanes/312/N/add_state_row.py`, this report. Then `python3 notes/_lanes/312/N/add_state_row.py --write`, the `s311-D7` stamp, and `python3 knowledge/_wrap_commit.py unlock --tag 312-AC` after the gate run. The zip `sutherland-react-kit.zip` is in outputs only, not for the repo.
