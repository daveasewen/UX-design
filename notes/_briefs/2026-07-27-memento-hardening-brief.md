# ENACTMENT BRIEF — Memento hardening (M-set, M3–M12)

provenance: local_1564cbbc-76e2-4d02-86a7-70254a6f5af4 · 2026-07-27
status: ruled — `notes/_MEMENTO-DECISIONS.md` § ★ M-SET (batch row + M7 read-back + routing amendment)

**For an OPUS window, solo, effort MAX — NOT Sonnet** (Dave, ruling window, verbatim in the ledger:
*"be careful and precise I don't trust sonnet, it cant think on its feet"*). No Sonnet subagents on
this set. **Every item carries a STOP condition — on any ambiguity: STOP that item, write the fork
into the wrap notes, move to the next. Never improvise on canon.** Price: ~35–45% of one window.
M1/M2 are ALREADY inscribed in `knowledge/_RUNBOOK-context-gauge.md` § Half 0b — nothing to do there.

**READ, don't reconstruct:** the ledger § M-SET → this brief → per-item pointers. Sandbox warts:
`_RUNBOOK-git-commit.md` § sandbox warts · build = ONE foreground call ≤45s · fresh sandbox loses
tiktoken — reinstall (`pip install tiktoken --break-system-packages`) BEFORE trusting any stamp.

## Sequence (dependency-ordered)

### 1 · M3 — build determinism: `knowledge/_instrument-fit.json`
Signature (observed #17): `git diff` after a clean build = pure key-order churn in
`dangling_citations` (`axs-003`/`aca-004`/`avd-006` swap positions; 5 ins/5 del, zero content).
Find the emitter (grep for `dangling_citations` in `knowledge/`), emit with sorted keys — the V2-P2
class (7 `sorted()` sites fixed 2026-07-26; this dict escaped that sweep). While in the file, check
its OTHER dict/set emissions once; fix what you SEE, don't enumerate speculatively.
**Proof:** build twice, `git diff --name-only` clean between the two. Receipt = the twice-clean
paste in the commit body.
**STOP if:** the churn source is NOT in an emitter you can point at (e.g. it's upstream data) —
that's a different disease; write it up, don't patch symptoms.

### 2 · M4a — view-as-table interim port (sparkline + scatter)
Two idioms live (grep receipts, 2026-07-27): SOLVED = `dv-tbl-toggle dv-vt dv-dd` button with
`aria-controls`/`aria-expanded` — `Chart-bar.reference.html:305,383,429,471,540` ·
`Chart-line.reference.html:325,423` · `Chart-combo.reference.html:304` ·
`Chart-donut.reference.html:281,344`. OLD = bare `<details><summary>View as table</summary>` —
`Chart-sparkline.reference.html:148` · `Chart-scatter.reference.html:163,230`.
Port the SOLVED form to the three old sites: copy from Chart-bar, rewire `aria-controls` to each
chart's own table id, bring the toggle's JS + any CSS the button needs (survey Chart-bar's pattern
in full FIRST — button + script + styles travel together). Snippets are canon: edit snippets, regen
showroom via the build, never hand-edit showroom.
**Verify:** build green + open both showroom panes + toggle works + type composites intact
(`.t-cm-chart-label`, not raw shorthand — gate-enforced).
**STOP if:** sparkline's inline-scale layout genuinely can't host the toolbar button — write the
fork (it may be a deliberate variant, Dave's call), port scatter only.
**Note:** the JS-off seg wart (§C·2 item 22) is a SEPARATE known issue — do not chase it here.

### 3 · M4b — accrete `chart-table-toggle` as an ADR-0013 partial
Observed duplication ×12 after the port — well past the accretion bar (ruling 3: accrete from
OBSERVED duplication). Follow ADR-0013 joining mechanics exactly: PARTIAL block in the owning atom ·
registry entry in `knowledge/component-types.json` · consumers get generated AUTO-PARTIAL blocks
(provenance-commented) · `gen_component_partials.py --check` green · ratchet green.
**STOP if:** the owning-atom choice is ambiguous (no obvious home atom for chart chrome) — the
accretion SHAPE is then Dave's call; ship M4a only and write the fork. Do not invent a new
atom-family convention on your feet.

### 4 · M6 — tiktoken auto-heal in `knowledge/_capture_gate.py`
On ImportError: ONE quiet `pip install tiktoken --break-system-packages` attempt (subprocess,
timeout ≤60s), re-import; on failure fall through to the EXISTING bytes/3.53 fallback labelled
ESTIMATE (unchanged — it is honest, keep its self-description). Selftest bite: the fallback path
must still be provably reachable (simulate missing module).
**STOP if:** the gate's selftest structure makes the bite awkward — add the install attempt only,
leave the bite as a written TODO for Dave's eyes; never ship an untested bite as if tested.

### 5 · M7 — §A size line: WARN-only, GROWTH-TRIGGERED (RULED, ruling window — Dave: "agreed")
**NEVER blocks.** Two triggers, warn only: **(a)** §A grew since the last wrap's stamped §A
measurement AND no banner line names a §A change — the steady state is SILENT, so it cannot
wallpaper; **(b)** backstop: §A > 4,500 tk (today: 4,208). Persist the per-wrap §A measurement
wherever the gate already records its stamp comparison. GM-D7-am's *"not even a guard banner"*
stays honoured: nothing in this item can ever force a §A trim.
⚠ **Hash convention, PIN IT here and in M5:** §A sha256 = lines `# §A` → line before `# §C`,
`'\n'.join` + trailing newline (= `999b1e3d…` today). A wrong-shape probe cost an abort at #17.

### 6 · M8 — banner-region sub-budget in the wrap gate
Region = file top through the line before `## ⬛ DO THIS FIRST` minus §A (i.e. the header + ★ LATEST
+ ★ PRIOR banners — reuse the gate's existing region parser; do NOT write a second one).
**warn 4,000 / block 5,000 tk.** Selftest bite each way.
**STOP if:** the existing parser can't isolate the region cleanly — a second parser is exactly the
drift class; write the fork.

### 7 · M9 — retirement receipts proxy + dreamer hunt line
(a) Wrap gate, ADVISORY first: every line REMOVED from DO-FIRST vs HEAD must appear verbatim (or by
batch key) in `_GM-ARCHIVE.md`. Promote to blocking only after it's seen working once.
(b) `.claude/agents/dreamer.md` § What to hunt, append: "**Retirements without receipts** — DO-FIRST
lines that vanished with no archive batch naming them." (dot-path is blocked to file tools — edit
via shell, per A-D5 precedent.)

### 8 · M10 — chain-level budget in the wrap gate
GM + `_LIVE-STATE.md` combined: **warn 24,000 / block 28,000 tk** (the D7 chain contract's number,
now enforced; chain measured 29,193 at #17 — expect the warn to FIRE until LS's next 2d roll trims
it. That first warn is CORRECT, not a defect: it is the contract finally being measured).

### 9 · M11 — dream-pass absence-signal line
`knowledge/_RUNBOOK-dream-pass.md`, after step 9: "**If a scheduled fire produces NO proposals file,
that absence IS the failure signal** — read the session transcript; nothing in the repo is at risk
(the pass's only output is the proposals file; promotion is Dave's alone)." Note beside it that the
conductor model is deliberately unpinned (dreamer IS pinned Opus).
**DAVE'S HALF (his, this week, before Sun 08-02):** fire `memento-dream-pass` once from the Cowork
UI, supervised — the scheduler+fresh-session path has never actually fired.

### 10 · M12 — register Memento v1 target
`_FUTURE-STATE.md`: "**Memento v1 shareable pack** — portable kit (capture ritual + gate + gauge
canon + dream-pass runbook + dreamer spec + GM/LS templates), project-agnostic. Blockers: M3–M10
landed · one clean unattended Sunday fire · MEMORY.md trim." Target, not started.

### 11 · M5 — build `knowledge/_gm_move.py` (the hardened mover)
Single mover ALL pass/wrap scripts use thereafter. Behaviours (each with a selftest bite that
proves it FIRES): line-start anchors ONLY (^-anchored; bare-substring = refuse) · §A sha256 assert
before/after every write, region located by HASH-SEARCH never line numbers · projected-line-count
guard (cap-aware: DO-FIRST 120/180, §C 150) · identical-string no-op = loud FAIL · all-or-nothing
(any assert fails ⇒ NOTHING written) · one-line receipt per move to stdout. Then: capture runbook
steps 2c/2d/2e reference it (edit the runbook lines that describe hand-rolled moves).
**STOP if:** wiring it into the runbook text requires re-describing the ritual — pointer, not prose.

### 12 · MEMORY.md trim (rides along IF this is a Cowork session with memory access)
19.5KB → 17.1KB target. Mechanics RULED: trim hooks + move whole entries to `MEMORY-ARCHIVE.md`,
NEVER delete memory files; dir is outside all repo mounts — file tools only, no shell.

## Acceptance (the whole set)
ONE foreground build `[62/62]` exit 0 · `git diff` clean after a SECOND build (M3 proof) · every new
gate check has a bite · `_capture_gate.py --wrap`: the git phantom-WARN GONE; expect M10's chain
warn to fire honestly · STAND-002 PASS · receipts per item in the commit body · ledger § M-SET gains
an ENACTED line naming what landed and what STOPPED · ONE commit via
`knowledge/_git_commit.sh --reconciled <msgfile>` · Desktop closed; Dave pushes the stack.
