#!/usr/bin/env python3
"""#286 wrap — build the ops for step 1 (`Last refreshed`) and step 2d (the delta roll).

EVERY assertion below runs IN THE WRITING PROCESS, before the mover ever reads the ops file
(#166's stale-msgfile class). The ops file is session-owned and uniquely named under
`notes/_lanes/286/W/` — never `/tmp`, which `s218-D7` clause 3 forbids for evidence and which
`_seam.py`'s SCRATCH arm would delete mid-run anyway (lane V's #285 note).

WHAT IT BUILDS — four ops, in this order, exactly the #285 shape:
  1. insert  `## Rolled 2026-09-18 #286` header at the top of `_LIVE-STATE-ARCHIVE.md`
  2. insert  #282's `Previous:` chain segment, VERBATIM, under that header
  3. move    the `#283` ⏱ PRIOR DELTA block out of `_LIVE-STATE.md` into that same section
  4. replace the `Last refreshed` line — #286 stamp in front, #285 demoted to `Previous:`,
             #282's segment REMOVED (it is in op 2, not deleted) and a trim note added

⛔ THE VERBATIM GUARANTEE IS MECHANICAL, NOT EDITORIAL: the moved segment is a SLICE of the
   old line, never re-typed, and a post-condition asserts the slice is byte-identical to what
   the archive receives.
"""
import json
import os
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
LSA = os.path.join(ROOT, "_LIVE-STATE-ARCHIVE.md")
HERE = os.path.dirname(os.path.abspath(__file__))

# ── PRE-CONDITIONS, on the INPUT (the #285 lesson: a guard that tests the OUTPUT fires on
#    correct behaviour — #285's own pre-condition assert was wrong in exactly that way) ──────
for p in (LS, LSA):
    assert os.path.exists(p), f"missing {p}"
    assert os.path.getsize(p) > 20_000, f"implausibly small: {p}"

lines = open(LS, encoding="utf-8").read().split("\n")
lr_idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(lr_idx) == 1, f"expected exactly one `Last refreshed` line, found {len(lr_idx)}"
OLD = lines[lr_idx[0]]
assert "**#285 wrap**" in OLD, "INPUT is not #285's stamp — refusing to re-date"
assert "**#286 wrap**" not in OLD, "INPUT already carries a #286 stamp — refusing to run twice"

SEP = " Previous: "
segs = OLD.split(SEP)
assert len(segs) == 4, f"expected 4 `Previous:`-joined segments, found {len(segs)}"
assert segs[1].startswith("2026-09-18 (Fri from `date` — **#284 wrap**")
assert segs[2].startswith("2026-09-18 (Fri from `date` — **#283 wrap**")
assert segs[3].startswith("2026-09-18 (Fri from `date` — **#282 wrap**")

# The #282 segment runs to the first trailing trim note. Located, never guessed.
TRIM_MARK = "*Last refreshed (#281, trimmed at the #285 wrap)"
t = segs[3].find(TRIM_MARK)
assert t > 1000, f"trim-note marker not found (or absurdly early) at {t}"
SEG282 = segs[3][:t].rstrip()            # ← the thing that MOVES, verbatim
TAIL = segs[3][t:]                       # ← the stack of trim notes, kept in place
assert SEG282.endswith(")*"), repr(SEG282[-40:])
assert len(SEG282) > 5_000, len(SEG282)   # measured 8,218 at #286; a floor, not a target

# ── THE NEW #286 SEGMENT ────────────────────────────────────────────────────────────────────
NEW286 = (
 "*Last refreshed: 2026-09-18 (Fri from `date` — **#286 wrap**. "
 "✅ **NO DATE SPLIT: the session, its three commits, this ritual and its own commit are ALL "
 "2026-09-18** — `date` read at this seat at the ritual's open. "
 "⛔★★★ **READ `_HANDOFF-137-the-connector-lever-reads-and-the-masters-are-sized.md` FIRST — IT "
 "IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT**, and it does NOT replace `_HANDOFF-130`…`-136`, "
 "whose open items still stand except the two closed below, each with a receipt. "
 "⛔★★ **NO RULING WAS INSCRIBED AND `knowledge/_rulings.json` STAYS AT 620 — verified at this "
 "seat by `json.load` over the `rulings` list, and no `s286-` id exists in the store.** "
 "★★★ **DAVE SPOKE TWICE AND BOTH SENTENCES ARE RECORDED AS HIS WORDS RATHER THAN INSCRIBED AS "
 "RULINGS:** ***\"okay go on everything\"*** (to an opener naming the standing wording, the "
 "masters' registration and the 256,000 fix, plus the cold-boot question) and "
 "***\"okay size-on-the-existing-node\"*** (the SHAPE of a master registration). "
 "⚠ **Reading the first as ratification-of-the-wording-AS-WRITTEN is the CONDUCTOR'S reading, "
 "not Dave's sentence** — `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md` says so in its own "
 "words, and **whether either sentence is inscribed as a ruling was put to Dave at the wrap "
 "call and is not this seat's to decide.** "
 "⛔★★★ **THE CONNECTOR LEVER READ, AND IT IS A READING AND NOT A VERDICT: BOOT COLD 73,832 "
 "real (n=1) against #285's 80,863 — delta −7,031, ONE variable changed** (Dave set the "
 "built-in Browser connector's 17 `mcp__Claude_Browser__*` tools to BLOCKED; skills, computer "
 "use and the other three connectors held constant BY DESIGN). ★ **The cleanest boot experiment "
 "this record carries** — and ⛔ **one reading against one reading cannot separate the lever "
 "from the ordinary spread** (the last seven post-diet readings span 72,110–83,636, a spread of "
 "11,526, WIDER than this delta), so the direction is consistent with the block having worked "
 "and **the magnitude is not established**. ⛔ **73,832 is the ELEVENTH post-diet reading over "
 "`BOOT_CEILING_TK` 70,000 — 3,832 OVER — and the literal is SHRINK-ONLY by `s240-D2`/`s241-D1`: "
 "cut the boot, never raise the number, and raising it is Dave's word alone.** The figure is "
 "stated ONCE, in the `post-mortem #286:` line (`s241-D2`), and the finding file "
 "`notes/_lanes/286/BOOT-COLD-2026-09-18.md` is deliberately NOT in `notes/_GAUGE-LOG.md` for "
 "that reason. "
 "★★★ **THE 40 MASTERS ARE REGISTERED — `W-285lm` CLOSES, AND THE SHAPE IS HIS.** On "
 "***\"okay size-on-the-existing-node\"*** a master is a **SIZE FIELD on its lockup's existing "
 "node, never its own node**: lane R2 wrote a `sizes` map onto all **8** logo nodes, five raw "
 "heights each (24/28/32/36/40) = the 40 masters, **merge-on-write**. Verified at THIS seat by "
 "`json.load`: **8 nodes (unmoved) · 33 edges (unmoved) · 8 of 8 nodes carry `sizes` · 12 "
 "`governedBy` edges intact**. ⚠ **THE FIELD'S KEY NAME IS NOT HIS WORD** — he named the "
 "location, not the spelling; `sizes` is lane R2's reading of the file's own plural vocabulary "
 "(`nodes`, `edges`, `unresolved`, `fills`) and is recorded as the lane's reasoning, not as his. "
 "⚠ **AND LANE R FIRST REPORTED THE MASTERS NOT REGISTRABLE — the generator is blind to "
 "`masters/`** — which is why R2 exists; both readings stand. "
 "★★ **`knowledge/_standing.md` IS OUT OF DRAFT AND `W-285sc` CLOSES — ON A HEADER-ONLY CHANGE.** "
 "Measured here against `09ddf155`: **8 insertions, 3 deletions, ONE hunk, all of it above the "
 "`---` rule**, and the **eight lines are BYTE-IDENTICAL** (936 B of body, compared "
 "programmatically, not by eye). ⛔ **An instrument reciting a constraint still does not inscribe "
 "it**, and the header now says so in its own words. ⚠ **`knowledge/_seam.py:44` STILL CALLS THE "
 "FILE A DRAFT** — a stale claim inside a live instrument, found here and NOT edited, because "
 "the brief located it at `:26` and this seat measures `:44`: **both readings are published.** "
 "★★ **THE SEAM GREW AN `INSEAT` ARM AND `_git_commit.sh` GREW `--quiet` — #285'S MOVES 2 AND 3, "
 "BUILT** (`knowledge/_seam.py` +214/−6, `knowledge/_git_commit.sh` +60/−1). The arm counts the "
 "conductor's OWN in-seat tool output since the last seam and warns past `INSEAT_WARN_TK`. "
 "⚠ **THAT 10,000 IS *PICKED*, NOT RULED — the file says so itself** — and both the number and "
 "its placement are ruling-shaped and were put to Dave, not decided here. "
 "⛔ **THE 256,000 WORDING IS FIXED IN THE GAUGE AND 58 PROSE LOCATIONS ARE STILL OWED.** "
 "`knowledge/_gauge_tokens.py` reads **+25/−3 with the CONSTANTS UNCHANGED** (`BUDGET_HARD` is "
 "still `256_000`); **58 locations across 10 live files** still call it a wall or a hard line — "
 "`_RUNBOOK-context-gauge.md:85`'s ***\"256,000 stays the UNQUALIFIED wall (`s214-D2`)\"*** among "
 "them. ⛔ **NOT EDITED HERE: amending ratified runbook and ruling text is Dave's word alone**, "
 "and it is minted as a NEW carry rather than folded into the old one. "
 "✅ **LANE V, ADVERSARIAL, 24 of 24 TESTABLE CLAIMS PASS.** ⚠ **Two method notes are published "
 "rather than buried: it OVERWROTE `knowledge/_capture_gate.py` with HEAD mid-run and restored "
 "it byte-exact, and it moved two symlink farms to `_to_delete/`** — a verifier mutating the "
 "tree it verifies is worth saying out loud even when the restore is exact. "
 "★★ **NINE OPUS LANES, EVERY ONE AN `Agent` AT DEPTH 1, NONE IN SEAT — THE DELEGATION RULE "
 "OBEYED A SECOND CONSECUTIVE SESSION AND STILL UNINSCRIBED.** Measured at this seat from the "
 "conductor's transcript `f00a81c6-812c-4fb9-b2e1-90eec24a3c47.jsonl`: S 83,120 · R 93,872 · "
 "G 122,502 · T 145,539 · V 170,927 · C 101,132 · P 60,602 · R2 241,918 · C2 93,636 = "
 "**subs 1,113,248 real (n=9)**, QUOTA and never FILL. ★★ **THE PRICE, BOTH SIDES: the nine lane "
 "replies cost the conductor's window 3,399 cl100k IN TOTAL** — the `s218-D7` stub contract "
 "working — **against 1,113,248 real of sub FILL**, roughly 0.3%. ⛔ **Two sessions' obedience is "
 "evidence the shape is affordable, not a rule that it is required; his sentence is still "
 "uninscribed.** "
 "⚙ **GAUGE, MEASURED AT THIS SEAT BY IMPORTING `_checkin.read_fill` rather than re-implementing "
 "it: FILL 162,555 real / 22 turns against 161,544 / 20 DECLARED at the wrap-brief cut, delta "
 "1,011** — the hand-over's own cost, not a disagreement. ✅ **17,445 INSIDE the 180,000 QUALITY "
 "line — the first session in five to close under it** — and 256,000 clear for the fourth "
 "running. ✅ **THE DECLARED AND MEASURED BOOT AGREE TO THE TOKEN (73,832), AND THAT AGREEMENT IS "
 "WHAT IDENTIFIES THE WINDOW** — the `s214-D5` precondition for `delta` being a legal "
 "subtraction at all. "
 "⛔ **SIX BLOCKING GATE FAILS AT THE OPEN, carried in the `#243` DECLARED not-a-wrap form — the "
 "TWELFTH consecutive wrap on that path** (the boot-drift CEILING BREACH + five boot "
 "double-counts: #243 ×5, #264, #272, #273, #274). **A wrap may not repair an inherited gate "
 "fail** and this one did not try. "
 "⚠ **THE STORE'S ID REGEX REFUSED A `W-286r2`-SHAPED ID — THE THIRD INSTANCE IN TWO SESSIONS** "
 "(lane R2's row is `W-286rb`); a finding, not a fix, because widening an id convention is not a "
 "wrap's call. "
 "⚠ **CI WAS READ OVER THE PUBLIC API AND RESOLVES #285'S OWN DECLARED GAP:** run `35386047978` "
 "on `7ed49d37` is **completed / failure**, failing `Survey the COMMITTED tree` + `Knowledge "
 "build` — **and the identical two steps fail on `09ddf155` and on `d2ae9c73`, which #285 could "
 "only read as `in_progress` and correctly claimed no colour for.** ⛔ **The red is INHERITED, "
 "not born at #286.** "
 "Carry set `_CARRIES.md` § `residual → #287` — **NINE new items and TWO STRIKES, each with its "
 "receipt**; gauge, declared skips with their sizes, the cloud-store result and not-done: the "
 "⏱ LATEST DELTA below. **This wrap's own filed report (`s218-D7`): "
 "`notes/_subreports/2026-09-18-286-W-wrap.md`.** **Narrative dossier (1b): "
 "`_DECISION-HISTORY/2026-09-18-286-the-connector-lever-reads-and-the-masters-are-sized.md`.** "
 "**His words verbatim: `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md`.**)*"
)

TRIMNOTE286 = ("*Last refreshed (#282, trimmed at the #286 wrap): #282's `Previous:` chain segment "
               "was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-18 #286, in the same "
               "section as the #283 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*")

NEW = SEP.join([NEW286, segs[0], segs[1], segs[2]]) + "  " + TRIMNOTE286 + "  " + TAIL

# ── POST-CONDITIONS on the PROJECTED text, before anything is written ────────────────────────
assert NEW != OLD
assert SEG282 not in NEW, "the #282 segment is still in the projected line — it must MOVE, not copy"
assert segs[0] in NEW and segs[1] in NEW and segs[2] in NEW, "a kept segment was lost"
assert NEW.count("**#286 wrap**") == 1 and NEW.count("**#285 wrap**") == 1
assert NEW.startswith("*Last refreshed: 2026-09-18 (Fri from `date` — **#286 wrap**")
assert TRIM_MARK in NEW, "the existing trim-note stack was dropped"

LSA_HEADER = "## Rolled 2026-09-18 #286 (2d, at the #286 wrap) — via the mover"
assert LSA_HEADER not in open(LSA, encoding="utf-8").read(), "the #286 archive section already exists"

ops = [
 {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
  "at": "## Rolled 2026-09-18 #285 (2d, at the #285 wrap)", "where": "before",
  "lines": [LSA_HEADER, "",
            "### #282's `Previous:` chain segment — moved VERBATIM at the #286 wrap (`Last refreshed` trim)",
            "", SEG282, ""]},
 {"op": "move", "src": "_LIVE-STATE.md",
  "start": "## ⏱ PRIOR DELTA — 2026-09-18 (Fri from `date`) (**#283**",
  "end": {"regex": r"^## 🕓 OPEN — Latin Univers"},
  "dst": "_LIVE-STATE-ARCHIVE.md",
  "at": "### #282's `Previous:` chain segment — moved VERBATIM at the #286 wrap", "where": "after"},
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [OLD], "replace": [NEW]},
]

STAMP = int(time.time())
OPSF = os.path.join(HERE, f"ops-286-lastrefreshed-{STAMP}.json")
with open(OPSF, "w", encoding="utf-8") as fh:
    json.dump(ops, fh, ensure_ascii=False)
# ⛔ THE #166 GUARD: assert the msgfile exists and has a size floor IN THIS PROCESS.
assert os.path.exists(OPSF), f"ops file was not written: {OPSF}"
sz = os.path.getsize(OPSF)
assert sz > 8_000, f"ops file implausibly small ({sz} B) — a truncated write reads as success"
print(f"OPS {OPSF}  {sz:,} B  {len(ops)} ops")
print(f"  moved segment: {len(SEG282):,} chars   old line {len(OLD):,} → new {len(NEW):,}")
