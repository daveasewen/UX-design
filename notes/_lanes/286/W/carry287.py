#!/usr/bin/env python3
"""#286 wrap — build `_CARRIES.md` § `## residual → #287` from § `## residual → #286`.

ONE programmatic pass, the #261…#285 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) TWO STRIKES, each carrying its receipt (`s183-D1` strike form, `s188-D2` receipt);
  (c) NINE new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

⚠ TWO THINGS THE WRAP BRIEF NAMED AS STRIKES ARE DELIBERATELY *NOT* STRUCK, and the reason is
`s271-D4`'s own warning that a wrong strike is worse than a stale item:

  · **the 256,000 wording fix** is HALF of #284's item ② ("THE CONTEXT-WINDOW FINDING, AND
    DAVE'S CORRECTION OF WHAT IT MEANS"). The headline records a FINDING and HIS CORRECTION,
    both of which stay true; only the un-ordered wording edit moved, and only in the gauge.
    Its discharge — and the 58 prose locations still owed — is said in NEW item ④ instead.
  · **#285's moves 2 and 3** are HALF of #285's item ④ ("THE COMMIT TOOK SIX RUNS, AND TWO OF
    THEM WERE A STRANDED `index.lock`"). That headline records what happened at #284 and stays
    true however the tools change. The build is said in NEW item ⑤ instead.

⚠ ALSO NOT STRUCK, each for a stated reason:
  · **#282's ① "THE LOGO MASTERS AND THE THIRD DIAL"** — two things; the masters half is
    discharged and **the third dial is untouched and still his**, so the item ages whole.
  · **#255's ⑨ (sixty of 136 showroom pages)** — its headline records an ACT, per #285.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #286:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) TWO strikes, each with its receipt ---------------------------------------------------
STRIKES = [
 ("⬛ **② THE MASTERS ARE REGENERATED AND RE-ACCEPTED, AND THE REGISTRATION IS STILL THE OPEN "
  "HALF** [1, DAVE'S]",
  "⬛ ~~**② THE MASTERS ARE REGENERATED AND RE-ACCEPTED, AND THE REGISTRATION IS STILL THE OPEN "
  "HALF**~~ ⛔ **STRUCK AT THE #286 WRAP — THE OPEN HALF IS CLOSED, AND THE STRIKE NAMES ITS "
  "RECEIPT (`s183-D1` strike form, `s188-D2` receipt).** Dave released the `gen_kg_icons.py` fence "
  "with ***\"okay go on everything\"*** and then named the SHAPE with ***\"okay "
  "size-on-the-existing-node\"*** — so a master is a **SIZE FIELD on its lockup's existing node, "
  "never its own node**, and lane R's shapes 2 (40 new `logo:<stem>-<h>` nodes) and 3 (a new "
  "`logoMaster:` kind) are refused by that sentence. Lane R2 wrote a `sizes` map onto all **8** "
  "existing nodes, five raw heights each (24/28/32/36/40) = the 40 masters, merge-on-write. "
  "✅ **VERIFIED AT THE #286 WRAP SEAT BY `json.load` RATHER THAN FROM THE LANE'S PROSE: 8 nodes "
  "(unmoved) · 33 edges (unmoved) · 8 of 8 nodes carrying `sizes` with exactly five keys · 12 "
  "`governedBy` edges intact.** Row `W-285lm` is CLOSED. ⚠ **THE FIELD'S KEY NAME IS NOT HIS "
  "WORD** — he named the location, not the spelling; `sizes` is the lane's reading of the file's "
  "own plural vocabulary (`nodes`, `edges`, `unresolved`, `fills`) and is recorded as the lane's "
  "reasoning. ⚠ **AND LANE R FIRST REPORTED THE MASTERS NOT REGISTRABLE** — the generator is "
  "blind to `masters/` — which is why R2 exists at all; both readings stand. Correction inscribed "
  "at `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md`, "
  "`notes/_subreports/2026-09-18-286-R-masters-registered.md` and "
  "`notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md`, commit `7ed49d37`. "
  "⛔ **THE KG EXPLORER IS NOT REBUILT TO SHOW THE NEW FIELD — see the new items.** The original "
  "item follows unedited. [1, DAVE'S]"),

 ("⬛ **③ `knowledge/_standing.md` IS A DRAFT AND ITS EIGHT LINES ARE HIS TO RATIFY** [1, DAVE'S]",
  "⬛ ~~**③ `knowledge/_standing.md` IS A DRAFT AND ITS EIGHT LINES ARE HIS TO RATIFY**~~ "
  "⛔ **STRUCK AT THE #286 WRAP — THE FILE IS OUT OF DRAFT, AND THE STRIKE NAMES ITS RECEIPT "
  "(`s183-D1` / `s188-D2`).** His word came as the first item of an opener that named exactly this: "
  "***\"okay go on everything\"***. Lane S rewrote the header in `1caaa0b1`; measured at the #286 "
  "wrap seat against `09ddf155`, the change is **8 insertions and 3 deletions in ONE hunk, entirely "
  "above the `---` rule**, and the **eight lines are BYTE-IDENTICAL** (936 B of body, compared "
  "programmatically, not by eye). Row `W-285sc` is CLOSED. ⚠ **AND THE JOIN IS RECORDED RATHER "
  "THAN SMOOTHED: reading *\"go on everything\"* as ratification of the WORDING AS WRITTEN is the "
  "CONDUCTOR'S reading, not Dave's sentence** — he did not say \"as written\", did not quote a line "
  "and did not say \"ratified\"; `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md` says so in its own "
  "words, and the new header cites it, **so the act stays reversible by one word from him**. "
  "⚠ **WHETHER THAT SENTENCE IS INSCRIBED AS A RULING WAS PUT TO DAVE AT THE WRAP CALL AND IS NOT "
  "THE WRAP'S TO DECIDE** — `knowledge/_rulings.json` stays at 620. ⚠ **`knowledge/_seam.py` STILL "
  "CALLS THE FILE A DRAFT AT EVERY SEAM and was NOT edited** — see the new items. Receipts: "
  "`notes/_subreports/2026-09-18-286-S-standing-ratified.md` · `1caaa0b1`. The original item "
  "follows unedited. [1, DAVE'S]"),
]
for old, new in STRIKES:
    assert aged.count(old) == 1, f"headline did not match exactly once: {old[:70]!r}"
    aged = aged.replace(old, new)

# ---- (c) the session's NINE new items ---------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING. Ten words.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age — #285's accidental-visibility trap). Ages spelled in words.
NEWITEMS = [
 "⬛ **① THE CONNECTOR LEVER READS −7,031 AND THE CEILING STILL STANDS** [NEW — 0, DAVE'S] — put "
 "to Dave at the wrap call for what happens NEXT; the act that produced the reading is already "
 "his. **BOOT COLD 73,832 real (n=1) against #285's 80,863 — delta −7,031 — with ONE variable "
 "changed:** the built-in Browser connector's 17 `mcp__Claude_Browser__*` tools set to BLOCKED. "
 "Held constant BY DESIGN: skills untouched, computer use off, the other three connectors on "
 "(Claude Docs, Claude in Chrome, GitHub). ★ **The cleanest one-variable boot experiment this "
 "record carries.** ⛔ **AND IT IS ONE READING AGAINST ONE READING, WHICH IS NOT A CAUSE.** The "
 "last seven post-diet readings span **72,110–83,636, a spread of 11,526 — WIDER than the delta "
 "being claimed** — so the direction is consistent with the block having worked and **the "
 "magnitude is not established**. **What would make it a verdict is named and NOT done: a second "
 "cold boot on the same setup**, same instrument, first turn. ⛔ **73,832 IS 3,832 OVER "
 "`BOOT_CEILING_TK` 70,000 — THE ELEVENTH POST-DIET READING OVER IT — AND THE LITERAL IS "
 "SHRINK-ONLY** (`s240-D2`/`s241-D1`): a 7K improvement is progress toward the number, never a "
 "licence to raise it, and raising it is his word alone. ⛔ **THE NEXT LEVER IS NAMED AND NOT "
 "RANKED:** boot's decomposition into system prompt / tool schemas / deferred-tool list / MCP "
 "instructions is `ds-025` item 1 and **still dark from every mount**, so no connector is ranked "
 "and no saving is predicted. Receipts: `notes/_lanes/286/BOOT-COLD-2026-09-18.md` (deliberately "
 "NOT in `notes/_GAUGE-LOG.md`, so the figure cannot become a double-count) · "
 "`notes/_subreports/2026-09-18-286-G-gauge-wording-and-boot-cold.md` · the `post-mortem #286:` "
 "line, which states the figure ONCE (`s241-D2`).",

 "⬛ **② DAVE SPOKE TWICE AND NEITHER SENTENCE IS INSCRIBED — WHETHER THEY BECOME RULINGS IS HIS** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call, and this is the whole of it. His two sentences "
 "today, verbatim: ***\"okay go on everything\"*** — his entire reply to an opener naming three "
 "items (the eight standing lines' wording, HOW the masters get registered, the 256,000 wording "
 "fix) plus the cold-boot question — and ***\"okay size-on-the-existing-node\"***, answering the "
 "SHAPE of a master registration. ⛔ **BOTH ARE RECORDED AS HIS WORDS AND NEITHER IS INSCRIBED: "
 "`knowledge/_rulings.json` reads 620 at the open and at the close, and no `s286-` id exists in "
 "the store** (`json.load` at the wrap seat, not restated from the brief). ⚠ **The acts taken on "
 "them are real and are receipted** (the standing file out of DRAFT, the masters registered) — "
 "**an act is not an inscription**, and `s271-D4` is the reason the distinction is kept: an item "
 "written before his answer is a QUESTION PUT, never a state of the world. ⛔ **WHETHER EITHER "
 "SENTENCE SHOULD BECOME A RULING IS HIS AND WAS NOT DECIDED BY THE WRAP.** Receipt: "
 "`notes/_lanes/286/DAVE-RULINGS-2026-09-18.md`, which records both sentences AND the conductor's "
 "own reading of the first, marked as the conductor's.",

 "⬛ **③ THE MASTERS' FIELD KEY IS THE LANE'S SPELLING, NOT HIS — AND THE EXPLORER CANNOT SEE IT** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call. He named the LOCATION (*\"size-on-the-existing-"
 "node\"*) and **did not name the SPELLING**; lane R2 chose **`sizes`** by reading the file's own "
 "plural vocabulary (`nodes`, `edges`, `unresolved`, `fills`) and recorded that as its reasoning "
 "rather than as his word. ⛔ **SO THE KEY NAME IS RULING-SHAPED AND OPEN**, and a later rename is "
 "a one-pass edit while nothing reads it. ⛔ **AND NOTHING READS IT YET: THE KG EXPLORER WAS NOT "
 "REBUILT** to show the new `sizes` map — declared here rather than discovered later, the "
 "[[instrument-without-a-consumer]] shape. Receipts: "
 "`notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md` · `knowledge/_logo_nodes.json` "
 "· `7ed49d37`.",

 "⬛ **④ THE 256,000 WORDING IS FIXED IN THE GAUGE AND 58 PROSE LOCATIONS ARE STILL OWED** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call, because **every one of the 58 is ratified "
 "runbook or ruling text and amending it is his word alone.** ✅ **DONE:** "
 "`knowledge/_gauge_tokens.py` **+25/−3 with the CONSTANTS UNCHANGED** — `BUDGET_HARD` is still "
 "`256_000`; **the defect was never the number, it was the word next to it.** ⛔ **OWED: 58 "
 "locations across 10 live files still call 256,000 a wall or a hard line**, counted by a named "
 "probe (`256,000|256000|256_000|256K`, filtered to lines also carrying *hard* or *wall*): "
 "`_RUNBOOK-context-gauge.md` seven, `notes/_MEMENTO-DECISIONS.md` ten, `knowledge/_rulings.json` "
 "ten, `notes/_RULINGS.html` nine, `knowledge/_state.json` eight, `_LIVE-STATE.md` seven, "
 "`GOOD-MORNING.md` three, `_CHAIN.md` two, `dashboard/index.html` one, `knowledge/_standing.md` "
 "one (already correct). ★ **The sharpest is `_RUNBOOK-context-gauge.md:85` — *\"⛔ 256,000 stays "
 "the UNQUALIFIED wall (`s214-D2`)\"*** — and `:926`'s *\"256,000 is the absolute hard stop\"*. "
 "⚠ **THIS IS MINTED AS A NEW CARRY RATHER THAN FOLDED INTO #284'S ITEM ②, WHICH IS NOT STRUCK:** "
 "that headline records the FINDING and HIS CORRECTION, both still true, and a strike that is "
 "wrong is worse than an item that is merely stale (`s271-D4`). Receipt: "
 "`notes/_subreports/2026-09-18-286-G-gauge-wording-and-boot-cold.md` § OWED.",

 "⚠ **⑤ THE SEAM'S `INSEAT` ARM AND `--quiet` ARE BUILT, AND THE 10,000 IS *PICKED*, NOT RULED** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call for the NUMBER and its PLACEMENT only; the "
 "build is done. **#285's moves 2 and 3 landed:** `knowledge/_seam.py` **+214/−6** gains an "
 "`INSEAT` block that reads the conductor's OWN transcript (non-sidechain `tool_result` blocks), "
 "counts what has landed IN SEAT since the last seam against a gitignored marker, and warns past "
 "`INSEAT_WARN_TK`; `--no-inseat` suppresses it and does not move the marker. "
 "`knowledge/_git_commit.sh` **+60/−1** gains `--quiet`, answering the measured ~30K of "
 "commit-script output that cost #284's conductor his own window. ★ **The arm turns #284's "
 "delegation argument from prose that lived once in a handoff into a number that fires while the "
 "session can still change course** — the `_seam.py` move of #283, applied to a second quantity. "
 "⛔ **`INSEAT_WARN_TK = 10_000` IS PICKED AND THE FILE SAYS SO ITSELF** (the same standing as "
 "`DISK_WARN_PCT`), reasoned between a conductor's ~45K of in-seat lane work and a delegated "
 "lane's ~300 — **both the figure and the block's placement are his.** ⚠ **NOT STRUCK AND NOT "
 "FOLDED: #285's item ④ (the commit took six runs) keeps its headline**, which records what "
 "happened at #284 and stays true however the tools change. Receipt: "
 "`notes/_subreports/2026-09-18-286-T-seam-inseat-and-quiet-commit.md`.",

 "⚠ **⑥ `knowledge/_seam.py` STILL CALLS `_standing.md` A DRAFT AT EVERY SEAM, AND THE LINE NUMBER "
 "IS DISPUTED** [NEW — 0, DAVE'S] — a stale claim inside a LIVE instrument, found at the #286 wrap "
 "and **NOT edited**, because the seam's own text belongs with whoever rules on the seam. The line "
 "reads *\"`knowledge/_standing.md` is a DRAFT until Dave approves it; the seam re-quotes, it never "
 "inscribes\"* and it has been FALSE since `1caaa0b1`. ⛔ **THE WRAP BRIEF LOCATES IT AT `:26` AND "
 "THE WRAP SEAT MEASURES `:44` — BOTH READINGS ARE PUBLISHED AND NEITHER IS REWRITTEN.** ⚠ **The "
 "second half of the sentence is still TRUE and must survive any edit** (the seam re-quotes, it "
 "never inscribes), which is exactly why this is a wording question and not a deletion. "
 "★ **General form, and it is the reason this is carried rather than dropped: a docstring that "
 "states a file's STATUS ages the moment the status changes, and no gate reads docstrings.** "
 "Receipt: `grep -n DRAFT knowledge/_seam.py` at the #286 wrap seat.",

 "⚠ **⑦ NINE LANES, NONE IN SEAT — THE DELEGATION RULE OBEYED A SECOND SESSION AND STILL "
 "UNINSCRIBED** [NEW — 0, DAVE'S] — the counter-measurement to the lapse that ages beside this one "
 "(written in words, not a bracket, so the probe does not read it as a second carry), and ⛔ **it "
 "does NOT close that carry.** Measured at the #286 wrap seat by IMPORTING `_checkin.read_fill` "
 "rather than re-implementing it, against the conductor's own transcript: **NINE lanes, every one "
 "an `Agent` at `spawnDepth 1`, model opus** — S 83,120 / R 93,872 / G 122,502 / T 145,539 / "
 "V 170,927 / C 101,132 / P 60,602 / R2 241,918 / C2 93,636 ⇒ **subs 1,113,248 real (n=9)**, QUOTA "
 "and never FILL. ★★ **THE PRICE, BOTH SIDES: the nine lane replies cost the conductor's window "
 "3,399 cl100k IN TOTAL** — the `s218-D7` stub contract working — **against 1,113,248 real of sub "
 "FILL**, roughly 0.3%; the nine briefs cost 10,528 cl100k to send. ⚠ **A TENTH SUB — THE WRAP "
 "SEAT ITSELF — IS DELIBERATELY EXCLUDED FROM THE FIGURE**, because its own total cannot be final "
 "from inside itself and `s214-D5` forbids turning an unknown into a number. ⇒ **two sessions' "
 "obedience is evidence the shape is affordable, not a rule that it is required, and his sentence "
 "is still uninscribed.** Receipts: this wrap's filed report § THE DELEGATION MEASUREMENT · "
 "`notes/_lanes/286/W/measure286.py` and `lanereplies286.py`.",

 "⚠ **⑧ AN ADVERSARIAL VERIFIER MUTATED THE TREE IT WAS VERIFYING, AND RESTORED IT BYTE-EXACT** "
 "[NEW — 0] — named, not called a defect, because the restore's exactness is what keeps it a note. "
 "Lane V read **24 of 24 testable claims PASS** across the S, R, G and T lanes — and in the "
 "course of it **overwrote `knowledge/_capture_gate.py` with HEAD mid-run and restored it "
 "byte-exact**, and **moved two symlink farms to `_to_delete/`**. ⚠ **A 24-of-24 pass from a seat "
 "that edited the gate it was measuring against deserves to say so out loud**, and a restore that "
 "was byte-exact is the only reason this is a method note rather than a finding about the result. "
 "⛔ **RULING-SHAPED AND NOT INSCRIBED: whether a verifier lane may mutate the tree at all**, and "
 "if so whether it owes a declared before/after digest rather than an assurance. Receipt: "
 "`notes/_subreports/2026-09-18-286-V-verifier.md`.",

 "⚠ **⑨ THE CLOUD MEMORY ARCHIVE IS AT 48,990 OF ITS 49,152 B CAP AND THE NEXT CUT MAY NOT FIT** "
 "[NEW — 0, DAVE'S] — measured at #285, met at #286, and it is **a measurement rather than a trim "
 "order.** The Project store's `index.md` keeps the newest THREE wrap lines and older ones move "
 "VERBATIM to `MEMORY-ARCHIVE.md`; that archive stood at **48,990 of 49,152 B** after #285's cut, "
 "leaving **162 B**. ⛔ **NOTHING IS TRUNCATED TO MAKE A MOVE FIT** — if the move is refused the "
 "older line STAYS in `index.md`, the hook's foot says so, and the shortfall is carried. "
 "⚠ **NOTHING IS AT RISK EITHER, AND THAT IS WORTH SAYING BESIDE THE ALARM:** the repo is the "
 "record and memory is the accelerator — the handoffs, dossiers, ledgers and git hold every one of "
 "those sessions in full. ⛔ **WHAT TO DO — condense, split, or something else — IS HIS, and the "
 "dream pass is its usual seat.** Receipt: `notes/_lanes/286/WRAP-MEMORY-HOOK.md` (result recorded "
 "at its foot, not assumed) · #285's filed report finding 10.",
]

body = aged[len("> **residual → #286:** "):]
newline = "> **residual → #287:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d ; strikes %d"
      % (before, n_new, after, len(NEWITEMS), len(STRIKES)))

SECTION = "## residual → #287"
assert SECTION not in text, "section already exists"
anchor = "## residual → #286"
i = text.index(anchor)
if "--write" not in sys.argv:
    print("DRY — nothing written")
    sys.exit(0)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
