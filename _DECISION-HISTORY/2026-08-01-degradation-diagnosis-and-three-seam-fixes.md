# #73 — The degradation diagnosis, and the three seam fixes it licensed

provenance: local_5be8e1c8 (#73) · 2026-08-01
status: observed

**Spine entry:** `_LIVE-STATE.md` ⏱ #73 delta · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #73

## The question

Dave opened: *"Im concerned about the wrap up, budgeting and pricing, and the good morning
process, it was working well for a few session. i need answers to why its degrading again."*

## How the answer was built (verify before asking, artefacts not banners)

Read `_CHAIN.md` only, then checked its claims against `git log` and the files themselves.
The probe immediately invalidated two things in the chain: the #72 residual said the 2c/2d
rolls were not run, but `e7df94d`'s receipts and `_GM-ARCHIVE.md`'s Batch #72 showed 2c/2f
RAN — only 2d was truly skipped; and the size line's "measured #72: 24.2K→23.5K, banner
SHORT" was authored mid-wrap before the banner landed — the committed artefact measured
26.5K, a net addition whose true figure lived only in a commit message no roll rule reads.

## The four causes (none of them decay)

1. **The opener half of the ritual is ungateable** — pre-flight, title read-back, pace panel
   live in chat where no gate sees them. The wrap gate then goes red honestly, every time,
   and had no legal refusal form for the pre-flight ([[honest-refusal-needs-a-legal-form]]).
2. **The wrap gate has no consumer** — not in `_git_commit.sh`'s path, so red blocks nothing
   (#71 and #72 both committed through it). [[instrument-without-a-consumer]].
3. **Banners authored before the seam they report** — third consecutive instance, this time
   inside the declared-gap mechanism itself (#72's residual and size line).
4. **The wrap is budget-subordinate** — last in the window, first thing cut. #72's budget
   call truncated the rolls, dossier and memory pass; GM grew 23.5K→26.5K.

Plus the recurring tax: tiktoken dies with every fresh sandbox and blocked the first commit
of every session. And part of "it was working well" was invisibility: pre-#59 the gauge
silently estimated, and #70/#71's chain truthfully read FRESH over skipped wraps. The
machinery got MORE honest, which reads as degradation.

## What was enacted, on Dave's word ("lets get the memento stuff fixed")

- **(g)** `8d176a1` — `_git_commit.sh` self-heals tiktoken before the chain check, probing
  `get_encoding` and installing only when degraded; a failed heal defers to the check's own
  diagnosis. Mutation-proven by its own enactment run (uninstalled → healed → real
  measurement). **Mistake, declared:** the fix first landed under a stub message because I
  ran the live script on a tree carrying its own edit — "clean tree" was an unverified
  premise ([[premise-ages-faster-than-rule]], mine this time). Amended same minute, unpushed.
- **(h)** `514f4bd` — `check_preflight` gains the legal refusal `⛔ NOT CAPTURED —
  UNMEASURED.` + reason (exact form, scoped, four mutation-run arms: legal passes as WARN,
  near-miss fails, refusal+numbers fails, reasonless fails). Live effect: #72's 3-fail red
  became 1 precise fail — which exposed a NEW residual: the check grades the FIRST matching
  line, so with no stamp in the LATEST banner it graded #71's wording. Declared, not fixed.
- **(f)** `514f4bd` — `_gen_chain.py` surfaces the forward title ABOVE the banners
  (`YOU ARE #N. TITLE THIS CHAT →`) and refuses a stale title (title #N ≠ ★ LATEST + 1),
  inherited free by `--check` and the commit seam. Catches a STALE title; cannot see a
  skipped wrap — the honest scope #72 itself wrote.

## Deliberately NOT done (Dave's, with the why)

Wiring the wrap gate into `_git_commit.sh` would block mid-session commits — a tradeoff only
he can rule ([[unkeyed-gate-vs-roll2f-tension]]'s lesson: a new gate can make a correct
state unreachable). The trigger index (e) is ~16 lines of read-chain content that need his
eyes. The dormant % path stays a standing fork (#58). The wrap-budget-reservation idea
(reserve the wrap at the opener so budget calls cut the JOB) was floated in chat, unpriced.

## Also this session

The owed 2d roll ran (mover receipts); three #72 claims struck at source (`f70f602`);
`__tmp_moved.html` swept; memory index compacted at its cap (17 settled entries archived);
the banner-before-seam memory gained its #73 clause: **declare LAST, and re-read the
declaration against the artefact before the chain is generated.**
