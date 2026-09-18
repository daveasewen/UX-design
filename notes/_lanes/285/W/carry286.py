#!/usr/bin/env python3
"""#285 wrap — build `_CARRIES.md` § `## residual → #286` from § `## residual → #285`.

ONE programmatic pass, the #261…#284 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) TWO STRIKES, each carrying its receipt (`s183-D1` strike form, `s188-D2` receipt):
      · #284's NEW item ③ claimed the 40 masters were "DRAWN AND ACCEPTED BY EYE". ⛔ **DAVE
        REOPENED HIS OWN ACCEPTANCE AT #285** with a 4x crop of the wordmark — *"the word mark
        is distorted, look at the B"* — so the acceptance half of that claim was FALSE for the
        artefacts it named. The masters were REGENERATED and RE-ACCEPTED on different files.
        Struck in place, receipt named, BODY NOT RE-TYPED; the current state is NEW item ②.
      · #274's item ⑦ claimed the showroom "HAS NOW BEEN 108 PAGES STALE FOR TWO CONSECUTIVE
        WRAPS". ⛔ **RE-SYNCED AT #285 in `ff354475`** — 108 pages rewritten, one line each,
        `:is(` → `:where(`, verified by decoding all 108. Struck with its receipt.
  (c) EIGHT new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
⚠ NOT struck, and each for a stated reason:
  · **the masters carry at `[2]→[3]`** (#282's ① "THE LOGO MASTERS AND THE THIRD DIAL") — its
    close condition is REGISTRATION in `_logo_nodes.json`, behind the `gen_kg_icons.py` fence,
    and that is untouched. An acceptance is not the row's close condition; row `W-285lm` stays
    OPEN by the commit lane's own amendment.
  · **#255's item ⑨ ("SIXTY OF THE 136 SHOWROOM PAGES ARE STALE")** — its headline records an
    ACT ("this wrap declared the gap rather than regenerating them"), which stays true however
    the tree moves. `s271-D4`: a strike that is wrong is worse than an item that is merely
    stale. The staleness half is discharged and is said in NEW item ④, not by editing theirs.
  · the delegation lapse, the hard-wall question, the git-lock runbook line, the four
    generators, `col26-012`, the boot ceiling, `s277-D12`, the `#243` not-a-wrap form,
    `jade-lifestyle`, the third dial, the theory door, the `_gauge_tokens.py` 256,000 wording
    fix, the two-probe-shape question — every one ages and none is touched.
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #285:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) TWO strikes, each with its receipt -------------------------------------------------
STRIKES = [
 (("⬛ **③ THE 40 MASTERS ARE DRAWN AND ACCEPTED BY EYE; THE REGISTRATION IS OWED** [1, DAVE'S]"),
  ("⬛ ~~**③ THE 40 MASTERS ARE DRAWN AND ACCEPTED BY EYE; THE REGISTRATION IS OWED**~~ ⛔ **STRUCK "
   "AT THE #285 WRAP — THE ACCEPTANCE HALF IS RETRACTED BY DAVE HIMSELF, AND THE RETRACTION NAMES "
   "ITS RECEIPT (`s183-D1` strike form, `s188-D2` receipt): HE REOPENED HIS OWN #284 ACCEPTANCE.** "
   "On a 4x crop of the #284 wordmark his words were ***\"Maybe we misunderstand each other on the "
   "logo scaling, see image the word mark is distorted, look at the B\"*** — and he was right twice "
   "over. Lane LM2 found **two** causes in `snap_wordmark()`, not the one the task named: per-node "
   "snapping of straight segments inside curved glyphs (S, B, C) while the cubic control points "
   "stayed unsnapped, which kinks every bowl at the join; and **the wordmark was never scaled "
   "uniformly** — `kx/ky` measured **1.0039 / 0.9949 / 1.0436 / 0.9949 / 0.9896** (written with "
   "slashes, not the middot the carry set splits on), so at h=32 it was "
   "drawn **4.4% wider than tall**. ⚠ **The #284 lane's own probes could not see it** (they counted "
   "anti-aliased pixels and stem runs, neither of which can see an aspect error) and **the #284 wrap "
   "published the acceptance as a measurement of the world.** Regenerated as ONE uniform scale "
   "`s = h/85` plus ONE translation applied to nodes AND control points; lane V's adversarial check "
   "reads **16/16 PASS** with max residual **5.4e-5 px** against the Figma source. Dave's word on the "
   "regenerated sheet: ***\"2. accept\"***. Correction inscribed at "
   "`notes/_lanes/285/DAVE-RULINGS-2026-09-18.md`, `notes/_subreports/2026-09-18-285-LM2-logo-masters-regen.md` "
   "and `notes/_subreports/2026-09-18-285-V-verifier.md`, commit `b99d092c`; the row amendment is in "
   "`ff354475`. ⛔ **THE REGISTRATION HALF IS NOT STRUCK AND IS NOT CLOSED** — `_logo_nodes.json` is "
   "still untouched behind the `gen_kg_icons.py` fence, row `W-285lm` stays OPEN, and its "
   "`closes_when` was not invented or rewritten. The original item follows unedited. [1, DAVE'S]")),

 (("⚠ **⑦ THE SHOWROOM HAS NOW BEEN 108 PAGES STALE FOR TWO CONSECUTIVE WRAPS AND THE DIFF IS "
   "STILL A SPECIFICITY CHANGE** [11, DAVE'S]"),
  ("⚠ ~~**⑦ THE SHOWROOM HAS NOW BEEN 108 PAGES STALE FOR TWO CONSECUTIVE WRAPS AND THE DIFF IS "
   "STILL A SPECIFICITY CHANGE**~~ ⛔ **STRUCK AT THE #285 WRAP — RE-SYNCED, AND THE RETRACTION "
   "NAMES ITS RECEIPT (`s183-D1` / `s188-D2`): commit `ff354475`, cut on Dave's own *\"1. go\"*.** "
   "`python3 knowledge/gen_showroom.py` — the one remedy the gate itself names, and no other "
   "generator was run — wrote **137 page(s) -> showroom/ (108 written, 0 orphan(s) pruned)**. The "
   "diff is **108 files changed, 108 insertions(+), 108 deletions(-)**, ONE changed line per page, "
   "and lane C2 verified it **by decoding all 108 base64 payloads rather than sampling**: "
   "non-payload lines byte-identical in all 108, and in all 108 the single changed line is the old "
   "line with `:is(` → `:where(` and nothing else. ⚠ **AND THE `138 v 108` HALF IS EXPLAINED RATHER "
   "THAN INHERITED:** `showroom/` holds **138** top-level `.html` = **137 generator-owned + "
   "`index.html`, which `gen_library_214.py` owns**; the 108 are the stale SUBSET of the 137, so "
   "**108 ⊂ 137 ⊂ 138** and the two figures were never in tension. Nothing was deleted, moved or "
   "pruned. Inscribed at `notes/_subreports/2026-09-18-285-C2-showroom.md` §§ *The diff* and *The "
   "138-vs-108 measurement*. The original item follows unedited. [11, DAVE'S]")),
]
for old, new in STRIKES:
    assert aged.count(old) == 1, f"headline did not match exactly once: {old[:70]!r}"
    aged = aged.replace(old, new)

# ---- (c) the session's EIGHT new items ------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
NEWITEMS = [
 "⬛ **① THE CONNECTOR ANSWER CAME BY ACT — #286 MEASURES BOOT COLD** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call for what happens AFTER the reading; the act "
 "itself is already his. **The question was #284's carry ④ — *which connectors Apollo needs* — and "
 "he did not answer it in words. He answered it in the Tool-permissions panel: he set the built-in "
 "Browser's SEVENTEEN tools to BLOCKED** (screenshot read in-seat), and the `mcp__Claude_Browser__*` "
 "server dropped out of the conductor's tool set inside the same session. ⇒ **#286'S FIRST MOVE IS "
 "A MEASUREMENT, NOT A LANE: read boot COLD at the opener and compare against today's 80,863 real, "
 "ONE variable changed.** ⚠ **Skills are untouched BY DESIGN** — a second run, and only if the "
 "first moves. His setup as he described it: *\"this is how the setup stand now\"* · *\"I havnt "
 "touched anything and computer use is off\"*; connectors Browser (now blocked), Claude Docs, Claude "
 "in Chrome, GitHub; skills dave-voice, dream-pass, swiss-design-system, gtb-brand (off), docs, "
 "deep-research, import-memory. On deep-research: *\"but deep research might be useful no? is it "
 "big\"* — KEPT; a skill costs its description only (~80 tokens). ⛔ **NOTHING IS INSCRIBED: the boot "
 "ceiling stays 70,000, SHRINK-ONLY, and what to detach next is his.** Receipts: "
 "`notes/_lanes/285/DAVE-RULINGS-2026-09-18.md` § THE CONNECTOR ANSWER, BY ACT · `_HANDOFF-136`.",

 "⬛ **② THE MASTERS ARE REGENERATED AND RE-ACCEPTED, AND THE REGISTRATION IS STILL THE OPEN HALF** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call for the registration only; the acceptance is his "
 "and is quoted. ✅ **RE-ACCEPTED:** ***\"2. accept\"*** — replacing the #284 acceptance **he "
 "reopened himself** with the B crop (struck above, receipted). The wordmark now moves RIGIDLY: "
 "`quantise_runs()` DELETED (32 lines), `snap_wordmark()` rewritten 43 → 30 lines as one uniform "
 "scale `s = h/85` — the same factor the hexagon is drawn at, so the lockup relationship is exact — "
 "plus one translation applied to **nodes and control points alike**; `snapped_nodes` is `0` and the "
 "report asserts it. The 20 `hexagon-*` masters are **byte-identical to HEAD**. Verifier: **16/16 "
 "PASS**, max residual **5.4e-5 px** vs the Figma source, two caveats carried (one wording, one a "
 "sub-pixel property inherited from the source, neither a defect). ⛔ **STILL OWED AND STILL HIS: "
 "registration in `_logo_nodes.json`**, which needs a sanctioned run of `gen_kg_icons.py` — one of "
 "the four generators that undo hand-authored state — so **HOW** is his word. Row `W-285lm` stays "
 "OPEN with `closes_when` UNCHANGED; the eye-half is recorded in the row's `body`, not by inventing "
 "a close condition. Receipts: `b99d092c` · `ff354475` · "
 "`notes/_subreports/2026-09-18-285-LM2-logo-masters-regen.md` · `…-285-V-verifier.md`.",

 "⬛ **③ `knowledge/_standing.md` IS A DRAFT AND ITS EIGHT LINES ARE HIS TO RATIFY** [NEW — 0, "
 "DAVE'S] — put to Dave at the wrap call; ⛔ **NOT INSCRIBED — the seam RE-QUOTES, it never "
 "inscribes, and its own header says *\"DRAFT — Dave's approval pending; nothing here is inscribed "
 "by this file\"*.** He cut the lane in his own words — ***\"yes to the seam re-quoting the standing "
 "constraints\"*** — on the messy-middle finding he had just read (*\"Okay this sound good.\"* to "
 "the conductor's read that only tactic 1, front-load rules and re-quote constraints at the tail, is "
 "usable in Cowork; output-priming is API-only, hygiene and retrieval are already the chain's "
 "rules). `_seam.py` now prints a FOURTH block, **LAST**, after SCRATCH — the recency end, which is "
 "the whole mechanism: everything read at an opener becomes the MIDDLE the moment work starts. "
 "Measured at this seat: **8 lines · 246 cl100k**. ⚠ **WHAT IS HIS IS THE WORDING OF THE EIGHT, "
 "line by line** — each was drafted FROM THE RECORD with its receipt in parentheses, and a drafted "
 "constraint is not a ruled one. Row `W-285sc` is open on exactly this. ⚠ **AND THE COUNTING SITE "
 "IT ADDED WAS BORN UNREGISTERED** — see ⑦. Receipts: "
 "`notes/_lanes/285/DAVE-RULINGS-2026-09-18.md` · `notes/_subreports/2026-09-18-285-SC-seam-standing.md` "
 "· `knowledge/_standing.md` · `b99d092c`.",

 "⬛ **④ THE SHOWROOM IS RE-SYNCED AND `138 v 108` IS AN EXPLANATION, NOT AN INHERITANCE** [NEW — 0] "
 "— a closure with receipts, recorded so the next wrap does not re-declare a gap that is gone. Cut "
 "on his ***\"1. go\"***; landed `ff354475`. **108 pages, one line each, `:is(` → `:where(`, "
 "verified by decoding all 108 rather than sampling.** **138 = 137 generator-owned + `index.html`** "
 "(owned by `knowledge/_render/gen_library_214.py`), and the 108 are the stale subset of the 137: "
 "**108 ⊂ 137 ⊂ 138**. ⚠ **`SHOWROOM_ACK` SHOULD NO LONGER BE NEEDED TO PASS THE `s191-D1` GATE ON "
 "A CLEAN TREE, AND THAT IS A PREDICTION UNTIL THE NEXT COMMIT MEASURES IT** — this wrap's own "
 "commit is the first test. ⚠ **#255's item ⑨ is NOT struck** (it ages beside this one): its "
 "headline records an ACT, and `s271-D4` says a wrong strike is worse than a stale item. Receipts: "
 "`notes/_subreports/2026-09-18-285-C2-showroom.md` · `ff354475`.",

 "⬛ **⑤ THE DELEGATION RULE WAS OBEYED FOR A WHOLE SESSION, AND THE MEASUREMENT IS THE ARGUMENT** "
 "[NEW — 0] — the counter-measurement to the lapse that ages beside this one at age 1 (written in words, not a bracket, so the probe does not read it as a second carry), and ⛔ **it "
 "does NOT close that carry, which is ruling-shaped and still his.** Measured at this seat from the "
 "conductor's own transcript: **SEVEN lanes, every one an `Agent` at `spawnDepth 1`, model opus** — "
 "LM2 (masters regen) · SC (seam standing) · V (adversarial verifier) · C (commit) · C2 (showroom "
 "commit) · P (push) · W (this wrap, on its second attempt). **NO lane work was done in seat.** The "
 "conductor's in-seat tool output was three seam reads, one tiktoken measure, two directory "
 "listings, four image reads and one shot read. ★★ **THE PRICE, BOTH SIDES: the seven lane replies "
 "cost the conductor's window 3,382 cl100k IN TOTAL — the `s218-D7` stub contract working — against "
 "≈738,851 real of sub FILL across the seven seats.** ⇒ **the shape #284's carry ① asks for is "
 "affordable and was affordable today**; whether it becomes a rule is still his sentence to "
 "inscribe. Receipts: this wrap's filed report § THE DELEGATION MEASUREMENT · the seven "
 "`notes/_subreports/2026-09-18-285-*.md`.",

 "⚠ **⑥ A WRAP SUB CAN DIE MID-RITUAL ON A NETWORK ERROR — ONE DID TODAY, AND IT WROTE NOTHING** "
 "[NEW — 0] — named because the NEXT one may not be so lucky, not because anything is broken. "
 "#285's first wrap sub reached **five reads and 90,605 real** and then took "
 "`API Error: Can't reach the API server — check your internet or DNS (ENOTFOUND)` at "
 "**14:52:22Z**, 11 usage records in, and stopped. ✅ **IT HAD WRITTEN NOTHING, SO THERE WAS NO "
 "HALF-STATE TO REPAIR** — `notes/_lanes/285/W/` was empty when the retry opened, and the tree was "
 "exactly as the lanes left it. ⛔ **THAT IS LUCK, NOT DESIGN.** A sub that died AFTER a 2c move and "
 "BEFORE its receipt was read back would leave a half-rolled banner with green receipts nobody "
 "read, which is the #166 stale-msgfile shape arriving by a different door. ⚠ **RULING-SHAPED AND "
 "NOT INSCRIBED: whether the ritual owes a RESUME contract** — a written marker of which steps have "
 "landed, so a retry can tell a fresh tree from a half-rolled one. The all-or-nothing guarantee "
 "`_gm_move.py` gives is PER-TRANSACTION, never across the ritual. Receipt: the dead sub's own "
 "transcript tail, quoted in this wrap's filed report § Finding 5.",

 "⚠ **⑦ `_seam.py` WAS AN UNREGISTERED MEASURER FROM THE MOMENT IT GAINED A COUNTER, AND THIS SEAT "
 "REGISTERED IT** [NEW — 0] — closed, and recorded because the SHAPE will recur. Lane SC added "
 "`standing_tokens()` to `knowledge/_seam.py` in `b99d092c`; `ds-021 (C)` went RED at the wrap gate "
 "— *\"counts tokens (cl100k) and is NOT in MEASURERS — an UNREGISTERED measurer\"* — so **SEVEN "
 "blocking fails stood at this ritual's open and SIX at its close.** Registered here as "
 "**`estimate-only`**, the `_compose_slice.py` precedent (#270 wrap) exactly: it encodes with "
 "tiktoken cl100k only, never calls `_gauge_tokens.count()`, has no API path, and its figure is "
 "never a FILL or budget claim. ⛔ **A DECLARATION, NOT A RULING**, and it was **this seat's fail to "
 "close rather than an inherited one** — the gate fired on a counting site born in this session's "
 "own commit. ★ **The general form is worth the line: a lane that adds a counter adds a gate "
 "obligation, and the gate finds out at the wrap.** Receipts: `knowledge/_capture_gate.py` § "
 "`MEASURERS[\"_seam.py\"]` · `b99d092c`.",

 "⚠ **⑧ `_seam.py`'s SCRATCH ARM DELETES A LANE'S OWN `/tmp` WORKING FILES MID-RUN, BY DESIGN, AND "
 "IT WILL BITE** [NEW — 0] — lane V's carried note, verified in the seam's own docstring, **not "
 "fixed here** because changing what an instrument removes changes what it claims. `_seam.py` runs "
 "at EVERY seam and cleans *\"the current user's own top-level entries under `/tmp` and "
 "`/var/tmp`\"* with ONE keep-list (`/tmp/gitshim`). A lane holding working files there loses them "
 "the moment the conductor reads the next seam — **the lane is not the process that cleans, so it "
 "gets no warning and no receipt.** ⚠ **The defence that worked today was a convention, not a "
 "guard:** every ops file, builder and msgfile of this wrap lives under `notes/_lanes/285/W/`, "
 "which `s218-D7` clause 3 already requires for evidence. ⛔ **RULING-SHAPED AND NOT INSCRIBED: "
 "whether the keep-list grows, whether the clean becomes opt-in at a seam, or whether lanes are "
 "simply forbidden `/tmp` — all three are his.** ⚠ Sibling, and NOT the same item: `s283-D1`'s "
 "scratch clean is what 4c also does, and the 4c/step-5 collision that ages at age 2 (in words, not a bracket, for the same reason) is CLOSED; "
 "this is a different surface. Receipts: `notes/_subreports/2026-09-18-285-V-verifier.md` · "
 "`knowledge/_seam.py` § SCRATCH.",
]

body = aged[len("> **residual → #285:** "):]
newline = "> **residual → #286:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d ; strikes %d"
      % (before, n_new, after, len(NEWITEMS), len(STRIKES)))

SECTION = "## residual → #286"
assert SECTION not in text, "section already exists"
anchor = "## residual → #285"
i = text.index(anchor)
if "--write" not in sys.argv:
    print("DRY — nothing written"); sys.exit(0)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
