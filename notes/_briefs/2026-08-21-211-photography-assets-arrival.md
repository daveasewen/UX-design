# Photography assets — arrival record (#211, 2026-08-21)

**Dave's word (#211, verbatim):** *"I've added a photography folder to the project assets so we can use them during generation if we need to. might be nice to use them in the image and carousel components. they will need to be mapped and added to the KG and we'll probably have to tag them at some point too."*

## What arrived (measured, not assumed)

- Path: `knowledge/assets/photography/` — **251 JPEGs, 2.5 GB** (`ls | wc -l`, `du -sh`, #211).
- Provenance mix by filename: `GettyImages-*` (majority), `EyeEm_*`, bare-number files — **licensed stock**; the one file probed carries EXIF `copyright=All Rights Reserved` and a usable EXIF description (*"Young woman smiling and hiding her face behind red book…"*), so **EXIF descriptions are a real seed for the tagging pass**.

## The fence (enacted #211, conductor)

The folder arrived **untracked and un-ignored** — one `--all-dirty` commit away from pushing 2.5 GB of licensed stock into git history. `.gitignore` now carries `knowledge/assets/photography/`. **Originals are NON-REPO by this fence**; this file is the in-repo home. Un-ignoring is a pipeline ruling, Dave's (see below).

## Owed (store row `W-93` carries the close condition)

1. **Manifest** (committed): filename · dimensions · EXIF description · licence source per image — the committed surface the KG can point at.
2. **KG mapping**: photo nodes + edges to consumers — Dave named **Image-block** and **Carousel** as the natural first consumers.
3. **Tagging pass** — approach unruled; EXIF descriptions are the free head start.
4. **Pipeline ruling (Dave's):** originals NON-REPO as fenced now · git-LFS · committed web-sized derivatives. Until ruled, real photos are reachable only by path from a working tree that has them — any brief using them must declare that.
