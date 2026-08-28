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
    print(f"wiring selftest: 13 bites · {len(fails)} failure(s)")
    for f in fails:
        print(f"  ⛔ {f}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
