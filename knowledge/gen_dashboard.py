#!/usr/bin/env python3
"""
gen_dashboard.py — the generated progress dashboard ("mission control").

RULED by Dave at #164: *"this is a priority after the side quest, it will really help
me"*. Brief: `_BRIEF-progress-dashboard-2026-08-13-v1.md`. Two design rulings, his:
(1) the component library is **Mono** — the page consumes `knowledge/canon/canon.css`'s
gated `.cn-*` component scopes and `canon/type.css` composites, inventing nothing;
(2) the aesthetic is the **swiss-design-system** skill — typographic grid, hairline
section rules, the accent-dash label pattern, white space as structure.

SAME LAW AS THE SHOWROOM: built FROM THE STORES, never hand-edited, regenerated as a
build step, so it cannot rot. If a number is wrong, the store is wrong — fix the store
and regenerate. The dashboard REPORTS; it never repairs.

Sources (every panel names its own):
  knowledge/_state.json        — open work, owners, close conditions, the 19-item
                                 UNCONDITIONED legacy set
  knowledge/_rulings.json      — the ruling count and the tail
  knowledge/_governs.py        — RUN here, never asserted: the provenance-gap set
  knowledge/_binds-ratchet.json, knowledge/_type_ratchet.json — the debt ratchets
  _CHAIN.md, _LIVE-STATE.md    — session position
  _FUTURE-STATE.md             — the forward lane
  live gate runs               — the gates-health strip is MEASURED at generation

PRIORITY (#165, Dave: *I generate the priorities, he overrules*):
  The order on this page is a SCORE COMPUTED HERE from six weighted criteria whose
  weights are printed on the page. It is labelled PROPOSAL on every surface it touches,
  it is never written back to a store, and it is regenerated every build — so it cannot
  rot into a decision. Dave overrules with an OPTIONAL `priority_override` integer on a
  `_state.json` item (1 = first), validated when present by `_state.py` and displayed as
  "DAVE OVERRULED → n". ⛔ No override value is authored by this program, ever.
  Where an input does not exist in the store the item is scored AND flagged LOW
  CONFIDENCE with the missing inputs NAMED — `links` is empty across the corpus, which
  is measured and reported on the page as a flagged problem, not repaired here.

DETERMINISM: no timestamps, no git sha. The page's only clock is the session number it
reads out of `_CHAIN.md` plus the measurements themselves, so `--check` means "the
dashboard disagrees with the stores or with a live gate", never "a day has passed".

ACCESSIBILITY LAW APPLIED (standing, Dave):
  * dyslexia — exec summary FIRST, in prose, at 21px; no bullet walls above the fold
  * astigmatism — **no meaning is ever carried by hue alone.** Every verdict is a WORD
    (PASS / FAIL / DEBT / DAVE'S / MINE). Colour is redundant confirmation only.
  * two-red law (s151-D1) + the green mirror (s155-D1), MONO ONLY, light background:
    red #DA1A00-on-white, green #137F3C-on-white. Dark values (#F6604C / #66CC8D) are
    NOT used because this page renders light-only — declared, not smuggled.
  * the Swiss accent is #305A85, a blue already in the repo's legacy information fill.
    It is DECORATIVE ONLY (label dashes, rules) and carries no status meaning — blue
    and green are Dave's stable hues.

Usage:
  python3 knowledge/gen_dashboard.py            # write dashboard/index.html
  python3 knowledge/gen_dashboard.py --check    # regenerate, compare, rc=1 if stale
  python3 knowledge/gen_dashboard.py --no-gates # skip the live gate runs (fast draft)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import concurrent.futures as _fut
import html as htmlmod
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTD = os.path.join(ROOT, "dashboard")
OUT = os.path.join(OUTD, "index.html")

E = lambda s: htmlmod.escape(str(s), quote=True)          # noqa: E731


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# GATES — RUN, never asserted. Read-only invocations only.
#
# ⛔ `_validate_type_composites.py --ratchet` is DELIBERATELY NOT USED: it WRITES
# _type_ratchet.json when the count shrinks, and a reporting surface must not mutate a
# store. We run the plain (read-only) gate, read the baseline, and compute the
# comparison here — labelled as computed, with the owning gate named.
# ---------------------------------------------------------------------------
GATES = [
    ("snippets",        ["_validate_snippets.py"],              "every snippet against the canon contract"),
    ("binds-resolve",   ["_validate_binds_resolve.py"],         "every binds address resolves to a real token leaf"),
    ("binds-ratchet",   ["_validate_binds_ratchet.py"],         "metas carrying binds may only grow"),
    ("palette-tier",    ["_validate_palette_tier.py"],          "every theme names a palette per family (s157-D2)"),
    ("theme-cascade",   ["canon/gen_theme_cascade.py", "--check"], "the projected cascade matches canon.css"),
    ("showroom",        ["gen_showroom.py", "--check"],         "the 75 component pages are in sync"),
    ("provenance",      ["_governs.py", "--selftest"],          "every ruling points a reader at canon"),
    ("type-composites", ["_validate_type_composites.py"],       "raw type declarations outside the composites"),
]

GATE_TIMEOUT = 120


def _run_gate(spec):
    name, argv, why = spec
    env = dict(os.environ)
    env.setdefault("TMPDIR", "/var/tmp")                       # ENOSPC pothole n=6/n=7
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, argv[0])] + argv[1:],
                           cwd=ROOT, env=env, capture_output=True, text=True,
                           timeout=GATE_TIMEOUT)
        rc, out = p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        rc, out = 124, "TIMEOUT after %ds — no verdict" % GATE_TIMEOUT
    except Exception as exc:                                   # a crash is not a fail
        rc, out = 125, "CRASHED, NAMED: %s" % exc
    lines = [ln.rstrip() for ln in out.splitlines() if ln.strip()]
    headline = lines[-1] if lines else "(no output)"
    return {"name": name, "why": why, "rc": rc, "headline": headline,
            "cmd": "python3 knowledge/" + " ".join(argv), "lines": lines}


def run_gates(enabled=True):
    if not enabled:
        return []
    with _fut.ThreadPoolExecutor(max_workers=len(GATES)) as ex:
        return list(ex.map(_run_gate, GATES))


# ---------------------------------------------------------------------------
# STORE READS
# ---------------------------------------------------------------------------
def read_state():
    s = _json(os.path.join(HERE, "_state.json"))
    items = s["items"]
    return {
        "items": items,
        "open": [i for i in items if i["state"] == "open"],
        "blocked": [i for i in items if i["state"] == "blocked"],
        "done": [i for i in items if i["state"] == "done"],
    }


def kanban_columns(items, prio=None):
    """The kanban board, DERIVED — the store has no status/lifecycle field.

    ⛔ NOTHING IS INVENTED. `_state.json` items carry no `status`, `lane`, `phase` or
    `priority` key (checked: all 37 items expose exactly id/title/body/state/opened/
    owner/condition/closes_when/links/home/provenance, plus optional owner_inferred and
    closed_by). The only lifecycle axes that EXIST are:
        * `state`      — open | blocked | done
        * `condition`  — UNCONDITIONED | stated  (i.e. whether `closes_when` is set)
    So the columns are the product of those two, and the panel SAYS SO on the page. The
    derivation is stated, not smuggled in as if the store had shipped these columns.
    """
    cols = [
        {"key": "unconditioned", "name": "No close condition",
         "rule": "state = open AND condition = UNCONDITIONED",
         "note": "the frozen legacy set — may only shrink", "items": []},
        {"key": "conditioned", "name": "Open, condition stated",
         "rule": "state = open AND condition = stated",
         "note": "has a checkable closes_when", "items": []},
        {"key": "blocked", "name": "Blocked",
         "rule": "state = blocked", "note": "the store's own word", "items": []},
        {"key": "done", "name": "Done",
         "rule": "state = done", "note": "carries closed_by", "items": []},
    ]
    by = {c["key"]: c for c in cols}
    for i in items:
        st = i.get("state")
        if st == "done":
            k = "done"
        elif st == "blocked":
            k = "blocked"
        elif i.get("condition") == "UNCONDITIONED":
            k = "unconditioned"
        else:
            k = "conditioned"
        by[k]["items"].append(i)
    for c in cols:
        if prio and c["key"] != "done":
            c["items"] = sort_by_priority(c["items"], prio)
        else:
            c["items"].sort(key=lambda x: x["id"])
    return cols


# ---------------------------------------------------------------------------
# PRIORITY — A PROPOSAL. Derived at generation, never stored.
#
# RULED by Dave (#165): *Claude generates the priorities, Dave overrules.* So this is
# computed here, regenerated every build, and can therefore not rot — and it is
# labelled PROPOSAL everywhere it appears. The overrule channel is the OPTIONAL
# `priority_override` integer on a `_state.json` item (schema #165, gated in
# `_state.py`). ⛔ NO VALUE IS AUTHORED HERE OR IN THE STORE: the field is absent on
# every item until Dave writes one. An agent that both proposes a priority and writes
# it into the store has ruled its own priority and read it back as if it were his.
#
# ⚠ CONFIDENCE IS PART OF THE NUMBER. Where a criterion's input does not exist in the
# store, the item does NOT get a clean score — it gets the score AND a LOW-CONFIDENCE
# flag naming exactly which inputs were missing. A tidy number computed from thin data
# is the failure this whole page exists to avoid [[measuring-tool-must-not-guess]].
# ---------------------------------------------------------------------------
DEADLINE_SET = "Friday 2026-08-14"
_RISK_RE = re.compile(r"\b(gate|gates|validate|selftest|test|instrument|ratchet|"
                      r"mutation|coverage|regress)", re.I)
_DEADLINE_RE = re.compile(r"\b(friday|2026-08-1[34]|deadline|before the wrap)\b", re.I)
_DECISION_RE = re.compile(r"\b(dave|rule[sd]?|ruling|decide|decision|ratif|approve|"
                          r"his word|overrule)", re.I)

# (key, column name, weight, what it measures, where the input comes from)
CRITERIA = [
    ("unlock",   "Unlock",          0.30,
     "how much other work this item is blocking",
     "the item's <code>links</code> array, plus inbound links from other items"),
    ("rot",      "Rot risk",        0.20,
     "cost of delay — how long it has been open, and whether it can even be closed",
     "<code>opened</code> (session number) and <code>condition</code>"),
    ("effort",   "Effort (inverse)", 0.15,
     "a small job scores higher than a big one, all else equal",
     "the item's OPTIONAL <code>effort</code> (S/M/L) where present — otherwise "
     "<strong>PROXY ONLY</strong>: the length of the item's <code>body</code>."),
    ("deadline", "Deadline",        0.15,
     "proximity to the %s set" % DEADLINE_SET,
     "the item's OPTIONAL <code>deadline</code> (ISO date) where present — otherwise "
     "<strong>PROXY ONLY</strong>: a prose scan of <code>title</code>/<code>body</code>/"
     "<code>closes_when</code>."),
    ("risk",     "Risk reduction",  0.10,
     "does closing this close a gate-coverage hole",
     "PROXY ONLY — prose signal (gate / selftest / ratchet / coverage)"),
    ("load",     "Decision relief", 0.10,
     "does finishing this take a decision OFF Dave's plate",
     "<code>owner</code> plus a prose scan for a pending decision"),
]
WEIGHTS_SUM = round(sum(c[2] for c in CRITERIA), 4)   # must be 1.0; asserted at build


# ---- the REAL inputs (#166), where present. Gated in `_state.py`; ABSENT on every item
# until Dave writes one, so today every one of these paths is dark and the PROXY branch
# below is what actually runs. That is the honest state, and the page says so.
EFFORT_SCORE = {"S": 1.0, "M": 0.5, "L": 0.0}   # inverse: small scores higher


def _deadline_score(value, horizon=None):
    """Return 0..1 for a real ISO `deadline`, or None when there is no usable field.

    None is the signal to fall back to the PROXY — it is NEVER silently read as 0.0,
    because a zero and an unmeasured thing are different claims
    [[measuring-tool-must-not-guess]]."""
    if not isinstance(value, str):
        return None
    import datetime as _dt
    try:
        due = _dt.date.fromisoformat(value)
    except ValueError:
        return None
    try:
        ref = _dt.date.fromisoformat((horizon or "").strip().split()[-1])
    except (ValueError, IndexError):
        ref = _dt.date.today()
    days = (due - ref).days
    if days <= 0:
        return 1.0              # due, or overdue
    return max(0.0, min(1.0, 1.0 - days / 30.0))


def _prose(i):
    return " ".join(str(i.get(k) or "") for k in ("title", "body", "closes_when"))


def score_item(i, session, inbound, links_corpus_empty):
    """Return (score 0–100, per-criterion sub-scores, list of MISSING INPUT names).

    Every branch that cannot measure records a missing input by NAME — it never
    silently substitutes zero and reports the total as if it were whole."""
    sub, missing = {}, []

    # --- unlock -------------------------------------------------------------
    n_links = len(i.get("links") or [])
    n_in = inbound.get(i["id"], 0)
    if links_corpus_empty:
        missing.append(("unlock", "no item in the store carries any links, so the "
                        "dependency graph cannot be read"))
        sub["unlock"] = 0.0
    else:
        sub["unlock"] = min(1.0, (n_links + 2 * n_in) / 6.0)

    # --- rot ----------------------------------------------------------------
    opened = i.get("opened")
    if not isinstance(opened, int) or opened <= 0:
        missing.append(("age", "opened is %r — the item's birth session is unknown, so "
                        "cost-of-delay cannot be measured" % opened))
        age_part = 0.0
    else:
        try:
            age_part = min(1.0, max(0, int(session) - opened) / 60.0)
        except (TypeError, ValueError):
            missing.append(("age", "the session number could not be read from _CHAIN.md"))
            age_part = 0.0
    sub["rot"] = min(1.0, age_part + (0.4 if i.get("condition") == "UNCONDITIONED" else 0.0))

    # --- effort -------------------------------------------------------------
    # ⚠ THE REAL INPUT REPLACES THE PROXY, it does not blend with it. A blend would let the
    # prose keep a vote in a criterion Dave has already answered, and would make the score
    # unattributable — you could not say which number moved it.
    eff = i.get("effort")
    if eff in EFFORT_SCORE:
        sub["effort"] = EFFORT_SCORE[eff]
    else:
        if eff is not None:
            missing.append(("effort", "the item carries effort=%r, which is not S/M/L — the "
                            "gate should have refused it; falling back to the body-length "
                            "PROXY and saying so" % (eff,)))
        body = str(i.get("body") or "")
        if not body.strip():
            missing.append(("effort", "the item has no `effort` field and no body text, so "
                            "even the length PROXY has nothing to measure"))
            sub["effort"] = 0.0
        else:
            missing.append(("effort", "the item has no `effort` field — the score reads the "
                            "byte-length of its body as a PROXY, which measures the prose, "
                            "not the work"))
            sub["effort"] = max(0.0, min(1.0, 1.0 - (len(body) / 1200.0)))

    # --- deadline -----------------------------------------------------------
    dl = i.get("deadline")
    dl_score = _deadline_score(dl, DEADLINE_SET)
    if dl_score is not None:
        sub["deadline"] = dl_score
    else:
        if dl is not None:
            missing.append(("deadline", "the item carries deadline=%r, which is not an ISO "
                            "date — the gate should have refused it; falling back to the "
                            "prose PROXY and saying so" % (dl,)))
        missing.append(("deadline", "the item has no `deadline` field — the score reads a "
                        "prose scan of the item's own words as a PROXY, so an item scores "
                        "higher by SAYING 'friday'"))
        sub["deadline"] = 1.0 if _DEADLINE_RE.search(_prose(i)) else 0.0

    # --- risk reduction -----------------------------------------------------
    sub["risk"] = min(1.0, len(set(m.group(0).lower() for m in
                                   _RISK_RE.finditer(_prose(i)))) / 3.0)

    # --- decision-load relief ----------------------------------------------
    if i.get("owner") == "claude":
        sub["load"] = 1.0 if _DECISION_RE.search(_prose(i)) else 0.4
    else:
        sub["load"] = 0.0

    total = sum(w * sub[k] for k, _n, w, _d, _s in CRITERIA)
    return int(round(total * 100)), sub, missing


def priorities(items, session):
    """Score every LIVE item (open/blocked). Done items are not ranked — a finished
    thing has no priority, and giving it one would put it in the queue."""
    links_corpus_empty = not any(i.get("links") for i in items)
    inbound = {}
    for i in items:
        for l in (i.get("links") or []):
            key = str(l).strip()
            inbound[key] = inbound.get(key, 0) + 1
    out = {}
    for i in items:
        if i.get("state") in ("done", "dropped"):
            continue
        s, sub, missing = score_item(i, session, inbound, links_corpus_empty)
        ov = i.get("priority_override")
        ov = ov if isinstance(ov, int) and not isinstance(ov, bool) else None
        out[i["id"]] = {"score": s, "sub": sub, "missing": missing, "override": ov}
    ranked = sorted(out.items(),
                    key=lambda kv: (0 if kv[1]["override"] is not None else 1,
                                    kv[1]["override"] if kv[1]["override"] is not None else 0,
                                    -kv[1]["score"], kv[0]))
    for n, (iid, rec) in enumerate(ranked, 1):
        rec["rank"] = n
    return {"by_id": out, "ranked": [iid for iid, _ in ranked],
            "links_corpus_empty": links_corpus_empty,
            "n_overrides": sum(1 for r in out.values() if r["override"] is not None)}


def links_coverage(items):
    """MEASURED, never repaired (Dave, #165: sparse links is a FLAGGED PROBLEM).

    The dashboard reports the coverage number and queues the backfill as Dave's work.
    Backfilling links would be an agent inventing the dependency graph it then scores
    itself against — a closed loop with no reader in it."""
    total = len(items)
    withl = sum(1 for i in items if i.get("links"))
    live = [i for i in items if i.get("state") not in ("done", "dropped")]
    return {"total": total, "with_links": withl,
            "pct": (100.0 * withl / total) if total else 0.0,
            "live_total": len(live),
            "live_with_links": sum(1 for i in live if i.get("links"))}


def sort_by_priority(group, prio):
    """Rank order: an OVERRULE always wins; then the proposed score; then id."""
    def key(i):
        r = prio["by_id"].get(i["id"])
        if not r:
            return (2, 0, 0, i["id"])
        if r["override"] is not None:
            return (0, r["override"], 0, i["id"])
        return (1, 0, -r["score"], i["id"])
    return sorted(group, key=key)


def short_title(t, n=64):
    """Trim for a card. The FULL title is on the two plates below — this is a glance
    surface, so a trim here loses nothing that the page does not also show in full."""
    t = re.sub(r"\s+", " ", str(t)).strip()
    if len(t) <= n:
        return t, False
    cut = t[:n].rsplit(" ", 1)[0]
    return (cut or t[:n]) + "…", True


def read_rulings():
    r = _json(os.path.join(HERE, "_rulings.json"))
    rs = r["rulings"]
    return {"n": len(rs), "tail": rs[-1], "rulings": rs}


def provenance_gaps(gate_result):
    """The provenance-gap set, taken VERBATIM from the live _governs run.

    ⛔ NOT authored here. Missing governs/evidence/status values are DAVE'S to supply;
    inventing one would be inventing provenance. We display the gate's own words."""
    if not gate_result:
        return {"fails": [], "ids": [], "measured": False}
    fails = [ln.strip() for ln in gate_result["lines"] if ln.strip().startswith("FAIL")]
    ids = []
    for ln in fails:
        m = re.search(r"ruling '?([a-zA-Z0-9\-]+)'?", ln)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return {"fails": fails, "ids": ids, "measured": True}


def read_session():
    chain = _read(os.path.join(ROOT, "_CHAIN.md"))
    m = re.search(r"YOU ARE #(\d+)", chain)
    session = m.group(1) if m else "unknown"
    t = re.search(r"TITLE THIS CHAT →\*\*\s*`([^`]+)`", chain)
    title = t.group(1) if t else ""
    ls = _read(os.path.join(ROOT, "_LIVE-STATE.md"))
    r = re.search(r"Last refreshed: (\d{4}-\d{2}-\d{2})", ls)
    refreshed = r.group(1) if r else "unknown"
    return {"session": session, "title": title, "refreshed": refreshed}


def read_ratchets():
    binds = _json(os.path.join(HERE, "_binds-ratchet.json"))
    typ = _json(os.path.join(HERE, "_type_ratchet.json"))
    return {"binds": binds, "type": typ}


def type_debt(gate_result, baseline):
    """Measured type-composite count vs the declared shrink-only baseline.

    The comparison is COMPUTED HERE (the owning gate is `--ratchet`, which writes and
    is therefore not run by a reporting surface). Label it as such on the page."""
    if not gate_result:
        return {"count": None, "baseline": baseline, "delta": None}
    m = None
    for ln in gate_result["lines"]:
        m = re.search(r"TYPE GATE FAIL — (\d+) violation", ln) or m
    count = int(m.group(1)) if m else None
    return {"count": count, "baseline": baseline,
            "delta": (count - baseline) if count is not None else None}


def read_future_state():
    txt = _read(os.path.join(ROOT, "_FUTURE-STATE.md"))
    blocks = re.split(r"^## ", txt, flags=re.M)[1:]
    out = []
    for b in blocks:
        head = b.splitlines()[0].strip()
        st = re.search(r"\*\*Status:\*\*\s*`([^`]+)`", b)
        born = re.search(r"\[born ([^\]·]+)", b)
        out.append({"title": head,
                    "status": st.group(1) if st else "unstated",
                    "born": born.group(1).strip() if born else ""})
    return out


def wave_claim(rulings):
    """The 114-row bind wave. This is a CLAIM QUOTED FROM THE STORE (s162-D1), not a
    measurement taken here — the page says so."""
    for r in rulings:
        blob = json.dumps(r)
        m = re.search(r"(?:CLOSED|closed)\s*114/114", blob)
        if m:
            return {"id": r["id"], "text": "114/114 — wave CLOSED", "ruled": r.get("ruled", "")}
    return None


# ---------------------------------------------------------------------------
# RENDER
# ---------------------------------------------------------------------------
CSS = """
:root{
  --dash-accent:#305A85;          /* DECORATIVE ONLY — carries no status meaning */
  --dash-red:#DA1A00;             /* s151-D1, on white */
  --dash-green:#137F3C;           /* s155-D1 mirror, on white */
  --dash-ink:#1A1A1A;
  --dash-mute:#545454;
  --dash-rule:#D7D8D6;
  --dash-band:#F3F3F3;
  --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
  --dash-font:"Univers Next for HSBC","Helvetica Neue",Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box;}
body{margin:0;background:#FFFFFF;color:var(--dash-ink);font-family:var(--dash-font);
  -webkit-font-smoothing:antialiased;}
.wrap{max-width:1200px;margin:0 auto;padding:0 var(--s4);}
section{padding:var(--s6) 0;border-top:1px solid var(--dash-rule);}
section:first-of-type{border-top:0;}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dash-accent);display:flex;align-items:center;gap:.5rem;margin:0 0 var(--s3);}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--dash-accent);}
h1{font-size:3.5625rem;line-height:1.04;font-weight:300;margin:0 0 var(--s3);letter-spacing:0;}
h2{font-size:2.125rem;line-height:1.15;font-weight:300;margin:0 0 var(--s3);}
h3{font-size:1.1875rem;line-height:1.2;font-weight:500;margin:0 0 var(--s2);}
p{line-height:1.75;margin:0 0 var(--s2);}
.lede p{font-size:21px;line-height:1.75;max-width:68ch;}
.lede p strong{font-weight:500;}
.meta{font-size:14px;color:var(--dash-mute);line-height:1.6;}
.sourceline{font-size:12px;color:var(--dash-mute);letter-spacing:.04em;margin-top:var(--s3);}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em;}

/* verdict words — the WORD is the signal; colour only repeats it */
.v{font-weight:500;letter-spacing:.06em;text-transform:uppercase;font-size:13px;
  white-space:nowrap;}
.v-pass{color:var(--dash-green);}
.v-fail{color:var(--dash-red);}
.v-debt{color:var(--dash-ink);}
.v-note{color:var(--dash-mute);}

table.strip{width:100%;border-collapse:collapse;}
table.strip th{text-align:left;font-size:12px;font-weight:500;letter-spacing:.12em;
  text-transform:uppercase;color:var(--dash-mute);padding:0 var(--s2) .6rem 0;
  border-bottom:1px solid var(--dash-rule);}
table.strip td{padding:.9rem var(--s2) .9rem 0;border-bottom:1px solid var(--dash-rule);
  vertical-align:top;font-size:15px;line-height:1.5;}
table.strip td.head{max-width:52ch;color:var(--dash-mute);}
table.strip td.gate{font-weight:500;}

.plates{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--dash-rule);}
.plate{padding:var(--s4) var(--s4) var(--s4) 0;}
.plate + .plate{border-left:1px solid var(--dash-rule);padding-left:var(--s4);}
.plate h3 .n{font-weight:300;font-size:2.125rem;display:block;line-height:1;margin-bottom:.4rem;}
ul.items{list-style:none;margin:0;padding:0;}
ul.items li{padding:var(--s2) 0;border-bottom:1px solid var(--dash-rule);}
ul.items li .id{font-size:12px;letter-spacing:.1em;color:var(--dash-mute);}
ul.items li .ti{font-size:16px;font-weight:500;line-height:1.4;display:block;margin:.2rem 0;}
ul.items li .cw{font-size:14px;color:var(--dash-mute);line-height:1.55;}

/* kanban — a GLANCE surface. Columns are DERIVED (state × condition); the derivation
   rule is printed in every column head, because a column nobody can trace is a claim. */
.kb{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:1px solid var(--dash-rule);}
.kb .col{padding:var(--s3) var(--s3) var(--s3) 0;min-width:0;}
.kb .col + .col{border-left:1px solid var(--dash-rule);padding-left:var(--s3);}
.kb .colhead{margin:0 0 var(--s3);}
.kb .colhead .n{display:block;font-size:2.125rem;font-weight:300;line-height:1;margin-bottom:.3rem;}
.kb .colhead .nm{display:block;font-size:15px;font-weight:500;line-height:1.25;letter-spacing:.02em;}
.kb .colhead .rule{display:block;font-size:12px;color:var(--dash-mute);line-height:1.5;margin-top:.35rem;}
.kb .cards{list-style:none;margin:0;padding:0;}
.kb .card{border:1px solid var(--dash-rule);padding:.65rem .7rem;margin:0 0 .5rem;background:#FFFFFF;}
.kb .card .cid{font-size:12px;letter-spacing:.1em;color:var(--dash-mute);display:block;}
.kb .card .ct{font-size:15px;font-weight:500;line-height:1.35;display:block;margin:.25rem 0 .35rem;
  overflow-wrap:anywhere;}
.kb .card .own{font-size:11px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid currentColor;padding:.1rem .35rem;display:inline-block;}
.kb .card .own-dave{color:var(--dash-ink);}
.kb .card .own-claude{color:var(--dash-mute);}
.kb .card .inf{font-size:11px;letter-spacing:.06em;color:var(--dash-mute);margin-left:.4rem;}
.kb .col-blocked .colhead .nm{color:var(--dash-red);}
.kb .col-done .colhead .nm{color:var(--dash-green);}
.kb .col-blocked .card{border-left:3px solid var(--dash-red);}
.kb .col-done .card{border-left:3px solid var(--dash-green);}
.kb .empty{font-size:14px;color:var(--dash-mute);}

/* priority — a PROPOSAL. The word PROPOSAL is on every surface that shows a score. */
.kb .card .pri{display:block;font-size:12px;letter-spacing:.06em;color:var(--dash-mute);
  margin:.35rem 0 .3rem;line-height:1.4;}
.kb .card .pri b{font-weight:500;color:var(--dash-ink);}
.kb .card .lowconf{font-weight:500;color:var(--dash-ink);}
.kb .card .ovr{font-weight:500;color:var(--dash-ink);letter-spacing:.08em;}
ul.items li .pri{font-size:13px;color:var(--dash-mute);display:block;margin-bottom:.15rem;}
ul.items li .pri b{font-weight:500;color:var(--dash-ink);}
table.pri{width:100%;border-collapse:collapse;}
table.pri th{text-align:left;font-size:12px;font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:var(--dash-mute);padding:0 .8rem .6rem 0;
  border-bottom:1px solid var(--dash-rule);vertical-align:bottom;}
table.pri th.num,table.pri td.num{text-align:right;padding-right:.8rem;}
table.pri td{padding:.75rem .8rem .75rem 0;border-bottom:1px solid var(--dash-rule);
  font-size:15px;line-height:1.5;vertical-align:top;}
table.pri td.rk{font-size:1.1875rem;font-weight:300;}
table.pri td.ti{max-width:46ch;}
table.pri td.ti .id{font-size:12px;letter-spacing:.1em;color:var(--dash-mute);
  display:block;margin-bottom:.15rem;}
table.pri td.flag{font-size:12px;color:var(--dash-mute);max-width:38ch;line-height:1.5;}
table.pri td.sc{font-weight:500;white-space:nowrap;}
table.pri tr.has-ovr td{background:var(--dash-band);}
/* narrow: the six per-criterion sub-scores drop out. The SCORE and the LOW-CONFIDENCE
   flag never drop — a number without its confidence is the thing we refuse to print.
   The weights table above still declares every criterion at every width. */
@media (max-width:900px){
  table.pri th.subcol,table.pri td.subcol,
  table.pri th.ownc,table.pri td.ownc{display:none;}
  table.pri{table-layout:fixed;}
  table.pri td.ti{max-width:none;}
  table.pri td,table.pri th{padding-right:.5rem;}
  table.pri th.num:first-child,table.pri td.rk{width:2.2rem;}
  table.pri td.flag{max-width:none;}
}
.wtable{width:100%;border-collapse:collapse;margin-bottom:var(--s3);}
.wtable th{text-align:left;font-size:12px;font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:var(--dash-mute);padding:0 .8rem .6rem 0;
  border-bottom:1px solid var(--dash-rule);}
.wtable td{padding:.7rem .8rem;border-bottom:1px solid var(--dash-rule);font-size:15px;
  line-height:1.55;vertical-align:top;padding-left:0;}
.wtable td.w{font-size:1.1875rem;font-weight:300;white-space:nowrap;}
.wtable td.src{color:var(--dash-mute);font-size:13px;max-width:44ch;}

.band{background:var(--dash-band);}
.band .wrap{padding-top:var(--s6);padding-bottom:var(--s6);}
ol.fails{margin:0;padding-left:1.4rem;}
ol.fails li{font-size:15px;line-height:1.6;padding:.45rem 0;max-width:100ch;}

.future{display:grid;grid-template-columns:1fr;gap:0;}
.future .row{display:grid;grid-template-columns:9rem 1fr;gap:var(--s3);
  padding:var(--s2) 0;border-bottom:1px solid var(--dash-rule);align-items:baseline;}
.future .row .st{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--dash-mute);}
.future .row .ti{font-size:16px;line-height:1.5;max-width:80ch;}

@media (max-width:1000px){
  .kb{grid-template-columns:1fr 1fr;}
  .kb .col{border-left:0;padding-left:0;padding-right:var(--s3);}
  .kb .col:nth-child(2n){border-left:1px solid var(--dash-rule);padding-left:var(--s3);}
  .kb .col:nth-child(n+3){border-top:1px solid var(--dash-rule);}
}
@media (max-width:820px){
  h1{font-size:2.6875rem;}
  .kb{grid-template-columns:1fr;}
  .kb .col,.kb .col:nth-child(2n){border-left:0;padding-left:0;}
  .kb .col + .col{border-top:1px solid var(--dash-rule);}
  .plates{grid-template-columns:1fr;}
  .plate + .plate{border-left:0;border-top:1px solid var(--dash-rule);padding-left:0;}
  .future .row{grid-template-columns:1fr;gap:.2rem;}
}
@media print{ body{color:#000;} }
"""


def verdict(rc, name):
    if name == "type-composites":
        return ("DEBT", "v-debt")
    if rc == 0:
        return ("PASS", "v-pass")
    if rc in (124, 125):
        return ("NO VERDICT", "v-note")
    return ("FAIL", "v-fail")


def pri_badge(iid, prio):
    """The card/plate badge. PROPOSAL unless Dave has overruled — and an overrule says so
    in his words, not in a colour."""
    r = prio["by_id"].get(iid)
    if not r:
        return ""
    if r["override"] is not None:
        return ('<span class="pri"><span class="ovr">DAVE OVERRULED &rarr; %d</span></span>'
                % r["override"])
    flag = (' &middot; <span class="lowconf">LOW CONFIDENCE</span>, %d input(s) missing'
            % len(r["missing"])) if r["missing"] else ""
    return ('<span class="pri">PROPOSAL &middot; rank <b>%d</b> &middot; score <b>%d</b>/100%s</span>'
            % (r["rank"], r["score"], flag))


def render(state, rulings, gaps, session, ratchets, tdebt, future, gates, wave, kanban,
           prio, cov):
    o = []
    a = o.append
    dave = sort_by_priority([i for i in state["open"] if i.get("owner") == "dave"], prio)
    mine = sort_by_priority([i for i in state["open"] if i.get("owner") == "claude"], prio)
    unconditioned = [i for i in state["open"] if i.get("condition") == "UNCONDITIONED"]
    n_fail = sum(1 for g in gates if g["rc"] != 0 and g["name"] != "type-composites")
    n_pass = sum(1 for g in gates if g["rc"] == 0)

    a("<!DOCTYPE html>")
    a('<html lang="en" data-apollo-theme="mono">')
    a("<head>")
    a('<meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1">')
    a("<title>Mission control — Apollo progress dashboard</title>")
    a("<!--")
    a("  GENERATED by knowledge/gen_dashboard.py FROM THE STORES. DO NOT HAND-EDIT.")
    a("  If a number here is wrong, the STORE is wrong: fix the store, regenerate.")
    a("  `python3 knowledge/gen_dashboard.py --check` is the build gate.")
    a("-->")
    a('<link rel="stylesheet" href="../knowledge/canon/type.css">')
    a('<link rel="stylesheet" href="../knowledge/canon/canon.css">')
    a("<style>%s</style>" % CSS)
    a("</head>")
    a('<body data-theme="light">')

    # ---- masthead + exec summary -----------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">Apollo · mission control · session #%s</p>' % E(session["session"]))
    a("<h1>Where the work stands</h1>")
    a('<div class="lede">')
    a("<p><strong>%d things are open.</strong> %d of them are yours to rule, %d are mine to build. "
      "%d of the open items still have no checkable close condition — they are the frozen legacy set, "
      "and that set may only shrink." % (len(state["open"]), len(dave), len(mine), len(unconditioned)))
    if gates:
        a("<p>%d of %d gates were run just now and passed; %s. "
          "The type-composite gate is not counted as a pass or a fail — it reports declared debt, "
          "which is a third thing." % (n_pass, len(gates),
                                       ("%d failed" % n_fail) if n_fail else "none failed"))
    if gaps["measured"]:
        a("<p>The provenance gate is the one that is red, and it is red on purpose: %d checks fail "
          "across %d rulings that are missing a <code>governs</code>, <code>evidence</code> or "
          "<code>status</code> value. <strong>Those values are yours and nobody else&rsquo;s</strong> — "
          "authoring them would be inventing provenance, so this page lists them and stops."
          % (len(gaps["fails"]), len(gaps["ids"])))
    if tdebt["delta"] is not None and tdebt["delta"] > 0:
        a("<p><span class=\"v v-fail\">Ratchet breach</span> — the type-composite count measures "
          "<strong>%d</strong> against a declared, shrink-only baseline of <strong>%d</strong>. "
          "That is %d more than the ratchet permits. Measured here; not fixed here."
          % (tdebt["count"], tdebt["baseline"], tdebt["delta"]))
    a("<p>The order everything is shown in is a <strong>PROPOSAL</strong> — a score I compute "
      "from the store at build time, out of six weighted criteria printed in full below. "
      "It is not a ruling and it does not persist: you overrule it by writing a "
      "<code>priority_override</code> rank on the item, and an overruled item says "
      "<strong>DAVE OVERRULED</strong> wherever it appears. %s"
      % ("<strong>No item carries an override yet</strong> — the field is absent everywhere, "
         "because a priority I write into the store and then read back is not your judgement, "
         "it is mine wearing your name.</p>" if not prio["n_overrides"] else
         "%d item(s) currently carry your override.</p>" % prio["n_overrides"]))
    a("<p><span class=\"v v-fail\">Flagged problem</span> — <strong>%d of %d items carry any "
      "<code>links</code></strong> (%.0f%%). The dependency graph the score's heaviest "
      "criterion (Unlock, weight %.2f) needs <em>does not exist in the data</em>, so every "
      "score on this page is flagged LOW CONFIDENCE and the unlock column reads zero for "
      "everything. This is MEASURED and QUEUED, not repaired: backfilling links would mean "
      "inventing the dependency graph and then scoring against my own invention. It is "
      "yours, and it is %s work.</p>"
      % (cov["with_links"], cov["total"], cov["pct"], CRITERIA[0][2], DEADLINE_SET))
    a("<p>Everything on this page was read out of the stores or measured by running the thing. "
      "Nothing is asserted from memory.</p>")
    a("</div>")
    a('<p class="sourceline">SOURCES · knowledge/_state.json · knowledge/_rulings.json · '
      'live gate runs · _CHAIN.md · _LIVE-STATE.md (last refreshed %s) · _FUTURE-STATE.md</p>'
      % E(session["refreshed"]))
    a("</div></section>")

    # ---- gates health strip ----------------------------------------------
    if gates:
        a('<section><div class="wrap">')
        a('<p class="label">Gates health — measured at generation, never asserted</p>')
        a("<h2>Eight gates, run just now</h2>")
        a('<table class="strip"><thead><tr>'
          "<th>Gate</th><th>Verdict</th><th>rc</th><th>What it proves</th><th>Its own last line</th>"
          "</tr></thead><tbody>")
        for g in gates:
            word, cls = verdict(g["rc"], g["name"])
            a("<tr><td class=\"gate\">%s</td><td><span class=\"v %s\">%s</span></td>"
              "<td>%d</td><td class=\"head\">%s</td><td class=\"head\">%s</td></tr>"
              % (E(g["name"]), cls, word, g["rc"], E(g["why"]), E(g["headline"][:180])))
        a("</tbody></table>")
        a('<p class="sourceline">Each row is a real subprocess run from this generator '
          '(read-only invocations only). <code>--ratchet</code> is deliberately NOT run: it writes '
          'a store, and a reporting surface must not repair what it reports.</p>')
        a("</div></section>")

    # ---- progress toward atomic ------------------------------------------
    a('<section class="band"><div class="wrap">')
    a('<p class="label">Progress toward atomic</p>')
    a("<h2>The counts that move</h2>")
    a('<div class="cn-stat-card"><div class="board" style="max-width:none">')

    def card(label, value, note):
        a('<div class="stat-card" role="group" aria-label="%s">' % E(label))
        a('<p class="lbl16 t-cm-caption">%s</p>' % E(label))
        a('<span class="amt t-cm-figure-3"><span>%s</span></span>' % E(value))
        a('<span class="delta"><span class="t-cm-figure-6">%s</span></span>' % E(note))
        a("</div>")

    card("Rulings recorded", rulings["n"], "tail %s" % rulings["tail"]["id"])
    card("Rulings with a provenance gap", len(gaps["ids"]) if gaps["measured"] else "—",
         "Dave's to supply")
    card("Open items", len(state["open"]), "%d yours · %d mine" % (len(dave), len(mine)))
    card("Open with no close condition", len(unconditioned), "frozen legacy set, shrink-only")
    card("Items carrying links", "%d/%d" % (cov["with_links"], cov["total"]),
         "%.0f%% — the dependency graph, MEASURED" % cov["pct"])
    card("Items with your override", prio["n_overrides"],
         "yours to set; none authored here")
    card("Metas carrying binds", "%d/%d" % (ratchets["binds"]["floor"], ratchets["binds"]["corpus"]),
         "floor may only rise")
    if tdebt["count"] is not None:
        card("Type-composite debt", tdebt["count"],
             "baseline %d · delta %+d" % (tdebt["baseline"], tdebt["delta"]))
    if wave:
        card("The s142-D1 bind wave", "114/114", "claimed by %s, not measured here" % wave["id"])
    a("</div></div>")
    a('<p class="sourceline">Mono <code>.cn-stat-card</code> from knowledge/canon/canon.css — the '
      'gated component, unmodified. SOURCES · _rulings.json · _state.json · _binds-ratchet.json · '
      '_type_ratchet.json · the live _governs run.</p>')
    a("</div></section>")

    # ---- priority PROPOSAL ------------------------------------------------
    live_items = [i for i in state["items"] if i["id"] in prio["by_id"]]
    a('<section><div class="wrap">')
    a('<p class="label">Priority &mdash; a PROPOSAL, not a ruling</p>')
    a("<h2>My proposed order, and the weights it came from</h2>")
    a("<p class=\"meta\">You ruled that I generate the priorities and you overrule them. This is "
      "the generated half. It is <strong>computed at build time from the store</strong>, never "
      "written back into it, so it cannot rot and it cannot quietly become a decision. Six "
      "criteria, each scored 0&ndash;1, combined with the declared weights below into a score "
      "out of 100. <strong>The weights themselves are a proposal too</strong> &mdash; change any "
      "number in the table and the order changes; nothing about them is ratified.</p>")
    a('<table class="wtable"><thead><tr><th>Criterion</th><th>Weight</th>'
      "<th>What it measures</th><th>Where the input comes from</th></tr></thead><tbody>")
    for key, name, w, desc, src in CRITERIA:
        a("<tr><td><strong>%s</strong></td><td class=\"w\">%.2f</td><td>%s</td>"
          "<td class=\"src\">%s</td></tr>" % (E(name), w, E(desc), src))
    a("<tr><td><strong>TOTAL</strong></td><td class=\"w\">%.2f</td><td colspan=\"2\" "
      "class=\"src\">Score = 100 &times; &Sigma;(weight &times; criterion). Deadline set: "
      "<strong>%s</strong>.</td></tr>" % (WEIGHTS_SUM, E(DEADLINE_SET)))
    a("</tbody></table>")
    # ⚠ MEASURED, NOT TYPED. This paragraph used to assert "there is no effort field, no
    # deadline field" — true when written, and it would have gone quietly false the moment
    # the fields landed [[premise-ages-faster-than-rule]]. It now counts them.
    _all = state["items"]
    _n_eff = sum(1 for i in _all if i.get("effort") in EFFORT_SCORE)
    _n_dl = sum(1 for i in _all if _deadline_score(i.get("deadline"), DEADLINE_SET) is not None)
    a("<p class=\"meta\"><strong>Some inputs are proxies, and the table says which.</strong> "
      "<code>opened</code>, <code>condition</code> and <code>owner</code> are real fields. "
      "<code>effort</code> and <code>deadline</code> are OPTIONAL real fields that <em>replace</em> "
      "their proxy when present &mdash; today they are present on <strong>%d</strong> and "
      "<strong>%d</strong> of %d items respectively, so the proxy is what runs everywhere else. "
      "<code>links</code> is empty on %d of %d items. Where an input was missing, the score "
      "carries a LOW-CONFIDENCE flag naming it. A clean-looking number from thin data is the one "
      "thing this page must never print.</p>" % (_n_eff, _n_dl, cov["total"],
                                                 cov["total"] - cov["with_links"],
                                                 cov["total"]))
    _sc = sorted(r["score"] for r in prio["by_id"].values())
    if _sc:
        a("<p class=\"meta\"><strong>How much this ranking actually separates the work: not much, "
          "and here is the number.</strong> The %d scored items span <strong>%d to %d</strong> "
          "out of 100 across <strong>%d distinct values</strong>, so the gap between rank 1 and "
          "rank %d is %d points. That is what a ranking looks like when its heaviest criterion "
          "has no data: the order below is a tie-break, not a verdict. It gets sharper the "
          "moment <code>links</code> exists.</p>"
          % (len(_sc), _sc[0], _sc[-1], len(set(_sc)), len(_sc), _sc[-1] - _sc[0]))
    seen_why, legend = set(), []
    for r in prio["by_id"].values():
        for short, why in r["missing"]:
            if short not in seen_why:
                seen_why.add(short)
                legend.append((short, why))
    if legend:
        a("<p class=\"meta\"><strong>What the missing-input words in the last column mean.</strong> "
          + " ".join("<strong>%s</strong> — %s." % (E(s), E(w)) for s, w in legend) + "</p>")
    a('<table class="pri"><thead><tr><th class="num">#</th><th>Item</th><th class="ownc">Owner</th>'
      '<th class="num">Score</th>')
    for _k, name, w, _d, _s in CRITERIA:
        a('<th class="num subcol">%s<br>%.2f</th>' % (E(name), w))
    a("<th>Confidence</th></tr></thead><tbody>")
    for iid in prio["ranked"]:
        it = next(i for i in live_items if i["id"] == iid)
        r = prio["by_id"][iid]
        t, _ = short_title(it["title"], 72)
        a('<tr class="%s">' % ("has-ovr" if r["override"] is not None else ""))
        a('<td class="num rk">%d</td>' % r["rank"])
        a('<td class="ti"><span class="id">%s</span> %s</td>' % (E(iid), E(t)))
        a('<td class="ownc">%s</td>' % ("DAVE" if it.get("owner") == "dave" else "CLAUDE"))
        if r["override"] is not None:
            a('<td class="num sc">DAVE OVERRULED &rarr; %d</td>' % r["override"])
        else:
            a('<td class="num sc">%d <span class="v v-note">PROPOSAL</span></td>' % r["score"])
        for k, _n, _w, _d, _s in CRITERIA:
            a('<td class="num subcol">%.2f</td>' % r["sub"][k])
        a('<td class="flag">%s</td>' % (
            ("<strong>LOW CONFIDENCE</strong><br>missing: "
             + E(" · ".join(m[0] for m in r["missing"])))
            if r["missing"] else "all inputs present"))
        a("</tr>")
    a("</tbody></table>")
    a('<p class="sourceline">SOURCE · knowledge/_state.json, every item where state is not done '
      'or dropped, scored by <code>gen_dashboard.py::score_item()</code> at generation. '
      'The override channel is the OPTIONAL <code>priority_override</code> integer (1 = first, '
      'range 1–999), validated when present by <code>knowledge/_state.py</code> and wired into '
      '_build_all.py as a routed step. ⛔ No override value has been authored by me, here or in '
      'the store.</p>')
    a("</div></section>")

    # ---- links coverage — REPORTED, queued, never repaired ----------------
    a('<section class="band"><div class="wrap">')
    a('<p class="label">Flagged problem &mdash; the dependency graph does not exist</p>')
    a("<h2>%d of %d items carry links &mdash; %.0f%%</h2>"
      % (cov["with_links"], cov["total"], cov["pct"]))
    a("<p>Among the %d live items it is <strong>%d</strong>. <code>links</code> is a required "
      "field, so it is present on every item &mdash; and empty on almost all of them. The "
      "consequence is concrete and it is on this page: the heaviest criterion in the score "
      "above (Unlock, weight %.2f) has nothing to read, contributes zero to every item, and "
      "the remaining %.2f of weight is doing all the work of ranking your backlog.</p>"
      % (cov["live_total"], cov["live_with_links"], CRITERIA[0][2], 1 - CRITERIA[0][2]))
    a("<p><strong>Queued as your work for the %s set, not repaired here.</strong> I could "
      "populate <code>links</code> by guessing which item blocks which from the prose &mdash; "
      "and then the score would rank your backlog against a dependency graph I invented and "
      "you never saw. That is a closed loop with no reader in it. The number is reported; the "
      "backfill waits for you.</p>" % E(DEADLINE_SET))
    a('<p class="sourceline">SOURCE · knowledge/_state.json, counted at generation. This panel '
      'moves on its own the moment links are written — it is a measurement, not a note.</p>')
    a("</div></section>")

    # ---- kanban (quick visual reference) ---------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">Board — quick visual reference</p>')
    a("<h2>All %d items, four columns</h2>" % len(state["items"]))
    a('<p class="meta"><strong>The columns are DERIVED, not stored.</strong> '
      '<code>_state.json</code> has no <code>status</code>, <code>lane</code>, '
      '<code>phase</code> or <code>priority</code> field — the only lifecycle axes that '
      'exist in the data are <code>state</code> (open / blocked / done) and '
      '<code>condition</code> (UNCONDITIONED / stated, i.e. whether a '
      '<code>closes_when</code> is set). Each column head prints the exact rule that put '
      'items in it, so you can check the derivation rather than trust it. Owner is the '
      'store&rsquo;s <code>owner</code>, written as a WORD; where the store marks it '
      'inferred the card says <em>inferred</em>. <strong>Cards are ordered by the proposed '
      'priority score</strong> (an overruled card sits at the top of its column); the Done '
      'column stays in id order, because a finished thing has no priority.</p>')
    a('<div class="kb">')
    for c in kanban:
        a('<div class="col col-%s">' % E(c["key"]))
        a('<div class="colhead"><span class="n">%d</span><span class="nm">%s</span>'
          '<span class="rule">%s<br>%s</span></div>'
          % (len(c["items"]), E(c["name"]), E(c["rule"]), E(c["note"])))
        if not c["items"]:
            a('<p class="empty">None.</p>')
        else:
            a('<ul class="cards">')
            for i in c["items"]:
                t, trimmed = short_title(i["title"])
                own = "DAVE" if i.get("owner") == "dave" else "CLAUDE"
                ocls = "own-dave" if i.get("owner") == "dave" else "own-claude"
                inf = '<span class="inf">inferred</span>' if i.get("owner_inferred") else ""
                a('<li class="card"><span class="cid">%s</span>'
                  '<span class="ct" title="%s">%s</span>%s'
                  '<span class="own %s">%s</span>%s</li>'
                  % (E(i["id"]), E(i["title"]), E(t), pri_badge(i["id"], prio),
                     ocls, own, inf))
            a("</ul>")
        a("</div>")
    a("</div>")
    a('<p class="sourceline">SOURCE · knowledge/_state.json, every item, no filter. Titles are '
      'trimmed for the glance only — the full title of every OPEN item is on the two plates '
      'below. The board REPORTS the store; it does not re-classify, re-prioritise or move '
      'anything. Red on the blocked column and green on the done column (s151-D1 / s155-D1, '
      'light mode) repeat the column&rsquo;s own word; no meaning is carried by hue.</p>')
    a("</div></section>")

    # ---- the two plates ---------------------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">The two plates</p>')
    a("<h2>What is on your plate, and what is on mine</h2>")
    a('<p class="meta">Owner comes from <code>_state.json</code>. Where the store marks the owner '
      'as inferred, the item says so — an inference is not a ruling. <strong>Both plates are in '
      'proposed-priority order</strong>, highest score first, with any item you have overruled '
      'lifted to the top of its plate; the badge on each item says which of the two it is.</p>')
    a('<div class="plates">')
    for title, group, who in (("Dave&rsquo;s plate", dave, "DAVE'S"),
                              ("My plate", mine, "MINE")):
        a('<div class="plate">')
        a("<h3><span class=\"n\">%d</span>%s <span class=\"v v-note\">%s</span></h3>"
          % (len(group), title, who))
        a('<ul class="items">')
        for i in group:
            cond = i.get("closes_when") or "NO CLOSE CONDITION — frozen legacy item"
            inf = " · owner inferred" if i.get("owner_inferred") else ""
            a("<li>%s<span class=\"id\">%s%s</span><span class=\"ti\">%s</span>"
              "<span class=\"cw\">Closes when: %s</span></li>"
              % (pri_badge(i["id"], prio), E(i["id"]), E(inf), E(i["title"]), E(cond)))
        a("</ul></div>")
    a("</div>")
    a('<p class="sourceline">SOURCE · knowledge/_state.json (items where state = open).</p>')
    a("</div></section>")

    # ---- provenance gap ---------------------------------------------------
    if gaps["measured"] and gaps["fails"]:
        a('<section class="band"><div class="wrap">')
        a('<p class="label">Yours alone — the provenance gap</p>')
        a("<h2>%d checks, %d rulings, nobody else&rsquo;s to answer</h2>"
          % (len(gaps["fails"]), len(gaps["ids"])))
        a("<p>These are the live words of <code>knowledge/_governs.py --selftest</code>, run by this "
          "generator. Each one wants a <code>governs</code>, <code>evidence</code> or "
          "<code>status</code> value on a ruling in <code>_rulings.json</code>. "
          "<strong>No value has been drafted, guessed, or suggested here</strong> — a provenance "
          "field authored by an agent is a false inscription, which is the failure this gate exists "
          "to catch. Rulings affected: %s.</p>" % E(", ".join(gaps["ids"])))
        a('<ol class="fails">')
        for f in gaps["fails"]:
            a("<li>%s</li>" % E(f))
        a("</ol>")
        a('<p class="sourceline">SOURCE · live run, <code>python3 knowledge/_governs.py '
          '--selftest</code>. The gate could not run at all for five sessions (#158–#163) because '
          '_build_all.py aborted above it — see _LIVE-STATE.md #164.</p>')
        a("</div></section>")

    # ---- future-state lane ------------------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">The forward lane</p>')
    a("<h2>%d things held for later</h2>" % len(future))
    a('<p class="meta">Read straight out of <code>_FUTURE-STATE.md</code>. Status is the file&rsquo;s '
      'own word. Nothing here has been promoted, re-prioritised or re-worded.</p>')
    a('<div class="future">')
    for f in future:
        a('<div class="row"><span class="st">%s</span><span class="ti">%s</span></div>'
          % (E(f["status"]), E(re.sub(r"[*`]", "", f["title"]))))
    a("</div>")
    a('<p class="sourceline">SOURCE · _FUTURE-STATE.md.</p>')
    a("</div></section>")

    # ---- footer -----------------------------------------------------------
    a('<section><div class="wrap">')
    a('<p class="label">How to read this page</p>')
    a("<p class=\"meta\">Generated by <code>knowledge/gen_dashboard.py</code> from the stores; it is "
      "never hand-edited. <code>--check</code> regenerates and compares, so a stale dashboard fails "
      "the build rather than lying quietly. It carries no timestamp on purpose: its clock is the "
      "session number in <code>_CHAIN.md</code> (#%s) and the measurements themselves.</p>"
      % E(session["session"]))
    a("<p class=\"meta\">Components are Mono, from <code>knowledge/canon/canon.css</code> — nothing "
      "new was invented. Layout follows the swiss-design-system skill. Every verdict is a WORD "
      "first; the two-red law (red #DA1A00) and its green mirror (#137F3C) are applied on white, "
      "light mode only, as redundant confirmation. The blue rules and dashes are decorative and "
      "carry no meaning.</p>")
    a("<p class=\"meta\">This page reports. It does not repair, rule, or promote anything.</p>")
    a("</div></section>")
    a("</body></html>")
    return "\n".join(o) + "\n"


def build(with_gates=True):
    gates = run_gates(with_gates)
    gmap = {g["name"]: g for g in gates}
    state = read_state()
    rulings = read_rulings()
    gaps = provenance_gaps(gmap.get("provenance"))
    ratchets = read_ratchets()
    tdebt = type_debt(gmap.get("type-composites"), ratchets["type"]["baseline"])
    session = read_session()
    if abs(WEIGHTS_SUM - 1.0) > 1e-9:                    # a score out of 100 that isn't
        raise SystemExit("gen_dashboard REFUSING: CRITERIA weights sum to %r, not 1.0 — a "
                         "score presented as /100 must be a weighted mean, not an arbitrary "
                         "total." % WEIGHTS_SUM)
    prio = priorities(state["items"], session["session"])
    cov = links_coverage(state["items"])
    return render(state, rulings, gaps, session, ratchets, tdebt,
                  read_future_state(), gates, wave_claim(rulings["rulings"]),
                  kanban_columns(state["items"], prio), prio, cov)


def main(argv):
    check = "--check" in argv
    with_gates = "--no-gates" not in argv
    html = build(with_gates)
    if check:
        if not os.path.exists(OUT):
            print("gen_dashboard --check FAIL — %s does not exist." % os.path.relpath(OUT, ROOT))
            return 1
        cur = _read(OUT)
        if cur != html:
            print("gen_dashboard --check FAIL — dashboard/index.html is OUT OF SYNC with the "
                  "stores or with a live gate result. Re-run `python3 knowledge/gen_dashboard.py`.")
            return 1
        print("gen_dashboard --check OK — dashboard/index.html in sync.")
        return 0
    os.makedirs(OUTD, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("gen_dashboard — wrote %s (%d bytes)." % (os.path.relpath(OUT, ROOT), len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
