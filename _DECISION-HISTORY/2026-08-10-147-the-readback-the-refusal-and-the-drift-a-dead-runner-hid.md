# #147 — the readback, the refusal, and the 245-value drift a dead runner hid

provenance: #147 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #147 · ledger: `knowledge/_rulings.json` §§ `s147-D1`,
`s147-D2` · banner: `GOOD-MORNING.md` ★ LATEST #147. This dossier holds the WHY and HOW; the terse
records hold the WHAT. Authored by the delegated OPUS wrap sub from the conductor's relayed record —
every figure below is one the conductor verified in-window; this sub ruled nothing.*

## The arc

#146 closed with two things owed and one thing unknown. Owed: a readback on whether Dave's *"do it
please"* had ratified the ONE-GATE **design** or merely the build, and a decision on the two
generator-code sites #146 surveyed but deliberately did not smooth. Unknown, though nobody knew it
yet: whether anything in the corpus had drifted while `_build_all.py` sat dead from #139 to #146.

The session answered all three, in that order, and the third answer was the expensive one.

## Finding 1 — the readback closed, and it closed on the artefact's own words

The readback was the #146 carry's item ①, one session old. What made it cheap was **not** re-deriving
the argument from memory: the analysis was grounded in `knowledge/_validate_binds_resolve.py`'s own
docstring — one class, one seam, one gate; `STORES` maps a single home per address; `resolve()` is
imported from `gen_snippet_tokens` rather than re-implemented. Dave: *"it seemed like the right
choice."*

The lesson worth keeping is procedural, not architectural. A readback that quotes the artefact is a
readback Dave can rule on in one exchange; a readback that paraphrases the agent's recollection asks
him to audit the agent instead of the design. The [[clarify-reflect-back]] discipline works when the
reflection has a source.

## Finding 2 — one condition, two severities: `s147-D1`

`gen_snippet_tokens.py`'s `project_canon` writer path carried `except KeyError: continue`. The very
same condition, on the checker path, was LOUD. That asymmetry is #146's surveyed site 3, and it is
the shape #146 named: *a correspondence between two artefacts held by nothing, with silent
fall-through on a non-match.*

The fix is small — collect `"UNRESOLVED — write refused"` and refuse the write. What makes it a
finding rather than a patch is the **drive**: a forced `KeyError` turned it RED, and `canon/canon.css`
came back byte-identical afterwards, so the refusal is real and the happy path is untouched.

⚠ The honest limit, recorded at the ruling: **0 unresolved vars exist in today's corpus**, so there is
no behaviour change until it bites. A green here cannot see scope
[[green-tests-cannot-see-scope]] — the drive proves the clause, and the clause is what was ruled.

## Finding 3 — `s147-D2`, and where it was homed

Check D — every manifest snippet must match ≥1 `.cn-<slug>{` block in `canon/canon.css` — went into
the **existing** gate rather than a new file, which is finding 1's ratified design being spent rather
than merely agreed. **75/75 absolute, no allowlist.** Selftest 5→6 bites; the real-corpus mutation
drive renamed `.cn-accordion`, got RED, and restored `cmp`-verified.

`knowledge/_rulings.json` went 106→108 by **textual insertion**, with the priors asserted parse-equal
— [[serializer-defaults-reformat-the-file]], applied without having to be re-learned.

## Finding 4 — the 245-value drift, and why nobody saw it for eight sessions

`gen_snippet_tokens --check` came back RED. The first move was **not** to fix it: a control run at
HEAD proved the drift **pre-existing** [[attribute-the-diff]]. That single control is what turned a
suspected self-inflicted regression into an attributable finding.

All 245 values are the RAG family. The snippets were last projected at **#98**; the tranches are dated
**2026-07-21**. Both pre-date the `s122-D2` mono RAG re-base — `#F6604C` mode-invariant and its
siblings, Dave's by-eye ruling, signed off *"mega"* at #123. So the ruling landed, and the projection
that would have carried it into the artefacts never ran.

**Why it never ran is the part to keep.** The `--check` lives inside `_build_all.py`, and
`_build_all.py` was dead at `check_routes()` from #139 to #146. This is
[[instrument-without-a-consumer]] — **second occurrence** — and the corroborating detail is almost
too neat: the tranches' own last commit message reads *"silent drift, now gated"*. The gate existed.
The runner that runs the gate did not.

Dave ruled **"proceed"**: 245 values + 1 canon literal projected. Receipts, all re-driven in-window —
`gen_snippet_tokens --check` OK · `canon/gen_theme_cascade.py --check` OK (201/206) · binds gate
75/75 · 956 · 102 · 0 fails.

★ The generalisable form: **a repaired runner does not report the damage done while it was dead.**
Repairing `_build_all.py` at #146 was correct and insufficient; the first full drive after the repair
is where the eight sessions of accumulated drift becomes visible. That is why #148's top residual is
the full end-to-end drive, and why it moved to the top rather than staying a tidy-up.

## The correction — msgfile class, instance 6, in this session

Commit `f853a91` went in with a **doubled** `after #147 —` subject prefix. The mechanism, traced:
the first invocation **mutated the original msgfile in place**; the retries were `cp`'d **from that
mutated file**; T3 prepended its generated prefix again. The script's own subject check passed,
because that check is derived from its own write — self-confirming, the exact shape #146's premise
analysis had already isolated as a *different* shape needing an independent reference.

Amended clean to `2ed0425` while unpushed (ahead-1 verified first, per the runbook's amend gotcha).

Two things banked, neither of them a rule anyone had written down:

1. **A `cp` of a mutated msgfile is not a fresh msgfile.** "Fresh" has to mean *generated from
   scratch by `printf`*, not *copied from something that was fresh an hour ago*.
2. Since #128, `_git_commit.sh` **refuses** without explicit paths or `--all-dirty`, and its refusal
   prints only the dirty list — which reads like a staging or lock failure rather than a missing
   argument. The runbook's own warning applies: *read this file when the script surprises you*.

⚠ The gate for this class is **still unbuilt, at six instances**. The priority note is bumped in the
residual; whether it gets built is Dave's.

## The gauge — a miss, written as a miss

boot **55,951** real, inside the 54,859±1,178 band — a datapoint, never corrected into the constant.

⛔ **No check-in ran inside the projection lane or the compaction lane**, and the wrap opened at FILL
**182,509** against a stop line of **150,929** — roughly 31.6K past it.
[[checkin-at-the-ends-cannot-catch-the-lane]] recurred, in a session that had the memory hook loaded.
The wrap fits inside the hard 256K with margin, so nothing was lost; the finding is that the lane
structure, not the budget, is what failed. A declared gap passes and a silent one fails — this one is
declared, here and on the banner.

## Resolved state, and what is still open

**Resolved:** the `s146-D1` scope readback · `s147-D1` · `s147-D2` · the 245-value RAG projection ·
the quota poll (session 10% · weekly 46% · Fable 58%) · the owed `MEMORY.md` compaction pass
(19.6→17.1KB, 5 entries archived, hooks preserved verbatim, nothing deleted).

**Still open, and carried:** the full `_build_all.py` end-to-end drive (now top) · the `_validate_kg`
`check_freshness` tempfile question · `success-ink`'s binding site · the dark selected-row token ·
`#1A1A1A` on dark RAG tints · `tooltip.tip` and the vocabularies · **the msgfile gate, ×6** ·
render-proof debt ×2 · the #139 queue (including the 42 fork verdicts and the 15 token-split
exceptions) · the memory-index remainder · step-0 confirm-retire · the ENOSPC runbook correction ·
the meta reflow · the 8 `DEF-COLOR-MISTYPE` deferrals.

⚠ Every item above is recorded, not ruled. This wrap ruled nothing.
