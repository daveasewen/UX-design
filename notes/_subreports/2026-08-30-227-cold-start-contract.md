# #227 lane 7 — the cold-start contract

Opus build sub · conductor Fable · 2026-08-30 · no commits, no store rows, no rulings.

## COUNTS

- **built 7** — `apollo-spider/cold-start/{DESIGN-CONTRACT.md, gen_projections.py,
  verify_placement.py, REPORT-TEMPLATE.md}` + 3 generated projections under
  `cold-start/projections/`.
- **retuned 7** — six `SKILL.md` `description:` frontmatter lines (all six that ship, not
  five — see the premise correction below) + grill-me's *When to run this* section.
- **ruling-shaped 5** — listed below; none of them taken here.
- **UNPROVEN 3** — listed below.

## What was built, and what is proven about it

`DESIGN-CONTRACT.md` — **30 lines**, against a 40-line budget that is now MACHINE-ENFORCED
rather than remembered: `gen_projections.py` refuses to write anything at all from an
over-budget source, and says by how much. Order is the brief's: declare the lane, grill
first, the five rules inline, scope, the report pointer, then the six questions compact.
On-canon is written as the default and freestyle as the designer's explicit word.

`gen_projections.py` — one source, three host files, one `render()` used by the writer, the
checker and the selftest so they cannot disagree about correct. `--check` is byte-derived
over the whole file. `--selftest` is **7 arms**: fresh tree green, idempotent, hand-edited
body red, stripped header red, deleted projection red, over-budget source refuses AND
writes nothing, shipped contract inside budget. All green.

The `--check` red path was **driven at the CLI, not only inside the selftest** — twice, and
the second time on a drift I had not planted (a header reword mid-build), which is the only
kind of evidence worth much [[mutation-tests-the-clause-not-the-feature]].

No `_helpgate` import. The shared gate resolves by walking up for `_helpgate.py`; from
`cold-start/` that walk finds nothing **in the repo and nothing in an unzipped pack either**
(measured: `_helpgate.py` exists only at `knowledge/` and `apollo-spider/gumdrop/`). Rather
than ship an import that works on one side of the release boundary, the `-h/--help` guard is
inlined in both scripts with the same contract. Noted in each docstring.

`verify_placement.py` — advisory, exits 0 always, on every arm of the designer-facing run
(driven on a cold directory: exit 0, three NO RULES rows, copy-into-place lines). Its
`--selftest` arm does exit 1 on failure, deliberately: that arm is the build-time checker,
not the designer's run, and a checker nobody has watched go red has proved nothing. Said so
in the docstring.

Its useful state is the middle one: **a file that exists but does not carry the contract**
(an older instructions file, or a merge that dropped it) reads as NO RULES, not as a pass.
A `MARKER` constant does that, and selftest arm 1 asserts the marker is still present in
`DESIGN-CONTRACT.md` — so a reword of the contract cannot silently blind the checker
[[instrument-without-a-consumer]].

`REPORT-TEMPLATE.md` — four boxes. Box 2 is *what lane was declared*, with "nothing
declared" named as the most useful possible answer. That is the false-report killer.

## Hook-word retune

Every existing trigger kept; phrases added, never replaced. Every added phrase is
design-output-shaped, and each clause is bounded to design output so it cannot claim
non-design work:

| skill | shape of what was added |
|---|---|
| generate-from-canon | "build me a dashboard", "make a page", "create a form", "add a card to this screen" — bounded by *whenever the thing being asked for IS a piece of UI* |
| draft-a-new-pattern | "we need a component the system doesn't have", "design a new pattern" — bounded by *the output is UI and nothing in the library fits* |
| grill-me | "new design project", "make this look like our brand", "which theme should we use" — **and explicitly: skip it, silently, when a current brief already exists** |
| check-against-design-system | "does this match our design system", "why does this look off" — bounded to *an existing screen or component* |
| check-with-gates | "check my work", "is this accessible", "is this ready to share" |
| usability-review | "is this usable", "what's confusing here" — bounded to *the experience rather than the construction* |

⚠ *new project* alone was deliberately NOT used for grill-me — a new **code** project would
fire it. Every occurrence is *new design project* / *new design task*.

All six frontmatter blocks re-parsed with PyYAML after editing; descriptions 516–713 chars.
Diff scope confirmed: five files changed one line each, grill-me changed its description and
its trigger section only. No skill body otherwise touched.

**grill-me's brief-file state rule** is now load-bearing prose, not an aside. `briefs/` is
named as the trigger — *"That folder is the trigger, not the shape of the request"* — with
the explicit instruction that a current brief means the skill is finished: do not ask, do not
mention it. And the consequence is stated in the file, because that is what makes it stick:
a grill that re-fires on every prompt is one a designer turns off within the hour, and they
turn off everything else with it.

## PREMISE CORRECTION — six skills ship, not five

The brief says "the five `apollo-spider/skills/*/SKILL.md` files (incl. grill-me)". Measured
at HEAD: **six** are tracked. `grill-me/SKILL.md` was born earlier today (`365db63`, #227
lane 1) and the ratified manifest is at `1e028a1b`, which predates it — hence its
`skills` group reads `files: 5`. All six were retuned [[premise-ages-faster-than-rule]].

## EXPECTED PACK-MANIFEST DELTA (measured, by driving `groups()` — not read by eye)

**No manifest was regenerated.** These are the deltas a regen WILL produce, and one of them
is a defect that predates this lane.

1. **`skills` group: 5 → 6 files.** `apollo-spider/skills/grill-me/SKILL.md` is claimed and
   flattens to `skills/grill-me/SKILL.md`. The group's `plain` prose still says *"The five
   Spider skills"* and its `status` says *"four rewritten … one new"* — both will read false
   at six. Prose, in a manifest, so not touched here.

2. ⛔ **All 7 `cold-start/` files are UNCLAIMED by every group — they would NOT ship.**
   Probed directly against the live group table:

   ```
   UNCLAIMED  apollo-spider/cold-start/DESIGN-CONTRACT.md
   UNCLAIMED  apollo-spider/cold-start/gen_projections.py
   UNCLAIMED  apollo-spider/cold-start/verify_placement.py
   UNCLAIMED  apollo-spider/cold-start/REPORT-TEMPLATE.md
   UNCLAIMED  apollo-spider/cold-start/projections/CLAUDE.md
   UNCLAIMED  apollo-spider/cold-start/projections/AGENTS.md
   UNCLAIMED  apollo-spider/cold-start/projections/.github/copilot-instructions.md
   ```

   `gumdrop` matches only `apollo-spider/gumdrop/`, `FIRST-SESSION.md`, `.github/`,
   `.vscode/`; `skills` matches only `*/SKILL.md`. So the entire deliverable is invisible to
   the ship list until a group claims it — the exact [[forgotten-document-class]] shape, and
   the reason it is written down here rather than assumed. Either widen `gumdrop` or mint a
   `cold-start` group (ruling-shaped, §2 below). `pack_path()` already lands them correctly
   at `cold-start/…` under the pack root once claimed, which is the path every doc I wrote
   assumes — verified through the same function the stager and `--check` both read.

3. ⛔ **`apollo-spider/skills/grill-me/brief-template.md` is UNCLAIMED and would NOT ship**
   — while `grill-me/SKILL.md` instructs *"Use the shape in `brief-template.md`, beside this
   file."* The `skills` match is `endswith("/SKILL.md")`, so a companion file beside a skill
   cannot be claimed by anything. Born with lane 1 today; not this lane's to fix, but it
   would ship a skill pointing at a file that is not in the pack.

4. ⛔ **grill-me is absent from the two places Copilot actually looks.** There is no
   `.github/prompts/grill-me.prompt.md` (the other five all have one) and grill-me is missing
   from the skills table in `apollo-spider/.github/copilot-instructions.md`. On the primary
   corp path, the skill this whole contract front-loads is unreachable as a slash command and
   unlisted at boot. Not fixed here — `.github/` is shipped release surface and adding a file
   moves the `gumdrop` group's list. Priced: two small files, one table row.

## RULING-SHAPED — 5, none taken

1. **Placement of the copilot projection.** The pack already ships
   `apollo-spider/.github/copilot-instructions.md` (the Memento boot rules). My projection is
   the DESIGN contract — a different document with a different job. Merged into that file, or
   kept separate? The generator deliberately owns `cold-start/projections/` and nothing else,
   so either answer is one line of placement work.
2. **How `cold-start/` is claimed by the manifest** — widen `gumdrop`, or a new named group.
   A named group is what puts it on Dave's go/no-go page and makes it auditable if it ever
   drops out of a cut, which is the argument the `gumdrop` group itself records.
3. **Does `verify_placement.py` join `ci-template/run-gates.py`?** It is advisory by
   construction; a designer who never runs it gets no warning at all.
4. **On-canon as the default lane.** Written that way on Dave's direction ("the design skill
   is basically enforced"), but which lane is the default IS the ruling, and it is his.
5. **The grill-me Copilot gap** (delta 4 above) — fix inside this release or after.

## UNPROVEN — 3

1. **The hook words have never been driven against a cold host.** No Copilot here and no
   fresh Claude session; the retune is reasoned from the phrasing designers use, not measured
   against real matching behaviour. The honest test is Dave typing "build me a dashboard"
   into a fresh session with the pack open and reporting which skill, if any, fired.
2. **The contract has never been read by a cold assistant.** That it actually stops
   improvisation is the claim the whole lane rests on and it is untested. Cheapest proof:
   place the projections in a scratch project, open a fresh session, one short prompt, see
   whether the first reply declares a lane.
3. **The 40-line budget is enforced but its premise is asserted.** "Hosts truncate or readers
   skim past 40 lines" is a reasonable design instinct, not a measurement. The gate is worth
   having either way; the number is not evidence-backed.

## REPLAY-THESE

- Nothing forbidden was touched. Confirmed by `git status`: six modified `SKILL.md`, one
  untracked `apollo-spider/cold-start/`. No `memento-package/`, `dist/`, manifest, ledger,
  `_CHAIN.md`, `_state.json`, `_rulings.json`, canon, snippet or token file.
- ⛔ **Do not regenerate any manifest to "pick up" the new files.** The delta is written out
  above so the conductor can rule on the group question first — a regen before that ruling
  ships the `skills` prose correction and still silently drops all 7 cold-start files.
- The three commands, all green at hand-off:
  `python3 apollo-spider/cold-start/gen_projections.py --check`
  `python3 apollo-spider/cold-start/gen_projections.py --selftest`
  `python3 apollo-spider/cold-start/verify_placement.py --selftest`
- `TMPDIR=/dev/shm` was needed for the selftests on this VM (disk 100% full). The scripts use
  `tempfile`, which honours `TMPDIR`, so no code change is involved — but a green selftest on
  a full disk needs that env var set.
