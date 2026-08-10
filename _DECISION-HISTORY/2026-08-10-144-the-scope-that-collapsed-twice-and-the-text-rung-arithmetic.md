# #144 — the rag a11y lane: a scope that collapsed twice, and the arithmetic that says why coloured text needs its own rung

provenance: 144 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA (#144) · `GOOD-MORNING.md` ★ LATEST (#144).
Ledger: `knowledge/_rulings.json` § `s144-D1`. Verbatim record: `reviews/PLUSMINUS-TUNER-2026-08-10-s144-v2.html`
(Dave's export) and `reviews/RAG-TEXT-RUNG-2026-08-10-s144-v1.html` (the scoping controller).
Both-way links per `_DECISION-HISTORY/README.md`.*

---

## Why this session existed

#143 closed with a family-level a11y fail: all four rag glyph rungs (`rag.success-glyph`,
`rag.error-glyph`, `rag.warning-glyph`, `rag.information-glyph`) fail AA on white, and a second,
smaller gap — the C4 bind address named a family (`rag.success`), not a specific rung. #144 was
conductor + 3 Sonnet subs, Dave live, and opened to fix that: residual ① of #143, the rag a11y lane.

The session's real shape turned out to be about scope, not colour maths.

## The scope collapsed twice, on Dave's own words

The opening brief carried the #143 finding at full width: four rag hues, all failing, a rung to
mint, an amber problem that looked like the hardest of the four because amber's ruled fill only
just clears white in the first place.

Dave narrowed it once, ruling out anything that isn't literally rendered as coloured text on the
page. Then he narrowed it again, verbatim: *"we don't need to worry about info or warning text,
they are not used and the only coloured text is for plus and minus, red and green. these are the
only coloured text we use."* Two colours, one shape (a signed numeral), out of an opening brief
that read as four colours and an open rung question. The amber problem — the one that had looked
structurally hardest, because its fill sits closest to the AA boundary — evaporated entirely,
because amber text does not exist anywhere in the product.

Asked why text needs its own treatment at all when the fills (`s122-D2`) are mode-invariant and
untouched, Dave gave the rationale, verbatim, typos included: *"statuses are fine they have labels
and the roundels carry a glyph that create teh meaning tah background doesnt matter."* The
distinction is R-D6 restated in a new shape: a status fill carries its meaning through a label and
a roundel glyph, so the fill's own contrast is a salience lever, not a legibility requirement — it
can afford to be one hex on both `.light` and `.dark`. A plus/minus numeral has no label and no
glyph riding alongside it; the sign character IS the meaning, and colour is doing salience work on
top of that, but the numeral's own pixels are body text and WCAG 1.4.3 applies to them directly.
That is the entire reason a text value must clear 4.5:1 where a fill, cased differently, need not.

## Why a separate rung, and not an edit to the fills: the arithmetic is closed

Before any tuning, the session worked out whether a single hex could serve as both the fill (used
as tint/background, mode-invariant) and the text value (used as body-text foreground, contrast-
sensitive) — i.e. whether `s122-D2` could simply be reused. It cannot, and the reason is
arithmetic, not taste: a value used as text on white needs relative luminance L ≤ 0.1833; the same
value used as text on the dark ink `#1A1A1A` needs L ≥ 0.2215. Those two constraints don't
overlap — the window is empty. No single hex can be both AA-legible on white and AA-legible on
`#1A1A1A`. That is *why* the coloured-text rung has to be a second, per-mode pair of values rather
than a shared constant with the fills, and it is why dark needed no new work at all: the existing
`s122-D2` fills already clear AA as text on `#1A1A1A` (error 5.55, success 8.77) — only the light
leg required tuning.

## Building the tuner, and catching an instrument lying by omission

`PLUSMINUS-TUNER` v1 let Dave move saturation and brightness in HSB space with the hue locked to
the `s122-D2` fill hues (red 7.0588°, green 142.9412°). It worked, but green-light's own export
carried `gamutClipped: true` — and nothing in the tool, or in the session, chased what that boolean
actually meant. It meant the per-channel RGB clamp that keeps an out-of-gamut colour on-screen had
silently rotated the hue **+6.84°** (142.94° → 149.78°) while reporting only a flag, not a
consequence. Hue lock was the entire premise of the exercise — a tool that reports "clipped: true"
and lets the hue move anyway is lying by omission about the one thing it was built to hold fixed.

v2 fixed it properly: instead of clamping each RGB channel independently (which is what rotates
the hue), it clamps chroma at the gamut boundary *along the locked hue*, driven at 2.6× the gamut
ceiling to prove the clamp actually holds under pressure. Result: **+0.087°** of drift, three orders
of magnitude tighter, declared in the export rather than silently absorbed.

## The second instrument finding: hue can be locked in one space, not both

Fixing the HSB-side drift surfaced a second, more interesting fact. Once `#137F3C` (the tuned
green-light value) is converted to OKLCH and its hue measured there, it sits at 150.06° — a
**−4.53°** drift from the locked 154.5908°, even though the *same* value measures only **−0.16°**
of drift in HSB, the space the tool actually drives. v2's drift alarm keys to the driving model
(HSB), so it read green throughout — correctly, by its own contract, but silently with respect to
OKLCH.

This is not a bug in v2. It is a property of HSB: the space is not perceptually uniform, so moving
saturation and brightness at fixed HSB hue does not hold OKLCH hue fixed, and vice versa. Hue can
be locked in one colour space or the other — never both simultaneously, for any tool built on
either model. Put to Dave as a declared property rather than a defect, he accepted the tuned value
as it stood.

## Dave ruled, and the ruling is a straight readback

Off v2's own export (`drivingModelAtExport: hsb`, `selectedGroundRoleId: 'selected'`), Dave set
four values: minus/red light `#DA1A00` (4.503 on `#F1F1F1`), minus/red dark `#F6604C` (4.763 on
`#272727`, unchanged from the fill), plus/green light `#137F3C` (4.503), plus/green dark `#66CC8D`
(7.531, unchanged from the fill). The ground set for the AA obligation deliberately excludes the
two rag tints — `s134-D4` already rules that a rag-tinted ground gets the `#1A1A1A` glyph ink
treatment, not a coloured rung, so testing the coloured text against its own family's tint would be
testing a combination the pattern never produces. Against every other ground (pure, zebra, hover,
selected, both themes), all four values clear 4.5:1. Recorded as `s144-D1`, textual insertion, 103
priors asserted parse-equal before and after.

## Two side-findings, both corrections rather than new work

**#143's wrap asserted a false absence.** It claimed the rag family "resolves only to
`-background`/`-glyph` rungs — there is no bare `rag.success`." That's false against the artefact:
all four bare roles exist in `semantic-colour.json` and resolve via `$alias` straight to their
`-glyph` rung. Nobody had actually grepped for the bare key before writing the negative — the
[[unmatched-grep-is-not-an-absence]] class, recurring in a new shape. Half of #143's residual ①
dissolves on this correction alone: the rung was never structurally missing, only unspecified for
a use-case (a numeral) that sits outside `s134-D4`'s tint+ink pattern.

**The conductor briefed an estimate as if it were a measurement.** The build sub's brief carried
the locked hues as 7.3°/145.3°; re-deriving them from the actual `s122-D2` hex values gives
7.0588°/142.9412°. The build sub re-derived on its own initiative, caught the mismatch, and locked
the tuner to its own measurement rather than the briefed number. The sub behaved exactly as it
should; the finding is that the conductor's number was wrong, not that anyone downstream trusted it
uncritically.

## What's still open

The ruling is RULED, not ENACTED — nothing has been written into `semantic-colour.json`. Three
things carry to #145, all Dave's: the rung's own NAME (`rag.<hue>-text` vs `-ink`, with precedent —
`rag.text.on-information` was minted at `s131-D1` as a severity-specific ink slot); whether a dark
"selected row" semantic token should exist at all (`#272727` was used as a labelled approximation,
unclaimed by any token); and an unverified check — `#1A1A1A` ink measures 1.62/2.03 against the
dark rag tints, which looks alarming until you remember `s134-D4` puts the ink rule on the pastel
*shape*, not the tint, so this may be measuring a combination the pattern never actually produces.
Flagged as unverified rather than treated as a finding.

## Gauge and process

Boot 54,872 real, inside the measured band. Four instrumental check-ins ran inside the lane
(71,785 → 99,004 → 107,379 → 118,056); one call — a full `rag` key dump out of
`semantic-colour.json` printed whole to stdout rather than looked up narrowly — cost roughly 27K on
its own, the single largest avoidable spend of the session. Quota was asked for three times and
never answered, so every routing decision rested on #143's day-old panel reading. The read-chain
contract held (`_CHAIN.md` only, ninth session running) after #143 broke it. ENOSPC sat at n=10;
`PYTHONPATH=/var/tmp/py-s142` gave a working gauge with zero install for the second session
running, which means the runbook correction is now proven twice and still not written into the
runbooks themselves. Lane ② (the colour-spine DTCG migration) did not open this session — a
declared, FILL-bound call the conductor made and told Dave about in advance, not a surprise
discovered at the wrap.
