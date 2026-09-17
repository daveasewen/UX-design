#!/usr/bin/env python3
"""#280 wrap — build `_CARRIES.md` § `## residual → #281` from § `## residual → #280`.

ONE programmatic pass, the #261…#279 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ TWO SURGICAL EDITS, each carrying its `s183-D1`/`s188-D2` receipt:
      · #279's ① ("THE GRAPH IS NOT THREE LAYERS: THE LAYOUT LANE IS #280'S FIRST MOVE") — the
        question was PUT and ANSWERED this session, `s280-D1`;
      · #279's ② ("HIS 15-BASE EXPORT IS RECEIVED AND UNREAD BY THE RECORD") — it is read and
        fourteen of fifteen are inscribed.
      Each is STRUCK with the correction named, never re-typed, and what SURVIVES each strike is
      carried as a NEW item rather than left inside a struck one.
  (c) the session's SIX new items written in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
⚠ NOT re-minted: the `#243` not-a-wrap form (already in this set, and this wrap is its SIXTH
  running — the age bracket is what carries that, not a second copy).
"""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #280:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the TWO surgical edits ------------------------------------------------------------
OLD1 = "⬛ **① THE GRAPH IS NOT THREE LAYERS: THE LAYOUT LANE IS #280'S FIRST MOVE** [1, DAVE'S]"
NEW1 = ("~~⬛ **① THE GRAPH IS NOT THREE LAYERS: THE LAYOUT LANE IS #280'S FIRST MOVE** [1, DAVE'S]~~ "
        "⛔ **STRUCK AT THE #280 WRAP — THE QUESTION WAS PUT AND HE ANSWERED IT; THE STRIKE CARRIES "
        "ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt).** The claim below — that the layout "
        "question has never been put to him and that #280's first move is a lane rendering ONE "
        "option — was TRUE when written at the #279 wrap and is SPENT now: lane LY rendered exactly "
        "that one option (`b212ca2`, explorer 1.17 strata, default pixel-identical by canvas md5), "
        "lane LS drew FOUR sketches on one page (`a7ecd8f`), and **his export at 20:30Z chose all "
        "four PLUS the original, in 2D and 3D, force the default** — inscribed as **`s280-D1`** "
        "(`53a91bd`) and built as explorer 1.18's six cells (`b5df9c9` · `eddf87a` · `c3805ec`). "
        "Correction inscribed at: `knowledge/_rulings.json` § `s280-D1` · "
        "`notes/_lanes/280/layout-sketches/DAVE-EXPORT-sketches-2026-09-16.json` · "
        "`notes/_lanes/280/DAVE-RULINGS-2026-09-17.md` item 3 · "
        "`_HANDOFF-131-the-matrix-and-the-front-door.md`. ⚠ **ONE THING SURVIVES THE STRIKE AND IS "
        "CARRIED AS A NEW ITEM RATHER THAN LEFT INSIDE A STRUCK ONE: the EYE-CHECK of the six cells "
        "is asked and UNANSWERED — item ② below.**")
assert aged.count(OLD1) == 1, ("strike anchor 1", aged.count(OLD1))
aged = aged.replace(OLD1, NEW1, 1)

OLD2 = ("⬛ **② HIS 15-BASE EXPORT IS RECEIVED AND UNREAD BY THE RECORD — THE INSCRIBE LANE IS "
        "#280'S** [1, DAVE'S]")
NEW2 = ("~~⬛ **② HIS 15-BASE EXPORT IS RECEIVED AND UNREAD BY THE RECORD — THE INSCRIBE LANE IS "
        "#280'S** [1, DAVE'S]~~ ⛔ **STRUCK AT THE #280 WRAP — THE RECORD HAS READ IT AND THE STRIKE "
        "CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt).** The claim below — that the "
        "15-base export is UNREAD by the record — was TRUE when written at the #279 wrap and is "
        "FALSE now: lane IN read it WHOLE and inscribed **nine** twins while asking **six** rows "
        "back on a page rather than guessing (`c4d0d22`), and lane IN2 read his ASK export and "
        "inscribed **five** more (`850acbf`) ⇒ **fourteen of the fifteen are settled**, the "
        "exporter-defect list is born at `knowledge/_ICON-GAPS.md`, and `gen_kg_icons.py` now "
        "REBUILDS the fourteen from his own exports and REFUSES on disagreement (22/22, mutants "
        "32/32). Correction inscribed at: `notes/_subreports/2026-09-16-280-IN-inscribe-active.md` · "
        "`notes/_subreports/2026-09-16-280-IN2-inscribe-ask.md` · `c4d0d22` · `850acbf`. ⚠ **ONE "
        "THING SURVIVES THE STRIKE AND IS CARRIED AS A NEW ITEM: `jade-lifestyle` is OPEN BY HIS "
        "OWN WORD (`choice: \"open\"`, `twin: null`) with his lean recorded ON THE NULL — item ③ "
        "below.**")
assert aged.count(OLD2) == 1, ("strike anchor 2", aged.count(OLD2))
aged = aged.replace(OLD2, NEW2, 1)

# ---- (c) the session's SIX new items --------------------------------------------------------
NEWITEMS = [
 "⬛ **① THE ORPHAN CENSUS EXPORT IS HIS, TEN RADIOS, AND IT HAS NOT ARRIVED — #281'S FIRST MOVE** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call and NOT answered. On the pink UX cloud in "
 "explorer 1.18 he asked *\"do we have a plan to wire up the orphans etc?\"*, and his word on the "
 "census itself was *\"cool\"*. Lane OC answered the counting half and refused the deciding half: "
 "**157 of the 4,618 nodes on the stage have no line any chip can draw**, four causes, **ten sets**, "
 "each set a radio on `notes/_lanes/280/orphan-census/ORPHANS-2026-09-17.html`. ⚠ **The largest set "
 "is a switch that was left off, not a gap in the vocabulary:** 100 of the 145 UX principles are "
 "dark, 99 with no edge of any kind in storage, and the principle generator can ALREADY emit the two "
 "kinds that would light every one of them — a principle's research family and the sources it was "
 "graded on, both behind flags since `s275-D2`. ⛔ **Turning the first on puts a FAMILY NODE on the "
 "stage, which is a new kind of thing and therefore HIS word, not a lane's.** The second-largest set "
 "is not an orphan set at all — 94 base `rule:` dots that light the moment the HSBC `rule:` chip goes "
 "on. ⇒ **the census becomes the orphan PLAN on his export, and not before.** Receipt: "
 "`notes/_subreports/2026-09-17-280-OC-orphan-census.md` · `82359a5` · row `W-280oc`.",

 "⬛ **② THE EYE-CHECK OF THE SIX MATRIX CELLS IS ASKED AND UNANSWERED** [NEW — 0, DAVE'S] — put to "
 "Dave at the wrap call. `s280-D1` gave him what he asked for — **force · strata · shells × 2D · 3D, "
 "six cells, force the default** — and the contact sheet `notes/_lanes/280/layout-matrix/"
 "MATRIX-2026-09-16.html` puts all six in front of his eye at once. ⚠ **The matrix is what his own "
 "sentence asked for and it is NOT the same thing as six cells being worth keeping:** the conductor "
 "expects **Floors (strata-3D) or Orbits (shells-2D) to go**, and that is an expectation, not a "
 "finding. ⛔ **NOT RULED, and a lane may not thin the matrix on its own — the six cells are ruled "
 "law until he looks.** Receipts: `notes/_subreports/2026-09-16-280-LM-layout-matrix.md` · "
 "`notes/_subreports/2026-09-16-280-LS-layout-sketches.md` · row `W-280lm` (owner dave, closes on his "
 "word on the contact sheet).",

 "⬛ **③ `jade-lifestyle` IS OPEN BY HIS OWN WORD, AND HIS LEAN IS RECORDED ON THE NULL** "
 "[NEW — 0, DAVE'S] — of the fifteen multi-active icon bases, fourteen are settled and this one is "
 "not. His ASK export answers it `choice: \"open\"`, `twin: null`, with the note *\"jade-lifestyle-"
 "active-2 - think is the most likely the correct icon\"*. ⛔ **Lane IN2 wrote NOTHING into the "
 "library for it** — no default, no entry on the mislabelled list — and put his sentence on the empty "
 "slot instead, so the record carries his lean **without anyone turning a lean into a decision**. ⚠ "
 "That is the `s277-D6` standing instruction (*where flag and note disagree the NOTE is his sentence "
 "— ask, do not guess*) applied to a row where he himself declined to decide. Receipts: "
 "`notes/_lanes/280/inscribe-active/DAVE-EXPORT-ask-2026-09-16.json` · "
 "`notes/_subreports/2026-09-16-280-IN2-inscribe-ask.md` · `850acbf`.",

 "⬛ **④ TWO THINGS WERE DECLARED OUT BY THEIR OWN LANES AND NEITHER IS RULED OUT** [NEW — 0] — "
 "**(a)** the **shells-3D cutaway**: lane LS drew it as one of the four sketches (the front half of "
 "the outer two shells removed, 1,157 nodes left drawn) and lane LM declared it OUT of explorer 1.18 "
 "along with equal plate/ring sizes per layer — a build decision taken inside a lane, not a ruling, "
 "and the sketch is the evidence that he has already seen the thing being deferred. **(b)** **snippet "
 "scripts are STRIPPED in the sandbox** that renders a component inside the INSPECT modal (lane EX4), "
 "so a component whose behaviour lives in script renders as its markup and nothing says on the page "
 "which ones those are. ⚠ **Both are declared in their reports rather than discovered at the next "
 "wrap, which is the whole point of writing them down**; neither is a defect and neither is his call "
 "until it is put to him as one. Receipts: `notes/_subreports/2026-09-16-280-LM-layout-matrix.md` · "
 "`notes/_subreports/2026-09-17-280-EX4-explorer-artefacts.md`.",

 "⬛ **⑤ THE WRAP-SUB MEMORY SEAT LIMIT IS MEASURED FALSE TWICE AND THE RUNBOOK STILL SAYS IT IS "
 "STRUCTURAL** [NEW — 0, DAVE'S] — `knowledge/_RUNBOOK-capture-ritual.md` step 3 inscribes that a "
 "delegated wrap sub *\"cannot reach the store at all\"*. **#279's wrap sub wrote the claude.ai "
 "Project store from its own seat, and #280's did too** — file **7,607 B**, index line inserted "
 "newest-first, `index.md` now **6,882 B of the 49,152 B cap**, both calls returning a version token "
 "and neither refused. ⛔ **The runbook line is NOT edited by either wrap — amending a ratified step "
 "is Dave's word** — and both wraps wrote `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md` FIRST, in obedience "
 "to the rule, before testing it. ⚠ **What #278 observed is not re-judged:** it may have been another "
 "seat's capability, a transient, or a claim that was never probed. **RULING-SHAPED: is the limit "
 "real, and if it is not, does the hook file remain as the belt-and-braces receipt or retire?** "
 "Receipts: `notes/_lanes/279/WRAP-MEMORY-HOOK.md` · `notes/_lanes/280/WRAP-MEMORY-HOOK.md` · "
 "`5cc3ecd`.",

 "⬛ **⑥ THREE #278/#279 ITEMS HAVE NO LINE OF THEIR OWN IN THIS SET AND ARE MINTED HERE RATHER THAN "
 "LEFT IN A BANNER** [NEW — 0, DAVE'S] — each was carried in a wrap REPORT and never in `_CARRIES.md`, "
 "which is the home `s225-D2` gives a carry; minting them here is the repair, and they are written as "
 "the questions they are. **(a)** the **`s129-D1` boot-floor LABEL** — the constant 70,794 is right, "
 "its label still describes a `MEMORY.md` that does not exist in the repo and never did. **(b)** the "
 "**two-probe-shape §A question** — #269/#270/#271 stamped `sha256 b9aef5f5…` over 169 lines and "
 "#272…#280 stamp `4311cce4…` over 198; **two probe shapes, not a change in §A**, and which shape the "
 "`size:` stamp should quote is his. **(c)** **what `s214-D6` means when `_CHAIN.md` comes in BELOW "
 "its ~10–12K band** — the clause commands SHORTER and never decide-what-to-drop, so a chain below "
 "band is either a success or an under-record and the clause does not say which. ⚠ **NOT re-minted "
 "here: the `#243` not-a-wrap form, which already stands in this set and is at its SIXTH consecutive "
 "wrap — the age bracket carries that, a second copy would not.**",
]

line = "> **residual → #281:** " + " · ".join(NEWITEMS) + " · " + aged[len("> **residual → #280:** "):]
after = len(cg._carry_items(line))

HEADER = (
 "---\n\n## residual → #281\n\n"
 "*Written at the #280 wrap under `s225-D2` clause (i). ⚠ **DATE SPLIT — the session opened "
 "2026-09-16 and its ritual and wrap commit are 2026-09-17**, the #241 shape by ADDITION; nothing was "
 "re-dated, and the eight lane commits of 09-16 keep their own date. Ages +1, wording unchanged, "
 "nothing dropped for being old; ★ **TWO carries STRUCK, each with its receipt** — #279's ① (the "
 "layout question, ANSWERED by his export and `s280-D1`) and #279's ② (the 15-base export, now READ "
 "and fourteen-fifteenths inscribed). A corrected claim is the ONE thing `s183-D1` licenses a wrap to "
 "re-word, and what survives each strike is carried as a NEW item rather than left inside a struck "
 "one. #280 mints SIX new carries.*\n\n"
 f"<!-- WRITTEN-FIRST: residual → #281 — the aged tail below the SIX new items is the #280 line put "
 f"through ONE programmatic pass (`notes/_lanes/280/W/carry281.py`): {n_num + n_new} age brackets "
 f"bumped ({n_new} of them `NEW — 0` → `1`), and EXACTLY TWO surgical edits — both STRIKES carrying "
 f"their `s183-D1`/`s188-D2` receipts, each asserted as a count of one in the script rather than left "
 f"implicit. Probe count at write time: {after}. -->\n\n"
 + line + "\n\n")

if "--write" not in sys.argv:
    print(f"DRY: ages bumped {n_num + n_new} ({n_new} NEW→1) · 2 strikes · {len(NEWITEMS)} new items · "
          f"carries {before} → {after}")
    sys.exit(0)
MARK = "---\n\n## residual → #280\n"
assert text.count(MARK) == 1
text = text.replace(MARK, HEADER + MARK, 1)
open(CARRIES, "w", encoding="utf-8").write(text)
print(f"WROTE § residual → #281: ages bumped {n_num + n_new} ({n_new} NEW→1) · 2 strikes · "
      f"{len(NEWITEMS)} new items · carries {before} → {after}")
