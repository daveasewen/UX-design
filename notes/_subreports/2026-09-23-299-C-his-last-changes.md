# #299-C: Dave's last changes to the plain Friday deck

provenance: 299 · 2026-09-23
status: observed
session: #299 · 2026-09-23 · lane C (Opus 5.5, remote-device seat)
brief: the conductor's in-chat brief to lane C. Dave's words, 13:34 BST: "last few changes for now. in slide order." (verbatim in the brief)
tokens: UNMEASURED (this lane's message.usage cannot be read from the device seat)

## VERDICT

**DONE, all eight items. One is declared as a deviation and one is flagged for Dave's eye.** Copy items 1, 2, 4, 5, 7 and 14 landed in commit 1, together with the rail label. Slide 09 landed on its own in commit 2. The pixel diffs, before against after at 1920x1080 and 1440x900, show only 01, 02, 04, 05, 07, 09 and 14 changing. The deck was rebuilt with `build_c.py` every time and never hand-edited. `build_e.py` was not run.

- ⚠ **DEVIATION, declared: the rail label lives in `notes/_lanes/296/C/build_c.py`, not in the source.** The rail's chapter titles are the `PLAIN_CHAPTERS` constant, which is injected at build time. The source has no rail label. So "change the rail label to Result too" and "edit only the source" could not both be met. I changed the one title string in `build_c.py` (line 213), the same place #297 D added the Evolution chapter, and added a two-line comment. Nothing else in `build_c.py` changed.
- ⚠ **Slide 09, for Dave's eye.** Its resting angle now matches the brain's exactly, "the same way": the callipers' camera `YAW0` goes from -35 to -27, with pitch 20 kept. The plate's on-screen edges are now parallel to the brain's plate on slide 10. But the calliper's plate is long along its beam, and it lies a quarter turn (PSI -90) from the other plates. So on 09 the plate's long side still recedes to the right, where the long sides of the plates on 07, 08 and 10 run across the front. That quarter turn is the object's lie on the plate (#296 E2), not its resting angle, and it was not touched. Also, slides 07 and 08 still rest at -35 / 20 (see item 9). If Dave's "match the others" meant the plate's turn, that change is PSI, not the camera angle.

## The items, in slide order

Source = `notes/_lanes/296/C/v14-plain-before-c.html`. Line numbers are as they now stand.

1. **01, the strap on one line.** DONE. Source line 428.
   - old: `A smart design engine powered by&nbsp;AI<br>on brand, on standard, accessible, at&nbsp;speed`
   - new: `A smart design engine powered by&nbsp;AI &mdash; on brand, on standard, accessible, at&nbsp;speed`
   - Measured before editing: at 26px the one-line strap is **975.6px** wide. Its `max-width:34em` (884px) would have wrapped it, and the column (`.inner`) is 1120px at both render sizes. So the measure was lifted, and the **type was not shrunk**: source line 184 `#s1 .sub{... max-width:34em ...}` → `max-width:none` plus a comment. The 1120 column bounds it now, with 144px to spare.
   - Probe (`_work/probe_after.py`): `strap_lines: 1` at 1920x1080 and at 1440x900. Font size 26px at both, as before.
2. **02, the order of play, chapter 5.** DONE. Source line 448.
   - old: `<b>The result<em>demo &middot; what she is made of</em></b>`
   - new: `<b>Result<em>the working system</em></b>`
   - Evolution and the other four chapters are unchanged.
   - **The rail changed too** (`build_c.py` line 213): `{n:5, title:'The result',  id:'s9',  subs:[]}` → `{n:5, title:'Result',      id:'s9',  subs:[]}`. The rail shows only the current chapter's title (`tinyTitles:false`), so **the label is visible only on slide 14**. There, "5 THE RESULT" now reads "5 RESULT". It is also in each rail button's aria-label ("5 Result"). Probe: the rail titles are now Problem · Research · Evaluation · Evolution · Result · The ask.
   - No other chapter name was changed. Pre-existing and left alone: the rail has a sixth chapter, "The ask" (15-16), which the order of play (5 chapters) does not list.
3. **03.** Dave: "good". Untouched.
4. **04.** DONE. Source line 472.
   - old: `<b>The work checked automatically and by a human.</b>`
   - new: `<b>The work checked automatically, and then by a human.</b>`
   - The heading stays at 3 lines at both sizes.
5. **05.** DONE. Source line 493.
   - old: `<b>the agents invented parts &mdash; and got them&nbsp;wrong.</b>`
   - new: `<b>the agents &lsquo;innovated&rsquo;, they invented components, but got them&nbsp;wrong.</b>`
   - The curly quotes use the deck's own entity style (`&lsquo;Agile&rsquo;` on 03). The `&nbsp;` before "wrong." that guards against a widow is kept.
   - The heading goes from 3 to 4 lines at both sizes. There is no overflow, and the rail gap is unchanged.
6. **06.** Dave: "good". Untouched.
7. **07, the emphasis.** DONE. Source line 520. The text as it stood (it does say 36 and 137): `<h2 class="rv d1"><b>The first improvement:</b> the catalogue went from 36 to&nbsp;137.</h2>`
   - new: `<h2 class="rv d1">The first improvement: <b>the catalogue went from 36 to&nbsp;137.</b></h2>`
   - This copies the sibling pattern exactly: a plain lead-in, a space, then the fact in `<b>`. The siblings are 08 `The second: <b>we started to build ...</b>`, 09 `Third: <b>the system checks ...</b>`, 10 `Fourth: <b>a designer&rsquo;s judgement ...</b>` and 11 `... <b>and gave us the opportunity ...</b>`.
   - The line count is unchanged (2 at 1920, 3 at 1440). The existing break before "to 137" at 1440 is as it was.
8. **08.** Dave: "good". Untouched.
9. **09, the callipers' resting angle.** DONE, flagged (see VERDICT). Source line 6594, inside the callipers' own IIFE (`getElementById('cp')`). The same constant appears on four other drawings' lines, and those were left alone.
   - old: `var YAW0 = -35*D2R, PIT0 = 20*D2R, YAW_R = 25*D2R, PIT_R = 12*D2R, TAU = 1.0;`
   - new: `var YAW0 = -27*D2R, PIT0 = 20*D2R, YAW_R = 25*D2R, PIT_R = 12*D2R, TAU = 1.0;` with a 4-line non-rendered comment above it (Dave's words, the old value, PSI untouched, the orbit window).
   - How #298 B did it (its report): the brain's rest was one constant, `YAW0` -35 → -27 with PIT0 20 kept ("reading B"). The **shared** rest angle is still **-35 / 20**, and the books (07) and shells (08) sit there. #298 B moved the brain alone off it, so the brain's plate edges read 9.89° / 33.87° against 13.47° / 26.03° for the shared set. The callipers is built the same way (`YAW0`/`PIT0`/`YAW_R`/`PIT_R`/`setView`), so the same one-constant change applies. Per the brief, 09 now rests at the brain's -27 / 20.
   - Probe `calView()` at rest: before yaw -35 / pitch 20, depth coefficients beam -0.770 / jaws +0.539. After: **yaw -27 / pitch 20**, beam -0.837 / jaws +0.427.
   - The plate's screen edges, by atan(sin 20° · tan(yaw - θ)): before 13.47° (the short side) / 26.03° (the long side), parallel to 08's shells. After: **9.89° (short) / 33.87° (long)**, parallel to 10's brain. On the brain, the 9.89° edge is the long side. On the callipers it is the short side, because of PSI -90.
   - Fit: the drawing re-fits itself from the orbit sweep (`sweepBox`, K 0.42). The rest scale goes 3.4448 → 3.659 at 1920 and 2.8789 → 3.058 at 1440, so the callipers rest about 6% larger. The rest frame is fully in frame at both sizes.
   - The orbit is now yaw -52..-2 (was -60..-10). It stays inside the window where the painter's order is exact for PSI -90 (the beam's depth coefficient < 0 and the jaws' > 0 need yaw in -90..0). At the mouse corners the jaws' coefficient is +0.03 / +0.04, positive but with little margin. At yaw -2 the view is nearly a front elevation.
   - Pre-existing, made a little worse: at the two left mouse corners (yaw -52 / -60) the plate's far end runs past the canvas's right edge. The draw box's right edge is 759.8 against a 668 canvas at 1440, where before it was 728.9 against 668. That is the K 0.42 fit trading orbit room for rest size, as designed. The rest pose is unaffected. Shots: `_work/orbit-after-*.png`.
10. **10–13.** Dave: "good". Untouched.
14. **14.** DONE. Source line 769.
    - old: `<b>Let&rsquo;s build something.</b>`
    - new: `<b>Let&rsquo;s see what it&rsquo;s made.</b>`
    - This is Dave's wording verbatim. He starts the roughly 11-minute build at the top of the talk. Apostrophes use `&rsquo;`, as the deck does throughout. The heading stays at 1 line.

Nothing was skipped. Every old text quoted in the brief was found on the slide number given.

## Render checks

Every render ran at the seat, on the mount, one bash call per viewport: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/299/C/_work/shoot_c.py <deck> <dir> WxH`. The driver is a copy of `notes/_lanes/297/W/_work/shoot_w.py`: `goto("file://…")`, `executable_path=$RENDER_SHELL`, freezes and pointer block. Each viewport took about 43 s. The diffs used `_work/pdiff_c.py`, a copy of `pdiff_w.py`, which splits the rail band (x<200) from the content.

**Pixel diff, the pre-edit deck against the final deck. All 16 slides plus 11's second state:**

| slide | 1920x1080 | 1440x900 |
|---|---|---|
| **01** s1 | content DIFF (the strap) | content DIFF. The "rail band" x 160-200 is the strap itself: the rail is hidden on 01 and the column starts at 160 |
| **02** s2 | content DIFF 1328-1513 x 625-665 (chapter 5 only) | content DIFF 1124-1302 x 537-574 |
| 03 s3 | SAME | SAME |
| **04** s5x | content DIFF (the heading) | content DIFF |
| **05** s5r | content DIFF (the heading, one more line, the leads move down) | content DIFF |
| 06 s4p | SAME | SAME |
| **07** s6 | content DIFF (the heading); rail 10 px, see below | content DIFF |
| 08 s7 | SAME | SAME |
| **09** s8 | content DIFF 892-1595 x 365-715 (the drawing only) | content DIFF 726-1314 x 303-597 |
| 10 s7b · 11 s6b · 11b s6b · 12 s10 · 13 s10map | SAME | SAME |
| **14** s9 | rail DIFF 72-161 x 405-414 (the title "THE RESULT" → "RESULT") + content DIFF (the heading) | rail DIFF 72-161 x 337-346 + content DIFF |
| 15 s11 · 16 s12 | SAME | SAME |

- **The rail band differs only on 14**, which is the one slide where chapter 5 is current and its title shows. On 07, 10 rail pixels differ with a maximum channel sum of 3/765 (bbox 34-42 x 274-277 at 1920, 34-42 x 248-251 at 1440). That is the harness's own flicker, which #298 B measured between two shots of the same unedited deck. It shows up in some pairs and not others (copy → final at 1440 has it; before → final at 1440 does not).
- **Commit-by-commit.** Before against the copy-only deck: 01 02 04 05 07 14 differ, nothing else. The copy-only deck against the final: **09 content only** (plus the 07 flicker).
- **DOM facts** (section order, element counts, the full slide text, pagenums): the only text changes are the six intended ones. s1 has one element fewer (the `<br>`). The final deck's facts are identical to the copy-only deck's, so 09 changed no text.
- Rail-collision and overflow checks: 0 rail hits anywhere. The rail gap on 14 widens (37.4 → 71.5 at 1440, 237.4 → 271.5 at 1920) because "RESULT" is shorter. The one flagged render, 11b-s6b (4 box items on the "Proposal:" line), is pre-existing and unchanged. 0 page errors and 0 console errors, before and after. `anatomyState()` is unchanged (the callipers is not in slide 12's anatomy).
- **By eye**, at this seat on the 1440 shots: the strap is on one line; 02 reads "5 Result / the working system"; the 05 heading wraps cleanly to 4 lines; on 07 the fact carries the bold as on 08-10; 09's drawing is whole and rests at the brain's angle; 14 reads "Let's see what it's made." with "5 RESULT" on the rail.

**Contact sheet: `notes/_lanes/299/C/before-after.png`** (2952x7232, 1.12 MB). Seven rows (01 02 04 05 07 09 14), each with the 1440x900 render BEFORE on the left and AFTER on the right, labelled. The driver is `_work/sheet_c.py`.

## Commits

See § POST-COMMIT for the second commit's sha. Both commits went through `SESSION_N=299 INSTRUMENT_AUTOSTAGE=0 bash knowledge/_git_commit.sh --reconciled --quiet=<log> <msgfile> <paths>`, with the msgfiles written by python and line 1 a plain summary (T3 adds the prefix).

1. **`2f0a385d`** (`2f0a385d00a225d26029e7395ae900dcc0f3d0da`), `after #299 2026-09-23 — Dave's last copy changes to the plain Friday deck`. 3 files, +18 / -16: the source, the rebuilt deck and `build_c.py`. All gates passed. The doc-row gate passed with rows present. The boot-drift check printed two ❌ FAIL lines (#297's boot reading, 127,600, over the 72,768 ceiling), but they did not block and are not this lane's. The run exited 0 with "locks clear". The transcript is `notes/_lanes/299/C/_gitcommit-C1.log`. Read-back: all three paths are byte-identical to HEAD.
2. **Slide 09**, with this report and the contact sheet. See § POST-COMMIT.

Pre-edit premise: the deck, the source and `build_c.py` were each byte-identical to HEAD `4c9b4040` (`git hash-object` against `git rev-parse HEAD:<path>`). `git status` was never run. There were no `.git` locks at the start.

## UNPROVEN / CLAIMED

- **UNPROVEN:** print (Cmd-P) was not rendered. The print CSS sets `#s1 .sub{font-size:22px}` in a 1136px column, so the one-line strap should fit (about 826px at 22px, scaled from the 26px measure). Price: one print-to-PDF of 01.
- **CLAIMED:** the books' plate edges (11.17° / 30.6°) come from the formula with the books' PSI -5. They were not measured on pixels.
- **UNPROVEN:** whether Dave's "match the others" meant the camera angle (done) or the plate's quarter turn (PSI, not done). The contact sheet's row 09, next to slide 10, is what he should rule from.

## PATHS

Changed, committed: `notes/_lanes/296/C/v14-plain-before-c.html` (the source) · `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt) · `notes/_lanes/296/C/build_c.py` (the rail label, declared).
Created, committed: `notes/_lanes/299/C/before-after.png` · this report.
Working files, **not committed**: `notes/_lanes/299/C/_work/`. This holds the pre-edit copies `before.html`, `source.before.html` and `build_c.before.py`; the mid-state `after-copy.html` and `source.after-copy.html`; the final `after.html`; the six render folders `before-*`, `copy-*` and `after-*` with `_facts.json`; the drivers `shoot_c.py`, `pdiff_c.py`, `sheet_c.py`, `probe_strap.py`, `probe_after.py`, `probe_cal.py`, `edit_copy.py`; and the peeks and orbit shots. Also not committed: the msgfiles `_msg-C1.txt` / `_msg-C2.txt` and the committer transcripts `_gitcommit-C*.log`.
