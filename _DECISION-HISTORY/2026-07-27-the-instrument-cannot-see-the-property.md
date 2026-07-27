# The instrument cannot see the property — the KG exploration, and the hit-area rule that its own mechanism switches off

```
provenance: local_b8238b6c-a0b0-4ceb-a58d-3ab5605e428b · 2026-07-27
status: observed
```

*Session: 2026-07-27 later morning #3 (Opus 5, solo self-conducting, effort MAX). Opened as exploration
beat 1 of Dave's FLOATED KG forcing-function idea — deliberately NOT a build. Spine entry:
`_LIVE-STATE.md` ⏱ LATEST. Defect record: `knowledge/_DS-IMPROVEMENTS.md` **ds-015**. Held ideas:
`_FUTURE-STATE.md` § "forcing the KG into the decision loop" → **Exploration beat 1**. Sibling arc,
same day: `2026-07-27-the-gate-that-narrowed-its-own-rule.md`.*

---

## Why this session existed

Dave floated it the session before, holding the evidence: he had supplied the governing fact from the KG
(*"the gap is only 2px minimum, this is in the dataviz specifications in the KG"*) after I recommended a
mechanism without consulting it. His words: *"we may create something that will force decisions to check
that KG… you will have to explore the benefits, method and implications with me."*

**The instruction was explore, not build.** That constraint held all session and is the reason this dossier
records findings and framings rather than an artefact. Two things were enacted; both are reversible and
neither pre-empts a ruling.

## Finding 1 — the consult's denominator lies, and that is the smaller half

The prior handoff flagged that `_consult.py` "truncates by default". Bite-tested it. It is worse than
truncation, because of *how* it reports:

```
rulings (5/5 shown, --all for more)
```

`5/5` is **shown / CAP**, not shown / total. `_consult.py:200` truncates the bucket, `:217` then counts the
*truncated* list — **the true population is discarded before it is ever printed.** So the string reads, to
a human and to an agent, as *"all five of five"*. Measured true totals: 28, 38, 54.

| query | rulings shown/true | worst bucket | share of bytes seen |
|---|---|---|---|
| stacked bar segment separation | 5 / 28 | advisory 5/38 | 22% |
| button press physics | 5 / 28 | advisory 5/54 | 17% |
| type composite binding | 5 / 38 | **blocking 5/16** | 18% |

**Blocking rules truncate too.** An agent obeying "consult before designing" can see 5 of 16 things that
will fail its build, under a header that reads complete.

## Finding 2 — the enforcement column is a keyword guess printed in the grammar of fact

`enforcement_for_rule()` decides gated-ness by **keyword overlap between the rule's text and the gate's
text/glob**. It never opens the gate's implementation. Output is `gated by <script> over <bite>` — the same
confident shape whether the gate enforces the rule or merely shares vocabulary with it.

Measured: **54 BLOCKING rules · consult claims a gate for 25 · of those, 10 are named in no `.py` file
under `knowledge/` at all.**

⚠ **Stated honestly at the time and repeated here:** "no literal mention" proves *unverified*, not
*unenforced* — a gate may enforce a rule's substance without naming its ID. That is precisely ADR-0016's
CLAIMED/UNPROVEN distinction applied to my own measurement, and it is why the next finding matters: it is
the one case that was run to ground.

**In fairness to the tool:** its own docstring is candid — it says *"possibly gated by"* on fuzzy matches
and calls this *"the gate-glob-coverage question, answered per-query."* It was built as a hint and is a
good hint. The defect only becomes load-bearing under Dave's proposal, which would promote the hint to an
authority. **A design-intent problem, not a bug** — which is why the call is his.

## Finding 3 — `icon-005`/`aid-009`, and Dave turning the exhibit into the finding

I offered the worked exhibit: the consult says `icon-005` ("functional icons need a minimum 44×44px target
area") is *"gated by validate-icons"*. `_validate_icons.py` byte-matches inline SVG **path data** against
the icon library — it cannot evaluate a target area. Wrong gate; the word "icon" in both is the whole basis
of the attribution. The real 44×44 check lives in `_validate_a11y.py` and is a **warning**; the actual
hit-area gate is still *PENDING DAVE SIGN-OFF*.

**Dave then said the thing that reframed the session:**

> *"so the 44px rule is negated by the hit area mechanism, maybe we are checking the wrong thing"*

He was right, and reading the code made it sharper than his phrasing. The check does not mis-measure the
expander. It **skips**:

```python
# an explicit hit-area expander for THIS selector exempts both tiers
# (static CSS can't size the expander; the render axis owns that check)
if re.search(re.escape(sel) + r'\s*::(before|after)', s):
    continue
```

**Adopting the correct mechanism is what removes a component from the check.** And it defers to a "render
axis" that does not exist — the handoff has no receiver.

Measured across the corpus, reproducing the gate's own regexes: **67 snippets · 1,869 selectors skipped by
the `CTRL` vocabulary · 14 eligible · 7 exempted · 7 actually measured.** Verdict: 0 failures, exit 0.
64 of 67 snippets use `::before`. **Library-wide hit-area compliance rests on 7 measured selectors.**

**The diamond is the proof, three times over.** `.dv-leg-sw.sw-diamond` is `8×8px` + `rotate(45deg)`, its
target on `.dv-leg-sw::before{min-width:var(--hit,44px)}`:

1. **Scope** — `.dv-leg-sw` does not match `CTRL`. Never examined. *(Same hand-maintained-vocabulary class
   as the `dtype in ("donut","pie","stacked")` fork behind ds-014. `dv-vocab` closed that for dataviz
   only — **`CTRL` is unswept.**)*
2. **Parse** — the expander is `min-width:var(--hit,44px)`; the regex reads literal `(\d+)px`. It cannot
   read a token.
3. **Exemption** — `::before` present → `continue`.

⚠ And the defect this hides is a **transform** consequence — the rotation stood the 44px target on its
corner. **No static box measurement can see that in principle.** It was caught by `elementFromPoint` at
render, by hand, during the legend wave; that snippet's own comment records *"the divvy did not name it."*

## The generalisation — instrument fit is a THIRD axis, not a sub-case

The important negative result: **angle (1) of the FLOATED idea would not have caught this.** Angle (1) is
*compare what a rule SAYS against what its gate DEMANDS*. Here the rule says "target area", the gate says
"target size". **The vocabulary matches. The narrowing is not in the words — it is in the instrument.**

A static regex can observe a *declared box*. The rule is about a *target*. The two stop tracking each other
the moment the property is expressed through a mechanism — an expander, a token, a transform — and the gate
**goes quiet rather than red**.

⇒ The question to ask of every rule: **"what property does this rule name, and can this gate's instrument
observe that property at all?"** Instruments weakest→strongest: static parse → DOM read → render+hit-test →
human eye. **A gate whose instrument is weaker than its rule's property is inert by construction, however
well written.**

⇒ **This sits on top of ADR-0016, not inside it.** PROVEN/CLAIMED/UNPROVEN ask *"is there a check, and can
it fail?"* Instrument-fit asks *"is it looking at the right thing?"* — **a check can be PROVEN and still be
measuring a proxy that does not track its rule.** dv-004 (this morning) was the *narrowing* case; `aid-009`
is the *instrument* case, and it is the larger one.

## Dave's second reframe — the propagation defect, and the best angle yet

> *"we are relying too much on my memory here, the hit mechanism should have triggered something that
> cascaded this elsewhere."*

Correct, and it names something none of the four held angles did. Adopting the `::before` expander is a
**local CSS decision with a global governance consequence** — it silently removes the component from
`aid-009`'s sample. Nothing carried that fact anywhere: no registry entry, no re-check, no flag on the rule.
**The only thing connecting adoption to exemption was Dave remembering the mechanism existed.**

Sibling of the assertion-propagation gap (*a gate fires on FLIP, so a doc known-wrong-now is never chased*).
**Here the gate never fires at all, because the adoption IS the exemption.**

⇒ **Design implication:** the trigger should not be a periodic sweep — it should be **adoption-time**. When
a component takes up a mechanism that changes which gate can see it, *that* is the event that must cascade.
Cheapest first cut: the mechanism is already a marker in the CSS; make claiming the exemption require naming
the rule it exempts from, and let the register harvest the claim. **An exemption that must declare itself is
an exemption you can count.**

## Enacted (two, both reversible, neither pre-empting a ruling)

1. **`_validate_a11y.py` — the silent `continue` now warns.** Exemptions declare themselves and can be
   counted: **6 → 13 warnings, 0 failures, exit 0, build 58/58 green.** Carries an **anti-false-fix block**:
   do NOT "fix" this by deleting the exemption and failing those selectors — they are not known
   non-compliant, they are known *unmeasured*, and a static parse cannot tell the difference. That would
   trade a blind pass for a blind fail.
2. **`_RUNBOOK-context-gauge.md` — the pre-flight now has three terms.** See below.

## The procedural finding — Dave priced the instrument

Mid-session, at Amber: *"be careful with the tasks amber is close to wrap-up, and remember that it self
consumes tockens too."* Then: *"can we encode a pre-flight mechanism rather than loosing it in this chat."*

The PRE-FLIGHT rule was already inscribed (ruled earlier the same day), so it was not re-litigated — what
was missing is the **meta-cost**. Instruments are not free: the task list, the gauge confirmation, the
consult, and above all the ritual. **Evidence already in the record:** the previous session priced its
render job correctly (38 + 15 = 53, and it held), then ran the **ritual unpriced** — +5%, taking a true
Amber 58% to Red 63%, which is why that handoff's band had to be corrected at close. *The rule was obeyed
for the work and skipped for the instrument.*

⇒ Inscribed as the mechanism, one line:
> **A pre-flight estimate that does not include the wrap is not a pre-flight estimate.**
> `fill + job + WRAP (~5%) = projected band` — always three terms, never two.

With two biting consequences: **reserve the wrap before starting the job** (at Amber the honest question is
never *"can I fit this job?"* but *"can I fit this job AND the ritual?"*), and **instruments are subject to
their own bands** — except reading the band table, which costs a grep and whose omission has caused a wrong
band twice.

**This session then applied it to itself:** at ~58% with a ~5% ritual outstanding, the instrument-fit
tagging pass (a build) was cut rather than started. That is the rule working as intended, on the first
window after it was written.

## What I got wrong, and one thing I got right by checking

- **Nothing was mis-asserted this session, because the recommendation went through the consult first** —
  the explicit remedy from this morning's arc (*consult before RECOMMENDING, not just before designing*).
  First time that ordering was followed unprompted; recording it so the next session knows it is cheap.
- **I nearly overclaimed on Finding 2.** "10 blocking rules with no gate" is `unverified`, not
  `unenforced`, and the distinction is the whole of ADR-0016. Caught before presenting, stated in the
  presentation, and repeated in ds-015's severity caveat.
- **Corrected a stale figure in the handoff prose within the first two minutes:** the ★ LATEST banner said
  register `PROVEN 4 / UNPROVEN 52 of 76`; the generated file read **54 of 78** — DV-D14 and DV-D15 were
  inscribed and the register harvested them. The banner was authored before that run. **Exactly the class
  the RED ~63% stamp told the next reader to re-verify, and the stamp worked.**
- **Verified rather than accepted a standing claim:** Dave was 90% sure Claude could rename the chat window.
  Searched the loaded and deferred tool sets — no rename tool exists (`session_info` is read-only). The
  runbook's step-4b claim stands, now re-verified 2026-07-27 rather than inherited.

## Open — all Dave's

1. Does **instrument fit** join the register as a third axis, or stand as its own check?
2. Is the trigger **adoption-time** or sweep-time?
3. The **instrument-tagging pass across 465 rules** — mechanical, would rank the whole corpus. NOT started,
   deliberately: it is a build and the window was capped.
4. **Fix or remove the consult's enforcement column** — a wrong "gated by" is worse than no column. Fixing
   the `5/5` denominator is trivial and separable.
5. **`CTRL` is an unswept vocabulary** — the `dv-vocab` fix pattern applies directly and has not been run
   anywhere but dataviz.
