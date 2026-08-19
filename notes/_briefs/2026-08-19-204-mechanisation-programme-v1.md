# The mechanisation programme — ruled `s204-D1`, #204, 2026-08-19

*Governed by `s204-D1` (Dave's: "lets not loose any of this, we'll do the 1 and two next and
scope and plan the rest, I need some rigour for this so I don't spend my week fixing
externalities"). This file is the durable home of all five items; the ruling points here.
THE RIGOUR BAR applies to every item: consumer named at birth · priced consequences section ·
no gate that cannot pass in the environment it runs in (#173 class) · promotion by evidence,
never speculation.*

## Adopted trial amendments (in force for every future PM wave)

1. **Incremental claim table** — the build-PM appends claim rows as each lane closes; the
   table is never a final act. (#204 proof: the build-PM died at minute 43 with the table
   unwritten; a finisher reconstructed it — one lossy hop.)
2. **Fix loop inside the build-PM's mandate** — verifier CONTRADICTED rows route back as a
   repair lane, same fences, before the table is called final. (#204 proof: the fix went to a
   cold fourth sub because agent-resume was unavailable — ~30-40K cold-start tax per hop.)
3. **Run-before-cite** — the verifier may not cite a search it did not run; output pasted.
   (#204 proof: the verifier composed a query, claimed 2 hits, ran it after — 35 hits incl.
   `s140-D1`. It caught itself; the rule removes the reliance on self-catching.)
4. **Verifier render lane** — stage Chromium+Playwright per `_RUNBOOK-render-verify.md`
   (recipe proven ×3; potholes: ENOSPC masquerading as network failure, foreign-session /tmp),
   verify from pixels: contrast maths on rendered ink · hit-area geometry · dangling-var
   silent-black (pixel sampling — the class that passes all thirteen gates) · every theme leg
   light AND dark. Output: machine conformance report per review surface + side-by-side PNGs.
   Boundary, stated: this proves MECHANICS, not taste — Dave's eye remains the instrument for
   design judgment; the lane shrinks his review from find-the-defects to rule-on-the-choices.

## BUILD NEXT (ruled, store rows W-44 · W-45)

### Item 1 — schema'd tables + generated join + evidence linter (`W-44`)
- Claim and challenge tables become JSONL with a fixed schema (id · claim · evidence pointer
  · tag PROVEN/MEASURED/CLAIMED/UNPROVEN · verdict CONFIRMED/CONTRADICTED/UNTESTED).
- A join script emits ONLY disagreement rows, untested rows, fence-touch rows; CONFIRMED
  collapses to a count. The conductor reads a generated diff, never two documents.
- An evidence linter enforces `s182-D1` (every mechanical claim carries its probeable token)
  and SAMPLES: re-runs a random subset of evidence commands and compares rc.
- **Consumer at birth:** the PM-wave briefs (both PMs write the JSONL; the conductor's seat
  runs the join at the seam). Not wired into `_build_all.py` until driven in ≥1 real wave.
- **Consequences, priced:** a schema too tight forces prose back into chat (the honest-refusal
  vocabulary class — leave a free-text `note` field); the join script must SURFACE, never
  suppress — a row it hides is a decision nobody made; markdown human-readable renders are
  generated FROM the JSONL, never hand-kept beside it (write-once, ADR-0017).

### Item 2 — verifier probe registry + promotion rule (`W-45`)
- Every historically-found defect class becomes a scripted probe: meta-schema sweep ·
  duplicate-ID/IDREF scan · dangling-var pixel test · premise-vs-store diff · stale-figure
  grep (carried numbers vs live measurement). Registry = a directory + manifest; the verifier
  brief says "run the registry, then hunt free".
- **Promotion rule:** a probe that catches a real defect TWICE (two sessions, receipts named)
  becomes a candidate `_build_all.py` gate — candidature recorded in `_DS-IMPROVEMENTS.md`,
  promotion itself remains governed by derivation governance (Dave promotes).
- **Consumer at birth:** the verifier-PM brief (every wave). The registry manifest carries a
  `caught:` ledger per probe — the promotion evidence IS the ledger.
- **Consequences, priced:** registry probes rot like all instruments — each needs a selftest
  (plant-then-detect both directions, the borrowed-instruments pattern); a registry the
  verifier trusts too much narrows its free hunting — the brief must keep the free-hunt
  mandate explicit; sandbox-vs-CI environment splits (#173) apply to any pixel probe.

## SCOPE AND PLAN ONLY (not build — `W-46` is the scoping lane)

### Item 3 — decision-capture controller (attacks Dave's review burden directly)
One generated page: one card per PROPOSED item — evidence, store-search (s202-D3 attached),
options as buttons; picks written to a jsonl the CONDUCTOR inscribes from via
`_inscribe_ruling.py`. Machinery captures and transports decisions; it NEVER makes them.
Scoping questions: where picks land (new jsonl vs `_REVIEW-SIGNOFF.md`) · how a pick's
firmness is read back (the readback-sensation rule — a pick from an incomplete set reads as a
ruling) · live-controller conventions per `feedback-live-controller` (live contrast + export).

### Item 4 — mint-time brief generation (kills the stale-premise class at source)
`gen_brief.py` mints PM briefs from the live store: open items, DO-NOT-RULE pulled from
rulings tagged Dave's, fences from the runbook, premise table PRE-FILLED by running the
probes at mint time (`s200-D1` mint-time derivation pattern). Scoping questions: brief schema
· which probes are mintable vs seat-bound · how a generator's owned regions are declared
(the do-not-rule-list-cannot-fence-a-generator class).

### Item 5 — CI pixel leg
Once item-2 pixel probes exist as scripts, the existing CI render job runs them on every
push. Scoping questions: shared measurer with the sandbox (#173 — a gate that cannot pass in
one environment) · which probes are push-blocking vs survey-tier · the could-not-ask exit
protocol (still unruled, carried).

## Order and prices (PICKED, Dave may reorder)
W-44 then W-45 next session(s), each ~one Opus PM lane; W-46 scoping doc ~one lane, its output
three scoped proposals returning to Dave. Items 3-5 build only after their scopes are ruled.
