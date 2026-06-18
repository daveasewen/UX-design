# Time-based indicators

> Source: HSBC Common Toolkit — "Time-based indicators" (Figma node 45233:181220, "Gaps and edits" branch). Guidance/pattern page — **no bound design tokens** (composed from existing components: Countdown timer, Loading indicator, Progress tracker, etc.).

## Purpose

Time-based indicators are visual cues that show the **remaining time before something will change state or expire**. They reassure the user about timing and prompt action before a deadline.

## Usage

Two primary jobs:

- **Inform** — tell the user they're coming to the end of a specific time period (e.g. a session or offer ending soon).
- **Remind** — prompt the user about an upcoming event.

## Structure

Time-based indicators are not a single component — they're assembled from existing patterns (e.g. a countdown timer, a progress/segmented bar, or a labelled date/time) plus accompanying copy. They always sit **within** a larger pattern, never standalone.

## Behaviour

- **Do** use a time-based indicator **within a single pattern** (paired with the content/action it relates to).
- **Don't** use a time-based indicator **on its own** — it must accompany other content that gives it context.

## Copy considerations

Make the remaining time and what will happen clear in the copy (the indicator supplements the text, it doesn't replace it).

## Accessibility

- **Alt text** — the indicator icon is **supplementary to the text**, so alt text is **not required** (the text carries the meaning).
- **Colour contrast** — the indicator should meet the **non-text contrast ratio of 3:1** against adjacent colours.
- **Animation** — the indicator is **not considered essential**, and so **should not be animated** (avoid motion that could distract or fail prefers-reduced-motion expectations).

## Related WCAG

1.4.11 Non-text Contrast (3:1), 1.4.1 Use of Color, 4.1.3 Status Messages, 2.3.3 Animation from Interactions.

## Related components

Countdown timer, Loading indicator, Progress tracker (the concrete components that may act as time-based indicators).
