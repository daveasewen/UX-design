# `#226`-digest — dream pass 10 digested to one screen for Dave's sitting

session: `#226` · 2026-08-30
window: conductor window #226 (Opus digest sub)
sub index: `digest`
brief: dispatched in-chat by the #226 conductor — no brief file was written; the brief's terms are
restated verbatim in VERDICT below so this report is readable without it
tokens: `UNMEASURED — this sub has no read on its own `message.usage`; `knowledge/_checkin.py` was
deliberately NOT run because it appends to a counted dataset and a digest sub must not move the
gauge's own population`

## VERDICT

**DONE.** Dream pass 10's four proposals — `notes/_dream/2026-08-30-proposals.md`, all four still
`status: floated` — are digested into one review page at
`reviews/DREAM-PASS-10-DIGEST-2026-08-30-v1.html`, in plain prose with the ID codes set small
beside the words rather than carrying the decision. Each proposal gets: one plain sentence, what
enacting it would change by named file and line, what it costs, what could go wrong with the
consequences replayed rather than gestured at, and its current status with any answering ruling
quoted. **The hard fence held in full**: nothing was enacted, promoted or marked ruled;
`knowledge/_rulings.json`, `GOOD-MORNING.md`, `_CARRIES.md` and `dist/` were not touched; no
generator and no `_build_all.py` was run; no git operation beyond read-only `log`; no commit; no
`_state.json` row. Exactly two files were written — the review page and this report.

The one thing I could not do is put pixels on screen: the sandbox root filesystem is at **100%,
0 bytes available**, so the Playwright chromium shell could not be installed and the light/dark
render is **UNPROVEN by screenshot**. It is proven *structurally* instead, at the exact point where
this class of page breaks — see finding 6.

COUNTS: findings 8 · ruling-shaped 9 · UNPROVEN 4

## What was done

1. **Located the pass output.** `notes/_dream/2026-08-30-proposals.md`, 28,174 bytes, mtime
   `Aug 30 07:30`, read in full. Provenance line `local_85a77eb9-…` · 2026-08-30 · `status: floated`.
   Four proposals P1–P4 plus nine checked-clear items (gg1–gg9) and a Method section.
2. **Read the governing rulings out of the store**, not out of the proposals file's quotations:
   `s218-D7`, `s223-D2`, `s223-D3`, `s223-D7`, `s224-D1`, `s224-D2`, `s225-D1`, `s225-D2`,
   `s225-D3`, `s219-D4`, `s129-D5`, `s125-D1`. Store stands at **279 entries** (the pass read 276 —
   three rulings have landed since it ran, all three of them `s225-D*`).
3. **Re-measured every figure** against the working tree rather than reproducing the pass's numbers.
   The pass measured at `48df9c6`; HEAD is now `e29c25b`. See finding 1.
4. **Read the review-page idiom** from `reviews/RUNG-ENACT-2026-08-27-v1.html` and the theme-flip
   idiom from `reviews/SITTING-220-2026-08-27-v1.html:2633`, and followed both.
5. **Wrote** `reviews/DREAM-PASS-10-DIGEST-2026-08-30-v1.html` (45.8 KB, versioned `-v1`, nothing
   overwritten) and this report.
6. **Declared the tree at close, and proved which changes were not mine.** `git status --porcelain`
   shows my two untracked files, plus `knowledge/_probe/session-226.json` (untracked) and three
   modified append-only logs: `knowledge/_graph-mark-observations.jsonl`, `notes/_REHEARSAL-LOG.jsonl`,
   `notes/_dream/_GRADE-DECISIONS.jsonl`. **None of the four is mine.** The probe file and two logs
   carry 10:33 mtimes from the conductor's own `_checkin.py`; `_graph-mark-observations.jsonl`
   appended at 10:50, close enough to one of my calls to be worth disproving rather than assuming, so
   I drove it: size and mtime recorded, `import _capture_gate, _gen_chain` run, both re-read —
   `395856 → 395856`, mtime unmoved. The appends are the conductor's concurrent memento retrievals
   (`"query": "residual carries"`, a query I never issued). I staged, reverted and cleaned nothing.

## Findings

**1. The tree moved under the pass, and all four findings survived the re-measurement.**
HEAD is `e29c25b` — `after #225 2026-08-30 — #225: v1.0.3 ratified and baked, and the carry list
left the banner` — not the `48df9c6` the pass measured against. Every figure on the review page is
my own reading at `e29c25b`; where it differs from the pass's, the page shows both.

**2. P1 re-measured, and it is marginally better than the pass reported but the shape is identical.**
Importing the gate's own `SUBREPORT_COUNTS_RE` / `SUBREPORT_REPLAY_RE` / `SUBREPORT_QUESTIONS_RE`
from `knowledge/_capture_gate.py` and applying them to every filed report (`_TEMPLATE.md` excluded):

| population | n | COUNTS | REPLAY | QUESTIONS |
|---|---|---|---|---|
| all filed reports, mine | **67** | 31 | 24 | 29 |
| all filed reports, the pass's | 64 | 28 | 21 | 26 |
| basename `>= 2026-08-28`, mine | **18** | 6 | 6 | 7 |
| basename `>= 2026-08-28`, the pass's | 15 | 3 | 3 | 4 |

Three reports landed between the pass and me. The post-fix rate rose from 20/20/27% to 33/33/39% —
still under half, and still worse than the corpus rate.

**3. P1 carries a trap the proposal names but does not weight, and I have weighted it on the page.**
The failure mode is a migration from FIELD LINE to SECTION HEADING (`## REPLAY-THESE`). A heading
has no `<path> (~N tk)` items beneath it, so **the priced half is genuinely absent, not merely
unparsed**. Widening `SUBREPORT_REPLAY_RE` to accept the heading therefore buys a green parse over
a deferral that is still silent — which is the precise thing `s218-D7` built the line to prevent
("Stub carries a priced REPLAY-THESE line so deferral is declared"). This is a
[[instrument-without-a-consumer]] shape wearing the opposite costume: not a gate that cannot fail,
but a gate that would newly pass on the strength of the decoration alone. It is ruling-shaped and
is on the page as such.

**4. P2 re-driven live, and the population is still empty at the new HEAD.**
```
_last_wrap_commit('.')  →  ('e29c25b146903f9800f34796fdd6560284375b16',
                            'after #225 2026-08-30 — #225: v1.0.3 ratified and baked, …')
_changed_since('.', <that sha>, 'notes/_subreports')  →  []
```
`git log -n 150 --format='%s' | grep -c '^after #'` → **130** (the pass got 129); of those,
`grep -ci wrap` → **11**. `WRAP_COMMIT_SUBJECT_RE = re.compile(r"^after\s+#\d+\b")` confirmed
verbatim at `knowledge/_capture_gate.py:4657`; the two documented shapes confirmed at
`knowledge/_git_commit.sh:138–139`. Two consumers confirmed by grep: `:4386` (`regen_serial_check`)
and `:4710` (`subreport_citation_check`).

**5. P2's proposed key is a guess, and I flagged it as one.** The proposal suggests keying on the
commit that moves `GOOD-MORNING.md`'s ★ LATEST banner. That is a *suggestion*, not a measurement —
and `s225-D2` (ruled this morning) moves the carry list out of `GOOD-MORNING.md` into a generated
home, changing what that file holds and therefore which commits touch it. Building on the suggestion
without probing it first would inherit the same non-specificity in a new costume. Named on the page
and in the questions below. Also flagged there: **landing P2 before P1 makes the citation check
start grading a corpus that is two-thirds unparseable**, so the ordering of the two is a real
choice, not a detail.

**6. P3 re-derived, and the sentence is unchanged.** From this seat:
`_gen_chain.build_verdict_line()` returns `⛔ **BUILD VERDICT: 75 of 140 steps green (#62,
`18c7789`) — 65 steps have NEVER been in a green verdict.** …` verbatim, and
`_gen_chain.VERDICT_SHA` is `"18c7789"` with its defence comment at `:277–279` intact. **The
sharpest thing about P3 is not in the proposal**: its option (c) — re-point `VERDICT_SHA` by hand —
is the shape of the act `s125-D1` explicitly rejected, and that ruling carries a `watch` field
written against exactly this: *"A future session 'helpfully' correcting 75 to 98 by hand would enact
the alternative Dave rejected, under cover of tidiness."* The proposal names (c) as "the minimum"
without surfacing that a standing ruling watches for it. It is on the page in Dave's own words.

**7. P4 is PART-ANSWERED, and I traced exactly which part.** `s225-D1` (2026-08-30, in the store,
`status: ruled`) says verbatim: *"This entry also answers dream pass 10 P4's concern for THIS cut:
the fresh ratify word lives in the store, not only in a generator comment."* So the half of P4(a)
that asked for the word to be inscribed is **DONE**. Two things remain open, verified live:
- **The key still points elsewhere.** `knowledge/_release/_gen_pack_manifest.py:612` reads
  `"v1.0.3": "s224-D1",` and `knowledge/_release/_pack_manifest.json` publishes
  `"RATIFIED — s224-D1 names v1.0.3 in the store; s219-D4(2) satisfied by the store, not by prose"`.
  `s225-D1`'s own enactment note records that key, so this is **by Dave's word, not drift** — but
  the sentence the machine publishes names the *naming* ruling, which `s223-D3` is precisely the
  ruling that distinguishes from the word.
- **P4(b), the re-checker, was never built.** `ratification_status()` (`:626–643`) still checks only
  that the keyed id exists with `status == "ruled"`.

**8. P4(b) has a consequence the proposal does not state, and it stops a release.** The proposed arm
refuses when the keyed ruling's evidence names an earlier session than the cut. `s224-D1`'s evidence
reads `"chat #224 2026-08-29"` — earlier than the #225 ratify. **So enacting (b) against the key as
it stands today would flip the manifest to PROPOSED**, and `apollo-spider/build-designer-pack.sh:152`
is `ratified || die`, so the next `--release` would die. The guard must land *after* the key moves,
never before. Mitigating and also verified: `s223-D8` requires PROPOSED and RATIFIED to pack
byte-identical content (asserted at `_gen_pack_manifest.py:3211`), so a status flip does not disturb
the shipped v1.0.3 bytes — the refusal is at the build script only. This ordering is the single
most actionable thing in the digest and it leads the P4 consequences on the page.

**Bonus, not a proposal — declared because it will be visible the moment Dave flips the page to
dark.** In canon's `[data-theme="dark"]` block, `--text-secondary` is `#FFFFFF`, identical to
`--text-default`, and `--border-subtle` is `#808080`, identical to `--border-strong`. So the page's
`--ink`/`--ink-2` and `--line`/`--line-2` pairs **collapse to one value each in dark**. Hierarchy on
the page is therefore carried by weight and by rule in dark rather than by ink. This is canon's own
behaviour and every existing review page inherits it; I did not work around it and I did not
"fix" it. Named here so it reads as known rather than as a defect of this page.

## RULING-SHAPED QUESTIONS

⛔ **None of these is decided. Nothing below was enacted, and no proposal was marked ruled.**

1. **P1 — fix the gate, or fix the writing?** (a) Widen `SUBREPORT_REPLAY_RE` and
   `SUBREPORT_QUESTIONS_RE` at `knowledge/_capture_gate.py:4655–4656` to meet where subs actually
   write (~small; the #221 remedy applied to its two siblings). (b) Leave the patterns alone and
   tighten `notes/_subreports/_TEMPLATE.md` and the sub briefs so subs write the field form (~small,
   slower to take effect, but keeps the priced replay items alive). **No recommendation offered** —
   the pass proposes (a); finding 3 is the reason (b) is not obviously worse.
2. **P1 — if the gate is widened, must the priced items survive?** Yes/no on accepting a bare
   `## REPLAY-THESE` heading with nothing priced beneath it. This is the whole value of the line.
3. **P2 — which mark identifies a wrap?** (a) The `GOOD-MORNING.md` LATEST-banner move, as proposed
   — cheap but unprobed and destabilised by `s225-D2`. (b) A wrap-specific token in the subject.
   (c) A git trailer on the wrap commit. **No recommendation offered**; (a) needs one probe over the
   log before it is built either way.
4. **P2 — which lands first, P1 or P2?** P2 first gives an honest red on the next wrap; P1 first
   gives a quiet landing. Both defensible; it is a temperament call.
5. **P3 — (a) generate the anchor, (b) stamp it with an expiry, or (c) re-point `VERDICT_SHA` by
   hand?** The pass recommends (a) with (b) as fallback. **⛔ Dave should see finding 6 before
   picking (c)**: `s125-D1`'s `watch` field is written against that motion.
6. **P3 — if (b): how many sessions old is too old?** The refusal needs a number and the number is
   Dave's.
7. **P4 — does `RATIFY_IDS["v1.0.3"]` move to `s225-D1`?** Leaving it at `s224-D1` is defensible
   (`s225-D1`'s own enactment note records that key), but then the pack publishes the naming ruling
   as its ratification. One line either way.
8. **P4 — is the re-checker built, and when?** **⛔ If yes, it must be sequenced AFTER question 7,
   or the next `--release` dies** (finding 8).
9. **The B3 observation from gg5, forwarded not floated.** `ALERT_LIST_GRADES = ("STALE",)` at
   `knowledge/_gardener.py:154` is the only arm that names a hook, and STALE has been **0 across all
   three grading cycles** while AGING went 1 → 16 → 33. The alert has never listed anything. The
   pass deliberately did not float this because it is the B3 review's own subject; it is on the
   digest page under "also in the pass" so it reaches Dave's eye at the sitting.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN — the light/dark render was not photographed.** The sandbox root filesystem is at
  **100% / 0 bytes available** (`df -h /` → `9.6G 9.6G 0 100%`), so `python3 -m playwright install
  chromium-headless-shell` failed twice — `ENOSPC` writing to `/var/tmp`, then `Download failure,
  code=1` when redirected to the `/sessions` volume (the node driver still stages through the full
  root fs). Per `knowledge/_RUNBOOK-render-verify.md` this is the sanctioned recipe and it is
  environment-blocked, not skipped. **Price to prove: one render pass from a seat with disk — two
  screenshots, light and dark, ~340 MB browser download plus ~3 tool calls.**
  What IS proven instead, statically and at the exact point where this class of page fails
  (the #220 black-on-black bug): all six canon tokens the page aliases —
  `--background-default`, `--surface-subtle`, `--border-subtle`, `--border-strong`, `--text-default`,
  `--text-secondary` — are redefined inside canon's `[data-theme="dark"]` **attribute-selector**
  block (`knowledge/canon/canon.css:660`, spanning 197 lines), which matches `<body data-theme="dark">`
  directly; and the page declares its own `--ink`/`--line`/`--page` tokens on that **same element**,
  so the flip re-resolves rather than leaving light values substituted on a child.
- **UNPROVEN — P2's LATEST-banner key.** Whether the wrap commit is reliably the one that moves
  `GOOD-MORNING.md`, and whether `s225-D2`'s carry-list move changes that, was not tested.
  **Price: one `git log --format=… -- GOOD-MORNING.md` over 150 commits cross-checked against the
  11 wrap-mentioning subjects, ~2 minutes.**
- **UNPROVEN — whether P3 option (a) is buildable at all.** Whether any machine-readable record of
  green build verdicts exists to derive an anchor from was not established; if none exists, (a)
  collapses into (b). **Price: one sweep of CI artefacts and `knowledge/` for a verdict record,
  ~3,000 tk.** ⛔ Not settled by running `_build_all.py`: the chain forbids partial runs, the sandbox
  cannot complete one inside a call boundary, and a tiktoken-less run reproduces the very artefact
  that caused P3.
- **CLAIMED, not re-driven — the consequence chains for P1 and P2.** Finding 3 (widening buys a
  green parse over a silent deferral) and finding 5 (P2 before P1 yields a red) are reasoned from
  the code and the measured rates as read, not driven by mutating the gate and running it.
  **Re-driving costs ~1 gate run each on a scratch copy.** Finding 8's chain, by contrast, IS
  traced end to end: the evidence string, the `ratification_status()` body, and the
  `ratified || die` line were each read.
- **NOT CLAIMED — the pass's own method.** I did not re-verify the pass's transcript reading, its
  gg1–gg9 checked-clear sweep, or its `_validate_wiring.py` and `_gate_doc_rows.py` runs. Those are
  reported on the digest page as the pass's findings, attributed to it, not as mine.

## Evidence

No evidence files: every claim above quotes its probe inline, and every probe is a read-only command
re-runnable from the repo root. The two written artefacts are
`reviews/DREAM-PASS-10-DIGEST-2026-08-30-v1.html` and this report.

REPLAY-THESE: `reviews/DREAM-PASS-10-DIGEST-2026-08-30-v1.html` (~9,500 tk — the sitting surface; Dave reads this one, not this report) · `notes/_dream/2026-08-30-proposals.md` (~11,000 tk — only if a proposal is promoted; the digest carries every figure Dave needs to choose) · `knowledge/_rulings.json` § `s125-D1` `watch` field (~400 tk — before anyone picks P3 option (c)) · `knowledge/_release/_gen_pack_manifest.py:612–643` (~900 tk — before anyone sequences P4)
