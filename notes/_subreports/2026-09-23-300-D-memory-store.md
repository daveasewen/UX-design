# Lane D — the memory store · #300 · 2026-09-23

provenance: #300 lane D · 2026-09-23 · Opus 5.5 sub (cloud container + Dave's Mac through device_bash) · read-only on Project memory (memory_list ×4 pages, memory_read ×2 calls; no write, append, str_replace or delete) · repo writes only in `notes/_lanes/300/D/` and this file · no git status, no commits.

## For Dave — the answer in plain words

**Memory costs you about 20,000 tokens at every start, and about the same again whenever something is written to it mid-session.** The list of memory files that arrives before anyone speaks is already at its ceiling: it shows 150 of the 234 Apollo files and stops there. It can't grow any more, but it also can't shrink until the store holds fewer than 150 files.

**Today's second copy was pure waste.** When the start placed the new wrap note, the whole list came in again with your next message (+23,600 tokens), and it was the same list word for word. The new note isn't even one of the 150 that get shown.

**The store is not a copy of the repo.** About 200 of its files came over from the old Cowork memory folder on 16 September, and they were never saved in the repo (git has never held them). In a sample of 23 files, under a fifth of their lines exist anywhere in the repo. So nothing gets deleted until the store has been copied into the repo.

**What I'd do, in order:**
1. **Now, before Friday: stop the memory steps at the start of a session** (reading the index and the archive, and placing the wrap note). That saves about 43,000 tokens a session. Nothing is deleted, and it can be switched back on any time. The wrap notes already live in the repo.
2. **Copy the whole store into the repo.** One sub, about 10,000 tokens, nothing in memory changes, fully reversible. This lane has already proven the method on 23 files.
3. **After Friday, and only when you say so: cut Apollo's memory to a handful of files, or to none.** The start gets about 19,000–20,000 tokens lighter. Deleting is permanent, so it waits until step 2 has been checked.

**Retire it or shrink it?** Once step 1 is done, emptying Apollo's memory and keeping five files are within 1,000 tokens of each other per session. Retiring only pulls clearly ahead (about 16,000 tokens more) if there's a switch that turns memory off for this project alone. Lane B is checking whether one exists. Your other work isn't touched either way. Your 16 personal account files (profile, preferences, areas, topics) aren't part of Apollo's list, and I recommend no change to them.

## The numbers (tape = cl100k estimate · real = billed, from usage fields)

| # | What | Figure | Receipt |
|---|---|---|---|
| 1 | Store census | 250 files, 1,007,956 B = 234 Apollo files (993,985 B) + 16 account files (13,971 B); 0 other-Project files visible | memory_list, no prefix, 2 pages (150 + 100); `notes/_lanes/300/D/store-census.tsv` |
| 2 | Boot memory list (the `cowork_memory_context` attachment) | 40,645 chars · **13,296 tape** as text (14,680 tape as the ASCII-escaped JSON record — the brief's figure) ≈ **20.4–21.7K real** | `replay_D.py` §1 · conductor transcript line 18 (0-based) |
| 3 | Its listing | 150 entries + "… and more (showing 150 — memory_list for the rest)"; mean **84.8 tape/line** ≈ 130–139 real | `replay_D.py` §1 |
| 4 | The re-send | fill 187,863 → 211,454 (**+23,591 real**, all cache_creation) at the next user message; re-sent text **byte-identical** to the boot copy (sha1 `1f05af5af7ef` both, 40,645 chars both) while the store version changed `e53a7626…` → `e87e7f1c…` | transcript lines 18 and 130; `replay_D.py` §1–2 |
| 5 | Other memory blocks at boot | `<user_memory>` guidance in the system prompt 5,637 + five memory tool schemas 3,634 + memory MCP instructions 478 = **9,749 tape** | `replay_D.py` §4 |
| 6 | Memory's share of the conductor boot | 23,045 tape ≈ 35.3–37.7K real = **28–30 % of 126,185** | #2 + #5, scaled |
| 7 | Opener memory traffic | 9 calls, **14,217 tape** (inputs 3,564, results 10,653) ≈ 21.8–23.2K real | `replay_D.py` §3 |
| 8 | Memory-attributable by message 14 | boot blocks + opener traffic + one re-send ≈ 50,558 tape ≈ **77–83K real of the 211,454** | #2 + #5 + #7 + #4 |
| 9 | Repo twins | filename 8/234 (all a stale July-18 copy) · description sentence 14/234 · body sample 62/325 line-heads (19 %) · git history: 8/234 basenames ever committed (1,621 commits, full history) | §4 below |
| 10 | Store cut to 5 files | **953 tape ≈ 1.46–1.56K real** — saves 18.9–20.2K real per boot and per re-send | `model.py` (§6) |
| 11 | Account-level premise | 16 account files; 2 already rendered in full (327 tape); the other 14 appear 0 times in today's listing; if they surfaced after a cut: ≈ 315 tape | §3 below |

**Tape → real ratio: 1.531–1.634**, derived from the #300 re-send. The real delta 23,591 covers the snapshot (13,296 tape) + Dave's message (206) + the reminder (26) + the previous reply's text (910), and possibly its thinking (972). 23,591 / 15,410 = 1.531, and 23,591 / 14,438 = 1.634. Single figures below use 1.559 (inside the range; it matches the ×1.559 in memory file `tape-is-openai-not-claude.md` from #53, cited as corroboration only). The ratio is assumed uniform across prose, JSON schemas and paths. That's an inference, and lane A reconciles to the boot.

## 1. Census

- **250 files** (memory_list with no prefix: page 1 = 150, page 2 = 100). Apollo subtree `/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/`: **234 files, 993,985 B**. Account level: **16 files, 13,971 B** (`/areas/` ×8, `/people/` ×1, `/topics/` ×5, `/profile.md`, `/preferences.md`). **Other Projects: none visible.** This session's memory-server instructions say other Projects' files are not readable. `_HANDOFF-129…:18` and the runbook (step 3, ~line 700) still say "other Projects' subtrees visible", and that premise is stale today.
- **Apollo files by kind:** topic/ruling notes 169 (536,649 B) · wrap-NNN 31 (192,656 B) · archive shards 3 (115,444 B) · hook-overflow 11 (80,864 B) · feedback-* 14 (53,281 B) · areas/ 5 (9,000 B) · index.md 1 (6,091 B).
- **Dates:** 203 of 234 carry the 2026-09-16 03:13–03:20Z import stamp; 31 were written or edited later.
- **Source tag** = the frontmatter `sources:` key, printed in the listing line. Best-known tag per file is in column `source_tag_best` of the census:
  - `cowork-import` 199: 134 listed, 6 read, 59 inferred from the import stamp. The stamp→tag rule holds with no exception on the 150 listed.
  - `cowork` 32: 14 listed, 3 read, 15 inferred (later wraps).
  - None 2: wrap-280 and wrap-281.
  - Unknown 1: `MEMORY-ARCHIVE.md`, never read.
  - `cowork-import` was written by the Anthropic import (`_HANDOFF-129…:13`). `cowork` is written by our own seats: the #300 conductor's `memory_write` content carried `sources:` in its frontmatter (transcript line 83). The repo hook files don't (grep of `notes/_lanes/{280,286,299}/WRAP-MEMORY-HOOK.md`: 0 hits).
- Per-file table: **`notes/_lanes/300/D/store-census.tsv`** (10 columns: scope, path, bytes, updated, in_boot_snapshot, source_tag, aliases, snapshot description, preview, source_tag_best). `store-census-v2.tsv` beside it is an earlier 9-column copy. Deleting is off on this mount, so it stays.

## 2. The listing line, its cost, and which 150 are shown

**Format** (harness-printed): `<full path> [aliases: …] [sources: …] — <description, or the first body line, cut near 160 chars + "…">`.

**Per line, mean 84.8 tape:**
- the `/projects/<uuid>/` prefix, printed on every line: **28.0** (4,200 tape across 150 lines, a third of the listing)
- relative path: 9.4
- tags: 6.3
- description: 40.4
- separators: ≈ 0.8

**Whole snapshot, 13,296 tape:** preamble 138 · profile 126 · preferences 201 · listing 12,826 (header 14 + 150 entries 12,725 + truncation line 15 + frame) · close 5.

**The cap binds.** 150 are shown and 84 are hidden, so **deleting files saves nothing until the Apollo count falls below 150**. After that, each file removed saves ≈ 85 tape ≈ 130–139 real at every boot and every re-send. The listing cost has sat flat at its maximum since the 09-16 import took the store past 150 (inference: the store arrived as ~200 files, `_HANDOFF-129…:16`). It isn't what grew lately. `_HANDOFF-129…:23` records the Cowork seat at #278 carrying the "cloud listing" (≈8K, unit not stated there), so the list isn't a cloud-seat invention either.

**Which 150? Opaque.** They are neither the first 150 by path nor the newest 150 by update time (scripts `cmp.py`, `sel.py`). In path order:
- **Shown:** `MEMORY-ARCHIVE-2`, `-3` · `areas/*` (5) · `filed-sub-reports-ruled-218` → `wrap-281` (143).
- **Hidden:** `MEMORY-ARCHIVE.md` · `a-crash…`, `a-new-tier…` · `art-director…` → `feedback-wrap-is-not-optional` (60) · `wrap-282…` → `write-once…` (21).
- ⇒ **The 18 newest wrap notes (#282–#299), placed one per opener, are not in the boot list.** In today's snapshot, placing them has had no effect anyone can see at boot.

## 3. Account files: the premise test

Premise: "account-level files would fill the 150-line listing if project files were cut." **FALSE, on count and on cost.**
- Only 16 account files exist. Two of them (profile, preferences) are already rendered in full as their own sections (327 tape).
- The other 14 don't appear in today's listing at all, even though 9 of them sort before `/projects/` by path. The listing is therefore Apollo-scoped or Apollo-first (inference).
- If all 14 surfaced after a cut, they would add ≈ 315 tape (22 tape per line: short paths, short descriptions) ≈ 0.5K real.
- These files hold Dave's other work and family matters. **No action is recommended on them.** Changing them is an externality to his other chats.

## 4. Repo twins: was the Cowork memory directory committed? No.

| Test | Result |
|---|---|
| (a) same filename anywhere in the repo | **8 / 234**, all in `_retired/agent-memory-snapshot-2026-07-18/store/` (comms-style-exec-summary, feedback-type-composites-mandatory, gate-glob-scope-rule, git-push-method, memento-framing, model-selection-by-phase, sandbox-html-rendering, workflow-commit-summaries). July-18 copies, and stale: git-push-method's 95 line-heads match its July copy in 11. |
| (b) distinctive sentence: first 48 chars of each file's description/first line, `grep -F` over 7,911 text files (340 MB; repo minus `.git`, `node_modules`, `notes/_lanes/300`) | **14 / 234**: 6 in the July-18 copy, 8 in `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md` (wrap-277…285) |
| (c) body sample: 23 files (20 read by this lane, 3 already in the conductor transcript); every line ≥ 60 chars → a 60-char head, `grep -F` over the same corpus; wraps also 8-gram-shingled against their own hook file | **62 / 325 heads (19 %)**. Wrap notes with a hook: wrap-299 100 %, wrap-296 71 %, wrap-286 59 % (shingles). wrap-270 (before hooks began at #273): 2 %. index.md 33 %, MEMORY-ARCHIVE-3 23 %, areas/presentation-friday 23 % (shingles vs all hooks). **The 14 imported notes: 0–29 %, 10 of 14 at 0 %.** |
| (d) git history: `git --no-optional-locks log --all --name-only`, 1,621 commits since 2026-05-31, not shallow | **8 / 234 basenames ever committed** (`knowledge/_agent-memory/store`, later `_retired/agent-memory-snapshot-2026-07-18/store`). The ~200 imported Cowork files never entered git. |

**Verdict:** about 0.7 MB of the store (≈190 imported notes, plus the archive shards' pre-#278 lines and `areas/*`) exists nowhere else verbatim. `_HANDOFF-129…:20` says "harmless while the repo holds everything durable", and that does not hold for this content. Wrap notes #273–#299 (27 files, 173,327 B) do have repo hook files, partial to full. The imported notes' substance may exist in the repo in other words (decision history, runbooks); that was not measured.

## 5. The re-send, traced (conductor transcript, 0-based line numbers)

**The opener's nine memory calls** (14,217 tape):
- `memory_read index.md` (line 28)
- `memory_list` after `wrap-281` (line 53). The conductor had to list what the snapshot hides.
- `memory_read MEMORY-ARCHIVE-3 + areas/presentation-friday-25th-288` (line 73)
- `memory_write` wrap-299 (new file), `memory_append` MEMORY-ARCHIVE-3, `memory_str_replace` presentation-friday, `memory_str_replace` index.md ×3 (lines 83–104)

**The re-send:**
- The next user message (line 128, 14:58:10Z) carried a fresh `cowork_memory_context` (line 130). The fill rose by +23,591 real.
- No re-send happened inside the tool loop (lines 83–123). One re-send covered five writes.
- **The re-sent text equals the boot text byte for byte.** The writes changed file bodies, not listed descriptions, and the one new file is hidden by the cap.
- The harness says the snapshot "is replaced when the store changes" (snapshot preamble). Its guidance adds "a newer snapshot, if one arrives, supersedes it" (system prompt `<user_memory>`). The old copy stays in context, so **every re-send is additive**.
- ⚠ This transcript has only one later user turn, and it followed writes. So "re-sends on store change" versus "re-sends on every user turn" is not separable here. **Natural experiment:** the conductor's next user turn after these lanes, with no store write in between, should carry no `cowork_memory_context` (X to read).

**Sub seats:**
- All four lane subs booted at 66,3xx real with **no** `cowork_memory_context` and no `<user_memory>` block. They do carry the five memory tool schemas (3,634 tape; this lane's own snapshot).
- A sub can read the store in the cloud seat (this lane did), and `_HANDOFF-150…:60` records "a memory sub placed the #298 hook". **The runbook's "only the conductor's seat can write cloud memory" (step 3, ~line 694) is stale for the cloud seat.**

**The runbook's price is too low.** It prices the opener placement at "≈4K tokens" (step 3, ~line 699). #300 measured ≈ 22K real of memory traffic plus the ≈ 23.6K re-send.

## 6. The snapshot after a cut

Model (`model.py`): four of the five lines come from today's snapshot; the absent one (wrap-299) is estimated from its preview ×1.80, the measured listing/preview token ratio over 87 files.

| Store state | Tape | Real (×1.531–1.634) |
|---|---|---|
| Now: 150 lines, capped | 13,296 | 20.4–21.7K |
| Cut to 5 (index.md, MEMORY-ARCHIVE-3, areas/presentation-friday, memory-brain-is-the-repo-278, wrap-299) | **953** | **1.46–1.56K** |
| Cut to 5, and the 14 account lines surface | 1,282 | 1.96–2.10K |
| One pointer file | 569 | 0.87–0.93K |
| Apollo subtree emptied | 492 | 0.75–0.80K |
| Emptied, 14 account lines surface | 821 | 1.26–1.34K |

Cut to 5 saves **18.9–20.2K real at every boot**, and at every re-send afterwards (the re-sent copy is the small one). An uncapped listing of all 234 would be ≈ 20.4K tape. The cap is already hiding a third of the store.

## 7. Export-then-delete: method and cost

**Export (no store change, reversible):**
1. `memory_list`, two pages (paths and bytes, ≈ 7K tokens without previews).
2. `memory_read` in **12 batches of ≤ 20 paths, bin-packed to 82–84 KB each**.
   - A result over the tool-output limit spills to a container file (`/root/.claude/projects/…/tool-results/mcp-memory-memory_read-*.txt`) instead of entering the context.
   - Observed here: an 18-file batch of 64,338 chars (19,330 tape) spilled. The threshold itself is unmeasured, but it is ≤ 64,338 chars, and every packed batch is larger.
   - Context cost ≈ 350 tokens per batch.
3. A container script splits each spill on `=== <path> ===`. It keeps each `[updated][version]` header in a manifest (path, bytes, sha256, version token; **the version token is what `memory_delete` requires**), tars the files, and `device_commit_files` them into the repo (e.g. `notes/_memory-export-2026-09-2x/`). **Proven end to end on 23 files → `notes/_lanes/300/D/sample/`.**
4. Verify on the Mac: 234 files, bytes against memory_list (± the header), the sha manifest. Commit through `knowledge/_git_commit.sh`.

**Export cost:**
- ≈ 8–10K tokens in the exporting seat (12 × ~350 + scripts + commits).
- **0 re-sends.** A sub can do it.
- Quota: one sub boot (~66K real) plus its turns.

**Delete (store change, permanent):**

5. `memory_delete` takes **one path and an `if_version` from a prior read** (schema loaded, never called). The export manifest supplies both. A file changed since the export fails safe.
6. ≈ 229 calls (cut to 5) or 234 (empty), ~20 parallel calls per message. At ≈ 100–130 tokens per call that is **≈ 23–30K tokens in the deleting seat** (estimate).
7. **One** re-send lands on the conductor's next user turn, and it is the new, small snapshot (~1.5K real). There is none at all if the delete is a session's last act.

**Rules on deleting:**
- The tool's own description says delete "ONLY when the user explicitly asks … Never delete proactively to clean up". So it needs **Dave's explicit word, in plain prose.**
- Undo isn't practical: re-creating ~1 MB through `memory_write` passes every byte through a context.
- **Order: export → verify → Friday → delete → check the next boot's attachment size** (`replay_D.py` §1).

## 8. Retire or shrink? (per session, memory-attributable only; real at ×1.559)

| Option | Tape | Real | Saves vs today |
|---|---|---|---|
| Today: boot blocks + opener traffic + one re-send | 50,558 | 78.8K (77.4–82.6) | — |
| **B. Stop the opener memory steps only** (no reads, no writes, so no re-send) | 23,045 | 35.9K | **42.9K** |
| C. Cut to 5, no ritual | 10,702 | 16.7K | 62.1K |
| D. Cut to 5, lean ritual (read index, 1 write, 1 edit, small re-send) | 15,357 | 23.9K | 54.9K |
| E. Empty Apollo's subtree (memory feature still on), no ritual | 10,241 | 16.0K | 62.9K |
| F. Memory off for this Project, **if** such a switch exists and removes all four blocks | 0 | 0 | 78.8K — UNSOURCED (lane B) |

**Reading:**
- The big win is **B**, followed by any cut below the cap.
- **Retiring (E) and shrinking (C) differ by 461 tape ≈ 0.7K real.** That's noise.
- Retiring only clearly beats shrinking through F, and F's value depends on its scope. An account-wide switch would turn memory off in Dave's other chats (externality); a per-project one would not.

**What retiring loses:**
- the ambient list of ~150 lesson titles at boot (an arbitrary-looking subset that already hides the newest notes);
- memory context for Apollo chats on claude.ai outside Cowork;
- the live Friday strand note `areas/presentation-friday-25th-288.md`. **Keep it until after Friday.**

**What shrinking keeps:** a slot for a tiny boot pointer that arrives free (§10.1).

## 9. Dependencies and externalities (store-side; the opener's are lane C's)

- **Project instructions**: "List the Project memory and read index.md" and "If notes/_lanes/<n>/WRAP-MEMORY-HOOK.md … is not yet in Project memory, place it". Both go with option B.
- **`knowledge/_RUNBOOK-capture-ritual.md` step 3** (lines ~618–712): memory update, placement at the next opener (the ≈4K claim), and the seat-limit text, which is stale for the cloud seat.
- **`knowledge/_gardener.py` 184–222**: grades the repo mirror (`WRAP-MEMORY-HOOK*.md`) and declares the store unreachable. Unaffected by any option here.
- **`knowledge/_capture_gate.py`** `memory_cap_check` (3908–3950, ADVISORY, `MEMORY_CAP_BLOCKING = False`) and `HOOK_STORE_SKIP` (4661): these resolve the old Cowork path. Unaffected.
- `knowledge/_checkin.py:1388` and `knowledge/_gauge_tokens.py:187`: comments only.
- `_HANDOFF-129…:18,20` and the runbook: "other Projects' subtrees visible" and "harmless while the repo holds everything durable". Both are false today (§1, §4).
- `knowledge/_ENACTMENT-REGISTER.md:37` ADR-0007, "Project memory as a temporal decision-graph" (UNPROVEN). The name overlaps; X to check whether it means this store.
- The **dream-pass skill** (a claude.ai skill, not inspected) may read the store. UNSOURCED; X to check. `notes/_dream/_MEMORY-GRADES.json` holds index lines (one MEMORY-ARCHIVE-3 line was found there).

**Externalities:**
- **Dave's other work:** none, unless account files or an account-wide switch are touched.
- **Friday's deck:** none from B or the export. Keep `areas/presentation-friday-25th-288.md` until after Friday.
- **The wrap ritual:** B removes the opener placement. The wrap notes stay in the repo, where they already are.

## 10. Ideas (unproven, labelled)

1. **The listing as a free boot card.** After a cut, one file whose *description* is the boot pointer (e.g. "#301 — first beat …; read _HANDOFF-151") arrives at boot for ~90 tape with no read call. Only ~160 characters survive the cut-off. Write it as the session's last act so no re-send lands on a live conductor. Unproven.
2. **Write only in the last turn.** A store change in a session's final turn costs nothing in that window, and the next boot pays for it once. This follows from the re-send riding the next user message (lines 83–130).
3. **A boot-size alarm.** Run `replay_D.py` §1 at the wrap seat and flag a snapshot over 2K tape after a cut. That catches a re-import refilling the store (the "one-way risk" of `_HANDOFF-129…:20`).
4. **Our only lever on the listing is the file count.** The path prefix (a third of every line) and the tags are harness-printed.

## 11. Replay (reproduces the top numbers)

- Container-side working scripts (`cmp.py`, `sel.py`, `runs.py`, `model.py`, `window.py`, `memtools.py`, `opener_mem.py` and others) are copied to `notes/_lanes/300/D/scripts/`. They read `snap_18.txt`, written by `snap.py`, and the census TSV. Run `snap.py` first, in the container.
- Cloud container: `python3 notes/_lanes/300/D/replay_D.py /root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl`. The repo copy of the script runs as-is. It prints the snapshot sizes, sha and identity, the listing count and per-line mean, the fills, the memory tool traffic and the memory boot blocks.
- Store census: `memory_list` (no prefix; continue with cursor) → 250 lines. The saved table is `notes/_lanes/300/D/store-census.tsv`.
- Mac, twins: from the repo root, `python3 notes/_lanes/300/D/twin_needles.py; xargs -0 -a notes/_lanes/300/D/corpus.lst0 grep -F -o -H -f notes/_lanes/300/D/needles.txt | wc -l` → 14. Then `python3 notes/_lanes/300/D/body_twins.py; xargs -0 -a notes/_lanes/300/D/corpus.lst0 grep -F -o -H -f notes/_lanes/300/D/body-needles.txt > notes/_lanes/300/D/hits-body.txt; python3 notes/_lanes/300/D/body_agg.py` → 62/325. Finally `python3 notes/_lanes/300/D/shingle.py`.
- Mac, git: `GIT_OPTIONAL_LOCKS=0 git --no-optional-locks log --all --name-only --format= | sort -u` → match basenames: 8 / 234.

## Spend

Hand-sum of `/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb/subagents/agent-a23a3fec975143ffe.jsonl` at filing, per distinct message.id: **84 assistant messages · boot 66,324 real · last fill 302,590 real** · cache_creation 245,016 · cache_read 15,622,989 · output 11,049 · input 168. A few more messages follow for the hand-back. The fill is high because the store listing was read twice (with and without previews, ≈ 30K) and the lane's reasoning is long. The 18-file memory read spilled to a container file and never entered the context.
