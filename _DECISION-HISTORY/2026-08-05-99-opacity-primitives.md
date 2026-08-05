# #99 — Opacity primitives: the ladder that got minted and the licence that shrank it

provenance: local_8794def5-f6e7-4cdf-84cf-4fe3e09846bd · 2026-08-05
status: ruled — ledger `notes/_MEMENTO-DECISIONS.md` § ★ #99 · `_rulings.json` ds-026

## The arc, and why it's worth keeping

**1 · The spread was built to answer "which numbers", and the survey reframed it.**
#96-D2 asked for a set of opacity primitives for Dave's eye; #98-D3 fixed the spacing at 4%.
The pre-build survey found the real state: NO opacity primitives existed anywhere — every
translucency in canon was a hardcoded literal or an interim dial (`--stack-fill-alpha`), and
Dave's 2026-07-18 no-text-fade ruling made text strength explicitly out of scope. So the review
doc (`reviews/OPACITY-PRIMITIVES-2026-08-05-v1.html`) was framed as four decisions — what
promotes, naming, legacy migration, consumer re-bind — with the full 4→96 ladder live over both
grounds and driven into the two waiting consumers.

**2 · Dave ruled the four, then a plain-prose question reversed one of them.**
D1 full ladder · D2 `--alpha-04…96` · D3 migrate-everything-to-nearest-step *including the
ADR-0009 hover* (ties round DOWN, his tie-break) · D4 re-bind the waiting dials. But when asked
for the two D4 numbers, he asked for plain prose — and his answer to the plain-prose version was
a different, better decision: **charts stay solid canonical palette; opacity is for state changes
only, for now; the tints are flexibility, not the default reach** (#99-D1). D4 died on the spot:
no consumer re-bind, dial retired. The lesson: a decision Dave can't answer in numbers is a
decision that wasn't his shape yet — the plain-prose re-ask didn't just clarify, it produced
the ruling the numeric question was hiding.

**3 · The enactment found its own premise was under-measured.**
Mid-migration, the corpus sweep showed the review's "five legacy values" table was measured on
canon.css samples, not the snippet corpus: **125 literal opacity declarations across 49 files**
(chart state classes `.24/.12`, harness `h2 .6` ×~40, strays `.45/.75`). The enactment stayed
scoped to the five ratified sites; the wider class was measured, registered
(`_DS-IMPROVEMENTS.md` § #99) and FORKED to Dave rather than silently widened — the
conflated-fix rule applied to scope instead of cause.

**4 · Two instrument potholes, both the document-was-right kind.**
The render probe failed 3 of 9 asserts on first run: `color-mix` serialises as `color(srgb
0.389333…)` (0–1 floats read as 0–255 → "99.3 expected, 0.39 got" — the value was EXACT), and a
mode-scoped custom prop probed on `documentElement` instead of `body`. Both fixed in the probe.
Separately, a bulk-edit regex ate two `:root` closing braces (Cards/Headers) — caught by re-grep
before any gate ran.

**5 · The stop line blew, again, by the named mechanism.**
The serial enactment loop (~30 mutating calls) carried no riding check-in; the first read after
it was FILL 201,000 vs stop 150,929. Identical to #95's class, already inscribed as blow
mechanism 2 in `stop-line-repriced-93`. Wrap opened immediately, nothing squeezed, eyeballs
rolled to #100. Not a new lesson — a repeat offence; the owed fix is behavioural (check-in every
~10 mutating calls inside an enactment loop).

## Resolved state

Minted: `knowledge/tokens/opacity.json` (24 steps, licence in `$description`). Migrated: Button
hover (68), Cards pulse (48), Headers sub (80), Modals/Drawer/Modal-lightbox bg-content (84),
Input-fields h2 (60) — all in SOURCES, manifests bound, `alpha/*` taught to the validator.
Retired: `--stack-fill-alpha`. Gates 75/0, showroom regen + 11 bites, 9 render asserts exact.

## Still open

The 125/49 corpus fork (Dave: sweep-now vs as-opened) · `--pri-hover` stored equivalents derived
at retired 0.70 (re-derivation = measurement + Dave's promotion) · Input-fields `p.note` .75 ·
eyeballs (candle hollow/filled · bullet flex-height · Confirmation Replay idiom) · #97 flag ②.
