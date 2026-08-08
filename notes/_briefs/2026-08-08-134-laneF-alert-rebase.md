# laneF — Alert.reference.html rebase to token spine (2026-08-08)

Source of truth: `knowledge/tokens/semantic-colour.json` rag/* `$value`s (s122-D2 mono
mode-invariant, s123-D3 tint = tuned opacity, s134-D3 amber already current).

## Old → new (retired values now live in inline comments, not erased)

| var | old light | old dark | new (both themes) | spine line |
|---|---|---|---|---|
| --err | #B92F1E | #CC4333 | **#F6604C** | error-background ~465 |
| --warn | #E0A61F | #E0A61F | #E0A61F (unchanged, s134-D3) | warning-background ~485 |
| --ok | #2B7E4F | #4A9568 | **#66CC8D** | success-background ~505 |
| --info | #306EC6 | #2674DC | **#78A7E8** | information-background ~528 |
| --err-t | #F1E0DC | #2C120D | **#FDD9D4 / #60302A** | error-tint ~571 |
| --warn-t | #F6E5CC | #3C2C13 | **#F6E6C0 / #614C1C** | warning-tint ~584 |
| --ok-t | #DCEDE3 | #12291D | **#D4F1DF / #32533F** | success-tint ~610 |
| --info-t | #D6E3EC | #092131 | **#DFEAF9 / #38475C** | information-tint ~636 |
| mark (all 4 statuses, both themes) | mixed (tint-knockout / white / #1A1A1A) | white-shape/black-mark literal | **flat #1A1A1A** | s122-D2 note, all four `-background` entries |

Per-status `.ic` mark overrides (old ~117-121) and the dark-theme white/black roundel
override retired by declaration, citing s122-D2; s134-D2 confirmed no theme flip for Mono.

## Computed mark-on-shape (new bytes, #1A1A1A mark)

error 5.55:1 · warning 7.99:1 · success 8.77:1 · information 7.04:1 — all ≥4.5, both
themes (shapes mode-invariant). Matches spine prediction (~5.55/7.99/8.77/7.04) exactly.
This RESOLVES the prior s134 [WARN] flag (err 3.68 / ok 3.63 failing in dark under the
old white-mark scheme) — nothing remains open on this axis.

## Selftest

`python3 knowledge/_validate_state_contrast.py --selftest` → 18/18 arms `ok`, then named
refusal `StateContrastSelftestError: playwright not installed`. **rc=2** (checked directly,
not through a pipe).

## Deliverables

- `knowledge/snippets/Alert.reference.html` — rebased, stale comments updated by addition.
- `reviews/_alert-light-specimen-2026-08-08-s134-v2.html`, `_alert-dark-specimen-...-v2.html`
  — fresh byte-copies of the fixed snippet (v1 untouched).
- `reviews/ALERT-ERROR-MARK-REVIEW-2026-08-08-s134-v2.html` — iframes repointed to the
  -v2 specimens, copy updated to reflect the flat-mark/no-flip as-built (v1 untouched).

DO-NOT-RULE respected: no token spine edits, no new colours, no commits, no rulings/chain
edits, nothing removed (all old material retained by addition or left as v1 copies).
