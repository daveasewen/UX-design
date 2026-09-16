# FABLE CHECK — the #277 Opus wave, re-driven by the conductor (Fable 5.1)
2026-09-16 · Dave: *"you've been on opus for a while by mistake, I'm not sure I trust its judgement, I've switched to fable, can you check its work please"* · READ-ONLY, nothing changed, by addition.

## What was checked, and how
Every mechanism the 29 `$why` sentences name was grepped in the three LIVE metas (`knowledge/components/chart-{line,pie,bar}.meta.json`), not in the proposals. The 47-cell family matrix was re-derived by importing lane CP's builder (its rebuild was byte-identical to `66fdc49` — `git status` empty). The pie/donut polarity and the 5-vs-6 conflict were read from the file. Lane IX's byte-match claim was checked against `knowledge/_validate_icons.py` (exists, is a path-data match, promoted gate since 2026-06-24).

## Verdict
**The three decisions stand as posed. Two `$why` sentences are wrong on mechanism and must be reworded before any land lane splices them. Three Opus seats (CO, CV, CP) let both through — CV caught `dv-bar-002` and `dv-pie-001` and missed these.**

### RED — 2 of 29
| edge | what it says | what the file says | fix |
|---|---|---|---|
| `chart-bar` → `dv-bar-001` | "this meta's optional `title` prop" | **there is no `title` prop** on `chart-bar` (props: orientation · series · sort · data …). A title exists only as a TYPE ROLE — `tokens.font-family` line 33 routes `title` through `.t-cm-section-label`. | *"A title that reflects the main insight is the slot `tokens.font-family` types as `.t-cm-section-label`; the rule is why that slot is typed at all rather than left to the author."* |
| `chart-line` → `dv-line-005` | "the reason `responsive` pins the viewBox 1:1 rather than rescaling intervals" | the 1:1 pin is DV-D02's **text-never-scales** mechanism (`responsive.rule`, line 100). It says nothing about measurement intervals. A true-sounding sentence with no binding in it. | *"Comparable intervals and a gridline density the author may drop when it confuses is TASTE the meta hands to the author; the meta's `series` cap of 1–5 on ONE continuous time axis (`when`) is the only structural trace, and it is thin — this edge is the weakest of the nine."* — or **drop it and declare the drop**. |

### AMBER — 1
`chart-line` → `dv-line-019`-class question: `dv-019` (vibrating boundaries) is held OFF chart-line in the matrix. Adjacent saturated near-complementary *strokes* can vibrate too. Defensible either way; not re-opened.

### GREEN — everything else re-driven
- 27 of 29 `$why` name a mechanism that is in the file: `series` marker geometries, `legendFilter`, `dvTip` in `motion.hover`, the `dv-line-011` / `dv-bar-007` / `dv-bar-009` / `dv-pie-009` / `dv-pie-010` antiPattern citations, `labelling` spider/direct, `slices`, `valueMode`, `orientation`, `.dv-barkey`, `.t-cm-chart-label` 12/500, DV-D02, the `chart-combo` yield (`edges` line 238).
- The three drops (`dv-line-009/-010` → sparkline, `dv-pie-003` → donut) are right on the file.
- D-2 polarity: `chart-pie.meta.json` line 4 *"ported from Chart-donut.reference.html … inner radius dropped to 0"*; line 16 yields to `chart-donut` for a centre total. CJ's reading holds.
- Family matrix: **47 = bar 17 · line 15 · pie 15**, re-derived; the two settled cells (`dv-008` pie — `responsive.rule` says `.dv-stage` scrolls; `dv-015` line — a between-types rule) are right; `dv-013` on bar is a real judgement call, correctly left to Dave.
- 5-vs-6: `chart-pie.meta.json` line 16 `parts ≤ 5`, line 25 `Maximum 6 (dv-pie-009)`. Real, and correctly flagged not resolved.
- IX: the join is structural. Not re-derived to the pair count; the method is the gate's own. ⚠ 102 inline `<path d>` occurrences match NO library glyph — off-library geometry in snippets, a finding for the icons lane to carry.

## Condition on landing
D-1(a) may land only with the two sentences above replaced. That is a land-lane instruction, not a page change; the page's counts do not move.
