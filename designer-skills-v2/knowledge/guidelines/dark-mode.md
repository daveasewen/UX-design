---
title: Dark mode
source: HSBC Common Toolkit (MCP) — "Gaps and edits" branch, Foundations › Dark mode page (node 46025:22918)
type: foundation-guidance
captured: 2026-06-17
related_tokens: semantic-colour.json (dark mode), colour.json (neutral-dark-mode, rag-dark), elevation.json
external_ref: https://create.hsbc/Guidelines/Foundations/Elevation.html
note: Guidance-only page — introduces NO new design tokens. Dark-mode token values live in semantic-colour.json (dark mode) and the dark-mode-only primitives. RAG-bordered do/don't examples consume colour/rag/* tokens.
---

# Dark mode

Dark mode is an alternative view to traditional, lighter designs, where a darker theme is used to reduce the amount of light emitted from a digital display.

## Considerations

- Users may choose dark mode for various reasons, including personal comfort, to improve eyestrain, or for greater accessibility.
- Reducing the amount of light emitted is key to successfully implementing dark mode.
- It's **not a straight inversion** of a light mode design. Swapping an already-dark background to a white background is counterintuitive and could create a jarring user experience in a low-light environment.
- Colour usage needs to be considered and reduced where possible, including using **desaturated** colours.
- Accessibility standards must still be met, especially around colour contrast. Reducing the amount of light emitted shouldn't come at the cost of accessibility.
- The HSBC brand must still be recognisable in dark mode. Exact colour values may change between light and dark mode, but following the HSBC guidelines maintains cohesive design across modes.

## Behaviour

Users are usually able to set their preference for dark mode at a system level. Detecting and following the user's preference provides a seamless experience — and, where possible, more granular control should be given to let users set their dark-mode preference within platform settings, to override their system setting.

## Colour

> **Accessibility — maintain a 3:1 contrast ratio.** Maintain a sufficient level of colour contrast when adjusting and exchanging colours for dark mode, to ensure an accessible experience.

- ✅ **Do** keep already-dark backgrounds to maintain a majority-dark design.
- ❌ **Don't** invert already-dark backgrounds to light.
- ✅ **Do** use the appropriate adjusted colour palette.
- ❌ **Don't** use the same bright or rich colours across both light and dark modes.

## Elevation

Elevation is a visual indication of depth or distance. In light mode, different levels of elevation are shown with overlays and shadows that darken lower levels. In dark mode the effectiveness of these methods is limited because the background is already dark. The methods below show how to use elevation in dark mode specifically, but the full [elevation guidelines](https://create.hsbc/Guidelines/Foundations/Elevation.html) should still be followed.

### Lighter background surfaces

In light mode, depth perception is created by darkening deeper levels. In dark mode, use the reverse effect and make the higher levels lighter. The lighter the background surface of the level, the higher it appears to be.

## Typography and icons

Follow the standard type and icon foundations; ensure colour contrast for text and icons still meets accessibility requirements against the darker surfaces (see the 3:1 note above).

## Imagery

- ✅ **Do** use a low-opacity overlay on the image to reduce brightness.
- ❌ **Don't** use overly bright imagery in dark mode.
- ✅ **Do** consider the edges of an illustration and use opacity to optimise for light and dark mode.
- ✅ **Do** include a background when needed, but consider how it's contained as well as how bright it is.
