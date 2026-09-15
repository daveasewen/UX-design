# #275 — the principles and the second seat

provenance: 275 · 2026-09-15
status: observed

**Spine:** `_LIVE-STATE.md` § ⏱ LATEST DELTA — 2026-09-15 (#275) · `GOOD-MORNING.md` § ★ LATEST (#275)
**Ledger:** `knowledge/_rulings.json` §§ `s275-D1`…`s275-D6` · `notes/_RULINGS.html`
**His words, in order, verbatim:** `notes/_lanes/275/DAVE-RULINGS-2026-09-15.md`
**Brief:** `_HANDOFF-126-the-principles-and-the-second-seat.md` (written by the conductor BEFORE this ritual)
**Wrap report:** `notes/_subreports/2026-09-15-275-W-wrap.md`

---

## The arc in one line

Step 3 of `s269-D1` ran the same way steps 1 and 2 ran — propose read-only, verify read-only, put six decisions to Dave, land only on his word — and while it ran, a second live session wrote into this session's lane.

---

## 1. The method is now the finding, because it did not vary

`s269-D1` names five steps for filling the knowledge graph's thirteen empty families. #273 did roles. #274 did the 470 guideline rules. #275 did step 3: the **145 UX principles** and the **30 polarities**.

The shape was RK's, unaltered:

1. **One Opus lane builds a generator that can land and does not.** `77b043f` (lane RP, 285,000 real) wrote `knowledge/gen_kg_principles.py` with `--dry-run`, `--land --ratified`, a 15-bite selftest and an 18-mutant harness. Dry-run: **175 nodes / 111 edges / 27 declared nulls**. It landed nothing.
2. **A review page carries at most six decisions, recommendation first.** `REVIEW-principles-into-graph-2026-09-15-v1.html`, RP-1…RP-6, with the recommended option (a) first on each.
3. **A second read-only lane drives every claim before Dave sees any of it.** `2cbfbad` (lane RV, 144,000 real).
4. **Nothing lands until his export.**

**Why this is worth writing down rather than assuming:** the method caught two things in one day that no gate would have.

- **Three selftest bites were DEAD.** They ran, they passed, and they asserted nothing. Only the mutation harness — which breaks the generator deliberately and demands that a bite notice — exposed them. A selftest that passes against a broken generator is not a test; it is a green light with no bulb behind it. `s182-D1` says a mechanical claim carries a probeable token, and this is the same lesson one level down: a probe carries a proof that it can fail.
- **The verifier corrected the conductor, not the lane.** Lane RV re-derived twelve of the conductor's own brief claims and found two of his figures wrong: *"31 families"* measured **32**, and *"60 live type strings"* measured **62**. Both were corrected **by addition** in `REPORT.md` rather than by editing the original claim. Neither changed a ruling. What they changed is what the record says, and the verifier lane exists precisely so that a conductor's arithmetic is not the last word on itself.

---

## 2. Six rulings out of an export and one word

His export, stamped **2026-09-15T16:27:07.539Z**, came back **six for six, all (a), no notes, no nulls**. The conductor read the whole set back in chat — there was nothing in it that was a sequel under RK-3/RK-4/RK-6, because no answer carried a sentence — and his *"go"* inscribed the six at `ffcb029`:

| id | what it settles |
|---|---|
| `s275-D1` | a `ux:<id>` node carries **twelve fields** |
| `s275-D2` | **all six edge types** ratified — `tensionWith` · `hasParty` · `touches` · `resolvedBy` · `challengedBy` · `explainedBy`; **this is the id `--land --ratified` takes** |
| `s275-D3` | a **`polarity:<id>` is a NODE**, not an attribute |
| `s275-D4` | the **20 standards rows land plain**; their joins are authored later |
| `s275-D5` | the metas cite the **six A-grade laws** in ONE authored lane, merged with `P-274-3` |
| `s275-D6` | the store and its **explorer reader land in the SAME commit** |

The only other things he typed all day were *"gm"*, *"can you surface the page please"*, and a first *"go"* that started the lane.

⚠ **The quote gate refused two of those four sentences** (`_quote_gate.py` returned 2 verbatim / 2 not-in-the-record). The refusal is about the **index**, which covers neither `notes/_lanes/` nor the `says` field — not about the words. Verified directly against `notes/_lanes/275/DAVE-RULINGS-2026-09-15.md`: **4 of 4 exact**. This is the third consecutive wrap to hit the same index gap and the third to say so.

---

## 3. The inscription went in twice wrong before it went in right

Both failures are worth keeping, because a green gate stood over both.

- **Attempt one re-dumped `_rulings.json`** — a 3,672-line diff where six spans were wanted. That is the **#179 class**, and it is written down in three places. It was reverted.
- **Attempt two committed with `_rulings.json` UNCHANGED**, because the splice asserted on a trailing newline the file did not have, failed quietly inside a command chain, and the commit went out anyway. Amended within the minute.

`_validate_kg.py` reported **OK** across both. The store was structurally valid when it had been rewritten wholesale, and structurally valid when it had not been written at all. What caught each was a hand proof of the span — not a gate [[no-gate-parses-the-artefact]].

---

## 4. `s269-D1` step 3 is done, and the base graph did not move

`eb47a58` (lane RL2, 183,000 real) landed `knowledge/_ux_principle_nodes.json`:

- **175 nodes / 111 edges / 15 declared null edges.** The dry-run's "27" reconciles as **15 nulls + 12 edgeless polarities** — written down rather than smoothed over, because two different numbers for the same thing is how a record starts lying.
- **`s275-D1` checked field by field: 1,595 comparisons, 0 mismatches.**
- Explorer **v1.11 → v1.12**, a "UX principles" chip (`uxprinciples`) **OFF by default**, plus `ux` / `polarity` type chips. The chip's palette is plum `#8A1A5C` / `#E68ABF` — deliberately **not** a third red, because the two-red law (`s151-D1`) owns that vocabulary.
- **The base graph is pixel-stable: 0 of 951 base nodes moved.** A new family that re-lays-out the old graph is a new graph; this one is an addition.
- Gates: `_validate_kg.py` OK · selftest PASS · `_validate_compose.py` PASS · `_validate_roles_resolve.py` **FAIL(6) inherited** (#261's `data-grid` `with`-slugs). Chromium: 0 console errors, 5 screenshots reviewed by the conductor before anything was presented — the `#268` art-director rule, held.

---

## 5. The second seat — a new hazard, healed by addition, not ruled

The #274 session was still open while #275 ran. At 17:25 BST it committed `5dd19ee` **into `notes/_lanes/275/`**, replacing lane RP's page-builder input `principles-kg-decisions-2026-09-15.json` with a chat-derived pseudo-export — **71 lines lighter**. Shortly after, #275's own `Write` of `DAVE-RULINGS-2026-09-15.md` overwrote the single line #274 had added.

**Both were healed by addition at `49e2a44`**, and the shape of the heal is the part to keep:

- the builder input was restored with **`git show 2cbfbad:<path>`** — the only working restore on this mount, and the reason `git stash` sequences are banned;
- the #274 record was **kept beside it** under its own name, `DAVE-EXPORT-from-274-chat-2026-09-15.json`, rather than discarded as the loser;
- the overwritten line was **appended back**.

Nothing was re-dumped, nothing re-dated, nothing deleted. And the corroboration in the #274 chat — Dave's *"so go with the recommendations you think?"* — is **recorded as corroboration and is not the source of the rulings**: `s275-D1`…`s275-D6` cite his own 16:27Z export from the #275 seat.

⬛ **What is open, and it is his alone:** is **one seat at a time** the rule, or may a second seat write **provided it writes only under `notes/_lanes/<its own N>/`**? Put to Dave at the #276 opener. Nothing in this session rules it, and the heal is not a precedent for a rule.

---

## 6. What this wrap did not do, named rather than smoothed

- **Memory (step 3) was read-only at this seat by the brief** — a declared seat limit, not a skip. The hook body and its one `MEMORY.md` index line were written in the `s271-D4` form to `notes/_lanes/275/WRAP-MEMORY-HOOK.md` for the conductor to place.
- **Five blocking gate refusals are carried in the `#243` form**, all inherited: the boot ceiling breach and the boot double-counts of #243, #264, #272 and #273. `notes/_GAUGE-LOG.md` is append-only and every one of those blocks is another session's testimony.
- **The showroom is 108 pages stale for the third consecutive wrap** — a `:is(…)` → `:where(…)` specificity diff, one line per generated page, predating all three sessions.
- **The resolver reads FAIL(6)**, all six #261's, measured at this seat rather than quoted.
- **`/sessions` is 97% full.** 4c cleaned what this user owns; dead-session orphans cannot be removed from inside.

---

## Resolved state, and what is still open

**Resolved:** `s269-D1` steps 1, 2 and 3 — roles, rules, principles + polarities — are in the graph. **Step 4 is icons (666) then logos**, in the same shape; step 5 is the four edge types `setIn` / `behaviourFrom` / `capturedFrom` / `acceptsCapability`.

**Open, and his:** the two-seat question · the `--land --ratified` id-only unlock · the explorer's missing `statement` span · RP-4's four name-only WCAG joins · which components go first for `s275-D5` · `P-274-1`/`P-274-2`/`P-274-3` · the push (29 local before this wrap, 30 after).

**Both-way links:** spine `_LIVE-STATE.md` § ⏱ LATEST DELTA (#275) · ledger `knowledge/_rulings.json` §§ `s275-D1`…`s275-D6` · carry set `_CARRIES.md` § `## residual → #276`.
