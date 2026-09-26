# #304 Run 4 seat 4a — the generate skill composes, the drafts are ready, the candidate is built

provenance: 304 · 2026-09-26 (Sat night) · seat 4a (Opus 5.5) · base HEAD 6af293df · read-only git, no commit, no push, no Project memory
status: skill rewritten in the tree; drafts written in the lane folder only; candidate v1.0.14 built in a scratch clone, reproducibly. Every test below was run at Dave's seat. Nothing in canon, the stores or apollo-spider/dist was touched by this seat.

## The answer

The pack's generate skill now tells an agent to compose from the graph and never to trace a template. Its first building step runs the reader, a decision table ties every part to the question it answers and the `when` clause and rulings that chose it, and the bento template is fenced as a reference fixture whose grammar may be borrowed but whose content may not. Every hard rule the old skill carried is still carried (65 of 65 anchors, measured against the old blob). The candidate zip carries the reader and the 638 rulings, and it rebuilds byte-identical from one command. Two nailed lines of Run 4 do not hold yet, and neither is the skill's doing: the pack builder's `--check` goes red because its Gumdrop stamp rewrites three historical rulings inside the Constitution, and `knowledge/brain/` is not in any ship group.

## For seat 4c: the candidate

- Zip: `$HOME/r4a-scratch/cand/out/Apollo-Spider-v1.0.14.zip` at Dave's seat (`/sessions/rcw-0115rtjy4mpbeejfbjiuhael/r4a-scratch/cand/out/…`), sha256 `2e82723788106d83033f72bc528905446b5b0b578a4c19447a7a90623551135d`, 21 MB, 1,784 entries. The unzipped stage is beside it at `…/out/Apollo-Spider-v1.0.14/`.
- What it is: base `6af293df` plus the rewritten skill, with `VERSION` and `MEMENTO_CUT_VERSION` set to v1.0.14 and the four Gumdrop/FIRST-SESSION literals swept, committed in the scratch clone only (candidate commit `d3578c68`, dated as the base commit so the sha is stable). Manifest sha `81e640e5…`, 1,779 files, gate probe ARMED and identical to v1.0.13's verdicts (41 runnable, 10 repo-bound, 4 needs-dep).
- It does NOT carry Run 3's in-flight canon changes (the builder reads a commit, and canon.css is being edited in the tree right now) and it does NOT carry the drafts (the reader has no overlay flag; adding one is a canon change). One thing changes between v1.0.13 and this candidate as far as a cold agent can see: the skill, plus the reader and Constitution it can now call.
- Rebuild (the scratch lives outside the mount and dies with the VM; about two minutes, one step per call):

```
bash notes/_lanes/304/R4a/build_candidate.sh prep [BASE_SHA]   # clone --shared + overlay + candidate commit
bash notes/_lanes/304/R4a/build_candidate.sh full              # full-tree stage for the differential arm (1 GB)
bash notes/_lanes/304/R4a/build_candidate.sh probe             # repeat until PROBE COMPLETE (R4A_CHUNK=secs per call)
bash notes/_lanes/304/R4a/build_candidate.sh manifest
bash notes/_lanes/304/R4a/build_candidate.sh bake              # build-designer-pack.sh --dry-run
bash notes/_lanes/304/R4a/build_candidate.sh check             # --check, pack-docs --strict, zip counts
```

Reproducibility was driven, not assumed: two builds from scratch gave the same candidate commit, the same manifest sha and the same zip sha. After Run 3 commits, run `prep <new sha>` and the rest to carry its canon.

## What the skill now tells an agent

In three lines: run the reader on the brief and treat its `unresolved` list as the work list; choose each part by the question it answers and the `when` clause true for your data, and write that decision table down; copy each chosen component's own snippet whole onto canon's layout grammar, never a template's body.

The mechanism was confirmed in code before the edit. The skills group ships every path under `apollo-spider/skills/` (`_gen_pack_manifest.py` `_groups()`), so the tree's skill is the candidate's skill and no second live skill exists. The reader group arms at `VERSION >= READER_SHIPS_FROM` ("v1.0.14", s279-D1). The old text is recoverable as blob `ed25805c` (`HEAD:apollo-spider/skills/generate-from-canon/SKILL.md`).

What changed, rule by rule. Rule 1a is new: compose, never trace; anything at `level: template` is a reference fixture, read for its grammar, and a template the seed names is read through its meta. Rule 2 keeps "copy the snippet" and scopes s230-D1 beat 3 ("zero invented markup") to the component, which is the reading #288's handoff said the pass condition had lost. Rule 3a makes "your style is harness only" checkable: the page places parts and never sizes them. Rule 7 cites s249-D5 ("No ragged layouts"). Rule 7a keeps the bento question and "a skip is a yes" word for word (the cold-start projections point at rule 7a by number), and replaces "splice the snippet … start from Template-dashboard-bento.reference.html and edit it down" with the wall's grammar as a class skeleton and a line that everything inside the tiles comes from the brief and the graph. Rule 18 now uses the chart engine that replaced the interim recipe (s249-D4, `dv-render.js`'s own header: "It REPLACES rule 18"), with the hand-geometry recipe kept as the last resort. The procedure gains step 2, the decision table, with a stated order (a false `when` rules a part out, then most claims true, then priority, then yields), and step 8 now measures geometry from the DOM as well as driving controls.

Dave's Thursday sentence set the boundary for what the skill does not say: "I don't want it to be a set of instructions as that should be part of the graph and I may share the prompt with the audience." None of his three observations is written into the skill as an instruction. They are drafted as graph entries below. Rule 3a and the geometry step are the old copy rule and s249-D5 made checkable, not his observations restated.

## Premise probe: what the reader hands a cold agent, and what "compose" means for a bento wall

Run on a CEO-dashboard sentence, the reader returned 13 winners and 14 alternates, 61 governing rulings and 48 obeys rows in 35,468 tokens, in 0.7 s. Three things in it shaped the skill:

- It put `component:template-dashboard-bento` in the seed ("slug words in the task: dashboard+bento"). Without rule 1a, the reader itself would hand a cold agent the template to trace.
- It left the chart role unresolved because the sentence named no intent. A typed per-panel run (`--intent change-over-time --shape "time-series × 1–5-series"`) resolves it, so step 1 makes `unresolved` the work list and shows that command.
- For one chart panel it returns five charts as winners (line, stacked-area, candlestick, combo, sparkline), which is R5's finding. Step 2's order is what picks one.

For a bento wall, composing means borrowing the grammar and not the content. The per-theme gutters live only under `:where(.cn-template-dashboard-bento) .tpl-page .c-bento.tpl-wall[data-bento-role="dashboard"]`, so the skill gives that scope and structure as a class skeleton. Driven at the seat against the candidate's canon.css, the skeleton gets mono 40/4, console 40/4 and supercharge 24/2, which are the s219-D1 defaults. The template file opened raw gets 40/4 in every theme, including supercharge. So the composed skeleton is more correct than a trace in supercharge.

## Test it hard: the cold dry-read

The checklist is the path an agent holding only the pack must walk. Every item was scripted in `notes/_lanes/304/R4a/verify_skill.py` and run against the candidate stage. Result: 7 of 7 PASS.

1. It can find the skill: `.github/copilot-instructions.md` in the pack indexes `skills/generate-from-canon/SKILL.md` (C7).
2. Every path and command the skill names resolves in the pack: 33 of 33 (C1). Globs are matched case-insensitively, as the skill's own rule says. The declared skips are the designer's `briefs/` folder, a token name and `path/to/…` placeholders.
3. The Run 4 nailed lines hold (C2): no "splice", no "edit it down", no "start from knowledge/snippets/Template…", step 1 calls the reader, templates are fenced as reference fixtures, rule 7a and the bento question survive.
4. Nothing ruled was dropped (C3): 65 anchor phrases read off the OLD skill are all present. The first run of this arm caught two losses, the `data-mode` root warning and the resize re-fit hook. Both are restored.
5. Every ruling id the skill cites exists in the pack's own `_rulings.json` (C4): 17 of 17.
6. The skill's reader and ASK commands run inside a copy of the pack's `knowledge/`, with no repo on the path (C5): 6 of 6 exit 0, no repo path leaks, and the live Constitution is 638.
7. What the skill describes exists (C7): the seed has every field it names, component rows carry id/when/snippet/meta/why/alternate, the grammar classes are in the pack's canon.css, the template meta carries `$bentoGrammar`, and the chart snippets carry `dvRender`.
8. The pack-docs gate finds nothing in the skill (C6). At first run it did find three bare names (`components/summary.meta.json` and two others) that the old skill also carried; they now have their `knowledge/` prefix. Pack-wide the gate reads 220 findings against v1.0.13's 219. The delta is all in runbooks changed since v1.0.13.

Not done by this seat: a spawned cold run. That is 4c/4f's job, and seat rules said spawn nothing.

## The drafts (lane folder only; Dave rules them Tuesday)

Folder: `notes/_lanes/304/R4a/drafts/`. `make_drafts.py` reads every current value live from the metas and writes the proposals. `check_drafts.py` rehearses enactment on a scratch copy of `knowledge/`. Result: 7 of 7 arms PASS.

`when-rules.proposed.json` covers 22 rows: R5's 18 dashboard parts, the dashboard frame, and the three parts observation C adds.
- Twelve rows are KEEP.
- Chart-line is AMEND: the two clauses on decision-page question 1.
- Data-grid is NEW: `records >= 2 AND needs in (sort, filter, select, edit)`, question 3.
- List-items is AMEND: `needs = none`, plus a proposed `records × fields` shape. The shapes store is closed, so that shape needs his word.
- Filter-toolbar-bar and footer are NEW.
- Template-dashboard-bento is ENACT-RULED. s272-D85 ratified its gate on 15 September and it never reached the meta. The prose half is where the graph, not the skill, says "compose, never trace".
- Modals, split-button and dropdown are NEW. Dropdown uses his own s270-D1 cut-off ("we use dropdowns for 5 and above").
- Button is AMEND: `actions <= 1`, this seat's addition for his eye.
- Five registry names are added by addition under s273-D4: `needs`, `layout.grammar`, `interrupts`, `actions`, `options`.

`observations.proposed.json` and `rulings.proposed.json` put his three Thursday sentences in graph form:
- A, the bento ground: eight `role_defaults_219.SUPERSESSIONS` rows (dashboard × four themes, pageBg grey→white, bentoBg transparent→grey). This is the layer s220-D2 and s222-D1 used, and the receipt is never rewritten. It comes with the meta text and the regen order. R6a's finding stands: this moves s219-D1's shipped default within s219-D3's rails and does not contradict s219-D3. The dark leg stays his.
- B, own size: a ruling whose `governs` names all 137 metas, so the reader's live Q1 join puts it into every seed's `governs`. R6a's wording is carried, and 4c's size check is its instrument.
- C, lightest pattern: a ruling over modals, split-button, dropdown and button, with the `when` rows above. Modals' "yields to" prose is what the yieldsTo derivation reads.

The rehearsal arms:
- T1: each patch changes exactly one field, textually.
- T2: no patched meta gains a schema error.
- T3: the resolver's failure set is the same six before and after (the schema page's inherited reds), and it counts the five new names (44 of 44).
- T4: all three ruling entries pass `_inscribe_ruling.py --dry-run` with placeholder ids.
- T5: role_defaults applies the eight rows and its selftest passes; the dashboard defaults read white/grey in all four themes.
- T6: R5's when-evaluator on the patched metas goes from 17/20 to 19/20 (variant A) and from 18/20 to 19/20 (B), with no regression, and 8/8 on new tests. The remaining miss is W18 as R5 wrote it, whose context cannot state "must be sorted" without the new field. Stated with it (W18n), the grid is picked.
- T7: nothing under `knowledge/` moved while the rehearsal ran.

## Findings for the conductor

1. The pack builder corrupts the Constitution it now ships. From v1.0.14 the stamp block in `build-designer-pack.sh` rewrites every "Memento — Gumdrop vX" literal in the stage. That now includes three historical rulings in `knowledge/_rulings.json` (for example "Memento cut = Memento - Gumdrop v1.0.0" becomes v1.0.14). `--check` goes RED on exactly that file, and the builder's own DRIFT line recommends syncing the repo copy, which would falsify his record. The fix is to scope the stamp away from `knowledge/_rulings.json`. That is build machinery, the cut seat's to take with a verifier. Not touched here.
2. `knowledge/brain/` is not shipped (0 files). It is in no group and not in `READER_CLOSURE`. The 145 principles and 30 polarities do reach seeds through `_ux_principle_nodes.json`, which ships. The plan's nailed line "the brain directory" is NOT NAILED until the ship list says otherwise, and that is a manifest change.
3. A canon defect that bites the demo prompt, which asks for Common: `gen_bento_role_vars.py` emits `[data-apollo-theme="legacy"]` only. So `data-apollo-theme="common"`, the name s227-D8 says new work emits, gets mono's 40/4 dashboard gutters instead of legacy's 24/4. canon.css carries 420 legacy selectors and 418 common. Run 3's territory.
4. The reader's own selftest reads 73 of 79 at HEAD, the same six reds in the tree and in the candidate (logos.md scope row, three logo/photo override bites, two verb-map bites). They are inherited and not this seat's.
5. The builder's checks on the candidate, for the record. Generator selftest: 248 bites, 0 fail (249 in the tree at v1.0.13; the one-bite difference was not investigated). Cold-host gate: 3 of 3 hosts PLACED. Pack-docs: advisory exit 0, 220 findings. `--check`: RED, finding 1. The demo-page gate was not run; it needs the render drive and is 4g's.

## Ruling-shaped questions for Dave (plain words, for the Tuesday pages)

1. The skill now reads your "zero invented markup" rule from 31 August as applying to each component, not to the page: copy each part's markup exactly, but write the page's arrangement yourself. Is that the reading?
2. Five new words for the when-rules (needs, layout grammar, interrupts, actions, options): can they go in, alongside question 3 on the when-rules page?
3. Should the button give way to the split button when an action has related actions beside it? That is the one draft row that did not come from your words or the probe.

## Changed files (for the commit seat)

Modified, tracked: `apollo-spider/skills/generate-from-canon/SKILL.md`. It is the only tracked file this seat changed. The other modified paths in the tree are other seats'.

New:
- `notes/_lanes/304/R4a/`: `NOTES.md`, `build_candidate.sh`, `verify_skill.py`, `verify-skill-results.json`
- `notes/_lanes/304/R4a/drafts/`: `make_drafts.py`, `check_drafts.py`, `check-drafts-results.json`, `when-rules.proposed.json`, `observations.proposed.json`, `rulings.proposed.json`
- this report

Commit-seat notes:
- The skill change ships only at a v1.0.14 cut, which is Dave's word. The frozen v1.0.13 zip is untouched.
- The doc-row gate will want a row for this report.
- Scratch outside the mount (not for the commit): `$HOME/r4a-scratch/cand/` (clone, stage, zip, logs). The full stage and the enactment scratch were deleted to give back 1.1 GB.

## Replay

```
PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/304/R4a/drafts/make_drafts.py
PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/304/R4a/drafts/check_drafts.py
PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/304/R4a/verify_skill.py $HOME/r4a-scratch/cand/out/Apollo-Spider-v1.0.14 [<unzipped v1.0.13 stage>]
git --no-optional-locks show HEAD:apollo-spider/skills/generate-from-canon/SKILL.md   # the old skill
```
