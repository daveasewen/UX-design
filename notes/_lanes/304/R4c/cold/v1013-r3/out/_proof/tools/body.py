import re,sys
p=sys.argv[1]; w=int(sys.argv[2]) if len(sys.argv)>2 else 260
s=open(p).read()
s=re.sub(r'<!-- ===== APOLLO-DEMO (.*?) START.*?APOLLO-DEMO \1 END ===== -->','',s,flags=re.S)
s=re.sub(r'/\* ===== APOLLO-DEMO (.*?) START.*?APOLLO-DEMO \1 END ===== \*/','',s,flags=re.S)
b=s[s.find('<body'):]
b=re.sub(r'<script type="application/json" id="token-manifest">.*?</script>','[token-manifest]',b,flags=re.S)
b=re.sub(r'<!--.*?-->','',b,flags=re.S)
b=re.sub(r'<symbol.*?</symbol>','<symbol/>',b,flags=re.S)
mode=sys.argv[3] if len(sys.argv)>3 else 'all'
if mode=='noscript': b=re.sub(r'<script>.*?</script>','[script]',b,flags=re.S)
for l in b.split('\n'):
  if l.strip(): print(l[:w])
