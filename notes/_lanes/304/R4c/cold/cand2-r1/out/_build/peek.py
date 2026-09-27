import sys,re
p=sys.argv[1]; mode=sys.argv[2] if len(sys.argv)>2 else 'body'
h=open(p,encoding='utf-8').read()
# strip demo fences
h2=re.sub(r'<!-- ===== APOLLO-DEMO (.*?) START.*?<!-- ===== APOLLO-DEMO \1 END ===== -->','[[DEMO:\\1]]',h,flags=re.S)
h2=re.sub(r'/\* ===== APOLLO-DEMO (.*?) START.*?/\* ===== APOLLO-DEMO \1 END ===== \*/','[[DEMOJS:\\1]]',h2,flags=re.S)
if mode=='body':
  m=re.search(r'<body[^>]*>(.*)</body>',h2,re.S); b=m.group(1)
  b=re.sub(r'(<script[^>]*>)(.*?)(</script>)',lambda m:m.group(1)+'[[SCRIPT %d chars]]'%len(m.group(2))+m.group(3),b,flags=re.S)
  b=re.sub(r'<svg.*?</svg>',lambda m:'<svg…%d>'%len(m.group(0)),b,flags=re.S)
  b=re.sub(r'\n\s*\n+','\n',b)
  print(b)
elif mode=='scripts':
  for m in re.finditer(r'<script([^>]*)>(.*?)</script>',h2,re.S):
    print('=== SCRIPT',m.group(1),len(m.group(2))); print(m.group(2)[:int(sys.argv[3]) if len(sys.argv)>3 else 3000])
elif mode=='comments':
  for m in re.finditer(r'<!--(.*?)-->',h2,re.S):
    print('---',m.group(1)[:600])
