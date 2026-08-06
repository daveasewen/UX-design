# #109 — The boot floor was measured, and it was wrong by 45,400 in two different ways

provenance: clever-dreamy-ritchie #109 · 2026-08-06
status: observed

## The arc

**1 · What the published number claimed to be, and what it actually was.** `knowledge/_gauge_tokens.py`
published boot as **30,499 ± 8,000** — the figure every pre-flight in this repo has priced against since
`ds-025` was opened at #37. Measured directly against `message.usage` at first turn (n=5: #103 65,023 ·
#104 64,765 · #105 67,370 · #107 65,046 · #109 64,778; err = half-range, which is itself the session-shape
variation the file's own stale warning was worried about), the real figure is **75,899 ± 1,400**. The
published number was wrong by **45,400** — 30% of the 150,929 stop line, large enough on its own to flip
a go/no-go on whether a job-plus-wrap fits inside working budget.

**2 · Two separate defects, and conflating them would have hidden the second.** (a) **STALE CONSTANT** —
`BOOT_HARNESS_EST = 20_000 ± 8_000` sat 5.6x outside its own error bar against the measured 65,400. The
file carried its own warning, unchanged since it was written: *"RE-MEASURE WHEN THE SESSION SHAPE
CHANGES — a new MCP server or plugin moves this figure."* Nobody actioned it for roughly 72 sessions —
[[instrument-without-a-consumer]], an instrument that spoke once and was never read back.
(b) **STRUCTURAL** — independent of the constant's value, `measure_boot()` computed `boot = disk +
harness`, where `harness` stood for turn ONE (the harness/system-prompt cost) and `disk` was
`_CHAIN.md`, read at turn TWO. Two different moments in the conversation, added as though they were two
halves of one thing. `_CHAIN.md` is not inside the floor — it lands on top of it, previously uncounted.
Fixing (a) alone, without noticing (b), would have produced a differently-wrong number wearing a
confident error bar — the [[premise-ages-faster-than-rule]] failure, twice in one file.

**3 · The measured floor, assembled from parts that are each independently real.**
```
first turn        65,400 ± 1,400   MEASURED, message.usage first turn, n=5
  MEMORY.md        8,470           MEASURED at #109, tokenised off the mounted auto-memory
  remainder       56,308           system prompt + tool schemas + deferred-tool list +
                                    MCP server instructions + CLAUDE.md — bounded and named,
                                    not yet split (this is what ds-025 item 1 now means)
+ _CHAIN.md       10,499           MEASURED, ADDITIVE — lands at turn 2, on top of boot
= floor           75,899           before a word of work
```
Room for job+wrap fell from 169,501 (against the wrong published floor) to 124,101 (against the
measured one) — the corrected figure the #109 job itself had to fit inside.

**4 · The enactment, and what it deliberately does not touch.** `knowledge/_gauge_tokens.py` (+35/-10,
uncommitted going into this wrap): `BOOT_HARNESS_EST`/`BOOT_HARNESS_ERR` → `BOOT_FIRSTTURN_TK = 65_400` /
`BOOT_FIRSTTURN_ERR = 1_400`; the returned dict's keys `disk`/`disk_method` → `chain`/`chain_method`,
`harness*` → `firstturn*`; the method label now states MEASURED with its sample count and coverage,
replacing "estimate — UNREACHABLE". The original ±4%-style defence — estimate it, label it, carry the
error bar, move on — was **left intact and marked**: the reasoning was sound, only the premise under it
had rotted. No budget, threshold or gate was touched — amber 160,000, working 200,000, stop 150,929 are
unchanged; this is a floor correction, not a re-dial.

**5 · The receipts, run rather than claimed.** MUTATION TEST, two-way: re-enacting the OLD constant
(20,000) reproduced the OLD published figure EXACTLY (30,499), delta 45,400 — proves the constant is
CONSUMED by `measure_boot()`, not cosmetic. `python3 knowledge/_gauge_tokens.py --selftest` → OK (5
fixtures exact; cache fidelity, content-hash keying, corrupt-file robustness, degraded-measurement
honesty, band/floor guard all bite). The #53 floor guard re-run on the corrected floor clears (75,899 <
200,000). A grep for external consumers of `BOOT_HARNESS_*` and `boot['disk']` outside
`_gauge_tokens.py` found zero — the only outside caller (`_capture_gate.py:3456`) uses the returned
failure LIST, never the dict's keys directly, so the rename does not silently break a second file.
`_checkin.py --window 200000` read FILL 98,070 real mid-session, boot 64,778 real, cache continuity 8/10,
rehearsal 0 structural fails / 16 warns.

**6 · What #105 got wrong on the way here, and why the old entry is superseded, not deleted.** #105's
gauge-log stratum derived *"harness ~55,780"* by subtracting the disk figure from the whole-boot
`message.usage` reading. That subtraction is the identical conflation named in movement 2(b) — treating
a turn-2 addition and a turn-1 measurement as separable halves of the same number — and is now
superseded by this session's structural fix. The #105 entry is not edited; it is superseded in place,
per the record-correction discipline (the wrong sentence's target — the old `boot = disk + harness`
shape — is what changed, not the sentence itself).

**7 · The false record, and its correction.** `notes/_MEMENTO-DECISIONS.md:1297`, `:1399` and (found in
the same pass, not separately flagged by the brief) `:1562` all asserted that the boot was *"NEVER
MEASURED IN 36 SESSIONS."* That was true when written (#52) and has been false since the `message.usage`
first-turn method landed — it just never got chased, because nothing re-tests a prose claim once it
stops matching its own source. Corrected at all three sites this wrap: struck through, not deleted,
with a pointer to this dossier and to `ds-025`'s re-scoped state (movement 8).

**8 · Dave's rulings, and what rolls to #110.** `#109-D1` — lane: fix the boot number first, then the
research candidates, over a full harness audit or a corpus trim. `#109-D2` — retitle #109 to this lane;
the generated title's per-theme collision sweep + `type.css:180` + `ds-032` roll to #110 as an explicit
pointer, not dropped. `#109-D3` — `ds-025` item 1 stays OPEN, RE-SCOPED: the boot TOTAL is now measured
and that half is closed; item 1 now means the DECOMPOSITION of the 56,308 remainder only (MEMORY.md's
8,470 is already split out). Dave asked to understand the re-scope before ruling it and approved the
re-scope itself — he has **not** signed off the `_gauge_tokens.py` code change line by line, so it is
recorded as ENACTED + UNRATIFIED, not as a closed loop. `#109-D4`, verbatim: *"Lets fix this properly, no
patches no sticking plasters."* That sentence governs the four-phase plan below, which is priced and
awaiting Dave's confirm to open, not yet running: **P1** split the 56,308 by tokenising what is actually
on disk (skill frontmatter at the mounted + RPM skill paths, CLAUDE.md, plugin manifests), with the
Cowork system prompt falling out as the residual by subtraction — ★ a method correction worth keeping:
the original assumption was that attribution needed one fresh throwaway session boot per config (6–8
sessions); most of the 56,308 is directly tokenisable in one pass, which collapses P1 from a project to
a morning. **P2** cut what doesn't earn its boot rent — seven MCP servers load unauthenticated (Asana,
Atlassian, Intercom, Linear, Notion, Slack, Figma) plus a second, duplicate Figma server; each drop
needs Dave's call (authorise or remove) and a re-measure after. **P3** gate it — a boot-ceiling gate that
fails loud on drift, the mechanical form of D4's "no sticking plasters." **P4** the old `_CHAIN.md`
corpus-trim option, now correctly priced at 14% of the floor rather than the main event.
