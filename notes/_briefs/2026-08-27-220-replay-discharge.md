# #220 sub brief — REPLAY-THESE discharge across the #219 filed reports (verify, NO repair)

**Model: Opus. Budget: sub spend is QUOTA and today quota is use-it-or-lose-it — be thorough. FILL discipline inside your own window still applies.**

## Mission
The #219 filed sub-reports carry `REPLAY-THESE` sections the conductor owes replays on. Discharge the queue: enumerate, replay each item exactly as its report states it, record the verdict. VERIFY ONLY — you repair nothing, promote nothing, rule nothing.

## Method
1. Enumerate: `grep -ln 'REPLAY-THESE' /sessions/gifted-ecstatic-carson/mnt/UX-design/notes/_subreports/2026-08-2[56]-219-*.md` (and `2026-08-26-219-*`). List every item verbatim before running any.
2. Replay each item AS WRITTEN — same command, same file, same expectation. Name the probe in your log ([[unmatched-grep-is-not-an-absence]]: an unmatched grep names its pattern; a matched one quotes the line).
3. Verdict per item: GREEN (expectation holds, quote the evidence line) · RED (state what the probe invalidates — say what it invalidates, not just "failed") · COULD-NOT-RUN (name the first obstacle AND check whether it is the binding one before writing "blocked" — grep the runbooks first).
4. Known environment limits: no `gh`, GitHub API 404s unauthenticated — any CI-reaching item is COULD-NOT-RUN with that named reason, and it stays the conductor's. `_build_all.py` must NEVER be run partially — any item asking for it is COULD-NOT-RUN (sandbox-impossible, ~49s vs ~45s call kill), noted for CI. tiktoken: `pip install tiktoken --break-system-packages` before any gauge-touching probe.
5. A crash is not a fail: a probe that errors is COULD-NOT-RUN with the error quoted, never a RED.

## DO-NOT-RULE / DO-NOT-TOUCH
- You own ONE region: your filed report (plus a scratch log under `/tmp`). No repo file changes at all — no repairs even for one-character fixes (log them as findings), no generator runs that write (if a replay item itself regenerates a file, run it against a COPY under /tmp and `cmp` — never in place), no git, no memory, no `_rulings.json`, no `_state.json`, no promotions (both #219 advisory gates STAY advisory).
- `_capture_gate.py --selftest` writes a repo file — if an item names it, run with the repo copy protected: note the #158 write-by-default class and verify via `git show HEAD:` comparison afterwards is NOT available to you (no checkout) — so instead record the file's pre/post hash and restore content from the pre-read if it moved.

## Pitfalls / consequences (mandatory, Dave #165)
- A replay run against a stale premise reports a phantom red — verify the premise (file exists, generator name current) before grading.
- Ritual output ≠ ritual ran: verify against the target file/git log, never a banner.
- Sandbox call-boundary kills at ~178s: drive long items as separate calls.

## Report
FILE at `notes/_subreports/2026-08-27-220-replay-discharge.md`: a table of every item (source report path · item verbatim · verdict · evidence), a `COUNTS:` line (items N · green · red · could-not-run), `RULING-SHAPED QUESTIONS` (Dave's), `REPLAY-THESE` (anything the conductor must re-run, e.g. CI-bound items). Chat gets a STUB (≤6 lines).
