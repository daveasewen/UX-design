#!/usr/bin/env python3
"""#288 wrap — build `_CARRIES.md` § `## residual → #289` from § `## residual → #288`.

ONE programmatic pass, the #261…#287 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ⛔ **ZERO STRIKES, AND THE ZERO IS A JUDGMENT WITH A REASON, NOT AN OVERSIGHT**;
  (c) SIXTEEN new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

⛔ WHY NOTHING IS STRUCK, AND IT IS THE `s271-D4` / `s183-D1` REASONING APPLIED, NOT LAZINESS:

  The ONE thing #288 closed that can be receipted is that the `s219-D3` generation arm is BUILT
  (lane A: `knowledge/canon/gen_bento_role_vars.py`, gates green, a four-theme rendered proof).
  The carry that names it is #288's item ② — headline **"MONO'S 0 IS DOUBTED AND THE `s219-D3`
  GENERATION ARM IS TO BE BUILT"**. A strike removes the HEADLINE, not a clause of it, and the
  first half of that headline — **Mono's 0 is doubted** — is STILL TRUE: `s217-D2` still rules
  `layout/bento/gutter` 0 for mono, Dave ruled nothing on the value today, and the arm delivers
  the ROLE-DEFAULT reading (40/24/40/24) while the token reading (0/24/24/0) stands un-overruled.
  ⇒ **The discharge is said in NEW item ⑩ instead** — exactly the move #287 made for the
  connector-lever item, and for the same reason in `s271-D4`'s own words: *"a strike that is
  wrong is worse than an item that is merely stale."*
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #288:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) NO STRIKES — see the module docstring -----------------------------------------------
STRIKES = []

# ---- (c) the session's SIXTEEN new items ------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age). Ages spelled in words.
NEWITEMS = [
 "⬛ **① APOLLO COMPOSES AND THE SLOPPINESS IS ALIGNMENT SPACING AND DIMENSIONS** [NEW — 0, "
 "DAVE'S] — **his verdict by eye on the composition probe, and it is the session's headline.** "
 "Verbatim: *\"so better is someways and worse in others, its more interesting and complete page "
 ", but its more sloppy .\"* and *\"we need to do something about the sloppiness and, its all "
 "about alignment spacing and dimensions, this looks like its working the way I'd have expected, "
 "at least it's diverged from the tamplete\"*. ⇒ **TWO things in one sentence and they pull "
 "opposite ways: the METHOD is endorsed — a cold one-shot with the template unreachable produced "
 "a page that diverged from it and worked the way he expected — and the EXECUTION is not.** "
 "⛔ **THE DEFECT CLASS IS NAMED BY HIM, not by a lane: alignment, spacing, dimensions.** ⚠ "
 "**NOT INSCRIBED — he did not say *inscribe* today and the rulings store stays at 622**, so "
 "this is a question put and not a state of the world (`s271-D4`). What the conductor saw on the "
 "render is recorded as the CONDUCTOR'S reading and not as his: KPI tiles with dead space below "
 "the sparklines, a half-empty programmes table card against a full-height decisions card, two "
 "bottom-row cards not sharing a bottom edge, a filter bar narrower than the table it filters, "
 "and column gutters differing between the KPI row and the rows below. Receipts: "
 "`notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` § On the probe sheet · "
 "`notes/_subreports/2026-09-19-288-P-composition-probe.md` · `notes/_lanes/288/P/probe-sheet.html`.",

 "⬛ **② THE TEST BRIEF FOR THESE PROBES IS HIS OWN AND IS OWED BY HIM** [NEW — 0, DAVE'S] — "
 "verbatim, in the same breath as the verdict: *\"I'll create a test brief for these tests.\"* "
 "⇒ **OWED BY DAVE, not by a lane, and no lane may write it** — the probe's own brief was a "
 "fallback invented by the conductor because the frozen demo prompt could not be found, which is "
 "the very gap this sentence closes. ⚠ **Until it exists, every composition probe answers a "
 "brief nobody ratified**, and two probe pages compared side by side are answering two different "
 "asks. Receipt: `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` § On the probe sheet.",

 "⬛ **③ WHAT THE ONE-SHOT GENERATES *FROM* — AND THE #230 PASS CONDITION REWARDS TRACING** "
 "[NEW — 0, DAVE'S] — **he challenged the premise on seeing the showroom template**, verbatim: "
 "*\"there is a definitely a problem here, 2 actually, the template is a bit wonky and it's "
 "basically copied by the AI, what is the point of building the KG if the agent just traces an "
 "existing file, its very safe but 1. its of average quality anyway... its okay but not great 2. "
 "what was the point of building the system if it just traces from existing examples???\"* and "
 "*\"the results with VS co-pilot are pretty much identical to this, this isn't Apollo its a "
 "dot-to-dot book\"*. ⇒ **TWO problems, both his: the template's quality, and the path that "
 "copies it.** ⛔ **The mechanism is named and is not a ruling: the #230 *zero invented markup* "
 "pass condition REWARDS tracing** — a builder that splices the template byte-identically scores "
 "perfectly against it. ⚠ **Whether that condition is re-cut, scoped or replaced is HIS and is "
 "NOT decided here.** Receipt: `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` § After wave 1 landed.",

 "⬛ **④ THE DECK'S NEW STRUCTURE IS HIS, AND WAVE 2 IS BLOCKED ON IT** [NEW — 0, DAVE'S] — "
 "verbatim: *\"so we also have to actually prepare and create the presentation, we made a good "
 "start but I want to change the structure. please include this is the plan. we might have to "
 "parallelise some of this to get it nailed quickly.\"* ⇒ **The presentation is IN the plan by "
 "his word, and its STRUCTURE is changing — and the new structure has not been stated.** The "
 "*\"good start\"* is the conductor's reading and is marked as the conductor's: the #268 deck "
 "`notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html` with eleven slides and per-slide PNG receipts "
 "under `notes/_subreports/slides-268-v7/`, plus `notes/_DEMO-PREP-david-rice-hsbc.html`. ⛔ "
 "**A deck re-cut lane CANNOT be seated until he gives the structure** — the strand map names "
 "the strand and stops there, correctly. ⚠ **And he asked a question in the same turn that is "
 "still unanswered: *\"can parallel agents cross communicate rather than having solo lanes that "
 "report to the orchestrator?\"*** Receipt: `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` § Third turn.",

 "⬛ **⑤ WHICH EVENT FRIDAY 2026-09-25 IS — SMALL INTERNAL DEMO OR DAVID RICE** [NEW — 0, "
 "DAVE'S] — ⛔ **NOT ESTABLISHED, and lane M put it on a full dark band of its own on the strand "
 "map rather than guessing.** Everything downstream turns on it: what the deck must carry, "
 "whether the one-shot runs live or recorded, and how much of the bento strand has to be "
 "presentable rather than merely correct. ⚠ **Six days from his order to the date, and the path "
 "on the strand map is written for BOTH readings because the seat could not choose between "
 "them.** Receipt: `notes/_STRAND-MAP-2026-09-19.html` § THE DATE · "
 "`notes/_subreports/2026-09-19-288-M-strand-map.md`.",

 "⬛ **⑥ THE OUTER GUTTER HAS TWO ANSWERS AND THE INNER GUTTER HAS THREE, AND NONE IS RULED** "
 "[NEW — 0, DAVE'S] — **measured by lanes A and B, published and NOT reconciled.** The OUTER "
 "(structural bento) gutter reads **0/24/24/0** from the token `layout/bento/gutter` "
 "(`s217-D2`, mono and supercharge at 0) and **40/24/40/24** from the role defaults in "
 "`knowledge/_render/_bento_edit_rails.json`, which is what lane A's arm delivers because that "
 "is the file `s219-D3` names as the one generated source. The INNER (embedded bento or "
 "tile-group) gutter has **three**: canon's literal `1px`, the `subSpacing` reading 4/4/4/2, and "
 "the template's pinned `4`. ⛔ **Supercharge's `0` is INHERITED and was never decided** — it "
 "arrives from the token table, not from a sentence anyone spoke. ⚠ **Lane A picked the rails "
 "manifest and DECLARED the pick rather than hiding it, and picked NO winner between the two "
 "outer readings** — the disagreement is left for Dave, exactly as his gutters correction at "
 "#287 requires (two deliberate quantities, not a contradiction). Receipts: "
 "`notes/_subreports/2026-09-19-288-A-s219-d3-arm.md` §3 · "
 "`notes/_subreports/2026-09-19-288-B-bento-renders.md` §1–2 · `notes/_lanes/288/B/four-themes.html`.",

 "⚠ **⑦ THE SPECIFICITY ROOT CAUSE — CANON'S OWN INSTANCE-DIAL RECIPE SILENTLY LOSES FOR THE "
 "DASHBOARD ROLE** [NEW — 0] — **measured by lane P, not inferred.** "
 "`.c-bento.wall-ops{--bento-gutter:…}` has specificity **(0,2,0)** and loses to canon's own "
 "`.c-bento[data-bento-role=\"dashboard\"]:has(> .c-bento__grid > .c-bento){…}` at **(0,4,0)**. "
 "⇒ **The instance-dial recipe canon documents for tuning one bento's gutter does not take "
 "effect on a dashboard-of-bentos, and nothing says so** — the override is written, the page "
 "renders, and the value never lands. ⛔ **A silent loss, not an error**, which is the class "
 "that survives longest. ⚠ **Not fixed and not ruled here** — a specificity change to canon is a "
 "generator change and a lane at a wrap may not make one. Receipt: "
 "`notes/_subreports/2026-09-19-288-P-composition-probe.md` § Findings.",

 "⬛ **⑧ LANE T'S SIX-QUESTION DECISION PACK — PUT AND UNANSWERED** [NEW — 0, DAVE'S] — **put to "
 "Dave at the wrap call and NOT answered, so it carries as a question and not as a state of the "
 "world** (`s271-D4`). The six: an inline-style rule with the raw-value census re-measured at "
 "**87** attributes in the snippet corpus (against #287's 88, both readings published and "
 "neither rewritten); the template's STATUS and whether `showroom/index.json`'s fixed status "
 "list can express *proposed* at all; the **three** `$awaitingDave` entries the meta carried at "
 "HEAD; and a max-width ruling. ⛔ **Lane T's headline is that the drawn page is sound and the "
 "PAPERWORK is not** — zero invented markup, zero dangling vars, zero raw inline lengths, and a "
 "`$status` block four of whose five claims it measured FALSE. Receipts: "
 "`notes/_subreports/2026-09-19-288-T-template-quality.md` §5–8 · "
 "`notes/_lanes/288/T/template-quality-review.html`.",

 "⬛ **⑨ THE SWISS DESIGN SKILL AS AN APOLLO TASTE GUARANTEE — PARKED BY HIS OWN WORD** [NEW — "
 "0, DAVE'S] — verbatim, at the opener: *\"one thing I noticed and something to add to future "
 "design experimentation, the Swiss design skill is very very successful, the we managed to hit "
 "the aesthetic pretty bang on. I want to borrow some of it for Apollo as some sort of taste "
 "guarantee or guidence.\"* and *\"Not for now but don't let me forget this.\"* ⇒ **PARKED, "
 "explicitly, with an explicit instruction not to lose it** — which is why it is a carry rather "
 "than a plan. The conductor's reading, marked as the conductor's: the skill's discipline (grid, "
 "hierarchy, typographic structure) is a candidate TASTE LAYER distinct from the token and gate "
 "mechanics that govern correctness. ⚠ **No `_state.json` row was minted, because a close "
 "condition is his to state and not a seat's to invent.** Cloud memory copy: "
 "`swiss-skill-as-apollo-taste-guarantee-288.md`. Receipt: "
 "`notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` § At the opener.",

 "⚠ **⑩ THE `s219-D3` GENERATION ARM IS BUILT — THE DISCHARGE IS SAID HERE RATHER THAN BY "
 "STRIKING THE ITEM THAT AGES BESIDE IT** [NEW — 0] — **lane A built it: a new generator "
 "`knowledge/canon/gen_bento_role_vars.py` (289 lines) that reads "
 "`knowledge/_render/_bento_edit_rails.json` — the `s219-D3` one-generated-file, un-consumed and "
 "self-declared `$groundwork_only` since #219 — cross-checks it against the owner the file "
 "itself names, and mints per-theme `--bento-dashboard-main` and `--bento-dashboard-sub` between "
 "new `AUTO-BENTO-ROLE-VARS` markers placed BEFORE `AUTO-THEMES START` (because "
 "`gen_theme_cascade.py` rebuilds everything after that marker and would silently destroy a "
 "block placed later — asserted by the generator's own selftest).** The snippet's two pinned "
 "literals at `:802` and `:804` are now `var()` references with mono fallbacks that are "
 "load-bearing rather than leftovers, and a four-theme rendered-DOM proof was taken. ⛔ **THE "
 "CARRY IT DISCHARGES IS *NOT* STRUCK, and the reason is the rule rather than reluctance:** that "
 "headline reads *\"MONO'S 0 IS DOUBTED AND THE `s219-D3` GENERATION ARM IS TO BE BUILT\"*, a "
 "strike removes the whole headline, and **Mono's 0 is still doubted and still ruled at 0 by "
 "`s217-D2`** — Dave ruled nothing on the value today. `s271-D4`: *\"a strike that is wrong is "
 "worse than an item that is merely stale.\"* ⚠ **AND THE ARM BEING BUILT DOES NOT SETTLE WHICH "
 "OUTER READING IS RIGHT** — see the item above. Receipt: "
 "`notes/_subreports/2026-09-19-288-A-s219-d3-arm.md`.",

 "⚠ **⑪ THE FROZEN DEMO PROMPT IS NOT RECOVERABLE FROM THE RECORD** [NEW — 0] — **lane P "
 "searched and reports the absence as an absence rather than substituting a claim**: "
 "`_memento_search.py` (and `--all`), the #229 cold-start acceptance brief, the #230 demo-day "
 "brief, the #258 demo-fence brief, and a repo-wide grep for the prompt's own distinctive "
 "phrases. ⇒ **Every brief DESCRIBES the test and none of them carries the prompt's text.** The "
 "probe therefore ran on the lane brief's FALLBACK wording, said out loud on the sheet, and ⛔ "
 "**the two pages compared side by side answer DIFFERENT briefs** — the traced template was "
 "built at an earlier session against a business-banking account overview. ⇒ **The comparison is "
 "about HOW each was made, never about which answers a shared ask better**, and that limit is "
 "printed on the sheet rather than buried. ⚠ **Whether the prompt is re-frozen and where it "
 "lives is a decision nobody has taken.** Receipt: "
 "`notes/_subreports/2026-09-19-288-P-composition-probe.md` §1.",

 "⚠ **⑫ THE `$awaitingDave` COUNT HAS THREE READINGS AND ALL THREE ARE PUBLISHED** [NEW — 0] — "
 "`_HANDOFF-138` says **four**, lanes M and T each read **three** at HEAD, and lane A's "
 "additions take the file to **five** by ADDITION. ⛔ **Nothing is reconciled and nothing is "
 "rewritten** — the handoff's four is a dated reading, the lanes' three is HEAD's, and five is "
 "the tree after lane A. ⚠ **What the count IS at any moment is answerable by reading "
 "`knowledge/components/template-dashboard-bento.meta.json`, which is cheaper than a carried "
 "figure and is why no fourth number is minted here** [[measure-dont-convert-units]]. Receipts: "
 "`notes/_subreports/2026-09-19-288-T-template-quality.md` §6 · "
 "`notes/_subreports/2026-09-19-288-A-s219-d3-arm.md` §5.",

 "⚠ **⑬ `knowledge/_render/seat_env.sh` GLOBS A PLAYWRIGHT PATH 1.63 NO LONGER SHIPS, AND A "
 "ONE-LINE FIX IS OWED AND NOT DONE** [NEW — 0] — **declared by two lanes from opposite sides: "
 "lane B symlinked around it and rendered; lane T could not render at all and said so rather "
 "than reporting a CSS reading as a rendered one.** ⇒ **A render seat that works only if the "
 "lane happens to improvise is not a render seat.** ⛔ **NOT FIXED HERE** — a wrap does not "
 "repair an instrument mid-ritual, and the fix is one line in a file no gate grades. Receipts: "
 "`notes/_subreports/2026-09-19-288-B-bento-renders.md` §5 · "
 "`notes/_subreports/2026-09-19-288-T-template-quality.md` §4.",

 "⚠ **⑭ A LANE RAN `git stash push` AGAINST THE STANDING RULE, AND DECLARED IT ITSELF** [NEW — "
 "0] — **lane A ran it while building the arm; no stash entry was created and the lane verified "
 "the tree intact afterwards.** ⇒ **A git write from a build lane, against the standing rule "
 "that git writes belong to the commit lane, declared by the lane that made it rather than "
 "discovered at the wrap.** ★ **A judgment named in a report is a judgment the conductor can "
 "correct — one discovered at the wrap is one he inherits.** ⚠ **What to do about it is his**, "
 "and the #166 sibling stands: `git stash@{N}` indices reshuffle after every drop, so a "
 "stash-by-index dance loses the wrong entry. Receipt: `notes/_lanes/288/WRAP-BRIEF.md` § "
 "Declared by lanes.",

 "⬛ **⑮ FOUR THINGS ARE STALE OR DARK ON THE DELIVERY PATH AND NONE OF THEM IS SCHEDULED** "
 "[NEW — 0, DAVE'S] — **named on the strand map and in the wrap brief, gathered here so they "
 "are countable rather than scattered.** (i) **the showroom still shows the pinned 40/4** and "
 "needs a re-sync after lane A's arm, or the surface Dave looks at disagrees with the canon that "
 "generates it; (ii) a **dashboard freshness check** is still owed — `dashboard/index.html` has "
 "no `--check` arm the way `_gen_chain.py` and `_render_rulings.py` do, so it goes stale on "
 "every unrelated store write; (iii) the **deck carries stale graph figures** — 2,837 on the "
 "slide against 4,820 today; (iv) **the one-shot's quality has been dark since 2026-09-02** — "
 "nothing has graded it end to end since. ⛔ **All four are his to schedule and none is a wrap's "
 "to take.** Receipts: `notes/_STRAND-MAP-2026-09-19.html` · `notes/_lanes/288/WRAP-BRIEF.md`.",

 "⚠ **⑯ FOUR OF THE FIVE FILED LANE REPORTS CARRY NO `RULING-SHAPED QUESTIONS` HEADING, AND "
 "`s218-D7` MAKES IT MANDATORY** [NEW — 0] — **measured at this seat by grep over the five "
 "filed reports, not assumed**: only lane M carries the heading. Lane T carries a *Decision "
 "pack* that does the same work under a different name; lanes A, B and P carry the substance in "
 "sections named *WHAT IS NOT DONE*, *WHAT I COULD NOT ESTABLISH* and *Gaps*. ⛔ **The CONTENT "
 "is there in every case — what is missing is the NAME the gate and the next reader look for**, "
 "and `subreport_citation_check` parses exactly that heading. Also measured: only lane P carries "
 "a `COUNTS:` line and only lane T a `REPLAY-THESE:` line. ⛔ **NOT REPAIRED HERE — a wrap does "
 "not edit another seat's filed report**, which is dated history (`ADR-0017` / `s192-D1`); the "
 "finding is published instead. ⚠ **Whether the brief template or the gate tier is what moves is "
 "his** — the check is ADVISORY at birth and its tier is one line, `SUBREPORT_CITE_BLOCKING`.",

 "⚠ **⑰ THREE MORE MEASURED GAPS ON THE COMPOSITION PATH, AND NO GATE IN THE TREE SEES ANY OF "
 "THEM** [NEW — 0] — **lane P measured each on a live render rather than reading it off a "
 "file.** (i) **a nested bento cannot carry its own column count below 1100px**: the compiled "
 "bands re-declare `--bento-cols-now` on the grid and answer the WALL, not the window, so a "
 "one-column inner wall 896px wide rendered as three columns and its dominant tile came out "
 "296px instead of 896 — the per-instance dial the token's own `$note` promises is reachable "
 "only for full-width inner walls; (ii) **canon CLIPS SILENTLY when DP-18 is broken** — a 694px "
 "list stretched a row to 791px inside a wall canon fixes at 320px and `.c-bento{overflow:"
 "hidden}` swallowed it with **no symptom in the DOM and `pageErrors: []`**; (iii) **no gate "
 "reads the composition of a page that LINKS `canon.css`** — `_validate_composition.py` reads "
 "the grammar from the artefact's own `@container` blocks, so the orphan-cell arithmetic `DP-16` "
 "and `s249-D5` rest on cannot be checked on a linked page at all, and this is the first such "
 "page in the tree. ⛔ **Ten gaps were named in total (`G1`…`G10`) and `_validate_compose.py` "
 "ignoring its path argument is one of them.** ⚠ **None is fixed and none is ruled** — every one "
 "is a generator or gate change. Receipt: "
 "`notes/_subreports/2026-09-19-288-P-composition-probe.md` §7–8.",
]

for old, new in STRIKES:
    assert aged.count(old) == 1, f"headline did not match exactly once: {old[:70]!r}"
    aged = aged.replace(old, new)

head, body = aged.split(":**", 1)
assert head == "> **residual → #288", repr(head)
newline = "> **residual → #289:** " + " · ".join(NEWITEMS) + " · " + body.strip()

after = len(cg._carry_items(newline))
print(f"carries: #288 {before} items  ->  #289 {after} items   "
      f"(+{after - before}; {len(NEWITEMS)} new written, {len(STRIKES)} struck, "
      f"{n_new} of #288's own new items aged in)")

# ---- splice the new section in, NEWEST FIRST ---------------------------------------------------
ANCHOR = "## residual → #288"
assert text.count(ANCHOR) == 1
block = "## residual → #289\n\n" + newline + "\n\n" + ANCHOR
out = text.replace(ANCHOR, block, 1)
assert out.count("## residual → #289") == 1
assert src in out, "POST-CONDITION FAILED: the #288 line did not survive verbatim"

if "--write" in sys.argv:
    open(CARRIES, "w", encoding="utf-8").write(out)
    print("WROTE _CARRIES.md § residual → #289")
else:
    print("DRY — pass --write to land it")
