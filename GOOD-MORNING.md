# Good morning, Dave ☕

*Briefing — written end of 2026-07-17, session **"Type-token system — build from Figma."** Read this → `_LIVE-STATE.md` (LIVE "TYPE-TOKEN SYSTEM" entry) → `knowledge/_proforma/_TYPE-DECISIONS.md` (every ruling + WHY) → then carry on. Dense on purpose.*

## The session in one line
Took the Figma type file and built a **type-token system**: reconciled + 4px-normalised **primitives**, two composite sets **Editorial** (full line-height) + **Component** (cap-trim → 4px grid-slot), a working **`type.css`**, and a **grid gate** — all decisions captured in `_TYPE-DECISIONS.md`. Proposals are built and **awaiting your promotion to canon**.

## ⏭ FIRST TASK — carry on in the agreed order (promotion first)
We agreed to continue in this order; picked up where a stretched context window left off:
1. **Promote the type proposals to canon** *(your sign-off step — canon promotion = Dave only)*: move `tokens/_proposals/typography-reconciled-2026-07-17.json` + `typography-composites-2026-07-17.json` into `tokens/typography.json`, settle `knowledge/canon/type.css`, mind the blast-radius. **Task #8**: wire `_validate_grid.py` into `_build_all.py` as DEF-005.
2. **Retrofit sweep** (task #9): ~**123** off-grid values in `canon.css` + **69** across proforma tranches. Fix **source snippets + spacing tokens + regenerate** (canon.css is generated — don't hand-edit). Also investigate the **arrow-padding 5/6/7px asset** (likely an off-grid asset, not a real optical).
3. **Vertical-stack spacing rule** (task #7): trimming hands vertical rhythm to spacing tokens — draft rule in `_TYPE-DECISIONS.md` (4px gaps slot-edge to slot-edge; min gap ≥ upper block's descender depth; Editorial keeps paragraph-spacing; baseline-grid now clean).

## What landed (all built this session)
- **Primitives** — `tokens/_proposals/typography-reconciled-2026-07-17.json`. Reconciled with repo export; weights **250/300/350/400/500/700** confirmed from the Latin desktop OTF; display sizes `font-00`/`font-0` added (scale-2/3 **inferred**, flagged); 4px-normalised (only font-1/3/4 moved at scale-1).
- **Composites** — `tokens/_proposals/typography-composites-2026-07-17.json` + `knowledge/canon/type.css`. Editorial roles (display/heading/body/caption) + Component roles (label/button/input/link/figure/caption…). Component = `text-box-trim` (native) + Capsize fallback + 4px grid-slot.
- **Grid gate** — `knowledge/_validate_grid.py`. 4n + 2px half-step; font-size/letter-spacing/border/radius exempt. Passes selftest + type.css.
- **Specimens (real Univers)** — `reviews/TYPE-SPECIMEN-2026-07-17.html` (scale, weights, the measured crop→slot proof) and `reviews/TYPE-COMPOSITES-2026-07-17.html` (both sets in action, dark-mode step-up). `.REVIEW.html` twins carry your comments.
- **Rulings ledger** — `knowledge/_proforma/_TYPE-DECISIONS.md` — READ FIRST before touching type.

## On your desk
- **Promotion is yours** — I built the proposals but didn't touch canon `typography.json` (governance: promotion = Dave).
- **Commit**: hand-ready summary below — commit + push via **GitHub Desktop** (Desktop closed while any terminal commit runs). New/changed files: `_TYPE-DECISIONS.md`, `typography-reconciled/composites` proposals, `type.css`, `_validate_grid.py`, three `reviews/TYPE-*` pairs, `_LIVE-STATE.md`, this file, `knowledge/assets/fonts/_desktop/` (Latin OTF/TTF — **note licensing: desktop licence, product needs the webfont renewed on create.hsbc**).
- **Webfont licence** expired on create.hsbc — chase renewal (product needs it; desktop files are internal-only).

## Queue after type (from tasks + `_LIVE-STATE`)
- Review-overlay upgrades — **image paste + audio dictation + export-as-bundle** (task #4; it's a **product** feature now).
- DataViz still **🟡 PARKED** (needs your in-browser pass + Layer-2 controls).
- Bigger horizon captured this session (memory): **"lovable on rails"** 4-phase spine (Discover/Create/Craft/Dispatch), **chat-to-KB bot**, **KB-distillation-at-deploy**, modes = **tiered adherence** (a11y = the one non-removable floor, admin-tunable).

> Opener: **"Title this chat: Type tokens — promote to canon + retrofit."** Then GOOD-MORNING → `_LIVE-STATE.md` → `_TYPE-DECISIONS.md` → promote, then the retrofit sweep.
