# The gauge re-denomination — how a rule aimed at the wrong decision blanked a stamp for thirteen sessions

provenance: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367 · 2026-07-30
status: ruled — `notes/_MEMENTO-DECISIONS.md` § ★★ #56 (D23–D26)

> **Session #56, Opus solo, Dave live.** Spine entry: `_LIVE-STATE.md` ⏱ LATEST #56.
> Ledger: `notes/_MEMENTO-DECISIONS.md` § ★★ #56. Commits `52c54e9`, `82bfdf4`.
> **Dave opened with the proposal AND the diagnosis, and both were right.** This dossier records
> what verification added, what it took away, and the two things I got wrong on the way.

---

## 1. The opener, and why verifying a premise you agree with still matters

Dave's opening message was not a question. It was a diagnosis and a proposal:

> *"Pre-flight has been refused 12 consecutive sessions. The cause is the stamp's all-or-nothing
> format, not the measurement — one unobservable term (boot half) suppresses three measurable
> ones, which contradicts D10. Propose: re-denominate the pre-flight in absolute tape against
> thresholds, as the chain and banner caps already are."*

The temptation was to say *"agreed"* and start building. [[premise-ages-faster-than-rule]] says
verify the premise like repo state, and doing so changed three things:

- **The count was 13, not 12.** #54 recorded the twelfth; #55 the thirteenth. One session stale.
- **"Three measurable terms" was generous.** Only throughput is genuinely measured. Fill's disk
  half is measured and its harness half unreachable; **job and wrap are estimates in any unit.**
  Re-denominating does not make them measured — it makes them **statable without the
  unobservable denominator.** Still the prize, but a smaller and more defensible claim, and
  overselling it would have made the ruling easier to attack later.
- **⛔ The band could not be converted at all.** `45/60/63` are percentages *of the window*;
  converting them means multiplying by the exact quantity nobody can observe. So this was never
  a re-denomination of Dave's thresholds — **it needed NEW ones**, which [[m8-cap-at-its-own-floor]]
  says must be derived rather than picked.

★ **The last point was the one worth having.** Had I accepted "re-denominate" literally, I would
have shipped converted numbers wearing a measurement's clothes — the exact defect
[[measure-dont-convert-units]] names.

## 2. The dead end I walked into, and Dave walking me out of it

Having found the band un-convertible, I told him absolute thresholds were **not derivable** —
n=2 measured throughputs on record, and n=2 derives nothing. I offered a split: build the
D10 (c) stamp now, start collecting for the thresholds later.

His reply was blunt and correct:

> *"I feel like I'm banging my head against a wall. we had a test with an API key to estimate
> token usage, so we have a measurement mechanism… I just want a good way of estimating the
> price of jobs in tokens against the budget."*

**Two things I had wrong.**

**(a) The counter already existed.** `knowledge/_measure_tokenizer.py` calls Anthropic's
`count_tokens`; the key was in place; the endpoint is reachable from the sandbox. I had reasoned
about what we *could* measure without checking what we *already* measured.

**(b) The budget was never the window.** I had been trying to derive thresholds from our own
session history. Dave's framing — *"the point at which retrieval becomes unreliable"* — makes
the budget **a property of the model, not of our corpus.** That is published, and it does not
need n=anything from us.

★★ **And the finding that had been sitting in the repo for a day:**
`notes/2026-07-29-context-degradation-research.md`, finding 2 —
*"the band table's unit is wrong. The published degradation literature measures in absolute
tokens (32K/128K/200K). Apollo's throttle measures in % of window."* **A worker had written
Dave's proposal into the repo the previous session and nothing acted on it.** The wall he was
banging his head against was partly one we built.

## 3. The verification that moved my own recommendation

Dave asked me to check the *shape* of context rot on Anthropic models specifically. It changed
the number I had given him an hour earlier, which is the point of asking.

| what | finding |
|---|---|
| **Shape** | A **gradient, not a cliff** — Anthropic's own phrasing. |
| **Volume** | Claude scores **93% on MRCR v2 at 256K**, **76% at 1M**. |
| **Position** | Recall is **U-shaped** — start and end strong, **~30% weaker in the middle.** |

⛔ **What it invalidated:** my 150K recommendation. The 128–200K figures come from *other*
models — the fabrication study behind them tested 35 open-weight models, no Claude, a scoping
error **our own research note had already flagged and I repeated anyway.** The Claude-specific
number moved the working budget to **200K**, with 256K as the last measured-good point.

★★ **And the finding nobody had named:** the U-shape means **position is a lever, and a cheaper
one than shrinking.** `_CHAIN.md` is read first; the wrap is written last. **Canon already sits
at the two strong ends of every window** — the Memento architecture has been exploiting this
since #33 without anyone saying so. The operational consequence is now in the runbook and in the
gate's own notes: **a finding made mid-window is sitting in the weakest region, so write it to
its home when you find it rather than carrying it to the wrap.**

## 4. The argument that actually unstuck it

Thirteen sessions refused the stamp because the boot's harness half is unobservable, and each
read [[feedback-measuring-tool-must-not-guess]] as forbidding a number it could not measure.

**±8,000 tokens on a 200,000 budget is ±4%, and no job's go/no-go flips on 4%.**

★★ **We were holding a PLANNING ESTIMATE to a standard built for a PUBLISHED MEASUREMENT.**
"A measuring tool must not guess" governs what gets asserted as **fact** — a number another
session will quote without re-deriving. A planning figure is consumed **once, by the session that
wrote it**, to answer *"does this fit?"*. A labelled estimate with an error bar is the right
instrument there; refusing to produce one is not rigour, it is an unusable gauge.

⇒ **The operational rule, now in memory:** before withholding a number, ask **what decision
consumes it** — and **say which standard you are applying**, because the two look identical from
outside and that is how this hid for nineteen sessions.

## 5. The finding — a gate that matched the wrong line and looked healthy

While mutation-testing the new check, a control failed that should have passed. The cause:

**`PREFLIGHT_RE` accepted a bare `pre-flight:` but not the banner's `pre-flight #55:`.**

`check_preflight` takes the **first** matching line. Banners have carried the `#NN` form for many
sessions, so the regex skipped the live ★ LATEST stamp at the top of the file and matched **the
first ARCHIVED STRATUM** instead — blocks from #49–#51 that read *"FIFTH consecutive"*,
*"SIXTH consecutive"*, and are ratified history.

⛔ **Those blocks can never go green. For those sessions the pre-flight FAIL was unfixable by
construction** — writing a flawless stamp today could not clear a failure being read off a block
written weeks earlier. Sessions were staring at a red gate and correctly concluding their own
stamp was the problem. It wasn't.

★ **[[unmatched-grep-is-not-an-absence]], inverted into a fourth face: the pattern MATCHED, so
nothing looked broken — but a matched pattern is not the RIGHT pattern.** An unmatched grep
announces itself; a mis-targeted one reports success.

**And it recurred one function later, in the same wrap.** My new `ABS_TOTAL_RE` failed on the
first real stamp — `= **96,897 of 200,000**` — because every fixture I had written was plain text
while every banner in this corpus is bold-laden. **Same defect, same session, my own code:** a
pattern tested against the form its author types rather than the form the record is written in.
Both are now pinned by fixtures.

## 6. What was built

- **`knowledge/_gauge_tokens.py`** — real counts via `count_tokens`, content-hash cached (never
  mtime), `cl100k` demoted to a LABELLED fallback. Budget **amber 160,000 · working 200,000
  (Dave's) · hard 256,000 (sourced)**. `assert_budget_clears_floor()` mechanises #53's lesson so
  a cap at or under its own floor cannot ship again.
- **`check_preflight_tokens`** — 12 fixtures, every arm mutation-tested. **A declared gap passes,
  a silent one fails.** `RESERVE SPEND` buys the working overrun and **not** the hard one, because
  past 256K there is no measurement to reason from and **a receipt cannot manufacture evidence.**
- **The percentage path stays live and green** — additive per Dave's #55 ruling; it gets cut in
  one deliberate pass once the new path has proven itself, never both motions at once.

## 7. Dave's framing correction, which is bigger than the build

I proposed a stop line — *"Memento takes no new work, then back to Apollo."* He corrected it:

> *"memento is my project and context manager and I use it to build Apollo, so although I want to
> move on, I rely on Memento working to get Apollo done."*

★★ **Freezing the instrument to get to the work is freezing the thing the work runs on.** The rule
that replaced my stop line is **a test, applied per item**: *does this unblock Apollo, or is it
Memento improving Memento?* The first is built; the second is logged and deferred. Applied the
same hour: today's pre-flight **passes** (you cannot delegate or schedule work you cannot price);
the 2d delta gate **does not**, and was deferred rather than built.

★ **The corollary, and it is the answer to "how much is left":** the list is not the problem, the
**rate** is. #55 closed one gate and opened two items doing it. **Apply the test when an item is
born, not at the wrap when it is already written down.**

## 8. Still open

- **The delegation inversion — FLOATED BY DAVE, UNRULED.** *"Use subagents more often, parallels
  when I'm needed."* The Mode-2 ruling (2026-07-23) is stale for a nameable reason: it predates
  `_CHAIN.md`, the retrieval index and the gates. Three counters are on the table with it —
  the orchestrator's window is the fan-out ceiling (~15 returns); ★ **the binding constraint is
  VERIFIABILITY, not budget — delegate what a gate can check**; and he is currently doing the
  routing job himself, which is the real content of *"hard for me to manage"*.
- **Owed:** the #55 1b dossier · the archive CONTENT-probe · `ds-021`'s three-homes (**re-scope
  it** — #56 settled the unit question, only the write-up remains).
- **My two errors.** (i) I hand-rolled the git lock sequence instead of reading
  `_RUNBOOK-git-commit.md`, which has `_git_commit.sh` for exactly that — **the runbook counts
  this failure and I am the sixth session of eight.** Dave told me the runbook existed; I had not
  looked. ★ **A memory that summarises a runbook competes with it.** (ii) The 150K figure, above.
  ⚠ **Both are the same shape as #54's finding: the right source existed and was not consulted** —
  and the session's `consult-receipts` line is `none`, which is that failure showing up in the
  measurement.
