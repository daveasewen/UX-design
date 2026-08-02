#!/usr/bin/env python3
"""
_test_git_commit.py — harness for knowledge/_git_commit.sh (handoff-testing regime, session #78).

WHY: the commit script is the seam where a red wrap / stale chain / stale msgfile becomes
DURABLE. Its #74-D1 consumer split and the #78-D3 headline prefix were proven by one-off
shims on the real seam at ruling time and never had a permanent harness — a green that
cannot be re-run is an assertion. This suite runs the REAL script text inside throwaway
fixture repos (tempfile — native fs, normal perms, git init works) and bites by NAME.

Method: each arm builds a fresh fixture repo: git init + initial commit + a dirty file +
a knowledge/ dir holding (a) a copy of the real _git_commit.sh, (b) stub _gen_chain.py and
(c) stub _capture_gate.py whose exit codes are forced via STUB_GEN_CHAIN_EXIT /
STUB_CAPTURE_GATE_EXIT env vars, (d) a GOOD-MORNING.md banner variant per arm. A fake
tiktoken on PYTHONPATH keeps the self-heal block instant and offline. Mutation controls
re-run an arm against a deliberately broken script copy and PASS only if the arm goes RED —
every green here is provably able to fail.

Run:  python3 knowledge/_test_git_commit.py --selftest        (exit 0 green / 1 red)
      python3 knowledge/_test_git_commit.py --selftest --only <substr>   (chunking)

NOT covered (declared, not glossed): the real _gen_chain.py / _capture_gate.py verdict
honesty (their own selftests own that — this harness proves the CONSUMER both ways);
the sandbox delete-guard itself (fixtures live on a normal fs, so the mv-aside dance is
proven mechanically, not against a guard that blocks unlink); step 0.5 reconcile judgment.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REAL_SCRIPT = os.path.join(HERE, "_git_commit.sh")

BANNER_PRIMARY = ("> ## ★ LATEST — 2026-08-02 (Sun **#77**, SONNET sub — "
                  "✅ **SUMMARY GLYPHS**)\n")
BANNER_NO_INNER_SEP = "> ## ★ LATEST — 2026-08-02 (Sun **#77**, SONNET sub ✅ NO-SEP)\n"
BANNER_LONG_SUMMARY = ("> ## ★ LATEST — 2026-08-02 (Sun **#77**, SONNET sub — "
                       + "✅ " + "L" * 130 + ")\n")
GM_NO_BANNER = "# GOOD-MORNING\n\nNo latest banner here at all.\n"

EXPECT_NONWRAP = "after #77 2026-08-02 — ✅ **SUMMARY GLYPHS**"
EXPECT_WRAP = "#77 2026-08-02 — ✅ **SUMMARY GLYPHS**"

# ⚠ blank separator line is deliberate: git's %s subject folds ALL lines up to the first
# blank line into one subject. The script preserves body lines verbatim (T3 rewrites only
# line 1), so a msgfile whose body starts on line 2 with no blank line gets its body folded
# into the git subject. That is git behaviour, not a script defect — but it means real
# msgfiles should carry a blank line 2 (declared in the harness report).
MSG_BODY = "PLACEHOLDER-HEADLINE-to-be-replaced-by-T3\n\nbody: fixture arm detail line\n"

RESULTS = []


def sh(cmd, cwd, env=None, timeout=35):
    """Run a command; return (exit, combined output). Fails LOUD and NAMED on timeout."""
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError("TIMEOUT (%ss) running %r in %s" % (timeout, cmd, cwd))
    return r.returncode, (r.stdout + r.stderr)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


STUB_TMPL = '''#!/usr/bin/env python3
import os, sys
code = os.environ.get("{var}", "0")
if not code.isdigit():
    sys.exit("stub {name}: {var} is not a digit: %r" % code)
print("STUB {name} args=%r exit=%s" % (sys.argv[1:], code))
sys.exit(int(code))
'''

FAKE_TIKTOKEN = '''class _Enc:
    def encode(self, s):
        return [0] * max(1, len(s) // 4)
def get_encoding(name):
    return _Enc()
'''


def build_fixture(root, script_text, banner):
    """git repo + knowledge/ stubs + GM banner + one dirty file + msgfile. Returns env."""
    know = os.path.join(root, "knowledge")
    write(os.path.join(know, "_git_commit.sh"), script_text)
    write(os.path.join(know, "_gen_chain.py"),
          STUB_TMPL.format(var="STUB_GEN_CHAIN_EXIT", name="_gen_chain.py"))
    write(os.path.join(know, "_capture_gate.py"),
          STUB_TMPL.format(var="STUB_CAPTURE_GATE_EXIT", name="_capture_gate.py"))
    write(os.path.join(know, "_build_live_state.py"),
          STUB_TMPL.format(var="STUB_LIVE_STATE_EXIT", name="_build_live_state.py"))
    write(os.path.join(root, "pystubs", "tiktoken.py"), FAKE_TIKTOKEN)
    write(os.path.join(root, "GOOD-MORNING.md"), banner)
    write(os.path.join(root, "README.md"), "fixture repo\n")

    for cmd in (["git", "init", "-q"],
                ["git", "config", "user.name", "Fixture"],
                ["git", "config", "user.email", "fixture@test.local"],
                ["git", "add", "-A"],
                ["git", "commit", "-q", "-m", "init"]):
        rc, out = sh(cmd, cwd=root)
        if rc != 0:
            raise RuntimeError("fixture setup failed at %r: %s" % (cmd, out))

    write(os.path.join(root, "work.txt"), "dirty work to stage\n")
    write(os.path.join(root, "msg.txt"), MSG_BODY)

    env = dict(os.environ)
    env.update({
        "HOME": root,
        "GIT_CONFIG_NOSYSTEM": "1",
        "PYTHONPATH": os.path.join(root, "pystubs"),
        "STUB_GEN_CHAIN_EXIT": "0",
        "STUB_CAPTURE_GATE_EXIT": "0",
        "STUB_LIVE_STATE_EXIT": "0",
    })
    return env


def run_commit(root, env, args):
    script = os.path.join(root, "knowledge", "_git_commit.sh")
    return sh(["bash", script] + list(args), cwd=root, env=env)


def head_hash(root):
    rc, out = sh(["git", "rev-parse", "HEAD"], cwd=root)
    if rc != 0:
        raise RuntimeError("git rev-parse HEAD failed in fixture: " + out)
    return out.strip()


def head_subject(root):
    rc, out = sh(["git", "log", "-1", "--format=%s"], cwd=root)
    if rc != 0:
        raise RuntimeError("git log failed in fixture: " + out)
    return out.strip()


def staged_empty(root):
    rc, _ = sh(["git", "diff", "--cached", "--quiet"], cwd=root)
    return rc == 0


def real_script_text():
    with open(REAL_SCRIPT, encoding="utf-8") as f:
        return f.read()


# ---------------- arms (each takes script_text so mutation controls can reuse) ----------

def arm_happy_path(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "expected exit 0, got %d; out tail: %s" % (rc, out[-400:])
        if head_hash(root) == before:
            return False, "HEAD did not advance"
        if "staged: work.txt" not in out:
            return False, "dirty file was not staged; out: %s" % out[-400:]
        if "✓ done" not in out:
            return False, "success line missing"
        if "⚠ HEAD message does not match" in out:
            return False, "stale-msgfile mismatch warning fired on happy path"
        subj = head_subject(root)
        if subj != EXPECT_NONWRAP:
            return False, "subject %r != expected %r" % (subj, EXPECT_NONWRAP)
        return True, ""


def arm_nonwrap_prefix(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "exit %d; out tail: %s" % (rc, out[-400:])
        subj = head_subject(root)
        if not subj.startswith("after #77 2026-08-02 — "):
            return False, "non-wrap subject lacks 'after #N date — ' prefix: %r" % subj
        if subj != EXPECT_NONWRAP:
            return False, "subject %r != expected %r" % (subj, EXPECT_NONWRAP)
        return True, ""


def arm_wrap_no_prefix(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"])
        if rc != 0:
            return False, "exit %d; out tail: %s" % (rc, out[-400:])
        subj = head_subject(root)
        if subj.startswith("after "):
            return False, "wrap subject wrongly carries the 'after ' prefix: %r" % subj
        if subj != EXPECT_WRAP:
            return False, "subject %r != expected %r" % (subj, EXPECT_WRAP)
        return True, ""


def arm_cap_after_prefix(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_LONG_SUMMARY)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "exit %d; out tail: %s" % (rc, out[-400:])
        subj = head_subject(root)
        if not subj.startswith("after #77"):
            return False, "capped subject lost the prefix: %r" % subj
        if len(subj) > 120:
            return False, "cap not applied after prefixing: len=%d %r" % (len(subj), subj)
        if not subj.endswith("…"):
            return False, "long summary not visibly truncated: %r" % subj
        return True, ""


def arm_warn_split_plain(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_CAPTURE_GATE_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "plain commit BLOCKED by red gate (exit %d) — WARN mode broken" % rc
        if head_hash(root) == before:
            return False, "commit did not land under WARN mode"
        if "wrap gate RED — visible, not blocking" not in out:
            return False, "warn text missing; out tail: %s" % out[-400:]
        return True, ""


def arm_warn_split_wrap_blocks(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_CAPTURE_GATE_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"])
        if rc == 0:
            return False, "red gate on --wrap did NOT block"
        if "wrap gate RED on a --wrap commit" not in out:
            return False, "blocking message missing; out tail: %s" % out[-400:]
        if head_hash(root) != before:
            return False, "HEAD advanced despite blocked wrap"
        if not staged_empty(root):
            return False, "something was staged despite refusal"
        return True, ""


def arm_spine_consumer_warn_plain(script_text):
    # #78-D2 consumer, WARN side: a red spine-writer selftest on a PLAIN commit is visible,
    # never blocking — a mid-session commit is a correct state (the ds-022 lesson, as #74-D1).
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_LIVE_STATE_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "plain commit BLOCKED by red spine-writer (exit %d) — WARN mode broken" % rc
        if head_hash(root) == before:
            return False, "commit did not land under spine-writer WARN mode"
        if "spine-writer selftest RED — visible, not blocking" not in out:
            return False, "spine-writer warn text missing; out tail: %s" % out[-400:]
        return True, ""


def arm_spine_consumer_wrap_blocks(script_text):
    # #78-D2 consumer, BLOCK side: red spine-writer selftest on --wrap refuses, nothing staged.
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_LIVE_STATE_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"])
        if rc == 0:
            return False, "red spine-writer on --wrap did NOT block"
        if "spine-writer selftest RED on a --wrap commit" not in out:
            return False, "spine-writer blocking message missing; out tail: %s" % out[-400:]
        if head_hash(root) != before:
            return False, "HEAD advanced despite blocked wrap"
        if not staged_empty(root):
            return False, "something was staged despite spine-writer refusal"
        return True, ""


def arm_gen_chain_refusal(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_GEN_CHAIN_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc == 0:
            return False, "script did not refuse on _gen_chain.py --check exit 1"
        if "--check REFUSED" not in out:
            return False, "refusal message missing; out tail: %s" % out[-400:]
        if "STUB _gen_chain.py args=['--check']" not in out:
            return False, "stub was not called with --check; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged before the chain check refused"
        if head_hash(root) != before:
            return False, "HEAD advanced despite chain refusal"
        return True, ""


def arm_missing_msgfile(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["--reconciled", "no-such-msg.txt"])
        if rc == 0:
            return False, "missing msgfile did not refuse"
        if "missing or empty" not in out:
            return False, "stale-msgfile trap message missing; out: %s" % out[-300:]
        return True, ""


def arm_empty_msgfile(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        write(os.path.join(root, "empty.txt"), "")
        rc, out = run_commit(root, env, ["--reconciled", "empty.txt"])
        if rc == 0:
            return False, "empty msgfile did not refuse"
        if "missing or empty" not in out:
            return False, "stale-msgfile trap message missing; out: %s" % out[-300:]
        return True, ""


def arm_no_args(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, [])
        if rc == 0:
            return False, "no-args invocation did not refuse"
        if "no msgfile given" not in out:
            return False, "usage refusal missing; out: %s" % out[-300:]
        return True, ""


def arm_not_reconciled(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["msg.txt"])
        if rc == 0:
            return False, "missing --reconciled did not refuse"
        if "refusing to stage" not in out:
            return False, "reconcile refusal missing; out: %s" % out[-300:]
        if not staged_empty(root):
            return False, "staged despite reconcile refusal"
        return True, ""


def arm_stale_lock_moved(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        write(os.path.join(root, ".git", "index.lock"), "")
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "pre-existing index.lock blocked the run (exit %d); out tail: %s" % (
                rc, out[-400:])
        if head_hash(root) == before:
            return False, "commit did not land after lock dance"
        stale_dir = os.path.join(root, "_to_delete", "_stale_locks")
        if not os.path.isdir(stale_dir):
            return False, "_to_delete/_stale_locks was never created"
        moved = [f for f in os.listdir(stale_dir) if re.match(r"^index\.lock\.\d+", f)]
        if not moved:
            return False, "index.lock was not mv'd into _stale_locks; contents: %r" % (
                os.listdir(stale_dir),)
        return True, ""


def arm_banner_fallback(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_NO_INNER_SEP)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc != 0:
            return False, "fallback heading blocked the commit (exit %d); out tail: %s" % (
                rc, out[-400:])
        if "T3 NOTE" not in out:
            return False, "fallback note not printed; out tail: %s" % out[-400:]
        subj = head_subject(root)
        if not subj.startswith("after #77 2026-08-02 — 2026-08-02 ("):
            return False, "fallback subject shape unexpected: %r" % subj
        return True, ""


def arm_missing_banner_fails_loud(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, GM_NO_BANNER)
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"])
        if rc == 0:
            return False, "wholly missing banner did NOT fail loud"
        if "T3 headline generation failed" not in out:
            return False, "loud T3 failure message missing; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite T3 failure"
        if head_hash(root) != before:
            return False, "HEAD advanced despite T3 failure"
        return True, ""


# ---------------- mutation controls (the arm must go RED against a broken copy) ---------

def mutation_prefix_removed(script_text):
    target = 'prefix = "" if wrap == "1" else "after "'
    if target not in script_text:
        raise RuntimeError("mutation target not found — _git_commit.sh drifted from the "
                           "#78-D3 form this harness pins: %r" % target)
    mutated = script_text.replace(target, 'prefix = ""')
    ok, detail = arm_nonwrap_prefix(mutated)
    if ok:
        return False, "arm_nonwrap_prefix stayed GREEN against a prefix-stripped script — harness cannot fail"
    return True, "went RED as required: %s" % detail


def mutation_lockclear_removed(script_text):
    target = "# clear · stage · clear · commit · clear\nclear_locks\n"
    if target not in script_text:
        raise RuntimeError("mutation target not found — pre-stage clear_locks line moved; "
                           "update the mutation control")
    mutated = script_text.replace(
        target, "# clear · stage · clear · commit · clear\n: # MUTATED: clear_locks removed\n")
    ok, detail = arm_stale_lock_moved(mutated)
    if ok:
        return False, "arm_stale_lock_moved stayed GREEN with the lock-clear deleted — harness cannot fail"
    return True, "went RED as required: %s" % detail


ARMS = [
    ("happy_path_commit_lands", arm_happy_path),
    ("nonwrap_headline_after_prefix_78D3", arm_nonwrap_prefix),
    ("wrap_headline_no_prefix", arm_wrap_no_prefix),
    ("cap_120_applied_after_prefix", arm_cap_after_prefix),
    ("warn_split_red_gate_plain_commit_lands", arm_warn_split_plain),
    ("warn_split_red_gate_wrap_blocks", arm_warn_split_wrap_blocks),
    ("spine_consumer_warn_plain_78D2", arm_spine_consumer_warn_plain),
    ("spine_consumer_wrap_blocks_78D2", arm_spine_consumer_wrap_blocks),
    ("gen_chain_check_refusal_pre_stage", arm_gen_chain_refusal),
    ("missing_msgfile_refused", arm_missing_msgfile),
    ("empty_msgfile_refused", arm_empty_msgfile),
    ("no_args_refused", arm_no_args),
    ("not_reconciled_refused", arm_not_reconciled),
    ("stale_index_lock_moved_aside", arm_stale_lock_moved),
    ("banner_fallback_note_printed", arm_banner_fallback),
    ("missing_banner_fails_loud", arm_missing_banner_fails_loud),
    ("MUTATION_prefix_stripped_bites", mutation_prefix_removed),
    ("MUTATION_lockclear_removed_bites", mutation_lockclear_removed),
]


def main(argv):
    only = None
    args = list(argv)
    if "--only" in args:
        i = args.index("--only")
        try:
            only = args[i + 1]
        except IndexError:
            sys.exit("--only needs a substring argument")
        del args[i:i + 2]
    for a in args:
        if a != "--selftest":
            sys.exit("unknown argument %r — usage: --selftest [--only <substr>]" % a)

    script_text = real_script_text()
    print("== _test_git_commit.py selftest — real script: %s (%d bytes) ==" % (
        REAL_SCRIPT, len(script_text)))
    for name, fn in ARMS:
        if only and only not in name:
            continue
        try:
            ok, detail = fn(script_text)
        except RuntimeError as e:
            ok, detail = False, "LOUD helper failure: %s" % e
        RESULTS.append((name, ok, detail))
        print(("  PASS  " if ok else "  FAIL  ") + name +
              ((" — " + detail) if detail and (not ok or name.startswith("MUTATION")) else ""))

    bites = [(n, d) for n, o, d in RESULTS if not o]
    print("--")
    if bites:
        print("BITES (%d):" % len(bites))
        for n, d in bites:
            print("  ✗ %s — %s" % (n, d))
        return 1
    print("ALL GREEN — %d arms (incl. %d mutation controls)" % (
        len(RESULTS), sum(1 for n, _, _ in RESULTS if n.startswith("MUTATION"))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
