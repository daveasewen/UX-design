# BRIEF — Borrowed instruments programme (B2 → B1 → B3)
**2026-08-12 · v2 · supersedes `-v1` (kept on disk). Authored in a side session on Dave's "go" · conductor = the running session**
**Status: RULED-TO-EXPLORE by Dave (all three approved for speccing, 2026-08-12). NOTHING here is ENACTED. B3 carries an UNRULED fork (§5) and v2 adds FOUR further Dave-only rulings (§7) — all hard gates.**
**v2 delta:** adds §3b (three-tier promotion model), §3c (queue mechanics: backpressure · controller · deferment pricing), §3d (cadence), measured dream-pass history in §0, pitfalls P19–P23, expanded DO-NOT-RULE.

---

## 0. Provenance and receipts

Source material (verified, not paraphrased from the video):
- OpenAI, *Harness engineering* — https://openai.com/index/harness-engineering/ (doc-gardening agent, graded knowledge base, short AGENTS.md map, CI validation of docs)
- Anthropic, *Long-running Claude for scientific computing* — https://www.anthropic.com/research/long-running-Claude (progress file, failed-approach-with-reason records)
- Anthropic, *Effective harnesses for long-running agents* — https://anthropic.com/engineering/effective-harnesses-for-long-running-agents (structured handoff survives model upgrades; sprint scaffolding didn't)
- Arize, *Context management in agent harnesses* — https://arize.com/blog/context-management-in-agent-harnesses/ (plan stored on disk, short plan block re-injected ahead of noisy history every call)
- Anthropic, *Agentic coding and persistent returns to expertise* — https://www.anthropic.com/research/claude-code-expertise (behavioural only; justifies verification investment, adds no machinery)

Repo state at authoring: HEAD `f2e1409` (#163). `MEMORY.md` = **18,258 bytes measured on disk** (`wc -c`, sandbox mount, 2026-08-12). Boot floor canon: 54,859 ±1,178 real (re-based s129-D1). Stop line 150,929.

**Dream-pass history, measured** (`ls -lt notes/_dream/`, 2026-08-12): six proposals files — Jul 26 (×2, v2 same day), Jul 28, Aug 2, Aug 8, Aug 9. Cadence ≈ every 2–6 days, ad hoc. Sizes 19–27KB each. **Promotion status of these six files is UNMEASURED — conductor's first probe (§3d).**

⚠ CONDUCTOR: re-verify these premises before enacting anything — HEAD, the byte counts, the `_dream/` listing, and that files named below still exist. This brief was written against #163 and ages like any premise.

---

## 1. Goal and framing

Adopt three externally-validated context practices into Memento **without importing their governance model** (their agents self-edit docs; ours never do — with ONE narrow, Dave-ruled exception defined in §3b Tier 1). Order is dependency-driven:

**B2 (plan block) → B1 (gardener) → B3 (map grades).**

B3 depends on B1 as its refresh consumer. Do not reorder. Do not build B3 first — a grade with no re-checker is an instrument without a consumer, minted ~90 times.

Design law for the whole programme (added v2, from Dave's queue discussion): **the system adapts to Dave's attention; it never demands Dave adapt to the system.** Mechanise verification, never judgment. Enforcement = backpressure + friction-removal + visible pricing — never nagging, never deadlines, never auto-decisions.

---

## 2. B2 — Regenerated plan block at lane seams

**What:** `_checkin.py --block` emits a six-line block, REGENERATED from state at every lane seam (never carried forward):

```
SOURCE: <file> @ <mtime>  (provenance line — mandatory, line 0)
DONE:   <from _LIVE-STATE / chain>
DOING:  <current lane>
NEXT:   <next lane or item id>
STOP:   <stop condition — budget figure OR close condition>
BUDGET: <gauge headline, real tokens, method named>
```

**Rules:**
- GENERATE-NEVER-INHERIT (extend T3's subject to cover the block). A block pasted from the previous seam is the read-chain staleness class.
- The block is a RENDERING of state, never a store. ⛔ No `current.md`, no fifth register. If the block is wrong, fix state, regenerate.
- Sub-agent briefs embed the block + the DO-NOT-RULE list (s110 precedent).
- BUDGET line follows gauge law: real tokens, method travels with the number, no percentage without a named denominator.

**Mutation test (must be able to fail):** corrupt the SOURCE mtime → conductor must reject the block. Hand-edit a block and present it → seam check must detect non-regenerated block (hash the render inputs).

**Deliverable:** patch to `_checkin.py` + one runbook paragraph. Verification = RE-READ the emitted block against state, not the script's banner.

---

## 3. B1 — Doc-gardening lane

**What:** `knowledge/_gardener.py` + a pinned-**Opus** subagent lane, run as an arm of the dream-pass (same cadence, same governance). Two jobs: (a) FINDINGS — sweep canon/runbooks/memory-hooks for claims contradicted by repo state; (b) REFRESH — re-run the probes behind B3 grades and restamp them (once B3 exists).

**Hard fences (each is a BLOCK, not a warn):**
1. **FILE-ONLY**, except the Tier-1 carve-out IF AND ONLY IF Dave rules it (§3b). Default sole write target: one proposals file in `notes/_dream/`. Any other write → BLOCK.
2. **Quote-both.** Every finding quotes (a) the canon line verbatim with path:line, (b) the contradicting repo evidence verbatim, (c) the probe that produced (b). A finding missing any leg is refused by the output validator.
3. **Cap + rank.** Max N findings per pass (propose N=10; **value is Dave's**), ranked by ★-weight of the canon touched. Truncation DECLARED in the file.
4. **Header-wins.** A ratified record can be FLAGGED, never proposed-for-trim. Findings against ratified docs carry `FLAG-ONLY` status mechanically.
5. **Scope carve-out.** Wrap already has the s161-D4 stale-top-item fence. Gardener scope = what that fence does NOT see: mid-canon claims, runbook drift, memory hooks naming moved/absent files (the #80 class). No duplicate fence under a second name.
6. **Self-check.** First act of every run: verify its own target list resolves. Fails LOUD and NAMED, exits nonzero, files nothing.

**Budget note:** cheap in BUDGET, 5–10× in QUOTA (it's a sub). Weekly with dream-pass, never per-session. Name which budget binds before each run.

**Mutation tests:** (a) plant a known-false canon line → found with all three legs; (b) point one target at a moved file → loud exit; (c) attempt out-of-bounds write in test harness → BLOCK; (d) plant 15 findings-worth → caps at N; (e) [if Tier 1 ruled in] plant a pointer whose target moved WITH content change → must NOT auto-apply, must queue as Tier 2.

---

## 3b. Three-tier promotion model (v2 — Dave's review load)

Principle: **mechanise the verification, never the judgment.** Dave reviews exceptions, not everything.

**Tier 1 — MECHANICAL (pointer rot). Auto-apply, IF Dave rules the carve-out.**
Definition (all four conditions, machine-checked): the claim is a *pointer* (path, filename, line ref) — not a measurement, not a ruling, not prose meaning; the old target provably absent; the new target provably present; content hash of the target matches (the thing moved, it didn't change). Then: gardener repairs the pointer in place, logs every repair to a REGISTER (before / after / probe / hash), reversible via git. Dave sees only a count in the pass receipt.
⚠ **This is a carve-out from "promotion is Dave's alone" — absolute until now. It does not exist until Dave rules it, narrowly worded. Anything failing ANY of the four conditions is NOT Tier 1** (P19).

**Tier 2 — FACTUAL DRIFT. Machine does the legwork; Dave rules in one line.**
A stated figure/fact is machine-refutable (doc says 13 fails, suite measures 9) but the fix is a judgment (living figure vs ratified record-of-a-moment). Gardener runs the probe, quotes both sides, presents a one-liner: **update / it's a record, flag-only**. Batched in the controller (§3c), accept-all-able. ⛔ Never auto-applied — a "corrected" ruled datapoint is the boot-floor-band defect generalised.

**Tier 3 — MEANING. Never mechanised, no exceptions.**
Anything touching a ruling, a premise behind a ruling, Dave's recorded words, close conditions, or register status. Full finding, full evidence, Dave's eyes. Wrong Tier 1 = broken pointer; wrong Tier 3 = confident false tattoo — the founding risk. Tier classification itself is machine-checked; **ambiguity resolves UPWARD** (unsure ⇒ higher tier).

---

## 3c. Queue mechanics (v2 — gentle enforcement, system-side)

Three mechanisms. None nag, none deadline, none decide for Dave.

**① Backpressure — the queue caps itself.** While > Q items sit unreviewed (Q is Dave's; propose 15), the dream-pass proposal arm PAUSES — reports "queue full, K awaiting, oldest <date>" and adds nothing. Tier-1 repairs and grade refreshes CONTINUE (they don't need Dave). Gate-inside-the-growth-loop applied to Dave's attention: the pile cannot grow past reviewability. ⛔ Queued items NEVER expire, NEVER auto-close — a timeout that rules is invented ruling.

**② Controller — review as taps, not reading.** The queue renders as ONE live HTML deck (existing live-controller law: decision control per item, clicks compile to a single ruling message the conductor enacts). Card = canon quote · evidence quote · probe · [accept / flag / reject]. Target: ten items ≈ two minutes. This attacks the real behavioural trap — six 20KB prose files is a wall; cards are a coffee.

**③ Deferment pricing — visible age, stated cost.** One line on the boot surface (GOOD-MORNING, which exists for this): *"Review queue: 4 items, oldest 9 days — while it waits: grades on 3 ★★ entries decaying; proposal arm paused."* True cost, no alarm, no deadline. Precedent: `DEFER_STREAK` (`_gm_usage.py`) + the standing price-every-deferment instruction — this is that instruction, mechanised.

**Mutation tests:** (a) fill queue past Q → proposal arm must refuse, loudly, while refresh arm still runs; (b) controller with zero items → renders honest empty state, files nothing; (c) deferment line derived from a stale queue file → provenance check fails loud (no banner-trust).

---

## 3d. Cadence (v2)

Measured: passes run every 2–6 days, ad hoc. Ruled-by-this-brief as OPEN QUESTION with recommendation:
- **Frequency: keep roughly as-is.** The bottleneck is promotion, not generation; more passes = more backlog + quota (sub = 5–10× quota).
- **Regularity: fix it.** One scheduled weekly slot (proposal: Monday morning, before the week's sessions). Ad-hoc extras remain at Dave's word. Rationale: B3's STALE must mean "the world may have moved," not "Dave had a busy week"; a scheduled pass makes grade decay a real signal and quota spend predictable.
- **Conductor's first probe before any of this:** measure the promotion rate of the six existing proposals files. If few were promoted, the binding constraint is review friction → §3c ② is the priority build, and cadence changes wait.

---

## 4. B3 — Staleness grades on the map (⚠ BIGGEST CHANGE — §5 gate first)

**What:** every entry in the memory index gains a machine-written verification record: `last-verified date + probe name + result`. Written ONLY by the gardener's refresh pass (B1 is the consumer). Schema promotion is Dave's.

**Why it's the biggest change:** it alters *retrieval behaviour globally*. Once grades exist, sessions discount low-graded entries. That is the point — and the risk: a missed refresh silently demotes TRUE canon. The refresh cadence becomes load-bearing (§3d) with a gate that fails the dream-pass wrap if the refresh arm didn't run.

**Rules:**
- A grade is a CONCLUSION and conclusions are debt (s129-D5): every grade names its re-checker (the gardener) and its expiry (one dream-pass cycle → decays to STALE, visibly, automatically — absence of refresh must be VISIBLE, not silent).
- No grade from a banner: generated from a named probe or not written.
- Script-written only. Hand-written grade → validator rejects.
- Vocabulary must say UNKNOWN honestly. UNKNOWN never defaults to a passing grade.

**Mutation tests:** (a) skip refresh one cycle → all grades visibly STALE; (b) hand-edit a grade → rejected; (c) delete a probe a grade names → next refresh marks UNKNOWN, loud.

---

## 5. ⛔ GATE — the B3 fork (UNRULED, Dave's, conductor STOPS here)

**Option A — INLINE.** Grades inside `MEMORY.md`. ~30-char suffix × ~90 lines ≈ +2,700 bytes ≈ +15% on an 18,258-byte file, paid at EVERY boot, inside the ruled boot-floor band (54,859 ±1,178). **Requires a deliberate RE-BASE ruling BEFORE the first graded boot** — else the first graded session reads out-of-band and band discipline is damaged either way.
- Gain: notice-UNPROMPTED — staleness visible at recall, no lookup. The #49 property that justifies index residence.
- Cost: permanent boot tokens + re-base + every index edit touches graded lines. Near-irreversible once re-based.

**Option B — SIDECAR.** Grades in a separate file (e.g. `_MEMORY-GRADES.json`). Boot cost zero, index untouched, no re-base, fully reversible.
- Cost: look-up-BY-NAME. Unprompted recall shows today's confident one-liner — the doubt is in the drawer, not on the label. That blind spot is the founding failure mode; mitigations each add an instrument needing a consumer.
- Gain: reversible; converts a speculative irreversible ruling into a later evidenced one.

**Recommendation: B-then-review.** Sidecar + ONE bounded mitigation: the boot chain-read step prints grade alerts for ★★/⛔ entries only (few lines; measure real cost before ruling permanent). Run one full dream-pass cycle. Re-put the fork to Dave WITH numbers: how often a grade changed a retrieval decision; what the alert surface cost in real tokens. Promote to inline only if notice-UNPROMPTED measurably earned its boot tokens.

**Dave rules:** A now / B now / **B-then-review (recommended)**. Also his: grade schema, refresh cadence (§3d), and the §7 additions.

**Dave's stated conditions of engagement (2026-08-12, this session):** he accepts the sidecar blind spot only with the ★★/⛔ alert line; the refresh becomes a standing obligation missable only loudly; B-then-review MUST return to him with numbers — it is a deferral with a return date, not a disappearance.

---

## 6. Pitfalls register — enactment gates, not prose

Every row BLOCK or fail-loud. WARN is not a state here.

| # | Condition | Action |
|---|---|---|
| P1 | Plan block without SOURCE provenance line | BLOCK at seam |
| P2 | Plan block not regenerated (input-hash mismatch vs state) | BLOCK at seam |
| P3 | Any new file proposing itself as a state STORE (a `current.md`) | BLOCK — duplicate home is the defect |
| P4 | Gardener write outside `notes/_dream/` (Tier-1 register excepted IF ruled) | BLOCK |
| P5 | Finding missing canon quote+path:line / evidence quote / probe name | Finding refused |
| P6 | Findings > cap N | Truncate at N, truncation DECLARED |
| P7 | Finding proposes trimming a ratified record | FLAG-ONLY mechanically |
| P8 | Gardener target list has unresolvable path | Exit nonzero, loud, nothing filed |
| P9 | Grade written by hand / outside refresh pass | Validator rejects |
| P10 | Grade derived from banner rather than named probe | Validator rejects |
| P11 | Refresh arm skipped a cycle | Grades decay STALE visibly; dream-pass wrap declares it |
| P12 | Any B3 enactment before the §5 fork is ruled | STOP — Dave's gate |
| P13 | Inline chosen without boot re-base ruling first | STOP — band discipline |
| P14 | Sub spawned as Sonnet | STOP — Opus pinned, Dave #153 |
| P15 | Instrument built without naming its consumer AND what runs its proof | STOP before build |
| P16 | "VERIFIED" claimed off script output rather than re-reading the artefact | Reject the claim (ADR-0016) |
| P17 | Wrap skipped or delegated without brief + DO-NOT-RULE + `--wrap` | Non-negotiable, Dave #86 |
| P18 | Any lane > ~15K without an interior check-in | BLOCK — checkin law |
| P19 | Auto-apply of any change failing ANY of the four Tier-1 conditions | BLOCK — tier ambiguity resolves UPWARD |
| P20 | Tier-1 repair without a register entry (before/after/probe/hash) | BLOCK |
| P21 | Any queued item expired, auto-closed, or defaulted by timeout | BLOCK — invented ruling |
| P22 | Proposal arm generates while queue > Q | BLOCK — backpressure law |
| P23 | Deferment line computed from stale queue state (provenance check fails) | Fail loud, line omitted, omission declared |

## 7. DO-NOT-RULE (conductor must not decide; queue for Dave)

- §5 fork: A / B / **B-then-review** — **hard gate**
- **Tier-1 carve-out from "promotion is Dave's alone"** (§3b) — exists only on Dave's narrow wording — **hard gate**
- Grade schema and vocabulary
- Gardener findings cap N (10 is a proposal)
- **Queue cap Q** (15 is a proposal) **and the pause rule itself** — behavioural constraints on Dave are Dave's
- Refresh cadence + whether the weekly pass gets an actual schedule (§3d)
- Boot-floor re-base, if inline ever chosen
- Promotion of ANY gardener finding (Tiers 2–3 always; Tier 1 unless/until carved out)
- Anything touching the 19 unconditioned legacy items or the G-series in the chain

## 8. Verification standard

Per deliverable, three separate claims, never conflated: **RULED** (Dave's word, logged in `_rulings.json`) → **ENACTED** (code/file exists, re-read not banner-quoted) → **VERIFIED** (its mutation test was run and could have failed, and the artefact was driven on real data). Six-beat ladder applies. A green that can't fail is an assertion.

*— end of brief v2*
