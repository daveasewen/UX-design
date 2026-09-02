#!/usr/bin/env python3
"""#238 lane V — ADVERSARIAL harness for the polarity gate (s238-D7).

Every hostile row is applied to a COPY of knowledge/brain/ and driven through the THREE REAL DOORS:
  A  CLI      python3 knowledge/_validate_polarities.py --check --brain <copy>
  B  BUILD    the _build_all.py STEPS entry in the build's own `[sys.executable, path] + args` form,
              env POLARITY_BRAIN_DIR=<copy>, then route(label) for the remedy (never the whole build)
  C  SEAM     the `# ── POLARITY GATE — s238-D7` block of knowledge/_git_commit.sh, extracted verbatim
              between its marker and `fi`, run in a throwaway bash with fail() defined (never a commit)
then through the WRITE door on a second copy:
  W  --write --brain <copy-w>   (the decisive door: it either ACCEPTS the home and re-derives, or
              refuses by NAME and leaves every byte)
and, when W accepted, doors A/B/C again on the post-write copy ("the author ran --write" state).

A mutation of the HOME makes the derived files STALE, so the as-committed doors go red on
STALE-GENERATED regardless of the refusal under probe. The decisive state for a home mutation is
therefore AFTER --write; for a mutation of a GENERATED file (or a stray file) it is AS-IS.

Verdicts (expect = what a correct gate SHOULD do, the adversary's reading of the rulings):
  CAUGHT      expect red · decisive doors all rc!=0 · the expected NAME printed · no traceback · nothing written
  ESCAPED     expect red · some decisive door rc 0
  MISNAMED    expect red · red, but the expected name is not printed (another name, or none)
  CRASH       expect red · red only by an uncaught traceback (a crash is not a fail)
  WROTE       expect red · a refusing door changed bytes
  GREEN-OK    expect green · every decisive door rc 0
  FALSE-RED   expect green · a decisive door refused a legal row
Nothing under the live repo is touched: copies under /sessions/wonderful-adoring-euler/mnt/outputs/v238/arms/.
"""
import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys

REPO = "/sessions/keen-serene-johnson/mnt/UX-design"
KNOW = os.path.join(REPO, "knowledge")
V = "/sessions/keen-serene-johnson/mnt/outputs/f239"
REAL = os.path.join(V, "brain-real")
ARMS = os.path.join(V, "arms")
GRAVE = os.path.join(V, "_graveyard")
VALIDATOR = os.path.join(KNOW, "_validate_polarities.py")
PY = sys.executable

sys.path.insert(0, KNOW)
_argv = sys.argv
sys.argv = ["x"]
with contextlib.redirect_stdout(io.StringIO()):
    import _build_all as b  # noqa: E402
sys.argv = _argv
STEP = [s for s in b.STEPS if s[1] == "_validate_polarities.py" and "--check" in s[2]][0]
KIND, REMEDY = b.route(STEP[0])
assert KIND == b.GATE, KIND

# the seam block, extracted verbatim (marker → first `fi`), wrapped with fail() like P's probe
_seam_src = open(os.path.join(KNOW, "_git_commit.sh"), encoding="utf-8").read().splitlines()
_blk, _on = [], False
for ln in _seam_src:
    if ln.startswith("# ── POLARITY GATE — s238-D7"):
        _on = True
    if _on:
        _blk.append(ln)
        if ln == "fi":
            break
assert _blk and _blk[-1] == "fi", "seam block not found"
SEAM_SH = os.path.join(V, "_seam_block.sh")
with open(SEAM_SH, "w", encoding="utf-8") as f:
    f.write("set -u\nfail() { echo \"✗ $1\" >&2; exit 1; }\n" + "\n".join(_blk) + "\necho SEAM-BLOCK-EXIT-0\n")


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tree(root):
    out = {}
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            out[os.path.relpath(p, root)] = sha(p)
    return out


def names(out):
    # the seam's own line says "polarity gate REFUSED (s238-D7)" — a ruling id, not a refusal name
    return sorted(n for n in set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out)) if not re.match(r"^s\d+-D\d+$", n))


def run(cmd, env_extra=None):
    env = dict(os.environ)
    env.pop("POLARITY_BRAIN_DIR", None)
    env.pop("POLARITY_ACK", None)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def door_cli(brain):
    return run([PY, VALIDATOR, "--check", "--brain", brain])


def door_build(brain):
    return run([PY, os.path.join(KNOW, STEP[1])] + list(STEP[2]), {"POLARITY_BRAIN_DIR": brain})


def door_seam(brain):
    return run(["bash", SEAM_SH], {"POLARITY_BRAIN_DIR": brain})


def door_write(brain):
    return run([PY, VALIDATOR, "--write", "--brain", brain])


def fresh_copy(dst):
    if os.path.exists(dst):
        os.makedirs(GRAVE, exist_ok=True)
        shutil.move(dst, os.path.join(GRAVE, os.path.basename(dst) + "-" + str(os.getpid())))
    shutil.copytree(REAL, dst)
    return dst


def mutate_json(path, fn):
    obj = json.loads(open(path, encoding="utf-8").read())
    fn(obj)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def pol(fn):
    return lambda d: mutate_json(os.path.join(d, "polarities.json"), fn)


def stubs(fn):
    return lambda d: mutate_json(os.path.join(d, "stubs.json"), fn)


def schema(fn):
    return lambda d: mutate_json(os.path.join(d, "schema", "polarity.schema.json"), fn)


def principles(fn):
    return lambda d: mutate_json(os.path.join(d, "principles.json"), fn)


RESULTS = []


def arm(n, slug, expect, mutate, must_name=None, decisive="after-write", basis="", note=""):
    d = os.path.join(ARMS, f"{n:02d}-{slug}")
    if os.path.exists(d):
        os.makedirs(GRAVE, exist_ok=True)
        shutil.move(d, os.path.join(GRAVE, os.path.basename(d) + "-" + str(os.getpid())))
    os.makedirs(d)
    brain = fresh_copy(os.path.join(d, "brain"))
    try:
        mutate(brain)
    except Exception as e:  # noqa: BLE001
        RESULTS.append(dict(n=n, slug=slug, expect=expect, verdict="SETUP-CRASH", note=f"mutation setup crashed: {e!r}",
                            basis=basis, must=must_name, decisive=decisive))
        return
    h0 = tree(brain)
    asis = {}
    for k, fn in (("A", door_cli), ("B", door_build), ("C", door_seam)):
        rc, out = fn(brain)
        asis[k] = dict(rc=rc, names=names(out), crash="Traceback" in out, out=out)
    untouched_asis = tree(brain) == h0
    # the write door on a second copy of the SAME mutant
    brain_w = os.path.join(d, "brain-w")
    shutil.copytree(brain, brain_w)
    hw0 = tree(brain_w)
    homes0 = {k: v for k, v in hw0.items() if not k.startswith("_generated/")}
    rcw, outw = door_write(brain_w)
    hw1 = tree(brain_w)
    homes1 = {k: v for k, v in hw1.items() if not k.startswith("_generated/")}
    w = dict(rc=rcw, names=names(outw), crash="Traceback" in outw, out=outw,
             homes_untouched=homes0 == homes1, gen_untouched=hw0 == hw1)
    after = {}
    if rcw == 0:
        h1 = tree(brain_w)
        for k, fn in (("A", door_cli), ("B", door_build), ("C", door_seam)):
            rc, out = fn(brain_w)
            after[k] = dict(rc=rc, names=names(out), crash="Traceback" in out, out=out)
        untouched_after = tree(brain_w) == h1
    else:
        untouched_after = True
    # ---- verdict on the DECISIVE state ----
    if decisive == "as-is":
        doors = dict(asis)
        doors["W"] = w
    else:
        doors = dict(after) if after else {}
        doors["W"] = w
    rcs = {k: v["rc"] for k, v in doors.items()}
    allnames = sorted(set(sum((v["names"] for v in doors.values()), [])))
    crashed = any(v["crash"] for v in doors.values())
    if expect == "red":
        if decisive == "as-is":
            red_all = all(rcs[k] != 0 for k in ("A", "B", "C"))
            green_any = any(rcs[k] == 0 for k in ("A", "B", "C"))
        else:
            # after-write: the write door ACCEPTING the home is the escape (the doors after it are green)
            red_all = rcs["W"] != 0
            green_any = rcs["W"] == 0
        if green_any:
            verdict = "ESCAPED"
        elif crashed:
            verdict = "CRASH"
        elif must_name and must_name not in allnames:
            verdict = "MISNAMED"
        elif not (untouched_asis and (w["gen_untouched"] if rcw != 0 else w["homes_untouched"])):
            verdict = "WROTE"
        elif red_all:
            verdict = "CAUGHT"
        else:
            verdict = "MIXED"
    else:
        if decisive == "as-is":
            ok = all(rcs[k] == 0 for k in ("A", "B", "C"))
        else:
            ok = rcs["W"] == 0 and after and all(after[k]["rc"] == 0 for k in ("A", "B", "C"))
        verdict = "GREEN-OK" if ok else "FALSE-RED"
    RESULTS.append(dict(n=n, slug=slug, expect=expect, must=must_name, decisive=decisive, basis=basis, note=note,
                        verdict=verdict, asis={k: (v["rc"], v["names"], v["crash"]) for k, v in asis.items()},
                        write=(rcw, w["names"], w["crash"], w["homes_untouched"], w["gen_untouched"]),
                        after={k: (v["rc"], v["names"], v["crash"]) for k, v in after.items()},
                        untouched_asis=untouched_asis, untouched_after=untouched_after,
                        first_line=next((ln.strip() for ln in (w["out"] if rcw else "").splitlines() if "REFUSED (" in ln), "")
                        or next((ln.strip() for ln in asis["A"]["out"].splitlines() if "REFUSED (" in ln), ""),
                        cmd=f"python3 knowledge/_validate_polarities.py --check --brain {brain}  "
                            f"·  --write --brain {brain_w}"))
    with open(os.path.join(d, "doors.txt"), "w", encoding="utf-8") as f:
        f.write(f"ARM {n:02d} {slug}\nexpect {expect} must {must_name} decisive {decisive}\n{basis}\n{note}\n")
        for k, v in asis.items():
            f.write(f"\n===== AS-IS door {k} rc={v['rc']} names={v['names']} crash={v['crash']}\n{v['out']}\n")
        f.write(f"\n===== WRITE rc={rcw} names={w['names']} crash={w['crash']} homes_untouched={w['homes_untouched']} gen_untouched={w['gen_untouched']}\n{outw}\n")
        for k, v in after.items():
            f.write(f"\n===== AFTER-WRITE door {k} rc={v['rc']} names={v['names']} crash={v['crash']}\n{v['out']}\n")


def table():
    lines = []
    hdr = f"{'#':>3} {'verdict':9} {'exp':5} {'decisive':11} {'as-is A/B/C':>15} {'W':>3} {'after A/B/C':>12}  arm"
    lines.append(hdr)
    lines.append("-" * len(hdr))
    for r in RESULTS:
        if r["verdict"] == "SETUP-CRASH":
            lines.append(f"{r['n']:>3} {r['verdict']:9} {r['expect']:5} {r['decisive']:11} {'':>15} {'':>3} {'':>12}  {r['slug']}  :: {r['note']}")
            continue
        a = "/".join(str(r["asis"][k][0]) for k in "ABC")
        af = "/".join(str(r["after"][k][0]) for k in "ABC") if r["after"] else "-"
        lines.append(f"{r['n']:>3} {r['verdict']:9} {r['expect']:5} {r['decisive']:11} {a:>15} {r['write'][0]:>3} {af:>12}  {r['slug']}")
        nm = sorted(set(r["write"][1]) | set(sum((v[1] for v in r["asis"].values()), [])) | set(sum((v[1] for v in r["after"].values()), [])))
        lines.append(f"{'':>3} {'':9} {'':5} {'':11} names={nm} must={r['must']} untouched(as-is)={r['untouched_asis']} write(homes,gen)untouched=({r['write'][3]},{r['write'][4]})")
        if r["first_line"]:
            lines.append(f"{'':>3} {'':9} {'':5} {'':11} first: {r['first_line'][:150]}")
        if r["note"]:
            lines.append(f"{'':>3} {'':9} {'':5} {'':11} note: {r['note']}")
    c = {}
    for r in RESULTS:
        c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    lines.append("-" * len(hdr))
    lines.append("verdicts: " + " · ".join(f"{k} {v}" for k, v in sorted(c.items())) + f" · arms {len(RESULTS)}")
    return "\n".join(lines)


def dump(path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, indent=1, ensure_ascii=False)
