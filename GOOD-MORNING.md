# Good morning, Dave ☕

## The session in one line
Promoted **Cards**, **List-items**, and **Status-indicator** to gated canon; locked the **hub-and-spoke code-binding model**; and settled the **passive-atom rubric question** — leaving three components at a clean 9/9 and the atom-reuse web visibly tightening.

## The headline shifts
1. **Code↔design naming is solved: hub-and-spoke (LOCKED 2026-06-22).** Figma node ID = the only identity; names are per-namespace — figma `name` / `$displayName`+`$aliases` (ours) / per-library `codeBindings` spokes. Never guess or normalise a code name; populate spokes from Code Connect. `codeBindings` is now a first-class field in `meta.schema.json`; procedure in `_RUNBOOK-onboard-code-library.md` (registered in README); saved to memory.
2. **List-items transaction row → 9.0/9.** Reuses four canon primitives — **Avatar**, **Tags**, the **Loading-indicator** spinner (mirrored, not hard-coded), and the **Status-indicator** RAG tint chip. Now carries the **full RAG** status set (Pending/Declined/Approved), container-query reflow (1.4.10), roving Arrow/Home/End nav, native `:disabled`. Logged a **systemic `$darkFinding`**: `text/secondary` on the dark hover surface = 3.34:1 (<4.5), token-level, affects every row.
3. **Status-indicator → 9.0/9.** Passive RAG atom, three forms (inline dot+label, square tint chip, live `aria-live`). Its tint chip **IS** the List-items status detail — cross-referenced both ways. Findings logged: amber dot 1.69:1 standalone (use the chip; label carries meaning, 1.4.1) and **`rag/neutral-tint` missing** from the store.
4. **Rubric decision A (passive-atom AT).** A component meta can set `"interactive": false`; the scorer then credits AT via `role`/`aria-live`/`aria-label` instead of a keyboard handler it shouldn't have — but a passive component exposing *nothing* still scores 0, so the bar stays real. Lifted Status-indicator 8.5→9, Badge 6→7, Divider 5→6, Loading-indicator 5.5→6.

## State
- **Board:** 3 at 9/9 (**Tabs, List-items, Status-indicator**); average 6.3/9.
- **Build green** — `cd knowledge && python3 _build_all.py` (snippet 32/32, schema 32/32, integrity 0 errors). **Working tree clean** — everything above is committed (last commit: List-items full RAG).
- **Parked:** Figma dark-mode port (task #19); `rag/neutral-tint` token gap; the dark hover/secondary-text `$darkFinding`.

## First task next session — Table (★, 6.5/9), but decide one thing first
The canonical Table (`table.meta.json`) is a **static semantic data table** — props are `headerType`/`orientation`/`cellAlign`; **no sort, no selection**. Its accessibility is `scope`/`caption`/reflow (1.3.1, 1.4.10), **not** `role`/`aria`/keyboard. So the rubric's AT signal doesn't fit it — **same shape as the passive-atom question we just solved.**

**Decide:** is Table `interactive:false`-like (credit semantic-table AT: caption + `scope` + a focusable scroll `region`), or does it earn AT the interactive way (sortable `<th>` buttons + `aria-sort` + keyboard)? Pick before building.

Its three gaps to 9/9: **states** (0.5), **AT** (0), **responsive** (0 — `overflow-x:auto` isn't counted; needs a real `@media`/container reflow). `table/*` tokens are already clean.

## The thing to hold
You kept the work **honest** twice: Status-indicator went 8.5→9 by *fixing the rubric*, not faking a `keydown`; and findings got *flagged* (amber dot, neutral-tint, dark hover) rather than absorbed. That discipline — verification as enforcement — is the project working. Table will tempt you to bolt on sort just to chase 9/9; let the component's real nature decide instead.

Have a good one. 💧
