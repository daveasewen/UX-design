# #157 — the enum that landed, and the palette that was never shared

provenance: 157 · 2026-08-12
status: ruled — `knowledge/_rulings.json` § `s157-D1`, § `s157-D2`

*Session #157, Wednesday 2026-08-12. FABLE conductor + this OPUS wrap sub, Dave live, one arc that
turned into two: the enum addition the residual chain had been carrying since #143, and — because
Dave looked at the rendered result rather than the diff — a structural fall-through nobody's gate
measures. Spine entries: `GOOD-MORNING.md` ★ LATEST #157 · `_LIVE-STATE.md` ⏱ LATEST #157.
Ledger: `knowledge/_rulings.json` § `s157-D1` (117th) · § `s157-D2` (118th).*

---

## 1. The item that had been abstract for fourteen sessions became one word

The residual chain carried *"`success-ink` BINDING SITE"* from #143 onward. #156's survey made it
exact: `s155-D1` ruled a green text seat, and the only monetary component — `amount-display` — had a
`sign` enum of `["none", "negative"]`. **There was no seat to bind to.** An enum addition is a
ruling, so #156 could only name it and stop.

Dave ruled it in three words — *"go for it"* — and the enactment is `s157-D1`:
`knowledge/components/amount-display.meta.json` `sign` is now `["none", "negative", "positive"]`,
with the binds **re-keyed by REVERSAL of the #142 re-key**: `positive` → `rag.success`,
`negative` → `rag.error`, `none` left **UNBOUND**. The unbinding of `none` is a declared delta,
unvetoed, and it stays Dave's to veto later — it is written down rather than smoothed over.

**Why the reversal and not an addition:** #142's re-key had pointed the two-value enum's keys at the
shape that made sense when there was no positive. Adding a third value without reversing would have
left `negative` reading as the default case. The delta was declared before the write and the ratchet
was the check: `_validate_binds_ratchet` **PASS 33/33** — the floor cannot fall, so the write could
only be additive in effect.

`_rulings.json` took the entry by **textual splice**, priors asserted parse-equal first: the file
carries mixed `\u` escaping and a serializer round-trip is impossible
[[serializer-defaults-reformat-the-file]].

## 2. The specimen was rendered, not asserted — and the render is why the session forked

`knowledge/snippets/Amount-display.reference.html` gained a `sign=positive` section: all three sizes,
the `+` sign carried **redundantly with colour** per WCAG 1.4.1, and `--success-ink` at `#137F3C`
light / `#66CC8D` dark. Measured in-render, not derived: **5.09:1 on white**, **8.77:1 on `#1A1A1A`**,
both AA; computed inks read back as `rgb(19,127,60)` / `rgb(102,204,141)`.

The renders exist because of a piece of luck worth inscribing: **`/var/tmp` SURVIVED from prior
sessions.** #156's disk fence — ~1.7 GB of stale nobody-owned `pw-browsers-*` and `chromelibs` that
could not be deleted — was, this session, **the thing that made the render possible**: the browsers
and the `libXdamage` lib farm were already on disk, so `PLAYWRIGHT_BROWSERS_PATH` + an
`LD_LIBRARY_PATH` at `/var/tmp/chromelibs` produced a working chromium with **no download at all**.
★ The same leftovers that were a fence one session were the toolkit the next; the honest reading is
that neither state is a standing environmental fact and both must be re-measured
[[refusal-names-the-first-obstacle]] [[stale-mount-corroborates-a-stale-premise]].

Dave's verdict on the render: *"for mono it's perfect"* — **the mono seat is approved in-window.**
PNGs: `_review/s157-amount-light.png` · `_review/s157-amount-dark.png`.

## 3. Then he said the sentence that forked the session

> *"no difference between the themes, this isn't bound properly."*

He was looking at the four themes side by side and they were identical. The measured cause, first-hand:

- `gen_theme_cascade` **re-projects only the vars a theme actually overrides.**
- **No theme overrides `rag/success-ink` or `rag/error-ink`** — those rungs are mono-only by ruling
  (`s151-D1` / `s155-D1`).
- Therefore every non-mono theme **inherits the mono greens silently.** Nothing declares it, nothing
  measures it.

This is [[fall-through-class-declare-what-you-mean]] one tier up: the class was known at the *value*
level and is here at the *palette* level. ★ **No gate measures it**, which is the part that makes it
structural rather than a bug.

## 4. `s157-D2` — palette sharing becomes structural, and then was deliberately not built

Dave ruled off the full #122 RAG controller screen plus the measurement: *"okay cool do it"*. The
ruling is a **named-palette tier extending ADR-0014's neutral DNA tier** — not a parallel mechanism.

| family | legacy | mono | console | supercharge |
|---|---|---|---|---|
| RAG | own | own | ── shared ── | |
| grey ramp | own | ── shared ── | | own |

The measurement that made it a ruling rather than a tidy-up: **console and supercharge duplicate 12
of 16 rag keys hex-identically**; the 4 that differ are `-tint` keys and differ *legitimately*
(different grounds). A shared palette is therefore not a refactor of coincidence — it is the
structure the values were already in.

**And it was NOT enacted, on purpose.** The wrap opened at FILL 130,372 against the 150,929 stop
line — ~20K of room against a 42–49K wrap price. Cramming the build would have meant a wrap authored
at the wrong end of the gauge [[stop-line-repriced-93]]. The build is written down instead:
`notes/_briefs/2026-08-12-s157-palette-tier-brief.md`, and **#158 is to cite it, not restate it**.

## 5. What went wrong, recorded because it is the (n+1)th instance

`gen_showroom.py` **WROTE ON A `--help` INVOCATION.** One accidental full write of 14 pages. This is
the carried *generators-write-by-default* class, homed in `_FUTURE-STATE.md` at #153 — this is at
least its third recorded instance. The revert needed a stale `.git/index.lock` cleared first (the
delete grant), and `git checkout` was the restore path. ★ **A `--help` flag that mutates the
repository is not a usability wart; it is a generator with no dry-run and no argument parse before
its side effects**, and the class will keep producing instances until a gate refuses the write
[[gate-dont-patch]].

Twelve *other* stale showroom pages were regenerated in the same pass and **kept** — they are
generated files catching up to their sources, not this session's content.

## 6. Where it landed

- ✅ `s157-D1` **RULED + ENACTED + VERIFIED** — enum, binds reversal, ratchet 33/33, specimen
  rendered and seen, mono seat approved by Dave in-window.
- ✅ `s157-D2` **RULED, NOT ENACTED** — brief in hand, #158's top item.
- ⛔ Open, and Dave's: the `none`-unbound delta stands unvetoed; the non-mono `-ink` question is
  **not** answered by `s157-D2` (sharing a palette is not forking a value); palette **names** are his.
- ⛔ Still unmeasured by any gate: **no gate resolves meta binds against the colour spine** (#145).
  The natural home is the palette gate `s157-D2` calls for — one instrument closes both.

Gauge: boot **54,851** real (in the 54,859±1,178 band — a datapoint, never corrected into the
constant [[boot-floor-measured-109]]); opener FILL 63,517; wrap-open FILL **130,372** vs stop
**150,929**. Quota polled at the opener from Dave's panel: session **0%** · weekly **59%** ·
Fable **73%**, resets Thu 10:59PM.
