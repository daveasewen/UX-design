# #267 lane F — demo evidence for "six months into N weeks"

```
provenance: 267 · 2026-09-10 · Fable (Dave's request for judgement)
status: observed — nothing ruled
deliverable: notes/_DEMO-EVIDENCE-n-weeks-2026-09-10-v1.html
```

## Done

- Evidence page built (swiss idiom, light + dark, two-red law #DA1A00 / #F6604C): the verbatim
  sentence with ONE ⬛ slot (the comparator), a 15-row week table, the comparator's three options
  with a recommendation, an 11-row KPI support table (6 supported / 3 partly / 2 not), the three
  CAIO attacks, and one inline SVG of KG nodes over date from `_kg_history.json` (no libraries).
- Every number on the page carries a path or a git command.

## NOT done (declared)

- No N chosen. The repo holds no "six months" and no comparator; the slot is Dave's.
- No hours derived. 234 numbered sessions exist; no source states a session length.
- Page not driven in a browser (static HTML, no script; two themes by CSS tokens only).
- Run-of-show PP04 not edited — this page is its evidence; the edit is lane S's / Dave's.
- Not pushed.

## Every figure and its source

| Figure | Value | Source |
|---|---|---|
| First commit | 2026-05-31 | `git log --reverse --format=%ad --date=short \| head -1` |
| v1.0.10 release | 2026-09-10 | `git log --diff-filter=A --format=%ad -- apollo-spider/dist/Apollo-Spider-v1.0.10.zip`; commit `de8ed57` |
| Elapsed | 102 days = 14.57 weeks; 15 seven-day bins, bin 15 in progress | arithmetic on the two dates |
| Commit days | 73 | `git log --format=%ad --date=short \| sort -u \| wc -l` |
| Commits | 1,280 | `git rev-list --count HEAD` |
| Sessions | 234 distinct `#N` in commit subjects, #2…#267 (33 numbers absent) | `git log --format=%s` regex `#(\d{1,3})\b` |
| Dossiers | 218 dated (219 files incl. README), first 2026-07-05 | `ls _DECISION-HISTORY` |
| Authors | Claude 1,193 · daveasewen 79 · Apollo (Claude) 7 | `git log --format=%an \| sort \| uniq -c` |
| Rulings | 444, 2026-07-28 → 2026-09-10, all `by: Dave`; per ISO week 16/85/76/65/42/89/71 | `knowledge/_rulings.json` |
| Rulings per 7-day bin | 6 · 91 · 67 · 72 · 40 · 88 · 80 (weeks 9–15) | same, binned from 05-31 |
| KG snapshots | 51, 2026-05-31 → 2026-09-09 | `knowledge/_kg_history.json` |
| Last snapshot | 889 nodes / 1,172 edges; 137 component · 137 snippet · 381 pattern · 220 context · 14 ruling nodes | same, key `2026-09-09` |
| Graph first built | 2026-08-08: 75 → 503 nodes | same |
| Second inventory | 2026-08-20: components 91 → 135, patterns 223 → 374 | same |
| Components per bin end | 0,0,32,32,38,38,38,67,67,75,76,135,135,136,137 | same, last snapshot ≤ bin end |
| Root snippets (pre-graph) | 32 @06-20 · 38 @07-04 · 67 @07-25 · 75 @08-08 · 135 @08-22 | `git ls-tree -r <commit> \| grep '^knowledge/snippets/[^/]*\.reference\.html$'` |
| Today's counts | 137 snippets · 138 metas · 56 gate scripts · 17 runbooks · 17 ADRs | `ls` in `knowledge/` and `docs/decisions/` |
| Gate scripts by add-date | 50 (cum. per bin 0,0,3,5,7,7,16,24,25,28,32,40,44,48,50) | `git log --diff-filter=A -- 'knowledge/_validate_*.py' 'knowledge/_gate_*.py' 'knowledge/_release/_gate_*.py'` |
| Releases | v1.0.0 08-26 · .1 08-27 · .2 08-28 · .3 08-29 · .4 08-31 · .6 09-03 · .7 09-08 · .8 09-08 · .9 09-09 · .10 09-10; v1.0.5 never cut | `git log --diff-filter=A -- apollo-spider/dist/*.zip`; #233 subject for v1.0.5 |
| Frozen ledger | apollo-spider, 10 zips | `knowledge/_release/_frozen-releases.json` |
| Release gates | 10/10 green v1.0.10 (gate 10 ADVISORY, 219 findings); 9/9 v1.0.8; 7/9 v1.0.9 PROPOSED | `notes/_subreports/2026-09-10-267-R-release-v1010.md`; git subjects 09-08 / 09-09 |
| Ship-set gates | 45 at v1.0.8 | git subject 2026-09-08 |
| Cold-run series | 2/2/0/2 → 3/2/0/2 → 3/2/3/3 → 3/2/3/2 → 3/2/3/3 → 3/3/3/2 (08 Sep); C6 2/3/3/2 (10 Sep, both gates FAIL — `gen_provenance_receipt.py` absent from zip) | `notes/_subreports/2026-09-08-258-C5-cold-run-5.md` L52; `…267-C6-cold-run-6.md` |
| Cold-run cost | C5 ≈235K tokens; C6 ≈205K at freeze / ≈250K total; no wall-clock anywhere | C5 L112; C6 § Context; grep for minute/elapsed/duration = none |
| First HSBC → v1.0.0 | 70 days | 06-17 → 08-26 |
| GOV.UK second system | 2026-07-02 | `second-system-govuk/` add-date; git subject |
| Absence of "six months" | none in repo | `notes/_lanes/2026-09-10-266-T-timeline-trawl.md` § 3.2 |
| Industry lines | "40–60% faster", "~10x", "91%" — sourced, not ours | `digital-experience-transformation/strategy/`, `docs/research-dossier.md` |

## Recommendation carried (not a ruling)

Option C — drop the comparator, state the measured build; option A (Dave's own prior build)
as the spoken fallback if he asks "compared with what?".

## Tokens (ESTIMATED)

≈60K lane fill: reads of the trawl, the run-of-show and prep (text-extracted), eleven bash
probes over git / the two JSON ledgers / the subreports, the skill, one page write, one note.
