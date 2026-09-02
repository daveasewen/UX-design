set -u
fail() { echo "✗ $1" >&2; exit 1; }
# ── POLARITY GATE — s238-D7 (#238 lane P): the five refusals, AT THE COMMIT SEAM ─────────────
# "A gate that is not a consumer of every commit is not a gate" (s238-D7's last sentence). The
# same `--check` runs as a _build_all.py STEPS entry; it runs HERE because the commit is where a
# dangling party, an untyped link, a judgement field, a typed status or an authored edge file in
# knowledge/brain/ turns DURABLE — and where a stale derived file (knowledge/brain/_generated/,
# status with a clock per s238-D3) would be committed against a moved home. Refusals are NAMED by
# the gate itself (R1..R5 / STALE-GENERATED / MISSING-GENERATED); this line owns only the
# consequence — nothing staged. It regenerates NOTHING (a stale derived file is the author's to
# re-derive with `--write` and NAME in the reconciliation, P5). Declared-gap hatch POLARITY_ACK,
# spelled like its neighbours (declared passes, silent fails). Harness: _test_git_commit.py stubs
# `_validate_polarities.py` (STUB_POLARITY_EXIT) and drives it non-zero + through the hatch.
if [ -z "${POLARITY_ACK:-}" ]; then
  python3 knowledge/_validate_polarities.py --check ||
    fail "polarity gate REFUSED (s238-D7) — the refusal is NAMED directly above and the gate owns the diagnosis (a node in knowledge/brain/polarities.json fails one of the five refusals, or knowledge/brain/_generated/ is stale — for staleness run: python3 knowledge/_validate_polarities.py --write, then NAME the regenerated files in your --reconciled list). Or re-run with POLARITY_ACK=\"<real reason>\" to pass it as a DECLARED gap. Nothing has been staged."
  echo "— polarity gate green (_validate_polarities.py --check passed, s238-D7)"
else
  echo "— polarity gate: DECLARED GAP — $POLARITY_ACK"
fi
echo SEAM-BLOCK-EXIT-0
