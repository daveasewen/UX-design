# #300-C — The opener: what it costs, what leans on it, and a lean design

session: #300 · 2026-09-23
window: lane C — Opus 5.5 sub at the cloud seat, READ-ONLY on the repo apart from this report and `notes/_lanes/300/C/`; no Project-memory writes (brief rule 4)
brief: `notes/_lanes/300/BRIEF-300-boot-diet.md`
tokens: **302,081 real** context at the report-patch turn (87 distinct messages; sub boot 66,335) · output 90,859 · cache writes 244,507 · cumulative input processed 16.9M — a hand sum (`input + cache_creation + cache_read` per distinct `message.id`) over `…/d75f51cc-…/subagents/agent-aabef72a0a20f9190.jsonl`, not a `_checkin.py` reading
work files: `notes/_lanes/300/C/gen_boot_card_proto.py` (prototype generator) · `notes/_lanes/300/C/BOOT-CARD-300-prototype.md` (its output from today's files) · `notes/_lanes/300/C/PROJECT-INSTRUCTIONS-as-of-2026-09-23-ROLLBACK.txt` (today's Project instructions, byte-exact, md5 `a6e11674ea1bf0c74ffbd37cb10c5489` — the rollback)

---

## For Dave — in plain words

**Our own start-of-chat routine costs about 81,000 tokens on top of the 126,000 the cloud loads by itself. About 50,000 of it can go before Friday with nothing built: new Project instructions, and the wrap placing its own memory note.**

**Where today's 81,000 went** (measured on this chat):
- **Reading the handoff and the chain** — about 19,000.
- **Putting yesterday's memory note into Project memory** — about 21,000. Because that changes the memory, **your next message then carried the whole memory list again** — another 19,000.
- **Reading the memory index and its list** — about 5,500. It repeats what the handoff says.
- **A wrong turn finding the folder** — about 2,700. The instructions say "the UX-design folder"; the folder is called `Projects--UX-design`.
- **Digging for detail for the first reply** — about 6,000. The rest is the voice guide and the model's own working.

**The quick win — before Friday, nothing to build, fully reversible:**
1. **The wrap places the memory note**, as its very last act, through a helper. #299 already proved a helper can write to memory from the cloud.
2. **The start of a chat stops reading and writing memory.**
3. **The folder is named exactly**, so the first step never misses.
4. **The context check-in leaves the start.** In the cloud it finds nothing and quietly does nothing, and it has not worked since the move to the cloud on 22 September.
→ A chat would start its first reply at about **156,000 instead of 188,000**, and your first message would no longer cost 19,000 extra: **about 161,000 after your first message instead of 211,000.**

**The chain stays.** You said it is fundamental. Nothing here drops it.

**After Friday — one build:** a **one-page boot card** written by the wrap, holding the session number and title, the questions owed to you in plain words, the first beat, and where to fetch everything else. A working prototype made from today's files is about **1,450 tokens**. With the card plus the full chain, a chat starts at about **142,000**. With the card alone, and the chain fetched when the work needs it, it starts at about **131,000**. Which of the two is your call: it comes down to whether a one-page chain still counts as the chain.

**What this does NOT fix:** the 126,000 the cloud loads before anyone speaks. The wrap's gate stays red on that until the boot itself is cut (lanes A, B and D) or you rule on the ceiling.

**Next step:** the conductor puts version 2 of the instructions (§6) to you, and the #300 wrap becomes the first to place its own memory note.

---

## VERDICT

**HOLDS, with four corrections to the brief's premises.** The opener (the procedure between the harness boot and the first reply, plus the store re-send it causes) cost **81,049 real** at #300: **61,678 before the first reply + 19,371 re-sent at turn 2.** A no-build change (Project instructions v2 + the wrap placing the memory hook) removes **~50.6K per session**. The boot card built after Friday takes the opener to **~16.5K (card + chain)** or **~5.2K (card only)**. **None of it moves the 126,185 harness boot**, so the wrap gate's boot-ceiling arm stays RED either way.

**Corrections:**
- (a) **`BOOT_FIRSTTURN_TK` no longer exists.** It was DELETED at `s294-D7` (`knowledge/_gauge_tokens.py:281`), and the selftest fails if it comes back (`:885-886`). Only `BOOT_CEILING_TK = 72_768` remains (`:351`).
- (b) **#296, not #297, was the first cloud seat.** #296 was unmeasured (`notes/_lanes/298/DAVE-WORDS-AND-BOOT-FINDING-2026-09-23.md:21`; `notes/_lanes/296/WRAP-BRIEF.md:1` records the check-in's NO TRANSCRIPT at #296).
- (c) **Every arm `_checkin.py` carries has been dead since #296**, not only its fill reading (§3.1).
- (d) **The runbook's "only the conductor's seat can write the store" (#278) is false at the cloud seat.** #299's opener placed the #298 hook through a memory sub (`_HANDOFF-150-…md:60`; `notes/_lanes/299/WRAP-BRIEF.md:10`).

COUNTS: 13 opener messages traced · 6 moves mapped · 31 live dependents named (§3) · 18 externalities (§8) · 1 prototype card generated and checked · 0 repo files changed outside `notes/_lanes/300/C/` and this report.

---

## 1. What the opener does today — MEASURED (real tokens, `message.usage`)

Method: fill = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`, one value per distinct `message.id`. Source: `/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl` (the conductor, cloud container). Each step's delta = the previous message's `output_tokens` (thinking + tool calls, re-entering as input) + the tool results. The results are counted in cl100k over their TEXT (not the JSON-escaped form, which over-counts ★/⛔ by ~15%).

| # | msg | fill | Δ real | what came in (cl100k tape) | band item |
|---|---|---|---|---|---|
| 1 | xaQUZG | **126,185** | — | harness boot | HARNESS |
| 2 | YUNeAS | 133,075 | +6,890 | memory `index.md` 2,129 · dave-voice skill body 1,520 · first `ls` 446 · prev out 595 | procedure |
| 3 | 6WT6Ce | 135,728 | +2,653 | 2nd `ls` 1,300 — the first tried `$HOME/mnt/UX-design`, which does not exist | **folder miss** |
| 4 | 1rCSRf | 143,584 | +7,856 | `_HANDOFF-150` 5,116 | procedure |
| 5 | aNs5y5 | 157,635 | +14,051 | `_CHAIN.md` 7,428 · `memory_list` page 2 1,480 · `_checkin.py` 50 | procedure |
| 6 | 9b7vKD | 161,168 | +3,533 | `WRAP-MEMORY-HOOK.md` 1,747 · `ensure_env.sh` 109 · fill probe 35 | procedure |
| 7 | ozfUZ8 | 172,784 | +11,616 | `MEMORY-ARCHIVE-3.md` + `areas/presentation-friday-25th-288.md` 6,771 — read ONLY to get `if_version` tokens | **placement** |
| 8 | WNL7ox | 179,611 | +6,827 | the 3 store writes' bodies (prev out 6,529) | **placement** |
| 9–10 | Cosz6H · mT8cf5 | 181,821 | +2,210 | two `index.md` edits | **placement** |
| 11–13 | JCVowM · 2FZx7q · vuEZK1 | **187,863** | +6,042 | `git log` / rulings / lane grep 2,367 · fill probe 97 | orientation |
| — | first reply | | out 4,220 (visible text 910 tape) | | RUNNING |
| 14 | 3xDMuD | **211,454** | +23,591 | reply 4,220 + **memory snapshot RE-SENT 13,546 tape** + Dave's words 206 | **re-send** |

**By band item:** procedure reads 32,313 · folder miss 2,653 · placement 20,653 · orientation 6,042 = **61,678**; re-send **19,371** (23,591 − the reply's 4,220). REPLAY: the §Evidence one-liner prints `126185 187863 211454`.

**Wall-clock:** 14:46:47 → reply by ~14:49:35 UTC (transcript `timestamp`s). Time is not the problem; tokens are.

**Why the re-send happens (READ, not inferred):** the snapshot's own header says *"Assembled from the user's memory store … it is replaced when the store changes"* (transcript row 18). Its `version` changed between boot and turn 2 (`e53a7626…` → `e87e7f1c…`, rows 18 and 130). It arrived with Dave's next message, not with tool results: the six messages after the writes (rows 93–123) show no jump. No skills-list re-send at #300: one `skill_listing`, at boot only. #298's +25,021 included one (`notes/_lanes/299/WRAP-MEMORY-HOOK.md:24`).

## 2. Units — tape to real

The real/tape ratio is **~1.5 for Apollo's record prose.** It comes from three single-read steps: handoff (7,856−249)/5,116 = **1.49** · chain+list (14,051−706)/8,958 = **1.49** · archive (11,616−922)/6,806 = **1.57**. The turn-2 re-send gives **1.41**. The repo's own reference is `_gauge_tokens.py:28` (`_CHAIN.md` 4,384 tape / 6,897 real = **1.57**). **The card itself runs higher:** this lane read a 635-tape draft card and its own usage moved Δ1,240 − 213 prior output = 1,027 real, **×1.62** (code spans and glyphs tokenize worse). Card figures use 1.62. ASSUMPTION: a previous message's `output_tokens` re-enters 1:1. The steps' consistency supports this but does not prove it. Every "real" figure in §7 that is not a usage delta is tape × 1.5, labelled PROJECTED.

## 3. Dependency map — what reads or checks each thing the opener touches

### 3.1 `knowledge/_checkin.py` — the opener's check-in (DEAD at the cloud seat since #296)
- The transcript glob is `/sessions/*/mnt/.claude/projects/*/*.jsonl` (`:84`). `find_transcript` calls `sys.exit` on no match (`:87-97`). `main()` calls it at `:1179`, **before every arm**: disk `:1291` · REHEARSAL (the wrap gate early, #92) `:1329` · B2 plan block `:1345` · **B3 grade alerts** (`s179-D1`'s one mitigation) `:1379` · dream-pass seam (#185) `:1479` · 119-sweep expiry nag (`s241-D2`) `:1537`.
- #300's output, verbatim: `NO TRANSCRIPT FOUND under /sessions/*/mnt/.claude/projects/*/*.jsonl`. The cloud conductor's transcript lives in the cloud container, which the Mac cannot see.
- **Side effects stopped, MEASURED:**
  - `notes/_REHEARSAL-LOG.jsonl` `rehearse` rows: 41 on 2026-09-21, **0 on 09-22 and 09-23**, while the wrap gate's own `wrap-open` rows continue (32 and 25).
  - `notes/_dream/_GRADE-DECISIONS.jsonl` last row `2026-09-21T21:41:57`. **The B3 review's dataset stopped growing five sessions ago, silently.**
- Consumers that single-source the transcript from it are blind too: `_seam.py:94`, `_boot_decompose.py:11`, `_boot_remeasure.py:10`, `_memory_cap_check.py:33`, `_recall_probe.py:15`.
- Wraps since #297 measure fill by a hand sum in the cloud shell (`notes/_subreports/2026-09-22-297-W-wrap.md:33,66`; `…298-W-wrap.md:18`). "Should the hand sum become the sanctioned form?" is an open question for Dave (`297-W-wrap.md:66`).
- The `pip install tiktoken` line exists for this script (it FAILS LOUD without tiktoken, `:60`). tiktoken installs to the per-session user site (`/sessions/rcw-<session>/.local/…`, MEASURED at this seat), so every session pays it again. The render env's `outputs/_render-env/pylibs` on the mount persists.

### 3.2 `knowledge/_render/ensure_env.sh`
- It prints ONE line when OK (`:69`: `ENSURE_ENV: OK envdir=… shell=… pylibs=11 libs=2 size=408M`). 109 tape at #300.
- The render recipe in the Project instructions **re-runs it before every render anyway**. The opener's call buys an early warning and nothing else.
- `knowledge/_RUNBOOK-render-verify.md:34-35` OWES the line to the Project instructions ("after the `_checkin.py` step"). If the check-in leaves the opener, that runbook line is amended BY ADDITION.

### 3.3 `_gauge_tokens.py` constants and the capture gate's boot-ceiling arm
- `BOOT_CEILING_TK = 72_768` (`:351`, `s295-D3`, shrink-only, Dave's word) · `BOOT_BAND_WINDOW = 7` (`:326`) · `BOOT_BAND_SIGMA = 2.0` (`:327`). `BOOT_FIRSTTURN_TK` is deleted (`:281`).
- `_capture_gate.py::boot_constant_drift_check` (`:4878`) · `BOOT_DRIFT_BLOCKING = True` (`:226`) · `BOOT_CEILING_FROM_SESSION = 295` (`:4071`). The `s244-D1` declared discharge (`:4148-4187`) needs a LATER reading under the ceiling.
- **Run read-only now:** `FAIL boot-drift CEILING BREACH … #297 127,600 · #298 127,661`; derived band 89,443 ±26,087 (n=7, #288–#298).
- Since #298's wrap, `--wrap` commits have been refused and every wrap takes the DECLARED not-a-wrap path (`notes/_subreports/2026-09-23-298-W-wrap.md:44`; `…299-W-wrap.md:105`).
- ⇒ **The arm reads message 1. No opener move changes it.** Only the harness (A/B/D) or Dave's ruling does. Shrinking the Project instructions (410 tape, ~600 real, inside the boot's `session_context`) is the one opener-side lever on the boot, and it is negligible.

### 3.4 `_HANDOFF-*.md` — newest one read at the opener
- Readers: `_session.py` (R3 CHAIN OVERTAKEN, `:67,200`; its boot witness `_SESSIONS.jsonl` is dead since #108, last row 2026-08-06) · `_git_commit.sh:582` (post-wrap `_HANDOFF-<n+1>` commit guard) · `_test_git_commit.py` · `_validate_type_composites.py:271` (a citation).
- Handoffs are **cumulative**: `_HANDOFF-150:20` says it "does NOT replace `_HANDOFF-130`…`-149`". The machine index of every open item is `_CARRIES.md` § residual.
- **Handoffs are not in the Memento index.** `knowledge/_memento-index.json` holds 14 kinds, and neither handoff nor chain is one of them. The record's newest layer is invisible to `_memento_search.py`.

### 3.5 `_CHAIN.md` — generated, the "read contract"
- Built by `_gen_chain.py` (`OUT_NAME :63`, title block `:694`).
- Checked by `_build_all.py:491-495` (write · `--check` · `--selftest`), and so by CI (`.github/workflows/gates.yml:272` runs `_build_all.py`).
- `_capture_gate.py` mentions it 41 times: M10 read-chain budget `:2539-2578`, DO-FIRST items named in the chain `:3983`, B2 plan block `:6331`, and more.
- `_gen_chain.py` and `_memento_search.py` are in the package VERBATIM set (`_validate_package_delta.py:12,96`). An edit needs both `memento-package/` copies in the same commit.
- Opener models that assume the chain lands at turn 2: `_surface_recorder.py:66-67,81`, `_boot_remeasure.py:35`, `_gauge_tokens.py:139` (advisory instruments).
- **Dave, verbatim (#298 post-wrap, 12:44–12:49 BST):** *"the chain is fundamental to the project management surly , it might be made more efficient but getting rid of it doesnt make sense to me"* (`notes/_lanes/298/DAVE-WORDS-AND-BOOT-FINDING-2026-09-23.md:47`).

### 3.6 `GOOD-MORNING.md`
- The source the chain slices (header + ★ LATEST). About 30 live `knowledge/` scripts read it (`_gen_chain`, `_build_memento_index`, `_capture_gate`, `_gm_move`, `_gm_usage`, `_roll_state`, `_git_commit.sh`, …).
- **No opener read since #33**, and no move here changes it. **Unaffected.**

### 3.7 Memory `index.md`, the archive shards, and `WRAP-MEMORY-HOOK.md`
- Runbook step 3 (`knowledge/_RUNBOOK-capture-ritual.md:618-710`): the wrap sub writes `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md`, and "the CONDUCTOR places it at the NEXT opener" (`:697-699`, the #278 seat limit). **The cloud falsifies that premise** (VERDICT d).
- The index is capped at 49,152 B per file (`:703`). Archive shards open when the current one nears the cap: MEMORY-ARCHIVE-2 at #293, MEMORY-ARCHIVE-3 at the #296 opener (snapshot listing lines, transcript row 18).
- The `s271-D4` re-read of the hook's open items is **the ritual's final beat** (`:667-691`, `:792-797`). Placement must come after it.
- **The API forces reads.** Every edit to an existing store file needs `if_version` from a prior read (tool contract). So rolling ONE index line into the 20.7 KB archive shard cost a full read of it: **11,616 real** at #300 (step 7).
- `_capture_gate.py::hook_open_items_recheck` (`s271-D4`, `:4775`) → **`DECLARED SKIP — … carries no .auto-memory/MEMORY.md`**. `memory_cap_check` (`:3921`) → **`DID NOT RUN`**. Both resolve through `_memory_cap_check.resolve_path()` against the pre-#278 local store, so **both have been dead since #278** (run read-only now).
- `_gardener.py` (the dream pass) grades the **repo mirror** `notes/_lanes/<n>/WRAP-MEMORY-HOOK*.md` (`s294-D6`, `:194-222`, `:806-816`) and calls the cloud store unreachable. ⇒ **keep writing the hook FILE at every wrap.** The gardener never needs the store.
- The snapshot (boot) carries **the listing, not index.md's text.** "#298 WRAPPED" appears 0 times in it (row 18). Its 13,296 tape is 12,822 listing (150 lines) + profile 123 + preferences 198 + header 138 (lane D owns the census).

### 3.8 `knowledge/_memento_search.py` — the on-demand door
- Two-stage. `--fetch gm:LATEST` works today: 663 tape, 0.2 s at the seat.
- Fetch is kind-agnostic (`:131-140`). Stage-1 search drops kinds outside `KIND_ORDER` (`:74-75`).
- ⇒ Indexing handoff and chain sections in `_build_memento_index.py` alone makes `--fetch` work without touching the verbatim set. Making them SEARCHABLE needs `KIND_ORDER`, and so the two package copies.
- `_build_memento_index.py` has a bootstrap copy that the release manifest names (`knowledge/_release/_gen_pack_manifest.py:1839,2225`). That puts it in the release audit's path.

## 4. The lean design

### (i) THE BOOT CARD — generated at the wrap, ≤1,500 real
- **Prototype (built and run at the seat):** `notes/_lanes/300/C/gen_boot_card_proto.py` → `notes/_lanes/300/C/BOOT-CARD-300-prototype.md` = **3,126 B · 896 tape ≈ 1,450 real**, at the ×1.62 MEASURED for a card read (§2). A first cut at 941 tape would have been ~1,520 real, over the brief's 1,500, so the cap was tightened to 900 tape and the card trimmed.
- It is built from files that already exist: the newest handoff (session number from the H1, the OWED list as questions, the cold-seat facts, the post-wrap addendum headlines, a section map with sizes) and `_CHAIN.md` (the `YOU ARE #N. TITLE THIS CHAT →` line).
- **Its gate, `--check`** — five legs:
  1. FRESH: byte-equal to a regeneration.
  2. CAP: ≤900 tape (≈1,460 real at ×1.62). A real FIRST BEAT adds ~30–60 tape, so the cap will force a trim. That is intended.
  3. ROUTING: the handoff's `→ #N` equals the chain's `YOU ARE #N`.
  4. OWED: items were parsed.
  5. FIRST BEAT: present.
- **Today's result:** `BOOT CARD: FAIL (896 tape · #300 · 9 owed)`, one leg: *"NO FIRST BEAT section in the handoff (fallback used)"*. That is correct: no wrap has ever written one. **A new wrap obligation:** a `## FIRST BEAT` section in the handoff, one or two sentences, not a greeting, not a question.
- **Production form (after Friday):**
  - Rename it to `knowledge/_gen_boot_card.py`, with the help-gate prelude (`_validate_help_gate.py`: no write on `--help`) and `--check` / `--selftest` so `_build_survey.py` can ask it.
  - Wire write + `--check` into `_build_all.py` beside `_gen_chain.py`, which puts it in CI.
  - Output `_BOOT-CARD.md` at the root with a contract header (GENERATED · cap · replaced every wrap).
  - It runs at a **new ritual beat 5c**, after 5b and the `s271-D4` re-read, so post-wrap facts land on the card.
- **Known prototype defects:** section-map labels are crude, and cold-seat facts are cut to 4 items of 16 words. At the opener, `--check` should skip the tiktoken-dependent cap leg (the cap is enforced at the wrap, where tiktoken exists).

### (ii) Handoff and chain on demand, by section
- **Now, zero code:** `gen_boot_card --section <HEADING>` reads the live handoff (never stale). `_memento_search.py --fetch gm:LATEST` is the chain's banner (exists). `cat _CHAIN.md` gets the whole chain. The card prints these commands and the section sizes.
- **Later (optional):** add `parse_sections(…, <newest handoff>, "handoff", "handoff-section")` and `(…, "_CHAIN.md", "chain", "chain-section")` to `_build_memento_index.py`, which makes fetch work. `KIND_ORDER` for search needs the verbatim-set copies.
- ⚠ The index is rebuilt at 2g, before 5b, so an index-served handoff misses the addendum. The live read is the safer door.

### (iii) The memory hook at the WRAP seat — the careful plan Dave asked for
1. **Who:** a small memory sub (M), spawned by the wrap conductor after W, and **last**: after 5b, the `s271-D4` re-read and the boot card. Feasible, because #299's opener already did exactly this through a sub.
2. **What:** today's steps, unchanged: index line on top · oldest line to the archive · `wrap-<n>` file · area file. Or the SLIM form: **no archive roll**, because the evicted line already lives in the repo mirror. That drops the shard read, **−~10.6K real per placement**.
3. **Store line = pointer + title only**, no open items. Then a post-wrap ruling cannot make the store stale, and the card carries the open items.
4. **Cost moves:** ~21K from the next conductor's window to M's own window (disposable). The re-send (~19.4K) falls on the ENDING chat, and only if Dave speaks after the wrap.
5. **Fallback:** if a wrap could not place it, the card says so and the conductor places it through a sub. It pays the re-send once.
6. **Or retire it** (ruling): no live gate reads the store (§3.7). The loss is the accelerator for Dave's OTHER chats in this Project, which would stop seeing wrap lines. Lane D sizes what the snapshot then saves.

### (iv) `_checkin.py` and `ensure_env.sh` — one line each
- **One opener shell call:** `…_gen_boot_card.py --check; cat _BOOT-CARD.md; bash knowledge/_render/ensure_env.sh 2>&1 | tail -1`.
- **Check-in: out of the opener at the cloud seat** (it is a no-op there, §3.1).
  - Fill, when it matters: the container-side hand sum (the card carries the recipe).
  - The dead arms (after Friday): a no-transcript mode in `_checkin.py` that runs disk · rehearsal · grades · dream · 119 and prints **one summary line**. That restores five dead consumers.
- **tiktoken:** vendor it into `outputs/_render-env/pylibs` from `ensure_env.sh`, with `TIKTOKEN_CACHE_DIR` on the mount. The pip line then leaves the opener.
- ⚠ **The token saving from (iv) is small** (the two outputs were ~160 tape). Its value is honesty: removing a ritual that pretends to measure.

## 5. Minimal change set

| # | move | owner | when | reversible? |
|---|---|---|---|---|
| 1 | Paste Project instructions **v2** (§6): exact folder; one shell call; handoff + chain read (his ruling); no memory read or write at the opener; check-in and pip lines gone | Dave's paste | **before Friday** | yes — the rollback file, byte-exact |
| 2 | The **#300 wrap places its own hook** through a memory sub, last beat; amend runbook step 3 (`:692-710`) BY ADDITION for the cloud seat; amend `_RUNBOOK-render-verify.md:34-35` ("after the `_checkin.py` step") | the wrap seat | **tonight's wrap** | yes |
| 3 | `knowledge/_gen_boot_card.py` + `_build_all.py` wiring + ritual beat 5c + `## FIRST BEAT` in the handoff | a build lane | after Friday | yes (a generated file) |
| 4 | Project instructions **v3** (card-first) | Dave's paste | after 3 | yes |
| 5 | `_checkin.py` no-transcript arms-only mode (one line) · tiktoken vendored in `ensure_env.sh` | a build lane | after Friday | yes |
| 6 | Rulings: chain at the opener (A: card + chain / B: card, chain on call) · memory ritual (keep at wrap / slim / retire) · the boot ceiling (untouched by all of the above) | Dave | after Friday | — |

## 6. Draft Project instructions — paste-ready

**v2 — before Friday, nothing to build** (replaces only the opener block; Standing and Rendering are unchanged):

```
This is Apollo, a governed design-system engine. The repo is the folder mounted at $HOME/mnt/Projects--UX-design on Dave's computer (never the empty UX-design--UX-design). The repo is the record; Project memory is the accelerator.

On the first turn of every session, before replying:

1. In one shell call at Dave's seat: cd "$HOME/mnt/Projects--UX-design"; ls _HANDOFF-*.md | sort -t- -k2 -n | tail -1; bash knowledge/_render/ensure_env.sh 2>&1 | tail -1. If ensure_env prints FAIL, read the ninth stratum of knowledge/_RUNBOOK-render-verify.md before anything renders.
2. Read that newest _HANDOFF-*.md. It outranks everything, including _CHAIN.md.
3. Read _CHAIN.md.
4. Do not read or write Project memory at the opener: the wrap placed the last session's note. Only if the handoff says it was NOT placed, place it through a sub.
5. Reply in dave-voice with the session's first beat — not a greeting, not a question.

Standing: Dave rules from plain prose and visuals, never ID codes. Commits only via knowledge/_git_commit.sh; push is at the conductor's judgement with a CI read-back in chat. Every sub files its report at notes/_subreports/. At the cloud seat _checkin.py cannot see the conductor's transcript; when the fill matters, hand-sum it in the cloud shell.

Rendering: every render runs at Dave's seat, on the mount, in one bash call — export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver> with executable_path=$RENDER_SHELL. Never route a build through the cloud workspace because the seat "has no Playwright" — it does once ensure_env.sh has run. Files written for Dave live in the repo beside their source; give him the path, not a download.
```

**v3 — after the card exists** (the opener block only):

```
On the first turn of every session, before replying, in ONE shell call at Dave's seat:
cd "$HOME/mnt/Projects--UX-design" && python3 knowledge/_gen_boot_card.py --check; cat _BOOT-CARD.md; bash knowledge/_render/ensure_env.sh 2>&1 | tail -1
[A] Then read _CHAIN.md.   [B] Nothing else — fetch handoff and chain sections with the commands on the card when the work needs them.
If the card check fails, read the newest _HANDOFF-*.md instead — it outranks everything, including _CHAIN.md.
Never write Project memory at the opener. Reply in dave-voice with the card's first beat — not a greeting, not a question.
```

(Sort the handoffs numerically. `_HANDOFF-86`/`-87` sort after `-150` lexically, and `ls -t` trusts mtimes that a touch can move.)

## 7. The opener's cost, before and after

| | first reply at | turn 2 (after a one-paragraph message) | opener cost | room to 200K / 256K at turn 2 |
|---|---|---|---|---|
| **today (#300, MEASURED)** | **187,863** | **211,454** | **81,049** (61,678 + 19,371 re-send) | −11K / 45K |
| v2, no build (PROJECTED from measured parts) | ~156,300 | ~160,800 | ~30,100 | ~39K / ~95K |
| v3-A card + chain (PROJECTED) | ~142,700 | ~147,200 | ~16,500 | ~53K / ~109K |
| v3-B card only (PROJECTED) | ~131,400 | ~135,900 | ~5,200 | ~64K / ~120K |

- **v2 removes (MEASURED items):** placement 20,653 · index + list 5,469 · the hook read 2,691 (read only to place it) · folder miss 2,653 · check-in 74. That is 31,540, plus the 19,371 re-send.
- **v3 adds** the card (~1,450) and removes the handoff read (7,856) and the orientation (6,042), because the card carries the first beat and the owed list.
- **Kept in every row:** dave-voice (~2,330) · ensure_env (~170) · the model's own output.
- **The boot is 126,185 in every row.**

## 8. Externalities — every one named

1. **His ruling on the chain.** v2 and v3-A keep it at the opener. v3-B does not, so it must be put to him, not enacted.
2. **Dave's other chats in the Apollo Project** see the memory store. Placement at the wrap makes it *fresher* (it lands when the session closes, not when the next one opens). Retiring the ritual takes the wrap lines away from those chats.
3. **The re-send moves to the ending chat** (~19.4K) if Dave speaks after the wrap. It is harmless at the true end, but paid if a post-wrap conversation continues.
4. **A post-wrap ruling after placement** makes the store's open list stale. Mitigation: pointer-only store lines (§4 iii-3).
5. **The wrap grows:** it authors a FIRST BEAT, runs the card generator, and runs an M sub (~15–21K in M's own window, ~300 real stub in the conductor).
6. **CI:** a card `--check` in `_build_all.py` turns a stale or uncommitted card RED in the `gates` job, as `_CHAIN.md` does. `_build_survey.py` counts shift by the new script (they are pinned in wrap reports as "59 pass · 6 FAIL · 4 COULD-NOT-ASK"; check whether any test pins them).
7. **Help gate:** a new entry-point script must not write on `--help` (`_validate_help_gate.py`).
8. **Package parity:** any edit to `_memento_search.py` or `_gen_chain.py` needs the two `memento-package/` copies (`_validate_package_delta.py`). The card design avoids both files.
9. **Release pack:** `_build_memento_index.py`'s bootstrap copy is named in `_gen_pack_manifest.py:1839,2225`. Indexing handoffs touches the release audit, so it stays after Friday.
10. **Runbooks go stale unless amended:** step 3's #278 seat-limit paragraph (`_RUNBOOK-capture-ritual.md:692-710`) and render-verify's "after the `_checkin.py` step" (`:34-35`).
11. **Advisory instruments model the chain as turn-2 additive** (`_surface_recorder.py:66-67,81`, `_boot_remeasure.py:35`, `_gauge_tokens.py:139`). Their opener model is wrong under v3-B.
12. **The five dead `_checkin.py` arms** (rehearsal, B3 grades, dream seam, 119 expiry, disk) are an externality of the cloud move, already paid for five sessions. Dropping the line makes it visible, and restoring them is a build (§4 iv).
13. **`hook_open_items_recheck` and `memory_cap_check`** have been dead since #278. Retiring the store loses no live machine check.
14. **The gardener grades the repo mirror**, so every wrap must still write `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md` whatever happens to the store.
15. **The boot-ceiling arm stays RED.** No opener move touches message 1, and `--wrap` stays refused, so the declared not-a-wrap path continues.
16. **Friday's deck:** no move touches the deck files or their build (`notes/_lanes/296/C/build_c.py`). The instructions change is a paste, and the rollback is on disk.
17. **Dave's client work on the same account:** Project instructions and the Apollo memory subtree are per-Project, so there is no externality (lane B owns account-level switches).
18. **Handoffs are cumulative** (§3.4). A card built from only the newest handoff must point at `_CARRIES.md` § residual for the older open items, or those items drop out of view at the opener. The prototype does.

## 9. Ideas not yet proven — labelled

- **UNPROVEN: the "one call" opener.** Card + ensure_env in one shell call, then reply. It is projected at ~5K; no session has run it.
- **UNPROVEN: timing as a lever.** Batch every store write into the last tool call before a chat's final reply. The re-send attaches to the NEXT user message (row 130), so a write with no next message costs nothing. This is inferred from one chat.
- **UNPROVEN: the card as the chain's efficient form.** Generate the card and `_CHAIN.md` from the same `_gen_chain` data, so "the chain" is one artefact with a one-page face and a full body. This speaks to his "made more efficient". It needs `_gen_chain.py` edits, and so the package copies.
- **REJECTED: the card in Project docs.** It would bust the prompt cache of every chat in the Project on each write, per the Projects tool's own warning ("Changing a doc's content busts the prompt cache").
- **UNPROVEN: a zero-store Apollo.** Memory would hold only profile and preferences, and the card would be the only accelerator. Lane D sizes the boot saving. The loss is externality 2.

## RULING-SHAPED QUESTIONS

1. **The chain at the opener:** is a one-page boot card "the chain made more efficient" (v3-B, ~131K start), or must the full chain still be read at every start (v3-A, ~142K)?
2. **Where the memory note is placed:** at the end of the wrap, by a helper (recommended), or not at all?
3. **The memory archive:** when the index is full, drop the oldest line (the repo keeps it) instead of reading the 20 KB archive to append it? That saves ~10.6K per placement.
4. **The dead check-in:** restore its five checks as one line at the start (a build), or retire them by name?
5. **The boot ceiling** is unchanged by all of this and still yours: cut the boot, raise the number, or keep the declared path.

## UNPROVEN / CLAIMED (ADR-0016)

- **PROJECTED:** every §7 figure not labelled MEASURED (tape × 1.49–1.57, and output tokens assumed to re-enter 1:1).
- **INFERRED:** that a sub can write the store at the WRAP seat. It is READ that a sub placed a hook at #299's opener (`_HANDOFF-150:60`). This lane did not write (brief rule 4).
- **CLAIMED:** "#298 +25,021 included a skills-list re-send" is taken from `notes/_lanes/299/WRAP-MEMORY-HOOK.md:24`. This lane did not re-read #298's transcript (not in this container).
- **NOT MEASURED:** the wall-clock of a first ensure_env build moving from the opener into a render call (the runbook says one call once timed out at 180 s mid-unzip, `_RUNBOOK-render-verify.md:31-33`).

## Evidence — REPLAY-THESE

- Fills (cloud container): `python3 -c "import json;s={};[s.__setitem__(r['message']['id'],r['message']['usage']) for r in map(json.loads,open('/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl')) if r.get('type')=='assistant'];f=[u['input_tokens']+u['cache_creation_input_tokens']+u['cache_read_input_tokens'] for u in s.values()];print(f[0],f[12],f[13])"` → `126185 187863 211454`
- Card (seat): `cd "$HOME/mnt/Projects--UX-design" && python3 notes/_lanes/300/C/gen_boot_card_proto.py --check` → `BOOT CARD: FAIL (896 tape · #300 · 9 owed)` + one leg, NO FIRST BEAT
- Check-in exits before every arm (seat): `sed -n '84,97p;1179p' knowledge/_checkin.py`
- Ceiling arm (seat): `PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print(g.boot_constant_drift_check('.')[0])"` → `CEILING BREACH … #297 127,600 · #298 127,661`
- Dead memory arms (seat): the same import, `g.hook_open_items_recheck('.')` and `g.memory_cap_check('.')` → `DECLARED SKIP` · `DID NOT RUN`
