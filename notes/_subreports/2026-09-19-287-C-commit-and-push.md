# `#287`-C — the commit-and-push lane: three lanes landed, pushed, CI read back

session: `#287` · 2026-09-19
window: lane C (commit and push)
sub index: `C`
brief: conductor Fable 5.1, lane C — commit today's three lanes (I · K · W) through the sanctioned
script, push, read CI back over the public API
tokens: `UNMEASURED — lane subagent; message.usage not readable from inside the lane`

## VERDICT

**DONE, in ONE commit, on the FIRST invocation — no gate refused this lane.**
sha **`75a490cda77db7065c6b866ba68fbc99d9d33279`**, pushed and verified, CI read back.
The `gates` job is red on the **same two inherited steps**, and nothing new.

## 1 · The reconciliation — every dirty path named and accounted for

`git status --short` at lane open: **21 entries** · `git diff --stat HEAD` **17 files, +6,165 / −3,835**.

| path | lane | why it is dirty |
|---|---|---|
| `knowledge/_rulings.json` | **I** + **W** | I inscribed `s287-D1`/`s287-D2` (620 → **622**, re-derived here by `json.load`); W annotated 6 existing records |
| `notes/_RULINGS.html` | I | re-rendered from the store in the same change (`_render_rulings.py`) |
| `knowledge/_seam.py` | I | `:44` DRAFT clause amended — `_standing.md` is no longer a draft |
| `knowledge/_standing.md` | I | header brought onto the ruling |
| `knowledge/_kg_explorer.template.html`, `knowledge/_build_kg_explorer.py` | K | explorer reads the `sizes` map; generator at **v1.27** |
| `notes/_KG-EXPLORER.html` | K | the rebuilt served explorer |
| `knowledge/_state.json` | K + W | row `W-287k` (K) + 7 rows (W) |
| `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md` | W | the wall wording sweep; chain regenerated, `--check` FRESH at lane open (no regeneration needed by this lane) |
| `knowledge/_RUNBOOK-context-gauge.md`, `notes/_MEMENTO-DECISIONS.md` | W | wall wording |
| `knowledge/_memento-index.json` | W | memento index rebuilt |
| `dashboard/index.html` | W | **REGENERATED** — see §2 |
| `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` | — | the two append-only instrument logs (W-22 declaration; the script auto-stages what it dirtied, `#261 M2`) |
| `notes/_lanes/287/` | I · K · W | `DAVE-RULINGS-2026-09-19.md`, `BOOT-COLD-2026-09-19.md`, `K/` evidence — see §3 |
| the three `notes/_subreports/2026-09-19-287-{I,K,W}-*.md` | I · K · W | the filed reports |

Nothing was dirty that no lane owns. `_gen_chain.py --check` was **GREEN at lane open** — the first
commit lane in three sessions that did not have to regenerate `_CHAIN.md` itself (#286 lanes C and
C2 both met it RED).

## 2 · The dashboard regeneration is DECLARED, not hidden

`dashboard/index.html` carries a **9,590-line diff**. Lane W measured that a regeneration from the
**UNCHANGED `HEAD` `_state.json`** alone moves **11,617 lines** — i.e. the committed dashboard was
already stale against its own source before #287 touched it. W's seven row edits account for
~1,262 lines of the delta, most of that `gen_dashboard.py`'s re-ranking cascade.

⬛ **This is stated on the face of the commit message, not buried.** The dashboard in the tree is
now FRESH against the store for the first time in several sessions, and the bulk of its diff is
**inherited staleness**, not #287 wording.

## 3 · The 4.3 MB before-copy — MOVED, not committed, and not deleted

`notes/_lanes/287/K/before-_KG-EXPLORER.html` was a **4,361,115-byte** plain copy of the
pre-rebuild explorer, with an **806,971-byte `.gz` beside it**. Committing the plain copy was
refused by the brief. The sandbox delete-guard forbids `rm`, so the **#284/#286 `mv` precedent**
was used — the same move lane C took with the 898 symlinks at #286:

```
$ mkdir -p _to_delete/287-K-before
$ mv notes/_lanes/287/K/before-_KG-EXPLORER.html _to_delete/287-K-before/
$ git check-ignore -v _to_delete/
.gitignore:34:_to_delete/	_to_delete/
```

The `mv` **succeeded** — no unlink was needed and none was attempted. `_to_delete/` is gitignored,
so the copy is outside the commit and outside the index. **`.gitignore` was NOT edited** and no
path was excluded from staging: the file simply is not in `notes/_lanes/287/` any more.
The **`.gz` (807 KB) IS committed** — it is the evidence K filed, in the form that was meant to
be kept. `notes/_lanes/287/` carries **0 symlinks** (checked).

## 4 · The store rows for the three reports

`_gate_doc_rows.py`'s second half (#208) refuses a commit that stages a sub-report with no
`_state.json` row (`s218-D7`). At lane open only **K** had one (`W-287k`). Rows `W-287i`,
`W-287w` and `W-287c` were written through **`_state.py`'s module API**, never by hand-editing
`_state.json`.

⚠ **Writing another lane's row is a judgment this lane made.** Each row's `closes_when` is taken
from that lane's own filed verdict and nothing was re-worded; the alternative was
`DOC_ROW_ACK`, which would have shipped three invisible documents to pass a gate. Named here so
the conductor can correct a close-condition rather than discover it.

## 5 · Compliance

- Commits ONLY via `knowledge/_git_commit.sh`, **every path named explicitly** (P5). The T3 prefix
  was generated by the script and **never hand-written**; a **fresh** msgfile name was used.
- `gen_kg_rules.py`, `land_rests_on.py`, `gen_kg_icons.py`, `_build_all.py`: **not run.**
- `python3 knowledge/_gen_chain.py`: **not run** — `--check` was already green.
- `rm .git/index.lock` / any `rm` inside `.git`: **never run.**
- Working files under `notes/_lanes/287/C/` only. `/tmp` not used for the msgfile.
- `--quiet` used on every invocation.

---

## 6 · The commit — ONE run, NO refusal

`SESSION_N=287 bash knowledge/_git_commit.sh --reconciled --quiet <msgfile> <22 paths>`.
**One invocation, exit 0, no gate refused.** The #286 lanes needed two runs (C) and one (C2); the
difference here is the same one C2 named — the prior lane's report was read before calling, so
`SESSION_N=287` was on the first call, and the four `--check`s that have refused commit lanes in
past sessions (chain · doc rows · showroom · mention map) were each driven to green *before* the
script ran rather than being discovered by it.

⚠ **One self-inflicted staleness, found and cleared before the call.** Writing the three store
rows moved `_state.json` 706 → **709** items, which (a) put `dashboard/index.html` out of sync with
its own source again and (b) re-staled `_CHAIN.md` (the chain prints the item counts). Both were
regenerated by their own generators — `gen_dashboard.py` and `_gen_chain.py`, neither fenced — and
re-checked green (`_CHAIN.md` FRESH, 12,063 tk). `notes/_lanes/287/C/_CHAIN.before-regen.md` is the
before-copy. **No fenced generator was run.**

Gate verdicts from the `--quiet` stream, in order:

```
— msgfile line 1 carries no T3 prefix (#208 reuse gate passed)
— chain fresh (_gen_chain.py --check passed)
— doc rows present (_gate_doc_rows.py passed)
— showroom in sync (gen_showroom --check passed, s191-D1)
— polarity gate green (_validate_polarities.py --check passed, s238-D7)
— mention map fresh (_build_graph_mention_map.py --check passed, #208 [110] class gate)
— session witness agrees (#287)
⚠ wrap gate RED — visible, not blocking: this commit is DECLARED not-a-wrap (#74-D1).
— spine-writer selftest green (mid-session commit, DECLARED not-a-wrap)
— T3 headline: after #287 2026-09-19 — #287 lanes I·K·W: 2 rulings inscribed, …
— mention map is either unchanged or staged (#208 [110] second-half assert)
— doc rows present for this commit's staged adds (_gate_doc_rows.py, post-staging)
— committed: 75a490cd after #287 2026-09-19 — #287 lanes I·K·W: …
— subject asserted identical to the headline T3 generated (in memory, not re-read — #171)
— subject carries exactly ONE T3 prefix (#208 doubled-subject assert)
✓ done — locks clear, safe for Dave to push via GitHub Desktop
— --quiet: 559 transcript lines · exit 0
```

**The subject was NOT truncated this time**, unlike #286 lane R2's. `git log -1 --format=%s`:

> `after #287 2026-09-19 — #287 lanes I·K·W: 2 rulings inscribed, the explorer reads `sizes`, the 256,000 wall reworded`

118 characters against the script's 120-char cap — the subject was written to fit the prefix the
script adds, rather than discovering the cap afterwards.

### The gate reds seen and NOT paid to unblock

All four classes were RED on the committing run, all non-blocking on a declared not-a-wrap
(#74-D1), and **none was touched by this lane**:

- **`boot-drift CEILING BREACH`** — the gate still names **7** readings (#277–#283) against
  `BOOT_CEILING_TK` 70,000. ⚠ It does **not** yet count #286's 73,832 or #287's 74,120; the wrap's
  `notes/_GAUGE-LOG.md` line is where those enter (`s241-D2`), and a commit lane does not write it.
  The number is shrink-only (`s240-D2` / `s241-D1`) and was **not raised**.
- **`boot double-count`** ×5 — #243 (×5), #264, #272, #273, #274. Unchanged from #286.
- **`_LIVE-STATE.md` / `GOOD-MORNING.md` date zones do not carry 2026-09-19** — a wrap act
  (ritual steps 1 / 2). Not done here.

⚠ **All of these BLOCK at the wrap's `--wrap` run.** Largest committed file under
`notes/_lanes/287/`: the **806,971-byte `.gz`**. No 4.3 MB blob went up.

## 7 · The push — VERDICT

`bash knowledge/_git_commit.sh --push --quiet`, the only sanctioned path (`s133-D2` / `s203-D1`),
exit 0, 3 transcript lines. The verdict line, **verbatim**:

> `✅ pushed and VERIFIED: remote master == local 75a490cda77db7065c6b866ba68fbc99d9d33279`

Independently re-verified outside the script:

```
local:  75a490cda77db7065c6b866ba68fbc99d9d33279
remote: 75a490cda77db7065c6b866ba68fbc99d9d33279
```

**One commit went up, not three** — unlike #286, where lane C2's push carried three local-only
commits. The clean-tree gate passed on the first attempt because the commit above left
`git status --short` empty, this lane's own working files included.

## 8 · CI read-back — `head_sha=75a490cd`

`GET https://api.github.com/repos/daveasewen/UX-design/actions/runs?head_sha=75a490cda…`, unauthed.
**`total_count` = 1.** Run **`35431307797`**, workflow `gates`, created **08:10:57Z** — seconds
after the push. Polled at 08:13:31Z, 08:15:26Z, 08:17:27Z and 08:18:35Z.

| | status | conclusion |
|---|---|---|
| **the RUN** `35431307797` | **`in_progress`** at the last read | ⬛ **none claimed** |
| job `gates` | `completed` | **`failure`** |
| job `release` | `completed` | `success` |
| job `render` | **`in_progress`** | ⬛ none claimed |

⬛ **NO run-level colour is claimed.** The run had not completed at the last read.

### The `gates` failure is the SAME TWO STEPS — inherited, not new

`/actions/runs/35431307797/jobs`, failed steps on `gates`:

> step **5** — `Survey the COMMITTED tree — every check/selftest before any regeneration` · `failure`
> step **6** — `Knowledge build — all derived views + blocking gates` · `failure`

Re-read on the **previous** commit `9c013d2d` (run `35396866095`, completed `failure`): the failed
steps are **`5` and `6`, the same two names, in the same job**. ⬛ **The red is INHERITED. This
commit neither introduced a CI failure nor cleared one.** `release` is `success` on both.

⚠ **`render` is unresolved on this run**, exactly as it was on #286's read. It completed `success`
on `9c013d2d`; here it was still on step 6 (`Full state-contrast sweep — BLOCKING (s218-D4)`) at
08:13:31Z and still `in_progress` at 08:18:35Z. Whether it passes is **not claimed either way**.
Polling stopped at ~8 minutes per the brief's stop rule. **The next reader should re-poll
`35431307797`.**

## 9 · Report state

⚠ **This report is DIRTY in the working tree.** §6, §7, §8 and this note — the sha, the push
verdict, the CI read — were written AFTER the commit, by instruction (the #286 C2 order). The
**committed** copy of this file ends at §5 and its VERDICT block carries an HTML-comment
placeholder. **The wrap must commit this file again** to land them. Nothing else in the tree is
dirty except the instrument logs the verification itself appends to.
