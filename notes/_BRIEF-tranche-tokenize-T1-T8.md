# Worker brief — tokenize the pro-forma tranches T1–T8

*Written by the composer (conductor session), 2026-07-19 afternoon. You are a WORKER: work in an
isolated worktree, do NOT commit, hand back a **receipt** in `notes/_receipts/` for the composer to
reconcile + commit. Companion: `_RUNBOOK-parallel-conductor.md`, `_STANDARDS.md` §1.*

## Why
The 8 tranche files (`knowledge/_proforma/Tranche-1..8-interactive.html`) hardcode their theme values in
`[data-theme="light"]/[dark]` blocks and carry **no `#token-manifest`**, so they've drifted from the
token store — they still render pre-R-D16 ink `#333333`, surfaces `#1D1D1D`, borders `#707070`, none of
today's 3-tier or elevation work. `_STANDARDS.md` §4 says components are **styled BY the tokens**. Fix
the drift the right way: make each tranche's theme block a **projection of the store**, not a hand-typed
copy — so it can never drift again.

## Approach (do NOT hand-edit values — project them)
1. **Extend the existing projector** `knowledge/gen_snippet_tokens.py` to also target
   `knowledge/_proforma/Tranche-*-interactive.html`. It already projects a `#token-manifest` into
   `[data-theme]` blocks for snippets; tranches use the same bare `[data-theme="light"]{ }` block shape,
   so the same `project()` logic applies. Add a tranche glob (keep snippets working). It resolves each
   token's `$value` (the gate-verified cache) — so 3-tier tokens like `surface/raised` resolve correctly.
2. **Add a `<script type="application/json" id="token-manifest">` to each Tranche-1..8**, mapping its
   local theme vars → token paths per the table below. (Verify each tranche's var set first — they
   descend from the same `_PROFORMA` base so they should match T6; handle any extra vars per-file.)
3. **Run the projector**, then **gate**: `python3 knowledge/_build_all.py` must stay green (35/35). The
   `_validate_proforma` universal gate allows hex only inside theme blocks — which is now generated.
4. **Receipt** in `notes/_receipts/2026-07-19-worker-tranche-tokenize.md`: what changed, the gate result,
   and the FLAGGED items (below) for the composer to rule on. Do NOT commit.

## The mapping — BIND THESE (clean, unambiguous)
| tranche var | → token | note |
|---|---|---|
| `--page` | `background/default` | ground |
| `--raised` | `surface/raised` | the new dark elevation (L #FFFFFF / D #1F1F1F) |
| `--ink` | `text/default` | now #1A1A1A/#FFFFFF |
| `--ink2` | `text/secondary` | ⚠ R-D16 collapsed this to the single ink — muted text goes full-ink; that's the ruling |
| `--line` | `border/subtle` | |
| `--fbord` | `form/border/default` | |
| `--fborda` | `form/border/active` | |
| `--fbordd` | `form/border/disabled` | |
| `--icon` | `icon/default` | |
| `--icon-rev` | `icon/default-reverse` | |
| `--focus` | `focus/ring` | |
| `--err` | `rag/error` | |
| `--err-t` | `rag/error-tint` | |
| `--warn` | `rag/warning` (`warning`) | |
| `--warn-t` | `rag/warning-tint` (`warning-tint`) | |
| `--success` | `rag/success` (`success`) | |
| `--success-t` | `success-tint` | |
| `--info` | `rag/information` (`information`) | |
| `--info-t` | `information-tint` | |

## FLAG — do NOT invent; bind to the suggested default and RECORD in the receipt for composer review
These tranche vars have no exact token today. Bind to the suggested nearest token, but **flag each in the
receipt** so the composer can rule (some may need a new semantic token):
- `--pri` / `--pri-h` / `--pri-lbl` — **the mono PRIMARY-ACTION button colour** (near-black bg / near-white
  label). There is **no semantic token for this** — a real gap. Suggested interim: `--pri`→`text/default`,
  `--pri-lbl`→`text/reverse`, `--pri-h`→ hover (no token). **This likely needs new `action/primary/*`
  semantic tokens — composer/Dave decision. Flag prominently.**
- `--disi` (#B7B7B7/#767676) → suggest `text/disabled` (value will shift lighter; disabled = contrast-exempt).
- `--line2` (#EDEDED/#3A3A3A faint divider) → suggest `divider/border/break` (dark value shifts noticeably lighter) — flag.
- `--surf` (#F3F3F3/#212121) → suggest `surface/subtle` — flag.
- `--scrim` → `overlay/version1`; `--shadow` → `elevation/functional`. Near, not exact — flag.

## Guardrails
- **Values are already ruled** — you are re-pointing to the store, not choosing colours. Do NOT promote or
  invent tokens (promotion is Dave's alone). Where a binding needs a decision, FLAG it, don't decide it.
- Keep every non-theme rule intact (real icons, 4px grid, square corners, motion). Only the theme-block
  **values** change (via projection) + the added manifest.
- Isolated worktree; **no commits**; receipt only. The composer reconciles + commits.
- If a tranche's var set differs from the table, handle the extras per-file and note them.

## Definition of done
All 8 tranches carry a `#token-manifest`; `gen_snippet_tokens.py --check` reports them in sync; build
green 35/35; receipt filed with the flagged items. Composer picks it up from the receipt.
