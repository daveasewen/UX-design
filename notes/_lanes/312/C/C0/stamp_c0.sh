#!/bin/bash
# #311 C0 — run INSIDE the seat-wide commit lock: stamp D17/D18/D19/D58 enacted at the build sha, regen titles + rulings page, add the born-closed row.
set -e
SHA="$1"; [ -n "$SHA" ] || { echo "usage: stamp_c0.sh <build sha>"; exit 2; }
cd "$HOME/mnt/Projects--UX-design"
for id in s305-D17 s305-D18 s305-D19 s305-D58; do
  python3 knowledge/_inscribe_ruling.py --set-status $id enacted --evidence-sha "$SHA" --write 2>&1 | tail -1
done
python3 knowledge/gen_kg_titles.py --write 2>&1 | tail -1
python3 knowledge/_render_rulings.py 2>&1 | tail -1
python3 - <<'PY'
import sys; sys.path.insert(0, "knowledge")
import _state
d = _state.load()
if not any(i.get("id") == "W-311c0" for i in d["items"]):
    _state.add(d, id="W-311c0", home="notes/_subreports/2026-10-01-311-C0-schema-calls.md",
        title="#311 lane C0 report - s305-D17, D18, D19 and D58 built in the metas and meta.schema.json and stamped enacted: a part's own words as ownText settings, the bento wall's tiles slot by role, 41 same-name clashes settled (32 settings with bindsData, 9 slots), three probe rule arms",
        project="apollo", opened=311, owner="claude", state="done", closes_when="the report is committed",
        closed_by="born closed (s305-D40): notes/_subreports/2026-10-01-311-C0-schema-calls.md filed at #311 - the file is the record.",
        body="s218-D7 filed report.", condition="stated")
    _state.save(d); print("row W-311c0 added")
PY
