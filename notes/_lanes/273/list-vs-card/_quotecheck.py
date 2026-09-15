import json,re,html,sys,unicodedata
PAGE="notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html"
SRC="notes/_lanes/272/harvest-decisions-2026-09-14.json"
src=json.load(open(SRC)); src=src.get("decisions",src)
allowed={k:src[k]["notes"] for k in ("B-09","B-10","B-20","N-account-card")}
txt=open(PAGE).read()
def norm(s):
    s=html.unescape(s)
    s=s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace("—","--")
    s=re.sub(r"<[^>]+>","",s)
    return re.sub(r"\s+"," ",s).strip()
# every curly-quoted span of 6+ words on the page
spans=re.findall(r"&ldquo;(.+?)&rdquo;",txt,re.S)
print("quoted spans found on page:",len(spans))
bad=0; dave=0; ext=0
for s in spans:
    n=norm(s)
    if len(n.split())<4: continue
    hit=[k for k,v in allowed.items() if n in norm(v)]
    if hit:
        dave+=1; print("  DAVE  OK  [%s] %s..."%(hit[0],n[:60]))
    else:
        ext+=1; print("  EXT   (external/system quote, %d words) %s..."%(len(n.split()),n[:70]))
        if len(n.split())>=15:
            bad+=1; print("     !! EXTERNAL QUOTE >=15 WORDS")
print("\nDave spans: %d  external spans: %d  over-length external: %d"%(dave,ext,bad))
# also: any <blockquote class="dave"> must match verbatim
for m in re.finditer(r'<blockquote class="dave">&ldquo;(.+?)&rdquo;<cite>(.+?)</cite>',txt,re.S):
    n=norm(m.group(1)); rid=m.group(2).split(" ")[0]
    ok = n == norm(allowed[rid])
    print("blockquote %-15s verbatim-exact: %s"%(rid, ok))
    if not ok:
        print("   page:",n); print("   src :",norm(allowed[rid]))
sys.exit(1 if bad else 0)
