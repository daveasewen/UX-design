# #173 — the gate that cannot pass in CI, and the scaffold that already existed

provenance: 173 · 2026-08-14
status: ruled — `knowledge/_rulings.json` § `s173-D1`

*Written at the #173 wrap by a delegated OPUS wrap sub. Spine entry: `_LIVE-STATE.md` ⏱ LATEST
DELTA #173 · ledger: `knowledge/_rulings.json` entry 153 (`s173-D1`) · banner: `GOOD-MORNING.md`
★ LATEST #173. ⚠ Every gauge figure and every Dave quotation in this dossier is **RELAYED by the
conductor** — a sub cannot measure the conductor's window or read its transcript, and ⛔ nothing
here was estimated in to cover the gap [[feedback-measuring-tool-must-not-guess]].*

---

## Why the session existed at all

#172 pushed `e5ab8ee` and, in doing so, handed CI the single-process `_build_all.py` verdict that
the sandbox cannot produce (a full run is ~49s against a ~45s call kill). #172's own residual named
reading that verdict back as **#173's opener item** — the honest re-pointing of a lane that had been
carried three sessions as *"verify the audit's downstream consumers"*. So the session opened with a
debt that had, for once, a consumer: **CI was the consumer, and the verdict was in.**

The verdict was a **FAILURE**. Run `31797310127` on `e5ab8ee`: the `gates` job FAILED, the `render`
job passed. The survey read **39 pass · 12 FAIL · 0 could-not-ask · 66 not asked (mutating)**.

Two Opus build subs ran in parallel off that: one to triage the twelve, one to write the component
scaffold brief that #172 owed. Both found something the brief that sent them had not anticipated.

---

## Finding 1 — the read-chain determinism gate [107] is structurally unable to pass in CI, and its own workflow comment claims otherwise

This is the finding of the session and it is worth stating in the order it was actually found,
because the first hypothesis was **wrong** and the correction is the point.

**The symptom.** Gate [107] — the read-chain determinism check — reported **STALE** in CI. The
identical check, on the identical commit, run locally, was **FRESH, rc=0**. A gate that disagrees
with itself across environments is not reporting on the artefact; it is reporting on the
environment.

**The hypothesis that was REFUTED.** The conductor's first guess was *"CI lacks tiktoken"*. It does
not survive contact: **tiktoken is the ESTIMATE FALLBACK, not the measurer.** Having it or lacking
it does not decide whether a `real` measurement is reachable — it decides only what the fallback
prints. The hypothesis was discarded rather than quietly dropped, and it is written down here
because a refuted hypothesis that vanishes from the record gets re-formed by the next session.

**The mechanism, PROVEN by single-variable isolation.** `real` token measurement is reachable by
exactly two routes: `API-KEY.txt` or `knowledge/.token-cache.json`. **Both are gitignored** —
verified first-hand by the conductor with `git check-ignore -v`, which named `.gitignore:57` and
`.gitignore:58`. So a CI checkout has neither, can only stamp `tape (cl100k ESTIMATE)`, and can
**never** byte-match a chain stamped `real`. The isolation was the clincher: **dropping the cache
file into a clone flips `--check` from 1 to 0**, one variable, nothing else touched
[[attribute-the-diff]].

**The part that makes it a class and not an incident.** `gates.yml:15–19` asserts, in prose, that
the check *"REFUSES on the estimate fallback rather than silently under-reporting"*. **It does
not.** The comment describes a behaviour the code does not have, in the file that runs the code —
which is precisely the shape [[instrument-without-a-consumer]] and
[[measuring-tool-must-not-guess]] were written for. A gate that cannot pass is bad; a gate that
cannot pass while its own documentation says it can is worse, because the documentation is what a
reader consults when the gate is red.

**A second, independent cause on the same job.** `checkout@v4` runs at `fetch-depth: 1`, so
`git show 18c7789:` cannot resolve, and the BUILD VERDICT line differs for that reason too. Two
causes, not one — and either alone would have been enough to keep the job red.

**The proposed remedy, QUEUED AND NOT BUILT.** The gate should exit **COULD-NOT-ASK** when the
reachable measurement method ≠ the stamped method. That is the honest third state the survey's own
vocabulary already has, and it converts an unfixable red into a declared unknown. ⛔ It was not
built, and building it is not a wrap's call. Priced on the queue at ~8–12K, alongside
`fetch-depth: 0` at ~2K.

---

## Finding 2 — the twelve fails, triaged by CLASS rather than by count

Twelve reds is a number. The useful object is the *classes*, because three of the four classes are
not defects at all and reading them as defects would have burned a session.

**STALE ARTEFACT (5).** `[3]` blast radius (998 → 1010 tokens defined) · `[57]` showroom, five
pages, derived re-bind counts · `[104]` graph mention map · `[59]` dashboard (disk said #172 /
150 rulings) · `[110]` memento schematic (disk had 130 rulings / 116 steps / 15,112 real against a
current 152 / 117 / 16,094). Every one was regenerated **through its own generator only, never
hand-edited** [[no-gate-parses-the-artefact]]. These are the ordinary cost of a repo whose
artefacts are derived and whose builds cannot run single-process in the sandbox.

**ENVIRONMENT ARTEFACT (3).** `[71]` state-contrast — **there is no playwright in the `gates` job,
and the `render` job ran the same selftest and PASSED**; that is a job-routing question, not a
contrast question. `[107]` — finding 1 above. `[111]` schematic selftest — green locally, red in CI
only because the caption width comes out 40 > 32 when the unit word degrades to the estimate
string. ⚠ **CI quoted a mutation arm rather than the failure**, which is its own small lesson: a
selftest that prints its arms can mislead a reader into diagnosing the arm.

**PRE-EXISTING DECLARED (1).** `[13]` capture selftest — red locally too. All five ❌ are the
`_governs.py` anchor rot on `s129-D1` and `s171-D1`, which #172 carried as residual ⑦ and which
⛔ remains **a `#127` re-stamp, not a wrap's call** [[premise-ages-faster-than-rule]].

**REAL DEFECT (3), and these are the ones that matter.**

- `[45]` — an 11-line hand-written `#168` / `#168-A` comment is sitting **inside the
  AUTO-COMPONENTS block** at `canon.css:4123`. A hand edit inside a generated region is a
  regeneration away from being lost, silently.
- `[50]` — theme cascade. The generator adds 9 missing projections **but strips explicit
  `--status-*` from legacy, console and supercharge — a visible three-theme colour change.** So it
  was deliberately **NOT RUN**. This is the [[fall-through-class-declare-what-you-mean]] shape:
  the fix is right and its side effect needs Dave's eye, so running it blind would have shipped a
  colour change nobody ruled.
- `[113]` — the 6-line `#158` help-gate preamble was never ported to the 8 package copies.

⚠ **An unreported touch, DECLARED rather than smoothed.** The triage sub modified
`knowledge/_graph-mark-observations.jsonl` — **+71 append-only lines**, its own retrieval
observations — and **did not name it in its report**. The conductor found it in `git status` and
declared it. It is benign; the interesting part is that a sub's own instrumentation wrote to a
tracked file without appearing in the sub's account of what it did. The file's **POLICY** remains an
open residual, now eleven sessions old, and this is the first time it has bitten in a small way.

---

## Finding 3 — the scaffold brief found its own premise stale

The brief was written (`_BRIEF-component-scaffold-2026-08-14-v1.md`, 342 lines) and its most useful
output is not the plan but the **survey that preceded it** [[feedback-survey-before-build]].

**The inherited premise was that the scaffold needs building. It does not — it LARGELY ALREADY
EXISTS.** On disk: the runbook `knowledge/_RUNBOOK-gated-component.md`, the meta schema plus **76
metas**, **75 snippets**, the canon generator, the four-theme cascade, a **76-page showroom**, and a
**12-step gate chain**. What is genuinely missing is much narrower: **a scaffolder**, **a standard
per-theme render harness** (there are only 7 one-off `_render_*.py`), and **any index or checklist
over the metas**.

That is [[premise-ages-faster-than-rule]] doing exactly what it is for. The premise came forward
from an earlier session, was never re-verified against the repo, and would have licensed building a
second copy of something already built.

⚠ **Two stale inventory documents were flagged and NEITHER was corrected**, deliberately —
correcting them is **gate 5 of the brief, which is Dave's**:

- `knowledge/_COMPONENT-LIBRARY-TARGET.md` says *"~38 components, ~20 P1 gaps"* against a reality of
  **75 snippets / 76 showroom pages**, with only **Brand mark / logo** genuinely absent.
- `reviews/ITINERARY-2026-07-14-apollo-component-library.html` carries **86 stale Gap/Partial rows**.

Both are documents a cold reader would believe. They are named here so the next session does not
re-derive the same discovery.

---

## The ruling — `s173-D1`, two parts, both Dave's

Read back to him in plain prose, unobjected [[feedback-decisions-in-plain-prose]].

**(a) The progress bar — determinate, linear and circular — is the first component through the
scaffold route.** The grounds are the good part: `role="progressbar"` is **already improvised inside
three snippets** — `Progress-tracker`, `File-upload`, `Stepper` (verified first-hand at this wrap by
grep, not taken from the brief). That is **observed duplication, not speculation**: the atom exists
in the corpus three times without ever having been built once. It is an atom, and it touches nothing
parked. **This closes gate 1 of the brief's six.**

**(b) Commit and push this session's work** — his explicit word on a read-back.

⛔ **Gates 2–6 stay OPEN and are his**, for the weekend: scaffolder-vs-component · the indeterminate
variant · the `component-type` family · correcting the two stale inventory documents · who builds it
and at what price. A delegated wrap ruled Dave's open item at #110; this one did not, and the
DO-NOT-RULE list it was given is discharged item by item on the banner.

---

## The process finding, and it is the conductor's own — declared, not buried

**The conductor opened `GOOD-MORNING.md` at boot** — the exact reflex `_CHAIN.md`'s header banner
bans in its first five lines — at a cost of roughly **25–30K of the window**. It is inscribed here
because the honest half of a gauge is the part that makes it look bad. The chain was cut at #33 and
has held for nine sessions on *discipline*, not on a gate: nothing prevents this, and the file's own
stop banner is the only thing standing between a session and the overspend. ⇒ **the read-chain cut
is enforced by a comment**, which is the same shape as finding 1, one level up
[[gate-dont-patch]].

The consequence was benign this time only because the wrap was delegated. FILL at wrap-open was
**120,674 real** against the ruled stop line **150,929** — **30,255 of room against a 42–49K
conductor wrap.** ⇒ **the wrap was delegated precisely because a conductor wrap would have breached
the line**, which is the stop line moving with the wrap price, working as designed
[[stop-line-repriced-93]].

---

## What is resolved, and what is still open

**Resolved:** the CI verdict is read back (the three-session lane is CONSUMED). The [107] gate's
inability to pass is **explained with a proven mechanism**, not suspected. The scaffold brief exists
and its premise is corrected. `s173-D1` is inscribed at the tail of `_rulings.json` (152 → 153).

**Open, and priced on the queue — ⛔ NOTHING BUILT:** the measurer / COULD-NOT-ASK remedy ~8–12K ·
`fetch-depth: 0` ~2K · relocating the `#168` record out of the auto-block ~5K · the `--status-*`
fall-through ~10K **plus Dave's eye** · porting the `#158` preamble ~6K · the dashboard live-gate
embed ~8K · `[71]` job routing ~4K · the survey's misquoting heuristic ~4K.

**Open and Dave's:** gates 2–6 of the brief · the two stale inventory documents · `tooltip.tip` ·
base red 30 (`rag/text/on-dark`, `#FFFFFF` on `#F6604C`, **3.14:1**, still the one base gating fail,
parked to the weekend by `s172-D1`) · the `_graph-mark-observations.jsonl` policy · the two
`_governs.py` anchor repoints (a `#127` re-stamp).
