#!/usr/bin/env python3
"""#238-P — MIGRATE the 30 R1 tension rows into the polarity home, with a receipt.

GENERATION, NOT COPY (s234-D1): `knowledge/brain/polarities.json` and `knowledge/brain/stubs.json`
are DERIVED from the frozen R1 register row-by-row by the rules printed below. The judgement
this migration needs (which link TYPE a former `apollo_touch` value carries; how a side string
splits into parties; what a dangling id resolves to) is declared HERE AS DATA — `LINKS`,
`PARTIES`, `DANGLING` — so the report's migration table and the generated files are printed by
the SAME function and cannot disagree (brief pitfall 8).

Read-only over the R1 assets. Writes into knowledge/brain/ ONLY with --write; a bare run prints
the receipt and the table to stdout and writes nothing.

Rulings governing the shape: s238-D1 (node is the home; N typed parties; typed out-links;
pairwise edges derived), s238-D4 (tension -> polarity: ids `tn-` -> `pl-`), s238-D6 (four link
types; untyped refused), s237-D5 (explainedBy: one-directional, advisory), s237-D9 / s238-D3
(status derived, never typed — so NO status field is written here).

MIGRATION RULES (printed again at run time beside the counts they produced):
  P1 PARTY     each `pr-` id in a side string -> one party {ref, role=<side>}; a parenthetical
               gloss after the id -> `note`, verbatim; a conjunction residual ("… and X", "+ X")
               -> a declared STUB party on the same side; a side with no id at all -> one STUB
               party whose phrase is the side string, verbatim (lane T finding 8).
  P2 DANGLING  two ids resolve to nothing in the register (lane T's probe, reproduced at this
               seat): `pr-info-scent` -> `pr-information-scent` (T finding 7);
               `pr-two-red-law` -> the ruling `s151-D1` as a PARTY (its `says` opens
               "THE TWO-RED LAW, background-keyed, FIRM"); the R1 spelling is kept in `note`.
  L1 RESOLVED  a ruling id cited in `how_it_resolves` with a resolving verb -> `resolvedBy`.
  L2 EXPLAINS  an `apollo_touch` saying the polarity's principle IS the ruling -> `explainedBy`
               (the s237-D5 relation; T finding 2 names tn-01).
  L3 CHALLENGE an `apollo_touch` saying a ruling SHOULD change -> `challengedBy` (T finding 2
               names tn-11, tn-14).
  L4 TOUCHES   a ruling id listed in `apollo_touch` with no verb, or a verb this lane cannot
               settle -> `touches`, the least claim (it never closes an open question); the row
               is marked UNPROVEN in the table wherever a stronger reading exists.
  L5 NO-ID     an `apollo_touch` with no ruling id -> NO link; the words stay at the frozen R1
               row, reachable through `sources`.
  Q  QUOTE     every link carries the <=15-word quote that justifies its type, taken from the
               R1 row's own text (never paraphrased).
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
R1_DIR = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-236-R1-principles-survey")
SRC = os.path.join(R1_DIR, "tensions.json")
SRC_REL = os.path.relpath(SRC, REPO)
REGISTER = os.path.join(R1_DIR, "principle-register.json")
RULINGS = os.path.join(REPO, "knowledge/_rulings.json")
BRAIN = os.path.join(REPO, "knowledge/brain")
SELF_REL = os.path.relpath(os.path.abspath(__file__), REPO)

# ---------------------------------------------------------------------------------------------
# P1 / P2 — parties, declared per row: (ref, role, note). A `st-` ref declares a stub whose
# verbatim phrase is in STUBS. Nothing here is a status and nothing here is a judgement.
# ---------------------------------------------------------------------------------------------
STUBS = {
    "st-honesty": "honesty",
    "st-input-validation-and-security": "input validation and security",
    "st-consistency-of-investment-across-a-journey": "consistency of investment across a journey",
    "st-information-density-on-a-dashboard": "information density on a dashboard",
    "st-onboarding-tours-and-first-run-guidance": "onboarding tours and first-run guidance",
    "st-long-tail-and-regulated-edge-cases": "long-tail and regulated edge cases",
    "st-user-autonomy": "user autonomy",
    "st-brand-palette": "brand palette",
    "st-dense-financial-tables": "dense financial tables",
    "st-four-theme-flexibility": "four-theme flexibility (mono, legacy, console, supercharge)",
    "st-progressive-disclosure": "progressive disclosure",
    "st-brand-led-chart-styling-and-engaging-visuals": "brand-led chart styling and 'engaging' visuals",
    "st-using-heuristic-scores-as-a-quality-rubric": "using heuristic scores as a quality rubric",
    "st-minimal-visual-chrome-and-brand-led-focus-styling": "minimal visual chrome and brand-led focus styling",
    "st-the-generation-chain": "the generation chain (KG = brain, consumers derived)",
}

PARTIES = {
    "tn-01": [("pr-jakobs-law", "side_a", "work like everything else"),
              ("pr-von-restorff", "side_b", "the different thing is remembered")],
    "tn-02": [("pr-hick", "side_a", "fewer choices, faster decision"),
              ("pr-teslers-law", "side_b", "complexity is conserved")],
    "tn-03": [("pr-doherty", "side_a", "under 400 ms"),
              ("pr-labour-illusion", "side_b", "visible work raises perceived value"),
              ("pr-response-limits", "side_c", "0.1 / 1 / 10 s")],
    "tn-04": [("pr-aesthetic-usability", "side_a", "beauty raises perceived usability"),
              ("pr-nng-visibility", "side_b", None),
              ("st-honesty", "side_b", None)],
    "tn-05": [("pr-postels-law", "side_a", "be liberal in what you accept"),
              ("st-input-validation-and-security", "side_b", None)],
    "tn-06": [("pr-peak-end", "side_a", "the peak and the ending dominate memory"),
              ("st-consistency-of-investment-across-a-journey", "side_b", None)],
    "tn-07": [("pr-fitts", "side_a", "big, close targets"),
              ("st-information-density-on-a-dashboard", "side_b", None)],
    "tn-08": [("pr-flow", "side_a", "protect absorbed focus"),
              ("pr-nng-visibility", "side_b", "keep people informed")],
    "tn-09": [("pr-goal-gradient", "side_a", "accelerate near the goal"),
              ("pr-zeigarnik", "side_b", "unfinished tasks stay in mind")],
    "tn-10": [("pr-paradox-active-user", "side_a", "people never read instructions"),
              ("st-onboarding-tours-and-first-run-guidance", "side_b", None)],
    "tn-11": [("pr-pareto", "side_a", "optimise the vital few"),
              ("st-long-tail-and-regulated-edge-cases", "side_b", None)],
    "tn-12": [("pr-occam", "side_a", "fewest assumptions"),
              ("pr-teslers-law", "side_b", "irreducible complexity")],
    "tn-13": [("pr-choice-overload", "side_a", "too many options paralyse"),
              ("st-user-autonomy", "side_b", None),
              ("pr-idp-offer-choice", "side_b", None)],
    "tn-14": [("pr-millers-law-menus", "side_a", "7±2"),
              ("pr-working-memory-4", "side_b", "about four chunks")],
    "tn-15": [("pr-wcag-1-4-3", "side_a", "text contrast minimum"),
              ("st-brand-palette", "side_b", None),
              ("s151-D1", "side_b", "pr-two-red-law")],
    "tn-16": [("pr-wcag-2-5-5", "side_a", "44 px enhanced targets"),
              ("st-dense-financial-tables", "side_b", None),
              ("s116-D1", "side_b", "data marks")],
    "tn-17": [("pr-govuk-consistent-not-uniform", "side_a", None),
              ("st-four-theme-flexibility", "side_b", None)],
    "tn-18": [("pr-nng-recognition", "side_a", "show options"),
              ("pr-nng-minimalist", "side_b", "every element competes")],
    "tn-19": [("pr-dsa25", "side_a", "no manipulative interfaces"),
              ("pr-social-proof", "side_b", None),
              ("pr-goal-gradient", "side_b", None),
              ("pr-loss-aversion", "side_b", None)],
    "tn-20": [("pr-fca-consumer-understanding", "side_a", None),
              ("pr-nng-minimalist", "side_b", None),
              ("st-progressive-disclosure", "side_b", None)],
    "tn-21": [("pr-graphical-perception", "side_a", "position beats angle beats area"),
              ("st-brand-led-chart-styling-and-engaging-visuals", "side_b", None)],
    "tn-22": [("pr-gestalt-common-region", "side_a", "a boundary makes a group"),
              ("pr-gestalt-proximity", "side_b", "nearness makes a group")],
    "tn-23": [("pr-shneiderman-feedback", "side_a", "proportional feedback"),
              ("pr-response-limits", "side_b", "acknowledge within 0.1 s")],
    "tn-24": [("pr-idp-be-consistent", "side_a", None),
              ("pr-idp-offer-choice", "side_b", None)],
    "tn-25": [("pr-anti-preselection", "side_a", "never pre-tick"),
              ("pr-tog-defaults", "side_b", "good defaults help people")],
    "tn-26": [("pr-cognitive-load", "side_a", "reduce extraneous load"),
              ("pr-coga-6", "side_b", "do not rely on memory")],
    "tn-27": [("pr-evaluator-effect", "side_a", "experts disagree"),
              ("st-using-heuristic-scores-as-a-quality-rubric", "side_b", None)],
    "tn-28": [("pr-f-pattern", "side_a", "design for scanning"),
              ("pr-information-scent", "side_b", "people follow the strongest cue")],
    "tn-29": [("pr-wcag-2-4-13", "side_a", "focus appearance"),
              ("st-minimal-visual-chrome-and-brand-led-focus-styling", "side_b", None)],
    "tn-30": [("pr-baymard-guidelines", "side_a", "proprietary evidence"),
              ("st-the-generation-chain", "side_b", None)],
}

# P2 — the dangling ids and what they resolve to (receipt lines printed at run time)
DANGLING = {
    "pr-info-scent": ("pr-information-scent", "principle", "tn-28",
                      "T finding 7: the register holds `pr-information-scent`; near-miss by string"),
    "pr-two-red-law": ("s151-D1", "ruling", "tn-15",
                       "s151-D1 `says` opens \"THE TWO-RED LAW, background-keyed, FIRM\""),
}

# ---------------------------------------------------------------------------------------------
# L1..L5 — links, declared per row: (type, ref, quote, provenance_field, rule, unproven_note)
# ---------------------------------------------------------------------------------------------
LINKS = {
    "tn-01": [("explainedBy", "s151-D1",
               "The law IS a Von Restorff budget with a legal contrast floor attached.",
               "apollo_touch", "L2", None)],
    "tn-02": [("touches", "s217-D5",
               "three types with ruled option sets is exactly this trade, made once",
               "apollo_touch", "L4",
               "T finding 2 reads this as a genuine resolution (resolvedBy); this lane reads "
               "s217-D5 as an INSTANCE of the trade, not the rule for it — `touches` keeps the "
               "question open; Dave's eye")],
    "tn-07": [("resolvedBy", "s116-D1",
               "Split the rule by object class, which Apollo already did: s116-D1 exempts data marks",
               "how_it_resolves", "L1", None),
              ("touches", "s114-D3", "s114-D3/D5 hit-area sweep", "apollo_touch", "L4", None),
              ("touches", "s114-D5", "s114-D3/D5 hit-area sweep", "apollo_touch", "L4", None)],
    "tn-08": [("touches", "s135-D1", "the shell exists; the ROUTING RULE does not",
               "apollo_touch", "L4", None)],
    "tn-11": [("challengedBy", "s234-D2",
               "The factory's quality rubric (s234-D2/D6) should carry consequence, not just frequency.",
               "apollo_touch", "L3", None),
              ("challengedBy", "s234-D6",
               "The factory's quality rubric (s234-D2/D6) should carry consequence, not just frequency.",
               "apollo_touch", "L3", None)],
    "tn-14": [("challengedBy", "s217-D2",
               "Bento module counts (s217-D2/D5) should be justified by grouping and scanning, NOT by 7±2.",
               "apollo_touch", "L3", None),
              ("challengedBy", "s217-D5",
               "Bento module counts (s217-D2/D5) should be justified by grouping and scanning, NOT by 7±2.",
               "apollo_touch", "L3", None)],
    "tn-15": [("resolvedBy", "s151-D1",
               "Background-keyed colour rules, which is exactly what s151-D1 does",
               "how_it_resolves", "L1", None),
              ("touches", "s149-D1", "s149-D1 (mono error ink camp)", "apollo_touch", "L4", None),
              ("touches", "s194-D1",
               "s194-D1 (contrast duty attaches to label and glyph, not chrome)",
               "apollo_touch", "L4", None)],
    "tn-16": [("resolvedBy", "s234-D3", "adopt 2.5.5 for controls (s234-D3)",
               "how_it_resolves", "L1", None),
              ("resolvedBy", "s116-D1", "exempt marks explicitly with a named check (s116-D1)",
               "how_it_resolves", "L1", None)],
    "tn-17": [("resolvedBy", "s202-D1",
               "s202-D1 inherits console's tuned dimensions across the square themes",
               "how_it_resolves", "L1", None),
              ("touches", "s217-D2", "s217-D2 (gutter is the only divergence)",
               "apollo_touch", "L4", None)],
    "tn-22": [("resolvedBy", "s217-D8",
               "keyline HUGS the module rather than sitting centred in the gutter, which resolves this precisely",
               "how_it_resolves+apollo_touch", "L1", None)],
    "tn-27": [("resolvedBy", "s234-D6",
               "Dave already leans this way: 'mechanical over inference' (s234-D6)",
               "how_it_resolves", "L1", None),
              ("touches", "s234-D2", "s234-D2 factory goal", "apollo_touch", "L4", None)],
    "tn-29": [("touches", "s234-D3", "Apollo adopted 2.4.13 at s234-D3", "apollo_touch", "L4",
               "\"adopted\" could be read as resolvedBy; the row's how_it_resolves names no "
               "ruling, so the least claim is taken; status is settled-by-obligation either way")],
}

# L5 — apollo_touch values that carry NO ruling id, so no link (the words stay at the R1 row)
NO_ID_TOUCH = {"tn-03", "tn-04", "tn-05", "tn-18", "tn-19", "tn-20", "tn-21", "tn-25", "tn-30"}
NULL_TOUCH = {"tn-06", "tn-09", "tn-10", "tn-12", "tn-13", "tn-23", "tn-24", "tn-26", "tn-28"}

RULING_ID = re.compile(r"\bs\d+-D\d+\b")
PR_ID = re.compile(r"\bpr-[a-z0-9][a-z0-9-]*", re.I)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def words(s):
    return len(s.split())


def new_id(tn):
    return "pl-" + tn.split("-", 1)[1]


def migrate():
    src = json.load(open(SRC, encoding="utf-8"))
    tensions = src["tensions"]
    register = {p["id"]: p for p in json.load(open(REGISTER, encoding="utf-8"))["principles"]}
    rulings = {r["id"]: r for r in json.load(open(RULINGS, encoding="utf-8"))["rulings"]}
    problems = []

    # --- the row-by-row derivation -------------------------------------------------------
    polarities, table, stub_use = [], [], {}
    for t in tensions:
        tid = t["id"]
        # every `pr-` / ruling id the R1 side strings carry must be accounted for by PARTIES
        side_ids = set()
        for k in ("side_a", "side_b", "side_c"):
            s = t.get(k) or ""
            side_ids |= {m.rstrip("-.,;:").lower() for m in PR_ID.findall(s)}
            side_ids |= set(RULING_ID.findall(s))
        declared = {ref for ref, _r, _n in PARTIES[tid]}
        for sid in side_ids:
            target = DANGLING.get(sid, (sid,))[0]
            if target not in declared:
                problems.append(f"{tid}: R1 side id {sid!r} is not carried by PARTIES")
        for ref, role, note in PARTIES[tid]:
            if ref.startswith("st-"):
                if ref not in STUBS:
                    problems.append(f"{tid}: stub {ref!r} is not declared in STUBS")
                stub_use.setdefault(ref, []).append(tid)
            elif ref.startswith("pr-"):
                if ref not in register:
                    problems.append(f"{tid}: party {ref!r} not in the principle register")
            elif ref not in rulings:
                problems.append(f"{tid}: party {ref!r} is neither a principle, a stub nor a ruling")
            if note is not None and words(note) > 15:
                problems.append(f"{tid}: note on {ref!r} exceeds 15 words")
        parties = []
        for ref, role, note in PARTIES[tid]:
            p = {"ref": ref, "role": role}
            if note is not None:
                p["note"] = note
            parties.append(p)

        links = []
        touch = t.get("apollo_touch")
        touch_ids = set(RULING_ID.findall(touch or ""))   # `s114-D3/D5`: the D5 half is checked by hand below
        for typ, ref, quote, field, rule, unproven in LINKS.get(tid, []):
            if ref not in rulings:
                problems.append(f"{tid}: link {ref!r} not in knowledge/_rulings.json")
            if words(quote) > 15:
                problems.append(f"{tid}: quote for {ref!r} is {words(quote)} words (>15)")
            # the quote must be VERBATIM from the row's own text (rule Q)
            hay = " ".join(str(t.get(k) or "") for k in ("the_pull", "mediating_variable",
                                                          "how_it_resolves", "apollo_touch"))
            if quote not in hay:
                problems.append(f"{tid}: quote {quote!r} is not verbatim in the R1 row")
            links.append({"type": typ, "ref": ref, "quote": quote})
        if touch is None and tid not in NULL_TOUCH:
            problems.append(f"{tid}: apollo_touch is null but the row is not in NULL_TOUCH")
        if touch and not touch_ids and tid not in NO_ID_TOUCH:
            problems.append(f"{tid}: apollo_touch carries no ruling id but is not in NO_ID_TOUCH")
        if touch_ids:
            linked = {l["ref"] for l in links}
            for rid in touch_ids:
                if rid not in linked:
                    problems.append(f"{tid}: apollo_touch names {rid} but no link carries it")
        # `s114-D3/D5` — the shorthand carries a second id the regex cannot see; declared:
        if tid == "tn-07" and "s114-D5" not in {l["ref"] for l in links}:
            problems.append("tn-07: the D5 half of `s114-D3/D5` is not linked")

        node = {
            "id": new_id(tid),
            "parties": parties,
            "mediating_variable": t["mediating_variable"],
            "links": links,
            "sources": [{"path": SRC_REL, "id": tid}],
        }
        polarities.append(node)
        table.append({
            "r1_id": tid, "id": node["id"],
            "apollo_touch": touch,
            "links": [(typ, ref, quote, field, rule, unproven)
                      for typ, ref, quote, field, rule, unproven in LINKS.get(tid, [])],
            "no_link_reason": ("null in R1" if touch is None else
                               ("no ruling id in the value" if tid in NO_ID_TOUCH else None)),
        })

    unused = sorted(set(STUBS) - set(stub_use))
    if unused:
        problems.append(f"declared stubs referenced by no row: {unused}")

    stubs = [{"id": k, "phrase": v} for k, v in sorted(STUBS.items())]
    return src, polarities, stubs, table, problems, stub_use


def render_files(src, polarities, stubs):
    src_sha = sha256(SRC)
    pol = {
        "$description": (
            "THE ONE HOME for polarities (s238-D1): a polarity is a node with N typed parties, "
            "each resolving to a principle, an obligation, a ruling (knowledge/_rulings.json) or a "
            "declared stub (stubs.json), and typed out-links to rulings (s238-D6: resolvedBy / "
            "explainedBy / challengedBy / touches). It carries NO status (s238-D3: derived at build "
            "time into _generated/polarity-status.json) and NO judgement text (s238-D7 refusal 3: "
            "its only judgement is a typed link). Pairwise edges are DERIVED into "
            "_generated/polarity-edges.json, never authored. Schema: schema/polarity.schema.json. "
            "Writer: knowledge/_validate_polarities.py --add-polarity (textual, reconstruction-proven). "
            "'tension' was renamed 'polarity' before generation (s238-D4); ids tn-NN -> pl-NN, the "
            "R1 id kept under sources[].id."),
        "$migration": {
            "from": SRC_REL, "sha256": src_sha, "by": SELF_REL,
            "receipts": [
                "pr-info-scent -> pr-information-scent (tn-28 -> pl-28; lane T finding 7)",
                "pr-two-red-law -> s151-D1 as a PARTY of pl-15, R1 spelling kept in note "
                "(s151-D1 says: \"THE TWO-RED LAW, background-keyed, FIRM\")",
                "side_a/side_b/side_c -> parties[].role; apollo_touch -> links[] typed by the rules "
                "printed in " + SELF_REL + "; the_pull/how_it_resolves stay at the frozen R1 row",
            ],
        },
        "polarities": polarities,
    }
    st = {
        "$description": (
            "DECLARED STUBS (lane T finding 8): a party that is a phrase, not a register node. A stub "
            "is a node with an id and the verbatim phrase, nothing else. Home: knowledge/brain/ "
            "(s238-D1). Writer: knowledge/_validate_polarities.py --add-stub."),
        "stubs": stubs,
    }
    return (json.dumps(pol, indent=1, ensure_ascii=False) + "\n",
            json.dumps(st, indent=1, ensure_ascii=False) + "\n")


def print_table(table, polarities, stubs, stub_use):
    by_type = {}
    n_links = 0
    for p in polarities:
        for l in p["links"]:
            by_type[l["type"]] = by_type.get(l["type"], 0) + 1
            n_links += 1
    n_parties = sum(len(p["parties"]) for p in polarities)
    print("=" * 96)
    print(__doc__.split("MIGRATION RULES", 1)[1].split("\n", 1)[1].rstrip())
    print("=" * 96)
    print(f"rows {len(polarities)} · parties {n_parties} · stubs {len(stubs)} · links {n_links} by type "
          + " ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
    print("\n--- P2 DANGLING-ID RECEIPTS ---")
    for old, (new, kind, tid, why) in DANGLING.items():
        print(f"  {tid}: {old!r} -> {new!r} ({kind}) — {why}")
    print("\n--- MIGRATION TABLE: every former apollo_touch -> typed link(s), with the quote that justifies the type ---")
    unproven = 0
    for row in table:
        if row["apollo_touch"] is None:
            print(f"  {row['r1_id']} -> {row['id']}: apollo_touch null -> no link")
            continue
        if not row["links"]:
            print(f"  {row['r1_id']} -> {row['id']}: NO LINK ({row['no_link_reason']}) — value: "
                  f"\"{row['apollo_touch'][:70]}…\"")
            continue
        for typ, ref, quote, field, rule, unp in row["links"]:
            flag = " ⚠ UNPROVEN: " + unp if unp else ""
            if unp:
                unproven += 1
            print(f"  {row['r1_id']} -> {row['id']}: {typ:12s} {ref:9s} [{rule} from {field}] "
                  f"\"{quote}\"{flag}")
    print(f"\n  link-type verdicts marked UNPROVEN: {unproven}")
    print("\n--- STUBS (id · verbatim phrase · used by) ---")
    for s in stubs:
        print(f"  {s['id']:55s} \"{s['phrase']}\"  <- {', '.join(stub_use[s['id']])}")
    return {"rows": len(polarities), "parties": n_parties, "stubs": len(stubs), "links": n_links,
            "by_type": by_type, "unproven_types": unproven}


def main(argv):
    write = "--write" in argv
    out_dir = None
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
    src, polarities, stubs, table, problems, stub_use = migrate()
    counts = print_table(table, polarities, stubs, stub_use)
    print("\n--- SOURCE RECEIPT ---")
    print(f"  {SRC_REL}\n  sha256 {sha256(SRC)}")
    if problems:
        print("\n⛔ MIGRATION REFUSED — the declared tables do not account for the R1 rows:")
        for p in problems:
            print("   -", p)
        return 1
    pol_text, st_text = render_files(src, polarities, stubs)
    print("\n  polarities.json would be", len(pol_text), "bytes; stubs.json", len(st_text), "bytes")
    print("  COUNTS", json.dumps(counts, ensure_ascii=False))
    if write or out_dir:
        dest = out_dir or BRAIN
        os.makedirs(dest, exist_ok=True)
        for name, text in (("polarities.json", pol_text), ("stubs.json", st_text)):
            path = os.path.join(dest, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  WROTE {path}  sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()}")
    else:
        print("  (dry run — pass --write to write into knowledge/brain/, or --out DIR)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
