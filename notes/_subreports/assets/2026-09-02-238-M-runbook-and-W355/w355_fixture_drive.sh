#!/usr/bin/env bash
# #238 lane M — W-355 FIXTURE DRIVE. Builds a throwaway repo under /dev/shm/w355/ (the ONE place git
# is permitted for this lane), copies the repo's knowledge/_git_commit.sh + the REAL _session.py, and
# drives the deadlock and its declared form. Every arm prints one `ARM … verdict=PASS|FAIL` line.
# Usage: bash w355_fixture_drive.sh <repo root>      (one bash call; /dev/shm is per-call; cleans up)
set -u
REPO="${1:?repo root}"
FX=/dev/shm/w355/repo
rm -rf /dev/shm/w355; mkdir -p "$FX/knowledge" "$FX/pystubs" "$FX/outputs"
cp "$REPO/knowledge/_git_commit.sh" "$FX/knowledge/_git_commit.sh"
cp "$REPO/knowledge/_session.py" "$REPO/knowledge/_helpgate.py" "$FX/knowledge/"
for s in _gen_chain.py _capture_gate.py _build_live_state.py _gate_doc_rows.py gen_showroom.py _build_graph_mention_map.py _gate_scratch_hygiene.py; do
  printf '#!/usr/bin/env python3\nimport sys; print("STUB %s", sys.argv[1:]); sys.exit(0)\n' "$s" > "$FX/knowledge/$s"
done
printf 'class _E:\n    def encode(self, s): return [0]*max(1,len(s)//4)\ndef get_encoding(n): return _E()\n' > "$FX/pystubs/tiktoken.py"
printf '{"fixture": "mention map at HEAD"}\n' > "$FX/knowledge/_graph-mention-map.json"
cat > "$FX/GOOD-MORNING.md" <<'EOF'
> ## ★ LATEST — 2026-09-02 (Wed **#238**, FABLE sub — ✅ **W-355 FIXTURE**)

**TITLE THE NEXT CHAT →** `#239 — next session`
EOF
printf '# _CHAIN.md (fixture) — routes the reader to #239\n' > "$FX/_CHAIN.md"
printf '{"n": 238, "event": "boot", "ts": "2026-09-02T09:00:00"}\n{"n": 238, "event": "wrap", "ts": "2026-09-02T15:00:00"}\n' > "$FX/knowledge/_SESSIONS.jsonl"
# the UNFIXED control: the same script with its two W-355 blocks stripped (marker → first column-0 `fi`)
python3 - "$FX/knowledge/_git_commit.sh" "$FX/knowledge/_git_commit.unfixed.sh" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
marks = ("# ── W-355 DECLARED FORM (1/2)", "# ── W-355 DECLARED FORM (2/2)")
out, skip = [], False
for line in open(src, encoding="utf-8"):
    if line.startswith(marks): skip = True
    if skip:
        if line.rstrip("\n") == "fi": skip = False
        continue
    out.append(line)
s = "".join(out)
assert 'if [ -n "${SESSION_N:-}" ]; then' in s and "SESSION_N_HELD" not in s, "strip went wrong"
open(dst, "w", encoding="utf-8").write(s)
print("— control script written: W-355 blocks stripped, %d → %d lines" % (sum(1 for _ in open(src)), len(out)))
PY
cd "$FX" || exit 1
export HOME="$FX" GIT_CONFIG_NOSYSTEM=1 PYTHONPATH="$FX/pystubs"
git init -q && git config user.name Fixture && git config user.email fixture@test.local
git add -A && git commit -q -m "post-wrap state of #238" && echo "— fixture HEAD: $(git log -1 --format='%h %s')"
printf '# handoff for #239 (fixture)\n' > _HANDOFF-239-x.md
ACK="post-wrap handoff for #239 is the file being committed (W-355 declared form)"
n=0
arm() { # arm <label> <expect RED|GREEN> <needle> <script> [ENV=..]... -- <args...>
  local label="$1" expect="$2" needle="$3" script="$4"; shift 4
  local envs=(); while [ "$1" != "--" ]; do envs+=("$1"); shift; done; shift
  n=$((n+1)); local msg="outputs/msg-$n.txt"
  printf '%s\n\n%s\n' "post-wrap handoff for #239 (arm $n)" "body: $ACK" > "$msg"
  local before; before=$(git rev-parse HEAD)
  local out rc; out=$(env "${envs[@]}" bash "$script" --reconciled "$msg" "$@" 2>&1); rc=$?
  local after; after=$(git rev-parse HEAD)
  local got="GREEN"; [ "$rc" -eq 0 ] || got="RED"
  local hit="no"; printf '%s' "$out" | grep -qF -- "$needle" && hit="yes"
  local verdict="FAIL"; [ "$got" = "$expect" ] && [ "$hit" = "yes" ] && verdict="PASS"
  local moved="held"; [ "$before" != "$after" ] && moved="advanced→$(git log -1 --format=%h)"
  echo "ARM $n [$label] rc=$rc expect=$expect got=$got needle_seen=$hit HEAD=$moved verdict=$verdict"
  printf '%s\n' "$out" | grep -E "R3 CHAIN OVERTAKEN|DECLARED GAP|W-355 declared form|T3 REFUSES|T3 headline|— committed:|✗ " | sed 's/^/      | /' | cut -c1-170 | head -8
  [ "$moved" != "held" ] && echo "      | subject: $(git log -1 --format=%s)" && echo "      | files:   $(git show --name-only --format= HEAD | tr '\n' ' ')"
}
UNF=knowledge/_git_commit.unfixed.sh; FIX=knowledge/_git_commit.sh
echo "=== CONTROL (unfixed script) — the deadlock must reproduce BOTH ways ==="
arm "control: SESSION_N=238 alone → R3"          RED   "R3 CHAIN OVERTAKEN"                 $UNF SESSION_N=238 -- _HANDOFF-239-x.md
arm "control: SESSION_ACK alone → T3 s130-D3"    RED   "non-wrap commit with no SESSION_N"  $UNF SESSION_ACK="$ACK" -- _HANDOFF-239-x.md
echo "=== FIXED script — the declared form ==="
arm "fixed: SESSION_N=238 + SESSION_ACK (wrapped seat)" GREEN "W-355 declared form" $FIX SESSION_N=238 SESSION_ACK="$ACK" -- _HANDOFF-239-x.md
printf 'more work after the handoff\n' > work.txt
arm "fixed: SESSION_N=238 alone, overtake still on disk → R3 still RED" RED "R3 CHAIN OVERTAKEN" $FIX SESSION_N=238 -- work.txt
arm "fixed: SESSION_N=239 + SESSION_ACK (next seat)"     GREEN "W-355 declared form" $FIX SESSION_N=239 SESSION_ACK="$ACK" -- work.txt
printf 'wrap-time work\n' > work2.txt
arm "fixed: --wrap SESSION_N=239 + ACK, banner #238 → T3 still refuses" RED "T3 REFUSES (s130-D3)" $FIX SESSION_N=239 SESSION_ACK="$ACK" -- --wrap work2.txt
arm "fixed: --wrap SESSION_N=238 + ACK → lands from the banner"         GREEN "W-355 declared form" $FIX SESSION_N=238 SESSION_ACK="$ACK" -- --wrap work2.txt
echo "=== fixture log ==="; git log --format='%h %s' | sed 's/^/  /'
echo "=== cleanup ==="
cd /; rm -rf /dev/shm/w355
echo "leftover dirs: $(ls -d /dev/shm/w355 2>/dev/null | wc -l) · git processes: $(pgrep -c -x git 2>/dev/null || echo 0) · locks: $(find /dev/shm -name '*.lock' 2>/dev/null | wc -l)"
