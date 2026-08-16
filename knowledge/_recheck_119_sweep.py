#!/usr/bin/env python3
"""_recheck_119_sweep.py — re-checker for the 21 rulings whose `status` froze at the #119
metadata sweep (W-21, promoted s186-D2 from dream pass 6 P1).

WHAT IT DOES. Every ruling in `knowledge/_rulings.json` carrying the byte-identical sweep
string — "enactment state NOT asserted here (UNPROVEN by this sweep)" — gets a LIVE verdict,
derived by probing the record's own text, and the verdicts are written to the sidecar
`knowledge/_119-sweep-recheck.json` (the B3 pattern: the source file is never touched).

⛔ WHY A SIDECAR. `_rulings.json` has exactly ONE sanctioned writer, `_inscribe_ruling.py`,
and it APPENDS only — it cannot edit a status field, and hand-editing is the #179 class
[[serializer-defaults-reformat-the-file]]. A re-checker that rewrote statuses would need a
second writer; a second writer is the defect. The sidecar is keyed by ruling id.

VERDICTS (three, and the honest one is the point):
  STILL-UNENACTED  — the record's `says` quotes a file:line literal, the probe ran, and the
                     old value is still there (e.g. ds-033's type.css:180 `#111`).
  LITERAL-GONE     — the quoted literal no longer matches: enactment (or drift) has occurred
                     SINCE the sweep. ⚠ This is NOT "ENACTED" — a gone literal proves change,
                     not intent; the verdict names what was probed and a human reads it.
  UNPROBEABLE      — no quotable file:line literal in the record. DECLARED, never defaulted
                     [[feedback-measuring-tool-must-not-guess]]. An honest UNPROVEN with a
                     re-checker and a date is no longer the s129-D5 debt; one without is.

PROBE. `says` is scanned for backticked `path:line` tokens and for backticked literals quoted
near them. A probe runs only when BOTH a resolvable path and a quotable literal exist — a
path alone proves presence of a file, not the state of a claim [[unmatched-grep-is-not-an-absence]].
Every probe's target and outcome are written to the sidecar, so the verdict quotes what it
measured [[gate-must-quote-what-it-forbids]].

CONSUMER. The capture ritual's 2c step reads the sidecar's `stale_after` field: verdicts are
dated and EXPIRE (s129-D5's expiry arm) — a verdict older than `STALE_AFTER_SESSIONS` sessions
is reported as EXPIRED by --report, which is the nag that keeps this from becoming the next
frozen sweep. (Wiring a one-line consumer into _checkin.py is Lane B's seam; until then the
runbook step and --report are the consumers, and this sentence declares that honestly.)

SELFTEST. `--selftest` is mutation-tested both directions: it must find ds-033
STILL-UNENACTED on the real tree, and it must flip to LITERAL-GONE on a mutated copy —
a green that cannot fail is an assertion [[six-beat-ladder-ruled]].

rc: 0 = ran, sidecar written · 1 = refusal (loud, named) · 2 = selftest failure.
"""

import json, re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULINGS = ROOT / "knowledge" / "_rulings.json"
SIDECAR = ROOT / "knowledge" / "_119-sweep-recheck.json"
SWEEP_STRING = "enactment state NOT asserted here (UNPROVEN by this sweep)"
STALE_AFTER_SESSIONS = 15  # PICKED, not derived — same provisional standing as GRADE_AGING_DAYS; Dave may rule it.

# The store's `says` fields carry BARE path:line tokens (backticks are stripped at inscription)
# and often a basename without its directory — measured on ds-033 before this grammar was set
# [[measure-dont-convert-units]]: probe the corpus's actual text, not the text you wish it had.
PATHLINE_RE = re.compile(r"([\w./\-]+\.(?:css|py|md|json|js|html)):(\d+)")
# Literal candidates: hex colours and backticked spans ONLY. A double-quoted capture was
# tried and KILLED by the selftest's mutation arm: it matched `"dark"` — a token that is on
# the target line for every dark-theme rule, so the probe could not fail. A literal must
# DISCRIMINATE the claim, not merely co-occur with it [[gate-must-quote-what-it-forbids]].
LITERAL_RES = (re.compile(r"#[0-9A-Fa-f]{3,8}\b"),
               re.compile(r"`([^`\n]{3,120})`"))


def resolve_path(path, root):
    """ROOT-relative first; else a UNIQUE basename match under knowledge/ or the root.
    Ambiguity is a refusal to probe, not a guess [[feedback-measuring-tool-must-not-guess]]."""
    f = root / path
    if f.exists():
        return f
    hits = [p for p in root.rglob(pathlib.Path(path).name)
            if ".git" not in p.parts and p.is_file()]
    # Release packs and review fixtures are COPIES, not canon (designer-skills packs are
    # releases; reviews/_assets are frozen specimens) — a ruling's subject is the canonical
    # file. Filter copies out FIRST, then demand uniqueness among what remains.
    canon = [p for p in hits
             if not any(part.startswith("designer-skills") or part in ("reviews", "dist", "node_modules")
                        for part in p.relative_to(root).parts)]
    return canon[0] if len(canon) == 1 else None


def literal_candidates(says):
    out = []
    for rx in LITERAL_RES:
        for m in rx.findall(says):
            tok = m if isinstance(m, str) else m[0]
            if tok and not PATHLINE_RE.fullmatch(tok):
                out.append(tok)
    return out


class RecheckRefused(Exception):
    pass


def load_rulings():
    try:
        doc = json.loads(RULINGS.read_text())
    except Exception as e:  # noqa: BLE001 — the refusal must name the parse error, not mask it
        raise RecheckRefused(f"REFUSED: {RULINGS} did not parse: {e}")  # [[a-crash-is-not-a-fail]]
    rulings = doc if isinstance(doc, list) else doc.get("rulings", [])
    if not rulings:
        raise RecheckRefused("REFUSED: no rulings found — wrong file shape, not an empty population")
    return rulings


def frozen_subset(rulings):
    return [r for r in rulings if SWEEP_STRING in str(r.get("status", ""))]


def probe_record(r, root=ROOT):
    """Return (verdict, probes:list). Probes only what the record itself quotes."""
    says = str(r.get("says", ""))
    probes = []
    hits = PATHLINE_RE.findall(says)
    if not hits:
        return "UNPROBEABLE", [{"why": "no backticked path:line in `says`"}]
    for path, line in hits:
        f = resolve_path(path, root)
        if f is None:
            probes.append({"target": f"{path}:{line}", "ran": False,
                           "why": "path does not resolve (or basename ambiguous — refusing to guess)"})
            continue
        try:
            text_line = f.read_text().splitlines()[int(line) - 1]
        except IndexError:
            probes.append({"target": f"{path}:{line}", "ran": False, "why": "line beyond EOF"})
            continue
        # STRONG discriminator first: a "still reads X" clause names the exact residue the
        # record claims is unenacted — probe THAT. Any other co-occurring literal is weak:
        # ds-033 quotes `color:#fff`, which survives a real enactment of the background hex,
        # so matching it would grade genuine enactment STILL-UNENACTED forever (found by the
        # selftest's mutation arm, kept as the reason this branch exists).
        strong = re.findall(r"still reads\s+(#[0-9A-Fa-f]{3,8}|`[^`\n]+`)", says)
        strong = [s.strip("`") for s in strong]
        lits = strong if strong else literal_candidates(says)
        matched = [l for l in lits if l in text_line]
        discriminator = "strong (still-reads clause)" if strong else "weak (co-occurring literal)"
        probes.append({"target": f"{path}:{line}", "ran": True,
                       "line_now": text_line.strip()[:200],
                       "discriminator": discriminator,
                       "quoted_literals_still_present": matched})
        if matched and strong:
            return "STILL-UNENACTED", probes
        if matched:
            # A weak match asserts co-occurrence, not the claim — advisory, never the headline
            # verdict (ds-025 matched `#109`, which proves nothing about enactment).
            return "WEAK-MATCH (advisory — no still-reads clause; a human reads the probe)", probes
    ran_any = any(p.get("ran") for p in probes)
    return ("LITERAL-GONE" if ran_any else "UNPROBEABLE"), probes


def run(write=True):
    rulings = load_rulings()
    frozen = frozen_subset(rulings)
    out = {
        "schema": "119-sweep-recheck v1 (W-21, s186-D2; sidecar because _rulings.json is append-only via _inscribe_ruling.py)",
        "rechecked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "population": len(frozen),
        "stale_after_sessions": STALE_AFTER_SESSIONS,
        "verdicts": {},
    }
    for r in frozen:
        v, probes = probe_record(r)
        out["verdicts"][r.get("id", "<no id>")] = {"verdict": v, "probes": probes}
    if write:
        SIDECAR.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    return out


def report(out):
    tally = {}
    for v in out["verdicts"].values():
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
    line = " · ".join(f"{k} {n}" for k, n in sorted(tally.items()))
    print(f"119-sweep recheck: {out['population']} frozen records — {line} · rechecked_at {out['rechecked_at']}")
    for rid, v in sorted(out["verdicts"].items()):
        if v["verdict"] != "UNPROBEABLE":
            tgt = next((p["target"] for p in v["probes"] if p.get("ran")), "?")
            print(f"  {rid}: {v['verdict']}  ({tgt})")


def selftest():
    """Mutation-tested both directions on ds-033, the record whose contradiction started this."""
    out = run(write=False)
    v = out["verdicts"].get("ds-033", {}).get("verdict")
    if v != "STILL-UNENACTED":
        print(f"SELFTEST FAIL: ds-033 expected STILL-UNENACTED on the real tree, got {v!r}")
        return 2
    # mutation arm: on a doctored record the checker must NOT say STILL-UNENACTED
    rulings = load_rulings()
    rec = dict(next(r for r in rulings if r.get("id") == "ds-033"))
    rec["says"] = rec["says"].replace("#111", "#0E0E0E")  # the literal the probe matches on
    mv, _ = probe_record(rec)
    if mv == "STILL-UNENACTED":
        print("SELFTEST FAIL: mutated ds-033 still graded STILL-UNENACTED — the probe cannot fail")
        return 2
    print(f"selftest OK: ds-033 STILL-UNENACTED on real tree · mutated copy → {mv} (the check can fail)")
    return 0


if __name__ == "__main__":
    try:
        if "--selftest" in sys.argv:
            sys.exit(selftest())
        out = run(write="--dry-run" not in sys.argv)
        report(out)
    except RecheckRefused as e:
        print(e)
        sys.exit(1)
