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
| A — foundational | 7 ADRs + charter §4/§4b/§9/§9a + LIVE-STATE entries (~20) | 0 | 0 | ~20 |
| B — method/process | feedback+project memories, runbook rules (~30–40) | 0 | 0 | all |
| C — long-tail DS | ingest register (~462), `_DS-IMPROVEMENTS`, desk rulings | 0 | 0 | sample/on-touch |

**Status: not started.** First run = Tier A batch 1 in a fresh session (see runbook §8).

## Ledger

*(none yet — first audit session appends here)*

`node-id · verdict · YYYY-MM-DD · one-line basis · auditor=Dave`
