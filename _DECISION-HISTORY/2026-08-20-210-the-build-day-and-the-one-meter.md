# #210 — the build day, and the one Meter

```
provenance: 210 · 2026-08-20
status: observed
```

*Back-links: `GOOD-MORNING.md` ★ LATEST #210 banner · `_LIVE-STATE.md` ⏱ LATEST DELTA #210 ·
`knowledge/_rulings.json` § `s210-D1`…`s210-D5` · `notes/_briefs/2026-08-20-210-meter-categorical-split-impacts-v1.md` ·
the four `notes/_briefs/2026-08-20-210-*` mints and the eleven `notes/_receipts/2026-08-20-210-*` lane receipts.*

---

## Why this session looks the way it does

Dave opened it with a number, not a topic: *"good morning, we have 9 hours to rinse some work out
of these tokens"* — the panel read **All 73% / Fable 86%, resets in 9h04**. That is a session shaped
by a **quota clock**, not by a design question, and it explains every structural choice below: three
fan-out waves instead of one, twenty work subs instead of five, a Fable conductor kept deliberately
thin, and a mid-afternoon *"still loads of tokens… maybe we should do something heavier or long
running"* that bought wave 6 outright.

The interesting part is that a session run to a clock still produced **the first inscribed rulings
since #207** — five of them — and enacted all five the same day.

---

## Finding 1 — two use-cases that look like one object, and the right answer was to keep both

Dave's own words on `ledger` vs `transaction-row`:

> *"they are two separate use-cases. They are intrinsically related and may actually be perametised
> versions of the same larger object. What we need to do is keep them both and park them for a more
> forensic revisit. there are things I want to borrow from each and re-engineer into one system that
> goes from perametised molecule (transaction row) to the ledger organism."*

This arrived as an answer to one of #209's two **existence questions** — and it is a refusal to
answer it on the terms it was asked. The question was "does `transaction-row` deserve to exist given
row 91 was ruled a DUPLICATE"; the answer was "the duplicate framing is the wrong frame, park it".
Row `W-65` carries the park. **Nothing was deleted, nothing was merged**, and the forensic revisit is
a named future object rather than a vague intention.

⚠ The lesson worth keeping: *an existence question is not always a yes/no*. #209 built the review page
that put the two side by side (`reviews/REVIEW-210-existence-side-by-side-v1.html`, row `W-64`) and
the page did its job precisely by making Dave say something neither branch had anticipated.

## Finding 2 — the other existence question DID collapse, and it became five rulings

The second #209 existence question — `limits-meter` vs `Progress-bar`, where the meta already claimed
the use — went the other way:

> *"Maybe we roll them up into a single meter component that covers both concepts… we just have
> progress variants, also I would like the option of the bigger titles… a set of meter variants
> embedded in an organism, in this case a daily transfer limit lock-up"*

That one sentence carried four separable decisions, and the session did **not** inscribe them off the
sentence. It built the proposal first (`81384c7`), asked **eight** questions back, got eight answers
plus *"you got it right on the meter question"*, and only then inscribed:

| ruling | what it settles |
|---|---|
| **`s210-D1`** | ONE Meter. Completes `s173-D1`; ⛔ it does not reverse it. |
| **`s210-D2`** | default title **small** |
| **`s210-D3`** | width is **container-owned** |
| **`s210-D4`** | per-payment dropped from the lock-up |
| **`s210-D5`** | **Option C** — the parents' metas become **thin category aliases** (readings progress / allowance), `role=progressbar` on both |

`s210-D5` is the one that needed a memo rather than an answer: Dave asked for the impacts of the
categorical split before choosing, got
`notes/_briefs/2026-08-20-210-meter-categorical-split-impacts-v1.md`, and replied *"C look sgood to
me, all works"*. **The memo is the receipt for the choice**, and it is why the fold could be enacted
the same hour (`a2e2d2c`) rather than carried.

⚠ What is still open and is HIS: the **parent-snippet disposition**. The memo says the parents
*retire*; it does not name where they go. A wrap does not get to name it.

## Finding 3 — three waves, and the waves got better at being waves

The build day ran **wave 4 → wave 5 → wave 6**, all three briefed by `gen_brief.py` (its 2nd, 3rd and
4th production mints — the generator built at #209 and driven four times since).

- **Wave 4** (`9089e31`, row `W-74`) — the heavy 7 deferred out of wave 3: calendar, tree, cascader,
  splitter, **qr-code**, carousel, image-block. The qr-code lane wrote an **in-lane ISO 18004
  encoder** and then **decoded its own output back from the rendered pixels** rather than trusting the
  encoder — the difference between a green test and a driven one
  [[mutation-tests-the-clause-not-the-feature]]. It surfaced a finding it could not rule: **dark-mode
  QR polarity** is a scanner-compatibility question, and that is Dave's.
- **Wave 5** (`89f8f4c`, row `W-79`) — Layer 2 opened: 3 app shells + 3 page templates + 3 form
  templates + 2 lock-ups. It **proposed the artefact-class convention** (a reference-snippet grammar
  for shells/templates/lock-ups) and then *earned* it in the same wave: the **descender gate caught a
  live shell defect** that the convention's own structure had made visible.
- **Wave 6** (`4e50090`, row `W-84`) — 16 P3 organisms (4 shells + 5 templates + 7 lock-ups). Its
  brief carried **wave-5's seven lessons as binding law**, not as advice. ★ **Lesson 3 still caught a
  THIRD live container self-query.** A lesson written into a brief is worth more than a lesson written
  into a retrospective — but it is worth *less* than a gate, which is exactly what the P-7 finding
  below is about.

**Library 91 → 135** across the day (the wave commits' own counts: `100→107`, `108→119`, `119→135`;
the `107→108` step falls inside a repair commit and this wrap did not re-derive it). **Layer 2 is
COMPLETE except row 124** (the variant matrices), which is deferred to Dave.

## Finding 4 — the same class kept surfacing, and one instance was already live behind a green gate

Two findings recurred across every wave, which is what makes them classes rather than defects:

**`ds-005` — a trim-block's specificity beats a single-class override. FIVE catches** (Sidebar-nav
4/4 clipping with a control, Timeline, Document-row, +2). The remedy is a class choice — which
selector shape wins — and that choice is Dave's.

**`container-type` self-query.** Three in-wave catches, and then probe **P-7** found the class
**LIVE in the gated Layout-utilities**: `.l-split` **can never collapse**, and four templates already
carry workarounds for a behaviour nobody had named. Plus an unnamed Transfer-list instance.

⚠ This is the finding to re-read: **the gates were green over it the whole time.** A class caught
three times inside one day's waves had been sitting in shipped, gated code — the waves did not
introduce it, they made it legible [[green-tests-cannot-see-scope]].

**And P-8 found a GENERATOR defect**, which is a different order of problem: `gen_token_ramp`
**appends its AUTO-TOKENS block inside an HTML comment**. Five files' alpha ramps are dead — including
**Button, with 46 declarations commented out** — and **12 variables are ABSENT** entirely. Nothing
renders wrong loudly; it renders wrong *quietly*, which is the [[dangling-dataviz-var-renders-silent-black]]
shape one layer up. ⛔ The repair is a build, not a wrap's.

## Finding 5 — the CI story was a queue again, and no threshold was moved

The day opened GREEN (`74c59d7`, run 32371619468 — the **third consecutive** green at open). Then the
day's own pushes surfaced a **regen queue**, one layer at a time, each repaired at cause:

`[45]` canon determinism (**the conductor's own serial-set miss, owned rather than attributed**) →
`[3]`/`[107]` blast-radius + graph report → `[40]`/`[50]` AUTO-TOKENS + cascade → icon-source 17
UNKNOWNs + a blast-radius re-seed (diff reviewed) → coverage name-join (8 template metas) + **three
real WCAG SCs added to BOTH mirrored tables** (2.4.2 / 3.2.3 / 3.3.3, rules 35 → 38) → `[115]`
chain-size **TAPE-TIER borderline** (23,055 / 57,443).

⛔ **NO THRESHOLD WAS MOVED.** `[115]` is the [[gate-cannot-pass-in-one-environment]] class — the
chain is measured against a tier that a mid-session tree legitimately exceeds — and the **expected
healer is the wrap's own banner roll**, not a re-based constant. `s208-D1`'s rider is the reason that
sentence is written this way: *"I don't want to move the goals just so the system stops complaining."*

## Finding 6 — what the day did NOT settle

Dave floated and parked, in the same breath, the thing that would have been the most expensive
detour available:

> *"maybe we need to mint a minimum spacing for all interactions (collisions) with text that have the
> line-height trim - lets not think about this right now... any stacked text actually need a
> line-height (or a fake lineheight created by padding)... lets not drill into this right now. we
> need decisions and progress and new components :)"*

Row `W-67` carries it FLOATED-PARKED. ★ **The park is the decision** — a floated item recorded as
floated is not a loose end; an un-recorded one is.

---

## Where it landed

**Five rulings inscribed, all enacted the same session.** Library at **135**. **Layer 2 complete
except row 124.** Fifteen work commits, all pushed and remote-verified at `a581226`. Two probes
registered ADVISORY (`W-85`) with **nothing repaired** — registration is not repair, and the
promotion is Dave's.

**Still open, all his:** `W-63` (the wave-3 nine + ~20 design questions) · `W-65` · `W-66`
classes-half · `W-67` · `W-70` · `W-74` · `W-79` · `W-84` · `W-85` · row 124 · the parent-snippet
destination · the `ds-005` class choice · dark-mode QR polarity · the gauge-constant re-base · the
`[115]` bound · the `gen_token_ramp` repair.
