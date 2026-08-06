#!/usr/bin/env python3
"""Conductor-surface recorder — RULED #112-D1 (Dave), built #113.

WHY THIS EXISTS, and why it is the THIRD attempt:

  #109  measured the boot floor and never wrote the samples down next to the constant.
  #110  measured a SUB's injected surface, not the conductor's own.
  #111  named the remedy verbatim — "record the conductor's own surface decomposition at
        every wrap" — and did not build it. Its measurement went into banner PROSE only.
  #112  ruled it FIRST, before any probe: "otherwise #112 measures one number and #113 is
        blind again — that is the #109 defect a third time."  Its budget went elsewhere.

The defect all three share is not measurement, it is STORAGE. A number in a banner cannot be
diffed against next session. This module's whole job is to make consecutive sessions diffable.

★ THE UNIT IS REAL CLAUDE TOKENS (#82-D1, Dave's, ruled #54) — MEASURED, NEVER CONVERTED.
  Every figure here goes through `_gauge_tokens.count()`, which returns `(tokens, method)` and
  refuses rather than guessing. This module never accepts a bare int from anywhere.

★ WHAT CANNOT BE MEASURED IS NAMED, NEVER DEFAULTED (Dave, #112: "if you have no instrument
  for a number, SAY SO and ask — never reuse a stale reading"). A component that was not
  captured is recorded as a DECLARED GAP with a reason. It is never omitted and never zeroed.
  A silent gap fails; a declared gap passes. That asymmetry is the entire mechanism.

⚠ THE CAPTURE PROBLEM, stated honestly. The conductor's surface — the deferred-tool list, the
  MCP instruction blocks, the system prompt — lives in the model's context, NOT on disk. There
  is no API that hands it over. To measure it, the conductor must reproduce it into a file.
  That reproduction is what cost #111 ~32K fill. This module does not abolish that cost; it
  makes it PAYABLE ONCE per changed component, by storing a content hash so an unchanged
  component is recognised as unchanged next session.

⛔ CARRYING A PRIOR MEASUREMENT FORWARD IS LEGAL ONLY ON A HASH MATCH. An assertion that a
  component is "unchanged" is NOT evidence — it is recorded as UNVERIFIED and counts as a
  declared gap, not as a measurement. This is the clause that stops a stale reading being
  laundered into a fresh record, which is what Dave ruled against at #112.

CLI
    _surface_recorder.py record --session 113 --from <dir> [--boot 55025]
    _surface_recorder.py diff 112 113
    _surface_recorder.py show [--session N]
    _surface_recorder.py selftest

`--from <dir>` is a staging directory of plain-text files, one per component. Recognised
names are in `COMPONENTS`; anything else is recorded under `extra` and still measured.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gauge_tokens as gt  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_surface-samples.json")

# The components of the conductor's boot surface. `on_disk` ones the recorder can read for
# itself; the rest MUST be staged by the conductor because they exist only in its context.
COMPONENTS = {
    "memory_md":      {"on_disk": None,  # resolved at runtime — the mounted auto-memory
                       "what": "MEMORY.md, the auto-memory index injected every session"},
    "chain_md":       {"on_disk": "_CHAIN.md",
                       "what": "_CHAIN.md — ADDITIVE, lands at turn 2 on top of boot"},
    "deferred_tools": {"on_disk": None,
                       "what": "the deferred-tool name list (server-prefixed tool names)"},
    "mcp_blocks":     {"on_disk": None,
                       "what": "MCP server instruction blocks, concatenated"},
    "skill_catalog":  {"on_disk": None,
                       "what": "the available-skills listing"},
    "agent_types":    {"on_disk": None,
                       "what": "the available agent-types listing"},
    "system_prompt":  {"on_disk": None,
                       "what": "the system prompt proper, excluding the blocks above"},
}

# ⛔ SCOPE — CAUGHT #113 BY DRIVING THE THING, after the tests were already green.
# Not every component is resident at the FIRST TURN. `_CHAIN.md` is ADDITIVE: it lands at turn 2,
# on TOP of boot (`_gauge_tokens.py:115`, and it has said so since #33). The first version of this
# module summed every component and subtracted the lot from the boot figure, which silently
# understated the unattributed remainder by the whole size of the chain — 11,345 real.
# ★ The tests were ALL GREEN and five mutations killed five clauses. None of them could see this,
#   because every test used synthetic content where the scope distinction does not exist. A ceiling
#   carries its own unit; a component carries its own SCOPE. [[measure-dont-convert-units]]
ADDITIVE = {"chain_md"}          # measured, but NOT part of the first-turn boot total

# ⚠ n=1. #112 measured boot 55,025 vs #111's 55,733 = -708 with an UNCHANGED server set and an
# UNCHANGED MEMORY.md. That is ONE observation, not a distribution. It is stored so a diff can
# LABEL a delta, never so a diff can DISMISS one. Re-derive it; do not inherit it.
NOISE_FLOOR_TK = 708
NOISE_FLOOR_N = 1
NOISE_FLOOR_SRC = "#112 vs #111, unchanged servers + unchanged MEMORY.md"


class CaptureRefused(RuntimeError):
    """Raised when a record would have to be written with a number nobody measured."""


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:32]


def _now() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def load() -> list[dict]:
    try:
        with open(STORE, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        return []
    if not isinstance(d, list):
        raise CaptureRefused(f"{STORE} is not a list — refusing to append to a store "
                             f"whose shape I do not recognise (found {type(d).__name__}).")
    return d


def save(samples: list[dict]) -> None:
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=1, ensure_ascii=False)
        f.write("\n")


def sample_for(session: int, samples: list[dict] | None = None) -> dict | None:
    for s in (samples if samples is not None else load()):
        if s.get("session") == session:
            return s
    return None


def measure_component(name: str, text: str) -> dict:
    """Measure one component. The method travels WITH the number, always."""
    tk, method = gt.count(text)
    if method != "real":
        # An estimate is not a measurement. Record it, LABEL it, never let it read as real.
        return {"tk": tk, "method": method, "sha": _sha(text), "bytes": len(text.encode()),
                "verified": False,
                "note": f"method={method!r}, NOT real tokens — this figure may not be "
                        f"compared against a real-token constant"}
    return {"tk": tk, "method": "real", "sha": _sha(text), "bytes": len(text.encode()),
            "verified": True}


def carry_forward(name: str, prior: dict, asserted_unchanged: bool) -> dict:
    """Carry a prior measurement into this session's record.

    ⛔ LEGAL ONLY on evidence. Without the content there is no hash, so there is no evidence —
    only an assertion. An asserted carry is recorded UNVERIFIED and counts as a declared gap.
    """
    out = dict(prior)
    out["carried_from"] = prior.get("_session")
    if asserted_unchanged:
        out["verified"] = False
        out["note"] = ("CARRIED ON ASSERTION, NOT ON A HASH MATCH — no content was supplied "
                       "this session, so 'unchanged' is unevidenced. Counts as a DECLARED GAP.")
    return out


def build_record(session: int, staged: dict[str, str], *, boot_tk: int | None = None,
                 gaps: dict[str, str] | None = None, servers: dict | None = None) -> dict:
    """Build (do not write) one session record from staged component text."""
    comps: dict[str, dict] = {}
    declared: dict[str, str] = dict(gaps or {})

    for name, text in staged.items():
        if text is None:
            declared.setdefault(name, "staged as None — no content supplied")
            continue
        comps[name] = measure_component(name, text)
        comps[name]["_session"] = session

    # Anything in COMPONENTS neither measured nor explicitly declared is a SILENT gap.
    # Silent gaps are the failure mode this whole module exists to prevent. Refuse.
    silent = [k for k in COMPONENTS if k not in comps and k not in declared]
    if silent:
        raise CaptureRefused(
            "SILENT GAP — these surface components were neither measured nor declared: "
            + ", ".join(sorted(silent))
            + ".\nDeclare each with --gap NAME=REASON, or stage its content. A declared gap "
              "passes; a silent one fails. (Dave, #56: 'a DECLARED gap passes, a SILENT one "
              "fails — that asymmetry is the mechanism.')")

    ok = {k: c for k, c in comps.items() if c.get("verified")}
    measured_total = sum(c["tk"] for c in ok.values())
    boot_measured = sum(c["tk"] for k, c in ok.items() if k not in ADDITIVE)
    additive = sum(c["tk"] for k, c in ok.items() if k in ADDITIVE)
    rec = {
        "session": session,
        "at": _now(),
        "unit": "real Claude tokens (_gauge_tokens.count) — MEASURED, never converted",
        "boot_firstturn_tk": boot_tk,
        "boot_source": "message.usage first turn" if boot_tk is not None else None,
        "components": comps,
        "declared_gaps": declared,
        "servers": servers or {},
        "measured_total_tk": measured_total,
        "boot_measured_tk": boot_measured,
        "additive_tk": additive,
        "additive_components": sorted(k for k in ok if k in ADDITIVE),
    }
    if boot_tk is not None:
        # The residual is a SUBTRACTION, and it is labelled as one. #111-D3: a number arrived
        # at by subtraction has not been attributed, it has been assumed.
        # ⛔ Only BOOT-SCOPE components subtract. An additive one does not live in this total.
        rec["unattributed_tk"] = boot_tk - boot_measured
        rec["floor_tk"] = boot_tk + additive
        rec["floor_note"] = ("boot first-turn + ADDITIVE components — the real cost before a "
                             "word of work. Compare against `_gauge_tokens` BOOT_FIRSTTURN_TK "
                             "(+ its chain line), never against a fill reading.")
        rec["unattributed_note"] = ("ARRIVED AT BY SUBTRACTION, NOT MEASURED. Dave #111-D3: "
                                    "'The drop has NOT been attributed to the residual. It has "
                                    "been assumed to be.' Do not rule on this number.")
    return rec


def record(session: int, staged: dict[str, str], **kw) -> dict:
    rec = build_record(session, staged, **kw)
    samples = load()
    samples = [s for s in samples if s.get("session") != session]
    samples.append(rec)
    samples.sort(key=lambda s: s.get("session", 0))
    save(samples)
    return rec


def diff(a: int, b: int, samples: list[dict] | None = None) -> dict:
    """Diff two sessions' surfaces. THIS is the output #111-D3 was missing."""
    samples = samples if samples is not None else load()
    ra, rb = sample_for(a, samples), sample_for(b, samples)
    missing = [str(s) for s, r in ((a, ra), (b, rb)) if r is None]
    if missing:
        raise CaptureRefused(
            f"no surface sample recorded for session(s) {', '.join(missing)}. "
            f"A diff cannot be synthesised from a banner — that is the #109/#110/#111 defect. "
            f"Recorded sessions: {sorted(s.get('session') for s in samples) or 'none'}.")

    per: dict[str, dict] = {}
    for name in sorted(set(ra["components"]) | set(rb["components"])):
        ca, cb = ra["components"].get(name), rb["components"].get(name)
        if ca and cb:
            same = ca.get("sha") == cb.get("sha")
            per[name] = {"a": ca["tk"], "b": cb["tk"], "delta": cb["tk"] - ca["tk"],
                         "identical_content": same,
                         "both_real": ca.get("verified") and cb.get("verified")}
        else:
            per[name] = {"a": ca["tk"] if ca else None, "b": cb["tk"] if cb else None,
                         "delta": None,
                         "note": "present in only one session — not diffable, NOT zero"}

    def _sum(keys) -> int:
        return sum(per[k]["delta"] for k in keys
                   if per[k].get("delta") is not None and per[k].get("both_real"))

    # ⛔ Only BOOT-SCOPE deltas may be set against a boot delta. An additive component's growth
    # is real cost but it is NOT part of the first-turn total, so netting it here would credit
    # the residual with movement that never happened in boot.
    attributed = _sum([k for k in per if k not in ADDITIVE])
    additive_delta = _sum([k for k in per if k in ADDITIVE])
    out = {"a": a, "b": b, "per_component": per, "attributed_delta_tk": attributed,
           "additive_delta_tk": additive_delta,
           "declared_gaps_a": ra.get("declared_gaps", {}),
           "declared_gaps_b": rb.get("declared_gaps", {})}

    ba, bb = ra.get("boot_firstturn_tk"), rb.get("boot_firstturn_tk")
    if ba is not None and bb is not None:
        total = bb - ba
        out["boot_delta_tk"] = total
        out["unattributed_delta_tk"] = total - attributed
        # LABEL, never dismiss. n=1 is stated in the same breath as the label.
        mag = abs(out["unattributed_delta_tk"])
        out["noise_floor_tk"] = NOISE_FLOOR_TK
        out["noise_floor_n"] = NOISE_FLOOR_N
        out["noise_floor_src"] = NOISE_FLOOR_SRC
        out["unattributed_vs_noise"] = (
            f"{mag / NOISE_FLOOR_TK:.1f}x noise floor" if NOISE_FLOOR_TK else "n/a")
        out["verdict"] = ("SIGNAL — larger than the observed noise floor"
                          if mag > NOISE_FLOOR_TK else
                          "WITHIN NOISE FLOOR — but n=1, so this label is weak evidence, "
                          "not a dismissal")
    else:
        out["boot_delta_tk"] = None
        out["unattributed_delta_tk"] = None
        out["verdict"] = ("boot figure absent for at least one session — the unattributed "
                          "quantity CANNOT be computed and is not defaulted to zero")
    return out


def render_diff(d: dict) -> str:
    L = [f"SURFACE DIFF  #{d['a']} → #{d['b']}   (unit: real Claude tokens)", ""]
    L.append(f"  {'component':<18}{'#'+str(d['a']):>10}{'#'+str(d['b']):>10}{'delta':>10}   note")
    for name, p in d["per_component"].items():
        a = f"{p['a']:,}" if p["a"] is not None else "—"
        b = f"{p['b']:,}" if p["b"] is not None else "—"
        dl = f"{p['delta']:+,}" if p["delta"] is not None else "—"
        note = ""
        if p.get("identical_content"):
            note = "content IDENTICAL (sha match)"
        elif p.get("note"):
            note = p["note"]
        elif p.get("both_real") is False:
            note = "⚠ not both real-token measurements"
        L.append(f"  {name:<18}{a:>10}{b:>10}{dl:>10}   {note}")
    L += ["", f"  attributed delta      {d['attributed_delta_tk']:+,}   (boot-scope only)",
          f"  additive delta        {d['additive_delta_tk']:+,}   "
          f"({', '.join(sorted(ADDITIVE))} — real cost, NOT in boot)"]
    if d.get("boot_delta_tk") is not None:
        L.append(f"  boot delta            {d['boot_delta_tk']:+,}")
        L.append(f"  UNATTRIBUTED          {d['unattributed_delta_tk']:+,}   "
                 f"({d['unattributed_vs_noise']})")
        L.append(f"  noise floor           {d['noise_floor_tk']:,}  "
                 f"n={d['noise_floor_n']} — {d['noise_floor_src']}")
    L.append(f"  verdict: {d['verdict']}")
    for side in ("a", "b"):
        g = d[f"declared_gaps_{side}"]
        if g:
            L.append(f"  declared gaps #{d[side]}: " + "; ".join(f"{k} ({v})" for k, v in g.items()))
    return "\n".join(L)


def stage_from_dir(path: str) -> dict[str, str]:
    staged: dict[str, str] = {}
    if not os.path.isdir(path):
        raise CaptureRefused(f"staging dir not found: {path}")
    for fn in sorted(os.listdir(path)):
        if fn.startswith("."):
            continue
        name = os.path.splitext(fn)[0]
        with open(os.path.join(path, fn), encoding="utf-8", errors="replace") as f:
            staged[name] = f.read()
    if not staged:
        raise CaptureRefused(f"staging dir {path} is empty — nothing to measure. "
                             f"An empty capture is not a zero surface.")
    return staged


# ── selftest ──────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    """Drive the clauses. A green that cannot fail is an assertion, not a test (#63-D1)."""
    import tempfile
    global STORE
    fails: list[str] = []
    orig = STORE
    fd, tmp = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.unlink(tmp)
    STORE = tmp

    def chk(name: str, cond: bool, why: str = "") -> None:
        print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  — {why}" if why and not cond else ""))
        if not cond:
            fails.append(name)

    try:
        full = {k: f"surface content for {k} " * 20 for k in COMPONENTS}

        # T1 — a complete capture records and round-trips.
        r1 = record(111, dict(full), boot_tk=55_733)
        chk("T1 complete capture records", sample_for(111) is not None)
        chk("T1 every component measured", len(r1["components"]) == len(COMPONENTS))

        # T2 — a SILENT gap is refused. This is the load-bearing clause.
        part = {k: v for k, v in full.items() if k != "mcp_blocks"}
        try:
            build_record(999, part, boot_tk=1)
            chk("T2 silent gap refused", False, "build_record accepted a missing component")
        except CaptureRefused as e:
            chk("T2 silent gap refused", "mcp_blocks" in str(e) and "SILENT GAP" in str(e))

        # T3 — the SAME gap, DECLARED, passes. Refusal must have a legal discharge, or the
        # gate bites honesty (#111-D1: "No session should ever be blocked with no honest way
        # forward"). T2 and T3 differ by one thing only: the declaration.
        try:
            r3 = build_record(999, part, boot_tk=1, gaps={"mcp_blocks": "not reproduced — "
                                                          "priced at ~2.8K fill, deferred"})
            chk("T3 declared gap passes", "mcp_blocks" in r3["declared_gaps"])
        except CaptureRefused as e:
            chk("T3 declared gap passes", False, f"refused a DECLARED gap: {e}")

        # T4 — an unchanged component is recognised by hash, not by assertion.
        r2 = record(112, dict(full), boot_tk=55_025)
        d = diff(111, 112)
        chk("T4 identical content detected by sha",
            all(p["identical_content"] for p in d["per_component"].values()))
        chk("T4 attributed delta is zero when nothing changed", d["attributed_delta_tk"] == 0)

        # T5 — the unattributed quantity is the boot delta minus what was attributed. THIS is
        # the number #111-D3 said had been assumed rather than measured.
        chk("T5 unattributed = boot delta - attributed",
            d["unattributed_delta_tk"] == (55_025 - 55_733) - 0,
            f"got {d['unattributed_delta_tk']}")
        chk("T5 labelled against the noise floor, with n stated",
            d["noise_floor_n"] == 1 and "noise" in d["verdict"].lower())

        # T6 — a changed component is attributed to that component, not to the residual.
        grown = dict(full)
        grown["memory_md"] = full["memory_md"] + ("extra hook line " * 40)
        record(113, grown, boot_tk=56_000)
        d2 = diff(112, 113)
        chk("T6 changed component flagged not-identical",
            d2["per_component"]["memory_md"]["identical_content"] is False)
        chk("T6 growth attributed to the component",
            d2["per_component"]["memory_md"]["delta"] > 0)
        chk("T6 residual shrinks by exactly what was attributed",
            d2["unattributed_delta_tk"] == (56_000 - 55_025) - d2["attributed_delta_tk"])

        # T7 — a missing sample REFUSES rather than synthesising a diff. The #109/#110/#111
        # defect was precisely that a missing sample got narrated instead of refused.
        try:
            diff(112, 120)
            chk("T7 missing sample refused", False, "diff invented a comparison")
        except CaptureRefused as e:
            chk("T7 missing sample refused", "120" in str(e))

        # T8 — no boot figure ⇒ the unattributed quantity is NOT defaulted to zero.
        record(114, dict(full))
        d3 = diff(113, 114)
        chk("T8 absent boot ⇒ unattributed is None, never 0",
            d3["unattributed_delta_tk"] is None and "not defaulted" in d3["verdict"])

        # T9 — a carry-forward on assertion is marked UNVERIFIED.
        c = carry_forward("mcp_blocks", dict(r2["components"]["mcp_blocks"]), True)
        chk("T9 asserted carry is UNVERIFIED", c["verified"] is False and "ASSERTION" in c["note"])

        # T11 — SCOPE. An ADDITIVE component must not be netted off the boot total. This is the
        # defect the first nine tests could not see, because synthetic content has no scope.
        # Grow ONLY the additive component; boot-scope attribution must not move at all.
        big = dict(full)
        big["chain_md"] = full["chain_md"] + ("chain growth " * 200)
        r11 = record(115, big, boot_tk=55_025)
        r10 = sample_for(114)
        chk("T11 additive excluded from boot_measured",
            r11["boot_measured_tk"] == r11["measured_total_tk"] - r11["components"]["chain_md"]["tk"])
        chk("T11 unattributed uses BOOT scope, not the total",
            r11["unattributed_tk"] == 55_025 - r11["boot_measured_tk"])
        chk("T11 floor = boot + additive, not boot - additive",
            r11["floor_tk"] == 55_025 + r11["additive_tk"] > 55_025)
        d11 = diff(114, 115, [s for s in load() if s["session"] in (114, 115)])
        chk("T11 chain growth lands in additive_delta, NOT attributed",
            d11["additive_delta_tk"] > 0 and d11["attributed_delta_tk"] == 0,
            f"attributed={d11['attributed_delta_tk']} additive={d11['additive_delta_tk']}")
        _ = r10

        # T10 — the store refuses a shape it does not recognise.
        with open(STORE, "w") as f:
            json.dump({"not": "a list"}, f)
        try:
            load()
            chk("T10 bad store shape refused", False, "load() accepted a dict")
        except CaptureRefused:
            chk("T10 bad store shape refused", True)

    finally:
        STORE = orig
        if os.path.exists(tmp):
            os.unlink(tmp)

    print()
    print(f"  {len(fails)} FAILING" if fails else "  ALL GREEN")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("record")
    p.add_argument("--session", type=int, required=True)
    p.add_argument("--from", dest="src", required=True, help="staging dir of component .txt")
    p.add_argument("--boot", type=int, default=None, help="boot first-turn real tokens")
    p.add_argument("--gap", action="append", default=[], metavar="NAME=REASON")

    p = sub.add_parser("diff")
    p.add_argument("a", type=int)
    p.add_argument("b", type=int)

    p = sub.add_parser("show")
    p.add_argument("--session", type=int, default=None)

    sub.add_parser("selftest")
    a = ap.parse_args()

    try:
        if a.cmd == "selftest":
            return selftest()
        if a.cmd == "record":
            gaps = {}
            for g in a.gap:
                if "=" not in g:
                    print(f"⛔ --gap needs NAME=REASON, got {g!r}", file=sys.stderr)
                    return 2
                k, v = g.split("=", 1)
                gaps[k.strip()] = v.strip()
            rec = record(a.session, stage_from_dir(a.src), boot_tk=a.boot, gaps=gaps)
            print(f"recorded #{rec['session']} → {STORE}")
            print(f"  measured total   {rec['measured_total_tk']:,} real")
            if rec.get("unattributed_tk") is not None:
                print(f"  unattributed     {rec['unattributed_tk']:,}  "
                      f"(BY SUBTRACTION — not measured, do not rule on it)")
            for k, v in rec["declared_gaps"].items():
                print(f"  declared gap     {k}: {v}")
            return 0
        if a.cmd == "diff":
            print(render_diff(diff(a.a, a.b)))
            return 0
        if a.cmd == "show":
            s = load()
            if a.session is not None:
                r = sample_for(a.session, s)
                if r is None:
                    print(f"no sample for #{a.session}; have "
                          f"{sorted(x.get('session') for x in s) or 'none'}")
                    return 1
                print(json.dumps(r, indent=1, ensure_ascii=False))
            else:
                for r in s:
                    print(f"#{r['session']:>4}  {r['at']}  measured "
                          f"{r['measured_total_tk']:>8,}  boot "
                          f"{r.get('boot_firstturn_tk') or '—':>8}  "
                          f"gaps {len(r.get('declared_gaps', {}))}")
            return 0
    except (CaptureRefused, gt.MeasurementRefused) as e:
        print(f"⛔ REFUSED: {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
