#!/usr/bin/env python3
"""#239 lane F — every row of V's escaped-repro.txt re-driven in its STANDALONE form, same order.

For each row: cp -r knowledge/brain $T · the mutation V wrote (M/S/K/G as in escaped-repro.txt) ·
`--write --brain $T` · `--check --brain $T` (a generated/stray-file row: --check as-is). The
decisive door is the one V named. Writer rows drive --add-*; the door rows drive the build form
and the extracted seam block; the argv rows drive the contradictory flags. Nothing under the live
repo is touched. Output: escaped-now-caught.txt beside this script (and under outputs/f239/).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

REPO = "/sessions/eager-wizardly-lovelace/mnt/UX-design"
F = "/dev/shm/p242"
OUT_DIRS = [os.path.join(REPO, "notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt")]
KNOW = os.path.join(REPO, "knowledge")
VAL = os.path.join(KNOW, "_validate_polarities.py")
REAL = os.path.join(F, "brain-real")
ROOT = os.path.join(F, "standalone")
PY = sys.executable
ZW = "​"
NAME_RE = re.compile(r"REFUSED \(([A-Za-z0-9-]+)\)")


def run(cmd, env_extra=None, cwd=REPO):
    env = dict(os.environ)
    env.pop("POLARITY_BRAIN_DIR", None)
    env.pop("POLARITY_ACK", None)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def names(out):
    return sorted(n for n in set(NAME_RE.findall(out)) if not re.match(r"^s\d+-D\d+$", n))


def first_refused(out):
    return next((ln.strip() for ln in out.splitlines() if "REFUSED (" in ln and "POLARITY GATE REFUSED" not in ln), "")


def tree(root):
    out = {}
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            out[os.path.relpath(p, root)] = ("link:" + os.readlink(p)) if os.path.islink(p) else hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def fresh(slug):
    d = os.path.join(ROOT, slug)
    if os.path.exists(d):
        shutil.move(d, os.path.join(F, "_graveyard", f"standalone-{slug}-{os.getpid()}"))
    shutil.copytree(REAL, d)
    return d


def mj(path, fn):
    o = json.load(open(path, encoding="utf-8"))
    fn(o)
    json.dump(o, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def M(fn):
    return lambda T: mj(os.path.join(T, "polarities.json"), fn)


def S(fn):
    return lambda T: mj(os.path.join(T, "stubs.json"), fn)


def K(fn):
    return lambda T: mj(os.path.join(T, "schema", "polarity.schema.json"), fn)


def P(fn):
    return lambda T: mj(os.path.join(T, "principles.json"), fn)


def W(relpath, text, mode="w"):
    def _w(T):
        p = os.path.join(T, relpath)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
            f.write(text)
    return _w


def both(*fns):
    return lambda T: [f(T) for f in fns]


def sed(relpath, pattern, repl, count=1):
    def _s(T):
        p = os.path.join(T, relpath)
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(re.sub(pattern, repl, t, count=count))
    return _s


LINES = []


def say(s=""):
    print(s)
    LINES.append(s)


def row(n, grade, what, mutate, decisive="after-write", expect_names=None):
    T = fresh(str(n))
    mutate(T)
    h0 = tree(T)
    rcw, outw = run([PY, VAL, "--write", "--brain", T])
    h1 = tree(T)
    rcc, outc = run([PY, VAL, "--check", "--brain", T])
    nm = names(outw + outc)
    if decisive == "as-is":
        caught = rcc != 0
    else:
        caught = rcw != 0
    untouched = (h0 == h1) if rcw != 0 else True
    crash = "Traceback" in outw + outc
    verdict = "CAUGHT" if (caught and not crash and untouched) else ("CRASH" if crash else ("WROTE" if not untouched else "ESCAPED"))
    if verdict == "CAUGHT" and expect_names and not all(e in nm for e in expect_names):
        verdict = "MISNAMED"
    say(f"{str(n):>3}  {grade:8}  {verdict:8}  write-rc={rcw} check-rc={rcc}  names={nm}")
    say(f"     {what}")
    say(f"     ⛔ {first_refused(outw if rcw else outc)[:170]}")
    return verdict


say("#239-F — EVERY ESCAPED ROW OF V's escaped-repro.txt, RE-DRIVEN STANDALONE AFTER THE FIX (same order)")
say("cp -r knowledge/brain $T ; <mutation> ; --write --brain $T ; --check --brain $T   (decisive door as V named it)")
say("verdict CAUGHT = decisive door rc!=0, no traceback, nothing written on refusal; the names printed follow.")
say("")
say(" #   grade     verdict   doors                                   names")
say("---  --------  --------  --------------------------------------  ----------------------------------------------")
V = {}
V[22] = row(22, "PROMISED", "stub whose phrase is one U+200B", S(lambda o: o["stubs"].append({"id": "st-zwsp", "phrase": ZW})), expect_names=["S-STUB-SHAPE"])
V[30] = row(30, "RULED", "resolvedBy s200-D2 — superseded in s200-D3's PROSE", M(lambda o: o["polarities"][2]["links"].append({"type": "resolvedBy", "ref": "s200-D2"})), expect_names=["R1-SUPERSEDED"])
V[31] = row(31, "RULED", "resolvedBy gauge-band — status 'still open'", M(lambda o: o["polarities"][2]["links"].append({"type": "resolvedBy", "ref": "gauge-band"})), expect_names=["R1-DANGLING"])
V[32] = row(32, "RULED", "resolvedBy s182-D1 — status PARKED", M(lambda o: o["polarities"][2]["links"].append({"type": "resolvedBy", "ref": "s182-D1"})), expect_names=["R1-DANGLING"])
V[70] = row(70, "PROMISED", "generated_at 2099-01-01 on all three derived files",
            both(sed("_generated/polarity-status.json", r'"generated_at": "2026-09-02T', '"generated_at": "2099-01-01T'),
                 sed("_generated/polarity-edges.json", r'"generated_at": "2026-09-02T', '"generated_at": "2099-01-01T'),
                 sed("_generated/defaults-declaration.txt", r"generated_at: 2026-09-02T", "generated_at: 2099-01-01T")), decisive="as-is")
V[71] = row(71, "PROMISED", "generated_at 'banana'", sed("_generated/polarity-status.json", r'"generated_at": "[^"]*"', '"generated_at": "banana"'), decisive="as-is")
V[82] = row(82, "PROMISED", "$migration.verdicts = {pl-01: ...}", M(lambda o: o["$migration"].__setitem__("verdicts", {"pl-01": "Jakob wins in Apollo — Von Restorff only for chrome."})), expect_names=["R3-JUDGEMENT-FIELD"])
V[83] = row(83, "PROMISED", "$description replaced by 500 words of verdict", M(lambda o: o.__setitem__("$description", " ".join(["Aesthetics must win over usability …"] * 32))), expect_names=["R3-JUDGEMENT-FIELD"])
V[93] = row(93, "PROMISED", "sources[0].id 'tn-0１' (fullwidth 1)", M(lambda o: o["polarities"][0]["sources"][0].__setitem__("id", "tn-0１")))
V[110] = row(110, "RULED", "schema minItems 2→1 + pl-01 with ONE party",
             both(K(lambda s: s["properties"]["parties"].__setitem__("minItems", 1)),
                  M(lambda o: o["polarities"][0].__setitem__("parties", o["polarities"][0]["parties"][:1]))), expect_names=["S-MIN-PARTIES"])
V[111] = row(111, "RULED", "schema enum + 'relatedTo' + a relatedTo link",
             both(K(lambda s: s["properties"]["links"]["items"]["properties"]["type"]["enum"].append("relatedTo")),
                  M(lambda o: o["polarities"][0]["links"].append({"type": "relatedTo", "ref": "s116-D1"}))), expect_names=["R2-UNKNOWN-TYPE"])
V[112] = row(112, "RULED", "schema parties.items.additionalProperties true + party.why",
             both(K(lambda s: s["properties"]["parties"]["items"].__setitem__("additionalProperties", True)),
                  M(lambda o: o["polarities"][0]["parties"][0].__setitem__("why", "because Jakob wins in Apollo"))), expect_names=["R3-JUDGEMENT-FIELD"])
V[210] = row(210, "RULED", ".edges.json (authored edge list) at brain top", W(".edges.json", '{"edges":[{"from":"pr-fitts","to":"pr-hick"}]}\n'), decisive="as-is", expect_names=["R4-AUTHORED-EDGES"])
V[211] = row(211, "RULED", "_generated/.authored-edges.json", W("_generated/.authored-edges.json", '{"edges":[]}\n'), decisive="as-is", expect_names=["R4-STRAY-FILE"])
V[212] = row(212, "RULED", "_generated/.polarity-edges.json.tmp (half-written)", W("_generated/.polarity-edges.json.tmp", '{"edges":[1]}\n'), decisive="as-is", expect_names=["R4-STRAY-FILE"])
V[213] = row(213, "RULED", "schema/edges.json (authored edge list)", W("schema/edges.json", '{"edges":[{"from":"pr-fitts","to":"pr-hick"}]}\n'), decisive="as-is", expect_names=["R4-AUTHORED-EDGES"])
V[214] = row(214, "PROMISED", "schema/polarity.schema.v2.json (second schema)", W("schema/polarity.schema.v2.json", '{"minItems":1}\n'), decisive="as-is", expect_names=["R4-STRAY-FILE"])
V[216] = row(216, "RULED", "__pycache__/edges.json", W("__pycache__/edges.json", '{"edges":[]}\n'), decisive="as-is", expect_names=["R4-STRAY-FILE"])
V[220] = row(220, "PROMISED", "pl-01 sources → knowledge/_rulings.json#s238-D7, quote = 13 words OF THE RULING",
             M(lambda o: (o["polarities"][0].__setitem__("sources", [{"path": "knowledge/_rulings.json", "id": "s238-D7"}]),
                          o["polarities"][0]["links"][0].__setitem__("quote", "A gate that is not a consumer of every commit is not a gate"))), expect_names=["R3-QUOTE-NOT-VERBATIM"])
V[222] = row(222, "PROMISED", "P arm 23's paraphrase + sources.path → nowhere",
             M(lambda o: (o["polarities"][0]["sources"][0].__setitem__("path", "notes/no-such-file.json"),
                          o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget"))), expect_names=["R3-QUOTE-NOT-VERBATIM"])
V[223] = row(223, "PROMISED", "resolvedBy s116-D1 with quote ''", M(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1", "quote": ""})), expect_names=["R3-QUOTE-NOT-VERBATIM"])
V[224] = row(224, "PROMISED", "resolvedBy s116-D1 with quote 'the'", M(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1", "quote": "the"})), expect_names=["R3-QUOTE-NOT-VERBATIM"])
V[230] = row(230, "RULED", "party.note = 14-word verdict", M(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", "Jakob must always win in Apollo because Dave rules by eye and prefers familiarity")), expect_names=["R3-JUDGEMENT-FIELD"])
V[231] = row(231, "RULED", "party.note = 44 visible words joined by U+200B", M(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", ZW.join(["Jakob", "must", "always", "win", "in", "Apollo", "because", "Dave", "rules", "by", "eye"] * 4))), expect_names=["R3-NOTE-TOO-LONG"])
V[232] = row(232, "RULED", "mediating_variable = 300-word verdict", M(lambda o: o["polarities"][0].__setitem__("mediating_variable", " ".join(["Jakob wins and Von Restorff loses …"] * 20))), expect_names=["R3-JUDGEMENT-FIELD"])
V[233] = row(233, "RULED", "sources[0].id = 300-word verdict on pl-04", M(lambda o: o["polarities"][3]["sources"][0].__setitem__("id", " ".join(["aesthetics wins over usability in Apollo, always."] * 30))), expect_names=["R3-JUDGEMENT-FIELD"])
V[234] = row(234, "PROMISED", "stub phrase = 15-word verdict declared as a party", S(lambda o: o["stubs"].append({"id": "st-dense-tables-win", "phrase": "dense financial tables must always beat whitespace in Apollo because Dave prefers density everywhere"})), expect_names=["R3-JUDGEMENT-FIELD"])
V[241] = row(241, "UNRULED", "principles.json statement rewritten ('Fitts is wrong …')", P(lambda p: p["principles"][0].__setitem__("statement", "Fitts is wrong and Apollo ignores it.")))
V[243] = row(243, "UNRULED", "pl-16: resolvedBy s116-D1 AND challengedBy s116-D1", M(lambda o: o["polarities"][15]["links"].append({"type": "challengedBy", "ref": "s116-D1"})))
V[244] = row(244, "UNRULED", "all 30 rows deleted", M(lambda o: o.__setitem__("polarities", [])))
V[245] = row(245, "UNRULED", "all 21 links deleted", M(lambda o: [n.__setitem__("links", []) for n in o["polarities"]]))
V[246] = row(246, "PROMISED", "$migration.sha256 = 64 zeros", M(lambda o: o["$migration"].__setitem__("sha256", "0" * 64)))
V[247] = row(247, "PROMISED", "$migration.from = a path that does not exist", M(lambda o: o["$migration"].__setitem__("from", "notes/does-not-exist.json")))
V[300] = row(300, "PROMISED", "pl-01 sources → knowledge/brain/polarities.json#pl-01, quote = 8 words of its own mediating_variable",
             M(lambda o: (o["polarities"][0].__setitem__("sources", [{"path": "knowledge/brain/polarities.json", "id": "pl-01"}]),
                          o["polarities"][0]["links"][0].__setitem__("quote", " ".join(o["polarities"][0]["mediating_variable"].split()[:8])))), expect_names=["R3-QUOTE-NOT-VERBATIM"])
V[301] = row(301, "UNRULED", "principles.json pr-wcag-1-4-3 grade L→C", P(lambda p: [x.__setitem__("grade", "C") for x in p["principles"] if x["id"] == "pr-wcag-1-4-3"]))
V[310] = row(310, "RULED", "schema sources.items.additionalProperties true + judgement (V's TOTAL escape)",
             both(K(lambda s: s["properties"]["sources"]["items"].__setitem__("additionalProperties", True)),
                  M(lambda o: o["polarities"][0]["sources"][0].__setitem__("judgement", "Jakob wins in Apollo; …"))), expect_names=["R3-JUDGEMENT-FIELD"])
V[311] = row(311, "PROMISED", "schema sources.minItems 0 + sources [] + paraphrased quote",
             both(K(lambda s: s["properties"]["sources"].__setitem__("minItems", 0)),
                  M(lambda o: (o["polarities"][0].__setitem__("sources", []), o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget")))), expect_names=["R3-QUOTE-NOT-VERBATIM"])
V[312] = row(312, "PROMISED", "schema note.maxWords 500 + a 64-word note",
             both(K(lambda s: s["properties"]["parties"]["items"]["properties"]["note"].__setitem__("maxWords", 500)),
                  M(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", " ".join(["Jakob wins in Apollo because Dave prefers familiar chrome."] * 8)))), expect_names=["R3-NOTE-TOO-LONG"])
V[400] = row(400, "PROMISED", "resolvedBy s116-D1 with NO quote at all", M(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1"})))
V[401] = row(401, "PROMISED", "pl-04 sources[0].id → 'tn-02'", M(lambda o: o["polarities"][3]["sources"][0].__setitem__("id", "tn-02")))
V[402] = row(402, "UNRULED", "pl-01's body duplicated under id pl-31", M(lambda o: o["polarities"].append(dict(o["polarities"][0], id="pl-31"))))


def symlink(T):
    shutil.move(os.path.join(T, "polarities.json"), os.path.join(T, "..", "moved-403.json"))
    os.symlink(os.path.join(T, "..", "moved-403.json"), os.path.join(T, "polarities.json"))
V[403] = row(403, "PROMISED", "polarities.json replaced by a symlink to a file outside the home", symlink, decisive="as-is")

# ---- WRITER rows ----------------------------------------------------------------------------------
say("")
for n, grade, what, which, entry in (
        (324, "PROMISED", "WRITER: --add-polarity of an entry whose quote has no reachable source", "polarity",
         {"id": "pl-91", "parties": [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}], "mediating_variable": "target count",
          "links": [{"type": "resolvedBy", "ref": "s116-D1", "quote": "this quote exists nowhere"}], "sources": [{"path": "selftest", "id": "x"}]}),
        (328, "PROMISED", "WRITER: --add-stub of the U+200B phrase", "stub", {"id": "st-zwsp", "phrase": ZW})):
    T = fresh(str(n))
    ep = os.path.join(ROOT, f"entry-{n}.json")
    json.dump(entry, open(ep, "w", encoding="utf-8"), ensure_ascii=False)
    h0 = tree(T)
    rc, out = run([PY, VAL, f"--add-{which}", ep, "--write", "--brain", T])
    verdict = "CAUGHT" if rc != 0 and tree(T) == h0 and "Traceback" not in out else "ESCAPED"
    V[n] = verdict
    say(f"{n:>3}  {grade:8}  {verdict:8}  rc={rc} homes-untouched={tree(T) == h0}  names={names(out)}")
    say(f"     {what}")
    say(f"     ⛔ {first_refused(out)[:170]}")

# ---- DOOR rows ---------------------------------------------------------------------------------------
say("")
sys.path.insert(0, KNOW)
_argv = sys.argv
sys.argv = ["x"]
import contextlib, io  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import _build_all as b  # noqa: E402
sys.argv = _argv
STEP = [s for s in b.STEPS if s[1] == "_validate_polarities.py" and "--check" in s[2]][0]
nowhere = os.path.join(F, "no-such-home")
rcA, outA = run([PY, VAL, "--check", "--brain", nowhere])
rcB, outB = run([PY, os.path.join(KNOW, STEP[1])] + list(STEP[2]), {"POLARITY_BRAIN_DIR": nowhere})
kind, remedy = b.route(STEP[0])
rcC, outC = run(["bash", os.path.join(F, "_seam_block.sh")], {"POLARITY_BRAIN_DIR": nowhere})
d1 = "CAUGHT" if (rcA == 1 and rcB == 1 and rcC == 1 and not any(ln.startswith("COULD-NOT-ASK:") for ln in (outA + outB + outC).splitlines())) else "ESCAPED"
V["D1"] = d1
say(f" D1  PROMISED  {d1:8}  A(cli)={rcA} B(build form)={rcB} C(seam)={rcC}  names={names(outA + outB + outC)}")
say(f"     BUILD DOOR: home absent (POLARITY_BRAIN_DIR=/nowhere) — the build loop routes rc {rcB} as {kind.upper() if isinstance(kind, str) else kind} (was 77 = COULD-NOT-ASK, build continued)")
say(f"     ⛔ {first_refused(outA)[:170]}")
# D2: the fake-repo stand-in, exactly as V built it (wave3 lines 195-227), dirty tree + clean redirect
FAKE = os.path.join(F, "fakerepo-standalone")
if os.path.exists(FAKE):
    shutil.move(FAKE, os.path.join(F, "_graveyard", f"fakerepo-standalone-{os.getpid()}"))
os.makedirs(os.path.join(FAKE, "knowledge"))
for fn in ("_validate_polarities.py", "_helpgate.py", "_could_not_ask.py", "_rulings.json"):
    shutil.copy2(os.path.join(KNOW, fn), os.path.join(FAKE, "knowledge", fn))
for relp in ("notes/_subreports/assets/2026-09-02-237-T-tensions-schema/open-tensions.json",
             "notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json"):
    os.makedirs(os.path.dirname(os.path.join(FAKE, relp)), exist_ok=True)
    shutil.copy2(os.path.join(REPO, relp), os.path.join(FAKE, relp))
shutil.copytree(REAL, os.path.join(FAKE, "knowledge", "brain"))
mj(os.path.join(FAKE, "knowledge", "brain", "polarities.json"), lambda o: o["polarities"][0].__setitem__("status", "open"))
rc0, out0 = run(["bash", os.path.join(F, "_seam_block.sh")], cwd=FAKE)
rc1, out1 = run(["bash", os.path.join(F, "_seam_block.sh")], {"POLARITY_BRAIN_DIR": REAL}, cwd=FAKE)
declared = [ln for ln in out1.splitlines() if "REDIRECTED to" in ln]
d2 = "CAUGHT" if (rc0 == 1 and rc1 == 1 and "R5-TYPED-STATUS" in out1 and declared) else "ESCAPED"
V["D2"] = d2
say(f" D2  PROMISED  {d2:8}  (a) no env rc={rc0} names={names(out0)} · (b) POLARITY_BRAIN_DIR=<clean copy> rc={rc1} names={names(out1)}")
say(f"     SEAM DOOR: the redirect is DECLARED and the tree's own home is gated: {declared[0][:120] if declared else 'NO DECLARED LINE'}")
say(f"     ✗ {[ln for ln in out1.splitlines() if ln.startswith('✗')][0][:170] if any(ln.startswith('✗') for ln in out1.splitlines()) else ''}")
# argv rows
say("")
T = fresh("A1")
ep = os.path.join(ROOT, "entry-A1.json")
json.dump({"id": "pl-90", "parties": [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}], "mediating_variable": "x", "links": [], "sources": [{"path": "x", "id": "y"}]}, open(ep, "w"))
h0 = tree(T)
rc, out = run([PY, VAL, "--add-polarity", ep, "--dry-run", "--write", "--brain", T])
a1 = "CAUGHT" if rc == 2 and tree(T) == h0 else "ESCAPED"
V["A1"] = a1
say(f" A1  PROMISED  {a1:8}  rc={rc} file-changed={tree(T) != h0}   --add-polarity FILE --dry-run --write")
say(f"     ⛔ {out.strip().splitlines()[-1][:170] if out.strip() else ''}")
T = fresh("A2")
h0 = tree(T)
rc, out = run([PY, VAL, "--check", "--write", "--brain", T])
a2 = "CAUGHT" if rc == 2 and tree(T) == h0 else "ESCAPED"
V["A2"] = a2
say(f" A2  PROMISED  {a2:8}  rc={rc} _generated-changed={tree(T) != h0}   --check --write")
say(f"     ⛔ {out.strip().splitlines()[-1][:170] if out.strip() else ''}")

# ---- TOTALS ----------------------------------------------------------------------------------------------
say("")
grades = {"RULED": [30, 31, 32, 110, 111, 112, 210, 211, 212, 213, 216, 230, 231, 232, 233, 310],
          "PROMISED": [22, 70, 71, 82, 83, 93, 214, 220, 222, 223, 224, 234, 246, 247, 300, 311, 312, 400, 401, 403, 324, 328, "D1", "D2", "A1", "A2"],
          "UNRULED": [241, 243, 244, 245, 301, 402]}
still = {g: [k for k in ks if V[k] != "CAUGHT"] for g, ks in grades.items()}
caught = sum(1 for k in V if V[k] == "CAUGHT")
say(f"TOTAL: {len(V)} rows re-driven · CAUGHT {caught} · still ESCAPED {len(V) - caught} "
    f"(RULED {len(still['RULED'])} · PROMISED {len(still['PROMISED'])} · UNRULED {len(still['UNRULED'])})")
for g in ("RULED", "PROMISED", "UNRULED"):
    say(f"  {g:8}: {len(grades[g]) - len(still[g])}/{len(grades[g])} caught" + (f" · STILL ESCAPING: {still[g]}" if still[g] else ""))
say(f"  verdict per row: {json.dumps({str(k): v for k, v in V.items()})}")
for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "escaped-now-caught.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(LINES) + "\n")
