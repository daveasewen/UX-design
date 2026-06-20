# Integrity token-path warnings — triage (2026-06-20)

The integrity lint's best-effort TOKENS pass (WARNING-only) flagged **20** "token path may
not resolve" warnings over the meta `tokens` prose. Triaged below. Net: 20 → **3**, all of the
remaining 3 are intentional documentation, not defects. No canon/snippet/appearance changed —
these are descriptive metadata strings only.

## Root cause (18 of 20): deprecated-binding prose
The bulk were the regex matching **deprecated token names written on purpose** in the Section-4
migration backlog notes — e.g. `rag/icon (depricate)/error/icon … → rebind rag/text/on-dark`.
The old (deprecated) path is *expected* not to resolve; that's the whole point of the note. The
lint already intended to skip these (it skipped paths literally containing `depricate`), but the
`(depricate)` marker sits in the surrounding prose, not inside the extracted path token, so they
slipped through.

**Fix:** in `_build_integrity.py`, the TOKENS pass now skips any `tokens` value that documents a
deprecated/migration binding (`"depricate"/"deprecated"` in the value). WARNING pass only —
ERROR logic and exit codes untouched. Live rebind *targets* remain ERROR-checked by the REBIND
pass, so nothing real is lost. This cleared all 18:
Input fields, Notifications, Pagination (×2), Quick actions (×3), Selection controls, Slider,
Status indicator, Tags (×4), View options.

## Plain-English false matches (2 of 20): prose typo fixes
- **Button** — `…solid buttons (primary/secondary)…` meant "primary & secondary buttons"; the
  slash made it look like a token. Reworded to `(primary & secondary)`.
- **Hero** — `blur/surface (… radius blur/background-surface = 12)` was loose shorthand; the real
  token `blur/background-surface` was already named beside it. Dropped the shorthand.

## Residual (3) — intentional, left as-is (worth a glance, not defects)
- **Modals `overlay/background-blur`** — the prose explicitly documents the *Figma* name and says
  it resolves to the store token. Informational mapping note; left verbatim.
- **Tabs `layout/focus/ring-width`, `layout/focus/ring-offset`** — these are the **proposed**
  focus-ring tokens, not yet in the store. They track the lane-C `focus/ring` sign-off
  (`_FINDINGS-INDEX.md §6`). Leave until that decision lands; warning is the correct signal.

## Verification
`python3 _build_all.py` → EXIT 0; integrity PASS — 0 errors, **3** warnings (was 20); schema 32/32.
