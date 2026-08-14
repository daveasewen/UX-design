# #175 — the rule that turned on WHAT IS MEASURED, not what it looks like

```
provenance: s175 · 2026-08-14
status: ruled → knowledge/_rulings.json § s175-D1 (entry 155)
```

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #175 · banner: `GOOD-MORNING.md` ★ LATEST #175 ·
ledger: `knowledge/_rulings.json` § `s175-D1` · discharged float:
`_retired/_FLOAT-174-dave-ink-clarification-DISCHARGED-175.md`.*

---

## 1. The question the session opened on, and why it was open

#174 ended with Dave saying two things about colour that did not obviously fit together. First,
asked whether to keep or revert a generator-driven strip of 25 `--status-*` declarations, he said
*"lets keep it nice and simple, all of them use the appropriate dark ink on white and the lightest
ink for dark"*. Then, unprompted, *"no red just black ink and white."*

The #174 wrap did the right thing with that: it **did not enact it**. It wrote
`notes/_FLOAT-174-dave-ink-clarification.md`, put **three readings** to him — narrow (the status
set), wider (all status and RAG colour, which would collide with the two-red law), narrowest
(this component only) — and said openly that the narrowest reading was *attractive precisely
because it made an open problem disappear, which is reason to distrust it, not to prefer it.*

That float is the reason this session was cheap and clean. The alternative — inferring a scope
from two sentences and regenerating on the strength of it — is exactly the #174 finding one level
up.

## 2. What he actually ruled, and why the shape of it is the interesting part

Across four exchanges, on plain-prose read-backs, unobjected:

1. *"Just use the default ink colours (blackest) for all the progress bars, all themes, no red."*
2. *"specifically for progress bars we don't use colours in all four themes. the other ruling was a
   miscommunication. the only type of progress indicator that may use colour is the step tracker
   component"*
3. *"This is two components that are treated separately but the designer can choose to have the
   desktop version, with circles, collapse into bar type as a responsive behavior. so there are
   three patterns. these will have colours in legacy for sure. Its undecided for teh other themes
   as yet."*
4. (shown that Supercharge's blackest ink resolves to `#13110E`, not the Mono literal `#1A1A1A`)
   *"thats the right black for supercharge"*

★ **The rule is SEMANTIC, not visual.** It does not say "bars are black and circles are coloured".
It says a **continuous quantity** is ink and **discrete steps** may carry colour — and quotation 3
is what proves it, because it explicitly contemplates a step tracker that *collapses into a bar
shape* at `@container (max-width:520px)` and keeps its colour. Had the rule been drawn on
appearance, that responsive state would have flipped its own rule mid-viewport.

This is why the token split is `progress/complete` vs a newly minted `step/complete`, and not a
`bar` vs `circle` split. A visual split would have been enactable in the same number of lines and
would have been wrong the first time a designer used the collapse.

## 3. The supersession, and whose word did it

The `progress/complete` `$note` carried a ratified Dave ruling from **2026-07-21**: *"in mono and
console it should be black. the colours in legacy and supercharge are fine."* This session
reverses the legacy/supercharge half of it.

⚠ **It is superseded on HIS word, not on our judgment** — he called the earlier ruling *"a
miscommunication"*. That distinction is inscribed rather than smoothed, because a supersession
that reads as an agent's re-reading of an old ruling is a different and much worse animal than
one the ruler disowned himself. The 2026-07-21 sentence is **preserved verbatim in the token file
and appended to** — add, never trim a ratified record.

## 4. What was NOT ruled, and the one that is easiest to launder

Four things stayed open on purpose:

- **The three UNDECIDED step-colour themes.** Legacy is DEFINITE (*"for sure"*). Mono, Console and
  Supercharge are **FLOATED**. The values they carry today are **inherited, not ruled**, and both
  theme files say so in their `$note` so a later reader cannot mistake residue for a position.
- ★ **The per-theme-ink generalisation.** Dave ratified that `#13110E` is the right black **for
  Supercharge**. That ratifies THE INSTANCE. The general principle — that "blackest ink" resolves
  **per theme through the alias chain** rather than as one literal black — is **implied but not
  ruled**, and is recorded as an open generalisation. It would have been one sentence to write it
  up as ruled; it is not his word yet [[feedback-dont-launder-a-premise-into-a-ruling]].
- **`step/incomplete` does not exist.** The step components still bind `progress/incomplete`. The
  asymmetry is visible in the manifests and was deliberately left alone.
- **The fill-on-track contrast failure.** FIXED for the bar as a side-effect of the ink move
  (Legacy dark 1.75 → 9.15, Supercharge dark 2.38 → 10.46, measured, 3:1 non-text). **STILL FAILING
  on the step components** at exactly the old numbers, because the colour moved with them. The
  float warned that reading 3 would make this problem "disappear"; it did not disappear, it
  narrowed, and it is carried in that narrowed form.

## 5. The #174 class did not recur, and it was fenced deliberately

#174's finding was that **a do-not-rule list names DECISIONS and cannot fence a GENERATOR'S BLAST
RADIUS** — `[50]` and `[45]` rode in as a side-effect of a legitimate regeneration.

The remedy tried this session was to make the brief require **naming which regions of `canon.css`
each generator owns, and attributing every hunk**. Result, verified first-hand by the conductor
rather than taken from the sub's report: **11 insertions / 11 deletions, two regions, zero
unattributed hunks.** No `--status-*` declaration touched. No comment block deleted. The only
comment line in the entire diff is a path-count bump `140 → 141`.

★ That is one datapoint, not a proven gate. The fence was **prose in a brief**, and prose in a
brief is exactly the enforcement tier `_CHAIN.md`'s read-chain comment sits at — see §7.

## 6. The instrument question, and the honest answer

`machinery: 10 instrument / 52 feature`.

The 10 lines are **not a new instrument**. `gen_theme_cascade.py:548` hard-asserted
`supercharge progress/complete == #B92F1E` — an assertion whose **SUBJECT MOVED** and which is
false by construction after this ruling. It was **retargeted** to `step/complete`, plus one clause
asserting the new state, and the clause was **mutation-tested to prove it bites**.

⚠ Writing that clause surfaced a real trap worth naming: `load_themes()` returns **alias-expanded**
overrides, so *"no declared override"* and *"override expanded through the DNA tier"* are
**indistinguishable in that dict**, and nothing at the call site says so. The new clause therefore
asserts the **value** (`progress/complete` tracks `text/default`) rather than the absence of an
override. Absence would have been a green that cannot fail.

⛔ The four-theme contrast checker stays **queued and unbuilt** — building it in the same breath as
the finding is what `s172-D3`'s observed-failure rule forbids.

## 7. What went wrong in this session, stated plainly

⛔ **The conductor opened `GOOD-MORNING.md` at boot — roughly 26K — the exact reflex `_CHAIN.md`'s
own header bans, and the exact overspend #173 declared as its own finding ⑦. Second session
running.** It is why this wrap was delegated: FILL reached 128,839 against a 150,929 stop line,
leaving ~22.1K against a 42–49K conductor wrap.

★ The structural reading is the same one #173 filed: **the read-chain cut is enforced by a COMMENT,
not a gate.** A comment cannot fail. This is the `[107]` shape and the §5 shape — three instances
of the same class in three sessions, and the only one of the three that has bitten twice is the
one whose enforcement tier is prose.

⚠ Also: the **#175 title carried a stale premise** — it announced the `--status-*` strip as
*uncommitted*, when it was committed at `76b024c` and pushed. Title generation inherited a premise
that the wrap it came from had already invalidated [[premise-ages-faster-than-rule]].

## 8. Friction carried, not fixed

`knowledge/_RUNBOOK-gated-component.md` is still 54 lines, still omits the icon gate, the type
ratchet, the radius `MIGRATED_SNIPPETS` step and the registry step — **and its step 6 instructs
running `_build_all.py`, which is banned.** It also omits `gen_showroom.py`: editing a snippet
manifest silently staled four showroom pages this session and only `--check` caught it.

Two new entries join that log: the `load_themes()` alias-expansion ambiguity above, and — worth a
gate one day — **a FILTERED `_validate_state_contrast.py` run rewrites the WHOLE tracked audit as
if the filter were the population.** It was restored byte-identical here, by hand, because someone
remembered.

## 9. Where this leaves things

**Settled:** the bar is ink in all four themes; the step components are unchanged and byte-identical
in all 8 theme×mode cells; the #174 ink float is discharged at its narrowest reading; the two-red
law and the mono error ink camp are untouched.

**Open and Dave's:** the three undecided step themes · the per-theme-ink generalisation · a
`step/incomplete` · whether the new selftest clause needs a Legacy mirror · the fill-on-track
contrast failure on the step components.

**Owed to CI:** the full 76-snippet state-contrast population run, and the composite `_build_all.py`
verdict.
