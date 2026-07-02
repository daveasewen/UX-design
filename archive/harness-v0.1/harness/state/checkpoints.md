# Checkpoints — resumable run state

The output of each completed step, written before the run advances. Enables
partial resumption and isolates failures.

## What a checkpoint contains

- run id, step id, spoke, timestamp
- the validated output (or a pointer to it)
- the contract version it validated against
- gate result (pass / fail / escalate) if applicable
- the next step the orchestrator chose

## Invalidation rules (from HDS)

| Situation | Action |
|---|---|
| Transient error | retry only; keep prior checkpoints |
| Malformed input (type 2) | invalidate the upstream checkpoint that produced the bad field |
| Empty/again-from-scratch input | invalidate all; re-run from the first spoke |

## Resumption

On restart, the orchestrator loads the latest valid checkpoint chain and
continues from the next step — no re-running of completed, still-valid work.

## Portability

Checkpoints are plain JSON files (or whatever the deployment runtime maps them
to). Keep them engine-agnostic so a run authored here can resume on the agency
machine or on Promenaut.
