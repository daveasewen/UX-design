# #311 lane A1 (overnight wave 1) — the shared stylesheet and "link, don't paste": both checks now read one answer; pages are refused from sizing parts

COUNTS: build commit 50159e7a · rulings built 2 (s307-D74 whole, s307-D75 all but a legacy ledger) · stamped enacted 1 (s307-D74) · rows closed 1 (W-307yc) · rows left open with progress 1 (W-307yd: 15 sizing rules on 4 old fitness screens, pinned shrink-only) · canon regens 1 (one line, Links) · gates run: compose PASS, receipt --selftest PASS (AK–AP new), gen_provenance_receipt --selftest PASS (G new), snippets 137/0, gen_canon_components --check in sync, test_gates 36/36 (run case by case) · false red found and fixed in the new check 1

## What this seat found
This lane was launched twice. The first A1 seat (21:18–22:13 UTC, no report filed) left the whole build uncommitted in the working tree: the two gates, the receipt mint, four bite-tests, the Links snippet and one canon line. This second seat read every changed line against the two rulings, ran it, found one false red in it, fixed that, and committed. Nothing the first seat wrote was taken on its word.

## s307-D74 — link, don't paste; the two checks agree (W-307yc)
Dave, by click, 2026-09-28 21:17 BST: "Link, don't paste; make both checks agree". The #246 lane B finding was that the receipt gate passed a page that pasted every part's `<style>` in, and the compose gate failed the same page.
- `knowledge/_validate_receipt.py`: new `link_or_paste(html)` — `STYLE-PASTED` when a region is spliced with `kind=style`, `CANON-NOT-LINKED` when no live (uncommented) `<link rel=stylesheet>` names canon.css. Step 3c of `check()` calls it.
- `knowledge/_validate_compose.py`: check 10 calls the SAME function from `check_screen`. One definition, two readers: they cannot disagree.
- `knowledge/gen_provenance_receipt.py`: the mint refuses `kind=style` and writes `<link>` to canon.css and type.css, wrapping each markup region in its `.cn-<slug>` scope outside the hashed bytes.
- Proof: receipt selftest arms AK–AO (linked passes; pasted, unlinked, commented-out link and `mycanon.css` all red) and AP (the compose gate returns the same verdict on linked, pasted and unlinked pages: `linked c=[] r=[]; pasted c=['STYLE-PASTED'] r=['STYLE-PASTED']; unlinked c=['CANON-NOT-LINKED'] r=['CANON-NOT-LINKED']`). Mint selftest G: `kind=style REFUSED (True); minted page links canon.css and the compose gate agrees (no compose fails)`. test_gates cases "compose gate bites on a pasted stylesheet" and "… canon.css unlinked" PASS.
- The pack skill already says to link (apollo-spider/skills/generate-from-canon/SKILL.md, step 5 "Link knowledge/canon/canon.css"); no `kind=style` survives anywhere in knowledge/ outside the gates and their tests (grep).

## s307-D75 — rebuild the shared stylesheet; a page places parts and never sizes them (W-307yd)
Dave, by click, 2026-09-28 21:17 BST: "Rebuild the shared stylesheet".
- The stylesheet carries the parts' rules: `gen_canon_components.py --check` → "137 components in sync"; the #248 rule 6b now sits in canon (`canon.css` `:where(.cn-template-dashboard-bento) .tpl-page .c-bento__tile.tpl-group-context{grid-column:1 / -1;}`).
- Demo widths are real defaults: the last canon read of the showroom dial was Links' `.related{max-width:var(--demo-width, 560px)}`; it is now `max-width:560px` in the snippet and canon (the one-line regen), and `_render_links.py` sets `max-width` on `#related` for its narrow shot. canon.css now reads `--demo-width` 0 times outside comments (15 mentions, all in comments recording the old values). `--demo-width` left `RUNTIME_VARS`; compose check 11 reds any read of it in canon.
- Pages never size a part: compose check 9 reds a page whose own `<style>` or inline `style=""` sets font-size, height, min-height, padding, width, zoom or transform on a part (a `.c-*`/`.cn-*` class, or a class canon defines under a `.cn-*` scope the element sits inside).
- FALSE RED FOUND AND FIXED (this seat): the first seat's check 9 counted a part's own data API as sizing. The snippets themselves write 161 inline sizing declarations over 41 (class, prop) pairs — Meter's `.meter-fill` width, Progress-bar's `.pb-fill` width, Skeleton's `.bone` widths, Links' `.arrow` font-size, Tags' `.tag.link` font-size. A faithful splice of Meter would have failed the compose gate — the very link/paste disagreement D74 closed. New `_part_inline_api()` reads those pairs from the 137 snippets, scoped by part, and licenses them. Proof: `<div class="cn-meter">…<div class="meter-fill" style="width:62%">` → 0 hits; the same with `.meter-track style="height:20px"` → 1 hit.
- The legacy ledger: four older hand-composed fitness screens size parts. Pins, shrink-only, after the fix: canon-gallery 2 (was 21), nio-dash-console-v1 4 (was 8), nio-dash-console-v2 8 (was 12), payments-journey 1. Hits: canon-gallery `.cn-modals .overlay {padding}`, `.cn-modals .overlay .dialog {transform}`; payments-journey inline padding on `.cn-summary`; nio v1/v2 `.nio-shell .sh {min-height}` and inline padding on the three segmented-control chart wrappers; nio v2 also `.sh-masthead {width}`, `.nio-donut-split .dv-svg {width,height}`, `.nio-leg-list .dv-legrow {width}`, `.row .tag {padding,height}`. A new hit on any of them reds; a lower count prints a note to lower the pin.
- So W-307yd's `closes_when` ("the page carries no sizing rules") is met for every new page and NOT for these four: the row stays open by addition, and s307-D75 stays `ruled`.

## Gates run (at the seat, TMPDIR=/dev/shm)
`_validate_compose.py` RESULT PASS (7 screens) · `_validate_receipt.py --selftest` PASS · `gen_provenance_receipt.py --selftest` PASS · `_validate_snippets.py` 137/0 · `canon/gen_canon_components.py --check` in sync · `knowledge/_tests/test_gates.py` 36 tests, 0 failures — run case by case through `/tmp/a1/tg_one.py` (the seat's call ceiling tonight swung between 6 s and 33 s, below the suite's ~140 s), results in `/tmp/a1/tg_results.txt`. `_wrap_commit.py unlock --tag 311-A1` after.

## Found, not fixed
- The 15 legacy sizing rules above. canon-gallery's 2 wait on W-307q2 (keep or retire that page, Dave's). The nio and payments ones change how reviewed screens look, so they are a build with a look, not a gate fix.
- The Tabs part's real default is `--tabs-w:640px` (canon.css, unfenced); whether it should fill its container is Dave's (lane D's W-307ye question, job F's page). Not touched here.
- Eighteen older pages under `outputs/` and `reviews/` carry receipts minted before D74; none is in a gate's population. `reviews/COLDRUN-267-2026-09-10-v1.html` reports NO-RECEIPT, `outputs/baseline-246/arm-B-sighted/dashboard.html` reds on BEHAVIOUR-NOT-LOADED (pre-existing, not this change).
- The chart receipts were not re-driven: canon moved by one Links line no chart page reads. The combined-HEAD survey is the check.

## Ruling-shaped questions
- None new. The legacy four are a "look" question only if Dave wants the old fitness screens kept; if they are history, retiring them empties the ledger.

## Commits
- `50159e7a` — the build: the two gates, the mint, four bite-tests, Links snippet + its one canon line, `_render_links.py`, `_COMPOSE-AUDIT.md`, and `showroom/links.html` (the commit script's showroom sync gate asked for `gen_showroom.py` after the Links snippet changed; 1 page written).
- The stamp commit (this report, `knowledge/_rulings.json` s307-D74 → enacted at 50159e7a with the reconstruction proof PASSED, `knowledge/_state.json` W-307yc closed / W-307yd note / born-closed row W-311an, `gen_kg_titles.py --write`, `_render_rulings.py`) follows it; its sha is in `git log`.
- The commit lock was waited on for about two hours (D13, F2, C0 and H2 held it in turn); it was never broken.
