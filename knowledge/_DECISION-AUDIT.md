# _DECISION-AUDIT — validation ledger

*The provenance of the **audit itself**: which decision nodes have been correctness-audited, the
verdict, and the one-line basis. Complements `_LIVE-STATE.md` (lifecycle: live/dead) — this is
validation (right/wrong). Per **ADR-0007 §5** + method `_RUNBOOK-decision-audit.md`.
⚠️ **INTERIM — hand-maintained** until the generated system carries `validation:` states on nodes.*

*Append one line per adjudicated node. Verdict ∈ {vouched, amend, overturn, defer}. Auditor is
always a human (Dave) — the engine never sets `vouched`.*

---

## Coverage

| Tier | Scope | Audited | Vouched | Open (`unaudited`) |
|---|---|---|---|---|
| A — foundational | 7 ADRs + charter §4/§4b/§9/§9a + LIVE-STATE entries (~20) | 5 | 2 (+1 split-vouch, +2 amend) | ~15 |
| B — method/process | feedback+project memories, runbook rules (~30–40) | 0 | 0 | all |
| C — long-tail DS | ingest register (~462), `_DS-IMPROVEMENTS`, desk rulings | 0 | 0 | sample/on-touch |

**Status: Tier A batch 1 COMPLETE (2026-07-05).** Nodes audited: ADR-0006 (amend), charter §9/§9a (vouch+defer), ADR-0007 (vouch), ADR-0005 (vouch), `derivation-governance` (amend). Batch boundary — stop. Next: Tier A batch 2 (ADR-0001–0004, charter §4/§4b) in a fresh session. Re-audit obligations: the two amended nodes' edits re-enter `unaudited`.

## Ledger

`node-id · verdict · YYYY-MM-DD · one-line basis · auditor=Dave`

- **ADR-0006** (flexing-engine product shape) · **amend** · 2026-07-05 · spine (engine-over-agents, own-the-governance, flex-with-dials) sound and vouched, BUT the register dial still names the superseded "cool/warm/hot" looks-language (§Decision 2 + §Decision 5); amend to the §9 inference ramp (retrieve/extend/invent). Amended text re-enters as `unaudited` and must be re-audited. · auditor=Dave
- **Charter §9 / §9a** (register = inference ramp + provenance) · **vouch (framing) + defer (proven/safe status)** · 2026-07-05 · the *definition* is vouched (register = inference level not look; cardinal floor as leash; provenance-over-feeling; gestalt-stays-human). The claim that it is **demonstrated/safe is deferred**: no worked retrieve/extend/invent spread exists yet, and the safety machinery (isolated generation, divergence probe, mode-B self-check) is named-not-built. ⚠️ Deferred proof obligation must be tracked in `_LIVE-STATE` OPEN — "we can't forget this verification" (Dave). · auditor=Dave
- **ADR-0007** (project memory = temporal decision-graph) · **vouch** · 2026-07-05 · core diagnosis (context-staleness = unrecorded supersession edge) and lightweight-first / edges-over-storage discipline are proportionate and right; §5 anti-laundering guard is the load-bearing part. Noted residual: the node is vouched by the very process it authorises (circularity — no check exists outside the ADR-0007 frame); ceremony-weight + unbuilt-mechanism concerns tracked as OPEN, not correctness faults. · auditor=Dave
- **ADR-0005** (ratify knowledge-engine pivot) · **vouch** · 2026-07-05 · most-proven node in the batch — engine has actually run (gates green, 25 self-tests, cold-start reproducible, generalised to GOV.UK as an independent second system), so the pivot rests on more than the commit-count selection-effect. Reversibility means the forward market bet softening costs little. ⚠️ Ledger note: the token-store history-purge remains **conditionally-accepted, not resolved** (real brand values still in git history; risk holds only while repo stays private — external trigger). Keep visibly OPEN; do not treat as closed by association. · auditor=Dave
- **`derivation-governance`** (engine never derives-and-promotes) · **amend** · 2026-07-05 · core VOUCHED (promotion is human, never automatic/derived — the constitutional rule this audit itself embodies). Amended DETAIL: promotion is **not a single-person say-so into general canon** but a **staged, multi-human path** — inference-born candidates land in a **holding pen / sandbox**, are worked through, and reviewed **with colleagues**; an existing **"extension library"** concept can act as a *separate-but-connected canon* where emerging innovation matures, with promotion to general canon only if broadly useful. Not fully worked out (Dave) → OPEN thread: define the holding-pen / extension-library promotion process; connects to the ADR-0006 compounding-canon promote loop. Amended memory text re-enters `unaudited`. · auditor=Dave
