#!/usr/bin/env python3
"""replay.py — the E3 replay in one command: generate a wrap's views from its STORY + extended FACTS, at both stages,
and grade each against the hand-written file (DESIGN.md § 8), filing the diffs under notes/_lanes/312/E/replay/<n>/.

Usage (from the repo root):
  python3 notes/_lanes/312/E/replay.py --session 310 --story knowledge/_tests/wrap_views/310/STORY.md \
      --facts notes/_lanes/312/E/facts/FACTS-310.json [--out notes/_lanes/312/E/replay/310]

The facts file must carry the phase-3 keys AND the `post` block (the three under notes/_lanes/312/E/facts/ do).
The hand files are found from the facts' handoff number and the session's W dir; a later wrap's `STRUCK AT THE #N+1
WRAP` addendum on the hand handoff is cut before grading (it is by addition, not this wrap's view).

★ E-replay (2026-10-01), the grading as run, each choice declared here and in REPLAY.md:
  memory    graded at the WRAP stage against what the placer places — `memory_indexline_<n>.txt` + `memory_file_<n>.md`
            (= front + body), NOT the hook's placer instructions (they name the hand process's five payload files, which
            phase 3 replaces with one) and NOT an area-file payload (no story section carries one; Found-not-fixed).
            Headings for memory are graded by LEVEL SEQUENCE inside the hook's `## BODY` (the #309 hand heading read
            `### OPEN, DAVE'S —`, the template's constant is #310's `### OPEN —`).
  report    headings are graded against the `s218-D7` form the generated report must carry (`## Found, not fixed`,
            `## Ruling-shaped questions`, `REPLAY-THESE:`), not the hand file's (`## RULING-SHAPED QUESTIONS`): the
            generated report IS the filed report (`s306-D5`).
  DECLARED  one figure class is declared per session and reported, not hidden: the POST-ROLL carries count (429/436/442),
            which no tool can measure before the roll — the generated views name the probe instead (E-build § 2). A
            declared figure still prints in the per-view diff under `declared`.
  prior-strikes  graded against the addendum at the foot of the previous handoff, on figures, words and headings; its
            SIZE is not graded — the view is the strike receipt verbatim (`strike-<k>.txt` is graded byte for byte), where
            the hand seats wrote a second, shorter line by hand.
  carries-delta  graded by the `s183-D1` RECONSTRUCTION on the GENERATED block: `_CARRIES.md` from the FULL #n line down,
            the block appended, #n+1 rendered, compared byte for byte with the hand-rolled FULL #n+1 line.
Verdict per view: GREEN · GREEN (declared: …) · RED (named).
"""
# DECLARED figures, per session: {figure: why no generated view can carry it}. Each is printed in the per-view diff and
# in REPLAY.md; a view whose only residue is declared reads GREEN (declared: …), never plain GREEN.
POST_ROLL = "the post-roll carries count — typed by the hand seat AFTER the roll; no tool measures it before the roll, the generated views name the probe (E-build § 2)"
AFTER_5B = "_CHAIN.md after the 5b regen — typed by the hand seat after the regen that FOLLOWS the views; post.chain_tk_after_5b is null by the #241 rule"
COMMIT_LOG = "a figure typed from the committer's log (run seconds, path counts, minutes to the summary, the previous wrap's chain) — FACTS.json carries no commit timing; a --gate-log/--commit-log reader would close it (E-build Found-not-fixed 4)"
PROSE_REF = "a session number the hand seat cited in prose ('#309's date-split line', 'the second since #309'), not a measured figure"
HAND_CHOICE = "the hand seat's own choice of the day's last commit on the date-split line (lane P's, 'and the night's first lanes'); the generated line takes the last commit dated that day (`d1901fa2`)"
AREA_FILE = "a memory AREA payload (areas/<name>.md) the hand seat wrote beside the hook; no story section carries one — Found-not-fixed 1 of this lane's report"
LAUNCH_FILE = "the hand process's SECOND facts file (`_wrap_facts.py` run again to the launch); phase 3 carries the launch cut inside FACTS.json as `fill.launch` (★ E-replay), so there is no second file to name"
PRIOR_TEXT = "an id the hand seat put in its SECOND text of the strike (the prior handoff's addendum); the generated addendum is the strike receipt verbatim, and that receipt is proven byte for byte by the carries reconstruction"
DECLARED = {309: {"429": POST_ROLL, "8,105": AFTER_5B, "114": COMMIT_LOG},
            310: {"436": POST_ROLL, "7,988": AFTER_5B, "7,824": COMMIT_LOG, "7,947": COMMIT_LOG, "123": COMMIT_LOG,
                  "8,105": AFTER_5B, "s310-D7": PRIOR_TEXT, "s310-D8": PRIOR_TEXT, "facts-launch.json": LAUNCH_FILE},
            311: {"442": POST_ROLL, "8,499": AFTER_5B, "8,305": COMMIT_LOG, "7,824": COMMIT_LOG, "100": COMMIT_LOG, "141": COMMIT_LOG,
                  "_memento-index.json": COMMIT_LOG, "canon.css": COMMIT_LOG, "facts-launch.json": LAUNCH_FILE, "309": PROSE_REF, "148fa6fc": HAND_CHOICE,
                  "apollo-other-libraries.md": AREA_FILE}}
_UNUSED = {
            311: {"442": POST_ROLL, "8,499": AFTER_5B}}   # (superseded above)
REPORT_HEADINGS = ["## VERDICT", "## 1. The fill", "## 2. Each step, and what the tool did", "## 3. What this wrap found",
                   "## 4. What is carried, not committed", "## Found, not fixed", "## Ruling-shaped questions", "## UNPROVEN"]
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
import _wrap_carries as wc  # noqa: E402

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
    payloads = [os.path.join(w, "_work", f"memory_indexline_{n}.txt"), os.path.join(w, "_work", f"memory_file_{n}.md")]
    out["WRAP-MEMORY-HOOK.md"] = (hook, payloads)
    out["prior-strikes.md"] = ("PRIOR", None)
    return out


def carries_proof(repo, n, block):
    """The `s183-D1` reconstruction proof on the GENERATED delta block: take `_CARRIES.md` from the FULL `#n` line down
    (the file as it stood at the #n wrap), append the generated `#n+1 (delta from #n)` block, render `#n+1`, and compare
    byte for byte with the hand-written FULL `#n+1` line the wrap seat actually rolled. Returns (verdict, detail)."""
    text = open(os.path.join(repo, "_CARRIES.md"), encoding="utf-8").read()
    lines = text.split("\n")
    secs = wc.sections(lines)
    try:
        hand = wc.list_line(lines, n + 1)[1]
    except wc.CarryError as e:
        return "NO HAND LINE", str(e)
    base_idx = next(i for s_, i in secs if s_ == n)
    base = "\n".join(lines[base_idx:])
    try:
        new, receipt = wc.delta_append(base, n, n + 1, None, None, block=block)
        rendered, _ = wc.render_text(new, n + 1)
    except wc.CarryError as e:
        return "RED", f"refused: {e}"
    if rendered == hand:
        return "GREEN", f"rendered #{n + 1} == the hand-written FULL line, {len(hand):,} chars; block {receipt['block_bytes']:,} B; {receipt['rendered_items']} items ({receipt['rendered_items_with_new']} with NEW)"
    i = next((k for k, (a, b) in enumerate(zip(rendered, hand)) if a != b), min(len(rendered), len(hand)))
    return "RED", f"differs at char {i:,} of {len(hand):,}: rendered …{rendered[max(0, i-60):i+60]!r}… hand …{hand[max(0, i-60):i+60]!r}…"


def prior_strikes_hand(repo, facts, n):
    """The hand-written STRUCK addendum at the foot of the previous handoff (appended by addition at the #n wrap)."""
    p = os.path.join(repo, facts["handoff"]["prev_name"])
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    mark = f"## ⬛ STRUCK AT THE #{n} WRAP"
    if mark not in t:
        return None
    t = t[t.index(mark):]
    nxt = f"## ⬛ STRUCK AT THE #{n + 1} WRAP"
    return ("\n---\n\n" + t[:t.index(nxt)] if nxt in t else "\n---\n\n" + t).rstrip("\n") + "\n"


def _body(text):
    return text[text.index("### What landed"):] if "### What landed" in text else text


def _levels(text):
    return [m.group(1) for l in text.split("\n") for m in [wv.HEAD_RE.match(l)] if m]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session", type=int, required=True); ap.add_argument("--story", required=True); ap.add_argument("--facts", required=True)
    ap.add_argument("--out"); ap.add_argument("--repo", default=REPO)
    a = ap.parse_args()
    out = a.out or os.path.join(a.repo, "notes", "_lanes", "312", "E", "replay", str(a.session))
    os.makedirs(os.path.join(out, "views"), exist_ok=True)
    story, facts = wv.load(a.story, a.facts)
    views, d, s = wv.generate(story, facts, "post" if "post" in facts else "wrap")
    wrap_views, _, _ = wv.generate(story, facts, "wrap")
    fails, warns = wv.check_limits(views, story, facts, d)
    declared = DECLARED.get(a.session, {})
    for k, v in views.items():
        with open(os.path.join(out, "views", k), "w", encoding="utf-8") as fh:
            fh.write(v)
    hands = hand_files(a.session, facts, a.repo)
    story_text = open(a.story, encoding="utf-8").read()
    rows = []
    cut = f"## ⬛ STRUCK AT THE #{a.session + 1} WRAP"
    for k, text in views.items():
        h = hands.get(k)
        if k == "carries-delta.md":
            verdict, detail = carries_proof(a.repo, a.session, text)
            with open(os.path.join(out, f"diff-{k}.md"), "w", encoding="utf-8") as fh:
                fh.write(f"## carries-delta — {verdict}\n\n- RECONSTRUCTION (s183-D1), on the GENERATED block: {detail}\n")
            rows.append((k, verdict + (" (reconstruction)" if verdict == "GREEN" else ""), {"figures": {}, "words": {"missing": []}, "headings": {"same": True, "generated": [], "hand": []},
                                                                        "size": {"generated": wv._tk(text), "hand": 0, "ratio": None, "over_limit": False, "over_ratio": False}, "verdict": verdict}))
            continue
        if isinstance(h, tuple) and h[0] == "PRIOR":
            hand = prior_strikes_hand(a.repo, facts, a.session)
            if hand is None:
                rows.append((k, "NO HAND FILE", None)); continue
        elif isinstance(h, tuple):
            hook, payloads = h
            if not os.path.exists(hook) or not all(os.path.exists(p) for p in payloads):
                rows.append((k, "NO HAND FILE", None)); continue
            hand = "".join(open(p, encoding="utf-8").read() + "\n" for p in payloads)
            text = wrap_views[k]          # the placer's file is written at the wrap stage; the post line is by addition
            text = text[text.index("## INDEX LINE"):]      # what the placer places: the index line, the front block, the body
            text = "\n".join(l for l in text.split("\n") if l not in ("## INDEX LINE", "## FRONT BLOCK", "## BODY"))
        elif not h or not os.path.exists(h):
            rows.append((k, "NO HAND FILE", None)); continue
        else:
            hand = open(h, encoding="utf-8").read()
        view = k.split(".")[0].replace("WRAP-MEMORY-HOOK", "memory").replace("new", "carries")
        rep = wv.diff_views(text, hand, view, facts, story_text, LIMITS.get(view), cut)
        # the declared grading (docstring): re-derive the verdict from the parts, naming every declared figure
        notes = []
        for fk, v in rep["figures"].items():
            dec = sorted(x for x in v["missing"] if x in declared)
            if dec:
                v["declared"] = dec
                v["missing"] = [x for x in v["missing"] if x not in declared]
                notes.append(f"declared {fk}: " + ", ".join(dec))
        if view == "memory":
            gl, hl = _levels(_body(text)), _levels(hand)
            rep["headings"] = {"generated": gl, "hand": hl, "same": gl == hl, "graded": "levels inside ## BODY"}
        if view == "report":
            gh = [l for l in rep["headings"]["generated"] if not l.startswith("## POST-COMMIT")]
            rep["headings"] = {"generated": gh, "hand": REPORT_HEADINGS, "same": gh == REPORT_HEADINGS, "graded": "the s218-D7 form, not the hand file"}
        if view == "prior-strikes":
            rep["size"]["over_ratio"] = False; rep["size"]["graded"] = "not graded (the receipt verbatim)"
        red = (any(v["missing"] or v["extra_unsourced"] for v in rep["figures"].values()) or rep["words"]["missing"]
               or not rep["headings"]["same"] or rep["size"]["over_limit"] or rep["size"]["over_ratio"])
        rep["verdict"] = "RED" if red else ("GREEN (" + "; ".join(notes) + ")" if notes else "GREEN")
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
        green += verdict.startswith("GREEN")
    graded = [r for r in rows if r[2] is not None]
    used = sorted({x for _, _, r in rows if r for v in r["figures"].values() for x in v.get("declared", [])})
    summary += ["", f"VERDICT: {green} of {len(graded)} graded views GREEN" + (" — the session replays GREEN" if green == len(graded) and not fails else " — RED") + "; the residue is explained in the lane's report, view by view.",
                ""] + [f"- declared `{x}`: {declared[x]}" for x in used] + [
                "", "Grading as run: " + "; ".join(x.strip() for x in __doc__.split("★ E-replay")[1].split("Verdict per view")[0].split("\n") if x.strip()), ""]
    with open(os.path.join(out, "REPLAY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(summary))
    print("\n".join(summary))
    print("→", os.path.relpath(out, a.repo))


if __name__ == "__main__":
    main()
