# #300 · Lane A — Attribute the window

provenance: 300 · 2026-09-23 · lane A (Opus 5.5, sub of the cloud conductor) · read-only · status: observed
work files: `notes/_lanes/300/A/` (scripts `attribute_window.py`, `features.py`, `top25.py`; outputs in `out/`)

## For Dave, in plain words

**The cloud boot is 126,185 tokens before anyone speaks, and three things make it up.**

1. **Tool definitions — about 65K (half the boot).** The cloud seat loads the full instructions for 68 tools. The biggest: 17 in-chat widgets (maps, recipes, quizzes, charts, sport scores) at 16K, the Artifact tool at 12K, scheduled tasks at 7.5K, the Mac link at 6K.
2. **Anthropic's system prompt — about 31.5K.** A quarter of it (8K) is guidance on how to use Project memory.
3. **The memory list — 19K.** The names and one-line summaries of 150 files in our Project memory, laid in at the start. Our own Project instructions are under 1K.

**Against the desktop seat (74.7K), the cloud adds about 40K of tool definitions and 19K of memory list, and saves about 8K of prompt.** That is the whole jump from 72K to 126K.

**When the four #300 subs were launched, the window stood at 250,519:**
- the boot: 126K (50%)
- the conductor's own thinking and writing, kept in the window: 56K (22%)
- files and notes read at the opener and since: 49K (20%)
- the memory list sent a second time: 19K (8%)

**Two surprises.**
- **The second memory list was identical to the first, byte for byte.** It is re-sent whenever anything in the memory store changes, even when the list itself shows no change. The opener's five memory edits cost 19K on your next message and bought nothing.
- **The conductor's thinking stays in its own window.** Thinking hard about your 15:58 message cost 22K. Writing this brief at the conductor cost another 15K. The subs' thinking stays in the subs' windows. Only their short stubs come back.

**Next step:** P should rank these levers. The sizes are in section 6.

---

## 1. The boot, itemised — 126,185 real

**Measured:** message 1 (`msg_…VxxaQUZG`, transcript row 26, 14:46:53 UTC): `input 2 + cache_creation 30,004 + cache_read 96,179 = 126,185`. The cache boundary splits the boot for free:
- **the prefix (tool definitions + system prompt) = 96,179 real, measured.** Evidence that the boundary sits exactly there: CLI bundle `/opt/node22/bin/claude` @198582500 puts the system prompt in `cacheScope:"org"` blocks with nothing dynamic before them, and the #300 system prompt carries no dynamic-boundary marker. Cached from an earlier same-day request with the same prefix (inference: #299, same date and project; the prompt holds the date and the project id).
- **the first user turn (every attachment + your "Good Morning!") = 30,006 real, measured.**

### 1a. How tape becomes real (rule 6)

Two ratios, both derived from this transcript's own usage fields:

| ratio | value | derivation |
|---|--:|---|
| `rt` — tool definitions (tape of `<function>{json}</function>`, `ensure_ascii=False`) | **0.983** | two-seat solve. Conductor prefix 96,179 = 65,765·rt + 21,698·rs. Sub-seat prefix 57,572 (the cache_read shared by subs B, C and D; A wrote it) = 57,722·rt + 571·rs. The subs load 60 of the same tool definitions byte-for-byte, drop 8 and add `SubagentHandback`. |
| `rs` — prose, markdown, tool results | **1.453** | same solve. **Cross-checked independently.** (i) The memory re-send, where the content is byte-identical, gives **1.431**. (ii) Every step of the session trace (section 2) reconciles as *retained output + user-side tape × rs* with residuals of −297 to +770 real per step. (iii) The desktop #294 boot's cache_creation side reconciles within ~33 real at the same ratio (section 4, inference). |

⚠ A constant tool-use preamble P that the snapshot does not show is absorbed into the ratios. With P = 500 the solve gives rs 1.457 and rt 0.974, so the split moves by under 600 real. Why tools come out near 1.0 but prose near 1.45 is **inference**. The likely reason is a more compact server-side rendering of JSON schemas. The ratios are empirical and the split does not depend on that explanation.

### 1b. The boot by group

| group | items | tape (cl100k) | real (est) | measured anchor |
|---|--:|--:|--:|---|
| system prompt | 9 | 21,698 | 31,531 |  |
| first user turn | 14 | 20,382 | 29,320 |  |
| tool: mcp__widgets__* | 17 | 16,550 | 16,268 |  |
| tool: core Claude Code tools | 20 | 14,972 | 14,720 |  |
| tool: Artifact* | 1 | 11,906 | 11,704 |  |
| tool: mcp__remote-devices__* | 7 | 6,414 | 6,306 |  |
| tool: mcp__claude-code-remote__* | 6 | 5,546 | 5,451 |  |
| tool: mcp__memory__* | 5 | 3,624 | 3,562 |  |
| tool: the rest (skills/onboarding/review UI) | 4 | 2,661 | 2,616 |  |
| tool: mcp__claude_ai__* | 7 | 2,224 | 2,186 |  |
| tool: Projects | 1 | 1,868 | 1,836 |  |
| **prefix: all tools + system prompt** | 77 | 87,463 | 96,180 | **cache_read 96,179** |
| **first user turn** | 14 | 20,382 | 29,320 | **cache_creation + input 30,006** |
| **BOOT** | | **107,845** | **125,500** | **126,185** |

**Residual: measured 126,185 − estimated 125,500 = +685 real (0.5%).** All of it sits in the first user turn (estimated 29,320 against 30,006 measured). The prefix reconciles by construction because its ratios are solved from it. Inference: the residual comes from attachment wrapper strings I rebuilt from the CLI bundle but could not reproduce to the byte.

### 1c. The system prompt by top-level section (3 strings + `cliPrefix`, from `prompt_snapshot` row 35)

| section (block) | tape | real (est, x1.453) |
|---|--:|--:|
| agentic_behavior | 7,707 | 11,199 |
| claude_behavior | 6,229 | 9,052 |
| <user_memory> guidance (block 2) | 5,637 | 8,191 |
| Your current remote execution environment (block 2) | 913 | 1,327 |
| Claude in Chrome browser automation (block 2) | 871 | 1,266 |
| Saving skills (block 1) | 200 | 291 |
| Model identity (block 2) | 115 | 167 |
| cliPrefix | 20 | 29 |
| (block 0 text outside tags) | 6 | 9 |
| **system prompt total** | **21,698** | **31,531** |

Second level, real (est): **claude_behavior** covers refusal handling 3,281 · product information 1,665 · tone and formatting 1,303 · user wellbeing 1,183 · evenhandedness 461 · cyber 301 · knowledge cutoff 283 · reminders 257 · mistakes 198 · legal 90. **agentic_behavior** covers the_work 3,785 · workspace_and_tools 4,978 · how_a_task_runs 1,662 · situation 520 · send_user_message_tool 238. Inside workspace_and_tools: device_bridge 1,072 · browsers 834 · artifacts 683 · skills 612 · where_files_live 356 · workspace 327 · desktop_computer_use 230 · delivering_files 214 · scheduled_tasks 199 · web_content 154 · connectors 135 · questions_and_task_list 113. **<user_memory>** covers two privacy_requirements blocks (895 + 1,384 tape), memory_application 1,227 tape, Writing 1,454 tape and Reading 295 tape.

### 1d. Every loaded tool, by family (68 loaded; 114 more are deferred and cost only their names)

| family | tool | tape (cl100k) | real (est, x0.983) |
|---|---|--:|--:|
| **core Claude Code tools** (20) | *subtotal* | **14,972** | **14,720** |
| | ScheduleWakeup | 1,849 | 1,818 |
| | TaskUpdate | 1,526 | 1,500 |
| | AskUserQuestion | 1,264 | 1,243 |
| | SendUserFile | 1,227 | 1,206 |
| | TaskCreate | 1,129 | 1,110 |
| | Grep | 1,018 | 1,001 |
| | Bash | 933 | 917 |
| | Agent | 903 | 888 |
| | Skill | 762 | 749 |
| | Read | 658 | 647 |
| | ToolSearch | 603 | 593 |
| | ListAgents | 474 | 466 |
| | WebFetch | 444 | 436 |
| | ReadNotifications | 441 | 434 |
| | Edit | 349 | 343 |
| | RefreshMcpTools | 345 | 339 |
| | WebSearch | 316 | 311 |
| | SendUserMessage | 252 | 248 |
| | Write | 244 | 240 |
| | Glob | 235 | 231 |
| **Artifact*** (1) | *subtotal* | **11,906** | **11,704** |
| | Artifact | 11,906 | 11,704 |
| **Projects** (1) | *subtotal* | **1,868** | **1,836** |
| | Projects | 1,868 | 1,836 |
| **mcp__widgets__*** (17) | *subtotal* | **16,550** | **16,268** |
| | mcp__widgets__places_map_display_v0 | 2,374 | 2,334 |
| | mcp__widgets__chart_display_v0 | 2,257 | 2,219 |
| | mcp__widgets__quiz_display_v0 | 1,150 | 1,130 |
| | mcp__widgets__recipe_display_v0 | 1,036 | 1,018 |
| | mcp__widgets__places_search | 1,033 | 1,015 |
| | mcp__widgets__message_compose_v1 | 921 | 905 |
| | mcp__widgets__places_list_display_v0 | 833 | 819 |
| | mcp__widgets__itinerary_display_v0 | 831 | 817 |
| | mcp__widgets__step_card_display_v0 | 775 | 762 |
| | mcp__widgets__comparison_card_display_v0 | 748 | 735 |
| | mcp__widgets__product_carousel_display_v0 | 719 | 707 |
| | mcp__widgets__options_card_display_v0 | 717 | 705 |
| | mcp__widgets__translation_display_v0 | 703 | 691 |
| | mcp__widgets__fetch_sports_data | 701 | 689 |
| | mcp__widgets__link_preview_display_v0 | 689 | 677 |
| | mcp__widgets__featured_card_display_v0 | 664 | 653 |
| | mcp__widgets__weather_fetch | 399 | 392 |
| **mcp__claude_ai__*** (7) | *subtotal* | **2,224** | **2,186** |
| | mcp__claude_ai__launch_extended_search_task | 945 | 929 |
| | mcp__claude_ai__read_conversation | 295 | 290 |
| | mcp__claude_ai__image_search | 251 | 247 |
| | mcp__claude_ai__current_time | 238 | 234 |
| | mcp__claude_ai__conversation_search | 213 | 209 |
| | mcp__claude_ai__recent_chats | 161 | 158 |
| | mcp__claude_ai__end_conversation | 121 | 119 |
| **mcp__claude-code-remote__*** (6) | *subtotal* | **5,546** | **5,451** |
| | mcp__claude-code-remote__create_trigger | 1,741 | 1,711 |
| | mcp__claude-code-remote__update_trigger | 1,206 | 1,186 |
| | mcp__claude-code-remote__list_triggers | 977 | 960 |
| | mcp__claude-code-remote__send_later | 685 | 673 |
| | mcp__claude-code-remote__fire_trigger | 475 | 467 |
| | mcp__claude-code-remote__delete_trigger | 462 | 454 |
| **mcp__memory__*** (5) | *subtotal* | **3,624** | **3,562** |
| | mcp__memory__memory_write | 1,022 | 1,005 |
| | mcp__memory__memory_str_replace | 976 | 959 |
| | mcp__memory__memory_append | 934 | 918 |
| | mcp__memory__memory_list | 447 | 439 |
| | mcp__memory__memory_read | 245 | 241 |
| **mcp__remote-devices__*** (7) | *subtotal* | **6,414** | **6,306** |
| | mcp__remote-devices__device_bash | 1,517 | 1,491 |
| | mcp__remote-devices__device_stage_files | 1,066 | 1,048 |
| | mcp__remote-devices__device_list_dir | 909 | 894 |
| | mcp__remote-devices__device_commit_files | 781 | 768 |
| | mcp__remote-devices__list_legacy_live_artifacts | 743 | 730 |
| | mcp__remote-devices__device_request_delete_permission | 728 | 716 |
| | mcp__remote-devices__device_request_folder_access | 670 | 659 |
| **the rest (skills/onboarding/review UI)** (4) | *subtotal* | **2,661** | **2,616** |
| | propose_skills | 923 | 907 |
| | ReportFindings | 702 | 690 |
| | SuggestSkills | 603 | 593 |
| | ShowOnboardingRolePicker | 433 | 426 |
| **all 68 loaded tools** | | **65,765** | **64,649** |

**Deferred (names only, 1,217 tape ≈ 1,768 real):** 43 computer-use, 22 Claude in Chrome, 17 built-in browser, 28 core/other (Artifact comments/data, Cron×3, plan mode, worktrees, plugins, skills search, MCP resources, notebook, push, monitor, task get/list/stop, SendMessage, connectors), 2 visualize, 1 memory (`memory_delete`), 1 remote-devices. **No Claude Docs tool is present, loaded or deferred.** The boot went 127,661 (#298) → 126,178 (#299) → 126,185 (#300). Inference: part of that −1.5K is the Docs connector's absence.

### 1e. The first user turn (attachments, rendered as the model sees them)

| item | tape | real (est) | ratio used |
|---|--:|--:|---|
| att:cowork_memory_context | 13,306 | 19,038 | re-send ratio |
| att:skill_listing | 2,857 | 4,152 | rs |
| att:deferred_tools_delta | 1,217 | 1,768 | rs |
| att:session_context | 769 | 1,117 | rs |
| att:mcp_instructions_delta | 745 | 1,083 | rs |
| att:agent_listing_delta | 594 | 863 | rs |
| att:environment | 275 | 400 | rs |
| att:remote_session_change | 195 | 283 | rs |
| att:file | 135 | 196 | rs |
| device-link reminder (this session is linked to the Mac) | 114 | 166 | rs |
| user turn: Dave's first message + timezone line | 83 | 121 | rs |
| att:model | 47 | 68 | rs |
| att:total_tokens_reminder | 23 | 33 | rs |
| att:date | 22 | 32 | rs |
| **first user turn total** | **20,382** | **29,320** | measured **30,006** (cache_creation 30,004 + input 2) |

⚠ **The brief's attachment figures were tapes of the JSON, not of what the model sees.** Rendered, the memory snapshot is 13,296 tape, not 14,680 (the JSON escapes add ~1.4K). The skill listing is 2,857, not 3,112. The deferred list is 1,217, not 2,601: the JSON carries every name twice, in `addedNames` and in `addedLines`.

**Inside the memory snapshot (13,296 tape, row 18):** profile 123 · preferences 198 · **listing 12,822** (150 file lines at ~84 tape each, plus "… and more (showing 150 — memory_list for the rest)"). **The 48-character project path prefix repeats on all 150 lines: 28 tape × 150 = 4,200 tape (~6.1K real), 32% of the listing.** Lane D owns the store; this is the attribution only.

---

## 2. The opener and the session, message by message

Fill is REAL: `input + cache_creation + cache_read` per distinct `message.id`. Each delta splits into the prior message's `output_tokens` (measured, and fully retained, thinking included) plus the user-side items sent since (tape × rs). The residual is what is left over.

| # | UTC | fill (real) | delta | = retained prior output | + user-side tape (~real) | residual | what the step did |
|--:|---|--:|--:|--:|--:|--:|---|
| 1 | 14:46:53 | 126,185 | +126,185 | 0 | 20,382 (~29,618) | +96,567 = the prefix (tools + system, 96,179 measured) + 388 | boot; then ls mount, memory_read index.md, Skill dave-voice |
| 2 | 14:46:57 | 133,075 | +6,890 | 595 | 4,129 (~6,000) | +295 | results in: mount listing, index.md, dave-voice body; then ls repo |
| 3 | 14:47:01 | 135,728 | +2,653 | 370 | 1,323 (~1,923) | +360 | repo listing in; then cat _HANDOFF-150 |
| 4 | 14:47:07 | 143,584 | +7,856 | 249 | 5,139 (~7,468) | +139 | handoff in; then cat _CHAIN.md, memory_list, _checkin.py |
| 5 | 14:47:15 | 157,635 | +14,051 | 706 | 8,981 (~13,051) | +294 | chain, memory_list page, checkin (NO TRANSCRIPT FOUND) in; then hook read, ensure_env, transcript ls |
| 6 | 14:47:23 | 161,168 | +3,533 | 620 | 1,914 (~2,781) | +132 | hook in; then fill check, memory_read archive shard + presentation area |
| 7 | 14:47:55 | 172,784 | +11,616 | 922 | 6,829 (~9,924) | +770 | archive + area in; then memory_write hook file, memory_append archive, str_replace area |
| 8 | 14:48:18 | 179,611 | +6,827 | 6,529 | 148 (~215) | +83 | write confirmations in; then str_replace index.md |
| 9 | 14:48:33 | 180,384 | +773 | 679 | 71 (~103) | -9 | then str_replace index.md (cut) |
| 10 | 14:48:37 | 181,821 | +1,437 | 1,340 | 74 (~108) | -11 | then str_replace index.md, git log + rulings |
| 11 | 14:48:43 | 184,309 | +2,488 | 497 | 1,374 (~1,997) | -6 | git/rulings in; then fill check |
| 12 | 14:49:00 | 184,982 | +673 | 531 | 120 (~174) | -32 | then grep for the ask |
| 13 | 14:49:35 | 187,863 | +2,881 | 1,279 | 1,088 (~1,581) | +21 | grep in; the first beat reply (end of turn 1) |
| 14 | 15:01:46 | 211,454 | +23,591 | 4,220 | 13,535 (~19,668) | -297 | Dave's #300 message + memory snapshot RE-SENT (identical); long thinking; Bash |
| 15 | 15:02:05 | 234,169 | +22,715 | 21,985 | 487 (~708) | +22 | thinking of 14 retained; prompt_snapshot inspection |
| 16 | 15:03:49 | 235,602 | +1,433 | 1,004 | 273 (~397) | +32 | then BRIEF-300 written in-seat (heredoc) + SendUserMessage |
| 17 | 15:04:26 | 250,519 | +14,917 | 14,785 | 46 (~67) | +65 | brief turn retained; four Agent launches (A-D) |

**The three bands at message 17 (250,519 real):**
- **BOOT** 126,185 (50.4%).
- **OPENER, msgs 2–13: +61,678 (24.6%).** Retained outputs 14,317 + reads and results ~45,323 (31,190 tape) + residual 2,036. Largest reads: `_CHAIN.md` ~10.8K · `MEMORY-ARCHIVE-3.md` + presentation area ~9.8K · `_HANDOFF-150` ~7.4K · `index.md` ~3.1K · #299 hook ~2.5K · dave-voice skill body ~2.2K · memory_list page ~2.2K · git log + rulings ~1.9K · repo listing ~1.9K · "the ask" grep ~1.5K. The hook-placement turn's own output (the memory_write, append and edit calls, plus thinking) is 6,529. `_checkin.py` returned `NO TRANSCRIPT FOUND` (row 60), so it cost almost nothing and measured nothing.
- **RUNNING, msgs 14–17: +62,656 (25.0%).** Retained outputs 41,994, of which your "think hard" answer's reasoning is 21,985 and the in-seat brief write is 14,785. Memory re-send ~19,038. Your message plus tool results ~1.8K. Residual −178.
- **Across the window, the conductor's own retained outputs total 56,311 real (22.5%).** That is more than every file the opener read put together.

**The re-send, pinned down:**
1. **Byte-identical.** Row 18 (14:46:47) and row 130 (14:58:11) have the same content, sha256 `8388cdd7538824d9…`. The `version` changes: `e53a76267c2f` → `e87e7f1c401e`.
2. **Why nothing visible changed.** The listing is alphabetical and shows the first 150 files. `index.md`, `MEMORY-ARCHIVE-3.md` and `areas/presentation-friday-25th-288.md` were edited and are in view, but a line shows path, source and description, not size or date. So body edits leave the line unchanged. The new `wrap-299-…md` sorts after the 150th line (`wrap-281-…`) and lands out of view.
3. **The trigger is the version, not the content.** The CLI bundle's `pG()` (@200301575) re-attaches when `r?.version !== n.version`. It never compares content.
4. **It fires only at a user turn.** The writes landed at msgs 7–10 (14:48:04–14:48:38). No snapshot arrived during msgs 8–13 of the same turn. It arrived with your next message (row 130). The code agrees: the per-turn fetch runs for the main thread only (`g8r`, `Js(r)!=="main"` returns early). That is also why the subs never receive a snapshot.

**Thinking is retained in full.** Msg 15's delta is +22,715 against msg 14's 21,985 output tokens plus a 464-tape result. Msg 17's delta is +14,917 against msg 16's 14,785. Msg 14's delta fits the same model across the user-turn boundary: 4,220 retained plus the snapshot at 1.431. A model that drops the thinking would need an implausible ratio of 1.68.

---

## 3. Top 25 by cost, and what brings each in

Real figures are measured for outputs and estimated (tape × ratio) for everything else. The **brought in by** column is **inference from names and placement**. Whether a switch exists is lane B's to establish.

| # | real | band | item | brought in by |
|--:|--:|---|---|---|
| 1 | 21,985 (measured) | running | output of msg 14: conductor reasoning on Dave's "think hard" message (thinking retained) | the conductor thinking in-seat (retained in window) |
| 2 | 19,038 (est) | running | memory snapshot RE-SENT (byte-identical) | feature: Project memory, triggered by the opener's store writes |
| 3 | 19,038 (est) | boot | memory snapshot at boot (cowork_memory_context) | feature: Project memory (cloud leg); content = our store listing |
| 4 | 14,785 (measured) | running | output of msg 16: writing BRIEF-300 in-seat + message + thinking | our procedure: brief written at the conductor |
| 5 | 11,704 (est) | boot | Artifact | feature: Artifacts |
| 6 | 11,199 (est) | boot | agentic_behavior | harness: agent/Cowork base prompt (fixed, inference) |
| 7 | 10,794 (est) | opener | cat _CHAIN.md | our own instruction (step 2) |
| 8 | 9,839 (est) | opener | memory_read MEMORY-ARCHIVE-3 + presentation area | opener: conductor's judgment (index pointers) |
| 9 | 9,052 (est) | boot | claude_behavior | harness: claude.ai base prompt (fixed) |
| 10 | 8,191 (est) | boot | <user_memory> guidance (block 2) | feature: Project memory |
| 11 | 7,434 (est) | opener | cat _HANDOFF-150 | our own instruction (step 1) |
| 12 | 6,529 (measured) | opener | output of msg 7: hook placement turn: memory_write/append/str_replace + thinking | our own instruction (step 6) |
| 13 | 4,220 (measured) | opener | output of msg 13: the first beat: reply + thinking | our own instruction (first beat in dave-voice) |
| 14 | 4,152 (est) | boot | skill listing (22 skills) | setting: skills enabled (22; four are Dave's own) |
| 15 | 3,094 (est) | opener | memory_read index.md | our own instruction (step 3) |
| 16 | 2,539 (est) | opener | cat #299 WRAP-MEMORY-HOOK.md | our own instruction (step 6) |
| 17 | 2,334 (est) | boot | mcp__widgets__places_map_display_v0 | feature: in-chat widgets (inference) |
| 18 | 2,219 (est) | boot | mcp__widgets__chart_display_v0 | feature: in-chat widgets (inference) |
| 19 | 2,209 (est) | opener | dave-voice skill body | our own instruction (reply in dave-voice) |
| 20 | 2,151 (est) | opener | memory_list page | our own instruction (step 3) |
| 21 | 1,892 (est) | opener | git log + rulings read | opener: conductor's judgment |
| 22 | 1,889 (est) | opener | ls repo root | opener: conductor finding the handoff |
| 23 | 1,836 (est) | boot | Projects | feature: Projects (claude.ai Project binding) |
| 24 | 1,818 (est) | boot | ScheduleWakeup | feature: scheduled tasks (inference) |
| 25 | 1,768 (est) | boot | deferred tool names (114) | harness: tool search (114 deferred names) |

**The same boot grouped by the feature that brings it in** (real est; the mapping is INFERENCE):

| feature (by name) | real (est) | parts |
|---|--:|---|
| Project memory (snapshot, guidance, 5 tools, MCP note) | 31,498 | snapshot 19,038, guidance 8,191, tools 3,562, mcp_note 695, deferred 12 |
| Widgets (17 mcp__widgets__ tools) | 16,269 | tools 16,269 |
| Artifacts (tool, prompt section, skills, deferred names) | 12,708 | tool 11,704, prompt 683, skills 312, deferred 9 |
| Mac link (remote-devices tools, bridge + env sections, link and folder notes) | 9,082 | tools 6,305, prompt 2,399, deferred 16, link_note 166, folders 196 |
| Scheduled tasks (triggers, ScheduleWakeup, Cron names, prompt section) | 7,486 | tools 7,269, prompt 199, deferred 17 |
| Skills (listing, Skill/propose/suggest tools, prompt sections) | 7,312 | listing 4,152, tools 2,249, prompt 902, deferred 9 |
| claude.ai chat tools (search chats, research, images, time, end) | 2,186 | tools 2,186 |
| Browsers + computer use (Chrome section, MCP note, 22+43+17 names, browser skills) | 5,172 | prompt 2,329, mcp_note 343, deferred 1,473, skills 1,026 |
| Projects tool | 1,836 | tool 1,836 |
| Onboarding + review UI (role picker, ReportFindings) | 1,116 | tools 1,116 |
| Tasks (TaskCreate/TaskUpdate) | 2,610 | tools 2,610 |
| Our Project instructions (session_context attachedProject) | 939 | text 939 |

Left over, fixed as far as the names show: claude_behavior 9,052 · agentic_behavior minus its feature subsections ~7,570 · core tools 9,541 (Agent, AskUserQuestion, Bash, Edit, Glob, Grep, ListAgents, Read, ReadNotifications, RefreshMcpTools, SendUserFile, SendUserMessage, ToolSearch, WebFetch, WebSearch, Write) · agent roster 863 · environment, model, date and attribution lines ~800.

---

## 4. The two seats lined up — desktop #294 against cloud #300

The desktop figures come from the repo. `knowledge/_gauge_tokens.py:179–180` has boot 74,656 = input 2 + cache_creation 38,612 + cache_read 36,042. `:205` has systemPrompt 4 strings 26,984 tape = 7,901 · 8 · 13,662 · 5,413, `<env>` 10,095 of it. `:206` has opener attachments 6,719 tape (skills 2,717 · MCP blocks 2,400 · deferred names 986 · agents 552 · rest 64). `:209` has residual ≈40,953 by mixed-unit subtraction. #295 read 72,768 (`:337`, `:351`, the ruled ceiling).

**★ The desktop's 8-tape string is `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__`.** It is exactly 8 cl100k tokens, and the CLI bundle defines `$L="__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__"` (@191053600). Blocks before it are cached `global`, blocks after it `org` (@198582500). **This splits the desktop boot (inference):**
- **cache_read 36,042** = tools + the 7,901-tape static block (×1.453 = 11,480) ⇒ **desktop tool definitions ≈ 24,530 real**. The cliPrefix and header take ~30.
- **Check:** cache_creation 38,614 = dynamic prompt 19,075 tape (×1.453 = 27,716) + attachments 6,719 tape (9,763) + ~1,135 for the first message and small lines. That fits, and the leftover is the right size.

| component (real) | desktop #294 | cloud #300 | the cloud adds |
|---|--:|--:|--:|
| tool definitions | ~24,530 (inference, cache boundary) | ~64,648 (est) | **≈ +40,100** |
| system prompt | ~39,208 (26,984 tape × 1.453) | ~31,531 (est) | **≈ −7,700** |
| memory snapshot | 0 recorded at boot (`2026-09-21-294-G…md:238–241`) | 19,038 (measured by difference) | **≈ +19,000** |
| other first-turn items | ~10,900 | ~10,968 (30,006 − 19,038) | ≈ 0 |
| **boot, measured** | **74,656** | **126,185** | **+51,529** |

Cloud-only families by name (inference: none appears in the desktop seat's list in `notes/_lanes/293/NOTE-boot-has-three-bands.md`) add ~34.7K real: widgets 16,269 · the Mac link 6,305 · triggers 5,452 · the rest (skills, onboarding and review UI) 2,616 · claude.ai chat tools 2,186 · Projects 1,836. The other ~5K of the +40K would be a larger core set (inference).

⚠ **Caveats.** The desktop reading is n=1 and may have run a different model and tokenizer. On the desktop "laptop" leg the CLI filters memory snapshots out of some transcript paths (`I4e`, @205188476), so "0 recorded" may not prove "0 sent". The 74,656 total, though, leaves no room for a 19K snapshot beside ~24.5K of tools. **UNPROVEN either way.**

---

## 5. What this corrects or sharpens in the brief

1. **"Cloud is the source."** HOLDS for the boot: +51.5K, being +40K of tools and +19K of memory snapshot, less 7.7K of prompt. It does NOT hold for the running band. The biggest single item in the window is the conductor's own retained thinking, which the seat does not cause.
2. **"Store writes trigger the re-send."** HOLDS, more sharply. The version triggers it, not the content. It fires at the next user turn even when the rendered list is identical. Any writer counts, sub or other chat (inference from the code: the version is the store's).
3. **"prompt_snapshot equals what is billed."** HOLDS to within 0.5% at boot and ±770 real per step, under ratios derived from the transcript itself. The snapshot is written after the first call (row 35). Row 22 has no `tools`. Message 2 read message 1's whole prompt from cache (cache_read 126,183), so the tools and prompt were byte-identical across the two calls.
4. **The brief's attachment tapes** were JSON tapes (section 1e). Use the rendered figures.
5. **The conductor is at 250,519 real at message 17**, not ~212K. Inference: when the four stubs land, its next turn reads ~253K (250,519 + 1,714 retained + four stubs).

## 6. What the sizes suggest (INFERENCE, handed to B, C, D, X and P; nothing enacted)

| lever | size, real | status |
|---|--:|---|
| No memory writes in a chat that continues (hook at the wrap seat, last act) | **−19,038 per re-send** | size measured; the mechanism is from code, see section 2 |
| Keep heavy thinking and long writes off the conductor (subs think; a sub writes the brief) | **up to −36,770** (msgs 14 + 16 outputs) | measured sizes; the saving is inference |
| Opener reads on demand (chain, handoff, archive shard, index, hook, list, voice) | **up to ~38,000** | measured reads; lane C |
| Project memory for Apollo (snapshot, guidance, tools, note) | **up to 31,498 at boot** | lane B: is there a per-project switch, and what does it remove? |
| Loaded families: widgets 16,269 · Artifacts 12,708 · scheduled tasks 7,486 · skills 7,312 · chat tools 2,186 | up to ~46,000 | lane B: which are switchable |
| Seat: desktop boot 74,656 against cloud 126,185 | **−51,529** | lane B: is the desktop seat still offered |
| Harness asks, via feedback, not ours: defer widgets the way Chrome is deferred (~15 real per deferred name against 957 per loaded widget); re-send memory only when the rendered content changes | 16K; 19K per re-send | UNPROVEN whether Anthropic would act |

## 7. Receipts and replay

- **Transcript:** `/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl` (cloud container). Rows cited are 0-based line numbers: 18 and 130 (memory snapshots), 22 and 35 (`prompt_snapshot`), 26 (message 1).
- **Sub transcripts:** `…/d75f51cc-…/subagents/agent-*.jsonl`. The first-message cache_read is 57,572 for B, C and D. A has 0 (it wrote the cache).
- **CLI bundle:** `/opt/node22/bin/claude`, byte offsets as cited (read with python `mmap`).
- **Repo:** `knowledge/_gauge_tokens.py:179–209, 337, 351` · `notes/_subreports/2026-09-21-294-G-enact-d4-d5-d6-d7.md:230–265` · `notes/_lanes/298/DAVE-WORDS-AND-BOOT-FINDING-2026-09-23.md` · `notes/_GAUGE-LOG.md:4105, 4131` (the #297 and #298 boots; #298's read 65,194 ≈ tools est 64,648 + cliPrefix, within 0.8%, inference) · memory `areas/boot-three-bands-293.md` (read-only).

**REPLAY-THESE** (in the cloud container, after `pip install tiktoken --break-system-packages`; copy the scripts from `notes/_lanes/300/A/` via `device_bash cat`):
1. `python3 attribute_window.py /root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl --csv out` prints the boot split, the ratios, the reconciliation and the trace.
2. `python3 features.py <same path>` prints the feature groups, and `python3 top25.py` the ranked items. Both need `out/attribution.json` from step 1.
3. The re-send identity check: `python3 -c "import json;R=[json.loads(l) for l in open('<path>')];print(R[18]['attachment']['content']==R[130]['attachment']['content'])"` prints `True`.

## 8. Spend

Hand-summed from `…/subagents/agent-a3b362defba4eb634.jsonl` (this lane) at filing, message 59: first fill 66,307, last fill 267,134 real (input side). Cumulative input side is 9,421,377, almost all of it cache reads. `output_tokens` recorded sum to 3,676; this sub's usage lines appear to leave out thinking, so treat that figure as a floor. A few messages follow the filing.
