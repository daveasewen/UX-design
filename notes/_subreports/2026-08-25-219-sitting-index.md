# `#219` sitting index — every call open to Dave's eye today, on one surface

**Deliverable:** `reviews/SITTING-219-2026-08-25-v1.html` — a single review page indexing **34 open
calls**, grouped by what each one costs him: 11 want his eye, 18 want one word, 5 want his word on
the record. Nothing was committed.

COUNTS: findings 6 · ruling-shaped 0 · UNPROVEN 3

⛔ **This lane put NO question of its own.** Every card is a call that was already open when the
sitting started, quoted from a filed report, a sign-off row, or a live control on another page, with
a link to the surface where the call is actually made. **Ruling-shaped count is 0 by design** — a
lane whose job is to index Dave's open questions must not add to them.

---

## VERDICT

The page renders in all four themes × light/dark with **0 page errors, 0 console errors, 0 failed
requests**, **65/65 links resolve** (files exist *and* the named anchors exist on the target pages),
and the page ground is **byte-identical, in all six measured theme/mode combinations, to the page
its chrome was copied from**. The chrome is copied, not re-drawn.

---

## What was built

`reviews/SITTING-219-2026-08-25-v1.html` — hand-authored, **no generator**. The page IS its own
source, and its header comment says so. That is a deliberate choice, declared: a one-sitting index
whose content is a snapshot of one day's open calls has nothing to regenerate *from*, and inventing
a generator for it would create a second home for facts that live in the seven filed reports
([[write-once-principle-floated-192]]).

**The chrome is COPIED, never re-drawn** ([[specimen-starts-from-reference]]):

| element | copied verbatim from |
|---|---|
| sticky `header.app`, `.ctl`, `.seg` theme/mode switch, the `--page`/`--ink`/`--sp-*` palette block, the child-ink restatement rider, the hash router `<script>` | `reviews/GALLERY-COMPARE-2026-08-25-v2.html` |
| the `.sx-tag` / `.sx-tag-o` / `.sx-tag-p` badge grammar | `knowledge/_render/_bento_recut_219.py::RECUT_CSS` |
| the "owner + what an answer mints, on the card's own face" card contract | `_bento_recut_219.py::open_control_html` |

⛔ **No selector on the page names a canon component, a `--bento-*` dial or a tile class.** Every
page-local rule is prefixed `.sx` or names page furniture, so nothing here can reach a wall or a
component — the same fence the re-cut module writes into its own CSS header.

### The header line, as briefed

> **34 open calls, waiting on you.** — **Nothing on this page is ruled by this page.**

and, restated in the footer, that no question is invented and none the store has already answered is
re-put.

---

## How the 34 were derived

**Sources read, per the brief:** `knowledge/_REVIEW-SIGNOFF.md` rows `W-136`/`W-137` and the bento
sitting rows · the live controls on `reviews/BENTO-CANON-2026-08-25-v4.html`, `-v5.html`,
`GALLERY-COMPARE-2026-08-25-v2.html`, `SEGMENTED-ADOPTION-2026-08-25-v1.html`,
`UNCONSUMED-MINTS-2026-08-25-v1.html` · the RULING-SHAPED QUESTIONS section of **all seven** `#219`
sub-reports · `knowledge/_render/_bento_recut_219.py::LEDGER`.

**The re-cut lane's ledger was reused rather than re-derived**, as the brief directed. Its `state`,
`receipt`, `residue`, `owner` and `mints` fields are the source of truth for the six bento cards, so
the index cannot disagree with the pages it links to — and `open_control_html`'s refusal (a settled
question may not be re-put as a live control) already fenced that set.

**Every non-ledger item was probed against the store before it was listed.** `knowledge/_rulings.json`
(250 rulings) was searched by term for each candidate; the readings that mattered:

| candidate | store reading | verdict |
|---|---|---|
| `.lg` corner map | `s201-D1` mints the xs/s/m/l scale, `s199-D3` rules the curve match is the point — **neither maps the legacy names onto it** | OPEN |
| card padding for 3 themes | `s201-D4` ratifies the formula; `s200-D3` narrows the mint to **console only**, and says the other themes' outputs "remain PROPOSAL-ONLY … open until Dave tunes or rules them" | PART RULED |
| justified-row re-pack / rhythm | `s217-D5` rules the **mode** into existence, silent on both | OPEN |
| tail vs whole wall | **0 hits** in the store | OPEN |
| two-wraps grammar | **0 hits** | OPEN |
| chain-size gate assertion | **0 hits** | OPEN |
| gallery role default | `s218-D6`(4) scopes itself: *"the GALLERY ROLE's s217-D3 exemption elsewhere is untouched until he says wider"* | PART RULED |

⛔ **`s219-*` rulings in the store: none.** Nothing ruled today could have closed an item behind this
lane's back.

**Dedupe:** several reports restate each other. `W-142 Q3` (stacked area) and lane 4 §4.1 are one
card. `s149-D1`'s stale status appears as lane 5 finding 7 **and** seam 3 §6 — one card, citing both.
Lane 3's rider (the render-verify pothole → runbook stratum) was **dropped as already discharged**:
seam 1 §⑤ landed it as the fifth stratum, which this lane then used to render.

**Every card cites its report by path**, as briefed — all seven are cited at least once.

---

## Findings

**1 · A drifting grey that was a transition, not a colour — and it would have been reported as a
defect.** The first theme sweep measured `body` backgroundColor as mid-greys that *changed between
runs and between viewports* (console light read `184,184,184`, then `114,114,114`). A computed style
cannot be random, so the reading was the artefact: canon transitions the body ground, and the sweep
measured 50 ms after flipping the theme, catching the transition mid-flight. **Re-measured at 800 ms
settle, every value lands exactly on its token.** ★ The general shape: *a computed-style probe taken
straight after a state change measures the animation, not the state* — and it produces a plausible
wrong number rather than an error, which is the dangerous kind.

**2 · The parity check is what proved it, not the re-measure.** Re-measuring my own page at a longer
settle would only have shown my page changed its mind. Measuring **`GALLERY-COMPARE v2` under the
identical probe** showed the *source* page drifting the same way — which is what turned "my page has
a grey ground defect" into "my probe has a timing defect." Copying chrome buys a control specimen for
free; the check is only worth running because the chrome was copied rather than re-drawn.

**3 · An anchor check is a different check from a file check, and only one of them was cheap to get
wrong.** All 65 hrefs were verified in two tiers: the file exists on disk, **and** where the href
carries a fragment, `id="<frag>"` is present in the target file's bytes. **14 of the 65 carry a
fragment** — 11 pointing into another page, 3 into this one. A link-check that stopped at "the file
exists" would have passed a link to
`#squaring` on a page that had renamed the section ([[unmatched-grep-is-not-an-absence]] in its
positive form: matched ≠ present, so quote the line).

**4 · `Q9` is a Dave-owned open call that no page puts as a control — and it was nearly missed.**
The re-cut ledger carries `Q9` as `PARTIAL`, `owner="Dave"`, with a `mints` field, but its
`asked_as` says *"Not asked on these pages at all — recorded here so nothing on them can be read as
re-opening it."* So it never appears in the recut report's list of live controls (items 3–7 there are
Q2/Q3/Q6/Q11/Q12, the five the brief names). **It is listed here as EYE 5**, pointed at the matrix
explorer where the construction actually lives, because dropping a Dave-owned open call from an index
*of Dave-owned open calls* is the worse of the two errors. Declared so the conductor can strike it in
one line if he reads the scope differently.

**5 · `W-137`'s three named calls are all answered — the row is open for a different reason.** The
sign-off row still reads ⬛ AWAITING, and a fast read would list three photography calls that Dave
already settled at `s218-D6`. The row's own closing sentence says why it stays open: *"the three
CALLS are answered, Dave's eye over the page itself is not, and a wrap closes no row of his."* **The
card says exactly that**, and lists no settled call as open. [[premise-ages-faster-than-rule]] — the
row's ⬛ badge is not the same fact as the row's contents.

**6 · The re-cut lane's refusal is a reusable fence, and it did fence this page.** `open_control_html`
raises `REFUSED: <key> is RULED — a settled question may not be re-put as a live control`. Six of the
twelve ledger rows are `RULED` and are struck on their own pages; none of them appears as a card
here. The fence was not re-implemented — it was **read, and obeyed by construction**.

---

## Verification — driven, not claimed

**Render-verify per `knowledge/_RUNBOOK-render-verify.md`, fifth stratum.** `tiktoken` installed
first. `/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu` **`ls`'d before trusting it** (2
entries: `libXdamage.so.1`, `libXdamage.so.1.1.0` — not hollow), then confirmed with `ldd | grep "not
found"` printing **nothing**. Fresh session-suffixed farm `/var/tmp/fonts-s219idx` (10 symlinks) +
conf with the `<include>` present.

**Font control probe — asserted with controls, not a boolean:**

| probe | measured | reading |
|---|---|---|
| `HSBC_MtUnivers_Latin` | **347** | the real cut |
| `"Univers Next HSBC"` | **347** | alias resolves |
| `"Univers Next for HSBC"` | **347** | alias resolves |
| `DejaVu Sans` — control | 375 | genuinely different face |
| nonexistent face — control | 301 | default fallback |

Identical at **1180 and 480**. Both aliases land on the target and neither lands on the
nonexistent-face number, which is the assertion that catches a silent fallback.

**Page health:** `pageerrors: []` · `console (error/warning): []` · `requestfailed: []`, at both
widths.

**Links:** `65/65` resolve. **51 file-only · 11 cross-file with a fragment · 3 same-page anchors**,
and **every fragment is present in its target's bytes**. 0 bad. *(Counted by probe, not typed — an
earlier draft of this line carried a wrong figure and was corrected against the measurement,
[[measure-dont-convert-units]].)*

**Structure, read back from the live document:** `article.sx-card` = **34** · `main section` = **3** ·
`main a` = 63 (65 total hrefs − 2 stylesheet `<link>`s). Key prefixes counted in the source:
`EYE` 11 · `WORD` 18 · `REC` 5 = 34, matching the header's printed count.

**Theme × mode ground parity, measured at settle, against the source of the chrome:**

| theme/mode | `SITTING-219` body | `GALLERY-COMPARE v2` body | token |
|---|---|---|---|
| mono light | `255,255,255` | `255,255,255` | `#FFFFFF` |
| mono dark | `26,26,26` | `26,26,26` | `#FFFFFF` |
| console light | `255,255,255` | `255,255,255` | `#FFFFFF` |
| console dark | `26,26,26` | `26,26,26` | `#FFFFFF` |
| supercharge light | `247,246,244` | `247,246,244` | `#F7F6F4` |
| supercharge dark | `26,26,26` | `26,26,26` | `#F7F6F4` |

**Contrast, computed off `getComputedStyle` in the live document, 8 theme/mode legs:** headline ink
12.63–17.45 · body ink 6.26–17.45 · the inverted `Open · yours` tag 12.63–17.45. **Lowest reading
anywhere: 6.26:1** (legacy dark body ink). Nothing near 4.5.

**PNGs seen**, not just written: console light and console dark at 1180. The page reads in the real
HSBC cut; one defect was found **by eye** and fixed — the "Where it lives / Raised in" rows ran
together at 4px, so they now sit under a hairline rule at 8px. Re-driven green after the fix.

**Tree assertions:** `.uuid` strays in the TTF dir → **0**. Render PNGs were staged into the repo to
be read and then moved out with a same-mount `mv` into `_to_delete/` (never `rm`, never a cross-mount
`mv` — the `#138` pothole). `git status --untracked-files=all` after: **one line that is mine**,
`?? reviews/SITTING-219-2026-08-25-v1.html`.

⚠ **NOT MINE, declared for the reconcile:** `notes/_REHEARSAL-LOG.jsonl` and
`notes/_dream/_GRADE-DECISIONS.jsonl` are modified in the working tree. This lane wrote neither; both
are append-only telemetry and were already dirty. Named so the conductor does not attribute them
here.

---

## UNPROVEN / CLAIMED (ADR-0016)

1. **The page was read by eye at ONE theme (console), two modes, one width (1180).** The other three
   themes and the 480 width are asserted **numerically** — ground parity, ink contrast, zero errors —
   and were screenshotted, but the mono / legacy / supercharge PNGs and the 480 PNGs were **not
   looked at**. Bounded verification (`s172-D3`), and the residual is named rather than implied.
2. **No link was followed.** "Resolves" means the file exists on disk and the fragment's `id` is
   present in its bytes. Whether each target section still *frames* the question the card says it
   frames is inherited from the reports and the ledger, not re-verified by opening 20 pages.
3. **The 34 is a count of what these named sources carry today.** It is not a claim that 34 is
   everything open to Dave anywhere — the brief named the sources, and a call that lives only in a
   pre-`#219` document nobody cited would not appear. `_REVIEW-SIGNOFF.md` was read at rows
   `W-136`/`W-137` and the bento sitting rows, as briefed, **not end to end** (the file is 110KB).

---

## Store rows

Minted through `_state.py::add()` in the grammar of the `#219` seam rows. Next fresh id was `W-181`
per `s215-D1`.

| id | home | owner | closes_when (abridged) |
|---|---|---|---|
| `W-181` | `reviews/SITTING-219-2026-08-25-v1.html` | dave | Dave has worked the sitting from the page, or it is superseded by a later sitting index |
| `W-182` | `notes/_subreports/2026-08-25-219-sitting-index.md` | claude | retired with the `#219` record once the sitting index commits |

`W-182` is **this report**, rowed at creation — the `#185` forgotten-document class does not exempt
the document that names it.

---

## Not done, on purpose

- **Nothing committed.** Working tree left for the conductor: one untracked file
  (`reviews/SITTING-219-2026-08-25-v1.html`), one new report, two store rows.
- **No ruling, no threshold, no promotion, no reword of any Dave-owned row.** The DO-NOT-RULE list
  binds and nothing on it was touched. `knowledge/_rulings.json` was **read only**.
- **No `_LIVE-STATE.md` edit** — residual ③'s discharge is listed as `WORD 1`, which is the call
  itself, not its execution.
- **No page linked from the index was modified.** The index points at them; it does not re-cut them.
- **`_build_all.py` end-to-end was not run.** This lane added no generator and no build step, so
  there is nothing of its own for the serial to regenerate.
