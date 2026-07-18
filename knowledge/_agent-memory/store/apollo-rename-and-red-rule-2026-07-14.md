# Housekeeping — Apollo rename + red-rule fix (2026-07-14, Dave)

Two rulings, both committed to the live repo (local commits, Dave pushes via Desktop).

## 1. Project renamed: Promenaut → Apollo  (commit be3c364)
- "Promenaut" → "Apollo" everywhere; "Smart Design System" descriptor DROPPED → just
  "Apollo" (Dave: singular preferred over "Apollo SDS"). 51 files + 3 pipeline-spec files renamed.
- Scope: archive/ INCLUDED (Dave wants it kept as part of the one project — "may be resuscitated,
  two hypotheses"). Transformation workstream touched only where it named Promenaut/SDS.
- Generated `designer-skills-v1/knowledge/` rebuilds from source (gitignored). NB: on THIS
  bridge mount `rm -rf` can't purge, so a rebuild there can leave stale copies — fixed the 3 by
  hand; on a normal filesystem the rebuild is clean.

## 2. Red rule corrected: red = the PRIMARY-action accent, once per screen  (commit f8e05e5)
- OLD (wrong): "red = destructive only." NEW (Dave): **red is the primary-action accent, used
  ONCE per screen on the single primary action; destructive/error takes a distinct, non-red
  treatment.** Universal across registers (Dave chose this over the charter's register-tied version).
- Changed: charter `_FIXED-FLEX-CHARTER §4` red-forward ceiling (superseded inline, dated);
  gate `BRAND-1` in `runs/proof-001-payments-dashboard/gate2_assembly.py` (now blocks red on any
  non-primary action AND red used >once; passes when red is on the one primary action or absent);
  proof-001/002 specs, figma-make-prompt, contract-001 redForward, northstar vision.
- The guidelines were ALREADY correct (red = strategic primary-CTA accent, "tactically red").

### Propagation gap (OPEN — supersession discipline)
Left as historical run OUTPUTS, NOT rewritten (they'd misdescribe what they rendered):
- `knowledge/_fitness-test/sme-payments.html`, `sme-payments.canon.html`, `sme-payments-desktop.canon.html`
- `runs/proof-001-payments-dashboard/_GATE2-REPORT.md`
→ If those builds are revived, regenerate under the new rule. `_LIVE-STATE.md` should carry this at
  next end-of-session refresh.

## 3. designer-skills-v1 rebuild (2026-07-14, same day — the "designer live-fire" pack)

`designer-skills-v1/` is the Copilot skill pack + curated `knowledge/` cut for a real designer to
try Apollo hands-on ("designer live-fire"). `designer-skills-v1/knowledge/` and the distributable
`Apollo-designer-skills.zip` at repo root are BOTH gitignored generated artifacts — not tracked in
git, rebuilt from the live `knowledge/` source via `designer-skills-v1/build-designer-kb.sh`.

Rebuilt both today after the 1.4.11 border-token fixes (commit `547e7cc`) so the pack a designer
would receive reflects current values, not the stale 09:40 snapshot from before the fix. Confirmed
the rebuild actually picked up the new values (`divider/border/subsection` dark → `#696969`) before
re-zipping.

**Two sandbox gotchas hit and worked around, worth knowing for next time:**
- `build-designer-kb.sh` opens with `rm -rf "$DST"` — fails under `set -e` on this bridge mount
  (delete-guard blocks `rm` on existing files, same as the recurring git-lock issue). Workaround:
  `mv` the existing `designer-skills-v1/knowledge` out of the way to `_to_delete/` FIRST, then run
  the script unmodified — `rm -rf` on a now-nonexistent path is a no-op, `mkdir -p` recreates clean.
- `zip -r` cannot write directly to a file living on this bridge-mounted device folder AT ALL —
  even to a brand-new filename that never existed. `zip` internally writes to a temp file
  (`ziXXXXXX`) then does a final rename-to-target to finalize the central directory, and that
  rename is blocked here regardless of whether the target pre-existed (`zip I/O error: Operation
  not permitted` / `Could not create output file`). `tar czf` does NOT hit this (single direct
  write, no temp+rename) — so the working pattern is: `tar czf` the folder on-device → stage the
  tarball into the cloud sandbox via `device_stage_files` → `tar xzf` + `zip -r` in the (unrestricted)
  cloud sandbox → `SendUserFile` the finished zip → `device_commit_files` it back to the device path.
  Don't waste time retrying plain `zip -r` on-device — it will keep failing the same way.

Left some zip temp-file debris (`ziw5W6eB`, `zi4q9DL6`, `zicd2uuT`) and empty 0-byte
`Apollo-designer-skills.zip`/`-NEW.zip` attempts in the repo root from the failed direct-zip
attempts — all moved to `_to_delete/` (device_bash can't `rm`), repo root is clean.

### Follow-up same day: AGENTS.md added to the pack

Dave flagged (from memory) that the pack's own `README.md` requires `AGENTS.md` "at the repo
root" as setup step 3 — but the zip didn't actually include it. Investigated before touching
anything: read `AGENTS.md` in full (root operating manual — core principles incl. retrieval-not-
recall/never invent a hex-icon-component, craft-vs-taste, gate tiers, WCAG 2.2 AA compliance bar)
and confirmed it's genuinely needed, not just nice-to-have — the pack's 4 skills (generate-from-
canon, check-against-design-system, usability-review, draft-a-new-pattern) don't restate those
governing principles themselves, they assume AGENTS.md is present per the README's own setup
instructions. Rebuilt the zip with `AGENTS.md` added at the zip root alongside `designer-skills-v1/`,
landed via the same tar-workaround, confirmed via `unzip -l`/`unzip -t` (AGENTS.md present, 6530
bytes, no archive errors). `Apollo-designer-skills.zip` is gitignored/untracked, same as before —
no git commit needed for this, just the device-bridge file landing.
