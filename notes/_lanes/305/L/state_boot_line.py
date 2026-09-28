# #305 lane L - Dave's boot line added BY ADDITION to W-305w (the row carrying _HANDOFF-156 OWED item 9), through _state.py.
import sys; sys.path.insert(0, 'knowledge')
import _state as st
LINE = "it doesnt seem like there is much we can do about the boot, its just tinkering around the edges"
doc = st.load()
it = [i for i in doc['items'] if i['id'] == 'W-305w']
assert len(it) == 1 and it[0]['state'] == 'open', it
it = it[0]
before = it['body']
assert LINE not in before
it['body'] = before + (" · #305 post-wrap (by addition, lane L, 2026-09-28): Dave's words on the boot, Mon 11:41 BST, verbatim: \""
                       + LINE + "\" - a view, not a ruling (not inscribed); it bears on the boot-ceiling question this row carries "
                       "(_HANDOFF-156 OWED item 9: cut the boot, move the ceiling again, or keep the declared path), which stays open. "
                       "Source: notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md#The boot.")
assert it['body'].startswith(before)
ok, fails, _ = st.check(doc)
print('check ok', ok); assert ok, fails[:5]
st.save(doc)
print('W-305w body', len(before), '->', len(it['body']))
