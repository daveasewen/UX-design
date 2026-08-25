# #219 lane 6 — gates backlog: package delta, gm_usage red, [hidden] class sweep, mask_comments fork

**Lane:** 6 of the #219 crank · **Model:** Opus · **Base:** `04655de`, clean tree · **Committed:** nothing (conductor reconciles).
**Brief:** `notes/_briefs/2026-08-25-219-crank-divvy.md` — DO-NOT-RULE honoured in full. No `_rulings.json` write, no constant, no threshold, no Dave row, no promotion, no memory write.

**COUNTS:** findings 5 · ruling-shaped 3 · UNPROVEN 2 · new instruments 1 (`_validate_hidden_display.py`, 1 file, ~330 instrument-lines, 0 feature-lines) · corpus signals from item C: 25 across 17 of 135 snippets (3 CERTAIN).

---

## Verdicts, one line each

| item | verdict |
|---|---|
| **A** — CI red [120] package delta | **NOT SYNCED — RULING-SHAPED, RETURNED TO DAVE.** There is no sync mechanism; the package's only sync path is a per-instance Dave authorization, and the last one was declared explicitly non-standing. The `_capture_gate.py` shim question is **CLOSED GREEN with evidence** — no re-port owed. |
| **B** — CI red [18] `_gm_usage.py --selftest` | **DIAGNOSED AT CAUSE, NOT PATCHED.** Not a lane-1/2 edit, not the #173 environment class. `#218 wrapped TWICE`, both wraps self-reported under the same session number with different testimony, and the reader has no way to represent that. **RULING-SHAPED.** |
| **C** — `[hidden]`-vs-author-display class check | **BUILT, ADVISORY, GREEN in both directions on 16 bites, RUN on the real corpus.** 3 CERTAIN live instances of the #218 defect found. **Repaired nothing.** |
| **D** — `mask_comments` duplication (W-92) | **ALREADY CLOSED at #218, before this lane's base — and closed better than the brief asked.** Verified end to end, including a fresh mutation. **Nothing to do; no divergence.** |

---

## A — CI red [120]: the package VERBATIM SET has drifted, and no mechanism exists to un-drift it

### What is red, verbatim

`python3 knowledge/_validate_package_delta.py`:

```
memento-package delta-audit: 2 failure(s)
  ✗ VERBATIM SET: memento-package/machinery/_gen_chain.py DIFFERS from knowledge/_gen_chain.py (copy=machinery/ file=_gen_chain.py) — 35 line(s) differ (sha256 20ba66b82a07 vs source 6f000fbef0d7)
  ✗ VERBATIM SET: memento-package/claude-plugin/memento/machinery/_gen_chain.py DIFFERS from knowledge/_gen_chain.py (copy=claude-plugin copy file=_gen_chain.py) — 35 line(s) differ (sha256 20ba66b82a07 vs source 6f000fbef0d7)
```

The `--selftest` red is the SAME fact seen from the other side, and this is worth stating precisely because the brief asked for "selftest green + one mutation arm red" and **the mutation arms were already all green**. The only failing bite is the real-repo control:

```
✗ real repo: clean (0 findings; got 2: [...the two VERBATIM SET lines above...])
```

**All eight mutation arms pass, at base, untouched by me** — ARM1 (doctored file / missing file), ARM3 (cross-copy divergence / pairwise-invisible both-copies-missing), ARM4 (rogue file named / `__pycache__` control), ARM2 (a/b/c/d — ported function changed, ported function gone, ported constant changed, docstring commit mismatch). The instrument is healthy. **Its subject is not.** There was no mutation arm for me to drive red that was not already red-on-demand.

### The drift is lane 2's, and it is real content

`git diff d178313~1 d178313 -- knowledge/_gen_chain.py` = 35 lines: the #219 seam-1 tape-ratio unit fix (`cg.measure_tokens` tier now READ rather than assumed, the `unit_word(cg)` label, and a NEW bite asserting both sides of the ratio came off one measurer). Substantive, correct, and exactly the kind of change a mirror exists to carry.

### The mechanism question — the brief's actual instruction — answered

The brief said: *"Find the package's own sync mechanism … and sync THROUGH it, never by hand-copy unless that IS the mechanism."*

**I searched for it and it does not exist.** Probes run, all named so the absence is falsifiable:

- `grep -rln "sync" memento-package/ --include=*.py --include=*.md --include=*.sh` → **no matches.**
- `ls knowledge/*.sh scripts/ tools/ bin/` → one shell script in the repo, `knowledge/_git_commit.sh`; nothing package-facing.
- `grep -rn "COPY_A\|memento-package" knowledge/_build_all.py` → the package appears ONLY as two gate invocations (`_PKGDELTA`, lines 485/487/800/801). The build **audits** the package; it never **writes** it.
- `memento-package/machinery/_MACHINERY-MANIFEST.md` — a table of copies with source commits and the annotation `RE-SYNCED #193`. A record of syncs, not a means of one.
- `knowledge/_RUNBOOK-*.md` + `notes/_MEMENTO-DECISIONS.md` — no remedy path for arm 1. (Arm 2 names its own remedy in the failure string — *"re-review and re-port, or update the docstring"*. Arm 1 names only the boundary ruling.)
- `_memento_search.py "memento-package verbatim set re-sync authorization" --all` → nothing beyond what is quoted below.

**The mechanism is a Dave authorization.** And the record carries TWO rulings on it that do not agree, which is precisely why I stopped.

`s114-D7` (#114, 2026-08-06, by Dave):
> "The memento-package stays a LIVE tracking mirror, not a frozen release. Verbatim: 'lets keep it live and do the fix... versioning in the git only. lets call it and experiment.' Re-sync ENACTED; delta-audit clean PASS."

`s193-D1` clause (b) (#193, 2026-08-17, by Dave):
> "the memento-package VERBATIM SET re-sync is authorized ONCE for #193 (his #64 release boundary) — explicitly NOT a standing rule."

And the #193 dossier, `_DECISION-HISTORY/2026-08-17-193-rock-solid-and-the-first-full-chained-build.md:48-50`, in its own words:
> "`s193-D1`(b) is the narrower half and the one most likely to be misread later: the memento-package VERBATIM SET re-sync was **authorized once, for #193**, on Dave's explicit yes, against his own #64 release boundary. It is **not** a standing rule and must never be quoted as one."

A sub syncing the mirror today would be doing exactly the thing the later ruling says must never be quoted as licence. A sub deciding *which* of two Dave rulings governs would be ruling. **Both are outside my DO-NOT-RULE list.** So: not synced, returned.

I also considered and rejected the two obvious dodges, so the conductor does not have to re-derive them. Narrowing the gate's VERBATIM_SET, or adding a "mirror may lag" tolerance, would be **a threshold** — DO-NOT-RULE names thresholds explicitly. Marking the red COULD-NOT-ASK would be the #173 defect run backwards: hiding a true, environment-independent red behind a refusal.

### The `_capture_gate.py` mirror question — CLOSED GREEN, with evidence

The brief asked whether lane 2's `_capture_gate.py` edit needs a package mirror. **It does not, and arm 2 is correctly green rather than accidentally green.**

The package's `_capture_gate.py` is **not a copy** — it is a purpose-written shim, exempt by design from wholesale comparison. Arm 2 instead AST-hashes, by name, the 12 declared ported symbols against their port commits. Probe:

```
git diff d178313~1 d178313 -- knowledge/_capture_gate.py | grep -E "(chain_parts|read_chain_tk|measure_tokens|measurement_degraded|dofirst_index|_heal_tiktoken|BYTES_PER_TOKEN|DOFIRST_ITEM_RE|DOFIRST_HOOK_MAX|DOFIRST_INDEX_TK_MAX|LS_DELTA_RE|_TIKTOKEN_HEAL_TRIED)"
→ (empty)
```

Lane 2's 46 lines landed in `BOOT_SIGNED_RE` (hunk `@@ -3682,8 +3682,22 @@`) and `selftest_boot_delta_parse` (hunk `@@ -7422,6 +7436,36 @@`). **Neither is a ported symbol.** The shim's declared provenance is intact; no re-port is owed; the gate is green for the right reason. This half of item A needs nothing from Dave.

### UNPROVEN, declared

Once the mirror IS re-synced (whenever that is ruled), `_gen_chain.py`'s new dependency surface inside the package is unexercised by me — the package copy imports `cg.measure_tokens` and now unpacks a **two-tuple** where the shim must supply one. I did not drive the package's `_gen_chain.py` against the package's own shim. **If the shim's `measure_tokens` returns a bare int rather than `(tk, tier)`, the re-synced copy breaks at runtime and no arm of this gate would see it** — the gate compares bytes and provenance, never behaviour. This is a real, named, priced follow-on for whoever enacts the sync, not a blocker for the ruling.

---

## B — CI red [18]: `_gm_usage.py --selftest`

### The failing assertion, verbatim

```
[_gm_usage selftest] FAIL:
  ✗ real-repo usage history reads clean (got: ['session #218 testifies DIFFERENTLY in GOOD-MORNING.md and GOOD-MORNING.md — one of them is false and this reader cannot tell which. REFUSED.'])
  ✗ real-repo report closes in exactly ONE of its two legal states, never a remedy choice
```

Reproduced locally at base, first try. **Deterministic. Not the #173 class** — nothing here is tier-, key-, network- or tiktoken-dependent; it reads two lines of committed markdown and compares them.

### The cause, at cause

`knowledge/_gm_usage.py:486` raises the refusal when the same session number carries two *differing* testimonies. `HISTORY_SOURCES` (`:414`) is `(notes/_GAUGE-LOG.md, GOOD-MORNING.md)`. Both testimonies here come from **the same file**, which is why the message names `GOOD-MORNING.md` twice — that is not a display bug, it is the literal truth.

`GOOD-MORNING.md`, the two lines:

```
499: > **section-usage #218 (self-report, delegated OPUS wrap sub):** GM HDR:C LATEST:C PRIOR:R DOFIRST:U A:U C1:R C2:U C4:U STRATA:C · LS HDR:C LANES:R SPIN:U ...
517: > **section-usage #218 (second wrap; self-report, delegated OPUS wrap sub):** GM HDR:C LATEST:C PRIOR:U DOFIRST:U A:U C1:U C2:U C4:U STRATA:C · LS HDR:C LANES:U SPIN:U ...
```

They differ on `PRIOR` (R vs U), `C1` (R vs U) and `LANES` (R vs U).

Provenance, so nobody re-derives it:

```
git blame -L 499,499 → 61302a3  Claude 2026-08-24
git blame -L 517,517 → a339fed  Claude 2026-08-25   (#218 wrap commit)
```

**#218 wrapped twice**, each delegated wrap sub honestly self-reported its own section usage, and both reports are true *about their own wrap*. The reader's data model keys testimony by session NUMBER alone and therefore reads two true statements as one contradiction. It refuses — **correctly, by its own contract**. The red is the instrument working.

### Why I did not fix it

Every available fix is a ruling:

- **Collapse / keep-last / keep-first** — picks which wrap's testimony is the session's, i.e. decides what a "session" measures.
- **Give the record a distinct id** (`#218b`, or a wrap ordinal) — changes the record's grammar, and `GOOD-MORNING.md` is on my DO-NOT-TOUCH list, so I cannot even stage the data half.
- **Sum or merge the two** — invents a measurement nobody made.

So: diagnosed, quoted, returned. No patch. Nothing in the artefact touched.

### One non-ruling improvement, priced but NOT taken

When both testimonies come from the same source, the refusal reads *"in GOOD-MORNING.md and GOOD-MORNING.md"* and gives no line numbers — so a reader who trusts the message alone cannot find either line. Carrying `(line N)` on each side would be a pure diagnostic improvement with no semantic content. I left it: it does not move the red, and touching the refusal string while the refusal itself is the open question invites a later reader to think the red was addressed. **Queued, not done.**

---

## C — the `[hidden]`-vs-author-display class check — BUILT, and it found live defects

`knowledge/_validate_hidden_display.py`, **NEW**, ADVISORY, non-gating, writes nothing anywhere.

### The class, restated from the record

The UA sheet's `[hidden]{display:none}` sits at specificity (0,1,0). Any author `display:` rule that matches the same element and is not beaten on specificity/order **wins**, and the element paints while `hidden` tells assistive technology it is gone. `s218-D5` clause 3, Dave's, verbatim:

> "The palette hidden-option defect (author display beats [hidden]; a phantom option painted and sat in the a11y tree of an empty listbox) is fixed at cause with the one-line CSS rule in the snippet's own style block, landed now; the repo-wide [hidden]-vs-author-display check joins the gates backlog as a class candidate."

One instance was fixed. **The class was never swept.** This is the sweep.

### Shape

Three certainty tiers, kept apart on purpose:

- **STATIC / DYNAMIC** — CERTAIN. The painting selector states no ancestor or sibling condition, so if the element exists the collision is real. `DYNAMIC` = the attribute arrives from the snippet's own script, target resolved from its `querySelector` / `getElementById` / `querySelectorAll` binding (with `forEach` iteration variables inheriting their list's binding).
- **STATIC? / DYNAMIC?** — POSSIBLE. The painter carries a combinator; this reader does not verify ancestors, so the pair may never meet in the real DOM. Reported *with the reason attached to every line*, never sold as certain.
- **UNRESOLVED** — the script writes `hidden` to a receiver this reader cannot resolve to a selector. **Declared and counted**, with the source line quoted, because an unresolvable target is a gap in the instrument's reach and not a clean bill.

Comment discipline throughout: HTML comments via the shared `_htmlmask.mask_comments` (item D's helper — its first new consumer), CSS `/* */` and JS `//` masked length- and line-preservingly. All three views keep the file's own line structure, so **every line number printed addresses the file**.

### Selftest — 16 bites, all green, and it bites in BOTH directions

```
✓ STATIC defect is CAUGHT and names the class, the painting rule and the missing remedy
✓ the RULED remedy `.x[hidden]{display:none}` clears the finding (no false positive on the s218-D5 fix shape)
✓ a LOWER-specificity [hidden] remedy is still caught, and the message quotes both specificities
✓ a painting rule inside a CSS comment is NOT counted (comment-masked)
✓ a hidden-bearing element inside an HTML comment is NOT counted (shared _htmlmask)
✓ a script-set `hidden` on a querySelector-bound element is RESOLVED and caught
✓ the forEach iteration variable inherits its list's binding (querySelectorAll)
✓ an unresolvable script target is DECLARED as UNCHECKED, not silently dropped
✓ a painter whose own selector carries [hidden] is read as a deliberate override, not the defect
✓ REAL #218 case: Command-palette carries NO CERTAIN finding with the ruled fix in place
✓ REAL #218 case MUTANT: delete the ruled one-line remedy and the ORIGINAL phantom option is named again
✓ REAL #218 case MUTANT is CERTAIN-tier, not a hedged POSSIBLE
✓ line numbers are FILE-relative, not block-relative (painter line 6, element line 10)
✓ a `hidden` write inside a JS comment is NOT counted (prose about the defect is not the defect)
✓ an ANCESTOR-conditioned painter lands in the POSSIBLE tier and says why
✓ when BOTH a certain and a possible painter match, the element reports the CERTAIN one
✅ _validate_hidden_display selftest: all bites pass
```

**The mutant-red-by-name arm is driven on the REAL historical instance, not a fixture** [[mutation-tests-the-clause-not-the-feature]]. Delete Dave's ruled one-liner from the live `Command-palette.reference.html` and the check re-names the original #218 defect, by file, class, element line and painting rule:

```
Command-palette.reference.html: STATIC hidden-bearing <div> (class=cp-opt) at line 230 is painted by
`.cp-opt{display:flex}` (line 92, specificity (0, 1, 0)); the file has NO matching `[hidden]{display:none}`
remedy — the UA `[hidden]{display:none}` is (0,1,0) and loses, so the element renders while `hidden`
tells AT it is gone (#218 W3 F1 class, s218-D5 clause 3)
```

Line 230 **is** `#cp2-o1`, the phantom option Dave saw. With the remedy in place, clean. The check goes green on Dave's own fix and red on its removal — the clause is proven, not the feature.

### Two defects found in the checker itself, and fixed before the run

Recorded because a first-draft instrument that ships its own defects is the #193 finding-3 class:

1. **Combinator blindness sold as certainty.** The first draft reported `.cp-stage-mock span{display:block}` against `#cp1-title` as a flat finding — a false positive, since `cp1-title` has no `.cp-stage-mock` ancestor. It would have made the check's real-file control fail against a *correct* file. Remedied by the CERTAIN/POSSIBLE tier split, which is now itself bite-tested in both directions.
2. **Line numbers named the wrong frame.** Painters were reported at style-block-relative lines (`.dv-empty-frame` at "line 170" when it is on line 220) — the ds-021 defect, in a gate whose own output is meant to be actionable [[measure-dont-convert-units]]. Both the block-isolation and the selector-start offset were wrong; both fixed, and the fix is asserted by a bite rather than assumed.

### CORPUS RUN — the findings

```
135 snippet(s) scanned, 17 with signals · 3 STATIC · 0 DYNAMIC · 3 STATIC? · 6 DYNAMIC? · 13 UNRESOLVED
```

**REPAIRED NOTHING.** Triage input, as briefed.

#### ⛔ THREE CERTAIN findings — the same defect, the same class name, three files

```
Chart-butterfly-h.reference.html: <div class="dv-empty-frame"> hidden at line 317, painted by `.dv-empty-frame{display:flex}` (line 220), NO [hidden] remedy in the file
Chart-butterfly-v.reference.html: <div class="dv-empty-frame"> hidden at line 320, painted by `.dv-empty-frame{display:flex}` (line 224), NO [hidden] remedy in the file
Chart-histogram.reference.html:  <div class="dv-empty-frame"> hidden at line 271, painted by `.dv-empty-frame{display:flex}` (line 182), NO [hidden] remedy in the file
```

Verified by hand on `Chart-butterfly-h.reference.html` rather than trusted from the tool — `grep -c "\[hidden\]"` returns **0** for the file, the rule at line 220 reads `.dv-empty-frame{width:580px; height:260px; display:flex; ...}`, and the markup at 317 is `<div class="dv-empty-frame" hidden>`. **This is the #218 defect, live, unfixed, in three chart specimens.** The consequence, if it renders as the bytes say: the "No data for this period / Try a different date range or clear your filters" empty-state frame paints **on top of a chart that has data**, and sits in the a11y tree while claiming to be absent.

I have NOT confirmed this in a browser — that is the honest limit of a byte-reader. It is a **PRIORITY-1 triage item**, not a proven render.

⚠ **Ownership note for the conductor, before anyone repairs these:** these three are chart snippets, and the brief's shared-file rule is that generated regions belong to their generators. Whoever takes the repair must first establish whether `.dv-empty-frame` is authored in the snippet or projected into it — a hand-edit into a generated region would be reverted by the next regen and the fix would silently vanish [[gate-dont-patch]].

#### The POSSIBLE tier (9) and UNRESOLVED (13)

Nine `?`-tier signals across Command-palette (3), Data-grid, Navigations, Page-header-lockup (2), Template-create-edit, Template-wizard. Each names its ancestor condition; each needs one look to clear or confirm. Notably **all nine of these files already carry a `[hidden]{display:none}` remedy for their real targets** — the `?` hits are against unrelated painters, which is the expected shape of a combinator-blind reader and the reason the tier exists.

Thirteen UNRESOLVED across Avatar-group, Cascader (2), Command-palette, Secure-entry (2), Sidebar-nav, Standing-order-mandate-row, Stepper, Tabs, Template-auth (2), Template-wizard. These are dominated by helper-scoped and destructured bindings (`p.pop.hidden`, `col.hidden`, `panel.hidden`) and by computed targets (`document.getElementById('p-' + (i + 1)).hidden`). Extending the resolver to reach them is a real, bounded piece of work — **priced, not smuggled in**, since the brief scoped this lane to building the check and running it.

---

## D — the `mask_comments` duplication (W-92) — ALREADY CLOSED, verified not assumed

**The brief's premise has aged.** [[premise-ages-faster-than-rule]] — I verified the premise before working to it, and it no longer holds. This was closed at **#218 seam 1, commit `adb5130`**, which is an ancestor of this lane's base `04655de`. There was nothing to extract and nothing to merge.

`git log --diff-filter=A -- knowledge/_htmlmask.py` → `adb5130 2026-08-24`.

### What is actually there — and it exceeds what the brief specified

| the brief asked for | what exists at base |
|---|---|
| ONE shared helper consumed by both | `knowledge/_htmlmask.py`; `gen_token_ramp.py:108` and `gen_component_partials.py:225` both `from _htmlmask import COMMENT_OPEN, COMMENT_CLOSE, mask_comments` |
| byte-equivalent behaviour proven | both generators' `--check` green (below) |
| a comparing selftest so a future fork is caught | **two** mechanisms, not one |

The second mechanism is the better one and the brief did not ask for it: `_htmlmask.selftest_mask()` holds the mask's own properties in one place and **both consumers run it** (`gen_token_ramp.py:196`, `gen_component_partials.py:572`, each prefixing failures `shared mask: …`), so neither generator can inherit a weaker test than the other. A helper whose tests live in only one caller is half-tested; this one is not.

### Byte-equivalence, measured at base

```
### gen_token_ramp --check
gen_token_ramp: 0 file(s) DRIFTED (0 with block, 0 block-removed), 147 already in sync.   exit=0
### gen_component_partials --check
gen_component_partials --check OK — all AUTO-PARTIAL blocks in sync, contracts hold.       exit=0
```

Both generators' outputs are in sync with the committed artefacts across 147 files. **No divergence anywhere — nothing to report as a merge-stopper.**

### The fork-detector, DRIVEN not read

A green assertion nobody has made fail is an assertion [[instrument-without-a-consumer]]. So I drove it. In a throwaway copy of the three files (`/tmp`, discarded), I re-introduced the exact regression — a local `def mask_comments` shadowing the import — and ran `gen_token_ramp.py --selftest`:

```
gen_token_ramp selftest: FAIL
   ❌ mask_comments came from `__main__`, not `_htmlmask` — a second copy of the comment mask is back,
      and no gate compares copies (W-92). Import it, never re-implement it.
```

**Red, by name, citing W-92.** The guard works. **Item D needs nothing.**

*(Sandbox note for the next lane: `/var/tmp` hit ENOSPC on a `cp -r knowledge/` — the disk is at 81%, 1.9G free, and `knowledge/assets/` is large. Copy the three files you need, not the tree.)*

---

## RULING-SHAPED QUESTIONS — Dave's, not mine

### Q1 (A) — How does the memento-package mirror stay in sync from now on?

Two of Dave's own rulings point opposite ways and the CI red sits between them. **Nothing about this is a technical question** — the sync itself is a two-file byte copy that takes seconds.

- `s114-D7` (#114): the package "stays a **LIVE tracking mirror**, not a frozen release… 'lets keep it live and do the fix'."
- `s193-D1`(b) (#193, later): the VERBATIM SET re-sync "is authorized **ONCE** for #193… explicitly **NOT** a standing rule", and the dossier adds it "must never be quoted as one."

The shapes available, offered as an option set rather than a recommendation, since which one is right depends on what Dave wants the package to BE:

**(a) Standing licence.** A verbatim-set re-sync is routine maintenance any lane may perform whenever the gate reds, no authorization needed. Reads `s114-D7` as governing and `s193-D1`(b) as a note about #193's particular circumstances. *Consequence: this red never recurs; the release boundary becomes an audit trail rather than a gate.*

**(b) Per-instance, as now.** Every sync needs Dave's word. Reads `s193-D1`(b) as governing. *Consequence: honest, and the red recurs on every future `_gen_chain.py` edit — it is red today for the second time in six sessions. Each recurrence costs a lane's diagnosis to re-derive what this report just derived.*

**(c) Mechanised WITH an authorization gate.** Build the sync script that does not exist, and have it refuse unless the session carries an explicit authorization token. *Consequence: makes the boundary enforceable rather than remembered, but it is new machinery, and per s172-D3(e) it needs Dave's yes before anyone builds it.*

**Immediately actionable regardless of which he picks:** the two rulings' tension should be recorded so the next lane does not re-derive it. That is an inscription, and inscriptions are Dave's.

### Q2 (B) — How does a session that wrapped TWICE testify?

`#218` produced two honest self-reports under one session number. `_gm_usage.py` reads them as a contradiction and refuses. The refusal is correct; the **record's grammar** has no way to say "same session, second wrap." Shapes: collapse to one (which?) · give wraps an ordinal (`#218.1`/`#218.2`) so both stand and the reader gains a wrap axis · or rule that the second wrap SUPERSEDES and the record should carry only one line. **This is a record-grammar decision and it touches `GOOD-MORNING.md`, which no lane may edit.** Note the standing hook already in memory — *"a skipped wrap certifies the WRONG session"* — this is its mirror image: a doubled wrap testifies twice.

### Q3 (C) — Do the three `dv-empty-frame` findings get repaired, and does this check get promoted?

Two separable decisions:

**(i) The repair.** Three chart snippets carry the #218 defect, unfixed. The remedy is the one-line rule Dave already ruled at `s218-D5` clause 3, applied to a different class name. Whether it lands as a matching one-liner per file, or whether `dv-empty-frame` should stop declaring `display:flex` at rest, is a design call — and per the ownership note above, whether the region is generated must be established first.

**(ii) The promotion.** This check enters ADVISORY, which is where a new check belongs. It is bite-tested in both directions, mutation-proven on the real historical instance, and it has now found real defects on its first corpus run. **Promotion to blocking is explicitly NOT proposed here** — DO-NOT-RULE names promotions of advisory gates, and it should survive real use first (ADR-0005 §5). Recorded so the conductor knows it is a live candidate, not so it moves.

---

## Pitfalls replayed (Dave #165)

- **A is not a lane failure and must not be re-briefed as one.** A future lane handed "sync the package" will hit the same wall and burn the same diagnosis. The blocker is a ruling, and the diagnosis is in this file.
- **B's red will still be red after any lane that does not touch `GOOD-MORNING.md`** — which is every lane, correctly. Do not let its persistence read as "lane 6 failed to fix it."
- **C's `?` and UNRESOLVED tiers are not defects.** Anyone reading the corpus output as a 25-item repair list will file 22 non-issues. The CERTAIN count is 3.
- **D's brief premise was stale.** Worth a look at whether other gates-backlog items were priced against a repo state that has since moved [[premise-ages-faster-than-rule]].
- **The new gate is NOT wired into `_build_all.py`.** Deliberate: wiring a gate into the build is a build-surface change and the brief scoped this lane to building and running it. It runs standalone today; **nothing calls it** — an instrument with no consumer is its own defect class [[instrument-without-a-consumer]], so this must not sit unwired indefinitely.

  ⚠ **There is a precedent from this very crank, and the conductor should apply it consistently.** Lane 5 built `knowledge/_gate_minted_consumption.py` — also new, also ADVISORY, also a "nothing was watching this" class check — and **wired it into `_build_all.py` at the `ADVISORY` tier** (`_build_all.py:409` and `:795`). Its own inline comment states the same posture mine takes: *"ADVISORY ON PURPOSE and it must stay so… Promotion needs a `$consumer`/`$reserved` declaration on the token, and is DAVE'S WORD, not a builder's pick."* Two near-identical instruments landing in one crank, one wired and one not, is an inconsistency a later session will read as a judgment about the unwired one. **Recommendation (not a ruling): wire this gate at the same ADVISORY tier, in the same motion the conductor reconciles lane 5's.**

## Files touched — and what is NOT mine

**Mine, and only these:**

| path | change |
|---|---|
| `knowledge/_validate_hidden_display.py` | **NEW** — the advisory sweep, ~330 lines, all instrument |
| `notes/_subreports/2026-08-25-219-lane6-gates-backlog.md` | **NEW** — this report |
| `knowledge/_state.json` | +26 lines — two existence rows, `W-178` (the gate) and `W-179` (this report). `_state.check()` green after both. No existing row read, reworded or closed. |

**⛔ Present in the working tree at my exit and NOT mine — do not attribute these to lane 6:**

| path | whose |
|---|---|
| `knowledge/_gate_minted_consumption.py` (untracked) | **lane 5** — its own inline provenance says "built #219 lane 5" |
| `knowledge/_build_all.py` (modified, +16) | **lane 5** — wires the above at the ADVISORY tier |
| `knowledge/_graph-mark-observations.jsonl` (modified, +50) | **shared side effect** — append-only retrieval observation log; 47 of the 50 appended lines are dated 2026-08-25 across several lanes. One `_memento_search.py --all` call of mine (the Q1 authorization search) contributed some. Nothing was edited; the file only grows. |

No commit — the conductor reconciles every path, no blind `git add -A`.

**DO-NOT-RULE / DO-NOT-TOUCH verified clean at exit**, by probe not by claim: `git status --porcelain -- knowledge/_rulings.json GOOD-MORNING.md _CHAIN.md _LIVE-STATE.md` returns **empty**. No constant, band, advisory, threshold or stop line moved; no Dave row touched; no gate promoted; no memory write.
