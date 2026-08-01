# Worker receipt — `/wayfinder` desk research — 2026-08-01

```
provenance: worker-wayfinder-desk-research · 2026-08-01
status: observed
```

**Lane:** `worker-wayfinder-desk-research` · **Role: WORKER.** No git touched — a conductor reconciles and commits.
**Brief:** none. Dave's opener, verbatim: *"I want you to research something for memento. take a look at this and do some desk research around its claims. https://www.aihero.dev/skills-wayfinder — leave receipts for another window to pick up for the commit."* Then, second message, verbatim and without comment: *"this is the repo https://github.com/mattpocock/skills/tree/main"*.
**Model:** Opus 5 (`claude-opus-5`, per session env). **Stamp:** 2026-08-01, 17:05 BST first draft, correction pass ~1h later.
**Output:** `notes/2026-08-01-wayfinder-skill-desk-research.md` (**FLOATED**, 31,751 B, **carries a CORRECTION LOG at its head — read that first**).

**Context gauge at authoring: 🔴 RED ~85% — ESTIMATE, gap DECLARED not defaulted.** No addressable handle for a running parent ([[cowork-gauge-transcript-crack]] #68 DISPROVEN). The correction pass cost roughly what the original research cost. Per [[planning-estimate-is-not-a-measurement]] this flips no decision here, but **the next window should assume this lane had no headroom left for a third pass** — the open probes in §8/U1 were deliberately not run.

---

## ⛔ READ THIS FIRST — a finding in this note was published wrong and then retracted

The first draft's headline-3 finding ("the repo's README has drifted from the skills it ships") was
**wrong**. It was an artefact of my own fetch layer serving per-path caches of different ages. Dave
posting the bare repo URL was the trigger to re-probe; five probes settled it. **§5 is retracted in
place and replaced.** §2, §3, §4, §6, §7 survive, and §5.2 states why each does.

**If you are committing this, commit the corrected file — do not resurrect the first version from
anywhere.** The retraction is the most useful thing in the note.

---

## ✅ FOR THE COMMITTING WINDOW — do exactly this

**Two files, both new, both additive. Nothing else in the tree was touched by this lane.**

```
notes/2026-08-01-wayfinder-skill-desk-research.md               (new, 31,751 B)
notes/_receipts/2026-08-01-wayfinder-desk-research-worker.md    (new, this file)
```

1. **Do NOT `git add -A`.** Per [[feedback-worktree-reconcile-trail]] the tree is shared — add the two paths above by name and reconcile anything else on its own merits.
2. **Commit via `knowledge/_git_commit.sh`** — do not hand-roll, per [[git-lock-mv-not-rm]] (⛔ #56). Dave pushes from GitHub Desktop afterwards; nothing to paste back.
3. Suggested subject: `notes: desk research on /wayfinder — FLOATED, incl. retraction of a stale-read finding`

### ⛔ What this lane deliberately did NOT write, and you should not add

- **No `notes/_MEMENTO-DECISIONS.md` entry.** Nothing was ruled. Per [[feedback-dont-launder-a-premise-into-a-ruling]] a survey does not write to the ledger — **and a lane that just got a finding wrong doubly does not.**
- **No `_FUTURE-STATE.md` entry, no `GOOD-MORNING.md` §C edit, no gate, no charter edit, no runbook edit.** §5.3 proposes a two-fetch staleness control and §7.1 proposes one charter row. Both are **Dave's to rule**. Per [[gate-inside-the-growth-loop]] I am not adding machinery to buy back my own mistake.
- **Nothing from `mattpocock/skills` vendored in.** Desk research only.

---

## Verification — what was run, not asserted

| Check | Method | Result |
|---|---|---|
| Capture gate accepts the note | `python3 knowledge/_capture_gate.py` | `51 in scope · 0 fail · 0 warn` (re-run after every edit, incl. the correction pass) |
| **The gate actually SEES the note** (mutation test) | renamed to `_tmp-mutation-probe.md` → re-ran → renamed back → re-ran | **51 → 50 → 51.** The green moves when the file moves ⇒ measurement, not assertion |
| Gate glob covers it | `_capture_gate.py:11-12` — *"notes/YYYY-MM-DD-*.md (non-underscore-prefixed, date >= CUTOVER)"* | matches |
| **Remote-artefact staleness** (the control I failed to run first time) | fetch a file the claim says must exist (`to-spec`) **and** one it says must be gone (`to-prd`) | **both resolve ⇒ the view is cached, not live.** Two fetches, decisive |

Mutation test run **at birth** per [[gate-must-quote-what-it-forbids]]. Restores used `mv`, never `rm` ([[git-lock-mv-not-rm]]).

---

## What the note says now, in four lines

1. **The aihero page and the installable `SKILL.md` disagree** on three load-bearing mechanisms (research-subagent, the "research excepted" carve-out, the `research/<name>` branch). Cite the `SKILL.md`. **Survives** — `wayfinder/SKILL.md` could not have been in the stale cache, since the skill didn't exist until v1.1 (Jul 8).
2. **Its two hard caps (100K/ticket, 1 ticket/session) are picked, not derived** — [[m8-cap-at-its-own-floor]] from outside. **Survives**, with one downgrade: re-fetch `.out-of-scope/question-limits.md` before repeating the tension.
3. ⛔ **RETRACTED and replaced:** three GitHub API endpoints agreed with each other and **all three were one 2.5-month-old snapshot**. Concordance among endpoints of one system is **one reading, not three**.
4. **One idea worth stealing:** the fog-vs-ticket test — *"can you state the question precisely now, not whether you can answer it."*

## ⛔ Fork to Dave — three, in priority order

1. **★ Does the two-fetch staleness control earn a place?** Before reasoning about whether a remote artefact is current: fetch one thing the claim predicts **exists** and one it predicts is **gone**. Both resolving ⇒ cached view. It is two fetches and it would have caught this. §5.3. **Unruled, and I am not enacting it.**
2. **Does "fog" earn a row in `_FIXED-FLEX-CHARTER.md`?** We have words for *ticketed* and *out of scope*; we have **no single word** for *"known to be coming, not yet sharp enough to state"* — currently "floated"/"unruled"/"UNPROVEN"/"owed" depending on the author. One row, not a section. §7.1.
3. **Mine to press ([[feedback-press-on-deferments]]):** grep our gates for a `MEMORY.md` index↔file drift check. **This survived the retraction intact** — it never depended on his repo. ~15 min, one sub. Still the only item here I would defend spending money on today.

---

## Residual / risks handed forward

- **§8 U1–U5 remain open** and were **not** run in the correction pass (no headroom — see the gauge). U1 in particular now needs a **fresh** fetch of `setup-matt-pocock-skills/SKILL.md`: my earlier read of the surrounding tree is void.
- ⚠ **Anything in the note sourced from artefacts D, E, H, or I is stale and marked so in §1.** The withdrawn minor points were: the "22 skills" arithmetic, the "Linear vs GitLab" inconsistency, and the star/fork counts.
- **§6's Shape Up mapping rests on a search summary, not a full chapter fetch.** Safe as a table; re-fetch before quoting a line of it in public copy.
- **[[dave-public-positioning]]:** this note is internal and names mechanism freely. Public copy stays abstract.
- ★ **The transferable lesson, if only one survives:** [[instruction-right-cause-wrong]] — *documenting a defect is not immunity to it.* §9 risk 4 of the first draft named the exact control I had not run, and I shipped anyway, because the finding flattered a lesson I already held. That risk line is left **standing verbatim** in §9 as the evidence.
