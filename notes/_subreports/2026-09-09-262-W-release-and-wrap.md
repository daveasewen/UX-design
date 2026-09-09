# `#262`-`W` — v1.0.9 RELEASED at `dd129e8`, and the #262 capture ritual

session: `#262` · 2026-09-09
window: delegated RELEASE + WRAP sub (Opus 5)
sub index: `W`
brief: cut in chat by the conductor (Fable) at **166,436 real FILL** — **3,564 UNDER** the
`s260-D2` delegated line of 180,000.
tokens: `<declared in the stub at close — this seat's own `_checkin.py` reading>`

provenance: 262 · 2026-09-09
status: observed

## VERDICT

**v1.0.9 IS RELEASED, and the zip is byte-identical to lane O2's twice-proved dry run.**
`RATIFY_IDS["v1.0.9"] = "s262-D6"` is keyed to Dave's word *"Ratify v1.0.9"* (inscribed at
`33a6608`); the manifest was regenerated at the **same** cut commit `dd129e8` and **exactly one
line moved** — `PROPOSED` → `RATIFIED` — with the ship list unmoved at **1698 files /
45,867,344 bytes**. `--release` baked
`736d0fb034b71048e0ef7789206837afa7ef76c33330117fa0be3410c149c780`, which is **O2's dry-run
fingerprint to the byte**, so nothing was decided by the mode flag. `--check` **GREEN** against
`dd129e8efa79`. The frozen ledger is re-seeded with the version literal moved in the same story
(`v1.0.8 → v1.0.9`, apollo-spider **9 zips**, `babd4fe1b727`), so the laundering arm has nothing
to say. **The nine release gates are 9/9 GREEN.** The capture ritual ran steps 1 → 5b; step 3
(memory) is a **SEAT LIMIT**, declared not skipped, exactly as at #261.

COUNTS: findings 4 · ruling-shaped 2 · UNPROVEN 3

REPLAY-THESE: none — the stub carries everything the conductor needs to close #262. The two
ruling-shaped questions below are Dave's and are carried in `_CARRIES.md` § `residual → #263`
as items ③ and ⑥; the four findings are summarised on the ★ LATEST banner and in full in the
⏱ LATEST DELTA, so no path here needs re-reading to write the wrap.

---

## Part 1 — the release

### The key (`3cab7c3`)

The status is **DERIVED, not typed** (`s237-D9`) — read back off the module before the manifest
was touched, which is the #257/#260 order:

    v1.0.9 s262-D6 RATIFIED — s262-D6 names v1.0.9 in the store; s219-D4(2) satisfied by the
    store, not by prose

The `⛔ NO RATIFY_IDS ROW IS KEYED TO v1.0.9` comment at `VERSION` was amended in the same
commit — a comment asserting the opposite of the module's own behaviour is the
assertion-propagation class, and it sits four lines above the constant it lies about.

`_gate_frozen_release.py:130` apollo-spider row literal `v1.0.8 → v1.0.9`, in this same commit —
the **fourth version home** the gate's own comment warns about.

    rm -rf /var/tmp/full9r && mkdir -p /var/tmp/full9r && git archive dd129e8 | tar -x -C /var/tmp/full9r
    bash apollo-spider/build-designer-pack.sh --manifest --commit dd129e8 --full-stage /var/tmp/full9r
      commit dd129e8efa79  files 1698  bytes 45867344  sha256 0265deb8da0b6a04
      differential arm: ARMED — REPO-BOUND verdicts are MEASURED

★ **The manifest diff was CHECKED, not assumed** — a regeneration that quietly moved the ship
list would be a different release under the same word:

    -  "status": "PROPOSED — no ruling is keyed to v1.0.9 yet …"
    +  "status": "RATIFIED — s262-D6 names v1.0.9 in the store; …"

One line. 1698 files and 45,867,344 bytes unchanged from O2's PROPOSED manifest; only the content
hash moves (`bc10de6fdc7fa8ce` → `0265deb8da0b6a04`), because the status line is inside it. The
gate probe moved by one line too, and it is **cosmetic**: the recorded `full_stage` path
(`/var/tmp/full9p` → `/var/tmp/full9r`) — the stage directory this seat used, not a verdict.

### The bake (`b94adff`)

    bash apollo-spider/build-designer-pack.sh --release --commit dd129e8
      220 finding(s). ADVISORY — exiting 0.  (pack-docs gate; pre-existing runbook path names)
      736d0fb034b71048e0ef7789206837afa7ef76c33330117fa0be3410c149c780
        apollo-spider/dist/Apollo-Spider-v1.0.9.zip     size 21M

    bash apollo-spider/build-designer-pack.sh --check apollo-spider/dist/Apollo-Spider-v1.0.9.zip \
         --commit dd129e8
    CHECK GREEN — matches the manifest at dd129e8efa79

The brief's stop condition — *"the zip sha256 must equal O2's dry-run `736d0fb0…c780`; if it does
not, STOP"* — was **not** reached: it matched. Dave's go/no-go page was rewritten by the bake and
the review overlay re-injected (`_make_review.py`).

### The frozen ledger (`c0538c1`) — and FINDING 1

    python3 knowledge/_release/_gate_frozen_release.py --seed
      designer-skills-v1   version v1          6 file(s)  b83d048483b7
      designer-skills-v2   version v2        849 file(s)  e1d8019b97cc
      apollo-spider        version v1.0.9      9 file(s)  babd4fe1b727

**FINDING 1 — `--seed` hashes the tree at HEAD, so seeding before the release commit records the
PRIOR digest and the prior file count, silently.** Run at this seat immediately after `--release`
(the R3 sequence read from a distance), it printed `apollo-spider v1.0.9 **8** file(s)
**c115142abcda**` — v1.0.8's digest, unchanged, while a ninth zip sat untracked on disk. Nothing
errored; the row simply said the surface had not moved when it had. Re-run after `b94adff` it
reads **9 file(s) `babd4fe1b727`**. ⚠ **R3's #260 order is right and this is not a defect in it —
R3 committed `49bc5ef` first and seeded after.** What is missing is that the ordering constraint
is nowhere written down: the seed's own printed warning says *"if a frozen surface MOVED, bump
that row's version in this same commit"* and says nothing about **when** to run it. A seed run one
step early is indistinguishable, in its own output, from a surface that genuinely did not move —
[[roll-pointer-is-not-an-absence]] in the release machinery.

### The nine release gates, post-bake — 9/9 GREEN

| # | gate | rc | line |
|---|---|---|---|
| 1 | `_release/_gate_frozen_release.py` | 0 | `PASS — 3 arm(s) asked, no frozen surface moved.` |
| 2 | `_release/_gate_frozen_release.py --selftest` | 0 | `selftest: 14 bites, 0 fail(s)` |
| 3 | `_release/_gate_release_audit.py --check` | 0 | `PASS — byte-identical to a fresh generation at dd129e8efa79 (1698 files, 0265deb8da0b6a04)` |
| 4 | `_release/_gate_release_audit.py --selftest` | 0 | `selftest: 10 bites, 0 fail(s)` |
| 5 | `_release/_gate_release_audit.py --pack` | 0 | `PASS — v1.0.9 matches the manifest at dd129e8efa79` (v1.0.6/7/8 `SKIPPED — FROZEN HISTORY`) |
| 6 | `_release/_gate_ci_template.py --check` | 0 | `PASS — the template parses, ships what it calls, and hides nothing.` |
| 7 | `_release/_gate_ci_template.py --selftest` | 0 | `selftest: 10 bites, 0 fail(s)` |
| 8 | `build-designer-pack.sh --selftest` | 0 | `selftest: 221 bites, 0 fail(s)` |
| 9 | `apollo-spider/cold-start/gen_projections.py --check` | 0 | `OK — 3 projection(s) and 3 PLACED host file(s) in sync` |

⚠ Gate 8's **no-ratification refusal arm now reads `SKIPPED — the manifest is already
ratified`** — unproven in this pass **by construction**, not by omission: lanes O and O2 drove it
red before the key existed. Gate 8's bite count is **221**, not R3's 216 — five bites were added
between #260 and #262 (lane M1's `differential_arm` receipts, `#261`).

**FINDING 2 — the brief's gate-9 path is stale in the record.** `notes/_subreports/2026-09-08-260-R3-release.md`
names `cold-start/gen_projections.py --check`; the file lives at
**`apollo-spider/cold-start/gen_projections.py`**. Reported, not repaired — R3's report is dated
history (`s192-D1`) and is not re-edited.

### Declared skips, unchanged from lanes R / O / O2

- `knowledge/_validate_screen.py` — NOT RUN at this seat.
- `knowledge/_tests/test_gates.py` — SKIPPED: copytrees ≈5 GB, ENOSPC in this sandbox.
- The `--full-stage` shape was used, as at #260 and #262-O2. Still the optional flag that decides
  the ship set; **now recorded by lane M1's probe artefact**, so the shape is no longer silent.

### FINDING 3 — the clean-tree loop did NOT bite this time

`#260`-R3's ruling-shaped block records that `_git_commit.sh` appends to
`notes/_REHEARSAL-LOG.jsonl` **after** staging, so the sanctioned commit path can never leave the
clean tree `--release` requires. **Lane M2 fixed it at `425318f` (#261) and the fix held here:**
plain `git -c user.name=… commit` per this brief, and `require_clean` passed on the first attempt.
That carry was already STRUCK at the #261 wrap with its receipt; this is the first release to run
over the repaired path, which is the proof the strike was claiming.

---

## Part 2 — the capture ritual

Steps 1 · 1b · 2 · 2c · 2d · 2e · 2f · 2g · 3 · 4 · 4b · 4c · 5 · 5b, in order, per
`knowledge/_RUNBOOK-capture-ritual.md`.

### FINDING 4 — CLAUDE.md / AGENTS.md in `s262-D4`'s `governs`, and why they were LEFT

`s262-D4`'s `governs` names `CLAUDE.md` and `AGENTS.md` alongside the opener's real sources. Both
are **GENERATED from `apollo-spider/cold-start/DESIGN-CONTRACT.md`** by
`gen_projections.py`, and both are **correctly silent** about the salutation opener — the
projector places what the contract declares, and the contract does not declare the menu.

⛔ **NOT TRIMMED, and the reason is the ledger's own rule, not a judgment about the entry.**
`knowledge/_rulings.json` is append-only through `_inscribe_ruling.py`, whose contract is a
reconstruction proof that *every other byte is identical*; the runbook's step 4 permits **adding**
a decision node and **cross-linking**, never editing a ratified one, and `s183-D1` is explicit
that ratified text is amended **by ADDITION**. Editing a `governs` list after inscription would
be a silent rewrite of a ruling in Dave's name. ⇒ **the note is recorded here and on the banner,
and the entry stands.** It is harmless: an over-wide `governs` names two files that a reader will
find silent, which is a false lead, not a false claim.

## RULING-SHAPED QUESTIONS

1. ⬛ **Nothing tests that the pack HOLDS a goal across a session.** `s262-D5` models option 3 on
   Claude Code's `/goal`: the goal is stated once and **held for the whole session** as the thing
   every step is checked against. Every gate in the release line parses **text** — the menu's
   wording, the projection's placement, the manifest's file list. **Holding a goal is a
   BEHAVIOUR**, and it is the sixth venue of [[no-gate-parses-the-artefact]]: the ruling can be
   satisfied in the file and violated in every session that reads it, and nothing would say so.
   **Ruling-shaped: is a behaviour test owed here, or is `/goal` accepted as unenforceable
   guidance?** (Raised by lane O2 as UNPROVEN; carried here as ruling-shaped because the release
   shipped on it.)
2. ⬛ **The sidebar `chart` line glyph is HAND-BAKED, not the library's.** Found while reading the
   nav family for the banner: `Sidebar-nav`'s chart line icon is drawn inline rather than pulled
   from the icon library, and **its filled twin is `insight-active`** — a different name, a
   different family. `s262-D3` now rules that the current nav item carries the `-active` glyph, so
   a hand-baked line glyph whose active partner is named for another concept is a trap the next
   nav lane will step into. **Ruling-shaped: promote the pair into the library under one name, or
   declare the sidebar's glyphs local by design.** Reported, not repaired — it is component work,
   not wrap work.

## UNPROVEN from this seat

- That a cold designer can unzip v1.0.9 and drive it end to end. `--check` proves the zip against
  the manifest; the 44 other gates were not driven from **inside** the unzipped pack.
- That the amended salutation menu behaves as `s262-D5` describes. **No live assistant was driven
  through it** — O2 declared this and it is unchanged: the wording is proved, the behaviour is not.
- `_validate_fit_physics.py`'s measurement checks under a real browser — no chromium binary at
  this seat.
