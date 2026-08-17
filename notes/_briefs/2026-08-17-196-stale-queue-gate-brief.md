# Brief — stale-queue gate (`_validate_queue_fresh.py`) · #196 · Opus build sub

**Commissioned by:** Dave, #196 ("I want a proper fix, thorough and tested").
**Class being fixed:** prose work-state claims outlive reality — GM §C·1(a) STEP 2 sat "open"
for 12 sessions after the wave LANDED (`df44e51` #95). Second recurrence on that exact line
(#26 was the first). Sister defects: 7-vs-14 meta count (#195), standing-44-measured-4 (#194).
The cure's shape: the 119-sweep's still-reads clause, pointed at queue items instead of
decision literals. Mirror of the doc-row gate: that catches documents with no row; this
catches rows outliving their documents.

## Deliverable

`knowledge/_validate_queue_fresh.py` + queue-line annotations in `GOOD-MORNING.md` §C·1 +
a route in `knowledge/_build_all.py` (STEPS entry **and** ROUTE_ROWS row — a STEPS entry
with no ROUTE_ROWS row aborts every full build above step 1; see `_build_all.py:236`).

## Mechanism (the annotation grammar — build THIS, don't invent another)

Open queue items gain a machine tail, one per item, HTML-comment so GM's render is untouched:

`<!-- qprobe: state=open expects-absent=knowledge/snippets/Chart-foo.reference.html,... -->`
`<!-- qprobe: state=landed receipt=df44e51 -->`
`<!-- qprobe: state=partial declared="lane B open; lanes A landed" expects-absent=... -->`

Rules:
- `state=open` + `expects-absent=<paths>`: gate FAILS (warn-tier) if ANY named path exists —
  an "open" item whose deliverables are on disk is the defect, loud and named, quoting the
  path AND the queue line ([[gate-must-quote-what-it-forbids]]).
- `state=landed` + `receipt=<sha>`: gate verifies the sha exists in `git log` (format check +
  `git cat-file -e`). A landed claim with no receipt or a bad sha = fail.
- `state=partial` + `declared=`: the legal form for honest in-between states — NEVER refuse an
  honest statement ([[honest-refusal-needs-a-legal-form]]); `expects-absent` optional, checked
  if present.
- An open-looking §C·1 item (bold heading line starting `**(a)`–`**(e)` or a `STEP N` clause)
  with NO qprobe tail = **fail** (gate the PRESENCE, not the drift — an unannotated item is
  invisible to the gate forever, the exact instrument-without-a-consumer trap).
- Unparseable qprobe = loud named refusal, rc≠0, never a silent skip ([[a-crash-is-not-a-fail]]).

## Annotate the real corpus (part of the deliverable)

Annotate §C·1 strands (a)–(e) as they truly are TODAY, by measurement:
(a) STEP 1 + STEP 2 landed (receipts `00abdf3`, `df44e51`) — the #196 correction is already in
the file; add the qprobe tails · (b)/(c)/(d) open — name the artefacts each would produce
(survey the strand text for its named files; where a strand names no concrete artefact, use
`state=open expects-absent=` with an empty list and `declared="no probeable artefact"` — a
DECLARED gap passes, a silent one fails) · (e) partial (legacy half enacted `s131-D1`;
`s130-D4/D5/D6` + tabs badges ruled-not-enacted; owner DAVE).
⚠ Base your annotations on the CURRENT file content — read it, don't trust this brief's
summary ([[premise-ages-faster-than-rule]]).

## Proof standard (all mandatory, in this order)

1. **Drive on real data:** run against today's GOOD-MORNING.md → green after your annotations.
2. **Mutation, FAIL direction:** flip strand (a) STEP 2's qprobe back to `state=open
   expects-absent=knowledge/snippets/Chart-pie.reference.html` → gate MUST refuse, quoting the
   path; restore → green. This replays today's actual 12-session miss as the test case.
3. **Mutation, other direction:** plant `state=landed receipt=0000000` → must refuse (bad sha);
   remove a qprobe tail from an open strand → must refuse (presence rule). Restore → green.
4. **Selftest:** `--selftest` with ≥4 bites covering: path-exists refusal · bad-receipt
   refusal · missing-tail refusal · partial-with-declared passes. Wire selftest into the route
   (`_build_all.py` gets BOTH the gate step and its selftest reachable — see #165's lesson at
   `_build_all.py:140`).
5. **Route proof:** `python3 knowledge/_build_all.py --check-route <label>` equivalent — use
   whatever the existing per-step invocation form is (READ the file; do NOT run a full
   `_build_all.py` — any partial run strands the tree mid-build, docstring lines 5–21).
6. Confirm `check_routes` green (the routes count will go 122 → 123; report the real number
   you measure, don't assert this one).

## Severity

**WARN tier.** The BLOCKING flip is DAVE'S — put a one-line `# BLOCKING flip = Dave's word
(#196)` comment at the severity constant.

## Fences — DO-NOT-RULE / DO-NOT-TOUCH

- ⛔ NO writes to `knowledge/_rulings.json` (only `_inscribe_ruling.py` writes it, conductor's).
- ⛔ NO git commits, NO push — report file list; the conductor commits ONE commit.
- ⛔ Do NOT run `_build_all.py` (full or partial). Per-step invocations only.
- ⛔ Do NOT edit generated files: `_CHAIN.md`, compliance outputs, `_memento-index.json`.
  GOOD-MORNING.md §C·1 is hand-prose and IS yours to annotate — but ONLY comment tails +
  nothing ruled; do not reword Dave's text.
- ⛔ Do NOT touch the `#166` label strings in `_build_all.py` (join keys).
- ⛔ The queue items' CONTENT (what is open, what it means) is Dave's/conductor's — you
  annotate measured state, you do not close, re-scope, or re-order items.
- ⛔ `pip install tiktoken --break-system-packages` first if any tool refuses on it.

## Consequences / pitfalls — REPLAYED (Dave #165, mandatory reading)

- (a) An over-eager presence rule could nag every prose line in §C·1; scope the item-detector
  to the strand-heading grammar above and TEST that scope (a non-item line must NOT trigger).
- (b) `expects-absent` on partially-landed work would false-fail — that's what `state=partial`
  + `declared=` exists for; the gate must pass a declared partial WITHOUT checking absent paths
  unless given them.
- (c) This gate reads a ROLLING file (GM). Its qprobe tails must survive the banner-roll
  machinery — comment tails live in §C body, which does NOT roll; verify by reading
  `_roll_state.py`'s targets before finalising placement. If they could roll, say so in the
  report; do not silently relocate.
- (d) A green that can't fail is an assertion — hence the mandatory mutation drives.

## Report back (lands in conductor fill — keep it tight)

Files touched · routes count measured · each proof step's one-line result · any fence you
could not honour, DECLARED · your own token spend if measurable.
