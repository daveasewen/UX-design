---
title: Logos
source: HSBC Common Toolkit (MCP) — "Gaps and edits" branch, Foundations › Logos page (node 29:1009)
type: foundation-guidance
captured: 2026-06-17
related_assets: knowledge/assets/logos/ (8 logo SVG variants, 12 before s282-D4 — EXPORTED 2026-06-17, vector; see _export-logos.py)
external_ref: https://create.hsbc/foundations-and-identity/Logos.html
note: This page is largely a sticker sheet of logo artwork; detailed usage/structure/placement rules live on create.hsbc (link above). No design tokens.
---

# Logos

The detailed logo standard (usage, structure, behaviours, placement, clear space, minimum sizes) lives on **create.hsbc** → [Logos](https://create.hsbc/foundations-and-identity/Logos.html). The Figma page provides the artwork sticker sheet.

## Logo set
Two logo lockups (the *Masterbrand with identifier* lockup was SCRAPPED — s282-D4, Dave 2026-09-18: its four files moved to `_to_delete/logos-identifier-282/`, its nodes removed from the graph), each available in **Colour** and **Monotone**, and in **On Light** and **On Dark** treatments (the On-Dark artwork is the light/reverse version for dark surfaces):

1. **Hexagon** — the HSBC hexagon mark alone.
2. **Masterbrand** — hexagon + "HSBC" wordmark.
3. ~~Masterbrand with identifier~~ — SCRAPPED (s282-D4). The identifier lockup was an "Example identifier" placeholder; two of its four exports were the plain masterbrand on a wider canvas (#282 logo review, exporter defect).

That's **8 variants** (2 lockups × {Colour, Monotone} × {On Light, On Dark}) — was 12 before s282-D4.

## Exported assets
SVGs exported to `knowledge/assets/logos/<lockup>-<light|dark>-<colour|mono>.svg` via `_export-logos.py` (Figma `file_content:read` token). All 12 (now 8) came through as **vector** (hexagon in `#DB0011`/white; masterbrand wordmark and identifier as vector paths) — no embedded raster.

> Per the icons sourcing rule, treat these exports as **internal prototype assets**; for production/dev handoff, source official logo artwork from create.hsbc / the UI Centre.
