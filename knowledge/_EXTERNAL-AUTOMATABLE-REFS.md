# External automatable-check refs (axe-core import)

> Off-the-shelf automatable checks that EXIST for each SC in our compliance graph, imported from axe-core v4.12.1 (2026-07-14) — see `compliance/_vendor/_INGEST-NOTES.md` for provenance. Advisory, does not gate the build. This is NOT the same as `verified_by`: it says tooling is *available*, not that *we* run it.

**15/31 of our SCs have at least one axe-core rule tagged against them.** 16 have no OSS axe-core coverage at all — genuinely manual/bespoke territory for now.

## Easy wins — axe-core covers it, we haven't wired it up (13)

| SC | axe-core rule(s) |
|---|---|
| 1.1.1 | `aria-meter-name`, `aria-progressbar-name`, `image-alt`, `input-image-alt`, `object-alt`, `role-img-alt`, `svg-img-alt` |
| 1.2.2 | `video-caption` |
| 1.3.1 | `aria-hidden-body`, `aria-required-children`, `aria-required-parent`, `definition-list`, `dlitem`, `list`, `listitem`, `p-as-heading`, `table-fake-caption`, `td-has-header`, `td-headers-attr`, `th-has-data-cells` |
| 1.3.5 | `autocomplete-valid` |
| 1.4.1 | `link-in-text-block` |
| 1.4.4 | `meta-viewport` |
| 2.1.1 | `frame-focusable-content`, `scrollable-region-focusable`, `server-side-image-map` |
| 2.2.1 | `meta-refresh` |
| 2.2.2 | `blink`, `marquee` |
| 2.4.1 | `bypass` |
| 2.4.4 | `area-alt`, `link-name` |
| 3.3.2 | `form-field-multiple-labels` |
| 4.1.2 | `area-alt`, `aria-allowed-attr`, `aria-braille-equivalent`, `aria-command-name`, `aria-conditional-attr`, `aria-deprecated-role`, `aria-hidden-body`, `aria-hidden-focus`, `aria-input-field-name`, `aria-prohibited-attr`, `aria-required-attr`, `aria-roledescription`, `aria-roles`, `aria-tab-name`, `aria-toggle-field-name`, `aria-tooltip-name`, `aria-valid-attr-value`, `aria-valid-attr`, `button-name`, `duplicate-id-aria`, `frame-title-unique`, `frame-title`, `input-button-name`, `input-image-alt`, `label`, `link-name`, `nested-interactive`, `select-name`, `summary-name` |

## Already wired (verified_by set independently of this import) (2)

| SC | axe-core rule(s) |
|---|---|
| 1.4.3 | `color-contrast` |
| 2.5.8 | `target-size` |

## No OSS axe-core coverage found (16)

| SC |
|---|
| 1.2.5 |
| 1.3.2 |
| 1.4.10 |
| 1.4.11 |
| 1.4.13 |
| 2.1.2 |
| 2.3.3 |
| 2.4.11 |
| 2.4.3 |
| 2.4.5 |
| 2.4.6 |
| 2.4.7 |
| 2.4.8 |
| 2.5.7 |
| 3.3.1 |
| 4.1.3 |

## W3C ACT Rules Format

Checked 2026-07-14, **not ingested this pass** — no structured export found without scraping ~500 individual rule pages. See `compliance/_vendor/_INGEST-NOTES.md` for what was checked and the deferred approach.

