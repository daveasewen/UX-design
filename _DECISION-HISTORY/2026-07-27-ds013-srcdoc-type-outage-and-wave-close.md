---
provenance: 2026-07-27 (date from `date`)
status: observed
session: "legend wave CLOSED (combo + line) + ds-013 — srcdoc killed type.css in all 49 showroom panes"
model: Opus 5 solo self-conducting, effort MAX
commit: ba336dc
gauge: RED ~80% at authoring
---

# ds-013 + the legend wave close — 2026-07-27

## 1 · The session started with a bug report, not a lane

Dave, cold, choosing the session shape:

> *"1. but I also have an issue with the labeling on the donut and bars, they are all to big apart
> from the reset button, we had an independent scale for labels that seems to have been lost, can
> you fix and diagnose please"*

Two things are worth noticing about that sentence before the diagnosis. First, **it was right** —
there *is* an independent scale for labels (the DV-D08 chart text ladder, `.t-cm-chart-label` =
12px/500) and it *had* been lost. Second, **the exception carried the diagnosis**: "all too big
apart from the reset button" is not a vague complaint, it is a discriminating observation. Reset is
the one legend control whose snippet CSS hard-codes `font-size:12px`. Any explanation had to make
Reset the exception, which ruled out "the legend CSS is wrong" and pointed at the composite layer.

## 2 · The cause was three tiers below the charts

`gen_showroom.py` embeds each reference snippet **verbatim** and hands it to the pane iframe via
**`srcdoc`**. A srcdoc document has no URL of its own; per spec it inherits the base URL of the
**parent** document — `showroom/<Component>.html`. So the snippet's own

```html
<link rel="stylesheet" href="../canon/type.css">
```

which is correct from `knowledge/snippets/`, re-resolved against `showroom/` to `<repo>/canon/type.css`
— **a path that does not exist**. type.css 404'd in **all 49 panes that link it**, and every
`.t-cm-*` composite *and* every selector-list binding inside it was inert.

Measured in the licensed HSBC cut, computed styles, both panes of `showroom/Chart-donut.html` and
`Chart-bar.html`:

| element | before | after | canon |
|---|---|---|---|
| `.dv-leg-item` (label) | 16px / 400 | **12px / 500** | 12/500 |
| `.dv-key` (letter key) | 16px / 400 | **12px / 700** | 12/700 |
| `.dv-leg-reset` | 12px / 400 | **12px / 500** | 12/500 |
| `.t-cm-chart-label` rule | NOT FOUND | **12px / 500** | — |
| `type.css` cssRules | absent | **57** | — |

**A 404 stylesheet throws nothing.** There is no console error a person reads, no failing gate, no
red build. It presents as "the type looks a bit off" — which is exactly why it survived long enough
for Dave to be the one who found it.

## 3 · Old outage, new symptom — observed, not inferred

The tempting story is "lane ① broke it". It did not, and the distinction was cheap to settle:
render the **pre-migration** snippet (`git show 7401daf~1`) under the same unreachable-type.css
condition. Result: `.dv-legbtn` = **13.333px / 400** — the `<button>` UA default.

So the outage is old. What DV-D11 changed is that `.dv-leg-item{font:inherit}` swapped the button's
13.33px UA default for the **inherited 16px** body size, and the key lost its 700 weight. A 2.7px
regression on top of a silent library-wide one — enough to cross Dave's threshold. Both facts are
true and the record needs both, because "the migration broke it" would have sent the next session
looking in the wrong file.

## 4 · Fix, and why it is a gate

`rebase_payload_urls()` re-points each payload's relative URLs so they resolve from `showroom/`. The
half that matters is the second half: **a rebased URL whose target does not exist fails the build.**
The condition is gated, not the instance — `feedback-gate-dont-patch`.

Two things are pinned in the selftest because they are the traps:

- **Bite 2 — do NOT "simplify" this to an injected `<base href>`.** A `<base>` element also re-bases
  **fragment-only** URLs, which would break every inline icon-sprite reference (`<use href="#ic-*">`)
  in the library. That trade — a type outage for an icon outage — is the kind of fix that looks
  cleaner in the diff and is worse in the browser.
- **Bite 4 — the function is deliberately NOT idempotent.** Feeding it an already-rebased payload
  fails loud rather than walking the path up another level silently.

**The selftest earned its keep immediately: it caught a real defect in my own fix** — `?query` and
`#fragment` suffixes were being dropped by the rebase — before that shipped. A gate written in the
same hour as the fix is still worth writing.

## 5 · Lanes ② and ③ — two calls the divvy did not name

The handoff warned that each member needs a survey rather than a mechanical port. Both members
proved it.

**Combo keeps a shape modifier; bar dropped its.** These look contradictory and are the same rule.
The swatch shape earns its place when it *mirrors a real mark distinction*: combo has two mark types
on one plot (bar rects + a line with circular nodes), so shape is a genuine non-colour channel. Bar's
marks are all rects, so its `.sw-circle/.sw-square/.sw-diamond` were decoration. Chart-line, whose
markers genuinely are circle/square/diamond, earns the full set.

**The diamond's hit target was standing on its corner.** The 44px Apollo hit area is an invisible
`::before` *child* of the swatch, so `transform:rotate(45deg)` on the diamond rotated the target with
it. Counter-rotated (`translateY(-50%) rotate(-45deg)`), and proved rather than asserted:
`document.elementFromPoint(cx-20, cy-20)` returns the swatch for all three shapes at both widths — a
point that lands inside an axis-aligned 44px box and outside a 45°-rotated one.

**DV-D10 was NOT enacted, deliberately.** The GOOD-MORNING divvy said lane ② should also build the
axis-proximate lockups. The ratified ledger is narrower and wins: DV-D10 reads *"Enactment rides the
O1 build."* O1 is its own session. Enacting the lockups here would have rebuilt the legend twice and
spent Dave's DV-D10 eye on a layout nobody asked for yet. **The divvy line was a Polaroid; the ledger
is a tattoo** — the 2026-07-22 precedent in §A is the same shape, and the ledger was right then too.

## 6 · The verify suite was lying by construction

`_verify_dv_legend_members.js` — written one session earlier, for one member — had baked in **bar's
three series** (`const [a, b, c] = L.ids`) and the **literal series name `"Current"`** in the
announcement check. On a 2-series member it crashed. Worse than crashing: on any member that happened
to name a series "Current", check 13 would have passed **without testing anything**.

Generalised to per-N invariants, with names read off the markup (`nameOf(id)`). 54 → 100 checks; bar's
54 unchanged in number, wording and meaning.

The lesson generalises past this file: **a suite that hardcodes one member's data cannot verify the
next one, and it fails in the direction that reads as green.** This is the same family as ds-013 —
silent wrongness beats loud wrongness at surviving.

## 7 · A promotion tried, measured, and reversed

The registry's own note instructed: when the last member migrates, promote `class="dv-legrow` to
dv-legend's universal contract and drop it from the four extraContracts. Done — and the build failed,
**correctly**: `Chart-sparkline` (and `Chart-scatter`) are members of the dataviz behaviour **group**
but carry no legend at all.

**The group is broader than the capability.** So the universal contract stays empty — no longer
"because the wave hasn't landed" but for a permanent, better reason. The instruction had quietly
assumed group == legend-carrying members. Both beats are inscribed in the registry description,
because the reversal is the more useful fact for whoever reads it next.

The real fix is the already-open item: a **per-member behaviour opt-in** in the registry schema —
which would also stop Chart-sparkline carrying an inert legend payload. Schema change, Dave's call.

## 8 · Numbers, stated as what they are

Page budget after the close: **28,723 B (88%)**. The prior handoff predicted ~27,768 B (85%). That
was a prediction; this is a measurement, and it is recorded as a measurement — which is precisely
what that handoff's own Correction 2 was about. Predictions labelled as measurements are the
project's most reliable way of being confidently wrong.

`dv-behaviour.js` 15,771 → 13,004 B. Build 56/56. Exemplar 27/27. Members 100/100. Migration checker
exit 0.

## 9 · What is owed

**49 showroom panes now render canon type for the first time and nobody has looked at them.** Dave
chose "lanes now, sweep after"; the lanes took the window. Registered in `_REVIEW-SIGNOFF.md` and
made the next session's §DO-FIRST.

The instruction there is deliberate: **build the sweep as a numeric assertion, not an eyeball pass.**
An eyeball pass authored at the end of a hot session is the failure mode, not the mitigation — this
session's own gauge (🔴 ~80%) is the argument.

**The standing pattern is now four deep.** ds-010, ds-012, ds-013 and this session's diamond hit-area
were all found by rendering the real artefact in the real cut, and none was reachable by any static
gate we had. ds-013 differs in the way that should sting slightly: **it was found by Dave, not by us.**
The gate it produced is the first of the four to make its class of failure build-blocking.
