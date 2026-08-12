# #160 — the nine that were never values, and the class that was measured at 2

provenance: 160 · 2026-08-12
status: ruled — `knowledge/_rulings.json` § `s160-D1`, § `s160-D2`

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #160 · banner: `GOOD-MORNING.md` ★ LATEST #160 ·
ledger: `knowledge/_rulings.json` (124 entries — `s160-D1`, `s160-D2` are the 123rd and 124th).*

---

## 1. The palette names were ratified, not renamed

#158 minted three RAG palettes and named them `mono` / `legacy` / `console-supercharge`. #159 carried
the names forward as residual ③ — *"fine for now, may split later"*, Dave's own words in chat, and a
float rather than a commitment ([[memento-three-registers]]).

#160 put the question back to him plainly and he closed it: **"do the rename as is, all good."**
That is `s160-D1` — **the names are RATIFIED AS-IS**, not amended. The enactment is deliberately
small: the three palette `$description` fields and `_themes.json` were amended **BY ADDITION**, with
the was-text kept verbatim, and a `_rulings.json` entry recorded. `_validate_palette_tier.py` re-driven
**rc=0** (re-driven again by this wrap sub: *4 theme(s), 3 palette(s), 38 declared key(s), 75 component
meta(s), 75 snippet manifest(s)*).

**Why it matters more than a name:** the float said *may split later*, and a float that nobody
re-asks becomes a fact by attrition. The ruling does not forbid a later split — Dave said so — but
it converts an open drift into a ratified state with a receipt. The placeholder-names carry ends
here, one session after it was raised.

## 2. The nine snippet fails were never a values question

The carry read **"the 9 snippet fails all await Dave's values [1]"** — Alert ×3 · Badge ×2 ·
Form-layout ×1 · List-items ×3 — and it had been read that way since #158, when the count moved
13 → 9. The session opened by building a controller so Dave could rule the nine values.

**He did not rule values. He found the rule.** *"pLease find this rule, maybe its failing"* — and the
rule was already written: `s134-D1` plus `s151-D1` clause 4. Seven of the nine were **rag-on-tint**
pairs, and `s151-D2` had already moved that class to the **meaning-carrier** gate; the gate was
measuring them under the wrong clause. The controller's export then ruled the shape rather than the
values: **keep ×3** and **badge monoink**.

That is `s160-D2` — **resolved BY INTENT, not by value**. Enactment:

- **seven rag-on-tint pairs migrated to the meaning-carrier gate** (the `s151-D2` motion), with
  breadcrumbs left in `Alert`, `Form-layout` and `List-items`, and `data-carries` declarations added.
  ⚠ **`List-items` deliberately declares `"label"` only** — the `Status-indicator` precedent, not an
  oversight, and it is written down so a later reader does not "fix" it.
- **badge numeral → `rag/text/on-light` `#1A1A1A` in BOTH modes** (5.55:1), **mono-only** via the
  `s158-D1` guards vocabulary in all three override sets. `canon.css` was **REGENERATED, never
  hand-edited** — the whole point of `s158-D1`.
- the amendment Dave added mid-flight, verbatim: *"if there are any reports generated, there should
  still be a soft warning but not a block, I don't care how we label it."* ★ **Nothing was built for
  it** — the mechanism already had it: the 🟡 advisory tier is exit-code-exempt. The honest record is
  *the requirement was already satisfied*, not *a warning tier was added* ([[instrument-without-a-consumer]]).

Snippet gate: **75 snippets, 0 failures** (was 9). Both canon generators rc=0, replayed **in-window**
by the conductor rather than relayed from a sub.

**And the eye caught the instrument, not the artefact.** The first dark shot failed to flip
`data-theme`, so two previews rendered identically; **Dave is the one who said the two previews look
the same.** The re-render, light and real dark, was then approved. ★ A specimen that renders the same
thing twice passes every check the builder can run — the only instrument that catches it is the
person who expected a difference ([[attribute-the-diff]]).

## 3. The write-freedom class was 2, not 15

#158's residual ⑤ carried *"15 argparse scripts unverified"*. #160 measured the class instead of
inheriting the count and got **2** — because **15 was the count of argparse scripts**, full stop,
while the class is *argparse scripts that WRITE on a bare no-args run*. Different unit, different
number ([[measure-dont-convert-units]]).

The remedy is the house pattern, in the house module: `write_gate()` added to `knowledge/_helpgate.py`
beside `help_gate()`, and `_audit_props_axes.py` gated. **Driven, not asserted:** a bare run exits
**rc=2** with a named refusal (*"A bare run is not a stated intention… Pass --write to confirm"*) and
`--write` proceeds. `test_gates.py` gained a bite test **and a mutation control**, both passing; the
conductor re-drove the fence-crossing in-window rather than accepting the sub's word
([[a-new-tier-silently-bypasses-its-tests]]).

⬛ **One EXCEPTION is left open and named: `_gen_titles.py` writes by contract** — the wrap workflow
requires it to write its receipt — so it is ungated. **Dave may rule otherwise**; it is not closed by
this session's judgment.

## 4. What is still open when this closes

- **The full-tree `_validate_state_contrast.py` sweep was not re-run unfiltered.**
  `knowledge/_STATE-CONTRAST-AUDIT.md` currently holds a **4-snippet filtered** artefact (−302 lines
  against HEAD). It is committed as-is with that stated; **re-run before trusting it as the whole-tree
  record** ([[green-tests-cannot-see-scope]]).
- **`test_gates.py` full suite is rc=1 in-sandbox** — ENOSPC inside the 24 mutation-bite `copytree`
  copies, **not** the new cases (both of those pass). Full green is CI's to deliver.
- **The wave.** `s142-D1` is the next window's top item, and the argument for that ordering is this
  session: canon is generated and green, the palettes are named, both `-ink` seats are ruled, and the
  snippet gate reads 75/0. The foundation is clean in a way it has not been for several sessions.

## 5. The environment, again

**ENOSPC n=5.** `/var/tmp/chromium-1234` directories were **present at the opener's `ls` and gone
thirty minutes later** — the sandbox reclaimed them mid-session. The `s160-D2` sub rebuilt a farm at
`/var/tmp/pw-browsers-s136` and rendered fine. The carried **ENOSPC runbook-correction** item recurs
for the fifth time; it is still not fixed, and it is still not this wrap's to fix.

★ **The lesson worth keeping:** *present at the opener* is not *present now* — a disk fact ages
inside a single window, not just between them ([[stale-mount-corroborates-a-stale-premise]]).
