# wrap_views fixtures — one frozen wrap per directory

Each `<n>/` holds the wrap's `STORY.md` (the one hand-written file) and `FACTS.json` (the one measured file,
`_wrap_facts.py`, with its phase-3 keys and its `post` block), and `expected/` — every view `_wrap_views.py`
generates from the two, frozen byte-exact. `python3 knowledge/_wrap_views.py --selftest` regenerates each
fixture and compares; a template change that moves a byte goes red here and is re-frozen deliberately
(copy the new output in, in the same commit as the template change, and say so in the commit).

- `310/` — the #310 wrap (one day, no date split, one CI red, two subs), derived backwards from its hand-written
  views by #311 lane E0 (`notes/_lanes/312/E/STORY-310.example.md`); facts extended at #312 lane E-build from
  the real transcript (`knowledge/_tmp/wrap310/conductor-310.jsonl`, staged) and the real commit history.
- `309/`, `311/` — frozen by #312 lane E-replay (2026-10-01): the date-split branches (resumed after a pause / ran
  on), two CI reds and a CI read still owed at the wrap (#309), six and thirty-three subs, #311's three pushes and
  two-half pre-push check. Their stories were derived backwards from the hand-written views and replay GREEN
  (`notes/_lanes/312/E/replay/<n>/REPLAY.md`); the facts carry the E-replay readers (`fill.launch`, `subs.each`,
  `fill.source`, `ci.owed_at_wrap`, `ci.pushes`, `rulings.by_date`, the pre-push step ids). `310/` was re-frozen
  the same day for the template changes the replay made (its story is the example plus the figures it had left out).

The fixtures are the design's § 8 (`notes/_lanes/312/E/DESIGN.md`): frozen after the replay has diffed the
generated views against the hand-written ones and explained the residue.
