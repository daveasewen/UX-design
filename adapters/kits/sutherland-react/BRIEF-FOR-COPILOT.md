# Brief for the Copilot agent — fill the Apollo adapter manifest for Sutherland React

You are working in VS Code with GitHub Copilot in agent mode. This folder is a kit. Sutherland's source (the HSBC React component library) is open beside it in the same workspace. The Apollo repo is NOT here and you do not need it.

## What Apollo is, in two lines

Apollo is a governed design-system engine: a set of component specs (parts) with props, slots, states and tokens, checked by gates. It governs; a client's library renders. This manifest is how Apollo learns which Sutherland component renders each Apollo part.

Apollo has no Sutherland mapping yet. Every Sutherland-side name in `manifest.json` is `null` because none has been read; you are starting from nothing on the Sutherland side.

## The job

Fill `manifest.json` for every part listed in `parts.json` by READING Sutherland's own source: its component files, their props (TypeScript types or PropTypes), their children and render props, and their token or theme files. Write names and types only. Hand back one file: `manifest.json`.

## The rules — read these before you touch the file

1. Never guess. A name you did not read in a Sutherland source file does not go in the manifest. If you cannot find a match, the Apollo prop, slot, state, value or event goes into that binding's `unmapped` block with a one-line reason. An honest gap is worth more than a plausible name.
2. Cite the source. Every binding has a `source` field and every prop and slot row has one too: the Sutherland file path, relative to Sutherland's repo root, where you read the name. `theirs.file` carries the component's own file.
3. Status stays `"unverified"`. You never set `rendered` or `accepted`; those need a side-by-side render on record and Dave's word, which happen in Apollo.
4. No Sutherland source code goes into the output. Names, types and file paths only. Do not paste implementations, JSX, comments or licence text.
5. Do not add, remove or rename Apollo-side names. The `apollo` fields, the `hole` types and the `values` keys came from Apollo's metas. You fill the Sutherland side (`theirs`, `import`, `file`, `export`, the right-hand side of `values`, `states`, `events`, `source`). One exception: when a part takes content and `parts.json` lists no slot for it, you may add a single slot row `{"apollo": "children", "theirs": "<their name>", "kind": "children"}`.
6. Do not invent a Sutherland component to cover an Apollo part. If Sutherland has no counterpart for a part (for example no metric tile), leave that binding's `theirs.component` as `null`, set `source` to the file(s) you searched, and say in `$notes` what you looked for and where. Do not move it to the top-level `unmapped` list; that list is Apollo's.
7. Never normalise names. Sutherland's names are Sutherland's; write them exactly as exported. If a prop is called `variant` where Apollo says `type`, the row reads `"apollo": "type", "theirs": "variant"`.

## Step by step

1. Open `parts.json`. Each entry is one Apollo part: `slug`, `role`, `purpose`, `props` (each with the `hole` it becomes), `slots`, `states`, `events`, `variants`. The first four (cards, list-items, status-indicator, table) once had empty placeholder slots in Apollo; the rest are cohort one. The order means nothing more than that. `askedAs` shows the name Dave used when it differs from the slug.
2. Open `manifest.json`. Every part in `parts.json` has an empty row under `bindings`, with every Sutherland-side name set to `null`. The first four rows also carry a `$legacy` block: the old placeholder, every field reading TODO. It names no Sutherland component and is not a hint; ignore it and leave it as it is. You fill nulls; you do not add bindings for parts that are not in `parts.json`.
3. For each binding, in order:
   a. Find the Sutherland component that renders this part. Search Sutherland's `src` for the Apollo name, its variants and its purpose words. Read the component file and its types file.
   b. Fill `theirs.component` (the exported name), `theirs.import` (the specifier an app would import from, e.g. the package name or a subpath), `theirs.export` (`"named"` or `"default"`), `theirs.file` (the source file), and `source` (the file(s) you read, comma-separated if several).
   c. Props. For each row in `props`, set `theirs` to the Sutherland prop name and `source` to the file that declares it. Check the `hole`: `boolean` means TRUE renders their prop and FALSE renders nothing; `enum` means Apollo's value is looked up in `values`, so fill each value's right-hand side with Sutherland's value (`"primary": "primary"`, `"tertiary": "outline"`). An Apollo value Sutherland cannot express stays `null` AND is listed under the binding's `unmapped.values` with a reason. A prop with no Sutherland counterpart: leave `theirs` as `null` AND add it to `unmapped.props` with a reason.
   d. Slots. For each row in `slots`, set `theirs` (a prop name, a named slot, or `"children"`) and `kind` (`"children"`, `"prop"` or `"slot"`). No counterpart: `unmapped.slots` with a reason.
   e. States. Add a `states` object: each Apollo state name from `parts.json` maps to how Sutherland shows it (a prop like `disabled`, an attribute, a class name). No counterpart: `null` here AND a row in `unmapped.states`.
   f. Events. Add an `events` object only when `parts.json` lists events for the part: each Apollo event name maps to Sutherland's handler prop (`onChange`). No counterpart: `null` AND `unmapped.events`.
   g. Leave `status` as `"unverified"`. Do not add `evidence`.
4. Tokens. Find Sutherland's token or theme source (a `tokens` folder, a theme object, CSS custom properties, a Style Dictionary build). Add one `{"$ref": "<their file path>"}` per file under `tokens.resolver.sets.sutherland.sources`. Then, for each Sutherland token you can place with confidence, add a row to `tokens.map`: `theirs` (their exact name), `apollo` (an Apollo semantic token written as `{path}` from `apollo-tokens.json`, for example `{text.default}` or `{gap.component.m}`), `status: "unverified"`, `source`. Map at the semantic tier only: the checker refuses `{color.*}` palette paths. When you are not confident, do not add the row.
5. Fill `library`: `package` (from Sutherland's `package.json` name), `version` (its version), `source.repo` (the repo URL or local path), `source.commit` (the checked-out commit, `git rev-parse HEAD`), `source.readOn` (today, `YYYY-MM-DD`). Set `manifest.written` to today and `manifest.by` to `"GitHub Copilot agent on Dave's work machine"`.
6. Run the checker (below) until it prints `PASS`. Fix what it names. Do not silence a problem by deleting the Apollo-side row that caused it.
7. Write a short `FILL-NOTES.md` beside the manifest: which parts had no counterpart, where Sutherland's tokens live, and anything you were unsure about. Plain sentences, no code.

## How to run the checker

Open a terminal in this folder and run:

```
python3 check_manifest.py manifest.json
```

It needs only Python 3 (standard library, nothing to install) and the other files in this folder. `PASS` with the counts means the file is well-formed and complete by Apollo's rules. `FAIL` lists each problem with its path into the JSON, for example `$.bindings[3].props[1]: an enum hole needs a values map`. Exit code 0 is pass, 1 is fail.

## What to hand back

One file: `manifest.json`, passing the checker, plus `FILL-NOTES.md`. Nothing else in this folder needs to change.

## The shape, in one example

```json
{
  "apollo": { "meta": "button" },
  "theirs": { "component": "Button", "import": "@hsbc/sutherland-react", "export": "named", "file": "src/components/Button/Button.tsx" },
  "props": [
    { "apollo": "type", "theirs": "variant", "hole": "enum",
      "values": { "primary": "primary", "secondary": "secondary", "tertiary": "outline", "quaternary": null },
      "source": "src/components/Button/Button.types.ts" },
    { "apollo": "state", "theirs": null, "hole": "enum",
      "values": { "default": null, "hover": null, "pressed": null, "disabled": null, "processing": null, "success": null },
      "source": "src/components/Button/Button.types.ts",
      "$notes": "Sutherland has no state prop; the states are carried under `states` below" },
    { "apollo": "size", "theirs": "size", "hole": "enum", "values": { "default": "medium", "large": "large" }, "source": "src/components/Button/Button.types.ts" },
    { "apollo": "surface", "theirs": null, "hole": "enum", "values": { "on-light": null, "on-dark": null }, "source": "src/components/Button/Button.types.ts" },
    { "apollo": "label", "theirs": "children", "hole": "string", "source": "src/components/Button/Button.tsx" }
  ],
  "slots": [],
  "states": { "default": "none", "hover": "css :hover", "pressed": "css :active", "disabled": "disabled", "processing": null, "success": null },
  "unmapped": {
    "props": [ { "apollo": "state", "reason": "no state prop; states are CSS pseudo-classes and the disabled prop" },
               { "apollo": "surface", "reason": "no on-dark variant on Button" } ],
    "values": [ { "apollo": "type", "value": "quaternary", "reason": "Button.types.ts declares primary | secondary | outline only" } ],
    "states": [ { "apollo": "processing", "reason": "no loading state on Button" },
                { "apollo": "success", "reason": "no success state on Button" } ]
  },
  "status": "unverified",
  "source": "src/components/Button/Button.tsx, src/components/Button/Button.types.ts"
}
```

The Apollo-side names in this example are button's real ones from `parts.json`; the Sutherland-side names are illustrative and yours come from Sutherland's files.
