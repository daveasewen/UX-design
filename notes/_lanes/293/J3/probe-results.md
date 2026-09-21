# 293 · J3 — probe results

One question set (`questions-as-sent.json`), three artefacts, **three live requests, no retry**.
`state` = `{"artefact_path": <repo-relative path>, "page_text": <tag-stripped text, cap 6000>}`.
Model requested `jev-latest`; model answered `jev-1.13.0` on all three.

## Artefacts

| | path | text chars | truncated | ground truth (grep, before the calls) |
| --- | --- | --- | --- | --- |
| **P** | `notes/_lanes/292/H/design-system-map.html` | 2582 | no | 10 HAVE / 2 badged `Coming soon` |
| **N** | `notes/_lanes/293/J3/fixture-unbadged.html` | 2496 | no | 0 badges; both gap tiles relabelled `Held`; prose still says the two are "not held in this repository today" |
| **M** | `notes/_lanes/293/J3/fixture-one-unbadged.html` | 2583 | no | 1 badge (tile 02); tile 11 un-badged and un-faded; prose untouched |

Both fixtures are byte-derived from P by deterministic string replacement — see `../../293/J3/` and the diff in the subreport. Nothing was hand-written.

## Answers

| artefact | Noul A `marks_every_gap` | Noul B `claims_unbuilt_as_available` | Score `absence_honesty` | confidence | probabilities 0/1/2/3 | latency (measured) | request id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **P** | **0.85** | **0.13** | **2.99** | 0.99 | 0.0 / 0.0 / 0.0 / 1.0 | **584.1 ms** | `req_01a0c464fc6873479f8bf2234d75c0f2` |
| **N** | **0.12** | **0.89** | **1.66** | 0.34 | 0.0 / 0.48 / 0.39 / 0.13 | **620.9 ms** | `req_01a0c464feec7a38a0a5de2293b5c200` |
| **M** | **0.82** | **0.21** | **2.92** | 0.92 | 0.0 / 0.01 / 0.06 / 0.93 | **578.9 ms** | `req_01a0c4650126737e9d77feece43a8e15` |

Tokens: 4,023 input / 177 output across the three calls (measured, from `usage`).

## Discrimination

- **P > N: yes, hard.** Score 2.99 → 1.66. Noul A 0.85 → 0.12. Noul B 0.13 → 0.89.
- **M > N: yes.** 2.92 vs 1.66.
- **P > M: NO.** 2.99 vs 2.92, Noul A 0.85 vs 0.82, Noul B 0.13 vs 0.21. M was built to land at level 2 and landed on level 3 with 0.93 of the mass. **The ladder collapsed at the P/M boundary.**

## Why M failed to separate — the instrument, not the rubric

M's mutation is **almost entirely invisible in `state`**. Tag-stripped, the only difference from P is that one line (`Coming soon`) disappeared and nothing replaced it; the fade is `data-state="soon"` CSS, which `html_to_state` discards by design. Meanwhile M's key section still reads *"Two are faded and badged: User Research & Insights, and CX Principles."* So the text Jev was shown **still asserts that both gaps are marked**. Jev answered the state it was given correctly. The probe measured a cost of `html_to_state`, which lane J2 published as lossy and untested.

## Latency — measured vs declared, both published

| call | measured, wall clock incl. TLS | J2's measured | TypeSafe declared |
| --- | --- | --- | --- |
| P | 584.1 ms | 703.3 ms | 70–500 ms |
| N | 620.9 ms | — | 70–500 ms |
| M | 578.9 ms | 683.6 ms | 70–500 ms |

J3 mean **594.6 ms** over 3; J2 mean 693.5 ms over 2. **All five calls to date exceed the top of the declared band** — J3 by 1.16–1.24×, J2 by 1.37×. J3's three calls were consecutive on a connection already warmed by the session, which is the most likely reason they sit ~100 ms below J2's; that is a hypothesis, not a measurement (no warm/cold control was run). n = 5.
