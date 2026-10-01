#!/usr/bin/env python3
"""gen_runbook_index.py — the runbook of runbooks. GENERATED, so it cannot drift.

Dave 2026-07-18: "maybe we have a runbook of runbooks ;) my brain is basically a
recursive magpie always building a nest."

WHY GENERATED AND NOT WRITTEN. A hand-maintained index of runbooks is precisely the
artefact that rots silently — someone adds a runbook and forgets the index, or rewrites
the index from scratch and drops an entry. That is the same failure that nearly killed
§A's standing instruction on 2026-07-18. This scans knowledge/_RUNBOOK-*.md and rebuilds
the list every build, so "what runbooks exist" is derived from the filesystem rather than
from anyone's memory of it.

It reads each runbook's H1 and its first italic purpose line / first paragraph, so the
description is owned by the runbook itself — one source of truth per runbook.

Usage:  python3 knowledge/gen_runbook_index.py    # writes knowledge/_RUNBOOKS.md
Wired into _build_all.py. Never hand-edit _RUNBOOKS.md.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, glob, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "_RUNBOOKS.md")
# s313-D47 (Dave 2026-10-01 17:49 BST, pictures page call 28, by click: "Show the date of the newest
# runbook change"). The stamp used to be the BUILD date, so every build rewrote this file when nothing
# in it had changed. It is now the date of the newest change to any runbook, read from git:
#   * a runbook edited and not yet committed (or new and untracked)  -> today: that IS the newest change;
#   * otherwise the committer date of the last commit touching knowledge/_RUNBOOK-*.md;
#   * in a SHALLOW clone (CI, a cloud lane) that last commit can be the clone's boundary, whose date is
#     not the change's date — the true date is unknown there, so the stamp already in _RUNBOOKS.md
#     STANDS (never a guess); with no stamp on disk the boundary date is printed, and said to be one.
# ⛔ Read-only git only (`git log`, `git diff --quiet`, `git ls-files`): never `git status` (it locks).
STAMP_RE = re.compile(r"newest runbook change (\d{4}-\d{2}-\d{2})")
RUNBOOK_GLOB = "knowledge/_RUNBOOK-*.md"


def _git(*args):
    return subprocess.run(("git", "-C", ROOT) + args, capture_output=True, text=True, timeout=30)


def _shallow_boundaries():
    try:
        gitdir = _git("rev-parse", "--git-common-dir").stdout.strip()
        path = gitdir if os.path.isabs(gitdir) else os.path.join(ROOT, gitdir)
        with open(os.path.join(path, "shallow"), encoding="utf-8") as fh:
            return {ln.strip() for ln in fh if ln.strip()}
    except (OSError, subprocess.SubprocessError):
        return set()


def newest_runbook_change(today=None, on_disk=None):
    """-> (YYYY-MM-DD, how) — the date of the newest runbook change, and where it was read."""
    today = today or datetime.date.today().isoformat()
    try:
        dirty = _git("diff", "--quiet", "HEAD", "--", RUNBOOK_GLOB).returncode == 1
        untracked = bool(_git("ls-files", "-o", "--exclude-standard", "--", RUNBOOK_GLOB).stdout.strip())
        if dirty or untracked:
            return today, "uncommitted runbook change"
        r = _git("log", "-1", "--format=%H %cs", "--", RUNBOOK_GLOB)
    except (OSError, subprocess.SubprocessError):
        r = None
    if r is None or r.returncode != 0 or not r.stdout.strip():
        if on_disk:
            return on_disk, "git unreadable — the stamp on disk stands"
        return today, "git unreadable and no stamp on disk — today"
    sha, date = r.stdout.split()
    if sha in _shallow_boundaries():
        if on_disk:
            return on_disk, "shallow clone — the stamp on disk stands"
        return date, "shallow clone boundary %s — the true date is older" % sha[:8]
    return date, "last commit touching a runbook, %s" % sha[:8]


def summarise(path):
    """Title from the H1; purpose from the first italic line or first real paragraph."""
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"^#\s+(.+)$", txt, re.M)
    title = m.group(1).strip() if m else os.path.basename(path)
    body = txt[m.end():] if m else txt
    purpose = ""
    it = re.search(r"^\s*\*([^*].+?)\*\s*$", body, re.M | re.S)
    if it:
        purpose = it.group(1)
    else:
        for para in re.split(r"\n\s*\n", body):
            p = para.strip()
            if p and not p.startswith(("#", "```", ">", "|", "-", "*")):
                purpose = p
                break
    purpose = re.sub(r"\s+", " ", purpose).strip()
    if len(purpose) > 240:
        purpose = purpose[:237].rsplit(" ", 1)[0] + "…"
    return title, purpose


def build():
    paths = sorted(glob.glob(os.path.join(HERE, "_RUNBOOK-*.md")))
    try:
        m = STAMP_RE.search(open(OUT, encoding="utf-8").read())
    except OSError:
        m = None
    stamp, how = newest_runbook_change(on_disk=m.group(1) if m else None)
    lines = [
        "# Runbooks — the index",
        "",
        "*GENERATED by `knowledge/gen_runbook_index.py` — do not hand-edit; add a runbook and it appears.*",
        "",
        "Runbooks are **tattoos, not Polaroids** (see the Memento framing in `GOOD-MORNING.md` §A): the method",
        "written down so a cold agent can operate the engine without a human remembering how. A rule that lives",
        "only in the artefact it governs dies the first time that artefact is rewritten — so it lives here too.",
        "",
        "**This index is generated from the filesystem**, because a hand-maintained list of runbooks is exactly",
        "the thing that rots when someone adds the tenth one and forgets the list.",
        "",
        f"**{len(paths)} runbooks**, newest runbook change {stamp}.",
        "",
    ]
    for p in paths:
        name = os.path.basename(p)
        title, purpose = summarise(p)
        lines.append(f"### `{name}`")
        lines.append(f"**{title}**")
        if purpose:
            lines.append("")
            lines.append(purpose)
        lines.append("")

    lines += [
        "---",
        "",
        "## Read these before acting",
        "",
        "- **Any git operation** → `_RUNBOOK-git-commit.md`. The sandbox delete-guard means git can create",
        "  `.git/*.lock` but never unlink it. Sequence is **clear → stage → clear → commit → clear**, using",
        "  `mv` and never `rm`. Getting this wrong wastes a turn every time.",
        "- **End of session** → `_RUNBOOK-capture-ritual.md`. Run it unasked.",
        "- **Building a component** → `_RUNBOOK-gated-component.md`, after surveying `snippets/` +",
        "  `components/*.meta.json` + the tranches. Skipping the survey duplicated Tab-bar and Stepper in T8.",
        "",
        "*Entry points: `GOOD-MORNING.md` §A (orientation) · `_LIVE-STATE.md` (live/dead/open) ·",
        "`AGENTS.md` (repo agent contract) · `guidelines/_rules-index.json` (the 465-rule spine).*",
        "",
    ]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"runbook index: {len(paths)} runbooks, newest runbook change {stamp} ({how}) "
          f"-> {os.path.relpath(OUT, HERE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
