# `_retired/` — deliberately kept, not rubbish

**STANDING:** work that was reverted, superseded or parked but is **worth returning to**. Tracked in git,
unlike `_to_delete/`.

## Why this exists (Dave, 2026-07-18)

> *"I might keep that as an archive… maybe it's not an archive, maybe it's 'retired' and we keep the
> `_to_delete` for other things."*

He was right, and the check proved it. `_to_delete/` held **29.7 MB of genuine rubbish** (duplicate
tarballs, snapshots, `.stale` temp files, git locks) **and 0.14 MB that was not rubbish at all** —
including two complete, documented gates. `_to_delete/` is **gitignored**, so those were not in git, not
pushed, and one `rm -rf` from gone. I had recommended deleting the directory without looking inside it.

**The naming was the defect.** A bin labelled *delete me* that holds things you want back is how you lose
them — the same failure as the `#1A1A1A` value without its reason, and §A's instruction reduced to a
label. The label has to carry the meaning.

## The split

| | `_retired/` | `_to_delete/` |
|---|---|---|
| **contains** | reverted/superseded work with residual value | duplicates, snapshots, `.stale` files, git locks |
| **git** | **tracked** | gitignored |
| **safe to empty?** | **no — deliberate keeps** | yes, any time |

## Plain English — what the junk in `_to_delete/` actually is

*Dave, 2026-07-18: "you'll have to explain like I'm 5 what you mean by tarballs, snapshots…" Fair — and it
matters, because you cannot check a claim that something is rubbish if you cannot read the list. Written
here so the next person (or the next cold session) can sort the bin without a developer.*

| You'll see | It means |
|---|---|
| `.tar.gz` · `.tgz` — a **tarball** | **A zip file.** `tar` squashes a folder into one file, `gz` compresses it. Mac would just say "archive". |
| `..._snapshot...` | **A copy taken before doing something risky** — Save As before a big edit. A safety net that was never needed. |
| `.stale` | **The old version, superseded.** A label meaning "replaced, don't use." Usually with the date it was retired. |
| `DUP` | **Duplicate.** A second copy of something that already exists properly elsewhere. The long number is a timestamp. |
| `*.lock` — **git locks** | Git drops a tiny "I'm busy, don't touch" note while it works, and tidies it up after. The sandbox **can't delete files**, so they pile up. They are **0 bytes** — literally empty. |

**The rule of thumb for sorting the bin:** genuine rubbish is always *a zip file*, *a dated copy of
something that still exists*, or *an empty file*. Anything that is none of those three — actual working
files with real content, like the Tranche 6 folder below — **stop and look before deleting.**

## What's in here

### `tranche6-reverted-20260715/`
The reverted Tranche 6 (see the T6-revert lesson: proposed work replaced reviewed work without asking —
the origin of the *ask-what-Dave-valued-before-mine-vs-fresh* rule). **The revert was about process, not
about these artefacts**, so two gates went out with it and may be independently salvageable:

- `_validate_state_cluster.py` + `_STATE-CLUSTER-GATE.md`
- `_validate_glyph_presence.py` + `_GLYPH-PRESENCE-GATE.md`

Neither is wired into `_build_all.py`. **Open question for Dave: are these worth reviving on their own
merits?** Given the session that found them was about gates being the only thing that makes a rule
survive, they deserve a look rather than a bin. `apollo-tranche6-apply.tgz` is the matching apply bundle.
