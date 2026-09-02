#!/usr/bin/env python3
"""#237-T — the 21 OPEN tensions, four fields each, FLOATED.

Two things here are DERIVED and printed; two are AUTHORED and marked `proposed`.

DERIVED
  RULE K  (knowable by the factory): the mediating_variable text is matched against a
          keyword map of the grill's six standard questions. A match is DIRECT when the
          variable names the slot's own subject, PROXY when the slot only stands in for
          it (Q3 "compact ... for people who live in this all day" proxies task frequency
          and user expertise), STANDING-RULE when the variable needs no designer input at
          all because it is a property of the artefact or of the pipeline, and NONE when
          nothing in the six reaches it.
  RULE D  (disposition): three-way, applied uniformly.
          DEFAULT+DECLARE      - a conservative standing answer exists and a wrong answer
                                 is recoverable in the edit pass. No question, ever.
          DEFAULT+CONDITIONAL  - same, but a NAMED trigger drawn from the six answers
                                 fires one question. Does NOT grow the standing grill.
          ASK-AT-GRILL         - no defensible conservative default. Grows the grill by 1.
          The headline number is the count of ASK-AT-GRILL.

AUTHORED (marked `proposed`, nothing is ruled)
  factory_default_proposed - this lane's words for R1's how_it_resolves, conservative side.
  ask_when / question      - the close condition and the designer-facing line.
"""
import json, os, re

REPO = "/sessions/dreamy-relaxed-noether/mnt/UX-design"
ASSETS = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-237-T-tensions-schema")
sort = json.load(open(os.path.join(ASSETS, "tension-sort.json")))
rows = {r["id"]: r for r in sort["rows"]}

# --- RULE K: the grill's six, as keyword probes over the mediating variable -------------
SLOTS = {
    "Q1 theme":       r"theme|corner|radius",
    "Q2 mode":        r"\blight\b|\bdark\b",
    "Q3 density/width": r"densit|width|device|pointer|screen|expertise|frequency|daily",
    "Q4 brand":       r"brand|palette|logo|typeface|mandate",
    "Q5 data":        r"\bdata\b|content|figures|real ",
    "Q6 fixed/off-limits": r"legal|regulat|accessib|contrast|compliance|lawful|consent",
}
# variables that need no designer input: they are properties of the artefact or pipeline
STANDING = {
    "tn-03": "object class of the interaction (direct manipulation vs delegated computation) — the same split s116-D1 makes",
    "tn-04": "which skill is running: evaluating (check-against-design-system) or shipping (generate-from-canon)",
    "tn-05": "pipeline layer: input surface vs persistence boundary",
    "tn-06": "build sequencing — polish is the last pass by construction",
    "tn-09": "whether the progress value is a real measurement or a minted one",
    "tn-10": "pattern choice: in-place signifier vs first-run tour",
    "tn-12": "whether a removed element has a named destination in the used/missing note",
    "tn-14": "citation hygiene — which number the brain is allowed to quote",
    "tn-23": "acknowledgement vs celebration: a property of the event, not of the client",
    "tn-24": "route count on the generated screen",
    "tn-28": "whether the page has heading structure and link labels — mechanically checkable",
    "tn-30": "the licence field on the source node (s237-D4 routes pointer-only families)",
}

AUTHORED = {
 "tn-01": ("Converge on mechanism, diverge on signal: standard placement and behaviour, exactly one element carrying the brand moment per view.",
           "Q4 names a brand mandate that changes a MECHANISM (placement, control behaviour), not just a signal",
           "Your brand asks for a non-standard control here — may we keep standard behaviour and carry the brand in the signal instead?",
           "DEFAULT+CONDITIONAL"),
 "tn-02": ("Nothing is removed without a named destination; progressive disclosure only where Q3 density is comfortable, never where it is compact.",
           "never — Q3 already carries it",
           "-",
           "DEFAULT+DECLARE"),
 "tn-03": ("Acknowledge every action immediately and quietly; show the work only where the system is computing on the user's behalf and the wait is real.",
           "never — the component contract says which kind of operation it is",
           "-",
           "DEFAULT+DECLARE"),
 "tn-04": ("A beauty pass never stands in for the mechanical rubric; when evaluating, the look is a confound to control, not a score.",
           "never — the running skill says which mode this is",
           "-",
           "DEFAULT+DECLARE"),
 "tn-05": ("Accept and normalise at the input surface, validate strictly at the boundary, and SHOW the normalisation. Never silently accept ambiguity.",
           "never — a behaviour rule, homed at #235's behaviour address",
           "-",
           "DEFAULT+DECLARE"),
 "tn-06": ("Polish is allocated to the last pass, never the first; a delightful ending on an unfinished journey is refused.",
           "never — build sequencing",
           "-",
           "DEFAULT+DECLARE"),
 "tn-08": ("Nothing blocks. Status accretes in a place the user chooses to look; only an irreversible or time-critical event may interrupt.",
           "the brief or the data names an irreversible or time-critical event AND the screen carries a notification surface",
           "Which of these events must stop someone mid-task — and which can wait until they look?",
           "DEFAULT+CONDITIONAL"),
 "tn-09": ("Progress shows real progress toward the user's own goal. A minted or endowed head start is refused, not offered as an option.",
           "never — a refusal default; the artefact either measures progress or fabricates it",
           "-",
           "DEFAULT+DECLARE"),
 "tn-10": ("No first-run tour. Guidance sits in place, at the moment of need, and exploration is recoverable.",
           "never — a pattern default",
           "-",
           "DEFAULT+DECLARE"),
 "tn-11": ("Rank by expected cost, not frequency: a rare case with an expensive consequence outranks a common one.",
           "Q6 was SKIPPED and the surface handles money, eligibility, health or identity",
           "You skipped the fixed/off-limits question and this screen handles money — is there a regulatory requirement it has to meet?",
           "DEFAULT+CONDITIONAL"),
 "tn-12": ("Every removed element carries a named destination in the used/missing note. 'Simplified' with no destination is a defect.",
           "never — checkable on the artefact",
           "-",
           "DEFAULT+DECLARE"),
 "tn-13": ("A curated set with the full set one action away; the curation is never described as settled science.",
           "never — Q3 density proxies the expertise moderator",
           "-",
           "DEFAULT+DECLARE"),
 "tn-14": ("Group by chunking and justify counts by scanning cost. Neither 7±2 nor 4 is quoted as a limit.",
           "never — a citation rule about what the brain may say",
           "-",
           "DEFAULT+DECLARE"),
 "tn-18": ("Show what the current step needs; everything else stays reachable without recall. The residual is a flagged observation, never a score.",
           "never — reported through the inferential half of the rubric (s234-D6)",
           "-",
           "DEFAULT+DECLARE"),
 "tn-21": ("Rank encodings by accuracy first. If a brand rule overrides the ranking, the accuracy cost is recorded as a decision.",
           "Q4 names a chart style that lowers the encoding rank (donut, 3-D, area for comparison)",
           "Your brand chart style reads less accurately than the plain one — is this for deciding, or for communicating?",
           "DEFAULT+CONDITIONAL"),
 "tn-22": ("Spacing and keylines never assert different groups; the keyline hugs the module (s217-D8) rather than sitting centred in the gutter.",
           "never — already enacted in the bento canon",
           "-",
           "DEFAULT+DECLARE"),
 "tn-23": ("Acknowledgement is instant, quiet and always. Celebration is proportional and rare. The two are never conflated.",
           "never — a property of the event",
           "-",
           "DEFAULT+DECLARE"),
 "tn-24": ("Multiple entries, one model. A second route that behaves differently is refused rather than shipped.",
           "never — checkable on the artefact",
           "-",
           "DEFAULT+DECLARE"),
 "tn-26": ("Before anything is removed, the build records what the user must now hold in their head; task state stays visible.",
           "never — a build-time check on the removal",
           "-",
           "DEFAULT+DECLARE"),
 "tn-28": ("An F-pattern reading is treated as a diagnostic that scent and structure are missing, never as a layout to design toward.",
           "never — structure is mechanically checkable",
           "-",
           "DEFAULT+DECLARE"),
 "tn-30": ("The generator refuses to emit text from a no-derivatives or proprietary source; those families are pointers with an access note.",
           "never — s237-D4 already routes pointer-only families",
           "-",
           "DEFAULT+DECLARE"),
}

out = []
for tid, r in rows.items():
    if r["bucket"] != "open":
        continue
    mv = r["mediating_variable"]
    hits = [name for name, pat in SLOTS.items() if re.search(pat, mv, re.I)]
    if tid in STANDING:
        knowable, how = "YES", "STANDING-RULE: " + STANDING[tid]
    elif hits:
        knowable, how = "YES", "GRILL " + " + ".join(hits)
    else:
        knowable, how = "NO", "no slot in the six reaches it"
    d, aw, q, disp = AUTHORED[tid]
    out.append({
        "id": tid, "mediating_variable": mv,
        "factory_default_proposed": d, "knowable_by_factory": knowable,
        "knowable_how": how, "grill_slots_matched": hits,
        "ask_when": aw, "question_proposed": q, "disposition": disp,
        "register": "FLOATED — proposed, never ruled",
    })
out.sort(key=lambda x: x["id"])

from collections import Counter
c = Counter(o["disposition"] for o in out)
print("RULE K matched slots per open tension (DERIVED):")
for o in out:
    print(f"  {o['id']}  knowable={o['knowable_by_factory']:3s}  {o['knowable_how'][:78]}")
print()
print("RULE D dispositions (DERIVED from the two-clause test):")
for k, v in sorted(c.items()):
    print(f"  {k:20s} {v:2d}   {', '.join(o['id'] for o in out if o['disposition']==k)}")
print()
print(f"HEADLINE  of {len(out)} open tensions:  ASK-AT-GRILL {c.get('ASK-AT-GRILL',0)}"
      f"  ·  DEFAULT+CONDITIONAL {c.get('DEFAULT+CONDITIONAL',0)}"
      f"  ·  DEFAULT+DECLARE {c.get('DEFAULT+DECLARE',0)}")
print(f"STANDING GRILL GROWS BY: {c.get('ASK-AT-GRILL',0)} question(s).")
print(f"DECLARATION GROWS BY: {c.get('DEFAULT+DECLARE',0)+c.get('DEFAULT+CONDITIONAL',0)} standing default lines.")
nk = [o['id'] for o in out if o['knowable_by_factory'] == 'NO']
print(f"NOT reachable by the six at all: {len(nk)} {nk}")

json.dump({"$description": "#237-T open-tension table. RULE K and RULE D are printed in "
                           "_derive_open_table.py. Every default is FLOATED (proposed), never ruled.",
           "generated": "2026-09-02", "lane": "237-T",
           "counts": dict(c), "n_open": len(out), "rows": out},
          open(os.path.join(ASSETS, "open-tensions.json"), "w"), indent=1, ensure_ascii=False)
print("\nWROTE", os.path.join(ASSETS, "open-tensions.json"))
