#!/usr/bin/env bash
# Build the lean, designer-facing KB for the Copilot skill pack (v2).
# Run from the repo root:  bash designer-skills-v2/build-designer-kb.sh
# REPO-SIDE TOOL ONLY — not shipped in the pack zip. Testers get the baked
# knowledge/ folder; they never run this. Re-run when canon changes, then re-zip.
#
# v2 fixes over v1 (the v1 copy-list had gone stale against the KB layout):
#   + canon/type.css            hand-authored type composites (.t-cm-*/.t-ed-*) —
#                               snippets bind these; without it the KB is incomplete
#   + tokens/themes/            the ADR-0011 theme override sets + _themes.json
#                               registry (underscore kept: it's data, not machinery)
#   - assets/icons/*.py         the exporter script no longer ships
#   ~ provenance stamp          README records what the KB was baked from (PROVENANCE env)
set -euo pipefail
SRC="${SRC:-knowledge}"
DST="${DST:-designer-skills-v2/knowledge}"
PROVENANCE="${PROVENANCE:-the working tree, $(date +%Y-%m-%d)}"
rm -rf "$DST"
mkdir -p "$DST"/{components,tokens/themes,canon,snippets,compliance/rules,guidelines,assets}

# Components — contracts + schema + a11y conformance (skip the EXAMPLE template)
for f in "$SRC"/components/*.meta.json; do
  case "$(basename "$f")" in EXAMPLE-*) ;; *) cp "$f" "$DST/components/";; esac
done
cp "$SRC"/components/meta.schema.json "$DST/components/" 2>/dev/null || true
cp "$SRC"/components/_ACCESSIBILITY-CONFORMANCE.md "$DST/components/" 2>/dev/null || true

# Tokens — the stores only (skip _blast-radius / _manifests / _raw machinery)…
for f in "$SRC"/tokens/*.json; do
  case "$(basename "$f")" in _*|EXAMPLE-*) ;; *) cp "$f" "$DST/tokens/";; esac
done
# …plus the theme override sets. _themes.json IS the registry (data, not machinery).
cp "$SRC"/tokens/themes/*.json "$DST/tokens/themes/" 2>/dev/null || true

# Canon — the composition layer AND the hand-authored type composites
cp "$SRC"/canon/canon.css "$DST/canon/" 2>/dev/null || true
cp "$SRC"/canon/type.css  "$DST/canon/" 2>/dev/null || true

# Snippets — the reviewed reference markup
cp "$SRC"/snippets/*.reference.html "$DST/snippets/" 2>/dev/null || true

# Compliance — the WCAG graph + rules + schema (skip the builder)
cp "$SRC"/compliance/graph-index.json "$DST/compliance/" 2>/dev/null || true
cp "$SRC"/compliance/rule.schema.json "$DST/compliance/" 2>/dev/null || true
cp "$SRC"/compliance/README.md "$DST/compliance/" 2>/dev/null || true
cp "$SRC"/compliance/rules/*.json "$DST/compliance/rules/" 2>/dev/null || true

# Icons — the real library (skills must use real glyphs, never invent);
# drop the exporter machinery
cp -R "$SRC"/assets/icons "$DST/assets/" 2>/dev/null || true
find "$DST/assets/icons" -name "*.py" -delete 2>/dev/null || true

# Guidelines — design-relevant reference only. EXCLUDE internal/process/governance
# (edit this list to taste):
EXCLUDE="README.md _INGESTION-QUEUE.md _RECONCILIATION.md accessibility-framework.md accessibility-management-roles.md accessibility-qa-cx-testing.md accessibility-standards-hub.md digital-accessibility-standards.md digital-governance.md design-system-processes.md"
for f in "$SRC"/guidelines/*.md; do
  b="$(basename "$f")"; skip=0
  for x in $EXCLUDE; do [ "$b" = "$x" ] && skip=1; done
  [ $skip -eq 0 ] && cp "$f" "$DST/guidelines/"
done

# The KB's own readme (regenerated each build)
cat > "$DST/README.md" <<MD
# Design system — knowledge base

The reference data the Copilot skills read. **Pre-built** from the live design
system — don't hand-edit, and don't try to regenerate it; ask the design-system
team for a refreshed pack instead. Baked from ${PROVENANCE}.

- \`components/\` — one \`*.meta.json\` per component (props, variants, token
  bindings, states, anti-patterns, accessibility) + the schema.
- \`tokens/\` — the design tokens (colour, type, spacing, elevation, motion, …).
- \`tokens/themes/\` — the theme override sets (+ \`_themes.json\` registry). The
  components bind semantic roles; the active theme decides the hex. **Apollo Mono
  is the baseline** — monochrome, colour only in RAG status + data-vis.
- \`canon/canon.css\` — the composition layer (tokens + reviewed component CSS).
- \`canon/type.css\` — the type composites (\`.t-cm-*\` component / \`.t-ed-*\`
  editorial). Component text binds a composite class, never raw font values.
- \`snippets/\` — the reviewed reference markup for each component.
- \`compliance/\` — the WCAG map (which accessibility criteria apply to which
  component) + the rule set.
- \`assets/icons/\` — the real icon library + manifest (skills use these, never
  invent icons).
- \`guidelines/\` — design standards for reference (brand, colour, type,
  accessibility, tone, component standards, …).

**Two honest notes.** The guidelines are *reference* — a designer or a skill
consults them (they matter most when **creating a new pattern**). And the
*authoritative* compliance checks (real contrast maths, token fidelity,
accessibility) run as executable gates in CI, not here — the in-editor check
applies the same rules as guidance so you catch drift early.

Intentionally left out: the build scripts, audit/working docs, and
process/governance guidelines — this folder is the design reference, not the
workshop.
MD

echo "Built $DST (from ${PROVENANCE})"
