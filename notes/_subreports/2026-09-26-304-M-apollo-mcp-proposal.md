# #304 lane M — the Apollo-MCP proposal page

provenance: 304 · 2026-09-26 · lane M (Opus 5.5) · repo HEAD 571d458c (read-only)
status: built and rendered. Not committed: the conductor commits.

## What was built
- **The page:** `notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html` (70,121 B, self-contained, inline CSS and SVG, no external scripts). House style copied from `notes/_PROPOSAL-apollo-story-2026-09-20-v2.html`, including its decisions overlay (19 boxes: 11 sections + 7 decisions + whole page; exports markdown for `notes/_lanes/304/`). Body copy about 2,800 words (sources and technical footer excluded), zero em-dashes, no ruling ids in the body.
- **Sections:** header with his Saturday ask verbatim · the answer · the thread (20 June to 26 Sept, dated) · the field as three layers + four cards + "re-checked today" · the flow diagram (wide SVG for desktop, tall SVG for phone, same content) · three routes side by side (A own protocol, B A2UI catalogue over MCP with MCP Apps fallback, recommended, C MCP Apps raw HTML only) · the four adds · "every run-time choice is mechanical" (Jev dev-time only, 21 Sept) · measured today + the five gaps · build path in six phases with estimates · risks and controls · seven decisions · 42 dated sources · technical footer.
- **Working files:** `notes/_lanes/304/M/page.src.html` (template), `build.py` (parses G2's sources 1–40 from the filed report, never retyped; copies the overlay from the v2 page and swaps only its settings), `render.py` (driver).

## The seven decisions put to Dave
1. Route: B. 2. Name: Apollo-MCP, or Apollo Live / Apollo Wire / Apollo Floor; recommends **Apollo Live** (names what it does, not the pipe). 3. First vehicle: June's contextual dashboard on mock data. 4. Money screens data-only, confirmation in the bank's own flow. 5. Read the Jev ruling as covering the live screen too (G1 flagged that "run time" at #293 meant compose time). 6. First catalogue = the dashboard's ~15 parts, not all 137. 7. Start phases 1–4 now (they pay back at design time; June's "one shared investment"), dashboard after.

## Research re-check (all 2026-09-26)
- A2UI: **unchanged.** v0.9.1 production, v1.0 release candidate, Q4 2026; roadmap "Last Updated: June 2026"; SwiftUI still "Planned". Catalogue ids are URIs, JSON Schema, `supportedCatalogIds`; inline catalogues "not recommended in production".
- MCP Apps hosts: **firmer.** The official client matrix (https://modelcontextprotocol.io/extensions/client-matrix) now lists ChatGPT, Cursor, PostHog Code; G2 had them only from a secondary source. Extension id `io.modelcontextprotocol/ui` confirmed there.
- A2UI in chat hosts: **narrower than G2.** "A2UI in the World": no general chat host (Claude, ChatGPT, Copilot, Gemini app) renders A2UI natively; Gemini Enterprise does only for self-serve agents registered via the A2A path, not managed Vertex agents.
- MCP core: **new to the page.** The 2026-07-28 spec (GA) is stateless (no handshake, no session id) and puts method and tool names in HTTP headers so gateways can route and authorise without parsing the body.
- Enterprise-Managed Authorization: **new.** Official MCP extension (`io.modelcontextprotocol/enterprise-managed-authorization`, spec under ext-auth `specification/stable`): the enterprise IdP decides server access.
- MCP-UI: **unchanged.** "The MCP-UI packages implement the spec, and serve as a community playground for future enhancements."
- Google's 17 June post confirms the fallback: "packaging the A2UI rendering engine directly within the MCP App bundle".
- Not re-checked: G2 sources 1, 2, 4, 8–11, 13–15, 18, 19, 21–40.

## Counts re-probed this lane (HEAD 571d458c)
138 metas; when 39 · slots 35 · answers 26 · shape 26 · provides 108 · priority 25 (all match G1). showroom 137 + 8 = 145. Reference snippets **137**, not G1's 139 (the folder also holds two `_REVIEW-66-*.html`, the likely difference); 0 `<template>`, 0 `{{`, 0 custom elements, 1 `data-slot`. Timings (0.82 s selector, 0.68 s static gate, 107 s KG build) are G1's, not re-measured.

## Render receipts
Run at the seat per the Project instructions (ensure_env OK, seat_env OK). No page errors. 1440: scrollWidth 1440, doc 18,998 px, 0 elements past the right edge, no clipped overflow, wide diagram at 0.948 scale (12 px text renders 11.4 px). 390: scrollWidth 390, doc 32,111 px, 0 past the edge, tall diagram at 0.922 (11.1 px). Routes use CSS subgrid so rows align across A/B/C on desktop and stack as cards on a phone. Looked at by eye; fixed on the way: host arrows hidden under the host frame, missing step arrows, six accent "Proves" lines (now black), mobile gap under split labels, answer paragraph trimmed. The fixed decisions bar is made static in shots only.
Shots in `notes/_lanes/304/M/shots/`: `apollo-mcp-v1-w1440-full.png`, `apollo-mcp-v1-w390-full.png`, slices `w1440-part01..13.png`, `w390-part01..23.png` (a stale `w390-part24.png` from the first run may remain), close-ups `diagram-w1440@2x.png`, `diagram-w390@2x.png`, `routes-w1440@2x.png`, `routes-w390@2x.png`.

## Could not verify / caveats
- The render seat lacks Helvetica Neue's thin and medium weights, so h1 (200) and landmarks (500) render at regular in the shots; on Dave's Mac they show as designed.
- Build-path session estimates are this lane's, unmeasured, with nothing to calibrate against.
- "It can run hot" is his word as recorded in a retired memory note (G1 marks it DAVE), not a verbatim transcript line.
- The fixed default order "where the rules can't decide" is a proposal detail, not an existing mechanism.

## v2 (same day, on Dave's 14:51 and 14:52 messages)
- **Page:** `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` (83,383 B). v1 untouched (md5 253f36b5… before and after the v2 build). Built by `notes/_lanes/304/M/build_v2.py` from `page-v2.src.html`, reusing v1's CSS and diagram and build.py's sources/overlay logic; rendered by `render_v2.py` into `notes/_lanes/304/M/shots/v2/`.
- **Jev corrected.** v1 wrongly read the 21 Sept ruling (s294-D10) as a run-time ban. v2 removes that. A new "Judgement at run time" section quotes his 14:51 and puts a rules-only baseline beside "rules plus Jev". Jev ranks inside the rules' shortlist or reads intent and data shape, and can never add a part. Costs: a dependency that makes the layer less portable, and a network hop of 579–621 ms per call (quoted from the ruling's own text, n=3). Degrades to the rules' order, recorded. The diagram's step 1 now reads "rules shortlist, a judge may rank". New decision: Jev in the GenUI layer, yes/no/later. Recommends yes for the PoC, behind a switch that is off by default.
- **Split into two parts.** An "at a glance" answer sits at the top (both, at different depths: the PoC is defined in full, the architecture only as the direction it must not paint out). Part one is the target architecture: the field, the three routes, the diagram, the four adds, judgement. Part two is the PoC: scope in and out, what it proves, entitlements, build path. The PoC is now milestone one: six steps, 11–15 sessions estimated, with Jev side by side as step six. Everything else is listed "after the PoC", not estimated.
- **Entitlements best guess**, labelled "Best guess for the PoC, not HSBC's entitlement model". Four mock roles (corporate treasurer, relationship manager, operations analyst, read-only auditor) mapped to tools and data scopes, with a mock £500,000 approval limit. Enforced at the tool call, with grants and refusals written into the record. Worked example: "What needs my attention this morning?" at 09:10 on month end gives two different surfaces, for the treasurer and the operations analyst. No HSBC source was read; all invented.
- **Decisions: now six.** Route, PoC as scoped, Jev yes/no/later, name, money screens, when to start. Dropped or merged: first vehicle and catalogue scope go into "PoC as scoped"; "what the Jev ruling covers" is settled by his 14:51.
- **Render:** no page errors. 1440: scrollWidth 1440, doc 23,890 px, 0 elements past the edge. 390: scrollWidth 390, doc 39,898 px, 0 past the edge. Diagram smallest text 11.4 / 11.1 px. 20 decision boxes. Looked at by eye: the two part bands, the judgement comparison, the scope lists, the roles table, the worked example and the build path, at both widths. Body is about 3,900 words, longer than v1's 2,800 because of the new PoC half.
- **Housekeeping:** the stale `shots/w390-part24.png` from v1's first run is deleted. The delete permission was granted for the repo folder for this session, and only that one file was removed.
