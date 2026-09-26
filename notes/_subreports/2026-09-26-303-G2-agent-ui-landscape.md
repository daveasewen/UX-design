# #303 lane G2 — agent-UI protocol landscape (research, 2026-09-26)

Filed by the conductor from lane G2's hand-back (the research seat had no repo access). Every claim carries its source number; the source list is at the foot. Accessed dates are 2026-09-26 unless stated.

## 1. Google A2UI
- Announced 2025-12-15, Apache 2.0, launched at v0.8. Agents send declarative data, never code; the client keeps a "catalog of trusted, pre-approved UI components" [1].
- v0.9 (2026-04-17): "Frontend developers don't want new components. They already have a design system." Bundled set renamed Standard → Basic; React renderer added beside Flutter, Lit, Angular [2].
- Production is v0.9.1, MIME `application/a2ui+json`; v1.0 is a release candidate (client→server RPC, action IDs) [3], targeted Q4 2026 with renderer certification [6]. v1.0 is spec'd, not shipped.
- Wire format v0.9.1: JSONL. Server→client `createSurface` (surfaceId, catalogId, optional theme, sendDataModel), `updateComponents`, `updateDataModel` (JSON Pointer + value), `deleteSurface`. Client→server `action` (name, sourceComponentId, timestamp, context) and `error` (incl. VALIDATION_FAILED). Components are a flat ID-linked list with a required `root`; properties are `Dynamic*` (literal, `{path}` binding, or `{call}`); inputs bind two-way locally and sync to the server only on an action [4].
- Catalogues are JSON Schema; client declares `supportedCatalogIds` in preference order or inline catalogues; the agent picks one per surface, fixed for its life [4][5]. Guidance: catalogues should "directly reflect a client's design system"; version like an API (add freely, deprecate not delete, bump URI only on a major) [5]. Validation on both sides, graceful fallback [5].
- Transports: A2A, AG-UI, MCP, WebSocket, SSE [4]. Renderers official: React, Flutter, Lit, Angular [2]; AndroidX Compose renderer on v0.9.1 with a Material 3 Basic catalogue [10]; SwiftUI on the roadmap for Q2 2026, NOT verified shipped [6]. Flutter `genui` v0.9.0 on 2026-05-14 [9].
- Adopters Google lists in production: Opal, Gemini Enterprise, Flutter GenUI SDK, ADK; partners CopilotKit/AG-UI, AG2 [7]. Gemini Enterprise ships a built-in A2UI renderer and sends agents its own catalogue [11] (GA vs preview not stated). Oracle Agent Spec and a Vercel json-render proof named in [2]. Reaction to v0.9 mixed [8].

## 2. MCP-UI and MCP Apps
- SEP-1865 proposed 2025-11-21 by MCP maintainers, MCP-UI (Ido Salomon, Liad Yosef), Anthropic and OpenAI, built on MCP-UI and OpenAI's Apps SDK [13]; live 2026-01-26 as "the first official MCP extension" [14].
- A tool's `_meta.ui.resourceUri` points at a `ui://` resource, MIME `text/html;profile=mcp-app`; hosts can prefetch and review it [15][16]. Sandboxed cross-origin iframe; default CSP `default-src 'none'`, `connect-src 'none'`, widened by `connectDomains` / `resourceDomains` / `frameDomains`; permissions requestable [15].
- postMessage JSON-RPC: `ui/initialize`, `ui/notifications/tool-input` and `tool-result`, `tools/call`, `ui/message`, `ui/open-link`, `ui/update-model-context`, `ui/request-display-mode` [15]. Host passes standard CSS variables (colour, type, radius, shadow) — the only theming hook [15]. Hosts can restrict which tools a view calls and gate UI-initiated calls behind consent [14][16].
- Legacy MCP-UI: rawHtml, externalUrl, remote-dom; actions tool/prompt/notify/link/intent [18]. MCP-UI now "an implementation of MCP Apps" and "a community playground", Apache 2.0 [17]. MCP Apps ships HTML only; external URLs, remote DOM, native widgets are future work [13].
- Hosts in the official docs: Claude (web, desktop), VS Code GitHub Copilot, Microsoft 365 Copilot, Goose, Postman, MCPJam, Archestra [16]. A secondary log (2026-08-23) adds ChatGPT, Cursor, PostHog Code; JetBrains, Kiro, Antigravity not yet [19]. Extension id `io.modelcontextprotocol/ui` [19]. The 2026-07-28 core spec formalised an extensions framework with Apps as one extension [20].

## 3. OpenAI Apps SDK, AG-UI, the three layers
- Apps SDK launched on MCP 2025-10-06 (partners incl. Figma, Canva, Booking.com); Business/Enterprise/Edu preview 2025-11-13 [21]. ChatGPT now "implements the open MCP Apps standard"; `window.openai` / `openai/outputTemplate` remain as compatibility aliases, no deprecation date [22].
- AG-UI (CopilotKit): lifecycle, streamed text/tool-call, StateSnapshot / StateDelta (RFC 6902), MessagesSnapshot, Activity, Reasoning, Subagent, Raw, Custom events [24]. "AG-UI is not a generative UI specification" — it is the transport that carries A2UI and MCP-UI [23]. Layering: MCP = tools/context, A2A = agent-to-agent, AG-UI/A2UI = agent-to-user (spec-vs-transport verified; exact three-layer wording not re-verified).

## 4. Others
- Vercel AI SDK RSC `streamUI` "currently experimental"; AI SDK UI recommended for production [25]. Vercel Labs json-render (Jan 2026, Apache 2.0): Zod-defined catalogue, progressive streaming, React/Vue/Svelte/React Native, 36 shadcn components; InfoQ: a "tool" where A2UI is a "protocol" [26].
- Thesys C1 launched 2025-04-18 [27]; OpenAI-compatible API returning UI specs; claims ISO 27001 and SOC 2 [28]; proprietary.
- Microsoft Adaptive Cards: declarative JSON rendered natively per host; as of 2026-07-14 Teams and M365 Copilot Chat target schema 1.5, Bot Framework Web Chat 1.6, Outlook Actionable Messages 1.0–1.2 [29]. M365 Copilot is also an MCP Apps host [16].

## 5. Design systems as the catalogue
- Figma: design systems are "the lingua franca between design and AI" [30] (undated); Dev Mode MCP beta June 2025 [31]. Storybook MCP (preview, docs v10.6): component manifests to agents, interaction and a11y tests in a "self-healing loop" [32]. shadcn MCP for namespaced registries, Aug 2025 [33]. IBM Carbon MCP public preview, page updated 2026-09-23 [34]. Atlassian `@atlaskit/ads-mcp`; 2026-09-16 a CLI reached 60% more agents than the MCP server — "judge the whole task, not only the payload" [35].
- A2UI's catalogue guidance is the clearest statement that the design system is the catalogue [2][5]. All the above serve coding agents at design time. No public case found of a bank or enterprise design system as a run-time A2UI / MCP Apps catalogue. Salesforce SLDS, Polaris, GOV.UK, Material MCPs not verified.

## 6. Risks and controls for a regulated bank
- OWASP LLM Top 10 2025: LLM01 prompt injection, LLM05 improper output handling, LLM06 excessive agency [36]. OWASP Agentic Top 10 (2025-12-09) [37]: ASI01 goal hijack, ASI05 unexpected code execution, ASI07 insecure inter-agent comms, ASI09 human-agent trust exploitation [38] — ASI09 is the spoofing risk: a convincing, well-branded agent UI is itself the attack surface.
- VentureBeat 2026-09-07: stored XSS through MCP Apps — a tool stores malicious HTML which later runs in a trusted client, enabling credential harvesting [40]. A2UI's answer: no code crosses the wire [1][12].
- MCP security best practices: confused deputy, token passthrough forbidden, SSRF, session hijacking, least-privilege scope with step-up [39] — maps to data entitlements.
- Neither spec mandates accessibility: A2UI lists ARIA/keyboard/contrast as "long-term vision" [6]; MCP Apps silent [15]. No protocol guidance found on replay, determinism or audit retention.

## What this means for Apollo-MCP (lane G2's read)
1. Speak the standards, don't invent one: Apollo's components as a versioned A2UI catalogue (JSON Schema `catalogId`), delivered over MCP, with MCP Apps as the fallback shell running Apollo's own A2UI renderer in the iframe [12] — reaching Claude, ChatGPT, M365 Copilot.
2. The protocols leave "what is allowed" to the client; Apollo's metas say when a component should be used, for what data shape and question, under which ruling.
3. Apollo's gates fill the accessibility gap in both specs; run them server-side before `updateComponents` goes out.
4. The knowledge graph as the audit record: catalogue version, component ids and the rulings each obeys, per surface.
5. No raw-HTML MCP Apps for anything transactional; declarative-only surfaces; entitlements enforced at MCP tool scope [39], never in the UI.

## Sources
1. Google Developers Blog, "Introducing A2UI", https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/, 2025-12-15
2. Google Developers Blog, "A2UI v0.9", https://developers.googleblog.com/a2ui-v0-9-generative-ui/, 2026-04-17
3. A2UI home, https://a2ui.org/
4. A2UI v0.9.1 spec, https://a2ui.org/specification/v0.9.1-a2ui/
5. A2UI Catalogs, https://a2ui.org/concepts/catalogs/
6. A2UI Roadmap, https://a2ui.org/roadmap/
7. A2UI in the World, https://a2ui.org/ecosystem/a2ui-in-the-world/
8. InfoQ, "Google Releases A2UI v0.9", https://www.infoq.com/news/2026/07/google-a2ui-genui/, 2026-07-03
9. Flutter Blog, "New updates to A2UI and GenUI", https://flutter.dev/blog/new-updates-to-a2ui-and-flutters-genui-package, 2026-05-14
10. Android Developers, A2UI renderer for Compose, https://developer.android.com/develop/ui/compose/agentic
11. Google Cloud Blog, "Gemini Enterprise and A2UI", https://cloud.google.com/blog/topics/developers-practitioners/guide-to-gemini-enterprise-and-a2ui-integration, 2026-05-29
12. Google Developers Blog, "A2UI + MCP Apps", https://developers.googleblog.com/a2ui-and-mcp-apps/, 2026-06-17
13. MCP Blog, MCP Apps proposal, https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/, 2025-11-21
14. MCP Blog, MCP Apps, https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/, 2026-01-26
15. MCP Apps spec 2026-01-26, https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
16. MCP Apps overview, https://modelcontextprotocol.io/extensions/apps/overview
17. MCP-UI, https://mcpui.dev/
18. MCP-UI README, https://github.com/MCP-UI-Org/mcp-ui
19. DevMoment, "MCP Apps in 2026", https://www.devmoment.dev/journal/mcp-apps-field-log-2026, 2026-08-23 (secondary)
20. MCP Blog, "The 2026-07-28 Specification", https://blog.modelcontextprotocol.io/posts/2026-07-28/, 2026-07-28
21. OpenAI, "Introducing apps in ChatGPT", https://openai.com/index/introducing-apps-in-chatgpt/, 2025-10-06
22. OpenAI Developers, "Add UI to your MCP server", https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt
23. CopilotKit, "AG-UI and A2UI", https://www.copilotkit.ai/ag-ui-and-a2ui
24. AG-UI Events, https://docs.ag-ui.com/concepts/events
25. AI SDK, streamUI reference, https://ai-sdk.dev/docs/reference/ai-sdk-rsc/stream-ui
26. InfoQ, "Vercel Releases JSON-Render", https://www.infoq.com/news/2026/03/vercel-json-render/, 2026-03-26
27. BusinessWire, "Thesys Introduces C1", https://www.businesswire.com/news/home/20250418761213/en/, 2025-04-18
28. Thesys, https://www.thesys.dev/
29. Microsoft Learn, "Adaptive Cards for agent design", https://learn.microsoft.com/en-us/agents/design-guidelines/adaptive-cards-for-agent-design, 2026-07-14
30. Figma Blog, "Design Systems and AI", https://www.figma.com/blog/design-systems-ai-mcp/, undated
31. AlternativeTo, "Figma launches Dev Mode MCP server", https://alternativeto.net/news/2025/6/figma-launches-dev-mode-mcp-server-for-direct-ai-access-to-design-data, 2025-06
32. Storybook, MCP server docs, https://storybook.js.org/docs/ai/mcp/overview
33. shadcn/ui, "CLI 3.0 and MCP Server", https://ui.shadcn.com/docs/changelog/2025-08-cli-3-mcp, 2025-08
34. Carbon, "Carbon MCP", https://carbondesignsystem.com/developing/carbon-mcp/overview/, 2026-09-23
35. Atlassian, "Giving AI agents design system context from the terminal", https://www.atlassian.com/blog/ai-at-work/giving-ai-agents-design-system-context-from-the-terminal-what-we-learned-building-a-cli, 2026-09-16
36. OWASP, LLM Top 10 2025, https://genai.owasp.org/llm-top-10/
37. OWASP, Top 10 for Agentic Applications 2026, https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/, 2025-12-09
38. Teleport, "OWASP Top 10 for Agentic Applications", https://goteleport.com/blog/owasp-top-10-agentic-applications/
39. MCP, "Security Best Practices", https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
40. VentureBeat, "MCP's new spec turns a planted prompt into a stolen credential", https://venturebeat.com/security/mcps-new-spec-turns-a-planted-prompt-into-a-stolen-credential, 2026-09-07
