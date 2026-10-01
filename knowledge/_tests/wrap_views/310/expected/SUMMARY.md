# #310 — summary for Dave

## Decisions
- 8 rulings, 841 → 849: the thin arrow from the icon assets; Net FX exposure is the first "up is bad" metric, because colour means good or bad news, not direction; dark mode mirrors light by default (black tiles on the dark grey ground) with the reverse as an option; Supercharge the same with its own darkest; Supercharge's pressed tile at #25211C for now; the option named "dark tiles, black or grey"; the white ink softens to #E1E1E1 and the tab strip takes its container's colour.
- The last two are ruled but not built. Your note said "i need to see this", so they get built and shown to you before they stand.

## Outputs
- Built: black tiles by default and grey tiles as an option, recorded in the theme register (51 of 137 components change in dark), and the interim pressed tile.
- Three review pages reached you through the review artifact (v18 to v20). The repo's halation tool showed the ink, not the tile, is what cuts the glare.
- The wrap is committed and pushed (`b40bddc2`, plus `4ece47a5` for the wrap seat's files). The full pre-push check ran on the wrap first and came back clean. CI is green on all three jobs.
- Next chat: `Apollo - #311: the soft white and the tab strip, built and shown`.

## Problems
- One CI red in the session. The conductor pushed without running its own pre-push check, and lane B fixed it the same hour.
- The session ran to 372,194, past the hard line (350,000). It crossed that line at 17:17, and the conductor didn't notice until 17:35.
- Still yours: Supercharge's dark page colour, the Figma values for the pressed tile, the pack re-cut at the end of the week, and the container types.
