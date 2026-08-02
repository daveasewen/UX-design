#!/usr/bin/env bash
# _git_commit.sh — the sandbox commit dance, mechanised.
# provenance: lane session 2026-07-26 (dream-pass P2, Dave ruled accept-enact-now) · status: ruled
#
# WHY: 5 of 7 commit-running sessions (3 of 5 at ruling; #36 + #41 since) reconstructed the clear·stage·clear·commit·clear sequence
# from memory under wrap-time heat and hit the lock failure first (dream-pass P2 evidence).
# Per feedback-gate-dont-patch: make the condition mechanical, not another prose reminder.
# The sandbox delete-guard means locks can only be MOVED (mv), never rm'd — see the runbook.
#
# USAGE:  bash knowledge/_git_commit.sh --reconciled <msgfile>
#   <msgfile>      commit message file — UNIQUE name, in a session-owned dir (outputs/), never /tmp
#   --reconciled   you have run `git status --short` and can name WHY every dirty path exists
#                  (runbook step 0.5 — the script cannot do this judgment for you)
# The script REFUSES to stage while any .git/*.lock exists, and never runs rm inside .git.

set -u
cd "$(dirname "$0")/.." || exit 1

RECONCILED=0
WRAP=0
MSGFILE=""
for a in "$@"; do
  case "$a" in
    --reconciled) RECONCILED=1 ;;
    --wrap) WRAP=1 ;;
    *) MSGFILE="$a" ;;
  esac
done

clear_locks() {
  mkdir -p _to_delete/_stale_locks
  for L in $(find .git -name '*.lock' 2>/dev/null); do
    mv "$L" "_to_delete/_stale_locks/$(basename "$L").$(date +%s%N)" || true
  done
}

fail() { echo "✗ $1" >&2; exit 1; }

[ -n "$MSGFILE" ] || fail "no msgfile given. Usage: _git_commit.sh --reconciled <msgfile>"
[ -s "$MSGFILE" ] || fail "msgfile '$MSGFILE' missing or empty (stale-msgfile trap — see runbook gotchas)"
echo "— msgfile head: $(head -1 "$MSGFILE")"

if [ "$RECONCILED" -ne 1 ]; then
  echo "✗ refusing to stage: run 'git status --short', account for EVERY dirty path (step 0.5),"
  echo "  then re-run with --reconciled. Dirty paths now:"
  git status --short
  exit 1
fi

# tiktoken self-heal — enacted #73 (Dave: "lets get the memento stuff fixed"; proposed #72).
# The sandbox is fresh every session, pip state does not survive, and the measurement seam (#59)
# rightly REFUSES when degraded — so every session's first commit was blocking on the same known
# cause with the fix arriving too late. Heal that ONE cause BEFORE the check runs. If healing
# fails, the check below still owns the diagnosis and refuses honestly — this layer removes only
# the cause it can prove and fix, and never masks the check (★ a wrapper must not restate a cause
# it did not determine; it may remove one it verified).
if ! python3 -c "import tiktoken; tiktoken.get_encoding('cl100k_base')" >/dev/null 2>&1; then
  echo "— tiktoken degraded (fresh sandbox) — self-healing: pip install tiktoken --break-system-packages"
  pip install tiktoken --break-system-packages -q >/dev/null 2>&1 || true
  if python3 -c "import tiktoken; tiktoken.get_encoding('cl100k_base')" >/dev/null 2>&1; then
    echo "— tiktoken restored: the measurement below is real, not estimated"
  else
    echo "⚠ self-heal FAILED — proceeding; the chain check below will refuse with the honest cause"
  fi
fi

# chain-staleness gate — this is the seam that actually reads disk state. _gen_chain.py --check's
# OTHER caller (_build_all.py) runs it immediately AFTER regenerating the file, so it can only ever
# catch nondeterminism in build(), never a chain left stale by a hand-edit to GOOD-MORNING.md /
# _LIVE-STATE.md that was never regenerated — the #32 defect, which is what actually landed at the
# #56 wrap (stale chain, clean tree, committed). Refuse loudly; do NOT auto-regenerate here — that
# would stage a file this session never showed you.
# ⛔ CORRECTED #58b, found by the probe worker: this line used to re-assert "_CHAIN.md is STALE" and
# name "regenerate it" as the remedy, on ANY non-zero exit — so when --check refused because its
# TOKEN MEASURER was degraded (tiktoken absent / encoding file unreachable), the honest message it
# had just printed was immediately overridden here by a WRONG CAUSE and a WRONG REMEDY, at the one
# seam that blocks. ★ A WRAPPER MUST NOT RESTATE A CAUSE IT DID NOT DETERMINE. The check owns the
# diagnosis and has already printed it; this layer owns only the consequence — nothing was staged.
python3 knowledge/_gen_chain.py --check ||
  fail "_gen_chain.py --check REFUSED (exit non-zero) — its message is printed directly above and it is the authority on the cause; this script does not second-guess it. Nothing has been staged. If it named STALENESS, run: python3 knowledge/_gen_chain.py — then re-run this script. If it named a DEGRADED MEASUREMENT, regenerating will NOT help: fix tiktoken first (pip install tiktoken --break-system-packages) and re-run."
echo "— chain fresh (_gen_chain.py --check passed)"

# session-witness consumer — BUILT #89, the honest-certification leg of the #87-D1 drill.
# ⛔ WHY THIS CANNOT BE FOLDED INTO THE CHECK ABOVE: `_gen_chain.py --check` compares _CHAIN.md
# against GOOD-MORNING.md. If GM is a session stale (a skipped wrap), the chain regenerates
# CONSISTENTLY stale and --check goes GREEN — the two mechanisms agree with each other and are
# both wrong. That is the seam that certified #84 at #86's first commit, and _gen_chain's own
# #73 comment already said it "canNOT catch a skipped wrap". _session.py answers from a witness
# written at BOOT (knowledge/_SESSIONS.jsonl), which is outside the set of files the corpus
# generates about itself, so it is the only thing here that can disagree with GM.
# WARN/--wrap split, matching #74-D1 and #78-D2: an absent --session is visible mid-session and
# BLOCKING on the final commit, so existing mid-session call sites keep working unchanged.
if [ -n "${SESSION_N:-}" ]; then
  python3 knowledge/_session.py --declare "$SESSION_N" ||
    fail "_session.py REFUSED for declared session #$SESSION_N — its named witnesses are printed directly above and it owns the diagnosis. This is the #86 defect class: the boot path and the running session disagree about who you are, and a commit made now certifies the WRONG session. Fix the cause, or re-run with SESSION_ACK=\"<real reason>\" to pass it as a DECLARED gap (declared passes, silent fails). Nothing has been staged."
  echo "— session witness agrees (#$SESSION_N)"
elif [ -n "${SESSION_ACK:-}" ]; then
  python3 knowledge/_session.py --acknowledge "$SESSION_ACK" || true
  echo "⚠ session witness gap DECLARED, not clean: $SESSION_ACK"
elif [ "$WRAP" -eq 1 ]; then
  fail "the FINAL commit must declare its session: SESSION_N=<n> bash knowledge/_git_commit.sh --wrap --reconciled <msgfile>. Without it the commit subject is derived from GOOD-MORNING.md's own banner, which is the artefact a skipped wrap leaves stale — that is exactly how #84 got certified at #86's first commit. Declare it, or pass SESSION_ACK=\"<real reason>\". Nothing has been staged."
else
  echo "⚠ no SESSION_N declared — visible, not blocking on a mid-session commit (#89)."
  echo "  The session's FINAL commit must declare it, where absence BLOCKS."
fi

# wrap-gate consumer — RULED #74-D1 (the WARN/--wrap split; the wiring was #73's deliberate
# not-done because the tradeoff was Dave's). The gate was honest with no consumer: #71 and #72
# committed through red ([[instrument-without-a-consumer]]). The commit seam is where a red wrap
# becomes DURABLE, so it is consumed HERE — but a mid-session commit is a CORRECT state (three of
# #73's four commits), and a gate that blocked it would make that state unreachable (the ds-022
# lesson). The split: default = the gate runs and reports, red is a VISIBLE WARN and a DECLARED
# not-a-wrap; --wrap = the session's final commit, red BLOCKS.
# ⚠ DECLARED residual, scope honest: nothing at this seam can see a session that never wraps at
# all (the #70 class) — every commit it made was legitimately mid-session. The chain title check
# catches that NEXT session. This consumer kills only the committed-through-red class.
# ⚠ Mutation scope: the shim tests force the gate's EXIT CODE and prove this CONSUMER both ways;
# the gate's own verdict honesty is proven by its own selftest, not here.
if [ "$WRAP" -eq 1 ]; then
  python3 knowledge/_capture_gate.py --wrap ||
    fail "wrap gate RED on a --wrap commit — this is the FINAL commit and the gate now has its consumer (#74-D1). Its findings are printed directly above and it owns the diagnosis; fix them, or declare a real gap in the legal form (⛔ NOT CAPTURED — UNMEASURED. + reason). Nothing has been staged."
  echo "— wrap gate GREEN on the wrap commit (#74-D1 consumer)"
else
  if python3 knowledge/_capture_gate.py --wrap; then
    echo "— wrap gate green (mid-session commit, DECLARED not-a-wrap)"
  else
    echo "⚠ wrap gate RED — visible, not blocking: this commit is DECLARED not-a-wrap (#74-D1)."
    echo "  The session's FINAL commit must run with --wrap, where red BLOCKS."
  fi
fi

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

# T3 #77-D2 — single-source the commit headline from the GM ★ LATEST banner (handoff-testing-
# regime plan, RULED #77). Kills the "found only in the commit message" class (#72/#76): the
# banner becomes the one source and a finding that exists only in the msgfile is unwritable.
# Body lines 2+ stay freehand. Minimal edit — does not touch the --wrap split or the chain check.
# ⚠ #77 refinement: the FIRST cut of this block took "everything after the heading's own first
# em-dash", which lands on the DATE-to-paren dash and so keeps the role clause ("Sun **#N**,
# MODEL, Dave live") as noise ahead of the actual summary. Primary parse now reaches INTO the
# parenthetical and skips past ITS OWN first " — " (the role clause's own separator from the
# summary glyphs) to get the summary alone. Cosmetics must never block a commit, so a heading
# shaped unusually (no " — " inside the parenthetical) is not a hard failure — it falls back to
# the original first-em-dash reading and prints a one-line note naming the fallback. Only a
# WHOLLY MISSING ★ LATEST heading still fails loud (nothing to derive a headline from at all).
python3 - "$MSGFILE" "$WRAP" <<'PYEOF' || fail "T3 headline generation failed (see traceback above) — the ★ LATEST banner in GOOD-MORNING.md could not be parsed. Nothing has been staged."
import re, sys
msgfile = sys.argv[1]
wrap = sys.argv[2]  # "1" on --wrap commits, "0" otherwise (#78-D3)
with open("GOOD-MORNING.md", encoding="utf-8") as f:
    gm = f.read()
m = re.search(r"^\s*>?\s*#{1,6}\s*★\s*LATEST\s*—\s*(\d{4}-\d{2}-\d{2}).*?\*\*#(\d+)\*\*.*$",
              gm, re.M)
if not m:
    sys.exit("T3: no `> ## ★ LATEST — <date> (... **#N** ...)` banner heading found in "
             "GOOD-MORNING.md — cannot derive the commit headline.")
date, n, line = m.group(1), m.group(2), m.group(0)

# Primary parse: the parenthetical's content AFTER ITS OWN first " — ", skipping the role
# clause to reach the summary glyphs. The parenthetical is the outermost "(...)" on the line —
# first "(" to the LAST ")" at line-end — so nested parens inside the summary (e.g. "(banners
# 2/2)") are swallowed whole, not mistaken for the close.
after, fallback_note = None, None
paren_m = re.search(r"\((.*)\)\s*$", line)
if paren_m:
    parts = paren_m.group(1).split(" — ", 1)
    if len(parts) == 2 and parts[1].strip():
        after = parts[1].strip()
if after is None:
    # FALLBACK — cosmetics must never block a commit. The primary parse found no " — " of its
    # own inside the parenthetical (an unusual or malformed heading); fall back to the reading
    # this block used before the #77 refinement: everything after the heading's OWN first
    # em-dash (the LATEST—date separator). Still readable, just carries the role clause as noise.
    after = line.split("—", 1)[1].strip()
    fallback_note = ("— T3 NOTE: primary headline parse (role-clause skip) found no ' — ' of "
                     "its own inside the ★ LATEST parenthetical — fell back to the first-em-dash "
                     "reading. Heading: " + line.strip()[:200])

# #78-D3: a NON-wrap commit derives its headline from the PRIOR session's banner — prefix it
# "after " so git log never attributes a mid-session commit to that session. Wrap = unprefixed.
prefix = "" if wrap == "1" else "after "
headline = f"{prefix}#{n} {date} — {after}"
if len(headline) > 120:
    headline = headline[:117] + "…"
with open(msgfile, encoding="utf-8") as f:
    body_lines = f.read().splitlines()
with open(msgfile, "w", encoding="utf-8") as f:
    f.write("\n".join([headline] + body_lines[1:]) + "\n")
if fallback_note:
    print(fallback_note)
print(f"— T3 headline: {headline[:100]}{'…' if len(headline) > 100 else ''}")
PYEOF

# clear · stage · clear · commit · clear
clear_locks
find .git -name '*.lock' | grep -q . && fail "lock survived the mv-aside — do NOT stage; investigate"

git add -A 2>/dev/null
git diff --cached --name-only | sed 's/^/  staged: /'
git diff --cached --quiet && fail "nothing staged — empty commit refused"

clear_locks

BEFORE=$(git rev-parse HEAD)
git -c user.name="Claude" -c user.email="claude@anthropic.com" commit -F "$MSGFILE" 2>&1 |
  grep -v 'unable to unlink' || true
AFTER=$(git rev-parse HEAD)
[ "$BEFORE" != "$AFTER" ] || fail "HEAD did not advance — commit did not land"
echo "— committed: $(git log --oneline -1)"
git log -1 --format=%s | head -1 | grep -qF "$(head -1 "$MSGFILE" | cut -c1-40)" ||
  echo "⚠ HEAD message does not match msgfile head — CHECK for the stale-msgfile trap"

# last action: clear the lock git just respawned; no git command after this
clear_locks
echo "✓ done — locks clear, safe for Dave to push via GitHub Desktop"
