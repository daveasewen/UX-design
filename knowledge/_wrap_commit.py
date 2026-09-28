#!/usr/bin/env python3
"""_wrap_commit.py — the commit door: the paths file, the msgfile, and one `_git_commit.sh` run.

Built #306 lane W1 for `s306-D4` phase 1 (Dave, 2026-09-28 16:58 BST, "go on both"). It is the
permanent form of `notes/_lanes/306/T/commit_t.sh` (and U's and V's copies), of the `paths_*.py`
path-list builders and the `_msg-*.py` msgfile writers, and of the #303–#305 wrap seats'
`commit_w1.sh` / `commit_w5b.sh`. `_git_commit.sh` stays exactly as it is: this door only makes
sure what it is handed cannot strand a lock or trip a gate that the door could have seen first.

THE LESSONS IT ENCODES (`_HANDOFF-156` § THINGS A COLD SEAT SHOULD KNOW):
  · `_git_commit.sh` strands `.git/index.lock` on a named path that is UNCHANGED, then blames the
    next path (#304 C1). ⇒ every path is checked changed-or-untracked BEFORE the run; one that is
    not REFUSES the whole run (exit 3), naming it.
  · A stranded lock is MOVED to `notes/_lanes/_orphan-locks/` with a unique suffix, never `rm`'d,
    then `git reset -q`, then EVERY lock moved again: on this mount the reset itself strands
    `HEAD.lock` and `refs/heads/master.lock` (found at this tool's first real use, #306 W1). The door refuses to start
    while any `.git/*.lock` exists, and checks again after the run.
  · `SESSION_N` is required, and line 1 of the msgfile must carry NO T3 prefix (`after #N <date> — `
    or `#N <date> — `): `_git_commit.sh` prepends it and refuses a reused msgfile (#208). The
    prefix pattern here is PINNED to the one in `_git_commit.sh` by a selftest bite, not trusted.
  · Line 1 ≤ 170 chars, then a blank line (the #124 subject-fold class; the committer caps the
    subject at 200 including its ~25-char prefix). A msgfile is never overwritten (unique names).
  · `git status` is never run; every read is `git --no-optional-locks`.

Usage:
  python3 knowledge/_wrap_commit.py paths --out PATHS.txt [--dir D ...] [--from FILE] [path ...]
  python3 knowledge/_wrap_commit.py msg --out MSG.txt --line1 "306 W1: ..." (--body TEXT|--body-file F) [--trailer T ...]
  python3 knowledge/_wrap_commit.py commit --session 306 --msg MSG.txt --paths PATHS.txt --log LOG [--wrap] [--dry-run]
  python3 knowledge/_wrap_commit.py unlock --tag 306-W1 [--dry-run]
  python3 knowledge/_wrap_commit.py --selftest
"""
import argparse
import datetime
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
COMMITTER = os.path.join(HERE, "_git_commit.sh")
ORPHANS = "notes/_lanes/_orphan-locks"
T3_PREFIX_RE = re.compile(r"^(?:after )?#\d+ \d{4}-\d{2}-\d{2} — ")
LINE1_MAX = 170
SKIP_PARTS = ("backup", "__pycache__")
ENV = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}


class DoorError(Exception):
    """A named refusal. At the CLI it means: nothing was committed."""


def _git(repo, *args):
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=repo, capture_output=True, text=True, env=ENV)


def changed_set(repo):
    """Every path that differs from HEAD, plus every untracked, not-ignored path."""
    a = _git(repo, "diff", "--name-only", "HEAD")
    b = _git(repo, "ls-files", "--others", "--exclude-standard")
    if a.returncode or b.returncode:
        raise DoorError("git could not list changed paths: " + (a.stderr or b.stderr).strip()[:200])
    return set(filter(None, a.stdout.splitlines())) | set(filter(None, b.stdout.splitlines()))


def build_paths(repo, paths=(), dirs=()):
    """(keep, skipped). Directories expand to their changed/untracked files, minus backup/ and __pycache__/."""
    ch = changed_set(repo)
    keep, skip = [], []
    for d in dirs:
        d = d.rstrip("/") + "/"
        hits = sorted(p for p in ch if p.startswith(d) and not any(s in p.split("/") for s in SKIP_PARTS)
                      and not p.endswith(".pyc"))
        keep += hits
        if not hits:
            skip.append((d, "nothing changed under it"))
    for p in paths:
        p = p.strip()
        if not p:
            continue
        if p in ch:
            keep.append(p)
        elif not os.path.exists(os.path.join(repo, p)):
            skip.append((p, "absent"))
        elif _git(repo, "ls-files", "--error-unmatch", p).returncode == 0:
            skip.append((p, "unchanged vs HEAD"))
        else:
            skip.append((p, "ignored or not a file"))
    return list(dict.fromkeys(keep)), skip


def locks(repo):
    return sorted(glob.glob(os.path.join(repo, ".git", "*.lock")) + glob.glob(os.path.join(repo, ".git", "refs", "heads", "*.lock")))


def write_msg(out, line1, body, trailers=(), force=False):
    line1 = line1.strip()
    if not line1 or "\n" in line1:
        raise DoorError("line 1 must be one non-empty line")
    if T3_PREFIX_RE.match(line1):
        raise DoorError(f"line 1 already carries a T3 prefix — `_git_commit.sh` adds it (#208): {line1[:60]!r}")
    if len(line1) > LINE1_MAX:
        raise DoorError(f"line 1 is {len(line1)} chars (cap {LINE1_MAX}: the subject is capped at 200 with its prefix)")
    if os.path.exists(out) and not force:
        raise DoorError(f"{out} exists — a msgfile is used once (#208 reuse gate); name a new one")
    text = line1 + "\n\n" + (body or "").strip() + "\n"
    if trailers:
        text += "\n" + "\n".join(t.strip() for t in trailers) + "\n"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    return {"line1_chars": len(line1), "bytes": len(text.encode()), "trailers": len(trailers)}


def commit(repo, session, msg, paths_file, log, wrap=False, dry_run=False, committer=COMMITTER):
    held = locks(repo)
    if held:
        raise DoorError("a lock is held — " + ", ".join(os.path.relpath(l, repo) for l in held) +
                        " — run `_wrap_commit.py unlock --tag <tag>` (moves it, never rm)")
    if not str(session).isdigit():
        raise DoorError("--session N is required (SESSION_N, s130-D3)")
    with open(msg, encoding="utf-8") as f:
        l1 = f.readline().rstrip("\n")
    if T3_PREFIX_RE.match(l1):
        raise DoorError("the msgfile's line 1 carries a T3 prefix — it has been through a commit run (#208)")
    with open(paths_file, encoding="utf-8") as f:
        P = [p.strip() for p in f if p.strip()]
    if not P:
        raise DoorError("the paths file is empty")
    ch = changed_set(repo)
    bad = [p for p in P if p not in ch]
    if bad:
        raise DoorError("REFUSED before the committer ran — named path(s) neither changed nor untracked "
                        "(the committer strands the lock on these): " + ", ".join(bad[:8]))
    argv = ["bash", committer, "--reconciled"] + (["--wrap"] if wrap else []) + [f"--quiet={log}", msg] + P
    print(f"paths checked: {len(P)} of {len(P)} changed-or-untracked")
    print("SESSION_N=%s %s" % (session, " ".join(argv[:5 + wrap]) + f" <{len(P)} paths>"))
    if dry_run:
        print("DRY-RUN — the committer was not run"); return 0
    r = subprocess.run(argv, cwd=repo, env={**ENV, "SESSION_N": str(session)})
    held = locks(repo)
    head = _git(repo, "log", "-1", "--format=%h %s").stdout.strip()
    print(f"EXIT={r.returncode} · HEAD {head[:160]}")
    if held:
        print("⛔ LOCK STRANDED after the run: " + ", ".join(os.path.relpath(l, repo) for l in held) +
              " — run `_wrap_commit.py unlock --tag <tag>`")
        return r.returncode or 4
    print("locks: none held")
    return r.returncode


def unlock(repo, tag, dry_run=False, orphans=ORPHANS, reset=True):
    """Move every stranded lock (never rm), `git reset -q`, then move again whatever came back.

    ⚠ FOUND AT THIS TOOL'S FIRST REAL USE (#306 W1, 16:41 UTC): on this mount `git reset -q` itself
    strands `.git/HEAD.lock` and `.git/refs/heads/master.lock` ("unable to unlink … Operation not
    permitted" — the mount forbids delete). So the second pass moves EVERY `.git/*.lock` and
    `.git/refs/heads/*.lock`, not only `index.lock`. HEAD and the index were intact afterwards."""
    dst_dir = os.path.join(repo, orphans)
    moved = []
    for attempt in (1, 2):
        held = locks(repo)
        if not held:
            break
        for lk in held:
            rel = os.path.relpath(lk, os.path.join(repo, ".git")).replace("/", "-")
            dst = os.path.join(dst_dir, f"{rel}-{tag}-{datetime.datetime.now():%H%M%S}-{attempt}")
            if dry_run:
                print("DRY-RUN would move", os.path.relpath(lk, repo), "→", os.path.relpath(dst, repo)); continue
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(lk, dst); moved.append(os.path.relpath(dst, repo))
        if dry_run:
            return moved
        if attempt == 1 and reset:
            subprocess.run(["git", "reset", "-q"], cwd=repo, env=ENV, capture_output=True)
    left = locks(repo)
    print("moved:", moved or "nothing — no lock held", "· locks left:", [os.path.relpath(l, repo) for l in left] or "none")
    return moved


# ------------------------------------------------------------------------------------ selftest
def selftest():
    ok = True

    def bite(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok = ok and bool(cond)

    src = open(COMMITTER, encoding="utf-8").read()
    m = re.search(r'pat = re\.compile\(r"(.+?)"\)', src)
    bite("the T3 prefix pattern is PINNED to _git_commit.sh's own", m and m.group(1) == T3_PREFIX_RE.pattern)
    with tempfile.TemporaryDirectory() as td:
        g = lambda *a: subprocess.run(["git", *a], cwd=td, capture_output=True, env={**ENV, "GIT_AUTHOR_NAME": "t",
                                      "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
        g("init", "-q")
        w = lambda p, s: (os.makedirs(os.path.dirname(os.path.join(td, p)) or td, exist_ok=True),
                          open(os.path.join(td, p), "w").write(s))
        w("same.txt", "a"); w("chg.txt", "a"); w(".gitignore", "ign.txt\n"); w("lane/x.md", "x")
        g("add", "-A"); g("commit", "-qm", "base")
        w("chg.txt", "b"); w("new.txt", "n"); w("ign.txt", "i"); w("lane/y.md", "y"); w("lane/backup/z.md", "z")
        keep, skip = build_paths(td, ["same.txt", "chg.txt", "new.txt", "ign.txt", "gone.txt"], ["lane"])
        bite("paths keeps changed + untracked, expands a dir minus backup/",
             keep == ["lane/y.md", "chg.txt", "new.txt"])
        sk = dict(skip)
        bite("paths skips unchanged / ignored / absent, each named",
             sk.get("same.txt") == "unchanged vs HEAD" and sk.get("ign.txt", "").startswith("ignored")
             and sk.get("gone.txt") == "absent")
        mf = os.path.join(td, "m1.txt")
        rec = write_msg(mf, "306 X: a headline", "body", ["Co-Authored-By: x"])
        txt = open(mf).read()
        bite("msg: line 1, a blank line, the body, the trailers", txt.split("\n")[:3] == ["306 X: a headline", "", "body"]
             and txt.rstrip().endswith("Co-Authored-By: x"))
        for name, args in [("msg refuses a T3 prefix on line 1", (os.path.join(td, "m2"), "after #306 2026-09-28 — x", "b")),
                           ("msg refuses the wrap-shaped prefix", (os.path.join(td, "m3"), "#306 2026-09-28 — x", "b")),
                           ("msg refuses line 1 over 170 chars", (os.path.join(td, "m4"), "x" * 171, "b")),
                           ("msg refuses to overwrite a msgfile", (mf, "306 X: y", "b"))]:
            try:
                write_msg(*args); bite(name, False)
            except DoorError:
                bite(name, True)
        fake = os.path.join(td, "fake_commit.sh")
        w("fake_commit.sh", 'echo "$SESSION_N $*" > "$(dirname "$0")/called.txt"\n')
        pf = os.path.join(td, "p.txt")
        open(pf, "w").write("chg.txt\nsame.txt\n")
        try:
            commit(td, 306, mf, pf, os.path.join(td, "l.log"), committer=fake); bite("commit refuses an unchanged path BEFORE the committer", False)
        except DoorError as e:
            bite("commit refuses an unchanged path BEFORE the committer", "same.txt" in str(e) and not os.path.exists(os.path.join(td, "called.txt")))
        open(pf, "w").write("chg.txt\nnew.txt\n")
        rc = commit(td, 306, mf, pf, os.path.join(td, "l.log"), committer=fake)
        called = open(os.path.join(td, "called.txt")).read()
        bite("commit runs the committer with SESSION_N, --reconciled, --quiet=LOG, the msg and the paths",
             rc == 0 and called.startswith("306 --reconciled --quiet=") and called.rstrip().endswith("chg.txt new.txt"))
        os.remove(os.path.join(td, "called.txt"))
        commit(td, 306, mf, pf, os.path.join(td, "l.log"), dry_run=True, committer=fake)
        bite("commit --dry-run does not run the committer", not os.path.exists(os.path.join(td, "called.txt")))
        try:
            commit(td, "", mf, pf, os.path.join(td, "l.log"), committer=fake); bite("commit refuses without SESSION_N", False)
        except DoorError:
            bite("commit refuses without SESSION_N", True)
        open(os.path.join(td, ".git", "index.lock"), "w").write("")
        try:
            commit(td, 306, mf, pf, os.path.join(td, "l.log"), committer=fake); bite("commit refuses while a lock is held", False)
        except DoorError as e:
            bite("commit refuses while a lock is held", "index.lock" in str(e))
        open(os.path.join(td, ".git", "HEAD.lock"), "w").write("")
        os.makedirs(os.path.join(td, ".git", "refs", "heads"), exist_ok=True)
        open(os.path.join(td, ".git", "refs", "heads", "master.lock"), "w").write("")
        mv = unlock(td, "selftest", orphans="orphans")
        bite("unlock MOVES every lock — index, HEAD, refs/heads/master (never rm) — with unique names",
             len(mv) == 3 and all(os.path.exists(os.path.join(td, m)) for m in mv) and locks(td) == []
             and len(set(mv)) == 3)
        bite("unlock with no lock moves nothing", unlock(td, "selftest", orphans="orphans") == [])
    print("wrap-commit selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="verb")
    p = sub.add_parser("paths"); p.add_argument("--out", required=True); p.add_argument("--dir", action="append", default=[])
    p.add_argument("--from", dest="from_file"); p.add_argument("path", nargs="*")
    m = sub.add_parser("msg"); m.add_argument("--out", required=True); m.add_argument("--line1", required=True)
    m.add_argument("--body"); m.add_argument("--body-file"); m.add_argument("--trailer", action="append", default=[])
    c = sub.add_parser("commit"); c.add_argument("--session", required=True); c.add_argument("--msg", required=True)
    c.add_argument("--paths", required=True); c.add_argument("--log", required=True)
    c.add_argument("--wrap", action="store_true"); c.add_argument("--dry-run", action="store_true")
    u = sub.add_parser("unlock"); u.add_argument("--tag", required=True); u.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.verb == "paths":
            extra = [l.strip() for l in open(a.from_file, encoding="utf-8")] if a.from_file else []
            keep, skip = build_paths(REPO, a.path + extra, a.dir)
            with open(a.out, "w", encoding="utf-8") as f:
                f.write("".join(k + "\n" for k in keep))
            print(f"{len(keep)} path(s) named → {a.out}")
            for s in skip:
                print("  skip", *s)
            return 0
        if a.verb == "msg":
            body = a.body if a.body is not None else (open(a.body_file, encoding="utf-8").read() if a.body_file else "")
            print("msgfile", a.out, write_msg(a.out, a.line1, body, a.trailer))
            return 0
        if a.verb == "commit":
            return commit(REPO, a.session, a.msg, a.paths, a.log, a.wrap, a.dry_run)
        if a.verb == "unlock":
            unlock(REPO, a.tag, a.dry_run); return 0
    except DoorError as e:
        print("⛔ REFUSED:", e); return 3
    ap.print_help(); return 2


if __name__ == "__main__":
    sys.exit(main())
