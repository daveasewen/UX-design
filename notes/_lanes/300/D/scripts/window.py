import json, tiktoken
enc=tiktoken.get_encoding('cl100k_base')
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
L=open(P).read().split('\n')
def tk(s): return len(enc.encode(s, disallowed_special=()))
for i in range(123,135):
    if not L[i].strip(): continue
    d=json.loads(L[i]); t=d.get('type')
    if t=='attachment':
        a=d['attachment']; s=json.dumps(a,ensure_ascii=False)
        body=a.get('content') if isinstance(a.get('content'),str) else s
        print(i,t,a.get('type'),'json-chars',len(s),'cl100k(json)',tk(s),'cl100k(content)',tk(body))
    elif t in('user','assistant'):
        m=d.get('message',{}); c=m.get('content')
        s=c if isinstance(c,str) else json.dumps(c,ensure_ascii=False)
        print(i,t,'chars',len(s),'cl100k',tk(s))
    else:
        print(i,t)
