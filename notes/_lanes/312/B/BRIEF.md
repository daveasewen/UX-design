# Lane B — #312 — The reworks from his picture page — nine parts, the third red, the 29 forks, the loose ends

## REVISED 2026-10-01 12:00 BST by #311 lane R — supersedes the lanes and timing below

From Dave's 11:10 rulings (`s311-D3..D9`, `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md`), the two-lane seat rule (`notes/_REVIEW-311-X-why-the-night-was-slow-2026-10-01-v1.html`) and the fuel left (all models about 83%, Fable about 58% at noon, estimated). The revised plan: `notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html`. Seat rule for every lane: at most two lanes on the Mac, one of them the single committer AC; text and research lanes work in the cloud on a clone of the GitHub repo taken after the noon push and hand named paths to AC; a cloud lane never commits.

B1–B4, B6, B7, BV DEFERRED to Friday 2026-10-02 07:30 (renders in four themes at the seat; the Fable fuel goes to L today). Not superseded by `s311-D3`: the hand edits become what the emitter must reproduce byte for byte; B1's date picker lands before phase 2's first cohort (button, tabs, table, date picker, metric) converts. B7 loses one item to phase 2: `snippet_theme_css()` projecting an option is the emitter's job once snippets are generated. B5's picks remain a proposal (rows 9, 10, 29 wait on Dave). Committer Friday: AC (seat).

The text below is the draft as written on 2026-09-30; its intent stands, its lanes and times are superseded where this section says so.

---

Draft brief written by #311 lane P (Fable) on 2026-09-30 for the Thursday burn (`notes/_PLAN-311-thursday-burn-2026-10-01-v1.html`, job B). The #312 conductor launches it on Dave's yes and may amend lane splits; nothing here is his ruling.

## The ask
`s308-D1..D15` (his 08:05 export `notes/_lanes/307/DAVE-RULINGS-2026-09-29-what-you-asked-to-see.md`, inscribed by `notes/_subreports/2026-09-29-308-I-inscribe-15.md`) left twelve work rows, none built:
- `W-308i1` the tree's chosen mark per theme (red in Supercharge and Common, black in Console and Mono); `W-308i2` the today ring inside the chosen square on the calendar, the date picker follows; `W-308i3` the standing-order / Direct Debit row as a list-items variant; `W-308i4` the range slider as Slider's two-handle form; `W-308i5` the rating reworked, not deleted; `W-308i6` the transfer list reworked then promoted; `W-308i7` the split button promoted; `W-308i8` the floating add button reworked then promoted, its three stray body rules in canon.css repaired (`W-307qy`, `s307-D55`); `W-308i9` back to top's reference page reworked then promoted.
- `W-308ia` the third red in mono, #A8000B, investigated on its own (not folded).
- `W-308ib` the 29 colour forks settled within his rules, each checked for halation and contrast (`reviews/_rag_bloom_model.py`; load it as `notes/_lanes/310/C/bloom_options.py` does). Anything not settleable within a ruling on record comes back as a question on the page, not a change.
- `W-308ic` the cold run's three fixes (the rerun itself is job G's).
Loose ends found and not fixed this week, one lane: the banking demo's filters onto one row (`.ftb-row` → `.ftb-primary`, `W-309g3`); the receipt page's blank arrow (`#metric-up` undefined), missing chart script and the splice markers that drop a rule each (`W-309g4`; the one-tile group is his, leave it); the masthead search/account buttons without `.nv-btn` (0×0 SVGs); Template-error's hard-coded `--surface:#1F1F1F` in dark; `snippet_theme_css()` cannot project an option so the showroom panes cannot show one; `_drive_chart_engine.py` hard-codes `channel="chromium"` (take the seat's `$RENDER_SHELL`); the avatar disc 1.03:1 on grey tiles; an `add` subcommand for `knowledge/_state.py` so rows stop being hand-inserted. Sources: `notes/_subreports/2026-09-30-311-A-*.md` and `-311-B-*.md` § Found, not fixed; `_HANDOFF-161` items 3 and 7.

## Lanes × model, and what each owns
- B1 · Fable · tree mark + today ring (`W-308i1`, `i2`), Calendar and Date picker snippets only.
- B2 · Fable · list-items variant for the standing-order row + the rating (`W-308i3`, `i5`).
- B3 · Fable · range slider + transfer list (`W-308i4`, `i6`).
- B4 · Fable · split button, floating add button (+ the three stray rules), back to top (`W-308i7`, `i8`, `i9`).
- B5 · Fable · the 29 forks (`W-308ib`), a table with the pick, the rule cited and the bloom score per fork.
- B6 · Opus 5.5 · the third red (`W-308ia`) and the cold run's three fixes (`W-308ic`).
- B7 · Opus 5.5 · the loose ends lane.
- BV · Fable · verifier: every reworked part rendered in four themes at the seat, before (HEAD~) and after, the manifest contrast pairs re-checked, the promoted parts' registrations checked, canon.css diff explained line by line.
Commit seat: job A's (AC). Lanes hand named paths; they never regenerate canon.

## Dave's one moment
One review page in the evening: every reworked part before and after in the themes where the theme matters, a does-it-stand call each, the forks table, the third-red finding. Nothing stands until he has looked (`s308-D8..D11`: promotion waits on his eye). Same shell and publish route as job A's page.

## Done when
Nine parts reworked and rendered; the forks table complete with a pick or a question per fork; the loose ends fixed at source (each with its own line in the report); rows stay open until his eye except the loose ends, which close with receipts.

## Hard rules (every lane, every seat)
- Repo: `$HOME/mnt/Projects--UX-design` on Dave's Mac through `mcp__remote-devices__device_bash` (never `UX-design--UX-design`); `timeout_ms` up to 178000 on long calls. Text-only lanes may run in the cloud workspace on a /tmp clone; anything that renders runs at the seat: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`, drivers with `executable_path=$RENDER_SHELL` (`_drive_chart_engine.py` needs the wrapper `outputs/310/A/drive_wrap.py` until job B fixes its channel).
- Never `git status`. Never `rm` in the mount (`/tmp` is fine, and you MUST clear your own /tmp clone when done; two clones at once is the seat's ceiling, root has 3.7G free). No push: the conductor pushes and reads CI back. Never read or write claude.ai Project memory.
- Commits only by the commit seat named in this brief: `SESSION_N=312 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile> <named paths>` (line 1 WITHOUT a `#312 date —` prefix; named, changed paths only, never a no-op `git add`; re-run with the Memento schematic if it regenerates; msgfile ends with the Co-Authored-By and Claude-Session lines the conductor gives you). After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 312-<seat>`.
- Pre-push routine before handing paths to the commit seat (worker checklist step 5, `s309-D7`): a /tmp clone, the chunked survey 1:12, 13:55, 56:140, 141:167 with `--include-mutating`, `test_gates`, `_validate_evidence`, the sliced state-contrast sweep when snippets or canon change (about 2 min a slice, three or four slices per call). Never survey on the mount.
- Single writers: `knowledge/canon/canon.css`, the 27 chart receipts, `knowledge/_state.json`, `knowledge/_rulings.json` = job A's commit seat only (it runs the regen serial once per wave; lanes never regenerate). `knowledge/components/*.meta.json` + `meta.schema.json` = job C's schema lane (morning) then job D's consumers lane (afternoon). `_edge_register.json`, `_kg_verbs.json`, `_validate_edges.py`, the explorer builder = job D. `knowledge/_wrap_*.py` + the capture-ritual runbook = job E. `apollo-launchpad/` = job C. `apollo-spider/dist` = job G. Anything else you need to touch that is not yours: stop and say so in your report.
- An inscription is not done until `python3 knowledge/gen_kg_titles.py --write` and `python3 knowledge/_render_rulings.py` run and commit with it. Adding or removing a component meta means re-basing ASSERT-009 in the same change (`notes/_lanes/309/cond/assert009_rebase.py`). A regen that appends to `knowledge/_graph-mark-observations.jsonl` commits it with the schematic. `_build_survey.py` appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD before any regen. `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes run `--check`, then `--land --ratified s305-D26`.
- Dave rules from plain prose and pictures, never ID codes. Nothing a lane builds "stands" until he has looked where this brief says so; nothing is inscribed without his word. Cite a source for every claim; a number is pasted from a run or not written.
- File your report at `notes/_subreports/2026-10-01-312-<lane>-<topic>.md` with a `COUNTS:` line, a `## Found, not fixed` section and a `## Ruling-shaped questions` heading (even if empty), and a born-closed store row (`s305-D40` form, see W-311a1 in `knowledge/_state.json`; use `_state.add()` via `_state.load()/save()` — `json.dumps(indent=2, ensure_ascii=False)+'\n'` round-trips the file byte-exact). The conductor reads only your `COUNTS:` line and headline: put the verdict there.
