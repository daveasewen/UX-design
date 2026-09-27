# HANDOFF #155 — #304 → #305 — THE WEEKEND RUNS LANDED, AND THE REVIEW MOVED TO AN ARTIFACT

provenance: 304 · 2026-09-26
status: observed

*Written by the delegated OPUS 5.5 wrap seat at the close of #304 (conductor Opus 5.5, a CLOUD session linked to Dave's computer). Every figure here was measured at this seat unless it says otherwise; the lanes' figures are the lanes'.*

⛔ **DATE SPLIT.** Opened Saturday 2026-09-26 14:40 BST; the runs went on through the night on 49 delegated seats; he spoke again Sunday 2026-09-27 11:44 to 12:16; then this ritual (`date` at this seat: `Sun Sep 27 11:21:13 UTC 2026`). Keys, filenames and the stratum carry the session date 2026-09-26 (`s294-D11`); the GM header line, the banner, the delta and the stamp carry 2026-09-27; lane reports keep the day they were written.

⛔ **NOTHING WAS INSCRIBED. `knowledge/_rulings.json` READS 638**, by `json.load` over `rulings`: newest `s295-D4`. He never said "inscribe". Statuses were STAMPED on existing records (Run 2: 184 `enacted` with receipts; later `s245-D10` and `s277-D12`, at `aaf3bb7e`) — status writes, not rulings. His words are verbatim in `notes/_lanes/304/WRAP-BRIEF.md` — **quote them; never paraphrase.**

⛔★ **#305'S FIRST BEAT IS THE TUESDAY SITTING:** `notes/_SITTING-304-tuesday-2026-09-29-v1.html`, 53 calls, opened through the artifact **"Apollo 304 review"** (`https://claude.ai/artifact/1PpLec2QecFEjdnDAXYCw5`). Put call 1 first: cut v1.0.14 from candidate 2?

⛔★ **HIS LINKS DO NOT OPEN. NEVER HAND HIM A `computer://` LINK TO A REVIEW PAGE AGAIN.** The Claude app shows *"Files saved in this location can't be previewed."* for files in his repo folder. Review pages go to him as that ONE artifact, republished to the same URL; his decision boxes save per browser and device, and he returns his answers with **"Copy as text"** pasted in chat.

⛔ **THE FILL IS A HAND SUM, NOT A `_checkin.py` READING.** Over `/root/.claude/projects/-home-claude/7a58cbdf-2621-5d8e-b384-1bf3979f7d8b.jsonl`, at this seat, 65 distinct messages: **boot 131,130** · over 200,000 at 15:34 Sat · over 256,000 at 17:51 Sat · **over 300,000 at 22:08 Sat** · 389,266 at 11:16 Sun (the conductor's "about 389,000") · **453,905 at the wrap** (the message that launched this seat). Over the hard line by 153,905.

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-154`.** Every open item on those still stands **except the ones struck with receipts** — this wrap strikes ONE item on `_HANDOFF-154` § OWED (addendum at its foot) and four carries in `_CARRIES.md` § `residual → #305`.
4. `notes/_lanes/304/WRAP-BRIEF.md` — his thirteen messages, verbatim, with the facts.
5. **For the first beat:** the sitting page itself, and its report `notes/_subreports/2026-09-27-304-W5b-tuesday-sitting.md`. Behind it: `notes/_subreports/2026-09-27-304-R4s2-candidate-2-scores.md` (the cut) and `notes/_subreports/2026-09-27-304-V5-verifier-wave-five.md` (what shipped unruled).
6. `_CARRIES.md` § `residual → #305` when you need the bodies. Fetch the section; do not read it at boot.
7. The other reports, when the work needs them: `notes/_subreports/2026-09-2{6,7}-304-*.md` (39) · this wrap's `notes/_subreports/2026-09-27-304-W-wrap.md`.

---

## ⛔⛔ HIS WORDS

**All thirteen are in `notes/_lanes/304/WRAP-BRIEF.md`, with their BST day and time — seven of them were sent mid-turn and live only as `queued_command` attachments in the transcript.** The ones that set #305's work:

> Sat 14:51 — are we defining the a poc too or the architecture for the final piece, btw we can make a best guess for this for a poc. Also the reason we've rejected jev at build time is because it makes Apollo less transferable at the moment, its not rulled out completly for a GenUI project.

> Sat 15:33 — Put together a plan, lets leverage some big pushes over this weekend that I can leave you to churn though, recommend the models, effort levels and subs structure you propose to get some work nailed by early next week. don't worry about token spend. lets get ripping, you know the usual instructions, watch the externalities, dependancies and test it hard :)

> Sun 11:44 — I don't understand why but any link you expose for me doesn't work
>
> can you investigate a solution, and then surface everything I have to revirew or check over

> Sun 12:11 — I seem to have lost the index page there's no back button on any of the pages so i cant navigate in the internal browser

> Sun 12:16 — no worries lets wrap up

---

## WHAT THE SESSION FOUND

- **Jev is not ruled out for GenUI** — his 14:51 words narrow #303's carried caution (dev-time only) to build-time portability. The v2 page carries rules-then-Jev-ranks.
- **CI had been stopping at step 8 since 2026-09-09.** Run 1 took it to the end (146, now 152), and two of the plan's premises turned out wrong on the way (`notes/_subreports/2026-09-26-304-R1-ci-sees-to-146.md`).
- **The store said "ruled" for 184 rulings the tree had built** (Run 2); 109 could not be settled and are his, on the uncertain-stamps page.
- **Composing stopped the tracing but did not raise quality** (R4s); candidate 2 is better and cleaner, and most of the gain is the chart engine, which lifts old pages too (R4s2).
- **A scheduled seat acted on a live tree** — dream pass 14 ran `git status` on the mount and its uncommitted row took CI step 117 red once.
- **The app cannot preview his repo's files**, so every link the session gave him was dead from the start.
- **The artifact hub's links lack the `notes/` prefix** the pages were published under (measured at this seat) — unproven that they open.

## WHAT LANDED

| Commit | CI run | What |
|---|---|---|
| `6af293df` | `36257551837` | wave one: Runs 1, 2, 5; the Apollo-MCP page v1 + v2; A1–A4; the plan (F); six decision pages (R6a/b); V1 |
| `4be130e5` · `aaf3bb7e` | `36275037261` | wave two: Run 3 (`s245-D10`, `s277-D12`), Run 4 (skill, two advisory gates, harness, cold runs scored); V2; then the two status stamps |
| `86249459` | `36281589292` | wave three: W3a (minus the Kpi-tile trio), W3c, W3b, V3 |
| `3100da99` | `36291750194` | wave four: W4a, W4b, J, V4; candidate 2 built |
| `ff382c0b` | — | dream pass 14, the scheduled fire (not this chat) |
| `52049781` | `36306939769` | wave five: W5a as narrowed by F5, W5c + KG generator wiring, the sitting page, candidate 2 scored, V5, F5 |
| `8a5fa863` | `36311157795` | wave six: W6's reduced-motion fit; dream pass 14's `_LIVE-STATE.md` row carried |
| *the wrap* | § POST-WRAP | this ritual |

All pushed (`571d458c..8a5fa863`), plain `git push origin master`, DECLARED, by commit seats C1–C6, each reading CI back after `render`: release ✅, gates ⛔ at steps 5 and 6 on the predicted set, render ✅ — except `[121]` on wave two (fixed by W3c) and `[117]` on wave five (the dream pass, fixed at wave six). Last read: step 5 FAIL `[132]` only; step 6 reds `[81] [90] [98] [131] [132] [136]`, advisory `[138] [139] [148]`, `[151]`/`[152]` exit 77. The artifact **"Apollo 304 review"** is not in git: version 2 `1790507590-9f08`, 160 files; its hub is copied to `notes/_lanes/304/ARTIFACT/index.html`.

---

## THE STRIKES — BY ADDITION, WITH THEIR RECEIPTS (`s183-D1` / `s188-D2`)

On `_HANDOFF-154` § OWED (addendum at its foot) and in `_CARRIES.md` § `residual → #305`:
- **`_HANDOFF-154` item 1, the Apollo-MCP proposal page — STRUCK BY THE ACT.** v1 by lane M, v2 on his 14:51 and 14:52 words, both at `6af293df`. The Jev clause of #303's carry is corrected by his 14:51 words, with that receipt. His seven decisions on the page are a NEW item.
- **`s277-D12`, tokens at group grain — STRUCK, ENACTED** at `4be130e5`, stamped at `aaf3bb7e`, V2 PASS, CI `36275037261`.
- **`s245-D10`, the console radius build — STRUCK, ENACTED** at the same commits; the card padding that rode with it is a NEW item.
- **#227's help-gate abort in CI step 6 — STRUCK, THE ABORT IS GONE:** the help gate at step 8 passes and CI asked 146 of 146 on `6af293df`, 152 of 152 on `8a5fa863`.
⛔ **NOT STRUCK:** everything else on `_HANDOFF-154` § OWED — Friday, the Common prompt, his three observations (now a question on the when-rules decision page), the Spider pack on his work machine, the HSBC face, the callipers, `_HANDOFF-152`'s list.

---

## ⬛ OWED TO #305, IN ORDER — EACH WRITTEN AS THE QUESTION IT IS

1. ⬛★★★ **The Tuesday sitting — will he take the 53 calls, starting with call 1, cut v1.0.14 from candidate 2?** Open it through the artifact. Groups 3–6 (calls 14–53) can go on one "yes to the recommendations"; groups 1–2 want his eye. The proposal's seven decisions are group 5; Jev as a suggester is group 6. His answers come back by "Copy as text" pasted in chat — inscribe only on his word.
2. ⬛ **Keep or reverse the three behaviours that shipped without a ruling?** Tick-label thinning (8px, anchor last, `3100da99`), the right-gutter fit (`52049781`, provisional constants), console card padding 20 → 8 (`4be130e5`). Sitting calls cover them.
3. ⬛ **The two held back — which Kpi-tile form (trim, clip-visible, or leave it), and the root trim default yes or no?** `notes/_lanes/304/W3a/held-back/`; call 41c.
4. ⬛ **Do the hub's links open?** If not, republish to the same URL with each href prefixed `notes/` — an act, not a ruling — and ask him to try one link and one back button.
5. ⬛ **The dream pass on a live tree — change its runbook so the §🔀 row rides its own commit, and keep `git status` out of its seat?** His; the runbook is `knowledge/_RUNBOOK-dream-pass.md` step 7b.
6. ⬛ **Friday 2026-09-25 — what came back?** Still not in the record. Ask; do not assume.
7. ⬛ **Everything still standing on `_HANDOFF-154` § OWED items 2–8**, each at its true age.

---

## THE ARTIFACT — HOW TO UPDATE IT

`https://claude.ai/artifact/1PpLec2QecFEjdnDAXYCw5`, private, owned by Dave. **To change it from a new chat, pass that URL as `url` and READ it first** (a publish to an artifact the chat has not read is refused). ⚠ **The service refuses published paths that start with `_`**, so every page sits under `notes/` in the artifact while the repo's copies sit at `notes/_…` on disk; the hub is at the root. ⚠ **The "← All review pages" button exists ONLY in the published copies** — they and the hub are in #304's cloud scratchpad (`/tmp/claude-0/-home-claude/7a58cbdf-2621-5d8e-b384-1bf3979f7d8b/scratchpad/review304/`), which a new chat's container may not have; the hub is kept at `notes/_lanes/304/ARTIFACT/index.html`. A page republished from the repo loses the button unless it is patched again. The decision bar's "Export rulings .md" cannot save a file from inside the artifact.

---

## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING

- ⛔★★ **NEVER RUN `git status`**, and **`python3 knowledge/_capture_gate.py --wrap` strands `.git/index.lock` on this mount** — the eighth wrap running (#297–#304); `git reset -q` then strands `HEAD.lock` and `refs/heads/master.lock`. Move stranded locks to `notes/_lanes/_orphan-locks/` with a unique suffix (never `rm`), `git reset -q`, move again. Read-only git: `git --no-optional-locks`.
- ⛔ **`_git_commit.sh` strands the index lock on a named path that is UNCHANGED, then blames the next path** (C1). Name only changed or untracked paths — check each with `git --no-optional-locks diff --quiet HEAD -- <p>` first.
- ⛔ **The scheduled dream pass fires weekly (Sunday about 07:12 BST) and may land in a live session:** it commits, and leaves its §🔀 row and stamp in `_LIVE-STATE.md` uncommitted by design. Carry them in the next commit, declared, or CI step 117 goes red.
- ⚠ **CI step numbers moved +4 from step 86 up at `52049781`** (152 steps): any older note quoting 86 or above reads four low.
- ⛔ **`device_bash` kills background jobs when the call returns** — run gates in the foreground with the longest timeout.
- ⛔ **Project memory: none at the opener, none while the chat is live.** The note is placed only after he says he is done.
- ⛔ **The window lines: working 256,000, hard 300,000 (his, #301); stop 180,000 and tolerance 220,000 unmoved. `BOOT_CEILING_TK` 72,768:** a `--wrap` commit is refused by the boot-ceiling arm; the legal path is `_git_commit.sh` WITHOUT `--wrap`, DECLARED not-a-wrap in the message body.
- ⛔ **THE FILL IS A HAND SUM over the cloud transcript** (`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` of the last record per distinct `message.id`). His mid-turn messages are `queued_command` attachments, not user turns.
- ⛔ **`_git_commit.sh` needs `SESSION_N=305`** and a msgfile whose line 1 has no `after #N` or `#N date —` prefix; write msgfiles with python. **Mint `_state` rows for new reports and regenerate `_CHAIN.md` BEFORE the first commit attempt.** The regen serial, in order: `_render_rulings.py` → `tokens/_build_blast_radius.py` → `_build_memento_index.py` → `_build_graph_mention_map.py` → `_gen_chain.py` → `_gen_schematic.py`.
- **`pip install tiktoken --break-system-packages` FIRST** if it is missing.
- ⚠ **Other-seat paths stay dirty by declaration** (dream pass 14's `notes/_dream/_MEMORY-GRADES.json` and `_GRADE-DECISIONS.jsonl` · `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` · `notes/_lanes/294/WRAP-MEMORY-HOOK.md` · #297 lane A's report tail · `notes/_context/2026-09-24-302-context-curve-dave-paste.md` · the untracked nested `UX-design/` · untracked lane work under `notes/_lanes/297`–`303` · the side-quest seat's `notes/_lanes/304-sq/`, its report and four receipts); #304's own `*.pre-W3a.*` and `*.pre-W4b.*` source backups are left too.

---

*Filed report: `notes/_subreports/2026-09-27-304-W-wrap.md`. Dossier: `_DECISION-HISTORY/2026-09-26-304-the-weekend-runs-landed-and-the-review-moved-to-an-artifact.md`. Memory hook: `notes/_lanes/304/WRAP-MEMORY-HOOK.md`. His words and the facts: `notes/_lanes/304/WRAP-BRIEF.md`.*

*Title the next chat:* `Apollo - #305: the Tuesday sitting, 53 calls`
