# Runbook — compile a criteria contract from a brief

*Written 2026-07-02 (window work, G2 from the north-star mock). The operating model's
first step made repeatable: **brief → criteria contract → the contract becomes the gates.**
Nothing generates before the contract is agreed.*

## What a contract is

One JSON file per run, stored at `runs/<run-id>/contract.json`. It is the definition of
done, written and agreed BEFORE generation. Every field either configures a gate or
records a licence. If a requirement can't be expressed as a gate config or a licence,
it goes to `advisory` (annotate) or `taste` (human) — it does not silently vanish.

## Compilation map (brief v2 section → contract field)

| Brief section | Contract field | Notes |
|---|---|---|
| §1 Intent & structural licence | `intent`, `flex[]` | licences are explicit permissions |
| §2 Register dial | `register` | single value or `spread` — never an adjective |
| §3 Immutable data | `correctness.figures` | verbatim; the sums that must hold |
| §4 Correctness rules | `correctness.rules[]` | each rule names its check: gate / advisory / taste |
| §5 Design system | `fixed[]` | curbs as token paths + the charter §4 ratified rules |
| — (charter, standing) | `gates.blocking`, `gates.advisory` | the tiered check list, exactly as `_build_all.py` tiers them |
| — (method, standing) | `tasteProtocol`, `promotion` | 20-second call on survivors; derive-and-flag policy |

## The sign-off rule

`agreedBy` starts null. A generation run against a contract with `agreedBy: null` is a
process violation — the run's outputs are T3 exploration at best. Agreement is recorded
as `{"agreedBy": "Dave", "on": "YYYY-MM-DD"}`.

## Status / honesty

The **compiler is not built** (G2 stays open until brief→contract is mechanical). This
runbook + the worked example (`runs/contract-001-sme-payments/contract.json`, compiled
by hand from `_TEST-BRIEF-v2-sme-payments.md`) are the spec for it. Second worked input:
the GOV.UK run (`second-system-govuk/`) shows the `fixed[]` block is system-relative —
the contract format must not hardcode HSBC token paths.

## Companion
`_FIXED-FLEX-CHARTER.md` (curbs, registers, tiering) · `_TEST-BRIEF-v2-sme-payments.md`
(the brief format) · `_validate_advisory.py` (where prose-rule checks live) ·
north-star mock region 2 (`_VISION-northstar-front-end_2026-07-02.html`).
