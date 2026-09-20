# Brief — international banking for CEOs

Date: 2026-09-19
Status: the standing test brief for one-shot composition probes (Dave, #288). Use as written; do not add design settings to it.

## What we're making

An interactive prototype of an international banking product for the CEOs of HSBC's corporate and institutional clients. It has an overview page and a set of linked sub-pages, with the workflows simulated end to end so a CEO can click through a real task — approve a payment, acknowledge a risk exception, request a report — and see it complete.

This is a new project. It sits alongside the existing group-treasurer dashboard and borrows its data conventions, but it is a different audience with different questions. Leave the treasurer screen as it is.

## Who it's for

A CEO. Not a treasurer, not an analyst. They want to know three things when they open it, in this order:

1. **Can we fund our plans?** Cash, available liquidity and funding headroom, at a glance.
2. **Where are we exposed?** Exposure by region and currency, with a way to drill through to the positions and limits behind the number.
3. **What needs my attention?** Pending approvals and material risk exceptions, each one leading to the record they can act on.

Everything else on the overview supports one of those three. If it doesn't, it belongs on a sub-page.

## Pages

Overview · Accounts and transactions · Liquidity and funding · Payments and approvals · FX and markets · Risk and limits · Trade finance · Reports · Messages and service requests · Settings.

## How it should behave

- One set of filters — entity, region, date range — shared across every page and remembered as you move between them.
- Reporting in GBP over a rolling 30 days, with the FX rates used shown plainly as illustrative.
- Records are searchable, sortable and paged; every row opens a detail view.
- Approvals and requests validate their inputs and complete with a confirmation. Risk acknowledgements take an audit note.
- Exports, messages and navigation state all work; nothing dead-ends.

## Data

Realistic placeholder entities, currencies and 30-day time series, with enough rows to make sorting, filtering and paging meaningful. No live banking connections, no credentials.

## Boundaries

Use the design system as it stands — its components, patterns and accessibility defaults. Don't invent components, variants, colours or icons; if something is missing, say so as a gap rather than improvising. Desktop first, comfortable density.

## What "done" means

A CEO can open the overview, answer the three questions without scrolling, and complete at least one workflow on each sub-page. Anything untested or unsupported is described as a gap, not claimed.
