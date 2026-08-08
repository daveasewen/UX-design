# 2026-08-08 s134 laneH — tint-only shell enactment (s134-D4)

Enacted s134-D4 (Dave #134, "nailed to the mast") in `knowledge/snippets/Alert.reference.html`:
`.alert` shell drops `border:1px solid var(--accent);` and the `border-width` transition/collapse
leg on `.alert.removing` — shell is now tint-background-only. Marks unchanged, #1A1A1A, both
themes (s122-D2/s134-D2). Both removals retired BY DECLARATION — CSS comments cite s134-D4 and
quote the old construction, no silent deletion. `--accent` binding on `.alert.err/.warn/.ok/.info`
left intact (still feeds the icon/glyph colour channel, only the shell edge is gone).

Proof: grepped the file for border/box-shadow/outline on `.alert*` — only two accessibility
`:focus-visible` outlines remain (link and dismiss control), no shell edge. Ran
`_validate_state_contrast.py --selftest`: 18/18 non-browser arms ok, rc=2 named refusal
(playwright not installed) — checked directly, matches expectation.

Wrote `reviews/_alert-{light,dark}-specimen-2026-08-08-s134-v3.html` (byte-copies of the enacted
snippet, dark differs only in `body data-theme`) and
`reviews/ALERT-ERROR-MARK-REVIEW-2026-08-08-s134-v3.html` (iframes at v3, copy updated to describe
the tint-only shell). v2 specimens/review untouched (verified by diff/md5 before writing v3).

DO-NOT-RULE observed: no token edits, no new colours, no commits, no chain/GM/state/rulings edits,
no `rm` used.
