# The mark-map pass, and the half-dead canon

```
provenance: session #122 · 2026-08-07
status: observed
```

*The WHY and HOW of session #122. The WHAT lives in the terse records: five rulings in
`knowledge/_rulings.json` (`s122-D1`…`s122-D5`, Dave's — this file records none of them, it
points at them), the defect record at `knowledge/_DS-IMPROVEMENTS.md` § ds-038 (the legacy
drift) and § ds-039 (the half-dead canon), and the session's `★ LATEST` banner in
`GOOD-MORNING.md`. Both-way links: ← `_LIVE-STATE.md` ⏱ #122 delta · ← `GOOD-MORNING.md`
★ LATEST #122.*

---

## Why the session opened where it did

#121 left one thing on Dave's plate and named it plainly: **the mark-map combination pass** —
status × theme values for the `--mark-*` map that `s121-D1` had ruled the STRUCTURE of while
leaving the VALUES provisional. That is a ruling that cannot be taken from a table of hex
codes; it is an eye ruling. So the session's first act was to build him something to rule
*with*: `reviews/outputs/mark-map-controller-v1.html`, a live controller showing every status ×
theme cell with its contrast leg.

v1 shipped with a render nobody could verify in-sandbox. That is worth stating plainly, because
everything else in this session flows from it: **the instrument was not trustworthy, and the
person using it was.**

## Finding 1 — Dave's eye said the legacy lane was wrong, and it was

Dave's words, at the controller: *"legacy hasn't picked up the colours."*

The obvious reading was a controller bug. The v4 revision added **KG fixtures** — the standard's
own values ({#col25-017}) rendered beside the live ones — and that changed the character of the
observation completely. A mismatch was no longer merely *visible*; it was **attributable**: you
could see WHICH side disagreed with the standard.

What it attributed to was real drift. `apollo-legacy.overrides.json` carried per-mode dark values
— error `#DB0011`, information `#4587A7` — with `$notes` citing "registry ownsHexes". The token
store, which is the spine, held no dark variance at all. Dave ruled it in one sentence
(`s122-D1`): dark = light, no mode fork. Five override paths flattened, old values retired into
the `$notes` as history rather than deleted.

**The method note:** the fixtures were the difference. An instrument that shows you the live
value tells you something looks off. An instrument that shows you the live value *beside the
standard's value* tells you which one is lying. That is a cheap change with a large return, and
it is the reason the second finding was reachable at all.

## Finding 2 — `canon.css` had been half dead for twenty-three sessions

With legacy's drift explained, one thing still did not add up: the fix did not fully land where
it should have. So `canon.css` was parsed — with `tinycss2`, as CSS — apparently for the first
time in this repo's history.

**1,252 rules parsed. After the fix, 3,319.** Two thousand and sixty-seven rules had been dead,
including **all four theme blocks**.

The cause was small and stupid in the way these always are. `gen_canon_components.py` harvests
`<style>` blocks from reference snippets with a lazy, comment-blind regex. A `<style>` *mentioned
inside a documentation comment* in `Chart-butterfly-h.reference.html` was harvested as though it
were CSS, and what got injected into `canon.css` at ~line 4580 was **markup** — a `<link>` tag and
a comment tail. A CSS parser hits `<`, gives up, and silently discards the remainder of the file.
It had been that way since **#99 (`ba02920`)**.

**The why behind the why — and this is the durable lesson.** Nineteen-plus green gates stand over
`canon.css`. Not one of them parses it. They check its *content* — does this token exist, does
that value resolve, is this literal absent — and every one of those checks is satisfied by text
that a browser will never reach. **A gate suite that never applies the target format's own parser
to the target file is a green that cannot fail**, which is to say an assertion. The same shape as
[[mutation-tests-the-clause-not-the-feature]], one level further out.

And the finding did not come from any gate. It came from an eye, routed through a fixture that
made the eye's complaint attributable.

## The fix, and the refusal clause

Two changes to `gen_canon_components.py`:

1. **Strip HTML comments before harvest.** Removes the cause.
2. **A HARVEST-NOT-CSS refusal clause in `gen_one()`.** Removes the class. If a harvested `<style>`
   contains a literal `<`, the generator fails loud and named rather than injecting markup into
   canon. Mutation-tested: planting a `<` in a harvested style BITES.

The second one matters more than the first. The comment-strip fixes the instance that happened;
the refusal clause fixes the instance that has not happened yet — gate the condition, don't patch
the occurrence.

## Then the pass Dave actually came for

With canon parsing again, the combination pass could be run against something real. Three rulings
landed by eye off the controller (v5, then v6):

- **`s122-D2` — the MONO map**, mode-invariant, mark `#1A1A1A` across all four statuses. This
  **splits the aligned lane**: mono no longer shares RAG values with console/supercharge. That is
  a consequence worth naming, because "the themes agree" had been an unexamined assumption.
- **`s122-D3` — CONSOLE + SUPERCHARGE share one map**, mode-invariant, per-status marks.
- **`s122-D5` — legacy marks WHITE except warning, which stays BLACK.** Needed *because* of
  `s122-D2`: once the base atoms went `#1A1A1A` ×4, legacy would otherwise have inherited them.

`s122-D3`'s console half was blocked by ADR-0014's sibling fence, which forbids console diverging
from mono. Dave lifted it for `rag/*` in his own register: *"just ditch that rule for now, I don't
think I'll change my mind on this, but nothing will stop us if I do ;)"* — `s122-D4`, reversible by
his word, with `badge/` and `tabs/` narrowed to members rather than blanket-freed.

Mechanically, `gen_theme_cascade.py` grew a `"marks"` key in the overrides JSON so `--mark-*` is
emitted per theme block, failing loud on a missing mode.

## What we got wrong

- **`s122-D1` was mis-appended** to `_rulings.json`'s `_README` list before the mistake was noticed
  (21 ≠ 53). Repaired the same minute, verified.
- **The DS entry was numbered `ds-033`**, which collided with an existing ruling id; renamed
  `ds-038`. The canon finding then went in as `ds-039`, matching the generator comments.
- **v1 shipped unverifiable.** Dave's eye and the v4 KG fixtures caught both real defects. The
  numeric gates caught neither, and could not have.

## Where it stands

Ruled and enacted: all five. Gates green (property-resolves 0/87, legacy-leak 0, theme-provenance
37 pre-existing and attributed, cascade selftest OK, `tinycss2` 0 errors).

**Not driven visually.** Nobody has eyeballed rendered marks on the new fills.
`reviews/outputs/mark-map-controller-v6.html` is in `_REVIEW-SIGNOFF.md` awaiting Dave's eye — and
given that this entire session's two findings came from that eye and not from the gates, that is
not a formality.

**Open, and Dave's** (standing home: `_LIVE-STATE.md` § OPEN):

- Legacy warning/information **backgrounds** fell through to the new mono values
  (`#E0A61F` / `#78A7E8`, were `#F0B13A` / `#7DABCD`) — never declared in legacy's overrides, so
  never ruled. A mechanical consequence, not a decision anyone took.
- `_themes.json` `ownsHexes` is now stale: *"`#B92F1E` is Mono's only red"* is false as of
  `s122-D3`. The theme-provenance advisory's 37 are measured against that stale map.
- Supercharge badge / tabs-badge shifted to `#B92F1E` via store alias edges.
- Legacy success white-on-teal mark leg is **4.56** — the weakest, still over the bar.
- `*-tint` pairs remain unruled for mode-invariance.
- `gen_canon_tokens.py` still DESTROYS the hand-authored TOKENS alpha/marks/mark-carriers atoms if
  run (they sit inside AUTO markers with no store origin) — a pre-existing `s121-D1` defect,
  priced and unfixed.
