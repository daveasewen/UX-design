"""R1 lane 1c — the memento schematic's [125] re-stale class, closed at the commit seam.
Patches knowledge/_git_commit.sh (a freshness gate + a second-half assert, mirroring the #208
mention-map gate) and knowledge/_test_git_commit.py (stub, fixture file, happy-path assertions,
two arms, one mutation control). Idempotent. Usage: python3 door_schematic.py <repo>"""
import os, sys
repo = sys.argv[1]
SH = os.path.join(repo, "knowledge", "_git_commit.sh")
PY = os.path.join(repo, "knowledge", "_test_git_commit.py")

GATE = r'''
# ── MEMENTO-SCHEMATIC FRESHNESS GATE — CI survey step [125]'s re-stale class (#304 R1, lane 1c) ──
# ⛔ THE PREMISE THE BRIEF CARRIED, AND WHY IT WAS WRONG. The #304 plan asked for "the same
# head-only advance the chain got at c896bcaf". Probed at #304 R1 in a full-history clone of
# 571d458c: regenerate the schematic, COMMIT, re-ask `--check` → FRESH. A HEAD-only advance does
# NOT stale this file (it renders no sha). What staled it is CONTENT: every figure is read off
# disk at generation time (`_state.json` rows, `_rulings.json`, `_CHAIN.md` / GOOD-MORNING size,
# dossiers, the memento index, `_graph-mark-observations.jsonl`, the mention map), those move on
# nearly every commit, and NOTHING at the commit seam ever regenerated it — last regenerated at
# f81bbdd4 (2026-09-21), red in CI's survey on every push since. Softening `--check` to forgive
# figure drift would launder exactly the staleness the schematic exists to refuse (c896bcaf's own
# M1 bite: "REAL content staleness is STILL RED"). So the fix is the #208 mention-map precedent,
# at the one seam where staleness turns durable: regenerate, and never stage what was not named.
#
# OWNED REGION, WRITTEN DOWN BEFORE RUNNING THE GENERATOR [[do-not-rule-list-cannot-fence-a-generator]]:
#   `_gen_schematic.py` (no args) writes EXACTLY ONE path — OUT_REL,
#   reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html (`write()`, :1033); its other three
#   `open(..., "w")` sit inside `selftest()`'s TemporaryDirectory. It READS the mention map, so
#   this gate sits AFTER the mention-map gate: a stale map refuses first, and this asks next run.
# ONE DIFFERENCE FROM #208, BY DESIGN: a caller who ALREADY NAMED the schematic path (or passed
#   --all-dirty) has consented to staging it, so a regeneration rides with the commit instead of
#   costing a second full run of this script. Unnamed ⇒ REFUSED, exactly as #208 (P5 holds).
# EXIT 77 is the generator's own tier refusal (#193: this environment cannot reproduce the
#   committed page's token unit). It is NOT regenerated here — that would publish a weaker
#   instrument's figures under the committed tier's name — and it does not block: visible, named.
SCHEMATIC_PATH="reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html"
if [ -z "${SCHEMATIC_ACK:-}" ]; then
  python3 knowledge/_gen_schematic.py --check >/dev/null 2>&1
  _sch_rc=$?
  if [ "$_sch_rc" -eq 0 ]; then
    echo "— memento schematic fresh (_gen_schematic.py --check passed, #304 R1 [125] class gate)"
  elif [ "$_sch_rc" -eq 77 ]; then
    echo "— memento schematic COULD-NOT-ASK here (_gen_schematic.py --check exit 77, its tier refusal) — NOT regenerated, NOT blocking: a weaker instrument's figures are never published under the committed tier's name (#193)"
  else
    echo "— memento schematic STALE — regenerating the ONE file this generator writes:"
    python3 knowledge/_gen_schematic.py ||
      fail "the memento-schematic generator itself REFUSED (its named cause is printed above; it is the authority on it — this script does not second-guess it). Nothing has been staged."
    python3 knowledge/_gen_schematic.py --check >/dev/null 2>&1 ||
      fail "memento schematic STILL stale after a targeted regeneration — nondeterminism in the generator or a mid-flight input (another seat appending to an input it reads), NOT the ordinary re-stale class. Do not re-run blind; run python3 knowledge/_gen_schematic.py --check and read its diff. Nothing has been staged."
    _sch_named="$ALLDIRTY"
    for _q in "${PATHS[@]}"; do [ "$_q" = "$SCHEMATIC_PATH" ] && _sch_named=1; done
    if [ "$_sch_named" -eq 1 ]; then
      echo "— memento schematic REGENERATED just now and already among your named paths ($SCHEMATIC_PATH) — it rides with this commit"
    else
      fail "MEMENTO-SCHEMATIC GATE (#304 R1, CI survey step [125]'s re-stale class): the schematic was stale and has been REGENERATED just now — $SCHEMATIC_PATH. It is NOT staged, because this script never stages a path you did not name (P5, ruled 2026-08-02). Re-run this exact command with that path appended to your list. Nothing has been staged by this run."
    fi
  fi
else
  echo "— memento-schematic gate: DECLARED GAP — $SCHEMATIC_ACK"
fi
'''

HALF2 = r'''
# ── MEMENTO-SCHEMATIC GATE, SECOND HALF: REGENERATED-BUT-NOT-STAGED (#304 R1) ─────────────────
# Same argument as the mention map's second half above: fresh on DISK is not fresh in the COMMIT
# under explicit-path staging. A schematic that differs from HEAD and is not staged means CI's
# survey reads the OLD blob against the NEW corpus. ⚠ Residual, declared: an INPUT the schematic
# counts (e.g. knowledge/_graph-mark-observations.jsonl, appended by every memento search) left
# dirty and unnamed is rendered into the staged schematic but not committed — name it too.
# Unconditional, as #208's second half is: SCHEMATIC_ACK passes a STALE schematic, never an
# unstaged regenerated one.
if ! git diff --quiet -- "$SCHEMATIC_PATH" 2>/dev/null; then
  fail "MEMENTO-SCHEMATIC GATE (#304 R1, second half): '$SCHEMATIC_PATH' differs from HEAD and is NOT staged — the commit would carry the OLD schematic against a NEW corpus, which is exactly what CI's survey step [125] reads. Append '$SCHEMATIC_PATH' to your named paths and re-run. Nothing has been committed."
fi
echo "— memento schematic is either unchanged or staged (#304 R1 [125] second-half assert)"
'''

s = open(SH, encoding="utf-8").read()
if "MEMENTO-SCHEMATIC FRESHNESS GATE" not in s:
    anchor = '  echo "— mention-map gate: DECLARED GAP — $MENTION_MAP_ACK"\nfi\n'
    assert s.count(anchor) == 1, "mention-map gate anchor not unique"
    s = s.replace(anchor, anchor + GATE, 1)
    anchor2 = 'echo "— mention map is either unchanged or staged (#208 [110] second-half assert)"\n'
    assert s.count(anchor2) == 1
    s = s.replace(anchor2, anchor2 + HALF2, 1)
    open(SH, "w", encoding="utf-8").write(s)
    print("patched _git_commit.sh")
else:
    print("_git_commit.sh already patched")

t = open(PY, encoding="utf-8").read()
if "STUB_SCHEMATIC" in t:
    print("_test_git_commit.py already patched"); sys.exit(0)

STUB = r"""
# #304 R1 — the memento-schematic gate is the #208 shape exactly (one generator, two modes, the
# second changes the first's answer), so its stub is the mention-map stub's twin with its own
# variables; STUB_SCHEMATIC_CHECK_EXIT lets an arm drive the #193 tier refusal (77) directly.
STUB_SCHEMATIC = '''#!/usr/bin/env python3
import os, sys
marker = os.environ["STUB_SCHEMATIC_MARKER"]
regen_exit = os.environ.get("STUB_SCHEMATIC_REGEN_EXIT", "0")
check_exit = os.environ.get("STUB_SCHEMATIC_CHECK_EXIT", "")
stale = os.environ.get("STUB_SCHEMATIC_STALE", "0") == "1"
if "--check" in sys.argv[1:]:
    if check_exit:
        print("STUB _gen_schematic.py args=%r forced exit=%s" % (sys.argv[1:], check_exit))
        sys.exit(int(check_exit))
    fresh = (not stale) or os.path.exists(marker)
    print("STUB _gen_schematic.py args=%r fresh=%s" % (sys.argv[1:], fresh))
    sys.exit(0 if fresh else 1)
print("STUB _gen_schematic.py args=%r regenerate exit=%s" % (sys.argv[1:], regen_exit))
if regen_exit == "0":
    open(marker, "w").close()
    p = os.path.join("reviews", "MEMENTO-SCHEMATIC-2026-08-07-v2.html")
    with open(p, "w") as f:
        f.write("<p>schematic REGENERATED by the stub</p>\\n")
sys.exit(int(regen_exit))
'''
"""
a = "FAKE_TIKTOKEN = '''class _Enc:"
assert t.count(a) == 1
t = t.replace(a, STUB.lstrip("\n") + "\n" + a, 1)

a = '    write(os.path.join(know, "_build_graph_mention_map.py"), STUB_MENTION_MAP)\n'
assert t.count(a) == 1
t = t.replace(a, a + '    # #304 R1 — the memento-schematic gate, wired in the SAME edit as its stub (no sixth blind-harness).\n'
                     '    write(os.path.join(know, "_gen_schematic.py"), STUB_SCHEMATIC)\n', 1)

a = '    write(os.path.join(know, "_graph-mention-map.json"), \'{"fixture": "mention map at HEAD"}\\n\')\n'
assert t.count(a) == 1, "map fixture anchor"
t = t.replace(a, a + '    write(os.path.join(root, "reviews", "MEMENTO-SCHEMATIC-2026-08-07-v2.html"), "<p>schematic at HEAD</p>\\n")\n', 1)

a = '        "STUB_MENTION_MAP_MARKER": os.path.join(root, ".git", "stub-mention-map-regenerated"),\n'
assert t.count(a) == 1
t = t.replace(a, a + '        "STUB_SCHEMATIC_STALE": "0",\n        "STUB_SCHEMATIC_REGEN_EXIT": "0",\n'
                     '        "STUB_SCHEMATIC_MARKER": os.path.join(root, ".git", "stub-schematic-regenerated"),\n', 1)

a = '''        if "— mention map is either unchanged or staged" not in out:
            return False, "mention-map second-half assert (#208) did not run on the happy path; out tail: %s" % out[-400:]
'''
assert t.count(a) == 1
t = t.replace(a, a + '''        # #304 R1 — the memento-schematic gate's two halves, SEEN to run on the happy path.
        if "— memento schematic fresh" not in out:
            return False, "memento-schematic freshness gate (#304 R1) did not run on the happy path; out tail: %s" % out[-400:]
        if "— memento schematic is either unchanged or staged" not in out:
            return False, "memento-schematic second-half assert (#304 R1) did not run on the happy path; out tail: %s" % out[-400:]
''', 1)

ARMS = r'''

SCHEMATIC_REL = "reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html"


def arm_schematic_stale_regenerates_and_refuses(script_text):
    """#304 R1 — CI survey step [125]'s re-stale class. A STALE schematic must be REGENERATED
    (announced) and, when its path was NOT named, REFUSED with the path to add (P5). When the path
    WAS named, the regeneration rides with the commit in ONE run. A refusing generator blocks. A
    77 tier refusal neither regenerates nor blocks. SCHEMATIC_ACK passes a stale one, named."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        env["STUB_SCHEMATIC_STALE"] = "1"
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "a STALE schematic with its path UNNAMED did NOT block the commit"
        if "— memento schematic STALE — regenerating" not in out:
            return False, "the regeneration was not ANNOUNCED; out tail: %s" % out[-600:]
        if "STUB _gen_schematic.py args=[] regenerate" not in out:
            return False, "the generator was never invoked in regenerate mode; out tail: %s" % out[-600:]
        if "MEMENTO-SCHEMATIC GATE (#304 R1" not in out or SCHEMATIC_REL not in out:
            return False, "the refusal did not NAME the gate and the path to add; out tail: %s" % out[-600:]
        if not staged_empty(root):
            return False, "staged despite the schematic refusal — P5 violated"
        if head_hash(root) != before:
            return False, "HEAD advanced despite the schematic refusal"
        # the generator's OWN refusal must not be swallowed
        env2 = dict(env)
        env2["STUB_SCHEMATIC_REGEN_EXIT"] = "1"
        env2["STUB_SCHEMATIC_MARKER"] = os.path.join(root, ".git", "schematic-marker-2")
        rc2, out2 = run_commit(root, env2, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc2 == 0:
            return False, "a REFUSING schematic generator did not block the commit"
        if "the memento-schematic generator itself REFUSED" not in out2:
            return False, "generator-refusal message missing; out tail: %s" % out2[-600:]
        # 77 = the tier refusal: visible, not regenerated, not blocking (the first run's
        # regeneration is put back first, so the second half is not what this sub-case asks)
        sh(["git", "checkout", "-q", "--", SCHEMATIC_REL], cwd=root)
        env4 = dict(env)
        env4["STUB_SCHEMATIC_CHECK_EXIT"] = "77"
        env4["STUB_SCHEMATIC_MARKER"] = os.path.join(root, ".git", "schematic-marker-4")
        rc4, out4 = run_commit(root, env4, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc4 != 0:
            return False, "a 77 tier refusal BLOCKED the commit (exit %d); out tail: %s" % (rc4, out4[-600:])
        if "memento schematic COULD-NOT-ASK here" not in out4 or "regenerate exit" in out4:
            return False, "a 77 was not declared, or it regenerated; out tail: %s" % out4[-600:]
        before = head_hash(root)
        # named in advance ⇒ one run: regenerated, staged, committed
        env3 = dict(env)
        env3["STUB_SCHEMATIC_MARKER"] = os.path.join(root, ".git", "schematic-marker-3")
        write(os.path.join(root, "work.txt"), "more dirty work\n")
        rc3, out3 = run_commit(root, env3, ["--reconciled", "msg.txt"] + STAGE_PATHS + [SCHEMATIC_REL])
        if rc3 != 0:
            return False, "a NAMED stale schematic did not ride with the commit (exit %d); out tail: %s" % (rc3, out3[-600:])
        if "already among your named paths" not in out3:
            return False, "the named-path branch was not reported; out tail: %s" % out3[-600:]
        if head_hash(root) == before:
            return False, "commit did not land with the schematic path named"
        # declared passes, silent fails
        before = head_hash(root)
        env5 = dict(env)
        env5["STUB_SCHEMATIC_MARKER"] = os.path.join(root, ".git", "schematic-marker-5")
        env5["SCHEMATIC_ACK"] = "fixture-declared gap (#304 R1 arm)"
        write(os.path.join(root, "work.txt"), "yet more dirty work\n")
        rc5, out5 = run_commit(root, env5, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc5 != 0:
            return False, "SCHEMATIC_ACK did not pass the stale gate (exit %d); out tail: %s" % (rc5, out5[-600:])
        if "memento-schematic gate: DECLARED GAP — fixture-declared gap (#304 R1 arm)" not in out5:
            return False, "the declared gap was not NAMED; out tail: %s" % out5[-600:]
        if head_hash(root) == before:
            return False, "commit did not land under the declared-gap hatch"
        return True, ""


def arm_schematic_regenerated_not_staged(script_text):
    """#304 R1 second half — a schematic FRESH on disk but differing from HEAD and not staged must
    block; naming it clears the gate."""
    with tempfile.TemporaryDirectory() as root:
        env = build_fixture(root, script_text, BANNER_PRIMARY)
        write(os.path.join(root, SCHEMATIC_REL), "<p>schematic REGENERATED, not named</p>\n")
        before = head_hash(root)
        rc, out = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS)
        if rc == 0:
            return False, "an unstaged regenerated schematic did NOT block the commit"
        if "MEMENTO-SCHEMATIC GATE (#304 R1, second half)" not in out:
            return False, "second-half refusal message missing; out tail: %s" % out[-600:]
        if head_hash(root) != before:
            return False, "HEAD advanced despite the second-half refusal"
        rc2, out2 = run_commit(root, env, ["--reconciled", "msg.txt"] + STAGE_PATHS + [SCHEMATIC_REL])
        if rc2 != 0:
            return False, "naming the schematic did NOT clear the second-half gate (exit %d); out tail: %s" % (rc2, out2[-600:])
        if "— memento schematic is either unchanged or staged" not in out2:
            return False, "the second-half assert did not report a pass; out tail: %s" % out2[-600:]
        if head_hash(root) == before:
            return False, "commit did not land once the schematic path was named"
        return True, ""


def mutation_schematic_gate_removed_bites(script_text):
    """MUTATION — delete the freshness gate's regenerate-and-refuse line; the stale arm must go RED."""
    needle = 'fail "MEMENTO-SCHEMATIC GATE (#304 R1, CI survey step [125]'
    if needle not in script_text:
        raise RuntimeError("mutation anchor missing — the gate's refusal text changed")
    mutated = "\n".join(("      true  # MUTATED" if needle in ln else ln) for ln in script_text.split("\n"))
    ok, detail = arm_schematic_stale_regenerates_and_refuses(mutated)
    if ok:
        return False, "arm_schematic_stale_regenerates_and_refuses stayed GREEN with the refusal deleted — harness cannot fail"
    return True, "went RED as required: %s" % detail


def mutation_schematic_second_half_removed_bites(script_text):
    """MUTATION — delete the second-half fail; the not-staged arm must go RED."""
    needle = 'fail "MEMENTO-SCHEMATIC GATE (#304 R1, second half)'
    if needle not in script_text:
        raise RuntimeError("mutation anchor missing — the second-half refusal text changed")
    mutated = "\n".join(("    true  # MUTATED" if needle in ln else ln) for ln in script_text.split("\n"))
    ok, detail = arm_schematic_regenerated_not_staged(mutated)
    if ok:
        return False, "arm_schematic_regenerated_not_staged stayed GREEN with the second half deleted — harness cannot fail"
    return True, "went RED as required: %s" % detail
'''
a = "\n\nARMS = [\n"
assert t.count(a) == 1
t = t.replace(a, ARMS + a, 1)
a = '    ("mention_map_regenerated_not_staged_208", arm_mention_map_regenerated_not_staged),\n'
assert t.count(a) == 1
t = t.replace(a, a + '    # #304 R1 — the memento-schematic gate ([125] re-stale class): driven, hatched, and mutation-bitten\n'
                     '    ("schematic_stale_regenerates_and_refuses_304R1", arm_schematic_stale_regenerates_and_refuses),\n'
                     '    ("schematic_regenerated_not_staged_304R1", arm_schematic_regenerated_not_staged),\n'
                     '    ("MUTATION_schematic_gate_removed_bites_304R1", mutation_schematic_gate_removed_bites),\n'
                     '    ("MUTATION_schematic_second_half_removed_bites_304R1", mutation_schematic_second_half_removed_bites),\n', 1)
open(PY, "w", encoding="utf-8").write(t)
print("patched _test_git_commit.py")
