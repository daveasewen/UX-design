# Sub brief — photography manifest + derivatives + library consumers (#217, Opus build sub)

**Ruling in force: `s217-D1`** (read it from `knowledge/_rulings.json`, not from this brief): originals NON-REPO (the `.gitignore` fence at `knowledge/assets/photography/` stands), committed manifest + web-sized derivatives of USED photos only, each derivative carrying a manifest row. Hosted cloud store is NOTED-FUTURE, not ruled — do not design for it.

## Context (verified this session, not assumed)
- `knowledge/assets/photography/` — 251 JPEGs, 2.5 GB, licensed stock (GettyImages-*, EyeEm_*, bare-number). At least one file carries a usable EXIF description; treat EXIF as the tagging seed.
- Arrival record: `notes/_briefs/2026-08-21-211-photography-assets-arrival.md` — read it first.
- Dave named **Image-block** and **Carousel** as the first consumers (#211, verbatim in the arrival record).

## Scope (your generator owns these REGIONS and nothing outside them)
1. **Manifest generator** (new script, home it per repo convention beside its peers — survey `knowledge/` for how sibling generators are homed before picking): reads the photography folder, emits a **committed** manifest — filename · pixel dimensions · EXIF description · licence source (derive from filename provenance + EXIF copyright). 251 rows. The manifest file must live OUTSIDE the ignored folder or it will be silently ignored — verify with `git check-ignore` before homing it.
2. **Derivative minting** (same script or sibling): web-sized sRGB JPEG, max edge ~1600px, target ≤300 KB, deterministic naming, output dir committed. Mint ONLY for photos you actually wire into consumers below — pick 8–12 photos yourself as specimens (picking specimens is not ruling; Dave swaps later by eye).
3. **Wire real photos into the Image-block and Carousel library specimens** — SURVEY FIRST: find the current canonical specimen pages (`s215-D5`: library v2 replaced `showroom/index.html`; grep before building). Copy the approved artefact as your starting point, never re-draw [[specimen-starts-from-reference]].
4. **Render-proof**: read `knowledge/_RUNBOOK-render-verify.md` BEFORE any render attempt — chromium libs from #213 may be absent in this fresh sandbox; the re-extract recipe is the runbook's fourth stratum. `set_content()` is BANNED; use `goto("file://…")`. Builds >45s wall die at the call boundary — chunk.
5. **Rows**: sign-off row(s) in `knowledge/_REVIEW-SIGNOFF.md` (AWAITING), a store row for each new document at creation (forgotten-document class), DS defects you find go to `knowledge/_DS-IMPROVEMENTS.md` by addition.

## DO-NOT-RULE (hard fence)
- `knowledge/_rulings.json` is READ-ONLY to you.
- No tagging taxonomy — the approach is UNRULED; EXIF text goes into the manifest verbatim, nothing more.
- No KG schema decisions — record what a KG mapping WOULD need as a priced note, do not build it.
- No judgment on which photos Dave should prefer, no green-band photo calls.
- No token, theme, gauge, threshold, lane, or worklist edits.
- Do NOT commit or push — the conductor reconciles the working tree path by path.
- Do NOT git-checkout/reset anything.

## Pitfalls to carry (mandatory replay, Dave #165)
- (a) An EXIF field that is absent is **UNKNOWN, never defaulted** — the manifest row says so explicitly; the script fails LOUD and NAMED on unreadable files and declares the residual count.
- (b) The one probed file is not the population — measure EXIF coverage across all 251 and report the real number.
- (c) Verify at the end that `git status` shows NO original JPEG staged-able — the fence holding is a checked claim, not an assumption.
- (d) A count is not a measurement — report derivative sizes in KB measured, not intended.
- (e) Version, don't overwrite: `-vN` filenames for specimen pages; sandbox cannot rm (use mv).

## Report back (replayed in-window by the conductor)
What you built with paths · EXIF coverage measured · derivative count + sizes · every refusal/residual declared · rows added · what a probe would INVALIDATE if it failed · your token spend.
