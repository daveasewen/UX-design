# ADR-0002 — Build on open, model-agnostic standards

**Status:** accepted · **Date:** 2026-05-31

## Context
Files must transfer between home, agency and Promenaut machines and run under
different models (Claude, GPT‑5.5). We need conventions that no single vendor owns.

## Decision
Adopt three open standards as the spine:
- **AGENTS.md** for operating instructions (root + per-discipline overrides).
- **Agent Skills / SKILL.md** for reusable capabilities.
- **MCP** for live tool/data access (Figma Dev Mode MCP + Code Connect).
Everything else is plain Markdown + typed JSON, versioned in Git.

## Rationale
- AGENTS.md: open (Linux Foundation / Agentic AI Foundation), editor-agnostic, 60k+ adopters.
- Agent Skills: open Anthropic spec, read by ~32 tools incl. OpenAI Codex/ChatGPT, Cursor, Gemini CLI — genuinely cross-model.
- MCP: open protocol for runtime tool access.

## Consequence
Handoff to Promenaut is a `git pull`, not a port. No model-specific prompt syntax
in committed files except in clearly-marked adapters.
