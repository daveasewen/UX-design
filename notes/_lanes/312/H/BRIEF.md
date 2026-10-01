# Lane H — #312 — Studio on paper — the permutation matrix researched, the Assembly and Studio modes drawn as a proposal

## REVISED 2026-10-01 12:00 BST by #311 lane R — supersedes the lanes and timing below

From Dave's 11:10 rulings (`s311-D3..D9`, `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md`), the two-lane seat rule (`notes/_REVIEW-311-X-why-the-night-was-slow-2026-10-01-v1.html`) and the fuel left (all models about 83%, Fable about 58% at noon, estimated). The revised plan: `notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html`. Seat rule for every lane: at most two lanes on the Mac, one of them the single committer AC; text and research lanes work in the cloud on a clone of the GitHub repo taken after the noon push and hand named paths to AC; a cloud lane never commits.

H3 DEFERRED (Friday or later). H1 and H2 landed overnight (`3756e3ec`, `3d32433a`, `c58749e9`). H3 was yesterday's first drop when the all-models line ran hot; it still is. Cloud only when it runs; committer AC.

The text below is the draft as written on 2026-09-30; its intent stands, its lanes and times are superseded where this section says so.

---

Draft brief written by #311 lane P (Fable) on 2026-09-30 for the Thursday burn (`notes/_PLAN-311-thursday-burn-2026-10-01-v1.html`, job H). The #312 conductor launches it on Dave's yes and may amend lane splits; nothing here is his ruling.

## The ask
Two of his Sunday ideas, noted and never worked: the permutation matrix (`notes/_receipts/2026-09-27-304-sq-permutation-matrix.md`, his 10:35–10:43 words: a matrix of options for a brief with a recommendation, catering for variance in structure and in the agent's decisions, "could it actually be built into apollos decision mechanism", "Okay add the note") and the Assembly/Studio modes (`notes/_receipts/2026-09-27-304-sq-assembly-studio-modes.md`, his 10:54 "the mode selection the first bifurcation would be 'Apollo assembly' and 'Apollo studio' with sub-modes below. What do you think? Can we expand on this", and 10:58: the names stand, Launchpad names the Gen-UI strand). Neither is ruled; both are ideas he asked to be expanded. The #280 matrix that got the explorer layout ruled is the precedent (`notes/_lanes/280/`). Not in scope: the Swiss taste layer — "Not for now but don't let me forget this" (`_CARRIES.md`, age 22) stands.

## Lanes × model, and what each owns
- H1 · Fable · research: morphological analysis and option matrices as decision instruments (Zwicky onward, current practice in design tooling), when a matrix helps and when it is noise (two or three axes, not 81 cells), how the axes are found from a brief (the decisions the agent would otherwise make silently), and a worked example on a real Apollo brief from `notes/_briefs/`; lands on how Explore in Studio would hand a pick to Assembly by promotion.
- H2 · Fable · the modes as a proposal: door at the start or lever mid-work or both; the sub-modes (Assembly: Compose, Adapt, Check, Hand off; Studio: Explore, Sketch, Propose, Review) tested against what the gates do in each; what it would mean for the pack and the generate skill; what is a place not a mode (the record).
- H3 · Opus 5.5 · the proposal page with his decisions overlay (copy the overlay from `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`), nothing decided on it.
Cloud workspace only; no seat. Commit seat AC, final wave; paths under `notes/`. The first job the conductor drops if the all-models line runs hot.

## Dave's one moment
None. One proposal page for whenever he wants to read it.

## Done when
Two research reports with sources and dates, one proposal page with calls and recommendations, no ruling touched.

## Hard rules (every lane, every seat)
- Repo: `$HOME/mnt/Projects--UX-design` on Dave's Mac through `mcp__remote-devices__device_bash` (never `UX-design--UX-design`); `timeout_ms` up to 178000 on long calls. Text-only lanes may run in the cloud workspace on a /tmp clone; anything that renders runs at the seat: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`, drivers with `executable_path=$RENDER_SHELL` (`_drive_chart_engine.py` needs the wrapper `outputs/310/A/drive_wrap.py` until job B fixes its channel).
- Never `git status`. Never `rm` in the mount (`/tmp` is fine, and you MUST clear your own /tmp clone when done; two clones at once is the seat's ceiling, root has 3.7G free). No push: the conductor pushes and reads CI back. Never read or write claude.ai Project memory.
- Commits only by the commit seat named in this brief: `SESSION_N=312 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile> <named paths>` (line 1 WITHOUT a `#312 date —` prefix; named, changed paths only, never a no-op `git add`; re-run with the Memento schematic if it regenerates; msgfile ends with the Co-Authored-By and Claude-Session lines the conductor gives you). After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 312-<seat>`.
- Pre-push routine before handing paths to the commit seat (worker checklist step 5, `s309-D7`): a /tmp clone, the chunked survey 1:12, 13:55, 56:140, 141:167 with `--include-mutating`, `test_gates`, `_validate_evidence`, the sliced state-contrast sweep when snippets or canon change (about 2 min a slice, three or four slices per call). Never survey on the mount.
- Single writers: `knowledge/canon/canon.css`, the 27 chart receipts, `knowledge/_state.json`, `knowledge/_rulings.json` = job A's commit seat only (it runs the regen serial once per wave; lanes never regenerate). `knowledge/components/*.meta.json` + `meta.schema.json` = job C's schema lane (morning) then job D's consumers lane (afternoon). `_edge_register.json`, `_kg_verbs.json`, `_validate_edges.py`, the explorer builder = job D. `knowledge/_wrap_*.py` + the capture-ritual runbook = job E. `apollo-launchpad/` = job C. `apollo-spider/dist` = job G. Anything else you need to touch that is not yours: stop and say so in your report.
- An inscription is not done until `python3 knowledge/gen_kg_titles.py --write` and `python3 knowledge/_render_rulings.py` run and commit with it. Adding or removing a component meta means re-basing ASSERT-009 in the same change (`notes/_lanes/309/cond/assert009_rebase.py`). A regen that appends to `knowledge/_graph-mark-observations.jsonl` commits it with the schematic. `_build_survey.py` appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD before any regen. `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes run `--check`, then `--land --ratified s305-D26`.
- Dave rules from plain prose and pictures, never ID codes. Nothing a lane builds "stands" until he has looked where this brief says so; nothing is inscribed without his word. Cite a source for every claim; a number is pasted from a run or not written.
- File your report at `notes/_subreports/2026-10-01-312-<lane>-<topic>.md` with a `COUNTS:` line, a `## Found, not fixed` section and a `## Ruling-shaped questions` heading (even if empty), and a born-closed store row (`s305-D40` form, see W-311a1 in `knowledge/_state.json`; use `_state.add()` via `_state.load()/save()` — `json.dumps(indent=2, ensure_ascii=False)+'\n'` round-trips the file byte-exact). The conductor reads only your `COUNTS:` line and headline: put the verdict there.
