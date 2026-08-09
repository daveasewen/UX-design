# #138 — the fontconfig permanent fix: a symlink farm, and a false green that read ten faces as one

```
provenance: wrap-sub #138 · 2026-08-09
status: observed
```

Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#138) and § OPEN (closure entry over the #137
fontconfig item) · Banner: `GOOD-MORNING.md` ★ LATEST #138 · Source runbook:
`knowledge/_RUNBOOK-render-verify.md` § SYMLINK FARM (#138) · Gate:
`knowledge/_capture_gate.py::instrument_stray_check` · Predecessor arc:
`_DECISION-HISTORY/2026-08-09-137-dream-pass-6-triage.md` (Finding 5, where the cause was
diagnosed and priced but not enacted).

⚠ **Written by the wrap sub from the conductor's session facts.** The drives, probes and
measurements quoted below are the conductor's own first-hand work this session, reported here,
not re-run by this sub — this sub's own first-hand work is the capture ritual itself (the
mover ops, the roll-state and section-usage measurements, the title derivation), which is
reported as such.

---

## Why this session existed

#137 closed with the fontconfig cause **diagnosed and priced, not enacted**: #136's ENOSPC fix
had pointed `FONTCONFIG_FILE`'s `<dir>` straight at the repo's own TTF directory to avoid copying
fonts onto a nearly-full disk, and fontconfig's own directory-identity marker (`.uuid` and its
lock/temp siblings) then landed inside the tree it was scanning, tripping the clean-tree push
gate. Dave's instruction from #137 stood unenacted: *"no patches or hacks, solve it permanently
please."* #138 opened as one titled lane to finish exactly that — inherited whole as #137's
residual ①.

---

## Finding 1 — the permanent fix is a symlink farm, and it had to be DRIVEN, not asserted

Copying the TTFs back out of the repo (the old, pre-#136 recipe) would reopen the ENOSPC
constraint that forced #136's change in the first place. Symlinking them costs almost nothing:
`ln -s` each repo `.ttf` into `/var/tmp/fonts-<session>/`, then point `FONTCONFIG_FILE`'s `<dir>`
at that farm instead of the repo path. Fontconfig's `.uuid` marker then lands in `/var/tmp`,
never in the tree it scans — ~5 KB of links against the same disk budget #136 was defending.

**The premise was reproduced first-hand before anything was built on top of it.** Running
`fc-cache` against a conf whose `<dir>` was still the repo TTF directory reproduced the exact
three stray names #136 had left — `.uuid`, `.uuid.LCK`, `.uuid.TMP-XXXXXX` (the `.TMP` suffix is
a random atomic-write token; #136 got `NpSPVs`, this run got `SpeXCi`). That the defect
reproduces on demand is what makes the fix's later absence of strays a real finding rather than
an assumption that nothing happened to fire this run.

**Driven three ways, with a mutation that discriminates rather than merely repeating the green:**

| leg | setup | repo strays |
|---|---|---|
| A | farm conf, `<dir>` = `/var/tmp/fonts-<session>` (clean dir) | **0** |
| B | mutation — ONLY `<dir>` swapped back to the repo, everything else identical | **3** (so the test CAN fail) |
| C | after cleanup | **0** |

Leg B is the point: a test that only ever runs the working configuration cannot tell a real fix
from a fix that was never exercised. Enacted in `knowledge/_RUNBOOK-render-verify.md` as a new
`§ SYMLINK FARM (#138)` block, by addition — #129's and #136's recipes stand as history, with a
pointer marking the `<dir>`→repo element on `:42`/`:46` SUPERSEDED rather than deleted.

---

## Finding 2 — the first verification probe was a false green, and it is the same class as #137's

**The first width-probe against the fixed configuration returned 345 for every face measured —
including a face that does not exist.** That is not a passing test; it is an instrument that
cannot fail, reporting the same number regardless of what it is asked to check.

**Cause:** `FONTCONFIG_FILE` *replaces* the system fontconfig, it does not layer on top of it. The
working conf had no `<include ignore_missing="yes">/etc/fonts/fonts.conf</include>` line, so it
exposed only the ten faces physically present in the symlink farm (all HSBC cuts) against 394
available on the box. Every font request — the real HSBC alias, a control face that should differ,
even a face name that does not exist anywhere — fell back to the only faces fontconfig could see,
and they all measured the same canvas width.

**The second-order consequence is the one worth keeping.** A page rendered against this broken
configuration renders *entirely correctly in the HSBC cut*, because there is nothing else for it
to fall back to. It looks like a pass. **#136-era renders, made under the same missing-`<include>`
shape, could not have shown a fallback bug even if one existed** — the render being visually
correct was never evidence that the fallback chain was intact, only that the narrow font set
happened to contain what was asked for.

The `<include>` line is now written into the runbook as mandatory, with the reasoning attached so
the next session does not have to rediscover it by reproducing the same false green.
`document.fonts.check()` was tried as a cheaper alternative assertion and returned `true` in
**both** the broken and the working configuration — recorded as worthless for this purpose, not
merely unused.

**Class:** [[green-tests-cannot-see-scope]] — a green that cannot fail is an assertion, not a
test. This is the same shape as #137's `sed`-grabbed-comment-lines false green (Finding 3 of that
session's dossier), two sessions running. The specific, transferable lesson here is narrower than
the slogan: **a probe against a narrowed environment cannot tell "correct" from "nothing else was
available to be wrong."** The fix is a control, not a boolean — see Finding 3.

---

## Finding 3 — the working assertion needed a control, not a boolean, and the runbook records the recipe

Once the `<include>` gap was found, the verification was rebuilt to compare against controls
rather than trust a single reading:

| probe | broken conf | working conf |
|---|---|---|
| `HSBC_MtUnivers_Latin` (the real cut) | 345 | **347** |
| `Univers Next HSBC` (type.css `--uf` alias) | 345 | **347** |
| `Univers Next for HSBC` (snippet `--font` alias) | 345 | **347** |
| `DejaVu Sans` — a genuinely different face | 345 | 375 |
| a nonexistent face — the default-fallback control | 345 | 301 |

*(40px `Handgloves 12345`, `showroom/chart-bar.html`, `goto file://` — never `set_content()`,
which drops `type.css` silently — identical at 1180 and 480.)* The assertion that catches a silent
fallback is that **both aliases land on the target number and on neither control's number.** This
table, and the requirement to measure against two controls rather than one boolean, is now in
`_RUNBOOK-render-verify.md` alongside the `<include>` line — the runbook previously recorded only
the `FONTCONFIG_FILE` environment variable, never the conf body, and that gap is what let #136's
`<dir>` choice travel three sessions unexamined.

**And the tree was asserted, every render run, not just the font:** `ls -a <TTF dir> | grep -c
'^\.uuid'` → **0**, and `git status --short --untracked-files=all -- knowledge/` → **0 lines**,
both re-confirmed after the real render (leg C above).

---

## Finding 4 — two operational potholes, both owned in the same lane rather than worked around

**ENOSPC, fourth occurrence.** `/sessions` was 100% full with 18 M free at session open — the
same fixed-cutoff shape as #129 and #136; `/` had 1.7 G. `/var/tmp` persisted across sessions
(`pw-browsers-{129,s131,s136}`, `pylibs`, `chromelibs` all survived from prior sessions), so no
Chromium download was needed this time — but three 344 M browser copies now sit in `/var/tmp`
against 1.7 G free, and pruning them is explicitly not this lane's call.

**A cross-filesystem `mv`, hit twice.** `mv` from the repo mount to `/var/tmp` fails — it is a
different filesystem, so the kernel falls back to copy+unlink, and the unlink of the source is
denied (`Operation not permitted`), leaving the original file in place. This briefly left the
session's own reproduction strays sitting in the tree. A same-mount `mv` to `_to_delete/` is a
rename and works, which is the existing convention. The second occurrence of this pothole was
caught **by the new gate** (Finding 5) rather than by inspection — an unplanned live
demonstration that the gate does what it was built to do.

---

## Finding 5 — the class is now gated: an instrument writing into the tree it measures

**The class, named because it took two instances in two sessions to see it clearly:** `s137-D1`
(the verification instruments themselves appending to a tracked rehearsal log) was the first
instance; fontconfig's `<dir>` pointed at the repo was the second. Until this session, the only
thing that ever caught a stray was the `--push` clean-tree assertion — the last possible moment,
after all the work, and it already carries one named exclusion that could in principle widen.

**`instrument_stray_check()`, new in `knowledge/_capture_gate.py`, wired into `wrap_checks()`.**
Two passes, and the second one is the point:

- **Pass 1** respects `.gitignore` — because `knowledge/assets` was measured to carry **60**
  untracked-but-ignored paths (`.DS_Store` files, the unlicensed Helvetica Armenian webfont
  companions), and a gate that ignored `.gitignore` wholesale would fire on every single wrap.
  Noise is how a gate gets switched off, not how it earns trust.
- **Pass 2** re-checks the same directories *without* `--exclude-standard`, filtered to
  `INSTRUMENT_SIGNATURES = (".uuid",)` — so adding `.uuid*` to a `.gitignore` entry cannot blind
  this gate. Dave refused exactly that ignore rule at #137, on the grounds that it hides an
  instrument still writing where it must not; pass 2 makes that refusal structural rather than
  something a future session has to remember and re-litigate.

**Driven four ways, not asserted:** a clean tree stays silent · a planted `.uuid` +
`.uuid.LCK` pair FAILS, classified `structural` · the same planted files, then added to
`.gitignore`, STILL fail · a non-signature untracked file fails via pass 1 alone (the general
case still works). `py_compile` is clean.

**Why it lives at the wrap seam and not in `_build_all.py`, deliberately:** the obvious home for
a check like this is the build's own selftest, but a full `_build_all.py` run is
sandbox-impossible (~49s against the ~45s call-kill), which is exactly how `_capture_gate.py
--selftest` itself sat red for three consecutive wraps (#137's Finding 6) with nothing able to
see it. A gate that cannot run in the mode the work actually happens in cannot fail, and a green
that cannot fail is an assertion — the same lesson as Finding 2, applied to the gate's own
placement rather than to a render probe. It ran inside this session's own wrap-decision
rehearsal and was correctly silent, which is the first live proof that it fires at the seam it
was designed for.

**Scope, stated rather than left implicit:** `INSTRUMENT_READONLY_DIRS = ("knowledge/assets",)`
— asset directories that instruments read and humans do not hand-author, so an untracked path
there is presumptively an instrument's. It does not police the whole tree; untracked
work-in-progress elsewhere during a session is legitimate and this gate has nothing to say about
it.

---

## What was put to Dave, and what was not

**Nothing this session was put to Dave as a ruling with named alternatives.** The one instruction
recorded is Dave's own gate-scope answer — asked as a four-option question about how far to
widen `instrument_stray_check`'s enforcement, he answered *"i just want a solid fix."* Read as:
stop presenting menus, make it solid. The narrow, wrap-time-only gate described above is what was
built on that instruction. **It is recorded here as an instruction, not a ruling** — no `s138-*`
id was minted in `knowledge/_rulings.json`, because promotion to a ruling is Dave's alone and
nothing here was offered to him as a choice between alternatives.

---

## What is resolved, and what is still open

**Resolved:** the fontconfig cause, fixed by the symlink farm and driven three ways plus a real
render. The false green, caught before anything was reported on the strength of it, and
attributed to a specific missing `<include>` line rather than patched over. The instrument-stray
class, gated at the wrap seam with a two-pass design that survives a `.gitignore` attempt to
blind it.

**Open, and none of it is this wrap's to close:**

- **The symlink farm is unproven in a COLD sandbox.** This session re-used `/var/tmp` staging
  left behind by #129, #131 and #136 (`pw-browsers-*`, `pylibs`, `chromelibs` all survived);
  runbook steps 1–4 (the actual download-and-install sequence) were never re-run against an empty
  `/var/tmp`. Declared here rather than left to be discovered the next time `/var/tmp` is
  genuinely empty.
- **Three 344 M browser copies in `/var/tmp`** against 1.7 G free — pruning them is not this
  lane's call.
- **The 7 residual `_governs` prose-in-`evidence` pointers** on five inherited ratified records
  (#137's Finding 6) — untouched, still Dave's.
- **Dream pass 6, P1/P3/P4/P5** — still Dave's, all unruled.
- **`chart-bar.html`'s x-axis labels crowd/overlap at 480px** — seen during this session's own
  render pass, not investigated, not this lane.
- **The wrap-step candidate** (`git log` since boot, foreign commits named in the banner) —
  Dave's words from #137, still floated, not ruled.
- **The 16 tier-map rows, the `s136-D1` enact lanes, lane A's held enactment sub, and the three
  readbacks (clause-A copy · #67-D2 · mono no-border)** — all carried forward unchanged.

---

*Both-way links: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#138) and § OPEN (closure entry, born #138) ·
`GOOD-MORNING.md` ★ LATEST #138 · `knowledge/_RUNBOOK-render-verify.md` § SYMLINK FARM (#138) ·
`knowledge/_capture_gate.py::instrument_stray_check` · `notes/_GAUGE-LOG.md` § #138 (post-wrap) ·
predecessor `_DECISION-HISTORY/2026-08-09-137-dream-pass-6-triage.md` § Finding 5.*
