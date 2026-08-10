# #143 — the s142-D1 enactment: a ruling that named a colour value the prop doesn't have, and a glyph that fails AA on half its modes

provenance: 143 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA (#143) · `GOOD-MORNING.md` ★ LATEST (#143).
Ledger: `knowledge/_rulings.json` § `s143-D1` (§ `s142-D1` status flipped to ENACTED #143 in the
same pass). Verbatim record: `reviews/BINDS-AUTHORING-VERDICTS-2026-08-10-s142-v3.json` (unchanged,
the source `s142-D1` enacts from). Both-way links per `_DECISION-HISTORY/README.md`.*

---

## Why this session existed

#142 closed with one ruling and two things still to do: enact `s142-D1` (113 of 114 rows, 12 class
verdicts, into the metas) and migrate the colour spine to DTCG. #143 was conductor + one build sub +
this wrap sub, Dave live, and ran as one arc: the enactment lane, residual ① of #142.

## The enactment landed, and the conductor re-drove the gates rather than quoting them

30 bind rows across 24 metas plus 83 annotation rows — 113 of the 114 ruled rows — landed across 54
component metas plus `knowledge/_binds-ratchet.json`. Ratchet coverage moved 11 → 33 of 75; the floor
was rebased 11 → 33, refuse-to-lower guard intact. `tooltip.tip` — the one row `s142-D1` left
unruled — was verified byte-identical to HEAD via `git show`, untouched.

The conductor re-ran the three gates on the artefact rather than trusting the build sub's own report:
`_validate_binds_ratchet.py` → PASS, 33 of 75, rc=0; `_validate_dtcg.py` → `PASS — 0 failure(s), 61
declared deferral(s)`, rc=0; `_validate_standing_instructions.py` → PASS, 28 standing docs reachable,
rc=0.

## The diff forensics: a net-negative line count, attributed rather than assumed

`git diff --stat` read 140 insertions against 162 deletions on a change that should mostly *add*
binds. Rather than accept that as ambient noise, the conductor ran a keypath-set comparison against
HEAD across every changed meta (excluding `$status`, which is expected to change) and found **zero
lost keypaths**. The cause: `$note` and `$status` reflowed onto shared lines during the textual
insertion, which reads as deletions-plus-insertions in a line-oriented diff even though no content
was lost. This is recorded as a residual — the hand-formatted metas are now cosmetically
inconsistent — not a defect.

## The premise correction: half of #142's residual ① could not exist

#142's residual named "the DTCG-deferral updates" as part of this enactment's scope. The build sub
checked rather than assumed: `_validate_dtcg.py`'s corpus is `knowledge/tokens/*.json`, which is
**disjoint** from `knowledge/components/*.meta.json`. A metas-only enactment cannot move a deferral
count that lives entirely in a different file family — and it didn't: 61 declared deferrals, before
and after. This is recorded as a corrected premise in #142's own residual wording, not as work left
undone.

## The finding: the ruling's subject didn't match the artefact's subject

`amount-display.sign`'s enum is `["none", "negative"]` — there is no `"positive"` value. The `s142-D1`
class-C4 address read *"rag.success | rag.error (positive / negative)"*, describing an enum the prop
does not have. The build sub re-keyed `positive` → `none` to make the bind land, which means the
**default, no-sign-shown state is bound to `rag.success`** — a colour claim resting on a value that
was never in the artefact Dave was shown. The ratchet gate is green and structurally cannot see this:
it checks that a bind exists, not that the address it was ruled from matches the prop's real shape.
This was surfaced to Dave with a live three-treatment specimen — as-enacted, half-bind, monochrome —
built on real token values, on both Apollo surfaces, rather than described in prose.

## Dave's ruling: `s143-D1`, two verdicts

**(A) `size` is two axes, additive — keep both.** A size enum can legitimately drive icon scale
*and* type scale at once; they are not competing mechanisms. T-D15 (2026-07-24,
`segmented-control.size`'s typography mini-ramp) **stands, not superseded** — C2's icon-ramp binds
sit alongside it. The four `$status` tension flags the build sub had written on
`segmented-control.size`, `amount-display.size`, `amount-input.size` and `stat-card.size` are
downgraded from TENSION to CROSS-REFERENCE in this wrap: they were never conflicts, they were two
true things about one prop.

**(B) `amount-display.sign` — Treatment A, keep exactly as enacted, both legs bound.** Dave's words,
verbatim: *"rule A but these colours will have to adjusted for Ally"* — Ally being accessibility. The
bind stands as the build sub wrote it (including the `positive` → `none` re-key). What doesn't close
yet is the colour VALUE: it carries an accessibility adjustment as an open item, not a resolved one.

## The a11y finding Dave's ruling then exposed: family-level, not component-level

Measuring WCAG contrast of the rag glyph rungs used as numeral text surfaced something the C4 bind
alone would not have: **all four rag glyph rungs fail AA on white** and three of four also fail on
dark ink, because `semantic-colour.json` gives each rung one hex value for both `.light` and `.dark`.

| value | on #FFFFFF | on #1A1A1A |
|---|---|---|
| `rag.success-glyph` #66CC8D | 1.98 FAIL | 8.77 AA |
| `rag.error-glyph` #F6604C | 3.14 FAIL | 5.55 AA |
| `rag.warning-glyph` #E0A61F | 2.18 FAIL | 7.99 AA |
| `rag.information-glyph` #78A7E8 | 2.47 FAIL | 7.04 AA |
| mono red #B92F1E (ruled) | 6.02 AA | 2.89 FAIL |

No single hex value can pass AA on both a white and a near-black page background — this is a
structural gap in the token, not a value someone picked badly. It surfaced now rather than earlier
because `s134-D4` had already nailed rag as *tint + ink* — a glyph living on its own tinted chip,
never a numeral standing directly on the page — and `s142-D1`'s C4 bind is the first consumer to take
a rag rung outside that pattern. A second, related gap sits under it: the C4 address names the
*family* (`rag.success` / `rag.error`), but the family only resolves to `-background` and `-glyph`
rungs — there is no bare `rag.success` value. The rung itself is unspecified in the ruling.

## Process notes, declared rather than smoothed

The conductor opened on `GOOD-MORNING.md` directly instead of `_CHAIN.md` — the read-chain contract's
own file names this exact overspend in its stop header, and it is the same class as a prior #41
finding. Cost: roughly 25K of the session's job room, which is the measured reason the colour-spine
migration lane never opened this session. Separately, ENOSPC held at n=9 (`/sessions` at 0 bytes
free); `pip install tiktoken --break-system-packages` now fails outright rather than being rescued by
`TMPDIR=/var/tmp` — the failure is the install call itself, not the temp directory. What worked:
`/var/tmp/py-s142`, a site-dir left over from the previous session, gave a working gauge with no
install at all. Three runbooks still instruct the install-first path; the corrected remedy — reuse the
prior session's site-dir — is proposed to #144, not enacted here.

## What is deliberately still open

The rag glyph a11y values and the unspecified rung (Dave's — the values, not the finding, are his to
rule) · the colour-spine DTCG migration (now blocked behind the a11y question as well as originally
waiting on it) · `tooltip.tip` · the intent-map and capability vocabularies · the 42 fork verdicts ·
the 15 token-split exceptions · the msgfile-mutation gate (class ×4, still unbuilt) · the ENOSPC
runbook corrections (proposed, not enacted) · the meta reflow's cosmetic residual (54 files, `$note`/
`$status` sharing lines).

---

Resolved state: `s142-D1` RULED AND ENACTED. `s143-D1` RULED — (A) fully enacted this wrap (the four
flag downgrades), (B) part-enacted (the bind already stood from `s142-D1`; the colour-value
adjustment is not enacted here). The next hop is Dave's: the rag a11y values, the unspecified rung,
and only then the colour-spine migration.
