# #149 — the identical failure that was one banner, and mono joining the ink camp

provenance: #149 · 2026-08-11
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #149 · ledger: `knowledge/_rulings.json` § `s149-D1` ·
banner: `GOOD-MORNING.md` ★ LATEST #149. This dossier holds the WHY and HOW; the terse records hold
the WHAT. Authored by the delegated OPUS wrap sub. Every claim below is either verified first-hand by
this sub against the artefact (and says so), or attributed to the conductor and marked as relayed.
**This sub ruled nothing** — `s149-D1` is Dave's, made in-window, and was already written to the
ledger by the conductor before this wrap opened.*

## The arc

#148 drove all 110 build steps for the first time and came back with **8 gate reds**. #149 opened as
the triage lane for those reds. It closed three of them — 105, 106 and a fresh re-measurement of 63 —
ruled one colour question, and found one new defect. The interesting part of the session is not the
count; it is that two of the three "closures" were **diagnoses of the instrument, not of the subject**.

## ① The "identical failure" that was never two failures

#148's most alarming finding was recorded as *unruled*: **steps 105 and 106 failed with the identical
message**, and 106 is the *selftest* for 105's delta-audit. The written worry was the right one —
[[mutation-tests-the-clause-not-the-feature]] — *a selftest that cannot fail independently of its
subject is echoing it, not testing it.* #149's job was to establish whether that was what was
happening.

**It was not.** The identical text came from the runner's own **shared `_PKGDELTA` banner**: both
steps print through the same banner helper, so a red in either prints the same headline. The two
steps were failing for **two different reasons**, and one of them was not a defect in the audit at
all — **106's red was a clean-repo precondition**, not a broken clause.

★ The lesson worth carrying: **two steps that print the same string are not thereby the same finding.**
The evidence for "identical" was the *output*, and the output was a shared surface. This is the
[[a-crash-is-not-a-fail]] family read from the other end — a message that is not specific enough to
discriminate makes two unlike states look like one.

The real defect underneath was a genuine drift: `chain_parts` in the packaged shim had moved on from
its declared port commit. So the remedy was a **re-port**, enacted on Dave's word:

- both `_gen_chain.py` copies (`memento-package/machinery/` and
  `memento-package/claude-plugin/memento/machinery/`) — **154 lines** each,
- both `_search_core.py` copies — **14 lines** each,
- the `chain_parts` shim splice in **both** `_capture_gate.py` copies,
- provenance moved **`c853b0a` → `9dcf62d`**, *including the gate's own constant* `PORT_COMMIT_A` in
  `knowledge/_validate_package_delta.py`.

★ That last clause is the one that matters. The gate parametrises its expectation on
`PORT_COMMIT_A` precisely so a re-port cannot be done in the artefact and forgotten in the checker
(the #114 note in that file says so in as many words). Re-porting the copies **and** advancing the
constant is one act; doing only the first would have left the gate red while the record said "fixed".

**Verified first-hand by this wrap sub, not quoted:**
`python3 knowledge/_validate_package_delta.py` → *"memento-package delta-audit: 0 failure(s) · ✅
VERBATIM SET byte-identical (both copies) · shim provenance clean (both chains) · copies identical to
each other · no unknown files"*, **rc 0**; `--selftest` → *"✅ `_validate_package_delta` selftest: all
bites pass"*, **rc 0**, with ARM2(a)–(d) quoting `9dcf62d` in their own failure text. Both were also
re-driven and replayed by the conductor in-window.

⚠ **Declared, not fixed:** the file's prose header still narrates the chain as *"@ commit c853b0a
(re-ported #114)"* at `:20` and `:87` while the live constant at `:88` reads `9dcf62d` with its own
`★ #149 RE-PORT` comment. The **checked** value is the constant; the stale words are docstring. It is
named here rather than edited because gate machinery was on this wrap's DO-NOT-RULE list — and
because prose staler than its own code is exactly the class this project keeps banking.

## ② Red 63 re-measured, and it is WORSE than the record said

The state-contrast red (step 63) was carried into #149 with the Aug-8 audit's **14 text failures** as
its size. That number was stale. A fresh drive — composed in chunks **through the gate's own
functions**, with the return code computed from *its* expression rather than a re-implementation —
produced, at 2026-08-10 22:30:

**20 ❌ text failures · 32 🟡 icon warnings · 14 ⬛ declared holes, across 75 snippets.**

Verified first-hand by this sub against `knowledge/_STATE-CONTRAST-AUDIT.md`: the headline reads
*"20 text failure(s) across 75 snippet(s)"*, and `grep -c` returns 20 / 32 / 14 for the three markers.

The delta is not noise, and its shape is instructive. **Banner went 4 → 8**: the old record showed
only `[light|dark]/pressed` at 4.09:1; the new one shows **hover 2.72:1 and pressed 2.47:1 in both
modes**. The failures did not appear — **they were always there and the older instrument could not
see the hover leg on that surface.** Selection-controls likewise 8 → 10, with
"Accept terms & conditions" now failing on the *light* legs it previously only failed on in dark.

★ Two carried lessons fire here at once. [[planning-estimate-is-not-a-measurement]] — the 14 was a
figure from a document, not from a run. And [[conclusions-are-debt-s129-d5]] — *"verified" is a
property of a moment*; an audit file is a dated measurement wearing the grammar of a fact.

## ③ `s149-D1` — mono error joins the ink camp

Red 63's biggest single family is the mono error surface, so triage ran straight into a colour
question that only Dave can answer. The lane built a series of live controllers (v1 → v5) and he
ruled from them. **The standard, verbatim: *"the standard is we use dark text on `#F6604C`"*, scoped
*"this is right for mono only"*.**

What it settles (full text in `knowledge/_rulings.json` § `s149-D1`):

- **Mono banner** — fill **stays `#F6604C`**; text/label **`#1A1A1A`**; hover and pressed become
  **white transparencies at 8% / 14%**. Measured **5.55 base · 6.04 hover (`#F76D5A`) · 6.41 pressed
  (`#F77665`)** — ★ **contrast RISES with state**, which is the inversion that made the old treatment
  fail: it was the *hover* and *pressed* legs, not rest, that were breaking. The `s130-D4`
  percentages survive intact; what changed is the **wash medium** — ink-derived → white-fixed.
- **Mono marks** take the `s145-D1` `rag/error-ink` rung on **both legs**: light `#DA1A00` (5.09 on
  white), dark `#F6604C` (5.55 on `#1A1A1A`).
- **Mono tab badge** — `#F6604C` with a `#1A1A1A` numeral, **mode-invariant at 5.55 both ways**,
  plus a `.ovcount` re-point: the snippet was painting `--tabs-active` / `--text-reverse` and never
  reading its own badge seat, which is why the dark numeral was rendering at 1:1 — invisible.

**What it amends, and why the amendment is a measurement rather than a preference.** `s130-D4` moved
the mono fill to `#B92F1E` and rode the label on white. That move is **DROPPED for mono**: `#B92F1E`
against black text measures **2.89** — it is killed by arithmetic, not by taste. `s130-D5` is
TOUCHED (colour returns to the mark; labels stay ink at 17.4) and the tabs badge seat is amended for
mono (was light `#B92F1E` / dark `#CC4333`, white numeral). **Legacy `s131-D1` and console/SC
`s132-D1` are UNTOUCHED** — this is a one-theme ruling, and the four-theme constraint is why that
scoping matters [[four-themes-flexibility-is-the-requirement]].

⛔ **RULED, NOT ENACTED.** No value moved in any token or canon file this session. The ledger entry
says so in its own `status` field, and enactment is #150's lane 1: token amendments (mono banner +
badge legs) · canon consumption (wash medium, mark inks, `.ovcount` re-point) · a re-drive of
`_validate_state_contrast.py` to restate the 20-fail headline.

Four questions are recorded **open** on the entry itself, deliberately not folded into the ruling:
the dark-mode red-text policy P1/P2/P3 from v2 (narrowed by the dark-mark pick, still unruled) · v3's
glyph/bare-role follow-up (moot for mono since the fill stays put, but `s130-D4` still names
`#B92F1E` for any non-mono consumer) · whether "marks" reaches the radio dot, the switch and the
indeterminate dash · and whether the box border takes the rung or `#F6604C`.

## ④ The conductor's own defect, owned in-window

⚠ **v2 and v3 of the controller re-derived `s130-D4`, which was already settled.** Dave caught it.
This is [[survey-before-build]] recurring: the settled ruling existed, in the ledger, greppable, and
two controller generations were spent re-proposing it. The cost was not large — the same instrument
went on to produce the ruling — but the shape is the expensive one, and it is recorded as the
conductor's, not smoothed into the narrative.

## ⑤ The new defect, found and NOT fixed

`knowledge/_governs.py`'s **default lister** flags `chat #<n>` evidence as **UNRESOLVED** — verbatim:

> `evidence: chat #148 (live) - Dave's pick from the three-option set  ⛔ UNRESOLVED — points at
> 'chat #148 (live) - ...' whose FILE 'chat' does not exist — a pointer index whose pointers rot is
> worse than none`

— while the **anchor predicate and the selftest accept the same string**, because `s148-D1` taught
them to. Reproduced first-hand by this sub at wrap: one UNRESOLVED line, on the chat form, from the
default lister, at rc 0.

★ **The class: `s148-D1` was enacted in one code path and the second path never learned it.** This is
[[gate-must-quote-what-it-forbids]] seen from the other side — two consumers of one rule, one of them
updated. It goes to #150 as item ③, unfixed by this wrap because the fix is gate machinery and gate
machinery was named on the DO-NOT-RULE list.

⚠ It also means `s149-D1`'s own chat-form evidence line will read UNRESOLVED in that lister until
the fix lands. **The gate did not go red on it** — the capture gate was run and its verdict is in the
commit state — but the lister's complaint is expected, and is not evidence that the ledger entry is
malformed.

## ⑥ Artefacts, and one of them has a bug

`_review/` carries controllers **v1 … v5** plus their generators (`_gen_ruled_preview_v3.py`,
`_build_v4.py`, `_build_v5.py`). v5 is the preview Dave ruled *against* on the one-treatment
question; v3 is where `#B92F1E`-under-black was measured dead. Both are cited as evidence on the
ledger entry, which is why the directory is committed rather than left as chat-only attachments
(capture-ritual step 1, dream-pass v2 P5(b) — *a chat-only attachment is an un-retrievable citation*).

⚠ **v1 carries a `<base>` bug** — its specimens lose `type.css`. Noted, **not fixed**; it is superseded
for its purpose by v2–v5 and kept as the arc's record.

★ **A premise was wrong and it was cheap to catch:** the Playwright install from #148 **SURVIVED** in
`/var/tmp`. The standing note *"the render sandbox is FRESH every session"* did not hold here, and
#149 got a free install it had priced for. Root fs remains **95%** full. Recorded as an observation
about the premise, not as a new rule — one survival is not a guarantee, and the honest form is that
the premise is **not reliable in either direction**.

## What is resolved, and what is still open

**Resolved:** 105 and 106 are green (re-driven twice, rc 0 both) · the "identical failure" question
#148 left unruled is answered and it was the banner · red 63's size is a fresh measurement, 20 not 14
· `s149-D1` is ruled and recorded.

**Open, all of it going to #150:** the enactment of `s149-D1` (**new top**) and its four named open
questions · gate reds **30 · 36 · 45 · 51 · 82** plus the `path.star` pairing fix in the specimen ·
the `_governs.py` lister fall-through · and the whole #148 carry, ages incremented.
