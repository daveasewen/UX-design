# #162 — the last unruled row, and the flip that was already there

provenance: 162 · 2026-08-12
status: ruled — `knowledge/_rulings.json` § `s162-D1`

*The WHY and HOW of session #162. The WHAT lives in `knowledge/_rulings.json` (`s162-D1`),
`knowledge/components/tooltip.meta.json` (the `tip` row's `$status`), the ★ LATEST banner in
`GOOD-MORNING.md` and the ⏱ LATEST delta in `_LIVE-STATE.md`. Both-way links: those entries point
back here; this file points at them.*

---

## 1. The session had exactly one job, and it was not a build

#161 closed with a finding rather than a task: the `s142-D1` three-axis wave had been **fully enacted
at #143**, two sessions before anyone wrote down that it was owed. A build sub re-derived it row by
row — 113 of 114 rows already carried a `$status` naming the ruling — and what remained was **one
row, `tooltip.tip`, and Dave's word**. #162 opened on that and nothing else.

The arc matters because the shape of the work inverted. There was no enactment to plan, no gate to
repair; the only instrument that could close the item was **Dave's eye on a rendered artefact**. So
the session's real question became: *what does he have to SEE in order to rule?*

## 2. What was built to make the ruling possible

`reviews/REVIEW-tooltip-tip-s162.html` — both edges (`top` and `bottom`), light **and** dark, with
the snippet's CSS carried **verbatim** rather than re-authored for the review page. That last detail
is the load-bearing one: a review page that re-writes the styles it is reviewing is a specimen of
itself, and a ruling made on it would be a ruling about the review page.

## 3. The finding that changed the question

While preparing the specimen, the reviewed snippet turned out to be **space-aware**: it already
flips above/below at runtime to fit the viewport, the same mechanism by which it shifts along the
edge to accommodate a long message. So `tip` was never a *style* choice waiting for a token — it was
a **runtime preference the component already overrides when the geometry demands it**.

This is the whole reason the ruling could be made on sight and did not need a values debate. Dave
saw the two edges, and then said, verbatim:

> *"so yes, the tooltip should flip if there is no space to display it in the same way as it moves
> from the edge to accommodate the message"*

and, after the read-back:

> *"this a behavior that will be constant across all themes, i don't think this needs tokenizing"*

★ **The read-back happened BEFORE the ruling was recorded**, which is the discipline that keeps a
paraphrase from becoming a ruling.

## 4. The dead end that wasn't taken

The obvious cheap path was to classify `tip` from the manifest — an enum with two values and no
colour looks like a structural param on paper, and the class would have come out the same. It was
not taken, because *the same answer for the wrong reason is how a class gets mis-set later*. The
distinguishing fact (the runtime flip) is only visible in the rendered component, and it is now
written into the `$status` so the next reader does not have to re-derive it.

## 5. Two corrections the session produced as a by-product

**(a) A carried repo-state claim was false.** #161's record said the wraps `6726a2a` + `ee091ef` were
NOT pushed. The remote already had them — the pre-commit ahead-count was **1**, not 3. A "not
pushed" line is a claim about a *remote*, i.e. about a clock this window does not own; it goes stale
the moment Dave touches GitHub Desktop and nothing in the ritual re-tests it. Recorded as a
measurement. **No gate was invented for it** — that would be a ruling, and rulings are Dave's.

**(b) The msgfile-prefix class recurred, instance 8, and the trigger was new.** The first T3
invocation **refused** (`--all-dirty` missing). The retry reused the *already mutated* msgfile, so
the generated `after #N <date> —` prefix was applied twice (`6e0ed57`), repaired by an amend from a
fresh `printf` while the commit was still unpushed. The standing rule already said "a fresh msgfile
per invocation"; what it did not say is that **a REFUSED invocation is still an invocation, because
it still mutated the file**. That is the sentence the hook now carries.

## 6. What is resolved, and what is still open

**Resolved.** `s162-D1` is recorded; `knowledge/_rulings.json` runs 128 → 129; the `tip` row carries
its `$status`; the snippet, binds-resolve and palette-tier gates were re-driven green (75/0 · 0 fails
· OK); the ruling commit `0fa5f8f` is committed **and pushed on Dave's explicit word**. The
`s142-D1` wave closes at **114/114**.

**Still open, and named rather than smoothed.**

- **The wave's value-level aesthetic leg.** Only *tooltip* was rendered and seen. 113 rows remain
  unseen, and only Dave's eye can close them.
- **G18.** Explained with five measured live hits, flip-to-block recommended — **he has not ruled**.
- The ENOSPC fence, re-measured at **n=7** (`/` 97%, foreign-owned `/var/tmp` dirs undeletable, the
  `--target /var/tmp/pylibs-s162` recipe held). It produced **no new fact**, so the runbook was not
  amended — a re-measurement is not an amendment.
