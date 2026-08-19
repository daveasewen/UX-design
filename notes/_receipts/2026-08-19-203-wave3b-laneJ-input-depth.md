# Receipt — #203 Wave 3b, Lane J · input depth (Combobox 21 · Multi-select 22 · Tags input 23)

*Worker receipt against `_BRIEF-wave3b-verified-work-2026-08-19-v1.md` (read in full) and the base
brief `_BRIEF-wave3-foundations-2026-08-19-v1.md` it extends.*
*⛔ Nothing here is a ruling. No commit, no push. No `git checkout` / `restore` / `stash` of any kind
was run. No generator was run — not even `--check` (Lane G owns that surface this wave).*
*Author's context gauge at authoring: `_checkin.py` — FILL **145,808 real**, boot 56,488, peak 145,808
over 30 turns, room to the advisory stop line (150,929) **5,121**. ⚠ Declared, as Lane A declared it:
`_checkin.py` reads the live transcript and a sub cannot prove the transcript it found is its own
rather than the conductor's — treat the figure as ORDER-OF-MAGNITUDE for this sub.*

---

## Headline

**All three rows are TRUE gaps, and all three are now built, gated and shown in four themes.**
Unlike wave 3a — where 18 of 18 briefed "gaps" already existed — Lane J's step-0 probes came back
genuinely empty. The three components are the first new gated components of #203 for this lane, and
every shared grammar in them is copied from an approved artefact rather than re-drawn.

## Step 0 — the premise, verified first-hand (hardened per addendum §1)

| Claim inherited | Verdict | Probe, quoted |
|---|---|---|
| HEAD unstated; establish it | HEAD = **`ec2336d`** (#202 wrap) | `git log --oneline -1` |
| Row 21 Combobox / autocomplete absent | ✅ **TRUE — absent** | `ls knowledge/snippets/ \| grep -iE 'combo\|auto\|multi\|tag\|select\|chip\|token\|listbox\|typeahead\|pick'` → `Account-selector`, `Chart-combo`, `Date-picker`, `Date-range-picker`, `Selection-controls`, `Tags`, `Time-picker` — no combobox. `ls knowledge/components/` → no combobox/autocomplete/typeahead meta. `grep -rn 'aria-autocomplete' knowledge/snippets/` → **0 hits**. |
| Row 22 Multi-select absent | ✅ **TRUE — absent** | `grep -rn 'aria-multiselectable' knowledge/snippets/` → **0 hits**. ⚠ ALTERNATE-SLUG FINDING: `dropdown.meta.json` DOES declare a `multi-select (non-native)` variant and a `filterable single-select` variant — but the snippet's own header reads *"CANONICAL REFERENCE for the non-native single-select Dropdown"* and `grep -nE 'filter\|multi\|checkbox' Dropdown.reference.html` → **0 hits**. The variants were documented in the meta and never built. |
| Row 23 Tags input absent | ✅ **TRUE — absent** | `Tags.reference.html` EXISTS and is gated, but `grep -nE '<input\|contenteditable' Tags.reference.html` → **0 hits**; `tags.meta.json` declares `"category":"atom"` with variants `tag` / `tag-link` only. It is the DISPLAY half. The input half did not exist under any slug. |
| Itinerary wording for the three rows | verified verbatim | parsed the .xlsx with openpyxl: row 21 "Combobox / autocomplete … Type-ahead select", row 22 "Multi-select … Chips-in-field selection", row 23 "Tags input … Free-entry token field", all `Gap / P2 / 2 Depth`. |
| Baseline gate state before I wrote anything | measured | snippets rc=0 (76 snippets, **0** failures) · a11y rc=0 (179 warn) · type ratchet rc=0 (debt **1097**). ⚠ Lane A's receipt records "76 snippets, 18 failures, rc=1" for the snippet gate at the same HEAD; I could not reproduce that — it is **green** here, measured directly, twice. Flagged for the conductor rather than silently overwritten. |

**Searched twice before calling anything new** [[unrun-search-indistinguishable-from-absent-record]]:
`python3 knowledge/_memento_search.py "combobox autocomplete multi-select tags input"` → returns only
GOOD-MORNING sections (`gm:A:WHERE` and kin), nothing on point; and a direct regex over
`knowledge/_rulings.json` for `combobox|autocomplete|multi-?select|tags.?input|chips-in-field` →
**0 hits**. No ruling exists on any of the three. Nothing here re-opens a settled question, and the
seven decisions below are genuinely open rather than already answered (`s202-D3`).

## What was built (all NEW files, unique names — nothing existing was touched)

| File | What it is |
|---|---|
| `knowledge/snippets/Combobox.reference.html` | Type-ahead single-select. Boxed + underline field styles, live filtering, no-results seat, completed/disabled/error. |
| `knowledge/snippets/Multi-select.reference.html` | Chips-in-field **and** count-summary variants, `aria-multiselectable`, Backspace-removes-last, disabled/error. |
| `knowledge/snippets/Tags-input.reference.html` | Free entry; Enter/comma commits, blur commits, arm-then-remove Backspace, duplicate + limit refusals, empty/disabled states. |
| `knowledge/components/combobox.meta.json` · `multi-select.meta.json` · `tags-input.meta.json` | Metas, schema-valid, each with its own `$provenance-note` naming the step-0 probes. |
| `reviews/REVIEW-203-combobox-four-themes-v1.html` · `-multi-select-` · `-tags-input-` | 8 live panes each: 4 themes × light/dark, responsive at 1100px. |
| `notes/_receipts/2026-08-19-203-wave3b-laneJ-input-depth.md` | this receipt |

**Shared grammar copied, never re-drawn** (the #202 lesson): the field is the gated
Input-fields/Textarea boxed anatomy; the listbox is the gated Dropdown menu (`.menu/.opt/.tick/.sep`,
44px rows, light shadow / dark grey outline); the chip is the gated Tags chip (em-based, square
CONTROL radius, 24px hit pseudo-element on the dismiss, V1 collapse dismiss, the library close
glyph). Only the input-driven halves are new.

## Gates — every rc captured directly, never after a pipe

| Gate | Baseline (before) | After | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | rc=0 · 76 snippets, 0 failures | **rc=0** · 85 snippets, 0 failures | ✅ my three pass |
| `_validate_a11y.py` | rc=0 · 179 warn | **rc=0** · 186 warn | ✅ +7 warnings, ALL mine, all one class: `button.x` 24px dismiss — the gated Tags value inherited unchanged (see finding 3) |
| `_validate_type_composites.py --ratchet` | rc=0 · debt 1097 | **rc=0** · debt **1097, 0 new** | ✅ my three contribute **0** — zero raw font declarations in any of them (the Progress-bar precedent: `<link>` to type.css, every text element composed) |
| `_validate_state_contrast.py Combobox Multi-select Tags-input` | — | **rc=0** | ✅ 0 text failures, 0 carrier failures, 0 declared holes. 8 advisory declared seats (`data-carries="symbol label"`, correctly demoted) + 4 decorative icon warns (dark hover/pressed, 1.21:1, aria-hidden) |
| `_build_integrity.py` | rc=1 (see below) | **rc=0** · 0 errors, 79/79 schema valid | ✅ |
| `_validate_coverage.py` | rc=1 | rc=1 — **none of the FAIL lines are mine** | ⚠ the failures name `Command-palette`, `Sidebar-nav`, `Kpi-tile`, `Timeline` — other lanes' snippets landing without metas yet, mid-wave. My three names resolve. |
| `_validate_radius.py` | rc=0 | **rc=0** · 0 strict fails; the 1 advisory file is `Anchor-nav` (Lane I), not mine | ✅ |

⚠ **A gate caught a real defect in my own meta and I fixed it rather than routing around it.**
`_build_integrity.py` first ran **rc=1**: `[Tags input] relatedSC unknown to compliance lookup: 3.3.3`.
3.3.3 Error Suggestion genuinely applies, but `KNOWN_SC` is in a shared file this lane may not edit,
so the SC was removed from the array and the reason written into the meta as `$sc-note`. **Proposal
below.** Declared, not dropped silently.

**Gates left to the conductor, by name:** `_build_all.py` (all six), `gen_canon_components.py` (my
three have **no `.cn-` scope in canon.css** — stated in all three manifests and on all three review
pages), `gen_showroom.py` (CATEGORIES), `gen_theme_cascade.py`, and the coverage gate once the other
lanes' metas land. A declared gap passes; a silent one fails.

## Render-verify — driven, not asserted

Ran the `_RUNBOOK-render-verify.md` recipe (symlink farm at `/var/tmp/fonts-s203j`, cachedir outside
the repo, `/etc/fonts/fonts.conf` included; browsers reused read-only from `/var/tmp/pw-browsers-s197`;
`goto file://…`, never `set_content`).

- **Font control probe** (40px `Handgloves 12345`), all three pages, identical:
  `HSBC_MtUnivers_Latin` **347** · `"Univers Next HSBC"` **347** · `"Univers Next for HSBC"` **347** ·
  `DejaVu Sans` 375 · nonexistent face 301. Both aliases land on the target and on neither control —
  the real HSBC cut, not a silent fallback.
- **Tree assert:** `ls -a knowledge/assets/fonts/_desktop/TTF/ | grep -c '^\.uuid'` → **0**.
- **Four-theme proof, measured not assumed** — computed `--border-radius-control` in the dark pane of
  each theme: mono **0** · legacy **0** · console **8px** · supercharge **0**; `--error`: mono/supercharge
  `#F6604C`-family, legacy `#A8000B`, console `#B92F1E`; supercharge ink `#F7F6F4` on border `#524842`.
  The themes genuinely flex; a single-theme green would not have shown this.
- **Drove all three by script and read the crops** (not the full pages — `_RUNBOOK-context-gauge.md`
  "price the instrument"): typed `uni` into every Combobox pane (list narrowed to 3, matched run
  underlined, active row took fill **and** inset rule); clicked two options in Multi-select (chips
  appeared in the field, count summary read "1 selected"); committed `INV-4473` then a duplicate
  `INV-4471` in Tags input (chip added, counter moved to "3 of 8 tags", duplicate refused with symbol
  + ink message + red field stroke). Console and Mono crops read by eye, light and dark.

⚠ **A defect I introduced and then caught, by measuring rather than by looking.** The first build of
the review pages emitted a self-referential rebind — `--border-radius-control: var(--border-radius-control)`
— for every var whose name already matches its canon token name. A self-reference is invalid CSS and
resolves to **nothing**, so radius and the 44px `--target-min` were silently dead in all 24 panes and
the pages still *looked* fine. Caught by reading the computed value (`radius: ""`), fixed by omitting
the declaration so canon's own value cascades in, and re-measured (`0/0/8px/0`). The page generator
lived at `/var/tmp/s203j/mkreview.py`, outside the repo; it is not an instrument the repo carries.

⚠ **Stray files I could not remove, declared:** nine render PNGs sit in `_to_delete/s203j-renders/`.
`rm` returns `Operation not permitted` in this sandbox (the known mv-not-rm class) and the directory
is `.gitignore`d (line 25), so they are invisible to git — but they are there, and they are mine.

## Decisions needed — Dave's, every one PROPOSED

1. **Multi-select: which variant is the default?** Chips-in-field keeps every choice visible but the
   field grows; count-summary stays one row tall and moves the chips beneath. Both are built, both are
   on the review page in all four themes. Nothing is ruled.
2. **Tags input: does Backspace take one press or two?** Built as arm-then-remove (first press arms the
   last chip with an inset outline and announces it; second removes). One press is faster and loses
   data silently for fast typists.
3. **Combobox: keep both highlight carriers?** The active row has the hover fill *and* a 3px inset rule.
   In Mono light the rule barely reads against the fill; in Console it is obvious. Keep both, or fill only?
4. **Combobox: no free text, confirmed?** The value must come from the list. A combobox that also accepts
   typed values is a different contract (`aria-autocomplete="both"`) and was fenced out.
5. **Tags input: no suggestions, confirmed?** A suggesting tags input is Tags-input composed with
   Multi-select. Deliberately not built.
6. **The 24px chip dismiss.** Inherited unchanged from gated Tags — the WCAG 2.5.8 minimum, not our 44px
   floor. Raising it changes Tags, a shared artefact. Lane L's hit-area sweep should see it.
7. **Tags input `max` = 8** is illustrative, not a ruled product limit.

## Proposals for the conductor to merge (shared files — I did not touch any of them)

- **`_build_integrity.py` `KNOWN_SC`:** add **3.3.3 Error Suggestion**. It is a real SC, it applies to
  every component that refuses input with an explanation, and its absence currently forces an honest
  meta to under-declare. (`tags-input.meta.json` carries a `$sc-note` recording the removal.)
- **`_DS-IMPROVEMENTS.md`:** there is **no `.t-cm-*` emphasis hook** — the editorial composites have
  `.em` (weight 500) but the component composites have nothing, so a single-line control label cannot be
  emphasised without a raw `font-weight`, which TYPE-002 blocks. It bit three times in this lane
  (matched run, counter approaching the limit, selected option). Workarounds used: underline, and
  changing the wording. A `.t-cm-*-em` rung would close it.
- **`gen_showroom.py` CATEGORIES:** three new entries under Inputs & forms — `combobox`,
  `multi-select`, `tags-input`.
- **`_validate_radius.py` MIGRATED_SNIPPETS:** the three new snippets bind `border-radius/control`
  (and `/surface`) properly and pass strict; add them so the migration list stays honest.
- **`gen_canon_components.py`** must be re-run over the three new snippets to emit `.cn-combobox`,
  `.cn-multi-select`, `.cn-tags-input`. The review pages hand-write that rebind as a preview and say so
  on the page; they can be regenerated unchanged afterwards.
- **The itinerary rows 21/22/23** move Gap → Built (Lane H's derivation should pick them up from the
  store, not from a hand edit).

## Friction log

- The addendum's alternate-slug hardening earned its keep on row 22: the *meta* claimed a multi-select
  variant that the *snippet* never implemented. A meta is a claim; the snippet is the artefact
  [[premise-ages-faster-than-rule]].
- The Progress-bar zero-raw-type precedent is the one to copy for any new snippet — the ratchet is
  shrink-only, and it costs nothing to start at 0 rather than paying debt down later.
- The a11y and state-contrast gates both wrote their audit files as a side effect of a filtered run.
  Declared, per the addendum.
