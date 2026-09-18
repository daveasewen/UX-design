# #285 · LANE SC — THE SEAM RE-QUOTES THE STANDING CONSTRAINTS

provenance: 285 · 2026-09-18 · lane SC (BUILD) · conductor Fable 5.1
status: filed · nothing committed by this lane

**Dave, #285 opener:** *"yes to the seam re-quoting the standing constraints"*. The finding behind it:
everything read at a session's opener (~80K of handoff, chain and check-in) becomes the MIDDLE of the
context the moment work starts, and the standing rules in it drift out of attention
(lost-in-the-middle / U-shaped attention). `_seam.py` already runs before and after every lane and
re-quotes the FILL line; it now re-quotes the standing constraints too, at the TAIL — the recency end.

⚠ **`knowledge/_standing.md` IS A DRAFT.** Its header says so verbatim: *"DRAFT — Dave's approval
pending; nothing here is inscribed by this file."* Eight lines were drafted FROM THE RECORD
(`_HANDOFF-135-the-logo-masters-land-and-the-disk-lever-is-found.md`,
`notes/_lanes/284/DAVE-RULINGS-2026-09-18.md`), each with its receipt in parentheses. **The seam
re-quotes; it never inscribes.** `knowledge/_rulings.json` is untouched and stays at 620.

## TOUCHED PATHS — exact, and all of them

- `knowledge/_standing.md` — **NEW** (untracked). 8 constraint lines + a DRAFT header.
- `knowledge/_seam.py` — **MODIFIED**.
- `notes/_subreports/2026-09-18-285-SC-seam-standing.md` — **NEW**, this file.

⛔ Nothing else. No commit, no push; no generator run (`gen_kg_icons.py`, `gen_kg_rules.py`,
`land_rests_on.py`, `_build_all.py` were all untouched); `_gauge_tokens.py` untouched.

## THE DIFF — `knowledge/_seam.py`

1. **Docstring.** *"Three lines"* → *"Four blocks"* in the opening line and in WHAT IT PRINTS, which
   now names the STANDING block and its tally line. A new paragraph, **THE FOURTH BLOCK — WHY IT IS
   LAST**, carries Dave's words, the lost-in-the-middle reason, and the instruction that the block
   must NOT be moved above SCRATCH. Usage gains `--no-standing`.
2. **Constants.** `STANDING_PATH` (= `knowledge/_standing.md`) and `STANDING_TK_CEILING = 300` — a
   PICKED figure, the ceiling the selftest holds the block under so the tail stays a tail.
3. **`standing_lines(path)`** — the parse, deliberately dumb: drop everything up to and including the
   first `---` rule, then every non-empty, non-`#` line is a constraint, printed VERBATIM.
4. **`standing_tokens(lines)`** — cl100k via tiktoken, on the joined printed block. Unavailable →
   `?`, never a guessed number (the selftest FAILS on `?` rather than passing a blind arm).
5. **`standing_block(path)`** — `STANDING`, the lines, then `STANDING <n> lines · <tokens> cl100k`.
   **ADVISORY, like every other line here:** a missing file returns
   `STANDING — knowledge/_standing.md ABSENT`, an unreadable one names the exception, an empty one
   says `EMPTY` — and `main()` still returns 0 in every case. Paths outside the repo print as given,
   never as a `../../..` climb.
6. **`main()`** — `--no-standing` added; the block prints LAST, after SCRATCH, when not suppressed.
7. **`selftest()`** — a third non-verdict arm: the block prints and starts with `STANDING`, the tally
   line agrees with the line count, tiktoken was actually available, and the count is ≤ 300. Arm
   total 6 → 7.

## MEASURED — the cost of the block

- **246 cl100k tokens · 8 lines** (tiktoken `cl100k_base`, on the eight lines joined by newlines).
- Against the ≤ 250 target in the brief and the 300 ceiling the selftest enforces: **inside both.**
- It is paid TWICE PER LANE (the seam runs before the cut and after the land) — ~492 cl100k a lane,
  against a 180,000 quality line. The FILL line it sits beside costs about a tenth of that.

## OUTPUT 1 — `python3 knowledge/_seam.py --selftest`

```
seam selftest: 7 arms, all GREEN
```

(rc 0.)

## OUTPUT 2 — `python3 knowledge/_seam.py --no-clean`

```
FILL  158,586 real / 11 turns · boot 80,863 · ✅ 21,414 real under the 180,000 stop line
DISK  /sessions 0.3% · 9,653,508 KB free · ✅
SCRATCH 2 own entries · 2 removable (--no-clean)
STANDING
Everything is delegated: the conductor orchestrates and judges; lane work done in-seat is a lapse (#57 / s204-D1, restated #284).
The four generators that undo hand-authored state — gen_kg_rules.py, land_rests_on.py, gen_kg_icons.py, _build_all.py single-process — never run without Dave's word (H-135 open 11).
Commits only through knowledge/_git_commit.sh, as a lane by default; push is the conductor's call with a CI read-back (H-135 move 3).
180,000 FILL is the QUALITY line and stands; 256,000 is not a wall for this model in Cowork (Dave's correction, #284).
Strike nothing from a carry without a receipt (s183-D1 / s188-D2).
Dave rules from plain prose and visuals, never ID codes; render readings side by side for a visual ruling (#66-D5, s172-D1).
Every sub files its full report at notes/_subreports/ (s218-D7).
A ruling is Dave's word inscribed; a proposal, a lane's finding or his enthusiasm is not one (s271-D4).
STANDING 8 lines · 246 cl100k
```

(rc 0. The FILL reading is this LANE's own window, not the conductor's.)

## THE RECEIPTS BEHIND THE EIGHT DRAFT LINES

| line | receipt, and where this lane read it |
|---|---|
| everything is delegated | `#57` / `s204-D1`, restated #284 in Dave's own words (`DAVE-RULINGS-2026-09-18.md`, delegation bullet); `_HANDOFF-135` § THE DELEGATION LAPSE |
| the four generators | `_HANDOFF-135` § OPEN item 11 — *"A standing-orders line naming the CLASS is his"* |
| commits via `_git_commit.sh`, as a lane | `_HANDOFF-135` § FIRST MOVES item 3; the six-run commit measured in § THE COMMIT TOOK SIX RUNS |
| 180,000 quality line; 256,000 not a wall | Dave's same-turn correction, `DAVE-RULINGS-2026-09-18.md` § FINDING; `_HANDOFF-135` § THE WINDOW FINDING |
| no strike without a receipt | `s183-D1` / `s188-D2`, cited at `_HANDOFF-135` § THE DISK LEVER |
| plain prose and visuals, never ID codes | the two-register rule `#66-D5` (`_RUNBOOK-review-doc.md`); the plain-prose read-back at `s172-D1`; visual rulings ruled by eye off a review page (`s176-D2`, `s262-D2`) |
| subs file at `notes/_subreports/` | `s218-D7` (`_gate_doc_rows.py:60`, `_capture_gate.py:5599`) |
| a ruling is Dave's word inscribed | `s271-D4`, the form `_HANDOFF-135` § OPEN is written in |

⬛ **OWED TO DAVE, AND THE POINT OF THE DRAFT HEADER:** eight lines, each ruling-shaped, none of them
inscribed by this lane. What he approves can be inscribed later by the conductor; what he strikes or
rewords is edited in `_standing.md` and re-measured. **The mechanism is his to ratify separately from
the wording.**
