#!/usr/bin/env python3
"""#279 wrap — build `_CARRIES.md` § `## residual → #280` from § `## residual → #279`.

ONE programmatic pass, the #261…#278 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ ONE SURGICAL EDIT, carrying its `s183-D1`/`s188-D2` receipt:
      · #279's ① ("LAND THE ICONS, THEN THE CONSTITUTION WAVE") asserted the thirteen `s277`
        rulings are "LAW and NOT IN THE TREE". #279 ENACTED eleven of them. The claim is
        CORRECTED, so the carry is STRUCK with the correction named — never re-typed.
  (c) the session's SEVEN new items written in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
"""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","..","..",".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #279:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the ONE surgical edit ------------------------------------------------------------
OLD = ("⬛ **① LAND THE ICONS, THEN THE CONSTITUTION WAVE — `s277-D4..D13`** [2, DAVE'S]")
NEW = ("~~⬛ **① LAND THE ICONS, THEN THE CONSTITUTION WAVE — `s277-D4..D13`** [2, DAVE'S]~~ "
       "⛔ **STRUCK AT THE #279 WRAP — THE WAVE LANDED AND THE STRIKE CARRIES ITS RECEIPT "
       "(`s183-D1` strike, `s188-D2` receipt).** The claim below — that `s277-D4`…`s277-D13` "
       "are *\"LAW and NOT IN THE TREE\"* — was TRUE when written at the #278 wrap and is FALSE "
       "now: #279 ENACTED ELEVEN OF THE THIRTEEN across ten lane commits. Correction inscribed "
       "at: `f641242` + `84658db` (icons, `s277-D4..D7`) · `d6bd57b` (the reader, `s277-D10` + "
       "`s277-D13` under `s278-D1`) · `9e7a158` + `e3facb4` (scope, `s277-D9`) · `2c6b640` + "
       "`9b2e1b0` (explorer v1.16, `s277-D8`) · `eb2ff7c` (the verbs, `s277-D11`) · `df33a24` + "
       "`3710d6b` (the pack at v2.1, `s279-D1`) · and `_HANDOFF-130-the-wave-lands-and-the-graph-"
       "question.md`. ⚠ **TWO THINGS SURVIVE THE STRIKE AND ARE CARRIED AS NEW ITEMS, NOT LEFT "
       "INSIDE A STRUCK ONE: `s277-D12` (tokens at group+tier) WAS NEVER STARTED — item ③ — and "
       "`s277-D8` IS ENACTED TO ITS LETTER AND REFUSED BY DAVE'S OWN EYE — item ①.**")
assert aged.count(OLD) == 1, ("strike anchor", aged.count(OLD))
aged = aged.replace(OLD, NEW, 1)

# ---- (c) the session's SEVEN new items ----------------------------------------------------
NEWITEMS = [
 "⬛ **① THE GRAPH IS NOT THREE LAYERS — THE LAYOUT QUESTION IS #280'S FIRST** [NEW — 0, DAVE'S] "
 "— put to Dave at the wrap call and NOT answered. He looked at explorer 1.16 and wrote, verbatim: "
 "*\"BTW do we still have work to do on the graph... this does not look like 3 layers, just "
 "relabelling and grouping them isn't what I expected tbh.\"* (`notes/_lanes/279/DAVE-RULINGS-"
 "2026-09-16.md` item 6). ⚠ **Neither the lanes nor the ruling as written are at fault:** "
 "`s277-D8` as inscribed says *storage untouched; chips and family labels change*, and EX/EX2 "
 "built exactly that and EV verified it. **What he expected is a LAYOUT — three visibly separated "
 "layers on the stage, not three labels over one force graph.** ⛔ **RULING-SHAPED AND NOT "
 "INSCRIBED**, because the option has never been put to him. **#280's FIRST move is a LAYOUT lane "
 "that renders ONE concrete option on a page for his eye, not a description of one.** Priced by "
 "lane EX2 already: the OFF-column band is **5,700 world units** between the base cluster "
 "(x ≤ 449) and the assets column (x ≥ 6,172); runtime column packing is **~25 lines** but it "
 "moves ghost positions, so chip-off canvas stops being pixel-identical to 1.15 and it needs its "
 "own lane with pixel proof. Receipts: `notes/_subreports/2026-09-16-279-EX2-explorer-fix.md` · "
 "`notes/_subreports/2026-09-16-279-EV-explorer-verify.md` · `9b2e1b0`.",

 "⬛ **② HIS 15-BASE EXPORT IS RECEIVED AND UNREAD BY THE RECORD — THE INSCRIBE LANE IS #280'S** "
 "[NEW — 0, DAVE'S] — `notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json`, "
 "received 15:55Z from the sheet lane AR built under `s277-D6` / `P-277-3` (15 bases · 31 "
 "\"active\" drawings · 46 glyphs; driver 36/36 green). Read but NOT inscribed: **15 of 15 choose "
 "a twin** (7 bare `-active`, 8 `-active-2`) and **12 of 15 flag or note a MISLABELED drawing** — "
 "his second defect, the exporter's, exactly as `s277-D6` recorded. ⚠ **Flag and note DISAGREE on "
 "`electricity`** (flag names the twin, note names `-active-2`), and **four rows are note-only**: "
 "`employee-banking-solution`, `financial-health-check`, `reward`, `jade-lifestyle` (*\"Im not "
 "certain\"*). ⛔ **TWO STANDING INSTRUCTIONS FOR THAT LANE: twins become `activeVariantOf` / "
 "`defaultActive` and mislabels join the exporter-defect list; and WHERE FLAG AND NOTE DISAGREE "
 "THE NOTE IS HIS SENTENCE — ASK, DO NOT GUESS.** The file was UNTRACKED at this ritual's open "
 "and is committed by it, so the citation resolves. Row: `W-279ar`.",

 "⬛ **③ `s277-D12` — TOKENS AT GROUP+TIER — WAS NEVER STARTED** [NEW — 0, DAVE'S] — of the "
 "thirteen `s277` rulings, twelve now have a lane behind them and this one has none: no lane was "
 "cut for it at #279 and no line of it exists in the tree. It is the one ruled-but-unbuilt item "
 "the wave leaves behind, and it is **#280's third move** after the layout question and the "
 "export. Context it rests on: `s269-D3` (*\"TOKENS ENTER THE GRAPH AT TIER GRAIN — semantic "
 "versus primitive — and NEVER as 932 leaf nodes\"*), the reader's tokens leg (25 groups in the "
 "live seed, `_compose_slice.py`), and lane SC's measured note that the reader's tier map holds "
 "**43** groups where the audit's ≈128 was `_blast-radius.json`'s LEAF count.",

 "⬛ **④ THE `designrulings` SUB-CHIP IS RULING-SHAPED AND ITS NUMBER DOES NOT MEAN WHAT IT SAYS** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call. Lane EV graded it **stretched**: the chip's "
 "label reads **341** = 295 `governs`→component/snippet (Constitution family, visible only with "
 "that chip on) + 28 base `governedBy` + 8 asset `ruledBy` + **10 asset `governedBy` nulls that "
 "can never draw**; at page defaults a chip labelled 341 governs **28** drawn edges. Two options, "
 "his: **(a)** accept EX's reading — third provenance = *the rulings a design cites*, an edge "
 "chip, ON by default — and relabel the count to the drawn edges it governs, *citations* not "
 "*rulings*; **(b)** declare the third provenance a set of RULING nodes, remove the sub-chip, "
 "ship DESIGN GOVERNANCE with two provenances and a visible *third: pending scope ruling* slot, "
 "and rule per-ruling scope in its own lane. ⛔ **`s277-D8` FIXED DESIGN GOVERNANCE AT THREE "
 "PROVENANCES, SO LANE SC'S \"inference by declared scope\" CHIP IS A RULING BEFORE IT IS ~25 "
 "LINES OF CODE.** Row: `W-279ev` (open, closes on his word). Receipt: "
 "`notes/_subreports/2026-09-16-279-EV-explorer-verify.md` §2, §9.",

 "⬛ **⑤ A THIRTEENTH VERB FOR THE ASSETS EDGES, AND `verbVia` KEEP-OR-DROP** [NEW — 0, DAVE'S] — "
 "put to Dave at the wrap call; lane VB declared both *\"Dave's to ratify, not this lane's to "
 "pad\"* (`notes/_subreports/2026-09-16-279-VB-verbs.md` §9). **(a)** `usesIcon` **371** and "
 "`usesLogo` **19** have a CONSUMER — the slice's `assets` field and ASK Q12 — and no verb; a "
 "thirteenth (*uses*?) would name them, or they stay unverbed. **(b)** whether `resolvedBy` 7 / "
 "`challengedBy` 4 / `explainedBy` 1 / `touches` 9 / `hasParty` 68 get verbs — one *decided* for "
 "`resolvedBy` alone would split `s238-D6`'s four. **(c)** `verbVia` keep or drop: keeping it is "
 "provenance at **~+1,500 tokens** across 122 rows, dropping it leaves `verb` alone. The twelve "
 "verbs as shipped read **36 of 58 edge types** and walk **2,351 of 3,136 edges = 75%** "
 "(`eb2ff7c`); **785 edges are walked by nothing**, `definedIn` 470 the largest.",

 "⬛ **⑥ THE SPIDER `v1.0.14` CUT IS ARMED, VERSION-GATED AND UN-FIRED** [NEW — 0, DAVE'S] — "
 "`s279-D1` puts the reader and the Constitution inside designer-skills-v2 (v2.1, `df33a24` + "
 "`3710d6b`), and lane PK carried the same reversal into `apollo-spider` **by addition and behind "
 "a version gate** — `READER_SHIPS_FROM = \"v1.0.14\"` / `READER_RULING = \"s279-D1\"` — rather "
 "than firing it. ⚠ **The gate is not timidity: v1.0.13's manifest is RATIFIED (`s268-D3`), its "
 "zip frozen, and two BLOCKING arms pin the generator byte-for-byte, so any emitted change at "
 "v1.0.13 turns both red.** Cutting Spider is **Dave's word under `s219-D4(2)`** and is "
 "`P-269-1`'s tripwire, not a lane's to take. Size of the cut, priced by PK: `--probe` + "
 "`--manifest` at a commit, the key into `RATIFY_IDS` on ratification, `--release`, the ledger "
 "literal, `--seed`.",

 "⬛ **⑦ `va25-013` CANNOT BE NARROWED BY AN OVERRIDE — IT NEEDS A RULE SPLIT, AND THAT IS HIS "
 "CALL** [NEW — 0, DAVE'S] — lane SC2 landed per-rule `ruleFacets` overrides (27 on 5 rows, 0 "
 "refused, 26 strictly narrower) and deliberately left this one alone: **`va25-013` stays at 111 "
 "components BY ITS OWN WORDS** — its text says *\"icons/avatars 1:1 square\"*, so it genuinely "
 "binds icon-bearing components and an override stripping `icons` would contradict the quoted "
 "rule. ⇒ **If it is to be narrowed it is a RULE SPLIT in `knowledge/guidelines/visual-assets.md` "
 "(video/photo vs icon/avatar vs third-party logo), never a facet override.** Size: one guideline "
 "edit plus a regen of `_rules-index.json`. Left at file grain for the same reason: `va25-001/002/"
 "005/006/007/012`, `avd-006` (a BLOCKING alt-text gate that must keep icon-bearing components), "
 "`neuro-026` (an override cannot WIDEN). Receipt: "
 "`notes/_subreports/2026-09-16-279-SC2-scope-fix.md`.",
]

line = "> **residual → #280:** " + " · ".join(NEWITEMS) + " · " + aged[len("> **residual → #279:** "):]
after = len(cg._carry_items(line))

HEADER = (
 "---\n\n## residual → #280\n\n"
 "*Written straight here at the #279 wrap (✅ **NO DATE SPLIT — the session, its ritual and all "
 "of its commits are 2026-09-16**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing "
 "dropped for being old; ★ **ONE carry STRUCK, with its receipt** — the #278 carry that said the "
 "thirteen `s277` rulings were \"LAW and NOT IN THE TREE\" was CORRECTED by the day's own commits, "
 "and a corrected claim is the ONE thing `s183-D1` licenses a wrap to re-word. #279 was an "
 "ENACTMENT session across ten lane commits and three Fable verify seats, so it mints SEVEN new "
 "carries.*\n\n"
 f"<!-- WRITTEN-FIRST: residual → #280 — the aged tail below the SEVEN new items is the #279 line "
 f"put through ONE programmatic pass (`notes/_lanes/279/W/carry280.py`): {n_num + n_new} age "
 f"brackets bumped ({n_new} of them `NEW — 0` → `1`), and EXACTLY ONE surgical edit — a STRIKE "
 f"carrying its `s183-D1`/`s188-D2` receipt, asserted as a count of one in the script rather than "
 f"left implicit. Probe count at write time: {after}. -->\n\n"
 + line + "\n\n")

if "--write" not in sys.argv:
    print(f"DRY: ages bumped {n_num + n_new} ({n_new} NEW→1) · 1 strike · {len(NEWITEMS)} new items · "
          f"carries {before} → {after}")
    sys.exit(0)
MARK = "---\n\n## residual → #279\n"
assert text.count(MARK) == 1
text = text.replace(MARK, HEADER + MARK, 1)
open(CARRIES, "w", encoding="utf-8").write(text)
print(f"WROTE § residual → #280: ages bumped {n_num + n_new} ({n_new} NEW→1) · 1 strike · "
      f"{len(NEWITEMS)} new items · carries {before} → {after}")
