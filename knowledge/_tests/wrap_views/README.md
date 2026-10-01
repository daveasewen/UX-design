# wrap_views fixtures — one frozen wrap per directory

Each `<n>/` holds the wrap's `STORY.md` (the one hand-written file) and `FACTS.json` (the one measured file,
`_wrap_facts.py`, with its phase-3 keys and its `post` block), and `expected/` — every view `_wrap_views.py`
generates from the two, frozen byte-exact. `python3 knowledge/_wrap_views.py --selftest` regenerates each
fixture and compares; a template change that moves a byte goes red here and is re-frozen deliberately
(copy the new output in, in the same commit as the template change, and say so in the commit).

- `310/` — the #310 wrap (one day, no date split, one CI red, two subs), derived backwards from its hand-written
  views by #311 lane E0 (`notes/_lanes/312/E/STORY-310.example.md`); facts extended at #312 lane E-build from
  the real transcript (`knowledge/_tmp/wrap310/conductor-310.jsonl`, staged) and the real commit history.
- `309/`, `311/` — owed by the replay lane (#312 E-replay): the date-split branches, two CI reds, six and
  thirty-three subs. Their extended facts are ready at `notes/_lanes/312/E/facts/FACTS-<n>.json`.

The fixtures are the design's § 8 (`notes/_lanes/312/E/DESIGN.md`): frozen after the replay has diffed the
generated views against the hand-written ones and explained the residue.
