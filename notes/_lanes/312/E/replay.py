#!/usr/bin/env python3
"""replay.py — the E3 replay in one command: generate a wrap's views from its STORY + extended FACTS, at both stages,
and grade each against the hand-written file (DESIGN.md § 8), filing the diffs under notes/_lanes/312/E/replay/<n>/.

Usage (from the repo root):
  python3 notes/_lanes/312/E/replay.py --session 310 --story knowledge/_tests/wrap_views/310/STORY.md \
      --facts notes/_lanes/312/E/facts/FACTS-310.json [--out notes/_lanes/312/E/replay/310]

The facts file must carry the phase-3 keys AND the `post` block (the three under notes/_lanes/312/E/facts/ do).
The hand files are found from the facts' handoff number and the session's W dir; a later wrap's `STRUCK AT THE #N+1
WRAP` addendum on the hand handoff is cut before grading (it is by addition, not this wrap's view). The memory hook
is graded against the hook + its four payload files concatenated, because phase 3 makes ONE file of the five.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "knowledge"))
import _wrap_views as wv  # noqa: E402

LIMITS = {"banner": 1200, "delta": 1513, "handoff": 8106}


def hand_files(n, facts, repo):
    w = os.path.join(repo, "notes", "_lanes", str(n), "W")
    hno = facts["handoff"]["no"]
    handoff = glob.glob(os.path.join(repo, f"_HANDOFF-{hno}-*.md"))
    dossier = glob.glob(os.path.join(repo, "_DECISION-HISTORY", f"*-{n}-*.md"))
    report = glob.glob(os.path.join(repo, "notes", "_subreports", f"*-{n}-W-wrap.md"))
    out = {"banner.md": os.path.join(w, "banner.md"), "delta.md": os.path.join(w, "delta.md"), "stratum.md": os.path.join(w, "stratum.md"),
           "stamp.md": os.path.join(w, "stamp.md"), "datesplit.md": os.path.join(w, "datesplit.md"), "5b.md": os.path.join(w, "5b.md"),
           "handoff.md": handoff[0] if handoff else None, "dossier.md": dossier[0] if dossier else None,
           "report.md": report[0] if report else None, "SUMMARY.md": os.path.join(w, "SUMMARY.md"),
           "new.txt": os.path.join(w, "new.txt"), "rows.json": os.path.join(w, "rows.json"), "msg.txt": os.path.join(w, "_msg-W1.txt"),
           "msg-5b.txt": os.path.join(w, "_msg-W5b.txt")}
    strikes = sorted(glob.glob(os.path.join(w, "strike-*.txt")))
    for i, p in enumerate(strikes, 1):
        out[f"strike-{i}.txt"] = p
    hook = os.path.join(repo, "notes", "_lanes", str(n), "WRAP-MEMORY-HOOK.md")
    payloads = sorted(glob.glob(os.path.join(w, "_work", "memory_*")))
    out["WRAP-MEMORY-HOOK.md"] = (hook, payloads)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session", type=int, required=True); ap.add_argument("--story", required=True); ap.add_argument("--facts", required=True)
    ap.add_argument("--out"); ap.add_argument("--repo", default=REPO)
    a = ap.parse_args()
    out = a.out or os.path.join(a.repo, "notes", "_lanes", "312", "E", "replay", str(a.session))
    os.makedirs(os.path.join(out, "views"), exist_ok=True)
    story, facts = wv.load(a.story, a.facts)
    views, d, s = wv.generate(story, facts, "post" if "post" in facts else "wrap")
    fails, warns = wv.check_limits(views, story, facts, d)
    for k, v in views.items():
        with open(os.path.join(out, "views", k), "w", encoding="utf-8") as fh:
            fh.write(v)
    hands = hand_files(a.session, facts, a.repo)
    story_text = open(a.story, encoding="utf-8").read()
    rows = []
    cut = f"## ⬛ STRUCK AT THE #{a.session + 1} WRAP"
    for k, text in views.items():
        h = hands.get(k)
        if isinstance(h, tuple):
            hook, payloads = h
            if not os.path.exists(hook):
                rows.append((k, "NO HAND FILE", None)); continue
            hand = "".join(open(p, encoding="utf-8").read() + "\n" for p in [hook] + payloads)
        elif not h or not os.path.exists(h):
            rows.append((k, "NO HAND FILE", None)); continue
        else:
            hand = open(h, encoding="utf-8").read()
        view = k.split(".")[0].replace("WRAP-MEMORY-HOOK", "memory").replace("new", "carries")
        rep = wv.diff_views(text, hand, view, facts, story_text, LIMITS.get(view), cut)
        with open(os.path.join(out, f"diff-{k}.md"), "w", encoding="utf-8") as fh:
            fh.write(wv.render_diff(rep))
        rows.append((k, rep["verdict"], rep))
    summary = [f"# replay #{a.session} — generated from `{os.path.relpath(a.story, a.repo)}` + `{os.path.relpath(a.facts, a.repo)}`", "",
               f"limits: {len(fails)} fail · {len(warns)} warn" + ("".join(f"\n- ✗ {x}" for x in fails)) + ("".join(f"\n- ⚠ {x}" for x in warns)), "",
               "| view | verdict | size gen / hand | figures missing | unsourced | words missing | headings |", "|---|---|---|---|---|---|---|"]
    green = 0
    for k, verdict, rep in rows:
        if rep is None:
            summary.append(f"| {k} | {verdict} | | | | | |"); continue
        miss = sum(len(v["missing"]) for v in rep["figures"].values())
        uns = sum(len(v["extra_unsourced"]) for v in rep["figures"].values())
        summary.append(f"| {k} | {verdict} | {rep['size']['generated']:,} / {rep['size']['hand']:,} ({rep['size']['ratio']}) | {miss} | {uns} | "
                       f"{len(rep['words']['missing'])} | {'same' if rep['headings']['same'] else 'differ'} |")
        green += verdict == "GREEN"
    graded = [r for r in rows if r[2] is not None]
    summary += ["", f"VERDICT: {green} of {len(graded)} graded views GREEN; the residue is explained in the lane's report, view by view.", ""]
    with open(os.path.join(out, "REPLAY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(summary))
    print("\n".join(summary))
    print("→", os.path.relpath(out, a.repo))


if __name__ == "__main__":
    main()
