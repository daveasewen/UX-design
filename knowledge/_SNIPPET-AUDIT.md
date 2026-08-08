# Snippet gate — reference implementations vs canon

## Accordion.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Account-card.reference.html — ❌ 8 FAIL
- ❌ Account-card.reference.html: DRIFT --ok (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Account-card.reference.html: DRIFT --ok (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Account-card.reference.html: DRIFT --ok-tint (light) = #DCEDE3 but rag/success-tint = #D4F1DF
- ❌ Account-card.reference.html: DRIFT --ok-tint (dark) = #12291D but rag/success-tint = #32533F
- ❌ Account-card.reference.html: DRIFT --warn (light) = #C58900 but rag/warning = #E0A61F
- ❌ Account-card.reference.html: DRIFT --warn (dark) = #C58900 but rag/warning = #E0A61F
- ❌ Account-card.reference.html: DRIFT --warn-tint (light) = #F6E5CC but rag/warning-tint = #F6E6C0
- ❌ Account-card.reference.html: DRIFT --warn-tint (dark) = #3C2C13 but rag/warning-tint = #614C1C

## Account-selector.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Action-bar.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Alert.reference.html — ❌ 19 FAIL
- ❌ Alert.reference.html: DRIFT --err (light) = #B92F1E but rag/error = #F6604C
- ❌ Alert.reference.html: DRIFT --err (dark) = #CC4333 but rag/error = #F6604C
- ❌ Alert.reference.html: DRIFT --warn (light) = #C58900 but rag/warning = #E0A61F
- ❌ Alert.reference.html: DRIFT --warn (dark) = #C58900 but rag/warning = #E0A61F
- ❌ Alert.reference.html: DRIFT --ok (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Alert.reference.html: DRIFT --ok (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Alert.reference.html: DRIFT --info (light) = #306EC6 but rag/information = #78A7E8
- ❌ Alert.reference.html: DRIFT --info (dark) = #2674DC but rag/information = #78A7E8
- ❌ Alert.reference.html: DRIFT --err-t (light) = #F1E0DC but rag/error-tint = #FDD9D4
- ❌ Alert.reference.html: DRIFT --err-t (dark) = #2C120D but rag/error-tint = #60302A
- ❌ Alert.reference.html: DRIFT --warn-t (light) = #F6E5CC but rag/warning-tint = #F6E6C0
- ❌ Alert.reference.html: DRIFT --warn-t (dark) = #3C2C13 but rag/warning-tint = #614C1C
- ❌ Alert.reference.html: DRIFT --ok-t (light) = #DCEDE3 but rag/success-tint = #D4F1DF
- ❌ Alert.reference.html: DRIFT --ok-t (dark) = #12291D but rag/success-tint = #32533F
- ❌ Alert.reference.html: DRIFT --info-t (light) = #D6E3EC but rag/information-tint = #DFEAF9
- ❌ Alert.reference.html: DRIFT --info-t (dark) = #092131 but rag/information-tint = #38475C
- ❌ Alert.reference.html: CONTRAST rag/error on rag/error-tint (light) = 2.4:1 < 3.0:1
- ❌ Alert.reference.html: CONTRAST rag/success on rag/success-tint (light) = 1.65:1 < 3.0:1
- ❌ Alert.reference.html: CONTRAST rag/information on rag/information-tint (light) = 2.03:1 < 3.0:1

## Amount-display.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Amount-input.reference.html — ❌ 5 FAIL
- ❌ Amount-input.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Amount-input.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ Amount-input.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Amount-input.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Amount-input.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1

## Avatar.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Badge.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Banner.reference.html — ❌ 12 FAIL
- ❌ Banner.reference.html: DRIFT --err-bg (light) = #B92F1E but rag/error-background = #F6604C
- ❌ Banner.reference.html: DRIFT --err-bg (dark) = #B92F1E but rag/error-background = #F6604C
- ❌ Banner.reference.html: DRIFT --warn-bg (light) = #F0B13A but rag/warning-background = #E0A61F
- ❌ Banner.reference.html: DRIFT --warn-bg (dark) = #F0B13A but rag/warning-background = #E0A61F
- ❌ Banner.reference.html: DRIFT --ok-bg (light) = #5DAC7B but rag/success-background = #66CC8D
- ❌ Banner.reference.html: DRIFT --ok-bg (dark) = #43AD6F but rag/success-background = #66CC8D
- ❌ Banner.reference.html: DRIFT --info-bg (light) = #7DABCD but rag/information-background = #78A7E8
- ❌ Banner.reference.html: DRIFT --info-bg (dark) = #5F92B9 but rag/information-background = #78A7E8
- ❌ Banner.reference.html: CONTRAST rag/text/on-dark on rag/error-background (light) = 3.14:1 < 4.5:1
- ❌ Banner.reference.html: CONTRAST rag/text/on-dark on rag/error-background (dark) = 3.14:1 < 4.5:1
- ❌ Banner.reference.html: CONTRAST rag/text/on-dark on rag/error-background (light) = 3.14:1 < 4.5:1 (icon-015, promoted 2026-07-02)
- ❌ Banner.reference.html: CONTRAST rag/text/on-dark on rag/error-background (dark) = 3.14:1 < 4.5:1 (icon-015, promoted 2026-07-02)

## Breadcrumbs.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Button.reference.html — ❌ 2 FAIL
- ❌ Button.reference.html: DRIFT --success (light) = #5DAC7B but rag/success-background = #66CC8D
- ❌ Button.reference.html: DRIFT --success (dark) = #43AD6F but rag/success-background = #66CC8D

## Cards.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-bar.reference.html — ❌ 11 FAIL
- ❌ Chart-bar.reference.html: DRIFT --status-breach (light) = #B92F1E but rag/error = #F6604C
- ❌ Chart-bar.reference.html: DRIFT --status-breach (dark) = #CC4333 but rag/error = #F6604C
- ❌ Chart-bar.reference.html: DRIFT --status-watch (light) = #C58900 but rag/warning = #E0A61F
- ❌ Chart-bar.reference.html: DRIFT --status-watch (dark) = #C58900 but rag/warning = #E0A61F
- ❌ Chart-bar.reference.html: DRIFT --status-healthy (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Chart-bar.reference.html: DRIFT --status-healthy (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Chart-bar.reference.html: DRIFT --status-info (light) = #306EC6 but rag/information = #78A7E8
- ❌ Chart-bar.reference.html: DRIFT --status-info (dark) = #2674DC but rag/information = #78A7E8
- ❌ Chart-bar.reference.html: CONTRAST rag/warning on background/default (light) = 2.18:1 < 3.0:1
- ❌ Chart-bar.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1
- ❌ Chart-bar.reference.html: CONTRAST rag/information on background/default (light) = 2.47:1 < 3.0:1

## Chart-boxplot.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-bullet.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-butterfly-h.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-butterfly-v.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-candlestick.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-combo.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-donut.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-histogram.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-line.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-pie.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-scatter.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-sparkline.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Chart-stacked-area.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Confirmation.reference.html — ❌ 2 FAIL
- ❌ Confirmation.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Confirmation.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1
- 🟡 Confirmation.reference.html: ALLOWED drift --success (dark) = #FFFFFF (token rag/success = #66CC8D) — RAG ROUNDEL POLICY (Dave 2026-07-02 eve): dark roundels are WHITE with a BLACK mark — icon shape + label carry meaning. The glyph's tick is a page-cutout, so white shape + black page = 21:1 (rag/success #00847F with a black cutout was 2.77, failing the >=4.5 mark leg). Light keeps rag/success.

## Countdown-timer.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Data-grid.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Date-picker.reference.html — ❌ 4 FAIL
- ❌ Date-picker.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Date-picker.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ Date-picker.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Date-picker.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D

## Date-range-picker.reference.html — ❌ 2 FAIL
- ❌ Date-range-picker.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Date-range-picker.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C

## Divider.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Drawer.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Dropdown.reference.html — ❌ 2 FAIL
- ❌ Dropdown.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Dropdown.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C

## Empty-state.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Eyebrow.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## File-upload.reference.html — ❌ 5 FAIL
- ❌ File-upload.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ File-upload.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ File-upload.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ File-upload.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ File-upload.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1

## Form-layout.reference.html — ❌ 8 FAIL
- ❌ Form-layout.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Form-layout.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ Form-layout.reference.html: DRIFT --error-tint (light) = #F1E0DC but rag/error-tint = #FDD9D4
- ❌ Form-layout.reference.html: DRIFT --error-tint (dark) = #2C120D but rag/error-tint = #60302A
- ❌ Form-layout.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Form-layout.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Form-layout.reference.html: CONTRAST rag/error on rag/error-tint (light) = 2.4:1 < 3.0:1
- ❌ Form-layout.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1

## Headers.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Hero.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Icon-button.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Input-fields.reference.html — ❌ 5 FAIL
- ❌ Input-fields.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Input-fields.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ Input-fields.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Input-fields.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Input-fields.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1

## Links.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## List-items.reference.html — ❌ 19 FAIL
- ❌ List-items.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ List-items.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ List-items.reference.html: DRIFT --warning (light) = #C58900 but rag/warning = #E0A61F
- ❌ List-items.reference.html: DRIFT --warning (dark) = #C58900 but rag/warning = #E0A61F
- ❌ List-items.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ List-items.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ List-items.reference.html: DRIFT --info (light) = #306EC6 but rag/information = #78A7E8
- ❌ List-items.reference.html: DRIFT --info (dark) = #2674DC but rag/information = #78A7E8
- ❌ List-items.reference.html: DRIFT --success-tint (light) = #DCEDE3 but rag/success-tint = #D4F1DF
- ❌ List-items.reference.html: DRIFT --success-tint (dark) = #12291D but rag/success-tint = #32533F
- ❌ List-items.reference.html: DRIFT --warning-tint (light) = #F6E5CC but rag/warning-tint = #F6E6C0
- ❌ List-items.reference.html: DRIFT --warning-tint (dark) = #3C2C13 but rag/warning-tint = #614C1C
- ❌ List-items.reference.html: DRIFT --error-tint (light) = #F1E0DC but rag/error-tint = #FDD9D4
- ❌ List-items.reference.html: DRIFT --error-tint (dark) = #2C120D but rag/error-tint = #60302A
- ❌ List-items.reference.html: DRIFT --info-tint (light) = #D6E3EC but rag/information-tint = #DFEAF9
- ❌ List-items.reference.html: DRIFT --info-tint (dark) = #092131 but rag/information-tint = #38475C
- ❌ List-items.reference.html: CONTRAST rag/success on rag/success-tint (light) = 1.65:1 < 3.0:1
- ❌ List-items.reference.html: CONTRAST rag/error on rag/error-tint (light) = 2.4:1 < 3.0:1
- ❌ List-items.reference.html: CONTRAST rag/information on rag/information-tint (light) = 2.03:1 < 3.0:1

## Loading-indicator.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Modal-lightbox.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Modals.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Navigations.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Notifications.reference.html — ❌ 4 FAIL
- ❌ Notifications.reference.html: DRIFT --ok (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Notifications.reference.html: DRIFT --ok (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Notifications.reference.html: DRIFT --ok-t (light) = #DCEDE3 but rag/success-tint = #D4F1DF
- ❌ Notifications.reference.html: DRIFT --ok-t (dark) = #12291D but rag/success-tint = #32533F
- 🟡 Notifications.reference.html: ALLOWED drift --err (light) = #A8000B (token rag/error = #F6604C) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --err (dark) = #A8000B (token rag/error = #F6604C) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --warn (light) = #FFBB33 (token rag/warning = #E0A61F) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --warn (dark) = #FFBB33 (token rag/warning = #E0A61F) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --info (light) = #305A85 (token rag/information = #78A7E8) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --info (dark) = #305A85 (token rag/information = #78A7E8) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --err-t (light) = #F9F2F3 (token rag/error-tint = #FDD9D4) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --err-t (dark) = #260005 (token rag/error-tint = #60302A) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --warn-t (light) = #FFF8EA (token rag/warning-tint = #F6E6C0) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --warn-t (dark) = #221701 (token rag/warning-tint = #614C1C) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --info-t (light) = #EBEFF4 (token rag/information-tint = #DFEAF9) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)
- 🟡 Notifications.reference.html: ALLOWED drift --info-t (dark) = #000D1B (token rag/information-tint = #38475C) — LEGACY REFERENCE (R-D19 / _STYLE-PROVENANCE §A-AUTH): Notifications is kept as an Apollo LEGACY reference — no active Mono notification canon exists yet. Its RAG values are legitimate Legacy hexes (error #A8000B/#DB0011, amber #FFBB33, navy #305A85/#4587A7 + their Legacy tints), NOT drift from the Mono roles they nominally bind. R-D20 rebased those bare roles onto Mono, so every RAG var now reads as drift here; waived because the ruling is 'do not convert — retag to the Legacy theme' (a future build). (Prior note retained: global solid banners kept the deeper light accents in dark for white-text contrast; blue/400 dangling-alias fixed; remaining gap = no dedicated dark rag-SURFACE token — see dark-rag-token-gaps.)

## Pagination.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Popover.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Progress-tracker.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Quick-actions.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Reorder.reference.html — ❌ 3 FAIL
- ❌ Reorder.reference.html: DRIFT --drop (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Reorder.reference.html: DRIFT --drop (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Reorder.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1

## Search-field.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Secure-entry.reference.html — ❌ 5 FAIL
- ❌ Secure-entry.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Secure-entry.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ Secure-entry.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Secure-entry.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Secure-entry.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1

## Segmented-control.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Selection-controls.reference.html — ❌ 2 FAIL
- ❌ Selection-controls.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Selection-controls.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C

## Skeleton-loader.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Slider.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Stat-card.reference.html — ❌ 5 FAIL
- ❌ Stat-card.reference.html: DRIFT --up (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Stat-card.reference.html: DRIFT --up (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Stat-card.reference.html: DRIFT --down (light) = #B92F1E but rag/error = #F6604C
- ❌ Stat-card.reference.html: DRIFT --down (dark) = #CC4333 but rag/error = #F6604C
- ❌ Stat-card.reference.html: CONTRAST rag/success on tertiary/background/default (light) = 1.98:1 < 3.0:1

## Status-indicator.reference.html — ❌ 18 FAIL
- ❌ Status-indicator.reference.html: DRIFT --success (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Status-indicator.reference.html: DRIFT --success (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Status-indicator.reference.html: DRIFT --warning (light) = #C58900 but rag/warning = #E0A61F
- ❌ Status-indicator.reference.html: DRIFT --warning (dark) = #C58900 but rag/warning = #E0A61F
- ❌ Status-indicator.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Status-indicator.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C
- ❌ Status-indicator.reference.html: DRIFT --info (light) = #306EC6 but rag/information = #78A7E8
- ❌ Status-indicator.reference.html: DRIFT --info (dark) = #2674DC but rag/information = #78A7E8
- ❌ Status-indicator.reference.html: DRIFT --success-tint (light) = #DCEDE3 but rag/success-tint = #D4F1DF
- ❌ Status-indicator.reference.html: DRIFT --success-tint (dark) = #12291D but rag/success-tint = #32533F
- ❌ Status-indicator.reference.html: DRIFT --warning-tint (light) = #F6E5CC but rag/warning-tint = #F6E6C0
- ❌ Status-indicator.reference.html: DRIFT --warning-tint (dark) = #3C2C13 but rag/warning-tint = #614C1C
- ❌ Status-indicator.reference.html: DRIFT --error-tint (light) = #F1E0DC but rag/error-tint = #FDD9D4
- ❌ Status-indicator.reference.html: DRIFT --error-tint (dark) = #2C120D but rag/error-tint = #60302A
- ❌ Status-indicator.reference.html: DRIFT --info-tint (light) = #D6E3EC but rag/information-tint = #DFEAF9
- ❌ Status-indicator.reference.html: DRIFT --info-tint (dark) = #092131 but rag/information-tint = #38475C
- ❌ Status-indicator.reference.html: CONTRAST rag/success on background/default (light) = 1.98:1 < 3.0:1
- ❌ Status-indicator.reference.html: CONTRAST rag/information on background/default (light) = 2.47:1 < 3.0:1

## Stepper.reference.html — ❌ 2 FAIL
- ❌ Stepper.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Stepper.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C

## Summary.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Tab-bar.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Table.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Tabs.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Tags.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Textarea.reference.html — ❌ 2 FAIL
- ❌ Textarea.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Textarea.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C

## Time-picker.reference.html — ❌ 2 FAIL
- ❌ Time-picker.reference.html: DRIFT --error (light) = #B92F1E but rag/error = #F6604C
- ❌ Time-picker.reference.html: DRIFT --error (dark) = #CC4333 but rag/error = #F6604C

## Toast.reference.html — ❌ 9 FAIL
- ❌ Toast.reference.html: DRIFT --warn (light) = #C58900 but rag/warning = #E0A61F
- ❌ Toast.reference.html: DRIFT --warn (dark) = #C58900 but rag/warning = #E0A61F
- ❌ Toast.reference.html: DRIFT --ok (light) = #2B7E4F but rag/success = #66CC8D
- ❌ Toast.reference.html: DRIFT --ok (dark) = #4A9568 but rag/success = #66CC8D
- ❌ Toast.reference.html: DRIFT --info (light) = #306EC6 but rag/information = #78A7E8
- ❌ Toast.reference.html: DRIFT --info (dark) = #2674DC but rag/information = #78A7E8
- ❌ Toast.reference.html: CONTRAST rag/warning on tertiary/background/default (light) = 2.18:1 < 3.0:1
- ❌ Toast.reference.html: CONTRAST rag/success on tertiary/background/default (light) = 1.98:1 < 3.0:1
- ❌ Toast.reference.html: CONTRAST rag/information on tertiary/background/default (light) = 2.47:1 < 3.0:1

## Tooltip.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## Video-player.reference.html — ✅ PASS
- 🟡 Video-player.reference.html: ALLOWED drift --accent-label (light) = #333333 (token button/primary/label/default = #FFFFFF) — ON-SCRIM EXCEPTION (Dave 2026-07-21): the bigplay glyph sits on --onvideo-fill (text/reverse — LIGHT in both modes), so the dark-mode label value #333333 applies in BOTH modes; the light-mode ladder value #FFFFFF would be white-on-white. Pending Dave's eyeball per _REVIEW-SIGNOFF.
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.

## View-options.reference.html — ✅ PASS
- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.
