import re
p = 'knowledge/_validate_edges.py'
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)

rep("""              A node's kind is its id's prefix before the first colon. Prints COUNTS first, then every""",
"""              and THE ACCEPTS (s308-D40, advisory first; s308-D43's four limits; #309 lane B). Every
              containedBy line, child → parent, against the parent's kind-bearing slots
              (`slots.<n>.accepts.kind`) or, with none, what the parent's KIND accepts
              (register `$containers.kinds`). Component kinds are read from each meta's `kind`
              (an alias seat is its owner's kind); a subcomponent: node is a part; a line carrying
              `part` is accepted by the parent's own part row (subComponents).
                NOT-ACCEPTED      the parent does not accept the child's kind
                CARD-HOLDS        a record (a card) holding a layout, a housing or another record
                TOO-MANY          a tile (register `$containers.tiles`) accepting through a multiple slot
                TILE-IN-TILE      a tile directly inside a tile (nest through a bento)
                MIXED-SLOTS       a sameKind slot (a carousel's slides) accepting two kinds
                MISSING           a required kind-bearing slot that accepts no line
                NO-KIND           a component meta with no kind (an alias seat excepted)
                LONE-CARD         WARNS only: a record accepted by a housing through no multiple slot
                                  (a lone card is a tile) — never turns the exit red
              A node's kind is its id's prefix before the first colon. Prints COUNTS first, then every""")

rep("""SHAPE_KEYS = ('self', 'loops', 'bothWays', 'chains')
""", """SHAPE_KEYS = ('self', 'loops', 'bothWays', 'chains')
ACCEPT_CLASSES = ('NOT-ACCEPTED', 'CARD-HOLDS', 'TOO-MANY', 'TILE-IN-TILE', 'MIXED-SLOTS', 'MISSING', 'NO-KIND',
                  'LONE-CARD')   # s308-D40 / s308-D43 (#309 lane B)
ACCEPT_WARN_ONLY = ('LONE-CARD',)   # s308-D43: 'the first three refuse, and the lone-card rule warns'
""")

rep("""def _cycles(P):""", '''def load_metas(K=HERE):
    """{'component:<stem>': meta} for every knowledge/components/<stem>.meta.json."""
    d = os.path.join(K, 'components')
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith('.meta.json'):
            with open(os.path.join(d, f), encoding='utf-8') as fh:
                out['component:' + f[:-len('.meta.json')]] = json.load(fh)
    return out


def node_kind(nid, metas):
    """The container kind of a node: a subcomponent is a part; a component is its meta's `kind`, an alias
    seat its owner's; anything else has none (None)."""
    if kind_of(nid) == 'subcomponent':
        return 'part'
    m = metas.get(nid)
    if not isinstance(m, dict):
        return None
    if isinstance(m.get('aliasOf'), dict):
        own = m['aliasOf'].get('component')
        return node_kind(own, metas) if own and own != nid else None
    return m.get('kind')


def kind_slots(meta):
    """{slot: slotEntry} for the slots that say which kinds they accept."""
    sl = (meta or {}).get('slots')
    return {n: v for n, v in (sl.items() if isinstance(sl, dict) else [])
            if not n.startswith('$') and isinstance(v, dict) and ((v.get('accepts') or {}).get('kind'))}


def check_accepts(edges, metas, containers):
    """s308-D40 + s308-D43 (#309 lane B). {'lines', 'accepted', 'derived', 'byClass', 'failures'}; a failure is
    (class, 'containedBy', s, t, detail). `derived` lists (s, t, slot) for every line a kind-bearing slot accepted."""
    kinds = containers.get('kinds') or {}
    tiles = set(containers.get('tiles') or [])
    failures, derived, filled = [], [], defaultdict(list)
    for nid, m in sorted(metas.items()):
        if isinstance(m, dict) and 'aliasOf' not in m and m.get('kind') not in kinds:
            failures.append(('NO-KIND', 'containedBy', nid, None, f"declares kind {m.get('kind')!r}; one of {sorted(kinds)} is required"))
    lines = [e for e in edges if e.get('type') == 'containedBy' and e.get('t')]
    accepted = 0
    for e in lines:
        s, t = e['s'], e['t']
        ck, pk = node_kind(s, metas), node_kind(t, metas)
        if ck not in kinds or pk not in kinds:
            continue            # NO-KIND names the meta; the line cannot be judged without it
        pm = metas.get(t) or {}
        if e.get('part'):
            sc = pm.get('subComponents')
            if isinstance(sc, dict) and e['part'] in sc:
                accepted += 1; continue
            failures.append(('NOT-ACCEPTED', 'containedBy', s, t, f"names part {e['part']!r}, which {t}'s subComponents do not")); continue
        if ck in (kinds[pk].get('never') or []):
            failures.append(('CARD-HOLDS', 'containedBy', s, t, f"a {pk} (a card) holding a {ck}; a card never holds a layout, a housing or another record")); continue
        if s in tiles and t in tiles:
            failures.append(('TILE-IN-TILE', 'containedBy', s, t, 'a tile directly inside a tile; nest through a bento')); continue
        slots = kind_slots(pm)
        slot = None
        if ck == 'part' and ck in (kinds[pk].get('accepts') or []):
            ok = True                 # a part fills its parent's part row, not a content slot
        elif slots:
            slot = next((n for n, v in slots.items() if ck in v['accepts']['kind']), None)
            ok = slot is not None
        else:
            ok = ck in (kinds[pk].get('accepts') or [])
        if not ok:
            where = (f"its slots accept {sorted({k for v in slots.values() for k in v['accepts']['kind']})}" if slots
                     else f"a {pk} accepts {kinds[pk].get('accepts')}")
            failures.append(('NOT-ACCEPTED', 'containedBy', s, t, f"a {ck} in a {pk}; {where}")); continue
        accepted += 1
        sv = slots.get(slot) if slot else None
        if slot:
            derived.append((s, t, slot)); filled[(t, slot)].append((ck, s))
        if t in tiles and sv and sv.get('multiple'):
            failures.append(('TOO-MANY', 'containedBy', s, t, f"tile slot {slot!r} is multiple; a tile holds exactly one thing"))
        if ck == 'record' and pk == 'housing' and not (sv and sv.get('multiple')):
            failures.append(('LONE-CARD', 'containedBy', s, t, 'a record alone in a housing: a lone card is a tile (warns)'))
    for (t, slot), kids in sorted(filled.items()):
        if kind_slots(metas.get(t)).get(slot, {}).get('sameKind') and len({k for k, _ in kids}) > 1:
            failures.append(('MIXED-SLOTS', 'containedBy', None, t, f"slot {slot!r} holds {sorted({k for k, _ in kids})}; its slides all hold the same kind"))
    for t, m in sorted(metas.items()):
        for n, v in kind_slots(m).items():
            if v.get('required') and not filled.get((t, n)):
                failures.append(('MISSING', 'containedBy', None, t, f"required slot {n!r} (accepts {v['accepts']['kind']}) accepts no containedBy line"))
    byc = Counter(c for c, *_ in failures)
    return {'lines': len(lines), 'accepted': accepted, 'derived': derived,
            'byClass': {c: byc[c] for c in ACCEPT_CLASSES}, 'failures': failures,
            'refusals': sum(n for c, n in byc.items() if c not in ACCEPT_WARN_ONLY)}


def print_accepts(acc):
    shown = {c: n for c, n in acc['byClass'].items() if n}
    print(f"  accepts: {acc['lines']} containedBy lines · accepted {acc['accepted']} · through a kind-bearing slot "
          f"{len(acc['derived'])} · by class {shown or 'none'}")
    for s, t, slot in acc['derived']:
        print(f"  · derived: {t} accepts {s} (slot {slot!r}, by kind)")
    for c, ty, s, t, d in acc['failures']:
        print(f"  {'!' if c in ACCEPT_WARN_ONLY else '✗'} {c:16} {ty:18} {s} → {t}   {d}")
    print('EDGE ACCEPTS: ' + ('every containedBy line is accepted by its parent' if not acc['refusals']
                              else 'REFUSALS above (ADVISORY first, s308-D40)')
          + (f" · warnings {sum(acc['byClass'][c] for c in ACCEPT_WARN_ONLY)}" if any(acc['byClass'][c] for c in ACCEPT_WARN_ONLY) else ''))


def _cycles(P):''')

rep("""    res = check_ends(edges, rows)
    shp = check_shape(edges, rows)
    if '--json' in argv:
        out = {k: v for k, v in res.items() if k != 'failures'}
        out['shape'] = {k: v for k, v in shp.items() if k != 'failures'}
        print(json.dumps(out, sort_keys=True))
    else:
        print_ends(res, rows, how, drift(edges, rows), shp)
    return 1 if (res['fail'] or res['byClass']['OVER-COUNT'] or any(shp['byClass'].values())) else 0""",
"""    res = check_ends(edges, rows)
    shp = check_shape(edges, rows)
    acc = check_accepts(edges, load_metas(), reg.get('$containers') or {})
    if '--json' in argv:
        out = {k: v for k, v in res.items() if k != 'failures'}
        out['shape'] = {k: v for k, v in shp.items() if k != 'failures'}
        out['accepts'] = {k: v for k, v in acc.items() if k not in ('failures', 'derived')}
        print(json.dumps(out, sort_keys=True))
    else:
        print_ends(res, rows, how, drift(edges, rows), shp)
        print_accepts(acc)
    return 1 if (res['fail'] or res['byClass']['OVER-COUNT'] or any(shp['byClass'].values()) or acc['refusals']) else 0""")

rep("""    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))""",
'''    # — s308-D40 / s308-D43 (#309 lane B): the accepts check and the four nesting limits
    metas, cont = load_metas(), reg.get('$containers') or {}
    acc0 = check_accepts(edges, metas, cont)

    def acc_red(cls, e2=None, metas2=None, cont2=None):
        a = check_accepts(e2 if e2 is not None else edges, metas2 if metas2 is not None else metas,
                          cont2 if cont2 is not None else cont)
        return a['byClass'][cls] == acc0['byClass'][cls] + 1
    CB = lambda s_, t_: {'s': 'component:' + s_, 't': 'component:' + t_, 'type': 'containedBy'}
    d34 = ('component:cards', 'component:carousel', 'slides')
    bite(26, f"CONTROL (accepts): {acc0['lines']} containedBy lines judged, {acc0['accepted']} accepted, "
             f"{acc0['refusals']} refusal(s) on the real tree; s308-D34 'a carousel holds cards' is DERIVED — Cards (record) "
             f"accepted by Carousel's slides slot, no authored pair",
         lambda: d34 in acc0['derived'] and check_accepts(edges, metas, cont)['byClass'] == acc0['byClass'])
    bite(27, "CARD-HOLDS: the s308-D34 line reversed (a carousel inside Cards) goes red",
         lambda: acc_red('CARD-HOLDS', edges + [CB('carousel', 'cards')]))
    bite(28, "NOT-ACCEPTED: a layout (template-dashboard) inside a block (button) goes red",
         lambda: acc_red('NOT-ACCEPTED', edges + [CB('template-dashboard', 'button')]))
    c29 = dict(cont, tiles=['component:drawer', 'component:modals'])
    bite(29, "TILE-IN-TILE: with two housings declared tiles, one directly inside the other goes red",
         lambda: acc_red('TILE-IN-TILE', edges + [CB('drawer', 'modals')], cont2=c29))
    c30 = dict(cont, tiles=['component:carousel'])
    bite(30, "TOO-MANY: a tile whose accepting slot is multiple (Carousel planted as a tile) goes red",
         lambda: acc_red('TOO-MANY', cont2=c30))
    bite(31, "MIXED-SLOTS: an image block beside Cards in Carousel's slides goes red",
         lambda: acc_red('MIXED-SLOTS', edges + [CB('image-block', 'carousel')]))
    bite(32, "MISSING: Carousel's required slides slot with its one line taken away goes red",
         lambda: acc_red('MISSING', [e for e in edges if not (e['type'] == 'containedBy' and (e['s'], e['t']) == d34[:2])]))
    m33 = copy.deepcopy(metas); m33['component:button'].pop('kind', None)
    bite(33, "NO-KIND: Button without its kind goes red", lambda: acc_red('NO-KIND', metas2=m33))
    bite(34, "LONE-CARD WARNS: a record alone in a housing (account-card in a drawer) is named, and the refusal count does not move",
         lambda: acc_red('LONE-CARD', edges + [CB('account-card', 'drawer')])
         and check_accepts(edges + [CB('account-card', 'drawer')], metas, cont)['refusals'] == acc0['refusals'])
    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))''')
open(p, 'w', encoding='utf-8').write(s)
print('patched')
