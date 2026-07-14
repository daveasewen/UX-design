# External automatable-check registries — ingest notes

## axe-core (ingested 2026-07-14)

**Source:** [`axe-core`](https://github.com/dequelabs/axe-core) v4.12.1, MPL-2.0, via `npm install axe-core` + `axe.getRules()`.

**Why vendored, not fetched live at build time:** the rest of `knowledge/` builds fully offline/on-device (see `working-model-cloud-vs-device` memory — no network needed to regenerate the designer KB). Requiring `npm install` inside `_build_all.py` would break that. Instead the rule metadata is snapshotted once into `axe-core-rules-snapshot.json` (this directory) and the generator (`knowledge/compliance/_import_axe_rules.py`) reads the snapshot, same pattern as `knowledge/tokens/_raw/` (a manual Figma export, not a live API call).

**To refresh the snapshot** (new axe-core release, or want the latest rule set):

```bash
mkdir -p /tmp/axe-refresh && cd /tmp/axe-refresh
npm init -y >/dev/null && npm install axe-core
node -e "
const fs = require('fs');
const axe = require('axe-core');
const pkg = require('axe-core/package.json');
const rules = axe.getRules();
const out = {
  '\$description': 'Vendored snapshot of axe-core rule metadata...',
  source: 'axe-core', source_version: pkg.version,
  source_homepage: 'https://github.com/dequelabs/axe-core',
  snapshotted: new Date().toISOString().slice(0,10),
  rule_count: rules.length, rules: {},
};
for (const r of rules) out.rules[r.ruleId] = {description: r.description, help: r.help, helpUrl: r.helpUrl, tags: r.tags};
fs.writeFileSync('axe-core-rules-snapshot.json', JSON.stringify(out, null, 2));
"
cp axe-core-rules-snapshot.json <repo>/knowledge/compliance/_vendor/
python3 knowledge/compliance/_import_axe_rules.py
```

**How SC numbers are recovered from axe's tags:** axe-core tags SCs as `wcag` + digits with no separators (e.g. `wcag143` = 1.4.3, `wcag1412` = 1.4.12). WCAG's own numbering is principle (1 digit) . guideline (1 digit) . criterion (1–2 digits), so the split is deterministic: first digit = principle, second = guideline, remainder = criterion. No ambiguity table needed — verified against all 31 of our existing hand-typed SCs, 100% match.

**Coverage found:** axe-core's OSS rule set carries WCAG tags for 29 distinct SCs (of ~87 in WCAG 2.2). Cross-referencing against our 31-SC compliance graph: see `knowledge/_EXTERNAL-AUTOMATABLE-REFS.md` for the current breakdown of which of our SCs axe-core could help verify and which have no OSS axe coverage at all (still genuinely manual/bespoke).

## W3C ACT Rules Format — checked, NOT ingested this pass

Checked 2026-07-14: `act-rules.github.io/rules/` lists ~500+ individual rules, each with an "Accessibility Requirements Mapping" to specific SCs, but **no structured JSON/CSV/API export was found** — the rules page is HTML-only with client-side filtering, and there's no `act-rules` npm package (checked the registry) or a `_data/*.json` export in the linked GitHub repo that would give a clean one-shot ingest. Getting a machine-readable form would mean scraping ~500 individual rule pages (each is its own file with YAML-ish frontmatter) — a real scraping project, not a "cheap-now slice."

**Decision:** deferred, not silently dropped. If this becomes worth doing, the approach would be: clone `github.com/act-rules/act-rules.github.io`, parse the per-rule markdown files' frontmatter (`accessibility-requirements` field) directly from the repo rather than the rendered site — cheaper than scraping HTML, still a dedicated task.
