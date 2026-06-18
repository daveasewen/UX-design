# View controls: sort options

> Source: HSBC Common Toolkit — "View controls: sort options" (Figma node 45226:146958, "Gaps and edits" branch). Guidance/pattern page — **no bound design tokens** (the control itself is built from Dropdown / List components).

## Purpose

Sort options are a **view control** that let users **change the order of content on a page** (e.g. newest first, A–Z, price low–high). They re-order existing content; they don't filter or add/remove it.

## Structure

A sort control is typically a labelled trigger ("Sort by…") that opens a single-select list of sort orders (built from the Dropdown + List-item components). Selecting an option re-orders the content and reflects the current choice in the trigger.

## Content display

The control shows the **currently applied sort order** so users always know how the content is ordered. Re-sorting updates the content in place.

## Usage

Use sort options when a list/grid has a meaningful default order that users may want to change. Pair with filters where users also need to narrow content (sort = order, filter = subset — keep them distinct).

## Copy guidance

Label the control clearly (e.g. "Sort by") and name each option by the order it produces (e.g. "Newest first", "A–Z", "Price: low to high") so the outcome is predictable.

## Accessibility

- Expose the control as a labelled select/combobox; announce the new order after sorting (status message) so screen-reader users know the content changed.
- The current sort option must be programmatically indicated (not by visual styling alone).
- Keyboard-operable trigger and option list.

## Related WCAG

4.1.3 Status Messages, 4.1.2 Name Role Value, 1.3.1 Info and Relationships, 2.1.1 Keyboard.

## Related components

Dropdown (single-select), List items — the building blocks of the sort control.
