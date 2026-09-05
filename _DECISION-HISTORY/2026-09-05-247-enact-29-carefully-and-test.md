# #247 — enact 29, carefully, and test: a plan before an edit, one wave landed, five rulings in Dave's words, and a blind judge who says nothing leads

```
provenance: 247 · 2026-09-05
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-05 … #247`. Ledger: `knowledge/_rulings.json`
§ `s247-D1` … `s247-D5` (inscribed by the conductor, read back at the wrap). Banner: `GOOD-MORNING.md` § ★ LATEST #247.
Reports: `notes/_subreports/2026-09-05-247-W1-D-density-edit.md` · `notes/_subreports/2026-09-05-247-W1-R-rerun.md` ·
`notes/_subreports/2026-09-05-247-wrap.md`. Briefs: `notes/_briefs/2026-09-05-247-W1-density-brief.md` ·
`notes/_briefs/2026-09-05-247-delegated-wrap-brief.md`. Review surfaces: `reviews/DP-TEST-PLAN-2026-09-05-v1.html` ·
`reviews/W1-DENSITY-2026-09-05-v1.html`. Score sheet: `notes/_dp-scores/w1.json`. Both-way: each of those files names this
dossier's session.*

This is the WHY and the HOW. The WHAT — figures, paths, the declared skips with their sizes — is in the ⏱ delta and the
`#### 2026-09-05 #247` stratum; nothing here is a second home for a number.

## 1. Why the session opened with "do we need both?" and did not start editing

#246 closed with Dave's *"lets do it and verify the results"* and a chain whose top carry read "enact DP-01…18, then re-run
the prompt". The obvious first move was the enact wave. Dave's first line was instead a question — *"do we need both?"* —
about whether the principles page and the enactment were two things or one. The conductor surfaced the principles page
again rather than answering from memory, because the page held 29 principles and the carry said eighteen, and the gap
between the two was itself a carried ruling-shaped question. Answering "do we need both" from the chain would have
answered it from a stale count.

## 2. Why 29 and not eighteen, and why "carefully" became a method

Put the eighteen-or-29 question plainly, Dave answered it plainly — *"okay lets do 29, carefully, and test"* — and then
went past the question: *"it would be cool if you could create a testing schedule, maybe a set of briefs or simple prompts
that we could use to experiment with, or if you have any other ideas."* That is `s247-D1`, and it did two things at once.
It struck the eighteen-vs-29 carry (29), and it turned "carefully" into a method rather than an adverb: one principle
group per wave, the frozen control re-run after each, the result scored, then the next group. The #246 finding was that
four dashboards from two models came out as the template's specimen; if all 29 principles were enacted in one pass and the
re-run moved, nothing would say which principle moved it. The schedule exists so that every wave has one variable.

## 3. Why the plan was a page and not a list

The test plan (`reviews/DP-TEST-PLAN-2026-09-05-v1.html`) is a review page because Dave reads review pages and rules on
them; a list in chat evaporates with the chat. It carries the W0…W8 schedule (W0 the #246 baseline, DONE; W1 density; W2
bento rhythm; W3 reveal; W4/W5 waiting on the principles page's Q8–Q13 / Q14–Q15; W6 the DP-17 three-way test that
`s246-D7` ruled; W7 a regression over all 29; W8 Dave's own cold VS Code run), the P0 frozen control and P1–P8 probe
prompts, three score instruments, and a conflict ledger — because Dave's stated wariness at #246 was *"possible conflicts
and complexity"*, and a ledger is the only way a conflict between two principles becomes a row instead of an opinion. It
also carries four ruling-shaped questions of its own (wave order · re-run cadence · a blind judge every wave · out-of-group
fixes). He answered none of them; he said *"go w1"*, and W1 ran on the plan's defaults. The four are carried, not assumed.

## 4. Why W1 was one edit, and why the edit was the template's lead group

Density (DP-06 07 08 09) went first because it is the cheapest wave with the largest visible effect and the one `s246-D5`
had already half-ruled (KPI row default, 2×2 removed). The single edit — GROUP 1 of `Template-dashboard-bento.reference.html`,
four `data-c="3"` tiles becoming six compact `data-c="1"` tiles — was chosen because the #246 finding located every
dashboard's shape in that one file: change the specimen and both models' output should follow. Six rather than four
because six divides every band (6/3+3/2+2+2/1 — square by construction, and the composition gate's C9 orphan arm agrees),
while four at `data-c="1"` orphans at the three-column band. Lane D built it, ran both validators to 0, and rendered it:
the first chart's top edge moved 675.7 → 516.5px at 1440 light. It also found that the row costs 287px at 520 (six stacked
tiles against four) — a wide-band gain and a narrow-band loss, which became `s247-D5` when Dave saw it.

## 5. Why the re-run measured the fold and richness separately, and why richness did not move

Lane R re-ran P0 on lane D's library, blind then sighted, with one instrument that it also re-ran on the #246 pages so the
comparison is the same script on both. The sighted page's first chart moved 837.8 → 678.6px — identical to the snippet's
−159.2, which is the evidence the edit passed through the composition intact. Six tiles and the whole chart canvas sit
above a 900px fold where the baseline had four and a cut canvas. Richness read 2/2/0/2 → 2/2/0/2, unchanged, and that is
correct rather than disappointing: instrument A scores the component SET, and density re-packs the set without adding to
it. That is the fact behind the review page's Q1 ("did W1 move?") and behind `s247-D2` — Dave: *"Okay W1 arm be is
better"* — which rules that the fold is the finding and leaves the instrument's fold row for W2+ unruled.

## 6. Why the blind arm regressed, and why it stays

The blind page came out at 2719px with the wall collapsed to one column and richness 1/1/0/2 — worse than baseline. The
cause was not the edit: the blind splice carried `Tabs.reference.html`'s demo width (L80) and panel cap (L120), and the
#246 blind builder had happened to write a `.tpl-tabs .tabs{width:100%}` harness line that this one did not. One harness
line outweighed the whole W1 edit on the blind arm. Dave's reaction — *"its just my gut reaction, we need this test, it's
just me expressing my frustration, the lack of vision is proving to be a rather big issue"* — was named at the time as
not a ruling, and it is recorded as evidence under the parts-with-addresses carry, because it is the sightless-consumer
problem seen from the result side. The blind arm stays in every wave: it is the demo condition, and the regression is the
kind of fact the plan exists to surface. Whether the two Tabs lines go under a DEMO CHROME marker is lane R's RSQ 4 and
Dave's.

## 7. Why the judge was blind, and why "nothing leads" matters more than the pick

Lane J was given `x.png` and `y.png` under a randomised key it was not told (seed 84664, flip=False; the key written by
lane R before J ran) and asked which reads denser above the fold and what it would change first on each. It picked W1
unprompted. Its first change for W1 was the finding of the day: *"the six tiles are uniformly weighted so nothing leads;
promote Group liquidity (larger number, wider tile)."* That is DP-07 and DP-14 (a lead, a rhythm) pushing against DP-06
(density in one row) — the first conflict-ledger entry that is a real conflict and not a hypothetical, and it arrived from
a reader who did not know which page was which. It is W2's opening fact, and it is why the next title is "one tile leads".

## 8. Why the status tiles became a ruling about flexibility rather than an option

Two of the six tiles (Awaiting approval · Undrawn facilities) carry a count or a status where the others carry a signed
delta against a period; they meet DP-08 by slot and not by content, and they break `kpi-tile.meta.json`'s own antiPattern
(a KPI tile with no series is a Stat card). Both lanes raised it as an a/b/c. Dave did not pick: *"This is an interesting
question and its where we might have to have some flexibility. Should there even be here? … if they are the only statuses
displays they shouldn't be hidden in the other cards."* `s247-D3` records exactly that — the tiles are not to be hidden in
the row; they get their own surface or a status bar at the top; the design is a carry. Ruling the option for him would
have been the #246 D7 mistake in a new place. Beside it, `s247-D4` (*"row for sure"*) confirmed and sharpened `s246-D5`:
the row is the shape, six is better in this instance, the count stays flexible.

## 9. Why a patch lane ran, and what class of defect it found

Lane R shipped the review page without rendering it. The patch lane found the grid's columns collapsing and a padding
shorthand wrong, fixed both, re-captured the three pages full-height with a 900px fold line drawn on (1157 · 2719 · 1316),
embedded them, and gave the RSQ list per-question reveal accordions — DP-04/05 applied to our own review surface. The
class is the one the memory hook names: no gate parses the artefact. Nothing in the review-page path renders what it
ships, so a lane can hand over a page it never saw. Whether a render-proof line joins every review-page brief is
ruling-shaped and carried; the 1 MB page is a fact of the data URIs and the #238 asset-size policy is still open.

## 10. Why the recall probe is reported twice

The probe was planted at the opener (n=4). The quiz missed K6 and scored 3/3 on the facts it had seen — because the plant
read-back was piped through `tail -8` and K6 never reached the window that was later quizzed on it. The brief's
instruction, followed here, is to report it as a measurement artefact AND as the miss it is: the record says 3/4, and the
plant rule (`--plant --session N` at the opener, never through `tail`/`head`) has now been violated by truncation a second
time. The rule stands; whether the tool should refuse a piped read-back is not built and is carried.

## 11. What the lanes cost, and why the wrap was delegated

Four subs, all Fable: D 109,328 · R 265,442 · J 45,183 · patch 60,440 = 480,393 quota, never window fill. The conductor's
fill at the brief cut was 180,791 real, past the 150,929 advisory; this seat read his transcript at 186,787 real over 83
turns. The wrap was delegated whole for that reason, and the five rulings were inscribed by the conductor before the cut
so that this seat would only read them back.

## 12. Resolved, and still open

**Resolved today:** eighteen vs 29 (29, `s247-D1`) · the schedule exists · W1 landed and moved the fold (`s247-D2`) · the
headline shape is a row (`s247-D4`) · a grid at 520 is acceptable (`s247-D5`) · the status tiles are not to be hidden in the
row (`s247-D3`, as flexibility).

**Still open, his:** the status surface design · the plan's four RSQs · a fold row in instrument A · the Tabs demo width
under DEMO CHROME · the two stale "only 6 and 3" comments · Q8–Q16 (W4/W5 wait on them) · the DP-17 test as W6 · every #246
carry at its age (the template chart whole, glue vs partial, splice vs link, mono for the SH, parts-with-addresses, the
cold test, [18], the radius build, the 4px audit). **Next:** W2 — bento rhythm, one tile leads.
