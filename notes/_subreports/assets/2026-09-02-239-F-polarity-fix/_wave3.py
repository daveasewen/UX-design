#!/usr/bin/env python3
"""WAVE 3 — redo of two arms, schema loosenings NO selftest arm overlaps, the WRITER door
(--add-polarity / --add-stub), and the two door asymmetries (rc 77 at the build; POLARITY_BRAIN_DIR
redirect at the seam, on a fake-repo stand-in so the live tree is never touched)."""
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, "/sessions/wonderful-adoring-euler/mnt/outputs/v238")
from _v_attack import *  # noqa: E402,F401,F403

LOG = os.path.join(V, "logs")
out_lines = []


def say(s=""):
    print(s)
    out_lines.append(s)


# ---- redo 221 / 240 ------------------------------------------------------------------------------
def self_oracle(d):
    o = json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())
    mv = " ".join(o["polarities"][0]["mediating_variable"].split()[:8])
    o["polarities"][0]["sources"] = [{"path": "knowledge/brain/polarities.json", "id": "pl-01"}]
    o["polarities"][0]["links"][0]["quote"] = mv
    with open(os.path.join(d, "polarities.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(o, indent=1, ensure_ascii=False) + "\n")
arm(300, "quote-oracle-repointed-to-itself-8-words", "red", self_oracle, "R3-QUOTE-NOT-VERBATIM",
    basis="the node names polarities.json/pl-01 as its own source; the quote is 8 words of its own mediating_variable")


def demote_obligation(d):
    o = json.loads(open(os.path.join(d, "polarities.json"), encoding="utf-8").read())
    p = json.loads(open(os.path.join(d, "principles.json"), encoding="utf-8").read())
    reg = {x["id"]: x for x in p["principles"]}
    target = None
    for n in o["polarities"]:
        for pt in n["parties"]:
            if pt["ref"] in reg and reg[pt["ref"]].get("grade") == "L":
                target = (n["id"], pt["ref"]); break
        if target: break
    reg[target[1]]["grade"] = "C"
    with open(os.path.join(d, "principles.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(p, indent=1, ensure_ascii=False) + "\n")
    say(f"  [301] demoted {target[1]} (a party of {target[0]}) from L to C")
arm(301, "register-obligation-demoted-L-to-C", "red", demote_obligation, None,
    basis="s237-D2 obligation outranks; a grade letter edit in principles.json silently re-sorts a settled-by-obligation row; no receipt against R1's seed")

# ---- schema loosenings that NO selftest arm overlaps --------------------------------------------
def loosen_sources_additional(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["sources"]["items"].__setitem__("additionalProperties", True))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0]["sources"][0].__setitem__("judgement", "Jakob wins in Apollo; Von Restorff only for the one primary action."))
arm(310, "schema-sources-additionalProperties-true-plus-judgement", "red", loosen_sources_additional, "R3-JUDGEMENT-FIELD",
    basis="s238-D7 (3); no selftest arm probes sources[] extra keys, so [142] cannot catch this loosening either")


def loosen_sources_minitems(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["sources"].__setitem__("minItems", 0))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: (o["polarities"][0].__setitem__("sources", []),
                                                                o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget")))
arm(311, "schema-sources-minItems-0-plus-no-sources-plus-paraphrase", "red", loosen_sources_minitems, "R3-QUOTE-NOT-VERBATIM",
    basis="a node with no source row has no oracle: every quote on it is UNVERIFIED and passes; no selftest arm probes sources.minItems")


def loosen_note_maxwords(d):
    mutate_json(os.path.join(d, "schema", "polarity.schema.json"), lambda s: s["properties"]["parties"]["items"]["properties"]["note"].__setitem__("maxWords", 500))
    mutate_json(os.path.join(d, "polarities.json"), lambda o: o["polarities"][0]["parties"][0].__setitem__("note", " ".join(["Jakob wins in Apollo because Dave prefers familiar chrome."] * 8)))
arm(312, "schema-note-maxWords-500-plus-64-word-note", "red", loosen_note_maxwords, "R3-NOTE-TOO-LONG",
    basis="s238-D7 (3); selftest arm 20 (16-word note) overlaps this one — expect: --check accepts, [142] catches one build later")

say(table())
dump(os.path.join(LOG, "wave3-arms.json"))

# ---- [142] on the accepted mutants: does the BUILD's selftest catch what the SEAM's --check let through?
say("\n== --selftest (build step [142], ABORT) on the accepted + re-derived mutants of 310/311/312")
for slug in ("310-schema-sources-additionalProperties-true-plus-judgement", "311-schema-sources-minItems-0-plus-no-sources-plus-paraphrase",
             "312-schema-note-maxWords-500-plus-64-word-note"):
    bw = os.path.join(ARMS, slug, "brain-w")
    if not os.path.isdir(os.path.join(bw, "_generated")):
        say(f"  {slug}: --write did not accept it; skipping"); continue
    rc, out = run([PY, VALIDATOR, "--selftest", "--brain", bw])
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().split()[1:2] == ["FAIL"]]
    tail = [ln for ln in out.splitlines() if ln.startswith("arms ")]
    say(f"  {slug}: selftest rc={rc} :: {tail[0] if tail else out[-200:]}")
    for f in fails:
        say(f"      {f[:120]}")
    with open(os.path.join(LOG, f"selftest-{slug}.txt"), "w", encoding="utf-8") as f:
        f.write(out)

# ---- THE WRITER DOOR -------------------------------------------------------------------------------
say("\n== THE WRITER DOOR (--add-polarity / --add-stub) on copies")


def wdoor(brain, which, entry, write):
    ep = os.path.join(os.path.dirname(brain), f"entry-{which}.json")
    with open(ep, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
    return run([PY, VALIDATOR, f"--add-{which}", ep, "--write" if write else "--dry-run", "--brain", brain])


GOOD = {"id": "pl-90", "parties": [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}],
        "mediating_variable": "target count", "links": [], "sources": [{"path": "selftest", "id": "x"}]}
W = []


def wcase(n, slug, prep, which, entry, write, expect_rc, check):
    d = os.path.join(ARMS, f"{n}-{slug}")
    if os.path.exists(d):
        shutil.move(d, os.path.join(GRAVE, os.path.basename(d) + "-" + str(os.getpid())))
    os.makedirs(d)
    brain = fresh_copy(os.path.join(d, "brain"))
    prep(brain)
    before = tree(brain)
    rc, out = wdoor(brain, which, entry, write)
    after = tree(brain)
    homes_changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k) and not k.startswith("_generated/"))
    verdict, detail = check(rc, out, brain, homes_changed)
    W.append((n, slug, rc, expect_rc, homes_changed, verdict, detail))
    say(f"  [{n}] {verdict:9} rc={rc} (expect {expect_rc}) homes changed={homes_changed} :: {slug} :: {detail[:140]}")
    with open(os.path.join(d, "writer.txt"), "w", encoding="utf-8") as f:
        f.write(out)


def parse_count(brain):
    return len(json.loads(open(os.path.join(brain, "polarities.json"), encoding="utf-8").read())["polarities"])


# W1: the description carries "polarities" IN QUOTES before the array — _array_bounds finds the first '"polarities"'
def desc_trap(brain):
    p = os.path.join(brain, "polarities.json")
    t = open(p, encoding="utf-8").read()
    t = t.replace('"$description": "THE ONE HOME', '"$description": "THE ONE HOME (the \\"polarities\\" array below)', 1)
    json.loads(t)
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
wcase(320, "writer-description-contains-quoted-polarities", desc_trap, "polarity", GOOD, True, 1,
      lambda rc, out, b, ch: (("CAUGHT" if rc != 0 and not ch else ("CORRUPTED" if ch and parse_count(b) != 31 else "GREEN-OK")),
                              next((ln for ln in out.splitlines() if "REFUSED" in ln), out.strip().splitlines()[-1] if out.strip() else "")))

# W2: an EMPTY polarities array (the `inside.strip() == ""` branch)
wcase(321, "writer-append-into-empty-array", pol(lambda o: o.__setitem__("polarities", [])), "polarity", GOOD, True, 0,
      lambda rc, out, b, ch: (("GREEN-OK" if rc == 0 and parse_count(b) == 1 else "FALSE-RED"), out.strip().splitlines()[-1] if out.strip() else ""))

# W3: duplicate id
wcase(322, "writer-duplicate-id-pl-01", lambda b: None, "polarity", dict(GOOD, id="pl-01"), True, 1,
      lambda rc, out, b, ch: (("CAUGHT" if rc != 0 and "S-DUP-ID" in out and not ch else "ESCAPED"), next((ln for ln in out.splitlines() if "REFUSED" in ln), "")))

# W4: duplicate stub id
wcase(323, "writer-duplicate-stub-id", lambda b: None, "stub", {"id": "st-brand-palette", "phrase": "another phrase"}, True, 1,
      lambda rc, out, b, ch: (("CAUGHT" if rc != 0 and "S-DUP-STUB" in out and not ch else "ESCAPED"), next((ln for ln in out.splitlines() if "REFUSED" in ln), "")))

# W5: an entry whose link quote has NO reachable source: accepted UNVERIFIED and WRITTEN
wcase(324, "writer-accepts-unverifiable-quote", lambda b: None, "polarity",
      dict(GOOD, id="pl-91", links=[{"type": "resolvedBy", "ref": "s116-D1", "quote": "this quote exists nowhere"}]), True, 0,
      lambda rc, out, b, ch: (("ESCAPED" if rc == 0 and parse_count(b) == 31 else "CAUGHT"), next((ln for ln in out.splitlines() if "UNVERIFIED" in ln), out.strip().splitlines()[-1] if out.strip() else "")))

# W6: the entry is a LIST (two entries at once)
wcase(325, "writer-entry-is-a-list", lambda b: None, "polarity", [GOOD, dict(GOOD, id="pl-92")], True, 1,
      lambda rc, out, b, ch: (("CAUGHT" if rc != 0 and not ch else "ESCAPED"), next((ln for ln in out.splitlines() if "REFUSED" in ln), out.strip().splitlines()[-1] if out.strip() else "")))

# W7: a foreign format (2-space indent) — the writer appends 1-space; mixed format results, no refusal
def reindent(brain):
    p = os.path.join(brain, "polarities.json")
    o = json.loads(open(p, encoding="utf-8").read())
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(o, indent=2, ensure_ascii=False) + "\n")
wcase(326, "writer-on-2-space-indented-file", reindent, "polarity", GOOD, True, 0,
      lambda rc, out, b, ch: (("GREEN-OK" if rc == 0 and parse_count(b) == 31 else "FALSE-RED"),
                              "mixed indent: " + repr(open(os.path.join(b, "polarities.json"), encoding="utf-8").read()[-260:-200])))

# W8: dry-run then --write of a bad entry (typed status) on the REAL-shaped copy — nothing written (P arm 47 control)
wcase(327, "writer-typed-status-refused-control", lambda b: None, "polarity", dict(GOOD, id="pl-93", status="open"), True, 1,
      lambda rc, out, b, ch: (("CAUGHT" if rc != 0 and "R5-TYPED-STATUS" in out and not ch else "ESCAPED"), next((ln for ln in out.splitlines() if "REFUSED" in ln), "")))

# W9: add-stub whose phrase is a zero-width space (wave-1 arm 22 through the writer)
wcase(328, "writer-stub-zwsp-phrase", lambda b: None, "stub", {"id": "st-zwsp", "phrase": "​"}, True, 1,
      lambda rc, out, b, ch: (("ESCAPED" if rc == 0 else "CAUGHT"), out.strip().splitlines()[-1] if out.strip() else ""))

# ---- DOOR ASYMMETRIES -------------------------------------------------------------------------------
say("\n== DOOR ASYMMETRY 1: the home is ABSENT (POLARITY_BRAIN_DIR -> a path that does not exist)")
nowhere = os.path.join(V, "no-such-home")
rcA, outA = door_cli(nowhere)
rcB, outB = door_build(nowhere)
rcC, outC = door_seam(nowhere)
say(f"  A CLI   rc={rcA} :: {outA.strip().splitlines()[0][:120] if outA.strip() else ''}")
say(f"  B BUILD rc={rcB} -> _build_all.main() treats 77 as 'COULD-NOT-ASK — declared refusal, build continues' (its own words, line ~1352); route={KIND}")
say(f"  C SEAM  rc={rcC} :: {[l for l in outC.splitlines() if l.startswith('✗') or 'SEAM' in l]}")
with open(os.path.join(LOG, "door-asymmetry-77.txt"), "w", encoding="utf-8") as f:
    f.write(f"A rc={rcA}\n{outA}\n\nB rc={rcB}\n{outB}\n\nC rc={rcC}\n{outC}\n")

say("\n== DOOR ASYMMETRY 2: POLARITY_BRAIN_DIR at the seam — a fake-repo stand-in whose knowledge/brain/ is DIRTY")
FAKE = os.path.join(V, "fakerepo")
if os.path.exists(FAKE):
    shutil.move(FAKE, os.path.join(GRAVE, "fakerepo-" + str(os.getpid())))
os.makedirs(os.path.join(FAKE, "knowledge"))
for fn in ("_validate_polarities.py", "_helpgate.py", "_could_not_ask.py", "_rulings.json"):
    shutil.copy2(os.path.join(KNOW, fn), os.path.join(FAKE, "knowledge", fn))
for rel in ("notes/_subreports/assets/2026-09-02-237-T-tensions-schema/open-tensions.json",
            "notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json"):
    os.makedirs(os.path.dirname(os.path.join(FAKE, rel)), exist_ok=True)
    shutil.copy2(os.path.join(REPO, rel), os.path.join(FAKE, rel))
shutil.copytree(REAL, os.path.join(FAKE, "knowledge", "brain"))
mutate_json(os.path.join(FAKE, "knowledge", "brain", "polarities.json"), lambda o: o["polarities"][0].__setitem__("status", "open"))


def seam_in(cwd, env_extra=None):
    env = dict(os.environ)
    env.pop("POLARITY_BRAIN_DIR", None)
    env.pop("POLARITY_ACK", None)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(["bash", SEAM_SH], cwd=cwd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


rc0, out0 = seam_in(FAKE)
rc1, out1 = seam_in(FAKE, {"POLARITY_BRAIN_DIR": REAL})
rc2, out2 = seam_in(FAKE, {"POLARITY_ACK": "lazy"})
say(f"  (a) seam block in the fake repo, no env:                 rc={rc0} names={names(out0)}  (proves the stand-in: the tree's brain IS dirty)")
say(f"  (b) same, POLARITY_BRAIN_DIR=<a clean copy elsewhere>:   rc={rc1} names={names(out1)} :: {[l for l in out1.splitlines() if 'polarity gate' in l][-1][:150]}")
say(f"      the ONLY trace of the redirect on the record: {[l[:120] for l in out1.splitlines() if 'home ' in l]}")
say(f"  (c) same, POLARITY_ACK=lazy (the spelled hatch):         rc={rc2} :: {[l for l in out2.splitlines() if 'DECLARED' in l]}")
with open(os.path.join(LOG, "door-asymmetry-seam-redirect.txt"), "w", encoding="utf-8") as f:
    f.write(f"(a) rc={rc0}\n{out0}\n\n(b) rc={rc1}\n{out1}\n\n(c) rc={rc2}\n{out2}\n")

say("\n== BUILD door on a CRASH arm: what the GATE remedy claims vs what the output names")
rcX, outX = door_build(os.path.join(ARMS, "44-role-object-unhashable", "brain"))
say(f"  rc={rcX} names={names(outX)} traceback={'Traceback' in outX}")
say("  remedy text the build prints: " + REMEDY.format(code=rcX).strip().replace("\n", " ")[:330])

with open(os.path.join(LOG, "wave3.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")
