# #305 lane L round two - s305-D64: BOOT_CEILING_TK 130,000 -> 135,000, and arm E's pin with it. Old text kept.
p = 'knowledge/_gauge_tokens.py'
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)
rep("BOOT_CEILING_TK = 130_000      # `s305-D29`, until the Mac seat, then measured there and shrunk.\n"
    "                               # (was 72_768 — `s295-D3`, #295 turn 1; before it 70_000 — `s241-D1`.)\n",
    "# ⬛ `s305-D64` (Dave, Mon 2026-09-28 12:21 BST, chat #305 — \"yes both\", to \"yes to both, the boot\n"
    "# ceiling at 135,000 and the wrap redesign as #306's second job, after your 102 ticks?\"): THE BOOT\n"
    "# CEILING IS 135,000. It SUPERSEDES `s305-D29`, which is not edited (its text above is kept). The\n"
    "# reason: the cloud seat boots at about 131,000 (#304 131,130 · #305 131,040), mostly tools and the\n"
    "# system prompt, which he cannot control — his 11:41 line: *\"it doesnt seem like there is much we can\n"
    "# do about the boot, its just tinkering around the edges\"*. The ceiling stays a TRIPWIRE FOR A REAL\n"
    "# JUMP, not a target. ⛔ SHRINK-ONLY RESUMES FROM 135,000: the next move is DOWN, on a measurement.\n"
    "BOOT_CEILING_TK = 135_000      # `s305-D64` (was 130_000 — `s305-D29`, until the Mac seat).\n"
    "                               # (before it 72_768 — `s295-D3`, #295 turn 1; 70_000 — `s241-D1`.)\n")
rep("            for name, want in ((\"BOOT_CEILING_TK\", 130_000), (\"STOP_LINE_TK\", STOP_LINE_TK),\n",
    "            # ★★ #305 post-wrap — MOVED A THIRD TIME, BY DAVE'S WORD (`s305-D64`, \"yes both\"): the pin is\n"
    "            # the NEW literal 135,000, and the direction check guards 135,000. Re-pinned, not weakened.\n"
    "            for name, want in ((\"BOOT_CEILING_TK\", 135_000), (\"STOP_LINE_TK\", STOP_LINE_TK),\n")
rep("f\"and `s305-D29` to 130,000, each on Dave's word, and it \"",
    "f\"`s305-D29` to 130,000 and `s305-D64` to 135,000, each on Dave's word, and it \"")
rep("                if name == \"BOOT_CEILING_TK\" and isinstance(got, int) and got > 130_000:\n"
    "                    failures.append(f\"[E s305-D29] {name} = {got:,} is ABOVE the 130,000 \"\n",
    "                if name == \"BOOT_CEILING_TK\" and isinstance(got, int) and got > 135_000:\n"
    "                    failures.append(f\"[E s305-D64] {name} = {got:,} is ABOVE the 135,000 \"\n")
open(p, 'w', encoding='utf-8').write(s); print('ok')
