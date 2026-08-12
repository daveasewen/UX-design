# BRIEF — Borrowed instruments programme (B2 → B1 → B3)
**2026-08-12 · v1 · authored in a side session on Dave's "go" · conductor = the running session**
**Status: RULED-TO-EXPLORE by Dave (all three approved for speccing, 2026-08-12). NOTHING here is ENACTED. B3 carries an UNRULED fork — a hard gate, see §5.**

---

## 0. Provenance and receipts

Source material (verified, not paraphrased from the video):
- OpenAI, *Harness engineering* — https://openai.com/index/harness-engineering/ (doc-gardening agent, graded knowledge base, short AGENTS.md map, CI validation of docs)
- Anthropic, *Long-running Claude for scientific computing* — https://www.anthropic.com/research/long-running-Claude (progress file, failed-approach-with-reason records)
- Anthropic, *Effective harnesses for long-running agents* — https://anthropic.com/engineering/effective-harnesses-for-long-running-agents (structured handoff survives model upgrades; sprint scaffolding didn't)
- Arize, *Context management in agent harnesses* — https://arize.com/blog/context-management-in-agent-harnesses/ (plan stored on disk, short plan block re-injected ahead of noisy history every call)
- Anthropic, *Agentic coding and persistent returns to expertise* — https://www.anthropic.com/research/claude-code-expertise (behavioural only; justifies verification investment, adds no machinery)

Repo state at authoring: HEAD `f2e1409` (#163). `MEMORY.md` = **18,258 bytes measured on disk** (`wc -c`, sandbox mount, 2026-08-12). Boot floor canon: 54,859 ±1,178 real (re-based s129-D1). Stop line 150,929.

⚠ CONDUCTOR: re-verify these premises before enacting anything — HEAD, the byte count, and that the files named below still exist. This brief was written against #163 and ages like any premise.

---

## 1. Goal and framing

Adopt three externally-validated context practices into Memento **without importing their governance model** (their agents self-edit docs; ours never do). Order is dependency-driven, not preference:

**B2 (plan block) → B1 (gardener) → B3 (map grades).**

B3 depends on B1 existing as its refresh consumer. B1 depends on nothing but is cheapest to fence after B2 proves the seam mechanics. Do not reorder. Do not build B3 first under any argument — a grade with no re-checker is an instrument without a consumer, minted ~90 times.

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

**What:** `knowledge/_gardener.py` + a pinned-**Opus** subagent lane, run as an arm of the dream-pass (same cadence, same governance). Sweeps canon/runbooks/memory-hooks for claims contradicted by repo state.

**Hard fences (each is a BLOCK, not a warn):**
1. **FILE-ONLY.** Sole write target: one proposals file in `notes/_dream/`. Any write outside → BLOCK. The gardener proposes; it never edits canon, never trims, never "fixes". OpenAI's gardener opens fix-up PRs — ours explicitly does not; auto-editing launders a misreading into canon, which is the confident-false-inscription class automated.
2. **Quote-both.** Every finding quotes (a) the canon line verbatim with path:line, and (b) the contradicting repo evidence verbatim, and (c) names the probe that produced (b). A finding missing any leg is refused by the output validator.
3. **Cap + rank.** Max N findings per pass (propose N=10; **the value is Dave's**), ranked by the ★-weight of the memory/canon touched. Uncapped = the Arize 27-call failure mode pointed at Dave's attention.
4. **Header-wins.** A ratified record can be FLAGGED, never proposed-for-trim. Findings against `_DECISION-HISTORY` or any ratified doc carry `FLAG-ONLY` status mechanically.
5. **Scope carve-out.** The wrap already has the s161-D4 stale-top-item fence. Gardener scope = what that fence does NOT see: mid-canon claims, runbook drift, memory hooks naming moved/absent files (the #80 class). Do not duplicate the wrap fence under a second name.
6. **Self-check.** First act of every run: verify its own target list resolves (files exist). Fails LOUD and NAMED, exits nonzero, files nothing. A gardener that silently sweeps a moved tree joins the #148 reds.

**Budget note:** cheap in BUDGET (report lands in fill), 5–10× in QUOTA (it's a sub). Weekly with dream-pass, never per-session. Name which budget binds before each run.

**Mutation tests:** (a) plant a known-false canon line → gardener must find it with all three legs; (b) point one target at a moved file → must exit loud; (c) attempt a write outside `notes/_dream/` in a test harness → must BLOCK; (d) plant 15 findings-worth → output must cap at N.

**Promotion:** Dave's alone, per dream-pass law. The gardener's output file is a queue of Polaroids; nothing self-promotes to tattoo.

---

## 4. B3 — Staleness grades on the map (⚠ BIGGEST CHANGE — read §5 gate first)

**What:** every entry in the memory index gains a machine-written verification record: `last-verified date + probe name + result`. Written ONLY by the gardener's refresh pass (B1 is the consumer). Schema promotion is Dave's.

**Why it's the biggest change:** it alters *retrieval behaviour globally*. Once grades exist, every future session will discount low-graded entries. That is the point — and the risk: a missed refresh silently demotes TRUE canon. The refresh cadence becomes load-bearing infrastructure and must be declared in canon, with a gate that fails the dream-pass if the refresh arm didn't run.

**Rules:**
- A grade is a CONCLUSION and conclusions are debt (s129-D5): every grade names its re-checker (the gardener) and its expiry (one dream-pass cycle → grade decays to STALE, visibly, automatically — absence of refresh must be VISIBLE, not silent).
- No grade from a banner (ritual output ≠ ritual ran): generated from a named probe or not written.
- Grades are written by script only. A hand-written grade is refused by the validator.
- Grade vocabulary must be able to say UNKNOWN honestly (measuring tool must not guess). UNKNOWN is never defaulted to a passing grade.

**Mutation tests:** (a) skip the refresh arm one cycle → all grades must visibly decay to STALE; (b) hand-edit a grade → validator rejects; (c) delete a probe a grade names → next refresh marks that grade UNKNOWN, loud.

---

## 5. ⛔ GATE — the B3 fork (UNRULED, Dave's, conductor STOPS here)

Two placements. **Do not enact either without Dave's explicit ruling.** Plain statement of each:

**Option A — INLINE.** Grades live inside `MEMORY.md` itself. Every boot pays for them. `MEMORY.md` is 18,258 bytes today; a ~30-char grade suffix on ~90 index lines ≈ +2,700 bytes ≈ **+15% on the index file**, landing directly inside the boot measurement. The boot floor is RULED at 54,859 ±1,178 and datapoints stay in band — so Option A **requires a deliberate RE-BASE ruling** (the s129-D1 kind) BEFORE the first graded boot, or the first graded session will read as an out-of-band anomaly and the band discipline is damaged either way (a "corrected" datapoint or a false alarm).
- Gain: notice-UNPROMPTED — staleness is visible the moment a memory is recalled, no lookup needed. By the #49 rule this is exactly the property that justifies living in the index.
- Cost: permanent boot tokens + a boot-floor re-base + every future index edit touches graded lines.

**Option B — SIDECAR.** Grades live in a separate file (e.g. `_MEMORY-GRADES.json` beside the index). Boot cost: zero. `MEMORY.md` untouched, boot floor untouched, no re-base.
- Cost: grades are look-up-BY-NAME — consulted only when retrieval or the conductor explicitly checks. A stale memory can still be *noticed unprompted* with a confident face, because the index line carries no mark. Mitigations exist (retrieval wrapper joins grades automatically; conductor checks grades at boot for ★-items only) but each mitigation is one more instrument needing a consumer.
- Gain: reversible, cheap, no ruled measurement disturbed. If grades prove their worth, promotion to inline later is a single, evidenced ruling instead of a speculative one.

**Recommendation (best-practice over convenience, stated plainly):** **Option B first**, with one mitigation — the boot sequence's existing chain-read step also prints grade alerts for ★★/⛔ entries only (a bounded, few-line surface; measure its real cost before ruling it permanent). Run one full dream-pass cycle. Then put inline-vs-sidecar to Dave again WITH measured evidence: how often grades changed a retrieval decision, what the alert surface cost in real tokens. Promote to inline only if the evidence says notice-UNPROMPTED earned its boot tokens. This converts an irreversible re-base into an evidenced one.

**Dave rules:** A now / B now / B-then-review (recommended). Also his: grade schema, gardener cap N, refresh cadence.

---

## 6. Pitfalls register — enactment gates, not prose

Each row is a checkable condition the conductor enforces. WARN is not a state here; every row is BLOCK or fail-loud.

| # | Condition | Action |
|---|---|---|
| P1 | Plan block presented without SOURCE provenance line | BLOCK at seam |
| P2 | Plan block not regenerated (input-hash mismatch vs state) | BLOCK at seam |
| P3 | Any new file proposing itself as a state STORE (a `current.md`) | BLOCK — state has homes; a duplicate home is the defect |
| P4 | Gardener write outside `notes/_dream/` | BLOCK |
| P5 | Finding missing any of: canon quote+path:line / evidence quote / probe name | Finding refused |
| P6 | Findings > cap N | Output truncated at N, truncation DECLARED in the file |
| P7 | Finding proposes trimming a ratified record | Demoted to FLAG-ONLY mechanically |
| P8 | Gardener target list has unresolvable path | Exit nonzero, loud, nothing filed |
| P9 | Grade written by hand / outside refresh pass | Validator rejects |
| P10 | Grade derived from banner rather than named probe | Validator rejects |
| P11 | Refresh arm skipped a cycle | All grades decay to STALE visibly; dream-pass wrap declares it |
| P12 | Any B3 enactment before the §5 fork is ruled | STOP — Dave's gate |
| P13 | Inline chosen without a boot re-base ruling first | STOP — band discipline |
| P14 | Sub spawned as Sonnet | STOP — Opus pinned, Dave #153 |
| P15 | Any instrument built without naming its consumer AND what runs its proof | STOP before build |
| P16 | "VERIFIED" claimed off script output rather than re-reading the artefact | Reject the claim (ADR-0016) |
| P17 | Wrap skipped or delegated without brief + DO-NOT-RULE + `--wrap` | Non-negotiable, Dave #86 |
| P18 | Any lane in this programme > ~15K without an interior check-in | BLOCK — checkin law |

## 7. DO-NOT-RULE (conductor must not decide; queue for Dave)

- §5 fork (A / B / B-then-review) — **hard gate**
- Grade schema and vocabulary
- Gardener cap N (10 is a proposal only)
- Refresh cadence
- Boot-floor re-base, if inline ever chosen
- Promotion of ANY gardener finding
- Anything touching the 19 unconditioned legacy items or the G-series in the chain

## 8. Verification standard

Per deliverable, three separate claims, never conflated: **RULED** (Dave's word, logged in `_rulings.json`) → **ENACTED** (code/file exists, re-read not banner-quoted) → **VERIFIED** (its mutation test was run and could have failed, and the artefact was driven on real data). Six-beat ladder applies. A green that can't fail is an assertion.

*— end of brief v1*
