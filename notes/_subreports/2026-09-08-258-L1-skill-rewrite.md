# #258 lane 1 — ENACTING s258-D1 AND s258-D2: the skill rewrite and the gate relaxation

**Model: Opus 5. Rulings enacted: `s258-D1` (rule 2a removed — the author may write JavaScript)
and `s258-D2` (builds are ambitious by default; mock data rich and deep; code is an avenue to
innovation). Read-only against snippets, metas and canon. Nothing of Dave's ruled.**

Dave's words, from `_rulings.json`:

> **s258-D1** — *"definitely remove 2a I'd like to see not only the wiring work it might deliver
> some code creativity."*
>
> **s258-D2** — *"I also want the builds to be more ambitious by default, assume that everything
> on the page should work, the mock data generated should be super-rich and deep so that enables
> more behaviors and interactions … writing code might be an avenue to innovation, the interface
> is pretty tied down."*

## What changed

**`apollo-spider/skills/generate-from-canon/SKILL.md`** — 199 → 236 lines, +47/−10.
Frontmatter `name: ADS-generate-from-canon` untouched; the four-file table, the Gaps list, the
theme rules, 7a/7b and the gates step are all unchanged.

- **:12–16** the "strict mode, not a creativity play" paragraph replaced with *strict about the
  interface, ambitious about the build* (`s258-D2`) — tokens and classes are the boundary, the
  JavaScript is not.
- **:50–61** rule **2a REPLACED**. Old text: *"Copy the script address with the markup; author no
  JS … Never write a handler yourself, never paraphrase the script."* New text: the author writes
  the JavaScript; a snippet's script is copied verbatim **where it fits**, and may be extended;
  the declared address still goes into the receipt and the `#behaviour-manifest`, but it now names
  the source you started from, not a promise you left it untouched.
- **:154–161** rule **13 — a DATA MODEL comes first.** One in-page `DATA` dataset before any
  markup; every KPI, chart, grid, filter option and drawer reads from it; no number typed twice;
  named entities with ids and relationships, real currencies, a time series, enough rows for
  paging and sorting to mean something; KPIs derived, never hard-coded.
- **:162–167** rule **14 — every control does something visible.** Filters re-drive grid **and**
  KPIs **and** charts (a chart that does not move is a defect, naming cold-run finding 3); nav
  switches the view; sort sorts; drawers open; a CTA that opens nothing is a Gap. Cross-component
  wiring is explicitly the author's to write.
- **:168–170** rule **15 — state survives a reload.** Filters, nav/view, sort, page size, theme
  via URL params (preferred) or `localStorage`, read back on load.
- **:171–172** rule **16 — zero uncaught JS errors on load**, console read before the claim.
- **:173–174** rule **17 — every page shell carries a footer** (lane 2's shell work).
- **:192–195** procedure step **2a "Model the data"**, before Compose.
- **:220–222** procedure step **6 "Drive it"** — console, every control, one reload.
- **:229–233** Output now asks for a **behaviour manifest** (per control: what it drives, where its
  state persists) and, where a snippet script was the starting point, whether it was carried
  verbatim or **extended** — extending is reported, not hidden.

**`knowledge/_validate_receipt.py`** — 983 → 1,011 lines, +46/−18, every change carrying a
`# s258-D1` comment (12 sites).

- **:101–105** the WHAT-IT-CHECKS docstring records the removal and what stays red.
- **:452–481 `address_loaded`** — the near-copy detection that used to be only a *hint* now
  becomes a **state**. A page script that is whitespace-shifted from, or shares ≥80% of its bytes
  with, the declared script returns `"NOTE"` instead of `False`. A declared address the page
  carries **no trace of** still returns `False`.
- **:542–546 `behaviour_verdict`** — `"NOTE"` renders as
  `· behaviour <addr> LOADED-EXTENDED (…) · NOTE:AUTHORED-JS`, green.
- **:556–562** `FAIL:BEHAVIOUR-PARTIAL-UNREGISTERED` → `NOTE:BEHAVIOUR-PARTIAL-UNREGISTERED`; the
  name is dropped from `fails`, so it no longer reds a run.
- **:714** `check()` now merges behaviour lines even when there are no fails — otherwise a NOTE on
  a green page was silently discarded.
- **:769** `--quiet` prints `NOTE:` lines as well as `FAIL:` ones.
- **Selftest, :890–966** — arms **M** (one-byte edited copy) and **N** (whitespace-shifted copy)
  flip from `BEHAVIOUR-NOT-LOADED` to `PASS`; **U** and **U2** (unregistered partial) flip to
  `PASS`. Three arms added/kept to fence the relaxation so it cannot be quoted wider than it is:
  **L** (page carries no script → still red), new **N3** (page carries an *unrelated* script only
  → still `BEHAVIOUR-NOT-LOADED`), new **U3** (a registered partial's block missing beside a noted
  ghost → still red).

**`apollo-spider/skills/grill-me/SKILL.md`** — +8 lines, by ADDITION only, nothing above
re-worded: a `s258-D1 / s258-D2` block under "Handing it on" saying the build is ambitious by
default, that question 5 (data) is now load-bearing, and that a skipped answer never licenses a
dead control.

## Gate exit codes, before and after

| run | before | after |
|---|---|---|
| `python3 knowledge/_validate_receipt.py --selftest` | `SELFTEST: PASS ✅`, **exit 0** (38 arms) | `SELFTEST: PASS ✅`, **exit 0** (41 arms) |
| `python3 knowledge/_validate_receipt.py outputs/coldrun-258/arm-A-blind/dashboard.html` | `FAIL:NO-RECEIPT`, **exit 1** | `FAIL:NO-RECEIPT`, **exit 1** |

⚠ **The cold-run page proves nothing about this change.** It carries no
`<script type="application/json" id="provenance-receipt">` at all, so step 0 refuses before any
behaviour arm runs — identical output before and after, to the byte. The relaxation is proven by
the selftest arms (M, N, U, U2 flipping; L, N3, U3 holding), which drive `check()` on real
temporary files, not on a helper.

## What was NOT done

- **No snippet, meta, canon or showroom file touched.** `App-shell-*.reference.html`,
  `Template-dashboard-bento.reference.html` and the data-grid / filter-toolbar-bar / sidebar-nav
  metas belong to other lanes this session and were not opened for edit.
- **The footer itself is lane 2's.** Rule 17 states the requirement; no shell snippet was given a
  footer here, so a build following rule 17 today has nothing to copy until lane 2 lands.
- **`gen_provenance_receipt.py` not touched.** It imports the shared primitives, and none of them
  changed — but whether the minted receipt should record "extended" rather than just the address
  is a schema question, not a relaxation, and is left open.
- **The `/goal` skill is PARKED** by `s258-D2`'s own words; not started.
- **Cold-run finding 1 not addressed** — rule 7a's mandated bento template still fails the gate
  rule 5 mandates (146 hex, 4 redefined canon classes). That is a snippet defect, another lane's
  file, and it is untouched here.
- **No `_build_all.py`, no commit, no push, no `git checkout`/`stash`.** The pack zip is
  unchanged, so v1.0.7 does not yet carry any of this.
- **No rulings inscribed**; nothing of Dave's decided.

## Tokens

≈100K cumulative on the harness counter at report time.

## Paths

- `apollo-spider/skills/generate-from-canon/SKILL.md` · `apollo-spider/skills/grill-me/SKILL.md`
- `knowledge/_validate_receipt.py`
- `notes/_subreports/2026-09-08-258-L1-skill-rewrite.md`
