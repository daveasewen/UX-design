# Promenaut Agentic Design Workflow

A portable, model-agnostic agentic harness for running design-discipline work
(UX/UI, and — as a skeleton — research, CX, copywriting) on the Promenaut
platform. Abstracted from the proven **HDS** editorial pipeline reference
architecture and built on open standards so the same files run under Claude,
GPT‑5.5, and Promenaut without rewrites.

## Why this repo exists

Three goals, in priority order:

1. **Make the UX/UI build‑&‑review pipeline actually work** — brief → prototype
   from the component library → expert + accessibility review → dev handoff.
2. **Spec the full multi‑discipline process** as a reusable skeleton so other
   disciplines (research, CX, copywriting) can be instantiated from the same
   harness later.
3. **Stay transferable** between machines and models. Everything is plain
   Markdown + structured data, versioned in Git, conforming to open agent
   standards (`AGENTS.md`, Agent Skills / `SKILL.md`, MCP).

## Status

`v0.1 — planning & research`. See [`docs/research-dossier.md`](docs/research-dossier.md)
for the full findings, recommendations, and proposed architecture.

## Repo map (proposed)

```
.
├── README.md                  ← you are here
├── AGENTS.md                  ← root operating instructions for any agent
├── docs/
│   ├── research-dossier.md    ← research findings + recommendations (start here)
│   ├── architecture.md        ← harness architecture (to be written)
│   └── decisions/             ← ADRs: one decision per file
├── harness/                   ← reusable, discipline-agnostic harness spec
│   ├── orchestrator.md
│   ├── state/                 ← persistent stores (canon, memory, checkpoints)
│   ├── errors.md              ← error taxonomy + recovery
│   └── hitl.md                ← human-in-the-loop gates
├── disciplines/
│   ├── ux-design/             ← working pipeline (Define → Develop)
│   ├── ui-design/             ← working pipeline (Develop → Deliver, Dave's part)
│   ├── ux-research/           ← skeleton spec
│   ├── cx-research/           ← skeleton spec
│   ├── cx-design/             ← skeleton spec (cross-cutting)
│   ├── ux-copy/               ← skeleton spec
│   └── inputs/                ← BA/PO cross-cutting inputs
├── knowledge/                 ← design-system canon, tokens, component metadata
└── skills/                    ← portable Agent Skills (SKILL.md folders)
```

## Transfer model

Author here (home) → push to GitHub (whitelisted) → pull on the agency machine
(real company assets, frontier model) → hand to Promenaut (Claude). Git is the
single source of truth; no machine-specific paths or model-specific syntax in
committed files.
