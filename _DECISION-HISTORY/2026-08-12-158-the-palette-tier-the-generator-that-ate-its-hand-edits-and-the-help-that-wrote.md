# #158 — the palette tier, the generator that ate its hand-edits, and the `--help` that wrote

provenance: 158 · 2026-08-12
status: ruled — `knowledge/_rulings.json` § `s158-D1`, § `s158-D2`, § `s158-D3`, § `s158-D4`

*Session #158, Wednesday 2026-08-12. FABLE conductor + FOUR delegated OPUS build subs + this OPUS
wrap sub, Dave live. Dave's plan ruling, in-chat: **"order by dependencies and fixes/tidying-up"**,
then **"okay lets proceed in your order"** — so the arcs below run in dependency order, not in the
order they were discovered. Spine entries: `GOOD-MORNING.md` ★ LATEST #158 · `_LIVE-STATE.md` ⏱
LATEST #158. Ledger: `knowledge/_rulings.json` § `s158-D1`…`s158-D4` (entries 119–122).*

---

## 1. The tier that was ruled at #157 and built at #158 — and why it needed a gate, not a script

`s157-D2` was ruled off Dave's own eye at #157 (*"no difference between the themes, this isn't bound
properly"*) and deliberately **not enacted** — the gauge said defer, and the brief
`notes/_briefs/2026-08-12-s157-palette-tier-brief.md` was written instead. #158 opened with that
brief in hand and it was **cited, never restated**.

What landed: `knowledge/tokens/palettes/rag/{mono,legacy,console-supercharge}.json`, a `ragPalette`
declaration per theme in `knowledge/tokens/themes/_themes.json`, and — the part that makes it a tier
rather than a refactor — `knowledge/_validate_palette_tier.py`, **six checks A–G**, wired into
`_build_all.py` and CI, each one mutation-proven.

**The why, and it is the reusable half:** sharing a palette by *copying* it is what the corpus
already had — console and supercharge duplicated **12 of 16 rag keys hex-identically** and nobody
could see it. A shared file with no gate is the same duplication with a longer path. The gate is
what makes the sharing *structural*: a theme that hand-carries a divergent palette-owned value now
fails. The four keys that legitimately differ are `-tint` keys, which derive from per-theme grounds
(`s123-D3`) and are therefore **not palette-owned** — they stay in each override set, and the gate
knows the difference. Extending ADR-0014's neutral-DNA tier rather than inventing a parallel
mechanism was the ruling's own instruction, and it held.

**A finding that saved a build:** #145's binds-resolution item — carried as an open instrument gap —
was found **already closed** by `_validate_binds_resolve.py`. It was proven closed **by mutation, not
by reading**, and then *not duplicated into the new gate*. An instrument built to close an
already-closed gap is the [[instrument-without-a-consumer]] defect wearing a build's clothes.

## 2. `s158-D1` — the hand-edits canon.css had been carrying, folded into the generator

The finding first: `knowledge/canon/canon.css` is a **generated** file that had accumulated **20
hand-edited lines** — the `s149-D1` guards, the error-atom no-ops, the badge blocks. Every one of
them was one blind regenerate away from disappearing, and nothing measured them.

Dave ruled it in-window: **fold them into the generator**. The mechanism is a `guards` vocabulary in
the theme override files, emitted by `gen_theme_cascade`; the proof is that all **20 lines come back
byte-identical from the generator**.

**The correction inside the correction.** Two `#524842` value diffs survived the fold and looked like
a regression. They were not: they are **stale generated output**. `s151-D2` had already made
`#AA9B92` the ruled value, and the stale pair measured **2.12:1** against the ruled value's
**7.01:1**. So `canon.css` was updated to the ruled value rather than the generator being bent to
reproduce a dead one — [[invariant-cannot-discriminate-reversal]]: the file agreed with itself and
was still wrong. ⚠ **Declared and not smoothed: Dave has NOT eyeballed the supercharge-light pressed
grey that this swap changes.**

## 3. `s158-D2`, `s158-D3` — two seats, ruled in three words each

- **`s158-D2`** — Dave: `rag/success-ink` is **canonical** for the positive seat. `amount-display`'s
  positive amount re-keyed accordingly.
- **`s158-D3`** — negative → `rag.error-ink`. This **supersedes `s157-D1`'s "unchanged"**, and it is
  recorded **by addition**: `s157-D1`'s text stands verbatim, `s158-D3` names what it replaces
  [[header-wins-over-audit]].

Both seats sit on **mono-only rungs**, so non-mono coloured monetary text remains **unruled** and is
declared as a fall-through rather than quietly inherited [[fall-through-class-declare-what-you-mean]].

## 4. `s158-D4` — Option B, and the discipline that made the trim safe

Dave picked **Option B**: the three theme override files shed the **36 palette-owned keys** they were
hand-carrying. The mechanics are the whole lesson:

1. the `$notes` on those keys were relocated **verbatim, BY ADDITION, first** — **36/36 verified**;
2. only then were the keys removed;
3. `canon.css` came out **md5-identical through the trim**, which is the proof that the removal was
   a de-duplication and not a behaviour change;
4. `--strict-absence` went **36 → 0**.

[[home-by-addition-then-cut]] in one move: probe, home, verify, *then* cut. A trim that is one motion
cannot tell a duplicate from a sole surviving copy.

## 5. The write-on-`--help` class finally got a gate — and the probe that found it broke something

#157 recorded `gen_showroom.py --help` performing a full repository write as *"the (n+1)th instance
of its class"*. #158 gated it: `knowledge/_helpgate.py` is a shared `help_gate()` shim, and
`knowledge/_validate_help_gate.py` is an **AST** check wired early in `_build_all.py`. **52 offenders
measured, 107 scripts guarded**, the mutation red quoted in the sub's report.

⚠ **The incident, disclosed rather than buried.** The probe sweep that measured the offenders ran
**real subprocesses**, and those subprocesses **stripped `external_automatable_refs` from 32
compliance files**. It was reverted **file by file from HEAD** — not with a bulk checkout — and a
`.git/index.lock` was cleared via the delete grant. The general form: **a probe that drives the real
thing is the only probe that proves anything, and it is also the one that can write.** The AST check
that shipped is precisely the instrument that makes such a sweep unnecessary next time.

⛔ **What this does NOT close:** the **no-args** leg. A bare `python3 knowledge/gen_*.py` still writes
by default, **15 argparse scripts are unverified**, and there is still no `--dry-run`. The standing
home in `_FUTURE-STATE.md` was amended by addition to say exactly this
[[green-tests-cannot-see-scope]].

## 6. `s149-D1` enacted at the SOURCE, and the wash guards that keep it mono-only

`s149-D1` had stood **RULED NOT ENACTED** since #149. It is now enacted where it belongs — in
`knowledge/snippets/Banner.reference.html`, the *source*, not in the generated CSS: mono error ink
becomes the on-light dark value, with **white 8% / 14% wash** at medium.

Mono-only is held by **three new wash guards per theme**, which preserve the ink-derived 14%/22%
washes for legacy, console and supercharge. The snippet gate moved **13 → 9**: **all four Banner reds
cleared**. The remaining nine — Alert ×3, Badge ×2, Form-layout ×1, List-items ×3 — **all need Dave's
values** and are not a gate defect.

⚠ **Declared unproven:** the wash *medium* is this sub-team's **reading of `s149-D1`'s text**.
Arithmetic corroborates it; **Dave may veto it once it is rendered.**

## 7. What this session did NOT do, and it is the top of the residual

**No specimen was rendered.** Three things landed that only Dave's eye can accept — the `s158-D3`
seat, the `s149-D1` dark-ink banner with its white wash, and the supercharge-light pressed grey —
and **none of them was seen**. That is not a shortfall discovered at the wrap; it is a priced
consequence of a four-sub build session, and it is written as residual ② rather than implied.

And `gen_canon_components --check` is **RED (rc=1, re-driven by this wrap sub)** on **four
pre-existing non-Banner hunks**: the tabs badge comment, selection-controls (one error-atom form +
three comments), and an amount-display block where **canon is BEHIND the `s157-D1` snippet**. ⛔ **A
blind regenerate would UN-ENACT ruled text**, so this is one reconciliation lane with a **per-hunk
canon-vs-snippet decision**, not a `--check` to heal. It is residual ①.

---

## Resolved state

`s157-D2` **ENACTED** with a six-check gate · `s158-D1`…`s158-D4` **RULED AND ENACTED** ·
`s149-D1` **ENACTED AT THE SOURCE** · the write-on-`--help` leg **GATED** · `_rulings.json` **118 →
122**, priors parse-equal at each splice.

## Still open

The four `gen_canon_components` hunks · **every one of this session's three visual changes is
UNVERIFIED BY DAVE'S EYE** · the wash-medium reading · the nine snippet fails awaiting Dave's values
· palette **names** (fine-for-now, may split later — Dave's) · non-mono coloured monetary text ·
the **no-args** write-freedom leg and its 15 unverified argparse scripts · the `none`-unbound delta.
