# The Project instructions now live — v2, pasted by Dave before "wrap" at #300

provenance: 300 · 2026-09-23
status: observed

⛔ **HIS ACT, NOT AN INSCRIBED RULING.** Dave pasted this text into the Apollo Project's instructions box between the conductor's last reply (17:46 BST) and his "wrap" (17:56 BST). He never said "inscribe"; `knowledge/_rulings.json` reads 638, newest `s295-D4`.

**Where the text comes from, three ways, all identical:** the conductor's wrap brief (quoted verbatim) · the conductor's transcript, a `session_context` attachment marked `changed: true` at 16:56:07 UTC, arriving with the "wrap" turn (`/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl`, row 254) · the wrap seat's own session context. **Byte-exact copy: `notes/_lanes/300/PROJECT-INSTRUCTIONS-v2-LIVE.txt`** — 1,893 B, the text plus one trailing newline (the rollback file's convention), **md5 `9d7837a3a5558553d404463adf8e72bc`**; the transcript's copy gives the same md5 by the same convention.

## The text, verbatim

```
This is Apollo, a governed design-system engine. The repo is the folder mounted at $HOME/mnt/Projects--UX-design on Dave's computer (never the empty UX-design--UX-design). The repo is the record; Project memory is the accelerator.

On the first turn of every session, before replying:

1. In one shell call at Dave's seat: cd "$HOME/mnt/Projects--UX-design"; ls _HANDOFF-*.md | sort -t- -k2 -n | tail -1; bash knowledge/_render/ensure_env.sh 2>&1 | tail -1. If ensure_env prints FAIL, read the ninth stratum of knowledge/_RUNBOOK-render-verify.md before anything renders.
2. Read that newest _HANDOFF-*.md. It outranks everything, including _CHAIN.md.
3. Read _CHAIN.md.
4. Do not read or write Project memory at the opener, or anywhere while the chat is live: any store change re-sends the whole memory list into the next turn. The last session's note is placed only after Dave says he is done; if it was not placed, leave it — the repo keeps every note at notes/_lanes/<n>/WRAP-MEMORY-HOOK.md.
5. Reply in dave-voice with the session's first beat — not a greeting, not a question.

Standing: Dave rules from plain prose and visuals, never ID codes. Commits only via knowledge/_git_commit.sh; push is at the conductor's judgement with a CI read-back in chat. Every sub files its report at notes/_subreports/. At the cloud seat _checkin.py cannot see the conductor's transcript; when the fill matters, hand-sum it in the cloud shell.

Rendering: every render runs at Dave's seat, on the mount, in one bash call — export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver> with executable_path=$RENDER_SHELL. Never route a build through the cloud workspace because the seat "has no Playwright" — it does once ensure_env.sh has run. Files written for Dave live in the repo beside their source; give him the path, not a download.
```

## The diff — recorded at the #300 wrap seat (python `difflib`, `n=0`)

| against | result |
|---|---|
| **the plan page's paste-ready block** (`notes/_PLAN-300-boot-diet-2026-09-23-v1.html`, its Technical section, HTML-unescaped; page md5 `7414d500b77d345307540021e22118ad`) | **IDENTICAL**, byte for byte — he pasted the page's text |
| **lane C's v2 draft** (`notes/_subreports/2026-09-23-300-C-lean-opener-and-dependencies.md` § 6, md5 of the block `860543acbf1260e860b87c189532ce3b`) | **step 4 only** — lane P's edit, flagged on the page: C's *"Do not read or write Project memory at the opener: the wrap placed the last session's note. Only if the handoff says it was NOT placed, place it through a sub."* became the live *"Do not read or write Project memory at the opener, or anywhere while the chat is live: any store change re-sends the whole memory list into the next turn. The last session's note is placed only after Dave says he is done; if it was not placed, leave it — the repo keeps every note at notes/_lanes/<n>/WRAP-MEMORY-HOOK.md."* Everything else is C's text unchanged. |
| **the rollback copy** — the instructions as they stood at #300's opener (`notes/_lanes/300/C/PROJECT-INSTRUCTIONS-as-of-2026-09-23-ROLLBACK.txt`, md5 `a6e11674ea1bf0c74ffbd37cb10c5489`; the transcript's boot `session_context`, row 19, reproduces that md5 at this seat) | **three changes, Rendering untouched:** (1) the first paragraph names the folder exactly — *"the folder mounted at $HOME/mnt/Projects--UX-design on Dave's computer (never the empty UX-design--UX-design)"* in place of *"the UX-design folder (Cowork must have it selected — the outer UX-design folder, not the empty nested one)"*; (2) the opener's seven unnumbered lines become five numbered steps — one shell call (`cd`, the newest handoff by numeric sort, `ensure_env.sh` tail), read the handoff, read `_CHAIN.md`, **no memory read or write at the opener or while the chat is live**, reply with the first beat; **gone:** listing Project memory and reading `index.md`, `pip install tiktoken` and `_checkin.py --window 200000 --no-block`, and placing the last session's hook at the opener; (3) Standing gains one sentence: *"At the cloud seat _checkin.py cannot see the conductor's transcript; when the fill matters, hand-sum it in the cloud shell."* |

**Rollback, if he wants it:** paste the rollback file's text back (md5 above). Nothing in the repo reads the instructions box, so nothing else needs undoing.

**What it changes downstream (not enacted here — carried to #301 as questions):** `knowledge/_RUNBOOK-capture-ritual.md` step 3's #278 paragraph still has the NEXT opener place the hook, and `knowledge/_RUNBOOK-render-verify.md` still names "the `_checkin.py` step". The first chat under this text (#301) is its first real test — the page projects ~161K after his first message, against today's 211,454.
