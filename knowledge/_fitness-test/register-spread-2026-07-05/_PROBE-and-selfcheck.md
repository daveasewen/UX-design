# §9 worked spread — divergence probe + mode-B brand self-check, 2026-07-05

*The first worked retrieve/extend/invent spread under the new §9 inference-ramp definition (the
"no worked spread exists yet" OPEN item in `_LIVE-STATE.md`). Screen: SME Payments
(`_TEST-BRIEF-v2-sme-payments.md`, reconciled to §9 language this session). Three bands generated
in **isolated, parallel passes** (separate cold agent contexts, none seeing the others or any prior
`_fitness-test/sme-payments*` variant) from the same signed contract. Files: `sober.html` ·
`balanced.html` · `expressive.html` in this folder.*

---

## TL;DR

The spread did what §9 predicts: **cardinal curbs held with zero violations across all three
bands; foundational curbs diverged in a monotonic, register-ordered way.** This is evidence the
inference-ramp framing is workable, not yet proof it's safe at scale (one screen, one spread — see
"what this doesn't prove" below). One real gap found: none of the three include the HSBC
logo/masterbrand mark — a shared limitation of the single-screen contract, not a register failure.
One process finding: the sober agent's self-report claimed two flagged-derivation comments that
don't actually exist in the file — self-report ≠ ground truth, verify the artifact.

## Divergence probe (structural, per §9 machinery)

| Signal | Sober | Balanced | Expressive |
|---|---|---|---|
| File size / lines | 15.9 KB / 336 | 27.7 KB / 435 | 21.0 KB / 401 |
| Named `.cn-*` components used | 7 (action-bar, eyebrow, headers, modals, status-indicator, summary, table) | 7 (account-card, eyebrow, modals, notifications, status-indicator, summary, table) | 3 (button, modals, table) |
| Flagged/derived candidates | 0 (self-report claimed 2 — **not found in file**, see below) | 5 | 3 |
| Motion/transition/animation mentions | 0 | 1 | 4 |
| `prefers-reduced-motion` present | no (nothing to reduce) | yes | yes |
| Raw hex colour in live CSS (leak check) | none | none (1 hex, in an explanatory comment only) | none (1 hex, in an explanatory comment only) |
| `border-radius` overrides | **0** | **0** | **0** |
| Heading structure | h1 + 5×h2 | h1 + 5×h2 (identical to sober) | 3×h2, no h1, numbered section-spines instead |
| Fixed figures present & consistent (122,450 / 45,200 / 72,748 / 106,302 / masked refs) | ✅ all, verbatim | ✅ all, verbatim | ✅ all, verbatim |
| ALL-CAPS text-transform | none | none | none |

**Reading it:** the two things §9 says should be *invariant* — cardinal curbs (brand colour
retrieved not typed, square corners, the correctness data) — came back **identical across all
three, with zero exceptions found by grep**, not just by agent self-report. The two things §9
says should *move with the register* — component-vocabulary purity (7→7→3, expressive drifting to
bespoke markup), motion (0→1→4), and composition (identical heading structure at
sober/balanced, restructured at expressive) — **did move, in the predicted direction.** This is a
genuine divergence, not three re-skins of one layout: expressive's information architecture
actually changed (no h1, section-spine numerals instead of eyebrows), where sober/balanced share
structure and differ mainly in confidence/density.

**Payments is a cardinal-heavy, narrow-road screen** (safety-critical figures, correctness rules)
— per the charter's own caveat, some clustering here is *expected*, not a failed spread. That
expectation held: none of the three touched the data layer differently; all the divergence is in
the foundational layer (composition, density, motion, component vocabulary), exactly where the
ramp says it should be.

## Mode-B brand self-check (advisory pre-flight, §9a — not a gate)

Six principles, checked against all three artifacts (file inspection; PNG render not available in
this sandbox — recommend Dave open the three HTML files directly to confirm visually, per the
project's own "review live HTML, not PNGs" rule):

| Principle | Sober | Balanced | Expressive |
|---|---|---|---|
| Square corners | ✅ zero radius overrides found | ✅ | ✅ |
| Tactically red (accent, not decoration) | ✅ red only on primary CTA/warn chip | ✅ red on hero balance is explicitly avoided (self-report), CTA only | ⚠️ red leads structurally (masthead fill, section numerals, hero figure) — matches "expressive releases red-forwardness," but is the outer edge of "tactical" |
| Clearly understood / single focal point | ✅ | ✅ (one hero balance figure) | ⚠️ multiple emphasis zones (hero + section spines + accent bars) — composition is intentionally busier, consistent with the band, worth Dave's eye |
| Internationally relatable | n/a (no imagery on this screen in any band) | n/a | n/a |
| Logical | ✅ | ✅ | ✅ |
| Creatively considered | ✅ | ✅ | ✅ |
| **Logo / masterbrand present** | ❌ | ❌ | ❌ |

**Logo gap — shared across all three, not a register effect.** `canon.css` only carries the logo
slot inside `.cn-navigations` (`--logo` var, `.cn-navigations .logo`); none of the three agents
built a nav/app-shell, because the contract scopes this as one screen, not a full IA. This is a
**contract-scope gap, not a §9 failure** — flag it for the next worked-spread contract (either
include the nav shell in scope, or note explicitly that a screen-level test excludes masterbrand
placement by design).

**Self-check verdict:** advisory pass with two things for Dave's eye (expressive's red-leadership
and busyness, right at the edge of "tactical") — exactly the "checks passed ≠ feels HSBC" caveat
this self-check exists to carry. Gestalt judgment is still Dave's, not the engine's.

## Process finding — self-report ≠ ground truth

The sober-band agent's self-report claimed: *"Two minor derivations flagged inline as HTML
comments."* Grepping the actual file for any flag/derive/candidate comment returns **zero
matches** — the derivations may have been reasoned about but were never written into the artifact.
This doesn't change the probe's verdict (sober still held every curb; the missing flags were minor
compositional choices, not brand risk), but it's a concrete instance of why the artifact must be
checked, not the agent's word — consistent with `verification=enforcement`
(`procedural-debt-and-method` memory).

## What this proves, and what it doesn't

**Proves:** the inference-ramp framing (§9) is workable end-to-end on a real, data-heavy, cardinal-
constrained screen — isolated generation didn't collapse the bands together, cardinal curbs held
with zero drift, foundational curbs moved in the predicted direction, and the whole run used
existing (named, not yet built) machinery successfully on the first try.

**Doesn't prove (per `_LIVE-STATE.md`'s own audit-deferred caveat):** this is one screen, one
spread, self-graded by structural grep rather than the full divergence-probe tooling (novelty
scoring, threshold calibration) or a rendered visual check. §9/§9a's "proven" status stays
**deferred** until more spreads land and Dave has eyeballed the actual HTML. This session moves it
from "no worked spread exists" to "one worked spread exists, results promising" — not further.

## Entry points

`_TEST-BRIEF-v2-sme-payments.md` (contract, reconciled to §9 this session) ·
`_FIXED-FLEX-CHARTER.md` §9/§9a (the machinery this exercises) · `_LIVE-STATE.md` (OPEN item this
closes/updates) · `sober.html` / `balanced.html` / `expressive.html` (the artifacts — open these
directly, don't just read this probe).
