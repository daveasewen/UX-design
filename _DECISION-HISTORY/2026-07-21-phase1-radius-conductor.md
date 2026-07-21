# 2026-07-21 — Phase 1 conducted: the parallel model's first full live-fire (dated from `date`, 22:33 BST)

*Conductor-session dossier. The WORKER arcs live in their receipts —
`notes/_receipts/2026-07-21-worker-A-radius-phase1.md` (radius + the F-series findings + three Dave
rulings enacted live) and `…worker-B-radius-phase1.md` (radius + the Button-mirror rebinds +
Video-player theming) — this dossier records only what the CONDUCTOR saw: how the parallel model
behaved under load, what broke, what held, and the wiring finding. Spine entry: `_LIVE-STATE.md`
LATEST DELTA 2026-07-21 (late night, Phase 1). Ledger: R-D22 + R-D16 reconfirm in
`knowledge/_proforma/_RAG-DECISIONS.md`.*

## Finding 1 — a chat TITLE got read as a role assignment (misfire, caught by Dave)

The Phase-0 handoff's forward title ended `[conductor + 2 Fable workers]`. A fresh session opened
with that text self-assigned CONDUCTOR — while this session already held the seat (Dave had picked
Conductor + 2 workers on the AskUserQuestion). Two conductors = two writers of shared state, the
precise clobber `_RUNBOOK-parallel-conductor.md` exists to prevent. Dave spotted it from the other
session's routing announcement; fix was a one-line stand-down paste that re-seated it as Worker A
(no session wasted — it went on to run the A brief and take three live rulings from Dave).

**Why it happened:** the forward title describes the PHASE's topology, and the handoff §C was
written before any next session existed — so "the next session is the conductor" was true when
written and false once this session took the seat. **Inscription (this capture): titles are LABELS,
never role assignments; the role comes from Dave's opener line only.** Written into
`_RUNBOOK-parallel-conductor.md` (trigger section) and the capture ritual's step 4b.

## Finding 2 — the receipts + reconcile discipline worked exactly as designed

Both workers finished with receipts at the conventioned paths; every one of the 92 dirty paths was
attributable (mine / A's / B's / regeneration) before staging — including three paths I did NOT
expect (`semantic-colour.json`, both theme override files, a new review sheet), all of which turned
out to be Dave ruling LIVE inside the worker sessions, receipted with verbatim quotes. The
`MIGRATED_SNIPPETS` shared-file race (both workers editing `_validate_radius.py`) merged clean —
21/21 basenames present, B's receipt even logged watching A's entries appear mid-session. Neither
worker's final build was guaranteed to postdate the other's final edit (A's provenance note said so
explicitly), so the conductor re-ran the full chain post-merge: green.

**The one real hazard for the divvy plan:** shared files. It merged fine this time because edits
were append-shaped and both workers read fresh; the standing practice now says the divvy plan NAMES
shared files and assigns each to one lane (or to the conductor).

## Finding 3 — `gen_canon_components` is not in the build: snippet→canon RULE text doesn't self-heal

Worker B refined `.cn-tabs .indicator` onto the indicator role in the SNIPPET; canon.css kept
`control` through multiple green builds. Cause: `_build_all.py` runs the VALUE projectors
(`gen_snippet_tokens`, `gen_theme_cascade`) but not the components-block generator — rule-text
changes in snippets only reach canon when `gen_canon_components.py` is run by hand. The sync gates
check values, not rule text, so this class of divergence is silent. Conductor regenerated the block
(the designed mechanism — never hand-edit an AUTO block) and it healed in one run, all 40 scopes.

**Open question for the wiring (queued, not enacted):** should `gen_canon_components` join the
build (regenerate-always, like the cascade) or stay on-demand with a `--check` sync gate (like the
projector)? The `--check` shape matches the established pattern; a regenerate-always step risks
masking hand-edits. Queued in §C rather than decided at midnight.

## Finding 4 — Dave, on the working model (verbatim, mid-reconcile)

*"okay I think that this way of working helps with the context, maybe we should always be thinking
about how to divvy up the tasks in the handoffs, whether its with subagents or parallel chats."*

Adopted as standing practice (this capture): **every handoff carries a DIVVY PLAN** — what's
parallelisable, lane count + model per lane, what stays serial, and which shared files belong to
which lane. Today's evidence: three Fable windows (conductor + A + B), each with its own clean
context; the burn spread instead of one session hitting Red; receipts merged without loss. The
worker A session additionally demonstrated the model absorbs LIVE Dave rulings mid-flight without
the conductor in the loop, receipted well enough to inscribe from (R-D22's quotes came straight off
the receipt).

## Resolved state at close

Radius ratchet CLOSED (21/21, gate 0/0) · R-D22 + R-D16 reconfirm inscribed · ds-007/ds-008 logged ·
canon components block regenerated (tabs indicator agreement) · full build green, conductor-verified ·
commit `99833a2` (+ this capture's wrap commit). Open: the ruling batch for Dave (Console px · Legacy
AA-fidelity family ×2 · fold-or-keep · `tabs/active` · bigplay eyeball) · the composition/atom-retrieval
strategy call BEFORE Phase-2 fan-out (worker A's sharpest finding: atoms retrieved by VALUE, not by
RULE — organisms re-implement sub-buttons; scale-press doesn't propagate) · A's F1/F2/F5 enact-queue ·
tag-atom role reconcile · designer-pack v2.1 re-bake post-push.
