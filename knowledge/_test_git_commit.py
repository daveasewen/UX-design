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
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import datetime
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

# s130-D3 (#130, Dave: GENERATE, NEVER INHERIT) — a NON-wrap subject is no longer derived from
# the on-disk ★ LATEST banner at all. It is generated from current-session sources only:
# the verified SESSION_N witness, today's `date`, and the msgfile's OWN first line:
#     after #<SESSION_N> <today> — <msgfile line 1>
# --wrap still derives from the banner (the wrap writes it first) and additionally ASSERTS the
# banner's #N == SESSION_N. Harness expectations follow the SCRIPT, never the reverse.
TODAY = datetime.date.today().isoformat()
MSG_FIRST_LINE = "PLACEHOLDER-HEADLINE-to-be-replaced-by-T3"
EXPECT_NONWRAP = "after #77 %s — %s" % (TODAY, MSG_FIRST_LINE)
EXPECT_WRAP = "#77 2026-08-02 — ✅ **SUMMARY GLYPHS**"

# #128 (P5, Dave 2026-08-02: `git add -A` RETIRED) — the script now REFUSES to stage unless the
# caller NAMES the paths (or passes --all-dirty). Every arm that must land a commit therefore
# names the fixture's dirty file explicitly.
STAGE_PATHS = ["work.txt"]

# ⚠ blank separator line: git's %s subject folds ALL lines up to the first blank line into
# one subject. This comment used to say "git behaviour, not a script defect — real msgfiles
# should carry a blank line 2". Commit 0eacf2d (#123→#124 seam) proved that a documented-but-
# ungated hazard is a scheduled defect: a JSONL body with no separator shipped an ~83,000-char
# subject and broke every git-log consumer at the next boot. #124: T3 now INSERTS the blank
# line (remedy) and a post-commit 200-char subject cap fails loud (consumer) — arms
# subject_fold_* below pin both.
MSG_BODY = MSG_FIRST_LINE + "\n\nbody: fixture arm detail line\n"

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
    write(os.path.join(know, "_session.py"),
          STUB_TMPL.format(var="STUB_SESSION_EXIT", name="_session.py"))
    # #191: the W-20 doc-row gate (wired into _git_commit.sh at #188) had no stub here, so EVERY
    # commit-path arm had been failing on `can't open file .../_gate_doc_rows.py` since that wiring
    # — and the three legacy mutation controls were going RED for the WRONG reason [[a-crash-is-not-a-fail]].
    write(os.path.join(know, "_gate_doc_rows.py"),
          STUB_TMPL.format(var="STUB_DOC_ROWS_EXIT", name="_gate_doc_rows.py"))
    # #192: the s191-D1 showroom sync gate (wired into _git_commit.sh at #191) had no stub here —
    # the SAME blind-harness class as the #188 doc-row gate, recurring one session later: all 14
    # commit-path arms were crashing on `can't open file .../gen_showroom.py` and the three legacy
    # mutation controls were green for the WRONG reason [[a-crash-is-not-a-fail]]. The recurrence
    # is why the detector below (_gate_harness_stubs.py) exists as an ARM, not a reminder.
    write(os.path.join(know, "gen_showroom.py"),
          STUB_TMPL.format(var="STUB_SHOWROOM_EXIT", name="gen_showroom.py"))
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
        "STUB_SESSION_EXIT": "0",
        "STUB_DOC_ROWS_EXIT": "0",
        "STUB_SHOWROOM_EXIT": "0",
        # #120: the SESSION_N session-witness gate (post-#116) BLOCKS a --wrap commit
        # without a declared session. Fixtures declare #77 to match BANNER_PRIMARY;
        # the gate's own clauses get dedicated arms (wrap_undeclared_session_blocks,
        # wrap_session_witness_refusal_blocks).
        "SESSION_N": "77",
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
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc != 0:
            return False, "expected exit 0, got %d; out tail: %s" % (rc, out[-400:])
        if head_hash(root) == before:
            return False, "HEAD did not advance"
        if "staged: work.txt" not in out:
            return False, "dirty file was not staged; out: %s" % out[-400:]
        if "✓ done" not in out:
            return False, "success line missing"
        # #192 — DEAD ASSERTION REPLACED. This arm used to assert the ABSENCE of
        # "⚠ HEAD message does not match", a string RETIRED at #128 when the substring warning
        # became the #171 SUBJECT-IDENTITY ASSERT. Grepped at #192: that text appears NOWHERE in
        # _git_commit.sh, so the check could not fire in either direction — a green that cannot
        # fail is an assertion [[unmatched-grep-is-not-an-absence]]. Assert the LIVE seam instead:
        # the #171 assert must have RUN and agreed, and no mismatch may have been reported.
        if "SUBJECT MISMATCH" in out:
            return False, "the #171 subject-identity assert reported a mismatch on the happy path"
        if "subject asserted identical to the headline T3 generated" not in out:
            return False, "the #171 subject-identity assert did not run; out tail: %s" % out[-400:]
        # #192 — the two gates whose absent stubs blinded this harness (doc-row #188, showroom
        # s191-D1) must be SEEN to run on the happy path, not merely stubbed into silence.
        if "— doc rows present" not in out:
            return False, "doc-row gate (W-20) did not run on the happy path; out tail: %s" % out[-400:]
        if "— showroom in sync" not in out:
            return False, "showroom sync gate (s191-D1) did not run on the happy path; out tail: %s" % out[-400:]
        subj = head_subject(root)
        if subj != EXPECT_NONWRAP:
            return False, "subject %r != expected %r" % (subj, EXPECT_NONWRAP)
        return True, ""


def arm_nonwrap_prefix(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc != 0:
            return False, "exit %d; out tail: %s" % (rc, out[-400:])
        subj = head_subject(root)
        if not subj.startswith("after #77 %s — " % TODAY):
            return False, "non-wrap subject lacks 'after #N date — ' prefix: %r" % subj
        if subj != EXPECT_NONWRAP:
            return False, "subject %r != expected %r" % (subj, EXPECT_NONWRAP)
        return True, ""


def arm_wrap_no_prefix(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
        if rc != 0:
            return False, "exit %d; out tail: %s" % (rc, out[-400:])
        subj = head_subject(root)
        if subj.startswith("after "):
            return False, "wrap subject wrongly carries the 'after ' prefix: %r" % subj
        if subj != EXPECT_WRAP:
            return False, "subject %r != expected %r" % (subj, EXPECT_WRAP)
        return True, ""


def arm_cap_after_prefix(script_text):
    # INTENT PRESERVED (source moved, not the rule): the 120-char cap is applied AFTER the
    # "after #N <date> — " prefix is composed, so the prefix survives truncation. s130-D3 made
    # the long text come from the MSGFILE's first line rather than a long banner summary
    # (BANNER_LONG_SUMMARY is now only reachable on --wrap), so the arm feeds a long first line.
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        write(os.path.join(root, "msg.txt"), "L" * 200 + "\n\nbody: cap arm\n")
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
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
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
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
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
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
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
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
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
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
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
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


def arm_doc_row_gate_refusal(script_text):
    """W-20 (#188) — the doc-row gate BLOCKS pre-stage when red, and its DOC_ROW_ACK hatch passes
    it as a DECLARED gap. #192: a stub existed for this gate since #191 but NOTHING drove it, so
    STUB_DOC_ROWS_EXIT was never once non-zero — the stub made the arms RUN, not the gate TESTED.
    """
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_DOC_ROWS_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "red doc-row gate did NOT block the commit"
        if "doc-row gate REFUSED" not in out:
            return False, "doc-row refusal message missing; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite the doc-row refusal"
        if head_hash(root) != before:
            return False, "HEAD advanced despite the doc-row refusal"
        # declared passes, silent fails: the ACK hatch must let the SAME red gate through, named.
        env["DOC_ROW_ACK"] = "fixture-declared gap (#192 arm)"
        rc2, out2 = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc2 != 0:
            return False, "DOC_ROW_ACK did not pass the red gate (exit %d); out tail: %s" % (rc2, out2[-400:])
        if "doc-row gate: DECLARED GAP — fixture-declared gap (#192 arm)" not in out2:
            return False, "the declared gap was not NAMED in the output; out tail: %s" % out2[-400:]
        if head_hash(root) == before:
            return False, "commit did not land under the declared-gap hatch"
        return True, ""


def arm_showroom_gate_refusal(script_text):
    """s191-D1 (#191, Dave: "yes") — the showroom sync gate BLOCKS pre-stage when red, with the
    same SHOWROOM_ACK declared-gap hatch. This gate had NO stub at all until #192, which is the
    blind-harness recurrence the detector below exists to catch."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_SHOWROOM_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "red showroom gate did NOT block the commit"
        if "showroom sync gate REFUSED (s191-D1)" not in out:
            return False, "showroom refusal message missing; out tail: %s" % out[-400:]
        if "STUB gen_showroom.py args=['--check']" not in out:
            return False, "the gate was not invoked with --check; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite the showroom refusal"
        if head_hash(root) != before:
            return False, "HEAD advanced despite the showroom refusal"
        env["SHOWROOM_ACK"] = "fixture-declared gap (#192 arm)"
        rc2, out2 = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc2 != 0:
            return False, "SHOWROOM_ACK did not pass the red gate (exit %d); out tail: %s" % (rc2, out2[-400:])
        if "showroom sync gate: DECLARED GAP — fixture-declared gap (#192 arm)" not in out2:
            return False, "the declared gap was not NAMED in the output; out tail: %s" % out2[-400:]
        if head_hash(root) == before:
            return False, "commit did not land under the declared-gap hatch"
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
    """CURRENT refusal semantics, two clauses (the arm follows the script, never the reverse):

    (a) ZERO args: s133-D2 added a `--push` dispatch on "$1" ABOVE the usage check, and the
        script runs under `set -u` — so a bare invocation refuses at that line with an unbound-
        variable error, never reaching "no msgfile given". A crash IS a refusal here (nothing is
        staged, HEAD is held) but it is NOT the same clause, so it is asserted separately and by
        name rather than papered over.
    (b) FLAGS BUT NO MSGFILE: the reachable path to the usage refusal proper.
    """
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, [])
        if rc == 0:
            return False, "no-args invocation did not refuse"
        if "unbound variable" not in out and "no msgfile given" not in out:
            return False, "no-args refusal is neither the set -u guard nor the usage text: %s" % out[-300:]
        if not staged_empty(root):
            return False, "staged despite no-args refusal"
        rc2, out2 = run_commit(root, env, ["--reconciled"])
        if rc2 == 0:
            return False, "--reconciled with no msgfile did not refuse"
        if "no msgfile given" not in out2:
            return False, "usage refusal missing; out: %s" % out2[-300:]
        if not staged_empty(root):
            return False, "staged despite usage refusal"
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
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
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
    # INTENT PRESERVED, PATH MOVED: a heading with no " — " of its own inside the parenthetical
    # falls back to the first-em-dash reading and prints a NOTE rather than blocking. s130-D3
    # made banner derivation reachable ONLY on --wrap (a non-wrap subject never reads the
    # banner), so this arm now drives the wrap path.
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_NO_INNER_SEP)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
        if rc != 0:
            return False, "fallback heading blocked the commit (exit %d); out tail: %s" % (
                rc, out[-400:])
        if "T3 NOTE" not in out:
            return False, "fallback note not printed; out tail: %s" % out[-400:]
        subj = head_subject(root)
        if not subj.startswith("#77 2026-08-02 — 2026-08-02 ("):
            return False, "fallback subject shape unexpected: %r" % subj
        return True, ""


def arm_missing_banner_fails_loud(script_text):
    with tempfile.TemporaryDirectory() as root:
        # INTENT PRESERVED, PATH MOVED (s130-D3): a wholly missing ★ LATEST heading is only a
        # T3 input on --wrap; a non-wrap commit never reads GOOD-MORNING.md at all.
        env = build_fixture(root, script_text, GM_NO_BANNER)
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "wholly missing banner did NOT fail loud"
        if "T3 headline generation REFUSED" not in out:
            return False, "loud T3 failure message missing; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite T3 failure"
        if head_hash(root) != before:
            return False, "HEAD advanced despite T3 failure"
        return True, ""


# #120: the post-#116 session-witness gate's own clauses. BLOCK side: a --wrap commit with
# no SESSION_N and no SESSION_ACK refuses pre-stage. REFUSAL side: a declared SESSION_N whose
# _session.py --declare exits non-zero refuses pre-stage. Both assert nothing staged, HEAD held.

def arm_wrap_undeclared_session_blocks(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        del env["SESSION_N"]
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "--wrap with no SESSION_N did NOT block"
        if "the FINAL commit must declare its session" not in out:
            return False, "SESSION_N blocking message missing; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite SESSION_N block"
        if head_hash(root) != before:
            return False, "HEAD advanced despite SESSION_N block"
        return True, ""


def arm_wrap_session_witness_refusal_blocks(script_text):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_SESSION_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "refused session witness did NOT block"
        if "_session.py REFUSED" not in out:
            return False, "witness-refusal message missing; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite witness refusal"
        if head_hash(root) != before:
            return False, "HEAD advanced despite witness refusal"
        return True, ""


def arm_subject_fold(script_text):
    """#124 — a msgfile whose body starts on line 2 with NO blank separator (the 0eacf2d
    shape) must still land with a SHORT subject: T3 inserts the blank line."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        write(os.path.join(root, "msg.txt"),
              "PLACEHOLDER-HEADLINE\n" + '{"date":"x","fails":0,"kind":"rehearse"}\n' * 6)
        expect = "after #77 %s — PLACEHOLDER-HEADLINE" % TODAY   # s130-D3 generated form
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc != 0:
            return False, "exit %d; out tail: %s" % (rc, out[-400:])
        subj = head_subject(root)
        if subj != expect:
            return False, "folded/wrong subject (len=%d): %r" % (len(subj), subj[:120])
        rc, body = sh(["git", "log", "-1", "--format=%b"], cwd=root)
        if '"kind":"rehearse"' not in body:
            return False, "body lines lost by the blank-line insert"
        return True, ""


def arm_declare_dirt_names_instrumentation(script_text):
    """W-22 (#191): `--declare-dirt` must NAME an instrumentation append and its writer, and must
    NOT declare ordinary dirt. The fixture PLANTS a dirty `notes/_REHEARSAL-LOG.jsonl` alongside
    the fixture's ordinary `work.txt`; both must appear in the dirty list, only the instrumentation
    path in the DECLARED block [[gate-must-quote-what-it-forbids]]."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        # PLANT it the way the real defect arrives: a TRACKED file the instruments APPEND to.
        # (An untracked file would be collapsed to `notes/` by `git status --short` and the arm
        # would be measuring directory collapse, not the declaration [[attribute-the-diff]].)
        log = os.path.join(root, "notes", "_REHEARSAL-LOG.jsonl")
        write(log, '{"kind":"rehearse","planted_by":"_test_git_commit.py"}\n')
        for cmd in (["git", "add", "notes/_REHEARSAL-LOG.jsonl"],
                    ["git", "commit", "-q", "-m", "rehearsal baseline"]):
            rc, out = sh(cmd, cwd=root, env=env)
            if rc != 0:
                raise RuntimeError("fixture plant failed at %r: %s" % (cmd, out))
        with open(log, "a", encoding="utf-8") as f:
            f.write('{"kind":"rehearse","appended_by":"the instrument itself"}\n')
        rc, out = run_commit(root, env, ["--declare-dirt"])
        if rc != 0:
            return False, "--declare-dirt is read-only and must exit 0, got %d; out: %s" % (rc, out[-400:])
        if "notes/_REHEARSAL-LOG.jsonl" not in out:
            return False, "planted instrumentation path absent from output: %s" % out[-400:]
        if "— DECLARED: instrumentation appends among the dirty paths" not in out:
            return False, "DECLARED block missing though instrumentation dirt was planted: %s" % out[-400:]
        if "written by:" not in out or "_capture_gate.py" not in out:
            return False, "declaration did not name the WRITER: %s" % out[-400:]
        decl = out.split("— DECLARED:", 1)[1]
        if "work.txt" in decl:
            return False, "ordinary dirt leaked into the DECLARED block — the declaration over-claims: %s" % decl
        if "_graph-mark-observations.jsonl" in decl:
            return False, "a NON-dirty instrumentation path was declared — the check is not reading the blob: %s" % decl
        return True, ""


def arm_declare_dirt_silent_without_instrumentation(script_text):
    """The other direction: ordinary dirt alone must print the dirty list and NO declaration."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        rc, out = run_commit(root, env, ["--declare-dirt"])
        if rc != 0:
            return False, "expected exit 0, got %d; out: %s" % (rc, out[-400:])
        if "work.txt" not in out:
            return False, "ordinary dirt missing from the dirty list: %s" % out[-400:]
        if "DECLARED: instrumentation appends" in out:
            return False, "DECLARED block fired with no instrumentation path dirty: %s" % out[-400:]
        return True, ""


def arm_harness_stub_coverage(script_text):
    """W-33 (#192) — THE DETECTOR'S CONSUMER. _gate_harness_stubs.py checks that every gate
    _git_commit.sh invokes has a fixture stub above. Twice now a gate was wired in unstubbed
    (#188 doc-row, #191 showroom) and the resulting CRASH read as a result; this arm is what
    makes the third time impossible [[instrument-without-a-consumer]].

    It reads the REAL files on disk (not `script_text`), because the coverage question is about
    the repo's true harness/script pair, not about a mutated copy.
    """
    sys.path.insert(0, HERE)
    import _gate_harness_stubs
    try:
        missing = _gate_harness_stubs.unstubbed()
    except RuntimeError as e:
        return False, "detector failed LOUD: %s" % e
    if missing:
        return False, ("BLIND HARNESS — _git_commit.sh invokes unstubbed gate(s): %s. Every "
                       "commit-path arm would crash on them and the crash would read as a result."
                       % ", ".join(n for n, _ in missing))
    return True, ""


# ---------------- mutation controls (the arm must go RED against a broken copy) ---------

def mutation_harness_stub_detector_bites(script_text):
    """W-33 (#192) — plant an unstubbed gate invocation on a COPY of _git_commit.sh and prove the
    detector REFUSES; the real tree is never touched (tempdir copies only, [[a-crash-is-not-a-fail]]
    demands the detector be shown able to fail, not asserted to be)."""
    with tempfile.TemporaryDirectory() as root:
        sys.path.insert(0, HERE)
        import _gate_harness_stubs
        planted = os.path.join(root, "_git_commit.sh")
        write(planted, script_text +
              '\npython3 knowledge/_gate_totally_unstubbed.py --check || fail "planted"\n')
        harness_copy = os.path.join(root, "_test_git_commit.py")
        with open(os.path.abspath(__file__), encoding="utf-8") as f:
            write(harness_copy, f.read())
        missing = _gate_harness_stubs.unstubbed(planted, harness_copy)
        names = [n for n, _ in missing]
        if "_gate_totally_unstubbed.py" not in names:
            return False, ("detector stayed GREEN against a planted unstubbed gate invocation — "
                           "it cannot fail; found only %r" % names)
        # and the CLEAN direction, same call, so a detector that simply always-refuses is caught:
        if _gate_harness_stubs.unstubbed():
            return False, "detector refuses on the REAL clean tree — it always-refuses, useless"
        return True, "went RED on the planted gate and GREEN on the clean tree: %s" % names




def mutation_blank_insert_removed(script_text):
    """#124 — with the T3 blank-line insert deleted, the fold arm must go RED (the post-commit
    subject cap is the backstop that makes the failure loud rather than silent)."""
    target = 'if body and body[0].strip():\n    body = [""] + body'
    if target not in script_text:
        raise RuntimeError("mutation target not found — the #124 blank-insert block moved; "
                           "update the mutation control")
    mutated = script_text.replace(target, "pass  # MUTATED: blank-insert removed")
    ok, detail = arm_subject_fold(mutated)
    if ok:
        return False, "arm_subject_fold stayed GREEN with the blank-insert deleted — harness cannot fail"
    return True, "went RED as required: %s" % detail



def mutation_prefix_removed(script_text):
    """#78-D3's `prefix = "" if wrap == "1" else "after "` line was RETIRED by s130-D3, which
    replaced banner inheritance with a GENERATED non-wrap subject. The control re-points at the
    current construction line so the mutation still provably bites."""
    target = 'headline = f"after #{session_n} {today} — {first}"'
    if target not in script_text:
        raise RuntimeError("mutation target not found — _git_commit.sh drifted from the "
                           "s130-D3 generated-subject form this harness pins: %r" % target)
    mutated = script_text.replace(target, 'headline = first')
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


def mutation_declare_dirt_call_removed(script_text):
    """W-22 (#191) — with the `--declare-dirt` consumer's call to `declare_instrumentation_dirt`
    deleted, the naming arm must go RED. A declaration whose consumer can be deleted silently is
    [[instrument-without-a-consumer]] in its second shape."""
    target = '    echo "— dirty paths:"; echo "$DIRT"\n    declare_instrumentation_dirt "$DIRT"\n'
    if target not in script_text:
        raise RuntimeError("mutation target not found — the --declare-dirt consumer block in "
                           "_git_commit.sh moved; update the mutation control")
    mutated = script_text.replace(
        target, '    echo "— dirty paths:"; echo "$DIRT"\n    : # MUTATED: declaration call removed\n')
    ok, detail = arm_declare_dirt_names_instrumentation(mutated)
    if ok:
        return False, ("arm_declare_dirt_names_instrumentation stayed GREEN with the declaration "
                       "call deleted — harness cannot fail")
    return True, "went RED as required: %s" % detail


def mutation_declare_dirt_match_widened(script_text):
    """The over-claim direction: if the path match is replaced by an unconditional match, EVERY
    dirty path gets declared. The silent-when-clean arm must go RED."""
    target = '    case "$blob" in\n      *"$p"*)\n'
    if target not in script_text:
        raise RuntimeError("mutation target not found — declare_instrumentation_dirt's case match "
                           "moved; update the mutation control")
    mutated = script_text.replace(target, '    case "$blob" in\n      *)  # MUTATED: match widened\n')
    ok, detail = arm_declare_dirt_silent_without_instrumentation(mutated)
    if ok:
        return False, ("arm_declare_dirt_silent_without_instrumentation stayed GREEN against an "
                       "always-matching declaration — harness cannot fail")
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
    ("wrap_undeclared_session_blocks_120", arm_wrap_undeclared_session_blocks),
    ("wrap_session_witness_refusal_blocks_120", arm_wrap_session_witness_refusal_blocks),
    ("subject_fold_blank_line_inserted_124", arm_subject_fold),
    ("MUTATION_blank_insert_removed_bites_124", mutation_blank_insert_removed),
    ("MUTATION_prefix_stripped_bites", mutation_prefix_removed),
    ("MUTATION_lockclear_removed_bites", mutation_lockclear_removed),
    ("declare_dirt_names_instrumentation_W22", arm_declare_dirt_names_instrumentation),
    ("declare_dirt_silent_without_instrumentation_W22", arm_declare_dirt_silent_without_instrumentation),
    ("MUTATION_declare_dirt_call_removed_bites_W22", mutation_declare_dirt_call_removed),
    ("MUTATION_declare_dirt_match_widened_bites_W22", mutation_declare_dirt_match_widened),
    ("doc_row_gate_refusal_and_ack_W20", arm_doc_row_gate_refusal),
    ("showroom_gate_refusal_and_ack_s191D1", arm_showroom_gate_refusal),
    ("harness_stub_coverage_W33", arm_harness_stub_coverage),
    ("MUTATION_harness_stub_detector_bites_W33", mutation_harness_stub_detector_bites),
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
