# #297 lane E — slide 11's tackled causes turn red, governance gets its reference mark; the standards line says friction

provenance: 297 · 2026-09-22 (session date; work done Wed 2026-09-23 ~09:25–10:05 BST) · lane E (Opus 5.5, remote-device seat)
status: observed
tokens: UNMEASURED — this seat has no `message.usage` read

Dave's four messages (09:07, 09:11, 09:15, 09:18 BST) are filed verbatim, by addition, at `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md`, with the conductor's reading beneath them.

## VERDICT

**DONE.** Both changes are in the plain deck. The deck was rebuilt from its source with `build_c.py`; it was never hand-edited, and `build_e.py` was not run. `build_c.py` itself is unchanged.
- **11, second state:** the tackled causes' text is now the deck's red. Lane C's upright red rules and dashed governance rule are gone. Governance stays ink and carries a red superscript dagger (†). The proposal note opens with the same dagger, hung in its left margin.
- **06, cause 04:** "Standards exist, but in too many places; asking someone is quicker than looking it up."
- **Pixel diff at 1920×1080 against HEAD 999cba4a's render:** content changed on **06 and 11's second state only**. 11's first state is SAME.
- **Rail collisions:** 0 at 1920×1080 and 0 at 1440×900, on 16 slides plus 11's second state.
- **Overflow:** none, except 11's second-state note, which sits under the Speed card by design (lanes C and D declared it). The note's dagger is part of that same flag.
- **Keys:** 10 → 11 → 11 second state → 12 and back behave exactly as in lane C's log.
- **For Dave:** `notes/_lanes/297/E/for-dave.html`. It is self-contained (302 KB) and shows 06, then 11's first state, then 11's second state. On his machine it is at `computer:///Users/daviewen/Documents/Claude/Projects/UX-design/notes/_lanes/297/E/for-dave.html`.

## 1 · 11, the second state

**What it looks like now.**
- **Red text.** On the next press these five causes turn red: "2 stage process (Figma + Code library)", "Small component library", "Lack of standards knowledge", "Highly variable design skills" and "AI generation quality (slop)". Their dividers stay grey. The colour fades in over 0.35s, and there is no fade under reduced motion.
- **Two stay ink.** "Lack of user data and research" is not tackled, and "Manual, linear governance process" is not solved.
- **The reference mark is a dagger (†), in the deck's red.** I used a dagger rather than an asterisk because an asterisk reads as a keyboard character. The dagger is the typesetter's reference mark.
  - **After "governance process"** the dagger is a superscript: 0.72 of the text size, raised about half its height, with a hair of space (0.16em) before it. It sits at line-height 0, so it adds no height to the line.
  - **In the note** the same dagger, at the same size and raise, hangs in the note's left margin, 4px before "**Proposal:**". So "Proposal:" keeps the card's text line, as it did under lane C.
  - The note reads: "† **Proposal:** sign off the system, / not the outputs — or at least a fast-track."
- **Everything else on 11 is as lane C left it.** That covers the headline, the three cards, the grey dividers and the note's place, size and fade.

**One layout, two states.** Both daggers are in the page in state 1 too, hidden. So nothing moves between the states, and only colour and opacity change. The pixel diff confirms state 1 is unchanged.

**The build behaviour is unchanged.** `data-steps="2"`, the `window.deckStep` hook, the keys, the wheel and "back from 12 shows state 2" are all lane C's script, untouched.

**Screen readers.** Both daggers are `aria-hidden`. The note is still `visibility:hidden` until state 2, and it follows the governance item in reading order, so the pairing needs no spoken mark.

**Markup.**
- Governance's item was `class="tk tk-prop"`. It is now `class="gov"`, because it is no longer highlighted, and it ends with `<sup class="ref" aria-hidden="true">&dagger;</sup>`.
- The note starts with the same `<sup>`.
- The CSS is lane C's state-2 block in the `297-C` style, rewritten in place and signed "#297 lane E". The `li.tk::before` rules and the dashed gradients are gone.

## 2 · 06, cause 04

**As set:**
> Standards exist, but in too many places; asking someone is quicker than looking it up.

- It is 87 characters; the line it replaces was 98. A non-breaking space keeps "it up." together.
- **It runs to 4 lines at 1920 and at 1440**, the same as the line it replaces. Its siblings run to 2–3.
- **Not tightened.** It breaks cleanly at both sizes, with no word left on its own: "Standards exist, but in too / many places; asking / someone is quicker than / looking it up." Dropping "someone" would save a word, but the sentence then loses who is being asked, so I left the brief's line as written.
- Nothing else on 06 changed.

**The alternative, for Dave:**
> The standards are written, but scattered — and pressed for time, designers ask rather than read.

Both lines say friction, not laziness: the standards exist, and asking is simply quicker. Neither calls designers lazy.

## 3 · Checks

- **Renders:** all 16 slides plus 11's second state, at 1920×1080 and 1440×900, with lane C's harness (freezes as lane A's). They are in `notes/_lanes/297/E/_work/after-1920/` and `after-1440/`; the baseline is `before-1920/`, rendered from the committed deck at HEAD 999cba4a (byte-identical to `git show HEAD:`).
- **Rail: 0 hits at both sizes.** Smallest clearance is 123.5px at 1920 and 37px at 1440, the same as lane D.
- **Overflow: 0 at both sizes, except 11's second-state note** (by design, as before). The flag now lists four line boxes rather than three, because the note's dagger is one of them. 0 page errors and 0 console errors.
- **Pixel diff at 1920 vs HEAD**, with the rail band (x < 200) and the content split:

| slide | rail band | content |
|---|---|---|
| 01–05, 08–11 (state 1), 12–16 | SAME | SAME |
| **06** | SAME | **DIFF** (1086,655)–(1271,742): cause 04's description only |
| 07 | 10 pixels differ by 1 level, (34,274)–(42,277) | SAME |
| **11 state 2** | SAME | **DIFF** (413,620)–(1423,796): the red text, the dagger and the note |

  - **07's rail flicker is the renderer, not the change.** Rendered twice, the pre-change deck differs from itself in the same 8×3 box. HEAD rendered twice (lane D's and mine) is SAME everywhere.
- **Keys** (`notes/_lanes/297/E/_work/navtest_e.py`, lane C's test; it now reads the text colours and the dagger, not the rules):
```
start deckGo(10) -> slide 10 · 11 state 1: tackled ink, gov ink, data ink, dagger hidden, note 0
ArrowDown -> 11 (11 / 16) state 1   tackled rgb(0,0,0)   dagger hidden  note 0
ArrowDown -> 11 (11 / 16) state 2   tackled rgb(218,26,0) gov rgb(0,0,0) data rgb(0,0,0) dagger visible note 1
ArrowDown -> 12 (12 / 16)
ArrowUp   -> 11 state 2 · ArrowUp -> 11 state 1 · ArrowUp -> 10
```
  - Space / Space / PageDown / PageUp ×3 give the same result.
  - Controls: 03 ↓↓ gives 04 then 05, and 13 ↑ gives 12, unchanged.
- **I looked at** 06 and 11's second state at 1920 in full, at 3× around the Speed card and the note, and at 2× at 1440 (`_work/zoom/`). The dagger sits clear of "process" and is not crammed. The two daggers match in size and colour, and "Proposal:" keeps the card's text line.
- **for-dave.html:** it renders at 1440 and at 390 wide, with no horizontal scroll. The arrow keys step 1 → 2 → 3, and there are 0 page errors.

## Deviations

1. **The note's dagger hangs in the margin** rather than pushing "Proposal:" right. It is still at the start of the note, and the note's text keeps the card's line.
2. **The daggers are `aria-hidden`** (section 1).
3. **06's line runs to 4 lines**, as the old one did, and was not tightened (section 2).
4. **Lane C's `tk-prop` class is renamed `gov`** on the governance item, since that item is no longer highlighted.
5. **Dave's 09:07 question** (review pages from his repo, not the cloud) is the conductor's to answer and apply. This report gives the `computer://` path for the review page above.
6. **W-297c and W-297d are left open.** Closing them is the conductor's call.

## Files

- **Changed:**
  - `notes/_lanes/296/C/v14-plain-before-c.html` (the source)
  - `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt, 523,097 bytes)
  - `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (appended)
- **New:** `notes/_lanes/297/E/for-dave.html` · this report · store row W-297e
- **Working, not committed:** `notes/_lanes/297/E/_work/`
  - `apply_e.py`: re-runnable from `source.pre-297E.html`
  - `shoot_e.py`, `zoom_e.py`, `pdiff_e.py`, `navtest_e.py`, `make_for_dave_e.py`
  - the before and after renders, `zoom/`, `r07/` (the jitter proof)
