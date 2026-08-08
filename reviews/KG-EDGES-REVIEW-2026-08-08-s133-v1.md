# KG Edges Review — Dave's-Eye Pass (2026-08-08, s133)

Mechanical KG migration is done and green. This is the leftover list needing a ruling. Nothing written to any meta/registry/gate/ruling file.

## Counts

- Near-miss nodes: 35
- ref:null prose edges: 98 (mustNotNeighbour 40, triggeredBy 22, hasPart 19, partial 5, family 12)
- governedBy candidates (proposed, unwritten): 47
- Token-claim samples: 5 (proposal only)
- Enacted this session: schema v2, 653 typed edges resolved, 98 prose edges declared ref:null+$note, 214 pattern + 139 context nodes, parse-gate green, index 642 -> 1073

Full detail (grouped prose edges, governedBy quotes, token-claim samples, proposed grammar) is in the HTML twin: reviews/KG-EDGES-REVIEW-2026-08-08-s133-v1.html

## Near-miss table

| node id | kind | candidate component (match type) | sources | action (yours) |
|---|---|---|---|---|
| `pattern:app-bottom-tab-bar` | pattern | tab-bar (embedded) | navigations | |
| `pattern:button-processing-state` | pattern | button (prefix) | loading-indicator | |
| `pattern:card-grid` | pattern | cards (prefix) | cards | |
| `pattern:card-pin-confirmation` | pattern | cards (prefix) | secure-entry | |
| `pattern:card-title-kicker` | pattern | cards (prefix) | eyebrow | |
| `pattern:clipboard-confirmation` | pattern | confirmation (suffix) | toast | |
| `pattern:hero-feature-video` | pattern | hero (prefix) | video-player | |
| `pattern:notification-dot-on-an-icon-button` | pattern | icon-button (embedded) | badge | |
| `pattern:payment-time-with-date-picker` | pattern | date-picker (embedded) | time-picker | |
| `pattern:review-summary` | pattern | summary (suffix) | list-items | |
| `pattern:spend-summary` | pattern | summary (suffix) | stat-card | |
| `pattern:statement-range-see-date-range-picker` | pattern | date-range-picker (embedded) | date-picker | |
| `pattern:table-row-actions` | pattern | table (prefix) | icon-button | |
| `pattern:table-trend-column` | pattern | table (prefix) | chart-sparkline | |
| `pattern:view-switcher-tab-bar` | pattern | tab-bar (embedded) | tabs | |
| `context:card` | context | cards (exact) | accordion, avatar, button, countdown-timer, divider, links, loading-indicator, status-indicator, tabs, tags, video-player | |
| `context:card-header` | context | cards (prefix), headers (suffix) | eyebrow, icon-button | |
| `context:dialog-modal` | context | modals (suffix) | button, countdown-timer | |
| `context:form` | context | form-layout (prefix) | accordion, button, countdown-timer, divider, dropdown, input-fields, notifications, search-field, selection-controls, slider | |
| `context:forms` | context | form-layout (prefix) | alert | |
| `context:header` | context | headers (exact) | avatar | |
| `context:icon` | context | icon-button (prefix) | badge | |
| `context:link` | context | links (exact) | badge | |
| `context:list` | context | list-items (prefix) | cards, divider, links, list-items, tags | |
| `context:list-item` | context | list-items (embedded) | avatar, status-indicator | |
| `context:modal-footer` | context | modals (prefix) | action-bar | |
| `context:modal-sheet` | context | modals (prefix) | headers | |
| `context:navigation` | context | navigations (exact) | avatar | |
| `context:navigation-item` | context | navigations (prefix) | badge | |
| `context:notification-centres` | context | notifications (prefix) | empty-state | |
| `context:page-header` | context | headers (suffix) | breadcrumbs, button, eyebrow, icon-button | |
| `context:section-header` | context | headers (suffix) | eyebrow, tabs | |
| `context:stat-card-kpi-tiles-the-receipted-seam` | context | stat-card (embedded) | chart-sparkline | |
| `context:tab` | context | tabs (exact), tab-bar (prefix) | badge | |
| `context:tab-panel` | context | tabs (prefix) | accordion | |
