# Cold-run brief — CANDIDATE, Spider v1.0.14 candidate (4a's pack)

You are ONE cold run in a series (#304, Run 4, lane 4f). You are a fresh agent. You have ONLY two
things: the Apollo pack named below, and the prompt below. Nothing else is yours to read.
Model: Opus 5.5. One run per agent; you know nothing about the other runs and must not look for them.

## Your run id

The conductor gives it in the dispatch line: one of `cand2-r1`, `cand2-r2`, `cand2-r3`. Below, `<RUN>` means that id.

## The pack

- Pack zip: `notes/_lanes/304/R4a/cand/Apollo-Spider-v1.0.14-candidate-2.zip`
  (sha256 `8a75ce321a0a481553d5dfbd7fc3a10b833df018624cecbe4d90bbee7aff47e3`; the conductor fills this in if it reads PENDING).
- Unzip it at the seat into your own workspace, and work only there:

```
REPO="$HOME/mnt/Projects--UX-design"
W="$HOME/cold/<RUN>"; mkdir -p "$W/out"
cd "$W" && unzip -q -o "$REPO/notes/_lanes/304/R4a/cand/Apollo-Spider-v1.0.14-candidate-2.zip" && mv Apollo-Spider-* pack   # the pack is now $W/pack
```

- The pack is your whole design system. Read it the way a Claude Code session opened in the pack
  folder would: `pack/CLAUDE.md` (or `AGENTS.md`), `pack/FIRST-SESSION.md`, `pack/README.md`, then the
  skills under `pack/skills/*/SKILL.md` ("Use the Apollo skills" in the prompt means these), then
  whatever they send you to inside `pack/`.

## The prompt — verbatim, do not edit it

```
Build an interactive international-banking prototype for the CEOs of HSBC corporate and institutional clients, with linked sub-pages and working simulated workflows. Use the Apollo skills and stay on-canon.

This is a new project, related to the existing group-treasurer dashboard but separate from it. Create new CEO screen files; do not overwrite the treasurer screen, canon, tokens or validators.

SETTINGS — already decided, do not ask
- Theme: Common. Light and dark, with a theme switch.
- Layout: bento, comfortable density, wide desktop. The section the bento sits in takes the lightest grey, so the white tiles have definition against it; the rest of the page and the title area stay as they are.
- Brand: the supplied HSBC masterbrand and Apollo tokens. No other assets.
- Data: realistic placeholder entities and currencies, GBP reporting with explicit illustrative FX rates, 30-day time series, and enough rows to sort, filter and page.
- Off-limits: Apollo accessibility defaults and existing patterns only. Invent no components, variants, colours or icons, and use each component as the pack gives it, at its own size. No live banking connections or real credentials.

DATA VISUALISATION
Be liberal with data visualisation. Wherever a figure moves over time, compares across entities, regions, currencies or products, or is a share of a whole, show it as an Apollo chart rather than a bare number or table, on the overview and on every sub-page. Use the full range of chart types the pack provides, each with its legend, tooltips and behaviour working.

THE OVERVIEW ANSWERS THREE QUESTIONS
1. Financial resilience — can we fund our plans? KPI tiles for cash, available liquidity and funding headroom.
2. Risk outlook — where are we exposed? A regional and currency exposure chart that drills through to the underlying positions and limits.
3. Decisions — what needs my attention? Summary cards for pending approvals and material risk exceptions, each linking to a record you can act on.

LINKED VIEWS
Overview · accounts and transactions · liquidity and funding · payments and approvals · FX and markets · risk and limits · trade finance · reports · HSBC messages and service requests · settings.

WORKING BEHAVIOUR
Make it fully interactive and as complete as possible across every sub-page: shared entity, region and date filters; searchable, sortable, paged records with detail views; validated simulated approvals and service requests; risk acknowledgements with audit notes; exports; messages; theme switching; navigation, filter and workflow state that persists. For each interaction, pick the lightest pattern that does the job.

PROOF
- Run and keep the pack baseline before building the UI, and tell inherited failures apart from new ones.
- Mint provenance, run the screen checks and the pack runner, then drive real browser interactions and check DOM geometry, computed spacing and console errors.
- Vision is disabled and there is no work-around; the usual errors are spacing, so double-check spacing. Report visual review as unavailable. A screenshot is not visual-validation evidence.
- Name anything unsupported or untested as a gap. Do not claim production banking capability or browser checks that were not run.
```

The SETTINGS block already answers the design questions. If a pack skill tells you to ask something,
record the question and the default you took in your run report and carry on; nobody will answer.

## Where your output goes

- Build in `$W/out/`. The overview is `$W/out/index.html`; linked sub-pages are further `.html`
  files in `$W/out/` (or views inside one page — your choice; say which).
- Reference the pack IN PLACE by relative path from `out/`, e.g. `../pack/knowledge/canon/canon.css`,
  or copy what you need into `out/`. Nothing outside `$W/out/` and `$W/pack/` may be referenced.
- When the build is done and your proof has run, FREEZE it: copy the folder into the repo, once:
  `mkdir -p "$REPO/notes/_lanes/304/R4c/cold/<RUN>" && cp -r "$W/out" "$REPO/notes/_lanes/304/R4c/cold/<RUN>/out"`
  (never copy `pack/`). Do not edit the frozen copy afterwards.
- Beside it write `$REPO/notes/_lanes/304/R4c/cold/<RUN>/RUN-REPORT.md` (≤ 900 words): which pack
  files you read (in order), what you built (pages, components, charts), every question you would have
  asked and the default you took, the proof the prompt asks for (baseline, provenance, screen checks,
  pack runner, driven browser checks — each with its command and result), and the Gaps list. Say
  plainly what you did not run.

## Tools and limits

- Work with `mcp__remote-devices__device_bash` at Dave's seat. Each call is capped at 180 s and runs
  in the foreground; nothing survives a call boundary except files. Long steps: split them.
- A browser, for the prompt's PROOF: the ONE thing you may take from outside the pack is the seat's
  render environment. In the SAME bash call as the browser work:
  `export TMPDIR=/dev/shm; bash "$REPO/knowledge/_render/ensure_env.sh"; source "$REPO/knowledge/_render/seat_env.sh"`
  then Python Playwright with `executable_path=os.environ["RENDER_SHELL"]`. Use it as a tool; do not
  read those scripts or anything near them for design guidance.
- Vision is disabled for this run (the prompt says so): never open an image (no Read of a PNG/JPG).
  Screenshots may be written for the record; they are not evidence.

## Forbidden

- Reading anything in the repo (`$REPO`) except the pack zip and writing your own output folder:
  no `notes/`, `knowledge/`, `showroom/`, `_CHAIN.md`, handoffs, other runs, rulings, the graph.
- Web search or fetch; Project memory; git of any kind; `_build_all.py`.
- Editing anything inside `pack/` except what the pack's own tools write when you run them.
- Looking for, reading or scoring with the eval harness (`notes/_lanes/304/R4c/harness/`). Scoring is
  done afterwards by another seat.

## Return to the conductor (≤ 200 words)

The run id, the frozen folder path, the entry page, the number of pages, the pack skills you followed,
the proof you ran with its results, the top three gaps, and your context use at the build→proof seam.
