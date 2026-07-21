# Component accessibility — conformance basis

> The `accessibility` blocks and `relatedSC` arrays in every `*.meta.json` are graded against **WCAG 2.2 AA** — the minimum set by **HSBC's digital accessibility framework**, governed by **Group Digital Experience and Accessibility**, mandatory on all HSBC digital projects. Source: `knowledge/guidelines/digital-accessibility-standards.md` (create.hsbc). New build is reviewed by the Brand Design Team before release.

## Why relatedSC was updated (2026-06-18)

The component metas originally cited **2.5.5 Target Size** — which is **AAA (Enhanced)** in WCAG 2.1. The **gradeable AA criterion** is **2.5.8 Target Size (Minimum)** (24×24px), added in WCAG 2.2. All target-size citations were moved to **2.5.8** (HSBC's 44px targets exceed both the 24px AA floor and the 44px AAA target). The WCAG-2.2-new criteria were also added where they apply.

## WCAG 2.2-new success criteria → components

- **2.5.8 Target Size (Minimum)** — AA, 24×24px. Applied across all interactive components (17 metas): avatar, slider, navigations, list-items, tabs, tags, view-options, button, headers, modals, pagination, quick-actions, selection-controls, reorder, dropdown, plus accordion/EXAMPLE-button (already on 2.5.8).
- **2.5.7 Dragging Movements** — AA. Every drag operation needs a single-pointer (non-drag) alternative. Applied to: **reorder, quick-actions, slider, list-items** (reorderable). Note: a slider operable by arrow keys already satisfies this.
- **2.4.11 Focus Not Obscured (Minimum)** — AA. A focused element must not be fully hidden by sticky/overlay content. Applied to: **navigations** (sticky masthead/flyouts), **modals** (overlay), **tabs** (sticky bar), **dropdown** (menu over trigger), **tooltip**, **search-field** (predictive dropdown).
- **3.3.8 Accessible Authentication (Minimum)** — AA. No cognitive-function test to log in. No component currently models auth; tracked at the standards level (`digital-accessibility-standards.md`).
- *(Also relevant but AAA / not added per-component:* 2.4.13 Focus Appearance, 2.5.5 Target Size (Enhanced)*; 3.2.6 Consistent Help is A — consider for the Contextual help pattern.)*

## For the compliance knowledge-graph

Treat every `relatedSC` entry as "must meet at **WCAG 2.2 AA**." The SC anchors are now concrete and gradeable (rule → component → check → SC → clause), with the conformance authority = Group Digital Experience and Accessibility.
