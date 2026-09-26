#!/usr/bin/env python3
"""kg_tokens_patch.py ROOT — #304 R3: teach the KG explorer (builder + template) and the verbs map the
token family landed by knowledge/gen_kg_tokens.py under s277-D12. Idempotent (a second run prints
ALREADY per edit and writes nothing); every edit asserts its anchor occurs EXACTLY once, else refuses.
Edits: builder VERSION 1.27 -> 1.28 with a version line; a TOKEN_FILE/TOKEN_FAM reader; pass E2 after
the assets pass; the column in place_extra; the view map; SRC_BY_TYPE; the XTRA counts and a print
line. Template: --c-token/--f-tokens in the three colour blocks (not a red: s151-D1 untouched);
FAMILY bindsToken:'tokens'; FAMLABEL; the System view's fams; NEWFAM; TYPES2; famOn tokens:0 (OFF by
default, like every additive family); READ; EFAMFILE. _kg_verbs.json: bindsToken under `unread` with a
note (the usesIcon precedent: a verb for it is Dave's to ratify, not this lane's to pad)."""
import json, os, sys
if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
K = os.path.join(ROOT, "knowledge")

def edit(path, old, new, tag):
    s = open(path, encoding="utf-8").read()
    if new in s:
        print("ALREADY", tag); return
    n = s.count(old)
    if n != 1:
        sys.exit("REFUSE %s: anchor occurs %d times in %s" % (tag, n, path))
    open(path, "w", encoding="utf-8").write(s.replace(old, new))
    print("EDITED ", tag)

B = os.path.join(K, "_build_kg_explorer.py")
T = os.path.join(K, "_kg_explorer.template.html")
VLINE = ('VERSION = "1.28"  # 1.28 (#304 R3, s277-D12 — Dave 2026-09-16, audit D-5 (a): "TOKENS ENTER THE GRAPH AT GROUP GRAIN WITH THEIR TIER ... with a structural `bindsToken` from the metas\' typed `tokens` block") A SIXTH ADDITIVE FAMILY, `tokens`, behind its own chip in the SYSTEM view, OFF by default like every additive family: the token: nodes and bindsToken edges landed by `gen_kg_tokens.py --land --ratified s277-D12` into knowledge/_token_nodes.json (group grain; tier, source and blast carried as node attributes; `paths` on each edge). Read by the same reader shape as the assets family (pass E2, after E); laid out in its own column right of assets; `token` gets a type colour and the family a stroke colour, neither a red. NO existing node id, edge type, file or fam KEY moves and no edge is invented; the default canvas does not move, because the chip loads OFF. · 1.27 ')
edit(B, 'VERSION = "1.27"  # 1.27 ', VLINE, "builder VERSION 1.28")
edit(B, "def asset_nodes(K=K):",
     "# #304 R3 s277-D12 — the tokens family: token:<group> nodes + bindsToken, landed by gen_kg_tokens.py\n"
     "TOKEN_FILE = '_token_nodes.json'\n"
     "TOKEN_FAM = 'tokens'   # the landed file's own `family` key; free in FAMILY/FAMLABEL (checked #304 R3)\n"
     "TOKEN_DRAWN = ('bindsToken',)\n\n\n"
     "def token_nodes(K=K):\n"
     "    \"\"\"(nodes, edges) from knowledge/_token_nodes.json — the asset reader's shape: a missing or\n"
     "    unreadable file is [], [].\"\"\"\n"
     "    fp = os.path.join(K, TOKEN_FILE)\n"
     "    if not os.path.exists(fp): return [], []\n"
     "    try: d = json.load(open(fp))\n"
     "    except Exception: return [], []\n"
     "    return d.get('nodes', []), d.get('edges', [])\n\n\n"
     "def asset_nodes(K=K):", "builder token_nodes reader")
edit(B, "    # ---- F. THE DOUBLE-NAMED FILE (#281, s281-D2).",
     "    # ---- E2. THE TOKENS FAMILY (#304 R3, s277-D12). Same shape as E: never restate a node another\n"
     "    # family owns; an edge whose ends are not both known is SKIPPED and counted, never guessed.\n"
     "    TN, TE = token_nodes(K)\n"
     "    for n in TN:\n"
     "        claims[n['id']].add(TOKEN_FAM)\n"
     "        if n['id'] in base or n['id'] in nodes: continue\n"
     "        add(n['id'], n.get('label') or n['id'], TOKEN_FAM,\n"
     "            **{k: v for k, v in n.items() if k not in ('id', 'label', 'fam', 'type')})\n"
     "        rep['token_nodes'] += 1\n"
     "    known_t = base | set(nodes)\n"
     "    for e in TE:\n"
     "        if e.get('s') in known_t and e.get('t') in known_t and e.get('type') in TOKEN_DRAWN:\n"
     "            link(e['s'], e['t'], e['type'], TOKEN_FAM, paths=e.get('paths')); rep['token_edges'] += 1\n"
     "        else: rep['token_edges_skipped'] += 1\n\n"
     "    # ---- F. THE DOUBLE-NAMED FILE (#281, s281-D2).", "builder pass E2")
edit(B, "(RULE_FAM, 2.2), (UX_FAM, -2.2), (ASSET_FAM, 3.4)):",
     "(RULE_FAM, 2.2), (UX_FAM, -2.2), (ASSET_FAM, 3.4), (TOKEN_FAM, 4.6)):", "builder column")
edit(B, "UX_FAM: 'explain', ASSET_FAM: 'system', 'governance': 'constitution'}",
     "UX_FAM: 'explain', ASSET_FAM: 'system', TOKEN_FAM: 'system', 'governance': 'constitution'}", "builder view map")
edit(B, "    'logo':      'knowledge/_logo_nodes.json',\n}",
     "    'logo':      'knowledge/_logo_nodes.json',\n    'token':     'knowledge/_token_nodes.json',   # #304 R3 s277-D12\n}", "builder SRC_BY_TYPE")
edit(B, "                      'assetNulls': rep.get('asset_edges_null', 0),\n",
     "                      'assetNulls': rep.get('asset_edges_null', 0),\n"
     "                      'tokens': rep.get('token_nodes', 0), 'tokenEdges': rep.get('token_edges', 0),\n", "builder XTRA counts")
edit(B, "    print(\"  strata bands (#280, s277-D8 rendered): \"",
     "    print(f\"  tokens family (s277-D12, ratified s277-D12; chip OFF by default): {rep.get('token_nodes', 0)} new nodes\"\n"
     "          f\" / {rep.get('token_edges', 0)} bindsToken\"\n"
     "          + (f\" · SKIPPED {rep['token_edges_skipped']}\" if rep.get('token_edges_skipped') else ''))\n"
     "    print(\"  strata bands (#280, s277-D8 rendered): \"", "builder print line")

# ---- template
edit(T, "  --c-icon:#0B7285;--c-iconGroup:#075A6A;--c-logo:#4E6E8E;--f-assets:#0B7285;\n  --mono:",
     "  --c-icon:#0B7285;--c-iconGroup:#075A6A;--c-logo:#4E6E8E;--f-assets:#0B7285;\n"
     "  /* #304 R3 s277-D12 — the tokens family: an ochre for the token: group node and its bindsToken lines. Not a red (s151-D1). */\n"
     "  --c-token:#8A6A12;--f-tokens:#8A6A12;\n  --mono:", "template light colours")
s = open(T, encoding="utf-8").read()
dark_old = "    --c-icon:#4FC3D9;--c-iconGroup:#8BD3E3;--c-logo:#9AB4D1;--f-assets:#4FC3D9;\n  }\n}"
dark_new = "    --c-icon:#4FC3D9;--c-iconGroup:#8BD3E3;--c-logo:#9AB4D1;--f-assets:#4FC3D9;\n    --c-token:#E2C263;--f-tokens:#E2C263;\n  }\n}"
edit(T, dark_old, dark_new, "template dark colours (media)")
edit(T, "  --c-icon:#4FC3D9;--c-iconGroup:#8BD3E3;--c-logo:#9AB4D1;--f-assets:#4FC3D9;\n}",
     "  --c-icon:#4FC3D9;--c-iconGroup:#8BD3E3;--c-logo:#9AB4D1;--f-assets:#4FC3D9;\n  --c-token:#E2C263;--f-tokens:#E2C263;\n}", "template dark colours (attr)")
edit(T, "  inGroup:'assets',activeVariantOf:'assets',usesIcon:'assets',usesLogo:'assets',defaultFor:'assets',ruledBy:'assets',\n",
     "  inGroup:'assets',activeVariantOf:'assets',usesIcon:'assets',usesLogo:'assets',defaultFor:'assets',ruledBy:'assets',\n"
     "  // #304 R3 s277-D12 — the tokens family's one edge type, its own family and chip (OFF by default).\n"
     "  bindsToken:'tokens',\n", "template FAMILY")
edit(T, "rules:'Rules & wiring',assets:'Assets',", "rules:'Rules & wiring',assets:'Assets',tokens:'Tokens',", "template FAMLABEL")
edit(T, "fams:['structure','usage','render','rules','assets']}", "fams:['structure','usage','render','rules','assets','tokens']}", "template VIEWS system")
edit(T, "const NEWFAM=['governance','guidelines','guidelinerules','uxprinciples','assets'];",
     "const NEWFAM=['governance','guidelines','guidelinerules','uxprinciples','assets','tokens'];", "template NEWFAM")
edit(T, "'icon','iconGroup','logo'];", "'icon','iconGroup','logo','token'];", "template TYPES2")
edit(T, "uxprinciples:0,assets:0,designrulings:1", "uxprinciples:0,assets:0,tokens:0,designrulings:1", "template famOn")
edit(T, "const READ={containedBy:['is contained by','contains'],", "const READ={bindsToken:['binds token','is bound by'],containedBy:['is contained by','contains'],", "template READ")
edit(T, "assets:'knowledge/_icon_nodes.json · knowledge/_logo_nodes.json',\n",
     "assets:'knowledge/_icon_nodes.json · knowledge/_logo_nodes.json',tokens:'knowledge/_token_nodes.json',\n", "template EFAMFILE")

# ---- verbs map: bindsToken read by no verb yet -> `unread` with a note. The file does not round-trip
# through json.dumps (hand-shaped layout), so the entry is inserted as TEXT after the `"unread": {` line,
# in the file's own indentation, and the result is re-parsed to prove it is still JSON.
V = os.path.join(K, "_kg_verbs.json")
src = open(V, encoding="utf-8").read()
if '"bindsToken"' in src:
    print("ALREADY verbs unread bindsToken")
else:
    anchor = '\n "unread": {\n'
    if src.count(anchor) != 1:
        sys.exit("REFUSE verbs: anchor occurs %d times" % src.count(anchor))
    note = ("component \u2192 token: group \u2014 landed #304 R3 under s277-D12 (tokens at group grain with their tier, "
            "bindsToken from the metas' typed tokens block). The same join the slice's `tokens` field (Q9) reads from the meta; the explorer draws it under its "
            "own Tokens chip (off by default). No verb of the twelve names it \u2014 which verb reads it (the usesIcon note's own candidate is a thirteenth, 'uses') "
            "is Dave's to ratify, not this lane's to pad.")
    ntok = len(json.load(open(os.path.join(K, "_token_nodes.json"), encoding="utf-8")).get("edges", []))
    entry = '  "bindsToken": {\n   "$note": %s,\n   "count": %d,\n   "nulls": 0\n  },\n' % (json.dumps(note, ensure_ascii=False), ntok)
    out = src.replace(anchor, anchor + entry)
    d = json.loads(out)
    assert "bindsToken" in d["unread"] and set(json.loads(src)["unread"]) <= set(d["unread"])
    open(V, "w", encoding="utf-8").write(out)
    print("EDITED  verbs unread bindsToken")
