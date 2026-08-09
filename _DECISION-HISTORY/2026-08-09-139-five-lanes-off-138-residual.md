# #139 — five lanes off #138's residual: an item unparked, a schema that forbids its own model, and a gate that had never run

provenance: 139 · 2026-08-09
status: observed

*Spine entries: `GOOD-MORNING.md` ★ LATEST #139 · `_LIVE-STATE.md` ⏱ LATEST DELTA #139.
Ledgers/artefacts cited: `knowledge/_TOKEN-FORK-LEDGER.json` · `knowledge/_FORK-BAN-GATE.md` ·
`knowledge/_validate_token_forks.py` · `knowledge/_audit_props_axes.py` ·
`knowledge/_render/verify_dv_gutter_render.py` · `knowledge/canon/dv-behaviour.js`.
Commits: `94a3a46` · `b2fb44f` · `54b080e` · `cc2079a` · `1f786c8`.
Written by the wrap sub from the conductor's measured facts plus first-hand repo reads; every
figure below is the conductor's measurement or a `git` read, none is this sub's estimate.*

## Why this session had no design question in it

#138 closed on a residual list rather than an open ruling. #139 took five of its items and ran
them as lanes — three build subs plus this wrap. The shape matters for reading the record: there
is **no `s139-*` ruling id**, because nothing was put to Dave as a ruling with named alternatives.
What the session produced instead is a **queue of five things that are now ready for him to rule**,
which is a different artefact and is filed as residual ①, not as decisions.

The binding budget was **FILL**, not quota, all session — which is why three build subs were
affordable ([[delegation-cost-inversion-110]]). Dave declined pace talk outright
(*"dont worry about the pace, i need all these fixes done"*), so the quota panel is recorded
**UNPOLLED**, not assumed comfortable.

## ① ds-012(b): what six weeks of parking cost, and what unparked it

ds-012(b) was RULED at **#6** and sat for roughly six weeks. The enactment is a runtime
`gutterPL()` in `knowledge/canon/dv-behaviour.js` computing the plot area **relative to the
gutter**, opt-in via `data-pl-fit`.

The finding worth keeping is not the fix, it is the **shape of the proof**. The claim under test
was "h-bar labels are clipped". A count of clipped labels at one width would have been a count, not
a measurement. What was run instead: **6/6 clipped → 0/6 at 1180, 480 and 320**, in the snippet
*and* the showroom, with the licensed cut confirmed by a **canvas probe carrying a DejaVu control
and a bogus-face control** — #138's lesson (`document.fonts.check()` is worthless; controls are
what discriminate) applied rather than merely cited.

And the gate was **bitten**: `verify_dv_gutter_render.py` reports 48/0, and the conductor
personally replayed the bite — a neutered copy of the fix makes it FAIL. A green that cannot fail
is an assertion; this one was shown to be able to fail.

**What is still open, and it is Dave's:** `PL_MAX_FRAC = 0.42` is a floor nobody has ruled, carried
as **PROVISIONAL-AWAITING-DAVE**. Separately declared and deliberately out of scope: the **JS-off
path still clips**. Naming it here rather than folding it into the success line is the point — it
is the part a later reader would otherwise have to rediscover.

## ② `s135-D4`: the blocker was never the verdicts, it was where they were read

#135 produced 82 verdicts and #135's own application attempt landed **0 of 82** — the generator had
no preservation path for the NEARMISS/PROSE/GOVERNED shapes and the freshness gate refused every
one. The move that unblocked it was reframing the verdicts JSON as a **generator input** rather
than a patch to apply afterwards. Result: **82/82** — MERGE 5 (edges 5→15), PROMOTE 52, ATTACH 25
(`governedBy` 0→25).

Three things make this trustworthy rather than merely green: **four loud refusal arms driven**
(the generator refuses, named, on each malformed shape), **check (f) mutation-tested** (89 red →
green, so the check discriminates), and a **double regen producing zero diff** (idempotent, so the
generator is not smuggling state).

The **15 token-split exceptions were left UNTOUCHED and DECLARED**. There is no tokens machinery in
that generator; inventing one to clear a count would have been the [[gate-narrows-its-own-rule]]
failure in reverse. They stay Dave's.

## ③ The audit that changed the schedule instead of the code

The `s136-D1` props-axes audit was expected to produce a coverage number. It produced a
**precondition**: 280 props across 76 metas, `binds` present **0/76**, `slots` key **0/76** — and
`meta.schema.json` **forbids both keys** (`additionalProperties: false`).

So the slots-key rollout and the DTCG re-encode are not "next"; they are **blocked**, and the thing
that unblocks them is a Dave ruling on the schema amendment. This is why residual ② points at
residual ① rather than standing alone.

Two honest residues in the same audit. **38 rows are unclassifiable because they are text-content**
— which is exactly the text-param refinement Dave FLOATED at #136 and which has never been ruled;
the audit re-derived the gap independently. **2 rows are behaviour, and the three-axis model has no
behaviour axis.** That is a coverage gap in a ruled model. It is **reported, not patched** —
patching a ruled model is not a sub's move.

## ④ The fork-ban gate, and why it re-priced #108

`_validate_token_forks.py` parses `canon.css` **in the consumer's grammar** — it resolves `var()`
down the specificity ladder the way the browser does, rather than grepping declarations. That is
the [[no-gate-parses-the-artefact]] standard, and it is what makes the output a measurement.

It was mutation-tested on **real bytes** (not a fixture) plus a two-direction selftest, and its 42
findings are recorded in `knowledge/_TOKEN-FORK-LEDGER.json` as
**`UNRULED-BASELINE-s139`** — a baseline, explicitly not a sanction.

★ The re-pricing: **#108's "40 colliding token names" is measurably stale — there are 104, with 20
FORK verdicts.** The reason to believe the new number is that the gate **independently reproduced**
#108's two known cases: `--pri-hover` at 48 contexts / 4 values, `--sec-hover` at 18 / 8. A new
instrument that agrees with the old one where the old one was measured, and disagrees where it was
merely counted, is the one worth trusting. [[a-new-tier-silently-bypasses-its-tests]] is the class
this avoids.

## ⑤ The gate that had never run — six sessions of it

`_validate_kg.py` was built at **#133**, documented, selftested, and **never wired into
`_build_all`'s STEPS**. For six sessions it was a gate that could not fail — the literal
[[instrument-without-a-consumer]] shape, and the very class #133 was proud of closing.

It was found because the sub building the *fork* gate asked **"does my gate actually RUN?"** — a
question, not an instrument. Both gates are now wired and `_validate_wiring.py` reports **32/32,
0 orphans**.

The general lesson, and it is the one to carry: *"is it built and green?"* and *"does it run in the
mode I work in?"* are different questions, and only the second one is load-bearing. #137 learned
this about `--selftest`; #139 learned it about a whole gate.

## ⑥ Two recurrences and a new pothole

**The doubled-prefix commit-subject class recurred** — this time on the *non-wrap* arm: the
conductor's msgfile carried the `#139 <date> — ` prefix that `_git_commit.sh` prepends itself.
Caught by the subject-verify step and amended **from a fresh msgfile** (the script mutates the
msgfile on refusal — #134's lesson, applied correctly this time). The class has now bitten in both
arms, which is the [[gate-dont-patch]] trigger: a msgfile whose line 1 matches `^#\d+ \d{4}-`
should be refused. **Not built, not ruled** — carried as residual ③.

**ENOSPC n=5**, `/sessions` at 7.5 M free, the worst reading yet. The browser crashed on launch
until `TMPDIR=/var/tmp` — the profile directory was landing on the full mount. The runbook already
prescribes exactly this, so the **premise held**; recorded as a confirmation rather than a finding.

★ **New, and it earned its runbook line: `git checkout -- <path>` cannot restore files on this
mount** — it fails with *"unable to unlink"*, the same permission shape as the long-known
`index.lock` wart. The working restore is **`git show HEAD:<path> > <path>`**. Enacted by addition
in `knowledge/_RUNBOOK-git-commit.md` § Gotchas.

## ⑦ The drift nobody was looking for

Lane ①'s regen exposed **25 non-chart showroom pages plus the index stale against the theme cascade
at HEAD**. It was **attributed with a control run** rather than assumed to be the lane's own doing
([[attribute-the-diff]]), and then committed **separately** (`b2fb44f`) so the ds-012(b) diff stayed
readable.

The uncomfortable part: nothing detects this. No gate compares a committed showroom page against
the cascade that generates it, so the drift was only visible because an unrelated lane happened to
regenerate. That is an observation, not a proposal — it is not this session's to fix.

## ⑧ One conductor fact this wrap declined to inscribe

The brief described #139 as *"the first Fable conductor session"*. The record disagrees: **#135 and
#136 both ran FABLE conductor**, per their own banner headers now in `_GM-ARCHIVE.md`. The banner
therefore records **FABLE conductor** with no first-ever claim.

This is [[premise-ages-faster-than-rule]] in its cheapest possible form — a claim that cost one
`git`/archive read to check and would have been a confident false inscription forever. The wrap's
job includes not laundering the brief.

## Resolved state, and what is still open

**Landed and evidenced:** ds-012(b) (`94a3a46`) · showroom drift regen (`b2fb44f`) · `s135-D4`
(`54b080e`) · the props-axes audit (`cc2079a`) · two orphan gates wired (`1f786c8`).

**Open, and all of it Dave's:** the `PL_MAX_FRAC=0.42` floor · the column-chart narrow-width
treatment (overlap below ~440, his eye) · the 42 fork verdicts · the 15 token-split exceptions ·
the `meta.schema.json` binds/slots amendment. The slots-rollout and DTCG lanes wait on the last of
those.

**Open, and not Dave's:** the doubled-prefix msgfile gate · the cold-sandbox symlink-farm proof
(carried unchanged from #138 — this sandbox was warm again) · `TMPDIR` fragility in
`_validate_kg.py`'s `check_freshness`, whose default path is one ENOSPC away from a spurious fail ·
the JS-off clipping path.
