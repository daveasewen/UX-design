# #304 wrap seat - write _CARRIES.md section "residual -> #305": new #304 items first, then the #304 set
# with EVERY age bracket +1 (the #297-#303 rule, re-verified below against #303's own bump), and the
# strikes BY ADDITION with receipts (s183-D1 / s188-D2). Modelled on #303's carries_304.py.
import re, sys
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/304/W/_work')
import _capture_gate as cg
from names_304 import *
AGE = cg._AGE_RE
P = '_CARRIES.md'
txt = open(P, encoding='utf-8').read()
L = txt.split('\n')
assert L[45] == '## residual → #304' and L[47].startswith('> **residual → #304:**'), (L[45], L[47][:40])
assert L[49] == '## residual → #303' and L[51].startswith('> **residual → #303:**')
assert '## residual → #305' not in txt
def bump_all(s):
    s = re.sub(r"\[NEW — 0(,[^\]]*)?\]", lambda m: '[\x00' + (m.group(1) or '') + ']', s)
    s = AGE.sub(lambda m: '[' + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace('[\x00', '[1')
body = re.sub(r"^> \*\*residual → #304:\*\*", "", L[47]).strip()
b303 = re.sub(r"^> \*\*residual → #303:\*\*", "", L[51]).strip()
old304_tail = body.split(' ·  ', 1)[1]
bb = bump_all(b303).split('·'); oo = old304_tail.split('·')
diff = [i for i in range(min(len(bb), len(oo))) if bb[i].strip() != oo[i].strip()]
print('verify +1 on #303->#304: segs', len(bb), len(oo), 'differing', len(diff), '(expect 6 = the #303 strikes)', diff[:10])
old = bump_all(body)
B = '`' + BRIEF + '`'
TAIL = " `_rulings.json` 638, nothing inscribed at #304"
STRIKES = [
 ("⬛ **① THE APOLLO-MCP PROPOSAL PAGE — HE ASKED FOR IT, AND IT IS #304'S FIRST BEAT**",
  "STRUCK AT THE #304 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — BY THE ACT. RECEIPT: lane M wrote v1 at #304's opener (`" + MCP1 + "`, report `" + REPM + "`) and the conductor wrote v2 on his 14:51 and 14:52 BST words of Saturday 2026-09-26 (`" + MCP2 + "`), both committed at `6af293df`. ⚠ AND ONE CLAUSE ABOVE IS CORRECTED BY HIS WORDS, WITH ITS RECEIPT (`s188-D2`): the caution that Jev is dev-time only, so run-time judgement must be mechanical, is his for BUILD time and not a bar on GenUI — *\"" + Q1451 + "\"* (" + B + "). v2 carries rules-then-Jev-ranks. His seven decisions on the page are carried as a NEW #304 item." + TAIL),
 ("⬛ **③ `s277-D12` — TOKENS AT GROUP+TIER — WAS NEVER STARTED**",
  "STRUCK AT THE #304 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — ENACTED. RECEIPT: Run 3 built it to the ruled text (43 `token:<group>` nodes carrying tier, source and blast radius, 835 structural `bindsToken` edges, `knowledge/gen_kg_tokens.py`; `" + REPR3 + "`), committed at `4be130e5`, the status stamped enacted with that sha at `aaf3bb7e`, verified by V2 (`" + REPV2 + "`), CI run `36275037261` read back after `render`." + TAIL),
 ("⬛ **⑨ THE RADIUS BUILD — `s245-D10` IS RULED CONSOLE-ONLY AND ITS ENACTMENT IS NOT DONE [",
  "STRUCK AT THE #304 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — ENACTED. RECEIPT: Run 3 minted the ruled console set through the generator (control 8 to 6, surface 20 to 8, container 20 to 12, segmented thumbs derived by `thumb_radius()`), mono, legacy and supercharge pixel-identical (`" + REPR3 + "`), committed at `4be130e5`, stamped enacted at `aaf3bb7e`, verified value by value by V2 (`" + REPV2 + "`), CI run `36275037261`. ⚠ The card padding 20 to 8 that rode with it has no ruling of its own and is carried as a NEW #304 item." + TAIL),
 ("⛔ **⑬ #227 SHIPPED TWO ENTRY POINTS WITH NO HELP GATE AND CI STEP 6 ABORTS ON THEM",
  "STRUCK AT THE #304 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — THE ABORT IS GONE. RECEIPT: Run 1 (`" + REPR1 + "`) cleared every abort-route red, the help gate at step 8 passes, and CI's step 6 asked every step for the first time since 2026-09-09 — 146 of 146 in run `36257551837` on `6af293df` (`" + REPC1 + "`), and 152 of 152 on `8a5fa863`, run `36311157795` (`" + REPC6 + "`)." + TAIL),
]
segs = old.split('·')
for key, why in STRIKES:
    assert '·' not in why, why[:60]
    hits = [i for i, s in enumerate(segs) if s.strip().startswith(key)]
    assert len(hits) == 1, (key[:50], hits)
    segs[hits[0]] = segs[hits[0]].rstrip() + ' ⛔ **' + why + '** '
old = '·'.join(segs)
NEW = [
 "⬛ **① THE TUESDAY SITTING, 53 CALLS — CALL 1 FIRST: CUT v1.0.14 FROM CANDIDATE 2?** [NEW — 0, DAVE'S] — the page is `" + SITTING + "` (seat W5b, Fable 5.1, corrected by F5 on V5's reading; report `" + REPW5B + "`), opened through the private artifact \"Apollo 304 review\" (`" + ARTIFACT_URL + "`). Six groups ordered by how much a yes unblocks: release 4, looks 9, brain 14, lines and housekeeping 14, Apollo-MCP 10, Jev 2. Groups 3 to 6 (calls 14 to 53) carry a recommendation each and can go on one \"yes to the recommendations\"; groups 1 and 2 want his eye, each with its picture. R4s and R4s2 disagree on the cut's condition and the page shows both (`" + REPR4S2 + "`). His answers come back by \"Copy as text\" pasted in chat",
 "⬛ **② THREE BEHAVIOURS SHIPPED ON A VERIFIER'S READING, WITHOUT A RULING — CONFIRM OR REVERSE** [NEW — 0, DAVE'S] — (a) tick-label thinning, a row of centred x-axis labels thinned to the smallest stride that clears by 8px, anchored on the LAST category, every chart (W4a `" + REPW4A + "`, commit `3100da99`, V4 `" + REPV4 + "`: *\"has NO ruling and is a canon behaviour change on every chart — it should ship\"*); (b) the right-gutter fit, under `ds-012(b)` by reading, provisional `PL_MAX_FRAC` and `PL_EDGE_PAD` (W5a `" + REPW5A + "`, commit `52049781`, V5 `" + REPV5 + "`, sitting call 6); (c) console card padding 20 to 8, `padding/card/internal`, which `s245-D10` does not name, read as licensed by `s201-D4` (R3 `" + REPR3 + "`, commit `4be130e5`, V2). Each commit message declares it",
 "⬛ **③ TWO THINGS HELD BACK FOR HIS EYE, NOT ENACTED** [NEW — 0, DAVE'S] — the Kpi-tile descender fix, `s261-D4`, three ways (V3's trim form, the clip-visible form, or leave it), diffs and held pages in `" + HELD + "` (W3a `" + REPW3A + "`); and W5a's root text-box-trim default, which reached 26 components on canon pages unruled (V5 `" + REPV5 + "`, sitting call 41c)",
 "⬛ **④ THE APOLLO-MCP PAGE'S SEVEN DECISIONS** [NEW — 0, DAVE'S] — `" + MCP2 + "`: the PoC first (June's contextual dashboard on mock data), entitlements a labelled best guess on his word (*\"" + Q1452 + "\"*), rules pick and Jev may rank. The probe behind it: 137 of 137 metas yield a valid A2UI v0.9.1 entry, 17 ready for run time (`" + REPR5 + "`). Group 5 of the sitting page (`W-304m`)",
 "⬛ **⑤ JEV AS AN EDGE SUGGESTER — CUT A HAND-RUN SWEEP, OR LEAVE IT?** [NEW — 0, DAVE'S] — his 16:19 BST question of Saturday, *\"" + Q1619 + "\"*. Lane J: AUC 0.954 on real against planted edges, clean at both extremes and noisy in the middle; worth keeping as a suggester he ratifies for four edge types (`obeys`, `providesRole`, `answersIntent`, `hasDataShape`), never a gate, never in `_build_all.py`; node titles are mechanical and W5c built them (`" + REPJ + "`). Group 6 of the sitting page (`W-304jv`)",
 "⚠ **⑥ THE REVIEW SURFACE IS NOW ONE ARTIFACT, AND ITS HUB'S LINKS ARE UNPROVEN** [NEW — 0] — his 11:44 BST words of Sunday, *\"" + Q1144 + "\"*, and his screenshot, *\"" + QSHOT + "\"*: `computer://` links to files in his repo folder cannot be previewed in the Claude app. Review pages now go to him as ONE private artifact (`" + ARTIFACT_URL + "`), republished to the same URL, never as `computer://` links. Version 2 (12:13 BST) added a fixed \"All review pages\" button to the published copies only (his 12:11 words, *\"" + Q1211 + "\"*). ⛔ MEASURED AT THE #304 WRAP SEAT: the hub's hrefs read `_SITTING-…` while the files are published under `notes/_SITTING-…`, so the hub's links probably do not open. The hub is copied to `" + ARTIFACT_COPY + "`. His decision boxes save per browser and device",
 "⬛ **⑦ THE SCHEDULED DREAM PASS IS AN EXTERNALITY ON A LIVE SESSION — CHANGE ITS RUNBOOK, OR KEEP CARRYING ITS ROW?** [NEW — 0, DAVE'S] — dream pass 14 fired at 07:12 BST Sunday while the runs were live, committed `ff382c0b`, ran `git status` on the mount against the house rule (`" + DREAM + "` § kk9), and by `knowledge/_RUNBOOK-dream-pass.md` step 7b wrote its §🔀 row and stamp into `_LIVE-STATE.md` after its own commit, uncommitted by design. The wave-five index was built over that file and CI step 117 (memento index determinism) went red once (`52049781`, run `36306939769`); W6 traced it (`" + REPW6 + "`), C6 carried the two lines at `8a5fa863` and step 117 read green (run `36311157795`)",
 "⚠ **⑧ `_git_commit.sh` STRANDS THE INDEX LOCK ON AN UNCHANGED NAMED PATH AND THEN BLAMES THE NEXT PATH** [NEW — 0] — measured by C1 (`" + REPC1 + "`): `git add` of an unchanged path makes git roll back its lock, the mount forbids the unlink, and the next `git add` fails, while the door sends stderr to `/dev/null` and names the wrong path. Workaround used by C2 to C6: name only changed or untracked paths. The fix belongs in the staging loop; not made",
 "⚠ **⑨ CI STEP NUMBERS MOVED +4 FROM STEP 86 UP AT `52049781`** [NEW — 0] — the four KG generator steps were wired as steps 86 to 89 (152 steps), so any carry or report quoting a step at or above 86 from before that commit reads four low: wave one's steps 86, 94, 127, 128 and 132 are today's 90, 98, 131, 132 and 136 (`" + REPC5 + "`)",
 "⚠ **⑩ THE CONDUCTOR'S WINDOW RAN 153,905 PAST THE 300K HARD LINE** [NEW — 0] — a hand sum at the #304 wrap seat over `" + TRANSCRIPT + "`: boot 131,130, over 256,000 at 17:51 BST Saturday, over 300,000 at 22:08 BST Saturday, 389,266 at 11:16 BST Sunday, and 453,905 at the message that launched the wrap seat. The runs were delegated, so the window grew by the read-backs; named, not graded",
]
for n in NEW:
    assert '·' not in n, n[:60]
line = '> **residual → #305:** ' + ' · '.join(NEW) + ' ·  ' + old.strip()
L[45:45] = ['## residual → #305', '', line, '']
open(P, 'w', encoding='utf-8').write('\n'.join(L))
chk = open(P, encoding='utf-8').read().split('\n')
l305 = next(l for l in chk if l.startswith('> **residual → #305:**'))
items = cg._carry_items(l305)
l304 = next(l for l in chk if l.startswith('> **residual → #304:**'))
print('items', len(items), 'prev', len(cg._carry_items(l304)), 'struck-this-wrap', l305.count('AT THE #304 WRAP, BY ADDITION'), 'new', len(NEW))
open('notes/_lanes/304/W/_work/carries_count.txt', 'w').write(str(len(items)) + '\n')
