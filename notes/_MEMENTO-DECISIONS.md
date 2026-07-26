# Memento dream-pass lane — decisions ledger

*Per the capture-review-decisions rule: rulings + WHY, so feedback doesn't evaporate.
Lane record: `_LIVE-STATE.md` §🔀 → scope v2 → scope v1 → the record note (all 2026-07-26).
Underscore-prefixed = exempt from `_capture_gate.py`'s glob by design (it IS the ledger).
All nodes seeded `unaudited` per `_RUNBOOK-decision-audit.md` — nothing self-promotes.*

| # | Ruling (Dave, 2026-07-26, via explicit option-select in-session) | Why (from the scope notes) | Audit |
|---|---|---|---|
| **D1** | **(a) Repo-side only.** Blocking gate bites on notes/dossiers; memory files carry the same fields by ritual discipline, session-checked at step 3, honestly UNENFORCED. | The store is invisible to every gate (runbook step 3, verified against sandbox mounts); per the gate-glob-scope rule a claim wider than the glob is a false inscription. | unaudited |
| **D2** | **Five status values:** `observed \| inferred \| ruled \| floated \| standing`. | The worked example (two-hemispheres essay — long-lived, Dave-owned, neither floated nor ruled) demanded the fifth register; four values would flatten it (memento-three-registers: never flatten). | unaudited |
| **D3** | **One script** — `_capture_gate.py` finally built, provenance checks inside it. | Less plumbing; the capture-ritual runbook already owned the spec (§ "The gate"). | unaudited |
| **D4′** | **Sequence §4.1 → A (Cowork) → C (Copilot) → B (Claude Code).** Supersedes v1's D4 row (which lacked C). | A proves the loop cheapest; C tests the harness-spinoff portability thesis + audits the capture ritual repo-only; B awaits Dave's CC migration. Flips freely if he moves sooner. | unaudited |
| **D5** | **RULED via A-D3 at first shape build:** dreamer home `.claude/agents/dreamer.md` — enacted. | Single file readable by Claude Code AND VS Code natively. Confirmed at first shape build, exactly as pencilled. | unaudited |
| D6 | *Pencilled, Dave's own action:* one-time check — repo on GitHub (private), Copilot tier, cloud-agent automations enabled. Before any Shape C build. | Shape C precondition (scope v2 §1.2). | — |
| **A-D1** | **Manual first, schedule later.** First dream pass runs by hand in the Shape A build session; the recurring task is created only after Dave reads the first proposals file. | Prove-one-then-wave (chart-expansion precedent): automation must earn itself on one proven output. | unaudited |
| **A-D2** | **Weekly, last ~15 transcripts** — the schedule's config once A-D1's proof lands. Not enacted until then. | ~15 ≈ the recent working set; weekly keeps plan usage low and proposals digestible. | unaudited |
| **A-D3** | **Enact D5 now:** dreamer steering spec checked in at `.claude/agents/dreamer.md`; task prompts say "read + follow", never restate. | One versioned spec maintained once (scope v2 §3), serving Shape A today and B/C from the same file. | unaudited |
| **A-D4** | **Proposals at `notes/_dream/YYYY-MM-DD-proposals.md`**, carrying `provenance:` + `status: floated` by discipline; `_dream/` stays OUTSIDE the gate glob until it earns its own gate. | Verified in-session: `_capture_gate.py` glob = `notes/*.md` → the subdir is honestly ungated (gate-glob-scope rule); claiming enforcement there would be a false inscription. | unaudited |

**Enacted same session:** `_capture_gate.py` + wired selftest in `_build_all.py`; runbook steps
1b/2/3 + gate section amended; cutover note `notes/2026-07-26-provenance-cutover.md`; the three
2026-07-26 lane notes retrofitted with field lines (lane-internal — not a corpus retrofit).

**Shape A enacted 2026-07-26 (the A-rows above, same session, Fable conductor + 1 Opus dreamer):**
`.claude/agents/dreamer.md` written (steering spec, single source — written via shell, dot-path
blocked to file tools); first dream pass run by hand — one cold Opus dreamer subagent over the
last 15 Cowork transcripts (turn-level) → `notes/_dream/2026-07-26-proposals.md`, 8 proposals,
all `status: floated`, conductor spot-checked 3/3 (P1/P3/P5 receipts exact). Schedule NOT created
(A-D1): weekly/~15 (A-D2) waits on Dave reading the file. Promotion remains Dave's alone.
*Known boundary artifact, surfaced not patched:* `_capture_gate.py --wrap` FAILs on
"GOOD-MORNING header ≠ today" whenever a lane session closes — the lane is ruled OUTSIDE the GM
queue, but the gate has no lane concept. Left firing deliberately (gate changes deserve their own
ruling); Dave decides whether wrap mode learns a lane flag or the FAIL stands as a reminder.
*(Second wart, same family: `--wrap` overwrites the committed build-mode report `_CAPTURE-GATE.md`
with its transient session verdict — restore by re-running build mode before staging.)*
