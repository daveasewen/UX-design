# Idea (Dave, #258, 2026-09-08, after the wrap) — context-aware responsive behaviours

**His words, verbatim:**

> Can we make responsive behaviors context aware, for instance, could a segmented control have two or more different responsive behaviors (in this case space-awarness). Imagine we have a set of controls in a row, one behavior could be a simple reflow and the seg-control might just stack under the other controls, another might be that it collapses into a split button, I could imagine that there are other responsive behaviors that might have more than one behavior bepending on context and designer preference. I don't know if we have this decision made at author time automatically, or the option is presented to the designer, or this is something that the designer finesses at edit mode.
>
> It's definitely something I'd like us to investigate, maybe theres some material only we can research.

**Status:** CAPTURED, not ruled, not scoped. Investigation owed — a research lane, not a build.

**Shape of the question (conductor's reading, labelled):** one component, N named responsive strategies (reflow / stack / collapse-to-split-button / overflow-menu / icon-only …), chosen by *context* (available inline space, siblings in the row, container query, density) and by *designer preference*. Three candidate decision points — author time (the skill picks), a presented option (the skill asks, like grill-me), or edit mode (the designer finesses on the rendered page). Possibly all three, layered.

**Where it would live if it lands:** `behaviour` meta (a `responsive.strategies[]` key with a default and a context rule), container queries in the snippet, and a skill rule. Related: `s258-D2` (the code is where innovation lives), the `behaviour`-meta backlog (51 scripted components untyped), rule 18's engine.

**Research leads to check first (unverified):** CSS container queries + `container-type:inline-size` (already used by Transfer-list); Priority+ navigation pattern; Material's "adaptive layouts" / canonical layouts; Apple HIG size classes; Polaris/Carbon overflow patterns; the pack's own Action-bar / View-options overflow behaviour. Whether any published system lets a designer choose *among* strategies per instance is the "material only we can research" question.
