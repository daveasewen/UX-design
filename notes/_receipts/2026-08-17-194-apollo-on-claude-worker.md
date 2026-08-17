# Receipt — #194 worker window: Apollo-on-Claude architecture brief

status: worker output, UNCOMMITTED by design — the #194 conductor is the SOLE COMMITTER
(per `notes/_briefs/2026-08-17-194-window2-divvy-brief.md`). This window staged NOTHING,
committed NOTHING, pushed NOTHING, inscribed NOTHING.

provenance: Dave's word in this window — "okay lets spec this out as a worker, i need you
to leave receipts for a conductor window." ⚠ This lane is NOT the divvy's recommended
window-2 lane (ds-034/ds-035 homing); Dave directed it directly, which outranks the
recommendation. Declared, not smoothed.

## Exactly what this window touched (the conductor reconciles these two paths + this file)

1. `notes/_briefs/2026-08-17-194-apollo-on-claude-brief.md` — NEW. The spec: Apollo keeps
   full functionality; Claude is the interface. Engine = MCP server / judgment = plugin
   skills / surface = artifacts. FLOATED — five decisions (D1–D5) are Dave's, listed inside
   with a proposed lane divvy, DO-NOT-RULE list, and the mandatory pitfalls section.
2. `knowledge/_state.json` — ONE textual addition, row `W-34` (open, owner=dave, opened=194,
   closes_when = Dave rules D1–D5 or drops the lane). Written through `_state.add()`;
   `check()` ok; byte-identical round-trip PROVEN before write (indent=2, ensure_ascii=False);
   diff is +13 lines, zero deletions. ⚠ A first attempt reformatted the whole store
   (indent=1, 828/815 lines) — caught by diff, reverted via `git checkout` (delete grant was
   active so checkout's unlink worked), redone clean. [[serializer-defaults-reformat-the-file]]
   drove the catch.
3. Gates run: `_gate_doc_rows.py --check` GREEN (population 6, unrowed 0) — the new brief
   is rowed. `_state.check()` ok, no fails.

4. `reviews/APOLLO-ON-CLAUDE-BRIEF-2026-08-17-v1.html` — NEW (added after this receipt's
   first write, on Dave's ask). Swiss-system HTML rendering of the brief (Archetype B,
   blue accent — Dave's stable hue). A RENDERING, not a second source of truth; the .md
   stays canonical. Homed in reviews/ (outside the doc-row gate's brief glob), declared here.

## NOT mine — declared

- The 44 modified paths in `git status --short` at this window's stop-point (derived views,
  compliance JSONs, `_LIVE-STATE.md`, dashboard, etc.) predate/parallel this window and
  belong to the conductor's lane. Untouched by me.
- `notes/_briefs/2026-08-17-194-window2-divvy-brief.md` — the conductor's, read only.
- The chain's titled item (ds-0NN chart-intent reconciliation) was NOT opened.
- `.git/index.lock` husk from a prior process was cleared via the delete grant
  (`allow_cowork_file_delete`, runbook step 0) BEFORE the divvy's no-commit rule was read;
  no git object was written by this window at any point.

## What the conductor owes

- Reconcile + commit paths 1–2 + this receipt (msgfile headline suggestion:
  "Apollo-on-Claude architecture brief (W-34) — worker output, floated, awaits Dave's sitting").
- Present the brief's D1–D5 to Dave IN PLAIN PROSE — it is a sitting agenda, not a build order.
- Do NOT open lanes A/B/C from the brief before Dave rules D1 (whether this is a lane at all).
