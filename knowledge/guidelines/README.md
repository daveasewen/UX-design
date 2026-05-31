# Guidelines (RAG canon)

Prose knowledge retrieved semantically (RAG), not graphed: brand voice, written
standards, IA conventions, pattern rationale, content style.

## Why RAG here (not a knowledge graph)

This content is unstructured and semantic — "what's our tone for error messages",
"how do we write empty states". Retrieval over well-structured Markdown is
sufficient; a graph would be overhead without payoff. (Contrast with the
component and compliance stores, where relationships justify a graph.)

## Structure

Keep one concern per Markdown file with clear headings, so chunks retrieve
cleanly:

```
guidelines/
├── voice-and-tone.md
├── writing-standards.md       # plain language, reading level, regulated terms
├── ia-conventions.md
└── pattern-rationale.md
```

## Source

Authored from the published design-standards website + internal docs (on the
agency machine). The public standards site can seed this at home for realism.
