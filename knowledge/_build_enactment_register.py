#!/usr/bin/env python3
"""Build _ENACTMENT-REGISTER.md — is each RULING actually in force?

WHY THIS EXISTS (ADR-0016, 2026-07-27; ruled by Dave: "we are losing decisions").
Our gates prove the corpus is SELF-CONSISTENT. Nothing proved a RULING IS LIVE in the
artefact Dave looks at. DV-D08 was ruled, inscribed, gated-green and silently not in
force for weeks. Every regression on Dave's ds-014 list was found by his eye.

This register is P1: it does not fix anything, it MEASURES the debt. One row per ruling.

THE FOUR VERDICTS — the middle one is the point:
  PROVEN      an executable check names the ruling AND a selftest case proves that
              check can FAIL on it. This is the only verdict that means "in force".
  CLAIMED     a check names the ruling but nothing proves the check can fail on it.
              ds-013 lived here: _sweep_type_enactment.py reported a cheerful
              "0 deviations" when it could not read the stylesheet at all.
  UNPROVEN    no executable check names the ruling. Most rows. That count is the finding.
  NOT-GATEABLE the ledger says so explicitly, with a reason. Never inferred.

Plus a SCOPE-BLINDNESS audit, which is how dv-004 escaped: a gate that branches on a
corpus vocabulary silently skips values it does not enumerate. Chart-bar's stacked figure
declares data-dv-type="stacked-column"; the dv-004 branch tests for "stacked". The gate
passed by never looking.

Usage:  python3 knowledge/_build_enactment_register.py [--check]
        --check = exit 1 if the register on disk is stale (build-step mode, ADVISORY first).
"""
import os, re, sys, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "_ENACTMENT-REGISTER.md")

LEDGERS = [("_proforma/_DATAVIZ-DECISIONS.md", "DV-D"),
           ("_proforma/_RAG-DECISIONS.md",     "R-D"),
           ("_proforma/_TYPE-DECISIONS.md",    "T-D"),
           ("_proforma/_BUTTON-DECISIONS.md",  "B-D")]
ADR_DIR = os.path.join(REPO, "docs", "decisions")

RULING_RE = re.compile(r"\b((?:DV-D|R-D|T-D|B-D)\d+)\b")
ADR_RE = re.compile(r"\b(ADR-\d{4})\b")
# Explicit, never inferred. The ledger must SAY it.
NOTGATE_RE = re.compile(
    r"not[- ]gateable|no gate can|cannot be gated|ungateable|judgment call|"
    r"eyeball only|not mechanically checkable", re.I)


def check_files():
    """Every executable check in the engine."""
    out = []
    for d in (HERE, os.path.join(HERE, "compliance")):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if re.match(r"(_validate_|_check_|_sweep_|_verify_|gen_).*\.(py|js)$", f):
                out.append(os.path.join(d, f))
    return out


def selftest_region(src):
    """Text of the file from its first selftest marker on. A ruling ID inside this
    region is evidence the check has a case that BITES on it."""
    m = re.search(r"def\s+_?selftest|SELFTEST|cases\s*=\s*\[|cases\.append", src)
    return src[m.start():] if m else ""


def harvest_rulings():
    """id -> {headline, source, notgateable, reason}. The DEFINING line is the one where
    the ID is followed by a separator — ledgers write `DV-D11 · The LEGEND MODEL …`."""
    rulings = {}
    for rel, prefix in LEDGERS:
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            continue
        lines = open(path, encoding="utf-8").read().splitlines()
        for i, ln in enumerate(lines):
            for rid in RULING_RE.findall(ln):
                if not rid.startswith(prefix):
                    continue
                defining = re.search(re.escape(rid) + r"\s*[·—\-–:]", ln)
                if rid in rulings and not defining:
                    continue
                if rid not in rulings or defining:
                    block = "\n".join(lines[i:i + 6])
                    ng = NOTGATE_RE.search(block)
                    head = re.sub(r"^[#>\-\*\s]+", "", ln).strip()
                    head = re.sub(r"\*\*", "", head)[:150]
                    rulings[rid] = {"headline": head, "source": rel,
                                    "notgateable": bool(ng),
                                    "reason": ng.group(0) if ng else ""}
    if os.path.isdir(ADR_DIR):
        for f in sorted(os.listdir(ADR_DIR)):
            m = ADR_RE.match(f)
            if not m:
                continue
            first = ""
            for ln in open(os.path.join(ADR_DIR, f), encoding="utf-8"):
                if ln.startswith("#"):
                    first = re.sub(r"^#+\s*", "", ln).strip()
                    break
            rulings[m.group(1)] = {"headline": first[:150],
                                   "source": "docs/decisions/" + f,
                                   "notgateable": False, "reason": ""}
    return rulings


def harvest_checks():
    """ruling id -> {'named': [files], 'bitten': [files]}"""
    idx = collections.defaultdict(lambda: {"named": [], "bitten": []})
    for path in check_files():
        src = open(path, encoding="utf-8", errors="replace").read()
        st = selftest_region(src)
        name = os.path.relpath(path, REPO)
        for rid in set(RULING_RE.findall(src)) | set(ADR_RE.findall(src)):
            idx[rid]["named"].append(name)
            if rid in st:
                idx[rid]["bitten"].append(name)
    return idx


def scope_blindness():
    """Vocabulary values live in the corpus that no gate branch enumerates.
    Seeded with the one PROVEN case (data-dv-type / _validate_dataviz.py, 2026-07-27)."""
    findings = []
    corpus = []
    for sub in ("snippets", "_proforma"):
        d = os.path.join(HERE, sub)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".html"):
                corpus.append(os.path.join(d, f))
    live = collections.Counter()
    for p in corpus:
        for v in re.findall(r'data-dv-type="([^"]+)"', open(p, encoding="utf-8").read()):
            live[v] += 1
    gate = os.path.join(HERE, "_validate_dataviz.py")
    if os.path.exists(gate) and live:
        gsrc = open(gate, encoding="utf-8").read()
        known = set(re.findall(r'"([a-z][a-z\-]*)"', gsrc))
        for val, n in sorted(live.items()):
            if val not in known:
                findings.append({"vocabulary": "data-dv-type", "value": val, "uses": n,
                                 "gate": "knowledge/_validate_dataviz.py",
                                 "note": "declared in the corpus, matched by no branch — "
                                         "every dtype-keyed rule silently skips it"})
    return findings


def render(rulings, idx, blind):
    rows, tally = [], collections.Counter()
    for rid in sorted(rulings, key=lambda s: (re.sub(r"\d+$", "", s),
                                              int(re.search(r"\d+$", s).group()))):
        r = rulings[rid]
        c = idx.get(rid, {"named": [], "bitten": []})
        if r["notgateable"]:
            verdict, ev = "NOT-GATEABLE", r["reason"]
        elif c["bitten"]:
            verdict, ev = "PROVEN", ", ".join(sorted(set(c["bitten"])))
        elif c["named"]:
            verdict, ev = "CLAIMED", ", ".join(sorted(set(c["named"])))
        else:
            verdict, ev = "UNPROVEN", "—"
        tally[verdict] += 1
        rows.append((rid, verdict, r["headline"], ev, r["source"]))

    total = sum(tally.values())
    L = []
    A = L.append
    A("# Enactment register — is each ruling actually IN FORCE?\n")
    A("> GENERATED by `knowledge/_build_enactment_register.py`. Do not hand-edit.\n>")
    A("> **P1 of the ADR-0016 build** (Dave ruled it 2026-07-27: *\"we are losing decisions,")
    A("> this is getting frustrating\"*). Gates prove the corpus is SELF-CONSISTENT; this asks")
    A("> the different question — **is the ruling live in the artefact Dave looks at?**\n")
    A("| verdict | count | meaning |")
    A("|---|---:|---|")
    A("| **PROVEN** | %d | a check names it AND a selftest proves that check can FAIL on it |"
      % tally["PROVEN"])
    A("| **CLAIMED** | %d | a check names it, nothing proves it can fail — the dangerous middle |"
      % tally["CLAIMED"])
    A("| **UNPROVEN** | %d | no executable check names it at all |" % tally["UNPROVEN"])
    A("| **NOT-GATEABLE** | %d | the ledger says so explicitly, with a reason |"
      % tally["NOT-GATEABLE"])
    A("| **TOTAL** | %d | |\n" % total)
    pct = (100.0 * tally["PROVEN"] / total) if total else 0
    A("**%d of %d rulings (%.0f%%) are PROVEN.** That number is the finding, not a failure "
      "of this script.\n" % (tally["PROVEN"], total, pct))
    # Denominator line — dream-pass-3 P2 (ruled 2026-07-28): the register must name its own
    # corpus. Derived from LEDGERS so it cannot drift from what is actually harvested.
    # Widening LEDGERS/RULING_RE is a separate, ruled decision (Dave's, unscheduled).
    A("**Denominator (P2, 2026-07-28): %d ledgers harvested — %s — plus `docs/decisions/ADR-*.md`. "
      "Deliberately OUTSIDE it: the Memento governance set (`notes/_MEMENTO-DECISIONS.md`, ~50 keyed "
      "rulings) and the ds-* body (`knowledge/_DS-IMPROVEMENTS.md`). Read the %.0f%% as *of the "
      "pillar ledgers*, not *of the project*.**\n"
      % (len(LEDGERS), " · ".join("`%s`" % rel for rel, _ in LEDGERS), pct))
    A("⚠ **CLAIMED is not a soft PROVEN.** ds-013 lived in CLAIMED for weeks: "
      "`_sweep_type_enactment.py` named its subject and reported *0 deviations* while it "
      "could not read the stylesheet at all. A green light from a blind check is worse than "
      "no check.\n")

    A("## Scope blindness — gates that cannot see part of their own corpus\n")
    if blind:
        A("| vocabulary | value | uses | gate | consequence |")
        A("|---|---|---:|---|---|")
        for b in blind:
            A("| `%s` | `%s` | %d | `%s` | %s |"
              % (b["vocabulary"], b["value"], b["uses"], b["gate"], b["note"]))
        A("")
        A("*OBSERVED 2026-07-27: this is exactly how **dv-004** (BLOCKING, ≥2px separation "
          "between colour blocks) passed on a chart with **0.0px** separation. Dave saw it; "
          "the build did not.*\n")
    else:
        A("*No scope-blind vocabulary values detected.*\n")

    A("## The register\n")
    A("| ruling | verdict | headline | evidence | ledger |")
    A("|---|---|---|---|---|")
    for rid, verdict, head, ev, src in rows:
        A("| `%s` | **%s** | %s | %s | `%s` |"
          % (rid, verdict, head.replace("|", "\\|"), ev.replace("|", "\\|"), src))
    A("")
    A("---\n")
    A("**P2** writes real ruled-vs-rendered proofs, flagged rows first. **P3** wires this as an "
      "advisory build step, blocking once the register is green or deliberately waived — the "
      "`_validate_partials.py` ratchet posture. *A gate that fails 80 rows on day one gets "
      "switched off, and a switched-off gate is how we got here.*\n")
    return "\n".join(L), tally, total


def main():
    rulings = harvest_rulings()
    idx = harvest_checks()
    blind = scope_blindness()
    text, tally, total = render(rulings, idx, blind)

    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur.strip() != text.strip():
            print("enactment register: STALE — re-run knowledge/_build_enactment_register.py")
            return 1
        print("enactment register: up to date (%d rulings, %d proven)" % (total, tally["PROVEN"]))
        return 0

    # anti-blind-check: this script must never report a cheerful empty register
    if total == 0:
        print("enactment register: harvested ZERO rulings — refusing to write. "
              "Check LEDGERS paths.")
        return 2
    open(OUT, "w", encoding="utf-8").write(text + "\n")
    json.dump({"total": total, "tally": dict(tally), "scope_blind": blind},
              open(os.path.join(HERE, "_enactment-register.json"), "w"), indent=1)
    print("enactment register: %d rulings -> PROVEN %d · CLAIMED %d · UNPROVEN %d · "
          "NOT-GATEABLE %d  (%s)"
          % (total, tally["PROVEN"], tally["CLAIMED"], tally["UNPROVEN"],
             tally["NOT-GATEABLE"], os.path.relpath(OUT, REPO)))
    if blind:
        print("  scope-blind vocabulary values: %s"
              % ", ".join("%s=%s" % (b["vocabulary"], b["value"]) for b in blind))
    return 0


if __name__ == "__main__":
    sys.exit(main())
