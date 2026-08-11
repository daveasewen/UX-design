# _FUTURE-STATE — the forward ledger

> STANDING: side-quests, feature ideas, and resurrection candidates — the future half of the state
> machine. Read alongside `_LIVE-STATE.md` (what's true now) and `_DECISION-HISTORY/` (how we got here).

*Created 2026-07-18 at Dave's ask during the consolidation review: "how do we store all the ideas for
side-quests, features and ideas that I want to hold onto, so we have a future-state-machine." Division
of labour: **`_LIVE-STATE` keeps in-flight TARGETS (ruled 2026-07-05) and the SPIN-OFF register (ruled
"surface, don't bury")** — this file holds everything forward-looking that is NOT in flight. An idea
graduates OUT of here into `_LIVE-STATE` OPEN/TARGET when work starts. Refresh with the capture ritual.*

**Entry format:** what · why it's held · what it feeds (Apollo phase/mode) · source/provenance pointer ·
status (`idea` / `parked` / `resurrection-candidate` / `graduated→LIVE`).

## ⚠ Proforma svg `data-pl/pr/h` are INERT — declared #72, homed #76 by the 2d EXIT CHECK

**What:** the `data-pl` / `data-pr` / `data-h` attributes specced onto the proforma svg during #72's
DV-D02-A discharge do nothing there — the proforma's inline engine reads the `DV_PL` / `DV_PR` / `DV_H`
constants and never looks at the attributes. `canon/` is unaffected; this is a proforma-only divergence.

**Why it's held:** it was declared honestly at #72 (`_LIVE-STATE.md` § #72 delta) and never contradicted,
but it lived ONLY on a rolling delta. ⚠ **Found by the step-2d EXIT CHECK at #76 with zero standing
home** — GM, `_FUTURE-STATE.md` and `_DS-IMPROVEMENTS.md` were all grepped and all empty. One more roll
and the finding would have existed only in `_LIVE-STATE-ARCHIVE.md`, which is a dated home and does not
count. This entry IS the copy-up the runbook requires before the #72 delta may move.

**What it feeds:** Craft — proforma/canon parity. The open question is which way parity should run
(teach the proforma engine to read the attributes, or strip attributes that assert a capability the
surface does not have). **Not ruled, not guessed at.**

**Source:** `_LIVE-STATE.md:83` (#72 delta, 2026-08-01) → `_LIVE-STATE-ARCHIVE.md` after #76's 2d roll ·
runbook `_RUNBOOK-capture-ritual.md` step 2d EXIT CHECK.
**Status:** `parked` — a declared inertness, not a regression. [born #76 · guards: proforma svg attribute
claims · until: parity ruled either direction]

## ★★ Cowork gauge crack — a sub can read its parent's transcript (found #67, Dave asked "is there another way?")

**What:** the Cowork harness exposes `session_info` tools. PROBED #67: (a) a session cannot list
ITSELF — self-reading is blocked; (b) **completed sessions ARE readable** (full transcripts of
#33–#66 confirmed listed) ⇒ post-hoc tiktoken measurement of real sessions can calibrate the
per-beat price estimates against actuals; (c) **a spawned sub sees the parent as an ordinary
session** ⇒ a tiny Haiku sub (`read_transcript` on the parent → tiktoken → report one number)
would give a measured MID-WINDOW gauge, bulk paid in the sub's window. Would convert the
standing ⛔ NOT CAPTURED — UNMEASURED Cowork gap into measurement-on-demand.
**Declared residual before it is believed:** transcript = conversation text only — system prompt,
tool schemas, images are not in it ⇒ it measures a FLOOR with a named gap, not the bill. And
claim (c) is UNPROVEN — the sub's read of a RUNNING parent has not been attempted; prove it
before pricing anything on it (a measurement mechanism gets the same discipline as any gate:
mutation-test it — feed it a session of known size first).
**What it feeds:** the throttle (`_RUNBOOK-context-gauge.md`); pre-flight stamps stop being
retrospective estimates.
**Source:** #67 chat, probe run live at Dave's question. **Status:** `idea` — probe first,
~one Haiku sub, next session candidate.
**⛔ DOWNGRADED #68 (2026-08-01, mutation-test run live):** claim (c) is **DISPROVEN AS SCOPED** — a Sonnet probe with a falsifiable pass criterion (quote commit `5f09f2a`) found the RUNNING parent ABSENT from `list_sessions`' full 205-session inventory, nothing marked running, `is_child` never true ⇒ a sub has NO ADDRESSABLE HANDLE to its live parent. Claims (a) and (b) stand: post-hoc calibration on completed sessions remains available NOW and is the surviving half. Status: `idea` → **post-hoc-only**. — three data-entry paths for bounded values (Dave, 2026-08-01 #67)

**What:** when Apollo's edit mode surfaces the bounded parameters a user may edit, the *values*
(the data a chart/component displays) get three entry paths: **(1) edit values** directly (inline,
within the declared bounds) · **(2) a values generator** (synthesise plausible data to shape —
series count, range, distribution) · **(3) CSV upload** (bring real data in).
**Why held:** floated in the #67 D4 scoping conversation (header-cluster/legend contents vary by
chart type + data shape; rules-as-record + inference-as-clerk agreed same beat) — edit mode itself
is not yet in flight. Register: FLOATED, not ruled.
**What it feeds:** Craft phase (edit mode = bounded parameters on rails); the values generator is
the same derivation-governance grain — machine drafts, bounds constrain, user decides.
**Source:** #67 session chat, alongside `notes/_briefs/2026-08-01-dv-lockup-scope-brief.md`.
**Status:** `idea`.

## ★★ EXPANDABLE "OTHER" BUCKETS — the cap must not become data loss (Dave, 2026-07-27 session #6)
**status: FLOATED — explicitly NOT ruled, not designed, not scoped.** Dave, verbatim, in the same
breath as ruling the segment cap:
> *"Lets cap at 6 for now, but note for later, all bucketed 'other' segments should be expandable,
> through some mechanism we'll explore later."*

**What it holds.** Segment caps bucket the remainder into an **"Other"** slice. Today that remainder is
**terminal** — the donut's `dv-pie-009` (≤6, live) buckets with **no route to the detail**, and
**DV-D18** (2026-07-27) has just extended the same cap to stacked columns. Dave's note says the bucket
must be **expandable**: the reader gets legibility by default and the detail on demand.

**Why it's held rather than built.** The mechanism is genuinely open — drill-in (Other replaces the
series set), expand-in-place (Other splits into its constituents), a companion detail view, or a
disclosure in the legend. **These are different products with different a11y, different keyboard
models, and different `dv-legend.js` state shapes**, and one of them (expand-in-place) collides with
the ≤6 cap it exists to relieve. Dave said *"we'll explore later"* — this is the note that makes later
possible, not a head start on it.

**⚠ WHY THIS IS LOAD-BEARING, not a nice-to-have.** **DV-D18 is only defensible because of this.** A
cap with no expansion route is **data loss presented as legibility** — the chart silently stops being
able to say what it was given. ⇒ **Flag it if a cap ships and this is still floated**; the pairing was
Dave's, in one sentence, and separating them would keep the constraint and drop the remedy.
Applies **retroactively to the donut**, which already caps and already has no route out.

**Feeds:** Craft (the chart programme) · **Source:** Dave, 2026-07-27 session #6 ·
**Ledger:** `knowledge/_proforma/_DATAVIZ-DECISIONS.md` § Batch 10, DV-D18 · **status:** `floated`

## ★★ FORCING THE KG INTO THE DECISION LOOP — "the KG shouldn't be ignored, that's what it's there for" (Dave, 2026-07-27)
**status: FLOATED — explicitly NOT ruled.** Dave, verbatim, mid-session:
> *"I want you to note that we may create something that will force decisions to check that KG in such
> situations, I don't know what that is, you will have to explore the benefits, method and implications
> with me, the KG is a valuable resource and shouldn't be ignored, thats what it is there for... along
> with many other things"*

**He named it while holding the evidence.** Same session, ds-014 call (a): I recommended a 2px
surface-coloured stroke for the stacked column's separation. Dave pushed back — *"I prefer the geometry
the border will obscure gridlines, may I know why you recommend borders?"* — and then supplied the fact
that settled it: *"btw the gap is only 2px minimum, this is in the dataviz specifications in the KG."*
**He was reading the KG. I was not.** CONSULT-before-designing is a STANDING rule and I skipped it; the
recommendation came from transferring the donut's mechanism without checking the ground under it.

**The finding that came out of finally running the consult, and it is the generalisable one:**
dv-004's rule text is **mechanism-NEUTRAL** — *"minimum 2px separation between colour blocks"*. But
`_validate_dataviz.py` had implemented it as *"must carry a surface-coloured stroke >=2px"*. **The gate
had silently narrowed a rule into one mechanism** — so the only "compliant" answer available to an agent
reading the gate was the wrong one for a chart that sits on gridlines. ⇒ **The KG was right and reachable
the whole time; the enforcement layer had drifted off it, and nothing compared the two.**
*(Fixed this session for dv-004 specifically — both mechanisms now pass, 9 new bites. The CLASS is what
this entry holds open.)*

**Why this is not just "remember to consult."** A rule that depends on the agent remembering is exactly
as reliable as a gate nobody proved can fail — which is the ds-013/CLAIMED lesson (ADR-0016). Dave's
instinct is to make it **structural**. Angles to explore WITH him, none picked:
- **(1) Rule-text vs gate-implementation drift check.** Compare what a rule SAYS against what its gate
  DEMANDS; flag narrowings. This is the one that would have caught dv-004 directly, and it is the exact
  mirror of ADR-0016: the register asks *"is this ruling live?"*, this asks *"is the gate still enforcing
  the rule, or its own paraphrase of it?"*
- **(2) Consult-on-write, not consult-by-discipline.** The build already touches every changed file — it
  could run the consult for the rule-IDs the diff touches and surface what governs them, advisory then
  blocking. Removes the remembering from the loop entirely.
- **(3) Consult receipt as a precondition on rulings.** A decision record must cite the consult it rests
  on. Cheap; games easily (a citation is not a reading) — probably weakest alone, useful combined.
- **(4) Reframe: the KG as the thing an agent must ASK, not the thing it may recall.** Ties to
  [[stale-reading-failure-mode]] and the retrieval-not-recall principle in the charter — this may be a
  charter-level statement rather than a tool.

**⚠ Implication to price honestly before building any of it — the instrument can be blind too.** Today's
consult printed **`rulings (5/5 shown, --all for more)`**: it TRUNCATES by default. A forcing function
built on a truncating query is a CLAIMED gate with extra steps — the ds-013 shape exactly. **Any build
here needs the consult's own recall bite-tested first** (does it return the governing rule for a known
case, and does it fail loudly when it cannot?). Second cost: every decision gains a friction step, and
the context gauge already binds.

**Feeds:** Discover/Create · the enactment-proof programme (ADR-0016 P2/P3) · the harness-framework
spin-off (this is a governance primitive other teams would want, not an Apollo local fix).
**Source:** this session, alongside ds-014 calls (a)+(b). **Owed: a session with Dave to explore it —
benefits, method, implications. Do NOT build ahead of that conversation.**

### ★★ EXPLORATION BEAT 1 — 2026-07-27 (later morning #3). Dave reframed it TWICE and both are his.

**Reframe A — "maybe we are checking the wrong thing." ⇒ INSTRUMENT FIT is a THIRD AXIS.**
Angle (1) as written (*compare what a rule SAYS against what its gate DEMANDS*) **would not have caught
`aid-009`.** The rule names *"a minimum 44×44px target area"*; `_validate_a11y.py` calls its check
*"target size"*. **The vocabulary matches — the narrowing is not in the words, it is in the INSTRUMENT.**
A static regex can observe a *declared box*. The rule is about a *target*. Those two stop tracking each
other the moment the corpus expresses the property through a mechanism — an expander, a token, or a
transform — and **the gate goes QUIET rather than RED.**
⇒ The question to ask of every rule: **"what property does this rule name, and can this gate's instrument
observe that property at all?"** Instruments, weakest→strongest: static parse → DOM read → render +
hit-test → human eye. **A gate whose instrument is weaker than its rule's property is inert BY
CONSTRUCTION, however well written.**
⇒ **This is a THIRD axis on top of ADR-0016, not a sub-case of it.** PROVEN/CLAIMED/UNPROVEN ask *"is
there a check, and can it fail?"* Instrument-fit asks *"is it looking at the right thing?"* — **a check
can be PROVEN (bite-tested, fails correctly) and still be measuring a proxy that does not track the rule.**
dv-004 was the *narrowing* case; `aid-009` is the *instrument* case, and it is the larger one.

**Reframe B — Dave's, and it names the propagation defect: *"the hit mechanism should have triggered
something that cascaded this elsewhere."*** Adopting the `::before` hit-area expander is a LOCAL CSS
decision with a GLOBAL governance consequence — it silently removes the component from `aid-009`'s
sample. **Nothing carried that fact anywhere.** No registry entry, no re-check, no flag on the rule. The
only thing that connected the adoption to the exemption was **Dave remembering the mechanism existed**,
which is [[stale-reading-failure-mode]] pointed at the enforcement layer instead of the design layer.
⇒ Sibling of [[assertion-propagation-gap]] (*a gate fires on FLIP, so a doc known-wrong-now is never
chased*): **here the gate never fires at all, because the adoption IS the exemption.**
⇒ **Design implication for the forcing function, and it may be the strongest angle yet:** the trigger
should not be a periodic sweep — it should be **adoption-time**. When a component takes up a mechanism
that changes which gate can see it, THAT is the event that must cascade. *(Cheapest first cut: the
mechanism is already a marker in the CSS. Make claiming the exemption require naming the rule it exempts
from, and let the register harvest the claim — an exemption that must declare itself is an exemption you
can count.)*

**⬛ OPEN, all Dave's:** (i) does instrument-fit join the register as a third axis, or stand as its own
check? (ii) is the trigger adoption-time or sweep-time? (iii) the instrument tagging pass across 465
rules is mechanical and would rank the whole corpus — **NOT started, deliberately** (scoped as a build,
and he capped the window). **Evidence backing all of the above: `ds-015`.**

### ★ Exploration beat 2 — 2026-07-27, later morning #4: (i)(iii) DELIVERED, (ii) RULED COMPLEMENTARY

**Dave ruled four of the five calls** (*"I'll go with your recommendation, I just want the most robust
methods"*). (i) third axis — built as its own generated register that sits ON TOP of ADR-0016.
(iii) **the 465-rule pass is BUILT and RUN**: `knowledge/_build_instrument_fit.py` →
`_INSTRUMENT-FIT.md`, 11 bites, advisory build steps 58+59, build 60/60 green.

**⇒ (ii) IS RULED, and the framing was the thing that needed correcting, not his lean.** He said
*"I lean adoption, seams less likely to carry mistakes… maybe sweep if more efficient, I need to
understand the implications of both"*, then on the analysis: ***"You're right about 2 they are
complimentary."***

- **Adoption-time** captures intent at the moment it exists, from whoever knows *why* — **counted**
  data, not inferred data. Blind to everything already shipped: **64 of 67 snippets already carry the
  `::before` expander and it would find zero of them.** And a *missing* declaration is silence — the
  very failure mode being hunted.
- **Sweep-time** is retroactive and needs no cooperation. **Proven the same day:** the pass surfaced
  **7 dangling citations** laid down months apart, which no adoption-time trigger could reach. But it
  reports late and **its own coverage is unmeasured** — this sweep is blind to 265 rules and cannot
  classify 279 more, and *nothing revealed that until a second check was built*.

⇒ **Each one's blind spot is the other's coverage, and the only way to detect a MISSING declaration
is to sweep for it** — so the sweep is not optional, it is what makes the adoption-time rule
enforceable. **Held shape for design (not yet built):** adoption-time as the forcing function +
a sweep **narrowed to one job — find undeclared adoptions**. Narrower than a general sweep, so
cheaper and less blind. Same pair now applies to itself in **`ds-016`** remedy (c).

**⬛ STILL OPEN, Dave's:** call **(4)** the consult's enforcement column — *"I lean fix, but this
probably needs a discussion"*, **NOT ruled**; the `5/5 shown` denominator is separable and trivial and
was **not** done (Red budget). Call **(5)** the `CTRL` vocabulary sweep — **ruled YES, not started.**
New: **whether to invest in the pattern table** (279 of 465 rules UNTAGGED — the figure is published
so the call is made on a number) and **ds-016's** three candidate remedies.
Evidence: `ds-016` · `_DECISION-HISTORY/2026-07-27-the-index-cannot-see-the-rule.md`.

## ★ Memento v1 — a shareable pack (registered M12, 2026-07-27 #18)
**status: TARGET, not started.** Registered by ruling (M-set item 12, `notes/_MEMENTO-DECISIONS.md`
§ ★ M-SET; brief `notes/_briefs/2026-07-27-memento-hardening-brief.md`).

**What.** The portable kit, extracted project-agnostic: the **capture ritual** + **`_capture_gate.py`**
+ the **gauge canon** (`_RUNBOOK-context-gauge.md`, bands and throttle) + the **dream-pass runbook** +
the **dreamer spec** (`.claude/agents/dreamer.md`) + **GM / `_LIVE-STATE` templates**.

**Why it's held.** It is the answer to a question nobody else has written down — *how does a
long-running agent project retain state, record supersession, and audit its own decisions when every
session starts with no memory.* Sibling to `_LIVE-STATE`'s first named spin-off candidate (the state
machine); Memento is that candidate grown teeth, because the gate half is what makes it more than a
filing convention.

**Blockers, all three:** (1) **M3–M10 landed** — the growth contracts must be enforced, not just
described, or the pack ships prose; (2) **one clean UNATTENDED Sunday fire** of the dream pass — the
scheduled path has never run end-to-end without a human in the window, so the lane is unproven exactly
where a shared pack would be used; (3) **`MEMORY.md` trim** — the index loads on every cold start and
is currently over target, which a recipient would inherit.

**What it feeds:** the state machine as a product, not a practice. Spin-off register, `_LIVE-STATE`
§ SPIN-OFF / GENERALISABLE CANDIDATES.

## ★ Dream-pass cadence — "a sleep once a week with occasional naps" (Dave, 2026-07-28 #22 post-wrap)
**status: FLOATED — posture confirmed, schedule deliberately UNCHANGED.** Dave, verbatim, closing #22:
*"so a sleep once a week with occasional naps, sound good for now"* — confirming the agent's read that
the bottleneck is his ruling time + enactment beats (dream work jumped the lane queue twice while
lane-1 step 2 waited), not dream supply (yield holds: 8 → 5 → 6 proposals across three passes in
three days — the corpus is not over-dreamed).
**What.** Weekly Sun 07:10 stays the FLOOR (A-D2 unchanged — M12's unattended proof depends on the
schedule firing untouched). **Manual "naps" licensed:** fire `run dream pass` (S-D4, one line) when
the unread transcript pile approaches ~15 — the lane's own lookback unit — or ahead of a targeted
hunt (pass 3 evidence: half its proposals came off hunt lines Dave added that same morning; the
steering works, which argues targeted manual fires over a shorter fixed interval).
**Re-price trigger:** AFTER M12's Sun 08-02 proof AND lane-1 landing — lane 1 should cut drift
generation, so a cadence priced today prices a corpus about to change. Judge on yield-per-pass data,
not feel. A floated item is not authority (ds-017): any actual schedule change re-rules A-D2.
**Feeds:** the Memento lane, steady-state · **Ledger context:** `notes/_MEMENTO-DECISIONS.md` A-D2
(weekly) + S-D4 (invocation) · **Source:** #22 post-wrap chat, Dave verbatim ·
provenance: session #22 · 2026-07-28 · status: floated

## ★ Multi-thread "GOOD-MORNING" — a handoff mechanism for parallel long-running threads (Dave, 2026-07-24)
**The problem Dave named:** two async threads now run in parallel ACROSS sessions — the chart **FAN-OUT**
(wave; GM §C·1a + `notes/_briefs/2026-07-24-chart-wave-lane{1,2,3}`) and the **CONTROLS SYSTEM** (seg atom +
hit-area + mini ramp). The single linear GOOD-MORNING is **single-threaded**: when you bounce between threads
across sessions, one thread's state goes stale in GM and **context slips** (observed 2026-07-24 — GM still said
controls-system "scoped" after it was built + committed `f5e7bce`).
**Explore:** GOOD-MORNING becomes a **dispatcher/index** across per-thread state docs (e.g. `GM-thread-<name>.md`),
each thread carrying its own Memento — orientation · single next-action · gauge reading · residues · brief/receipt
links. The master GM lists which threads are LIVE, their gauge, and the one next action per thread. Extends the
**parallel-session conductor** model (same-day lanes → async cross-session threads). Ties to: harness-framework
spin-off · session-title convention · the gauge-stamp practice.
**Bridge until built (in use now):** each thread = a labelled STRAND in the one GM's queue
{next action · model · gauge · residues · brief file}. **Not now — Dave: "note this for exploration."**

## ★ Parallel windows vs subagents — the execution-mechanism choice (Dave, 2026-07-24, reopened)
**The question Dave reopened** (while launching the chart fan-out): should fan-out lanes run as parallel
**Cowork windows** (the ratified parallel-session-conductor model, proven 2026-07-21) or as **subagents**
spawned inside one session (Mode-2 delegation — DELIBERATE per the routing audit #12, not default)?
**The frame — NOT rivals; pick by WORK SHAPE** (the converge/ship vs explore/noodle split we already have):
- **Windows** — full session each: own context budget + model + **effort knob** (subagents can't express the
  Fable·medium vs ·high distinction); your eye in the loop per lane → live rulings absorbed mid-flight (the
  chart exemplar's SIX refinements came this way); fresh conductor window = context hygiene. *Cost:* you
  shepherd + tend; parallel live threads drift/stale (the multi-thread problem above is the same tax).
- **Subagents** — one session orchestrates, no window-juggling; I hold all returns + reconcile with the whole
  picture. *Cost:* they start COLD (re-derive context every spawn — the expensive path on this plan); I get
  only their final message, not the transcript (you lose watch-and-intervene); a subagent can't pause for a
  live ruling; and the conductor BALLOONS (3 receipts absorbed into my own context vs a fresh window).
**Side-quest handling (the sharp bit):** the anti-pattern is a tangent becoming a SECOND LIVE WINDOW that
competes for attention + goes stale. Proposed rule → a tangent becomes a **window** only if it needs your eye
AND you're ready to tend it; if bounded + eye-free ("audit X, report back"), a **subagent**; else a
`_FUTURE-STATE` entry. Drains most of the staleness tax without babysitting threads.
**Agent's steer (for the talk, NOT ruled):** keep windows for ruling-generative build work (the chart
fan-out; also keeps the conductor fresh); adopt subagents as the home for bounded side-quests + repo-wide
searches — a force-multiplier, not a replacement for the session model. **Feeds:** the harness ·
harness-framework spin-off · the multi-thread GOOD-MORNING entry above. **Source:** in-chat 2026-07-24 (the
tuner-v2 / fan-out-handoff session). **Status:** idea — reopened, NOT ruled; Dave is talking it through,
decision + inscription to follow.
**UPDATE 2026-07-25 — a THIRD mechanism surveyed (notes-only, NOT ruled):** Claude Code now ships **dynamic
workflows** (Claude writes a JS orchestration script — `agent()`/`parallel()`/`pipeline()`, schema-validated
node outputs, per-node model routing, saved to `.claude/workflows/` as re-runnable `/commands`) + **agent
teams** (experimental: lead + teammates, shared task list, plan-approval + `TaskCompleted` exit-2 hooks) +
**subagent persistent `memory:`** (per-agent MEMORY.md that survives compaction — a productised slice of
Memento). Verified against the official docs; full mapping-to-our-practice table + the harness-spin-off
reframe (layer ON TOP of upstream, not competitor) in
`notes/2026-07-25-claude-code-orchestration-survey.md`. Sharp constraints: Claude Code/Desktop-side (Cowork
parity gap stands) · workflows take NO mid-run rulings (Dave's eye is load-bearing) · teams don't worktree-
isolate. Candidate trial: ONE bounded audit as a workflow vs the same job as a conductor divvy.

## ★ Mobile variants — a component-wide dimension to build out (Dave, 2026-07-24)
**What:** components will carry MOBILE variants, not just responsive reflow. Dave flagged this while ruling
the segmented control: the rounded **PILL segmented control** is reserved as a **mobile Tab-bar alternative**
(it already lives in `snippets/Tab-bar.reference.html` variant B — full-width, elevated, sliding pill), so the
desktop segmented-control atom stays square and drops the pill shape. **Follow-up (Dave's words): raise this
"when we've built out the library"** — i.e. after the base desktop set is fuller, do a mobile-variant pass as a
first-class dimension (touch targets already covered by the hit-area standard / `target/min`; the pill is one
instance). Candidates: bottom nav / tab-bar, mobile segmented (pill), sheets/drawers, mobile-first inputs.
**Not now** — logged so it isn't lost.

## ★★ Live radius / corner tuner — Dave: "return to soon, we need it, don't let me forget" (2026-07-22)
**STATE CORRECTION (2026-07-26, dream-pass P7): v1+v2 are BUILT + render-verified —
`reviews/RADIUS-CORNER-TUNER-2026-07-24-v*.html`. What remains OWED = the tweaks + ruling the numbers
with Dave ("we'll do the tuner after"). Do NOT rebuild from scratch; the ask below is the original
framing, kept for the WHY.**
**What:** an in-browser tuner that dials `border-radius/{control · surface · indicator}` (and a future
`data-mark` slot) **per theme**, live, with buttons/cards/chips/bars updating in place and the values
exportable straight to the theme override sets. **Why it's wanted:** settling corner numbers by argument
doesn't work — the uniform-4 Console misstep this session proved corners must be *tuned per component type,
by eye* (buttons=4, cards=12, bars=square all live at once). The mechanism already exists (role tier +
ADR-0013 component-type tier); the tuner is just the live controller over it. **Priority: SOON** — Dave
flagged it explicitly and twice ("probably soon", "don't let me forget"). Not built now only to avoid
derailing the chart build. **Pattern to reuse:** the "live controller + export" doctrine
([[feedback-live-controller]]) and the OKLab heatmap tuner (`reviews/HEATMAP-RAMP-2026-07-22-v1.html`) as
the interaction precedent. **Feeds:** Apollo interface / theme-generator horizon ([[four-theme-architecture]],
[[product-shape-flexing-engine]]). **Status:** idea — return-to-soon (Dave's standing reminder).

## ★ Heatmaps — PARKED, needs a dedicated live interpolation tool (Dave, 2026-07-22)
**What:** heatmap chart type(s), deliberately deferred out of the chart build-out. **Why held (Dave's
call):** heatmaps are two hard problems at once — (1) *data dimensionality* is unbounded (a heatmap can be
5×5 or 100×100, so cell geometry, labelling, and the table spine can't be a single static lock-up like the
bar/line kit), and (2) *colour is a continuous interpolation* across a ramp, not a fixed palette pull, so it
can't be pre-baked into flat DTCG tokens the way the categorical series + RAG sets are. Both point the same
way: **this wants a live, code-driven interpolation control — a real tool, not a snippet.** Dave: "all of this
suggests when Apollo gets an interface, we'll need a dedicated tool for the interpolation… live, using code.
We need to spec this carefully — just log the intention." **Intention logged; the careful spec is the
follow-up, not now.** Scope note: "probably stick to one heatmap type" when we do build (not the full
zoo of variants). **Seed already exists:** `reviews/HEATMAP-RAMP-2026-07-22-v1.html` — a working OKLab
interpolation tuner (ramp anchors → perceptual interpolation → binned/continuous → hex export + a
lightness-monotonic check). That tuner is the *proof-of-mechanism* for the eventual tool; my design read
(monotonic lightness carries the data; large cells sit in the luminance "bloom" regime; warm-mono default,
incandescent black→red→yellow→white only as an opt-in high-contrast variant because it crosses Dave's
least-stable red+yellow hues) is captured there and in-chat 2026-07-22. **Feeds:** Apollo interface / the
design-time interpolation tool ([[vision-contextual-dashboard]] neighbour; Layer-2 in-browser control
lineage). **Depends on:** a new sequential `data/heat/*` token *class* (distinct from categorical-isoluminant
and status-salience — a third dataviz colour class) — deferred with the type. **Source:** this session +
the tuner file. **Status:** parked (intention logged; spec pending).

## Showroom index: visual component thumbnails on the catalogue cards (Dave, 2026-07-22 wave-2 window)
Dave's ask, deferred at Amber gauge (his hot-clause: "just note it as a change"): each index card
carries a VISUAL of the component, not just name+meta. The count-in-header half SHIPPED same session
(big 40px numeral, self-updating). Thumbnails need a real design decision, not a quick edit:
(a) live mini-iframes = pages need a `#bare` chrome-less mode first or cards show harness header;
(b) static PNGs = blocked on the render-verify path (headless-shell refusal, standing);
(c) hand-rolled CSS glyphs = drift-prone duplication, against retrieval-not-recall.
Recommended shape when picked up: (a) — add `#bare` to the page chrome (hides header/controls,
shows the light pane only), cards embed `<iframe loading="lazy" src="<slug>.html#bare">` scaled;
zero new artefacts, reuses the live pages. Natural slot: Dave's post-buildout tidy pass.

- **The restyle saga + generate-then-normalise lineage** — the two-pass "generate free → constrain +
  verify" experiments and the ungoverned diagnostic pieces. *Why held:* Dave 2026-07-18: "definitely
  going to revisit all the old ideas and experiments… this one might fit into two of the four modes."
  *Feeds:* **Apollo Create — Creative and Explore modes.** *Source:*
  `_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md` + `knowledge/_fitness-test/register-spread-2026-07-05*/`
  + memory `generation-mechanism-ideas`. *Status:* resurrection-candidate.
- **The §9 tuning questions** (rule-crafting, inference tiering, the three-arm experiment) — parked by
  the 07-10 ruling until the substrate is rich enough. *Why held:* "I can tune a machine if it doesn't
  have all the parts" — the factory comes first, the tuning returns. *Feeds:* Create mode dials /
  register ramp. *Source:* `_DECISION-HISTORY/2026-07-07-s9-root-cause-and-ruling.md` +
  `knowledge/_FINDINGS-s9-session-2026-07-07.md`. *Status:* resurrection-candidate.
- **Masthead design revisit** — shipped as an **MLP** (Dave, 2026-07-18); iteration expected across
  much of what we produce. *Feeds:* Craft phase. *Source:*
  `_DECISION-HISTORY/2026-07-16-masthead-rounds.md`. *Status:* parked.
- **Iteration-machine front-end mock** — vision facade, proves alignment only. *Feeds:* the eventual
  Apollo interface/harness. *Source:* `notes/_VISION-iteration-machine_2026-07-03.html` (carries the
  old looks-language — reconcile before reuse, see `_LIVE-STATE` propagation gap). *Status:* parked.
- **Portfolio-interactions craft pass** — the wow pass on the Reorder testbed; don't gold-plate before
  the ask. *Feeds:* Craft. *Source:* memory `portfolio-interactions-invite`. *Status:* idea.

## Apollo Mono button-colour finessing — parked 2026-07-20 (Dave)

Raised by Dave right after the `button/*` snippet rebind landed (build green 35/35). Both are
COLOUR-only finessing, deliberately parked so we could carry on to component build-out — the rebind's
token wiring is settled; these are value/perception tweaks on top.

- **Primary hover ≈ secondary default (collision).** Dave: *"hover-primary is very similar to the
  secondary button, might be a little confusing."* Confirmed numerically: primary hover flattens to
  ~`#5F5F5F` (stored equiv `#626262`) and **secondary default is `#626262`** — essentially the same
  grey. Two different buttons in two different states read identically. *Fix space:* re-tune the primary
  hover opacity/colour, or shift the secondary default step, so the emphasis hierarchy stays legible.
  *Feeds:* Craft / Apollo Mono. *Status:* parked.
- **"Done" success state — RESOLVED 2026-07-20 (B-D6).** Was on the Legacy teal `#00847F`; now the R-D14
  green fill `rag/success-background` `#5DAC7B`/`#43AD6F` + black label (`text/on-success`). *Status:* done.

### ★ Button-states finesse pass — queued 2026-07-22 (Dave, post-ADR-0013: "not now but note for a follow up")

Raised right after the composition tier landed. **Theme posture stated in the same breath: Legacy
shouldn't change; Mono, Supercharge AND Console are all in design development.** The pass, when it runs:

- **Legacy state MECHANISM fidelity question.** Dave's observation: *"legacy button states seem to be
  using opacity, we just use colours."* ⚠ INTERPRETIVE FLAG for the session that picks this up: the
  as-built HSBC system's states may be OPACITY-based while our Legacy override set renders explicit
  colours (registry `stateMechanism: explicit`, ADR-0014). If confirmed against the real system, the
  faithful reproduction (R-D24 posture — "Legacy shouldn't change" = the DESIGN is frozen, our
  rendering of it can be corrected) may need its mechanism switched to opacity. VERIFY against the
  as-built source first — don't flip on the recollection. *Feeds:* Legacy fidelity.
  **★ THE REFERENCE (Dave, 2026-07-22: "This is legacy… record as the reference"):**
  `https://www.figma.com/design/mI8hvIkV98nquoqWzKh5Kn/HSBC-Common-Toolkit--MCP-?node-id=65884-68326`
  — the Common Toolkit file (same file as Modals' anatomy source, node 65884-68326 = the Legacy
  button states). Deliberately NOT fetched at record time; the finesse session pulls this node
  (Figma MCP / get_design_context) and reads the actual state mechanism + values off it — OBSERVED
  provenance, the ADR-0014 warm-ramp precedent.
- **Supercharge mechanism: keep the opacity OPTION open** — Dave: *"keep the option open for
  supercharge but it probably wont change"* (stays colour by default; the ADR-0014 snap gate already
  permits opacity where it snaps to a warm step, so the option IS structurally open — nothing to build,
  just don't foreclose it). *Feeds:* SC design development.
- **Mono + Console pressed = DARKER pressed fill.** Dave: *"the pressed state for console and mono
  should have a darker press colour for pressed."* Ties directly to the OPEN token gap flagged in
  Button's header since the rebind: tertiary/quaternary have NO background/pressed token (pressed
  reuses the hover tint) — and B-D7 just softened the physics darken to 0.94, so pressed reads less
  distinct than before. Fix space: mint pressed tokens a step darker than hover across the four
  emphasis tiers (primary already flips per-mode `#000000`/`#FFFFFF` — review whether that reads
  "darker" in dark mode). AA invariant per ADR-0009 §4; active > hover per the WCAG state rule.
  *Feeds:* Mono/Console design development.
- **Loader ATOM for all loading states.** Dave: *"there should be a loader atom for all loading
  states."* Button carries a local `.spin` spinner; Loading-indicator exists as its own snippet —
  exactly the ADR-0013 accretion shape: one loader atom (likely Loading-indicator as source), a
  `loader` partial/membership, consumers retrieve it (Button's `.spin` first proof). The ratchet
  census is the discovery tool. *Feeds:* the component-type registry's second group candidate.

*Why held:* Dave explicitly deferred — *"I'm not sure I want to do this now."* *Source:* in-chat
2026-07-22 afternoon, post-ADR-0013 wrap; ledger context `_BUTTON-DECISIONS.md` B-D1…B-D7. *Status:*
**queued (follow-up)** — a natural single session: mechanism-fidelity check + pressed-tint tuner
(review HTML, Dave rules live) + loader-atom accretion.

## Legacy-colour leakage — gate live, RAG green set to COMPLETE (2026-07-20)

The teal-in-Mono leak (B-D6/R-D17) is now guarded by **`_validate_legacy_leak.py`** (build-blocking; seeded
with the ruled teal `#00847F`). It caught **7** teal-binding surfaces; Button is fixed, the other seven are
**waived with provenance** pending the work below.

- **Complete the R-D14 green set, then rebind the 7 — DONE 2026-07-20 (R-D18).** Dave ruled the green set
  on the live tuner (glyph dark `#4A9568`, tints `#DCEDE3`/`#12291D`, bare role rebased). All seven rebound,
  all gate waivers cleared, teal fully evicted from Mono. *Status:* done.
- **Seed the gate with error/warning/info once ruled — roles now RULED (R-D20, 2026-07-21).** The three sets
  are complete + Mono; 6 Mono snippets swept, Notifications waived (Legacy ref). *Still open:* seed the Legacy
  error/amber/navy hexes into `LEGACY_ONLY_HEXES` (needs a Notifications waiver in the leak gate, since it holds
  them legitimately), and flip `_validate_theme_provenance.py` from advisory to blocking — both gated on the
  broader foreign-hex cleanup (58 hexes / 67 files). *Status:* idea.

## ★ Decision-graph — typed edges over the record corpus (ADR-0007's unbuilt half) — tasked to Fable (2026-07-21, Dave)

*Why held:* today's icon-011↔R-D6↔R-D3 reconciliation was done by hand because decision records cross-reference
in **prose**, not queryable edges — so recall = keyword search (consult) and reconciliation = manual archaeology.
Desk research confirmed this is **already decided** (ADR-0007 temporal decision-graph; slice 1 / staleness gate
built) — the missing half is the edge convention + generator + conflict gate. *What it feeds:* Apollo PM layer /
the `_STATE-MACHINE-TARGET` context machine. *The slice:* (1) typed-edge front-matter on ~35 decision nodes
(4 ledgers + 11 ADRs + REVIEW rules): `refines · supersedes · subsumes · bounds · conflicts-with · verified-by`
+ `status` + `validation` (unaudited→vouched); (2) generator → LIVE/DEAD/OPEN ledger + **reconciliation view**
(auto-surface any conflicts-with edge lacking a resolution) + per-node "what-touches-this" map; (3) **conflict
gate** — A bounds/conflicts B with no recorded resolution → build flags it (icon-011 vs R-D6 would have lit up).
*Rejected alternatives:* replicate-across-records (rot engine — denormalise only in generated views); graph DB
(tool-temptation — text-based KG gets 80%, per ADR-0007 + the July-2026 external scan). *Routing:* **Fable, fresh
cold session** (big/high-stakes/hands-off); guardrails — conflicts it surfaces are **queued for Dave's ruling,
not auto-resolved** (promotion is Dave's); open sub-call (author all edges in one Fable sweep vs stop at spec+gate
and hand edge-authoring to Sonnet) decided *after* the audit. *Source:* `_DECISION-HISTORY/2026-07-21-rag-completion-and-decision-graph.md`;
ADR-0007 + `notes/_STATE-MACHINE-TARGET.md`. *Status:* **tasked — next session.**

## Token schema: explicit nullable placeholder slots for anticipated flex (2026-07-20, Dave)

Dave's direction: *"we always have to think about max flexibility and save all possible values for the
architecture… the value can be a value or null, like placeholders"* — refined to *"probably not every
possible parameter but the ones we need to flex; I envisage a style builder in the future."* So: reserve
**explicit, nullable** slots on tokens for the dimensions we anticipate flexing (per-mode already; per-theme,
per-state mechanism, opacity), where `null` = *"slot declared, value not yet set"* — NOT a blanket dense
schema. *Why it fits us:* the teal leak was a **silently missing** dark green; an explicit `dark: null`
placeholder would make that hole machine-visible and let a gate fail any *live-component-bound* token whose
mode-slot is null. Needs: a clear null semantic (undecided vs intentionally-inherit) + that "no null under a
live binding" gate. *Feeds:* the **style-builder interface** (ADR-0009 — where a user configures mechanism +
values per state within the AA guarantee); pairs with `$extensions.apollo.state`. *Status:* **written up → `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md`**
(direction accepted; null-gate + slot rollout staged, pilot = the RAG green set). *Provenance:* this session.

## Side-quests (captured in `_LIVE-STATE` 07-16, now homed here)

- **Research knowledge-graph** — KG over the research corpus (dataviz desk research, nav catalog,
  masthead model, dossiers) so findings are queryable, not stranded. Harvest later; capture
  KG-friendly as we go. *Feeds:* Discover phase / ADR-0007 direction. *Status:* parked.
- **Swiss HTML viewer for the state ledgers** — a rendered, ideally editable face over
  `_LIVE-STATE`/this file, house style. Pairs with the PM-KG direction. *Status:* parked.
- **DataViz method → colleague presentation** — Dave 2026-07-18: "much of it deserves to be a
  presentation to colleagues." Material: the method dossier + V7 sheet + the vibration rule story.
  *Feeds:* Dispatch/advocacy. *Source:* `_DECISION-HISTORY/2026-07-16-dataviz-v7-arc.md`. *Status:* idea.
- **★ EXPERIMENT — isoluminant sweep across the WHOLE base Apollo palette, across the bands** — Dave,
  2026-07-19, during the RAG-colours review: *"run this across the whole base Apollo colour palette,
  across the bands."* Take the isoluminant band method built for RAG red/green/blue (match OKLCh **L**
  across hues, hue held, chroma capped to gamut, WCAG contrast measured vs white / black / `#1A1A1A`)
  and apply it to **every hue family × step** in `knowledge/tokens/colour.json` — re-cut each colour to
  sit at each band's shared lightness, to see how the full palette behaves under intensity-matching.
  **⚠️ Second axis to measure (Dave surfaced it in the same review): HALATION / bloom.** Intensity-match
  is one dimension; edge-extremity is another — *"thin lines and colour dance, thicker ones bloom… that's
  the halation effect."* Bright/high-step colours on the dark ground bloom (fills) or shimmer (thin
  strokes/text). The sweep should carry a bloom/edge-extremity read alongside contrast, tying to the
  existing edge-extremity advisory gate + the digital-black rationale (`color/black` `$note`, memory
  `attribute-the-diff` / `dark-rag-token-gaps`). *Why held:* Dave said "schedule after this RAG stuff" —
  runs once the RAG bands are ruled (R-D6). *Feeds:* Discover/colour-foundations + the DataViz/RAG
  palette work. *Source:* `reviews/_rag_colours_calc.py` (the sweep engine) + `reviews/RAG-COLOURS-2026-07-19-v1`
  review comments. *Status:* idea — queued next after RAG.

## Spin-outs (public-facing, beyond the internal engine)

- **★ SESSION-HARNESS TEMPLATE — the working method as a pro-forma for other teams** (Dave,
  2026-07-23, routing-sidequest session; registered by the conductor per the receipt). Extract the
  harness as a reusable kit: memento format (GOOD-MORNING/_LIVE-STATE spine) · capture ritual ·
  conductor/worker model + receipts · context gauge · MODEL-ROUTING skeleton · review overlay ·
  build-runner shape. Assessment (in the sidequest chat): the invariant + method layers are
  domain-agnostic — Apollo is just the knowledge layer. Likely shape = a **Cowork plugin**. Needs an
  environment appendix (sandbox git dance, window sizes are env-specific) + a Dave-specifics scrub.
  Canonical note: `notes/2026-07-23-harness-framework-spinoff.md` · memory `harness-framework-spinoff`.

- **★ APOLLO LABS — a public a11y / colour-science microtool ("Ally")** — Dave, 2026-07-19, riding off
  the isoluminant + halation work: *"we might just be on the edge of a really cool a11y tool here… spin
  out Apollo Labs as a side project for public consumption, good promotional material for HSBC."* The
  idea: a small public web tool that runs the palette analysis live — paste/import a palette → isoluminant
  band re-cut (match OKLCh L across hues, for CATEGORICAL palettes) **+** **salience-RAMP ordering** (loudness
  descends with hierarchy, for STATUS palettes — Dave 2026-07-19: *"this is good for colour palettes"*, the ramp
  reframe ENRICHES Labs, doesn't retire it) **+** halation / edge-extremity read (bloom on fills, shimmer on thin
  strokes) **+** WCAG contrast per ground. A demonstrable, sharable artefact of serious accessibility
  craft. *Why it matters:* doubles as **HSBC promotional material** (shows the bank leading on digital
  accessibility) and as an external face for the Apollo method. *Feeds:* the **accessibility aspiration**
  (most digitally accessible bank — memory `accessibility-aspiration`, ADR-0004) + Dispatch/advocacy +
  the spin-off-candidates thread (memory `spin-off-candidates`, `capability-gap-and-obsolescence`).
  *Engine already half-built:* `reviews/_rag_colours_calc.py` (isoluminant sweep) — the [[isoluminant sweep
  experiment]] above is the internal precursor; Apollo Labs is its public form. *Guardrail:* portability +
  no licensed-font / brand-confidential leakage before any public release (ties `univers-webfont-blocker`).
  *Status:* idea — spin-out candidate; surfaced mid-RAG, do not gold-plate before the RAG bands land.
  - **★ THE TWO-MODE OKLCh TUNER is the Labs UI prototype (2026-07-19).** Built to settle the RAG light fills:
    `reviews/RAG-LIGHT-FILLS-2026-07-19-v7` — wide saturation + fine lightness sliders **per hue, per mode**, hue
    held, live hex + WCAG contrast + **a ramp-order guard that reds when the hierarchy breaks**, each mode judged
    against its own ground. Dave: *"give me a saturation slider, make it wide so i can fine tune"* → *"i could do
    this for days."* This is exactly Labs' interaction model (paste palette → tune → live a11y read). Also a
    **Layer-2 in-browser control** for the design-time loop generally ([[dataviz-pillar-progress]]). Lesson banked:
    past ~2 colour round-trips, give the eye a live control instead of another static version. Port the OKLCh↔hex +
    contrast + ramp-guard JS from that file as the Labs seed.

## Type / font procurement targets

- **★ Variable Univers cut — target a ~440–460 weight rung** — Dave, 2026-07-19, in the RAG weight rig:
  *"shame there wasn't a weight in between."* The licensed cut is five STATIC weights (100/300/400/500/700 —
  no 600, no 450) and there is no variable-webfont licence, so the 400↔500 gap can't be bridged now. If a
  variable Univers is ever procured, **~450** is the value the halation weight-rule wants for the mid case.
  *Feeds:* the dark-mode weight ruling (R-D7) + brand font procurement. *Ties:* `univers-webfont-blocker`.
  *Status:* idea — needs licence, not ours to force.
- **★ Dual-observer calibration principle (astigmatic vs corrected)** — Dave, 2026-07-19: *"mixed weight
  might be better for me but weird for normally sighted."* Optimising to the most sensitive eye can diverge
  from the typical viewer. The principle: **serve the sensitive observer without breaking the typical one —
  and flag where they diverge.** Directly shapes **Apollo Labs** (report BOTH observers, mark the gap) and
  the weight ruling (polarity as hard token vs soft guideline). *Feeds:* accessibility aspiration + Apollo
  Labs. *Source:* `reviews/RAG-COLOURS-2026-07-19-v4` §W3. *Status:* principle — apply going forward.

## Feature ideas (product, not yet specced)

- **★ Responsive-type policy + TUNER — "curve-snapped" fluid type (Dave, 2026-07-23, chart-revisit
  session 1)** — two riffs, logged not built. **(1) The observation:** responsive components should
  have a per-family SCALING POLICY — *"some components might not be subject to it"* — and a tuner to
  dial it (sibling of the ★★ radius tuner; another theme-builder proto-organ). **VERIFIED state at
  logging (grep 2026-07-23): there is NO fluid font scaling anywhere** — zero `clamp()`/vw/cq-unit
  font-sizes in type.css/canon.css/snippets; type = fixed scale steps; responsiveness = LAYOUT
  collapses only, a mix of `@container` (component width — 8+ snippets, the direction) and `@media`
  (page width — a few, incl. Chart-sparkline; reconcile candidate). Charts are ALREADY exempt by law
  (DV-D02: text must not scale). Dave's floor instinct — **base = lowest step, 12px MEDIUM (500)** —
  matches DV-D05 + the enacted dataviz label snap (12/500). **(2) The idea:** *"could the scaling be
  less 'fixed' — based in the 'curve' of the scale but snap to 4px along the curve"* — i.e.
  container-driven position along the modular curve, QUANTISED to grid steps (fluid-but-snapped, no
  free interpolation). Architecture home if pursued: a **component-type-tier dial** (ADR-0013 — the
  press-physics pattern: families opt in/out, themes can zero it), policy tokens not code. Open
  design questions for a TYPE session (T-D15 candidate): the snap step (pure 4px regularises away
  14px — font-6 breaks the quantum today); container vs page basis as the canonical rule; weight
  behaviour along the curve (12px floor wants 500, larger sizes relax to 400 — the existing
  body-weight rule bounds this). *Status:* logged; needs a dedicated type-tier session + tuner
  sheet; do NOT enact piecemeal — T-D9/T-D12 binding architecture governs any change.
  *Live demo, same hour:* the Q6 sheet itself shipped BOTH failures — a viewBox stretch (specimen
  text + strokes scaling with pane width: accidental fluid type, the banned physics) and 11px
  authored labels (sub-floor, off-scale; `reviews/` isn't gate-globbed so nothing fired) — **Dave
  caught both by eye**; fixed to a 1:1 pin + t-cm-legal metrics (12/400). Also surfaced a live
  **weight seam: proforma labels = 12/500 (the 07-22 snap) vs canon chart axis composite
  `t-cm-legal` = 12/400** — flagged to Dave as chart-revisit Q8; the revisit pass must reconcile,
  and Dave's floor instinct (small sizes want MEDIUM) is one of the two candidate answers.

- **★ Narrative dossiers as a NODE-SET in the decision graph** — Dave, 2026-07-19, right after making the
  dossier a closing-ritual step (1b): *"it might have to be wired into the KB or the state manager or a
  separate graph or something, not sure but it's some kind of set of nodes for sure."* The dossiers
  (`_DECISION-HISTORY/*.md`) are the **why/how layer**: the ledgers/ADRs hold the WHAT (ruling + pin =
  "what" nodes); the dossier holds the reasoning ARC that connects them (why/how = the edges + rationale
  nodes). **Mechanism OPEN** — wire into the KB, the state-manager, or a separate graph; not yet decided.
  Natural fit with **ADR-0007 temporal decision-graph** (memory `pm-knowledge-graph-direction`), the
  **research-KG** side-quest above, and the **graphify** tool (memory `graphify-tool`); the `_capture_gate.py`
  MVP is where the parsing machinery would live. *Feeds:* Discover / PM-KG. *Status:* idea — node-shaped,
  mechanism TBD; harvest dossiers KG-friendly as we write them so the later wiring is cheap.


- **Tiered access to canon commits** — DS-admin → domain-admin → standard; sandbox open to all,
  commits tiered (Dave, 07-05; captured in the derivation-governance amend thread). *Feeds:*
  governance layer. *Status:* idea — set the goal first, the access model falls out.
- **Admin settings surface above the per-mode tier dials** — "non-removable = locked, not hardcoded"
  (Dave, 07-17). *Feeds:* the harness. *Status:* idea.
- **Review-overlay upgrades as product** — row-identity capture (the method debt), image paste,
  dictation, export. *Feeds:* Craft phase — the overlay IS the product surface. *Status:* idea,
  method-debt half already logged in `_LIVE-STATE` OPEN.
  - **NEW (Dave, 2026-07-19): bake the template controls into the overlay** — every review must carry a
    **light/dark toggle** and a **responsive-width slider** by default. Applied by hand in
    `reviews/SMALL-PICKS-DESK-2026-07-19.html` this session; the durable fix is to add both to
    `_review/_review-overlay.html` so `_make_review.py` injects them everywhere (theme toggle needs a
    body-level `.dark`/`data-theme` convention docs opt into). *Status:* idea → do before the next batch of reviews.
  - **★ PRINCIPLE (Dave, 2026-07-20): every review carries a DECISION CONTROL per open choice — the reviewer
    EDITS the choice in place, not a question round-trip.** Dave: *"add a selector and any other controls so I
    can edit the choices rather than us going back and forward, add this as a principle for all review."* So a
    review sheet is a **live editor**: each open question becomes a control (segmented selector / slider / toggle);
    the live specimen, the resolved-token table and the contrast readout all recompute as the control moves; an
    **export block** emits the settled values for the agent to read straight off (no AskUserQuestion loop). This is
    the review-sheet expression of the **μX / in-context edit-mode controls** concept below — the "edit designs" file
    — and generalises [[feedback-live-controller]] from "how-much" feel-dials to *all* open review choices. Controls
    are bounded by the rules (e.g. an "Elevate" hover option is shown **disabled** with the `webf-011` reason, so the
    sheet teaches the constraint while offering the choice). Reference implementation: **`reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v2.html`**
    (segmented selectors for ground/hover/pressed/label + opacity slider + live token table + export). The comment
    overlay stays for anything the controls don't cover. *Feeds:* Craft — the review overlay as product surface.
    *Status:* principle set → fold the generic control-injection into `_make_review.py` / the overlay when the next
    review batch lands; the per-choice control list derives from the decision, the same way the edit-mode inspector
    derives from `<name>.meta.json`.
- **Countdown numeral snap-slider prototype** — a continuous size input (dial 48–200px) that snaps the
  dial to the **4px grid** and the numeral to the nearest **type-ramp rung** (16/20/24/32/40/52). Working
  prototype in `reviews/SMALL-PICKS-DESK-2026-07-19.html` §1 (comment 3). *Why held:* Dave "might be
  interesting to prototype" — generalises to a **responsive-on-grid component** pattern (size once, stay
  on-grid + on-scale at every viewport). *Feeds:* Create/Craft — responsive token binding. *Status:* prototype built, idea for generalisation.
- **RAG colours — settle once and for all (dedicated review)** — Dave 2026-07-19: "we need to settle the
  RAG colours once and for all… a separate review." Ruled values exist (R-D1/R-D3/R-D4 role pairs) but
  three things are OPEN: dark-mode **green** has no ruled value (incumbent #1AA05C fails white text 3.37),
  dark **red/blue as glyph-on-text** fail 4.5 (pass 1.4.11 icons), and the **manifestation** (cell / pill /
  dot / bar) is undecided — the source of the dv-017 confusion. *Feeds:* the RAG token promotion +
  component rebind (after the blast-radius gate). *Source:* `knowledge/_proforma/_RAG-DECISIONS.md`
  R-D1..R-D4 "Still open". *Status:* queued — next review deliverable.
- **Edge-triage interface (Dave, 2026-07-19: "chat might not be the best ux")** — a small purpose-built UI to work
  the compliance graph's **27 unverified `verified_by` edges**, one SC at a time: show the claim (`applies_to`), the
  available axe-core rule (13 are "easy wins"), a verdict (wire a check / already covered by a bespoke gate / bespoke
  needed / n-a), and mark state — persisted back to the graph. The task is per-item, stateful and visual, which is
  exactly what chat is bad at. **This is a sibling of the μX concept** (proximate, task-specific controls; interface >
  chat for repetitive triage) and the natural step-2 after the KG **diagram** (`reviews/KG-COMPLIANCE-DIAGRAM-2026-07-19-v1`,
  built this session — see the gap) → the interface acts on it. *Feeds:* the harness + compliance moat. *Model:* Opus to
  design + decide per-SC; delegate the mechanical check-wiring down; a batched "verify all 27" hands-off pass could be a
  Fable job later (per `MODEL-ROUTING.md` — Fable = big high-trust-at-scale, not iterative triage). *Status:* idea → prototype next if Dave wants.
- **In-context edit-mode controls (Dave's "μX" concept)** — the harness edit mode (post-generation) surfaces a
  component's controls **proximate to the component itself**, as a floating overlay docked to the selected
  component's state — **only** the controls that component exposes, **no sidebar unless absolutely needed**. Dave
  2026-07-19: *"when I select the component very specific controls are surfaced under the actual component selected
  state… the parameters you can change are proximate to the component you are editing."* The panel carries a **grab
  bar** (drag to reposition — the checkered strip in his sketch). This is the real home of the **snap-slider** idea
  above (the review-doc slider was a proxy) and of every per-component control set. *Feeds:* **Apollo Create/Craft —
  the harness interface** (the eventual front-end, cf. iteration-machine mock). *Source:* Dave's sketch +
  message 2026-07-19; prototype at `reviews/EDIT-MODE-UX-PROTOTYPE-2026-07-19-v2.html`. *Status:* prototype built, develop later.
  - **rev 2 (Dave, 2026-07-19): the component is movable too — TWO grab bars.** One grab bar moves the component,
    one moves its controls. Crucially: **no absolute positioning — movement snaps to DOM containers** (the component
    reorders between slots in a layout stack), and **arrow keys ↑ ↓ move it in the stack**. The inspector snaps to a
    dock (below / beside the component) and travels with it. Dave: *"I'd like to be able to move the component too…
    No absolute positioning it should snap to the doms containers and we could use the arrow keys to move it in a
    stack."* Kinship with the **Reorder** component ([[portfolio-interactions-invite]]) — the stack-reorder mechanics transfer.
  - **UNIVERSAL (Dave, 2026-07-19): every component gets this kind of control set** — not just the countdown. In edit
    mode, selecting *any* component surfaces its own proximate controls + the two grab bars (move component in the
    stack · move the controls). The per-component control set is **derived from the component's meta** — its `props` /
    `variants` / sizes ARE the controls (e.g. Button → variant/size/label/icon/state; Tag → variant/size/dismissible;
    Countdown → style/size/max-time). So `components/<name>.meta.json` becomes the source of truth for the edit-mode
    inspector, the same way it already drives the review-spec spread ([[feedback-review-live-variant-spread]]). The
    shared machinery (grab bars, stack reorder, arrow-key move, dock-snap, 4px/ramp snapping) is component-agnostic;
    only the control list changes per meta. *Status:* principle set — build the generic inspector against the meta when the harness UI is specced.
  - **TIERED to the strict↔creative register (Dave, 2026-07-19): the controls exposed depend on the tier.** The several
    tiers that run between **strict** and **creative** each reveal a **different level of controls** — and *only* the
    controls that tier permits. At the **most open extreme, there are essentially no structured controls — just a prompt
    box** for freeform edits; the **tiers below progressively reveal** specific controls (e.g. "just the colour palette"),
    exposing only what's available at that level. Dave: *"at the extreme level there will be no controls really, although
    [there] is a prompt box so you can make edits… in the tiers below it'll reveal say just the colour palette, but only
    the controls that are available to those levels will be exposed."* So the inspector's control set = **(component meta:
    what's possible) ∩ (register tier: what's permitted)** — and at the free end that intersection collapses to the prompt
    box. This is the [[product-shape-flexing-engine]] / [[register-inference-ramp]] governance made visible in the UI: the
    same dials that constrain generation constrain which knobs the user sees. *Feeds:* [[multi-mode-product-vision]] —
    strict / creative / component-dev / explore. **Direction CONFIRMED (Dave, 2026-07-19):** the prompt-only extreme is
    the **most creative / open** end; moving toward strict progressively reveals more structured, permitted controls.
    *Status:* principle captured + confirmed.

- **★ Style-builder interface (Dave, 2026-07-20)** — a UI where a user configures **per-state styling**
  for a component: for each interaction state (default / hover / pressed / disabled) pick the **render
  mechanism** — `colour`, `opacity`, or **both** (Dave: *"we still allow the user to select either or
  both"*) — and the values, all **within the AA guarantee** (the builder only offers passing selections;
  the Mono primary editor already demonstrates this — disabled failing ramp steps + a contrast-clamped
  opacity dial). This is the harness-side home of **ADR-0009** (state styling: colour = universal
  substrate, opacity = optional operational layer). It's a specialisation of the **μX / in-context
  edit-mode inspector** above — the per-state control set derives from the token skeleton
  (`$extensions.apollo.state`) the same way the inspector derives from `<name>.meta.json`; and it inherits
  the **live-controls-in-reviews** discipline ([[feedback-live-controller]]). A fully chromatic mode
  (red default / blue hover / green active) is just an override set the builder edits. Reference editors:
  `reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v4.html` (opacity+colour+AA) and the v5 mechanism-switch
  sheet. *Feeds:* Craft / the harness; the four-theme model (R-D15). *Status:* principle set + ADR-0009
  accepted → build the generic per-state builder when the harness UI is specced; migrate opacity to a
  first-class number token then.
  **→ Widened to a THEME GENERATOR (Dave, 2026-07-21 evening, Phase-0 session):** *"ultimately we will
  build a theme generator from this, maximum flexibility."* The builder's output IS an override set
  (`tokens/themes/*.overrides.json`) — themes are data, the cascade generator renders them, so the
  generator UI = dials over the flex-slot schema. Consequence already enacted: **radius became a semantic
  TIER** (default + control/surface/indicator roles, alias-fallback chain, `layout.json`) because "one
  radius can't be universal — cards differ from buttons"; every future flex dimension should land as
  role-granular slots with a base fallback for the same reason. The alias-aware resolution in
  `gen_theme_cascade.py` (override the base → every role follows; dial a role → it wins) is the
  generator's core resolution semantic, already live.
  **→ Channel dials (Dave, 2026-07-23, in the Q6 dataviz-chrome ruling):** every themable role should
  expose ALL its render channels as generator levers — the Q6 shape (`data/axis`+`data/grid` = snapped
  colour + a declared alpha slot, default 1.0) is the pattern instance: *"creating new themes has many
  levels to pull on."* The Q6 sheet (`reviews/DATA-AXIS-GRID-2026-07-23-v1.html`), the ★★ radius tuner
  (top of file) and the Mono primary editors are all **proto-organs of this builder** — every live
  review controller we ship is a module of it, accreting toward the generator UI.

- **★ Token COMPRESSOR — dispatch-time distiller (Dave, 2026-07-23: "strip out for production code,
  so it's light … might not save much, let me know if this is pointless")** — assessed same day:
  **not pointless, but bytes are the wrong scoreboard** — brotli/gzip already crush token CSS ~85%,
  raw-size savings are marginal. The real jobs, in value order: **(1) SUBSETTING** — a product
  shipping 30 components ships only their tokens + partials (tree-shaking at the adapter boundary);
  **(2) GOVERNANCE** — production artefacts carry PROMOTED tokens only: default-value flex slots,
  unconsumed roles and provisional-agent values stripped — the Dispatch-phase enforcement of
  [[derivation-governance]]; **(3) CHAIN-FLATTENING where flex is dead** — alias hops (component →
  type-group → semantic → default) bake to literals only where the shipped product never flips that
  dial at runtime. The constraint that shapes the tool: **flattening kills runtime theming** —
  `[data-apollo-theme]` switching needs live vars — so the compressor is a DIAL (how much runtime
  flex survives to prod), not a flat pass. Architecturally this is the token-tier instance of
  [[kb-distillation-at-deploy]] and most likely a **stage of the ADR-0008 automated adapters**, not
  a standalone tool. *Status:* logged, unspecced; revisit when Dispatch is real.

- ~~**★ Tiered flex at the COMPONENT-TYPE level — ARCHITECTURE SESSION QUEUED**~~ **GRADUATED
  2026-07-21 (same day, late night #3) → RULED as ADR-0013** — component-type tier carries shared
  VALUES and shared RULES (generated partials); one registry; mechanism lands before Phase-2.
  Original record kept below for the audit trail. *(Dave, 2026-07-21 late
  evening; recorded deliberately WITHOUT exploration, his instruction: "lets not explore now but we
  need to record this and explore later").* The same flexibility the semantic radius tier gives
  (default → role) will be needed **per component TYPE** as well: *"I could imagine that segmented
  controls share the same radius"* — i.e. a type-level grouping (e.g. all segmented controls) sitting
  in the **component token tier**, between the semantic role and the individual component binding, so
  a theme (or the generator) can dial a component FAMILY without touching either the global role or
  each component. His framing, verbatim anchors: **"this will be the same for borders and other
  parameters"** (the pattern generalises across flex dimensions — radius, border, and beyond, so the
  eventual shape is *tiered application in the component token level* as a general schema, not a
  radius feature); **"mono doesn't really need this flexibility, but others might, and the generator
  will"** (Mono stays simple — the tier exists for other themes and ABOVE ALL as generator dials; do
  not complicate Mono's own store to serve it). **The semantic roles as built are FINE ("these are
  fine semantically")** — the component-type tier slots UNDER them, it does not replace them.
  *Open architecture questions for that session:* where type-groups live (token schema? meta?
  a `component-type` axis in the 3-tier stack?); fallback order (component → type-group → semantic
  role → default); how the cascade generator + manifests express type membership; interaction with
  ADR-0010 nullable slots + the token-tier gate. *Status:* **GRADUATED — ruled 2026-07-21 late
  night #3 as ADR-0013**; the open questions above are answered there (registry
  `knowledge/component-types.json` · fallback component → type-group → semantic role → default ·
  ratchet-style gate + selftests). Build = the queued clean-room session per ADR-0013 Consequences.

- **Blast-radius gate v2 — cascade-aware.** T-D13's gate matches selectors structurally
  (class/element presence per file) and gates on the file *set*, so a same-count file *swap* inside
  an acknowledged radius passes, and it doesn't reason about real cascade/specificity. The rigorous
  version parses each file's own CSS and detects genuine size/weight COLLISIONS (the `.tag` 14-vs-12
  case) rather than proxying via file membership. *Feeds:* the type-binding guard-rail. *Status:*
  idea — promote once the v1 has bedded in (cf. consult tool's fuzzy→rigorous path).

- ~~**Harmonise specimen-chrome section labels onto `.spec-h`.**~~ **GRADUATED 2026-07-18** — Dave
  ruled full-strength, no muting (opacity dropped); all 9 files now 12px/opacity-1. See T-D13.
- **Reference files don't uniformly `<link>` canon/type.css.** Found during the harmonisation: only
  5 of the touched specimens link the canon sheet; 4 (Avatar, Links, Selection-controls, Tags) are
  self-contained and can't consume canon classes without re-introducing global blast radius. A
  cold-blooded pass could give every reference file a consistent canon link + local override
  discipline. *Feeds:* specimen-doc consistency. *Status:* idea — not urgent; the specimens render
  correctly as-is.

## Mini chart type ramp — floor 12, ceiling 20 (Dave, 2026-07-23, parked at DV-D08)

- Charts may want their OWN quantised type ramp instead of riding font-5/6/7 — Dave: *"I'm still not
  sure about the scaling; we might have a separate mini font ramp for charts, say floor-12
  ceiling-20, we can explore later."* T-D15-flavoured (curve-snapped quantised type is the sibling
  entry); would supersede the DV-D05 chart bindings if built. Explore AFTER the chart-revisit wave.

## Apollo edit mode — post-generation designer-choice surface (Dave, 2026-07-23, at DV-D09)

- Ruled context for the bar-audit B3: canon defaults are placeholders; a planned EDIT MODE lets the
  designer choose (e.g. series colours) AFTER screen generation in Apollo. Craft-phase surface;
  siblings = the ★★ radius/corner tuner + theme-builder channel dials (the tuner-organ family).
  No spec yet — log intentions here as they accrete.

## Context gauge — Half-2 rebuild OR band re-shape (own session; parked 2026-07-26, dream-pass P6, Dave ruled defer-to-own-session)
The gauge's measuring half (`knowledge/_context_gauge.py`, dated 07-21) has been broken since ~07-21;
every wrap stamps "in-head tally, ESTIMATE ±15%". The sharp edge: the recalibrated Amber band is
**15 points wide** while the instrument's error is **±15%** — "Amber ~55" is consistent with anything
from Green to Red, yet the bands drive real behaviour (Amber blocks new build artefacts, fires the
flush + wrap). The session decides ONE of: **(a)** rebuild Half-2 as a real token count against the
transcript, or **(b)** re-shape the bands coarser than the error (e.g. keep-going / wrap-now).
Evidence + full framing: `notes/_dream/2026-07-26-proposals.md` §P6. Runbook: `_RUNBOOK-context-gauge.md`.

## Standing register elsewhere (pointers, not copies)

- **In-flight targets** — gates-as-a-service · chat-to-KB bot · ingestion done-right: `_LIVE-STATE.md`
  → PLANNED / TARGET STATES.
- **Spin-off / generalisable candidates** — state machine kit · font-audit instrument · real-font
  embedding · cockroach-doc pattern: `_LIVE-STATE.md` → SPIN-OFF section (ruled home).
- **Fable-session candidates** — `notes/_FABLE-BRIEF-consolidation.md` §7 (gate-glob audit, decision
  audit runs, KB structure).

- **★ SPINE COMPACTION — cold-start context bloat (Dave, 2026-07-21 late night #3: "we need to solve
  the bloat of all the context loading up each session").** Measured: orientation costs ~70k (~35% of
  the window) before any work — ~35-40k is the fixed Cowork baseline (bear it), but ~25k is
  `_LIVE-STATE.md` alone (~45k tokens, 633 lines, 8+ PRIOR deltas that never roll off and are mostly
  DUPLICATED in `_DECISION-HISTORY` already). Fix, two parts: **(1) delta retention rule** — LATEST +
  ≤2 priors stay in-file; older deltas relocate to `_DECISION-HISTORY` at capture time (mostly
  deletion; the History pointers already exist) — add to `_RUNBOOK-capture-ritual.md` step 1 + the
  `_capture_gate.py` spec; **(2) cold-read discipline** — a fresh session reads LATEST delta + OPEN
  section only, full file on demand (inscribe in GOOD-MORNING's read-order line). Claws back
  ~15-20k/session. Mechanical, Sonnet-able — fold into the ruling-batch window's enact-queue or run
  as a chore. Related: `memory-compaction-mechanics` (same pattern, repo-side); MEMORY.md index
  (~6k auto-load) is due its own densify pass under the adversarial-densify gate.

## ~~★★ FLOATED~~ ✅ RULED + BUILT 2026-07-27 (#5, cold as instructed) — the gauge must be a THROTTLE, not a thermometer

> **RULED COLD BY DAVE 2026-07-27 (later morning #5), exactly as this entry asked.** Canon now lives in
> `knowledge/_RUNBOOK-context-gauge.md` **§ ★ Half 0b — THE THROTTLE**. Rulings: **(a)** reserve is
> **RING-FENCED ~15%**, sized from the observed WORST overrun (+17), never additive · **(b)** any
> unplanned finding **triggers a re-price + the fork put to Dave** (log-and-stop / narrow / chase
> knowingly) · **(c)** **a new session is a REFILL, not a penalty** — *"we can reset the budget at any
> time by starting a new session"* · **every job is priced and debited**, stated out loud when it could
> move the band (*"like real life"* — the ~10% floor is gone; every overrun on record arrived as steps
> each under it) · **the window is the BUDGET, the BANK is the constraint, and the re-read is a
> ~22% TRANSACTION FEE** on every withdrawal (measured, *n*=1).
> **Enforced (FORM only):** `_capture_gate.py --wrap` now fails a handoff whose `pre-flight:` stamp is
> missing, short of three terms, arithmetically open, or mis-banded against the table — 7 bites + 2 green
> controls, and the bite was proven able to fail. **Honesty of the fill figure and whether a mid-job
> re-price happened are NOT observable and are declared unenforced.**
> ⚠ **The diagnosis below is kept VERBATIM** — it is the evidence the ruling was made on, and the entry
> that had to survive a compaction to be read at all *(see `ds-017`)*.

### The original diagnosis, as floated (2026-07-27 #4 wrap, ~97% fill)

**Dave, at wrap:** *"the pre-flighting needs work, we cant keep hitting red, its a waste of effort."*
**Evidence he's right — three sessions running:** 🔴 ~92% · 🔴 ~63% · 🔴 ~72%. The three-term
pre-flight rule (`fill + job + WRAP`) was inscribed *during* that run and did not stop it.

**⚠ UNRULED — this is a diagnosis and a proposal, not a decision.** Deliberately NOT written into
`_RUNBOOK-context-gauge.md`: that file is canon, this was authored at ~97% fill, and a rule about
not working past your budget should not itself be inscribed past budget. Rule it cold.

**Diagnosis — four points, the last one is the actual finding:**

1. **The estimate prices the job PLANNED, not the job RUN.** Every overrun was an *unplanned finding
   chased mid-job* (ds-016 today; the gauge-failure arc before it). In this project discovery is not
   noise — **it is the most common event**. A pre-flight with no discovery reserve is *systematically*
   optimistic, not occasionally wrong.
2. **It is ONE-SHOT.** Priced at the start, not re-read until wrap ⇒ a 17-point overrun is invisible
   until it is already spent.
3. **There is no ABORT rule.** On finding ds-016 there was a real choice — log it and stop, or chase
   it. Nothing forced a re-price, so it was chased from inside the sunk cost.
4. **★ Hitting Red is a SCOPE failure, not a MEASUREMENT failure.** A better estimate would not have
   saved this session; **only cutting would have.** ⇒ *The gauge has been used as a thermometer — it
   reports how hot you are and never tells you to stop.* **Dave wants a throttle.**

**Proposed shape (his framing, reflected back and confirmed at wrap):**
- a **DISCOVERY RESERVE** as a standing term in the pre-flight, sized from the observed overrun history
  (three data points exist: +?, +5, +17);
- **a finding mid-job TRIGGERS a re-price**, and the re-price produces an explicit **STOP-or-CONTINUE
  decision put to Dave** — not one the agent makes silently at the point where it is already invested;
- ⇒ the gauge gains the power to **CUT WORK**, which is the whole point.

**Sequencing (Dave asked whether to abort the next task — answer: no).** This is a runbook edit + a
ruling, ~10 minutes at the FRONT of the next window; it does not displace ds-016 / the `CTRL` sweep,
it precedes them. Related: [[feedback-context-gauge]] · `_RUNBOOK-context-gauge.md` ·
`_DECISION-HISTORY/2026-07-27-the-index-cannot-see-the-rule.md` (the session that produced the +17).

## ★ FLOATED 2026-07-28 — Memento × JIT context (Dave's idea: "a separate search tool working with good morning")

**UNRULED.** Apply the Tool-Search/progressive-disclosure pattern to the Memento chain itself: **duties
eager, reference deferred** — thin the eager chain to §A + LATEST banner + §C headlines + an LS INDEX,
and retrieve section bodies on demand (extend `_consult.py`, grep is the regex variant). Measured target:
`_LIVE-STATE` standing body **12,694 tk** (reference, not duty) ⇒ chain ~29.7K → ~18–19K, cold fee
~23–24% → ~18–19% (ESTIMATE). Prerequisite before any deferral: strengthen the miss-side gates
(reachability + fail-loud — ds-016 is our signature defect) + instrument section-usage at wrap.
Free symmetry: M10's 28K advisory becomes the demotion trigger (the `auto:N` analogue).
**Full survey + options O1/O2/O3 + risks: `notes/2026-07-28-memento-jit-context-research.md`.**
§C is at cap — entering the board displaces a line; Dave's call.

**UPDATE 2026-07-28 (same day):** Dave confirms the §1 reading and sharpens it twice — modularise the
search (consult CORE + corpus adapters, two-stage refs→fetch) and shift the STATE tier to
more-code-than-prose (LS entries as structured records; index + readable view both GENERATED; prose
retained for the orientation tier — data carries STATE, prose carries WHY). Sequencing delegated
("I'll go with your instinct") with the constraint **"memento working better before working on apollo
again"** — firmness pending read-back. Lane: M-set window (unchanged, M5 mover load-bearing) → wrap
instrumentation → O1′ schema+index → O2′ modular search → Apollo resumes. Detail: note §9.

## 🌱 `_memento-index.json` — 1.1 MB generated artefact vs. reviewable diffs (raised Dave 2026-07-28 #28)

provenance: local_7a4f5e6f-dea7-478b-8b7a-9e1b05d42f7f · 2026-07-28
status: floated

**Observed, not inferred:** GitHub Desktop refused to render the #28 diff ("too large to be
displayed by default"). Measured cause: `knowledge/_memento-index.json` is **1,115,565 B / 1,941
lines**, and **340 lines changed** across the two #28 commits. It embeds GM/LS/archive TEXT so the
Memento door can search it (O2′ #25), so any wrap that edits `GOOD-MORNING.md` or `_LIVE-STATE.md`
rewrites large parts of it.

**Cost is ergonomic, not correctness.** The index is regenerated every build and determinism-checked
(`_build_memento_index.py --check`), and it is NOT in the cold-start read chain. But it makes Desktop
useless for eyeballing precisely the commits most worth eyeballing — the wraps.

**⚠ The obvious fix breaks a standing convention.** Generated artefacts in this repo ARE committed —
`canon/canon.css`, `showroom/`, `guidelines/_rules-index.json`. Gitignoring the index would trade a
convention for diff readability, and would leave a fresh clone with no retrieval index until someone
runs a build. **Options, none ruled:** (a) leave it, accept the diff cost · (b) gitignore + regenerate
on build, and state the fresh-clone consequence · (c) split the embedded TEXT from the index STRUCTURE
so only the small half is tracked · (d) `.gitattributes` `-diff` on the path, so git marks it binary
and Desktop stops trying — the smallest change, keeps it tracked, loses nothing but the diff view.

Author's lean: **(d)** — it is one line, changes no convention, and the diff it suppresses was never
readable anyway. But this is a repo-convention call, so it is Dave's.

## ★ FLOATED 2026-07-29 — sub-agents vs worker lanes (Dave, after #35's wrap: "we never had the chat about sub-agents")

**Note:** `notes/2026-07-29-subagents-vs-worker-lanes.md` (FLOATED; ds-017 path — note + this entry, no GM/§C edit).

**The distinction nobody here has drawn:** a **worker lane** (own window, briefed slice, returns FILES + a commit + a receipt) is modelled, gated and proven — `_lanes.json`, `lane_routing_check` BLOCKING, conductor-commits, DIVVY PLAN. An **in-session sub-agent** (own context, discarded, returns **a message**) has **no model here at all**. ★ **The constraint that matters: a lane hands back artefacts you can verify; a sub-agent hands back prose you cannot — structurally a banner**, against a seven-session streak of *verify against `git log`, never a banner*. Candidate rule if it is ever adopted: **a sub-agent may do the WORKING, never the JUDGING.**

**Why it is live:** #35 spent six trim rounds inside the window whose quality they protected — textbook *context receives conclusions, not working* (the JIT note's doctrine, applied to sessions instead of tools). A sub-agent is **a way to buy a context window without buying a session.**

**Measured floor, n=1, NOT a constant:** a lane costs ~4–6 pts of the conductor's window before it saves anything; #35's whole build was ~12 ⇒ below ~15 pts of mechanical work, delegation loses.

⚠ **PREREQUISITE, and the recommendation: do not rule sub-agents until the BOOT is measured.** If ~17 pts of every window is fixed overhead, that number alone decides whether a fresh context is cheap or ruinous — and no session here has ever measured it. Also unapplied: the pace check (§ ★★ THE THIRD TIER) already decides delegation posture and has never been used for one.

## ⬛ COPIED UP AT #90's 2c EXIT CHECK — four #88/#89 deferrals that had NO standing home

*Homed by ADDITION so #88's banner could roll. Probed first: `drill pass` · `1 of 3` ·
`honest certification` · `presence index` each returned **0 hits** in `_FUTURE-STATE.md` and
**0** in `knowledge/_state.json`. Without this they would have rolled out of live state with the
banner — the exact 07-24 loss the EXIT CHECK exists to stop (6 of 7 deferrals lost, only the one
with a standing home survived).*

- **DRILL PASS IS 1 OF 3, DECLARED NOT CLAIMED** (#87-D1, N=2). Pass 1 landed at #88; pass 2 was
  owed to #89 and did not run. `status: parked` `[born #90 · guards: the drill's own completeness
  claim · until: passes 2 and 3 run, or Dave retires the drill]`
- **THE SWAP IS STILL OWED — ADDITIVE, NOT YET A SWAP** (#89-D1's second half). The prose presence
  index still stands in GM; cutting it in the same motion would be a cut before a probe.
  `status: parked` `[born #90 · guards: the "chain is a SWAP not an ADD" rule against its own
  enactment · until: the probe runs and the index is cut or ruled kept]`
- **ROUTING + HONEST CERTIFICATION STILL UNFIXED** (#88's own declaration, carried at #89).
  `status: parked` `[born #90 · guards: #88's rebuild claim, which is CLAIMED not proven ·
  until: re-proven at HEAD]`
- **`_state.json`'s FIVE UNCONDITIONED ITEMS ARE DAVE'S** — `W-0c` NEXT BUILD CANDIDATES and its
  four siblings have no close condition, so nothing can ever retire them. `status: parked`
  `[born #90 · guards: the store's close gate · until: Dave sets a close condition or rules them
  standing]`

*Source: `GOOD-MORNING.md` ★ PRIOR #88 banner, rolled to `_GM-ARCHIVE.md` at #90's 2c.*

## ⬛ THREE ORPHANED FORKS FROM THE 2026-08-02 DREAM PASS — homed #128 by ADDITION

*Ruled Dave 2026-08-02 (dream pass 4, P6): **"P6 ACCEPTED, addition only — one `_FUTURE-STATE.md`
entry homing the three orphaned forks (two-fetch staleness control · 'fog' charter row · `MEMORY.md`
index-drift gate) with the receipt path as source. Nothing ruled, nothing prioritised."** Source /
provenance: `notes/_MEMENTO-DECISIONS.md#P6 ACCEPTED, addition only` (the 08-02 pass entry) and its
re-check at `#⚠ P6 — HOLDS EXACTLY`. **Probe that made it a fork, re-run at #127 and unchanged:**
`two-fetch` · `staleness control` · `fog` · `index-drift` → **0 hits in `_FUTURE-STATE.md`**, 1 hit
each elsewhere and all four the SAME line — Dave's own ruling to home them. The only surface in the
corpus that mentioned the three forks was the record of the decision to home them. This entry ends
that. **Nothing below is ruled, scoped or prioritised — homing is not adoption.***

- **TWO-FETCH STALENESS CONTROL** — a retrieval that fetches a record twice, from two sources with
  different clocks, so a stale copy cannot corroborate a stale premise. Feeds: Discover (retrieval).
  `status: idea` `[born #128 · guards: nothing yet · until: Dave scopes it or retires it]`
- **THE "FOG" CHARTER ROW** — a charter row for the fixed/flex charter naming what is deliberately
  NOT known, so an absence has a home instead of being re-discovered. Feeds: Craft (charter).
  `status: idea` `[born #128 · guards: nothing yet · until: Dave scopes it or retires it]`
- **`MEMORY.md` INDEX-DRIFT GATE** — a check that the memory index still points at what it claims,
  i.e. the hook and the file agree. Feeds: Discover (memory). `status: idea`
  `[born #128 · guards: nothing yet · until: Dave scopes it or retires it]`

*⚠ Homed, not adopted: three sessions' worth of probes proved these had no standing home, not that
they are worth doing. Priority remains Dave's alone.*

## ⬛ COPIED UP AT #153's 2d EXIT CHECK — two #150 items that had NO standing home

provenance: session #153 · 2026-08-11
status: floated

*Homed by ADDITION so the **#150 delta could roll** at 2d. Probed FIRST, and the probe is the reason
this section exists: `no dry-run` · `write by default` · `token-drift` · `alias-vs-value` each
returned hits in **exactly one place** — `_LIVE-STATE.md:88`/`:92`, i.e. the #150 delta that was
about to roll out of live state, plus the `Last refreshed` chain tail that rolls at the SAME
boundary. Both would have left live state in this wrap, silently. That is the 07-24 loss the EXIT
CHECK exists to stop (6 of 7 deferrals lost; only the one with a standing home survived).*

*⚠ Their three siblings on the same #150 line DID have homes and are NOT copied here: the **16
rag-on-neutral pairs** were consumed by `s151-D2` (moved to the rendering gate, `_LIVE-STATE.md`
#151 delta, which stays live); the **mono hover-wash scoping gap** is residual ③ (Banner-8
hover-wash architecture gap); the **box border** question is residual ④. [[gap-in-record-vs-gap-in-evidence]]*

- **GENERATORS WRITE BY DEFAULT — THERE IS NO `--dry-run`** (declared #150, unfixed). A regeneration
  that heals a gate red also rewrites its target with no way to see the diff first; #150's own
  check-before-remedy slip was caught by hand, not by a flag. Feeds: Craft (generators).
  `status: idea` `[born #153 · guards: nothing yet · until: Dave scopes it or retires it]`
- **THE TOKEN-DRIFT CLASS ITSELF** (declared #150, unfixed). #150 found `semantic-colour.json`
  badge tokens where the **alias and the `$value` disagreed**, a silent drift dated back to
  `s122-D2`. One instance was repaired; **nothing re-checks the class**, so a second alias/value
  split would read exactly as green as the first did. Feeds: Craft (tokens).
  `status: idea` `[born #153 · guards: nothing yet · until: Dave scopes it or retires it]`

*⚠ Homed, not adopted, and NOT ruled: this wrap ruled nothing. Priority is Dave's alone.*

## ⬛ FLOATED #153 — `s153-D1` GREEN / SUCCESS-INK SCOPE: REFLECTED BACK, **NOT CONFIRMED**

provenance: session #153 · 2026-08-11
status: floated

⛔ **THIS IS NOT A RULING AND MUST NOT BE READ AS ONE.** Dave picked *"mirror the two-red law"* from
an option set and the conductor **reflected it back**; he has **not confirmed**. It is recorded here,
in the floated register, and **deliberately NOT in `knowledge/_rulings.json`** — an entry there is a
ruling by definition, and promotion is Dave's alone [[feedback-dont-launder-a-premise-into-a-ruling]].

- **THE SHAPE he indicated:** a **background-keyed fork** for green/success ink, mirroring the
  structure of `s151-D1`'s two-red law (one value on white, another everywhere else).
- ⛔ **THE TWO VALUES ARE NOT RULED AND MUST NOT BE INVENTED.** `s151-D1` fixed
  `#DA1A00`-on-white / `#F6604C`-else for RED; **no green pair has been named by anyone.** Deriving
  one from the red law would be exactly the laundering this entry exists to prevent.
- **What it needs:** Dave's confirmation of the shape, then the two values from him.
  `[born #153 · guards: this entry + the #153 residual ④ · until: Dave confirms or withdraws]`

> ✅ **PROMOTED #155 (2026-08-11, Dave live, ADDITION ONLY — the entry above stands as provenance).**
> Dave confirmed the shape in his own words: *"green is the same as red, this is decided already, dark
> and light in exactly the same contexts."* Recorded as `knowledge/_rulings.json` § `s155-D1` —
> **SHAPE RULED, VALUES STILL OWED BY DAVE** (no green pair has ever been named; deriving one from
> the red pair stays forbidden). This floated entry is CLOSED-BY-PROMOTION, not withdrawn.
> ✅ **VALUES RESOLVED same window (#155 amendment, Dave):** the pair was already ruled at `s144-D1` —
> **`#137F3C`-on-white / `#66CC8D`-else** (Dave named #66CC8D from memory; the record confirms it
> exact). Scope narrowed by Dave in the same breath: **MONO theme ONLY.** See `s155-D1`'s amended
> status in `knowledge/_rulings.json`.

*Prior state of this question: PUT TO DAVE #151 (unanswered) · CARRIED #152 (unanswered) · REFLECTED
#153 (unconfirmed). Three sessions open — the age is REPORTED, never acted on.*
