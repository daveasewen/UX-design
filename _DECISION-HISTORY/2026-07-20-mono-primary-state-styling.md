# 2026-07-20 — Mono primary-action → the state-styling architecture (a live-editor arc)

*Narrative dossier (capture-ritual step 1b): the WHY and HOW. The terse WHAT lives in
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…B-D5), `docs/decisions/ADR-0009-state-styling-architecture.md`,
and the 2026-07-20 (evening) `_LIVE-STATE.md` delta. Spine ↔ this file link both ways. Commit `b895c40`.*

## Where it started
The session opened to clear **token debt** so Dave could build more components (the Sutherland field
test — the other candidate — was parked because the Sutherland repo isn't available yet). The headline
debt was the **owed mono primary-action ruling**: every button tier resolved through the 3-tier stack
*except* the primary, whose only group was **Legacy red**. The plan was small: mint `button/primary/*`,
fix three Legacy-aliased border greys, done.

It did not stay small — and that was the value.

## Finding 1 — "no red" is a principle, not a carve-out
I framed the proposal as "red is Legacy-only." Dave corrected the *category*: **"Mono is [named]
because the UI is monochromatic; the only colour is dataviz, RAG and status."** So red isn't a
carve-out we tolerate — it's **out of bounds** for Mono, full stop. This reframing (B-D1) is why the
primary is a near-black ground that **inverts to near-white in dark**, never a hue. Small wording, big
boundary — recorded as a rule of thumb so it doesn't get re-litigated per-component.

## Finding 2 — the review sheet should be an editor, not a questionnaire
After the first static review sheet (v1), Dave: *"add a selector and any other controls so I can edit
the choices rather than us going back and forward… add this as a principle for all review."* This
promoted an existing seed (`_FUTURE-STATE`: "bake template controls into the overlay") into a **standing
principle**: every review carries a **decision control per open choice**; he edits in place and I read
the settled values off an **export block**. It's the review-sheet expression of the μX / edit-mode
concept. The rest of the session *ran on this loop* (v2→v7), which is exactly why it converged fast.
Corollary he stated: **controls are locked to the tokens and expose only what he can change** — so the
sheet went colour-only, ramp-locked, with label/icon/disabled shown *locked* (shared tokens).

## Finding 3 — hover: the mechanism flip-flop that taught the architecture
This is the crux, and it moved three times:
1. First I proposed **opacity, no colour token** (efficient, monochrome).
2. Dave: *"we don't use opacity… I just want to select a colour"* → I minted a real
   `background/hover` **colour** token.
3. Dave: *"use the opacity and store it as a token but we need the colour token too… both, operationally
   different"* → reversed again: **opacity operational, colour stored as the equivalent.**
4. Then the generalisation: *"someone might choose colour alone — part of the architecture"* and *"a mode
   that is red default, blue hover, green active."*

The flip-flop wasn't indecision — each turn exposed a requirement the previous framing dropped. The
resolution (**ADR-0009**): the **colour token is the universal substrate** (always present, per-theme
override, so a fully chromatic mode is just an override set); **opacity is an optional operational
layer**; **mechanism is a per-state SET `{colour|opacity|both}`** (Dave: *"either or both"*), colour-alone
first-class. A future **style-builder interface** configures it. Wired **non-breaking** as
`$extensions.apollo.state` (DTCG vendor extension — the stores already use `$extensions`, so no generator
risk), with an explicit migration note to a first-class number/opacity token later.

The neat sub-move (Dave's): the hover **opacity dial snaps its result to the nearest ramp step** so the
*ergonomics* are "just opacity" while the *stored artifact* is a compliant ramp colour. Operational
opacity + portable colour, from one control.

## Finding 4 — disabled: exempt is not a licence to be invisible
My first disabled fix matched the sibling buttons — and inherited their latent bug: `text/disabled`
`#E1E1E1` **equals** the `#E1E1E1` disabled ground → the label was literally invisible (1.0:1). Dave
caught it with a screenshot. His rule (B-D4): **"it doesn't have to be accessible, but invisible for
normal sighted people isn't acceptable."** Fix: mint `text/on-disabled`, a deliberate ghost. Then a
second correction — my *guard* (2:1 hard floor) blocked the *lighter* greys he wanted; he only wanted to
change the disabled **text colour**. So the guard became **informational** (Visible/Faint/Too-faint),
not a blocker — respecting that it's his exempt call. He settled on `#9D9D9D`/`#808080`.

## Where I went wrong (worth remembering)
- **Matched the sibling pattern uncritically** on disabled and imported its invisible-label bug. "Consistent
  with the other tiers" wasn't good enough when the other tiers were themselves wrong (ADR-0008: don't
  inherit a flaw to match).
- **Over-constrained a control.** The 2:1 disabled guard was me encoding my caution as a hard rule over
  Dave's exempt design call. Controls should inform on exempt dimensions, not block.
- **Read the disabled comment twice before landing it** — "still looks interactable" / "the colour of the
  disabled text" needed two passes. Reflecting the interpretation back in the reply (not just acting) is
  what caught it.

## Resolved state
Commit `b895c40`, build green 35/35. Primary ladder minted + settled; ADR-0009 accepted; two bugs fixed
(invisible disabled label, 3 Legacy border greys); live-controls principle + style-builder captured.

## Still open
- **`button/*` snippet rebind** (queue #4): until it runs, the *rendered* Mono button still shows red
  primary and hover isn't operationally opacity yet — batched across all tiers. **This is the thing to
  line up before building more components** on the primary.
- Opacity → **first-class number token** with the style-builder (currently `$extensions`).
- Other button tiers likely share the **invisible-disabled-label** defect — flagged for the batch.
- **T9 secure entry** still awaits Dave review.

*Links: `_BUTTON-DECISIONS.md` · `ADR-0009` · `_LIVE-STATE.md` (2026-07-20 evening) · memories
`state-styling-architecture`, `mono-primary-and-disabled-rules`, `feedback-live-controller` · editors
`reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v1…v7.html`.*
