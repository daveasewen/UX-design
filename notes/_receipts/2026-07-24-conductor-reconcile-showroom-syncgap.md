# Conductor reconcile — showroom-sync gap closed (chart-line)

*2026-07-24 ~09:57 BST (date from `date`) · OPUS·high CONDUCTOR window · opener: "reconcile + ONE
commit, then cut the wave briefs per the receipt's divvy plan." · baseline HEAD at window-open:
`dcad460`.*

## TL;DR

The conductor work the opener describes was **already committed this morning** by the prior Fable
window — worker reconcile `07ad314`, wave briefs `dcad460`. I did **not** redo it. But verifying the
committed tree (build + brief audit, per "verify before reporting") caught **one real correctness
gap the prior commits left**: `showroom/chart-line.html` was stale against the sentence-cased snippet,
so `_build_all.py` **failed its own showroom-sync gate on the clean committed tree** — contradicting
the spine's "53/53 green" claim. Closed it with one regenerated file. Build now **verifiably 53/53
GREEN on a clean checkout**.

## What I verified (read-only first)

- `git status` clean at `dcad460`; branch == origin/master; the three lane briefs
  (`2026-07-24-chart-wave-lane{1,2,3}-*.md`) exist and are **substantive + faithful to the divvy
  plan** (models Fable·med / Fable·med / Fable·high; the SIX refinements carried as canon; fences;
  a11y-never-dim-only constraint; read-order). No re-cut needed.
- `python3 knowledge/_build_all.py` on the committed tree → **EXIT 1**, sole failure:
  `❌ showroom sync failed (exit 1) — showroom/ is stale`. Every other gate passed (contrast audits
  0 GATING FAIL, parity, census, radius, blast, behaviour gate).

## Root cause (attributed, not guessed)

`gen_showroom.py` rewrote exactly **one** page: `showroom/chart-line.html`. Byte-cmp: 6 contiguous
bytes inside the embedded base64 payload. Decoded, the delta is a single word's casing —
committed showroom `legend **FILTER**` vs snippet-true `legend **filter**`. This is precisely the
`nam-002` sentence-case fix the ★ LATEST banner records the prior conductor absorbing: the **snippet**
`Chart-line.reference.html` carries lowercase "filter" (verified via `git show HEAD:`), but the
**showroom regen for that edit never made it into `dcad460`**. Classic reconcile miss — source
corrected, generated artefact left behind, so the build gate that guards exactly this drift went red.

## Fix (the ONE commit)

- **`showroom/chart-line.html`** — regenerated (`gen_showroom.py`, "1 written"). Now byte-matches the
  snippet-true payload; showroom-sync gate passes.
- Re-ran `_build_all.py` → **EXIT 0, "✅ all generators ran and the integrity + contrast gates
  passed" (53/53)**.

## Deliberately NOT committed

- **`knowledge/_ADVISORY-SIGNALS.md`** — the build regenerates it and it flips the order of two
  identical-type `unmasked-digits` signals (`40-12-26` ⇄ `00-00-00`). That is the **known
  non-deterministic emitter wobble** already logged in §C·4 enact-queue ("advisory-signals emitter
  stable sort — ordering wobble rode `db36e72`"). Reverted write-in-place (`git show HEAD: > file`,
  per `_RUNBOOK-git-commit.md` — `git checkout` doesn't work under the delete-guard). Committing it
  would just churn noise that re-wobbles next build; the real fix is the stable-sort enact item.

## Provenance correction (memento discipline — inscribe the correction as loudly as the claim)

The prior spine says "build 51→53/53". That was true in the **worker's** sandbox at receipt time, but
the **committed tree** was one un-regenerated showroom page short of green until this commit. Recording
it so "53/53" is now an OBSERVED-true-of-the-committed-tree fact, not an inherited belief. Lesson for
the runbook/next conductor: **after any source edit that a showroom page embeds, `gen_showroom.py`
must ride the same commit** — the showroom-sync gate is the backstop, so run `_build_all.py` to green
*before* declaring the reconcile done, not the snippet build alone.

## State handed on

- Build **53/53 GREEN** on clean checkout · working tree clean but for this receipt + spine note.
- Wave lanes ①②③ remain **ready to open** — unblocked by Dave's eyeball of `showroom/chart-line.html`
  (still the fan-out gate) + optional parallel-safe compare-sheet/mini-ramps solo.
- Commit stack for Dave to push (GitHub Desktop, whole stack): `07ad314` · `dcad460` · **this
  reconcile**. No token/snippet/registry content changed — library stays 65.
