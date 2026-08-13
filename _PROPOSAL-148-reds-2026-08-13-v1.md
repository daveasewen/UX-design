# PROPOSAL — the five OPEN #148 gate reds, re-measured (#168, Opus sub)

**Status:** MEASURED, not ruled. Nothing here is minted; `knowledge/_rulings.json` untouched.
**Measured:** 2026-08-13 at HEAD `0ce19ae`, each gate driven individually (never `_build_all.py`).

## 0. FIRST FINDING — the red NUMBERS rotted before the reds did

#148's reds were recorded as STEPS **positions** (`30 · 36 · 45 · 51 · 82`) in a **110-step** list at
HEAD `9524f0189`. `STEPS` is now **117** entries, so those positions address different steps today
(current position 30 = `_build_live_state.py`, not the text/icon contrast audit). The reds were
re-resolved at the #148 HEAD (`git show 9524f0189:knowledge/_build_all.py`, AST-parsed) and are
carried below **by script path**, which is the stable address.

| #148 pos | script (stable address) | current pos |
|---|---|---|
| 30 | `_build_surface_contrast_audit.py` | 34 |
| 36 | `gen_token_ramp.py --check` | 40 |
| 45 | `_validate_snippets.py` | 49 |
| 51 | `gen_showroom.py --check` | 57 |
| 82 | `_validate_dataviz.py` | 89 |

## 1. Measured state — three of five are GREEN, and they still BITE

| red | rc today | mutation (break → fix) | verdict |
|---|---|---|---|
| 36 `gen_token_ramp --check` | **0** — `0 file(s) DRIFTED … 87 already in sync` | inserted a line inside `AUTO-TOKENS` in `snippets/Accordion.reference.html` → **rc 1**, `1 file(s) DRIFTED`; restored → **rc 0** | **CLOSED, proven live** |
| 45 `_validate_snippets.py` | **0** — `75 snippet(s), 0 failure(s)` | added `<a href="/x">click here</a>` → **rc 1**, named `aca-004` failure; restored → **rc 0** | **CLOSED, proven live** |
| 51 `gen_showroom --check` | **0** — `75 page(s) + index in sync` | added a comment to `showroom/accordion.html` → **rc 1**, `OUT OF SYNC — stale: ['accordion.html']`; restored → **rc 0** | **CLOSED, proven live** |

Each green was mutation-tested precisely because a green that cannot fail is an assertion, not a
measurement. All three bite, with a named message. All mutations were reverted and re-measured green.

## 2. The two that are still RED — and they are ONE finding

Both remaining reds are **downstream of `s122-D2`** (Dave, #122 — MONO RAG re-based by eye off the
mark-map-controller). The re-base moved the RAG values LIGHTER, and two contrast gates that were
satisfied at the retired values now breach at the new ones. The gates are correct; the token/consumer
pairing was never re-decided after the re-base.

### Red 30 — `_build_surface_contrast_audit.py`, rc 1
```
text/icon contrast audit: 18 OK, 4 allowed, 1 GATING FAIL, 5 skipped(light-only)
  ❌ rag/text/on-dark: 3.14:1 on #F6604C (need 4.5:1, text)
```
`rag/text/on-dark` = `#FFFFFF`. The surface is `rag/error-background`, whose own `$note` records:
> "R-D14 LOCKED (breach): mode-stable #B92F1E, WHITE text (white 6.02 both grounds). … s122-D2 …
> MONO RAG re-based to #F6604C … Prior values retired to this note: light #B92F1E / dark #B92F1E."

So the white pairing was ruled at **#B92F1E (6.02:1)** and inherited by **#F6604C (3.14:1)**. The
other three RAG backgrounds are already in `RULED_PAIR_EXCLUSIONS` (`_contrast_utils.py:159`) because
a ruling forbids white on them; error is the only one where white is still the ruled ink.
Note `s149-D1` flipped the ink to `#1A1A1A` **on `#F6604C` — MONO ONLY**, so it does not by itself
settle this token. Also measured: `canon/canon.css` carries theme-keyed values (`#A8000B`, `#B92F1E`)
while `tokens/semantic-colour.json` carries only `#F6604C` — the audit reads the store, so it is
grading the MONO value for every theme.

**Options (Dave's, priced):**
- **A — a fourth `RULED_PAIR_EXCLUSIONS` entry** (`rag/text` × `rag/error-background`), citing that
  error red carries `#1A1A1A` ink like the other three. ~20 min. ⚠ only honest if the ink rule is
  ruled for **all** themes, not mono only; otherwise it hides a real breach in legacy/SC/console.
- **B — re-seat `rag/text/on-dark`** for the error ground (a new mode/ground-keyed ink token). ~1 h,
  touches every consumer of white-on-error. Highest fidelity, largest blast radius.
- **C — theme-key `rag/error-background` in the store** so the audit grades per theme like canon.css
  already does. ~1–2 h. Fixes the *class* (store is mono-only while canon is per-theme) rather than
  this one pair; the widest fix and the only one that stops the next re-base doing this again.
- **D — declare and leave red.** 0 min, but the build stays red and the red is read as weather.

### Red 82 — `_validate_dataviz.py`, rc 1
```
[FAIL] snippets/Chart-bar.reference.html  (5 charts, 3 blocking, 50 advisory)
   ✗ dv-016 [series]: var(--status-watch)=#E0A61F vs surface #FFFFFF = 2.18:1 (<3:1) in light mode.
   ✗ dv-016 [series]: var(--status-healthy)=#66CC8D vs surface #FFFFFF = 1.98:1 (<3:1) in light mode.
   ✗ dv-016 [series]: var(--status-info)=#78A7E8 vs surface #FFFFFF = 2.47:1 (<3:1) in light mode.
```
Same root. Chart cb3 ("Payment exceptions by status") maps `--status-*` → `rag/*-glyph`, and the
glyph notes record the re-base verbatim: warning "3.02 on white (1.4.11 graphic grade) … re-based to
`#E0A61F` … Prior values retired: light `#C58900`"; information "re-based to `#78A7E8` … prior
`#306EC6`". The retired values were the **graphic-strength** ones the amber carve-out exists to
protect (`amber/graphic` was chosen *because* dv-016 demands ≥3:1). The re-base was ruled for MONO
**marks**; **chart series** inherited it silently. `s167-D1` scopes palette *sharing*; it does not
license status hues as series fills, so this is not a settled question being re-opened.

**Options (Dave's, priced):**
- **A — cb3 uses the data/series palette**, RAG reserved for marks/labels. ~30 min, snippet-local,
  no token change. ⚠ changes what the reference demonstrates (a RAG-coloured bar chart).
- **B — restore a graphic-strength RAG tier** (`rag/*-glyph` at the retired ≥3:1 values, with the
  re-based values kept for marks). ~2 h. Restores the R-D3 "two ambers" shape for all four hues.
- **C — a declared dv-016 carve-out for status-as-series** with a label-carries-the-meaning argument
  (R-D6). ~30 min. ⚠ this weakens the one blocking rule that made the amber carve-out necessary.
- **D — declare and leave red.** 0 min; same cost as 30-D.

## 3. Consequences / pitfalls
- Options 30-A and 82-C both **make a gate stop asking a true question**. Prefer them only with an
  explicit statement of what is no longer measured.
- 30-C is the only option that addresses the *class* (a mono-only store grading four themes); it will
  surface further pairs currently invisible — expect new reds, which is the point.
- 82-B re-opens values Dave ruled **by eye** at #122; it must be re-judged by eye, not by ratio.
- The positional-index rot in §0 will recur: the build reports reds by step NUMBER while `STEPS`
  grows. Reporting the script path alongside the number would make future records stable. **Reported,
  not fixed** — out of scope for this brief.

## 4. Residuals, declared
- **UNPROVEN:** that the three now-green reds were closed *deliberately*; no ruling naming them was
  found in `_rulings.json` (138 entries) or the memory record. They may have been closed as
  collateral. What is proven is that they are green **and can still fail**.
- **UNPROVEN:** the state of #148 red 63 (`_validate_state_contrast.py`) — outside this brief.
- Nothing was run through `_build_all.py`; step positions above are AST-read, not build-observed.
