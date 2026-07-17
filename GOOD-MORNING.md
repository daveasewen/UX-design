# Good morning, Dave ☕

*Briefing — written end of 2026-07-17, session **"Type tokens — promote to canon + retrofit."** Read this → `_LIVE-STATE.md` (top LIVE "TYPE-TOKEN SYSTEM = PROMOTED" entry) → `knowledge/_proforma/_TYPE-DECISIONS.md` (every ruling + WHY) → then carry on.*

## The session in one line
Promoted the Apollo SDS type system to canon and drove the whole 4px-grid programme to completion: parked the HSBC-general incumbent as a sibling, ran the retrofit (230 snaps), drafted the vertical-stack rule, **retired the legacy arrow asset**, and **expanded the DEF-005 grid gate to enforce the whole library** — all build-green.

## What landed (all this session)
- **Type promoted to canon** — reconciled primitives → `tokens/typography.json`, composites → `tokens/typography-composites.json`, `knowledge/canon/type.css` settled.
- **HSBC-general parked as siblings** — `tokens/_typography-hsbc-general.json` + `_spacing-hsbc-general.json` (incumbent, still live for HSBC-general; underscore-prefixed → out of Apollo gen + blast-radius). Apollo = the proposed HSBC standard, governed by modes. Ruling: "preserve old as legacy."
- **Retrofit done** — 230 off-grid snaps (preserve-density ties, hairlines exempt) across canon.css + 38 snippets + 9 tranches; spacing `padding/responsive` micro-scale snapped. Review sheet: `reviews/GRID-RETROFIT-2026-07-17.html`.
- **Vertical-stack rule drafted** — the Component slot already contains the descender, so stacking is pure 4px rhythm (no new tokens/gate). In `_TYPE-DECISIONS.md`.
- **Arrow asset retired** — `padding/arrow` + `icon/arrow/font-N` were unused legacy fixed-px chevron; live components use an em-scaled, flex-centred chevron. Parked + 3 metas rebound. Zero visual change.
- **DEF-005 expanded** — grid gate rewritten block-aware + HTML-safe, exempts hairline(1/3px)/negative/square; now gates **50 files** (type.css + canon.css + snippets + tranches), all pass.

## On your desk
- **Commit 1 of 2 already pushed by you** — `4a7a103 feat(type,grid): promote Apollo SDS type to canon + 4px-grid retrofit`.
- **Commit 2 is ready to run** (arrow retirement + gate expansion + this handoff refresh) — paste-ready message is in the last chat message; **commit via GitHub Desktop** (Desktop was the source of the lock contention — keep it closed while any terminal commit runs). New file: `tokens/_icon-scale-hsbc-general.json`.
- **Webfont licence** — external dependency, **not Dave's to action** (owned elsewhere): the product needs the create.hsbc webfont licence renewed; the Latin desktop OTF/TTF we hold are internal-only, so renders fall back until it's sorted. Logged as a standing blocker on the *product* path, not a task.

## Queue next (numbered, actionable)
1. **Tranche 8** — BottomTabBar · InPageNav · FooterNav · RelatedLinks · Stepper (the other proforma fork; atomise per the ATOMISE ruling).
2. **Wire the em-chevron guidance** into the component-composite usage docs (the canon arrow pattern is now the em/flex chevron; make it discoverable so nobody re-adds fixed-px arrows).
3. **Review-overlay upgrades** — image paste + audio dictation + export-as-bundle (it's a product feature now).
4. **DataViz** — still 🟡 PARKED; needs your in-browser pass + Layer-2 controls.
5. Optional: extend DEF-005's square-exemption into a shared helper if other gates need "intrinsic size ≠ layout" logic.

> Opener: **"Title this chat: Tranche 8 — proforma nav-tail."** Then GOOD-MORNING → `_LIVE-STATE.md` → `_TYPE-DECISIONS.md`.
