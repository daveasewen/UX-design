# Good morning, Dave ☕

*Session briefing — written end of 2026-07-02, day session ("Ingestion day — commit the
window work, then create.hsbc guidelines"). Supersedes the evening-of-01 briefing; its desk
items carried below where still open.*

## The session in one line

The evening's uncommitted work is safely in history (13 commits today), the guidance
ingestion workstream became a machine — staged site map, KG-addressable rule IDs, a
generated reconciliation register, 144 rules across 11 engine-era files — and the day's
captures resolved one standing contradiction, source-backed two house rules, and surfaced
the Univers Next and text-on-gradient questions.

## What changed

1. **Everything committed.** The whole evening session (north-star mock, GOV.UK run, G5
   advisory tier, G2 contract, proposals) + today's work. Supporting palette sits in its
   own separable commit pending your ADR-0005 ruling. NOT pushed — your call.
2. **Ingestion is now a workstream with plumbing:** `guidelines/_INGESTION-QUEUE.md`
   (3-tier site map, per-page status) · rule IDs `{#prefix-nnn}` on every tagged rule ·
   `gen_rules_index.py` gates the build (step 3/17, bite-tested, already caught one real
   defect) · `_RECONCILIATION.md` GENERATED from [REVIEW] rules so it can't drift.
3. **Ingested today:** colour standards 2026 (+brand/supporting palettes) · illustration
   standards (v2.1) · icons (legacy upgraded) + pictograms (new class, named library gap) ·
   brand motion · typography 2026 + full specification · generative-AI governance.
4. **Resolved:** col26-007 — "4.5:1 vs 3:1" is asset-class differentiation (icons 4.5 ·
   pictograms 3 · chart indicators 3), not a contradiction. #4587A7 receipted as legacy
   illustration Blue 5 (dark-token leak now source-backed). Sort code masked in Table
   (your approve), advisory signal cleared.
5. **Your context recorded** (memory + register header): the 2026 refresh is IN
   DEVELOPMENT — your approvals embed unpublished refresh knowledge; deltas ≠ defects;
   component finessing pass coming (canon possibly "too expressive").

## On your desk (fastest first)

- **Push?** 13 commits local-only; drop/keep the palette commit per ADR-0005 first.
- **All-caps ruling** — now easier: the 2026 standard bans uppercase outside acronyms
  brand-wide (dyslexia rationale, type26-019). Source favours canon-wide.
- **Univers Next for HSBC** (type26-001) — refresh renames the core typeface; token store
  says Univers. 2026 mode in the store, or documented stay-on-2025?
- **Text-on-gradient vs charter §4** (type26-015) — spec bans text over gradients; the
  expressive gradient unlock targets heroes, which carry headlines. Needs your read.
- **Icon contrast gate delta** (icon-011) — brand wants 4.5:1, gates pass 3:1. Advisory
  until you promote.
- **Motion spring tension** (mot-007) — "not playful or bouncy" vs promoted Button spring;
  connects to your "too expressive" instinct; parked for the finessing pass.
- Carried: V6 proposals · V7 series pick (deferred again) · colleague chase (calibration
  = #1 unlock) · ADR-0005 provenance ruling.

## The register

`knowledge/guidelines/_RECONCILIATION.md` — 12 open items, regenerates every build.
Reconcile when a standard settles or you rule; never hand-edit it.

## Queue next (when ingestion resumes)

Web foundations · app foundations · accessibility foundations trio (hub + neurodiversity +
communication) · typefaces + creative-headlines subpages · logos/photography/hexagons 2026 ·
tone of voice (register shaping). The gen-AI page's strategy finding (gai-008: the gates ARE
principle 3, mechanised) is queued for `digital-experience-transformation/`.

## The window (Fable metered from the 7th)

Ingestion proved cheap-operator-friendly today (capture → distill → tag → gate is
runbook-shaped). Judgment-dense remainder for the window: calibration (if materials land),
G2 compiler spec, the reconciliation rulings above.
