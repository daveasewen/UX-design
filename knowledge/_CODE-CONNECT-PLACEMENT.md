# Code Connect — where it fits (placement note)

*Written 2026-06-20 (build chat). Strategy-owned (lane D) — this is the agreed placement, NOT a build-chat task. Sequencing + whether mappings become a pipeline check is the strategy chat's call.*

## One line
Code Connect is the **last-mile bridge** (Figma node → real Sutherland React component). It runs **after** the code library exists and is accepted — downstream of everything the build chat produces.

## Pipeline position
1. **Token + component canon** — semantic tokens (signed off), gated `snippets/*.reference.html` + `components/*.meta.json` (bindings, ARIA, contrast, states). ← build chat lives here.
2. **Sutherland acceptance fixtures** — `_build_sutherland_fixtures.py` → per-component contract (token bindings + requiredAria + passing contrast pairs + props). The snippets *are* the test.
3. **Sutherland JSON / React components land** — the actual library (≥1 week out as of 2026-06-20), validated against (2).
4. **Code Connect** — map each *accepted* Figma node → its Sutherland component (import + prop mapping). Figma Dev Mode / Figma MCP then returns canonical code, not generated guesses. This is the publish/wiring step.

## Hard dependencies (why not now)
- Needs **accepted Sutherland components** (step 3) — none exist yet.
- Needs **fixture-pass confidence** (step 2 ✓ vs 3) — mapping before acceptance wires Figma to non-canonical code.
→ Doing Code Connect early = false canon. Blocked until 3 lands.

## Opportunity to raise in strategy
The **Sutherland fixtures (2) can DRIVE the Code Connect mappings (4)** — the same per-component acceptance contract that validates a Sutherland component can generate/justify its Figma→code mapping. Connects acceptance directly to publish. Figma MCP already exposes the tooling (`get_code_connect_map`, `add_code_connect_map`, `get_code_connect_suggestions`).

## Ownership
Lane D / strategy chat (parked with Figma dark write-back + harness redesign). Build chat does not own sequencing or check-tiering of Code Connect.
