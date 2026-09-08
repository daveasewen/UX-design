# #261 lane R — his rulings page

**What.** The carried item (four sessions, never built) is built: a surface where Dave reads
his own rulings back. Built as a GENERATOR so it stays current at every wrap, not as a
one-off page that rots.

- `knowledge/_render_rulings.py` — 17,484 bytes. Reads `knowledge/_rulings.json`,
  writes `notes/_RULINGS.html`. `--out PATH`, `--src PATH`, `--check`.
- `notes/_RULINGS.html` — 762,382 bytes, self-contained (no CDN, no external fonts,
  no `<link>` at all — `grep -c "cdn\|https://fonts\|<link"` = 0).

**How.**
- 408 rulings, 137 id-groups, newest-first, grouped by id prefix (`s260`, `ds-`, …),
  groups ordered by latest date then session number.
- Each entry: id (mono, anchored `#s260-D5`), date, `by`, status pill, `ruled` in full,
  `says` as a bordered pull-quote — the point of the page — `governs` (mono, wraps),
  `evidence`, and the full `status` prose when it is longer than the pill.
- Status is 178 distinct free-text strings on disk; the pill normalises by first keyword
  found, in order SUPERSEDED → REVERSED → ABANDONED → PART-ENACTED → IN PROGRESS →
  ENACTED → BUILT → STANDING → OPEN → RULED → OTHER. Tally: RULED 276, ENACTED 108,
  STANDING 8, BUILT 5, OPEN 4, SUPERSEDED 3, PART-ENACTED 2, IN PROGRESS 1, OTHER 1.
  The full original string is still shown, so the normalisation loses nothing.
- Client-side vanilla JS, inline: text search over each article's textContent
  (id/ruled/says/governs/evidence), status filter, `by` filter, "Dave's words only"
  toggle (CSS class on body, hides everything but id + quote), live matched count,
  empty state, session headers auto-hide, and a hashchange handler that clears filters
  when you follow an anchor to a hidden entry.
- Swiss: system stack, 8px spacing scale, hairline rules between sections and entries,
  ultra-light stat numerals, the accent-dash label pattern, no shadows/radius.
- TWO-RED LAW honoured: `--accent:#DA1A00` on `:root` (white), `--accent:#F6604C` under
  `prefers-color-scheme:dark`. Accent is label, quote border, active pill outline and
  matched count only — never body text.
- Light/dark by `prefers-color-scheme`, all colour on `:root` tokens.
- 375px: single-column at ≤760px, `overflow-wrap:anywhere` on paths, controls
  `min-width:0;max-width:100%`. Print: filter bar and details hidden, black on white,
  `break-inside:avoid` per ruling.

**Verification receipts (verbatim).**

    $ python3 knowledge/_render_rulings.py
    wrote /sessions/zen-funny-hawking/mnt/UX-design/notes/_RULINGS.html  408 rulings  137 sessions  762382 bytes  sha256 e69957c57eeb9800835009732b793e21cd66a0a0bb1ad075300e75ba9c3365a7

    $ python3 knowledge/_render_rulings.py --check   # exit 0
    FRESH _RULINGS.html matches _rulings.json sha256 e69957c57eeb9800835009732b793e21cd66a0a0bb1ad075300e75ba9c3365a7

    $ python3 - (html.parser, stack-balance + count)
    parse: mismatched=0 unclosed=[] articles=408 unique_ids=408

RED PATH DRIVEN, not assumed — one byte mutated inside a `says` value in a temp copy:

    $ python3 knowledge/_render_rulings.py --check --src $T/mut.json   # exit 1
    STALE _RULINGS.html embeds e69957c57eeb9800835009732b793e21cd66a0a0bb1ad075300e75ba9c3365a7 but mut.json is now 16a87b7725e1e8d0cc8fbb0b4ed145c30f3bed3e53c1fafd46f1e7101dfb7f4a
    $ python3 knowledge/_render_rulings.py --check --src $T/same.json  # control, exit 0
    FRESH _RULINGS.html matches same.json sha256 e69957c57eeb9800835009732b793e21cd66a0a0bb1ad075300e75ba9c3365a7

**Not verified.** No browser was reachable this lane (workspace chromium is missing
`libxdamage1`; the pane refuses `file://`). The 375px no-overflow claim, print output and
the JS filters are argued from the CSS/JS, NOT driven. A follow-up lane with playwright
deps should screenshot 375/768/1200 × light/dark and assert `h-overflow=0px`, per the
usual `_render_*` convention. Do not treat those three as green until then.

**Open questions for Dave.**
1. Should `--check` become a WRAP-RITUAL GATE — wrap fails if `_RULINGS.html` is STALE?
   The hook exists and exits 1; wiring it into the wrap is HIS ruling, not mine.
2. `by` is "Dave" for all 408, so the `by` filter is a one-option control today. Keep it
   (future-proof) or drop it?
3. Status normalisation buckets above are mine. If any bucket name is wrong in his
   vocabulary, say so — it is a one-line list in the generator.
