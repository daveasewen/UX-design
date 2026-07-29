# Receipt — GOOD-MORNING.md size history: the file doubled while the anti-growth programme ran

```
provenance: local_8f342aa1-2684-42fe-a76f-c7ae95199b32 · #40 · 2026-07-29
status: observed
```

*Measured because Dave said it, unprompted: **"GM looks big again, pfff. we had it at 9k at one
point, this is a massive issue."** He was right, to the commit. This receipt is the evidence, and
it is logged in `notes/` rather than in `GOOD-MORNING.md` on his instruction — **recording the
finding in the file the finding is about would have added to the number.***

---

## §1 — THE ANSWER TO DAVE'S CLAIM: confirmed, and it was 9,274

**`00abdf3`, 2026-07-23 09:49 — `GOOD-MORNING.md` = 9,274 tape.** The working tree at the time of
writing is **18,433 tape.** ⇒ **the file has DOUBLED in six days.**

| | tape | when |
|---|---:|---|
| all-time MIN | 444 | `f78e400` 2026-06-20 |
| Dave's remembered figure | **9,274** | `00abdf3` 2026-07-23 |
| **all-time MAX** | **26,323** | **`113eefc` 2026-07-27** |
| last commit | 17,136 | `2b7bb72` 2026-07-29 |
| **working tree, #40's wrap** | **18,433** | uncommitted |

189 commits touch this file. Every figure is `tiktoken cl100k_base`.

## §2 — ★★ THE FINDING, and it is not the doubling

**The all-time maximum is the commit that introduced the growth contracts.**

`113eefc` — *"GM growth contracts, phase 1: the rules exist before any move cites them — and the
first honest measurement falsified D7's budget"* — **26,323 tape. The file has never been bigger,
before or since, than in the commit that wrote the rules against it growing.**

And it did not stop there. After that day's cut brought it to **13,200** (`e53afc4`, 07-27 22:14),
the programme ran continuously — sessions **#33 → #40**, seven sessions, all of them about the
record-keeping machinery. Over that stretch:

```
13,200  →  18,433      +5,233 tape, +40%
```

⇒ **the machinery built to stop GM growing has itself grown GM by 5,233 tape.** Every contract,
gate, ruling, correction, declared HOLE and fork lands in this file. ⚠ **#40's own wrap added
~1,300 of it** — a banner, a delta, a stratum and two corrections, every one correct by the ritual.

★ **This is [[gate-inside-the-growth-loop]] measured over six days instead of argued from one
session.** It is also the evidence behind Dave's sentence at #40: ***"this mechanism relies on
itself, which is why things spin out of control."***

## §3 — ⚠ WHAT THIS DOES *NOT* SAY. The honest qualifier, because the alarming reading is wrong

**The doubling is in the RETRIEVAL surface, not the cold-start cost.** Measured the same window:

| what | tape | state |
|---|---:|---|
| **read chain** (paid EVERY session) | **3,837** | ✅ **under M10's 4,500 warn — smallest in three sessions** |
| compactable region (retrieval) | 14,225 | over its 8,000 warn; block WITHDRAWN #39 |
| corpus GM+LS (retrieval) | 38,509 | over its 36,000 warn |

⇒ **#33's cut is holding.** A cold session pays 3,837 tape, and today's rolls made that *smaller*.
**Anyone reading "the file doubled" as "boot got twice as expensive" would be wrong**, and that
error is worth naming because it is the shape that produced the withdrawn compactable block —
[[premise-ages-faster-than-rule]].

⚠ **But two costs are real and neither is on any gate:**
1. **The corpus is over its warn**, so retrieval is searching a bigger, noisier surface.
2. **⬛ A human has to read this file.** Dave does. **No gate measures legibility**, and *"pfff"* is
   a reading no instrument here can take. ★ **The complaint arrived from the one reader the whole
   apparatus is built for, and nothing in the apparatus could have raised it.**

## §4 — THE METHOD, so it can be re-run rather than believed

```python
# per-commit size of GOOD-MORNING.md, oldest first
import subprocess, tiktoken
enc = tiktoken.get_encoding("cl100k_base")
log = subprocess.run(["git","log","--format=%h|%ad|%s","--date=format:%Y-%m-%d|%H:%M",
                      "--","GOOD-MORNING.md"], capture_output=True, text=True).stdout
for line in reversed(log.strip().split("\n")):
    h, day, tm, s = line.split("|", 3)
    txt = subprocess.run(["git","show",f"{h}:GOOD-MORNING.md"],
                         capture_output=True, text=True).stdout
    if txt: print(h, day, tm, len(enc.encode(txt)), s)
```

⚠ **`cl100k` is OpenAI's tokenizer, not Claude's** — every figure here is a PROXY (P3, raised by
Dave #39). ⚠ **The working-tree figure is uncommitted**; the last committed value is 17,136.

## §5 — PER-DAY TABLE (min · max · last, and the day's peak commit)

| date | commits | min | max | last | peak commit subject |
|---|---:|---:|---:|---:|---|
| 2026-06-19 | 3 | 745 | 1,337 | 1,337 | `33ed734` feat: contrast audits now gate the build + resolve r |
| 2026-06-20 | 1 | 444 | 444 | 444 | `f78e400` feat(knowledge): add advisory states-completeness pr |
| 2026-06-22 | 2 | 666 | 1,022 | 1,022 | `4199477` Table -> canon 9/9: card-collapse responsive + varia |
| 2026-07-02 | 6 | 1,010 | 1,463 | 1,312 | `48506ae` feat: north-star mock, charter §4 ratified, data-vis |
| 2026-07-03 | 7 | 1,222 | 1,584 | 1,562 | `37db284` brief: end-of-session GOOD-MORNING — desk cleared by |
| 2026-07-04 | 1 | 1,509 | 1,509 | 1,509 | `8eb151e` docs: refresh cold-start entry point — GOOD-MORNING  |
| 2026-07-05 | 11 | 923 | 1,433 | 1,309 | `8fb6077` docs: refresh GOOD-MORNING — spin-off register, insu |
| 2026-07-06 | 1 | 1,440 | 1,440 | 1,440 | `f0aed96` Record knowledge-usage trace design as prep tooling  |
| 2026-07-14 | 3 | 1,020 | 1,442 | 1,132 | `70d38f6` chore: restructure repo for human-readable navigatio |
| 2026-07-16 | 3 | 1,374 | 1,830 | 1,374 | `b1fd725` DataViz method dossier RATIFIED (Dave markup): appro |
| 2026-07-17 | 4 | 877 | 1,172 | 908 | `24accd0` Type-token system: reconciled primitives, Editorial/ |
| 2026-07-18 | 15 | 2,485 | 5,475 | 4,607 | `10c6e44` Handoff: make the Fable run self-kicking from the ha |
| 2026-07-19 | 11 | 4,641 | 6,293 | 5,244 | `d8330e6` docs: conductor handoff = strand menu + lanes (no me |
| 2026-07-20 | 13 | 4,748 | 7,348 | 7,348 | `f30eab0` docs(capture): COMMIT STATE → all evening-5 commits, |
| 2026-07-21 | 10 | 5,559 | 6,076 | 5,559 | `6e900b8` Record (not explore): component-type flex tier queue |
| 2026-07-22 | 10 | 5,753 | 8,568 | 8,568 | `99fcb6d` Chart-expansion scoped + Console corner fix + heatma |
| 2026-07-23 | 4 | 9,274 | 11,293 | 11,293 | `8c0e742` Wrap: bar-audit/conductor session captured — handoff |
| 2026-07-24 | 10 | 11,778 | 15,891 | 15,891 | `ec608c6` O1 "dark-in-light" ruled + inscribed (ADR-0014 D7/8) |
| 2026-07-25 | 8 | 10,451 | 17,405 | 10,651 | `1a7fd1f` Legend v5 (review candidate) + CANON table-popover m |
| 2026-07-26 | 6 | 10,274 | 12,704 | 12,704 | `f6c7f99` Capture ritual: lane 1 handoff + dossier + render-ve |
| 2026-07-27 | 28 | 12,598 | 26,323 | 13,200 | `113eefc` GM growth contracts, phase 1: the rules exist before |
| 2026-07-28 | 26 | 13,567 | 16,200 | 16,108 | `97d5ee8` Post-wrap addendum #28: chat titles — rename moves t |
| 2026-07-29 | 6 | 15,561 | 17,136 | 17,136 | `2b7bb72` The gate was inside the growth loop — the compactabl |

⚠ **Read the commit COUNT column too.** 2026-07-27 (28 commits) and 2026-07-28 (26) are the two
busiest days in the file's history **and both were machinery days** — growth contracts, the M-set,
the throttle, memento-search. The file's two heaviest days of change produced no components.

## Entry points

`notes/_GAUGE-LOG.md` (per-session bands + the tape/bill pairs) ·
`notes/_briefs/2026-07-30-nail-it-to-the-mast-structural-brief.md` (§1's growth loop — this receipt
is its six-day dataset) · `notes/_briefs/2026-07-29-roll-at-open-plan.md` §3 (displacement has a
floor) · `knowledge/_capture_gate.py` § `SIZE_BUDGET_TK`.
