#!/usr/bin/env bash
# Build the lean, designer-facing KB for the Copilot skill pack.
# Run from the repo root:  bash designer-skills-v1/build-designer-kb.sh
# Copies ONLY the reference data the skills read; leaves the internal machinery
# (Python gates/generators, audit + working docs) behind. Re-run when canon changes.
set -euo pipefail
SRC="${SRC:-knowledge}"
DST="${DST:-designer-skills-v1/knowledge}"
rm -rf "$DST"
mkdir -p "$DST"/{components,tokens,canon,snippets,compliance/rules,guidelines,assets}

# Components — contracts + schema + a11y conformance (skip the EXAMPLE template)
for f in "$SRC"/components/*.meta.json; do
  case "$(basename "$f")" in EXAMPLE-*) ;; *) cp "$f" "$DST/components/";; esac
done
cp "$SRC"/components/meta.schema.json "$DST/components/" 2>/dev/null || true
cp "$SRC"/components/_ACCESSIBILITY-CONFORMANCE.md "$DST/components/" 2>/dev/null || true

# Tokens — the stores only (skip _blast-radius / _manifests machinery)
for f in "$SRC"/tokens/*.json; do
  case "$(basename "$f")" in _*) ;; *) cp "$f" "$DST/tokens/";; esac
done

# Canon — the composition layer only (skip generators)
cp "$SRC"/canon/canon.css "$DST/canon/" 2>/dev/null || true

# Snippets — the reviewed reference markup
cp "$SRC"/snippets/*.reference.html "$DST/snippets/" 2>/dev/null || true

# Compliance — the WCAG graph + rules + schema (skip the builder)
cp "$SRC"/compliance/graph-index.json "$DST/compliance/" 2>/dev/null || true
cp "$SRC"/compliance/rule.schema.json "$DST/compliance/" 2>/dev/null || true
cp "$SRC"/compliance/README.md "$DST/compliance/" 2>/dev/null || true
cp "$SRC"/compliance/rules/*.json "$DST/compliance/rules/" 2>/dev/null || true

# Icons — the real library (skills must use real glyphs, never invent)
cp -R "$SRC"/assets/icons "$DST/assets/" 2>/dev/null || true

# Guidelines — design-relevant reference only. EXCLUDE internal/process/governance
# (edit this list to taste):
EXCLUDE="README.md _INGESTION-QUEUE.md _RECONCILIATION.md accessibility-framework.md accessibility-management-roles.md accessibility-qa-cx-testing.md accessibility-standards-hub.md digital-accessibility-standards.md digital-governance.md design-system-processes.md"
for f in "$SRC"/guidelines/*.md; do
  b="$(basename "$f")"; skip=0
  for x in $EXCLUDE; do [ "$b" = "$x" ] && skip=1; done
  [ $skip -eq 0 ] && cp "$f" "$DST/guidelines/"
done

# The KB's own readme (regenerated each build)
cat > "$DST/README.md" <<'MD'
# Design system — knowledge base

The reference data the Copilot skills read. **Generated** from the live design
system by `build-designer-kb.sh` — don't hand-edit; re-run the script to refresh.

- `components/` — one `*.meta.json` per component (props, variants, token
  bindings, states, anti-patterns, accessibility) + the schema.
- `tokens/` — the design tokens (colour, type, spacing, elevation, motion, …).
- `canon/canon.css` — the composition layer (tokens + reviewed component CSS).
- `snippets/` — the reviewed reference markup for each component.
- `compliance/` — the WCAG map (which accessibility criteria apply to which
  component) + the rule set.
- `assets/icons/` — the real icon library (skills use these, never invent icons).
- `guidelines/` — design standards for reference (brand, colour, type,
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

echo "Built $DST"
