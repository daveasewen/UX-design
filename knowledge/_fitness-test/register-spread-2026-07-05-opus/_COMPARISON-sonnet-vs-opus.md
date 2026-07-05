# §9 worked spread — Sonnet vs Opus re-run, 2026-07-05

*Same signed contract (`_TEST-BRIEF-v2-sme-payments.md`), two variables changed at once per Dave's
choice ("full 3-band spread, Opus"): (1) the contract's Sober bullet gained an explicit, mechanical
**canon rigour tier** rule (prefer gate-reviewed `.cn-*` over the never-reviewed `.c-*` utility
layer); (2) generation model switched Sonnet → Opus. This run tests both together, not in
isolation — if you need to know which one mattered, that's a follow-up test, not this one.*

## What Dave flagged in the first (Sonnet) pass

1. Sober was "dull" and didn't retrieve the right components — confirmed: it used the never-
   reviewed `.c-stat-grid` utility for the cash position instead of the gate-reviewed
   `.cn-account-card`, even though both exist in canon.
2. Expressive wasn't exciting enough.
3. Open question: is there a build→review→correct loop, and would Opus do better?

## Result 1 — the retrieval fix held, across all three bands

| | Sonnet sober | **Opus sober** | Sonnet balanced | **Opus balanced** | Sonnet expressive | **Opus expressive** |
|---|---|---|---|---|---|---|
| `.cn-account-card` used? | **No** | **Yes (7 refs)** | Yes | Yes (5 refs) | **No** | Yes (1 ref, as spec provenance for a derived hero figure) |
| Named `.cn-*` components | 7 | **9** | 7 | **9** | 3 | 4 |
| `.c-*` (never-reviewed) fallback classes | present (`.c-stat-grid` etc.) | **0** | present | 1 (`c-eyebrow`, layout glue only) | present | 1 (`c-row`, layout glue only) |
| Flagged/derived candidates | 0 (self-report claimed 2 — **not actually in the file**) | 2 (real, in-file) | 5 | 2 | 3 | 3 |

Every Opus band retrieved `.cn-account-card` for the balance display and named, in its own report,
which `.cn-*` alternatives it checked and ruled out before ever touching the `.c-*` layer — sober
now uses **zero** utility-layer fallback classes, versus relying on them for its centrepiece before.
This is the concrete fix for finding 1, not just a self-report — verified by grep against the actual
files, the same way the first spread's self-report/artifact mismatch was caught.

## Result 2 — expressive read as a bigger swing (needs Dave's eyeball, not just this table)

Opus's expressive band ("the reckoning wall") describes three full-bleed bands with real scale
contrast (a 76px display balance against 13px eyebrows), a full-bleed red slab as the deliberate
"centre of gravity" for the approval decision, and a 22°-angled seam derived explicitly from
brand-principles' "Angular" (Hexagon 45°/90°, type 22°) — versus the Sonnet version's angled
masthead + numbered section spines. Structurally: fewer named `.cn-*` components (4, down from
Sonnet's already-low 3 — expressive is expected to lean furthest from named components into bespoke
composition) and comparable flagged-candidate count (3 vs 3). **This is a text description of a
bolder swing, not proof of one** — the sandbox has no Chromium available to render a PNG for either
run, so this table cannot settle "is it actually more exciting." Open both `expressive.html` files
side by side and judge — that's the point of the mode-B self-check ("a human still signs the
gestalt").

## Result 3 — cardinal curbs held with zero violations, again, on both models

Same checks as the first spread, re-run on the Opus set: zero unexplained raw hex in live CSS (every
hex that appears is inside a comment citing the `var()` it derives from); zero `border-radius`
overrides beyond `0` and the pre-existing round-dot exemption (8px status dots, canon-authored, not
new); zero ALL-CAPS; all four fixed figures (£122,450 / £45,200 / £72,748 / £106,302) present and
consistent in every file; masked refs held. **Neither model needed the "don't invent brand values"
guardrail relaxed to produce a bigger creative swing at expressive** — Opus went further
compositionally while holding the same floor Sonnet held.

## Result 4 — a genuine contract bug, caught independently by two Opus passes, missed by Sonnet

The contract's §3 said "Scheduled total: £106,302 (must equal the sum of the rows)" — but £106,302
is the sum of **all 5** rows (2 awaiting-approval + 3 scheduled), while the 3 rows actually labelled
"Scheduled" sum to only £56,600. **Both the Opus sober and Opus balanced passes caught this
independently** (sober fixed a caption that had mislabelled it; balanced flagged it in a comment and
rendered the correct £56,600/£49,702/£106,302 breakdown). Neither Sonnet pass flagged it. **Fixed in
the contract** (§3, this session) so it can't mislabel on-screen again. This is the clearest signal
in this test: two independent runs converging on the same real ambiguity is a genuine quality
finding, not noise — Opus's extra rigor caught something Sonnet's builds (and the original brief
author) missed.

## Answering the process question

**Is there a build→review→correct loop?** Still no — this remains one isolated generation pass per
band. But the Opus sober report shows self-correction *within* a single pass (it caught and fixed
its own maths-caption error before finishing), which is different from a designed loop but is
evidence Opus applies more internal verification during generation itself. **This doesn't replace a
real review-correct step** — it just means Opus needs it less on a per-pass basis. A designed
loop (generate → structural/curb check → patch → re-check) is still an unbuilt piece of the harness,
worth its own test once the model question settles.

## Net verdict

Both changes (rigour-tier rule + Opus) point the same direction as intended, verified against the
actual files rather than agent self-reports. This is **still one spread, one screen** — it doesn't
yet isolate which of the two changes did the work, and the "more exciting" question is explicitly
Dave's call to make by opening the files, not something a grep can settle. Recommend: Dave reviews
both `expressive.html` files directly; if Opus's spread reads better, that's a real signal to prefer
Opus for judgment-heavy generation passes per `model-selection-by-phase`, consistent with what that
memory already predicts (Opus for judgment, Sonnet for throughput) — this would be the first
concrete evidence for that split, not just the a priori assumption.

## Entry points

`_TEST-BRIEF-v2-sme-payments.md` (contract, now with the rigour-tier rule + the §3 fix) ·
`../register-spread-2026-07-05/` (the original Sonnet spread + its probe) · `sober.html` /
`balanced.html` / `expressive.html` in this folder (the Opus artifacts) · `_LIVE-STATE.md`.
