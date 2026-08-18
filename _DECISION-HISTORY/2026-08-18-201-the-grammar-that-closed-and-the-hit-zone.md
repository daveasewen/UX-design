# #201 — the grammar that closed, and the hit zone

provenance: 201 · 2026-08-18
status: ruled — `knowledge/_rulings.json` (`s201-D1` … `s201-D5`)

*The WHY and HOW of session #201. The WHAT lives in the ledger (`knowledge/_rulings.json`), the
★ LATEST banner of `GOOD-MORNING.md`, and the ⏱ LATEST delta of `_LIVE-STATE.md`. Both-way links:
spine entry = `_LIVE-STATE.md` ⏱ LATEST DELTA #201 · ledger = the five `s201-*` records ·
predecessor dossier = `_DECISION-HISTORY/2026-08-18-200-mint-time-derivation-and-the-console-narrowing.md`.*

---

## Finding 1 — the debt #200 created knowingly was closed by a SWAP, not an ADD

#200 minted a dimension-first `s` scale beside the padding-first `small`/`medium`/`large` set and
wrote the consequence down honestly: console then carried **two segmented grammars at once**, four
thumbs across two systems, arbitration unwritten. It was the first thing this session's consumer
would trip on, and it was named as such on the banner.

The repair was not "add the missing `xs`/`m`/`l` and tidy later". Dave tuned the three remaining
scales on tuner v3, pasted the export, and the enactment **retired the padding-first keys off disk
in the same motion as it minted the dimension-first ones** — `s201-D1`. The reason this shape was
chosen rather than a two-step migration is the one the repo has paid for before: a sequenced
rename or a sequenced retire leaves a window in which a glob consumer reads a mixed set and cannot
tell which half is live. #199's alias re-point was moved in one act for exactly the same reason.
A migration that is a SWAP has no window; a migration that is an ADD is nothing but window.

Values, for the record: **xs 24/2/6 → thumb 4 · m 44/4/10 → thumb 6 · l 48/4/12 → thumb 8**,
console only, all steps on the 2px/4px grid `s200-D1` fixed.

Dave also floated, in the same beat, *"a proposal for 5 dimensions in the future"*. It is recorded
as floated and nothing was named — the standing discipline is that an instinct spoken aloud is not
a ruling, and re-putting it later as an option would launder it into one.

## Finding 2 — 44 was ambiguous, and the ambiguity was in the noun, not the number

`s200-D4` minted `size/segmented-control/min-hit-area: 44` as a read-back of Dave's words, with
the veto window left open. The open question was never the value. It was **what 44 measures**: the
visual height of the control, or the area a finger can hit.

`s201-D2` settles it as the **hit zone** — the interactive target. That immediately raises a second
question the first answer cannot dodge: what happens when the visual height is already larger?
`s201-D3` answers it — **hit box = `max(44, visual height)`**, natural above the floor, so `l` keeps
its 48 rather than being clamped down to the minimum. The floor raises; it never lowers.

Both rulings are geometry that the specimen renders, which is why they were ruled off the specimen
rather than off a table.

## Finding 3 — the eye-read caught what 8/8 green asserts did not

One Opus sub built `reviews/SEGMENTED-SCALE-SPECIMEN-2026-08-18-v1.html`: four scales live, light
and dark on the real console palettes, eight computed-style assertions, a hit-zone overlay that is
**driven** rather than described, checked at 1240 and 480.

The asserts came back 8/8. A visual read then caught a **stacking defect** — and the asserts were
green across it, because they measured the values they were written to measure and the defect was
not one of them. It was fixed and re-verified.

This is the session's cheapest lesson and it is not new: a green test cannot see the scope it was
not given. It is also the argument for the specimen existing at all. Dave's verdict was
*"this is great"*, which consumes #200's residual ④ — the `s200-D4` tokens were unproven in render
and are now proven — **for console, and only for console**. Mono, legacy and supercharge have
nothing minted, so "proven in render" remains a claim about one theme.

## Finding 4 — two rules that needed no build

`s201-D4` promoted the card padding formula `max(radius, 8)` snap-2 from **PROPOSED** (where
`s200-D1` left it) to **RATIFIED**. It stays mint-time; nothing derives at render.

`s201-D5` settled the square-theme floor: **`max(container − padding, 0)`, squares stay square**.
The raw derivation goes negative for mono / legacy / supercharge, which is what left #200's
residual ⑦ open. The ruling is deliberately **RULE ONLY** — it tells the generator what to do
without telling it to run, and nothing was minted for those three themes. When they mint is Dave's.

## Finding 5 — the mint-time pitfall #200 predicted arrived one session later

#200's own consequences list carried pitfall (e): *"a mint-time derivation is only as good as its
re-mint."* At this wrap, running the instrument rather than trusting the brief:

```
python3 knowledge/gen_radius_derive.py --check   →   rc=1, 18 drifts
```

`knowledge/_derive-radius-proposal.json` still carries the **retired** `segmented-thumb/small|
medium|large` (18/16/14) and knows nothing of `xs`/`m`/`l` (4/6/8). `s201-D1` moved the token store
and the generator's own proposal did not move with it.

Two things follow, and only the first is settled. The first: the theme's actual contract is green —
`_validate_radius.py` is rc=0 with 0 strict fails, as are `_dtcg_units.py`,
`_validate_token_tiers.py`, `_validate_token_forks.py`, `_validate_palette_tier.py` and
`_validate_theme_provenance.py`, all re-run at this wrap rather than copied from a brief. The
second, unsettled: the next re-mint either repairs the sidecar or **overwrites `s201-D1`'s tuned
values with recomputed ones**, and which of those it does is unmeasured. The wrap declared it and
did not repair it — a re-mint is an enactment, and a wrap rules nothing.

## Finding 6 — the 44 gate is priced, and a price is not a fence

`knowledge/_DS-IMPROVEMENTS.md` gained a queued build candidate at #201: parse rendered specimens
in the consumer's grammar and assert that any element in the segmented-control role with visual
height < 44 presents an interactive box ≥ 44px computed, shipping with a mutation proof (remove the
`::after`, the gate goes RED). The specimen's own geometry is named as the reference.

It is **priced, not built**. Until it runs, a 36px target still ships clean, and the token remains
a number in a file that nothing reads.

---

## Resolved state

Console's segmented grammar is single and dimension-first. 44 is a hit zone with a `max()` rule
above it. The card formula is ratified. The square-theme floor is ruled without being minted. The
specimen is approved by eye.

## Still open

The derive-proposal sidecar is stale against the store it generates · the specimen's asserts have
no consumer · `s201-D5` is unminted for three themes · the 5-dimension proposal is floated ·
the 44 gate is queued, not built · the baked artefacts remain stale, with CI's complete
`_build_all.py` pass at this session's push **expected** to clear them — expected, not done, and
the read-back is owed.
