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
# ⛔ #239 lane F (V finding 10 D2): `POLARITY_BRAIN_DIR` was a SILENT second hatch — the gate
# honours it, so the seam read a clean copy elsewhere while the tree's own knowledge/brain/ was
# dirty, and the only trace was the gate's `home …` line. Now the redirect is DECLARED on the
# record AND the tree's own home is gated in the same breath (the commit carries THAT one).
# Since #239 an absent home in the source repo is rc 1 from the gate itself (never 77), so the
# `|| fail` below stops on it at every door, not only here.
if [ -z "${POLARITY_ACK:-}" ]; then
  if [ -n "${POLARITY_BRAIN_DIR:-}" ]; then
    echo "— polarity gate: REDIRECTED to $POLARITY_BRAIN_DIR (DECLARED via POLARITY_BRAIN_DIR — a probe target; the tree's own knowledge/brain/ is gated next and is what the commit carries)"
    python3 knowledge/_validate_polarities.py --check ||
      fail "polarity gate REFUSED (s238-D7) on the REDIRECTED home $POLARITY_BRAIN_DIR — the refusal is NAMED directly above. Nothing has been staged."
    ( unset POLARITY_BRAIN_DIR; python3 knowledge/_validate_polarities.py --check ) ||
      fail "polarity gate REFUSED (s238-D7) on the TREE'S OWN knowledge/brain/ (the redirect above passed, the commit's home does not) — the refusal is NAMED directly above. Nothing has been staged."
  else
    python3 knowledge/_validate_polarities.py --check ||
      fail "polarity gate REFUSED (s238-D7) — the refusal is NAMED directly above and the gate owns the diagnosis (a node in knowledge/brain/polarities.json fails one of the five refusals, or knowledge/brain/_generated/ is stale — for staleness run: python3 knowledge/_validate_polarities.py --write, then NAME the regenerated files in your --reconciled list). Or re-run with POLARITY_ACK=\"<real reason>\" to pass it as a DECLARED gap. Nothing has been staged."
  fi
  echo "— polarity gate green (_validate_polarities.py --check passed, s238-D7)"
else
  echo "— polarity gate: DECLARED GAP — $POLARITY_ACK"
fi

echo SEAM-BLOCK-EXIT-0
