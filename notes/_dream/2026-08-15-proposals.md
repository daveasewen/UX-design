# Dream pass 7 — floated proposals

provenance: `local_4191e490-a4c6-4ff0-9db7-ae0d4bb5e72e` · 2026-08-15
status: floated

*I PROPOSE ONLY. Nothing here self-promotes; promotion is Dave's alone on reading this file
(derivation-governance). Every prior pass's RULED rows and every prior pass's checked-clear list were
read before hunting, along with the 2026-08-09 pass's P1–P5, which are STILL FLOATED and are NOT
re-floated here — where new evidence bears on one it is referenced, not duplicated.*

Ranked by prevalence, highest first.

---

### P1 — Four owed items were copied onto a "STANDING CARRY" line in `GOOD-MORNING.md` precisely so a rolling banner would not lose them, and that line has not been touched in 56 sessions; its own counter still says "SEVENTH consecutive roll" while `_LIVE-STATE.md` says "twelfth roll" for the same item

- EVIDENCE:
  - `GOOD-MORNING.md:438` — *"**⬛ STANDING CARRY, COPIED UP AT #120's 2c EXIT CHECK** — items that
    lived ONLY on the #118 banner, which rolls this wrap."* It carries four items: **the commit-gate
    hatch** (`--acknowledge`/`SESSION_ACK`, declared DEAD #117) · **the archive-move body-grep gate**
    (owed since #117) · **the attribution re-probe** (*"now the **SEVENTH** consecutive roll"*) ·
    **varied tally queries** (owed since #115).
  - `git log -L438,438:GOOD-MORNING.md` returns **exactly one commit**: `e3174d1`, 2026-08-07, **#120**.
    The line has not been edited since. The chain is at **#176** — **56 sessions**.
  - All four item strings appear in exactly **one** live-spine location, that line. Greps across
    `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md` for `SESSION_ACK`, `body-grep` and `tally quer`
    return **1 / 0 / 0** each — the GM:438 hit only. They are **not** on #176's `residual → #177`
    list, which is the aged, EXIT-CHECK-protected carry list.
  - **A direct contradiction between two live counters for one item.** `_LIVE-STATE.md:687` —
    *"**The BOOT-RENT PLAN (P2)** and **the ATTRIBUTION RE-PROBE** — ⛔ **DAVE'S, twelfth roll at
    #125.**"* GM:438 says seventh (#120); LS:687 says twelfth (#125). Both frozen, 51 and 56 sessions
    respectively, and they disagree.
  - **The header ordinal is the same class and worse.** `GOOD-MORNING.md:10` —
    *"**STATE: ★★ THE READ CHAIN IS CUT (#33) and it HELD — EIGHTH session running.**"* The string
    `EIGHTH session running` was introduced by `1b27827` (*after #105*, 2026-08-05) and appears in no
    later commit that changes it, while `git log -L10,10` shows the **line itself** was edited as
    recently as `b60707c` (**#126**) — someone rewrote the line and left the ordinal. **71 sessions.**
  - **The contrast is what makes this a mechanism, not a nitpick.** The `residual → #N` carry list
    ages correctly — `s128-D2`'s brackets run `[2] … [33]` and increment every wrap — and `s161-D4`'s
    stale-top-item fence cross-checks it against `_rulings.json` (#176: *"0 fails, reported by the
    gate"*). **But the fence reads `residual → #N` lists only.** The STANDING CARRY block and the §
    header ordinal sit outside every fence, and they are the two places that rotted.
- PREVALENCE: **2 of 2** hand-typed ordinals living outside the `s128-D2` age-bracket system are
  stale (GM:438 by 56 sessions, GM:10 by 71); **0** of the ~50 bracketed residual ages are. Three
  live spine sites; one outright contradiction between two of them; four owed items reachable from
  exactly one unfenced line each.
- PROPOSED: smallest reversible step — **fold the four STANDING CARRY items into the `residual → #N`
  list at the next 2c EXIT CHECK, with `s128-D2` age brackets**, which brings them inside the
  `s161-D4` fence and inside the roll that already works; and **delete the two bare ordinals**
  (GM:438's "SEVENTH", GM:10's "EIGHTH") rather than re-stamping them — *stale twice ⇒ GENERATE*
  (`_CHAIN.md`'s own precedent for `_build_all.py`'s remedy string). If Dave wants the read-chain
  count kept, the `s129-D5` triage option is **generate it** from the stratum stack, not type it.
  Touches: `GOOD-MORNING.md` (:10, :438), `_LIVE-STATE.md:687`,
  `knowledge/_RUNBOOK-capture-ritual.md` step 2c.
- status: floated

---

### P2 — The one repeatedly-measured, ~26K-per-session process cost in the record — the conductor opening `GOOD-MORNING.md` at boot — stopped being measurable at #176, because nothing in the wrap brief requires the conductor to declare its boot reads

- EVIDENCE:
  - `notes/_GAUGE-LOG.md`, post-mortem **#173**: *"the conductor declared its own overspend rather
    than letting the arithmetic absorb it: **it opened `GOOD-MORNING.md` at boot** — the reflex
    `_CHAIN.md`'s header banner bans — **costing roughly 25–30K of the window**. ★ That is the
    session's process finding: **the read-chain cut is enforced by a COMMENT, not a gate**."*
  - Same file, post-mortem **#175**: *"⛔ **NAMED CAUSE: the conductor opened `GOOD-MORNING.md` at
    boot, ~26K** — the exact reflex `_CHAIN.md`'s header banner bans, and the exact overspend #173
    recorded as its own finding ⑦. **SECOND SESSION RUNNING.**"*
  - **#176 residual ⑭** (`_CHAIN.md`, the `residual → #177` list): *"**THE CONDUCTOR'S GM OVERSPEND
    [4]** — ⚠ **and it is NOT reported for #176: no boot-read of `GOOD-MORNING.md` was declared to
    this sub either way, so the item is carried UNMEASURED rather than claimed clean.**"*
  - So the series is: **measured (#173) → measured and worse for being unchanged (#175) → unmeasurable
    (#176)**. The item itself is homed and carried at age `[4]`; what is *not* homed is that its only
    data source is a voluntary sentence a conductor may or may not put in a wrap brief. The wrap sub
    cannot measure the conductor's window (`s168-D2`, and every gauge line says so), so the honest
    `UNMEASURED` is now the *default*, not the exception — and an item that reads UNMEASURED forever
    is indistinguishable from one nobody is chasing [[unrun-search-indistinguishable-from-absent-record]].
  - The instrument half is already conceded in the record: *"the read-chain cut is enforced by a
    COMMENT, not a gate — **and a comment cannot fail**"* [[instrument-without-a-consumer]].
- PREVALENCE: **3 of the last 4 wraps** (#173, #175, #176) name this cost; 2 of 3 with a number, the
  third declared unmeasurable. It is the only cause in `_GAUGE-LOG.md` since #170 that repeats with a
  named mechanism rather than as noise.
- PROPOSED: smallest reversible step, and it is one line, not an instrument — **add a required field
  to the wrap-sub brief: "boot reads: <files opened at boot, or NONE>"**, so the wrap can report
  MEASURED or CLEAN instead of UNMEASURED. Home it in
  `knowledge/_RUNBOOK-parallel-conductor.md`'s brief template alongside the `s172-D3` machinery-price
  line and the `s165` consequences/pitfalls section. ⛔ **Explicitly NOT a new gate** — `s172-D3`
  fences appetite for new instruments, and this proposal deliberately takes the cheapest of the
  `s129-D5` three options (**a named re-checker in prose**, not a built one). If Dave prefers, the
  alternative is to **stamp the item with an expiry**: if it reads UNMEASURED twice more, it is
  struck rather than carried.
- status: floated

---

### P3 — Three memory files publish a boot figure that contradicts the ruled `s171-D1` band, and two of the three publish it in the `description:` frontmatter — the field that renders in the index and in search results, while the correction sits in the body

- EVIDENCE (all paths under the mount's `.auto-memory/`):
  - The ruling: `s171-D1` (#171, 2026-08-14) — **`BOOT_FIRSTTURN_TK 54,859 ±1,178 → 56,158 ±849`**.
    Verified live in code: `knowledge/_gauge_tokens.py:166-167` reads `BOOT_FIRSTTURN_TK = 56_158` /
    `BOOT_FIRSTTURN_ERR = 849`. Band = **55,309 … 57,007**.
  - `boot-floor-measured-109.md:3` — `description: "The boot floor is **75,899 real** — the gauge
    published 30,499…"`. That is **18,892 above the band ceiling**. The file's own body, line 15,
    carries the correct re-base. **The same file states both.**
  - `boot-measurable-via-usage.md:3` — `description: "…re-measured live 08-02 (**boot 61,854**)…"`.
    **4,847 above the ceiling.**
  - `budget-vs-quota-vocabulary.md:11` — *"Today: stop line 150,929 (the wrap already carved out) −
    **boot 62,462** = **88,467**."* A **derived** figure, and it is the one Dave is most likely to
    quote as "my budget". On the ruled band it is `150,929 − 56,158 = **94,771**` — the published
    number understates the working budget by **~6,300 real tokens**, in the hook whose whole job is
    the BUDGET-vs-QUOTA vocabulary.
  - This is textbook `s129-D5`: a **conclusion inscribed as a number** (an arithmetic result and two
    measurement snapshots) in a place nothing re-derives, in a domain whose own memory hook rules
    *"datapoints stay IN band; never 'correct' one into another"* — the rule the corpus obeys for
    *datapoints* and breaks for *derived figures*.
  - Corroborating, and it is why this is timely rather than perennial: at the close of #176 the
    conductor told Dave in chat *"fire the dream-pass whenever you like — **the memory index is due
    its compaction**"* (session `local_991c6fc6`). A compaction that carries these three strings
    forward makes them harder to find, not easier.
- PREVALENCE: **3 of the 5 memory files that state a boot number** contradict the ruled band
  (`grep -lE "boot [0-9]{2},[0-9]{3}|boot floor is [0-9]" *.md` → 5 files; `hook-overflow-2026-08-08.md`
  is a dated archive and `surface-recorder-built-113.md` is already flagged in the index as
  *"3 constants MEASURABLY STALE"*, so both are honest). **2 of the 3** are in `description:` — the
  retrieval surface. Corpus context: **14 of 279** memory files are gauge/context-accounting hooks,
  **59,706 of 1,077,517 bytes (5.5%)**, which is why one re-base has this many places to rot.
- PROPOSED: smallest reversible step, and it is Dave's to run because it edits memory — **at the
  compaction pass, fix the three strings only**: (a) `boot-floor-measured-109.md` description →
  state the *current* ruled band with the 75,899 kept in the body as the #109 finding it was;
  (b) `boot-measurable-via-usage.md` description → drop the parenthetical figure, keep the claim
  ("directly measurable via `message.usage`") which is what the hook is *for*;
  (c) `budget-vs-quota-vocabulary.md:11` → replace the frozen arithmetic with the **form**
  (`budget = stop line − boot`) and point at `knowledge/_gauge_tokens.py` for the terms — the
  `s129-D5` **generate-it** option, and the one that cannot rot at the next re-base.
  ⛔ Consequence to state plainly: this is the third re-base (#109 → `s129-D1` → `s171-D1`); a fourth
  will rot any figure left in prose, so (c)'s form-not-number shape is the only durable one of the three.
- status: floated

---

### P4 — Enacting a ruling breaks its predecessor's provenance anchor by construction, so `_governs.py` will accrue one permanent FAIL per re-based constant forever — and one of the two current anchor fails names a text string that never existed at the address it points to

- EVIDENCE:
  - `python3 knowledge/_governs.py --selftest` today: **14 FAILs, rc=0**. This matches the #176
    record exactly (*"`_governs` selftest went 7→14 on the new entries"*) — **the count is not the
    finding**; twelve of the fourteen are the `s175-D1`/`s176-D1`/`s176-D2` evidence-format nits the
    record already carries as residual ②. The finding is the other two.
  - **Fail 1 — rot caused by correct enactment.** *"ruling **`s129-D1`** points at
    `knowledge/_gauge_tokens.py#BOOT_FIRSTTURN_TK = 54_859` — the file is there but the ANCHOR TEXT
    IS GONE."* It is gone **because `s171-D1` was enacted** and changed that very line to `56_158`
    (`_gauge_tokens.py:166`). The anchor did not rot from neglect; it rotted from the system working.
    Every future re-base of a ruled constant produces exactly this, one per re-base, permanently.
  - **Fail 2 — an anchor that was never resolvable.** *"ruling **`s171-D1`** points at
    `notes/_GAUGE-LOG.md#boot-drift DECLARED #170 - series 55,337 / 55,309 / 56,170 / 56,326 /
    56,527 / 56,693` — … ANCHOR TEXT IS GONE."* The target line exists at
    `notes/_GAUGE-LOG.md:1660` and reads *"**boot-drift DECLARED #170 (2026-08-14):** mean 56,060 ·
    constant 54,859 ±1,178 · delta +1201 … **Samples now n=6: 55,337 · 55,309 · 56,170 · 56,326 ·
    56,527 · 56,…**"* — separator `·`, not ` / `, and no substring `- series`. **The anchor string
    was never present verbatim, at #171 or since.** It has failed identically for five sessions and
    was read the whole time as "pre-existing rot" rather than "born broken"
    [[assertion-propagation-gap]] — *a claim never true is never chased either*.
  - The record's current disposition is residual ㉑ *"TWO `_governs.py` ANCHOR FAILS ARE PRE-EXISTING
    AND UNREPAIRED — `s129-D1` and `s171-D1`; ⛔ repointing them is a `#127` re-stamp."* That is a
    correct refusal of the *wrong* remedy and it is why the item has not moved in five sessions —
    but it treats one class where there are two, and neither is repaired by repointing.
  - ⚠ Second-order, and it is the sharper half: **`s171-D1`'s surviving anchor points into
    `notes/_GAUGE-LOG.md`, which the 2f roll rewrites every wrap.** A pointer into a rolling artefact
    is guaranteed to rot [[read-chain-is-where-staleness-is-free]]. *(Checked, so this is not a second
    bug: the gauge log lagging the chain by one session — tail `#### 2026-08-14 #175` at #176 — is
    **by design**, GM keeps LATEST only and 2f rolls #N−1 out. Verified across four commits,
    `fa0729b`/`b51b622`/`76b024c`/`be1e0a7`, each tail = its own N−1.)*
- PREVALENCE: 2 anchor fails of 157 rulings today, but **structurally one per re-based constant, for
  ever** — this is the third boot re-base and the second is already dead. 5 sessions (#171→#176)
  reporting Fail 2 as rot when it was never resolvable. 1 of 2 live anchors in the gauge family
  points into a file the wrap ritual rewrites weekly.
- PROPOSED: two small, separable steps, **neither of which is a repoint** —
  (a) **`s129-D1` gets a `superseded_by: s171-D1` marker and its anchor is retired, not repointed** —
  a superseded ruling should not be asked to resolve against live code; `_governs.py` should skip
  anchors on superseded rulings, which is a ~3-line change and turns a permanent false-red into a
  true green. ⛔ Consequence: this makes it possible to hide a real rot by mislabelling something
  superseded — so the skip should **print the skipped anchors**, not swallow them.
  (b) **`s171-D1`'s `evidence[0]` is declared NEVER-RESOLVED and replaced with a legal form** —
  `chat #171 2026-08-14` and `commit 6d5db13` are both already in that entry's other two evidence
  strings and both resolve; the broken one adds nothing. ⛔ This *is* an edit to ratified record and
  is therefore **Dave's**, not a session's — floated, not proposed for enactment.
  ★ And the generalisable line, if he wants one: **an evidence pointer into a file the capture ritual
  rolls (`GOOD-MORNING.md` banners, `notes/_GAUGE-LOG.md` strata, `_LIVE-STATE.md` deltas) is
  invalid on arrival** — point at the commit or the chat, which do not roll.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(dd1) The `_governs.py` fail count is honestly reported, and the 12 evidence-format nits are
  correctly refused.** Measured **14** this pass; #176's own banner says *"7 → 14, measured both
  ends"* and residual ② adds *"⛔ **repair is an edit to RATIFIED RECORD and is not a wrap's call.**"*
  The number is right, the ownership is right, the refusal is right. P4 above deliberately excludes
  all twelve.
- **(dd2) `notes/_GAUGE-LOG.md` lagging the chain by exactly one session is BY DESIGN, not drift.**
  At #176 the tail is `#### 2026-08-14 #175`. Verified across four consecutive wrap commits — each
  one's gauge-log tail is its own N−1, because step 2f rolls the previous stratum out of GM. A future
  pass finding "the gauge log has no #N block" should read it as 2f working. *(This is why I did not
  float it; I had it half-written as a finding before checking.)*
- **(dd3) The `s161-D4` stale-top-item fence really ran at #176 and really passed.** The banner
  records *"every `residual → #N` owed claim cross-checked against `_rulings.json` status before
  committing — **0 fails**, reported by the gate."* P1 is not a claim that the fence is broken; it is
  a claim about the **region** the fence's glob does not cover [[gate-glob-scope-rule]].
- **(dd4) `.github/workflows/gates.yml`'s misleading comment and the `[107]` CI gate are already
  carried and priced.** Residual ⑩ names them with a remedy price (*COULD-NOT-ASK ~8–12K +
  `fetch-depth: 0` ~2K; ⛔ QUEUED NOT BUILT*). Correctly homed under `s172-D3`; not re-reported.
- **(dd5) The working tree was clean before and after this pass, and I wrote nothing but this file.**
  `git status --porcelain` → empty at open and at close. The only executable I ran against the repo
  was `knowledge/_governs.py --selftest`, which is read-only and left no diff. The stale zero-byte
  `.git/index.lock` on the mount is the known wart (memory hook `git-lock-mv-not-rm`); git worked
  around it, and ⛔ I did not touch it.
- **(dd6) Pass 6's P1 is UNCHANGED and still floated — referenced, not re-floated.** It reported
  **21 of 96** rulings frozen at the #119 metadata sweep string. Re-measured today: still exactly
  **21** such strings, while the store has grown to **157 rulings**. The absolute count has not
  moved, so the defect is bounded and not spreading; the *ratio* improved only because the
  denominator grew. Recorded here as evidence for Dave's eventual ruling on P1, not as a new finding.
- **(dd7) Out of scope by standing exclusion, recorded so it is not mistaken for an oversight:** this
  lane's own §🔀 status row in `_LIVE-STATE.md` was last written for pass 6 (2026-08-09). Dream-lane
  mechanics are barred from this pass's floating (pass 6, cc6). Noted, deliberately not proposed.

---

## Method

**Shape A (Cowork), pass 7.** Session `local_4191e490-a4c6-4ff0-9db7-ae0d4bb5e72e`, date **2026-08-15**
from the host's `date` (`Sat Aug 15 08:14:31 BST 2026`), not recalled. Repo root
`/Users/daviewen/Documents/Claude/Projects/UX-design`.

**⛔ CONTEXT FACT, declared not investigated (per dispatch):** this fire ran **Sat 2026-08-15, a day
ahead of the ruled Sun 07:10 cadence**. It is an early sitting on Dave's word, recorded on the #176
`residual → #177` list as item ㉓ (*"THE DREAM PASS IS SCHEDULED BY DAVE FOR AFTER THIS SESSION
[NEW — 0 — DAVE'S, DATED]"*), so the off-cadence run is expected, not drift. I did not investigate it.

**⛔ THE COVERAGE GAP, STATED PLAINLY, AS PASS 6 DID.** Pass 6 covered through **#136**. The chain is
now at **#176** — **forty sessions uncovered**. The transcript window is fifteen, and it spans
**#161–#176** exactly (`list_sessions`, 18 returned: fifteen numbered Apollo sessions #161–#176 plus
three side sessions — the designer presentation, the harness-borrows side quest, and a second #166).
So **#137–#160 — twenty-four sessions — are reachable only through repo artefacts**, and a finding
that lived only in one of those chats and left no artefact is **invisible to this pass**. Every
proposal above rests on a repo receipt produced this pass, not on a transcript claim.

**Read, in spec order:** `MEMORY.md` memory index (hooks only, as injected context) ·
`.claude/agents/dreamer.md` in full · `_CHAIN.md` (the #176 banner, `residual → #177` in full, and
the post-wrap addendum) · `GOOD-MORNING.md` by targeted line reads and greps only — ⛔ **deliberately
NOT opened top-to-bottom**, since a conductor doing exactly that is the subject of P2 · `_LIVE-STATE.md`
§🔀 rows and targeted greps · **all six prior proposals files**: every `### P` heading and every
checked-clear list (pass 3's, pass 4's (q)–(w), pass 5's (x)–(bb), pass 6's (cc1)–(cc6)) **before**
hunting anything, plus pass 6's P1–P5 headings, which remain floated and are not re-floated.

**Repo forensics run this pass:** `git log -L` line-histories on `GOOD-MORNING.md:10` and `:438` ·
`git log -S` on four frozen strings · `git show <sha>:notes/_GAUGE-LOG.md` across four wrap commits
(the 2f-lag control) · `knowledge/_rulings.json` parsed (157 entries; status census; `s129-D1` and
`s171-D1` evidence arrays read verbatim) · `knowledge/_gauge_tokens.py:166-167` read ·
`knowledge/_governs.py --selftest` run (14 fails, rc=0) · `notes/_GAUGE-LOG.md` #173/#174/#175 strata
read in full · `.github/workflows/gates.yml` read · the memory corpus at `.auto-memory/` measured
(279 files, 1,077,517 bytes; 14-file gauge family, 59,706 bytes) and grepped for boot/stop-line/window
figures.

**⛔ Nothing was written except this file.** `git status --porcelain` was **empty at open and empty at
close**. `_governs.py --selftest` is read-only and produced no diff; no tracked file was modified, so
nothing needed restoring. No git operations beyond read-only `log`/`show`/`status`. No memory writes.

**Transcripts.** `list_sessions` (18) read for the window map; **one transcript read in full**,
`local_991c6fc6` (#176), for its closing turns — it supplied Dave's own words on the mint
(*"okay lets mint these… lets get these in for now!"*) and the conductor's *"the memory index is due
its compaction"*, which is P3's timeliness receipt. The other fourteen were **not** read at turn
level this pass, and that is a deliberate trade stated rather than smoothed: pass 6 established that
turn-level transcripts carry tool names without arguments or results, so every checkable claim has to
be re-verified in the repo anyway. With forty sessions uncovered and fifteen transcripts available,
**repo forensics is the higher-yield instrument**, and all four proposals are built from it. ⚠ **The
cost of that trade, named:** a **repeated verbal instruction** from Dave across #161–#175 that left no
artefact would not have been caught. That is this pass's largest blind spot.

**Where the ceiling bit.** P2's whole subject — whether a conductor opened `GOOD-MORNING.md` at boot —
is exactly the kind of fact a turn-level transcript **cannot** answer (tool calls appear as bare
names). The record answers it for #173 and #175 only because those conductors *volunteered* it. That
is not incidental to P2; it **is** P2.
