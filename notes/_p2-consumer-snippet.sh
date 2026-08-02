# _p2-consumer-snippet.sh — DELIVERED NOT WIRED: consumer block for `_build_live_state.py --selftest` (Sub C, phase-2).
# Ruling: #78-D2 (option-select 2026-08-02) — the spine's ungated writer gets a selftest AND a consumer at the commit seam.
# Goes in: knowledge/_git_commit.sh, IMMEDIATELY AFTER the existing wrap-gate consumer block (#74-D1, the `if [ "$WRAP" -eq 1 ]` block ending "DECLARED not-a-wrap"). Owner of that file wires it.

# spine-writer selftest consumer — RULED #78-D2 (same WARN/--wrap split as the wrap gate above,
# #74-D1's shape). The #77 periphery inventory found `_build_live_state.py` splices _LIVE-STATE.md
# — the spine, the token-store of truth — IN PLACE with no selftest and no gate: an ungated writer
# on the one file every cold session trusts. The selftest now exists (5 arms: happy-path splice,
# idempotency, named refusal on a marker-less spine, no-half-writes on every failure path, and
# mutation controls proving each green can fail; it runs only on tempdir copies and hashes the
# real spine before/after). The commit seam is where a broken splicer's output becomes DURABLE,
# so it is consumed HERE — and as above, a mid-session commit is a CORRECT state, so red only
# WARNS there and BLOCKS on --wrap.
# ⚠ Mutation scope: mutant runs (suffix-eating splice, volatile block, refusal-bypass) proved the
# arms red on doctored COPIES; this consumer trusts the selftest's exit code, as with the wrap gate.
if [ "$WRAP" -eq 1 ]; then
  python3 knowledge/_build_live_state.py --selftest ||
    fail "spine-writer selftest RED on a --wrap commit — _build_live_state.py's splice of _LIVE-STATE.md is not trustworthy and this is the FINAL commit (#78-D2 consumer). Its failed arms are printed directly above and it owns the diagnosis; fix the writer, do not hand-patch the spine around it. Nothing has been staged."
  echo "— spine-writer selftest GREEN on the wrap commit (#78-D2 consumer)"
else
  if python3 knowledge/_build_live_state.py --selftest; then
    echo "— spine-writer selftest green (mid-session commit, DECLARED not-a-wrap)"
  else
    echo "⚠ spine-writer selftest RED — visible, not blocking: this commit is DECLARED not-a-wrap (#78-D2)."
    echo "  The session's FINAL commit must run with --wrap, where red BLOCKS."
  fi
fi
