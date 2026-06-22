# Runbook — onboard a new code library (add a binding spoke)

The repeatable procedure for connecting the design canon to a **consuming code library**
(Sutherland React today; others later). Written 2026-06-22 (Dave decision) so the system — not
anyone's memory — knows what to do when a new library appears. Trigger: a new code library starts
consuming the toolkit, or an existing library's real component/variant names become knowable
(e.g. Code Connect gets wired, or the Sutherland JSON lands).

## The model — hub-and-spoke (read this first)

One design component can feed **many** code libraries, each built by different people with different
naming conventions. So there is **no single "formal name."** Instead:

- **HUB = the Figma node identity** (`provenance.figma_node`). The only library-independent key.
  Never renamed. Everything reconciles *through* it.
- **Display name = `$displayName` / `$aliases`** on each variant. Ours, human-facing, stable across
  every library (we own it). This is the friendly name (e.g. "Link card").
- **Figma name = the variant's `name`** (e.g. `basic`). Authoritative for the Figma namespace only.
- **Each code library = a SPOKE** under `codeBindings`, keyed by a library id (e.g. `sutherland-react`).
  Each spoke records *that library's own* component name + variant→prop mapping, which **may differ**
  from the Figma names and from every other library's.

Names map through the node; they are **never normalised to a winner** and **never bound to each other**.

## Steps — add a spoke for library `<lib-id>`

1. **Pick the library id** — short, stable, kebab-case (`sutherland-react`, `web-components`,
   `compose`, …). This is the `codeBindings` key.
2. **Get the real names from Code Connect — do not guess.** Run `get_code_connect_map` (Figma MCP)
   for the component's node. If Code Connect isn't wired for this library yet, leave the spoke with
   `$status: "unverified"` and TODOs; a guessed name is worse than an admitted gap.
3. **Record the component name** the library uses (it may not match Figma's `name`).
4. **Map every variant → the library's prop(s).** Name the selector prop (it may not be `type`) and
   give each Figma variant value its library value. Cover all variants in `props`/`variants`, even the
   ones not yet built as snippets.
5. **Tag confidence** per `_CONFIDENCE.md`: `$status` = `verified` (confirmed against repo / Code
   Connect) or `unverified` (placeholder). Add `$source` (e.g. "Code Connect map 2026-07-xx").
6. **Do not touch the hub or other spokes.** Adding library B never edits library A's names, the
   Figma `name`, or `$displayName`. If two libraries disagree, that's expected — both are recorded.
7. **Rebuild green** — `python3 knowledge/_build_all.py`. `codeBindings` is a first-class optional
   field in `meta.schema.json`; the schema gate validates the meta still parses.

## Invariants (don't violate)

- **Never bind logic, gates, or Code Connect on a `$displayName`/`$alias`.** Friendly names are
  presentation only. Bind on the node id (hub) and the library's own value (spoke).
- **Never normalise names across libraries.** Different libraries keep different names; the node
  reconciles them. Do not rename one library's component to match another's or to match Figma.
- **Never guess a code name.** Populate spokes from Code Connect / the repo. Unverified ⇒ say so.
- **The hub is immutable.** `provenance.figma_node` is the identity; if it changes, that's a new
  component, not a rename.
- **Display names are library-independent** and live once, per variant, on the meta.

## Companion

`_RUNBOOK-gated-component.md` (build the gated snippet) · `_CONFIDENCE.md` (asserted | inferred |
review | verified | unverified) · `meta.schema.json` → `codeBindings` (the contract) ·
README "Parked" (Sutherland migration timing). First spoke recorded: `components/cards.meta.json`.
