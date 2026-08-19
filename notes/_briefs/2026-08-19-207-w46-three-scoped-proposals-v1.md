# W-46 — three scoped proposals, returning to Dave (#207, 2026-08-19)

> **STATUS: NOTHING HERE IS A RULING. Every item below is PROPOSED.**
> Scope-only lane under `s204-D1` § SCOPE AND PLAN ONLY, brief
> `notes/_briefs/2026-08-19-207-w46-scope-pm-brief.md` (store row `W-52`).
> Store row for THIS document: `W-53`. Claim table: `notes/_claims/207-w46-claims.jsonl`.
> No code was built, no generator written, no gate wired. Measurement commands were run and
> discarded; nothing reusable was left in the tree.

**How to read this.** Three proposals, one per mechanisation item. Each one says what the thing
is in plain words, who consumes it the day it is born, what it would cost, what has gone wrong
before that it could repeat, and what comes back to you as a decision. Decisions are written in
plain words. Where a scoping question turns out to be **already settled by a ruling**, it is
marked ✅ SETTLED with the ruling quoted, and it is *not* offered to you as a choice.

---

## 0 · What was actually run (run-before-cite)

Every search cited below was executed in this lane. Summary of the probes and their output:

| probe | result |
|---|---|
| `python3 -c "import json; d=json.load(open('knowledge/_rulings.json'))['rulings']; print(len(d))"` | **204 rulings** in the store |
| rulings scan, terms `notes/_claims` / `_claims/` | **0 hits — NO RULING** on the claims directory |
| rulings scan, terms `gen_brief` / `brief generation` / `mints PM brief` | **1 hit** — `s204-D1` only (the programme itself) |
| rulings scan, terms `could-not-ask` / `exit 77` / `third verdict` | **1 hit** — `s193-D1` |
| rulings scan, terms `ships ADVISORY` / `promotion trigger` | **1 hit** — `s114-D2` |
| rulings scan, terms `REVIEW-SIGNOFF` | **6 hits**, all component-colour rulings citing it as a sign-off receipt — none governing it as a decision sink |
| `python3 knowledge/_memento_search.py "controller deck never writes paste ruling message conductor enacts"` | ran; returns lane/GM/LS/ledger/runbook groups, no ruling — the rulings-store scan above is the decisive probe per [[retrieval-default-hides-the-ruling]] (store > chain) |
| `python3 knowledge/_memento_search.py "brief generator mint open items fences"` | ran; same shape, no ruling |
| `python3 knowledge/_probe_registry/_registry.py --list` | 5 probes, sessions P-1 [204] · P-2 [204,206] · P-3 [184,204] · P-4 [203,204,206] · P-5 [173,203,206] |

---

# PROPOSAL 1 — The decision-capture controller (programme item 3)

## What it is, in plain words

One web page, generated fresh each time. One card per decision that is waiting on you. Each card
says the choice in ordinary English, shows the evidence, shows the store search that failed to
settle it, and puts the options on buttons. You tap. At the bottom, a block of text you copy and
paste back into chat. **That paste is the decision.** The page itself never writes anything into
the repo, and the conductor is the only thing that inscribes.

## Consumer named at birth

The **session conductor at the review seam** — the moment in every wrap where open items are put
to you. The first real consumer already exists and is nameable: this very document (three
proposals) plus `W-51`'s promotion question. If the first deck is not driven on those, the build
does not start.

## Scoping answers

### (a) Where the picks land — ✅ MOSTLY SETTLED, and the question as posed carries a false premise

The programme brief asks "new jsonl vs `_REVIEW-SIGNOFF.md`". Neither, at the page's end: a
`file://` review page has no write path into the repo at all. The convention is already ruled and
already built:

> `knowledge/gen_gardener_controller.py` (built under `s179-D1`(4)):
> "★ **THE DECK NEVER WRITES ANYTHING.** It is not a fifth register (P3). It compiles a MESSAGE
> that Dave pastes to the conductor; the CONDUCTOR enacts. There is no fetch, no storage, no
> write-back — the queue data is EMBEDDED at generation time."

> `reviews/REVIEW-170-links-ratification-controller-v1.html:45`:
> "Nothing here writes anything. Pick per line, hit **Export ruling**, paste the text back in
> chat — that message is the ruling; only then does anything land in the store."

**PROPOSED, and it is the only genuinely open half:** what the *conductor* does with the paste.
Recommendation — the conductor writes `notes/_decisions/<n>-picks.jsonl` (directory does not
exist today; `ls -d notes/_decisions` → no such directory), and `_inscribe_ruling.py` stays the
only writer of `knowledge/_rulings.json`.

**Why not `_REVIEW-SIGNOFF.md`:** that file is the component interaction sign-off tracker, a
**dated period record** — ADR-0017 exempts and protects period records, and putting live decision
facts into one is precisely the write-once violation the ADR exists to stop.

**Legality check, probeable:** a picks jsonl is *not* in `_governs.ROLLING_FILES`
(`GOOD-MORNING.md`, `notes/_GAUGE-LOG.md`, `_LIVE-STATE.md` — `knowledge/_governs.py:196-200`),
so `path` and `anchor` evidence pointers into it are legal on arrival under `_inscribe_ruling.py`
R6 / `s177-D1`. A picks file inside a rolling artefact would have been invalid on arrival.

### (b) How a pick's firmness is read back — PROPOSED

Three mechanisms, all on the generator, none on the human:

1. **Every card declares its option set's completeness.** A card renders
   `options: 3 shown · set declared COMPLETE` or `options: 3 shown · set declared PARTIAL`. The
   generator **refuses to emit** a card whose input omits the declaration. An options array is
   itself an assertion that those are the options — this is [[feedback-dont-launder-a-premise-into-a-ruling]]
   and it is exactly what the #207 addendum §2 caught in the promotion line.
2. **Every card carries a free-text escape** — "none of these / say it in words" — always, not
   only when the author expects it. [[honest-refusal-needs-a-legal-form]]: if the surface has no
   legal way to say "wrong question", the answer comes back as a wrong pick.
3. **The export block prints the firmness the page can honestly claim**, per pick:
   `PICKED FROM A DECLARED-COMPLETE SET` or
   `PICKED FROM A PARTIAL SET — reads as a preference, not a ruling`. **The controller may never
   emit the word RULED.** Firmness is established by the conductor's plain-prose read-back in
   chat, per [[feedback-clarify-reflect-back]] and [[feedback-readback-sensation-not-mechanism]].

### (c) Live-controller conventions — ✅ SETTLED by precedent, copy them, do not re-derive

Taken from the built artefacts, not invented ([[specimen-starts-from-reference]] — #202's three
hand-rolled pages produced three invented defects):

- one self-contained HTML file, data embedded at generation time, no fetch and no storage;
- **binds no canon tokens and uses no red at all** — a throwaway review surface must not entangle
  with the two-red law `s151-D1` or the green mirror `s155-D1`;
- **provenance stamped visibly on the page**: source path, its mtime, its size, the pass id and
  the item count — "a deck rendered from a stale queue lies with confidence";
- the generator **fails loud, nonzero rc, no deck written** on a missing/unreadable/wrong-schema
  input — never a plausible-looking empty deck;
- light + dark via `prefers-color-scheme`;
- live contrast + export, per your standing preference [[feedback-live-controller]].

### (d) The #207 addendum made mechanical — PROPOSED, and this is the part that answers your critique

Your critique was that "P-2, P-4, P-5" is not a surface you can rule on. Proposed fix at the
generator, not in prose: **the deck refuses to render a card whose title matches a bare-ID shape**
(`^P-\d`, `^s\d+-D\d`, `^W-\d`, `^ds-\d`, `^ADR-\d`) unless a `plain_words` field is present and
non-empty; the ID may then appear only as a small trailing receipt. A rule about plain words that
lives in a brief gets forgotten; a refusal in the generator cannot ([[gate-dont-patch]],
[[translate-prose-into-machinery]]).

## Price

- **Build: ~1 Opus lane.** The generator is a copy-and-adapt of `gen_gardener_controller.py`, not
  a fresh draw: reuse its embed-at-generation, provenance stamp, fail-loud and plain-styling legs.
  Estimated 400–600 lines including a selftest that plants a bare-ID card and a
  missing-completeness card and proves both directions (fires / silent).
- **Ongoing:** one regeneration per wave (seconds); one deck file + one picks file per wave; one
  store row per artefact at creation (`_gate_doc_rows.py` is blocking).
- **Hidden ongoing cost, stated:** every card has to be *authored* — evidence, plain words, a run
  store search, a completeness declaration. That authoring is the real cost and it lands on the
  conductor, not on the machine. Proposal 2 (`gen_brief.py`) is what makes that cheap; the two
  items are cheaper together than apart.

## Consequences and pitfalls (REPLAYED from this project's history)

- ⛔ **The one existing decision deck was built and never driven again — MEASURED.**
  `_GARDENER-REVIEW.html` last moved at commit `fc5a096` (#179, 2026-08-15); `git log --oneline
  fc5a096..HEAD | wc -l` → **89 commits since**, with no regeneration. Its queue
  (`notes/_dream/_GARDENER-QUEUE.json`) has an mtime of Aug 15. This is
  [[instrument-without-a-consumer]] in the exact shape item 3 would repeat. **Mitigation
  proposed: the build does not start until the first deck's card list exists** — and it does,
  today, in this document.
- ⛔ **#170 / addendum §1 — ID-code decision surfaces.** Mitigated by (d)'s refusal.
- ⛔ **[[feedback-dont-launder-a-premise-into-a-ruling]] / addendum §2** — options presented as
  free when one of them is pre-answered. Mitigated by (a)'s ✅ SETTLED marking discipline and by
  (b)'s completeness declaration, but the discipline is the author's; no machine can detect that
  an option was already ruled unless the card carries its run store search (`s202-D3` makes that
  mandatory, so make the search field REQUIRED on every card).
- ⛔ **[[forgotten-document-class]] #185** — deck and picks file each get a store row at creation.
- ⛔ **ADR-0017 write-once** — any human-readable markdown of the picks is generated FROM the
  jsonl, never hand-kept beside it. Same clause `s204-D1` put on item 1's join.
- ⛔ **The fifth-register risk**, named by the gardener generator itself: a picks jsonl that
  starts carrying state becomes a register nobody ruled into existence. Proposed fence: the picks
  file is **append-only and terminal** — it records what you picked and when; it never carries
  status, and nothing reads it except `_inscribe_ruling.py`'s human operator.

## Open questions returning to you — Proposal 1

**Q1.1 — Does the deck stay strictly paste-only, or should the conductor be authorised to write a
picks file from the paste without a further word from you?**
Run search: rulings scan for `notes/_claims` / `_claims/` → **0 hits, no ruling**; scan for
`controller` / `paste` → 25 hits, all colour rulings ruled *off* controllers, none governing where
picks land. `python3 knowledge/_memento_search.py "controller deck never writes paste ruling
message conductor enacts"` → ran, no ruling surfaced. **OPEN, YOURS.** Related but distinct from
the DO-NOT-RULE item "whether `notes/_claims/` earns a store row", which stays untouched here.

**Q1.2 — Build it, or park it behind Proposal 2?** They compound: the deck is only cheap to feed
if briefs are minted. Priced above; the recommendation is Proposal 2 first, deck second, but the
order is yours.

---

# PROPOSAL 2 — Mint-time brief generation, `gen_brief.py` (programme item 4)

## What it is, in plain words

A script that writes the first draft of a PM brief by *reading the live store*, instead of a
person remembering what is open. It fills in the open items, the do-not-rule list, the fences, and
a premise table where every row has just been re-measured by running the probe — so a brief can no
longer ship a fact that was true last week.

## Consumer named at birth

**The conductor at the brief-writing seat.** That seat is the named failure point in a ruling:

> `s202-D3`: "…five builds argued about a component that does not exist because **the store was
> never asked at the brief-writing seat**. The existing store-before-open discipline failed there,
> not at retrieval — so the proof of search now travels WITH the question."

`gen_brief.py` is that ruling made mechanical rather than remembered.

## Scoping answers

### (a) Brief schema — PROPOSED: seven regions, each marked as machine-owned or human-owned

| region | owner | source |
|---|---|---|
| TITLE + GOVERNANCE | machine | ruling id, programme brief path, store row |
| THE JOB | **human** | the conductor writes it; the generator never invents scope |
| PREMISE TABLE | machine | probes run at mint time, each row = command · rc · timestamp |
| OPEN ITEMS | machine | `knowledge/_state.json` |
| DO-NOT-RULE | machine + human append | see (b) |
| FENCES + ENVIRONMENT | machine | runbook extraction |
| RETURN CONTRACT | **human** | what the sub owes back |

Machine regions are delimited by begin/end markers. Human regions are never touched on re-mint.

### (b) ⛔ A MEASURED FINDING that changes item 4's own specification

The programme brief says DO-NOT-RULE is "pulled from rulings tagged Dave's". **That filter selects
everything and is therefore not a filter.** Measured:

```
python3 -c "import json,collections; d=json.load(open('knowledge/_rulings.json'))['rulings']; print(collections.Counter(r.get('by') for r in d))"
→ Counter({'Dave': 204})
```

**204 of 204 rulings carry `by: Dave`.** Proposed replacement source, all three measured:

- `knowledge/_state.json` items with `state=open` **and** `owner=dave` → **21 items** (of 73 total;
  28 items are `owner=dave` in all states, 47 are `state=open`);
- rulings carrying a non-empty `open` field → **21 of 204** (`s142-D1`, `s143-D1`, `s144-D1`,
  `s145-D1`, `s146-D1`, `s147-D1`, …);
- a **human-appended** lane-specific block, because the current W-46 DO-NOT-RULE list (the
  vocabulary question, repair-or-park, the five W-44 schema choices) is *not* derivable from
  either source and would be silently dropped by a purely generated list. A generated list that
  loses an entry is worse than a hand list, because nobody will notice the gap.

⚠ Also measured, and it constrains the OPEN ITEMS region: **19 of 73 store items are
`condition: UNCONDITIONED`** (the frozen legacy set). A generated brief must print them as a
declared debt, never omit them — a declared gap passes, a silent one fails.

### (c) Which probes are mintable vs seat-bound — ✅ ANSWERED BY MEASUREMENT

Driven this lane, wall-clock:

| probe | plain words | wall | mint-time? |
|---|---|---|---|
| P-1 | component metas vs their schema | **0.20s** | ✅ mintable |
| P-2 | duplicate ids / dangling references in review pages | **0.13s** | ✅ mintable |
| P-4 | briefs and documents with no store row | **0.10s** | ✅ mintable |
| P-5 | a carried number vs a live re-count | **0.29s** | ✅ mintable |
| P-3 | a dead variable rendering as silent black, read from pixels | needs a browser | ⛔ **seat-bound** |

Four probes, **~0.72s total** — mint-time pre-fill is effectively free. P-3 cannot run at mint
time in a plain shell. **PROPOSED: the brief prints `P-3 NOT RUN AT MINT — environment
sandbox-render, see item 5` as a row**, never omits it. A declared gap passes; a silent one fails.

⚠ Worth your eye: P-5 now returns **findings=0**, where the #206 record has it at 1. The
difference is the `knowledge/README.md` repair recorded in the #207 addendum §3 — the probe agrees
with the repair. That is the premise table working before it exists.

### (d) How the generator's owned regions are declared — PROPOSED

This is the [[do-not-rule-list-cannot-fence-a-generator]] class, and the fix is that ownership is
*provable*, not stated:

1. `gen_brief.py --regions` prints exactly which marker-delimited regions it writes. **The
   brief-writing seat must run it before briefing any sub**, so a DO-NOT-RULE list can be checked
   against what the generator will actually overwrite.
2. Each machine region carries a checksum of its own generated content. On re-mint, if a region's
   content no longer matches its checksum, a human edited machine-owned text — the generator
   **refuses and names the region**, rather than overwriting the edit.
3. Human regions are never read, never validated, never rewritten.

## Price

- **Build: ~1 Opus lane.** Store reader + region writer + probe runner + refusal paths + a
  selftest that plants a hand-edit in a machine region and proves the refusal fires, and that a
  clean re-mint stays silent.
- **Ongoing: sub-second per mint**, plus a re-mint whenever the store moves.
- **Debt created, stated plainly:** a generated brief is one more derived view that can go stale.
  Proposed containment — the brief is a **dated period record** of a lane (ADR-0017 exempt); the
  **store stays the one live home**; the brief is never cited as the source of a live fact.

## Consequences and pitfalls (REPLAYED)

- ⛔ **[[premise-ages-faster-than-rule]], and this is the dangerous one.** At #203 a derived
  snapshot's Status column briefed six lanes at 18/18 false-Gap. Auto-filling a premise table is
  the same machine at higher speed: a wrong row now gets minted into every brief. **Mitigation
  proposed and non-negotiable: every premise row prints the command, the rc and the timestamp —
  never a summary word.** A row a reader cannot re-run is a claim, not a measurement
  ([[measure-dont-convert-units]], `s182-D1`).
- ⛔ **[[no-gate-parses-the-artefact]]** — the first gate on a generated brief must PARSE it in
  the consumer's grammar (the sub reading it), not grep it.
- ⛔ **[[instrument-without-a-consumer]]** — the generator must be driven on a real brief in the
  same wave it is built, or it is a zombie. The #208 wave's briefs are the named first consumer.
- ⛔ **[[green-tests-cannot-see-scope]]** — a green selftest proves the writer works, not that the
  brief is a brief anyone can act on. Proposed acceptance test: a sub is briefed from a minted
  brief and returns without asking a question the store could have answered.
- ⛔ **[[gate-glob-scope-rule]]** — the generator rules only as wide as the store it reads. Items
  outside `_state.json` (memory hooks, chat rulings) are invisible to it and the brief must say so.
- ⛔ **[[write-once-principle-floated-192]] / ADR-0017** — the minted brief must not become a
  second home for open-item facts.

## Open questions returning to you — Proposal 2

**Q2.1 — Given that `by: Dave` selects 204 of 204 rulings, is the store's `owner=dave` + a
human-appended block the right source for a generated DO-NOT-RULE list?**
Run search: rulings scan for `gen_brief` / `brief generation` / `mints PM brief` → **1 hit,
`s204-D1` only** (the programme entry itself, which specifies "rulings tagged Dave's" — the very
premise this measurement contradicts). Scan for `owner` / `tagged as Dave` → 1 hit, `s174-D1`,
unrelated (component-scaffold gates). `python3 knowledge/_memento_search.py "brief generator mint
open items fences"` → ran, no ruling. **OPEN, YOURS** — and note this is a correction to `s204-D1`'s
item-4 wording, so it is put to you as a correction, not taken.

**Q2.2 — Build gen_brief.py first, or the controller first?** Priced above. Recommendation:
`gen_brief.py` first, because it makes the controller's cards cheap to author.

---

# PROPOSAL 3 — The CI pixel leg (programme item 5)

## What it is, in plain words

Make the pixel probes run automatically in GitHub Actions on every push, instead of only in a
sandbox somebody staged by hand. The render job that would run them **already exists** — you ruled
it in at #155 ("keep the ubuntu solution") and it already installs Chromium.

## Consumer named at birth

`.github/workflows/gates.yml` → the **`render` job** (added #155 on the #153-A ⑨ proposal). It
already runs `pip install playwright && playwright install --with-deps chromium` as root, and
already carries one blocking step and one advisory step.

## Scoping answers

### (a) ⛔ THE NAMED DEFECT, measured this lane — and it must be fixed BEFORE any CI wiring

P-3's environment refusal **exits 1 and does not use the could-not-ask convention**. Measured:

```
env -u PYTHONPATH -u PLAYWRIGHT_BROWSERS_PATH -u LD_LIBRARY_PATH \
  python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check
→ rc = 1
first line: "  ⛔ NOT-IN-THIS-ENVIRONMENT: playwright is not importable. …REFUSED — not a pass."
last line:  "PROBE P-3 — findings=UNKNOWN (environment refused)"

grep -n "77\|COULD-NOT-ASK\|could_not_ask" knowledge/_probe_registry/_registry.py
→ 0 lines
```

So today, in CI, **a P-3 environment refusal is indistinguishable from a real measured failure** —
and the registry runner cannot bucket it either. That is precisely the class `s193-D1` ruled fixed:

> `s193-D1`: "MAKE THE GATES ROCK SOLID BY FIXING THE CLASS, NEVER PATCHING… the COULD-NOT-ASK
> third verdict (exit 77 + self-naming first line, `_could_not_ask.py`) wired across tier/
> reach-dependent gates and read by `_build_survey.py` and `_build_all.py`."

The convention requires **both halves**: exit code 77 *and* a first line beginning
`COULD-NOT-ASK:`. P-3 satisfies neither — its refusal line is indented and begins `⛔`.

**PROPOSED as step 1 of item 5, before any workflow edit:** wire P-3 and `_registry.py` to
`_could_not_ask.py`, keyed on the unreachable input (the playwright import), **never on "am I in
CI"** — that is the #173 lie in a new shape. Mutation-proven both ways: the refusal fires when the
import is gone, and a real finding on the reachable side still exits 1.

### (b) The "shared measurer" — ✅ ANSWERED, and the answer is: do not build one in this lane

Measured: **fourteen modules import playwright independently**
(`_build_instrument_fit.py`, `_render_button_responsive.py`, `_render_journey.py`,
`_render_links.py`, `_render_notif.py`, `_render_sme.py`, `_render_smej.py`, `_render_tags.py`,
`_sweep_type_enactment.py`, `_validate_hit_area.py`, `_validate_screen.py`,
`_validate_state_contrast.py`, `_verify_dv_stacked_enactment.py`, and P-3). There is no shared
measurer today.

The environments genuinely differ and the workflow already says why: CI has root, so
`playwright install --with-deps chromium` needs "none of the sandbox lib-farm choreography"; the
sandbox needs `PYTHONPATH=/var/tmp/pylibs`, `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-<n>`,
`LD_LIBRARY_PATH=…/chromelibs/…`, `TMPDIR=/var/tmp`.

**PROPOSED: P-3 is already close to environment-agnostic** — it searches
`PLAYWRIGHT_BROWSERS_PATH`, `~/.cache/ms-playwright` and `/var/tmp/pw-browsers-*`
(`probe_dangling_var_pixel.py:117,123`), which covers the CI default. So item 5 is a **CI step plus
the 77 wiring**, not a refactor. A fourteen-call-site measurer refactor is a separate, larger,
externality-heavy lane — and `s172-D3` fences exactly this appetite ("minimum complexity for the
current task, no abstractions for hypotheticals"), with your own condition attached: *"careful of
externalities, I don't want to fix something only to break other constituent parts."*

⚠ **UNMEASURED, declared:** P-3's wall-clock in CI. It renders 14 pages
(`--check` → "14 page(s) rendered … 14 positive control(s)"). I did not stage a browser in this
lane to time it. **Priced: one measured CI run before any tier is fixed** — do not set a tier on
an unmeasured runtime.

### (c) Which probes push-blocking vs survey-tier — PROPOSED, with a ruled precedent for the shape

The *shape* is not a fresh choice; you ruled it for a new gate at `s114-D2`:

> "(1) ships **ADVISORY** with the named rules; (2) a **NAMED PROMOTION TRIGGER in code, not
> prose**; (3) the waiver is a legal form an agent can use honestly (declare + name the rule +
> price the fix); (4) detection and discharge mutation-tested as SEPARATE clauses."

And the render job already carries a live example of survey tier: `continue-on-error: true` on the
full contrast sweep, "ADVISORY until the Banner 8 clear (#151 open)" — precisely because blocking
on a declared-open item makes every unrelated push red.

Applying that shape, **PROPOSED per probe** (all promotions remain yours under derivation
governance; `_promote.py` proposes and never promotes):

| probe | plain words | proposed tier | why |
|---|---|---|---|
| P-1 | metas vs their schema | **survey → blocking candidate** | 0 findings today, fast, deterministic; but its own `blind` field names an open widen-vs-repair question that is yours |
| P-2 | duplicate ids / dangling references | **survey** | 46 live findings today; blocking would redden every push over `W-49`'s open repair-or-park — the Banner-8 situation exactly |
| P-3 | dead variable → silent black, from pixels | **survey in the render job** | runtime unmeasured; promotion trigger = N consecutive clean CI runs, written in code |
| P-4 | documents with no store row | **survey** | its unrowed-doc half is already covered blocking by `_gate_doc_rows.py`; a second blocking gate on one condition is two code paths for one rule |
| P-5 | carried figure vs live re-count | **survey** | it is a heuristic, not a parser (its own declared gap); heuristics that block manufacture waivers |

**Not one of these is proposed as push-blocking on day one.** That is deliberate and it follows
`s114-D2`: ship advisory, promote on a trigger written in code.

### (d) The could-not-ask exit protocol — ⛔ NOT RULED HERE, carried untouched

On your DO-NOT-RULE list, and left alone. What can be said without ruling it, so the question
reaches you narrower than it was:

- The **convention** exists and is ruled and enacted — `s193-D1`, `knowledge/_could_not_ask.py`,
  exit 77 + `COULD-NOT-ASK:` marker, five gates wired ([109], [112], [113], [59], [71]).
- `_build_survey.py` already reports three verdicts and **excludes refusals from its exit code**,
  so the old "one refusal blocks the whole queue" failure is closed.
- **The genuine residual, in plain words:** *when the last word from the render job is "I could
  not measure this", does that stop a push, or does it pass with the gap on the record?* That is
  yours, and item 5 must not decide it by choosing a `continue-on-error` value in a workflow file.
  Run search: rulings scan for `could-not-ask` / `exit 77` / `third verdict` → **1 hit, `s193-D1`**,
  which rules the *convention* and is silent on the exit protocol. **OPEN, YOURS.**

## Price

- **Build: ~half an Opus lane.** The 77 wiring for P-3 + `_registry.py` (~30–60 lines plus
  selftest arms, both directions) is the substantive part; the workflow edit is a handful of lines.
- **Ongoing CI cost:** the render job already installs Chromium, so the marginal cost is P-3's own
  runtime — **unmeasured, and a measured run is a precondition, not a follow-up.**
- **Priced deferment:** the shared-measurer refactor across 14 call sites is deferred, priced at
  ~1–2 Opus lanes with high externality risk, and is **not recommended** until a second probe
  actually needs it.

## Consequences and pitfalls (REPLAYED)

- ⛔ **#173, [[gate-cannot-pass-in-one-environment]]** — the named killer for this item. The
  workflow file already carries the full post-mortem: a gate that cannot pass while the
  documentation says it can is worse than one that simply cannot pass, "because this file is what
  a reader consults when the gate is red." Mitigation: (a)'s 77 wiring, keyed on the unreachable
  input and never on a CI env var.
- ⛔ **[[instrument-without-a-consumer]]** — a probe wired into CI that everyone learns to ignore
  is worse than an unwired one, because it manufactures consent for red.
- ⛔ **[[a-crash-is-not-a-fail]]** — the registry runner must distinguish crash, refusal and
  finding. Today it distinguishes none of them; it parses a `findings=<n>` line, and P-3 prints
  `findings=UNKNOWN` on refusal.
- ⛔ **[[gate-glob-scope-rule]]** — rule only as wide as the glob. Already live evidence:
  `_gate_dataviz_vars.py` names `knowledge/snippets/DataViz-interactive.html` in its declared glob
  and that file does not exist (`ls knowledge/snippets/ | grep -c DataViz-interactive` → 0). A CI
  tier set against a glob with a phantom member is a tier set against a smaller population than it
  claims.
- ⛔ **[[green-tests-cannot-see-scope]]** — a green CI leg proves the probes ran on the pages the
  glob names, nothing more. The registry's own line applies: *a green registry run means the
  probes ran; it does not mean the tree is clean.*
- ⛔ **[[mutation-tests-the-clause-not-the-feature]]** — the 77 wiring must be proven by taking the
  import away and reading the exit code, never by asserting on the module's constant.

## Open questions returning to you — Proposal 3

**Q3.1 — Approve the sequencing: fix P-3's refusal to the ruled 77 convention FIRST, then wire
CI?** Run search: rulings scan `could-not-ask` / `exit 77` / `third verdict` → 1 hit, `s193-D1`,
which rules the convention as a class fix but names five specific gates, not P-3 (P-3 did not
exist until #206). So whether `s193-D1` *reaches* P-3 by its own class logic, or needs your word,
is the question. My reading: it reaches it, and this is a defect repair rather than a new
decision — but I am not ruling that.

**Q3.2 — The proposed tier table in (c): accept, or move any probe?** Run search: rulings scan
`ships ADVISORY` / `promotion trigger` → **1 hit, `s114-D2`**, which rules the *shape* (advisory
first, trigger in code) but not these five probes. **OPEN, YOURS**, and it stays entangled with the
DO-NOT-RULE items it must not pre-empt: `W-49`'s repair-or-park sets P-2's tier, and the
twice-caught vocabulary question sets whether any of them is a promotion candidate at all.

---

## Deferments, each priced

| deferred | price if taken later | why deferred |
|---|---|---|
| Shared render measurer across 14 playwright call sites | ~1–2 Opus lanes, high externality risk | `s172-D3` fence — no abstraction for a hypothetical; one probe does not justify it |
| P-3 CI wall-clock measurement | ~15 min inside the first build lane | cannot be measured without staging a browser; it is a precondition of setting P-3's tier, not a follow-up |
| Promotion of any probe to a blocking `_build_all.py` gate | one ruling of yours + ~half a lane to wire | derivation governance — promotion is yours, and the twice-caught vocabulary question is upstream of it |
| A parser (not a heuristic) behind P-5 | ~half an Opus lane | declared gap in the probe's own docstring; blocking a heuristic manufactures waivers |
| Repair of the 46 duplicate-id / IDREF findings | unpriced here — it is `W-49`'s repair-or-park, and that is yours | DO-NOT-RULE |
| `notes/_decisions/` as a directory with a store row | ~10 min | contingent on Q1.1 |

## What this lane deliberately did NOT do

No code was built. No generator was written. No gate was wired. `_build_all.py` was not run.
`_LIVE-STATE.md`, `GOOD-MORNING.md`, `_CHAIN.md` and `knowledge/_rulings.json` were not touched.
Nothing was committed. The twice-caught vocabulary question, the promote/wait call on the three
probe candidates, `W-49`'s repair-or-park, the five W-44 schema choices, whether `notes/_claims/`
earns a store row, PM-topology permanence and the could-not-ask exit protocol were all left
untouched and unruled — each is named above only where a proposal has to route around it.
