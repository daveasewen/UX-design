import re,sys
def clean(h):
  h=re.sub(r'<!-- ===== AUTO-BEHAVIOUR (\S+) START.*?AUTO-BEHAVIOUR \1 END ===== -->',lambda m:'[[AUTOB %s]]'%m.group(1),h,flags=re.S)
  return h
def figures(path):
  h=clean(open(path,encoding='utf-8').read())
  b=h[h.find('<body'):]
  out=[];pos=0
  while True:
    i=b.find('<figure',pos)
    if i<0: break
    # balanced figure
    depth=0;j=i
    for m in re.finditer(r'<(/?)figure\b',b[i:]):
      depth+= -1 if m.group(1) else 1
      if depth==0: j=i+m.end(); break
    j=b.find('>',j)+1
    out.append(b[i:j]); pos=j
  return out
if __name__=='__main__':
  fs=figures(sys.argv[1])
  for k,f in enumerate(fs):
    t=re.search(r'data-dv-type="([^"]+)"',f)
    print(k, t and t.group(1), len(f), re.search(r'data-lockup-title="([^"]*)"',f).group(1) if 'data-lockup-title' in f else '')
  if len(sys.argv)>2:
    f=fs[int(sys.argv[2])]
    f=re.sub(r'<!--.*?-->','',f,flags=re.S)
    f=re.sub(r'<svg class="dv-ico.*?</svg>','<ICO>',f,flags=re.S)
    f=re.sub(r'(<tbody[^>]*>).*?(</tbody>)',r'\1…\2',f,flags=re.S)
    f=re.sub(r'\n\s*\n+','\n',f)
    print(f)
