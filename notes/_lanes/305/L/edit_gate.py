# #305 lane L - s305-D62 into knowledge/_capture_gate.py: the two pins, the fixtures that price against
# the live working line, and the declared-breach vocabulary. Old comments kept; additions marked s305-D62.
p = 'knowledge/_capture_gate.py'
s = open(p, encoding='utf-8').read()
orig = s
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:70], s.count(old))
    s = s.replace(old, new)

# 1. the declared-breach vocabulary: blocks written against the new working line still read as declared
rep('_WALL = r"(?:200,000|200000|256,000|256000|working\\s+(?:ceiling|wall|line))"\n',
    '# `s305-D62` (2026-09-28): 320,000 added — BUDGET_WORKING moved 256,000 → 320,000 (Dave, *"Lets make\n'
    '# the window 320 including a wrap"*). 200,000 and 256,000 are KEPT so older blocks still read as declared.\n'
    '_WALL = r"(?:200,000|200000|256,000|256000|320,000|320000|working\\s+(?:ceiling|wall|line))"\n')

# 2. the fixtures: every `of 256,000` priced against the live working line -> `of 320,000`
n_of = s.count("of 256,000 — ") + s.count('"of 256,000"')
rep("# #301: every `of 200,000` below → `of 256,000` — the stamp must price against the live\n",
    "# `s305-D62` (2026-09-28): every `of 256,000` below → `of 320,000`, same reason — BUDGET_WORKING\n"
    "# moved 256,000 → 320,000; the totals of the three over-the-line fixtures were lifted to match.\n"
    "# #301: every `of 200,000` below → `of 256,000` — the stamp must price against the live\n")
s = s.replace("of 256,000 — ", "of 320,000 — ").replace('_ABS_OK.replace("of 256,000", "of 500,000")',
                                                          '_ABS_OK.replace("of 320,000", "of 500,000")')
# over-the-working-line fixtures: 266,897 sits under 320,000 now -> lift to 336,897 (over 320,000, under 350,000)
rep('     "pre-flight #56: boot 26,897 measured + job 200,000 est + wrap 40,000 est "\n'
    '     "= 266,897 of 320,000 — RED\\n", True),\n',
    '     # `s305-D62`: lifted 266,897 → 336,897 (job 200,000 → 270,000): over the new 320,000 working\n'
    '     # line, under the new 350,000 hard line, so it still tests the RED overrun.\n'
    '     "pre-flight #56: boot 26,897 measured + job 270,000 est + wrap 40,000 est "\n'
    '     "= 336,897 of 320,000 — RED\\n", True),\n')
rep('     "pre-flight #56: boot 26,897 measured + job 200,000 est + wrap 40,000 est "\n'
    '     "= 266,897 of 320,000 — RED · RESERVE SPEND — forked to Dave\\n", False),\n',
    '     "pre-flight #56: boot 26,897 measured + job 270,000 est + wrap 40,000 est "\n'
    '     "= 336,897 of 320,000 — RED · RESERVE SPEND — forked to Dave\\n", False),\n')
rep('     "pre-flight #56: boot 26,897 measured + job 250,000 est + wrap 40,000 est "\n'
    '     "= 316,897 of 320,000 — RED · RESERVE SPEND — forked to Dave\\n", True),\n',
    '     # `s305-D62`: lifted 316,897 → 366,897 (job 250,000 → 300,000) so it stays PAST the hard line\n'
    '     # after the 300,000 → 350,000 move.\n'
    '     "pre-flight #56: boot 26,897 measured + job 300,000 est + wrap 40,000 est "\n'
    '     "= 366,897 of 320,000 — RED · RESERVE SPEND — forked to Dave\\n", True),\n')

# 3. the triple pin
rep("    if (gauge.BUDGET_AMBER, gauge.BUDGET_WORKING, gauge.BUDGET_HARD) != (160_000, 256_000, 300_000):\n"
    "        failures.append(\n"
    "            f\"budget = {(gauge.BUDGET_AMBER, gauge.BUDGET_WORKING, gauge.BUDGET_HARD)}, ruled \"\n"
    "            f\"(160,000 at #56 · 256,000 / 300,000 at #301). WORKING is PICKED by Dave #301 \"\n",
    "    # ⬛ `s305-D62` (Dave, 2026-09-28, chat #305, verbatim: *\"Lets make the window 320 including a\n"
    "    # wrap, 320 is a bright amber and 350 as the limit.\"*): WORKING 256_000 → 320_000 (and it\n"
    "    # includes the wrap), HARD 300_000 → 350_000. AMBER did NOT move. Re-pinned, not weakened.\n"
    "    if (gauge.BUDGET_AMBER, gauge.BUDGET_WORKING, gauge.BUDGET_HARD) != (160_000, 320_000, 350_000):\n"
    "        failures.append(\n"
    "            f\"budget = {(gauge.BUDGET_AMBER, gauge.BUDGET_WORKING, gauge.BUDGET_HARD)}, ruled \"\n"
    "            f\"(160,000 at #56 · 320,000 / 350,000 by `s305-D62`; 256,000 / 300,000 at #301 and \"\n"
    "            f\"`s305-D28`). WORKING is PICKED by Dave #301 \"\n")
# 4. the stop/tolerance pin
rep("    if (gauge.STOP_LINE_TK, gauge.TOLERATED_TK) != (236_000, 276_000):\n"
    "        failures.append(\n"
    "            f\"stop/tolerance = {(gauge.STOP_LINE_TK, gauge.TOLERATED_TK)}, ruled (236,000, \"\n"
    "            f\"276,000) by `s305-D28` (was 180,000 `s271-D1` / 220,000 `s272-D93`). Both are \"\n"
    "            f\"ADVISORY lines under working 256,000 / hard 300,000 and both are Dave's to move — \"\n",
    "    # ⬛ `s305-D62` (2026-09-28) moves both again: stop 236,000 → 300,000 (the wrap starts there and\n"
    "    # lands inside 320,000), tolerance 276,000 → 320,000 (his bright-amber line). Re-pinned, not weakened.\n"
    "    if (gauge.STOP_LINE_TK, gauge.TOLERATED_TK) != (300_000, 320_000):\n"
    "        failures.append(\n"
    "            f\"stop/tolerance = {(gauge.STOP_LINE_TK, gauge.TOLERATED_TK)}, ruled (300,000, \"\n"
    "            f\"320,000) by `s305-D62` (was 236,000 / 276,000 `s305-D28`; 180,000 `s271-D1` / 220,000 \"\n"
    "            f\"`s272-D93` before). Both are \"\n"
    "            f\"ADVISORY lines under working 320,000 / hard 350,000 and both are Dave's to move — \"\n")
# 5. the fail messages that name the line's authority
rep('f"({gauge.BUDGET_WORKING:,}, Dave #56, re-dialled #301) and UNMARKED.',
    'f"({gauge.BUDGET_WORKING:,}, Dave #56, re-dialled #301 and `s305-D62`) and UNMARKED.')
rep('f"budget is {gauge.BUDGET_WORKING:,} (Dave #56, re-dialled #301). Re-dialling it is his "',
    'f"budget is {gauge.BUDGET_WORKING:,} (Dave #56, re-dialled #301 and `s305-D62`). Re-dialling it is his "')
rep('            f"That line is PICKED by Dave #301 as an experiment until the Mac seat fix, ABOVE "\n',
    '            f"That line is Dave\'s (`s305-D62`, 2026-09-28; PICKED at #301 as an experiment until the "\n'
    '            f"Mac seat fix), ABOVE "\n')
open(p, 'w', encoding='utf-8').write(s)
print('ok fixtures-of-256 before:', n_of, '| remaining "of 256,000 — ":', s.count("of 256,000 — "), '|', len(orig), '->', len(s))
