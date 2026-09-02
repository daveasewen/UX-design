# #238 — LANE V: ADVERSARIAL VERIFIER of the polarity gate (bounded, `s172-D3`: depth cap 1, targeted proof)

Read `notes/_briefs/2026-09-02-238-COMMON-lane-rules.md` first. Then lane P's report `notes/_subreports/2026-09-02-238-P-polarity-gate.md` and its brief `notes/_briefs/2026-09-02-238-P-polarity-gate-brief.md`. Rulings: `s238-D1`, `D3`, `D5`, `D6`, `D7`.

Dave's instruction, verbatim: "just test the crap out of it please". You are the adversary. Lane P claims 55 arms red 45/45; your job is to find what its self-test cannot see.

## ATTACK, on copies under `/sessions/wonderful-adoring-euler/mnt/outputs/v238/` (nothing under /dev/shm survives a call boundary here — P finding 15; use the mount)
1. **Every refusal through the REAL entry points** — `knowledge/_validate_polarities.py --check`, the `_build_all.py` step (drive the step FUNCTION, never the whole build), and the `_git_commit.sh` "POLARITY GATE — s238-D7" block (invoke the block's function/script directly, never a commit). Same mutation, three doors: does each door go red by NAME with rc≠0 and nothing written?
2. **Hostile rows** the brief did not list: a `ref` that resolves only case-insensitively · a stub whose phrase is empty · a `links[].ref` to a `_rulings.json` id whose status is not `ruled` · a party role outside any vocabulary · a polarity whose parties are the same principle twice under different roles · a generated file with a hand edit that preserves length (content check must catch it) · `generated_at` in the future · an `additionalProperties` smuggle via a nested object · unicode-confusable ids (`pr-information-scent` vs a Cyrillic `с`) · a 31st row appended to `polarities.json` without a stub · the schema file itself mutated (`minItems` 2→1) · an empty `links` array (legal or not? say which the ruling implies).
3. **The migration table** — re-derive the 21 typed links from the frozen `apollo_touch` text with your own reading and diff against P's; every disagreement is a finding, not a fix.
4. **The sort** — P reports 6·4·20 against `s238-D6`'s predicted 6·9·15; explain the gap from the rules printed, or mark it UNPROVEN. Re-run `_derive_sort.py` and `_validate_polarities.py`'s status derivation side by side.
5. **The generated views** — is `polarity-edges.json` derivable to the byte from `polarities.json` twice in a row (determinism)? Does `--check` pass on the live tree right now?

## RULES
Depth cap 1: report, do not fix. You write ONLY your report and assets. Touch nothing under `knowledge/`. No git. Machinery price: every finding names the probe command that reproduces it.

## COUNTS
**attacks n · caught n · ESCAPED n · migration disagreements n · determinism ok/fail · live --check green/red · UNPROVEN n.** ESCAPED rows are the headline — list them first, each with its reproducing command.

## FILING
`X = V`, slug `polarity-verifier`. Stub back to chat per COMMON — ESCAPED list in full even if it breaks 12 lines.
