# #296 lane C - the SAME chapter rail into the v14-plant deck. Style, nav and script come from
# build_c.py unchanged; only the chapters list differs. Rebuilds from v14-plant-before-rail.html.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_c
R = os.path.abspath('.') + '/'
SRC = R + 'notes/_lanes/296/C/v14-plant-before-rail.html'
DST = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plant.html'
PLANT_CHAPTERS = '''  chapters: [
    {n:1, title:'Why now',               id:'s3',        subs:[]},
    {n:2, title:'Systemised design',     id:'s4',        subs:[]},
    {n:3, title:'The experiment',        id:'s5',        subs:[]},
    {n:4, title:'The insight',           id:'s5insight', subs:[]},
    {n:5, title:'The breakdown',         id:'s5break',   subs:[]},
    {n:6, title:'What we built',         id:'s6',        subs:['s7','s8']},
    {n:7, title:'The build and the ask', id:'s9',        subs:['s10','s10map','s11','s12']}
  ]
'''
build_c.build(SRC, DST, PLANT_CHAPTERS)
# the rail code must be byte-identical between the two decks, chapters list excluded
import re
def blocks(path):
    h = open(path, encoding='utf-8').read()
    s = h.index('<style data-lane="296-C">'); e = h.index('</nav>\n', s) + 7
    t = h.index('<script data-lane="296-C">'); u = h.index('</script>\n', t) + 10
    sc = h[t:u]; a = sc.index('  chapters: ['); b = sc.index('  ]\n};', a) + 6
    return h[s:e], sc[:a] + sc[b:]
A = blocks(build_c.DST); B = blocks(DST)
assert A[0] == B[0] and A[1] == B[1], 'rail code differs between decks'
print('rail code identical (style+nav %d B, script minus chapters %d B)' % (len(A[0]), len(A[1])))
