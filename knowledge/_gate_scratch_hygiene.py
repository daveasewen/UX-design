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

Exit codes: 0 always (advisory). `--selftest` exits 1 on a failed arm.
"""
import os, pwd, shutil, subprocess, sys

SCRATCH_ROOTS = ["/var/tmp", "/tmp"]
FILL_WARN_PCT = 80


def _me():
    return pwd.getpwuid(os.getuid()).pw_name


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


def report(clean=False):
    pct, free = vm_fill_pct()
    tag = "⚠" if pct >= FILL_WARN_PCT else "·"
    print(f"{tag} VM disk fill {pct}% · free {free // 1024}K")
    own = mine()
    if own:
        print(f"⚠ {len(own)} scratch entr{'y' if len(own) == 1 else 'ies'} owned by "
              f"{_me()} — REMOVABLE NOW ONLY (the owner dies with the session):")
        for p in own:
            print(f"    {p}" + ("  → removed" if clean and _rm(p) else ""))
    else:
        print(f"· no scratch owned by {_me()} under {', '.join(SCRATCH_ROOTS)} — clean wrap")
    ob = orphan_bytes()
    if ob:
        print(f"· {ob // (1024 * 1024)}M owned by dead sessions — UNREMOVABLE from inside "
              f"(named for drift visibility, not action)")
    return 0  # advisory


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
    print("\n".join(fails) if fails else "scratch-hygiene selftest: 3 arms, all GREEN")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(report(clean="--clean" in sys.argv))
