# s227 lane 9 — one page for every loose end today

**COUNTS: cards 44 · sources 5 · deduped 3 · excluded-as-ruled 7 · UNPROVEN 2**

Sub: Opus build sub, session #227, lane 9. Conductor: Fable seat.
⛔ No rulings, no store rows, no W-rows, no commits. One file created:

- `reviews/SESSION-227-DECISIONS-2026-08-30-v1.html` (83,504 bytes, self-contained)

`git status --porcelain` at hand-off: **one line**, this page, untracked. Nothing else moved.

---

## 1. What it is

Dave's question was *"do we need another DASHBOARD-DIFF-DECISIONS page for any loose end?"* —
answered yes, once, for everything. 44 cards, every one of them ruling-shaped, drawn from five
sub-reports, grouped by **how much of him each one costs**:

| band | cards | what it means |
|---|---|---|
| **One look settles it** | 8 | The answer is on a page. Open it, look, say the word. |
| **One word settles it** | 26 | Options already written out. Yes / no / which. |
| **Needs a sitting** | 10 | The answer changes what happens next, or a check is owed first. |

Filters on top: All 44 · Undecided · the three bands · **Due Monday 15** · **From #226 9**.

Every card carries the question in Dave's-eye prose, its evidence quoted, and
**`<b>Source:</b> <file> §<section>`** as the last line — so any card can be walked back to the
report that raised it in one hop.

### The Monday filter is the point

`s227-D6` scopes the cut to *"the SHARP set applied or explicitly parked"*. **That clause is why
this page exists**: 15 cards (C2–C12, N1–N6, minus the ones already ruled) are that apply-or-park,
and the page says so in the header. Without it, "explicitly parked" has no surface to happen on.

## 2. The greyed strip — six things ruled today, no controls

At the top, dashed border, ink-3, **no radios**: the red team's two BLOCKING findings and four
more are settled, with the ruling id on each so Dave sees the receipt and moves on.

| item | closed by |
|---|---|
| B1 — nothing in `cold-start/` reaches a designer | `s227-D6` (manifest gains a `cold-start` group) |
| B2 — Copilot gets the contract only by overwriting the boot file | `s227-D5` — **Merge** |
| S1 — the "on-canon" escape hatch defeats box 2 | `s227-D6` (S1 sentence in the cut) |
| S11 + grill-me `Q5` — `brief-template.md` and grill-me don't ship | `s227-D6` (claimed in the ship list) |
| S13 — the Copilot boot file omits grill-me | `s227-D6` (prompts shim + skills-table row) |
| N5 — the manifest prose says "five skills" | `s227-D6` (six retuned descriptions) |

**Read the rulings, don't trust the brief.** The brief named B1/B2/S1 as resolved. Reading
`s227-D6`'s `says` field found **three more** already inside the authorized cut — S11, S13, N5,
and grill-me's own Q5. Those four came off the card deck and into the strip. Four cards Dave does
not have to read.

## 3. Dedupe — 3 cards carry two sources each

| card | question | sources merged |
|---|---|---|
| **W3** | the five zero-inset `.seg` consumers | segmented `Q2` + grill-me `Q4` (the A1 remainder, from both sides) |
| **W5** | "Common" in copy vs `legacy` in code | grill-me `Q6` + fab-overlay §theme button |
| **W7** | three instruments nothing ever runs | segmented `Q3` (`gen_radius_derive`) + red team §REPLAY (`gen_projections`, `verify_placement`) |

47 source citations across 44 cards. Each source is cited by at least 5 cards:
`redteam 16 · seg 9 · dream 9 · fab 8 · grill 5`.

**One overlap declared rather than merged.** `L5` (the `sm`→`xs` ordinal map) asks the same map
question as **`Q-B7`** on the dashboard diff page. The card says so in its own words —
*"Answer it there or here, not twice"* — and carries what changed under it today: six more
files now depend on the proposed reading, and console `xs` thumb is no longer `0` (it is `4`),
so Q-B7's premise has moved. Deleting it would have hidden a moved premise; duplicating it
silently would have been the dupe.

## 4. One finding of my own, from re-probing a source's evidence

The fab-overlay report says canon carries **three** leaked bare `body{…}` rules and cites
**two** line numbers, at `:14103` and `:16175`. Re-probed at this HEAD:

```
knowledge/canon/canon.css:14183   body{margin:0; padding:2.25rem; background:var(--page); ...}
knowledge/canon/canon.css:16255   body{margin:0; background:var(--page); ...}
grep -c '^[[:space:]]*body[[:space:]]*{'  ->  2
```

**Two, not three — and both lines moved**, because lane 6 regenerated `canon.css` after lane 3
looked. Card `W12` carries the correction in its own words so nobody spends an afternoon hunting
a third rule that may never have existed. ([[premise-ages-faster-than-rule]].)

## 5. Mechanics — reused wholesale, one declared departure

Card shell, control building, `paint`/`hydrate`, three-tier copy, `localStorage` in `try/catch`,
filters, the in-page assertion and the sticky bar are all lifted from
`DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html`. Serialisation is identical:
**`<card-id> <VERB> — <comment>`**, one line each, multi-line comments collapsed, comments on
undecided cards surfaced under `NOTES ON UNDECIDED`.

**The departure, declared.** That page split verbs by *finding vs question*. Everything here is a
question, so the split is by **what the card is asking for**:

- **`data-kind="edit"` (15 cards)** — a minimal edit is already written in the source report.
  Verbs **Apply · Park · Reject · Discuss**; box labelled *"Your comment"*.
- **`data-kind="choice"` (29 cards)** — Dave's words, number or pick are the answer.
  Verbs **Answer · Park · Discuss**; box labelled *"Your answer / ruling"*.

Prompt sections follow the three bands rather than findings/questions, and the footer counts
one number — **Decided N/44 · Left N** — because that is the number he is actually working down.

## 6. Proof — the controller was EXECUTED, not grepped

No browser (VM disk 100% full, no pip). The page's `<script>` was extracted and **run under
`node` against a ~110-line DOM shim built from the real card list parsed out of the HTML**. That
drives the shipped code path, not a re-implementation.

**44 checks, all green.** Highlights:

| probe | result |
|---|---|
| `node --check` on the page's script | SYNTAX OK |
| cards parsed back out of the HTML (stdlib `HTMLParser`) | **44** |
| band split / `data-class` agreement | look 8 · word 26 · sit 10 — **0 mismatches** with section id |
| kind split | edit 15 · choice 29 |
| distinct sources cited | **5** — `redteam 16 · seg 9 · dream 9 · fab 8 · grill 5`, 47 citations |
| duplicate card ids | none |
| controls built at runtime | **147 radios** (= 4×15 + 3×29) + 44 textareas, exactly as predicted |
| comment labels | 29 read *"Your answer / ruling"*, 15 read *"Your comment"* |
| in-page assertion | `44 cards rendered from 5 sources · 15 with an edit already written · 29 open choices · 3 cards cite two sources · 47 source citations · all ids unique.` |
| decide 6 cards across all three bands | counts `0/44` → `6/44`, left `38`; chips read Answer · Apply · Reject · Park · Discuss |
| an edit card offered `answer` / a choice card offered `apply` | **neither exists** — verb sets are per-kind, proven by absence |
| multi-line comment | collapsed to `W3 ANSWER — give them a 2px inset like the other six` |
| comment on an **undecided** card | surfaced under `NOTES ON UNDECIDED`, not lost |
| prompt band ordering | ONE LOOK < ONE WORD < NEEDS A SITTING |
| `localStorage` round trip | one key `apollo-227-session-loose-ends-v1`, 44 entries, `C4 = {"d":"apply","c":"yes, both markers"}` |
| all seven filters | 44 · 38 · 8 · 26 · 10 · **15 (Monday)** · **9 (#226)**, `aria-pressed` exclusive |
| empty band hidden / restored | yes, both ways |
| copy with **no** clipboard API and `execCommand` false | falls through to *"Copy blocked — text selected below…"*, `<pre>` still holds 770 chars |
| Clear all | `0/44`, chips reset **per kind** (Undecided / Unanswered) |
| links | all 6 resolve on disk (4 review pages, 2 showroom pages) |
| external resources | **none** — no fonts, no scripts, no images |
| balance | CSS `{}` 108/108 · `<article>` 44/44 · `<section>` 5/5 · `<pre>` 33/33 · `<div>` 51/51 · `<p>` 183/183 |

### Mutation-proved — the assertion is not decoratively green

Four arms, run against the shipped script:

```
ARM 0  untouched                       ->  44 cards rendered from 5 sources ...      class "assert"
ARM 1  one card removed                ->  COUNT MISMATCH - rendered 43 (expected 44) class "assert bad"
ARM 2  duplicate id planted            ->  COUNT MISMATCH ... duplicate ids: L5       class "assert bad"
ARM 3  one whole source removed        ->  4 sources (expected 5)                     class "assert bad"
```

**Storage-dead arm** (`localStorage` throws on both read and write): page fully functional —
decided 1/44, prompt line `C4 APPLY — works without storage`, **0 keys written**, no exception
escaped. Only refresh-survival is lost, and the page says so in its own "How this works" block.

## 7. UNPROVEN, declared (2)

1. **Nothing has been rendered.** No headless browser, no pip, disk 100% full — the lane
   constraint. Layout, type sizes, colour, the light/dark flip and whether 44 cards read as
   navigable rather than as a wall are **unseen**. The logic is executed and proven; the
   *appearance* is not. Dave opening the file is the first render.
   **Price to prove: one render pass from a seat with disk — light + dark at 1180 and 480.**
2. **`label:has(input:checked)` is unverified in Dave's browser.** It tints the selected verb
   pill. If `:has()` were unsupported the tint is simply absent — the card's chip and left border
   are set from JS via `data-state` and do not depend on it, so state remains visible. Bounded,
   not proven. *(Inherited from the reference page, same construction.)*

## 8. Ruling-shaped — none. One note for the conductor.

This lane raised no `Q:` of its own; the page **is** the questions. One note:

**`W6` says four review pages have no store row, and this page is the fourth.** The card lists
all four by path. Minting the rows is the conductor's act at the wrap
([[forgotten-document-class]] / #185) — if it does not happen there, the page that carries 44 of
Dave's open decisions is invisible to every later retrieval.

REPLAY-THESE: `reviews/SESSION-227-DECISIONS-2026-08-30-v1.html` (~0 tk — Dave opens it and works it; the page is the deliverable, not this report) · `knowledge/_rulings.json` § `s227-D6` `says` field (~300 tk — the "SHARP set applied or explicitly parked" clause is what makes 15 of these cards Monday-bound; read it before pricing the cut) · this report §2, the greyed strip table (~250 tk — four items came off the deck because the ruling said more than the brief did) · this report §4 (~150 tk — the `body{}` count is 2, not 3, and the lines moved)
