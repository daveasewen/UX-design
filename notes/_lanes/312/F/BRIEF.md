# Lane F — #312 — The pictures he is owed — one page that turns his stalled questions into calls with a recommendation each

## REVISED 2026-10-01 12:00 BST by #311 lane R — supersedes the lanes and timing below

From Dave's 11:10 rulings (`s311-D3..D9`, `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md`), the two-lane seat rule (`notes/_REVIEW-311-X-why-the-night-was-slow-2026-10-01-v1.html`) and the fuel left (all models about 83%, Fable about 58% at noon, estimated). The revised plan: `notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html`. Seat rule for every lane: at most two lanes on the Mac, one of them the single committer AC; text and research lanes work in the cloud on a clone of the GitHub repo taken after the noon push and hand named paths to AC; a cloud lane never commits.

RUNS TODAY as ONE Opus lane at the SEAT in series (F3 renders, F4 renders, F5 the page), the one seat slot beside the committer, from 12:30 to about 18:30. F1 and F2 landed overnight (`d4e6a1a9`, `e75c8c1e`) and feed F5. If renders run long, F5 ships with the pictures it has and names the rest as plain calls. Committer AC, 20:00 wave; paths under `notes/`.

The text below is the draft as written on 2026-09-30; its intent stands, its lanes and times are superseded where this section says so.

---

Draft brief written by #311 lane P (Fable) on 2026-09-30 for the Thursday burn (`notes/_PLAN-311-thursday-burn-2026-10-01-v1.html`, job F). The #312 conductor launches it on Dave's yes and may amend lane splits; nothing here is his ruling.

## The ask
274 of the 548 live rows are Dave's and the oldest stall because they need a picture. Draw them, one page, every call with a recommendation, most answerable by a click:
1. Container types — section, division, sector, panel (`W-308iw`, his 18:56 note Tue). Conductor's lean: section yes (a page region mapped to a landmark), panel already defined, division and sector no. Draw section and panel on the real demo.
2. Is the #261 nav family (sidebar-nav, tab-bar) a dashboard tile group? The bento-matrix selftest's bites R6e/R6d are red on it (`s308-D33` enacted in part, `8fe11818`); the selftest is held until he answers. Picture: the family on the dashboard, counted both ways.
3. The ring "set to fill" against the donut meta's "does not stretch" (`s305-D59`, `W-305n2`): his sketch, a 4px-grid scale with upper and lower bands, best size computed at build time. Draw the bands in four themes.
4. The list rule worked on its own (`W-305e1`, he answered Change) and the page-header lock-up (`W-305e3`): two or three drawn options each.
5. The top-nav shell as an IA question (`W-305e2`): top nav, mega menu for multiple levels, what hands over to what — explored rigorously, options drawn.
6. A header component for bento groups; can two intimately linked subjects form one group (`W-305e4`, `W-305e5`).
7. The rails half of call 9: the ramp word and its scope (`W-305w2`, `s305-D10` held).
8. The two token names `surface/section` and `notification/contextual/border/alpha` — accept or rename (`_CARRIES.md` residual, age 5).
9. The dark RAG roundels that paint pure white by policy while the ink softened (lane B's found item 2, `notes/_subreports/2026-09-30-311-B-*.md`).
10. Lane D's six (`notes/_subreports/2026-09-28-307-D-quick-18.md`): the Tabs width (`W-307ye`), a plain 0 corner or a token (`W-307qn`), which size rule trims the #245 image (`W-307qp`), the showroom focus ring as a token (`W-307q8`), the old canon gallery page and the runbook index date (`W-307q2`), which theme a generated fallback follows (`W-307q5`).
Left off on purpose: the interim pressed tile (`s310-D5`, waits on Figma); the §C·2 ruling batch (`W-305h3`, no picture would help).

## Lanes × model, and what each owns
- F1 · Fable · the top-nav shell IA exploration (item 5): options drawn as wireframes on the banking demo, a recommendation, the when-rule it implies.
- F2 · Fable · the list rule and the page-header lock-up (item 4): options drawn, a recommendation each.
- F3 · Opus 5.5 · renders: container types and the nav family on the real demo (items 1, 2), at the seat.
- F4 · Opus 5.5 · renders: the donut bands, the rails ramp, the roundels, the bento group header (items 3, 6, 7, 9), four themes, at the seat.
- F5 · Opus 5.5 · the page: shell copied from `notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html`, new localStorage key, one call per item with a recommendation, pictures inline as `<img>`, verified at 1440 and 390, Copy as text returns every call. Items 8 and 10 as plain calls.
Midday launch; nothing from the morning is needed. Commit seat AC, evening wave; paths under `notes/`.

## Dave's one moment
The page, when he likes (Friday morning is the natural slot). Nothing is built or inscribed until he answers; every call says a drawn option is not a ruling.

## Done when
One page, about twenty calls, each with a recommendation and the row it closes named; verified at both widths; published into the artifact by the conductor.

## Hard rules (every lane, every seat)
- Repo: `$HOME/mnt/Projects--UX-design` on Dave's Mac through `mcp__remote-devices__device_bash` (never `UX-design--UX-design`); `timeout_ms` up to 178000 on long calls. Text-only lanes may run in the cloud workspace on a /tmp clone; anything that renders runs at the seat: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`, drivers with `executable_path=$RENDER_SHELL` (`_drive_chart_engine.py` needs the wrapper `outputs/310/A/drive_wrap.py` until job B fixes its channel).
- Never `git status`. Never `rm` in the mount (`/tmp` is fine, and you MUST clear your own /tmp clone when done; two clones at once is the seat's ceiling, root has 3.7G free). No push: the conductor pushes and reads CI back. Never read or write claude.ai Project memory.
- Commits only by the commit seat named in this brief: `SESSION_N=312 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile> <named paths>` (line 1 WITHOUT a `#312 date —` prefix; named, changed paths only, never a no-op `git add`; re-run with the Memento schematic if it regenerates; msgfile ends with the Co-Authored-By and Claude-Session lines the conductor gives you). After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 312-<seat>`.
- Pre-push routine before handing paths to the commit seat (worker checklist step 5, `s309-D7`): a /tmp clone, the chunked survey 1:12, 13:55, 56:140, 141:167 with `--include-mutating`, `test_gates`, `_validate_evidence`, the sliced state-contrast sweep when snippets or canon change (about 2 min a slice, three or four slices per call). Never survey on the mount.
- Single writers: `knowledge/canon/canon.css`, the 27 chart receipts, `knowledge/_state.json`, `knowledge/_rulings.json` = job A's commit seat only (it runs the regen serial once per wave; lanes never regenerate). `knowledge/components/*.meta.json` + `meta.schema.json` = job C's schema lane (morning) then job D's consumers lane (afternoon). `_edge_register.json`, `_kg_verbs.json`, `_validate_edges.py`, the explorer builder = job D. `knowledge/_wrap_*.py` + the capture-ritual runbook = job E. `apollo-launchpad/` = job C. `apollo-spider/dist` = job G. Anything else you need to touch that is not yours: stop and say so in your report.
- An inscription is not done until `python3 knowledge/gen_kg_titles.py --write` and `python3 knowledge/_render_rulings.py` run and commit with it. Adding or removing a component meta means re-basing ASSERT-009 in the same change (`notes/_lanes/309/cond/assert009_rebase.py`). A regen that appends to `knowledge/_graph-mark-observations.jsonl` commits it with the schematic. `_build_survey.py` appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD before any regen. `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes run `--check`, then `--land --ratified s305-D26`.
- Dave rules from plain prose and pictures, never ID codes. Nothing a lane builds "stands" until he has looked where this brief says so; nothing is inscribed without his word. Cite a source for every claim; a number is pasted from a run or not written.
- File your report at `notes/_subreports/2026-10-01-312-<lane>-<topic>.md` with a `COUNTS:` line, a `## Found, not fixed` section and a `## Ruling-shaped questions` heading (even if empty), and a born-closed store row (`s305-D40` form, see W-311a1 in `knowledge/_state.json`; use `_state.add()` via `_state.load()/save()` — `json.dumps(indent=2, ensure_ascii=False)+'\n'` round-trips the file byte-exact). The conductor reads only your `COUNTS:` line and headline: put the verdict there.
