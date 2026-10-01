# First prompt for Copilot chat (agent mode)

Open Copilot chat in VS Code, switch it to Agent mode, make sure both this kit folder and Sutherland's repo are in the workspace, then paste everything between the lines.

---

Read `BRIEF-FOR-COPILOT.md` in the `sutherland-react` kit folder and follow it exactly. The job: fill `manifest.json` for every Apollo part listed in `parts.json` by reading the Sutherland React component library's own source in this workspace. Nothing is mapped yet: every Sutherland-side name is `null`, and the `$legacy` blocks on the first four rows are empty TODO placeholders, not hints. Rules you must keep: never guess a name you did not read in a Sutherland file; cite the Sutherland file path for every binding, prop and slot; a prop, slot, state, value or event with no Sutherland counterpart goes into that binding's `unmapped` block with a one-line reason; leave every `status` as `"unverified"`; copy no Sutherland source code into the output, names and types only; do not add, remove or rename any Apollo-side name.

Work part by part in the order of `parts.json`. After each part, run `python3 check_manifest.py manifest.json` in the kit folder and fix what it reports before moving on. When every part is done, fill the `library` block from Sutherland's `package.json` and `git rev-parse HEAD`, add Sutherland's token files under `tokens.resolver.sets.sutherland.sources`, and add `tokens.map` rows only for tokens you can place with confidence on an Apollo semantic token from `apollo-tokens.json`.

Finish by writing `FILL-NOTES.md` beside the manifest: which parts had no Sutherland counterpart and why, where Sutherland's tokens live, and anything you were unsure about. Then tell me the checker's final line.

---

If Copilot asks which folder is Sutherland's, point it at the repo root (the folder with Sutherland's `package.json`). If it starts writing code or a script to "automate" the mapping, stop it and tell it to read the files and fill the JSON by hand; the checker is the only script this job needs.
