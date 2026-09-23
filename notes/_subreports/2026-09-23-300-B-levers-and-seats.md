# #300 Lane B — Levers and seats: what switches the cloud boot off, and where else the conductor could sit

provenance: 300 · lane B · 2026-09-23 · Opus 5.5 subagent in the cloud container · read-only on the repo apart from this report and `notes/_lanes/300/B/` · no Project-memory writes · no git.

---

## For Dave — the answer first

**Most of the 126K cloud boot is harness you cannot switch off in Settings.** About half of it is tool definitions the cloud seat loads before you speak. Only a few families have a switch you own.

**The switches you own are small unless they hit your client work.**
- **Claude in Chrome off + computer use off**: about **3,700 tokens**. Your client work loses those two features until you switch them back.
- **Pause memory**: about **31,700 tokens at boot**, plus about **23,600 every time the memory store changes mid-session**. But the memory switch covers your whole account. Every chat and project, client work included, stops using and making memories while it is paused. It can be switched back on. Never press "Reset" — that deletes everything.

**One switch has no side effects, and it is worth testing first.** A per-conversation setting called **Tool access → On demand** keeps tools out of the boot until Claude looks them up. It is documented for connectors. No source says whether it also covers the built-in families: widgets, memory, scheduled tasks and the link to your Mac. If it does, it saves **up to ~33,500 tokens**. If it doesn't, it saves nothing. It takes one fresh conversation to find out, and nothing else on the account changes.

**The biggest lever is where the conductor sits, not a setting.** Claude Code on your Mac, opened in the repo, boots at roughly **30,000 tokens**, about **96,000 less than today**. Your skills (dave-voice and the rest) sync over automatically, and it reads the repo's AGENTS.md by itself. It gives up the claude.ai Project memory and this chat window. You would read the work either in the desktop app's Code tab or in a browser or phone through Remote Control.

**The old local Cowork seat (the ~72K boot) is gone for your plan.** Cowork sessions now run in the cloud on every surface. Once an account has the merged chat-and-Cowork experience, it cannot switch back.

**What not to do.**
- Don't turn off "Code execution and file creation" to get rid of the 12K Artifact tool. That switch also kills files, code and skills.
- Don't switch off the Word, PowerPoint, Excel and PDF skills. Your client decks need them, and the saving is only ~1K.

**Next step:** open one fresh conversation in the Apollo project, set Tool access to On demand before the first message, send "boot probe", and read the first-turn fill (commands in §8).

---

## 1. How I measured (units, and why they are not cl100k)

**Tape** = cl100k (tiktoken) counts of the payload the transcript records: the `prompt_snapshot` attachment (system prompt + 68 tool schemas) and the boot attachments. Tape is an estimate.

**Real** = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` of the first assistant message, per distinct `message.id`.

**The scale is two registers, not one ratio.** I fitted two unknowns (real per cl100k for tool JSON; real per cl100k for prose) to two measured boots:

| boot | real (usage) | tool tape | prose tape | receipt |
|---|---:|---:|---:|---|
| conductor #300, message 1 | 126,185 | 66,903 | 41,723 | `d75f51cc….jsonl` line 26 (usage), line 35 (snapshot) |
| this lane's own sub, message 1 | 66,336 | 58,706 | 5,967 | `subagents/agent-a15bc00f2eaf18c75.jsonl` line 10 |

- **Fit:** tools **×0.983** real per cl100k; prose **×1.449** real per cl100k.
- **Independent check.** Predict the #300 memory re-send from the prose ratio: 15,429 tape (previous visible reply 1,882 + Dave's message 234 + reminder 17 + rendered snapshot 13,296) × 1.449 = **22,349 predicted**, against **23,591 measured**. That is 0.947, so prose is probably ×1.45–1.53.
- A single ratio would be wrong both ways. The conductor as a whole is ×1.147 and the sub is ×1.026, because the conductor is prose-heavy.
- The repo's gauge records Opus-5-era prose ratios of 1.486–1.664 (`knowledge/_gauge_tokens.py` docstring, lines 24–29). That is the same direction.
- Receipts:
  - `python3 notes/_lanes/300/B/levers_measure.py` (prints the fit and the check).
  - The snapshot's memory block rendered as its `content` string = 13,296 tape. As JSON it is 14,671; the brief's 14,680 is the JSON form.

**The exact route failed.** I tried the free `count_tokens` endpoint, the method the repo's gauge rules as "THE UNIT" (`_gauge_tokens.py:24,50`):
1. `knowledge/_gauge_tokens.py::read_key()` (lines 406–417) only accepts a line starting `ANTHROPIC_API_KEY=`. `API-KEY.txt` holds a bare `sk-ant-…` line, so read_key() returns None.
2. With the bare line, the API answered **HTTP 401 "API key is invalid."** on 2026-09-23.
   - Script: `notes/_lanes/300/B/real_counts.py`. The key was never printed.
   - Consequence for every lane: the gauge's real-token path cannot run today. See §6.

Token counting is free per platform.claude.com (read 2026-09-23), so this is worth fixing.

---

## 2. The harness, family by family — what switches each off

Sizes come from the conductor's own boot payload. Real = tape × 0.983 (tools) or × 1.449 (prose).

- **"Switch"** says where it lives and at what scope. **Account** = every chat and project on Dave's claude.ai account. **App** = the desktop app on this Mac. **Conversation** = only the chat it is set in.
- **"Removes the tools?"**: *documented* means a source says the feature stops. That the harness then drops the tool schemas at the next boot is **INFERENCE** unless marked *precedent*.
- **Precedent.** After Dave blocked Claude Docs, the next cloud boot arrived without the Docs tools and 1,483 real lighter: 127,661 → 126,178 (`notes/_lanes/299/WRAP-BRIEF.md:6`). Not all of that difference need be Docs, and the line does not name the switch he used. It is still evidence that account-level switches remove tools at the next boot.

### 2a. The table

| # | Family / block (what the boot carries) | tape | **real** | Switch, scope, source | Removes the tools? | Apollo loses | Dave's other work loses | Undo |
|---|---|---:|---:|---|---|---|---|---|
| 1 | **Memory**: 5 memory tools 3,666 + `<user_memory>` rules 5,637 + memory snapshot 13,296 + memory server note 478 + 1 deferred name | 23,084 | **31,730** at boot; **+23,591 per store change** mid-session (measured) | Settings › Memory › "Generate memory from chats" → **Pause**. **Account**. Global, with no per-project switch in the three articles read [S1, S19, S20]. | Documented: paused memory is not used or made [S1]. System prompt: this setting "is what stops memory from being used and updated". Tool drop = INFERENCE; test with one boot. | The memory accelerator (index, hooks, archive shards). The repo stays the record. The opener's memory ritual has to go (lane C). | **All** chats and projects stop using and making memories while paused, client projects and Cowork tasks included [S1]. | Unpause restores it. **Reset deletes everything, including project memories** [S1]. |
| 2 | **Chat search**: `conversation_search`, `read_conversation`, `recent_chats` | 660 | **649** | Settings › Memory › "Search and reference chats" off. **Account** [S1]. | INFERENCE (these are the chat-search tools). | Past-chat lookup (rarely used; the repo is the record). | All chats lose past-chat search. | Toggle back. |
| 3 | **Widgets**: 17 tools (maps, weather, recipes, sports, cards, quiz…). Largest family. | 16,826 | **16,540** (16,191 net of names if deferred) | **No switch for Pro/Max.** Weather and recipes "require web search", and the merged experience has "no web search toggle" [S6, S14, S4]. Team/Enterprise owners can turn maps and image search off org-wide [S8]; this account is Max (`notes/2026-07-26-memento-dream-pass-scope-v2.md:8`). Possibly removable by Tool access (row 15). | Fixed unless row 15 works. | Nothing: Apollo never uses them. | — | — |
| 4 | **Artifact tool** (+ `<artifacts>` + 3 artifact skills). Largest single tool: 11,967. | 12,652 | **12,753** | **No separate switch on Pro/Max.** Only "Code execution and file creation", which also removes files, code and skills: "We no longer support artifacts without Code execution and file creation enabled" [S9]. Claude Design/Slides/Docs switches in Settings › Capabilities may shrink the tool text (INFERENCE; the Docs precedent removed Docs tools, not this tool). | Fixed on the cloud seat. | Apollo publishes to the repo, not artifacts. | Turning code execution off would break client work too. Don't. | — |
| 5 | **Scheduled tasks**: 6 trigger tools + `<scheduled_tasks>` | 5,836 | **5,799** | **No switch found** for Pro/Max. Scheduled tasks "run remotely" [S16]. | Fixed. | — | — | — |
| 6 | **Link to the Mac**: 7 loaded bridge tools + `<device_bridge>` + "Working with the user's computer" + `<where_files_live>` + 1 deferred name | 8,203 | **8,832** | Only by **not linking** the conversation (no desktop app). Local file access needs the desktop app open and the session started on desktop [S2]. | INFERENCE. | **The repo.** Viable only if the repo leaves the Mac (§4.3). | — | — |
| 7 | **Other claude.ai tools**: Research launcher 978, image search 248, current time 235, end conversation 118 | 1,579 | **1,552** | Research has a per-chat on/off (+ › Research or `/deep-research`) [S15, S4], but the tool loads either way. Image search rides on web search [S14]. | Fixed. | — | — | — |
| 8 | **Projects tool + Project instructions** | 2,721 | **3,031** | Run the conductor **outside the Project**. **Conversation** scope. | Tool drop = INFERENCE. | The Project instructions (can move into AGENTS.md or the first message). The memory scope changes: outside a Project the snapshot would be account memory, not Project memory (lane D). | None. | Start the next session back in the Project. |
| 9 | **Claude in Chrome**: 22 deferred names + Chrome block 871 + server note 236 + 2 skill entries | 1,672 | **2,422** | Settings › Connectors › Claude in Chrome off. Or Settings › Cowork › Preferred browser → built-in [S12]. **Account**. | INFERENCE (Docs precedent says likely). | Nothing: renders are headless Playwright on the mount. | Client work loses Chrome automation with his sign-ins. | Toggle back. |
| 10 | **Computer use**: 43 deferred names + `<desktop_computer_use>` + 1 skill entry | 854 | **1,237** | Desktop app › Settings › General › "Enable computer use" off [S13]. **App** (this Mac). | INFERENCE. | Nothing (Apollo uses the bridge shell). | Client work loses screen control. | Toggle back. |
| 11 | **Built-in browser**: 17 deferred names + `<browsers>` + 1 skill entry | 1,030 | **1,492** | **No off switch found.** Only "Preferred browser" [S12]. | Fixed. | — | — | — |
| 12 | **Custom visuals** (2 deferred names) | 18 | ~26 | None. "You don't need to turn anything on" [S7]. | Fixed (negligible). | — | — | — |
| 13 | **Skills listing** (22 entries; ~1,330 real of it is already counted in rows 4 and 9–11) | 2,835 | **~4,100** | Customize › Skills, per-skill toggles. **Account**, and the settings also sync into Claude Code and the Office add-ins [S11]. Plugin skills go by uninstalling the plugin. | Documented for the listing. | Only toggle what Apollo doesn't use: the plugin-management pair (204 real) and the browser/computer entries (counted in rows 9–11). | Office skills (docx/pptx/xlsx/pdf = **1,097 real**) serve client decks. **Not advised.** | Toggle back. |
| 14 | **Third-party connectors** | 0 | **0** | Per-chat connector toggles and Tool access exist [S17, S5], but **none were loaded or deferred at this boot** (deferred list = first-party servers only). | — | — | — | — |
| 15 | **Tool access = On demand**: all 42 loaded MCP tools (widgets, memory, scheduled, bridge, claude.ai) | 34,390 | **up to 33,522** (widgets alone 16,191) | "+" › Connectors › Tool access › **On demand**. **Conversation**: "Your selection only applies to that conversation." Documented for **connectors** [S5]. | **UNTESTED** for built-in families. Claude Code's own mechanism works the same way: names at boot, schemas via ToolSearch; servers can force "alwaysLoad" [S27]. | If it works: one ToolSearch step before the first shell call (~1.5K). | **None.** | Per conversation. |
| 16 | **Fixed core**: 24 Claude Code tools 18,003 + the rest of the system prompt 12,186 + small boot notes ~1,380 (agent list, environment, date, deferred-core names, file) | 31,572 | **~37,400** | None (harness). | — | — | — | — |

**Reconciliation.** Rows 1–13 without overlap, plus row 16, sum to 108,626 tape and **126,196 real**, against 126,185 measured. The fit makes this hold by construction; the check that is not by construction is the re-send in §1. Row 15 overlaps rows 1, 2, 3, 5, 6 and 7.

The full per-tool table (68 rows, tape with description/schema split) is in `notes/_lanes/300/B/conductor-tools-table.txt`. The lever arithmetic is in `notes/_lanes/300/B/levers-table.txt`.

### 2b. Sums Dave can act on

| Package | real saving at boot | Other work loses | Confidence |
|---|---:|---|---|
| Chrome off + computer use off + plugin-management uninstall | **~3,900** | Chrome automation, screen control | Switches documented; tool drop inferred (Docs precedent) |
| + Chat search off | **~4,500** | Past-chat search everywhere | Same |
| Pause memory | **~31,700** + ~23,600 per mid-session store change | Memory in every chat and project | Switch documented; tool drop inferred |
| Tool access On demand (untested) | **0 to ~33,500** | Nothing | Untested |
| Leave the Project | **~3,000** (memory scope changes) | Nothing | Inferred |

**The settings levers never reach the big blocks.** The fixed core (~37K), the Artifact tool (12.8K), scheduled tasks (5.8K) and, unless Tool access works, widgets (16.5K) have no Pro/Max switch. The seat is the only lever that removes them together.

---

## 3. The zero-side-effect test: Tool access "On demand"

**Why first.** It is the only switch that could reach the widgets, memory, scheduled-task and bridge families (33.5K real). It is scoped to one conversation, so client work cannot be touched [S5].

**Why it might not work (INFERENCE).**
- The article speaks of connectors: "When you connect many services to Claude…".
- The built-in families behave like servers marked "alwaysLoad". At #300's boot they loaded in full while Chrome, computer use and the built-in browser were deferred: 42 loaded MCP tools vs 86 deferred names, from the deferred-tools attachment, line 10.

**Protocol.** One fresh conversation, 2 minutes, no externality.
1. New conversation in the Apollo project. Before typing, open "+" › Connectors › Tool access and pick **On demand**. If the menu is absent in a Project conversation, that is the answer; record it.
2. Send `boot probe — reply with one word`.
3. Read the first-turn fill and the loaded families (§8, lines 1–2). A pass is a boot well under 126K, with the widgets and memory families gone from the loaded list and present only as deferred names.
4. Close that conversation. Nothing else changes.

---

## 4. The seat band

### 4.1 Is a local (non-cloud) Cowork still offered? **No, not for this account.**

- "How Cowork in the cloud works … **Sessions run in the cloud on every surface.**" [S2]
- The merged experience: "Once your account has the new experience, you can't switch back to separate 'Chat' and 'Cowork' options." [S4] This account has it. The conductor's system prompt says "If asked about Claude Cowork: Cowork's capabilities are now part of Claude" (grep of the #300 snapshot).
- Local execution "remains available for **existing desktop deployments**" in the admin architecture note [S3]. Memory from local tasks "stays with those tasks" [S4]. Local Cowork "don't use memory" [S1].
- **Dispatch** still runs on the desktop, but "isn't available to new users. If you already use Dispatch, you can keep using it for now" [S18]. Whether Dave has it is UNSOURCED.
- So the ~72K local seat (`BOOT_CEILING_TK = 72_768`, `knowledge/_gauge_tokens.py:351`) cannot be restored through Cowork. **INFERENCE (timeline):** #297 was the first 127K boot, after the merge launched on 16 September per `notes/_subreports/2026-09-23-298-A-…md` §1. The seat change and the account's move to the merged experience are plausibly the same event.

### 4.2 The conductor as Claude Code on the Mac, inside the repo — **yes, and it is the big lever**

**Where.** Either the desktop app's **Code tab** with Environment = **Local** and Project folder = the UX-design repo [S24, line 47], or the **CLI** (`claude`) in the repo folder. Both run on the Mac and bill the same Max plan [S22].

**Boot — measured core plus sized additions.**

| part | tape | real | how known |
|---|---:|---:|---|
| Clean CLI payload: 23 tools 16,226 + system 1,368 + first-message context 1,489 | 19,083 | **~20,100** | **MEASURED** (details below) |
| Interactive-only tools (AskUserQuestion, TaskCreate, TaskUpdate; sized from the conductor's copies) | 3,934 | ~3,900 | INFERENCE |
| Account skills synced (the 12 `anthropic-skills` listing entries) | 1,863 | ~2,700 | Sync documented [S11]; size from #300 listing |
| AGENTS.md, read automatically when there is no CLAUDE.md (v2.1.277+) [S26] | 1,858 | ~2,700 | Tape measured on the mount |
| The repo's 3 custom subagents (`.claude/agents/`) | ~150 | ~200 | INFERENCE |
| **Total, Artifact tool off** (`"enableArtifact": false` in `.claude/settings.json`, v2.1.242+) [S28] | | **≈ 29,600** | |
| Artifact tool left on (7.5K–11.8K depending on artifact features) | | ≈ 37,000–41,000 | size from two captures |
| **Against today's 126,185** | | **−85K to −97K** | |

How the core was measured:
- A local stand-in server recorded the CLI's first request and answered 400, so no model call was made.
- Claude Code **2.1.280**, `env -i` (no cloud variables), `-p` print mode, API-key mode, empty git repo.
- Result: `notes/_lanes/300/B/cli-capture-summary.txt`; replay with `cli_capture/run_capture.sh`.
- API-key mode means **no** synced skills, **no** Artifact tool and **no** claude.ai connectors. Those are added separately in the table.
- The interactive truth is one `/context` away (§8, line 4).

**For comparison.**
- The old local Cowork seat was ~72.8K.
- Every cloud sub boots at **66.3K real**: measured 66,307 / 66,324 / 66,335 / 66,336 for this wave's four lanes. 58.7K of that tape is tool schemas the subs never use.
- A Claude Code sub on the Mac carries its own short prompt and whatever `tools:` its definition allows [S29]. That saving lands in plan usage, not in the conductor's window (INFERENCE on size).

**What carries over.**
- **Skills, dave-voice included.** "Skills you've enabled in your Claude settings also load in Claude Code … when you sign in with the same Claude account … v2.1.273 or later … Run /skills … under claude.ai sync" [S11]. Desktop local sessions "load the skills enabled for your claude.ai account" [S24, line 429].
- **Project instructions.** AGENTS.md already exists (1,858 tape) and is read at start [S26].
- **Git.** Native git on local disk. The rule never to run `git status` exists because it strands `.git/index.lock` on the FUSE mount; that is a mount artefact that should not recur natively (INFERENCE).
- **Transcripts.** Claude Code writes `~/.claude/projects/<encoded-repo>/<session>.jsonl` [S26]. `_checkin.py` looks only at `/sessions/*/mnt/.claude/projects/*/*.jsonl` (`knowledge/_checkin.py:84`), so it needs a Mac glob. After that the hand sums end: the fill is readable again.
- **The window Dave reads in.**
  - The Code tab is a GUI with chat, diff, file editor and a browser pane that can open local HTML [S24].
  - **Remote Control** shows a local session at claude.ai/code and in the phone app. The desktop setting is "Settings › Claude Code › Enable remote control by default" [S25, line 195].
- **Connectors.** claude.ai connectors reach Claude Code; MCP tools are **deferred by default** there [S27, S30].
- **Chrome and computer use** are off by default in the CLI [S31, S32]. The boot stays lean unless asked.

**What breaks, or must change.**
1. **claude.ai Project memory.** No source says Claude Code reads it, so treat it as unavailable (INFERENCE from absence). Replace it with repo files, or with Claude Code's **auto memory**: an index plus topic files, first 200 lines or 25KB loaded [S26].
   - `autoMemoryDirectory` can point it into the repo; `autoMemoryEnabled: false` turns it off per project [S26].
   - Unlike the cloud snapshot, auto memory is not re-injected when a file changes; files are read with tools.
2. **The render environment.**
   - `ensure_env.sh` builds an **aarch64 Linux** headless Chromium plus Debian libs on the mount for the Cowork VM (`knowledge/_render/ensure_env.sh:9–11, 41–59`). Those binaries will not run natively on macOS.
   - A Mac seat needs `pip install playwright && python -m playwright install chromium`, and a darwin branch in `seat_env.sh` / `ensure_env.sh` for `$RENDER_SHELL`.
   - The rule "render at the seat, on the mount" still holds; only the binary changes.
3. **The Projects tool and project docs**: not in Claude Code (INFERENCE).
4. **Gauge constants** (`BOOT_FIRSTTURN_TK`, `BOOT_CEILING_TK`) and the capture gate's boot-ceiling arm must be re-baselined to the new seat (lane C's map).
5. **Billing trap.** "If you have an ANTHROPIC_API_KEY environment variable set … Claude Code will use this API key … resulting in API usage charges" [S22]. The repo keeps a key file at the root. Nothing may export it into the shell Dave launches Claude Code from.
6. **Scheduled work** moves to Claude Code Desktop's own scheduled tasks, or stays in claude.ai (INFERENCE).

**Dave's other work.** Unaffected. No account setting changes; client work stays in claude.ai.

### 4.3 Repo in the cloud container, computer link dropped — **possible, but it moves the break to Dave's eyes**

- **Claude Code on the web / cloud sessions.** "Your GitHub repository is cloned into this environment" and the work is pushed to a branch [S21]. `claude --cloud` starts one from the terminal; `--teleport` pulls a cloud session back to the Mac [S33]. The repo is on GitHub (`origin` = `github.com/daveasewen/UX-design`, `.git/config`).
- **Saves** the link-to-Mac block (**~8.8K real**, row 6) plus whatever the cloud host loads. The cloud boot is not measured here. My first capture inherited the cloud env with tool search off (66 tools loaded upfront, Chrome's included), so it is not representative.
- **Breaks:**
  - Dave's by-eye reading. Every file "beside its source" then lives in the cloud clone until pushed and pulled.
  - Rendering at the seat. It would run in the cloud VM, which has a browser.
  - Gitignored secrets: `API-KEY.txt` and `.env.local` (TYPESAFE keys for the typesafe-ai skill) would be absent.
  - Concurrency between two working copies.
  - In the merged claude.ai conversation, "**Add from GitHub isn't supported**" [S4].
  - Claude Code **Projects** (cloud threads sharing repos, instructions and memory) roll out first to accounts **without** existing claude.ai projects [S34], so they probably don't reach this account yet.
- **Security note** (not a lever). The `origin` URL in `.git/config` embeds a credential; I masked it and did not print it. A cloud move should use the Claude GitHub App or `/web-setup` [S33], not that URL.

### 4.4 Ideas I cannot yet prove (labelled, for P and X)

1. **Headless workers at the seat.** The Mac's Cowork VM carries `/opt/cowork/claude-bin/claude`, a 2,293,944-byte shim dated Sep 18. Asked for its version it says "only `claude -p "<prompt>"` is supported in this environment".
   - If it runs a lean headless Claude Code on the plan, lanes could run at the seat with ~20K boots instead of 66K, reading the repo directly.
   - UNTESTED. Its boot, billing and auth are unknown. Try one trivial prompt only with Dave's OK.
2. **Hybrid reading surface.** Conductor in the Code tab (Local) with Remote Control on. Dave reads in the desktop app at his desk and in claude.ai/code on the phone [S24, S25]. The Code tab's browser pane could replace some screenshot round-trips for by-eye checks (INFERENCE).
3. **Skills that never enter the listing.** In Claude Code, a skill with `disable-model-invocation: true` "stay[s] completely out of context until you invoke [it] with /name" [S29]. Apollo's rarely used skills could cost zero at boot.
4. **Artifact tool trim on the cloud seat.** The artifact capability flags change the Artifact tool's size (11,967 tape at #300 vs 7,676 in my env-inherited capture). Switching off Claude Design/Slides/Docs in Settings › Capabilities may shrink it by a few K. The Docs precedent removed the Docs tools. UNTESTED for this tool.
5. **Memory writes only at wrap.** Keep memory on, but write to the store only at the end of a session. The ~23.6K re-send then lands in the next boot's single snapshot, not mid-session (timing lever; lane C owns the opener side).

---

## 5. Premises in the brief, checked from this lane

- **"Cloud is the source" — HOLDS for the four biggest cloud-only blocks.**
  - Memory: local Cowork "don't use memory"; memory reached cloud Cowork on 25 August 2026 [S1, S23].
  - The widgets family, the scheduled-task tools and the Mac-link bridge are cloud-harness families.
  - Together: ~31.7K + 16.5K + 5.8K + 8.8K ≈ **62.8K real**, on the order of the 126K − 72.8K = 53.4K gap. Lane A owns the line-up.
- **"Store writes trigger the re-send" — SUPPORTED.**
  - The snapshot's own framing reads "Assembled from the user's memory store and delivered by the system; **it is replaced when the store changes**" (#300 snapshot, first line).
  - Timing: the re-sent block arrived on the turn after the placement writes (transcript: attachment before message `…3xDMuD`, 187,863 → 211,454).
  - Size: the increment matches a full re-injection (22.3K predicted vs 23.6K measured).
- **"prompt_snapshot equals what is billed" — CONSISTENT, with a unit caveat.**
  - The two boots reconcile under a two-register scale. The third, independent point lands within 5.3%.
  - Two caveats: attachments must be counted as rendered text, not JSON (the memory block is 13,296 rendered vs 14,671 JSON). And "thinking" from earlier turns does not appear to be carried; the check fits only if it is not.

---

## 6. Things found off this lane's path (for X and the conductor)

1. **The gauge's real-token path is dead.**
   - `read_key()` misses the bare-key form in `API-KEY.txt` (`knowledge/_gauge_tokens.py:406–417`).
   - The key itself returned **401 invalid** on 2026-09-23.
   - `MODEL = "claude-opus-5"` (`:49`), while the conductor runs `claude-opus-5-5` (46/46 assistant messages).
   - So every "real" the gauge prints today is either the cl100k fallback or a refusal. Check before trusting any gauge figure in #300.
2. **The Docs precedent.** After Docs was blocked at account level, the next cloud boot came without its tools and 1,483 real lighter (`notes/_lanes/299/WRAP-BRIEF.md:6`; the switch used is not named there). It is the best evidence that rows 1, 2, 9 and 10 would behave the same.
3. **Capture incident, disclosed.**
   - What happened: my first CLI capture inherited the cloud session's environment variables. It synced the account's skills read-only into a scratch config directory and sent its one request to my local stand-in server. No model call; no write to the repo or to Project memory.
   - What I checked: the conductor's transcript was unchanged (no matching lines; mtime before the run).
   - What I cannot rule out: that the child process touched the session's local messaging socket.
   - Fix: all later captures ran under `env -i`.
4. **Subagents cost 66.3K real each at boot** in the cloud seat, none of it usable by a read-only lane (widgets, Artifact, scheduled tasks and memory ride along). Four lanes ≈ 265K of boot, mostly cache reads. No cloud switch reaches it; the Claude Code seat does.

---

## 7. Sources (all read 2026-09-23)

| id | source |
|---|---|
| S1 | support.claude.com/en/articles/11817273 — Use Claude's chat search and memory ("Updated over a week ago") |
| S2 | support.claude.com/en/articles/15520349 — Use Claude Cowork on web, desktop, and mobile |
| S3 | support.claude.com/en/articles/14479288 — Claude Cowork architecture overview |
| S4 | support.claude.com/en/articles/16761823 — Claude Cowork and chat are one Claude |
| S5 | support.claude.com/en/articles/13730515 — Manage Claude's tool access (dated March 16, 2026) |
| S6 | support.claude.com/en/articles/13641943 — Visual and interactive content (March 16, 2026) |
| S7 | support.claude.com/en/articles/13979539 — Custom visuals in chat and Cowork (April 22, 2026) |
| S8 | support.claude.com/en/articles/13663666 — Visual and interactive content on Team and Enterprise plans (March 16, 2026) |
| S9 | support.claude.com/en/articles/9487310 — What are artifacts and how do I use them? |
| S10 | support.claude.com/en/articles/14729249 — Use artifacts in Claude Cowork |
| S11 | support.claude.com/en/articles/12512180 — Use skills in Claude (sync to Claude Code, `syncClaudeAiSkills`) |
| S12 | support.claude.com/en/articles/12012173 — Get started with Claude in Chrome (Preferred browser setting) |
| S13 | support.claude.com/en/articles/14128542 — Let Claude use your computer in Cowork |
| S14 | support.claude.com/en/articles/10684626 — Enable and use web search ("no web search toggle" in the new experience) |
| S15 | support.claude.com/en/articles/11088861 — Use Research on Claude (June 2, 2026) |
| S16 | support.claude.com/en/articles/13854387 — Schedule recurring tasks in Claude Cowork |
| S17 | support.claude.com/en/articles/11176164 — Use connectors (August 20, 2026) |
| S18 | support.claude.com/en/articles/13947068 — Assign tasks from anywhere (Dispatch) |
| S19 | support.claude.com/en/articles/14116274 — Organize your tasks with projects in Claude Cowork |
| S20 | support.claude.com/en/articles/9517075 — What are projects? |
| S21 | support.claude.com/en/articles/12618689 — Claude Code on the web (March 16, 2026) |
| S22 | support.claude.com/en/articles/11145838 — Use Claude Code with your Pro or Max plan (August 19, 2026) |
| S23 | support.claude.com/en/articles/12138966 — Release notes (25 Aug 2026 memory in cloud Cowork; 22 Sep 2026 Opus 5.5) |
| S24 | code.claude.com/docs/en/desktop.md — Code tab: Local/Cloud/SSH, skills in local sessions |
| S25 | code.claude.com/docs/en/remote-control.md |
| S26 | code.claude.com/docs/en/memory.md — CLAUDE.md/AGENTS.md, auto memory |
| S27 | code.claude.com/docs/en/mcp.md — tool search default, `alwaysLoad`, connector delivery by seat |
| S28 | code.claude.com/docs/en/artifacts.md — "Disable artifacts", `enableArtifact` |
| S29 | code.claude.com/docs/en/context-window.md — illustrative startup costs; `disable-model-invocation` |
| S30 | code.claude.com/docs/en/costs.md — "MCP tool definitions are deferred by default" |
| S31 | code.claude.com/docs/en/chrome.md · S32 code.claude.com/docs/en/computer-use.md |
| S33 | code.claude.com/docs/en/claude-code-on-the-web.md — `--cloud`, `--teleport`, GitHub auth |
| S34 | code.claude.com/docs/en/claude-projects.md — rollout note |
| S35 | platform.claude.com/docs/en/build-with-claude/token-counting — "free to use" |
| S36 | support.claude.com/en/articles/14503520 — beta features (July 7, 2026): Claude Code Desktop beta, cloud research preview |

Prior repo research used: `notes/_subreports/2026-09-23-298-A-claude-docs-connector-removal.md`.

---

## 8. REPLAY-THESE

Run in the cloud container, where the transcripts live. The scripts are also copied to `notes/_lanes/300/B/`.

1. Families, fit and every lever row: `python3 /tmp/claude-0/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb/scratchpad/B/levers_measure.py` (defaults to the conductor jsonl and this lane's sub jsonl).
2. Boot fill of any session (use it for the Tool-access probe): `python3 …/scratchpad/B/spend.py <transcript.jsonl>` ("boot fill (msg 1)"). Loaded families: `python3 …/scratchpad/B/tools.py <transcript.jsonl> | head -12`.
3. Clean Claude Code CLI boot payload: `bash …/scratchpad/B/cap/run_capture.sh` (expects 23 tools / 16,226 tape on v2.1.280).
4. Interactive Mac boot, exact: in Terminal, `cd` into the repo, run `claude`, then `/context`. Or open the desktop Code tab › Local › the repo folder and run `/context`.

## 9. Spend (hand-summed from this lane's transcript)

`subagents/agent-a15bc00f2eaf18c75.jsonl`, per distinct message id, at the time of writing:
- 97 assistant messages; boot 66,336 real; peak fill 314,218.
- Output 117,280.
- Cumulative processed input 19.19M, of which cache reads were 18.93M.
- Final figures are in the stub.
