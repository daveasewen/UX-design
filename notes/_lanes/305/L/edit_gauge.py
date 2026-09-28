# #305 lane L - s305-D62 into knowledge/_gauge_tokens.py, by addition around each constant; the old text kept.
p = 'knowledge/_gauge_tokens.py'
s = open(p, encoding='utf-8').read()
orig = s
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:60], s.count(old))
    s = s.replace(old, new)

rep("BUDGET_HARD = 300_000        # PICKED by Dave #301 (2026-09-23) — an EXPERIMENT until the Mac\n",
    "# ⬛ `s305-D62` (Dave, Mon 2026-09-28 11:41 BST, chat #305, verbatim: *\"Lets make the window 320\n"
    "# including a wrap, 320 is a bright amber and 350 as the limit.\"*): BUDGET_HARD 300,000 → 350,000 and\n"
    "# BUDGET_WORKING 256,000 → 320,000, and the working window INCLUDES the wrap. It SUPERSEDES `s305-D28`'s\n"
    "# figures; `s305-D28` is not edited, and the comments at both constants below are kept as its record.\n"
    "BUDGET_HARD = 350_000        # `s305-D62` (was 300_000 — `s305-D28` / #301). Everything below this\n"
    "                             # line is the record of the 300,000 figure, kept as written.\n"
    "                             # PICKED by Dave #301 (2026-09-23) — an EXPERIMENT until the Mac\n")
rep("BUDGET_WORKING = 256_000     # PICKED by Dave #301 (2026-09-23, 20:21 BST), answering whether the\n",
    "BUDGET_WORKING = 320_000     # `s305-D62` (was 256_000 — `s305-D28` / #301): the working window,\n"
    "                             # INCLUDING the wrap; 320,000 is his bright-amber line. The lines\n"
    "                             # below are the record of the 256,000 figure, kept as written.\n"
    "                             # PICKED by Dave #301 (2026-09-23, 20:21 BST), answering whether the\n")
rep("STOP_LINE_TK = 236_000       # `s305-D28` (was 180_000 — `s260-D2` + `s271-D1`); the ONE advisory\n"
    "                             # stop line, Dave's to move\n",
    "# ⬛ `s305-D62` (Dave, 2026-09-28): the working window is 320,000 INCLUDING the wrap, 320,000 is the\n"
    "# bright-amber line, 350,000 the limit. The conductor's reading, stated in the ruling: the stop line,\n"
    "# where the wrap STARTS, moves 236,000 → 300,000 so that a wrap lands inside 320,000; the tolerance\n"
    "# line becomes the amber line, 276,000 → 320,000. `s305-D28` is not edited; its text above stands.\n"
    "# Both stay ADVISORY — the blocking tier is BUDGET_HARD, as before.\n"
    "STOP_LINE_TK = 300_000       # `s305-D62` (was 236_000 — `s305-D28`; before it 180_000 — `s260-D2`\n"
    "                             # + `s271-D1`); the ONE advisory stop line, Dave's to move\n")
rep("TOLERATED_TK = 276_000       # `s305-D28` (was 220_000 — `s272-D93`); advisory tolerance band,\n"
    "                             # Dave's to move\n",
    "TOLERATED_TK = 320_000       # `s305-D62` — the bright-amber line (was 276_000 — `s305-D28`; before\n"
    "                             # it 220_000 — `s272-D93`); advisory tolerance band, Dave's to move\n")
rep("    XX Does NOT re-pin the ruled budget triple. `(BUDGET_AMBER, BUDGET_WORKING, BUDGET_HARD)\n"
    "    == (160_000, 256_000, 300_000)` (#301, Dave's picked experiment: HARD 256_000 -> 300_000,\n"
    "    WORKING 200_000 -> 256_000) has exactly ONE authority",
    "    XX Does NOT re-pin the ruled budget triple. `(BUDGET_AMBER, BUDGET_WORKING, BUDGET_HARD)\n"
    "    == (160_000, 256_000, 300_000)` (#301, Dave's picked experiment: HARD 256_000 -> 300_000,\n"
    "    WORKING 200_000 -> 256_000; `s305-D62` then moved it to (160_000, 320_000, 350_000)) has exactly ONE authority")
rep('    print(f"  budget   amber {BUDGET_AMBER:,} · working {BUDGET_WORKING:,} (Dave #56) · "\n'
    '          f"(working PICKED Dave #301, was 200,000) · "\n'
    '          f"quality-max {BUDGET_HARD:,} (PICKED Dave #301 — experiment; was 256,000 SOURCED, "\n'
    '          f"93% MRCR v2)")\n',
    '    print(f"  budget   amber {BUDGET_AMBER:,} · working {BUDGET_WORKING:,} incl. the wrap (Dave #56) · "\n'
    '          f"(working `s305-D62`, was 256,000 `s305-D28`, 200,000 before #301) · "\n'
    '          f"quality-max {BUDGET_HARD:,} (`s305-D62`, was 300,000 PICKED #301; 256,000 SOURCED, "\n'
    '          f"93% MRCR v2)")\n')
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(orig), '->', len(s))
