# #271 HARVEST — LANE C RECEIPT

**Slice C — page-frame + page-title + wayfinding + arrangement.** 2026-09-14, session 271.
**READ-ONLY on canon.** Nothing under `knowledge/` was written, read-modified or regenerated. All output is under `notes/_lanes/271/harvest/C/`.

---

## Counts

| Measure | Count |
| --- | --- |
| Components in the brief's slice-C list | 43 named (`template-*` given as 13) |
| Components that actually exist as metas | **42** (`template-*` is **12**, not 13 — see gaps) |
| Components covered by a proposal | **42 / 42 — full coverage, none skipped** |
| `when` proposals written (`PROPOSED-WHEN.json`) | **42** |
| Our own sources recorded (`SOURCES.json.ours`) | **27** |
| External verbatim quotes recorded (`SOURCES.json.external`) | **108** |
| Distinct discriminator rules those quotes touch | **68** |
| **Components** whose proposal is unanimous — the review page's test: `disagreements` opens with the word *none* | **4 of 42** |
| **Rules** where systems speak and disagree (`DECISION-TABLE.json`) | **15 rows**, naming 27 distinct components and touching 25 of the 42 proposals |
| **Components** with **no** external rule found at all | **17 of 42** (`confidence: "none"`); 17 proposals also cite no external system in `sources` |
| Components whose `when` is already adopted canon | **4** (`confidence: "canon"`) |
| Longest quote | 14 words (cap is < 15) |

**These three rows are on two different axes and must not be added up.** The first version of this receipt printed 4 + 15 + 17 = 36 against 42 proposals, which reads as a partition and is not one: rows are per-RULE and proposals are per-COMPONENT, and the sets overlap (only `tab-bar` and `divider` fall outside all three). Corrected 2026-09-14. Recount with `python3 notes/_lanes/271/harvest/_recount.py C`.

### Confidence split across the 42 proposals
- `canon` — 4 · `consensus-external` — 11 · `single-external` — 10 · `none` — 17

### The 4 unanimous rules (no decision row needed — ratify as written)
`app-shell-focused` · `template-wizard` · `template-confirmation` · `template-error` (scope half only; its language/furniture half is contested → R16).

---

## Systems consulted

| System | Quotes harvested | Note |
| --- | --- | --- |
| USWDS | 29 | richest source in this slice; every component page carries a when-to-use / when-to-consider-something-else block |
| GOV.UK Design System | 25 | patterns as well as components — the template family's only external support |
| Carbon (IBM) | 11 | the only system with an explicit side-nav item count |
| Apple HIG | 10 | fetched via the HIG JSON endpoint; the rendered pages are JS-gated |
| Polaris (Shopify) | 10 | recovered from the system's own source markdown in `Shopify/polaris` on GitHub |
| NN/g | 9 | the only source with a back-to-top threshold |
| Material 3 | 7 | **meta descriptions only** — see fetch failures |
| Ant Design | 7 | server-rendered, clean |
| **Spectrum (Adobe)** | **0** | fetch failure — silent in every row |
| **Atlassian** | **0** | fetch failure — silent in every row |
| **Fluent 2 (Microsoft)** | **0** | fetch failure — silent in every row |

---

## Fetch failures — named, never guessed

Recorded in full under `SOURCES.json.refused` (7 systems, 22 URLs).

1. **Spectrum (Adobe)** — `tabs`, `breadcrumbs`, `side-navigation`, `divider`. HTTP 200, body client-rendered, no guidance text served. **Zero quotes. Spectrum's "silent" in the decision table is a fetch failure, not a position.**
2. **Atlassian** — `breadcrumbs`, `tabs`, `pagination`, `side-navigation` usage pages. Same: 200, client-rendered shell only. **Zero quotes.**
3. **Fluent 2 (Microsoft)** — `nav`, `tablist`, `breadcrumb` usage pages. Same. **Zero quotes.**
4. **Material 3 — PARTIAL.** Every `/guidelines` body returns `This website requires JavaScript.` Only the served `<meta name="description">` is readable, and **every M3 quote in `SOURCES.json` is flagged as such.** Consequence: M3's fuller rules — in particular the navigation-bar 3–5 destination rule that would have corroborated our `tab-bar` number — **could not be verified and are NOT recorded.**
5. **Polaris (Shopify)** — `polaris.shopify.com/components/...` now 301s to `shopify.dev/docs/api/polaris` and serves no guidance. Recovered from the system's **own** source `.mdx` in `Shopify/polaris` on GitHub; those raw URLs are cited on each quote.
6. **USWDS templates** — `authentication-pages` and `form-templates` fetch 200 but carry **no** when-to-use block. Consequence: `template-auth` and `template-create-edit` have **no external rule**.
7. **Carbon** — `patterns/global-header/` fetched 200, no when-to-use block extracted.

---

## Declared gaps

- **`template-*` is 12, not 13.** The brief says 13. On disk: `auth, confirmation, create-edit, dashboard-bento, dashboard, detail, empty, error, list-index, report, settings, wizard` = 12. No thirteenth template meta exists. Nothing was invented to fill the count.
- **`headers` is listed twice in the brief's slice-C line** (once under page-frame, once at the end of arrangement). Covered once.
- **The whole template family is unsourced by construction.** No public system ships page templates at our granularity — USWDS ships five (404, landing, documentation, authentication, form) and **none** maps onto a template of ours. That is a finding, not a coverage failure: 9 of the 12 templates carry `confidence: "none"` for that reason and it is stated on each.
- **`account-selector`** is listed in slice C but is an **input**-role component; its real siblings (`dropdown`, `combobox`) belong to slice A. Covered, flagged, zero external sources — no public system ships an account picker.
- **`image-block`, `video-player`, `card-header-lockup`, `hero-variants`** are **not role providers in `roles.json`** — they have no adopted `when` to extend. Their proposals are therefore speculative and say so.
- **Cross-slice overlap, not duplicated:** `pagination`, `accordion`, `carousel` and `cards` appear in the `wayfinding` / `arrangement` roles but are **slice B's components**. Quotes bearing on the *tabs* side of the tabs-vs-accordion cut are recorded here; no proposal was written for any of the four.
- **`s270-D1`** (single-select cut-off 5) touches no slice-C component. Cited as canon in `PROPOSED-WHEN.json`, not re-litigated. Slice B's `record-list` whens likewise referenced, not redone.
- **Not attempted for budget:** W3C ARIA APG, Base Web, Primer, Lightning, Salesforce. Coverage was spent on the eleven systems the brief names.

---

## Files

- `notes/_lanes/271/harvest/C/SOURCES.json`
- `notes/_lanes/271/harvest/C/PROPOSED-WHEN.json`
- `notes/_lanes/271/harvest/C/DECISION-TABLE.json`
- `notes/_lanes/271/harvest/C/RECEIPT.md`

## Recount — 2026-09-14

Every number above re-derived from this slice's three JSONs by script, so the receipt states what the JSONs carry and not what the lane remembered.

```
$ python3 notes/_lanes/271/harvest/_recount.py C
SLICE C
  SOURCES     ours 27 · external 108 · refused 7
  quotes      longest 14 words · at-or-over the <15 cap: 0
  proposals   42
  confidence  canon 4 · consensus-external 11 · single-external 10 · none 17
  unanimous   4  (page test: `disagreements` opens with "none") -> app-shell-focused, template-wizard, template-confirmation, template-error
  expected silence recorded in `disagreements`: 0 -> 
  decision rows 15 · distinct components named by a row 27 · proposals a row touches 25
  rows flagged kind=internal: 0 -> 
  system-disagreement rows: 15
  proposals citing NO external system in `sources`: 17
  component values that are not an existing meta stem: 0
  external findings with component: null: 2
```
