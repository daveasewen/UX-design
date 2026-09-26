import sys,re,html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style','svg','template'): s.skip+=1
        if t in('p','div','li','h1','h2','h3','h4','section','tr','br','td','th','figcaption'): s.out.append('\n')
        if t=='section':
            d=dict(a); s.out.append('\n=== SECTION %s %s ===\n'%(d.get('id',''),d.get('class','')))
    def handle_endtag(s,t):
        if t in('script','style','svg','template'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
    def handle_comment(s,d):
        if '--comments' in sys.argv: s.out.append('\n<!--'+d[:800]+'-->\n')
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=''.join(p.out); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
print(t)
