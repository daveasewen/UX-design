import sys
from PIL import Image
out=sys.argv[1]; cols=int(sys.argv[2]); files=sys.argv[3:]
ims=[Image.open(f).convert('RGB') for f in files]
w=max(i.width for i in ims); h=max(i.height for i in ims)
rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*w+(cols-1)*8, rows*h+(rows-1)*8),(255,0,255))
for k,i in enumerate(ims): S.paste(i,((k%cols)*(w+8),(k//cols)*(h+8)))
if S.width>2400: S=S.resize((2400,int(S.height*2400/S.width)))
S.save(out)
