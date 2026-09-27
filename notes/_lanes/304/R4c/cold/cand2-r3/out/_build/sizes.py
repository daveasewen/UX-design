import os, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand2-r3'); js = open(W + '/tools/size.js').read()
SN = W + '/pack/knowledge/snippets/'
ref = ['Kpi-tile', 'Dropdown', 'Segmented-control', 'Button', 'List-items', 'Summary', 'Data-grid', 'Drawer', 'App-shell-side-nav', 'Chart-line', 'Chart-bar', 'Input-fields', 'Textarea', 'Toast']
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); ctx = b.new_context(viewport={'width': 1600, 'height': 1000})
    showroom = {}
    for n in ref:
        pg = ctx.new_page(); pg.goto('file://' + SN + n + '.reference.html'); pg.wait_for_timeout(500)
        if n == 'Drawer': pg.evaluate("document.getElementById('open') && document.getElementById('open').click()"); pg.wait_for_timeout(400)
        if n == 'Toast': pg.evaluate("document.getElementById('spawnOk') && document.getElementById('spawnOk').click()"); pg.wait_for_timeout(300)
        r = pg.evaluate(js); showroom.update({k: v for k, v in r.items() if v is not None and k not in showroom}); pg.close()
    mine = {}
    for pgname in ['index', 'accounts', 'messages', 'settings']:
        pg = ctx.new_page(); pg.goto('file://' + W + '/out/' + pgname + '.html'); pg.wait_for_timeout(700)
        if pgname == 'accounts':
            pg.locator('#tbody tr[data-id] td').nth(2).click(); pg.wait_for_timeout(500)
        if pgname == 'settings':
            pg.locator('label[for="nt-weekly"]').click(); pg.wait_for_timeout(300)
        r = pg.evaluate(js); mine.update({k: v for k, v in r.items() if v is not None and k not in mine}); pg.close()
    for k in sorted(set(showroom) | set(mine)):
        s, m = showroom.get(k), mine.get(k)
        same = (s is not None and m is not None and s[0] == m[0])
        print(json.dumps({'part': k, 'showroom': s, 'page': m, 'height_equal': same}))
    b.close()
