# 2026-08-07 — #121: the ds-018 token schema ruling (A1 · B1″ · C1)

provenance: local_d6b0bd3d-7747-40da-8de7-033c6e86e758 · 2026-08-07
status: ruled — `_rulings.json` s121-D1

## Why this session existed
114 C2 failures / 87 files were the sole blocker to a fully green build (#120). Dave's framing at the opener: the token schema is built on MONO as the base of all four themes — it must be flexible, robust, standards-adherent, reliable.

## The arc — three defects wearing one number
Measurement split the 114 into: **A (104)** alpha-ramp REACHABILITY (values existed in canon since #99; standalone specimens couldn't reach them), **B (7)** `--mark` missing from the schema entirely (silent SVG-initial black), **C (3)** `--phys-size` undeclared press-physics divisors.

**The B case is the interesting arc.** First proposal: default `--mark: var(--page)` (knockout = page). Dave: no — the glyph is sometimes white ON dark surfaces. Second proposal: alias `--icon-on-inverse`. Dave again: no — *"we have ruled that the amber warning glyph should be black on amber on a white page. so the ruling must be more flexible."* The repo then produced the precedent that settles the shape: the RAG ROUNDEL POLICY (canon.css, Dave 2026-07-02) rules glyph colour PER STATUS × SURFACE driven by the ≥4.5:1 mark leg. No single alias can carry that. Hence **B1″: per-status semantic map + contextual carrier** — and Dave's closing word: *"we will mint the actual combinations soon but we need this flexibility now"* ⇒ structure ruled, values provisional.

**Dead-end worth recording:** both wrong proposals were schema-legal and standards-plausible. What killed each was a RULED INSTANCE Dave could quote. The schema question was never "what token" but "who rules the value, at what granularity" — status × theme, his.

## Findings beyond the ruling
1. **The projector carried the same defect it was meant to prevent:** `gen_snippet_tokens.py` had no `alpha/` route — manifests bound `alpha/*` at #99, the router silently fell through to semantic-colour.json. The ds-018 silent-lookup class inside the measuring instrument. Route + unitless fix; 29 UNRESOLVED → 0.
2. **Distribution, not linking:** proforma files are standalone too, so minting tokens in canon alone fixes nothing there — the generator (4th injection type) is what makes canon the single source for portable specimens.
3. **Gate-scope lesson re-confirmed:** the pro-forma no-hardcode rule flagged the injected DEFINITIONS; the exemption strips exactly the marker span and was mutation-tested from outside the span.

## Resolved state / open
C2 green 0/114, `--strict`, generator wired, 96/97 steps driven. OPEN: the combination pass (Dave: status × theme mark values + Empty-state 120 confirm) · memento-package delta-audit red (pre-existing #120; sits on #64 copies-only + open #114 pack-sync — needs Dave). Ledger: `_rulings.json` s121-D1 · spine: `_LIVE-STATE.md` ⏱ #121.
