# Lane G — #312 — The re-cut candidate — the designer pack as it stands tonight, built as a candidate and cold-run, so Friday's cut is a click

## REVISED 2026-10-01 12:00 BST by #311 lane R — supersedes the lanes and timing below

From Dave's 11:10 rulings (`s311-D3..D9`, `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md`), the two-lane seat rule (`notes/_REVIEW-311-X-why-the-night-was-slow-2026-10-01-v1.html`) and the fuel left (all models about 83%, Fable about 58% at noon, estimated). The revised plan: `notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html`. Seat rule for every lane: at most two lanes on the Mac, one of them the single committer AC; text and research lanes work in the cloud on a clone of the GitHub repo taken after the noon push and hand named paths to AC; a cloud lane never commits.

DEFERRED to Friday 2026-10-02 (Dave's own words: the re-cut "towards the end of the week"; the cold runs are fresh sessions; the candidate should carry Friday morning's A and B work). The cut stays Dave's, on his machine, through the frozen-release gate. Committer Friday: AC (seat), final wave.

The text below is the draft as written on 2026-09-30; its intent stands, its lanes and times are superseded where this section says so.

---

Draft brief written by #311 lane P (Fable) on 2026-09-30 for the Thursday burn (`notes/_PLAN-311-thursday-burn-2026-10-01-v1.html`, job G). The #312 conductor launches it on Dave's yes and may amend lane splits; nothing here is his ruling.

## The ask
`s309-D4`, his 07:07 words Wed: "We'll recut towards the end of the week". The frozen v1.0.14 still names Kpi-tile and carries no kinds. Since it: Metric (`s309-D2`), the five kinds, the logos fix (`W-305v2`), the dark tiles (`s310-D3..D6`), the soft white and the tab strip (`s310-D7`, `D8`), the icons and Supercharge's page (`s311-D1`, `D2`, pending his eye), plus whatever jobs A and B land by the last wave. Two rulings ask for the cold run on it: `s307-D66` (run the cold-start once on the current pack and show me) and `s308-D15` (the three fixes — job B's B6 — then the fresh-session run again on the next cut, with Console). The harness: `notes/_lanes/304/R4c/harness/` (score, render, drive, compare) and its briefs under `notes/_lanes/304/R4c/`; it scored candidate 2 against v1.0.13 on 2026-09-27 (`notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html`). The manifest tool: `_gen_pack_manifest.py`; `READER_SHIPS_FROM` gates the reader. Build the candidate as a candidate, never frozen: the cut is his, through the frozen-release gate on his machine. Restate once on the verdict page the known collision: the store in the pack ships the Launchpad rulings (`W-305v2`; his Sunday word: "they don't get the release, only designers, dont fret").

## Lanes × model, and what each owns
- G1 · Opus 5.5 · evening, after the last wave commit and its CI read-back: the candidate zip from the manifest tool at the last green sha (say which), `--check` first; if a red stands at 20:00 build at the last green sha and say so.
- G2, G3 · Opus 5.5 · two cold starts in fresh sessions (one with Console), the `s308-D15` protocol, scored by the harness against v1.0.14; the pages and receipts filed.
- GV · Fable · judges the render pairs and writes the one-page verdict: cut or not yet, with the score table and what changed since v1.0.14.
Owns `apollo-spider/dist/` (the candidate name carries `-candidate`); touches nothing else. Commit seat AC, final wave; the zip stays untracked as the release zips are.

## Dave's one moment
The cut, Friday, on his machine, through the frozen-release gate. Never unattended. The verdict page is for the click.

## Done when
A candidate zip at a named sha, two cold-run receipts, harness scores side by side with v1.0.14, one verdict page with one call.

## Hard rules (every lane, every seat)
- Repo: `$HOME/mnt/Projects--UX-design` on Dave's Mac through `mcp__remote-devices__device_bash` (never `UX-design--UX-design`); `timeout_ms` up to 178000 on long calls. Text-only lanes may run in the cloud workspace on a /tmp clone; anything that renders runs at the seat: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`, drivers with `executable_path=$RENDER_SHELL` (`_drive_chart_engine.py` needs the wrapper `outputs/310/A/drive_wrap.py` until job B fixes its channel).
- Never `git status`. Never `rm` in the mount (`/tmp` is fine, and you MUST clear your own /tmp clone when done; two clones at once is the seat's ceiling, root has 3.7G free). No push: the conductor pushes and reads CI back. Never read or write claude.ai Project memory.
- Commits only by the commit seat named in this brief: `SESSION_N=312 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile> <named paths>` (line 1 WITHOUT a `#312 date —` prefix; named, changed paths only, never a no-op `git add`; re-run with the Memento schematic if it regenerates; msgfile ends with the Co-Authored-By and Claude-Session lines the conductor gives you). After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 312-<seat>`.
- Pre-push routine before handing paths to the commit seat (worker checklist step 5, `s309-D7`): a /tmp clone, the chunked survey 1:12, 13:55, 56:140, 141:167 with `--include-mutating`, `test_gates`, `_validate_evidence`, the sliced state-contrast sweep when snippets or canon change (about 2 min a slice, three or four slices per call). Never survey on the mount.
- Single writers: `knowledge/canon/canon.css`, the 27 chart receipts, `knowledge/_state.json`, `knowledge/_rulings.json` = job A's commit seat only (it runs the regen serial once per wave; lanes never regenerate). `knowledge/components/*.meta.json` + `meta.schema.json` = job C's schema lane (morning) then job D's consumers lane (afternoon). `_edge_register.json`, `_kg_verbs.json`, `_validate_edges.py`, the explorer builder = job D. `knowledge/_wrap_*.py` + the capture-ritual runbook = job E. `apollo-launchpad/` = job C. `apollo-spider/dist` = job G. Anything else you need to touch that is not yours: stop and say so in your report.
- An inscription is not done until `python3 knowledge/gen_kg_titles.py --write` and `python3 knowledge/_render_rulings.py` run and commit with it. Adding or removing a component meta means re-basing ASSERT-009 in the same change (`notes/_lanes/309/cond/assert009_rebase.py`). A regen that appends to `knowledge/_graph-mark-observations.jsonl` commits it with the schematic. `_build_survey.py` appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD before any regen. `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes run `--check`, then `--land --ratified s305-D26`.
- Dave rules from plain prose and pictures, never ID codes. Nothing a lane builds "stands" until he has looked where this brief says so; nothing is inscribed without his word. Cite a source for every claim; a number is pasted from a run or not written.
- File your report at `notes/_subreports/2026-10-01-312-<lane>-<topic>.md` with a `COUNTS:` line, a `## Found, not fixed` section and a `## Ruling-shaped questions` heading (even if empty), and a born-closed store row (`s305-D40` form, see W-311a1 in `knowledge/_state.json`; use `_state.add()` via `_state.load()/save()` — `json.dumps(indent=2, ensure_ascii=False)+'\n'` round-trips the file byte-exact). The conductor reads only your `COUNTS:` line and headline: put the verdict there.
