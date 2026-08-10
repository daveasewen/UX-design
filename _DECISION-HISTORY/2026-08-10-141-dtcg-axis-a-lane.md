# #141 — the DTCG / axis-A lane: a ruling, an enactment, and a finding that re-priced the lane

provenance: 141 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA (#141) · `GOOD-MORNING.md` ★ LATEST (#141).
Ledger: `knowledge/_rulings.json` § `s141-D1`. Commits: `9196e13`, `b4f59e6` — both pushed by Dave.
Both-way links per `_DECISION-HISTORY/README.md`.*

---

## Why this session existed

#140 closed with residual ① : *"DTCG re-encode + `binds` rollout (0/76) — UNBLOCKED BY `s140-D1`"*.
That framing carried an assumption nobody had tested: that the rollout was a **migration** — that the
addresses existed somewhere in the corpus and the job was to move them into a new key. #141 opened to
do the migration and closed having discovered that the migration is mostly not available.

The arc ran end to end in one session: **survey → gates → Dave's ruling → enactment → push.**

## Finding 1 — the survey found four decisions, not one job

`knowledge/_draft_binds.py` walked 277 props across the meta corpus and produced
`reviews/BINDS-DRAFT-2026-08-09-s141-v1.json`. It proposed **12 bindings** and flagged **120 rows
`$doubt`** — flagged by the drafter itself rather than smoothed, which is the same discipline the #140
slots draft used.

Alongside it, the DTCG conformance work surfaced three more open questions that were **not** the
agent's to answer: the `number`→`dimension` class (104 tokens), the `layout.json` scale-1/2/3 encoding,
and the component-composite `lineHeight` key. Each had named alternatives, so each went to Dave rather
than being decided by the enacting agent.

**The why:** an agent that picks the encoding is minting a ruling and calling it enactment. The four
questions were put on a live controller — `reviews/BINDS-REVIEW-2026-08-09-s141-v1.html` — with the
alternatives stated, because Dave rules by seeing.

## Finding 2 — `s141-D1`, and the read-back that preceded it

Dave ruled all four off the controller's own export, verbatim, and the ruling was **read back in chat
before being recorded**. The four verdicts:

- **(A) number→dimension: MIGRATE-TICKED, all 104, none excluded.** `$type: "dimension"` with a px
  unit. ★ The clause that matters for later: *the unit-strip for raw-number consumers is priced
  separately, **not waived*** — the ruling did not quietly absorb a cost it had not seen.
- **(B) `layout.json` scale-1/2/3: B1 — dimension + `$extensions`.** The token value is the scale's
  min-width entry viewport; the full breakpoint set is preserved **verbatim** under
  `$extensions com.apollo.sds`. The alternative (collapse the set) would have destroyed information
  DTCG has no slot for; B1 keeps it addressable.
- **(C) binds draft: ACCEPT-PROPOSED.** The 12 land. ⛔ **The 120 `$doubt` rows stay OPEN** — accepting
  the confident dozen is explicitly not accepting the doubtful hundred.
- **(D) composite `lineHeight`: OMIT.** The key stays absent, `DEF-COMPONENT-LINEHEIGHT` stands, and
  `--strict` keeps failing until it is ruled. A deferral that keeps a gate red is more honest than a
  guess that turns it green.

Recorded into `knowledge/_rulings.json` by **textual insertion**, with the **prior 100 rulings asserted
parse-equal**. The hand-formatted-JSON lesson (a serializer would have reformatted the file) was
applied rather than cited.

## Finding 3 — the enactment, and what was proven rather than asserted

Two commits, both pushed by Dave.

**`9196e13`** — `typography-composites.json` re-encoded to DTCG composites with a **reverse-map
assertion** and a `-pre-s141` backup; **`_validate_dtcg.py` built, 6/6 drives including a named-error
arm**; **`_validate_binds_ratchet.py` + its floor file built, 5/5 drives**; the binds draft and the
review controller.

**`b4f59e6`** — the **104-token migration across 5 spine files** (4 by round-trip, typography by
textual insertion, per the serializer rule); B1; the **12 bindings into 11 metas**, textual and
schema-checked; the unit-strip seam `knowledge/_dtcg_units.py` **wired into 4 consumers**, with
`canon.css` and **75 snippets proven byte-identical** — which is the load-bearing proof: a token-type
migration that changed a single rendered byte would have been a silent regression. DTCG deferrals went
**65 → 61**, and the two ruled classes were not merely retired but **promoted to a blocking
`DTCG-006`** — the deferral became a gate, which is the only way a ruling stops needing to be
remembered.

The ratchet floor moved **0 → 11**, and **lowering is refused by construction**: `--rebase` only ever
raises it. That is the enforcement half of `s136-D1` axis A, staged exactly as `s140-D1` (D3) said —
permit now, gate later.

## Finding 4 — the finding that re-priced the residual it came from

★ **Axis A is an authoring job, not a migration.**

Of **109 visual props**, only **12 had a recoverable spine address**. The meta `tokens` maps — the
obvious place to mine addresses from — are **prose**: **391 of 561 entries resolve to no address at
all**. There is nothing to migrate for the remaining ~97; the bindings have to be **authored**, prop by
prop, against Dave's pick-lists (which exist for 62 of them).

**Why this matters more than the enactment does:** #140's residual ① priced this lane as a mechanical
rollout. If #142 inherits that framing it will price an authoring wave as a migration and be wrong by
an order of magnitude. Coverage after enactment, measured: **11 of 75 metas · 12 of 109 visual props.**

## Finding 5 — two process classes, one recurring and one that stopped

⚠ **The msgfile-mutation class recurred — fourth session running (#133, #139, #140, #141).** The shape
this time was new and instructive: the conductor re-ran `_git_commit.sh` with the **same msgfile for a
diagnostic**, and got a **tripled** prefix. The existing rule — *a fresh msgfile per attempt* — is
written down and was followed for real attempts; nobody had thought of a **diagnostic** as an attempt.
The gate is still unbuilt and the candidate regex is still known. This is now the clearest
gate-don't-patch trigger on the board.

✅ **The #140 "immortal `index.lock`" class did NOT recur, and the reason is a step rather than a
tool.** `_RUNBOOK-git-commit.md` **step 0** — ask for the delete grant at the first commit of the
session — was followed. Git tidied its own locks. The entire `mv` choreography was unnecessary, and
**#140's `/var/tmp` PATH shim was never needed at all**.

⇒ #140 residual ⑤ ("the immortal-lock class needs a durable remedy") should be **re-priced, not
carried verbatim**: the durable remedy may simply be *"run step 0, every session"*. **This session did
not rule that** — one non-recurrence is one datapoint, not a proof — and it goes to #142 as a
confirm-or-retire item.

## Finding 6 — what was declared rather than smoothed

- ⬛ **Neither review HTML was render-proven.** `BINDS-REVIEW` (this session) and
  `SLOTS-DRAFT-REVIEW` (carried from #140) were checked structurally; no browser run happened in
  either session. Two sessions of render-proof debt, carried as such.
- ⬛ **Pre-existing generator drift at HEAD** — `canon.css` font-family collapse, RAG snippet colours,
  `_GRAPH-REPORT` totals. It **fails identically before and after this lane**, established by control
  rather than assumed, so it is **attributed, not inherited**. Not from this lane, not fixed by it.
- ⚠ **One record defect, found and corrected at the wrap:** `knowledge/_binds-ratchet.json`'s `$note`
  still read *"Floor is 0 because coverage is 0: no meta carries binds yet"* while its own `floor` key
  read **11** and its own `carrying` list named eleven metas. The number moved; the prose about the
  number did not; nothing chases prose. Corrected in place, with every other key asserted parse-equal.

## Resolved state, and what is still open

**Resolved:** `s141-D1` ruled and enacted end to end, pushed, with two new gates green on the artefact
at HEAD (`_validate_dtcg.py` → `PASS — 0 failure(s), 61 declared deferral(s)`;
`_validate_binds_ratchet.py` → `PASS`, 11/75 vs floor 11).

**Open, and every one of them is Dave's:** the **120 `$doubt` rows** and the ~97 unaddressed visual
props (the authoring wave) · the **intent-map and capability vocabularies**, still unruled from #140 ·
the **`--scale-scale-N` CSS-var exposure** question · **`DEF-COLOR-MISTYPE` ×8** · the **`lineHeight`
D1 stand** · the msgfile gate · the re-priced immortal-lock item · the render-proof debt ×2.

⛔ **The #141 wrap ruled nothing and closed nothing.** Every item above was carried, not decided.
