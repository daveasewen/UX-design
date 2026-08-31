#!/usr/bin/env python3
"""Wiring gate (#119, bucket D) — every gate script on disk must be WIRED or EXEMPT.

#118's finding: building an instrument is gated; WIRING it is not. A validator can be
written, reviewed, committed, remembered, and cited in memory without ever entering
`_build_all.py`'s STEPS — four orphans on disk proved it, each unwired for a different
reason. This gate closes that seam: it fails LOUD, naming the orphan, the moment a
gate script lands on disk with nothing running it and no named exemption.

⛔ #221 WIDENED BOTH HALVES OF THAT SENTENCE, and the old wording is kept here in the
correction rather than smoothed away, because this file is what a reader consults when the
gate is green. It used to say "every `_validate_*.py`" and "no STEPS entry", and BOTH were
narrower than the repo:
  * POPULATION — now `_validate_*.py` AND `_gate_*.py`. #220-L1 finding 8 measured this gate
    reporting `43 validator(s) · 0 failure(s)` while three `_gate_*.py` files sat outside its
    glob entirely, one of them a genuine orphan. [[gate-glob-scope-rule]]
  * WIRED — now four named surfaces, not one: `_build_all.STEPS`, `_git_commit.sh` (the commit
    seam), `.github/workflows/gates.yml`, and a DECLARED-AND-VERIFIED arm (`ARM_OF`).
⚠ The counts this gate prints are therefore not comparable to a pre-#221 run. That is the
point: the old number was a smaller question.

Exemptions are EXPLICIT and NAMED in EXEMPT below — each carries a reason and a date.
An exemption for a file that IS wired, or that does not exist, is itself a FAIL
(a stale exemption is the same rot class as a stale constant). Same for `ARM_OF`, whose
every clause is re-verified on every run.

Unit note: this gate COUNTS presence, it does not measure. A count finds orphans;
only RUNNING them sorts oversight from rot (#118). This gate's job is only the seam.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re
import sys
from pathlib import Path

# #230 F6 — the ruled third verdict, from its one home. `_could_not_ask.py` sits beside this file
# in `knowledge/` and SHIPS in the pack (it is in the gates group's helper closure), so this
# import resolves on both sides of the release boundary.
import _could_not_ask as cna  # noqa: E402 - after the help gate's path insert, by necessity

HERE = Path(__file__).resolve().parent
BUILD = HERE / "_build_all.py"
SELF = "_validate_wiring.py"

# ⛔ #221 — TWO CAUSES, FROM #220-L1 FINDING 8. This gate reported `43 validator(s) on disk ·
# 42 wired · 1 exempt · 0 failure(s)` and rc=0, and BOTH halves of that green were a function
# of what it was allowed to look at [[gate-glob-scope-rule]].
#   ① ITS POPULATION WAS ONE NAMESPACE. `HERE.glob("_validate_*.py")` — so the five
#      `_gate_*.py` files in this same directory were not merely passing, they were never
#      ASKED. The anti-orphan gate could not see the namespace where today's orphans live, and
#      #118's class — *"building an instrument is gated; WIRING it is not"* — was unpoliced in
#      the newer naming convention from the day that convention was invented.
#   ② ITS DEFINITION OF "WIRED" WAS ONE SURFACE. `_build_all.STEPS` was the only consumer this
#      repo had at #119. It now has three more, and each of them RUNS a script for real:
#      `_git_commit.sh` (the commit seam — `s133-D2` makes it the only push path),
#      `.github/workflows/gates.yml` (CI), and being an ARM imported by an already-wired script
#      (`_gate_harness_stubs.py` is `_test_git_commit.py`'s detector, by its own comment: *"the
#      detector below (_gate_harness_stubs.py) exists as an ARM, not a reminder"*). Calling
#      those orphans would have been as false as calling them wired — a gate that names a
#      commit-seam gate an orphan teaches its readers to add exemptions.
# ⚠ THE ARM SURFACE IS ONE LEVEL DEEP, ON PURPOSE. An import only counts as wiring if the
# IMPORTER is itself wired by a direct surface. A transitive closure would let any two unwired
# scripts import each other into legitimacy, which is laundering with extra steps — bitten
# below, in the direction that matters (bite 8).
COMMIT_SH = HERE / "_git_commit.sh"
CI_YML = HERE.parent / ".github" / "workflows" / "gates.yml"
POPULATION_GLOBS = ("_validate_*.py", "_gate_*.py")

# name -> (reason, date). May only shrink without a new declared reason.
EXEMPT: dict[str, tuple[str, str]] = {
    # _validate_screen.py UN-EXEMPTED #120 — the #118 "ROTTED" verdict was a drifted
    # a11y.check() call signature; repaired, bite-tested, WIRED in _build_all.py same pass.
    # _validate_state_contrast.py UN-EXEMPTED #125 (s125-D2, Dave). Its reason claimed the
    # chromium download was "blocked by sandbox TLS (UNABLE_TO_GET_ISSUER_CERT_LOCALLY on all
    # 3 CDNs)". DISPROVEN by direct observation, not by argument: _RUNBOOK-render-verify.md was
    # followed literally and the download SUCCEEDED (chromium_headless_shell-1234 in the cache),
    # chromium launched, and the validator ran and produced output. The installer's non-zero
    # exit is the __dirlock EPERM the runbook banks as "a failure message AFTER a success" —
    # the original diagnosis read that exit as a refusal. ⇒ an environmental fence is verified
    # against the thing itself, never carried forward from a prior session's banner.
    # EMPTY IS A LEGITIMATE STATE: selftest bites 3+4 use a SYNTHETIC exemption so they keep
    # biting with no real entries here — a bite that needs a real exemption to exist is a bite
    # that can silently stop existing.
    "_validate_descender_computed.py": (
        "G2 render leg (#215, row W-101): drives real pages in headless chromium and reads "
        "getComputedStyle — needs a STAGED BROWSER, which _build_all.py's environment does not "
        "guarantee. Wiring it would make the build red on an ENVIRONMENT fact dressed as an "
        "artefact verdict (#173/#183 class). It runs on demand: "
        "`python3 knowledge/_validate_descender_clip.py --computed`, proof-of-record wherever "
        "chromium is staged. ⚠ Re-visit if the render job ever gains a knowledge-gate step.",
        "2026-08-22",
    ),
    # #221, from #220-L1 finding 15. This is the FIRST entry this gate has ever carried for the
    # `_gate_*.py` namespace, and it exists because widening the population (above) made a real
    # orphan visible — which is the gate working, not the gate being appeased.
    "_gate_pack_imports.py": (
        "Built #219 and WIRED NOWHERE — not in _build_all.STEPS, not in gates.yml, not at the "
        "commit seam (#220-L1 finding 15, re-measured at #221 HEAD: 0 references in all three). "
        "Its known-answer test DOES fire — driven against the frozen v1.0.0 zip it reports the "
        "exact ImportError the release shipped — so this is not rot, it is an instrument waiting "
        "on a decision. ⬛ WIRING IT IS DAVE'S (#220-L1 ruling-shaped Q4: advisory-and-wired is a "
        "different state from advisory-and-unwired, and only the first can ever tell you "
        "anything). It is ALSO deliberately fenced out of the pack's own gate roster "
        "(`_gen_pack_manifest.RELEASE_SIDE_GATES`) so the ruled 55 does not move, which is why "
        "shipping it is not the answer either. ⚠ EXPIRES ON HIS WORD: wire it and bite 3 above "
        "turns this entry into a STALE EXEMPTION failure by itself.",
        "2026-08-27",
    ),
}


def population() -> list[str]:
    """Every gate script on disk, across BOTH naming conventions (#221)."""
    names: set[str] = set()
    for g in POPULATION_GLOBS:
        names |= {p.name for p in HERE.glob(g)}
    return sorted(names)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ★★ #230 F6 — THE PACK-CONTEXT REFUSAL. THIS GATE GRADES THE SOURCE REPO'S WIRING, AND AN
# INSTALLED PACK HAS NONE OF IT.
#
# WHAT WAS MEASURED (#230 rehearsal, F6). A pristine `Apollo-Spider-v1.0.5` unzip, running the
# command the design contract itself ends on — `python3 ci-template/run-gates.py` — printed
# `37 pass · 1 FAIL` and exited 1. The single FAIL was this gate, and every one of its 25
# findings was the same fact said 25 ways: `⛔ ORPHAN: _validate_grid.py exists on disk and
# NOTHING RUNS IT` (×23), plus a DANGLING EXEMPTION and a DANGLING ARM for two files the pack
# does not ship. Nothing was wrong with the pack. The gate was reading `_build_all.STEPS`,
# `_git_commit.sh` and `gates.yml` — three files that exist ONLY in the design system's own
# repo — finding all three empty via `read()`'s `else ""`, and concluding that 23 correctly
# shipped gates were orphans.
#
# ⛔ THIS IS #173 EXACTLY — "a gate that CANNOT PASS in one environment"
# [[gate-cannot-pass-in-one-environment]] — and it was shipping as RUNNABLE. `read()`'s empty
# string is a silent WIDENING: absent wiring text is indistinguishable from wiring text that
# names nothing, so the gate went confidently red about a question it had not been able to ask.
#
# THE FIX IS THE CONDITION, NOT THE INSTANCE [[gate-dont-patch]]. The gate does not ask "am I in
# a pack" and it does not read an env var — that would be the #173 lie in a new shape, and
# `_could_not_ask.py`'s own docstring forbids it by name. It asks the only honest question:
# CAN I REACH ANY WIRING SURFACE AT ALL? If every one of them is absent, the population on disk
# cannot be graded against anything, and the honest verdict is the ruled third one — exit 77,
# `COULD-NOT-ASK:`, the missing input named. If even ONE surface is readable the gate grades
# normally, so the repo run is untouched and a repo that lost its `gates.yml` still goes
# LOUDER (bite 9), never quieter.
#
# ⚠ AND IT MUST STILL BITE. A refusal that swallowed the gate's purpose would be worse than the
# red it cures, so this arm is mutation-proven in BOTH directions — bites 10 and 10b below.
#
# ⚠ THE DOWNSTREAM CONSEQUENCE, STATED: `_gen_pack_manifest.classify()` puts an exit-77 refusal
# that names an unshipped repo path into REPO-BOUND (s223-D5 clause 1, narrowed at s223-D6), and
# REPO-BOUND gates DO NOT SHIP. So at the next `--manifest` probe this gate stops riding in the
# pack at all, which is where it always belonged. Until that re-probe the shipped manifest still
# lists it RUNNABLE, and `ci-template/run-gates.py` counts the 77 as a could-not-ask and prints
# it in full — loud, never a silent pass.
WIRING_SURFACES = (("knowledge/_build_all.py", lambda: BUILD),
                   ("knowledge/_git_commit.sh", lambda: COMMIT_SH),
                   (".github/workflows/gates.yml", lambda: CI_YML))


def reachable_surfaces() -> list[str]:
    """The wiring surfaces this run can actually READ. Empty means the question is unaskable."""
    return [label for label, get in WIRING_SURFACES if get().exists()]


# ⛔ AN IMPORT IS NOT AN INVOCATION — AND THIS GATE PROVED IT ON ITS AUTHOR, MID-REPAIR.
# #221's first cut derived the ARM surface automatically: any gate imported by a wired script
# counted as wired. Driven on the real tree it immediately promoted
# `_validate_descender_computed.py` to "wired" and then correctly fired `STALE EXEMPTION` on
# it — because `_validate_descender_clip.py` (wired) imports it but only REACHES it under
# `--computed`, which the wired invocation does not pass. The automatic rule could not tell
# "is on the import graph" from "is actually run", and the exemption it would have dissolved is
# a real #173 fence protecting the build from a browser it does not have.
# ⇒ AN INDIRECT CONSUMER IS DECLARED BY NAME, AND THE DECLARATION IS THEN VERIFIED. Explicit
# like `EXEMPT`, but stronger: an entry here asserts a mechanical fact (the importer exists, is
# wired by a direct surface, and does import this module) and every clause is checked on every
# run, so the declaration cannot rot into a lie. Laundering is impossible by construction —
# naming an unwired importer FAILS.
ARM_OF: dict[str, tuple[str, str, str]] = {
    "_gate_harness_stubs.py": (
        "_test_git_commit.py",
        "W-33 (#192) — the detector's consumer, and the consumer says so in its own words at "
        "`_test_git_commit.py:158`: \"the detector below (_gate_harness_stubs.py) exists as an "
        "ARM, not a reminder\". It is imported and CALLED unconditionally in that file's default "
        "run (`:791` `import _gate_harness_stubs`, `:793` `_gate_harness_stubs.unstubbed()`), "
        "and `_test_git_commit.py --selftest` is wired at `_build_all.py:131`.",
        "2026-08-27",
    ),
}


def arm_failures(build_text: str, commit_text: str, ci_text: str, disk: list[str],
                 arm_map: dict[str, tuple[str, str, str]] | None = None) -> list[str]:
    """Verify every declared indirect consumer. Returns failure strings."""
    arm_map = ARM_OF if arm_map is None else arm_map
    out = []
    for name, (importer, _why, when) in sorted(arm_map.items()):
        if name not in disk:
            out.append(f"DANGLING ARM: {name} is declared an arm of {importer} but is not on disk.")
            continue
        text = read(HERE / importer)
        if not text:
            out.append(f"BROKEN ARM: {name}'s declared consumer {importer} is not on disk.")
            continue
        importer_wired = (re.search(r'["\']' + re.escape(importer) + r'["\']', build_text)
                          or re.search(re.escape(importer), commit_text)
                          or re.search(re.escape(importer), ci_text))
        if not importer_wired:
            out.append(f"LAUNDERED ARM: {name} is declared an arm of {importer}, but {importer} "
                       f"is ITSELF unwired. An unwired script cannot wire another one.")
        if not re.search(r'(?m)^\s*(?:import|from)\s+' + re.escape(name[:-3]) + r'\b', text):
            out.append(f"STALE ARM [{when}]: {importer} does not import {name} any more. "
                       f"Re-check the claim or remove the declaration.")
    return out


def arm_names(arm_map: dict[str, tuple[str, str, str]] | None = None) -> set[str]:
    return set((ARM_OF if arm_map is None else arm_map).keys())


def check(build_text: str, disk: list[str],
          exempt_map: dict[str, tuple[str, str]] | None = None,
          commit_text: str = "", ci_text: str = "",
          arms: set[str] | None = None) -> list[str]:
    """Return failure strings. Pure so the selftest can bite it.

    `exempt_map` defaults to the module's EXEMPT; passing it explicitly is what lets the
    selftest bite the exemption clauses with a SYNTHETIC entry instead of borrowing a real
    one (#125 — EXEMPT is legitimately empty now, and `next(iter(EXEMPT))` would have raised).

    ⚠ #221: `commit_text` / `ci_text` / `arms` default to EMPTY, deliberately. A caller that
    forgets them gets the OLD, narrower reading — which fails LOUD (more orphans) rather than
    quiet (more greens). A default that widened silently would be the false-green shape this
    whole repair is about.
    """
    exempt_map = EXEMPT if exempt_map is None else exempt_map
    arms = set() if arms is None else arms
    fails = []
    for name in sorted(disk):
        wired = (re.search(r'["\']' + re.escape(name) + r'["\']', build_text)
                 or re.search(re.escape(name), commit_text)
                 or re.search(re.escape(name), ci_text)
                 or name in arms)
        is_exempt = name in exempt_map
        if name == SELF:
            # the wiring gate itself must be wired — an unwired wiring gate is a joke
            if not wired:
                fails.append(f"ORPHAN (the gate itself): {name} has no STEPS entry in _build_all.py")
            continue
        if not wired and not is_exempt:
            fails.append(f"ORPHAN: {name} exists on disk and NOTHING RUNS IT — no _build_all.STEPS "
                         f"entry, no _git_commit.sh invocation, no gates.yml step, not an arm of a "
                         f"wired script, and no named exemption. Wire it or exempt it BY NAME with "
                         f"a reason and a date.")
        if wired and is_exempt:
            fails.append(f"STALE EXEMPTION: {name} is wired AND exempt "
                         f"({exempt_map[name][0]!r}, {exempt_map[name][1]}). Remove the exemption.")
    for name in exempt_map:
        if name not in disk:
            fails.append(f"DANGLING EXEMPTION: {name} is exempt but not on disk. Remove it.")
    return fails


def run() -> int:
    # #230 F6 — the pack-context refusal. See WIRING_SURFACES above for the measurement.
    if not reachable_surfaces():
        return cna.refuse(
            SELF,
            "knowledge/_build_all.py does not exist here, and neither does "
            "knowledge/_git_commit.sh nor .github/workflows/gates.yml. All three are the WIRING "
            "SURFACES this gate grades, they exist only in the design system's own source repo, "
            "and an installed pack does not carry them. Without one of them every gate on disk "
            "reads as an ORPHAN, which would be a confident verdict about a question that was "
            "never asked. Run this gate from the source repo, where the proof is reachable.")
    build_text, commit_text, ci_text = read(BUILD), read(COMMIT_SH), read(CI_YML)
    disk = population()
    arms = arm_names()
    fails = (check(build_text, disk, None, commit_text, ci_text, arms)
             + arm_failures(build_text, commit_text, ci_text, disk))
    by = {"_build_all.STEPS": 0, "_git_commit.sh": 0, "gates.yml": 0, "arm-of-a-wired-script": 0}
    for n in disk:
        if re.search(r'["\']' + re.escape(n) + r'["\']', build_text):
            by["_build_all.STEPS"] += 1
        elif re.search(re.escape(n), commit_text):
            by["_git_commit.sh"] += 1
        elif re.search(re.escape(n), ci_text):
            by["gates.yml"] += 1
        elif n in arms:
            by["arm-of-a-wired-script"] += 1
    n_validate = sum(1 for n in disk if n.startswith("_validate_"))
    print(f"wiring gate: {len(disk)} gate script(s) on disk "
          f"({n_validate} _validate_* · {len(disk) - n_validate} _gate_*, #221 widened) · "
          f"{sum(by.values())} wired · {len(EXEMPT)} exempt by name · {len(fails)} failure(s)")
    print("  wired by surface: " + " · ".join(f"{k} {v}" for k, v in by.items()))
    for name, (importer, _why, when) in sorted(ARM_OF.items()):
        print(f"  ⬛ ARM (declared + verified): {name} is run by {importer} [{when}]")
    # ⚠ EXEMPTIONS ARE PRINTED, NEVER SILENT. An exemption that only lives in source is a
    # green with a footnote nobody reads; this is the same posture `_build_survey.py` takes
    # with COULD-NOT-ASK, for the same reason.
    for name, (why, when) in sorted(EXEMPT.items()):
        print(f"  ⬛ EXEMPT (declared, not counted as wired): {name} [{when}] — {why[:110]}…")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


def selftest() -> int:
    # #230 F6 — the selftest itself is repo-bound: it opens `_build_all.py` unguarded on its
    # first line, which is why the v1.0.5 probe recorded `'selftest': 'crashed'` beside this
    # gate's verdict. A crash is not a fail [[a-crash-is-not-a-fail]]; it is the same unaskable
    # question as `run()`'s, and it gets the same honest answer rather than a traceback.
    if not reachable_surfaces():
        return cna.refuse(
            SELF + " --selftest",
            "knowledge/_build_all.py does not exist here — the selftest mutates the REAL wiring "
            "text to prove the gate bites, and there is no wiring text to mutate outside the "
            "design system's own source repo.")
    build_text = BUILD.read_text(encoding="utf-8")
    commit_text, ci_text = read(COMMIT_SH), read(CI_YML)
    disk = population()
    fails = []
    # bite 1 (DETECTION, remove a REAL entry): strip a wired validator from the build text.
    # ⚠ #221: the candidate must be wired ONLY in STEPS. Now that three more surfaces count,
    # a name that is also in `_git_commit.sh` would survive the mutation and this bite would
    # measure nothing while still passing — a bite quietly emptied by a widening.
    wired_real = next(n for n in disk
                      if n not in EXEMPT and n != SELF
                      and re.search(r'["\']' + re.escape(n) + r'["\']', build_text)
                      and not re.search(re.escape(n), commit_text)
                      and not re.search(re.escape(n), ci_text))
    mutated = build_text.replace(wired_real, wired_real + ".MUTATED")
    if not any("ORPHAN" in f and wired_real in f for f in check(mutated, disk)):
        fails.append(f"bite 1 FAILED: removing {wired_real}'s entry did not fire")
    # bite 2 (DETECTION, other direction): add a fake orphan to disk
    if not any("_validate_fake_orphan.py" in f
               for f in check(build_text, disk + ["_validate_fake_orphan.py"])):
        fails.append("bite 2 FAILED: a fake orphan on disk did not fire")
    # bite 3 (REMEDIATION clause, not just detection — #104's lesson): a stale
    # exemption (exempt AND wired) must fire, proving the exempt list can't absorb a fix silently.
    # SYNTHETIC name, not a borrowed real one (#125): these two bites used to read
    # `next(iter(EXEMPT))`, so emptying EXEMPT would have crashed the selftest — and "make the
    # crash go away" would have meant deleting the two bites that police the exemption list
    # exactly when nothing is exempt. The clause must be testable when the list is empty.
    synth = "_validate_synthetic_exemption.py"
    synth_map = {synth: ("SYNTHETIC — selftest fixture only, never a real exemption", "2026-08-07")}
    wired_plus = build_text + f'\n# ("x", "{synth}"),\n("x", "{synth}")'
    if not any("STALE EXEMPTION" in f and synth in f
               for f in check(wired_plus, disk + [synth], synth_map)):
        fails.append(f"bite 3 FAILED: stale exemption for {synth} did not fire")
    # bite 4: a dangling exemption (exempt, not on disk) must fire
    if not any("DANGLING EXEMPTION" in f and synth in f
               for f in check(build_text, disk, synth_map)):
        fails.append("bite 4 FAILED: dangling exemption did not fire")

    # ── #221 BITES 5–9: the two widenings, each driven in BOTH directions ──────────────────
    # bite 5 — THE BITE FOR #220-L1 FINDING 8. A `_gate_*.py` orphan must fire. Before #221 the
    # population glob could not see this namespace at all, so this bite could not have failed
    # — it could not have RUN. [[unmatched-grep-is-not-an-absence]] as a gate defect.
    if not any("_gate_fake_orphan.py" in f
               for f in check(build_text, disk + ["_gate_fake_orphan.py"], None,
                              commit_text, ci_text, set())):
        fails.append("bite 5 FAILED: a `_gate_*.py` orphan on disk did not fire — the population "
                     "glob has narrowed back to one namespace (#220-L1 finding 8)")
    # bite 5b — POPULATION CONTROL, not a mutation: the real namespace must actually be in the
    # population. A glob that matched nothing would pass bite 5 by accident.
    if not any(n.startswith("_gate_") for n in disk):
        fails.append("bite 5b FAILED: no `_gate_*.py` in the population — the widened glob "
                     "matches nothing, so bite 5 proves nothing")
    # ⚠ bites 6–8 assert about THE FIXTURE NAME ONLY. An earlier cut asserted `if check(...)`
    # — "no failures at all" — which folded every unrelated finding on the real tree into the
    # bite's verdict and made two of them fail for a reason that had nothing to do with them.
    # A bite must be able to fail for exactly one reason.
    # bite 6 — the commit seam counts as wiring (`_gate_doc_rows.py`'s real state)
    fake = "_gate_seam_only.py"
    if any(fake in f for f in check(build_text, disk + [fake], None,
                                    f"python3 knowledge/{fake} --check", "", set())):
        fails.append("bite 6 FAILED: a script invoked at the commit seam was called an orphan")
    # bite 6b — and the OTHER direction: remove the seam text and it must fire again
    if not any(fake in f for f in check(build_text, disk + [fake], None, "", "", set())):
        fails.append("bite 6b FAILED: with the seam invocation gone, the same script did not fire")
    # bite 6c — the CI surface, both directions, same shape
    if any(fake in f for f in check(build_text, disk + [fake], None, "",
                                    f"run: python3 knowledge/{fake} --check", set())):
        fails.append("bite 6c FAILED: a script run by a gates.yml step was called an orphan")
    # bite 7 — a DECLARED, VERIFIED arm counts (`_gate_harness_stubs.py`'s real state)
    if any(fake in f for f in check(build_text, disk + [fake], None, "", "", {fake})):
        fails.append("bite 7 FAILED: a declared arm of a wired script was called an orphan")
    # bite 8 — ⛔ THE ANTI-LAUNDERING DIRECTION. A declaration naming an UNWIRED importer must
    # fail; this is the clause that stops the ARM_OF table becoming a second exemption list
    # with no reader. Fixture importer is a name nothing wires.
    launder = {fake: ("_gate_launder_importer.py", "SYNTHETIC fixture", "2026-08-27")}
    got = arm_failures(build_text, commit_text, ci_text, disk + [fake], launder)
    if not any("BROKEN ARM" in f or "LAUNDERED ARM" in f for f in got):
        fails.append("bite 8 FAILED: an arm declared against an unwired/absent importer passed")
    # bite 8b — a declaration whose importer is wired but does NOT import it must fire STALE
    stale = {fake: ("_validate_wiring.py", "SYNTHETIC fixture", "2026-08-27")}
    if not any("STALE ARM" in f for f in
               arm_failures(build_text, commit_text, ci_text, disk + [fake], stale)):
        fails.append("bite 8b FAILED: an arm declaration whose importer does not import it passed")
    # bite 8c — the CONTROL: the real declarations must be clean, or the three bites above are
    # measuring a table nobody can satisfy
    real_arm_fails = arm_failures(build_text, commit_text, ci_text, disk)
    if real_arm_fails:
        fails.append("bite 8c FAILED (control): the REAL ARM_OF table does not verify: "
                     + " | ".join(real_arm_fails))
    # bite 9 — the real tree's own answer, asserted rather than assumed: every surface the
    # gate now trusts must be READABLE. A missing gates.yml would silently narrow the gate.
    for label, p in (("_build_all.py", BUILD), ("_git_commit.sh", COMMIT_SH), ("gates.yml", CI_YML)):
        if not read(p):
            fails.append(f"bite 9 FAILED: wiring surface {label} is unreadable at {p} — the gate "
                         f"would go quietly narrower, not louder")
    # ── #230 BITES 10–10c: the pack-context refusal, driven in BOTH directions ──────────────
    # ⛔ THE THING UNDER TEST IS `run()` ITSELF, not a predicate. A bite that asserted
    # `reachable_surfaces() == []` would prove the helper and nothing about the gate's exit code
    # [[mutation-tests-the-clause-not-the-feature]] — so the mutation TAKES THE INPUT AWAY and
    # the real entry point is driven over it.
    import contextlib
    import io as _io

    def _drive_run_with(build, commit, ci):
        """run(), with the three wiring surfaces repointed. Returns (rc, output)."""
        global BUILD, COMMIT_SH, CI_YML
        keep = (BUILD, COMMIT_SH, CI_YML)
        BUILD, COMMIT_SH, CI_YML = build, commit, ci
        buf = _io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = run()
        finally:
            BUILD, COMMIT_SH, CI_YML = keep
        return rc, buf.getvalue()

    gone = HERE / "_no_such_wiring_surface_230"
    # bite 10 — every surface taken away: the gate must REFUSE (77 + the marker), never red.
    rc10, out10 = _drive_run_with(gone / "_build_all.py", gone / "_git_commit.sh", gone / "gates.yml")
    if rc10 != cna.EXIT:
        fails.append(f"bite 10 FAILED: with all three wiring surfaces absent the gate exited "
                     f"{rc10}, not {cna.EXIT}. That is the #230 F6 defect — 23 shipped gates "
                     f"called ORPHANs because the question could not be asked.")
    if cna.reason_in(out10) is None:
        fails.append("bite 10 FAILED: the refusal carried no `COULD-NOT-ASK:` line — the exit "
                     "code buckets it, the line is what a human reads")
    # bite 10b — THE OTHER DIRECTION, and the one that stops the refusal swallowing the gate.
    # ONE surface back is enough: the gate must grade again, and a planted orphan must still red.
    rc10b, out10b = _drive_run_with(gone / "_build_all.py", gone / "_git_commit.sh", CI_YML)
    if rc10b == cna.EXIT:
        fails.append("bite 10b FAILED: one readable wiring surface was still treated as "
                     "unaskable — the refusal has widened past its condition and now hides "
                     "real orphans")
    # bite 10c — THE REAL, UNMUTATED TREE is not refusing. Without this control, bites 10/10b
    # could both pass on a repo whose gate never grades anything at all.
    if not reachable_surfaces():
        fails.append("bite 10c FAILED (control): this source repo reaches NO wiring surface, so "
                     "the gate is refusing on its own tree and every bite above is theatre")
    # bite 10d — ⛔ THE DOWNSTREAM CLAUSE, driven not asserted. The refusal is only correct if
    # the release classifier reads it as REPO-BOUND; classified NEEDS-DEP it would ship anyway
    # and tell a designer to `pip install` the repo [[instrument-without-a-consumer]].
    try:
        sys.path.insert(0, str(HERE / "_release"))
        import _gen_pack_manifest as _gpm  # noqa: E402 - repo-side, and this arm is repo-bound
        verdict, why = _gpm.classify(rc10, out10, "", set())
        if verdict != "REPO-BOUND":
            fails.append(f"bite 10d FAILED: the release classifier reads this refusal as "
                         f"{verdict} ({why}), not REPO-BOUND. A NEEDS-DEP refusal SHIPS, and no "
                         f"`pip install` can produce knowledge/_build_all.py.")
    except ImportError as e:
        fails.append(f"bite 10d COULD NOT RUN: {e} — the downstream clause is UNPROVEN, not "
                     f"green [[feedback-check-ran-never-reached-plan]]")

    print(f"wiring selftest: 17 bites · {len(fails)} failure(s)")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
