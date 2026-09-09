# `#262`-`O2` — Dave's amendment to options 2 and 3 (s262-D5), and v1.0.9 re-cut again

session: `#262` · 2026-09-09 · sub index: `O2` · provenance: 262 · 2026-09-09 · status: observed
lane: amend the opener wording lane O had just enacted, inscribe it, move the cut. **DID NOT RELEASE.**

## VERDICT
Option 2 now reads **"they type or paste it"** — his order. Option 3 is now modelled on Claude
Code's **`/goal`**: the goal is stated once and **held for the whole session** as the thing every
step is checked against, the shape is proposed and confirmed **before building anything**, and
progress is reported **against the goal, not against a task list**. Inscribed as `s262-D5`.
v1.0.9 re-cut at **`dd129e8`** — 1698 files, manifest sha256 `bc10de6fdc7fa8ce`, zip twice-baked
to `736d0fb034b71048e0ef7789206837afa7ef76c33330117fa0be3410c149c780`, `--check` GREEN.
**Still PROPOSED**: no `--release`, no `RATIFY_IDS` row.
COUNTS: findings 1 · ruling-shaped 0 · declared skips 1

## Step 1 — the wording (`1518ed6`)
`cold-start/COPILOT-BOOT.md` is the one source, so only the option list moved. Option 3 grew from
two lines to five, but stays inside the pack's voice and the "one line each, then wait" fence is
untouched — the extra sentences tell the assistant how to *hold* the goal, not what to say aloud.

**FINDING 1 — `FIRST-SESSION.md` Step 5 needed no edit.** It already read "type or paste a brief,
or just describe the goal" — lane O had written it in his order by luck rather than by ruling.
Checked, not assumed; left alone rather than churned. The two `copilot-instructions.md` moved via
`python3 cold-start/gen_projections.py`, never by hand.

Gates: `gen_projections --check` **OK** (3 projections + 3 PLACED hosts) · `verify_placement.py`
**3/3 PLACED**.

## Step 2 — `s262-D5` (`dd129e8`)
A **new entry**, not an edit to `s262-D4` — that is the whole point of the amendment shape. Through
`_inscribe_ruling.py`: textual span 1416 bytes at offset 635643, rulings 421 → 422, reconstruction
proof PASSED, every other byte identical. `says` carries both of his sentences verbatim.
`governs` names the source, the projector and the two projections — the path, not just the files.

## Step 3 — the re-cut (`daf1358`)
`b0d81e8`'s cut never shipped either, so moving it a second time is still clean.

    git archive dd129e8 | tar -x -C /var/tmp/full9p
    --probe    --commit dd129e8 --full-stage /var/tmp/full9p   41 / 4 / 9 — lane O's shape exactly
    --manifest --commit dd129e8 --full-stage /var/tmp/full9p
        commit dd129e8efa79  files 1698  bytes 45867344  sha256 bc10de6fdc7fa8ce
        differential arm: ARMED — REPO-BOUND verdicts are MEASURED
    build-designer-pack.sh --dry-run --commit dd129e8 → /var/tmp/p1  736d0fb0…9780 · → p2 same
    cmp p1 p2 → rc 0 BYTE-IDENTICAL
    --check /var/tmp/p1/Apollo-Spider-v1.0.9.zip --commit dd129e8 → CHECK GREEN
The pack-docs gate ran ADVISORY inside the bake: 220 findings, rc 0, all pre-existing runbook path
names. The go/no-go page was rewritten by the dry run and the review overlay re-injected.

## Commits · what stays for Dave · unproven
`1518ed6` the wording · `dd129e8` the ruling · `daf1358` the cut. NOT PUSHED (s133-D2).
> **"Ratify v1.0.9."** — now against `dd129e8`. Expect `736d0fb0…9780`.
UNPROVEN: the nine release gates were not re-run in full (lane R's table stands; declared skip);
no live assistant was driven through the amended menu, and nothing yet tests that a pack actually
*holds* the goal across a session — that is a behaviour, and no gate parses it.
