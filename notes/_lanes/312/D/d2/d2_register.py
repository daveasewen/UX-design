#!/usr/bin/env python3
"""#311 overnight lane D2 — s308-D22 + s308-D27 (item 7: the outside term, the neatest name wins) and
s308-D23 (item 8: the two ruling-to-ruling vocabularies folded into one) written into
knowledge/_edge_register.json. Run once from the repo root; it rewrites the register in the file's own form
(indent 1, ensure_ascii False) and prints what moved. Idempotent: a second run changes nothing.

Grades are the research page's word map (notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v2.html §05,
"How close each match is was my judgement, made by reading both definitions"), re-pointed by s308-D27's order:
a design-system vocabulary first (Canonical ds:/dt:, Spectrum) where one covers the type, SKOS, Dublin Core or
PROV otherwise; where none of those fits, the page's own nearest term stays and says so.
"""
import json

REG = 'knowledge/_edge_register.json'
reg = json.load(open(REG, encoding='utf-8'))

C, SP, SK, DC, PR = 'Canonical ds:', 'Spectrum', 'SKOS', 'Dublin Core', 'PROV'
OT = 'other (none of the design-system vocabularies, SKOS, Dublin Core or PROV covers it)'
# word: (term, vocabulary, grade, also)
T = {
    'acceptsCapability': ('consumesApi', 'Backstage', 'close', [], OT),
    'activeVariantOf': ('ds:variantOf', C, 'close', ['Dublin Core isVersionOf'], None),
    'answersIntent': ('responds-to', 'IBIS', 'loose', [], OT),
    'appliesTo': ('dcterms:conformsTo, walked back', DC, 'close', [], None),
    'behaviourFrom': ('prov:wasDerivedFrom', PR, 'close', ['prov:hadPrimarySource'], None),
    'bindsToken': ('ds:hasTokenBinding', C, 'close', ['Spectrum tokenBindings'], None),
    'boundBy': ('dcterms:conformsTo', DC, 'close', ['dcterms:source'], None),
    'bounds': ('overrides / subsumes', 'Kruchten', 'loose', [], OT),
    'capturedFrom': ('prov:hadPrimarySource', PR, 'close', ['prov:wasDerivedFrom'], None),
    'challengedBy': ('objects-to', 'IBIS', 'close', [], OT),
    'checkedBy': ('a SHACL shape or W3C ACT rule that checks it', 'SHACL / ACT', 'close', [], OT),
    'cites': ('dcterms:references', DC, 'exact', [], None),
    'commonPattern': ('skos:related (a pattern language’s related patterns)', SK, 'loose', [], None),
    'composedOf': ('dcterms:hasPart', DC, 'close', ['Atomic Design composition'], None),
    'confirms': ('enables', 'Kruchten', 'loose', ['IBIS supports'], OT),
    'consumes': ('dcterms:requires', DC, 'close', ['Backstage consumesApi'], None),
    'containedBy': ('ds:parentComponent', C, 'exact', ['dcterms:isPartOf'], None),
    'corrects': ('replaces', 'IBIS', 'loose', [], OT),
    'defaultActive': ('a Wikidata qualifier (the theme)', 'Wikidata', 'close', [], OT),
    'defaultFor': ('a Wikidata qualifier (the theme)', 'Wikidata', 'close', [], OT),
    'definedIn': ('rdfs:isDefinedBy', 'RDFS', 'exact', [], None),
    'delegatesTo': ('aria-controls / aria-haspopup', 'WAI-ARIA', 'loose', [], OT),
    'drivesConsumer': ('aria-controls', 'WAI-ARIA', 'close', [], OT),
    'enacts': ('enables / comprises', 'Kruchten', 'loose', [], OT),
    'enClause': ('dcterms:source', DC, 'close', ['dcterms:conformsTo'], None),
    'enforcedBy': ('a SHACL shape or W3C ACT rule that checks it', 'SHACL / ACT', 'close', [], OT),
    'evidencedBy': ('prov:hadPrimarySource', PR, 'close', [], None),
    'explainedBy': ('supports', 'IBIS', 'close', [], OT),
    'extends': ('enables / comprises', 'Kruchten', 'loose', ['IBIS replaces'], OT),
    'family': ('skos:related', SK, 'loose', [], None),
    'flaggedBy': (None, None, None, [], 'none found: the page’s word map names no outside term (Apollo’s own)'),
    'governedBy': ('traces to, walked back', 'Kruchten', 'close', [], OT),
    'governs': ('traces to', 'Kruchten', 'close', [], OT),
    'groupsWith': ('skos:related', SK, 'close', [], None),
    'hasDataShape': (None, None, None, [], 'none found: the page’s word map names no outside term (Apollo’s own)'),
    'hasPart': ('ds:hasSubcomponent', C, 'exact', ['dcterms:hasPart'], None),
    'hasParty': ('n-ary relation, pattern 1', 'W3C n-ary relations note', 'exact', [], OT),
    'inFamily': ('skos:broader', SK, 'close', ['skos:inScheme'], None),
    'inGroup': ('skos:inScheme', SK, 'close', [], None),
    'mentions': ('dcterms:references', DC, 'exact', [], None),
    'mustNotNeighbour': ('sh:disjoint', 'SHACL', 'loose', ['Kruchten forbids'], OT),
    'narrows': ('overrides / subsumes', 'Kruchten', 'loose', [], OT),
    'obeys': ('dcterms:conformsTo', DC, 'close', [], None),
    'partial': ('ds:inheritsFrom', C, 'close', ['dcterms:isVersionOf'], None),
    'providesRole': ('providesApi', 'Backstage', 'close', [], OT),
    'refines': ('overrides / subsumes', 'Kruchten', 'loose', [], OT),
    'renderedBy': ('ds:implementsBlock, walked back', C, 'close', ['UI ontology realizes'], None),
    'resolvedBy': ('responds-to', 'IBIS', 'close', [], OT),
    'restsOn': ('supports', 'IBIS', 'close', [], OT),
    'retires': ('dcterms:replaces', DC, 'loose', ['IBIS replaces'], None),
    'reuses': ('dcterms:requires', DC, 'close', [], None),
    'ruledIn': ('prov:wasGeneratedBy', PR, 'exact', [], None),
    'setIn': ('the design-token typography composite', 'DTCG design tokens', 'close', [], None),
    'supersedes': ('dcterms:replaces', DC, 'exact', ['ADR superseded'], None),
    'supersedesClause': ('dcterms:replaces (one clause)', DC, 'close', ['ADR superseded'], None),
    'tensionWith': ('skos:related', SK, 'loose', ['QOC trade-off'], None),
    'touches': ('responds-to', 'IBIS', 'close', [], OT),
    'triggeredBy': ('aria-controls, walked back', 'WAI-ARIA', 'loose', [], OT),
    'under': ('skos:broader', SK, 'exact', [], None),
    'usedInContext': ('required context', 'WAI-ARIA', 'loose', [], OT),
    'usesIcon': ('dcterms:requires', DC, 'close', [], None),
    'usesLogo': ('dcterms:requires', DC, 'close', [], None),
    'verifiedBy': ('a SHACL shape or W3C ACT rule that checks it', 'SHACL / ACT', 'close', [], OT),
    'yieldsTo': ('is an alternative to (with precedence)', 'Kruchten', 'loose', [], OT),
}
# s308-D27: the neatest name wins. Where Apollo's word already IS the outside word, or reads plainer at no loss,
# it stays; adoption is taken where the outside term is the neater label. None is neater tonight (reasons below).
SAME = {'hasPart': 'dcterms:hasPart / ds:hasSubcomponent', 'supersedes': 'ADR superseded / dcterms:replaces',
        'definedIn': 'rdfs:isDefinedBy', 'cites': 'dcterms:references', 'mentions': 'dcterms:references',
        'hasParty': 'the n-ary pattern’s own word', 'under': 'skos:broader'}
D27 = ("s308-D27 (Dave 2026-09-29 12:13 BST, 'Lets do what is neatest, and if changes my answer thats fine, "
       "I don't like patches more than my preference for ango-saxon')")


def name_for(w, term, grade):
    if w in SAME:
        b = (f"kept: Apollo's word already says what {SAME[w]} says, as a plain word; adopting the prefixed term "
             "would rename storage for no gain in meaning")
    elif grade == 'exact':
        b = "kept: an exact match, and Apollo's word is the plainer label"
    elif grade in ('close', 'loose'):
        b = (f"kept: the outside term is {grade}, not the same relation, so adopting it as the name would say "
             "something the edge does not; the term is written beside it")
    else:
        b = "kept: no outside term exists; the word is Apollo's own"
    return {'word': w, 'adopted': False, 'basis': b + ' (' + D27 + ').'}


moved = 0
for row in reg['types']:
    w = row['word']
    term, vocab, grade, also, why = T[w]
    old = row.get('outside') or {}
    row['outside'] = {
        'term': term, 'vocabulary': vocab, 'grade': grade, 'also': also,
        **({'note': why} if why else {}),
        'candidates': old.get('candidates', []),
        'name': name_for(w, term, grade),
        'basis': ("s308-D22 + s308-D27 (#311 lane D2): the word map's grade on notes/_RESEARCH-308-design-system-"
                  "ontologies-2026-09-29-v2.html §05, re-pointed design-system vocabulary first, then SKOS, Dublin "
                  "Core or PROV"),
    }
    moved += 1

# s308-D23 — item 8: the older decision graph's nine types folded onto the ruling-edges vocabulary
reg['$folded'] = {
    'what': ("s308-D23 (Dave 2026-09-29 09:26 BST, '8. Fold the two ruling-to-ruling vocabularies into one — "
             "Take it'). knowledge/_decision-graph.json (the older decision graph: ADR, R-D, dv-, icon-, DEF- records) "
             "spelled its ruling-to-ruling links in nine types; knowledge/_ruling_edges.json spells them in ten. ONE "
             "vocabulary is read: each older type is mapped here onto a register row (with `reverse` when the older "
             "spelling points the other way), retired into one, or — where no match exists — brought forward as "
             "a proposal in `$proposed`. knowledge/_validate_edges.py --coverage refuses an older type this map does "
             "not name (FOLD-MISSING) and a map target with no register row or proposal (FOLD-DANGLING)."),
    'source': 'knowledge/_decision-graph.json edges[].type',
    'types': {
        'refines': {'to': 'refines', 'grade': 'exact', 'basis': 'the same word, the same direction'},
        'supersedes': {'to': 'supersedes', 'grade': 'exact', 'basis': 'the same word, the same direction'},
        'bounds': {'to': 'bounds', 'grade': 'exact', 'basis': 'the same word, the same direction'},
        'enacted-by': {'to': 'enacts', 'reverse': True, 'grade': 'exact',
                       'basis': "two spellings of one idea (the ruling's own example): A enacted-by B is B enacts A"},
        'relates': {'to': 'mentions', 'grade': 'close',
                    'basis': 'an untyped pointer from one record to another, which is what mentions carries'},
        'subsumes': {'to': 'extends', 'grade': 'close',
                     'basis': "its one line (R-D6.A2 subsumes icon-015's amber exemption) takes the older claim into "
                              "the later ruling, which is what extends says"},
        'verified-by': {'to': 'verifiedBy', 'grade': 'close',
                        'basis': 'a record checked by a gate or another record; the register row verifiedBy says it '
                                 'for a criterion, so this widens its start if these lines ever enter the graph'},
        'conflicts-with': {'to': 'conflictsWith', 'proposal': True, 'grade': None,
                           'basis': 'no match in the ten: brought forward as a proposal (s308-D23 names it, 8 older '
                                    'lines use it, Kruchten names it too)'},
        'diverges-from': {'to': 'divergesFrom', 'proposal': True, 'grade': None,
                          'basis': 'no match in the ten: brought forward as a proposal (1 older line, DEF-006 from '
                                   'DEF-005: a deliberate difference, ruled "do not reconcile")'},
    },
    'later': ("'depends on' (Kruchten's constrains: if this ruling is retired the other falls with it) is noted for "
              "later, not built (s308-D23: 'A second one is worth considering later')."),
}
reg['$proposed'] = {
    'what': ("Edge types brought forward as PROPOSALS (s308-D23: 'Where no match exists, bring the older type forward "
             "as a proposal'). Not rows: no edge of them is in the graph, the ends check does not read them, and "
             "_validate_edges.py --coverage refuses any edge that uses one (PROPOSED-HAS-EDGES) until it is made a "
             "row."),
    'types': {
        'conflictsWith': {'from': ['ruling'], 'to': ['ruling'], 'plain': 'conflicts with',
                          'shape': {'self': False, 'loops': True, 'bothWays': True, 'chains': False},
                          'why': {'required': True, 'floor': None},
                          'outside': {'term': 'conflicts with', 'vocabulary': 'Kruchten', 'grade': 'exact'},
                          'older': {'type': 'conflicts-with', 'lines': 8, 'file': 'knowledge/_decision-graph.json'}},
        'divergesFrom': {'from': ['ruling'], 'to': ['ruling'], 'plain': 'deliberately differs from',
                         'shape': {'self': False, 'loops': True, 'bothWays': True, 'chains': False},
                         'why': {'required': True, 'floor': None},
                         'outside': {'term': None, 'vocabulary': None, 'grade': None},
                         'older': {'type': 'diverges-from', 'lines': 1, 'file': 'knowledge/_decision-graph.json'}},
    },
}
F = reg['$schema']['fields']
F['outside'] = ("s308-D22 + s308-D27: the nearest outside term (`term`, its `vocabulary`), graded `exact`, `close` "
                "or `loose` (SKOS's three), pointing first at a design-system vocabulary (Canonical ds:/dt:, "
                "Spectrum), then SKOS, Dublin Core or PROV; `also` other near terms; `note` where only another "
                "vocabulary fits; `name` the neatest-name decision (s308-D27: the outside term adopted outright "
                "where neater, `adopted` true). CHECKED by _validate_edges.py: a row without `outside`, or with "
                "a grade outside the three, is REGISTER-SHAPE.")
reg['$schema']['rulings']['s308-D22'] = 'item 7 — `outside` per row (#311 lane D2)'
reg['$schema']['rulings']['s308-D27'] = 'item 7 v2 — the neatest name wins; `outside.name` per row (#311 lane D2)'
reg['$schema']['rulings']['s308-D23'] = 'item 8 — `$folded` + `$proposed` (#311 lane D2)'
d = reg.get('$doc') or {}
if isinstance(d.get('owed'), dict):
    d['owed'].pop('item 8 (s308-D23)', None)

with open(REG, 'w', encoding='utf-8') as f:
    f.write(json.dumps(reg, indent=1, ensure_ascii=False) + '\n')
g = {}
for r in reg['types']:
    g[r['outside']['grade']] = g.get(r['outside']['grade'], 0) + 1
print('outside written', moved, '· grades', g, '· adopted', sum(r['outside']['name']['adopted'] for r in reg['types']),
      '· folded', len(reg['$folded']['types']), '· proposed', list(reg['$proposed']['types']))
