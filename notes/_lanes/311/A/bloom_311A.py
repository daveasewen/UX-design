"""#311 lane A — the repo's bloom model (reviews/_rag_bloom_model.py) on the BUILT inks, loaded without its prints
(as notes/_lanes/310/C/bloom_options.py). Scores are relative; 100 = a 40px white fill on #1A1A1A."""
src=open('reviews/_rag_bloom_model.py').read(); src=src[:src.index("DPG='#1A1A1A'")]
ns={}; exec(src,ns); B,wcag=ns['B'],ns['wcag']
rows=[("Before: #FFFFFF on the black tile","#FFFFFF","#000000"),("After: #E1E1E1 on the black tile","#E1E1E1","#000000"),
      ("Before: #FFFFFF on the grey ground #1F1F1F","#FFFFFF","#1F1F1F"),("After: #E1E1E1 on the grey ground #1F1F1F","#E1E1E1","#1F1F1F"),
      ("Before: #FFFFFF on the page #1A1A1A","#FFFFFF","#1A1A1A"),("After: #E1E1E1 on the page #1A1A1A","#E1E1E1","#1A1A1A"),
      ("Supercharge, unchanged: #F7F6F4 on its #13110E tile","#F7F6F4","#13110E"),
      ("Common secondary, unchanged: #9B9B9B on the black tile","#9B9B9B","#000000")]
print(f"{'pair':56} {'text 2px':>9} {'value 5px':>9} {'wcag':>6}")
for lab,fg,bg in rows: print(f"{lab:56} {B(fg,bg,2):9} {B(fg,bg,5):9} {wcag(fg,bg):6.2f}")
