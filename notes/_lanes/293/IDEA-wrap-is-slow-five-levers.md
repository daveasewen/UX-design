# Idea, not a lane — the wrap is slow, and five levers

provenance: 293, Jev side-quest worker seat (Fable 5.1) · 2026-09-21 · **NOT ENACTED, NOT SCHEDULED**

⛔ Touches the capture ritual, so post-Friday-25th under Dave's standing word: *"any analysis is fine
but any changes with impact will need to be made after the presentations and demos."*

## His words, verbatim

> another thing, the wrap takes a long time to run... is this something we could work on in the
> future? any ideas

## Where the time goes — MEASURED from the record

| what | figure | source |
|---|---|---|
| runbook the wrap sub must read | **896 lines**, 16 steps (1, 1b, 2, 2c–2g, 3, 4, 4b–4d, 5, 5b) | `knowledge/_RUNBOOK-capture-ritual.md` |
| files written per wrap | **14** (handoff, dossier, subreport, memory hook, LS + LS-archive, GM + GM-archive, gauge log, carries, chain, index, state, titles receipt) | #293 W § FILES WRITTEN |
| wrap sub cost at #292 | **115,674** tokens, plus a second commit seat **85,536** | HANDOFF-143 § subs |
| #293 wrap subreport alone | 20,871 chars | `notes/_subreports/2026-09-21-293-W-wrap.md` |
| banner drafts against the 1,200 cap at #292 | **six** — five trims, the sixth merged two bullets; closed with 2 tokens headroom | HANDOFF-143 § THE BANNER CAP |
| inherited gate fails re-explained | **seven**, for the **eighteenth consecutive** "declared NOT-A-WRAP" wrap | HANDOFF-143 § THE GATES |
| index rebuilt | after **every** GM/LS edge, not once | #293 W § WHAT WAS DONE |

## Five levers

1. **One story, not three.** Handoff, decision-history dossier and wrap subreport each narrate the
   session in a different shape. Write ONE structured source (the sub's findings as sections with
   tags) and GENERATE the other two views from it, the way `_CHAIN.md` is generated from GM + LS.
   Halves the prose; removes the drift between them.
2. **Count before drafting.** The ★ LATEST banner is drafted, measured against `s241-D2`'s 1,200 /
   10 lines, trimmed, repeated. Have `_gen_chain.py` (or a banner generator) take candidate bullets
   and either report the budget per bullet before drafting, or choose which survive. *(A Jev Choice
   over bullets — "which of these must a cold seat read first" — is the typed version; analysis
   only, see J5.)*
3. **Rule the seven inherited fails closed — biggest payoff, no code.** Boot-drift CEILING BREACH
   and six boot double-counts (#243 ×5, #264, #272, #273, #274, #287) are append-only testimony no
   wrap may repair. Every wrap re-reads, re-verifies and re-documents them, then takes the #243
   path. **One ruling from Dave that they are CLOSED as history** turns the gate green and deletes
   that paragraph from every future wrap. (Interacts with the boot bands note — if the next cold
   boot lands under 70k, the breach has ended on its own.)
4. **Wrap as you go.** The ⏱ delta, the carries and the DAVE-RULINGS file are reconstructed from
   the whole transcript at the end. The seam check already fires ~5× a session; each firing is a
   moment to append the delta-so-far and his entries verbatim to a draft. The wrap then EDITS a
   draft instead of reading a transcript. Also fixes the "DAVE-RULINGS appended after the commit"
   wrong-order class (four consecutive sessions, HANDOFF-143).
5. **Mechanics in parallel with prose.** Steps 2c–2g, 4–4d and the index/titles/gate/commit are
   scripted and need no judgment. Run them as ONE script (`_wrap_mechanics.py`) while the sub writes
   the prose; serialise only at the commit. Rebuild the index once, at the end, not per edge.

## Order proposed after the 25th, only if ruled

3 (a ruling, no build) → 5 (script exists in pieces) → 4 → 2 → 1.

## Ruling-shaped questions — QUESTIONS PUT, nothing inscribed

1. Close the seven inherited gate fails as history? (lever 3)
2. Is one generated view of the session acceptable in place of three hand-written ones, given
   `s218-D7` filed-report rules? (lever 1)
3. May the seam check write to a wrap draft — i.e. may an instrument append to a session file? (lever 4)
