# `#244`-`lane-C` — four Claude-owned debt items: lane records, the seam-block pointer, the mechanised `MEMORY.md` cap, one `s203-D1` read-back

session: `#244` · 2026-09-03
window: lane C (Claude-owned debt sweep, carried from #243)
sub index: `lane-C`
brief: in-chat lane brief (no `notes/_briefs/` file was cut for this lane)
tokens: `UNMEASURED — a subagent seat cannot read its own `message.usage`; no transcript path was given to this lane`

## VERDICT

All four regions are **DONE**. (1) `knowledge/_lanes.json`'s lane-2 `§C·1 strands (a)–(d)` step
moved `queued` → `active` with a receipt naming #244 lane A (nav/menu family, chart-expansion
wave 3) and lane B (radius tuner); `validate_lanes` clean, `_capture_gate.py::lane_routing_check`
green, `_validate_queue_fresh.py` PASS. ⚠ **ONE DECLARED OUT-OF-LIST WRITE:** the records edit
staled the GENERATED `§🛤 LANES` view, so `python3 knowledge/_gen_lanes.py` was run — **two lines
changed, both inside the `AUTO-LANES` markers**, no hand edit. (2) The carry-⑤ pointer is written
as one line in the `_LIVE-STATE.md` header zone naming lane P's copy as current and both #238/#239
copies as dated history. (3) `knowledge/_memory_cap_check.py` is built — `--path`, cl100k **tape**
end to end, `MEMORY_CAP_TAPE = 1802` derived from the measured live stub, `--check` non-zero over
cap, `--selftest` **13 bites OK incl. a break arm** — and WIRED as an **ADVISORY (warn) arm**,
copying the `SUBREPORT_CITE_BLOCKING` pattern exactly. (4) One `s203-D1` read-back run: `9628bae`
(#242) is **Failure**, recorded verbatim below with its run URL. Three read-backs remain owed.

COUNTS: findings 6 · ruling-shaped 2 · UNPROVEN 2

## What was done

**Item 1 — `knowledge/_lanes.json` lane-2 step state.** The `§C·1 strands (a)–(d)` entry moved
`"state": "queued"` → `"active"` and its `"receipt": null` → a receipt string that names the
staleness class, the three landed waves (#209 · #210 · #218), and **#244 lane A (nav/menu family,
§C·1 chart-expansion wave 3) and lane B (radius tuner)**, with the explicit clause that ACTIVE
means in flight, not shipped. `DV-J2b`'s `superseded` and `DV-J1`'s `landed` were **NOT touched**
— both are correct under `s190-D1` / Dave's word #191, and the brief's premise that they were the
stale part is wrong (see Finding 1). Consumers driven:

- `knowledge/_gen_lanes.py` `load_lanes()` → `validate errors: []`
- `knowledge/_gen_lanes.py --selftest` → `OK — 21 bites, every refusal fired, green controls held`
- `knowledge/_capture_gate.py::lane_routing_check('.')` → `FAILS: []` · note: *"lane-routing: GM
  eager ROUTING line agrees with 4 lane records (BLOCKING — O1′ #24; records are the truth)."*
- `knowledge/_validate_queue_fresh.py` → `RESULT: PASS — no §C·1 item's stated state is
  contradicted by disk or git.` (exit 0)
- `knowledge/_gen_lanes.py --check` → red immediately after the edit, green after the regenerate.

**Item 2 — the `_seam_block.sh` pointer.** One line inserted in `_LIVE-STATE.md` immediately after
the `WRAP DATE SPLIT` parenthetical (i.e. inside the 40-line header zone the wrap's
`"Last refreshed"` check reads, and above `## 🛤 LANES`), in the same `*(⛔ **TITLE:** …)*` form as
its neighbours. Nothing else in the file was touched. The `Last refreshed` line did not move and
still carries `2026-09-03`.

**Item 3 — the mechanised cap.** New file `knowledge/_memory_cap_check.py` (standalone CLI +
importable). Wiring: `knowledge/_capture_gate.py` gained `MEMORY_CAP_BLOCKING = False`, a
`memory_cap_check(repo)` returning `(warns, notes)` that IMPORTS `_memory_cap_check` (one
implementation, no second copy of the cap), and three lines in `run()` next to
`subreport_citation_check` using the house `(fails if X_BLOCKING else warns).extend(...)` form.

**Item 4 — the read-back.** Route kept off the Actions LIST view throughout (the ≈55,692-real
lesson). Cost: two page loads and four JS calls, no screenshots, no `get_page_text`.

Files touched (repo-relative to `/Users/daviewen/Documents/Claude/Projects/UX-design`):

- `knowledge/_lanes.json` — one sequence entry (state + receipt)
- `_LIVE-STATE.md` — **two separate writes:** the carry-⑤ pointer line (hand, authorised by item
  2) and the `AUTO-LANES` block regenerate (machine, `_gen_lanes.py`, 2 lines, declared)
- `knowledge/_memory_cap_check.py` — NEW, 221 lines (`wc -l`)
- `knowledge/_capture_gate.py` — `MEMORY_CAP_BLOCKING`, `memory_cap_check()`, 3 lines in `run()`

⚠ **NOT THIS LANE'S, DECLARED SO NOBODY ATTRIBUTES THEM HERE:** `git status` also shows
`knowledge/_graph-mark-observations.jsonl` (+24), `notes/_REHEARSAL-LOG.jsonl` (+1) and
`notes/_dream/_GRADE-DECISIONS.jsonl` (+1) dirty. Their mtimes are **15:36 / 15:46**, before this
lane opened (**15:57**) — another #244 seat's append-only logs, untouched by lane C.

## Findings

1. **THE BRIEF'S PREMISE FOR ITEM 1 WAS PARTLY WRONG, AND THE CARRY WAS RIGHT.** The brief called
   `DV-J2b: superseded` and `DV-J1: landed` stale. They are not: `superseded` is a legal step state
   (`STEP_STATES` in `_gen_lanes.py:47`, ruled `s190-D1`) and its receipt names the superseding
   ruling `s182-D2` as `validate_lanes` requires; `DV-J1: landed` is Dave's word #191 verbatim
   (*"call it landed, with a receipt naming both halves"*). The only stale field was the one carry
   ⑥ named — the `queued` line with `receipt: null`. **Probe:** `_gen_lanes.load_lanes()` returned
   `[]` errors on the file BEFORE the edit as well.

2. **THE RECORDS EDIT MECHANICALLY STALES `_LIVE-STATE.md`, SO ITEM 1 CANNOT BE DONE WITHOUT A
   WRITE TO A FILE THIS LANE WAS FENCED OUT OF.** `_gen_lanes.py --check` compares the
   `AUTO-LANES` block against the records and returned exit 1 with *"✗ _LIVE-STATE.md §🛤 LANES is
   out of sync with knowledge/_lanes.json"* the moment the JSON changed. `main()` writes ONLY via
   `spliced()` (verified at `_gen_lanes.py:306-307`), and the file's own contract is *"never
   hand-edit between these markers"*. The regenerate was run and the diff verified as **2 lines,
   both between the markers**. ⬛ Declared for the conductor to accept or revert. See RS-1.

3. **THE LIVE `MEMORY.md` STUB IS 1,502 cl100k TAPE — 42% OF LANE F's PRE-STUB 3,569.** Measured
   at `/sessions/practical-laughing-clarke/mnt/.auto-memory/MEMORY.md`: `1,502 tape · 4,884 B ·
   33 lines`. `s243-D1`'s stub therefore cut ≈2,067 tape off every seat's boot. ⚠ TAPE, NOT REAL —
   never summed with a `message.usage` figure.

4. **THE CAP FILE LIVES OUTSIDE THE REPO, WHICH IS WHY IT MUST NOT BE BLOCKING YET.** The index is
   a Cowork surface resolved by the `/sessions/*/mnt` glob (the same resolution
   `_boot_decompose.py:133` uses). On any non-Cowork tree there is nothing to grade, which is the
   [[gate-cannot-pass-in-one-environment]] shape. Absence is therefore emitted as a **declared
   NOTE** (*"DID NOT RUN … This is UNKNOWN, not a pass"*), never a warn and never a fail, and
   `resolve_path` returns exit code **2 = could not measure**, distinct from **1 = measured and
   over**. Driven: with `MOUNT_GLOB` pointed at a nonexistent path, `warns == []` and the declared
   note fired.

5. **THE WARN ARM FIRES — DRIVEN, NOT CLAIMED.** With `resolve_path` injected to return a 6,800-tape
   fixture and the REAL grader and REAL cap: `memory_cap_check('.')` returned exactly one warn,
   `memory-cap (ADVISORY): OVER CAP: MEMORY.md is 6,800 cl100k tape against a cap of 1,802 tape —
   +4,998 tape …`, and the fails list stayed empty. The `--selftest` break arm (an always-green
   grader substituted for `grade`) is CAUGHT, so the cap is load-bearing and not decoration.

6. **THE `s203-D1` VERDICT FOR `9628bae` IS FAILURE, AND IT IS THE THIRTEENTH CONSECUTIVE RED.**
   Recorded verbatim off the run page:

   > run URL: `https://github.com/daveasewen/UX-design/actions/runs/33752385428`
   > workflow: `gates` · run **#482** · `gates.yml` · `on: push`
   > commit: `9628bae` (`/daveasewen/UX-design/commit/9628bae6087069e95a9eef2e1dbf95e2ff7ee80f`)
   > branch: `master` · Triggered via push · daveasewen pushed
   > **Status: `Failure`** · Total duration `13m 57s` · Artifacts `1`
   > jobs: `gates 5m 10s` · `render 13m 18s` · `release 18s`
   > Annotations: **`5 errors and 1 warning`** — `release` → `Process completed with exit code 1.`
   > · `gates` → `Process completed with exit code 1.`

   #239's opener read run **#478 FAILURE** and every run **#227 → #238** as failed; #482 continues
   the streak. Last green remains `e7cf3db`. ⚠ **The FAILING STEP INSIDE each job was NOT opened**
   — that is the cap, deliberately. **Three read-backs stay owed:** `a09a3ea` (#240), `7f8801f`
   (#241), and #243's `7ad3a26` when it is pushed (it is local-only as of this lane).

## RULING-SHAPED QUESTIONS

1. **THE `AUTO-LANES` REGENERATE — IS A GENERATOR WRITE INSIDE A FENCED FILE AN EDIT?** This lane
   was fenced out of `_LIVE-STATE.md` except for the carry-⑤ pointer, yet item 1's records edit
   makes `_gen_lanes.py --check` red until the generated block is rewritten. Options: **(a)** a
   lane that edits records also runs the generator, because the block is a machine mirror and
   leaving it red hands the wrap a defect the lane created — the choice taken here, declared;
   **(b)** the lane leaves it red and the conductor runs one command at the wrap; **(c)** the fence
   is restated to name generated blocks as exempt from a file-level "no edits" instruction.
   **Recommend (c) as the standing rule**, because (a) and (b) both re-litigate the same question
   every time a sub touches a records file. **DAVE'S.**

2. **`MEMORY_CAP_TAPE = 1802` AND ITS 20% — THE BASE IS MEASURED, THE MULTIPLIER IS NOT.** 1,502
   tape is reproducible (`--measure`); the +20% is an agent's pick, stated as such in the
   docstring. Options: **(a)** leave 1802 advisory and let two or three sessions of readings show
   whether the headroom is right; **(b)** rule the multiplier now; **(c)** derive the cap the way
   `s240-D1` derives the boot band (a window of readings + σ) instead of a flat percentage.
   **Recommend (a) now, (c) once there are ≥5 readings** — a flat percentage on a single reading is
   the picked-constant shape this repo keeps catching. Promotion of `MEMORY_CAP_BLOCKING` to
   blocking is separately **DAVE'S WORD** and is gated on Finding 4's env question. **DAVE'S.**

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that `_capture_gate.py` still passes END TO END with the new arm — `--selftest`
  exceeds the ~178 s sandbox call wall (a skip carried from #243, unchanged by this lane). What WAS
  established: the module compiles (`py_compile`), imports, and `memory_cap_check` was driven three
  ways (green live · warn arm fires · declared-missing arm). Price to prove: one run outside the
  call wall, ≈**180-400 s** of wall time, no token cost to a lane.
- **UNPROVEN:** what actually failed inside run #482's `gates` and `release` jobs. The cap stops at
  the run page. Price to prove: two step-log opens, ≈**8-15K real** of FILL each; the #239
  uncapped route cost **≈55,692 real**.
- **CLAIMED:** that lane A is the nav/menu family (wave 3) and lane B the radius tuner — taken from
  this lane's brief, not read back off lane A's or lane B's own filed reports (neither exists yet at
  the time of writing). If either lane's scope changed, the receipt string in `_lanes.json` needs
  the correction at the wrap reconcile.
- **CLAIMED (declared, not repaired):** `_validate_wiring.py` remains at `1 failure` — #235's
  orphan `_validate_receipt.py`, unchanged and pre-existing. `_memory_cap_check.py` adds no new
  orphan because the wiring gate scopes to `_validate_*` / `_gate_*` names only.

## Evidence

No evidence files: every claim above quotes its probe inline, and each is re-runnable in one
command from the repo root. The four that matter:

```
python3 knowledge/_gen_lanes.py --check
python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print(g.lane_routing_check('.'))"
python3 knowledge/_memory_cap_check.py --selftest
python3 knowledge/_memory_cap_check.py --check --path /sessions/*/mnt/.auto-memory/MEMORY.md
```

REPLAY-THESE: Finding 6's verbatim run-page block (~350 tk — it is the `s203-D1` read-back Dave is
owed in chat, and a paraphrase does not discharge it) · RS-1, the `AUTO-LANES` fence question
(~300 tk) · `knowledge/_memory_cap_check.py` docstring provenance block (~450 tk, only if the cap
constant is to be moved)
