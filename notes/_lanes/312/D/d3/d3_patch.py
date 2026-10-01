"""#311 lane D3 — patch the explorer builder and template for s308-D28 (five edges, theme + aria node kinds)."""
import re
B = 'knowledge/_build_kg_explorer.py'
T = 'knowledge/_kg_explorer.template.html'
b = open(B, encoding='utf-8').read()
t = open(T, encoding='utf-8').read()


def rep(s, a, z, n=1):
    assert s.count(a) == n, (a[:70], s.count(a))
    return s.replace(a, z)


b = re.sub(r'^VERSION = "1\.36"  # ', 'VERSION = "1.37"  # 1.37 (#311 overnight lane D3, s308-D28 — Dave 2026-09-29 12:13 BST: "9. Five edges the outside world has and Apollo lacks Changed in v2 — Take it") pass E4 reads knowledge/_standard_nodes.json (gen_kg_standards.py): aliasOf, providesCapability, ariaRole, replacedBy, and the theme and aria node kinds; a defaultFor null carrying a theme now points at theme:<it>. 1.36 ', b, count=1, flags=re.M)
assert 'VERSION = "1.37"' in b
b = rep(b, """SOURCE_DRAWN = ('setIn', 'behaviourFrom', 'capturedFrom', 'acceptsCapability')
""", """SOURCE_DRAWN = ('setIn', 'behaviourFrom', 'capturedFrom', 'acceptsCapability')

# 1.37 (#311 overnight lane D3, s308-D28) — THE FIVE EDGES THE OUTSIDE WORLD HAS: knowledge/_standard_nodes.json,
# landed by gen_kg_standards.py. Each edge carries its own `fam` (tokens / sources / guidelines / structure) and
# its own `maker`; theme:<id> nodes join the assets family, aria:<role> nodes the guidelines family.
STANDARD_FILE = '_standard_nodes.json'
STANDARD_DRAWN = ('aliasOf', 'providesCapability', 'ariaRole', 'replacedBy')
""")
b = rep(b, """def asset_nodes(K=K):""", """def standard_nodes(K=K):
    \"\"\"(nodes, edges) from knowledge/_standard_nodes.json — the token reader's shape: a missing or
    unreadable file is [], [].\"\"\"
    fp = os.path.join(K, STANDARD_FILE)
    if not os.path.exists(fp): return [], []
    try: d = json.load(open(fp))
    except Exception: return [], []
    return d.get('nodes', []), d.get('edges', [])


def asset_nodes(K=K):""")
b = rep(b, """            link(e['s'], None, e['type'], ASSET_FAM, note=note); rep['asset_edges_null'] += 1""",
        """            link(e['s'], None, e['type'], ASSET_FAM, note=note, theme=e.get('theme'), ruling=e.get('ruling'))  # 1.37: the theme rides, so E4 can point it at theme:<it>
            rep['asset_edges_null'] += 1""")
b = rep(b, """    # ---- F. THE DOUBLE-NAMED FILE (#281, s281-D2).""", """    # ---- E4. THE FIVE EDGES (1.37, #311 lane D3, s308-D28). Same shape as E2/E3: never restate a node another
    # family owns; an edge whose ends are not both known is SKIPPED and counted, never guessed. Then (c): a
    # defaultFor line declared null with a `theme` qualifier now points at theme:<that> — the theme node kind.
    XN, XE = standard_nodes(K)
    for n in XN:
        claims[n['id']].add(n.get('fam') or ASSET_FAM)
        if n['id'] in base or n['id'] in nodes: continue
        add(n['id'], n.get('label') or n['id'], n.get('fam') or ASSET_FAM,
            **{k: v for k, v in n.items() if k not in ('id', 'label', 'fam', 'type')})
        rep['standard_nodes'] += 1
    known_x = base | set(nodes)
    for e in XE:
        if e.get('s') in known_x and e.get('t') in known_x and e.get('type') in STANDARD_DRAWN:
            link(e['s'], e['t'], e['type'], e.get('fam') or ASSET_FAM, note=(e.get('note') or '')[:320], maker=e.get('maker'),
                 **{k: e[k] for k in ('version', 'released', 'ruling', 'leaves') if k in e}); rep['standard_edges'] += 1
        else: _skip(rep, 'standard_edges_skipped', e)
    for e in edges:
        if e.get('type') == 'defaultFor' and e.get('t') is None and e.get('theme') and ('theme:' + e['theme']) in nodes:
            e['t'] = 'theme:' + e['theme']; rep['defaultFor_to_theme'] += 1; rep['asset_edges_null'] -= 1

    # ---- F. THE DOUBLE-NAMED FILE (#281, s281-D2).""")
open(B, 'w', encoding='utf-8').write(b)

# template: two node kinds (colour + TYPES2), four edge types in the FAMILY map
t = rep(t, "--c-capability:#2F7A6B;--f-sources:#3F5AA8;", "--c-capability:#2F7A6B;--c-theme:#8A5A1F;--c-aria:#2E6E8E;--f-sources:#3F5AA8;")
t = rep(t, "--c-capability:#7FCBB9;--f-sources:#8FA4E8;", "--c-capability:#7FCBB9;--c-theme:#D9A867;--c-aria:#86C1DD;--f-sources:#8FA4E8;", 2)
t = rep(t, "'typestyle','file','figma','capability'];", "'typestyle','file','figma','capability','theme','aria'];")
t = rep(t, "  setIn:'sources',behaviourFrom:'sources',capturedFrom:'sources',acceptsCapability:'sources',\n",
        "  setIn:'sources',behaviourFrom:'sources',capturedFrom:'sources',acceptsCapability:'sources',\n"
        "  // 1.37 (#311 lane D3, s308-D28) — the five edges the outside world has: token alias in Tokens, the providing\n"
        "  // half of a capability in Sources, a component's ARIA role beside the WCAG criteria, replacement in Structure.\n"
        "  aliasOf:'tokens',providesCapability:'sources',ariaRole:'guidelines',replacedBy:'structure',\n")
open(T, 'w', encoding='utf-8').write(t)
print('patched builder 1.37 + template')
