"""#287 lane K — the store row for this lane's report, written through _state.py's module API
(never by hand-editing _state.json). Shape copied from notes/_lanes/286/R2/row_w286r.py."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'knowledge'))
import _state

doc = _state.load()
ok, fails, notes = _state.check(doc)
print('PRE  check ok=%s fails=%d' % (ok, len(fails)))
if any(i['id'] == 'W-287k' for i in doc['items']):
    print('W-287k already present — nothing written'); sys.exit(0)
it = _state.add(doc,
    id='W-287k',
    title='#287 lane K — the explorer READS the logo masters (`sizes`) and is rebuilt at v1.27',
    state='open', owner='dave', opened=287, project='apollo',
    closes_when=("Dave has opened a logo node in the served explorer and either accepted the three "
                 "readings of `sizes` (the aside's masters row, INSPECT's per-height record rows, the "
                 "MASTERS tab) or named what he wants shown differently"),
    home='notes/_subreports/2026-09-19-287-K-explorer-shows-sizes.md',
    links=['notes/_lanes/287/K/', 'knowledge/_kg_explorer.template.html',
           'knowledge/_build_kg_explorer.py', 'notes/_KG-EXPLORER.html',
           'notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md'],
    body=("⬛ Dave 2026-09-19: \"keep `sizes` and rebuild.\" The key name stands and notes/_KG-EXPLORER.html "
          "is rebuilt at v1.27, where #286 lane R2's `sizes` map is now READ in three places instead of "
          "being one line of JSON: the aside's logo head names the 5 heights, INSPECT's record lists one "
          "row per height linking its own master SVG with the stored geometry and digest, and a MASTERS "
          "tab draws all five at their declared heights on the lockup's own ground. Measured: 8/8 logo "
          "nodes carry sizes with 5 keys, 40 entries byte-equal to _logo_nodes.json; 8 nodes / 33 edges "
          "unchanged; _validate_kg.py green. The baked coordinates moved because the Constitution grew "
          "between builds (11 nodes from another lane's _rulings.json), not because of this field."))
ok, fails, notes = _state.check(doc)
print('POST check ok=%s fails=%d' % (ok, len(fails)))
for n in notes: print('  NOTE:', n[:160])
_state.save(doc)
print('SAVED W-287k')
