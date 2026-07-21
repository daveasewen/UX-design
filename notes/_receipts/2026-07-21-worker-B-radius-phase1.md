# RECEIPT — Worker B · Phase-1 radius migration + theme-response audit (surfaces & structure)

*2026-07-21 21:10 BST (date from `date`). Brief: `notes/_briefs/2026-07-21-phase1-worker-B-brief.md`.
Worker per `knowledge/_RUNBOOK-parallel-conductor.md` — NO git, no shared-state writes. Conductor
reconciles + commits.*

## What landed

All **10 assigned files migrated — 23/23 declarations rebound** onto role tokens (both theme blocks +
`#token-manifest` binding + `MIGRATED_SNIPPETS` ratchet, each file one change). `50%`/`999px` idioms
left literal. Notifications = **radius only**, Legacy RAG colours/`#A8000B`/driftAllow untouched.
Regenerated (`gen_snippet_tokens` → 0 values projected = hand-typed 0s matched resolved Mono;
`gen_theme_cascade` 28 overrides / 52 projections; `gen_showroom` 11 pages rewritten) → **build
42/42 green**.

**Verified flexing, not assumed:** computed-style probe of every rebound selector inside the showroom
iframes across all 4 themes — 23/23 respond: Mono / Legacy / Supercharge = 0 (square, per Dave's
Legacy-square ruling), **Console control=8px · surface=12px** (indicator→default=8). Renders (30 PNG:
10 Mono + 10 Console + 10 Legacy; Supercharge skipped — Phase-0 pixel-diff-proven ≡ Mono) backed the
probe; harness banners confirmed the cascade sees the new vars ("Apollo Console: 3 var(s) re-bound" etc.).

## Per-element role choices (all match the canon census unless flagged)

| File | Element → role |
|---|---|
| Tabs (6) | `.tab`, `.demo-controls button`, `.overflow__trigger`, `.overflow__item` → **control** · `.overflow__menu` → **surface** · `.indicator` → **indicator** ⚑ |
| Modals (4) | `.btn`, `.demo-controls button`, `.dialog .close` → **control** · `.dialog` → **surface** |
| Account-card (3) | `.account-card` → **surface** · `.tag`, `.chip` → **indicator** |
| Table (3) | `.demo-controls > button` → **control** · `table` → **surface** · `.hint kbd` → **indicator** |
| List-items (2) | `.tag`, `.status` → **indicator** |
| Action-bar (1) | `.action-bar .btn` → **control** |
| Confirmation (1) | `.confirm .btn` → **control** |
| Links (1) | `a.lnk` (focus-ring shape) → **control** |
| Notifications (1) | `.note` → **surface** (LEGACY file — radius only) |
| Video-player (1) | `.bigplay` → **control** |

⚑ **The invited refinement (dossier: "`.cn-tabs .indicator` left as control, worker may refine"):**
snippet binds the active-tab bar to **indicator** (non-interactive marker — the role's namesake);
canon.css line ~2066 still says control. Zero visual divergence in all four current themes (both roles
alias default everywhere the two differ), but latent: **propose conductor flips canon `.cn-tabs
.indicator` → `--border-radius-indicator`** so snippet+canon agree before any theme dials indicator.

**Taxonomy note for the PROVISIONAL census:** canon itself is split on the tag atom — `.cn-tags .tag`
= control (~1751) vs the *reused* tag atoms in account-card/list-items = indicator (~2817/1020). Mine
match their per-context canon, but the atom diverges across contexts. Worker A holds
`Tags.reference.html`; conductor should reconcile one ruling for the tag atom (interactive/dismissible
variant argues control; the non-interactive label chip argues indicator).

## Theme-response findings (propose only — promotion is Dave's)

1. **Mono renders RED primary CTAs in the Button MIRRORS** — Action-bar, Modals, Confirmation
   (render-confirmed on Action-bar: red "Confirm payment" both modes under Mono). Mechanism: they
   still bind **`primary/background/default`**, whose BASE value is `#DB0011`
   (semantic-colour.json ~309) — but Button.reference was rebound onto the **`button/*` ladder**
   (B-D1: Mono primary monochrome) on 07-20 and the mirrors were not. Same rot-class as the T1–T9
   pre-R-D20 drift Phase 0 caught. **Proposal:** rebind the three mirrors' `--pri`/`--pri-hover`
   (+ Modals secondary set if applicable) onto the same button/* paths as Button.reference; Legacy
   keeps its red CTA via the existing `button/primary/background/default` override in
   `apollo-legacy.overrides.json`. Colour change ⇒ Dave/conductor enacts, not me.
2. **Links `--arrow` → `primary/background/default`** — same class: red chevron on standalone links
   under Mono (R-D19: Mono's only red = status/RAG/dataviz). Fold into the same ruling as (1) —
   red-accent-once-per-screen (07-14 rule) vs B-D1-mono is exactly the tension Dave should rule once.
3. **Tabs under Mono: active bar + `More` count badge red** — `tabs/active` still resolves Legacy red.
   Known §A-AUTH C "**ruling owed**" (Mono = ink indicator); now confirmed live in the harness. The
   `.ovcount` badge binds `tabs/active` too, so one ruling moves both.
4. **Video-player is theme-UNREACHABLE beyond text/page** — `:root{ --controls:#FFFFFF;
   --accent:#DB0011; --scrim:#000000D9; --focus:#4d9fff; }` + `--muted:#767676/#9a9a9a` are all
   **absent from the manifest** and outside the theme blocks: no theme can reach them. `--accent` =
   Legacy red leak in Mono; `--focus:#4d9fff` is a rogue blue, ≠ `focus/ring` (#305A85/#4587A7);
   greys trigger the standing **grey-tint check** before any swap. **Proposal:** manifest them
   (focus/ring is a straight rebind; accent + scrim + controls need token homes; greys → surface to
   Dave with numbers).
5. **Legacy reach is GOOD on my slice** — Confirmation: teal roundel + red Done CTA, "3 var(s)
   re-bound"; List-items: 9 vars re-bound, teal Received/Approved, amber Pending, red Declined, both
   modes. Bonus: the Legacy-dark render shows the **white-tick-on-teal roundel** — live evidence for
   the queued §C·2 `text/on-success` black-vs-white ruling.
6. **Gate blind-spot (for the conductor):** a Mono surface resolving base `#DB0011` (findings 1–3) is
   not flagged by the R-D17 legacy-leak gate — scope presumably doesn't cover snippet-resolved
   values / pre-migration roles. Same shape as the declared-pairs contrast blind spot. Worth a line in
   `_DS-IMPROVEMENTS.md` or widening after the mirrors rebind.

## Open questions

- **Tabs is §A-AUTH "DO NOT ALIGN — archived"** (tab canon = the Reconciled tab+stepper), yet it was
  in my brief's worklist and is now migrated + STRICT. No harm (radius ≠ colour align; it stays gated
  while it lives in `snippets/`), but confirm the ratchet should keep archived files or they leave the
  dir instead.
- Tag-atom role ruling (above) — coordinate with Worker A's Tags file.

## Files touched (mine — plus note Worker A's parallel edit)

- `knowledge/snippets/{Tabs,Modals,Account-card,Table,List-items,Action-bar,Confirmation,Links,Notifications,Video-player}.reference.html`
- `knowledge/_validate_radius.py` (10 basenames added; **`Input-fields.reference.html` appeared from
  Worker A mid-session — left intact**, shared-tree merge fine)
- Regenerated: `knowledge/_RADIUS-GATE.md`, `canon/canon.css` AUTO blocks, `showroom/*` (11 pages)
- This receipt. **NO commits made; no shared-state files touched.**

## Proposed §C lines

- Rebind Button-MIRROR primaries (Action-bar/Modals/Confirmation `--pri*`) + Links `--arrow` onto the
  button/* ladder — kills the Mono red leak; Legacy override already carries the red CTA. Needs Dave
  (colour). Evidence: worker-B receipt findings 1–2.
- Rule `tabs/active` Mono value (ink, per §A-AUTH C) — one ruling also fixes the More-badge.
- ~~Manifest Video-player's `:root` styling vars~~ **DONE in-session (Dave ruled live). Superseding
  §C line → ★ FAST FOLLOWER: Video-player review** — Dave (end-of-session, ~22:05 BST): current state
  "fine-ish for now… lets make it a fast follower". Scope in `_REVIEW-SIGNOFF.md` (on-scrim bigplay
  incl. white-in-Legacy · darkened muted · scrub played-vs-track). Queue it NEAR-TERM, not inside the
  consolidated Mono pass.
- Flip canon `.cn-tabs .indicator` → indicator role (match Worker B snippet refinement).
- Rule the tag-atom radius role once (control vs indicator) across Tags/Account-card/List-items.

---

# ADDENDUM — same evening (~21:25 BST): Dave ruled in-session; findings 1–2 + video-player ENACTED

*Provenance: Dave, this session, on the receipt findings — quoted the ADR-0009 BUTTON/PRIMARY Mono
ladder and ruled: (a) "Primary is #1A1A1A for primary always"; (b) video player is provisional —
"theme it and make the primary action colour #1A1A1A"; (c) "#DB0011 should be bound to Legacy only."
These are enactments under EXISTING rulings (B-D1/ADR-0009 + R-D19) — slot-population, no new ledger
entry needed (reference-don't-duplicate). Tabs `tabs/active` (finding 3) NOT ruled — still queued.*

**Enacted (manifest rebinds; projector flowed values; CSS untouched except Video-player):**

- **Action-bar / Modals / Confirmation** `--pri`/`--pri-hover`/`--on-pri` →
  `button/primary/{background/default, background/hover, label/default}`. Hover keeps the mirrors'
  colour mechanism using the STORED hover colour (#626262/#B7B7B7 — spec-sanctioned "portable").
- **Links** `--arrow` → `button/primary/background/default`; stale "brand red" header comment fixed.
- **Video-player THEMED:** `--accent`/`--accent-label`/`--controls`/`--scrim`/`--focus` moved from
  `:root` into both theme blocks + manifested → `button/primary/background/default`,
  `button/primary/label/default`, `text/reverse`, `overlay/version2` (exact #000000D9 match — no new
  token needed), `focus/ring` (kills the rogue `#4d9fff`). `.bigplay` `color:#fff` literal →
  `var(--accent-label)`. **`--muted`: initially held for the grey-tint check → Dave RULED same
  evening ("this is fine, resolve to the near black") → BOUND to `text/secondary`
  (#767676/#9a9a9a → #1A1A1A/#FFFFFF, deliberate darkening); review flag added to
  `_REVIEW-SIGNOFF.md` consolidated-pass list (Dave: "we can review later").**
- **Declared contrastPairs updated** in all four to the ladder paths (they still pointed at
  `primary/*` — would have been the declared-pairs blind spot again).

**Verified (probe + renders):** build **42/42 green**; computed-style probe across themes ×
light/dark: Mono + Console primaries = `#1A1A1A`/label `#FFFFFF` (light), `#FAFAFA`/label `#333333`
(dark); **Legacy = `#DB0011` white-label via its override set** — red now unreachable outside Legacy
on these surfaces. Links arrow + bigplay follow identically.

**New flag for Dave (from the Mono render):** the bigplay sits on the always-dark VIDEO substrate —
under Mono LIGHT the #1A1A1A button runs low-contrast against the dark thumbnail (dark mode #FAFAFA
pops). May want the on-scrim treatment (reverse fill both modes, like `--controls`) or a scrim-aware
primary variant. Enacted as ruled; visibility question queued.

**→ RESOLVED same evening (~21:55):** measured it for Dave — light-mode fill **1.2:1** vs video
(fail 1.4.11; note the OLD red was itself only 2.7:1 against the lighter gradient end — pre-existing,
exposed not caused). Dave: **"yes but let me eyeball"** → ON-SCRIM treatment ENACTED: bigplay fill →
new `--onvideo-fill` bound `text/reverse` (white BOTH modes, 14–19:1); glyph `--accent-label` now
#333333 both modes via **driftAllow ["light"]** (documented on-scrim exception in the manifest);
themed `--accent` remains on the scrub `.played` (Legacy scrub stays red; **Legacy bigplay is now
white too** — flagged for the eyeball). Render-verified both modes; build 42/42 green (Worker A's
earlier reds cleared — their loop completed). Sign-off pending Dave's eyeball per `_REVIEW-SIGNOFF`.

**Files touched by the addendum:** the same 5 snippets (Action-bar, Modals, Confirmation, Links,
Video-player) + `knowledge/_REVIEW-SIGNOFF.md` (surgical append: Video-player review flag, Dave's
instruction) + regenerated `canon/canon.css` AUTO blocks and `showroom/*`. Still NO commits.

**⚠ Build-state note for the conductor (shared-tree attribution, ~21:40 BST):** my last clean full
build was 42/42 green. A later re-run went red on **Worker A's in-flight files only** — Badge
(rag/error-background dark 2.89:1) + Progress-tracker (`--complete` #DB0011 vs projected
#B92F1E/#CC4333) + the sync gates stale against those same two. **No worker-B file appears in any
failure**; radius gate 0 strict / 0 advisory (the full 21-file ratchet is now migrated across both
workers). I deliberately did NOT run A's projection steps over their half-edited state — reconcile
after A's receipt lands.
