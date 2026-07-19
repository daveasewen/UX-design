# 2026-07-19 — The money atom, digital-black as the new #000, and the grey ramp ruled onto semantics

*Narrative dossier (capture-ritual step 1b — the why + how). Terse records: `_LIVE-STATE.md`
(state) · `_proforma/_RAG-DECISIONS.md` R-D16 (rulings) · `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1`
(the surfaced greys). Both-way link: those hold the WHAT; this holds the WHY. Session opened on "read good
morning" as a components-expansion worker; Dave promoted it to conductor mid-session.*

## Why this session existed
The itinerary's P1 foundations were still unbuilt. Dave: "pad out Apollo's components." Reconciling the stale
07-14 itinerary against the tranches showed most P1 "gaps" had quietly been built in T1–T8; the genuinely
missing atoms were few. Picked the **money-format primitive** first, on the ATOMISE rule — it is the true atom
that Account-card, Table cells, transaction rows and KPI tiles all compose on, and its absence was already
flagged as the account-card `$balance-type-finding`.

## The money atom — how the shape settled
Built `Amount-display` to the full canon bar (snippet + meta + review + gates). Three findings drove the shape:
- **copy-025** (surfaced by CONSULT) — currency symbol/code precedes the amount with NO space, or it can wrap
  to a different line. Baked in.
- **Tabular figures are the whole point** — money columns must align. The specimen proves the CONDITION (a
  right-aligned column), not just the element.
- **The ramp had no home for the display size.** I first called 32px "off-ramp" and flagged a phantom "30px"
  from the account-card finding. Dave: "check the font ramp, there's no 30px" — and pointed at the runbook
  index. The ramp is 12/14/16/20/32/40/52; `apply_type_snap` maps 30→32. So 32 was always the rung; the
  finding's "30" was loose. Promoted a figure composite at 32 (`.t-cm-figure-4`, tabular) via the T-D14
  add-a-rung procedure, then — on Dave's "parked jobs" nod — added `.t-cm-figure-5/6` (16/14) so money renders
  as true numeric figures at every size, not borrowed label/caption styles.
- **Colour deferred.** I over-built a directional gain/loss variant; Dave: "forget about colour for now, it's
  being dealt with elsewhere." Stripped it — the atom is monochrome money-format only.

## "Digital black is the new #000" — the ruling that became a library sweep
I left the atom's dark ground pure `#000` and noted the new digital-black rule only covers the reverse-text
halation case. Dave corrected the scope in two messages: "use this #1A1A1A" → "digital black is the new 000."
That is a GENERAL replacement, not conditional. The blast radius was real: **all 38 components** declared a
pure-`#000` dark ground. So the change was a library-wide sweep — `background/default` dark → `#1A1A1A`, and
every component's `--page` (plus five other ground vars: menu/header/nav surfaces, table cell, tooltip) → 
`#1A1A1A`, while **shadows and overlays stay pure `#000`** (they carry no reverse text, so no halation). This
expands the original `neutral-blacks.proposals.json` framing, which had scoped `#1A1A1A` as a *conditional*
substitute. Committed by the conductor, pushed by Dave.

## text/default is a COLOUR, not a type spec — the axis confusion
Dave asked "what is text/default" expecting the 4px-snapped, leading-trimmed ramp. It is a **colour** token
(`#333`/`#FFF`). The type ramp he meant is the separate `.t-cm-*` composite system. Once separated, I bound
all three amount sizes to the figure composites (no raw font on the atom) — the type retrofit done right for
one atom.

## The grey ramp meets the greys — R-D16
The conductor strand (same day) had built the Apollo Mono neutral ramp `color/mono/1–15` (a dual-end curve).
Dave: "there are new colours for Apollo Mono… playback what you find." The useful realisation: components bind
*semantic* grey roles, so they inherit the ramp centrally — nothing to hardcode. I surfaced all 79 semantic
greys against the ramp as a review sheet (grey-tint check: surface with numbers, never auto-swap). **CONSULT
earned its keep**: it flagged `col25-011` ("typography = white or Grey-8 only"), so text ink was already
governed and not a free nearest-step swap — exactly the tension worth surfacing.

Dave ruled (R-D16) on the sheet:
1. **Text ink → `mono/4 #1A1A1A`** — the "make it black" option. This **supersedes `col25-011` for Mono**;
   Grey-8 stays Legacy. (Rationale: Mono is "very mono"; the ink is the digital black, not the Legacy grey.)
2. **Drop the secondary text grey** — Mono carries no second text grey; muted/caption hierarchy is weight +
   size, not colour. (This is the strong "very mono" stance; it makes muted text full-ink — a visible change.)
3. `#767676` (Grey-6) → `mono/8 #808080`; tinted `#D7D8D6` → `mono/12 #E1E1E1` (it was non-neutral, a faint
   green cast); mechanical nearest-step maps approved.

Ruled, **not yet enacted** — enactment is a mechanical token + 38-declaration sync + regen + gate, deferred to
a fresh Sonnet pass rather than run at the tail of a long Opus context.

## The STAND-002 catch (the gate doing its job)
Running the build during the capture ritual went red: **STAND-002** — the prior from-scratch GOOD-MORNING
rewrite had dropped the "other standing documents" reachability list, orphaning five standing docs
(`_DS-IMPROVEMENTS`, `_ICON-GAPS`, `_DATAVIZ-DECISIONS`, `_PROFORMA-RULES`, `_TYPE-DECISIONS`). This is the
exact failure mode the gate was built for, and it had been **committed + pushed red**. Restored the list in
§A. Lesson reinforced: a rewrite of the spine file is the moment the reachability gate matters most.

## Resolved vs open
- **Resolved:** Amount-display built + gated; figure-4/5/6 rungs; digital-black library sweep (committed);
  R-D16 grey rulings recorded; STAND-002 restored (build green).
- **Open:** enact R-D16 (Sonnet); then the next P1 atom, OTP/PIN. The `col25-011` Mono-override annotation is
  owed. The `_make_review` co-location trap (snippet review copies land in the gated `snippets/` dir) is a
  logged tooling fix.
