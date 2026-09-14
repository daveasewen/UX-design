# SCHEMA DIFF — the four DESK edge types (#270 lane 1, PROPOSAL ONLY)

⛔ **NOTHING HERE IS APPLIED.** A new edge type is a closed-vocabulary change (#75): this lane
proposes the diff, Dave ratifies, then `gen_kg_roles_desk.py --land --ratified sNNN-DN` lands it.
Every hunk below was applied to a **scratch copy** and re-validated — see `VALIDATE-RECEIPT.md`.

There are **four** files in the change. Only the first is `meta.schema.json`.

---

## 1. `knowledge/components/meta.schema.json` — the edge-type enum (`properties.edges.properties`)

```diff
--- a/knowledge/components/meta.schema.json
+++ b/knowledge/components/meta.schema.json
@@ properties.edges.properties @@
         "drivesConsumer": {
           "type": "array",
           "items": { "$ref": "#/definitions/edge" }
         },
+        "providesRole": {
+          "type": "array",
+          "items": { "$ref": "#/definitions/edge" },
+          "description": "s270-Dn (enacting s269-D1 item 1). The ROLE this component fills — the slot a composer asks for (`wants: <role>`) and this component answers (`provides: <role>`). ONE HOME, generation chain not copy chain: the edge is DERIVED from this meta's own top-level `provides` by knowledge/gen_kg_roles_desk.py, resolved against knowledge/roles.json (the address set is the fence — a thirteenth role is Dave's ruling, s252-D1, never a lane's drift). The `providers` lists inside roles.json remain a MEMBERSHIP CROSS-CHECK and are NOT a source: they carry 108 entries where the metas carry 24 (ROLES-DRIFT.md). Never authored by hand; never copied back into roles.json."
+        },
+        "answersIntent": {
+          "type": "array",
+          "items": { "$ref": "#/definitions/edge" },
+          "description": "s270-Dn (enacting s269-D1 item 1). The QUESTION this component answers for the reader — the function face of FFF. DERIVED from this meta's own top-level `answers` (s251-D11: the chart `intent` word extended to every component), resolved against knowledge/chart-intents.json. A component whose purpose genuinely spans two words carries two edges, in the meta's own order. A sixth chart word, or a new non-chart word, is Dave's ruling on a review page, never a lane's."
+        },
+        "hasDataShape": {
+          "type": "array",
+          "items": { "$ref": "#/definitions/edge" },
+          "description": "s270-Dn (enacting s269-D1 item 1). The DATA SHAPE this component takes — the second face of FFF, `<x-dimension> × <mark>`. DERIVED from this meta's own top-level `shape`, resolved against knowledge/shapes.json (CLOSED by s254-D2 item 1). Two components sharing a shape value are declaring themselves candidates to swap, which is exactly what the resolver's `instead-of` grade compares: the edge makes that claim readable in the graph instead of only in the resolver."
+        },
+        "yieldsTo": {
+          "type": "array",
+          "items": { "$ref": "#/definitions/edge" },
+          "description": "s270-Dn (enacting s269-D1 item 1). The sibling this component STANDS DOWN FOR, and the test. DERIVED from the PROSE half of this meta's own `when` — the beats/yields sentence after the first em-dash (s253-D1; when-fields.json $grammar: the prose half is never parsed by the gate, and this is the one consumer that reads it). Only `yields to X` produces an edge: `beats Y` is Y's fact, not this component's, and an edge lives on the meta that declares it — the inverse is read by traversing the graph, never by writing a second edge into a second meta. An anaphoric target (\"yields to it\", \"yields to both\") is ref:null + $note, declared and never guessed."
+        },
         "$contract": {
```

*(Anchor lines are illustrative — the four keys are appended to `properties.edges.properties`;
`additionalProperties: false` on `edges` is what makes this addition load-bearing, and `_validate_kg.py`
check (d) reads the enum straight out of this file, so no second list needs touching.)*

## 2. `knowledge/components/meta.schema.json` — the node-id grammar (`definitions.edge.properties.ref.pattern`)

```diff
@@ definitions.edge.properties.ref @@
-          "pattern": "^(component|pattern|context|snippet|ruling):.+$"
+          "pattern": "^(component|pattern|context|snippet|ruling|role|intent|shape):.+$"
```

and the prose in `definitions.edge.description` + `properties.edges.description`, which both spell
the grammar out longhand:

```diff
-ref is a node-id ('component:<stem>' | 'pattern:<slug>' | 'context:<slug>' | 'snippet:<filename>' | 'ruling:<sNNN-DN>')
+ref is a node-id ('component:<stem>' | 'pattern:<slug>' | 'context:<slug>' | 'snippet:<filename>' | 'ruling:<sNNN-DN>' | 'role:<slug>' | 'intent:<word>' | 'shape:<value>')
```

## 3. `knowledge/_validate_kg.py` — the resolver (three constants, one dict)

```diff
-REF_RE = re.compile(r"^(component|pattern|context|snippet|ruling):.+$")
-NODE_KINDS = ("component", "pattern", "context", "snippet", "ruling")
+REF_RE = re.compile(r"^(component|pattern|context|snippet|ruling|role|intent|shape):.+$")
+NODE_KINDS = ("component", "pattern", "context", "snippet", "ruling", "role", "intent", "shape")
+ROLES = HERE / "roles.json"
+INTENTS = HERE / "chart-intents.json"
+SHAPES = HERE / "shapes.json"
+
+
+def store_ids(path, key, prefix):
+    """role:/intent:/shape: resolve against the STORE, not a registry file — the
+    store is already the ONE home (ADR-0017 write-once) and a _nodes-role.json
+    would be a second one."""
+    if not path.exists():
+        return set()
+    vocab = json.loads(path.read_text(encoding="utf-8"))[key]
+    return {f"{prefix}:{k}" for k in vocab}
@@ validate_corpus, resolvers dict @@
         "ruling": ruling_ids(rulings_path),
+        "role": store_ids(roles_path or ROLES, "roles", "role"),
+        "intent": store_ids(intents_path or INTENTS, "chart-intent", "intent"),
+        "shape": store_ids(shapes_path or SHAPES, "shapes", "shape"),
     }
```

**Why no new registry file.** `_nodes-pattern.json` / `_nodes-context.json` exist because pattern and
context nodes have no other home. Roles, intents and shapes already have one each, with a resolver
apiece (`_validate_roles_resolve.py`, `_validate_intent_resolve.py`). Minting `_nodes-role.json`
would create the exact second home ADR-0017 forbids and roles.json's own `$description` names as the
fence. **Recommendation: resolve against the three stores; add no registry files.**

## 4. `knowledge/_kg_explorer.template.html` — three colour variables

The explorer needs no code change (`_build_kg_explorer.py:extract()` types a node by its id prefix,
so `role:` / `intent:` / `shape:` nodes appear with no edit — measured: 890→935 nodes, 1267→1382
edges on the landed scratch). But the template paints a node from `--c-<type>`, and three vars are
missing, so the new nodes would render with an undefined colour in all three theme blocks:

```diff
@@ _kg_explorer.template.html:11 (light) and :22, :29 (dark) @@
-  --c-component:#DA1A00;--c-snippet:#7A7A7A;--c-pattern:#1F4FBF;--c-context:#0E8A5F;--c-ruling:#111111;
+  --c-component:#DA1A00;--c-snippet:#7A7A7A;--c-pattern:#1F4FBF;--c-context:#0E8A5F;--c-ruling:#111111;
+  --c-role:#8A4FBF;--c-intent:#B07A00;--c-shape:#0E6F8A;
```

Hues are a **proposal, not a ruling** — they must clear the two-red law (s151-D1: red is
`#DA1A00` on white / `#F6604C` elsewhere, and nothing else may read as red) and be checked per theme
(four themes, tested per theme). Dave's call, or the art director's.

---

## What does NOT change

- `knowledge/gen_kg_edges.py` — **no edit needed.** `merge_edges` (s268-D6 (c)) starts from the
  meta's own `edges` and refreshes only the derived types, so the four new types are carried
  byte-for-byte. Measured on the landed scratch: `gen_kg_edges.py` re-run → **0 files drifted**
  (`_validate_kg.py` check (e) idempotence holds).
- `knowledge/roles.json`, `chart-intents.json`, `shapes.json`, `when-fields.json` — read only.
  No value is added to any vocabulary by this lane.
- `_nodes-pattern.json`, `_nodes-context.json` — untouched.
- `_kg_history.py` — no edit; it reads the built graph.
