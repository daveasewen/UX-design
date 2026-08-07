# #125 — the repair session, and the claim that went false three times

```
provenance: 125 · 2026-08-07
status: observed
```

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #125 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #125 ·
**Rulings:** `knowledge/_rulings.json` (`s125-D1`, `s125-D2`, `s125-D3`) ·
**Banner:** `GOOD-MORNING.md` ★ LATEST #125.
Both-way links per `_DECISION-HISTORY/README.md`.

---

## 0. What this session actually was, and why the title lies

The session was opened as **"the schematic — memento drawn whole"**: one live HTML diagram of the whole
Memento mechanism — chain, store, search, marks, gates, package — driven from the real file inventory so
it could not drift. That was #124's residual ① and Dave's own pick.

**It is not what happened.** At the opener Dave redirected: *"lets repair what we have to first."*
#125 became a **repair session**, and the schematic was never started.

This is recorded first and plainly because the alternative is worse. A session title is a **label**, and
a cold reader who finds a confident title and no artefact will spend real tokens looking for the artefact.
The title stands as the record of what the session was *opened for*; this document is the record of what
it *was*.

---

## 1. The through-line, stated before the findings that produced it

Three separate repairs this session turned out to be the same defect wearing three costumes:

> **A claim that was true when it was written, went false, and had nothing that re-checks it.**

The three instances differ in *medium* and are identical in *mechanism*:

| # | Instance | Medium | Why nothing caught it |
|---|---|---|---|
| 1 | **the 75** — the chain banner's build-step count | **prose** | the gate audits the `size:` **stamp** (regex-matched, tolerance-checked). **No gate parses prose.** |
| 2 | **the exemption reason** on `_validate_state_contrast.py` | **a code comment** | it was disproven by #124 *on its own date* and the disproof never propagated to the comment |
| 3 | **`parse()`** returning silent `null` | **a return value** | it is an **input**, and nothing re-checks an input; the `null` was treated as data |

Related and already inscribed: `no-gate-parses-the-artefact` (#122) · `assertion-propagation-gap` ·
`measuring-tool-must-not-guess` · `silent-lookup-failure-class`.

★ The reason this is worth a dossier rather than a ledger line: **each of the three was found by a
different method**, and none of the methods would have found the other two. A git archaeology probe found
the 75. A first-hand environment probe found the exemption reason. A mutation test found `parse()`. There
is no single instrument here, which is precisely why the class keeps recurring.

---

## 2. `s125-D1` — the 75, and why Dave refused the obvious fix

### The finding

The chain banner asserts **"ALL 75 STEPS ASKED AND GREEN (#62)"**. Disk, measured this session by reading
`knowledge/_build_all.py`'s AST, is **98**.

The first hypothesis was the expensive one: that 75 and 97 were counting **different objects** (registered
steps vs distinct labels), in which case the banner would not be stale, it would be incomparable. That
hypothesis had to die before anything else could proceed.

**The probe that killed it:**

```
git show 18c7789:knowledge/_build_all.py   →  len(STEPS) = 75 ·  distinct labels = 75
HEAD                                        →  len(STEPS) = 97 ·  distinct labels = 97
```

**1:1 at both ends ⇒ the same object.** The banner is simply **stale by 22**.

### The correction that was already there, and had already failed

The line had been re-stamped once before — **72 → 75** — and the act was classified at the time as a
*"Perishable reading"* (`notes/_MEMENTO-DECISIONS.md:813`). So the record had already named the class,
applied the remedy, and **the class recurred on the very line that named it.**

★ This is the dead end worth recording: *classifying a defect is not remedying it.* "Perishable reading"
told a future session what kind of thing the number was. It did not give anything the job of re-reading it.

### The ruling

The obvious move was a **third re-stamp** — change 75 to 98 and move on. **Dave refused it and ruled the
other way:** the count stops being a typed number and becomes a **generated figure** — `_gen_chain.py`
reads `len(STEPS)` out of `_build_all.py`'s AST at generation time, so the banner cannot be stale because
nobody types it.

★ The reasoning, in the general form: **a value that has gone stale twice will go stale a third time; the
fix is not a fresher value, it is removing the human from the loop that produces it.** A re-stamp buys
one session of accuracy at the price of guaranteeing the next recurrence.

### ⛔ And it was not built

The window ran out. **`s125-D1` is RULED and NOT ENACTED**, and it rolls to #126.

This left the wrap with a genuinely awkward choice, and it is worth naming because the wrong answer looks
helpful: **the honest move was NOT to quietly re-stamp the banner to 98 while writing up the ruling.**
Re-stamping is *exactly the act the ruling forbids*, so doing it "just to be accurate" would have enacted
the alternative Dave rejected, under cover of tidiness. The number is instead **marked KNOWN-STALE in
place, with a pointer to the ruling**. The record now says *"this says 75, disk is 98, here is why nobody
is allowed to just change it"* — which is uglier and true.

⚠ **Declared limit of the probe:** only the **COUNT** was proven. The banner's **GREEN verdict** was not —
a full single-process `_build_all.py` run is sandbox-impossible (~49s against the ~45s call kill), and the
single-process verdict belongs to CI on push. Saying "75 is wrong, so the green is wrong too" would have
been a second unchecked claim replacing the first.

---

## 3. `s125-D2` — the exemption whose reason was never true

### The finding

`_validate_state_contrast.py` sat in `_validate_wiring.py`'s `EXEMPT` map with a named reason: the
playwright browser download fails with `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` on all three CDNs, so the
validator cannot run in-sandbox, so it is exempt from the wiring requirement.

**#124 had already disproven that on its own date** — it followed `_RUNBOOK-render-verify.md` end to end
and rendered *and drove* a page at 1180/480. The exemption's reason was dead the moment that happened.
**Nothing propagated the disproof to the exemption.**

Sub 1 then observed the download **succeed**, with the installer throwing `EPERM … rmdir '__dirlock'`
afterwards — **a failure message AFTER a success**, which is a shape `_RUNBOOK-render-verify.md`
explicitly banks and warns about.

★ The lesson: **an exemption carries a reason, and a reason is a claim.** The wiring gate checked that
every exemption *had* a reason and was *named* and *dated*. It could not check whether the reason was
still **true** — and a stale reason is invisible precisely because the gate reports green on it.

### The enactment, and the bite it nearly caused

The validator was un-exempted and wired into `_build_all.py` with its exact-label `ROUTE_ROWS` row.
**`EXEMPT` is now empty** — and that emptiness was itself a small trap: the wiring selftest synthesised
its bites using `next(iter(EXEMPT))`, which **raises on an empty dict**. The tempting repair is to leave
one token exemption in place so the selftest keeps working; that would have been *making the test pass by
preserving the defect*. Instead `check()` gained an optional `exempt_map` parameter, so the selftest
injects its own synthetic map and **all four bites survive an empty real one**.

**Evidence, re-run at the wrap (2026-08-07):**

```
wiring gate      : 30 validators on disk · 30 wired · 0 exempt · 0 failures   rc=0
wiring selftest  : 4 bites · 0 failures                                       rc=0
_build_all.py --selftest : PASS — exact-ID routing over 98 steps              rc=0
```

Both changes were mutation-tested.

---

## 4. `s125-D3` — the input that nothing re-checked

### The finding

`parse()` in `_validate_state_contrast.py` could not read `color(srgb …)` — which is **how chromium
serialises every `color-mix()` result**. Fed a syntax it did not know, it returned `null`, and `null` was
treated downstream as a measurement.

**The mutation test is what made this undeniable**, and it is the sharpest single result of the session:

> The old code, fed `oklab()`, returned a **fabricated `{"ratio":1}` with no warning.**

Not an error. Not a skip. A **1:1 contrast ratio**, invented, indistinguishable from a real catastrophic
failure — and therefore reported as one, every build, silently.

### The ruling

`parse()` now reads `color(srgb …)`, and — this is the load-bearing half — **REFUSES unreadable syntax by
name**: `StateContrastParseError`, carrying the value, the property and the element. A refusal is reported
as **UNMEASURED: a hole, not a pass and not a failure.**

★ The general form, and it is why this is a ruling rather than a patch: **teaching the parser one more
syntax fixes today's inputs; refusing by name fixes every future input.** The set of colour syntaxes
chromium can emit is open-ended. A parser that guesses on the unknown will be wrong again; a parser that
refuses on the unknown will be *loud* again — and loud is recoverable.

### What it moved

**20 false failures removed · 4 newly surfaced and REAL · 42 pre-existing.**

Two observed reversals, both of which had been sitting in the audit as catastrophic:

- Button `.primary` hover: **1:1 → 6.01:1**
- Stepper "Next": **1:1 → 6.39:1**

⚠ The 4 newly-surfaced failures are **real and are Dave's to rule**. They were not fixed, closed or
waived at the wrap, and no threshold was touched:

- **Banner `.abtn:active` — 4.09:1 (needs 4.5), LIGHT and DARK**, `canon.css:3963` / `:3975` — new.
- Pre-existing and also real: **Tabs ×2 dark at 1.00:1** (`.cn-tabs .ovcount`, `canon.css:2496` — a
  genuine token collision, white on white in dark) · **Selection-controls ×8** (light/pressed 3.95:1 ×6,
  dark 3.66:1).

★ Note the shape of the result: **the instrument got better and the failure count went UP in the places
that matter.** A repair that only ever reduces the red count is a repair that should be suspected.

---

## 5. Two defects found, deliberately NOT fixed

Both were found while proving `s125-D3` and both were **scoped out of it on purpose**, so that the
mutation test proved **one clause** rather than a bundle. A green that covers three changes at once cannot
say which one it is green about.

**(a) `effBg` walks ANCESTORS ONLY.** It cannot see an absolutely-positioned **sibling** that paints the
selected pill, so it measures the wrong background ⇒ **32 false failures** (Segmented-control ×12, Charts
×16, View-options ×4). Real rendering is fine. This is a **geometry** defect and is distinct from
`s125-D3`'s **parse** defect — conflating them is how a fix guarantees its own recurrence.

**(b) `out[3] = <headline>` OVERWRITES** the first snippet's heading instead of inserting. The committed
`_STATE-CONTRAST-AUDIT.md` claims *"across 38 snippet(s)"* and contains **37** — `Accordion` was eaten.
The artefact is also **stale by 37**: it covers 38 snippets while `knowledge/snippets/` holds **75**.

⚠ **Two additions measured at the wrap itself, and they widen (b):**

1. With **zero** snippets in scope the same line does not overwrite, it **crashes** —
   `IndexError: list assignment index out of range`. So the defect has two faces, and only one of them
   was known.
2. `_validate_state_contrast.py` has **no `--selftest` flag**, and silently treats an unrecognised
   argument as a **snippet-name filter**. That is how the crash was reached: an unknown was *defaulted*
   rather than *named* — `measuring-tool-must-not-guess`, in the same file the session had just repaired
   for guessing.

★ The second one is the quiet lesson of the wrap: **the wrap found a fourth instance of the session's own
class, in the session's own subject file, by making an ordinary mistake.**

---

## 6. ⚠⚠ The contradiction — recorded, not adjudicated

Two Opus subs, one session, the same sandbox family, **opposite first-hand environmental readings**:

- **Sub 1:** the browser download **SUCCEEDS**; the installer then throws `EPERM … rmdir '__dirlock'` —
  a failure message after a success.
- **Sub 2:** playwright's node downloader **IS TLS-blocked** on all three CDNs, and `NODE_EXTRA_CA_CERTS`
  does **not** fix it, while `curl` reaches the same URLs fine. It installed chromium **by hand** to
  `/tmp/pw-browsers` (`PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers`,
  `LD_LIBRARY_PATH=/tmp/extralibs/usr/lib/aarch64-linux-gnu`).

**A third datapoint arrived at the wrap, and it adjudicates nothing.** Sub 2's hand-installed browser was
still present at `/tmp/pw-browsers` and a real chromium launched from it, while playwright's own default
path `~/.cache/ms-playwright/` did not exist. That says **the workaround persists**. It says nothing about
whether the downloader is blocked, **because no download was attempted at the wrap.**

⛔ **Both readings are recorded verbatim in `_LIVE-STATE.md` § OPEN. No winner was picked, nothing was
averaged, and `_RUNBOOK-render-verify.md` was NOT edited on either basis.**

★ The reasoning is the whole point of the entry. The cheap move is to pick the reading that matches the
runbook and call the other sub mistaken — which would produce a **tidy, confident, possibly false**
record, and #124 had just been burned by exactly that (it carried a TLS fence as a fact and Dave caught
it). Two first-hand observations that disagree are **evidence about the environment's variability**, and
flattening them destroys the only signal there is. A **re-verify is owed at #126**: a fresh, deliberate
download attempt whose result is written down.

⚠ Until then, **neither reading may be carried forward as a fact** — a fence inherited as a fact is a
premise, and premises age faster than rules.

---

## 7. ⛔ What we got wrong

**(a) The first repair-set probe was wrong twice, and both errors were the instrument.** It reported
*"0 test arms"* and *"1 unwired validator"*. In fact the arms are named `arm_*`, not `test_*`, and the
validator was exempt **by name** — both readings were artefacts of how the probe looked, not facts about
the repo.

It was caught before publishing. ★ **But it is the same guessing class the session was convened to repair,
committed by the session repairing it** — which is the most honest thing in this document. Knowing the
class does not immunise you against it; only an instrument that refuses on the unknown does.

**(b) `_STATE-CONTRAST-AUDIT.md` was overwritten during proving** and restored via `git show >` rather
than `git checkout`, because of a stale `.git/index.lock`. The restore was correct; the method was a
workaround, and it is named rather than smoothed over.

---

## 8. The gauge, and one datapoint that is recorded and NOT acted on

- **boot 53,681 real** (`message.usage`, first turn). ⚠ The **published floor is 75,899**, and this is the
  **fourth datapoint below it**, consistent with the post-break n=3 mean of 54,859.
  ⛔ **The re-base is DAVE'S and remains UNTAKEN. The datapoint is recorded; nothing was re-based.**
  ★ This is the discipline the whole session was about, applied to the session's own instrument: a
  measurement that disagrees with a published constant is *evidence*, not *authority*.
- FILL check-ins: **74,857 → 117,087 → 128,026 → 143,686** against the stop line **150,929**.
  **The wrap was delegated at 143,686** — roll, not ride.
- Conversation-half throughput **214,164 real**.
- ✅ Dave's quota panel GIVEN: **session 6% · all-models 10% · Fable 16%, resets Thu.**
- ⚠ `tiktoken` refused on the first `pip` attempt and installed on retry — noted, not chased.
- ★ **Delegation inversion confirmed again:** 3 subs spent ~246K subagent tokens; the conductor paid only
  their reports. **Cheap in FILL, expensive in QUOTA** — name which budget binds before choosing posture.

---

## 9. Resolved state, and what is still open

**Resolved:** `s125-D2` and `s125-D3` are ruled and enacted, with gates re-run green at the wrap.
The 75-vs-97 question is **answered** (same object, stale by 22).
The exemption's reason is **disproven and removed**.

**Open, and rolling to #126:**

1. ⬛ **`s125-D1` — RULED, NOT ENACTED.** The generated step figure in `_gen_chain.py`. Banner 75, disk 98.
2. ⬛ **The schematic v2** — generated, six subsystems; **v1 kept and tombstoned.** Dave's original #125
   pick, untouched. v1 (`reviews/MEMENTO-SCHEMATIC-2026-07-26-v1.html`, `f783008`) is hand-authored,
   referenced by no generator, asserts *"27 blocking validators in a 55-step build"* against a disk of
   **30 validators, 98 steps**, and draws a **different subject** (the dream-pass lane).
3. ⬛ **`effBg` sibling blindness** — 32 false failures.
4. ⬛ **`out[3]` heading overwrite** (plus the zero-snippet crash and the silent unknown-arg filter), and
   `_STATE-CONTRAST-AUDIT.md` **stale by 37**.
5. ⬛ **The render-runbook contradiction — re-verify.**
6. ⬛ **The 4 real contrast failures — DAVE'S to rule.**
7. ⬛ Carried: the fall-through class still has no gate · `s116-D4`/`s116-D5` · `s114-D2` · stale-mount
   seam · P4 chain trim · 89-D2 enactment · `ds-032` · `ds-025` · boot-rent plan · attribution re-probe
   (**twelfth roll**).

---

## 10. The one line to carry forward

If a future session takes one thing from #125, it is this, and it is a question rather than a rule:

> **"What re-checks this?"** — asked of every claim a record makes, including the claims made by comments,
> by return values, and by the record's own prose. A claim with no answer to that question is not wrong
> yet. It is **scheduled** to be wrong.
