#!/usr/bin/env python3
"""_gen_pack_manifest.py — the GENERATOR behind `apollo-spider/build-designer-pack.sh`.

WHY THIS EXISTS. `s219-D4(2)`: "THE EXACT CUT IS A PROPOSED MANIFEST FOR HIS EYE BEFORE THE
BAKE — release = explicit, versioned, Dave's word." A hand-kept ship list is the v1 defect the
v2 receipt names in its own words ("v1's copy-list had gone stale"): a copy-list typed by a
human ages against the tree that moved underneath it and nothing measures the gap. So the
manifest is GENERATED from a NAMED COMMIT — never from the working tree, never by hand — and
the bake reads the manifest rather than re-deriving the list a second time.

THE THREE JOBS (one file, three modes; the .sh is the only entry point a human drives):

  --manifest   enumerate the cut at <commit> into knowledge/_release/_pack_manifest.json
  --probe      import-probe every knowledge/_validate_*.py in an ISOLATED staging dir and
               write knowledge/_release/_pack_gate_probe.json (the gate verdict table)
  --stage      materialise the manifest's paths at <commit> into a dir (the bake's stage)
  --zip        deterministic zip of a stage dir (fixed mtimes, sorted order, fixed mode)
  --check      verify a baked pack against manifest + commit
  --selftest   the bites, mutation-tested

⛔ THE GATE VERDICTS ARE MEASURED, NOT READ BY EYE. `--probe` copies each validator plus its
LOCAL helper imports into a throwaway dir that contains ONLY the non-gate shipped set, then
RUNS it and classifies the exit. Reading a validator's import block by eye answers "what does
it import", which is not the question — the question is "does it RUN outside this repo", and
only a run answers that [[mutation-tests-the-clause-not-the-feature]]. The classifier:

  RUNNABLE        the gate reached a verdict (exit 0, or a clean non-zero FAIL with no
                  traceback) inside the staged pack
  NEEDS-DEP(x)    ModuleNotFoundError naming a third-party module `x` — or (s223-D5) an honest
                  COULD-NOT-ASK refusal at exit 77, where `x` is the remedy the refusal itself
                  names: the gate could not ASK its question on this box, which is a fact about
                  the box, never a verdict about the pack
  REPO-BOUND(why) it crashed reaching for something the pack does not ship — the offending
                  path is extracted from the traceback and named in the verdict

★ THE DIFFERENTIAL ARM — because a FAIL is not automatically a run. A gate that returns a
clean non-zero verdict inside the pack has demonstrably RUN; but its red may be caused by the
pack not carrying the thing it audits (`_validate_package_delta.py` audits `memento-package/`
against `knowledge/` — in a designer's project that subject does not exist, so its red is a
packaging artefact, not a finding). Reading the message and deciding by eye is exactly the
guess this module refuses. So every FAIL is re-run against a FULL-TREE stage of the same
commit and the two verdicts are compared:

  FAIL in pack + PASS in full tree  ⇒  REPO-BOUND (the pack does not carry its subject)
  FAIL in both                      ⇒  RUNNABLE (a live red, honestly declared, not a fence)

⛔ The full-tree run happens in a `git archive` STAGE under /var/tmp, never in the repo — a
validator that writes an audit file must not be allowed to dirty Dave's tree (#158 class).

⛔ DETERMINISM. The manifest carries NO timestamp. Its provenance is the commit sha, and the
build date it stamps into the pack README is the COMMIT's own date, not today's — a build-day
stamp would make two bakes of the same commit differ, which destroys the delta-audit this
whole shape exists to enable. `manifest_sha256` is the sha256 of the manifest file's bytes.

GATE-GLOB-SCOPE: this module reads the repo through `git ls-tree`/`git archive` at a named
commit and writes exactly two files under `knowledge/_release/`, plus whatever stage/zip path
it is explicitly given. It globs nothing else and widens no other gate's glob.

USAGE
    python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit <sha>
    python3 knowledge/_release/_gen_pack_manifest.py --probe --commit <sha>
    python3 knowledge/_release/_gen_pack_manifest.py --stage <dir> --commit <sha>
    python3 knowledge/_release/_gen_pack_manifest.py --zip <stage> --out <zip> --commit <sha>
    python3 knowledge/_release/_gen_pack_manifest.py --check <zip> --commit <sha>
    python3 knowledge/_release/_gen_pack_manifest.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# ---------------------------------------------------------------------------------------------
# IDENTITY (s219-D8). Two name families, and the rule is module TYPE correctness:
#   APOLLO PACK RELEASES take LUNAR MODULE names — they are what lands in a designer's hands.
#   MEMENTO RELEASES take COMMAND MODULE names — Memento navigates, remembers, carries the crew.
# The repo stays the command seat. s219-D8 tightens that to the STRICT MISSION PAIR: a release
# takes ONE mission's whole pair. This is Apollo 9 — SPIDER (the LM) and GUMDROP (the CM). The
# next release takes Apollo 10's pair, then Apollo 11's, in mission order; the names are in the
# ruling, not copied here, because a future release's name is not this file's live fact.
# s219-D6's module-type error and s219-D7's cross-mission pairing are both SUPERSEDED — neither
# reached a commit — and D7's two-family TYPE rule stands and is stated above.
#
# ⚠ THE FILENAMES ARE DELIBERATELY GENERIC — `_gen_pack_manifest.py`, `_pack_manifest.json`,
# `_pack_gate_probe.json`. The release IDENTITY lives in the DATA below and in the zip's name,
# never in the machinery's filenames. #219 paid for the other choice: the v3-named generator and
# its two v3-named artefacts had to be renamed across nine files the moment Dave named the
# release, and Eagle and Columbia are still in reserve. The generator is the machinery that cuts
# THE CURRENT PACK; what that pack is called is a field, not a path.
# (The names are spelled out only in the report, deliberately — a stale-name grep runs over this
# file in the selftest, and a file that quotes the dead name cannot police it.)
PACK_NAME = "Apollo — Spider"          # display name, prose register
PACK_SLUG = "Apollo-Spider"            # filename register: the zip and the pack root
VERSION = "v1.0.2"                     # Spider's own lineage starts here; v1/v2 stay frozen
MEMENTO_CUT_NAME = "Memento — Gumdrop"
MEMENTO_CUT_VERSION = "v1.0.2"

SCHEMA = "apollo-designer-pack-manifest/1"
MANIFEST_PATH = os.path.join(HERE, "_pack_manifest.json")
PROBE_PATH = os.path.join(HERE, "_pack_gate_probe.json")

# ---------------------------------------------------------------------------------------------
# THE CUT — declared as include/exclude rules over the commit's tracked path list.
# Each group is (key, title, plain-words purpose, [rules]). A rule is a predicate over a path.
# Order matters: the FIRST group that claims a path owns it, so a path can never be double-counted.
# ---------------------------------------------------------------------------------------------

def _pfx(*prefixes):
    return lambda p: p.startswith(prefixes)


def _under(prefix, suffixes=None, not_under=(), not_base=()):
    def f(p):
        if not p.startswith(prefix):
            return False
        rest = p[len(prefix):]
        if any(rest.startswith(n) for n in not_under):
            return False
        b = os.path.basename(p)
        if b in not_base:
            return False
        if suffixes and not p.endswith(tuple(suffixes)):
            return False
        return True
    return f


# Design-facing runbooks: the ones a designer building with Apollo actually opens.
# The Memento-internal ones (capture-ritual, git-commit, context-gauge, parallel-conductor,
# dream-pass, decision-audit) are NOT here — see MEMENTO_RUNBOOK_CALL in the manifest notes.
DESIGN_RUNBOOKS = [
    "_RUNBOOK-compose-from-canon.md",
    "_RUNBOOK-gated-component.md",
    "_RUNBOOK-render-verify.md",
    "_RUNBOOK-criteria-contract.md",
    "_RUNBOOK-consult.md",
    "_RUNBOOK-onboard-code-library.md",
    "_RUNBOOK-review-doc.md",
    "_RUNBOOK-toolkit-tranche.md",
    "_RUNBOOK-reconcile-dark-tokens.md",
    "_RUNBOOK-external-claims.md",
    "_RUNBOOKS.md",
]

# Explicitly NOT shipped with the design half. Memento's own half ships none of these either:
# memento-package/ carries machinery only (5 files + the manifest), no runbooks at all — so the
# clean cut MIRRORS that choice and these stay repo-side. Named so the omission is auditable.
MEMENTO_INTERNAL_RUNBOOKS = [
    "_RUNBOOK-capture-ritual.md",
    "_RUNBOOK-git-commit.md",
    "_RUNBOOK-context-gauge.md",
    "_RUNBOOK-parallel-conductor.md",
    "_RUNBOOK-dream-pass.md",
    "_RUNBOOK-decision-audit.md",
    "_RUNBOOK-densify-adversarial.md",
]

# The local (in-repo) modules each validator needs. MEASURED by AST at probe time, not typed —
# this constant is only the seed for the stage: helpers live beside the gates in knowledge/.
HELPER_HOMES = {
    "gen_theme_cascade": "knowledge/canon/gen_theme_cascade.py",
}

# HOW A GATE IS INVOKED IN THE PACK, where a bare run is not the right question (#219 N2 -> N1
# handoff, N2's own measurement). The probe DERIVES an invocation for the two shapes it can
# detect — a write-gate refusal wants `--write`, an args refusal that names `--all` wants `--all`.
# Everything else defaults to bare, and for one gate bare is the wrong question:
#
#   _validate_type_composites.py — bare, it reports the design system's ENTIRE standing composite
#   debt (664 inside the pack) as if a designer had caused it on the day they unzipped. `--check`
#   asks the question the pack actually wants asked — "has the declared debt GROWN?" — and it is
#   the gate's own ratchet arm, not a softer gate: `TYPE RATCHET CHECK PASS — declared debt holds
#   at 1091 (0 new). This is DEBT, not a pass of the underlying gate.`
#
# ⛔ THIS TABLE IS A LAST RESORT AND MUST STAY SMALL. An invocation the PROBE measures is a
# verdict; an invocation typed here is a claim, and it ages like every other typed claim. Each
# entry needs a one-line reason above it, and the manifest carries the invocation so the pack's
# runner replays what was measured rather than knowing a convention.
DECLARED_INVOCATIONS = {
    "_validate_type_composites.py": "--check",
}

# Data files the gates read that are NOT part of any other group but must ride with the gates
# for them to have anything to check. Verdict-driven: only the ones the probe proves are needed.
GATE_DATA_CANDIDATES = [
    "knowledge/_assertions.json",
    "knowledge/_ASSERTIONS.md",
    "knowledge/_binds-ratchet.json",
    "knowledge/_type_ratchet.json",
    "knowledge/_TOKEN-FORK-LEDGER.json",
    "knowledge/component-types.json",
    "knowledge/chart-intents.json",
    "knowledge/canon/_type-bindings.json",
    "knowledge/canon/_bindings-applied.json",
]

# ---------------------------------------------------------------------------------------------
# THE PHOTOGRAPHY SPECIMEN (#220, Dave's ask: "30 or so… so that the bentos and gallery work")
#
# ⛔ WHY THIS EXISTS AT ALL. The pack ships showroom/, and the shipped bento and gallery pages
# reference photographs BY FILENAME. `knowledge/assets/photography-web/` was excluded wholesale,
# so v1.0.0's foundations pages render with every image broken. A library whose showroom is a
# grid of missing-image glyphs is not a library.
#
# THE FIRST FIFTEEN ARE NOT A CHOICE. They are `gen_bento_roles_217.SPECIMEN_FILES` — the pinned
# set every one of those pages was built and signed off on — and they are IMPORTED from that
# module, never re-typed here. ADR-0017: one home. A second copy of a pinned list is a list that
# drifts, and #218 already paid for slicing this set by sort order
# [[specimen-starts-from-reference]].
#
# THE OTHER FIFTEEN are chosen against the manifest's own measured data, not by eye:
#   · ≤ 300 KB derivative, the ceiling `verify_photography_218.py` already declares;
#   · ASPECT SPREAD to the limit the population allows — and the population is the constraint,
#     not the taste: of 251 derivatives only 8 are portrait and 3 are square. All 5 unpinned
#     portraits and all 3 squares are taken, because taking fewer would leave a bento with no
#     tall or square tile to place. The remaining 7 are landscape.
#   · SUBJECT and SOURCE variety read out of `exif_description` / `licence_source`: the pinned 15
#     are 13/15 Getty and lean corporate, so the 7 landscapes deliberately bring Stocksy and
#     EyeEm, and subjects the pinned set has none of — trade/logistics, culture, travel,
#     architecture, a close portrait, leisure.
#
# ⚠ A PINNED NAME WHOSE FILE IS GONE SHIPS NOTHING, SILENTLY, unless something says so. The
# selftest bites the whole set for existence at generation time.
PHOTOGRAPHY_ADDITIONS = (
    # the five unpinned portraits — every portrait the population has
    "1168737-w1600.jpg",                        # Stocksy · woman reading behind a red book
    "688657-w1600.jpg",                         # Stocksy · woman on a boat, feet in the water
    "gettyimages-1273552095-144dpi-w1600.jpg",  # Getty · Hong Kong street traffic
    "gettyimages-2184837877-w1600.jpg",         # Getty · man eating lunch at a cafe
    "gettyimages-643949547-144dpi-w1600.jpg",   # Getty · alpenglow on a mountain ridge
    # all three squares — every square the population has
    "gettyimages-167527306-w1600.jpg",          # Getty · child in a wetsuit on a beach
    "gettyimages-184310083-w1600.jpg",          # Getty · balcony shadows, architectural abstract
    "gettyimages-dv2068033-144dpi-w1600.jpg",   # Getty · office worker at a desk at sunset
    # seven landscapes, for subject and source spread
    "3476592-w1600.jpg",                        # Stocksy · boys on a sandy beach at sunset
    "eyeem-100014108-147578861-w1600.jpg",      # EyeEm · close portrait, woman to camera
    "eyeem-100014108-152975235-w1600.jpg",      # EyeEm · low angle, building against sky
    "stocksy-3225764-w1600.jpg",                # Stocksy · Man Mo temple lanterns, Hong Kong
    "stocksy-5763914-w1600.jpg",                # Stocksy · docks and containers — trade
    "stocksy-613297-w1600.jpg",                 # Stocksy · two professionals discussing finance
    "stocksy-6968340-w1600.jpg",                # Stocksy · airplane wing at sunrise
)


# ---------------------------------------------------------------------------------------------
# GATES THAT LIVE IN THE DESIGNER-GATE NAMESPACE BUT AUDIT THE RELEASE, NOT THE DESIGN (#220)
#
# Every other release-side gate is fenced out of the ship list by ACCIDENT of where it sits:
# `knowledge/_release/_gate_*.py` does not start with `knowledge/_gate_`, so the gates match
# never sees it. `_gate_pack_imports.py` sits at `knowledge/` and would therefore be claimed —
# and its SUBJECT is a baked pack. A designer who unzips this has no zip to audit and no bake to
# run; the gate would ship, be counted in the roster, and have nothing to say.
#
# ⛔ AND IT WOULD MOVE A NUMBER DAVE RULED. `s219-D9`: *"the ship list carries only gates that can
# actually run in a designer's project - 55 files in the gates group (35 runnable + 3 needs-dep
# + helpers/data/ci-template)"*. Letting a new gate in raises 55 to 56 with nobody deciding
# anything [[dont-launder-a-premise-into-a-ruling]]. The roster stays at 55 and whether this
# gate should ship is asked, not assumed.
RELEASE_SIDE_GATES = {"_gate_pack_imports.py"}

_PHOTO_SPECIMEN = []


def photography_specimen():
    """The 30 filenames that ship. The pinned 15 come from their ONE home, by import."""
    if not _PHOTO_SPECIMEN:
        d = os.path.join(ROOT, "knowledge", "_render")
        if d not in sys.path:
            sys.path.insert(0, d)
        try:
            from gen_bento_roles_217 import SPECIMEN_FILES
        except Exception as e:                    # loud and named — never a quiet short set
            raise RuntimeError("photography specimen REFUSED: cannot read the pinned set from "
                               "knowledge/_render/gen_bento_roles_217.py (%s). The pack's bento "
                               "and gallery pages name those files; shipping a guess is worse "
                               "than refusing." % e)
        _PHOTO_SPECIMEN.extend(tuple(SPECIMEN_FILES) + PHOTOGRAPHY_ADDITIONS)
    return tuple(_PHOTO_SPECIMEN)


PHOTOGRAPHY_DIR = "knowledge/assets/photography-web/"

EXCLUDED = [
    ("reviews/", "Dave's review surfaces — this session's thinking, not the engine. s219-D4(1): "
                 "'without all the review files and extras'."),
    ("notes/", "Briefs, receipts and filed sub-reports — the workshop's paperwork."),
    ("runs/", "Session run logs — state, not machinery."),
    ("archive/", "Retired material, kept for history only."),
    ("projects/", "Client project work — not the design system."),
    ("system-manager/", "A strand project, not Apollo."),
    ("second-system-govuk/", "A strand project, not Apollo."),
    ("digital-experience-transformation/", "A strand project, not Apollo."),
    ("knowledge/assets/fonts/", "LICENCE. Only the _desktop set ships (see the library group); "
                                "any webfont pack is outside the licence we hold."),
    ("knowledge/assets/photography/", "LICENCE. Getty/EyeEm stock originals — non-repo already."),
    ("knowledge/assets/photography-web/", "LICENCE, NARROWED AT #220. The 251 derivatives as a "
                                          "SET stay out — redistributing a stock library is not "
                                          "covered. What ships is a NAMED specimen of 30, and "
                                          "only because the shipped bento and gallery pages "
                                          "reference 15 of them BY FILENAME and render broken "
                                          "without them (Dave's ask, #220). Same shape as the "
                                          "fonts fence: the directory is excluded, one declared "
                                          "subset is not. ⚠ THE LICENCE POSITION ITSELF IS NOT "
                                          "SETTLED — s219-D5(Q2) settled the FONT licence and "
                                          "says nothing about Getty/EyeEm/Stocksy. This is "
                                          "Dave's word to give, and it is asked in the report."),
    ("knowledge/tokens/_raw/", "ADR-0005: raw Figma exports are client assets, untracked."),
    ("API-KEY.txt", "Secret."),
    (".token-cache.json", "Secret."),
    ("GOOD-MORNING.md", "Dave's session state. s219-D4(1): state, not machinery."),
    ("_LIVE-STATE.md", "Dave's session state."),
    ("_CHAIN.md", "Dave's session state."),
    ("knowledge/_state.json", "Dave's task store — his items, not a designer's."),
    ("knowledge/_rulings.json", "Apollo's ruling store — Dave's record."),
    ("knowledge/_SESSIONS.jsonl", "Session state."),
    ("knowledge/_memento-index.json",
     "Generated from Apollo's own record — Dave's memory, and it must not travel. ⚠ THE REASON "
     "THIS ROW USED TO GIVE WAS FALSE, and it is corrected here rather than softened: it said "
     "'adopters regenerate'. THEY CANNOT. Measured at #220 from a fresh stage — the pack carries "
     "NO index builder (`knowledge/_build_memento_index.py` is not in the ship list and nothing "
     "else writes the index), so a Gumdrop designer following `memento-package/README.md` line "
     "59 or the boot skill's line 75 to `machinery/_memento_search.py` gets a refusal naming "
     "`python3 knowledge/_build_all.py`, which the pack also does not carry. RETRIEVAL — half of "
     "what Memento IS — cannot be started in a Gumdrop project at all. Driven, not reasoned: "
     "copying Apollo's builder into the stage and running it produces FIFTEEN refusals (every "
     "declared source missing, every glob empty), because its corpus contract is Apollo's "
     "GM/LS/archives/gauge-log/lanes/briefs, none of which a fresh project has. So carrying the "
     "builder in the import closure is not the fix — it would ship a REFUSAL, the exact thing "
     "s219-D9 chose against. This is `memento-package/machinery/_MACHINERY-MANIFEST.md`'s own "
     "generalisation-debt item 3 ('index bootstrap for a fresh project'), still undone: the cut "
     "was copied verbatim on the stated rule that 'generalisation is a build step, not a copy "
     "step', and that build step was never built. ⛔ NOT SETTLED HERE — what the pack should do "
     "about retrieval is a ship-list decision and Dave's alone; it is asked in the #220 "
     "addendum report with three priced options."),
    ("designer-skills-v1/", "FROZEN release, s114-D4."),
    ("designer-skills-v2/", "FROZEN release, s114-D4. Its four SKILL.md were the REFERENCE for "
                            "the Spider refresh, not the source — Spider ships its own five from "
                            "apollo-spider/skills/ (#219 R3)."),
]


def groups():
    """The ordered group table. First match owns the path."""
    return [
        dict(key="engine-canon.tokens", group="engine-canon", title="Tokens",
             plain="Every design token you work from — colour, type, spacing, elevation, "
                   "motion, the four theme override sets and the palettes.",
             match=_under("knowledge/tokens/", not_under=("_raw/",),
                          not_base=("EXAMPLE-tokens.json",))),
        dict(key="engine-canon.components", group="engine-canon", title="Component contracts",
             plain="One .meta.json per component: props, variants, token bindings, states, "
                   "anti-patterns, accessibility. Plus the schema they validate against.",
             match=lambda p: p.startswith("knowledge/components/")
                             and not os.path.basename(p).startswith("EXAMPLE-")),
        dict(key="engine-canon.snippets", group="engine-canon", title="Reference markup",
             plain="The reviewed HTML for each component — what 'correct' looks like.",
             match=lambda p: p.startswith("knowledge/snippets/")
                             and not os.path.basename(p).startswith("EXAMPLE-")),
        dict(key="engine-canon.canon", group="engine-canon", title="Canon CSS + its generators",
             plain="canon.css and type.css (the composition layer), the data-vis behaviour JS, "
                   "the type bindings, and the generators that mint canon from tokens.",
             match=_under("knowledge/canon/", not_under=("__pycache__/",))),
        dict(key="engine-canon.compliance", group="engine-canon", title="Compliance graph",
             plain="Which WCAG criteria apply to which component, plus the rule set.",
             match=_under("knowledge/compliance/", not_under=("_vendor/",),
                          not_base=("EXAMPLE-contrast-rule.json",))),
        dict(key="engine-canon.icons", group="engine-canon", title="Icon library",
             plain="The real glyphs. Skills must use these and never invent an icon — the v2 "
                   "pack shipped them for exactly that reason.",
             match=_under("knowledge/assets/icons/", not_base=())),
        dict(key="engine-canon.logos", group="engine-canon", title="Brand marks",
             plain="The hexagon and masterbrand SVGs, light/dark, colour/mono.",
             match=_under("knowledge/assets/logos/")),
        dict(key="engine-canon.guidelines", group="engine-canon", title="Design guidelines",
             plain="The written standards a designer consults — brand, colour, type, tone, "
                   "accessibility, component standards.",
             match=_under("knowledge/guidelines/")),

        dict(key="gates", group="gates", title="Runnable gates",
              plain="The executable checks. Each one below was RUN in an isolated copy of this "
                   "pack to find out whether it works away from this repo — the verdicts are "
                   "measured, not guessed.",
             match=lambda p: (p.startswith("knowledge/_validate_")
                              or p.startswith("knowledge/_gate_")) and p.endswith(".py")
                             and os.path.basename(p) not in RELEASE_SIDE_GATES),

        dict(key="runbooks", group="runbooks", title="Runbooks",
             plain="The design-facing procedures: how to compose from canon, how to take a "
                   "component through its gates, how to render and verify, how to write a "
                   "criteria contract, how to onboard an existing code library.",
             match=lambda p: os.path.dirname(p) == "knowledge"
                             and os.path.basename(p) in DESIGN_RUNBOOKS),

        dict(key="library.showroom", group="library", title="Showroom",
             plain="The live library: every component page, the foundations pages (bento, "
                   "grids, logos, photography), the thumbnails and the index.",
             match=_under("showroom/")),
        dict(key="library.rails", group="library", title="Edit-pass rails manifest",
             plain="The one generated file the library, the editor and the generator all read, "
                   "so none of them can drift (s219-D3(6)).",
             match=lambda p: p == "knowledge/_render/_bento_edit_rails.json"),
        dict(key="library.render", group="library", title="Render machinery",
             plain="render.py — the proven headless-Chromium shape, so a designer can see their "
                   "own work the way Dave does.",
             match=lambda p: p == "knowledge/_render/render.py"),
        # s219-D5 (Q2) SETTLED the licence question this card used to carry: the desktop cut
        # ships, "designers are in-licence". The rule is unchanged — the group already claimed
        # these files — but the card no longer sends Dave to an open question that is closed.
        # The fence that is NOT moved: everything else under knowledge/assets/fonts/ stays
        # EXCLUDED, webfont packs included; the licence covers the desktop set only.
        dict(key="library.fonts", group="library", title="Desktop fonts",
             plain="The licensed desktop cut, so the library renders in the real face. "
                   "LICENCE POSITION, settled at s219-D5: these ship — your designers are "
                   "in-licence, the same licence that lets the desktop set be tracked in this "
                   "private repo. The webfont packs stay out.",
             match=_under("knowledge/assets/fonts/_desktop/")),
        # #220, Dave's ask. NAMED FILES ONLY — the match is set membership, never a prefix, so
        # the directory stays excluded and only the declared specimen crosses the fence. See
        # PHOTOGRAPHY_ADDITIONS for how the 30 were chosen and what the population allowed.
        dict(key="library.photography", group="library", title="Photography specimen",
             plain="Thirty photographs, so the bento and gallery pages in the showroom actually "
                   "have something in them. Fifteen are the pinned set those pages name by "
                   "filename — without them every tile is a broken image. The other fifteen add "
                   "the tall and square shapes a bento needs and a wider spread of subjects. "
                   "LICENCE POSITION: the stock library as a whole does NOT ship; this named "
                   "specimen does, and whether it may is Dave's word.",
             match=lambda p: (p.startswith(PHOTOGRAPHY_DIR)
                              and p[len(PHOTOGRAPHY_DIR):] in set(photography_specimen()))),

        dict(key="memento", group="memento-clean-cut", title="Memento machinery",
             plain="A clean cut of Memento — the chain generator, retrieval, the graph edges, "
                   "the gauge shim, the consult lexicon. Machinery only, no record: every "
                   "adopting project grows its own chain.",
             match=lambda p: p.startswith("memento-package/machinery/")
                             and "__pycache__" not in p),
        dict(key="memento.docs", group="memento-clean-cut", title="Memento docs",
             plain="What Memento is, and the boot rule.",
             match=lambda p: p in ("memento-package/WHAT-MEMENTO-IS.md",
                                   "memento-package/README.md")),
        dict(key="memento.plugin", group="memento-clean-cut", title="Memento Claude plugin",
             plain="The packaged plugin — the boot skill and its reference.",
             match=lambda p: p.startswith("memento-package/claude-plugin/")
                             and "__pycache__" not in p and not p.endswith(".zip")),

        # ---- THE COLD START (#219 N3, s219-D5 Q1 + Q4) ----------------------------------------
        # ⚠ ITS OWN GROUP, DECIDED AND DECLARED. These files could have been folded into
        # `memento-clean-cut`, and that was the alternative considered. They are not, for two
        # reasons. (1) The memento cards say "machinery only, no record: every adopting project
        # grows its own chain" — which s219-D5(Q1) has now made FALSE for this cut, since the
        # empty stores and a starter chain DO ship. Hiding the change inside a card that states
        # the opposite is how a release ships a contradiction. (2) The cold start is one
        # deliverable answering one clause of one ruling, and a named group is what makes it
        # visible on Dave's page and auditable if it ever silently drops out of the cut
        # [[forgotten-document-class]].
        # ⚠ ORDER: this sits BEFORE `skills` and matches only its own three prefixes, so it can
        # never swallow `apollo-spider/skills/`. It sits AFTER the memento groups so nothing it
        # claims was already owned.
        dict(key="gumdrop", group="gumdrop", title="Memento — Gumdrop cold start",
             plain="What a designer meets on day one: the guided first session, the Copilot "
                   "boot instructions, an empty task store and an empty rulings store with the "
                   "shapes already right, a starter chain that explains the first move, and the "
                   "two Memento runbooks rewritten for VS Code + Copilot. The stores ship EMPTY "
                   "on purpose — the shape is machinery, the contents are the designer's record.",
             match=lambda p: (p.startswith("apollo-spider/gumdrop/")
                              or p == "apollo-spider/FIRST-SESSION.md"
                              # `.github/` whole, not just copilot-instructions.md: the five
                              # prompt-file shims under `.github/prompts/` are the BRIDGE that
                              # makes the skills reachable in VS Code (#219 N3 dialect check).
                              # Naming one file here and adding the shims later is how half a
                              # bridge ships.
                              or p.startswith("apollo-spider/.github/"))),

        # #219 seam 7, on R3's Q1: the skills group ships R3's OWN five, not v2's four. Until this
        # was repointed the pack shipped v2's skills and none of the refreshed set — the whole
        # point of s219-D4(4). ⚠ FUNCTION OF THE COMMIT like every other path: at a commit before
        # apollo-spider/skills/ is tracked this claims NOTHING and the group is empty.
        dict(key="skills", group="skills", title="Skills",
             plain="The five Spider skills: four refreshed against this knowledge base and the new "
                   "gate-runner that runs the packed gates on a designer's own work.",
             match=lambda p: p.startswith("apollo-spider/skills/")
                             and p.endswith("/SKILL.md")),
    ]


# ---------------------------------------------------------------------------------------------
# git plumbing — every read is at a NAMED COMMIT
# ---------------------------------------------------------------------------------------------

def git(*args, cwd=None, binary=False):
    r = subprocess.run(["git"] + list(args), cwd=cwd or ROOT,
                       capture_output=True, check=False)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.decode()[:400]))
    return r.stdout if binary else r.stdout.decode()


def resolve_commit(ref):
    return git("rev-parse", ref).strip()


def commit_date(sha):
    """The COMMIT's own date, ISO, UTC. Used for the README stamp and the zip mtimes so two
    bakes of the same commit are byte-identical [[measure-dont-convert-units]]."""
    return git("show", "-s", "--format=%cI", sha).strip()


def commit_epoch(sha):
    return int(git("show", "-s", "--format=%ct", sha).strip())


def tree_paths(sha):
    out = git("ls-tree", "-r", "--name-only", sha)
    return [l for l in out.split("\n") if l]


def blob_sizes(sha, paths):
    """One batch call — `git cat-file --batch-check` over the named blobs."""
    if not paths:
        return {}
    inp = "".join("%s:%s\n" % (sha, p) for p in paths)
    r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=ROOT,
                       input=inp.encode(), capture_output=True, check=True)
    sizes = {}
    for path, line in zip(paths, r.stdout.decode().strip().split("\n")):
        parts = line.split()
        sizes[path] = int(parts[2]) if len(parts) >= 3 and parts[1] == "blob" else 0
    return sizes


def blob_shas(sha, paths):
    if not paths:
        return {}
    inp = "".join("%s:%s\n" % (sha, p) for p in paths)
    r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=ROOT,
                       input=inp.encode(), capture_output=True, check=True)
    out = {}
    for path, line in zip(paths, r.stdout.decode().strip().split("\n")):
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "blob":
            out[path] = parts[0]
    return out


def is_dirty():
    return bool(git("status", "--porcelain").strip())


# ⚠ #219 bake. The status is READ FROM THE STORE, never typed (the house rule: a ratification
# is Dave's word made record, s219-D4(2), and the record's one home is knowledge/_rulings.json).
# The read is from the CHECKOUT's store deliberately — the cut commit predates the ratification
# entry by construction, so a commit-archive read would deadlock the bake against itself.
# Fails LOUD on a malformed store; a missing entry is not an error, it is PROPOSED.
#
# ⛔ #223, s223-D3 — THE KEY IS PER CUT, NOT ETERNAL. This was a single hard-coded id,
# `RATIFY_ID = "s219-D10"`, which is Dave's word for v1.0.0 and for nothing else. Because the
# lookup never mentioned the VERSION, every future manifest inherited v1.0.0's ratification:
# bump `VERSION` to v1.0.2 and the page still printed "Ratified", and `--release` — whose only
# fence is that word (build-designer-pack.sh: `ratified || die`) — would have waved the next
# bake through without ever asking him. s219-D4(2) says the cut is HIS word; an eternal key
# turns one word into a standing permission, which is the opposite of what it says.
# So the id is now looked up BY THIS CUT'S VERSION. v1.0.0 keeps its word forever — the
# mapping is a ledger, not a switch, and rows are added, never moved. A version with no row
# is PROPOSED: the machine ASKS, and only Dave's fresh ruling answers.
# An EXPLICIT MAPPING deliberately, not a text-match on ruling bodies: a substring hunt for
# "v1.0.2" across every `says` field would ratify a cut off a ruling that merely MENTIONED it
# (this very entry, s223-D3, names v1.0.2 in its own body while explicitly withholding the
# word) — a gate that cannot tell a mention from a mandate is not a gate.
RATIFY_IDS = {
    "v1.0.0": "s219-D10",   # #219, Dave's word 'bake' (2026-08-26)
}

RULINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_rulings.json")


def ratify_id(version=None):
    """The ruling id that ratifies THIS cut — None if no ruling has been keyed to it yet."""
    return RATIFY_IDS.get(VERSION if version is None else version)


def ratification_status(store_path=None, version=None):
    v = VERSION if version is None else version
    p = RULINGS_PATH if store_path is None else store_path
    data = json.load(open(p))
    rl = data if isinstance(data, list) else data.get("rulings", data.get("entries"))
    if rl is None:
        raise SystemExit("_gen_pack_manifest: knowledge/_rulings.json has no rulings array — "
                         "cannot derive the release status from a store I cannot read")
    want = ratify_id(v)
    if want is None:
        return ("PROPOSED — no ruling is keyed to %s yet (s223-D3: the ratify check is re-keyed "
                "PER CUT). s219-D4(2): release = his word, and this cut has not had it." % v)
    for r in rl:
        if r.get("id") == want and r.get("status") == "ruled":
            return ("RATIFIED — %s names %s in the store; "
                    "s219-D4(2) satisfied by the store, not by prose" % (want, v))
    return ("PROPOSED — %s is keyed to ruling %s, which is not 'ruled' in the store "
            "(s219-D4(2): release = his word)" % (v, want))


def status_word():
    return "RATIFIED" if ratification_status().startswith("RATIFIED") else "PROPOSED"


# ---------------------------------------------------------------------------------------------
# THE GATE PROBE — measured, in an isolated dir
# ---------------------------------------------------------------------------------------------

STD = set(sys.stdlib_module_names)


def local_imports(src_text, knowledge_files):
    """AST scan for imports that resolve to a module living in knowledge/. Used to decide what
    to COPY into the probe stage — never to decide the verdict."""
    mods = set()
    try:
        t = ast.parse(src_text)
    except SyntaxError:
        return set(), set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                mods.add(n.module.split(".")[0])
    local = {m for m in mods if (m + ".py") in knowledge_files or m in HELPER_HOMES}
    third = {m for m in mods if m not in STD and m not in local}
    return local, third


TRACE = "Traceback (most recent call last)"
# ★ Widened deliberately: a well-mannered gate CATCHES its ImportError and prints a courteous
# refusal instead of a traceback (`_validate_state_contrast.py` prints COULD-NOT-ASK). Matching
# only `ModuleNotFoundError:` would call those RUNNABLE and hide a real dependency
# [[unmatched-grep-is-not-an-absence]] — the needle is the phrase, not the exception class.
MODNOTFOUND = re.compile(r"No module named [\"']([^\"']+)[\"']")
# ⛔ s223-D5 clause (1) — A REFUSAL IS NOT A VERDICT. Exit 77 is `_could_not_ask.EXIT`, the ruled
# COULD-NOT-ASK code: the gate could not ASK its question on THIS box. Named here as a literal
# because the classifier must run inside the staged pack, where `knowledge/_could_not_ask.py`
# may not be importable — the number is the contract, and it is asserted in `--selftest`.
REFUSAL_EXIT = 77
# The remedy a refusal names in its own words — the ruled legal form puts it in backticks
# (`playwright install chromium`). Read, never guessed [[feedback-measuring-tool-must-not-guess]].
REFUSAL_REMEDY = re.compile(r"`([^`\n]{3,80})`")
PATHERR = re.compile(r"(?:FileNotFoundError|NotADirectoryError|IsADirectoryError)[^\n]*?"
                     r"'([^']+)'")
# A gate that refuses for want of an ARGUMENT has run perfectly well; it just wants a target.
ARGS_REFUSAL = re.compile(r"no input files|Pass paths or --all|need at least one|"
                          r"REFUSED: need", re.I)
# A green that graded nothing. The gate's own count, in the gate's own words.
# ⚠ INPUT nouns only. The first cut matched any `0 <word>(s)` and therefore read "135
# snippet(s), 0 failure(s)" — a gate that graded 135 files and found nothing wrong — as a
# vacuous pass. Zero FAILURES is the good news; zero FILES is the empty subject. Different
# nouns, opposite meanings [[measure-dont-convert-units]].
EMPTY_POP = re.compile(r"\b(?:0|no) (?:[a-z\-]+ )?"
                       r"(?:file|snippet|page|component|token|doc|rule|path|meta|specimen|"
                       r"artefact|item|tranche|css|html)\(s\)")
# THE SUBJECT TEST, anchored. A failure message mentions plenty of paths — the glob it scanned,
# the files it graded, the rule it cites. Only the paths in a MISSING-language clause answer the
# packaging question, so the sentence context is part of the needle: matching bare path-shapes
# called `_validate_token_forks.py` repo-bound off the line "glob: knowledge/canon/*.css", which
# is the file it successfully READ [[unmatched-grep-is-not-an-absence]], other direction.
MISSING_LINE = re.compile(r"does not exist|not found|cannot read|no such file|UNPARSEABLE|"
                          r"missing|nothing to check|could not (?:find|read|open)", re.I)
PATHISH = re.compile(r"((?:knowledge|showroom|reviews|notes|runs|memento-package|"
                     r"designer-skills-v[12]|projects|archive)/[A-Za-z0-9_.\-]+"
                     r"(?:/[A-Za-z0-9_.\-]+)*"
                     r"|GOOD-MORNING\.md|_LIVE-STATE\.md|_CHAIN\.md|_rulings\.json|_state\.json)")


def _refusal_dep(blob):
    """Name what a COULD-NOT-ASK refusal says is missing, in the REFUSAL'S OWN WORDS."""
    line = next((l for l in blob.split("\n") if "COULD-NOT-ASK" in l), "")
    for cmd in REFUSAL_REMEDY.findall(line or blob):
        if "install" in cmd:
            return cmd
    return "something this box does not have — see the refusal"


def classify(rc, out, err, shipped):
    """The verdict classifier. Reads the RUN, never the source."""
    blob = (out or "") + "\n" + (err or "")
    if rc == 124:
        return "REPO-BOUND", "timed out in the staged pack (>%ds) — it is walking something " \
                             "the pack does not carry" % PROBE_TIMEOUT
    m = MODNOTFOUND.search(blob)
    if m:
        name = m.group(1).split(".")[0]
        if name in STD:
            return "REPO-BOUND", "stdlib module %r unavailable — environment, not the pack" % name
        return "NEEDS-DEP", name
    # ⛔ s223-D5 clause (1) — THE EXIT-77 ARM. A gate that exits 77 has REFUSED: it did not reach
    # a verdict, it said the question was unaskable on this box. Without this arm such a run fell
    # through to "ran, verdict FAIL — a verdict is a run" (RUNNABLE), so a refusal was recorded as
    # a red, and the differential arm below could call it "a live red". Measured at #223: the
    # browser gates, once repaired to refuse honestly instead of crashing, classified by whether
    # the PROBE MACHINE happened to have chromium installed. NEEDS-DEP is the existing vocabulary
    # for exactly this — the gate ships, and the missing thing is named beside it. Kept BELOW the
    # MODNOTFOUND arm on purpose: a refusal that names a module still gets classified by that
    # module's name, which is more precise than the remedy sentence.
    if rc == REFUSAL_EXIT:
        return "NEEDS-DEP", _refusal_dep(blob)
    if TRACE in blob:
        pm = PATHERR.search(blob)
        if pm:
            missing = pm.group(1)
            short = missing.replace(os.sep, "/")
            for s in shipped:
                if short.endswith(s):
                    return "RUNNABLE", "reached a verdict (path error inside the shipped set)"
            return "REPO-BOUND", "reaches for %s, which the pack does not ship" % _tail(short)
        first = [l for l in blob.strip().split("\n") if l.strip()]
        return "REPO-BOUND", "crashed: %s" % (first[-1][:160] if first else "unknown")
    if rc == 0:
        return "RUNNABLE", "ran clean, verdict PASS"
    if ARGS_REFUSAL.search(blob):
        return "RUNNABLE", "runs; it wants an explicit target and refuses without one — a " \
                           "stated contract, not a fence"
    # THE SUBJECT TEST. A clean FAIL is a verdict — unless the message says the thing it went
    # looking for is not in the pack. That is a packaging fact, and it is readable mechanically.
    outside = []
    for line in blob.split("\n"):
        if not MISSING_LINE.search(line):
            continue
        for p in PATHISH.findall(line):
            if p not in shipped and "*" not in p:
                outside.append(p)
    if outside:
        return "REPO-BOUND", "runs, but its verdict is about %s, which the pack does not ship" \
                             % _tail(outside[0])
    return "RUNNABLE", "ran, verdict FAIL (exit %d) — a verdict is a run" % rc


FLAG_REJECTED = ("cannot read %s", "unrecognized arguments: %s", "no such file or directory: '%s'",
                 "unknown argument '%s'", "invalid argument %s")


def flag_rejected(flag, text):
    """Did the gate read the declared flag as a FILENAME (or refuse it) rather than as a flag?

    The failure this catches is specific and was MEASURED: a gate whose copy at some commit has
    no `--check` arm reads `--check` as a path and reports `cannot read --check: [Errno 2]` — an
    argument error dressed as a verdict. Matching is on the flag NEXT TO an error phrase, never
    on the flag alone: a gate that legitimately prints its own flag in a summary line must not
    trip this [[unmatched-grep-is-not-an-absence]], in its mirror form.
    """
    low = text.lower()
    return any((tpl % flag.lower()) in low for tpl in FLAG_REJECTED)


def _tail(p, n=3):
    """Name the path the way the DESIGNER will see it, not the way the probe staged it.
    The probe extracts into <tmp>/pack/, so a raw traceback path reads
    `/var/tmp/packprobe-xxxx/pack/knowledge/_state.json` — and `pack/knowledge/_state.json` on
    Dave's page is a directory that exists nowhere. Strip the stage, keep the repo path."""
    if "/pack/" in p:
        p = p.split("/pack/")[-1]
    parts = [x for x in p.split("/") if x]
    return "/".join(parts[-n:]) if len(parts) > n else p


PROBE_TIMEOUT = 25


def probe_gates(sha, stage_root=None, only=None, verbose=False, full_stage=None):
    """Materialise the non-gate shipped set in a throwaway dir, then RUN each gate in it."""
    paths = tree_paths(sha)
    tbl = groups()
    claimed = {}
    for p in paths:
        for g in tbl:
            if g["match"](p):
                claimed.setdefault(g["key"], []).append(p)
                break
    gate_paths = sorted(claimed.get("gates", []))
    non_gate = sorted(p for k, v in claimed.items() if k != "gates" for p in v)

    knowledge_files = {os.path.basename(p) for p in paths if os.path.dirname(p) == "knowledge"}

    tmp = stage_root or tempfile.mkdtemp(prefix="packgateprobe-", dir="/var/tmp")
    stage = os.path.join(tmp, "pack")
    if not os.path.isdir(stage):
        os.makedirs(stage, exist_ok=True)
        extract(sha, non_gate + GATE_DATA_CANDIDATES, stage, tolerant=True)

    shipped = set(non_gate)
    results = []
    for gp in gate_paths:
        base = os.path.basename(gp)
        if only and base not in only:
            continue
        src = git("show", "%s:%s" % (sha, gp))
        loc, third = local_imports(src, knowledge_files)
        # copy the gate + its local helper closure into the stage
        copied = [gp]
        frontier = set(loc)
        seen = set()
        while frontier:
            m = frontier.pop()
            if m in seen:
                continue
            seen.add(m)
            home = HELPER_HOMES.get(m, "knowledge/%s.py" % m)
            if home in paths:
                copied.append(home)
                l2, _ = local_imports(git("show", "%s:%s" % (sha, home)), knowledge_files)
                frontier |= (l2 - seen)
        extract(sha, copied, stage, tolerant=True)

        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR="/var/tmp",
                   PYTHONPATH=os.path.join(stage, "knowledge"))
        r = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp],
                           cwd=stage, capture_output=True, env=env)
        out, err = r.stdout.decode("utf8", "replace"), r.stderr.decode("utf8", "replace")
        invocation = DECLARED_INVOCATIONS.get(base, "")
        if invocation:
            r2 = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp, invocation],
                                cwd=stage, capture_output=True, env=env)
            o2 = r2.stdout.decode("utf8", "replace")
            e2 = r2.stderr.decode("utf8", "replace")
            if flag_rejected(invocation, o2 + e2):
                # THE DECLARED INVOCATION IS A CLAIM AND THE PROBE CHECKS IT. At a commit whose
                # copy of this gate has no such flag, the flag is read as a FILENAME and the
                # verdict becomes an argument error — a worse red than the honest one, invented
                # by the table. So the claim falls back to the measured bare run and says so.
                invocation = ""
            else:
                r, out, err = r2, o2, e2
        if "REFUSED (write-gate)" in out + err:
            invocation = "--write"
        elif ARGS_REFUSAL.search(out + err) and "--all" in (out + err):
            invocation = "--all"
        if invocation:
            r = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp, invocation],
                               cwd=stage, capture_output=True, env=env)
            out, err = r.stdout.decode("utf8", "replace"), r.stderr.decode("utf8", "replace")
        verdict, why = classify(r.returncode, out, err, shipped)
        # ⛔ THE VACUOUS-PASS ARM. `_validate_no_hardcode.py` exits 0 with "passed (0 tranche
        # file(s))" — it graded NOTHING and called it green. In the pack that is correct and
        # expected (the tranche dir is the DESIGNER's work, which does not exist yet), but a
        # green that graded zero must never be presented as a green that graded something
        # [[green-tests-cannot-see-scope]]. So the population is measured from the gate's own
        # output and DECLARED beside its verdict.
        population = ""
        if verdict == "RUNNABLE" and r.returncode == 0:
            population = "EMPTY-IN-PACK" if EMPTY_POP.search(out + err) else "graded"
        fail_head = ""
        differential = ""
        if verdict == "RUNNABLE" and r.returncode != 0:
            lines = [l.strip() for l in (out + "\n" + err).split("\n") if l.strip()]
            fail_head = " / ".join(lines[:3])[:300]
            if full_stage:
                fr = subprocess.run(
                    ["timeout", str(PROBE_TIMEOUT), sys.executable, gp]
                    + ([invocation] if invocation else []),
                    cwd=full_stage, capture_output=True,
                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR="/var/tmp",
                             PYTHONPATH=os.path.join(full_stage, "knowledge")))
                fout = (fr.stdout + fr.stderr).decode("utf8", "replace")
                if fr.returncode == 0:
                    differential = "full-tree PASS"
                    verdict = "REPO-BOUND"
                    why = ("runs, but its subject is not in the pack — it is GREEN against the "
                           "full repo and RED here: " + (fail_head[:140] or "no message"))
                elif TRACE in fout:
                    differential = "full-tree CRASH"
                else:
                    differential = "full-tree FAIL too"
                    why = ("ran, verdict FAIL in the pack AND in the full repo — a live red, "
                           "not a packaging fence: " + (fail_head[:140] or "no message"))

        # the selftest arm — does the gate prove it can BITE without repo data?
        st = subprocess.run(["timeout", str(PROBE_TIMEOUT), sys.executable, gp, "--selftest"],
                            cwd=stage, capture_output=True, env=env)
        sout = (st.stdout + st.stderr).decode("utf8", "replace")
        if "unrecognized" in sout or "usage:" in sout.lower() and st.returncode == 2:
            selftest = "none"
        elif st.returncode == 0:
            selftest = "green"
        elif TRACE in sout or "No module named" in sout:
            selftest = "crashed"
        else:
            selftest = "red"

        results.append(dict(
            gate=base, path=gp, verdict=verdict, why=why,
            third_party=sorted(third), local_imports=sorted(seen),
            invocation=invocation, selftest=selftest, exit=r.returncode,
            fail_head=fail_head, differential=differential, population=population,
        ))
        if verbose:
            print("%-42s %-12s %s" % (base, verdict, why), flush=True)
    return dict(commit=sha, timeout_s=PROBE_TIMEOUT, gates=results), tmp


def extract(sha, paths, dest, tolerant=False):
    """git archive the named paths at the named commit into dest. Bytes come from the COMMIT."""
    paths = [p for p in paths if p]
    if not paths:
        return
    if tolerant:
        have = set(tree_paths(sha))
        paths = [p for p in paths if p in have]
        if not paths:
            return
    os.makedirs(dest, exist_ok=True)
    for i in range(0, len(paths), 400):
        chunk = paths[i:i + 400]
        ar = subprocess.run(["git", "archive", "--format=tar", sha, "--"] + chunk,
                            cwd=ROOT, capture_output=True)
        if ar.returncode != 0:
            raise RuntimeError("git archive failed: " + ar.stderr.decode()[:400])
        tr = subprocess.run(["tar", "-x", "-C", dest], input=ar.stdout, capture_output=True)
        if tr.returncode != 0:
            raise RuntimeError("tar failed: " + tr.stderr.decode()[:400])


PACK_SURFACE_PREFIX = "apollo-spider/"

# ---------------------------------------------------------------------------------------------
# THE SEED MAP (#219 N3, s219-D5(Q1)). One prefix, and it exists because of a MEASUREMENT, not
# a preference: every piece of Memento machinery resolves its own homes from where the FILE sits.
#
#   _gen_chain.py    writes `_CHAIN.md` into `dirname(dirname(__file__))`
#   _state.py        reads `_state.json` from its OWN dir, and resolves `home` against the parent
#   _inscribe_ruling reads `_rulings.json` from its OWN dir
#   _governs.py      resolves an evidence PATH against `dirname(dirname(__file__))`
#
# The Gumdrop cut's chain root is therefore `memento-package/` (that is where the shipped
# `_gen_chain.py` will write), and the record machinery has to sit ONE level above `machinery/`
# so its parent is the PACK ROOT — otherwise a designer's ruling that cites a real file
# (`knowledge/tokens/…`, `showroom/…`) is refused as "path does not exist", because the
# resolver would be looking inside `memento-package/`. Measured, this session, both ways.
#
# The repo keeps these files under `apollo-spider/gumdrop/` — they are RELEASE surface, and the
# repo's own `memento-package/` is a separate, frozen package whose delta gate fails loud on any
# file it does not know (`_validate_package_delta.py`, arm 4). So the stage MOVES them, and
# `pack_path` is still the ONE function both the stager and `--check` read, exactly as the
# flatten is. Order matters: the seed map is consulted BEFORE the flatten, or `apollo-spider/`
# would claim these paths first and land them at the pack root.
SEED_PREFIXES = (("apollo-spider/gumdrop/", "memento-package/"),)


def pack_path(p):
    """Repo path -> path inside the pack root.

    #219 stage 2, conductor-authorised (R3 Q2 + seam 7's stage-1 flag). The pack's OWN
    surfaces — skills/, ci-template/ — live under apollo-spider/ in the REPO, but a
    designer who unzips the pack must find skills/ at the root, not nested two levels down
    as Apollo-Spider-v1.0.0/apollo-spider/skills/. R3's consequence note:
    "most will not find the skills at all. That is a silent failure of the whole release."
    So the bake's stage flattens that ONE prefix, and check_pack verifies through the SAME
    mapping — one function, both directions, so the stager and the checker cannot disagree
    about the layout. Everything else (knowledge/, showroom/, memento-package/) already
    sits at the root and passes through unchanged.
    """
    for src, dst in SEED_PREFIXES:
        if p.startswith(src):
            return dst + p[len(src):]
    return p[len(PACK_SURFACE_PREFIX):] if p.startswith(PACK_SURFACE_PREFIX) else p


def apply_seed_map(stage):
    """Move the seed-mapped subtrees into place, BEFORE the flatten.

    Merges into a destination directory that already exists (the Gumdrop cut lands beside the
    frozen `memento-package/` files, which is the whole point) but REFUSES on a file collision
    rather than overwriting either side — same discipline as `flatten_stage`."""
    for src, dst in SEED_PREFIXES:
        s_root = os.path.join(stage, src.rstrip("/"))
        if not os.path.isdir(s_root):
            continue
        for root, _dirs, files in os.walk(s_root):
            for name in files:
                sp = os.path.join(root, name)
                rel = os.path.relpath(sp, s_root)
                dp = os.path.join(stage, dst.rstrip("/"), rel)
                if os.path.exists(dp):
                    raise RuntimeError("seed collision: %r already exists at the stage"
                                       % os.path.join(dst, rel))
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                os.rename(sp, dp)
        shutil.rmtree(s_root)


def flatten_stage(stage):
    """Move the stage's apollo-spider/ contents to the stage root (the pack_path layout).
    Refuses on a name collision rather than silently overwriting either side."""
    nested = os.path.join(stage, PACK_SURFACE_PREFIX.rstrip("/"))
    if not os.path.isdir(nested):
        return
    for entry in sorted(os.listdir(nested)):
        dst = os.path.join(stage, entry)
        if os.path.exists(dst):
            raise RuntimeError("flatten collision: %r already exists at the stage root" % entry)
        os.rename(os.path.join(nested, entry), dst)
    os.rmdir(nested)


# ---------------------------------------------------------------------------------------------
# THE IMPORT CLOSURE (#220, at cause on the v1.0.0 defect)
#
# ⛔ WHAT WENT WRONG, AND WHY IT WAS A DECISION AND NOT A FILE. v1.0.0 shipped
# `memento-package/claude-plugin/memento/machinery/_gen_chain.py`, and it dies on import:
# `ModuleNotFoundError: No module named '_could_not_ask'`. Its sibling copy at
# `memento-package/machinery/` runs, because the SEED MAP above lands
# `apollo-spider/gumdrop/machinery/_could_not_ask.py` there — and only there. The package delta
# gate was GREEN over the difference, because it compares paths and bytes and never asks whether
# either copy runs. So the pack shipped a chain generator a Gumdrop designer cannot start.
#
# The closure that already existed was `helper_closure` in build_manifest, and it is exactly the
# right idea in the wrong scope: it is keyed on the GATE PROBE (only files the probe ran), and it
# resolves every helper into `knowledge/` (`HELPER_HOMES`). A module packed anywhere else — the
# whole memento cut, the gumdrop cut — is outside its reach. Copying one file into one directory
# would have been a plaster that recurs at v1.0.2 [[gate-dont-patch]].
#
# THE DECISION, RESTATED: *any* module a packed `.py` imports AT MODULE LEVEL must be reachable
# from where that file lands IN THE PACK. Not in the repo — the repo copy of `_gen_chain.py` is
# equally broken and nobody noticed, because in the repo nobody runs it from there.
#
# HOW RESOLUTION IS MODELLED, and where the model stops. Python finds a module on `sys.path`, so
# the model reads the roots each file actually declares:
#   · its own directory (every one of these files does `sys.path.insert(0, HERE)`);
#   · any `sys.path.insert/append` whose argument is a `__file__`-rooted expression this module
#     can evaluate — `os.path.dirname`, `os.path.abspath`, `os.path.join` over string literals
#     and module-level names it has already seen;
#   · the help-gate preamble, which is a WHILE LOOP searching upward for `_helpgate.py` and is
#     recognised as the idiom it is: the root is the nearest ancestor directory holding it.
# An insert this evaluator cannot read is COUNTED and REPORTED as `unmodelled`, never assumed
# harmless [[measuring-tool-must-not-guess]]. The static model is deliberately the cheap half:
# `knowledge/_gate_pack_imports.py` is the expensive half and it actually imports the files from
# a stage, which is the only reading that cannot be wrong about `sys.path`.
# ---------------------------------------------------------------------------------------------

_HELPGATE_IDIOM = "_hg_sys.path.insert"     # the repo-wide help-gate preamble, byte-stable
_UNKNOWN = object()


def _eval_pathish(node, env, selfdir):
    """Evaluate a `__file__`-rooted path expression, or return _UNKNOWN. No exec, no import."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        if node.id == "__file__":
            return selfdir + "/__self__.py"
        return env.get(node.id, _UNKNOWN)
    if isinstance(node, ast.Call):
        f, dotted = node.func, []
        while isinstance(f, ast.Attribute):
            dotted.append(f.attr)
            f = f.value
        if isinstance(f, ast.Name):
            dotted.append(f.id)
        name = ".".join(reversed(dotted))
        args = [_eval_pathish(a, env, selfdir) for a in node.args]
        if any(a is _UNKNOWN for a in args) or not args:
            return _UNKNOWN
        if name in ("os.path.abspath", "os.path.realpath"):
            return args[0]
        if name == "os.path.dirname":
            return os.path.dirname(args[0])
        if name == "os.path.join":
            return os.path.join(*args)
    return _UNKNOWN


def analyse_imports(src, packdir):
    """(module-level imported names, sys.path roots in PACK space, unmodelled-insert count).

    Module level ONLY, plus the bodies of top-level `try`/`if`/`while` — that is the set whose
    failure makes the FILE unimportable, which is the defect class. An import inside a function
    is a runtime question and is declared as out of scope rather than half-modelled."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set(), set(), 0
    env, roots, mods = {}, set(), set()
    unmodelled = [0]
    hg = _HELPGATE_IDIOM in src

    def visit(n):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            v = _eval_pathish(n.value, env, packdir)
            if v is not _UNKNOWN:
                env[n.targets[0].id] = v
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call):
            c, f, dotted = n.value, n.value.func, []
            while isinstance(f, ast.Attribute):
                dotted.append(f.attr)
                f = f.value
            if isinstance(f, ast.Name):
                dotted.append(f.id)
            nm = ".".join(reversed(dotted))
            if nm.endswith("path.insert") or nm.endswith("path.append"):
                v = _eval_pathish(c.args[-1], env, packdir) if c.args else _UNKNOWN
                if v is _UNKNOWN:
                    # The help-gate's own insert is UNKNOWN by construction (its variable is
                    # rebound inside the search loop) and it is modelled below, by name.
                    if not (hg and nm.startswith("_hg_sys")):
                        unmodelled[0] += 1
                else:
                    roots.add(os.path.normpath(v).lstrip("/"))
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module and n.level == 0:
                mods.add(n.module.split(".")[0])

    for n in tree.body:
        visit(n)
        if isinstance(n, (ast.Try, ast.If, ast.While)):
            for sub in ast.walk(n):
                if sub is not n:
                    visit(sub)
    roots.add(packdir)
    return mods, roots, unmodelled[0]


def import_closure(paths, read_blob):
    """What must be SEEDED so every packed module's module-level imports travel with it.

    `paths` are REPO paths; `read_blob(repo_path) -> str` supplies the bytes AT THE COMMIT (never
    the working tree — the whole bake is a function of a named commit). Returns
    (seeds, unmodelled, unsourced): seeds are dicts {module, dest, src, needed_by}, `dest` a PACK
    path, `src` the REPO path whose blob fills it. A module nobody in the pack carries lands in
    `unsourced` and the caller REFUSES — a closure that silently gives up is the blind gate again.
    """
    pk = {}
    for p in paths:
        pk[pack_path(p)] = p
    by_dir, by_base = {}, {}
    for q in pk:
        by_dir.setdefault(os.path.dirname(q), set()).add(os.path.basename(q))
        by_base.setdefault(os.path.basename(q), []).append(q)

    seeds, unsourced, unmodelled = {}, [], 0
    for q in sorted(pk):
        if not q.endswith(".py"):
            continue
        src = read_blob(pk[q])
        d = os.path.dirname(q)
        mods, roots, um = analyse_imports(src, d)
        unmodelled += um
        if _HELPGATE_IDIOM in src:
            a = d
            while True:
                if "_helpgate.py" in by_dir.get(a, set()):
                    roots.add(a)
                    break
                if not a:
                    break
                a = os.path.dirname(a)
        for m in sorted(mods):
            fn = m + ".py"
            if fn not in by_base:
                continue                              # stdlib, third party, or simply not ours
            if any(fn in by_dir.get(r, set()) for r in roots):
                continue                              # already reachable where it lands
            dest = os.path.join(d, fn)
            # The NEAREST carrier in pack space wins: a memento module is filled from the memento
            # copy, not from knowledge/. Deterministic — longest shared prefix, then sort order.
            cands = sorted(by_base[fn],
                           key=lambda c: (-len(os.path.commonprefix([c, q])), c))
            if not cands:
                unsourced.append((q, m))
                continue
            e = seeds.setdefault(dest, dict(module=m, dest=dest, src=pk[cands[0]], needed_by=[]))
            e["needed_by"].append(q)
    for e in seeds.values():
        e["needed_by"] = sorted(set(e["needed_by"]))
    return [seeds[k] for k in sorted(seeds)], unmodelled, sorted(unsourced)


def apply_closure(stage, seeds):
    """Materialise the closure ON THE STAGE, from bytes ALREADY IN THE STAGE.

    ⛔ The fill never comes from the working tree. Its source is the same blob the commit put at
    `pack_path(src)`, so a closure copy is byte-identical to the file it mirrors and `check_pack`
    can verify it against the commit like every other path."""
    for s in seeds:
        src = os.path.join(stage, pack_path(s["src"]))
        dst = os.path.join(stage, s["dest"])
        if not os.path.exists(src):
            raise RuntimeError("closure source missing from the stage: %r (for %r)"
                               % (pack_path(s["src"]), s["dest"]))
        if os.path.exists(dst):
            raise RuntimeError("closure collision: %r already exists at the stage" % s["dest"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)


# ---------------------------------------------------------------------------------------------
# THE COMPANION CLOSURE (#220 addendum) — the same sentence as the import closure, one clause
# wider, for a dependency no parser can see.
#
# ⛔ WHAT WENT WRONG. v1.0.1's stage shipped `_memento_search.py` — the Memento door, which the
# pack's own README and memento-boot skill both tell a designer to use — and running it from a
# fresh stage gives:
#
#     memento-search (Memento door): index missing at …/machinery/_memento-index.json
#       — run the build (python3 knowledge/_build_all.py); REFUSING to search nothing.
#
# and `knowledge/_build_all.py` is not in the pack. Retrieval, one of the two things Memento IS,
# could not be started in a Gumdrop project at all.
#
# ⚠ WHY THE POINTER IS NOT THE DEFECT, MEASURED. `_build_all.py` is named at 80 sites across 38
# packed files, and `memento-package/machinery/_MACHINERY-MANIFEST.md` rules the reason: the cut
# is "VERBATIM copies — Apollo names … are still inside them, on purpose … Generalisation is a
# build step, not a copy step; a half-renamed copy would be neither auditable nor runnable."
# A mechanical strip or repoint IS that half-rename. And Apollo's own
# `knowledge/_build_memento_index.py` cannot be the thing the closure carries: driven in a fresh
# stage it dies on `_gen_lanes`, and its declared corpus is the whole Apollo memory (GM/LS
# archives, gauge log, decisions ledger, briefs, lanes, component registry), which it REFUSES to
# build without. A closure carries files; it cannot carry a corpus.
#
# THE DECISION. The pack's OWN generalisation-debt list, item 3, is "Index bootstrap for a fresh
# project (the no-chain arm of the ratified boot rule)". The Gumdrop cut now carries that
# bootstrap (`apollo-spider/gumdrop/machinery/_build_memento_index.py`), and this closure states
# the packaging half: A PACKED DOOR TRAVELS WITH ITS BUILDER. The seed map lands the bootstrap in
# `memento-package/machinery/` and ONLY there — exactly the v1.0.0 shape that left the plugin
# mirror's `_gen_chain.py` unimportable — so the mirror is filled the same way, from bytes already
# in the stage.
#
# ⚠ WHY IT IS DECLARED AND NOT DERIVED. `import_closure` can read an `import` statement. Nothing
# static can read "this tool refuses until you run that other tool": the dependency lives in a
# runtime refusal string. So the pair is DECLARED here, with its reason, and the generator REFUSES
# if the named companion is carried nowhere — the same refusal the import closure makes, for the
# same reason [[instrument-without-a-consumer]].
DOOR_COMPANIONS = (
    ("_memento_search.py", "_build_memento_index.py",
     "the Memento door REFUSES until its index exists, and only this builder writes one"),
)


def companion_closure(paths):
    """Declared companions that must sit beside a packed door wherever that door lands.

    Same seed shape as `import_closure` (so `apply_closure`, the manifest block, `--stage` and
    `check_pack` all read one list), and the same nearest-carrier-in-pack-space fill rule.
    Returns (seeds, unsourced)."""
    pk = {}
    for p in paths:
        pk[pack_path(p)] = p
    by_dir, by_base = {}, {}
    for q in pk:
        by_dir.setdefault(os.path.dirname(q), set()).add(os.path.basename(q))
        by_base.setdefault(os.path.basename(q), []).append(q)

    seeds, unsourced = {}, []
    for door, companion, why in DOOR_COMPANIONS:
        for q in sorted(pk):
            if os.path.basename(q) != door:
                continue
            d = os.path.dirname(q)
            if companion in by_dir.get(d, set()):
                continue                              # already beside it
            cands = sorted(by_base.get(companion, []),
                           key=lambda c: (-len(os.path.commonprefix([c, q])), c))
            if not cands:
                unsourced.append((q, companion))
                continue
            dest = os.path.join(d, companion)
            e = seeds.setdefault(dest, dict(module=os.path.splitext(companion)[0], dest=dest,
                                            src=pk[cands[0]], needed_by=[], why=why))
            e["needed_by"].append(q)
    for e in seeds.values():
        e["needed_by"] = sorted(set(e["needed_by"]))
    return [seeds[k] for k in sorted(seeds)], sorted(unsourced)


# ---------------------------------------------------------------------------------------------
# THE MANIFEST
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# THE FIVE CARDS — and, since `s219-D5`, THEIR ANSWERS.
#
# Every card below was put to Dave on this page and every one of them came back answered in
# `s219-D5`. The card is NOT deleted when it is answered: the question is the reason the answer
# is legible, and a decision surface that erases what was asked leaves the answer floating. So
# each answered card carries an `answered` block — the ruling that settles it, his position in
# his own words, and (where a lane has enacted it) what the pack now does.
#
# ⛔ AN ANSWERED CARD STOPS ASKING. The renderer paints no radio input on an answered card and
# moves it out of the "only you can settle" section, whose count is DERIVED from the unanswered
# set. A page that keeps offering a settled choice is [[dont-launder-a-premise-into-a-ruling]]
# printed at 15.5px on the surface Dave rules from.
#
# ⚠ TRANSCRIBED, NOT DECIDED (#219 N1 scope note). Q2 and Q3 are this lane's clauses and their
# `enacted` lines are measured here. Q1, Q4 and Q5 carry his ruling and NO enactment claim —
# their work belongs to other lanes, and stating the position is a record, not a promotion.
OPEN_QUESTIONS = [
    dict(id="Q1", title="Memento ships machinery with no store — does the pack hand designers an "
                        "EMPTY record to fill?",
         body="I checked, because the brief asked. memento-package ships five machinery files "
              "and a lexicon, and it ships no record at all — no chain, no rulings store, no "
              "task store, not even an empty one. Its own manifest says why: every adopting "
              "project grows its own chain.||"
              "Mirroring that exactly means a designer unzips the pack, says good morning, and "
              "Memento has nowhere to write.||"
              "The proposal, if you want them productive on day one: ship three empty stores "
              "with the right shape and nothing inside. A task store holding an empty list. A "
              "rulings store holding an empty list. And no chain file at all — its absence is "
              "the signal the boot rule reads to know this is a new project.||"
              "An empty shape is machinery. A filled shape is your record. The line you drew "
              "holds either way. The only question is whether the designer types the first "
              "brace or we do.",
         options=["Mirror memento exactly — no stores, the pack's first run creates them",
                  "Ship the three empty store shapes (recommended)",
                  "Ship empty stores AND a starter _CHAIN.md explaining the first move"],
         answered=dict(
             ruling="s219-D5 (Q1)",
             position="Empty stores ship, plus a starter _CHAIN.md explaining the first move — "
                      "and the cold start itself is part of the release: “I think we need to "
                      "work on the UX of Memento on a cold strts and really guide the designers "
                      "through the first chat.”")),
    dict(id="Q2", title="Do the licensed desktop fonts travel in the zip?",
         body="The library only looks like Apollo in the real face. The desktop cut is tracked "
              "in this repo on purpose — the .gitignore says why: the repo is private and "
              "shared only in-licence.||"
              "A zip on GitHub is a wider audience than the repo. If your designers sit inside "
              "the same licence, the fonts ride along and the showroom renders correctly. If "
              "they do not, the pack ships without them and the library falls back to a stock "
              "face. It still works. It does not look right.||"
              "Eight of the thirty-four megabytes are the fonts, so this is also the single "
              "biggest lever on download size.",
         options=["Ship the desktop fonts (54 files) — designers are in-licence",
                  "Leave the fonts out and note the fallback in the pack README"],
         answered=dict(
             ruling="s219-D5 (Q2)",
             position="The 54 licensed desktop fonts SHIP. His words: “designers are "
                      "in-licence” — the same licence position that makes the desktop cut "
                      "tracked in this private repo covers the designers the pack goes to. "
                      "The webfont packs stay out; that fence is unmoved.",
             enacted="Shipped by the library group's rule over "
                     "knowledge/assets/fonts/_desktop/ — the count on this card is read out of "
                     "the manifest, not typed, so it cannot drift from what the zip carries.")),
    dict(id="Q3", title="Do the canon GENERATORS ship, or only the canon they produce?",
         body="The canon folder holds canon.css and type.css — and the four generators that "
              "mint them from the tokens.||"
              "v2 shipped the stylesheets only: a baked reference that nobody regenerates. You "
              "asked for as close to what you use as possible, and what you use is the "
              "generator.||"
              "Shipping them means a designer can change a token and re-mint canon. It also "
              "means they can produce canon that never passed a gate. The gates are in the "
              "pack too, which is why I lean towards shipping them.",
         options=["Ship the generators (the pack is the working engine — recommended, the gates are "
                  "in the pack too)",
                  "Ship the minted CSS only, v2-style"],
         answered=dict(
             ruling="s219-D5 (Q3)",
             position="The canon generators SHIP — “v3 is the working engine, the gates are in "
                      "the pack too” — WITH an explicit warning when a designer attempts one.",
             enacted="The warning fires IN THE PACK ONLY. Each of the four canon generators "
                     "asks _helpgate.pack_gate() whether it is running inside an unzipped pack "
                     "(a _MANIFEST.json carrying this schema, sitting beside knowledge/). In "
                     "this repo that marker does not exist and the call is a no-op, so nothing "
                     "here changes. In the pack it prints his own framing — changing a token "
                     "and re-minting canon can produce canon that never passed a gate — and "
                     "refuses until the designer passes --i-understand. Nothing is injected at "
                     "bake time: the file in the zip is byte-identical to the file in the "
                     "repo, which is what keeps the pack audit able to check it at all.")),
    dict(id="Q4", title="Which runbooks are design-facing and which are yours?",
         body="Eleven runbooks are proposed in, as design-facing. Seven are held out as your "
              "own working ritual: capture, git commit, the context gauge, the parallel "
              "conductor, the dream pass, decision audit, densify-adversarial.||"
              "memento-package itself ships no runbooks at all — machinery only — so mirroring "
              "it holds all seven out, and that is what the list currently does.||"
              "One is awkward. Capture is the ritual that makes Memento work. A designer with "
              "the machinery and no capture ritual has a chain that never grows.",
         options=["Hold all seven out (mirrors memento-package exactly)",
                  "Send capture-ritual across with the Memento half (recommended)",
                  "Send capture-ritual and context-gauge across"],
         answered=dict(
             ruling="s219-D5 (Q4)",
             position="capture-ritual AND context-gauge both cross — CUSTOMISED for the "
                      "designers' environment. His words: “remember the designers will be "
                      "running this in VS-code with co-pilot, I think we should ship this but "
                      "customised for their environment.” That also sets the pack's target "
                      "environment: VS Code + Copilot, on memento-package's "
                      "copilot-instructions.md precedent.")),
    # ---------------------------------------------------------------------------------------
    # #219 seam 7, on R2's Q1 (and R3's Q6 — the two lanes found the same thing from opposite
    # ends and both asked for a card). Dave is shown "39 gates that run anywhere" a few inches
    # further up this page. FOUR OF THEM ARRIVE RED, on a fresh unzip, before the designer has
    # written a line. That was in two filed reports and nowhere on his surface. This card
    # DECIDES NOTHING — deliberately no option is marked recommended, because which way this
    # goes is a positioning call about the first thing an outside designer ever sees.
    # ⚠ The four gate names below are checked against the repo by a selftest bite: a renamed
    # gate must break the bite rather than leave this card quietly lying (R3's finding 9).
    dict(id="Q5", title="Four of the packed gates are RED the day the pack is unzipped. "
                        "Ship them anyway, or clear them first?",
         body="Measured, not guessed — the gates were run out of an extracted pack from a "
              "directory that is not this repo, twice, by two different lanes: 32 pass, 4 fail. "
              "None of the four has anything to do with a designer's work. They are Apollo's "
              "own open reds at the commit the pack is cut from.||"
              "_validate_evidence.py — exits 2, which is bad arguments rather than a verdict. "
              "It needs a rows file handed to it and the pack's runner gives it none, so as the "
              "pack invokes it, it can never pass.||"
              "_validate_token_forks.py — three token forks are not in the ledger.||"
              "_validate_type_blast_radius.py — one selector, .search input, has escaped its "
              "declared radius.||"
              "_validate_type_composites.py — 664 composite violations inside the pack, 1,091 "
              "in this repo. That is the standing type-composite debt, which by your own ratchet "
              "may only ever shrink.||"
              "Why it matters more than the number looks: a designer unzips the pack, runs the "
              "gates exactly as the README and the new gate-runner skill tell them to, and is "
              "met with hundreds of violations they did not cause. The likely conclusion is that "
              "the gates are noise — and that conclusion is formed on day one and does not get "
              "revisited.||"
              "The middle option exists and works: a baseline file records today's reds so only "
              "the DIFFERENCE is the designer's, and the reds are still printed rather than "
              "hidden. It is built and mutation-tested, and it is deliberately NOT wired on, "
              "because switching it on is a decision about what the pack claims, not a "
              "mechanical default.",
         options=["Fix the four before the bake — cut the pack from a commit whose own gates are green",
                  "Ship them with the baseline switched on — reds recorded, printed, and only "
                  "new ones fail the designer's build",
                  "Ship them red and documented — the pack README names the four, the skill "
                  "tells designers to subtract them"],
         answered=dict(
             ruling="s219-D5 (Q5)",
             position="Fix the four BEFORE the bake — “cut v3 from a commit whose own gates are "
                      "green”. Each at cause: a missing gate-state file in the stage is SHIPPED, "
                      "not baselined away; a real defect is repaired; no baseline plaster. The "
                      "baseline machinery stays built and stays unwired.")),
    # ---------------------------------------------------------------------------------------
    # #219 seam 8 § ⑨ Q1, put on Dave's surface at stage 2. Answering Q5 at cause changed WHAT
    # THE PACK SHIPS, and the change arrived as a CONSEQUENCE rather than as a decision: the
    # honest reclassification of `_validate_evidence.py` to REPO-BOUND drops it and its helper
    # out of the ship list. `s219-D4(2)` makes the cut Dave's word, so a silent −2 on his own
    # roster is exactly the thing this page exists to refuse. This card DECIDES NOTHING — no
    # option carries `recommended`, because which way it goes is a positioning call about what
    # the pack's gate roster CLAIMS, not a mechanical default. [[dont-launder-a-premise-into-a-ruling]]
    # ⚠ The two dropped filenames are held in Q6_DROPPED_GATES and bitten for existence and for
    # absence from the ship list — the card must break rather than lie if either moves.
    dict(id="Q6", title="Answering Q5 quietly took two gates OUT of the pack. The roster is "
                        "55, not 57 — is that the cut you want?",
         body="This one is a consequence, not a proposal, and that is why it is on this page. "
              "Fixing the four red gates at cause meant classifying _validate_evidence.py "
              "honestly: it RUNS fine away from this repo, but everything it has an opinion "
              "about lives in notes/_claims — your session evidence — which s219-D4(1) "
              "permanently excludes from the pack. A gate whose subject the pack does not "
              "carry is REPO-BOUND, and REPO-BOUND gates do not ship.||"
              "So it falls out, and it takes its only local helper, _claimtable.py, with it. "
              "The gate group above is measured at 55 files where the earlier proposal said "
              "57. Nothing broke and nothing is hidden: the pack's own runner is 35 pass, "
              "0 fail, 0 could-not-ask, exit 0, from a directory that is not this repo.||"
              "The honest refusal did not disappear — it MOVED, from runtime to the ship list. "
              "Before, a designer ran the linter and it refused with a 77 that said “I cannot "
              "answer this here”. Now they never see it at all.||"
              "Which is better depends on what you want the roster to mean. If the roster is "
              "“checks that can tell you something about your work”, 55 is correct and the two "
              "were noise. If the roster is “the same gates Apollo runs”, then 57 with one of "
              "them refusing honestly is the truthful picture, and the refusal is a feature — "
              "it tells a designer the check exists and why it has nothing to say to them.||"
              "This is the same seam as two other open questions: the pack runner has three "
              "verdicts where the repo has four (there is no ADVISORY), and notes/_claims is "
              "named in three places. All three are the same argument about what an honest "
              "“cannot answer” looks like in a designer's project, and they want answering "
              "together.",
         options=["Correct as it stands — 55 gates. A check with nothing to measure in a "
                  "designer's project should not be in the zip at all",
                  "Ship them anyway — 57 gates, so the pack's roster matches Apollo's, and let "
                  "the evidence linter refuse with its honest 77 in the designer's run"],
         # #219 seam 9. Dave answered this card in the session, and at stage 2 the conductor
         # INSCRIBED the clause as `s219-D9` — so the OWED register comes off the card and the
         # receipt cites the store entry that actually carries it. The card carried
         # `inscription="OWED"` + a chat citation for the interval between his word and the
         # written clause; that machinery stays below for any future uninscribed answer, and
         # the selftest now verifies this citation against the STORE itself, not this dict's
         # own text [[memento-three-registers]] [[memento-framing]].
         answered=dict(
             ruling="s219-D9",
             position="The first reading: 55 gates. The ship list carries only the gates that "
                      "can actually tell a designer something about their own work, and a "
                      "check whose whole subject is this repo's session evidence is not one of "
                      "them. The two that fall out are NOT hidden by falling out — they are "
                      "named, with their reason, in the exclusion table below, which is where a "
                      "designer looks to find out what is deliberately absent.",
             enacted="Measured at this commit, not asserted. The gates group is assembled from "
                     "the probe's own verdicts — the gates it classified RUNNABLE or NEEDS-DEP, "
                     "plus the helper modules and data files they import — so the file count on "
                     "the group card is read out of the tree and nothing on this page types the "
                     "number 55. And the two that fell out are named, by filename and with the "
                     "probe's own reason, in their own row of the exclusion table: the drop is "
                     "stated on the same page as the count it changed.")),
]

# The two gates that fell OUT of the ship list when Q5 was answered at cause (#219 seam 8 § ⑨
# Q1). Held as data for the same reason as Q5_RED_GATES: Q6's whole subject is these two files,
# and a card that names a file which has since moved lies quietly on Dave's decision surface.
Q6_DROPPED_GATES = ["_validate_evidence.py", "_claimtable.py"]

# The four gates named in Q5's body. Held as data so the selftest can prove they still exist:
# a card that names a renamed gate is the read-chain-staleness class, and it would go stale
# silently on Dave's own decision surface. [[no-gate-parses-the-artefact]]
Q5_RED_GATES = ["_validate_evidence.py", "_validate_token_forks.py",
                "_validate_type_blast_radius.py", "_validate_type_composites.py"]


def build_manifest(sha, probe):
    paths = tree_paths(sha)
    tbl = groups()
    claimed = {}
    for p in paths:
        for g in tbl:
            if g["match"](p):
                claimed.setdefault(g["key"], []).append(p)
                break

    verdicts = {r["gate"]: r for r in probe["gates"]}
    runnable = sorted(r["path"] for r in probe["gates"] if r["verdict"] == "RUNNABLE")
    needsdep = sorted(r["path"] for r in probe["gates"] if r["verdict"] == "NEEDS-DEP")
    repobound = sorted(r["path"] for r in probe["gates"] if r["verdict"] == "REPO-BOUND")

    # The gates group SHIPS the runnable ones plus the needs-dep ones (a named pip install is
    # a documented prerequisite, not a fence). Repo-bound gates are OUT, each with its reason.
    ship_gates = runnable + needsdep
    helper_closure = sorted({h for r in probe["gates"] if r["verdict"] in ("RUNNABLE", "NEEDS-DEP")
                             for m in r["local_imports"]
                             for h in [HELPER_HOMES.get(m, "knowledge/%s.py" % m)]
                             if h in paths})
    gate_data = [p for p in GATE_DATA_CANDIDATES if p in paths]

    # ---- THE CI TEMPLATE RIDES WITH THE GATES (#219 R2, s219-D4(3)). ---------------------------
    # The pack-side half of "CI both halves" is a workflow a designer copies into their own repo,
    # plus the runner it calls and a README that says what blocks and how to turn a check off
    # honestly. It belongs to the GATES group and not to a group of its own, deliberately: a
    # workflow that runs the gates is not a seventh thing to explain to Dave, it is how the gates
    # get run. ⚠ IT IS A FUNCTION OF THE COMMIT LIKE EVERY OTHER PATH — at a commit where
    # apollo-spider/ci-template/ does not yet exist this list is EMPTY and the manifest's
    # bytes are unchanged, which is exactly why adding this rule did not invalidate the manifest
    # R1 generated. It starts shipping at the commit that lands the files.
    ci_template = sorted(p for p in paths if p.startswith("apollo-spider/ci-template/"))

    # Every path is owned by exactly ONE group. The gates group pulls in helper modules and data
    # files that other groups may already own (canon/_type-bindings.json is engine-canon's, and
    # the type gates read it) — without this the totals would count them twice and the pack size
    # on Dave's page would be a number nothing produced [[measure-dont-convert-units]].
    already = set()
    out_groups = []
    seen_group = {}
    for g in tbl:
        ps = sorted(claimed.get(g["key"], []))
        if g["key"] == "gates":
            ps = sorted(set(ship_gates) | set(helper_closure) | set(gate_data) | set(ci_template))
        ps = [p for p in ps if p not in already]
        already.update(ps)
        sizes = blob_sizes(sha, ps)
        entry = dict(key=g["key"], group=g["group"], title=g["title"], plain=g["plain"],
                     files=len(ps), bytes=sum(sizes.values()), paths=ps)
        if g["key"] == "gates":
            entry["verdicts"] = [dict(gate=r["gate"], verdict=r["verdict"], why=r["why"],
                                      selftest=r["selftest"],
                                      third_party=r["third_party"],
                                      population=r.get("population", ""),
                                      invocation=r["invocation"])
                                 for r in sorted(probe["gates"], key=lambda x: x["gate"])]
            entry["counts"] = dict(
                runnable=len(runnable), needs_dep=len(needsdep), repo_bound=len(repobound),
                empty_population=sum(1 for r in probe["gates"]
                                     if r.get("population") == "EMPTY-IN-PACK"))
            # Emitted ONLY when the files exist at this commit — an empty key would change the
            # manifest's bytes for every commit before the template landed, and a ship list has
            # to be a function of the tree, not of when the generator was edited.
            if ci_template:
                entry["ci_template"] = ci_template
        if g["key"] == "skills":
            # #219 seam 7: the placeholder slot is FILLED. R3 shipped the gate-runner as
            # `check-with-gates` (its pairing with check-against-design-system is the pedagogy:
            # the mechanical half and the reading half), so the named-empty-slot emission is gone
            # rather than left to promise a file that now exists under a different name.
            entry["status"] = "refreshed at #219 R3 — four rewritten against this KB, one new"
        out_groups.append(entry)
        seen_group.setdefault(g["group"], []).append(entry)

    # ---- THE IMPORT CLOSURE (#220). Computed over the FINAL ship list, from the commit's own
    # blobs, and recorded so the stager, `check_pack` and `_gate_pack_imports.py` all read ONE
    # answer. A module the pack does not carry anywhere is a REFUSAL, not a shrug: the whole
    # point of this block is that v1.0.0 shipped an unimportable file and nothing said so.
    ship_paths = sorted({p for e in out_groups for p in e["paths"]})
    _blob_cache = {}

    def _read_blob(p):
        if p not in _blob_cache:
            _blob_cache[p] = git("show", "%s:%s" % (sha, p))
        return _blob_cache[p]

    seeds, unmodelled, unsourced = import_closure(ship_paths, _read_blob)
    if unsourced:
        raise RuntimeError(
            "IMPORT CLOSURE REFUSED — %d packed module(s) import something the pack carries "
            "NOWHERE, so no seed can fix it. Either ship the module or stop shipping the "
            "importer: %s" % (len(unsourced), unsourced[:5]))
    comp_seeds, comp_unsourced = companion_closure(ship_paths)
    if comp_unsourced:
        raise RuntimeError(
            "COMPANION CLOSURE REFUSED — %d packed door(s) declare a companion the pack carries "
            "NOWHERE at this commit: %s.\n"
            "   The ship list comes from `git ls-tree` AT THE COMMIT, so an UNCOMMITTED companion "
            "is invisible here and this refusal is what an incomplete pair looks like.\n"
            "   REMEDY, one of: (1) commit the companion — for the Memento door that is "
            "`apollo-spider/gumdrop/machinery/_build_memento_index.py` — and re-run at the new "
            "sha; or (2) delete its DOOR_COMPANIONS entry, which is a decision to ship a door "
            "that cannot be opened."
            % (len(comp_unsourced), comp_unsourced[:5]))
    # ONE seed list from here on: the manifest block, `apply_closure`, `--stage` and `check_pack`
    # all read `import_closure.seeds`, and a second list would be a second place to forget.
    collide = {s["dest"] for s in seeds} & {s["dest"] for s in comp_seeds}
    if collide:
        raise RuntimeError("CLOSURE COLLISION — %s is claimed by both the import closure and a "
                           "declared companion" % sorted(collide))
    seeds = sorted(seeds + comp_seeds, key=lambda s: s["dest"])
    closure_bytes = blob_sizes(sha, sorted({s["src"] for s in seeds}))
    import_closure_block = dict(
        seeds=seeds,
        files=len(seeds),
        companions=len(comp_seeds),
        bytes=sum(closure_bytes.get(s["src"], 0) for s in seeds),
        unmodelled_path_inserts=unmodelled,
        why="A packed module's module-level imports must resolve from where THAT FILE lands in "
            "the pack. v1.0.0 shipped memento-package/claude-plugin/memento/machinery/"
            "_gen_chain.py with no _could_not_ask.py beside it and it could not be imported at "
            "all. These seeds are byte-copies of files already in the pack, placed where the "
            "importer can reach them. `companions` counts the DECLARED half (see "
            "DOOR_COMPANIONS): a dependency stated in a runtime refusal, which no import parser "
            "can see — v1.0.1's Memento door shipped with no index builder anywhere in the pack.",
    )

    totals = dict(
        files=sum(e["files"] for e in out_groups),
        bytes=sum(e["bytes"] for e in out_groups),
        # What a designer actually unzips: the ship list PLUS the closure copies. `files` stays
        # the ship list because `--manifest` refuses when it and `all_paths(man)` disagree.
        pack_files=sum(e["files"] for e in out_groups) + import_closure_block["files"],
        pack_bytes=sum(e["bytes"] for e in out_groups) + import_closure_block["bytes"],
        by_group={gk: dict(files=sum(e["files"] for e in es),
                           bytes=sum(e["bytes"] for e in es))
                  for gk, es in seen_group.items()},
    )

    excluded = [dict(path=p, reason=r) for p, r in EXCLUDED]
    excluded.append(dict(
        path="knowledge/_validate_* (repo-bound subset)",
        reason="MEASURED, not assumed: %d validators crashed reaching for something the pack "
               "does not carry. Each is named with its reason in the gates group's verdict "
               "table." % len(repobound)))
    # #219 seam 9, enacting Dave's Q6 answer. He ruled the 55-gate roster, and the condition he
    # ruled it under is that the two that fell out are STATED rather than silently absent. So
    # they get their own row, spelled by name, with the reason read out of the probe — not a
    # sentence pointing at another table [[premise-ages-faster-than-rule]].
    _q6_why = {r["gate"]: r["why"] for r in probe["gates"]}
    excluded.append(dict(
        path=", ".join("knowledge/%s" % g for g in Q6_DROPPED_GATES),
        reason="THE TWO THAT TOOK THE ROSTER FROM 57 TO 55, named because Dave's answer to Q6 "
               "was 55 gates on the condition the drop is visible. %s — and _claimtable.py is "
               "its only local helper, so it travels with it. Neither is missing by accident "
               "and neither is broken: a check whose subject the pack does not carry has "
               "nothing to say in a designer's project."
               % _q6_why.get("_validate_evidence.py",
                             "_validate_evidence.py is REPO-BOUND").replace(
                   "runs, but its verdict is about",
                   "_validate_evidence.py runs, but its verdict is about")))
    excluded.append(dict(
        path="knowledge/ (everything else)",
        reason="The audit files, build scripts, session machinery and working documents that "
               "make up the rest of knowledge/ — the workshop, not the engine."))

    return dict(
        schema=SCHEMA,
        pack=PACK_NAME,
        slug=PACK_SLUG,
        version=VERSION,
        # The cut of Memento inside this pack has its OWN identity and its own version line
        # (s219-D8). It is stamped here, in the pack README and in PROVENANCE.json — the three
        # places the pack states where it came from — and NOWHERE inside memento-package/, which
        # is the repo's own machinery and not this release's to sign.
        # ⚠ #219 seam 9, on N3's HANDOFF 1. This line USED to read "machinery only, no record",
        # which s219-D5(Q1) made FALSE the moment the empty stores and the starter chain joined
        # the cut. It is stated in three places (here, _PACK.json, the pack README) and all
        # three were corrected together — a pack whose own provenance line contradicts its own
        # contents is the [[gate-dont-patch]] class, so `cut/no-record-claim-is-dead` below
        # greps for the dead phrasing in this file AND in the bake script.
        carries=dict(name=MEMENTO_CUT_NAME, version=MEMENTO_CUT_VERSION,
                     what="A clean cut of Memento: the machinery, plus a cold start whose "
                          "record is EMPTY on purpose — an empty task store and an empty "
                          "rulings store with the shapes already right, and a starter "
                          "_CHAIN.md that the first wrap replaces. Its version line is its "
                          "own; the pack's version does not move it."),
        status=ratification_status(),
        commit=sha,
        commit_date=commit_date(sha),
        ruling="s219-D8 (naming) · s219-D5 (the five cards) · s219-D4 (the cut)",
        groups=out_groups,
        excluded=excluded,
        import_closure=import_closure_block,
        open_questions=OPEN_QUESTIONS,
        totals=totals,
        gate_probe=dict(timeout_s=probe["timeout_s"],
                        commit=probe["commit"],
                        repo_bound=[dict(gate=r["gate"], why=r["why"])
                                    for r in sorted(probe["gates"], key=lambda x: x["gate"])
                                    if r["verdict"] == "REPO-BOUND"]),
    )


def canonical(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def manifest_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def all_paths(man):
    out = []
    for g in man["groups"]:
        out.extend(g["paths"])
    return sorted(set(out))


# ---------------------------------------------------------------------------------------------
# THE PAGE — Dave's go/no-go surface. GENERATED from the manifest, never hand-kept: a page that
# said 1,590 files while the manifest said something else is the exact defect this release shape exists to end.
# Two-register rule (_RUNBOOK-review-doc.md, ruled #66-D5): plain prose leads every card, the
# machinery folds beneath it. Dave is dyslexic — one group per card, one idea per sentence.
# ---------------------------------------------------------------------------------------------

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _words(n):
    """Small counts read as words in Dave's prose, and the count is still DERIVED.

    #219 seam 9: the lede said "six groups" while the manifest carried seven. Spelling the
    number is a house habit in running text; the point of this helper is that the digit comes
    from the data either way [[banner-figures-are-parsed-not-prose]]."""
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
            8: "eight", 9: "nine", 10: "ten"}.get(n, str(n))


def mb(n):
    if n >= 1_000_000:
        return "%.1f MB" % (n / 1_000_000)
    if n >= 1000:
        return "%d KB" % round(n / 1000)
    return "%d bytes" % n


PAGE_CSS = """
  :root{ --pg:#FFFFFF; --pgink:#1A1A1A; --pgmut:#626262; --pgline:#E1E1E1; --pgsoft:#F5F5F5; }
  body{margin:0; padding:40px 32px 120px; background:var(--pg); color:var(--pgink);
       font-family:var(--typography-font-family, system-ui, -apple-system, "Segoe UI", sans-serif);
       -webkit-font-smoothing:antialiased; line-height:1.55;}
  .wrap{max-width:1180px; margin:0 auto;}
  h1{font-size:28px; line-height:1.2; margin:0 0 6px; letter-spacing:-.01em;}
  h2{font-size:20px; margin:56px 0 4px; letter-spacing:-.01em;}
  h3{font-size:15px; margin:28px 0 8px; text-transform:uppercase; letter-spacing:.08em; color:var(--pgmut);}
  p{margin:8px 0 14px; max-width:76ch;}
  .lede{font-size:16px; color:var(--pgmut);}
  code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9em;
       background:var(--pgsoft); padding:1px 5px; border-radius:4px;}
  .tag{display:inline-block; font-size:11px; font-weight:700; letter-spacing:.09em;
       text-transform:uppercase; padding:3px 8px; border-radius:4px; vertical-align:2px;}
  .tag.prop{background:#1A1A1A; color:#FFFFFF;}
  .tag.in{background:#E8F3EC; color:#1F5C38; border:1px solid #BEDCC9;}
  .tag.out{background:#F0F0F0; color:#555555; border:1px solid #DDDDDD;}
  .tag.ask{background:#FFF0E6; color:#8A4B10; border:1px solid #E8C6A8;}
  .tag.dep{background:#EEF2F7; color:#3B5570; border:1px solid #C9D6E4;}
  table{border-collapse:collapse; width:100%; margin:14px 0 8px; font-size:14px;}
  th,td{text-align:left; padding:9px 10px; border-bottom:1px solid var(--pgline); vertical-align:top;}
  th{font-size:11px; text-transform:uppercase; letter-spacing:.07em; color:var(--pgmut); font-weight:700;}
  td.num{text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap;}
  .note{border-left:3px solid var(--pgline); padding:2px 0 2px 14px; color:var(--pgmut);
        font-size:14px; margin:14px 0; max-width:76ch;}
  .warn{border-left-color:#C25A18; color:#7A3A0E;}
  .card{border:1px solid var(--pgline); border-radius:10px; background:#FFF; padding:20px 22px;
        margin:16px 0;}
  .card h3{margin-top:0; color:var(--pgink); font-size:17px; text-transform:none;
           letter-spacing:-.01em;}
  .card .plain{font-size:15.5px; max-width:70ch; margin:6px 0 12px;}
  .metrics{display:flex; flex-wrap:wrap; gap:22px; margin:10px 0 4px; font-size:13px;
           color:var(--pgmut);}
  .metrics b{display:block; font-size:19px; color:var(--pgink); font-variant-numeric:tabular-nums;
             letter-spacing:-.01em;}
  details{margin:10px 0 0;}
  summary{cursor:pointer; font-size:13px; color:var(--pgmut); padding:6px 0;}
  .paths{max-height:280px; overflow:auto; background:var(--pgsoft); border-radius:6px;
         padding:10px 12px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
         font-size:11.5px; line-height:1.7; color:#3A3A3A;}
  .q{border:1px solid #E8C6A8; background:#FFFCF8;}
  .q h3{color:#7A3A0E;}
  .opts{margin:14px 0 0; padding:0; list-style:none;}
  .opts li{margin:0 0 8px; padding:10px 12px; border:1px solid var(--pgline); border-radius:8px;
           background:#FFF; font-size:14.5px;}
  .opts label{display:flex; gap:10px; align-items:flex-start; cursor:pointer;}
  .rec{font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
       color:#1F5C38; margin-left:6px;}
  .ruled{font-size:15.5px; max-width:70ch; margin:6px 0 12px; padding:12px 14px;
         background:#F3F8F5; border:1px solid #BEDCC9; border-radius:8px;}
  .head{display:flex; flex-wrap:wrap; gap:34px; padding:18px 22px; border:1px solid var(--pgline);
        border-radius:10px; background:var(--pgsoft); margin:18px 0 8px;}
  .head div b{display:block; font-size:24px; letter-spacing:-.02em;
              font-variant-numeric:tabular-nums;}
  .head div span{font-size:12px; color:var(--pgmut); text-transform:uppercase; letter-spacing:.07em;}
  ul{max-width:76ch;} li{margin:5px 0;}
  /* ⚠ MEASURED at 480px: the exclusions table forced the whole document to 798px wide, so the
     PAGE scrolled sideways rather than the table. Wide content scrolls inside its own box. */
  .tw{overflow-x:auto;}
  .tw>table{min-width:520px;}
"""


# The lead-in prose for each group card, one entry per group declared in groups().
# ⚠ MODULE SCOPE at #219 seam 9 so the selftest can assert it is COMPLETE: the
# lookup below is a bare subscript, so a group declared without a lead takes the
# whole page down with a KeyError at render time — which is exactly what the new
# `gumdrop` group did, and no bite could see it while this dict was a local.
GROUP_LEAD = {
    "engine-canon": (
        "The engine itself",
        "This is the part you actually work in every day. Tokens, the contract for every "
        "component, the reference markup, the canon stylesheets, the compliance map, the "
        "real icons and the written guidelines. Nothing here is a summary of Apollo — it "
        "is Apollo."),
    "gates": (
        "The gates",
        "The checks that make Apollo a system rather than a folder of files. Every gate "
        "below was actually RUN inside a copy of this pack, on its own, outside your repo. "
        "The verdicts are measurements, not opinions — and the ones that only work here "
        "are named, with the reason, and left out."),
    "runbooks": (
        "The runbooks",
        "The written procedures. How to compose from canon. How to take a component "
        "through its gates. How to render a page and actually look at it. How to write a "
        "criteria contract before you build. How to bring an existing code library in."),
    "library": (
        "The library",
        "The showroom, alive — every component page, the foundations pages, the thumbnails, "
        "the index. Plus the rails file the library, the editor and the generator all read, "
        "and the render script so a designer can see their own work the way you do."),
    "memento-clean-cut": (
        "A clean cut of Memento — the machinery",
        "The chain generator, retrieval, the graph edges, the gauge shim, the lexicon. "
        "These files carry no record: not one line of this project's history travels in "
        "them. What a designer starts from is the group below."),
    # #219 seam 9 (N3's region 6). Its OWN lead, and it must exist: `GROUP_LEAD[gk]` is a
    # bare subscript, so a group declared without a lead takes the page down with a
    # KeyError at render — measured, not assumed [[no-gate-parses-the-artefact]].
    "gumdrop": (
        "Day one — the cold start",
        "The machinery above can hold a record; this is the empty record it holds it in, "
        "and the walkthrough that gets a designer to their first entry. An empty task "
        "store and an empty rulings store, both with the shapes already right and both "
        "DRIVEN against the empty shape rather than eyeballed. A starter chain that says "
        "what the first move is and is replaced the first time they wrap. A guided first "
        "session. And the two Memento runbooks — capture at wrap, and the context gauge — "
        "rewritten for VS Code and Copilot, honest about the one thing that environment "
        "cannot measure."),
    "skills": (
        "The skills",
        "Five, and they are written. Four rewritten against this knowledge base — the "
        "library is 135 components now, not 40, and the red law they quoted was three "
        "rulings out of date. The fifth is new: the gate-runner that actually runs the "
        "packed gates on a designer's own work, and reads the verdicts back honestly."),
}

# The order the group cards render in — the THIRD copy of the group set, hoisted at #219
# seam 9 stage 2 for the same reason GROUP_LEAD was at stage 1: as a typed local inside
# render_page it silently omitted N3's `gumdrop` group, so the lede counted seven groups,
# GROUP_LEAD carried the lead, the manifest carried the files — and Dave's page rendered
# six cards, with the clean-cut lead promising "the group below" above a card that never
# came. No KeyError this time, which is worse: the page lied quietly instead of dying.
# Bitten both directions in the selftest, plus the lede correspondence — the prose says
# "the last two are Memento … and the day-one walk-in", so the order must END with that
# pair. [[green-tests-cannot-see-scope]] [[no-gate-parses-the-artefact]]
GROUP_ORDER = ["engine-canon", "gates", "runbooks", "library", "skills",
               "memento-clean-cut", "gumdrop"]


def render_page(man, zip_bytes=None, zip_sha=None, man_sha=None):
    G = {}
    for g in man["groups"]:
        G.setdefault(g["group"], []).append(g)
    gates = [g for g in man["groups"] if g["key"] == "gates"][0]
    c = gates["counts"]


    out = []
    A = out.append
    A('<!doctype html>\n<meta charset="utf-8">')
    A('<title>%s — the release manifest — %s</title>' % (esc(PACK_NAME), status_word()))
    A('<!-- reviews/RELEASE-SPIDER-2026-08-26-v1.html — #219 R1.\n'
      '     GENERATED by knowledge/_release/_gen_pack_manifest.py --page. Do not hand-edit:\n'
      '     every count on this page is read out of _pack_manifest.json, which is itself\n'
      '     generated from a named commit. Nothing on this page is typed. -->')
    A('<link rel="stylesheet" href="../knowledge/canon/canon.css">')
    A('<link rel="stylesheet" href="../knowledge/canon/type.css">')
    A('<style>%s</style>' % PAGE_CSS)
    A('<div class="wrap">')

    if status_word() == "RATIFIED":
        A('<h1>%s — what ships <span class="tag ok">Ratified</span></h1>' % esc(PACK_NAME))
        A('<p class="lede">#219 · 2026-08-26 · ratified by %s — Dave’s word, in the store. '
          'This page is the list the bake reads.</p>' % ratify_id())
    else:
        A('<h1>%s — what ships <span class="tag prop">Proposed</span></h1>' % esc(PACK_NAME))
        A('<p class="lede">#219 · 2026-08-26 · nothing is baked, nothing is committed, '
          'no release exists. This page is the list, for your eye. The bake does not run until '
          'you say it does.</p>')
    # s219-D8, the naming, stated once in plain words where a reader meets the pack for the
    # first time. Two families by TYPE, and one MISSION per release.
    A('<p class="note"><b>The names.</b> This pack is <b>%s</b>, version <code>%s</code> — '
      'Apollo pack releases take LUNAR MODULE names, because they are the thing that lands in a '
      'designer\'s hands. The clean cut of Memento it carries is <b>%s %s</b> — Memento '
      'releases take COMMAND MODULE names, because Memento is what navigates and remembers. '
      'The repo itself stays the command seat. A release takes <b>one mission\'s whole pair</b>: '
      'Spider and Gumdrop are both Apollo 9, and the next release is Apollo 10\'s pair, in '
      'mission order. (<code>s219-D8</code>; supersedes <code>s219-D7</code> and '
      '<code>s219-D6</code>, neither of which reached a commit.)</p>'
      % (esc(PACK_NAME), esc(man["version"]), esc(MEMENTO_CUT_NAME),
         esc(MEMENTO_CUT_VERSION)))

    A('<h2>The short version</h2>')
    # ⚠ DERIVED, not typed. This sentence said "six groups" while the manifest carried seven —
    # the cold start had been added as its own group and the prose beside it had not moved.
    # A count on Dave's decision surface is read out of the thing it counts, always.
    _n_groups = len(G)
    _n_engine = len([k for k in G if not k.startswith(("memento", "gumdrop"))])
    A('<p>You said you wanted designers to get <em>as close to what you use as possible, '
      'without the review files and the extras, even a clean cut of Memento</em>. This is that '
      'list. It is %s groups. %s of them are things you already work in; the last two are '
      'Memento with its memory emptied out, and the day-one walk-in that goes with it.</p>'
      % (_words(_n_groups), _words(_n_engine).capitalize()))
    A('<p>The list is not typed by hand. It is worked out from one named commit, so the pack '
      'and the repo can never quietly disagree — and building the same commit twice gives a '
      'file that is <b>identical down to the byte</b>, which is what makes it possible to see '
      'exactly what changed between two releases.</p>')

    A('<div class="head">')
    # #220: what a designer unzips is the ship list PLUS the import-closure copies. The label
    # says "in the pack", so the number has to be the pack's, not the ship list's.
    A('<div><b>%s</b><span>files in the pack</span></div>'
      % "{:,}".format(man["totals"].get("pack_files", man["totals"]["files"])))
    A('<div><b>%s</b><span>on disk</span></div>'
      % mb(man["totals"].get("pack_bytes", man["totals"]["bytes"])))
    if zip_bytes:
        A('<div><b>%s</b><span>zipped — the download</span></div>' % mb(zip_bytes))
    A('<div><b>%d</b><span>gates that run anywhere</span></div>' % (c["runnable"] + c["needs_dep"]))
    # DERIVED, both halves. The headline metric counts what is STILL open — a page that said
    # "5 questions for you" beside five cards he has already answered would be the
    # [[banner-figures-are-parsed-not-prose]] class one inch from where he rules, which is
    # exactly what seam 7 fixed here in the other direction.
    _still_open = len([q for q in man["open_questions"] if not q.get("answered")])
    _settled = len(man["open_questions"]) - _still_open
    A('<div><b>%d</b><span>questions for you</span></div>' % _still_open)
    if _settled:
        A('<div><b>%d</b><span>you have settled</span></div>' % _settled)
    A('</div>')
    A('<p class="note">Read from commit <code>%s</code> (%s) — nothing has been baked. '
      'Manifest fingerprint '
      '<code>%s</code>. Version <code>%s</code>.</p>'
      % (esc(man["commit"][:12]), esc(man["commit_date"][:10]),
         esc((man_sha or "")[:16]), esc(man["version"])))

    # ---- the groups, one card each
    A('<h2>What goes in — one card per group</h2>')
    for gk in GROUP_ORDER:
        entries = G.get(gk, [])
        if not entries:
            continue
        t = man["totals"]["by_group"][gk]
        lead_title, lead_plain = GROUP_LEAD[gk]
        A('<div class="card">')
        A('<h3>%s <span class="tag in">In</span></h3>' % esc(lead_title))
        A('<p class="plain">%s</p>' % esc(lead_plain))
        A('<div class="metrics"><div><b>%s</b>%s</div><div><b>%s</b>on disk</div></div>'
          % ("{:,}".format(t["files"]), "files in this group", mb(t["bytes"])))
        A('<table><tr><th>part</th><th>what it is</th><th class="num">files</th>'
          '<th class="num">size</th></tr>')
        for e in entries:
            A('<tr><td><b>%s</b></td><td>%s</td><td class="num">%s</td><td class="num">%s</td></tr>'
              % (esc(e["title"]), esc(e["plain"]), "{:,}".format(e["files"]), mb(e["bytes"])))
        A('</table>')

        if gk == "gates":
            A(render_gate_table(gates))
            # #219 R2 — the pack-side half of "CI both halves". Rendered only when the files
            # are actually in the commit the manifest was built from, so this page can never
            # promise a designer a workflow that is not in the zip.
            if gates.get("ci_template"):
                A('<p class="note"><b>The pack ships a CI workflow too.</b> %d file(s) at '
                  '<code>ci-template/</code> in the pack root (their repo home is '
                  '<code>apollo-spider/ci-template/</code>): a GitHub Actions workflow a '
                  'designer copies into their own repo, the runner it calls, and a README that '
                  'says what blocks, what only advises, and how to turn a check off honestly '
                  '(delete the step — never hide it behind continue-on-error).</p>'
                  % len(gates["ci_template"]))
        # #219 seam 7: the "Empty slot, named" renderer is GONE with its producer. Leaving the
        # consumer behind was not harmless — rendered against a manifest generated before the
        # repoint it still painted "PLACEHOLDER — R3 writes it" onto Dave's page for a skill
        # that exists (measured, not reasoned: it fired on the stale manifest during this seam).
        # A consumer that outlives its producer keeps telling the old story to whoever feeds it
        # old data. [[instrument-without-a-consumer]], inverted.

        allp = sorted({p for e in entries for p in e["paths"]})
        A('<details><summary>Every path in this group (%s)</summary><div class="paths">%s</div>'
          '</details>' % ("{:,}".format(len(allp)), "<br>".join(esc(p) for p in allp)))
        A('</div>')

    # ---- what stays out
    A('<h2>What stays out, and why <span class="tag out">Out</span></h2>')
    A('<p>Every line below is a deliberate exclusion, not an oversight. Three reasons cover '
      'nearly all of it: it is your working paperwork, it is your session record, or we do not '
      'hold a licence that lets us pass it on.</p>')
    A('<table><tr><th>what</th><th>why it stays here</th></tr>')
    for x in man["excluded"]:
        A('<tr><td><code>%s</code></td><td>%s</td></tr>' % (esc(x["path"]), esc(x["reason"])))
    A('</table>')

    # ---- the open questions
    # #219 seam 7: the count was the word "Four", typed, while the list beside it was data. A
    # fifth card would have left the heading lying on Dave's own decision surface, which is the
    # [[banner-figures-are-parsed-not-prose]] class one inch from where he rules. Now derived.
    _NW = {1: "One thing", 2: "Two things", 3: "Three things", 4: "Four things",
           5: "Five things", 6: "Six things", 7: "Seven things"}

    def _body(q):
        # Short paragraphs, not a wall. The body carries `||` where a break belongs — Dave
        # reads one idea per block, and an unbroken twelve-line paragraph is the format he
        # has already told us costs him time.
        for para in q["body"].split("||"):
            A('<p class="plain">%s</p>' % esc(para.strip()))

    open_q = [q for q in man["open_questions"] if not q.get("answered")]
    done_q = [q for q in man["open_questions"] if q.get("answered")]

    if open_q:
        _nq = len(open_q)
        A('<h2>%s only you can settle <span class="tag ask">Ask</span></h2>'
          % _NW.get(_nq, "%d things" % _nq))
        A('<p>None of these are blocked on work. They are all judgement calls about where a '
          'line sits. Nothing is pre-selected.</p>')
        for q in open_q:
            A('<div class="card q">')
            A('<h3>%s. %s</h3>' % (esc(q["id"]), esc(q["title"])))
            _body(q)
            A('<ul class="opts">')
            for i, o in enumerate(q["options"]):
                rec = " recommended" in o or "(recommended" in o
                A('<li><label><input type="radio" name="%s" value="%d"><span>%s%s</span>'
                  '</label></li>'
                  % (esc(q["id"]), i,
                     esc(o.replace(" (recommended)", "").replace(" — recommended", "")),
                     '<span class="rec">recommended</span>' if rec else ""))
            A('</ul></div>')

    # ---- the same cards, once he has answered them. NO radio inputs: an answered card must
    # not keep offering the choice back. The question stays visible because the answer is only
    # legible beside what was asked.
    if done_q:
        _nd = len(done_q)
        A('<h2>%s you settled <span class="tag in">Ruled</span></h2>'
          % _NW.get(_nd, "%d things" % _nd))
        A('<p>Your answers, as they were given, with the ruling that carries each one. Where a '
          'lane has already built it, what the pack now does is stated underneath.</p>')
        for q in done_q:
            ans = q["answered"]
            A('<div class="card">')
            A('<h3>%s. %s</h3>' % (esc(q["id"]), esc(q["title"])))
            # #219 seam 9: an answer Dave gave in the session, whose clause is not yet in the
            # rulings store, must NOT paint the same "Ruled" tag as one that is. Same three
            # registers as everywhere else — what he said, and what has been written down, are
            # different facts and the page says which is which.
            if ans.get("inscription") == "OWED":
                A('<p class="ruled"><span class="tag prop">Your answer</span> <b>%s</b> — %s</p>'
                  % (esc(ans.get("answered_in", "")), esc(ans["position"])))
                A('<p class="note warn"><b>Not written down yet.</b> You settled this in the '
                  'session and the pack already reflects it, but the clause is not in the '
                  'rulings store — <code>%s</code>. Inscribing it is the last step, and until '
                  'it happens this card is your word, not a record.</p>' % esc(ans["ruling"]))
            else:
                A('<p class="ruled"><span class="tag in">Ruled</span> <b>%s</b> — %s</p>'
                  % (esc(ans["ruling"]), esc(ans["position"])))
            if ans.get("enacted"):
                A('<p class="note"><b>What the pack does now.</b> %s</p>' % esc(ans["enacted"]))
            A('<details><summary>The question as it was put to you, and the options</summary>')
            _body(q)
            A('<ul class="opts">')
            for o in q["options"]:
                A('<li><span>%s</span></li>'
                  % esc(o.replace(" (recommended)", "").replace(" — recommended", "")))
            A('</ul></details></div>')

    # ---- how the bake works
    A('<h2>How it gets built, once you say yes</h2>')
    A('<p>One command, from a commit you name. It refuses to run on a messy working tree, it '
      'refuses to run without a commit, and it refuses to cut a release at all while this page '
      'still says <em>Proposed</em>. That last refusal is the one that matters: the release is '
      'your word, not the script\'s.</p>')
    # #219 stage 2 — the layout, stated so the page shows the TRUE shape a designer meets.
    # ⛔ #220. The pack root was TYPED here as `Apollo-Spider-v1.0.0/` while the thing it names
    # is `PACK_SLUG`-`VERSION` two hundred lines up. At the v1.0.1 bump Dave's go/no-go page
    # would have described unzipping a folder the bake no longer produces — a page whose job is
    # to be believed, quietly wrong about the one path a designer types first. Derived now.
    A('<p class="note"><b>What unzipping looks like.</b> The zip opens into one folder, '
      '<code>%s-%s/</code>, and everything sits directly inside it: '
      '<code>FIRST-SESSION.md</code>, <code>skills/</code>, <code>.github/</code>, '
      '<code>knowledge/</code>, <code>ci-template/</code>, '
      '<code>showroom/</code>, <code>memento-package/</code>, <code>_MANIFEST.json</code>, '
      '<code>README.md</code>. The skills and the CI template live under '
      '<code>apollo-spider/</code> in this repo, but the bake flattens that prefix away '
      '— a designer must find <code>skills/</code> the moment the zip opens, not two folders '
      'down. The pack checker verifies the zip through the same mapping.</p>'
      % (PACK_SLUG, VERSION))
    A('<details><summary>The commands</summary><div class="paths">'
      'bash apollo-spider/build-designer-pack.sh --manifest --commit &lt;sha&gt;<br>'
      'bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/x '
      '--commit &lt;sha&gt;<br>'
      'bash apollo-spider/build-designer-pack.sh --release --commit &lt;sha&gt;<br>'
      'bash apollo-spider/build-designer-pack.sh --check &lt;zip&gt; --commit &lt;sha&gt;'
      '</div></details>')
    if zip_sha:
        A('<p class="note">Proved today on a throwaway copy: built twice, into two different '
          'directories, and both files came out with the same fingerprint '
          '<code>%s</code>. Then checked back against the commit, file by file — green; '
          'and with one byte changed in one token file — red, naming the file.</p>'
          % esc(zip_sha[:16]))

    A('<p class="note warn"><b>Nothing here is enacted.</b> <code>apollo-spider/</code> '
      'holds the build script and nothing else. No pack has been baked, no zip exists in '
      '<code>dist/</code>, and no ruling was written. v1 and v2 are untouched.</p>')
    A('</div>')
    html = "\n".join(out) + "\n"
    # Every table gets a scroll box. Done here rather than at each emit site so a table added
    # later cannot forget it — the responsive rule is enforced once, not remembered three times.
    html = html.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return html


def render_gate_table(gates):
    rows = ['<h3 style="text-transform:none;letter-spacing:0;color:#1A1A1A;font-size:15px;'
            'margin-top:22px">Every gate, and whether it works away from home</h3>',
            '<p style="font-size:14.5px;max-width:70ch">Each one was copied into a bare '
            'directory holding only the pack, and run. Three answers: it works; it works but '
            'needs something installed first; or it only makes sense inside your repo, in '
            'which case it stays here and the reason is written down.</p>',
            '<table><tr><th>gate</th><th>verdict</th><th>what happened when it ran</th>'
            '<th>own tests</th></tr>']
    order = {"RUNNABLE": 0, "NEEDS-DEP": 1, "REPO-BOUND": 2}
    for v in sorted(gates["verdicts"], key=lambda r: (order[r["verdict"]], r["gate"])):
        tag = {"RUNNABLE": "in", "NEEDS-DEP": "dep", "REPO-BOUND": "out"}[v["verdict"]]
        label = v["verdict"]
        if v["verdict"] == "NEEDS-DEP":
            label = "needs " + esc(v["why"])
        extra = ""
        if v.get("population") == "EMPTY-IN-PACK":
            extra = (' <span class="tag ask">nothing to grade yet</span>')
        st = {"green": "pass", "red": "fail", "crashed": "won’t run here",
              "none": "none"}.get(v["selftest"], v["selftest"])
        rows.append('<tr><td><code>%s</code></td><td><span class="tag %s">%s</span>%s</td>'
                    '<td>%s</td><td>%s</td></tr>'
                    % (esc(v["gate"]), tag, esc(label), extra, esc(v["why"]), esc(st)))
    rows.append('</table>')
    rows.append('<p class="note">Three gates want <code>playwright</code> installed because '
                'they drive a real browser. They ship anyway and say so themselves when you '
                'run them without it. The ones marked <em>nothing to grade yet</em> run '
                'perfectly — they simply have no work of the designer’s to look at until '
                'the designer makes some.</p>')
    return "\n".join(rows)


# ---------------------------------------------------------------------------------------------
# THE ZIP — deterministic by construction
# ---------------------------------------------------------------------------------------------

def deterministic_zip(stage, out_zip, epoch, prefix=None):
    """Fixed mtimes (the COMMIT's), sorted order, fixed external attrs, no extra fields.
    Two runs over the same stage produce byte-identical archives.

    `prefix` wraps everything in ONE root folder — both so unzipping does not spray files into
    the user's cwd, and because --check's fidelity test needs a single root to strip."""
    import time
    dt = time.gmtime(epoch)
    date_time = (dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec)
    files = []
    for dirpath, dirnames, filenames in os.walk(stage):
        dirnames.sort()
        for f in sorted(filenames):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, stage)
            files.append((prefix + "/" + rel if prefix else rel, full))
    files.sort(key=lambda t: t[0])
    os.makedirs(os.path.dirname(os.path.abspath(out_zip)), exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel, full in files:
            zi = zipfile.ZipInfo(rel, date_time=date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o644 << 16)
            zi.create_system = 3
            with open(full, "rb") as fh:
                z.writestr(zi, fh.read(), compresslevel=9)
    return out_zip


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------------------------
# --check — a baked pack against manifest + commit
# ---------------------------------------------------------------------------------------------

def check_pack(zip_path, man, sha):
    fails = []
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        # #219 stage 2: the pack layout is pack_path(repo path) — the stager flattens
        # apollo-spider/ to the root, and this check verifies through the SAME mapping.
        repo_by_pack = {}
        for p in all_paths(man):
            q = pack_path(p)
            if q in repo_by_pack:
                fails.append("flatten collision: %r and %r both land at pack path %r"
                             % (repo_by_pack[q], p, q))
            repo_by_pack[q] = p
        # #220: the closure copies are pack paths with no repo path of their own — their bytes
        # are the SOURCE's blob, so they verify against the commit through the same bridge.
        for s in man.get("import_closure", {}).get("seeds", []):
            if s["dest"] in repo_by_pack:
                fails.append("closure collision: %r is both a shipped path and a closure copy"
                             % s["dest"])
            repo_by_pack[s["dest"]] = s["src"]
        want = set(repo_by_pack)
        # the pack root is <pack>/<pack path>; strip the single root component
        roots = {n.split("/")[0] for n in names}
        if len(roots) != 1:
            fails.append("pack has %d roots, expected 1: %s" % (len(roots), sorted(roots)[:5]))
        root = sorted(roots)[0] if roots else ""
        # ⚠ THE ROOT README, addressed exactly. The first cut picked it with a substring match
        # over a SET, which also matched `knowledge/README.md` — and set iteration order is
        # hash-randomised per process, so the same zip checked twice gave different answers.
        # A non-deterministic check is worse than no check.
        readme = [n for n in names if n == root + "/README.md"]
        got = {n[len(root) + 1:] for n in names if n.startswith(root + "/")}
        generated = {p for p in got if p in ("README.md", "PROVENANCE.json", "_MANIFEST.json")}
        missing = sorted(want - got)
        extra = sorted(got - want - generated)
        if missing:
            fails.append("%d manifest path(s) MISSING from the pack, first: %s"
                         % (len(missing), missing[:5]))
        if extra:
            fails.append("%d path(s) in the pack that the manifest does not name, first: %s"
                         % (len(extra), extra[:5]))
        # byte fidelity against the commit — the blob lives at the REPO path, the bytes in the
        # zip live at the PACK path; repo_by_pack is the bridge.
        want_sha = blob_shas(sha, sorted(repo_by_pack[p] for p in (want & got)))
        bad = []
        for p in sorted(want & got):
            data = z.read(root + "/" + p)
            oid = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
            rp = repo_by_pack[p]
            if want_sha.get(rp) and oid != want_sha[rp]:
                bad.append(p)
        if bad:
            fails.append("%d file(s) differ from the commit's blobs, first: %s"
                         % (len(bad), bad[:5]))
        if readme:
            txt = z.read(readme[0]).decode("utf8", "replace")
            if sha not in txt:
                fails.append("pack README does not carry the commit sha %s" % sha[:12])
            if manifest_hash(canonical(man)) not in txt:
                fails.append("pack README does not carry the manifest hash")
        else:
            fails.append("pack has no README.md at its root")
    return fails


# ---------------------------------------------------------------------------------------------
# selftest — mutation-tested both directions
# ---------------------------------------------------------------------------------------------

def selftest():
    fails = []
    n = [0]

    def bite(name, got, want, why=""):
        n[0] += 1
        if got != want:
            fails.append("[%s] got %r, wanted %r %s" % (name, got, want, why))

    # ---- classifier: the verdicts are a function of the RUN, and each arm can fail
    v, w = classify(0, "all green", "", set())
    bite("classify/clean-pass", v, "RUNNABLE")
    v, w = classify(1, "FAIL: 3 components missing a binding", "", set())
    bite("classify/clean-fail", v, "RUNNABLE", "a verdict is a run")
    v, w = classify(1, "", TRACE + "\nModuleNotFoundError: No module named 'playwright'", set())
    bite("classify/needs-dep", v, "NEEDS-DEP")
    bite("classify/needs-dep-name", w, "playwright")
    v, w = classify(1, "", TRACE + "\nFileNotFoundError: [Errno 2] No such file or directory: "
                                   "'/x/reviews/_REVIEW-QUEUE.json'", set())
    bite("classify/repo-bound", v, "REPO-BOUND")
    bite("classify/repo-bound-names-why", "reviews/_REVIEW-QUEUE.json" in w, True)
    v, w = classify(1, "", TRACE + "\nFileNotFoundError: [Errno 2] No such file or directory: "
                                   "'/x/knowledge/tokens/colour.json'",
                    {"knowledge/tokens/colour.json"})
    bite("classify/shipped-path-is-not-repo-bound", v, "RUNNABLE",
         "a path error INSIDE the shipped set is a verdict, not a fence")
    v, w = classify(124, "", "", set())
    bite("classify/timeout", v, "REPO-BOUND")

    # ---- the courteous-refusal arm: a gate that CATCHES ImportError and prints prose is still
    # a missing dependency. This is the bite that the narrow `ModuleNotFoundError:` regex failed.
    v, w = classify(77, "COULD-NOT-ASK: the 'playwright' module is not installed "
                        "(ModuleNotFoundError(\"No module named 'playwright'\"))", "", set())
    bite("classify/caught-import", v, "NEEDS-DEP")
    bite("classify/caught-import-name", w, "playwright")

    # ---- s223-D5 clause (1): THE EXIT-77 ARM. A refusal that names no module at all — the
    # browser gates' third state, where playwright IMPORTS and its browser will not run — must
    # still be NEEDS-DEP, and must name the remedy the refusal itself printed. Before this arm
    # these fell through to RUNNABLE and a refusal was filed as a verdict FAIL.
    v, w = classify(REFUSAL_EXIT,
                    "COULD-NOT-ASK: HIT-AREA: HARNESS UNAVAILABLE — playwright is installed and "
                    "a chromium binary was found, but it would not START on this box. The binary "
                    "is on disk; what failed is starting it — `playwright install --with-deps "
                    "chromium` re-installs it with the system libraries it needs.", "", set())
    bite("classify/refusal-is-needs-dep", v, "NEEDS-DEP", "a refusal is not a verdict")
    bite("classify/refusal-names-its-own-remedy", w, "playwright install --with-deps chromium")
    # …and the arm is SCOPED to 77: a real measured red must stay a red [[gate-inside-the-growth-loop]]
    v, w = classify(1, "ADVISORY: 12 target(s) measured, 2 finding(s) — UNDER by 5px", "", set())
    bite("classify/refusal-arm-does-not-widen", v, "RUNNABLE", "a measured FAIL is still a run")

    # ---- the SUBJECT test, both directions. A missing-language line naming an unshipped path
    # is REPO-BOUND; the very same path shape in a non-missing line must NOT trip it.
    v, w = classify(1, "UNPARSEABLE — GOOD-MORNING.md — file not found", "",
                    {"knowledge/tokens/colour.json"})
    bite("classify/subject-missing", v, "REPO-BOUND")
    v, w = classify(1, "glob      : knowledge/canon/*.css  (2 file(s))\n"
                       "parsed    : 12009 declarations\nFORK: --c-x forks --c-y", "",
                    {"knowledge/canon/canon.css"})
    bite("classify/subject-present-is-a-verdict", v, "RUNNABLE",
         "a path named in a line it successfully READ must not read as a fence")
    v, w = classify(1, "✗ VERBATIM SET: source knowledge/_gen_chain.py does not exist", "",
                    {"knowledge/canon/canon.css"})
    bite("classify/subject-named-in-why", "_gen_chain.py" in w, True)

    # ---- the vacuous-pass detector, both directions. This is the bite the first cut failed.
    bite("empty-pop/zero-inputs",
         bool(EMPTY_POP.search("✅ No-hardcode gate passed (0 tranche file(s)).")), True)
    bite("empty-pop/zero-failures-is-NOT-empty",
         bool(EMPTY_POP.search("a11y gate: 135 snippet(s), 0 failure(s), 286 warning(s)")), False,
         "zero FAILURES is the good news; only zero FILES is an empty subject")
    bite("empty-pop/zero-warnings-is-NOT-empty",
         bool(EMPTY_POP.search("gate: 40 page(s), 0 warning(s)")), False)

    # ---- path naming: the probe's stage prefix must never reach Dave's page
    bite("tail/strips-stage",
         _tail("/var/tmp/packprobe-abc/pack/knowledge/_state.json"), "knowledge/_state.json")
    bite("tail/keeps-plain-path", _tail("knowledge/canon/canon.css"), "knowledge/canon/canon.css")

    # ---- the args-refusal arm
    v, w = classify(2, "✖ HIT-AREA: no input files. Pass paths or --all.", "", set())
    bite("classify/args-refusal", v, "RUNNABLE")

    # ---- MUTATION: a classifier that answered from the source rather than the run would call
    # a playwright import REPO-BOUND. Prove the discriminator is the message, not the exit code.
    v1, _ = classify(1, "", TRACE + "\nModuleNotFoundError: No module named 'playwright'", set())
    v2, _ = classify(1, "", TRACE + "\nFileNotFoundError: 'runs/x.json'", set())
    bite("classify/discriminates", v1 != v2, True)

    # ---- the group table: no path may be claimed twice, and every group must be reachable
    tbl = groups()
    keys = [g["key"] for g in tbl]
    bite("groups/unique-keys", len(keys), len(set(keys)))
    probe_paths = ["knowledge/tokens/colour.json", "knowledge/components/button.meta.json",
                   "knowledge/snippets/button.reference.html", "knowledge/canon/canon.css",
                   "knowledge/_validate_radius.py", "showroom/index.json",
                   "memento-package/machinery/_gen_chain.py",
                   "apollo-spider/skills/generate-from-canon/SKILL.md",
                   "apollo-spider/skills/check-with-gates/SKILL.md",
                   "knowledge/_RUNBOOK-compose-from-canon.md",
                   "apollo-spider/gumdrop/_rulings.json",
                   "apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md",
                   "apollo-spider/FIRST-SESSION.md",
                   "apollo-spider/.github/copilot-instructions.md"]
    for p in probe_paths:
        hits = [g["key"] for g in tbl if g["match"](p)]
        bite("groups/claims:%s" % os.path.basename(p), len(hits) >= 1, True,
             "no group claims it")
    # excluded paths must be claimed by NOBODY
    for p in ["reviews/x.html", "notes/_briefs/x.md", "knowledge/tokens/_raw/x.json",
              "API-KEY.txt", "GOOD-MORNING.md", "knowledge/_rulings.json",
              "knowledge/assets/photography-web/x.jpg", "designer-skills-v1/knowledge/x.json",
              "knowledge/_RUNBOOK-capture-ritual.md", "knowledge/_state.json",
              # #219 seam 7, the repoint proved in the OTHER direction: v2 is a FROZEN release
              # (s114-D4) and its SKILL.md must now be claimed by nobody. Without this bite the
              # skills match could silently widen back to v2 and only the ship list would know.
              "designer-skills-v2/generate-from-canon/SKILL.md"]:
        hits = [g["key"] for g in tbl if g["match"](p)]
        bite("groups/excludes:%s" % p, hits, [], "an EXCLUDED path was claimed by %s" % hits)

    # ---- the flatten (#219 stage 2, R3 Q2): pack layout is pack_path(repo path)
    bite("packpath/skills-flatten",
         pack_path("apollo-spider/skills/usability-review/SKILL.md"),
         "skills/usability-review/SKILL.md")
    bite("packpath/ci-template-flatten",
         pack_path("apollo-spider/ci-template/run-gates.py"),
         "ci-template/run-gates.py")
    bite("packpath/engine-passes-through", pack_path("knowledge/canon/canon.css"),
         "knowledge/canon/canon.css")
    # ---- the SEED MAP (#219 N3). The mapping is asserted AND driven on a real stage, because
    # the whole reason it exists is that Memento's machinery resolves paths from where the FILE
    # sits — a mapping that is only asserted proves nothing about where the bytes land.
    bite("packpath/seed-chain",
         pack_path("apollo-spider/gumdrop/_CHAIN.md"), "memento-package/_CHAIN.md")
    bite("packpath/seed-store",
         pack_path("apollo-spider/gumdrop/_rulings.json"), "memento-package/_rulings.json")
    bite("packpath/seed-beats-flatten",
         pack_path("apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md"),
         "memento-package/runbooks/_RUNBOOK-capture-ritual.md",
         "the seed map must be consulted BEFORE the apollo-spider flatten")
    bite("packpath/coldstart-docs-flatten",
         pack_path("apollo-spider/FIRST-SESSION.md"), "FIRST-SESSION.md")
    tmp2 = tempfile.mkdtemp(prefix="packseed-", dir="/var/tmp")
    try:
        os.makedirs(os.path.join(tmp2, "apollo-spider", "gumdrop", "runbooks"))
        os.makedirs(os.path.join(tmp2, "memento-package", "machinery"))
        open(os.path.join(tmp2, "apollo-spider", "gumdrop", "_state.py"), "w").write("m\n")
        open(os.path.join(tmp2, "apollo-spider", "gumdrop", "runbooks", "r.md"), "w").write("r\n")
        open(os.path.join(tmp2, "memento-package", "machinery", "_gen_chain.py"), "w").write("g\n")
        apply_seed_map(tmp2)
        bite("seed/lands-beside-frozen-machinery",
             os.path.exists(os.path.join(tmp2, "memento-package", "_state.py")), True)
        bite("seed/subdir-carried",
             os.path.exists(os.path.join(tmp2, "memento-package", "runbooks", "r.md")), True)
        bite("seed/frozen-side-untouched",
             open(os.path.join(tmp2, "memento-package", "machinery", "_gen_chain.py")).read(),
             "g\n")
        bite("seed/source-dir-gone",
             os.path.exists(os.path.join(tmp2, "apollo-spider", "gumdrop")), False)
        # the collision refusal — a seed file that would overwrite a frozen one must REFUSE
        os.makedirs(os.path.join(tmp2, "apollo-spider", "gumdrop"))
        open(os.path.join(tmp2, "apollo-spider", "gumdrop", "_state.py"), "w").write("second\n")
        try:
            apply_seed_map(tmp2)
            bite("seed/collision-refused", "ACCEPTED", "refused",
                 "a seed file silently overwrote what was already at the destination")
        except RuntimeError as ex:
            bite("seed/collision-refused", "collision" in str(ex), True)
        bite("seed/collision-left-the-original",
             open(os.path.join(tmp2, "memento-package", "_state.py")).read(), "m\n")
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)
    mapped = [pack_path(p) for p in probe_paths]
    bite("packpath/injective-on-probe-set", len(set(mapped)), len(mapped),
         "two shipped repo paths may not land on one pack path")
    # driven, not just mapped: a real stage, flattened, and the collision refusal
    tmp = tempfile.mkdtemp(prefix="packflatten-", dir="/var/tmp")
    try:
        os.makedirs(os.path.join(tmp, "apollo-spider", "skills", "x"))
        os.makedirs(os.path.join(tmp, "knowledge"))
        open(os.path.join(tmp, "apollo-spider", "skills", "x", "SKILL.md"), "w").write("s\n")
        open(os.path.join(tmp, "knowledge", "y.css"), "w").write("c\n")
        flatten_stage(tmp)
        bite("flatten/skills-at-root",
             os.path.exists(os.path.join(tmp, "skills", "x", "SKILL.md")), True)
        bite("flatten/nested-dir-gone",
             os.path.exists(os.path.join(tmp, "apollo-spider")), False)
        bite("flatten/engine-untouched",
             os.path.exists(os.path.join(tmp, "knowledge", "y.css")), True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # the collision refusal, on its OWN stage — reusing the last one made a no-op mutant die
    # by FileExistsError instead of by a named bite [[a-crash-is-not-a-fail]]
    tmp = tempfile.mkdtemp(prefix="packflatten-", dir="/var/tmp")
    try:
        os.makedirs(os.path.join(tmp, "apollo-spider"))
        # file vs file: the one shape os.rename would SILENTLY overwrite if the guard went
        open(os.path.join(tmp, "apollo-spider", "README.md"), "w").write("pack side\n")
        open(os.path.join(tmp, "README.md"), "w").write("root side\n")
        try:
            flatten_stage(tmp)
            verdict = "no error"
        except RuntimeError:
            verdict = "RuntimeError"
        except OSError as e:
            verdict = "OSError: %s" % type(e).__name__
        bite("flatten/collision-refused", verdict, "RuntimeError",
             "a colliding name must refuse, never overwrite")
        bite("flatten/collision-nothing-clobbered",
             open(os.path.join(tmp, "README.md")).read(), "root side\n",
             "the refusal must fire BEFORE the overwrite")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- THE IMPORT CLOSURE (#220). Bitten on a synthetic pack that reproduces the v1.0.0
    # SHAPE — two mirrored machinery dirs, one of them missing the sibling — because a bite over
    # the live tree only proves today's tree [[mutation-tests-the-clause-not-the-feature]].
    _HG = ("import os as _hg_os, sys as _hg_sys\n"
           "_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))\n"
           "while _hg_d != '/' and not _hg_os.path.exists("
           "_hg_os.path.join(_hg_d, '_helpgate.py')):\n"
           "    _hg_d = _hg_os.path.dirname(_hg_d)\n"
           "_hg_sys.path.insert(0, _hg_d)\n"
           "from _helpgate import help_gate\n")
    fake = {
        "apollo-spider/gumdrop/_helpgate.py": "def help_gate(*a): pass\n",
        "apollo-spider/gumdrop/machinery/_could_not_ask.py": _HG,
        "memento-package/machinery/_gen_chain.py":
            _HG + "import os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n"
                  "sys.path.insert(0, HERE)\nimport _could_not_ask\n",
        "memento-package/claude-plugin/memento/machinery/_gen_chain.py":
            _HG + "import os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n"
                  "sys.path.insert(0, HERE)\nimport _could_not_ask\n",
    }
    seeds, unmod, unsourced = import_closure(sorted(fake), lambda p: fake[p])
    bite("closure/finds-the-v100-defect",
         [s["dest"] for s in seeds],
         ["memento-package/claude-plugin/memento/machinery/_could_not_ask.py"],
         "the closure must name the ONE dir whose sibling import cannot resolve")
    bite("closure/seed-source-is-the-nearest-carrier",
         seeds[0]["src"] if seeds else None,
         "apollo-spider/gumdrop/machinery/_could_not_ask.py")
    bite("closure/needed-by-names-the-importer",
         seeds[0]["needed_by"] if seeds else None,
         ["memento-package/claude-plugin/memento/machinery/_gen_chain.py"])
    bite("closure/no-unsourced-in-the-fixture", unsourced, [])
    bite("closure/helpgate-walkup-is-modelled", unmod, 0,
         "the help-gate preamble is an idiom, not an unmodelled sys.path insert")
    # the seeded copy resolves — the same closure over the FIXED pack finds nothing left to do
    fixed = dict(fake)
    fixed["memento-package/claude-plugin/memento/machinery/_could_not_ask.py"] = _HG
    bite("closure/idempotent-once-satisfied",
         import_closure(sorted(fixed), lambda p: fixed[p])[0], [])
    # ⚠ THE DECLARED LIMIT, bitten so it cannot be forgotten. A module the pack carries NOWHERE
    # is indistinguishable, statically, from a third-party import — so the closure cannot see it
    # and MUST NOT pretend to. That case is `_gate_pack_imports.py`'s, which imports for real.
    # Bitten in both directions so the limit is a measured property, not a comment.
    orphan = {"memento-package/machinery/_gen_chain.py":
              "import os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n"
              "sys.path.insert(0, HERE)\nimport _nowhere_at_all\n"}
    _os, _ou, _ous = import_closure(sorted(orphan), lambda p: orphan[p])
    bite("closure/limit-a-module-the-pack-lacks-is-invisible", (_os, _ous), ([], []),
         "static closure cannot tell 'ours but absent' from 'third party' — the runtime gate can")
    # an unmodelled sys.path insert is COUNTED, never assumed harmless
    murky = {"knowledge/x.py": "import sys\nsys.path.insert(0, compute_it())\nimport _y\n",
             "knowledge/deep/_y.py": ""}
    bite("closure/unmodelled-insert-counted",
         import_closure(sorted(murky), lambda p: murky[p])[1], 1)

    # ---- THE COMPANION CLOSURE (#220 addendum). Same fixture SHAPE — the seed map lands the
    # builder in memento-package/machinery only, and the plugin mirror carries the door with no
    # builder beside it. That is the v1.0.0 defect wearing different clothes, and the bite is
    # over a synthetic pack for the same reason [[mutation-tests-the-clause-not-the-feature]].
    doors = {
        "apollo-spider/gumdrop/machinery/_build_memento_index.py": "BUILDER\n",
        "memento-package/machinery/_memento_search.py": "DOOR\n",
        "memento-package/claude-plugin/memento/machinery/_memento_search.py": "DOOR\n",
    }
    cseeds, cunsourced = companion_closure(sorted(doors))
    # ⚠ EXACTLY ONE seed, and the bite was WRONG first: `pack_path` already lands the builder in
    # memento-package/machinery/, so that door is satisfied by the seed map and needs nothing.
    # The plugin mirror is the only dir the map does not reach — which is, precisely, the v1.0.0
    # defect's dir. The fixture corrected the expectation, not the code.
    bite("companion/fills-only-the-dir-the-seed-map-cannot-reach",
         sorted(s["dest"] for s in cseeds),
         ["memento-package/claude-plugin/memento/machinery/_build_memento_index.py"],
         "the seed map already satisfies memento-package/machinery; the mirror is the gap")
    bite("companion/source-is-the-nearest-carrier",
         sorted({s["src"] for s in cseeds}),
         ["apollo-spider/gumdrop/machinery/_build_memento_index.py"])
    bite("companion/needed-by-names-the-door",
         cseeds[0]["needed_by"] if cseeds else None,
         ["memento-package/claude-plugin/memento/machinery/_memento_search.py"])
    bite("companion/why-travels-with-the-seed",
         bool(cseeds and "REFUSES until its index" in cseeds[0].get("why", "")), True,
         "a declared dependency must carry the reason it was declared")
    bite("companion/no-unsourced-in-the-fixture", cunsourced, [])
    # already satisfied -> nothing to do (so a second bake does not re-seed)
    satisfied = dict(doors)
    satisfied["memento-package/machinery/_build_memento_index.py"] = "BUILDER\n"
    satisfied["memento-package/claude-plugin/memento/machinery/"
              "_build_memento_index.py"] = "BUILDER\n"
    bite("companion/idempotent-once-satisfied", companion_closure(sorted(satisfied))[0], [])
    # a door with NO builder anywhere must REFUSE, never ship a door that cannot open
    orphan_door = {"memento-package/machinery/_memento_search.py": "DOOR\n"}
    _cs, _cu = companion_closure(sorted(orphan_door))
    bite("companion/door-with-no-builder-anywhere-is-unsourced",
         (_cs, _cu), ([], [("memento-package/machinery/_memento_search.py",
                            "_build_memento_index.py")]),
         "build_manifest REFUSES on this — a packed door whose builder is nowhere")
    bite("companion/no-door-no-seed", companion_closure(
        ["apollo-spider/gumdrop/machinery/_build_memento_index.py"])[0], [],
        "a builder with no door beside it is not a reason to copy anything")
    # ---- the stage arm: DRIVEN, because a mapping that is only asserted proves nothing
    tmp3 = tempfile.mkdtemp(prefix="packclosure-", dir="/var/tmp")
    try:
        for d in ("memento-package/machinery",
                  "memento-package/claude-plugin/memento/machinery"):
            os.makedirs(os.path.join(tmp3, d))
        open(os.path.join(tmp3, "memento-package/machinery/_could_not_ask.py"),
             "w").write("REAL\n")
        apply_closure(tmp3, [dict(module="_could_not_ask",
                                  dest="memento-package/claude-plugin/memento/machinery/"
                                       "_could_not_ask.py",
                                  src="apollo-spider/gumdrop/machinery/_could_not_ask.py",
                                  needed_by=[])])
        bite("closure/stage-copy-lands",
             open(os.path.join(tmp3, "memento-package/claude-plugin/memento/machinery/"
                                     "_could_not_ask.py")).read(), "REAL\n",
             "the copy must come from the STAGE (the commit's bytes), not the working tree")
        try:
            apply_closure(tmp3, [dict(module="_x", dest="memento-package/machinery/_x.py",
                                      src="apollo-spider/gumdrop/machinery/_nope.py",
                                      needed_by=[])])
            verdict = "no error"
        except RuntimeError:
            verdict = "RuntimeError"
        bite("closure/stage-missing-source-refuses", verdict, "RuntimeError")
    finally:
        shutil.rmtree(tmp3, ignore_errors=True)

    # ---- THE PHOTOGRAPHY SPECIMEN (#220). The pinned 15 are IMPORTED; the bite proves the
    # import happened and that the set is the size and shape the group claims.
    spec = photography_specimen()
    bite("photography/thirty", len(spec), 30)
    bite("photography/no-duplicates", len(set(spec)), 30)
    bite("photography/fifteen-additions", len(PHOTOGRAPHY_ADDITIONS), 15)
    _rendr = os.path.join(ROOT, "knowledge", "_render")
    if _rendr not in sys.path:
        sys.path.insert(0, _rendr)
    try:
        from gen_bento_roles_217 import SPECIMEN_FILES as _PIN
        bite("photography/pinned-set-is-the-pages-own",
             sorted(set(_PIN) - set(spec)), [],
             "every name the bento/gallery pages resolve must be in the cut")
        bite("photography/additions-do-not-overlap-the-pin",
             sorted(set(_PIN) & set(PHOTOGRAPHY_ADDITIONS)), [])
    except ImportError as e:
        fails.append("[photography/pinned-set-readable] %s" % e)
        n[0] += 1
    # ⚠ A pinned name whose file is gone ships nothing, silently. Bitten against DISK.
    _webd = os.path.join(ROOT, PHOTOGRAPHY_DIR)
    bite("photography/every-named-file-exists",
         sorted(f for f in spec if not os.path.exists(os.path.join(_webd, f))), [],
         "a named specimen file is missing from knowledge/assets/photography-web/")
    # the fence: the DIRECTORY stays excluded, only the named set crosses
    bite("photography/unnamed-file-claimed-by-nobody",
         [g["key"] for g in tbl if g["match"](PHOTOGRAPHY_DIR + "not-in-the-specimen.jpg")], [])
    bite("photography/named-file-is-claimed",
         [g["key"] for g in tbl if g["match"](PHOTOGRAPHY_DIR + spec[0])],
         ["library.photography"])

    # ---- the roster fence (#220). A release-side gate must not slip into the designer roster
    # and move `s219-D9`'s ruled 55. Bitten in BOTH directions or it is not a fence.
    bite("gates/release-side-gate-is-not-shipped",
         [g["key"] for g in tbl if g["match"]("knowledge/_gate_pack_imports.py")], [],
         "it audits a baked pack; a designer has no pack to audit, and s219-D9 ruled 55")
    bite("gates/an-ordinary-gate-still-ships",
         [g["key"] for g in tbl if g["match"]("knowledge/_gate_minted_consumption.py")],
         ["gates"], "the fence must be one named file, not a widened glob")

    # ---- retrieval (#220 addendum). The `_memento-index.json` exclusion used to promise
    # "adopters regenerate"; the pack ships nothing they could regenerate it WITH, so the promise
    # was false and the row now says so. A stated reason is a CONCLUSION, and a conclusion is
    # debt [[conclusions-are-debt-s129-d5]] — these two bites are its re-checker. If a future
    # lane ships a builder, the second one goes red and the reason must be rewritten, not left
    # to rot into a second false promise.
    _idx_reason = dict(EXCLUDED)["knowledge/_memento-index.json"]
    bite("retrieval/exclusion-names-the-missing-builder",
         "_build_memento_index.py" in _idx_reason and "CANNOT" in _idx_reason, True,
         "the row must name what is absent, not imply adopters can regenerate")
    bite("retrieval/no-index-builder-travels",
         [g["key"] for g in tbl if g["match"]("knowledge/_build_memento_index.py")], [],
         "if this ever ships, the exclusion reason above is STALE — rewrite it in the same edit")

    # ---- the open questions (#219 seam 7). Dave's decision surface is generated from this list,
    # so the list is what has to be checked — the page cannot be trusted to police itself.
    qids = [q["id"] for q in OPEN_QUESTIONS]
    bite("questions/unique-ids", len(qids), len(set(qids)))
    # An answered card must say WHO answered it. "It was decided" with no ruling id is how a
    # conductor's reading becomes a ruling by repetition [[dont-launder-a-premise-into-a-ruling]].
    for q in OPEN_QUESTIONS:
        a = q.get("answered")
        if not a:
            continue
        bite("questions/answered-cites-a-ruling:%s" % q["id"],
             bool(a.get("ruling", "").startswith("s")), True,
             "an answered card must name the ruling that settles it")
        bite("questions/answered-states-a-position:%s" % q["id"],
             len(a.get("position", "").strip()) > 40, True)
        # ⚠ AN UNINSCRIBED ANSWER MUST SAY SO. Writing a clause into _rulings.json is the
        # conductor's act and no generator's — so between Dave's word in chat and the store
        # entry, a card carries `inscription="OWED"` and cites the chat it came from, in the
        # repo's own evidence grammar. A card that cites a ruling id whose store entry does
        # not carry the clause is a confident FALSE inscription [[memento-framing]]. Q6 lived
        # in this register for exactly one stage (seam 9 stage 1 → the s219-D9 inscription);
        # the guard stays armed for the next answer that arrives by chat.
        if a.get("inscription") == "OWED":
            bite("questions/owed-clause-cites-the-chat:%s" % q["id"],
                 bool(re.match(r"^chat #\d+ \d{4}-\d{2}-\d{2} — Dave: ",
                               a.get("answered_in", ""))), True,
                 "an answer not yet in the rulings store must name the chat that carried it")
            bite("questions/owed-clause-says-owed-in-the-ruling-line:%s" % q["id"],
                 "OWED" in a.get("ruling", ""), True,
                 "the ruling line must not read as inscribed when it is not")
    # ⚠ WIDENED at #219 seam 9, and still a CLOSED set. Q2/Q3 are N1's clauses; Q6 is seam 9's,
    # and its enactment is the roster cut plus the named exclusion row measured below. The point
    # of the bite is that a lane cannot quietly claim an enactment it did not make — so the set
    # grows only when a seam adds one and names itself here.
    bite("questions/enactment-claims-are-a-closed-set",
         sorted(q["id"] for q in OPEN_QUESTIONS
                if q.get("answered", {}).get("enacted")), ["Q2", "Q3", "Q6"],
         "only a clause a lane actually enacted may claim an enactment on Dave's page")

    # ---- EVERY GROUP HAS A LEAD, or the page does not render (#219 seam 9). `GROUP_LEAD[gk]`
    # is a bare subscript in render_page, so a group declared in groups() with no lead is a
    # KeyError that takes down the whole of Dave's decision surface — and the 149-bite selftest
    # was green through it, because the dict was a local nothing could reach.
    # [[no-gate-parses-the-artefact]] [[green-tests-cannot-see-scope]]
    _declared_groups = sorted({g["group"] for g in groups()})
    bite("page/every-group-has-a-lead",
         [gk for gk in _declared_groups if gk not in GROUP_LEAD], [],
         "a group with no GROUP_LEAD entry is a KeyError at render, not a missing paragraph")
    bite("page/no-orphan-leads",
         [gk for gk in GROUP_LEAD if gk not in _declared_groups], [],
         "a lead for a group that no longer exists is prose describing a cut that did not happen")
    # ---- AND EVERY GROUP IS A CARD (#219 seam 9 stage 2). The render loop's order list was
    # a typed local too — the gumdrop group had a lead, a manifest entry and a lede counting
    # seven, and NO card, because nothing iterated it. A group absent from GROUP_ORDER fails
    # here instead of vanishing from Dave's page. [[green-tests-cannot-see-scope]]
    bite("page/every-group-is-a-card",
         [gk for gk in _declared_groups if gk not in GROUP_ORDER], [],
         "a group missing from GROUP_ORDER renders no card — the lede counts it, the page "
         "never shows it")
    bite("page/no-orphan-card-slots",
         [gk for gk in GROUP_ORDER if gk not in _declared_groups], [],
         "an order slot for a group that no longer exists")
    bite("page/order-ends-with-the-memento-pair",
         GROUP_ORDER[-2:], ["memento-clean-cut", "gumdrop"],
         "the lede says 'the last two are Memento … and the day-one walk-in', and the "
         "clean-cut lead says 'the group below' — the order must make both true")

    # ---- THE DEAD CUT-LEVEL CLAIM CANNOT COME BACK (#219 seam 9, on N3's HANDOFF 1). Until
    # this seam, the pack README, _PACK.json and this generator all said Memento — Gumdrop ships
    # no chain, no rulings, and no record of the kind spelled below. s219-D5(Q1) made that FALSE, and it was
    # false in three files at once — so the fix is a GATE over the phrasing, not three edits
    # [[gate-dont-patch]]. The phrase is assembled, never typed whole, for the same reason the
    # dead-name bites assemble theirs: a literal here would fail on this file's own text.
    _dead_claim = "no record of any" + " kind"
    _bake = os.path.join(ROOT, PACK_SURFACE_PREFIX, "build-designer-pack.sh")
    _gen_src = open(os.path.abspath(__file__), encoding="utf-8").read()
    bite("cut/no-record-claim-is-dead:generator", _dead_claim in _gen_src, False,
         "the cut ships EMPTY stores and a starter chain — saying otherwise ships a "
         "contradiction on the same page as the files")
    if os.path.exists(_bake):
        bite("cut/no-record-claim-is-dead:bake-script",
             _dead_claim in open(_bake, encoding="utf-8").read(), False,
             "the pack README is written by the bake script and must describe what the bake put "
             "in the pack")
        _bake_src = open(_bake, encoding="utf-8").read()
        bite("cut/readme-points-at-the-cold-start", "FIRST-SESSION.md" in _bake_src, True,
             "the README must name the file a designer is supposed to open first")

    # ---- THE RENAME CANNOT ROT BACK (s219-D8). The generator names the pack in DATA, and its
    # own source must carry no surviving reference to the name the release used to have. A grep
    # over this file is a real assertion here because this file IS the naming authority.
    _src = open(os.path.abspath(__file__), encoding="utf-8").read()
    # ⚠ THE DEAD NAMES ARE ASSEMBLED, NEVER TYPED WHOLE. Spelling them as literals here would
    # put them in the very file the bite greps, and the check would fail on its own text — a
    # self-referential red that teaches you to weaken the assertion. Driven: the first cut of
    # this bite went red on itself, four times.
    for dead in ("designer-skills-" + "v3", "_v3" + "_manifest", "_v3" + "_gate_probe",
                 "Apollo-" + "designer-skills"):
        bite("naming/no-stale:%s" % dead, dead in _src, False,
             "the pre-s219-D8 name survives in the generator that is supposed to have replaced it")
    bite("naming/slug-matches-name", PACK_SLUG, PACK_NAME.replace(" — ", "-"))
    bite("naming/prefix-is-the-pack-dir", PACK_SURFACE_PREFIX, "apollo-spider/")
    # ⚠ #220. The literal on the right is a HAND-MOVED FIXTURE and that is deliberate: it makes
    # every version bump of the carried cut a decision somebody typed, not a value that drifted.
    # Moved v1.0.0 -> v1.0.1 at the #220 bake, and v1.0.1 -> v1.0.2 at #223 (s223-D2), each
    # time in the same edit as MEMENTO_CUT_VERSION itself.
    bite("naming/memento-cut-is-named", (MEMENTO_CUT_NAME, MEMENTO_CUT_VERSION),
         ("Memento — Gumdrop", "v1.0.2"),
         "the cut inside the pack carries its own identity (s219-D8)")
    for q in OPEN_QUESTIONS:
        bite("questions/has-body:%s" % q["id"], len(q["body"].strip()) > 40, True)
        bite("questions/two-or-more-options:%s" % q["id"], len(q["options"]) >= 2, True,
             "a question with one answer is not a question")
    q5 = [q for q in OPEN_QUESTIONS if q["id"] == "Q5"]
    bite("questions/Q5-present", len(q5), 1, "R2's Q1 card — four gates arrive red at bake")
    if q5:
        body = q5[0]["body"]
        # Named, and STILL REAL. A card naming a renamed gate lies quietly on Dave's own page.
        for gname in Q5_RED_GATES:
            bite("questions/Q5-names:%s" % gname, gname in body, True,
                 "the red-gate card must state the gate by name")
            bite("questions/Q5-gate-exists:%s" % gname,
                 os.path.exists(os.path.join(ROOT, "knowledge", gname)), True,
                 "the card names a gate that is no longer in the repo — re-derive it")
        bite("questions/Q5-three-dispositions", len(q5[0]["options"]), 3,
             "fix-before-bake / baseline / ship-red-documented")
        # It is a QUESTION card. The renderer paints a 'recommended' flag on any option whose
        # text carries the word, and this one must not carry it in any option: seam 7 was told
        # to put the choice to Dave, not to make it. [[dont-launder-a-premise-into-a-ruling]]
        bite("questions/Q5-decides-nothing",
             [o for o in q5[0]["options"] if "recommended" in o], [],
             "the red-gate card must not pre-select a disposition")

    # ---- Q6, the roster cut (#219 seam 8 § ⑨ Q1). Same shape of assertion as Q5's, for the
    # same reason: the card's whole subject is two named files, and if either moves the card
    # must BREAK rather than go on describing a repo that no longer exists.
    q6 = [q for q in OPEN_QUESTIONS if q["id"] == "Q6"]
    bite("questions/Q6-present", len(q6), 1,
         "seam 8's roster question — 55 gates, not 57 — must be on Dave's page")
    if q6:
        body6 = q6[0]["body"]
        # #219 seam 9: this bite USED to assert Q6 was the one unanswered card. Dave answered
        # it — '55 gates' — so the assertion INVERTS rather than being deleted: the card must
        # now carry a receipt, and the page must have nothing left to ask.
        _a6 = q6[0].get("answered") or {}
        bite("questions/Q6-is-answered", bool(_a6), True,
             "Dave answered the roster card at #219; the card must carry his answer")
        bite("questions/Q6-receipt-names-the-count", "55" in _a6.get("position", ""), True,
             "the receipt must state the roster he ruled")
        # #219 seam 9 stage 2: the conductor inscribed the Q6 clause as s219-D9, so the OWED
        # register comes OFF this card — a card still saying OWED after the clause lands tells
        # Dave his written ruling is unwritten, the inverse lie of the one OWED prevents. And
        # the citation is proved against the STORE, not against this file's own dict: citing a
        # ruling whose entry does not carry the clause is the false-inscription class
        # [[memento-framing]] [[no-gate-parses-the-artefact]].
        bite("questions/Q6-inscription-flag-is-off", "inscription" in _a6, False,
             "s219-D9 is in the store; the card must no longer carry the OWED register")
        bite("questions/Q6-cites-the-inscribed-ruling", _a6.get("ruling"), "s219-D9",
             "the receipt cites the clause the conductor inscribed, not the chat")
        _store = json.load(open(os.path.join(ROOT, "knowledge", "_rulings.json"),
                                encoding="utf-8"))
        _d9 = [r for r in _store.get("rulings", []) if r.get("id") == "s219-D9"]
        bite("questions/Q6-cited-ruling-is-in-the-store", len(_d9), 1,
             "the card cites s219-D9 — the store must actually hold it")
        bite("questions/Q6-cited-ruling-carries-the-count",
             bool(_d9) and "55" in _d9[0].get("says", ""), True,
             "the cited entry must itself carry the 55-gate clause — cite-without-clause is "
             "the confident FALSE inscription this page exists to refuse")
        bite("questions/no-card-is-still-asking",
             [q["id"] for q in OPEN_QUESTIONS if not q.get("answered")], [],
             "every card on the pre-bake page is answered; a page that still asks is not ready "
             "to bake")
        for gname in Q6_DROPPED_GATES:
            bite("questions/Q6-names:%s" % gname, gname in body6, True,
                 "the roster card must state the dropped gate by name")
            bite("questions/Q6-gate-exists:%s" % gname,
                 os.path.exists(os.path.join(ROOT, "knowledge", gname)), True,
                 "the card names a file that is no longer in the repo — re-derive it")
        # THE CARD'S PREMISE, PROBED. Q6 exists only because the probe classified the evidence
        # linter REPO-BOUND. If that verdict ever moves, the card is describing a cut that did
        # not happen. [[premise-ages-faster-than-rule]]
        _pp = os.path.join(HERE, "_pack_gate_probe.json")
        if os.path.exists(_pp):
            _pg = {g["gate"]: g["verdict"] for g in json.load(open(_pp))["gates"]}
            bite("questions/Q6-premise-evidence-is-repo-bound",
                 _pg.get("_validate_evidence.py"), "REPO-BOUND",
                 "Q6 says the evidence linter dropped out as REPO-BOUND — the probe must agree")
        bite("questions/Q6-two-readings", len(q6[0]["options"]), 2,
             "correct-as-is / ship-anyway-and-refuse")
        bite("questions/Q6-decides-nothing",
             [o for o in q6[0]["options"] if "recommended" in o], [],
             "the roster card must not pre-select a disposition — s219-D4(2) makes the cut Dave's")

    # ---- THE DECLARED INVOCATIONS (#219 N2 -> N1 handoff). A typed invocation is a claim, so
    # the gate it names must exist and the probe must be able to disown it when it does not work.
    for g, inv in DECLARED_INVOCATIONS.items():
        bite("invocation/gate-exists:%s" % g,
             os.path.exists(os.path.join(ROOT, "knowledge", g)), True,
             "a declared invocation names a gate that is not in the repo — re-derive it")
        bite("invocation/is-a-flag:%s" % g, inv.startswith("-"), True)
    bite("invocation/rejection-is-seen",
         flag_rejected("--check", "! cannot read --check: [Errno 2] No such file"), True,
         "a flag read as a FILENAME must be disowned, not shipped as a verdict")
    bite("invocation/legit-mention-is-not-a-rejection",
         flag_rejected("--check", "TYPE RATCHET CHECK PASS — declared debt holds at 1091 "
                                  "(0 new); run --check in CI"), False,
         "a gate naming its own flag in a summary must not read as a rejection")
    _runner = open(os.path.join(ROOT, "apollo-spider", "ci-template", "run-gates.py"),
                   encoding="utf-8").read()
    bite("invocation/runner-reads-the-manifest", 'v.get("invocation")' in _runner, True,
         "the pack's runner must take the argv from the manifest, not from a convention")
    bite("invocation/runner-passes-it", "run_one(path, cwd, pack, a.timeout, argv)" in _runner,
         True, "the runner must actually PASS the argv it read")

    # ---- THE PACK GATE (s219-D5 Q3, #219 N1). The canon generators ship, and a designer who
    # reaches for one is warned — IN THE PACK ONLY. Both halves are DRIVEN, in real processes:
    # a no-op here cannot be proved by reading the marker check, and a warning that only exists
    # in a docstring is not a warning [[mutation-tests-the-clause-not-the-feature]].
    import _helpgate as _hg
    CANON_GENS = ["knowledge/canon/gen_canon_tokens.py",
                  "knowledge/canon/gen_canon_components.py",
                  "knowledge/canon/gen_canon_bento.py",
                  "knowledge/canon/gen_theme_cascade.py"]
    for g in CANON_GENS:
        _gsrc = open(os.path.join(ROOT, g), encoding="utf-8").read()
        bite("packguard/wired:%s" % os.path.basename(g),
             "_pack_gate(__file__" in _gsrc, True,
             "a canon generator that ships must ask the pack gate")
        # ⛔ #219 seam 8. `pack_gate` HAS a `name` guard and it DEFAULTS to "__main__", so a call
        # site that omits `name=__name__` gets the guard's value without the guard's meaning: the
        # refusal fires on IMPORT as well as on run. Measured cost — two shipped gates
        # (`_validate_state_snap.py`, `_gate_minted_consumption.py`) IMPORT `gen_theme_cascade`
        # and both went RED (exit 2) inside a real baked pack. Neither lane's proof could see it:
        # N1 drove the generators as SCRIPTS, and N2's stage had no `_MANIFEST.json` marker at its
        # root so the guard never fired there at all. The wiring bite above is therefore not
        # enough — the ARGUMENT is the clause [[mutation-tests-the-clause-not-the-feature]].
        bite("packguard/guard-is-argued:%s" % os.path.basename(g),
             "name=__name__" in _gsrc, True,
             "the pack gate must be told __name__, or it refuses importers too")
        bite("packguard/repo-is-not-a-pack:%s" % os.path.basename(g),
             _hg.pack_root(os.path.join(ROOT, g)), None,
             "the marker must NOT be found in this repo — that is what keeps repo behaviour "
             "unchanged on the same bytes")

    tmp = tempfile.mkdtemp(prefix="packguard-", dir="/var/tmp")
    try:
        def _fake_pack(where, schema=SCHEMA):
            os.makedirs(os.path.join(where, "knowledge", "canon"), exist_ok=True)
            shutil.copy(os.path.join(ROOT, "knowledge", "_helpgate.py"),
                        os.path.join(where, "knowledge", "_helpgate.py"))
            if schema is not None:
                with open(os.path.join(where, "_MANIFEST.json"), "w") as f:
                    json.dump({"schema": schema, "version": VERSION}, f)
            gen = os.path.join(where, "knowledge", "canon", "gen_fake.py")
            with open(gen, "w") as f:
                f.write('"""fake canon generator."""\n'
                        'import os as _o, sys as _s\n'
                        '_d = _o.path.dirname(_o.path.abspath(__file__))\n'
                        'while _d != "/" and not _o.path.exists(_o.path.join(_d, "_helpgate.py")):\n'
                        '    _d = _o.path.dirname(_d)\n'
                        '_s.path.insert(0, _d)\n'
                        'from _helpgate import pack_gate as _pg\n'
                        '_pg(__file__, name=__name__, what="canon")\n'
                        'VALUE = 42\n'
                        # shaped like a real canon generator: the WORK is under __main__, the
                        # shared definitions are importable. That is why the import arm is a
                        # real question rather than a trivially true one.
                        'if __name__ == "__main__":\n'
                        '    print("MINTED", _s.argv[1:])\n')
            return gen

        def _consumer(where, gen):
            """A shipped GATE that IMPORTS a canon generator — the shape that broke."""
            c = os.path.join(where, "knowledge", "gate_fake_consumer.py")
            with open(c, "w") as f:
                f.write('"""a gate that imports the generator for its single source of truth."""\n'
                        'import os as _o, sys as _s\n'
                        '_s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'
                        ' "canon"))\n'
                        'from %s import VALUE\n'
                        'print("GATE RAN", VALUE)\n' % os.path.basename(gen)[:-3])
            return c

        def _drive(gen, *argv):
            r = subprocess.run([sys.executable, gen] + list(argv),
                               capture_output=True, text=True)
            return r.returncode, r.stdout + r.stderr

        inside = _fake_pack(os.path.join(tmp, "Apollo-Spider-v1.0.0"))
        rc, out = _drive(inside)
        bite("packguard/refuses-in-a-pack", (rc, "REFUSED (pack-gate)" in out), (2, True),
             "inside a pack the generator must refuse, loud and named: " + out[-300:])
        _flat = " ".join(out.split())   # the warning is WRAPPED for a terminal; the claim is
        bite("packguard/carries-daves-framing",              # about the words, not the wrapping
             "canon that never passed a gate" in _flat, True,
             "the warning must carry the framing the ruling quotes, not a paraphrase")
        bite("packguard/names-the-hatch", "--i-understand" in out, True,
             "a refusal must name the flag that proceeds")
        bite("packguard/minted-nothing", "MINTED" in out, False,
             "the refusal must fire BEFORE the generator does its work")

        # ---- THE IMPORT ARM (#219 seam 8). The refusal is for someone RUNNING the generator.
        # A shipped gate that imports it for a shared definition is not re-minting anything, and
        # must be untouched. Driven inside the SAME fake pack, so the marker is genuinely found.
        rc, out = _drive(_consumer(os.path.join(tmp, "Apollo-Spider-v1.0.0"), inside))
        bite("packguard/import-is-a-no-op", (rc, "GATE RAN 42" in out), (0, True),
             "a gate that IMPORTS a canon generator inside a pack must not be refused — this is "
             "the arm that catches a call site which forgot `name=__name__`: " + out[-300:])
        bite("packguard/import-does-not-mint", "MINTED" in out, False,
             "importing must not run the generator's own work either")

        rc, out = _drive(inside, "--i-understand", "--only", "x")
        bite("packguard/flag-proceeds", (rc, "MINTED" in out), (0, True),
             "--i-understand must let the run through: " + out[-300:])
        bite("packguard/flag-is-consumed", "MINTED ['--only', 'x']" in out, True,
             "the acknowledgement flag must not survive into the generator's own argv: "
             + out[-200:])

        outside = _fake_pack(os.path.join(tmp, "not-a-pack"), schema=None)
        rc, out = _drive(outside)
        bite("packguard/no-marker-is-a-no-op", (rc, "MINTED" in out), (0, True),
             "with no pack marker the guard must be invisible: " + out[-300:])

        wrong = _fake_pack(os.path.join(tmp, "wrong-schema"), schema="something-else/9")
        rc, out = _drive(wrong)
        bite("packguard/wrong-schema-is-not-a-pack", (rc, "MINTED" in out), (0, True),
             "a stray _MANIFEST.json must not be mistaken for a pack: " + out[-300:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- determinism: canonical() is order-independent
    a = canonical({"b": 1, "a": [3, 2]})
    b = canonical({"a": [3, 2], "b": 1})
    bite("canonical/stable", a, b)
    bite("canonical/mutation", canonical({"a": [2, 3], "b": 1}) != a, True,
         "a real content change MUST change the bytes")

    # ---- deterministic_zip: same stage twice ⇒ identical bytes; a content change ⇒ different
    tmp = tempfile.mkdtemp(prefix="packziptest-", dir="/var/tmp")
    try:
        st = os.path.join(tmp, "stage")
        os.makedirs(os.path.join(st, "sub"))
        open(os.path.join(st, "a.txt"), "w").write("alpha\n")
        open(os.path.join(st, "sub", "b.txt"), "w").write("beta\n")
        z1 = deterministic_zip(st, os.path.join(tmp, "1.zip"), 1700000000, prefix="pack")
        os.utime(os.path.join(st, "a.txt"), (0, 0))          # mtime noise MUST NOT matter
        z2 = deterministic_zip(st, os.path.join(tmp, "2.zip"), 1700000000, prefix="pack")
        bite("zip/reproducible", sha256_file(z1), sha256_file(z2))
        with zipfile.ZipFile(z1) as _z:
            bite("zip/single-root", sorted({n.split("/")[0] for n in _z.namelist()}), ["pack"])
        open(os.path.join(st, "a.txt"), "w").write("alphaX\n")
        z3 = deterministic_zip(st, os.path.join(tmp, "3.zip"), 1700000000, prefix="pack")
        bite("zip/mutation", sha256_file(z3) != sha256_file(z1), True,
             "a content change MUST change the zip — otherwise the check is vacuous")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("selftest: %d bites, %d fail(s)" % (n[0], len(fails)))
    for f in fails:
        print("  RED " + f)
    return not fails


# ---------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--stage")
    ap.add_argument("--zip")
    ap.add_argument("--check")
    ap.add_argument("--page", help="write Dave's go/no-go page to this path")
    ap.add_argument("--zip-bytes", type=int, help="--page: the proved zip size, in bytes")
    ap.add_argument("--zip-sha", help="--page: the proved zip fingerprint")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--commit")
    ap.add_argument("--out")
    ap.add_argument("--only", help="probe only these gate basenames (comma separated)")
    ap.add_argument("--probe-stage", help="reuse an existing probe stage dir")
    ap.add_argument("--full-stage", help="a git-archive stage of the WHOLE commit, for the "
                                         "differential arm (never the repo itself)")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(0 if selftest() else 1)

    if a.probe:
        if not a.commit:
            print("REFUSED: --probe needs --commit <sha> (a probe of 'the tree' is a probe of "
                  "nothing reproducible)", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        if a.full_stage and os.path.abspath(a.full_stage) == ROOT:
            print("REFUSED: --full-stage may not be the repo itself — a validator that writes "
                  "an audit file would dirty the tree (#158 write-by-default class).",
                  file=sys.stderr)
            sys.exit(2)
        probe, tmp = probe_gates(sha, stage_root=a.probe_stage, verbose=a.verbose,
                                 full_stage=a.full_stage,
                                 only=set(a.only.split(",")) if a.only else None)
        out = a.out or PROBE_PATH
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(canonical(probe))
        print("probe -> %s (stage %s)" % (out, tmp))
        return

    if a.manifest:
        if not a.commit:
            print("REFUSED: --manifest needs --commit <sha>", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        if not os.path.exists(PROBE_PATH):
            print("REFUSED: no gate probe at %s — run --probe first. The gate verdicts are "
                  "MEASURED; a manifest that guessed them would be prose." % PROBE_PATH,
                  file=sys.stderr)
            sys.exit(2)
        probe = json.load(open(PROBE_PATH))
        if probe["commit"] != sha:
            print("REFUSED: the gate probe was run at %s, not %s. Re-probe."
                  % (probe["commit"][:12], sha[:12]), file=sys.stderr)
            sys.exit(2)
        man = build_manifest(sha, probe)
        # The totals must be the count of DISTINCT shipped paths. A group table that let a path
        # be owned twice would inflate the size on Dave's go/no-go page — the number he is
        # ruling on has to be the number the bake produces.
        if len(all_paths(man)) != man["totals"]["files"]:
            print("REFUSED: totals say %d files but the distinct path set is %d — a path is "
                  "owned by two groups." % (man["totals"]["files"], len(all_paths(man))),
                  file=sys.stderr)
            sys.exit(2)
        text = canonical(man)
        out = a.out or MANIFEST_PATH
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(text)
        print("manifest -> %s" % out)
        print("  commit %s  files %d  bytes %d  sha256 %s"
              % (sha[:12], man["totals"]["files"], man["totals"]["bytes"],
                 manifest_hash(text)[:16]))
        return

    if a.page:
        text = open(MANIFEST_PATH).read()
        man = json.loads(text)
        html = render_page(man, zip_bytes=a.zip_bytes, zip_sha=a.zip_sha,
                           man_sha=manifest_hash(text))
        os.makedirs(os.path.dirname(os.path.abspath(a.page)), exist_ok=True)
        open(a.page, "w").write(html)
        print("page -> %s (%d bytes)" % (a.page, len(html)))
        # ⛔ #220: THE RECIPE, AT THE MOMENT IT IS NEEDED AND WITH THE PATH THAT EXISTS.
        # Writing this page REWRITES Dave's review surface and strips the review pair's
        # stamps, so the overlay has to be re-injected or he opens a page with no comment
        # pins on it (#219 R2's item 5). The #219 stage-2 recipes told the conductor to run
        # `knowledge/_make_review.py`, which has never existed — the injector is and always
        # was `knowledge/_review/_make_review.py`, and a conductor following the block
        # verbatim got `No such file or directory` [[read-chain-is-where-staleness-is-free]].
        # It is printed here, by the tool that causes the need, rather than left in a report.
        print("  NEXT: python3 knowledge/_review/_make_review.py %s" % a.page)
        print("        (this write stripped the review pair's stamps — re-inject the overlay)")
        return

    if a.stage:
        if not a.commit:
            print("REFUSED: --stage needs --commit <sha>", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        man = json.load(open(a.out or MANIFEST_PATH))
        if man["commit"] != sha:
            print("REFUSED: manifest is for %s, you asked for %s"
                  % (man["commit"][:12], sha[:12]), file=sys.stderr)
            sys.exit(2)
        extract(sha, all_paths(man), a.stage)
        apply_seed_map(a.stage)          # seed map FIRST — see pack_path
        flatten_stage(a.stage)
        # THE IMPORT CLOSURE, last: it copies within the flattened stage, so it must run after
        # both moves or it would fill a directory the flatten is about to rename (#220).
        seeds = man.get("import_closure", {}).get("seeds", [])
        apply_closure(a.stage, seeds)
        print("staged %d paths + %d import-closure copies -> %s "
              "(pack surfaces flattened to the root — see pack_path)"
              % (len(all_paths(man)), len(seeds), a.stage))
        for s in seeds:
            print("  closure: %s  <- %s  (for %s)"
                  % (s["dest"], s["src"], ", ".join(s["needed_by"])))
        return

    if a.zip:
        if not a.commit or not a.out:
            print("REFUSED: --zip needs --commit and --out", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        deterministic_zip(a.zip, a.out, commit_epoch(sha),
                          prefix=os.path.basename(os.path.normpath(a.zip)))
        print("%s  %s" % (sha256_file(a.out), a.out))
        return

    if a.check:
        if not a.commit:
            print("REFUSED: --check needs --commit <sha>", file=sys.stderr)
            sys.exit(2)
        sha = resolve_commit(a.commit)
        man = json.load(open(MANIFEST_PATH))
        fails = check_pack(a.check, man, sha)
        if fails:
            print("CHECK RED — %d problem(s):" % len(fails))
            for f in fails:
                print("  " + f)
            sys.exit(1)
        print("CHECK GREEN — %s matches the manifest at %s" % (a.check, sha[:12]))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
