# #238 — COMMON RULES FOR EVERY LANE (read first; each lane brief points here)

**Seat:** repo at `/sessions/wonderful-adoring-euler/mnt/UX-design/` (bash) = `/Users/daviewen/Documents/Claude/Projects/UX-design/` (Read/Write/Edit). Branch `master`, HEAD `97519cd` + seven uncommitted rulings `s238-D1`…`s238-D7` in `knowledge/_rulings.json` (read them first: `python3 -c "import json;[print(e['id'],'—',e['ruled'][:160]) for e in json.load(open('knowledge/_rulings.json'))['rulings'] if e['id'].startswith('s238')]"`).

**Model:** you are a Fable sub on a quota-burn day (Dave: "max out the tokens", "just test the crap out of it"). Spend freely on probes, renders, self-tests. Never spend on re-reading whole archives — `python3 knowledge/_memento_search.py "<q>"` → `--fetch <id>`.

**Never:** `git` of any kind (no commit, checkout, stash, branch — the conductor commits) · writes to `knowledge/_rulings.json`, `knowledge/_state.json`, `_CARRIES.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md`, memory · `_build_all.py` (a partial run strands the tree) · `_gen_chain.py` · edits to dated history (prior reports, their `assets/`, plan v1, the T review, briefs) — ADR-0017.

**Register:** rulings are quoted from `_rulings.json`, never memory; everything you propose is FLOATED ("proposed", never "the default is"); UNPROVEN is an honest word — use it, never guess (ADR-0016). Our words + ≤15-word quotes.

**Sandbox:** one heavy call at a time (~178 s kill); `pip install tiktoken --break-system-packages` if a gauge refuses; `TMPDIR=/dev/shm` for scratch; renders per `knowledge/_RUNBOOK-render-verify.md` (read its newest stratum first; lane T finding 11: the stored `fonts.conf` hardcodes another seat's mount path — generate a per-seat one).

**Consequences replayed (Dave #165):** every report carries a PITFALLS section naming what could go wrong with what you built, owner per row.

**Filing (s218-D7):** copy `notes/_subreports/_TEMPLATE.md` → `notes/_subreports/2026-09-02-238-<X>-<slug>.md`; assets → `notes/_subreports/assets/2026-09-02-238-<X>-<slug>/`; `brief:` = your lane brief. Close with **REPLAY-THESE** (≤7 lines, sized). Token spend: `UNMEASURED — no message.usage at a sub's seat` + the shape.

**Return to chat = a STUB, ≤12 lines:** report path · counts line · REPLAY-THESE · UNPROVEN list · files written (paths only). Nothing else — the conductor's window is the binding budget.
