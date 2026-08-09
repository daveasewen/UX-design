# #140 — the `s136-D1` precondition: schema amendment, slots rollout, and two vocabularies left open

provenance: 140 · 2026-08-09
status: ruled — `knowledge/_rulings.json` § `s140-D1`, `s140-D2`

*The WHY and HOW of #140. The WHAT lives in `knowledge/_rulings.json` (`s140-D1`, `s140-D2`), the
★ LATEST banner in `GOOD-MORNING.md`, and the ⏱ LATEST delta in `_LIVE-STATE.md`. Both-way links:
this dossier ← the banner and the delta cite it by path; it cites them here.*

---

## 1. The arc, and why it was one arc rather than five lanes

#139 handed #140 a five-item ruling queue. Only one of those items was a **precondition**: #139's
props-axes audit had measured `binds` 0/76, `slots` 0/76 and then found that `meta.schema.json`
**forbids both keys** (`additionalProperties: false`). That is not a finding about coverage, it is a
finding about what can be scheduled at all — the slots-rollout and DTCG lanes could not start.

So #140 did not sample the queue. It took the blocker, put it to Dave as a live controller, and
then rode the ruling straight through to enactment in the same window: **amend → draft → rule →
enact**. The other four queue items were left untouched and are carried, explicitly, as Dave's.

## 2. `s140-D1` — the amendment, and the read-back that changed nothing but proved something

Three questions went to Dave on `reviews/SCHEMA-AMENDMENT-CONTROLLER-2026-08-09-s140-v1.html`,
each with named alternatives; he answered in one message
(*"D1. lets do hybrid / D2. accept and make mandatory / D3. Permit now, enforce by gate later"*).

- **D1 — `binds` shape: HYBRID.** A single token-name string, an array, or an intent map. The
  alternative (pick one shape) would have been cheaper to gate and wrong for the corpus: the 280
  measured props include all three arities.
- **D2 — the slots contract, with `use` MANDATORY.** `accepts` is by tier or capability only; a
  child list is **mechanically refused** by `additionalProperties: false`. ★ The phrase *"make
  mandatory"* was ambiguous in isolation — it was read as the `use` field, per the controller's own
  D2 option text, and **confirmed in chat before recording**. The read-back cost one exchange and
  removed the only place this ruling could have been silently mis-inscribed.
- **D3 — permit now, enforce by gate later.** Both keys stay optional in the schema; `s136-D1`'s
  "binds mandatory for visual props" clause becomes a **shrink-only ratchet gate**, not a schema
  constraint. The reason is sequencing, and it is the same reason wrap-mode gates exist: a schema
  that demands `binds` on the day it ships makes every meta red for a state no build can fix.

**Evidence, and how it was made trustworthy.** 75/76 metas validate. The single failure is on
`EXAMPLE-button` and is **pre-existing** — established by a **control run against the
pre-amendment schema**, delta zero, rather than by inspection ([[attribute-the-diff]]). 13/13
drives green, including the arm that asserts a child-list `accepts` is **REFUSED** — a schema
whose refusals are undriven is an assertion, not a gate.

**Left open on purpose:** the intent vocabulary. Legal but unruled. A vocabulary invented by the
agent that ships inside a ruled schema would be a promotion nobody made.

## 3. `s140-D2` — the verdicts, and the amendment the draft could not see

The build sub drafted 42 contracts across 28 components, marked provisional-agent, and flagged 4
rows `$doubt` itself. Dave ruled off the review export.

24 accepted verbatim. The four that moved are the interesting part:

- **`cards` → DUAL-AXIS.** The draft had assumed the axes are exclusive: if a thing is a variant it
  is not a slot. Dave's amendment says both — the card variants **will** be built (axis B) **and**
  the content stays slot-injectable (axis C). The slot is kept, with a `$note` recording the second
  half. ★ **This is the finding of the session:** the three-axis model does not partition
  components, and the draft's implicit exclusivity was a modelling error nobody had written down.
- **`empty-state.body` → a text param**, which folds it into the FLOATED 38-row text-param
  refinement from #136 rather than resolving it here.
- **`segmented-control.content` → a variant-axis candidate**, not a slot.
- **`textarea.rows` REJECTED** — the audit had a false positive; it is a sizing param and always was.

**How it was enacted, and why not with a serializer.** The metas are hand-formatted. Any JSON
serializer would have reformatted 25 files and buried the ruling inside a whitespace diff, so the
insertion was **textual**, with a **per-file assertion that the rest of the file parses equal**.
That is the [[serializer-defaults-reformat-the-file]] rule applied rather than cited. 25 of 76
metas now carry ruled slot contracts.

**Left open on purpose, again:** the ~20 capability strings. Agent-proposed, UNRULED.

## 4. What the session got wrong, or could not prove

- ⬛ **The slots review HTML was never render-proven.** It was checked structurally; no browser ran
  this session. Declared at the time, not discovered afterwards — but it is an unproven artefact
  that Dave ruled from, and that is worth saying plainly.
- ⚠ **A new sandbox class: the immortal `index.lock`.** Every git op left a **zero-byte**
  `.git/index.lock` that neither git nor `rm` could unlink, and which then blocked the next op — so
  the runbook's `clear · stage · clear · commit · clear` sequence could not self-heal, because the
  clear step is itself a git op. The workaround was a **PATH shim**: a `git` earlier on `PATH` that
  `mv`s the lock aside and `exec`s `/usr/bin/git`, which covers the calls made *inside*
  `_git_commit.sh` as well as the direct ones. ⛔ It lives in `/var/tmp`. It is not in the repo, it
  dies with the sandbox, and calling it a fix would be a false inscription.
- ⚠ **The doubled-prefix msgfile class recurred a third time** (#133 · #139 · #140). The mechanism
  was new: a msgfile the script had already mutated on refusal was `cp`-ed and reused. Caught by
  subject-verify, amended from a fresh msgfile. Three occurrences is well past the
  [[gate-dont-patch]] trigger, and **the gate is still not built**.
- ⚠ **ENOSPC n=6** — `/sessions` 100% full at 1.1 M free, the worst reading recorded. Both
  documented remedies (`pip --target /var/tmp/...`, `TMPDIR=/var/tmp`) held; a sixth confirmation,
  not a new finding.
- ⛔ **The wrap opened ~2,000 tokens PAST the stop line** (152,901 vs 150,929). The cause is
  measurable and is a lane, not a mis-priced wrap: the memory-index compaction lane ran *after* the
  seam check-in, so the last reading available to the wrap decision was ~46K stale. This is exactly
  the failure [[checkin-at-the-ends-cannot-catch-the-lane]] describes; the remedy was cited this
  session and still not applied at lane granularity.
- ⚙ **boot 56,271 real — 234 ABOVE the 54,859 ±1,178 band.** A datapoint. It is recorded as an
  out-of-band reading and **not corrected into the constant**.

## 5. Resolved state, and what is still open

**Resolved:** the `s136-D1` schema precondition is gone — `binds` and `slots` are legal, and 25/76
metas carry ruled slot contracts. The DTCG re-encode and the `binds` rollout are now schedulable.

**Still open, and all of it is Dave's or unbuilt:** the intent-map vocabulary · the ~20 capability
strings · the four remaining #139 queue items (`PL_MAX_FRAC=0.42`, narrow-width columns, the 42
fork verdicts, the 15 token-split exceptions) · the doubled-prefix msgfile gate · a durable remedy
for the immortal-lock class · the memory-index archive-merge remainder (19.1KB against a 17.1KB
target) · the carried #139/#138 set (cold-sandbox symlink farm, `TMPDIR` fragility in
`_validate_kg`'s `check_freshness`, the unproven slots review render).
