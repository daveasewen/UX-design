# #110 — The boot-drift gate: built, wired, and it caught its own crash

provenance: #110 · 2026-08-06
status: observed

## The arc

**1 · What #109 handed forward, and where this session redirected.** #109 measured the boot floor at
75,899 real against a published 30,499 and left a four-phase plan (`ds-036`, Dave's "no patches no
sticking plasters"): P1 split the 56,308 unattributed first-turn remainder, P2 cut boot rent from
unauthenticated MCP servers, P3 gate the ceiling so a drift like this cannot sit unread for 72
sessions again, P4 trim `_CHAIN.md`'s 10,499. Dave's opener ruling (`#110-D1`) opened the plan and
delegated P1 to a Sonnet sub; posture (`#110-D2`) was crank, delegate hard. The lane that actually
ran was P1 then P3 — P2 was overtaken by what P1's own result implied, and P4 rolled forward
untouched.

**2 · P1's result: 15,660 of the 56,308, not the whole remainder.** A delegated Sonnet sub (158,736
of its own tokens — quota, not conductor fill) tokenised what is actually on disk: skill catalog
4,725 · deferred-tool list 4,012 · MCP server instructions 2,863 · `AGENTS.md` 2,799 (flagged
UNCONFIRMED as boot-injected, not asserted) · agent-types list 930 · plugin manifests 331. That
totals 15,660. The remaining 40,648 is a residual by subtraction — base system prompt and the full
JSON schemas of pre-loaded tools — named and bounded, not measured. `MEMORY.md` was re-measured at
8,800, up 330 on #109's 8,470. A genuine gap surfaced in the same pass: `find -iname CLAUDE.md`
returns zero hits anywhere in the mount, yet `_checkin.py:331` labels a boot slot "CLAUDE.md"
generically — `AGENTS.md` is the plausible referent but its boot-injection status is confirmed
neither way. The sub's own caveat, kept rather than smoothed over: it measured *its own* injected
surface, not the conductor's — the tool-list half corroborates from the conductor's own context,
the remainder does not and stays labelled UNVERIFIED.

**3 · The finding that changed the plan: P2's ceiling turned out to be small.** Between #109 and
#110, five MCP servers (Asana, Atlassian, Intercom, Linear, Notion) had already dropped out of the
tool surface on their own — nothing this session did caused it, it was simply observed. That put a
number on P2 for the first time: gross saving ~2,646 real already banked, roughly 530 per server.
The servers still live and nameable as candidates (Slack, a duplicate second Figma server, one
unauthenticated one) are worth an estimated ~1,500–3,000 total — 2 to 4 percent of the 75,899
floor. By Dave's own `#109-D4` standard — "fix this properly, no patches no sticking plasters" — a
cut this small, chased for its own sake, is exactly the sticking plaster the ruling was written
against. That is what redirected effort from P2 to P3 mid-session (`#110-D3`), and the redirection
is dated to this specific measurement, not a change of mind in the abstract.

**4 · What got built: a boot-ceiling gate, the mechanical form of "no sticking plasters."**
`knowledge/_capture_gate.py` gained `boot_constant_drift_check()` and its parser
`_parse_boot_samples()`, plus two new module constants, `BOOT_DRIFT_BLOCKING = True` and
`BOOT_DRIFT_WINDOW = 6`. It is wired into `wrap_checks()` immediately before `lane_routing_check`.
The check reads `_gauge_tokens.BOOT_FIRSTTURN_TK` and `_ERR`, reads the boot samples recorded in
`notes/_GAUGE-LOG.md`, takes the mean of the most recent six, and fails when that mean sits further
from the published constant than the constant's own error bar allows. It is deliberately narrow: it
reports the measurement and the drift, and it never edits the constant or widens the band itself —
re-pricing is a human act this gate can recommend but not perform.

**5 · The crash the gate itself caused, and what caught it.** The first in-situ run of the new check
did not fail cleanly — it crashed with `NameError: io`, because the module reached for `io.open()`
without importing `io`. The AST-based structural check that runs at build time had already passed
this code; a crash is not the same failure shape as a red verdict, and the earlier check was not
built to distinguish them. The only reason this was caught before it could ship silently broken was
running the gate for real — `python3 knowledge/_capture_gate.py --wrap` — rather than trusting the
static pass. Fixed by importing `open()` correctly (removing the stray `io.` prefix); no other
change was needed.

**6 · The receipts, run rather than claimed.** In situ against the live gauge log: PASS, delta −43
(published constant 65,400 ± 1,400 against a recent mean of 65,356, n=6 of 21 parsed samples).
MUTATION test against #109's own stale constant (20,000 ± 8,000, the exact value that sat 5.6x
outside its error bar for ~72 sessions): FAILS, drift +45,356 — closely reproducing #109's own
recorded 45,400 (the 44-token difference is explained by this run using a 6-sample window against
#109's 5-sample one, not a new discrepancy). REVERSE MUTATION, pinning the constant to 65,200 ±
1,400: PASSES — proof the gate is not simply always red regardless of input. REACHABILITY: the
check appears and fires inside a real, complete `--wrap` run with exit 0, not merely inside an
isolated unit test — it is wired, not just written.

**7 · What's still open, and why it reads as a live signal rather than a closed loop.** The gate
grades the published constant against *logged* history, and the current session's own boot number
only lands in `notes/_GAUGE-LOG.md` once this wrap's roll executes — so a drift is structurally
caught one session after it first appears, never the session it happens in. #110's own boot measured
62,462 real — 2,894 below the published constant and already below the ±1,400 band floor — but it
will not trip the gate at #110's own wrap, precisely because of that one-session lag; if the next
few sessions hold near 62.5K, the rolling mean will cross the bar and the gate will fire on its own,
which is the design working as intended rather than a bug. Three questions are deliberately left for
Dave rather than resolved by the agent that built the gate: whether `BOOT_DRIFT_BLOCKING = True`
should really block or only warn (an agent's provisional call, not his ruling); whether to refresh
`BOOT_FIRSTTURN_TK` given the 62,462 reading; and whether the 40,648 residual is worth continuing to
chase at all, given it looks harness-owned and possibly uncuttable. All three are homed as DO-FIRST
item 26 (lettered a/b/c) in `GOOD-MORNING.md`, each with a close condition of "Dave rules it."

**8 · Dave's rulings, and what rolls to #111.** `#110-D1` — open the four-phase plan, P1 delegated
to a Sonnet sub, chosen over P2-first, over cranking the design queue, and over research candidates
1+2. `#110-D2` — posture: crank, delegate hard. `#110-D3` — P3, gate the floor, chosen over banking
P2's small win and over closing the boot lane outright, taken after the P2-ceiling finding above.
Rolling forward, unstarted or unfinished: P2 itself (now correctly priced small rather than
abandoned) and P4's `_CHAIN.md` trim; the per-theme collision sweep (35 names, DO-FIRST item 21);
`type.css:180`'s enactment (ruled #108, not yet made, item 19); `ds-032`'s enactment (item 25,
newly homed this session after living on rolling banners since #106 with no standing place); ds-029's
first-idiom flag (item 20); the `_state.json`-vs-open-rulings gap (item 22); and research candidates
1+2, not yet started. Stop line held throughout (check-ins 61,065 → 90,240 → 105,029 → 129,768
against a 150,929 line, 21,161 runway at wrap-open) and the wrap itself was delegated off-window,
the #107 mechanism, so its own drafting cost sub quota rather than conductor fill.
