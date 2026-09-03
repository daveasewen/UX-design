# `#241`-`D` — the ritual diet: what the process layer costs, what consumes it, and what to cut

session: `#241` · 2026-09-02
window: lane D (conductor window #241)
sub index: `D`
brief: chat brief from the #241 conductor (no `notes/_briefs/` file was minted for this lane —
DECLARED GAP, not an omission I can repair from here)
tokens: `UNMEASURED — no message.usage at a sub's own seat; UNOBSERVABLE and DECLARED, never estimated`

---

## EXEC SUMMARY — for Dave, plain prose

You are right, and there is a number on it. The single most expensive thing the process layer does
is print the whole wrap gate — 7,534 tokens of it — every single time a session runs its check-in,
and it ran 22 times yesterday. Nobody reads those 130 lines; the only fact anyone takes from them
is "0 fails, 13 warns", which is 52 tokens. That one change saves more than everything else on this
list combined.

Second: your read chain carries a list of 461 bare item numbers with no words attached (2,615
tokens, every session, forever). No gate reads it. The four counts above it carry all the meaning.

Third: the morning banner and the "latest delta" say the same things twice, in defensive prose, at
5,099 tokens a session to read and roughly the same again to write.

The recommended package cuts about 27,000–42,000 tokens per session and touches nothing you
decided. Your rulings store, the fuel gauge, the recall probe and the open-item presence index all
stay — those four are the ones that protect something real, and they are cheap.

One thing a diet cannot get back: the gauge exists because sessions genuinely blew the window
(#230 crossed 256,000 at your conductor's own seat), and the rulings store is the only reason your
decisions survive a closed chat. Neither is on the cut list.

COUNTS: findings `11` · ruling-shaped `4` · UNPROVEN `4`

COUNTS: components inventoried `33` · measured `24` · estimated `6` · DELETE `4` · SHRINK `7` ·
KEEP `19` · UNPROVEN `3`

---

## What was done

A read-only inventory and measurement pass over the opener, per-lane and wrap ritual layers.
No repo file was edited except this report. `git status --porcelain | md5sum` was captured before
and after every instrument run and is **unchanged** (`347420beedfa6ff13b3f788b0583ab80`, 4 dirty
paths, both times) — including the wrap-gate run below, which was executed with
`_rehearsal_log_append` stubbed to a no-op so it could not append to `notes/_REHEARSAL-LOG.jsonl`.

`pip install tiktoken --break-system-packages` → already satisfied. Every ESTIMATE below is
tiktoken `cl100k_base` over the exact file or the exact captured stdout, and is labelled.
Every `real` figure is quoted from an instrument that produced it, never converted
[[measure-dont-convert-units]].

`_build_all.py` was NOT run. Nothing was committed. Nothing was ruled.

---

## PART 1 — THE INVENTORY, WITH ITS PRICE

### 1a. OPENER — what a session must read or run before it works

| # | Component | Cost | How |
|---|---|---|---|
| 1 | `_CHAIN.md` read, whole | **11,319 tk** | MEASURED |
| 2 | └ chain header / preamble (43 ln) | **3,062 tk** | MEASURED |
| 3 | └ § ★ LATEST banner (16 ln) | **3,353 tk** | MEASURED |
| 4 | └ § ⬛ OPEN WORKLIST presence index (6 ln, 28 items) | **418 tk** | MEASURED |
| 5 | └ § ⏱ LATEST DELTA (15 ln) | **1,746 tk** | MEASURED |
| 6 | └ § ⬛ OPEN WORK, 461 bare ids (15 ln) | **2,615 tk** | MEASURED |
| 7 | └ footer (5 ln) | **125 tk** | MEASURED |
| 8 | Title read-back in chat | ~40 tk | ESTIMATE (one line, cl100k) |
| 9 | `_checkin.py` core block (HOW HOT / DISK / FILL / SEAM / DREAM / 119) | **1,295 tk** | MEASURED |
| 10 | `_checkin.py` REHEARSAL — the whole wrap gate, printed | **7,534 tk** | MEASURED |
| 11 | `_checkin.py` B3 GRADE alerts | **68 tk** | MEASURED (by its own instrument) |
| 12 | `_recall_probe.py --plant` + its store file | **503 tk** on disk; ~80 tk printed | MEASURED / ESTIMATE |
| 13 | `MEMORY.md` (Cowork auto-memory, NON-REPO) | **3,509 tk** | MEASURED |
| 14 | Boot first turn (harness + roster + memory + tools) | **75,206 – 76,915 real**, n=7 | MEASURED, quoted from `notes/_GAUGE-LOG.md` |

**Commands.**

```
python3 -c "import tiktoken; enc=tiktoken.get_encoding('cl100k_base'); \
  print(len(enc.encode(open('_CHAIN.md',encoding='utf-8').read())))"
→ 11319
```

The region split was cut on the section headings of the same file (`^> ## ★ LATEST`,
`⬛ OPEN WORKLIST`, `^## ⏱ LATEST DELTA`, `^## ⬛ OPEN WORK`, `^\*\(Chain ends`) and the six
regions sum to 11,319 exactly — the split is a partition, not a sample.

```
python3 knowledge/_checkin.py --no-rehearse --no-grades   →  50 lines, 4,227 chars, 1,295 tk
```

```
# wrap gate, run WITHOUT writing (log-append stubbed, report=None):
python3 - <<'EOF'
import sys,io,contextlib; sys.path.insert(0,'knowledge')
import _capture_gate as cg
cg._rehearsal_log_append = lambda repo,entry: None
buf=io.StringIO()
with contextlib.redirect_stdout(buf): rc=cg.run(mode="wrap", report=None)
EOF
→ rc 0 | 130 lines | 23,077 chars | 7,534 tk
```

```
python3 knowledge/_recall_probe.py --status --session 241
→ PROBE:  planted 2026-09-02T20:55:51Z, n=4 — NO CHECK RECORDED yet.
```

```
wc -c /sessions/…/mnt/.auto-memory/MEMORY.md  → 12454
tiktoken cl100k over the same file            → 3,509 tk   (was 6,104 pre-#240 compaction)
```

Boot staircase, quoted from `notes/_GAUGE-LOG.md` post-mortems #234–#240 (`grep -n
"post-mortem #2[34]" notes/_GAUGE-LOG.md`): **75,206 · 75,294 · 75,198 · 76,915 · 75,336 ·
75,619 · 76,138 real**. Every one read first-hand with `knowledge/_checkin.py` at its own wrap
seat; all seven are outside the `s208-D1` band 55,595–57,903, which is what `s240-D1` already
retires in principle.

⛔ **#241's own conductor boot is NOT in this report.** My seat's check-in read **69,092 real**
first-turn — that is a *subagent* boot, a different object, and summing or comparing it to the
conductor's would be exactly the defect [[measure-dont-convert-units]] names. The first
post-diet conductor boot is `s240-D2`'s ceiling input and it is the conductor's to read.

### 1b. HOW OFTEN the opener instruments actually fire

This is the multiplier that turns a 7,534 tk print into the biggest line item in the ritual.

```
python3 -c "…collections.Counter over notes/_REHEARSAL-LOG.jsonl by (date, kind)…"
2026-08-31 {'rehearse': 15, 'wrap-open': 121}
2026-09-01 {'rehearse': 11, 'wrap-open': 35}
2026-09-02 {'rehearse': 22, 'wrap-open': 59}
```

```
python3 -c "…Counter over notes/_dream/_GRADE-DECISIONS.jsonl by date…"
2026-09-01  11 check-ins that printed grades
2026-09-02  22 check-ins that printed grades
```

2026-09-02 held roughly eight windows (#234…#241), 2026-09-01 roughly two (#232–#233).
⇒ **3–6 check-ins per session**, each currently printing 7,534 tk of gate output it did not need.

### 1c. PER-LANE — the conductor's cost of delegating

| # | Component | Cost | How |
|---|---|---|---|
| 15 | Lane brief (`COMMON-lane-rules` + per-lane) | **453 tk** + **961–2,093 tk** | MEASURED |
| 16 | Lane launch → return, conductor FILL, all-in | **≈19,000 real per lane** (n=5) | MEASURED at #238 |
| 17 | Filed sub-report `s218-D7`, written in the sub's window | **mean 7,083 tk** (18 files, 2026-09-02; 127,502 tk total) | MEASURED |
| 18 | `s203-D1` CI read-back route | **≈55,692 real** for one verdict | MEASURED at #239 |

The ~19K figure is **not mine and is not derived** — it is homed at
`knowledge/_RUNBOOK-context-gauge.md` lines 381–411, § *MEASURED, NOT RULED — A LANE IS PRICED AT
ITS RETURN, NOT ITS LAUNCH*, quoting `notes/_GAUGE-LOG.md` § `#### 2026-09-02 #238`: *six lanes
went out from an opener FILL of 103,211; the five reconciled in-window put the conductor at
198,667 real*. The same section carries #239's ≈55,692 read-back price and #240's decision not to
launch at all.

### 1d. WRAP — what closing a session costs

The ritual is fourteen steps (`knowledge/_RUNBOOK-capture-ritual.md` line 34: *1, 1b, 2, 2c, 2d,
2e, 2f, 2g, 3, 4, 4b, 4c, 5, 5b*).

| # | Component | Cost | How |
|---|---|---|---|
| 19 | The 14-step sequence itself (prose to follow) | runbook **16,967 tk** on disk | MEASURED |
| 20 | `_capture_gate.py --wrap` stdout | **7,534 tk**, rc 0, 13 warns | MEASURED |
| 21 | ★ LATEST banner, WRITE | **3,353 tk** | MEASURED |
| 22 | ⏱ LATEST delta, WRITE | **1,746 tk** | MEASURED |
| 23 | 2f stratum → `notes/_GAUGE-LOG.md` | **4,179 tk** for the #239 block (last 20 ln) | MEASURED |
| 24 | └ of which the `post-mortem #N` line alone | #238 **465 tk** · #239 **445 tk** | MEASURED |
| 25 | 1b dossier → `_DECISION-HISTORY/` | **2,457–3,913 tk** (last 5, mean 3,078) | MEASURED |
| 26 | Filed wrap sub-report | **3,765 tk** (`2026-09-02-240-wrap.md`, 178 ln) | MEASURED |
| 27 | `_CARRIES.md` § `residual → #241` — ONE LINE | **72,013 tk · 202 items** | MEASURED |
| 28 | 2c/2d rolls → `_GM-ARCHIVE.md` / `_LIVE-STATE-ARCHIVE.md` | 15 ln + 13 ln at #240 | quoted from the banner |
| 29 | 2g `_memento-index.json` rebuild | not priced | UNPROVEN |
| 30 | `_rulings.json` inscription | store now **332** entries | MEASURED |
| 31 | `_state.json` W- row minting | store now **461** rows | MEASURED |

**The gate's own shape.** `_capture_gate.py` is 9,026 lines / 148,870 tk and must never be read.
Grepping it instead: 127 `def`, 70 `fails.append`, and `wrap_checks()` (line 4917) calls **25
named checks**, tiered by **12 module-level constants**:

```
grep -n "^[A-Z_]*BLOCKING\s*=" knowledge/_capture_gate.py
SECTION_USAGE_BLOCKING = True     CONSULT_RECEIPT_BLOCKING = False
BOOT_DRIFT_BLOCKING    = True     USAGE_HISTORY_BLOCKING   = False
SUBS_LINE_BLOCKING     = True     REGEN_SERIAL_BLOCKING    = False
UNKEYED_BLOCKING       = True     SHARED_HELPER_BLOCKING   = False
ROLL_CLAIM_BLOCKING    = True     SUBREPORT_CITE_BLOCKING  = False
STALE_TOP_BLOCKING     = True
CARRY_GATE_BLOCKING    = True
```

⇒ **8 blocking, 4 advisory-at-birth.** The named check functions are: `plan_block_check` ·
`instrument_stray_check` · `governing_records_join_check` · `regen_serial_check` ·
`shared_helper_dedup_check` · `subreport_citation_check` · `check_preflight` · `check_budgets` ·
`retirement_receipts` · `section_usage_probe` · `usage_history_probe` · `consult_receipt_probe` ·
`index_freshness_check` · `boot_constant_drift_check` · `lane_routing_check` ·
`dofirst_index_present_check` · `gauge_log_continuity` · `gauge_log_subs_line` ·
`stop_line_consistency` · `unkeyed_testimony` · `roll_claim_check` · `stale_top_item_check` ·
`carry_wording_check` · `title_generation_check` · `check_file` (per-file, build mode).

**The write-only sinks.** These are never read at boot and never by a gate in whole; they are
where the ritual's output goes to rest:

```
_GM-ARCHIVE.md          3,195,554 B    962,034 tk
_CARRIES.md             2,900,547 B    862,158 tk
_LIVE-STATE-ARCHIVE.md  1,643,816 B    482,840 tk
notes/_GAUGE-LOG.md       985,386 B    292,371 tk   (156 post-mortem blocks)
notes/_MEMENTO-DECISIONS.md 557,040 B  153,924 tk
```

### 1e. STANDING / RETRIEVAL

| # | Component | State |
|---|---|---|
| 32 | `_measure_tokenizer.py` | **0 Python consumers**, flagged #77, re-probed #81, STILL zero — the gate warns about it every wrap |
| 33 | 119-sweep recheck (`knowledge/_119-sweep-recheck.json`, 1,316 tk) | **EXPIRED** — 15 sessions old; verdicts 20 UNPROVEABLE · 1 WEAK-MATCH |
| — | Dream pass proposals | newest `2026-08-30-proposals.md`, 8,396 tk, 87h old at my seat |

The Cowork auto-memory index is present and readable at
`/sessions/wizardly-gallant-wozniak/mnt/.auto-memory/MEMORY.md` — **12,454 B / 3,509 tk / 109
lines**, alongside **310 memory files totalling 1,210,415 B**. It is read-only from bash, exactly
as [[memory-md-is-in-the-mount]] says.

---

## PART 2 — CONSUMER TRACE

The project's own rule: an instrument without a consumer is a zombie. I ran the trace rather than
asserting it.

```
for t in _CHAIN.md _CARRIES.md _GAUGE-LOG.md _recall_probe "_probe/session" 119_sweep \
         _REVIEW-SIGNOFF _GRADE-DECISIONS _REHEARSAL-LOG _memento-index.json \
         _rulings.json _state.json ; do grep -rl "$t" knowledge/*.py .github ; done
```

| Component | Who reads it | When | What breaks if removed |
|---|---|---|---|
| `_CHAIN.md` | 13 scripts + `.github/workflows/gates.yml`; `_checkin.py` parses `CHAIN_STOP_RE` for the stop line | every opener, every check-in, CI | The stop line loses its source; the cold-start contract disappears. **KEEP** |
| chain § OPEN WORK, 461 ids | **NOTHING.** `dofirst_index_present_check` reads the *28-item DO-FIRST presence index*, a different block. `grep -n "OPEN WORK\|ids only\|DAVE'S (" knowledge/_capture_gate.py` returns one hit — line 1548, which *generates* the presence index | never | Nothing mechanical. **DELETE** |
| chain § presence index (28) | `dofirst_index_present_check`, BLOCKING at birth | every wrap | #60's defect returns: open items invisible to a cold session. **KEEP** |
| chain § ★ LATEST banner | `check_budgets`, `stale_top_item_check`, `carry_wording_check`, `_gm_move.py`, `roll_claim_check` | every wrap | The wrap's own record. **SHRINK, don't delete** |
| `_CARRIES.md` | `_capture_gate.py` (`_carry_items`, `carry_wording_check`) + `_build_memento_index.py` — **two** consumers, both process | every wrap | Carry drops go silent (11 genuine drops in 10 wraps, per `CARRY_GATE_BLOCKING`'s own note). **KEEP the gate, SHRINK the line** |
| `notes/_GAUGE-LOG.md` | `boot_constant_drift_check`, `gauge_log_continuity`, `gauge_log_subs_line`, `_roll_state.py`, `_gm_usage.py`, `gen_dashboard.py` | every wrap | The boot series `s240-D1` derives from. **KEEP, cap the prose** |
| `_checkin.py` REHEARSAL | a human reading 130 lines of stdout; the only durable artefact is a **52-token** JSONL record: `{"date":…,"fails":0,"heals_at_wrap":0,"kind":"rehearse","structural":0,"warns":13}` | 3–6× per session | Nothing — the record survives. **SHRINK to the record** |
| `knowledge/_probe/session-N.json` | **only `_recall_probe.py` itself** — no gate reads it | opener + past 150K | Blind-recall degradation goes undetected. Cost is ~503 tk. **KEEP** |
| `_rulings.json` | 12 scripts + CI | continuously, by retrieval | Dave's decisions stop surviving the chat. **KEEP, untouchable** |
| `_measure_tokenizer.py` | **0 consumers**, twice re-probed | never | Nothing. It costs a warn line at every wrap. **DELETE** |
| 119-sweep | `_checkin.py` prints its expiry nag | 3–6× per session | Nothing actionable — its live verdicts are 20 UNPROVEABLE + 1 WEAK-MATCH. **DELETE the nag** |
| B3 grade alerts | `_checkin.py`; every print logs a measured row to `_GRADE-DECISIONS.jsonl` (256 alert rows: min 41 · mean 97 · max 185 tk) | every check-in | The s179-D1 evidence series. It costs 68 tk. **KEEP** |
| Filed sub-reports | `_gate_doc_rows.py --check` + `subreport_citation_check` (advisory) | every wrap | An unrowed report fails the gate. **KEEP the mechanism, SHRINK the size** |

---

## PART 3 — PRODUCT vs PROCESS, LAST FIVE SESSIONS

Counted off `notes/_subreports/` filenames — one file per lane, the sub index is in the name.

| Session | Lanes | Product | Process |
|---|---|---|---|
| #236 | 3 — `P-plan-build`, `R1-principles-survey`, `R2-sdlc-playbook` | 2 (designer's brain) | 1 (plan) |
| #237 | 2 — `G-gap-discharge`, `T-tensions-schema` | 1 (tensions schema) | 1 (gap discharge) |
| #238 | 6 — `A-plan-v2`, `B-L2-behaviour-address`, `C-licence-tiering`, `M-runbook-and-W355`, `P-polarity-gate`, `V-polarity-verifier` | 3 | 3 (plan, runbook, verifier) |
| #239 | 2 — `F-polarity-fix`, `R-assert-009-rebase` | 1 | 1 (assertion rebase) |
| #240 | **0 product lanes** + 1 wrap sub | 0 | 1 |
| **Total** | **14 lanes** | **7** | **7** |

**The finding that matters is not the 50/50 split.** It is what "product" now means. Every one of
those seven product lanes is *designer's-brain / polarity* work. **Charts, bento and themes have
had zero lanes since #232** (`2026-09-01-232-repair-and-recut.md`, `…-232-restage-v105.md`); the
last bento lane was #231's `bento-snippet`. Eight sessions.

And #240 is the shape Dave is reacting to: one whole morning, no product lane, three rulings about
the instrument, and the stated reason is arithmetic — FILL 135,020 @ 21 turns against a ~19K lane
price meant a lane did not fit.

---

## PART 4 — THE CUT PLAN

### DELETE — no consumer, or the only consumer is process itself

| Rank | Item | Costs now | Saves | What breaks | Whose call |
|---|---|---|---|---|---|
| **D1** | The rehearsal's 130-line gate dump inside `_checkin.py`. Print the record it already writes (`fails · warns · structural`) instead of `_cg.run(rehearse=True)`'s full stdout | **7,534 tk × 3–6 per session** = 22,602–45,204 tk | **≥22,400 tk/session** | Nothing. The 52-tk JSONL record is unchanged; print the fail *names* when `fails > 0` or when `warns` moves | **Mechanical** — one `print` site, `_checkin.py:1174-1181` |
| **D2** | Chain § ⬛ OPEN WORK, the 461 bare ids. Keep the four generated counts (461 · 376 live · 199 Dave's · 177 mine) | **2,615 tk every session** | **~2,555 tk/session** | Nothing. No gate reads it; `python3 knowledge/_state.py` has the bodies | **Mechanical** — `_gen_chain.py:479-483` |
| **D3** | The 119-sweep expiry nag in the check-in | ~120 tk × 3–6/session; currently EXPIRED and nagging | ~500 tk/session | Nothing — 20 UNPROVEABLE + 1 WEAK-MATCH is not an actionable verdict. Re-run it once and retire it, or retire it now | **Mechanical**, but retiring the *sweep* is Dave's |
| **D4** | `knowledge/_measure_tokenizer.py` | one WARN line in every wrap-gate run | ~100 tk/wrap + a zombie | Nothing. Zero consumers, twice re-probed (#77, #81). This is the project's own rule applied to itself | **Mechanical** |

### SHRINK — keep the function, cap the form

| Rank | Item | Costs now | Saves | What breaks | Whose call |
|---|---|---|---|---|---|
| **S1** | ★ LATEST banner: cap at **10 lines / ≤1,200 tk**. Make the ⏱ delta the sole home for gauge / declared-skips / not-done detail — today the two say the same things twice | **3,353 tk** read + 3,353 write | **~2,150 read + ~2,150 write** per session | Nothing mechanical; `check_budgets` already enforces caps, so the number is a constant edit | **Dave's** (the cap number); mechanical to enforce |
| **S2** | The wrap record as a **form, not prose**. Banner + delta + 2f stratum = **9,278 tk** per wrap, most of it defensive narration ("NOT CLAIMED", "read from the file, never from belief"). One line per field, values only | 9,278 tk/wrap | ~5,000 write + ~3,000 read | The prose is where premises get declared. A form must carry an explicit `DECLARED:` field or the honesty contract silently dies | **Dave's** |
| **S3** | `_CARRIES.md` § residual line: **202 items, 72,013 tk, one line**, wording frozen by a blocking gate, ageing forever, nothing closing | 72,013 tk to parse; grows every wrap | Age-cap at N ⇒ archive with an `s188-D2` receipt. ~30–50% at N=10 (ESTIMATE — I did not parse the age brackets) | The strike mechanism already exists and preserves wording verbatim, so nothing is dropped — but an age cap is a policy about *Dave's* open work | **Dave's** |
| **S4** | Filed sub-reports: **mean 7,083 tk**, 18 in one day (127,502 tk). Cap at the template's own skeleton: VERDICT + COUNTS + findings + ruling-shaped + REPLAY-THESE ≈ 2,500 tk | 7,083 tk of **QUOTA** per lane | ~4,500 tk **quota** per lane | Evidence must move to `assets/` rather than be deleted, or a receipt becomes a claim | **Mechanical** (template + `subreport_citation_check`) |
| **S5** | 2f stratum: **4,179 tk** per wrap into a 292,371-tk log. The `post-mortem #N` line alone (445–465 tk) is what the drift check parses | 4,179 tk/wrap | ~2,500 tk/wrap | `boot_constant_drift_check` needs the boot figure stated **once**. #240's own block already declares the double-count defect — a shorter block *fixes* that | **Mechanical** |
| **S6** | The `s203-D1` CI read-back route: **≈55,692 real** for one verdict | 55,692 real when it fires | ~45,000 real | The remedy is already homed (`_RUNBOOK-context-gauge.md` § MEASURED, NOT RULED): cap at the run page plus one JS grep. It is written down and not yet enforced | **Mechanical** |
| **S7** | Wrap-gate stdout itself: 130 lines, 13 warns that are the same 13 every run | 7,534 tk per `--wrap` (59 `wrap-open` runs logged on 2026-09-02) | ~5,000 tk/run once warns print as a delta | A warn that stops being printed stops being seen. Print new/changed warns in full, unchanged ones as a count + names | **Mechanical** |

### KEEP — each protects something Dave actually cares about

| Item | Cost | What it protects |
|---|---|---|
| `_CHAIN.md` as the whole contract | 11,319 tk | The cut itself: GM+LS retrieval surface is **93,447 tk**. The chain is already the biggest saving in the project |
| `_checkin.py` core block (FILL / boot / stop line / SEAM) | **1,295 tk** | The window. #230 crossed **256,000** at the conductor's seat; #232 crossed the 190,000 stop line by **41,518**. Cheap and load-bearing |
| ⏱ LATEST DELTA | 1,746 tk | The one place the previous session reaches the next. Keep this; shrink the banner that duplicates it |
| ⬛ OPEN WORKLIST presence index (28) + `dofirst_index_present_check` | **418 tk** | #60's defect — open items a cold session cannot learn exist. Cheapest item in the chain |
| `_recall_probe.py` | ~503 tk | Blind recall past 150K. FILL passed the 150,929 advisory in **six of the last seven sessions** |
| `_rulings.json` + `_inscribe_ruling.py` | 0 at boot (retrieval only); store now **332** | How Dave's decisions survive a closed chat. Untouchable |
| B3 grade alerts | **68 tk** | s179-D1's evidence series, and it measures its own cost |
| The 8 blocking gate checks with a named prior failure — `index_freshness_check` (cost 2 sessions), `carry_wording_check` (11 drops in 10 wraps), `stale_top_item_check` (false "owed" for 2 sessions), `title_generation_check`, `gauge_log_continuity` (3 skipped wraps), `boot_constant_drift_check`, `unkeyed_testimony`, `stop_line_consistency` | inside the 7,534 tk | Each has a named, dated failure it already caught. **Cut their OUTPUT (S7), never the checks** |
| `_gate_doc_rows.py` + filed-sub-report rowing | small | An unrowed report is an orphan document |
| 1b dossier (2,457–3,913 tk) | ~3,078 tk/wrap | Dave asked for this by name in 2026-07-19: *recording the why and how* |
| Step 3, the memory write | non-repo | Outside git, invisible to every gate — the only thing that survives a repo-less morning |

### ★ RECOMMENDED DEFAULT PACKAGE — one package, take it whole

**D1 + D2 + D3 + D4 + S1 + S5 + S7.** All seven are mechanical; not one of them touches a ruling,
a carry, or a decision.

- **D1** rehearsal prints its record, not the gate — **≥22,400 tk/session**
- **D2** the 461-id dump leaves the chain, its four counts stay — **2,555 tk/session**
- **D3 + D4** the 119-sweep nag and `_measure_tokenizer.py` retire — **~600 tk/session**
- **S1** banner capped at 10 lines / 1,200 tk — **~4,300 tk/session** (read + write)
- **S5** 2f stratum stated once, not twice — **~2,500 tk/wrap** (and it fixes #240's declared
  double-count defect as a side effect)
- **S7** wrap-gate warns print as a delta — **~5,000 tk per `--wrap` run**

**Sized: ~27,300 tk/session at the conservative floor (3 check-ins) and ~42,100 at 6.**
That is between one and a half and two-and-a-quarter lanes bought back per session, at the #238
price of ~19K per lane. **#240 declined to launch a lane because 19K did not fit. This package
buys back one to two.**

S2, S3, S4 and S6 are the second wave and three of them are Dave's word.

---

## Findings

1. **The rehearsal is the single most expensive process item in the project.** `_checkin.py`
   calls `_cg.run(rehearse=True)`, which prints the entire wrap gate — 130 lines, 7,534 tk —
   and the only durable output is a 52-token JSONL record. Probe: the redirect_stdout run above;
   `tail -1 notes/_REHEARSAL-LOG.jsonl` → `{"date": "2026-09-02", "fails": 0, "heals_at_wrap": 0,
   "kind": "rehearse", "structural": 0, "structural_names": [], "warns": 13}`.
2. **It fires 3–6 times a session.** 22 rehearsals on 2026-09-02 across ~8 windows; 11 on
   2026-09-01 across ~2. Plus **59 `wrap-open` gate runs** on 2026-09-02 alone.
3. **The chain carries 2,615 tk of bare item numbers that nothing reads.** `grep -n "OPEN WORK\|ids
   only\|DAVE'S (" knowledge/_capture_gate.py` → one hit, line 1548, which *generates* the
   28-item presence index. The 461-id block has no reader [[unmatched-grep-is-not-an-absence]] —
   the probe is named and the grep is quoted.
4. **The banner and the delta duplicate each other.** 3,353 tk and 1,746 tk, and both carry the
   same ⓪–⑦ / GAUGE / NOT DONE material. 5,099 tk of the chain's 11,319 is the same session
   record told twice.
5. **The carry line is 72,013 tokens on one line.** `_carry_items` over `_CARRIES.md` §
   `residual → #241` → **202** items. The chain's own claim of 202 is confirmed. It only grows;
   the gate freezes its wording; nothing closes.
6. **`_measure_tokenizer.py` has zero consumers and the gate says so at every wrap** — quoted
   verbatim from the run above: *"0 Python consumers, flagged by #77's periphery inventory,
   re-probed #81 and STILL zero."* The project diagnosed its own zombie and kept it.
7. **The 119-sweep is expired and nagging.** `_checkin.py` prints `⛔ EXPIRED — 15 sessions old
   (limit 15) … UNPROBEABLE 20 · WEAK-MATCH 1` on every check-in.
8. **Charts, bento and themes have had no lane since #232** — eight sessions. All seven "product"
   lanes in the last five sessions are designer's-brain / polarity.
9. **#240 launched zero product lanes**, and the stated reason is the ~19K lane price against
   FILL 135,020. The arithmetic was correct; the diet is what changes the arithmetic.
10. **The archives are 2.6 million tokens of write-only sink** (`_GM-ARCHIVE.md` 962,034 ·
    `_CARRIES.md` 862,158 · `_LIVE-STATE-ARCHIVE.md` 482,840 · `notes/_GAUGE-LOG.md` 292,371).
    Nothing at boot reads them; three gate checks read *slices* of the gauge log. This is not a
    cost per session — it is stated so nobody mistakes the roll ritual for a cost driver. **It
    isn't one. The banner and the rehearsal are.**
11. **The chain's ruling count is already one stale.** It says 331; the store parses at **332**
    (`python3 -c "import json;print(len(json.load(open('knowledge/_rulings.json'))['rulings']))"`).
    A ruling was inscribed after the #240 wrap. Not a defect — a demonstration that a copied
    figure ages [[trust-the-spine]].

---

## RULING-SHAPED QUESTIONS

1. **The banner cap.** Option (a) **10 lines / ≤1,200 tk**, delta owns all detail; option (b) 8
   lines / ≤900 tk, harsher; option (c) leave uncapped. **Recommend (a)** — it halves the most-read
   surface in the project without removing a category of information, and `check_budgets` already
   has the enforcement shape.
2. **The carry age cap (S3).** 202 items, 72,013 tk, ageing forever. Option (a) archive at age ≥10
   with an `s188-D2` receipt; (b) at age ≥20; (c) no cap, carry everything. **Recommend (a)** —
   the strike form already preserves wording verbatim beneath the strike, so nothing is dropped;
   but this is your open work and the cap is your number, not mine.
3. **The 119-sweep.** Option (a) retire it — its live verdicts are unprobeable; (b) re-run once,
   then retire; (c) keep the nag. **Recommend (a)**, with (b) acceptable if you want the last
   reading on the record.
4. **The wrap record as a form (S2).** This is the deepest cut and the riskiest: the prose is where
   premises and declared gaps get stated in words. Option (a) form with a mandatory `DECLARED:`
   field; (b) keep prose, cap at N lines; (c) leave it. **Recommend (a)** — but only after D1/D2/S1
   land, because those are free and this one is not.

---

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** *how many check-ins a single session actually runs.* The rehearsal and grade logs
  are keyed by **date**, not session, and 2026-09-02 held roughly eight windows. My 3–6 figure is
  a division, not a count. Price to prove: one session-id field in `_rehearsal_log_append` and one
  wrap to observe it — under 200 tokens of code.
- **UNPROVEN:** *whether every rehearsal's 7,534 tk actually entered the conductor's context.* I
  measured the stdout the instrument produces. Whether a given session piped, truncated or read it
  whole is not observable from here [[unmatched-grep-is-not-an-absence]]. Price to prove: one
  `--terse` flag and a before/after FILL reading at one wrap.
- **UNPROVEN:** *the S3 carry saving.* I measured the line at 72,013 tk and 202 items but did not
  parse the age brackets, so "30–50% at N=10" is an ESTIMATE with no probe behind it. Price to
  prove: one `_carry_items` walk reading each item's `[N]` bracket — ~5 minutes, no new code.
- **CLAIMED:** *the product/process classification of the 14 lanes.* Read off filenames and the
  #234–#240 banners, not off the reports themselves. The **counts** are probeable
  (`ls notes/_subreports/`); the **labels** are my judgment. Re-read costs ~127,000 tk.
- **NOT MEASURED, DELIBERATELY:** *#241's conductor boot.* My seat read 69,092 real — a subagent
  boot, a different object. The first post-diet conductor boot is `s240-D2`'s input and it is the
  conductor's to read, not mine to guess [[feedback-measuring-tool-must-not-guess]].

---

## Consequences and pitfalls — MANDATORY (Dave #165)

**(a) The gauge exists because sessions blew the window, and that is not history.** #230 crossed
the **256,000** wall at the conductor's own seat — the first time it happened there. #232 crossed
the armed 190,000 stop line by **41,518** and declared it late. Six of the last seven sessions
passed the 150,929 advisory. Cutting the check-in's *core* block (1,295 tk) would be the one cut
that pays for itself in a single overrun. **It is not on the list. Do not let a diet mood take it.**

**(b) The rulings store is how your decisions survive a closed chat.** 332 entries, twelve
consumers, zero cost at boot. A diet that touched it would not be a diet; it would be amnesia.
It is not on the list either.

**(c) A shorter banner can silently lose the declared gap.** The verbosity Dave is reacting to is
partly the honesty contract doing its job — *"a declared gap passes, a silent one fails"* is
enforced by prose, not by a field. If S1 or S2 lands, the cap must carry an explicit `DECLARED:`
line or the asymmetry that makes the whole record trustworthy quietly inverts.

**(d) Deleting the 461-id dump does not delete the items.** They live in `_state.json` and are
reachable by `python3 knowledge/_state.py`. But the chain currently *looks* like an inventory, and
a reader who trusted that look will now have to run a command. Say so in the chain footer, or the
first cold session to want an id will read `_state.json` whole — 147,059 tk, thirteen times what
the dump cost [[home-by-addition-then-cut]].

**(e) The rehearsal cut trades a loud surface for a quiet one.** Today a session cannot miss a new
warn, because all 13 print every time. A delta print means an unchanged warn goes unseen — which
is fine until a warn that was always there starts mattering. Mitigation: print the full list on
the *first* check-in of a session and the delta thereafter.

**(f) A carry age cap can archive something still live.** The carries are Dave's open work, and
"old" is not "done". `s225-D2` already says the pointer is not the list and nothing was dropped;
an age cap has to keep the same property or it becomes the drop the whole `s188-D2` mechanism was
built to prevent.

**(g) The savings are in FILL, not in quota** [[budget-vs-quota-vocabulary]] [[delegation-cost-inversion-110]].
D1, D2, S1, S5 and S7 all buy back **conductor window**, which is exactly the budget that bound
#240. S4 buys back **quota**, which is a different budget and does not help the lane that would
not fit. Name which one binds before spending the saving.

**(h) This lane is a recommendation and nothing here is ruled.** No constant, band, floor,
advisory, stop line, wall, cap, tier or version was moved by me. No file was edited by this lane
except this report. `git status --porcelain | md5sum` was **unchanged**
(`347420beedfa6ff13b3f788b0583ab80`) across every instrument run above, including the wrap-gate run.

⚠ **BUT THE TREE MOVED UNDER ME AFTER MY MEASUREMENTS, AND IT WAS NOT THIS LANE.** At my close
`git status` additionally shows ` M knowledge/_capture_gate.py` · ` M knowledge/_gauge_tokens.py` ·
` M knowledge/_surface_recorder.py`. Those are a **concurrent #241 lane** — almost certainly the
`W-386` boot-band build, which is ruled to touch exactly those files. **Consequence for this
report:** every gate and gauge figure above was taken from the tree as it stood *before* that
build landed, and the wrap-gate stdout figure (7,534 tk) in particular may not survive a re-point
of `boot_constant_drift_check` [[stale-mount-corroborates-a-stale-premise]]. Re-measure D1's saving
after the boot-band build commits; the *shape* of the finding — a full gate dump printed at every
check-in — does not depend on the figure.

---

## Evidence

No evidence directory: every figure above quotes the command that produced it inline, and every
command is re-runnable from the repo root.

REPLAY-THESE: `knowledge/_RUNBOOK-context-gauge.md` lines 381–411, § MEASURED, NOT RULED (~700 tk
— the ~19K lane price and the ≈55,692 read-back price, in their standing home) · `notes/_GAUGE-LOG.md`
§ `#### 2026-09-02 #238` post-mortem line (~465 tk — the n=5 measurement itself)
