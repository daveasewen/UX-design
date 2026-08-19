#!/usr/bin/env bash
# _git_commit.sh — the sandbox commit dance, mechanised.
# provenance: lane session 2026-07-26 (dream-pass P2, Dave ruled accept-enact-now) · status: ruled
#
# WHY: 5 of 7 commit-running sessions (3 of 5 at ruling; #36 + #41 since) reconstructed the clear·stage·clear·commit·clear sequence
# from memory under wrap-time heat and hit the lock failure first (dream-pass P2 evidence).
# Per feedback-gate-dont-patch: make the condition mechanical, not another prose reminder.
# The sandbox delete-guard means locks can only be MOVED (mv), never rm'd — see the runbook.
#
# USAGE:  bash knowledge/_git_commit.sh --reconciled <msgfile> <path> [<path> ...]
#   <msgfile>      commit message file — UNIQUE name, in a session-owned dir (outputs/), never /tmp
#   <path>...      THE PATHS TO STAGE, named explicitly. Required.
#   --reconciled   you have run `git status --short` and can name WHY every dirty path exists
#                  (runbook step 0.5 — the script cannot do this judgment for you)
#   --all-dirty    escape hatch: stage every dirty path, each one ECHOED first. Use only when the
#                  reconciliation genuinely covered all of them; it is never the default.
# The script REFUSES to stage while any .git/*.lock exists, and never runs rm inside .git.
#
# ⚠ `git add -A` RETIRED — ruled Dave 2026-08-02 (dream pass 4, P5 "ACCEPTED, option (a)"), enacted
# #128. `--reconciled` asserted a judgment the staging call then ignored: `add -A` swept whatever
# happened to be dirty, including another worker's uncorrected draft (#70). The flag now means what
# it says — you name the paths, and anything you did not name cannot ride along. The escape hatch
# exists because refusing a legal intention with no legal form is how a gate gets worked around
# rather than obeyed; it stages nothing silently.

set -u
cd "$(dirname "$0")/.." || exit 1

RECONCILED=0

# ── W-22 (dream pass 6 P2, pass-8 datapoint ee4): THE INSTRUMENTATION APPENDS ARE DECLARED ────
# The three tracked files our own verification instruments APPEND to while they verify. They are
# dirty-at-baseline for a reason that is not a worker's uncommitted draft, and until #188 the only
# machinery that knew this was the ONE s137-D1 exclusion — the other two arrived at a push refusal
# as anonymous dirt, indistinguishable from someone's half-finished edit.
#
# ⛔ THIS IS A DECLARATION, NOT AN EXCLUSION. `PUSH_DIRT`'s exclude list is UNCHANGED and still
# names exactly one path in full: s137-D1 says "do NOT generalise this to a pattern or a second
# file", and widening it here would be a sub ruling Dave's open policy question. Whether the other
# two should also be excluded, committed on the spot, or moved out of the tree is ⬛ DAVE'S — pass
# 6 P2 is FLOATED, not ruled. What machinery can honestly do without his word is say WHICH dirt is
# instrument-written and WHICH instrument wrote it, so the refusal is diagnostic
# [[refusal-names-the-first-obstacle]] instead of a heap of paths.
INSTRUMENTATION_PATHS=(
  "notes/_REHEARSAL-LOG.jsonl|_capture_gate.py --wrap / --rehearse, _checkin.py (rehearsal rows)|EXCLUDED from the push gate by s137-D1"
  "knowledge/_graph-mark-observations.jsonl|the graph mark observers|NOT excluded — its POLICY is ⬛ DAVE'S, unruled (dream pass 6 P2)"
  "notes/_dream/_GRADE-DECISIONS.jsonl|_checkin.py B3 grade alerts / _gardener.py --grade-decision|NOT excluded — its POLICY is ⬛ DAVE'S, unruled (dream pass 6 P2)"
)

declare_instrumentation_dirt() {
  # $1 = a `git status --short` blob (may be empty). Prints a DECLARED block naming any of the
  # three instrumentation appends inside it. Emits nothing when none of them are dirty.
  local blob="${1-}" hit=0 rec p writer note
  for rec in "${INSTRUMENTATION_PATHS[@]}"; do
    p="${rec%%|*}"; writer="${rec#*|}"; note="${writer#*|}"; writer="${writer%%|*}"
    case "$blob" in
      *"$p"*)
        [ "$hit" -eq 0 ] && echo "— DECLARED: instrumentation appends among the dirty paths (W-22; dream pass 6 P2 is FLOATED, not ruled):"
        hit=1
        echo "    $p"
        echo "      written by: $writer"
        echo "      status:     $note"
        ;;
    esac
  done
  [ "$hit" -eq 1 ] && echo "  ⇒ this dirt is machine-written, not an uncommitted draft. ⛔ The POLICY (exclude / commit / relocate) is DAVE'S; this line only DECLARES it."
  return 0
}

# `bash knowledge/_git_commit.sh --declare-dirt` — the declaration's OWN consumer, read-only:
# no staging, no commit, no push, no writes [[instrument-without-a-consumer]]. Exit 0 always;
# it reports, it does not gate.
if [ "${1-}" = "--declare-dirt" ]; then
  DIRT=$(git status --short -- .)
  if [ -z "$DIRT" ]; then
    echo "— tree clean: no instrumentation dirt to declare."
  else
    echo "— dirty paths:"; echo "$DIRT"
    declare_instrumentation_dirt "$DIRT"
  fi
  exit 0
fi

# ── PUSH MODE (s133-D2, Dave: "I dont mind if its reasonable gated" → "okay do it") ──────────
# `bash knowledge/_git_commit.sh --push` — the ONLY push path. Fires ONLY on Dave's explicit
# in-session word (the caller's attestation, same contract as --reconciled). Gates, each a refusal:
# master only · fast-forward only (no force flag EXISTS here) · clean tree · credential present ·
# remote head == local head verified AFTER. Supersedes git-push-method BY ADDITION: Desktop remains.
if [ "$1" = "--push" ]; then
  BR=$(git rev-parse --abbrev-ref HEAD)
  [ "$BR" = "master" ] || { echo "✗ push refused: branch is '$BR', not master (s133-D2)"; exit 1; }
  # s137-D1 (Dave, #137): ONE named exclusion — `notes/_REHEARSAL-LOG.jsonl` is the one tracked file the
  # verification instruments themselves write (`_capture_gate.py --wrap`, `_checkin.py`), so verifying a
  # commit AFTER making it dirtied the tree and refused the very push s133-D2 exists to allow (dream pass 6
  # P2; 9 sessions of declared instances, priced at #125, homed nowhere until #137). The path is named in
  # full so the exclusion CANNOT silently widen — do NOT generalise this to a pattern or a second file.
  PUSH_DIRT=$(git status --short -- . ':(exclude)notes/_REHEARSAL-LOG.jsonl')
  if [ -n "$PUSH_DIRT" ]; then
    echo "✗ push refused: tree not clean — commit first (s133-D2; rehearsal log excluded per s137-D1). Dirty paths:"
    echo "$PUSH_DIRT"
    declare_instrumentation_dirt "$PUSH_DIRT"
    exit 1
  fi
  git config remote.origin.url | grep -q "@github.com" || { echo "✗ push refused: no credential in remote URL. Dave: fine-grained PAT (this repo, Contents r/w, 90d) — ⛔ do NOT paste it into chat; run this yourself in a terminal: git config remote.origin.url https://<TOKEN>@github.com/daveasewen/UX-design.git   (W-24 / dream pass 6 P4: the credential never transits the chat; the gate behaves identically. Expiry ~2026-11-06 for the token minted 2026-08-08 — if that date has passed, re-issue rather than re-read this line. ⛔ the token's SCOPE is Dave's security call, unproposed.)"; exit 1; }
  LOCAL=$(git rev-parse HEAD)
  git push origin master 2>&1 | grep -v "^remote:" || true
  REMOTE=$(git ls-remote origin refs/heads/master | cut -f1)
  [ "$LOCAL" = "$REMOTE" ] || { echo "✗ push VERIFY FAILED: local $LOCAL != remote $REMOTE — investigate, do not retry blind"; exit 1; }
  echo "✅ pushed and VERIFIED: remote master == local $LOCAL"
  for L in $(find .git -name '*.lock' 2>/dev/null); do mv "$L" _to_delete/_stale_locks/$(basename $L).$(date +%s%N) 2>/dev/null || rm -f "$L"; done
  exit 0
fi

WRAP=0
ALLDIRTY=0
MSGFILE=""
PATHS=()
for a in "$@"; do
  case "$a" in
    --reconciled) RECONCILED=1 ;;
    --wrap) WRAP=1 ;;
    --all-dirty) ALLDIRTY=1 ;;
    --session=*) ;;
    *) if [ -z "$MSGFILE" ]; then MSGFILE="$a"; else PATHS+=("$a"); fi ;;
  esac
done

clear_locks() {
  mkdir -p _to_delete/_stale_locks
  for L in $(find .git -name '*.lock' 2>/dev/null); do
    mv "$L" "_to_delete/_stale_locks/$(basename "$L").$(date +%s%N)" || true
  done
}

fail() { echo "✗ $1" >&2; exit 1; }

# ── T3 PREFIX COUNTER — ONE IMPLEMENTATION, THREE CONSUMERS (#208) ───────────────────────────
# The prefix T3 generates has TWO legal shapes: `after #<n> <date> — ` (non-wrap) and
# `#<n> <date> — ` (wrap). Counting them is the primitive under the msgfile-reuse gate below,
# the post-commit subject assert, and `--selftest`. It exists ONCE because the #170 gate matched
# only the `after ` shape: feeding a WRAP msgfile (line 1 = `#207 2026-08-18 — …`) into a
# NON-WRAP run walked straight past it and produced `after #208 2026-08-19 — #207 2026-08-18 — …`.
# That is 1 of the 8 documented doubled/tripled subjects, and it is why this counts BOTH shapes.
# ⚠ `— ` here is U+2014 + space, the same literal T3 emits; a hyphen is not this prefix.
# ⛔ #208 NEW-2, FIXED THE SAME SESSION IT WAS FOUND — this counter was `re.findall`, i.e.
# UNANCHORED, and it refused an HONEST subject that QUOTED a prior one mid-line ("restores the
# `after #207 … — x` subject"). The #170 gate this widens has always been ANCHORED (`re.match`,
# :487 in the T3 block below). An unanchored counter is not a wider gate, it is a DIFFERENT one:
# it counts MENTIONS, and a mention is not a prefix. It now counts the STACK — how many prefixes
# sit consecutively AT THE START, which is the only place stacking can happen, because T3 always
# prepends. `after #208 … — after #207 … — x` still counts 2; the honest quote counts 1.
# ⚠ `— ` here is U+2014 + space, the same literal T3 emits; a hyphen is not this prefix.
prefix_count() {
  python3 - "$1" <<'PY'
import re, sys
s = sys.argv[1]
pat = re.compile(r"^(?:after )?#\d+ \d{4}-\d{2}-\d{2} — ")
n = 0
while True:
    m = pat.match(s)
    if not m:
        break
    n += 1
    s = s[m.end():]
print(n)
PY
}

# ── #208 SELFTEST — the msgfile-prefix gate, BOTH DIRECTIONS, no repo state touched ──────────
# `bash knowledge/_git_commit.sh --selftest`. Read-only: no staging, no commit, no push, no
# writes [[instrument-without-a-consumer]]. Every arm names the class it bites.
if [ "${1-}" = "--selftest" ]; then
  SF_FAILS=0
  bite() { # bite <name> <expected> <actual>
    if [ "$2" = "$3" ]; then echo "  [OK]   $1 (expected $2)"; else
      echo "  [FAIL] $1 — expected $2, got $3"; SF_FAILS=$((SF_FAILS + 1)); fi
  }
  echo "— #208 msgfile-prefix gate selftest"
  # FIRES: every shape a reused msgfile actually arrives in
  bite "non-wrap prefix (the #170 shape) is seen"       1 "$(prefix_count 'after #207 2026-08-18 — wave1 receipts')"
  bite "WRAP prefix (the shape #170 MISSED) is seen"    1 "$(prefix_count '#207 2026-08-18 — wrap: session close')"
  bite "doubled non-wrap prefix counts 2"               2 "$(prefix_count 'after #208 2026-08-19 — after #207 2026-08-18 — x')"
  bite "wrap-into-non-wrap stack counts 2 (the hole)"   2 "$(prefix_count 'after #208 2026-08-19 — #207 2026-08-18 — x')"
  bite "tripled counts 3"                               3 "$(prefix_count 'after #1 2026-01-01 — after #1 2026-01-01 — after #1 2026-01-01 — x')"
  # STAYS SILENT: near misses that a looser matcher would eat
  bite "a fresh subject carries no prefix"              0 "$(prefix_count 'wave1: make CI legible')"
  bite "session ref with no date is not a prefix"       0 "$(prefix_count '#208 — fix the gates')"
  bite "date with no session ref is not a prefix"       0 "$(prefix_count '2026-08-19 — fix the gates')"
  bite "hyphen is not the em-dash separator"            0 "$(prefix_count 'after #207 2026-08-18 - wave1 receipts')"
  bite "prose mentioning a session mid-line"            0 "$(prefix_count 'fixes the class #205 found')"
  # ⛔ NEW-2 (#208 verifier): the arms above never carried a DATE mid-line, so the false positive
  # they were meant to fence never got exercised. These two are that case, both directions.
  bite "honest subject QUOTING a prior prefix mid-line" 1 "$(prefix_count 'after #208 2026-08-19 — restores the after #207 2026-08-18 — x subject')"
  bite "a quoted prefix with no prefix of its own"      0 "$(prefix_count 'restores the after #207 2026-08-18 — x subject')"
  bite "a prefix after a leading word is not a stack"   0 "$(prefix_count 'see after #207 2026-08-18 — x')"
  # the ACK hatch exists and is spelled the same way as its two neighbours (declared passes,
  # silent fails). A hatch nothing asserts is a hatch that can be deleted by accident.
  if grep -q 'PREFIX_ACK' "$0"; then echo "  [OK]   PREFIX_ACK hatch present (declared passes, silent fails)";
  else echo "  [FAIL] PREFIX_ACK hatch absent — the door gate has no legal form for a declared exception"; SF_FAILS=$((SF_FAILS + 1)); fi
  if [ "$SF_FAILS" -ne 0 ]; then
    echo "✗ selftest FAILED — $SF_FAILS bite(s)"; exit 1
  fi
  echo "✓ selftest OK — 14 bites: 6 fire, 7 stay silent, 1 hatch present"
  exit 0
fi

[ -n "$MSGFILE" ] || fail "no msgfile given. Usage: _git_commit.sh --reconciled <msgfile>"
[ -s "$MSGFILE" ] || fail "msgfile '$MSGFILE' missing or empty (stale-msgfile trap — see runbook gotchas)"
echo "— msgfile head: $(head -1 "$MSGFILE")"

# ── REUSED-MSGFILE GATE, AT THE DOOR (#208; widens the #170 gate) ────────────────────────────
# The #170 gate lives INSIDE T3's non-wrap branch and matches only `after #N <date> — `. Two
# holes, both documented in the 8-instance count: (1) a WRAP msgfile's line 1 is `#N <date> — `,
# which that regex does not see, so reusing a wrap msgfile on a non-wrap run stacked a second
# prefix; (2) the wrap branch never asked the question at all, and silently DROPS line 1 into
# the void (it takes the body from line 2 onward), so a reused wrap msgfile lost its first line
# with no word said. Asking HERE — before any gate that can refuse, and long before T3 writes
# anything — makes the answer independent of which branch T3 will take.
# ⛔ The #170 in-branch check is LEFT IN PLACE, unchanged. Two gates on one class is not
# duplication when the inner one is the one that has been proven to bite.
# ⛔ #208 NEW-2: the counter is ANCHORED (see prefix_count above) — it asks "does line 1 START
# with a stacked prefix", not "does the word appear somewhere". An honest subject that QUOTES a
# prior one is no longer refused. Declared-gap hatch: PREFIX_ACK="<real reason>" passes it
# DECLARED, spelled exactly like its neighbours DOC_ROW_ACK / SHOWROOM_ACK / SESSION_ACK
# (declared passes, silent fails) — a gate with no legal exception invites the workaround.
MSG_L1=$(head -1 "$MSGFILE")
if [ -n "${PREFIX_ACK:-}" ]; then
  echo "— reused-msgfile gate: DECLARED GAP — $PREFIX_ACK"
elif [ "$(prefix_count "$MSG_L1")" -gt 0 ]; then
  fail "REUSED-MSGFILE GATE (#208, widening #170): line 1 of '$MSGFILE' already carries a T3 prefix — \"$(printf '%s' "$MSG_L1" | cut -c1-80)\". This file has been through a commit run before, so this run would stack a second prefix (the doubled-subject class, 8 documented instances). REMEDY: write a FRESH msgfile with a FRESH name — one printf per invocation, never a reused path:
    printf '%s\\n' '<your one-line summary>' '' '<body…>' > outputs/_msg-<session>-<slug>-\$(date +%s).txt
  Nothing has been staged, and this msgfile has not been modified."
fi
echo "— msgfile line 1 carries no T3 prefix (#208 reuse gate passed)"

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

# doc-row gate — W-20 (#188), the forgotten-document class (#185): a brief-class document with no
# store row is invisible to every carry. The commit is the seam where the defect turns DURABLE,
# so the gate runs here [check-after-its-own-remedy]. Fix = one _state.add() row through the
# store's own writer. Declared-gap hatch: DOC_ROW_ACK="<real reason>" passes it DECLARED
# (declared passes, silent fails). Wired by the conductor at #188; Dave may veto the blocking.
if [ -z "${DOC_ROW_ACK:-}" ]; then
  python3 knowledge/_gate_doc_rows.py ||
    fail "doc-row gate REFUSED — an in-scope document has no store row (list printed above). Add the row via _state.add(), or re-run with DOC_ROW_ACK=\"<real reason>\" to pass it as a DECLARED gap. Nothing has been staged."
  echo "— doc rows present (_gate_doc_rows.py passed)"
else
  echo "— doc-row gate: DECLARED GAP — $DOC_ROW_ACK"
fi

# showroom sync gate — s191-D1 (#191, Dave: "yes"). A ruling's deletion (s182-D2) survived four
# sessions on the generated showroom — Dave's review surface — because nothing at the commit seam
# checked generated-vs-canon sync. The commit is where staleness turns durable, so the check runs
# here BLOCKING. Declared-gap hatch mirrors the doc-row gate (declared passes, silent fails).
if [ -z "${SHOWROOM_ACK:-}" ]; then
  python3 knowledge/gen_showroom.py --check ||
    fail "showroom sync gate REFUSED (s191-D1) — generated showroom out of sync with canon (list printed above). Run: python3 knowledge/gen_showroom.py — or re-run with SHOWROOM_ACK=\"<real reason>\" to pass it as a DECLARED gap. Nothing has been staged."
  echo "— showroom in sync (gen_showroom --check passed, s191-D1)"
else
  echo "— showroom sync gate: DECLARED GAP — $SHOWROOM_ACK"
fi

# ── MENTION-MAP FRESHNESS GATE — the [110] re-stale CLASS, 3rd recurrence (#208) ──────────────
# ⛔ THE CLASS, NOT THE INSTANCE. `knowledge/_graph-mention-map.json` is derived from
# `_decision-graph.json` + `_memento-index.json`, which are themselves derived from the corpus.
# So ANY doc/generator change re-stales it, and CI step [110] (`_build_graph_mention_map.py
# --check`) goes red — in the SURVEY step, which asks the committed tree BEFORE any rebuild, so
# the later "Knowledge build" step regenerating it cannot rescue the read. It was repaired
# targeted three times (#205 pitfall (d); d07e85c / 49ba965 → 5a716a6) because nothing at the
# COMMIT SEAM — the one place staleness turns durable — ever asked the question.
#
# OWNED REGIONS, WRITTEN DOWN BEFORE RUNNING THE GENERATOR [[do-not-rule-list-cannot-fence-a-generator]]:
#   `_build_graph_mention_map.py` writes EXACTLY ONE path — `knowledge/_graph-mention-map.json`,
#   whole-file overwrite (`OUT_PATH`, the file's only `open(..., "w")` outside its selftest
#   tempfile). It READS `_decision-graph.json` and `_memento-index.json` and writes neither.
#   Probe: `grep -n '"w"' knowledge/_build_graph_mention_map.py` → the selftest tempfile and
#   OUT_PATH, nothing else. That single-owner, single-file property is why regenerating here is
#   safe; it is NOT a licence to run any other generator at this seam.
#
# ⛔ AND IT DOES NOT STAGE WHAT YOU DID NOT NAME. Regenerating is safe; staging silently is not
# (P5, ruled Dave 2026-08-02 — `git add -A` retired). So a stale map is REGENERATED (announced,
# one path named) and then REFUSED, with the path to add to your `--reconciled` list. One
# re-run, and the class cannot reach a commit. Declared-gap hatch mirrors its two neighbours.
if [ -z "${MENTION_MAP_ACK:-}" ]; then
  if python3 knowledge/_build_graph_mention_map.py --check >/dev/null 2>&1; then
    echo "— mention map fresh (_build_graph_mention_map.py --check passed, #208 [110] class gate)"
  else
    echo "— mention map STALE — regenerating the ONE file this generator owns:"
    python3 knowledge/_build_graph_mention_map.py ||
      fail "the mention-map generator itself REFUSED (its named cause is printed above; it is the authority on it — this script does not second-guess it). Nothing has been staged."
    python3 knowledge/_build_graph_mention_map.py --check ||
      fail "mention map STILL stale after a targeted regeneration — that is nondeterminism in the generator or a mid-flight input, NOT the ordinary re-stale class. Do not re-run blind; read _build_graph_mention_map.py. Nothing has been staged."
    fail "MENTION-MAP GATE (#208, the [110] re-stale class, 3rd recurrence): the map was stale and has been REGENERATED just now — knowledge/_graph-mention-map.json. It is NOT staged, because this script never stages a path you did not name (P5, ruled 2026-08-02). Re-run this exact command with that path appended to your list. Nothing has been staged by this run."
  fi
else
  echo "— mention-map gate: DECLARED GAP — $MENTION_MAP_ACK"
fi

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
# ⛔ s130-D3 (Dave, #130) — GENERATE, NEVER INHERIT. The #128 defect: a NON-wrap commit read
# whatever banner was ON DISK, so a session that wrote no banner inherited the PRIOR session's
# subject ("after #127 …" on #128's commits), and the subject assert compared the REWRITTEN
# file, so it was true and useless. Remedy, per Dave's ruling:
#   - NON-wrap: the banner is NEVER read. The subject is generated from current-session
#     sources only: the SESSION_N witness (verified by _session.py at the seam above), today's
#     `date`, and the msgfile's OWN first line, written this session by its author. If
#     SESSION_N is absent there is no current-session source and T3 REFUSES loudly —
#     inheriting a stale banner is no longer a reachable behaviour.
#   - --wrap: banner derivation stands (the wrap writes its banner first), but T3 now ASSERTS
#     the banner's #N equals the declared SESSION_N and REFUSES on mismatch — the banner is a
#     VERIFIED current-session source, not an assumed one.
# ⛔ #171 — T3's generated headline is CAPTURED INTO A SHELL VARIABLE here and the post-commit
# subject assert compares the COMMITTED subject against THAT variable. It used to compare the
# committed subject against the msgfile's first line — the very line T3 rewrites four lines
# below — so it compared a value to itself and could not fail. DRIVEN #171: with a simulated
# prefix-stacking write-back, a doubled subject landed and the assert still printed
# "— subject asserted identical to msgfile line 1" and exited 0. The msgfile is now a
# DIAGNOSTIC in that failure text, never the authority.
# ⛔ #208 — T3 NO LONGER WRITES TO THE CALLER'S MSGFILE. It renders to a SEPARATE file and the
# commit is made from that. Before this, T3 rewrote `$MSGFILE` in place and then five more
# refusals could still fire (lock survived · no paths named · nothing staged · empty commit ·
# a git error) — every one of which left the caller holding a msgfile that had already grown a
# prefix. The caller then fixed the named problem, re-ran the SAME file, and stacked a second
# prefix: that is the mechanism behind the 8 doubled/tripled subjects, and no gate could undo
# it because the mutation happened before the refusal. A render file makes the msgfile
# READ-ONLY input for the whole run, so a refusal costs nothing and a retry is safe.
# ⚠ The render file is DERIVED and disposable: it sits beside the msgfile (session-owned dir,
# gitignored `outputs/`), is overwritten every run, and is never staged.
RENDERED="${MSGFILE}.t3-rendered"
T3_OUT=$(python3 - "$MSGFILE" "$WRAP" "${SESSION_N:-}" "$(date +%F)" "$RENDERED" 2>&1 <<'PYEOF'
import re, sys
msgfile = sys.argv[1]
wrap = sys.argv[2]  # "1" on --wrap commits, "0" otherwise (#78-D3)
session_n = sys.argv[3].strip()  # boot-witness-verified by _session.py above (s130-D3)
today = sys.argv[4].strip()      # from `date`, never from belief (T-D12)
fallback_note = None
if wrap == "1":
    # --wrap: the banner was written THIS session by the wrap itself; derive from it as before,
    # but VERIFY that claim against the session witness (s130-D3) instead of assuming it.
    with open("GOOD-MORNING.md", encoding="utf-8") as f:
        gm = f.read()
    m = re.search(r"^\s*>?\s*#{1,6}\s*★\s*LATEST\s*—\s*(\d{4}-\d{2}-\d{2}).*?\*\*#(\d+)\*\*.*$",
                  gm, re.M)
    if not m:
        sys.exit("T3: no `> ## ★ LATEST — <date> (... **#N** ...)` banner heading found in "
                 "GOOD-MORNING.md — cannot derive the commit headline.")
    date, n, line = m.group(1), m.group(2), m.group(0)
    # s130-D3 REFUSAL: a wrap subject certifies the declared session or nobody. SESSION_N is
    # mandatory on --wrap (enforced at the seam above), so a mismatch here means the banner on
    # disk is NOT this session's — committing would certify the wrong session (#128's defect).
    if not session_n:
        sys.exit("T3 REFUSES (s130-D3): --wrap with no SESSION_N reached T3 — the session seam "
                 "above should have blocked this; nothing to verify the banner against.")
    if n != session_n:
        sys.exit(f"T3 REFUSES (s130-D3): GOOD-MORNING.md's ★ LATEST banner says #{n} but the "
                 f"declared session is #{session_n} — the on-disk banner is another session's "
                 "and a subject derived from it certifies the WRONG session (the #128 defect). "
                 "Write this session's banner (ritual step 2), then re-run.")
    # Primary parse: the parenthetical's content AFTER ITS OWN first " — ", skipping the role
    # clause to reach the summary glyphs. The parenthetical is the outermost "(...)" on the
    # line — first "(" to the LAST ")" at line-end — so nested parens inside the summary
    # (e.g. "(banners 2/2)") are swallowed whole, not mistaken for the close.
    after = None
    paren_m = re.search(r"\((.*)\)\s*$", line)
    if paren_m:
        parts = paren_m.group(1).split(" — ", 1)
        if len(parts) == 2 and parts[1].strip():
            after = parts[1].strip()
    if after is None:
        # FALLBACK — cosmetics must never block a commit. The primary parse found no " — " of
        # its own inside the parenthetical; fall back to the pre-#77 first-em-dash reading.
        after = line.split("—", 1)[1].strip()
        fallback_note = ("— T3 NOTE: primary headline parse (role-clause skip) found no ' — ' "
                         "of its own inside the ★ LATEST parenthetical — fell back to the "
                         "first-em-dash reading. Heading: " + line.strip()[:200])
    headline = f"#{n} {date} — {after}"
else:
    # NON-wrap (s130-D3): the banner is NEVER read. Generate from current-session sources —
    # the verified SESSION_N witness, today's `date`, and the msgfile's own first line. This
    # replaces #78-D3's "after <banner>" inheritance, whose 'after ' prefix survives with a
    # meaning that is now true by construction: after #<THIS session>, not after whatever
    # session last wrote a banner.
    if not session_n:
        sys.exit("T3 REFUSES (s130-D3): non-wrap commit with no SESSION_N — there is no "
                 "current-session source to generate a subject from, and inheriting the "
                 "on-disk ★ LATEST banner is the #128 wrong-subject defect. Re-run as "
                 "SESSION_N=<n> bash knowledge/_git_commit.sh --reconciled <msgfile>.")
    with open(msgfile, encoding="utf-8") as f:
        first = f.readline().strip()
    if not first:
        sys.exit("T3 REFUSES (s130-D3): the msgfile's first line is empty — a non-wrap "
                 "subject is generated from the msgfile's own first line, written this "
                 "session; there is nothing to generate from.")
    # #170 — REUSED-MSGFILE GATE (the x12 prefix-stacking class, mechanism identified #170):
    # T3 WRITES the generated headline back into the msgfile below, so feeding the same file
    # through a second invocation stacks a second prefix ("after #N date — after #N date — …").
    # Every doubled/tripled subject since #157 was THIS, not the generator misfiring. Gate the
    # PRESENCE at the seam where it turns durable: a msgfile whose first line already carries
    # the prefix has been through T3 once and is stale by definition — fresh printf per
    # invocation (memory git-push-method, tripled #157, amended; recurred #164, #169, #170).
    if re.match(r"after #\d+ \d{4}-\d{2}-\d{2} — ", first):
        sys.exit("T3 REFUSES (#170 reused-msgfile gate): the msgfile's first line already "
                 "carries an 'after #N <date> — ' prefix, so this file has been through T3 "
                 "before — invoking again would stack the prefix (the doubled-subject class, "
                 "x12 instances). Write a FRESH msgfile (fresh printf per invocation) and re-run. "
                 "Nothing has been staged.")
    headline = f"after #{session_n} {today} — {first}"
if len(headline) > 120:
    headline = headline[:117] + "…"
with open(msgfile, encoding="utf-8") as f:
    body_lines = f.read().splitlines()
body = body_lines[1:]
# #124 — SUBJECT-FOLD GATE. git's %s folds ALL consecutive non-blank lines into the subject:
# commit 0eacf2d (a JSONL body with no separator) shipped an ~83,000-char subject that broke
# every git-log consumer at the next boot. A blank line after the headline is therefore
# STRUCTURAL, not cosmetic — insert it whenever the body doesn't already start blank.
if body and body[0].strip():
    body = [""] + body
# #208: the RENDER file, never `msgfile` — see the shell comment above this heredoc.
with open(sys.argv[5], "w", encoding="utf-8") as f:
    f.write("\n".join([headline] + body) + "\n")
if fallback_note:
    print(fallback_note)
print(f"— T3 headline: {headline[:100]}{'…' if len(headline) > 100 else ''}")
# #171 — the machine line the shell captures. This, not the rewritten msgfile, is what the
# post-commit subject assert compares git's %s against.
print("T3-SUBJECT\t" + headline)
PYEOF
) || { printf '%s\n' "$T3_OUT" >&2; fail "T3 headline generation REFUSED (reason printed above) — s130-D3: a subject is generated from a current-session source or not at all; a stale on-disk banner is never inherited. Non-wrap commits require SESSION_N=<n>. Nothing has been staged."; }
# replay T3's human output (notes + headline), then lift the machine line into memory
printf '%s\n' "$T3_OUT" | grep -v '^T3-SUBJECT' || true
GEN_SUBJ=$(printf '%s\n' "$T3_OUT" | sed -n 's/^T3-SUBJECT\t//p')
[ -n "$GEN_SUBJ" ] || fail "T3 exited 0 but emitted no T3-SUBJECT line — the generated headline was not captured, so the post-commit subject assert would have nothing to compare against (#171). Nothing has been staged."

# clear · stage · clear · commit · clear
clear_locks
find .git -name '*.lock' | grep -q . && fail "lock survived the mv-aside — do NOT stage; investigate"

# EXPLICIT-PATH STAGING — P5 option (a), enacted #128. `git add -A` is gone; the paths come from
# the reconciliation, not from whatever the tree happens to be carrying.
if [ "$ALLDIRTY" -eq 1 ]; then
  echo "— --all-dirty: staging every dirty path, named:"
  git status --porcelain | sed 's/^/  dirty: /'
  while IFS= read -r _p; do [ -n "$_p" ] && PATHS+=("$_p"); done < <(git status --porcelain | cut -c4-)
fi
if [ "${#PATHS[@]}" -eq 0 ]; then
  echo '✗ refusing to stage: no paths given. --reconciled means you can name WHY every dirty path'
  echo '  exists — so name the ones this commit is for (P5, ruled 2026-08-02: git add -A retired).'
  echo "  Re-run as: bash knowledge/_git_commit.sh --reconciled <msgfile> <path> [<path> ...]"
  echo "  or, if the reconciliation really covered all of them, add --all-dirty. Dirty paths now:"
  git status --short
  exit 1
fi
for _p in "${PATHS[@]}"; do
  git add -- "$_p" 2>/dev/null || fail "could not stage '$_p' — named in the reconciliation but git refused it"
done
git diff --cached --name-only | sed 's/^/  staged: /'
UNSTAGED_DIRTY=$(git status --porcelain | grep -c '^.[MD?]' || true)
[ "$UNSTAGED_DIRTY" -eq 0 ] ||
  echo "⚠ $UNSTAGED_DIRTY dirty path(s) NOT staged — deliberate under explicit-path staging; they stay for the next commit"
git diff --cached --quiet && fail "nothing staged — empty commit refused"

# ── MENTION-MAP GATE, SECOND HALF: REGENERATED-BUT-NOT-STAGED (#208) ──────────────────────────
# The freshness gate above proves the map on DISK is current. This proves the map going into the
# COMMIT is. Under explicit-path staging those are different claims, and the difference is the
# hole the three targeted repairs kept falling through: regenerate the map, commit without
# naming it, and CI's survey reads the OLD blob against the NEW corpus — red again, with a clean
# local `--check`. Asked after staging because that is when the answer exists.
MAP_PATH="knowledge/_graph-mention-map.json"
if ! git diff --quiet -- "$MAP_PATH" 2>/dev/null; then
  fail "MENTION-MAP GATE (#208, second half): '$MAP_PATH' differs from HEAD and is NOT staged — the commit would carry the OLD map against a NEW corpus, which is exactly what CI's survey step [110] reads (it asks the committed tree BEFORE any rebuild). Append '$MAP_PATH' to your named paths and re-run. Nothing has been committed."
fi
echo "— mention map is either unchanged or staged (#208 [110] second-half assert)"

# ── DOC-ROW GATE, SECOND HALF: THE DOCS OF *THIS* COMMIT (#208) ─────────────────────────────
# The pre-staging run above can only see docs that are ALREADY COMMITTED (its population comes
# from `git log`), so a single-commit session that adds a brief ships it unrowed and the gate
# reports PASS while doing it (#207 postscript). `_gate_doc_rows.py` now ALSO reads
# `git diff --cached --diff-filter=A` — but that set is EMPTY until the staging loop above has
# run, so the answer only exists here. Same DOC_ROW_ACK hatch: declared passes, silent fails.
if [ -z "${DOC_ROW_ACK:-}" ]; then
  python3 knowledge/_gate_doc_rows.py ||
    fail "doc-row gate REFUSED (post-staging) — a document STAGED IN THIS COMMIT has no store row (list printed above). Add the row via _state.add(), or re-run with DOC_ROW_ACK=\"<real reason>\" to pass it DECLARED."
  echo "— doc rows present for this commit's staged adds (_gate_doc_rows.py, post-staging)"
fi

clear_locks

BEFORE=$(git rev-parse HEAD)
# --cleanup=verbatim — enacted #128, ruled the same session it was found. git's `strip` cleanup
# (the default whenever `commit.cleanup=strip` is configured, and the default for editor-supplied
# messages) DELETES every line beginning with '#'. The T3 headline this script generates BEGINS
# WITH '#<session>' on a wrap commit — so the subject line was silently removed and git promoted
# the first body line to %s. MEASURED #128 in a scratch repo, git 2.34.1: with `commit.cleanup=strip`
# the subject of a `#128 … / <blank> / body` msgfile came back as literally `body`; with
# `--cleanup=verbatim`, `#128 …`. Nothing warned. `verbatim` also means the msgfile is committed
# exactly as written — which is the property the assert below relies on.
# #208: `-F "$RENDERED"`, not `-F "$MSGFILE"` — the msgfile is READ-ONLY input for this run.
[ -s "$RENDERED" ] || fail "T3 exited 0 but wrote no render file at '$RENDERED' — the commit message the assert compares against would not exist. Nothing has been committed."
git -c user.name="Claude" -c user.email="claude@anthropic.com" commit --cleanup=verbatim -F "$RENDERED" 2>&1 |
  grep -v 'unable to unlink' || true
AFTER=$(git rev-parse HEAD)
[ "$BEFORE" != "$AFTER" ] || fail "HEAD did not advance — commit did not land"
echo "— committed: $(git log -1 --format='%h %s' | cut -c1-120)"
# #124 subject-fold consumer — the T3 blank-line insert is the remedy; this check sits at the
# seam where a folded subject becomes DURABLE (the commit), so it cannot be blinded by its own
# remedy. 0eacf2d shipped ~83,000 chars as %s and broke every git-log consumer at the next boot.
SUBJ_LEN=$(git log -1 --format=%s | wc -c)
[ "$SUBJ_LEN" -le 200 ] || fail "commit subject is ${SUBJ_LEN} chars (cap 200) — the 0eacf2d subject-fold class: no blank line after the headline, so git folded the body into %s. The commit LANDED; fix the msgfile and amend BEFORE Dave pushes."
# SUBJECT-IDENTITY ASSERT — enacted #128, and it FAILS LOUD. What stood here was a substring
# `grep -qF` on the first 40 chars that only ever printed a warning, so the two ways this seam
# actually breaks both passed it: git's cleanup silently deleting a '#'-leading subject, and the
# stale-msgfile trap. The commit HAS landed by the time this runs — that is the point, this is the
# seam where a wrong subject becomes DURABLE — so the failure text says so and names the remedy.
# ⛔ #171 — THE SUBJECT NOW ASSERTS AGAINST THE GENERATED HEADLINE HELD IN MEMORY ($GEN_SUBJ),
# NEVER against the msgfile T3 rewrote. The old comparison read back the same line T3 had
# written seconds earlier: a value compared to itself, structurally unable to fail. Driven #171
# with a simulated prefix-stacking write-back — the doubled subject landed and this seam
# printed green. $GEN_SUBJ is captured BEFORE staging and is not touched by anything after.
MSG_HEAD=$(head -1 "$MSGFILE")
GIT_SUBJ=$(git log -1 --format=%s)
if [ "$GIT_SUBJ" != "$GEN_SUBJ" ]; then
  echo "✗ SUBJECT MISMATCH — the commit LANDED but git's subject is not the headline T3 generated." >&2
  echo "    T3 generated: $(printf '%s' "$GEN_SUBJ" | cut -c1-160)" >&2
  echo "    git    %s  : $(printf '%s' "$GIT_SUBJ" | cut -c1-160)" >&2
  echo "    msgfile[1]  : $(printf '%s' "$MSG_HEAD" | cut -c1-160)   (diagnostic only — T3 rewrote this file)" >&2
  echo "  Known causes: (a) message cleanup ate a '#'-leading subject — check --cleanup=verbatim" >&2
  echo "  survived, (b) the stale-msgfile trap, (c) something rewrote the msgfile between T3 and" >&2
  echo "  the commit. Fix the msgfile and amend BEFORE Dave pushes." >&2
  clear_locks
  exit 1
fi
echo "— subject asserted identical to the headline T3 generated (in memory, not re-read from the msgfile — #171)"
# ── #208 — EXACTLY-ONE-PREFIX ASSERT, on the COMMITTED subject ────────────────────────────────
# The identity assert above compares the subject to the headline T3 generated. It cannot see a
# prefix that was ALREADY in the generated headline, which is precisely what a reused msgfile
# produces (`after #208 … — after #207 … — x` is a faithful copy of what T3 built). So the
# CLASS gets its own check, on `git log -1 --format=%s` — the artefact a reader actually meets.
# Both refusals are post-commit BY DESIGN: this is the seam where a doubled subject turns
# DURABLE, and the remedy (amend before the push) is only available here.
SUBJ_PREFIXES=$(prefix_count "$GIT_SUBJ")
if [ "$SUBJ_PREFIXES" -ne 1 ]; then
  echo "✗ SUBJECT PREFIX COUNT = $SUBJ_PREFIXES (must be exactly 1) — the doubled-subject class (#208, 8 documented instances)." >&2
  echo "    git %s : $(printf '%s' "$GIT_SUBJ" | cut -c1-160)" >&2
  echo "  0 means T3's prefix never reached the subject (check --cleanup=verbatim survived);" >&2
  echo "  2+ means a msgfile was reused and the prefix stacked. The commit LANDED: fix the" >&2
  echo "  msgfile (FRESH file, fresh printf) and 'git commit --amend -F <fresh>' BEFORE Dave pushes." >&2
  clear_locks
  exit 1
fi
echo "— subject carries exactly ONE T3 prefix (#208 doubled-subject assert)"

# last action: clear the lock git just respawned; no git command after this
clear_locks
echo "✓ done — locks clear, safe for Dave to push via GitHub Desktop"
