# Lane A — s130-D4/D5/D6 + tabs remainder (2026-08-08, session #134 sub)

## RETRIEVE (done)

Fetched `ledger:130-the-pointer-repairs-landed-and-the-128-wrong-subject-def` (`notes/_MEMENTO-DECISIONS.md:5399`)
in full — the complete ★★ #130 ledger entry, including the exact `s130-D4`/`D5`/`D6` bodies and the
"also ruled, also unenacted" tabs clause. Cross-checked `knowledge/_rulings.json` (entries `s130-D4`
line 1475, `s130-D5` line 1493, `s130-D6` line 1511) and `_LIVE-STATE.md:365-386, 465-468` (§ OPEN, item
"NEW #130 — THE ENACTMENT LANE").

**Confirmed current status (repo state, not banner):** as of #133 (latest wrap on disk), `s130-D4`/`D5`/`D6`
and tabs are **still RULED-NOT-ENACTED**. Only the legacy-reversed-text half of the surrounding item was
closed, by `s131-D1` (#131) — a different surface (legacy RAG fills), not this item. `_LIVE-STATE.md:383`
states explicitly: *"The REST of this item is UNTOUCHED: `s130-D4`/`D5`/`D6` and tabs are still
RULED-NOT-ENACTED."* No grep hit for these ids marks them enacted anywhere in `_LIVE-STATE.md`,
`_MEMENTO-DECISIONS.md`, or `_rulings.json` beyond the #130 record itself.

## ANALYSE — why this is NOT a mechanical remainder

I looked for the concrete edit sites before touching anything:

- `s130-D4` (banner ghost/tint states, pressed 14% / hover 8%, error red `#F6604C`→`#B92F1E`): the #130
  dossier's own FINDING 3 states **the quaternary/ghost banner has no pressed token at all — hover ==
  pressed, "the press is literally inexpressible until `s130-D4` is enacted."** Enacting this ruling
  therefore means **minting a new token slot**, not editing an existing value — that's spine surgery
  (new key in `semantic-colour.json` + theme cascade regen + component-spec update), not a mechanical
  form change.
- The error-red token itself is genuinely ambiguous on inspection: `semantic-colour.json:463-573` shows
  the MONO error family has been flipped between `#F6604C` and `#B92F1E` across `s122-D2`, `R-D14`,
  `R-D20`, `s123-D3` — several different roles (background/glyph/tint) at different states, with
  overlapping notes. Picking the wrong one of ~4 occurrences and writing `#B92F1E` over it risks the
  exact false-inscription class this project is built to catch. This needs the live specimen
  (`reviews/CONTRAST-CONTROLLER-2026-08-08-v3.html`) walked side-by-side with the token file, not a grep-and-edit.
- `s130-D6` (chip pressed, per-theme greys): `knowledge/tokens/layout.json` is the only token file
  matching "chip" — no existing chip-pressed slot per theme was found to overwrite; this also reads as a
  mint, and the four theme values (mono/console/legacy/SC) need to land in the *pressed* slot
  specifically, verified against each theme's own ramp, not assumed by name.
- **Tabs:** `knowledge/components/tabs.meta.json` has **no `badge` reference at all** — so there is
  nothing on disk to "keep as-is." Confirming the ruling is already satisfied, or landing it, both
  require locating the actual badge markup in the snippet corpus (not the meta) and reading its live
  computed contrast — a verification step, not a known-value copy.
- Dark mode is explicitly **carved out by #130 itself**: *"an enactor must not quietly add the third"*
  — two of three states already invert via cascade and the banner wash must stay mode-invariant. This
  guard stands untouched here, per the DO-NOT-RULE list.

Given the brief's constraint — enact ONLY mechanical, already-ruled work, never invent close conditions,
never touch gates/thresholds without a full mutation-test+render-proof pipeline — none of `s130-D4`,
`s130-D5`, `s130-D6`, or tabs clears that bar in this pass. Each requires either minting a new token
(a spine decision beyond "already-specified value copy") or a live contrast re-measurement to place a
value correctly among several similarly-named existing tokens.

## RESULT

**No token file was edited. No value moved.** This matches the honest status already recorded at
`_LIVE-STATE.md:368`: *"No value moved in any token file. Owner: Dave — the enactment licence is his word."*
I did not overrule that annotation.

## What remains, and why (UNPROVEN, not done)

1. `s130-D4` — mint the quaternary/ghost banner pressed-state token, resolve which of the ~4 `#F6604C`/
   `#B92F1E` mono-error occurrences the ruling addresses, apply pressed 14%/hover 8%, regen, mutation-test,
   render-proof.
2. `s130-D5` — locate check/selection label token(s), rebind to `--ink`, move error signal to border+message,
   verify 17.40:1 reproduces on committed bytes.
3. `s130-D6` — mint chip-pressed token per theme (mono `#484848`/`#313131`, console neutral-6/5, legacy
   `#767676`, SC unchanged), scoped so shared form/background/pressed are untouched.
4. Tabs — locate badge markup in the snippet corpus, confirm ink-dark/legacy-red state against the ruling,
   land only if a gap is found.

All four need Dave's go/confirm on the specific edit site given the token-history ambiguity found above,
consistent with `_LIVE-STATE.md`'s own "Owner: Dave" note on this item.

## Files touched
- `notes/_briefs/2026-08-08-134-laneA-s130-remainder.md` (this file, new)

No other files were modified.
