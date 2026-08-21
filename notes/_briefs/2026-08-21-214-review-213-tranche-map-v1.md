# Splitting the 43-component review into sittings — a proposal

**Session #214 · 2026-08-21 · Opus analysis lane**
**Subject:** `reviews/REVIEW-213-wave-components-four-theme-v1.html` (store row W-99i)
**Status:** ⛔ PROPOSED, NOT RULED. Every bundle and every tranche below is a *reading order* for
you. Nothing here merges a component, closes a question, renames a file, or touches a W- row.
Bundling two components is a claim that they should be **looked at together**, never a claim that
one of them should be deleted.

---

## What is actually on the page

Forty-three components. **172 questions**, and they divide like this:

- **145 questions attached to individual components** — between 1 and 8 each.
- **27 questions in the five rule-once panels** — Wave 3 (5), Wave 4 (4), App shells (8),
  Templates (9), Lock-ups (1). These are the ones where a single answer settles the same thing
  across nine or eleven components at once.

Two thirds of the page's decision-weight sits in four places: the eleven templates (35 questions
with their panel), the seven app shells (30), the three big overlay organisms — Calendar, Tree,
Cascader — (27 with their panel), and the lock-ups (19).

**A thing worth knowing before you start.** Of the 43 metas, only **15 carry a written question
list** (`$decisionsForDave`) — the three wave-3 fintech rows minus Limits meter, the three
selection controls, the three action-chrome pieces, and all seven app shells. The other **28 —
every template, every lock-up, all seven heavy organisms, and Limits meter — carry no question
list at all.** Their questions exist *only* in the lane receipts and on this review page. That has
a practical consequence for any split: for those 28, the review surface is not a convenience, it
is the only structured home the questions have. If the page is broken up, the questions have to
travel with the pieces or they become invisible.

---

## Your four rows: the verdict

You named the transaction list, the standing order list, the document row and the transaction row,
and guessed they were variants of one type. **You are right, and the components say so themselves
— but the set splits two ways, not one, and only two of your four are actually on this review
page.**

Here is what the artefacts show.

**Three of them are genuinely one shape.** The List-items transaction row (gated, promoted,
9.0/9), Document-row, and Standing-order-mandate-row all use the same list anatomy: a `<ul>` of
`<li>` rows, and — measured, not assumed — the *identical* density values `--row-h: 76px`,
`--row-pad: 14px`, `--label-gap: 12px`. Only five snippets in the entire 135-snippet library carry
that trio; three of them are these, and the other two are the templates that compose them.
Standing-order-mandate-row's own meta does not hedge about it: *"Same ROW SHAPE, copied wholesale
(passive li + stretched link + sibling button + list shell + the disabled-glyph lesson)"* from
Document-row. That is declared provenance, not a resemblance I inferred.

**The single axis that separates them is how many actions a row has.** List-items makes the whole
row a `<button>` — one target, one action. Document-row cannot do that, because opening a document
and downloading it are two different actions and you cannot nest a control inside a button. So it
uses a passive row with a stretched link plus a sibling button. Standing-order copied that
two-action shape because a mandate can be paused. Everything else about the three — subject
matter, chips, glyph, meta line — is content sitting inside the same frame.

**The fourth one is not a row at all.** Transaction row is a `<table>` — 2 tables, 13 `<th>`, 22
`<td>`, and *not a single `<li>`*. It shares none of the density tokens. That is not an accident
of authoring: it is a ledger, and a running balance is a relationship *between* rows, which a list
of independent rows cannot express. Its own meta states the discriminator flatly: *"Drop the
running balance and this component collapses into"* the List-items transaction list.

**And there is a fifth member you did not name, which is on the page.** Template · list / index
`$composes` Document-row, carries the same three density tokens, and draws **both a table body and
a list body side by side so that one can be chosen.** Its single biggest question is "Table or
list?" — which is the same question as Transaction row's "should this exist at all", asked one
layer up. These two must be answered in the same sitting or they will contradict each other.

**So the family is:** one row shape with an actions axis (1 or 2) and a subject axis
(transaction / document / mandate), plus one table that is a separate thing whose existence is
conditional on you wanting a running balance, plus one template that is currently sitting on the
fence between the two.

**What a parameterised unification could look like** (one line, as a sketch, not a proposal to
build): *one row organism with `actions: one | two`, `subject: transaction | document | mandate`,
and a slot for the trailing affordance — and separately, a ledger table that is not pretending to
be a row at all.*

**This is where the design work is.** Two of these components carry an explicit written statement
that they should be deleted if you rule a certain way — Transaction row ("if the product's
statement is a list and not a ledger, this component should not exist") and Document-row (variant
B "IS structurally a List-items row and should be one"). Nobody is asking you to bless four
similar things. They are asking you to say what the shape is, once.

⚠ **Two of your four are not on this review page.** The List-items transaction list and
Document-row are older, already-built components. They need to be open in front of you for this
sitting, but they are not among the 43 and nothing on this page rules them.

---

## The other families I found

I swept the remaining 39 and measured, rather than going by name. Two of the name-based groupings
turned out to be real families and one turned out not to be.

**The seven app shells are one component wearing seven hats — the strongest family on the page.**
Mean overlap of token-bearing CSS declarations across all 21 pairs is **64%**, and the closest
pair (top-nav vs split) is 85%. They differ in layout arrangement, not in substance. What
separates them measurably is their *breakpoints*, and there the evidence is a mess worth seeing:
top-nav uses 900/600, side-nav uses 1040/720, multi-column uses 1200/840 — three different pairs —
while all four wave-6 shells reuse 900/600. Nothing anywhere ratifies any of those numbers.
*Unification sketch: one shell with a `nav: top | side | rail | split | focused | doormat` prop and
one ruled breakpoint scale.* **Needs design work — and the breakpoint scale is the upstream call.**

**The eleven templates are not one family, but they contain three near-duplicate pairs.**
Overall overlap is 38%, which is family resemblance rather than sameness. But three pairs stand
out sharply: **Dashboard and Report at 87%**, **Create/edit and Auth at 77%**, and **Error and
Confirmation at 75%**. Each pair is worth looking at as a pair — a report is a dashboard with
provenance, an auth page is a create/edit form with one column, and a confirmation is an error
page with a different roundel. *Unification sketch: three organisms with a tone/purpose prop
instead of six files.* **Needs design work, at the pair level.**

**The nine lock-ups are NOT a family — the name is doing work the artefacts do not.** Mean
declaration overlap is **14.8%**, the lowest of any group I measured, and the closest pair (Hero
and Stats-band) only reaches 37%. Page-header, Filter-toolbar, Section-heading, Card-header, Hero,
Stats-band, Footer-doormat, CTA and Feature-grid share a naming convention and nothing else
structural. I flag this deliberately: the natural instinct is to treat "the lock-ups" as one
bundle because they are called one thing. The evidence says they are nine separate small
decisions. **Do not bundle them for merging. Bundle them for a sitting only.**

**Two smaller pairs, both flagged by the components themselves.** FAB and Back-to-top are two
round floating buttons in the same corner (38% overlap) and the review page already asks "FAB
versus Back-to-top — they collide." Calendar, Tree and Cascader form a three-way overlap that the
page asks about twice ("Do Tree and Cascader both exist?" and "Tree versus Cascader versus
Sidebar-nav"). **Both need design work.**

**The wave-3 selection controls and the heavy media organisms are not families.** Range slider /
Rating / Transfer list sit at 21% and share only the wave-3 panel. Splitter / QR code / Carousel /
Image block sit at 23% and share only a 480px breakpoint. These are singletons that happen to have
been built in the same week.

---

## Something that runs across everything

Pulled out because it is the real shape of the page, and it is your instinct generalised: **there
are roughly a dozen questions on this surface that are all the same question — "does this thing
exist, or is it the other thing?"**

Transaction row versus the List-items list. Limits meter versus Runway bar (and "should Limits
meter exist at all"). Calendar versus Date-picker's panel. Tree versus Cascader versus
Sidebar-nav. Cascader versus Tree again. Carousel standard versus peek — one component or two.
FAB versus Back-to-top. Standing order versus Direct Debit — one component or two. Template ·
wizard, "should this template exist at all". Template · list/index, table or list. And the lock-up
panel's single question: one flexible organism with an arrangement prop, or nine named files.

Every one of these is cheap to answer and expensive to defer, because the cosmetic questions
underneath them are wasted work if the component turns out not to exist. **That is why the tranche
order below front-loads them.**

---

## The proposed sittings

Six tranches. Sized by *question count*, not component count, because a lock-up with one question
and a Calendar with eight are not the same afternoon. Ordered so that anything that cascades is
answered before the things it cascades into.

### Sitting 1 — The statement family · 20 questions

**Transaction row · Standing order / mandate row · Limits meter · Template · list / index · the
Wave 3 panel.**

Deliberately the lightest count and the heaviest thinking. This is your four rows plus the
template that sits on the fence, and it contains three "should this exist" rulings that unblock
work elsewhere. Have the List-items transaction list and Document-row open alongside — they are
not on the page but they are half the evidence.

The Wave 3 panel sits here because it is upstream of everything in wave 3: it holds the
monochrome-money decision, the warning-versus-error seat for "Failed" and "At limit", the icon
idiom, and the missing recurring-payment glyph. Those cascade into Sitting 6 as well.

*Expect a long, slow sitting despite the small number. Nothing else on the page asks you to decide
whether a component should be deleted three times over.*

### Sitting 2 — The duplicate court · 35 questions

**Calendar · Tree · Cascader · FAB · Back to top · the Wave 4 panel.**

Every overlap question that is not about rows. Calendar asks whether Date-picker should consume
it; Tree and Cascader ask twice whether they are both real; FAB and Back-to-top ask which of them
owns the bottom-right corner. The Wave 4 panel comes with them because it carries the
descender-clip gate defect, the four missing accessibility roles, the invisible Date-picker ring,
and the type-composite debt drift — all of which touch these same three organisms.

*The longest sitting by count, but the questions are similar to each other, which makes it faster
than it reads.*

### Sitting 3 — The seven app shells · 30 questions

**Top nav · Side nav · Multi-column · Split · Focused · Doormat · Nav rail · the App shells
panel.**

The panel first, and specifically its first two items, because they are the two biggest
unanswered numbers in the whole set: **the breakpoint scale** (three different pairs shipped in
one wave, nothing ratified) and **the brand mark** (twelve official SVGs exist, zero of 108
snippets reference one, so every shell currently shows a text stand-in). Answer those two and most
of the seven shells become cosmetic.

*Shells come before templates because a shell wraps a template, and the breakpoint and brand
answers land inside the templates too.*

### Sitting 4 — The templates · 32 questions

**Dashboard · Detail · Create/edit · Wizard · Auth · Settings · Empty · Error · Confirmation · the
Templates panel.** (List / index was decided in Sitting 1; Report moves to Sitting 6 because its
questions are about charts.)

The panel is the biggest of the five and is genuinely upstream: whether a template is a
"component" at all, whether the schema needs a composition edge, whether a template ships any
JavaScript (today ten of eleven ship none, so every search box, chip, switch and sort header on
these pages *looks live and is not*), and where a shell ends and a template begins.

Read the three near-duplicate pairs together when you reach them: Dashboard with Report's shape in
mind, Create/edit next to Auth, Error next to Confirmation.

### Sitting 5 — The lock-ups · 23 questions

**Page-header · Filter toolbar · Section-heading · Card-header · Hero variants · Stats-band ·
Footer doormat · CTA · Feature grid · Split button · the Lock-ups panel.**

The panel here is one question and it governs all nine: one flexible organism with an arrangement
prop, or nine named files. Answer it first; the receipt notes the split is mechanical either way,
because each arrangement block is already self-contained.

After that these are nine small independent calls — the measurements say they share almost
nothing, so do not look for a pattern that is not there. Split button joins this sitting as a
singleton of similar weight.

### Sitting 6 — The remainder · 32 questions

**Splitter · QR code · Carousel · Image block · Template · report · Range slider · Rating ·
Transfer list.**

Everything with no family. Genuinely independent calls, and the most straightforwardly enjoyable
sitting of the six — the QR-code-in-dark-mode question is already measured and waiting, and
Rating's filled-star colour is a single yes/no about whether the library gains a warm token.

---

## Sitting sizes at a glance

| Sitting | Theme | Components | Questions |
|---|---|---|---|
| 1 | The statement family | 4 (+2 off-page) | 20 |
| 2 | The duplicate court | 5 | 35 |
| 3 | The app shells | 7 | 30 |
| 4 | The templates | 9 | 32 |
| 5 | The lock-ups | 10 | 23 |
| 6 | The remainder | 8 | 32 |
| | | **43** | **172** |

---

## What this proposal does not do

It does not split the review file. It does not merge, delete or rename any component. It does not
close any question or touch W-63, W-71–W-84 or W-99i. It is a reading order and a set of viewing
groups, offered so that a 172-question page becomes six afternoons instead of one impossible one.

⬛ **Open to you:** whether the split is a reading order over one page, or six generated pages. If
it is six pages, the 28 components whose questions live only on this surface are the ones that
need the questions carried across — they have no meta to fall back on.
