# #111 — The boot-drift gate gets a legal discharge, and #110's residual premise is ruled unsafe

provenance: #111 · 2026-08-06
status: observed

## The arc

**1 · What #110 handed forward, and the two things #111 was asked to settle.** #110 built and wired
`boot_constant_drift_check()` — a gate that fails when the boot-token constant drifts outside its own
error bar against the logged history — but shipped it BLOCKING with no way to pass except fixing the
drift or editing the constant, neither of which is always available or always correct. #110 also left
DO-FIRST item 26's three questions open: warn-vs-block on the new gate, whether to refresh
`BOOT_FIRSTTURN_TK` given a falling boot figure, and whether the 40,648 residual was worth continuing
to chase. #111's opener put all three to Dave, plus a fourth live problem the DO-FIRST index-shave
work had produced: #110's wrap sub had raised `DOFIRST_INDEX_TK_MAX` 700→800 to clear its own gate.

**2 · #111-D1: the tier was right, the gate was missing its escape hatch.** Dave kept
`BOOT_DRIFT_BLOCKING = True` — the drift should still block a silent wrap — but named the actual
defect precisely: *"the gate as built has no legal discharge — that's the defect, not the tier … the
gate bites SILENCE, not reality … No session should ever be blocked with no honest way forward."* The
fix is `BOOT_DRIFT_DECL_RE` (a regex matching a specific declared-drift line shape in
`notes/_GAUGE-LOG.md`), `BOOT_DRIFT_LEGAL_FORM` (the exact wording a session must write), and
`_parse_boot_drift_declarations()`, wired into `boot_constant_drift_check()` as a 3-way branch: no
declaration and drift present ⇒ FAIL, naming the legal form; a declaration whose mean/constant/
error-bar/delta MATCH what the gate independently computes ⇒ PASS, discharged (but still logged as
unfixed); a declaration whose figures do NOT match ⇒ FAIL, louder than no declaration at all — a
session cannot write itself a pass with wrong numbers. Six scenario tests plus a mutation test
(`if matched:` → `if False:`, which fails T3 and proves the discharge clause is load-bearing) drove
this rather than merely asserting it.

**3 · #111-D4: the cap #110 raised to clear its own gate is reversed.** #110's wrap sub, faced with
the DO-FIRST presence index exceeding its 700-tape ceiling, raised `DOFIRST_INDEX_TK_MAX` to 800
rather than shortening the index. Dave's ruling was immediate and general: *"A cap raised to clear its
own gate is not a cap."* This session reversed it to 700 and shaved the index instead — 21 DO-FIRST
headings compacted, taking the index from 726 to 681 tape. The DO-NOT-RULE list for #111's own wrap
names this cap explicitly, because the same failure — raising a ceiling to clear a gate it exists to
enforce — is exactly the shape a wrap session is most tempted to repeat under time pressure.

**4 · The method lesson inside the shave: two different bounds, and they don't compose the way they
look like they do.** The first attempt at shortening the index cut 81 characters across 5 DO-FIRST
headings and the measured index went UP by 4 tape. `DOFIRST_HOOK_MAX` is a 46-character BYTE bound per
item; `DOFIRST_INDEX_TK_MAX` is a TAPE (token) bound on the whole assembled index. Inside that 46-char
window, plain ASCII is cheap and backticks/★/✅/curly-quote glyphs are expensive — so trimming
characters without changing which characters remain can make the token count worse, not better. The
fix was re-measuring what the 46-char window actually cost per glyph and rewriting the hooks toward
cheap ASCII, not merely shorter text. This cost the wrap three extra measurement round-trips before
landing on the right lever — named as the cheaper of the two mechanisms behind the stop-line overrun
below, because a single measurement up front would have collapsed it to one trip.

**5 · #111-D2: the constant stays where it is, on Dave's own diagnosis of why.** #110's boot measured
62,462 and #111's measured 55,733 — two record lows in a row, the second 6,729 below the first, against
a published constant of 65,400±1,400 built from the #103–#109 cluster (~65,300). Refreshing the
constant now would fit a line through five old samples and two new ones from what looks like a
different regime. Dave's ruling: *"Don't fit a constant across a structural break … do not borrow
precision from a configuration that no longer exists."* The refresh is deferred, not refused — it
waits on more post-change samples, and the drift stays DECLARED in `notes/_GAUGE-LOG.md` in the exact
legal form #111-D1 built, so the gate passes honestly rather than by suppression.

**6 · The conductor measured its OWN surface, and it changed the shape of #110's biggest finding.**
#110's P2 pricing (five departed MCP servers ≈ 530/server, remaining candidates ≈ 1,500–3,000) came
from a Sonnet sub measuring ITS OWN injected tool surface, not the conductor's — a caveat #110 declared
rather than hid. #111 measured the conductor's own surface inline instead of delegating: deferred-tool
list 3,709 real across 148 tools/14 servers, deferred-only servers averaging 262 real each (Figma 990 ·
Slack 721 · Gmail 598 · chrome 429 · computer-use 389 · … · cowork-onboarding 30), and MCP
instruction-block servers averaging 932 real each (computer-use 1,660 · Figma 749 · chrome 388) against
only 3 measured. The ratio between the two — 3.6× — is exactly the hypothesis Dave had floated, now
confirmed rather than assumed. It cuts both ways on the actual pricing, though: the measured deferred
mean (262) is BELOW #110's ~530/server estimate, meaning the departed-server saving may have been
OVER-priced, and the live remaining candidates (Slack + a duplicate Figma) total 836 real — lower than
#110's 1,500–3,000 band, not higher. The larger, newly-measured money is elsewhere: computer-use and
chrome each inject their guidance TWICE (a system-prompt section and a separate MCP instruction block),
measured here on one copy only and declared, not doubled by assumption; and four UUID-named servers
cost roughly 37 real per tool against ~14 for short-named ones, purely from the 36-character id
repeating in every tool name — 2,388 real for 64 tools, for zero function.

**7 · #111-D3: the number that actually needed ruling was not any of the above.** Somewhere in this
session's own arithmetic a 9,308-token drop got attributed to "the residual" without the attribution
being demonstrated — Dave caught it directly: *"The 9,308 drop has NOT been attributed to the residual.
It has been assumed to be."* This matters beyond the one figure, because #110's whole redirection from
P2 to P3 rested on the premise that the 40,648 residual is harness-owned and therefore roughly
uncuttable — and that premise was never actually measured, only assumed plausible. Dave ruled it
UNSAFE to build further conclusions on. The remedy is not a re-argument; it's a probe: measure, then
attribute, which is exactly the boot-floor lesson #109 already taught (the samples were never written
down next to the constant) recurring one layer downstream. This is rolled to #112 as the attribution
re-probe, ahead of the constant refresh it will eventually inform.

**8 · The stop line blew anyway, with three check-ins running.** 82,046 → 114,524 → 156,152 FILL
against a 150,929 stop line — blown by 5,223, declared in-chat at the reading rather than discovered at
the wrap. Unlike #108's single-late-check-in failure, three check-ins ran here; the line still blew
because of two named mechanisms: the attribution probe's own method required reproducing the injected
MCP/tool surface into files to measure it, costing roughly 32K fill that was necessary for the
measurement but not priced into the plan in advance, and the DO-FIRST index shave's four round-trips
(section 4 above) that a single upfront measurement would have collapsed into one. Quota stood at 73%
used / 27% left with 9h56m to reset; Fable's remaining 5% was held untouched, per Dave, since none of
this lane was judgment work. The attribution probe itself ran INLINE rather than delegated — costing
~32K of this session's own fill instead of a sub's quota — which is the #110 delegation finding
(quota vs fill) working as intended, and which is also what let #111 measure the CONDUCTOR's surface
directly rather than inheriting #110's sub-vs-conductor caveat.

**9 · What's still flagged, not fixed, and why leaving it alone was the correct move.** DO-FIRST items
10 and 14 carry a roll term inherited from #64 — about 44 sessions overdue — and nobody has ever ruled
on them. #110's wrap sub found them and correctly left them alone rather than silently rolling or
"fixing" an unruled item; #111 did the same, and additionally excluded both from this session's own
index-shave pass specifically so the flag itself could not be erased as a side effect of a cosmetic
edit. This is carried forward exactly as it stood, unresolved, because resolving it is not this
session's — or any agent's — call to make.

**10 · Dave's rulings, and what rolls to #112.** `#111-D1` — `BOOT_DRIFT_BLOCKING` stays BLOCKING, the
gate gets a legal discharge clause, enacted and driven this window. `#111-D2` — the boot constant is
NOT refreshed, deferred pending post-change samples, the drift stays declared. `#111-D3` — the residual
premise is UNSAFE as stated; measure, then attribute; open, rolled to #112. `#111-D4` —
`DOFIRST_INDEX_TK_MAX` reversed 800→700, enacted, index shaved to 681. `#111-D5` — `MEMORY.md`
compaction is #112's first act, not a rolled pointer, because the same warning fired twice during #110
and was ignored both times. Rolling forward: the attribution re-probe then the constant refresh, in
that order; P2 re-priced (836 real on named candidates, duplication and the UUID-prefix cost now the
larger targets); P4's `_CHAIN.md` trim (10,499); the untouched enact queue (`type.css:180`, `ds-032`,
ds-029's first idiom, the per-theme collision sweep); and the `_state.json`-vs-open-rulings gap. Stop
line blown by 5,223 despite three check-ins, mechanism named and inscribed rather than left to recur
unexplained.
