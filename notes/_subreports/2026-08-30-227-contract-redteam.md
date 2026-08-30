# #227 lane 8 — RED TEAM: the cold-start contract

Opus adversarial sub (s204-D1 verifier role) · conductor Fable · 2026-08-30.
Nothing edited. No commits, no store rows, no rulings. This file is the only write.

## COUNTS

**findings 21 · BLOCKING 2 · SHARP 13 · NIT 6 · UNPROVEN 4**

## VERDICT

**DO NOT SHIP** — B1 and B2 are not fix-later items; they are the difference between a
release that carries this lane and one that does not.

> Dave: the contract is good and the machinery is honest, but on Tuesday it does not reach
> a single designer — the ship list claims none of `cold-start/`, and Copilot, the primary
> path, can only get the contract by overwriting the pack's own boot file.

---

## What survived the attack (credit where it is due)

Recorded first, because the findings below are otherwise unbalanced.

- **`gen_projections.py --check` could not be fooled on drift.** Body edit, stripped header,
  deleted file, empty file — all red, all driven at the CLI. The one-`render()`-function
  discipline holds.
- **Truncation ordering is RIGHT.** At 15 lines the projection still carries the lane rule,
  the grill rule, and *all five* rules — line 15 is `- **Check before you show.**`. Whatever
  a host cuts, it cuts the scope clause and the six questions, not the rules. That ordering
  was worth getting right and it was got right.
- **The over-budget refusal is real** — 43 lines, `write rc=2`, nothing written, the number
  named.
- **`verify_placement.py` really is always-0 on the designer path**, on every arm I could
  drive including a garbage root.
- **The #224-style triage works when the brief exists.** "The corners are broken, it's all
  square" → box 3 → a brief whose Q1 reads *skipped — Mono* closes the report in one read.
  Boxes 2 and 3 are the right two boxes. The attacks below are on the edges of that, not on
  the idea.

---

# BLOCKING

## B1 — the entire deliverable is not in the ship list. Nothing in `cold-start/` reaches a designer.

**DRIVEN**, not read by eye — the live group table from
`knowledge/_release/_gen_pack_manifest.py`, `groups()`, called against the candidate paths:

```
DROPPED apollo-spider/cold-start/DESIGN-CONTRACT.md            []
DROPPED apollo-spider/cold-start/gen_projections.py            []
DROPPED apollo-spider/cold-start/verify_placement.py           []
DROPPED apollo-spider/cold-start/REPORT-TEMPLATE.md            []
DROPPED apollo-spider/cold-start/projections/CLAUDE.md         []
SHIPS   apollo-spider/skills/grill-me/SKILL.md                 ['skills']
```

`gumdrop` matches `apollo-spider/gumdrop/`, `FIRST-SESSION.md`, `.github/`, `.vscode/`;
`skills` matches `apollo-spider/skills/**/SKILL.md`. No group claims `cold-start/`, and
there is **no unclaimed-path check anywhere in the generator** — I grepped for
`claimed|unclaimed|coverage|orphan`; the only "claimed by nobody" bite is the photography
fence (line 2838). So the drop is silent: `--manifest` goes green, Dave's go/no-go page
shows nothing missing.

Compounding: `apollo-spider/cold-start/` is **untracked** (`git status`: `?? apollo-spider/
cold-start/`), and the bake stages from a named commit via `git archive`. Two independent
reasons it ships zero files.

Second-order: contract §5 — *"fill in `cold-start/REPORT-TEMPLATE.md`"* — is a dangling
path even if a designer hand-copies a projection into place.

The build report declares this (§EXPECTED PACK-MANIFEST DELTA 2). **A declared gap in a
filed report is not a shipped file**, and the release is Tuesday. That is why it is graded
BLOCKING rather than credited as handled.

**Minimal edit** — `knowledge/_release/_gen_pack_manifest.py`, a new group placed *before*
`skills` (same ordering argument the `gumdrop` group's own comment makes):

```python
dict(key="cold-start", group="cold-start", title="The cold-start design contract",
     plain="The one-page contract every host reads before it builds — the source, the "
           "three host projections, the generator that keeps them byte-identical, the "
           "placement checker, and the four-box problem report.",
     match=lambda p: p.startswith("apollo-spider/cold-start/")),
```

plus `git add apollo-spider/cold-start/`. A named group (not widening `gumdrop`) is what
puts it on Dave's page and makes a future silent drop visible — the argument the `gumdrop`
group already records for itself.

---

## B2 — on Copilot, the primary corp path, the contract is either absent or arrives by destroying the pack's boot file.

Copilot reads `.github/copilot-instructions.md`. The pack **already ships one** — the
Memento boot rule, the operating rules, the skills table, and the pointer to the five
`.github/prompts/` slash-command shims. The projection targets the identical path. **No
merged file exists anywhere in the tree.**

**DRIVEN** — `verify_placement.py --root` against the shipped pack layout (which is the
workspace FIRST-SESSION.md tells the designer to open: *"Open **this pack's folder** as your
VS Code workspace"*):

```
  NO RULES   .github/copilot-instructions.md GitHub Copilot — the file exists but the design contract is not in it
  ...
  Copy the projections into place:
    cold-start/projections/.github/copilot-instructions.md  ->  .github/copilot-instructions.md
```

The tool does not merely fail to help — it **instructs the designer to overwrite** the boot
rule, the skills table and the prompt-file bridge, and it does so in the one layout the pack
tells them to work in. A designer who follows the tool's own remedy line loses "good
morning", loses the chain read, and loses every slash command. A designer who does not
follow it gets no contract on Copilot at all, because Copilot does not read `CLAUDE.md` and
the pack ships no root `AGENTS.md`.

There is no third shipped state. The build report names this as ruling-shaped question 1
("Merged into that file, or kept separate?"). Left open, Tuesday ships one of two broken
states.

**Minimal edit — two lines, both cheap:**

1. Prepend the contract to the shipped `apollo-spider/.github/copilot-instructions.md`,
   above `# Copilot instructions — Apollo, and Memento`, and let the copilot projection be
   *that* merged file rather than a standalone. (The generator can own the merge: render the
   copilot host as `contract + "\n\n---\n\n" + existing`.)
2. `verify_placement.py` `report()`, the copilot row of the remedy block:

   before: `out("    cold-start/projections/%s  ->  %s" % (rel, rel))`
   after (for a row whose state is `no-contract`):
   `out("    MERGE cold-start/projections/%s INTO %s — do not overwrite it, that file may already carry other rules" % (rel, rel))`

**BELIEVED, not observed here** (worth checking before choosing the fix): current VS Code
Copilot also reads `AGENTS.md` at the workspace root, and supports
`.github/instructions/*.instructions.md` with `applyTo` globs. If either holds in the
designer's build, shipping the contract as `.github/instructions/apollo-design.instructions.md`
dissolves the collision entirely and is the cheapest answer. I could not drive Copilot here.

---

# SHARP

## S1 — rule 1's escape hatch defeats the report template's own discriminator.

Contract §1 ends: *"if you cannot reach the skills, say so plainly and follow the five rules
below by hand."* A skill-less Copilot therefore declares **on-canon** — honestly — for a
build that was pure improvisation. `REPORT-TEMPLATE.md` box 2 asks only:

> *"Did it say **on-canon** or **freestyle**? Paste the line. If it said neither, write
> **"nothing declared"** — that is the single most useful answer in this whole template."*

On exactly the reports the template exists to sort, box 2 will read **on-canon**. The
"could not reach the skills" sentence is in the transcript and the template never harvests
it.

**Minimal edit** — `REPORT-TEMPLATE.md` box 2, add one sentence after "Paste the line.":

> after: `Paste the line — and the next sentence too, if it said it could not reach the skills. An "on-canon" build that could not open a skill is the same as no rules at all, and that is the second most useful answer here.`

## S2 — the brief template teaches the null case; the skip→default line is missable.

`brief-template.md` puts the two load-bearing lines below a six-row table, unemphasised:

```
Skipped: <list the question numbers skipped, or "none">
Defaults used: <e.g. "Q1 skipped — proceeding with Mono, announced 2026-08-30", or "none">
```

and then the **filled example** — the part anyone actually copies — demonstrates:

```
Skipped: none
Defaults used: none
```

The one artefact that closes a #224 "it's all square" report in one read is shown only in
its empty form. Worse, the same fact has two homes: `grill-me/SKILL.md` says the brief
records `skipped — proceeding with Mono (announced <date>)` *in the row*, while the template
puts it in the `Defaults used:` line. Two homes for one fact (ADR-0017) means they can
disagree in a real brief.

**Minimal edit** — make the filled example show a skipped theme, and put the fact in the row:

before: `| 1 | Theme | Console — "it should feel like the newer product, softer" |`
after: `| 1 | Theme | **skipped — proceeding with Mono, announced 2026-08-30. Every corner square by design.** |`

before: `Skipped: none` / `Defaults used: none`
after: `Skipped: 1` / `Defaults used: Q1 skipped — Mono, announced before the build started`

## S3 — FIRST-SESSION.md ships a competing bug-report format that omits the discriminator.

`FIRST-SESSION.md`, § *If something goes wrong* — the page a designer actually walks on day
one — says:

> *"the most useful bug report is: what you said, what it did, and a screenshot if that is
> easier than describing it."*

No lane. No brief. No pointer to `REPORT-TEMPLATE.md`. Two report formats ship in one pack
and the one the designer will meet first is the one without the false-report killer in it.

**Minimal edit** — `FIRST-SESSION.md`, that sentence:

after: `the most useful bug report is: what you said, what it did, a screenshot — and two more lines that decide most of them: the lane the assistant declared in its first reply, and the brief from `briefs/`. `cold-start/REPORT-TEMPLATE.md` is that, as four boxes.`

## S4 — `verify_placement` guards one sentence; a gutted or inverted contract reads PLACED.

`MARKER = "Declare the lane, in your first reply."` — one sentence out of thirty lines.

**DRIVEN, three ways:**

- a file containing only `Always be nice. Declare the lane, in your first reply.` →
  `PLACED     CLAUDE.md    Claude`
- the real projection with the entire `**3. The five rules.**` block excised → `PLACED`
- a placed copy edited to `Freestyle is the default…` and `**Invent freely.**` → `PLACED`,
  and `gen_projections --check` **stayed green** (it only ever inspects the three templates
  under `cold-start/projections/`; the deployed copies are outside its world).

The docstring promises more than the code delivers: *"Present is not the same as correct,
and this is the failure a 'does the file exist' check reads as a pass."* It is kept for one
sentence and dropped for the rest. The stated failure mode — *"a merge that dropped it"* —
is precisely the merge that keeps the opening line.

**Minimal edit** — `verify_placement.py`:

before: `MARKER = "Declare the lane, in your first reply."`
after:
```python
MARKERS = ("Declare the lane, in your first reply.",   # §1 — the lane
           "**Never invent.**")                        # §3 — the rules block
```
and in `inspect()`, `if all(m in text for m in MARKERS)`, with the detail naming which one
is absent. Arm 1 of `selftest()` then asserts both are still in `DESIGN-CONTRACT.md`.

## S5 — the line budget measures the wrong unit.

**DRIVEN**: a contract of **31 lines and 23,333 bytes** (one 20k-character line appended)
wrote all three projections and passed `--check` green. The 23KB projection is what a host
would load.

The docstring states the purpose: *"Hosts truncate and readers skim; a contract that runs
long is a contract whose last rule is never read."* Hosts truncate on tokens or bytes.
Lines are not that unit. ([[measure-dont-convert-units]] — a count is not a measurement of
the thing you care about.)

**Minimal edit** — `gen_projections.py`:

before: `LINE_BUDGET = 40`
after:
```python
LINE_BUDGET = 40
BYTE_BUDGET = 4096   # what a host actually truncates on; 40 long lines is not "short"
```
and a second refusal in `read_source()` in the same shape, naming the overage in bytes.

## S6 — "Run `skills/…/SKILL.md`" is a verb a skill-less host cannot honour, and the sentence that explains it lives in a different file.

The pack's own `.github/copilot-instructions.md` carries the missing sentence:

> *"⚠ **These are not auto-loaded — you have to open them.** … **read that `SKILL.md` first
> and then follow it.**"*

The contract carries no equivalent. Its own §3 says the five rules *"hold even when no skill
is open"* — so the reader has been told skills may not be open, then told to "Run" one.
`check-with-gates` is not reading: its actual work is
`python3 ci-template/run-gates.py`. A cold host reads the markdown and reports "checked",
in good faith, having run nothing. That is the angle-1 failure mode exactly: the wrong thing
done while honestly claiming compliance.

**Minimal edit** — `DESIGN-CONTRACT.md`, §3 fifth bullet:

before: `- **Check before you show.** Run `skills/check-with-gates/SKILL.md` before you put a screen in front of anyone. An unchecked screen is a guess.`
after: `- **Check before you show.** Open `skills/check-with-gates/SKILL.md` and do what it says — it ends in `python3 ci-template/run-gates.py`, and reading the file is not running it. An unchecked screen is a guess, and so is an unrun gate.`

## S7 — rule 4 points a cold host at a file that says it is not for building from.

`knowledge/_render/_bento_edit_rails.json`, its own first keys:

> `"$what": "The bento EDIT-PASS VOCABULARY: every dial Apollo's edit pass exposes…"`
> `"$groundwork_only": "No editor is built or proposed here. This is the vocabulary such an editor would read"`

The contract says *"Layout comes from the rails in `knowledge/_render/_bento_edit_rails.json`,
not from taste."* A cold, skill-less host follows that literally, opens 38KB of dial
vocabulary, and gets no layout. (`generate-from-canon` §7 makes the same claim, so the
contract inherited it rather than invented it — but the contract is the only text a cold
host has.)

**Minimal edit** — `DESIGN-CONTRACT.md`, §3 fourth bullet:

before: `- **Dashboards are bento-first.** Layout comes from the rails in `knowledge/_render/_bento_edit_rails.json`, not from taste.`
after: `- **Dashboards are bento-first.** The procedure is in `skills/generate-from-canon/SKILL.md`; `knowledge/_render/_bento_edit_rails.json` is the dial vocabulary it reads, not a layout. Either way, not from taste.`

## S8 — precedence against the designer's own instruction files is unaddressed.

`grep -i 'precedence|other instruction|global|user-level'` across `cold-start/` returns
**nothing** (OBSERVED). A designer whose global instructions say *"never ask clarifying
questions"* now has two texts in context and no tiebreak.

**BELIEVED** (my general knowledge of host behaviour, not measured in this VM, and it should
not be presented to Dave as measured): Claude Code loads `~/.claude/CLAUDE.md` alongside the
project `CLAUDE.md`; VS Code Copilot applies user-level custom instructions alongside
`.github/copilot-instructions.md`. In both, *both* texts are present and the model resolves
the conflict by judgment — no documented rule guarantees the project file wins. So the
collision is live and its outcome is a coin toss.

**Minimal edit** — `DESIGN-CONTRACT.md`, §2, appended to the last sentence:

after: `…and say that default out loud before anything is built. If another instruction file tells you never to ask questions, say that in the same reply and still ask question 1 — the theme is the one answer nobody can guess back afterwards.`

One clause, one question, no nagging. It is also the clause that keeps the hostile
*"don't ask me questions, just build it"* case sane.

## S9 — "asks for it in words" has no test, so the hostile openers are undecided.

§1: *"Freestyle happens only when the designer asks for it in words."* Neither *"skip the
apollo stuff, my manager wants it quick"* nor *"don't ask me questions, just build it"*
contains the word. The text supports both readings — drop to freestyle, or hold the lane and
push back — and the wrong one in either direction is a real cost: fold silently and the
false reports return; hold and lecture and the pack gets turned off.

**Minimal edit** — `DESIGN-CONTRACT.md`, §1:

before: `Freestyle happens only when the designer asks for it in words.`
after: `Freestyle happens only when the designer asks for it in words. "Quickly" and "don't ask me questions" are not that ask — they shorten the grill, not the lane; say which lane you are in, once, and get on with it.`

## S10 — §4 and §1 disagree about which lane a third-party design skill is.

§1 offers exactly two lanes. §4 permits a non-Apollo skill for design output *"If you use a
non-Apollo skill to produce design output, say so in the same reply"* — and never says which
lane that is. The hostile opener *"use my company's design skill for this"* is compliant with
§4 while declaring **on-canon** under §1, which is the undeclared-source state §4 exists to
end.

**Minimal edit** — `DESIGN-CONTRACT.md`, §4:

before: `If you use a non-Apollo skill to produce design output, say so in the same reply — an undeclared source is what turns a design problem into an unreadable bug report.`
after: `If you use a non-Apollo skill to produce design output, that is freestyle: declare it in the same reply and name the skill — an undeclared source is what turns a design problem into an unreadable bug report.`

## S11 — `brief-template.md` does not ship, while the skill that ships points at it.

**DRIVEN** (same `groups()` probe): `apollo-spider/skills/grill-me/brief-template.md` →
`DROPPED []`. The `skills` match is `p.startswith("apollo-spider/skills/") and
p.endswith("/SKILL.md")`, so a companion file beside a skill cannot be claimed by anything.
`grill-me/SKILL.md` line 142 ships saying *"Use the shape in `brief-template.md`, beside this
file."* Declared by the builder (§delta 3), unfixed.

**Minimal edit** — the `skills` group match:

before: `match=lambda p: p.startswith("apollo-spider/skills/") and p.endswith("/SKILL.md")`
after: `match=lambda p: p.startswith("apollo-spider/skills/") and (p.endswith("/SKILL.md") or p.endswith("/brief-template.md"))`

## S12 — the self-sufficiency fallback points at the first thing a truncation cuts.

§2: *"If you cannot reach that skill, ask the six questions at the foot of this file
yourself."* The six questions are lines 23–32 of a 32-line projection — below the `---`,
last in the file. The host that cannot reach a skill is the same host most likely to have
truncated. The fallback's target is the least survivable part of the document.

(The ordering above line 15 is right, and I said so under *What survived*. This is the one
place it is not.)

**Minimal edit** — `DESIGN-CONTRACT.md`, §2:

before: `If you cannot reach that skill, ask the six questions at the foot of this file yourself.`
after: `If you cannot reach that skill, ask the six questions at the foot of this file yourself. If you cannot see those either, ask this one: **which theme — Mono, Common, Console or Supercharge?** It is the answer that changes every corner on the page.`

## S13 — grill-me is invisible on the Copilot path, and the shipped boot file states a false roster.

*(Counted under SHARP; it is BLOCKING-adjacent, and if B2's merge is done the contract does
reach grill-me by path — which is why it is not a third BLOCKING.)*

`apollo-spider/.github/copilot-instructions.md`: *"The **five** files under `skills/` are
written instructions"* + a five-row table with no grill-me row. `ls .github/prompts/` →
five files, no `grill-me.prompt.md`. `grep -rn grill .github/` → **nothing**. Six skills are
tracked. So at boot, on the primary path, Copilot is told a roster that omits the one skill
the whole contract routes to, and the slash command does not exist.

**Minimal edit** — two: `s/The five files under/The six files under/` plus a table row
`| starting a new design task — the six questions that decide how it will look | `skills/grill-me/SKILL.md` |`,
and a `.github/prompts/grill-me.prompt.md` copied from the shape of the other five.


---

# NIT

**N1 — `--root` at a path that is not a directory prints the tool's most alarming output.**
DRIVEN, both `--root /dev/shm/m2/NO-SUCH-DIR` and `--root cold-start/DESIGN-CONTRACT.md`:
a full, confident *"⚠ 3 of 3 hosts start COLD here"* report, exit 0, indistinguishable from
a real cold project. A typo reads as an emergency. Fix, in `run()` before `report()`:
`if not os.path.isdir(root): out("NOT A DIRECTORY: %s — nothing was inspected." % root); return 0`.

**N2 — a rogue extra file in `projections/` is invisible.** DRIVEN: `cp CLAUDE.md
GEMINI.md` → `--check` green. The generator owns the directory but does not police it. A
stale hand-made fourth projection could sit there forever.

**N3 — an empty projection reports the wrong cause.** DRIVEN: `: > AGENTS.md` → *"the
GENERATED header has been edited or lost."* Right verdict, imprecise cause; `splitlines()[:1]`
on `""` is `[]`.

**N4 — the three projections are one document in three places.** Byte-identical apart from
one word in the header comment. That is correct engineering (one source, no drift) but the
"three hosts" framing may lead Dave to expect per-host content. Worth knowing, not fixing.

**N5 — the manifest's `skills` prose will read false at six.** *"The five Spider skills"*
and *"four rewritten … one new"*. Declared by the builder; still true.

**N6 — the `AGENTS.md` collision in a designer's own repo is named nowhere.** The generator
docstring flags only the copilot merge (*"⚠ THIS PACK ALREADY SHIPS ITS OWN
`.github/copilot-instructions.md`"*). A team `AGENTS.md` is at least as common and gets no
warning at all — and this repo's own root has one, so it is not a hypothetical shape.

---

# The two cold walks, in short

**Claude / `CLAUDE.md`, "build me a dashboard".** §1 → declares on-canon. §2 → `briefs/`
absent → opens `skills/grill-me/SKILL.md` (ships; resolves from the pack root) → asks the
theme first. Designer answers → brief written → build. **This walk works.** Its failure
points are S1 (if the skills are unreachable it still says "on-canon"), S6 ("Run" the gates
skill), and S7 (rule 4's dead-end pointer). Nothing here is fatal.

**Copilot / `.github/copilot-instructions.md`, "make this screen match our brand".** The
projection is not on the machine (B1). Even placed, it is placed *over* the boot file (B2).
Assume both fixed: §2 fires — *"make this look like our brand"* is now a literal grill-me
trigger phrase — but the boot file's roster says five skills and grill-me is not among them
(S13), and there is no slash command. The request is also ambiguous between grill-me
(Q4 brand assets) and check-against-design-system (*"is this on brand"* is a listed trigger
for it). Two skills claim the same sentence. Not graded separately — the contract's §2
resolves it (grill first), and that is the right resolution.

---

# UNPROVEN — 4

1. **No cold host was driven.** No Copilot, no fresh Claude session. Every angle-1 and
   angle-2 walk above is a close reading of the text, not a measurement of behaviour. The
   builder's UNPROVEN 1 and 2 stand unchanged and I could not retire either.
2. **The truncation premise is unmeasured.** My "first 15 lines" finding is arithmetic on
   the file, not on any host's loader. Which lines a host actually loads is unknown, so both
   the credit ("ordering is right") and S12 rest on an assumed cut point.
3. **Host precedence is BELIEVED, not OBSERVED** (S8). Stated as belief in the finding; must
   not reach Dave as measured.
4. **Whether Copilot reads `AGENTS.md` or `.github/instructions/*.instructions.md`** in the
   designer's VS Code build is BELIEVED. It bears directly on B2's cheapest fix and is worth
   one check by someone with a Copilot in front of them before the merge is chosen.

---

# COUNTS, restated

- **findings 21** — BLOCKING 2 (B1, B2) · SHARP 13 (S1–S13) · NIT 6 (N1–N6).
- **UNPROVEN 4.**
- Machinery driven: `gen_projections.py --check` ✅ · `--selftest` ✅ 7 arms ·
  `verify_placement.py --selftest` ✅ 4 arms · over-budget refusal ✅ ·
  byte-budget hole ✅ red-that-stayed-green · placed-copy blindness ✅ ·
  marker-gutting ✅ · rogue-file blindness ✅ · non-directory `--root` ✅.
  `TMPDIR=/dev/shm` throughout (VM disk full); every mutation in `/dev/shm`, nothing in the
  repo touched.

# REPLAY-THESE (conductor)

- **B1 and B2 are the release.** Everything else can ship late.
- ⛔ Do not regenerate the pack manifest until the `cold-start` group question is ruled — a
  regen now ships the `skills` 5→6 prose correction and *still* silently drops all seven
  cold-start files, which would make the drop look reviewed.
- The builder's ruling-shaped questions 1 (copilot merge) and 2 (how `cold-start` is claimed)
  are the two that block. Question 3 (does `verify_placement` join `run-gates.py`?) is now
  answered by evidence: **nothing in the repo references either script** —
  `grep -rn 'gen_projections|verify_placement|DESIGN-CONTRACT|cold-start/'` across `.py .md
  .yml .sh .json` returns only a 2026-08-27 brief that means a different "cold start". No CI
  arm, no runbook, no FIRST-SESSION line. As shipped, **nobody runs either script, ever**
  ([[instrument-without-a-consumer]]). If `gen_projections --check` is not added to
  `.github/workflows/gates.yml`, the byte-derived drift guard is decoration.
- Nothing was edited. `git status` unchanged from hand-off apart from this file.
