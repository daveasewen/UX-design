#!/usr/bin/env python3
"""_gate_scratch_hygiene.py — VM-disk scratch litter probe. Born ADVISORY at #227.

WHY THIS EXISTS (measured #227, 2026-08-30). The Cowork sandbox VM disk (~9.6G) PERSISTS
across sessions, but each session runs as a THROWAWAY Linux user. `/var/tmp` carries the
sticky bit, so a file that outlives its session user is PERMANENTLY UNDELETABLE from inside
the VM — no root, `sudo` is disabled by the container's no-new-privileges flag. At #227 boot
the VM was 100% full (3.2G of orphaned session scratch: the #220 playwright browsers at 984M,
bake twins, dry-runs) and the sandbox could not even create its user — FIVE identical
`useradd: No space left on device` failures before a host restart got a shell.

⇒ THE ONLY MOMENT SCRATCH CAN BE CLEANED IS WHILE ITS OWNER STILL EXISTS. This probe names,
at wrap time, every file the CURRENT session user owns on the VM disk, so the wrap can remove
it before the user dies and the file becomes a permanent squatter.

⛔ ADVISORY, DELIBERATELY. Promotion to blocking is Dave's (derivation governance; the
`_gate_pack_imports.py` precedent — born advisory #220). A blocking gate here could strand a
wrap over litter the wrap can still fix, which is backwards.

⚠ WHAT IT CANNOT SEE: litter owned by DEAD users is reported as a TOTAL ONLY — it is
unremovable and the number exists so drift is visible, not actionable. The actionable list is
strictly the current user's files.

★★ #294 `s294-D12` — AND A SECOND, IN-REPO HOLDING DIRECTORY IS NOW MEASURED HERE: `_to_delete/`.
Everything above is about scratch OUTSIDE the repository, and #293's own wrap wrote that
"`_to_delete/` is still an accumulating squatter that `4c` does not reach". It was literally
true: `SCRATCH_ROOTS` is `/var/tmp`, `/tmp`, `~/tmp`, `~/.cache` (+ `~/.local` on `--wrap`) —
every one outside the repo — and this file mentioned `_to_delete` zero times. Measured at
2026-09-21: 108 top-level entries, oldest 2026-08-06 (46 days). `to_delete_backlog()` below
derives each entry's SESSION (not its age in days) and names every entry older than
`TO_DELETE_MAX_AGE_SESSIONS`, which is **3** — Dave's figure, "N+3 is fine".
⛔ PURGING IS NOT THIS ARM'S JOB. `s282-D4` records that on this mount the unlink is refused, so
there is nothing to remove from inside; the arm NAMES the entries and stops. The remedy is
outside the repo and it is Dave's.

Exit codes: 0 on a plain run (advisory, as born). ⛔ `--wrap` now exits 1 when `_to_delete/`
holds an entry older than 3 sessions (`s294-D12`: "the arm refuses on a `--wrap` run only; on a
plain run it reports") — and because NOTHING consumes this script's exit code, the REFUSAL WITH
TEETH is seated in `_capture_gate.py`'s wrap checks, which `_git_commit.sh --wrap` does consume.
It calls `to_delete_backlog()` here rather than re-implementing it. `--selftest` exits 1 on a
failed arm.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import os, pwd, re, shutil, subprocess, sys

SCRATCH_ROOTS = ["/var/tmp", "/tmp",
                 # #283 (s283-D1, Dave: "make this a regular check - more mechanical"): the SESSION
                 # HOME is on the same persistent /sessions disk and is NEVER removed when the
                 # session user dies — 127 dead homes held 4.8G at #283. Our own residue per lane
                 # (~38M: tokenizer cache, pip) is the ONE part of that leak we can stop.
                 os.path.expanduser("~/tmp"), os.path.expanduser("~/.cache")]
# wrap-only: ~/.local holds the session's pip installs (tiktoken) — the gauge needs it until the
# very end, so it is cleaned by `--clean --wrap` (ritual step 4c), never at a lane seam.
WRAP_ONLY_ROOTS = [os.path.expanduser("~/.local")]
KEEP = ("/tmp/gitshim",)   # the mount's git shim — 4c deleted it at #282; named as kept, never removed
FILL_WARN_PCT = 80


# ── ★★ `s294-D12` — `_to_delete/`, THE IN-REPO HOLDING DIRECTORY, AGED IN SESSIONS ───────────
TO_DELETE_DIRNAME = "_to_delete"
# ⚠ N = 3 AND IT IS DAVE'S, said in the same breath as "inscribe": "N+3 is fine". It is the one
# figure the review page left open, and it is not a seat's to re-dial.
TO_DELETE_MAX_AGE_SESSIONS = 3
# ⛔ SESSIONS, NOT DAYS, and the derivation is stated because the ruling asks WHICH. TWO sources,
# in this order:
#   (1) THE ENTRY'S OWN NAME, when it carries a session: `_s276-D6-lane-ownership-guard`,
#       `286-V-symlinks`, `_217-entry-inputs`. Preferred because it is the author's own label.
#       ⚠ MEASURED 2026-09-21: only 40 of 108 entries carry one, so name-only would silently
#       excuse 68 entries — an exemption by naming habit [[unmatched-grep-is-not-an-absence]].
#   (2) THE NEWEST COMMIT OLDER THAN THE ENTRY'S MTIME, whose subject carries `#N` (either T3
#       shape — `#N <date> — ` or `after #N <date> — `). This covers every entry, and it is a
#       repo fact rather than a filesystem one: mtimes survive a move, session numbers do not lie
#       about which ritual an entry belongs to.
# An entry no source can date is reported as UNDATED and, deliberately, does NOT refuse: a gate
# that blocks on its own blind spot teaches the next session to delete the evidence.
# ⚠ `(?=[-_]|$)` and not a bare boundary: `_s129` (a whole entry name, measured live) must derive
# by NAME, while `_stale_pycache-116` must NOT — the digits have to be the name's own head.
ENTRY_SESSION_RE = re.compile(r"^_?[sS]?(\d{2,4})(?=[-_]|$)")
COMMIT_SESSION_RE = re.compile(r"^(?:after\s+)?#(\d+)\b")


def _me():
    return pwd.getpwuid(os.getuid()).pw_name


def _repo_root(start=None):
    """The nearest ancestor holding `.git`, or None. This file lives in `<repo>/knowledge/`."""
    d = os.path.abspath(start or os.path.dirname(os.path.abspath(__file__)))
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def _commit_timeline(repo, limit=4000):
    """[(committer_epoch, session_n)] newest-first, or None if git could not answer."""
    try:
        r = subprocess.run(["git", "-C", repo, "log", "-n", str(limit), "--format=%ct%x09%s"],
                           capture_output=True, text=True, timeout=60)
    except Exception:                                                 # noqa: BLE001
        return None
    if r.returncode != 0:
        return None
    out = []
    for line in r.stdout.splitlines():
        ct, _tab, subj = line.partition("\t")
        m = COMMIT_SESSION_RE.match(subj.strip())
        if m and ct.strip().isdigit():
            out.append((int(ct), int(m.group(1))))
    return out


def entry_session(name, mtime, timeline):
    """(session_n, how) for one top-level entry. `session_n` is None when neither source dates it."""
    m = ENTRY_SESSION_RE.match(name)
    if m:
        return int(m.group(1)), "name"
    for ct, n in (timeline or []):          # newest-first: the first one older than the mtime
        if ct <= mtime:
            return n, "commit"
    return None, "undated"


def to_delete_backlog(repo=None, max_age=None):
    """`s294-D12` — age `_to_delete/`'s TOP-LEVEL entries in SESSIONS. Returns a dict:

      {"ran": bool, "why": str|None, "dir": path, "current": int|None, "max_age": int,
       "entries": N, "stale": [(name, session_n, how, age_in_sessions)], "undated": [names]}

    `ran` False means the backlog could not be aged and the caller must say so rather than pass:
    an unmeasured directory is not an empty one. Top-level only — an entry's tree goes with it.
    ⛔ READ-ONLY. It never removes anything (`s282-D4`: the mount refuses unlink anyway).
    """
    max_age = TO_DELETE_MAX_AGE_SESSIONS if max_age is None else max_age
    repo = repo or _repo_root()
    res = {"ran": False, "why": None, "dir": None, "current": None, "max_age": max_age,
           "entries": 0, "stale": [], "undated": []}
    if not repo:
        res["why"] = ("no git repository found above this file, so `_to_delete/` has no home to "
                      "be measured in and no commit timeline to age against")
        return res
    d = os.path.join(repo, TO_DELETE_DIRNAME)
    res["dir"] = d
    if not os.path.isdir(d):
        res["ran"] = True                   # a truly absent holding directory IS the clean case
        return res
    timeline = _commit_timeline(repo)
    if timeline is None or not timeline:
        res["why"] = (f"`git log` gave no session-bearing subject under {repo}, so an entry's "
                      f"session cannot be derived from the commit timeline — UNKNOWN, not clean")
        return res
    res["current"] = max(n for _ct, n in timeline[:1]) if timeline else None
    res["ran"] = True
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        try:
            mtime = os.lstat(p).st_mtime
        except OSError:
            continue
        res["entries"] += 1
        n, how = entry_session(name, mtime, timeline)
        if n is None:
            res["undated"].append(name)
            continue
        age = res["current"] - n
        if age > max_age:
            res["stale"].append((name, n, how, age))
    res["stale"].sort(key=lambda t: (-t[3], t[0]))
    return res


def to_delete_lines(repo=None, max_age=None, show=12):
    """The human/machine lines for the backlog. Returns (refusals, notes) — both lists of str.

    `refusals` is non-empty ONLY when the arm has a measured population older than N sessions.
    The caller decides whether a refusal blocks (`--wrap` here; FAILS in `_capture_gate`)."""
    b = to_delete_backlog(repo, max_age)
    refusals, notes = [], []
    if not b["ran"]:
        notes.append(f"⚠ `_to_delete/` BACKLOG NOT MEASURED (`s294-D12`) — {b['why']}. NOT a "
                     f"pass: the holding directory was never aged.")
        return refusals, notes
    if b["dir"] is None or not os.path.isdir(b["dir"] or ""):
        notes.append(f"· no `{TO_DELETE_DIRNAME}/` in this tree — nothing held, nothing to age.")
        return refusals, notes
    if b["undated"]:
        notes.append(f"⚠ `_to_delete/`: {len(b['undated'])} top-level entr"
                     f"{'y' if len(b['undated']) == 1 else 'ies'} carry NO session in the name "
                     f"and predate every commit in the timeline, so they are UNDATED and are "
                     f"reported rather than refused on: {', '.join(b['undated'][:6])}"
                     f"{' …' if len(b['undated']) > 6 else ''}")
    if not b["stale"]:
        notes.append(f"· `_to_delete/`: {b['entries']} top-level entr"
                     f"{'y' if b['entries'] == 1 else 'ies'}, none older than "
                     f"{b['max_age']} sessions (current #{b['current']}) — `s294-D12` clean.")
        return refusals, notes
    named = " · ".join(f"{n} (#{s} by {how}, {age} sessions)"
                       for n, s, how, age in b["stale"][:show])
    more = f" … and {len(b['stale']) - show} more" if len(b["stale"]) > show else ""
    refusals.append(
        f"`_to_delete/` BACKLOG (`s294-D12`, Dave: N+3): {len(b['stale'])} of {b['entries']} "
        f"top-level entries are OLDER THAN {b['max_age']} SESSIONS against the current session "
        f"#{b['current']}. ⛔ WHAT IS FORBIDDEN, QUOTED: a wrap while `{TO_DELETE_DIRNAME}/` "
        f"holds any top-level entry whose session is more than {b['max_age']} behind the current "
        f"one. Age is in SESSIONS, not days — derived from the entry's own name when it carries "
        f"one (`_s276-D6-…`), otherwise from the newest commit older than its mtime. THE "
        f"ENTRIES: {named}{more}. ⛔ PURGING IS NOT THIS ARM'S JOB and is not attempted: "
        f"`s282-D4` records that this mount refuses unlink, so the remedy is OUTSIDE the "
        f"repository and it is Dave's — the arm names them and stops. `{TO_DELETE_DIRNAME}/` is "
        f"gitignored, so nothing here is in any commit.")
    return refusals, notes


def vm_fill_pct(path="/"):
    t = shutil.disk_usage(path)
    return round(100 * t.used / t.total, 1), t.free


def mine(roots=None, user=None):
    """Paths under the scratch roots owned by `user` (default: current user). Top-level only —
    removal of a top-level entry takes its tree with it."""
    user = user or _me()
    out = []
    for root in (roots or SCRATCH_ROOTS):
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            p = os.path.join(root, name)
            try:
                if pwd.getpwuid(os.lstat(p).st_uid).pw_name == user:
                    out.append(p)
            except (KeyError, OSError):
                continue  # dead owner or vanished — not ours, not actionable
    return out


def orphan_bytes(roots=None):
    """Total bytes under the roots NOT owned by the current user — the unremovable residue."""
    me_uid = os.getuid()
    total = 0
    for root in (roots or SCRATCH_ROOTS):
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            for f in filenames:
                try:
                    st = os.lstat(os.path.join(dirpath, f))
                    if st.st_uid != me_uid:
                        total += st.st_size
                except OSError:
                    continue
    return total


def report(clean=False, wrap=False):
    pct, free = vm_fill_pct()
    tag = "⚠" if pct >= FILL_WARN_PCT else "·"
    print(f"{tag} VM disk fill {pct}% · free {free // 1024}K")
    own = mine()
    if own:
        print(f"⚠ {len(own)} scratch entr{'y' if len(own) == 1 else 'ies'} owned by "
              f"{_me()} — REMOVABLE NOW ONLY (the owner dies with the session):")
        for p in own:
            if p in KEEP:
                print(f"    {p}  → KEPT (keep-list)"); continue
            print(f"    {p}" + ("  → removed" if clean and _rm(p) else ""))
    else:
        print(f"· no scratch owned by {_me()} under {', '.join(SCRATCH_ROOTS)} — clean wrap")
    ob = orphan_bytes()
    if ob:
        print(f"· {ob // (1024 * 1024)}M owned by dead sessions — UNREMOVABLE from inside "
              f"(named for drift visibility, not action)")
    # ---- ★★ `s294-D12` — the in-repo holding directory. REPORTS on a plain run; on `--wrap` the
    # refusal is the exit code, because that is the only run the ruling makes it refuse.
    refusals, notes = to_delete_lines()
    for n in notes:
        print(f"{n}")
    for r in refusals:
        print(("⛔ WRAP REFUSED — " if wrap else "⚠ REPORTED (a plain run; `--wrap` refuses) — ")
              + r)
    return 1 if (wrap and refusals) else 0  # advisory except the `s294-D12` --wrap arm


def _rm(p):
    try:
        subprocess.run(["rm", "-rf", p], capture_output=True, timeout=120)
        return not os.path.exists(p)
    except Exception:
        return False


def selftest():
    fails = []
    import tempfile
    td = tempfile.mkdtemp(prefix="shy-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    try:
        # arm 1: a file I own under a scratch root IS seen
        probe = os.path.join(td, "litter.bin")
        open(probe, "w").write("x")
        seen = mine(roots=[td])
        if probe not in seen:
            fails.append(f"[own-file seen] expected {probe} in {seen}")
        # arm 2: an empty root reports clean
        empty = os.path.join(td, "empty"); os.makedirs(empty)
        if mine(roots=[empty]):
            fails.append("[empty clean] empty root reported litter")
        # arm 3: fill pct is a sane percentage
        pct, _ = vm_fill_pct()
        if not (0 <= pct <= 100):
            fails.append(f"[fill sane] {pct}")
    finally:
        shutil.rmtree(td, ignore_errors=True)
    fails += selftest_to_delete()
    n = 3 + 8
    print("\n".join(fails) if fails
          else f"scratch-hygiene selftest: {n} arms, all GREEN (3 scratch + 8 `s294-D12`)")
    return 1 if fails else 0


def selftest_to_delete():
    """★★ `s294-D12` — PLANT-THEN-DETECT on a real git repo with a real `_to_delete/`.

    ⛔ The two arms that matter are the NEGATIVES: a RECENT entry must not refuse (or the gate is
    "refuse always" wearing a measurement's clothes), and an UNDATED entry must not refuse (or
    the gate blocks on its own blind spot and the remedy becomes deleting the evidence).
    """
    import tempfile, time
    fails = []
    now = int(time.time())
    # ---- pure-function arms first: the session derivation itself, both sources.
    timeline = [(now - 1000, 294), (now - 200000, 290), (now - 900000, 280)]
    for name, mtime, want_n, want_how in (
            ("_s276-D6-lane-ownership-guard", now, 276, "name"),
            ("286-V-symlinks", now, 286, "name"),
            ("_217-entry-inputs", now, 217, "name"),
            ("_stale_pycache-116", now - 1000, 294, "commit"),   # no session IN the name
            ("outputs_wrap110_part1.py.1786015959", now - 200000, 290, "commit"),
            ("logos-identifier-282", now - 1_000_000, None, "undated")):
        got_n, got_how = entry_session(name, mtime, timeline)
        if (got_n, got_how) != (want_n, want_how):
            fails.append(f"[s294-D12 session derivation] `{name}` → ({got_n}, {got_how}), "
                         f"expected ({want_n}, {want_how}) — the arm ages the wrong object")
    # ---- and the arms on a real tree.
    td = tempfile.mkdtemp(prefix="s294d12-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    try:
        git = ["git", "-C", td, "-c", "user.email=t@t", "-c", "user.name=t"]
        try:
            if subprocess.run(git[:3] + ["init", "-q"], capture_output=True,
                              timeout=30).returncode != 0:
                raise RuntimeError("git init failed")
            open(os.path.join(td, "x.txt"), "w").write("x\n")
            subprocess.run(git + ["add", "-A"], capture_output=True, timeout=30)
            subprocess.run(git + ["commit", "-qm", "#294 2026-09-21 — the wrap"],
                           capture_output=True, timeout=30)
        except Exception as e:                                        # noqa: BLE001
            fails.append(f"[s294-D12] git unavailable in this checkout ({e}) — the tree arms "
                         f"did not run, which is DECLARED, not green")
            return fails
        hold = os.path.join(td, TO_DELETE_DIRNAME)

        # arm A: NO `_to_delete/` at all ⇒ ran, clean, no refusal.
        r_, n_ = to_delete_lines(repo=td)
        if r_ or not any("nothing held" in x for x in n_):
            fails.append(f"[s294-D12 absent] an absent holding directory must be the clean case — "
                         f"refusals={r_} notes={n_}")

        # arm B: a RECENT entry (this session) ⇒ no refusal. The negative control.
        os.makedirs(os.path.join(hold, "_s294-B-fresh"))
        r_, n_ = to_delete_lines(repo=td)
        if r_:
            fails.append(f"[s294-D12 recent] an entry from the CURRENT session refused — the arm "
                         f"is 'refuse always', not a measurement: {r_}")
        if not any("none older than 3 sessions" in x for x in n_):
            fails.append(f"[s294-D12 recent] the clean case left no note stating what it "
                         f"measured: {n_}")

        # arm C: the boundary. N = 3 means 3 sessions behind PASSES, 4 REFUSES — the figure is
        # Dave's and an off-by-one here re-dials his ruling silently.
        os.makedirs(os.path.join(hold, "_s291-exactly-three-back"))
        if to_delete_lines(repo=td)[0]:
            fails.append("[s294-D12 boundary] #291 is exactly 3 sessions behind #294 and must "
                         "PASS — N=3 is Dave's figure ('N+3 is fine'), and >N is the condition")
        os.makedirs(os.path.join(hold, "_s290-four-back"))
        r_, _n = to_delete_lines(repo=td)
        if not any("_s290-four-back" in x for x in r_):
            fails.append(f"[s294-D12 stale] an entry 4 sessions behind did NOT refuse — the gate "
                         f"does not bite: {r_}")

        # arm D: the refusal must NAME the entry and quote what it forbids, and must not claim a
        # purge it cannot do (`s282-D4`: this mount refuses unlink).
        blob = " ".join(to_delete_lines(repo=td)[0])
        for needle in ("WHAT IS FORBIDDEN", "_s290-four-back", "s282-D4", "SESSIONS, not days"):
            if needle not in blob:
                fails.append(f"[s294-D12 refusal text] the refusal does not carry `{needle}` "
                             f"[[gate-must-quote-what-it-forbids]]")

        # arm E: an UNDATED entry (no session in the name, mtime older than every commit) is
        # REPORTED, never refused on. The second negative control.
        shutil.rmtree(os.path.join(hold, "_s290-four-back"))
        u = os.path.join(hold, "logos-identifier-282-nope")
        os.makedirs(u)
        os.utime(u, (0, 0))
        r_, n_ = to_delete_lines(repo=td)
        if any("logos-identifier-282-nope" in x for x in r_):
            fails.append("[s294-D12 undated] an entry the arm cannot date was REFUSED on — a "
                         "gate that blocks on its own blind spot teaches the next session to "
                         "delete the evidence")
        if not any("UNDATED" in x for x in n_):
            fails.append(f"[s294-D12 undated] the undated entry was not reported at all — the "
                         f"blind spot is silent, which is worse than loud: {n_}")

        # arm F: TOP-LEVEL ONLY — a stale-named file nested inside a fresh entry is not an entry.
        open(os.path.join(hold, "_s294-B-fresh", "_s200-deep.txt"), "w").write("x\n")
        if any("_s200-deep" in x for x in to_delete_lines(repo=td)[0]):
            fails.append("[s294-D12 top-level] a nested path was aged as a top-level entry — "
                         "removal of a top-level entry takes its tree with it, so the population "
                         "is top-level or the counts are meaningless")

        # arm G: a repo with NO session-bearing commit ⇒ NOT MEASURED, never clean.
        td2 = tempfile.mkdtemp(prefix="s294d12b-",
                               dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
        try:
            subprocess.run(["git", "-C", td2, "init", "-q"], capture_output=True, timeout=30)
            os.makedirs(os.path.join(td2, TO_DELETE_DIRNAME, "_s100-ancient"))
            r_, n_ = to_delete_lines(repo=td2)
            if r_ or not any("NOT MEASURED" in x and "NOT a pass" in x for x in n_):
                fails.append(f"[s294-D12 unknown] a repo with no session-bearing commit must "
                             f"declare UNKNOWN, not grade or pass — refusals={r_} notes={n_}")
        finally:
            shutil.rmtree(td2, ignore_errors=True)

        # arm H: N is not a literal this seat may move.
        if TO_DELETE_MAX_AGE_SESSIONS != 3:
            fails.append(f"[s294-D12 N] TO_DELETE_MAX_AGE_SESSIONS is "
                         f"{TO_DELETE_MAX_AGE_SESSIONS}, not 3 — N is Dave's figure ('N+3 is "
                         f"fine', #294) and re-dialling it is his word, not a seat's")
    finally:
        shutil.rmtree(td, ignore_errors=True)
    return fails


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    _wrap = "--wrap" in sys.argv
    if _wrap:
        SCRATCH_ROOTS += WRAP_ONLY_ROOTS
    sys.exit(report(clean="--clean" in sys.argv, wrap=_wrap))
