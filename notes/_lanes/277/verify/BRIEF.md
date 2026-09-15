# LANE CV — BRIEF — verify lane CO, and reconcile it against lane CJ
#277 · 2026-09-15 · same wave · written by the conductor · **model: opus** · READ-ONLY

## Why you exist
A green verifier is not a review (#268, Dave ×3) and a lane agreeing with itself is not evidence. Two independent lanes ran this wave:
- **CO** (`8c80aa2`, `notes/_lanes/277/charts/`) — the mechanical author. Proposes **29** `obeys` edges: chart-line 9, chart-pie 10, chart-bar 10.
- **CJ** (`f84eb78`, `notes/_lanes/277/judgement/RECOMMEND.md`) — independent judgement, never read CO's output.

**They converge on the three drops** (`dv-line-009`, `dv-line-010` → sparkline; `dv-pie-003` → donut-only). **They diverge on scope and on arithmetic.** Your job is to grade CO's claims AND to resolve the divergence with measurement.

⛔ **READ-ONLY. You land nothing and you fix nothing.** Your only writes are under `notes/_lanes/277/verify/`. Corrections are made **BY ADDITION** — you say what is wrong and what the true figure is; you do not edit CO's or CJ's files.

## PART 1 — grade every claim in `notes/_lanes/277/charts/REPORT.md`
GREEN / RED / AMBER per claim, with the command that graded it. Re-drive, never re-read: run the builder, run the gates yourself, open the page. Specifically re-derive:
- The per-file rule counts (10 / 11 / 11 / 19) and the 470 total.
- Each of the 29 `$why` sentences: does the rule actually bind that component, and is the sentence **authored** (a reason) rather than a restatement of the rule text? Name every one that is a restatement. This is the half no gate can see.
- The three declared drops — correct, and correctly declared?
- Schema validation of the three proposed metas including the `$why` requirement.
- CO reports **mutant M9 survived** (a #179-class re-dump passing 19 bites) and that bite 20 now catches it. **Re-run the mutation harness and confirm M9 goes red with bite 20 and green without it.** A mutation test that is not driven is a claim.
- CO's two reported findings: (i) `_rules-index.json`'s `dv-019` row carrying `dv-017`'s sentence; (ii) the export-shape and caps driver reds. Confirm or correct each.
- CO recorded a **brief disagreement** (§7): it did not bake `type.css` into a srcdoc because the page has no srcdoc. Grade the substance — is the #261 label-crop actually enforced on this page, per theme, or not? Drive it, do not read it.

## PART 2 — reconcile CO against CJ (this is the point of the lane)
For each, MEASURE and state which is right, or state that it is a judgement Dave must take:
1. **Scope.** CO proposes three components. CJ recommends authoring **`chart-donut` (11 pie rules), `chart-sparkline` (the 2 spark rules) and `chart-combo` (4 cross-file citations) in the same wave**. `s276-D5` names three components and says "Then STOP and look again." ⚠ Is CJ's Q3 a widening of the ruling, or is it the "look again" the ruling asked for? Say which, plainly, and give Dave the count either way.
2. **The pie/donut polarity.** CJ: the pie meta was *ported from* `Chart-donut.reference.html`, so "does the donut share the pie spec" is backwards, and `dv-pie-003` belongs on the donut alone. CO drops `dv-pie-003` from pie but proposes nothing for donut. Verify the provenance claim against the files and git history.
3. **The family-rule arithmetic.** CO's option (b) = **49** (bar 18, line 16, pie 15). CJ's = **46** (bar 17, line 15, pie 14). ⚠ Note CO's per-component figures exceed the 19 family rules plus that file's own rules in at least one reading — **derive the true numbers yourself and show the working**. One of these is wrong and the review page cannot carry both.
4. **`dv-013` / `dv-015`.** CJ says both bind none of the three (`dv-015` is enacted by `roles.json` `when` predicates and binds the role, not the component). Check it.
5. **The `≤ 5 parts` vs `max 6` conflict** CJ surfaced between `roles.json`/`chart-pie.when` and `dv-pie-009`. Confirm it exists and name every file that carries either number. Do not resolve it — it is ruling-shaped and Dave's.
6. **The capitalisation split.** CJ: `df44e51` created both cases in one wave, `provenance.source` does not align with case, blast radius 29–50 files each, a case-only rename needs the two-step `git mv`. Confirm the blast-radius figure.

## PART 3 — the page, by eye
Open `notes/_lanes/277/charts/REVIEW-charts-2026-09-15-v1.html` in chromium (`source knowledge/_render/seat_env.sh`), screenshot **both themes**, and read it as the person who has to decide from it. Grade: is the recommendation first? Are the options genuinely exclusive? Does any decision card contain a figure this lane just found to be wrong? Is anything clipped at 390px? A page that passes its driver and fails on sight is the #268 failure — say so if it does.

## Deliverable — `notes/_lanes/277/verify/VERIFY.md`
Counts of GREEN / RED / AMBER at the top. Then every claim with its grade and the command. Then PART 2 as a table: claim · CO · CJ · MEASURED · who is right. Then PART 3 with the screenshot paths. Then a short **"what the conductor must change before Dave sees this page"** list — specific, ordered, each item one line.

## Gates and cautions
`python3 knowledge/_validate_kg.py` must be OK · `git status` shows changes ONLY under `notes/_lanes/277/verify/` · never `git stash` · never `gen_kg_edges.py` · never `_build_all.py` · textual span only · stale `.git/index.lock` → `mv` to `.git/_orphan-locks/`, never delete (two lanes hit this today) · one commit at the end, `#277 2026-09-15 — lane CV: …`, `--numstat` in the file.

⚠ Two stray untracked files at repo root (`artefact`, 0 B; `rule?`, 49 B) were created by a shell-redirect accident at 21:33. **Do not sweep them** — the conductor will. Just confirm they are still untracked and unchanged.
