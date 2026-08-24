# Photography → knowledge-graph mapping — what it WOULD need (PRICED, NOT BUILT)

**Status: NOT BUILT, and deliberately so.** #211 owes a KG mapping for the photography set
(*"they will need to be mapped and added to the KG"*, Dave). The #217 build sub that produced the
manifest was fenced from making KG schema decisions, so this file records what such a mapping
would require and what it would cost — nothing here is a schema, a ruling, or a proposal Dave has
seen. Written at #217 under `s217-D1`.

## What already exists to hang it on

| surface | address | state |
|---|---|---|
| committed manifest, 251 rows | `knowledge/_PHOTOGRAPHY-MANIFEST.json` (+ `.md`) | BUILT #217 |
| committed web derivatives | `knowledge/assets/photography-web/` | BUILT #217, 12 files |
| originals | `knowledge/assets/photography/` | NON-REPO (`.gitignore`, #211) |
| generator | `knowledge/_build_photo_manifest.py` | BUILT #217, `--check` + `--selftest` green |
| first consumers, named by Dave | Image-block · Carousel | specimens BUILT #217, see below |

The manifest's JSON row IS the node payload a KG would point at: `filename`, `width`, `height`,
`orientation`, `exif_description`, `licence_source`, `licence_source_basis`, `licensor_url`,
`derivative`. Every field already states its own provenance, and absence is `null`, never a
default — so a KG built on it inherits an honest UNKNOWN rather than a fabricated value.

## What a mapping would need — the five open questions, none of them answered here

1. **Node identity.** Is the node the ORIGINAL (which is non-repo and may never be committed) or
   the DERIVATIVE (committed, but only 12 of 251 exist and the set grows only as photos are used)?
   These give different graphs: original-as-node means 239 nodes point at files no clone has;
   derivative-as-node means the graph cannot see 95% of the library. A third answer — the
   MANIFEST ROW as the node, with the original and derivative as attributes — is the one the
   manifest's shape already favours, but it is not chosen here.
2. **Edge vocabulary to consumers.** Dave named Image-block and Carousel. An edge
   `photo -[used_by]-> component` is the obvious first form; whether it points at the COMPONENT
   or at a specific SPECIMEN PAGE (`knowledge/_fitness-test/photography-*-v1.html`) is a real
   choice — the component is stable, the specimen is versioned and will be superseded.
3. **Tagging.** UNRULED (#211 owed item 3). 245 of 251 files carry an EXIF description, which is
   the free seed, but turning descriptive prose into tags is exactly the taxonomy decision that
   has not been made. Any KG that adds a `tag` edge type has silently made it.
4. **Licence as a first-class thing or a string.** `licence_source` today is a string
   (`"Getty Images"`, `"Kike Arnaiz / Stocksy United"`, an EyeEm copyright line). A KG could
   promote each licensor to a node and hang `licensor_url` / `web_statement` off it — useful the
   moment anyone asks "what can we actually publish?", and unnecessary before then.
5. **Where the graph lives.** `knowledge/_validate_kg.py` and the existing graph builders already
   define a shape for this repo; a photography mapping should join that shape rather than invent
   a second one. Nobody has checked whether they can carry 251 asset nodes — that check is part
   of the price below, not a claim made here.

## Price (estimate, and an estimate is not a measurement)

- **Answering the five questions with Dave: one sitting.** Q1 and Q3 are the load-bearing ones;
  Q2/Q4/Q5 follow from them.
- **Building the mapping once answered: small.** The manifest is already machine-readable and
  regenerable, so the mapping is a projection, not a data-entry job. The risk is not volume, it
  is committing to a node identity that the future hosted image store (NOTED-FUTURE in `s217-D1`,
  not ruled) would immediately invalidate — which is the strongest argument for taking Q1
  seriously before writing any edges.

## What would INVALIDATE this note

If Dave rules the hosted cloud image store, Q1 is answered from outside (the node becomes the
store's asset id) and most of this file is superseded. If he rules a tagging approach, Q3 closes
and Q2's edge set widens. Either ruling should be checked before anyone builds from this page.
