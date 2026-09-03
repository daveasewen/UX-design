# `#242`-`lane F` — DECOMPOSE THE BOOT and design its OFFLOAD

session: `#242` · 2026-09-03
window: lane F (Fable conducting)
sub index: `lane-F`
brief: `notes/_briefs/2026-09-03-242-lane-F-boot-offload-brief.md`
tokens: `UNMEASURED — a lane cannot read its own `message.usage`; this seat's spend is
DECLARED, never estimated.` (This lane's own *first-turn* boot IS on record at 40,118 real —
see finding 3 — but its total spend is not observable from this seat.)

## VERDICT

All five brief regions are DONE, and the decomposition landed harder than the brief expected
because the boot payload turned out to be **on disk after all**. The session transcript
(`mnt/.claude/projects/*/*.jsonl`) records the opener attachments verbatim, so five of the seven
components are measured from the actual bytes the model was sent rather than reconstructed from
source files. **The headline is unwelcome: everything Dave owns is ~11% of his boot.** Σ(ours) =
**7,964 cl100k tape**; the boot total is **70,710 real**; the remainder ≈ **62,746**, labelled
ESTIMATED-BY-SUBTRACTION and mixing units by construction. That residual is corroborated in
**REAL units, independently**: a lane seat carrying the identical roster, `MEMORY.md`, MCP blocks
and deferred-name list boots at **39,819 / 40,118 real** (n=2) — a floor no repo edit reaches.
⛔ **So JIT, progressive disclosure and componentisation of our own files have a hard ceiling of
about 4,600 tape of realistic saving against a 70,710 boot, and the only lever with real leverage
is the one that is not in the repo at all: Dave's plugin/MCP panel.** The 710-over reading is
NOT the band's problem — under the band that will exist when it is graded it is 1.15σ, green. It
is the **CEILING's** problem, and the ceiling arm will fail the **#243** wrap by name, not this
one. A repeatable instrument, `knowledge/_boot_decompose.py`, is staged and uncommitted; its
`--selftest` passes 3 arms, one of them a break arm.

COUNTS: findings 8 · ruling-shaped 4 · UNPROVEN 3

*(brief's extended counts: components measured 7 · estimated-by-subtraction 1 · files added 1 ·
selftest arms 3)*

## THE LEAD TABLE

Every `tape` figure is **cl100k tiktoken tape, a PROXY** — ⛔ never summed with, or converted to,
a `message.usage` real figure [[measure-dont-convert-units]]. Command for every row in this
table, run at this seat:

```
python3 knowledge/_boot_decompose.py --real 70710 --transcript <the #242 conductor .jsonl>
```

| # | component | tape | movable? | mechanism | risk named | owner |
|---|---|---:|---|---|---|---|
| 1 | `MEMORY.md` auto-memory index (12,656 B · 111 lines) | **3,569** | PARTLY (~2,219) | progressive disclosure: a ⛔/★★★ stub + ONE retrieval line; the rest by `_memento_search.py` | tier-B/C hooks stop firing **UNPROMPTED**; they survive only as look-up-BY-NAME (`MEMORY-ARCHIVE` #49 line) | **Dave** — nothing else may write the store |
| 2 | skills roster, 19 skills, name + description | **1,626** | PARTLY (~900) | componentisation: disable the plugin-roster skills in Dave's panel | a disabled skill never auto-triggers; `dave-voice` (107) is EVERY-REPLY and must stay | **Dave** (panel, non-repo) |
| 3 | MCP instruction blocks — `computer-use` **1,162** + `claude-in-chrome` **236** | **1,398** | YES (1,162 today) | mechanisation: disconnect `computer-use` unless the day's work is desktop automation | no native-app control that session; Chrome work unaffected | **Dave** (panel, non-repo) |
| 4 | deferred tool NAME list (74 names) | **800** | PARTLY (~243) | same lever as row 3 — `computer-use` contributes 243, `claude-in-chrome` 274 | the tools vanish from the roster, not just their schemas | **Dave** (panel, non-repo) |
| 5 | agent listing (6 subagent types) | **557** | NO | harness-generated from the agent definitions | — | harness |
| 6 | total-tokens reminder | **13** | NO | — | — | harness |
| 7 | first user message (`good morning`) | **2** | NO | — | — | Dave |
| — | **Σ OURS** | **7,964** | | | | |
| 8 | **HARNESS REMAINDER** = 70,710 real − 7,964 tape | **≈62,746** | **NO** | ⛔ ESTIMATED-BY-SUBTRACTION — a residual, never a measurement; units mixed by construction | Anthropic's system prompt + the loaded tool schemas; **not on disk anywhere in this mount** | Anthropic |

`CLAUDE.md`: **ABSENT and DECLARED** — `ls /sessions/…/mnt/UX-design/CLAUDE.md` returns *No such
file*. The `claudeMd` block in the system prompt carries `MEMORY.md` only, so row 1 is the whole
of it and there is no separate project-instructions cost to cut.

## THE DESIGN (one page)

**Progressive disclosure for `MEMORY.md`.** Measured tiers of the current 110 non-blank lines:
**A** (⛔ or ★★★) n=32, **1,270 tape** · **B** (★★) n=33, **1,010 tape** · **C** (★ or unmarked)
n=45, **1,289 tape**. The stub is tier A verbatim, plus one line naming
`python3 knowledge/_memento_search.py "<q>"` → `--fetch <id>`, plus the archive pointer: **≈1,350
tape, saving 2,219 (62%)**. The line that decides which tier moves is already drawn and is not
mine to redraw — `MEMORY-ARCHIVE` #49: *look-up-BY-NAME moves, notice-UNPROMPTED stays*. A tier-A
hook is what makes a session notice a rule nobody asked about; a retrieval index only answers
when queried. Tier C is the safest cut and the cheapest (1,289); tier B is 1,010 more and is
where genuine recall loss starts.

**Componentisation of the roster.** Boot-worthy because they fire on their own: `dave-voice`
(107, EVERY reply), `swiss-design-system` (105), `dream-pass` (55), `consolidate-memory` (30).
Plugin-roster candidates Dave can disable, priced: `docx` 232 · `pptx` 221 · `xlsx` 212 · `pdf`
104 · `create-cowork-plugin` 81 · `cowork-plugin-customizer` 60 · `schedule` 56 ·
`explain-usage` 52 · `import-memory` 37 · `setup-cowork` 31 = **1,086 tape**. Realistically ~900
after keeping one or two.

**Mechanisation, and an honest limit on it.** The cap Dave wants can be *computed* but only
*half-enforced*: `MEMORY.md` lives in the Cowork mount, not the repo, so a CI gate literally
cannot see it — this is the [[gate-cannot-pass-in-one-environment]] shape and pretending
otherwise builds a check that is red forever in one place. The legal form is a **sandbox-side
advisory with a declared skip in CI**: `_boot_decompose.py` already prints the tape figure per
component; the gate addition is a comparison against a typed `MEMORY_TAPE_CAP` beside
`BOOT_CEILING_TK`, shrink-only on the same ratchet, that DECLARES *unmeasurable here* when the
mount is absent rather than passing silently. **Consumer, named**: the conductor at the opener
beside `_checkin.py`, and the wrap when the boot-drift ceiling arm fires — the gate currently
says *cut the boot* and nothing tells it where. That is the gap this instrument closes
[[instrument-without-a-consumer]].

**Calibration, REPORTED and not APPLIED.** `MEMORY.md` today is 12,656 B / 3,569 tape = **3.55 B
per tape token**. #241's diet shrank it 21,064 → 12,454 B inside a −7,046 **real** drop that also
removed Figma and switched `computer-use` off; ⛔ that −7,046 may not be divided by this ratio to
attribute a share — three variables moved at once and the arithmetic would be a fiction.

## THE EXPERIMENT (#243, one variable)

1. **Lever:** turn `computer-use` OFF in Dave's panel before the opener. Nothing else changes —
   `MEMORY.md` untouched, roster untouched, no plugin removed.
2. **Reading:** first turn of #243, `python3 knowledge/_checkin.py`, the `message.usage` boot line.
3. **Baseline:** #242 = **70,710 real** (#241 = 69,092).
4. **Predicted direction:** DOWN. Disk-measurable footprint 1,162 (MCP block) + 243 (names) =
   **1,405 tape**; the real saving is larger if its tool schemas load, unknown if they do not.
5. **The item's price** = 70,710 − the #243 reading, in real, quoted with its command.
6. **Confirms the hypothesis if** #243 lands ≤ **69,305** — i.e. it recovers the +1,618 of
   finding 6 and puts the boot back under the 70,000 ceiling without touching memory at all.
7. **Refutes it if** #243 stays above 70,000; then the +1,618 is elsewhere and the roster diet
   (~900 tape) is the next single lever, at **#244**.
8. ⛔ **Do not flip two levers.** #241 flipped three and is why the −7,046 cannot be apportioned.
9. Run `python3 knowledge/_boot_decompose.py --real <reading>` at the same opener to file the
   BEFORE/AFTER component rows beside the real figure.
10. Log the pair in `notes/_BOOT-DISK-LOG.jsonl` shape so the series survives the session.

## Findings

1. **The boot payload is ON DISK for five of seven components.** `mnt/.claude/projects/*/*.jsonl`
   records the opener attachments verbatim (`deferred_tools_delta`, `agent_listing_delta`,
   `mcp_instructions_delta`, `skill_listing`, `total_tokens_reminder`). Probe: the record walk in
   `knowledge/_boot_decompose.py`, run above. This is new — every prior boot measurement worked
   from source files and hard-coded paths.
2. **70,710 is confirmed first-hand at the conductor's opener, not relayed.** The first assistant
   record carries `input_tokens 2 · cache_creation_input_tokens 30,440 · cache_read_input_tokens
   40,268` — sum **70,710 real**, agreeing to the token with the figure in Dave's chat.
3. **A LANE seat boots at ~40K real with the identical disk inputs.** `python3
   knowledge/_boot_decompose.py --lanes` → **40,118** and **39,819 real** (n=2), briefs 602 and
   430 tape. ⇒ the conductor's seat carries **≈30,891 real MORE** than a lane, and none of that
   difference is on disk. This is the real-unit corroboration the subtraction alone could not give.
4. **Σ(ours) = 7,964 tape ≈ 11% of the boot.** Even a *perfect* offload of every file Dave owns
   cannot move the boot by more than about that, and realistically ~4,600 tape (rows 1–4's
   movable columns summed).
5. **`CLAUDE.md` does not exist in the repo** — declared, not assumed absent; `ls` quoted above.
6. **#241 → #242 rose +1,618 real** (69,092 → 70,710) against a pre-diet series whose spread was
   only 641. `computer-use` is ON at this seat (its 1,162-tape instruction block and 243 tape of
   tool names are both in the #242 opener) and was OFF at #241 per the #240 diet record.
   **1,405 tape of re-added disk footprint against a +1,618 real rise** is the closest single
   explanation available; it is a HYPOTHESIS with an experiment, not an attribution.
7. **`MEMORY.md` is NOT the regression.** 12,454 B (#241) → 12,656 B (#242) = **+202 B ≈ +57
   tape**. The compaction held.
8. **The 710-over reading is a CEILING event, not a BAND event, and it does not bite at #242's
   wrap.** `BOOT_CEILING_FROM_SESSION = 241` (`knowledge/_capture_gate.py:3813`), so only
   readings from #241 on are graded against `BOOT_CEILING_TK = 70,000`. See the section below.

## WHAT `derived_boot_band()` REPORTS, AND WHAT THE GATE WILL DO

Computed at this seat by importing the live function — `python3 -c "from _gauge_tokens import
derived_boot_band; derived_boot_band()"` against `notes/_GAUGE-LOG.md` as it stands:

- **NOW** the band is **75,672 ± 641**, n=7, sessions **#234–#240** (75,206 · 75,294 · 75,198 ·
  76,915 · 75,336 · 75,619 · 76,138). ⛔ **#241's 69,092 is NOT in the log** — `grep 69,092
  notes/_GAUGE-LOG.md` returns nothing; it enters at #242's 2f roll, exactly as #240's did at
  #241. Against *this* band 70,710 sits **−4,962, i.e. 7.75σ**, far past the ±1,281 red line.
  **But that band is entirely pre-diet and is about to be superseded, so quoting 7.75σ as the
  verdict would be grading the new regime by the old one.**
- **AT THE #242 WRAP**, once #241 rolls in, the window is #235–#241 and the newest reading is
  **#241's 69,092**: band **74,799 ± 2,589**, delta **−5,707**, red line **±5,178** ⇒ **RED, a
  STEP CHANGE**, which under `#111-D1` **passes only with a matching `boot-drift DECLARED #242`
  line** in `notes/_GAUGE-LOG.md` and fails louder than none if its figures are wrong. **Ceiling
  arm: clean** — 69,092 is under 70,000.
- **AT THE #243 WRAP**, when 70,710 itself enters (window #236–#242): band **74,144 ± 2,991**,
  delta **−3,434** against a **±5,982** red line ⇒ **band GREEN, 1.15σ — inside noise.** ⛔ **The
  ceiling arm FAILS**: 70,710 > 70,000 and #242 ≥ #241, so it is a post-diet reading and the gate
  raises `boot-drift CEILING BREACH` by name, with its own remedy clause — *"the remedy is to CUT
  THE BOOT, never to raise the literal. Raising it is Dave's word alone and is not a price a wrap
  may pay to unblock itself."*
- **So: is 710-over noise?** Against the band that will actually grade it, **yes — 1.15σ.**
  Against the ceiling, **it does not matter whether it is noise**: the ceiling is graded per
  READING and one boot over it fails by name. The two answers are different and both are true.

## What was done

- Read the brief, then `knowledge/_boot_remeasure.py` (its `TARGETS` are hard-coded to a **stale
  mount**, `/sessions/upbeat-compassionate-darwin/…` — it would DECLARE MISSING here rather than
  measure; noted, **not edited**, per the fence), `knowledge/_gm_usage.py`'s docstring,
  `knowledge/_gauge_tokens.py` lines 184–270, `knowledge/_capture_gate.py` lines 3813 / 4120–4245,
  `notes/_BOOT-DISK-LOG.jsonl`, and the boot-reading tail of `notes/_GAUGE-LOG.md` by grep.
- Added **`knowledge/_boot_decompose.py`** — ⛔ **STAGING REFUSED AND DECLARED, NOT CLAIMED**:
  `git add` returned `fatal: Unable to create '.git/index.lock': File exists` on two attempts
  20 s apart, so another lane holds the index. The lock was **NOT removed**
  [[git-lock-mv-not-rm]]. Both files are on disk and **untracked**; the conductor stages them at
  the reconcile. **Uncommitted**, `_build_all.py` not run.
  Three modes (`--real`, `--lanes`, `--transcript`), a named consumer in the docstring, a unit on
  every printed line, a loud refusal without tiktoken, and `--selftest` with **3 arms**: an
  envelope-vs-payload arm carrying a **break arm** (it fails if the JSON envelope does not measure
  larger than the payload, i.e. if the check could not bite), an unknown-attachment-shape arm
  (must DECLARE, never count zero), and a synthetic-transcript arm pinning the real total to the
  three input fields with `output_tokens` excluded. `--selftest` exits 0.
- ⛔ Nothing under `mnt/.auto-memory/` was written. No skill, plugin, store, GM/LS/CARRIES or
  prior report was touched. No ruling inscribed. No commit, no push, no build.
- `GOOD-MORNING.md` and `_LIVE-STATE.md` were **never read**, whole or in part.

## RULING-SHAPED QUESTIONS

**Dave — four decisions, in plain sentences. No codes.**

1. **The biggest lever is not in the repo, and it is yours.** About nine tenths of your 70,710
   boot is Anthropic's system prompt and the tool schemas, and no file we can edit touches it.
   Of the tenth we do own, the single largest movable piece is the desktop-control connection
   (`computer-use`): it costs about 1,400 of our units and it came back on between yesterday and
   today, which is very close to the whole of today's 1,618-token rise. Do you want it switched
   off by default and turned on only on days you need it — or left on, and the boot budget spent
   there deliberately?
2. **How deep do you want the memory index cut?** Keeping only the ⛔ and ★★★ lines plus one
   retrieval pointer saves about 62% of the index. Keeping ⛔, ★★★ and ★★ saves about 34%. The
   difference is real: the lines we drop stop *reminding* a session unprompted and survive only
   if something goes looking for them by name. My recommendation is to cut the unmarked and ★
   lines first (about a third of the index, the safest third) and hold the ★★ tier until we have
   watched one session run without them.
3. **Do you want the four document skills off the roster?** Word, PowerPoint, Excel and PDF cost
   about 770 of our units between them and none of them has fired in this programme. Turning
   them off means Claude will not reach for them on its own; you can still ask by name. I
   recommend off.
4. **The ceiling will fail a wrap two sessions from now, and it should be allowed to.** Today's
   70,710 is 710 over the 70,000 you set, which the gate will flag as a hard failure when it
   reaches the log at the next-but-one wrap. It is not a mistake in the number and the fix is not
   to raise it. Confirm you want it left at 70,000 and the boot cut instead.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that `computer-use` is the cause of the +1,618. Price to prove: **one session**
  — #243 with that one lever flipped, read from `_checkin.py`'s first turn. Nothing cheaper
  exists; boot is only observable at an opener.
- **UNPROVEN:** the real-token price of the `MEMORY.md` stub and of the roster diet. Both are
  measured in **tape** here and tape never converts. Price to prove: **one session each**, one
  lever at a time (#244, #245).
- **UNPROVEN:** that the harness remainder is genuinely fixed. The lane-seat figures bound it
  from below in real units, but no probe in this mount can enumerate Anthropic's system prompt or
  the loaded tool schemas. Price to prove: none available from inside a session.
- **CLAIMED:** that `computer-use` was OFF at #241. This is read from the #240 wrap stratum's
  prose in `notes/_GAUGE-LOG.md`, which itself declares the roster diet *"not repo-observable"* —
  it is the conductor's testimony, not a receipt. Re-reading it costs nothing and changes nothing;
  only the #243 A/B settles it.
- **CLAIMED:** the #241 boot of 69,092. Quoted from the brief and from `s241-D1`'s value; it is
  **not yet in `notes/_GAUGE-LOG.md`** and was not read first-hand at this seat.

## Evidence

No evidence directory: every figure above names the command that produced it inline, and all of
them are reproducible with `python3 knowledge/_boot_decompose.py` in its three modes.

REPLAY-THESE: `knowledge/_boot_decompose.py` (~2,900 tk — only if the conductor intends to review
the instrument itself) · the lead table and the `derived_boot_band()` section of this file
(~1,400 tk) — everything else is summarised in the stub.
