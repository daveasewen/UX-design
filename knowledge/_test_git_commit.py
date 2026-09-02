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

# #208 — the mention-map gate (the [110] re-stale class) cannot use STUB_TMPL: it invokes ONE
# generator in TWO modes and the second mode must CHANGE the first mode's answer (regenerate,
# then re-check fresh). A single fixed exit code can only ever exercise the generator-refused
# branch, which would leave the branch that actually matters — regenerated-then-refuse-with-the-
# path — untested [[mutation-tests-the-clause-not-the-feature]]. So: STUB_MENTION_MAP_STALE picks
# the starting state, STUB_MENTION_MAP_REGEN_EXIT decides whether the regeneration itself refuses,
# and a marker (written INSIDE .git, so it never shows up as a dirty path) carries "a regeneration
# has happened" from the second invocation back to the third.
STUB_MENTION_MAP = '''#!/usr/bin/env python3
import os, sys
marker = os.environ["STUB_MENTION_MAP_MARKER"]
regen_exit = os.environ.get("STUB_MENTION_MAP_REGEN_EXIT", "0")
if not regen_exit.isdigit():
    sys.exit("stub _build_graph_mention_map.py: STUB_MENTION_MAP_REGEN_EXIT is not a digit: %r"
             % regen_exit)
stale = os.environ.get("STUB_MENTION_MAP_STALE", "0") == "1"
if "--check" in sys.argv[1:]:
    fresh = (not stale) or os.path.exists(marker)
    print("STUB _build_graph_mention_map.py args=%r fresh=%s" % (sys.argv[1:], fresh))
    sys.exit(0 if fresh else 1)
print("STUB _build_graph_mention_map.py args=%r regenerate exit=%s" % (sys.argv[1:], regen_exit))
if regen_exit == "0":
    open(marker, "w").close()
sys.exit(int(regen_exit))
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
    # #208: the mention-map freshness gate (the [110] re-stale class) was wired into
    # _git_commit.sh THIS session with no stub here — the THIRD occurrence of the blind-harness
    # class (#188 doc-row, #191 showroom), and this time the W-33 detector caught it as a red arm
    # in CI run #355 rather than a human noticing 14 arms crashing [[a-crash-is-not-a-fail]].
    write(os.path.join(know, "_build_graph_mention_map.py"), STUB_MENTION_MAP)
    # #228: the scratch-hygiene probe was wired into _git_commit.sh's --wrap seam THIS session
    # (Dave: "wire both"). FOURTH occurrence of the blind-harness class (#188 doc-row, #191
    # showroom, #208 mention-map) — and, as at #208, the W-33 detector caught it as a red arm
    # rather than a human noticing crashes [[a-crash-is-not-a-fail]]. Caught locally this time,
    # before the push, because the survey was re-run after the wiring instead of before it.
    write(os.path.join(know, "_gate_scratch_hygiene.py"),
          STUB_TMPL.format(var="STUB_SCRATCH_HYGIENE_EXIT", name="_gate_scratch_hygiene.py"))
    # #238 lane P: the polarity gate (s238-D7) was wired into _git_commit.sh's pre-staging seam in
    # the SAME edit as this stub — the blind-harness class (#188, #191, #208, #228) is not getting a
    # fifth instance. Its arm (polarity_gate_refusal_and_ack_s238D7) drives the stub non-zero and
    # through the POLARITY_ACK hatch, so the stub makes the arms RUN *and* the gate TESTED.
    write(os.path.join(know, "_validate_polarities.py"),
          STUB_TMPL.format(var="STUB_POLARITY_EXIT", name="_validate_polarities.py"))
    write(os.path.join(root, "pystubs", "tiktoken.py"), FAKE_TIKTOKEN)
    # The gate's SECOND half asks whether the map differs from HEAD but is unstaged. That
    # question only has a meaningful answer if the map is a TRACKED file, so the fixture commits
    # one at init (see arm_mention_map_regenerated_not_staged).
    write(os.path.join(know, "_graph-mention-map.json"), '{"fixture": "mention map at HEAD"}\n')
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
        "STUB_SCRATCH_HYGIENE_EXIT": "0",
        "STUB_POLARITY_EXIT": "0",          # #238 lane P — the s238-D7 gate's stub, green at rest
        "STUB_MENTION_MAP_STALE": "0",
        "STUB_MENTION_MAP_REGEN_EXIT": "0",
        # marker lives inside .git so a regeneration never registers as a dirty working path
        "STUB_MENTION_MAP_MARKER": os.path.join(root, ".git", "stub-mention-map-regenerated"),
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
        # #208 — same rule for the mention-map gate's two halves: SEEN to run, not stubbed silent.
        if "— mention map fresh" not in out:
            return False, "mention-map freshness gate (#208) did not run on the happy path; out tail: %s" % out[-400:]
        if "— mention map is either unchanged or staged" not in out:
            return False, "mention-map second-half assert (#208) did not run on the happy path; out tail: %s" % out[-400:]
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


def arm_scratch_hygiene_advisory_on_wrap(script_text):
    """#228 — the scratch-hygiene probe RUNS on --wrap and NEVER blocks, even red.

    The #192 lesson in the doc-row arm's own docstring is the reason this exists: *"a stub
    existed for this gate since #191 but NOTHING drove it, so STUB_DOC_ROWS_EXIT was never once
    non-zero — the stub made the arms RUN, not the gate TESTED."* So this arm drives the stub
    NON-ZERO and asserts the commit lands anyway. That is the whole content of the posture:
    the gate is ADVISORY at birth and promotion is ⬛ Dave's, so a red probe blocking a wrap
    would be the defect, not the proof.

    BOTH DIRECTIONS, or it says nothing: it is also asserted ABSENT from a non-wrap commit —
    a mid-session commit is a correct state to hold scratch in, and a probe that ran there
    would be reporting litter the session is still using.
    """
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_SCRATCH_HYGIENE_EXIT"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "--wrap", "msg.txt"] + STAGE_PATHS)
        if rc != 0:
            return False, "a RED advisory probe BLOCKED a --wrap commit (exit %d); out tail: %s" % (rc, out[-400:])
        if "STUB _gate_scratch_hygiene.py" not in out:
            return False, "the probe was not driven on --wrap; out tail: %s" % out[-400:]
        if "scratch hygiene (ADVISORY" not in out:
            return False, "the advisory label was not printed; out tail: %s" % out[-400:]
        if head_hash(root) == before:
            return False, "HEAD did not advance — the wrap commit did not land"
    with tempfile.TemporaryDirectory() as root2:
        env2 = build_fixture(root2, script_text, BANNER_PRIMARY)
        env2["STUB_SCRATCH_HYGIENE_EXIT"] = "1"
        rc2, out2 = run_commit(root2, env2, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc2 != 0:
            return False, "a non-wrap commit failed (exit %d); out tail: %s" % (rc2, out2[-400:])
        if "STUB _gate_scratch_hygiene.py" in out2:
            return False, "the probe ran on a NON-wrap commit — it is wrap-only by design"
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


def arm_mention_map_stale_regenerates_and_refuses(script_text):
    """#208 — the mention-map freshness gate (the [110] re-stale class, 3rd recurrence). A STALE
    map must be REGENERATED (announced, one path named) and then REFUSED, so the caller re-runs
    naming the path — regenerating silently would stage what nobody named (P5). Drives the stub
    non-zero so the gate is TESTED, not merely RUN [[green-tests-cannot-see-scope]]."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_MENTION_MAP_STALE"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "a STALE mention map did NOT block the commit"
        if "— mention map STALE — regenerating" not in out:
            return False, "the regeneration was not ANNOUNCED; out tail: %s" % out[-600:]
        if "STUB _build_graph_mention_map.py args=[] regenerate" not in out:
            return False, "the generator was never invoked in regenerate mode; out tail: %s" % out[-600:]
        if "MENTION-MAP GATE (#208" not in out or "knowledge/_graph-mention-map.json" not in out:
            return False, "the refusal did not NAME the gate and the path to add; out tail: %s" % out[-600:]
        if not staged_empty(root):
            return False, "staged despite the mention-map refusal — P5 violated"
        if head_hash(root) != before:
            return False, "HEAD advanced despite the mention-map refusal"
        # the generator's OWN refusal is a different, louder failure: it must not be swallowed.
        env2 = dict(env)
        env2["STUB_MENTION_MAP_REGEN_EXIT"] = "1"
        env2["STUB_MENTION_MAP_MARKER"] = os.path.join(root, ".git", "marker-2")
        rc2, out2 = run_commit(root, env2, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc2 == 0:
            return False, "a REFUSING generator did not block the commit"
        if "the mention-map generator itself REFUSED" not in out2:
            return False, "generator-refusal message missing; out tail: %s" % out2[-600:]
        # declared passes, silent fails: the ACK hatch lets the SAME stale map through, named.
        env["MENTION_MAP_ACK"] = "fixture-declared gap (#208 arm)"
        rc3, out3 = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc3 != 0:
            return False, "MENTION_MAP_ACK did not pass the stale gate (exit %d); out tail: %s" % (rc3, out3[-600:])
        if "mention-map gate: DECLARED GAP — fixture-declared gap (#208 arm)" not in out3:
            return False, "the declared gap was not NAMED in the output; out tail: %s" % out3[-600:]
        if head_hash(root) == before:
            return False, "commit did not land under the declared-gap hatch"
        return True, ""


def arm_mention_map_regenerated_not_staged(script_text):
    """#208 second half — a map that is FRESH on disk but differs from HEAD and was not named in
    the staged paths must block. That is the exact hole the three targeted [110] repairs fell
    through: green `--check` locally, OLD blob in the commit, red survey in CI."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        # fresh on disk (STALE=0), but modified relative to HEAD and NOT among STAGE_PATHS
        write(os.path.join(root, "knowledge", "_graph-mention-map.json"),
              '{"fixture": "mention map REGENERATED, not named"}\n')
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "an unstaged regenerated map did NOT block the commit"
        if "MENTION-MAP GATE (#208, second half)" not in out:
            return False, "second-half refusal message missing; out tail: %s" % out[-600:]
        if head_hash(root) != before:
            return False, "HEAD advanced despite the second-half refusal"
        # naming the path is the documented remedy — it must actually clear the gate.
        rc2, out2 = run_commit(root, env,
                               ["--reconciled", "msg.txt"] + STAGE_PATHS
                               + ["knowledge/_graph-mention-map.json"])
        if rc2 != 0:
            return False, ("naming the map path did NOT clear the second-half gate (exit %d); "
                           "out tail: %s" % (rc2, out2[-600:]))
        if "— mention map is either unchanged or staged" not in out2:
            return False, "the second-half assert did not report a pass; out tail: %s" % out2[-600:]
        if head_hash(root) == before:
            return False, "commit did not land once the map path was named"
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


# ---------------- W-355 (#238 lane M) — the post-wrap handoff DEADLOCK and its DECLARED form ----
# These arms run the REAL knowledge/_session.py (+ its _helpgate.py), NOT the STUB_SESSION_EXIT
# stub: the deadlock lives in the interplay of _session.py's R3 (handoff_max >= gm_title), the
# shell's SESSION_N / SESSION_ACK branches, and T3's s130-D3 refusal — a forced exit code cannot
# reproduce it [[mutation-tests-the-clause-not-the-feature]]. The fixture is the disk state a
# wrapped seat leaves behind: GM banner #238 with the TITLE line minting #239, _SESSIONS.jsonl
# carrying #238's boot AND wrap (so R2 is silent), a fake _CHAIN.md, and — the file under test —
# an untracked _HANDOFF-239-x.md named for staging. The CONTROL is the script with its two W-355
# blocks stripped (the pre-#238 shell): it must deadlock BOTH ways before the fix counts.

REAL_SESSION_PY = os.path.join(HERE, "_session.py")
REAL_HELPGATE_PY = os.path.join(HERE, "_helpgate.py")
W355_BANNER = ("> ## ★ LATEST — 2026-09-02 (Wed **#238**, FABLE sub — ✅ **W-355 FIXTURE**)\n\n"
               "**TITLE THE NEXT CHAT →** `#239 — next session`\n")
W355_HANDOFF = "_HANDOFF-239-x.md"
W355_ACK = "post-wrap handoff for #239 is the file being committed (W-355 declared form)"
W355_MSG_LINE1 = "post-wrap handoff for #239"
W355_MSG = W355_MSG_LINE1 + "\n\nbody: " + W355_ACK + "\n"
W355_MARK = {1: "# ── W-355 DECLARED FORM (1/2)", 2: "# ── W-355 DECLARED FORM (2/2)"}
W355_EXPECT_NONWRAP = "after #%s %s — " + W355_MSG_LINE1
W355_EXPECT_WRAP = "#238 2026-09-02 — ✅ **W-355 FIXTURE**"


def w355_strip(script_text, blocks=(1, 2)):
    """The script WITHOUT the named W-355 block(s). Each block runs from its marker comment to the
    first column-0 `fi` after it. Fails LOUD if a marker is missing or the strip left a trace."""
    for b in blocks:
        if W355_MARK[b] not in script_text:
            raise RuntimeError("mutation target not found — W-355 block %d marker moved: %r"
                               % (b, W355_MARK[b]))
    out, skipping = [], False
    for line in script_text.splitlines(keepends=True):
        if any(line.startswith(W355_MARK[b]) for b in blocks):
            skipping = True
        if skipping:
            if line.rstrip("\n") == "fi":
                skipping = False
            continue
        out.append(line)
    stripped = "".join(out)
    if 'if [ -n "${SESSION_N:-}" ]; then' not in stripped:
        raise RuntimeError("w355_strip ate the original session chain — the strip is wrong")
    if blocks == (1, 2) and "SESSION_N_HELD" in stripped:
        raise RuntimeError("w355_strip left SESSION_N_HELD behind — the strip is wrong")
    return stripped


def build_fixture_w355(root, script_text, handoff=True):
    """build_fixture + the REAL _session.py/_helpgate.py + post-wrap #238 disk state, committed,
    so the only dirty path is the handoff (when asked for). Returns env with NO session vars."""
    env = build_fixture(root, script_text, W355_BANNER)
    know = os.path.join(root, "knowledge")
    for src, dst in ((REAL_SESSION_PY, "_session.py"), (REAL_HELPGATE_PY, "_helpgate.py")):
        with open(src, encoding="utf-8") as f:
            write(os.path.join(know, dst), f.read())
    write(os.path.join(know, "_SESSIONS.jsonl"),
          '{"n": 238, "event": "boot", "ts": "2026-09-02T09:00:00"}\n'
          '{"n": 238, "event": "wrap", "ts": "2026-09-02T15:00:00"}\n')
    write(os.path.join(root, "_CHAIN.md"), "# _CHAIN.md (fixture) — routes the reader to #239\n")
    for cmd in (["git", "add", "-A"], ["git", "commit", "-q", "-m", "post-wrap state of #238"]):
        rc, out = sh(cmd, cwd=root)
        if rc != 0:
            raise RuntimeError("w355 fixture setup failed at %r: %s" % (cmd, out))
    if handoff:
        write(os.path.join(root, W355_HANDOFF), "# handoff for #239 (fixture)\n")
    write(os.path.join(root, "msg.txt"), W355_MSG)
    env.pop("SESSION_N", None)
    env.pop("SESSION_ACK", None)
    return env


def _w355_run(root, env, args, session_n=None, ack=None):
    e = dict(env)
    if session_n is not None:
        e["SESSION_N"] = str(session_n)
    if ack is not None:
        e["SESSION_ACK"] = ack
    return run_commit(root, e, args)


def arm_w355_deadlock_reproduced_on_unfixed_script(script_text):
    """CONTROL — the pre-#238 shell deadlocks BOTH ways. GREEN only if both halves are RED with
    their named causes and nothing moved: R3 with SESSION_N; T3 s130-D3 with SESSION_ACK alone."""
    unfixed = w355_strip(script_text)
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture_w355(root, unfixed)
        before = head_hash(root)
        rc1, out1 = _w355_run(root, env, ["--reconciled", "msg.txt", W355_HANDOFF], session_n=238)
        if rc1 == 0 or "R3 CHAIN OVERTAKEN" not in out1:
            return False, "half 1 (SESSION_N alone) did not refuse on R3; rc=%d tail: %s" % (rc1, out1[-400:])
        rc2, out2 = _w355_run(root, env, ["--reconciled", "msg.txt", W355_HANDOFF], ack=W355_ACK)
        if rc2 == 0 or "non-wrap commit with no SESSION_N" not in out2:
            return False, "half 2 (SESSION_ACK alone) did not refuse at T3; rc=%d tail: %s" % (rc2, out2[-400:])
        if head_hash(root) != before or not staged_empty(root):
            return False, "the deadlocked runs moved HEAD or left something staged"
        return True, "both halves RED: R3 with SESSION_N · T3 s130-D3 with SESSION_ACK alone"


def _w355_lands(script_text, session_n):
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture_w355(root, script_text)
        before = head_hash(root)
        rc, out = _w355_run(root, env, ["--reconciled", "msg.txt", W355_HANDOFF],
                            session_n=session_n, ack=W355_ACK)
        if rc != 0:
            return False, "exit %d; tail: %s" % (rc, out[-500:])
        if "R3 CHAIN OVERTAKEN" not in out or "DECLARED GAP" not in out:
            return False, "the covered refusal is not on the record; tail: %s" % out[-400:]
        if "W-355 declared form" not in out:
            return False, "the declared-form line did not print; tail: %s" % out[-400:]
        if head_hash(root) == before:
            return False, "HEAD did not advance"
        expect = W355_EXPECT_NONWRAP % (session_n, TODAY)
        subj = head_subject(root)
        if subj != expect:
            return False, "subject %r != %r" % (subj, expect)
        rc, names = sh(["git", "show", "--name-only", "--format=", "HEAD"], cwd=root)
        if W355_HANDOFF not in names:
            return False, "the handoff is not in the commit: %r" % names
        return True, ""


def arm_w355_declared_form_lands_from_wrapped_seat(script_text):
    """SESSION_N=238 (the seat that wrapped: declared == banner) + SESSION_ACK → the handoff commits."""
    return _w355_lands(script_text, 238)


def arm_w355_declared_form_lands_from_next_seat(script_text):
    """SESSION_N=239 (the next seat: declared == title) + SESSION_ACK → the same handoff commits."""
    return _w355_lands(script_text, 239)


def arm_w355_r3_still_refuses_without_ack(script_text):
    """The check is NOT removed: SESSION_N alone, handoff present → R3 refuses, nothing staged."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture_w355(root, script_text)
        before = head_hash(root)
        rc, out = _w355_run(root, env, ["--reconciled", "msg.txt", W355_HANDOFF], session_n=238)
        if rc == 0:
            return False, "SESSION_N alone LANDED over a real overtake — R3 has been removed"
        if "R3 CHAIN OVERTAKEN" not in out or "_session.py REFUSED for declared session #238" not in out:
            return False, "refusal cause not named; tail: %s" % out[-400:]
        if head_hash(root) != before or not staged_empty(root):
            return False, "HEAD moved or something staged despite the refusal"
        return True, ""


def arm_w355_declared_form_does_not_bypass_T3_wrap(script_text):
    """--wrap with SESSION_N=239 + SESSION_ACK, banner says #238 → the seam passes DECLARED, then
    T3's s130-D3 banner assertion still REFUSES. The declared form covers the witness, not T3."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture_w355(root, script_text)
        before = head_hash(root)
        rc, out = _w355_run(root, env, ["--reconciled", "--wrap", "msg.txt", W355_HANDOFF],
                            session_n=239, ack=W355_ACK)
        if rc == 0:
            return False, "a --wrap whose banner names another session LANDED under the declared form"
        if "DECLARED GAP" not in out:
            return False, "the seam did not pass declared first; tail: %s" % out[-400:]
        if "T3 REFUSES (s130-D3)" not in out or "banner says #238" not in out:
            return False, "T3's banner assertion did not fire; tail: %s" % out[-400:]
        if head_hash(root) != before:
            return False, "HEAD advanced"
        return True, ""


def arm_w355_wrap_with_next_handoff_lands(script_text):
    """--wrap with SESSION_N=238 + SESSION_ACK (the wrap itself carrying _HANDOFF-239) → lands,
    subject derived from the banner as before and verified against the declared session."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture_w355(root, script_text)
        before = head_hash(root)
        rc, out = _w355_run(root, env, ["--reconciled", "--wrap", "msg.txt", W355_HANDOFF],
                            session_n=238, ack=W355_ACK)
        if rc != 0:
            return False, "exit %d; tail: %s" % (rc, out[-500:])
        if head_hash(root) == before:
            return False, "HEAD did not advance"
        subj = head_subject(root)
        if subj != W355_EXPECT_WRAP:
            return False, "subject %r != %r" % (subj, W355_EXPECT_WRAP)
        return True, ""


def arm_w355_ordinary_commit_unaffected(script_text):
    """No handoff on disk, SESSION_N alone → the plain branch runs ("session witness agrees") and
    the commit lands: the addition changes nothing for a commit that never needed it."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture_w355(root, script_text, handoff=False)
        write(os.path.join(root, "work2.txt"), "ordinary dirty work\n")
        before = head_hash(root)
        rc, out = _w355_run(root, env, ["--reconciled", "msg.txt", "work2.txt"], session_n=238)
        if rc != 0:
            return False, "exit %d; tail: %s" % (rc, out[-500:])
        if "session witness agrees (#238)" not in out:
            return False, "the plain branch did not run; tail: %s" % out[-400:]
        if "W-355 declared form" in out:
            return False, "the declared-form line printed on a run that never set SESSION_ACK"
        if head_hash(root) == before:
            return False, "HEAD did not advance"
        return True, ""


def mutation_w355_declared_form_removed_bites(script_text):
    """Both W-355 blocks stripped → the landing arm must go RED (the fix is load-bearing)."""
    ok, detail = arm_w355_declared_form_lands_from_wrapped_seat(w355_strip(script_text))
    if ok:
        return False, "the landing arm stayed GREEN with the W-355 blocks stripped — harness cannot fail"
    return True, "went RED as required: %s" % detail[:160]


def mutation_w355_restore_removed_bites(script_text):
    """Only block (2/2) stripped → SESSION_N is never restored, T3 refuses the non-wrap commit:
    the restore half is load-bearing on its own, not decoration."""
    ok, detail = arm_w355_declared_form_lands_from_wrapped_seat(w355_strip(script_text, blocks=(2,)))
    if ok:
        return False, "the landing arm stayed GREEN with the restore block stripped — harness cannot fail"
    if "non-wrap commit with no SESSION_N" not in detail:
        return False, "went RED for the wrong reason (expected T3 s130-D3): %s" % detail[:200]
    return True, "went RED at T3 as required (SESSION_N never restored)"


# ---------------- #238 lane P — the polarity gate at the seam (s238-D7) ----------------------------

def arm_polarity_gate_refusal_and_ack(script_text):
    """s238-D7 (#238 lane P) — the polarity gate BLOCKS pre-stage when red, is SEEN to run on the
    happy path (with `--check`, the same argv the build step passes), and its POLARITY_ACK hatch
    passes the SAME red gate through DECLARED, named in the output. The stub is driven non-zero
    here so the gate is TESTED, not merely RUN [[green-tests-cannot-see-scope]]; the gate's own
    verdict honesty is proven by `_validate_polarities.py --selftest` (42 red arms), not here."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        before = head_hash(root)
        # 1 — SEEN to run, green, with --check, on an ordinary commit
        rc0, out0 = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc0 != 0:
            return False, "green polarity stub blocked the commit (exit %d); out tail: %s" % (rc0, out0[-400:])
        if "STUB _validate_polarities.py args=['--check']" not in out0:
            return False, "the gate was not invoked with --check on the happy path; out tail: %s" % out0[-400:]
        if "— polarity gate green" not in out0:
            return False, "polarity gate (s238-D7) did not announce itself on the happy path; out tail: %s" % out0[-400:]
        # 2 — RED blocks: nothing staged, HEAD unmoved, refusal NAMED
        write(os.path.join(root, "work.txt"), "second dirty edit\n")
        after_first = head_hash(root)
        env["STUB_POLARITY_EXIT"] = "1"
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "red polarity gate did NOT block the commit"
        if "polarity gate REFUSED (s238-D7)" not in out:
            return False, "polarity refusal message missing; out tail: %s" % out[-400:]
        if not staged_empty(root):
            return False, "staged despite the polarity refusal"
        if head_hash(root) != after_first:
            return False, "HEAD advanced despite the polarity refusal"
        # 3 — declared passes, silent fails: the ACK hatch lets the SAME red gate through, NAMED
        env["POLARITY_ACK"] = "fixture-declared gap (#238 lane P arm)"
        rc2, out2 = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc2 != 0:
            return False, "POLARITY_ACK did not pass the red gate (exit %d); out tail: %s" % (rc2, out2[-400:])
        if "polarity gate: DECLARED GAP — fixture-declared gap (#238 lane P arm)" not in out2:
            return False, "the declared gap was not NAMED in the output; out tail: %s" % out2[-400:]
        if "STUB _validate_polarities.py" in out2:
            return False, "the gate ran under the ACK hatch — the hatch must DECLARE, not re-ask"
        if head_hash(root) == after_first:
            return False, "commit did not land under the declared-gap hatch"
        if before == after_first:
            return False, "the first (green) commit did not land"
        return True, ""


def mutation_polarity_gate_block_removed(script_text):
    """The seam consumer can be deleted silently unless something bites: strip the polarity block
    from a COPY of the script and prove the arm goes RED (the gate is no longer a consumer of
    every commit — s238-D7's last sentence)."""
    marker = "# ── POLARITY GATE — s238-D7"
    if marker not in script_text:
        raise RuntimeError("mutation target not found — the polarity gate block marker moved")
    out, skipping = [], False
    for line in script_text.splitlines(keepends=True):
        if line.startswith(marker):
            skipping = True
        if skipping:
            if line.rstrip("\n") == "fi":
                skipping = False
            continue
        out.append(line)
    mutated = "".join(out)
    if "_validate_polarities.py" in mutated:
        raise RuntimeError("the strip left the polarity invocation behind — the mutation is wrong")
    ok, detail = arm_polarity_gate_refusal_and_ack(mutated)
    if ok:
        return False, "arm_polarity_gate_refusal_and_ack stayed GREEN with the seam block deleted — harness cannot fail"
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
    ("mention_map_stale_regenerates_and_refuses_208", arm_mention_map_stale_regenerates_and_refuses),
    ("mention_map_regenerated_not_staged_208", arm_mention_map_regenerated_not_staged),
    ("scratch_hygiene_advisory_on_wrap_228", arm_scratch_hygiene_advisory_on_wrap),
    ("harness_stub_coverage_W33", arm_harness_stub_coverage),
    ("MUTATION_harness_stub_detector_bites_W33", mutation_harness_stub_detector_bites),
    # #238 lane P — the polarity gate at the seam (s238-D7): driven red + hatch, and its block bites
    ("polarity_gate_refusal_and_ack_s238D7", arm_polarity_gate_refusal_and_ack),
    ("MUTATION_polarity_gate_block_removed_bites_s238D7", mutation_polarity_gate_block_removed),
    # W-355 (#238 lane M) — real _session.py in the fixture; control first, then the declared form
    ("w355_deadlock_reproduced_on_unfixed_script_CONTROL", arm_w355_deadlock_reproduced_on_unfixed_script),
    ("w355_declared_form_lands_from_wrapped_seat", arm_w355_declared_form_lands_from_wrapped_seat),
    ("w355_declared_form_lands_from_next_seat", arm_w355_declared_form_lands_from_next_seat),
    ("w355_r3_still_refuses_without_ack", arm_w355_r3_still_refuses_without_ack),
    ("w355_declared_form_does_not_bypass_T3_wrap", arm_w355_declared_form_does_not_bypass_T3_wrap),
    ("w355_wrap_with_next_handoff_lands", arm_w355_wrap_with_next_handoff_lands),
    ("w355_ordinary_commit_unaffected", arm_w355_ordinary_commit_unaffected),
    ("MUTATION_w355_declared_form_removed_bites", mutation_w355_declared_form_removed_bites),
    ("MUTATION_w355_restore_removed_bites", mutation_w355_restore_removed_bites),
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
