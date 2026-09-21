# 293 · lane J5 — recall over re-ranking: a costed proposal. ANALYSIS ONLY.

**Filed** 2026-09-21 · **Scope** analysis only, no live call, no change · **No commit** ·
**Deliverable** `notes/_lanes/293/J5/jev-recall-proposal.html`

Dave's words govern this lane, verbatim and at the top of the page:

> "okay this seems like a big job and maybe a dramatic change to the system, given that I have a
> presentation on Friday any analysis is fine but any chages with impact will need to be made
> after the presentations and demos."

Nothing on the page is phrased as done, started or scheduled. Every action is "after the 25th,
if ruled." **No live Jev call was made by this lane. No git command was run. `.env.local` was
never opened and no key material was read, printed or written. No existing file was modified;
the only two files created are this subreport and the page.**

---

## 1 · What I read

| path | why |
| --- | --- |
| `.claude/skills/swiss-design-system/SKILL.md` | the page idiom — archetype B (1/3 : 2/3 splits, decorative index numerals), tokens, accent-only rule, emphasis dormant |
| `notes/_lanes/293/J/jev-integration-brief.html` | skimmed head + headings only, for the house CSS token block and section rhythm; its content is **not** repeated on J5 |
| `notes/_subreports/2026-09-21-293-J2-jev-adapter.md` | 2 calls, 693.5 ms mean, the `jev-1.13.0`-is-echoed-not-sent finding, the unfalsified Score, the receipts-tracking question left open |
| `notes/_subreports/2026-09-21-293-J3-jev-probe.md` | 3 calls, 594.6 ms mean, confidence leaves 1.0, **the stripper lesson** (`html_to_state` discards the CSS that carried the mutation; the residual prose vouched for the removed marker) |
| `notes/_subreports/2026-09-21-293-J4-memento-rerank.md` | 14 calls, the flat verdict, the fixture's provenance (357 `consult-receipts` lines, 63 with payload), the ds-018 argument |
| `notes/_lanes/293/J4/rerank-results.md` | the per-query table, the aggregate, the token/latency/cost block |
| `notes/_lanes/269/kg-gaps/DAVE-RULINGS-2026-09-14.md` | Dave's six decisions on #269 |
| `_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html` | tag-stripped, summary + the twelve-candidate-edge table read only |
| `knowledge/_search_core.py` | where a second door plugs in |
| `knowledge/_build_kg_explorer.py` | its inputs only (grep of `json.load`/`glob`), to name where a proposed-edge file would sit **without changing the build** |
| `knowledge/_memento-index.json`, `_ruling_edges.json`, `_icon_nodes.json`, `_consult-lexicon.json`, `roles.json`, `_kg_history.json`, `components/*.meta.json`, `notes/_lanes/267/E/edge-recs.json` | the counts below |
| `knowledge/canon/canon.css` | confirmed present; linked from the page at `../../../../knowledge/canon/canon.css` |

`knowledge/canon/canon.css` exists (`ls knowledge/canon/`). It is linked, and the page also
carries its own `:root` token block so it stands alone if opened from outside the tree.

---

## 2 · Counts I measured — commands and output

### 2.1 Memento index — 2,282 records

```
$ python3 -c "
import json, collections
d = json.load(open('knowledge/_memento-index.json')); r = d['records']
print('records:', len(r))
print(collections.Counter(x.get('kind') for x in r).most_common())
tot = sum(len(x.get('text','')) for x in r)
print('total text chars', tot, 'mean', tot//len(r))"

records: 2282
[('ls-archive-section', 535), ('pattern-node', 380), ('gauge-block', 275),
 ('gm-archive-section', 263), ('context-node', 222), ('brief', 206),
 ('component-meta', 139), ('ledger-section', 86), ('carries-section', 71),
 ('runbook-section', 57), ('gm-section', 20), ('dream', 13), ('ls-section', 11), ('lane', 4)]
total text chars 40029693 mean 17541
```

Record keys: `file · head · id · kind · line · text`. Top-level keys of the index file:
`$generated_by · records`. **14 bucket kinds — that is the closed set the label vocabulary on
the page is derived from.**

The 40.0M-char total is why the page states plainly that a 600-char cap reads **3.4%** of the
corpus (2,282 × 600 = 1.37M of 40.03M). That is a limitation of the estimate, not a hidden
assumption.

### 2.2 Lexicon — 69 synonyms

```
$ python3 -c "import json; d=json.load(open('knowledge/_consult-lexicon.json'))
for k,v in d.items(): print(k, len(v))"
$comment 18
synonyms 69
```

### 2.3 The plug point in `_search_core.py`

```
$ grep -n "s <= 0" knowledge/_search_core.py
106:        if s <= 0:
```

`search()` is at line 94, signature
`search(records, query, lexicon, bucket_fn, caps, all_results=False, decorate=None)`;
`score_record()` is at line 81 and returns `matched_original * 2 + matched_expanded`.
**Line 106 is where a zero-scoring record is dropped, and that is where recall is lost.** The
page names an optional labels argument beside the existing `decorate` hook, consulted only for
records lexical scored at zero, surfaced as a separately-headed group. **Proposal only —
`_search_core.py` and `_memento_search.py` were not touched.**

### 2.4 `_build_kg_explorer.py` inputs (read, not changed)

Inputs named by grep of `json.load` / `glob` in the builder: `knowledge/components/*.meta.json`,
`_nodes-pattern.json`, `_nodes-context.json`, `_rulings.json`, `_ruling_edges.json`,
`_rule_nodes.json`, `_ux_principle_nodes.json`, `_icon_nodes.json`, `_logo_nodes.json`,
`_kg_verbs.json`, `_kg_history.json`, plus `knowledge/compliance/rules/*`.

```
$ python3 -c "import json; d=json.load(open('knowledge/_kg_history.json'))
print(len(d),'days', sorted(d)[0], sorted(d)[-1])"
54 days 2026-05-31 2026-09-14
```

A proposed-edge sidecar would sit beside those as `knowledge/_edge_proposals.json`, **with no
reader in the builder and no entry in `_kg_verbs.json`.** The builder is unmodified.

### 2.5 Component metas, roles, icons

```
$ ls knowledge/components/*.meta.json | wc -l
138

$ python3 -c "... count metas carrying `provides` ..."
metas with provides: 108   total entries: 108   distinct roles: 12

$ python3 -c "import json; print(json.load(open('knowledge/roles.json'))['roles'])"
['headline-metric','status-surface','chart-panel','record-list','page-frame','page-title',
 'wayfinding','action','arrangement','feedback','input','overlay']      # 12

$ python3 -c "import json, collections; d=json.load(open('knowledge/_icon_nodes.json'))
print('nodes',len(d['nodes']),'edges',len(d['edges']))
print(collections.Counter(e['type'] for e in d['edges']))
u=[e for e in d['edges'] if e['type']=='usesIcon']
print('distinct sources',len({e['s'] for e in u}),'targets',len({e['t'] for e in u}))
print('ratified:', d.get('ratified'))"

nodes 676 edges 1294
Counter({'inGroup': 666, 'usesIcon': 371, 'activeVariantOf': 234, 'defaultActive': 15, 'ruledBy': 8})
distinct sources 105 targets 81
ratified: s277-D4
```

**Correction carried onto the page.** #269 lists usesIcon at "19 metas name an icon path". That
is a prose-citation count. Measured today, `_icon_nodes.json` **already holds 371 `usesIcon`
edges** across 105 components and 81 icons, ratified s277-D4, derived by byte-match of
normalised `<path d>` through each meta's `renderedBy` snippet. So usesIcon is not at zero; it
is the better **audit** target, and the page prices it both ways rather than repeating #269's
framing uncorrected. My own grep of the metas found 18 mentioning `icons/` and 5 distinct
`assets/icons/*.svg` paths — a third figure again, and none of the three is wrong; they count
different things. Stated rather than reconciled away.

### 2.6 The ruling→ruling edges — 78 is a judgement count, not an edge count

```
$ python3 -c "import json, collections; d=json.load(open('knowledge/_ruling_edges.json'))
print(list(d.keys())); print('edges', len(d['edges']))
print(collections.Counter(x.get('source') for x in d['edges']))
print('plain mentions', len(d['ratified_plain_mentions']))"

['_README','ratified','generated_from','edges','ratified_plain_mentions']
edges 48      # 47 sourced 'edge-recs#N' (N up to 78) + 1 'store-field:superseded_by'
plain mentions 31

$ python3 -c "import json; print(len(json.load(open('notes/_lanes/267/E/edge-recs.json'))))"
78
```

`_README`, verbatim in part: *"lane E's 78 judgements … `ratified_plain_mentions` are the 31
rows Dave ratified as PLAIN CITATIONS: they stay derived `mentions`, never authored."*
**47 authored + 31 plain = 78.** The brief's "78 derived ruling→ruling edges" resolves to 78
judged *pairs*; the file holds 48 edges. The page states the split and keeps the 78-call budget,
because auditing the 31 Dave declined is the half with a recorded human verdict to check
against.

---

## 3 · The cost model — every input labelled

Two measured constants, both from J4's `rerank-results.md`, and one declared price:

| | value | grade |
| --- | --- | --- |
| input tokens per candidate-question | **364.7** (102,106 ÷ 14 requests ÷ 20 questions) | measured |
| seconds per question, batched 20/request | **0.046** (920.0 ms ÷ 20) | measured |
| request latency, batched | **920.0 ms** mean | measured |
| price | **$0.042 / 1M input tokens** | **declared** (rerank cookbook, jev-1.12; the API returns no cost field) |

```
A  memento labels, 2 q/record   2,282 recs → 4,564 q → 1,664,328 tok → $0.0699 → 229 req → 211 s
A  memento labels, 1 q/record   2,282 recs → 2,282 q →   832,164 tok → $0.0350 → 115 req → 106 s
B  providesRole  138 × 12       1,656 pairs →           603,884 tok → $0.0254 →  83 req →  76 s
B  usesIcon audit (371 derived)   371 pairs →           135,290 tok → $0.0057 →  19 req →  18 s
B  usesIcon 138 × 81 matched   11,178 pairs →         4,076,217 tok → $0.1712 → 559 req → 514 s
B  usesIcon 138 × 666 full     91,908 pairs →        33,515,565 tok → $1.4077 → 4,596 req → 70 min
C  ruling-edge audit, 78 judged     78 pairs →            28,444 tok → $0.0012 →   4 req →   4 s
```

Pair counts measured; token / cost / request / wall figures **derived** from the two measured
constants and the declared price. Recommended B scope is the first two B rows: 2,027 pairs,
$0.031, 94 s.

**Success measure for A, fixed in advance and stated on the page:** re-run J4's 14-row fixture
and count absent-from-top-20. It is **4 / 14** today (measured). That number is the target, not
MRR — MRR is what made the re-rank look like an almost-result.

---

## 4 · What I could NOT verify

1. **The price.** $0.042 / 1M input tokens is **declared** — carried from TypeSafe's rerank
   cookbook for jev-1.12, never billed, never returned by the API. Every dollar figure on the
   page inherits that. Lane J5 made no call and could not check it, and a jev-1.13 price is
   unknown to us. **This is the single largest unverified input on the page.**
2. **Accuracy of anything.** Nineteen calls, zero repeats, no ground truth that predated a
   question. A labelling pass that runs once and is trusted thereafter is the worst consumer of
   an uncalibrated instrument — on the page as risk 3, and the reason the sidecar must stay a
   discardable sidecar.
3. **The token estimate per record for Proposal A.** 364.7 tok/question is measured, but it was
   measured on a *candidate inside a 20-candidate state with one Score question*. A per-record
   state with one Choice over a closed label set plus one Score is a different shape, and the
   Choice's label list is itself input tokens that J4's figure does not contain. The A estimate
   is therefore a **floor**, not a bound. Order of magnitude is safe; the second digit is not.
4. **The 600-char cap's adequacy.** J4 truncated 266 of 280 candidates at 600 chars and still
   got a working ladder — but the index's mean record is 17,541 chars. Whether 600 chars is
   enough to label a record's *topic* is untested. A 2,000-char variant is ~$0.10 and also
   untested.
5. **Which #269 counts are current.** The families-at-zero figures on the page (932 tokens, 666
   icons, 470 rules, 145 principles, 251 photos, 111 fonts, 12 roles) are cited **as #269
   printed them on 2026-09-14** and were not re-measured here, except the two I did re-measure
   (12 roles — confirmed; usesIcon — **contradicted**, see §2.5). Given one of the two I checked
   had moved, others may have too.
6. **Whether the second door would actually work.** Line 106 is where recall is lost, and that
   is verified by reading. That a label sidecar would recover the four absent rows is a
   hypothesis and is written on the page as one, with a failure condition attached.
---

## ⚙ THE THREE MACHINE-READ LINES — ADDED BY THE #294 WRAP AT STAGING, AND SAID SO

⚠ **Lane J5 filed this report before `s294-D2` existed** (the ruling was taken, inscribed and
enacted later the same day, #294), so it carried none of the three lines `s218-D7` requires and the
`s294-D2` arm — which reads the STAGED set only — would have refused the commit that carries it.
The **#294 wrap** added them rather than exempting the file, on lane C2's own precedent from that
session. ⛔ **No sentence of this lane's was altered, deleted or renumbered, no item was put in its
author's mouth, and every figure below is the #294 wrap's count of THIS report's own text, derived
and shown:**

**findings 20** = the measured statements the body makes — the memento index at **2,282 records /
14 kinds / 40,029,693 text chars / mean 17,541** · a 600-char cap therefore reading **3.4%** of the
corpus · the lexicon at **69 synonyms** · **`_search_core.py:106` is where a zero-scoring record is
dropped, and that is where recall is lost** (`search()` at :94, `score_record()` at :81) ·
`_build_kg_explorer.py`'s inputs named by grep of `json.load`/`glob`, **builder unmodified** ·
`_kg_history.json` at **54 days, 2026-05-31 → 2026-09-14** · **138** component metas, **108**
carrying `provides`, **12** distinct roles (confirming `roles.json`) · `_icon_nodes.json` at **676
nodes / 1,294 edges**, of which **371 `usesIcon` across 105 sources and 81 icons, ratified
`s277-D4`** · ★ **THE CORRECTION THAT MATTERS: #269's *"19 metas name an icon path"* is a
prose-citation count, and `usesIcon` is NOT at zero** · **three different icon counts (371 derived ·
18 metas mentioning `icons/` · 5 distinct `assets/icons/*.svg`), none of them wrong, stated rather
than reconciled away** · `_ruling_edges.json` at **48 edges (47 `edge-recs#N` + 1
`store-field:superseded_by`) + 31 `ratified_plain_mentions` = the 78 JUDGED PAIRS**, so the brief's
*"78 derived ruling→ruling edges"* resolves to pairs and not to edges · the cost model's **two
measured constants** (364.7 input tok per candidate-question · 920.0 ms per batched request, 0.046 s
per question) **and one DECLARED price** ($0.042 / 1M input) · the seven costed scopes, pair counts
measured and every token / cost / request / wall figure derived · and the success measure fixed in
advance — **absent-from-top-20 is 4 of 14 today, measured**, and that is the target rather than MRR.

## RULING-SHAPED QUESTIONS

**ruling-shaped 2** — ⚠ **and this lane raised no such section of its own; the two below are what
its BODY carries forward rather than settles, quoted from it and not invented here:** **(1)** whether
the second door at `_search_core.py:106` is built at all, and which of the seven scopes — governed
by **Dave's own words at the head of the lane**, *"okay this seems like a big job and maybe a
dramatic change to the system, given that I have a presentation on Friday any analysis is fine but
any chages with impact will need to be made after the presentations and demos"* — so **nothing on
the page is phrased as done, started or scheduled and every action is *after the 25th, if ruled***;
**(2)** the **price is DECLARED and is the single largest unverified input on the page** — every
dollar figure inherits it, the API returns no cost field, and a `jev-1.13` price is unknown.
⛔ No question was attributed to lane J5 that its own text does not carry.

**UNPROVEN 6** = the lane's own § 4 *"What I could NOT verify"*, as it numbered them: the declared
price · **the accuracy of anything** (19 calls, zero repeats, no ground truth that predated a
question) · the per-record token estimate for Proposal A being a **floor, not a bound** · whether a
600-char cap is enough to label a record's topic, untested · which of #269's families-at-zero counts
are still current (**one of the two re-measured had moved**, so others may have) · and whether the
second door would actually recover the four absent rows, written on the page as a hypothesis with a
failure condition attached.

COUNTS: findings 20 · ruling-shaped 2 · UNPROVEN 6

REPLAY-THESE: `python3 -c "import json,collections; d=json.load(open('knowledge/_memento-index.json')); r=d['records']; print(len(r), collections.Counter(x.get('kind') for x in r).most_common())"` · `python3 -c "import json; d=json.load(open('knowledge/_consult-lexicon.json')); print({k:len(v) for k,v in d.items()})"` · `grep -n "s <= 0" knowledge/_search_core.py` · `python3 -c "import json; d=json.load(open('knowledge/_icon_nodes.json')); import collections; print(len(d['nodes']), len(d['edges']), collections.Counter(e['type'] for e in d['edges']), d.get('ratified'))"` · `python3 -c "import json; d=json.load(open('knowledge/_ruling_edges.json')); print(len(d['edges']), len(d['ratified_plain_mentions']))"` · `python3 -c "import json; print(len(json.load(open('notes/_lanes/267/E/edge-recs.json'))))"` · `ls knowledge/components/*.meta.json | wc -l`
